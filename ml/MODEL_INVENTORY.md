# Model inventory — night2026-10-24

Audit UTC: 2026-10-24T00:29:25.901450+00:00. OBSERVED means inspected checkpoint/graph/file metadata; MEASURED means saved results; SIMULATED is the vendor CPU graph; UNKNOWN is not filled from filenames. Two unique trained checkpoints are present. Split-Pose is an output-ABI variant of the same pose weights. No new neural forward was run for this inventory.

## Common detector/pose implementation

OBSERVED exporter: Ultralytics8.4.184, Torch2.14.1+cu126, ONNX1.23.2; source ONNX IR7/opset13. Existing export call: format=onnx,imgsz=640,batch=1,opset=13,dynamic=False,simplify=False,half=False,nms=False,device=cpu. Exporter versions differ from versions embedded in the original checkpoints.

Input images: float32[1,3,640,640], RGB uint8 source -> Pillow bilinear letterbox with pad114 -> /255 -> contiguousNCHW. Decoder restores original-image xyxy/keypoints once, uses class-aware host NMS once, confidence.25/IoU.45/max300. No repeated sigmoid/DFL/coordinate decode. Behavior baseline separately requires person score.5/keypoint score.5.

OBSERVED current isolated SDK: tpu_framework_bin2026.9.45, tpu_compiler_bin2026.9.493, dnn_quant_bin2026.9.98, SDK Torch2.9.1+cpu, NumPy1.26.4, ONNX1.16.2, ORT1.29.0. Remote TPU firmware/runtime versions: UNKNOWN. Official source codec0.0.1 is user-confirmed/hash-pinned, not guessed from a similarly named package.

PTQ: preliminary_model_conditioning -> RegularModel.calibrate_torch -> quantize(thresholds), constructor percentile100/default max-abs, no samplewise/activation percentile override. Compiler O1/TPU_H1M. Baseline calibration is exactly one preprocessed bus image, SHA028d5e8325942e8a438a41396583aff1a4b14d1ac445f1e4450ace65a4d83faf; this is smoke calibration, not representative training or independent quality data.

## helmet-v1

OBSERVED architecture: Ultralytics YOLOv8 nano DetectionModel, two classes; 3,011,238 unfused parameters. YAML and loaded module topology establish this identification; it is not inferred from the directory.
Checkpoint metadata version 8.0.23, date 2023-01-30T01:39:31.068862. Stored epoch=-1/stripped checkpoint does not establish training duration. Full training membership, original seed, optimizer history and EMA provenance: UNKNOWN.
Source/download pin: https://huggingface.co/keremberke/yolov8n-hard-hat-detection/tree/287bafa2feb311ee45d21f9e9b33315ff6ff955d. Pose assets release tagv8.3.0 is a download-container tag, not the checkpoint training version.

| Artifact | Exact local file | SHA256 |
|---|---|---|
| weights.pt | /workspace/artifacts/detection/helmet/weights.pt | 05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c |
| weights.onnx | /workspace/artifacts/detection/helmet/weights.onnx | b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47 |
| manifest.json | /workspace/artifacts/detection/helmet/manifest.json | 71d6a489f1e2c1b10214371482f5bb4d928d9d2c9585d2d7782b10514d18e7cc |
| TPU | /workspace/artifacts/linq-sdk/helmet-compile/model.tpu | 408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa |

Canonical classes: ['helmet', 'bare_head']; source names: ['Hardhat', 'NO-Hardhat'].
Semantic limit: helmet is a detected object/head-cover proxy; bare_head is a detected source NO-Hardhat head region. Neither is automatically a correctly owned person violation. Hidden head, held helmet or conflicting ownership remain unknown. This model has no person class.

| Output name | Shape | dtype |
|---|---|---|
| output0 | [1, 6, 8400] | float32 |

Compile evidence: /workspace/artifacts/linq-sdk/helmet-compile/compile-report.json; PASS is compilation only. Historical report runtime_abi_verified=false is immutable; later actual capture-derived verified manifests provide runtime evidence separately.
MEASURED actual LinQ: request262bdaa1-c24b-48ac-b073-6b28fd014248/status0/matchingID,10234.49ms,2bare_head(.352586,.259503); float reference1matched(IoU.925226) plus1extra TPU detection. This is one smoke example, not systematic precision evidence.
MEASURED development52/44complete-class: helmetTP19FP11FN6/P.6333/R.76/F1.6909; bareTP23FP7FN9/P.7667/R.71875/F1.7419. Confirmed upstream-photo overlap; no independent test/ownership GT. Earlier confidence and tiling candidates rejected; baseline retained.

## pose-v1

OBSERVED architecture: Ultralytics YOLOv8 nano PoseModel, one class and17x3 keypoints; 3,295,470 unfused parameters. YAML and loaded module topology establish this identification; it is not inferred from the directory.
Checkpoint metadata version 8.0.77, date 2023-04-17T08:01:11.737149. Stored epoch=-1/stripped checkpoint does not establish training duration. Full training membership, original seed, optimizer history and EMA provenance: UNKNOWN.
Source/download pin: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt. Pose assets release tagv8.3.0 is a download-container tag, not the checkpoint training version.

| Artifact | Exact local file | SHA256 |
|---|---|---|
| weights.pt | /workspace/artifacts/detection/pose/weights.pt | c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212 |
| weights.onnx | /workspace/artifacts/detection/pose/weights.onnx | 398cc23eac1b4702656d2ec4486d7aa1e5bda8563d33babaa9017ab3fdd5b02f |
| manifest.json | /workspace/artifacts/detection/pose/manifest.json | da955b16b8bf3bfc147cb1d1282a02714d7fac45a74a4416e1b0ef4744c63daa |
| TPU | /workspace/artifacts/linq-sdk/pose-compile/model.tpu | 23c0e53439032860706c28d1e9f493f1e84bda85b679997b7336412db62c4e1c |

Canonical classes: ['person']; source names: ['person'].
Semantic limit: person boxes and COCO-17(x,y,confidence) are observations, not fall/run/medical labels. Missing pose evidence is unknown.

| Output name | Shape | dtype |
|---|---|---|
| output0 | [1, 56, 8400] | float32 |

Compile evidence: /workspace/artifacts/linq-sdk/pose-compile/compile-report.json; PASS is compilation only. Historical report runtime_abi_verified=false is immutable; later actual capture-derived verified manifests provide runtime evidence separately.
SIMULATED limitation: mixed combined output lost keypoint-confidence numerical resolution after PTQ; REJECTED. Actual LinQ execution for this mixed graph: NOT_RUN. It is not the preferred fall model.

## pose-split-v1

OBSERVED architecture: Ultralytics YOLOv8 nano PoseModel, one class and17x3 keypoints; 3,295,470 unfused parameters. YAML and loaded module topology establish this identification; it is not inferred from the directory.
Checkpoint metadata version 8.0.77, date 2023-04-17T08:01:11.737149. Stored epoch=-1/stripped checkpoint does not establish training duration. Full training membership, original seed, optimizer history and EMA provenance: UNKNOWN.
Source/download pin: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt. Pose assets release tagv8.3.0 is a download-container tag, not the checkpoint training version.

| Artifact | Exact local file | SHA256 |
|---|---|---|
| weights.pt | /workspace/artifacts/detection/pose-split/weights.pt | c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212 |
| weights.onnx | /workspace/artifacts/detection/pose-split/weights.onnx | 802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00 |
| manifest.json | /workspace/artifacts/detection/pose-split/manifest.json | eac2ba5e8f46c5ecfad8ec3d09b2fd96d8d53ebc564c04685b4e505f2a339a35 |
| TPU | /workspace/artifacts/linq-sdk/pose-split-compile/model.tpu | c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b |

Canonical classes: ['person']; source names: ['person'].
Semantic limit: person boxes and COCO-17(x,y,confidence) are observations, not fall/run/medical labels. Missing pose evidence is unknown.

| Output name | Shape | dtype |
|---|---|---|
| /model.22/Mul_2_output_0 | [1, 4, 8400] | float32 |
| /model.22/Sigmoid_output_0 | [1, 1, 8400] | float32 |
| /model.22/Mul_4_output_0 | [1, 17, 2, 8400] | float32 |
| /model.22/Sigmoid_1_output_0 | [1, 17, 1, 8400] | float32 |

OBSERVED split graph exposes boxes, person probabilities, keypoint XY and keypoint probabilities before concatenation. Host operations are reshape/concatenate only. Same trained weight SHA as pose-v1; no new trained architecture.

Compile evidence: /workspace/artifacts/linq-sdk/pose-split-compile/compile-report.json; PASS is compilation only. Historical report runtime_abi_verified=false is immutable; later actual capture-derived verified manifests provide runtime evidence separately.
MEASURED actual LinQ: request1f986b07-896d-48b9-8b4f-6ce2d0f8dc16/status0/matchingID,11152.85ms,3people,visible-keypoints16/17/9. Further UR01 real11calls/status0/bitwise input parity and decoded score/box/KPconfidence parity are saved under /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps.
MEASURED source-reference event limits: full3274-frame UR20 baseline misses10/10falls; at225fixed2FPS frames TP1FP0FN9/F1.1818. No eligible>=3sgroundlying positive in this set. Current Split-Pose confidence is not globally collapsed; source/conditioned+PTQ person-score drift was measured on industrial inputs. Accuracy is not accepted despite working TPU execution.

## pose-ptq-mendeley8-v1 — rejected calibration variant

OBSERVED: same YOLOv8n pose weights and source ONNX802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00; conditioned graph byte-identical to Split-Pose baseline. No distinct trained checkpoint. Same four-output ABI and preprocessing/postprocessing.
TPU: /workspace/artifacts/quality/candidates/pose-ptq-mendeley8-v1/compile/model.tpu; SHA256 0aed469bd7771348ca39c3a3d429166a74e26cb97154ca655a6491800cb67918. O1/TPU_H1M compiled in75.545s. Calibration exactly8Mendeley midpoint tensors/1conservative source group, corpusSHA161c8692d1b15249762c6fcb28867c6eaf1c98f190729544d6e917015829544b. No validation/test calibration.
SIMULATED paired225-frame event quality: both old/new TP1FP0FN9/F1.1818. REJECTED_NO_EVENT_QUALITY_GAIN. Actual LinQ: NOT_RUN; not deployed and not selected.

## Organizer stock program, claimed ResNet50

Architecture exactness: UNKNOWN at checkpoint/topology level; ResNet50 is the official example/program claim only. No separately supplied trained checkpoint or source ONNX. Source training version/exporter/IR/opset/calibration/quantization: UNKNOWN. Do not infer compiler preset/target solely from filename.
TPU /workspace/artifacts/linq-api/torch_resnet50_b1_o5_h1m.tpu; SHA2560bac3ad590505fb20753e4888bec3fce9202a6e1c96cad3abe74a2a4b283d60c. Official example /workspace/artifacts/linq-api/example_torch_resnet50.py is hash-pinned in static audit.
Input input.1 float32[1,3,224,224]; output495 float32[1,1000]. Classes are1000ImageNet logits/scores per example; exact class-index vocabulary/version UNKNOWN. Supplied example uses ImageNet mean/std normalization; preserve its exact code, not detector/255 preprocessing.
Actual automatic completion status0 and saved numerical/class checks exist under /workspace/artifacts/linq-rpc/resnet50-001. This is a stock service/format smoke test, not an industrial model. Do not rerun it as a network check.

## Shared infrastructure and preservation boundary

Historical execution paths/names are evidence only. NEW remote files must be under matvey/ with matvey_ names; protected captain/baseline programs and foreign queues are never touched. One own TPU request maximum, Jupyter CPU threads1–2. Own isolated staging and any new candidate LinQ qualification remain separately gated; no old root-cache submission is authorized by this inventory.

Raw static audit subreports (no neural forward): /workspace/artifacts/night-20261024/inventory/{detection-audit,linq-audit}.json. SHA256 fields above refer to file bytes. Helmet dataset semantic digest39e13... differs from serialized JSON fileSHA346f74...; these identities must not be interchanged. Existing successful unit tests are software evidence, not model accuracy.
