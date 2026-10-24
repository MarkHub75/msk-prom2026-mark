## Video-first final integration — 2026-10-24 19:31 UTC

Current package: `/workspace/artifacts/matvey-final-20261025/video-first-v2/`.
See `docs/handoffs/VIDEO_FIRST_FINAL_20261025.md` and
`ml/reports/video-first-final-20261025.json`. Main f6b5358a and its ML contract
remain unchanged. New real pretrained smoke0/fire1 model is integrated locally;
no training or new TPU execution. Seven new full scenes:2648frames/5296calls
(3966GPU,1330CPU). Selected package includes three prior scenes:10/3297/7243.
New actual Argus CPU smoke job:408calls,204/407frames/model, event1/evidence1,
API200,48.434s. No app/rule/backend changes. Source DFire30 detector F1 smoke.8333,
fire.8966; overlap/exhaustiveness UNKNOWN, not independent industrial/event GT.
Fire headlight false alert retained. Current S07 Fall03 missed/bedADL10 alert;
not accepted as a successful fall demo.528testsPASS(4skipped). Latest Data
research forklift/person and cigarette ABI candidates are recorded, not promoted.
All assigned agents completed; no own compute jobs. No new automatic experiment.

## Final integration inventory — unchanged checkpoints

Registry handoff docs/handoffs/MODEL_REGISTRY_HANDOFF_20261025.md. Primary COCO80
coco-reference-yolov8n@640-v1-a6a8c37f7e45 local-only; Pose matvey-pose-yolov8n@
640-v1-acc5f51228b9; Helmet matvey-helmet-yolov8n@640-v1-5c3af1f3b855. Full ONNX,
tails, historical TPU binaries/hash manifest outsideGit in finalmodels/. No new
weights/training/compile/remoteplacement/promotion. Actual Argus CPU114callsPASS;
existing TPU tails15savednumeric callsPASS, no live requests. New specialist fire/
smoke/cigarette/no_harness/suspended_load/cargo absent; export-only scalar training
heads remain unselected. Current strict remote namespace conflicts with old app
uploader; local-only additions setlinq_program:null, never invoke unsafe uploader.

# Model inventory — night2026-10-24

## Current coverage release

Eight rules share the original person/Pose and Helmet runtimes; no eight duplicate
CV engines were created. Original baseline weights/ONNX/TPU remain unchanged.
There are still two original selected trained baselines; a later Training Agent
handoff additionally supplies four UNSELECTED fold-specific temporal heads, listed
below. The old "two unique trained checkpoints" statement is a night inventory,
not a denial of these new candidate files. Missing specialist models and exact
requested ABI/annotation semantics are in ml/scenarios/TRAINING_REQUIREMENTS.json
and TRAINING_ADDENDUM.json. Full scenario LinQ validation is not established.


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
Input input.1 float32[1,3,224,224]; output495 float32[1,1000]. Classes are1000ImageNet logits/scores per example; exact class-index vocabulary/version UNKNOWN. Supplied example center-crops a square85%of the short dimension, PIL-resizes224, then(RGB/255-mean[.485,.456,.406])/std[.229,.224,.225], classoffset1; preserve its exact default resize kernel, not detector/255 preprocessing.
Actual automatic completion status0 and saved numerical/class checks exist under /workspace/artifacts/linq-rpc/resnet50-001. This is a stock service/format smoke test, not an industrial model. Do not rerun it as a network check.

## Shared infrastructure and preservation boundary

Historical execution paths/names are evidence only. NEW remote files must be under matvey/ with matvey_ names; protected captain/baseline programs and foreign queues are never touched. One own TPU request maximum, Jupyter CPU threads1–2. Own isolated staging and any new candidate LinQ qualification remain separately gated; no old root-cache submission is authorized by this inventory.

Raw static audit subreports (no neural forward): /workspace/artifacts/night-20261024/inventory/{detection-audit,linq-audit}.json. SHA256 fields above refer to file bytes. Helmet dataset semantic digest39e13... differs from serialized JSON fileSHA346f74...; these identities must not be interchanged. Existing successful unit tests are software evidence, not model accuracy.

## New night candidates — rejected, never deployed

Both use the SAME YOLOv8n Helmet checkpoint05ed3a...; no new trained weights/version. Same exporter/IR/opset13/static640 preprocessing/decoder/conf.25/NMS.45 and8Mendeleycalibration tensorsSHA161c8692d1b15249762c6fcb28867c6eaf1c98f190729544d6e917015829544b; O1/TPU_H1M. Actual LinQ for both: NOT_RUN because validation failed. Preserve baseline for rollback.

| Variant | Source ONNX / outputs | TPU SHA256 / artifact | SIMULATED decision |
|---|---|---|---|
| E001 matvey_helmet_ptq_mendeley8_v1 | Existing b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47, output0[1,6,8400]f32 | ecd5a8853745bc9055b7a2c8eb4ddee43177761b9b6e4a04048a32751b5fae5e; /workspace/artifacts/night-20261024/E001/matvey_helmet_ptq_mendeley8_v1/compile/model.tpu | macroF1 .741682→.735185; bareR .59375unchanged; REJECT |
| E005 matvey_helmet_split_v1 | e802cef32d4fc3398128b770ddc29d0ded6888a2e6a58a921e20202d306ee33a; /model.22/Mul_2_output_0[1,4,8400] and /model.22/Sigmoid_output_0[1,2,8400]f32; split_detect_v8 | 27c1801181a6637c1744a13e45a2713f3afbc36fce517ec6705696a51b8289f6; /workspace/artifacts/night-20261024/E005/matvey_helmet_split_v1/compile/model.tpu | float52bitwiseequal, PTQ macroF1 .327778/bareR .03125; REJECT |

E001 compile61.81s; E005 compile59.62s (CPU2, not device inference time). Split output changes quantization-boundary behavior despite float parity; scale/anchor audits saved, mechanism UNKNOWN. The baseline combined output already has per-channel scales. Baseline PTQ52diagnostic object metrics differ from saved native: helmetTP23FP11FN2, bareTP19FP3FN13; macro .741682. These are vendor SIMULATED values, not52newhardware calls. Fall/Running candidates change input/rules only and remain OFF/unpromoted; same pose architecture/checkpoint/ONNX/TPU. See report for all rejected decisions.

## Saved-output follow-up E006/E007 — no model/ABI changes

E006 GT-level attribution: native/float primaryTP/FP assignments are identical, but raw native/float arrays are NOTbitwiseequal. Historical NPZ binding uses preserved common52image/prediction insertion order; no embedded nativeNPZimageIDs, so disclose that limitation. OriginalPTQ retains19helmetTP and recovers4; bare retains19 and loses4, each loss with saved sameclassIoU>=.5 overlap but below primaryscore.25. Native FP18 vsPTQ14 splits9corresponding/9withoutcounterpart/5new. These are saved developmental outputs, not new hardware or causalconditioning isolation. Originalthresholds/weights/TPU unchanged.

E007 source running46frames:30no decodedperson,16IoUbelow.5,zero lost at existing consumer.5gate. All345sourceIDs/geometry/hash records verified;768nativeXMLboxes match,188decodedboxes/keypoints inoriginal384x288 bounds. ElevenoutofboundsGTboxes arewalkingonly, preserved. No storedpreNMS for CAVIAR, so threshold/NMS/rawnonresponse causes remainUNKNOWN; no inverseletterboxnumericalreplay claim. No newNNcalls, training, compile, remoteoperation or modelpromotion. See ml/reports/night-followup-20261024.json and EVAL_REPORT.

## Training Agent temporal candidates — metadata/hash intake only

Source: /workspace/artifacts/training/matvey_training_20261024/matvey_training_handoff.json;
EXPERIMENTAL_EXPORT_VERIFIED, new_training=false for that handoff operation,
improved=false, production_model_selected=false. Export report SHA256 3e813883813b363169dc17aaefd12c739e89c5268ec7e8895cf7a51514d0fb8a.
Reported TCN/MLP kinds and graph operators are supplied by the Training export
report; root verified file bytes/descriptors, did not deserialize checkpoints or
retrain. Original external author/repository and full independent episode GT are
UNKNOWN. GMD weak source-clip/group CV is not industrial event accuracy. Input
pose_window float32[1,24,74] -> fall_logit float32[1,1], static opset13/IR7; exact
74-feature ordering/mask/sampling plan is required before integration. Four fold
heads are not automatically a single deployable checkpoint; no best outer-test
fold selection. CPU cached-feature float export parity only; compilation/PTQ/ABI/
actual LinQ and independent video quality NOT_RUN/BLOCKED. No head is selected.

| Candidate | Reported kind | Checkpoint SHA256 | ONNX SHA256 |
|---|---|---|---|
|gmd-outer-1|tcn|132351e26f19c6cb29a5bd5a990419d7060ba552eb2f552db6c71653658a7af2|8f966bd8dbf22148567325a37fa2bc7735748f8fd268f54269d95acec771641f|
|gmd-outer-2|mlp|24b266bdd948b548c85f48641a342829f1238793fb3ef4eff8774013d1659de3|bdf106cd1050455856bfe99b8ca621f545645ef966e7f780a0a6f0594105de60|
|gmd-outer-3|tcn|68cffe43c63583b8231294664395e293923632e7373e103c5d9055641107305d|500c7411a6731aedaf778ae29afd84a1e566d9ecc7c89ad318bd8c87131d8666|
|gmd-outer-4|mlp|959a963724997f4838a4b66caa8b85d2be41097df334d99014bf38eb8d340ace|4a2aa6a8279cf224cdb8f9ce03c362c9bbd405f20634c521b4c9c9e26fcf3aa5|

E012 camera-fixed ROI is a HOST-ONLY experiment using the unchanged Split-Pose
checkpoint, four cropped calls and one global NMS.345frames/1380CPUcalls/173.06s;
running matches0/46unchanged, walking11/482→27/482 with one old match lost.
REJECTED on the predeclared primary gate; not in production video inference, not
compiled/uploaded, no new TPU artifact and no new LinQ invocation. No model or
threshold replacement is made by this technical eight-rule release.

## Received rejected CPU fine-tune — continuation 24 October

Training handoff10992b4d22c5218569132729de1864726d8cc446f3441338cfdc1c00541c3a65
was received with verified result/best/last/baseline bytes. This is an MLP temporal
head on cached GMD pose features, despite the directory name yolo_pilot. Six CPU
epochs, best epoch1; reported paired weak-video validation macroF1 .72953216374269
for both baseline and candidate, gain0. REJECT_KEEP_BASELINE; no model promotion,
export/compile/PTQ/actualLinQ or independent event qualification. Checkpoint digests
and receipt: reports/intake-20261024.json. No checkpoint was deserialized by root.

Canonical reuse constraints v2 (SHA4598a443...) supersede the mistaken v1 head4
folder description: head4 trains subjects2/3, selects on1, outer development4.
Heads1/2/3 saw Subject4 in training/selection. An all-four ensemble cannot be
reported as held-out Subject4. Four heads remain unselected/export-only.

## Captain video handoff before18:00MSK

Existing Helmet/Split-Pose bytes retained. Portable intermediate exports now
carry13real-source frames/15historical actualTPUcompletions, with full selected
numeric arrays, original MP4, source/PTS/RGB/input/decoder proof. No new model or
TPU submission. Exact paths and limits: docs/handoffs/EGOR_LINQ_VIDEO_20261024.md
and reports/video-handoff-20261024.json. Product mapping helmet/no_helmet/person
follows main contract; final Argus schema pending. Historical PIL preprocessing
is not identical to current app OpenCV, and full actual transforms are preserved.

## Complete local scene export

Same Helmet/Pose weights plus existing official COCO80 reference f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36
were run on all770frames/7videos on free lockedRTX4090. COCO reference is local
only, not Matvey-trained or TPUqualified. No new checkpoint/compile/promotion.
All classmaps, fixed.25/.45 thresholds, decoded observations and per-model TPU
coverage are in scene-packs-20261024. Object proposals are not GT/events;
report/limits docs/handoffs/SCENE_PACKS_20261024.md.
