# Eight-scenario model requests and LinQ gates

This is a request for Training/Data intake, not implemented scenario coverage, a resource allocation, an external event schema or a decision to deploy a model. The machine-readable authority for this handoff is [TRAINING_REQUIREMENTS.json](../ml/scenarios/TRAINING_REQUIREMENTS.json). Root forwards it through the agreed shared handoff; this task does not contact another account or change a producer worktree.

The official page-4 image was inspected. Its eight examples are preserved: running/abrupt movement, proximity to moving machinery/transport, phone use in equipment/moving context, smoking/open flame outside designated places, climbing/passing under conveyor/load, height without harness, falling/floor lying/immobility, and cargo handling violating a rule. Page 4 explicitly calls cargo an additional scenario; that does not make it disappear from the mapping. Helmet is supplementary and does not replace one of the eight. Loss of consciousness cannot be diagnosed from RGB footage.

## Verified intake and its limits

The current producer READY pointer and all five immutable release file registries were verified using the existing read-only handoff verifier: exact approved use, manifest digest, every pinned file byte count/SHA256, class map, splits and checksum registry. No raw media was decoded, no source was discovered and no inference ran.

| READY release | Permitted scope relevant here | Cannot silently become |
|---|---|---|
| SHEL5K source-box diagnostic19 | Private noncommercial parser/geometry/source-label QA | Training, wearer negatives, independent event evaluation |
| Mendeley factory replay16 | Existing development/calibration/replay and annotation preparation | Independent validation/test or action labels inferred from folder categories |
| EDF native fall source3 | Source-positive fall-process window development, other times UNKNOWN | Negative complement, floor-lying/immobility GT or complete event precision |
| CAVIAR running/walking source3 | Explicit source actor walking/running windows and permitted local training/prototyping, unboxed/unknown masks retained | Industrial running/abrupt-motion quality, approved danger-zone policy or final test |
| PPED object-presence48 EXIF diagnostic | Canonical-frame object/parser/scale QA and review queue | Detector training, wearer ownership/absence, action or event evaluation |

PPED has literal Coverall, Face_Shield, Gas_Mask, Gloves, Goggles and Mask regions. It has no harness, Helmet/BareHead, wearer-state or fit/attachment annotations. Non-detection, unlabeled areas and nearby PPE do not establish a worker's lack of protection. No new training is allowed merely because a release says READY.

The Training handoff `/workspace/artifacts/training/matvey_training_20261024/matvey_training_handoff.json` was inspected only after its seven allowlisted descriptor files passed byte/SHA checks. Its four ONNX and four checkpoint descriptor hashes were also checked without loading/deserializing weights or reading the Training worktree. It records **no new training and no production model selection**.

GMD currently supplies four subject-fold-specific heads: TCN, MLP, TCN, MLP. Each takes `pose_window float32 [1,24,74]` and returns `fall_logit float32 [1,1]`. Float ONNX parity on cached development features passed; no decisions changed at the frozen .5 point. That is export-only acceptance. The imported weak-clip source CV (160 clips, four outer groups, macroF1 about .800) is not worker-linked incident accuracy, industrial evaluation, floor immobility or medical evidence. No compiler, vendor PTQ, actual runtime ABI or LinQ execution gate passed for these heads.

The cached feature recipe uses the highest-score proposal with unverified source-actor binding and native FP32 pose features. A production handoff still needs the exact 74-channel order, units/masks, timestamps/cadence, normalization and window-to-bag/episode aggregation. An all-invalid or actor-unbound window must be UNKNOWN and make zero temporal-head neural calls. Do not automatically choose the best outer-fold head, retrain on held-out groups or replace the rule baseline with this export.

## Exact scenario requests

Each JSON scenario specifies literal object classes, separate actor actions/states, actor-object ownership, original-frame/PTS annotation requirements, hard-negative families and requested pilot video support. The common annotation request explicitly distinguishes complete, partial and unknown class coverage, ignore areas, visibility, gaps and censoring.

| ID | Baseline candidate requested; not selected | Essential missing evidence / semantic boundary |
|---|---|---|
| S01 Running / abrupt movement | Retained static640 Split-Pose plus masked actor-window TCN/MLP only after feature/actor contract approval | Walk/run/turn and abrupt-motion intervals, stable actor IDs, camera motion and dangerous-area policy. Image-plane motion is not m/s; CAVIAR does not supply industrial danger semantics. |
| S02 Proximity | Static640 YOLOv8n-style person/forklift/vehicle/machinery detector plus paired motion/scene rule | Equipment instance/moving state, actor-machine pair GT, near AND safe support. Perspective overlap is not physical proximity; metric distances require calibrated geometry. |
| S03 Phone | Static640 person/phone detector plus owner-linked hand/head evidence; optional masked actor-use head | Phone use versus presence, tool/radio negatives, actor operation/movement context and temporal labels. Hidden/small device is UNKNOWN. |
| S04 Smoking / flame | Static640 person/cigarette/flame detector; separately labelled temporal smoking and flame branches | Cigarette ownership/gesture and flame visibility, permitted-place policy, steam/dust/welding/glare negatives. Smoke alone is not smoking; fire presence does not reveal hazardous contents. |
| S05 Barrier / conveyor / load | Static640 person/barrier/conveyor/suspended-load detector plus scene geometry and optional actor-action head | Reviewed over/under crossing direction and interval, suspension/equipment state, approved forbidden geometry. Generic polygon entry does not establish climbing or passing beneath machinery. |
| S06 Height / harness | Static640 person/harness/lanyard detector plus reviewed visible wearer-state ROI classifier | Independently established height-risk policy and observable harness state, ownership and exhaustive absence review. Detector non-detection is not absence; nearby harness is not worn/attached harness. |
| S07 Fall / lying / immobility | Retained Split-Pose rule baseline; GMD fixed-window heads remain export-only candidates | Actor-linked transitions and already-lying states, floor/bed distinction, continuous >=3s lying segments with context, keypoint observability and movement/unknown masks. GMD weak clip category cannot replace incident GT. |
| S08 Cargo | Static640 person/load detector plus carrying ownership/temporal action and explicit rule | Safe/violating episodes under the SAME policy; shared loads and trolley negatives. Mass requires measured metadata; load size/posture alone is not a violation. |

For new object detectors, the requested starting family is a small static batch-one RGB640 YOLOv8n detector because the existing family has an exercised LinQ preparation path. No new initialization checkpoint or source rights are assumed: Training must supply a reviewed checkpoint/hash/class map. Class-dependent head changes still need full export/compile validation. A verified `split_detect_v8` extraction may expose already-decoded boxes `[1,4,8400]` and class scores `[1,nc,8400]`; actual tensor names and shapes must come from the exported graph, never a guessed mapping. Host code performs layout restoration/NMS only, with no repeated sigmoid or neural decode.

Phone use, smoking, climbing and cargo action are not solved by object presence. Their optional temporal request proposes a fixed 24-step actor window, but `F`, feature order, cadence and masks must be explicitly frozen before export; there must be no dynamic feature width at deployment. Multi-label actor-state logits remain distinct from a policy violation. Harness wearer-state classification requires positive observability; it cannot create valid absence labels from detector misses.

## Minimum footage and measurable quality

The per-scenario pilot intake floor requests six continuous original clips from at least three independent site/camera components, ten reviewed positive episodes, ten hard-negative episodes and ten minutes of continuous negative exposure. This is an engineering request for annotation/protocol planning, **not a statistically sufficient training set, an official accuracy target or automatic permission to train**. Each named positive subtype and hard-negative family must be represented; report unmet support as BLOCKED. The fall request additionally requires >=3s observable lying segments and five-second pre/post context; other scenarios request at least three seconds of context. Original-source grouping precedes frame selection and train/calibration/validation/sealed-test assignment.

Report object per-class TP/FP/FN/P/R/F1 and AP on complete labels, with partial-known-positive recall separately; actor-state and episode P/R/F1 require actor-linked reviewed positives AND verified negative support. Always publish counts, unknown/abstention coverage, source groups, object input sizes and uncertainty. Missing suitable GT yields NOT_MEASURABLE/null, not an invented zero or percentage. False alerts per hour requires reviewed continuous negative exposure. Existing .25/.5 confidence and posture thresholds are operating parameters, not validated quality gates. Root must freeze paired candidate/baseline comparison and safety-regression criteria before a run; this document sets no invented absolute accuracy target.

## Export, PTQ, runtime and checkpoint handoff

Training must deliver a hashed best/last/resumable checkpoint bundle, initialization identity/rights, code/dependency versions, seed/optimizer/schedule/epochs/precision, source-group/split manifests, annotation hashes, training curves, validation support and frozen selection rationale. Include the ordered class/feature map, normalization/inverse geometry, output semantics, NMS and temporal masks/state/reset/aggregation policy. Do not deserialize an untrusted checkpoint merely to inspect it; hash checks establish identity, not accuracy or approval.

Verify native FP -> ONNX -> conditioned graph -> vendor quantized reference -> actual named runtime ABI on identical inputs. Calibration is train/calibration only; save exact tensors/groups, thresholds/scales, graph/compiler versions and full program SHA. Each newly trained detector/action head needs its own actual LinQ qualification; a local ONNX or cached-feature parity pass is insufficient. The pose extractor plus learned temporal head chain must both meet the neural-placement requirement. No new model/family is declared compatible merely because another YOLO compiled.

Historical Helmet/Split-Pose hardware completion remains historical PASS for those hashes. **NEW Matvey remote placement is still blocked/unexecuted for this intake.** New deployment uses only reviewed own `matvey_*.tpu` files under `/auto/cache/<runtimeLogin>/matvey/`, owned queues and central admission, controlled by root. Nothing here authorizes protected files, legacy locations, credential access, network/VPN/SSH changes, staging, compilation or inference.

GPU resources belong to the separate Training Agent. This task performed metadata/hash verification and authored two request documents only. Data/Training READY scope, model acceptance, root resource allocation and runtime placement remain separate gates. Engine, common contracts and producer worktrees are unchanged.
