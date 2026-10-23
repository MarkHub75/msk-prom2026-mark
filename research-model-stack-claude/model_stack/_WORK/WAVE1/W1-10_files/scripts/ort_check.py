"""Run ONNX Runtime CPU on bus.jpg for each exported variant; compare with PyTorch reference.
Usage: ort_check.py ONNX_ROOT WEIGHTS_DIR OUT_JSON"""
import sys, json, glob, os
from pathlib import Path
import numpy as np, torch, onnxruntime as ort, cv2
from ultralytics import YOLO, ASSETS
from ultralytics.data.augment import LetterBox

root, wdir, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
img = cv2.imread(str(ASSETS / "bus.jpg"))
res = {"image": str(ASSETS / "bus.jpg"), "image_shape": list(img.shape), "ort": ort.__version__, "torch": torch.__version__}

def prep(h, w):
    lb = LetterBox(new_shape=(h, w), auto=False, stride=32)(image=img)
    x = lb[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0
    return np.ascontiguousarray(x)

ref_cache = {}
def torch_ref(wt, x):
    m = YOLO(str(wdir / wt)).model.float().eval()
    with torch.no_grad():
        y = m(torch.from_numpy(x))
    y = y[0] if isinstance(y, (tuple, list)) else y
    return y.numpy()

def iou(a, b):
    x1 = np.maximum(a[:, None, 0], b[None, :, 0]); y1 = np.maximum(a[:, None, 1], b[None, :, 1])
    x2 = np.minimum(a[:, None, 2], b[None, :, 2]); y2 = np.minimum(a[:, None, 3], b[None, :, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    ar = lambda r: (r[:, 2] - r[:, 0]) * (r[:, 3] - r[:, 1])
    return inter / (ar(a)[:, None] + ar(b)[None] - inter + 1e-9)

for f in sorted(root.glob("*/*.onnx")):
    name = f.parent.name
    r = {}
    try:
        s = ort.InferenceSession(str(f), providers=["CPUExecutionProvider"])
        inp = s.get_inputs()[0]
        shp = inp.shape
        h = shp[2] if isinstance(shp[2], int) else 640
        w = shp[3] if isinstance(shp[3], int) else 640
        b = shp[0] if isinstance(shp[0], int) else 1
        x = prep(h, w)
        xb = np.repeat(x, b, axis=0)
        y = s.run(None, {inp.name: xb})[0]
        r.update(input=[b, 3, h, w], output_shape=list(y.shape), output_dtype=str(y.dtype))
        if b > 1:
            r["batch_rows_identical_maxdiff"] = float(np.abs(y[1:] - y[:1]).max())
        wt = f.stem + ".pt"
        if y.shape[1] == 84:  # raw decoded output
            ref = torch_ref(wt, x)
            r["torch_ref_shape"] = list(ref.shape)
            if ref.shape == y[:1].shape:
                d = np.abs(ref - y[:1])
                r["maxabs_diff_vs_torch_boxes"] = float(d[:, :4].max())
                r["maxabs_diff_vs_torch_scores"] = float(d[:, 4:].max())
            r["box_range"] = [float(y[0, :4].min()), float(y[0, :4].max())]
            r["score_range"] = [float(y[0, 4:].min()), float(y[0, 4:].max())]
            r["n_anchor_maxscore_gt_0.25"] = int((y[0, 4:].max(0) > 0.25).sum())
        else:  # [B,300,6]
            det = y[0]
            keep = det[det[:, 4] > 0.25]
            r["n_det_conf_gt_0.25"] = int(len(keep))
            r["dets_conf_gt_0.25"] = [[round(float(v), 2) for v in row] for row in keep[:10]]
        # dynamic: second shape
        if not isinstance(shp[2], int):
            x2 = prep(480, 640)
            y2 = s.run(None, {inp.name: np.repeat(x2, 2, axis=0)})[0]
            r["dynamic_test_input"] = [2, 3, 480, 640]; r["dynamic_test_output"] = list(y2.shape)
    except Exception as e:
        r["error"] = repr(e)[:600]
    # Ultralytics predict on ONNX vs .pt (end-to-end incl. pre/post)
    try:
        imgsz = r.get("input", [1, 3, 640, 640])[2:]
        po = YOLO(str(f), task="detect").predict(str(ASSETS / "bus.jpg"), imgsz=imgsz, verbose=False, device="cpu")[0]
        pp = YOLO(str(wdir / (f.stem + ".pt"))).predict(str(ASSETS / "bus.jpg"), imgsz=imgsz, verbose=False, device="cpu")[0]
        bo, bp = po.boxes.xyxy.numpy(), pp.boxes.xyxy.numpy()
        r["predict_onnx_n"], r["predict_pt_n"] = len(bo), len(bp)
        r["predict_onnx_cls"] = sorted(po.boxes.cls.int().tolist()); r["predict_pt_cls"] = sorted(pp.boxes.cls.int().tolist())
        if len(bo) and len(bp):
            r["predict_min_best_iou"] = float(iou(bo, bp).max(1).min())
    except Exception as e:
        r["predict_error"] = repr(e)[:600]
    res[name] = r
    print(name, json.dumps(r)[:400], flush=True)
json.dump(res, open(out, "w"), indent=1)
