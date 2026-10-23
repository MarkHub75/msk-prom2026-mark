
### Search before asking

I searched the issues and found earlier reports of the same symptom class: #19991, #22737, #24861 (detection), and #5016 (classification, not tested here). This issue is the follow-up invited on closed PR #25481 — the test-only PR was closed with the note that a parity bug should come as an issue with a reproducer, which is what this is.

### Environment

Reproduces deterministically on two platforms, same code path:

| | Platform A | Platform B |
|---|---|---|
| OS / arch | macOS 26, arm64 (Apple M4) | Linux, x86_64 (Intel Xeon 2.20GHz, AVX2) |
| Python | 3.12.13 | 3.13.15 |
| ultralytics | 8.4.158 | 8.4.158 |
| torch | 2.14.0 | 2.11.0+cpu |
| onnxruntime | 1.30.0 (CPUExecutionProvider) | 1.30.0 (CPUExecutionProvider) |
| export | onnx 1.23.0, opset 18, all-default args | same |

Model: `yolov8n.pt` (public checkpoint), exported with `model.export(format="onnx", imgsz=640)` — no other settings.

### Problem

For non-square sources, inference through the default ONNX export produces a different detection set than the `.pt` model — beyond any floating-point margin: detections are dropped or added depending on the confidence threshold, matched boxes shift by ~12px, and confidences shift by up to ~0.17. The exported model and the `.pt` model are numerically near-identical when given the same input (control case below), so this is not kernel or export noise — the two predict paths feed the model different pixels.

### Minimal reproducer (37 lines, no custom helpers — repo utilities only)

```python
"""MRE: .pt and default-exported ONNX predictions disagree on non-square sources (ultralytics 8.4.158)."""
import cv2
from ultralytics import YOLO
from ultralytics.data.augment import LetterBox
from ultralytics.utils.metrics import box_iou

print(f"ultralytics ONNX backend: onnxruntime {__import__('onnxruntime').__version__} (CPUExecutionProvider)")
im = cv2.imread("bus.jpg")  # 810x1080 non-square source
model = YOLO("yolov8n.pt")  # public checkpoint
f = model.export(format="onnx", imgsz=640)  # default export settings
exported = YOLO(f)

pt = model.predict(im, imgsz=640, conf=0.15, verbose=False)[0].boxes.data
on = exported.predict(im, imgsz=640, conf=0.15, verbose=False)[0].boxes.data
print(f"\nnon-square source (bus.jpg 810x1080), conf=0.15: PyTorch={len(pt)} vs ONNX={len(on)} detections")

sq = LetterBox((640, 640), auto=False)(image=im)  # control: identical pixels to both backends
pt_sq = model.predict(sq, imgsz=640, conf=0.15, verbose=False)[0].boxes.data
on_sq = exported.predict(sq, imgsz=640, conf=0.15, verbose=False)[0].boxes.data
iou = box_iou(pt_sq[:, :4], on_sq[:, :4])
j = iou.argmax(1)
dxy = (pt_sq[:, :4] - on_sq[j, :4]).abs().max()
dcf = (pt_sq[:, 4] - on_sq[j, 4]).abs().max()
print(f"control, same square 640x640 input: PyTorch={len(pt_sq)} vs ONNX={len(on_sq)} detections, "
      f"min best-IoU {iou.max(1).values.min():.4f}, max box delta {dxy:.4f}px, max conf delta {dcf:.6f}")

assert len(pt) == len(on) and len(pt_sq) == len(on_sq) and iou.max(1).values.min() > 0.99, (
    f"divergence: non-square source gives pt={len(pt)} vs onnx={len(on)} detections, "
    "while identical square input agrees -> letterbox asymmetry, not kernel noise"
)
print("\nno divergence (fixed or not reproduced): backends agree on this source")
```

**Output (macOS arm64 — identical counts on Linux x86_64):**

```
ultralytics ONNX backend: onnxruntime 1.30.0 (CPUExecutionProvider)
non-square source (bus.jpg 810x1080), conf=0.15: PyTorch=6 vs ONNX=5 detections
control, same square 640x640 input: PyTorch=5 vs ONNX=5 detections, min best-IoU 1.0000, max box delta 0.0001px, max conf delta 0.000001
AssertionError: divergence: non-square source gives pt=6 vs onnx=5 detections, while identical square input agrees -> letterbox asymmetry, not kernel noise
```

### Root cause

`BasePredictor.pre_transform` in `ultralytics/engine/predictor.py` (lines 212–219 in 8.4.158):

```python
same_shapes = len({x.shape for x in im}) == 1
letterbox = LetterBox(
    self.imgsz,
    auto=same_shapes
    and self.args.rect
    and (self.model.format == "pt" or (getattr(self.model, "dynamic", False) and self.model.format != "imx")),
    stride=self.model.stride,
)
```

`auto=True` — rect letterboxing with minimal stride-aligned padding — applies **only when `model.format == "pt"`** (or for dynamic-shape non-imx exports). A static ONNX export always receives square `imgsz × imgsz` letterboxing. For any non-square source the two paths therefore run the same weights on different input tensors, and every downstream difference follows from that. The control case in the MRE (identical square input) shows the exported graph agrees with PyTorch to ~1e-4 px / ~1e-6 confidence, i.e. ordinary fp32 kernel variance.

Note the same gate also means `dynamic=True` exports can rect-letterbox while static exports cannot, so even two ONNX exports of the same model can disagree with each other on non-square sources.

### Measured impact (bus.jpg, 810×1080, imgsz=640)

Detection counts by confidence threshold (yolov8n, `.pt` vs static ONNX):

| conf | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 (default) | 0.30 | 0.35 | 0.40 | 0.45–0.65 |
|---|---|---|---|---|---|---|---|---|---|
| PyTorch | 13 | 6 | **6** | 6 | 5 | 4 | 4 | 4 | 4 |
| ONNX | 7 | 6 | **5** | 5 | 5 | 5 | 5 | 5 | 4 |

At the default `conf=0.25` the counts happen to match, but only 3 of 5 detections IoU-match (>0.5) across backends; matched pairs differ by up to **12.1 px** and **0.169 confidence**.

Concrete production impact on `yolo26n.pt` (same mechanism): at `conf=0.60` the `.pt` model reports 5 detections, the exported model 4 — the 5th (a person) has confidence 0.654 native vs 0.5563 exported, so it silently disappears from an ONNX deployment. The bus box itself moves by 10.1 px (x-origin 0.0 vs 10.1).

### Raw-head tolerance floor (context for any future parity testing)

Calibration sweep: 50 images derived from `bus.jpg` (contrast / gamma / scale / aspect-ratio / flip variants), default export (raw one-to-many head, no NMS), FP32 PyTorch forward vs ONNX Runtime CPU on identical preprocessed input — absolute error over the full `(1, 84, 8400)` head output:

| model | platform | conf max | conf P99.9 | box (xywh) max |
|---|---|---|---|---|
| yolov8n | macOS arm64 | 4.7e-05 | 1.2e-07 | 3.5e-03 px |
| yolov8n | Linux x86_64 (AVX2) | 3.3e-05 | 1.2e-07 | 5.2e-03 px |
| yolo26n | macOS arm64 | 8.0e-05 | 1.1e-07 | 1.2e-02 px |
| yolo26n | Linux x86_64 (AVX2) | 1.5e-05 | 1.1e-07 | 1.6e-02 px |

Kernel-level parity is ≤1e-4 confidence and ≤0.02 px on both platforms — three to four orders of magnitude below the detection-level divergence above. This is also why the tolerances in the closed PR #25481 (12 px / 0.12 conf, sized to "observed cross-platform fp32 variance") were measuring the wrong thing: they were absorbing this deterministic preprocessing asymmetry, not fp32 noise, while a genuine kernel-level export regression at 1e-3 confidence would still have passed.

### Suggested directions (maintainer's call)

1. Make the letterbox contract consistent across formats: either give static exports the same rect policy when shape allows, or make `.pt` predict use the square policy that static exports will see. Today the same `imgsz` argument silently means "long-side, minimal padding" for `.pt` and "exact square" for static exports.
2. Interim: document the behavior in the export docs and/or log a one-time notice when a static-shape model is predicted on a non-square source, pointing at `dynamic=True` for consistent rect behavior.
3. If an export parity test is ever reconsidered: run both backends on identical square-letterboxed input and assert near the measured kernel floor (~1e-3 px / 1e-4 conf). That is tight, deterministic, and non-flaky — unlike detection-level tolerances, which sit on top of this asymmetry.

### Notes

- The gate is pure Python, so the asymmetry is platform-independent; both platforms above reproduce the same 6-vs-5 count on the MRE.
- #19991, #22737 and #24861 report this symptom class; I can't confirm their exact inputs were non-square without their pipelines, so I'm linking rather than claiming they're the same root cause.
- Happy to test any proposed fix against the sweep + MRE above.

I have read the CLA Document and I sign the CLA.

