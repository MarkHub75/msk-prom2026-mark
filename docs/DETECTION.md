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
