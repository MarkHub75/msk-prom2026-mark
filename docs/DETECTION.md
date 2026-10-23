# CV Detection implementation

Public API is `preprocess(rgb_uint8_hwc, manifest) -> (tensor, LetterboxTransform)` and `decode(outputs, manifest, transform) -> list[dict]` from `ml.detection`. `NativeReferenceBackend(weights, manifest, device='cpu').infer(request)` is explicitly PyTorch, with no LinQ fallback.

## Model manifest

Required fields: `model_id`, `input` (`name`, static batch-one `shape`, `layout`, `dtype`, `scale`), `decoder`, ordered `classes`. Optional `output_name` is mandatory for multiple-output mappings. `output_layout` is BCN for YOLOv8 and BNC for classic YOLOv5. `thresholds` provides confidence, IoU, max_detections. Pose uses COCO-17 x/y/score. The input is RGB, centered letterbox with value 114, Pillow bilinear resize; exact rounded dimensions are retained for inverse coordinates. This is our explicit recipe; it does not claim pixel equality with OpenCV letterbox implementations.

`detect_v8` and `pose_v8` consume decoded xywh/probabilities. `detect_v5` multiplies objectness by class score. Sigmoid/DFL/anchor/stride decode must already be inside these graphs. Raw conv heads, embedded-NMS and end-to-end outputs are rejected rather than guessed. Host NMS is stable and class-aware. Float raw outputs are required; vendor raw integer packing requires the vendor-supported conversion before this decoder.

## Reproduce export and parity

Use an isolated preparation environment with the compatible installed torch/ultralytics; do not install export dependencies into the TPU compiler environment. Current preparation run used `/workspace/.venv-cv-prepare/bin/python`, Python 3.12.15, torch 2.14.1+cu126, ultralytics 8.4.184, onnx 1.23.2, onnxruntime 1.31.0. These versions are not claimed compatible with LinQ SDK.

```bash
python -m ml.detection.export --weights /path/to/trusted/pose.pt --output /path/to/artifacts/pose --model-id pose-v1 --decoder pose_v8
python -m ml.detection.export --weights /path/to/trusted/helmet.pt --output /path/to/artifacts/helmet --model-id helmet-v1 --decoder detect_v8 --class-map '{"Hardhat":"helmet","NO-Hardhat":"bare_head"}'
python -m ml.detection.verify --manifest /path/to/artifacts/pose/manifest.json --image /path/to/image.jpg --device cuda:0 --output /path/to/parity.json
python -m unittest discover -s tests -p test_detection.py -v
```

Only trusted `.pt` weights should be deserialized. Export writes owned copies of weights, ONNX and a manifest with SHA256, actual names/shapes, class map, versions and `linq_status=NOT_RUN`. Export and ONNX checker success do not establish TPU execution. Calibration data and TPU hashes must be added by the LinQ compiler stage.

## Actual preparation evidence, 2026-10-23

Artifacts are outside Git at `/workspace/artifacts/detection/`:

| Artifact | Source | SHA256 |
|---|---|---|
| helmet.pt | keremberke/yolov8n-hard-hat-detection HF revision `287bafa2feb311ee45d21f9e9b33315ff6ff955d`, best.pt | `05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c` |
| pose.pt | ultralytics/assets release v8.3.0, yolov8n-pose.pt | `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212` |
| bus.jpg | ultralytics/ultralytics tag v8.3.0, ultralytics/assets/bus.jpg | `c02019c4979c191eb739ddd944445ef408dad5679acab6fd520ef9d434bfbc63` |

Both models loaded, exported with static input `[1,3,640,640]`, opset13, and passed `onnx.checker`. Pose output is `[1,56,8400]`; helmet output is `[1,6,8400]` with classes `helmet,bare_head`.

Paired CPU PyTorch vs ONNX CPU inference on the same prepared bus image passed `atol=1e-3, rtol=1e-3`: pose max absolute error 0.000847, 3/3 post-NMS detections; helmet 0.000946, 1/1 detections. Initial CUDA defaults failed raw tolerance (max errors 0.302 and 0.508). Disabling TF32 for paired verification fixed this: pose CUDA max error 0.000710 and helmet CUDA result recorded in parity-cuda-fp32.json. The verify tool explicitly disables TF32; normal reference execution leaves application precision policy unchanged.

These are single-image numerical checks, not accuracy, latency SLA, steady throughput, industrial generalization or LinQ validation. The bus image is not a target helmet/fall evaluation set. Positive/negative target footage and TPU parity remain required. No compiled TPU program, calibration run or actual LinQ inference has been performed by this component.

Weight/dataset rights must be tracked separately from code provenance before redistribution or commercial use. Download links are reproducible provenance, not a blanket license grant.

## Corrective split pose graph for PTQ

The original combined pose graph is retained. A measured vendor quantizer issue assigned coordinate-range scale to keypoint confidence channels, collapsing them to zero in simulation. The corrective export exposes **upstream tensors before mixed concatenation**, rather than gathering from an already mixed graph output:

```bash
python -m ml.detection.split_pose --manifest /workspace/artifacts/detection/pose/manifest.json --output /workspace/artifacts/detection/pose-split
```

`split_pose_v8` requires a named output mapping defined by `split_outputs` in manifest:

| Semantic | Actual source tensor | Shape |
|---|---|---|
| boxes | `/model.22/Mul_2_output_0` | `[1,4,8400]` |
| class_scores | `/model.22/Sigmoid_output_0` | `[1,1,8400]` |
| keypoint_xy | `/model.22/Mul_4_output_0` | `[1,17,2,8400]` |
| keypoint_scores | `/model.22/Sigmoid_1_output_0` | `[1,17,1,8400]` |

The graph-surgery helper discovers these tensors through the final Concat -> keypoint Reshape -> keypoint Concat structure, validates the probability Sigmoid producers, and extracts a backward-reachable subgraph. Both mixed `/model.22/Concat_4_output_0` and terminal `output0` are absent from the new graph. All coordinate decoding and sigmoid operations remain inside ONNX. Host code only concatenates and reshapes the four already-decoded outputs before applying the existing NMS/geometry decoder.

Actual artifact `/workspace/artifacts/detection/pose-split/weights.onnx` SHA256 is `802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00`. ONNX checker passed. Original vs split float ONNX on the same bus image was bit-identical (maxabs 0, three identical post-NMS detections); keypoint probabilities ranged from 0.00341755 to 0.99890792 across all anchors. Evidence is `pose-split/graph-parity.json`. This establishes graph-surgery correctness for that input; vendor quantization, compiler, simulation and device execution must be checked independently by LinQ Integration.

## Compare exported numeric runtime captures (CV-02)

`ml.detection.compare_capture` compares already-captured named tensor arrays. It does not execute a model and cannot establish that the source was real hardware. Capture format agreed with LinQ Integration is `capture.json`, `inputs.npz`, `outputs.npz`. NPZ keys are exact tensor names; arrays are real numeric data only. Loading always uses `allow_pickle=False`; object/string/complex arrays are rejected. Never export notebook locals, session objects or unfiltered outputs.

```bash
python -m ml.detection.compare_capture \
  --reference /path/to/golden-outputs.npz \
  --actual /path/to/capture/outputs.npz \
  --manifest /path/to/model/manifest.json \
  --metadata /path/to/capture/capture.json \
  --output /path/to/comparison.json
```

If runtime tensor names differ, supply an explicit JSON map through `--name-map` or `capture.json`'s `runtime_to_reference`. Direction is **actual runtime name -> reference name**. Without a map only exact identity names are accepted. Unmapped or extra tensors, duplicate map destinations, nonfinite values, different shapes or different dtypes invalidate the capture comparison. Raw integer TPU codes must first be converted through the verified runtime ABI; this tool neither guesses scales nor silently casts mismatching dtypes.

API: `compare_captures(reference, actual, runtime_to_reference=None, manifest=None, metadata=None, relative_epsilon=1e-8, min_match_iou=.1)`. `load_numeric_npz(path)` supplies detached numeric dictionaries. Per-output statistics include shape/dtype, max/mean/p95 absolute differences, and relative differences `abs(actual-reference)/max(abs(reference),epsilon)`. Relative errors around zero can be large, so inspect them with absolute errors. No tolerance produces a quality PASS. Overall `COMPARED` means valid numeric tensors were compared, even if their values differ substantially; `INVALID_CAPTURE` means structural/numeric checks failed. CLI exit 0 means `COMPARED`, exit 2 means invalid capture. No hardware or quality acceptance is implied.

Decoded comparison requires manifest plus `metadata.original_transform` containing exactly integer fields `original_width`, `original_height`, `input_width`, `input_height`, `resized_width`, `resized_height`, `left`, `top`. If missing, decoded stage is explicitly `SKIPPED`. Invalid metadata/output is `INVALID_METADATA_OR_OUTPUT` while preserving valid raw numeric diagnostics. Split pose outputs are restored through the same `split_pose_v8` decoder. Diagnostic detection pairing is greedy same-class descending IoU above `min_match_iou`; this is not ground-truth matching. Reports include unmatched detections, box differences, scores, keypoint confidences, and XY error on jointly visible points at confidence >=.5. These thresholds define diagnostics only, not target acceptance.

Actual smoke evidence saved outside Git:

- `pose-split/capture-golden-smoke.json`: golden NPZ compared to itself, 4 output tensors exactly equal and 3 identical decoded detections. This checks file/decoder plumbing only.
- `pose-split/capture-simulation-comparison.json`: pre-existing vendor **simulation** outputs compared with their saved float references, 3/3 decoded persons, paired box IoUs .911/.872/.781. Largest all-anchor differences are 170.51 px for box channels, 206.02 px for keypoint XY, .1188 class score and .7634 keypoint confidence. Unselected anchors are included in these maxima; they cannot be replaced by favorable selected examples. This is a diagnostic comparison of simulation, not a hardware capture or a target-video quality result.

Every report states `hardware_execution=NOT_ESTABLISHED_BY_COMPARISON` and `target_quality=NOT_EVALUATED`. Actual Jupyter runtime captures and independently labeled video are still needed.
