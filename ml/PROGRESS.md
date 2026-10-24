# ML/CV quality sprint — progress

## Night checkpoint 2026-10-24T01:12:56.048453+00:00

MEASURED / SIMULATED: E001–E005 finished, all three directions used their two NEW hypothesis budgets. No training, no new LinQ calls, no network/service changes. Root integrated Detection b26aaf74 and Behavior 0082c8de in isolated branches. Numeric summaries: ml/reports/night-20261024.json; graph-ready CSV and decision table beside it. Source artifacts remain immutable outside Git. Code checkpoint before this record: d9d616899992818d7d9bd5eafe99b338747ff2c3.

| Experiment | Before / hypothesis | After / evidence | Decision |
|---|---|---|---|
| E001 control | Native Helmet vs original float ONNX, same52reviewed images | MEASURED same class counts/AP/P/R/F1; macroF1 .716422. Vendor baseline SIMULATED macroF1 .741682 but bare recall .71875→.59375 | Quantization-chain class regression observed; conditioning vs PTQ not causally isolated |
| E001 | Diverse8calibration, same weights/export | SIMULATED macroF1 .741682→.735185, bare recall unchanged .59375 | REJECT; TPU ecd5a885... retained locally, never deployed |
| E005 | FinalConcat split, same data8control | Float52raw BITWISE parity. SIMULATED macroF1 .327778, bare recall .03125 | REJECT; baseline output scales already perchannel, no invented global-scale explanation |
| E002 | EDF original320x240 vs half then restored, same2584frames each | MEASURED torso/frame .641254→.553793; unknown/missing .541796→.597523; positive support1/24→0/24; confirmation0/24both | Keep original RGB; support is not incident recall; P/F1/falsealerts/hour NOT_MEASURABLE |
| E004 | Allow one side torso pair, replay sameUR20 observations | MEASURED same2FPS TP1FP0FN9/F1 .181818; all3274 TP0FP0FN10both | REJECT, optionalflag OFF; unknown reduction alone is no event improvement |
| E003 H1/H2 | CAVIAR bodyheight speed / observedbbox anchor | MEASURED baseline=H1=H2 TP0FP0FN3/F1=0;0/46running actorframes associated,11/528knownactorframes associated | Both REJECT; no ROI third hypothesis; Running/Zone remains experimental |

OBSERVED data handoff: four immutable producer READY releases now available; EDF and CAVIAR consumed under exact approved research-development use and hashes. Neither is an independent industrial test; EDF complement UNKNOWN, CAVIAR uses sourceFrame*40ms nominaltime, not originalPTS. No source search/download duplicated; Data worktree untouched. Finetune BLOCKED: no approved complete clean train/heldout release. Expansion BLOCKED: no actor/geometry/policy GT for machinery, barriers, phone, flame, height or loads. Do not invent extra recognizers from clip labels.

OBSERVED shared infrastructure safety: own namespaces and cross-journal active-request fence integrated. Stage/bootstrap now fail closed outside runtime-account matvey/; no stock-file permissions lookup. Prepare-only is default. Durable ambiguous publication and request state prevent blind repeats; these are software/fault-test evidence, not a new shared-service outage test. Historical old-path completed captures remain evidence; new Matvey staging has NOT been performed. No captain baseline touched.


## ACTIVE NIGHT CYCLE — 2026-10-24T00:31:35.783154+00:00

New autonomous cycle authorized for at most6–7hours; do not fill time artificially. No intermediate user questions. Current integration baseline1bdeeafc; working branchmatvey_cv. Historical335tests are the last completed full suite, not an automatic new PASS. Existing runtime/model checkpoints remain immutable; previous rejected hypotheses are not rerun.

OBSERVED E000: exact checkpoint topology establishes Helmet YOLOv8n DetectionModel(3,011,238unfusedparameters,storedUltralytics8.0.23) and Pose YOLOv8n PoseModel(3,295,470parameters,stored8.0.77). Split-Pose shares the same trained weights; exporter8.4.184 is a different version. Full inventory in MODEL_INVENTORY.md; unknown history/runtime versions stay UNKNOWN.

OBSERVED E000 handoff: producer release tools were changing, so ad-hoc external ingestion was blocked. Data Orchestrator then published immutable READY versions SHEL5Kdiagnostic19 and Mendeleyreplay16;65pinnedfiles/hash records verified READ_ONLY, roles not promoted. Native UR/RUN actorGT remains requested through /workspace/shared/dataset-handoff/ML_REQUIREMENTS.json. Existing ML-owned52val/8calib/20URpreview snapshot READY at ml-baseline-night-v1/READY.json, fileSHA5f30081065e69e9316e96b972353267caaae868212194b312ddc8ceae065f74b.

OBSERVED integrity correction: historical Helmet dataset_digest39e13... is canonical semantic SHA, not serialized file SHA346f74... . Source GT/predictions and metrics are unchanged; current docs/manifest fields are being clarified. Eight handoff guard tests cover mutation, scope, split leakage, sealed test and producer metadata.

Shared infrastructure constraints are active: no network/VPN/SSH/firewall/service changes, no captain/baseline/foreign queue operations. New own remote artifacts matvey/ and matvey_ names only, max1ownactiveTPUrequest. Until isolated staging and all client entrypoints are verified, no new remote model task is allowed. CPU/model preparation and ready-data evaluation continue independently.


Authority: current user directive, /workspace/ML_24H_PLAYBOOK.md and official case (20 pages visually read; PDF contains scanned slides). Application/backend/frontend work is frozen. Existing contracts and video pipeline are retained.

Current checkpoint: Helmet and Fall are FROZEN runtime baselines after two failed hypothesis families each, improvement=false. Fall quality is NOT_ACCEPTED; independent test is absent. Running/Zone prototype+scorer are BASELINE/NOT_EVALUATED pending real GT.335 tests PASS. All specialized agents completed; no heavy ML process is running. Non-force push failed AUTHENTICATION_UNAVAILABLE/exit128; local commits saved, remote not verified. Model-only local archive is ready; external destination/account pending. The allocation/status paragraphs below are a historical log, superseded by this current checkpoint.

| UTC / MSK | Experiment | Problem / hypothesis | Action and evidence | Decision |
|---|---|---|---|---|
| 2026-10-23 22:57 / 2026-10-24 01:57 | E00-intake | Working hardware is not measured detection quality | Baseline code13d25593, existing Helmet/Split-Pose checkpoints and actual captures inventoried; Running/Zone production implementation absent | Freeze baseline; do not invent accuracy |
| 2026-10-23 / 2026-10-24 | D00 | Adjacent/duplicate images can leak across source splits | Detection agent audited1416 Construction-PPE pairs;1268 connected components,30 cross-split components,10 orphan labels | Source test-touching components excluded from32-image val; preserve all original data |

| 2026-10-23 23:05–23:16 / 2026-10-24 02:05–02:16 | E00/E01 Helmet | Thin source head boxes and incomplete labels distort quality | Blind AI repair, second AI review of4 new+4 old images; fixed52-image quality-v3,44 complete/class; original32 report retained | Recompute baseline and all candidates on identical corrected GT; annotation repair is not model improvement |
| 2026-10-23 23:16 / 2026-10-24 02:16 | E02 Helmet | Higher confidence might reduce FP without losing recall | .25/.4/.5 macroF1 .71642/.65248/.52273; raised thresholds lose both class recalls | Hypothesis REJECTED (1 failed); retain checkpoint and .25 |
| 2026-10-23 23:10–23:18 / 2026-10-24 02:10–02:18 | E00 temporal | Source labels/MP4 may not match our incident semantics |20 source clips,3274 original-PTS RGB frames,59 unknown frames; bed-lying hard negative, short fall tails. Native runner completed49.70s, no TPU fallback | Incident scoring awaits frozen review policy; native timing is not LinQ throughput |
| 2026-10-23 / 2026-10-24 | Q00 LinQ numeric audit | Industrial confidence drift despite successful TPU execution | Saved hardware class/KP tensors bitwise match vendor quantized simulation; FP-to-conditioned+PTQ confidence loss measured on3 industrial inputs | Do not blame AMQP codec or assert current global keypoint collapse; conditioning/PTQ causal isolation incomplete |
| 2026-10-23 / 2026-10-24 | E03 PTQ | Diverse industrial calibration may reduce current quantization drift |8 fixed Mendeley midpoint frames,1 conservative source group; CPU2 unchanged split-pose ONNX/O1 compile allocated | Candidate NOT_PROMOTED; validation and actual LinQ gate pending |
| 2026-10-23 / 2026-10-24 | Scope steering | Separate Data Orchestrator owns dataset work | New searches/downloads stopped; existing intake and sealed selection handed off in DATA_HANDOFF.md; official8-scenario matrix in SCENARIOS.md | ML owns models/scoring/LinQ only; move beyond Helmet/Fall after at most2 failed hypotheses |

Live ownership: Detection /workspace/agents/detection (completed Helmet E01/E02/handoff, no GPU); Behavior /workspace/agents/fall (offline temporal scorer, then Running/Zone prototype); LinQ /workspace/agents/linq (CPU2 isolated PTQ compile). Root owns the eight sprint registers, native evaluation and evaluation decisions. Root native GPU job completed and released the shared lock. No independent final test has been evaluated. Dataset intake after the steering belongs to the separate Data Orchestrator; its worktree is untouched.

Completed since that allocation: H-HELMET-02 fixed tiling was rejected (macroF1 .716422 -> .606575, helmet recall .76 -> .72); two Helmet hypothesis families exhausted, stage FROZEN with original checkpoint/full-frame .25/NMS.45 and independent-test gate still open. H-FALL-02 upright-history retention gave no gain at either matched cadence and remains OFF. Native full-cadence fall TP0/FP0/FN10; paired2FPS native TP1/FP0/FN9. Cadence sensitivity is disclosed, not treated as an improvement. Temporal metric v1.1 corrects all-missed F1 to0 while leaving precision undefined.

New hardware check completed:11 real Split-Pose requests on URfall01, all matching UUID/status0/numeric hashes. No event,1miss. Initial processing131.018s/.083958FPS; RPCp50=10.630s/p95=18.967s. Finalizing EOF made0newrequests. Hardware PASS is not detector quality PASS. Running/Zone offline prototype merged8241e428, production recognition remains unvalidated.311 software tests passed before reusable SDK reference backend1924a14b; repeat after all merges. H-FALL-01 paired225-frame CPU2 simulation is the only active model experiment; no heavy GPU job is allocated.

Official dates: checkpoint24October18:00MSK; target stable ML freeze24October20:00–22:00MSK; submission25October10:00MSK. Speed is measured separately; few-second response remains an official requirement, not already satisfied.

PTQ closure: H-FALL-01 baseline/candidate BOTH TP1 FP0 FN9, P1.0 (one alert), R.10, F1.1818 on225 identical2FPS frames/20clips under v1.1. Valid CPU2 runs472.386s/464.813s. REJECTED_NO_EVENT_QUALITY_GAIN; second failed Fall family reached. Both own-model configurations are FROZEN as runtime checkpoints, improvement=false; Fall is NOT an accepted accurate recognizer. No candidate upload/LinQ or third tweak. Hardware baseline parity remains separate from accuracy.

The invalid32-call CFR decoder attempt is retained and never scored. Four client-env Torch fixture errors were fixed only in tests;319passed afterward. Data work remains with Data Orchestrator. All heavy ML resources are IDLE; final task is the already-started Running/Zone evaluator and its checks. Local84.2MB/24-member model archive is verified but off-Vast destination/account is pending; external backup is not claimed.

Final code merges: e42d6186 offline motion scorer and explicit synthetic fixtures,059f4055 completed PTQ results, f5796657 dependency-free graph fixture tests. Root actual missing-GT check: NOT_EVALUATED/null metrics.335 software tests passed after all code merges. No app/backend/frontend or Data Orchestrator files changed. Native agents completed and all heavy resources are idle. Next model/data-backed experiments depend on Running/Zone actor/episode/geometry GT; then equipment proximity and phone as suitable annotated data becomes available. No further Helmet/Fall tuning is allocated.

Git preservation: attempted ordinary push matvey_cv at91473909, exit128/AUTHENTICATION_UNAVAILABLE; no force, no credential output retained. Final metadata records the blocker; no repeated authentication attempts or main changes.
