# Active ML/CV task register

## Закрыт дополнительный анализ сохранённых выходов

E006: четыре потерянных bare_head TP послеPTQ имеют savedoverlapIoU>=.5, score<.25; Native/float primarymatches одинаковы, raw неbitwise. E007: running30/46безdecodedperson,16/46IoU<.5,0потерь наconsumer.5. E008: localartifact/runtimeevidence integrityPASS, independentquality/newplacement/backup всёещёнеподтверждены.417softwaretestsPASS. НиодногоновогоNN/TPU/GPU/обучения/порогов, budgetsнеобнулены. Отчёты: NIGHT_REPORT.md и ml/reports/night-followup-20261024.json. Переходкследующемуциклу толькопоновойзадаче.

## Ночной ML-этап 24.10.2026 — завершён

- Инвентаризация: две обученные YOLOv8n модели, точные checkpoint/export версии, SHA256, исходные/отклонённые ONNX/TPU в ml/MODEL_INVENTORY.md.
- E001/E005 Helmet, E002/E004 Fall, E003H1/H2 Running: две новые гипотезы на направление закрыты; ни одного promotion. История/метрики в ml/EXPERIMENTS.csv и ml/reports/night-20261024*. Ни одной новой тренировки или TPU-задачи.
- Data Orchestrator handoff: read-only четыре READY версии, EDF/CAVIAR использованы строго в approved development scope. Независимый test/clean train/zone-policy GT не готовы.
- Безопасность общего LinQ: matvey/ и matvey_ namespace, один собственный активный запрос между журналами, durable UNKNOWN, own bootstrap publication lock/fsync, старые completed captures доступны офлайн. Физическая сеть/очереди капитана не тронуты.
- Проверки:397softwaretests PASS; новые графики PNG/SVG/PDF и контрольные суммы вне Git. Bootstrap только PREPARED, не опубликован; новое размещение в matvey/ не подтверждено.
- Backend/frontend не менялись. Переход к интеграции/новым функциям в этот цикл не выполняется. NIGHT_REPORT.md и RESUME.md — точка продолжения. Новые heavy jobs не активны.


## Latest backend/recovery stage

- Baseline c8dd54a2 clean and matched origin/matvey_cv. Mark backend code/URL not supplied; GitHub connector404 and noninteractive remote-head read failed. Actual external backend integration remains OPEN, not a local-test PASS.
- DELIVERY: committed ACK schema, strict revision type, durable destination/media-prefix digest, ACK-loss replay and no silent endpoint change.
- CHECK: prepared backend_probe for explicit POST/ACK/journal/JPEG and stable labelled probe UUID. Local-test HTTP passed with1revision/1notification; Mark's journal/frontend/media have not been contacted.
- RELIABILITY: e2555e5f merged. REALnewframe13 of4_tr6: confirmed publish -> clientclose ->UNKNOWN, cursor unchanged ->receive-only SAMEUUID completion ->Helmet completion.2freshRPCs total, no retry publication. Physical VPN/SSH untouched; do not rerun this one-shot test.
- PERFORMANCE: one ordinary Helmet call10.430s; setup3.286s, publish/confirm4.496s, responsewait0.958s, close1.650s. Proposals documented, no realtime/speedup claim.
- VERIFICATION:231tests PASS. README, ACK schema, handoff/check and performance docs updated. Await actual backend endpoint/source; no new models/types or automatic follow-on work.

This section supersedes earlier task-stage statuses below.

## Latest video-MVP iteration

| Item | Owner | Result |
|---|---|---|
| Verified runtime manifests | Detection / agent/detection | a6597683 merged; real captures/ABI/hashes checked, candidate artifacts unchanged |
| Behavioral acceptance | Behavior / agent/fall | c654d9ab merged; original engine reused, strict ownership/gaps/dedup, explicit DEMO policy only |
| Remote frame factory | LinQ / agent/linq | 9a5e5d45 merged; stable logical-frame mapping, UUID journal/cache/reconcile, one outstanding task fence |
| File MVP and handoff | Root / matvey_cv | Durable source cursor + observation/behavior/event transaction, snapshots/PTS, local HTTP test receiver, schema/example/docs |
| Actual LinQ execution | Root | 2 REAL industrial frames /4status0RPCs, no confirmed episode; labelled repeated-image integration fixture6frames/12status0RPCs ->1episode/2revisions/1testnotification |
| Verification | Root | 217tests PASS; schema/source-evidence/HTTP PASS on labelled fixture; completed restart0newRPCs, no duplicate event export |
| Industrial positive quality | Requires reviewed source/video | OPEN: current real clips produced insufficient model evidence; never count abstention as compliance |
| Team backend/frontend | Mark / frontend participant | OPEN: adapter/contract ready; actual two-team-service interaction and permanent evidence hosting not verified |

Current iteration closes after checkpoint/commit. No further feature, research, training or remote experiments start without the user's next instruction. Historical rows below are superseded by this section and RESUME.md.

Baseline: matvey_cv 118e068b; continuation retains the approved MVP. Root is the sole writer here. Existing 61 tests and model/compiler/simulator evidence are documented in docs/STATUS.md.

| ID | Owner / directory | Task | Acceptance | State |
|---|---|---|---|---|
| LQ-01 | LinQ / agents/linq | Capture a real supplied notebook call without notebook/session secrets | Numeric tensors + program/input/output hashes + timing; safe failure; tests; user-run cells/runbook | Code merged fd5adcbf; real capture pending user session |
| CV-02 | Detection / agents/detection | Compare captured TPU tensors to float/golden and decode split pose | Explicit name map, shape/dtype checks, per-output and decoded differences; tests; no automatic PASS quality claim | Merged 133ea22e; actual TPU capture pending |
| BH-02 | Behavior / agents/fall | Reproducible event acceptance scenarios | Helmet, fall, lying, immobility, gaps, ambiguous owners, no repeat; source-native backend label; deterministic semantic expectations | Merged 50dd2f65; 8 scenarios / 101 observations / 7 incidents / 12 revisions |
| OR-02 | Root / project | AGENTS, architecture, contract consistency, review and integration | Isolated branches, no main/research/media changes, combined tests pass | Implemented; checkpoint RESUME.md, 96 combined tests PASS |
| HW-01 | User existing Jupyter | Run stock example.ipynb and export safe capture | Completed ResNet50 TPU call; no credentials/full notebook outputs in export | User reports stock status_code=0/class257/0.39s; numeric capture pending |
| APP-01 | Backend/frontend team | Real event endpoint, evidence serving, alert/journal | Persist-before-ACK + idempotent event revisions + visible evidence and filters | External integration pending |

Historical completed coding agents are not counted as running. Live state must be checked through native agent tools; this table records work items rather than pretending hardware access or background execution.

Checkpoint saved at user request: see ../RESUME.md. All three coding agents completed; no continuing background tasks. The later resumed packaging stage below supersedes that checkpoint; the current kit has been built.

## Resumed packaging stage

- KIT-01: current portable kit builder, runtime-only source/dependencies/docs and existing Helmet + Split-Pose TPU programs; archive is /workspace/artifacts/linq-jupyter-kit.zip. Inventory and isolated imports/model preparation checked.
- LQ-02: portable prepare_case/capture_case merged from agent/linq 56a3d13f; no new training, export or SDK experiments.
- Binding limitation: actual remote example.ipynb import/call/result extraction is still not available locally. User was asked for only credential-free code. bindings.py refuses to issue any request until an actual binding exists. The public local pytpu example is clearly labelled LOCAL and is not substituted for the working remote API.
- Current suite:113 tests PASS. Stock inference is confirmed by user report; own-model hardware capture remains pending.

## Own-model upload and network resilience

- STOCK-RPC: actual automatic ResNet50 completed, results/integrity outside Git; never repeat as a connection check.
- DEPLOY-01: both actual uploads STAGED with matching remote SHA256/byte counts; one real inference per model completed. Helmet 262bdaa1...: status 0, float32 [1,6,8400], 10234.49 ms, 2 bare_heads; reference 1 matched at IoU 0.9252 plus 1 extra actual. Split-Pose 1f986b07...: status 0, 4 expected float32 tensors, 11152.85 ms, 3 persons, visible keypoints 16/17/9. Both capture integrity/ABI/decoding/same-input smoke PASS. Results outside Git in helmet-001/ and pose-split-001/. Do not repeat uploads/inferences.
- RPC-RECOVERY: 7f705a32, 474afee8 and 97a7a5d2 merged. Fsynced pre-publication intent/context, UNKNOWN state, retained ambiguous reply queues, numeric response durable before ACK, receive-only/offline CLI reconciliation. Root added local/pending capture resume and deployment/request locking. 37 affected transport + 13 affected pipeline tests PASS; old full suite not rerun.
- INFRA: Arch user manages autossh/systemd/VPN; Vast must not change this configuration.
- Next: connect the verified remote model bindings to the existing video worker/backend, then measure target-video quality and full-chain latency. Historical packaged manifests are not automatically promoted to production bindings.
- ITERATION CLOSED: user explicitly requested a final checkpoint and stop. No active agent tasks or further automatic development; wait for the user's next instruction. Artifacts retained, server left running.
