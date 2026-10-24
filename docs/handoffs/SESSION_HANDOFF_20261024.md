# HISTORICAL HANDOFF — superseded by the scene-pack continuation

**Latest context:** [SESSION_HANDOFF_20261024_SCENES.md](SESSION_HANDOFF_20261024_SCENES.md).
Read that file first: captain moved rules/app to Mark, and seven full localGPU
scene packs are now ready. The snapshot below is preserved as history; its old
"no full scenes"/Git-auth/priority statuses are not current.

# SESSION HANDOFF — MOSPROM-2026, ML/CV

Снимок: **2026-10-24 12:47:31 UTC / 2026-10-24 15:47:31 МСК**. Дедлайн: **25 октября 2026, 10:00 МСК = 07:00 UTC**. Это передача контекста, а не разрешение автоматически начинать новые обучения или сетевые эксперименты.

## 1. Роль, текущая цель и границы

Роль — главный ML/CV Orchestrator Матвея: модели, правила поведения, оценка качества, контракты ML-наблюдений, общий видеопайплайн и квалификация инференса на настоящем LinQ. Марк разрабатывает backend, Егор — frontend; их код не менять. Data Orchestrator отвечает за источники/очистку/разметку/публикацию данных, Training Orchestrator — за обучение и экспорт кандидатов. Не дублировать их исследования, не редактировать их worktree.

Последняя содержательная директива изменила приоритет с Helmet/Fall/Running на **исполняемые прототипы всех восьми групп официального кейса**, затем выбор трёх направлений доведения. Техническое покрытие реализовано и заморожено. Приоритеты доведения: **07 → 02 → 01**. Это не три достоверных готовых видеодемонстрации. Helmet полезен отдельно и не заменяет ни одну из восьми групп.

Текущая операция — только этот handoff. Новых ML-экспериментов, обучений, LinQ-запросов, сетевых настроек или изменений pipeline при его подготовке не было. После записи остановиться. Следующая сессия должна продолжать по новой задаче пользователя, не перезапускать архитектурное исследование.

## 2. Git, рабочие каталоги и сохранность

- Единственный рабочий каталог root: **`/workspace/project`**.
- Ветка: **`matvey_cv`**. Не переключать ветки, не изменять `main` и ветки капитана.
- **HEAD до создания этого документа: `4b10c7a7332b7ce5ac1aa8233acb6be1df5eb893`** (`Freeze eight runnable behavioral prototypes with honest video evidence and ranked priorities`).
- Проверенный ML-code checkpoint до последней документации: `77e019f47242d38a97adb513fbe68a76e8295309`; финальный лог — 480 тестов PASS.
- На старте передачи tracked/staged изменений нет. Единственный pre-existing untracked: **`.ipynb_checkpoints/`**. Содержимое не открывалось, не удалялось и не индексировалось; не делать `git add .`.
- Этот файл сохраняется отдельным документационным коммитом. Его собственный SHA невозможно корректно встроить в его же содержимое. Точный containing commit: `git log -1 --format=%H -- docs/handoffs/SESSION_HANDOFF_20261024.md`; текущий HEAD: `git rev-parse HEAD`.
- Все изменения основной ML-сессии закоммичены локально. Remote SHA/push **не подтверждены**: прежние попытки завершались exit128/AUTHENTICATION_UNAVAILABLE; аутентификационные циклы не повторять. Не force push.

Снимок refs других worktree (это не проверка их чистоты; они не изменялись):

| Worktree | Branch | HEAD при передаче | Ответственность |
|---|---|---|---|
| `/workspace/agents/detection` | `agent/detection` | `ddd8b26d` | Object/context правила03/04/06/08, screen, E012 |
| `/workspace/agents/fall` | `agent/fall` | `0c88b073` | Правила01/02/05/07, floor/camera guards |
| `/workspace/agents/linq` | `agent/linq` | `0cf284e1` | LinQ/Training требования, отдельный passive broker report |
| `/workspace/agents/data-audit` | `agent/data-audit` | `b2a58b98` | Data Orchestrator |
| `/workspace/agents/training` | `agent/training` | `0832ef99` | Training Orchestrator |
| `/workspace/agents/speed` | `agent/speed` | `07b4d6fe` | Резерв, не назначать без необходимости |

В `agent/linq` есть **не включённый в matvey_cv** коммит `0cf284e1`, только `docs/linq/QUEUE_CHECK_2026-10-24_112616Z.md`. Его можно читать через `git show agent/linq:<path>`. Не мержить автоматически; Data/Training ветки передают результаты через manifests, а не merge.

Среда не считается защищённой от recycle/destroy: по предыдущему capability-аудиту `/workspace` не volume-backed. Обычный stop/start и уничтожение/recycle — разные вещи. Сервер не останавливался.

## 3. Что реализовано: общий конвейер и восемь сценариев

### Общие компоненты

- `ml/detection/`: preprocess/decoder/native-reference, YOLOv8 Detection/Pose и split-output ABI.
- `ml/behavior/engine.py`: существующий person tracker, временные переходы, confirmation, gaps/epoch reset, дедупликация и legacy EventMutation.
- `ml/linq/{amqp,journal,admission,namespace,video}.py`: единственный официальный AMQP-клиент и durable состояние. Не писать второй клиент.
- `ml/pipeline/{cli,file_video,runner,delivery,evidence}.py`: видео/наблюдения → behavior → транзакционный outbox/checkpoint → JSON/evidence. Старые backend adapters сохранены; реальная интеграция с Марком не объявлена выполненной.
- `ml/scenarios/common.py`: общая геометрия и sourced facts.
- `ml/scenarios/engine.py`: **один** общий context, существующий BehaviorEngine обновляется один раз, общая ассоциация предметов, temporal/dedup для восьми групп.
- `ml/scenarios/{contracts,journal,cli,fixtures}.py`: внутренний EventCandidate, отдельные таблицы в той же SQLite транзакции, replay, явно синтетические acceptance inputs.
- `ml/pipeline/video_clock.py`: encoded best-effort presentation time через установленный ffprobe. Не подменяет время wall clock или предполагаемым FPS.
- `configs/scenarios/01.json` … `08.json`, `suite.example.json`: отдельные конфиги плюс объединённый opt-in suite. По умолчанию site geometry/политики не выдумываются.

**Контракты:** `ml/contracts/schemas/observation.schema.json`, `event.schema.json` и `ml/contracts/__init__.py` остались byte-identical к checkpoint8f879606. Новый `event_candidate.schema.json` — **INTERNAL additive profile** `mosprom.event_candidate.v1`, не расширение внешнего EventMutation v1. Внешний endpoint по-прежнему получает только `missing_helmet`, `suspected_fall`, `prolonged_lying`. Новые candidate-типы в HTTP Марка не отправляются.

Опциональная интеграция в существующий worker: `--scenario-config <suite.json>`. Новый конвейер не включается скрытно; не меняет рабочие веса. Выходы: `events.sqlite`, `candidates.jsonl`, `scenario-diagnostics.jsonl`, `scenario-summary.json`, `evidence/*.jpg` и sidecar JSON. Sidecar содержит исходные frame/PTS/media/RGB/snapshot SHA. Candidate confidence может быть null; это не calibrated probability. `episode_group_id` связывает07 с исходной legacy-историей.

### Реальные статусы восьми групп

Точный текст страницы4 и SHA PDF/image: `ml/scenarios/catalog.json`. Полная матрица: `ml/SCENARIO_COVERAGE.md`. Все восемь имеют **PROTOTYPE + RUNNABLE**; это означает исполняемые правила на определённых наблюдениях, а не наличие всех необходимых trained detectors.

| ID / правило | Файл в `ml/scenarios/rules/` | Реальный статус и критический блокер |
|---|---|---|
|01 Бег / резкие перемещения в зоне техники | `motion.py` | Раздельные running-action и apparent-motion. CAVIAR run/walk доступен; новая action-модель не квалифицирована. Старый motion-proxy TP0/FP0/FN3. E012 не восстановил running observations. Для image-speed нужны camera-bound зона/политика/статичная камера; никаких м/с без калибровки |
|02 Сближение с движущимися механизмами/транспортом | `machinery.py` | В промышленном screen3 контекста погрузчика, но опасность и GT не установлены. Нужны детектор техники, треки/наблюдаемое движение и утверждённая danger policy. Измерения в pixels/body-heights — проекция, не физические метры |
|03 Телефон при оборудовании/перемещении | `phone.py` | Нужны owned phone, action/use, wrist/head visibility и activity context. Присутствие телефона само по себе недостаточно. Qualified detector/action pipeline отсутствует |
|04 Курение / открытый огонь вне разрешённых мест | `fire_smoking.py` | Smoking/open-fire раздельно. В видео есть неоднозначная дымка, не подтверждённые сигарета/огонь. Нужны discriminator/gesture/ownership/allowed-zone policy |
|05 Ограждение / под конвейером / подвешенным грузом | `barriers.py` | Три подправила `fence_climb`, `under_conveyor`, `under_suspended_load`; одно пересечение линии не считается перелезанием. Нужны action/pose/operation facts и surveyed geometry. Реальное действие не установлено |
|06 Высота без использования привязи | `height.py` | Объявленная height/work зона + visibility + wearer-linked absence/use. **Present alone→UNKNOWN**, observable in_use→NEGATIVE; visible absence/not_in_use→POSITIVE. Не делать вывод по отсутствию аннотации; реальное событие не установлено |
|07 Падение / лежание на полу / видимые опасные признаки | `fall.py` | Обёртка существующего engine, без медицинского диагноза. Реальный saved-native fall06→1candidate и ready JPEG; ordinary reference→0. Лежание/неподвижность требуют пола. SOURCE EVALUATED, качество слабое; полноценная аппаратная проверка позитивного нового эпизода отсутствует |
|08 Переноска груза с нарушением правила — дополнительный | `cargo.py` | Owned manual cargo + конкретное правило зоны/наблюдаемое закрытие лица. Не выводить массу по bbox; forklift stack не подменяет manual-cargo GT. Детектор/ownership/policy не квалифицированы |

**Ни один полный новый сценарий нельзя пометить LINQ_VERIFIED только из-за старого person/Pose status0.** При отсутствии модели, visibility, ownership или политики — UNKNOWN/BLOCKED. Synthetic/manual facts не превращаются в model predictions или независимый GT.

## 4. Что проверено и где доказательства

### Программные и синтетические проверки

Последний полный запуск: **480 tests PASS за7.585s**, `/workspace/artifacts/matvey-scenarios/software-tests-release.log`. Во время создания этого handoff тесты повторно не запускались: проверен существующий лог и фактические файлы.

Основные новые тесты:

- `tests/test_scenarios_objects.py`, `test_scenarios_spatial.py`: positive/negative/insufficient для всех правил/подправил, floor/harness/camera semantics.
- `tests/test_scenarios_suite.py`: all8 через общий pipeline, candidate JSON Schema, evidence frame/PTS, restart/replay/dedup, gaps/epoch, rollback обеих state-машин, immutable input, duplicate object IDs, real fact source-binding, writer-lock, site camera/image binding и immobility support time.
- `tests/test_scenario_video_clock.py`: nonzero encoded origin, duplicate/missing PTS, ordinal evidence без approximate seek.
- `tests/test_scenario_person_roi.py`: crop geometry/global coordinates/global NMS и неполные GT.
- Старые transport/capture/recovery/backend-local-test regressions также входят в480. Их успех — software evidence, не accuracy.

24 labelled synthetic cases (8×positive/negative/unknown) PASS: `/workspace/artifacts/matvey-scenarios/release-acceptance-v1/coverage-acceptance.json`. Synthetic JPEG подписаны явно. Ранние `coverage-v1`, `command-acceptance-v1`, `final-acceptance-v1`, `freeze-acceptance-v1` и failed-test logs сохранены; использовать последний release snapshot, не перезаписывать историю.

### Настоящие source-видео и saved outputs

- `/workspace/artifacts/matvey-scenarios/real-replay-v1/real-replay-check.json`:2реальных промышленных кадра0/13, исходные PTS0/518.962ms,4**исторических** correlated status0 LinQ replies. Новых NN/RPC0; подтверждённого нарушения нет. SHA/index/PTS привязаны к оригинальному4_tr6.mp4; diagnostic JPEG не является положительным событием.
- `/workspace/artifacts/matvey-scenarios/ur07-video-evidence-v1/check.json`: source fall06,7наблюдений → **1suspected_fall**, start1500ms/confirm2500ms, **JPEGframe75 ready**. Ordinary ADL01,10наблюдений →0. Это **saved-native replay**, не новые нейровычисления и не LinQ на этих кадрах.
- Source positive inputs: `.../ur07-video-evidence-v1/fall-06-cam0/inputs.observations.jsonl`; видео `/workspace/datasets/quality/temporal/processed/urfall/fall-06-cam0-rgb.mp4`. Source SHA `8e867b39f72f239e61c04f6cd1857c8abf760725af4f5d5767e7c5204f730f64`.
- `/workspace/artifacts/matvey-scenarios/encoded-evidence-review.json`: sequential original RGB hash, encoded PTS и сохранённый sidecar совпадают.
- `/workspace/artifacts/matvey-scenarios/ur20-saved-native-2fps-v1/`:225наблюдений/20источников,1candidate07. `caviar-saved-native-v1/`:345source JPEG observations,0candidates при отсутствии action/specialist/policy facts; UNKNOWN не переименован в compliance.
- `/workspace/artifacts/matvey-scenarios/video-screen-v1/report.json`, `docs/SCENARIO_VIDEO_SCREEN.md`:16Mendeley-видео,84уникальных просмотренных кадра, нет подтверждённого positive/negative episode GT.02 review contexts: `3_tr45`, `7_te4`, `7_tr15`;04haze `5_tr19`, `6_tr15` — неоднозначно.03/05/06/08 не установлены. Sparse screen не равен temporal annotation.

Главный machine-readable итог: `ml/reports/scenario-coverage-20261024.json`; exact source hashes внутри. Малые synthetic/real-native примеры: `docs/examples/event_candidate.synthetic.json`, `event_candidate.real-native.json`.

## 5. Эксперименты и причины отказов — не повторять вслепую

Полная история: `ml/EXPERIMENTS.csv`, `ml/PROGRESS.md`, `ml/EVAL_PROTOCOL.md`, `ml/ERROR_ANALYSIS.md`, `ml/EVAL_REPORT.md`. Native, vendor SIMULATED и настоящий LinQ должны оставаться разными evidence-категориями. Test не использовался для подбора; независимого industrial final test нет.

| Эксперимент / fixed scope | Результат | Решение |
|---|---|---|
|Helmet native,52development images/44complete-class | helmet TP19/FP11/FN6, P.6333/R.76/F1.6909; bare TP23/FP7/FN9, P.7667/R.71875/F1.7419; macroF1.716422 | Source-photo overlap с pretraining, AI-review; не independent test и не wearer-event quality |
|Ранние confidence.4/.5 | macroF1.652482/.522727; оба class recalls упали за guard.02 | REJECT, baseline.25/NMS.45 сохранён; не скрывать FN повышением confidence |
|Ранний Helmet fixed tiling | macroF1.716422→.606575; helmetFP11→30/recall.76→.72 | REJECT; не повторять ту же гипотезу без новых данных |
|E001 Helmet diverse8calib | baseline vendor SIMULATED macroF1.741682, bareR.59375; candidate.735185, bareRunchanged | REJECT. Native/float counts/AP одинаковы; drift дальше conditioning/PTQ/simulator, causality не изолирована |
|E005 Helmet split output | float52raw bitwise parity; SIMULATED macroF1.327778/bareR.03125 | REJECT. Baseline уже per-channel scales; «одна глобальная шкала» не доказанная причина |
|Fall full3274frames vs matched2FPS225frames | Full TP0/FP0/FN10; at2FPS TP1/FP0/FN9, P1(1alert)/R.10/F1.1818 | Низкое качество. Cadence не сравнивать как model gain. Prolonged-lying positive support недостаточен |
|H-FALL history-retention и Pose8calibPTQ | На одинаковой cadence endpoint не улучшился | REJECT, flags OFF; mixed-output Pose также отвергнут из-за confidence quantization в simulation |
|E002 EDF3/source24positive windows | Original320×240 torso/frame.641254 vs half/restored.553793; UNKNOWN/missing.541796→.597523; support1/24→0/24, confirmation0/24both | Не менять original RGB. Вне positive90.48%UNKNOWN; P/F1/FPR/hour НЕИЗМЕРИМЫ; support coverage не event recall |
|E004 partial torso | Те же TP1/FP0/FN9 at2FPS и0/0/10full | REJECT, default OFF. МеньшеUNKNOWN без event gain не улучшение |
|E003 CAVIAR baseline/H1bodyheight/H2bbox | Все TP0/FP0/FN3, frameFN46; only11/528actors matched,0/46running | Оба REJECT. Source-derived25FPS, не camera PTS. Zone GT нет |
|E006 saved Helmet drift | Native/float primaryTP/FP одинаковы, raw НЕbitwise. PTQ сохраняет19bareTP/теряет4; у4lost есть saved overlapIoU≥.5, score<.25. Helmet восстанавливает4GT. FP18→14=9retained+5new | DIAGNOSTIC, не threshold recommendation/causal proof. Raw index binding по historical common52order, без embedded imageID |
|E007 saved CAVIAR attribution | Running46:30no decodedperson/.25,16IoU<.5,0consumer.5gate.11OOBGT относятся к walking | Consumer threshold.5 не объясняет текущий running провал. Pre-NMS tensors нет, более ранние причины UNKNOWN |
|E008 local release review | bytes/components/historical captures integrityPASS, qualityNOT_QUALIFIED | Это не подпись оборудования/автоматическое принятие качества |
|E009–E011 coverage/replay/screen/ranking |8rules,24synthetic cases, реальные saved/native source проверки; выбран07/02/01 | Engineering acceptance, не eight-model accuracy и не3qualified demos |
|E012 person ROI после покрытия |345frames/1380**CPU** calls/173.06s; running0/46→0/46, walking11/482→27/482(10retained/1lost/17new) | **REJECT**, running gain0<.10. Guard walkingcount≥11 выполнен, но primary fail. No second variant, не deploy |
|E013 timebase |6_tr15 encodedfirst39.028ms vsCVrelative0 | Исправлен opt-in clock/evidence; не accuracy gain |

E012 protocol заморожен ДО первого forward:4corner tiles60%W/H, неизменные weights/conf.25/person.5/globalNMS.45; running match-recall gain≥.10 ANDwalkingcount≥11 и recall-drop≤.02. CPU2/OpenCV1/600scap, GPU скрыта. Full345 завершён; partial scoring не использовался. Unboxed/otherstate/background UNKNOWN, поэтому precision/FPR не выдаются. Все данные: `/workspace/artifacts/matvey-scenarios/E012-person-roi-v1/`; protocol SHA `265d81b9b0109732aefeb5457739f982b57da61db9d5a30f15d28086d2900bca`, closeout/comparison/crop records/20rawRGBNPZ/полные observations. Raw media не коммитить.

Ночные E001–E008: `/workspace/artifacts/night-20261024/`; summaries в `ml/reports/night-20261024.json`, `night-followup-20261024.json`, CSV и figures/figures-followup вне Git. Все rejects сохранены.

## 6. Модели, ABI, checkpoints и настоящие результаты LinQ

### Выбранные baseline, проверенные по файлам при handoff

Все8selected artifact descriptors(2модели×weights/ONNX/TPU/export manifest) существуют, byte counts и SHA совпали с `ml/RELEASE_MANIFEST.json`. Веса не заменялись.

| Артефакт | Путь | SHA256 |
|---|---|---|
|Helmet weights, YOLOv8n DetectionModel nc2 | `/workspace/artifacts/detection/helmet/weights.pt` | `05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c` |
|Helmet ONNX | `/workspace/artifacts/detection/helmet/weights.onnx` | `b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47` |
|Helmet TPU | `/workspace/artifacts/linq-sdk/helmet-compile/model.tpu` | `408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa` |
|Pose weights, YOLOv8n PoseModel | `/workspace/artifacts/detection/pose-split/weights.pt` | `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212` |
|Split-Pose ONNX | `/workspace/artifacts/detection/pose-split/weights.onnx` | `802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00` |
|Split-Pose TPU | `/workspace/artifacts/linq-sdk/pose-split-compile/model.tpu` | `c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b` |

Exact provenance/version/architecture: `ml/MODEL_INVENTORY.md`. Helmet embedded Ultralytics8.0.23, Pose8.0.77; exporter8.4.184 — другая версия. Split-Pose — ABI-variant тех же весов, не новое обучение. Input RGB letterbox640/pad114, /255 float32NCHW[1,3,640,640]; decoded original-image xyxy/COCO17. Decoder conf.25/IoU.45/max300; behavior отдельно person/KP.5. Source ONNX static opset13/IR7. SDK conditioning→calibrate→PTQ→O1/TPU_H1M; базовая smoke calibration1bus, не target-domain qualification.

Helmet outputs `output0`float32[1,6,8400], class0helmet/class1bare_head(sourceHardhat/NO-Hardhat); человек не является классом этой модели. Split-Pose четыре float32 выхода:

- `/model.22/Mul_2_output_0` [1,4,8400], boxes;
- `/model.22/Sigmoid_output_0` [1,1,8400], person confidence;
- `/model.22/Mul_4_output_0` [1,17,2,8400], keypoint XY;
- `/model.22/Sigmoid_1_output_0` [1,17,1,8400], keypoint confidence.

Mixed Pose `/workspace/artifacts/linq-sdk/pose-compile/model.tpu` не предпочтителен: исторический PTQ confidence defect, actual mixed LinQ NOT_RUN. Rejected Pose8calib program SHA `0aed469bd7771348ca39c3a3d429166a74e26cb97154ca655a6491800cb67918`; E001Helmet SHA `ecd5a8853745bc9055b7a2c8eb4ddee43177761b9b6e4a04048a32751b5fae5e`; E005Helmet split SHA `27c1801181a6637c1744a13e45a2713f3afbc36fce517ec6705696a51b8289f6`. Они отвергнуты, не загружать ради формального status0.

### Исторический настоящий LinQ — не повторять как network check

- ResNet50: `/workspace/artifacts/linq-rpc/resnet50-001/{capture.json,inputs.npz,outputs.npz,integrity-review.json,resnet-check.json}`. Реальный успешный автоматический вызов выполнен. Stock name/architecture claim не заменяет происхождение checkpoint; не переисполнять защищённые чужие программы.
- Helmet: `/workspace/artifacts/linq-rpc/helmet-001/`, UUID `262bdaa1-c24b-48ac-b073-6b28fd014248`, matching status0,10.234s,2bare_head. Один additional относительно float, confidence.259503; это smoke, не систематическая target precision.
- Split-Pose: `/workspace/artifacts/linq-rpc/pose-split-001/`, UUID `1f986b07-896d-48b9-8b4f-6ce2d0f8dc16`, status0,11.153s,3people, confidence KP сохранён.
- `/workspace/artifacts/quality/pose/e00-linq-urfall01-2fps/`:11реальных correlated status0, exact input parity с SDK и9matchedperson numerical score/box/KP parity сsimulation; **0events/1miss**.131.018s/.083958FPS, RPCp50=10.630s/p95=18.967s. Device-only time UNKNOWN.
- Старые `.046FPS` — repeated-image control, не real-video accuracy/realtime. Новый E012≈173s — CPU preprocessing/inference/IO, не TPU latency.

### Runtime/формат и состояние подключения

Сохранять единственный `ml/linq/` клиент: официальный pure-Python `tpu_pycloud_format==0.0.1` находится `/workspace/linq-client/tpu_pycloud_format/`; reviewed source manifest `/workspace/artifacts/linq-rpc/format-source.json`. Используются реальные `PyTask`, `serialize`, `deserialize` (`data,metadata,worker`), а не пакет с похожим именем. Credential file **существует** `/workspace/linq-client/connection.env`; содержимое при handoff не читалось и сюда не включено. Наличие файла не доказывает авторизованность текущего процесса.

Known bridge endpoint127.0.0.1:15672 — **AMQP**, не HTTP API. Inference exchange `tpu.direct`, request routing_key `input`; ownreply `matvey_reply_<full canonical UUID>`. Target/response-routing/message-ID headers из официальной библиотеки, body `serialize(PyTask(named_inputs))`. Проверять replyUUID/status_code/expected tensor ABI/finite values. Timeouts конечные; Pika blocking connect/close может превысить polling deadline —60sне гарантированный hard wall-clock cancellation.

Newownremote path только `/auto/cache/<runtime_account>/matvey/`, имена `matvey_...`; program names `matvey_helmet-v1.tpu`, `matvey_pose-split-v1.tpu`. Старые root-cache receipts доказывают исторические байты, не новое размещение. Fresh submissions со старым manifest блокируются; terminal captures можно читать offline. Legacy receive-only допускается только по явно проверенному own UUID, не массовым allowlist.

Bootstrap `/workspace/artifacts/linq-rpc/matvey-bootstrap-v1/`: `matvey_jupyter_upload_bootstrap.zip` (2reviewed helper files), `matvey_upload_bridge.json`, `matvey_start_jupyter_upload.py`. Проверены структура/hash/syntax. **PREPARED, published=false** при handoff. Payload SHA `2b1860be05e98adac98697262545e109d7a03a4703eabfe8197930493e35e2f0`. Подтверждённого ownMatvey staging/namespace-aware live manifest нет; не утверждать удалённое размещение и не переименовывать legacy receipts.

Отдельный неmerged report `agent/linq:docs/linq/QUEUE_CHECK_2026-10-24_112616Z.md` сообщает passive AMQP Connection.Start21/21; авторизованные queue counters/consumers и handlers UNKNOWN из-за недоступных runtime credentials в том процессе. Нового TPU/ResNet test не делал. **Handshake не является TPU proof; root его при handoff не повторял.** Report также фиксирует запрет active probes без согласования нагрузки/владельца и остановок чужих Jupyter kernels.

## 7. Новые результаты двух других оркестраторов: обнаружены при handoff, НЕ интегрированы

Это важное дополнение к старому RESUME: нельзя говорить, что вообще никаких train-ready данных больше нет. Diagnostic registry остался прежним, но появились отдельные training/experimental publications.

### Data Orchestrator

`/workspace/shared/dataset-handoff/READY.json` —5diagnostic releases, file SHA `a64075cade3db2e1befde7e1854084f0b64e0e8fe04b7fa11eaff57eb5ae54cf`, updated2026-10-24T03:52:48Z:

| ID | Версия / manifestSHA | Допустимый scope |
|---|---|---|
|shel5k-sourcebox-diagnostic19 |v1-20261024 /552e821ee6c758d12b10414347c056052bc230c5ab40e5bc2f57633e9c3a8155 |19images/312sourceobjects; parser/geometry/QA, NC restrictions; не training/event/independent test |
|mendeley-factory-replay16 |v1-20261024 /0a51efec6b04dba61bfde9ff24d8f48e418094b0f51789f35f49e5da99458a16 |16videos/3112frames; calibration-known source; replay/manual annotation prep, не event GT |
|edf-native-fall-source3 |v1-20261024 /938eee89db240694263a78e282e836ccd84170dba694e392666884d8a8dec284 |3RGB320×240/12917frames/24sourcepositive windows; complement UNKNOWN, не floorlying/negative GT |
|caviar-running-walking-source3 |v1-20261024 /8141488a97d3cdad6e4d322b85177d6db3d95667858153e027a1b598cb4f9ae7 |Source actor run/walk development/prototyping с unknown masks; sharedcamera/actors, не industrial test; JPEGtime nominal25FPS |
|pped-object-presence48-exif-diagnostic |v1-20261024 /fd06001a76fd9a5f39461472602e604a1ba25b4d2a43134002ade494e617e5c4 |48EXIF-canonical presence/bbox diagnostics; не training/calibration/threshold/test/wearer-state approval и не Helmet/BareHead task |

Полные releases: `/workspace/datasets/research/releases/<id>/<version>/`. ML-owned frozen snapshot: `/workspace/shared/dataset-handoff/ml-baseline-night-v1/READY.json` (52Helmet/8calib/20UR), SHA `5f30081065e69e9316e96b972353267caaae868212194b312ddc8ceae065f74b`. Consumer `/workspace/shared/dataset-handoff/ML_REQUIREMENTS.json`, протокол `ml/DATA_HANDOFF_PROTOCOL.md`.

**Новое:** `/workspace/shared/dataset-handoff/READY_FOR_TRAIN.json` и immutable `/workspace/shared/dataset-handoff/data-release-20261024/READY.json`, оба SHA `d6b3cf6959b59de4f3daf8d14455ccf7c1d22986e7d1e40a2f08181e37db20ae`. Schema **`mosprom-training-datasets-v1`**, не старый diagnostic handoff schema. Не передавать его в consumer с неподдерживаемой схемой с последующим обходом ошибки.

- Dataset `mosprom-gmd-video-weakclip/v1-20261024`, `/workspace/datasets/research/releases/mosprom-gmd-video-weakclip/v1-20261024/`.
- READY_FOR_TRAIN только для **VIDEO_WEAK_LABEL_CLASSIFICATION**:123train(61ADL/62Fall),37val(20ADL/17Fall). Test EMPTY_BLOCKED_NO_INDEPENDENT_TEST.
- Source author categories160videos,79Fall/81ADL; **new HUMAN_VERIFIED=0**, нет frame/event/bboxGT. `forbid_frame_label_broadcast=true`, `bbox_training_supported=false`.
- Subjects1+2+3train/4val, всё video и derivatives вместе; physical person/camera independence UNKNOWN; val уже смотрели. Это не новый untouched test. Source ADL не означает отсутствие всех восьми нарушений.
- Manifest SHA `2b17335c33ffd128c54344cf0a10e0ae69d8e19afe7042b4b2983ff9bb8e03ef`.
- При handoff проверены SHA manifest/train/val/class_map/VALIDATION metadata. Все video/media заново не аудировались.
- `do_not_retrain_existing_four_heads=true`. Intended new training: RGB/temporal-MIL video adaptation, не bbox detector training. Не повторять завершённые four-head experiments автоматически.

Ещё один опубликованный пакет: `/workspace/shared/dataset-handoff/data-extension-20261024/EXPERIMENTAL_HANDOFF.v2.json`, SHA `982036c31df6e43feff12f43b9a65ad3ffaee0d71bd0ece61a81696573131185`, **EXPERIMENTAL_REVIEW_ONLY/no_automatic_integration**, metadata commit036e06d2. Index/cards включают KTH/GMD source heads и E33negative transfer.

E33 по producer-report: DIRECT_CCTV_USE_REJECTED,99source windows(91walking/8running), observable1at640 и11at1280; observable walking классифицированы running, все8running UNKNOWN, supportedF1/accuracy0. **Source bbox ORACLE association**, не autonomous industrial test; не переносить хороший KTH source-score в утверждение о CCTV. Root не повторял оценку. Ссылки: `/workspace/datasets/research/experiments/night-20261024-extension/caviar-transfer-v1/{MANIFEST.json,evaluation-n640-v1/SOURCE_TRANSFER.json,evaluation-n1280-v1/SOURCE_TRANSFER.json}`.

### Training Orchestrator

Потребности восьми сценариев уже отправлены consumer-owned pointer `/workspace/shared/training-handoff/ML_REQUESTS.json` → immutable `matvey_requests_v2.json`, SHA `e241ea010224fca34612d7d7b0b6c689dd63022c009773cc3c4eabfbe3ea3568`. **REQUEST_ONLY_NO_AUTOSTART**, приоритет07/02/01. Источники в репозитории `ml/scenarios/TRAINING_REQUIREMENTS.json`, `TRAINING_ADDENDUM.json` (особенно harness USE и fact binding). Это не GPU lease и не команда начать обучение.

Ранее известный экспорт: `/workspace/artifacts/training/matvey_training_20261024/{matvey_training_handoff.json,matvey_training_handoff_final.json}`. Final handoff SHA `302387a0ceacca54c4056ecf847cbad697b7799ae253129c3858877fcf5829d4`.4fold-specific TCN/MLP candidates, static `pose_window`float32[1,24,74] →`fall_logit`float32[1,1], opset13/IR7. SHA/ABI/источники в `ml/MODEL_INVENTORY.md`, export report `matvey_gmd_window_export_v2/matvey_export_report.json` SHA `3e813883813b363169dc17aaefd12c739e89c5268ec7e8895cf7a51514d0fb8a`. Float parity только на cached features, не end-to-end live video. Четыре outer-fold head нельзя автоматически превратить в одну production model или выбрать по outer-test. Compile/PTQ/actualLinQ NOT_RUN; physical feature74 order/masks/sampling необходимы.

**Более новый результат, ещё не включён в root model inventory/release:**

- `/workspace/artifacts/training/matvey_yolo_pilot_20261024/matvey_training_result_handoff.json`, SHA `10992b4d22c5218569132729de1864726d8cc446f3441338cfdc1c00541c3a65`, status **COMPLETED_TRAINED_CANDIDATE_REJECTED**, source training commit `a92343cd` (worktree HEAD при handoff0832ef99).
- Folder name `yolo_pilot` **не доказывает YOLO architecture**. Проверенный config указывает **MLP, CPU, AdamW, lr.0001, seed20261024**, max epochs30; фактически6epochs/best_epoch1/0.3066s, GPUfalse. Это fine-tune существующего GMD temporal head по cached pose features, не trained machinery/phone detector.
- `/workspace/artifacts/training/matvey_yolo_pilot_20261024/matvey_gmd_finetune_v1/matvey_result.json`, SHA `1f9048e1ddaac36fa59066ae87df47d613794e77a51c5905d259e332a5cdcf30`.
- На тех же37weak-val videos baseline=candidate macroF1 **.72953216374269**, gain0; Fall P.666667/R.823529/F1.736842. Confusion ADL[13,7],Fall[3,14]. Это **video-level source classification**, НЕ event-level Fall/F1 промышленного pipeline. Deployment_allowed=false; independent_event_quality NOT_EVALUATED; export/LinQfalse. Не сравнивать с UR event F1.1818 как один endpoint.
- Best checkpoint `.../matvey_gmd_finetune_v1/matvey_best.pt`, SHA `5726466aa2ae251c54a85f0341f471ed79e966e7702c56346f6b1069c21931a0`; last `matvey_last.pt`, SHA `9e6ff92882a16a148906d45e0ceada18932b84345721a47ce7a0549417d8ffd5`.
- Baseline kept `/workspace/datasets/research/experiments/night-20261024-extension/gmd/models-v1/outer-4/selected.pt`, SHA `959a963724997f4838a4b66caa8b85d2be41097df334d99014bf38eb8d340ace`.
- Эти4descriptors(result,best,last,baseline) проверены по byte counts/SHA при handoff. Не запускать повторное обучение. Никакой automatic promotion.
- Coordination `/workspace/shared/dataset-handoff/matvey_training_gpu_request.json`: **WITHDRAWN_NO_GPU_JOB_STARTED**, allocation_received=false, activeGPU0, новыхLinQ0, no_automatic_next_cycle=true. Нельзя считать имя GPU-request разрешением занять4090.

Новый агент должен сначала оформить metadata intake этих публикаций, прежде чем говорить «данных нет» или «модель готова». В этой handoff-задаче чужие ветки не мержились, root release/models не менялись.

## 8. Процессы, журналы и работа в процессе

На снимке подготовки native agents `/root/detection`, `/root/behavior`, `/root/linq` имеют status **completed**, не активные ML workers. Собственных незавершённых training/inference/compile команд не найдено при sanitised `/proc`-проверке; `nvidia-smi --query-compute-apps=pid,process_name,used_memory` вернул0строк. Это моментальный снимок, не гарантия занятости всей команды в будущем и не информация о загрузке удалённого LinQ.

Проверены только собственные local RPC roots:

| Root | request.json COMPLETED | Другие активные/неопределённые |
|---|---:|---|
| `/workspace/artifacts/linq-rpc/` |4|нет в найденных metadata|
| `/workspace/artifacts/video-mvp/` |18|нет|
| `/workspace/artifacts/quality/pose/e00-linq-urfall01-2fps/` |11|нет|
| `/workspace/artifacts/matvey-scenarios/` |0|нетRPCjournals|

Default `/workspace/artifacts/linq-rpc/matvey-admission/active.json` отсутствует (директория не создана новыми root remote tasks). Это **не разрешает** чистить чужие очереди или считать LinQ свободным. Если новая metadata UNKNOWN/SUBMITTING/ACCEPTED появилась — остановить только свою новую отправку, reconcile прежний UUID receive-only. Не сбрасывать journal ради повторения.

Сохранены работающие infrastructure processes, snapshot PID/comm без аргументов/секретов: Jupyter PID435(`jupyter-noteboo`) и124121(`jupyter-lab`), supervisord614, Caddy943, sshd380, ssh22199 и другие SSH-сессии. Назначение конкретного SSH22199 отдельно не проверялось; не утверждать по имени процесса, что это наш tunnel. **Ничего из этого не останавливать/не перезапускать.** Собственных ML PID для продолжения нет. PID снимка могут измениться.

Полные argv/env не записывались: там могут быть credentials. Runtime credential file существует, но его значения и применимость к любому конкретному процессу здесь UNKNOWN. Старые успешные network reports не доказывают нынешний авторизованный inference.

## 9. Критические решения и ограничения

1. **Общая инфраструктура капитана:** не менять OpenVPN, SSH, NetworkManager, routes, firewall, systemd/services; не останавливать ноутбук/туннель/Jupyter kernels. При сбое сохранить own-state и перейти к local independent work. Пассивный broker handshake не доказывает TPU fault/успех.
2. **Общий LinQ account:** не трогать `baseline/`, `mosprom_*_cut_ap9999*.tpu`, чужие файлы/queues. Новые ownremote только `matvey/`, имена `matvey_`. Не read/purge/redeclare/delete foreign queues. OMP/OpenCV/ORT1–2threads в собственном Jupyter kernel. Max1ownactiveTPUrequest по умолчанию.
3. **Durability:** unique canonical requestUUID, correlated reply, finite timeout, fsynced intent/arrays before ACK, global own-request admission across journals. UNKNOWN нельзя автоматически повторять. Одного AMQP tunnel недостаточно для filesystem upload; нужен отдельный разрешённый Jupyter channel/receipt.
4. **One state writer:** lock до restore checkpoints; event/candidate/behavior/suite/video одной SQLtransaction. Duplicate frame с иным semantic input отклоняется. Candidate UUID/revision стабильны на retry; gap не safe evidence.
5. **Observability:** object presence≠use; отсутствие annotation≠absence; человек на фоне выше≠work at height; harness present≠in_use; horizontal pose≠lying on floor; image motion≠running/metric speed; haze≠smoking/fire; linecrossing≠climbing. Medical diagnosis запрещён.
6. **Input binding:** exact camera/epoch/frame/PTS/media hash для real facts; conflicts/duplicates/stale rejected. Duplicate explicit object keys quarantined. Site policy требует camera_id/image_size/provenance. Sequential frame ordinal+encodedPTS+SHA вместо unchecked seek/CV-relativetime.
7. **ML qualification:** BASELINE/EVALUATED/IMPROVED/LINQ_VERIFIED/FROZEN могут сочетаться, но software PASS/compile PASS/export parity не accuracy. Нужны SAMEfixedvalidation и untouched finaltest; не выбирать пороги/architecture по test. В coverage480 — software count. Старый baseline не заменять candidate без полного gate.
8. **Compute:**4090 общий с Training Orchestrator, один согласованный heavy GPU job и advisory `/workspace/artifacts/quality/gpu.lock`. Не считать lock-файл аппаратным scheduler; согласовать фактическую allocation. Data — source CPU audit, не sharedLinQ. E012 CPU2 не мешал Training GPU.
9. **Git/data:** только matvey_cv; только свои worktree; no reset/rebase/forcepush/main/captain merge. Датасеты, media, source GT/predictions, checkpoints/ONNX/TPU, notebooks с runtime и секреты не Git. Использовать immutable handoff scope/hash; data_ready_for_annotation не training approval.
10. **Frozen scope:** технический eight-rule release готов, quality release открыт. Не создавать бесконечную цепочку улучшений; фиксировать null/NOT_MEASURABLE, rejects, bad trials. E012 и завершённые ResNet/UR01/H-FALL/H-HELMET не повторять без новой информации/задачи.

## 10. Блокеры и точные следующие действия

Порядок для новой сессии, после нового разрешения продолжать разработку:

1. Прочитать раздел11, проверить branch/status/HEAD и новые published handoffs. Не переписывать pipeline и не перечитывать весь research archive. Сохранить новые incoming statuses из раздел7 в ML registers **отдельным intake commit**; не мержить Data/Training ветки и не выбирать outer-fold по test. `READY_FOR_TRAIN` только weak-video; многие старые blanket-фразы «нет train-ready» теперь требуют scope-уточнения.
2. Согласовать с Data+Training конкретную выполнимую цель **07/02/01** до позднего24октября.07: independent episode/floor/hardnegative GT и корректный feature74 adapter;02: human-reviewed person/vehicle/movement/danger-policy;01: upstream person/gait observations, не очередное повышение confidence. Для03/04/05/06/08 запросы уже точные, ждать qualified inputs, не маскировать missing detector вручную заданным POSITIVE.
3. Принять/reject Training results по manifests/label unit/lineage/split/metrics. НовыйCPUfine-tune уже reject сgain0 — не повторять. E33 отрицательный transfer не обходить увеличением разрешения без новой гипотезы. Не применять weak ADL/Fall video labels как bbox/frame/onset GT. Independent industrial finaltest всё ещё отсутствует.
4. Для настоящего liveLinQ сначала подтвердить допустимое окно с капитаном/владельцем общего аккаунта. Не делать extraResNet/network-recovery test. Проверить собственную durable metadata; использовать только разрешённую runtime config без вывода значений.
5. Подготовленный **own** Matvey bootstrap в отдельном notebook/kernel, авторизованный upload, matchingSHA receipt и reviewed namespace-aware runtime manifest. Старый root-cache manifest не переименовывать в «новый proof». Затем один limited own model task по существующему client, реальный statusUUID/tensors/capture review; max1active. Текущая удалённая availability/handlers UNKNOWN, нельзя заранее назвать этот шаг выполненным.
6. Только qualified neural candidate: exact preprocessing→ONNX/compile/PTQ→numeric/ABI/decoder→реальный LinQ→fixed independent evaluation; preserve rollback. Если права/данные/SDK/network блокируют — записать blocker, не изобретать числа и не вмешиваться в капитана.
7. До handoff команде зафиксировать именно заявляемый scope: eight runnable prototypes vs subset reliable real-video/LinQ recognizers. События новых типов требуют согласованного отдельного backend mapping; это не текущая задача переписывания backend/frontend. Матвей отвечает за ML контракты/примеры/инструкции.
8. External preservation: нужен явно разрешённый off-Vast destination/account и checksum verification. Сейчас external backup/remoteGit не подтверждены. Не выбирать чужой cloud account автоматически. После stable cutoff — только critical fixes, не новый широкий search/training цикл.

Неизвестные/открытые факты: target industrial independent test, person/camera identity independence части source datasets, qualified specialist weights, site safety rules/geometry, медицинское состояние, live LinQ handler/queue consumers, actual TPU firmware/device-only timing, Mark's real service integration, external backup/remote SHA.

## 11. Как проверить после передачи и что читать первым

Читайте в этом порядке:

1. Этот handoff и `/workspace/project/AGENTS.md` — роли/изоляция/инфраструктура.
2. Верх `RESUME.md`, `ml/SCENARIO_COVERAGE.md`, `docs/SCENARIO_RUNBOOK.md`.
3. `docs/SCENARIO_RUNTIME_CONTRACT.md`, `ml/scenarios/catalog.json`, candidate schema и2examples; не менять внешнийeventv1.
4. `ml/MODEL_INVENTORY.md`, `ml/RELEASE_MANIFEST.json`, `ml/reports/scenario-coverage-20261024.json`.
5. `ml/EVAL_REPORT.md`, `ml/EVAL_PROTOCOL.md`, `ml/ERROR_ANALYSIS.md`, `ml/EXPERIMENTS.csv`, актуальный верх `ml/PROGRESS.md`.
6. **Отдельно новые** Data/Training pointers из раздел7, `ml/DATA_HANDOFF_PROTOCOL.md`, Training requirements/addendum. Они могут быть свежее root RESUME.
7. Только при подготовке допустимого realLinQ — верх `docs/JUPYTER_RUNBOOK.md`, `ml/linq/`, `docs/LINQ.md`; нижние старые инструкции/root-cache paths исторические.
8. Официальный `/workspace/case/КЕЙС_LinQ.pdf`, page4; при уточнении требований не подменять source старым `Deep-Research`. `INDEX.md` — маршрутизатор исследований, не доказательство реализации. Playbook `/workspace/ML_24H_PLAYBOOK.md`, если нужен scope, не запускать всё заново.

Безопасные проверки (ничего из этого не делает новый TPU/GPU inference):

```bash
cd /workspace/project
git branch --show-current
git status --short
git log -1 --format=%H
/workspace/.venvs/linq-client/bin/python -m unittest discover -s tests -q
```

Для неизменного code checkpoint ожидается480testsPASS. Новый run — в новой сессии после проверки branch; этот handoff не выдаёт прочтение старого лога за повторный запуск.

```bash
/workspace/.venvs/linq-client/bin/python -m ml.quality.release_review \
  --output /workspace/artifacts/handoff-20261024/NEW-integrity-review.json \
  --integrity-only
```

Ожидание: integrityPASS и **quality_release=NOT_QUALIFIED** одновременно. Без --integrity-only exit2 обозначает незакрытый independent-quality gate, не порчу весов. Output должен быть новый, старые review не перезаписываются.

```bash
/workspace/.venvs/linq-client/bin/python -m ml.scenarios.cli \
  --state-dir /workspace/artifacts/handoff-20261024/NEW-synthetic-acceptance \
  --synthetic-all --synthetic-evidence
```

Ожидание24synthetic-onlycasesPASS; не real-video accuracy. При необходимости проверенный real-source replay **без нового NN/LinQ**:

```bash
/workspace/.venvs/linq-client/bin/python -m ml.scenarios.cli \
  --state-dir /workspace/artifacts/handoff-20261024/NEW-fall06-replay \
  --config configs/scenarios/suite.example.json \
  --input /workspace/artifacts/matvey-scenarios/ur07-video-evidence-v1/fall-06-cam0/inputs.observations.jsonl \
  --source-video /workspace/datasets/quality/temporal/processed/urfall/fall-06-cam0-rgb.mp4
```

Ожидание1native-provenancecandidate07 и ready evidence frame75/2500ms, no newremote calls. Не запускать «живую» команду с legacy namespace. Full live template в SCENARIO_RUNBOOK **заблокирован prerequisite stage**, не инструкция автоматически отправлять на общий аккаунт.

Проверенные интерпретаторы/компоненты существуют:

- `/workspace/.venvs/linq-client/bin/python`: transport/replay/tests, NumPy/OpenCV/jsonschema, без необходимости Torch.
- `/workspace/.venvs/linq-sdk/bin/python`: supplied compiler/PTQ SDK, отдельно от основного PyTorch.
- `/venv/main/bin/python`: основной Torch/Ultralytics/CUDA; не переустанавливать и не трогать drivers ради mismatch.
- `/usr/bin/ffprobe`: encoded timestamp clock. Нет тихого fallback к estimatedtime.

## 12. Зависимости, артефакты и сохранение для продолжения

**От Data Orchestrator** (`/workspace/agents/data-audit`, только его branch): нужны immutable manifests со scope/rights/split/coverage/actor/time/unknown; независимые hardnegatives и industrial groups; reviewed machine/action/zone/harness-use/phone/cargo labels. Получать через shared manifests, проверять SHA/label-unit до pixel/model work. Текущий weak-video READY_FOR_TRAIN не решает bbox/action/onset gaps всех восьми. Не править его исходные annotations/data, не передавать model-driven selected cases как finaltest.

**От Training Orchestrator** (`/workspace/agents/training`, только его branch): qualified checkpoint+modelcard/classes/feature plan/source commit/seed/config/val metrics/export/compile/PTQ/LinQ gates. Coordinate exclusive4090/GPUlock. Сейчас CPUfine-tune reject,4heads export-only, новых accepted specialist detectors нет. Requests уже опубликованы, root не стартует jobs за него. Не принимать слова «YOLO pilot», «exportPASS», «sourceCVhighF1» за production qualification.

**От root/пользователя и владельца LinQ:** явная ownMatvey file placement+receipt, доступное согласованное execution window/runtimeauth, проверка полной model pipeline. AMQP tunnel не filesystem mount; не менять Arch/VPN/systemd с Vast. Backend/frontend остаются у Марка/Егора; externalEventCandidate mapping пока не внедрён.

Быстрый указатель к большим артефактам вне Git:

| Назначение | Путь |
|---|---|
|Исходные модели/exports | `/workspace/artifacts/detection/{helmet,pose,pose-split}/` |
|SDK compile programs/reports | `/workspace/artifacts/linq-sdk/{helmet,pose,pose-split}-compile/` |
|Actual service captures | `/workspace/artifacts/linq-rpc/{resnet50-001,helmet-001,pose-split-001}/` |
|Legacy video/journals | `/workspace/artifacts/video-mvp/{industrial-001,industrial-002,repeated-image-control-001}/` |
|Old MLquality | `/workspace/artifacts/quality/{helmet,pose}/` |
|Night experiments E001–E008 | `/workspace/artifacts/night-20261024/` |
|Eight-scenario acceptance/replay/screen/E012 | `/workspace/artifacts/matvey-scenarios/` |
|Producer immutable datasets | `/workspace/datasets/research/releases/` |
|Original reviewed Helmet/UR | `/workspace/datasets/quality/` |
|NewTraining models/metadata | `/workspace/artifacts/training/` и producer-described experiment paths, не foreign worktree edits |
|Shared pointers | `/workspace/shared/dataset-handoff/`, `/workspace/shared/training-handoff/` |

Локальный model-only snapshot19files: `/workspace/artifacts/night-20261024/preservation/matvey_models_night_20261024.tar.gz`,81,683,583bytes,SHA `41bdddf35b647c76d04c2994187c529bf8285f2847ca9ecb91f043a418484601`. Старый24member архив `/workspace/artifacts/quality/release/mosprom-ml-models-quality-checkpoint-20261024.tar.gz`,SHA `e30f1034b79b6d1610c047b131693c58f15fc667c42ed4fe7c26741c45292445` сохранён. Это **не off-Vast backup**; новые GMD/unselectedCPUcheckpoints в этих старых tar не включены. Не удалять originals/rejects/rawmedia. Отсутствие approved external destination — открытый blocker.

Во время этой передачи проверены branch/HEAD/status, current published pointers и ограниченные metadata SHA, selected model artifacts, существующий480testlog, наличие ключевых файлов, local request states и sanitized process snapshot. Новые обучения/инференс/сетевые probes не выполнялись. Нет секретов, токенов или private keys в этом документе. Следующее действие — получить новую задачу и продолжить с фактов выше, не с начала проекта.
