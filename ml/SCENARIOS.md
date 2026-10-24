# Scenario quality register

## Актуальный ночной итог

Эта старая матрица сохранена как история предыдущего цикла. Текущие стадии и восемь сценариев: [SCENARIO_COVERAGE.md](SCENARIO_COVERAGE.md). CAVIAR теперь оценён на source-scoped development:0/3runningwindows, обе новые гипотезы отклонены; Zone по-прежнему без GT. Helmet E001/E005 и Fall E002/E004 также закрыты без promotion. Старые «ожидаем/не оценено» ниже не относятся к текущему READY/ночному циклу.


Authority: official LinQ case page4 lists eight example scenarios, not an obligation to ship eight unvalidated recognizers. Helmet is supplementary. The app contract and existing production video worker are unchanged.

Stage policy: BASELINE pins executable/checkpoint/config; EVALUATED requires saved TP/FP/FN and support on fixed labelled data; IMPROVED requires the predeclared validation criterion and LinQ qualification; FROZEN pins the best verified bundle and rollback. Unavailable prototypes remain BASELINE/NOT_IMPLEMENTED. A baseline may be frozen unchanged with improvement=false and open independent-test gates. At most two failed justified hypotheses per scenario; threshold .4/.5 are operating points of one hypothesis, not two unrelated experiments. No test-driven tuning.

| Official scenario | Stage / implementation | Algorithm / missing component | Data contract requested from Data Orchestrator | LinQ gate |
|---|---|---|---|---|
| Running / abrupt movement | BASELINE / UNVALIDATED_OFFLINE_PROTOTYPE | Existing pose/person tracks; confidence and PTS guarded motion, camera-dependent image-plane thresholds; no uncalibrated m/s | Actor/track episode intervals, walk/run/turn hard negatives, gaps/ID switches, camera geometry and independent groups | Split-Pose actual hardware PASS; running rule NOT_EVALUATED |
| Proximity to moving machinery | BASELINE / NOT_IMPLEMENTED | Person + equipment detector, explicit danger geometry and relative motion | Equipment boxes, movement and near/safe episode GT; camera calibration if metric distance required | Person pose PASS; equipment model/export/PTQ NOT_RUN |
| Phone use | BASELINE / NOT_IMPLEMENTED | Small-object detection plus hand/head ownership and time support | Phone boxes and use episodes; tools/occlusion negatives; unknown coverage | No phone model qualified |
| Smoking / open flame | BASELINE / NOT_IMPLEMENTED | Separate cigarette/smoke/flame evidence plus time/authorized-area policy | Positive and difficult negative sequences; source rights and visibility | No model qualified |
| Barrier / conveyor / suspended-load crossing | BASELINE / UNVALIDATED_OFFLINE_POLYGON_PROTOTYPE | Existing person tracks + versioned polygons/direction; scene-specific load/conveyor semantics | Geometry provenance, crossing episodes, boundary touches, re-entry and tracking failures | Pose PASS; polygon event semantics NOT_EVALUATED |
| Height without visible safety equipment | BASELINE / NOT_IMPLEMENTED | Configured hazardous region + person/pose + visible harness evidence; unknown when unobservable | Scene/height policy and visible equipment labels; occlusion negatives | Pose PASS; harness model NOT_RUN |
| Fall / prolonged lying / immobility | FROZEN / baseline retained; fall quality NOT_ACCEPTED | Split-Pose + existing posture/transition/gap/confirmation rules; no medical diagnosis | Fall transitions, floor vs bed, sitting/crouching/bending, >=3s observable lying; unknown and censoring | Split-Pose actual hardware PASS; PTQ candidate rejected; independent quality gate open |
| Cargo handling, supplementary case example | BASELINE / NOT_IMPLEMENTED | Person/load ownership and trajectory/posture with explicit violation policy | Load boxes, policy-qualified episodes and safe carrying negatives | No load model qualified |

Supplementary Helmet: FROZEN with improvement=false after two failed hypothesis families on development-quality-v3 (52 images,44 complete/class). Confidence .25 baseline retained; .4/.5 and fixed tiling fail the declared criteria. No further Helmet tuning in this stage. Person ownership/event accuracy and independent source test remain open. Actual Helmet TPU executes, which does not establish industrial accuracy.

Experiments allocated at stage start (completed/readiness delivered; outcomes below): (1) unchanged Fall E00 on20 URFall clips/all3274 original-PTS frames; (2) one Split-Pose PTQ candidate with8 fixed industrial calibration frames, followed by paired validation and actual LinQ only if justified; (3) Running/Zone offline E00 with explicit uncertainty, then dataset-backed episode evaluation when the Data Orchestrator supplies GT. No long training is allocated.

GPU coordination: /workspace/artifacts/quality/gpu.lock is an advisory exclusive flock shared by all heavy jobs. Root native UR20 evaluation completed and released it. Every ML/Data worker must agree to acquire it; its existence alone cannot enforce cooperation by an external process. No simultaneous training/evaluation; new long runs require explicit allocation. Compiler/PTQ experiment is CPU-only with two threads. Do not change another orchestrator's branch.

Fall closure: both PTQ calibrations on the same225frames have TP1/FP0/FN9, recall.10/F1.1818. Upright-history retention also gave no gain. Two failed families reached; freeze the original checkpoint as runtime rollback, NOT an accepted accurate fall detector. No third Fall hypothesis. Running/Zone is next, pending real episode GT from Data Orchestrator.

Running/Zone evaluation readiness: scorer and annotation contract completed in ml/quality/temporal/MOTION_EVAL.md. No real episode GT or approved polygons -> NOT_EVALUATED/null metrics. Existing code plus335 software checks is engineering evidence only.

Next three data-dependent experiments, with no automatic launch: (1) Running vs walking/turning episode evaluation with the Data Orchestrator frozen GT and an explicit experimental motion proxy; (2) Zone entry/direction evaluation with approved polygons and track/actor truth; (3) equipment-person proximity baseline only after suitable labelled data and detector availability. Each new neural version still requires ONNX/PTQ/real LinQ qualification. Phone, smoking/fire, height and cargo follow sequentially when appropriate data are available.
