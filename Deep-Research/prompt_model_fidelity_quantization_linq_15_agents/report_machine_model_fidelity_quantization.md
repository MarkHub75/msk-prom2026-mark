---
topic: model_fidelity_quantization
scope: >-
  Evidence-based preservation of detection, pose, tracking and useful video-event
  behavior across source preparation, export, graph passes, floating precision,
  PTQ, compiler and LinQ runtime boundaries. Includes versioned contracts,
  diagnosis, conditional recovery, independent acceptance and an unrun test program.
not_covered:
  - "linq_platform: provisioning, credentials and a verified installed SDK/device bundle"
  - "model_stack: final checkpoint selection, acquired weights and a tested deployment implementation"
  - "datasets: acquisition, licensing and independent annotation of industrial video"
  - "training_strategy: executed adaptation, GPU procurement and measured training budgets"
  - "violation_methods: complete scenario feasibility and final behavioral predicates"
  - "video_architecture/operator_product: production service implementation and operator workflow"
  - "evaluation/hackathon_strategy/market_deployment: final risk approval, competition strategy or safety certification"
answers:
  - question: "What is a defensible source baseline and golden comparison?"
    section: source-golden-contract
  - question: "How can the first divergent export, graph, dtype or runtime boundary be isolated?"
    section: fidelity-ladder
  - question: "Which preprocessing, geometry, detector, pose and NMS contracts must match?"
    section: input-output-geometry
  - question: "Which exporter and operator semantics are version dependent?"
    section: exporter-graph-semantics
  - question: "How should floating conversion be separated from quantization loss?"
    section: floating-numerics
  - question: "How should calibration data, method and effective configuration be tested?"
    section: ptq-calibration
  - question: "When are selective precision, correction, QAT or a different architecture viable?"
    section: recovery-admission
  - question: "Why do small objects, occlusion, pose and causal events need separate slices?"
    section: small-pose-temporal
  - question: "What is documented for LinQ and what remains unknown in the granted environment?"
    section: linq-route-access
  - question: "What constitutes quality acceptance and honest uncertainty?"
    section: acceptance-five-gates
  - question: "Which diagnostic action and rollback follow each failure symptom?"
    section: diagnosis-stop-loss
  - question: "Which practical tests should be run, with which observables and limits?"
    section: experiment-program
  - question: "What proves actual TPU execution and what should the jury see?"
    section: device-jury-evidence
  - question: "Which engineer questions and neighboring-topic handoffs are highest priority?"
    section: questions-handoffs
keywords:
  - model fidelity
  - LinQ
  - TPU
  - ONNX
  - onnx_direct
  - GraphDef
  - QuantizedModel
  - QM
  - pytpu
  - PTQ
  - QAT
  - QDQ
  - calibration
  - percentile
  - mixed precision
  - Ultralytics 8.3.230
  - custom nc
  - BCN BNC final6
  - NMS
  - RT-DETR-l
  - RTMPose SimCC
  - ByteTrack
  - PTS
  - timely event recall
  - false alerts per camera-hour
  - paired cluster uncertainty
  - non-inferiority
  - AR01
entity_schema:
  experiment:
    fields:
      - id_status
      - decision_owner
      - inputs_boundary
      - procedure_evidence
      - outcomes_limits
    location: experiment-program
    note: "Comparison tables elsewhere are explanations, not homogeneous entity catalogs."
takeaways:
  - "Begin with one supplier-supported unchanged completed-device smoke and an immutable source/tensor baseline; CPU/RTX or compile success cannot establish LinQ quality."
  - "Check semantic adapters and float import before attributing loss to INT8; retain every parent and adjacent plus source-to-final deltas."
  - "Ultralytics 8.3.230 provides a source-coherent Detect/Pose example, not acquired weights or a verified LinQ route; custom nc and final6 collisions require explicit schema admission."
  - "LinQ native PTQ is documented; current percentile semantics, QDQ/encodings preservation, matching QAT and precision islands remain UNK pending Q006/Q007 and E006/E007."
  - "Independent absolute candidate quality, paired non-inferiority, causal event/delivery and device evidence are separate gates; no universal 1%, 1 FPS or sufficient calibration N is established."
  - "All E001-E012 are PROPOSED/UNRUN. After E001 and Q001-Q003, prioritize E002, E003 and E005 after E004; catalog-only access may make E005 unavailable."
checked_at: "2026-10-24T00:04:32+03:00"
timezone: Europe/Moscow
checked_at_meaning: "Local authoring/evidence-record inspection time; no new source retrieval or model verification. Source access dates remain those in SOURCES.md."
context_version: mosprom-research-v1
case_availability:
  full_case: _WORK/INPUT/CASE_LINQ.pdf
  pages: 20
  sha256: 7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e
  provenance: "Root read all 20 pages visually; W2-07 separately read pages 5/7/13/19 from existing renders. Both share the same PDF provenance."
  target_grant: NOT_RECEIVED
  matched_sdk_runtime_device_bundle: NOT_RECEIVED
  selected_weights: NOT_RECEIVED
  independent_ground_truth: NOT_RECEIVED
actual_checks:
  - "Saved documents, static source and artifact metadata were read during two research waves; local case hash/visual observations are attributed in S001-S004."
  - "This compression uses saved evidence only; YAML, relative links/anchors/IDs and strict UTF-8 were checked during authoring."
execution_state:
  model_export_import_ptq_qat_compiler_device_quality_runs: NONE
  experiments: PROPOSED_UNRUN
  measured_values: NONE
  acceptance_policy: TEAM_DECISION_PENDING
human_report: report_human_model_fidelity_quantization.md
evidence_files:
  - SOURCES.md
  - RAW_FACTS.md
  - CRITIC.md
  - OPEN_QUESTIONS.md
open_questions_file: OPEN_QUESTIONS.md
---

# Model fidelity and quantization: engineering decisions

<a id="evidence-state"></a>
## Evidence state and applicability

**No successful transfer, accuracy, FPS, GPU-memory fit or target compatibility is claimed.** The saved evidence comprises 188 sources, 250 facts, 19 open questions, 12 proposed experiments and 11 critic findings. W1 contained 15 tasks (12 general / 3 LinQ); W2 contained 7. Those are research tasks, not model runs. Source access is dated 2026-10-23 Europe/Moscow; finishing this English text does not refresh those sources. [F002](RAW_FACTS.md#F002), [S004](SOURCES.md#S004).

Evidence labels: **DOC** = primary documented interface; **CODE** = static source/metadata observation; **CLAIM** = vendor/author statement, including an unverified reported run; **PUB** = attributable published measurement with its own conditions; **OBS** = our actual local observation, restricted to the stated hash/read/metadata/arithmetic activity; **INF** = inference from cited evidence; **PROPOSED** = future procedure; **UNK** = unresolved. Execution status is independent: reading DOC/CODE/PUB does not change **UNRUN**. All E001–E012 are **PROPOSED / UNRUN**. Other topics' experiments remain secondary evidence with their original topic/date/scope. [F003](RAW_FACTS.md#F003).

The full case is available. Root checked its hash and visually read all 20 pages; W2-07 independently read pages 5/7/13/19 from existing renders. This is additional reading within one document provenance, not independent document confirmation. The case requires useful timely evidence-backed alerts, duplicate suppression, LinQ neural inference and speed measurement; it permits prioritizing scenarios. It establishes no universal mAP, recall, quantization loss, minimum FPS, deadline D or statistical α. The team's CPU+TPU/no-GPU server and uploaded-file processing account is a **working assumption**, not an observed grant; “even 1 FPS” is oral context. [S001](SOURCES.md#S001), [S002](SOURCES.md#S002), [S003](SOURCES.md#S003), [F001](RAW_FACTS.md#F001), [F249](RAW_FACTS.md#F249).

**Recommended admission order (INF/PROPOSED):** obtain one matched supported bundle and unchanged known input/output; demonstrate completed device inference; freeze exact source weights and input tensors; compare preparation → same-dtype ONNX → same-dtype alternate runtime → supplier float import → native quantized reference → compiler/device. Independently check media adapters, task quality, causal tracking/events and visible delivery. Prefer a fixed batch=1/static FP32/no-extra-simplification/no-graph-NMS first custom route **only if the actual importer accepts it**. Opset is a supplier constraint, not a guessed 13. [F154](RAW_FACTS.md#F154), [F205](RAW_FACTS.md#F205), [F206](RAW_FACTS.md#F206), [F212](RAW_FACTS.md#F212), [Q001](OPEN_QUESTIONS.md#Q001).

<a id="source-golden-contract"></a>
## Source, golden tensors and independent ground truth

**Preserve both A↔B fidelity and A→GT/B→GT absolute quality.** A is the source model in its native runtime; B is a candidate; a parent is an immutable artifact immediately before one change. Source predictions are not independent GT. An exact copy of a source that cannot see a phone remains unsuitable for that task. [F006](RAW_FACTS.md#F006), [F145](RAW_FACTS.md#F145), [F152](RAW_FACTS.md#F152).

The proposed source contract records checkpoint bytes/hash, architecture/config/source commit, license, actual load log and missing/unexpected keys, EMA/fusion/eval/BN/dropout state, task/head/end2end, class meanings/nc/order, skeleton/K/D/visibility, dependencies/build/device/driver, compute policy, accepted B/H/W/dtype, every output role, preprocessing/decoder/NMS, tracker/rules/zones/sampling and evaluator. `strict=False` can accept partial loading; `eval()` changes dropout/BatchNorm. Filename and architecture do not establish model identity. Incomplete history remains “known since acquisition”; pretraining/test overlap can remain UNK. [F004](RAW_FACTS.md#F004), [F005](RAW_FACTS.md#F005), [F011](RAW_FACTS.md#F011), [Q003](OPEN_QUESTIONS.md#Q003).

Maintain two different fixtures:

1. **Same-tensor:** immutable exact input bytes/hash/shape/layout/dtype/range plus all native source outputs before decoder. This isolates numerical/model boundaries. ONNX `ReferenceEvaluator` can generate missing expected `output_i.pb` from the ONNX model itself; label those **ONNX-derived**, separately from **source-runtime expected**. They cannot validate the export against PyTorch. [F007](RAW_FACTS.md#F007), [F008](RAW_FACTS.md#F008).
2. **Complete-media:** original frame/clip bytes, decoded canonical pixels, transform ledger, source PTS/time_base/epoch, canonical detections/pose, tracks/events and delivery evidence. This tests media→alert behavior. A same-tensor PASS leaves this path untested. [F057](RAW_FACTS.md#F057), [F064](RAW_FACTS.md#F064), [F189](RAW_FACTS.md#F189).

Measure repeatability inside each stack before selecting tolerances: same state/input/batch and fresh process. Seeds do not ensure equality across CPU/GPU, versions, batch kernels, TF32, reduced accumulation or nondeterministic operators. Do not automatically widen tolerance to conceal unstable source behavior. Pin actual deterministic/benchmark/autocast settings; `.half()` is not autocast. [F004](RAW_FACTS.md#F004), [F067](RAW_FACTS.md#F067), [F068](RAW_FACTS.md#F068), [F069](RAW_FACTS.md#F069).

**Golden pack is NOT_COLLECTED.** A proposed diagnostic budget is 24–40 real frames from independent incidents/sessions, 8–12 short causal clips and separately reviewed continuous negative intervals; these numbers establish neither representativeness nor statistical power. Materialize ordered actual IDs/hashes under E001. Suggested roles: normal person/machine and empty; odd landscape/portrait; tiny phone/PPE across distances; occlusion/wrong ownership/critical joints; real glare/shadow/dust/steam/blur/compression; zone crossings/short events; fall/lying versus bending/sitting if selected; persistent incident, two episodes/re-entry, EOF; continuous negatives and VFR/gap/reconnect. Synthetic RGB/ramp/rotation/axis/decoder fixtures have `origin=synthetic` and no industrial quality claim. [E001](OPEN_QUESTIONS.md#E001), [Q013](OPEN_QUESTIONS.md#Q013), [Q014](OPEN_QUESTIONS.md#Q014).

Every real sample needs owner/provenance, rights to process/annotate/store/show, camera/site/session/common-incident lineage and independent labels. Downloadability is not a license. Freeze **train / calibration / dev / sealed test before crops, sampling, augmentation or fit**; derivatives inherit parent groups, including synchronized cameras of one incident. Calibration inputs adapt the model even without labels. Dev includes threshold/recovery/sensitivity selection; reused debugging fixtures cease to be sealed test. New-camera claims require camera-heldout design; site-heldout and same-camera temporal holdout answer different questions. [F009](RAW_FACTS.md#F009), [F010](RAW_FACTS.md#F010), [F090](RAW_FACTS.md#F090), [F250](RAW_FACTS.md#F250).

<a id="fidelity-ladder"></a>
## Fidelity ladder: observable boundaries and rollback

**Find the first observable divergence, retaining both adjacent and source→final deltas.** Several small adjacent errors can accumulate. A hidden stage is UNAVAILABLE and the combined transition is confounded; it never receives an invented PASS. An observed boundary does not identify a kernel inside a fused region. All rows are proposed, unrun procedures. [F027](RAW_FACTS.md#F027), [F108](RAW_FACTS.md#F108), [F143](RAW_FACTS.md#F143).

| Boundary / required input | Observable and discriminating diagnostic | Continue or rollback / limit |
|---|---|---|
| Exact checkpoint/config→native source | Repeated all-output arrays, finite masks, load keys/eval/EMA/compute; fresh process and state reset | Establish stable identity first. Seed/repeatability is not GT accuracy. E001/E004 |
| Ordinary eager→prepared eager→same-dtype ONNX | Separate fusion/export flags/forward rewrite; both control-flow outcomes, accepted rectangular shapes and batch permutations | Revert first failing parent/pass. Checker/export success is not parity. E004 |
| ONNX→alternate same-dtype runtime; separately supplier float import | Exact tensors/all roles, provider/optimizations; one pass at a time; Identity/Transpose/Split and neural float comparison | Reject unsupported semantics without equivalent lowering. ORT PASS is not importer PASS. E004/E005 |
| Dtype-only child, if controllable | Initializer clipping/casts, finite/range/per-head errors, actual compute/accumulator policy | Revert converter or supported precision boundary. FP32 I/O does not mean FP32 internals. E004/E011 |
| Float→native quantized reference | Effective settings, W/A scales/zp/axis/tails; fresh models and fixed calibration/dev | Repair policy/coverage before supported recovery. Reconstruction MSE is not event quality. E006 |
| Same QM→compiler/TLM→device | Explicit target/preset/batch/descriptors, coverage, completed user/raw outputs and quant-reference deltas | Repair ABI/config/packing/completion before training. TLM timing is not TPU latency. E007 |
| Complete media→canonical detection/pose | Pixels/tensor hashes, geometry, raw/pre/post-NMS and exactly-once conversion; shared decoder | Fix adapter/transform owner and repeat downstream. Same-tensor success leaves media path open. E002/E008 |
| Fixed-schedule tracking/rules→actual scheduler→visible alert | B→B repeatability, first pool/assignment/FSM divergence, all GT, full terminal/delivery ledger | Require independent task/event/device/latency gates. AP/FPS alone cannot admit timely events. E009/E010 |

Detailed program and criteria: [E001–E012](OPEN_QUESTIONS.md#experiment-program); foundational boundaries: [F013](RAW_FACTS.md#F013), [F025](RAW_FACTS.md#F025), [F067](RAW_FACTS.md#F067), [F131](RAW_FACTS.md#F131), [F206](RAW_FACTS.md#F206), [F238](RAW_FACTS.md#F238).

<a id="input-output-geometry"></a>
## Input/output geometry, custom classes, pose and NMS

**A model loss claim requires identical semantics at both ends.** Assign one owner for decode/orientation/SAR/colorspace/range/layout/resize/interpolation/pad/crop/normalization/dtype. Record actual resized W/H, four pads and affine/crop history; `xywh` alone is ambiguous: distinguish cxcywh/tlwh/xyxy, normalized/model-input/source coordinates and continuous W/H boundaries versus last pixel W−1/H−1. Top-down crops need an actor-specific inverse. Torchvision wrappers may already normalize/resize internally. [F060](RAW_FACTS.md#F060), [F061](RAW_FACTS.md#F061), [F066](RAW_FACTS.md#F066).

CODE: OpenCV 4.10.0's inspected FFmpeg backend converts to BGR24 despite the `CONVERT_RGB` property name; other backends need their own checks. FFmpeg CLI autorotate/CFR may rotate or duplicate/drop frames; CLI behavior does not establish every libav/service consumer. Freeze actual decoded roster/PTS, not requested seek boundaries. [F063](RAW_FACTS.md#F063), [F065](RAW_FACTS.md#F065), [F194](RAW_FACTS.md#F194).

### Ultralytics 8.3.230: source-coherent worked contract, not a target run

CODE/PROPOSED: all internal helpers use commit `389b87f8cb9dbf2f31be8b70a94a3e47e11693db`; external PyTorch/ONNX/OpenCV/NumPy/torchvision builds and actual weights remain UNK. The proposed ordinary non-end2end Detect/Pose profile is `format="onnx", imgsz=(640,640), batch=1, dynamic=False, half=False, nms=False, simplify=False`; explicit opset follows actual importer admission. Input `images[1,3,640,640]` is FP32 RGB/255. Image preparation is explicit LetterBox `(640,640), auto=False, scale_fill=False, scaleup=True, center=True, stride=32, padding_value=114, interpolation=cv2.INTER_LINEAR`, then BGR→RGB/BHWC→BCHW/contiguous/FP32/255. Ready tensors bypass image conversion and must already satisfy the contract. [F206](RAW_FACTS.md#F206), [F207](RAW_FACTS.md#F207), [S018](SOURCES.md#S018), [S153](SOURCES.md#S153).

Wrapper trap: `pre_transform` uses `same_shapes && rect && (pt || (dynamic && !imx))`. `Model.predict` supplies `rect=True` despite `default.yaml rect=False`; same `imgsz=640` does not give equal `.pt` and static ONNX inputs. Freeze preprocessing or explicitly disable rect. [F207](RAW_FACTS.md#F207).

The ordinary no-NMS output is one `output0` in **BCN**: Detect `[B,4+nc,A]`, Pose `[B,4+nc+K*D,A]`. Boxes are **already DFL/box-decoded cxcywh in model-input pixels**; classes are independent sigmoid probabilities; **no objectness**. Pose xy is `(raw_xy*2+anchor−0.5)*stride`; D=3's third component is a sigmoid score, not depth or categorical GT visibility. Box/keypoint tails retain the same candidate identity. For the specific strides 8/16/32, 640² yields A=8400, 640×384 yields A=5040. Detect nc=1/2/3 gives C=5/6/7; K17,D3 Pose gives C=56/57/58. These are analytic source-derived shapes, not acquired checkpoint metadata. [F208](RAW_FACTS.md#F208), [S019](SOURCES.md#S019).

**Custom nc=2 collision:** correct `[1,6,8400]` BCN is not final detections. Incorrect transpose `[1,8400,6]` triggers NMS's early `shape[-1]==6` final-box shortcut; `nc=2,end2end=False` do not disable it. Rare A=6 also collides. Validate schema before calling NMS; never infer layout/nc from 84/85 or lastdim6. In the pinned third-party LinQ runner, 84/85-only normalization, first rank≥3 ndarray fallback, COCO80→91 mapping and exact Unicode typo `args.output_tensอร์_name` are static client findings, not reproduced exceptions or SDK defects. Fixing only shape does not fix class meaning/pose extras/multioutput roles. [F041](RAW_FACTS.md#F041), [F042](RAW_FACTS.md#F042), [F181](RAW_FACTS.md#F181), [F209](RAW_FACTS.md#F209), [S043](SOURCES.md#S043).

Analytic geometry fixtures (not neural measurements): G01 source853×481→640² resizes to640×361, pads L/T/R/B=0/139/0/140; G02 portrait481×853 gives361×640 and139/0/140/0; G03 explicit auto/stride32 gives640×384 and0/11/0/12. G04 clips source box `[−3,−2,855,483]` to `[0,0,853,481]`. Version8.3.230's xyxy box inverse uses rounded pad_y139, point inverse uses ≈139.55451348; fabricated input y200 becomes81.3015625 versus80.5625 source pixels, a .7390625 difference. Preserve the source's intended inverse or change both branches as a versioned policy. Unlike8.3.0, Pose boxes are **not rounded**, and executable `Results.Keypoints` does **not zero low-confidence xy**, despite stale docstrings. Image-only G01/G02 remain valid; annotation-path ratio_pad and G03 wrapper/G04 Pose expectations require the version-specific update. Pixel equality also requires external build equality. [F210](RAW_FACTS.md#F210), [F211](RAW_FACTS.md#F211).

### Model-family contracts and conditional fallback admission

| Source identity / status | Output and preprocessing semantics | LinQ limit / next decision |
|---|---|---|
| Ultralytics8.3.230 ordinary Detect/Pose; CODE, no weights | BCN4+nc(+K*D), decoded pixel cxcywh+sigmoid, explicit nc and one no-NMS output | Source contract only; E002/E004/E005 then native PTQ/device |
| YOLOv5v7.0; CODE | BNC5+nc, objectness×class and its own anchors/decoder; obj.5×class.8=.4, whereas v8 .8 stays.8 | No custom target proof; do not apply modern 84/85 heuristic. [F047](RAW_FACTS.md#F047) |
| torchvision FasterRCNN eval; CODE | List[Dict], internal normalization/resize/proposals/ROI/softmax/background0/class-wise NMS/postprocess | Explicit tested wrapper for pre-NMS access; operator admission remains open. [F055](RAW_FACTS.md#F055), [F061](RAW_FACTS.md#F061) |
| Original DETR commit `29901c51d7fe8712168b8d0d64351170bc0f83e0`; CODE | B×Q×(C+1) logits, softmax and remove no-object, normalized cxcywh→xyxy×W/H, normally no NMS | Different from RT-DETR sigmoid; float/schema gate required. [F054](RAW_FACTS.md#F054), [S050](SOURCES.md#S050) |
| RT-DETR-l/U8.3.230, candidate `rtdetr-l.pt`; CODE/PROPOSED | Static640/opset16 proposal; stretch `scale_fill=True`, RGB/255; BNC `[1,300,84]`, normalized cxcywh+sigmoid; ×original W/H, no external NMS/DFL | Internal TopK300/GridSample-16/attention remain neural operations; reject quick fallback if unsupported without equivalent lowering. [F241](RAW_FACTS.md#F241), [F242](RAW_FACTS.md#F242) |
| RTMPose-m/MMPose1.3.2+MMDeploy1.3.1; CODE/PROPOSED | Actor crop→RGB normalized `[1,3,256,192]`; raw `simcc_x[1,17,384]`, `simcc_y[1,17,512]`; host codec/inverse | Dependency/metadata/GAU/ScaleNorm/two-output/flip/schedule gates; no acquired weights/target proof. [F243](RAW_FACTS.md#F243), [F244](RAW_FACTS.md#F244) |
| Vendor `tiny_yolo3_b8_o5_128x128_asic.tpu`; CLAIM | Author's NHWC `[8,416,416,3]` float32 0..1, anchors/COCO adapter | Author reports done; actual program/results not received. Separate from custom YOLOv8. E003/E008. [F234](RAW_FACTS.md#F234) |

For RT-DETR-l the [weight locator](https://github.com/ultralytics/assets/releases/download/v8.3.0/rtdetr-l.pt) comes from source; bytes/hash were not fetched. GridSample-16 is bilinear/zeros/align_corners=False (`grid=2*sampling_locations−1`), and TopK/attention are internal; CPU postprocessing does not remove them. Opset13 is not a neutral replacement for this sampler. [F241](RAW_FACTS.md#F241), [S174](SOURCES.md#S174), [S175](SOURCES.md#S175), [S176](SOURCES.md#S176).

For RTMPose-m use config `rtmpose-m_8xb256-420e_coco-256x192.py`, MMPose commit `5408bc76f5b848cf925a0d1857899011d8c5b497`, MMDeploy commit `bc75c9d6c8940aa03d0e1e5b5962bd930478ba77`. The [final pose checkpoint locator](https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-m_simcc-coco_pt-aic-coco_420e-256x192-d8dd5ca4_20230127.pth) is not the backbone pretrain URI; bytes/hash remain unavailable. Host detector bbox→center/scale padding1.25→aspect192/256→TopdownAffine defines each crop/actor ledger. Normalize pixel0..255 with mean123.675/116.28/103.53 and std58.395/57.12/57.375, **no extra /255**. `create_input`'s dummy full-image bbox is not a detector pipeline. Decode axis argmax, score=min(axis maxima); score≤0 produces−1 coordinates, then split_ratio2 gives−.5 before inverse. No default softmax/DARK. Pin invalid/visibility policy and test affine inverse; for selected rotation0, `xy/input_size*input_scale+input_center−.5*input_scale`. [F243](RAW_FACTS.md#F243), [S177](SOURCES.md#S177), [S180](SOURCES.md#S180).

RTMPose admission is conditional: MMDeploy1.3.1 requirements pin mmpose1.0.0, but its backend inverse needs input_center/input_scale produced by the newer1.3.2 pipeline; old TopdownAffine omits them. Explicit dependency override/lock and registry/metadata smoke precede export. Stock SimCC config has fixed spatial input but dynamic batch; proposed B1 specialization sets `dynamic_axes=None` **before tracing**, not by rewriting metadata. Export `_forward` bypasses predictor flip TTA; choose source `flip_test=False` or separately implement/measure two TPU calls with correct left/right mapping. GAU/ScaleNorm/MatMul remain neural risks; detector+N crops costs must be measured. Generic single-output TRT INT8 pose config is not a ready SimCC/LinQ recipe. Changing pose adds no phone/cigarette/harness classes. [F243](RAW_FACTS.md#F243), [F245](RAW_FACTS.md#F245), [Q016](OPEN_QUESTIONS.md#Q016).

### NMS is a versioned quality policy

CODE/DOC: freeze confidence/IoU and strictness, class-aware/agnostic, multi-label/classes, sort/ties, pre-NMS and final caps, global versus per-class counts, valid-count/padding and time limits. Ultralytics8.3.230 uses strict score `>conf`; defaults conf.25/IoU.45/max_det300/max_nms30000/max_wh7680 and default time_limit `2+.05*B` are tool settings, not acceptance limits. In-place coordinate-view mutation requires raw dumps or independent copies **before** NMS. `torchvision` in `sys.modules` changes the branch; equal-score CPU/GPU selections can differ. A time-limit break may leave remaining batch items empty: that is incomplete processing, not a verified negative. Graph NMS and external/core NMS can differ in xyxy head mode, caps/multi-label/padding/trace-unrolled batch. [F049](RAW_FACTS.md#F049), [F050](RAW_FACTS.md#F050), [F053](RAW_FACTS.md#F053), [F209](RAW_FACTS.md#F209).

ONNX NonMaxSuppression-11 takes boxes[B,N,4]/scores[B,C,N], returns **int64 [batch,class,box] indices**. `center_point_box=0` uses y1,x1,y2,x2; =1 uses cxcywh; default `max_output_boxes_per_class=0` selects none. Gather/score lookup/sorting/global cap are separate. Probe t−ε/t/t+ε, IoU boundary, equal scores, overlapping classes, caps/valid counts/zero padding, and retained candidate IDs/unmatched objects. [F051](RAW_FACTS.md#F051), [F052](RAW_FACTS.md#F052), [E002](OPEN_QUESTIONS.md#E002).

<a id="exporter-graph-semantics"></a>
## Exporter/version matrix and graph semantics

**Pin the effective exporter and every graph parent; framework version alone is insufficient.** CODE/DOC: PyTorch2.9 defaults `dynamo=True`; optimize became default in2.7, and since2.6 constant folding is always enabled despite the deprecated flag. Ultralytics8.3.230 explicitly uses legacy export/`dynamo=False` for torch≥2.4. Legacy trace captures executed tensor operations; non-Tensor arguments, Python bool/`.item()`/shape branches can specialize. `dynamic_shapes` applies to dynamo, `dynamic_axes` to legacy; symbolic metadata cannot restore uncaptured control flow. `torch.cond` refactoring requires both-branch/target validation. [F013](RAW_FACTS.md#F013), [F014](RAW_FACTS.md#F014), [F015](RAW_FACTS.md#F015), [F023](RAW_FACTS.md#F023), [S012](SOURCES.md#S012), [S017](SOURCES.md#S017).

Ultralytics prepares deepcopy→eval→float→fuse, Detect export flags, C2f forward_split and dry runs. `simplify=False` disables onnxslim, not preparation/folding. Source eager→prepared eager must be checked separately. The exporter can lower IR header to10; retain actual serialized bytes and audit behavior rather than treating header editing as compatibility proof. NMS dynamic batch can still be bounded by traced loop/unroll/padding. [F018](RAW_FACTS.md#F018), [F021](RAW_FACTS.md#F021), [F022](RAW_FACTS.md#F022), [F206](RAW_FACTS.md#F206).

| Transformation / version scope | Discriminating probe and safe action |
|---|---|
| ONNX IR versus operator-set/domain/schema version | They evolve independently. Inventory actual ops/attributes/dtypes; never only relabel `ir_version`/`opset_import`. Shape inference is incomplete; unknown shape is not itself proof of bad model. [F025](RAW_FACTS.md#F025), [F026](RAW_FACTS.md#F026) |
| Softmax11→13 | Rank>2 normalization differs even for the same explicit axis;11 flatten-to-2D/default1 versus13 direct-axis/default−1. Probe DFL/attention/class axes. [F029](RAW_FACTS.md#F029) |
| Resize/scales→sizes | Equal H/W need not preserve sample centers. Ramp/impulse/odd/length1 probes; pin half_pixel/asymmetric/align_corners/pytorch_half_pixel, nearest rounding and schema-specific antialias. [F030](RAW_FACTS.md#F030), [F031](RAW_FACTS.md#F031), [F062](RAW_FACTS.md#F062) |
| Transpose/Reshape/Gather/Slice/Concat | Axis-index tensors; Reshape is not permutation. Check0/−1/allowzero, scalar versus vector indices/rank, negative steps, empties and branch order; update all axes/weights/shape tensors. [F032](RAW_FACTS.md#F032), [F033](RAW_FACTS.md#F033) |
| Conv/fusion/static specialization | SAME_UPPER/LOWER, odd padding/stride/dilation/group; cancellation/finite-mask fixtures. Export statically before capture when possible; metadata rewrite is a separate serialized parent. [F034](RAW_FACTS.md#F034), [F213](RAW_FACTS.md#F213) |
| Optimization/intermediate outputs | Portable graph separate from provider/hardware-optimized graph; debug instrumentation can change fusion/placement. Confirm diagnosis on unchanged deployment artifact. [F036](RAW_FACTS.md#F036), [F039](RAW_FACTS.md#F039), [F151](RAW_FACTS.md#F151) |

Tool bounds are not task gates: ONNX checker/full_check establish structure/shape consistency, not source parity. onnxsim0.4.36 `check_n=0` can return check_ok without numerical inference; its CPU sanity path uses `rtol=1e-4,atol=1e-5`. PyTorch2.9 verification uses example inputs and arbitrary internal warning thresholds max_abs `5e-3` / max_rel `1e-1`. Record actual checked inputs/status, then apply approved independent budgets. [F017](RAW_FACTS.md#F017), [F024](RAW_FACTS.md#F024), [F027](RAW_FACTS.md#F027), [F028](RAW_FACTS.md#F028).

PUB: ORT1.31.0 issue authors reported FP16 Conv→Add→Cast→Reciprocal finite→Inf after ConvAddFusion and Range/Gather negative-step failure after GatherToSliceFusion; disabling the specific pass restored their examples. These are external reproductions, not ours, not all ORT versions, and not LinQ defects. They justify isolated passes/portable parents. [F037](RAW_FACTS.md#F037), [F038](RAW_FACTS.md#F038), [issue33345](https://github.com/microsoft/onnxruntime/issues/33345), [issue33358](https://github.com/microsoft/onnxruntime/issues/33358).

<a id="floating-numerics"></a>
## Floating format, converter policy and execution are different factors

**Inspect conversion before blaming INT8.** DOC/CODE: equivalent FP32 expressions may differ because of summation/fusion/batch kernels/TF32/accumulation; fusion can also improve local rounding. onnxconverter-common1.16.0 clips constants before casting, using `min_positive_val=1e-7,max_finite_val=1e4` with sign preserved (zero/NaN/Inf preserved). These are converter policy, not FP16 representational limits. `keep_io_types=True` inserts boundary casts rather than making internals FP32. BF16 trades wider range for coarser mantissa; shifted softmax prevents exponential overflow but cannot recover rounded logits. Storage dtype is not compute or accumulator dtype. [F067](RAW_FACTS.md#F067), [F071](RAW_FACTS.md#F071), [F072](RAW_FACTS.md#F072), [F074](RAW_FACTS.md#F074), [F077](RAW_FACTS.md#F077).

Diagnostics start with output roles/shapes/dtypes/index exactness and finite masks, then per-semantic-head/channel abs/relative error distributions/ranges/worst IDs, decision margins, matched/unmatched objects and GT. State units: source pixels/model pixels/scores. `isclose(a,b)` uses `abs(a-b)<=atol+rtol*abs(b)` and is asymmetric; report absolute error near zero. Cosine=1 under positive scaling can coexist with threshold flips. Matched-only mean IoU hides lost objects. SQNR `20log10(norm(reference)/norm(diff))` is higher-better despite an API name containing “err”; do not treat it as AP/recall. [F075](RAW_FACTS.md#F075), [F108](RAW_FACTS.md#F108), [F109](RAW_FACTS.md#F109), [F145](RAW_FACTS.md#F145).

CODE/UNK: converter1.16.0 ModelProto `auto_convert_mixed_precision(model,feed_dict,...)` hardcodes CPU sessions. Its separate `auto_convert_mixed_precision_model_path(source_model_path,input_feed,target_model_path,provider,...)` passes provider to baseline and trials. ORT1.23.2 can insert FP16→FP32 CPU casts for eligible unassigned nodes; some CPU ops support FP16, others do not. Thus “CPU FP16 graph impossible / GPU always required” is too broad. Converter does not pin ORT; these versions were statically compared, not jointly run. CPU validation may test different compute than CUDA and proves neither native FP16 speed nor LinQ precision. Search feed_dict is tuning data. [F225](RAW_FACTS.md#F225), [F226](RAW_FACTS.md#F226), [F227](RAW_FACTS.md#F227), [F228](RAW_FACTS.md#F228), [F229](RAW_FACTS.md#F229), [Q019](OPEN_QUESTIONS.md#Q019).

<a id="ptq-calibration"></a>
## PTQ: calibration method, data and effective configuration

**“INT8” and “percentile” do not identify a numerical contract.** Record W-only versus W+A, per-tensor/channel/axis, signedness/symmetry, W/A/bias/accumulator types, scales/zp, rounding/clipping/saturation/requantization and actual kernel coverage. Weight-only float-activation paths are distinct from W8A8. Range selection trades clipping rare signals against coarser resolution elsewhere; more samples may improve coverage while adding extrema. Determine whether a tail is a decode/normalization error, irrelevant domain or essential rare case. There is no established universal best calibrator or sufficient N. [F079](RAW_FACTS.md#F079), [F087](RAW_FACTS.md#F087), [F088](RAW_FACTS.md#F088), [F089](RAW_FACTS.md#F089).

| Implementation / evidence scope | Mechanism and configuration that must be preserved | Limit |
|---|---|---|
| ORT1.22.0; CODE/DOC | INT8 MinMax/Entropy/Percentile paths; activation histogram; quantize_static defaults QDQ/per_channel=False/MinMax; Percentile factory99.999 versus docstring99.99 | Record factory/effective W/A settings and provider. Not a LinQ formula. [F080](RAW_FACTS.md#F080), [F081](RAW_FACTS.md#F081) |
| NNCF2.17.0/OpenVINO2025; CODE/DOC | Per-sample statistic plus cross-sample aggregation, separate W/A estimator settings; sample unit/batch/reduction axes/quantile/aggregator/subset/backend | `MIXED` means symmetric weights/asymmetric activations, not FP16/INT8 islands; subset300 is a default, not sufficiency. [F082](RAW_FACTS.md#F082), [F083](RAW_FACTS.md#F083) |
| TF2.20/LiteRT; CODE/DOC | Representative signatures/names/dtypes, inspected MinMax accumulation, operator-specific scales/bias; actual supported_ops/I/O/coverage | Float fallback may remain; integer-only needs explicit verification. Tutorial take(100)/eval overlap is not our data design. [F085](RAW_FACTS.md#F085), [F086](RAW_FACTS.md#F086), [F087](RAW_FACTS.md#F087) |
| LinQ guide2025 and third-party RegularModel client; DOC/CODE/UNK | Native data-dependent PTQ is documented. Guide percentile prose concerns weights, default100.0; formula/tails/domain/current effective object remain unknown | No evidence for activation histogram equivalence, “100=no clipping”, generic KL/MSE API or per-channel support. [F173](RAW_FACTS.md#F173), [F214](RAW_FACTS.md#F214), [F215](RAW_FACTS.md#F215) |

Tensor MSE is a useful diagnostic; it does not establish a generic MSE-calibrator API in the inspected selectors. Capture calibration input hashes/order/count/groups/camera/light/scale/pose/empty/hard-negative coverage and preprocessing. Top-down pose calibration uses actual normalized person crops. N calibration examples and compiled batch B are different axes. Adjacent duplicates add little diversity; first sorted500 and preparation chunk128 are client defaults, not manufacturer recommendations or streaming/RAM guarantees. [F083](RAW_FACTS.md#F083), [F176](RAW_FACTS.md#F176), [F177](RAW_FACTS.md#F177), [F243](RAW_FACTS.md#F243).

**Effective-setting admission precedes sweeps.** The pinned LinQ client catches every TypeError then recalibrates without percentile; error may originate inside a supported call after state mutation. CLI differences do not prove different policies. Fail closed, use fresh models and retain first traceback/requested→passed→resolved/effective values/encodings. Proposed E006 uses two **documentedly valid** P settings×two frozen distributions with distinct tails, fresh model per cell and two fresh repetitions of one cell. Changed activation thresholds can be mediated by changed weights; direct activation-percentile causality requires a supported frozen-weight intervention or implementation trace. No observed effect on an insensitive probe does not prove an ignored option. [F175](RAW_FACTS.md#F175), [F214](RAW_FACTS.md#F214), [F216](RAW_FACTS.md#F216), [E006](OPEN_QUESTIONS.md#E006), [Q006](OPEN_QUESTIONS.md#Q006).

On dev, vary one factor: group composition at fixed N; nested N with fixed order; method with identical data; order/cache/fresh model with fixed policy. Preserve float parent, effective W/A encodings, bounds/tails/clipping, save→fresh-process-load outputs and task/event deltas. Endpoint-hit fraction is not clipping; byte-hash changes alone do not prove numerical serialization loss. Hidden implementation limits attribution rather than authorizing an assumed ORT algorithm. [F173](RAW_FACTS.md#F173), [F185](RAW_FACTS.md#F185), [Q015](OPEN_QUESTIONS.md#Q015).

<a id="recovery-admission"></a>
## Recovery admission: supported consumer before GPU work

**Do not train an artifact whose target arithmetic cannot be preserved.** For LinQ, external QDQ/encodings import/preservation, a native matching QAT simulator, freeze/bypass recalibration, allowed precision islands and neural CPU placement remain **UNK**. Parser/compile acceptance may fold/recalibrate/requantize; it does not establish numerical preservation. E007 must admit a concrete supported route before QAT/correction investment. This is absence of evidence, not proof that these features do not exist. [F091](RAW_FACTS.md#F091), [F105](RAW_FACTS.md#F105), [F219](RAW_FACTS.md#F219), [F221](RAW_FACTS.md#F221), [F222](RAW_FACTS.md#F222), [F224](RAW_FACTS.md#F224), [Q007](OPEN_QUESTIONS.md#Q007).

| Method / access and data | Benefit evidence / cost and risk | Admission and verification |
|---|---|---|
| Fix preprocessing/schema/float pass; source/config/tensors/code | PROPOSED: removes the localized semantic error without training; changed policy can create another mismatch | E002/E004/E005, repeat affected downstream gates |
| Native PTQ; representative unlabelled calibration plus separate dev/test and actual quantizer | DOC: data-dependent ranges; own gain UNK; tails/cache/axis/leakage risks | E006 effective policy→E007→independent E008/E009 |
| Selective precision; localized block and supported Q→FP→Q/placement | PUB partial recovery exists; repeated ranking/evaluation, transfers and lost fusion may cost latency | Node exclusion ≠ output exclusion ≠ consumer-specific QDQ. Actual names after fusion, shared/residual boundaries and compiled precision matter. E007/E011 |
| Bias correction/CLE; representative data, algebraically valid scaling | Corrects mean, not variance/clipped signal. AIMET2.20 correction disables activation quantizers and removes wrappers; SiLU/GELU/branches need proof | One correction ablation, serialize/recompile and independent task/event gate. [F099](RAW_FACTS.md#F099), [F100](RAW_FACTS.md#F100) |
| AdaRound; stable grid/scales/folding, unlabelled reconstruction | Optimizes weight rounding; changing grid later changes the problem; does not automatically repair activation clipping | AIMET2.20 ONNX notebook is a classification example, not detector/pose/LinQ proof. E007 stable encodings→E011. [F095](RAW_FACTS.md#F095), [F096](RAW_FACTS.md#F096) |
| BRECQ; architecture-specific blocks/cache/CUDA optimization | PUB low-bit detector recovery; original adapters cover ResNet/MobileNet/RegNet patterns, not arbitrary modern YOLO/attention/ROI/pose; memory/time UNK | Bounded architecture pilot and full export/import/compile/device round trip. [F097](RAW_FACTS.md#F097), [F098](RAW_FACTS.md#F098) |
| QAT; trainable source, labels or aligned teacher, matching simulator/consumer/export | PUB recovery exists; extra optimizer/backprop/observer/range-learning memory; BN/observer/checkpoint semantics and import may erase learned ranges | E007 before GPU; measured resource pilot, preserved numerical contract and independent E008/E009 after winner freeze. [F092](RAW_FACTS.md#F092), [F093](RAW_FACTS.md#F093) |
| Distillation/QAD; good teacher and task-specific class/query/anchor/joint/feature alignment | Mechanism documented; retrieved ModelOpt evidence mainly LLM, not our CV gain. Teacher adds compute/cache and can reproduce wrong predictions | Not arbitrary KL on post-NMS rows; validate GT/task loss/target contract. [F103](RAW_FACTS.md#F103) |
| ROI/tiling/input change; raw detail, merge/schedule/CPU permission | May preserve tiny information; new calls/seams/duplicates/lost context/large people; SAHI aerial AP50 is another domain | New system policy reopens geometry/task/event/latency E002/E008–E010. [F120](RAW_FACTS.md#F120), [F122](RAW_FACTS.md#F122) |
| Alternate exact checkpoint; weights/license/lock/operator/decoder admission | Can change baseline quality/compatibility; LinQ advantage unmeasured | RT-DETR/RTMPose blockers must pass before training; full ladder repeats. [F245](RAW_FACTS.md#F245) |

CODE/DOC: ORT exact node exclusions and NNCF2.18 accuracy control provide examples of controls needed, not LinQ APIs. NNCF accuracy-control dispatch covers OpenVINO/ONNX; ordinary quantize support elsewhere does not extend that API. `ONLY_ACTIVATIONS` is not a fully float block. QDQ may move/fuse; float storage does not prove float compute. Raising a head's precision after upstream quantization cannot restore lost information; block effects are not additive. [F106](RAW_FACTS.md#F106), [F107](RAW_FACTS.md#F107), [F111](RAW_FACTS.md#F111), [F113](RAW_FACTS.md#F113), [F117](RAW_FACTS.md#F117).

PROPOSED E011 budget: up to six semantic regions plus at most two boundary/interaction probes, then one justified correction or separately admitted QAT pilot. Team may change this **before** running; it is an organizational bound, not scientific sufficiency. Count ranking/calibration/evaluation/cache/serialization/export/compile/device and billable time, not only optimizer steps. Two RTX3090 do not pool into48GB; no24GB fit or N-hour promise is established. Measure allocated/reserved VRAM/RAM and steady step/eval/export/compile costs on the actual host/model/data. [F104](RAW_FACTS.md#F104), [Q017](OPEN_QUESTIONS.md#Q017), [E011](OPEN_QUESTIONS.md#E011).

### Published quantitative outcomes: external, not target predictions

| Published scope | Numbers and reported recipe | Decision supported / unresolved conditions |
|---|---|---|
| Wu et al., EfficientNet-b0, TF weights→PyTorch, ImageNet2012 val,224²,1024 train calibration; W8A8 compute, other ops usually float | Top1%:76.85 float→72.06 PTQ; partial76.35 excludes10/82 Conv; **separate** QAT76.95 from best PTQ,15epochs/SGD1e−3/B256 | Partial/QAT can help even INT8; not a sequential partial→QAT run or proof of regularization. Checkpoint hash/software/hardware/eval batch/GPU-hours unknown. [F230](RAW_FACTS.md#F230), [S086](SOURCES.md#S086) |
| BRECQ FasterRCNN-R50/COCO,256 train calibration,resize800/max1333,B32,20000iter/block | mAP0–100:38.55float; W4A8 bias correction*0.25/AdaRound*37.58/BRECQ38.29; BRECQ W8A8 38.54,W2A8 34.23 | Independent recipes, not a recovery sequence; low-bit gain does not imply equal gain for good INT8. Coverage/exclusions/eval split/hash/software/hardware/wall-time unknown. [F231](RAW_FACTS.md#F231), [S093](SOURCES.md#S093) |
| MMDeploy1.3.1 accuracy table,YOLOX-s/COCO2017 | Box AP40.5 PyTorchFP32;40.3TRT-FP32;40.3FP16;29.3INT8 | Deployment can have large loss. Accuracy input/batch/hardware/calibration unknown; latency row is YOLOX-tiny, so its416/T4 setup cannot fill these fields. [F232](RAW_FACTS.md#F232), [S167](SOURCES.md#S167) |
| MMDeploy0.14/ncnn,S-ViPNAS-MobileNetV3,flip_test=False,linked256×192 config | Keypoint AP0–1:.687float→.683INT8; Wholebody.459→.445 | Direct pose INT8 measurement exists in this limited scope; not RTMPose/YOLOPose or fall-event evidence. Exact weights/split/ncnn/MMPose/hardware/calibration/coverage unknown. [F233](RAW_FACTS.md#F233), [S168](SOURCES.md#S168) |

Primary measurement sources: [Wu](https://arxiv.org/pdf/2004.09602v1), [BRECQ](https://arxiv.org/pdf/2102.05426v2), [MMDeploy1.3.1](https://github.com/open-mmlab/mmdeploy/blob/v1.3.1/docs/en/03-benchmark/benchmark.md), [MMDeploy0.14](https://github.com/open-mmlab/mmdeploy/blob/v0.14.0/docs/en/03-benchmark/quantization.md). No reproduction or measured local benefit was performed.

<a id="small-pose-temporal"></a>
## Small objects, occluded pose and causal event propagation

**Check observability and class meaning before numerical rescue.** COCO has cell phone, not cigarette/safety harness; actual custom weights/classes are not known. Precision repair cannot create a missing class or recover detail eliminated at resize. Record object size in source/input/crop pixels. DARK addresses coordinate discretization, not evidence for INT8-weight recovery. [F123](RAW_FACTS.md#F123), [F130](RAW_FACTS.md#F130).

Stress slices follow decision logic: tiny phone at wrist, partial person, foot at zone edge, critical wrist/hip/ankle, two overlapping actors and object/joint ownership, rare lighting/blur. Report missing people as well as matched joints. COCO pose summary lacks a default small-pose result; GT v=1 annotated occluded and v=2 visible need separate slices; pin skeleton/order/sigmas/scale. Good average OKS can hide the critical joint or correct coordinates assigned to the wrong actor. SAHI0.11.18 defaults GREEDYNMM/IOS plus full-image pass, unlike paper NMS; paper aerial results are not industrial INT8 evidence. [F121](RAW_FACTS.md#F121), [F122](RAW_FACTS.md#F122), [F124](RAW_FACTS.md#F124), [F126](RAW_FACTS.md#F126), [F127](RAW_FACTS.md#F127), [F146](RAW_FACTS.md#F146).

PROPOSED trace: `raw candidate → threshold/NMS → tracker pool → association → physical actor → predicate → FSM → notification`. Score drift changes low/high/new-track pools, bbox jitter changes crossing, joint drift changes angle/predicate, dropout interrupts confirmation, ID switches duplicate or transfer history. Pin each policy and retain first divergent decision. [F131](RAW_FACTS.md#F131), [F132](RAW_FACTS.md#F132), [F141](RAW_FACTS.md#F141).

CODE: original ByteTrack uses low-score recovery; an aggressive pre-tracker cutoff destroys it. `frame_id+=1`, Kalman `dt=1`, while frame_rate scales buffer; setting frame_rate=1 does not make physical-time/VFR-aware tracking. In the inspected implementation equality at `track_thresh` falls outside both strict pools. BoT-SORT adds a ReID NN and CMC, requiring additional input/weight/device lineage. Compare actors/continuity against GT, not numeric ID equality. [F133](RAW_FACTS.md#F133), [F135](RAW_FACTS.md#F135), [F136](RAW_FACTS.md#F136).

Use source `PTS*time_base`, timestamp provenance and stream epoch; PTS is normally neither UTC nor monotonic. Declare a clock mapping/uncertainty for onset→visible-alert latency. Separate confirmation duration, maximum observation gap, clear duration, hysteresis, cooldown and dedup key. Kalman prediction is not an observation of a phone/pose; insufficient evidence should yield UNKNOWN under an approved policy. Reconnect/EOF/reset/drain/late reply closure must be explicit. [F064](RAW_FACTS.md#F064), [F137](RAW_FACTS.md#F137), [Q011](OPEN_QUESTIONS.md#Q011), [Q012](OPEN_QUESTIONS.md#Q012).

E009 first compares A/B on identical roster/source schedule/frozen downstream, after B→B harness repeatability. Scores-only/boxes-only/fixed-crop oracle interventions are diagnostic, not production performance or additive causal decomposition. E010 separately runs unchanged predictions/rules through actual sampling/queue/load/delivery. Future-endpoint interpolation (including ByteTrack's offline interpolation) and backdated alerts cannot count as online timely TP. Temporal NNs additionally need physical window duration, causal/noncausal mode, padding/missing masks and hidden-state reset; same frame count at another FPS changes context. [F134](RAW_FACTS.md#F134), [E009](OPEN_QUESTIONS.md#E009), [E010](OPEN_QUESTIONS.md#E010).

**1 FPS is scenario dependent.** Hypothetical ideal point-sampling with uniform random phase, intervalΔ and duration d has at-least-one-hit probability `min(1,d/Δ)` and k-hit probability `clamp(d/Δ−(k−1),0,1)`. For d=.2s at1FPS the first probability is.2; adverse phase can miss entirely. This is analytic coverage, not measured recall or an established phase distribution. Detection/occlusion/confirmation add losses. Predeclare rates×phases/burst gaps; count **all GT episodes**, including those wholly missed by sampling. [Temporal protocol](RAW_FACTS.md#engineering-annex), [E010](OPEN_QUESTIONS.md#E010).

<a id="linq-route-access"></a>
## LinQ documented chain, version seams and access scenarios

**A documented native route exists; the granted compatible environment is unknown.** DOC: [Framework manual H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf),2025, `RU.РМДВ.04.06.014-03 34 01`, describes `ONNX → TensorFlow GraphDef → QuantizedModel (.qm) → Network → compile → .tpu → runtime → TPU`. Researchers read its complete extracted text; original PDF bytes/visual verification were unavailable. Signature/prose discrepancies can be extraction/document issues and are not established SDK bugs. The vendor performance PDF has similar extraction-only provenance; the full case PDF is a separate locally verified document. [S133](SOURCES.md#S133), [S137](SOURCES.md#S137), [F154](RAW_FACTS.md#F154), [F159](RAW_FACTS.md#F159).

| Boundary / documentary evidence | Required actual admission artifact |
|---|---|
| Preparation host/model→ONNX | Exact source/exporter/lock and actual IR/opsets/domains/operators/attributes plus same-tensor source parity |
| `from onnx_direct import onnx_to_tf`→float TF | Actual distribution/module/callable/file/hash/signature, GraphDef and all value/port/layout mappings, float executor |
| TF→QM | Matching QuantizedModel/RegularModel API, calibration_dict, numerical policy/effective encodings, reference outputs and save/load |
| QM→Network→compiler | `compile_(hardware_parameters,network,parameters,slicing_scheme=None)`; explicit reference/compile targets/preset/batch, resolved config, tensor descriptions, coverage |
| `.tpu`→runtime→usable output | Matched compiler/runtime/pytpu/libtpu/driver/firmware, actual SKU/session/device, user/raw descriptors and completed request trace |
| Outputs→task/events | Actual file/media service, transform/decode/NMS owners, CPU responsibilities/extra NN placement, PTS and delivery closure |

DOC/UNK: the guide's preparation example is Linux CPU host (Ubuntu20.04/i7-7700/RAM≥32GB/Python3.11); it neither proves minimum hardware nor arbitrary Windows/ARM compilation. Documentary API names include `get_hw_params(tpu_type)`, `Device.list_devices`, `Device.open`, `device.load`, `program.inference` and `inference.sync(input_dict)`. These must be matched to the supplied release, not assembled into an assumed current recipe. No SSH/SCP/HTTP endpoint, credentials, upload authorization or actual tools follow from the documented local tensor runtime. [F153](RAW_FACTS.md#F153), [F155](RAW_FACTS.md#F155), [F156](RAW_FACTS.md#F156), [Q001](OPEN_QUESTIONS.md#Q001).

Version scopes must stay separate: guide2025 Python3.11; live software page Python3.8; pytpu15.0.24 metadata Python≥3.6; vendor benchmark Runtime16.18.6/Framework2026.8.43. Manual-03 follows-02 but no document→wheel→native release mapping was found. Fresh pytpu15.0.24 source already contains Device/Program/Inference despite old README `iva_tpu/TPUDevice`. `/usr/lib/libtpu.2.so` is lazy-loaded; Python import alone need not validate native presence/ABI. Obtain actual filenames/hashes/OS/arch/Python/TF/ONNX/NumPy/native lock and unchanged completed smoke. [F197](RAW_FACTS.md#F197), [F198](RAW_FACTS.md#F198), [F203](RAW_FACTS.md#F203), [F204](RAW_FACTS.md#F204), [F205](RAW_FACTS.md#F205), [Q002](OPEN_QUESTIONS.md#Q002).

DOC/CODE seams: guide `QuantizedModel.quantize(calibration_dict,...)`/`save(file_path)` versus client `RegularModel.calibrate→quantize`/`save(file_dir,file_name)`/tuple unpack from_quantized_model. Assignment to one name does not establish a non-tuple return; different facades may coexist. Extracted `as_graph` signature says64x64_fpga while prose says128x128_asic; explicit `TPU_128x128_PARAMS` at compile does not repair the separate reference default. DEFAULT/STAGING versus O1/O5 are not established aliases; STAGING warning includes wrong programs/long compilation. Use one matched supported preset and save resolved objects/config. [F199](RAW_FACTS.md#F199), [F200](RAW_FACTS.md#F200), [F201](RAW_FACTS.md#F201), [F202](RAW_FACTS.md#F202), [Q005](OPEN_QUESTIONS.md#Q005).

### Supplier float importer and exact output ports

UNK: public material did not reveal an implementation/versioned semantic contract for actual `onnx_direct.onnx_to_tf`. Public-name404/TLS failures do not prove absent private wheels or universal closure; onnx-tf/onnx2tf/unrelated onnx_direct are not interchangeable. The third-party build's broad imports/retries, static input metadata rewrite, first-output selection and stripped TF suffixes are client assumptions. [F212](RAW_FACTS.md#F212), [S139](SOURCES.md#S139), [Q004](OPEN_QUESTIONS.md#Q004).

For **every** required output, record ONNX graph-output ordinal/Value name/producer node+output index/dtype/shape/role → actual TF tensor **including port**/layout/inserted transforms → QM/TPU user/raw name/index/shape/layout/dtype/bytes/packing/scales. ONNX node and Value namespaces differ; TF `output:1` is not operation `output`, and ONNX `output0` does not prove TF `output0:0`. Ordinary selected Detect/Pose has one output each; segmentation/custom multihead/SimCC must preserve all roles. E005 first uses axis-coded Identity/Transpose and two-output Split, then the actual neural graph. Micrograph PASS does not cover the full operator inventory. Hidden float execution makes import+PTQ confounded, though end-to-end GT evaluation can remain possible. [F213](RAW_FACTS.md#F213), [E005](OPEN_QUESTIONS.md#E005), [Q015](OPEN_QUESTIONS.md#Q015).

### User format, RAW and completion

DOC/CODE: quantized TF reference examples rescale inputs/outputs; TLM/TPU examples use user-format tensors. Do not automatically apply TF rescale again to FULL device output. Historical byte pointers are addresses, not numerical INT8 declarations; `view(user_dtype)` reinterprets bytes and does not dequantize. Modes RAW0/PRE_PROCESS1/POST_PROCESS2/FULL3 differ from **RAW program** defined by missing user_dtype. Mode alone does not change metadata-controlled buffer interpretation. Historical `Codec.encode/decode` delegates to `tpu_tlm_is.models.iotools.tpu_encode/tpu_decode` with user/tpu shapes/order/dtypes/padding/scales/anchor and needs that internal dependency. It reveals no current arithmetic/availability; `astype(int8)`, generic scale or old FPGA formula is not a substitute. [F178](RAW_FACTS.md#F178), [F179](RAW_FACTS.md#F179), [F239](RAW_FACTS.md#F239), [Q008](OPEN_QUESTIONS.md#Q008).

DOC/CODE: guide calls `inference.sync` blocking; historical sync allocates buffers→native `tpu_run_inference`→reads output→checks `tpu_get_inference_status`. There is no separate visible Python barrier; native semantics must provide completion. The client's preferred `.run` does not inherit `.sync` guarantees. Timer must end after actual readiness/completion; timeout is not cancellation, and late results need attempt/job identity/idempotency. Current reset/cancel/retry/thread-safety and PRE/POST placement remain UNK. [F186](RAW_FACTS.md#F186), [F188](RAW_FACTS.md#F188), [F238](RAW_FACTS.md#F238), [Q008](OPEN_QUESTIONS.md#Q008).

### External LinQ results: what can and cannot be inferred

CLAIM/CODE: pinned `linq-cv-bench` author reports vendor TinyYOLO3 done; self-build YOLOv8 source has no available QM/TPU/build logs/metrics/predictions in checked complete trees/releases/Actions. Missing public artifacts do not refute an actual private run or prove failure. “expected VALID”, qps2000 and “strict” are not raw valid logs, measured speed or equal model hashes. TinyYOLO3 and self-build YOLOv8 are different architectures/input layouts/decoders; a bug in one runner does not refute the other route. [F234](RAW_FACTS.md#F234), [F235](RAW_FACTS.md#F235), [F236](RAW_FACTS.md#F236), [Q018](OPEN_QUESTIONS.md#Q018).

CLAIM/PUB: extracted official [performance presentation](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf) reports label `yolov8n_pose`,B1: HP104.8FPS/21.51ms; HPQ419.2FPS/21.51ms, on i7-10700K/Ubuntu24.04/Runtime16.18.6/Framework2026.8.43. Original visual table, exact weights/input/precision/AP/OKS, completed counts/timing boundaries and independent HPQ measurement are unknown. HPQ=4×HP does not establish our parallelism; `1000/FPS` does not reconstruct reported latency. A benchmark label is not custom-pose fidelity, stream capacity or SLA. [F237](RAW_FACTS.md#F237), [S137](SOURCES.md#S137).

CODE/INF: Python vendor direct adapter times runtime call only, conditional on blocking completion. Warmup10 images/B8 makes the second timed batch count6 useful images against time for8 slots; hypothetical N16/equal batch timing gives6/8=.75. N5000/no failures gives4990 useful counted images over4992 timed slots (≈.999599 under equal timing). These are source arithmetic, not benchmark measurements. Padding duplicates are not new frames. Native MLPerf is another path: Python warmup defect cannot be assigned to it or the vendor table. Its wrapper's weak VALID predicate/possible stale directory logs justify fresh run ID/config/full raw logs and successful exit code; they do not establish an observed invalid run. [F240](RAW_FACTS.md#F240).

### Access scenarios and claim boundaries

| Actual grant, still unknown | Action after inventory | Observable conclusion / remaining limit |
|---|---|---|
| Full SDK/compiler/runtime/custom models | Matched bundle, E003 unchanged smoke, E004–E007 and independent E008–E010 | Most ladder only where references/dumps exist. Does not promise float device/every-op dumps/islands/approved neural fallback |
| Restricted server/runtime/permitted custom artifact | Use actual endpoints/descriptors/logs, fixed files/IDs and exposed comparisons; do not change server without grant | Available output/GT/device evidence; hidden import/PTQ/compiler causality stays confounded. Mark NOT_EXPOSED only after actual inventory |
| Catalog/model service | Freeze service/model revision/request IDs/complete input-output census; service→GT E008/E009 and available attestation | Without exact source, no checkpoint fidelity; without completion/placement, own LinQ claim HOLD or explicitly limited supplier attestation |

All scenarios still require actual neural LinQ inference. CPU decode/geometry/NMS/Kalman/rules are proposed responsibilities requiring agreement; this does not authorize neural CPU fallback. Extra pose/ReID/temporal NNs each need lineage and an approved placement boundary. [F223](RAW_FACTS.md#F223), [Q001](OPEN_QUESTIONS.md#Q001), [Q009](OPEN_QUESTIONS.md#Q009), [E003](OPEN_QUESTIONS.md#E003), [E012](OPEN_QUESTIONS.md#E012).

<a id="acceptance-five-gates"></a>
## Acceptance: five independent gates, units and uncertainty

**No aggregate PASS exists until every required gate is supported in its declared scope.** PROPOSED gates are an engineering contract, not a LinQ standard. [Engineering annex](RAW_FACTS.md#engineering-annex), [F143](RAW_FACTS.md#F143), [F149](RAW_FACTS.md#F149), [E012](OPEN_QUESTIONS.md#E012).

| Gate | Required evidence / what PASS establishes | Does not establish |
|---|---|---|
| Source | Checkpoint/config/classes/skeleton/load/eval/fusion/EMA/lock/license/data/policy identity and repeatability | GT quality or target execution |
| Tensor | Same input bytes; all names/roles/ports/shapes/layouts/dtypes; finite masks, per-semantic numerical deltas | Independent accuracy, other shapes or complete media path |
| Task | Independent GT/canonical outputs/pinned evaluator/lost-gained-unmatched IDs/class-size-visibility slices | Correct event actor, continuity or delivery |
| Event | Continuous source PTS, independent actor/episode GT, frozen causal tracker/FSM, complete delivery census/exposure | Future safety or a different camera population |
| Device | Source/export/compiled/service lineage and coverage; input→job→device→completion→output correlation | Whole neural placement from a label/utilization/API response alone |

AR01 must be approved **before winner selection**: owner/approvers/date/version, chosen scenarios/cameras/conditions/actors/episodes/exclusions, minimum observable duration, deadline D and visible-alert boundary, evaluator/metric units, absolute B floors and cost/error caps, allowed paired lossδ, must-pass IDs, uncertainty estimand/design, α/sidedness/multiplicity and stopping rule. Current state: **TEAM_DECISION_PENDING** for policy, **DATUM_MISSING** for inputs/GT/device trace, **MEASURED=none**. Future unknown interface is not yet NOT_EXPOSED. [F249](RAW_FACTS.md#F249), [F250](RAW_FACTS.md#F250), [Q012](OPEN_QUESTIONS.md#Q012), [Q013](OPEN_QUESTIONS.md#Q013).

| Endpoint | Unit / split / denominator and acceptance use | Limit |
|---|---|---|
| Raw repeatability/error | Exact tensor/output role; debug/dev; absolute output units and explicit relative reference/finite masks; approved bounds after repeatability | Low error/cosine/SQNR is not GT quality; debug graph differs from deployment |
| Detection AP and frozen TP/FP/FN | Independent grouped test; evaluator/classes/ignore/maxDets/IoUs/size; scale0–1 or0–100; absolute B+paired loss+critical slices | Pooled AP is not mean frame precision; diagnostic Hungarian matching does not replace evaluator; no-positive recall undefined |
| Pose OKS/PCK/drift | Independent skeleton/order/sigmas/scale/visibility; source pixels or named normalization; unmatched people separately | Confidence is not universal visibility probability; mean OKS is not event continuity |
| HOTA/DetA/AssA/IDF1 | Independent continuous physical-identity GT, fixed reset/order/time and pinned evaluator | Numeric track-ID equality and counts are not quality; tracking score does not measure delivery |
| Useful timely event recall | **All GT episodes** in scope, correct actor/type/camera/zone, causal evidence, deadline and complete follow-up | Sampling misses remain FN; future interpolation/backdating is not timely TP; gained TP cannot conceal critical lost TP |
| False/duplicate visible alerts | Full adjudicated alert census / **union source-camera-hours** of declared reviewed exposure; duplicates separately | Curated balanced clips do not estimate natural prevalence/precision; silence without GT says nothing about recall |
| Throughput/latency | Completed real source IDs / precise interval, warmup/batch/padding/concurrency/boundary; p50/p95/p99+n+miss/late/timeout, frame age/max gap | Config QPS/enqueue/padded slots are not FPS; success-only p95 hides misses; unpaced replay is not live SLA |
| Device/coverage | Artifact/session/input/completion/output/device plus compile/partition evidence and extra NN branches | Inventory, label, utilization or CPU ndarray alone is not all-graph TPU execution |

Metric evidence: [F145](RAW_FACTS.md#F145), [F146](RAW_FACTS.md#F146), [F148](RAW_FACTS.md#F148), [F189](RAW_FACTS.md#F189), [F195](RAW_FACTS.md#F195), [F238](RAW_FACTS.md#F238), [F240](RAW_FACTS.md#F240).

PROPOSED non-inferiority: higher-better `Dq=qB−qA`, require `L(Dq)≥−δq` **and** absolute B floor. Cost `Dc=cB−cA`, require `U(Dc)≤δc` **and** absolute cap. Equivalence requires the entire CI within predeclared two-sided bounds; `p>.05` does not prove it. Confirmed invariant/budget violation→FAIL; missing policy/data→HOLD; CI spanning allowed and unacceptable regions or insufficient design/support→INCONCLUSIVE. UNAVAILABLE identifies an actually inaccessible stage. A weak source copy cannot pass the absolute gate. [F149](RAW_FACTS.md#F149), [F150](RAW_FACTS.md#F150), [F250](RAW_FACTS.md#F250).

Paired inference uses the **same eligible independent clusters** in A/B/GT, chosen for the estimand (site/camera-session/common incident). Recompute pooled AP/evaluator/event matching/rate/exposure in each resample; duplicate cluster draws need separate ID namespaces. Preserve undefined draws/no-positive slices; more resamples do not add cameras. Few clusters, BCa degeneracy, selection or unknown dependence require sensitivity/descriptive reporting and possibly INCONCLUSIVE. Do not insert arbitrary `n_eff` into an exact binomial formula. [F149](RAW_FACTS.md#F149), [F150](RAW_FACTS.md#F150), [F250](RAW_FACTS.md#F250).

### Zero-error arithmetic has explicit assumptions

INF, **hypothetical, not model measurements**: for pre-fixed n>0 iid Bernoulli observable GT episodes, one binary outcome each, frozen policy/matcher/deadline and complete follow-up, zero misses gives one-sided `Umiss=1−α^(1/n)`, `Lrecall=α^(1/n)`. Illustrative α=.05:20/20→13.91% upper miss/86.09% lower recall;100/100→2.95%/97.05%;300/300→.994%/99.006%. Two-sided95% Clopper–Pearson at0/20 instead gives16.84% upper miss because it usesα/2. Exact coverage is within the declared sampling model, not a posterior probability or universal safety guarantee. n=0 means recall unestimated. [F246](RAW_FACTS.md#F246), [F247](RAW_FACTS.md#F247), [S185](SOURCES.md#S185).

For pre-fixed T>0 source-camera-hours under homogeneous Poisson constant intensity/independent increments, zero false alerts gives `Urate=−lnα/T`: illustrative0/10h→.29957 per camera-hour,0/100h→.02996. Rate is not probability or precision. Cooldown bursts, heterogeneous cameras, outages/incomplete review may violate HPP. Count union original intervals per camera, not replay wall hours or overlapping cuts. T=0 gives undefined rate. [F248](RAW_FACTS.md#F248), [S186](SOURCES.md#S186), [S187](SOURCES.md#S187).

Paired example:100 episodes with79 both TP,1 A-only,1 B-only,19 neither gives80TP each/netΔrecall0 **and one new miss**. Gained TP cannot offset a must-pass regression. Zero new regressions among80 pre-fixed iid **baseline-success** episodes gives conditional upper3.675% atα.05; it is neither absolute B miss bound nor CI of paired recall difference. These formulas are not AP/OKS/HOTA intervals. Fixed-n bounds do not survive unaccounted test tuning/selection/clustering/optional stopping. A fully reviewed fixed-roster zero-regression statement can be valid while population inference remains INCONCLUSIVE. [F247](RAW_FACTS.md#F247), [F250](RAW_FACTS.md#F250), [Analytic annex](RAW_FACTS.md#engineering-annex).

<a id="diagnosis-stop-loss"></a>
## Symptom → minimal diagnostic → remedy → stop-loss

**Preserve the bad candidate/first divergent IDs and immutable accepted bundle.** These are candidate causes, not diagnoses from appearance. Confirm fixes on the same roster and repeat affected downstream gates. [F143](RAW_FACTS.md#F143), [F206](RAW_FACTS.md#F206), [E011](OPEN_QUESTIONS.md#E011).

| Symptom / boundary | Discriminating diagnostic | Remedy / remaining risk |
|---|---|---|
| Almost all detections disappear: media/schema | Exact input hashes/ranges/layout/color; raw roles and synthetic positive/empty outputs; complete status ledger | Fix single transform/decode/map owner, distinguish empty from failed. Actual model loss may remain. [F041](RAW_FACTS.md#F041), [F057](RAW_FACTS.md#F057), [F189](RAW_FACTS.md#F189) |
| Shifted/scaled/mirrored geometry | Asymmetric odd landscape/portrait/color/ramp; common raw decoder and ledger corners | Fix rotation/coordinate space/pad/crop/inverse; preserve intentional source box/point difference or version policy. [F060](RAW_FACTS.md#F060), [F210](RAW_FACTS.md#F210) |
| Mixed classes/pose tails | Synthetic one-class scores, shuffled/missing outputs, explicit nc/class/skeleton/port roles | Remove COCO84/85/first-output guesses; actual weights still needed for class meaning. [F043](RAW_FACTS.md#F043), [F045](RAW_FACTS.md#F045), [F213](RAW_FACTS.md#F213) |
| Confidence distribution shifts | Before cutoff: raw semantic channels/initializer clipping/scales/margins and first divergent parent | Correct duplicate sigmoid/objectness/dequant, then effective PTQ. Threshold retuning is a new dev policy, not proof quantization was fixed. [F071](RAW_FACTS.md#F071), [F214](RAW_FACTS.md#F214) |
| Duplicate/empty/lost NMS output | BCN/BNC/final6/A6, t±ε/t, IoU/ties/classes/caps/valid count and terminal status | Explicit shared NMS or proven graph equivalent; small numeric drift can still cross a boundary. [F048](RAW_FACTS.md#F048), [F051](RAW_FACTS.md#F051), [F209](RAW_FACTS.md#F209) |
| Easy cases pass, tiny/occluded fail | A/B→GT size/visibility/owner slices, same crops, pre-cutoff outputs and observability/classes | Input/ROI policy if source detail exists; coverage or supported block correction only by diagnosis. Tiling costs/context and invisible features remain limits. [F120](RAW_FACTS.md#F120), [F130](RAW_FACTS.md#F130) |
| Pose jitter / broken events | B→B then same-schedule A/B; first critical-joint/pool/assignment/predicate/FSM change, PTS/gap/reset | Fix schema/geometry/time/state/policy; numeric precision only after causality. Hysteresis can hide real brief events. [F131](RAW_FACTS.md#F131), [E009](OPEN_QUESTIONS.md#E009) |
| Source↔ONNX pass, LinQ fails | E005 float import; E006 native quant reference; E007 same QM/device and descriptors/packing/completion | Repair first failing importer/ABI/target/preset/compile boundary. Hidden stages remain confounded. [F212](RAW_FACTS.md#F212), [F238](RAW_FACTS.md#F238), [F239](RAW_FACTS.md#F239) |
| Fixed replay passes, real load fails | Complete source/scheduled/completed/drop/unresolved/delivery trace, batch/queue age/reorder/retry/EOF clocks | Fix supported scheduler/drop/idempotency/drain; higher FPS alone cannot recover brief-event coverage. [F240](RAW_FACTS.md#F240), [E010](OPEN_QUESTIONS.md#E010) |
| Backend comparisons are incomparable | Diff weights/inputs/rules/NMS/dtype/batch/provider/hardware/GT denominators | Rerun controlled parents or label as system comparison; no causal “INT8 lost X” claim. [F067](RAW_FACTS.md#F067), [F250](RAW_FACTS.md#F250) |

Decision order (PROPOSED): missing source/grant/scope→Q001–Q003/Q012 (catalog narrows claim); unstable source→load/eval/state/compute, not wider tolerances; input/schema→E002; preparation/export/import→revert first parent/minimal op/port test, not calibration/QAT; accepted float but bad quant reference→E006 effective policy/data/axis/cache and one supported intervention; good quant reference but bad device→E007 same QM/target/ABI/packing/completion, not initial training; raw/task near but events bad→margins/actor/time/state/fixed replay; proven quantization loss plus consumer proof→bounded selective/correction then conditional QAT pilot. [E004](OPEN_QUESTIONS.md#E004), [E005](OPEN_QUESTIONS.md#E005), [E006](OPEN_QUESTIONS.md#E006), [E007](OPEN_QUESTIONS.md#E007), [E011](OPEN_QUESTIONS.md#E011).

Stop at unsupported op/version/numerical boundary without documented equivalent lowering: **BLOCKED_FOR_ADMISSION**; admit an exact alternate route or actually supplied vendor artifact before more training. Stop recovery when required gates pass or the pre-agreed rescue budget expires. Roll back **weights/config+preprocess+decoder/classes/skeleton+tracker/rules/zones/sampling+compatible runtime**, not weights alone. Keep failed artifacts/logs. New model/shape/dtype/compiler/runtime/adapter/rule/schedule/camera geometry reopens affected gates. The historical45-hour competition window does not restart when research finishes; use actual clock and official deadline. [F245](RAW_FACTS.md#F245), [E012](OPEN_QUESTIONS.md#E012).

<a id="experiment-program"></a>
## E001–E012 practical program: all PROPOSED / UNRUN

**Three priorities after E001 and Q001–Q003:** E002 input/output/geometry; E003 unchanged completed-device smoke; E005 supplier float importer **after E004**. Catalog-only may make E005 UNAVAILABLE; proceed to service→GT E008/E009 with restricted claims. This is diagnostic prioritization, not measured duration. Common preparation: actual source/checkpoint/hash and ordered sample IDs from the future manifest, rights/group/split/PTS, independent GT and approved AR01. Roles below are selectors, not existing filenames/IDs. No invented server API/commands are required. Full canonical program: [OPEN_QUESTIONS](OPEN_QUESTIONS.md#experiment-program).

Each experiment follows YAML `experiment` fields. Common outcomes: PASS(scope) only after complete real run/approved limits; FAIL for confirmed invariant/budget violation; HOLD for missing data/access/policy; INCONCLUSIVE for insufficient measured precision/coverage/assumptions; UNAVAILABLE for an actually inaccessible operation. None currently has a result.

<a id="E001"></a>
### E001 — Freeze source, splits and AR01

**id_status:** E001; PROPOSED / UNRUN. [Canonical E001](OPEN_QUESTIONS.md#E001).

**decision_owner:** Model/data/evaluation leads establish whether a controlled comparison exists and what can be admitted.

**inputs_boundary:** Actual source/config/license/load/runtime, grant, media/rights/independent GT; Q001–Q003/Q012–Q014. Received artifacts→immutable contract; all future manifest roles. No device leg.

**procedure_evidence:** Hash weights/config/classes/skeleton/sidecars/dependencies and media→pixels→tensor/PTS lineage; pin eval/fusion/EMA/partial load. Audit duplicates/common incidents before transforms; freeze train/calib/dev/test, actual ordered IDs and full rollback. Approve scope/evaluator/units/floors/caps/δ/D/α/must-pass/stopping before selection. Save signed versioned AR01/manifests/rights/missing list; unknown pretraining stays unknown.

**outcomes_limits:** PASS required fields/approval; FAIL prohibited leakage/identity inconsistency; HOLD missing source/GT/policy. Narrow debug freeze can coexist with population HOLD. No accuracy/parity/device proof. [F004](RAW_FACTS.md#F004), [F009](RAW_FACTS.md#F009), [F250](RAW_FACTS.md#F250).

<a id="E002"></a>
### E002 — Admit pixels, tensor schema, decoder and geometry

**id_status:** E002; PROPOSED / UNRUN. [Canonical E002](OPEN_QUESTIONS.md#E002).

**decision_owner:** Adapter/CV lead separates semantic errors from model loss.

**inputs_boundary:** E001, actual IO and pinned preprocess/head/NMS/inverse, permitted CPU environment. Media→tensor and fabricated raw→canonical outputs. Roles odd landscape/portrait, empty/ownership/critical pose plus synthetic RGB/ramp/rotation/nc1/2/3/axis fixtures.

**procedure_evidence:** Record pixels/tensor hashes/ranges, actual resize/pads/crops, transform owner. Test all names/ports/roles, BCN/BNC/final6/A6/84/85 collisions, missing/shuffled multioutputs, class/skeleton map and exactly-once DFL/sigmoid/objectness/dequant. NMS t−ε/t/t+ε/IoU/ties/classes/caps/padding/time-limit. Apply version8.3.230 G01–G04 expectations, not old Pose rounding/zeroing. Save expected/actual arrays, schema rejects and dependency/branch/geometry logs.

**outcomes_limits:** PASS structural/synthetic arithmetic/approved numeric expectations; FAIL wrong role/axis/geometry/double transform/silent fallback. Inventory may make hidden portions UNAVAILABLE; preserve available black-box checks. No industrial accuracy or device proof. [F206](RAW_FACTS.md#F206), [F209](RAW_FACTS.md#F209), [F211](RAW_FACTS.md#F211).

<a id="E003"></a>
### E003 — Complete an unchanged known-good LinQ inference

**id_status:** E003; PROPOSED / UNRUN. [Canonical E003](OPEN_QUESTIONS.md#E003).

**decision_owner:** Platform/runtime owner admits actual access/bundle/program before custom build.

**inputs_boundary:** Supplier-supported TPU/service revision, known input/expected output/descriptors and actual invocation instruction; Q001/Q002/Q008/Q009. Unchanged supported artifact→completed LinQ output; two valid known inputs, normal/empty only if meaningful for that model.

**procedure_evidence:** Capture available source/export/compiled hashes or service/model revisions, session/device/input hashes and real/padded slots. Use documented actual path, establish readiness/completion/errors and correct user/raw interpretation; compare finite/schema/known expected. Save artifact→job/request→device→completion→named-output correlation, terminal statuses and permitted coverage/partition/profile. Import/load/inventory alone is insufficient.

**outcomes_limits:** PASS completed correct unchanged output with adequate scoped attribution; FAIL wrong artifact/backend/output/error; HOLD label/utilization/enqueue without completion. Service attestation is separately attributed. No custom upload support/full placement without report/task/events/FPS proof. [F203](RAW_FACTS.md#F203), [F238](RAW_FACTS.md#F238), [F239](RAW_FACTS.md#F239).

<a id="E004"></a>
### E004 — Source repeatability, preparation and same-dtype export

**id_status:** E004; PROPOSED / UNRUN. [Canonical E004](OPEN_QUESTIONS.md#E004).

**decision_owner:** Model/export lead admits float parents or reverts first divergence.

**inputs_boundary:** E001/E002 actual checkpoint/lock, exact tensors and exporter/opset. Ordinary eager→prepared eager→unsimplified same-dtype ONNX→alternate same-dtype runtime→individual passes. Roles normal/empty/odd/tiny/pose/owner plus accepted branch/shape/batch controls.

**procedure_evidence:** Measure repeated source state/input/batch/fresh process; log fusion/export/C2f/TF32/autocast/compute. Serialize/hash every graph parent/IR/opset/inventory/warning. Test both branches, B/[a,b]/[b,a] and accepted rectangles; compare all outputs/finite masks/per-head abs-relative/range and source→final. Dtype-only child separately records constant clipping/casts. Checker/check_ok/verify alone cannot admit.

**outcomes_limits:** PASS approved structural/repeatability/numeric budgets; FAIL first divergence/nonfinite/schema/unapproved pass; HOLD absent source/bounds. Revert preparation/pass/operator/shape, not train. No TPU/importer/GT proof. [F013](RAW_FACTS.md#F013), [F027](RAW_FACTS.md#F027), [F067](RAW_FACTS.md#F067), [F206](RAW_FACTS.md#F206).

<a id="E005"></a>
### E005 — Supplier float ONNX→TF and complete port identity

**id_status:** E005; PROPOSED / UNRUN. [Canonical E005](OPEN_QUESTIONS.md#E005).

**decision_owner:** SDK/import owner admits importer semantics before attributing PTQ loss.

**inputs_boundary:** E004 and actual Q004/Q005 bundle/supported float executor. Exact ONNX→float imported TF before QM. Axis-coded `[1,3,2,2]` values `100*c+10*h+w`, Identity/Transpose and two-output Split, then actual neural tensors.

**procedure_evidence:** Record distribution/module/callable/file/version/hash/signature/actual kwargs, every serialized parent and full Value/ordinal/producer-port→TF exact tensor-port/layout→QM table. Test both Split outputs independent of dict order; reject stripped ports/first-output/retries without branch evidence. Then compare every neural raw channel/candidate/keypoint and shared decoder. Save GraphDefs/hashes/mapping/arrays/deltas/tracebacks.

**outcomes_limits:** PASS unambiguous mapping/roles/arithmetic/budgets; FAIL swapped/missing port/axis/endpoint. No float executor→UNAVAILABLE and confounded import+PTQ, not PASS. No device/PTQ/full-neural-operator proof from micrograph success. [F212](RAW_FACTS.md#F212), [F213](RAW_FACTS.md#F213), [Q015](OPEN_QUESTIONS.md#Q015).

<a id="E006"></a>
### E006 — Effective native PTQ policy and save/load

**id_status:** E006; PROPOSED / UNRUN. [Canonical E006](OPEN_QUESTIONS.md#E006).

**decision_owner:** Quantization/SDK owner identifies actual calibration factor and reproducibility.

**inputs_boundary:** Admitted float parent, supported weighted probe/encodings/hooks, separate calib/dev and Q006 definition. Float TF→native quantized reference→fresh-process reload. Materialized tail distributions A/B and dev tiny/light/hard-negative roles; test untouched.

**procedure_evidence:** Two documented-valid P settings×two distributions; fresh model per cell and two fresh repeats of one cell; no blanket TypeError retry. Capture requested/passed/effective config, order/count/groups/cache, weights/ranges/thresholds/scales/zp/axis/signedness and first boundary. Direct activation effects require frozen-weight intervention/implementation trace, else confounded. Compare actual bounds/clipping and save/load without recalibration; then one-factor supported method/coverage/N/order probes. Save QM/encodings/arrays/warnings.

**outcomes_limits:** PASS explained application/repeatability and approved dev gates; FAIL invalid scales/confirmed ignored supported setting/numeric reload drift; HOLD/INCONCLUSIVE hidden or indistinguishable scope. No effect is not proof ignored. Device only via E007; no best-percentile/independent-quality/QAT proof. [F175](RAW_FACTS.md#F175), [F214](RAW_FACTS.md#F214), [F216](RAW_FACTS.md#F216).

<a id="E007"></a>
### E007 — Compiler/device numerical consumer before training

**id_status:** E007; PROPOSED / UNRUN. [Canonical E007](OPEN_QUESTIONS.md#E007).

**decision_owner:** Compiler/quant/platform owners choose executable native PTQ, external-preserve or native matching-simulator recovery route.

**inputs_boundary:** E003/E005/E006, matched official recipe Q005/Q007/Q008 and weighted probe with distinct scales/axis/zp. Quantized reference→TLM if exposed→compiled→completed device; external QDQ/encodings traverse full import chain.

**procedure_evidence:** One clean QM, explicit reference/compile target/preset/config/batch; rounding/half-step/clipping/zp/bias/accumulator probes and documented equivalent lowering. Islands require actual Q→FP→Q/shared-residual boundary/precision/placement and outputs, not QDQ counts. FULL↔RAW+codec only via current supported ABI. Validate unchanged deployment graph after debug. Save QM/TPU/config/coverage/CPU portions/descriptors plus input/job/device/completion/output trace.

**outcomes_limits:** PASS preserved numerical contract or documented equivalent lowering with approved placement/budgets; FAIL changed arithmetic/wrong target/hidden fallback/unsupported boundary. Hidden consumer/report→HOLD/UNAVAILABLE corresponding recovery, no speculative GPU work. No full-model gain/task/events/speed proof. [F217](RAW_FACTS.md#F217), [F224](RAW_FACTS.md#F224), [F238](RAW_FACTS.md#F238), [F239](RAW_FACTS.md#F239).

<a id="E008"></a>
### E008 — Independent detection/pose and lost/gained regression gate

**id_status:** E008; PROPOSED / UNRUN. [Canonical E008](OPEN_QUESTIONS.md#E008).

**decision_owner:** CV/evaluation lead accepts candidate quality against independent GT.

**inputs_boundary:** Actual A/B prediction roster/E001 source/E007 final artifact, grouped independent test/rights/GT/skeleton, frozen adapters/evaluator and Q012 policy. A/B separately→GT; diagnostic A↔B separately. All test roles/critical IDs.

**procedure_evidence:** Official pooled AP/OKS/PCK with units/config; separate class-consistent one-to-one diagnostic matches, lost/gained/unmatched/allGT IDs/margins. Include source+input size, class/visibility/occlusion/critical joints and missing people. Paired clusters recompute full evaluator, preserving undefined draws/few-cluster sensitivity. Save predictions/GT/evaluator hashes/counts/estimates/absolute B/Δ/uncertainty and linked E003/E007 device proof.

**outcomes_limits:** PASS all approved absolute/slice/non-inferiority/invariant gates in scope; FAIL confirmed/critical must-pass regression; INCONCLUSIVE rare n0/few clusters/wide bounds; HOLD missing GT/policy. Gained TP cannot cancel critical loss. No tracking/event/natural-stream exposure or new-population proof. [F145](RAW_FACTS.md#F145), [F146](RAW_FACTS.md#F146), [F250](RAW_FACTS.md#F250).

<a id="E009"></a>
### E009 — Causal tracking/event parity on fixed schedule

**id_status:** E009; PROPOSED / UNRUN. [Canonical E009](OPEN_QUESTIONS.md#E009).

**decision_owner:** Tracking/event/evaluation owners localize propagation and admit event policy.

**inputs_boundary:** E008 outputs, continuous PTS/epoch clips, independent actor/episode/onset-uncertainty GT/complete follow-up, frozen tracker/FSM/zones/reset/warm prefix/deadline. A→same downstream versus B→same downstream/schedule. Short/zone/occlusion/owner/fall-if-selected/persistent/re-entry/EOF/continuous-negative roles.

**procedure_evidence:** B→B repeatability first; record low/high/new pools/association costs/predicates/consumed frames/FSM and first divergence. Oracle scores/boxes/fixed-crop branches remain diagnostic. One-to-one event matching by actor/type/camera/zone/temporal+deadline policy; no future leakage/backdating. Save four paired episode cells+IDs, allGT timely recall/late/miss/wrong-actor/duplicate/false/unknown, union source-camera-hours, tracking metrics where GT exists and latency n+misses. Link original prediction/device lineage.

**outcomes_limits:** PASS approved continuity/event/dedup/absolute gates and complete closure; FAIL critical miss/wrong person/ongoing duplicate/future leakage; HOLD/INCONCLUSIVE insufficient truth/follow-up/support. No actual queue/load/visible-delivery proof; E010 is separate. [F131](RAW_FACTS.md#F131), [F134](RAW_FACTS.md#F134), [F148](RAW_FACTS.md#F148), [F250](RAW_FACTS.md#F250).

<a id="E010"></a>
### E010 — Actual uploaded-video schedule, load and visible delivery

**id_status:** E010; PROPOSED / UNRUN. [Canonical E010](OPEN_QUESTIONS.md#E010).

**decision_owner:** Video/runtime/product owners select measured sampling/concurrency/drop/timing policy.

**inputs_boundary:** E003/E008/E009, actual Q010/Q011 grant/service, permitted load/fault validation, AR01/clock mapping. Fixed causal replay→actual scheduler/completed inference→visible alert. Same original positive/negative/short/VFR/gap/reconnect/EOF bytes/PTS; server upload if confirmed, no assumed laptop stream.

**procedure_evidence:** One stream then permitted declared concurrency; census source/sampled/scheduled/completed/dropped/failed/unresolved, real/padded slots and retry IDs. Whole-batch warmup or exact matched accounting; timer through readiness, separate decode/queue/copy/infer/NMS/rules/delivery. Paced replay anchor/speed/clock uncertainty separate from unpaced throughput. Predeclared rate×phase/burst-gap tests include all GT; adaptive triggers causal. Supported late/reorder/duplicate/error/EOF/drain validation; timeout≠cancel. Save useful completed real FPS/interval, quantiles+n+miss/late/timeout/age/max-gap, terminal/delivery ledger and device/placement traces.

**outcomes_limits:** PASS quality/completeness/latency/device gates at that load; FAIL deadline/coverage/hidden neural backend switch; HOLD missing completion/clock/device; INCONCLUSIVE insufficient exposure/support. Correct model/bad queues calls for architecture remedy. No other stream/site/event-duration/1FPS guarantee. [F186](RAW_FACTS.md#F186), [F189](RAW_FACTS.md#F189), [F238](RAW_FACTS.md#F238), [F240](RAW_FACTS.md#F240).

<a id="E011"></a>
### E011 — Bounded recovery or alternate-route admission

**id_status:** E011; PROPOSED / UNRUN. [Canonical E011](OPEN_QUESTIONS.md#E011).

**decision_owner:** Model/quant/training owner invests only in localized executable loss.

**inputs_boundary:** Failed E004–E010 boundary/IDs, clean parent/full rollback, fixed calib/dev/sealed test, E007/Q007 consumer and separately authorized resource pilot if needed. One PTQ parent→one correction/island/QAT or exact alternate→full export/import/compile/device. Actual dev-failure and holdout IDs.

**procedure_evidence:** Fix semantics/import/effective calibration first. Proposed≤6 semantic regions+≤2 boundary/interactions, one justified correction with ablation; QAT requires simulator/BN/observer/checkpoint/export round trip and measured allocated/reserved memory/step/eval/export/compile/billable ledger. RT-DETR tests sampler16/TopK/attention admission; RTMPose dependency/registry/metadata/two-output/flip-off/fixed-crop before full detector+N crops. Optional ORT tool needs exact entry-point/provider/optimized-graph smoke. Freeze winner on dev; save all trials/failed artifacts/placement/encodings and independent E008/E009 results.

**outcomes_limits:** PASS reproducible post-compile gain with required absolute/task/event/device/latency gates; FAIL lost export/compile gain/critical regression/budget overrun; HOLD absent consumer/data/pilot; UNAVAILABLE unsupported actual grant. Stop unsupported boundary without equivalent lowering, exhausted pre-agreed budget or accepted result; full rollback. No universal method/bitwidth/GPU speedup. [F091](RAW_FACTS.md#F091), [F117](RAW_FACTS.md#F117), [F230](RAW_FACTS.md#F230), [F245](RAW_FACTS.md#F245).

<a id="E012"></a>
### E012 — Reviewable acceptance, demo and complete rollback

**id_status:** E012; PROPOSED / UNRUN. [Canonical E012](OPEN_QUESTIONS.md#E012).

**decision_owner:** Evaluation lead/team approver permits only evidenced scope.

**inputs_boundary:** Applicable actual E001–E011 results/approvals, complete source/candidate/GT/evaluator/device/delivery evidence without secrets. Collected evidence→versioned claim/demo/accepted-bundle restoration; not a new benchmark. All evaluated IDs plus disclosed good/worst/negative examples.

**procedure_evidence:** Populate MEASURED only from logs; each required gate gets status+scope, adjacent/source-final deltas, counts/exposure/uncertainty, lost/gained/dropped IDs and hidden boundaries. Link original hash/PTS→model/export/compiled/service→completed job/device→raw/canonical→GT→visible alert. Keep vendor/paper numbers separate. Restore entire model/preprocess/decoder/classes/skeleton/tracker/rules/zones/sampling/runtime and verify baseline; save portable proof pack/signed owner-date-decision/risks/rollback result.

**outcomes_limits:** PASS actual required gates/evidence/full restoration in scope; FAIL required violation/false claim/failed rollback; HOLD missing proof. Narrow fixed-roster PASS can coexist with population INCONCLUSIVE. New configuration reopens gates. No synthetic industrial-footage substitution/fabricated LinQ–NVIDIA comparison/certification/future-safety guarantee. [F001](RAW_FACTS.md#F001), [F246](RAW_FACTS.md#F246), [F250](RAW_FACTS.md#F250).

<a id="device-jury-evidence"></a>
## Actual TPU proof and jury evidence

**Prove both lineage/compiled neural coverage and completed per-request execution.** Source→export→QM/TPU/service revision identity/target/preset/partitions explains what could execute; input→request/attempt/job→actual session/device→completion→named output explains what did execute. Neither replaces the other. Device inventory/UI label/utilization, compile success, response or CPU ndarray alone cannot prove whole neural placement. Restricted-service attestation must be labeled as such, with its IDs/scope and uncovered portions. [F195](RAW_FACTS.md#F195), [F223](RAW_FACTS.md#F223), [F238](RAW_FACTS.md#F238), [Q009](OPEN_QUESTIONS.md#Q009).

PROPOSED jury pack: identical **real** clips/hash/PTS, selected scope/GT/rules, source+actual-target+GT overlays in original geometry, machine-readable raw/canonical predictions/matches, actor/episode evidence and visible alerts; full continuous segment demonstrates one ongoing incident→one alert, distinct re-entry not suppressed, and negative behavior. Include worst regressions and uncertainty/unsupported slices. Preserve model/config/classes/skeleton/runtime and all parent hashes/versions, compiled coverage/completion traces, counts/exposure/paired deltas/evaluator, timing interval/warmup/batch/concurrency/latency n+misses. [F001](RAW_FACTS.md#F001), [F249](RAW_FACTS.md#F249), [E012](OPEN_QUESTIONS.md#E012).

Claim wording must match evidence: no source→report service quality, not checkpoint fidelity; hidden importer/PTQ→combined transition, not pure INT8 loss; timely events→allGT/correct actor/causal frames/deadline/clock/visible delivery; speed→completed real IDs and stated boundary, not configured QPS or success-only p95; zero false→count/exposure/model-conditional bound or descriptive roster statement. Published LinQ/Wu/BRECQ/MMDeploy results explain choices separately from our measurements. Do not construct LinQ/NVIDIA comparisons from different models/inputs/policies/hardware or show generated factory footage as actual video. [F230](RAW_FACTS.md#F230), [F237](RAW_FACTS.md#F237), [F240](RAW_FACTS.md#F240), [F247](RAW_FACTS.md#F247).

<a id="questions-handoffs"></a>
## Engineer questions, unresolved owners and neighboring topics

**Obtain one compatible executable route first.** Prepared questions have not been sent externally. A generic web overview cannot resolve missing grants/artifacts or team risk decisions. [OPEN_QUESTIONS](OPEN_QUESTIONS.md).

| Priority / owner | Concrete missing answer and closure |
|---|---|
| P0 platform/organizer; [Q001](OPEN_QUESTIONS.md#Q001)/[Q002](OPEN_QUESTIONS.md#Q002) | Actual grant, custom weights/build/upload/tools/quotas; exact SKU/reference+compile target; matched framework/importer/compiler/runtime/pytpu/native/driver/firmware hashes and known-good program/input/output. Close with inventory and completed E003, not Python import |
| P0 model lead; [Q003](OPEN_QUESTIONS.md#Q003) | Actual weights/config/license/load/state/classes/skeleton/external lock. Close immutable source bundle and repeated outputs; catalog without source narrows claim |
| P0 SDK/compiler; [Q004](OPEN_QUESTIONS.md#Q004)/[Q005](OPEN_QUESTIONS.md#Q005) | Callable/distribution/mapping/ports/float executor; accepted IR/opsets/domains/attributes/shapes/batches/multioutputs, actual targets/presets/save/return schema. Close matched definitions plus E005/neural inventory/compile report |
| P0 quant/compiler before sweep/training; [Q006](OPEN_QUESTIONS.md#Q006)/[Q007](OPEN_QUESTIONS.md#Q007) | Percentile object/formula/tails/domain/effective settings/cache; QDQ/encodings/native-simulator preservation, W/A/bias/accumulator/rounding/axis/boundaries. Close E006/E007 with matched recipe |
| P0 runtime/organizer; [Q008](OPEN_QUESTIONS.md#Q008)/[Q009](OPEN_QUESTIONS.md#Q009) | Completion/readiness/timeout/cancel/retry/thread safety; current user/raw/codec/PRE/POST placement; per-job/coverage evidence and permitted neural CPU boundary including extra NN. Close correlated completed smoke/placement |
| P0 video/event; [Q010](OPEN_QUESTIONS.md#Q010)/[Q011](OPEN_QUESTIONS.md#Q011) | Actual file/codecs/media/transform/output ownership; PTS/epochs/sampling/drops/reorder/retry/EOF/drain/clock/visible-alert/load-validation contract. Close dumps/complete ledgers/E009/E010 |
| P0 risk/product/evaluation and data rights; [Q012](OPEN_QUESTIONS.md#Q012)/[Q013](OPEN_QUESTIONS.md#Q013) | Approved scenarios/observable episode semantics/D/floors/caps/δ/α/stopping and licensed independent GT/continuous negatives/full follow-up. Close signed AR01 and real manifests, not SDK engineer guesses |
| P1 evaluation; [Q014](OPEN_QUESTIONS.md#Q014)/[Q015](OPEN_QUESTIONS.md#Q015) | Population/estimand/independent clusters/actual support/exposure; exposed intermediate references/dumps and instrumentation effect. Close design+inventory, preserve confounding/INCONCLUSIVE where necessary |
| P1 or P0 before fallback; [Q016](OPEN_QUESTIONS.md#Q016)/[Q017](OPEN_QUESTIONS.md#Q017) | Exact alternate weights/lock/operator admission; actual correction/QAT memory/time/cost. Close E011 admission and permitted measured pilot after E007 |
| P2, P0 before quoting author accuracy; [Q018](OPEN_QUESTIONS.md#Q018) | Separate TinyYOLO3/custom YOLOv8 program/source hashes/raw predictions/metrics/MLPerf logs/config/runID/exit code; original performance PDF/methodology. Otherwise retain limited author/vendor attribution |
| P1 only if tool selected; [Q019](OPEN_QUESTIONS.md#Q019) | Exact converter/ORT wheel/providers/optimized graph and supported fixture. Close local provider smoke; CPU search is not target proof |

Suggested five-person ownership is organizational, not an actual assignment: platform/compiler obtains grant/E003/E005/E007; model/export/quant owns schemas/E004/E006/E011; data owns rights/IDs/grouped GT; video/tracking owns causal replay/full service census; evaluation/product owns AR01/independent E008/E012/demo. Platform and source preparation can proceed in parallel, but training depends on E007 and final testing on winner freeze. Handoffs require parent hash/config, actual IDs, first failed boundary, outputs/logs and next-owner decision. [E001](OPEN_QUESTIONS.md#E001), [E011](OPEN_QUESTIONS.md#E011).

| Neighbor topic | Transfer / required return | Q/E dependency |
|---|---|---|
| linq_platform | Version/ABI/import/numerics/codec/completion/placement seams → matched bundle/capability inventory/trace | Q001/Q002/Q004–Q009; E003/E005–E007 |
| model_stack | U8.3.230 and RT-DETR/RTMPose contracts/blockers → actual weights/config/license/classes/lock | Q003/Q005/Q016; E002/E004/E011 |
| datasets | Pack roles/rights/group inheritance/visibility/actor/continuous negatives → real media/GT/manifests | Q013/Q014; E001/E008/E009 |
| training_strategy | First quantized divergence/IDs/encodings/conditional correction → bounded measured pilot | Q006/Q007/Q017; E006/E007/E011 |
| evaluation | AR01/units/paired clusters/zero-count assumptions/lost-gained ledger → approved design/budgets | Q012–Q014; E008/E009/E012 |
| violation_methods | Tiny/pose/ownership/UNKNOWN and causal episode semantics → chosen predicates/GT definitions | Q011/Q012; E009 |
| video_architecture | File/completion/batch/PTS/epoch/drop/closure contract → actual schedule/load/clock traces | Q008–Q011; E003/E010 |
| operator_product | Visible-alert usefulness/wrong actor/late/duplicate/unknown/review burden → approved policy | Q011/Q012; E009/E010/E012 |
| hackathon_strategy, market_deployment | Evaluable scope/evidence/limits → honest defense without safety extrapolation | Q012/Q018; E012 |

These are file-based handoffs, not messages sent to engineers or other projects. Documentary critic closures K003/K006/K008 establish the source contract, published comparison support and alternate route cards only; seven other findings are narrowed and K010 acceptance remains open. None closes the actual target/data questions or turns UNRUN into PASS. [CRITIC dispositions](CRITIC.md#w2-dispositions), [F002](RAW_FACTS.md#F002), [F003](RAW_FACTS.md#F003).
