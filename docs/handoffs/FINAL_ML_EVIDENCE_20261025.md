# MOSPROM-2026 — финальный ML-пакет

Фактический итог этой итерации:12полных сохранённых localCUDA сцен,2830исходных кадров,8490model calls суммарно (6180новых/2060кадров). Никаких пропусков или протягивания детекций в full local наборе.8originalMP4 без изменения байтов;4предсуществующих derivative MP4 обозначены playback, не nativeoriginal.

**Настоящий Argus local integration PASS:** original3_tr45 → штатный LocalBackend/ONNX CPU → JSONL → неизменённые trackers/rules → episode1 → evidenceJPEG1 → конечный event1 в изолированной SQLite → GET event API200.38/75кадров на каждую из3моделей,114новых CPU ONNX calls,15.855с job wall-clock.37кадров пропущены по штатному step2, без интерполяции; точные списки/PTS в integration/local_argus_cpu/artifacts.json. Событие proximity подтверждено наPTS2800мс, metric distance1.10096bodyheights, **не метры и не GT**. UI-визуальный тест не выполнен, публичный сервер не поднимался. Выбран отдельный CPU annotated.mp4 из actual job outputs. GPU-replay этого же видео имеет confirm2760мс и хранится отдельно.

**Настоящие LinQ outputs сохранены:**15исторических correlated status0 model calls на13уникальных source frames. UR01 Pose11/160, industrial4_tr6 Pose+Helmet наframes0/13 из522. Numeric inputs/outputs,UUID,status,ABI,hashes и Argus tails проверены.15tail replays побитово совпали. На industrial Helmet оба decoded списка пустые; не выдавать это за positive PPE detection quality. Между TPU observations в TPU-видео нет переноса рамок.

**Saved TPU→Argus replay PASS, live end-to-end BLOCKED:** сырые response.npz → настоящий проверенный ONNX tail → неизменённый tools/linq/yolo_io.postprocess → FrameDetections/read_jsonl → analyze/rules. UR01 использует11savedTPUPose+same-frame GPUCOCO; industrial2savedPose/Helmet+same-frame GPUCOCO. Это MIXED replay,0новых TPU/CNN calls и0episodes, без app DB injection. Файлы integration/saved_tpu_replays. Нового live TPU request не было: собственные staging receipts отсутствуют, Jupyter auth/channel capability не предоставлена. Availability самого TPU UNKNOWN, не заявляем поломку сети. Общая сеть/службы/чужие очереди и программы не менялись.

Исторические call wallclock incl transport: min9.424с, median10.630с, max22.685с;15calls сумма173.312с. Device-only time и delivered-alert latency NOT_MEASURED; не realtime. Видео продолжает идти с исходным PTS, export/render time не является временем TPU.

## Покрытие и качество

|Сценарий|Программный статус текущего Argus|Качество целевого события|
|---|---|---|
|S01 бег|RUNNABLE/PROTOTYPE; полные CAVIAR run/walk,0events|NOT_MEASURED independent; person localization2/168COCO,0/168Pose running actor frames|
|S02 сближение|RUNNABLE/PROTOTYPE;1actual local event+evidence/API|NOT_MEASURED: нет distance/policy GT|
|S03 телефон|RUNNABLE/PROTOTYPE; COCO67 и штатный rule|NOT_MEASURED, телефон/ownership/negativeGT не установлены|
|S04 курение/огонь|BLOCKED: specialistclasses/model_missing|NOT_MEASURED; дымка в видео не specialist inference|
|S05 перелезание/под грузом|PROTOTYPE/BLOCKED: зоны, climbing semantics, suspended_load model отсутствуют|NOT_MEASURED|
|S06 высота/привязь|BLOCKED: no_harness+height policy отсутствуют|NOT_MEASURED|
|S07 падение/лежание|RUNNABLE/PROTOTYPE, current Argus0selected episodes|NOT_MEASURED independent; исторический другой consumer имеет diagnostic1/10recall|
|S08 переноска|BLOCKED: load_carrying skeleton, cargo/policy model нет|NOT_MEASURED|

Полная цепочка/сигналы/зависимости каждой строки: SCENARIO_COVERAGE.json. Detector и event metrics разделены. Текущие независимые GT/TP/FP/FN/P/R/F1/FP-hour/delay — NOT_MEASURED; нулевые predicted episodes не являются истинными negatives. safewatch eval не запускался на weak/partial GT: он не поддерживает unknown masks/actor ownership/bounded-onset GT. Нельзя выдавать отсутствующие expected за полностью безопасное видео.

Новые source-scoped detector metrics SOURCE_SCOPED_DETECTOR_METRICS.json: CAVIAR source boxes/actors, весь lossy playback, unique IoU≥.5. COCO walking87/743 и51/662, running2/168; Pose walking27/743 и59/662, running0/168. Это person localization recall, **не running classifier recall**, не precision/independent benchmark. Неаннотированные области UNKNOWN.

Исторические development metrics в metrics/: Helmet FP32 helmetTP19FP11FN6/F1.6909, bare_head→no_helmetTP23FP7FN9/F1.7419;52images,44complete/class,pretraining overlap. Старый ML BehaviorEngine Fall2FPS TP1FP0FN9/F1.1818; Running source prototype TP0FP0FN3/F1=0. Они не пересчитаны текущим Argus, не включены в independent industrial table и не доказывают качество нового full-video пути. Порог .25, разные consumers/cadences явно сохранены.

Три лучших **доступных** демо: S02 application event, S07pose/fall+confuser, PPEfull model proposals. Обоснование и недостающие positive/negative pairs — DEMO_SELECTION.md. Это не3quality-qualified violations. S01debug не выбран из-за низкого upstream recall. New specialist models/long research/training/compile не запускались.

## Проверки и ограничения передачи

527softwaretestsOK(4skipped) после integration/packaging additions; финальный лог matvey_tests_v3.log (точное время в логе). Independent audit5newscenes/2060RGB+PTS/6180inputbindingsPASS; прошлые7/770audit сохранены.12full visuals+2historicalTPU visuals проверены по всем originalframe/RGB/encodedPTS; presentation normalized to0,1msquantization, полный originalPTS сохранён в JSON/HUD. All source MP4 bytes unchanged.

Марк owns Argus rules/app/backend, Егор получает видео. Код приложения/main/чужие worktrees не менялись. Лишь отдельная копия main использовалась для конфигурации actual local test. Версии моделей/классы/минимальное подключение — MODEL_REGISTRY_HANDOFF.md. Веса/бинарники/видео внеGit. Сохранённый ZIP — локальная передача, не проверенный off-Vast backup; разрешённый внешний destination не предоставлен. Права и исходные notices не расширены до публичного распространения.
