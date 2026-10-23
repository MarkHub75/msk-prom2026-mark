---
topic: cv_accuracy_vast
context_version: mosprom-research-v1
scope: >-
  Evidence-based CV quality objectives, conditional model and adaptation choices,
  causal event evaluation, and a reproducible one/two RTX 3090 Vast.ai laboratory
  plan for the 2026 Mosprom LinQ case. Documentary research and proposed experiments;
  no paid compute or model/device execution.
not_covered:
  - "Camera metric geometry and calibration: separate follow-up; links to violation_methods and video_architecture."
  - "Full LinQ PTQ/QAT and deployment accuracy investigation: follow-up to linq_platform/model_stack."
  - "Comprehensive behavioral checkpoints and video dataset search: separate follow-up to datasets/violation_methods."
  - "Complete operator product, market, or submission implementation: operator_product, market_deployment, hackathon_strategy."
answers:
  - "What was actually checked, and what remains unmeasured? See evidence-status."
  - "Which bounded A/B/C route, owners, and cutoffs fit the remaining competition window? See bounded-route."
  - "How should timely events, false alerts, duplicates, exposure, and uncertainty be measured? See quality-contract."
  - "Which real media leads exist, and what rights, timing, and annotation work remain? See media-readiness; Q001-Q004."
  - "What can TRAIN, DEV, optional CAL/SELECT, and LOCKBOX legitimately support? See data-roles."
  - "Which exact detector, pose, verifier, and export-reserve candidates merit conditional checks? See model-candidates."
  - "What do published benchmarks and licenses establish, and what do they not establish? See benchmarks-and-rights; Q008/Q017."
  - "How do sampling, causal state, tracking, and ownership affect event quality? See causal-time-and-tracking."
  - "When can thresholds, calibration, postprocessing, data QA, or one fine-tune help? See thresholds and adaptation."
  - "Which source-backed training/export versions and head-specific traps must be retained? See export-envelope; Q008/Q018."
  - "Which proposed experiments should run first, and what are their controls and stopping gates? See experiment-program."
  - "When is one or two RTX 3090 useful, and what must actual qualification measure? See gpu-schedule; Q009/Q022."
  - "What public Vast offers were observed, and how are full lifecycle costs accounted? See vast-offers-and-costs; Q013-Q015."
  - "Which exact Vast CLI artifact and commands were checked, and what transfer risks remain? See vast-cli; Q016."
  - "How should native recovery mutations, progress, snapshots, and archive acceptance be recorded? See recovery-and-registry; Q011/Q012."
  - "What does public LinQ evidence support, and what exact handoff and device proof are missing? See linq-handoff; Q006/Q007/Q018-Q021."
  - "Which unresolved gates and neighboring research handoffs have concrete next actions? See open-gates and handoffs."
keywords:
  - CV accuracy
  - LinQ
  - Mosprom 2026
  - timely event recall
  - false alerts per camera-hour
  - causal replay
  - TRAIN DEV LOCKBOX
  - URFD
  - CAUCAFall v5
  - YOLO26s
  - Objects365
  - D-FINE-M
  - YOLOX-s
  - RTMPose-s
  - MobileNetV3-small
  - TSM
  - ByteTrack
  - OC-SORT
  - calibration
  - hard negatives
  - partial labels
  - Vast.ai
  - RTX 3090 24 GB
  - CLI v1.9.0
  - EMA
  - OOM recovery
  - ONNX
  - placement
  - ResNet50
entity_schema:
  model_candidate: [role, identity_and_initialization, hypothesis_and_gate]
  experiment: [id_priority, control_and_factor, inputs_and_measures, stop_and_evidence]
  open_gate: [id, unknown_and_decision, proposed_owner_and_closure]
takeaways:
  - "Start A: one accepted pretrained frontend plus causal CPU rules/FSM, without new training. Observable lying-state is conditional on usable media/frontend; otherwise a person-in-polygon scenario requires authorized team video. Without media, only synthetic logic feasibility is supportable."
  - "B is one fine-tune after confirmed frontend error, exhaustive TRAIN labels, DEV, accepted weights/use, export/runtime gates, and separately authorized actual-host qualification. C is one justified challenger or useful second GPU only with ready work and measured mandatory reserves."
  - "No target model ranking, quality, VRAM, training time, LinQ latency, recovery RPO/RTO, or actual charges were measured. All E001-E012 are PROPOSED/UNRUN."
  - "Current proposed URFD pair is DEV only: TRAIN is empty and independent LOCKBOX absent. Curated clips do not establish industrial prevalence or ordinary-background FP/hour."
  - "YOLO26s has author-reported O365v1-to-COCO lineage; D-FINE COCO AP is not a controlled target ranking. Exact code, weights, backbone, data, and distribution rights require separate decisions."
  - "The received Vast CLI v1.9.0 wheel uses argv subprocess copy, not legacy shell=True; unchecked return codes and disabled host-key checking remain. Copy success is not a verified archive."
  - "Vast quotes are historical public snapshots, not reservations. Whole-offer compute and allocated disk must not be counted twice. Loading storage has a current-document contradiction; account units and charges remain unknown."
  - "The historical LinQ worked example is ResNet50 classification. yolo5s is only a tested-name; no exact detection fallback or issued SDK compatibility is proven. Final neural inference requires actual LinQ placement, parity, and full delivery evidence."
checked_at:
  access_date: "2026-10-23"
  timezone: Europe/Moscow
  research_started: "2026-10-23T19:36:01+03:00"
  public_offer_snapshot_utc: "2026-10-23T17:04:35Z/2026-10-23T17:04:37Z"
  second_wave_finished: "2026-10-23T20:50:48+03:00"
  human_assembly_started: "2026-10-23T21:18:11+03:00"
  machine_role_started: "2026-10-23T21:49:03+03:00"
case_availability: >-
  Full official case was issued according to the team context. Root visually read
  all 20 raster pages and critical pages separately; portable notes preserve provenance.
  Actual team videos, labeled corpus, issued SDK/server inventory, and account are unavailable here.
actually_checked:
  - "Saved primary documentation, pinned source, papers, release/model metadata, and their conditions."
  - "Official case through root's attributed direct visual observations; no independent PDF reread by compressor."
  - "Read-only unauthenticated public Vast offer JSON; URFD synchronization CSV bytes; release Vast CLI wheel bytes/static code."
  - "Compressor's local YAML, answer coverage, ID/link, and semantic consistency checks; no new internet research."
human_report: report_human_cv_accuracy_vast.md
sources: SOURCES.md
raw_facts: RAW_FACTS.md
open_questions: OPEN_QUESTIONS.md
critic: CRITIC.md
---

# CV quality and Vast.ai research plan for LinQ

## evidence-status

Evidence legend: **DOC** = primary documentation statement; **CODE** = static code/artifact metadata observation; **PUB** = authors' published measurement with their configuration; **OBS** = our actual read-only/local observation; **INF** = inference from stated evidence; **PROP** = proposed policy/experiment; **UNK** = unknown. A vendor family claim is a claim, not execution evidence. **UNRUN** independently marks an unperformed procedure. Facts F001–F201 are in [RAW_FACTS.md](RAW_FACTS.md), sources S001–S290 in [SOURCES.md](SOURCES.md), unresolved Q001–Q024 in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md), original K001–K011 and W2 outcomes in [CRITIC.md](CRITIC.md). IDs are local to `cv_accuracy_vast`; [ID_MAP](_WORK/ID_MAP.md) preserves branch mappings.

**OBS:** Research comprised 16 W1 branches, one fresh-context critic, seven targeted W2 branches, then sequential collector/author/editor/compressor. S001–S290 are reading records, including repeated URLs and three local provenance records; **290 records are not 290 independent confirmations**. Saved evidence includes code/docs/metadata, six public offer rows, a small CSV, and CLI wheel bytes. No rental/payment, training, GPU qualification, model quality/VRAM/timing benchmark, model export, ONNX parity, recovery drill, or LinQ execution occurred. No large model binaries were obtained. All E001–E012 below are PROP/UNRUN. Source-backed versions are not installed locks. F002/F020; S002/S003.

**OBS/DOC boundary:** Root visually read the 20-page official case, including separate larger p5/7/13 views. Case PDF: 8,320,969 bytes, SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`; exact public PDF URL unknown. [CASE_NOTES](_WORK/CASE_NOTES.md) and S001 preserve this provenance. The case requires neural inference on LinQ, measured speed, prompt evidence-backed notification, one notification per continuing incident, and a filterable event journal; prioritizing scenarios is allowed. It does not establish an exact accuracy formula, device inventory, or sufficient labeled benchmark. Team statements “even 1 FPS, prioritize accuracy” and CPU+TPU/file-on-server are **team verbal reports**, not official scoring or issued hardware documentation. RTX 4070 exists in context; its VRAM/OS/driver are unknown. F001/F002.

## bounded-route

**PROP, selected integration F003/F017; K011 resolved by a bounded route, not runtime success.** First scope: observable **lying person** in a fixed view with one alert per continuing episode, only after media rights and frontend distinguishability are established. Lying does not prove fall transition, prolonged immobility, unconsciousness, or cause. If this route lacks accepted media or suitable frontend, the sole fallback scope is person-in-user-polygon on authorized team video **after such video is obtained**; a polygon alone does not prove physical danger. Without authorized media, support only synthetic logic feasibility.

- **A:** one accepted pretrained frontend + causal CPU rules/thresholds/FSM, **no new training**. Gates: rights/media/time/event labels → synthetic ledger acceptance → oracle real replay → frontend causal replay → same-head floating export/parity → issued known-good LinQ serial sample and our exact graph → measured full delivery → freeze. A may conclude with honest feasibility rather than industrial quality.
- **B:** **one** baseline fine-tune only for human-confirmed frontend error, with exhaustive TRAIN, separate DEV groups, accepted exact weights/use, source-backed train/export setup and actual runtime gate. Actual 3090 qualification follows **separate spending authorization**, before heavy training. Recheck the entire final bundle.
- **C:** **one** error-driven challenger or useful second-GPU workload, only after completed A/B, ready inputs, and measured reserves. Spatial changes, augmentation, pose, verifier, ensemble, and DDP are alternatives, not a mandatory cumulative queue.

Before first rental, check documents/data/available local CPU export mechanics and archive readiness. Requiring measured fit on an as-yet-unrented 3090 would be circular; actual-host fit belongs to the separately authorized first paid qualification. Research/public quotes authorize no spending. F003/F017; Q009/Q013.

**PROP ownership slots, not assigned people:** R1 data/labels/rights; R2 evaluation/FSM/reviewer/LOCKBOX; R3 model/training/Vast/artifacts; R4 LinQ integration; R5 product/submission/coordinator. R1/R2 prepare labels and fixtures while R3 prepares pretrained export, R4 identifies issued SDK/sample/policy, and R5 fixes scope, evidence UI, deduplication/journal and submission inventory. Actual names/availability are Q023.

**Recorded clock, not a promised compute allocation:** W2 ended 2026-10-23 20:50:48 MSK, leaving **37 h 09 min 12 s** to 2026-10-25 10:00 MSK. Human assembly began 21:18:11 MSK, leaving **36 h 41 min 49 s**. Original 45 hours describe the whole contest; they cannot restart. Selected cutoffs: **24 October 11:00 MSK** = one end-to-end feasibility result or explicit blocker/scope reduction; expansion thereafter requires finished incumbent, ready inputs, measured reserve. **24 October 18:00 MSK** = freeze scenario/models/heads/rules/sampling/evaluator and stop optional new families/scenarios/jobs; unfinished optional jobs follow declared stop/save policy. Then complete parity/LinQ/evaluation/archive/UI/README/demo/teaser/slides/submission before **25 October 10:00 MSK**. Blocking fixes receive new artifact identity and affected rechecks. F001/F017; S001 pp15/18.

Before B/C compute `available_until_freeze - remaining_mandatory_work - recovery_reserve`. Mandatory work includes LinQ/parity, independent evaluation if available, external archive verification, product delivery, and submission. Unknown durations/reserves are not zero: do not start optional work until protected. No training-hour or ×2 speed estimate was measured. F017/F104/F129/F140.

## quality-contract

**PROP F008/F021–F029:** optimize a complete pipeline's timely event detection under false-alert, deadline, and coverage constraints. Object AP diagnoses causes; it is not safety-event accuracy. Case wording “a few seconds” needs scenario-owner values `D_c` (deadline), `Rmin_c` (timely recall floor), `B_c` (false-notification budget), severity/response/coverage/delivery endpoint. These values are UNK/Q005; show a Pareto frontier and raw counts until agreed.

| Layer | Required measurements and interpretation |
|---|---|
| Objects | Per-class precision/recall, AP50:95 with evaluator/IoU/max-detections/class map; original and final-input pixel size/visibility. COCO APsmall is an annotation-area bin, not PPE visibility. |
| Association | Wrong owner/actor/pair, ID switches, fragmentation, recovery; IDF1/HOTA when suitable GT exists. A correct phone box can belong to the wrong person. |
| Events | Timely and eventual recall, late/missed/censored, onset/end/first-observable boundaries and unknown intervals. |
| Notifications | Semantic FP per eligible camera-hour, PPV, duplicate alerts per episode/hour, wrong actor, suppressed second actor. |
| Time | Source sampling interval/phase, fresh observations, frame age, queue/drops, decision→emit→receive and actually observable end-to-end endpoint. |
| Robustness | Camera/session/view/site, final pixel size, occlusion, clothing/light/background/compression, short/long events; macro/worst-group and raw counts. |
| Deployment | Same-head reference→floating ONNX→converted graph→actual LinQ; tensor/box/score/class/ranking/decision differences and causal event replay. |

**DOC/INF:** [COCO](https://cocodataset.org/dataset/detection-eval.htm) does not assess notification deadlines. [ActivityNet evaluator](https://raw.githubusercontent.com/activitynet/ActivityNet/ebc8aebb4018a758c4efb35bb7ab547d31b1eb1e/Evaluation/eval_detection.py) temporal matching and [NIST ActEV §6](https://actev.nist.gov/pub/TRECVID_ActEV_2020_EvaluationPlan.pdf) miss/excess instance-time are useful diagnostics; excess instance-time is not UI notification count. [HOTA](https://arxiv.org/html/2009.07736v2) does not establish person-object ownership or physical danger. S004–S008/S067; F022/F023/F057.

### Event, alert, track, matching, exposure

**PROP:** GT stores `gt_event_id`, scenario/severity, camera/session/site, actor or actor-set, zone/rule version, onset/end, `first_observable`, boundary uncertainty, visibility/unknown, censoring. Onset and first observable differ; do not backdate observability after seeing the outcome. An alert has its own ID, event UUID, actor/pair hypothesis, source frame/crop IDs, decision/emit/receive timestamps and evidence. Raw tracker ID only links tracklets. F023/F060/F074/F177.

Freeze scenario/ignore/censor rules before matching. Fixture v0 uses one-to-one scenario/camera/actor/time matching: maximize timely cardinality, minimize total delay, then lexical `(gt_event_id,alert_id)`. Deadline is inclusive; event interval `[onset,end)` is half-open. One alert cannot match two GT; duplicates do not add TP. Correct late alert is `late`/eventual match, **not semantic FP**, but remains a deadline miss. Wrong actor cannot match; count corresponding unmatched GT and wrong-actor/FP burden. Keep semantic FP, duplicates, and all emitted notification counts distinct. Recall with no assessable GT and precision with no alerts are `N/A`. Detected-only latency p95 conceals misses; `RecallWithin(d)` uses all assessable GT. F008/F179.

Eligible exposure means authorized, in-scope readable source video with reviewable truth. **System downtime within available video stays in the denominator**; report system coverage and blind intervals alongside FP/H. Truly absent/unassessable source time is unknown, not TN. If EOF precedes the applicable deadline, apply predeclared right-censoring; if deadline already elapsed, a missing alert remains missed. Curated positive/ADL clips support only descriptive rate on fully reviewed negative intervals, otherwise `N/A`; they do not establish factory background rate or prevalence. F008/F025/F176/F180.

**INF algebra, not measurements:** all-negative prediction at prevalence 1/1000 gives 99.9% accuracy and zero recall. For the same defined unit, `PPV = πr/[πr+(1−π)f]`; precision from balanced clips does not transfer to rare-event streams. More adjacent frames do not create independent incidents. F024.

### Uncertainty and selection

Report TP/FN/FP, GT/alert counts, eligible hours, independent incidents/sessions/cameras, interval method/level, paired group differences, and seed variability separately. Wilson/exact binomial need appropriate independent trials, not pooled adjacent frames. Under independent Bernoulli trials with all n successes, one-sided 95% lower bound is `0.05^(1/n)`: **10/10≈0.741, 20/20≈0.861, 59/59≈0.9505**. These are algebraic illustrations, not results or an event quota. Under stationary Poisson assumptions, zero FP in H hours gives one-sided 95% upper rate `−ln(0.05)/H≈2.996/H`; ten hours imply approximately `<0.30/hour`, not zero error. Clustered light/steam/identity failures can violate that model. Few groups may leave variability unestimable; bootstrapping zero does not manufacture a reliable nonzero upper bound. Sampling phases share one group. Post-search DEV intervals are descriptive, not nominal winner guarantees. F025/F090/F107; [NIST TN2119](https://doi.org/10.6028/NIST.TN.2119), [Poisson model](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm), [selection overfit](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf).

## media-readiness

**OBS/DOC; F173–F181/S255–S258:** actual team inventory, event labels, exhaustive TRAIN, continuous negatives and independent LOCKBOX are unconfirmed. A concrete obtaining/reannotation path exists, not a ready benchmark.

- **URFD:** [primary dataset page](https://fenix.ur.edu.pl/~mkepski/ds/uf.html) describes 30 fall/40 ADL sequences and RGB/depth/view/synchronization distinctions; **CC BY-NC-SA 4.0**, academic/noncommercial use, commercial use needs separate agreement per source. Contest/demo/redistribution/deployment use needs owner's acceptance; no author contact occurred. Candidate [fall-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4) / [adl-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4): HEAD HTTP200/video/mp4, **1,299,104 / 1,194,846 bytes**. Full media bytes/hash/decode/content/PTS are absent. Last-Modified 2020-02-25 is file metadata, not incident date.
- **Received CSV:** [fall-01-data.csv](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-data.csv), **2466 bytes**, actual SHA256 `60e156223725e401155b4fd25a672c498ed5b4e17897337c6971d90041818bcc`, **160 rows**, frame **1…160**, time **0…5305 ms**, adjacent differences **33/34 ms**. First-to-last span **5.305 s** is not fall/lying duration or decoder FPS. MP4↔CSV mapping unknown; if inconsistent, prefer original PNG + documented mapping. A demanded ten-second hold cannot be inferred from this short sequence; shorter hold also needs visible post-state/EOF review.
- **CAUCAFall v5:** [card](https://data.mendeley.com/datasets/7w7fccy7ky/5), DOI **10.17632/7w7fccy7ky.5**, published **2025-03-18**, **CC BY 4.0**. Card describes AVI/PNG/TXT, fall/no-fall segmentation, nominal **23 FPS,1080×960**. Motion-trigger DVR starts on person entry: task clips do not supply continuous negative camera-hours. Card opened; Python/API returned403; exact AVI/PTS not acquired.

For first feasibility, accept and fully review one positive plus a comparable negative, then add exit/reentry/rearm, second actor, unknown gap as available; no invented statistical quota. Dense bbox/pose GT is optional for initial event replay but exhaustive relevant object labels are required for fine-tune. Store originals/hash/source/rights, parent incident/session/camera/subject lineage, frame index/timebase/PTS and timestamp origin. Annotate whole timeline `positive / verified_negative / unknown / out_of_scope`, onset/observable/end/censoring/actor, polygon/anchor/rule if applicable; second reviewer resolves critical ambiguities. Model output is not truth. F176/F177.

**Object package ≠ event package:** object training needs ontology/order, boxes/masks, visibility/ignore and exhaustive class/ROI coverage. Event evaluation needs uninterrupted source time, actor/event identity, temporal boundaries, verified negatives, deadline/matching/coverage. COCO JSON/segmentation alone does not supply the latter; clip event labels do not supply exhaustive detector supervision. F073/F074/F176/F177; Q001–Q004.

## data-roles

**PROP selected contract F004, K006 resolved:** mandatory roles are **TRAIN / DEV / LOCKBOX**. Current proposed URFD pair is **DEV only**, TRAIN empty, independent LOCKBOX absent. Do not create seven tiny subsets by adding CAL/TUNE/CHECK/SELECT terminology. All frames/crops/windows/synthetic descendants/phases and synchronized cameras of one incident inherit their parent group/split. Split by incident/session/camera/site according to the claim; new clip ID is not unseen camera.

| Decision | Allowed data and after-view status |
|---|---|
| Semantic/error audit, thresholds/dwell/gap/rearm, size/crop, checkpoint/model choice, export/decoder/quantization debugging | DEV; one incumbent + one prejustified alternative, logged views/trials. Development even without gradients. |
| Gradient training | TRAIN; checkpoint/early stop chosen on DEV. One B after gates; mutations create new identity. |
| Calibration | DEV; optional grouped CAL/folds within development if sufficient groups. Not required for A; fit/selection data are not independent confirmation. |
| Whole-system selection | Optional frozen SELECT only if independent groups genuinely remain; at most two pre-frozen complete bundles, no knob tuning. Any new threshold/router/rule makes it DEV. |
| Independent final evaluation | Previously unopened LOCKBOX after exact-bundle freeze; one planned evaluation. Fixing from its results absorbs it into DEV; a new independent claim needs new groups. |
| Refit TRAIN+DEV | Separate post-selection decision, not scheduled here; new checkpoint/bundle, UNVERIFIED status. Old artifact's pass does not transfer. |

Grouped CV is allowed **inside development** with fit/calibration/selection repeated within folds; it estimates the development procedure, not a newly closed test. Camera-specific override needs declared adapt-session and separate future evaluate-session; unseen camera receives common fallback and unverified generalization. Too few positives/groups/background → feasibility/raw counts/N/A, not random-frame confirmation. F004/F076/F083/F088/F091/F107; Q004/Q022.

## model-candidates

**CODE/PUB + PROP; no target ranking, actual binary load, 24 GB fit, or LinQ support established.** Candidate records use the declared `model_candidate` schema. Metadata hashes below are publisher/LFS digests, **not locally computed downloaded-model hashes**. Code/weight/data rights are separate. F005/F006/F014/F030–F047/F169/F183.

| role | identity_and_initialization | hypothesis_and_gate |
|---|---|---|
| Baseline D | Ultralytics **8.4.184**, source `de290d865035acbfa4bb24cc88960d8b52c26e45`; assets **v8.4.0/yolo26s.pt**, **20,422,725 bytes**, metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b` | First general-object/person frontend, optional single B. Accept AGPL/Enterprise use; verify actual useful features, same-head export, parity, deadline. Generic detections are not lying/fall/phone-use recognition. |
| Conditional C | D-FINE source `956d1709314c2c6a4df6f34de232054578a7449f`; M/HGNetv2-B2, four decoder layers; HF `Peterande/D-FINE@19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth`, **79,108,938 bytes**, LFS SHA256 `b44a7586bf490858c7b8bce9e44bd025cb88724df9a07a8deb3ae1c12e608195` | Only for residual **visible-object localization error** after label/visibility/final-pixel audit and one baseline spatial alternative. Need native init/right/export/device gates, meaningful event gain and reserve. No automatic O365/RF-DETR extra run. |
| Deferred pose | RTMPose-s, MMPose **v1.3.2**, source `5408bc76f5b848cf925a0d1857899011d8c5b497`; AIC+COCO17, H×W **256×192**; `rtmpose-s_simcc-aic-coco_pt-aic-coco_420e-256x192-fcb2599b_20230126.pth`, matching **project** config | Same person proposals, test large visible posture versus bbox-only events. Exact weight rights/SimCC path/visibility/crop cost remain gates; invalid pose is unknown, not safe. |
| Deferred V | timm **v1.0.22**, source `78c3724f4545c0067d0b4d2f7df6337196be01ce`; HF `timm/mobilenetv3_small_100.lamb_in1k@1824797e7887cbec1990e4adbd6675960a36c589/model.safetensors`, **10,241,912 bytes**, LFS SHA256 `46d2c063b18125884c48937afa4c49e18128869e52e8db96df48bf0a4d7ff697` | ImageNet1000 initializer only; proposed supervised `helmet_visible / bare_head_visible / unassessable` head. Need real-proposal TRAIN/DEV, proposal ceiling, threshold-only comparator, rights resolution and separate LinQ gate. |
| Export-research reserve | YOLOX-s source `6ddff4824372906469a7fae2dc3206c7aa4bbaee`, release **0.1.1rc0/yolox_s.pth**, HEAD **72,089,125 bytes**, actual hash unknown | Explicit CNN/ONNX/host-decoder alternative, not proven LinQ detection fallback. Exact checkpoint grant unresolved; current/legacy preprocessing differ; repeat full quality/runtime evaluation. |
| Deferred neural temporal | No accepted causal target checkpoint. TSM/online TSM, MoViNet, SlowFast, PoseC3D considered as architectures | Reopen only for a failure distinguishable by available **past frame order**, with target clips/labels, causal training/state/reset/export/license and reserve. A uses CPU FSM. |

Primary locators: [YOLO asset](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt), [D-FINE exact HF asset](https://huggingface.co/Peterande/D-FINE/resolve/19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth), [RTMPose project zoo](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/projects/rtmpose/README.md), [timm card](https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/blob/1824797e7887cbec1990e4adbd6675960a36c589/README.md), [YOLOX release](https://github.com/Megvii-BaseDetection/YOLOX/releases/tag/0.1.1rc0). S015–S037/S244/S254/S259–S272.

## benchmarks-and-rights

**PUB, not target evidence:** YOLO26s reports COCO AP **48.6 dense /47.8 e2e**, dense APsmall **29.5**, **9.5M fused** parameters. Author recipe: **Objects365v1 pretrain150 epochs → COCO S70**, batch128/input640/MuSGD. This is author lineage, not binary `train_args` inspection. Do not combine dense AP and e2e latency; T4/TensorRT latency is not LinQ timing. D-FINE-M COCO **52.3 AP/33.2 APsmall** versus O365→COCO **55.1/37.9** uses different exposure/recipes/capacity. Paper versus native YAML schedules differ: COCO **120+4 vs132/stop120**; obj2coco **29+49 vs56/stop48**. Qualitative D-FINE-X occlusion illustrations do not establish quantitative M performance on our people. YOLOX current AP40.5 is not legacy39.6; use matching preprocessing. F005/F168/F170; [YOLO26 paper](https://arxiv.org/html/2606.03748v1), [recipe](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/yolo26-training-recipe.md), [D-FINE paper](https://arxiv.org/html/2410.13842v1); S240–S254.

**INF:** before larger detector, measure bbox width/height in original and actual resized/letterboxed input. Test one larger whole-frame size **or** consistent ROI policy on the same checkpoint. Enlarging a tiny crop does not restore lost details. ROI fan-out, cut objects and queues belong in event/runtime cost. RF-DETR-M/L and RT-DETRv2 remain library alternatives, not extra scheduled jobs. F036/F167/F171.

**DOC, rights decision still UNK:**

- Ultralytics explicitly covers **code/models/docs under AGPL-3.0 or Enterprise**. Team must accept delivery/use/notices; README existence is not compliance. An incompatible proprietary delivery without alternate grant blocks that route. [License](https://www.ultralytics.com/license), S246; F006/F169.
- Exact HF D-FINE-M model repository has **Apache-2.0 model-level designation**, stronger than code license alone. Actual model bytes and GitHub/HF byte identity remain unchecked; same filename/size is insufficient. Native `PPHGNetV2_B2_stage1.pth` grant/conversion lineage unresolved. Constructor `pretrained=True` can download backbone **before** detector initialization; disabling it is a versioned modification requiring load verification, not automatic provenance clearance. [HF card](https://huggingface.co/Peterande/D-FINE/blob/19214e91f5ce4c1e609022c38b1fc953c47404e7/README.md), [backbone](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/nn/backbone/hgnetv2.py), S243/S244/S247; F006/F169/F170.
- YOLOX Apache code/release does not resolve exact checkpoint scope; [user issue1865](https://github.com/Megvii-BaseDetection/YOLOX/issues/1865) is not a maintainer grant or prohibition. RF-DETR Apache-designated N/S/M/L does not cover Plus/PML. DEIMv2/EdgeCrafter noncommercial terms exclude them from active portable shortlist until use is accepted. F006/F033/F037.
- [Objects365 terms](https://www.objects365.org/download.html) distinguish academic-purpose download, annotations/site CC-BY4.0, image rights. Preserve upstream scope for YOLO26/O365 initialization; this is **not** a newly inferred prohibition on all trained weights. S253.
- timm exact HF card says Apache-2.0 while pinned [project ImageNet-weights notice](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/README.md#licenses) restricts use: **unresolved official-statement conflict**. MMPose Apache code does not by itself establish grant for exact RTMPose weights/data chain. F044/F184; S259/S262/S037.

Retain exact code/license/card/notices/modifications, init/data lineage, actual bytes/hash/load. Q008/Q017 block only retained assets; deferred pose/V do not expand A's mandatory dependencies. These are source designations and open use decisions, not legal clearance.

## causal-time-and-tracking

**PROP:** A's CPU FSM is `normal/candidate/active/recovery` with explicit unknown/stale/gap/rearm policy. Use source seconds and fresh evidence, not update-call count, repeated cached frames, or summed confidence. N uniformly spaced observations at f span **`(N−1)/f`** from first to last; model stride and history duration differ. VFR/drops/bursts require real timestamps; positives across a long blind gap do not prove continuous dwell. An ideal sampler with period Δ and random phase can miss a distinguishing interval d entirely; the ideal one-hit illustration is not event recall. Replay several `φ∈[0,Δ)` phases around short-event boundaries using actual source frames and unique IDs; phases are not independent incidents. F009/F048–F054/F180; S049 [clocks](https://gstreamer.freedesktop.org/documentation/application-development/advanced/clocks.html).

Record `source_pts`, `available_at`, decode/inference start/end, decision, emit, receive. File PTS measures media time; physical exposure needs mapping. Without capture mapping call latency replay-to-receipt or the actual measured endpoint, **not glass-to-alert**. Include sampling/arrival, decode/preprocess, copies/queues, every neural node, tracking/rules/confirmation/delivery. Cached replay checks causal decisions, not actual LinQ wall deadlines. F052/F097/F180/F194.

**CODE:** first tracker candidate ByteTrack, one conditional comparator OC-SORT on identical detections/rules. ByteTrack's high-score association then low-score recovery needs low-score boxes preserved upstream. Pinned ByteTrack source `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`: frame ID increments per update, buffer scales `frame_rate/30*track_buffer`, Kalman `dt=1`; OC-SORT `8462e7e729a93ccd3bd995c0a79a890336cb3a0b` also has step-based age/history. Sparse updates versus empty updates produce different behavior: frame buffer is not seconds without a scheduling/adapter decision. Offline interpolation sees future endpoints and is not online evidence. ReID is a further neural node requiring observed event benefit and target gate. F055–F058/F062; [ByteTrack code](https://github.com/FoundationVision/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99), [OC-SORT code](https://github.com/noahcao/OC_SORT/tree/8462e7e729a93ccd3bd995c0a79a890336cb3a0b), S053–S061.

**PROP event identity:** event UUID stores tracklet aliases, camera/stream epoch, actor/pair, notified/unknown/rearm history. Causal confident reassociation preserves ongoing event; a new raw ID does not authorize duplicate notification. Ambiguous merge must not transfer A's evidence to B. Global cooldown must not suppress a second actor. One missing detection/unknown does not end violation or establish positive support; rearm needs declared fresh negative evidence. Person-object relation confidence is separate from detector/track confidence; permit `unassigned`. Helmet in hand is not `worn_by`, nearest phone is not proven owner/use, invisible head is not `bare_head_visible`, projected vehicle overlap is not metric proximity/contact. F059/F060/F063/F179.

### C01–C10 synthetic acceptance, specification only

**PROP/UNRUN F179:** runner does not yet exist. Fixture v0 constants are **unit-test constants, not industrial recommendations**: `D=2.0s`; two fresh positives with `t2−t1>=0.5s`, positive gaps≤0.75s; unknown breaks candidate support but does not rearm ACTIVE; fresh negatives spanning1.0s with gaps≤0.75s rearm. Unique source IDs only; stale/extrapolated duplicates give no support. Emit at actual decision, no backdating. Late grace after event end is zero. Matching follows quality-contract.

| Fixture | Isolated expected behavior |
|---|---|
| C01 | A `[1,8)`, positives1/1.5→emit1.5 timely1; evaluator boundary emit3.0 also timely. |
| C02 | Same GT, alert3.01→timely0/late1/deadline-miss1/eventual1, no semantic FP. |
| C03 | Ongoing A, alerts1.5/2.0→timely1/duplicate1; production FSM emits only first. |
| C04 | A `[1,8)`, B `[2,7)`, positives1/1.5 and2/2.5→two timely alerts. |
| C05 | A `[1,3)` then `[5,8)`, negatives3/3.5/4 and new positives5/5.5→two UUIDs/timely alerts. |
| C06 | Causally available x1→x2 bridge for A, positives1/1.5 then x2 at2→one alert, emitted flag retained. |
| C07 | A/B tracker merge ambiguous→no fabricated ownership bridge; unresolved B by4 remains deadline miss; one alert cannot cover both GT. |
| C08 | Positive1, unknown1.2…3, positives3/3.5→emit3.5 late; unknown after ACTIVE neither rearms nor creates return duplicate. Unknown GT gap is not verified-negative exposure. |
| C09 | GT `[1.1,1.4)`, negative samples1.0/1.5→missed1; do not extend positive duration to next sample. |
| C10 | Onset7/EOF8/deadline9→right-censored1; onset5.5/EOF8/deadline7.5→missed1. |

Require exact counts/UUID/rearm/causal cutoff/censoring and row-order-invariant matching; any mismatch blocks threshold tuning. Save fixtures/config/expected/actual/diff. E002 then tests **oracle real observations first**, followed by frontend on the same timestamps, immediate versus one FSM, native grid versus one Δ plus phases. Oracle failure diagnoses scope/time/evidence; frontend-only failure diagnoses model/features. E003 separately measures actual device wall clock. F179–F181; [full corpus](_WORK/W2_D.md).

## thresholds

**PROP/INF:** start identity scores + tuned class/event thresholds; compare one FSM before new training. Calibration is a separate hypothesis versus already tuned thresholds. A strictly monotonic scalar map before aggregation preserves ranking and attainable scalar-threshold decisions; ECE improvement alone cannot improve that frontier. Numerical pooling/routing may alter this and needs full-pipeline evaluation. Detector/relation/event scores are not interchangeable probabilities. F085–F088; [Guo et al.](https://proceedings.mlr.press/v70/guo17a.html), [detection calibration](https://arxiv.org/abs/2004.13546v1); S101/S102.

DEV sweeps freeze bundle/class map/sampling/matching and `Rmin_c/B_c/D_c`. Cache below every tested floor and before irreversible suppression when comparing NMS: cache floor0.3 cannot test0.1; hard-NMS-deleted boxes cannot be recovered. New graph/head/quantization/decoder requires score and event re-evaluation. Per-camera fitting needs independent positive/negative groups, not many correlated frames. Camera onboarding uses adapt-session→separate evaluate-session. Unlabeled production score drift/alert reduction is not precision; emitted-alert-only feedback misses false negatives, so independently review random continuous intervals. F087/F088/F091/F092; [threshold documentation v1.5](https://scikit-learn.org/1.5/modules/classification_threshold.html), S105/S106.

For postprocessing preserve threshold inclusivity/ties/routing; higher threshold does not guarantee finite-sample event precision monotonicity through tracking/FSM. Hard NMS needs class-aware IoU/top-k/coordinate policy; class-agnostic suppression can remove nested person/PPE. E2e head is not arbitrary dense+NMS. Soft-NMS linear/Gaussian are different hypotheses with Nt/sigma/cutoff and retuned scores. Persistence/hysteresis can confirm persistent FP, erase short TP and increase latency; count fresh observations and max age/gap. WBF fixes neither missing proposals nor semantics universally and can merge people/move boxes across zones. Preserve exact constituents, class/coordinate/score mapping, fusion weights/IoU/threshold and target cost. F089/F095/F096; [Soft-NMS](https://arxiv.org/abs/1704.04503v2), [WBF](https://arxiv.org/abs/1910.13302v3), [pinned implementation](https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/ensemble_boxes/ensemble_boxes_wbf.py).

## adaptation

**PROP:** build a human-reviewed DEV error atlas before B: missing/wrong GT, unobservable state, lost input pixels, object class/localization, ownership, rule, sampling, queue/delivery. Confident unlabeled proposal may be missing annotation, not hard negative; large loss on wrong GT is not useful supervision. Mine only TRAIN/unlabeled development pool; moving DEV example into TRAIN consumes that independence. Group near-duplicate failures. Mix confirmed FP, independently reviewed FN, uncertain/diverse cases and random audit; no universal optimal ratio established. F070–F079; [TIDE](https://arxiv.org/html/2008.08115v2), [CLOD](https://arxiv.org/html/2211.13993v3), [Co-mining](https://arxiv.org/html/2012.01950v2), S084–S087.

Use matched distractors/positives: person vs mannequin/poster/reflection; phone vs radio/scanner/tool; deliberate lying/lying repair vs visible fall transition; stationary vs moving vehicle with optical-axis ambiguity. A stationary person is not mannequin, phone bbox is not use, stationary image bbox is not proof of no motion. Add distractor class only if trainer/downstream supports it; otherwise preserve QA taxonomy separately. Completeness is `(asset/interval,class,ROI)`: unreviewed/partial/exhaustive/ambiguous, verified absent classes, ignore/visibility, reviewer/version. Missing class annotation differs from missing instances of a known class; class masks do not fix an omitted person. PPE-only labels cannot imply phone-negative. `iscrowd` is not universal ignore. For small B, prefer fully reviewed bounded TRAIN subset. F072–F075; S088–S090.

Annotator instructions, disputed-example pilot, independent critical-boundary review, reason codes; machine checks timestamps/boxes/classes/ID collisions/duplicates/coverage while humans scan full frames and transitions. Bbox interpolation does not establish action between endpoints. Future frames may help human GT labeling, never causal runtime. Compare targeted QA/mining with random/diverse annotation at equal **human budget**, plus same-length continued-training control to separate data gain from extra steps. Record new independent groups and real-DEV retention. Mined examples do not estimate prevalence; OHEM chooses training RoIs and is a different algorithm. F074–F077; [CVAT QA](https://docs.cvat.ai/docs/qa-analytics/quality-control/).

### One fine-tune recipe and ontology retention

**PROP, not optimized/tested:** candidate YOLO B starts `yolo26s.pt`, input640, full FT, explicit AdamW, **`lr0=3e-4`, `freeze=0`, `warmup_bias_lr=0.0`, weight_decay=5e-4, `cos_lr=False`, `lrf=0.01`**. Btrain/Bval/accumulation/AMP/stop/warmup/augmentations follow data audit and actual qualification. W1 warmup1–3, 20/50-epoch windows and `nbs=16` (native default64) are alternatives/deviations, not simultaneously selected or sufficient guarantees. `optimizer=auto` invalidates a claim of unchanged hand-selected LR. F065/F066/F162; [pinned defaults](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml), [guide](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/finetuning-guide.md).

Preserve needed ontology/class order, transfer key log, replay rights and retention DEV; keeping backbone does not retain a changed head's classes. Helmet/vest-only output cannot still detect person/phone/vehicle by assertion. D-FINE `map_class_weights` may copy same-shaped tensors wholesale; COCO↔O365 mapping is not arbitrary helmet/vest/harness semantics. Log matched/unmatched/remapped keys and test `id→name→output`; unexpected missing backbone keys stop. Freeze→unfreeze is conditional alternative, not second mandatory B: YOLO `freeze=11` freezes whole backbone;10 leaves C2PSA. Stage2 from stage1 best is new phase/recipe with `resume=False`, not same optimizer continuation. D-FINE `-t` tuning≠`-r` resume; shortened epochs need coordinated native transforms/stop_epoch/clean phase/EMA. F064–F069/F163/F164.

### Augmentation for a named failure

**PROP:** record native defaults first; default Mosaic/HSV is not “no augmentation.” Test one bounded light/contrast, blur/compression, or spatial policy tied to actual failures, with previews, labels/visibility/ROI, final-pixel distributions and dropped-target counts. Separate clean real DEV, real nuisance slices and synthetic corruption; synthetic-only gain is not camera transfer. Video geometry must be clip-consistent and transform boxes/keypoints/zones/relations together. Per-frame jitter invents motion/flicker; time crop/drop/speed change needs real-time remapping. Reversal can turn fall into rising; shuffle destroys order; vertical flip changes posture semantics; repeat frames do not make fresh evidence. Cross-video Mosaic/MixUp/CutMix is excluded from event baseline. F080–F084; [pinned augmentation](https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/data/augment.py), S097/S098.

Copy-Paste needs masks/rights and correct relation labels; helmet on floor differs from worn helmet. Published COCO gains coexist with small-VOC/pasted-small-object negative cases, not universal improvement. Procedural rendering, mask-aware pasting and random text-to-image provide different label reliability. Prompt text is not GT; synthetic human/PPE anatomy/contact/occlusion/object count/provenance/rights need audit. Defer mass synthesis before a demonstrated data gap. F080/F082/F083; [Copy-Paste](https://arxiv.org/html/2012.07177v2), [small objects](https://arxiv.org/html/1902.07296v1), [DomainBed](https://arxiv.org/html/2007.01434v1).

### Specialists, cascades, temporal models

**INF:** for true event E, timely proposal G, verifier acceptance A, remaining-chain preservation H, `R_event=P(G|E)·P(A|G,E)·P(H|A,G,E)≤P(G|E)`; no independence assumed. Frame recall×accuracy on ideal GT crops is not this quantity. Measure real event-level proposal ceiling, selective/abstain route, threshold-only comparator and fan-out/burst cost. OR ensemble adds proposals/FP, AND limits recall, WBF can merge actors; teacher agreement is not GT. Distillation removes online teacher cost only when teacher actually absent. Every online learned node requires separate rights/export/placement/parity/load/state gate. F094–F099/F187; [NoScope §4](https://people.eecs.berkeley.edu/~matei/papers/2017/vldb_noscope.pdf).

**CODE V:** RGB FP32 NCHW224², `/255`, ImageNet mean `(0.485,0.456,0.406)`, std `(0.229,0.224,0.225)`, bicubic, `crop_pct=0.875`. Initial logits1000 are not target classes. New three-class head needs supervised TRAIN; `unassessable` means abstain. Native center crop may cut helmet; changed crop geometry is new train/eval/export recipe. timm `--pretrained-path` can replace1000→3; strict `--initial-checkpoint` is not equivalent. Native ONNX dynamic-batch/default-mode behavior needs an explicit unbuilt static1 legacy adapter. Classifier is stateless; per-track cache/FSM still needs reset. F183–F185; S261/S263–S266.

**CODE pose:** exact `projects/rtmpose` config/checkpoint must match; similarly named `configs/` recipe is not interchangeable. H×W256×192 vs `input_size=(192,256)` W×H. Preserve crop affine/padding/inverse mapping/bbox→track link after NMS, per-feature confidence/valid/age. Invalid joint is not `(0,0)`; shoulder–hip angle is projected2D, not gravity/3D biomechanics/consciousness/contact. F041–F046.

**CODE temporal:** ordinary TSM shift reads `t+1`; switching sampling cannot make arbitrary weights causal. Official online demo uses different `mobilenetv2_jester_online.pth.tar`, **27 Jester classes/10 state buffers**, `[frame,states]→[logits,next_states]`. TVM `tvm.nd.empty` gives no zero-reset guarantee; per-person lifecycle not demonstrated. This is a static missing guarantee, not observed failure. No accepted causal target checkpoint; neural temporal deferred. F186; [shift](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/ops/temporal_shift.py), [online main](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/main.py), S267–S270.

## export-envelope

**PROP, source-backed/UNRUN F007/F160–F166:** Linux x86_64, **Python3.11.9, Torch2.5.1, torchvision0.20.1**; official **cu124** pair for training, same core's **CPU wheels** in separate export env. Isolate projects/extras. Pins **NumPy1.26.4, ONNX1.17.0, ORT CPU1.20.1, OpenCV4.10.0.84**; D-FINE ancillary **transformers4.44.2/calflops0.3.2**. Full transitive resolve/hash lock/install/`pip check`/imports/checkpoint load are not done. ORT1.20 row supports opset21/IR10 as a version bound, not our kernels/parity or LinQ. W1 Torch2.14.1 Docker metadata was a genuine candidate, not installed common environment. Conditional fallback **Torch2.4.1/vision0.19.1** requires separate manifest after localized need. Torch2.6 changed `torch.load(weights_only=...)` default: compatibility risk for trusted checkpoint, not observed universal D-FINE failure. [Torch versions](https://pytorch.org/get-started/previous-versions/), [2.6 release](https://github.com/pytorch/pytorch/releases/tag/v2.6.0), [ORT compatibility](https://onnxruntime.ai/docs/reference/compatibility.html); S218–S239.

**YOLO first floating proposal:** static batch1, FP32,640×640,CPU, **`dynamic=False,simplify=False,half=False,nms=False,opset18`**, explicit **`dynamo=False`**. Pinned supported YOLO26 head with `nms=False` selects e2e/one-to-one; `[B,K,6]` expected, actual graph/head/IR unknown. NMS-free retains potentially sensitive TopK/Gather. Conditional dense export (`nms=None` in examined path) only if actual one-to-many weights remain; fusion cannot recreate them. It is a new head/bundle/reference, not arbitrary decoder substitution. F007/F035/F147/F162; [exporter](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py), [head](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py).

**D-FINE source:** EMA.module if available else model→deploy+postprocessor; inputs **`images`,`orig_target_sizes`**, outputs **`labels/boxes/scores`**. Preserve size dtype/order, coordinate frame and decoder. Native **opset16**, dummy batch32/dynamic axes are not static1. **`--simplify` uses `store_true` with defaultTrue; omitting flag does not disable it.** Proposed versioned static1 adapter sets `dynamo=False,dynamic_axes=None`, simplification opt-in; **not built/run**. timm native exporter likewise uses dynamic batch/inherited Torch default; proposed V static1 adapter unbuilt. F147/F163–F165/F185; [D-FINE exporter](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py), [postprocessor](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/zoo/dfine/postprocessor.py).

Before expensive training: trusted init load→same-head reference→export→checker+numerical ORT→operator inventory→issued SDK diagnostic. `onnx.checker` is structural, not numeric equivalence; ORT is not TPU. Preserve unsimplified graph/sidecars. Final selected checkpoint must repeat affected gates. No graph/export/device gate passed in this research. Q008/Q018.

## experiment-program

**All PROP/UNRUN.** Active order **E001→E002→E003/E004**; SDK work may parallel media preparation. B waits for data and target path, E005 before B/recovery, E006 the single B. Other rows are conditional library alternatives, **not a cumulative schedule**. Predeclare meaningful gain, constraints, time/budget and stop before observing results. No universal AP stop criterion exists. Full procedures: [RAW_FACTS E catalog](RAW_FACTS.md); F019.

| id_priority | control_and_factor | inputs_and_measures | stop_and_evidence |
|---|---|---|---|
| E001 now | Oracle ledger vs policyv0/FSM matcher | Synthetic C01–C10; exact timely/late/miss/duplicate/actor/rearm/censor | Any mismatch blocks tuning; save fixtures/config/expected/actual/diff. PASS only logic. |
| E002 now | Oracle→frontend same policy; separately immediate→one FSM, native→one Δ/phases | Authorized decoded DEV/PTS/events; timely/late/missed/censored, fresh evidence, negative seconds/duplicates | No time map→no time claim; oracle failure→scope/schedule; frontend failure→model. Media/label hashes/time map/schedule/cache/ledgers/view log; not factory rate or LinQ timing. |
| E003 mandatory target | Issued serial vendor sample→our same-head graph→full pipeline | SDK/golden tensors/DEV; compile/load/schema/placement/parity/reset/state/real queue/delivery | Mandatory neural node unverified→no final PASS; SDK/env/op/compiled hashes/raw outputs/trace. Sample PASS≠detector PASS. |
| E004 before heavy B | Pretrained export-first in frozen envelope; representative train+val fixture on actual host | Resolve/import/trusted load/head/IR/ops; actual B/AMP/work/train+val peaks/save/reload | Paid step requires separate authorization; incompatible env→new manifest; OOM recovery≠fit. Lock/wheels/source+patch/config/graphs/tensors/hardware logs. |
| E005 before B/recovery | Disposable stock control vs pinned fail/fork guard; corrupted second copy | Tiny TRAIN/synthetic and external endpoint; OOM inclB1/start+later NaN/EMA-half repair/AMP/pending accumulation/archive | Mutation cannot pass clean comparison; FAILED_TECH or TRAINED_UNARCHIVED; persistent events/list/bytes/hash/trusted-load receipt. Not exact resume/RPO proof. |
| E006 single B | Frozen pretrained A vs one fine-tuned B, same event pipeline | Exhaustive TRAIN + DEV; timely quality at same FP/deadline/coverage, retention, actual work/cost | Missing labels/rights/runtime→no start; no meaningful event/retention gain→keep A. Init/load/split/config/curves/progress/checkpoint/raw predictions/target gate. |
| E007 conditional C | Same checkpoint640 vs one spatial policy first; residual visible localization error→D-FINE-M whole-product comparator | Fixed DEV pixel/visibility/error atlas; object/occlusion/event paired slices and runtime | Missing information/reserve→stop; retain crop/resize policy/raw outputs/FN gallery/pixel+compute costs/bundle. Not pure architecture ablation. |
| E008 one data hypothesis | Continued-training + equal annotation-budget control; targeted QA/mining OR one augmentation | TRAIN mining/labels + DEV; object/event retention, human effort, real slices | Partial labels/semantic damage→stop; annotation/reviewer/version/transform/previews. Synthetic AP/loss≠real transfer. |
| E009 association error | ByteTrack→OC-SORT, identical detections/rules | Causal DEV cache/PTS/owner GT; wrong-owner/timely/duplicate/rearm, IDF1/HOTA diagnostic | No event benefit→keep simple; track/alias/UUID/config logs. No offline interpolation as online result. |
| E010 deferred pose | Bbox rules→RTMPose-s, same proposals | Grouped DEV visible joints/events; timely/FP/unknown/occlusion/crop cost | Invalid pose/proposal/target path→abstain/defer; exact config/weights/crops/raw pose/events/node logs. Not consciousness/metric-geometry proof. |
| E011 deferred V | Tuned D+FSM vs strict/selective supervised3-head V | TRAIN crops, real-proposal DEV; event proposal ceiling, same timely recall/deadline FP, abstention/fan-out/bursts | No named error/labels/rights/device/gain→defer; init/head/route/crop/export/cache/reset/events/target. GT-crop accuracy insufficient. |
| E012 conditional GPU2 | Isolated1GPU→ready joint independent jobs; DDP separate recipe | Separately authorized actual resources; valid-result wall time/full cost/CPU/RAM/I/O/VRAM/work | No ready work/reserve or joint slowdown→1GPU; offers/state timeline/traces/receipts/Charges. Samples/s≠quality gain. |

Large HPO/ASHA is deferred. ASHA needs informative early scalar rank and enough parallel search; 1–2 GPUs do not inherit published acceleration. Multi-stage late rank can differ; trial completion order changes pruning. Same epochs need not mean same applied updates/exposure under retry/accumulation/oversampling. Exploration and confirmation differ; Optuna/Ray cannot create data or independence. F100–F109; [ASHA](https://arxiv.org/html/1810.05934v5), [Hyperband](https://jmlr.org/papers/volume18/16-558/16-558.pdf).

## gpu-schedule

**PROP F016/F135–F144:** one RTX3090 is default for authorized work, possibly no training if gates fail. Prepare data/CPU export/SDK before rental; actual host qualification→one B→native validation/save/receipt→event evaluation. QA/product/LinQ run in parallel on team roles. A successful forward is not backward/optimizer/EMA/native-val fit; representative dense/worst-shape train **and validation**, save/reload must be measured. Record peak allocated/reserved, Btrain/Bval, AMP/optimizer, input/max objects, CPU/RAM/shm/DataLoader/decode/augment/disk/network, step/val/save/reload durations and mutations. New batch/shape/env→new manifest/relevant qualification. RTX4070 unknown setup is not proxy proof. Q009.

Two GPUs are conditional for ready independent frozen jobs/paired seeds or a ready eval queue; test isolated vs joint CPU/RAM/disk/network contention including transfer/archive. Native validation affects best/EMA/stopping/stages and cannot silently disappear. DDP keeps **replica per GPU**, not a48GB pool; accumulation does not reproduce physical batch/BatchNorm. Changed global batch/sampler/cadence is new recipe; compare convergence and time-to-valid-result/full cost, not samples/s. Multi-node adds network/recovery; D-FINE global-rank→CUDA-device risk is source-inferred, no ready fallback launcher. [DDP documentation read v2.14](https://docs.pytorch.org/docs/2.14/generated/torch.nn.parallel.DistributedDataParallel.html), [D-FINE utility](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/misc/dist_utils.py), S181–S192.

Rental GPU2 is justified by **completed admissible decisions before freeze** and measured mandatory reserves, not utilization. One saved2GPU offer had only8 effective CPU and `bw_nvlink=0`; no ×2 promise. If labels/SDK/evaluator are bottleneck, more CUDA is not the remedy. Q022.

## vast-offers-and-costs

**OBS historical only F011/F111; S145:** unauthenticated public GET [bundles API](https://console.vast.ai/api/v0/bundles/) returned HTTP200 **2026-10-23 17:04:35–37 UTC /20:04:35–37 MSK**. Filter RTX3090,num_gpus1/2,verified=true,external=false,rentable=true,**rented=false**,reliability≥0.99,disk_space≥100,allocation100,on-demand,order dph_total,limit3. W2 did not refresh market. Rounded USD values below are observed metadata, **not purchase/reservation, ongoing availability, actual invoice, or guaranteed rate**. [1GPU raw](_WORK/W1_12_MATERIALS/offers_1gpu_100gb.json), [2GPU raw](_WORK/W1_12_MATERIALS/offers_2gpu_100gb.json).

| Offer/machine | GPUs/region | Whole-offer compute $/h | Allocation100 disk $/h | Running total $/h | Ingress/egress $/TB |
|---|---|---:|---:|---:|---:|
|55729405/28164|1/India|0.186667|0.031481|0.218148|0.666667/0.666667|
|45174323/144003|1/CN|0.213333|0.027778|0.241111|2.666667/4.000000|
|47272935/36023|1/Taiwan|0.240000|0.027778|0.267778|26.666667/26.666667|
|45174324/144003|2/CN|0.426667|0.027778|0.454444|2.666667/4.000000|
|56506123/117305|2/Oregon|0.480000|0.055556|0.535556|4.000000/6.666667|
|57219980/140986|2/Taiwan|0.533333|0.027778|0.561111|2.666667/4.000000|

45174323/24 share machine144003; six rows are not six independent hosts. All snapshots report verified/hosting_type0 and `bw_nvlink=0`; Secure Cloud/NVLink not established. Reliability is platform field, not measured probability of our successful run. First offer fields include18 effective CPU, `cpu_ram=64322`, driver580.126.09,power300W;56506123 includes8CPU/275W. These and24576MiB GPU metadata are not hardware benchmarks. F111.

**PROP cost ledger F011/F112/F200:**

```text
C_vast = G*Trun + Srun(D)*Trun + Sstop(D)*Tstop
       + Bin*Vin + Bout*Vout
       + sum(separate_volume_rate_i*billable_hours_i)
       + other_documented_state_or_service_charges
C_project = C_vast + external_storage + external_egress
          + applicable_payment/FX/tax
```

G is **whole-offer** compute, D allocation, storage rates depend on state, transfer quantities use verified units. Snapshot `dph_total=dph_base+storage_total_cost`: do not add running disk twice or multiply multi-GPU dph_base by GPU count again. Observed `storage_total_cost=storage_cost*D/720` is JSON arithmetic, not universal month length. Nested quote `instance.gpuCostPerHour=0` does not establish a free period. CLI `--storage` says **GiB**, storage field help **$/GB/month**, billing **$/GB/hour**, network **$/TB**: exact byte divisors unknown; do not mix SI/TiB. Ingress enters rented host; egress leaves it, including checkpoints to archive/LinQ. Dataset/weights/packages/retries/setup/idle allocation/snapshots/optimizer/predictions/volumes/external side count according to actual metering; image-pull/loading scope unresolved. F112/F199/F200.

| Resource state | Documentary charge and unresolved boundary |
|---|---|
| Running/active connected | Whole-offer compute + allocation storage + metered network; idle/0% GPU does not discount paid preparation. |
| Loading | Compute inactive; **current FAQ includes online storage while current Billing/Manage say no charge**. Current-current conflict persists; do not claim loading fully free or infer transfer scope. |
| Stopped online | Compute inactive, storage continues and may be more expensive than running. Not backup/GPU reservation; restart availability uncertain. |
| Offline | Current Billing/FAQ exempt active/storage; legacy FAQ charges offline/broken storage. Current precedence is documentary choice, not observed bill; reserve conservatively, no outage-as-discount assumption. |
| Expired | Stopped contract/restart prohibited; possible deletion after48h. Exact expired rate unknown;48h is not backup SLA. |
| Destroyed instance | Container data deleted; separate volumes and delayed ledger may remain. Verify end of charging. |
| Separate attached/detached volume | Separately billed, survives instance destroy; separate identity/rate/lifecycle. |

F113/F199; [current Billing](https://docs.vast.ai/guides/reference/billing), [current FAQ](https://docs.vast.ai/guides/reference/faq/billing), [legacy FAQ](https://console.vast.ai/faq/), [Manage](https://docs.vast.ai/guides/instances/manage-instances), [Storage Types](https://docs.vast.ai/guides/instances/storage/types); S282–S290.

Before purchase refresh query/full raw+UTC and capture offer/machine/host/contract/end_date,type/region/reliability,GPU count/VRAM/driver/power,CPU/RAM/shm,PCIe,disk allocation/free/bandwidth,network/ports,running/stopped/storage/transfer rates+units. Owner must authorize total/time/resource/lifecycle limit, verify account/payment/autobilling and archive endpoint. **Balance is not spending cap**; unknown tax/FX/payment terms prevent assigned RUB total. Include failed attempts/bootstrap/idle/archive/recovery reserve. No account read or spending occurred. F115/F198/F200; Q013–Q016.

[Show Charges](https://docs.vast.ai/api-reference/billing/show-charges) has resource `type/source`, intervals/items **gpu/disk/bwd/bwu**; [Invoices](https://docs.vast.ai/api-reference/billing/show-invoices) report payments/top-ups, not usage. Fetch all raw pages via `next_token` until null with same UTC filters; avoid double-counting inclusive adjacent windows. Delayed correction/rounding means tiny zero does not prove exemption. Reconcile state timeline/resource inventory/rates and later ledger, retaining private raw separately. Exact units/divisors/loading/offline/expired billing and account terms remain Q015. F012/F199/F200; S286–S288.

## vast-cli

**OBS/CODE F012/F197–F198:** actual received wheel **v1.9.0**, release **2026-10-20T21:31:52Z**, source `28bde4827374ef658694db5a1e1e61508b966e2f`, **`vastai-1.9.0-py3-none-any.whl`**, **324493 bytes**, actual SHA256 **`dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b`**, matched release metadata; entry **`vastai.cli.main:main`**, **Python>=3.10,<4.0**. Wheel bytes/static inspection are real; installation/import/control-env dependency lock are UNRUN. [Release](https://github.com/vast-ai/vast-cli/releases/tag/v1.9.0), [wheel](https://github.com/vast-ai/vast-cli/releases/download/v1.9.0/vastai-1.9.0-py3-none-any.whl); S276/S277.

**Critical correction:** modular wheel copy uses subprocess **argv list, not `shell=True`**; legacy `vast.py` claim does not apply. **Unchecked returncode** and **`StrictHostKeyChecking=no`** remain. Destroy has **y/N prompt**, not archive verification. Search default omits **`rented=false`**, add explicitly. Explicit `local:path` has different dispatch from unprefixed Unix path; Windows pip does not install rsync/ssh or convert drive paths to POSIX. Use accepted trusted-host-key transport; copy initiation/exit0, actual resource state and independent archive receipt are separate. [storage source](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/storage.py#L78), [offers source](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/offers.py#L127); S278–S281.

**DOC examples, NOT EXECUTED:** future Linux/WSL control host, installed verified wheel, owner-configured account; IDs/paths/UTC bounds placeholders. Record actual CLI path/version/Python/OS/resolved dependencies. Keep secrets out of reports/images/public logs; raw show responses may include connection tokens/extra_env/onstart, redact review copies while retaining private evidence.

```bash
.venv-vast190/bin/vastai search offers 'gpu_name=RTX_3090 num_gpus=1 verified=true external=false rentable=true rented=false reliability>=0.99 disk_space>=100' --type on-demand --storage 100 --order dph_total --limit 3 --raw
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
.venv-vast190/bin/vastai show instances --raw
.venv-vast190/bin/vastai show volumes --raw
.venv-vast190/bin/vastai show invoices-v1 --charges --start-date START_UTC_UNIX --end-date END_UTC_UNIX --limit 100 --raw
```

For further Charges pages append `--next-token NEXT_TOKEN`. [Billing CLI](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/billing.py); F198/S288.

**NOT EXECUTED lifecycle examples**, only under future authorized lifecycle scope, with independent checks **between** commands; not an automatic destructive script:

```bash
.venv-vast190/bin/vastai copy INSTANCE_ID:/workspace/archive/run_id/ /srv/team_archive/run_id/
# Verify independent external list/bytes/SHA256/trusted-load receipt first.
.venv-vast190/bin/vastai stop instance INSTANCE_ID
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
# Only when separately needed and resource available:
.venv-vast190/bin/vastai start instance INSTANCE_ID
# Only after verified receipt and separate lifecycle decision:
.venv-vast190/bin/vastai destroy instance INSTANCE_ID
```

Trailing slash copies directory contents under documented transfer protocol. Accepted stop/start request is not actual stopped/running: poll. After destroy reconcile instance absence, remaining volumes and delayed Charges. SCP is not universal substitute when sshd unavailable/stopped. Wheel prompt/exit cannot prove archive integrity/trusted origin. [Data Movement](https://docs.vast.ai/guides/instances/storage/data-movement); F198/F199/S279/S289.

## recovery-and-registry

**CODE F010/F153–F159; proposed guard/drill UNRUN:** pinned Ultralytics first-start-epoch single-rank OOM/backend retry can halve batch to1, retry even batch1, retain already modified optimizer and repeat work. Later NaN can restore last EMA/replay epoch; start-epoch behavior differs. Save can repair live EMA and sanitize half copy. Finite checkpoint/ordinary CSV/exit0 do not establish clean immutable trajectory. Stock `fail_on_oom`, `disable_oom_recovery`, `nan_recovery=False`, `max_retries=0` disabling flags were **not established**. `amp=False`, `resume=False`, integer batch do not disable all recovery. Reserved `optimizer_step`/`on_before_zero_grad` callbacks are not dispatched by stock loop; step post-hook is not applied-update proof in fused AMP. Count attempts/calls/applied separately; applied count remains **null** until observer validated on chosen core/optimizer. [Trainer](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), [callbacks](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/callbacks/base.py), [torch_utils](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py); S210–S217.

Accumulation can leave pending gradients at epoch boundary; mandatory tail flush is not established and snapshot does not serialize them. Resume changes zero_grad/local cadence; EMA/half/RNG/sampler/loader cursor/raw optimizer do not form lossless replay. D-FINE native stage1-best reload/EMA change belongs to declared recipe, but unexpected nonfinite remains technical failure; writing `NaN.pth` alone does not stop AMP loop. Exact replay/controller platform is deferred. F010/F126/F157/F164.

**PROP registry statuses, not vendor flags:** OOM/NaN/save repair→`FAILED_TECH` for immutable comparison; useful salvage as child `RECOVERED_NONCOMPARABLE`; native EMA resume→`RESUMED_APPROX`; B/AMP/shape/optimizer change→new recipe/init run for clean ablation. Unexplained gaps→`INCOMPLETE_OBSERVABILITY`; absent external loadable copy→`TRAINED_UNARCHIVED`. `SUCCEEDED_COMPARABLE` requires declared work/allowed stop, no disqualifying mutation, sufficient observability, accepted validation and verified external archive; license and target acceptance remain separate. Epoch×dataset, EMA count or hook count cannot invent applied updates. F010/F015/F155/F158.

### Minimal proposed runbook and persistent records

1. **Prepare before rental:** source+patch, accepted weight/license/init/class map/load policy, exact data/labels/splits/lineage/time hashes, one recipe/stop/mutation policy, source-backed constraints→future resolved hash lock/image, budget/owner/external destination; available pretrained CPU export mechanics. No credentials in image/public manifest.
2. **Authorized bootstrap/qualification:** offer/contract/state, GPU UUID/VRAM/driver/CPU/RAM/shm/disk and actual packages/image; verify inputs. Test representative forward/loss/backward/optimizer/EMA/native-val/save/reload/export with physical train/val B and no hidden recovery. Tiny synthetic inputs prove mechanics only.
3. **Immutable run:** separate requested/resolved/effective configs; append phase/source-group/work/attempt-call-applied-or-null/LR/AMP/accumulation/mutation/warning/validation/checkpoint events, raw predictions and fixed DEV event metrics. Native “best” internal metric need not be best timely-event bundle.
4. **Snapshot before stripping:** close consistent native checkpoint, copy under immutable name before final `last/best` stripping; record run/attempt/parent, file list/bytes/hash/expected native state. Recovery snapshot and selected inference artifact have different roles/IDs.
5. **External acceptance:** independent destination reader verifies complete list/bytes/SHA256 and trusted trainer/environment load for expected identity/state. Receipt: source instance/run/attempt/checkpoint hash, destination/version, verified list/bytes/hashes, trusted-load env/result, UTC/verifier. Missing/mismatch/load failure→TRAINED_UNARCHIVED; keep prior verified snapshot and retry transfer, not training. E005 rejects a deliberately corrupted **second disposable copy**, never the sole artifact.
6. **Resume/export:** select latest verified recovery snapshot by manifest, verify inputs/env/parent, new approximate-lineage attempt; inference best is not recovery. Selected exact weights→same-head reference→ONNX/ORT→LinQ again; preserve unsimplified graph/sidecars. Archive PASS is not exact continuation, future host SLA, model quality, or device proof.
7. **End lifecycle independently:** after receipts for all unique outputs and authorized decision, exact-ID stop/destroy, actual-state polling, volumes and Charges reconciliation. Never trust combined copy-and-destroy exit0.

F121/F125–F134/F153–F165/F198. No runbook/controller/guard/registry implemented, no interruption test done. RPO/RTO and cadence require actual serialize/upload/verify/load durations and acceptable work loss, not universal “every N minutes.” Same disappearing host is not external backup.

**PROP lightweight structure:** one writer assigns immutable `run.json` per run/attempt and append-only `events.jsonl`, artifacts directories; stable team-side registry, worker only own outputs. Retain:

- source/submodules/patch bytes+hash; model/config/head/EMA-or-raw; exact init URL/revision/actual hash/license/card/notices/modifications;
- Dockerfile/actual image digest/full transitive hash lock/Python/OS/core/exporter/simplifier/CUDA/driver/hardware/offer/contract;
- exact media/images/labels/hashes/rights/ontology/ignore/reviewer, parent groups/splits/derivatives, source time/eligible exposure;
- full command, seeds, Btrain/Bval/nbs/actual accumulation/AMP/optimizer/LR/schedule/warmup/augmentation phases/validation/stop/selection, requested versus effective and mutations;
- actual consumed batches/images/groups/update attempts/calls/applied-or-null, curves/warnings/resources/durations, raw object/track/relation/event/alert outputs, counts/slices/uncertainty;
- pre-strip native recovery state/lineage, separate inference artifact, receipts/final seal/observability gaps;
- golden inputs/reference/graphs/IR/all domain-opsets/operators/decoder/preprocess, compiled/converted hashes/placement/state/parity/latency/final bundle;
- quote/raw UTC/rates/units/state timeline/volumes/transfers/all Charges pages/authorized limits; account raw private.

Monitor phase-aware heartbeat/UTC/monotonic duration for train/validation/save/transfer/export, GPU memory/utilization/temp/power, RAM/shm, free disk/inodes, loader/decode waits, loss/grad/AMP overflow/mutations, archive backlog/age of latest verified external snapshot. Long validation is not automatically deadlock; CPU-bound GPU idle prompts loader/augmentation audit, not GPU2. Smoke-derived phase timeouts, no universal minutes. F015/F122/F127/F131/F139/F142; [nvidia-smi](https://docs.nvidia.com/deploy/nvidia-smi/index.html).

## linq-handoff

**DOC boundary F013/F189–F195; S273–S275:** public [manual](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), 2025 **`RU.РМДВ.04.06.014-03 34 01`**, works through **ResNet50 classification** ONNX→TF→quantized representation→compile→runtime. **`yolo5s` p22 is only a tested-name**, not checkpoint/export/decoder identity. Undated [tech page](https://lin-q.ru/tech) lists yolo5s/yolo8/yolo11,resnet/mobilenet as family claims, not exact compatibility matrix or YOLO26 support. **Exact detection fallback is unknown.** Start with actually issued known-good vendor sample+weights/config/fixture/expected output. Manual-only ResNet50 is a better grounded infrastructure diagnostic than arbitrary YOLOv5s, not safety capability.

**Access limit:** W2 obtained full extracted manual text but **no PDF bytes/SHA/page PNG/visual verification** due TLS/access. Suspicious tensor names, filename differences and abbreviated conversion API are not verified copy-paste instructions. Historical Ubuntu20.04/Python3.11/RAM32GB/i7-7700 and sample Python3.8 log are not2026 inventory. Generic `tpu_framework-py3-none-any.whl` without release/hash does not identify issued SDK. TLM estimate is not wall latency; DEFAULT/STAGING/tensor cache do not prove multi-model residency/concurrency. Official case visual reading and manual extraction have different provenance. [W2-F boundary](_WORK/W2_F.md); F191/F192.

**Policy UNK Q007:** case requires neural inference on LinQ, but no literal ban on every neural CPU op was found. Team CPU+TPU statement does not authorize arbitrary fallback. Proposed host stages: decode/geometry/NMS/unlearned association/FSM. Detector/pose/ReID/V/T/learned router/fusion each need policy+actual per-node placement proof. State stored in host RAM is not necessarily neural execution on host. `.tpu` file, framework import, ORT success or low CPU utilization do not prove placement. F001/F013/F193/F194.

### Four acceptance gates, all UNRUN

1. **Same-head reference:** exact selected weights/state/head/preprocess/decoder and trusted load; raw golden tensors/outputs/classes/geometry/source/config/hash. Dense PyTorch is not reference for another e2e/deploy head.
2. **Floating ONNX:** static names/shapes/dtypes/IR/all `domain::opset`, checker **and numeric ORT** on same prepared tensors; unsimplified graph+sidecars/exporter/patch/lock/op attrs and tensor/box/score/rank/threshold flips. Checker PASS≠parity; ORT PASS≠TPU.
3. **Target representation/compile:** rename/layout/shape/precision/scales, exact ops attrs/dtypes, converter/compiler diagnostics/partitions; converted/compiled hashes and placement map. Compile PASS≠runtime quality.
4. **Issued LinQ end-to-end:** actual completion/raw outputs/backend, decoder/state/reset/isolation/memory/residency/load/bursts, full causal notification delivery, fixed DEV replay and frozen LOCKBOX only if available. Serial sample PASS≠multistream/cascade proof.

F145–F152/F193/F194. Predeclare tensor/event drift and quality/latency budgets; no universal tolerance assigned. Final checkpoint/blocking change repeats affected gates. First feed **identical already-prepared ndarray** to runtimes, then compare preprocessing separately on identical decoded pixels. Annotated JPEG cannot reconstruct crop geometry/routing. D-FINE `orig_target_sizes` must explicitly name coordinate system; adapter640² does not imply original H/W.

### Exact handoff package

**PROP F148/F193:** incomplete field = `unknown + owner + gate`, never architecture-name substitution.

| Block | Required retained fields |
|---|---|
| Target identity | OS/arch/kernel/CPU/RAM, actual LinQ SKU/count/board memory/firmware/driver; compiler/converter/runtime versions+hashes; local/remote API/quotas/policy; issued sample source/weights/fixture/expected output. |
| Per neural node | Role/node ID/source/config/checkpoint/actual hash/license/EMA-or-raw/task/classes, requested+actual head/fusion; exported graph/external-data list/exporter/effective flags/patch/lock. |
| Inputs | Count/names/dtypes/layout/shapes/batch/time/aux semantics/ranges; decode/color/resize/kernel/rounding/pad/crop/normalize versions; source→crop→model and inverse geometry; golden ndarrays+hashes. |
| Outputs | Names/rename/dtypes/axes/logits/probabilities/objectness/box encoding/units/frame; valid count/padding/background/null/class order/remap; top-k/NMS/threshold inclusivity/ties. Prevent double sigmoid/grid decode/NMS. |
| Representation | ONNX IR/all domain-opsets/op inventory with attrs/shapes/dtypes; ONNX→TF name/layout map, precision/scales/rescale owner/data provenance; converted/compiled hashes/partitions/host fallback. |
| Runtime DAG | D/V/T/pose/ReID/flow/router/fusion, call triggers/fan-out/streams/crop loads, serial/concurrent and resident/load-on-demand policy, copies/queues/drop/backpressure/timeouts/deadlines. |
| Time/state | Past-only frames/PTS, warmup/masks/padding; state shape/owner/lifetime, camera/stream_epoch/track/generation key; TTL/reset on seek/reconnect/gap/ID reuse/schema/model change; explicit `state=none` for stateless node. |
| Evidence | DEV fixtures/split provenance/raw reference/float/converted/device outputs, predeclared budgets, counts/slices/parity report, actual source/available/decision/emit/receive traces. |

**PROP probes F194:** known-good serial sample→our exact D; state isolation A-alone/B-alone/interleaved/scene cut/seek/reconnect/out-of-order/gap/expiry/reuse/restart. Warmup is unavailable, not safe negative. If V retained, D alone/V alone/**D→V→D** with load/unload/reload parity and actual memory; concurrency/residency only within documented limits. Replay real arrival/correlated crop bursts, backlog slope/drops/timeouts/fairness/frame age/completion tails. Serial resource sanity `U≈Σλ_X c_X<1` is necessary, not tail-deadline guarantee. Q020/Q021.

**Kill/localize:** vendor sample failure first localizes SDK/env/service, not whole YOLO family. If sample passes and graph fails, preserve offending node/attrs/shapes/dtypes/compiler diagnostic; tiny operator fixture diagnoses, never replaces whole-graph acceptance. Conditional e2e→dense is new bundle only with actual dense weights. Remove optional V/pose/ReID if their gate fails; retain acceptable D+CPU rules if semantics permit. Mandatory node unresolved policy/placement/parity, wrong decoder/classes/geometry, unsupported ops, state contamination or unbounded queue means no final PASS. Numerical parity with growing queue requires scope/load/router change and renewed evaluation. Without actual neural LinQ path **and measured speed**, case's mandatory requirement remains unmet despite CUDA demo. F151/F181/F194; Q006/Q007/Q018–Q021.

## open-gates

**UNK, not automatic technical FAIL.** Records follow `open_gate` schema; R1–R5 are proposed slots. New public pages cannot replace private media, actual artifacts/account/SDK, experiment execution, or scenario-owner decisions. Full reasons/locators/closure are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

| id | unknown_and_decision | proposed_owner_and_closure |
|---|---|---|
|Q001|One observable scope/frontend actually usable?|R5+R1/R2; accepted lying-state or authorized team-video zone, explicit boundaries/actors/unknown/deadline; otherwise synthetic logic.|
|Q002|Exact assets/use/redistribution/host-transfer rights?|R1+data owner; received source/hash/license/notices/use/region manifest; URFD NC not assumed accepted.|
|Q003|Actual decode/PTS/CSV mapping/durations/EOF?|R1/R2; decoded frame/time map and human onset/observable/end/censor labels.|
|Q004|Exhaustive TRAIN and independent groups?|R1/reviewerR2; lineage/near-duplicate audit, reviewed classes/ignore/splits; current pair DEV only.|
|Q005|Scenario deadline/FP/recall/coverage/delivery budgets?|R2/R5; predeclared floors/matcher/unknown/censor/response; fixture constants are not production targets.|
|Q006|Issued SDK/SKU/service/access/known-good sample?|R4; actual versions/hashes/inventory/quotas/sample+expected output and serial run; public manual not server identity.|
|Q007|Allowed neural CPU fallback and actual placement?|R4/R5; policy provenance plus per-node partition/backend trace; host state storage separate.|
|Q008|Accepted exact weights/use and installable chosen stack?|R3/R5; actual hashes/trusted load/head log, full resolved hash lock/pipcheck/import/explicit adapters.|
|Q009|Representative actual3090 train+val fit and work time?|R3; separately authorized first paid qualification, worst relevant paths/peaks/B/AMP/save/reload/no hidden recovery.|
|Q010|Named error justifying C/pose/V/temporal?|R2/R3; DEV error atlas and one controlled mechanism test/meaningful-gain constraints; no error→defer.|
|Q011|Fail/fork guard and honest progress observer executable?|R3; E005 disposable negative drill/append events/final seal; applied count null until validated.|
|Q012|External native pre-strip recovery loadable/RPO/RTO?|R3+independentR2 verifier; list/bytes/hash/trusted-load/lineage receipt, corrupted second-copy rejection; approximate continuation declared.|
|Q013|Spending authority/account owner/limits/lifecycle scope?|R3+financial owner/R5; separate explicit authorization and owner account/payment/autobilling terms; research authorizes none.|
|Q014|Refreshed offer/rates/units/stopped price available?|R3+owner; same-query UTC/full raw/host/contract/resource fields immediately before purchase.|
|Q015|Loading/offline/expiry/volumes/transfer actual charges?|R3+owner; actual state timeline/all paginated Charges/rates/units/later correction; no induced outage for billing research.|
|Q016|Control host/rsync/SSH/trusted archive transport ready?|R3; actual verified CLI/runtime/host keys/destination fixture and external receipt; no credentials in chat/image.|
|Q017|Exact optional fallback/backbone/pose/V rights and need?|R5/license owner/R3; accepted use/notices/init chain/bytes/load only if retained; timm conflict and YOLOX/B2 scope unresolved.|
|Q018|Actual exported head/IR/opsets/ops supported?|R3/R4; same-head floating graph inventory→compiler diagnostics/placement/raw target outputs; no architecture-name pass.|
|Q019|Converted bundle preserves quality and full deadline?|R4/R2; same-tensor reference/float/converted/device diffs + DEV events + actual full delivery; not LOCKBOX export debugging.|
|Q020|Residency/switch/concurrency/burst limits?|R4/R5; serial D/V/D and real bursts/queues/memory/tails; P0 for claimed cascade/stream load, P1 for single serialD.|
|Q021|Causal state/reset/isolation/freshness correct?|R2/R4; E001/E002/E003 traces across stream/actor/generation/gap/seek/reuse/restart, warmup unknown.|
|Q022|Enough independent quality evidence and useful GPU2?|R2/R3/R5; completed acceptable incumbent/independent groups/exposure/ready jobs/measured mandatory reserve; otherwise feasibility.|
|Q023|Actual people/reviewers/cutoff/submission owner assigned?|R5; names/availability/backup, reserve/freeze ledger, final inventory/upload acceptance by deadline.|
|Q024|Neighbor handoff accepted with actual inputs?|R2/R4/R5; concrete geometry/device/behavioral packages as specified below, not externally sent messages.|

**Gate order:** before rental Q001–Q003/Q006–Q008/Q013–Q016 document/data/local mechanics; Q009 only after separately authorized first qualification, never a pre-rental circular demand. Before heavy B additionally Q004/Q008–Q012 and actual target path. Before final LinQ bundle Q005–Q007/Q018–Q021. Insufficient gates→explicit feasibility/scope reduction. K006/K011 are already resolved integration choices, not unowned research tasks. F003/F004/F017/F018.

## handoffs

**PROP prepared transfers, no external messages sent/new neighbor research launched.**

- **Camera geometry/calibration:** original/final-input pixel sizes, camera/zone/rule versions, foot/body/bbox anchor, pose validity/visibility, source→crop→model/inverse transforms, boundary/occlusion/ownership errors. Decide when polygon/2D anchor suffices versus metric calibration; projected overlap is not physical contact.
- **LinQ quantization/deployment accuracy → linq_platform/model_stack:** retained exact source/weights/head/env/graph, all IR/domain-opsets/operators/attrs/shapes/dtypes, same-head golden inputs/raw PyTorch/ONNX outputs/decoder geometry, runtime DAG/state/load/crop/placement unknowns. Determine actual converter/compiler/precision/PTQ/QAT/data provenance and tensor/event drift budgets with real device evidence.
- **Behavioral models + video datasets → datasets/violation_methods:** lying≠fall≠unconsciousness; URFD rights/timing/asset gaps and CAUCAFall motion-trigger limitation; absent continuous negatives/onset/observable/end/actor/causal labels and residual CPU-FSM failures. Need untrimmed target clips, contrast actions and reproducible causal checkpoint, not architecture names.
- **evaluation/training_strategy/datasets:** shared TRAIN/DEV/LOCKBOX, matcher/coverage/uncertainty, partial-label QA/error atlas, native recovery mutations, E001–E012 as conditional library. **video_architecture/operator_product/hackathon_strategy:** source age/queue/drop/reset, event UUID/rearm/second actor, actual target load/policy, confirmed file/server flow, evidence/journal/full delivery endpoint, cutoff/material inventory. F018/F047/F063/F099/F152/F195; Q024.

**Five decisions before rental:** select observable scope+accepted media/use; identify real TRAIN/DEV/LOCKBOX/labels/time/exposure; accept objective/matcher and bounded one-incumbent queue; accept exact weights/head/export route and identify issued target/sample; set owner money/time/resource/lifecycle limit and trusted external archive. Actual3090 fit follows separately authorized qualification. F003/F017/F115/F181/F200.

**Stop expansion for these red flags:** correlated frames/crops/phases called independent test; demo reused as lockbox; old pass transferred to refit; curated clips called factory FP/hour; missing annotations used as negatives; larger detector chosen before visibility/pixel audit; lying renamed unconsciousness; phone renamed use; cooldown hides second actor; several factors changed under one “ablation”; OOM/NaN/save repair hidden by finite weights/exit0; model file without actual hash/load/decoder/target trace;2×24GB called48GB pool/×2 speed; copy exit0 followed by destroy without receipt; loading declared fully free/storage counted twice/compute multiplied twice; extra graph without placement/load/state/burst gate; optional work consumes frozen LinQ/submission reserve. Fix the cause, preserve incumbent and new artifact identity where affected. F020/F069/F078/F084/F109/F134/F151/F159/F164/F170/F181/F195/F200.
