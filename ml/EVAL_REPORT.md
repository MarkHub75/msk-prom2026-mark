# Evaluation report — quality sprint checkpoint

No candidate has been promoted. Software tests and hardware execution are separate from task accuracy. All quality numbers below are DEVELOPMENT diagnostics, not independent industrial test results.

## Helmet, fixed quality-v3

52 fixed images,44 complete per class,6 partial,2 unknown. Original52selection was frozen before predictions; source boxes repaired blind with version history, second AI review of8selected images, no independent human expert. DatasetSHA25639e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a. Confirmed same-photo overlap with baseline's upstream source means this source is development-only, never independent test.

| Full-frame confidence.25 | GT | TP | FP | FN | Precision | Recall | F1 | AP50 | mAP50:95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| helmet |25|19|11|6|.6333|.7600|.6909|.6661|.2473|
| bare_head |32|23|7|9|.7667|.71875|.7419|.8441|.6318|

MacroF1=.716422. These are class-aware OBJECT-BOX metrics, not wearer ownership or incident metrics. Partial/unknown images do not contribute primary precision/AP. AP uses custom101point evaluator, not a claim of exact COCO parity. Raw original32 E00 and GTv1/v2 are retained; better scores on repaired/expanded GT do not constitute model improvement.

| Hypothesis / same52GT | MacroF1 | helmet recall | bare_head recall | Decision |
|---|---:|---:|---:|---|
| H-HELMET-01 confidence.4 |.652482|.60|.53125|REJECT: F1/recall guard fail |
| H-HELMET-01 confidence.5 |.522727|.40|.375|REJECT: F1/recall guard fail |
| H-HELMET-02 fixed four tiles |.606575|.72|.84375|REJECT: overallF1 and helmetrecall fail |

Two failed hypothesis families reached. Freeze full-frame helmet-v1 .25/NMS.45; no more Helmet tuning in this stage. Tiling uses208nativecalls; totalframe diagnosticmean137.11ms including NPZwrites is not TPU speed. Rejected policy receives no LinQ promotion or final-test tuning.

## Fall/Lying

20 URFall development clips,3274original-PTS frames/109.133s,10source-reference fall episodes,0eligible>=3s floor-lying positives.59unknown source frames/1.967s; author labels plus sampled blind AI context review, not expert/exhaustive industrial GT. The native preview is DEPTH|RGB; only right320x240RGB is input. ADL10 intentional bed lying is negative for fall/floor violation. Native transition0 labels are coarse1s onset support; uncertainty is carried into matching. No false-alerts/hour claim from this limited reviewed exposure.

| Pipeline/cadence | Neural placement | TP | FP | FN | Precision | Recall | F1 | Scope |
|---|---|---:|---:|---:|---:|---:|---:|---|
| E00 all3274frames | RTX native |0|0|10|undefined|0|0*|20 source-reference clips |
| E00 fixed2FPS/225frames | replay of RTX native outputs |1|0|9|1.0|.10|.1818|Same20clips, different sampling protocol |
| H-FALL-02 allframes | same saved RTX outputs |0|0|10|undefined|0|0*|Rejected: no gain |
| H-FALL-02 fixed2FPS | same saved RTX outputs |1|0|9|1.0|.10|.1818|Rejected: no gain |
| E00 URfall01/2FPS11frames | REAL LinQ |0|0|1|undefined|0|0*|One development clip, no industrial generalization |
| H-FALL-01 baseline PTQ | vendor CPU quantized simulation |1|0|9|1.0|.10|.1818|Matched225frames/20clips |
| H-FALL-01 new PTQ | vendor CPU quantized simulation |1|0|9|1.0|.10|.1818|REJECTED: same quality as baseline |

*Protocolv1.1 computes F1 from2TP/(2TP+FP+FN), hence0for all missedGT; precision remains undefined with zero predictions. Historicalv1 reports used nullF1 and are retained. All comparisons use the same metric version before decisions. Prolonged-lying recall is undefined due zero eligible positive support, never100percent.

The large cadence sensitivity is not a model improvement: sampling can remove brief uncertain observations which reset continuous evidence. Missing-person and uncertain-posture rates must accompany any future temporal comparison. Hypothesis02 retains only recent confirmed upright timestamps through uncertain pose; it is OFF by default, did not improve this dataset and is not promoted. PTQ was the second/final Fall hypothesis and also gave no gain. Both valid runs completed225calls (baseline472.386s/candidate464.813s CPU2). Same source IDs/PTS/RGB were independently checked; no third sweep. The initial32-call CFR-duplicating decoder diagnostic is retained as INVALID, not scored and not counted as a quality gain/failure. Freeze the baseline as a runtime rollback with quality NOT_ACCEPTED; candidate was not staged on LinQ.

## Actual hardware and latency

Prior own-model Helmet/Split-Pose captures remain valid execution evidence. NEW real URfall01 test:11unique correlated LinQ replies/status0, all numeric journal hashes verified, sourceFPS30/sample2, maximum concurrentrequests1; no neural fallback. No event,1missed source-reference fall.11calls took131.018s, processedFPS.083958, RPCp50=10.630s/p95=18.967s. Timing is full transport-inclusive round trip, not device time. EOFfinalization made0newrequests. Artifacts /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps, first-window performance saved separately from cached/finalization metrics. This is not realtime or successful fall recognition.

Native full3274frame reference took49.699s including local diagnostics; it is separate GPU performance, never substituted for LinQ. Numeric audit of3industrialinputs showed nativeFP->conditioned/PTQ confidence loss, vendor simulation/hardware bitwise matching class/KP scores, and preserved current Split-Pose keypoint confidence. One isolated8frame-calibration PTQ program compiled but is NOT deployed/qualified; baseline retained.

## Running/Zone and remaining official scenarios

Offline RunningZonePrototype reuses existing tracking, visible-ankle anchors, originalPTS, explicitcamera geometry and confidence. Outputs are UNVALIDATED_PROTOTYPE diagnostics, not public events or recognized running. Image-plane displacement alone is not gait or metric speed. No production Running/Zone recognizer or data-backedP/R/F1 is claimed. See SCENARIOS.md for all8official examples and supplementaryHelmet stages.

New data acquisition/curation belongs to Data Orchestrator. Its worktree/branch is untouched. Independent final test is NOT_RUN; SH17 intake handed off before GT/model evaluation. Additional scenarios wait for suitable data rather than being presented as measured recognizers. No new neural architecture or long training has been launched. The isolated PTQ program changes calibration of the existing graph. After merging the reusable quantized backend,319 software tests passed in the client environment. Four fixture tests initially required absent Torch; a test-only adapter fixed that environment dependency without installing packages or changing production behavior. Later code merges require affected checks again.

Final software check after all code merges:335 tests PASS in5.851s. Running/Zone missing-GT readiness check returns NOT_EVALUATED with null P/R/F1; synthetic examples test only software. See ml/quality/temporal/MOTION_EVAL.md for annotation/track/geometry handoff. Precision1.0 in Fall is supported by only one alert; no robust industrial generalization follows. Generalization CIs are not estimated from one conservative temporal source group or unresolved PPE photo lineage. All selected checkpoints remain unchanged.
