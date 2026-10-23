
## Detailed normalized evidence dossiers

These canonical fact records retain substantive findings from all16W1 and7W2 reports in the public evidence base itself. Source-only registries are in SOURCES. They are grouped by research question; earlier W1 observations remain historical, and the canonical decision records F001–F025 and later W2 outcomes govern supersession. A branch-local test keeps its original meaning (CSV/static/media inspection), not neural execution. Embedded proposed tests are proposals. Internal method/alias labels are provenance names, not additional measured systems.

<a id="F026"></a>
### F026 — W1_M01: W1 M01 — Pose models: factory suitability and verified artifact paths

Provenance: [W1_M01:1](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M01 — Pose models: factory suitability and verified artifact paths

Research access began **2026-10-23 19:14 UTC** (22:14 Europe/Moscow); report saved 2026-10-23 19:22 UTC. Worker owns only this report and `_WORK/M01/`. All network checks below were performed here; **no model, video, training, export, compilation or LinQ execution was performed**. `local_test` is deliberately unused for network checks. Small source files and two model-card PDFs were saved; checkpoint/video archives were not downloaded. Access evidence: `M01/FETCH.json`, `FETCH2.json`, `FETCH3.json`, `ARTIFACT_HEAD.json`, `MOVENET_ACCESS.json`, `REVISIONS.json`. The case requirements were supplied in the worker assignment; root's direct case reading is in the sibling file `CASE_NOTES.md` (`_WORK/CASE_NOTES.md` from workspace root).

<a id="F027"></a>
### F027 — W1_M01: Branch question and decision

Provenance: [W1_M01:5](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

**Question:** Which actual pose artifacts are worth testing for CCTV safety, what do their benchmark numbers mean, and when does a skeleton add evidence beyond person boxes, tracking and camera zones?

**Decision [inference]:** keep **detector + tracking + ROI as the common baseline**. Add a gated pose branch for lying/posture transitions and climbing/crawling evidence when sufficient joints are actually visible. First compare **RTMPose-m (top-down, explicit crop and decode)** with **YOLO11n/s-pose (single-stage convenience baseline, licensing decision required)**. Add **RTMO-s/m** when simultaneous person count makes per-person crops costly. Use **ViTPose-B** as an offline accuracy comparator with detector conditions held constant, rather than claiming its benchmark implies a deployable factory winner. Treat MoveNet and MediaPipe as exploratory close-person comparators: their own model cards materially restrict the domain and do not validate industrial surveillance. **No candidate has verified LinQ compatibility here.** ONNX existence means an artifact to inspect, not support by the unknown LinQ compiler/runtime.

The strongest new information is not another leaderboard: (1) RTMPose pipeline timings skip detector frames; (2) ViTPose occlusion scores assume ground-truth boxes; (3) standard COCO keypoint evaluation omits a small-person bucket; (4) MediaPipe API and older linked model card describe different multi-person capability; (5) a real TFHub artifact returned HEAD 404 but GET 200.

<a id="F028"></a>
### F028 — W1_M01: Facts and consequential limitations

Provenance: [W1_M01:13](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Facts and consequential limitations

<a id="F029"></a>
### F029 — W1_M01: M01-F001 — MMPose is a toolbox, not one checkpoint [primary_docs]

Provenance: [W1_M01:15](_WORK/W1_M01.md); original aliases: M01-F001. Sources: [S023](SOURCES.md#S023), [S024](SOURCES.md#S024), [S025](SOURCES.md#S025), [S026](SOURCES.md#S026), [S027](SOURCES.md#S027), [S028](SOURCES.md#S028), [S029](SOURCES.md#S029).

### [M01-F001](RAW_FACTS.md#F029) — MMPose is a toolbox, not one checkpoint [primary_docs]

MMPose provides top-down, bottom-up and 3D model families; choosing “MMPose” does not fix joints, detector, resolution, training data or deployment graph. Its 1.x API/config migration matters: original ViTPose is an older MMPose-derived repository, so mixing its configs with current MMPose without porting is not a reproducible command. MMPose code root LICENSE is Apache-2.0; the separately inspected `LICENSES.md` lists EDPose under IDEA License 1.0. This is a concrete reason not to extrapolate the root code license to every model in the toolbox. RTMPose and RTMO code/configs are available in the inspected current repository. [[M01-S001](SOURCES.md#M01-S001), [M01-S002](SOURCES.md#M01-S002), [M01-S003](SOURCES.md#M01-S003)]

<a id="F030"></a>
### F030 — W1_M01: M01-F002 — Candidate contracts and architecture [primary_docs unless marked inference]

Provenance: [W1_M01:19](_WORK/W1_M01.md); original aliases: M01-F002. Sources: [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S021](SOURCES.md#S021), [S026](SOURCES.md#S026), [S027](SOURCES.md#S027), [S028](SOURCES.md#S028), [S029](SOURCES.md#S029), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031), [S032](SOURCES.md#S032), [S033](SOURCES.md#S033), [S034](SOURCES.md#S034), [S035](SOURCES.md#S035), [S036](SOURCES.md#S036), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040).

### [M01-F002](RAW_FACTS.md#F030) — Candidate contracts and architecture [primary_docs unless marked inference]

| Family / concrete branch | Dimensionality and inference route | Inputs → useful outputs | CCTV implications / failures |
|---|---|---|---|
| Ultralytics **YOLO11 pose** | 2D, single-stage person box + keypoint prediction; not an external bbox-first crop pipeline and not classic bottom-up joint grouping | Image, typical 640 input; one person class; COCO 17 joints; public result wrappers expose person boxes and `(N,17,2)` xy plus `(N,17)` confidence | [inference] Simple whole-frame baseline; resizing distant workers loses pixels; overlapping/occluded workers can cause missed/incorrect instances or joints. It is not a fall/action classifier. Exact raw tensor layout varies with export, so inspect the exported graph rather than treating wrapper output as ONNX contract. |
| **RTMPose-m**, 17-joint COCO/AIC model | 2D **top-down**, requires a detected/otherwise supplied person box | Crop `(width,height)=(192,256)`; normalize and NCHW; SimCC x and y vectors → 17 xy and scores; split ratio 2 gives x/y vector lengths 384/512 for this config | [inference] Crop preserves person allocation within network input but cannot restore missing image detail; detector failure is unrecoverable by pose. Multiple crops scale with person count; partial boxes/cropped feet and association errors contaminate posture. |
| **RTMO-s**, COCO / body7 | 2D one-stage; MMPose config explicitly `data_mode='bottomup'`, `BottomupPoseEstimator`; YOLO-style dense instance prediction with dynamic coordinate classification | 640×640 image; 17 joints, boxes and scores after postprocessing; no separate person detector needed | Authors claim faster than RTMPose above four persons, measured in their setup. [inference] A sensible crowded-scene branch, not evidence that unseen/occluded joints are observable or that tiny workers succeed. CrowdPose-trained checkpoints differ from COCO/body7 checkpoints. |
| **MoveNet SinglePose Lightning / Thunder** | 2D center/heatmap architecture; Google calls it bottom-up, but **SinglePose emits only one selected person**, not all workers | RGB 192² / 256²; TF tutorial SavedModel input int32; output `[1,1,17,3]` ordered **y,x,score**, normalized; video crop follows previous pose | [inference] Wrong-center person selection or crop continuity can silently change worker. SinglePose must not be applied to a full multi-worker image and treated as person-complete. |
| **MoveNet MultiPose Lightning v1** | 2D single forward pass for multiple instances | RGB `[1,H,W,3]`, H/W multiples of 32; recommended longest side 256; TF.js int32 / TFLite uint8; output float32 **`[1,6,56]`**: 51 y/x/score entries + ymin/xmin/ymax/xmax/instance score | **Maximum six detections** is an actual model limit, not a configurable tracker capacity. TF.js maxTracks=18 is not 18 simultaneous detections. Card says optimized for people 3–6 feet from webcam. |
| **MediaPipe Pose Landmarker**, full float16 v1 bundle | Detector → landmark ROI, with tracking in video/live modes; outputs image 2D+relative-z and estimated 3D | Detector 224² and landmarker 256²; **33 landmarks**, normalized image xyz/visibility; `WorldLandmarks` uses meters with hip midpoint origin; optional segmentation | Current API `num_poses` is an integer >0, **default 1**; no finite hard maximum is documented in inspected guide/code. Do not call API intrinsically single-person. [inference] Estimated hip-relative world coordinates are not calibrated camera-to-worker/machine distances. |
| **ViTPose-B**, classic COCO decoder | 2D top-down transformer + heatmap decoder; external detector boxes | 256×192 crop (config `[192,256]` width,height), COCO 17 joints, heatmaps decoded to xy+score | [inference] Useful accuracy comparator if detector/crop settings are held equal. Higher pose AP does not repair failed detection; GT-box occlusion scores are especially optimistic for an end-to-end CCTV pipeline. Larger variants add compute without target-domain proof. |
| Optional **RTMW / RTMPose whole-body** | Separate 2D whole-body branches; RTMW paper covers 2D/3D variants, not every downloadable RTMW weight is 3D | COCO-WholeBody branch has **133** keypoints; published 256×192 and 384×288 configs and pth/ONNX links | [inference] Potential close-up hand/foot detail, but a 133-joint prediction cannot establish a tiny phone/cigarette/harness or recover obscured hands. Keep outside first implementation unless these details measurably help. Artifacts found in README; not all independently access-checked. |

Sources: [M01-S002](SOURCES.md#M01-S002)–S009. Exact configs and inference code were fetched and preserved, not inferred from marketing names.

<a id="F031"></a>
### F031 — W1_M01: M01-F003 — RTMPose accuracy and speed refer to different pipelines [author_claim + primary_docs]

Provenance: [W1_M01:34](_WORK/W1_M01.md); original aliases: M01-F003. Sources: [S026](SOURCES.md#S026), [S027](SOURCES.md#S027).

### [M01-F003](RAW_FACTS.md#F031) — RTMPose accuracy and speed refer to different pipelines [author_claim + primary_docs]

The inspected RTMPose README has explicit separate sections:

* **Pipeline Performance:** detector invoked every **5 frames by default**, **flip test not used**; ONNXRuntime 1.12.1, TensorRT 8.4.3.1, CUDA 11.3, cuDNN 8.3.2, ncnn 20221128. RTMDet-nano+RTMPose-m row: 320² detector, 256×192 pose, pipeline AP 73.2, i7-11700 ORT 26.613 ms, GTX1660Ti TRT-FP16 4.312 ms. This is a published condition, not our measured stream throughput.
* **Model Zoo:** **flip test is used**; RTMPose-m AIC+COCO 256×192 row reports AP 75.8 and i7-11700 ORT latency 11.06 ms. It is not detector+tracker+decode+notification latency.
* README warns its multi-domain model results are unsuitable for academic comparison. Body7 models use combined datasets; Body8 describes evaluation adding OCHuman to seven datasets, not a new universally equivalent 8-training-dataset checkpoint.
* The pinned `rtmpose-m_8xb256-420e_coco-256x192.py` has COCO train/val annotations and `test_cfg.flip_test=True`, but the detection `bbox_file` is **commented out**. Do not assume running that config verbatim reproduces a published detector-based pipeline result. Record whether evaluation boxes are ground-truth or detections; inspect actual loader output before reporting a number.

**Consequence [inference]:** for rapid falls or entry into machinery, adopting detector interval=5 because it made a demo fast may delay first observation or omit a short event. Benchmark cadence is not a recommended safety cadence. Compare every-frame measurements and any proposed skip policy against event recall and onset latency using source timestamps. [[M01-S002](SOURCES.md#M01-S002)]

<a id="F032"></a>
### F032 — W1_M01: M01-F004 — RTMO figures depend on training mixture and hardware [author_claim]

Provenance: [W1_M01:45](_WORK/W1_M01.md); original aliases: M01-F004. Sources: [S028](SOURCES.md#S028), [S029](SOURCES.md#S029).

### [M01-F004](RAW_FACTS.md#F032) — RTMO figures depend on training mixture and hardware [author_claim]

RTMO-s COCO-only reports AP .677; body7 RTMO-s reports .686 on COCO val2017. RTMO-l COCO-only .724 versus body7 .748. Published latency s/m/l 8.9/12.4/19.1 ms is **V100 GPU + ONNXRuntime**. The latter .748 is not a pure COCO-trained score. CrowdPose-only RTMO-s test AP .673 with hard-crowd .591; body7 RTMO-l CrowdPose .838 with hard .772. These are different model/training rows, and hard crowd remains a materially different difficulty. No CPU or LinQ speed follows from these numbers. [[M01-S003](SOURCES.md#M01-S003)]

<a id="F033"></a>
### F033 — W1_M01: M01-F005 — ViTPose occlusion benchmark does not include detector failure [primary_docs]

Provenance: [W1_M01:49](_WORK/W1_M01.md); original aliases: M01-F005. Sources: [S030](SOURCES.md#S030).

### [M01-F005](RAW_FACTS.md#F033) — ViTPose occlusion benchmark does not include detector failure [primary_docs]

Original ViTPose README explicitly states **OCHuman test results use ground-truth bounding boxes**. Its COCO val table uses a detector with **56 AP on person**, and the inspected B config sets `use_gt_bbox=False`, a concrete detection JSON `COCO_val2017_detections_AP_H_56_person.json`, `flip_test=True`. COCO B classic decoder AP75.8/AR81.1 at 256×192 and OCHuman multi-task B AP88.0 are not directly comparable evidence that occluded workers are easier than normal workers. They use different evaluation and training conditions. [[M01-S004](SOURCES.md#M01-S004)]

<a id="F034"></a>
### F034 — W1_M01: M01-F006 — Standard COCO pose AP has no small-person breakdown [primary_docs + inference]

Provenance: [W1_M01:53](_WORK/W1_M01.md); original aliases: M01-F006. Sources: [S041](SOURCES.md#S041).

### [M01-F006](RAW_FACTS.md#F034) — Standard COCO pose AP has no small-person breakdown [primary_docs + inference]

Original `pycocotools/cocoeval.py`, `Params.setKpParams`, uses maxDets `[20]` and area labels **all, medium, large**, with ranges `[0,1e10]`, `[32²,96²]`, `[96²,1e10]`. Detection evaluation separately has a small bucket. Thus “all” may include small instances with valid labels; **do not claim small people are excluded from all AP**. The defensible statement is that default keypoint summaries do not report AP-small and aggregate pose AP does not establish far-worker quality. `num_keypoints==0` instances are ignored by keypoint evaluation; `v>0` is used for annotated joint matching. COCO `(x,y,v)` ground-truth visibility is not the same semantic as a learned model confidence score. [[M01-S010](SOURCES.md#M01-S010)]

**Target evaluation [inference]:** stratify by original-image person height/area, visible joints, partial frame truncation, crowding and camera elevation, with denominators including detector misses. Do not resize everything and then define “small” from model-input crop size.

<a id="F035"></a>
### F035 — W1_M01: M01-F007 — Google model cards narrow the industrial relevance [primary_docs]

Provenance: [W1_M01:59](_WORK/W1_M01.md); original aliases: M01-F007. Sources: [S021](SOURCES.md#S021), [S033](SOURCES.md#S033), [S034](SOURCES.md#S034), [S035](SOURCES.md#S035), [S036](SOURCES.md#S036), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040).

### [M01-F007](RAW_FACTS.md#F035) — Google model cards narrow the industrial relevance [primary_docs]

The **BlazePose GHUM 3D model card dated April 16, 2021**, authors Valentin Bazarevsky, Ivan Grishchenko, Eduard Gabriel Bazavan, says single-person video; out-of-scope examples include **more than 4m distance, head invisible, multiple people, metric-accurate depth, surveillance/identity recognition**. Training includes 30K consented mobile AR images and majority 85K fitness-pose images; images are back-facing smartphone captures. It says z is up to scale from GHUM fitting; invisible/hard-to-label positions may be annotated by a best guess/default pose. Older MediaPipe quality benchmark uses one person 2–4m from camera in Yoga/Dance/HIIT and evaluates 17 COCO points, not all 33. This is highly unlike distant industrial overhead CCTV. [[M01-S007](SOURCES.md#M01-S007), S008]

**Important version distinction:** current Pose Landmarker Python guide, last updated **2026-08-17 UTC**, supports `num_poses>1` (default1) and documents hip-relative `WorldLandmarks` in meters. This does not retroactively make the 2021 card a multi-worker validation study. It also does not prove the current full task bundle supplies calibrated scene geometry. Treat the discrepancy as a scope/version limitation to resolve, not as proof that the API cannot output multiple poses. [[M01-S006](SOURCES.md#M01-S006), S007]

MoveNet MultiPose's official card (no publication date visible in fetched PDF) similarly names 3–6ft webcam use, maximum6 people, and surveillance out of scope. It documents **29K final COCO training images after excluding images with three or more people**, 120K Active YouTube fitness images and 21K synthetic images. Evaluation includes 2.7K COCO-person images and 1.9K Active images. These are pose-label images sampled from videos, not fall onset/lying-duration event annotations. The card reports averaged OKS, not the same measure as COCO AP. [[M01-S009](SOURCES.md#M01-S009)]

Out-of-scope/intended-use language is preserved as the authors' scope statement. It is not silently equated with a separate license restriction or a legal conclusion about our use.

<a id="F036"></a>
### F036 — W1_M01: M01-F008 — Temporal wrappers can invalidate the observation stream [primary_docs + inference]

Provenance: [W1_M01:69](_WORK/W1_M01.md); original aliases: M01-F008. Sources: [S021](SOURCES.md#S021), [S033](SOURCES.md#S033), [S034](SOURCES.md#S034), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040).

### [M01-F008](RAW_FACTS.md#F036) — Temporal wrappers can invalidate the observation stream [primary_docs + inference]

Current MediaPipe Python guide explicitly says `detect_async` **ignores a new input frame if busy**. Video/live modes require frame timestamps. TF.js MoveNet defaults `enableSmoothing=True`; crop/keypoint filters and tracker age defaults are in source, including nominal 30Hz keypoint filtering. A wrapper's smoothed output and a tracker-propagated box are not proof that the worker was visually measured at each logical tick.

**Consequence [inference]:** maintain source PTS, request/result status, per-joint confidence/visibility and original crop transform. A dropped/busy frame is unknown, not an observed negative. Never count smoothing/interpolation as observed immobility or fall trajectory evidence. Sparse sampling must be evaluated after its real filters, dropped frames, association changes and detection cadence, not by applying a high-FPS paper claim to a 1-FPS system. [[M01-S006](SOURCES.md#M01-S006), S009]

<a id="F037"></a>
### F037 — W1_M01: Exact artifact and source/config routes

Provenance: [W1_M01:75](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Exact artifact and source/config routes

<a id="F038"></a>
### F038 — W1_M01: M01-F009 — Access-checked weight/archive manifest [artifact_access_checked]

Provenance: [W1_M01:77](_WORK/W1_M01.md); original aliases: M01-F009. Sources: [S002](SOURCES.md#S002), [S003](SOURCES.md#S003), [S004](SOURCES.md#S004), [S005](SOURCES.md#S005), [S006](SOURCES.md#S006), [S007](SOURCES.md#S007), [S008](SOURCES.md#S008), [S009](SOURCES.md#S009), [S010](SOURCES.md#S010), [S011](SOURCES.md#S011), [S012](SOURCES.md#S012).

### [M01-F009](RAW_FACTS.md#F038) — Access-checked weight/archive manifest [artifact_access_checked]

All URLs below are primary publisher paths or their original model-share links. HEAD checks establish server metadata only. No deserialization/inference or full archive integrity check was performed. Full transient redirect URLs are in JSON; use stable original URLs.

| ID | Exact artifact | Check / access condition |
|---|---|---|
| M01-A01 | https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-m_simcc-aic-coco_pt-aic-coco_420e-256x192-63eb25f7_20230126.pth | HEAD200, application/octet-stream, **54,536,690 bytes** |
| M01-A02 | https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/onnx_sdk/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip | HEAD200 zip, **50,799,818 bytes**. **Different training mixture from A01**; do not claim this is A01's equivalent export. |
| M01-A03 | https://download.openmmlab.com/mmpose/v1/projects/rtmo/rtmo-s_8xb32-600e_coco-640x640-8db55a59_20231211.pth | HEAD200 octet-stream, **39,718,803 bytes** |
| M01-A04 | https://download.openmmlab.com/mmpose/v1/projects/rtmo/onnx_sdk/rtmo-s_8xb32-600e_body7-640x640-dac2bf74_20231211.zip | HEAD200 zip, **36,442,532 bytes**. body7, **not A03's COCO-only equivalent**. |
| M01-A05 | https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-pose.pt | HEAD follows release-assets redirect,200 octet-stream, **6,255,593 bytes** |
| M01-A06 | https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task | HEAD200 octet-stream, **9,398,198 bytes** |
| M01-A07 | https://tfhub.dev/google/lite-model/movenet/multipose/lightning/tflite/float16/1?lite-format=tflite | **HEAD404, streamed GET200** to Google storage; 9,585,276 bytes reported; first512 bytes read, prefix includes **TFL3**. HEAD404 did not mean missing weights. |
| M01-A08 | https://www.kaggle.com/api/v1/models/google/movenet/tfLite/multipose-lightning-tflite-float16/1/download | Streamed GET200 gzip, **8,824,426 bytes** reported, first512 bytes only; anonymous request succeeded at access time. |
| M01-A09 | https://www.kaggle.com/api/v1/models/google/movenet/tensorFlow2/multipose-lightning/1/download | Streamed GET200 gzip, **18,612,451 bytes** reported, first512 bytes only. |
| M01-A10 | https://1drv.ms/u/s!AimBgYV7JjTlgSMjp1_NrV3VRSmK?e=Q1uZKs | Original ViTPose-B single-COCO share. HEAD200 redirects to **HTML landing page**, content-length0. **Binary access not established**; does not prove absent. |
| M01-A11 | http://images.cocodataset.org/annotations/annotations_trainval2017.zip | HEAD200 zip, **252,907,541 bytes**. Actual annotation archive listed by COCO; **not downloaded**. Includes source train/val annotation paths named by configs; no video-event labels implied. |

The SinglePose Thunder int8 legacy TFHub URL from the official tutorial also returned HEAD404; no independent GET was made for that specific file, so it remains only artifact_found rather than artifact_access_checked for successful binary access.

<a id="F039"></a>
### F039 — W1_M01: M01-F010 — Configuration and runnable code links [artifact_found + primary_docs]

Provenance: [W1_M01:97](_WORK/W1_M01.md); original aliases: M01-F010. Sources: [S013](SOURCES.md#S013), [S014](SOURCES.md#S014), [S015](SOURCES.md#S015), [S016](SOURCES.md#S016), [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S019](SOURCES.md#S019), [S020](SOURCES.md#S020), [S021](SOURCES.md#S021), [S022](SOURCES.md#S022).

### [M01-F010](RAW_FACTS.md#F039) — Configuration and runnable code links [artifact_found + primary_docs]

* RTMPose-m config: https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-m_8xb256-420e_coco-256x192.py . Original CPU ONNX example: https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/projects/rtmpose/examples/onnxruntime/main.py . Example uses mean `[123.675,116.28,103.53]`, std `[58.395,57.12,57.375]`, affine resize, NCHW and explicit SimCC decoding/inverse mapping. Run the example only with the correct crop/transform contract; do not reinterpret a whole-image pose result as detector-complete multi-person output.
* RTMO-s config: https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/configs/body_2d_keypoint/rtmo/coco/rtmo-s_8xb32-600e_coco-640x640.py . Training 600epochs, bottomup COCO train2017; RTMO head implementation: https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/mmpose/models/heads/hybrid_heads/rtmo_head.py . README provides `tools/train.py`, `tools/test.py`, and MMDeploy export path `configs/mmpose/pose-detection_rtmo_onnxruntime_dynamic-640x640.py`; no export performed here.
* YOLO11 pose yaml: https://github.com/ultralytics/ultralytics/blob/0bcee3df04c7a441b07c755202c2ea962cb7c387/ultralytics/cfg/models/11/yolo11-pose.yaml ; training/inference/export documentation https://docs.ultralytics.com/tasks/pose/ . Current docs default to newer YOLO26; pin the selected YOLO11 checkpoint/config instead of letting documentation defaults silently select another family. This report does not establish YOLO11 is the latest/best Ultralytics model.
* ViTPose-B config: https://github.com/ViTAE-Transformer/ViTPose/blob/c050ed29112da7704797cc1a65af0234b525010d/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/ViTPose_base_coco_256x192.py . Training/eval source under same repository `tools/`; MAE pretraining and external detection boxes are separate dependencies, not included by simply downloading pose weights.
* MoveNet inference wrapper/config: https://github.com/tensorflow/tfjs-models/blob/c731b9ebbd6f4c9e8bf99b0df76bbdbf9c25b07f/pose-detection/src/movenet/detector.ts and `constants.ts`; Python reference inference https://www.tensorflow.org/hub/tutorials/movenet . Published Google blog says trained with TensorFlow Object Detection API, but **exact released training recipe/config and full Active training dataset were not established as publicly reproducible here**. Generic TF OD source existence is not a reproducible MoveNet training artifact.
* MediaPipe task wrapper: https://github.com/google-ai-edge/mediapipe/blob/fd288e22e1b9fa5c2639dcd01129c15677630057/mediapipe/tasks/python/vision/pose_landmarker.py . Task bundle A06 and graph/runtime wrapper are public. **Exact training code/config and underlying consented image corpus for the released GHUM models were not found in inspected materials.**

<a id="F040"></a>
### F040 — W1_M01: M01-F011 — Licenses must be tracked by artifact type [primary_docs / unknown as stated]

Provenance: [W1_M01:106](_WORK/W1_M01.md); original aliases: M01-F011. Sources: [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S021](SOURCES.md#S021), [S023](SOURCES.md#S023), [S024](SOURCES.md#S024), [S025](SOURCES.md#S025), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031), [S032](SOURCES.md#S032), [S035](SOURCES.md#S035), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040), [S042](SOURCES.md#S042), [S043](SOURCES.md#S043), [S044](SOURCES.md#S044).

### [M01-F011](RAW_FACTS.md#F040) — Licenses must be tracked by artifact type [primary_docs / unknown as stated]

| Family | Code | Weights/model declaration | Data |
|---|---|---|---|
| Ultralytics pose | Root **AGPL-3.0**; official licensing page offers AGPL and Enterprise routes | Vendor licensing page addresses model use under those routes; do not relabel downloaded `.pt` Apache/MIT. A separate permissive weight grant was not established. | COCO annotation/image rights remain separate; Ultralytics code license does not replace them. |
| RTMPose / RTMO | MMPose Apache-2.0; inspect algorithm-specific exceptions; no RTMPose/RTMO exception in fetched `LICENSES.md` | Publisher downloadable weights found. Root Apache code license is evidence for code, **a separate weight-specific terms file inside archives was not inspected**; keep that distinction in distribution manifest. | AIC/COCO/body7 is not one uniformly licensed dataset. Component terms need their own checks. |
| ViTPose | Original repository Apache-2.0 | Original shares found, but no separately inspected weight-specific grant beyond repository declaration | COCO vs mixed COCO+AIC+MPII/CrowdPose variants differ; do not silently inherit repository license for media. |
| MoveNet | TF.js model wrapper Apache-2.0 source header | Google-owned Kaggle variation page declares **Apache2.0**; original card also states intended/out-of-scope use | COCO plus internal Active and synthetic sources; no public reusable release/rights manifest for Active established. |
| MediaPipe | Apache-2.0 source | Linked BlazePose GHUM card says **Apache License Version2.0**; current task bundle's separate embedded terms not inspected | Consented mobile AR/fitness training media are not a freely downloadable public dataset merely because model is Apache. |
| COCO | COCO software has BSD-style terms | Not applicable | **Annotations CC BY4.0; images owned by original holders/Flickr terms**, explicitly separated on original terms page. |

This is an evidence register, not a legal conclusion about distributing an entire combined application. Preserve both actual terms and authors' domain limitations without converting one into the other. [[M01-S001](SOURCES.md#M01-S001), S004, S005, S007, S009, S011]

<a id="F041"></a>
### F041 — W1_M01: Skeleton necessity by industrial scenario

Provenance: [W1_M01:119](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Skeleton necessity by industrial scenario

<a id="F042"></a>
### F042 — W1_M01: M01-F012 — Task decomposition [inference, proposed design; no model validation]

Provenance: [W1_M01:121](_WORK/W1_M01.md); original aliases: M01-F012. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [M01-F012](RAW_FACTS.md#F042) — Task decomposition [inference, proposed design; no model validation]

| Scenario | Baseline evidence | Skeleton contribution and limit |
|---|---|---|
| Running / sudden motion | Tracked ground-contact trajectory, camera-specific perspective/scale, source-time displacement; classify motion relative to scene | Temporal leg/arm motion can help distinguish walking/running in clear views. Single skeleton cannot prove running. Camera perspective and low cadence can alias gait; pose is optional, not prerequisite. |
| Moving-machine proximity | Person/machine detection+tracking, calibrated hazard zones/ground plane where valid, machine motion state | Pose can estimate visible ankle/foot position instead of box center. **Box overlap or hip-relative learned z does not prove physical proximity.** Partial occlusion may remove the very foot contact needed. |
| Prohibited phone use | Small-object detection, person/object association, head/hand crop, work/movement context and temporal confirmation | Wrist/head geometry narrows candidate crops; 17 body joints do not detect a phone. Hand near face has negatives including radio, wiping sweat, glasses, hearing protection, scratching, eating/drinking. |
| Smoking / open fire | Cigarette/smoke/flame evidence and designated-zone policy, time continuity | Pose may gate hand-to-mouth candidates but cannot establish cigarette or combustion. No skeleton required for visible flame outside allowed ROI. |
| Barrier climbing / under conveyor or suspended load | Barrier/machine/load geometry+ROI, person occupancy and path; policy configured per camera | Joint arrangement can support climbing/crawling when visible; must distinguish crouching beside from passing beneath. A hidden person cannot be “safe” because skeleton vanished. A worker behind equipment can overlap the equipment in 2D without being underneath. |
| Work at height without harness | Height/work-area context plus visible harness/lanyard/anchor evidence and association | Skeleton helps localize torso but does not prove harness absence or correct attachment; 2D body pose does not establish height above ground. |
| Fall / lying / immobility | Person detection and temporal state; visible low posture, onset transition, subsequent movement; confidence and occlusion state | Most useful pose branch. Distinguish **fall transition**, **currently lying**, **observed low motion** as separate labels. One horizontal-looking pose is not a fall. No inference of unconsciousness. |
| Improper carrying | Carried-object detection+association and actual known handling rule/SKU/context | Joint posture supports visible lifting pattern only. It does not determine load mass, safe force, fatigue or universal improper-carrying status. |

<a id="F043"></a>
### F043 — W1_M01: M01-F013 — Lying/falling/crouching and camera angle [inference]

Provenance: [W1_M01:134](_WORK/W1_M01.md); original aliases: M01-F013. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [M01-F013](RAW_FACTS.md#F043) — Lying/falling/crouching and camera angle [inference]

Required semantic separation:

1. **Lying:** a visible posture state with adequate torso/limb evidence; deliberate maintenance work, resting and staged floor exercise can share it.
2. **Falling:** a temporal transition whose onset and trajectory must actually be sampled; entry already lying is left-censored, not an observed fall.
3. **Crouching/kneeling/bending/seated:** hard negatives that shorten torso/box height without a fall.
4. **Immobility:** low measured motion over a documented interval, conditional on sufficient visibility; tracker predictions or repeated stale frames do not establish it.

At overhead/high elevation, standing torsos project short; along-camera-axis lying may not produce a wide bbox or horizontal skeleton. Perspective, camera roll and changing person distance alter 2D angles. Foreshortening can compress knees/hips; left/right swaps, foreign-worker joints at crossings and plausible hallucinated hidden joints can create abrupt kinematics. These are concrete target-test hypotheses, not measured rates for each family. Thresholds must be per-camera or camera-normalized and validated; no universal torso-angle/bbox-aspect rule is justified by the cited pose benchmarks.

For a person below equipment, treat blocked lower body or detector miss as **unknown visibility**, not a negative under-machine observation. Require enough scene geometry to disambiguate under/behind/alongside; source footage may be intrinsically unobservable from one view. Retain operator-review evidence instead of claiming depth recovery from generic 2D keypoints or monocular world landmarks.

<a id="F044"></a>
### F044 — W1_M01: Dataset, label and leakage links

Provenance: [W1_M01:147](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Dataset, label and leakage links

<a id="F045"></a>
### F045 — W1_M01: M01-F014 — Pose training annotations do not label industrial events [primary_docs + inference]

Provenance: [W1_M01:149](_WORK/W1_M01.md); original aliases: M01-F014. Sources: [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S021](SOURCES.md#S021), [S026](SOURCES.md#S026), [S027](SOURCES.md#S027), [S028](SOURCES.md#S028), [S029](SOURCES.md#S029), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031), [S032](SOURCES.md#S032), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040), [S041](SOURCES.md#S041), [S042](SOURCES.md#S042), [S043](SOURCES.md#S043), [S044](SOURCES.md#S044).

### [M01-F014](RAW_FACTS.md#F045) — Pose training annotations do not label industrial events [primary_docs + inference]

COCO annotation archive A11 and configs point to `person_keypoints_train2017.json` / `person_keypoints_val2017.json`. Standard COCO person annotation contains image/person instance linkage, bbox, area, `iscrowd`, `num_keypoints`, flattened 17×`(x,y,v)`. `v=0` unlabeled, `v=1` labeled but invisible, `v=2` labeled visible. These are per-image posture labels, not action start/end, fall cause, machinery state, prohibition policy, elapsed lying duration or carried mass. YOLO pose training text format separately encodes normalized person box and normalized keypoints; do not copy learned confidence into annotation visibility as if identical semantics. [[M01-S005](SOURCES.md#M01-S005), S010, S011]

RTMPose body7 and RTMO body7 include **AIC, COCO, CrowdPose, Halpe, MPII, PoseTrack18, sub-JHMDB**. ViTPose has single-task and mixed dataset variants; OCHuman evaluations differ in bbox protocol. **Known overlap risk:** evaluating a body7 pretrained model on frames/clips from its PoseTrack/sub-JHMDB sources may test training exposure, including people/scenes adjacent to action clips. Mixed checkpoints and same-benchmark AP require split-specific verification; training on a dataset name does not by itself prove test split leakage. Preserve exact checkpoint mixture, source video/person IDs and split membership. [[M01-S002](SOURCES.md#M01-S002), S003, S004]

MoveNet Active is video-derived, with original 2021 SinglePose launch blog saying at most3 frames per source video for training diversity. That statement does not establish video-disjoint holdout or reuse rights; the MultiPose card does not provide a full source-ID split manifest. **Unknown:** exact overlap of any target demo videos with Google internal Active material. Do not claim uncontaminated validation simply because the images were downloaded from a different mirror. [[M01-S009](SOURCES.md#M01-S009)]

<a id="F046"></a>
### F046 — W1_M01: Proposed discriminating experiment, not executed

Provenance: [W1_M01:157](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Proposed discriminating experiment, not executed

<a id="F047"></a>
### F047 — W1_M01: M01-F015 — A small test that changes the selection [hypothesis / proposed]

Provenance: [W1_M01:159](_WORK/W1_M01.md); original aliases: M01-F015. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [M01-F015](RAW_FACTS.md#F047) — A small test that changes the selection [hypothesis / proposed]

Inputs needed: authorized original CCTV clips and source timestamps, target camera geometry/context, annotated person boxes/keypoints for a bounded subset, event onset/offset intervals with visibility status, and later actual LinQ SDK/runtime/device access. Future RTX3090 work is separate from this research.

**Compare:** same person detector+tracker baseline; detector+RTMPose-m; YOLO11n/s-pose; RTMO-s; optional detector+ViTPose-B. First hold detector boxes constant for top-down models, then rerun end-to-end with detector errors included. Freeze hashes/configs and input/crop transforms. Evaluate raw and filtered temporal outputs separately. Do not compare one model with GT boxes to another with detections.

**Strata/hard negatives:** person size in original camera pixels; high/low/overhead angles; PPE/workwear; one/two/crowded workers; torso/legs/head occluded; frame-edge truncation; low light, steam, glare; voluntary lying under a machine, kneeling repair, crouch-to-stand, bending to pick up object, seated low stool, crawling beside vs under conveyor, entering already lying, standing worker hidden by passing load, another person crossing, camera vibration, compression artifacts. Do not create a false fall label for allowed maintenance lying.

**Metrics:** end-to-end person recall; percentage of ticks with sufficient task-relevant visible joints; errors on visible versus occluded joints separately; per-person association switches; fall-event recall and onset latency; lying-state precision/recall; false alarms per camera-hour; unknown/coverage fraction; duplicate incident rate. Report worst camera/size/occlusion strata and confidence intervals where sample count permits. Hardware: complete graph preprocessing/inference/decoding/tracking duration, actual processed cadence, queue/busy drops, and result-age distribution. Average FPS alone is inadequate.

**Cadence test:** replay same source at native and proposed sparse rates with timestamp-preserving frame selection; include transitions shorter than the proposed sampling interval. Recheck after filtering or detector-skip changes. A pose method wins only if its extra cost reduces event misses/false alarms or provides usable coverage in the required cameras. If skeleton disappears at task-critical moments, fall back to uncertainty/review; do not train logic to count hidden-joint guesses as direct measurements.

**LinQ gate:** once SDK/device are known, inspect chosen exported graph operator set, shapes and preprocessing/postprocessing, compile/run that exact artifact, and compare numerical keypoints and task outputs against its host reference. Separate model inference from host tracking/rule execution and obtain case acceptance for this split. No ONNX-to-LinQ assumption is supported here.

<a id="F048"></a>
### F048 — W1_M01: Unresolved questions and handoff

Provenance: [W1_M01:189](_WORK/W1_M01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Unresolved questions and handoff

1. **LinQ:** exact SDK/device/operators/shape constraints, graph partition and permitted host work remain unknown. Pose benchmark/export success elsewhere proves none of these.
2. **Target video:** no camera samples, person-pixel size distribution or target event annotations were examined here. Strong factory ranking needs that evidence. “Small/far/crowded/occluded” claims above distinguish source evidence from hypotheses.
3. **Licensing:** separate RTMPose/RTMO/ViTPose weight grants and archive notices were not conclusively inspected; component body7 dataset terms unresolved. MediaPipe old card/current bundle scope mismatch needs vendor-version documentation before operational claims. MoveNet Apache variation metadata was visible via web index while direct HTML was dynamic; archive notices not inspected.
4. **ViTPose weight:** OneDrive original share is real but binary retrieval not established; do not declare unavailable. An authorized full download/checksum and inference smoke test belong to later experiments.
5. **Temporal logic:** choose source-time sampling only after event-duration/latency experiment. Current source defaults (skip5, smoothing, async drops) are material recall risks, not safe settings endorsed for the case.
6. **Labels:** generic COCO pose data can adapt keypoint localization; it cannot validate fall onset, allowed maintenance lying, forbidden under-equipment route, harness attachment or improper carrying. Neighbor branches should supply actual video event datasets and source-disjoint splits.

Completion criterion reached: candidate artifact/config paths and their decision-relevant gaps are localized; no training/compute or unsupported LinQ claim is needed to support this research decision.

<a id="F049"></a>
### F049 — W1_M02: W1 M02 — Tracking identity, gaps and incident lifecycle

Provenance: [W1_M02:1](_WORK/W1_M02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M02 — Tracking identity, gaps and incident lifecycle

Branch question: which concrete online trackers and artifacts can support stable human/machine episodes through missed observations, occlusion and zone re-entry, without false new incidents or silently merging a different event?

Decision: retain the already proposed pinned direct ByteTrack baseline, but expose association and track state separately from emitted results, and maintain a timestamped incident ledger outside the tracker. OC-SORT is a meaningful motion-only challenger for non-linear motion; BoT-SORT-ReID is a challenger where actual target-camera appearance helps. Neither is a demonstrated industrial upgrade. DeepSORT/StrongSORT add an embedding dependency and GPL code. StrongSORT++ and published BoT-SORT post-interpolation results must be classified separately from causal live-alert results. No tracker or NN was executed here, no industrial video was scored, no training/paid compute/outreach occurred.

The sibling overview and RAW_FACTS were searched first. Prior ByteTrack dt=1, strict TTL and persistent-ledger findings are context, independently rechecked in raw code where mentioned. This branch's new contributions are OC-SORT output suppression and None semantics; BoT-SORT spatial gating of ReID; DeepSORT predicted output ambiguity; explicit offline processing; exact accessible DanceTrack annotation gaps and licenses.

<a id="F050"></a>
### F050 — W1_M02: Evidence and provenance

Provenance: [W1_M02:9](_WORK/W1_M02.md); original aliases: section record. Sources: [S045](SOURCES.md#S045), [S046](SOURCES.md#S046), [S047](SOURCES.md#S047), [S048](SOURCES.md#S048), [S049](SOURCES.md#S049), [S050](SOURCES.md#S050), [S051](SOURCES.md#S051), [S052](SOURCES.md#S052), [S053](SOURCES.md#S053), [S054](SOURCES.md#S054), [S055](SOURCES.md#S055), [S056](SOURCES.md#S056), [S057](SOURCES.md#S057), [S058](SOURCES.md#S058), [S059](SOURCES.md#S059).

## Evidence and provenance

Access date: 2026-10-23 UTC; capture completed 2026-10-23T19:20:10.755353+00:00. Access is metadata/source inspection unless explicitly marked local_test. Repo dates below are commit dates, not paper dates. All GitHub HEADs were independently resolved using GitHub commits API and raw files requested at those SHAs. Full metadata and statuses: `M02/revisions.json`, `M02/access.json`, `M02/artifacts_access.json`.

| Source ID | Primary title / author | Immutable source | Date / revision | Locator and evidence |
|---|---|---|---|---|
| [M02-S01](SOURCES.md#M02-S01) | FoundationVision/ByteTrack official repository README, code and LICENSE | https://github.com/FoundationVision/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99 | `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`, commit 2022-12-11T07:05:00Z | `M02/byte_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S02](SOURCES.md#M02-S02) | NirAharon/BoT-SORT official repository README, code and LICENSE | https://github.com/NirAharon/BoT-SORT/tree/251985436d6712aaf682aaaf5f71edb4987224bd | `251985436d6712aaf682aaaf5f71edb4987224bd`, commit 2022-10-30T15:12:42Z | `M02/bot_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S03](SOURCES.md#M02-S03) | noahcao/OC_SORT official repository README, code and LICENSE | https://github.com/noahcao/OC_SORT/tree/8462e7e729a93ccd3bd995c0a79a890336cb3a0b | `8462e7e729a93ccd3bd995c0a79a890336cb3a0b`, commit 2026-04-21T23:31:31Z | `M02/oc_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S04](SOURCES.md#M02-S04) | nwojke/deep_sort official repository README, code and LICENSE | https://github.com/nwojke/deep_sort/tree/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab | `f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab`, commit 2025-03-02T09:54:41Z | `M02/deep_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S05](SOURCES.md#M02-S05) | dyhBUPT/StrongSORT official repository README, code and LICENSE | https://github.com/dyhBUPT/StrongSORT/tree/ee995076da5083e28d0da1f885297df62705ebd7 | `ee995076da5083e28d0da1f885297df62705ebd7`, commit 2024-05-28T09:44:10Z | `M02/strong_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S06](SOURCES.md#M02-S06) | DanceTrack/DanceTrack official repository README, code and LICENSE | https://github.com/DanceTrack/DanceTrack/tree/44057dcc07e4bf6bcad2e6888c9d83ec63d4b1a3 | `44057dcc07e4bf6bcad2e6888c9d83ec63d4b1a3`, commit 2026-03-19T21:25:46Z | `M02/dance_*`; HTTP200 raw files except sports LICENSE404; `access.json` |
| [M02-S07](SOURCES.md#M02-S07) | MCG-NJU/SportsMOT official repository README, code and LICENSE | https://github.com/MCG-NJU/SportsMOT/tree/b06cfb4aacb0bb16c5778ac4ddb0d70ec6835444 | `b06cfb4aacb0bb16c5778ac4ddb0d70ec6835444`, commit 2023-07-24T02:13:51Z | `M02/sports_*`; HTTP200 raw files except sports LICENSE404; `access.json` |

Additional primary sources:

- **[M02-S08](SOURCES.md#M02-S08)** DanceTrack HF dataset, owner noahcao: https://huggingface.co/datasets/noahcao/dancetrack/tree/a0ba42ac690c41e9850a20e76a0b9450a6fb6a47 . Dataset API https://huggingface.co/api/datasets/noahcao/dancetrack and tree API https://huggingface.co/api/datasets/noahcao/dancetrack/tree/main?recursive=true&limit=100 . API GET200; `dance_info.txt`, `hf_dance.txt`. Exact archive: https://huggingface.co/datasets/noahcao/dancetrack/resolve/a0ba42ac690c41e9850a20e76a0b9450a6fb6a47/val.zip . HEAD200, application/zip, 4,209,785,614 bytes; HTTP206 byte ranges independently read ZIP directory and selected members, not archive/video download. LFS SHA256 `90ba30973761ce0b81a9654c11086d87537392475ac8bc666d842e645641277c` (metadata, not locally hashed full archive).
- **[M02-S09](SOURCES.md#M02-S09)** DanceTrack weights, owner noahcao: https://huggingface.co/noahcao/dancetrack_models . GET200 API and tree; `model_info.txt`, `hf_models.txt`. Exact repo revision recorded in model_info; direct artifact URL pattern `https://huggingface.co/noahcao/dancetrack_models/resolve/6487fc12a2fe13db44506592324cea83270f5812/bytetrack_models/bytetrack_model.pth.tar`; 792,835,731 bytes, LFS SHA256 `b8d1afba08f801f3fe2cb122faf3fc9af6c7856405a0da94cf91cdd5eb9b3321`. Metadata only; weights not downloaded, graph not inspected.
- **[M02-S10](SOURCES.md#M02-S10)** MOTChallenge MOT17 official dataset: https://motchallenge.net/data/MOT17/ , GET200 HTML saved `mot17.txt`. The old https://motchallenge.net/instructions/ returned HTTP410 here; no claim this means no current instructions exist. MOT17 is person tracking, not industrial incident GT.

<a id="F051"></a>
### F051 — W1_M02: Findings and exact implementation contracts

Provenance: [W1_M02:29](_WORK/W1_M02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Findings and exact implementation contracts

<a id="F052"></a>
### F052 — W1_M02: M02-F01 [primary_docs] ByteTrack remains detector-dependent.

Provenance: [W1_M02:31](_WORK/W1_M02.md); original aliases: M02-F01. Sources: [S045](SOURCES.md#S045).

**[M02-F01](RAW_FACTS.md#F052) [primary_docs] ByteTrack remains detector-dependent.** S01 `yolox/tracker/byte_tracker.py`, BYTETracker.update: Nx5 means xyxy,score; larger detector output multiplies objectness and class score. Coordinates are rescaled from model image to original dimensions. It associates high confidence boxes first against tracked+lost, then lower confidence against unmatched currently tracked tracks, then handles unconfirmed and new tracks. Low scores are not equivalent to safe behavior evidence. A detector yielding no box for a fully hidden person supplies no visual activity evidence. `Tracked`, `Lost`, `Removed`, plus `is_activated` differ from “incident active.” Default high/low scores and buffer are not calibrated for plant CCTV. The published MOT17 detector training uses CrowdHuman+MOT17+Cityperson+ETHZ; ablation uses CrowdHuman+half MOT17. Thus using the test-model detector on MOT17 training for one's validation leaks detector training. Different models in its zoo have different train/eval conditions.

<a id="F053"></a>
### F053 — W1_M02: M02-F02 [primary_docs, inference] ByteTrack and BoT-SORT share expiry-after-association hazard.

Provenance: [W1_M02:33](_WORK/W1_M02.md); original aliases: M02-F02. Sources: [S045](SOURCES.md#S045), [S046](SOURCES.md#S046).

**[M02-F02](RAW_FACTS.md#F053) [primary_docs, inference] ByteTrack and BoT-SORT share expiry-after-association hazard.** S01 update and S02 `tracker/bot_sort.py` lines203–218,304–342,414–426: frame_rate scales `int(frame_rate/30*track_buffer)`, but loss is counted in update steps. Lost tracks enter association before removal loop checks `frame_id-end_frame>max_time_lost`. Strict maximum identity age needs pre-association expiry using last measured source time/step. Raising buffer can reduce fragmentation but increases opportunity to merge a new similarly located person. Fixed cadence with explicit gap updates is coherent; passing source FPS while only updating sparse selected frames changes real-time TTL. Detector inference timeout, masked region, no-person result and queue drop must remain distinguishable even if all cause an empty tracker update.

<a id="F054"></a>
### F054 — W1_M02: M02-F03 [primary_docs] BoT-SORT-ReID is not arbitrary long-range re-entry matching.

Provenance: [W1_M02:35](_WORK/W1_M02.md); original aliases: M02-F03. Sources: [S046](SOURCES.md#S046).

**[M02-F03](RAW_FACTS.md#F054) [primary_docs] BoT-SORT-ReID is not arbitrary long-range re-entry matching.** S02 `tracker/bot_sort.py` lines267–275 and304–315: embeddings are extracted from current image crops only when `with_reid`; appearance distances are divided by2, thresholded, and rejected outside an IoU-distance proximity mask; final cost is minimum of geometric and surviving appearance cost. A good visual match outside the spatial gate cannot rescue that pair through the appearance term. ReID does not grant persistent human identity after exit. The second low-score pass is geometric. CMC uses current images and has implementation choices (`files`, `orb`, `ecc`, plus code-supported variants); README's original VideoStab-based GMC files can be precomputed with C++ tools. Measure the actual live CMC choice, do not inherit precomputed-file scores. Main implementation returns active activated tracks and stores tracked/lost/removed separately. Multiclass support does not mean pedestrian ReID weights generalize to forklifts or suspended loads.

<a id="F055"></a>
### F055 — W1_M02: M02-F04 [primary_docs] Original OC-SORT has a sharp None versus empty contract.

Provenance: [W1_M02:37](_WORK/W1_M02.md); original aliases: M02-F04. Sources: [S047](SOURCES.md#S047).

**[M02-F04](RAW_FACTS.md#F055) [primary_docs] Original OC-SORT has a sharp None versus empty contract.** S03 `trackers/ocsort_tracker/ocsort.py` lines197–208: documentation requires one call per frame and `np.empty((0,5))` when no detections. `None` returns an empty result before frame_count increments; it is not an empty time step. Defaults constructor lines180–194: max_age30, min_hits3, IoU .3, delta_t3, inertia .2, use_byte=False. Five-column input xyxy+score is rescaled like detector output. Main update output is Nx5 xyxy+ID, not detector score+ID/class. The public-detections update is a different API and can emit head-padding rows; do not conflate adapters.

<a id="F056"></a>
### F056 — W1_M02: M02-F05 [primary_docs, inference] OC-SORT may keep/reassociate an ID while withholding it from output after a gap.

Provenance: [W1_M02:39](_WORK/W1_M02.md); original aliases: M02-F05. Sources: [S047](SOURCES.md#S047).

**[M02-F05](RAW_FACTS.md#F056) [primary_docs, inference] OC-SORT may keep/reassociate an ID while withholding it from output after a gap.** S03 KalmanBoxTracker.predict lines144–157 resets hit_streak when `time_since_update>0`; update bbox resets time_since_update and increments hit_streak (136–140). OCSort.update lines321–328 emits only time_since_update<1 and (hit_streak>=min_hits or startup frame_count<=min_hits). One missed step followed by reacquisition after startup leads to hit_streak1,2 before3, so the old valid identity can be absent from output for the first two returning observations under min_hits3. Deletion is a different test `time_since_update>max_age`. An episode consumer equating “not emitted” with “left/clear” can split one incident even when association itself succeeded. ORU repairs filter state using a virtual trajectory when a later observation arrives; this cannot establish that unsafe action occurred during the hidden gap. The fixed F matrix and delta_t use steps, not seconds. README performance CPU700FPS excludes detector and appearance NN; no LinQ/host throughput measured here.

<a id="F057"></a>
### F057 — W1_M02: M02-F06 [primary_docs] DeepSORT's demo can emit a predicted box with no detection this step.

Provenance: [W1_M02:41](_WORK/W1_M02.md); original aliases: M02-F06. Sources: [S048](SOURCES.md#S048).

**[M02-F06](RAW_FACTS.md#F057) [primary_docs] DeepSORT's demo can emit a predicted box with no detection this step.** S04 `deep_sort/tracker.py`: defaults max_age30,n_init3; predict then update; confirmed tracks use appearance matching cascade, recent unmatched use IoU. Track.mark_missed deletes tentative immediately on miss and confirmed only after time_since_update>max_age. `deep_sort_app.py` lines182–198 emits confirmed tracks while time_since_update<=1, including one-step predictions. StrongSORT's demo lines189–204 does likewise. Therefore demo MOT result rows are not a direct list of current measured detections. An adapter must carry matched detection ID, last measured PTS and measured/predicted flags, instead of treating exported rows as fresh evidence for immobility or unsafe proximity.

<a id="F058"></a>
### F058 — W1_M02: M02-F07 [primary_docs] StrongSORT++ is retrospective and can rewrite IDs/boxes.

Provenance: [W1_M02:43](_WORK/W1_M02.md); original aliases: M02-F07. Sources: [S049](SOURCES.md#S049).

**[M02-F07](RAW_FACTS.md#F058) [primary_docs] StrongSORT++ is retrospective and can rewrite IDs/boxes.** S05 `strong_sort.py` first run() writes full sequence; optional AFLink then optional GSI read/write same output. `AFLink/AppFreeLink.py` constructor loads whole trajectory file, model.cuda(), and link() constructs global pair cost matrix, links track ends to starts with thrT=(0,30), thrS75, thrP .05, rewrites IDs and deduplicates (frame,id). `GSI.py` interpolates between known left/right observations, fits Gaussian process to whole track, and writes smoothed rows (confidence1). These rows are synthetic, not observations. Default GSI interval20,tau10 are frame-count settings. An exact current implementation needs CUDA for AFLink despite it being described as lightweight; adapting CPU is possible in principle but was not tested. StrongSORT's prepared detections+features+ECC are also a distinct input pathway from live detector+embedder+CMC.

<a id="F059"></a>
### F059 — W1_M02: M02-F08 [primary_docs] Published BoT-SORT test recipe also calls retrospective interpolation.

Provenance: [W1_M02:45](_WORK/W1_M02.md); original aliases: M02-F08. Sources: [S046](SOURCES.md#S046).

**[M02-F08](RAW_FACTS.md#F059) [primary_docs] Published BoT-SORT test recipe also calls retrospective interpolation.** S02 README tracking MOT17/MOT20 test commands call tools/interpolation.py after inference. Its dti() reads the entire sequence, fills gaps only where future endpoint exists, default CLI n_min5,n_dti20 (function default n_min25 is overridden by CLI), and overwrites unless save_path supplied. write_results_score writes score=-1 for every row, losing the measured/synthetic distinction. Do not use this output as online evidence or assume unmodified published quality is achievable before future frames arrive. Report causal raw results and delayed repaired results separately.

<a id="F060"></a>
### F060 — W1_M02: Exact real-sequence artifacts and limits

Provenance: [W1_M02:47](_WORK/W1_M02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Exact real-sequence artifacts and limits

<a id="F061"></a>
### F061 — W1_M02: M02-F09 [artifact_access_checked, local_test] Selected original DanceTrack validation annotations are actually available, not just a README schema.

Provenance: [W1_M02:49](_WORK/W1_M02.md); original aliases: M02-F09. Sources: [S052](SOURCES.md#S052), [S053](SOURCES.md#S053), [S054](SOURCES.md#S054), [S055](SOURCES.md#S055).

**[M02-F09](RAW_FACTS.md#F061) [artifact_access_checked, local_test] Selected original DanceTrack validation annotations are actually available, not just a README schema.** S08 archive remote tail bytes4209720078–4209785613 returned206. ZIP central directory bytes4206864773–4209785591 returned206 (2,920,819 bytes) and lists25 gt.txt files. Only two seqinfo.ini and two compressed gt.txt were fetched by local-header offsets. Saved `val_zip_tail.bin`, `val_zip_central.bin`, `val_zip_manifest.json`, `sample_val_dancetrack0010_*`, `sample_val_dancetrack0026_*`. Member decompression and NumPy label parsing were actually executed; no model/video test occurred.

- dancetrack0010: seqinfo says20FPS,1920x1080,1203frames; 7,029 GT rows and6 unique IDs locally counted. ID3 present at569, absent570–671, returns672:102 missing label frames (~5.1s of missing ticks). ID5 present252, returns295:42 missing (~2.1s). ID0 gap213→216:2 missing. This gives reproducible short and over-buffer same-ID returns.
- dancetrack0026:20FPS,1280x720,302frames;3,993 rows,19 IDs. Labels are highly interrupted; e.g.ID15 frame78→130 leaves51 missing. All gap locators and counts saved `annotation_gap_analysis.json`. **GT absence is not evidence of why:** without inspecting frames it may be occlusion, out-of-view or annotation policy. This branch did not visually diagnose any gap or claim a tracker failed there.
- Actual gt schema observed9 columns: frame,id,left,top,width,height,1,1,1; person ID0 is valid! Do not discard `id<=0`. No activity, unsafe-event ID, injury state, “clear”, occlusion reason, hazard ROI or physical distance labels. Last three values are constants in these files, not measured visibility confidence.

<a id="F062"></a>
### F062 — W1_M02: M02-F10 [author_claim, primary_docs] There is real-video evidence of association weakness, but no verified incident-lifecycle benchmark in these artifacts.

Provenance: [W1_M02:55](_WORK/W1_M02.md); original aliases: M02-F10. Sources: [S047](SOURCES.md#S047), [S050](SOURCES.md#S050), [S051](SOURCES.md#S051).

**[M02-F10](RAW_FACTS.md#F062) [author_claim, primary_docs] There is real-video evidence of association weakness, but no verified incident-lifecycle benchmark in these artifacts.** S06 DanceTrack authored baseline table gives ByteTrack val DetA70.5 but AssA31.5, HOTA47.1; not an incident duplicate rate. S03 OC-SORT README reports DanceTrack-test IDs1992 and Frag3838, and links rendered dancetrack0088 GIF. The GIF HTTP GET hit our8MB cap, was stopped and not saved/viewed; neither it nor BoT-SORT's MP4 demos establish a per-event failure here. Source videos have boxes/identities, not safety episodes. Thus an exact “incident wrongly ended at timestamp X by model Y” remains unknown until an event ledger is run and annotated. Do not disguise tracking fragmentation metrics as that test. The recovered GT long-gap sequences are concrete candidate tests with exact labels, not claimed executions.

SportsMOT S07 is a supplementary rapid-motion/moving-camera hard-negative source, not selected for deployment: 240 clips,25FPS official recordings, no shot change; players only, excluding referees/coaches/spectators. README's average clip485-frame prose conflicts with basketball table845.4; preserve seqinfo as runtime truth. GT uses MOT columns and example ID0. Test GT unavailable via README, distribution requires competition access. Non-commercial and no-redistribution conditions matter; no archive/video downloaded.

<a id="F063"></a>
### F063 — W1_M02: Episode contract and tests to run next (proposed)

Provenance: [W1_M02:59](_WORK/W1_M02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Episode contract and tests to run next (proposed)

<a id="F064"></a>
### F064 — W1_M02: M02-F11 [inference] Required separation:

Provenance: [W1_M02:61](_WORK/W1_M02.md); original aliases: M02-F11. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M02-F11](RAW_FACTS.md#F064) [inference] Required separation:** physical identity is not guaranteed by tracker ID; `track_uid=(camera,stream_epoch,tracker_instance,local_id)` prevents accidental reuse across resets. Use a separate stable episode_uid and an auditable possible-continuation relation. A track miss transitions evidence to unknown, not automatically safe/clear. Do not extend measured immobility time with predictions. Masked person boxes/hidden feet must retain evidence quality flags. Class-specific trackers prevent person/machine cross-association, but machine motion/proximity still needs appropriate detections and ground calibration.

Allow short-gap continuation only under a documented temporal/spatial/appearance policy; record uncertainty. Ambiguous reappearance by two similar uniformed people must not automatically inherit the old unsafe event. A confirmed visible exit can close zone occupancy; a frame edge miss/occlusion cannot establish exit. If a person leaves and later re-enters, whether it is one persistent hazard or new episode depends on explicit scenario/ROI policy and evidence of clearance. A persistent fall/lying hazard may remain unresolved even while person identity is lost; smoking/phone episodes require current localized evidence. Permanent ID blacklists suppress genuinely repeated incidents. Global camera cooldown merges different workers. Neither is acceptable general deduplication.

Minimal deterministic test proposal (not executed): feed fixed original-coordinate boxes at ordered ticks with a unique detection ID, no ML inference, after initial warmup. (1) OC-SORT20 observed ticks,1 empty,3 identical boxes: assert same internal ID and emitted-return pattern absent,absent,present for min_hits3; compare one None gap to show no age advancement. (2) DeepSORT confirmed track,empty update: assert its demo emits time_since_update1 but measurement flag false; next miss hidden while track still confirmed. (3) ByteTrack/BoT-SORT N+1 empty returns: compare stock association with pre-expiry adapter, assert no over-TTL ID resurrection. (4) two identical-looking tracks cross then one returns in old box: evaluate false merge/episode transfer. (5) stream restart with localID reuse: assert unique epoch and no automatic old episode closure. (6) repeated all-empty/timeout/masked steps: ledger remains unknown and emits no repeated alert. Instrument internal track state, matched_det_id, last-measured tick and emitted rows separately.

Real-sequence next test: use dancetrack0010 GT identity gaps above with actual frames, same detector outputs across ByteTrack,OC-SORT,BoT-SORT, and manually label gap causes. Native20Hz plus deterministic10/5/2Hz thinning, controlled detector misses and ROI masking; compare fixed-time buffers, not identical frame counts. Score ID switches, fragmentation, re-association precision, duplicate event starts, wrong old-event continuations, time to resume measured evidence, and unresolved-gap rate. Safety-event GT must be added; assigning “hazard=true” mechanically to an identity is only an association stress fixture. Evaluate raw causal output before optional interpolation, and prohibit future frames in live scoring.

<a id="F065"></a>
### F065 — W1_M02: Licenses, overlap, unanswered items

Provenance: [W1_M02:69](_WORK/W1_M02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Licenses, overlap, unanswered items

<a id="F066"></a>
### F066 — W1_M02: M02-F12 [primary_docs, unknown] Code, data and weight permissions are separate.

Provenance: [W1_M02:71](_WORK/W1_M02.md); original aliases: M02-F12. Sources: [S045](SOURCES.md#S045), [S046](SOURCES.md#S046), [S047](SOURCES.md#S047), [S048](SOURCES.md#S048), [S049](SOURCES.md#S049).

**[M02-F12](RAW_FACTS.md#F066) [primary_docs, unknown] Code, data and weight permissions are separate.** S01 ByteTrack MIT; S02 BoT-SORT MIT; S03 OC-SORT MIT, with upstream YOLOX Apache2 and other third-party terms; S04 DeepSORT GPLv3; S05 StrongSORT GPLv3. These are inspected LICENSE files, not legal advice or inferred weight grants. BoT-SORT FastReID dependency has separate upstream terms. DanceTrack code MIT, annotations CC-BY4, dataset available only non-commercial research, underlying Internet videos not owned by authors; dataset README expressly states these distinct conditions. SportsMOT README CC-BY-NC4 plus no redistribution without permission. DeepSORT/StrongSORT prepared embeddings, detector outputs and checkpoints and BoT-SORT ReID checkpoints have no separately verified explicit commercial weight grant in the material inspected. A public download page is not such a grant.

<a id="F067"></a>
### F067 — W1_M02: M02-F13 [artifact_found, artifact_access_checked] Weight/data paths:

Provenance: [W1_M02:73](_WORK/W1_M02.md); original aliases: M02-F13. Sources: [S060](SOURCES.md#S060), [S061](SOURCES.md#S061), [S062](SOURCES.md#S062), [S063](SOURCES.md#S063), [S064](SOURCES.md#S064), [S065](SOURCES.md#S065), [S066](SOURCES.md#S066).

**[M02-F13](RAW_FACTS.md#F067) [artifact_found, artifact_access_checked] Weight/data paths:**

- BoT-SORT MOT17 SBS-S50 https://drive.google.com/file/d/1QZFWpoa80rqo7O-HXmlss8J8CnS7IUsN/view ; MOT20 https://drive.google.com/file/d/1KqPQyj6MFyftliBHEIER7m_OrGpcrJwi/view . MOT17 landing GET200 HTML only, not checkpoint byte validation; MOT20 is README artifact_found, not separately checked. FastReID config MOT17 sbs_S50.yml read; detector weights inherited from ByteTrack, ReID trained from MOT train crops.
- StrongSORT prepared data https://drive.google.com/drive/folders/1Zk6TaSJPbpnqbz1w4kfhkKFCEzQbjfp_ GET200 boundedHTML; includes README-declared AFLink_epoch20.pth, YOLOX+BoT/SimpleCNN Nx arrays, ECCJSON, GT and result files. Exact checkpoint byte/download/license not checked. Baidu mirror https://pan.baidu.com/s/1EtBbo-12xhjsqW5x-dYX8A?pwd=sort not accessed.
- DeepSORT resources https://drive.google.com/open?id=18fKzfqnqhqW3s9zwsCbnVJ5XF2JFeqMp GET200 redirects to folderHTML only; expected mars-small128.pb (TensorFlow1.5 graph) and detections. Nx138 schema documented:10 MOT input columns+128 embedding. Alternate precomputed detections https://drive.google.com/open?id=1VVqtL0klSUvLnmBKS89il1EKC3IxUBVK found only, not checked.
- OC-SORT YOLOX pretrained folder https://drive.google.com/drive/folders/1LnhZVJlpufUnWuObZASIN1KwfhuvT_a8?usp=sharing found in pinned MODEL_ZOO; not accessed. It inherits detector weights rather than requiring a tracker neural checkpoint. StrongSORT AFLink is a separate learned model.
- HF DanceTrack exact validation archive and detector weight metadata above are checked; training archives train1.zip3,606,300,312 B and train2.zip3,299,320,948 B, test1.zip3,677,760,950 B and test2.zip2,882,754,122 B are API metadata only, no payload download.

Known overlap/leakage: using a MOT17 full-train detector or ReID to “validate” on MOT17 second half without verifying its training split contaminates evaluation. StrongSORT prepared val features may contain a detector trained elsewhere; do not assume clean split merely because filename says val. DanceTrack val and test checkpoints may differ; current HF model card is minimal and does not establish which checkpoint produced which published row. Trackers often share YOLOX/ByteTrack detections; their results are not independent model votes. Deterministic thinning of a held-out sequence remains the same underlying clip and must not straddle train/test.

Unresolved: target camera cadence/occlusion distributions; exact emitted-versus-internal-state adapters on chosen SDK; reliable identity after full occlusion or leaving view; machine-specific embeddings; target commercial rights for external videos/weights; actual CPU embedding/CMC latency and LinQ artifact compatibility. No numerical SLA or device quality is inferred from original papers. Own industrial clips with event IDs, gap causes and clear/unknown labels remain necessary.

Evidence boundary: local_test labels in F09 concern only ZIP member extraction and numerical annotation parsing, never tracker inference. Source commits and UTC source access status are captured; the attempted demo GIF read was capped and no video visual claim is made.

<a id="F068"></a>
### F068 — W1_M03: W1 M03 — Fall, lying, immobility: artifact and label audit

Provenance: [W1_M03:1](_WORK/W1_M03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M03 — Fall, lying, immobility: artifact and label audit

Research access date: 2026-10-23, approximately 19:05–19:25 UTC. Evidence directory: `_WORK/W1_M03_EVIDENCE/`. No training, model execution, paid compute, outreach or subagents. Python CSV parsing and static binary metadata inspection were executed; these are not inference. Context-prompt read; current case interpreted through root's `_WORK/CASE_NOTES.md`. Prior feasibility report used as a lead only.

<a id="F069"></a>
### F069 — W1_M03: Branch question and decision

Provenance: [W1_M03:5](_WORK/W1_M03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

Can a reproducible video→model→fall/lying/immobility event chain be assembled quickly, including real weights, temporal labels and hard negatives?

**[inference] Decision:** retain pose+tracking+causal host state machine as the short MVP reference. Real small temporal checkpoints exist and one complete PT/ONNX pair is preserved here. Their training/evaluation chains have label and split weaknesses, so published window accuracy cannot justify industrial event accuracy. The highest-value new evidence is author-linked **OmniFall**, which supplies dense fall/fallen/intentional-lying labels and grouped splits rather than just another video-level fall corpus.

Separate `fall_suspected` (observed transition), `lying_observed` (posture), and `post_fall_low_motion` (transition plus continuously observed low movement for N seconds). `fallen` is not synonymous with stationary. None diagnoses unconsciousness. Existing lying at stream start must not become a retrospectively inferred fall.

<a id="F070"></a>
### F070 — W1_M03: M03-F01 — OmniFall provides the needed semantics, not inactivity ground truth

Provenance: [W1_M03:28](_WORK/W1_M03.md); original aliases: M03-F01. Sources: [S069](SOURCES.md#S069), [S070](SOURCES.md#S070).

## [M03-F01](RAW_FACTS.md#F070) — OmniFall provides the needed semantics, not inactivity ground truth

**[primary_docs]** `LABELS.md`: core IDs include fall1, fallen2, lie_down5, lying6, stand_up7. Staged sources use0–9; synthetic/wild add kneeling/squatting/crawling/jumping through15. Boundaries distinguish motion transitions from static states. Fallen may still include ground-level movement after inertia settles; thus fallen2 is not low-motion-for-N truth. Walking0 also includes running/jogging, making this unsuitable as clean walk-versus-run labels.

**[artifact_access_checked]** Exact annotations, all under [M03-S02](SOURCES.md#M03-S02) file base:

- `labels/GMDCSA24.csv` GET200,19,737B.
- `labels/caucafall.csv` GET200,11,425B.
- `labels/label2id.csv` GET200,172B.
- `splits/cs/gmdcsa24/train.csv`, `val.csv`, `test.csv`: GET200,1,317/846/651B.

**[primary_docs]** Schema: `path,label,start,end,subject,cam,dataset`; start/end seconds; extensionless source-relative path. Identity is **(dataset,path)**, not path alone. Prepared file is `{root}/{dataset}/video/{path}.mp4`. GMD original directories have spaces (`Subject 1`), prepared keys underscores (`Subject_1`). Do not literally join original directories to prepared keys.

<a id="F071"></a>
### F071 — W1_M03: M03-F02 — exact controls and a previously hidden train/test limitation

Provenance: [W1_M03:41](_WORK/W1_M03.md); original aliases: M03-F02. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M03-F02](RAW_FACTS.md#F071) — exact controls and a previously hidden train/test limitation

**[local_test: CSV parsing only]** `GMD_ANNOTATION_AUDIT.json` computed from pinned CSVs:458 segments,160 unique videos. CS train75 videos subjects1,3; validation48 subject2; test37 subject4. Pairwise video-path intersections zero. This checks one source split, not every multi-view dataset or unseen industrial conditions.

| Source clip → prepared key | Exact action intervals in seconds | Consequence |
|---|---|---|
| `Subject 1/Fall/11.mp4` → `Subject_1/Fall/11` | standing0–0.52; fall0.52–2.7; fallen2.7–6.08 | CS **train**, not independent test. |
| `Subject 3/Fall/07.mp4` → `Subject_3/Fall/07` | standing0–1; fall1–3.86181; fallen3.862–9.02597 | CS **train**. Fallen interval≈5.164s is not prior low-motion interval. |
| `Subject 3/ADL/08.mp4` → `Subject_3/ADL/08` | intentional lie_down0–3.71597; lying3.716–4.896 | Reproducible intentional-lying negative, CS **train**. |
| `Subject_1/ADL/04` | lying0–1.14; stand_up1.14–3.58; sitting3.58–5.84 | Already lying at start; no observed fall history. |

Every row above has dataset=`GMDCSA24`. **[inference]** New temporal annotations must not silently overwrite previous manually reviewed visibility/low-motion annotations. Semantics differ; prepared encoding/timing may differ. Match actual PTS/duration/conversion before moving these seconds to original bytes. No video was decoded in this branch. Repeatedly inspected old clips are development evidence; fresh subject4 and target-camera holdouts remain necessary.

<a id="F072"></a>
### F072 — W1_M03: M03-F03 — sync/EOF, access and rights conditions

Provenance: [W1_M03:54](_WORK/W1_M03.md); original aliases: M03-F03. Sources: [S078](SOURCES.md#S078), [S079](SOURCES.md#S079), [S080](SOURCES.md#S080).

## [M03-F03](RAW_FACTS.md#F072) — sync/EOF, access and rights conditions

**[primary_docs]** `KNOWN_PITFALLS.md` reports segment ends beyond actual video EOF after multi-camera label propagation: MCFD85/1,352 segments,71/192 videos,max1.19s; EDF18/508,5/10,max7.36s; CMDFall76/42,143,75/384,max3.80s. Do not interpret padded/repeated EOF frames as observed low motion. `STRUCTURE.md` says CMDFall pre-cut clips duplicate continuous recordings; treating them as another split leaks footage and exposes target boundaries.

**[primary_docs]** HF README frontmatter says **cc-by-nc-4.0**, narrative assigns annotations/splits **CC BY-NC-SA4.0**. Package source explicitly records conflict. Preserve both statements; underlying video rights remain separate. Primary is author-linked simplexsigil2, not duplicate Zc129.

**[artifact_access_checked]** Exact synthetic archive URL: https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/83572a37b9e3081df8c06a56874b1d1f2a19386c/data_files/omnifall-synthetic_av1.tar . Range GET206 `bytes0-31/9716480000`,32B inspected. No archive/video downloaded or decoded. Author describes5s clips; these cannot establish10/30s inactivity.

**[primary_docs; original grant not independently verified]** Package source identifies Le2i original DOI10.25666/DATAUBFC-2024-04-09, CC BY-NC-SA3.0, original page https://search-data.ubfc.fr/imvia/FR-13002091000019-2024-04-09_Fall-Detection-Dataset.html and archive https://search-data.ubfc.fr/imvia/dl_data.php?file=101 . **Our Range GET returned503**, original landing page also503. Package's prior303/206 access and9,608,701,260B assertion are its documentation, not this branch's successful access. No inference of artifact absence. OOPS third-party footage research terms are not cleared by unified labels. Package code LICENSE Apache2.0 applies to code, not all source videos.

<a id="F073"></a>
### F073 — W1_M03: M03-F04 — real small temporal weights and an incomplete-looking ONNX that needs external data

Provenance: [W1_M03:64](_WORK/W1_M03.md); original aliases: M03-F04. Sources: [S081](SOURCES.md#S081).

## [M03-F04](RAW_FACTS.md#F073) — real small temporal weights and an incomplete-looking ONNX that needs external data

**[artifact_access_checked]** Exact base https://raw.githubusercontent.com/udayraj28/fall-detection-vision/e1c36afa34a966cae087543c01f01646b61141d6/ :

| File appended to base | Access, complete bytes | SHA256 |
|---|---|---|
| `models/checkpoints/best.pth` | GET200,810,808B, saved | `96918521abd9d2f29693887bcd673ea62ad8e293574b8639c7109b9abf71edc1` |
| `models/exports/fall_detector.onnx` | GET200,8,228B, saved | `580a1f7e40593013dbca52566d8d72f9fe849d8a6e8a1512c79ed85df9f1b716` |
| `models/exports/fall_detector.onnx.data` | GET200,807,424B, saved | `6b7ab751f5f4ab738ead96bb1ab1c11b936b34e41dda0a36ebabadd3bd86b412` |

**[primary_docs/artifact_found]** README says checkpoints are untracked and need training/separate acquisition. Actual pinned tree and full GET contradict this. Tree also lists `last.pth` and `yolo11n-pose.onnx`; those not validated here.

**[local_test: static metadata, not inference]** Safe zip/pickletools inspection without unpickling, and minimal ONNX protobuf field parsing, saved `PT_STATIC_STRINGS.json`/`ONNX_STATIC_METADATA.json`. Graph IR10/opset17; FLOAT `input[batch_size,30,5]` → FLOAT `output[1,3]`. Exporter requests dynamic output batch but saved metadata gives1. Graph includes2 LSTM, LayerNormalization,Gemm, shape/slice/transpose ops. External tensor locations explicitly require `fall_detector.onnx.data`:8KB ONNX alone is incomplete. No checker/ORT/PT parity/LinQ execution; torch/onnx not installed.

**[primary_docs]** `models/fall_detector.py`: two-layer unidirectional LSTM128, dropout0.3, LayerNorm, last timestep→3 logits,0normal/1falling/2fallen. `src/feature_extraction.py`: five per-frame features = hip→nose angle normalized, CoG y/frameheight, successive CoG delta, bbox width/height, mean COCO17 confidence. Input is not raw RGB or raw skeleton. Thirtyframes equal1s only at30fps. Delta is per frame rather than per second, so reduced inference cadence changes temporal meaning. Overhead/camera-axis falls and occluded nose/hips stress these inputs.

<a id="F074"></a>
### F074 — W1_M03: M03-F05 — concrete label and evaluation counterevidence for that checkpoint

Provenance: [W1_M03:80](_WORK/W1_M03.md); original aliases: M03-F05. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M03-F05](RAW_FACTS.md#F074) — concrete label and evaluation counterevidence for that checkpoint

**[primary_docs]** `src/dataset_processor.py` creates30-frame windows stride15; `split_data` lines468–505 randomly stratifies already-created X/y with no source/subject grouping. **[inference]** Overlapping windows may cross partitions and inflate validation; actual historical overlapping assignments cannot be counted without saved sample/source identities.

**[primary_docs]** `assign_labels` lines156–216 labels all windows falling when no fall boundary. With boundaries it requires>50% window overlap, then assigns first40% of fall interval falling and remainder fallen. This is a heuristic subdivision, not independently labeled post-fall state. UR parser identifies filename prefixes without fall timing. Le2i parser defaults absent annotations to ADL. Missing detections are removed into feature lists before windows; labels then use ordinal i×stride without original frame IDs. Gaps/multiple tracks can misalign temporal labels.

**[author_claim]** README lists UR70,Le2i140,3,000 synthetic feature sequences,17,502 total windows; claims98.2% accuracy/97.8% macroF1. Pinned `models/checkpoints/training_report.json` instead gives97.03%/96.42%,38epochs,best epoch23. PT pickle opcode stream has epoch69. No matched run/checkpoint/split manifest found; these numbers cannot be asserted for this checkpoint or industrial event inference.

**[unknown]** No root LICENSE or weight-specific grant found in checked tree. Public download is not a deployment grant; this is unresolved permission, not proof no grant exists. Backbone Ultralytics rights are separate. Keep this artifact for structural research, not a cleared deployment recommendation.

<a id="F075"></a>
### F075 — W1_M03: M03-F06 — second real skeleton artifact, with code/prose and split contradictions

Provenance: [W1_M03:90](_WORK/W1_M03.md); original aliases: M03-F06. Sources: [S082](SOURCES.md#S082).

## [M03-F06](RAW_FACTS.md#F075) — second real skeleton artifact, with code/prose and split contradictions

**[artifact_access_checked]** Exact base https://raw.githubusercontent.com/Rchit13/multi-model-fall-detection-system/47b54390988b9aa7e67353b7072be4d735245ac9/ . `models/standing_fall_model.h5`: GET200,4,018,632B,HDF5 signature; bytes inspected but not saved. `models/bed_fall_model.h5` and `models/chair_fall_model.h5`: Range206 first32B,total4,018,632B each. Tree includes bed/chair/standing scalers1,026B and posture scaler930B. Scalers not unpickled.

**[primary_docs]** README calls heads BiLSTM,60frames,24keypoints,focal loss. Actual `src/train_fall_models.py` sets30frames,12joints=24XY coordinates, plain LSTM128→LSTM64(no Bidirectional), binary crossentropy. StandardScaler is fitted on all X before80/20 test split(lines126–139): test-distribution preprocessing leakage. Sample split has no subject grouping shown. Label is filename prefix `f_`, not event timing. Actual HDF5 architecture/scaler metadata must be inspected before inference; README is insufficient.

**[primary_docs/unknown]** Root code LICENSE MIT,copyright2025Rchit13; README says pretrained components inference-only. Preserve this weight restriction/ambiguity separately from MIT code grant. Training-video rights not established. This is an actual artifact reserve, not a currently proven industrial baseline.

<a id="F076"></a>
### F076 — W1_M03: M03-F07 — RGB action and temporal localization remain different evaluation problems

Provenance: [W1_M03:98](_WORK/W1_M03.md); original aliases: M03-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M03-F07](RAW_FACTS.md#F076) — RGB action and temporal localization remain different evaluation problems

**[primary_docs]** OmniFall experiment code uses pre-extracted I3D/DINOv2/InternVideo2/VideoMAE features with segment classifier. Checked releases API empty; author HF model list empty; README points to supplement for feature links. This localizes an unresolved checkpoint path, not proof all checkpoints absent. `data/feature_dataset.py:get_features_for_segment` uses annotated segment bounds and can center with surrounding context. Package `_video_dataset.py` defaults uniform sampling over entire labeled segment. Such classification knows endpoints unavailable online. Continuous timeline localization and causal alarm latency require another evaluation path.

**[inference]** A general HMDB `fall_floor` RGB/PoseC3D classifier is an offline reserve; clip top1 does not prove onset,post-fall inactivity or maintenance negatives. Require exact checkpoint/preprocessing/causal window/device operators/parity before proposing temporal NN on LinQ. A host temporal head does not alone prove required LinQ neural execution.

<a id="F077"></a>
### F077 — W1_M03: Matched MVP protocol and hard negatives

Provenance: [W1_M03:104](_WORK/W1_M03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Matched MVP protocol and hard negatives

**[inference] Baseline A:** accepted LinQ pose frontend→person tracks with capture PTS→causal history→upright-to-low transition evidence→low posture→optional low-motion holdN. Confidence, body visibility and time gaps are part of eligibility. Camera cut, lost identity, occlusion or poor pose must produce UNKNOWN; no-detection must not accumulate inactivity. Already lying at start may emit lying-only observation.

**[inference] Baseline B:** same pose/track data plus small pinned30×5 LSTM after rights clarification and exact feature/cadence matching. Compare event false alarms/recall/gap sensitivity to A on fresh grouped data. Do not silently reframe30frames as1s at another cadence.

Target annotation fields: original hash,camera,track,valid-observation intervals,transition onset/end,low-posture interval,low-motion interval,recovery,censoring and reason,intentional maintenance/rest policy. Keep action labels separate from site-specific violations.

Hard negatives needed: intentional supported lying then still; supine/prone maintenance; rest; sitting/squatting/kneeling; bend/pick object; crawl; lying→sitting recovery; exercise; overhead/camera-axis views; cropped/occluded torso/legs; crossing tracks; carried person; camera vibration/cuts. These are proposed target controls, not claims all were visually checked. Exact ready annotation controls include GMDCSA `Subject_3/ADL/08`, CAUCA `adl/PickupobjectS1`, `adl/KneelS1`; CAUCA source video retrieval/decode remains undone.

Split by subject/recording/session and synchronized-view family **before** windows. Keep old inspected clips in dev. Report event-level recall by mechanism/view,false alarms per camera-hour,one-to-one event matching,latency from transition and separately from N-satisfied time,recovery/rearm,UNKNOWN coverage,misses under cadence reduction. Frame/clip accuracy is secondary. N10/N30 needs truly observed long holds and controls; EOF is censoring. Accuracy priority cannot justify sparse temporal sampling that misses the transition.

<a id="F078"></a>
### F078 — W1_M03: Unresolved and handoff

Provenance: [W1_M03:116](_WORK/W1_M03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Unresolved and handoff

1. LinQ pose/output/runtime grant,operators,shape restrictions,parity and performance unknown; no deployed claim.
2. Clarify udayraj weight grant,Rchit inference-only terms,and OmniFall annotation license discrepancy. No outreach sent.
3. Match original↔prepared video PTS before applying OmniFall seconds; obtain fresh subject4 and industrial holdouts.
4. Need matched checkpoint/run manifest and causal continuous benchmark. Actual artifact availability is established; quality is not.
5. W2 can independently inspect device/ONNX parity or video mapping if critic prioritizes it; no need to repeat old shallow dataset overview.

Evidence saved before handoff: pinned trees/commits,primary docs,small PT+complete ONNX pair,CSV split audit,static graph/pickle strings,and bounded access checks. The useful new contribution is a real temporal-artifact chain plus exact counterevidence limiting its claims, and OmniFall action/split linkage to previously reviewed clips.

<a id="F079"></a>
### F079 — W1_M04: W1 M04 — Бег, ходьба, резкое перемещение: проверка классов, весов и временных данных

Provenance: [W1_M04:1](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M04 — Бег, ходьба, резкое перемещение: проверка классов, весов и временных данных

Исследовательская ветка M04. Дата доступа: 23.10.2026, основные HTTP-проверки 19:29–19:34 UTC (22:29–22:34 MSK). Результат относится к исследованию, не к выполненному инференсу. Читал полный `_WORK/PROMPT_W1_M04.md`, `Context-prompt.md`, исходные CASE_NOTES и выборочно предыдущий итог feasibility, M03/M08. Их результаты использованы как указатели; нижеследующие новые артефакты проверены напрямую. Больших архивов/весов не скачивал, моделей не запускал, обучения/аренды/внешней переписки не было. Получены пять небольших видео суммарно 19.96 MB для проверки связки видео↔разметка. LinQ SDK, устройство, операторы и допустимый split с CPU остаются неизвестными.

<a id="F080"></a>
### F080 — W1_M04: Вопрос ветки и решение

Provenance: [W1_M04:5](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Вопрос ветки и решение

**Можно ли предъявить готовую модель и независимое видео, которые различают gait-run и walk, вместо подмены бега высокой скоростью bbox?** Да, есть точный RGB HMDB51 checkpoint с отдельными run/walk и реальные CCTV CAVIAR с покадровым movement running/walking, включая переходы одного ID. Но это **резервный проверочный путь**, не доказанная промышленная функция: веса обучены на HMDB, тестовый рецепт многовидовой, в целевом цехе не проверены, компиляция LinQ не установлена. Для прототипа оставлять две явно различные величины: перевод точки опоры по времени и уверенность в типе походки. Резкое ускорение — ещё одна метка/событие; ни run-logit, ни средняя скорость сами её не задают.

Критическое новое ограничение данных: современные определения MEVA **исключают** Walking и Running из аннотируемых state activities. Наличие огромного CCTV-корпуса и дорожек MEVID не даёт готовой истины walk/run. У Kinetics400 есть jogging, но нет общей пары walk/run: walking the dog, running on treadmill и riding or walking with horse — другие семантические классы.

<a id="F081"></a>
### F081 — W1_M04: Установленные факты и действия

Provenance: [W1_M04:11](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Установленные факты и действия

<a id="F082"></a>
### F082 — W1_M04: M04-F01 [artifact_access_checked; primary_docs] Готовый RGB checkpoint с отдельными классами.

Provenance: [W1_M04:13](_WORK/W1_M04.md); original aliases: M04-F01. Sources: [S083](SOURCES.md#S083), [S084](SOURCES.md#S084), [S085](SOURCES.md#S085), [S086](SOURCES.md#S086), [S087](SOURCES.md#S087), [S088](SOURCES.md#S088), [S089](SOURCES.md#S089).

**[M04-F01](RAW_FACTS.md#F082) [artifact_access_checked; primary_docs] Готовый RGB checkpoint с отдельными классами.** MMAction2 **v0.24.1**, `slowonly_k400_pretrained_r50_8x4x1_40e_hmdb51_rgb`: exact weights [[M04-S03](SOURCES.md#M04-S03)] HEAD 200, 127,223,551 bytes; целиком не загружены, SHA256 и исполнимость неизвестны. Именованный train/eval config, parent и base model сохранены [S02/S04]. Это `Recognizer3D` / `ResNet3dSlowOnly`, ResNet50, I3DHead 2048→51; base задаёт probability-average по клипам. HMDB label_map непосредственно прочитан: zero-based **run=32, walk=49**, stand=42, jump=19, turn=48; карта v1.2.0 совпала с v0.24.1 по SHA256. Не следует извлекать колонку 32 из другой, сокращённой карты классов.

Train: 8 кадров с `frame_interval=4`, один клип; RGB rawframes; short side 256, RandomResizedCrop, resize224, flip0.5. Mean `[123.675,116.28,103.53]`, std `[58.395,57.12,57.375]`, `to_bgr=False`, NCTHW. Val: один клип, CenterCrop224. **Test: 10 temporal clips × ThreeCrop256**, то есть 30 views. Опубликовано **65.95 top1 / 91.05 top5** по всем 51 классам [S01], не run/walk precision, не event recall, не результат одиночного causal crop. Конфиг `split=1`; train/test annotations берутся из одноимённых HMDB split1 rawframe lists. `load_from` родителя — K400 checkpoint для инициализации, не ссылка на финальные HMDB веса. Именно HMDB checkpoint в S03 нужен для 51-class выхода.

При 25fps восемь кадров interval4 занимают **28/25=1.12s** между первым и последним; номинальная область sampler 32/25=1.28s. При 1fps с тем же interval4 это уже 28s, а не прежний клип. При interval1 на 1fps получается 7s, также другой вход. При frame duplication нельзя восстановить утраченную фазу походки. Подать только person crop вместо полного rawframe — разумная исследовательская адаптация, но меняет обучающий input distribution и нуждается в отдельном тесте. У классификатора нет actor ownership или bbox proposals: при двух людях он не сообщает, кто бежит.

<a id="F083"></a>
### F083 — W1_M04: M04-F02 [local_test: annotation parsing; artifact_access_checked] CAVIAR даёт настоящую временную пару и переходы одного ID.

Provenance: [W1_M04:19](_WORK/W1_M04.md); original aliases: M04-F02. Sources: [S091](SOURCES.md#S091), [S092](SOURCES.md#S092), [S093](SOURCES.md#S093), [S094](SOURCES.md#S094).

**[M04-F02](RAW_FACTS.md#F083) [local_test: annotation parsing; artifact_access_checked] CAVIAR даёт настоящую временную пару и переходы одного ID.** GET200 получены XML `Fight_RunAway1/fra1gt.xml` и `Walk1/wk1gt.xml` [S06/S07], разобраны ElementTree. В run-файле 551 `<frame>`, 169 actor-frame labels running, 749 walking, 98 active, 93 inactive. Это количества actor-frame annotations, не эпизодов/уникальных людей. Есть **два** continuous run-interval:

| XML actor | До | Running, inclusive XML frame numbers | После |
|---|---|---|---|
| 7 | walking149–372 | **373–436**, 64 frames | walking437–550 |
| 6 | walking174–384 | **385–489**, 105 frames | последующие метки этого ID в разобранном файле не найдены |

Это полезнее склейки walk+run: настоящий непрерывный файл, один actor ID проходит смену состояния. Но конфликт/побег в публичном холле не воспроизводит промышленную срочную ходьбу или PPE. ID7 имеет также head/shoulder/feet annotations с `occluded` и confidence/evaluation; не все акторы/файлы имеют эти дополнительные точки. XML содержит `object id`, `box h,w,xc,yc`, `orientation`, `appearance`, `hypothesis/movement`, `role`, `context`, `situation`. **Нужное поле — movement.** Например frame0 actor7 имеет movement=walking, role=walker, context=immobile: context не заменяет движение. `active` не равно running. Отсутствующий объект не доказывает неподвижность.

В Walk1 611 XML frames: walking668 / active345 / inactive546 actor-frames, **нет running**. Это отрицательный run-контроль с нормальными движущимися людьми и активными состояниями. Не считать весь кадр отрицательным для других сценариев; `active` и background не размечены как универсальная безопасность. В официальном описании неподвижные на протяжении записи люди могут вообще не иметь bbox.

<a id="F084"></a>
### F084 — W1_M04: M04-F03 [local_test: full decode + limited visual inspection] Реальные небольшие видео доступны, но XML↔декодер требует сверки.

Provenance: [W1_M04:30](_WORK/W1_M04.md); original aliases: M04-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M04-F03](RAW_FACTS.md#F084) [local_test: full decode + limited visual inspection] Реальные небольшие видео доступны, но XML↔декодер требует сверки.** Пять файлов полностью скачаны с bounded requests и последовательно декодированы PyAV. OpenCV в среде отсутствует: первая попытка не выполнилась, затем использован доступный PyAV. Никакого model inference эти операции не включают. Контакт-лист `_WORK/M04/contact.jpg` просмотрен: KTH показывает того же видимого исполнителя в сходном фоне/одежде; CAVIAR — наклонная CCTV публичного холла, два бегущих после сближения, обычные пешеходы и окклюзии/небольшие дальние фигуры.

| Файл | HTTP / bytes | Декодировано | Размер / encoded average rate | SHA256 |
|---|---|---|---|---|
| KTH person15_walking_d1_uncomp.avi | GET200 /3,158,016 |741 |160×120 /25fps |`2e562f335121fbe143f31c8d51e2d8c1b95f143984c65e5e42219a5778d0a13c`|
| KTH person15_jogging_d1_uncomp.avi | GET200 /1,757,184 |420 |160×120 /25fps |`e1a4ce01fe97aa96bb8acaaaeadd769d943766cc9a9622c56db985240d886c89`|
| KTH person15_running_d1_uncomp.avi | GET200 /1,333,248 |325 |160×120 /25fps |`e91e2b9c0aded1a12009b32b7b4141437565d8d9b9a534ba31b5a33ce858b471`|
| CAVIAR Walk1.mpg | GET200 /7,208,095 |612 |384×288 /25fps |`a5d6dc7d7def01c1bdaeea8ff620195c148b366e1a52589bf4e46f15b6daa0c2`|
| CAVIAR Fight_RunAway1.mpg | GET200 /6,500,613 |552 |384×288 /25fps |`b1eb7821318a2443445ee0c6dd6edb4dd9ebe06c110b52dce9252b9117931a55`|

CAVIAR decode count на **один больше**, чем XML, у обоих файлов. Первые decoded timestamps необычны: Walk1 `[0,279.711,319.711,359.700]ms`; RunAway1 `[0,279.711,279.711,279.711]ms`. Это результат данного decoder/API; **причина и точное смещение не установлены**. Нельзя уже заявить, что XML373 соответствует PTS14.92s или decoded frame373. Для теста сначала сопоставить rendered annotation с изображением вокруг нескольких опорных кадров и переходов и сохранить mapping. Основная страница отдельно предупреждает о duplicated/missing frames **в Lisbon subset** и смещении старта синхронных ракурсов; это не объяснение автоматически для полученных INRIA файлов. Файлы доступны, содержимое реально декодировано; end-to-end проверка annotation alignment ещё не выполнена.

<a id="F085"></a>
### F085 — W1_M04: M04-F04 [primary_docs; local_test: video decode] KTH полезен для простого gait sanity-check, а не CCTV acceptance.

Provenance: [W1_M04:42](_WORK/W1_M04.md); original aliases: M04-F04. Sources: [S095](SOURCES.md#S095), [S096](SOURCES.md#S096), [S097](SOURCES.md#S097), [S098](SOURCES.md#S098), [S099](SOURCES.md#S099).

**[M04-F04](RAW_FACTS.md#F085) [primary_docs; local_test: video decode] KTH полезен для простого gait sanity-check, а не CCTV acceptance.** Schuldt/Laptev/Caputo, ICPR2004 [S08]: отдельно walking/jogging/running, 25 subjects, 4 scenarios, static25fps, однородный фон160×120; 2,391 subsequences в приблизительно600 исходных видео. Страница заявляет среднюю длину subsequence около4s — это не длина полного AVI. У скачанных файлов длительности по frame count29.64/16.8/13s; данные PTS ходят шагом40ms. Первичные sequence annotations HTTP200,38,292 bytes [S09]. Для person15 d1: walk `1–105,215–338,422–540,630–741`; jog `1–75,140–205,240–300,360–420`; run `1–50,100–150,180–225,280–325`. Это inclusive, **1-based** boundaries; CAVIAR frame numbers начинаются с0. Разделить train/test по субъекту и исходному видео до нарезки. Оригинальный протокол:8train/8val/9test субъектов. Рядом расположенные subsequences одного AVI нельзя раздать по случайным train/test.

KTH содержит вариант масштаба d2 и одежды d3, indoor d4, но проверенная triplet только d1. Не приписываю ей все условия. В полученной triplet отсутствует реальный same-ID walk→run переход: файл каждого класса снят отдельно. Опубликованных метрических скоростей/фазовых gait annotations в `00sequences` нет. Скорость GT из названия running выводить нельзя. Параллельные результаты Weizmann в предыдущем feasibility не повторяю; новая KTH triplet добавляет **jogging** и прямые первичные границы.

<a id="F086"></a>
### F086 — W1_M04: M04-F05 [primary_docs] Две важные ловушки donor-labels.

Provenance: [W1_M04:46](_WORK/W1_M04.md); original aliases: M04-F05. Sources: [S100](SOURCES.md#S100), [S101](SOURCES.md#S101).

**[M04-F05](RAW_FACTS.md#F086) [primary_docs] Две важные ловушки donor-labels.** Прочитан полный K400 label map [S10]: zero-based jogging168, running on treadmill281, walking the dog378, riding or walking with horse273. **Generic walk отсутствует**, generic run отсутствует. Значит K400 X3D/MoViNet/TSM из M08 может дать полезное jogging score/embedding, но нельзя честно писать «готовая бинарная run/walk модель» без нового решения/калибровки. При этом утверждение «в K400 вообще нет бега» тоже неверно. AVA60 evaluation pbtxt [S11] содержит **source id10 run/jog, id14 walk** — семантически точнее; source id не равен позиции в списке60. AVA SlowFast из M08 сохраняется как второй reference: person proposals + RGB temporal clip + RoIAlign, movie-domain и centered-window/lookahead. Его exact contract уже установлен M08 и здесь не дублируется как новый эксперимент.

<a id="F087"></a>
### F087 — W1_M04: M04-F06 [primary_docs; artifact_access_checked] MEVA — отрицательный результат поиска нужной разметки, не отрицательный результат доступности корпуса.

Provenance: [W1_M04:48](_WORK/W1_M04.md); original aliases: M04-F06. Sources: [S102](SOURCES.md#S102), [S103](SOURCES.md#S103), [S104](SOURCES.md#S104), [S105](SOURCES.md#S105).

**[M04-F06](RAW_FACTS.md#F087) [primary_docs; artifact_access_checked] MEVA — отрицательный результат поиска нужной разметки, не отрицательный результат доступности корпуса.** Прямо получены22-страничные MEVA Annotation Definitions,199,708 bytes,SHA256 `6a32c2d27f5aab6418c2a0d35cc5880425af48b729e99387fd074987d5d1792b` [S12]. **Стр.22**, Annotation Modifications: state activities Standing/Crouching/Sitting/Walking/Running/Carrying из V1/V2 больше не аннотируются; Falling также исключено отдельным пунктом. Поэтому отсутствие running annotations в современном MEVA — не подтверждение normal negative. Доступны большой CCTV-корпус, GPS, camera models, tracks, но проверенную бинарную run/walk GT-связку в этом релизе не получил. Старые V1/V2 могут быть иной веткой; наличие в истории не доказывает наличие в текущей release-папке. Repo master при API-проверке `421841a75577b697c314e952e585aecbb1b99e17`, committed2021-12-13; точный raw PDF сохранён/хеширован. MEVID identity labels не восстанавливают gait labels. Данные MEVA CC BY4.0, но это не исправляет отсутствие разметки.

<a id="F088"></a>
### F088 — W1_M04: Сравнение подходов и границы утверждений

Provenance: [W1_M04:50](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Сравнение подходов и границы утверждений

| Подход | Что измеряет / полезность | Что ломает walk/run вывод | Для первого испытания |
|---|---|---|---|
| Bbox/footpoint track + timestamp | Перемещение и резкие изменения траектории, дёшево на host | Pixel/s зависит от глубины, направления, зума; center bbox движется от позы; ID switch создаёт скачок; running-in-place имеет малую трансляцию | Самый простой baseline, но назвать image displacement proxy, если нет геометрии |
| Calibrated ground-point track | Метрическое перемещение по подтверждённой плоскости | Не определяет gait: fast-walk и медленный run могут пересекаться по скорости; скрытые ноги/ступени/иная поверхность нарушают вход | Отдельная оценка скорости и gait, без универсального m/s порога |
| Optical flow | Dense/local image motion, может помочь обнаружить динамику ног/тела | Flow тоже в pixel/frame; смена sampling cadence меняет величину; свет/тени/пар, машинный фон и движение камеры; большой шаг ломает correspondence | Считать в actor ROI, проверять фон/стабилизацию; не переводить raw flow в m/s |
| Pose/gait temporal features | Относительные углы/ритм, меньше зависимости от одежды и фона | Мелкие фигуры, закрытые ноги/PPE/груз, front view, keypoint jitter, разрывы ID; пространственная нормализация не нормализует время | Сохранять confidence и timestamps, abstain при недостаточном наблюдении; не интерполировать длинную окклюзию как GT |
| RGB action model | Прямой label semantics при подходящем обучении, готовые HMDB run/walk | Domain/context shortcut, frame sampling/crop mismatch, multiple actors, full-clip averaging, noncausal test | Точный HMDB checkpoint как offline reference; benchmark после causal adaptation отдельно |

Таблица — **M04-F07 [inference]**, инженерное сопоставление с проверенными input contracts, не заявленные результаты сравнения моделей. Гомографию здесь не разрабатываю. Без calibration один порог pixels/s на near/far участок не обосновывает одинаковую физическую скорость; height-normalized displacement полезен как эмпирический feature, но не метрология. На повороте/движении к камере вертикальная и горизонтальная составляющие меняют проекцию. Нельзя считать bbox overlap скоростью, расстоянием или риском.

<a id="F089"></a>
### F089 — W1_M04: Low-FPS evidence и kill gate

Provenance: [W1_M04:62](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Low-FPS evidence и kill gate

<a id="F090"></a>
### F090 — W1_M04: M04-F08 [local_test: annotation-only arithmetic; inference] 1 FPS не доказан для походки.

Provenance: [W1_M04:64](_WORK/W1_M04.md); original aliases: M04-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M04-F08](RAW_FACTS.md#F090) [local_test: annotation-only arithmetic; inference] 1 FPS не доказан для походки.** Выполнен перебор25 фаз сетки every25frames по реальным inclusive annotation intervals: CAVIAR actor7 running373–436 сохраняет лишь **2–3** observations; actor6 385–489 — **4–5**. KTH person15 running180–225 или280–325 — **1–2** observations. Это честное число наблюдаемых label-frame samples, **не качество модели на 1fps**. Модель/поза не запускались и low-FPS accuracy неизвестна. Сама конфигурация HMDB требует8 кадров interval4; фиксированный low-FPS вход меняет и длительность, и phase density.

Дополнительный математический предел: если единственное различающее движение длится D секунд между равномерными наблюдениями с шагомΔ, при D<Δ существует фаза, в которой оно целиком не наблюдается. При равномерной случайной фазе и идеальном single-observation detector вероятность хотя бы одного попадания min(1,D/Δ); это **упрощённая теоретическая модель**, не event recall gait-классификатора. Для различения походки одного попадания обычно недостаточно; универсального достаточного FPS эта ветка не установила. Acquisition/decode cadence, NN invocation cadence и notification cadence следует задавать отдельно. Выдавать результат раз в секунду можно, сохраняя более плотное temporal evidence; это не требует выбрасывать24/25 исходных кадров.

<a id="F091"></a>
### F091 — W1_M04: M04-F09 [hypothesis: proposed gate] Допуск сценария №1:

Provenance: [W1_M04:68](_WORK/W1_M04.md); original aliases: M04-F09. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M04-F09](RAW_FACTS.md#F091) [hypothesis: proposed gate] Допуск сценария №1:** заранее определить, запрещены ли gait-run, fast movement, abrupt acceleration либо несколько разных событий. Собрать permissioned target near/far/front/side footage с normal walk, fast-walk, jog/run, same-track transition, кратким рывком, running-in-place, перемещением на движущейся платформе, переноской груза, остановкой/поворотом, partial occlusion и crossing actors. Последние два теста важны для ID-switch spikes. Негатив camera shake/zoom и движущаяся техника на фоне проверяет flow/track shortcut. Разметить onset/offset, actor, visible/unknown, policy и согласие двух людей по fast-walk boundary. Нельзя выдавать невидимую походку за отрицательный класс.

Kill/demote до presentation: (a) заказчик требует gait-run, а доступен только speed threshold без blind gait validation; (b) обязательный 1fps acquisition не даёт требуемой temporal recall на коротких target bursts; (c) отсутствует выравнивание media↔annotation/PTS; (d) нет независимого holdout по camera/session/actor; (e) run score распознаёт фон/другого человека; (f) точный NN graph не исполняется на выданном LinQ. В (a) можно согласовать узкую формулировку «быстрое перемещение в настроенной зоне», но это изменение scope, не автоматическое выполнение gait requirement. Порог recall/false-alerts и допустимую задержку не изобретаю: численного SLA в case нет.

Оценивать отдельно: per-class confusion walk/fast-walk/jog/run/unknown; run episode recall при фиксированном false alerts/camera-hour; latency onset→first alert p50/p95 с acquisition+lookahead+NN+confirmation; duplicate alerts; missed short events; abstention/coverage; identity resets. Стратификация: apparent person-height, depth zone, view direction, leg visibility, lighting, source cadence. Для speed branch — MAE/bias относительно независимой ground-speed GT по зонам и направлению плюс event metrics. Успешный clip top1 не заменяет ни одно из этих измерений.

<a id="F092"></a>
### F092 — W1_M04: Неизвестное и адресная передача

Provenance: [W1_M04:94](_WORK/W1_M04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Неизвестное и адресная передача

- Root/evaluation: доступны реальные файлы и exact run intervals, но CAVIAR annotation alignment нужно закрыть до численной latency; пока evidence пригодно для planning/sanity-check, не headline benchmark.
- M08/model stack: SlowOnly RGB HMDB v0.24.1 даёт второй точный donor кроме PoseC3D. Отличать test30views256 от val1view224. Runtime совместимость legacy checkpoint с современной MMAction/LinQ не проверена; K400 jogging output не является бинарным walk/run.
- Dataset role: MEVA current definitions исключают нужные state labels; не брать unannotated walking/running как reliable negatives. KTH d1 triplet с полным хешем и frame segmentation добавляет контролируемый jog/run/walk; NC ограничение сохранить.
- Geometry role: нужна проверенная контактная точка, timestamp provenance и независимая GT скорости; глубинно гомографию не исследовал. Данные gait не калибруют метры/секунду.
- Open questions: target policy fast-walk vs gait-run; целевая длительность коротких рывков и допустимая задержка; разрешённая source cadence; target person-size/leg visibility; LinQ device/operators and measured end-to-end resources; weight-specific licensing; camera/site/session holdout. До ответов нельзя обещать промышленную точность или universal1fps.

Воспроизводимые локальные материалы: `_WORK/M04_fetch.py`, `M04_more.py`, `M04_video.py`; сохранённые HTML/raw configs/PDF/XML, HTTP manifests, hash/media-decode JSON, ограниченный contact sheet. Скрипты не содержат запуска нейросети. `local_test` в этом отчёте относится только к скачиванию, декодированию, парсингу и арифметике наблюдений.

<a id="F093"></a>
### F093 — W1_M05: W1 M05 — телефон, человек и одновременное перемещение: проверка артефактов и разметки

Provenance: [W1_M05:1](_WORK/W1_M05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M05 — телефон, человек и одновременное перемещение: проверка артефактов и разметки

Ветка: есть ли проверяемая связка «конкретные обученные веса → различимые действия с телефоном → тот же человек в реальном видео одновременно идёт», и что она действительно позволяет проверить для сценария №3? Дата прямых обращений: **2026-10-23, 19:33–19:35 UTC (22:33–22:35 Europe/Moscow)**. Автор работы: исследователь W1 M05; без обучения, запуска моделей, платного compute, скачивания исходных фильмов или подагентов. Основная новая работа — программная проверка AVA join и фактической схемы HOI, а не повторение COCO overview.

**Решение [inference]: сценарий №3 остаётся условным резервом для камеры, где различим телефон.** Семантический разрыв частично закрыт: в AVA 2.2 validation действительно есть одновременные phone+walk метки одного человека, а у UPT есть точные доступные веса и отдельные person–phone пары для carry/hold/talk/text. Но это две разные связки данных/задач: UPT обучен на статических HICO-DET; AVA SlowFast классифицирует действия по person ROI и видеоконтексту, без GT боксов телефона. Ни одна проверка ниже не доказывает различение радиостанции/сканера, непрерывные границы нарушения, видимость малого телефона на целевой CCTV или исполнение на LinQ.

<a id="F094"></a>
### F094 — W1_M05: Проверенные выводы

Provenance: [W1_M05:7](_WORK/W1_M05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Проверенные выводы



<a id="F095"></a>
### F095 — W1_M05: W1-M05-F001 [local_test, artifact_access_checked] — точный same-person join существует.

Provenance: [W1_M05:10](_WORK/W1_M05.md); original aliases: W1-M05-F001. Sources: [S101](SOURCES.md#S101), [S111](SOURCES.md#S111), [S112](SOURCES.md#S112), [S113](SOURCES.md#S113), [S114](SOURCES.md#S114).

**[W1-M05-F001](RAW_FACTS.md#F095) [local_test, artifact_access_checked] — точный same-person join существует.** Самостоятельно скачан официальный `ava_val_v2.2.csv.zip`: HTTP 200, 1,611,664 bytes, SHA256 `5596d8c17651a423ed64c1d83c189a7543b3adc6f397583c9e3523d95f43d28e`. В архиве CSV `research/action_recognition/ava/website/www/download/ava_val_v2.2.csv`, 243,029 строк. После группировки по `(video_id, integer timestamp, person_id)` получено 93,993 person-timestamp. Телефонное действие 15 или 57 есть в 1,240 таких группах: 1,113 answer-phone, 127 text/look-cellphone. Пересечение с walk=14: **77 person-timestamp**, в том числе 63 с action15 и 14 с action57; 8 исходных видео, 24 пары video/person, 27 максимальных последовательностей соседних целочисленных timestamps. У всех 77 групп совпадают person bbox для совместных меток. Ни один из 77 samples не входит в отдельно скачанный val excluded-timestamps CSV. Все три ID присутствуют в официальном 60-class evaluation pbtxt. Это результат выполненного разбора аннотаций, не нейросетевого теста. [S001–S003]

| Видео | Пример person_id и timestamps | Что установлено |
|---|---|---|
| `QTmwhrVal1g` | 91, 1181–1190; 106, 1230–1237 | длинные серии совместных sparse labels |
| `WSPvfxtqisg` | 1, 908–915; 7, 946–952 | несколько video/person серий |
| `Ekwy7wzLfjc` | 110, 1416–1420 | серия соседних меток |
| `bePts02nIY8` | 464, 1711–1715 | серия соседних меток |
| `5BDj0ow5hnA` | 571, 1415–1417 | серия соседних меток |
| `Di1MG6auDYo` | 22, 934–936 | серия соседних меток |
| `G4qq1MRXCiY`, `wONG7Vh87B4` | все строки в приложенном JSON | дополнительные совпадения |

**77 samples ≠ 77 независимых событий; 27 серий ≠ 27 подтверждённых непрерывных событий.** Список сохраняется в `W1_M05/ava_phone_walk_join.json`, включая исходные normalized person boxes и полные наборы action IDs. Person ID связывает соседние боксы внутри видео по документации, а не удостоверенную личность на протяжении всего фильма. Последовательность разметки не доказывает отсутствие склейки, непрерывную видимость телефона и точные onset/offset. Каждый источник нужно просмотреть перед изготовлением event pack; здесь исходные медиа не получены и их доступность не проверена. [S001–S003]



<a id="F096"></a>
### F096 — W1_M05: W1-M05-F002 [primary_docs] — схема AVA даёт действие человека, а не object ownership annotation.

Provenance: [W1_M05:25](_WORK/W1_M05.md); original aliases: W1-M05-F002. Sources: [S101](SOURCES.md#S101), [S111](SOURCES.md#S111), [S112](SOURCES.md#S112), [S113](SOURCES.md#S113), [S114](SOURCES.md#S114).

**[W1-M05-F002](RAW_FACTS.md#F096) [primary_docs] — схема AVA даёт действие человека, а не object ownership annotation.** CSV имеет 8 физических колонок: `video_id,timestamp,x1,y1,x2,y2,action_id,person_id`; координаты person bbox нормированы. Action15 — `answer phone`, action57 — `text on/look at a cellphone`, action14 — `walk`. В частности 57 объединяет взгляд на экран и ввод, поэтому его нельзя переименовать в доказанный texting. Отдельного phone bbox, ID устройства, hand contact, разрешения на использование и состояния станка здесь нет. Общий class17 `carry/hold (an object)` не сообщает, какой объект держат. AVA — игровые фильмы с разметкой по секундам, не промышленная CCTV. Source train/val разделены видео; любые crop/соседние секунды/другие планы одного источника должны оставаться в одной downstream группе. [S001–S003]



<a id="F097"></a>
### F097 — W1_M05: W1-M05-F003 [artifact_found, artifact_access_checked, primary_docs] — точный AVA checkpoint доступен как файл.

Provenance: [W1_M05:28](_WORK/W1_M05.md); original aliases: W1-M05-F003. Sources: [S115](SOURCES.md#S115), [S116](SOURCES.md#S116), [S117](SOURCES.md#S117), [S118](SOURCES.md#S118).

**[W1-M05-F003](RAW_FACTS.md#F097) [artifact_found, artifact_access_checked, primary_docs] — точный AVA checkpoint доступен как файл.** MMAction2 `slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb`, бинарный URL S005. Собственный HEAD: 200, Content-Length 135,802,749. Полный файл не скачан, hash и запуск весов отсутствуют. Проверен именно **AVA22 config**, а не похожий AVA21 config из более ранних материалов. Current main наблюдался как `a5a167dff2399e2d182a60332325f9c0d4663517`; сохранённые файлы имеют локальные SHA256 в manifest. Config: FastRCNN с SlowFast R50, RoIAlign, multilabel 81 канал включая background0, train `ava_train_v2.2.csv`, val `ava_val_v2.2.csv`; внешние FAIR person proposals. Требуются видеокадры и person proposals, а не только crop телефона. Видеотензор NCTHW; 32 кадра interval2; val resize короткой стороны256 без flip/crop; mean `[123.675,116.28,103.53]`, std `[58.395,57.12,57.375]`. Train random resize256–320, crop256 и flip0.5; 10 эпох, SGD lr0.075 при config batch setting 8×6. Это условия источника, не предложенные параметры для LinQ. Метрика источника — AVA frame-mAP; она не измеряет своевременный event recall/FP в час для телефонного нарушения. Числового результата телефонного класса для этого checkpoint здесь не проверено. [S004–S006]



<a id="F098"></a>
### F098 — W1_M05: W1-M05-F004 [primary_docs, inference] — штатный temporal donor использует будущие кадры.

Provenance: [W1_M05:31](_WORK/W1_M05.md); original aliases: W1-M05-F004. Sources: [S115](SOURCES.md#S115), [S117](SOURCES.md#S117), [S118](SOURCES.md#S118).

**[W1-M05-F004](RAW_FACTS.md#F098) [primary_docs, inference] — штатный temporal donor использует будущие кадры.** Прямо прочитан `SampleAVAFrames._get_clips`: start=`center−(clip_len//2)*interval`, stop=`center+((clip_len+1)//2)*interval`, затем `range(start,stop,interval)`. При 32×2 offsets **−32,−30,…,+30 frames**. AVADataset default FPS=30, timestamp_start=900; штатный AVA sampling требует до +1 секунды будущего относительно метки t, до времени инференса и event-confirmation. Это не причинный результат, доступный в момент t. При обработке с задержкой можно честно отнести результат к t после получения последнего кадра; прошлое-only окно является другим условием и требует отдельной проверки. Нельзя подавать «32 кадра с 1 FPS» и ожидать тот же learned temporal scale: это уже примерно минута вместо ~2 секунд. Sparse 1 Hz labels также не обосновывают пропуск нативных кадров в stream. [S004,S006]



<a id="F099"></a>
### F099 — W1_M05: W1-M05-F005 [artifact_found, artifact_access_checked] — UPT имеет точный обученный HOI donor с доступным payload.

Provenance: [W1_M05:34](_WORK/W1_M05.md); original aliases: W1-M05-F005. Sources: [S119](SOURCES.md#S119), [S120](SOURCES.md#S120), [S121](SOURCES.md#S121), [S122](SOURCES.md#S122).

**[W1-M05-F005](RAW_FACTS.md#F099) [artifact_found, artifact_access_checked] — UPT имеет точный обученный HOI donor с доступным payload.** Официальная реализация Zhang, Campbell, Gould, CVPR2022, *Efficient Two-Stage Detection of Human-Object Interactions With a Novel Unary-Pairwise Transformer*. Репозиторий archived; наблюдавшийся main `192743045e4c5f6827299fdc15809f5b97ac1b8e`. UPT-R50 HICO-DET model zoo ссылается на Drive ID `1lvopTC_JlGHdKOyyEZTUp2VtFfCQ-08z`, имя `upt-r50-hicodet.pt`. Первичный GET download возвращает HTML virus-scan warning, поэтому **HTTP200 этой страницы сам по себе не означает веса**. После штатного confirm form GET реально получен `application/octet-stream`, Content-Length **219,754,181**, первые 4,096 bytes прочитаны, начинается `504b0304` (ZIP serialization container). Поток закрыт, полный файл не получен; модель не загружена/не исполнялась. Записаны response metadata и hash только probe chunk, не hash checkpoint. Веса включают DETR detector согласно model zoo. [S007–S009]



<a id="F100"></a>
### F100 — W1_M05: W1-M05-F006 [primary_docs, local_test] — точный mapping не совпадает с 600-way HOI ID.

Provenance: [W1_M05:37](_WORK/W1_M05.md); original aliases: W1-M05-F006. Sources: [S123](SOURCES.md#S123), [S124](SOURCES.md#S124), [S125](SOURCES.md#S125), [S126](SOURCES.md#S126), [S127](SOURCES.md#S127).

**[W1-M05-F006](RAW_FACTS.md#F100) [primary_docs, local_test] — точный mapping не совпадает с 600-way HOI ID.** В официальной UPT implementation выход на изображение: `boxes[N,4]`, `pairing[2,M]` (индексы human, object в boxes), `scores[M]`, `labels[M]` (117-way verb для HICO-DET), `objects[M]` (80-way object), `size[2]`. Координаты boxes — pixel xyxy относительно фактически поданного resized tensor; `size` — его H,W. Для исходного кадра нужно выполнить обратное масштабирование. Один pair может иметь несколько выходных verb строк. Score вычисляется как sigmoid interaction logit × product prior. Это индекс пары в текущем изображении, а не постоянный track ID или юридическое владение. Evaluation utility переводит `(objects,verbs)` в 600-way interaction, проверяет пару по minimum human/object IoU 0.5 и использует 11-point AP. Нельзя трактовать выход `labels=101` как AVA class101 или 600-way HOI101. [S010,S011]

Скачан и полностью разобран JSON HICO-DET utilities submodule revision **`9dd59c1`**, указанной в официальном UPT repo: 12,246,669 bytes. Схема: `annotation,filenames,empty,objects,verbs,correspondence,size`; 38,118 image annotation records. Correspondence хранит zero-based `[hoi,obj,verb]`. Это converted training annotation, не оценочный video test.

| Объект=67 `cell_phone` | Verb ID | HOI ID | Pair-label count в train JSON | Число изображений |
|---|---:|---:|---:|---:|
| carry | 8 | 283 | 183 | 158 |
| hold | 36 | 284 | 538 | 471 |
| read | 73 | 285 | 188 | 150 |
| repair | 75 | 286 | 1 | 1 |
| talk_on | 101 | 287 | 235 | 223 |
| text_on | 103 | 288 | 131 | 104 |
| no_interaction | 57 | 289 | 1 | 1 |

Это точные результаты подсчёта приложенным `count_hico.py`, не заявленная полнота исходного HICO и не статистика ошибок модели. Сами названия классов не устанавливают temporal labels. В utilities dataset документации изображения без bbox annotations пропускаются при индексировании; downstream negative sampling должен явно учитывать такое поведение, а не получать «чистые отрицательные» автоматически. [S012,S013]



<a id="F101"></a>
### F101 — W1_M05: W1-M05-F007 [local_test, inference] — carry и use НЕ взаимоисключающие классы.

Provenance: [W1_M05:54](_WORK/W1_M05.md); original aliases: W1-M05-F007. Sources: [S126](SOURCES.md#S126).

**[W1-M05-F007](RAW_FACTS.md#F101) [local_test, inference] — carry и use НЕ взаимоисключающие классы.** `HICO_train2015_00000092.jpg` в скачанном JSON имеет phone HOI283,284,287, то есть carry, hold и talk_on для похожих human/phone boxes. Поэтому правило «carry-score велик → подавить use» семантически неверно. Допустимы отдельные положительные multi-label оценки; классификация только carry против use требует новой согласованной GT. Наличие лишь одного phone no_interaction pair-label в этом training representation означает, что само существование такого класса не является доказательством достаточной negative coverage. В 80 object names отсутствуют отдельные walkie-talkie, barcode scanner, industrial handheld terminal. Ошибки на этих предметах **unknown**: никаких запущенных confuser-тестов здесь нет. [S012]



<a id="F102"></a>
### F102 — W1_M05: W1-M05-F008 [inference] — артефакты дополняют друг друга, но не взаимозаменяемы.

Provenance: [W1_M05:57](_WORK/W1_M05.md); original aliases: W1-M05-F008. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W1-M05-F008](RAW_FACTS.md#F102) [inference] — артефакты дополняют друг друга, но не взаимозаменяемы.** UPT улучшает постановку association: связывает конкретный person bbox и конкретный phone bbox с verb, но обучается на изображении, не доказывает simultaneous walking. AVA joint labels закрывают same-person phone+walk at sampled timestamps, но не дают phone bbox/проверки scanner/radio. Их можно использовать в разных диагностических наборах: HICO для object/verb mapping и статической парности; AVA candidate clips для person-time fusion. Смешивать aggregate AP двух датасетов в рейтинг пригодности для CCTV нельзя.

<a id="F103"></a>
### F103 — W1_M05: Права и доступ: отдельные объекты

Provenance: [W1_M05:59](_WORK/W1_M05.md); original aliases: section record. Sources: [S108](SOURCES.md#S108), [S109](SOURCES.md#S109), [S110](SOURCES.md#S110), [S128](SOURCES.md#S128), [S129](SOURCES.md#S129).

## Права и доступ: отдельные объекты

| Объект | Проверенный статус | Не установлено |
|---|---|---|
| UPT code | BSD-3-Clause в LICENSE, HTTP200 [S014] | все условия каждой зависимости не перепроверялись |
| UPT weights | точный официальный link, 219,754,181-byte octet-stream probe | отдельная явная лицензия весов; full hash; содержимое state_dict; воспроизводимость/конвертация |
| HICO utilities code | README ссылается на MIT; submodule pinned | MIT утилит не следует автоматически переносить на фотографии/аннотации |
| HICO train converted annotations | официальный авторский utilities repo, реальный JSON скачан | отдельный полный grant на исходные images/annotations в этой проверке не установлен; source archive не скачан |
| MMAction2 code | LICENSE напрямую прочитан по observed commit, Apache-2.0; exact config/code прочитаны | отдельная проверка всех компонентов/weights grant отсутствует |
| AVA annotation release | официальный download page прямо указывает CC BY4.0 для перечисленных datasets | это не автоматическая очистка отдельных прав на оригинальные фильмы |
| AVA movies | известны YouTube IDs, схема времени и source split | actual retrievability, актуальная лицензия каждого ролика, разрешённая локальная передача/показ клипов, person visibility не проверены |

Не считать отказ HTTP, HTML interstitial или устаревший сайт доказательством отсутствия артефакта. GitHub API commit request дал 403; revision дополнительно прочитан из GitHub HTML `currentOid`, а payload snapshots имеют SHA256. Предполагаемые original HICO URLs `https://ywchao.github.io/hico/` и `https://ywchao.github.io/hico-det/` дали 404: это failed locator, не опровержение существования оригинального датасета. Действительный lead из utilities — `http://www-personal.umich.edu/~ywchao/hico/` и archive Drive ID `1QZcJmGVlF9f4h-XLWe9Gkmnmj2z1gSnk`; архив здесь не пробировался.

<a id="F104"></a>
### F104 — W1_M05: Практическая event-проверка и stop gates

Provenance: [W1_M05:73](_WORK/W1_M05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Практическая event-проверка и stop gates

**Наблюдаемая цель [inference]:** тот же человек в пересечении интервалов видимого use-like phone interaction и перемещения по цеху либо независимо установленной работы с оборудованием, при запрещающей policy. Не считать наклон головы, phone рядом с человеком или рабочую ROI доказательством всех звеньев. Истинное владение устройством не нужно: требуется наблюдаемая actor–device association. Сценарий движения легче локализовать, чем состояние «работает с оборудованием»; последнее требует внешней разметки контакта/операции или независимого состояния станка.

1. Сначала собрать permissioned target clips и проверить на нативном изображении, затем на **фактическом** preprocessing. Зафиксировать bbox телефона в исходных и model-input pixels, occlusion и возможность человека-разметчика различить phone/radio/scanner. Пример арифметики: 18 px при ширине1920 превращаются в 6 px при resize640; это не валидированный cutoff. Нативный crop до resize может сохранить детали, upscale уже уменьшенного кадра их не восстанавливает. Если доступный ракурс не различает предмет, вернуть unknown, а не высокий-confidence вывод из позы.
2. Обязательный matched набор: phone at ear; reading/texting while walking; carry at hip без use; телефон на столе/в руке соседа; сканер/радио/инструмент у уха или в двух руках; наклон головы к детали; PPE/gloves/occlusion; разрешённая процедура со служебным терминалом. Включить crowded handoff/crossing для проверки identity swap и далёкий small-phone, back view. Это **предлагаемые controls**, не обнаруженные готовые размеченные примеры AVA/HICO.
3. Непрерывная actor-time GT: отдельно phone-visible, association-confirmed/unknown, use-like interaction, walking, active-equipment context, policy и итоговое пересечение. Поставить start/end/censored/visibility intervals. Отрицательный контроль причинности: phone-use → убрал → пошёл; другой человек одновременно идёт; человек продолжает идти после прекращения use. Временно близкие, но непересекающиеся признаки не должны создавать нарушение.
4. Локальный эксперимент после разрешённого получения весов: RGB/resize/normalization и bbox coordinate round-trip; UPT verb/object→HOI mapping; сохранить raw пары/scores и не использовать carry как veto. Отдельно AVA centered replay с честным временем доступности последнего кадра и past-only ablation. Единицы split — source movie/target session/camera, а не crops/frames; AVA валидируемые примеры после настройки становятся development, не новым lockbox.
5. Измерять actor-compatible one-to-one event matching: all-event и observable-event recall с coverage; precision; unmatched alerts/camera-hour реального разрешённого отрицательного видео; duplicates/event; onset/confirmation/notification delay по PTS и wall clock раздельно. Отдельно ошибки detector, owner association, use label и temporal context. Не назначать универсальный порог пикселей, допустимый процент ошибок или фиксированный hold-time без требований команды.
6. Gate в MVP: нет разрешённого target pack, видимость недостаточна, confusers не отделяются, веса не воспроизводятся/не экспортируются либо нет подтверждённого device path — оставить reserve. UPT transformer+DETR и SlowFast+RoIAlign не являются доказанными LinQ моделями. Конкретный SDK и поддержка ops неизвестны; host rules/tracking/temporal state допустимы только после согласования архитектуры, а inference/скорость должны быть измерены на реальном устройстве.

<a id="F105"></a>
### F105 — W1_M05: Handoff и незакрытые вопросы

Provenance: [W1_M05:103](_WORK/W1_M05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Handoff и незакрытые вопросы

**M08:** можно заменить прежнее «same-video/person phone+walk join не проверялся» на F001 с ровно указанной единицей подсчёта; добавить +30-frame future dependency F004. **D15:** в итоговой event schema разделить sparse action samples, candidate consecutive runs и реально просмотренные continuous intervals; person_id AVA не global subject identity. **MVP/device owners:** две разные тяжёлые NN связки не объявлять готовой LinQ pipeline; сначала target camera visibility + confusers, затем exact host inference/export and device evidence.

Не закрыто: media access/permissions и визуальная пригодность восьми AVA источников; целевой промышленный event pack; per-class robustness phone/radio/scanner; full weight hash/actual execution; отдельные grants на UPT weights/HICO media; detector association stability в толпе; рабочее оборудование и разрешённый служебный терминал; экспорт и качество после PTQ на конкретном LinQ. Это локализованные gaps, а не доказательство невозможности сценария.

<a id="F106"></a>
### F106 — W1_M06: W1 M06 — movement-aware person–machine proximity

Provenance: [W1_M06:1](_WORK/W1_M06.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M06 — movement-aware person–machine proximity

Branch question: can we obtain an actual temporal model, code, weights and matched real sequences/labels for person–moving-machine danger, with explicit pedestrian/driver ownership and credible motion/footprint semantics?

**Decision:** no newly verified package closes that complete industrial CCTV chain. **NearCollision is a concrete new temporal research donor**, with reachable trained weights and a matched real six-frame test tensor and numeric labels, verified below using bounded ranges. It predicts proximity to its own moving camera, not a separately observed forklift–pedestrian pair. Its released notebook/ROS paths have material inconsistencies. **FP-TTC is a distinct dense temporal method**, but its advertised weight folder did not expose a downloadable checkpoint in this check, and its observation-plane TTC is not third-party pair collision risk. Keep the scenario a conditional reserve: detector + stable tracking + measured machine motion + calibrated ground envelope on host CPU; admit only after a real pair-specific test pack. No LinQ compatibility, accuracy or timing claim follows from any source here.

Access window: 2026-10-23 approximately 19:35–19:47 UTC; final clock check19:47:09 UTC. All paths under `W1_M06_evidence/` are private bounded evidence. No inference, training, GPU work, paid API, outreach or full dataset/weight download. `local_test` below means actual metadata/data inspection, not model execution. Read Context-prompt.md, complete assignment, targeted existing feasibility report, CASE_NOTES/SYNTHESIS_CONTRACT and D09's industrial-artifact findings. D09 remains the authority for its own industrial donor archive/member work; this branch does not relabel those clips as proximity truth.

<a id="F107"></a>
### F107 — W1_M06: M06-F01 — NearCollision has a real temporal artifact chain, with a different target

Provenance: [W1_M06:9](_WORK/W1_M06.md); original aliases: M06-F01. Sources: [S130](SOURCES.md#S130), [S131](SOURCES.md#S131), [S132](SOURCES.md#S132), [S133](SOURCES.md#S133), [S134](SOURCES.md#S134).

## [M06-F01](RAW_FACTS.md#F107) — NearCollision has a real temporal artifact chain, with a different target

**[M06-S01](SOURCES.md#M06-S01) / primary_docs, author_claim:** Aashi Manglik, Xinshuo Weng, Eshed Ohn-Bar, Kris M. Kitani, *Forecasting Time-to-Collision from Monocular Video: Feasibility, Dataset, and Challenges*, IROS 2019; inspected arXiv revision v3 dated 2020-11-02. https://arxiv.org/pdf/1903.09102 ; project https://aashi7.github.io/NearCollision.html . Locators: III.A–C, IV, Tables II/IV, VI.

Paper semantics, deliberately bounded: a camera/LIDAR suitcase traverses three university buildings. Near-collision means at least one person within one metre of the platform; it is not physical contact or a forklift footprint. Capture is 10Hz, pushing speed 0.2–1.5m/s. Six frames represent 0.5s history; labels forecast first positive proximity within six seconds. Published best MAE is 0.753±0.687s, but 5–6s-horizon MAE is 1.8369s. The paper acknowledges failures when people move away in the same direction, and warns that changed camera height, speed and scenes can impair generalization. Reported segment counts differ within the paper (13,658 versus 13,685); neither is an independent-event count. These are author results, not reproduced here.

**[M06-S02](SOURCES.md#M06-S02) / artifact_found, primary_docs:** official repository https://github.com/aashi7/NearCollision ; pinned HEAD `011ac10cbabc14159295f8d232730bb5baf2e0a2`, commit page https://github.com/aashi7/NearCollision/commit/011ac10cbabc14159295f8d232730bb5baf2e0a2 reports 2021-09-06 16:04:27−07:00. API commit request initially returned its SHA, later tree/API calls hit HTTP403 rate limit; ordinary repository/commit pages and immutable raw code returned200. That is an API-access limitation, not artifact absence.

README promises raw folders `mats_nov`, `mats_dec`, `mat_stereo_camera`, plus calibration, point clouds and stereo/depth data. **Fresh ordinary Drive folder GET showed only `h5_files` and `trained_models` children in the advertised root**, https://drive.google.com/drive/folders/1tAywlmXA3iDJtggUIP3FFh0RoBXtH1Qu . Thus the current raw-recording path advertised by README is unresolved; no conclusion that all raw data no longer exists. A repository `sample_data/sample.mat` is present, GitHub metadata size86.4MB, but was not downloaded. Its small extraction script reads `left_imgs`; this does not establish complete calibration/label fields of that MAT.

<a id="F108"></a>
### F108 — W1_M06: M06-F02 — exact reachable weights and matched HDF5, without huge downloads

Provenance: [W1_M06:19](_WORK/W1_M06.md); original aliases: M06-F02. Sources: [S135](SOURCES.md#S135), [S136](SOURCES.md#S136), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S140](SOURCES.md#S140).

## [M06-F02](RAW_FACTS.md#F108) — exact reachable weights and matched HDF5, without huge downloads

**artifact_access_checked:** Public Drive metadata actually enumerates files and byte counts, not merely a project-page promise. Saved HTML and decoded arrays: `near_models_drive*`, `near_h5_drive*`. Exact metadata folders:

- https://drive.google.com/drive/folders/1pcXLdWpLa8eXp7kv5uHuNW3MyuphSPoF
- https://drive.google.com/drive/folders/1uJ3AEIyaUTtOY4t8w4N0eAbiw7PJkOOl

| Artifact | Exact byte-access URL | Publisher/Drive size | Actual access check |
|---|---|---:|---|
| `6Image6s_027` | https://drive.usercontent.google.com/download?id=150hQ2oSEJkPsWpjpCW-XqNiEFlcVkwfL&export=download |97,711,273|HTTP206 bytes0–1023; binary legacy PyTorch/pickle-like prefix; not deserialized or executed|
| `vgg_on_voc800` | https://drive.usercontent.google.com/download?id=1KmaIY1DU4h2XnsJkkckv0GWdFY7oOytO&export=download&confirm=t |537,375,863|HTTP206 bytes0–65535; binary prefix; not fully downloaded|
| `6ImageTest.h5` | https://drive.usercontent.google.com/download?id=10uIEuqmaYnjtt3wGCTm7tmbdBmhQBigm&export=download&confirm=t |937,501,056|HTTP206 correct ranges; HDF5 magic and actual schema/labels/two windows inspected|
| `SingleImageTest.h5` | https://drive.google.com/file/d/1m9CLKFqjO3Tgw03uEJ_odptvo4upM5eQ/view |142,863,032|metadata only; no payload check|

The latter two large-file binary URLs initially returned HTTP200 HTML without `confirm=t`; HTTP200 alone would have falsely looked successful. Adding the standard confirmation query returned the bounded binary ranges. These are anonymous access observations, not license grants, full-file checksums or integrity validation. Metadata creation timestamps of the three central artifacts are in May2019; access is October2026. Weights/HDF5 are mutable Drive IDs without an independent release digest.

**local_test:** Installed only h5py into this branch's evidence/deps and used a bounded seekable HTTP reader (`inspect_h5.py`, timeout30s,1MiB metadata cap). Across the final schema/label pass,139,648 bytes read, comprising first64KiB plus two ending blocks. Saved `near_h5_schema.json`:

| HDF5 key | Actual shape/type | Observed meaning / caveat |
|---|---|---|
|`rgb`|`[1038,6,224,224,3]`, uint8|six ordered image tensors per example; contiguous storage offset2048|
|`labels`|`[1038]`, float64|min0, max5.9, mean2.0832369942196536; first values3.0,2.9,2.8,…; no negative sentinel observed|
|`Mean`|scalar float64|actual2.2997543581616484|
|`Variance`|scalar float64|actual2.9830609539231623|

Those are stored names/values; do not exchange them based on comments. Training-code comments claim Mean2.98/Variance2.299 for a differently named d2 file, reversing the magnitudes compared with this released test file. This observation does not prove which training dataset produced the checkpoint. Exact HDF5 root has only these four keys: no source recording IDs, timestamps, split groups or track/pair ownership. No independent no-event label is established by this label vector; zero can mean immediate proximity.

**local_test, actual image payload:** fetched sample0 bytes2048–905215 (903,168B), reshaped exactly six224×224×3 images using the inspected contiguous HDF5 layout. SHA256 of sample0 bytes `f38cbfb415bc2570b7a8c70c1780f30fda95084fa219c86ce353f7fe19e3c718`; saved `near_test_sample0.rgb`, `near_sample0.json` and visually inspected `near_sample0_contact.jpg`. It shows a low corridor viewpoint with a distant person and changing perspective; no forklift. This is a decoded six-frame real-image window, not a downloaded full source video or a validated future near-collision trajectory.

<a id="F109"></a>
### F109 — W1_M06: M06-F03 / local_test, temporal dependence:

Provenance: [W1_M06:48](_WORK/W1_M06.md); original aliases: M06-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M06-F03](RAW_FACTS.md#F109) / local_test, temporal dependence:** fetched only next sample1 bytes905216–1808383 (903,168B); SHA256 `ee848c8b670a55bb6ecc54e6639f96ed9425055684b8859d2ae591b1304ae8ed`. `numpy.array_equal(sample0[1:],sample1[:-1]) == True`. Five of six frames are byte-identical across neighboring test windows; labels3.0 versus2.9 seconds. Saved `near_sample_overlap.json`. This proves within-test overlap, **not train/test leakage**. However random-window re-splitting or counting1038 windows as1038 independent events would be invalid. Raw recording/stereo-view provenance is missing from the HDF5; group original traversals and both stereo views before any new split, then bootstrap/report uncertainty by event or recording.

<a id="F110"></a>
### F110 — W1_M06: M06-F04 — code-path contradictions that matter before reproduction

Provenance: [W1_M06:50](_WORK/W1_M06.md); original aliases: M06-F04. Sources: [S141](SOURCES.md#S141), [S142](SOURCES.md#S142), [S143](SOURCES.md#S143).

## [M06-F04](RAW_FACTS.md#F110) — code-path contradictions that matter before reproduction

**[M06-S03](SOURCES.md#M06-S03) / primary_docs, code inspection:** pinned training https://raw.githubusercontent.com/aashi7/NearCollision/011ac10cbabc14159295f8d232730bb5baf2e0a2/train/6ImageTrain.py ; saved `near_train_6ImageTrain.py`. Inputs are transformed224×224 per frame, ImageNet mean/std normalization, shared VGG16 feature extractor,512→16 convolution, six flattened features into2048-unit regression head. Targets are `labels - Mean`. Batch24, SGD0.001,50 epochs are code settings. Paths refer to `6ImageTestd2.h5`/`6ImageTraind2.h5`, not simply the released filenames; a reproducible trainer-to-checkpoint linkage remains unverified. No retraining was attempted.

**[M06-S04](SOURCES.md#M06-S04) / primary_docs, code inspection:** test notebook https://raw.githubusercontent.com/aashi7/NearCollision/011ac10cbabc14159295f8d232730bb5baf2e0a2/test/6ImageVideo.ipynb . Despite its six-frame filename, it declares `feature_size=16*7*7*3`, while concatenating all input frames. Released HDF5 contains six frames. Its load of the six-frame checkpoint is therefore a concrete shape inconsistency by code/schema comparison; not an executed exception. Notebook adds stored Mean to both predictions and centered ground truth. This must be checked/fixed with checkpoint tensor shapes before quoting reproduced MAE.

**[M06-S05](SOURCES.md#M06-S05) / primary_docs, code inspection:** ROS https://raw.githubusercontent.com/aashi7/NearCollision/011ac10cbabc14159295f8d232730bb5baf2e0a2/test/multi_stream_prediction.py . Six-frame deque is correct in head size, but frames are collected per ROS callback without explicit10Hz/timestamp spacing. It passes BGR images from `bgr8` into normalization with no visible BGR→RGB conversion; notebook data path differs. It produces one full-frame scalar and writes the same scalar on every retained person box. It does not track a particular pedestrian or infer person–forklift pair ownership. It gates on any person score>0.5; no detected person or insufficient history sets `t=1000`. That is missing perception/warmup, not measured safety. Unlike notebook evaluation, it publishes raw network output without visibly adding Mean. The absolute offset is material if trained on centered labels; exact deployed checkpoint target convention requires verification. Hard CUDA calls, ROS, TensorFlow Faster-RCNN and external detector checkpoints make this an old multi-framework reference, not a CPU/LinQ-ready binary.

**Rights / unknown:** inspected repository root has no LICENSE file and README gives citation instructions, not a permissive license. Public weight and HDF5 folders expose no separately verified data/checkpoint license. Code, weights and data rights all remain unknown separately; neither academic publication nor public binary access supplies a redistribution grant. Do not bundle these assets publicly on the basis of availability. This does not assert that the authors cannot grant rights.

<a id="F111"></a>
### F111 — W1_M06: M06-F05 — FP-TTC: movement-aware but wrong TTC frame and incomplete weights

Provenance: [W1_M06:60](_WORK/W1_M06.md); original aliases: M06-F05. Sources: [S144](SOURCES.md#S144), [S145](SOURCES.md#S145), [S146](SOURCES.md#S146), [S147](SOURCES.md#S147).

## [M06-F05](RAW_FACTS.md#F111) — FP-TTC: movement-aware but wrong TTC frame and incomplete weights

**[M06-S06](SOURCES.md#M06-S06) / primary_docs:** LChanglin official *FP-TTC: Fast Prediction of Time-to-Collision using Monocular Images*, README says submitted T-CSVT May2024. Pinned HEAD `625e5be66761d42bb2d0ac92b32881e274c767ad`; commit https://github.com/LChanglin/FP-TTC/commit/625e5be66761d42bb2d0ac92b32881e274c767ad dated2024-05-31 12:33:01+08:00. https://github.com/LChanglin/FP-TTC . README defines TTC to the observation plane, trains with Driving and KITTI, uses PyTorch1.12/CUDA11.3/RTX3090. Its temporal decoder intends current TTC from past images; this is a real temporal mechanism, unlike pixel-distance alarms. Relative speed/accuracy claims in README are author claims and not imported into industrial performance estimates.

**artifact_found/access_checked:** pinned `pretrained/` tree contains only `weights.txt`, whose72-byte text points to https://drive.google.com/drive/folders/1WL2cuKDt2YPERB8WaAScX9qbO4x4p4hI . Anonymous GET returned200 folder HTML titled weights but no item rows/checkpoint names in inspected content. No explicit access-denied response; cannot decide empty folder versus rendering/access issue. Exact advertised checkpoint `./pretrained/fpttc_mix.pth.tar` is not a checked binary. Do not claim the model lacks weights everywhere. Code license: no LICENSE in inspected root; weight license unknown; Driving/KITTI rights are separate and not checked into a blanket code grant.

**[M06-S07](SOURCES.md#M06-S07) / primary_docs, code:** https://raw.githubusercontent.com/LChanglin/FP-TTC/625e5be66761d42bb2d0ac92b32881e274c767ad/test.sh specifies two scales, upsample4, padding32, attention splits2/8, radius−1/4. Pinned `evaluation.py` reads KITTI `_10.png`/`_11.png`, resizes640×320, calls CUDA directly, exports dense `scale[0,0]` as `_eta_out.npy`; this is not an event label or an identity-resolved pair TTC. README inference section mistakenly says `sh train.sh`; use actual test.sh only after checkpoint/access issues are resolved. No real forklift video, driver/pedestrian annotation or industrial hard-negative evaluation found in inspected package. A stationary CCTV camera may observe a forklift crossing the floor without any approach toward its observation plane; that alone prevents substituting this dense ego TTC for pedestrian–forklift impact time.

<a id="F112"></a>
### F112 — W1_M06: M06-F06 — industrial collision literature does not automatically provide runnable risk models

Provenance: [W1_M06:68](_WORK/W1_M06.md); original aliases: M06-F06. Sources: [S148](SOURCES.md#S148), [S149](SOURCES.md#S149).

## [M06-F06](RAW_FACTS.md#F112) — industrial collision literature does not automatically provide runnable risk models

**[M06-S08](SOURCES.md#M06-S08) / primary_docs:** Hyeongjun Kim, Taejoo Kim, Won Jo, Jiwon Kim, Jeongmin Shin, Daechan Han, Yujin Hwang, Yukyung Choi, *Multispectral Benchmark Dataset and Baseline for Forklift Collision Avoidance*, Sensors22(20):7953,2022-10-19. https://doi.org/10.3390/s22207953 ; full primary article https://pmc.ncbi.nlm.nih.gov/articles/PMC9608680/ . Locators2.1.5–6,2.2,3.2,Data Availability. Real forklift-mounted synchronized stereo RGB/thermal data and SSD2.5D centroid-distance regression are relevant. However its hazardous-zone grouping uses a size threshold tied to an assumed5km/h braking condition, not measured pairwise movement/TTC. Data statement explicitly requires request to corresponding author and limits provided data to nonprofit purposes. No outreach performed. No exact checkpoint/code download was verified. Article CC BY does not override that data restriction. Four-sensor collection and monocular-CCTV runtime are materially different conditions. Treat as evidence for calibration and modality/domain limitations, not an available ready benchmark.

<a id="F113"></a>
### F113 — W1_M06: M06-F07 — NVIDIA's explicit industrial negatives are useful policy evidence, not metric truth

Provenance: [W1_M06:72](_WORK/W1_M06.md); original aliases: M06-F07. Sources: [S150](SOURCES.md#S150).

## [M06-F07](RAW_FACTS.md#F113) — NVIDIA's explicit industrial negatives are useful policy evidence, not metric truth

**[M06-S09](SOURCES.md#M06-S09) / primary_docs:** NVIDIA *VSS3.3.0 Warehouse Blueprint / Alerting Service*, live undated documentation accessed2026-10-23: https://docs.nvidia.com/vss/vision-agent/agent-workflows/industry-specific-examples/warehouse-operations-blueprint/microservice-configuration/alerting-service . Locators Overview,Alert Verification/Near Miss,Prompt Tuning. It verifies upstream proximity candidates with a short-clip VLM; operator-only, completely stationary forklift, far-separated and nonconvergent parallel movement are explicit negative cases. A freeze-position counterfactual distinguishes yielding because of path intersection from voluntary precaution. These are useful annotation dimensions. But a prompt's approximate1–2m criterion is not measured calibration; completed-clip reasoning can use future information. Documentation names Cosmos3 Nano Reasoner in overview and Cosmos Reason2 in near-miss prose, so pin deployed configuration before reproducing. No task-specific tuned weights or measured near-miss test set is supplied by this page. Its absence/no-visibility negative handling should not become a safety guarantee for an occluded or missed person.

<a id="F114"></a>
### F114 — W1_M06: M06-F08 — operational branch proposed for the case, with minimal assumptions

Provenance: [W1_M06:76](_WORK/W1_M06.md); original aliases: M06-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M06-F08](RAW_FACTS.md#F114) — operational branch proposed for the case, with minimal assumptions

**inference / proposed, not tested:** retain separate learned perception and CPU temporal reasoning. Detect each person and machine; track them using source timestamps; estimate machine ground movement over a minimum reliable history. Persist an ordered `(person_track,machine_track)` candidate, with explicit own-driver/occupant state. Stable co-motion inside a cab is supporting evidence, not sufficient to exclude a pedestrian walking beside a truck; require cab/seat region or human-reviewed ownership and allow uncertain state. A person getting off the forklift must transition out of driver ownership after ground contact, not be permanently blacklisted.

For a fixed camera on a locally planar floor, metric risk minimally needs lens distortion handling if material, a measured floor homography (at least four noncollinear correspondences with real units), a valid floor region, trustworthy contact estimates and frame timestamps. Person foot midpoint can approximate floor contact when feet are visible. Forklift bbox bottom centre is not its support polygon: forks, load overhang, turning tail and reversing require footprint/orientation or a deliberately conservative scene envelope. Pose may improve feet/occlusion state but cannot infer hidden metric contact by itself. Homography should project floor-contact features, not elevated whole bboxes. If only image-space zones are available, label the event as configured image-envelope proximity and demonstrate motion discrimination without metres/TTC claims.

For host-CPU constant-velocity screening with relative floor position `r=p_person−p_machine` and velocity `v=v_person−v_machine`, closest-approach time `t*=clip(−r·v/(v·v),0,H)` is only a **point-agent screening statistic**. Collision requires predicted person occupancy to intersect the time-indexed machine swept footprint, including uncertainty margin. Euclidean distance divided by speed is not generally TTC, especially for lateral passing or divergence. Braking, turns, speed changes, IDs switching, noisy contact and dropped frames invalidate a confident extrapolation. Distinguish current dangerous proximity, predicted collision and retrospective near-miss/evasion as separate labels. Static-near may still violate a different zone policy but must not satisfy this moving-machine scenario.

Moving/PTZ/vibrating cameras invalidate a single fixed image-to-floor mapping. Stabilization/global-motion estimation may preserve a conditional image-envelope experiment; metric velocities need camera pose/plane updates or another calibrated sensor. Masking/freeze/recalibration states should invalidate affected motion history and prevent synthetic velocity spikes. Neither NearCollision's ego training nor FP-TTC removes this requirement for an independently moving third-party pair.

<a id="F115"></a>
### F115 — W1_M06: M06-F09 — concrete evaluation gate and unresolved links

Provenance: [W1_M06:86](_WORK/W1_M06.md); original aliases: M06-F09. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M06-F09](RAW_FACTS.md#F115) — concrete evaluation gate and unresolved links

**proposed evaluation:** require at least one permissioned real target pair sequence and complete pre-event/after-clear footage; do not stage dangerous approaches. Annotate source timestamps, person/machine IDs, driver ownership transitions, machine-motion intervals, floor-contact visibility, valid calibration region, current envelope entry/exit, and separately future swept-path conflict/evasive action. Use an uncertainty/occluded flag; missing detections never constitute demonstrated negative truth. Label all candidate pairs in multi-agent footage, not just the visually obvious pair.

Essential controls: stationary-near; moving-far; driver-only; stopped-after-motion; same-direction separated; crossing in image but on different floor paths; forklift approaching another pedestrian than the selected one; turn/reverse/fork/load overhang; pedestrian exits cab; rack occlusion; missed/recovered IDs; camera movement; partial first/last event. Keep routine long video for false alarms per hour and event-level recall, paired with onset delay/advance and duration coverage. Report performance by direction/contact visibility, not just detector mAP or regression MAE on positive overlapping windows. Split by source episode/camera/day and shared simulation seed/multiview run; preserve source hashes.

The near-term experiment is **not** to port these old temporal models directly to LinQ. First restore an exact, runnable temporal reference off-device on the matched NearCollision sample/HDF5 if rights permit: fix head/frame agreement, confirm checkpoint output centering, explicit channel ordering and timestamp cadence, then compare to published evaluation. Separately build target CCTV pair labels and CPU geometry around the existing verified forklift/person detector route. Only measured export/operator support and actual device execution can establish LinQ suitability; host rules do not establish neural acceleration.

Unresolved localized links: (1) target-domain real pair-event/driver/static-near annotations and rights; (2) NearCollision current raw-recording access and independent split provenance; (3) NearCollision code/data/weight grants; (4) exact training variant/centering of6Image6s_027 and legacy dependency reproducibility; (5) FP-TTC actual checkpoint download/license; (6) target-camera calibration, forklift footprint and allowed violation policy; (7) exact LinQ model I/O/runtime constraints. This branch supplies a verifiable temporal artifact donor and concrete failure evidence, not a claimed complete warehouse safety system.

<a id="F116"></a>
### F116 — W1_M07: W1 M07 — barriers, under-conveyor passage, suspended loads, height and harness

Provenance: [W1_M07:1](_WORK/W1_M07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M07 — barriers, under-conveyor passage, suspended loads, height and harness

Access window: 2026-10-23 approximately 19:38–19:50 UTC (22:38–22:50 Moscow). Worker M07. No model inference, training, device test, outreach, paid API, or large archive download occurred. `local_test` below means explicitly described metadata/schema/media checks, never inference. This branch read the assignment and targeted sections of the earlier feasibility report as leads; all new findings below come from the linked primary artifacts.

<a id="F117"></a>
### F117 — W1_M07: Branch question and decision

Provenance: [W1_M07:5](_WORK/W1_M07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

Can a reproducible pretrained model + code + matched real video + annotations establish completed barrier climb, passage beneath a conveyor/suspended load, or work at known height without correctly attached harness?

**Decision [inference]: no complete verified target chain was established.** The useful new contribution is two accessible, decoded fence/wall probe clips and an inspected pose-rule implementation that does **not** recognize completed crossing; a much better specified **synthetic** under-load benchmark with readable annotations and evaluation outputs; and a precise localization of the harness-hook paper's unavailable-artifact gate. Narrow site-specific occupancy or corridor rules remain implementable with generic person tracking, but must retain their own event names. No LinQ support is inferred.

| Route | Evidence reached | Missing gate / permitted conclusion |
|---|---|---|
| Fence/wall pose rules | Pinned code, accessible generic pose weight URL, two downloaded/decoded clips | No temporal labels, provenance/license unresolved, no opposite-side landing criterion; posture/occupancy probe only |
| Suspended-load zero-shot detection | Pinned SynthSite code, exact checkpoint names, reachable weight files, 227 video/label references, published per-video outputs | All synthetic; no physical ground truth, target-camera test, or original evaluation weight hash |
| Harness hook geometry | Full primary 2026 paper, detailed formulas and evaluation conditions | Data by request; ready code/checkpoint/annotations not found in this inspected paper; geometry does not observe a closed valid connection |
| CML climbing/crawling | Primary paper + Figshare v3 metadata and archive addresses | Skeleton data, not matched target RGB events; no verified ready action checkpoint; archive HEAD403 in this session |
| CAAR real industrial contrasts | Official project terms, explicit harness attach/not-attach and suspended-load scope | Prior access authorization/email required, academic-only license; no acquired annotation or model payload |

<a id="F118"></a>
### F118 — W1_M07: M07-F01 — readable fence media does not supply completed-climb truth

Provenance: [W1_M07:33](_WORK/W1_M07.md); original aliases: M07-F01. Sources: [S166](SOURCES.md#S166), [S167](SOURCES.md#S167).

## [M07-F01](RAW_FACTS.md#F118) — readable fence media does not supply completed-climb truth

**[artifact_access_checked/local_test]** Both pinned files were downloaded in full, SHA256 hashed and decoded using PyAV. OpenCV was unavailable; no packages were installed. Full decoding succeeded for **301 frames each**, 1920×1080, 30fps (about 10.03 s). Six uniformly spaced frames were rendered into contact sheets and visually inspected.

| File / exact URL suffix after pinned repository raw base | Bytes | SHA256 |
|---|---:|---|
| `data/fenceclimb.mp4` | 3,524,804 | `15ab1fc0b23f702caaae3d86f2edbcd4e926c72557efa827b92a9bf6550d1159` |
| `data/wall.mp4` | 3,217,915 | `7f9594c9f933a6d9703426096e41ff18aacc16bd7b6e3e57b42c9898cca16234` |

Full URLs: https://raw.githubusercontent.com/Khushnoor-gojwari/Fence_detection_wall_and_iron_fence/3aa345f049a033f53c38608aec6d586ddc372ca7/data/fenceclimb.mp4 and https://raw.githubusercontent.com/Khushnoor-gojwari/Fence_detection_wall_and_iron_fence/3aa345f049a033f53c38608aec6d586ddc372ca7/data/wall.mp4 . Files, contact sheets and `video_decode.json` are in `M07_evidence/`.

**[local_test/unknown]** Samples show a person approaching, raising arms/feet against a fence/wall, then returning to the same apparent side. They do not visually establish a completed opposite-side landing. `wall.mp4` has a conspicuous overlaid timecode moving backward between sampled frames. This is a temporal-integrity red flag, not proof of a particular editing/generation process. Capture provenance, whether footage is real rather than generated, and media rights remain **unknown**. Do not call these verified real CCTV. No actor IDs, event time intervals, completed/attempt labels or independent negatives were acquired. Contact-sheet inspection is not frame-by-frame action annotation.

<a id="F119"></a>
### F119 — W1_M07: M07-F02 — exact pose code distinguishes neither entry nor completion

Provenance: [W1_M07:46](_WORK/W1_M07.md); original aliases: M07-F02. Sources: [S151](SOURCES.md#S151), [S152](SOURCES.md#S152), [S168](SOURCES.md#S168).

## [M07-F02](RAW_FACTS.md#F119) — exact pose code distinguishes neither entry nor completion

**[primary_docs]** In S01, `raw_cross` is restricted-side membership; four consecutive observations produce `crossed`. No earlier safe-side observation is required. `analyze_climb` combines near-boundary posture with raised hands/bent or lifted feet, or an ankle-above-line cue; five flags confirm climbing. Generic YOLOv8 pose supplies 17 COCO points, not a pretrained fence-action class. Pinned generic weight URL https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt HEAD200 **6,832,633 bytes**; not downloaded or executed.

**[inference]** A first-frame person already on the restricted side can become `CROSSED`. A worker reaching for an overhead object near the line can become `CLIMBING`. Confirmation suppresses jitter but does not add the absent approach→transfer→opposite landing stages. A suspended climber's ankles are not ground contact points; treating them as floor-side coordinates is especially unsafe. No target event performance follows from source availability.

**[unknown]** No repository license grant was visible in the inspected root listing; do not substitute the generic model's grant for application code or media. Ultralytics assets require their applicable model/license review; an inference frontend's own license cannot clear the entire stack. Exact package versions, export shape/operator support and LinQ runtime behavior were not tested.

<a id="F120"></a>
### F120 — W1_M07: M07-F03 — SynthSite has a strong matched schema, but all videos are synthetic

Provenance: [W1_M07:54](_WORK/W1_M07.md); original aliases: M07-F03. Sources: [S153](SOURCES.md#S153), [S154](SOURCES.md#S154), [S155](SOURCES.md#S155), [S169](SOURCES.md#S169).

## [M07-F03](RAW_FACTS.md#F120) — SynthSite has a strong matched schema, but all videos are synthetic

**[primary_docs]** S02 describes 227 generated short videos, with two or three reviewers, 150 unanimous Tier1 and 77 disagreement Tier2 clips. Labels are clip-wide `True_Positive` (hazard present) versus `False_Positive` (safe) — these are ground-truth class names, not confusion-matrix outcomes. No real incident footage is included. The card warns against substituting it for real safety assessment.

**[artifact_access_checked/local_test]** Downloaded `synthetic_video_labels.csv` (22,894 bytes), API video manifest, code, design notes and detector result CSVs. A local CSV/manifest check found 227 unique filenames, every label matched a `videos/*.mp4` manifest entry, no duplicates/missing references, correct reviewer counts, majority labels and tier agreement conditions. Counts: Tier1 unsafe76/safe74; Tier2 unsafe39/safe38. Label SHA256 `5eb1e15dc87a92070e690372014504e260d705c6810b9a157981503278555093`. `synth_integrity.json` records checks. These tests verify references and consistency, not visual correctness or accessible video payloads.

**[artifact_found]** Exact example: https://huggingface.co/datasets/govtech/SynthSite/resolve/2904ec01c3dbf2efba09f2cb1b7bdf17841d4d39/videos/sora-2-pro_0001.mp4 ; API declares **6,032,660 bytes**, LFS SHA256 `879c8b985886ad459f81ba3e2ca741d824e204f6a7641f66df3238661579d9de`. Video not downloaded or decoded. Saved tree `synth_tree.json` supplies remaining 226 paths and LFS metadata.

<a id="F121"></a>
### F121 — W1_M07: M07-F04 — exact under-load implementation and its causal limits

Provenance: [W1_M07:62](_WORK/W1_M07.md); original aliases: M07-F04. Sources: [S156](SOURCES.md#S156), [S157](SOURCES.md#S157), [S170](SOURCES.md#S170), [S171](SOURCES.md#S171).

## [M07-F04](RAW_FACTS.md#F121) — exact under-load implementation and its causal limits

**[primary_docs]** Downloadable code: https://huggingface.co/datasets/govtech/SynthSite/resolve/2904ec01c3dbf2efba09f2cb1b7bdf17841d4d39/code/hazard_detector_eval.py . Its YOLO route names `yolov8x-worldv2.pt`, text classes include person and hoisted load with crane hook, conf0.30/IoU0.40, ByteTrack, all-frame processing. It uses one-second windows with 12 positive votes and fills internal gaps of ≤2 observations. It estimates scale from median person-box height assuming 1.75m. DINO uses `IDEA-Research/grounding-dino-base` without revision pin, two text queries, ~1fps sampling and clip aggregation (≥2 violating samples OR ≥20%). Its normalized geometry filters include load-size and above-person/proximity tests.

Weight candidate matching code filename: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8x-worldv2.pt HEAD200 **146,355,704 bytes**. No author execution hash, release pin, package lock or weight download was established; accessible candidate is not exact-run reproduction. DINO current snapshot is S03.

**[inference]** This code is instructive rather than physical calibration. Median person height does not solve perspective, crouching, occlusion, variable worker depth or off-plane load geometry. Apparent clearance/box-center distance cannot establish the actual suspended-load footprint. A motorized hoist with a landed load must be distinguished from a suspended one. The algorithm can merge frame positives from different worker/load pairs because its hazard history is clip-global; this is not one worker's continuous event truth.

**[inference]** Copying this YOLO vote rule into a 1fps runtime makes its one-second window shorter than 12 samples, so it cannot trigger at all. At 30fps, 12 positives mean a different positive-time fraction from 16fps. Backfilling gaps uses later observed positives within the current history; distinguish detection time from reconstructed onset. The DINO OR rule can classify a five-sample clip unsafe after one positive (20%), so “two required frames” alone misdescribes it. Whole-clip aggregation cannot substantiate causal online alert latency. No temporal event boundaries are supplied in the annotation schema.

<a id="F122"></a>
### F122 — W1_M07: M07-F05 — outputs can be recounted, not promoted to target performance

Provenance: [W1_M07:72](_WORK/W1_M07.md); original aliases: M07-F05. Sources: [S153](SOURCES.md#S153), [S154](SOURCES.md#S154), [S155](SOURCES.md#S155).

## [M07-F05](RAW_FACTS.md#F122) — outputs can be recounted, not promoted to target performance

**[artifact_access_checked/local_test]** Both primary per-video output CSVs GET200 at the pinned S02 base under `results/detector_outcome/results_yolo_world.csv` and `results_grounding_dino.csv`. Local recount found 227 unique rows each: YOLO TP101/FP61/FN14/TN51; DINO TP38/FP13/FN77/TN99. This matches the author's result document. These are **author inference outputs independently recounted**, not models run here. Saved `results_recount.json`.

**[inference]** Synthetic appearance, generator cues, selection of usable generated scenes and ambiguous majority labels limit external validity. No held-out real-camera evaluation or disjoint calibration/test protocol was established by this branch. Reuse Tier1 as synthetic logic stress tests, keep Tier2 and individual votes visible as uncertainty. Never silently collapse disagreement into confident violation truth. Keep generated variants/source prompts/scenes grouped if later constructing splits; neighboring frames and overlapping windows must remain together. Results do not measure completed crawling, harness use or metric clearance.

**[primary_docs]** License: pinned `LICENSE`, custom GovTech Singapore terms incorporating MIT with exclusions (agency identifiers/third-party or restricted assets) and Singapore governing-law/arbitration additions. Applies to repository contents according to its text; do not reduce to unconditional plain MIT. Detector weights and third-party libraries remain separate grants. No blanket assertion about all generator output rights is independently verified here.

<a id="F123"></a>
### F123 — W1_M07: M07-F06 — hook paper's claim is stronger than its directly observed signal

Provenance: [W1_M07:80](_WORK/W1_M07.md); original aliases: M07-F06. Sources: [S158](SOURCES.md#S158), [S159](SOURCES.md#S159).

## [M07-F06](RAW_FACTS.md#F123) — hook paper's claim is stronger than its directly observed signal

**[primary_docs/author_claim]** S04 uses 2700 drone still images from controlled scaffolding and active sites, five categories (helmet/no-helmet/harness/no-harness/hook), 6:3:1 category-stratified split. It reports 90.82% on 305 harness-use instances. Equations compare hook/harness center image height, accept distance ≤λ times harness-box height (default λ3), and associate nearest eligible unique hook. Data Availability says data are available from corresponding author upon request. No downloadable checkpoint, ready implementation or annotation archive was identified in this inspected full paper. Search failure is not proof none exists elsewhere. Code/weight/data grants remain unresolved; article is CC BY4.0.

**[inference]** An image hook above a harness center and nearby is not evidence that the hook gate is closed, captures the anchor, belongs to that lanyard, or that the structure is a suitable anchor. A carried loose hook above the shoulder is a critical false-safe control. Nearest-hook assignment can fail when two workers cross or share adjacent scaffold bays. Image y-order is viewpoint dependent. The stated split does not establish project-disjoint evaluation; similar scaffold/background/worker imagery may occur on both sides unless grouping is provided. UAV still-image results do not establish small distant CCTV visibility or metric operating height.

<a id="F124"></a>
### F124 — W1_M07: M07-F07 — CML is a skeleton resource, with public/experiment distinction

Provenance: [W1_M07:86](_WORK/W1_M07.md); original aliases: M07-F07. Sources: [S160](SOURCES.md#S160), [S161](SOURCES.md#S161), [S162](SOURCES.md#S162), [S163](SOURCES.md#S163), [S164](SOURCES.md#S164), [S172](SOURCES.md#S172), [S173](SOURCES.md#S173).

## [M07-F07](RAW_FACTS.md#F124) — CML is a skeleton resource, with public/experiment distinction

**[primary_docs/artifact_access_checked]** S05 Table6 includes climb up/down and crawling in action taxonomies, not conveyor/fence-completion labels. Figshare v3 metadata explicitly distinguishes the larger experiment collection from public release: **6131 public samples, 4333 construction-related**, because redistribution/modification rights were not clear for many source datasets. Public license metadata CC BY4.0. Do not present all reported experiment samples as publicly downloadable target video.

Exact declared files: `Construction_Related_Data.zip`, **463,446,328 bytes**, https://ndownloader.figshare.com/files/36703026 ; `All_DATA.zip`, **799,212,259 bytes**, https://ndownloader.figshare.com/files/36703035 . First archive HEAD403 after redirects in this session; neither downloaded. The metadata remained 200. This localizes access uncertainty; it does not prove permanent unavailability. No verified pretrained CML checkpoint or matched industrial RGB clip/temporal label pair was obtained. Skeleton joint remapping is not a substitute for unseen equipment/scene geometry.

<a id="F125"></a>
### F125 — W1_M07: M07-F08 — CAAR is semantically promising but unavailable within this task

Provenance: [W1_M07:92](_WORK/W1_M07.md); original aliases: M07-F08. Sources: [S165](SOURCES.md#S165).

## [M07-F08](RAW_FACTS.md#F125) — CAAR is semantically promising but unavailable within this task

**[primary_docs]** S06 explicitly describes paired proper/improper harness attachment on an electric lift, suspended-load work and stepladder misuse, with multiview real-world collection claims. It reports untrimmed 4K30 footage and nine actors. Access requires prior requested rights; terms restrict academic research, prohibit redistribution and commercial use. Accordingly no model/video/annotation payload is acquired or cleared for commercial industrial use here. Do not infer clip boundaries, specific unsafe relation labels or model availability from example gallery captions.

<a id="F126"></a>
### F126 — W1_M07: M07-F09 — minimal honest event contracts and validation controls

Provenance: [W1_M07:96](_WORK/W1_M07.md); original aliases: M07-F09. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [M07-F09](RAW_FACTS.md#F126) — minimal honest event contracts and validation controls

The following are **[inference/hypothesis]** deployment contracts, not established model performance:

* **Boundary occupancy:** calibrated person contact proxy lies inside a configured image region. Distinguish initial occupant, observed entry and exit. No temporal NN or equipment classifier is necessary if the boundary is surveyed and static, but tracking/occlusion policy still is.
* **Completed fence climb:** one identity observed approaching on side A, progressing up/contacting the barrier, transferring torso/legs across its top, then landing/support on side B. Attempts, retreats and merely standing behind the fence are separate labels. A floor homography cannot be applied to raised limbs.
* **Under-conveyor passage:** a fixed known conveyor may be manually mapped. Require tracked entry A→visible transit→exit B and posture/corridor clearance evidence; disappearance alone is unknown. Variable/moving equipment requires equipment localization/state, and route geometry must account for gaps, designated crossings and maintenance authorization.
* **Under suspended load:** first establish that the object is hanging, then its current three-dimensional footprint/fall zone and relation to worker. Surveyed geometry, calibrated multiple views or crane telemetry may be necessary; a floor homography alone does not project an airborne object correctly. Moving ropes/hook alone do not prove load state.
* **At height without visible harness:** requires known surveyed elevated work surface, site policy/context requiring fall protection, person-to-surface assignment and adequate torso/strap visibility. Return `not_visible`, `ambiguous_owner` or `unknown_height` separately. Do not turn absence of a detector box into visible absence.
* **Valid harness connection:** additionally requires hook/lanyard/anchor association, visible closure/engagement and appropriate anchor evidence. A presence detector cannot supply these. Collective fall protection, lift guardrails and local procedure affect the operational rule; no legal threshold is inferred here.

Hard negatives: reach/stretch/repair next to fence; low gate or authorized gap; climb attempt and retreat; crouch to pick up tool outside conveyor; crawl beside/behind equipment; another worker emerging after occlusion; landed load on pallet; foreground person with distant overhead load; empty hook; elevated worker behind guardrail; reflective vest/backpack straps; harness under coat; two adjacent workers/hooks; loose hook held high; correctly attached worker whose hook is occluded. Critical false negatives include fast transfer between samples, conveyor occlusion lasting most of passage, low contrast thin straps/lanyards, small hook targets, dust/glare/night, identity swaps and a person reappearing after tracker reset.

For future evaluation, annotate source video/camera/identity, event intervals, attempted/completed/unknown states, visibility, geometry version, known surface height and attachment evidence. Split by camera/site/session/person where appropriate, group derivative clips, evaluate event recall and false alerts per camera-hour, identify duplicated alerts and detection delay relative to a stated observable trigger. Preserve the footage's original timing; sparse samples cannot retrospectively recover a missed transfer. This branch establishes **no measured accuracy/FPS/latency or LinQ PASS**.

<a id="F127"></a>
### F127 — W1_M07: Evidence inventory / unresolved gates

Provenance: [W1_M07:111](_WORK/W1_M07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Evidence inventory / unresolved gates

All private evidence is under `_WORK/M07_evidence/`: pinned source, two small clips, two contact sheets, video hashes/decode metadata, HF API metadata/tree, seven SynthSite documentation/code/label files, two output CSVs, integrity/recount JSON, DINO metadata, paper HTML/text, Figshare metadata/description, access-check headers. API 403 files preserve rate-limit responses and must not be mistaken for successful tree inventories.

Highest-value next changes in evidence: a permissioned target-camera sequence with completed crawl/climb truth; CAAR authorized annotation schema and applicable use grant; public exact trained harness/hook checkpoint with class map and actual closure/anchor labels; independently calibrated work-surface height; LinQ device/runtime/export/operator checks on whichever exact model is selected. Until then, narrow configuration-based routes and synthetic stress tests should be labeled separately from the full requested behaviors.

<a id="F128"></a>
### F128 — W1_M08: W1 M08 — temporal architecture checkpoints, sampling contracts, and one conditional extension

Provenance: [W1_M08:1](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 M08 — temporal architecture checkpoints, sampling contracts, and one conditional extension

Research/access date: 2026-10-23, 19:23–19:27 UTC (22:23–22:27 Moscow). Branch question: which temporal methods have an inspectable checkpoint→preprocessing→video-label contract and could become a host-side reference without claiming unsupported LinQ execution? Decision: prioritize causal MoViNet-A0 Stream only if a neural temporal module is needed; compare against track/pose rules. Keep STGCN++ as a conditional pose-window reference and X3D-XS as a bounded RGB clip reference. Do not put VideoMAE or AVA SlowFast on the delivery critical path. None is tested on LinQ; no models were loaded, exported, trained or executed.

Novel contribution relative to sibling feasibility report: exact config contradictions and artifact status, not a new broad feasibility vote. Read original case notes and targeted sibling lines concerning temporal models before researching. The case requires actual LinQ neural inference, measured speed, event evidence and suppression of duplicate ongoing incidents. A host temporal classifier alone does not satisfy the LinQ requirement.

Status vocabulary: `primary_docs` = directly read original docs/code; `artifact_found` = original linked file; `artifact_access_checked` = HTTP metadata/content checked; `local_test` = explicitly named local metadata/CSV operation only; `inference` = our engineering conclusion; `unknown` = missing evidence. HTTP success does not prove valid model, inference, video acquisition or deployment.

<a id="F129"></a>
### F129 — W1_M08: Decision-bearing findings

Provenance: [W1_M08:9](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Decision-bearing findings

<a id="F130"></a>
### F130 — W1_M08: M08-F01 [primary_docs; inference] Causal and buffered-online are different contracts.

Provenance: [W1_M08:11](_WORK/W1_M08.md); original aliases: M08-F01. Sources: [S175](SOURCES.md#S175), [S178](SOURCES.md#S178), [S189](SOURCES.md#S189).

**[M08-F01](RAW_FACTS.md#F130) [primary_docs; inference] Causal and buffered-online are different contracts.** MoViNet Stream explicitly uses causal (2+1)D convolution, external state tensors and one-frame updates. In contrast, standard MMAction TSM distributes eight samples across the supplied clip and shifts information both temporal directions; it can run on a trailing window after acquisition, but is not equivalent to a trained unidirectional streaming network. The original TSM online demo is a separate MobileNetV2 hand-gesture/Jester implementation with TVM and explicit supported gestures; do not transfer its Nano GPU >70 FPS claim (excluding I/O) to industrial actions, CPU or LinQ. [[M08-S01](SOURCES.md#M08-S01), S04, S15]

<a id="F131"></a>
### F131 — W1_M08: M08-F02 [primary_docs; artifact_access_checked] MoViNet-A0 Stream is the strongest concrete host candidate.

Provenance: [W1_M08:13](_WORK/W1_M08.md); original aliases: M08-F02. Sources: [S175](SOURCES.md#S175), [S177](SOURCES.md#S177).

**[M08-F02](RAW_FACTS.md#F131) [primary_docs; artifact_access_checked] MoViNet-A0 Stream is the strongest concrete host candidate.** Exact archive `movinet_a0_stream.tar.gz` returns HTTP200, 15,165,440 bytes. Linked `movinet_a0_stream.tflite` returns HTTP200, **27,141,832 bytes**, whereas the current README labels that link 13 MB. This is an artifact/documentation size discrepancy, not evidence of compression/runtime RAM. README reference construction: `model_id=a0`, `causal=True`, `conv_type=2plus1d`, `se_type=2plus3d`, `activation=hard_swish`, `gating_activation=hard_sigmoid`, `use_positional_encoding=False`, `use_external_states=True`, 600 classes, output states enabled. TFLite export fixes batch1, one frame, 172px; RGB tensor is `[1,1,172,172,3]` **plus state inputs**, not a stateless image classifier. Each output state must feed the matching next input. The 50-frame 172px evaluation refers to accumulated ten-second clips at recommended 5fps, not a required 50-frame input call or guaranteed event latency. Source K600 single-clip top1 72.05 is an author benchmark, not target safety accuracy. [[M08-S01](SOURCES.md#M08-S01), S03]

The model README distinguishes current and `_legacy` stream archives, with architecture changed in 2021 to mobile-friendly (2+1)D. Pin archive content/hash before export; do not mix old checkpoints/current construction. README gives float32 single-core Pixel4 22ms and Xeon W-2135 16ms single-frame A0, while 2022 official blog gives separately quantized A0 int8 4.80ms/3.1MB/65.0% and float16 17.47ms/7.6MB/71.5%. These are different binaries/precision conditions; the directly checked float TFLite is **not** the blog's int8 artifact. Quantized-binary exact current URL/license/metadata remains unresolved. Initialization/reset policy is an application decision: isolate per camera/person crop stream, reset on identity or source discontinuity, and validate long normal→incident transitions. Maintaining cumulative state forever may dilute or retain context; benchmark stream classification is not an onset detector. [inference]

<a id="F132"></a>
### F132 — W1_M08: M08-F03 [primary_docs; artifact_access_checked] STGCN++ is small but its sampling is offline and its data rights restrict immediate use.

Provenance: [W1_M08:17](_WORK/W1_M08.md); original aliases: M08-F03. Sources: [S183](SOURCES.md#S183), [S184](SOURCES.md#S184), [S185](SOURCES.md#S185), [S186](SOURCES.md#S186).

**[M08-F03](RAW_FACTS.md#F132) [primary_docs; artifact_access_checked] STGCN++ is small but its sampling is offline and its data rights restrict immediate use.** Exact MMAction v1.2.0 `stgcnpp_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d.py` and `...20221228-86e1e77a.pth` are inspectable; checkpoint HEAD200/5,859,545 bytes. Model is RecognizerGCN/STGCN, adaptive graph initialization, residual GCN, multiscale temporal convolution, COCO graph and 60-class head. Pipeline is PreNormalize2D→GenSkeFeat(coco,j)→UniformSampleFrames(100)→PoseDecode→FormatGCNInput(num_person=2). Train/val one clip, test **ten** clips. The 100 samples span the available action's duration; there is no fixed fps/seconds value in this contract. Thus “100 frames at 30fps = 3.33 seconds” would be an invented deployment assumption. README reports joint-only 89.29% xsub, 1.39M parameters/1.95G; do not quote fused four-stream results as this artifact's performance. Filename says 80e but actual tagged config's train loop is **16 epochs** with RepeatDataset times5. Preserve the actual config, not a parsed filename training schedule. [[M08-S09](SOURCES.md#M08-S09), S10]

Skeleton data donor `ntu60_2d.pkl` HEAD200/705,401,771 bytes; not downloaded/unpickled. Docs say dictionary `split` and `annotations`; each annotation has `frame_dir`, `total_frames`, `img_shape`/`original_shape`, `label`, `keypoint[M,T,V,C]`, `keypoint_score[M,T,V]`; COCO V17,C2 versus original Kinect NTU V25,C3. Those representations/checkpoints are not interchangeable. Tagged PreNormalize2D maps x to `(x−w/2)/(w/2)` and y to `(y−h/2)/(h/2)` using img_shape (fallback1080×1920); feeding already normalized coordinates without adjusting this step corrupts input. Joint feature generation includes available keypoint scores; verify the final channel contract during export rather than assuming x/y alone. 2D annotations were generated with Faster-RCNN R50 person detection and HRNet-w32, so substituting another pose extractor changes input distribution. NTU is staged, Kinect multi-view; not CCTV incident localization. Native labels include falling, phone, staggering, but no industrial policy. Original NTU page requires registration/request/release agreement and restricts data to academic/noncommercial research, including redistribution/derivation restrictions. A public derived-pickle URL does not resolve that. [[M08-S11](SOURCES.md#M08-S11), S12]

<a id="F133"></a>
### F133 — W1_M08: M08-F04 [primary_docs; artifact_access_checked] X3D-XS is a useful bounded RGB comparison, with an actual preprocessing discrepancy.

Provenance: [W1_M08:21](_WORK/W1_M08.md); original aliases: M08-F04. Sources: [S176](SOURCES.md#S176), [S179](SOURCES.md#S179), [S187](SOURCES.md#S187).

**[M08-F04](RAW_FACTS.md#F133) [primary_docs; artifact_access_checked] X3D-XS is a useful bounded RGB comparison, with an actual preprocessing discrepancy.** Original PyTorchVideo builder fixes pretrained XS to 4 frames, input_crop_size160; S13/160, M16/224. Official Hub demonstration instead uses XS/S crop182 and M256, with short-side equal to crop. Demo XS temporal rate12 at nominal30fps gives `clip_duration=4*12/30=1.6s`; effective sampled rate about2.5fps. It is not four adjacent30fps frames. Hub scales RGB /255, normalizes mean .45 and std .225, uniform temporal subsampling, short-side resize and center crop. Exact XS checkpoint `X3D_XS.pyth` HEAD200/30,779,313 bytes; loader expects `model_state`, 400-class Kinetics model. Builder says do not modify kwargs with pretrained=True. Consequently freeze one exact recipe and re-evaluate; do not silently combine 182px demo input with 160px model-zoo FLOP/accuracy claims. A trailing 1.6s buffer supports delayed online use, but X3D convolution has no external causal state. Raw float32 4×3×160×160 input is 1,228,800 bytes, **input only**, not RAM estimate. [[M08-S02](SOURCES.md#M08-S02), S05]

<a id="F134"></a>
### F134 — W1_M08: M08-F05 [primary_docs] TSM/TSN offer deployment-friendly 2D compute but no safe shortcut from clip to event.

Provenance: [W1_M08:23](_WORK/W1_M08.md); original aliases: M08-F05. Sources: [S178](SOURCES.md#S178), [S180](SOURCES.md#S180), [S189](SOURCES.md#S189).

**[M08-F05](RAW_FACTS.md#F134) [primary_docs] TSM/TSN offer deployment-friendly 2D compute but no safe shortcut from clip to event.** MMAction tagged TSM config uses 8 segments each clip_len1, frame_interval1, sampled across the full supplied video, 224px crops. Train uses multiscale crop/flip; val center-crop, test TenCrop (80 images per source clip). Thus `1x1x8` is not a fixed8-frame continuous temporal window. Exact checkpoint HEAD200/97,651,119 bytes, listed in artifact inventory. TSN is a useful order-agnostic average-segment baseline: cheaper temporal logic does not make it a reliable motion transition recognizer. TSM improves ordering cues but shifting channels is an operator/export concern and ordinary bidirectional TSM has future dependence within the clip. Host PyTorch CPU reference possible in principle; no FPS, memory or LinQ compiler support was measured. [[M08-S04](SOURCES.md#M08-S04), S06, S15]

<a id="F135"></a>
### F135 — W1_M08: M08-F06 [primary_docs] 3D CNN/SlowFast and VideoMAE remain offline references here.

Provenance: [W1_M08:25](_WORK/W1_M08.md); original aliases: M08-F06. Sources: [S181](SOURCES.md#S181), [S182](SOURCES.md#S182), [S187](SOURCES.md#S187), [S188](SOURCES.md#S188), [S190](SOURCES.md#S190).

**[M08-F06](RAW_FACTS.md#F135) [primary_docs] 3D CNN/SlowFast and VideoMAE remain offline references here.** Concrete AVA SlowFast config is FastRCNN with ResNet3dSlowFast plus 3D RoIAlign and multi-label AVA head (81 outputs including background). It needs full RGB clip **and person proposals**, not just a cropped actor or standalone classification call. Despite filename 8x8x1, pipeline is SampleAVAFrames clip_len32 interval2; slow resample_rate4/speed_ratio4. Tagged sampler explicitly starts at center−32 and ends before center+32, so at30fps last frame is center+30 (1s future) and span62/30≈2.067s; nominal window64/30≈2.133s. Preserving original center semantics adds at least ~1s lookahead plus decode/inference. A trailing-window relabel is a changed evaluation protocol. AVA prep fixes source30fps; reducing observation rate to1fps changes coverage dramatically. [[M08-S07](SOURCES.md#M08-S07), S08, S13]

VideoMAE-B checkpoint is K400-pretrained **recognition** donor, not an industrial anomaly or event detector: HEAD200/173,099,345 bytes. Tagged config is **test-only**, 16 frames interval4, num_clips5, ThreeCrop224, NCTHW, ImageNet mean/std. README table says short-side320, whereas config resize is224: another actual recipe discrepancy. 16x4 nominal30fps spans2.13s (first-to-last2s); test uses15 views, not one causal input. 87M/180G are source model statistics, no CPU/TPU performance guarantee. Original VideoMAE self-supervised masking and small-data transfer claims do not eliminate the need for target labels/fine-tuning or make the fine-tuned classifier causal. Broad temporal convolution/transformer heads are not a fourth deliverable merely because frameworks support them: no exact industrial checkpoint/data contract was established here. [[M08-S14](SOURCES.md#M08-S14), S16]

<a id="F136"></a>
### F136 — W1_M08: Four conditional methods and acquisition/decision contracts

Provenance: [W1_M08:29](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Four conditional methods and acquisition/decision contracts

| Candidate | Conditions / event contract | Practical split / stop condition |
|---|---|---|
| 1. Detector/pose/track + timed rules | Preserve timestamped observations and uncertainty; past-only ROI dwell, calibrated motion if geometry exists, posture-transition and motion-evidence history. Use hysteresis and per-episode close/re-arm rather than repeated frame alerts. Baseline for running/fall/immobility; fall requires transition, lying may need a separate prolonged-state rule. | Neural detector/pose only on LinQ **if exact export/device works**; CPU tracker/rules. Timestamp and identity gaps suspend evidence, not prove immobility. No new checkpoint claim in this branch. |
| 2. MoViNet A0 Stream | Exact above causal graph; choose per-scene or person-stream semantics; preserve 5fps-like inputs initially, compare temporal recall and onset latency. Fine-tune action head then selected blocks only if permissioned target clips exist; background/no-event must be represented. | Host TFLite CPU reference, per-stream state budget. On-device conditional on actual LinQ state I/O/operators/compiler. Stop if state handling or target recall fails. |
| 3. STGCN++ joint COCO17 | Pose extractor provenance, normalization, stable person assignment and confidence missingness must match; evaluate 100-sample past windows with explicit seconds and adapted head. Native whole-action test does not validate those windows. | Host GCN only after pose visibility is adequate. NTU donor permission and model-weight terms must be resolved; no new pose network just to decorate a weak visibility case. |
| 4. X3D-XS bounded RGB window | Freeze crop160 versus demo182 decision and sampling; 4 samples from1.6s is a **reference recipe**, not proven industrial optimum. Re-label full target episodes with start/end, visibility, actor and negatives. | Host CPU reference if rules miss cues; 3D operators make LinQ uncertain. Fine-tune on own data rather than treating K400 scores as violations. |

[inference] Keep acquisition fps separate from network inference/update fps. Store enough timestamped frames to revisit brief transitions even if NN output is throttled. Define event score timestamp, receptive context, first valid detection and notification time independently; centered-model lookahead must enter measured latency. One incident should create one episode notification and remain visible in the journal. No unconsciousness diagnosis, bbox-overlap-as-meters or weight/effort inference.

<a id="F137"></a>
### F137 — W1_M08: One supported additional hazard: apparent person-directed physical aggression

Provenance: [W1_M08:40](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## One supported additional hazard: apparent person-directed physical aggression

<a id="F138"></a>
### F138 — W1_M08: M08-F07 [artifact_access_checked; local_test(annotation only); inference] Conditional research extension, not validated production feature.

Provenance: [W1_M08:42](_WORK/W1_M08.md); original aliases: M08-F07. Sources: [S174](SOURCES.md#S174).

**[M08-F07](RAW_FACTS.md#F138) [artifact_access_checked; local_test(annotation only); inference] Conditional research extension, not validated production feature.** AVA labels64 `fight/hit (a person)` and76 `push (another person)` are in the actual 60-class evaluation pbtxt (HTTP200,2649 bytes). Validation zip was GET200 downloaded **to memory**, unzipped and parsed locally, 1,611,664 bytes: 243,029 annotation rows, **478 rows of class64 and86 of class76**. These are person-second annotations, not numbers of independent incidents or videos. Example row: video `55Ihr6uVIDA`, timestamp991sec, normalized bbox[.305,.216,.494,.987], action64, person19. Corresponding source identifier URL is https://www.youtube.com/watch?v=55Ihr6uVIDA&t=991s ; **not opened, video availability/content not verified or downloaded**. AVA original page plus MMAction video downloader provide a real video dataset→annotation→SlowFast trained-head path; this is stronger than an image-only “violence detector” lead but still no acquired target video.

CSV is eight scalar columns: video_id,timestamp,x1,y1,x2,y2,action_id,person_id; multiple rows allow simultaneous labels/person tracks. Google original page defines 430 videos (235train/64val/131test),15minutes at1sec annotation intervals, evaluation on included timestamps and exclusions; v2.1 removed duplicate movies and v2.2 adds missed annotations/corrects some extreme-aspect boxes. Exact checked SlowFast weight is **AVA2.1** with author25.80mAP, not AVA2.2; use AVA2.1 split/labels for its published comparison, or explicitly call AVA2.2 a new evaluation. No per-class aggression performance was established. Movie acting/domain shift, close interactions, assisted lifting, balance recovery, friendly contact, tool handoffs and handshakes must be matched negatives. Label “apparent hit/push requiring review”; intent and injury are unobservable.

AVA page explicitly grants dataset CC BY4.0; preserve attribution. Underlying movie/media rights and retrievability are not equated to a blanket clearance to redistribute footage. MMAction Apache2 code is separate from checkpoint publication and source movie rights. Do **not** add a second hazard merely to fill a quota: “heavy carrying” in NTU is already core scenario8 and has no visible mass ground truth; staggering is medically ambiguous and overlaps scenario7.

<a id="F139"></a>
### F139 — W1_M08: Evaluation and unresolved gates

Provenance: [W1_M08:48](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Evaluation and unresolved gates

<a id="F140"></a>
### F140 — W1_M08: M08-F08 [inference] Small-data fine-tuning design.

Provenance: [W1_M08:50](_WORK/W1_M08.md); original aliases: M08-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[M08-F08](RAW_FACTS.md#F140) [inference] Small-data fine-tuning design.** Split by source video/camera/site/actor recording session before generating windows. Keep adjacent and overlapping windows together; avoid random-frame splitting and calibration on test. NTU concurrent three-view captures require the intended cross-subject/cross-view protocol; treat views of one performance as linked if making a custom split. Kinetics CVDF README explicitly warns K400 validation largely overlaps K700 training; never claim independent cross-version testing. AVA-Kinetics includes original AVA videos plus K700 clips and is not automatically an independent holdout from either. Native clip top1, AVA frame-mAP and target event recall/false alerts/hour are different metrics. The directly GET-checked K400 val.csv (HTTP200,810,935 bytes) has header `label,youtube_id,time_start,time_end,split,is_cc`; e.g. first row abseiling,0wR5jVB-WPk,417,427,val,0. These are clip-level source intervals/class labels, not person boxes or industrial onset/offset/policy annotations. The `is_cc` field must not be erased when assembling redistributable source material. The checked K400 video-part list is a real1130-byte metadata list, not acquired videos.

Target evaluation needs episode start/end, actor, scenario/policy status, visibility, “unknown”, camera/source fps and independent annotation adjudication. Report event recall and onset-to-notification latency distribution at a fixed false-alert/hour operating point, plus duplicate counts, missed short transitions and occlusion/identity-reset strata. Use matched normal negatives: walking/fast safe work, bending/kneeling versus fall, resting/maintenance versus immobility, scanner/radio/tool versus phone, authorized locations, near-camera and distant actors. For MoViNet report both cold-start and continuous-prefix conditions; for window methods report stride and accumulated context; for centered AVA model include future acquisition delay.

Remaining unknowns: LinQ model/device/SDK/operators, accepted host/device split, measured RAM including state tensors, binary integrity/full hashes, exact weight-specific license notices, quantized artifact URL, target videos, label budget, local CPU throughput, event threshold/SLA. No inference/export/runtime checker was run. The only `local_test` here is CSV/archive parsing and input-memory arithmetic, not a model or video test.

<a id="F141"></a>
### F141 — W1_M08: Provenance and license boundaries

Provenance: [W1_M08:56](_WORK/W1_M08.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Provenance and license boundaries

MMAction sources below are pinned to **release tag v1.2.0** (release2023-10-12); tag's commit hash was not resolved. TensorFlow/PyTorchVideo/original TSM/VideoMAE sources are moving branches; source snapshots are preserved locally with SHA256 below. GitHub commit/tree API requests returned403, so no invented commit date/hash is supplied. Paper metadata: MoViNets, Kondratyuk/Yuan/Li/Zhang/Brown/Gong2021; X3D, Feichtenhofer2020; TSM, Lin/Gan/Han2019; VideoMAE, Tong et al.2022; STGCN++, Duan et al. PYSKL2022; AVA, Gu et al.2018. Code project licenses: TensorFlow Model Garden Apache2; MMAction Apache2; PyTorchVideo Apache2 (original LICENSE checked). Exact checkpoint-specific grants were **not separately inspected inside archives**; code license alone is not a verified weight-specific license. NTU media/data has original restrictive terms; AVA annotation dataset grants CC BY4; Kinetics annotation/video rights must be checked independently before release. Code/text downloads are research evidence, not model artifacts validated for use.

<a id="F142"></a>
### F142 — W1_M08: Exact downloadable artifact inventory (metadata only unless stated)

Provenance: [W1_M08:86](_WORK/W1_M08.md); original aliases: section record. Sources: [S112](SOURCES.md#S112), [S197](SOURCES.md#S197), [S198](SOURCES.md#S198), [S199](SOURCES.md#S199), [S200](SOURCES.md#S200), [S201](SOURCES.md#S201), [S202](SOURCES.md#S202), [S203](SOURCES.md#S203), [S204](SOURCES.md#S204), [S205](SOURCES.md#S205), [S206](SOURCES.md#S206).

### Exact downloadable artifact inventory (metadata only unless stated)

- https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tar.gz — HEAD HTTP200, length 15165440, accessed 2026-10-23T19:24:58.983270+00:00; no body/model loaded.
- https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tflite — HEAD HTTP200, length 27141832, accessed 2026-10-23T19:24:59.004670+00:00; no body/model loaded.
- https://dl.fbaipublicfiles.com/pytorchvideo/model_zoo/kinetics/X3D_XS.pyth — HEAD HTTP200, length 30779313, accessed 2026-10-23T19:24:59.419639+00:00; no body/model loaded.
- https://download.openmmlab.com/mmaction/v1.0/skeleton/data/ntu60_2d.pkl — HEAD HTTP200, length 705401771, accessed 2026-10-23T19:25:08.726238+00:00; no body/model loaded.
- https://research.google.com/ava/download/ava_v2.2.zip — HEAD HTTP200, length 7721406, accessed 2026-10-23T19:24:58.860793+00:00; no body/model loaded.
- https://research.google.com/ava/download/ava_val_v2.2.csv.zip — HEAD HTTP200, length 1611664, accessed 2026-10-23T19:24:58.847875+00:00; no body/model loaded.
- https://s3.amazonaws.com/kinetics/400/val/k400_val_path.txt — HEAD HTTP200, length 1130, accessed 2026-10-23T19:24:59.165661+00:00; no body/model loaded.
- https://download.openmmlab.com/mmaction/v1.0/skeleton/stgcnpp/stgcnpp_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d/stgcnpp_8xb16-joint-u100-80e_ntu60-xsub-keypoint-2d_20221228-86e1e77a.pth — HEAD HTTP200, length 5859545, accessed 2026-10-23T19:25:08.716407+00:00; no body/model loaded.
- https://download.openmmlab.com/mmaction/v1.0/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb8-8x8x1-20e_ava21-rgb/slowfast_kinetics400-pretrained-r50_8xb8-8x8x1-20e_ava21-rgb_20220906-39133ec7.pth — HEAD HTTP200, length 135802621, accessed 2026-10-23T19:25:11.859705+00:00; no body/model loaded.
- https://download.openmmlab.com/mmaction/v1.0/recognition/tsm/tsm_imagenet-pretrained-r50_8xb16-1x1x8-50e_kinetics400-rgb/tsm_imagenet-pretrained-r50_8xb16-1x1x8-50e_kinetics400-rgb_20220831-64d69186.pth — HEAD HTTP200, length 97651119, accessed 2026-10-23T19:25:08.734372+00:00; no body/model loaded.
- https://download.openmmlab.com/mmaction/v1.0/recognition/videomae/vit-base-p16_videomae-k400-pre_16x4x1_kinetics-400_20221013-860a3cd3.pth — HEAD HTTP200, length 173099345, accessed 2026-10-23T19:25:10.457283+00:00; no body/model loaded.

Evidence files: `_WORK/M08/access*.json`, `artifact_heads.json`, `ava_schema_check.json`; small scripts document exact operations. Failed guessed AVA storage URL403 and wrong raw label path404 are not absence claims; official `/ava/download/` links were subsequently found and checked successfully.

<a id="F143"></a>
### F143 — W1_D09: W1 D09 — industrial video and event-test-pack artifacts

Provenance: [W1_D09:1](_WORK/W1_D09.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D09 — industrial video and event-test-pack artifacts

Branch question: which public industrial/construction sources provide real videos plus actionable action/event annotations, rather than PPE frames, paper figures or workflow-only claims?

Decision: retain Safe/Unsafe Behaviours as the most direct accessible factory CCTV donor; add **SARD v1** as a newly verified real-video/action donor and **Foundation Pit v2** as a verifiable construction scene collection. Neither closes the eight case events without new annotation. **Factory Operation Video Dataset** supplies a concrete 265-second machine-only control candidate, with an unresolved data-license gate. **ENIGMA-360** supplies unusually inspectable temporal procedural annotations, but the checked downloader-generated raw-video URLs fail and the actions are electronics procedures rather than violations. No training, inference, paid services, outreach or large archive downloads were performed.

Access window: 2026-10-23 approximately 19:20–19:35 UTC (22:20–22:35 Moscow). Final clock check 19:34:13 UTC. Read `_WORK/CASE_NOTES.md` and targeted prior report/sibling facts before research. Source revisions below are immutable where available; DOIs/version numbers identify data releases. Local facts mean actual operations executed, never model accuracy.

<a id="F144"></a>
### F144 — W1_D09: D09-F01 — SARD: actual clips, actual tracked action annotations, incomplete packaging claims

Provenance: [W1_D09:9](_WORK/W1_D09.md); original aliases: D09-F01. Sources: [S207](SOURCES.md#S207), [S208](SOURCES.md#S208), [S209](SOURCES.md#S209), [S210](SOURCES.md#S210).

## [D09-F01](RAW_FACTS.md#F144) — SARD: actual clips, actual tracked action annotations, incomplete packaging claims

**[D09-S01](SOURCES.md#D09-S01) / primary_docs:** Chengfeng Wu, *SARD: A Comprehensive Dataset for Construction Site Activity Recognition*, Zenodo v1, published 2026-04-30; record created/modified 2026-05-13. DOI https://doi.org/10.5281/zenodo.19926448 ; metadata endpoint https://zenodo.org/api/records/19926448 . API says CC BY 4.0 and open access. Metadata saved as `D09/sard_record.json`. Author describes core video-level actions and supplementary person-box annotations. FPS/duration/participants/camera-source split are not specified by that metadata.

**artifact_access_checked:** Both server ranges returned HTTP 206 with correct Content-Range. Only final 1,500,000 bytes of each archive were read for complete central-directory inspection; ZIP64 extras were parsed. Whole-archive checksums below are publisher metadata, not locally verified full-download hashes.

| Exact artifact URL | Bytes | Publisher checksum | Inspected members |
|---|---:|---|---|
| https://zenodo.org/api/records/19926448/files/CoreSet.zip/content | 8,250,845,424 | MD5 0302eb8d2af0722a9aa02f578cd03f89 | 760 total entries: 748 MP4/WebM video files, root + 11 class directories |
| https://zenodo.org/api/records/19926448/files/ComplementarySet.zip/content | 35,002,552,520 | MD5 ba5586b6b5badf1987c62d84b876829c | root + `1.mp4`…`9.mp4`, each with corresponding `.txt` |

<a id="F145"></a>
### F145 — W1_D09: D09-F02 / local_test, archive inspection:

Provenance: [W1_D09:20](_WORK/W1_D09.md); original aliases: D09-F02. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D09-F02](RAW_FACTS.md#F145) / local_test, archive inspection:** Core counts by actual video entries: Carry object 52; Climb ladders 47; Hammer nails 51; Install scaffolding 79; Laying bricks 104; Measure 46; Mix concrete 86; Pour concrete 96; Saw 54; Shovel 49; Weld 84. No CSV/JSON/XML/TXT, split file, README, explicit event interval or 27-HOI-category map appears in the complete core manifest. The supplementary archive contains only videos and nine TXT files. The record's statement that splits/definitions are included is therefore **not matched by these two archive manifests**. Could be a missing external asset or implicit folder semantics; not evidence that no author-maintained splits exist anywhere. Saved `CoreSet.zip.manifest.json` and `ComplementarySet.zip.manifest.json` enumerate exact names, compressed sizes, uncompressed sizes, CRC and local-header offsets.

<a id="F146"></a>
### F146 — W1_D09: D09-F03 / local_test, annotation inspection:

Provenance: [W1_D09:22](_WORK/W1_D09.md); original aliases: D09-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D09-F03](RAW_FACTS.md#F146) / local_test, annotation inspection:** Fetched only compressed member `ComplementarySet/4.txt` with HTTP 206 from offset 14,582,488,003, then decompressed locally. Compressed bytes 1,342,805; extracted 5,963,836 bytes; SHA256 `a150bab8aa9d24ae919f8305c7328a45a7383d066d357b68d525f1aeb0315d6e`. Saved `SARD_Complementary_4.txt`. Observed structure is whitespace-separated: frame index, apparent track ID, object type, optional free-text action, final four box coordinates. Example interpreted row: frame 29, track 1, person, `stand(L)`, box `(1446,120,1498,192)`. Non-person entries can have empty action, e.g. helmet; do not parse by a fixed eight-token split because actions contain spaces. Coordinate format inferred as xyxy from values; frame rate and coordinate convention must still be verified against video.

Actual file statistics: 160,824 rows; frame IDs range 1–60,432, only 43,951 unique frame IDs occur. These are annotated-frame IDs, not proof that missing frames have no people. Person rows 49,546; object categories also include vest, helmet, slogan, hopper, hook, board, scaffold, brick and ebox. Person action frequencies: stand(L) 20,920; hold wood(E2b) 10,368; `Unknow` 6,594; hold rope(E3a) 5,991; walk(J) 2,598; carry steel(G2e) 2,408; cut with drill(N1f) 236; lift wood(S2b) 228; sit(K) 150; others less frequent. `Unknow` is 13.31% of person rows. No observed annotation value says unsafe proximity, no harness connection, phone, smoking, running, fall or under suspended load. A hook box is not a load polygon or safety exclusion zone.

<a id="F147"></a>
### F147 — W1_D09: D09-F04 / local_test, small videos actually acquired/decoded:

Provenance: [W1_D09:26](_WORK/W1_D09.md); original aliases: D09-F04. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D09-F04](RAW_FACTS.md#F147) / local_test, small videos actually acquired/decoded:** Two ranged member extractions, CRC checked against ZIP directory, decoded fully with PyAV. Contact sheets visually inspected at five positions each; this is sampled visual review, not dense frame-by-frame event annotation.

| Source member under CoreSet.zip | Local file | Actual media / checksum | What sampled frames establish |
|---|---|---|---|
| `CoreSet/Carry object/Efficient_Brick_Carrying_Tool_in_Action______ConstructionGear__BrickLaying.webm` | `D09/SARD_carry_tool.webm` | 392,686 bytes; 149 decoded frames; 720×1280, 30 FPS; PTS 0–4.933 s; SHA256 `39f1b3e1bd340ceb94b34558ecd444ea666fe62d7fa48785926754730b8b4e67` | A hand uses a handle/tool to lift/carry a bundle of bricks and sets it down. Full torso mostly outside frame; no known mass/procedure. Useful object co-motion/tool confuser, not improper-carrying truth. |
| `CoreSet/Climb ladders/output_0J7uK0isrlU_0_00_0_15.mp4` | `D09/SARD_climb_ladder.mp4` | 370,021 bytes; 450 decoded frames; 720×720, 30 FPS; PTS 0–14.966667 s; SHA256 `45c7096a3428749545fbf366887d8797392214c88e919ef7f5d797770e4192a8` | A person ascends a leaning ladder outdoors beside a commercial building. Useful ladder-action donor. No harness/anchor annotation, calibrated height or observed completed descent. Does not establish the policy violation “working at height without attachment.” |

**inference / split risk:** Names include repeated source IDs and adjacent cuts, e.g. `MNry7eqwc_Q_0_00_0_20.mp4`, `_0_20_0_31.mp4`, `_0_32_0_50.mp4` (exact manifest spelling governs); carry member examples `nWW8Rv2Apr4_0_00_0_14`, `_0_22_0_44`, `_0_45_1_07`, `_1_08_1_23`, `_1_24_end`. Group original source ID before any split; random clip/frame splits can share scene/actor/source content. Web/YouTube-style names and portrait clips mean this is not uniformly factory surveillance. CC BY dataset metadata is explicit, but individual upstream media provenance/releases were not independently resolved. No model/checkpoint is attached to the Zenodo record. Data grant does not license an unrelated action model.

<a id="F148"></a>
### F148 — W1_D09: D09-F05 — Foundation Pit v2: exact 42-video manifest, no packaged video event labels

Provenance: [W1_D09:35](_WORK/W1_D09.md); original aliases: D09-F05. Sources: [S211](SOURCES.md#S211), [S212](SOURCES.md#S212), [S213](SOURCES.md#S213).

## [D09-F05](RAW_FACTS.md#F148) — Foundation Pit v2: exact 42-video manifest, no packaged video event labels

**[D09-S02](SOURCES.md#D09-S02) / primary_docs:** Cheng Zhao, Weiwei Ye, Jinquan Xing, Xingyu Zhang, Jialun Niu, Huiguan Chen, *A Comprehensive Image and Video Dataset for Computer Vision-Based Safety Monitoring in Foundation Pit Construction*, Mendeley Data v2, 2025-11-07, Tongji University. https://data.mendeley.com/datasets/xjm2czccx9/2 ; DOI https://doi.org/10.17632/xjm2czccx9.2 . Exact working API: https://data.mendeley.com/public-api/datasets/xjm2czccx9 . Saved `pit_public_record.json` includes every file ID, URL and publisher SHA256. Version-path variants of that public API returned 404; `/api/datasets/...` misleadingly returned unrelated search results, so those must not be treated as the dataset record. Data license CC BY 4.0, with explicit third-party-content caveat in API. Code/weights not provided by inspected record.

<a id="F149"></a>
### F149 — W1_D09: D09-F06 / artifact_access_checked + local_test archive metadata:

Provenance: [W1_D09:39](_WORK/W1_D09.md); original aliases: D09-F06. Sources: [S214](SOURCES.md#S214), [S215](SOURCES.md#S215), [S216](SOURCES.md#S216), [S217](SOURCES.md#S217).

**[D09-F06](RAW_FACTS.md#F149) / artifact_access_checked + local_test archive metadata:** HTTP 206 supported for all four RARs. A bounded seekable remote reader fetched archive headers while skipping compressed payloads. Read totals 208,624 + 377,948 + 109,745 + 34,254 bytes. Complete parsed manifests saved `pit_Engineering_video1.rar.manifest.json` through `...4...`; **12 + 22 + 6 + 2 = 42 MP4 members**. No event labels/sidecars/JSON/XML files in those four video archives. First 40 have Pexels source names; final two `Donggang-H6-2.mp4` and `Donggang-H6-1 .mp4` (space before extension is real).

| Archive | Exact downloadable URL | Bytes; publisher SHA256 |
|---|---|---|
| Engineering_video1.rar | https://data.mendeley.com/public-files/datasets/xjm2czccx9/files/26755e12-ee6a-47e1-9474-cb4d9dd67782/file_downloaded | 527,281,904; `09ef33f18672d319058dbc225e5a62df1c0782d6478dd6e47fc64cd41a0d7f7e` |
| Engineering_video2.rar | https://data.mendeley.com/public-files/datasets/xjm2czccx9/files/80dac56f-9e6c-4818-aca3-9b15b7854d8c/file_downloaded | 384,549,980; `461b80dd7426ef4bde3170dcd0c13fd4b5d6412ee65cb623045dab2139ca1a93` |
| Engineering_video3.rar | https://data.mendeley.com/public-files/datasets/xjm2czccx9/files/7d4de4a3-424b-4f82-8699-d2902556a8ca/file_downloaded | 529,247,409; `abb44071c450313a383b2f356808e4c741a5cd92b2872c7e52152effc5738b01` |
| Engineering_video4.rar | https://data.mendeley.com/public-files/datasets/xjm2czccx9/files/0ad1f687-abfd-44d6-8848-60ff893bb261/file_downloaded | 723,240,398; `42da270b838478922ec7c010c88c0104d8bd2c044f05db06b0ec7c084f314ede` |

Member-level leads: video1 contains `pexels-kelly-4376239-640x360-24fps.mp4` (2,974,264 uncompressed bytes), video2 `pexels-kira-chats-1350977-1280x720-30fps.mp4` (2,151,000 bytes), video3 `pexels-westarmoney-5098881-1920x1080-60fps.mp4` (4,243,082 bytes). Resolution/FPS embedded in names are **not measured media properties**. No video payload decoded in this source. Total duration, views of individual clips and event eligibility remain unknown.

<a id="F150"></a>
### F150 — W1_D09: D09-F07 / local_test:

Provenance: [W1_D09:50](_WORK/W1_D09.md); original aliases: D09-F07. Sources: [S218](SOURCES.md#S218).

**[D09-F07](RAW_FACTS.md#F150) / local_test:** Downloaded only 1,241-byte `Readme.txt`, SHA256 `8feaeae79ecd3f17af356aebc6158bab0200041b6cb7244d6d70a52a001c56d6`: https://data.mendeley.com/public-files/datasets/xjm2czccx9/files/2addf14d-8865-4684-a5b3-9c4cce502fe0/file_downloaded . It separates image `equipment_classify/distance_mix/Annotations`, `Annotations-json`, `test`, JPEGImages from four video archives. Downloaded `distance_mix.rar` only (1,596,233 bytes), actual SHA256 matches publisher `b8a3d359464ba5292e28f5985f281ed4bfdd3e149df3361c717818bf74958eff`; parsed 3,155 metadata members (XML/JSON and test material), manifest saved. It is not evidence that temporally aligned person–machine annotations accompany the videos. Domain-construction scene diversity is valuable; near-miss/onset/clear/driver labels still require human annotation. Pexels names create a provenance check, not proof that CC BY from the aggregator overrides original stock terms.

<a id="F151"></a>
### F151 — W1_D09: D09-F08 — ENIGMA-360: temporal procedural ground truth, checked raw-video path fails

Provenance: [W1_D09:52](_WORK/W1_D09.md); original aliases: D09-F08. Sources: [S219](SOURCES.md#S219), [S220](SOURCES.md#S220), [S221](SOURCES.md#S221), [S222](SOURCES.md#S222), [S223](SOURCES.md#S223), [S224](SOURCES.md#S224).

## [D09-F08](RAW_FACTS.md#F151) — ENIGMA-360: temporal procedural ground truth, checked raw-video path fails

**[D09-S03](SOURCES.md#D09-S03) / primary_docs:** Ragusa et al., University of Catania and Next Vision, *ENIGMA-360: An Ego-Exo Dataset for Human Behavior Understanding in Industrial Scenarios*, 2026 arXiv 2603.09741. https://fpv-iplab.github.io/ENIGMA-360/ ; https://arxiv.org/abs/2603.09741 ; official repository https://github.com/fpv-iplab/ENIGMA-360 . Git HEAD verified as `2a19221b22d4651250d69dff16902c7fb69eef28` via ls-remote and shallow metadata clone without checking out large assets. Primary description: 180 synchronized ego/exo video pairs (360 videos), procedural industrial laboratory work. Website's separate “360 synchronized pairs” tile is inconsistent with abstract/180+180; count 180 pairs unless authors clarify.

**artifact_found / local_test:** Split files at revision above contain 103 train, 29 val, 48 test IDs; pairwise ID intersections zero. Official `annotations/action_taxonomy.json` contains 68 action IDs. E.g. pressing panel buttons, sitting at workbench, connecting screwdriver battery, turning on power supply, adjusting knobs, using oscilloscope probes. Temporal raw JSON `annotations/raw_json/45.json` contains `video_name`, `clips[].clip_id`, `action_time:[start,end]`, `action_label.id_action` and description. 46 intervals; final end 748.863 s. Gaps and a slight overlap exist; do not assume mutually exclusive exhaustive intervals. `annotations/action_labels/45.txt` contains 22,466 per-frame labels including action_0 and procedural classes; about 30 rows/s is consistent with 748.863 s but **not a local video-FPS measurement**. Unknown/background semantics of action_0 need loader documentation.

**artifact_access_checked:** Root README command `python downloader.py` points to a file actually at `scripts/downloader.py`. Script builds raw URLs as `https://iplab.dmi.unict.it/ENIGMA-360/data/videos/{id}/{id}_third_person.mp4` for fixed-camera view. Bounded GET for exact IDs45 (test) and54 (train) returned HTTP404 for both. No raw ENIGMA video downloaded/decoded. This localizes a failed currently advertised path; it does not prove all videos unavailable. Exact immutable script: https://raw.githubusercontent.com/fpv-iplab/ENIGMA-360/2a19221b22d4651250d69dff16902c7fb69eef28/scripts/downloader.py . Annotated files can be read via equivalent raw revision URLs.

**Rights / primary_docs:** `license.txt` explicitly CC BY-NC 4.0: https://raw.githubusercontent.com/fpv-iplab/ENIGMA-360/2a19221b22d4651250d69dff16902c7fb69eef28/license.txt . This is repository grant evidence; no separate commercial data/checkpoint grant found. Non-commercial use and attribution must be resolved for intended use; public raw availability alone is insufficient. No weight artifact verified. Suitable research for temporal segmentation or normal seated/tool-handling confusers, not a labeled factory near-miss/fall/phone/attachment safety benchmark. Keep paired views of one ID in one split, and confirm subject/procedure independence before claiming unseen-worker generalization.

<a id="F152"></a>
### F152 — W1_D09: D09-F09 — long printing-factory control: one real 265s clip and exact annotation join

Provenance: [W1_D09:62](_WORK/W1_D09.md); original aliases: D09-F09. Sources: [S225](SOURCES.md#S225), [S226](SOURCES.md#S226), [S227](SOURCES.md#S227), [S228](SOURCES.md#S228).

## [D09-F09](RAW_FACTS.md#F152) — long printing-factory control: one real 265s clip and exact annotation join

**[D09-S04](SOURCES.md#D09-S04) / primary_docs:** Shotaro Kataoka, Tetsuro Ito, Genki Iwaka, Masashi Oba, Hirofumi Nonaka, *Improving work detection by segmentation heuristics pre-training on factory operations video*, PLOS ONE, 2022-06-07, DOI10.1371/journal.pone.0267457. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0267457 . Authors describe 30h, three days, one fixed printing-factory camera/operator, 12 work labels per second; chronological train day1+day2 morning, val day2 afternoon, test day3. Their model uses 100 frames at1FPS (100s context), so its published work-class result is not a few-second safety-alert benchmark. Paper's CC BY license is not a verified video-data grant. Dataset https://www.kaggle.com/datasets/shotarokataoka/factory-oparation-video-dataset ; API metadata version1 last updated 2022-04-21, `licenseName:"Unknown"`. Code https://github.com/ShotaroKataoka/WorkDetectionFactoryPretrain ; README has data/example Google Drive links but no locally verified weight/license chain.

**artifact_access_checked:** Unauthenticated Kaggle file-list API works: https://www.kaggle.com/api/v1/datasets/list/shotarokataoka/factory-oparation-video-dataset . First page enumerates results CSV/NPZ, three daily annotation CSVs, and dated MP4s. Pagination token exists; full dataset count not enumerated. Whole-dataset API size fields disagree (~6.40GB search vs6.64GB view), so use exact individual sizes.

<a id="F153"></a>
### F153 — W1_D09: D09-F10 / local_test:

Provenance: [W1_D09:68](_WORK/W1_D09.md); original aliases: D09-F10. Sources: [S229](SOURCES.md#S229).

**[D09-F10](RAW_FACTS.md#F153) / local_test:** Exact small file download works:

https://www.kaggle.com/api/v1/datasets/download/shotarokataoka/factory-oparation-video-dataset/Factory%20Operation%20Video%20Dataset%2Fvideos%2F20180903%2F072733.mp4?datasetVersionNumber=1

GET200 returns a ZIP (8,426,422 bytes), not direct MP4. Member `072733.mp4` is 8,434,463 bytes, SHA256 `54c3b0d505ba3e16ec46e1bd27bcbea1d64621d4e4a8fc853700e30948f65bfd`. Fully decoded3975 frames, 640×480,15FPS; firstPTS0, lastPTS264.933333s (265s nominal duration). Saved `factory_072733.mp4`; six sampled visual frames show the printing machine/empty work area, not a person or incident. Not dense visual review of all frames.

Corresponding annotation endpoint replaces suffix with encoded `Factory Operation Video Dataset/video_operation_label_20180903.csv`. HTTP206 first65,536 compressed bytes of its ZIP yielded8,136 complete CSV rows through incremental deflate, sufficient for all3,975 frames of this MP4. Saved exact compressed prefix and decoded CSV prefix. Schema: index, video_path, id, all_frames_path, label, work_desc, hour,minute,second. **All3,975 rows matched by `all_frames_path` prefix `20180903/072733/` have label12, `Nonhuman work`.** `video_path` varies within that clip and starts `20180903/072732`, so a naive join on video_path would fail; use validated all_frames_path/video mapping and timestamps. Prefix first image annotation clock07:27:32, last07:31:57 agrees with overlay and265s wall time within frame clock quantization.

**Decision / inference:** candidate long routine-machine/no-human control for spurious person/action alarms, with real duration for alarms/hour denominators after complete review and rights resolution. It cannot certify all eight safety negatives: no risk-policy annotation, no pedestrian–vehicle pair, and one scene/operator does not cover real industrial diversity. Do not redistribute in final public demo solely because the article is CC BY. Data rights remain unknown rather than prohibited by inference.

<a id="F154"></a>
### F154 — W1_D09: D09-F11 — retain accessible Safe/Unsafe factory CCTV without relabeling overload as near-miss

Provenance: [W1_D09:78](_WORK/W1_D09.md); original aliases: D09-F11. Sources: [S230](SOURCES.md#S230), [S231](SOURCES.md#S231), [S232](SOURCES.md#S232), [S233](SOURCES.md#S233).

## [D09-F11](RAW_FACTS.md#F154) — retain accessible Safe/Unsafe factory CCTV without relabeling overload as near-miss

**[D09-S05](SOURCES.md#D09-S05) / primary_docs + artifact_access_checked:** Oğuzhan Önal and Emre Dandıl, Mendeley v1, published2024-06-11: https://data.mendeley.com/datasets/xjmtb22pff/1 ; https://data.mendeley.com/public-api/datasets/xjmtb22pff . Fresh API inspection confirms691 individual MP4s,566 `_tr` and125 `_te`; eight filename-prefix groups. CC BY4.0 in `data_licence` and third-party caveat; saved complete `safe_unsafe_record.json` with per-file publisher SHA256. Actual videos from factory security cameras are the direct target-domain advantage. Author paper describes 1–20s clips, two fixed cameras, eight walkway/intervention/panel/forklift-load safe/unsafe labels. No fresh payload decode in this branch; sibling decoding remains separate evidence.

Preserved exact original-host download paths (both fresh GET Range206):

- `3_te1.mp4`,24,506,317 bytes,publisher SHA256 `79c298ce0cb0eaa9a920285dce299dadc25ebfc737bf1f058c981f6bc2e23517`: https://data.mendeley.com/public-files/datasets/xjmtb22pff/files/5df42fde-34c9-48e7-ad06-d1b99c608cbe/file_downloaded .
- `7_te1.mp4`,4,458,655 bytes,publisher SHA256 `d99184fd5b7e3430bf31a31e3080a843e03dbdd4625828c81ffef97417a9a6b6`: https://data.mendeley.com/public-files/datasets/xjmtb22pff/files/87fb7e29-90ef-4eee-9501-d9e40ba38a2f/file_downloaded .

Load compliance does not encode worker–moving-machine proximity. Small trimmed clips censor pre-onset/post-clear and contain same-camera/background shortcuts. Keep camera/day/overlapping-episode groups separate; original train/test naming alone does not establish temporal/actor independence. Use walkway safe/unsafe pair for a declared scene rule; do not claim it solves fence climbing, crawling under conveyor or under suspended load.

<a id="F155"></a>
### F155 — W1_D09: D09-F12 — paper-only / gated / frame-only distinctions and changed access claim

Provenance: [W1_D09:89](_WORK/W1_D09.md); original aliases: D09-F12. Sources: [S234](SOURCES.md#S234), [S235](SOURCES.md#S235), [S236](SOURCES.md#S236).

## [D09-F12](RAW_FACTS.md#F155) — paper-only / gated / frame-only distinctions and changed access claim

**[D09-S06](SOURCES.md#D09-S06) / primary_docs:** Official Meng Yang et al. CMA repository https://github.com/S1mpleyang/ConstructionActionRecognition , README https://raw.githubusercontent.com/S1mpleyang/ConstructionActionRecognition/main/README.md . 2023 paper DOI10.1016/j.autcon.2022.104703; 2024 low-resolution follow-up DOI10.1016/j.aei.2023.102294. Current README announces1595 clips/seven actions via https://pan.baidu.com/s/1Qjrc5AcZePxvSJ4jYT2pvA , extract code `z7a2`; earlier email request paragraph is now HTML-commented. Thus “CMA only by author email” is stale relative to official current repository. No Baidu archive/actual classes/splits acquired here; no claim of readiness. README restricts dataset to research/non-commercial; custom research/education/attribution repository language, not an assumed MIT/Apache grant. Google Drive pretrain link is present, but pretrain ≠ verified CMA safety checkpoint. Exact code/data/model grants and artifact remain unresolved.

CAAR (already primary-checked in prior branch) remains academic access/no redistribution rather than absent; Open-Site harness paper's four videos remain a paper claim without acquired payload/grant; generic Roboflow construction safety is PPE/image evidence. Those do not count as newly available temporal event packs. iSafetyBench and synthetic NVIDIA warehouse/event collections are covered elsewhere; no duplication or upgrading of their domain/rights/annotation status here.

<a id="F156"></a>
### F156 — W1_D09: D09-F13 — concrete test-pack admission and causal/censoring limits

Provenance: [W1_D09:95](_WORK/W1_D09.md); original aliases: D09-F13. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D09-F13](RAW_FACTS.md#F156) — concrete test-pack admission and causal/censoring limits

| Case scenario | New usable lead | Missing truth / hard negatives required |
|---|---|---|
| #1 running | SARD4.txt walk/stand tracks as ordinary-action donor; no run value in inspected member | Need actual run transition/speed policy and fast-walk/camera-motion controls. Pixel displacement ≠ metric speed. |
| #2 moving-machine proximity | Safe/Unsafe originals +42 foundation scene clips; factory machine-only265s control | Need pair identities, observed machine motion, entering/remaining/exiting configured area. Driver/rider, stationary-near, moving-far, occluded-feet controls. Object overlap or hook proximity ≠ meters/TTC. |
| #3 phone | ENIGMA procedure/tool-handling prospective confusers, but checked video paths404 | No inspected phone-use labels or phone/face owner association. Require equipment context versus walking, tool/radio/drink controls. |
| #4 smoking/fire | SARD Weld84 clips are potential permitted-hot-work visual confusers | Weld folder ≠ flame/unsafe open-fire ground truth; no video of that folder decoded. Need site permission/hot-work zones, smoke-only/steam/reflection controls. |
| #5 barriers/underload | SARD ladder/scaffold action donors; supplementary hook/person tracks | Ladder ascent ≠ fence crossing. Need complete actor route, barrier geometry, load motion/footprint; no suspension/underload truth. |
| #6 height/harness | acquired SARD15s ladder clip is concrete gross-action donor | No reliable absent/present/connected/other-person tether annotation or calibrated working surface. Occlusion ≠ no harness. |
| #7 fall/immobility | factory long routine control only; no new fall positives | No industrial fall→lying→continuous-visible-low-motion positive; cannot substitute cut/unknown frames for observed immobility. |
| #8 improper carrying | acquired brick-tool clip + SARD carry steel/lift wood labels | No mass, task rule or approved handling procedure; carry action/box size does not imply violation. Need set-down/regrasp/one-vs-two-carrier controls. |

**Recommended next artifact work (no new model required):** admit the two SARD decoded samples only into development review, label onset/offset/visibility and source/rights explicitly; keep them out of blind holdout. Use original Safe/Unsafe camera-specific safe/unsafe pairs after the sibling identity closure. Resolve factory data rights and review the entire265s clip before calling it a negative. For a real pack require source_id/camera_id/episode_id, source PTS, actor/pair IDs, event onset/confirmation/clear, visibility states, left/right censoring and known site rule. Each event with one notification and rearm must be evaluated over continuous footage; trimmed clips at EOF do not prove clearance/rearm, and a cropped ladder clip cannot prove descent or attachment status.

**Do not sample1FPS first and then score only retained frames.** Preserve full source PTS/video for event annotation, then simulate causal sampling/dropouts at inference. An event shorter than cadence can disappear at some sampling phases; that is an evaluation failure case, not an absent event. Unknown labels/gaps remain unknown. Measure event recall, false alerts per fully reviewed eligible hour and duplicate-alert count; clip action accuracy on these sources does not supply industrial alarm performance or LinQ device evidence.

<a id="F157"></a>
### F157 — W1_D09: Evidence inventory and unresolved gates

Provenance: [W1_D09:112](_WORK/W1_D09.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Evidence inventory and unresolved gates

Small acquired media: SARD392,686-byte carry +370,021-byte ladder; factory8,434,463-byte MP4. Additional downloaded archives: only1.596MB image annotation RAR. Large SARD ZIPs/foundation RARs were inspected with bounded byte ranges, not fully downloaded. Publisher hashes explicitly distinguished from actual computed sample hashes. No neural model executed; no claims of LinQ compatibility/FPS/accuracy.

Private evidence directory `_WORK/D09/` holds source JSON, complete archive manifests, range tails/header samples, extracted sample TXT/CSV prefixes, decoded small media and contact sheets. ENIGMA shallow no-checkout repository holds exact tree/history snapshot and selected annotation blobs. A failed cv2 import was replaced with available PyAV; no package installation was needed.

Open gates: (1) SARD official split/27-HOI definition location and source-media releases; (2) SARD supplementary video4 actualFPS, box convention and ID continuity; (3) foundation camera/source provenance and whether temporally aligned annotation exists outside the four checked archives; (4) ENIGMA current valid raw-video path and commercial scope; (5) printing-factory dataset reuse grant; (6) exact CMA Baidu manifest/splits/classes and release permissions; (7) none of these artifacts establishes complete multi-scenario, continuous, real-factory safety-event holdout.

<a id="F158"></a>
### F158 — W1_D10: W1 D10 — fall, lying and immobility data: temporal semantics, negatives, acquisition and splits

Provenance: [W1_D10:1](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D10 — fall, lying and immobility data: temporal semantics, negatives, acquisition and splits

Research/access date: **2026-10-23**, final clock check **19:24:02 UTC**. Branch question: which source datasets can support a reviewable temporal fall/lying experiment, with actual negatives and grouping, rather than an accidentally inflated frame classifier? No model execution, training, video playback, full video/archive download, access request or outreach was performed. Small annotation CSVs, documentation PDFs, HTML and metadata were retrieved. `local_test` below means parsing those files only.

<a id="F159"></a>
### F159 — W1_D10: Decision

Provenance: [W1_D10:5](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Decision

<a id="F160"></a>
### F160 — W1_D10: D10-F01 [inference]

Provenance: [W1_D10:7](_WORK/W1_D10.md); original aliases: D10-F01. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D10-F01](RAW_FACTS.md#F160) [inference]** Use **URFD camera 0** for a bounded source-level ingestion/semantics test, **UP-Fall** for a subject-disjoint temporal evaluation when its raw images and labels are obtained, and **Montreal MCF** for confounding-action and view stress tests when use rights are established. All three remain staged indoor data, not a validation set for industrial CCTV. Keep fall event, lying state, and immobility duration as separate targets. None establishes unconsciousness or a safe operational alarm threshold.

<a id="F161"></a>
### F161 — W1_D10: D10-F02 [artifact_access_checked]

Provenance: [W1_D10:9](_WORK/W1_D10.md); original aliases: D10-F02. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D10-F02](RAW_FACTS.md#F161) [artifact_access_checked]** A materially useful correction to prior work: Montreal is **not uniformly inaccessible**. The web browsing tool returned an Anubis access page, but ordinary bounded Python HTTPS requests returned the original index and PDFs and genuine ZIP response headers. This is an access-path difference, not evidence that videos were downloaded or inspected. The index includes a 2025 erratum that is essential before transferring time labels across cameras.

<a id="F162"></a>
### F162 — W1_D10: D10-F03 [local_test + primary_docs]

Provenance: [W1_D10:11](_WORK/W1_D10.md); original aliases: D10-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D10-F03](RAW_FACTS.md#F162) [local_test + primary_docs]** URFD's ADL feature file contains **1,470 lying-labelled rows in 16 non-fall sequences**. Consequently, the row label `+1` cannot be reinterpreted as a fall event. These are an unusually useful, explicitly traceable hard-negative pool. Full findings below.

<a id="F163"></a>
### F163 — W1_D10: URFD: event-negative recordings can contain lying people

Provenance: [W1_D10:31](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## URFD: event-negative recordings can contain lying people

<a id="F164"></a>
### F164 — W1_D10: D10-F04 [primary_docs; S01]

Provenance: [W1_D10:33](_WORK/W1_D10.md); original aliases: D10-F04. Sources: [S237](SOURCES.md#S237).

**[D10-F04](RAW_FACTS.md#F164) [primary_docs; S01]** URFD has 30 fall and 40 ADL recordings. Camera 0 is parallel to the floor; camera 1 is ceiling mounted and exists only for falls. Images are stored as per-camera PNG ZIPs. Views use nearest timestamps rather than exact synchronized exposure. Feature rows describe a depth-frame posture: `-1` nonlying, `0` transient falling pose, `+1` lying on ground; the documented original posture classification excludes `0`. Dataset licence is **CC BY-NC-SA4.0**, explicitly noncommercial academic; commercial permission is a separate gate. Subject identities and an official subject-disjoint split were not established from this page.

<a id="F165"></a>
### F165 — W1_D10: D10-F05 [local_test; S02]

Provenance: [W1_D10:35](_WORK/W1_D10.md); original aliases: D10-F05. Sources: [S238](SOURCES.md#S238), [S239](SOURCES.md#S239).

**[D10-F05](RAW_FACTS.md#F165) [local_test; S02]** Parsed downloaded CSVs with Python `csv`, grouping by sequence column. Files have no header; 11 fields: sequence, frame, posture, eight depth-derived features. Counts:

| File | Recordings | Rows | `-1` | `0` | `+1` |
|---|---:|---:|---:|---:|---:|
| falls | 30 | 2,995 | 1,192 | 900 | 903 |
| ADLs | 40 | 8,549 | 6,260 | 819 | 1,470 |

ADLs with `+1`: **adl-10, adl-11, adl-21, adl-22, adl-23, adl-30 through adl-40**. Saved complete per-sequence transitions in `urfall-cam0-adls.csv.summary.json`. Example: adl-10 begins at frame 1 with `-1`, changes to `0` at frame 170 and `+1` at frame 200. Fall-01 changes to `0` at 83 and `+1` at 113. Frame coverage can start after 1 (e.g. adl-01 starts at 6); therefore do not fill omitted rows with a negative label or assume annotation row index equals image frame index. All 30 fall recordings have exactly 30 transient rows; this regularity is a **label-generation audit flag**, not verified physical duration of each fall.

<a id="F166"></a>
### F166 — W1_D10: D10-F06 [inference]

Provenance: [W1_D10:44](_WORK/W1_D10.md); original aliases: D10-F06. Sources: [S253](SOURCES.md#S253), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255).

**[D10-F06](RAW_FACTS.md#F166) [inference]** Use original recording category to identify event negatives and row posture to test lying discrimination. Preserve `0` as a temporal state and report performance around it. A static classifier trained only on `-1` vs `+1`, then called “fall detection,” is evaluating a different task. Some ADL `0` labels demonstrate that the transient-code name alone does not establish a true accident. The exact actions in each negative require video review, which was not performed.

Verified artifact endpoints (stream opened, headers checked, video body not acquired):

| Artifact | Exact URL | Result |
|---|---|---|
| Raw fall RGB PNG ZIP | https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0-rgb.zip | HTTP200 application/zip, Content-Length **57,727,213** |
| Candidate lying negative MP4 | https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4 | HTTP200 video/mp4, **2,472,849** bytes advertised; not watched |
| Synchronization CSV | https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-data.csv | HTTP200 text/csv, **2,856** bytes acquired; sample first rows `1,0`, `2,31`, `3,62` |

<a id="F167"></a>
### F167 — W1_D10: D10-F07 [inference]

Provenance: [W1_D10:54](_WORK/W1_D10.md); original aliases: D10-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D10-F07](RAW_FACTS.md#F167) [inference]** The two-column synchronization artifact should govern mapping camera-0 frame index to milliseconds for adl-10 rather than an assumed universal FPS. Never project camera-0 depth labels onto camera1 by identical frame number. Never include camera1-only falls with camera0 negatives in a purported balanced view test: viewpoint becomes correlated with class.

<a id="F168"></a>
### F168 — W1_D10: UP-Fall: dense original state labels and a real person split

Provenance: [W1_D10:56](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## UP-Fall: dense original state labels and a real person split

<a id="F169"></a>
### F169 — W1_D10: D10-F08 [primary_docs / author_claim; S03]

Provenance: [W1_D10:58](_WORK/W1_D10.md); original aliases: D10-F08. Sources: [S240](SOURCES.md#S240), [S241](SOURCES.md#S241).

**[D10-F08](RAW_FACTS.md#F169) [primary_docs / author_claim; S03]** This is staged data from 17 healthy young adults in a controlled room; falls used a mattress. Two fixed frontal/lateral cameras are about 1.82m high; consolidated sampling is roughly 18.4Hz. Trial CSVs contain timestamps, sensor channels and subject/activity/trial identifiers; PNG filenames are timestamps. Crucially the activity column changes within fall trials among standing, falling and lying; picking-up trials also change state. Fall tags were manually inspected, ADLs tagged from times. Thus **folder activity is not frame truth**. Negative activities include walking, standing, sitting, picking up an object, jumping and deliberate lying. These provide a useful counterexample to “horizontal person = fall.” This paragraph summarizes original conditions, not measured deployment performance.

<a id="F170"></a>
### F170 — W1_D10: D10-F09 [primary_docs; S04]

Provenance: [W1_D10:60](_WORK/W1_D10.md); original aliases: D10-F09. Sources: [S242](SOURCES.md#S242).

**[D10-F09](RAW_FACTS.md#F170) [primary_docs; S04]** Storage keys are subject/activity/trial, with a camera image ZIP for each view. Official page declares subject8/activity11/trials2–3 missing. Complete sensor downloads, optical-flow features and raw camera images are distinct products. A downloaded feature CSV or preliminary four-person sensor set does not constitute ready video input. Source page says publicly available and requests citation, but a clear reusable dataset licence covering raw images was **not found in inspected primary material**. Article CC BY status does not itself settle image-data rights.

<a id="F171"></a>
### F171 — W1_D10: D10-F10 [primary_docs; S05]

Provenance: [W1_D10:62](_WORK/W1_D10.md); original aliases: D10-F10. Sources: [S243](SOURCES.md#S243).

**[D10-F10](RAW_FACTS.md#F171) [primary_docs; S05]** The 2020 vision competition explicitly defines **train subjects1–12 / test subjects13–17**. Both cameras stay with their subject. Inputs are full frame sequences, not presegmented clips. Its metric builds 3-second windows with 50% overlap, labelled by the most frequent tag, resolving equal counts by the first tied tag. Some subjects have incomplete information. Treat this as a reproducible **historical classification protocol**, not an alarm-latency or industrial-safety SLA.

<a id="F172"></a>
### F172 — W1_D10: D10-F11 [inference]

Provenance: [W1_D10:64](_WORK/W1_D10.md); original aliases: D10-F11. Sources: [S244](SOURCES.md#S244), [S245](SOURCES.md#S245), [S256](SOURCES.md#S256), [S257](SOURCES.md#S257).

**[D10-F11](RAW_FACTS.md#F172) [inference]** Retain that person split as the first reproducible protocol, with validation subjects taken solely from1–12. Split before generating windows. The majority label can erase a short fall inside a window; add event recall and time-to-first-alarm evaluated on full timestamped sequences. Do not tune threshold or dwell time on13–17. Camera holdout of the same trial is not independent person/event generalization.

Actual access check for S06: direct URLs `https://drive.google.com/uc?export=download&id=1kq2qhQlzKbsobOUiqA4pRY83hoV3MhBT` and `https://drive.google.com/uc?export=download&id=1XJ61-FQ_2PMoEPdNVK5PblkEbXEetBx1` redirected to drive.usercontent.google.com and returned **HTTP200 text/html**, 2,040 and 2,475 bytes respectively, titled **Google Drive - Quota exceeded**. Local files keep original names but are HTML error responses, not executable Python or a usable ZIP. No retry-bypass, credentials, download API project or account was created. Raw image file-level availability remains unverified, not disproved.

<a id="F173"></a>
### F173 — W1_D10: Montreal MCF: exact temporal corrections and difficult confounds

Provenance: [W1_D10:68](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Montreal MCF: exact temporal corrections and difficult confounds

<a id="F174"></a>
### F174 — W1_D10: D10-F12 [primary_docs; S07]

Provenance: [W1_D10:70](_WORK/W1_D10.md); original aliases: D10-F12. Sources: [S246](SOURCES.md#S246), [S247](SOURCES.md#S247).

**[D10-F12](RAW_FACTS.md#F174) [primary_docs; S07]** MCF uses eight wide-angle IP cameras, one actor, staged falls with mattress. Nine interval states distinguish walking/standing, falling, lying on ground, crouching, moving down/up, sitting, sofa lying and horizontal movement. Schema is scenario/reference-camera/start-frame/end-frame/state. Same physical event appears in every camera. Confounds include chair/sofa occlusion, carrying, coat changes and housekeeping; compressed imagery, shadows and reflections are intentional difficulties. Keep every view of a scenario in one partition. A person-disjoint test within this dataset is impossible because it has one subject.

<a id="F175"></a>
### F175 — W1_D10: D10-F13 [primary_docs; S08]

Provenance: [W1_D10:72](_WORK/W1_D10.md); original aliases: D10-F13. Sources: [S248](SOURCES.md#S248).

**[D10-F13](RAW_FACTS.md#F175) [primary_docs; S08]** The 2025 erratum corrects reference cameras **11→8**, **10→7**, and scenario5/camera5 delay **“18 7”→18**. Corrected intervals, in the same state order as original report:

| Scenario / reference camera | Corrected frame ranges |
|---|---|
| 2 / 4 | 308–394; 395–425; 426–600 |
| 7 / 6 | 330–490; 491–520; 521–680 |
| 8 / 4 | 144–350; 351–380; 381–520 |
| 14 / 6 | 372–590; 591–620; 621–929; 930–969; 970–1019; 1020–1060; 1061–1115 |
| 18 / 6 | 301–480; 481–520; 521–655; 656–684; 685–710; 711–740 |

<a id="F176"></a>
### F176 — W1_D10: D10-F14 [primary_docs + inference; S07,S08]

Provenance: [W1_D10:82](_WORK/W1_D10.md); original aliases: D10-F14. Sources: [S246](SOURCES.md#S246), [S247](SOURCES.md#S247), [S248](SOURCES.md#S248).

**[D10-F14](RAW_FACTS.md#F176) [primary_docs + inference; S07,S08]** Important unresolved source contradiction: the index describes scenarios23–24 as confounding-only, while report p.21 assigns state2 (falling) to scenario23 intervals **1520–1595** and **3574–3614**, without a subsequent ground-lying state. Scenario24 has no state2 in its table. The erratum does not resolve this. Do not blindly classify all scenario23 frames as negative or relabel it positive; inspect the source footage and document the intended event definition. Original camera11 in that scenario is camera8 after erratum.

<a id="F177"></a>
### F177 — W1_D10: D10-F15 [artifact_access_checked]

Provenance: [W1_D10:84](_WORK/W1_D10.md); original aliases: D10-F15. Sources: [S258](SOURCES.md#S258), [S259](SOURCES.md#S259), [S260](SOURCES.md#S260).

**[D10-F15](RAW_FACTS.md#F177) [artifact_access_checked]** Verified through bounded streaming GET then closed response; ZIP payloads not saved:

| Artifact | Exact URL | Genuine response header |
|---|---|---|
| Full MCF | https://www.iro.umontreal.ca/~labimage/Dataset/dataset.zip | HTTP200 application/zip; **3,782,815,282** bytes |
| Scenario23 | https://www.iro.umontreal.ca/~labimage/Dataset/chute-zip/chute23.zip | HTTP200 application/zip; **647,752,573** bytes |
| Scenario24 | https://www.iro.umontreal.ca/~labimage/Dataset/chute-zip/chute24.zip | HTTP200 application/zip; **448,528,874** bytes |

The exact per-scenario link pattern is enumerated by the publisher index, not guessed as evidence. No explicit reuse licence was identified on that index or the inspected documentation. Citation request is not a commercial licence. **Data rights remain a gate.** Code and weight licences are not applicable to this source dataset; there is no candidate executable or weight artifact evaluated in this branch.

<a id="F178"></a>
### F178 — W1_D10: Le2i and derived UP-Fall: localized gaps, not invented readiness

Provenance: [W1_D10:94](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Le2i and derived UP-Fall: localized gaps, not invented readiness

<a id="F179"></a>
### F179 — W1_D10: D10-F16 [artifact_access_checked / unknown; S10]

Provenance: [W1_D10:96](_WORK/W1_D10.md); original aliases: D10-F16. Sources: [S250](SOURCES.md#S250).

**[D10-F16](RAW_FACTS.md#F179) [artifact_access_checked / unknown; S10]** Original ImViA URL returned404. Search found widely reused Kaggle and GitHub conversions and inconsistent counts/annotation coverage; they do not establish original rights or canonical frame truth. A third-party upload's CC BY claim cannot grant rights to original videos. Le2i remains a lead requiring a specific release inventory, original annotation README, actor mapping and rights chain before recommending acquisition. This report intentionally does not turn secondary claims of 191/221/249 videos into a verified count. Nor does it claim Le2i ceased to exist.

<a id="F180"></a>
### F180 — W1_D10: D10-F17 [primary_docs / artifact_access_checked; S11]

Provenance: [W1_D10:98](_WORK/W1_D10.md); original aliases: D10-F17. Sources: [S251](SOURCES.md#S251), [S252](SOURCES.md#S252), [S261](SOURCES.md#S261).

**[D10-F17](RAW_FACTS.md#F180) [primary_docs / artifact_access_checked; S11]** The Zenodo derivative has only five subjects and excludes sequences with fewer than100 extracted pose frames. It targets **impact** via binary `LABEL`, not fall onset or sustained immobility. API gives CC BY4.0 and these exact files: SUBJECT1.zip941,750; SUBJECT2.zip1,109,223; SUBJECT3.zip941,900; SUBJECT4.zip249,792; SUBJECT5.zip778,011 bytes. Example actual endpoint: https://zenodo.org/api/records/12773013/files/SUBJECT1.zip/content . API metadata was acquired; ZIP content not acquired. It is a small annotation/pose baseline lead, not substitute CCTV RGB. GitHub's README has a five-subject vs 9-male/8-female inconsistency and reverses original competition camera-view descriptions; rely on original camera metadata until independently checked. Derived skeletons from original trials must not count as an independent external test of a model trained on their source images.

<a id="F181"></a>
### F181 — W1_D10: Split and evaluation contract for this branch

Provenance: [W1_D10:100](_WORK/W1_D10.md); original aliases: section record. Sources: [S248](SOURCES.md#S248).

## Split and evaluation contract for this branch

The following are **D10-F18 [inference / proposed experiment]**, not claims of an existing published benchmark:

1. Build a manifest before feature extraction: dataset release, original subject, room/layout, session/date, source recording, physical event, view, source frame/timestamp, label source/revision, parent original and hash. Preserve “unknown subject” explicitly; do not derive actor identity from filenames or face appearance without documented mapping.
2. Group URFD by **fall/adl recording stem**, linking both views and all derivatives. If actor mapping later becomes available, regroup by actor; until then label the result recording-disjoint rather than subject-disjoint. Reserve camera0 for fall-vs-ADL comparisons. Use camera1 only for clearly labelled view analysis.
3. Group UP-Fall by subject for the official split. Keep trial and its two views and all overlapping windows together. Validation comes from training people only. Hold out complete rooms/sites in a later external set because the subject split still shares a laboratory.
4. Group MCF by scenario across all eight cameras. It supports recording/view robustness within one actor and scene. Do not advertise scene/person generalization. Keep scenario23 ambiguous until reviewed and include corrected camera delays and intervals from S08 in the manifest.
5. Keep a source-family registry across OmniFall, URFD, MCF, UP-Fall, pose derivatives, flipped clips, resized images, extracted frames and annotations. A derivative or reannotation is not an independent dataset. Exclude source ancestors of test recordings from training, retrieval exemplars and threshold tuning. Exact hashes plus near-duplicate temporal fingerprints support this audit; they were not computed for video in this branch.
6. Split raw groups first, then generate causal windows. Sliding windows from the same recording never cross partitions. Each output timestamp may use only frames already observed. Preserve chronological timestamps; avoid centred windows and future majority labels for an online result. Report window classification separately if reproducing the competition metric.
7. Evaluate event detection with event recall, false alarms per camera-hour and first-alarm delay distribution. Separately evaluate frame lying precision/recall, episode duration errors and track gaps. Report transitions and occluded intervals rather than silently dropping hard frames. Do not set an acceptable maximum delay without the case owner; no numerical SLA was established.
8. Record negative classes deliberately: controlled lying/down-and-up; kneeling/crouching/bending to pick items; sit/stand transfers; jumping; work on floor; maintenance under machinery; obscured lower body; person entering/exiting; camera motion, frozen stream or lost track. The first classes are source-supported leads above; industrial maintenance, frozen-stream controls and long natural inactivity are **hypothesis / collection needs**, not claimed contents of these datasets.

<a id="F182"></a>
### F182 — W1_D10: Gates and handoff

Provenance: [W1_D10:113](_WORK/W1_D10.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Gates and handoff

<a id="F183"></a>
### F183 — W1_D10: D10-F19 [inference]

Provenance: [W1_D10:115](_WORK/W1_D10.md); original aliases: D10-F19. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D10-F19](RAW_FACTS.md#F183) [inference]** Start with the two acquired URFD annotation CSVs and an agreed scope for its NC licence. Review adl-10 first when authorized footage review begins. For UP-Fall, acquire a small complete subject/activity/trial bundle containing original timestamp labels plus both views and confirm raw-image rights before scaling. For MCF, use the erratum and resolve scenario23 rather than copying online split recipes. Do not download the3.8GB aggregate merely to establish availability.

Unresolved: original actor IDs for URFD; exact negative action semantics without playback; UP-Fall raw trial binary access and raw-image licence; MCF commercial/reuse terms and scenario23 interpretation; Le2i canonical release/annotations/rights; source-alias membership in any OmniFall-derived model's training; industrial camera-height/occlusion/clothing shift; long-duration natural immobility negatives. No dataset here provides a validated label for consciousness, industrial injury or need for rescue.

Reproduction evidence: `access.json`, `access2.json`, `mcfd_access.json`, `urfall-cam0-*.csv`, their `.summary.json` files, `adl-10-data.csv`, `zenodo12773013.json`, `mcfd-index.html`, `technicalReport.pdf`, `Erratum-MCF.pdf` and extracted `.txt` under `_WORK/evidence_D10/`. A temporary script was renamed from `inspect.py` to `parse_metadata.py` because its filename shadowed Python's standard-library inspect module; no model test was involved.

<a id="F184"></a>
### F184 — W1_D11: W1 D11 — Independent CCTV walk/run evidence and evaluation limits

Provenance: [W1_D11:1](_WORK/W1_D11.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D11 — Independent CCTV walk/run evidence and evaluation limits

Research access: 2026-10-23 19:37–19:42 UTC (22:37–22:42 Moscow). Scope: scenario 1, running/abrupt movements; independent alternatives to M04 CAVIAR/KTH. Read complete assigned prompt, Context-prompt.md, CASE_NOTES.md and relevant prior feasibility running section. No training, inference, paid computation, outreach or large archives. Only one new video acquired, 16,867,976 bytes. Evidence directory `_WORK/D11/`; scripts and HTTP manifests retained. `local_test` below means parsing/decode/arithmetic, never neural inference.

<a id="F185"></a>
### F185 — W1_D11: Branch question and decision

Provenance: [W1_D11:5](_WORK/W1_D11.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

Can we add genuinely surveillance-like video with actors and time labels, rather than another trimmed sports/action corpus? **Yes: BEHAVE original Edinburgh interactions adds a fully downloaded fixed-camera sequence with group running and hard interaction negatives; VIRAT Release2 adds an exact remotely accessible running-positive clip and linked actor annotation.** They do not close industrial validation or short-burst latency. BEHAVE has annotation coordinate/time metadata questions; VIRAT has deliberate minimum-duration and label-tail rules, missing walk negatives in its original taxonomy, incomplete tracks, and restrictive redistribution terms. Promote both to research reserves; do not market them as an industrial walk/run benchmark. CAVIAR frame/XML mismatch remains M04/W2 work and is not resolved here.

<a id="F186"></a>
### F186 — W1_D11: Verified findings

Provenance: [W1_D11:9](_WORK/W1_D11.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Verified findings

<a id="F187"></a>
### F187 — W1_D11: D11-F01 [artifact_access_checked; local_test: full decode] BEHAVE independent video acquired

Provenance: [W1_D11:11](_WORK/W1_D11.md); original aliases: D11-F01. Sources: [S265](SOURCES.md#S265).

### [D11-F01](RAW_FACTS.md#F187) [artifact_access_checked; local_test: full decode] BEHAVE independent video acquired

Original **BEHAVE Interactions Test Case Scenarios**, Edinburgh Vision Group, page copyright Aroosha Laghaee 2007; cited dataset paper S. J. Blunsden/R. B. Fisher, *The BEHAVE video dataset: ground truthed video for multi-person behavior classification*, Annals BMVA 2010(4), 1–12. This is the 2007/2010 surveillance dataset, **not** MPI BEHAVE CVPR2022 human-object RGB-D data.

Direct video [[D11-S02](SOURCES.md#D11-S02)] GET200, **16,867,976 bytes**, SHA256 `2b5e93b7f198a3b56b6ab94638880825a864a601e8cc762195375f48461e5d19`. PyAV sequentially decoded **11,711 frames**, matching inclusive filename 35450–47160. Encoded MPEG4, **640×480, 25fps**, time_base1/25. First decoded frame PTS1/time0.04; sampled index9000 PTS9001/time360.04. Retained `behave_decode.json` and `behave_contact.jpg`. Contact sheet inspected: high fixed oblique camera overlooking street/parked cars; people appear small, cross/approach, run toward a group and become mutually occluded; glare/streaking/compression and parked-vehicle occlusion differ markedly from KTH isolated actors. Seven snapshots are not a complete gait adjudication or tracking result.

Page says two views and 25fps capture. Acquired only the listed AVI; did not obtain or verify synchronized second-view media. Treat its simultaneous views as one capture group if later found. Do not use camera-view diversity as independent actor/session evidence.

<a id="F188"></a>
### F188 — W1_D11: D11-F02 [primary_docs; local_test: annotation parsing] BEHAVE carries actual actors and temporal labels, but group labels overlap

Provenance: [W1_D11:19](_WORK/W1_D11.md); original aliases: D11-F02. Sources: [S266](SOURCES.md#S266).

### [D11-F02](RAW_FACTS.md#F188) [primary_docs; local_test: annotation parsing] BEHAVE carries actual actors and temporal labels, but group labels overlap

`markup.txt` [S03], GET200, 6,565bytes, SHA256 `0b17bc8c1fec3f9336a2a013a9c0bb2be586bbf895f3cc4ed498eebbf801e719`. Schema: optional two bracketed actor-ID groups, semicolon-separated start/end global frames and scenario label; inline comments, inconsistent whitespace and an extra empty semicolon occur. A robust parser must preserve raw line and reject ambiguous/reversed rows rather than assume CSV purity.

Local parser produced 171 parseable rows: WalkTogether43, RunTogether12, Chase10, InGroup35, Approach25, Split23, Fight19, Ignore2, Following1, Meet1. These are annotation rows, **not independent events**: `[2,4,5]` has both RunTogether and Chase at46334–46375; nested groups share the same interval. Direct downloaded raw text distinguishes these two labels (the web extraction misleadingly rendered both as RunTogether); trust retained raw artifact. Extra empty semicolons in Chase/Fight rows were tolerated by the parser. No deduplication was applied. A reversed InGroup interval2111→2035 is present (line9). Use `behave_labels.json` to audit, not automatic cleaned ground truth.

| Video/global range | Actor group | Source label | Use |
|---|---|---|---|
|35450–47160 /44396–44447|[1,2]|RunTogether|Short group-run candidate, 52 inclusive label frames (~2.08s at25fps)|
|35450–47160 /44400–44447|[1,2,4]|RunTogether|Same episode, expanding group; do not count as new independent positive|
|35450–47160 /44401–44447|[1,2,4,5]|RunTogether|Same episode, additional member|
|35450–47160 /46306–46375|[0,1]|RunTogether|Second separated group-run candidate,70frames (~2.8s)|
|35450–47160 /46330–46375|[2,4]|RunTogether|Overlapping chasers; same scene episode|
|35450–47160 /44611–44634|[1,5,4]|WalkTogether|Nearby walking control,24frames; identity/group membership changes|
|47300–58400 /51063–51167|[4,5]|RunTogether|Alternative source-listed file; not downloaded here|
|47300–58400 /55004–55111|[1,4]|RunTogether|Overlaps nested group labels; not independent crops|

The page defines Approach as groups approaching one another; it is **not a label of rapid approach**, acceleration, or danger. Chase is relational behavior and cannot be equated automatically with gait-run. RunTogether is a group-level statement, not per-frame leg-phase truth for every member. Unlabelled time is unknown because page says only many Clip1 interactions are labelled.

<a id="F189"></a>
### F189 — W1_D11: D11-F03 [artifact_access_checked; local_test; unknown] BEHAVE XGTF is usable structure, alignment is not yet benchmark-ready

Provenance: [W1_D11:38](_WORK/W1_D11.md); original aliases: D11-F03. Sources: [S262](SOURCES.md#S262), [S263](SOURCES.md#S263), [S267](SOURCES.md#S267).

### [D11-F03](RAW_FACTS.md#F189) [artifact_access_checked; local_test; unknown] BEHAVE XGTF is usable structure, alignment is not yet benchmark-ready

[S04] GET200,337,823bytes,SHA256 `90dd81cea02b4ae946ec681312a71ec2718247cf87d9c04f4502deb3e56c174d`. VIPER namespaces `http://lamp.cfar.umd.edu/viper#` and `http://lamp.cfar.umd.edu/viperdata#`; person objects IDs **0,1,2,4,5** with disjoint `framespan` intervals. Dynamic `bbox` has x,y,width,height and its own spans. No actor3 in this acquired annotation file; missing ID/box is not negative gait evidence. Example frame44396: actor0 bbox x138,y150,w48,h81; actor1 x73,y107,w40,h65; actor2 x1,y85,w16,h59.

Important contradiction: embedded FILE Information has **NUMFRAMES77814 and FRAMERATE1.0**, while decoded video is25fps/11711frames. Page explains INFO/XGTF can describe the full original sequence and contains workstation paths. Therefore do not drive timestamps from XGTF FRAMERATE. Filename and decoded count support candidate local zero-based index=`global_frame-35450`, but exact one-frame origin and spatial bbox scale/registration were **not conclusively overlay-verified**. Contact sheet used that relation only as a hypothesis. Do not silently rescale boxes or certify event latency. Source filename range contains removed material outside this subclip (e.g.11201–11499 omitted on page); concatenating subclips on a new timeline destroys global indices unless explicit map retained. W2 should overlay representative boxes at run onset/offset and certify coordinate scaling, origin and PTS mapping.

<a id="F190"></a>
### F190 — W1_D11: D11-F04 [primary_docs; artifact_access_checked; local_test: join] VIRAT original Release2 exact running-positive located

Provenance: [W1_D11:44](_WORK/W1_D11.md); original aliases: D11-F04. Sources: [S268](SOURCES.md#S268), [S269](SOURCES.md#S269), [S270](SOURCES.md#S270), [S271](SOURCES.md#S271), [S272](SOURCES.md#S272), [S273](SOURCES.md#S273).

### [D11-F04](RAW_FACTS.md#F190) [primary_docs; artifact_access_checked; local_test: join] VIRAT original Release2 exact running-positive located

Release document **Introduction for VIRAT Video Dataset Release2.0**, docv1.0 **2011-09-30**, Kitware/VIRAT [S05]. Eleven outdoor stationary HD scenes,720p/1080p H264; possible wind jitter. Original event map [S06] confirms **ID10=Person running**, **ID9=carrying**; numbered subsection3.2.10 is not zero-based class9. No generic walk class in original12-event taxonomy.

New exact link chain:

- Clip **VIRAT_S_050301_00_000000_000036.mp4**, file metadata65,008,519bytes and direct HEAD200 [S07]. **No media payload downloaded or decoded**, fps/PTS and visible gait remain unknown.
- Mapping [S08] event **30**, type**10**, duration**168**, start**45**, end**212**, one associated object; bit-vector maps to **objectID32** using official column-number-minus7 rule.
- Events [S09] GET20011,845bytes; local parser found168 event-frame rows, frame45–212 inclusive, all type10 event30. Bbox is event extent, not necessarily identical to person bbox.
- Objects [S10] GET200804,500bytes; object32 is type1(person), declared duration284frames38–321 but only **176 actual object-frame rows**; visible bbox heights80–107pixels in those rows. Gaps exist, so duration284 is not dense pose support. Event bboxes at frame45 x0,y654,w36,h120 and frame212 x0,y960,w36,h118; object bbox at first available frame38 x0,y669,w18,h80. Need visual alignment/edge truncation review, not blanket all-visible assumptions.

Source original annotation guidelines state visible portions only, little extrapolation through occlusion; crowd-source tracks may fragment. Annotation mode differs: some clips have events1–6 only, others1–12. **Absence of type10 in a6-class clip is not a no-running negative**. XLS listing modes/folds found in official docs item metadata but not downloaded/read in this branch. The first24 checked mapping files had no run; targeted later20 mappings yielded run positives in050300/050301. Retained `mapping_checks*.json`; this is not a prevalence estimate.

<a id="F191"></a>
### F191 — W1_D11: D11-F05 [primary_docs; inference] VIRAT temporal semantics censor short bursts and contaminate naive onset/offset scoring

Provenance: [W1_D11:57](_WORK/W1_D11.md); original aliases: D11-F05. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [D11-F05](RAW_FACTS.md#F191) [primary_docs; inference] VIRAT temporal semantics censor short bursts and contaminate naive onset/offset scoring

Original Release2.0 §3.2.10 requires running for **more than2seconds**, labels beginning when visibly running, and end delayed2seconds after running stops (wording about transition to standing/walking/sitting is itself awkward and should not be silently normalized). A camera model that detects a brief real run can appear false-positive if using this annotation regime. Last two seconds of a source event can be physically walking. It cannot be used unmodified as framewise pure-run truth or as short-burst recall coverage.

Original §4 recommends **scene-independent11-fold** evaluation, one scene per fold, and **scene-adapted5-fold** where different clips of same scene can occur train/test. Filename `VIRAT_S_XXYYZZ_KK_SSSSSS_TTTTTT`: XXcollection,YYscene,ZZsequence,KKsegment,start/endseconds. **First four numeric digitsXXYY identify scene**. Keep sequence+allsegments together at minimum; use scene grouping for unseen-camera claim. Actor object IDs are within-file track identities, not global people identities. All subsets/derived reannotations of identical video must share a source-video group.

Original scorer permissive matches spatial/temporal overlap above10%, allows multiple detections to one event without extra false-alarm penalty and one detection to multiple events. This is incompatible with case one-incident-one-message validation: separately measure duplicate alerts and onset latency; do not transfer original Pd/F-score as evidence of those properties.

<a id="F192"></a>
### F192 — W1_D11: D11-F06 [artifact_access_checked; primary_docs; local_test] Newer VIRAT DIVA annotations DO contain walking and running

Provenance: [W1_D11:65](_WORK/W1_D11.md); original aliases: D11-F06. Sources: [S274](SOURCES.md#S274), [S275](SOURCES.md#S275), [S276](SOURCES.md#S276), [S277](SOURCES.md#S277), [S278](SOURCES.md#S278).

### [D11-F06](RAW_FACTS.md#F192) [artifact_access_checked; primary_docs; local_test] Newer VIRAT DIVA annotations DO contain walking and running

This is a useful exception to M04's correct caution about **current MEVA** definitions: do not infer that VIRAT's linked older DIVA annotations exclude gait. Public GitLab repository pinned to **f1eff0d7db0dc0b25e1c99951ac0907521f3a216**, Roddy Collins,2021-09-21, README-update commit [S11]. KPF YAML,train/validate folders. Guideline **DIVA-Annotation-Guidelines-V1.0.docx.pdf** [S12],174,571bytes,GET200; text §4.4/4.5 requires ≥2s walking/running and extends each state1s after transition. Walking requires horizontal movement; pacing is annotated standing. These are dataset conventions, not universal human gait definitions.

Pinned `train/VIRAT_S_000000.activities.yml` [S13],GET20048,956bytes; parser finds59 activity_walking,42 activity_standing,4 activity_running rows. Structure `act.act2={label:1.0}`,`id2=activityID`,`timespan:[{tsr0:[start,end]}]`,`actors:[{id1:trackID,timespan:...}]`,`src:truth`. **Same actor16** has run5482–5527, walk5528–5644; walk5843–5899, run5900–5981, walk5982–6024. Concurrent Transport_HeavyCarry5482–6085 is a real hard-case annotation pairing. Actor28 run12783–12939; actor2 run1820–1993. No inference that heavy-carry means improper carrying.

However, this exact000000 media was not joined to the Release2 original-video listing in this pass; **annotation-only lead** until source-media identity/fps/frame convention established. Do not substitute000001 video: that is another source, and acquired000001.activities.yml has no activity_running. `types.yml` maps track IDs to object types, not actor personal identities. Geometry YAML not acquired; no claim of KPF bbox/time agreement. Train/validate tree existence is verified; actor/camera independence of those splits was not audited and should not be assumed from folder names.

<a id="F193"></a>
### F193 — W1_D11: Rights and artifact boundaries

Provenance: [W1_D11:73](_WORK/W1_D11.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Rights and artifact boundaries

<a id="F194"></a>
### F194 — W1_D11: D11-F07 [primary_docs; unknown]

Provenance: [W1_D11:75](_WORK/W1_D11.md); original aliases: D11-F07. Sources: [S279](SOURCES.md#S279).

**[D11-F07](RAW_FACTS.md#F194) [primary_docs; unknown]** Data licenses differ materially. VIRAT Ground agreement [S14] explicitly permits lawful research **and commercial purposes**, while requiring every user to accept/sign terms, protect PII and refrain from identifying people. Redistribution is limited to parties agreeing to terms; limited scientific publication/lecture frames/clips are allowed. This is neither NC-only nor unrestricted redistribution. No acceptance was performed for the user, and broad public product-demo redistribution is not established by the scientific exception. Aerial's separate unrestricted-distribution statement does not apply to Ground media. The annotation repository root read tree has no standalone LICENSE; a separate DIVA annotation grant was not located here. Ground agreement must not be casually replaced by an assumed GitLab license.

BEHAVE page says researchers can freely use and requests citation; no separate standardized license/commercial deployment/public-demo grant was located. Record this as limited primary permission language with unresolved broader rights, not CC or automatically NC. Do not conflate with the unrelated CVPR2022 BEHAVE license. No model code or checkpoint acquired/assessed by D11: code-license/weight-license are **not applicable to these dataset-only findings**, and no data grant clears pretrained weights. Acquisition/parsing scripts are authored local research utilities, not dataset-owner inference code.

<a id="F195"></a>
### F195 — W1_D11: Hard negatives, causal design and downstream admission

Provenance: [W1_D11:79](_WORK/W1_D11.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Hard negatives, causal design and downstream admission

<a id="F196"></a>
### F196 — W1_D11: D11-F08 [inference; hypothesis: proposed protocol]

Provenance: [W1_D11:81](_WORK/W1_D11.md); original aliases: D11-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D11-F08](RAW_FACTS.md#F196) [inference; hypothesis: proposed protocol]** Prioritize these controls by mechanism, not stock-video variety:

| Hard negative or uncertainty | Why needed | Public evidence / gap |
|---|---|---|
|Normal walk vs genuinely fast walk, same actor/direction/depth|Separate gait from image displacement|BEHAVE WalkTogether available; neither verified source has fast-walk taxonomy. Capture/annotate target fast walk|
|Running toward/away camera vs lateral walking; near/far|Perspective can invert pixel-speed ordering|BEHAVE high-oblique footage; VIRAT small-person variety author claim. Need depth/view-labelled holdout|
|Crossing actors, group formation/fight/chase|ID switch/crop substitution creates velocity/action spikes|BEHAVE overlapping group labels and occlusion are directly available; annotate per-actor visibility|
|Partial legs, image-edge cropping, parked-vehicle occlusion|Cannot determine gait from invisible feet|BEHAVE visual examples; VIRAT visible-only and sparse object rows. Unknown/abstain, not walk|
|Carrying, stopping/turning, reaching, hurrying to interact|Arm motion and body lean may mimic run|VIRAT DIVA actor16 run/walk+HeavyCarry labels provide candidate, pending media join|
|Camera jitter/zoom and moving background/vehicle|Flow and bbox velocity can fire on scene motion|VIRAT wind-jitter note; stable-target/controlled camera-motion footage still needed|
|Short burst<2s, onset/offset transitions|Source label duration conventions miss/extend events|VIRAT intentionally censors; BEHAVE selected run interval~2s but global coordinate verification pending|
|Running in place vs translation; stepping on moving platform|Gait and ground speed can dissociate|Not verified in acquired CCTV; permissioned target capture needed|
|Industrial PPE, low illumination, glare, steam, occlusion by equipment|Urban/staged yard domain does not prove workshop behavior|Neither corpus closes factory domain gap|

Evaluate a fixed preprocessing/model contract on intact continuous holdout videos, not random overlapping crops. Group all near-duplicate clips, cameras of same acted take, shared scene and people/session where known. BEHAVE repeated Vision Group actors/background mean random subclip split leaks identity/site; a second view does not remedy this. Report actor/camera/session-known versus unknown fields explicitly.

Do not downsample source acquisition to1fps then claim original gait evidence retained. Separate dense local decode evidence from neural invocation/notification cadence; preserve PTS and irregularity. Event metrics: run recall by duration including<2s target bursts, false alerts/camera-hour, onset→first-alert latency, duplicate messages, per-actor attribution, unknown coverage. Stratify person pixelheight/direction/leg visibility/occlusion/depth zone. Keep dataset operational label tails separate from physical-motion annotations used for latency. Do not infer metres/second or physical proximity from image boxes; gait annotation is not calibrated speed truth.

Admission: BEHAVE can enter local sanity tests after overlay/timebase verification and rights scope; VIRAT exact050301 can enter sustained-run testing after lawful authorized acquisition, decode and temporal alignment, plus annotation-mode check for any negative clips. Target-camera validation remains necessary. No claims of model accuracy, LinQ execution or runtime made.

<a id="F197"></a>
### F197 — W1_D11: Rejected / unresolved branches and handoff

Provenance: [W1_D11:120](_WORK/W1_D11.md); original aliases: section record. Sources: [S280](SOURCES.md#S280).

## Rejected / unresolved branches and handoff

PETS2009 was meaningfully searched as a potential crowd-run/evacuation alternative; the official Reading page https://www.cvg.reading.ac.uk/PETS2009/a.html was inaccessible to the web tool. Secondary OpenTraj and paper mirrors suggest group-level event semantics, but not promoted to verified primary dataset evidence here. Failure does not prove original data disappeared. No secondary source used to claim a new acquired gait corpus. KTH/CAVIAR and Weizmann deliberately not reacquired.

W2 priorities: (1) BEHAVE overlay/frame-origin/coordinate-scale verification, keep25fps encoded clock rather than XML1.0; (2) verify VIRAT050301 exact clip decoding and object32 visibility, do not interpret HEAD as video execution; (3) inspect original XLS annotation-mode/folds before negative mining; (4) media join for DIVA000000 and source-reannotation overlap registry; (5) rights scope for presentation/public reuse. Cross-corpus same-source leakage is a practical risk if both original VIRAT and DIVA derivative annotations are used on different sides of the split. No cross-actor global identity guarantee found. No factory fast-walk, leg-visibility stratification, short-burst ground truth or calibrated rapid-approach corpus closed. Those remain target-capture tasks, not reasons to inflate stock corpus claims.

<a id="F198"></a>
### F198 — W1_D12: W1 D12 — телефон, рука–предмет, дальний ракурс и рабочие объекты-обманки

Provenance: [W1_D12:1](_WORK/W1_D12.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D12 — телефон, рука–предмет, дальний ракурс и рабочие объекты-обманки

Дата первичных обращений: **2026-10-23, 19:39–19:47 UTC**. Ветка: какие доступные видеоданные и hand-object donors действительно добавляют phone-use, принадлежность конкретному человеку и рабочие отрицательные примеры сверх AVA/HICO, уже проверенных M05? Автор: W1 D12. Без обучения, инференса нейросетей, платных ресурсов и обращений к авторам. Скачаны небольшие архивы разметки; единственный полностью полученный исходный видеоклип — Charades `2RFLZ.mp4`, 765,584 bytes. P-DESTRE и MECCANO целиком не скачивались. `local_test` ниже означает выполненный разбор файлов/декодирование, а не тест качества модели.

**Решение [inference]: Charades — наиболее конкретное новое дополнение для воспроизводимого temporal phone-use donor; P-DESTRE — перспективный дальний ракурс с существенным дефектом person-ID в проверенном phone-фрагменте; MECCANO — рабочие hand/tool negatives; 100DOH — вспомогательная hand-contact задача, а не phone recognizer.** Сценарий №3 остаётся резервом для камеры с различимым телефоном. Ни один источник не маркирует промышленный запрет, разрешённый служебный терминал, радиостанцию и сканер как достаточный набор контролей.

<a id="F199"></a>
### F199 — W1_D12: Проверенные результаты

Provenance: [W1_D12:7](_WORK/W1_D12.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Проверенные результаты



<a id="F200"></a>
### F200 — W1_D12: W1-D12-F001 [artifact_access_checked, local_test] — фактически доступное phone-use видео Charades

Provenance: [W1_D12:10](_WORK/W1_D12.md); original aliases: W1-D12-F001. Sources: [S281](SOURCES.md#S281), [S282](SOURCES.md#S282), [S283](SOURCES.md#S283).

### [W1-D12-F001](RAW_FACTS.md#F200) [artifact_access_checked, local_test] — фактически доступное phone-use видео Charades

Официальный annotation archive `https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip` получен целиком: **HTTP200, 3,519,822 bytes**. Внутри есть исходные CSV, классы, mapping, MATLAB evaluation и `license.txt`. Старый project URL `https://prior.allenai.org/projects/charades` на дату исследования перенаправляет на главную AllenAI, однако архивы S3 работают; redirect homepage не означает исчезновение данных. [S001,S002]

Классы из реального файла `Charades_v1_classes.txt`:

| ID | Семантика | Соответствие нашему событию |
|---|---|---|
| c015 | Holding a phone/camera | наличие/держание; недостаточно для use |
| c016 | Playing with a phone/camera | use-like; телефон и камера объединены |
| c017 | Putting a phone/camera somewhere | переход прекращения/смены взаимодействия, не автоматически нарушение |
| c018 | Taking a phone/camera from somewhere | получение устройства, не автоматически использование |
| c019 | Talking on a phone/camera | разговорное phone-use-like действие; всё ещё объединённый объект |

Из собственного разбора: train 7,985 записей, test 1,863. Числа интервалов по c015…c019 соответственно **train 1055/673/219/298/217; test 265/187/71/115/42**. Числа уникальных клипов могут быть меньше: test c015=260, c016=186, c018=111; c019=42. Это не число независимых пользователей/нарушений. `charades_phone_summary.json` сохраняет counts/examples.

Точный выбранный test пример: `id=2RFLZ`, `subject=ENHU`, CSV length14.71; actions `c009 7.70 13.00;c019 3.00 10.40;c017 8.00 12.60;c015 2.30 12.40;c018 2.40 6.90`. `c019` размечен 3.0–10.4 секунд, одновременно могут быть hold/take/put. Нельзя превращать наличие carry/put в veto для use. [S002]

Видео archive `https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip` поддерживает Range: HTTP206, полный размер **16,339,546,533 bytes**. Скрипт прочёл ZIP central directory и только member `Charades_v1_480/2RFLZ.mp4`, без полного архива: **1,783,222 transferred bytes**, включая directory; compressed member760,539; полученный MP4765,584. SHA256 `77cb4611d404ed5a2aac77e24c374091f5eef452779c5763b8c5a38666fd28c6`. Воспроизводимые offsets/status сохранены в `charades_media_access.json`. URL отдельного опубликованного MP4 не найден; точный downloadable locator — URL ZIP + member, а не выдуманный individual URL. [S003]

PyAV действительно декодировал видео: **480×270, 222 frames, average_rate15029/1000 (~15.029fps), stream duration14.77144s**. Поэтому имя `480` не следует читать как гарантированную высоту480 или FPS24/30. Просмотрен contact sheet PTS0,3.061,6.055,9.049,12.043,14.040: домашний интерьер, один видимый человек, перемещение у стола/окна; в части кадров рука поднесена к голове/предмет держат перед собой. Объект мал и не одинаково различим во всех этих кадрах. Шесть кадров подтверждают декодируемость/сцену, **не независимый frame-by-frame GT** разговора на всём3–10.4s. Никакие детектор/классификатор не запускались. Попытка OpenCV не удалась из-за отсутствия cv2, затем успешно использован установленный PyAV; сохранены оба скрипта.



<a id="F201"></a>
### F201 — W1_D12: W1-D12-F002 [primary_docs, local_test, inference] — Charades закрывает temporal labels, но не actor relation

Provenance: [W1_D12:33](_WORK/W1_D12.md); original aliases: W1-D12-F002. Sources: [S281](SOURCES.md#S281).

### [W1-D12-F002](RAW_FACTS.md#F201) [primary_docs, local_test, inference] — Charades закрывает temporal labels, но не actor relation

CSV schema: `id,subject,scene,quality,relevance,verified,script,objects,descriptions,actions,length`. `actions` — разделённые `;` triples `class_id start_seconds end_seconds`. `objects` — список слов уровня клипа. В этом пакете **нет person bbox, phone bbox, hand bbox, pair indices или person-track ID для каждого действия**. Поле subject не является actor-localization на каждом кадре. Следовательно, совместные action intervals одного видео нельзя без просмотра переименовать в same-person phone+walk. Общий c097 означает walking through a doorway, а не всякое перемещение по цеху. Source evaluation scripts для video classification/temporal localization не измеряют actor-compatible промышленное event recall или FP/camera-hour. [S002]

Split сохранять по исходному video и, при проверке переноса на неизвестных людей, по subject; соседние frames/temporal crops одного source не должны попадать в train/test. Уже просмотренный2RFLZ — development/example, не lockbox. Проверка отсутствия cross-split subject overlap здесь не выполнена. Нет выбранных/запущенных trained Charades weights; это verified data donor, не готовая модель для LinQ.



<a id="F202"></a>
### F202 — W1_D12: W1-D12-F003 [primary_docs, artifact_access_checked, local_test] — P-DESTRE: дальний телефон существует в реальном annotation payload, но ID=-1

Provenance: [W1_D12:40](_WORK/W1_D12.md); original aliases: W1-D12-F003. Sources: [S284](SOURCES.md#S284), [S289](SOURCES.md#S289), [S290](SOURCES.md#S290), [S291](SOURCES.md#S291), [S292](SOURCES.md#S292), [S293](SOURCES.md#S293).

### [W1-D12-F003](RAW_FACTS.md#F202) [primary_docs, artifact_access_checked, local_test] — P-DESTRE: дальний телефон существует в реальном annotation payload, но ID=-1

Первичная страница P-DESTRE описывает drone video: 5.5–6.7m altitude, pitch45–90°, 3840×2160,30fps,H264MP4, университетские кампусы. Она даёт person bbox, ID и categorical action7=`Talking over the Phone`; отдельного phone/hand bbox нет. [S004]

`https://p-destre.di.ubi.pt/datasets/dataset.tar` реально отвечает HTTP206; Content-Range total **41,535,221,248 bytes**. Получен первый1MiB, затем точечными512-byte requests читались tar headers, перепрыгивая media payload. Индекс `pdestre_members.json` содержит159 members до начала annotations; media не декодированы. Точный выбранный member `P-DESTRE/videos/11-11-2019-1-2.MP4`: size732,182,022; tar header offset3,094,765,056; data offset3,094,765,568. Это подтверждает archive membership/доступный endpoint, а не полный hash или проигрывание этого файла. [S005]

После ограниченного поиска annotation members получен целиком `P-DESTRE/annotation/11-11-2019-1-2.txt`: **1,814,813 bytes,22,473 строки**. Из них **371 строка action7**, frames3…373 включительно, **все person ID=-1**. Остальные22,102 строки имеют action0 Walking. Нет основания соединять разных людей через ID=-1; даже одна непрерывная серия bbox нуждается в независимом actor association и просмотре. Разметка всё же связывает action7 с конкретным bbox данной строки/кадра. Не утверждаю, что все phone labels всего P-DESTRE имеют этот дефект: проверены ограниченные16 annotation files, не весь набор. Первые10 файлов дали единственный найденный phone-файл; следующие6 без phone. Сохранены поисковые logs, выбранный payload и summary. [S006]

Schema26 CSV columns: frame,ID,4 bbox fields,4 headpose fields,16 soft-label fields. Последняя колонка — action0…13. Пример первых значений phone-строки: `3,-1,2271.4,992.23,72.03,170.89,-1,-1,-1,-1,...,7`. Page называет bbox `x,y,h,w`; при этом фактические пары вроде72.03/170.89 выглядят как width/height вертикального человека. **Порядок h/w не разрешён визуально**, поэтому importer требует overlay на исходном кадре. Не молча менять порядок по догадке. ID=-1 и headpose flag=-1 встречаются в реальном payload; headpose primary page также описывает как output Deep Head Pose для части боксов, не manual gaze truth. [S004,S006]

Один action field не позволяет получить независимую co-label phone AND walk: walking0 и phone7 — разные значения одной колонки. Наш mapping: `action7 + bbox` → talking-phone-like person-frame; phone-use while walking requires motion/actor verification отдельно. В проверенных phone rows bbox numeric field4 диапазон63.72–180.06, field5 59.87–449.12: это **размеры человека**, не телефона и не порог видимости устройства. 4K не гарантирует различимый phone после resize. Source people mostly students, drone motion/overhead view и campus-background существенно отличаются от fixed industrial CCTV. Нет подтверждённых scanner/radio/tool negatives или рабочей техники. [S004–S006]



<a id="F203"></a>
### F203 — W1_D12: W1-D12-F004 [artifact_access_checked, local_test] — MECCANO даёт настоящие hand/tool/video labels, но zero phone taxonomy

Provenance: [W1_D12:53](_WORK/W1_D12.md); original aliases: W1-D12-F004. Sources: [S291](SOURCES.md#S291), [S292](SOURCES.md#S292), [S293](SOURCES.md#S293), [S294](SOURCES.md#S294), [S295](SOURCES.md#S295), [S296](SOURCES.md#S296).

### [W1-D12-F004](RAW_FACTS.md#F203) [artifact_access_checked, local_test] — MECCANO даёт настоящие hand/tool/video labels, но zero phone taxonomy

Скачаны и разобраны три официальных небольших архива: action annotations64,921B, active objects1,599,214B, hands2,634,441B; HTTP200 полных загрузок (предварительные Range206 отдельно в logs). RGB video endpoint ответил206, total11,920,575,383; получен только1MiB probe, видео не декодировались. [S007–S010]

20 object IDs прямо из JSON: **0 booklet;1 gray_angled_perforated_bar;2 partial_model;3 white_angled_perforated_bar;4 wrench;5 screwdriver;6 gray_perforated_bar;7 wheels_axle;8 red_angled_perforated_bar;9 red_perforated_bar;10 rod;11 handlebar;12 screw;13 tire;14 rim;15 washer;16 red_perforated_junction_bar;17 red_4_perforated_junction_bar;18 bolt;19 roller.** Phone/radio/scanner/person/PPE здесь отсутствуют. Нельзя считать generic hand contact доказательством phone use. Положительная польза: рабочие движения руками, booklet/screwdriver/wrench как естественные confusers. Отсутствие phone класса не удостоверяет, что случайный фон каждого кадра phone-free. [S009]

Action CSV: `video_id,action_id,action_name,start_frame,end_frame`, границы — имена вроде00076.jpg…00120.jpg. Пример val: video0007/action8 `take_screwdriver`01591–01600.jpg; action58 `screw_screw_with_screwdriver`01626–01682.jpg; action0 `check_booklet`00076–00120.jpg. Полная61-class map сохранена в schema_summary.json. 12 verbs первичного paper supplement: take,put,check,browse,plug,pull,align,screw,unscrew,tighten,loosen,fit. Наше соответствие `take_screwdriver` → tool interaction negative for prohibited phone use, **не phone use и не generic prohibited work**. Близкие/перекрывающиеся интервалы не надо принудительно превращать в взаимоисключающие состояния. [S008,S011]

Own counts: train5057 action segments/11 videos; val977/2; test2823/7, всего8857. Video grouping train0001–0006,0013–0016,0018; val0007,0017; test0008–0012,0019,0020. Active object JSON train21687 images/37385 annotations; val4271/6982; test12112/19980 (total64,347 annotations, тогда как page headline64,349; не подменять actual-file counts заголовком). COCO `images/annotations/categories`; bbox[x,y,width,height], image_id/category_id,area,iscrowd,ignore,empty segmentation. IDs начинаются с0; нельзя подставлять COCO80 mapping. Test image metadata **9676 images1920×1080 +2436 images1280×720** несмотря на page general1920×1080. [S009]

Hands — отдельный VIA CSV per video: filename,file_size,file_attributes,region_count,region_id,region_shape_attributes,region_attributes. Actual row00056.jpg содержит rect{x1168,y921,width285,height159}, class`SX_Hand`; встречается `DX_Hand`; region_count0 с `{}` означает отсутствие размеченных hand boxes данного кадра. Нет ID конкретного чужого человека и explicit hand↔object foreign key в этих двух отдельных файлах. Действующий субъект — camera wearer по egocentric task design; join по video/frame связывает сцену, но не устанавливает, какая из двух рук касается какого объекта. Эго-вид крупно показывает руки и подменяет задачу дальнего full-body association. [S010]



<a id="F204"></a>
### F204 — W1_D12: W1-D12-F005 [artifact_found, artifact_access_checked, primary_docs] — точный MECCANO tool detector найден, не исполнен

Provenance: [W1_D12:66](_WORK/W1_D12.md); original aliases: W1-D12-F005. Sources: [S285](SOURCES.md#S285), [S286](SOURCES.md#S286), [S297](SOURCES.md#S297).

### [W1-D12-F005](RAW_FACTS.md#F204) [artifact_found, artifact_access_checked, primary_docs] — точный MECCANO tool detector найден, не исполнен

Author repository revision получен `git ls-remote`: **50d3314cd8a79ca522c0cc73bb1b53b794f1ea60**. Model URL `https://iplab.dmi.unict.it/sharing/MECCANO/models/active_object_recognition/MECCANO_active_objects.pth` дал Range206 total**482,761,498 bytes**,512-byte probe; полный weight/hash/state_dict не получены. Pinned config `https://github.com/fpv-iplab/MECCANO/blob/50d3314cd8a79ca522c0cc73bb1b53b794f1ea60/configs/active_object_recognition/meccano_active_objects.yaml`: Detectron2 GeneralizedRCNN,R101,FPN,ROIHeads20 classes, BGR,mean103.53/116.28/123.675,std1, test min800/max1333; config также содержит test augmentation enabled, flip и9 scales400…1200. Нужно проверять вызывающий inference/eval entrypoint, применяет ли он TTA; один YAML не доказывает реальный effective multi-view runtime. Code/weight/data license grant в прочитанных README/page/annotation README не найден; отсутствие найденного grant ≠ доказательство отсутствия лицензии где-либо. Локальный tool detector не запускался. [S012,S013]



<a id="F205"></a>
### F205 — W1_D12: W1-D12-F006 [primary_docs, artifact_access_checked] — 100DOH generic contact не различает phone/radio/scanner

Provenance: [W1_D12:71](_WORK/W1_D12.md); original aliases: W1-D12-F006. Sources: [S298](SOURCES.md#S298), [S299](SOURCES.md#S299), [S300](SOURCES.md#S300), [S301](SOURCES.md#S301), [S302](SOURCES.md#S302), [S303](SOURCES.md#S303), [S304](SOURCES.md#S304), [S305](SOURCES.md#S305), [S306](SOURCES.md#S306), [S307](SOURCES.md#S307).

### [W1-D12-F006](RAW_FACTS.md#F205) [primary_docs, artifact_access_checked] — 100DOH generic contact не различает phone/radio/scanner

Shan,Geng,Shu,Fouhey,CVPR2020, *Understanding Human Hands in Contact at Internet Scale*. Code revision**e6eec712a498ec7844b97893c8d012cea1a71e09**. Detector categories в `demo.py`: background,targetobject,hand. Hand output10 columns: box4,score,state,offset vector3,left/right. README разделяет contact N(no),S(self),O(other person),P(portable object),F(stationary). Object row имеет тот же размер, но auxiliary state/offset/side для objects **не обучались**; использовать только box/score. Generic targetobject не имеет phone/camera/radio class. [S014,S015]

VOC parser читает bbox,contactstate,contactright,contactleft,magnitude,unitdx,unitdy,handside; уменьшает pixel coords на1 и magnitude×0.001. Нет person-track ID или temporal phone-use action. Input demo cv2 BGR, mean102.9801/115.9465/122.7717, short-side600/max1000; ResNet101 FasterRCNN + ROI align/custom compiled ops. Authors прямо отмечают трудности большого числа людей и ego left/right. Это candidate association aid, требующий phone classifier и actor association. [S015,S016]

Download page: file.zip содержит video IDs/frame annotations/specifications, **не гарантированное bundle оригинального видео**; endpoint Range206 total26,416,596,1MiB probe. Frame-cache/Pascal data agreement non-commercial research, no redistribution. Page TLS chain не прошёл requests verification; диагностический fetch с verify=False дал200 и сохранён как таковой, без утверждения authenticated TLS. Оба официальных Drive checkpoint IDs (`166IM6CXA32f9L6V7-EMd9m8gin6TFpim`100K и `1H2tWsZkS7tDF8q1-jdjx6V9XrK25EDbE`100K+ego) дали**404** и web open и direct view probe. Значит current official checkpoint path не воспроизведён; **не** утверждение, что веса нигде не существуют. Code MIT подтверждён отдельным LICENSE; это не commercial grant для frames, исходных интернет-видео или весов. [S017,S018]



<a id="F206"></a>
### F206 — W1_D12: W1-D12-F007 [primary_docs, unknown] — DMD и NTU не готовы как немедленный открытый target pack

Provenance: [W1_D12:80](_WORK/W1_D12.md); original aliases: W1-D12-F007. Sources: [S186](SOURCES.md#S186), [S287](SOURCES.md#S287), [S288](SOURCES.md#S288), [S308](SOURCES.md#S308), [S309](SOURCES.md#S309), [S310](SOURCES.md#S310).

### [W1-D12-F007](RAW_FACTS.md#F206) [primary_docs, unknown] — DMD и NTU не готовы как немедленный открытый target pack

DMD официальная страница различает talking/texting left/right, operating radio, drinking/hair; есть hands/objects location и temporal driver actions в VCD. Но **operating radio — автомобильная магнитола, не handheld walkie-talkie negative**. Запись запрещённых действий проводилась в стоящем автомобиле/симуляторе. Текущая страница 2026 содержит сокращение релиза: удалены некоторые участники, simulator/IR/depth больше не public, остаётсяRGB. Старую headline multimodality нельзя выдавать за текущий downloadable payload. [S019]

Download distraction URL `https://opendatasets.vicomtech.org/di21-dmd-dataset-distraction-rgb-ir/a268f10c` открыл лишь JS app shell; original filename всё ещёrgb-ir не отменяет текущий release notice. Нет извлечённого archive/file URL или проверенного VCD example; access route localized, payload schema/version unknown. CC BY-NC-ND4.0 + academic-only language; official terms нужно учитывать отдельно от возможности открыть page. Gaze/hands route `https://opendatasets.vicomtech.org/di21-dmd-dataset-gaze/8433939e`. [S020]

NTU первичная страница подтверждает A28 phone call,A29 play with phone/tablet,A32 selfie; clips labeled by filename S/C/P/R/A, без phone bbox. A29 не позволяет отделить tablet. Доступ RGB требует регистрации/request/release agreement/approval; academic/non-commercial, derivation/redistribution/commercial use требуют expressed permission. Группировать синхронные3 camera views и repetitions по source recording/performer; наличие camera split не равно unseen-person split. Нового прямого phone MP4 NTU не получено. Этот источник здесь только проверенный restricted-access alternative, не повтор модели PoseC3D из sibling report. [S021]

<a id="F207"></a>
### F207 — W1_D12: Лицензии и практический выбор

Provenance: [W1_D12:88](_WORK/W1_D12.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Лицензии и практический выбор

| Источник | Code / weights | Данные и ограничение |
|---|---|---|
| Charades | archive license прямо распространяет термин software на source/models/data; отдельные trained weights не выбраны | Non-Commercial Use; разрешён research/evaluation scope по тексту; for-profit derivation не разрешена; public modified data/third-party distribution не разрешены; публикация коротких academic examples допускается. Не вкладывать полученный MP4 в открытый demo bundle автоматически |
| P-DESTRE | обученные action weights не найдены/не проверялись | CC BY-NC-SA4.0; citation + page просит forwarding public reports; никакого сообщения авторам не отправлено. Соревновательный/промышленный downstream grant не установлен |
| MECCANO | exact code/weight found; grant unknown в прочитанных материалах | copyright page без найденной отдельной data license; для публичной демонстрации/обучения rights gap остаётся |
| 100DOH | MIT source; official weights404; separate weight grant unknown | frame-cache agreement noncommercial/no redistribution; source YouTube availability/rights отдельно |
| DMD | модель и code license не исследованы | CC BY-NC-ND4.0, academic-only; текущий release сокращён |
| NTU | borrowed implementations имеют свои лицензии; они не изменяют dataset agreement | academic/noncommercial; account approval; запрет derivation/redistribution/commercial без permission |

[inference] Для конкурса/публичной демонстрации команда должна сверить intended use с конкретным grant; задача исследования не даёт blanket коммерческую лицензию. Ни платных запросов, ни согласий от лица команды, ни outreach здесь не сделано.

<a id="F208"></a>
### F208 — W1_D12: Что конкретно проверять на целевой CCTV

Provenance: [W1_D12:101](_WORK/W1_D12.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Что конкретно проверять на целевой CCTV

1. Annotation должен разделять `phone_visible`, `phone_class_known`, `held/contact`, `use_like`, `actor_track`, `walking`, `equipment_work_context`, `policy_forbidden`; `unknown` отдельно от negative. Direct phone action labels не устанавливают служебное разрешение/запрет.
2. Matched hard negatives: carry у бедра/карман/на столе; другой человек с телефоном рядом; walkie-talkie к уху/рту; barcode scanner с экраном; payment/work terminal; screwdriver/black tool; glove/hand to face; ear protection adjustment; scratch/wipe/cough; clipboard/booklet; работа двумя руками и permitted terminal. Из проверенных наборов MECCANO покрывает tools/booklet, DMD покрывает магнитолу/comb/drink, **handheld radio/scanner/PPE confusers остаются отсутствующим target evidence**, а не якобы покрытыми классами.
3. Сохранить native phone/hand/person bbox pixel dimensions и после полного production resize/crop. Пример геометрии, не empirical threshold:18px phone на1920-wide при resize640 превращается в6px. Crop исходника до downscale может сохранить деталь; upscale уже потерянной детали её не восстанавливает. Не назначать универсальный min-pixel gate на основании dataset resolution.
4. Ракурсы: back view, ear-side occlusion, crossed hands, glove, tool blocking device, multiple nearby people, phone transferred between people. При невидимом предмете/head-down нельзя уверенно различить phone/scanner или phone-use vs ordinary work.
5. Event evaluation должен проверять тот же actor и temporal overlap движения/use. Source intervals не гарантируют точную continuous onset/offset; Charades example имеет overlapping take/put/call. Без phone ownership GT нельзя соединять walk одного человека и phone другого. P-DESTRE ID=-1 нельзя использовать как общий трек.
6. Holdout по source/session/person/camera; соседние кадры и synchronized views не независимые trials. Target positives и длинные разрешённые negatives нужны для event recall/FP per camera-hour; caption/video top1/frameAP не заменяют эти показатели. No real-world severity/causal attentional impairment вывод из ярлыка phone.

<a id="F209"></a>
### F209 — W1_D12: Handoff / незакрытые звенья

Provenance: [W1_D12:136](_WORK/W1_D12.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Handoff / незакрытые звенья

Root: добавить **actual decoded Charades2RFLZ** в evidence tiers, но не в redistributed competition bundle; заменить «phone video совсем не получено» на узкое «получен и декодирован один Charades donor; target industrial pack отсутствует». P-DESTRE можно предложить для дальнейшего дальнего review только с оговорками action categorical/ID=-1/h-w unverified/no media decode. MECCANO — curated tool/hand controls и версия-sensitive metadata, не positive phone labels. DMD current release contraction и100DOH official weight404 полезны для access-risk register.

Осталось неизвестно: разрешённый industrial camera pack и handheld scanner/radio/PPE negatives; legal grant под фактический конкурс/demo; проверенный P-DESTRE phone-object visibility и стабильные IDs других последовательностей; MECCANO code/data/weight grant; current DMD downloadable version/schema; полный100DOH checkpoint route; chosen trained temporal model на Charades и его exact artifact/config/input chain; LinQ SDK/ops/precision/host association/device quality. Ничто здесь не доказывает phone use while working автоматически по зональному присутствию или причинную потерю внимания.

<a id="F210"></a>
### F210 — W1_D13: W1 D13 — real industrial person–machine video: the remaining public-label gap

Provenance: [W1_D13:1](_WORK/W1_D13.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D13 — real industrial person–machine video: the remaining public-label gap

**Branch question:** is there a directly accessible, reusable real industrial fixed-camera video package containing separate pedestrian/machine tracks and temporal near-miss truth, including driver and machine-motion controls?

**Decision / inference:** this search did not establish that complete chain. The strongest new artifact is **PhysicalAI-SmartSpaces' real Warehouse_026/027 footage and calibration**: all eleven video URLs respond anonymously to bounded binary range requests. However, their tracking/depth ground truth is explicitly withheld, no released event labels were found in the complete repository file listing, and the same revision has inconsistent statements about public distribution of those real videos. The challenge's manual-label prohibition is an **evaluation protocol**, not automatically a universal prohibition in the CC BY license. Do not silently treat these real test scenes as an unrestricted training/relabeling pack, or describe their synthetic box counts as real annotation coverage. A separate real-forklift multispectral benchmark remains explicitly **request-only/non-profit** and uses an onboard camera, not outside-in CCTV.

Access: **2026-10-23, approximately 19:40–19:52 UTC / 22:40–22:52 Moscow**. Exact operation metadata is in `_WORK/D13/`. Read complete assignment, `_WORK/CASE_NOTES.md`, targeted older feasibility report, D09 and M06. No video was fully downloaded, decoded or visually annotated; no inference, training, hardware test, outreach or paid computation. `local_test` here means parsing downloaded JSON/HTML, not evaluating a model. HTTP ranges establish byte accessibility only.

<a id="F211"></a>
### F211 — W1_D13: D13-S01 / primary_docs — PhysicalAI-SmartSpaces release and paper

Provenance: [W1_D13:9](_WORK/W1_D13.md); original aliases: section record. Sources: [S311](SOURCES.md#S311), [S312](SOURCES.md#S312), [S313](SOURCES.md#S313), [S314](SOURCES.md#S314).

## [D13-S01](SOURCES.md#D13-S01) / primary_docs — PhysicalAI-SmartSpaces release and paper

Owner/publisher: **NVIDIA**. Dataset title *Physical AI Smart Spaces Dataset*. Repository API https://huggingface.co/api/datasets/nvidia/PhysicalAI-SmartSpaces returned HTTP200 and revision **`2cbe9563cbe9f47f846e5c871ee994572bbbc60e`**. Immutable card: https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/blob/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/README.md . Raw card HTTP200, 15,579 bytes. Card creation-history claims initial data collection December2023; real scene release June4,2026; Croissant/privacy additions July27,2026. These are card dates, not a verified recording date for each real video.

Paper: Yuxing Wang, Yizhou Wang, Anqi Li, Shuo Wang, Sameer Satish Pusegaonkar, Haoquan Liang, Jiajun Li, Shenxin Jiang, Jianhe Yuan, Shangru Li, Tongwei Dai, Zihao Chen, David C. Anastasiu, Sujit Biswas, Xunlei Wu, Zheng Tang, *Physical AI Smart Spaces: A Large-Scale Benchmark for Multi-Camera 3D Perception in Smart Spaces*, arXiv **2610.02580v1**, October1,2026. https://arxiv.org/abs/2610.02580 ; https://arxiv.org/html/2610.02580v1 . Direct HTML HTTP200; saved `smart_paper.txt` and extracted text. Relevant locators: §§3.2,3.5,4.1–4.3, concluding limitations. Do not infer publication/acceptance beyond the inspected preprint from its bibliography's conference string.

<a id="F212"></a>
### F212 — W1_D13: D13-F01 / artifact_access_checked + local_test — exact real assets exist, released GT does not accompany them

Provenance: [W1_D13:15](_WORK/W1_D13.md); original aliases: D13-F01. Sources: [S315](SOURCES.md#S315), [S316](SOURCES.md#S316).

### [D13-F01](RAW_FACTS.md#F212) / artifact_access_checked + local_test — exact real assets exist, released GT does not accompany them

The API's complete sibling list was parsed and all paths containing `Warehouse_026` or `Warehouse_027` saved in `real_tree.json`. Each scene contains only `calibration.json`, `vggt_reprojection_error.txt` and four/seven `videos/Camera_000N.mp4` files. There is **no `ground_truth.json`, track TXT, event JSON, depth map or map image under either real scene at this revision**. This is a claim about the checked release tree, not about all possible author-held assets. The card explicitly says these are real captures, first60s/1800 frames per camera, with video+calibration only and real ground truth/depth withheld. Its 2026 box counts therefore describe the synthetic scenes; the total scenes/camera-hours include the real scenes.

All video checks used `Range: bytes=0-1023`; all returned **206**, correct `Content-Range`, and an MP4 `ftypisom` prefix. They were individual MP4s, **not an archive whose annotation members might have been overlooked**. URL construction is exact and immutable:

`https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/<SCENE>/videos/<FILE>`

| Scene | Exact filename | Server-reported bytes |
|---|---|---:|
| Warehouse_026 | Camera_0000.mp4 | 19,802,011 |
| Warehouse_026 | Camera_0001.mp4 | 27,633,596 |
| Warehouse_026 | Camera_0002.mp4 | 38,707,343 |
| Warehouse_026 | Camera_0003.mp4 | 19,598,552 |
| Warehouse_027 | Camera_0000.mp4 | 36,433,143 |
| Warehouse_027 | Camera_0001.mp4 | 28,351,858 |
| Warehouse_027 | Camera_0002.mp4 | 29,101,239 |
| Warehouse_027 | Camera_0003.mp4 | 27,477,008 |
| Warehouse_027 | Camera_0004.mp4 | 22,303,508 |
| Warehouse_027 | Camera_0005.mp4 | 16,892,801 |
| Warehouse_027 | Camera_0006.mp4 | 23,613,453 |

Example complete binary URL: https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_026/videos/Camera_0000.mp4 . Every fully expanded URL and response is in `access.json`. Whole-file hashes and media-duration decoding were **not** performed; 1080p/30FPS/60s remain publisher documentation, corroborated for FPS/dimensions by calibration metadata, not decoded media observations.

<a id="F213"></a>
### F213 — W1_D13: D13-F02 / local_test — calibration is usable metadata, not certified distance accuracy

Provenance: [W1_D13:39](_WORK/W1_D13.md); original aliases: D13-F02. Sources: [S317](SOURCES.md#S317), [S318](SOURCES.md#S318).

### [D13-F02](RAW_FACTS.md#F213) / local_test — calibration is usable metadata, not certified distance accuracy

Both exact calibration URLs returned200 and were downloaded completely:

- https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_026/calibration.json —8,692 bytes, four sensors.
- https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_027/calibration.json —14,164 bytes, seven sensors.

Actual top-level keys: `calibrationType`, `sensors`. Per-camera fields include ID, `coordinates`, `scaleFactor`, attributes containing FPS/frameWidth/frameHeight, `intrinsicMatrix`3×3, `extrinsicMatrix`3×4, `cameraMatrix`3×4, `homography`3×3. Warehouse026 Camera0000 contains `translationToGlobalCoordinates`; Warehouse027 Camera0000 does **not**. Both observed `coordinates` are `(0,0)`, and `direction` attribute is empty. Code must tolerate these real-file differences rather than assume every illustrative README field is populated.

Paper §3.5 describes VGGT recovery of camera poses/point clouds, then a fitted dominant floor plane and normalized world frame. That is stronger than a manually drawn image-space zone but is not independent survey validation of a forklift safety envelope. The downloadable reprojection reports (same paths replacing `calibration.json` with `vggt_reprojection_error.txt`) returned200, 1,024 and1,468 bytes. Each summarizes1000 points. Warehouse026 mean0.0369/RMSE0.0542/max0.3630; Warehouse027 mean0.0660/RMSE0.0925/max0.6053. The reports call their dimension **“units”**; they do not establish that these numbers are metres or pixels. Do not report them as centimetre safety accuracy. No machine footprint, fork/load geometry, stopping-distance label or near-miss timing accompanies these calibration files.

<a id="F214"></a>
### F214 — W1_D13: D13-F03 / primary_docs — label schema and metric are tracking, not risky-event truth

Provenance: [W1_D13:50](_WORK/W1_D13.md); original aliases: D13-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [D13-F03](RAW_FACTS.md#F214) / primary_docs — label schema and metric are tracking, not risky-event truth

Released synthetic2025/2026 schema is per-frame: `object_type`, `object_id`, `3d_location [x,y,z]`, `3d_bounding_box_scale [w,l,h]`, `3d_bounding_box_rotation [pitch,roll,yaw]`, and `2d_bounding_box_visible {camera_id:[xmin,ymin,xmax,ymax]}`. It supports Person/Forklift and other mobile classes. It supplies geometry/identity and can support **derived** pair-distance/path diagnostics under assumptions. It does not give an author-certified pedestrian–forklift conflict event, event onset/offset, driver ownership, evasive action, site-policy violation or risk threshold. A visible2D box is not a full amodal footprint, and a 3D vehicle box may not encode forks, carried load and sweep on turning.

The real labels described in paper§3.5 were manually created in a global3D labeling UI, with projection into synchronized camera views. Their described existence does not make them downloadable. The benchmark evaluates **3D HOTA**, jointly detection/association/localization with3D IoU. Event recall, false alerts per eligible hour, duplicate alarms and time-to-alert are different evaluations. The official track also rewards causal online tracking, but this is a bonus condition, not proof that every leaderboard system is online.

<a id="F215"></a>
### F215 — W1_D13: D13-F04 / primary_docs — exact distribution/protocol inconsistency and rights scope

Provenance: [W1_D13:56](_WORK/W1_D13.md); original aliases: D13-F04. Sources: [S319](SOURCES.md#S319), [S320](SOURCES.md#S320), [S321](SOURCES.md#S321).

### [D13-F04](RAW_FACTS.md#F215) / primary_docs — exact distribution/protocol inconsistency and rights scope

Dataset card front matter says **CC BY4.0**. No separately verified model/code license follows from this data license; no weights were acquired in this branch. Exact Croissant: https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/croissant.json —HTTP200,13,588 bytes, saved `croissant.txt`.

At **the same revision**, Croissant `rai:personalSensitiveInformation` says the real target's raw frames are withheld and access occurs only through the challenge evaluator. `rai:dataSocialImpact` repeats this evaluation-only positioning. Paper concluding limitations similarly describe public splits as synthetic and the real target as withheld, with signed individual consent. Yet the README expressly announces the real video release and the eleven byte-access checks succeed. Possible explanation is stale generic privacy text or differently scoped “target”; **unknown**. Do not repair this contradiction by assuming either (a) all repository media is synthetic, (b) all real media is universally forbidden, or (c) CC BY metadata silently resolves all real footage use/protocol scope.

Official protocol sources: https://www.aicitychallenge.org/2026-faqs/ , GeneralQ9, and https://www.aicitychallenge.org/2026-track1/ . Browser web extraction returned their substantive official pages; direct Python HTTP requests returned403 and those failed responses were saved, so the local `.html` files are not snapshots of the substantive official content. FAQQ9 prohibits extra **manual test annotations for challenge participation**, discourages training on test data, describes automatically generated pseudo-labels as permissible with a tie-break preference against them, and requires reproducibility from training/validation/synthetic data for award verification. Track1 specifies RGB-only inference,3D HOTA and the+10% online-tracking bonus. These are challenge rules; they are not independently a replacement data license governing every external use. Paper/Croissant wording is stronger about exclusion from training. Record these separate scopes and preserve a benchmark holdout instead of hand-labeling it for this project's tuning. No clarification/outreach was attempted.

<a id="F216"></a>
### F216 — W1_D13: D13-F05 / inference — overlap and selection limits

Provenance: [W1_D13:64](_WORK/W1_D13.md); original aliases: D13-F05. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

### [D13-F05](RAW_FACTS.md#F216) / inference — overlap and selection limits

Card explicitly identifies CT2.5 paired rerenders:001/003/005/007/021/024 correspond to000/002/004/006/020/023 with the same geometry/cameras/GT and altered RGB. They are not six independent sites. Group source scene and its rerender, all synchronized camera views, and temporal episode before constructing a split. Random frame/clip split creates appearance/trajectory leakage. Real footage is only two1-minute synchronized site episodes: eleven camera-minutes are **two scene-minutes**, not eleven independent incidents or eleven minutes of independent safety exposure. No positive/negative event prevalence or class-by-scene real count has been established here; no full video review means no observed moving-near/stationary-near/driver-only controls can be claimed.

<a id="F217"></a>
### F217 — W1_D13: D13-S02 / primary_docs — a genuine real-forklift benchmark remains request-only

Provenance: [W1_D13:68](_WORK/W1_D13.md); original aliases: section record. Sources: [S148](SOURCES.md#S148), [S149](SOURCES.md#S149).

## [D13-S02](SOURCES.md#D13-S02) / primary_docs — a genuine real-forklift benchmark remains request-only

Hyeongjun Kim, Taejoo Kim, Won Jo, Jiwon Kim, Jeongmin Shin, Daechan Han, Yujin Hwang, Yukyung Choi, *Multispectral Benchmark Dataset and Baseline for Forklift Collision Avoidance*, **Sensors22(20),7953,2022-10-19**, DOI https://doi.org/10.3390/s22207953 . Primary full text https://pmc.ncbi.nlm.nih.gov/articles/PMC9608680/ ; actual direct request `?pdf=1` returned200 HTML234,784bytes, saved `multispectral_correct.txt`/`multispectral_correct_plain.txt`. Earlier `PMC9610749` was an incorrect identifier and must not be cited as this paper. Web extraction intermittently met CAPTCHA and MDPI429; the successful direct primary full text was read.

<a id="F218"></a>
### F218 — W1_D13: D13-F06 / author_claim, primary_docs:

Provenance: [W1_D13:72](_WORK/W1_D13.md); original aliases: D13-F06. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D13-F06](RAW_FACTS.md#F218) / author_claim, primary_docs:** TwoRGB/two thermal sensors ride on a real automated forklift in intralogistics; this is not a static warehouse CCTV camera observing a separate moving machine. §2.1.5 describes19,420 images per camera, manually labeled RGB-reference person boxes; aligned modalities share the transformed labels. Labels distinguish `person`, `people`, `background` and three occlusion levels. Centroid distances come from stereo matching/hole filling plus manual outlier removal and nearby depth averaging. These are centroid-depth annotations, not wheel/fork/load footprint distances or collision-event timestamps. Table2's rounded count19.5k and12.6k/20.6k train/test pedestrian counts differ from introductory20.2k-pedestrian wording: preserve the exact source table/paragraph rather than present a perfectly reconciled instance count. There is no inspected downloadable schema file, track-ID file, real archive or checkpoint.

<a id="F219"></a>
### F219 — W1_D13: D13-F07 / primary_docs:

Provenance: [W1_D13:74](_WORK/W1_D13.md); original aliases: D13-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D13-F07](RAW_FACTS.md#F219) / primary_docs:** The Data Availability Statement says access requires a request to the corresponding author and limits provided data to **non-profit purposes**. No request was sent. ArticleCC BY4.0 is a publication license and does not override this explicit data statement. No public archive/member, code license or pretrained SSD2.5D weight artifact was verified. Keep status **request-only**, not ready-public-download; a catalogue “dataset” entry or open-access paper is insufficient.

SSD2.5D is a method donor: RGB/thermal middle-feature fusion with centroid regression, not a matched ready CCTV proximity-event model. DetectionAP/MR and localizationALP, including braking-distance-derived warning/hazard subsets, do not measure third-party pair event recall. Hard cases named by authors include occlusion, low/irregular illumination and indoor background clutter. Four-sensor calibration/synchronization and moving-camera observations are original experimental conditions; a single fixed RGB camera cannot inherit their depth performance.

<a id="F220"></a>
### F220 — W1_D13: D13-S03 / primary_docs — older genuine warehouse tracking has an unresolved release link

Provenance: [W1_D13:78](_WORK/W1_D13.md); original aliases: section record. Sources: [S322](SOURCES.md#S322), [S323](SOURCES.md#S323).

## [D13-S03](SOURCES.md#D13-S03) / primary_docs — older genuine warehouse tracking has an unresolved release link

Syeda Fouzia and Reinhard Klette, *Comparing Trackers for Multiple Targets in Warehouses*, **International Journal of Fuzzy Logic and Intelligent Systems19(3):147–157,2019-09-25**, DOI https://doi.org/10.5391/ijfis.2019.19.3.147 ; official full text http://www.ijfis.org/journal/view.html?uid=876&&vmd=Full . Web tool returned full substantive article; direct HTTPS later disconnected, so access failure does not prove absence. Locators §§5–6, Table3, Acknowledgment.

<a id="F221"></a>
### F221 — W1_D13: D13-F08 / primary_docs:

Provenance: [W1_D13:82](_WORK/W1_D13.md); original aliases: D13-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[D13-F08](RAW_FACTS.md#F221) / primary_docs:** Paper describes a self-collected3,077-image training set,8,242 fork-truck/pedestrian ROIs, with added Caltech/INRIA pedestrian subsets. Three evaluation sequences are150frames/7tracks,614frames/21tracks and614frames/9tracks; difficulties low illumination, occlusion and clutter. Crown Equipment supported collecting sequences. This establishes a real warehouse tracking experiment, not public media availability. The inspected article has no exact downloadable dataset/track archive/checkpoint link. Ground-truth trajectory figures and MOT metrics are not released annotation files or risk-event GT. ArticleCC BY-NC3.0 is not a verified grant for underlying Crown video/code/weights. Status: **primary_docs experiment, unresolved artifact access**, not missing-everywhere and not a ready testpack.

<a id="F222"></a>
### F222 — W1_D13: D13-F09 / inference — why urban and other sibling donors do not close this branch

Provenance: [W1_D13:84](_WORK/W1_D13.md); original aliases: D13-F09. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D13-F09](RAW_FACTS.md#F222) / inference — why urban and other sibling donors do not close this branch

Urban autonomous-driving sources can stress person/vehicle perception or camera motion, but their road geometry, classes, viewpoint, scale, traffic rules and labels differ from forklift forks/load, reverse/sweep, warehouse occlusion and pedestrian/operator ownership. A projected overlap or small centroid distance is not a dangerous ground-plane encounter. A target-domain incident threshold depends on machine motion, footprint and applicable site procedure. A pretrained road detector's AP is not industrial event validation. Even real onboard-forklift depth is not a fixed-camera observed pair.

The prior M06 NearCollision six-frame/HDF5 donor predicts proximity to its own suitcase camera in university buildings; D09SARD construction actions and safe/unsafe factory clip classes do not suddenly become pair-risk GT. Older keremberke person/forklift weights are a detector donor, not a near-miss annotation source. Existing NVIDIA generated event controls remain synthetic. These sibling results are pointers, not newly rechecked primary artifacts in this branch. This branch deliberately adds a stronger real-data access/withheld-GT distinction rather than another long generic list.

<a id="F223"></a>
### F223 — W1_D13: D13-F10 / hypothesis — realistic baseline testpack and admission gate

Provenance: [W1_D13:90](_WORK/W1_D13.md); original aliases: D13-F10. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D13-F10](RAW_FACTS.md#F223) / hypothesis — realistic baseline testpack and admission gate

**Implementable baseline:** person+machine detections → stable per-class tracks → camera-corrected observed machine movement → ordered pedestrian/machine pairs → configured ground-envelope/path rule and temporal confirmation → one event/notification until clear/rearm. HostCPU tracking/rules are plausible architecture choices, not measured LinQ support. If calibration is unverified, report an image-space corridor/exclusion-zone proxy; do not print metres or TTC from bbox overlap. Forklift driver must be associated with vehicle/cab and excluded from free-pedestrian pairs; uncertain ownership remains unknown. Loss of either track during occlusion must not mean safe.

**Proposed small development pack:** permissioned real target footage with at least moving-machine/near-pedestrian, moving-machine/far-pedestrian, stationary-machine/near-pedestrian, driver-only, pedestrian crossing after machine clears, reverse/turn, barrier-separated apparent overlap, occlusion/reappearance and detector dropout. These are coverage cells, not an invented numerical accuracy SLA or statistical sufficiency claim. Use existing routine recordings or safe normal operations; no staged dangerous near miss is required. Accessible external routine clips can be supplementary stress donors only after their rights and full timeline are reviewed. SmartSpaces real holdout is not an automatically relabelable replacement given the release/protocol contradiction above.

Proposed annotation contract: `source_id`, camera/site/session, source hash and PTS/timebase; person/machine track IDs; pedestrian/driver/unknown ownership; machine moving/stationary/unknown; visible/occluded/out-of-frame; ground-contact uncertainty; machine footprint/load/exclusion policy if known; pair-specific near/path-crossing event onset, confirmation, clear, censoring and reviewer agreement. Separate physical incident, policy violation and configured visual-risk proxy. No event truth should be generated simply by applying the evaluated model's own threshold to its own tracks.

Split by site/camera session/source episode; isolate reviewed development from blind holdout; keep paired views and generated rerenders together. Annotate original-rate timestamps first, then run **causal** inference cadence/phase/dropout simulations. A short approach between1FPS samples is a miss, not an absent event. Evaluate event recall, time-to-alert from a defined reference onset, false alarms per fully reviewed eligible hour, duplicate notifications and rearm/ID-switch behavior. Unknown/hidden frames are not normal negatives. Trimmed EOF is censoring, not observed clearance. No speed/device/SLA claim is established until actual LinQ inference, output contract and end-to-end timing are measured.

<a id="F224"></a>
### F224 — W1_D13: Remaining unknowns and evidence inventory

Provenance: [W1_D13:100](_WORK/W1_D13.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Remaining unknowns and evidence inventory

1. Whether public real SmartSpaces videos and Croissant privacy statements refer to exactly the same target distribution, and what reuse scope the publisher intends outside challenge participation. Both forms coexist at the pinned revision; preserve this discrepancy.
2. Whether an official release of real tracks/events exists outside this checked tree; current card explicitly withholds realGT. The research did not establish a ready public real person–moving-machine positive/control event pair.
3. Real footage control coverage and true machine/driver content are unobserved here because only byte prefixes were read.
4. Multispectral benchmark actual downloadable files, source-level schema, temporal IDs/splits, weight/code artifacts and authorization remain unreceived; request-only/non-profit stands.
5. Older warehouse tracker source recordings/tracks/weights and underlying reuse grant remain unresolved.

Private `_WORK/D13/` contains complete HFAPI listing, pinned-ID access log and complete real-path list; card/Croissant/paper snapshots; both calibrations and reprojection reports; correct multispectral primaryHTML/plain text; failed direct officialFAQ/track403 bodies. Metadata was small (no complete media/model). No inference/local model evaluation occurred, no public bundle was created, and no model licensing claim was inferred from dataset metadata.

<a id="F225"></a>
### F225 — W1_D14: W1 D14 — real lifting/smoking videos, attachment semantics, and fire confusers

Provenance: [W1_D14:1](_WORK/W1_D14.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D14 — real lifting/smoking videos, attachment semantics, and fire confusers

Research/access: **2026-10-23, 19:50–19:57 UTC** (22:50–22:57 Moscow). Exclusive evidence: `_WORK/W1_D14_EVIDENCE/`. No models executed, exported or trained; no paid computation, outreach or whole large collection downloaded. `local_test` below means actual JSON/archive parsing or video decoding, not neural inference. Source snapshots, hashes and filesystem UTC write times are preserved in `sha256_manifest.json`, `evidence_write_times_UTC.json`; initial HTTP timestamps are in `access1.json`.

<a id="F226"></a>
### F226 — W1_D14: Branch question and decision

Provenance: [W1_D14:5](_WORK/W1_D14.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

Which remaining sources provide **actual video + usable semantics**, beyond the previous FURG/FIRESENSE fire audit, generic action labels, static harness images and synthetic safety demonstrations?

**Decision [inference]:** add **SAFELIFT v1** as a concrete measured lifting/lowering development donor, and two acquired **HMDB51 smoke** clips as visible-smoking development examples. Neither establishes industrial rule violations. SAFELIFT has important annotation defects and requires external dimensions/height and assumed load; HMDB lacks dense person/event truth and has movie/web provenance. Do not promise a general improper-carrying, correctly-connected-harness, completed fence crossing, or unsafe-under-load detector from these donors.

New negative leads **MmodalFire** and **FSAV** sharpen the plan: the former really includes laboratory non-fire mist/dry-ice controls but lives in a 4.93 GB archive not acquired here; the latter explicitly models false-fire/smoke tracks but its derived labels/splits require an author request. No new independent additional hazard meets the ready-data-plus-method bar in this branch. Do not fill the requested 1–2 slots by relabeling core scenario 8 as an extension. The M08 aggression proposal is a separate branch, not new D14 evidence.

<a id="F227"></a>
### F227 — W1_D14: D14-F01 — SAFELIFT: acquired real videos, endpoint measurements, no universal unsafe label

Provenance: [W1_D14:13](_WORK/W1_D14.md); original aliases: D14-F01. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D14-F01](RAW_FACTS.md#F227) — SAFELIFT: acquired real videos, endpoint measurements, no universal unsafe label

**[primary_docs; artifact_access_checked]** Dibenedetto, Lops, Lovreglio, Polignano, Ravallese and Torkamaan, *SAFELIFT Dataset: Safety-Aware Feedback for Ergonomic Lifting & Injury-Free Tasks*, Zenodo **18243098, v1**, published 2026-01-14; IUI2026 paper DOI **10.1145/3742413.3789143**. Record describes controlled package lifting. Source code is author-linked, pinned by `git ls-remote HEAD` to **e2ebe5098ba6354d4f53217f32a94be589349570**. GitHub API metadata returned403; do not invent the commit date.

<a id="F228"></a>
### F228 — W1_D14: Actual acquisition

Provenance: [W1_D14:17](_WORK/W1_D14.md); original aliases: section record. Sources: [S324](SOURCES.md#S324), [S325](SOURCES.md#S325), [S326](SOURCES.md#S326), [S327](SOURCES.md#S327), [S328](SOURCES.md#S328).

### Actual acquisition

| Artifact | Exact URL | Observed result |
|---|---|---|
| Record metadata | https://zenodo.org/api/records/18243098 | GET200,10,449B, saved |
| Annotations | https://zenodo.org/api/records/18243098/files/annotations.json/content | GET200,179,489B, full local JSON parsed |
| Subject count text | https://zenodo.org/api/records/18243098/files/count_subjects.txt/content | GET200,2,110B |
| Env2 frontal videos | https://zenodo.org/api/records/18243098/files/video_env_2_anonymized.zip/content | GET200,**4,253,000B**, full ZIP acquired and extracted |
| Env2 oblique videos | https://zenodo.org/api/records/18243098/files/video_env_2_oblique_anonymized.zip/content | Listed4,425,143B; **not downloaded** |

SHA256 annotations: `85472b2a750d74128f9fb83c69295467b1c32701926727c1b764a765c529b596`; acquired ZIP: `ba3298f0021eecfd12835699e3c5ae43543ebe65508ef4cb45c86e0a2db46648`. Zenodo publishes ZIP MD5 `8aaeca97486306041eeb0c4ae5d94f5c`; our SHA is independent. Other archive sizes in the saved metadata range25.5–247.8MB, not acquired. Do not describe all510.9MB as downloaded.

**[local_test: JSON parsing]** `annotations.json` is a list of **182 records/182 unique video basenames**, not dense frame boxes or a normalized event table. Top-level keys: `video`, `box_width_cm`, `box_height_cm`, `box_depth_cm`, `subject_height_cm`, `action_start`, `action_end`, `subjective_judgment`, `one_hand_lifting`, `multiple_subjects_lifting`, `subject_age`, `subject_gender`, `Note`. Each endpoint contains `video_second`, box bottom height, horizontal distance from midpoint of ankles, hand height and asymmetry angle. Unknown values are the **string `unknown`**, not numeric zero.

Independent completeness audit (`annotation_completeness.json`):

- `subjective_judgment`: **176 unknown,6 intermediate**. There is no observed safe/unsafe binary distribution to train or evaluate.
- `one_hand_lifting` and `multiple_subjects_lifting`: **False for all182**; these flags cannot supply positive one-hand/team-lift violations.
- Horizontal distance unknown in33/182 at **each** endpoint; hand height unknown in66/182 at **each** endpoint.
- Four records have **start second greater than end second**: `dn_0002_dg.mp4`, `dn_0004_dg.mp4`, `dn_0006_dg.mp4`, `dn_0008_dg.mp4`. Their video was not downloaded, so this is a schema/timing flag, not a proven correction. It might encode endpoint order differently; verify with source media before swapping times.
- No top-level actual load-mass, frequency, grip-quality, person-track or carrying-route key. Physical safety cannot be derived from just these endpoints.

**[local_test: video decoding; visual inspection]** PyAV18.1.0 fully decoded all **8 Env2 clips,1,647 frames**, 480×864, average rate749/25 (~29.96fps), valid decoded PTS. `safelift_decode_audit.json` preserves all hashes and original annotations. OpenCV was unavailable; PyAV succeeded without installation. Contact sheet visually inspected for two clips, eight time samples each; the other six were decoded but not independently visually labeled frame by frame.

| Member | Frames; last PTS | Original endpoint annotation | Direct visual observation / limit |
|---|---|---|---|
| `video_env_2_anonymized/jv-scrivania-terra-001.mp4` |195;6.475300s | start1s,end4s; box bottom70→0cm, hand103→33cm, horizontal73→36cm | Person lowers white box from desk to floor, bends/knees flex, releases and stands. At4.005s sampled frame box still near floor in hands; by5.007s near release. Treat integer endpoints as coarse measurements, not precise release GT. |
| `video_env_2_anonymized/md-scrivania-sedia-001.mp4` |219;7.276368s | start1s,end5s; box bottom70→46cm, hand103→79cm | Desk-to-chair lowering; face blurred; chair obscures part of interaction. Not prolonged carrying and no mass evidence. |
| Other6 |193,214,243,208,156,219frames | Mixed floor/chair/desk endpoint transitions | Decode/access confirmed; separate visual review still required. |

Two clip SHA256s respectively `0c1e1be9d5ea887aecb3f5de860db045953d1675d5e31b8e2f342b94d3793b3f` and `3c69dae1d7ed24f8d3b7897fd90407f67ba7dc10219e1ca487d687d276b43843`. PTS0 starts exactly0 here; this differs from acquired HMDB clips below.

**[primary_docs: exact code]** `main.py` lines251–280 initializes easy_ViTPose `h`, default `coco_25`, single_pose=True, `JunkyByte/easy_ViTPose` weights `torch/coco_25/vitpose-h-coco_25.pth`, auxiliary `yolov8/yolov8n.pt`; lines380/391 use `yoloe-11l-seg.pt` and MiDaS. Line442 reads known `subject_height_cm`. Linked README describes endpoint recommendation with assumed10kg and threshold0.7. These are author settings, not measured CCTV capability. Source main/compute/utils/requirements/LICENSE were retrieved at the pinned commit, no dependencies or model weights downloaded or run here. Exact model URLs are found in code, but the huge ViTPose branch and all component grants require their own verification.

**[inference]** A bounded pilot can estimate visible two-hand lift/lower endpoints and report posture measurements against known box/site geometry. It cannot identify mass, fatigue, force, coupling or all RNLE factors from distant RGB. Full recommendation computation also consumes end-of-lift information, so it cannot notify before observing that endpoint without a changed causal rule. Keep a past-only provisional warning distinct from retrospective scoring. The dataset’s current effective risk labels do not support claiming a trained unsafe-carry classifier.

**Rights [primary_docs; unknown]:** both Zenodo description and pinned repository LICENSE state **CC BY-NC-SA4.0**. This is a noncommercial restriction for these artifacts; it is separate from YOLOE/MiDaS/ViTPose/easy_ViTPose/component weight terms. Paper openness is not a commercial data grant. Consent/ethics approval is reported by authors, not independently audited. Front/oblique simultaneous recordings, same subjects and same box/site must be grouped before train/validation/test; no ready source-disjoint split was established.

<a id="F229"></a>
### F229 — W1_D14: D14-F02 — HMDB51 smoking: two real acquired clips,110-member class, versioned current rights statement

Provenance: [W1_D14:55](_WORK/W1_D14.md); original aliases: D14-F02. Sources: [S329](SOURCES.md#S329), [S330](SOURCES.md#S330).

## [D14-F02](RAW_FACTS.md#F229) — HMDB51 smoking: two real acquired clips,110-member class, versioned current rights statement

**[primary_docs]** Kuehne/Jhuang/Garrote/Poggio/Serre, *HMDB: A large video database for human motion recognition*, ICCV2011. The old Brown URL redirects to homepage; current official resource is https://serre.lab.brown.edu/hmdb51.html . It directly links the official **Serrelab/hmdb51** HF release. HF metadata current revision **1f1e6df3fccdfe34a230e60c00a799b82905b35f**, lastModified2026-03-09T12:09:31Z; README names itself the official release. Both current official page and HF card explicitly state **CC BY4.0**. Preserve that exact new version rather than silently repeating historical third-party NC statements. Original movie/web footage provenance remains a distinct rights question; this does not prove every film producer cleared redistribution.

**[artifact_access_checked; local_test: RAR parsing]** Source URL:

https://huggingface.co/datasets/Serrelab/hmdb51/resolve/1f1e6df3fccdfe34a230e60c00a799b82905b35f/hmdb51_org.rar

First64KiB range GET206 established total **2,124,008,126B**; full outer archive **not downloaded**. Five small RAR-header range requests located stored member `smoke.rar`: outer header offset119,112,737, length46; exact payload byte range **119112783–162147750**, GET206 **43,034,968B**. That bounded class archive alone acquired; SHA256 `a3e3ed9e6c81921bed82a1f7334cbcc576e94a0c5ac5da8d1a6fd5801404ac4a`. Archive manifest has **110 entries:109 AVI files and1directory**, class is `smoke`. Do not confuse it with fire-plume semantic class `smoke` in object detectors. `hmdb_outer_scan.json`, `hmdb_smoke_manifest.json` preserve offsets, sizes and CRCs.

Two members extracted with local7-Zip25.01 and fully decoded by PyAV;295frames total. A first rarfile attempt failed to find an extraction backend; explicit installed7-Zip path then succeeded. No downloaded executable or model execution.

| Member (within smoke.rar) | Acquired bytes / actual video | SHA256 |
|---|---|---|
| `smoke/After_work_smoke_in_the_garage_smoke_h_nm_np1_fr_med_1.avi` |426,496B;236frames;320×240;30fps; PTS0.033333…7.866667s | `d7fc934930c2a999ec312e838d86962f1a2a226a1c30ee7e54d9cfc93997ef17` |
| `smoke/American_History_X_smoke_h_nm_np1_fr_goo_26.avi` |142,848B;59frames;320×240;30fps; PTS0.033333…2.0s | `7f7d1edc97512c890f4763a04fd83409edc6f950ffb9460d992dcf1b9f379d95` |

**[local_test: decode; visual inspection]** Six sampled frames per clip inspected in `hmdb_smoke_contact.jpg`. Garage clip: dark close-up, cigarette brought to lips, glowing point and exhaled plume; later frames hands away while plume/episode context continues. Movie clip: **shot cut** between first sampled medium scene and close-up; hand-to-mouth/exhalation visible, black letterbox bands. These are stronger positive examples than an unverified internet URL, but cover neither distant factory workers nor normal hard negatives. Sampling did not create manual frame/puff GT.

**[inference]** Clip class is not dense event start/end, person localization, puff-cycle count or forbidden-zone status. A smoker can hold the object between puffs, and a hand-to-face model can confuse drinking/eating/inhalers/radio/face touching. Split **source film/channel/actor scene** before window extraction; names show multiple American History X and same garage-source clips, so random clip splitting is insufficient for source independence. Native train/test splits were not acquired or independently audited here. Acquired clips are development evidence, not a hidden test set. Existing generic HMDB recognition checkpoints may have trained on them: do not claim independent evaluation.

<a id="F230"></a>
### F230 — W1_D14: D14-F03 — smoking temporal prototype: downloadable artifacts, weak training contract

Provenance: [W1_D14:76](_WORK/W1_D14.md); original aliases: D14-F03. Sources: [S331](SOURCES.md#S331), [S332](SOURCES.md#S332).

## [D14-F03](RAW_FACTS.md#F230) — smoking temporal prototype: downloadable artifacts, weak training contract

**[primary_docs; artifact_access_checked]** https://github.com/aaryan-maker/smoking-and-posture-detection pinned **c9365ac40642db110577d8ebc6f46f578f4dff7a** by git ls-remote; commit date unknown. Raw `prepare_action_data.py`, `train_action_model.py`, `action_predictor.py`, `main.py`, `action_labels.json`, README fetched. HEAD `action_model.keras`200/**4,817,524B**, scaler200/**2,872B**; neither downloaded/deserialized/executed. Direct weight URL:

https://raw.githubusercontent.com/aaryan-maker/smoking-and-posture-detection/c9365ac40642db110577d8ebc6f46f578f4dff7a/action_model.keras

**[primary_docs]** This CNN/BiLSTM uses30 poses with velocity/acceleration, four classes smoke/sit/stand/walk. Preparation code lines373–415 skips failed poses and retains only the first30 **successful** poses; it discards timestamps. Thus30 items do not guarantee30 adjacent frames or fixed1s. Training uses stratified random sequence split, not verified source-film split. No eating/drinking class or event metric was established. Media are absent. LICENSE URL404 means **license not found at that path**, not proof no license anywhere. Weight/code/data rights are unresolved. Keep this as a reproducibility/sampling caution, not selected production smoking supply; a pose signal alone cannot verify the cigarette.

<a id="F231"></a>
### F231 — W1_D14: D14-F04 — fire negatives with a localized acquisition gap

Provenance: [W1_D14:84](_WORK/W1_D14.md); original aliases: D14-F04. Sources: [S333](SOURCES.md#S333), [S334](SOURCES.md#S334), [S335](SOURCES.md#S335), [S336](SOURCES.md#S336).

## [D14-F04](RAW_FACTS.md#F231) — fire negatives with a localized acquisition gap

**[primary_docs; artifact_found; unknown video access]** Jia/Guo/Chen/Zhang/Wang/Zhang, *MmodalFire: A Continuous Multimodal Dataset Comprising Video and Physical Sensing Data for Detecting Indoor Fires*, Scientific Data13,489,2026-02-19, DOI10.1038/s41597-026-06810-6. Direct publisher HTML GET200 saved; Figshare API https://api.figshare.com/v2/articles/28804448 GET200. **v1**, CC BY4, one file **MmodalFire.rar 4,929,210,010B**, URL https://ndownloader.figshare.com/files/53696243 . No archive/video downloaded.

Publisher reports65 controlled laboratory recordings, four fuels, non-fire **dry ice and humidifier water mist**, synchronized physical sensors, binary sequence labels. Useful mist confuser lead, not evidence about legal hot work/furnace/welding. Article contains acquisition camera30fps versus preprocessing12fps descriptions, and45s-plus versus700min aggregate claims; actual files need inspection. Code https://github.com/SiliconSisyphus/MultiModal-fire-detection is a published lead, not independently pinned/tested here. Reported random laboratory sampling/overlapping subsequences is not a strict camera/lab holdout. Do not use multimodal benchmark accuracy as RGB CCTV accuracy. Await bounded archive-member/annotation inspection if selected later.

**[primary_docs; artifact not acquired]** Ghimire/Kim/Jo/Lee/Jeong/Kim, *STV-FSANet*, Sensors26(15),4970,2026-08-05, DOI10.3390/s26154970; primary publisher search-index fulltext plus PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC13469129/ . Direct publisher fetch403 and web open429; PMC open bot-check. Primary **Data Availability Statement** explicitly makes derived FSAV annotations/splits request-only and says restricted Kim–Lee media cannot be redistributed. No public checkpoint/annotation download was established; no outreach made. It models fire/smoke/false-fire-smoke from candidate tracks and drops fragments below5 observations at10fps. This supports testing detector misses, broken tracks and suppressed short events; its fixed-tracklet scores are not industrial event recall. Do not call its58,733 tracks a downloaded public benchmark. Article license does not grant underlying six source collections.

<a id="F232"></a>
### F232 — W1_D14: D14-F05 — height/harness: actual reported video is not downloadable attachment truth

Provenance: [W1_D14:92](_WORK/W1_D14.md); original aliases: D14-F05. Sources: [S337](SOURCES.md#S337).

## [D14-F05](RAW_FACTS.md#F232) — height/harness: actual reported video is not downloadable attachment truth

**[primary_docs; author_claim; unknown artifact]** Wu/Li/Long/Zhang/Wan/Mei, *A Remote-Vision-Based Safety Helmet and Harness Monitoring System Based on Attribute Knowledge Modeling*, Remote Sensing15(2),347,2023-01-06, DOI10.3390/rs15020347, https://www.mdpi.com/2072-4292/15/2/347 . Primary indexed sections4.1/3.4/Data Availability read; direct GET403, web429. Reports four30fps2560×1080videos/7,200frames, three height scenes and one ground scene; bbox/attribute labels for workers, helmets and harnesses. Data availability is **on request**; no file acquired and no data/weight license grant independently found. Previous30-frame majority interpolation is an author smoothing choice, not proof of present safety equipment through occlusion.

**[inference]** These wearing labels differ from: harness fitted correctly; lanyard belongs to this worker; connector closed; connector fastened to approved anchor; continuous100% tie-off through transitions; anchor rated; fall clearance sufficient. A visible chest strap or hook box cannot prove that relational chain. A hidden tether is **unknown**, not absent. Height must come from surveyed surface/camera geometry or explicit zone policy. Do not import a broad “properly secured at height” claim from static PPE labels or this request-only video lead. Reflective vest/backpack/tools crossing the chest, scaffold rail and another worker’s tether are target confusers.

<a id="F233"></a>
### F233 — W1_D14: D14-F06 — UW-IOM: real temporal action donor, access not yet localized

Provenance: [W1_D14:98](_WORK/W1_D14.md); original aliases: D14-F06. Sources: [S338](SOURCES.md#S338), [S339](SOURCES.md#S339).

## [D14-F06](RAW_FACTS.md#F233) — UW-IOM: real temporal action donor, access not yet localized

**[primary_docs]** Parsa et al., UW Indoor Object Manipulation **v3,2020-11-02**, DOI10.17632/xwzzkxtf9s.3, https://data.mendeley.com/datasets/xwzzkxtf9s/3 . Original page GET200 saved. It describes20 participants, Kinect~12fps, box/rod pick-place-carry sequences and17 hierarchical action labels; data CC BY4. The page says empty boxes, whereas the associated paper’s abstract mentions varying weights: do not assume a mass label from that abstract. Code https://github.com/BehnooshParsa/HumanActionRecognition_with_ErgonomicRisk is original STCN training lead (2019); no exact trained weights inspected here.

Mendeley UI initial state has empty file list pending JS load. Probed API paths returned404 or400; JS-derived root-folder query returned200`[]`, not a verified empty dataset. **No UW-IOM video/annotation acquired**; folders/file identifiers remain unresolved. Keep as secondary action-segmentation donor, not exact improper-carrying ground truth or absent public data.

<a id="F234"></a>
### F234 — W1_D14: Scenario decisions and evaluation controls

Provenance: [W1_D14:104](_WORK/W1_D14.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Scenario decisions and evaluation controls

| Scenario | Strongest D14 addition | What remains missing |
|---|---|---|
| Smoking | Two genuine acquired/decoded HMDB clips; temporal-prototype code audit | Person/puff/onset/offset/forbidden-zone labels; distant factory positives; eating/drinking/radio/inhaler negatives; independent source-film split |
| Open fire | MmodalFire real nonfire mist/dry-ice source; FSAV verification failure modes | Acquired mist members; actual allowed furnace/welding/steam plant footage and permit state; smoke-only versus flame origin; short ignition/clear/rearm episodes |
| Manual handling | SAFELIFT8decoded clips + physical endpoint metadata + exact method code | Mass/frequency/coupling/work rule, complete numeric GT, corrected timing, team/one-hand positives, sustained carrying and independent target holdout |
| Height/harness | Reported4video wearing benchmark localized as request-only | Downloadable media/annotations/rights; actual connector-anchor-person relation; surveyed height and visibility labels |
| Fence/under-machine/suspended load | No stronger exact real violation video found in this branch | M07’s fence-climbing and synthetic suspended-load distinctions remain; do not promote generic climb/crawl labels to crossing/under-load truth |

**[inference/proposed evaluation]** Preserve actual decoded PTS and all negative exposure time. Label actor, event evidence, action phase, permitted/forbidden context, visible/occluded/unknown and source policy separately. A bent worker deliberately lowering a box and someone kneeling under equipment for authorized maintenance are required negatives for unsafe-posture and under-machine rules. A flame inside a permitted furnace/hot-work area may still be fire visually: retain detection, evaluate the authorization decision separately. Welder/PPE, steam plume, flame on a monitor, orange clothing/reflections, another worker’s harness, and repair crouch must be explicit categories; none is claimed acquired just because a donor’s folder name mentions welding.

Before future3090 experiments: choose exact local handling rule, correct SAFELIFT schema/timing exceptions against downloaded videos, group frontal/oblique/subject recordings, create new dense target labels, then compare pose/track rules with a trailing-window model. Measure episode recall/false alerts per camera-hour/onset latency/duplicate alarms and occlusion/short-event strata, not only clip accuracy or endpoint metric error. Unknown LinQ SDK/device/operator support and CPU throughput remain independent gates.

<a id="F235"></a>
### F235 — W1_D15: W1 D15 — Temporal event annotations, QA and leakage protocol

Provenance: [W1_D15:1](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D15 — Temporal event annotations, QA and leakage protocol

Checked 2026-10-23, 22:24–22:30 Europe/Moscow (19:24–19:30 UTC). Branch question: which existing annotation formats and evaluation implementations support an honest industrial CCTV event benchmark, and what must our own labels add?

**Decision [inference]:** retain original tool-native exports plus a versioned event JSONL sidecar and media/PTS manifest. CVAT is the spatial/tracking/pose editor; VIA3 is a lightweight offline temporal-span option. Neither exporter alone represents policy context, uncertainty, interrupted observation and incident lifecycle. Use one-to-one actor/pair-compatible event matching, causal replay and independently annotated continuous negative exposure. Classification accuracy, per-frame AP and unqualified temporal IoU cannot replace this benchmark.

Read full branch prompt, Context-prompt.md, CASE_NOTES.md, SYNTHESIS_CONTRACT.md, targeted prior feasibility report and W1 M02/M03. Case notes are root's direct case reading, not this worker's independent PDF observation. No models, tracker, video or LinQ inference executed; no training, paid compute, large media download, outreach or subagents. `local_test` means only actual CSV/source parsing. Proposed protocols below have status `hypothesis`.

<a id="F236"></a>
### F236 — W1_D15: Findings that change decisions

Provenance: [W1_D15:33](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Findings that change decisions

<a id="F237"></a>
### F237 — W1_D15: D15-F01 [primary_docs] CVAT needs a policy/time sidecar.

Provenance: [W1_D15:35](_WORK/W1_D15.md); original aliases: D15-F01. Sources: [S349](SOURCES.md#S349), [S350](SOURCES.md#S350), [S351](SOURCES.md#S351).

**[D15-F01](RAW_FACTS.md#F237) [primary_docs] CVAT needs a policy/time sidecar.** XML1.1 video tracks contain object IDs, frame-indexed boxes, outside/occluded/keyframe, manual/auto source and attributes; skeleton points have visibility flags. These are task-local track identities, not global people or events. An interpolated location is not independent observed action evidence. Keep native export and original index→PTS mapping; nominal FPS cannot represent variable cadence/drops. [[D15-S01](SOURCES.md#D15-S01)]

<a id="F238"></a>
### F238 — W1_D15: D15-F02 [primary_docs] QA export can lose disagreement evidence.

Provenance: [W1_D15:37](_WORK/W1_D15.md); original aliases: D15-F02. Sources: [S352](SOURCES.md#S352), [S353](SOURCES.md#S353).

**[D15-F02](RAW_FACTS.md#F238) [primary_docs] QA export can lose disagreement evidence.** CVAT consensus replicas are independent jobs excluded from task-level annotation import/export; per-job exports work. Merging overwrites parent annotations. Save each opinion before merge; a gold-frame comparison/majority does not resolve an invisible temporal boundary. [[D15-S02](SOURCES.md#D15-S02)]

<a id="F239"></a>
### F239 — W1_D15: D15-F03 [primary_docs; artifact_access_checked] VIA3 is a real offline temporal option.

Provenance: [W1_D15:39](_WORK/W1_D15.md); original aliases: D15-F03. Sources: [S354](SOURCES.md#S354), [S355](SOURCES.md#S355), [S356](SOURCES.md#S356), [S357](SOURCES.md#S357), [S358](SOURCES.md#S358).

**[D15-F03](RAW_FACTS.md#F239) [primary_docs; artifact_access_checked] VIA3 is a real offline temporal option.** It supports temporal segments and spatial regions, project JSON and annotation exports, in a standalone browser tool; VIA2 is image-only. Archive availability checked, GUI not run. Preserve original project; converter must retain attribute IDs/times. Censoring/person-pair policy remain our additions. Code BSD-2-Clause does not clear annotated videos. [[D15-S03](SOURCES.md#D15-S03)]

<a id="F240"></a>
### F240 — W1_D15: D15-F04 [primary_docs] Temporal mAP differs from alert quality.

Provenance: [W1_D15:41](_WORK/W1_D15.md); original aliases: D15-F04. Sources: [S359](SOURCES.md#S359).

**[D15-F04](RAW_FACTS.md#F240) [primary_docs] Temporal mAP differs from alert quality.** ActivityNet segment evaluation uses class/video/time at tIoU0.50:0.05:0.95; confidence-ranked predictions and GT locks allow one match per threshold, duplicates become FP. Schema lacks actor pairs and notification clock. Adopt one-to-one matching principle, not mAP as safety SLA. [[D15-S04](SOURCES.md#D15-S04)]

<a id="F241"></a>
### F241 — W1_D15: D15-F05 [primary_docs] Endpoint/matching choices matter.

Provenance: [W1_D15:43](_WORK/W1_D15.md); original aliases: D15-F05. Sources: [S360](SOURCES.md#S360), [S361](SOURCES.md#S361).

**[D15-F05](RAW_FACTS.md#F241) [primary_docs] Endpoint/matching choices matter.** sed_eval exposes onset/offset collars and optimal graph matching versus order-sensitive legacy greedy matching. Defaults0.2s/50% duration are audio defaults, not industrial tolerances. Event true negatives are undefined; negative exposure needs rates. [[D15-S05](SOURCES.md#D15-S05)]

<a id="F242"></a>
### F242 — W1_D15: D15-F06 [primary_docs] AVA is not dense event-boundary GT.

Provenance: [W1_D15:45](_WORK/W1_D15.md); original aliases: D15-F06. Sources: [S111](SOURCES.md#S111), [S201](SOURCES.md#S201).

**[D15-F06](RAW_FACTS.md#F242) [primary_docs] AVA is not dense event-boundary GT.** AVA2.2 labels persons/actions at1-second intervals, allows multi-label rows and supplies included/excluded timestamps; IDs link adjacent boxes within video. Version2.2 added2.5% missing labels;2.1 removed duplicate movies. Preserve revision/masks. Sampled phone+walk joins do not give exact violation onset or clear time. [[D15-S06](SOURCES.md#D15-S06)]

<a id="F243"></a>
### F243 — W1_D15: D15-F07 [primary_docs; local_test: CSV only] OmniFall separates transition/state but merges running into walk.

Provenance: [W1_D15:47](_WORK/W1_D15.md); original aliases: D15-F07. Sources: [S070](SOURCES.md#S070).

**[D15-F07](RAW_FACTS.md#F243) [primary_docs; local_test: CSV only] OmniFall separates transition/state but merges running into walk.** Independently fetched labels confirm fall1, fallen2, lie_down5, lying6; fallen may contain movement; walk0 includes jogging/running. CSV has458 segments; split files75/48/37 paths, train subject prefixes1/3, val2, test4. Thus known Subject1/3 examples are development, fallen is not immobility GT. Pitfalls document multiview labels beyond EOF. No source-video timing verified here. [[D15-S10](SOURCES.md#D15-S10); [M03-F01](RAW_FACTS.md#F070)/F02/F03]

<a id="F244"></a>
### F244 — W1_D15: D15-F08 [primary_docs; inference] Duplicate detection needs sequence context.

Provenance: [W1_D15:49](_WORK/W1_D15.md); original aliases: D15-F08. Sources: [S363](SOURCES.md#S363).

**[D15-F08](RAW_FACTS.md#F244) [primary_docs; inference] Duplicate detection needs sequence context.** DataEval exposes aligned/resampled relations and asymmetric containment: a test clip entirely inside a long training video can be fully leaked despite small train containment. Inspect candidate aligned runs; example hash thresholds are not universal guarantees. No dedup execution. [[D15-S08](SOURCES.md#D15-S08)]

<a id="F245"></a>
### F245 — W1_D15: D15-F09 [primary_docs; inference] Causality includes the tracker adapter.

Provenance: [W1_D15:51](_WORK/W1_D15.md); original aliases: D15-F09, M02-F05. Sources: [S362](SOURCES.md#S362).

**[D15-F09](RAW_FACTS.md#F245) [primary_docs; inference] Causality includes the tracker adapter.** Online-action definition uses frames observed so far. [M02-F05](RAW_FACTS.md#F056)/F06/F07/F08 supply exact separate code findings: retained IDs can be omitted from emitted results, output boxes can be predictions, retrospective interpolation uses future endpoints. This branch did not rerun trackers. No output is not clear/safe; repaired hidden path is not observed hidden action. [[D15-S07](SOURCES.md#D15-S07); `_WORK/W1_M02.md`]

<a id="F246"></a>
### F246 — W1_D15: D15-F10 [primary_docs] Calibration also needs grouped separation.

Provenance: [W1_D15:53](_WORK/W1_D15.md); original aliases: D15-F10. Sources: [S364](SOURCES.md#S364), [S365](SOURCES.md#S365).

**[D15-F10](RAW_FACTS.md#F246) [primary_docs] Calibration also needs grouped separation.** LeaveOneGroupOut excludes a declared group; probability calibration needs fit/calibration separation. Reliability diagrams compare score/outcome frequencies; Brier/log loss combine calibration and discrimination. Grouped protocol below extends these principles. [[D15-S09](SOURCES.md#D15-S09)]

<a id="F247"></a>
### F247 — W1_D15: Minimum annotation contract [hypothesis]

Provenance: [W1_D15:55](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Minimum annotation contract [hypothesis]

A clip label says an action/category characterizes a selected clip, not every moment. A span asserts activity under a declared boundary definition; sampled timestamp labels do not fill intervening frames. Frame labels need an explicit annotated-frame set. Bboxes localize objects; pose localizes joints with visibility; tracks link observations. Person-event and ordered person-machine relations are additional labels. None alone establishes a policy violation. Multi-label events must permit phone-use+walk rather than force mutually exclusive classes.

Store six UTF-8 JSONL tables, tool-native exports, codebook/dictionary, frame-PTS manifest and immutable split manifest. Use integer original PTS with rational time base, half-open `[start,end)` intervals and explicit EOF/last-frame duration convention. Milliseconds may be a display convenience. Unknown is null, not zero/negative.

| Table/key | Required fields and semantics |
|---|---|
| media/source_id | original URL/private reference, sha256, dataset revision, parent_recording_id, session_id, sync_group_id, site_id, camera_id, known subject groups, media/annotation rights separately, allowed use, time_base numerator/denominator, pts_origin, duration_pts, frame_pts_manifest_sha, transform_chain, split_group_id, split_role |
| entities/entity_id | source_id, entity_type, local actor/object identity and certainty/lineage, native bbox/keypoint references. Track ID+stream epoch differs from actor and event ID. Cross-video subject identity only if independently known. |
| coverage/coverage_id | source_id, interval, reviewed classes and actor/region scope, completeness=exhaustive/positive_only/sparse/unknown, visibility=visible/partial/hidden/outside, reason, usable_for_negative_rate, annotator/reviewer. Coverage exists even if no events. |
| events/event_id | source_id, literal scenario, observed action/state, subject_ids or ordered pair_ids, policy_version, onset interval [earliest,latest], offset interval, evidence intervals, visibility references, left/right censor flags/reasons, certainty=confirmed/possible/unresolvable, preceding-event link, provenance and adjudication reference |
| context/context_id | effective-time ROI/geometry version, authorized operation/area, machine moving/stopped/unknown and independent evidence, physical calibration/units/uncertainty, procedure version. Unknown context is not prohibited truth. |
| annotations/revision_id | immutable opinion ID, annotator/reviewer, creation time, tool/version, codebook version, native export/hash, superseded revision, disagreement and adjudication reason; retain original opinions |

Illustrative schema record, not observed evidence:

```json
{"schema_version":"mosprom-event-0.1","event_id":"s01:e004","source_id":"s01","scenario_literal":"fall_lying_immobility","observed_action_or_state":"fall_transition","subject_ids":["s01:p2"],"pair_ids":null,"onset_interval_ms":[5100,5260],"offset_interval_ms":[5860,6020],"evidence_intervals_ms":[[5260,5860]],"left_censored":false,"right_censored":false,"certainty":"confirmed","policy_version":"fall-visible-v1","annotation_revision":"r17"}
```

A linked post-fall-low-motion event requires observed low-motion evidence and a declared hold rule. Already lying at stream start is not an observed fall. Hidden periods may preserve unresolved incident identity without asserting observed continued action. Unknown gaps must not accumulate low-motion dwell or demonstrate safe-clear; continuation/reset rules belong to policy_version.

| Scenario | Extra GT and indispensable controls |
|---|---|
| Running | gait/action and person track; brisk walking, camera motion and scale/perspective changes. OmniFall walk0 is not a clean running negative. |
| Moving machine proximity | ordered person-machine pair, independently known machine motion, aligned geometry/zone rule; stationary machinery/projected-overlap-but-separated controls. Bbox overlap is not meters. |
| Phone while walking/working | visible use-like evidence owned by same person plus time overlap with walk/independent work state; carry-only, put-away-before-walk, radio/scanner and other-owner controls. |
| Smoking/open fire | smoking action versus flame-region episodes separately, effective authorized-area context; steam/dust/glare/welding/authorized-flame and hand-to-mouth controls. |
| Barrier/under conveyor/load | crossing direction, attempted/completed action, actor-object/zone relation; projection alone cannot prove physically under load. |
| Height/harness | known height context and harness/attachment components separately; hidden hook is unknown attachment, not absent attachment. |
| Fall/lying/low motion | transition, voluntary lie-down, already-lying, recovery motion, occlusion and bounded observed hold; no consciousness diagnosis. |
| Improper carrying | named procedure violation and actor-load relation; unknown mass/effort cannot be inferred from appearance; compliant carry and empty-hand controls. |

<a id="F248"></a>
### F248 — W1_D15: Reproducible QA and agreement [hypothesis]

Provenance: [W1_D15:89](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Reproducible QA and agreement [hypothesis]

1. Freeze codebook before scores: action/state, ownership, onset/offset definitions and positive/negative/ambiguous examples, interruption/clear/rearm and policy requirements. Separate physical onset, first visible evidence and first time a hold can be satisfied. New definitions create a new version and impacted-label review.
2. Two annotators independently label complete recordings or predeclared contiguous blocks, including negatives; hide model scores and each other's boundaries. If model proposals assist, record that and inspect proposal-free blocks for misses. Review ambiguities and stratified random negative blocks, not just easy samples.
3. Before adjudication, match same-class/same-actor candidates by the declared graph rule. Report mutual event precision/recall, unmatched counts, onset/offset absolute-difference distributions, ownership disagreements and visible/unknown coverage agreement. Bbox IoU/joint visibility are separate. Fixed-grid kappa/alpha can supplement on jointly exhaustively labeled time; rare positives make raw agreement misleading. Agreement after merging is not independent agreement.
4. Reviewer resolves disagreement using native frames/codebook. Preserve competing opinions and reason; retain uncertain boundary intervals when unresolved. Majority cannot reveal invisible attachment or metric distance. Publish unknown counts and adjudication rate.
5. Validator checks IDs/references, classes, ordered-pair types, monotonic original PTS, bounds within media, incompatible-state overlap, coverage contradictions, provenance groups crossing splits and multiview boundary gaps. Compare annotated EOF with decoded EOF; never pad video to satisfy hold.
6. Round-trip a small native-export/import/converter fixture and compare IDs, attributes, geometry, masks and original PTS. Export CVAT replicas independently. Choose QA sample size for rarity/disagreement; vendor example percentages are not acceptance criteria.

<a id="F249"></a>
### F249 — W1_D15: Event matching, uncertainty and censoring [hypothesis]

Provenance: [W1_D15:98](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Event matching, uncertainty and censoring [hypothesis]

Freeze YAML before lockbox access: scenario/policy, eligible visibility/completeness, hold/gap/clear, actor-pair matching, overlap criterion, onset early tolerance/late deadline, offset tolerance, duplicate/rearm, denominator and censor rules. Team must select tolerances from use cases; no universal seconds or acceptance percentage invented here.

**Score localized episodes and operational notifications separately.** Segment output has estimated start/end, entity/pair and score. Alert ledger has alert_id, incident_id, scenario, actor/pair, evidence PTS, estimated onset, confirmation source PTS, input-arrival/confirmation/queue/render/notification monotonic wall clocks, clear/rearm and evidence references. Backdated onset does not backdate notification.

For first-alert matching, build bipartite eligible edges for same class/policy, compatible GT actor or ordered pair, covered camera/time and declared timing/evidence criterion. Unknown actor is not a wildcard for actor-attributed TP; use separate scene-level scoring if necessary. Fire-region split/merge needs declared lineage policy.

Use maximum-cardinality one-to-one matching with deterministic secondary priority, e.g. earliest eligible alert, minimum onset difference, stable IDs. Save edge list and assignments. This operational matcher deliberately differs from confidence-ranked AP. An alert covers at most one event; each event earns one first-alert TP. A long alarm spanning episodes matches one and misses others. Wrong actor at right time is unmatched and true event missed. Extra compatible alerts are duplicates and count among unmatched operational alerts. Evaluator-only cooldown must not hide them; actual deduplication belongs to tested system output.

For segments, declare tIoU or onset+offset collars; optionally show threshold sensitivity with fixed headline. Brief transitions and long persistent states need class-appropriate interpretation. A broad segment can overlap well while notifying late; timely recall remains necessary. Zero-duration notification points cannot be scored by ordinary segment tIoU.

GT onset `[a,b]` gives alert source-time latency interval `[t-b,t-a]`. With deadline D, definitely timely if `t<=a+D`, definitely late if `t>b+D`, otherwise ambiguous, subject also to early-alarm eligibility. Report definite/possible timely recall range. Do not choose favourable boundary separately for each model. For uncertain tIoU, report endpoint-sensitivity analysis or predeclared adjudication, not arbitrary padding as truth.

| Metric | Definition and required caveat |
|---|---|
| all-known event recall | matched/all known GT events, including independently established hidden/partial events. Unknown existence behind full occlusion cannot become an invented all-world denominator. |
| observable recall | matched eligible/eligible GT, with eligible/all-known coverage and exclusions declared before model scores. Detector/tracker failure cannot make visible GT ineligible. |
| timely recall(D) | definitely timely matches/all selected denominator; show uncertainty range and both all-known/observable versions. Conditional latency median cannot replace recall. |
| event precision | matched/all scorable operational alerts, with wrong actor/class, duplicates and indeterminate counts. Unknown-coverage alerts remain indeterminate, not silently TP/FP. |
| unmatched/service-hour | unmatched alerts/reviewed service-valid camera-hours, with per-camera/shift counts. |
| negative false-alert rate | alerts inside exhaustively reviewed target-negative intervals/negative camera-hours, a distinct denominator. Show unique FP incidents and duplicate notifications. |
| duplicates | extra compatible notifications per GT, distribution/count. |
| boundary/latency | onset/duration/clear errors on eligible complete cases with counts/censor flags; source confirmation delay separate from wall notification delay. |

Zero-alert systems have undefined precision and zero recall where positives exist. Event-free footage has undefined event recall but valid FP exposure. Faster-than-real-time file replay measures throughput, not live camera-to-user delay; use paced/live run and clock alignment.

Left-censored already-active states test state detection/stream-join alert, not transition recall or physical-onset latency. Right-censored states can contribute observed presence/first-alert outcome, but not completed duration/clear/rearm correctness. An event lacking enough observed post-onset horizon for D is administratively censored for timely outcome; report count. Visibility loss/decoder failure is interruption with reason, not clean observed clearance. Pair conditional latency with recall/no-alert mass, rather than discarding misses.

<a id="F250"></a>
### F250 — W1_D15: Continuous negative exposure and split integrity [hypothesis]

Provenance: [W1_D15:127](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Continuous negative exposure and split integrity [hypothesis]

Trimmed staged positives plus equal-count short ADL cannot estimate operational precision or alarms/day. Use permissioned continuous recordings of ordinary work/hard negatives with reviewed class scope and real durations. Exclude titles/outros, decoder failures, loops, frozen and synthetic footage from claimed real-camera negative hours; show each duration separately. Genuine physical stillness is not automatically frozen video: verify stream continuity/scene evidence. Synthetic/dropout stress tests stay separate. Replaying one recording or making FPS variants does not create independent exposure hours.

Group provenance before frames/windows. Indivisible units are connected components of parent recording, overlapping crops, synchronized views and known duplicates/transforms. Keep synchronous views of the same take together. Hold actors/sites/cameras/sessions out according to claimed generalization. A camera-only split sharing simultaneous takes is contaminated. Save group edges/reasons; if grouping leaves too few independent groups, report unsupported estimate rather than random windows.

Audit SHA duplicates first, then perceptual/embedding candidates for transcodes, crops, borders, watermarks/speed changes. Verify aligned candidate runs and parent URLs/times; save scores, inspected frame pairs and decisions. Static backgrounds can create false candidates; sparse sampling can miss brief overlap. A clean audit is bounded by searched corpus/sampling. Undisclosed pretraining overlap remains unknown; record model training datasets/revisions separately.

Use complementary claims: grouped new-take/session same-camera test; leave-one-camera-out validation with sync grouping first; untouched target-site/camera lockbox. LOCO describes unseen camera geometry, not necessarily unseen actors/sites; one camera cannot support it. If held-camera calibration is allowed, distinguish unlabeled geometry from event-label tuning and report adapted/unadapted protocols.

Train-only fitting applies to scalers, imputation, normalization, embeddings and feature selection. Use separate grouped calibration/threshold dev data and lockbox. Calibrate explicit unit (frame/candidate/incident); post-suppression candidate scores are not automatically operational incident probabilities. Balanced negative sampling changes prevalence: preserve exposure/weights rather than advertise balanced-set calibration as deployment probability. Audit lighting, distance/size, occlusion, PPE/clothing, camera and available consented actor strata, with counts/uncertainty; avoid unsupported protected-trait inference. Compare models on identical groups/masks and fixed alarm budget, show pooled and camera-macro results. Cluster-bootstrap by session/camera/actor rather than iid frames; few groups limit precision.

<a id="F251"></a>
### F251 — W1_D15: Proposed experiments and logical gates

Provenance: [W1_D15:139](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Proposed experiments and logical gates

| ID | Inputs, actions, saved evidence | Decision gate; PASS does not prove |
|---|---|---|
| E001 | Native labels, media hashes/PTS, codebook, separate code/weight/media/annotation grants; export roundtrip fixture/manifest. | STOP on missing relevant action/context or unavailable media/right; PASS yields dev pack, not industrial or device validity. |
| E002 | Provenance graph, duplicate review, continuous exhaustive negatives; component edges/split hashes/exposure log. | STOP on cross-split group or unknown negative completeness; PASS cannot rule out undisclosed pretraining overlap. |
| E003 | Later exact CPU/RTX causal baseline, frozen artifacts/pre/post/environment and original PTS; predictions/config. | Must preserve actor/time/evidence contract; PASS reference only, no device throughput inference. |
| E004 | Frozen matching YAML, uncertain/censored cases, alert ledger; future-suffix perturbation must not change earlier alerts; save edges/counts/clock log. | STOP on future frames, GT boundaries or model-driven eligibility; PASS limited to split, wall latency requires paced/live run. |
| E005 | Same detections/GT across bbox, tracking, pose rules, temporal ablations; save ID-transfer/duplicate/clear errors. | Complexity needs relevant measured gain without lost recall/coverage; MOT gain alone insufficient. |
| E006 | Native/1/2/5FPS comparison conditions, deterministic PTS thinning, abrupt gaps; source timestamps retained. | Check brief events, holds, identity/rearm and unknown rates; no sufficient-FPS claim before evidence. |
| E007 | Authorized/forbidden context, moving/stopped machines, projection/uncertain-zone controls. | STOP physical distance/under-load/attachment claims without observability; PASS may support only image-space policy. |
| E008 | Later exact SDK/device/export/compile/reference parity and paced timing. | STOP unsupported actual path; PASS needs actual LinQ NN execution plus quality/timing, not checker success. |

<a id="F252"></a>
### F252 — W1_D15: Handoffs and open decisions

Provenance: [W1_D15:152](_WORK/W1_D15.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Handoffs and open decisions

M03: donor action boundaries need original-PTS, visibility and low-motion additions; Subject1/3 inspected clips remain development; fallen is not stationary. M02: expose matched_detection_id, last_measured_pts, emitted/predicted/internal-state flags and stream epoch; event identity follows explicit gap policy. Scenario workers: add actor/pair and policy eligibility, not only object/action labels. Synthesis: retain all-known/eligible recall with coverage, both negative-hour/service-hour denominators, uncertain/censored counts and source/wall clocks.

Unresolved team/organizer decisions: exact hold/clear/rearm semantics and incident definitions; class-specific notification deadlines/early tolerances; held-camera calibration permissions; continuous target media and exhaustive class scope; camera/source clocks and actual notification measurement path. No target accuracy, fairness guarantee, commercial media clearance or LinQ compatibility inferred.

<a id="F253"></a>
### F253 — W1_D16: W1 D16 — synthetic video, transfer evidence and independent real validation

Provenance: [W1_D16:1](_WORK/W1_D16.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W1 D16 — synthetic video, transfer evidence and independent real validation

Access window: 2026-10-23, approximately 19:47–19:56 UTC. Research only: no generation, training, inference, paid service, large video/archive download or device measurement. `local_test` below is reserved for executed HTTP/metadata/text checks, never model performance. Exact request timestamps, byte counts and SHA256 of acquired small documents are in `D16_evidence/access.json`; payload HEAD results are in `D16_evidence/payload_head.json`. Papers were downloaded and text-extracted locally; reported experiments remain **author_claim**, not reproduced experiments.

<a id="F254"></a>
### F254 — W1_D16: Branch question and decision

Provenance: [W1_D16:5](_WORK/W1_D16.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Branch question and decision

**Can synthetic videos legitimately expand industrial safety training/demo material, and do they establish real CCTV quality?**

**Decision [inference]: use as an explicitly marked augmentation/stress-test branch, contingent on a real-only grouped holdout. Do not substitute any generated, simulated or composited clips for independent real-world evaluation.** Primary studies support conditional gains, and also substantial negative transfer or weak synthetic-only results. Neither photorealism nor plausible prompted action supplies verified event truth, metric geometry, a valid harness connection, identity continuity or fall biomechanics. No inspected source establishes performance for all eight Mosprom events, LinQ export/runtime or target-camera industrial deployment.

The strongest new contribution here is the empirical comparison and exact limits below, rather than another NVIDIA catalog overview. Prior PhysicalAI-Event-Videos and active D13 SmartSpaces work are not duplicated. M07's SynthSite work is used only as a concrete semantics stress case and is explicitly distinguished from new transfer evidence.

<a id="F255"></a>
### F255 — W1_D16: D16-F01 — paired gains and negative results, with correct denominators

Provenance: [W1_D16:35](_WORK/W1_D16.md); original aliases: D16-F01. Sources: [S366](SOURCES.md#S366), [S367](SOURCES.md#S367), [S368](SOURCES.md#S368).

## [D16-F01](RAW_FACTS.md#F255) — paired gains and negative results, with correct denominators

**[author_claim/primary_docs, S01]** SURREACT reconstructs motion from real training video and rerenders humans with varied appearance/viewpoint. NTU CVS RGB unseen-view accuracy rises **53.6→69.0%** when adding VIBE-based synthetic data. More revealingly, one-shot Kinetics-15 Table9 uses 15 real training clips and 725 real test videos: RGB synthetic-only **9.4%**, real-only **26.2%**, synthetic+real with Mini-Kinetics backgrounds **32.7%**. With LSUN backgrounds, synthetic+real is **26.3%**, essentially the real baseline. Table5 also finds per-frame motion noise can hurt compared with unperturbed motion. This is conditional benefit, not evidence that unlimited randomization helps.

**[inference]** Motion derived from a source clip is not an independent new event. Keep the entire motion family and source real clip in one split. The background contrast is especially relevant to factory compositing: changing the renderer without matching clutter/occlusion can erase the gain. Those results do not measure fall mechanics, metric proximity, attached harnesses, continuous false alarms or industrial night CCTV.

<a id="F256"></a>
### F256 — W1_D16: D16-F02 — synthetic transfer is backbone/task dependent

Provenance: [W1_D16:41](_WORK/W1_D16.md); original aliases: D16-F02. Sources: [S372](SOURCES.md#S372), [S373](SOURCES.md#S373), [S374](SOURCES.md#S374), [S375](SOURCES.md#S375).

## [D16-F02](RAW_FACTS.md#F256) — synthetic transfer is backbone/task dependent

**[author_claim/primary_docs, S03]** SynAPT compares pretraining on 150 synthetic classes×1000 examples to a matched-size Kinetics subset, then transfers to disjoint downstream class sets. Its overall finding favors synthetic pretraining on lower static-context-bias tasks and Kinetics on UCF/HMDB. Table3 is a useful qualification: TimeSformer fine-tuning on Diving48 yields **44.86 synthetic vs46.37 Kinetics**, whereas Mini-SSV2 yields **51.10 vs48.92**, HMDB51 **54.38 vs59.51**. This transformer baseline already uses ImageNet-21K initialization. Thus even the paper's broad favorable low-bias pattern is not universal across all model/dataset cells.

**[inference]** Do not label this “synthetic-only recognizer matches real industrial safety.” It tests learned representation transfer followed by downstream learning, not zero-shot eight-scenario deployment. Safety decisions often intentionally depend on context: the same gait near a marked crossing and inside a machine envelope can have different labels. Removing context bias indiscriminately can remove required equipment/policy information.

**[primary_docs, S04]** SynAPT combines ElderSim, PHAV and SURREACT. Source retrieval still has distinct permissions: README says SynADL requires signed EULA/email, while SURREACT has its own access terms. Construction manifests are useful grouping clues; no source licenses are unified by the repository's existence. No matched ready safety-event checkpoint was verified here.

<a id="F257"></a>
### F257 — W1_D16: D16-F03 — more photographic rendering is not automatically more useful

Provenance: [W1_D16:49](_WORK/W1_D16.md); original aliases: D16-F03. Sources: [S376](SOURCES.md#S376), [S377](SOURCES.md#S377), [S386](SOURCES.md#S386), [S387](SOURCES.md#S387).

## [D16-F03](RAW_FACTS.md#F257) — more photographic rendering is not automatically more useful

**[author_claim/primary_docs, S05]** REMAG compares real and four synthetic variants from CG/neural rendering crossed with mocap/video-reconstructed motion. Its 11 activities, synchronized aerial/ground views and real test subjects allow a more controlled comparison than a generated demo. Synthetic training trails real by the paper's summarized **4–8%**; conventional CG outperforms Liquid-Warping-GAN rendering, and mocap beats reconstructed motion. Synthetic pretraining plus fine-tuning with 5 or10 real subjects improves over the corresponding small real subsets. Methods use Kinetics-400 pretrained SlowFast/MViT/X3D, 300 epochs and 64-frame clips with ≥80% same-label frames; this is not training from no real pretraining. Testing uses real subject groups.

**[inference]** This supports testing motion/appearance independently. It does not prove a physical simulator is correct, does not evaluate modern free-form text-to-video generation, and does not supply the target industrial event taxonomy. Dataset twins improve experimental control but require careful common-source grouping.

**[primary_docs/artifact_access_checked, S06]** Public REMAG data are CC BY4.0 per the authors. Exact paired archive checks on 2026-10-23: `http://cluster1.graphics.cs.cmu.edu:8080/REMAG/11_Activities/01_Real/Real_Aerial%2B11Act_224px.zip` HEAD200 **6,999,136,733 bytes**; `http://cluster1.graphics.cs.cmu.edu:8080/REMAG/11_Activities/02_SynCG-MC/SynCG-MC_Aerial_11Act_224px.zip` HEAD200 **164,204,609,691 bytes**. No payload downloaded. Published real aerial MD5 is `cadb0d24d595cdca65ba4d16c6c14109`; not verified against an acquired archive. No independently inspected training-checkpoint license or target ready weights.

<a id="F258"></a>
### F258 — W1_D16: D16-F04 — generator fidelity does not equal event truth

Provenance: [W1_D16:57](_WORK/W1_D16.md); original aliases: D16-F04. Sources: [S378](SOURCES.md#S378), [S379](SOURCES.md#S379), [S380](SOURCES.md#S380), [S381](SOURCES.md#S381), [S382](SOURCES.md#S382), [S383](SOURCES.md#S383).

## [D16-F04](RAW_FACTS.md#F258) — generator fidelity does not equal event truth

**[author_claim/primary_docs, S07]** VideoPhy v2 evaluates prompt adherence and physical commonsense separately through human judgments of material interactions. Its historical best CogVideoX-5B joint score is **39.6%**, despite **63.3%** semantic adherence; physical score **53%**. This is a benchmark-specific 2024 result, not a current ranking or a measured failure rate for modern industrial-video generators. Reported failure types include object/material physics violations. The repository provides human and automatic tables separately; an automatic evaluator's score is not human ground truth. These generated-video quality tests contain no industrial real-camera transfer experiment.

**[primary_docs, S08]** VBench separates subject consistency, background consistency, flicker, motion smoothness, dynamics and spatial relation. It identifies a tradeoff: nearly static videos can score well on temporal consistency, so dynamics must be checked alongside it. Its identity proxy uses inter-frame visual features; quality metrics should not be mistaken for per-person verified identity or measured geometry.

**[inference]** For this task, manually audit full clips and annotate observed evidence rather than trusting the prompt:

| Failure or ambiguity | Why a safety label can become wrong | Required audit/control |
|---|---|---|
| Person appearance changes, merges, disappears behind a column | One continuous worker event becomes different identities | Track continuity, occlusion state and explicit unknown intervals; crossing-person control |
| Foot sliding, skipped impact, reverse/repeated time, impossible recovery | A “fall” prompt may show neither a fall nor a meaningful immobility interval | Real-time onset/impact/recovery labels; inspect frame timestamps/full motion; no unconsciousness inference |
| Hook/rope disconnects, lanyard blends into scaffolding | A wearing-harness image becomes false “connected” truth | Separate worn/present/visible connection/unknown; loose-hook and occluded-anchor controls |
| Depth/order changes while image boxes overlap | “Under load” or “near machine” is physically ambiguous | Surveyed/calibrated geometry or explicit image-space event name; stationary-near, moving-far and driver controls |
| Phone/cigarette/small flame vanishes between frames | Tiny-object behavior is mislabeled across a clip | Per-interval object visibility; hand-to-ear without phone, tool/radio, steam/reflection controls |
| Generated negatives are unusually clean and empty | Model wins on scene appearance instead of absence of violation | Match actors, camera, clutter, generator and prompts across positive/negative siblings |

These failure examples are proposed checks, **not locally observed defects in downloaded SynthSite videos**. This branch did not download/decode generated media.

<a id="F259"></a>
### F259 — W1_D16: D16-F05 — rights are separate from usefulness and labeling

Provenance: [W1_D16:76](_WORK/W1_D16.md); original aliases: D16-F05. Sources: [S369](SOURCES.md#S369), [S370](SOURCES.md#S370), [S371](SOURCES.md#S371), [S384](SOURCES.md#S384), [S388](SOURCES.md#S388).

## [D16-F05](RAW_FACTS.md#F259) — rights are separate from usefulness and labeling

**[primary_docs, S02/S09]** SURREACT declares MP4/metadata/segmentation outputs, including 2D/3D joints, camera parameters and source-sequence IDs; it warns sequences may have fewer frames because motion estimation drops frames. A prompt label is different from such renderer-state annotation, and renderer-state annotations are still not measured real-world truth. Exact `surreact_ntu_vibe.tar.gz` URL in S02 returned HEAD401, consistent with documented credentials. Do not bypass it. The listed flow checkpoint https://lsh.paris.inria.fr/surreact/flow_surreact_2_v10_fixbg_pretrainsurreal_checkpoint.pth.tar returned HEAD200 **54,166,744 bytes**; it is optical-flow estimation, not a pretrained safety-action classifier.

**[primary_docs, S09]** SURREAL terms grant noncommercial scientific use and restrict commercial use, production of commercial artifacts and third-party availability without permission. SURREACT routes data/generation-code users to those terms; it cannot be assumed suitable for an industrial customer demo. A missing root `LICENSE` URL returned404; the substantive linked terms were nevertheless accessible. Training-code, base-model, human-body assets, input motion and output-media rights require separate checks.

**[inference]** A clip can be eligible for a synthetic demo only if its actual license/service terms and input rights permit that use. Merely writing “synthetic” does not clear rights. Conversely a permissive media license does not establish correct events or real-domain model quality. For any vendor such as Higgsfield, retain the actual plan/date/version/output-use terms and source-image consents before using outputs; no vendor-specific commercial clearance or ground-truth capability is asserted here, and no service was called. Watermarks, actor likenesses, factory photographs, uniforms/logos, motion assets and weights remain separate provenance fields.

<a id="F260"></a>
### F260 — W1_D16: D16-F06 — SynthSite is an instructive semantics stress case, not a real holdout

Provenance: [W1_D16:84](_WORK/W1_D16.md); original aliases: D16-F06. Sources: [S385](SOURCES.md#S385).

## [D16-F06](RAW_FACTS.md#F260) — SynthSite is an instructive semantics stress case, not a real holdout

**[primary_docs, inspected primary files S10; M07 acquisition credited]** Its 227 generated clips have reviewer votes and clip-wide hazard/safe class names, not event intervals or calibrated 3D relations. Two/three reviewers produce a unanimous/disagreement tier. M07 independently recounted detector CSVs rather than executing those models. This branch confirmed from the primary design note that operational-machine state and suspended-load reasoning are intended semantics, yet implemented spatial rules operate in image coordinates. No generated prompt can repair missing physical calibration.

**[inference]** Keep unanimous Tier1 for reproducible synthetic-rule probes; preserve individual Tier2 disagreement rather than forcing false certainty. Never reinterpret these labels as proof of true vertical footprint, metric clearance, online onset or same-worker continuous violation. Positive and safe clips should differ by the safety relation while retaining similar rendering cues. A detector's high score on these files is evidence about these synthetic files only. No SynthSite result is promoted here into a real benchmark or commercial clearance; M07 records its custom license and exact payloads.

<a id="F261"></a>
### F261 — W1_D16: D16-F07 — realistic grouped experiment for future RTX3090 work

Provenance: [W1_D16:90](_WORK/W1_D16.md); original aliases: D16-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D16-F07](RAW_FACTS.md#F261) — realistic grouped experiment for future RTX3090 work

Everything in this section is **inference/hypothesis**, not executed training or an agreed numerical SLA.

1. **Freeze a real test collection first.** Obtain permissioned original fixed-camera streams with natural background activity, event intervals, actor/pair IDs when visible, camera/time/site IDs and unknown/occlusion labels. Avoid recording dangerous near misses. Safe staged actions can test narrow observable behavior but are a separate stratum from natural incidents. Keep synthetic, composited and staged media clearly tagged.
2. **Group before any sampling.** A source recording/session, all views of its action, source actor motion, cloned background, adjacent segments, overlapping windows, prompt family, seed variants and generated descendants belong to one group. Assign groups to train/calibration/test before augmentation. A per-frame or random short-clip split is inadequate. Split at least by camera/session; add held-out site and held-out actors where feasible. State what cannot be made disjoint.
3. **Do not use test-camera images to design synthetic training.** Compositing actors into a test factory photograph, prompt editing after test errors or selecting best generated clips using test performance is adaptation/leakage. If deployment permits target-camera adaptation, name it and reserve a later untouched session/camera holdout. Distinguish unknown internet pretraining overlap from checked exact/near-duplicate video overlap.
4. **Compare controlled arms.** Real-only baseline; real+ordinary augmentation; same real+CG/mocap; same real+generative clips; optional synthetic-only diagnostic; synthetic pretraining→real fine-tuning. Hold model initialization, real-data subset, optimization budget, thresholds, sampling rate and validation information constant. Match total updates or report that extra compute is a confound. Include multiple fixed seeds and paired results on identical real events.
5. **Vary the synthetic dose.** Use a small preregistered ratio grid and a fixed total training budget. Report per-event/per-camera changes, including regressions. Do not select the best ratio on test. Compare generator/style-balanced negatives; optionally train a real-vs-synthetic discriminator on a separate audit partition to expose a source shortcut, without treating its score as transfer performance.
6. **Evaluate causal video alerts.** Preserve timestamp spacing, decode failures, tracking state and sampling policy. For each event, define observable onset, required persistence, event matching and deduplication before scoring. Report event recall, missed short events, false alerts per camera-hour, positive predictive value at natural prevalence, latency distribution conditional on detected events plus missed-event count, and repeat alerts per event. Include per-scenario/camera/day strata and uncertainty intervals clustered by session/camera rather than treating overlapping clips as independent.
7. **Measure hardware separately.** Future LinQ tests must cover exported operators, CPU preprocessing/tracking, real stream throughput, end-to-end latency, sample drops and memory. Neither GPU-paper accuracy nor a generated UI animation validates LinQ execution. A coarse 1fps policy can lose an event regardless of generator quality; run matched temporal-recall probes before choosing it.

**Acceptance decision [hypothesis]:** keep synthetic augmentation only if its prespecified real-test operating point improves the selected safety objective without unacceptable scenario regressions, and show the baseline and uncertainty. There is no justified universal synthetic fraction or generic “accuracy gain” to promise now.

<a id="F262"></a>
### F262 — W1_D16: D16-F08 — permitted demo wording and exclusions

Provenance: [W1_D16:104](_WORK/W1_D16.md); original aliases: D16-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [D16-F08](RAW_FACTS.md#F262) — permitted demo wording and exclusions

**[inference]** Every generated/simulated/composited demo clip should carry a persistent visible origin label, with provenance in its manifest. Suggested wording: “Synthetic scenario illustration; inference [actually executed / prerecorded output]. Not a measurement of real-site performance.” Put measured runtime only on actual device runs. Keep generated demo metrics, synthetic benchmarks and permissioned real validation in separate tables and exports. A mixed montage should retain labels per clip rather than a brief opening disclaimer.

Never call a synthetic clip independent real-world validation; never present prompt intentions as observed annotation; never count rendered views/clones as independent incidents; never let an output video implying a fall/collision substitute for physical observation. Composite footage remains synthetic even if the background is a real factory. A synthetic-only demo is useful for showing configured alert flow and reviewing event definitions, provided execution and provenance are described honestly.

<a id="F263"></a>
### F263 — W1_D16: Local evidence, unresolved gates and stopped leads

Provenance: [W1_D16:110](_WORK/W1_D16.md); original aliases: section record. Sources: [S389](SOURCES.md#S389).

## Local evidence, unresolved gates and stopped leads

- `D16_fetch.py` is the bounded acquisition script; `D16_evidence/access.json` records GETs/hashes, `payload_head.json` records four HEADs. No archive body, flow weight or video was downloaded. Saved PDFs are scholarly documents, not training datasets.
- A newer MDPI study, *Evaluating the Effectiveness of AI-Generated Data for Video-Based Action Recognition*, Electronics15(16):3712, 2026-08-19, https://doi.org/10.3390/electronics15163712 , appeared in primary search. Direct browser429/Python403 prevented full local verification; its headline result is deliberately excluded from the decision. This is an access limit, not a refutation or absence claim.
- Exact pretrained safety checkpoints, real industrial annotation intervals, commercial clearance and target-device artifacts remain unestablished for the transfer papers. Ready generic flow weights do not close that gap. REMAG makes paired empirical research plausible but its archives are far beyond this task's small-download scope.
- Open questions: actual permitted target footage, event definitions/calibration, class-wise real failure rates, generator provenance/terms, natural-vs-staged mix, pretraining overlap and LinQ SDK/device. None is resolved by synthetic visual quality alone.

<a id="F264"></a>
### F264 — W2_01: W2_01 — K001 exact RTMPose-m body7 static bundle and detector boundary

Provenance: [W2_01:1](_WORK/W2_01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_01 — K001 exact RTMPose-m body7 static bundle and detector boundary

Research performed **2026-10-23 20:12–20:19 UTC / 23:12–23:19 Europe/Moscow**. Exclusive evidence: [W2_01_EVIDENCE](_WORK/W2_01_EVIDENCE/). Assignment preserved verbatim as [PROMPT_FULL.md](_WORK/W2_01_EVIDENCE/PROMPT_FULL.md). No substantive task expansion; adaptive bounded check inspected the official CPU demo archive because its detector supply was the remaining chain question. No subagents, paid services, model execution, training, export, compilation, target-video benchmark or LinQ execution. Python `onnx` was installed to parse protobuf and run static schema checks. PTH bytes were hashed without deserialization.

<a id="F265"></a>
### F265 — W2_01: Decision and K outcome

Provenance: [W2_01:5](_WORK/W2_01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Decision and K outcome

**K001 = scope_narrowed.** The exact body7 pose archive is acquired and internally specified; its two outputs, actual preprocessing/decode metadata, graph operators and external-file status are now verified. This closes the HEAD-only pose-payload uncertainty. It does **not** close a complete detector→pose→LinQ reference build. The official easy CPU ZIP contains a materially different detector checkpoint and old AIC+COCO pose export; the later README export recipe names yet another detector checkpoint. Neither can be silently substituted for the measured body7 pose export. The exact published recipe detector PTH is now independently acquired, but its matching ONNX export is not established here. An independent detector is a conditional replacement requiring its own pre/postprocessing, original-frame bbox convention and parity/quality check.

**New counterevidence:** MMDeploy 1.2.0's actual `TopDownAffine` SDK component performs rounded/clipped ROI `CropResizePad` and corrects center/scale. The standalone Python demo uses `cv2.warpAffine`, normalizes `cv2.imread` data without a color swap, and must not be called an exact implementation of this SDK pipeline. A Python/MMPose affine port may be a legitimate separate reference, but needs explicit crop/output parity checks. This applies to the neighboring tiny archive too because its saved pipeline is byte-identical. This is a source observation, not a measured numerical discrepancy.

**Practical recommendation [inference]:** register the exact candidate as `RTMPose-m-body7-e48f03d0 / SDK1.2.0-RGB-CropResizePad-minSimCC / batch1`, rather than simply “RTMPose-m”. Preserve tiny as the cheaper exact-shape comparator; promote m only if target joint quality/event evidence improves sufficiently and actual LinQ compilation/execution succeeds. No m-versus-t industrial accuracy or speed comparison was run.

<a id="F266"></a>
### F266 — W2_01: Existing evidence read and bounded new methods

Provenance: [W2_01:13](_WORK/W2_01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Existing evidence read and bounded new methods

Read frozen K001 in [CRITIC.md](CRITIC.md), `_WORK/W1_M01.md`, saved M01 README/config/SimCC/demo/license/access evidence, `_WORK/CASE_NOTES.md`, `_WORK/SYNTHESIS_CONTRACT.md`, the original briefs' relevant context, and the neighboring feasibility RTMPose-t section. W1 established exact URLs and server metadata but did not acquire A02 or its graph. The neighboring report was a pointer, not independent primary verification of m. New checks are scripted and saved:

| Action | Exact observation / evidence | Evidence label |
|---|---|---|
| Bounded full GET of named body7 ZIP, max60MB; hash, ZIP CRC reads and file manifest | HTTP200, 50,799,818 B; six non-directory members; [ACCESS.json](_WORK/W2_01_EVIDENCE/ACCESS.json), [MANIFEST.json](_WORK/W2_01_EVIDENCE/MANIFEST.json), `check.py` | artifact_access_checked + local_test (ZIP/hash parsing only) |
| Parse actual ONNX with external loading disabled, run `onnx.checker.check_model` | Static check passes; [GRAPH.json](_WORK/W2_01_EVIDENCE/GRAPH.json), `parse.py`, [POSE_HEAD_DIMS.json](_WORK/W2_01_EVIDENCE/POSE_HEAD_DIMS.json) | local_test (static only) |
| GET pinned README, model and detector configs, standalone demo, code licenses, MMDeploy tag1.2 sources | Status/bytes/SHA recorded; NOTICE paths404; `source_checks.py`, `final_checks.py` | primary_docs + artifact_access_checked |
| HEAD exact body7 PTH and README detector PTH, then full GET of small detector PTH | Body7 PTH200/54,551,099 B HEAD only; recipe detector200/4,224,050 B downloaded and hashed, never loaded | artifact_access_checked |
| Read CPU ZIP via byte ranges with 15MB total cap; central-directory listing and selected members only | All used responses206; **3,699,756 network B**; selected ZIP reads/CRC succeeded. Full 54,564,140-B ZIP was **not** acquired or hashed. [CPU_RANGE_ACCESS.json](_WORK/W2_01_EVIDENCE/CPU_RANGE_ACCESS.json), [CPU_BUNDLE_MANIFEST.json](_WORK/W2_01_EVIDENCE/CPU_BUNDLE_MANIFEST.json), [CPU_SELECTED_HASHES.json](_WORK/W2_01_EVIDENCE/CPU_SELECTED_HASHES.json), `range_bundle.py` | artifact_access_checked + local_test (ZIP parsing only) |
| Parse CPU detector ONNX; independently reparse already-local tiny ONNX and tiny pipeline | [DETECTOR_GRAPH.json](_WORK/W2_01_EVIDENCE/DETECTOR_GRAPH.json), [TINY_EXISTING_GRAPH_REPARSE.json](_WORK/W2_01_EVIDENCE/TINY_EXISTING_GRAPH_REPARSE.json), [TINY_EXISTING_PIPELINE.json](_WORK/W2_01_EVIDENCE/TINY_EXISTING_PIPELINE.json), `compare.py` | local_test (static only, no new tiny retrieval) |

No visual interpretation of output JPGs, untrusted pickle loading, inference session, synthetic inference, frame decoding or event scoring occurred. Web tool open failed and exact-name search returned no results; neither is evidence that other files do not exist. Primary source GETs and the saved publisher tree provide the positive evidence below.

<a id="F267"></a>
### F267 — W2_01: W2-01-F001 — Acquired exact pose archive, hash and dependencies

Provenance: [W2_01:28](_WORK/W2_01.md); original aliases: W2-01-F001. Sources: [S003](SOURCES.md#S003).

## [W2-01-F001](RAW_FACTS.md#F267) — Acquired exact pose archive, hash and dependencies

**[artifact_access_checked + local_test]** Publisher archive is:

https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/onnx_sdk/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip

50,799,818 bytes, SHA256 **`f7fbb6c5c11a1bb70f3d445e4ddec5d144ea89ad5649c081ef976f9b24a0b741`**. Response Last-Modified 2023-08-31; filename's 2023-05-04 is not our download date or a verified training date. Member prefix is `20230831/rtmpose_onnx/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504/`:

| Member | Uncompressed bytes | SHA256 |
|---|---:|---|
| `deploy.json` | 356 | `42cdb5a0b67478b5650aa499a9c2ba7f852d5c168e1b482c330b57f4cc2c324e` |
| `pipeline.json` | 3,647 | `212763bd04f0f883491f32db5fbaaf75ae50c756556650468b08868fb0e0d7f0` |
| `detail.json` | 1,242 | `7f91c5a2676c6b544d7d8fe3e3c740293ce1d4fae6ee27825122865f304d9095` |
| `end2end.onnx` | 54,330,655 | `5c0a4bf67953e6d2ac43ce15e77dc9d5d354ae18430a47d2c5963a7bc5683e3c` |
| `output_onnxruntime.jpg` | 44,059 | `3e4cfcc0830faf07742c954bc5cc939afd9d7e1e6669ad8250928e26c0c68761` |
| `output_pytorch.jpg` | 44,059 | same hash as preceding JPG |

JPGs are byte-identical illustrations; they do **not** establish tensor parity or a fresh inference test. No detector, license, notice, source image, source checkpoint, tracker, SDK runtime library or external ONNX data member is bundled. `deploy.json` declares PoseDetector, MMDeploy1.2.0, `topdownposeestimator`, `backend=onnxruntime`, `precision=FP32`, `batch_size=1`, `dynamic_shape=true`, `weights=""`, `customs=[]`. Runtime dependencies remain external even though graph weight tensors are internal.

<a id="F268"></a>
### F268 — W2_01: W2-01-F002 — Actual graph and joint semantics

Provenance: [W2_01:47](_WORK/W2_01.md); original aliases: W2-01-F002. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-01-F002](RAW_FACTS.md#F268) — Actual graph and joint semantics

**[local_test: static parse/check]** ONNX IR6, producer `pytorch` version `1.9`, default-domain opset11. Input **`input: FLOAT [batch,3,256,192]`**. Outputs **`simcc_x: FLOAT [batch,MatMulsimcc_x_dim_1,384]`** and **`simcc_y: FLOAT [batch,MatMulsimcc_x_dim_1,512]`**. The exported joint dimension is symbolic; do not present the serialized output declaration as literal17. Independent static evidence is `head.final_layer.weight [17,768,7,7]` and bias[17], plus publisher COCO17 configuration. Runtime output-axis validation is still required.

247 nodes, 141 initializers (138 FLOAT, 3 INT64), no initializer external-data references, no model metadata, no non-default operator domains. Operator counts: Conv62, Sigmoid58, Mul72, Add12, Concat6, GlobalAveragePool4, HardSigmoid4, MaxPool3, Shape1, Slice1, Reshape1, ReduceSum2, Sqrt2, Clip2, Div3, MatMul7, Split2, Unsqueeze1, Squeeze2, Transpose1, Relu1. Graph outputs end in two MatMul nodes. Argmax, crop, color conversion and original-image decoding are outside this graph. Ordinary ONNX operators are **not** proof the issued LinQ compiler supports their exact shapes/semantics; dynamic batch and symbolic output axis may require a device-specific fixed-batch export/compilation step later.

**[primary_docs]** README identifies the 17-joint output as COCO convention: nose, left/right eye, left/right ear, left/right shoulder, elbow, wrist, hip, knee, ankle. “body7” denotes training mixture, not seven output joints. Output confidence is a distribution-response score, not COCO visibility v, calibrated probability, or evidence of no occlusion. No video PTS/actor IDs/event labels exist in this model artifact. A downstream record must retain source PTS, person-track reference, bbox provenance, exact crop transform, observed/unknown joint status and all raw scores.

<a id="F269"></a>
### F269 — W2_01: W2-01-F003 — Freeze the SDK preprocessing and decoder, not a similarly named Python path

Provenance: [W2_01:55](_WORK/W2_01.md); original aliases: W2-01-F003. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-01-F003](RAW_FACTS.md#F269) — Freeze the SDK preprocessing and decoder, not a similarly named Python path

**[artifact_found + primary_docs]** Actual `pipeline.json` independently confirms: load image; bbox center/scale with padding1.25, image_size[192,256]; TopDownAffine; Normalize mean[123.675,116.28,103.53], std[58.395,57.12,57.375], **to_rgb=true**; ImageToTensor; Collect metadata including bbox_score/center/scale; graph; `SimCCLabelDecode`. Its decoder params are input_size[192,256], sigma[4.9,5.66], split_ratio2, normalize=false, use_dark=false, flip_test=false. No extra `/255` is specified.

**[primary_docs]** MMDeploy v1.2.0 tag resolves to commit **`6cd29e2152d6935bde2f9252b47170724bac20ac`** (saved tag response). The exact SDK source gives this static contract:

1. `TopDownGetBboxCenterScale` receives **xywh**, computes center=(x+w/2,y+h/2), expands width/height to 192/256 aspect, scale=(expanded_w,expanded_h)/200×1.25. Keep original-image box units. Conversion from a detector's xyxy must happen explicitly.
2. `TopDownAffine` multiplies scale by200, rounds the ROI, intersects with image boundaries, rounds/intersects destination ROI, invokes **CropResizePad**, and replaces center/scale with corrected values. Those corrected metadata values feed decoding. The actual code is saved; generic “affine resize” is insufficient to reproduce edge/truncation behavior. Empty/tiny/invalid crops need a defined rejection path in a later implementation.
3. Normalize converts input image to RGB once and uses the pipeline's channel statistics; output tensor is channel-first FLOAT with batch1 reference.
4. Decoder locates argmax independently over each x and y distribution. Score is **min(max_x,max_y)**; score<=0 marks both raw locations -1. Divide coordinates by2. Original-image mapping is `x = x_crop * scale_x*200/192 + center_x - scale_x*200/2`, with analogous y/256. Use corrected metadata, not the uncorrected detector box. Ignore invalid-joint coordinates even though source mapping subsequently transforms them.
5. Decoder source copies SimCC tensors to CPU and waits on its stream; no neural-network execution on CPU is established by that fact. `batch_size=1` remains our explicit reference; graph-symbolic batch is not a tested batched wrapper contract. No softmax, DARK refinement, flip augmentation or mean-of-maxima score is part of this SDK decoder.

**[contradiction / source difference]** At pinned MMPose README revision, `examples/onnxruntime/main.py` reads BGR via `cv2.imread`, calls its own `cv2.warpAffine` path and subtracts RGB-ordered statistics without conversion. Its min-score decoding matches the SDK score rule, but its color/crop path is a different source contract. No numeric error magnitude is claimed without parity testing. This matters before quantization: do not blame m-body7 or LinQ for errors introduced by joining incompatible wrappers.

<a id="F270"></a>
### F270 — W2_01: W2-01-F004 — Exact source checkpoint is found; full body7 training provenance is not closed

Provenance: [W2_01:69](_WORK/W2_01.md); original aliases: W2-01-F004. Sources: [S390](SOURCES.md#S390).

## [W2-01-F004](RAW_FACTS.md#F270) — Exact source checkpoint is found; full body7 training provenance is not closed

**[artifact_found]** Actual `detail.json` names:

https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.pth

HEAD200, 54,551,099 B. It was not downloaded/loaded; no numerical PyTorch↔ONNX parity is claimed. This is the corresponding source **declared by exporter metadata**, stronger than a similar filename, but not an independent export reconstruction. W1 A01 `...aic-coco...63eb25f7_20230126.pth` is a different checkpoint and must not replace it.

**[primary_docs + unknown]** Archive declares MMPose1.1.0 and exporter-local config `../mmpose-wb/projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-m_8xb256-420e_coco-256x192.py`. Public named config fetched at both README pinned revision and v1.1.0 contains COCO dataset training, COCO17 RTMCC head and AIC+COCO CSPNeXt initialization; its own `flip_test=True` differs from actual exported SDK false. README links this same architecture config to both AIC+COCO and body7 checkpoints. Thus the public COCO config supplies architecture/codec context, **not a recovered exact seven-dataset training recipe**. The saved complete tree at pinned revision has no RTMPose body7 training path (RTMO body7 paths exist); that bounded search does not prove no other revision/repository has one. No teacher checkpoint is declared for this exact body7 export. DWPose/wholebody distillation references concern other models and cannot fill this gap.

**[author_claim]** README says body7 training combines AI Challenger, COCO, CrowdPose, MPII, sub-JHMDB, Halpe and PoseTrack18; Body8 evaluation adds OCHuman. Exact mixture/sampling/annotation conversion/teacher are not established. This is sufficient for artifact evaluation; it prevents claiming training reproducibility or cleared upstream training media.

<a id="F271"></a>
### F271 — W2_01: W2-01-F005 — Detector dependency: exact recipe artifact versus actual demo ZIP

Provenance: [W2_01:81](_WORK/W2_01.md); original aliases: W2-01-F005. Sources: [S391](SOURCES.md#S391), [S392](SOURCES.md#S392).

## [W2-01-F005](RAW_FACTS.md#F271) — Detector dependency: exact recipe artifact versus actual demo ZIP

**[primary_docs]** Pinned README lines around ONNX export explicitly pair RTMPose with config `projects/rtmpose/rtmdet/person/rtmdet_nano_320-8xb32_coco-person.py` and:

https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_nano_8xb32-100e_coco-obj365-person-05d8511e.pth

**[artifact_access_checked]** Acquired 4,224,050 bytes, SHA256 **`05d8511e7b3fabc62e27d2f624179e004ad14ee63a86ca9d9d22c88f3db0eee1`**. No pickle execution. Config has one `person` class (`num_classes=1`, metainfo `('person',)`), 320×320 keep-aspect resize, padding114, score_thr .05, NMS IoU .6, nms_pre1000, max_per_img100. Its inheritance is external `mmdet::rtmdet/rtmdet_l_8xb32-300e_coco.py`; full mmdetection/runtime versions must be pinned for export. Filename's Objects365/COCO training label is not recovered training config. One-class label0 is the expected person index from this config, not a measured output of the PTH.

**[artifact_access_checked + contradiction]** README also recommends https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmpose-cpu.zip . HEAD200/54,564,140 B. Bounded ranged ZIP inspection establishes:

- Actual detector `detail.json`: MMDeploy **1.0.0rc1**, mmdet **3.0.0rc2**, local PTH `../rtmdet_nano_8xb32-300e_coco-person_in1kpretrain/rtmdet_nano_8xb32-300e_coco-person_in1kpretrain-96154d0b.pth`. This is **not** the100e `05d8511e` recipe checkpoint. The local96154d0b PTH is not included; its public source URL is unknown here.
- Actual paired pose `detail.json`: MMPose1.0.0rc0; local `/home/PJLAB/jiangtao/Downloads/rtmpose-m-aic-coco.pth`, old config `rtmpose-m_8xb256-420e.py`. This is **not** the body7 archive. Its large graph was intentionally not fetched.
- Retrieved detector `end2end.onnx` is 4,012,393 B, SHA256 **`b8585adb6d1352796f6e86337e09c3459b830645a7e7192d9381670bea2facbd`**. Static schema check passes: IR6/opset11, FLOAT input[batch,3,height,width], FLOAT dets[batch,num_dets,Reshapedets_dim_2], INT64 labels[batch,num_dets]; 688 nodes, default domains, no external initializers. Includes NonMaxSuppression1, TopK2, Resize2, Range8, Gather38, dynamic-shape arithmetic. Exact counts in DETECTOR_GRAPH. These pose-independent dynamic/NMS ops add a distinct LinQ compiler gate.
- This detector's actual pipeline is BGR (`to_rgb=false`) normalization mean[103.53,116.28,123.675], std[57.375,57.12,58.395], resize320 keep_ratio, pad114, `ResizeBBox` postprocess. Do not apply pose RGB statistics to it. Export detail has score_threshold .05, confidence_threshold .005, IoU .5, max_output_boxes_per_class200, pre_top_k5000, keep_top_k100; pipeline postprocess separately has NMS IoU .6, score_thr .05, max_per_img100. Preserve both layers rather than choosing one undocumented threshold.

**Effect [inference]:** this acquired old detector could be a separately named candidate, but its unknown local source provenance and old SDK contract demote it as the default exact body7 partner. Preferred future route is export exact acquired05d8511e with pinned complete mmdetection/MMDeploy stack or use an independently verified target person detector. Both require a named model and separate input/decode contract; neither is supplied by the body7 ZIP. Publisher recipe is a build plan, not an already matched deploy bundle. Detector outputs must be mapped back to original frame before xyxy→xywh crop input, and misses remain unknown for downstream behavior rules.

<a id="F272"></a>
### F272 — W2_01: W2-01-F006 — Tiny comparison changes cost hypothesis, not semantics or safety evidence

Provenance: [W2_01:98](_WORK/W2_01.md); original aliases: W2-01-F006. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-01-F006](RAW_FACTS.md#F272) — Tiny comparison changes cost hypothesis, not semantics or safety evidence

**[local_test + primary_docs]** Independently reparsed already-acquired tiny ONNX: 13,350,364 B, SHA256 `a6c2f6a3896a4d51131d14d7a80a3d08b50f559af5a58a45d5b098aef510a70f`, IR6/opset11, same exact input and symbolic-output shapes, no external tensors, 168 nodes rather than247. Tiny pipeline SHA256 equals m pipeline **`212763bd04f0f883491f32db5fbaaf75ae50c756556650468b08868fb0e0d7f0`**. Its saved detail also says MMDeploy1.2/MMPose1.1. Thus m adds graph size/complexity, not a new crop/color/decode interface. This local reparse did not repeat tiny network access.

**[author_claim]** Same README Body8 table gives body7 m COCO AP74.9 versus t65.9, Body8 PCK94.25 versus91.44, with m13.59M/1.93G and t3.34M/.36G. The README evaluation and flip-test caveats from M01 remain; these are published nonindustrial conditions, not target evidence or LinQ throughput estimates. Accuracy priority motivates **testing** m, not automatically preferring it: actual far-worker/occlusion joint visibility, detector misses, causal event recall and alert latency decide. Neither pose directly classifies falling versus intentional lying, immobility, harness attachment, consciousness, unsafe carrying or physical distance.

<a id="F273"></a>
### F273 — W2_01: W2-01-F007 — Notices and rights by layer

Provenance: [W2_01:104](_WORK/W2_01.md); original aliases: W2-01-F007. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-01-F007](RAW_FACTS.md#F273) — Notices and rights by layer

**[primary_docs]** MMPose pinned LICENSE and MMDeploy1.2 LICENSE are Apache2.0 code grants with copyright/license/notice-preservation conditions and warranty disclaimer; retain them with derived code distributions. MMPose `LICENSES.md` lists an EDPose exception, not this RTMPose path. Source files bear OpenMMLab copyright comments. README requests citation and warns multi-domain practical model results are unsuitable for academic comparison. These notices should accompany the reference, without treating a citation request as a newly inferred legal prohibition.

**[artifact_access_checked + unknown]** Actual body7 ZIP has no LICENSE/NOTICE/model card; root NOTICE GETs at inspected MMPose/MMDeploy references returned404, not a global statement that no notice exists. The README/public weight links establish publication/access, but no distinct weight-specific grant was found in this bounded check. Do not erase positive Apache code grants, and do not elevate them into a verified grant for every trained checkpoint or seven underlying datasets. Rights layers:

| Layer | Established | Remaining |
|---|---|---|
| MMPose/MMDeploy code | Apache2.0 at saved references; EDPose exception separately listed | Package transitive OpenCV/ORT/mmdetection/other notices must be collected for actual build |
| Exact m-body7 ONNX/PTH | Official artifact/meta source declaration, access; ONNX hash | Separate model-weight grant scope not explicitly established; source PTH parity unrun |
| Detector05d8511e PTH | Official recipe and acquired hash | Exact matching export, full train recipe and specific weight grant scope |
| Old CPU-bundle detector ONNX | Official bundled bytes and static contract | Local96154d0b source and matching source rights unknown |
| Training media/annotations | Seven dataset names author-declared | Per-dataset terms, upstream media, conversion and redistribution scopes separate |
| Target video / event GT | None added by this work | Source rights, annotations, grouped split and industrial consent/access remain external |

<a id="F274"></a>
### F274 — W2_01: Exact first-run gates and residual K001 scope

Provenance: [W2_01:119](_WORK/W2_01.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Exact first-run gates and residual K001 scope

**Prepared now:** hash-pinned body7 graph/metadata, exact SDK1.2 preprocessing/decode source, actual body7 source-PTH URL, acquired recipe person PTH, counterexample proving CPU demo substitution is wrong, exact static tiny comparison. This is an exact **pose artifact contract**, not a full execution PASS.

1. **Build/reference gate:** choose the full versioned person-detector export and SDK/runtime implementation. Never use the old demo ZIP under the new recipe checkpoint's name. Bundle licenses/dependencies and agree allowed host CPU boundaries. No issued SDK/device means no support claim.
2. **Preprocessing/decoder gate:** under future authorized CPU/RTX execution, freeze batch1 and test image-color/channel statistics, in-frame/edge/truncated/empty bboxes, coordinate restoration, symbolic joint count17, both outputs and invalid-score handling. Compare exact SDK1.2 CropResizePad path against any alternate port before adopting its thresholds. Use actual corresponding body7 PTH only for numerical parity. JPG equality is insufficient.
3. **Detector→pose gate:** evaluate person box misses, crowded/partial workers, original-frame mapping and person association separately. Audit altered crop/score thresholds as a model change. A chosen crop port and independent detector constitute a newly named reference, not demonstrated publisher parity.
4. **Target/event gate:** causal video replay preserving PTS, target joint visibility/scale/occlusion strata, fall-transition versus lying/ADL controls, dropped frames and track switches, timely recall, false alerts/camera-hour and onset/notification latency. No event success follows from static schema compatibility. Source-media/annotation rights and held-out scene/subject grouping are required before validation claims.
5. **LinQ gate:** actual compiler/runtime with fixed graph/precision/input/output contracts, unsupported-operator report, verified execution location, quality delta and measured end-to-end latency. ONNX opset11 and zero custom operators alone are insufficient. Detector dynamic/NMS path and pose MatMul/normalization subgraphs are separate possible blockers; no unsupported claim is made absent SDK evidence.

<a id="F275"></a>
### F275 — W2_02: W2_02 — K002: original fall video, source clocks and visible-state development fixture

Provenance: [W2_02:1](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_02 — K002: original fall video, source clocks and visible-state development fixture

Access/review: **23 October 2026, approximately 23:10–23:20 Europe/Moscow** (20:10–20:20 UTC; individual HTTP times in evidence). Assignment is [PROMPT_FULL.md](_WORK/W2_02_EVIDENCE/PROMPT_FULL.md); substantive adaptations and corrected intermediate hypotheses are preserved in [METHOD_NOTES.md](_WORK/W2_02_EVIDENCE/METHOD_NOTES.md). Exclusive evidence directory: `W2_02_EVIDENCE/`. Read frozen K002, W1 M03/D10/D15, CASE_NOTES and SYNTHESIS_CONTRACT; original briefs govern. Root's direct case PDF reading is case provenance, not my independent case inspection.

**Decision:** K002 is **scope_narrowed**, not fully closed. A small actual-media/annotation/source-clock **development fixture now exists**: two previously familiar GMD originals, a newly reviewed subject4 member selected from the frozen test list, and the URFD adl-10 preview. All four fully decoded, with every frame PTS retained. The source-clock join is established for these bytes; exact automatic action boundaries are not independent visible-state truth. No clip demonstrates a complete ten- or thirty-second post-transition hold. URFD adl-10 reclines on a sofa, and subject4 Fall01 falls onto a bed/cot: posture names must not be promoted to ground fall or unconsciousness. All reviewed material is development/reviewed, including source-test subject4.

No inference, training, paid API/compute, LinQ execution, model accuracy or event benchmark was performed. `local_test` below means actual hashing, CSV parsing, source-code inspection and sequential video decoding, never neural execution. No independent human annotators were available; the manual observations are **preliminary single-researcher visual interpretation**, not consensus GT. No subagents, outreach, large archive or source-repository mutation.

<a id="F276"></a>
### F276 — W2_02: Source and artifact register

Provenance: [W2_02:9](_WORK/W2_02.md); original aliases: section record. Sources: [S237](SOURCES.md#S237), [S239](SOURCES.md#S239), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255), [S400](SOURCES.md#S400), [S401](SOURCES.md#S401), [S402](SOURCES.md#S402), [S403](SOURCES.md#S403), [S404](SOURCES.md#S404), [S405](SOURCES.md#S405), [S406](SOURCES.md#S406), [S407](SOURCES.md#S407), [S408](SOURCES.md#S408), [S409](SOURCES.md#S409), [S410](SOURCES.md#S410).

## Source and artifact register

**[W2-02-S01](SOURCES.md#W2-02-S01) [primary_docs + artifact_access_checked] — Ekram Alam et al., GMDCSA24 source repository**, pinned commit `5abac7693229900cf80f722e878fbb119211fc1c`; README credits Alam, Sufian, Dutta, Leo and Hameed. Tree: https://api.github.com/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/git/trees/5abac7693229900cf80f722e878fbb119211fc1c?recursive=1 . Newly acquired tree HTTP200/50,585B, saved `gmd_tree.json`. An initial call returned403 rate limit; subsequent ordinary request succeeded. No authentication/bypass. Primary file endpoints:

- https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/Subject%201/Fall/11.mp4
- https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/Subject%203/ADL/08.mp4
- https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/Subject%204/Fall/01.mp4

First two bodies were reused from sibling feasibility `_WORK/W1-09_samples/positive_S1_F11.mp4` and `negative_S3_A08.mp4`, copied here as `S1_F11.mp4` and `S3_A08.mp4`. This is not a new HTTP availability assertion for those two bodies. **New independent identity check** calculated Git blob SHA1 from each local body (`blob <length>\0<body>`) and compared with the newly fetched pinned tree: all three match exactly, including newly downloaded `S4_F01.mp4` HTTP200/1,714,708B. Thus older report interpretation is secondary, but identity and this decode/visual review are independently rechecked. `blob_identity.json` records source paths, sizes, tree blob IDs and equality.

**[W2-02-S02](SOURCES.md#W2-02-S02) [primary_docs] — Ekram Alam, Zenodo GMDCSA24 v2.1, published 2024-08-21**, DOI10.5281/zenodo.13354453. https://zenodo.org/records/13354453 ; newly fetched https://zenodo.org/api/records/13354453 HTTP200/3,960B, saved `zenodo.json`. Metadata licence `cc-by-4.0`; single ZIP1.1GB not downloaded. New tag check https://api.github.com/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/git/ref/tags/v2.1 HTTP200 links tag to exact `5abac769...` commit (`gmd_tag.json`). GitHub pinned LICENSE HTTP200/1,067B grants MIT under Ekram Alam2024; pinned README HTTP200/1,878B. Repository MIT and Zenodo CC BY4.0 are positive publisher grants, not an absence-of-licence finding. They differ by publication layer; verify desired distribution route and retain attribution. Actor/privacy/industrial deployment clearances are not established by these grants.

**[W2-02-S03](SOURCES.md#W2-02-S03) [artifact_found + local_test] — David Schneider et al., author-linked OmniFall labels/splits**, HF revision `83572a37b9e3081df8c06a56874b1d1f2a19386c`. https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/83572a37b9e3081df8c06a56874b1d1f2a19386c/labels/GMDCSA24.csv ; split https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/83572a37b9e3081df8c06a56874b1d1f2a19386c/splits/cs/gmdcsa24/test.csv . Reused exact saved W1 files, now copied here; re-parsed relevant rows and split membership. Schema `path,label,start,end,subject,cam,dataset`; seconds, extensionless paths. Local label map:8 standing,1 fall,2 fallen,5 lie_down,6 lying. Newly fetched pinned LABELS.md HTTP200: static motions start at rest; fallen may still contain ground-level movement; all videos relabelled under OmniFall semantics. Old source labels and new action seconds are not interchangeable. Existing README frontmatter CC BY-NC4.0 versus narrative annotations/splits CC BY-NC-SA4.0 discrepancy remains; no new permission resolution. Underlying video grants do not resolve annotation licence.

**[W2-02-S04](SOURCES.md#W2-02-S04) [primary_docs + artifact_access_checked] — Schneider / simplexsigil, omnifall-package**, commit `db33701e1911354b604422e748cb6acc237dc413`, W1 metadata author date2026-08-27. New exact source bodies: https://raw.githubusercontent.com/simplexsigil/omnifall-package/db33701e1911354b604422e748cb6acc237dc413/src/omnifall/_prepare.py HTTP200/146,360B and https://raw.githubusercontent.com/simplexsigil/omnifall-package/db33701e1911354b604422e748cb6acc237dc413/src/omnifall/_decode.py HTTP200/17,380B. Saved unchanged; inspected, not imported/executed. Locators: `_convert_gmdcsa24` lines2117–2150; `convert_tree` copyfile line1795; decoder lines336–338 and450–472. Package code licence is distinct from annotations/media; W1 saved Apache2.0 code grant is not a weight/media grant.

**[W2-02-S05](SOURCES.md#W2-02-S05) [primary_docs + artifact_access_checked] — Michał Kępski, University of Rzeszów, UR Fall Detection Dataset**, revision unstated; primary cited work Kwolek/Kępski2014. https://fenix.ur.edu.pl/~mkepski/ds/uf.html newly HTTP200/43,416B, saved `urfd_page.html`. Official page describes nearest-timestamp synchronization, frame number/ms since sequence start, and CC BY-NC-SA4.0 intended for noncommercial academic use; commercial use requires author permission. Newly fetched https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4 HTTP200 video/mp4,2,472,849B, copied untouched here. Reused source artifacts https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-data.csv and https://fenix.ur.edu.pl/~mkepski/ds/data/urfall-cam0-adls.csv from W1 evidence_D10, now copied and independently parsed. Video preview is not the original per-frame RGB PNG archive. No claim it is byte-equivalent to those PNGs.

<a id="F277"></a>
### F277 — W2_02: Exact media identities and decoded clocks

Provenance: [W2_02:27](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Exact media identities and decoded clocks

<a id="F278"></a>
### F278 — W2_02: W2-02-F01 [local_test; S01/S03/S05]

Provenance: [W2_02:29](_WORK/W2_02.md); original aliases: W2-02-F01. Sources: [S237](SOURCES.md#S237), [S239](SOURCES.md#S239), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255), [S400](SOURCES.md#S400), [S407](SOURCES.md#S407), [S408](SOURCES.md#S408).

**[W2-02-F01](RAW_FACTS.md#F278) [local_test; S01/S03/S05]** PyAV18.1.0, libavcodec62.28.102/libavformat62.12.102, sequential `container.decode(video=0)` decoded every available video frame in each file without a decoder exception. All video PTS strictly increasing. `decode.py`, `decode_manifest.json`, `*_pts_join.csv` preserve method/results. Codec h264 throughout. Raw seconds are `PTS*time_base`; relative stream seconds are `(PTS-stream.start_time)*time_base`. No clipping, resampling or padding was used to create these observations.

| File and source identity | SHA256 | Frames / resolution / time_base | Raw first–last video PTS seconds | Last relative stream timestamp / final packet support end |
|---|---|---|---|---|
| [S1_F11.mp4](_WORK/W2_02_EVIDENCE/S1_F11.mp4), Subject1/Fall11 | `c25e4fc9b669cb588b6145d2cfd94f2d403083293c08bc85fa863111372bfea7` |181 /1280×720 /1/30000|.033333–6.097400|6.064067 /6.097400|
| [S3_A08.mp4](_WORK/W2_02_EVIDENCE/S3_A08.mp4), Subject3/ADL08 | `b383bb83a22b286cfc65fdd934137ee8b29e84aef7be0b540271d7c69d10fa8b` |146 /1280×720 /1/30000|0–4.864067|4.864067 /4.896167|
| [S4_F01.mp4](_WORK/W2_02_EVIDENCE/S4_F01.mp4), Subject4/Fall01 | `be235fef9bda633f5f63ccbc28c1dbb6c0138728c5b1696d86f7a6e0c66f4516` |139 /640×480 /1/30000|0–4.624167|4.624167 /4.657500|
| [adl-10-cam0.mp4](_WORK/W2_02_EVIDENCE/adl-10-cam0.mp4), URFD adl-10 | `e8720d9d36f21c2e3222109b92d564ad3f1153927a9cf69dbd0eba0fcd003a23` |300 /640×240 /1/30|0–9.966667|9.966667 /10.000000|

Final packet support end means last frame PTS plus its decoded duration, in **relative** seconds. It describes that frame's display duration, not additional movement observations. Container duration alone is not reliable event exposure: S4 container4.675104s versus video support4.6575s. S1 raw container/stream metadata also differ in origin; keep the complete manifest rather than inferring frame timestamps from FPS. GMD rates are approximately30Hz but variable packet durations; exact PTS govern.

<a id="F279"></a>
### F279 — W2_02: W2-02-F02 [primary_docs + local_test; S03/S04] — source-to-annotation clock now resolved for fixture.

Provenance: [W2_02:40](_WORK/W2_02.md); original aliases: W2-02-F02. Sources: [S407](SOURCES.md#S407), [S408](SOURCES.md#S408), [S409](SOURCES.md#S409), [S410](SOURCES.md#S410).

**[W2-02-F02](RAW_FACTS.md#F279) [primary_docs + local_test; S03/S04] — source-to-annotation clock now resolved for fixture.** `_convert_gmdcsa24` maps `Subject N/...mp4` to `Subject_N/...` and `convert_tree` copies the file, without re-encoding. The decoder explicitly maps annotation time to `round(t/time_base)+stream.start_time`. Therefore **join on relative stream seconds**, keeping raw PTS separately. S1 start_time1000 ticks is a real .033333s offset; S3/S4 start_time0. Full relative-clock join:

| Source | Original OmniFall intervals, unchanged | Actual decoded index0 ranges selected by half-open interval join |
|---|---|---|
| S1F11 |standing[0,.52);fall[.52,2.7);fallen[2.7,6.08)|0–14;15–79;80–180|
| S3A08 |lie_down[0,3.71597);lying[3.716,4.896)|0–111;112–145|
| S4F01 |standing[0,1.14);fall[1.14,2.44);fallen[2.44,4.66)|0–33;34–72;73–138|

Half-open intervals are this fixture's explicit join convention, not a claim that original author documented all endpoint rounding choices. S3's .00003s gap contains no decoded frame. S1 final relative PTS6.064067 lies inside6.08, so **no missing-label tail or annotation overrun is inferred from its raw6.0974 PTS**. Earlier raw-clock diagnostic is superseded in METHOD_NOTES. S3 label end4.896 is ~.000167s before video support end4.896167; S4 end4.66 is .0025s after support end4.6575, within a single frame interval, not long missing footage. Unmodified label files retained. Prepared package conversion was inspected, not executed; byte-identity proof uses pinned original Git blobs plus documented copy-only converter, not a claim to have run package-wide preparation.

<a id="F280"></a>
### F280 — W2_02: W2-02-F03 [primary_docs; S04] — padded frame count cannot establish hold.

Provenance: [W2_02:50](_WORK/W2_02.md); original aliases: W2-02-F03. Sources: [S409](SOURCES.md#S409), [S410](SOURCES.md#S410).

**[W2-02-F03](RAW_FACTS.md#F280) [primary_docs; S04] — padded frame count cannot establish hold.** Decoder lines470–472 repeat the final frame if requested timestamps remain after EOF; nearest-frame sampling may also reuse a source frame. Thus a successfully returned tensor/window is not independent temporal coverage. This is a direct counterexample to using30×5 input or a nominal long window to prove a10/30-second observed hold. Our manifest ends at actual decoded observations and stores no synthetic extension.

<a id="F281"></a>
### F281 — W2_02: Visible states and counterevidence

Provenance: [W2_02:52](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Visible states and counterevidence

<a id="F282"></a>
### F282 — W2_02: W2-02-F04 [local_test + inference; S01/S03/S05]

Provenance: [W2_02:54](_WORK/W2_02.md); original aliases: W2-02-F04. Sources: [S237](SOURCES.md#S237), [S239](SOURCES.md#S239), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255), [S400](SOURCES.md#S400), [S407](SOURCES.md#S407), [S408](SOURCES.md#S408).

**[W2-02-F04](RAW_FACTS.md#F282) [local_test + inference; S01/S03/S05]** Generated labelled contact sheets with index0/raw time/relative time/annotation code; directly visually inspected all sheets at5fps across whole clips plus all decoded frames in bounded transition neighborhoods. Exact intervals: S1 raw[.4,2.9], S3[2.9,4.1], S4[1.05,2.65], URFD[5.2,7.1]. These give exhaustive frame review of those neighborhoods only. Earlier S3 lowering and later UR reclining were reviewed with whole-clip5fps samples; no claim every full-file frame was human reviewed. Review resolution300px thumbnails can conceal subtle movement; coarse absence of gross displacement is not physical immobility, breathing absence or consciousness evidence. `manual_preliminary.jsonl` carries separate proposed observational spans, role, source split, grouping, visibility and censoring. Numeric spans below are **approximate review anchors**, not adjudicated event boundaries.

| Fixture / original source split | Direct visual observation | Low posture and coarse movement | Censoring / interpretation |
|---|---|---|---|
|S1F11 /train subject1|Standing, then side descent through squat/supporting hand to tiled floor. Clear gross lowering occurs later than annotation fall start. Body broadly visible.|Low posture at sampled raw2.8s onward; bent-leg position changes during fallen interval, including ~3.8–4.0s. No gross displacement at sampled raw4.2–6.0974s.|No recovery before EOF. Single staged fall example; label fallen is not equivalent to sustained low-motion from2.7. Manual sidecar uses relative times, with conservative sampled low-motion anchor4.2–6.0641.|
|S3A08 /train subject3|Already low/seated at start; supporting arm, controlled lowering onto side on floor mat. No abrupt accident observed.|Already near-horizontal by sampled2.4s; broadly stable after2.6s through4.8641. OmniFall lie_down continues until3.71597, later than gross posture change.|Left-censored preceding standing/history; right-censored lying; deliberate-looking ADL hard negative, no independent intent claim beyond observed controlled motion and source ADL label.|
|S4F01 /frozen test subject4, now development/reviewed|Source tree confirms exact member. Actor stands on raised bed/cot, initially head cropped; descends onto that surface, with supporting arm/bent-leg adjustment.|Low on bed by sampled2.65s; broadly stable sampled3.0–4.6242. Surface/support and doorway compromise interpretation.|No ground fall or injury visible. No recovery before EOF. Source test membership retained as provenance, but this reviewed member is contaminated for our blind evaluation. Keep all its derivatives with subject4 group.|
|URFD adl-10 /official subject split not established|Walks forward, bends/sits on sofa at right, then reclines along sofa. Source MP4 is depth/RGB side-by-side preview, not pure RGB camera image.|Recline evolves after ~6.2s and still changes through ~7.8s. Partial posture looks stable at8–9.9667s; much of body is outside right RGB boundary.|No ground fall observed; significant cropping means whole-body low-motion unknown. Right-censored; no recovery. +1 label is not sufficient ground-location/accident evidence.|

Source annotations are retained unchanged beside these observations. The visual discrepancies do not silently repair or invalidate the published labels: action definitions, support surface and our target event are different. For S1 the very early fall start may encode preparation; for S3 rest/settling judgement differs from first horizontal posture. Only independently defined target annotation can settle onset-latency GT.

<a id="F283"></a>
### F283 — W2_02: W2-02-F05 [local_test + inference; S05] — URFD sync/frame/posture join.

Provenance: [W2_02:65](_WORK/W2_02.md); original aliases: W2-02-F05. Sources: [S237](SOURCES.md#S237), [S239](SOURCES.md#S239), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255).

**[W2-02-F05](RAW_FACTS.md#F283) [local_test + inference; S05] — URFD sync/frame/posture join.** Both sync CSV and adl-10 feature-label subset contain exactly300 records, source frame1–300 with no holes. Joining `source_frame=decoded_index0+1` yields:

| Source frame | Preview PTS seconds | Source synchronization ms | Posture code | Visible state around this point |
|---|---:|---:|---:|---|
|1|0|0|-1|actor far back, upright|
|169|5.600000|5600|-1|already sitting/support transfer|
|170|5.633333|5632|0|seated/reclining transition|
|199|6.600000|6599|0|reclining sideways|
|200|6.633333|6630|+1|still visibly adjusting/reclining on sofa|
|300|9.966667|9968|+1|partially cropped reclined tail|

Preview is CFR30; source sync is nonuniform, with `sync_ms−preview_pts_ms` ranging **−12.333 to+11.333ms**. Equal counts and visible matching progression support this **ordinal preview join** for the bounded fixture; they do not prove each MP4 image is pixel-equivalent to canonical source PNG or preserve their true capture clock. For source-time evaluation, retain sync timestamps, not assumed frame/30. Canonical PNG-to-preview per-frame identity remains unverified because no RGB PNG ZIP was downloaded. `0` spans frame170–199 even though no accident is observed, and `+1` begins while body continues settling on sofa. Thus neither code directly supplies fall onset, ground location or immobility interval. Source label definitions calling +1 lying on ground require this visible-state caveat for adl-10; do not generalize all1,470 ADL+1 rows as confirmed floor lying.

<a id="F284"></a>
### F284 — W2_02: What hold durations are actually available

Provenance: [W2_02:78](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## What hold durations are actually available

<a id="F285"></a>
### F285 — W2_02: W2-02-F06 [local_test + inference; S03/S05]

Provenance: [W2_02:80](_WORK/W2_02.md); original aliases: W2-02-F06. Sources: [S237](SOURCES.md#S237), [S239](SOURCES.md#S239), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255), [S407](SOURCES.md#S407), [S408](SOURCES.md#S408).

**[W2-02-F06](RAW_FACTS.md#F285) [local_test + inference; S03/S05]** Use last **actual observation**, not last display support, when bounding measured continuous evidence. These are maximum labelled tails available, not validated motionless durations:

| Fixture | Tail start convention | Last observed time | Available labelled observation horizon | Caveat |
|---|---:|---:|---:|---|
|S1F11|fallen2.7 relative|6.064067|**3.364067s**|leg motion inside fallen; coarse stable anchor4.2 allows at most1.864067s, sampled evidence only|
|S3A08|lying3.716|4.864067|**1.148067s**|controlled lying negative; more low-posture time visually possible, does not change published interval|
|S4F01|fallen2.44|4.624167|**2.184167s**|bed/cot; sampled stable anchor3.0 allows at most1.624167s|
|URFD adl-10|+1 source6630ms|9968ms|**3.338s** source clock|continues reclining, cropped; whole-body motion eligibility unknown|

No10s post-event hold is available in any of these files; no30s hold is available. Even UR preview total10s is not10s lying exposure. A rule requiring longer than these tails is **right-censored/unassessable**, not a missed alarm or a successful negative; do not loop/pad clips or tune N downward merely to pass. No complete clear/rearm cycle can be scored since none shows recovery. Smaller candidate holds still require independent motion/visibility annotation and an operational policy; these numbers do not recommend a dwell threshold.

<a id="F286"></a>
### F286 — W2_02: Rights, grouping and practical contract

Provenance: [W2_02:91](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Rights, grouping and practical contract

<a id="F287"></a>
### F287 — W2_02: W2-02-F07 [primary_docs + inference]

Provenance: [W2_02:93](_WORK/W2_02.md); original aliases: W2-02-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-02-F07](RAW_FACTS.md#F287) [primary_docs + inference]** Media, annotations, code and weights remain distinct. GMD v2.1 MIT repository and Zenodo CC BY4.0 grants support a real accessible data lead; preserve attribution and exact release. OmniFall annotation NC/SA discrepancy remains a separate clarification gate and does not cancel source-video grants. URFD source page explicitly restricts intended use to noncommercial academic; competition/commercial deployment use needs scope clarification/permission. Source preview access does not authorize unrestricted redistribution. Our sheets/sidecars inherit relevant underlying media/annotation obligations. There are no weights or inference claims in this branch. Industrial-person recording/privacy/site permissions are unknown, not supplied by laboratory corpus grants.

Operational fixture schema is concrete: `(dataset,path,original_sha256,commit/source_url)`, frozen source split, **current_role=development/reviewed**, subject/session/scene/view groups, raw pts/time_base, stream_start, relative seconds, source-frame/sync ms, original action/posture label, manual preliminary observation/visibility, left/right censoring, annotator/provenance, recovery_observed. Key example: S1F11 index80 has relative2.704233 and fallen label while raw2.737567; URFD index199 maps frame200, source6630ms, preview6.633333, posture+1, sofa-recline observation and cropped-body caveat. Do not replace unknown spans with negative labels.

Use this pack first for **engineering integrity**: verify decoder/source clock contracts, render original-time overlays, test visibility resets and distinguish floor lying from bed/sofa lying. One-to-one event scoring and later 1/2/5/native-FPS comparisons should replay source PTS causally, with requested versus actual selected frame timestamps logged to prevent duplicated samples from inflating observed hold. All views/derived frames/windows from a parent stay together; source subject1/3 are already reviewed train provenance; subject4 Fall01 remains source-test provenance but is now reviewed development. Unreviewed subject4 members cannot automatically be claimed a fresh blind industrial lockbox, especially once subject4 scene/actor is familiar.

<a id="F288"></a>
### F288 — W2_02: K002 outcome and exact remaining gates

Provenance: [W2_02:99](_WORK/W2_02.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## K002 outcome and exact remaining gates

<a id="F289"></a>
### F289 — W2_02: W2-02-F08 — K002: scope_narrowed.

Provenance: [W2_02:101](_WORK/W2_02.md); original aliases: W2-02-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-02-F08](RAW_FACTS.md#F289) — K002: scope_narrowed.** The bounded artifact gap is substantially addressed: exact source bytes, new member selection, full decode PTS, source-code clock offset, local annotation join, visible-state negatives and censor horizons now saved. Conditional closure applies only to **this four-video development fixture's source-clock/annotation traceability**. It does not close independent event GT, immobility validation or industrial readiness.

Remaining gates are exact:

1. **Independent annotation:** at least a second independent annotator and adjudication under an explicit target definition: observable descent onset, surface/contact ambiguity, rest/low-motion, visibility and recovery. Current AI-assisted review cannot be labelled consensus human GT. Preserve disagreement and uncertain intervals; do not silently rewrite OmniFall.
2. **URFD canonical capture identity:** compare frame-numbered original PNGs against preview, preserve source sync and per-view mapping. Ordinal preview alignment is useful but weaker than source-image identity.
3. **Hold collection:** collect authorized unextended continuous tails and recoveries covering whichever hold policy team selects, with natural negatives (rest/maintenance/crouch/sofa/floor work), occlusions and industrial camera shifts. This pack cannot establish10/30s recall or negative exposure FP/hour.
4. **Locked evaluation split:** define fresh grouped parent/actor/site holdout before tuning. All material reviewed here is dev; original source split is provenance. No standalone group here proves new-site industrial generalization.
5. **Rights:** resolve OmniFall annotation grant discrepancy and URFD intended-use scope; retain positive GMD grant rather than describing all fall media as uncleared. No outreach sent.
6. **Actual engineering execution:** choose lawful exact model/checkpoint/input cadence; run causal CPU/RTX replay and event evaluation later. LinQ SDK/device path and host-boundary acceptance remain organizer/SDK dependent. No inference/latency or export-support assertion follows from this fixture.

MCF scenario23 contradiction remains separate and open until permitted meaningful footage review; no3.8GB archive acquired. udayraj/Rchit training/weight restrictions remain W1 reserve reasons, not reproduced or waived. Practical effect: fall/lying becomes a stronger **conditional development candidate** with proven source-clock tooling and explicit hard negatives, while sustained immobility/medical interpretation stays outside demonstrated readiness.

<a id="F290"></a>
### F290 — W2_03: W2_03 — K003: CCTV gait, independent image/clock verification

Provenance: [W2_03:1](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_03 — K003: CCTV gait, independent image/clock verification

Проверка выполнена 23.10.2026, около 23:10–23:18 MSK (20:10–20:18 UTC). Прочитаны индивидуальное задание, CRITIC.md K003, `_WORK/CASE_NOTES.md`, `_WORK/SYNTHESIS_CONTRACT.md`, относящиеся к задаче W1_M04/W1_D11 и их сохранённые артефакты. Полная индивидуальная постановка сохранена в `W2_03_EVIDENCE/PROMPT_W2_03.md`; содержательных изменений задачи не было. Новых сетевых загрузок не выполнял: независимое основание — повторное локальное декодирование уже полученных первичных байтов и визуальный просмотр наложенных рамок.

**Решение K003 — scope_narrowed, не closed.** Масштаб bbox теперь проверен по изображению: **1× native pixels для CAVIAR и BEHAVE**, а не предполагаемое удвоение BEHAVE. Candidate `decoded_index0 = global_frame − 35450` для BEHAVE и `decoded_index0 = XML_frame` для CAVIAR согласуются с видимыми людьми в нескольких точках. Но просмотр вариантов ±1 не позволяет выбрать единственный origin. Поэтому temporal headline metric и заявления о промышленной переносимости по-прежнему не разрешены этим результатом. Разумный статус — **готовый прозрачный sanity fixture с явной неопределённостью**, не lockbox/acceptance corpus. No model execution, no training, no LinQ/CPU/RTX inference or runtime measurement.

<a id="F291"></a>
### F291 — W2_03: Методы и воспроизводимость

Provenance: [W2_03:7](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Методы и воспроизводимость

<a id="F292"></a>
### F292 — W2_03: W2-03-F01 [local_test: decode/parsing/rendering; artifact_found].

Provenance: [W2_03:9](_WORK/W2_03.md); original aliases: W2-03-F01. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F01](RAW_FACTS.md#F292) [local_test: decode/parsing/rendering; artifact_found].** Python, PyAV **18.1.0**, Pillow **12.1.1**; OpenCV отсутствует. Скрипты `align.py`, `align_broad.py` последовательно декодируют все три видео без seek, сохраняют каждый original frame PTS, time_base, decoded ordinal, checksum и rate. По XML/XGTF рамки рисуются на фактических decoded images; положение рамки фиксировано по выбранной annotation frame, а изображение меняется для offsets −1,0,+1 и отдельно −5,0,+5. Для пространственного масштаба независимо сопоставлены 0.5×,1×,2×. Ни детектор, ни pose estimator, ни action classifier не использованы; качество модели не является критерием выбора mapping. `audit.py` дополнительно сравнил SHA256 каждого RGB24 decoded image с предшествующим и перечислил nonincreasing PTS. Это lightweight проверка существующих небольших файлов, не распознавание.

Сохранены 16 offset sheets (8 narrow и 8 broad), 3 scale sheets, три полных clock JSON, `manifest.json`, `duplicate_audit.json`, `mapping.json`, `phase_observability.json` и исполнимые локальные research scripts. Все overlay evidence остаются в приватной папке этой ветки; публичное размещение не выполнялось. На одном промежуточном запуске broad sheets заменили narrow filenames; исправлены имена и повторно созданы оба набора. Финальные `_offsets_` = ±1, `_broad_offsets_` = ±5, что явно написано внутри изображений.

| Локальный исходник | Bytes | Decoded / annotation frames | SHA256 media |
|---|---:|---|---|
| M04/caviarrun.mpg | 6,500,613 | 552 / XML551 (0–550) | b1eb7821318a2443445ee0c6dd6edb4dd9ebe06c110b52dce9252b9117931a55 |
| M04/caviarwalk.mpg | 7,208,095 | 612 / XML611 (0–610) | a5d6dc7d7def01c1bdaeea8ff620195c148b366e1a52589bf4e46f15b6daa0c2 |
| D11/35450-47160.avi | 16,867,976 | 11,711 / sparse XGTF1919 frame keys | 2b5e93b7f198a3b56b6ab94638880825a864a601e8cc762195375f48461e5d19 |

1919 — количество уникальных frame keys с хотя бы одной bbox после разворачивания dynamic spans; это не длительность и не число размеченных gait frames. Hash/bytes всех четырёх annotation payloads указаны в `mapping.json`. W1 HTTP access status относится к прежнему получению; нынешний статус — **local payload re-access/decode**, не повторный HTTP200.

<a id="F293"></a>
### F293 — W2_03: Непосредственные визуальные результаты

Provenance: [W2_03:21](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Непосредственные визуальные результаты

<a id="F294"></a>
### F294 — W2_03: W2-03-F02 [local_test: overlay inspection; inference: mapping ambiguity].

Provenance: [W2_03:23](_WORK/W2_03.md); original aliases: W2-03-F02. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F02](RAW_FACTS.md#F294) [local_test: overlay inspection; inference: mapping ambiguity].** CAVIAR размеры 384×288. XML `box` содержит центр `xc,yc` и размеры `w,h`; преобразование в top-left: x=xc−w/2, y=yc−h/2. Native scale=1 правильно помещает рамки actor6/7 на людях около frame410 и actor0 в Walk1/frame63. При 0.5 и2 рамки смещаются на фон/другие части сцены. Просмотрены начала, переходы и концы: RunAway 0,21,22,174,372,373,384,385,410,436,437,489,490,550; Walk1 0,17,39,63,100,101,236,444,475,610. Evidence: `caviarrun_offsets_0–2.jpg`, `caviarwalk_offsets_0–1.jpg`, соответствующие scale sheets, а broad варианты дополнительно просмотрены вокруг run переходов.

Идентичность рамки/человека в средней части разумно согласуется с XML. Однако ручная рамка и малое межкадровое перемещение не различают ±1 уверенно. Большие offsets ±5 визуально ухудшают размещение движущихся фигур около410/436, но не задают статистического confidence interval. У actor7 около конца running фигура мала; actor6 около489 уже у края/за бликующей конструкцией, его bbox в XML489 всего7×4 pixels (xc24,yc211), хотя movement interval доходит до489. Следовательно даже внутри dense movement interval не каждая строка означает полную видимость ног или доступный person crop. Переход к отсутствующему actor6 в490 нельзя трактовать как достоверное прекращение физического бега/нормализацию.

<a id="F295"></a>
### F295 — W2_03: W2-03-F03 [local_test: overlay inspection; contradiction: 2× scale hypothesis].

Provenance: [W2_03:27](_WORK/W2_03.md); original aliases: W2-03-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F03](RAW_FACTS.md#F295) [local_test: overlay inspection; contradiction: 2× scale hypothesis].** BEHAVE 640×480, XGTF bbox использует top-left x,y и width,height. Прямая native scale=1 согласуется с actor0 в белом, actor1 в тёмном и другими тремя фигурами около44425/46360. На `behave_scales.jpg` scale2 переносит рамки вниз к машинам, scale0.5 — вверх на траву. Этим отвергнута гипотеза, будто координаты разметки надо удваивать из320×240. Bounding boxes довольно свободны и перекрываются при сближении людей; точное начало физической фазы gait из них не извлекается.

Проверены global41829,41850,44381,44396,44400,44401,44425,44447,44448,46306,46334,46360,46375,46376,46600. Native mapping g−35450 показывает вход actor0 у левого края около41829 и группу на правильных местах в обоих run episodes. В offsets±5 около44425/44447 видна заметная пространственная несогласованность; ±1 остаются приемлемыми по точности ручных boxes. Это сильное подтверждение правильной области subclip, но не сертификат single-frame origin. Начало второго group0,1 run46306 происходит у самого левого края, где фигуры частично видимы и перекрываются; run row не обещает, что там видна походка каждого участника. Позже46360 видны пять фигур, но это не делает source group row actor-complete gait GT.

<a id="F296"></a>
### F296 — W2_03: Время и контракт mapping

Provenance: [W2_03:31](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Время и контракт mapping

<a id="F297"></a>
### F297 — W2_03: W2-03-F04 [local_test: full PTS audit; contradiction: duplicate-image repair].

Provenance: [W2_03:33](_WORK/W2_03.md); original aliases: W2-03-F04. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F04](RAW_FACTS.md#F297) [local_test: full PTS audit; contradiction: duplicate-image repair].** В CAVIAR **ни одной byte-identical adjacent RGB image** не обнаружено во всех552/612 decoded frames. Значит extra decoded frame нельзя без основания удалить как повтор. Timestamp anomalies не только ранние: RunAway nonincreasing PTS на decoded indices **2,3,125,176,359**, Walk1 — **38,598**. Это индексы i, для которых PTS[i]≤PTS[i−1]; все исходные значения сохранены. Никакого доказательства, что capture потерял именно столько кадров, нет. Повторённый PTS и одинаковое изображение — разные свойства.

RunAway первые PTS: 0,25174,25174,25174,28774 в time_base1/90000; Walk1:0,25174,28774,32373. Оба nominal rate25fps. RunAway последний decoded551 PTS1997974=22.199711s; Walk1 decoded611 PTS2221173=24.6797s. Повторяющийся timestamp при новых RGB изображениях делает PTS-only sampler/дедупликацию опасными: можно выбросить новые визуальные наблюдения. Не исправлял bytes и не объявлял decoder clock равным physical capture clock.

BEHAVE все11,711 PTS строго возрастают, равны **index0+1** в time_base1/25. Первый decoded frame имеет0.04s, последний468.44s. Relative source timeline можно вычислять `(PTS−first_PTS)/25`, он точно совпадает с index0/25 для этого acquired clip. XML FILE Information FRAMERATE1.0/NUMFRAMES77814 остаётся metadata полного исходного набора и не заменяет acquired25fps video clock.

<a id="F298"></a>
### F298 — W2_03: W2-03-F05 [local_test: arithmetic; hypothesis: canonical evaluation contract].

Provenance: [W2_03:39](_WORK/W2_03.md); original aliases: W2-03-F05. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F05](RAW_FACTS.md#F298) [local_test: arithmetic; hypothesis: canonical evaluation contract].** Сохранён отдельный canonical clock `t_eval=i/25` с нулём на первом decoded frame. Это **задокументированный synthetic evaluation clock**, не восстановленное физическое время. Для CAVIAR он нужен для одинаково определённого sanity replay; original PTS и decoded ordinal всегда остаются рядом. Разметка связывается с candidate ordinal через δ∈{−1,0,+1}, sensitivity runs обязаны включать все три. Само множество±1 — проверенные конкурирующие варианты, не доказанная абсолютная граница ошибки. Для CAVIAR разницу original PTS и i/25 нельзя компенсировать одним постоянным offset на всём файле: сохранённые repeats меняют разность.

| Episode, source literal | Candidate decoded inclusive | Canonical interval [start,end), s | Original PTS at inclusive endpoints, s |
|---|---|---|---|
| CAVIAR actor7 movement=running373–436 |373–436|14.92–17.48|15.079711–17.599700|
| CAVIAR actor6 movement=running385–489 |385–489|15.40–19.60|15.559711–19.719711|
| BEHAVE [1,2] RunTogether44396–44447 |8946–8997|357.84–359.92|357.88–359.92|
| BEHAVE [0,1] RunTogether46306–46375 |10856–10925|434.24–437.04|434.28–437.04|

Inclusive endpoint PTS во второй колонке времени не является exclusive end: таблица специально сохраняет обе разные конвенции. Exact per-offset PTS лежат в `mapping.json`. За frame-safe сборку event interval отвечает выбранный mapping/version, его нельзя прятать внутри loader.

<a id="F299"></a>
### F299 — W2_03: Что действительно размечено и наблюдаемо

Provenance: [W2_03:50](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Что действительно размечено и наблюдаемо

<a id="F300"></a>
### F300 — W2_03: W2-03-F06 [artifact_found; local_test: annotation read; inference].

Provenance: [W2_03:52](_WORK/W2_03.md); original aliases: W2-03-F06. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F06](RAW_FACTS.md#F300) [artifact_found; local_test: annotation read; inference].** CAVIAR annotation связывает movement с object id: actor7 walking149–372→running373–436→walking437–550; actor6 walking174–384→running385–489, далее нет гарантированной разметки ID. Это два actor intervals одной сцены/источника, не два независимых испытания и не все бегущие люди мира. Видимость ног/occlusion не размечены отдельным качественным флагом; добавить локально reviewed visible/partly_visible/unknown интервалы до per-actor gait acceptance. По snapshots нельзя выдумать полную dense visibility truth.

BEHAVE `markup.txt` задаёт группы, например [1,2]44396–44447; [1,2,4]44400–44447; [1,2,4,5]44401–44447. Второй episode [0,1]46306–46375, вместе с [2,4]46330–46375 и [2,4,5]46334–46375. Это вложенные/перекрывающиеся group statements, **не шесть независимых positive events и не dense gait labels всех five IDs**. Chase и RunTogether могут одновременно описывать один участок. Для table ниже выбраны два разных episode envelope по конкретной group row, без расширения её владельцев. Actor0, видимый в первом эпизоде, не становится автоматически участником running [1,2]. Безусловный join bbox→running каждому человеку из сцены запрещён. Unlabelled spans не считать walking negatives; Walk1 имеет настоящий source walking control, но не «fast walk».

<a id="F301"></a>
### F301 — W2_03: Phase/dropout observation opportunity, без модели

Provenance: [W2_03:56](_WORK/W2_03.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Phase/dropout observation opportunity, без модели

<a id="F302"></a>
### F302 — W2_03: W2-03-F07 [local_test: deterministic label arithmetic; hypothesis: synthetic losses].

Provenance: [W2_03:58](_WORK/W2_03.md); original aliases: W2-03-F07. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F07](RAW_FACTS.md#F302) [local_test: deterministic label arithmetic; hypothesis: synthetic losses].** `phase.py` перебирает25 стартовых фаз p=0..24 кадров на canonical25Hz clock. Sampling ticks p/25+k/r переводятся **causal ceil** в ближайший не более ранний source ordinal: `i=p+ceil(25k/r)`. Для2fps интервалы между samples чередуются12/13 кадров; это осознанный контракт, а не ошибочное every12=2.083fps. Все native frames также проходят тот же sweep; события начинаются позже первых25frames, поэтому край первого sample их не цензурирует.

Random condition: независимый Bernoulli drop20% каждого исходного frame, seeds0..99 Python random; одинаковая seed-mask для всех rate/phase одного source length. Таблица показывает observed min–max по фазам и этим100 seeds, **не аналитические confidence intervals** и не гарантии будущего loss. Burst condition: один непрерывный25frame/1s outage, его начало перебирается по каждому source frame внутри соответствующего event; конец может выходить за event. Это другой тест, без одновременного random drop. Ни burst, ни20% не взяты из требований организатора, это явно synthetic sensitivity conditions.

Число samples означает лишь количество annotation-time opportunities. Оно не учитывает, видны ли ноги, не говорит о достаточности окна, корректности crop, recognition accuracy/recall, inference latency или notification SLA. Приδ=±1 phase extrema без drops сохраняют смысл, но random-mask-specific значения могут измениться; сохранённая таблица conditional δ=0.


| Source interval | FPS | Samples, phase min–max | Random20%, min–max | Burst1s, min–max |
|---|---:|---:|---:|---:|
| CAVIAR actor7 | 25 | 64–64 | 43–61 | 39–63 |
| CAVIAR actor7 | 1 | 2–3 | 0–3 | 1–3 |
| CAVIAR actor7 | 2 | 5–6 | 1–6 | 3–6 |
| CAVIAR actor7 | 5 | 12–13 | 5–13 | 7–13 |
| CAVIAR actor6 | 25 | 105–105 | 73–96 | 80–104 |
| CAVIAR actor6 | 1 | 4–5 | 0–5 | 3–5 |
| CAVIAR actor6 | 2 | 8–9 | 2–9 | 6–9 |
| CAVIAR actor6 | 5 | 21–21 | 11–21 | 16–21 |
| BEHAVE group1,2 | 25 | 52–52 | 33–47 | 27–51 |
| BEHAVE group1,2 | 1 | 2–3 | 0–3 | 1–3 |
| BEHAVE group1,2 | 2 | 4–5 | 0–5 | 2–5 |
| BEHAVE group1,2 | 5 | 10–11 | 4–11 | 5–11 |
| BEHAVE group0,1 | 25 | 70–70 | 46–65 | 45–69 |
| BEHAVE group0,1 | 1 | 2–3 | 0–3 | 1–3 |
| BEHAVE group0,1 | 2 | 5–6 | 0–6 | 3–6 |
| BEHAVE group0,1 | 5 | 14–14 | 6–14 | 9–14 |
| Walk1 actor1 control | 25 | 276–276 | 208–236 | 251–275 |
| Walk1 actor1 control | 1 | 11–12 | 3–12 | 10–11 |
| Walk1 actor1 control | 2 | 22–23 | 10–23 | 20–22 |
| Walk1 actor1 control | 5 | 55–56 | 35–52 | 50–55 |

Без drops first opportunity delay ranges: native0s;1fps0–0.96s;2fps0–0.48s;5fps0–0.16s. Это **sampling opportunity delay**, не задержка распознавания/оповещения. При1fps random-mask test способен оставить0 observations даже для этих2–4s intervals; это демонстрация потери возможности увидеть эпизод в конкретных синтетических условиях, не оценка модели. Контроль Walk1 также теряет временную структуру; большее количество still frames не доказывает gait separation.

<a id="F303"></a>
### F303 — W2_03: Sources, rights and remaining decision gates

Provenance: [W2_03:90](_WORK/W2_03.md); original aliases: section record. Sources: [S090](SOURCES.md#S090), [S091](SOURCES.md#S091), [S092](SOURCES.md#S092), [S093](SOURCES.md#S093), [S094](SOURCES.md#S094), [S264](SOURCES.md#S264), [S265](SOURCES.md#S265), [S266](SOURCES.md#S266), [S267](SOURCES.md#S267).

## Sources, rights and remaining decision gates

| ID | Primary identity / exact URL / locator | This wave observation |
|---|---|---|
| [W2-03-S01](SOURCES.md#W2-03-S01) | Robert B. Fisher/CAVIAR team, CAVIAR Test Case Scenarios, INRIA recordings2003; https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/ ; exact Fight_RunAway1 pair https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/Fight_RunAway1.mpg and https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/fra1gt.xml | Locally acquired media rehashed, fully decoded; XML parsed. No new HTTP request. Byte-pinned hashes in manifest/mapping. |
| [W2-03-S02](SOURCES.md#W2-03-S02) | Same authors/project; Walk1 https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/Walk1.mpg and https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/wk1gt.xml | Independent overlay observations of original saved payloads, no new network claim. |
| [W2-03-S03](SOURCES.md#W2-03-S03) | Edinburgh Vision Group/BEHAVE; Aroosha Laghaee2007 page, Blunsden/Fisher2010 citation; https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/index.html ; video https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160.avi | Fully decoded11,711frames; source byte identity and original clock audited locally. Publication date of exact AVI unknown. |
| [W2-03-S04](SOURCES.md#W2-03-S04) | Same BEHAVE source; https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160F.xgtf and https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/markup.txt ; XGTF sourcefile workstation filename, FILE Information, person/bbox spans; markup relevant group rows102–104,111,114,116 | Exact downloaded payload rehash/parsing, native bbox scale independently checked by images. Source revision not versioned; use saved hashes. |

<a id="F304"></a>
### F304 — W2_03: W2-03-F08 [primary_docs inherited with exact saved artifacts; unknown: broader grants].

Provenance: [W2_03:99](_WORK/W2_03.md); original aliases: W2-03-F08. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-03-F08](RAW_FACTS.md#F304) [primary_docs inherited with exact saved artifacts; unknown: broader grants].** Rights remain separate by layer. CAVIAR saved primary page/W1-M04 states CC BY-SA with attribution to CAVIAR/IST200137540; version and complete linked grant not resolved in this wave. Do not remove this positive grant merely because version is unclear. BEHAVE saved primary page says researchers can freely use and requests citation; neither an explicit standardized commercial deployment license nor public-demo redistribution grant was established. Exact media+annotation downloaded publicly are not automatically consent for unrestricted product distribution. These are older Edinburgh interaction BEHAVE data, not the unrelated2022 body/object BEHAVE license. Source media and annotation grants need to be carried with derivatives/overlay publication; overlays here are private research evidence. Local research utility code is newly authored, but this conveys no source-media rights. No model code/weights acquired in this wave; their licenses are **not evaluated**, and no dataset grant clears weights. Rights and organizer-policy confirmation remain owner-dependent before externally distributing examples; no outreach/terms acceptance done.

**K003 outcomes by component:**

| Component | Outcome | Exact basis / residual |
|---|---|---|
| Native spatial scale | closed for these saved frames/files | Both sources native1× fits people;0.5/2 fail visibly. Does not certify every annotation box. |
| Correct subclip/global region | scope_narrowed | BEHAVE g−35450 aligns onset/middle/end groups; XML full-source1fps rejected for acquired video timing. |
| Exact one-frame origin | still_open |±1 remain visually ambiguous under manual bboxes; file-count mismatch not explained by adjacent identical decoded images. Needs original frame images/frame-number burn-in or source conversion documentation/annotation re-review. |
| PTS and evaluation clock preservation | closed as audit/documentation, not physical-clock recovery | Every original PTS retained; extra repeats beyond start found. Canonical i/25 explicitly synthetic for CAVIAR; no byte rewrite. |
| Per-actor group-run completeness | still_open | Group rows not dense individual gait/visibility truth. Need independent per-person action and visibility review for target metrics. |
| FPS/drop opportunity | closed as arithmetic fixture |Full phase enumeration plus specified losses; no inference, no recognition accuracy. |
| Headline event metric / industrial generalization | still_open | No target factory corpus, visibility-reviewed truth, device execution or measured recognition. Preserve reserve/sanity status. |

Practical first action for engineering: load `mapping.json` together with source SHA and both clocks; do not sort/drop frames solely by PTS and do not double BEHAVE coordinates. Keep all crops/episodes from each continuous source in one provenance group; both CAVIAR files share scene/actors/background risk, BEHAVE repeated scene/session risk. If source-level gait acceptance is needed, review visibility and physical action boundaries on decoded clips before labeling crops, retaining original labels as a distinct layer. Actor6's7×4 last bbox is a concrete abstention/visibility stress case, not a clean completed run offset. Run canonical sensitivity replay forδ−1/0/+1; if outcome changes, report mapping-dependent result rather than selecting the favorable origin. No third search wave needed to recognize this remaining gap.

This work proves neither factory fast walking nor calibrated acceleration/proximity, neither1fps sufficiency nor scene-disjoint generalization, neither runtime nor LinQ compatibility. The usable advance is a reproducible media/annotation/clock package and a narrowed uncertainty, not a model score.

<a id="F305"></a>
### F305 — W2_04: W2_04 — K004: точные AVA media failures и полный bounded Charades review

Provenance: [W2_04:1](_WORK/W2_04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_04 — K004: точные AVA media failures и полный bounded Charades review

Дата: 2026-10-23, direct HTTP 20:21:23–20:21:27 UTC; автор W2_04, вторая/последняя волна. **Решение: K004 scope_narrowed; scenario phone остаётся reserve.** Для двух конкретных AVA same-person runs текущий официальный YouTube route сообщает unavailable; первый явно удалён по copyright request. Имеющийся Charades2RFLZ полностью просмотрен по 222 исходным кадрам: один непрерывно видимый после входа человек подходит к столу, подносит устройство/руку к уху, затем опускает предмет; убедительного walking одновременно с ear-use в данном клипе не установлено. Это домашний staged donor с broad clip/interval labels, не industrial event test pack.

<a id="F306"></a>
### F306 — W2_04: Задание, уже известное и независимый вопрос

Provenance: [W2_04:5](_WORK/W2_04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Задание, уже известное и независимый вопрос

Полный frozen prompt сохранён в [assignment.md](_WORK/W2_04_EVIDENCE/assignment.md). Содержательных изменений scope не было: после локализованного AVA failure выполнен предписанный fallback. Прочитаны K004 в CRITIC.md, W1_M05 join/media notes и W1_D12 report/media/license/CSV, CASE_NOTES.md и SYNTHESIS_CONTRACT.md. Original briefs задают research без модельных прогонов; root наблюдение кейса сохраняет **телефон при работе с оборудованием ИЛИ перемещении по цеху**, а не только stationary equipment work.

W1 уже установила 77 sparse co-label person/timestamp samples и 27 consecutive runs; пересчёт этих чисел не делался. Новые вопросы: что выдаёт официальный player **для exact IDs**, и что на самом деле видно на **всём** доступном коротком Charades donor с исходным временем? Здесь не склеиваются UPT pair weights, AVA person IDs и Charades temporal spans в одну проверенную модельную цепочку.

<a id="F307"></a>
### F307 — W2_04: W2-04-F001 [artifact_access_checked, local_test] — exact AVA localized failure

Provenance: [W2_04:11](_WORK/W2_04.md); original aliases: W2-04-F001. Sources: [S111](SOURCES.md#S111), [S411](SOURCES.md#S411), [S412](SOURCES.md#S412).

## [W2-04-F001](RAW_FACTS.md#F307) [artifact_access_checked, local_test] — exact AVA localized failure

[[W2-04-S001](SOURCES.md#W2-04-S001),S002,S003]. Выбраны исходно предложенные cases:

| Source/video/person | Source seconds | Annotation meaning | Current official media observation |
|---|---:|---|---|
| QTmwhrVal1g / 91 | 1181–1190 inclusive | saved AVA actions14 walk +15 answer phone; normalized person boxes at each sampled second | watch HTML200, player ERROR; interstitial says copyright removal on request by Reliance Entertainment |
| WSPvfxtqisg / 1 | 908–915 inclusive | saved AVA actions14 walk +15 answer phone | watch HTML200, player ERROR; generic unavailable |

`exact_ava_cases.json` contains only selected existing rows/boxes, with explicit W1 provenance, not a new annotation parse. The endpoint fetched was `https://www.youtube.com/watch?v=QTmwhrVal1g` and same route for WSPvfxtqisg. Independent ordinary requests with verified default TLS returned HTML200 (864128 and863927 bytes); regex located `ytInitialPlayerResponse`, JSON parser successfully parsed it, both `videoDetails=null`, no streamingData keys. Exact nested descriptions are preserved in player_1.json/player_2.json. QT description in Russian explicitly identifies removal for copyright violation following Reliance Entertainment request; WSP description merely repeats unavailable and does not state a cause. These are **player access responses**, not statements independently validating the underlying copyright claim.

Web open separately reported online-fetch throttling for both URLs; that web-tool failure alone did not establish content availability. The direct player response narrows the reason far more strongly for QT. No extractor, stream URL deciphering, download, proxy, mirror, replacement upload, login, agreement acceptance or anti-bot bypass was attempted. No AVA video frames/PTS/hash or box overlays can be truthfully supplied. HTTP200 here is not media availability. This localized result does not prove all AVA videos unavailable or that rights-holder-authorized copies cannot exist.

Official AVA page newly fetched HTTP200/32234B, hash `ab3fd75c77ac6a61137665ec48c7c8dc0354009625888b208de0bf14a6520df9`. Current page supplies annotation archives, not a direct MP4 for these cases. It defines source seconds from YouTube start, normalized x1/y1/x2/y2, person IDs linking adjacent frames within that video. Consecutive sparse person IDs still do not demonstrate continuous shot continuity/use or phone visibility. We did not turn IDs into global subjects or interpolate all seconds as dense GT.

<a id="F308"></a>
### F308 — W2_04: W2-04-F002 [local_test] — Charades source clock and bounded full inspection

Provenance: [W2_04:26](_WORK/W2_04.md); original aliases: W2-04-F002. Sources: [S281](SOURCES.md#S281), [S283](SOURCES.md#S283).

## [W2-04-F002](RAW_FACTS.md#F308) [local_test] — Charades source clock and bounded full inspection

[[W2-04-S004](SOURCES.md#W2-04-S004),S005]. Used existing `_WORK/W1_D12/charades_2RFLZ.mp4`, no second media retrieval. Its bytes765584 and SHA256 **77cb4611d404ed5a2aac77e24c374091f5eef452779c5763b8c5a38666fd28c6** match W1. PyAV decoded every video frame, no decode error. Exact stream contract: width480,height270; time_base1/15029; average_rate15029/1000; start_time0; stream duration222000ticks=14.7714418790s; 222 frames, indices0…221, PTS0…221000, all deltas1000ticks (0.0665380265s), strictly increasing. Last presented frame source time14.7049038526s. Container end duration is not an extra observed frame. CSV length14.71 differs from stream duration and was retained separately.

Created and **visually inspected all four all_frames_000/056/112/168.jpg sheets**, covering every frame in order with source PTS. Separately inspected native_review.jpg with eight 480×270 original-resolution frames around entry/reach/ear/return. This is complete bounded visual inventory, not playback at native speed, independent multi-rater GT, speech verification, or model inference. All-frame sheets resize to240×135; native panels resolve selected hand/device poses better but do not create detail beyond480×270. Bright backlit window, compression, body/hand occlusion and chair/table clutter limit object discrimination. No shot cut or second visible actor was observed; no audio track was evaluated.

| Frames/source PTS approx | Actual visible preliminary observation | What remains unknown |
|---|---|---|
| 0–34 /0–2.262s | Room/study, table and chair, no clearly visible person | Off-camera activity; empty scene is not negative human exposure |
| 35–55 /2.329–3.660s | Person enters from right and steps left toward table; reaches desk area | Device not securely distinguishable during entrance; cannot label walking+use positive |
| 56–73 /3.726–4.857s | Same visible person leans/reaches at tabletop | Exact phone contact/pickup boundary and device bbox absent |
| 74–77 /4.924–5.123s | Hand/device raised toward face/ear | Subframe onset; phone versus similar object from pixels alone |
| 78–123 /5.190–8.184s | Ear-side hand/device pose; person remains beside table, limited torso/head shifts | Spoken conversation unknown; lower legs partly obstructed; no convincing locomotion during ear-use |
| 124–142 /8.251–9.448s | Hand/device lowered and held out in front; gaze/attention seems directed toward hand area | Not certified texting, screen-reading or camera use; hand pose alone insufficient |
| 143–183 /9.515–12.177s | Person leans/reaches at table, hands near objects | Exact release/put-down/cord contact cannot be densely certified |
| 184–221 /12.243–14.705s | Person straightens beside table and shifts posture/body toward right near end | Exit/clear/rearm not fully observed; no phone-use walking episode established |

These are broad observer partitions, not frame-exact source action GT. Source script/descriptions mention desk telephone and cord, and visual reach→ear→return is compatible with that **stationary desk-phone interpretation**. It is not evidence for mobile handset texting while walking across an industrial floor. Ear pose does provide a useful nuisance example for generic hand-to-face detectors; beyond this one scene, unobserved phone/radio/scanner confusers remain unknown. No physical phone dimensions or universal min-pixel threshold is derived.

<a id="F309"></a>
### F309 — W2_04: W2-04-F003 [artifact_found, local_test, inference] — original labels do not follow dense visible onset

Provenance: [W2_04:45](_WORK/W2_04.md); original aliases: W2-04-F003. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-04-F003](RAW_FACTS.md#F309) [artifact_found, local_test, inference] — original labels do not follow dense visible onset

Saved original CSV row in charades_original_row.json: id2RFLZ,subjectENHU,sceneHome Office/Study, length14.71; actions `c009 7.70 13.00;c019 3.00 10.40;c017 8.00 12.60;c015 2.30 12.40;c018 2.40 6.90`. Source c019 talking on phone/camera3.0–10.4 spans approach/reach and return as well as visible ear pose; the all-frame review prevents pretending its endpoints are dense action-onset truth. Other intervals overlap; hold/take/put are not automatic vetoes for use. Class c009 is Putting something on a table, not an independent walk label; this donor has no source walking action interval.

Actual schema is `id,subject,scene,quality,relevance,verified,script,objects,descriptions,actions,length`; actions are clip-owned class/start/end triples. **No source person box, phone box, actor-per-action ID, track, pair relation or visibility flags.** One visible actor across the reviewed take supports preliminary visual same-actor association for this clip only. It does not supply a missing authoritative actor annotation. No bbox overlay was invented. native_review.jpg overlays original c019 interval and explicit missing-box notice in a separate white caption band; it is not a detector/GT-box output. AVA overlays cannot be generated without decoded media.

Use `source_id=Charades/2RFLZ`, original hash,subjectENHU and source group together. Mark this reviewed clip development/example, never fresh lockbox. To build an event benchmark, authorized dense annotation must separately record actor, object identity/visibility, ear/carry/look/use, walking overlap, onset uncertainty/censoring and policy context. Preserve native PTS for cadence/dropped-frame tests; do not relabel frame indices as30fps. Single short staged scene has no credible camera-hours denominator.

<a id="F310"></a>
### F310 — W2_04: W2-04-F004 [primary_docs, inference, unknown] — rights and practical gates

Provenance: [W2_04:53](_WORK/W2_04.md); original aliases: W2-04-F004. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-04-F004](RAW_FACTS.md#F310) [primary_docs, inference, unknown] — rights and practical gates

Current Google AVA download page explicitly offers listed datasets under CC BY4.0. This supports annotation reuse with attribution; it does not undo the **observed removal of source YouTube media** or prove rights to fetch another copyrighted copy. Source video copyright/platform access, annotations, implementation code and trained weights remain separate. Exact first-route removal ends this attempt; do not rescue with copyright-bypassing mirrors.

Charades archive license from AllenAI2016 covers source/models/data as defined there; general academic/nonprofit/government research and evaluation elsewhere permitted, for-profit use/derivation not granted, modified public data release and third-party distribution not granted. Limited academic-publication examples are separately described. Thus this private bounded research review is within stated evaluation scope, but **this MP4/contact sheets are not automatically cleared for public hackathon/demo redistribution**. No new agreement was accepted on behalf of team, no outreach made. Exact intended competition/deployment permissions remain separate. No code/checkpoint selected or executed here, so no inference about their licenses or LinQ compatibility follows.

Practical scenario gate stays reserve until (a) authorized target camera video includes phone visibly associated with same moving/working actor, (b) radio/scanner/allowed terminal/tool/PPE adjustment and carry controls, (c) dense event/actor/visibility GT with grouped source splits, (d) chosen model actually runs on CPU/RTX with causal event evaluation, then (e) issued SDK/device and accepted host boundary enable actual LinQ execution. UPT is HOI evidence only; Charades is temporal donor only; AVA samples are sparse actor-action labels only. Future-window dependence of the candidate AVA model is not cured by annotation inspection.

P-DESTRE733MB-class member was **not retrieved**, and no P-DESTRE bbox overlay/h-w resolution claimed. Its known phone rows ID=-1 must never become one shared person track. Other search cases were not expanded once the assigned two exact cases yielded a precise result; no unrelated online video substituted.

<a id="F311"></a>
### F311 — W2_04: K004 outcome and handoff

Provenance: [W2_04:63](_WORK/W2_04.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## K004 outcome and handoff

**K004 = scope_narrowed, not closed.** The two selected official media routes now have concrete player failure payloads (first copyright removal, second unspecified unavailable); decoded Charades donor now has complete bounded frame review/clock with one visible actor but **no established concurrent phone-use+walking** and no source actor/phone localization. The previous uncertainty “not fetched” becomes a localized official-route failure for these cases. The actual industrial phone event, hard negatives, rights, model quality and device gates remain open; this is not a disproven existence claim for the whole dataset. No third wave required to preserve that conclusion.

<a id="F312"></a>
### F312 — W2_05: W2_05 — K005: real moving-machine donor and exact forklift detector

Provenance: [W2_05:1](_WORK/W2_05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_05 — K005: real moving-machine donor and exact forklift detector

Access/actions: **2026-10-23, approximately 20:18–20:25 UTC / 23:18–23:25 Moscow**. Exclusive evidence directory: [W2_05_EVIDENCE](_WORK/W2_05_EVIDENCE/). Full assigned prompt copied there unchanged; no substantive task expansion. Read K005, W1 D13, M06 and the relevant D09 machine-donor passage, CASE_NOTES and SYNTHESIS_CONTRACT; original briefs consulted. Independent work is the fresh release/terms check, one complete individual real MP4 download/decode and sampled timeline review, plus exact detector static binary validation. No inference, training, paid resources, LinQ execution, outreach or subagents.

**Decision:** K005 is **scope_narrowed**, with the release-description contradiction still open. A real fixed-camera warehouse recording demonstrably contains separate workers and a moving driven forklift/reach-truck. Therefore “only synthetic machines” or “no confirmed real pedestrian–machine footage” is no longer accurate. It remains a **supplementary routine-footage reserve**, not a ready near-miss testpack: no released real pair/event labels, no independently surveyed safety envelope, unresolved external training/derivative-use interpretation, and no verified target-domain full control set. Do not turn this content review into challenge-test training or manual participation labels.

<a id="F313"></a>
### F313 — W2_05: W2-05-S01 / primary_docs — current versus pinned SmartSpaces release

Provenance: [W2_05:7](_WORK/W2_05.md); original aliases: section record. Sources: [S311](SOURCES.md#S311), [S312](SOURCES.md#S312).

## [W2-05-S01](SOURCES.md#W2-05-S01) / primary_docs — current versus pinned SmartSpaces release

Publisher NVIDIA, *Physical AI Smart Spaces Dataset*. API https://huggingface.co/api/datasets/nvidia/PhysicalAI-SmartSpaces returned200 and current revision **2cbe9563cbe9f47f846e5c871ee994572bbbc60e**, identical to W1. Immutable README https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/blob/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/README.md ; raw path replacing `blob` with `resolve`. Complete raw response200,15579B, SHA256 `cdba2b672c8ac8deed29f9b26ea1bf2df52f91898d73bc7f59cd6c7b542150ab`.

<a id="F314"></a>
### F314 — W2_05: W2-05-F01 / primary_docs + artifact_access_checked:

Provenance: [W2_05:11](_WORK/W2_05.md); original aliases: W2-05-F01. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-05-F01](RAW_FACTS.md#F314) / primary_docs + artifact_access_checked:** The scene-table note, quantification footnote and June4,2026 changelog explicitly release the two real test captures as first60s video+calibration, while withholding GT/depth. July27 adds Croissant and reprojection reports. Current README shows no later correction. The fresh API still has only calibration, reprojection report and four/seven videos under Warehouse026/027; W1's absent released-real-GT finding remains valid for this checked revision. It does not prove that author-held labels do not exist. Saved `current_api.json`, `README.md`, `access.json`; all exact URLs/statuses/hashes in the log.

<a id="F315"></a>
### F315 — W2_05: W2-05-F02 / contradiction + unknown:

Provenance: [W2_05:13](_WORK/W2_05.md); original aliases: W2-05-F02. Sources: [S314](SOURCES.md#S314), [S319](SOURCES.md#S319).

**[W2-05-F02](RAW_FACTS.md#F315) / contradiction + unknown:** Fresh raw Croissant200,13588B, SHA256 `fe6adeebeb7dd4832b94a879a62f5ae7be96b8b0590e9d9e99cbced6169abbdb`; exact https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/croissant.json . `rai:personalSensitiveInformation` and `rai:dataSocialImpact` retain a hidden real target/evaluator-only/no-raw-public-distribution position and exclusion from training. This conflicts with that same revision's explicit real-video release and successful complete download. W1 paper Wang et al., *Physical AI Smart Spaces*, arXiv2610.02580v1, concluding privacy/limitations text also retains withheld-target language: https://arxiv.org/html/2610.02580v1 . Nothing inspected establishes whether “target” means a distinct unreleased source remainder or stale text about these exact clips. Both explanations remain hypotheses. Do not silently choose either.

<a id="F316"></a>
### F316 — W2_05: W2-05-S02 / primary_docs — precise challenge scope and rights layers

Provenance: [W2_05:15](_WORK/W2_05.md); original aliases: section record. Sources: [S320](SOURCES.md#S320), [S321](SOURCES.md#S321).

## [W2-05-S02](SOURCES.md#W2-05-S02) / primary_docs — precise challenge scope and rights layers

Official https://www.aicitychallenge.org/2026-faqs/ GeneralQ9 and https://www.aicitychallenge.org/2026-track1/ were independently opened through web extraction. `official_web_notes.md` records paraphrases/locators; it is not a complete HTML snapshot. W1 local403 bodies remain failed direct-access evidence only.

<a id="F317"></a>
### F317 — W2_05: W2-05-F03 / primary_docs + inference:

Provenance: [W2_05:19](_WORK/W2_05.md); original aliases: W2-05-F03. Sources: [S414](SOURCES.md#S414).

**[W2-05-F03](RAW_FACTS.md#F317) / primary_docs + inference:** GeneralQ9 prohibits additional manual test annotations in challenge use, discourages training on test data, permits automatic pseudo labels with tie-break qualifications, and requires award verification reproducibility from train/val/synthetic data. This is a competition protocol, not proof of a universal external-use copyright ban. Track1 expressly identifies CC BY4.0 as the download license. The repository card and Croissant both carry CC BY4.0 metadata. License terms support copying/adapting with attribution/license/change notices; separate publicity/privacy rights are not automatically cleared: https://creativecommons.org/licenses/by/4.0/ . The positive grant must be retained in synthesis.

For this bounded private read/review, I relied on explicit real release + positive dataset license + official download statement. I did not claim unrestricted training/relabeling permission. No challenge submission or manual dense test annotation was created, and no source media was externally published. The report's coarse inventory is preliminary source appraisal, not challenge GT. The unresolved external question is narrowly: **does NVIDIA's CC BY grant cover these exact released real MP4s for independent industrial research, derivative temporal/event annotations, model tuning, and downstream identifiable-media redistribution, or does the Croissant exclusion refer to them?** That question cannot be settled by relabeling a challenge FAQ as a universal license. No author was contacted.

| Layer | Established status | Remaining limit |
|---|---|---|
| SmartSpaces source media | Explicit real release, anonymous access, dataset CC BY4.0 metadata and Track1 download statement | Contradictory real-target privacy/training text; derivative-use/redistribution interpretation unresolved |
| Real annotations | Withheld in card; none under checked scene tree | No real track/pair/event GT delivered |
| Calibration | Public actual JSON and reprojection reports previously checked | No independent surveyed floor/safety-envelope accuracy; report units not certified metres |
| Dataset utility code | Separate linked evaluator exists | Its code license does not clear footage/weights |
| Detector catalogue code | Publisher repository MIT | Does not independently prove every external weight/runtime/media layer MIT |
| Detector training images | Named HF mirror and original Roboflow v1 say CC BY4.0 | Image dataset, no temporal source grouping or event truth established here |
| Exact detector weights | Downloaded, hashed, static names/args inspected | HF model card has no explicit license field; publisher project MIT is positive scope evidence but artifact-specific weight grant remains less explicit |

<a id="F318"></a>
### F318 — W2_05: W2-05-S03 / artifact_access_checked + local_test — one complete real MP4

Provenance: [W2_05:33](_WORK/W2_05.md); original aliases: section record. Sources: [S316](SOURCES.md#S316).

## [W2-05-S03](SOURCES.md#W2-05-S03) / artifact_access_checked + local_test — one complete real MP4

Exact immutable asset: https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_026/videos/Camera_0000.mp4 . Full anonymous GET200, **19,802,011B**, SHA256 **83ed232a2f5fe3031807ed19020e1a44fe386e89b68f9bea621797f1552c9cda**. This exceeds W1 byte-prefix checking and confirms complete individual file accessibility; no archive/depth package fetched.

<a id="F319"></a>
### F319 — W2_05: W2-05-F04 / local_test:

Provenance: [W2_05:37](_WORK/W2_05.md); original aliases: W2-05-F04. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-05-F04](RAW_FACTS.md#F319) / local_test:** PyAV decoded all **1800** frames without raised error, H264,1920×1080,30fps. Stream timebase1/15360, duration921600 ticks=60s; first PTS0; last PTS921088=59.9666667s. All adjacent PTS increase by512. Saved actual `frame_pts.csv` (one row per decoded frame), `decode.json`, reproducible `decode.py`; source PTS preserved, no synthetic timestamps generated. No OpenCV installed; existing PyAV/Pillow used without installation. This is a media integrity/timing test, not model execution or accuracy measurement.

<a id="F320"></a>
### F320 — W2_05: W2-05-F05 / local_test + preliminary observed inventory:

Provenance: [W2_05:39](_WORK/W2_05.md); original aliases: W2-05-F05. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-05-F05](RAW_FACTS.md#F320) / local_test + preliminary observed inventory:** Reviewed six contact sheets spanning **every second0–59** at native PTS, then45 cropped detail frames at5fps from33.0–41.8s, all saved. All source frames were decoded, but visual review was **sampled across the complete timeline**, not a native30fps continuous human watch and not frame-accurate event annotation. Coarse boundaries below are descriptive observation windows, not ground truth onset/offset. No second camera was needed to establish separate worker/machine/operator content; its addition would be another synchronized view of this same physical minute, never another event or independent exposure minute.

| Coarse source-time window | Actually visible content | What it supports / does not support |
|---|---|---|
| 0–~10s | Three separate standing/walking workers near foreground pallet/rack: yellow hardhat/vest worker, white-shirt worker, blue/grey-shirt worker; distant red/black forked machine in aisle with blue projected spot | Real pedestrians separate from machine. Machine appears stationary in sampled early views; not a near stationary-machine control with known distance |
| ~10–~29s | Vest worker repeatedly bends and handles boxes on pallet; white-shirt worker stands/walks/gestures, later exits toward left; blue/grey worker becomes hidden by left racks | Real pose/handling/partial-occlusion distractors. Box handling is not a carrying-rule violation; absence behind rack is unknown visibility |
| ~30–~33s | Foreground vest worker continues box handling; distant machine still aligned in aisle | Apparent pre-motion baseline only; no validated stationary threshold/footpoint distance |
| ~34–~38s | Red forklift/reach-truck advances toward camera, forks pointing forward and low; blue projected light advances on floor; vest worker remains beside pallet | Direct visible machine motion with an independent worker in same aisle view; no certified near-miss, speed, contact, metre distance or collision course |
| ~38–~40.6s | Vest worker lifts/carries box and walks left toward rack/cross-aisle while truck continues advancing; worker becomes partly hidden, then exits left | Potential relative-path/occlusion stress sample. Cannot infer yielding causation, hazardous threshold or safety procedure from temporal order |
| ~41–~47s | Truck proceeds through foreground; operator visible inside/at operator station, especially44–46s; free worker no longer visibly in immediate aisle | Driver-like ownership control, movement/scale change, image truncation. Not permission to suppress all people near trucks; ownership transition and other cameras unreviewed |
| ~48–59s | Near truck leaves lower image; blue light and a distant dark upright machine-like object remain; no clearly visible free pedestrian in foreground aisle | Eligible-empty status and every object identity not exhaustively certified; edge exit is not machine stopped or event cleared |

Observed minimum: three distinguishable free workers and one driven forklift/reach-truck. A distant dark object at far end after foreground passage is machine-like but not assigned a certified class/identity; it may be separate equipment, and the review does not resolve that. Do not inflate object counts with uncertain silhouettes. Early operator visibility is poor because of range/mast; later operator visibility corroborates driver-like status, not an annotated driver ID.

<a id="F321"></a>
### F321 — W2_05: W2-05-F06 / inference:

Provenance: [W2_05:53](_WORK/W2_05.md); original aliases: W2-05-F06. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

**[W2-05-F06](RAW_FACTS.md#F321) / inference:** This supplies real moving-machine + pedestrian co-presence, apparent stationary/far-machine context, driver-like context, occlusion and perspective/scale changes in a single episode. It does **not** independently establish stationary-near, metrically moving-far, reverse/turn, barrier-separated overlap, safety-envelope breach, collision/near-miss or source-time positive event truth. No full event/control dataset is claimed. A blue spot is a visible warning-light distractor, not distance calibration or event label. Existing D13 calibration remains a geometry donor; Track1 submission units in metres do not establish independently measured real safety distance accuracy.

<a id="F322"></a>
### F322 — W2_05: W2-05-S04 / primary_docs + artifact_found — exact detector chain

Provenance: [W2_05:55](_WORK/W2_05.md); original aliases: section record. Sources: [S415](SOURCES.md#S415), [S416](SOURCES.md#S416).

## [W2-05-S04](SOURCES.md#W2-05-S04) / primary_docs + artifact_found — exact detector chain

Primary publisher repository Kerem Berke, *Awesome YOLOv8 Models*, pinned https://github.com/keremberke/awesome-yolov8-models/tree/fb4b7895a92913023ef222fdf0957b8ce2015766 ; README includes forklift model family row and MIT project statement, LICENSE saved. Exact HF author repository https://huggingface.co/keremberke/yolov8n-forklift-detection/tree/d8b594f321dd4c64eda16e435601fd266089fc32 ; API confirms public/non-gated revision, lastModified2023-02-22. Saved README/config/API. Its `inference:false` metadata is not a claim that the binary cannot run; no execution was attempted here.

<a id="F323"></a>
### F323 — W2_05: W2-05-F07 / artifact_access_checked + local_test:

Provenance: [W2_05:59](_WORK/W2_05.md); original aliases: W2-05-F07. Sources: [S417](SOURCES.md#S417).

**[W2-05-F07](RAW_FACTS.md#F323) / artifact_access_checked + local_test:** Exact primary weight https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt first returned206 for1024B with total6,216,376, then full GET200 **6,216,376B**, SHA256 **0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38**. It is a ZIP PyTorch checkpoint. Only `zipfile` and `pickletools.genops/dis` were used on its `best/data.pkl`: **no `pickle.load`, `torch.load`, module import from artifact, model construction or inference**. The static pickle opcode sequence at positions77445–77505 explicitly forms `names={0:'forklift',1:'person'}`. This directly corroborates the card's ordered labels, not just a secondary catalogue. Saved `checkpoint_static.json`, `checkpoint_pickle_dis.txt` and original weight.

Class mapping differs from AI City Track1 (**Person0/Forklift1**): never pass detector numeric classes into that schema unconverted. A two-class detector cannot automatically detect all mobile-mechanism types (pallet truck, robot, loaded forks) or identify driver relationships.

<a id="F324"></a>
### F324 — W2_05: W2-05-F08 / primary_docs + local_test + author_claim:

Provenance: [W2_05:63](_WORK/W2_05.md); original aliases: W2-05-F08. Sources: [S418](SOURCES.md#S418), [S419](SOURCES.md#S419).

**[W2-05-F08](RAW_FACTS.md#F324) / primary_docs + local_test + author_claim:** Card/config specify640 input, ultralytics8.0.21 / ultralyticsplus0.0.23 and validation `mAP@0.5(box)=0.83794` (stored under a `precision` metric type with explicit comment). This is publisher-reported image detection validation, not independent replication, event accuracy or SmartSpaces transfer performance. Static args include `yolov8n.yaml`, local `Forklift-1/data.yaml`,50epochs,batch8,imgsz640,SGD,seed0,pretrainedFalse. These embedded settings are provenance evidence, **not a fully recoverable training recipe**: local data YAML path is unavailable and exact image-manifest/initialization/environment reproducibility is not established.

Named source dataset: https://huggingface.co/datasets/keremberke/forklift-object-detection and original Mohamed Traore, *Forklift*, Roboflow v1 `raw-images`: https://universe.roboflow.com/mohamed-traore-2ekkp/forklift-dsitv/dataset/1 . Independently read original page: CC BY4.0,421 images,295/84/42 train/valid/test, auto-orient/no augmentations. This is positive **image-data** licensing evidence; it does not become checkpoint-specific or SmartSpaces-media licensing. HF model card has no explicit license metadata; the MIT catalogue LICENSE is stronger than no grant anywhere, weaker than an explicit artifact-specific weight grant. Runtime Ultralytics licensing/version obligations require separate exact deployment-chain review; nothing here grants an all-MIT chain.

<a id="F325"></a>
### F325 — W2_05: K005 outcome and practical handoff

Provenance: [W2_05:67](_WORK/W2_05.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## K005 outcome and practical handoff

| K005 component | Outcome | Exact new basis / remaining gate |
|---|---|---|
| Real machine/pedestrian existence unreviewed | **scope_narrowed** | Full source file/hash/decode + full-duration sampled inventory proves independent workers and moving driven truck; F04–F06 |
| Public release versus hidden-target wording | **contradiction** | Same current pinned revision still says both; F01–F03. No universal ban or unrestricted training conclusion |
| Exact detector primary artifact/map | **closed for artifact and class semantics** | Full binary/hash, safe opcode inspection, publisher card; F07. Weight grant/execution/transfer/LinQ remain open |
| Real risk/negative-control readiness | **still_open** | No certified pair-event labels/surveyed envelope/full controls; observed routine episode is supplementary only |

For model_stack/linq_platform: binary identity and640/two-class contract are concrete; export/operators/device support and post-export quality are untested. For training_strategy/datasets: retain CC BY evidence and contradiction separately, and preserve this official test scene as a holdout rather than tuning on it. For evaluation/video_architecture: PTS CSV enables future causal replay only after permitted-use decision; decode success is not a temporal model benchmark. Keep all four views of Warehouse026 grouped with its same source60s, likewise all seven of Warehouse027; no independent camera-hours/event multiplication.

The first useful engineering test remains a permissioned target pack with driver-only, stationary-near, moving-far, turn/reverse, rack occlusion and independent pair-policy labels; evaluate event recall, timely recall, eligible-hour false alerts, duplicates and onset-to-notification latency at native and downsampled cadence while retaining source PTS. No dangerous staging is required. External gate: organizer/owner target videos, policy and measured calibration; SDK gate: actual LinQ neural execution and allowed hostCPU tracking/rules. No performance, timing, inference or training test was performed in this branch.

<a id="F326"></a>
### F326 — W2_06: W2_06 — exact flame checkpoint and MmodalFire release audit

Provenance: [W2_06:1](_WORK/W2_06.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_06 — exact flame checkpoint and MmodalFire release audit

Access/local work: 2026-10-23, approximately 20:20–20:31 UTC (23:20–23:31 Moscow). Assignment K006. Exclusive evidence: `W2_06_EVIDENCE/`; full prompt copied there as `PROMPT_W2_06.md`. Read `_WORK/CASE_NOTES.md`, `_WORK/SYNTHESIS_CONTRACT.md`, K006, W1_D14 and named MmodalFire snapshots, and exact flame lead in adjacent feasibility report. Historical material was a locator, not current evidence. No substantive task change.

<a id="F327"></a>
### F327 — W2_06: Decision and K outcome

Provenance: [W2_06:5](_WORK/W2_06.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Decision and K outcome

**K006: scope_narrowed, not closed.** Exact current flame checkpoint independently acquired, hashed, statically inspected. Complete MmodalFire member manifest, README, settings workbook and mist sensor pair acquired. One small raw video acquired/fully decoded, but its visible clock excludes it from the listed mist sessions. **No mist video or dense flame onset/clear GT acquired.** Factory steam, allowed furnace/welding and permit controls remain open. Keep a narrow visible-flame-region development route; this evidence does not justify a ready industrial event MVP.

| Sub-question | Outcome | Basis and residual gate |
|---|---|---|
| Exact checkpoint/map/stated weight grant/static payload | closed for supply identity | F01 fresh bytes/card/API; 0 smoke/1 fire; AGPL. Execution/export/device/accuracy separate. |
| Full archive manifest/member access | closed for this listed file | F02 end block reached,103members,valid header CRCs,non-solid. Full-file MD5 not locally verified. |
| Small suitable mist video | still_open, localized | F03–04 clock-based mapping absent; smallest video Aug2 09:33 is not mist. Larger member identification/acquisition remains. |
| Onset/clear/rearm and factory validity | still_open | Binary sequence labels/session spans are not ignition/extinction GT. Target footage, authorization policy and SDK/device experiments needed. |

<a id="F328"></a>
### F328 — W2_06: W2-06-F01 — exact current flame supply confirmation

Provenance: [W2_06:16](_WORK/W2_06.md); original aliases: W2-06-F01. Sources: [S420](SOURCES.md#S420), [S421](SOURCES.md#S421), [S422](SOURCES.md#S422), [S423](SOURCES.md#S423).

## [W2-06-F01](RAW_FACTS.md#F328) — exact current flame supply confirmation

**[primary_docs; artifact_access_checked; local_test: ZIP/pickle bytecode parsing only]** Author/account rabahdev, *YOLOv8n — Fire & Smoke Detector (D-Fire fine-tune)*, HF `rabahdev/fire-smoke-yolov8n`. Current and pinned API both return **13017fe8af477c25f5298d168e2dfede4b000753**. Pinned card GET2001,262B; exact best.pt fresh GET200 **6,229,802B**, SHA256 **b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f**. Historical hash agrees, but these are independently current bytes.

Artifact: https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/13017fe8af477c25f5298d168e2dfede4b000753/best.pt . Card: https://huggingface.co/rabahdev/fire-smoke-yolov8n/raw/13017fe8af477c25f5298d168e2dfede4b000753/README.md . Current API: https://huggingface.co/api/models/rabahdev/fire-smoke-yolov8n . Pinned API: https://huggingface.co/api/models/rabahdev/fire-smoke-yolov8n/revision/13017fe8af477c25f5298d168e2dfede4b000753 . Evidence `hf_model.txt`,`hf_current.txt`,`hf_card.txt`,`access_metadata.json`,`checkpoint_static.json`,`best.pt`,`checkpoint_pickle_disassembly.txt`; performed code `checkpoint.py`.

Downloaded payload is a ZIP-based PyTorch checkpoint, not HTML. zipfile enumerated members and pickletools.dis disassembled data.pkl. **No pickle loading, torch import/load or model execution.** Byte offsets90151–90206 contain names dictionary integer0→smoke,1→fire. Offsets50–91 contain version8.4.51 and AGPL-3.0 metadata. These strings do not prove runtime validity. Smoke here means plume regions, not smoking people. Card and embedded map agree, preventing reversed class assignment.

**[author_claim; primary_docs]** Card says COCO-pretrained YOLOv8n, D-Fire fine-tune,50epochs,640image size,batch16,MuSGD(auto),lr0=.01,AppleMPS; train14,122/val3,099/test4,306images. Reports test mAP50=.754,mAP50–95=.430,precision=.766,recall=.688; smoke/fire mAP50–95=.499/.362. These are unreplicated image-level author results, not independent industrial event recall/latency/FP-hour. API lists no ONNX. RGB layout, normalization/letterbox, output graph dimensions/NMS, exact export parity and LinQ operators remain unobserved. Training size640 is not a graph-verified deployment input contract.

**Rights [primary_docs; unknown]** Card front matter and license section positively state AGPL-3.0 for model; embedded metadata agrees. Separate pinned LICENSE URL404 means standalone file not found at that path, not absence of grant. Runtime code/export-tool terms need separate pinned review. Fresh D-Fire master commit API gives **3890a756b224855f4f7ef8d237a70bc1834a4714**. Retrieved README/LICENSE: collection offered CC0, but underlying-image ownership disclaimed and README explicitly preserves original-provider terms for third-party PublicDataset sources. Thus AGPL/CC0 do not establish blanket underlying-media clearance. No legal opinion inferred.

**[primary_docs; inference]** D-Fire README names surveillance/web/public sources including HPWREN,FESB,FireNet. Older FURG/FIRESENSE media cannot automatically become source-independent holdout for this detector. Source-frame provenance/near-duplicate checking remains E002 work. Old five-clip FURG catalog not repeated.

<a id="F329"></a>
### F329 — W2_06: W2-06-F02 — complete MmodalFire manifest and real release structure

Provenance: [W2_06:30](_WORK/W2_06.md); original aliases: W2-06-F02. Sources: [S333](SOURCES.md#S333), [S334](SOURCES.md#S334), [S346](SOURCES.md#S346).

## [W2-06-F02](RAW_FACTS.md#F329) — complete MmodalFire manifest and real release structure

**[primary_docs; artifact_access_checked; local_test: RAR5 headers]** Qixing Zhang,Yang Jia,Yihan Guo,Yetang Chen,Xinmeng Zhang,Gang Wang, Figshare *MmodalFire: A Multimodal Dataset Comprising Video and Physical Sensing Data for Detecting Indoor Fires*, v1; https://api.figshare.com/v2/articles/28804448 . Paper Jia et al., *MmodalFire: A Continuous Multimodal Dataset Comprising Video and Physical Sensing Data for Detecting Indoor Fires*, Scientific Data13,489,2026-02-19, https://www.nature.com/articles/s41597-026-06810-6 . Current API GET2006,057B: one MmodalFire.rar **4,929,210,010B**, file53696243, dataset publication2026-03-28, CC BY4.0. Published MD5 **88287408a7a36a25999cf6276fa902a9** not locally verified.

URL https://ndownloader.figshare.com/files/53696243 . Initial range0–65535 GET20665,536B; total matches API; RAR5 signature526172211a070100. Response Last-Modified2025-04-16 is transport metadata, not substituted for publication. Downloader uses10second signed S3 URLs; expired direct URL403, fresh downloader ranges work. A preliminary rarfile remote-reader attempt did not complete within bounded time and was stopped, yielding no manifest. Manual RAR5 scanner then follows header+compressed-data sizes and validates header CRC32. Local interruptions were resumed from saved manifest. `manual_manifest.py`,`mmodalfire_manifest.json`,`manifest_summary.json`,`rar_access.json`,`rar_manual_ranges.json`. Resume overwrote request-only range list; it contains resumed requests, whereas complete manifest preserves all offsets/sizes/header CRC results. Recorded successful scanner metadata-range bytes **462,856**; stopped preliminary reader traffic not included. Full4.93GB archive not acquired.

**[local_test]** End header offset4,929,210,002,size8 exactly reaches declared archive end. **103 members:70CSV,28MP4,1XLSX,1TXT,3directories.** Main archive flags0; all member solid flags false; all parsed block CRCs match. One 原始数据 tree containing Physical sensing/,Video/,Readme.txt and SETTINGS OF THE COMBUSTION EXPERIMENT FOR DATA COLLECTION.xlsx. No separately named dense event annotation/box-label/processed-clip directory. Extensions alone do not rule out semantics inside uninspected members.

**[contradiction/scope mismatch]** Paper Data Records describes two lab folders MmodalFire(Xi’an)/MmodalFire(Hefei), InertialData/VideoData, and65recordings/experimental groups. Actual listed archive is a raw layout with28MP4. Several experiments may occupy one long raw file: **28 files does not disprove65experiments.** Second-lab/released coverage and count unit remain unresolved. Do not say65recordings acquired/decoded.

<a id="F330"></a>
### F330 — W2_06: W2-06-F03 — actual mist metadata/sensors and precise video join gap

Provenance: [W2_06:40](_WORK/W2_06.md); original aliases: W2-06-F03. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-06-F03](RAW_FACTS.md#F330) — actual mist metadata/sensors and precise video join gap

**[artifact_access_checked; local_test: extraction/read-only parsing]** Non-solid members allow exact ranges. Retrieved README310compressed/440raw bytes, workbook11,476compressed/13,282raw bytes. Derived one-member wrappers use original main/end/file headers; installed7-Zip25.01 extracts successfully, CRC checked. QuickOpen locator still references original large offset; wrappers are derived extracts, not original complete archives. Evidence metadata_*rar,metadata/,metadata_member_ranges.json,extract_metadata.py. Workbook ZIP/XML parsed read-only without formulas executed or source altered (`read_settings.py`,`settings_cells.json`); no workbook visual/recalculation claim.

README states raw surveillance videos show upper-left time and xxxx-1 physical file gives time for alignment. Actual worksheet1 A:G headers: Material,Lighting Environment(lx),Wind speed(m/s),Location of fire,Quantity of material,Time,Month.Day Hour:Min-Hour-Min. **No video filename column**, unlike publisher Table3. Rows2–39 describe38sessions; sheets2/3empty. These are session settings, not dense flame labels.

Workbook exact cells: A28–31 Dry ice1–4; F28–31 Aug4 15:12–15:20,15:23–15:30,15:41–15:51,15:56–16:03. A32–35 Mist1–4; F32–35 Aug10 16:01–16:09,16:12–16:20,16:22–16:29,16:31–16:37. G33 notes16:14 wind changed to.7m/s; G35 notes16:35 light on,68lux. Blank controls rows36/37 span16:38–16:42. Source cells contain fullwidth colons and no year. No ignition/extinction meaning given to these endpoints.

Retrieved **原始数据/Physical sensing/Humidifier4-1.csv**,133,001compressed/1,254,840raw bytes, and **Humidifier4-2.csv**,35,679compressed/616,066raw; independent7zip extraction successful. GB18030 CSV parse: each22,815data rows. -1 columns 时间/当前时间; first pair2022-08-10 08:31:23.167321 /2022-08-10 16:31:23.167321; last08:37:19.846596 /16:37:19.846596. Observed8hour offset preserved without assigning undocumented timezone. Current-time column strictly increasing,span356.679275s,steps.013417–.030592s. -2 six columns: smoke,temperature,5.0u/4.4u/3.8u bands,ultraviolet count. Equal row counts support positional-join candidate, not measured sync accuracy. No event labels in these two CSVs. SHA256 -1 **3b8cf615faaf2a704d55a4abcba5b182c39608e73741672cbc67c942ca89918a**; -2 **b17bc1323a50ef4a9844b05f217a811cd720bb03edd07928d7697d61844e13ed**. Evidence sensor/,sensor_csv_audit.json,sensor_member_access.json.

**[unknown; localized stop]** Video spanning2022-08-10 16:31:23–16:37:20 remains unidentified among opaque Downtest_ch01_...mp4 names. Every candidate range offset is available in manifest, but basename does not ground wall-clock join. Need acquire selected larger raw-video member and match upper-left camera clock against workbook/sensor time. After2.2MB minimum video below, next-smallest12.05MBcompressed; others48.70–253.84MB. Stopped without hundreds of MB of unverified material. This is a mapping/selected-media gap, not solid archive/authentication barrier, and arbitrary video is not renamed mist.

<a id="F331"></a>
### F331 — W2_06: W2-06-F04 — one actual short raw video, clock excludes mist

Provenance: [W2_06:52](_WORK/W2_06.md); original aliases: W2-06-F04. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## [W2-06-F04](RAW_FACTS.md#F331) — one actual short raw video, clock excludes mist

**[artifact_access_checked; local_test: extraction/full decode; visual sampled-frame inspection]** Smallest MP4: 原始数据/Video/Downtest_ch01_00000000002000300.mp4. Header offset375,353,196,size93; compressed payload range **375353289–377538003**,2,184,715B. Header+payload GET2062,184,808B. Derived wrapper7zip successful; extracted2,207,566B SHA256 **3f862452f3675fc85448b77ee238014f400e6aa1683d28645200c3b285b5721c**. small_video_access.json,small_video.rar,small_video/,small_video_decode.json,small_video_pts.json,small_video_contact.jpg.

PyAV fully decodes **1,064frames**,1920×1080,HEVC,time_base1/90000,firstPTS0,lastPTS3,825,540=42.506s. Stream declares1,065frames,duration3,832,740ticks,average_rate532500/21293(~25.009fps). Declared/decoded one-frame difference retained; this does not validate global30/12fps. Six samples visually inspected, not dense frame annotation. Camera display starts **2022年08月02日09:33:26**, sample frame80009:33:58. People move chair/handle room equipment. No flame/plume evident in inspected samples, but not all42.5s certified negative. Clock lies outside listed mist/dry-ice sessions. **Not an acquired mist control, completed flame event or dense negative GT.** No new manual event interval created.

<a id="F332"></a>
### F332 — W2_06: W2-06-F05 — temporal semantics and practical gate

Provenance: [W2_06:58](_WORK/W2_06.md); original aliases: W2-06-F05. Sources: [S424](SOURCES.md#S424).

## [W2-06-F05](RAW_FACTS.md#F332) — temporal semantics and practical gate

**[primary_docs; author_claim]** Publisher HTML/Table2/Table3 fresh GET200, saved article.txt/article_plain.txt/table2*/table3*. Article describes four fuels,dry-ice/humidifier controls,binary fire/nonfire sequences,5s windows and sensor fusion.30fps camera hardware versus12fps processed/recorded video,~45s videos versus>700min; acquired raw clip~25fps. Preserve distinct units/settings, no global correction inferred. Entire manifest does not establish released5sclips,65independent groups or dense onset/clear.

**[primary_docs; local static source reading]** Author code tree SHA **80063a3a7dd3335db28dfa67b1efd58583086ba1**, https://github.com/SiliconSisyphus/MultiModal-fire-detection/tree/80063a3a7dd3335db28dfa67b1efd58583086ba1 . Retrieved README,MIT LICENSE,Baseline/data/dataset.py,preprocess.py only. Dataset uses generic Action1/Action2,subject/trial spreadsheets, midpoint of supplied start/end and surrounding windows (dataset.py110–179,184–225). Midpoint-centered extraction uses future relative to midpoint and is not an online causal alarm rule. Generic start/end variables do not establish release ignition/extinction GT; named expected training spreadsheets not present in archive manifest. Code not executed. MIT source grant separate from Figshare CC BY4 media/metadata and model AGPL.

**[inference/proposed experiment]** Pin F01 bytes and actual runtime/export input contract first. Establish class correctness on development media; create new dense flame-region evidence,ignition/clear,visibility/unknown labels against original PTS,source/session grouping,censoring. Keep original binary sequence labels separate. Evaluate causal event precision,timely/all-event recall,unmatched alerts/camera-hour,duplicates,onset/confirmation/notification latency,clear/rearm; no arbitrary persistence threshold inferred here.

Required controls remain real factory steam/dust,smoke-only,welding/furnace under active/inactive authorization,orange clothing/reflections/screens,occlusion,tiny ignition. Lab mist is a narrow confuser only after actual video mapping, not a factory substitute. Smoking is separate: this detector proves no cigarette ownership,puff action or forbidden smoking. Exact LinQ compile/device parity,host boundary and measured latency await SDK/device and controlled replay. No inference,training,paid compute,huge archive download,subagents or outreach.

<a id="F333"></a>
### F333 — W2_07: W2_07 вЂ” actual MoViNet-A0 streaming contracts (K007)

Provenance: [W2_07:1](_WORK/W2_07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

# W2_07 — actual MoViNet-A0 streaming contracts (K007)

Access/static checks: 2026-10-23, approximately 20:25–20:35 UTC / 23:25–23:35 Moscow. Researcher W2_07. Full assignment preserved in [assignment.md](_WORK/W2_07_EVIDENCE/assignment.md). No substantive assignment change; the additional 2.6 MB quantized archive was checked because the frozen assignment explicitly requested the corresponding advertised INT8 artifact and grant.

<a id="F334"></a>
### F334 — W2_07: Decision and critic outcome

Provenance: [W2_07:5](_WORK/W2_07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Decision and critic outcome

**K007: scope_narrowed.** The previously missing actual artifact/state contract is now established for two distinct official A0 Stream artifacts. Both have accessible bytes, a single named signature, matched external states and a reproducible static manifest. The INT8 variant also has an explicit model-instance Apache 2.0 field. Neither establishes a task-specific industrial hazard detector, onset/clear quality, CPU latency or actual LinQ execution. Keep MoViNet as a conditional generic video-classifier/training donor, not a ready hazard head. Engineering should start only if a relevant permissioned target sequence and SDK/device path justify comparison with simpler methods.

The most consequential finding is memory semantics: the head carries a cumulative feature sum and frame count across calls. Its score classifies the prefix since reset; it is not a sliding-window onset score. The original float artifact additionally carries cumulative squeeze/excitation pool states in its blocks. The INT8 artifact is a different modified architecture: 30 block pool-state input/output pairs are literal identity passthroughs, but the head pool remains active. A label or score at time t is not evidence of current hazard presence or timely clearance. No temporal behavior was measured.

<a id="F335"></a>
### F335 — W2_07: Starting evidence and independent work

Provenance: [W2_07:11](_WORK/W2_07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Starting evidence and independent work

Read the exact K007 in CRITIC.md, `_WORK/W1_M08.md`, `_WORK/M08/movinet.txt`, `artifact_heads.json`, `movinetblog.txt`, `_WORK/CASE_NOTES.md`, and `_WORK/SYNTHESIS_CONTRACT.md`. W1 already established the causal architecture and HTTP headers, while leaving state/label contracts open. I did not repeat STGCN++ or X3D research. New work downloaded the complete float TFLite, parsed its FlatBuffer without an interpreter, pinned/read current and contemporaneous source, fetched a pinned 600-label file, followed the TF Hub migration, obtained official Kaggle model metadata, downloaded the small INT8 archive and parsed its sole model. No video was downloaded, decoded, or scored.

Tools actually used: Python 3.11 `requests`, stdlib hash/json/tarfile, FlatBuffers 25.12.19 and `tflite==2.18.0` schema parser installed with pip. The latter is a generated FlatBuffer schema reader; TensorFlow is absent. No TensorFlow, TFLite interpreter, model invocation, benchmark, training, ONNX export, paid API, outreach or subagent was used. Scripts and JSON outputs in the private evidence directory are repeatable metadata/static checks only. An initial script named `inspect.py` shadowed a Python stdlib module; renamed to `examine_bundle.py`, then reran successfully. Some historical source URL guesses returned 404; corrected paths below are the ones used as evidence.

<a id="F336"></a>
### F336 — W2_07: W2-07-F01 вЂ” exact float artifact identity and graph

Provenance: [W2_07:30](_WORK/W2_07.md); original aliases: W2-07-F01. Sources: [S198](SOURCES.md#S198).

## [W2-07-F01](RAW_FACTS.md#F336) — exact float artifact identity and graph

**artifact_access_checked/local_test.** HTTP 200, full **27,141,832 bytes**; SHA256 `04c02709bce4a8233b03f36620909924735051cfd4bcc83e3d9d7db9bbf375ad`. Google generation `1626903706896942`, metageneration `3`, last modified `2021-07-21 21:41:46 GMT`, ETag/MD5 `7ccd041e8adcc8ba0e1473ddefeebc20`, content-type application/octet-stream. Headers match W1 but this is an independent full-body fetch. An optional reproducible object version URL is S01 plus `?generation=1626903706896942` (not separately fetched).

FlatBuffer identifier TFL3; schema version 3; description `MLIR Converted.` One subgraph `main`; **one signature `serving_default`**, 44 named inputs and 44 named outputs. Inputs are `image` and 43 state tensors; outputs are `logits` and the same 43 state names. Every state input/output matches shape and dtype. No dynamic shape signature is present. Image is fixed `[1,1,172,172,3]`, FLOAT32; logits fixed `[1,600]`, FLOAT32. State payload alone is **2,696,832 bytes** (shape-product × dtype size), excluding image/output copies, weights, activations, interpreter and allocation overhead. This is not measured working-set memory.

All 1,372 tensors: 1,222 FLOAT32, 140 INT32, 10 INT64. No tensor has a quantization scale or zero-point vector. Integer tensors here include counters/shape indices and do not make an INT8 model. Minimum runtime metadata string is `2.5.0`; no class-map/associated-file metadata found. This runtime floor does not prove compatibility with a current runtime or LinQ.

896 builtin operator nodes, no custom operators observed. Counts and opcode versions: RESHAPE v1 203; CONV_2D v1 68; MUL v1 225; ADD v1 182; BROADCAST_TO v2 27; DEPTHWISE_CONV_2D v1 26; MEAN v1 30; CUMSUM v1 15; AVERAGE_POOL_2D v1 4; STRIDED_SLICE v4 26; CAST v1 16; DIV v2 16; CONCATENATION v1 26; MINIMUM v3 15; RELU v1 15; SUM v1 1; LOGISTIC v1 1. No SOFTMAX node. The named logits output is the classifier projection, not a verified calibrated probability or per-person detection. The graph has no detection boxes, track IDs, timestamps, hazard policy or event lifecycle output.

Complete tensor-name/index/shape/dtype pairing appears in the appendix and [static_graph.json](_WORK/W2_07_EVIDENCE/static_graph.json). Do not zip interpreter input/output arrays by order: use signature names. The physical tensor names have `serving_default_...:0` wrappers and anonymous `StatefulPartitionedCall:N` outputs; signature maps supply semantic keys.

<a id="F337"></a>
### F337 — W2_07: W2-07-F02 вЂ” advertised INT8 exists, has grant, and is a distinct graph

Provenance: [W2_07:42](_WORK/W2_07.md); original aliases: W2-07-F02. Sources: [S177](SOURCES.md#S177), [S198](SOURCES.md#S198), [S435](SOURCES.md#S435), [S436](SOURCES.md#S436), [S437](SOURCES.md#S437).

## [W2-07-F02](RAW_FACTS.md#F337) — advertised INT8 exists, has grant, and is a distinct graph

**artifact_access_checked/local_test/primary_docs.** S07 describes Google instance ID **322**, slug `a0-stream-kinetics-600-classification-tflite-int8`, framework tfLite, versionNumber **1**, versionId **445**, totalUncompressedBytes **3,276,048**, `licenseName: Apache 2.0`, overview explicitly INT8; usage history dates v1 to **2022-01-28**. This is an explicit model-instance license statement, stronger than inferring weights rights from the source-code license alone.

S08 returned HTTP 200 and redirected to public signed Google Storage `kaggle-models-data/322/445/bundle/archive.tar.gz`. Downloaded archive **2,641,653 bytes**, SHA256 `7b395747f5ed76429adac76e13a1d04e8ae6efe7a4196b39f32fc2b2f44e05d9`. Sole member `1.tflite`, **3,276,048 bytes**, SHA256 `6125b36e2485eeb5cc1fd6206cf5e5d70235593fbc84610d1dce97fe3aa9c2ac`. Canonical S08 is reusable; signed final URL is ephemeral. No account, agreement acceptance, inference, or external write was needed.

One subgraph, one `serving_default` signature, 44 inputs/44 outputs, same shape/dtype inventory as float at external interface, but renamed state keys such as `state_block3_layer0_stream_buffer` instead of `state/b3/l0/stream_buffer`. All image, stream-buffer, pool-buffer and logits I/O are **FLOAT32**; counters INT32. Quantized internal computation does not imply integer external I/O. All 43 state shapes/dtypes match outputs; **30 block pool buffer/count pairs map output to exactly the same tensor index as input**. Eleven convolution-stream buffers and two head-pool states remain updated (43в€’30=13); image is the other non-identity input. Preserve the complete signature state dictionary rather than deleting passthrough keys without a validated export.

452 tensors: 291 INT8, 118 INT32, 43 FLOAT32. 355 tensors have nonempty quantization scales (includes INT32 quantized biases); detailed per-tensor/per-axis scales, zero-points and dimensions are saved in `int8_static_graph.json`, not approximated by one global scale. Runtime metadata `2.3.0`; conversion metadata bytes include a `2.9.0` string, but the conversion metadata schema was not decoded, so it is not promoted to a proven exporter version. 227 operators: QUANTIZE v1 14, RESHAPE v1 74, CONV_2D v3 38, DEPTHWISE_CONV_2D v3 26, MUL v2 16, AVERAGE_POOL_2D v2 4, ADD v2 17, CONCATENATION v2 11, STRIDED_SLICE v4 11, DEQUANTIZE v2 13, SUM v2 1, CAST v1 1, DIV v2 1. No custom operator observed.

The head graph tail statically shows previous head pool input being quantized, added to spatially pooled current features, dequantized to new FLOAT32 pool output; frame count incremented, cast, and used as DIV denominator; classifier quantized projection followed by dequantized FLOAT32 logits. This is accumulation under quantized arithmetic, not a proof of exact real-number averaging or parity with float. Saved [graph_tail.json](_WORK/W2_07_EVIDENCE/graph_tail.json) provides input/output tensor names and node indices.

S06 explains that quantized MoViNets replace hard-swish with ReLU6 and remove squeeze/excitation layers; this independently explains the disappearance of 15 block cumulative pools and 30 passthrough state tensors. It reports architecture loss of 3–4 percentage points, another 2–3 from integer post-training quantization, and total 5–7 on full 10-second K600 clips; these are authors' historical aggregate claims, not our validation. Advertised A0 INT8: 65.0% top-1, 4.80 ms Pixel 4 CPU, 3.1 MB, recommended 172×172 at 5 FPS. Authors distinguish model-only throughput from camera pipeline throughput. Do not apply those numbers to S01, LinQ, eight hazards, multi-person crops, notification delay or current hardware. The current README calls the float A0 TFLite 13 MB, but actual downloaded S01 is 27,141,832 bytes: preserve the binary observation over the size label. Float16 was located by TF Hub redirect and HEAD-like streamed GET but not downloaded/parsed.

Counterevidence/documentation defects: the official INT8 usage string contains a `...tflite-float8...` example path, which is inconsistent with its INT8 slug/download metadata. Use the actual v1 download and parsed signature. Direct guessed Kaggle model metadata routes returned 404; the official list endpoint supplied the successful model record. TF Hub base model URL redirected to a generic Kaggle model-list page, so its success alone would not have established a specific variant.

<a id="F338"></a>
### F338 — W2_07: W2-07-F03 вЂ” pinned pooling, export and reset semantics

Provenance: [W2_07:58](_WORK/W2_07.md); original aliases: W2-07-F03. Sources: [S430](SOURCES.md#S430), [S431](SOURCES.md#S431), [S432](SOURCES.md#S432), [S433](SOURCES.md#S433).

## [W2-07-F03](RAW_FACTS.md#F338) — pinned pooling, export and reset semantics

**primary_docs + static graph inference.** S03 source is contemporaneous with float storage upload but not a cryptographically linked build recipe. Its `export_saved_model.py` lines 163–195 builds explicit `image` and state signatures; `predict` returns states plus `logits`; bundled `init_states` is optional. The actual float and INT8 binaries expose only `serving_default`, no `init_states` callable. Initialize from actual signature shapes/dtypes, not by guessing an extra signature. Historical `modeling/movinet.py` defines slash-state names, including `state/bN/lN/...`; current S02 source uses underscore names and changed conventions. Current source must not silently replace the archived binary's contract.

Historical S04 `GlobalAveragePool3D` lines 637–681 reads a pool sum and frame counter, increments counter by frames in this call, adds spatially averaged current features to the sum, and divides by all frames since initialization. In causal mode it uses cumulative sums so each within-clip step sees only its prefix; in noncausal mode it aggregates the current call while retaining history. Head uses global pooling; block squeeze/excitation also uses cumulative pooling in float. This is feature averaging before classifier projection, not arithmetic averaging of class probabilities and not a fixed recent duration. Finite convolution stream buffers and global accumulators have different horizons.

Current pinned README lines 303–320 explicitly initializes all state tensors to zero, feeds returned states to the next frame and uses the last output as video classification. Its TFLite example lines 370–395 does the same. The model-page usage supplies the same zero-state/per-video loop. Documentation expresses a new-video boundary by creating/reassigning initial states before the video loop; no automatic camera/actor/PTS detection or timed reset is promised. In the chosen lifecycle contract a new independent video/camera stream/crop identity must receive fresh zero states. This boundary policy is our reproducible application choice grounded in the documented video-loop initialization, not an experimentally validated industrial reset cadence.

**inference:** retaining states after an event can retain features of the event, and a long normal prefix can dilute a later short event in head pooling. Resetting frequently can restore short horizon but changes the reference computation and repeatedly incurs cold-start history; no time-local detection guarantee follows. Refeeding an old frame updates counts again; dropped source time does not advance the network unless a frame is supplied. No source timestamp is an input, so changing cadence changes physical time represented by the same buffer length and frame average. Do not represent these models as PTS-aware temporal encoders.

<a id="F339"></a>
### F339 — W2_07: W2-07-F04 вЂ” class-map provenance and eight-scenario mismatch

Provenance: [W2_07:68](_WORK/W2_07.md); original aliases: W2-07-F04. Sources: [S434](SOURCES.md#S434).

## [W2-07-F04](RAW_FACTS.md#F339) — class-map provenance and eight-scenario mismatch

**artifact_access_checked/local_test.** S05 label map has exactly 600 newline-separated labels, interpreted as zero-based output indices by the tutorial's label lookup. SHA256 `8dfca4202520ea8291ce0242ef33b006d0a0772b409663c090a2876bc1978dcf`; 9,209 bytes. The blog-pinned 2022 map and fetched current pinned map are byte-identical. Binary metadata contains no embedded label map: binding relies on official K600 model provenance and official tutorial/map convention, not an intrinsic self-description. No industrial fine-tuned head was found or tested.

| Case target | Exact K600 labels (zero-based) that could be donors/confusers | Why this is not a ready target head |
|---|---|---|
| Running / abrupt movement around machinery | 236 `jogging`; 427 `running on treadmill`; 223 `hurdling`; 307 `parkour`; 234 `jaywalking`; 572 `walking through snow` | Jogging is a closer generic gait-action donor; treadmill/hurdling/parkour are additional motion donors/confusers. No industrial speed/acceleration criterion or machinery-zone relation is encoded. |
| Dangerous proximity to moving mechanism/vehicle | 149 `driving car`; 150 `driving tractor` | Driver action does not label pedestrian/vehicle pair, motion envelope, zone breach or dangerous distance. |
| Phone while moving OR equipment work | 265 `looking at phone`; 516 `talking on cell phone`; 525 `texting` | Useful generic phone-action donors; do not encode concurrent movement/equipment operation, identity or permit. Looking at phone does not establish prohibited use. |
| Smoking/open flame outside designated place | 477 `smoking`; 478 `smoking hookah`; 479 `smoking pipe`; 261 `lighting fire`; 108 `cooking on campfire`; 170 `extinguishing fire`; 588 `welding` | Smoking class is potentially relevant action transfer; location permission, cigarette visibility and persistent flame are separate. Welding/cooking/extinguishing are meaningful confusers, not automatically violations. |
| Climbing barrier / under conveyor or suspended load | 101 `climbing ladder`; 100 `climbing a rope`; 102 `climbing tree`; 422 `rock climbing`; 307 `parkour` | No barrier/conveyor/load relation or work-zone policy class. Ladder climbing is not barrier crossing. |
| Height without harness | 101 `climbing ladder`; 536 `tightrope walking`; 60 `bungee jumping` | Height exposure, required PPE and verified anchorage are absent; rope-related class names cannot establish attachment safety. |
| Fall, lying, immobility | 172 `falling off bike`; 173 `falling off chair`; 474 `sleeping` | Particular falls do not cover general falls; sleeping is not unconsciousness, long immobility or a completed stationary-hold interval. |
| Incorrect carrying | 70 `carrying baby`; 133 `deadlifting`; 480 `snatch weight lifting` | No industrial carry procedure, load limits or misuse label. Generic movement is not a carrying-rule violation. |

These are names from the parsed class list, not measured successes. Matching a nearest name does not rename it as the policy target. No class returns actor/pair identity or temporal interval. Full-scene classification mixes multiple people; per-person cropping is a separate distribution/geometry decision. Each crop/track needs its own state and rules for identity switches, loss, reacquisition and framing; state must not move between unrelated actors.

<a id="F340"></a>
### F340 — W2_07: W2-07-F05 вЂ” concrete future first-run contract (NOT executed)

Provenance: [W2_07:85](_WORK/W2_07.md); original aliases: W2-07-F05. Sources: [S177](SOURCES.md#S177), [S198](SOURCES.md#S198).

## [W2-07-F05](RAW_FACTS.md#F340) — concrete future first-run contract (NOT executed)

The following is a proposed first reference run after inference authorization/environment access, not a test result. Fix S01 hash above first; choose FLOAT32 reference before comparing modified INT8. Save model SHA, software/runtime/delegate versions, video SHA/session/scene/actor groups, decoder, original time_base/PTS, selected PTS, resize/crop transform and state lifecycle ledger. Use one permissioned video and one fixed scene/crop; do not call it a lockbox after inspecting/tuning on it.

1. Read the exact `serving_default` signature mappings in `static_graph.json`; assert 44 inputs/44 outputs and image/logits shapes. Create zeros for each of 43 state inputs with the listed dtype (INT32 counters, FLOAT32 buffers). No inference required for this contract check.
2. Decode RGB chronological source frames, record original PTS; choose a declared 5-FPS sampling condition because S06 recommends it (then compare other rates later). Resize consistently to 172×172 (the pinned tutorial uses direct resize) and divide uint8 values by 255 into FLOAT32 [0,1]; record aspect distortion/crop policy. Exact `[1,1,172,172,3]` layout is batch,time,height,width,channels (NTHWC), RGB last. Do not pass BGR/uint8, normalize to [-1,1], stack arbitrary multi-frame clips into this fixed binary, or infer policy from a single frame.
3. At each selected source PTS call the signature once with `image` and all current state keys. Save raw `[1,600]` logits, remove only `logits` from returned mapping, and feed the 43 remaining same-name outputs into the next call. Softmax, if used for display/top-k, is external and logged; it is not a calibrated hazard probability. No `argmax` threshold is an event detector.
4. At a declared independent video/stream/crop identity boundary reset **all** states to newly allocated zeros. Log reason and PTS. Do not reset just head count, just buffers, or share one mutable state dictionary across streams. To compare INT8, use its own hash and underscore signature names, instantiate independently, and use FLOAT32 image/state/logits IO as the actual artifact requires. It is not a drop-in name-compatible or architecture-identical quantization of S01.
5. Record reference logits before any hazard adaptation; task-specific classifiers/rules and event confirmation/clear/rearm require independent annotations and predeclared policy. Future LinQ test must compile/run this exact graph and compare exact reference outputs/quality; neither a successful static parse nor CPU execution meets mandatory actual LinQ inference.

Potential source-code syntax/usage is intentionally not executed here. Current Kaggle quantized helper casts only inputs having actual nonzero scale and non-FLOAT32 dtype; the downloaded variant has FLOAT32 external image/state tensors, so its caller should not invent an INT8 image quantizer from internal scales.

<a id="F341"></a>
### F341 — W2_07: W2-07-F06 вЂ” future controls and decision gates

Provenance: [W2_07:97](_WORK/W2_07.md); original aliases: W2-07-F06. Sources: [S198](SOURCES.md#S198), [S437](SOURCES.md#S437).

## [W2-07-F06](RAW_FACTS.md#F341) — future controls and decision gates

| Future control | What must be held/logged | Observation and decision implication |
|---|---|---|
| Cold start / repeated zero reset | Same frames, same PTS, transform, runtime and hash; independent fresh dictionaries | Repeatability and early-history behavior. Static analysis does not predict detection latency. Compare cold-start prefix lengths; do not trim failed early events from denominator. |
| Long normal prefix → event → clear | Permissioned continuous GT with event onset/visible/confirmation/end, actor and censoring; vary genuine normal prefix length, no loops | Save complete logits and event alerts. Measure prefix dilution, onset/timely recall and persistence/clear lag. Failure keeps generic donor status or motivates explicitly bounded history plus validation. |
| Scene vs person crops / actor switches | Separate stream/crop IDs, crop transform, track/identity switches, occlusion, source group | Compare full scene with per-actor crop; reset at declared identity boundary. Detect state contamination; never call actor-level success from scene score alone. |
| Stream change, reconnect and restart | Camera ID, PTS discontinuity, runtime restart, state checkpoint/hash if retained | Compare full reset with same-stream resume. Unknown continuity gets explicit unknown state. Do not silently bridge different sources. |
| State interruption | Keep/discard state under identical frames; dropped frames vs processing pause vs source gap distinct | Measure recovery and carryover; do not duplicate frames to fill missing time or count a missing prediction as safe. |
| Cadence and frame loss | 1/2/5/native FPS replay plus phase offsets and dropped-frame bursts on original PTS | Event/timely recall, alert precision/FP per reviewed camera-hour, clear and duplicate behavior; each condition represents different source-time memory. No claim that 1 FPS is sufficient. |
| Quantized modified architecture | Independent S01/S08 hashes, same inputs/state-boundary policy; raw outputs and target event evaluation | Check numerical and task-quality delta without expecting parity by construction; internal INT8 does not imply LinQ support or faster full pipeline. |

Acceptance thresholds/notification deadline are organizer/team gates, not invented here. Evaluate one-to-one actor/pair-compatible episodes, all-event and observable-event recall with coverage, timely recall, unmatched alerts per reviewed negative camera-hour, duplicate alerts, onset/confirmation/notification latency and clear/rearm errors. Keep censored intervals explicit. Bad detector/visibility coverage must not hide missed GT events.

<a id="F342"></a>
### F342 — W2_07: Rights and unresolved gates

Provenance: [W2_07:111](_WORK/W2_07.md); original aliases: section record. Sources: [S198](SOURCES.md#S198), [S430](SOURCES.md#S430), [S435](SOURCES.md#S435), [S436](SOURCES.md#S436).

## Rights and unresolved gates

Code: S02 README/attached LICENSE Apache 2.0. INT8 weights: explicit S07 model-instance Apache 2.0, no separate license member in downloaded tar; preserve metadata, attribution and applicable notice obligations when using it. Float S01: linked from the officially Apache-licensed project, but bare binary has no embedded model license; no dedicated float instance grant was retrieved in this bounded check. Treat direct downloadable float rights as project-level provenance with that remaining per-artifact uncertainty, not as proven unlicensed. Do not transfer the INT8 instance grant to every unrelated artifact.

Class-map file is in the same project and map provenance is pinned; annotations/media are separate. No Kinetics source videos, industrial footage, consent, target annotations or redistribution rights were acquired or cleared. Model license does not clear YouTube/Kinetics media. Public accessibility is not a media grant. No request to authors/organizers was sent.

Remaining unknowns: exact binary build commit/checkpoint/calibration corpus and float-v-INT8 semantic parity; target action/actor/event usefulness; optimal lifecycle/window/reset policy; crop/camera distribution shifts; actual cold-start/normal-prefix/onset/clear/cadence behavior; actual CPU/RTX performance; exact LinQ ops/shapes/state binding/compiler support and host/device boundary; permissioned target labels; policy thresholds and notification SLA. Neither binary includes an industrial hazard head or event-state machine.

Practical handoff: `model_stack`/`model_fidelity_quantization` get the two hashes, distinct state names/architectures and reference manifests; `video_architecture` gets explicit prefix accumulator and reset ledger; `evaluation` gets the control matrix and original-PTS rule; `datasets`/`training_strategy` get only generic K600 donors, not target labels; `linq_platform` gets exact builtin versions/shapes and the unchanged external gate of real device execution. For K007 the static artifact gap is closed, task-specific temporal baseline and platform feasibility remain experiment/SDK/organizer/permission dependent.

<a id="F343"></a>
### F343 — W2_07: Appendix вЂ” exact float signature input/output contract

Provenance: [W2_07:121](_WORK/W2_07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Appendix — exact float signature input/output contract

All names below are signature keys. For each state the output has identical shape/dtype. `image` is input-only; `logits` is output-only `[1,600]` FLOAT32, tensor index 1371. Every pool counter is INT32 `[1]`; every pool/stream buffer FLOAT32. The table is generated from actual bytes, not source reconstruction.


| State / input | Input index | Output index | Shape | Dtype | Match |
|---|---:|---:|---|---|---|
| `image` | 37 | None | `[1, 1, 172, 172, 3]` | FLOAT32 | image only |
| `state/b0/l0/pool_buffer` | 29 | 514 | `[1, 1, 1, 1, 24]` | FLOAT32 | yes |
| `state/b0/l0/pool_frame_count` | 43 | 515 | `[1]` | INT32 | yes |
| `state/b1/l0/pool_buffer` | 33 | 584 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state/b1/l0/pool_frame_count` | 32 | 568 | `[1]` | INT32 | yes |
| `state/b1/l0/stream_buffer` | 13 | 625 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state/b1/l1/pool_buffer` | 39 | 642 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state/b1/l1/pool_frame_count` | 23 | 626 | `[1]` | INT32 | yes |
| `state/b1/l1/stream_buffer` | 3 | 683 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state/b1/l2/pool_buffer` | 21 | 700 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state/b1/l2/pool_frame_count` | 25 | 684 | `[1]` | INT32 | yes |
| `state/b1/l2/stream_buffer` | 40 | 751 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state/b2/l0/pool_buffer` | 6 | 768 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b2/l0/pool_frame_count` | 11 | 752 | `[1]` | INT32 | yes |
| `state/b2/l0/stream_buffer` | 38 | 809 | `[1, 4, 11, 11, 184]` | FLOAT32 | yes |
| `state/b2/l1/pool_buffer` | 2 | 826 | `[1, 1, 1, 1, 112]` | FLOAT32 | yes |
| `state/b2/l1/pool_frame_count` | 26 | 810 | `[1]` | INT32 | yes |
| `state/b2/l1/stream_buffer` | 10 | 867 | `[1, 2, 11, 11, 112]` | FLOAT32 | yes |
| `state/b2/l2/pool_buffer` | 5 | 884 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b2/l2/pool_frame_count` | 4 | 868 | `[1]` | INT32 | yes |
| `state/b2/l2/stream_buffer` | 12 | 925 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state/b3/l0/pool_buffer` | 31 | 942 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b3/l0/pool_frame_count` | 35 | 926 | `[1]` | INT32 | yes |
| `state/b3/l0/stream_buffer` | 1 | 983 | `[1, 4, 11, 11, 184]` | FLOAT32 | yes |
| `state/b3/l1/pool_buffer` | 14 | 1000 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b3/l1/pool_frame_count` | 19 | 984 | `[1]` | INT32 | yes |
| `state/b3/l1/stream_buffer` | 24 | 1041 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state/b3/l2/pool_buffer` | 15 | 1058 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b3/l2/pool_frame_count` | 30 | 1042 | `[1]` | INT32 | yes |
| `state/b3/l2/stream_buffer` | 20 | 1099 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state/b3/l3/pool_buffer` | 18 | 1116 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state/b3/l3/pool_frame_count` | 36 | 1100 | `[1]` | INT32 | yes |
| `state/b3/l3/stream_buffer` | 7 | 1163 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state/b4/l0/pool_buffer` | 9 | 1180 | `[1, 1, 1, 1, 384]` | FLOAT32 | yes |
| `state/b4/l0/pool_frame_count` | 8 | 1164 | `[1]` | INT32 | yes |
| `state/b4/l0/stream_buffer` | 17 | 1224 | `[1, 4, 6, 6, 384]` | FLOAT32 | yes |
| `state/b4/l1/pool_buffer` | 42 | 1226 | `[1, 1, 1, 1, 280]` | FLOAT32 | yes |
| `state/b4/l1/pool_frame_count` | 0 | 1227 | `[1]` | INT32 | yes |
| `state/b4/l2/pool_buffer` | 16 | 1274 | `[1, 1, 1, 1, 280]` | FLOAT32 | yes |
| `state/b4/l2/pool_frame_count` | 27 | 1275 | `[1]` | INT32 | yes |
| `state/b4/l3/pool_buffer` | 41 | 1322 | `[1, 1, 1, 1, 344]` | FLOAT32 | yes |
| `state/b4/l3/pool_frame_count` | 34 | 1323 | `[1]` | INT32 | yes |
| `state/head/pool_buffer` | 28 | 1360 | `[1, 1, 1, 1, 480]` | FLOAT32 | yes |
| `state/head/pool_frame_count` | 22 | 1361 | `[1]` | INT32 | yes |

<a id="F344"></a>
### F344 — W2_07: Appendix вЂ” exact INT8-variant signature input/output contract

Provenance: [W2_07:173](_WORK/W2_07.md); original aliases: section record. Sources: see explicit primary source identities/locators in this record and the branch acquisition notebook in SOURCES; no new execution asserted.

## Appendix — exact INT8-variant signature input/output contract

This separate table preserves the actual underscore names and the 30 literal identity pairs; same-index output is not evidence of updated cumulative state. `logits` output-only tensor index 451, `[1,600]` FLOAT32. Detailed internal quantization vectors are in the JSON manifest.

| State / input | Input index | Output index | Shape | Dtype | Match |
|---|---:|---:|---|---|---|
| `image` | 37 | None | `[1, 1, 172, 172, 3]` | FLOAT32 | image only |
| `state_block0_layer0_pool_buffer` | 17 | 17 | `[1, 1, 1, 1, 24]` | FLOAT32 | yes |
| `state_block0_layer0_pool_frame_count` | 18 | 18 | `[1]` | INT32 | yes |
| `state_block1_layer0_pool_buffer` | 30 | 30 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state_block1_layer0_pool_frame_count` | 19 | 19 | `[1]` | INT32 | yes |
| `state_block1_layer0_stream_buffer` | 27 | 270 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state_block1_layer1_pool_buffer` | 15 | 15 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state_block1_layer1_pool_frame_count` | 24 | 24 | `[1]` | INT32 | yes |
| `state_block1_layer1_stream_buffer` | 1 | 284 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state_block1_layer2_pool_buffer` | 38 | 38 | `[1, 1, 1, 1, 80]` | FLOAT32 | yes |
| `state_block1_layer2_pool_frame_count` | 36 | 36 | `[1]` | INT32 | yes |
| `state_block1_layer2_stream_buffer` | 2 | 302 | `[1, 2, 22, 22, 80]` | FLOAT32 | yes |
| `state_block2_layer0_pool_buffer` | 39 | 39 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block2_layer0_pool_frame_count` | 22 | 22 | `[1]` | INT32 | yes |
| `state_block2_layer0_stream_buffer` | 32 | 316 | `[1, 4, 11, 11, 184]` | FLOAT32 | yes |
| `state_block2_layer1_pool_buffer` | 10 | 10 | `[1, 1, 1, 1, 112]` | FLOAT32 | yes |
| `state_block2_layer1_pool_frame_count` | 43 | 43 | `[1]` | INT32 | yes |
| `state_block2_layer1_stream_buffer` | 11 | 330 | `[1, 2, 11, 11, 112]` | FLOAT32 | yes |
| `state_block2_layer2_pool_buffer` | 33 | 33 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block2_layer2_pool_frame_count` | 21 | 21 | `[1]` | INT32 | yes |
| `state_block2_layer2_stream_buffer` | 9 | 344 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state_block3_layer0_pool_buffer` | 20 | 20 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block3_layer0_pool_frame_count` | 31 | 31 | `[1]` | INT32 | yes |
| `state_block3_layer0_stream_buffer` | 8 | 358 | `[1, 4, 11, 11, 184]` | FLOAT32 | yes |
| `state_block3_layer1_pool_buffer` | 28 | 28 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block3_layer1_pool_frame_count` | 3 | 3 | `[1]` | INT32 | yes |
| `state_block3_layer1_stream_buffer` | 12 | 372 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state_block3_layer2_pool_buffer` | 4 | 4 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block3_layer2_pool_frame_count` | 16 | 16 | `[1]` | INT32 | yes |
| `state_block3_layer2_stream_buffer` | 25 | 386 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state_block3_layer3_pool_buffer` | 42 | 42 | `[1, 1, 1, 1, 184]` | FLOAT32 | yes |
| `state_block3_layer3_pool_frame_count` | 5 | 5 | `[1]` | INT32 | yes |
| `state_block3_layer3_stream_buffer` | 14 | 404 | `[1, 2, 11, 11, 184]` | FLOAT32 | yes |
| `state_block4_layer0_pool_buffer` | 6 | 6 | `[1, 1, 1, 1, 384]` | FLOAT32 | yes |
| `state_block4_layer0_pool_frame_count` | 13 | 13 | `[1]` | INT32 | yes |
| `state_block4_layer0_stream_buffer` | 26 | 440 | `[1, 4, 6, 6, 384]` | FLOAT32 | yes |
| `state_block4_layer1_pool_buffer` | 35 | 35 | `[1, 1, 1, 1, 280]` | FLOAT32 | yes |
| `state_block4_layer1_pool_frame_count` | 0 | 0 | `[1]` | INT32 | yes |
| `state_block4_layer2_pool_buffer` | 41 | 41 | `[1, 1, 1, 1, 280]` | FLOAT32 | yes |
| `state_block4_layer2_pool_frame_count` | 23 | 23 | `[1]` | INT32 | yes |
| `state_block4_layer3_pool_buffer` | 29 | 29 | `[1, 1, 1, 1, 344]` | FLOAT32 | yes |
| `state_block4_layer3_pool_frame_count` | 40 | 40 | `[1]` | INT32 | yes |
| `state_head_pool_buffer` | 34 | 442 | `[1, 1, 1, 1, 480]` | FLOAT32 | yes |
| `state_head_pool_frame_count` | 7 | 443 | `[1]` | INT32 | yes |
