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

## Verified runtime manifest from existing real captures

`from ml.detection import prepare_verified_manifest` exposes:

```python
manifest = prepare_verified_manifest("helmet", artifacts_root="/workspace/artifacts")
pose_manifest = prepare_verified_manifest("pose-split")
```

This helper reads the existing `linq-rpc/{name}-001` completed capture, its response, `linq-rpc/{name}/staging-receipt.json`, the original detection manifest and `linq-sdk/{name}-compile/compile-report.json` plus local program. It performs no network call, changes no original/candidate manifest and creates no files. `capture_review.review_capture` checks NPZ/file/tensor hashes, finite numeric values and exact shape/dtype. Additional checks require completed service status 0 (integer, not bool), the same canonical request/response/journal UUID, local/compiled/staged/captured program SHA256 equality, staged byte count/name, source ONNX hash equality, exact compiler/capture/response ABI, matching source input ABI and valid source decoder outputs. Both existing real helmet and split-pose captures were decoded locally by this helper.

The returned new dictionary retains an allowlisted preprocessing/decoder contract and adds `linq.runtime_abi_verified=True`, local `program_path`, exact `program_name`, `program_sha256`, `inputs`, `outputs`, identity `input_map`/`output_map` and local `evidence_paths`. Public source URLs and arbitrary capture/account/broker metadata are omitted. The orchestrator injects RPC directories, timeout and runner factory. ABI verification is based on the recorded completed remote calls and consistent bytes; it is not independent hardware attestation or target-video quality acceptance, and does not establish continuous-video capacity.

### Actual source video recommendation (read-only review)

Use `Deep-Research/datasets/_WORK/MATERIALS/W2-10/4_tr6.mp4`, **0–8 seconds**, as a real industrial-camera replay candidate. It is Önal/Dandıl Mendeley `xjmtb22pff/1`, folder `4_safe_walkway`, author member UUID `730fbd88-bb7e-4444-a826-e5f2f461a2b4`. Local SHA256 was rechecked and matches saved metadata: `f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a`. Video is H.264 1920×1080, 522 frames, 25.05 FPS (501/20), duration 20.838323 s, native timebase 1/16032. ffprobe presentation timestamps at source frames 0/50/100/150/200 are 0/1.996008/3.992016/5.988024/7.984032 s respectively, matching OpenCV positions in this sample.

Five decoded frames show a foreground seated worker with visibly uncovered head, plus walking/standing people. This is a plausible bare-head replay input, not a labeled helmet-violation holdout: the folder describes walkway use, site helmet policy is unknown, some heads are small or turned away, and no fall was observed in the inspected window. Use this as real-footage plumbing and operator-evidence demonstration; manually annotate before reporting accuracy. `0_tr16.mp4` is a second real candidate (24.8 FPS, foreground walking person in first 0–4 s), but has different initial timestamp/framing. `W2-11/CORE_SAMPLE.mp4` is a close-up concrete-mixing action, unsuitable for whole-person/helmet demonstration.

Inspection artifacts are outside Git: `/workspace/artifacts/video-review/candidates.jpg`, `inspection.json`, `native-pts.json`. The research archive and source videos were not modified or committed. `reference.avi` is repeated bus imagery and must never be described as real industrial source footage.

## ML-quality sprint: Helmet E00 and object scoring

The quality sprint follows `/workspace/ML_24H_PLAYBOOK.md`. External event/API schemas remain unchanged. New owned tools are in `ml/quality/helmet/`:

- `metrics.evaluate_dataset(dataset, predictions, classes=('helmet','bare_head'), confidence=.25, match_iou=.5, ap_score_floor=.001, max_detections=300, allow_test=False)` computes object P/R/F1, AP50 and mean AP over IoU .50:.05:.95 with a 101-point recall grid. This is an explicitly versioned custom metric, not a claim of exact COCO equivalence.
- Dataset images require `image_id`, `group_id`, `split`, `annotations` (class_name/positive-area original xyxy box/optional ignore), explicit `class_coverage` and optional `ignore_regions`. Predictions must explicitly include every image, including empty lists. Missing inference is an error, not an observed empty frame.
- Only class-complete images contribute to primary precision/recall/AP. Partial-label images get known-positive recall separately; their unannotated objects are never assumed absent. Unknown-class images are excluded. Regular GT matches take precedence over ignore regions; unmatched predictions with >=.5 intersection-over-prediction-area in an applicable ignore region are excluded. A class with zero complete GT has AP null, not zero. Final test requires explicit `allow_test=True`; it has not been invoked.
- `curate` inventories all images/labels, exact byte/decoded-RGB hashes and connected pHash/dHash duplicate proxies, then deterministically freezes a bounded official-val selection before predictions. It preserves original supplied splits and quarantines orphan labels. Perceptual proxies do **not** establish camera/actor/source independence.
- `baseline` accepts validation only, verifies frozen image bytes, acquires the shared `fcntl` GPU lock, stores raw outputs once at score floor .001 and evaluates operating confidence .25. It never trains or uses LinQ and never evaluates a test split.

Existing Construction-PPE ZIP was extracted outside Git to `/workspace/datasets/quality/helmet-construction-v1`. SHA256 `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`. Inventory: 1,416 paired images, 1,268 exact/perceptual proxy components, 30 components crossing original splits, 10 orphan labels quarantined. Frozen first development selection used 32 official-val images, one per proxy group, excluding components touching official test. It is development data only: known same-rooftop actor photos evade tight perceptual grouping, and pretraining-source overlap is unresolved. Do not train/fine-tune on this source under the current sprint decision.

A blind single-agent GT review was saved before predictions, identifying 18 complete/9 partial/5 unknown images and merging nine known rooftop-actor photos. Defects include `image1392.jpg` no_helmet box on the neck, unlabeled visible heads/helmets in `image705.jpg`/`image656.jpg`/`image547.jpg`, and uncertain tiny/occluded heads. A second independent review is still required before treating reviewed metrics as settled. Fixed reviewed dataset digest: `5586d7ab62252dd53829d7571d41da0c705f93ddd2b4924803b8e7ca99162a6f`.

Actual E00 GPU native run is `/workspace/artifacts/quality/helmet/e00-v1/`: frozen-input.json, raw NPZs, predictions.json, metrics-reviewed.json, metrics-source-provisional.json, run.json. At confidence .25/IoU .5 on the 18 single-reviewed complete images: helmet GT20/TP16/FP3/FN4, P .8421/R .8000/F1 .8205/AP50 .8057/mAP50-95 .2710; bare_head GT3/TP1/FP4/FN2, P .2000/R .3333/F1 .2500/AP50 .3366/mAP50-95 .1683. Bare-head support is far too small for stable threshold selection. The all-32 source-label benchmark is separate and provisional because of known annotation defects. Neither report is an independent industrial-video accuracy result. Test inference, training and LinQ execution were not performed by E00.

Primary provenance checked during the sprint: [current baseline model card](https://huggingface.co/keremberke/yolov8n-hard-hat-detection/blob/main/README.md) names the paired dataset; [its dataset card](https://huggingface.co/datasets/keremberke/hard-hat-detection/blob/main/README.md) links Roboflow `hard-hats-fhbh5/2`, reports CC BY 4.0 and 640×640 stretch. Therefore that source is not an independent baseline test. [Construction-PPE official config](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/construction-ppe.yaml) confirms counts/class map and AGPL notice; independent upstream-photo rights remain unresolved. [SHEL5K primary page](https://data.mendeley.com/datasets/9rcv8mm682/1) identifies its SHD5000 parent and CC BY-NC 3.0, so SHD/SHEL cannot be treated as unrelated sources. [SFCHD author repository](https://github.com/lijfrank/SFCHD-SCALE) supplies chemical-plant images with blur_head labels but no explicit blanket dataset license in the inspected repository page. Existing seven SFCHD images are potential source-separated holdout material only after rights, mapping and source/camera grouping decisions; no model has been run on them in this sprint.
