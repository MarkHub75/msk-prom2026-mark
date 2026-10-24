# Evaluation protocol quality-v1

This protocol is frozen before E00 predictions. Dataset selection/annotation decisions must not use model outputs. Any amendment gets a new data/protocol version and is logged; baseline and candidate are rerun on identical amended validation GT. Final test is not used for tuning, calibration, error-driven sample selection or early stopping.

## Groups and independence

Group original video/camera/scene/actor where known. Exact file and decoded-RGB SHA256 plus connected near-duplicate perceptual clusters are indivisible. A connected component touching final test cannot enter development. Unknown source identities are recorded, never made independent by random filenames. Public pretraining lineage can remain unknown and must be disclosed. The8already inspected Mendeley clips and old bus fixture are development, never independent test.

## Detection endpoint

Canonical classes helmet and bare_head are object/head-region labels; wearer-state/ownership is a separate endpoint. Model baseline inference:640x640RGB letterbox, float32NCHW, scale1/255, fixed original decoder/NMS. Operating confidence0.25, NMS IoU0.45, maxDets300. AP prediction floor0.001 only for score-ranked measurement; it is not a changed operating threshold. Head/helmet/hidden-head units cannot be merged blindly.

Primary P/R/F1 and AP use only images with explicitly reviewed COMPLETE coverage of that class; partial known GT supports separately labelled annotated-instance recall only. Unknown/occluded regions are ignored, not negatives. Matching is class-aware one-to-one greedy descending score at IoU0.5; unmatched positive annotations are FN; an unmatched prediction in a reviewed ignore region (IOA>=0.5) is ignored; remaining unmatched predictions are FP only under complete coverage. Undefined precision/recall/AP remains null with counts/reason.

AP50 and mean AP at IoU0.50:0.05:0.95 use101recall-point interpolation; this custom object evaluator must not be branded exact COCO unless independently checked against it. Separate source-label benchmark numbers from manually reviewed metrics. Stratify small objects, visibility, lighting, class, source and group; report support and group-bootstrap CI when sample size permits.

## Temporal endpoint

Evaluate event P/R/F1 separately for suspected_fall, prolonged_lying and offline Running/Zone experiments; do not change public event schemas. Native author posture transitions do not directly establish incident onsets. GT requires reviewed visible intervals, original PTS/frame alignment, track/source IDs, unknown windows and censoring. No unlabeled interval counts as verified negative. Missing detections/observations are unknown; gaps cannot accumulate evidence. Existing confirm durations and thresholds are the baseline.

Match same scenario/source/group with one prediction per GT episode; onset/overlap tolerance and review coverage must be fixed in a task-specific supplement BEFORE inference. False alerts/hour only over fully reviewed continuous exposure. Running/Zone production baseline is NOT_IMPLEMENTED, not a hidden success from zone_id/floor_polygon. No m/s without calibration. A model-generated annotation is never independent GT.

## Candidate budget and admission

E00 baseline first. E01 blind data/annotation correction with new manifest digest. E02 at most2operating-threshold candidates from{0.4,0.5} against0.25, NMS fixed; select on reviewed validation macroF1 with no class recall drop>0.02 and report uncertainty. E03 one fixed ROI/scale policy if small-object error evidence warrants it; do not tune coordinates on test. E04 at most1short fine-tune of the already exportable architecture, only with sufficient clean training labels and approved rights. No simultaneous GPU jobs.

Freeze selected complete inference bundle (weights, preprocessing, decoder, threshold, temporal rules, version) before E06 sealed test. Run baseline and selected final once on the same untouched independent test; no post-test selection. If improvement or independence is not demonstrated, keep the verified baseline and mark the claim unestablished.

## LinQ and performance

Actual own-model completion with matching UUID/status/tensors is required for release. Candidate must pass ONNX/compile/PTQ/numeric/decoded ABI on5–20development/calibration examples; final test never calibrates. Retain baseline for rollback. Speed/latency, neural-only vs full call, hardware placement and numerical parity are separate from accuracy. Unit-test counts are software evidence only.

## Recorded development amendments

E01 preserves the initial32-image E00 evidence and expands to a fixed52-image development set. Blind corrections preserve original boxes/reasons; GTv3 digest is39e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a. Both confidence candidates and tiling are scored on exactly this GT and the same matching/coverage rules. Label repair and sample expansion are not model improvements. Confirmed same-photo overlap with the baseline's upstream source excludes all Construction-PPE from independent final test or new training/calibration.

Temporal E00 native uses all3274 original frames. The paired PTQ experiment explicitly uses225 zero-based indices0,15,30,... (2FPS at source30FPS) across the same20 videos, chosen to fit the measured CPU inference budget before valid paired metrics. All selected RGB hashes/counts and PTS are frozen before either valid quantized run. Native outputs are replayed at the identical indices for reference. Never compare full-cadence vs2FPS metrics as a model gain; short uncertain observations can be skipped by sparse sampling. A failed preliminary CFR-duplicating decoder run is invalid diagnostic evidence, not a quality result.

Source-reference temporal metric v1.1 changes only F1 definition to2TP/(2TP+FP+FN), with null when its denominator is zero; precision remains null with no predictions and recall null with no positive support. Thus all missed positive events have F1=0. Historicalv1 nullF1 reports are retained; all compared configurations are rescored under v1.1. Coarse onset bounds, explicit unrun-video census, unknown windows and source-reference-only qualification remain unchanged.

Stages are BASELINE, EVALUATED, IMPROVED, FROZEN. At most two failed justified hypothesis families per scenario; multiple operating points of the same declared hypothesis share its budget. IMPROVED requires the declared paired validation gain and real LinQ qualification; no current candidate has passed both. A retained baseline can be FROZEN without improvement, with independent-test/quality failures explicitly open. New dataset discovery/acquisition belongs to the separate Data Orchestrator; its branch is not modified by ML agents.

## Autonomous night cycle protocol supplement

Immutable READY handoff and exact task capability are required before experiments; private source-box/import diagnostics do not authorize training or independent test. Current consumer interface is DATA_HANDOFF_PROTOCOL.md. Existing model/data baselines are reused; no completed test or rejected hypothesis is repeated without a new design/data justification.

E001 Helmet hypothesis is diverse source-disjoint calibration with unchanged YOLOv8n weights/sourcegraph/export/decoder/confidence.25/NMS.45. Compare current baseline quantized and candidate quantized on SAME52revieweddevelopmentimages (canonicaldataset39e13..., serializedfile346f74...). Primary acceptance: macroF1 gain>=.01, no classrecall decrease>.02, no bare_head FP increase. Native baseline saved predictions are reference only. Quantized CPU is SIMULATED, not LinQ execution; new candidate cannot replace the hardware-verified baseline before actual isolated LinQ and independent quality gates. Maxone such calibration candidate; optionalshortsamearchitecturefine-tune only with approved READY complete training data. Never use original-source test or SH17reservedtest for calibration.

E002 actual frozen resolution diagnostic: producer EDF native source3, original320x240 RGB vs PIL BILINEAR half160x120 then restored320x240 BEFORE identical640letterbox. Same2584selected indices0,5,... pervariant, encodedMP4PTS,24sourcepositive windows, endpoint-origin uncertainty +/-1originalframe. Native UR640x480 was unavailable, so no unpaired UR-preview comparison was made. Complement90.48% UNKNOWN. Support[start,confirmed] vs confirmation-point coverage are separate diagnostics; prolonged_lying is never counted as a source fall. Precision/F1/falsealerts-hour/personrecall NOT_MEASURABLE without corresponding GT. Keep unconditional observability/frame denominator alongside conditional per-detection torso rates.

E004 fixed optional same-side torso-pair candidate replays unchanged UR20 observations, same2FPS225primary frames and3274fullcadence secondary frames, same confidence/geometry/gap gates. Missing points cannot supply immobility evidence. Accept only event improvement without negative regression; no gain observed, flag remains OFF. Native/half-resolved EDF and partial torso are the two NEW Fall hypotheses in this night; no third.

E005 fixed second Helmet candidate extracts only the last Concatenation inputs, decoded boxes[1,4,8400]/class probs[1,2,8400]. Same trainedweights/sourcegraph operations, same8calib, conf.25/NMS.45 and52GT. Require raw float bitwise parity BEFORE PTQ, then compare both to existing best baseline and same-data8 control with E001 gates. Float parity PASS; quantized quality FAIL. No rejected candidate is uploaded merely to prove it can execute.

E003 uses producer CAVIAR source3 immutable originalJPEG/XML, every5th sourceframe345frames, sourceFrameID*40ms NOMINAL25FPS_DERIVED (not originalcameraPTS). Source visible literal run/walk only; appear/disappear, other states and unboxed regions UNKNOWN. Class-aware unique bidirectional IoU>=.5 ownership; missing model observation of known running actor remains FN. Three running windows (one right-censored),46sampled running actorframes,482walking actorframes. Baseline observedankles .2image-diagonals/s,1000ms confirmation,750msmaxgap,person/KP.5; H1 bodyheight normalization1.5/s; H2 observedbboxcenter same.2diag/s, with edge/visibility/gap resets, running-only and no invented polygon. One nativeNNpass is reused; policies are fixed before each replay. Gain in scoped eventF1 required, no accepted gain. See ml/quality/temporal/CAVIAR.md. Operational falsealerts/hour, industrial gait accuracy and Zone metrics NOT_MEASURABLE. Both NEW hypotheses consumed, no ROI third experiment.

No independent final test was available or used. New neural candidates did not qualify on development and therefore no new actual LinQ task was justified. Historical runtime qualification remains valid evidence; new Matvey-path placement remains a separate unsatisfied gate. No network/services/captain state were changed.
