# RAW_FACTS — cv_accuracy_vast

Сборка после двух волн, **2026-10-23, Europe/Moscow**. Основание — 16 самостоятельных W1, независимый критик K001–K011, 7 целевых W2, локальные исходные поручения и визуальные наблюдения root по кейсу. Нового интернета, третьей волны, аренды, обучения, экспорта, model benchmark или LinQ run сборщик не выполнял. Все E ниже **PROPOSED / UNRUN**. Даты/версии unknown не подменяются датой доступа. Источники — [SOURCES.md](SOURCES.md); обратный индекс — [_WORK/ID_MAP.md](_WORK/ID_MAP.md); оставшиеся gates — [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

## F001 — Что действительно требует кейс

**Основание:** S001, pp5/7/8/9/13/15/18/19; тип — переданное прямое визуальное наблюдение root, не собственное повторное чтение сборщика. **Проверка:** root просмотрел все 20 raster pages, p5/7/13 отдельно; PDF hash указан в S001. **Наблюдение:** важны быстрое и надёжное сообщение об инциденте, баланс precision/recall, один продолжающийся инцидент→одно сообщение, обязательные neural inference на LinQ и замер скорости. Допускается приоритизация сценариев с расширяемостью. Финальная сдача 25.10.2026 10:00 MSK; checkpoint 24.10 11:00/18:00. В кейсе не установлена численная формула accuracy, точный SDK/SKU/операторы/память или достаточный выданный labeled dataset. Сценарное «несколько секунд» не разрешает подавлять все короткие критические события. CPU neural ban как буквальная формула кейса не обнаружен; допустимость конкретного fallback требует ответа владельца кейса.

## F002 — Раздельная provenance и фактически выполненная работа

**Основание:** S002/S003, RUN_STATE и preambles W1/W2. **Тип:** процессное наблюдение/поручение. Исходный договор описывал до публикации кейса; тематическое поручение актуальнее: первый checkpoint уже прошёл. «Хоть 1 FPS, главное точность» и предпочтение file-on-server CPU+TPU — пересказ команды, не официальный numerical objective и не hardware inventory. RTX4070 существует по контексту, её VRAM/OS/driver unknown. План 1–2 RTX3090 24GB не является арендой. Реально получены документы/код/metadata, timestamped public offer JSON, малый URFD CSV и release CLI wheel; ничего из model train/export/benchmark/LinQ не выполнено. Соседние отчёты служили leads, их отдельные тесты не перенесены сюда как выполненные. High-сборщик читает сохранённое, не добавляет сеть. Предел: даже source-backed manifest не installed lock.

## F003 — Принятый один маршрут A→условный B→необязательный C (закрытие K011)

**Основание:** S001/S002; F173/F04/F08, F153, F100/F03, F135/F06; **тип:** интеграционное решение сборщика, не эксперимент. **Default A:** один pretrained frontend, причинная CPU FSM/правила/пороги, без нового обучения. Первый научно честный scope — наблюдаемое лежачее состояние в фиксированном ракурсе, одно уведомление на продолжающийся эпизод. URFD exact pair допускается только после принятия NC/use условий и проверки содержимого. Это не готовый обучающий пакет и не доказанная модель lying/fall. Если пригодного/разрешённого lying frontend/media нет, единственный fallback scope — person в пользовательском полигоне на разрешённом team video после получения такого видео; без него остаётся только synthetic logic feasibility. Полигон не доказывает физическую опасность.

**A gates:** права+asset/time/labels → synthetic ledger acceptance → oracle real replay → pretrained causal replay → floating export/parity → выданный LinQ serial sample и конкретный graph → полная latency/уведомления → freeze. Он может закончиться демонстрацией исполнимости без training и без industrial quality claim. Не подменять unknown сознанием/падением/неподвижностью. **B:** только при human-confirmed frontend error, exhaustive TRAIN labels, независимом DEV, принятых weights/use и train/export/runtime gates — **один fine-tune одной baseline recipe**, затем повтор full-bundle проверки. **C:** только после работающего A/B, готовой обусловленной ошибкой работы и измеренного запаса — **один** challenger либо одна полезная пара independent jobs/вторая GPU. Нельзя сложить spatial+augmentation+pose+verifier+ensemble+DDP в обязательную очередь. Для первого C при localization error условный D-FINE-M COCO HF exact asset; не добавлять одновременно O365 variant/RF-DETR.

Предарендные gates документальные, data и доступные CPU/local export checks. **Fit на конкретной3090 измеряется только после отдельного разрешения расходов на первую оплачиваемую qualification**, до heavy training; отсутствие уже арендованной3090 не превращает fit в предарендный prerequisite. Ни этот документ, ни public offers не разрешают тратить деньги. Минимум сохранности — native pre-strip snapshot, immutable внешняя копия, bytes/hash/trusted load receipt и lineage. Exact replay/controller/ASHA/KD/neural temporal deferred.

## F004 — Один data-role contract и статус после просмотра (закрытие K006)

**Основание:** F176/F06, W1-09 protocol и W1-11 selection; **тип:** выбранный интеграционный протокол. Split unit — исходный incident/session/camera/site по заявлению переносимости, со всеми производными crops/frames/augmentations/phase variants. Синхронные камеры одного инцидента не независимы. **Обязательный минимум только TRAIN / DEV / LOCKBOX.** На нынешней URFD паре TRAIN пуст, оба клипа только DEV, independent LOCKBOX отсутствует. Feasibility не ждёт искусственной квоты независимых событий, но не становится подтверждением качества. На малом числе групп допустима grouped cross-validation внутри development с полным повторением fit/calibration/selection по folds; это оценка development procedure, не новый independent lockbox. Нельзя делить соседние кадры ради численности.

| Решение | Разрешённые данные | Число/ограничение | После просмотра |
|---|---|---|---|
| Семантика, error audit, пороги, dwell/gap/unknown/rearm, size/crop, checkpoint/model choice | DEV | Один incumbent + одна заранее обоснованная альтернатива; views/trials в ledger | Development/exploratory; не confirmation |
| Gradient fine-tune | TRAIN; checkpoint/stop по DEV | Один B после gates | TRAIN не становится независимым; trial mutation даёт новый ID |
| Calibration | DEV; optional grouped CAL внутри development только при достаточных группах | В A не требуется | Fitted/fold selection data не независимый CHECK |
| Отбор готового целого pipeline | Optional frozen SELECT при реально лишних независимых группах | Не более двух заранее frozen bundles; без knob tuning | Selection evidence; не independent final confirmation. Любой новый threshold/router/rule превращает SELECT в DEV |
| Итоговая независимая оценка | До этого не открытый LOCKBOX после freeze exact bundle | Одна planned evaluation | Ошибка остаётся ошибкой этой версии. Любое исправление по нему поглощает набор в DEV; новый independent claim требует новых групп |
| Refit TRAIN+DEV | Только отдельное осознанное решение после отбора | Не назначен в текущем маршруте | Новый checkpoint/bundle identity и UNVERIFIED статус; прежняя оценка другого artifact не переносится автоматически |

CAL/TUNE/CHECK/SELECT не складываются в семь микровыборок. Camera overrides только по отдельным разрешённым development sessions; unseen camera получает общий fallback и неподтверждённую переносимость. Annotation fixes, экспорт/decoder/quantization debugging тоже development, даже без градиентов. При нехватке independent positives/continuous background честный выход — DEV feasibility с сырыми counts и N/A там, где знаменателя нет.

## F005 — Retained detector и что означает его benchmark

**Основание:** W1-02 источники/таблицы; S240–S06/S09–S14; **тип:** published/source/asset metadata плюс условная рекомендация. **Baseline:** Ultralytics8.4.184 source `de290d865035acbfa4bb24cc88960d8b52c26e45`, `yolo26s.pt` release v8.4.0, metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b`, 20,422,725 bytes; byte download/load UNRUN. Авторская lineage — O365v1 pretrain150 epochs→COCO S70, batch128/640/MuSGD, не COCO-only binary inspection. Published COCO AP48.6 dense/47.8 e2e, dense APsmall29.5, 9.5M fused. Нельзя соединить dense AP с e2e latency или считать APsmall visibility/target PPE metric.

**Conditional C:** D-FINE-M code `956d1709314c2c6a4df6f34de232054578a7449f`, HGNetv2-B2,4 decoder layers; точный выбранный источник HF `Peterande/D-FINE@19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth`, 79,108,938 bytes, LFS SHA256 `b44a7586bf490858c7b8bce9e44bd025cb88724df9a07a8deb3ae1c12e608195`. Actual byte hash unknown. Published AP52.3/APsmall33.2 против O365→COCO55.1/37.9; это разные exposure/capacity/recipe, не controlled YOLO26 pair. Paper COCO120+4 против YAML132/stop120; obj2coco paper29+49 против config56/stop48 — различающиеся рецепты, не единая цепочка. D-FINE Fig5 qualitative X не quantitative occlusion M proof. Сначала audit visible labels/input pixels и одна spatial alternative baseline. Потерянные resize пиксели не возвращаются от большего числа bins.

**Fallback условный:** YOLOX-s `0.1.1rc0/yolox_s.pth`, code `6ddff4824372906469a7fae2dc3206c7aa4bbaee`, 72,089,125 bytes HEAD; actual hash unknown. Current reported AP40.5 не legacy39.6 и preprocessing старых весов несовместим с новым release. Exact LinQ detector fallback не установлен. RF-DETR-M/L2026, RT-DETRv2 DSP и прочие W1 кандидаты сохранены ниже как каталог, не дополнительные активные runs. Ни одной target superiority/24GB fit/target latency цифры нет.

## F006 — Code, checkpoint, pretraining data и форма поставки: четыре отдельных слоя

**Основание:** S244–S14; S259–S04; W1-02 license registry. **Тип:** прочитанные первичные обозначения/ограничения, не legal clearance. YOLO code/models/docs явно AGPL-3.0 либо Enterprise; команда должна принять конкретную форму передачи и notices, существование README не означает compliance. Если выбранная закрытая proprietary форма несовместима с vendor grant и иной лицензии нет, этот путь blocked. D-FINE HF exact model repository имеет explicit Apache-2.0 model-level designation, сильнее одного code LICENSE; GitHub равенство байтов по имени/размеру не доказано. Отдельный native B2 stage1 grant/conversion chain unresolved; constructor с pretrained=True может скачать этот init до detector tuning, отключение — versioned change+load smoke. YOLOX official code Apache и release присутствуют, exact weight-specific scope unresolved; issue1865 — пользовательский вопрос без видимого maintainer grant, не запрет и не разрешение.

Objects365 upstream: academic-purpose download, annotations/site CC-BY4.0, image rights отдельно; shorthand проекта не заменяет upstream. Это **не** самостоятельное заключение о запрете trained weights, но unresolved scope сохраняется и для YOLO26 lineage. RF-DETR Apache-designated N/S/M/L не распространяет grant на Plus/PML variants. DEIMv2/EdgeCrafter noncommercial terms исключают их из активного переносимого shortlist до принятия use. RTMPose code Apache не автоматически exact weights clearance. Specialist timm model-card Apache конфликтует с project ImageNet weights notice — итог unresolved. Для всех retained assets сохранить source/license/card/notices/modifications, actual download/hash/load и target-data rights; не приписывать HEAD ни tensor integrity, ни бессрочную доступность.

## F007 — Выбранный training/export envelope, полностью UNRUN

**Основание:** S218–S22, source-backed предложение. Linux x86_64, Python3.11.9; отдельные project environments, Torch2.5.1/torchvision0.20.1 official cu124 для train, те же CPU versions для export; NumPy1.26.4, ONNX1.17.0, ORT CPU1.20.1, OpenCV4.10.0.84. Ancillary D-FINE candidates transformers4.44.2/calflops0.3.2; полный transitive resolver/lock/import **не выполнен**. ORT row1.20 opset21/IR10 — необходимая version bound, не proof kernels/parity. W1 torch2.14.1 image digest — реальная metadata candidate, не выбранный готовый общий recipe и не опровержение существования версии. Conservative separate fallback2.4.1/vision0.19.1 с новым recipe; не устанавливать старый core поверх image и называть прежним manifest.

YOLO proposed export: static1 FP32 640² CPU, dynamic=False/simplify=False/half=False/nms=False/opset18, wrapper explicit `dynamo=False`; e2e `[B,K,6]` ожидаемо, фактический graph/head/IR unknown. TopK/Gather остаются. Conditional dense с nms=None только если actual one-to-many weights сохранились; fusion их не восстанавливает. D-FINE native exporter EMA.module иначе model→deploy+postprocessor, images+orig_target_sizes→labels/boxes/scores, opset16; stock dummy32/dynamic axes и **store_true defaultTrue simplify** требуют proposed static1 adapter с explicit dynamo=False/dynamic_axes=None/simplify opt-in. Adapter не создан/не запускался; structural checker не numerical test. `-t` tuning≠`-r` resume, nc777/path placeholders надо заменить. Torch2.6 changed torch.load weights_only default; это риск exact checkpoint semantics, не доказанный отказ всех D-FINE весов. Actual train/val/save/reload memory и full graph gates остаются E003/E004.

## F008 — Основной measurement contract

**Основание:** S004–S11; F179; **тип:** предлагаемая спецификация на основе primary protocols. Основной вектор: timely event recall (все assessable GT к scenario deadline), eventual/late/missed, semantic FP/eligible camera-hour, duplicates/episode и /hour, wrong-actor, delivery latency, coverage/blind gaps, counts независимых groups. Late корректный alert не semantic FP, но остаётся deadline miss. Один alert не match двум GT; максимум timely cardinality, затем total delay, затем lexical IDs; GT не зависит от raw tracker ID. Deadline boundary inclusive, event interval half-open в fixturev0. Matching/ignore/censor/ties freeze до test. Дубликат ongoing эпизода не второй TP; второй человек/новый episode после rearm не должен подавляться global cooldown.

Eligible exposure — пригодное in-scope изображение с проверяемой GT; system outage внутри доступного видео не вычитается ради кандидата. Истинно отсутствующее/неоцениваемое видео unknown, не TN. Recall N=0 и precision при отсутствии alerts — N/A. Camera-hours не автоматически независимы. Detected-only p95 скрывает misses; RecallWithin(d) использует все GT. PTS/source time и monotonic decision/emit/receive раздельны, без capture mapping нельзя писать glass-to-alert. EOF где deadline ещё не прошёл — заранее заданное right-censor, не произвольный FN или быстрый TP.

COCO AP/area bins/IoU и MOT IDF1/HOTA — diagnostic, не safety event quality. ActEV TFA — instance-time, не count UI alerts/hour. Curated positive/ADL clips не production prevalence/FP rate. Wilson/exactbinomial/Poisson intervals только при подходящих units/dependence; zero FP верхняя односторонняя Poisson bound `-ln(alpha)/H`, все N успехов lower recall `alpha^(1/N)` — алгебраические следствия, не наши measured claims. Paired cluster uncertainty по incident/session/camera; кадры не independent trials. Нет универсальных FP/hour, threshold, числа групп, min FPS или certification из этих источников.

## F009 — Temporal/tracking/calibration: начальный минимум и пределы

**Основание:** W1-03/04/05/09 sources, W2-D/E. **Тип:** static/published mechanisms и наша policy, target effect unknown. CPU causal FSM с explicit fresh observation/unknown/gap/rearm; stale/extrapolated box и повтор кадра не новое подтверждение. Длительности в source seconds, не `track_buffer` frames; dt=1 Kalman/code frame-count требует конкретного timestamp/scheduling решения. Event UUID отдельно от track ID и person ownership; clothing/long occlusion не решаются TTL. ByteTrack low-score second association может восстанавливать треки, offline interpolation видит future endpoint и не online evidence. OC-SORT одна условная альтернатива на тех же detections; ReID neural node deferred до observed need и target pass.

Повышенный threshold не гарантирует precision monotonic на конечной выборке; изменённые NMS/tracking/FSM могут изменить вложенность. Сначала identity+tuned threshold versus calibrated+tuned threshold. Строго монотонная scalar calibration до aggregation не создаёт новых ранжирований/threshold attainable sets; ECE gain не alarm gain. Hard NMS baseline, Soft-NMS ограниченная DEV альтернатива, WBF не бесплатная замена: опубликован single-model negative result сохранён в branch. Невозможность наблюдать закрытую голову не доказывает no-PPE; phone bbox не phone-use; pose17 points не consciousness/contact/fall cause. Neural temporal, pose/ReID и crop verifier не обязательные стадии A.

## F010 — Native recovery честно approximate; trial mutation нельзя скрывать

**Основание:** S210–S08; W1-13/14 saved code; **тип:** статический control-flow вывод, GPU drill UNRUN. Ultralytics first-start-epoch single-rank OOM/backend retry halving floor1 сохраняет уже изменённый optimizer и повторяет work; batch1 retry тоже возможен. NaN поздно может restore last EMA/replay epoch, start epoch не rollback. Save ремонтирует live EMA/санитизирует half copy. Finite checkpoint/exit0/CSV не clean trajectory. Stock отключающих flags fail_on_oom/disable_oom_recovery/nan_recovery=False не установлено; amp=False/resume=False/explicit batch не выключают всё recovery. `optimizer_step`/on_before_zero_grad callbacks reserved и stock loop не dispatch; step post-hook≠applied update на fused AMP path.

Принята policy: OOM/NaN/save repair→FAILED_TECH для immutable A/B; salvage отдельный child `RECOVERED_NONCOMPARABLE`, native_ema attempt `RESUMED_APPROX`, новая recipe для изменения B/AMP/shape/optimizer. Applied updates null до проверенного observer, не epochs×dataset/EMA count; gaps→INCOMPLETE_OBSERVABILITY и не comparable success. Pending accumulation gradients не сериализованы, обязательного tail flush нет; epoch label не lossless boundary. D-FINE stage best_stg1 reload/EMA decay заранее часть recipe, unexpected nonfinite не чистый trial; save NaN.pth сам не останавливает AMP loop.

Минимальный proposed guard pinned subclass+append-only events, save copy on_model_save до stripping и внешний receipt; готовой реализации здесь нет. Native save weights EMA/half и state не exact raw/RNG/sampler/scheduler replay. Immutable pre-strip recovery snapshot и final inference artifact разные. После corrupt/missing/load failure — TRAINED_UNARCHIVED, transfer retry, не training заново. Exact continuation/controller/generation platform deferred. RPO/RTO, размеры/checkpoint latency и interrupt-resume effect unknown до E005.

## F011 — Реальные публичные Vast quotes и формула без двойного счёта

**Основание:** S145 raw JSON и S133–S12; **тип:** observed read-only HTTP200 metadata + documentary policy. Снимок **2026-10-23 17:04:35–37 UTC /20:04:35–37 MSK**, unauthenticated GET, не резерв. Фильтры RTX3090 num_gpus1/2 verified=true external=false rentable=true rented=false reliability≥0.99 disk_space≥100 allocated_storage100 on-demand order dph_total limit3. Исторические whole-offer total $/h: 1GPU55729405 .218148 (compute.186667+disk.031481),45174323 .241111,47272935 .267778; 2GPU45174324 .454444,56506123 .535556,57219980 .561111. 45174323/24 одна machine144003; нет шести независимых hosts. Full precision/fields ниже; ставки быстро устаревают. Многокарточный dph_base уже whole offer, не умножать ещё на2. dph_total уже содержит выбранный disk, не добавлять storage повторно.

Cost = whole-offer compute×actual active hours + allocated storage по state/rate/time + ingress/egress по фактическим quantity/unit + отдельные volumes/external storage/прочие документированные расходы + отдельно unknown tax/FX/payment. Idle running не бесплатно. Снимок storage_total_cost=storage_cost×D/720 — арифметика этих JSON, не универсальная календарная константа. CLI --storage GiB, field GB/month, billing GB/hour и TB network: byte divisor **unknown**, не смешивать SI/TiB. Ingress на rented machine / egress с неё; packages/weights/datasets/backup учитываются по metering, image-pull/loading precise scope unresolved.

Stopped compute не active, storage остаётся и может дороже running; stop не backup/GPU reservation, restart не гарантирован. Destroy удаляет container data, independent volumes остаются платными; expiry48h не backup SLA. Current billing+FAQ offline exemption конкурирует с legacy offline storage; как documentary default current, консервативный reserve до actual ledger. Loading имеет **current-current storage contradiction**, не заявлять полностью бесплатно. Account Charges/invoice/autobilling/negative balance/tax/FX не читались, расходы не разрешены.

## F012 — Выбран actual Vast wheel, legacy shell=True correction

**Основание:** S276–S15, actual small wheel static inspection. v1.9.0 release2026-10-20T21:31:52Z, commit `28bde4827374ef658694db5a1e1e61508b966e2f`, wheel324,493 bytes SHA256 **`dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b`** совпал с release metadata; entry `vastai.cli.main:main`, Python>=3.10,<4.0. Это реально полученные bytes CLI, не model checkpoint, не installation и не зависимый lock. В wheel modular `copy` использует subprocess **argv list, не shell=True**; checked returncode отсутствует и StrictHostKeyChecking=no сохраняется. Legacy vast.py вывод не переносится на wheel. Destroy имеет y/N prompt; это не archive receipt. CLI search default не включает rented=false, задавать явно. `local:path` dispatch отличается от unprefixed Unix local; первые команды выбирают numeric remote/unprefixed local Linux/WSL path. Native Windows pip не устанавливает rsync/ssh автоматически.

Copy HTTP/initiation/exit status, actual lifecycle state и archive verification — три разных результата. Before destroy обязательно immutable files+bytes+hash+trusted destination load, recorded parent/state/receipt и отдельное поручение lifecycle; не один автоматический script. Stop/start response не actual stopped/running, poll/reconcile. Show Charges endpoint resource type/source/items gpu,disk,bwd,bwu; CLI --charges/--invoices raw pagination с UTC bounds и next_token; invoices платежи≠usage. Расходы/stop/destroy здесь не выполнены. Полные будущие exact команды, даты placeholders и platform caveats сохранены в W2-G подробном блоке.

## F013 — LinQ public, historical, delivered, executed — разные статусы

**Основание:** S273–S03, S001, W1-16; **тип:** vendor docs/extract и интеграционный контракт. Manual2025 `RU.РМДВ.04.06.014-03 34 01` worked end-to-end **ResNet50 classification** ONNX→TF→quantized→compile→runtime; `yolo5s` p22 только tested-name без checkpoint/decoder/export identity. `/tech` live undated перечисляет yolo5s/yolo8/yolo11 и resnet/mobilenet, это family claim без version matrix и не YOLO26 support. Exact detection fallback не установлен. Первым infrastructure probe брать bundled known-good **выданный** vendor example; если только manual, диагностический ResNet50, не произвольный YOLOv5s. Этот smoke не safety baseline.

Manual PDF bytes/hash/PNG/visual в W2-F не получены из-за TLS/доступа, получен полный извлечённый текст; подозрительные names/indent/versions не copy-paste verified. Ubuntu20.04/Python3.11/RAM32GB/i7 example не actual server inventory; sample Python3.8 log не новая установленная версия. TLM estimate не wall latency. DEFAULT/STAGING и tensor-cache не гарантируют multi-model concurrency/residency. Каждый реально runtime neural node detector/pose/ReID/V/T/router/fusion имеет отдельный artifact/placement/parity gate; teacher-only отсутствует online только если действительно исключён. Neural CPU policy unresolved, CPU state storage не то же что execution placement.

Передать exact source/checkpoint/config/head/env/ONNX/IR/domain-opsets/operators attrs+shapes+dtypes, golden tensors, preprocessing/layout/rename/decoder class/geometry, converted/compiled hashes, precision owner, runtime DAG/state/reset/TTL/load/queue/crop fanout и acceptance. Четыре ворот: same-head reference→float ONNX→target representation→real issued LinQ full pipeline. ORT checker/run и TPU program existence не actual placement evidence. Actual SKU/SDK/access/ops/precision/residency/concurrency/latency **unknown**. До heavy train проверить путь pretrained; после финального checkpoint gate повторяется.

## F014 — Один concrete specialist, никакой обязательной второй сети

**Основание:** S259–S14. timm v1.0.22 code `78c3724f4545c0067d0b4d2f7df6337196be01ce`, exact `timm/mobilenetv3_small_100.lamb_in1k@1824797e7887cbec1990e4adbd6675960a36c589/model.safetensors`, metadata10,241,912 bytes LFS SHA256 `46d2c063b18125884c48937afa4c49e18128869e52e8db96df48bf0a4d7ff697`. Bytes/load/train/export UNRUN. ImageNet1000 initialization, не phone-use/fall/PPE classifier. Proposed future3-head `helmet_visible/bare_head_visible/unassessable` crop fine-tune; unknown≠safe/no-PPE. 224² input RGB FP32 mean/std ImageNet/bicubic/crop_pct.875 exact reference, изменение crop geometry новая recipe. Center crop может срезать helmet; resized tiny head не новые детали. Code Apache, model-card Apache designation против timm ImageNet weight notice unresolved.

Trainer pretrained-path умеет замену1000→3, initial-checkpoint strict не взаимозаменяем; missing только intended head. Native exporter всегда dynamic batch и наследует Torch default в обычной ветке: proposed static1 explicit legacy adapter UNRUN. Classifier neural state отсутствует, external per-track cache/FSM reset остаётся. V только при observed wrong-visible-class crops, proposal ceiling/threshold-only comparator и отдельном LinQ pass. Обычный TSM shift читает t+1; online-demo другой MobileNetV2 Jester27+10state buffers, другой checkpoint и reset obligations; tvm.nd.empty не zero reset guarantee. Neural temporal deferred. Ни KD, ни ensemble не первый route.

## F015 — Минимальный registry и приёмка артефактов

**Основание:** W1-13/14/15, W2-A/G; **тип:** proposed engineering contract, файловый runtime registry ещё не создан. Достаточны immutable manifest на run/attempt и append-only events: source+patch+env lock/image digest, init weight exact source/license/hash, data+labels/split/group lineage hashes, requested/resolved/effective config/head/ontology/seed/batch/AMP/stop policy, actual consumed work/unknown counts, reason/parent/recovery mutation, memory/time/cost and offer IDs, native recovery checkpoint до strip и отдельный selected inference artifact, raw predictions/event ledgers и diagnostics, export/parity/target records, external receipt. Manifest identity не перезаписывается effective config. Final seal не равен process exit0. `SUCCEEDED_COMPARABLE` требует eligibility и complete observation; `TRAINED_UNARCHIVED`, `FAILED_TECH`, `RECOVERED_NONCOMPARABLE`, `RESUMED_APPROX`, `INCOMPLETE_OBSERVABILITY` раздельны. Не реконструировать exact exposure по конечному CSV. Secrets/account raw остаются privately controlled. Успех archive не является target quality/license/fit proof.

## F016 — Одна GPU default; две только при ready-work и измерении

**Основание:** S181–S11 и W1-12 offers; **тип:** documentary resource model+proposed decision. DDP replica на каждой GPU не pool48GB; accumulation не эквивалент physical batch/BN. Предпочтение для двух — независимые frozen полезные jobs/paired seeds, когда они готовы. Joint CPU/RAM/disk/network contention измеряется; price2GPU и NVLink0 в observed offers не x2 speed. DDP только после measured per-rank fit, recipe/global-batch/convergence и better time-to-result; multi-node D-FINE global rank→CUDA device risk source-inferred, не готовый запасной launcher. Train/eval полезен только при готовом checkpoint stream; native val нельзя молча убрать, она влияет на best/EMA/stop/stages. Data/labels/evaluator/LinQ bottleneck не ускоряется второй CUDA. Решение по completed valid decisions до deadline, full cost и reserve; никаких выдуманных training-hour оценок.

## F017 — Пять предлагаемых role owners, checkpoint freeze и резервы

**Основание:** S001/S002/S003, W1-11/15, W2 route; **тип:** выбранная организационная policy, не фактическое назначение людей. На окончание W2 **23.10 20:50:48 MSK** до25.10 10:00 оставалось **37ч09м12с**, уже не исходные45ч; это арифметика расписания, не training budget. Автор должен указывать фактическое время своей сборки отдельно; не перезапускать эти часы в отчёте.

| Proposed owner slot | Ответственность/выход | Cutoff |
|---|---|---|
| R1 data/annotation + reviewer coordination | Rights/assets/lineage/labels, independent groups, time mapping; второй reviewer из R2 | До любого training; отсутствие assets→только DEV/synthetic feasibility |
| R2 evaluation/FSM | Scenario deadline, oracle/fixture runner, causal ledgers, freeze/lockbox access | Протокол до сравнения; после final freeze настройки прекращаются |
| R3 baseline/training + Vast operator | Exact init/env/qualification/один B, mutation log/native snapshots/receipt, budget с владельцем аккаунта | B только после data/runtime/resource gates; controller/exact replay deferred |
| R4 LinQ integration | Issued package/policy/sample, graph/placement/parity/state/full latency | Блокирует optional runs, если обязательный target path ещё не готов |
| R5 product/submission + coordinator | Один scope, GUI/уведомления/journal/evidence, README/demo/teaser/slides, gate/cutoff ledger | Обязательные submission materials и проверка загрузки до25.10 10:00 |

Это пять функций для команды из пяти, не утверждение, что кто-то уже назначен или доступен. Порядок времени: сейчас A и дешёвые gates. **К24.10 11:00** иметь один end-to-end feasibility либо записанный конкретный blocker+сужение scope. После11:00 новый train/challenger допускается только при законченном прошедшем incumbent, ready input и измеренном запасе; otherwise A/fix mandatory path. **К24.10 18:00** freeze scenario+models+heads+rules+sampling+evaluator; прекращение новых families/scenarios/optional GPUs. Затем обязательные final parity/LinQ/evaluation/delivery/submission, только blocking fixes с новым artifact ID и повтором затронутой проверки. Lockbox-driven fix не независимый результат той же версии.

Перед каждым B/C считать по фактическим замерам `available_until_freeze - remaining mandatory LinQ/parity/evaluation/archive/product/submission work - recovery reserve`; если резервы неизвестны/не обеспечены, optional run не начинается. Длительности не придуманы, резерв не «нулевой по умолчанию». Jobs с прогнозируемым завершением после freeze не запускать; growing queue, неготовые labels/SDK, failed artifact receipt либо необъяснённая mutation останавливают expansion. C не вытесняет obligatory verification. На18:00 optional незавершённый run остановить по объявленной policy, сохранить state и incumbent; не обещать эпохи «ещё чуть-чуть».

## F018 — Какие пробелы закрыла W2, а что осталось вне публичного поиска

**Основание:** W2-A…G и CRITIC. **Тип:** интеграционное разрешение критики. Документально появились pinned trainer fail/fork/progress, isolated compatibility envelopes и exporter traps, O365 lineage baseline, stronger exact D-FINE HF grant/hash metadata, obtainable URFD timing/rights и CAUCAFall motion-trigger limit, 10 causal fixtures, один specialist init с выявленным license conflict и defer temporal, ResNet50/yolo5s distinction и граница manual, actual modular CLI wheel и state/ledger contract. K006 выбран F004, K011 выбран F003/F017 — не никому не назначенная работа.

Остатки — team private data/use/labels/independent groups, accepted checkpoint/license/artifact bytes, actual account offer/rates/Charges/payment, actual installed stack/guard/fit/recovery, issued LinQ SDK/SKU/operators/backend/capacity/performance, organizer CPU/deadline interpretation и target quality. Их не закроет третья public wave без смены входов; конкретные proposed owners/closure в Q. «Closed documentary» никогда не «tested production».

## F019 — Минимальные первые эксперименты и граница всей библиотеки

**Тип:** proposed order. Активная последовательность E001→E002→E003/E004; E005 только если B/recovery используется, E006 один B после gates; E007/C при достаточном измеренном резерве. Остальные E — условные library alternatives, не обязательный план. Каждая проверка фиксирует question, входы, control, split, metrics, stop, artifacts и отрицательное толкование успеха. Никакого опыта не выполнено в research. Полные branch recipes/варианты/контрпримеры сохранены в подробных F ниже.

## F020 — Сквозные ограничения доказательств

DOC≠test; source pin≠installed lock; HTTP HEAD/metadata digest≠полученные/загруженные model bytes; published benchmark≠target paired evidence; image/checkpoint parameters≠24GB train+val peak; same epoch≠same applied updates; finite saved tensor≠clean trajectory; copy exit0≠archive; ORT≠TPU; classifier/pose state≠причина действия; curated clips≠background prevalence; pooled кадры≠независимые incidents; repeated selection≠confirmation; old lockbox result≠new refit artifact pass. Unknown hardware/SDK/date/price/runtime остаются unknown. Все пределы должны сохраняться и в коротком машинном отчёте.

# E-ID — предлагаемые различающие эксперименты (все UNRUN)

Общие условия: разрешённые inputs, immutable IDs, F004 data roles, заранее выбранные acceptance floors/meaningful gain/stop rules без выдуманных универсальных чисел; raw counts и ошибки сохраняются. Synthetic tensors допустимы для mechanics/shape, synthetic ledger для logic, но ни то ни другое не quality evidence. Actual paid/GPU/device действия требуют отдельного поручения владельца.

| E | Вопрос и один control/factor | Входы и split | Метрики / stop | Артефакты / исход / чего успех не доказывает |
|---|---|---|---|---|
| **E001** | Верен ли evaluator/FSM? Oracle ledger против specification C01–C10, одна policyv0 | Synthetic-only fixtures W2-D; не TRAIN/LOCKBOX | Exact timely/late/duplicate/actor/rearm/censor counts; любое mismatch блокирует tuning | fixtures/config/expected/actual/diff. PASS только logic; не detector accuracy и не industrial dwell/deadline |
| **E002** | Доступно ли достаточно свежего causal support к deadline? Native oracle→frontend replay; immediate versus одна FSM, затем одна samplingΔ с фазами | Rights-accepted exact media, decoded PTS, event/onset/observable/end/unknown; DEV | Per-phase timely/late/miss/censor/duplicates, fresh samples, reviewed negative seconds; no time mapping→stop time claim; missing independent groups→feasibility | Media/label/hash+mapping/phase schedule/observation cache/event ledger/view log. Oracle fail→scope/schedule; frontend fail→model. Не LinQ wall deadline, не factory FP/hour |
| **E003** | Исполним ли конкретный neural path на выданном LinQ? Vendor sample serial control→actual same-head graph | SDK identity/policy/sample, actual FP32 ONNX+golden tensors, DEV, W2-F P0–P8 | Compile/load/schema/backend/parity/state/reset/residency/burst/full delivery latency; mandatory node blocked/unverified→нет final PASS | SDK/model/env/operator/placement/compiled hashes, raw outputs/traces. Sample pass не YOLO pass; serial pass не concurrency; ORT неTPU; другой bundle требует нового gate |
| **E004** | Согласован ли выбранный env/export/24GB qualification? Pretrained export-first, затем representative train+val+save/reload | Trusted init, accepted constraints→actual lock, small TRAIN/DEV fixture; CPU/local first; отдельно разрешённая actual3090 qualification | pip check/import/load/key/head/schema/numerical diff/IR/op inventory; peak allocated/reserved train и val/actualB/AMP counts; any incompatibility→new manifest/blocked | Resolution+wheels/lock/source+patch/config/logs/graphs/tensors/memory/hardware. Synthetic shape pass не quality; one step не full worst-case memory; 4070 не proof3090 |
| **E005** | Отклоняется ли false-clean и цела ли внешняя recovery copy? Guard versus stock disposable control + corrupted second test copy | Pinned guard/env, tiny TRAIN/synthetic fixture, disposable snapshots, outside endpoint; lockbox absent | OOM dispatch inclB1, start/later/transient NaN, EMA/half repair, AMP attempts/calls/applied observer, pending accumulation; false accept/next work after fail должны0 в проверенном scope | Events/state/parent/config/checkpoint/list/bytes/hash/trusted-load receipt. Failure→FAILED_TECH/TRAINED_UNARCHIVED. Native resume approximate; PASS не RPO/exact trajectory/reliability/model gain |
| **E006** | Устраняет ли один target fine-tune human-confirmed frontend error? Frozen pretrained A против одного B | Exhaustive TRAIN ontology/rights, independent DEV; same full event pipeline; один заранее утверждённый recipe | Primary event quality при одинаковом FP/deadline/coverage constraints, class retention, actual work/VRAM/time; unknown data/runtime/license→не начинать | Init/load/labels/split/env/config/curves/checkpoint/actual-progress/raw predictions/target gate. PASS не universal new-camera gain; fullFT vsfreeze дополнительно не запускать автоматически |
| **E007** | Почему нужен C? Сначала same-checkpoint640 против одной spatial policy; C D-FINE-M только при сохраняющейся visible localization error | DEV error atlas original/preprocessed pixel+visibility/label completeness; fixed groups; TRAIN только если chosen adaptation | Target size/occlusion slices, event timely recall/FP/latency, paired counts/uncertainty; no meaningful gain либо mandatory reserve missing→stop C | FN gallery/policy/raw predictions/compute+pixel cost, whole pipeline freeze. Native product comparison не pure architecture effect; published COCO ranking не ответ |
| **E008** | Полезнее ли targeted annotation/одна augmentation? Control continued training и random annotation равного annotation budget; выбрать **один** фактор по error audit | TRAIN mining+QA; DEV selection, all parent groups disjoint; no lockbox mining | Event/object retention, human label effort, eligible exposure, error slices; partial labels/semantics damaged→stop | Annotation ledger/reviewer/version, exhaustive coverage/ignore, data snapshots/transforms. Improved train loss/synthetic AP не real-domain transfer; targeted examples не prevalence |
| **E009** | Исправляет ли tracker конкретные ID→event ошибки? ByteTrack versus OC-SORT, same detections/rules | Fixed DEV cached causal detections/PTS, ID/owner/episode labels | IDF1/HOTA diagnostic плюс wrong-owner/timely/duplicate/rearm under gaps; no event benefit→не добавлять complexity | Detection+track+alias/event UUID logs, config/seconds semantics. MOT score pass не phone ownership/physical contact; offline interpolation excluded |
| **E010** | Даёт ли pose17 дополнительное различение видимых состояний? Bbox rules control versus RTMPose-s same proposals | Independently grouped DEV with visibility/keypoint/episode labels, exact rights/init/config | Timely event quality/coverage/unknown/occlusion/crop cost; no valid pose/proposal→abstain, не hard safe gate | Pose+confidence/crop/PTS/FN gallery/target per-node logs. PASS не unconsciousness/fall cause/metric geometry; deferred в A |
| **E011** | Нужен ли один V? D+FSM threshold-only versus strict/selective timm3-head V | After visible wrong-class atlas/proposal ceiling, rights/exhaustive supervised TRAIN crops, DEV; lockbox only frozen final | FP/hour at same timely recall/deadline, abstention/coverage, proposal-conditioned ceiling/calls/bursts; no crop/gain/license/device→defer | Exact init/license/head/route/export/state/cache/raw/event/device artifacts. GT-crop accuracy не real-proposal/event benefit; neural temporal/KD separate deferred work |
| **E012** | Даёт ли вторая GPU полезное решение до freeze? Isolated1GPU versus measured joint ready jobs; DDP лишь separate recipe | Разрешённый actual offer/account, готовые jobs/locks/data; TRAIN qualification/DEV eval, no lockbox selection | Completed valid result walltime/full compute+storage+transfer cost, CPU/RAM/I/O contention, VRAM, actual updates; reserve/work missing→оставить1 | Offer/timeline/ledger/resource traces/receipts. Samples/s≠accuracy gain, cost headline≠full invoice, no x2 assumption |

E001 fixtures v0 подробные искусственные constants сохранены в W2-D блоке ниже: D2.0s, support2fresh с gap≤.75/Δt≥.5, negative1.0s rearm; это unit-test values, **не предложенные промышленные пороги**. E003 включает measured source→available→inference→decision→emit→receive; cached replay не wall-clock device run. E005 minimum recovery не превращается в обязательный сложный controller. Пределы остальных branch experiments сохранены в каталоге, но не добавлены в active route автоматически.


# Подробный каталог сохранённых наблюдений, выводов и процедур

Следующие F-записи сохраняют содержательную детализацию обеих волн. Это нормализованные секции базы с полными исходными условиями, а не новый независимый эксперимент сборщика. Локальные F-ID внутри секции могут ссылаться на один глобальный F-ID: единицей хранения выбран смысловой блок, а не каждое предложение. Все local→global соответствия находятся в ID_MAP.

Для каждого блока действует обязательная шкала: **DOC/static** — прочитанный код/docs/metadata; **PUBLISHED** — численный результат авторов с их условиями; **OBSERVED** — реально полученный HTTP/малый artifact и его локальная проверка; **INFERRED/PROPOSED** — наш вывод/будущая процедура; **UNRUN** — не исполнено. Точные типы уточняются внутри записи. Ни одна запись не даёт собственных target accuracy/VRAM/throughput/latency/RPO: они unknown. Предлагаемые команды и эксперименты не исполнялись.

При конфликте W1 и W2 применимость устанавливается F005–F014 и W2 записью: выбранный source-backed envelope заменяет candidate latest image как рабочее предложение; actual wheel заменяет legacy CLI claim; ResNet50 worked sample отделён от yolo5s tested-name; O365 lineage YOLO26 и точный grant D-FINE HF уточнены. Исходная история W1 остаётся доступна, но не является активным runbook. Все экспериментальные разделы ниже — библиотека для последующих решений, **не очередь обязательных запусков**; активная очередь только F003/F017.

## F021 — W1-01: Решение для команды

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Решение для команды»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F021 — основная рекомендация.** Оптимизировать своевременное обнаружение независимых опасных эпизодов, ограничивая поток ложных сообщений и время без контроля. Рабочая карточка системы должна одновременно показывать `event recall by deadline`, `false notifications / observed camera-hour`, дубликаты, задержку до уведомления, покрытие наблюдением и число независимых событий/камер/часов. Для красных и жёлтых событий нужны разные ограничения и рабочие точки. Одно число `accuracy`, `mAP` или `F1` для выбора недостаточно. Это наш инженерный вывод из требований кейса и несовпадения целей объектной детекции, локализации действий и операторского оповещения; это не формула жюри.

**F021 — порядок отбора.** Сначала отбрасывать варианты, не исполняющие нейронный inference на LinQ, нарушающие согласованный дедлайн, выдающие несколько сообщений на продолжающийся эпизод, либо не имеющие измеряемых timestamp/coverage. Затем строить Парето-фронт по пропускам к дедлайну, ложным сообщениям и нагрузке. Если владельцы процесса ещё не задали допустимые границы — показать фронт и неопределённость, не придумывать веса. Более высокий object mAP не компенсирует провал срочного event recall.

**F021 — практическое следствие.** На хакатоне полезнее сравнить несколько полностью определённых систем «детектор → трекер → правило → подтверждение → дедупликация → доставка» на одинаковых непрерывных видео, чем ранжировать отдельно детекторы по случайным кадрам. Нужны отрицательные интервалы с обычной работой, сложные похожие действия и короткие реальные нарушения. Положительные постановочные клипы пригодны для проверки возможности, но не для оценки реального precision или FP/час.

Основание кейса: `_WORK/CASE_NOTES.md`, наблюдения корневого исследователя по официальному PDF, с. 5, 7, 13: баланс качества, задержка порядка нескольких секунд, одно сообщение на продолжающуюся ситуацию, LinQ и обязательные замеры скорости. Эти страницы в данной ветке заново визуально не просмотрены; происхождение — переданные прямые наблюдения root. Рассказ экспертов об accuracy не устанавливает численную функцию оценки; CPU+TPU — сообщение команды, конфигурация неизвестна.


## F022 — W1-01: Какие знания переносим из соседних областей

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Какие знания переносим из соседних областей»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S004, S005, S006, S007, S008, S009, S011, S013.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


| Область | Проверенное основание | Что используем | Что не переносим автоматически |
|---|---|---|---|
| Объектная video analytics | COCO: AP/AR при разных IoU, категориях и размерах [S004] | Диагностика локализации и трудных размеров до анализа событий | AP на фотографиях не равен вероятности своевременного оповещения; COCO size bins не равны пригодности конкретной камеры |
| Temporal action localization | ActivityNet evaluator: ранжирование confidence, temporal IoU, AP, повторное сопоставление GT запрещено [S005] | Отдельный диагностический тест границ событий; проверка дубликатов | Хорошая локализация завершённого клипа не доказывает causal online alert и малую задержку |
| Extended surveillance | NIST ActEV 2020: instance miss и time-based false alarm с DET [S006] | Не сводить ошибки к кадрам; строить кривую пропуски/ложные тревоги | TFA — длительность/кратность ложных интервалов, **не число сообщений на камеру-час** |
| Real-time surveillance | NIST SDL 2021 оценивает вывод в ограниченном времени, различает известные/неизвестные площадки [S007] | Совместно проверять качество, реальное исполнение и переносимость | Их машины, протокол overlap и допустимая TFA не являются целями LinQ-кейса |
| Safety/alarm management | HSE: полезное сообщение, определённый ответ оператора, достаточно времени, ограничения внимания [S008, S009] | Стоимость ошибки включает перегрузку и несвоевременный ответ; нужна отдельная приоритизация | Не заявляем сертификацию safety function; нормы process industry не дают универсального FP/камеро-час для CV |
| Статистика испытаний | NIST: Wilson/exact binomial; R survival: Poisson rate CI [S011–S013] | Показывать знаменатели, границы неопределённости и условия независимости | «Точный» интервал не исправляет смещённую выборку и коррелированные события |

**F022 — важное противоречие метрик.** ActEV и ActivityNet намеренно отвечают на разные вопросы. У ActEV TFA штрафует ложную длительность и одновременно перекрывающиеся экземпляры; дробление ложного интервала на множество неперекрывающихся фрагментов само по себе не увеличивает TFA [S006]. В интерфейсе такое дробление может породить шквал сообщений. Поэтому даже заимствование официального surveillance evaluator требует второй, продуктовой оценки уведомлений. Обратная крайность: cooldown может сильно уменьшить число сообщений, скрыв новые независимые события. Требуется тест на reset/rearm и разные сущности.


## F023 — W1-01: Проект метрической спецификации, версия 0.1

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Проект метрической спецификации, версия 0.1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S004.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Всё в этом разделе — предлагаемый контракт команды. Конкретные временные допуски, IoU, confidence и границы допустимости должны фиксироваться на development-части после согласования определения событий; ниже они намеренно символические.

### 1. Единица истины и разметка

GT — эпизод `event_id`, `scenario`, `severity`, `camera_id`, `scene/site_id`, `actor_id` или множество участников, `zone/rule_version`, `t_onset`, `t_end`, `t_observable`, `deadline`, `visibility/ambiguity`, `annotation_version`. `t_onset` — начало определённого нарушения, а не начало файла или момент, когда разметчик решил назвать ситуацию опасной. `t_observable` — первый момент, когда нужные для этого класса признаки достаточно видимы по заранее записанным правилам. Устойчивое состояние и мгновенное действие требуют разных определений начала/конца.

Нельзя объявлять человека без каски из-за отсутствия бокса каски, когда голова закрыта: `unknown/occluded` отличается от подтверждённого отсутствия. Аналогично «лежит» не означает доказанное бессознательное состояние, а близость в 2D не доказывает опасную метрическую дистанцию. Семантика и геометрическая калибровка передаются соседним веткам; наша метрика должна оценивать именно обещанный класс.

Для неопределённой границы разрешить аннотацию `[t_onset_earliest, t_onset_latest]` и отдельно показать чувствительность задержки к этой неопределённости. Разногласия разметчиков разрешать до просмотра тестовых предсказаний. «Непонятный» материал не удалять молча: количество и длительность исключений публиковать, с причинами.

Сообщение системы — `alert_id`, `event_key`, `scenario`, `severity`, `camera_id`, `actor/zone`, `evidence_start/end`, `first_evidence_frame_pts`, `capture_time`, `inference_done`, `rule_confirmed`, `notification_emitted`, `notification_received/rendered`, `score`, `model/rule/runtime_version`. Треки могут меняться; GT episode ID не должен зависеть от ID трекера.

### 2. Сопоставление событий и сообщений

Допустимая пара должна иметь правильный класс/зону/участника или документированное правило пространственного соответствия, а также временное соответствие определению сценария. Нельзя засчитывать «пожар где-то в этом видео» вместо данного события. Допуски границ, actor/zone matching и момент разрешённого раннего предупреждения определяются до lockbox.

Для итогового event recall использовать детерминированное **one-to-one** сопоставление: одному эпизоду максимум одно первое корректное сообщение; одно сообщение не закрывает два независимых эпизода. При неоднозначном пересечении выбирать maximum-cardinality matching среди допустимых пар с документированным tie-break по своевременности и затем времени, независимо от метода. Для online-продукта полезно сохранять также последовательное сопоставление при поступлении сообщений: расхождение с offline matching — отдельная диагностика.

После сопоставления сообщения распределяются на первые истинные, поздние истинные, повторные к уже обнаруженному эпизоду, ложные семантически/пространственно и неоценимые из-за отсутствия GT. Первичное корректное сообщение не превращается в дополнительный TP из-за смены track ID. Повторное сообщение о всё ещё продолжающемся эпизоде увеличивает нагрузку/duplicates. Если красное повышение приоритета жёлтого — допустимая эскалация, это заранее отдельный тип перехода, а не произвольное исключение.

Размечать условия завершения/rearm: продолжение за краткой окклюзией, уход/возврат, второй человек, новое независимое действие. Большой глобальный cooldown нельзя считать успешной дедупликацией, если он глушит последующие нарушения.

### 3. Обязательные основные метрики

Пусть `N` — число GT эпизодов в заявленном scope, `M` — число хотя бы раз корректно обнаруженных эпизодов, `M(D)` — число с первым корректным сообщением не позже сценарного дедлайна `D_e` от onset. Тогда:

- `EventRecall = M/N` и `MissRate = 1 − M/N`;
- `TimelyEventRecall = Σ 1[first_correct_alert(e) − onset(e) ≤ D_e] / N`;
- `LateDetectionRate = (M − M(D))/N`; отдельно никогда не обнаруженные `(N−M)/N`;
- `SemanticFalseAlertsRate = N_semantic_false / H_observed_eligible`;
- `DuplicateRate = N_duplicate / N_detected_events`, плюс `N_duplicate / H_observed_eligible`;
- `NonActionableNotificationRate = (N_semantic_false + N_duplicate + N_other_nonactionable)/H_observed_eligible`, с непересекающимися категориями и записанной политикой для late;
- `NotificationPrecision = N_first_correct / N_assessable_notifications`, при чётко указанном статусе поздних и дубликатов. Для срочного канала дополнительно `TimelyNotificationPrecision`, где поздние не являются своевременными TP;
- поток **всех** сообщений на оператора-час, пики по фиксированным временным окнам и доля окон перегрузки. Порог перегрузки даёт владелец процесса, а не исследователь.

Для каждого класса с `N=0` recall — `N/A`, а не 0 или 1. При отсутствии сообщений precision — `N/A`; это не основание объявлять систему идеальной. Нельзя усреднять undefined значения как нули без отдельного соглашения. Поддерживать micro-итоги, macro по заявленным классам и индивидуальные значения; micro может скрыть редкий красный класс.

Число повторов на событие и число ложных событий на час отвечают разным вопросам. Дубли истинного эпизода тоже тревожат оператора; поэтому UI-нагрузка не должна учитывать только семантические FP. Отдельная `false alarm active duration / eligible negative time` полезна для постоянно подсвеченной зоны, но названа иначе и не выдаётся за FP notifications/hour или за точный ActEV TFA.

### 4. Время без наблюдений и знаменатели

Для каждой камеры и сценария хранить непересекающиеся интервалы `scheduled`, `input_available`, `readable/annotatable`, `in_scope`, `pipeline_healthy`, `dropped/stale`, `unknown`. Не просто «число обработанных кадров / FPS»: это может скрыть длинный разрыв. Единица exposure — реальная длительность eligibility, сумма по камерам. Параллельные камеры дают camera-hours, но не обязательно статистически независимые часы.

`H_observed_eligible` — длительность планового контроля, где существует пригодное изображение для данного сценария и разметка позволяет судить о нём; **системный отказ внутри этого времени не вычитается по удобству кандидата**. Пропуски inference/потерянные сообщения при доступном видео входят в end-to-end качество. Отдельно можно дать detector-only rate на обработанном подмножестве, строго обозначив условный знаменатель. Видео с неоднозначной истиной нельзя назвать отрицательным.

Публиковать `InputCoverage = H_input_readable_in_scope/H_scheduled_in_scope`, `ProcessingCoverage` внутри доступного времени, максимальный blind gap и распределение длины пробелов. При известном из внешней разметки событии во время сбоя pipeline — FN end-to-end. При полностью отсутствующем видео неизвестно, были ли нарушения: это unknown exposure, а не true negative. Если независимый журнал происшествий подтверждает событие в этот промежуток, можно отдельно включить его в deployment/system recall, объяснив источник истины.

Публиковать два обязательства: качество **при наблюдаемом входе** и способность реально обеспечивать наблюдение. Уменьшение denominator из-за отключения проблемной камеры не доказывает улучшение системы. Для negative-only теста дополнительно дать `FP/H_negative_observed`, поскольку он измеряет чистый фон; не смешивать такой знаменатель с all-observable exposure в сравнении кандидатов.

### 5. Latency-to-detection

Основная задержка — от GT onset до момента, когда операторское приложение действительно получило/отобразило первое корректное сообщение. Отдельные компоненты: захват/буфер → очередь → preprocess → inference → tracker/rule/confirmation → доставка/render. `Inference ms` и throughput не заменяют полную задержку. Если доступна только серверная отправка, назвать метрику server-emission latency; UI latency остаётся неизвестной.

В file replay использовать PTS для содержания и измеренные monotonic wall-clock времена поступления/обработки. При realtime replay отображать соответствие PTS → wall time; offline обработка «быстрее длины видео» не доказывает deadline, если используется будущий контекст. Запретить будущие кадры после момента выдачи решения; длина causal буфера и warm-up входят в бюджет. Часы между узлами синхронизировать либо оценить погрешность; при неизвестном capture delay не заявлять истинную glass-to-alert latency.

Дать median, p95/p99 (только при достаточном числе наблюдений), максимум, распределение по сценариям и `RecallWithin(d)` по диапазону d. Только detected-only latency систематически скрывает пропуски: основная кривая имеет знаменатель **все GT**; не найденные к концу допустимого горизонта остаются неуспехом. Поздние за пределами дедлайна считаются deadline misses, даже если eventual recall высок.

События у конца записи без достаточного периода наблюдения после onset отмечать right-censored по заранее записанному правилу: продолжить запись или исключить из deadline-анализа с опубликованным числом; не выдать их за быстрые/пропущенные произвольно. Отдельно считать latency от `t_observable`: это объясняет оптическую трудность, но не заменяет задержку от реального onset, важную для безопасности.

### 6. Объектный уровень для поиска причины

Отчёт по человеку/PPE/предметам должен включать per-class AP, recall на выбранной рабочей точке, размер объекта в исходных пикселях и после resize, степень окклюзии и срезы камеры. COCO AP@[.50:.95] полезен как воспроизводимая диагностика [S004], но локальная семантика PPE и зона ответственности отличаются от COCO. Нужен одинаковый evaluator/config между кандидатами; IoU и area definition фиксировать.

Фрагментация треков, потеря actor association, перескок зоны и неверный rearm — отдельные причины event FN/FP. Улучшение детектора, которое мало влияет на downstream события, не является приоритетом само по себе. Ранжировать ошибки по их вкладу в событие/задержку, а не только по количеству ошибочных кадров.


## F024 — W1-01: Цена ошибок, рабочие точки и ловушка accuracy

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Цена ошибок, рабочие точки и ловушка accuracy»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S008, S010.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F024.** При редких нарушениях accuracy почти полностью определяется обычным фоном. Алгебраический контрпример, **не измерение системы**: если нарушение есть у 1 из 1000 выбранных единиц, постоянный ответ «нет нарушения» даёт 99,9% accuracy и 0 recall. В видео выбор единицы произволен: удвоение FPS увеличивает количество почти одинаковых TN, не улучшая число обнаруженных эпизодов.

Для prevalence `π`, sensitivity `r` и false-positive probability `f` в одной и той же чётко определённой единице:

`Precision = π r / [π r + (1−π) f]`.

Это наша алгебра по определениям, а не обещание реального precision. Балансировка тестовых positive/negative клипов меняет π; полученный precision нельзя прямо переносить на непрерывный производственный поток. PR-кривую полезно показывать рядом с event recall–FP/hour; вывод о зависимости от дисбаланса поддерживает [S010]. Низкий frame-level FPR при очень большом количестве фоновых кадров способен дать много сообщений, но умножение его на FPS не даёт точный event FP rate: ошибки коррелируют, а temporal logic и дедупликация меняют количество.

**F024.** На одном и том же фиксированном скоринге повышение threshold обычно уменьшает множество срабатываний и не увеличивает recall; precision при этом не обязан монотонно расти на конечной выборке. После смены NMS, трекинга, confirmation, gate или cooldown даже простая вложенность предсказаний может исчезнуть. Поэтому измерять весь pipeline заново.

Precision можно «улучшить» подавлением коротких и неоднозначных эпизодов: исчезают FP, но одновременно короткое вторжение под груз, падение или быстрое опасное действие не успевает пройти несколько секунд подтверждения. Усиленное требование устойчивого трека исключает частично закрытых людей; жёсткий PPE-gate пропускает нарушения с плохо видимой головой. Поднятие threshold без аудита FN даёт ложное ощущение надёжности.

Recall можно «улучшить» низким threshold, длинным активным интервалом и повторной рассылкой. Тогда растёт поток сообщений; эпизод формально найден, но оператор не успевает выделить реальный риск. Высокий recall завершённых клипов может сопровождаться неприемлемым timely recall. Это инженерные failure modes, не измеренные эффекты наших кандидатов.

### Предлагаемая процедура жёлтого/красного канала

1. Для каждого сценария владелец процесса определяет последствие пропуска, необходимую реакцию и последний полезный момент уведомления; цвет следует этим свойствам, а не confidence модели. Высокая уверенность в неопасном состоянии не делает его красным. Принципы полезного сигнала и времени ответа берём из HSE [S008]; чисел из process industry не заимствуем.
2. Красный канал: искать максимальную нижнюю доверительную границу timely recall при согласованных верхних границах ложной нагрузки и задержки. Меньший confidence/более короткое подтверждение допустимы как гипотеза для теста, не как универсальное правило. Автоматическая реакция и safety certification данным исследованием не подтверждаются.
3. Жёлтый канал: допускается более длительное подтверждение, hysteresis и накопление свидетельств, если это согласуется с временем полезного ответа. Выбирать ограничение FP/час или нагрузку на обзор, проверяя нижнюю границу event recall. Жёлтые записи в журнале и прерывающие оператора уведомления считать отдельно.
4. Совместный бюджет каналов: много жёлтых сигналов может мешать красным. Проверять общий поток, пики и время доставки красного под нагрузкой; не тестировать цвета только изолированно.
5. Настройки `{threshold, persistence, hysteresis, cooldown, rearm, fps, resolution, model/runtime}` замораживаются как одна рабочая точка. Цвет не заменяет количественное описание.

Если известны реальные цены, возможна `ExpectedLoss/time = Σ C_FN,c · missed_events_c/time + Σ C_FP,c · false_alerts_c/time + delay_cost + operator_load_cost`. Цены должны прийти от анализа риска и процесса; `Fβ` подразумевает выбранный компромисс, но сам по себе не обосновывает его. Ошибки разных последствий не складывать с самовольными баллами. При неизвестных ценах оставлять вектор метрик и Парето-фронт. Кроме FN нужно учитывать цену пропуска нового события из-за cooldown и цену старого активного сигнала, скрывающего новый риск.


## F025 — W1-01: Доверительные интервалы и объём доказательства

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Доверительные интервалы и объём доказательства»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S011, S012, S013.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F025.** В отчёте обязательны сырые `TP/FN/FP`, число GT событий, camera-hours, число независимых площадок/камер/дней, method и confidence level. Wilson — разумный описательный вариант для доли, exact binomial — вариант для малых чисел/краёв; нормальная формула `p ± z√p(1−p)/n` у 0/1 ненадёжна [S011, S012]. Это предполагает подходящие независимые trials: сто соседних кадров одного падения не являются ста испытаниями.

Для редких ложных сообщений начать с exact Poisson rate interval по count `k` и exposure `H` [S013]. Наше математическое следствие при `k=0` и одностороннем confidence `1−α`: верхняя граница интенсивности `λ_U = −ln(α)/H`. Поэтому «0 FP» обязательно сопровождается H; это не доказательство нулевой будущей интенсивности. Двусторонняя верхняя граница использует `−ln(α/2)/H`; не путать её с односторонней. Аналогично при всех N успешных независимых событиях односторонняя exact нижняя граница recall — `α^(1/N)`, а не 1. Формулы — вывод из Poisson/binomial вероятности нулевых ошибок; вычислительный эксперимент не выполнялся.

Реальные FP могут приходить пачками на одной пыльной камере: Poisson предполагает слишком простую независимую интенсивность. Проверять counts по camera/session/day, распределение и всплески; при зависимости использовать paired cluster bootstrap по независимым сессиям/площадкам для разности кандидатов и exposure-weighted rate. Синхронные камеры одного происшествия кластеризовать вместе. Это предлагаемая статистическая процедура, не результат применения. При одной камере/одной сессии честно сообщить отсутствие основания для CI на переносимость; bootstrap кадров не исправляет проблему.

Показывать pooled и per-camera rate, macro и наиболее проблемные камеры с exposure, не только среднее. Маленькие срезы будут иметь широкие интервалы; отсутствие различия не доказывает эквивалентность. Заранее фиксировать семейство основных критериев/срезов: множество послетестовых поисков «победителя» делает обычные nominal CI чрезмерно оптимистичными. Если недостаточно независимых красных событий — утверждать feasibility на доступных примерах, а не доказанную надёжность.


## F026 — W1-01: График принятия решений и независимость

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «График принятия решений и независимость»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Это последовательность зависимых решений, а не обещание длительности работ.

| Шаг | Вход | Решение/выход | Условие перехода |
|---|---|---|---|
| A. До настройки | Приоритетные сценарии, камера/зона, операторский ответ | Онтология эпизода, deadline, unknown/blind policy, primary metrics | Разметчики и разработчики одинаково понимают событие |
| B. До обучения/threshold sweep | Список оригинальных видео/сцен/камер/инцидентов | Grouped train, validation; optional SELECT; lockbox manifest с хешами | Нет соседних кадров и того же инцидента между независимыми частями |
| C. Development | train/validation и непрерывные hard negatives | Несколько полных конфигураций, event error audit, Pareto curves | Есть causal replay и наблюдаемая latency; LinQ runtime проверяется отдельной веткой |
| D. Выбор | SELECT, если реально есть отдельные группы | Одна замороженная система и рабочие точки каналов | Критерии и evaluator frozen; иначе validation — development и это явно сказано |
| E. Единственная итоговая оценка | Неоткрытый lockbox, frozen build на LinQ | Сырые журналы, metrics+CI, hardware/runtime record | Никакой настройки по lockbox; провал остаётся провалом текущей версии |
| F. Демонстрация | Замороженный результат и известные ограничения | README с областью применимости и проверяемыми утверждениями | Не заменять итоговые метрики красивым выбранным роликом |

Для заявления о новых камерах отделять camera/site целиком. Для заявления «та же камера, новая смена» допустим time split с достаточным разрывом и исключением одного физического эпизода/сцены, но это **другая, более узкая** независимость; не выдавать её за перенос на неизвестную площадку. Если одинаковые камеры/фон присутствуют в train и test, это явно known-camera protocol. Перекодирование, crop, augmentation или разные fps одного оригинала не создают независимый test.

На lockbox запрещены выбор checkpoint, confidence, rule persistence, zone polygons по ошибкам модели, ensemble, calibration, rearm и «один последний фикс». После любого такого изменения нужен новый неиспользованный lockbox или результат честно маркируется как development. Настройка зон на служебном camera calibration material возможна лишь если это заранее допустимый input протокола, независимо от test GT; точный контракт передать ветке калибровки.


## F027 — W1-01: Обязательные срезы

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Обязательные срезы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- Каждый сценарий и severity; короткие/длительные эпизоды; одиночные/повторные; первый эпизод после старта и новый после rearm.
- Камера, площадка, known/unknown scene; смена/время суток, освещение, пыль/пар/дым, окклюзия, исходный размер человека и малых объектов, плотность людей, ракурс. Числовые границы bins выбираются из данных и фиксируются до test.
- Похожие безопасные действия: наклон/работа на полу против падения, закрытая голова против отсутствия каски, телефоноподобные инструменты, проход по разрешённой дорожке, неподвижный отдых. Конкретный набор зависит от выбранных сценариев; не обещать их все без данных.
- Исполнение: число потоков, resolution/FPS, steady-state/warm-up, очередь, потеря кадров, сетевой сбой/восстановление, смена track ID, долгий cooldown, доставленные/потерянные уведомления.
- Short critical events и события во время очереди/перегрузки; худшие камеры, отдельные false positive bursts. У каждого среза публиковать размер и unknown exclusions.


## F028 — W1-01: Различающий эксперимент E1: что даёт подтверждение и отдельные рабочие точки

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Различающий эксперимент E1: что даёт подтверждение и отдельные рабочие точки»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**Вопрос.** Улучшает ли сценарное temporal confirmation/hysteresis полезную точность при сохранении своевременного обнаружения коротких красных эпизодов, либо оно просто скрывает трудные случаи? Можно ли отделить выигрыш детектора от выигрыша правил?

**Необходимые входы.** Доступные непрерывные видеозаписи с разрешённым использованием и timestamps; достаточно независимо размеченных положительных эпизодов и обычной работы, включая hard negatives; правила GT/deadline от экспертов; split manifest; доступный LinQ runtime и точная конфигурация сервера; журнал доставки и наблюдения. Требования к GPU-памяти, стоимости или длительности здесь не оцениваются. Vast.ai/3090 для этого протокола не обязательны: можно начать с имеющейся модели и replay её causal score traces; итоговый runtime всё равно измерять на LinQ. Никакой аренды не требуется и не произведено.

**Варианты.** A: текущая модель + единая фиксированная рабочая точка. B: та же модель + scenario/severity-specific threshold и confirmation с явным rearm. C: альтернативная модель при тех же допустимых правилах и входном бюджете, только если ветка моделей предоставит исполнимую LinQ-сборку. A/B изолируют вклад postprocessing; B/C — вклад модели. Не менять одновременно незадокументированные fps и зоны.

**Процедура.** (1) Двойная независимая разметка/разбор неоднозначностей и freeze GT до test. (2) На development replay sweep разумных конфигураций; диапазоны берутся из score traces, длительности событий и дедлайна, не из произвольной цели «accuracy». (3) Строить event recall–FP/hour и timely recall–FP/hour, кривую recall-within-delay и нагрузку/duplicates. (4) На SELECT выбрать точки по заранее согласованным ограничениям; сохранить все варианты, чтобы увидеть цену изменений. (5) Freeze build/config/evaluator. (6) Однократный causal realtime replay lockbox на LinQ в заявленном числе потоков, с реальной доставкой в UI; сохранить полные negative exposure и сбои. (7) Сравнить парные результаты по общим episode/session, CI с подходящим cluster unit; причины расхождений раскрыть без перенастройки.

**Артефакты.** `split_manifest` с группами/хешами/лицензиями видео; GT episodes+observable intervals; `model/runtime/config` версии и hashes; исходные scores/track traces; alerts и delivery timestamps; camera health intervals; matching table по каждому GT и alert; сводка по классам/срезам/CI; DET-подобные и delay-кривые; LinQ hardware/SDK/операции/queue/FPS record; freeze record. Это предложенный список, файлы эксперимента в этой ветке не созданы.

**Интерпретация исходов.** B сохраняет своевременный recall и снижает FP/час/дубли — основание выбрать B при заданных ограничениях. B снижает FP, но теряет short-red или задерживает сообщение за deadline — нет основания объявлять его лучше; изменить правила только на development. C повышает mAP, но не улучшает downstream события — не приоритет для ограниченного времени. Любой кандидат не держит LinQ runtime — не финальный, даже если offline event score выше. Нет достаточного negative exposure/независимых событий — результат неопределённый, нужна более узкая формулировка scope.

**Что успех не докажет.** Не докажет safety integrity/certification, нулевой риск, перенос на неизвестные камеры, реальные редкие события без постановки, пригодность для иных расстояний/погоды, многочасовую устойчивость за пределами записей или способность оператора вовремя вмешаться. Последнее требует отдельной проверки response workflow; быстрый alert — необходимая часть, а не доказательство предотвращённого происшествия.


## F029 — W1-01: Отрицательные результаты, неизвестное и передачи

- Происхождение/locator: [W1-01](_WORK/W1_01.md), раздел «Отрицательные результаты, неизвестное и передачи»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F029 — чего первоисточники не дают.** Не найдено универсального приемлемого FP/камеро-час, confidence или confirmation для всех промышленных нарушений. Популярные process-control числа по alarm load относятся к операторской позиции и конкретной организации, а не одной CV-камере. Ни COCO, ни ActivityNet AP не содержит полного контракта своевременного полезного уведомления. ActEV TFA не решает счётчик UI-дубликатов. Источники не обосновывают автоматический перенос precision между balanced clips и deployment.

Передать соседним исследованиям:

- **Данные/splits:** непрерывный negative exposure, grouping по incident/site/camera/session; какие события действительно независимы; политика staged clips; лицензии; неизвестная prevalence.
- **Сценарии/веса:** точное определение onset/end/observable, нужны ли признаки взаимодействия/причины; минимальная полезная длительность; support/unknown для видимых PPE. Нужен перечень обещанных классов, не полный каталог весов здесь.
- **LinQ/квантование:** causal timestamps, фактические SDK/runtime/hardware/model hashes, inference+queue+delivery latency, accuracy после экспорт/quantization на том же frozen evaluation; не выводить speed из RTX.
- **Калибровка:** проверяемая семантика зон/расстояний и протокол допустимой per-camera настройки до test; ошибки геометрии должны иметь собственные срезы.
- **Операторский продукт:** полезное действие для каждого цвета, destination и момент получения alert, бюджет нагрузки и правила escalation/rearm/ack. Оценка одного сообщения на эпизод включает реальную доставку.

Точные вопросы команде: какие последствия/времена ответа различают красный/жёлтый; что означает «несколько секунд» по каждому приоритетному сценарию; где определён момент доставки; сколько независимых cameras/sites/incidents реально доступно; есть ли непрерывный фон с проверяемым GT; есть ли журнал camera health; кто фиксирует GT и кто хранит lockbox. Без ответов можно строить кривые и показывать feasibility, но нельзя честно объявить систему прошедшей произвольный accuracy threshold.

Итог ветки: выбрать ограниченный набор сценариев и **своевременное событийное качество при известной нагрузке и покрытии**; заморозить протокол до сравнения; хранить все знаменатели и failure cases. Это исследовательская рекомендация, а не выполненная валидация.


## F030 — W1-02: Решение прежде деталей

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Решение прежде деталей»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S015, S016, S017, S018, S019, S020, S022, S023, S025, S026, S027, S028.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


**F030 — Начать с одного сквозного baseline `YOLO26s`, а не с максимального COCO AP.** Конкретный код: Ultralytics **8.4.184**, commit `de290d865035acbfa4bb24cc88960d8b52c26e45`; веса `yolo26s.pt` release assets `v8.4.0`. Параллельный по смыслу, но не обязательно одновременно запускаемый кандидат: **D-FINE-M**, затем **RF-DETR-M/L**. Выбор окончательный только после target-данных и проверки SDK LinQ. Быстрый baseline означает минимальное число интеграционных неизвестных для команды, а не доказанную скорость на LinQ. Если AGPL-путь неприемлем для выбранной формы поставки, запасной CNN baseline **YOLOX-s**; его актуальный потолок качества ниже опубликованных новых семейств, зато есть простой исходный код и экспорт. [S015, S016, S017, S018, S019, S026]

**F030 — Основной ceiling-челленджер — D-FINE-M/L; альтернативный переносимый по экосистеме, но не доказанно по LinQ — RF-DETR-M/L.** D-FINE имеет COCO и Objects365→COCO checkpoint-ветки; эффект дополнительного pretraining нельзя выдавать за эффект одной архитектуры. RF-DETR требует фиксации современной модели Large: `rf-detr-large-2026.pth`, а не legacy `rf-detr-large.pth`. Transformer-челленджера выбирать только после проверки операторов и postprocessing. [S017–S022]

**F030 — RT-DETRv2-S с `discrete` sampling полезен как отдельный эксперимент совместимости.** Он заменяет bilinear sampling на индексирование, но из этого не следует поддержка TPU. Существуют отдельные DSP-веса; переключить флаг у обычных весов и считать результат эквивалентным нельзя. RT-DETRv4 — более новый кандидат с HGNetv2 inference и обучающей VFM-веткой, но воспроизведение полного teacher-рецепта избыточно до отбора базовых моделей. [S023–S025]

**F030 — Не выбирать по слову «новый» или «NMS-free».** YOLO27 на дату доступа только preview, весов и package support нет. У текущего YOLO26 `nms=False` действительно включает one-to-one путь **в прочитанной версии exporter**, но это не универсальная семантика для других версий YOLO: там могут различаться `end2end` и включение NMS. Некоторые backend-ветки затем принудительно выключают end-to-end. У DETR всё равно остаются sigmoid/top-k/boxes decoding и преобразования координат. [S016, S020, S027]

**F030 — COCO pretrained не покрывает нужную онтологию безопасности.** Есть `person`, несколько транспортных классов и `cell phone`; нет отдельных классов каски, жилета, страховочной привязи, промышленного погрузчика, сигареты и открытого пламени. Прогноз `truck` на погрузчик нельзя считать валидированным распознаванием техники. Наличие телефона не доказывает его использование, bbox человека не доказывает падение или опасное сближение. Нужны target-метки и последующая событийная логика. [S028; вывод исследователя]


## F031 — W1-02: Что диктует кейс

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Что диктует кейс»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


По `_WORK/CASE_NOTES.md` (визуальные наблюдения root, не мои повторные просмотры PDF): p5 — маленькие СИЗ, сложная среда и задержка несколько секунд; p7 — качество выше количества сценариев, один инцидент → одно уведомление; p13 — обязательны инференс LinQ и измерение скорости. Поэтому detector AP, event recall, FP/camera-hour и event-to-alert latency — разные уровни оценки. Слова экспертов о приоритете accuracy не задают численную формулу и не снимают ограничение задержки.


## F032 — W1-02: Фиксация версий

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Фиксация версий»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


| Семейство | Исходный репозиторий и зафиксированная ревизия | Дата commit UTC / статус |
|---|---|---|
| Ultralytics YOLO26 / YOLO11 | [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics/tree/de290d865035acbfa4bb24cc88960d8b52c26e45), `de290d865035acbfa4bb24cc88960d8b52c26e45` | 2026-10-23 15:51:48; `__version__=8.4.184`, не утверждаю совпадение wheel с этой ревизией |
| D-FINE | [Peterande/D-FINE](https://github.com/Peterande/D-FINE/tree/956d1709314c2c6a4df6f34de232054578a7449f), `956d1709314c2c6a4df6f34de232054578a7449f` | 2026-08-19 15:08:14; серия впервые выпущена 2024-10-18 |
| RF-DETR | [roboflow/rf-detr](https://github.com/roboflow/rf-detr/tree/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb), `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb` | 2026-10-16 05:38:07; `pyproject.toml=1.12.0.dev`, это development snapshot |
| RT-DETRv2 | [lyuwenyu/RT-DETR](https://github.com/lyuwenyu/RT-DETR/tree/df2a96c8c3a098567a1149bf0248da6efe6d495d), `df2a96c8c3a098567a1149bf0248da6efe6d495d` | 2026-10-09 07:38:10; v2 опубликован 2024-07-24 |
| RT-DETRv4 | [RT-DETRs/RT-DETRv4](https://github.com/RT-DETRs/RT-DETRv4/tree/55fefaaed7efe2a5f72d0a18fd4e05965e35c292), `55fefaaed7efe2a5f72d0a18fd4e05965e35c292` | 2026-07-06 08:42:59; code/config/checkpoints объявлены 2025-11-17 |
| YOLOX | [Megvii-BaseDetection/YOLOX](https://github.com/Megvii-BaseDetection/YOLOX/tree/6ddff4824372906469a7fae2dc3206c7aa4bbaee), `6ddff4824372906469a7fae2dc3206c7aa4bbaee` | 2025-06-08 03:52:54; исходная работа 2021 |
| DEIMv2 | [Intellindust-AI-Lab/DEIMv2](https://github.com/Intellindust-AI-Lab/DEIMv2/tree/f005f50ce565e63f6c298feccb51901a98c3d035), `f005f50ce565e63f6c298feccb51901a98c3d035` | 2026-10-23 10:47:06; серия объявлена 2025-09-26 |
| EdgeCrafter | [Intellindust-AI-Lab/EdgeCrafter](https://github.com/Intellindust-AI-Lab/EdgeCrafter/tree/d8752b75c9beaecfcdd0e5cd207bae3b6946ae23), `d8752b75c9beaecfcdd0e5cd207bae3b6946ae23` | 2026-10-22 10:47:44; резервное направление, не основной shortlist |

Один SHA не фиксирует Python/CUDA/ONNX dependencies и не фиксирует изменяемые внешние файлы весов. Для воспроизведения необходимо сохранить resolved environment и SHA256 реально полученного checkpoint. Ниже для YOLO приведены опубликованные GitHub digest из метаданных release, для RF-DETR — MD5, записанные авторами в исходнике; самостоятельно байты не проверялись.


## F033 — W1-02: Сопоставимый shortlist

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Сопоставимый shortlist»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S015, S016, S017, S019, S021, S023, S025, S026, S029, S030.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


В таблице **только опубликованные числа**, не наши результаты. AP — COCO detection AP50:95 val, кроме явно отмеченного. Условия скорости приведены отдельно. Нельзя вычислять из этой таблицы ожидаемую скорость на LinQ или заявлять ранжирование по устойчивости к пыли/телефонам.

| Кандидат / роль | Input | Reported AP | Params | Reported inference | Условие включения |
|---|---:|---:|---:|---:|---|
| YOLO26s / основной быстрый baseline | 640² | 48.6 dense / 47.8 e2e | 9.5M fused | T4 TensorRT10 2.5 ms | AGPL/выбранная лицензия приемлема; пройти экспорт и target data |
| YOLO26m / шаг качества в той же экосистеме | 640² | 53.1 dense / 52.5 e2e | 20.4M fused | T4 4.7 ms | Если s упирается в качество, а m проходит реальные ограничения |
| D-FINE-M COCO / основной challenger | 640² | 52.3 | 19M | T4 FP16 TRT10.4, 5.62 ms | Проверка attention/sampling и postprocessing |
| D-FINE-L COCO / следующий ceiling | 640² | 54.0 | 31M | там же 8.07 ms | Обоснованный gain на SELECT и допустимый LinQ p95 |
| D-FINE-M/L O365→COCO / отдельная init-ветка | 640² | 55.1 / 57.3 | 19M / 31M | 5.62 / 8.07 ms | Отдельно учесть происхождение и условия Objects365 |
| RF-DETR-M / альтернативный challenger | 576² | 54.7 | 33.7M fused | T4 FP16 TRT batch1, 4.4 ms | Зафиксировать current API, raw outputs и dependencies |
| RF-DETR-L 2026 / ceiling | 704² | 56.5 | 33.9M fused | там же 6.8 ms | Не перепутать с legacy Large; LinQ gate обязателен |
| RT-DETRv2-S / контрольный DETR | 640² | 48.1 | 20M | T4 FP16 TRT≥8.5.1 batch1, 217 FPS | Не считать FPS end-to-end video throughput |
| RT-DETRv2-S DSP / кандидат на operator workaround | 640² | 47.4 | семейство R18 | Для DSP отдельно скорость не установлена | Использовать отдельный checkpoint и square input на первом тесте |
| RT-DETRv4-M / резерв нового CNN DETR | 640² по config-пути | 53.7 | Не фиксировалось | README T4 5.91 ms; полный stack для этой строки не установлен | Не начинать teacher-training до baseline gate |
| YOLOX-s / запасной CNN baseline | 640² | 40.5 | 9.0M | README V100 9.8 ms | Сравнение T4/V100 напрямую недопустимо |

Источники: YOLO числа [S016], D-FINE [S017], RF-DETR [S019], RT-DETRv2 [S023], RTv4 [S025], YOLOX [S026]. RF-DETR README описывает внутренний авторский benchmark SAB на полном val2017; это сильнее одного рекламного графика, но остаётся измерением поставщика, а не независимым воспроизведением. Для dense/e2e YOLO скорость дана e2e-пути; нельзя сочетать AP dense и latency e2e в одну «точку».

### Контракт конкретных весов

| Модель | Точный checkpoint URL / идентификатор | Защита от подмены версии |
|---|---|---|
| YOLO26s | [v8.4.0/yolo26s.pt](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt) | GitHub metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b`; updated 2026-01-13 19:59:22 UTC |
| YOLO26n — только если s не проходит ресурсный gate | [v8.4.0/yolo26n.pt](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n.pt) | metadata SHA256 `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef` |
| YOLO26m | [v8.4.0/yolo26m.pt](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26m.pt) | metadata SHA256 `401cea9ab23ad19246ff7744859816bc599f350e93c9dd30367b6f0a0745d0b7` |
| D-FINE-M COCO | [dfinev1.0/dfine_m_coco.pth](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth) | release+filename; SHA256 не установлен |
| D-FINE-L COCO | [dfinev1.0/dfine_l_coco.pth](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_l_coco.pth) | То же |
| D-FINE-M O365→COCO | [dfinev1.0/dfine_m_obj2coco.pth](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_obj2coco.pth) | Отдельная ветка pretraining |
| D-FINE-L O365→COCO | [dfinev1.0/dfine_l_obj2coco_e25.pth](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_l_obj2coco_e25.pth) | Именно `e25`, а не произвольный L |
| RF-DETR-M | [medium_coco/checkpoint_best_regular.pth](https://repo.roboflow.com/rfdetr/medium_coco/checkpoint_best_regular.pth), локальное имя `rf-detr-medium.pth` | MD5 в pinned source `7223f764a87b863f02eb8d52bf0ce2ee` |
| RF-DETR-L 2026 | [rf-detr-large-2026.pth](https://repo.roboflow.com/rfdetr/rf-detr-large-2026.pth) | MD5 `5cb72153541cbcb9aa6efa26222acc75` |
| RF-DETR-S — меньший резерв | [small_coco/checkpoint_best_regular.pth](https://repo.roboflow.com/rfdetr/small_coco/checkpoint_best_regular.pth) | MD5 `fb37061c1af7bace359c91b723a8d5c1` |
| RT-DETRv2-S | [v0.2/rtdetrv2_r18vd_120e_coco_rerun_48.1.pth](https://github.com/lyuwenyu/storage/releases/download/v0.2/rtdetrv2_r18vd_120e_coco_rerun_48.1.pth) | Отдельно от более старого `v0.1/...120e...` |
| RT-DETRv2-S DSP | [v0.1/rtdetrv2_r18vd_dsp_3x_coco.pth](https://github.com/lyuwenyu/storage/releases/download/v0.1/rtdetrv2_r18vd_dsp_3x_coco.pth) | Не использовать веса S rerun с подменённым sampling без оценки |
| RT-DETRv4-M | [Google Drive file 1O-YpP4X-quuOXbi96y2TKkztbjroP5mX](https://drive.google.com/file/d/1O-YpP4X-quuOXbi96y2TKkztbjroP5mX) | Авторская ссылка; доступность бинарника и hash не проверялись |
| YOLOX-s | [0.1.1rc0/yolox_s.pth](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth) | Не путать с legacy `0.0.1` |

### Лицензия кода отдельно от весов

**F033.** У YOLO26 авторские docs явно распространяют AGPL-3.0/Enterprise на код, модели и документацию. Это не permissive baseline. У RF-DETR Apache-designated N/S/M/L checkpoints прямо включены в Apache-2.0; Plus-компоненты и detection A/F/P/XL/2XL — PML 1.0, и общее утверждение «весь RF-DETR Apache» неверно. [S015, S019, S021]

У D-FINE, RT-DETRv2, RT-DETRv4, YOLOX прочитаны project LICENSE Apache-2.0. Публичные checkpoint-ссылки найдены в официальных model zoo, **но отдельный юридический manifest для каждого бинарника не установлен**. Репозиторная лицензия не является достаточным доказательством отсутствия ограничений исходных datasets/pretrained backbone. У D-FINE pinned README прямо предупреждает о terms Objects365 для `*_obj365`/`*_obj2coco`. Команде необходимо сохранить исходные notices и provenance, а коммерческую пригодность не объявлять на основании одной таблицы AP.

У текущих **DEIMv2 и EdgeCrafter** собственная лицензия: материалы и веса для non-commercial purposes; commercial use требует отдельной лицензии, third-party материалы сохраняют свои условия. Рекомендация: исключить их из основного переносимого продуктового shortlist до решения о допустимой цели использования. Это не заключение о том, что конкретное участие в хакатоне запрещено: такой вывод из текста автоматически не следует. [S029, S030]


## F034 — W1-02: Fine-tuning: что реально воспроизводимо, а что только предлагается

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Fine-tuning: что реально воспроизводимо, а что только предлагается»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S022.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


Ниже **не готовые команды запуска на 3090**. Это проверенные entry points и компоненты рецепта. Неизвестные batch size, epochs и LR для target-данных должны определяться валидированным протоколом, а не копированием COCO-рецепта.

| Семейство | Проверенный рецепт / путь | Что переносить в target run | Что нельзя обещать |
|---|---|---|---|
| YOLO26 | `YOLO("yolo26s.pt").train(data=..., imgsz=640, ...)`; pinned docs; архитектура P3–P5 | Код revision, веса, class mapping, augmentation, optimizer, seed, image-size | Самая новая `pip install ultralytics` завтра не тот же рецепт; `coco8.yaml` не target dataset |
| D-FINE-M | `configs/dfine/dfine_hgnetv2_m_coco.yml`; custom config family; `train.py -c ... --use-amp -t checkpoint` | Вложенные include, HGNetv2 B2, 4 decoder layers; AdamW backbone LR 2e-5, base 2e-4; custom class config | COCO `epochs:132` и augmentation stop120 не рекомендованы автоматически для маленького target набора |
| D-FINE O365 | Отдельные `configs/dfine/custom/objects365/...obj2custom.yml` | Отдельный init factor, условия данных, корректный remap head | Прирост COCO AP не гарантирует прирост harness/phone recall |
| RF-DETR | `[train]` extra; `RFDETRMedium().train(dataset_dir=..., ...)`; COCO JSON/YOLO; current docs [S022] | Явный pretrained file, input resolution, selected class layout; physical batch отдельно от accumulation | `batch_size="auto"` есть в snapshot, но не доказательство fit/throughput; snapshot `1.12.0.dev` требует smoke gate |
| RT-DETRv2 | `rtdetrv2_pytorch/tools/train.py -c ... -t ... --use-amp`; S config `rtdetrv2_r18vd_120e_coco.yml` | Включаемые yaml, `remap_mscoco_category` для custom классов, optimizer, sampling | Пример `torchrun` на 4 GPUs не соответствует нашему плану 1–2 GPUs |
| RT-DETRv2 DSP | `rtdetrv2_r18vd_dsp_3x_coco.yml`, `cross_attn_method: discrete`, `epoches:36` | Отдельный checkpoint/config pair | Нельзя заменить continuous sampling без fine-tuning/валидации |
| RT-DETRv4 | `configs/rtv4/rtv4_hgnetv2_m_coco.yml`; README training teacher DINOv3 | Для первого target fine-tune оценить необходимость teacher отдельно | Полный published recipe требует дополнительных VFM весов/условий; не рекомендую воспроизводить его ради baseline |

**F034 — Память неизвестна до пробного шага на реальной машине.** Параметры, размер checkpoint и FLOPs не являются peak training VRAM. Нет подтверждённой таблицы fit выбранных target-рецептов в 24GB RTX3090. 2×24GB не дают автоматически 48GB доступной памяти для одной реплики DDP. Предлагаемая процедура: один GPU, минимальный physical batch, forward/backward/optimizer+EMA, затем validation; измерить allocated/reserved peak, подобрать batch и зафиксировать accumulation. После этого решать, нужен ли второй GPU. Снижение batch и checkpointing может менять training behavior/скорость; накопление градиентов не делает BN эквивалентным большому physical batch. Не заказывать Vast до экспортного gate и определения объёма данных. [Методическая рекомендация; не эксперимент]


## F035 — W1-02: Граф и postprocessing: конкретные риски для W1-16

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Граф и postprocessing: конкретные риски для W1-16»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S016, S018, S020, S021, S024.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


### YOLO26: различать ветку головы, embedding NMS и backend override

В pinned `exporter.py`, участок `Exporter.__call__` около строк 721–733 (локатор искать по `model.end2end = self.args.nms is False`): явное `nms=False` устанавливает end-to-end, если модель его поддерживает. Затем отдельные форматы (`rknn`, `ncnn`, `executorch`, `paddle`, `imx`, `edgetpu`, `qnn`) его выключают; LiteRT INT8/W8A16 тоже отключает эту ветку. Значит **на этом SHA для ONNX YOLO26 выбор one-to-one связан с `nms=False`, но сохранение one-to-one при иной конверсии проверяется отдельно**. Не переносить эту семантику на старые Ultralytics версии. [S020]

Для ONNX smoke-заявки предложить два раздельных артефакта: `format="onnx", imgsz=640, batch=1, dynamic=False, nms=False` и dense/head с документированным external NMS. Проверить фактические graph input/output и operators, а не только флаги. `nms=True` — request embedded NMS там, где поддержан; отсутствие embedded NMS само по себе не доказывает one-to-one. Published YOLO26 таблица отдельно даёт dense/e2e AP. [S016, S020]

Для dense custom класса меняется число каналов; нельзя жёстко закрепить `(1,84,8400)` для PPE-head. Для e2e тоже проверить реальный max_det/output, class IDs и scaling. TopK/Gather/Mod могут оказаться важнее NMS для компилятора. Нет данных, что LinQ — Coral Edge TPU: одно слово TPU не разрешает выбирать `format="edgetpu"`.

### D-FINE / RT-DETR: ONNX есть, полностью статического target-рецепта нет

Pinned D-FINE export script включает `cfg.model.deploy()` и `cfg.postprocessor.deploy()`, два входа `images` и `orig_target_sizes`, выходы `labels/boxes/scores`, opset16. Default dummy tensor **batch32**, batch axis объявлен dynamic. Это плохой default для первого TPU smoke при предполагаемом batch1; нужно создать отдельную target-адаптацию и записать diff, batch1/fixed dimensions и parity. RT-DETRv2 exporter использует dummy batch1, но тоже dynamic batch и два входа/opset16. Ни `onnx.checker`, ни успешный TensorRT build не доказывают компиляцию LinQ. [S018, S024]

RT-DETRv2 sampling default использует `F.grid_sample`; `discrete` путь использует integer coordinates/indexing. В pinned utils рядом с discrete имеется комментарий `FIX ME? for rectangle input`; начальный smoke вести на квадратном input и отдельной проверкой обсчитать несquare transform. DSP устраняет один класс операторных рисков, добавляет другие и не гарантирует полную TPU offload. [S024]

### RF-DETR: raw contract отличается от D-FINE

Pinned ONNX docs: `dets` — normalized cxcywh, `labels` — raw logits. Требуются sigmoid, class-layout-aware background handling и восстановление xyxy. Выходы сопоставлять **по именам**: при трёх custom classes ширина logits=4 совпадает с шириной bbox, и heuristic «последняя размерность=4 → boxes» ломается. Для official sparse COCO не отбрасывать последний logit автоматически; custom contiguous mapping имеет иную семантику. Объявить class schema в manifest. [S021]

Проверка raw graph vs graph+CPU postprocess должна идти отдельно. NMS-free не означает, что alerts не надо deduplicate, и не исключает ошибки нескольких query/class pairs. У LinQ необходимо измерить neural kernel, transfer, preprocessing/postprocessing и сквозную задержку. Quantization recipe и calibration остаются W1-16; готовых гарантий переносимости здесь нет.


## F036 — W1-02: Мелкие объекты и сложный фон

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Мелкие объекты и сложный фон»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S015, S017.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


**F036 — Увеличение общего AP не является свидетельством качества на малых СИЗ.** COCO AP_small относится к собственной размерной категории COCO; после downscale телефона из 1920×1080 в 640² его линейный размер меняется. Нужно измерять bbox width/height до и после preprocessing и отдельно считать recall для своих пиксельных диапазонов. Локальная каска на тёмном фоне и COCO bicycle — разные задачи.

Предлагаю сравнить три вмешательства **на одних данных, не одновременно менять всё**: (а) baseline whole-frame 640; (б) увеличенный whole-frame input в допустимой для каждой архитектуры кратности; (в) person/zone crops с фиксированным бюджетом crop count. Не объявлять 1280 универсально поддержанным размером RF-DETR: patch/window constraints и positional embeddings проверяются по выбранному config. Для cascade считать потери crop proposal: если person detector пропустил человека, PPE-stage не восстановит объект. Whole-frame stage и crops оба должны иметь допустимый LinQ neural path; GPU teacher может быть только training/offline-инструментом.

P2-варианты YOLO26 существуют как YAML-архитектуры без опубликованных scale-specific P2/P6 pretrained weights. Это исследовательская ветка, а не готовое улучшение baseline. У D-FINE demo-видео заявлена устойчивость к плотной толпе/blur; оно отобрано авторами и не является контролируемым тестом пыли, ночи или phone use. [S015, S017]

Целевой hard-negative набор должен включать пустые рабочие зоны, руку у лица без телефона, рации/инструменты, отражения/плакаты с людьми, жёлтые объекты вместо касок, частично видимые головы, дальних людей, движущиеся тени и парковку техники. Эти категории предложены как план сбора, а не утверждение о наличии готового dataset. На уровне frames оценивать class-wise PR и фоновые FP, на уровне видео — FP/camera-hour и event recall. На multi-label PPE нельзя превращать `unknown/occluded` в `no_harness`.


## F037 — W1-02: Альтернативы и отрицательные находки

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Альтернативы и отрицательные находки»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S015, S016, S019, S021, S027, S029, S030, S031, S032.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


**F037.** DEIMv2-S/X — технически сильные исследовательские альтернативы (paper v4: 50.9/57.8 AP; 9.71/50.3M). Но собственная лицензия и DINOv3 lineage снижают их приоритет для скорого переносимого результата. README указывает TensorRT≥10.6 для FP16 stability; на 2026-10-22 исправлен подсчёт attention FLOPs. Поэтому старый screenshot GFLOPs не надо использовать для затрат/скорости. [S029, S031]

EdgeCrafter — ещё более новый сосед: ECDet-M 54.3 COCO / 56.7 с O365, input640, T4 FP16 TRT10.6 batch1. Но те же non-commercial условия, дополнительный стек и отсутствие target evidence не оправдывают расширение первого сравнения. Точный резервный checkpoint: [edgecrafterv1/ecdet_m.pth](https://github.com/capsule2077/edgecrafter/releases/download/edgecrafterv1/ecdet_m.pth); config `ecdetseg/configs/ecdet/ecdet_m.yml`. [S030]

YOLO11 остаётся разумным резервом уже знакомой команде экосистемы, если реальная интеграция на конкретном SDK окажется проще. Нет оснований начинать миграцию только ради свежести. YOLO27 исключён: docs preview прямо говорят, что веса и package support ещё отсутствуют. [S027]

Open-vocabulary teacher/grounding-модели полезны как lead для разметки, но не выбраны как финальный инференс: их текстовые промпты не заменяют target validation и сами по себе не дают класс страховочной привязи нужной надёжности. RF-DETR paper рассматривает domain adaptability; это не доказательство преимущества на наших камерах. Полный подбор behavioral weights/datasets передан соседним исследователям. [S032; рекомендация]

**Противоречия источников.** У RF-DETR разные авторские live-страницы дают разные параметры и метрики Large: одна модельная страница ещё показывает около 129M/legacy Large, современный config — 33.9M и `large-2026`. Использовать pinned config+checkpoint, не смешивать таблицы. У Ultralytics YAML params выше fused inference counts, это объясняется удалением unused branch и folding; не считать расхождение свидетельством VRAM-экономии. У YOLO26 dense AP выше e2e AP, тогда как speed обычно e2e: headline «48.6 AP за 2.5ms» без пояснения путей некорректен. [S015, S016, S019, S021]


## F038 — W1-02: Дискриминирующий эксперимент, ещё не выполненный

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Дискриминирующий эксперимент, ещё не выполненный»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


**Вопрос:** повышает ли D-FINE-M или RF-DETR-M полезный recall phone/PPE/person при фиксированном приемлемом количестве ложных событий относительно YOLO26s, после реального LinQ экспорта и при допустимой задержке? Отдельный подпункт: DSP RT-DETR действительно помогает компилятору без неприемлемой потери target recall?

**Входы и предварительные условия.** Нужны официальный SDK/compiler/operators/precision LinQ, точная модель TPU/CPU/RAM, доступный inference endpoint и лимиты, target taxonomy, camera/session manifest, размеченные positives и negatives, правила события и выбранные acceptance thresholds. Нужен разрешённый training GPU только после read-only анализа доступного оборудования и export gate. Не нужны NAS, ансамбль всех семейств или полное COCO/Objects365 training с нуля.

**Предварительно записать:** целевой event recall floor, допустимые FP/camera-hour и p95 alert delay по каждому сценарию, число потоков и качество видео. Эти значения определяет команда с организаторами; здесь чисел нет. Без этого нельзя честно объявить победителя.

1. **Split до извлечения кадров.** Train/VAL/опциональный SELECT/lockbox по исходному видео, сессии и камере. Если независимость по камере заявляется, камер/одинаковых сцен между split быть не должно. Если камер мало, честно назвать более узкий within-camera temporal тест; не имитировать cross-camera generalization. Не делить соседние кадры и crops одного frame между splits. Аудит near-duplicates и источников pretraining по мере доступности; загрязнение pretraining нельзя полностью исключить.
2. **Gate0, без target training.** Закрепить код/weights/hash/dependencies; выполнить на разрешённом окружении reference inference и static batch1 export с совпадающим preprocessing. На малом фиксированном контрольном наборе сравнить tensors/boxes/scores/class mapping до и после экспорта, случаи пустого кадра/нескольких объектов/трёх custom classes. Снять histogram операторов, compiler logs, CPU fallback. Невозможность neural execution LinQ — стоп для этого финального кандидата; можно сохранить его как offline teacher.
3. **Небольшой тренировочный smoke.** Каждый retained кандидат обучить на train до реального backward+validation+checkpoint. Записать peak VRAM, wall-clock по стадиям, physical/effective batch; никаких обещаний времени или fit до этого. В начальном сравнении не включать O365 и COCO init одновременно как будто это одна модель.
4. **Основное сравнение.** YOLO26s, D-FINE-M COCO и RF-DETR-M с одинаковыми train/VAL/SELECT, классами и бюджетом инженерного выбора. Использовать родной fine-tune recipe каждой семьи, записывать различия; «одинаковое число epochs» не обеспечивает одинаковый compute. Точки остановки заранее определить по VAL plateau/лимиту, не по lockbox. Для сравнения влияния pretraining добавить отдельную D-FINE O365 ветку только при наличии ресурса и разрешённого происхождения.
5. **Отбор и пороги.** На VAL выбирать training/checkpoint, на SELECT — семейство/input/crop/порог/temporal rule в заранее ограниченном наборе вариантов. Если SELECT нет, учитывать, что VAL одновременно training selection и model selection; не называть это независимым тестом. Порог выбирать под заданный FP budget, а не под максимум одного pooled F1.
6. **LinQ сравнение.** Провести parity и quality check после target conversion/quantization, затем single/multistream test; включить decoder/preprocess/transfer/postprocess/queue/event rule. Замерить warm-up отдельно, steady-state p50/p95/p99 latency, dropped frames, FPS каждого этапа и end-to-end event-to-alert. Нагрузка и sequence должны совпадать. Calibration только из разрешённой train/calibration части, не lockbox.
7. **Lockbox один раз после freeze.** Сохранить неизменяемый manifest модели, порогов, head mode, правил событий, export и кода. Запустить lockbox; не менять checkpoint/threshold по его ошибкам. Если тест провален — честно сообщить failure и для следующей итерации сформировать новый независимый test, а не «дотюнить» прежний.

**Метрики:** frame AP50:95/AP_small только как вспомогательные; class-wise recall/precision при заданном threshold, recall по размеру/occlusion/освещению, FN критических объектов, фоновые FP; event recall, event precision, FP/camera-hour, доля duplicated alerts, missed short events, задержка capture→alert. Для редких событий привести counts и интервалы неопределённости с группировкой по видео/камере; frame bootstrap соседних кадров даст ложную уверенность. Reporting intervals — передача методисту оценки.

**Артефакты:** source SHA и license notices; weight SHA256 и origin URL; environment lock/container digest; train/VAL/SELECT/lockbox manifest и dedup audit; config и seed; learning curves/checkpoint decisions; sampled error gallery; raw detections + timestamps; export graph/opset/input-output schema/operators; compiler/fallback logs; paired parity report; per-camera event ledger; resource/latency logs; неизменяемый final model manifest.

**Возможные решения:** (а) baseline проходит всё, challenger не даёт устойчивого gain — оставить baseline; (б) challenger даёт прирост event recall при FP budget и проходит latency/LinQ — выбрать его; (в) высокое reference quality, но conversion ухудшает rare classes — отклонить финальный вариант/исправить export и повторить на development data; (г) у всех провал tiny PPE — уменьшить scope/изменить input/crops/данные, не маскировать средним person AP; (д) compile невозможен — offline teacher и совместимый student, но отдельный эксперимент distillation потребуется.

**Успех не доказывает:** качество на новых заводах/камерах/ночных режимах; безопасность эксплуатации; causal behavioral recognition; корректность геометрических дистанций; масштабирование на иное число потоков; право коммерческого использования всех upstream datasets; отсутствие pretraining contamination. Нельзя объявлять эти свойства по COCO AP или одному демо-видео.


## F039 — W1-02: Передачи соседним ячейкам и открытые вопросы

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Передачи соседним ячейкам и открытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


- **W1-16 / LinQ:** точный TPU и SDK/compiler, fixed shape/operator support, grid sampling vs discrete indexing, TopK/Gather/Mod, fallback visibility, batch32 default D-FINE exporter, dynamic batch RTv2, raw class layout RF-DETR, benchmark dense/e2e одной головы. Нужен не ответ «ONNX поддерживается», а успешный target compile+parity+quality+latency.
- **Datasets/evaluation:** target ontology, annotation `unknown/occluded`, размерные срезы, камера/сессия split, provenance pretrained и Objects365; minimum positive counts для каждого сценария.
- **Training/Vast:** не арендовать по числу параметров; сначала retained family и smoke VRAM. Подтвердить наличие локального/организаторского ресурса; необходимость 1/2×3090 решать по измерениям и дедлайну. Цены не исследовались и не заявляются.
- **Video/event architecture:** person/tech/phone/PPE detections не события; сохранять пропуски, связывание человека с предметом, dedup и короткие критические действия. Увеличение crop count должно входить в общий бюджет потоков.
- **Calibration/geometry:** расстояния/опасные зоны/высота — отдельный handoff, не свойство detector AP.
- **Product/licensing:** допустимость AGPL поставки, нужное происхождение весов, отношение проекта к non-commercial лицензиям. В ходе исследования никаких запросов лицензиарам не отправлялось.


## F040 — W1-02: Граница достоверности

- Происхождение/locator: [W1-02](_WORK/W1_02.md), раздел «Граница достоверности»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.


Проверены доступность текста/исходников, published model zoo и metadata. Веса существуют как авторские ссылки, но кроме release metadata не проверялись бинарный download, hash совпадение и licensable provenance каждого файла. Не установлены target AP, устойчивость к среде, fit в 24GB, runtime на 3090, время обучения, совместимость LinQ, качество INT8 и цена Vast. Любое заполнение этих полей требует отдельного выполненного эксперимента. Shortlist — решение о порядке проверки, а не сертификат готового deployment.


## F041 — W1-03: Решение для команды

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Решение для команды»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S041.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Рекомендация F041:** начать с существующего person detector + tracker + временных правил, затем проверить добавочную пользу 17-точечного pose в контролируемом ablation. Pose особенно уместен для разделения поз «наклон / сидит / горизонтальный корпус», когда плечи, таз и ноги достаточно видимы. Он не устанавливает сам факт падения, бега, потери сознания или опасной работы возле машины по одному кадру. Причина — разные действия могут иметь одинаковую мгновенную проекцию тела. Это вывод об идентифицируемости события, а не утверждение, что single-frame классификаторы не существуют (контрпример S041).

**F041:** основной воспроизводимый исследовательский кандидат — **RTMPose-s 17 COCO points, 256×192, MMPose v1.3.2**, top-down от тех же боксов, что использует baseline. Модель m — второй кандидат только при недостатке качества s и подтвержденном бюджете LinQ. Не выбирать 133 точки рук/лица без отдельной причины: для данной проверки нужны крупные суставы, а мелкие детали в дальнем CCTV могут отсутствовать физически.

**F041:** не делать pose обязательным фильтром, без которого детектор запрещает тревогу. При плохом скелете состояние — `unknown`, сохраняются bbox/track и отдельная логика недостатка наблюдения. Иначе пропуски позы на самом падении превратятся в систематические false negatives. Приоритет — сравнение event recall, false alerts/camera-hour и задержки, а не COCO AP.

**F041:** для «человек рядом с оборудованием» pose — уточнение положения стоп/рук, но необходимы зона опасности, состояние машины и геометрия камеры. Пересечение проекций руки и машины не доказывает физический контакт. Для «неподвижно лежит» нужна история; для «без сознания» видеопоза вообще не является достаточным подтверждением.

Основание требований: `_WORK/CASE_NOTES.md`, пересказ прямого визуального чтения root, стр. 5/7/13 кейса: баланс качества, несколько секунд до тревоги, одно событие → одно сообщение, обязательный LinQ inference и измерение скорости. Я самостоятельно PDF не переинтерпретировал. CPU+TPU и акцент экспертов на accuracy — сообщения команды, конфигурация и официальная численная формула не установлены.


## F042 — W1-03: Карта решений: что наблюдаем и что можно утверждать

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Карта решений: что наблюдаем и что можно утверждать»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Все формулы/правила ниже — предлагаемые инженерные гипотезы, не опубликованные результаты на нашей задаче.

| Сценарий | Что дает один pose-кадр | Минимальное продолжение | Когда нужна action-модель или иной канал | Основной отказ |
|---|---|---|---|---|
| Наклон | Наклон проекции плечи→таз; углы бедра/колена | Устойчивость в течение заданного времени, положение в разрешенной/опасной зоне | Если нужно различить «поднимает груз / обслуживает / упал вперед» | Работа лицом к камере, укороченный торс, закрытый таз |
| Сидит / присел | Взаимное положение таза, колен, стоп; согнутые ноги | Последовательность перехода и контекст опоры | Для причины/допустимости позы, неоднозначной фронтальной проекции | Таз/колени закрыты столом, ящиком, спецодеждой |
| Лежит | Горизонтальная проекция тела и низкий торс, если видны | Ground/zone context, длительность, проверка наблюдаемости | Если нужно отличить работу под оборудованием, отдых, падение | Лежащий вдоль оптической оси может выглядеть коротким/вертикальным |
| Падение | Кадр может быть похож на фазу падения или лежащего | Переход из предыдущей позы, снижение положения, изменение ориентации, последующее состояние; отдельный сценарий «уже лежал при появлении» | Если простая временная логика не разделяет быстрый присед, намеренное укладывание, падение с сохранением частично вертикальной позы | Потеря track на ударе; падение за ограждение; медленное оседание |
| Бег | Согнутые конечности и фаза шага — лишь признаки-кандидаты | История перемещения + частота/ритм движений; время в секундах | Для различения ходьбы, бега на месте, резкого шага; RGB/action при сильной неоднозначности | Однокадровая фаза ходьбы совпадает с бегом; шагов не видно |
| Опасная близость к машине | Стопы помогают выбрать ground anchor; кисти — приближение конечности | Полигон/метрика, движение и статус машины, tracking | Для «работает / трогает / ремонтирует», состояния механизма и контекста | Перспектива, occlusion, отражения; нормальная рабочая операция |
| Неподвижность | Ничего о длительности | История движения при стабильной видимости и камеры | Для «потеря сознания» нужны иные признаки/проверка оператором | Замороженный поток, закрытый человек, tracker держит старый bbox |

**F042:** безопасные семантические имена выходов — `bent_posture`, `low_or_horizontal_posture`, `possible_fall_transition`, `persistent_low_posture`, `fast_motion_candidate`, `person_in_danger_zone`, `insufficient_pose`. Не превращать `persistent_low_posture` автоматически в медицинское утверждение.


## F043 — W1-03: Что в геометрии относительно устойчиво

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Что в геометрии относительно устойчиво»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Пусть `S=(shoulder_l+shoulder_r)/2`, `H=(hip_l+hip_r)/2`; все точки нужны с собственной валидностью. Для каждого признака хранить `value`, `valid`, исходные confidence, возраст последнего фактического наблюдения.

1. **Положение таза относительно плеч и наклон корпуса**: `theta=atan2(|Sx-Hx|, |Sy-Hy|)`. Перенос изображения не меняет угол; одинаковое масштабирование осей тоже. Но это угол **2D проекции**, не угол корпуса к земной вертикали. При наклоне камеры нужна ее геометрия; около нулевой длины проекции торса угол не определять.
2. **Нормированные расстояния**: `(joint_i-H)/s`, где `s` — надежный масштаб из прошлой устойчивой позы/длины корпуса. Снижают зависимость от crop и расстояния до камеры в пределах приближения, но не устраняют перспективу. Не делить на текущую высоту bbox во время падения: сама нормировка меняет смысл вместе с позой. Проверить альтернативы `s` на validation.
3. **Углы локтя/бедра/колена**: инвариантны к переносу и равномерному масштабу в плоскости изображения, но не к ракурсу, перспективе или закрытым суставам. Нельзя выдавать их за биомеханически точные 3D углы. Для сидения полезны только при достаточной наблюдаемости цепочки hip–knee–ankle.
4. **Крупные пары вместо головы/запястий**: для наклона предпочтительна ось плечи–таз; голова исчезает за каской/спиной, кисти слишком малы. Это приоритет проверки, а не доказанный рейтинг точности суставов на нашем домене.
5. **Временные разности**: скорость таза, изменение угла, продолжительность низкой позы; считать по реальным timestamp, не по номеру кадра. Разности чувствительны к jitter и identity switch; acceleration еще чувствительнее. Сглаживание только причинное, с учетом собственного запаздывания. Будущие кадры недопустимы при измерении online latency.
6. **Ground anchor**: видимые лодыжки могут быть лучше центра bbox для зоны на полу, но при закрытых стопах это неизвестно. Bottom-center bbox — отдельный fallback с собственной ошибкой. Нельзя молча подменять наблюденные стопы предсказанными.

**F043:** нет основания объявлять любой из этих признаков «устойчивым к дальности и occlusion вообще». Его алгебраическая инвариантность к resize не восстанавливает потерянные пиксели и не решает перестановку суставов между людьми. Ресайз маленького crop до 256×192 не создает новых наблюдений. Нужны срезы по исходной высоте человека в пикселях, ракурсу и видимости конкретных суставов; универсальный нижний порог роста человека из изученных источников не следует.

### Маска качества и отказ от решения

Не трактовать score keypoint как калиброванную вероятность правильного сустава. На validation проверить связь score с ручной ошибкой и с event error. У каждого правила отдельный набор требуемых точек: наклону достаточно надежного торса, коленному углу нужны три надежные точки. Порог «видны X из 17» сам по себе может принять неверный для данного правила скелет.

Проверять скачки длины костей внутри track, внезапный перенос таза, swaps лево/право и соседних людей; такие эвристики сигнализируют сомнение, а не исправляют человека автоматически. Пропуски — маска, не `(0,0)`. Допустимая короткая интерполяция только для непрерывности отображения/признака с явным флагом; она не доказывает отсутствие движения. Для подозрения на падение сохранять исходный clip и причину отказа pose.


## F044 — W1-03: Воспроизводимые кандидаты и границы рецепта

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Воспроизводимые кандидаты и границы рецепта»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S036, S038, S042.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


### A. Общий detector → top-down RTMPose: основной ablation

Зафиксирован **MMPose v1.3.2**, commit **`5408bc76f5b848cf925a0d1857899011d8c5b497`**, commit date 2024-07-12 (проверено GitHub API). Код S036 реализует person selection + bbox score + bbox NMS → `inference_topdown`; из него можно взять адаптер к уже имеющемуся детектору. Нужно сохранить отображение bbox→track_id, а не связывать скелеты по индексу массива после NMS.

Для кандидата s брать согласованную пару из pinned `projects/rtmpose/README.md`, **AIC+COCO, 17 points**:

- config: `projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-s_8xb256-420e_coco-256x192.py` в указанном commit;
- checkpoint URL: `https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-s_simcc-aic-coco_pt-aic-coco_420e-256x192-fcb2599b_20230126.pth`;
- перед фактическим использованием скачать утвержденным процессом, записать SHA-256 и проверить, что config соответствует этому checkpoint. Суффикс имени файла — не наш вычисленный полный hash;
- для m аналогичная строка model zoo: `rtmpose-m_simcc-aic-coco_pt-aic-coco_420e-256x192-63eb25f7_20230126.pth`. Не сравнивать смену s→m одновременно со сменой detector, train data и temporal window.

Pinned repository содержит также `configs/body_2d_keypoint/rtmpose/coco/rtmpose-s_8xb256-420e_coco-256x192.py`: просмотренный config фиксирует 17 выходов, `input_size=(192,256)` в порядке W,H, RGB conversion, mean/std и SimCC split ratio=2. **Не смешивать автоматически** одноименные configs из `projects/` и `configs/`: перед запуском раскрыть `_base_`, сверить модельную архитектуру и preprocessing. `256×192` в model zoo обычно H×W, что важно для адаптера.

Не давать demo весь CCTV кадр как «один человек». Аффинное преобразование crop и обратное преобразование keypoints должны учитывать padding/aspect ratio; для bbox из глобального изображения возврат координат обязателен. Оптимизация запуска только на ROI приемлема после проверки, что ROI не отрезает отрицательные примеры и сами события.

Лицензия кода MMPose в этом commit — Apache-2.0; `LICENSES.md` отдельно перечисляет EDPose/IDEA License 1.0, RTMPose там не выделен. **Отдельный явный grant для конкретного .pth и всех обучающих наборов в проверенных файлах не найден**. Не приписывать всем весам автоматически Apache-2.0: закрыть provenance/licensing перед дальнейшим распространением. Для Body7/Body8 это особенно важно из-за комбинированных данных. Они не выбраны главным кандидатом.

### B. Одностадийный pose вместо отдельного detector+pose

Альтернатива для простоты интеграции — **Ultralytics YOLOv8-pose**, зафиксированный код `v8.3.0` → commit **`6e43d1e1e5db72afbf686dee6745669bcb124b0a`**, annotated tag 2024-09-30. В этой версии pose docs описывают YOLOv8, не текущие YOLO26; live docs нельзя подставлять в старый рецепт. Выход включает boxes/keypoints, отдельный person detector для pose не нужен.

Обнаруженная деталь S042: `Keypoints.__init__` выставляет координаты точек с conf<0.5 в ноль. Угол из `keypoints.xy` без маски может поэтому описать луч к левому верхнему углу кадра. Проверить raw output/маскирование выбранной версии до собственного threshold sweep. Это конкретное чтение кода, не результат инференса.

Код pinned version — AGPL-3.0; официальная текущая лицензионная страница относит trained weights к AGPL-3.0 по умолчанию с коммерческим вариантом. Это заявленная политика правообладателя, не юридический вывод о конкретном проекте. Веса этой альтернативы не скачаны, hash не зафиксирован, поэтому **B — резерв, не полностью pinned deploy-рецепт**. Его выбор также меняет detector; отдельно учитывать, какая часть выигрыша от boxes, какая от keypoints.

### C. Bottom-up / более тяжелый pose

При большом числе перекрывающихся людей top-down порождает много crop и ошибки выбора тела внутри crop. Bottom-up избегает обязательного person detector, но требует связывать суставы и обычно более высокого пространственного разрешения. В первом эксперименте не включать новый стек: переход оправдан, если срез crowded критичен и A проваливается именно из-за proposal/association. Источник S038 показывает, что оба семейства имеют ошибки в толпе; bottom-up не является автоматическим решением occlusion.


## F045 — W1-03: Противоречия, отрицательные результаты и ограничения поиска

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Противоречия, отрицательные результаты и ограничения поиска»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S040, S041.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F045:** высокая precision single-frame «лежит» и точное распознавание события «упал» — разные задачи. S041 не опровергает необходимость истории для причинного различения падения и намеренного лежания: обученный prior может угадывать типичные положения, но одинаковые наблюдения остаются неоднозначными. В benchmark нужно разнести `fall_transition` и `already_lying`.

**F045:** скелет уменьшает зависимость downstream признаков от текстуры одежды/фона, но extractor остается RGB-моделью. Нет доказательства, что он устойчив к пыли, паровым заслонам, темноте, нетипичной PPE или неподвижному потоку. При occlusion модель может выдать правдоподобный, но не наблюденный сустав.

**F045:** не найден проверенный рецепт, гарантирующий LinQ TPU support для RTMPose/SimCC или YOLO pose. ONNX export и слово TPU не устанавливают совместимость. Передача в platform cell должна включать требования к preprocessing, SimCC decode, обратной геометрии и NMS; их CPU-стоимость входит в E2E.

**F045 — проверяемая численная несогласованность в S040:** в Table 3 для positive=Falling указаны TP=147, FN=4, FP=3+4=7. Собственный арифметический пересчет этой опубликованной таблицы дает precision `147/154=95.45%`, F1 `294/305=96.39%`; текст §4.4 сообщает 98.50% и 97.91%. Accuracy из таблицы `403/414=97.34%` совпадает с текстом. Это не наш эксперимент и не доказательство причин ошибки; это дополнительная причина использовать S040 как описание механизма, а не обещание метрик. XML таблицы и абзац §4.4 повторно прочитаны для проверки.

Отрицательный поиск не равен отсутствию источника: отдельная лицензия RTMPose checkpoint не установлена в просмотренных README/LICENSE; полная зависимостная среда старого ORT-примера не воспроизведена; абсолютный минимальный размер человека для нужной event accuracy из статей не выводится. Часть publisher URL блокировалась 403/429; доказательными используются реально открытые arXiv HTML, авторский PDF и полный XML, а не одни search snippets. Предыдущие соседние отчеты не использованы как доказательство выполненных экспериментов.


## F046 — W1-03: Минимальный различающий эксперимент (предложение, не выполнен)

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Минимальный различающий эксперимент (предложение, не выполнен)»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос:** улучшает ли pose качество тревог относительно тех же person detections настолько, чтобы оправдать дополнительную задержку/сложность, особенно на наклонах, сидении и ложных падениях?

### Входы и предусловия

Нужны разрешенные continuous camera clips с timestamp и исходным разрешением; реальные отрицательные промежутки, а не только нарезки действий. Положительные/похожие негативные классы: падение, быстрый присед, наклон за предметом, сидение/вставание, намеренное укладывание, работа под оборудованием, бег/ходьба, частичная потеря видимости. Не создавать опасные реальные инсценировки; использовать разрешенные готовые либо безопасно организованные материалы. Требуются event start/end, person identity внутри видео, зона, видимость и причины неоднозначности; для небольшого диагностического поднабора — ручные keypoints/visibility.

Размер набора определяется доступными независимыми событиями/камерами и нужной неопределенностью, не выдуманным числом для обещанной accuracy. Нужны исполнитель на LinQ, точный runtime/SDK, доступная конфигурация CPU/TPU и подтвержденный формат графа. GPU training до проверки pretrained ablation не обязателен. Vast.ai 3090 не арендован; VRAM fit, время и деньги не оценены.

### Независимость и варианты

Сначала группировать по camera/scene/session/person и исходному видео; соседние кадры и копии одних событий не расходятся по частям. Train — только если потребуется обучение; validation — пороги, маски, окна и сглаживание; optional SELECT — выбор s/m/дополнительного pose канала; lockbox — единственная финальная проверка замороженной системы. Если те же камеры намеренно используются для camera-specific validation, это оценка знакомой камеры, не cross-camera generalization. Все камеры lockbox не должны участвовать в подборе глобальных порогов. Публичные датасеты, известные pretrained model, не подтверждают отсутствие pretraining contamination.

| Вариант | Одинаковые компоненты | Изменение | Что проверяет |
|---|---|---|---|
| A0 | detector D, tracker T, зоны, кадры, event/dedup evaluator | bbox aspect, trajectory, persistence | Простой конкурент |
| A1 | D,T и та же временная схема | + RTMPose-s geometry, validity/unknown | Чистую добавочную пользу pose |
| A2 | D,T, pose s | Геометрия + причинная state machine | Пользу истории поверх мгновенной позы |
| A3, только если требуется | D,T, схема A2 | s→m с теми же crop/данными | Нужно ли улучшение extractor |

Чтобы сравнение A0/A1 не стало соревнованием разных трудозатрат tuning, заранее ограничить и записать сетки порогов/окон; выбрать рабочую точку на validation по согласованной стоимости ошибок. Замена D на single-stage YOLO pose — отдельный эксперимент после основного, не «чистая польза keypoints».

### Процедура

1. Зафиксировать split manifest с camera/session/group ID и SHA-256 файлов, model/config/commit hashes, версию decoder/tracker/rules. До lockbox определить matching событий, допустимое окно детекции и критерий одного события.
2. Получить один набор boxes/tracks D/T для A0–A3. Отдельно учитывать пропуски D: oracle/ручные boxes только в диагностике верхней границы, не в основном product result. Отметить ID switch, fragment и occlusion.
3. Запустить s на исходных crop одинаковых timestamp; сохранить raw keypoints/scores/mask и качество. Для feature windows использовать elapsed seconds, записать фактические детекторную и pose частоты. Все фильтры causal. Временная схема минимум `normal → suspect_transition → confirmed / persistent_low / unknown → recovered`; already-low не требует выдумывать пропущенное начало падения.
4. На validation подобрать пороги и duration по событийному PR; оценивать варианты при одинаковом FP/hour либо одинаковом recall, показывая trade-off latency. Затем заморозить параметры. Lockbox открыть один раз; ошибка там — находка, а не повод дотюнинговать и повторно назвать тот же набор test.
5. Для выбранного варианта выполнить отдельный LinQ E2E run с реальной многолюдностью и количеством потоков. Измерить preprocessing, neural graph, decoding/NMS, tracker/rules, очередь и delivery. Разделить warmup, steady-state и перегрузку. Проверить runtime graph placement и качество после конвертации — это handoff, не готовый результат W1-03.

### Метрики, артефакты и критерии решения

- Основные: event recall/precision с явным matching; false alerts/camera-hour и продолжительность negative exposure; onset→alert latency p50/p95 и хвосты; duplicates/event; missed critical events по причинам. Время подтверждения входит в latency, а не вычитается как «не inference».
- Диагностика: ошибки «наклон→падение», «сидит→падение», «уже лежит→упал»; доля `unknown`, event recall среди rejected pose и всего потока; pose dropout, joint validity, track switches; ошибки ключевых точек на ручном поднаборе. Срезы по исходной высоте person, видимому торсу/ногам, числу людей и overlap, свету, ракурсу, motion blur и PPE. Высота после crop resize — неверная переменная для дальности.
- Resource metrics: E2E throughput, queue age, dropped/skipped frames, CPU/TPU placement и utilization, память по реальному run. Не считать один pose-call на одного человека равным одному кадру многопоточного сервиса.
- Неопределенность: интервалы/paired resampling по независимым clip/camera groups, не по коррелированным кадрам. Не сравнивать frame accuracy на дисбалансном потоке с event recall.
- Артефакты: split/provenance manifest; config+env lock; raw bbox/track/keypoint JSONL; feature/mask/state transitions; event matching table; per-stratum metrics; reproducible timing logs; failure clips с privacy controls; список неустановленного.

**Успех:** A1/A2 уменьшают релевантные ложные тревоги при согласованном recall и укладываются в обязательную E2E задержку на LinQ; улучшение сохраняется на критических срезах, а не только крупных неперекрытых людях. Если A0 не хуже в допусках — pose не включать в обязательный путь. Если выигрыш только на крупных видимых людях — ограничить область применимости и сделать качество/unknown явным. Если s и m одинаково ошибаются из-за отсутствующих суставов или идентичной проекции — смена размера сети не закрывает задачу; рассмотреть иной ракурс, RGB context/action model или другой сценарий.

Успешный эксперимент **не докажет** перенос на другие камеры, реальные несценарные аварии, потерю сознания, качество всех PPE/телефонных действий, deploy совместимость других action-моделей или отсутствие pretraining leakage. Неудача pose не доказывает невозможность распознавания события по RGB видео.


## F047 — W1-03: Передачи соседним ячейкам и вопросы до внедрения

- Происхождение/locator: [W1-03](_WORK/W1_03.md), раздел «Передачи соседним ячейкам и вопросы до внедрения»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S037.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


1. **Tracking/temporal:** pose frequency и detector frequency — разные параметры; S037 benchmark использует detector interval=5 frames. Пропуск detection может задержать появление человека и менять track recovery. Передавать timestamps, actual observed/predicted bbox, keypoint age/validity; измерять отдельно neural latency, scheduling lag и event-to-alert. Проверить удержание identity при падении/перекрытии и dedup после ID switch.
2. **Геометрия/калибровка:** определить ground plane, camera roll, допустимые зоны и смысл «возле». Не применять ground homography к рукам/голове вне плоскости пола. Нужен ли метрический зазор или достаточно нарисованного опасного полигона? Как определить статус движущегося механизма?
3. **LinQ/quantization:** установить SDK, operators, static shape/batch, формат, поддержку SimCC/GAU и placement. Сравнить keypoints/features/events до/после преобразования, особенно вблизи порогов. Не назвать ONNX готовым TPU-графом.
4. **Evaluation/datasets:** обеспечить независимые camera/scene groups, hard negatives и непрерывный фон; уточнить onset для падения и отдельную метку already-lying. Аннотация видимости ключевых суставов важнее общей «occluded» галочки. Данные с постановочными домашними падениями — диагностический источник, не доказательство industrial generalization.
5. **Action-model ветка:** передать причины неоднозначности (бег/шаг, работа/опасное взаимодействие, быстрый присед/падение), pose sequence + mask + bbox trajectory, не обещать достаточность skeleton-only. Подбор всех action weights/datasets здесь намеренно не выполнен.
6. **Product/scenario:** согласовать названия тревог и смысл `unknown`; длительность подтверждения нельзя механически копировать со страницы кейса, если она подавляет короткое опасное событие. Нужны evidence clip, дедупликация и фиксация пропуска наблюдения.

Приоритетный следующий шаг — не обучение на 3090, а A0/A1/A2 с одним detector/tracker на независимом camera-aware наборе и ранняя проверка достижимости LinQ. Это снижает неопределенность: нужен ли команде pose вообще, какие именно события он улучшает и где должен отказаться от вывода.


## F048 — W1-04: Решение для команды

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Решение для команды»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S044, S045, S046, S047, S048.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F048. Основной путь для хакатона:** нейронные наблюдения → идентификация человека/зоны → причинные признаки → сценарный конечный автомат (FSM) с временем в секундах → подтверждение → дедупликация/rearm. Начинать с устойчивых состояний и геометрических переходов, которые действительно видны: нахождение в зоне, видимое отсутствие PPE, лежащая поза. Для действий, различаемых только движением, сопоставить этот baseline с компактным temporal classifier; полноценную RGB video model добавлять после доказанного семантического недостатка признаков и проверки исполнения на LinQ. Это рекомендация по управлению риском интеграции, а не утверждение, что правила точнее нейросетей.

**F048. У разных сценариев разные часы подтверждения.** Длительное состояние, резкий переход и повторяемое действие не должны пользоваться одной выдержкой «несколько секунд». Для «долго находится без каски» выдержка может подавлять дрожание; для короткого пересечения барьера она способна удалить всё событие; для падения нужно различать переход и последующее лежание. Иллюстрация подтверждения на с. 9 кейса не отменяет дедлайн с. 5/7. Основание кейса — `_WORK/CASE_NOTES.md`, прямые визуальные наблюдения root; PDF в этой ветке повторно не рендерился.

**F048. 1 FPS — только экспериментальная точка, не универсальный режим.** Редкая выборка может быть достаточна для длительного видимого состояния, но не гарантирует наблюдение краткого действия, порядок жестов или оценку резкости движения. SlowFast разделяет семантику и частое наблюдение движения [S046]; MoViNet исследует зависимость от frame rate и temporal coverage [S045]. Их benchmark не устанавливает минимальный FPS для цеха.

**F048. Causal online quality — отдельное свойство.** Будущие кадры нельзя использовать для сигнала, выданного в прошлом. Bidirectional TSM и uniform sampling целого законченного клипа не равны online-модели [S044,S047]. В ByteTrack есть offline tracklet interpolation с обоими концами пропуска [S048]: её улучшение MOT-метрик нельзя переносить на доступный в момент тревоги трек. Для live допустимы экстраполяция с неопределённостью либо ожидание будущего кадра с честной задержкой.

**F048. Не смешивать пять частот:** source FPS, decoded FPS, реально новые нейронные observations/sec, tracker/rule update/sec и inference throughput. Повтор последнего bbox на каждом кадре не создаёт новых свидетельств. Зацепка W1-03 о RTMPose `skip detection=5 frames` передана как соседнее наблюдение: в этой ветке публикация не перепроверялась, число не используется как доказанный LinQ benchmark. В рецепте записать schedule detection/pose/tracking и stale age каждого признака.

Метрический контракт не переписываем: использовать `_WORK/W1_01.md` — timely event recall, ложные уведомления/наблюдаемый camera-hour, дубликаты, задержки, coverage и неопределённость. Вклад этой ветки — причинное исполнение, временная разметка и наблюдаемость стадий.


## F049 — W1-04: Матрица полезности, стоимости и данных

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Матрица полезности, стоимости и данных»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S044, S045, S047, S051.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


«Низкая/средняя/высокая» — качественная оценка дополнительных работ относительно работающего detector pipeline, **не измерение часов, денег, VRAM или скорости**. Всем вариантам нужны независимые непрерывные видео с отрицательным фоном и onset/end/observable из W1-01.

| Подход | Полезность | Стоимость и минимальные данные | Граница |
|---|---|---|---|
| Confidence hysteresis, causal EMA | Подавление колебаний уверенности длительного состояния | Низкая; scores, visibility, GT эпизодов и реальные интервалы кадров; обучение необязательно | Persistent error становится устойчивой; задержка/смещение границ |
| K-of-N в trailing window | Терпимость к отдельным пропускам | Низкая; валидационные последовательности при целевой частоте | N кадров при переменном FPS означает разное время; burst miss не равен независимым ошибкам |
| Timestamp-aware FSM, dwell, rearm | Начало, окончание, продолжение и одно сообщение | Низкая/средняя; GT переходов, окклюзий, второго человека, выхода/возврата | Порогами не восстановить невидимую каску, метрическую дистанцию или причину лежания |
| Траектория, sparse flow, motion features | Направление/изменение положения, триггер | Средняя; последовательные кадры, PTS, ID, hard negatives камера/свет/тени | Вектор пикселей не равен скорости в метрах; camera motion/масштаб; калибровка отдельно |
| Linear/MLP на causal summary features | Обучаемое сочетание позы/motion/confidence | Средняя; labeled windows/эпизоды, negative/background class, групповые splits | Нужны различающие признаки; clip accuracy не гарантирует timely alarm |
| Causal TCN/GRU над per-track features | Порядок и краткая история с masks/dt | Средняя; track-aligned sequences, onset labels, missingness, независимые люди/камеры | ID mixing разрушает историю; reset и export/state I/O на LinQ не установлены |
| Online uni-directional TSM | Temporal fusion внутри 2D backbone [S044] | Средняя/высокая; action dataset, causal variant, preprocessing, state per stream | Zero added FLOPs модуля не означает нулевой memory traffic или поддержку TPU |
| Streaming MoViNet | Causal 3D operations и stream buffers [S045,S051] | Высокая относительно FSM; temporal labels/background, buffer lifecycle, actual compatibility | State/cumulative pooling на длинном фоне влияют на новое событие; reset policy требует теста |
| Pose sequence: TCN/GCN/PoseC3D | Динамика тела с меньшей зависимостью от RGB-фона | Средняя/высокая; detector+pose, ID/confidence, sequences; heatmaps [S047] | Phone/PPE не кодируются скелетом; frontend не входит автоматически в head FLOPs |
| RGB 3D CNN / SlowFast / video transformer | Богатые action/context features | Высокая; transfer/дообучение, negative untrimmed видео, sampling, export/runtime validation | Clip classifier требует localization/background/postprocessing; benchmark score не доказывает deadline |
| Proposal → temporal verifier | Дорогой head только на кандидатах | Средняя/высокая; весь поток и missed proposals в GT, pre-trigger ring buffer | Recall ограничен proposal stage; verifier не увидит пропущенное событие |

Linear/TCN/GRU — дизайн кандидата, не проверенный pretrained checkpoint. Для TSM/MoViNet/SlowFast/PoseC3D выбраны архитектурные основания, а не готовые веса промышленных нарушений. Число эпизодов, достаточное для конкретного класса и доверительного интервала, не установлено; универсальная квота была бы выдумкой.


## F050 — W1-04: Как время меняет информацию

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Как время меняет информацию»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S045, S046, S047, S049, S050.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


### Частота, шаг и окно

Пусть `t_i` — timestamp экспозиции/PTS нового observation, `Δ_i=t_i−t_(i−1)`. Для равномерной выборки `Δ=1/f_obs`, N кадров покрывают расстояние между первым и последним `(N−1)/f_obs`; некоторые loaders задают duration как N/f, поэтому convention хранить явно. Clip span и шаг вызова модели различны: окно истории можно обновлять часто, не создавая новой информации между observations.

**F050 — аналитическая иллюстрация, не эксперимент.** Пусть единственный различающий признак виден d секунд, идеальный моментальный sampler имеет период Δ, фаза события относительно сетки равномерна, потерь/окклюзий нет. Вероятность хотя бы одного попадания `min(1,d/Δ)`. При d<Δ существуют фазы полного пропуска даже у идеального детектора. Для K точек в событии минимальный span `(K−1)Δ` — лишь необходимое условие, не гарантия при произвольной фазе. Реальные видео нарушают предположения; формула не является оценкой recall и не доказывает распознавание по одному попаданию.

Не «повышать FPS» повторением кадра и не считать это наблюдениями движения. Если модуль обучался на интервалах одного масштаба, сжатие/растяжение времени меняет смысл displacement и receptive field. Resampling возвращает решётку, не потерянные кадры; interpolated/repeated samples должны иметь mask и age. Speed augmentation не применять автоматически: «идёт»/«бежит» могут меняться по определению при изменении скорости.

При снижении FPS сравнить две постановки: фиксированный physical span с меньшим числом observations; фиксированное N с большим span. Иначе неясно, потеряна динамика или добавлен контекст. Sampling — часть модели [S045,S046], точные benchmark частоты не переносим в цех.

### Латентность и окна

Trailing window `[t−W,t]` не требует будущего; output доступен после decode/queue/inference, не в timestamp последнего кадра. Centered window требует lookahead: переносить результат к центру с нулевой задержкой нельзя. Uniform sampling всего файла опасен: модель могла увидеть завершение падения при заявленном начале тревоги [S047].

Разделить ожидание первого информативного observation, накопление causal evidence, processing/queue и delivery. Интервалы могут перекрываться: не складывать дважды dwell внутри собираемого окна. Хранить trace и реконструировать критический путь. При старте определить partial history/zero-padding/unknown и отдельно проверить warm-up. Длинная предыстория не обязательно означает ожидание W секунд после onset; прогноз по одному новому кадру не означает, что действие уже различимо.

### Пропуски, рывки, устаревшие данные

Разделить intentional sampling, network loss, decode failure, queue drop, skipped inference, низкую видимость, отсутствие объекта и ID loss. «Не получили кадр» не означает «нарушение закончилось».

GStreamer различает buffer timestamp, clock и segment running-time [S049]. PTS файла не является автоматически exposure time или UTC. Reconnect/seek/смена SEGMENT требуют stream epoch и отображения шкал. Runtime durations измерять монотонными часами; sync/capture mapping для end-to-end latency документировать отдельно.

Queue ограничивает buffers/bytes/time; blocking и dropping различны [S050]. Предложение: bounded inference queue, drops by reason и stale age, предсказуемая recent-data policy operative path. Trade-off: удаление старых кадров сокращает age, но может удалить краткое событие. Evidence ring хранить отдельно при возможности; восстановление старого события не выдавать за timely live alert. Быстрая обработка backlog не доказывает хороший live FPS.


## F051 — W1-04: Предлагаемая causal реализация baseline

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Предлагаемая causal реализация baseline»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S048, S052, S053.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Параметры ниже настраиваются на development, не являются нормативом. Для `(camera_epoch, entity_or_zone, scenario)` хранить `NORMAL → CANDIDATE → ACTIVE → RECOVERY → NORMAL`, отдельно `UNKNOWN/STALE`. Event key не равен необработанному track ID.

1. Уникальное observation получает PTS, receive time, provenance, visibility/confidence. Prediction-only bbox/pose не считается свежим positive PPE evidence.
2. Positive/negative/unknown разделены. Для CANDIDATE требовать заданные positive признаки, число свежих observations, временное покрытие и maximum gap. Две положительные точки по сторонам слепого интервала не являются непрерывно наблюдёнными двумя секундами нарушения.
3. Для EMA допустим `α_i=1−exp(−Δ_i/τ)`, `z_i=(1−α_i)z_(i−1)+α_i p_i`, **только при новом валидном observation**. Time-scaled forgetting не доказывает известное состояние между кадрами. Unknown обрабатывается отдельной decay/reset/hold policy с TTL, без накопления positive duration.
4. Разнести пороги входа/выхода. Dwell устойчивого состояния и short fast path перехода различны. Fast path разрешён, только если признак достаточен по семантике класса.
5. ACTIVE отправляет первое сообщение один раз; одиночный detector miss не завершает эпизод. Длительный stale означает потерю наблюдения, не recovered. Подтверждённое окончание/rearm разрешает новое событие. Проверить второго человека и уход/возврат первого.
6. Reconnect, camera change, timestamp rollback и неоднозначная reassociation требуют reset/карантина state по политике. Streaming state разделён по камерам/сущностям; batch не смешивает буферы потоков.

Motion displacement/dt вычислять между валидно сопоставленными observations с проверкой confidence/масштаба/gap. При большом gap отказаться от резкости/ускорения. Flow — apparent motion, не смысл действия [S052]. Нулевой flow при frozen stream не доказывает неподвижность человека: нужен независимый freshness/duplicate-frame health check.

**F051 — ловушка конкретного трекера.** В pinned ByteTrack `frame_id` увеличивается на `update`, TTL задан в update frames с масштабированием `frame_rate`, Kalman transition использует `dt=1` [S053]. При update только на 1 FPS observations и `frame_rate=30` physical TTL/динамика будут неожиданными. Реальная частота помогает TTL при регулярном sampling, но не делает фильтр timestamp-aware при jitter. Нужна проверенная обвязка/адаптация dt и noise либо регулярная grid с учётом пропусков; это предложения, не выполненный patch. Offline interpolation отключить для live-сравнения [S048].


## F052 — W1-04: Observability

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Observability»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


К W1-01 добавить trace, отделяющий отсутствие информации, ошибку модели и опоздание:

| Артефакт | Минимальные поля |
|---|---|
| Frame manifest | camera/session/epoch, frame_id, PTS/timebase, mapped capture time и mapping quality, receive/decode time, original index, repeated/dropped/late flags |
| Stage observation | model/version/hash, scheduled/executed/skipped, source frame IDs, crop, score/visibility, newest/oldest evidence time, inference start/end |
| Track trace | update PTS/dt, detected/predicted/interpolated, association confidence, ID switch/reset/rejoin, bbox/pose age |
| Temporal trace | state before/after, rule version, window frame IDs/span, masks/dt, score before/after smoothing, positive/negative/unknown support, confirm/suppress/reset reason |
| Streaming state | camera/entity owner, state epoch, init/reset reason, warm-up; config/hash, необязательно tensor dump |
| Health | queue levels/time/age, drops by cause, wall-time, fresh observations/sec by stage, stale intervals/reconnect/clock discontinuity |
| Alert | event key, causal evidence cutoff, first usable evidence, confirmed/emitted/received, suppression/rearm reason, attachment references |

Нужны распределения Δ_i, maximum gaps, observation age, per-stage throughput и latency tail под несколькими потоками, вместе с coverage. Сбросивший трудные кадры режим не должен молча улучшать знаменатель. Audit зависимостей проверяет: ни один кадр после фактического decision cutoff не использован в сигнале. Названия causal model недостаточно.


## F053 — W1-04: E04: различающий эксперимент

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «E04: различающий эксперимент»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос.** Убирает ли timestamp-aware confirmation ложные всплески без потери коротких событий, и сохраняется ли выигрыш temporal classifier после ограничения causality, gaps и стоимости на LinQ? До запуска неизвестно.

**Входы/ресурсы.** Непрерывные записи с исходными timestamps и достаточной temporal resolution; priority classes; GT onset/end/observable, actor/visibility, negative exposure, camera health; разметчик спорных границ; LinQ с известным runtime/hardware и разрешёнными моделями. GPU нужен только при выбранном learned head и авторизованном ресурсе; аренда Vast.ai не нужна для baseline и не запрашивалась. Время/цена/VRAM не оценены.

**Системы.** A: per-frame decision без confirmation, с тем же dedup контрактом. B: causal hysteresis/K-of-N. C: timestamp-aware FSM. D при данных/совместимости: compact causal feature classifier. E дополнительно: online TSM либо streaming MoViNet; RGB clip comparator на trailing window с реальным output time. Matching/семантика одинаковы; «падение» не подменяется «лежанием».

**Процедура — предложена, не выполнена:**

1. До tuning разделить train/validation/optional SELECT/lockbox по incident/site/camera/session согласно заявленному обобщению. Все нарезки, соседние кадры, FPS/drop copies одной записи в одном split. Для unseen-camera claim камера целиком held out; разрешённая per-camera настройка только development.
2. На development зафиксировать grid. Пример **исследовательских точек**, не целевых рекомендаций: 1/2/5/10 FPS и доступная исходная частота; несколько sampling phases. Это paired perturbations одного incident, не дополнительные независимые события. Span и N менять раздельно.
3. На frozen observation cache выполнить causal логический replay A–D: только доступные к решению observations, без future interpolation. Cache изолирует логику, **не измеряет runtime** и load-related misses. Frontend/provenance одинаковые либо честно сравниваются end-to-end systems с разными frontend.
4. Раздельно добавить decimation, random losses, burst losses, variable gaps, jitter/reordering, repeated frozen frames, reconnect/PTS reset, overload, ID fragmentation/switch. Затем наблюдаемые сочетания. Intensities выбрать по реальному потоку либо явно назвать synthetic stress range, не field distribution. Repeat не увеличивает support.
5. Проверить selected pipeline real-time replay/live на LinQ с decode/queue/delivery и wall-clock arrival, не быстрым offline iterator. Измерить реальные stage frequency/skips. После одиночного потока проверить предусмотренную многопоточность; capacity неизвестна.
6. Заморозить models/thresholds/τ/windows/dwell/TTL/reset/proposal/rearm на development/SELECT. Lockbox один раз; по нему нельзя выбирать checkpoint, threshold, ensemble или phase. Failures документировать; новые итерации требуют нового независимого теста.

**Метрики/срезы.** Основные W1-01; дополнительно timely recall loss относительно no-loss causal run, sensitivity к phase, duration buckets, unknown/stale coverage, число fresh observations до deadline, identity fragmentation, warm-up/reset failures, queue-age tails. Срезы устойчивого состояния/перехода, occlusion, small person, camera motion. Интервалы по независимым группам: пять phases не увеличивают N впятеро. Offline clip top-1/localization — диагностика.

**Артефакты.** Hash dataset/split manifest и timestamps; annotation version; sampler/loss seed и schedule; конфигурации; source/weights/runtime hashes/licenses; causal trace, event/alert ledger, exposure/gaps; paired report и failure clips; LinQ runtime report. Они пока не созданы.

**Решение по исходу.** Оставить C, если learned branch не улучшает своевременное качество при сопоставимых false notifications/coverage или не проходит runtime. Если 1 FPS теряет события по фазе — повысить observation rate, сузить обещание или исключить класс: smoothing информацию не восстановит. Если gaps от нагрузки — сначала schedule/queue, затем меньшая модель. Если при качественном входе правила путают разные действия — основание инвестировать в temporal classifier.

Успех не доказывает промышленную безопасность, unseen cameras/conditions, все длительности, будущую нагрузку, достаточность pose для phone/PPE или TPU после другого экспорта. Cache replay не доказывает runtime, synthetic loss — реальную сетевую надёжность.


## F054 — W1-04: Противоречия, отрицательные результаты, handoffs

- Происхождение/locator: [W1-04](_WORK/W1_04.md), раздел «Противоречия, отрицательные результаты, handoffs»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F054. Не подтверждено:** universal safe FPS/dwell; LinQ operator support по названию архитектуры; устойчивость к burst gaps по keypoint-drop тесту; независимое online event качество по MOT с interpolation/test tuning. EMA не исправляет persistent FP, cooldown не доказывает правильную дедупликацию.

CVF PDF TSM/SlowFast/MoViNet вернули 403; чтение заменено полными versioned arXiv HTML/PDF. MoViNet v3 дал 404; карточка указывает v2, использована она. GitHub API не открылся web-tool: малые commit metadata прочитаны `Invoke-RestMethod`, pinned raw code затем открыт web-tool. Это не benchmark. Дополнительные sampling papers появились в поиске, но без проверки в доказательства не включены.

Передачи:

- **W1-01/evaluation:** onset/observable/deadline и causal cutoff; существующие matching/coverage; duration/phase/gap/cold-start slices, независимость по исходным incident.
- **W1-03/frontend:** schedule detection/pose/tracking, source FPS, fresh observations, skeleton/confidence/crop provenance, полная frontend cost. Cached pose не новое evidence; skip detection виден в speed сравнении.
- **LinQ/runtime:** hardware/SDK/state I/O/supported ops/export/quantization; timestamp mapping/clock sync; queues, gaps, multi-stream capacity. RTX 3090/TFLite CPU не предсказывают TPU.
- **Данные/scenarios:** переходы наклонился/сел/лёг/упал; прошёл рядом/пересёк; многолюдность/occlusion; длительный negative фон и rearm. Веса/dataset licenses — соседняя ветка.
- **Calibration:** image motion не обещает метрическую скорость/дистанцию; camera calibration до test отдельно.
- **Product:** confirmation/recovery/rearm по scenario/severity, UNKNOWN/STALE policy; эскалация; время отправки отдельно от готовности полного evidence clip.

Открытые вопросы: минимальная длительность/ранний признак каждого события; доступный source FPS/PTS; сколько fresh observations до дедлайна; продолжение через occlusion; допустим ли поздний evidence clip после немедленного сигнала; независимый negative exposure; поддержка stateful model graph на LinQ. До ответов — causal baseline и измеримое сравнение, без обещания, что 1 FPS или тяжёлая video model уже решают короткие действия.


## F055 — W1-05: Решение сначала

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Решение сначала»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S054, S055, S057, S059, S061, S062, S064, S065, S066, S068.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F055. Основной shortlist: ByteTrack ↔ OC-SORT на одинаковых детекциях; BoT-SORT с явно включённым ReID — условный третий кандидат.** Длинная окклюзия, одинаковая спецодежда и пересечение людей не решаются увеличением `track_buffer`. ReID добавлять, если он уменьшает неверное связывание и ошибки событий на целевых сценах, а neural encoder действительно исполняется на LinQ с приемлемой задержкой. Это рекомендация, не установленный победитель. Архитектуры: S054–S061.

**F055. Raw track ID не равен человеку и не равен инциденту.** Нужен отдельный event UUID, время, доказательства и aliases tracklets. Иначе разрыв ID создаёт дубль, а ошибочная склейка переносит телефон/PPE/cooldown на другого сотрудника. Один IDSW способен увеличить, уменьшить или не изменить число уведомлений: последствия зависят от состояния события. Это инженерный вывод, не готовая функция MOT-библиотек.

**F055. Проверка времени обязательна до настройки поведения.** Исходные реализации считают шаги/кадры. Длительность нарушения, expiry и latency должны быть в секундах. При VFR, decimation и burst drops «30 кадров = секунда» неверно; замена buffer не исправляет Kalman dynamics. Прямой код: S055/S057/S059/S064.

**F055. PPE/phone-owner association реализовать отдельно от MOT, с `unknown`.** Трекер связывает экземпляры во времени; он не устанавливает, кто носит каску, держит телефон или управляет машиной. Близость боксов не доказывает отношение. Невидимая голова не доказывает отсутствие каски. Предлагаемый алгоритм ниже; научное основание отдельного contact inference — S066.

**F055. Современные альтернативы доступны с оговорками.** TrackTrack CVPR2025 имеет MIT-код, но официальный artifact требует два пула детекций и заранее подготовленные CMC-файлы. BoostTrack++ имеет MIT-код, но рецепт оценивает результат с GBI postprocessing и сохраняет author-default ошибочный shape variant. Свежий ARC-SORT от 15.10.2026 обещает будущий код; не execution candidate. S062–S065/S068.


## F056 — W1-05: Контекст кейса и критерий полезности

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Контекст кейса и критерий полезности»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Из `_WORK/CASE_NOTES.md`, подготовленного root после просмотра PDF: с.5 — малые PPE, плохое освещение, окклюзия, задержка несколько секунд; с.7 — одна ситуация → одно сообщение; с.13 — dedup и измеренная LinQ скорость. В этой ветке PDF повторно визуально не просмотрен: это явно внутреннее вторичное свидетельство.

Оценивать следует корректного участника и один продолжающийся episode, а не только цветные ID/MOTA. Для опасной близости важны оба участника: смена ID машины создаёт новую пару, смена ID человека переносит состояние опасности. Расстояние в метрах и калибровка — handoff соседней ветке.


## F057 — W1-05: Shortlist и фактическая архитектура

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Shortlist и фактическая архитектура»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S054, S058.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


| Кандидат | Проверенная структура | Зачем проверять | Ограничения |
|---|---|---|---|
| ByteTrack | Kalman + high-score association, затем low-score rescue оставшихся активных tracks; отдельной ReID-сети нет; MIT | Прозрачная линия при частичной окклюзии со снижением score | Полностью отсутствующая детекция не восстанавливается low-score pass; неоднозначное пересечение без appearance; upstream cutoff может уничтожить recovery pool |
| OC-SORT | Motion-only observation-centric re-update/momentum/recovery, MIT | Остановка, нелинейное движение, краткая потеря | Длинная окклюзия остаётся неоднозначной; `delta_t` observations означает шаги, не секунды |
| BoT-SORT off/on ReID | ByteTrack-подобный lifecycle, XYWH Kalman, GMC, optional FastReID, MIT | Установить пользу внешности в заводских пересечениях; GMC при дрожании | Дополнительный neural inference; одинаковая форма; ошибочный GMC без достаточного фона |
| Deep OC-SORT, резерв | OC-SORT + CMC + confidence-dependent appearance EMA + adaptive weighting, MIT | Если обычный ReID загрязняется плохими crops | Сложнее зависимости/encoder deployment; README использует `--post` |
| BoostTrack++, резерв | Confidence boosting, shape/Mahalanobis/soft BIoU, appearance, MIT | Низкая detector confidence и ложные новые IDs | Отделять `_post_gbi`; фиксировать shape variant; boosting может поддержать ложный bbox |
| TrackTrack, резерв | Iterative TPA + track-aware initialization, два detector pools, MIT | Дубли новых tracks рядом с активными | Один post-NMS output не воспроизводит весь метод; CMC-file reader требует live adaptation |

Не ранжировать абсолютные HOTA из разных статей как единый эксперимент. MOT17/MOT20 преимущественно pedestrian tracking; даже KITTI-cars у OC-SORT не доказывает качество складского погрузчика. Люди/машины/малые предметы требуют class gates, разного detector recall и lifecycle.

S054 сообщает 30 FPS на V100 и MOT17 HOTA 63.1 для системы авторов; S058 — 700+ FPS CPU при **уже готовых детекциях**. Это разные подсистемы и не прогноз LinQ. В BoT-SORT §4.4 прямо указаны ошибки GMC при нехватке фоновых точек и стоимость appearance. Измерять весь decode→detector→ReID→association→event→notify путь.


## F058 — W1-05: Frame-count, seconds и нерегулярные timestamps

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Frame-count, seconds и нерегулярные timestamps»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S055, S057, S059, S064.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F058 — наблюдение по исходникам, не запуск.** ByteTrack: `buffer_size=int(frame_rate/30*track_buffer)`, `frame_id += 1` на `update`, expiry через разность frame IDs, Kalman `dt=1`. Если приложение вызывает update только на выбранных кадрах, единица — обработанный кадр. Если на пропущенные кадры делает empty updates, контракт иной. BoT-SORT аналогично считает buffer/frame_id; OC-SORT использует step-based `time_since_update`, `frame_count`, `max_age` и observation history; TrackTrack expiry также frame-based, включая `update_without_detections`. S055/S057/S059/S064.

Математический пример, **не измерение**: buffer=30 при 30 updates/s — около секунды, при 5 updates/s — около шести. В timestamps `0.0,0.1,0.2,1.8` последний интервал не равен предыдущим; средний FPS не описывает скачок.

Предлагаемый контракт:

1. Хранить camera, stream epoch, source frame ID, presentation/capture timestamp и time base, монотонное время приёма/обработки, detector version. PTS не обязательно физическое время экспозиции; его происхождение документировать.
2. Обновлять в порядке video time. Повторный timestamp не считать независимой evidence. Out-of-order кадры ограниченно reorder с учётом latency либо отбрасывать с логом; не применять старое измерение к новому состоянию.
3. После seek/restart/PTS reset создавать новый epoch. Совпавший integer ID не склеивает людей разных эпох.
4. Быстрый вариант: проверенный фиксированный cadence, явный допустимый gap, predict-only шаги на выбранной сетке. Большой gap → unknown/lost/reset. Не размножать последний кадр как новые детекции.
5. Time-aware вариант: скорости за секунду, F(Δt), Q(Δt), time expiry; адаптировать observation history/re-update, covariance, gates и CMC. Изменить только F или TTL недостаточно. Это модификация, а не готовая способность upstream pin.
6. Разделить физическую длительность по video time и live event-to-alert latency. Offline replay не измеряет сетевую задержку. Clock skew и capture uncertainty показывать отдельно.

Seconds-based event timers нужны при обоих вариантах. Нельзя приписывать весь неизвестный интервал предыдущему PPE/phone state. Накапливать только наблюдённую evidence с ограничением inter-observation gap; длинный gap — unknown. Confirm/grace/clear окна выбираются на validation; мгновенные опасности не должны автоматически наследовать длительное confirmation.


## F059 — W1-05: Person-to-PPE / phone / vehicle association

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Person-to-PPE / phone / vehicle association»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S066.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Далее **собственный проектный протокол, не готовая опубликованная модель и не результат испытания**.

### Граф отношений

Вершины: person/vehicle tracklets, PPE/phone detections, body regions/keypoints, zones. Типы рёбер: `worn_by`, `held_by`, `near`, `inside_cab`, `danger_pair`. Confidence/observability отношений хранить отдельно от detector score и track confidence.

Сначала type/visibility/geometry hard gates; затем стоимость из нормированной геометрии, pose при наличии, temporal consistency и качества наблюдения. Constrained assignment допускает dummy `unassigned`; предмет не обязан получить владельца. Каска/жилет — разные слоты. Две руки могут контактировать с одним объектом: слепое one-to-one для всех типов рёбер неверно. При близких лучшем и втором кандидатах сохранять ambiguity и не присваивать уверенного владельца.

### PPE

- Каску сопоставлять голове, жилет — торсу, harness — соответствующей видимой части. Нормировать размеры человеком/головой, не диагональю всего изображения.
- IoU маленькой каски с полным person bbox низок даже при правильном ношении; containment неоднозначен при перекрытии person boxes.
- Состояния `present`, `absent with visible body part`, `unknown/unobservable` различны. Закрытая машиной голова не является отрицательным свидетельством. Каска в руке/на полке не доказывает `worn_by`.
- Накапливать evidence только на согласованном owner tracklet, с TTL. После неоднозначного пересечения не переносить PPE state безусловно.

### Phone

Baseline: phone detector в доступном crop + наблюдаемая рука/запястье/голова + устойчивое owner relation. `using` требует дополнительного действия/контекста, а не только phone visible. Hard negatives: телефон на столе/в кармане/у соседа, похожая рация/инструмент, рука у лица без телефона, чужой bbox поверх вытянутой руки.

S066 демонстрирует научную возможность contact inference: Faster R-CNN с side/contact/offset heads и выбором объекта по предсказанному вектору. Это отдельная задача отношений; она не является готовым industrial phone-use classifier и не решает person identity. ResNet-101/FRCNN рецепт не рекомендован к неизвестному TPU без проверки; exact weights/licenses/deployment этой веткой не сертифицированы.

### Vehicle

Разделить `near vehicle` и `driver/operator`: bbox в проекции кабины не доказывает управление. Для опасной близости ключ — пара episode identities человека/машины; смена любого raw ID требует проверки продолжения. Class-consistent association и class flicker log обязательны. Экранное расстояние не выдавать за метры, geometry/state машины — соседний handoff.


## F060 — W1-05: Восстановление и dedup событий

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Восстановление и dedup событий»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F060 — проект lifecycle:** tracker `tentative→confirmed→lost/occluded→recovered|closed`. Prediction-only позиция — поисковая гипотеза, не доказательство PPE/phone/лежания. Для reattachment проверять class, elapsed seconds, возможное перемещение, качественный appearance и других конкурирующих кандидатов. Один универсальный cosine/IoU threshold не обоснован.

Event lifecycle отдельный: `candidate→active/notified→grace_unknown→cleared/closed`. При убедительном восстановлении tracklet сохранить event UUID. При неопределённости сохранять неопределённость участника и историю гипотез; смена raw ID сама не открывает новое уведомление. Dedup не должен поглотить второго человека, другое транспортное средство или новое нарушение после подтверждённого прекращения. Cooldown не доказывает идентичность ситуации.

Запись события: camera/epoch, scenario/rule version, start/last-confirmed/notify/clear, UUID, участники и aliases с reason/confidence, evidence refs, unknown intervals, detector/tracker version, причины open/merge/close. Location-only alert при неизвестном владельце оценивать отдельно от корректного персонального attribution.

| Причина | Последствие для инцидентов | Как увидеть |
|---|---|---|
| Fragmentation после окклюзии | Дубль, сброс confirm timer или miss | Один GT incident → несколько prediction UUID |
| ID switch на пересечении | Phone/PPE A приписано B; cooldown подавляет A | Wrong-owner и participant confusion |
| Loose ReID merge одинаковой формы | Два нарушения превращены в одно | False merge; GT identities на predicted identity |
| Очень длинный buffer | Ghost alert, захват нового человека старым ID | Age seconds, evidence без observation |
| Невидимая голова = no helmet | False PPE incident | Visibility-conditioned precision |
| Upstream filtering/NMS | Нет recovery candidates, новый ID | Detector pool до/после фильтра |
| Неравномерный Δt = один кадр | Ошибка скорости, выдержки и reattachment | Timestamp audit и delivery perturbation |
| Global zone cooldown | Второе опасное событие подавлено | Overlapping GT incidents |
| Restart с ID=1 | Ошибочная история/dedup | camera+epoch namespace |
| Future interpolation | Завышенный online recall/скрытая latency | Causal replay |


## F061 — W1-05: Различающий эксперимент

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Различающий эксперимент»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S067.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос:** какой минимальный causal tracker+association+event layer уменьшает дубли и неверного участника, сохраняя event recall и требуемую задержку; помогает ли ReID при одинаковом detector output?

### Входы и split

Нужны целевые видео с timestamps и правами использования, разметка trajectory IDs/boxes/visibility/occlusion, object-owner/unknown, event intervals/participants/incident IDs/onset. Нужны длинные negatives, stop, crossing одинаковой формы, PPE в руке, телефон/инструмент у соседа, вход/выход, пустая сцена. Размер набора определяется доступными случаями и нужной неопределённостью; здесь не выдумывается.

Train/validation/optional SELECT/lockbox разделять группами камер/сцен/сеансов. Соседние кадры, одинаковые сцены/камеры не дают независимого обобщения. FPS-варианты одного видео остаются в одной группе. На validation тюнить score gates, buffer/grace, ReID, assignment margin, confirm/clear; SELECT для выбора из множества систем; lockbox один раз после фиксации. Чужой MOT half-train/half-val рецепт не достаточен для нашего camera-independent утверждения.

### Процедура

1. Зафиксировать manifest/checksums/splits/rules/constraints. Ambiguous ownership разметить явно.
2. Сохранить одинаковые detector outputs выбранной версии, включая low-score pool; TrackTrack требует отдельный loose-NMS pool. Без него это изменённый port, не reproduction. Зафиксировать NMS/score/coordinate transforms.
3. Сравнить ByteTrack, OC-SORT, BoT-SORT ReID off/on с одинаковым event layer. Резервы добавлять при конкретном диагностированном провале, не бесконечным поиском.
4. Для каждого клипа создать delivery schedules с исходными PTS: nominal cadence, regular stride, random/burst drops, late/duplicate/out-of-order, reconnect/reset. Параметры fault injections фиксировать до lockbox. Не менять физическую длительность незаметно при перекодировании.
5. Stress cases: stop→occlusion→restart, пересечение одинаковой формы, полное скрытие и выход в другом месте, смена владельца, второй нарушитель во время alert, несколько машин.
6. Causal replay: на t доступны только данные к t. Запретить будущую LI/GBI/global merge и будущие сведения CMC в доказательстве alert latency. Offline output — отдельная архивная строка.
7. Ablations: raw-ID dedup vs episode aliases; IoU-only owner vs assignment+unknown; frames vs seconds; ReID off/on; GMC off/on; при необходимости time-aware motion vs fixed grid. Не менять detector одновременно с tracker при выводе о причине.
8. Финальный выбранный full path на LinQ с target-compatible detector/ReID. Измерять association CPU и neural stages отдельно/вместе; повторить ключевые stress cases при целевой конкуренции потоков, с queue age/drop/decode→notify traces. До этого deployability условна.

### Метрики и артефакты

- MOT: HOTA/DetA/AssA, IDF1, IDSW, fragmentation, recovery по **секундам gap**, false reattachment/merge. S067 объясняет ограничение одной MOTA.
- Ownership: correct-owner precision/recall, wrong-owner rate, unknown/unassigned coverage, visibility/size/occlusion strata. Разделить visible/held-or-worn/using.
- Event: precision/recall/F1 с заранее заданным one-to-one GT–prediction matching по сценарию/времени/участнику. Overlap/onset tolerance выбирать до lockbox. Extra alert на тот же GT — duplicate; второй GT, поглощённый merge/cooldown, — miss. Отдельно wrong-participant alerts.
- Latency: onset→первое правильное alert p50/p95/max, miss count, timestamp uncertainty; realtime throughput/frame age. Missed event не исключать молча и не выдумывать ему конечную latency.
- Strata: camera/scene/light/size/density/stationary/moving/occlusion/gap/delivery schedule. Не заменять burst loss средним FPS.
- Artifacts: commits/config/environment/weight hashes+licenses; split manifest; detections; delivery timestamps; MOT outputs; ownership graph; UUID/alias traces; causal decision log; GT matching/error clips; LinQ stage traces. Uncertainty считать кластерами независимых clips/cameras, не соседними кадрами.

Acceptance: численные constraints задать до финального теста из кейса/сценария; официальная accuracy formula не установлена. Выбрать допустимый quality–latency frontier с явным контролем wrong-person/duplicates. Если ReID увеличивает merges формы — оставить motion-only+unknown. Если ни один не проходит — ограничить наблюдаемость/сцену/сценарий, исправить detector/association, не скрывать ошибки cooldown.

Успех на cached detections не доказывает detector quality/LinQ speed; одна камера не доказывает новые камеры/ночь/cross-camera ReID; HOTA не доказывает event count/phone-use; меньше duplicates не означает отсутствие merges/misses; offline reconstruction не доказывает своевременный alert.


## F062 — W1-05: Противоречия и отрицательные findings

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Противоречия и отрицательные findings»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S060, S061, S063, S069.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F062. Deep OC-SORT paper online ≠ любой README output online.** S060 §4.1 заявляет отсутствие offline postprocessing; S061 предлагает --post/_post. Это не доказывает ложность paper: версии/режимы различны. Raw и post оценивать раздельно.

**F062. BoostTrack++ corrected formula ≠ author-default.** S063 сохраняет ошибочный shape variant, поскольку гиперпараметры настроены на него; --s_sim_corr меняет поведение. Указывать commit+flag. Чужой frame-based schedule не переносить как seconds-based.

**F062. Virtual trajectory не observed evidence.** ORU корректирует фильтр после нового наблюдения; не доказывает телефон/PPE в скрытом интервале. Future LI/GBI/offline merge улучшает архивную реконструкцию, но не обязательно доступен при timely alert.

**F062. Live docs не фиксируют software stack.** S069 уже перечисляет больше вариантов/defaults, чем исторический ByteTrack/BoT-SORT. «Включить встроенный tracker» без package pin/config недостаточно.

CVF endpoints OC-SORT/100DOH/TrackTrack возвращали 403 либо timeout. Для первых двух успешно открыты полнотекстовые arXiv; для TrackTrack — official repo/raw implementation. Это не выдано за чтение недоступной CVF paper. Не найдено подтверждения, что generic ReID различает одинаковую промышленную форму, что phone box доказывает using, или что эти сети готовы на неизвестном LinQ TPU.


## F063 — W1-05: Handoffs / открытые вопросы / ресурсы

- Происхождение/locator: [W1-05](_WORK/W1_05.md), раздел «Handoffs / открытые вопросы / ресурсы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


1. **W1-01/W1-03 detector/scenario:** сохраняется ли low-score pool, есть ли body-part visibility/unknown, различаются ли phone visible/held/using и PPE held/worn? Нужны actual detection schema, calibration и observable size из данных.
2. **Video architecture:** PTS/capture clocks, VFR/stride, order/queue/drop/reconnect; единица update и допустимый gap. Временной контракт нужен до speed/immobility tuning.
3. **Event/evaluation:** определение одной ситуации/нового episode, независимых участников/пар, unknown, matching/FP/latency. Split manifest без lockbox tuning.
4. **LinQ:** точные CPU/TPU/runtime/SDK/operators, deployment ReID и concurrent load. CPU association возможен как отдельная стадия; neural inference остаётся LinQ requirement. Пока target encoder нет, motion-only — основной честный вариант.
5. **Calibration/vehicle:** ground plane, cab zones, machine state и danger geometry; не компенсировать association ошибочную геометрию.
6. **Prerequisites:** права на клипы, GT trajectories/events/owners, detector outputs, CPU environment, затем реальный LinQ; для ReID checked weights/licenses/deployment. Vast.ai не обязательный ресурс для association comparison и не авторизован. Цены/VRAM fit/runtime не оценивались.

Передача: **ByteTrack ↔ OC-SORT**, условный **BoT-SORT-ReID**; современный резерв Deep OC-SORT/BoostTrack++/TrackTrack после диагностики. Приоритет — timestamps, owner uncertainty, event UUID/aliases: без них улучшенный MOT может не улучшить число и качество инцидентов.


## F064 — W1-06: Решение и последствия

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Решение и последствия»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S070, S072, S073, S074, S076, S079, S080, S081.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**F064. Начать с pretrained YOLO26s и двух контролируемых режимов одной модели: полный fine-tune против freeze→unfreeze.** Это дешевле в сложности интерпретации, чем одновременно менять архитектуру, разрешение, датасет и optimizer. Для малого похожего домена freeze может ограничить переобучение; при сильном отличии промышленных изображений слишком глубокий freeze мешает адаптации. Выбор — по независимым группам validation, не по train loss. Предобучение даёт полезную исходную точку и скорость ранней сходимости, но не обещает финальное превосходство или защиту от overfit. [S070–S073, S081]

**F064. Третий режим — D-FINE-M с официальным custom-рецептом и аккуратно сокращённым расписанием; RF-DETR-M — альтернативная реализация challenger, если проходит переносимость.** У D-FINE есть конкретные custom/O365→custom YAML. У RF-DETR snapshot существенно новее многих блоговых рецептов: default accumulation уже 1, validation по умолчанию оценивает EMA, optimizer/scheduler имеют новую конфигурационную семантику. Поэтому чужой notebook без SHA — недостаточный рецепт. Нельзя утверждать, что любой из вариантов поместится в 24 GB. [S074–S079]

**F064. Удержание person/техники/телефона должно быть явным ограничением эксперимента.** Новый detector с выходами только helmet/vest больше не предоставляет прежние COCO-выходы: это изменение онтологии, ещё до forgetting. Даже при сохранении выходов freeze backbone не защищает trainable head и не гарантирует прежнее качество. Нужны объединённая онтология, полностью размеченные нужные классы, replay старых/общих сцен и отдельная retention-валидация. При невозможности replay сохранить общий detector отдельным компонентом и учесть его стоимость в LinQ, либо исследовать detector-specific distillation как дополнительную разработку. [S072, S076, S080]

**F064. До аренды нужен контракт данных и измеряемый smoke.** Зафиксировать код/веса/лицензии, label map и независимые split; проверить forward+loss+backward+optimizer+EMA и validation на выбранном GPU, а также совместимость inference с LinQ. Параметры модели и размер checkpoint не определяют peak VRAM. DDP не объединяет память двух карт для одной копии; accumulation не делает BatchNorm эквивалентным большому физическому batch. Это инженерные условия предлагаемой процедуры, не наши измерения.


## F065 — W1-06: Три проверяемых режима для предполагаемой 24 GB карты

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Три проверяемых режима для предполагаемой 24 GB карты»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S070, S071, S073, S074, S075, S076, S077, S078, S079.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**Все числа в колонке «предложение» — ограниченная сетка гипотез, а не опубликованные лучшие hyperparameters или обещание fit.** Запускать последовательно по одному фактору. Число независимых эпизодов/камер и плотность разметки важнее фиксированной границы по числу JPEG. «Малый» ниже — мало независимых сцен и редких positives; «средний» — достаточно сцен для отдельных train/val/retention групп; «многокамерный» — отдельная задача generalization, не синоним большого числа кадров.

| Режим | Проверенный исходный ориентир | Предложение и диапазон для проверки | Условия остановки/смысл |
|---|---|---|---|
| **A — полный YOLO26s fine-tune** | S070 пример pretrained,50 epochs,imgsz640; S073 linear LR default, warmup3, nbs64, patience100 | Сначала 640; AdamW явно, `lr0` из {1e-4,3e-4,1e-3}, `warmup_bias_lr=0.0`, `warmup_epochs`1–3, `weight_decay` сначала default5e-4, `cos_lr=False`, `lrf=0.01`; `freeze=0`. Для сравнения сначала один LR3e-4. Окна20 и50 epochs; 100 только при продолжающемся независимом gain. Physical batch сначала1–2 для smoke, затем проба2/4/8/16 с запасом для worst-case и val; зафиксировать `nbs=16` **как наше отклонение от default64**, журналировать реальный accumulation | Средние данные/заметный domain shift. Без прироста целевых/retention метрик на val не переходить к длинной сетке. OOM или NaN — техническая неудача, не результат качества. |
| **B — YOLO26s freeze→unfreeze** | S070 пример20 epochs freeze10→30 epochs full; freeze11 фиксирует весь YOLO26 backbone,10 оставляет C2PSA | Этап1 10–20 epochs, `freeze=11`, AdamW LR3e-4–1e-3. Этап2 загрузить stage1 best и новый train с `freeze=0`, `resume=False`, ещё20–30 epochs, LR1e-4–3e-4. Держать total exposure сопоставимым с A; остальные параметры одинаковы. Малый набор: отдельный вариант `mosaic=0` против0.5; не добавлять это изменение в тот же freeze-ablation | Похожий домен/мало независимых сцен. Если stage1 не учит целевые объекты или full A заметно лучше на held-out сценах, freeze не выбирать. Сохранить и оценить stage1 best: stage2 может ухудшить качество. |
| **C — D-FINE-M conservative full fine-tune** | S074 AdamW2.5e-4, backbone2.5e-5, wd1.25e-4,132epochs/stop120; O365→custom56/stop48/warmup0; S075 clipping0.1/EMA0.9999 | Начать COCO detector-init через `-t`, вход640 и M custom YAML, не training-from-scratch. Первый LR из {1e-4,2.5e-4}, backbone=0.1×base; native wd/AMP/clip/EMA сначала оставить. Для короткого адаптированного окна30–56epochs явно согласовать `transforms.policy.epoch`, `collate_fn.stop_epoch` и финальную чистую стадию; пример проверяемой пары56/48 соответствует O365 custom schedule, но для COCO-init является **нашим переносом расписания**. Physical batch1–2 smoke, затем2/4/8 по измерению; val batch отдельно уменьшить. Первая цель effective batch=physical, stock accumulation здесь не найден | Challenger только после A/B и LinQ gate. Нельзя молча оставить stop120 при56epoch и назвать это исходным двухстадийным recipe. Полный132/120 run — следующий эксперимент при наличии бюджета, а не обязательный старт. |

У A/B `nbs=16` уменьшает накопление относительно default64 и позволяет чаще optimizer updates на маленьком наборе; это проверяемая гипотеза, не «улучшение по документации». При маленьком числе batch накопление может охватывать существенную долю эпохи, поэтому записывать реальные optimizer steps, а не только epochs. У trainer accumulation вычисляется как `max(round(nbs/batch),1)`, decay масштабируется соответствующим effective batch; warmup временно меняет accumulation. У DDP используется global batch в этой логике. Для A/B не переносить CLI-параметр `grad_accum_steps` RF-DETR: в Ultralytics иной интерфейс. [S071]

У YOLO явный AdamW с default `warmup_bias_lr=0.1` может дать совсем не тот старт, который ожидается от малого `lr0`; поэтому в предложении явно0.0. `optimizer=auto` сам ставит bias warmup0 и игнорирует заданный lr0: до10000 рассчитанных iterations AdamW с LR, зависящим от `nc`, после — MuSGD0.01. Если сравнить20 и100epoch с auto, можно одновременно переключить optimizer, что разрушает интерпретацию «длиннее лучше». Scheduler зависит от total epochs: первые20epoch от50epoch run — не тот же LR trajectory, что отдельный20epoch run. [S071]

У D-FINE stock engine optimizer/scaler step выполняется каждый batch. **Не найден готовый accumulation knob в прочитанном training loop**; не обещать effective batch32 на3090 через несуществующий YAML-флаг. При изменении total_batch_size официальный README предлагает линейную подстройку LR/EMA/warmup, но это ориентир, требующий проверки на target. Достаточно маленький batch меняет статистику BN и число шагов. Локальный patch накопления потребовал бы отдельной проверки loss normalization, clipping, AMP, scheduler/EMA frequency, tail batch и DDP. На короткий хакатон предпочтительнее прозрачный stock loop. [S075–S076]

### Альтернатива C: RF-DETR-M, не четвёртый обязательный run

Если D-FINE не проходит переносимость/интеграцию, заменить C на RF Medium с pinned кодом S077–S078. Опубликованные API defaults: `lr=1e-4`, **`lr_encoder=1.5e-4` (не lower-backbone по умолчанию!)**, AdamW, wd1e-4, batch4, accumulation1,100epochs, step schedule с default lr_drop100. Для экспериментального короткого окна30–50epochs разумно явно выбрать `lr_scheduler="cosine"` вместо ожидания drop после завершения run; это наше изменение. Сравнить encoder LR {1e-5,5e-5,1.5e-4} при base1e-4 только после baseline. M input576, L704, стандартный detection input должен делиться на `patch_size*num_windows`=32. Увеличение M до704 проверять как отдельный resolution factor. [S077–S079]

Старт physical batch1–2, после smoke определить конкретное целое; `grad_accum_steps`1–8 только для выбранного nominal effective batch, например16=4×4 или2×8 на одной карте. Это математический target, не утверждение fit/эквивалентности. Model constructor `gradient_checkpointing=True` — ещё один memory/compute tradeoff, не нулевой по времени. `freeze_encoder` существует на уровне ModelConfig; не переносить `freeze=11` из YOLO. Для воспроизводимости явные batch/accum предпочтительнее auto: auto может менять effective batch между GPU, а LR автоматически не становится сопоставимым. В snapshot `eval_batch_size` задаётся отдельно и авто не пробуется. [S077]

Включить `early_stopping=True`, patience10–15 проверок, `early_stopping_min_delta=0.001` как исходный API default, **не как требуемый уровень точности**; `best_model_metric="map"`, `use_ema=True`, `early_stopping_use_ema=True`, `run_test=False`, `log_per_class_metrics=True`. По умолчанию validation EMA-only, aggregate primary mAP зеркалирует EMA; `eval_base_model=True` добавляет diagnostic base pass. Не сравнивать base checkpoint одного run с EMA другого без записи. Не включать auto test на lockbox каждый epoch. [S077–S078]


## F066 — W1-06: Разрешение, длина run и критерий выбора

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Разрешение, длина run и критерий выбора»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S070, S073, S074, S075, S076, S078, S079.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**F066. Сначала узнать размер нужных объектов после resize, потом тратить память на разрешение.** Для касок/телефонов/элементов привязи сравнить исходные и resized bounding boxes: доля исчезнувших/едва различимых instances, распределение bbox width/height/area, доля occluded/truncated. Для YOLO после640 кандидаты960 и1280, для D-FINE сначала640 и только затем отдельно согласованное изменение resize/base_size/eval_spatial_size. Это сетка нашего исследования, не подтверждённый прирост. При удвоении стороны растёт число пикселей, а training memory/latency зависят и от архитектуры. ROI/person crops могут быть экономнее общего high-res, но меняют распределение и downstream association; передача соседней ветке. [S070,S075,S079 + инженерный вывод]

На малом наборе не назначать длинный run потому, что «train loss ещё падает». На среднем допускается full network и более длинное окно при improving held-out curves. На многокамерном — смешивать камеры/освещение/масштаб объектов в train, ограничивать доминирование длинных клипов; проверять per-camera/per-condition и worst-group качество, а не только aggregate AP. Oversampling редких классов/камер — параметр протокола, он может переучить несколько людей/сцен; не считать повторённые кадры новыми независимыми примерами.

Сравнивать short-vs-long в двух смыслах: (1) те же первые/поздние checkpoints одного заранее заданного schedule, что показывает пользу продолжения; (2) полностью заданные короткий и длинный schedules при одинаковом init и data, что сравнивает конкретные recipes. Из-за scheduler total horizon эти вопросы не эквивалентны. Ранний слабый transformer не объявляется окончательно проигравшим только по первым эпохам; длинное окно разрешается, если позволяет бюджет и нет retention деградации. Бюджет учитывать по реальному wall time, optimizer steps и изображениями, включая validation, загрузку и запись артефактов; цифры времени заранее неизвестны.

**F066. Stock best не равно «лучший промышленный alert».** YOLO detection fitness в прочитанной версии использует mAP50:95 с весом1; это не event recall при FP/camera-hour. D-FINE выбирает по первому COCO statistic (bbox AP) и имеет best_stg1/stg2/EMA restart логику. У O365 YAML `epochs:56 # Early stop` — **фиксированное ограничение**, не adaptive patience. У RF early stopping выключен default и монитор требует явной настройки. [S073,S074,S076–S078]

Предлагается заранее задать приоритет: per-class retention floors и целевой recall/FP constraints; среди прошедших — target validation metric. На train/val можно выбирать checkpoint и пороги. Если val очень мал и используется многократно для всех решений, выделить SELECT для окончательного выбора между немногими финалистами; lockbox оставлять до фиксации модели, preprocessing и порогов. Уровни floors и FP budget должны прийти из кейса/оценки, здесь численно не выдуманы. Для stock training сохранить несколько кандидатов, затем выполнить внешний отбор; не предполагать, что штатный best.pt автоматически оптимизирует новый criterion.


## F067 — W1-06: Когда теряются нужные классы и generalization

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Когда теряются нужные классы и generalization»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S072, S076, S080.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**F067. Разделять четыре механизма, иначе «catastrophic forgetting» скрывает ошибку конвертации.**

1. **Выход исключён из новой онтологии.** Если names содержит только каску и жилет, person/phone отсутствуют по контракту. Freeze не возвращает отсутствующие выходы. Решение — согласовать union label map либо оставить общий detector как отдельный компонент.
2. **Неверный перенос head.** В pinned Ultralytics уже есть remap строк по нормализованным именам, включая one-to-many/one-to-one classification branches; train ставит target names до load. Совпадение строковых имён полезно для initialization, но `worker` не автоматически `person`, а `car` не автоматически промышленный forklift. Не утверждать, что «весь head всегда сбрасывается»: это неверно для данной версии. Сохранить log matched/unmatched/remapped и проверить id→name→output на примерах. [S072]
3. **Старый класс/объекты остались в кадре, но не размечены.** В обычном полностью supervised detector это не бесплатные unlabeled positives. Узкий PPE export часто скрывает людей/транспорт; объединить JSON/YAML недостаточно. Для каждого train image требуется полный набор необходимых target-меток либо специально реализованная partial-label/ignore логика. Простое добавление старых class names в YAML не сохраняет качество.
4. **Нормальная адаптация, но сужение распределения.** Одна дневная камера, несколько работников и соседние кадры могут улучшить val из того же клипа и ухудшить другие камеры/ночь/пыль. Снижение LR/freeze/early stop — меры риска, но не доказательство generalization. Нужен replay разнообразных общих сцен и независимые held-out группы.

У D-FINE `map_class_weights` при одинаковой форме копирует тензор целиком, не проверяя смысл классов; при разных размерах использует `obj365_ids`. Для произвольной custom онтологии default COCO↔O365 mapping не является semantic mapping. Исключение в head adjustment перехватывается, затем загрузка фильтрует несовместимые формы. Поэтому фраза README «mapping optional» означает возможность продолжить загрузку, **не гарантию правильного head-init или retention**. Для helmet/vest/harness проверить, что mapping не копирует случайный класс; если достоверного соответствия нет — исключить эти head tensors из init контролируемо, сохранить полный transfer log и проверить результат. Это особенно важно, когда одинаковое `nc` скрывает разный порядок классов. [S076]

Replay: сформировать разрешённый размеченный train retention subset со старыми необходимыми классами и hard negatives, отдельный retention-val не из этих эпизодов. Сравнить new-only против mixed train с одинаковой новой онтологией/инициализацией; варьировать долю replay как заранее выбранный sampling factor, а не добавлять lockbox кадры. Самая полезная начальная пропорция неизвестна. Отдельно измерять ΔAP/recall каждого старого класса относительно исходного detector на фиксированном retention-val и domain slices. Если классы отличаются, сравнивать только согласованные semantic endpoints; для отсутствующих у исходной модели PPE AP baseline не существует.

S080 показывает detector-specific distillation как альтернативу без исходных данных, поэтому формулировка guide «merge is the only reliable way» слишком абсолютна как научное утверждение. Но S080 — Fast R-CNN с конкретной loss и proposal sampling; generic `distill_model` в current YOLO не следует считать готовой защитой arbitrary old classes. Реализация и проверка такого метода — отдельный риск и teacher-memory overhead. Самый прозрачный первый вариант в малое время — правильные labels+replay+retention gate, а не новый continual-learning метод.


## F068 — W1-06: Различающий эксперимент: адаптация без утраты базовых функций

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Различающий эксперимент: адаптация без утраты базовых функций»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**Вопрос:** на зафиксированном датасете даёт ли freeze→unfreeze лучшее целевое качество при одинаковой онтологии/бюджете, и нужен ли replay, чтобы удержать person/технику/phone? Это экспериментальный план, не выполненный опыт.

**Входы:** разрешённые pretrained checkpoint и code snapshot; immutable annotation manifest; union ontology; train-new, train-replay, target-val, retention-val; при достаточном числе групп SELECT; lockbox. Нужны также камеры/эпизоды/дата/освещение, bbox/visibility metadata и заранее заданный FP/retention критерий. Требование всех COCO80 классов не предполагается: удерживать те, которые реально нужны выбранным сценариям.

**Процедура:**

1. Audit label map/boxes, missing labels и дубликатов; визуально проверить конвертацию. Split сначала по независимым camera/scene/episode groups, затем извлекать кадры/crops; сохранять parent lineage. Любая общая сцена между splits отменяет соответствующее заявление независимости. Если камер мало, честно обозначить within-camera temporal test и отдельно отсутствие evidence unseen-camera.
2. Smoke одного GPU без аренды до отдельной авторизации ресурсов: минимальный physical batch, наиболее плотные изображения и максимальный возможный multiscale input, несколько полных шагов с optimizer и EMA, checkpoint save/reload, validation. Записать peak allocated/reserved, `nvidia-smi`, batch, AMP, max targets, loss finite, train/val time; повторить после изменения resolution. Успех mini smoke не доказывает worst-case fit на всём run.
3. На одном init/seed/640 сначала A и B с одинаковым mixed train и фиксированным общим бюджетом; сохранить learning curves и stage candidates. Дополнительно A new-only против A mixed при одинаковой union ontology — изолирует replay, а не удаление head outputs. Не совмещать replay и разрешение в одном сравнении.
4. Проверить валидность стокового best и externally selected checkpoint; оценить target-val и retention-val тем же evaluator и class map. Для подходящих финалистов повторить seeds, число повторений определить доступным ресурсом до просмотра lockbox. Один seed — screening, не доказательство устойчивого преимущества.
5. Только если остаётся нужный gap — challenger C или RF substitute; затем отдельный размер входа на победившем режиме. Экспорт/операторы/квантование/real latency на LinQ — отдельный gate соседней ветки, включая parity FP32→export→target runtime.
6. Зафиксировать config/checkpoint/preprocess/threshold/event logic; SELECT выбрать финалиста, lockbox открыть один раз. По lockbox ничего не перенастраивать; обнаруженные проблемы становятся следующим циклом с новым независимым тестом.

**Метрики:** AP50:95/recall по каждому классу и размеру объекта; miss rate при согласованном FP budget; Δ старых классов относительно pretrained на retention-val; per-camera/lighting/occlusion slices, worst-group; доверительные интервалы/вариативность по эпизодам и seeds, без псевдоувеличения n соседними кадрами. Внешние event recall, FP/camera-hour, duplicates, late alerts, p50/p95 event-to-alert latency и measured LinQ throughput — по протоколу соседней evaluation/video ветки; detector AP их не заменяет. Записывать exposure source-camera-hours, optimizer updates и wall time, не только epochs.

**Артефакты:** SHA кода и resolved env; checkpoint URL+SHA256; license notices; class mapping и load logs; хеши split/annotations, group manifests, parent crop/frame lineage; exact merged config; seed/GPU/AMP/physical batch/accum/nbs; scheduler LR trace+optimizer step counter; checkpoint selection rule; raw per-image predictions/GT, per-class/per-group metrics; кривые и retention deltas; smoke memory log; checkpoint path+SHA256, export/parity handoff. Не сохранять только итоговую картинку mAP.

**Возможные исходы и решение:**

- B лучше target и проходит retention floors: выбрать B; упростить финальный inference по лучшему stage checkpoint.
- A лучше held-out камеры, B недоадаптируется: выбрать full A, не продлевать freeze по привычке.
- Mixed сохраняет нужные классы, new-only их теряет: replay становится частью обязательного recipe; его отсутствие — fail condition.
- Все detector runs теряют старые классы или нет полной разметки: остановить заявленную единую модель; исправить labels/ontology либо измерить отдельный общий detector в pipeline.
- C/RF улучшает detector metric, но не проходит LinQ/latency: это research candidate, не готовое финальное решение.
- Ни один режим не различим на числе независимых событий: выбирать более простой воспроизводимый вариант и расширять данные; не объявлять победу по дробной разнице aggregate mAP.

Успех на target-val не доказывает unseen-camera generalization, промышленную надёжность, корректность behavioral event, экспортную совместимость, сохранение качества после INT8 или соблюдение few-second alert latency. Даже успешный lockbox ограничен его охватом и размером.


## F069 — W1-06: Негативные результаты и передача

- Происхождение/locator: [W1-06](_WORK/W1_06.md), раздел «Негативные результаты и передача»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S074, S082.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved. Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.


**F069. Нет первичного доказательства оптимального числа эпох, LR, batch или 24 GB fit для нашей конкретной онтологии и кадров.** Есть официальный recipe и исполняемые defaults; отсутствуют наши labels, GPU smoke, LinQ operator/runtime evidence. Поэтому нельзя обещать «50 эпох достаточно», «freeze всегда повышает accuracy», «Objects365 гарантирует лучший перенос», «1280 решает маленькие СИЗ» или «2×3090 решат память». D-FINE прямо предупреждает о возможном overfit простых категорий при richer pretraining. [S074,S082]

Передача W1-02/модели: pin weights/checksum/licensing и выбор COCO/O365-init отдельно; YOLOX-s оставить совместимостным fallback, не добавлять ещё один sweep до результатов A/B. Передача data-ветке: union classes, annotation completeness, replay rights, group lineage и hard negatives. Передача evaluation: retention floors, checkpoint metric, SELECT/lockbox и cluster uncertainty. Передача resource/scheduling: physical batch smoke, стоимость validation/EMA/artifacts; никакой авторизации аренды отсюда не следует. Передача LinQ/export: выбранные graph/head/resolution, preprocessing, parity, измерение latency и quantization — не выполнять в рамках этой ячейки. Передача video/behavior: detector outputs не являются использованием телефона, падением или фактом опасного сближения.

Точные открытые вопросы: какие старые классы действительно нужны в выбранных сценариях; сколько независимых камер/эпизодов и positives; полна ли разметка человека/техники на PPE-кадрах; можно ли легально смешать replay; какие объективные retention/FP/latency ограничения; разрешён ли исходный YOLO license path; какая реальная LinQ конфигурация/SDK; какая GPU/версия окружения доступна для smoke; есть ли бюджет повторных seeds. Ответы меняют рецепт, а не заполняются вымышленными оценками.


## F070 — W1-07: Решение для команды

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Решение для команды»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S083, S084, S085, S086.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F070. Первая инвестиция — исправить целевую семантику и полноту меток, затем выбирать трудные примеры.** Высокоуверенная детекция без GT не обязательно false positive: это может быть пропущенная аннотация. Если автоматически добавить её как hard negative, модель получит прямо противоположный сигнал. Co-mining исследует именно повреждение обучения неразмеченными объектами [S084]; CLOD выделяет missing/spurious/wrong-class/wrong-location ошибки [S085]. Рекомендация: каждую выбранную ошибку сначала направлять на проверку человеком и только после неё — в положительные, проверенные отрицательные или `unknown/ignore`.

**F070. Практический baseline отбора — смесь причин ошибок, неопределённости, разнообразия и случайного аудита на уровне клипа/эпизода.** Не брать тысячи соседних кадров одного манекена. Не ограничиваться низким confidence: уверенные ложные тревоги и объекты без единой детекции такой отбор пропускает. Active learning для детекции даёт основание использовать uncertainty и учёт дисбаланса [S086]; доли потоков и способ дедупликации ниже — наш предлагаемый протокол, а не опубликованный оптимум.

**F070. За оставшееся время сначала ручной error ledger + QA и доразметка; сложный OHEM/custom loss — резерв.** OHEM — конкретный алгоритм отбора RoI по loss внутри обучения Fast R-CNN, а не синоним любой подборки отрицательных видео [S083]. Его интеграция в другой детектор не доказана этой статьёй. Исправление исходных данных не меняет граф inference; однако новый checkpoint всё равно требует повторной проверки экспорта, качества и скорости на LinQ. Ни ускорение, ни рост accuracy заранее не обещаем.

**F070. Нельзя требовать от разметчика невидимой причины.** «Лежит» наблюдается иначе, чем «упал»; «двигатель работает» иначе, чем «машина перемещается»; предмет возле уха иначе, чем доказанный телефонный разговор. Разделить наблюдаемое состояние, переход, предмет и контекст правила. Для неразличимого материала сохранять неопределённость, а не выдумывать отрицательный класс. Это инженерный вывод, согласованный с causal/observability ограничениями W1-04.

Основание требований кейса — `_WORK/CASE_NOTES.md`, прямые визуальные наблюдения root по официальному PDF, с. 5, 7, 13. В этой ветке PDF заново не рендерился. Метрики своевременности, FP/наблюдаемый camera-hour, дубликатов и coverage берём из W1-01; модельные и временные решения W1-02–04 здесь не пересказываются.


## F071 — W1-07: Что различать в петле ошибок

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Что различать в петле ошибок»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S087.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Три разных процедуры полезны в разных местах:

| Процедура | Что уже известно | Что выбираем | Основная опасность |
|---|---|---|---|
| Offline hard-negative mining | После просмотра подтверждено, что целевого нарушения нет | Неправильно сработавшие клипы/tracklets для тренировки или правил | Неполная разметка делает настоящий positive «фоном» |
| Active learning | Истина ещё не известна | Материал, который сначала предстоит разметить | Uncertainty отражает дрожание/шум и не видит уверенных ошибок |
| Annotation QA / label-error discovery | Есть метки и независимые предсказания/проверка | Подозрительные метки, их отсутствие и противоречия | Принять мнение текущей модели за истину и закрепить bias |
| OHEM | Есть тренировочные labels и вычисленный loss | Трудные RoI внутри minibatch | Большой loss из-за ошибочных labels получает повышенный вес |

**F071. Error ledger должен фиксировать причину, а не только FP/FN.** Для каждой записи хранить `error_id`, исходный файл/URL и SHA256, `source_group_id`, `camera_id`, `scene_id`, время/PTS, `event_id`, `track_id`, split, версия labels/модели/rules, prediction, GT до и после проверки, доказательный crop и полный контекст, reviewer, решение и downstream action. Минимальные причины: объект пропущен; неправильный класс; bbox; duplicate; фон; track/association; неверное состояние/переход; зона/контекст; задержка; GT missing; GT ambiguous; incomplete coverage; ошибка дедупликации. У объекта может быть одна основная причина и вторичные теги.

TIDE даёт первичную таксономию ошибок детектора и анализ через отдельные oracle corrections [S087]. Мы добавляем событийные причины. TIDE на bbox не объясняет ложное оповещение при правильной детекции телефона или задержку уведомления; гипотетический oracle-выигрыш не равен эффекту реального retraining. Прежде чем обвинять модель, сверить timestamps, видимость, scope labels и соответствие GT версии evaluator.


## F072 — W1-07: Матрица обязательных трудных пар

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Матрица обязательных трудных пар»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Всё в таблице — предлагаемые правила разметки и сбора; это не подтверждённые результаты модели.

| Пара | Что доразмечать | Какие отрицательные/контрольные эпизоды искать | Что нельзя заключать |
|---|---|---|---|
| Человек / манекен | `person`, `mannequin` или проверенный не-человек; трудность/видимость; полный силуэт и исходный кадр | Манекен с PPE/без PPE, плакат, отражение, подвешенная одежда; неподвижный настоящий человек, человек с тяжёлыми окклюзиями | Неподвижность не доказывает манекен. Исключение всех неподвижных person может убрать unconscious/lying |
| Телефон / инструмент | Видимый предмет, bbox/track, связь с рукой/человеком; `phone/tool/unknown`; действие отдельно | Рация, сканер, отвёртка, измеритель, перчатка у лица; телефон в разных положениях и масштабах | Наличие phone не доказывает использование; crop руки без контекста не доказывает нарушение рядом с техникой |
| Прилёг / падение | Отдельные `lying_state`, `fall_transition`, видимый onset и post-state, `intent_unknown`; возможность наблюдать переход | Намеренное приседание/укладывание, ремонт лёжа, ползание, спотыкание с восстановлением, уже лежащий человек при старте видео | Финальная поза не устанавливает причину. Манекен, упавший в постановке, не заменяет человеческое падение; safety-риск создания реальных падений не нужен |
| Техника стоит / движется | ID техники, интервалы наблюдаемого перемещения/остановки/неопределённости; движущиеся части отдельно от перемещения корпуса | Стоящий погрузчик рядом с движущимся работником; поворот колёс, свет/тени, камера дрожит; техника начинает/прекращает движение | Нулевое смещение bbox при движении вдоль оптической оси не доказывает остановку; `engine_on` не равен moving |

Собирать пары в сходных ракурсах, масштабе, освещении и фоне; иначе classifier запомнит «манекен — белая студия, человек — цех». Для каждой пары нужны и positive controls: исправление FP не должно подавить настоящих людей/телефоны/падения/движение. Не добавлять новый класс, если формат и downstream consumer его не поддерживают: можно хранить distractor taxonomy в QA manifest и использовать корректно проверенный background или отдельную задачу классификации. Решение зависит от выбранного pipeline.


## F073 — W1-07: Контракт partial labels: неизвестно не означает отрицательно

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Контракт partial labels: неизвестно не означает отрицательно»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S084, S088.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F073. Единицей полноты должен быть `(asset/interval, class, region)`; пустой label-файл сам по себе ничего не доказывает.** Предлагаемые поля manifest:

```text
asset_id, source_group_id, original_sha256, camera_id, scene_id, split
interval_start_pts, interval_end_pts, roi_id
reviewed_classes, exhaustive_classes, verified_absent_classes
annotation_status={unreviewed, partial, exhaustive, ambiguous}
ignore_regions, visibility, label_schema_version, reviewer_id, qa_status
```

Например, source PPE dataset с касками и людьми не становится phone-negative dataset оттого, что в нём нет класса phone. Отсутствие fall labels в object dataset ничего не говорит о лежащих людях и событиях. Изображение, где размечен только один из нескольких людей, нельзя без проверки использовать для exhaustive person supervision.

Два режима неполноты различаются: **category-level partial** — размечены не все классы; **instance-level sparse** — пропущена часть объектов одного класса. Mask по неизвестным классам помогает первому, но не исправляет пропущенных людей в уже размеченном классе. Clip-level метка «есть телефон» не локализует каждый телефон и не задаёт onset нарушения.

Рецепты по приоритету:

1. **Полностью проверить ограниченное целевое подмножество.** Для каждой выбранной единицы просмотреть весь релевантный интервал/ROI и все train classes, а не один model proposal. Это предпочтительный путь при ограниченном сроке: совместим с обычным supervised trainer и делает отрицательные labels осмысленными.
2. **Ignore неизвестных классов/областей/интервалов**, только если loss/assigner и evaluator действительно поддерживают нужную семантику. После export/import проверить, что ignore не превратился в background. Один `iscrowd` или текстовый атрибут не считается универсальным training mask. При отсутствии поддержки — исключить материал из соответствующего supervised loss или доразметить, а не надеяться на metadata.
3. **Partial-label-aware training.** CenterNet2/Federated Loss показывает работу с неполной категориальной аннотацией LVIS через подмножества классов [S088]; это альтернатива для соответствующего trainer, не готовая поправка YOLO и не лекарство от любого missing instance. Co-mining добавляет псевдометки между двумя видами изображения [S084]. Усложнение оправдано лишь если объём неполных данных и ожидаемая польза превышают риск интеграции; нужны отдельная абляция и проверка seed/model bias.
4. **Pseudo-labels — кандидаты на review.** Не записывать высокую уверенность как verified truth. В train допустим отдельный provenance `pseudo`, confidence и teacher version, со специально выбранным loss, а human/GT/pseudo учитывать раздельно. Манекены и инструменты особенно опасны как self-training positives. В validation/SELECT/lockbox псевдо-GT запрещён.

Не предлагать «выкинуть всё с высоким loss»: это может удалить редкие истинные опасности. CLOD и model–annotation disagreement полезны для очереди QA, а не для автоматической переписи истины. Для train-ranking предпочтительны out-of-fold predictions по независимым группам; при нехватке ресурсов использовать отдельный frozen teacher, указать его training exposure и ограничение. In-sample score от запомнившей примеры модели имеет слепые зоны. OOF здесь — наш защитный протокол, а не утверждение о выполненном CLOD запуске.


## F074 — W1-07: Разметка времени и QA

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Разметка времени и QA»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S089, S090.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F074. Размечать целый эпизод с предысторией и выходом, затем генерировать окна; не наоборот.** Сохранить исходные PTS/timebase, длительность и sampling mapping. У события нужны как минимум `event_class`, entity IDs, onset/end, `first_observable_time`, continuing-state, причины ambiguous/occluded, censoring на начале/конце клипа, zone/rule version. Временные границы с реальной неопределённостью хранить интервалом, например onset в `[t_a,t_b]`, а правила сопоставления согласовать с W1-01 до оценки.

Для fall start должен относиться к видимому переходу; для lying start — к видимому лежачему состоянию; уже лежащий при первом кадре — left-censored onset. Для движения техники просмотреть остановку, начало перемещения и возврат к остановке. Для phone tool-check нужен объектный crop и синхронный полный кадр. Будущие кадры могут помочь установить итоговую аннотацию, но `first_observable_time` не переносится задним числом, если доступные тогда признаки были неоднозначны; online replay видит только префикс. Конкретные automata/длительности оставлены W1-04.

Порядок QA:

1. Версионировать краткую инструкцию с разрешёнными/запрещёнными примерами всех четырёх пар; определить bbox convention, occlusion, неизвестный класс, границы и split policy. Прогнать пилот на контрастных клипах; расхождения сначала исправляют инструкцию.
2. Первому annotator дать исходный клип; для части QA и всех критичных разногласий второму дать клип независимо, без model confidence и ответа первого, чтобы уменьшить anchoring. Model-assisted boxes можно использовать для скорости, но независимый просмотр нужен для misses.
3. Автоматические проверки до merge: timestamp range/порядок, bbox вне кадра/нулевой площади, запрещённые классы, ID collisions, дубли, broken tracks, состояние вне видимости, incompatible labels, интервалы без coverage, отсутствие provenance. Их прохождение не доказывает правильность смысла.
4. Человек проверяет пропущенные объекты в полном кадре, начала/концы, ключевые transitions, occlusion и случайные промежуточные кадры. Интерполяция bbox не делает интерполяцию класса действия достоверной. Переходы нуждаются в просмотре, а не в механическом переносе метки между endpoints.
5. Сравнить независимые ответы по классу, объектам, границам и unknown; adjudicator разрешает спор с reason code. Не усреднять несовместимые временные границы без просмотра. Не принуждать consensus на физически неразличимых кадрах.
6. Сохранить label diff, версии инструкции и adjudication log. Закрыть QA до train/export; провести round-trip проверку нескольких positive/negative/ignore/track примеров в конечном training формате. Рабочее CVAT QA `Ground Truth job` — это gold для проверки разметчиков, **не модельный lockbox**.

CVAT документирует GT-based QA/review и независимые replica jobs/merge; availability зависит от редакции, а consensus ограничен 2D [S089, S090]. Авто-аналитика не является доказательством причинной семантики падения. Никакая установка CVAT здесь не выполнена и не требуется для самого протокола: при отсутствии подходящих возможностей достаточно локальных manifests и двух независимых проходов review.


## F075 — W1-07: Конкретная итерация error analysis → отбор → QA → доразметка → проверка

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Конкретная итерация error analysis → отбор → QA → доразметка → проверка»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F075. Предлагаемый рабочий цикл:**

1. **Заморозить исходное состояние:** checkpoint, preprocessing, inference resolution, labels, rules, thresholds, dataset manifests и evaluator. Создать split по группам до извлечения кадров/кропов.
2. **Прогнать train/unlabelled mining pool и development validation.** Train используется для кандидатов; validation — для классификации проблем и оценки. Validation-клипы не переносить в train: по найденному failure type искать новые train-side независимые эпизоды.
3. **Собрать четыре очереди:** подтверждённые уверенные FP; FN из полного ручного просмотра случайно выбранных интервалов/из GT; uncertain/disagreement; случайные и разнообразные клипы, включая фон без детекций. Последняя очередь обязательна: ни confidence ranking, ни model disagreement не находят все общие blind spots.
4. **Дедуплицировать по source clip/event/tracklet и сцене**, затем выбрать представителей разных камер, scale/occlusion/lighting, трудных пар и классов. Score uncertainty вычислять только как ranking proxy. Не считать соседние кадры дополнительными независимыми случаями. Сохранить selection seed, кандидатов, причины выбора/отказа и фактически затраченное annotator time.
5. **QA кандидатов → полная целевая доразметка** выбранных units по контракту выше. Возможные исходы: confirmed hard negative; overlooked positive; bad existing annotation; ambiguous/ignore; технический сбой. Решение «модель ошиблась» не предопределено.
6. **Выбрать исправление по причине.** Annotation → labels; недостаток примеров → train samples; duplicate/association → tracker/event layer; недоказанная причина → ontology/unknown; объективно невидимый предмет → сценарный scope. Не тратить retraining на ошибку timestamp или неверный zone config.
7. **Дообучить только разрешённый train**, сохраняя обычные positives и background. Не делать minibatches только из mined negatives; проверить забывание на прежних срезах. Число optimizer updates и schedule фиксировать при сравнении, так как добавление данных меняет смысл «столько же эпох».
8. **Повторить независимую development оценку**; выбрать готовую систему и пороги на validation/опциональном SELECT. Только затем один финальный lockbox audit. Если выявлена новая проблема lockbox и система изменена, прежний lockbox становится development: нужен новый нетронутый набор или честная маркировка отсутствия независимого финального теста.

При маленьком объёме начать с ручных карточек ошибок и stratified group sampling. Embedding clustering, committee disagreement и сложный AL framework добавлять после появления измеримой избыточности/ручного bottleneck. Не придумывать коэффициенты score без данных; random selection — обязательный соперник. Имеющиеся признаки/эмбеддинги можно переиспользовать для offline diversity, но новый encoder не требуется в inference на LinQ.


## F076 — W1-07: Leakage: обязательные границы

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Leakage: обязательные границы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S091.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F076. Split — свойство происхождения, а не имени файла.** Все производные одного source episode: raw clip, соседние кадры, ROI crop, resized/transcoded copies, annotations, flow, pose, embeddings, pseudo-labels и augmentations — наследуют одну split group. Match по SHA256 найдёт точные копии, но не перекодировку/обрезку; perceptual hashes/embeddings помогают обнаруживать кандидатов, ручная проверка подтверждает. DataEval демонстрирует именно video duplicates и cross-split sequence matching [S091]. Универсальный порог pHash из tutorial не переносим.

Два уровня честности:

- Для заявления о новых камерах/сценах группировать и исключать совпадение камер/сцен между train, validation, SELECT и lockbox; близкие фрагменты/повтор одной постановки держать вместе. Один event на нескольких камерах также объединить, иначе действие известно из другого ракурса. При повторных людях/сменах документировать дополнительную зависимость.
- Для будущего времени на известной камере можно проектировать отдельный temporal holdout с gap, но он **не** подтверждает camera-independent generalization и по данному brief не заменяет независимый набор. Если данных хватает только на одну сцену, написать, что независимость по сценам не проверена, а не называть random-frame split тестом.

Lockbox нельзя включать в mining, teacher fitting, pseudo-label generation для train, embeddings-based selector fitting, threshold/checkpoint/ensemble choice. Дедупликационный audit может читать fingerprints для контроля пересечений, не раскрывая labels разработчику; его цель — integrity, не tuning. Если lockbox labels ошибочны, отдельный reviewer делает protocol-based QA без предпочтения конкретной модели, правка получает версию, все сравниваемые системы переоцениваются; model selection после раскрытия требует нового holdout.

Метрики на curated hard-negative challenge set — диагностические. Переобогащённый телефонами/манекенами набор не оценивает natural prevalence, реальную FP/час или precision. Сохранить отдельно непрерывные случайно выбранные интервалы с известным observed time. Нельзя разбить challenge-clips на множество кадров и получить искусственно узкий confidence interval.


## F077 — W1-07: Различающий эксперимент, который нужно выполнить

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Различающий эксперимент, который нужно выполнить»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F077. Вопрос:** даёт ли QA + целевой отбор больше полезного улучшения за равное время разметки и сопоставимые training updates, чем случайная доразметка или продолжение обучения на прежних данных?

**Входы/предпосылки:** рабочий baseline checkpoint; разрешённый video pool с provenance и правами; reviewers и adjudicator, краткая ontology; непрерывные negative intervals и независимые положительные эпизоды всех выбранных сценариев; group manifests; установленный trainer с явно известной семантикой ignore; вычислительные ресурсы для фактических прогонов, которые ещё предстоит подтвердить. Vast.ai 3090 — только обсуждавшийся ресурс, не аренда/разрешённая трата. Финальная нейросеть обязана исполняться на LinQ; memory/operators/configuration пока неизвестны. Для QA и ранжирования не заявляем никакой GPU необходимости или времени выполнения.

**Дизайн:**

| Ветка | Данные | Обучение/цель сравнения |
|---|---|---|
| A | Исходный train, текущие метки | Продолжение с фиксированными updates: контроль гипотезы «просто дольше» |
| B | Исходный train + случайно выбранные группами клипы; QA по единому протоколу | Контроль выигрыша от новых данных и внимания людей |
| C | Исходный train + описанная смесь mining/uncertainty/diversity/random; тот же QA | Проверка ценности целевого отбора при равном annotator time |
| D, если ресурсы позволяют | QA исправляет только существующий train без новых клипов | Отделение эффекта исправления меток от пополнения покрытия |

Перед ветвлением одинаково исправить критические технические ошибки manifest/split; это integrity prerequisite. Смысловые подозрительные labels остаются предметом заранее оговорённой ветки D/общего QA. Не очищать одну ветвь скрытно лучше другой. Для B/C зафиксировать равный бюджет **времени людей**, учитывать просмотр, review, adjudication и export; число кадров/boxes может отличаться и должно быть записано. Отдельно измерить selection overhead. Если ресурсов нет на несколько ветвей, честный минимум — B vs C; A оставляет важный контроль, D полезна для attribution.

Все ветки стартуют с одного checkpoint и сопоставимого schedule/числа updates, preprocessing и разрешённых аугментаций; повторные seeds при возможности, иначе явно один run. Не менять architecture/rules одновременно с данными. Первая оценка — при одинаковом frozen operating point, чтобы увидеть собственно эффект данных; дополнительная — с одинаковой процедурой настройки на validation. При наличии SELECT он закрывает выбор ветки; его не использовать как новый train pool. Lockbox открывать после выбора.

**Оценка:** использовать W1-01: timely event recall с числом независимых событий, FP notifications/observed camera-hour, duplicate rate, задержки, coverage. Дополнительные диагностические величины: ошибки по каждой из четырёх пар; misses среди вручную проверенных случайных no-detection intervals; доля реальных label errors в QA очереди; число подтверждённых positives/negatives/unknown, уникальных source groups; annotator minutes на confirmed issue/эпизод; boundary disagreement до/после adjudication; regression на прежних классах. Указывать denominators и uncertainty с групповой единицей; frame accuracy не основная цель. Evaluation labels полностью проверяются независимо от выбора кандидатов.

**Артефакты:** frozen split manifest и duplicate audit; selection manifest/seed/reasons; source и label hashes; error ledger; annotation schema/instructions/diffs; reviewer/adjudication log и время; trainer config/commit/checkpoint hash; prediction/event logs с PTS; сравнительная таблица и карточки regressions; отдельный LinQ replay report после допуска checkpoint. Эти артефакты предлагаются, сейчас не созданы и не выполнены.

**Развилки результата:** C лучше B на независимых эпизодах при сопоставимом бюджете и без недопустимого падения recall/роста задержки → продолжать целевой цикл; B≈C → упростить до stratified random + QA, не платить за сложный selector; D даёт основной эффект → приоритет ревизии labels; FP меньше, но реальные positives потеряны → уменьшить domination negatives/пересмотреть ontology; улучшение только на challenge-наборе → не заявлять эксплуатационный выигрыш; все ветки одинаковы → проверить observability/domain coverage/семантику pipeline, а не добавлять эпохи автоматически.

**Что успех не докажет:** camera-independent transfer при совпадающих сценах; безопасность во всех условиях; количественный выигрыш на неизвестном LinQ до запуска; general-purpose superiority active learning; обнаружение невидимых причин; чистоту публичных pretrained datasets от наших тестовых роликов. Для последнего сохранять источник и отдельно отметить неизвестную pretraining exposure, особенно для популярных публичных fall videos.


## F078 — W1-07: Противоречия и отрицательные результаты поиска

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Противоречия и отрицательные результаты поиска»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- OHEM намеренно усиливает hard loss; sparse-label исследования показывают, что тот же hard negative может оказаться неразмеченным positive. Поэтому усиление сложности без QA имеет противоположные последствия. Это совместимые результаты при разных assumptions, а не обещание «включить оба и получить сумму gains».
- Ignore unknown уменьшает ложную supervision, но полное удаление отрицательных классов может ослабить background learning; CenterNet2 явно обсуждает этот компромисс. Предпочтительный короткий путь — небольшой exhaustive subset + реальные hard negatives, а не тотальное игнорирование фона.
- CVAT автоматизирует проверку согласия с GT, но не создаёт правильный GT и часть функций ограничена редакцией. Для команды нельзя считать SaaS analytics уже доступными.
- Не найден и не установлен универсальный источник/алгоритм, гарантирующий различение «прилёг/потерял сознание» или stationary/moving по одному кадру. Отсутствие такого доказательства не означает невозможность temporal решения, но требует правильной постановки и видимых признаков.
- Источники не дают основания назначить команде конкретный рост accuracy, число GPU-часов, annotation minutes или окупаемость аренды. Эти числа должны появиться из эксперимента.


## F079 — W1-07: Передача соседним веткам и точные открытые вопросы

- Происхождение/locator: [W1-07](_WORK/W1_07.md), раздел «Передача соседним веткам и точные открытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


1. **W1-01/evaluation:** принять schema `unknown`, exhaustive coverage, censored onset и group identity; определить, как ambiguous intervals исключаются из denominator, чтобы система не улучшалась простым abstention. Challenge set отдельно от natural-rate evaluation.
2. **W1-02/models и training:** проверить реальные ignore/mask semantics выбранного trainer/assigner; закрепить commit, конфиги, class mapping и checkpoint hash. Можно ли провести OOF по source groups или доступен независимый teacher? Как не потерять old positives при mined negatives?
3. **W1-03/pose и W1-04/temporal:** события с GT fall transition/lying state/unknown intent; движение корпуса и механизма различать. Потребуются clip context и PTS, а не только bbox. Никаких будущих кадров в прошлом alert.
4. **Datasets:** есть ли права на исходные цеховые видео; известны camera/source IDs, полнота классов и исходная split provenance? Public benchmark clips могли присутствовать в pretraining; отсутствие exposure пока не установлено.
5. **LinQ/deployment:** data-only изменение не освобождает новый checkpoint от export/quantization validation. Передать выбранные тяжёлые пары как regression suite; качество окончательного inference и latency проверяются на LinQ, точная конфигурация неизвестна.
6. **Product/operator:** feedback `false alarm` — сигнал для QA, не automatic negative label; нужен reason code и исходный контекст. Оператор мог пропустить другой объект или оценить бизнес-правило, а не нейронный класс.

Минимальный следующий полезный шаг: заморозить manifests/ontology и просмотреть контрастные train-side клипы четырёх пар плюс случайные интервалы без срабатываний; после QA сформировать сравнение B/C. Это конкретная работа с данными до какого-либо решения об аренде и до бессодержательного увеличения числа эпох.


## F080 — W1-08: Решение

- Происхождение/locator: [W1-08](_WORK/W1_08.md), раздел «Решение»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S093, S094, S095, S099.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F080. Первый кандидат — ограниченные, привязанные к наблюдаемым дефектам аугментации поверх полностью описанного baseline.** Отдельно испытывать фотометрию/декодирование и масштаб/кропы. Сложный DG-алгоритм или случайно сгенерированный завод не являются обязательным первым шагом. Диапазоны и вероятность выбирать на train/validation, сохраняя реальные чистые кадры. Ни один источник не устанавливает target gain для каски, телефона или страховочной привязи на наших камерах.

**F080. Синтетическая устойчивость и перенос на новую камеру — разные утверждения.** Для первого достаточно отдельной corruption-suite, для второго нужны реальные независимые camera/scene groups. JPEG на кадрах обучающей камеры не имитирует новый ракурс, слепую зону или иную высоту подвеса. Не использовать lockbox, его фон, crops и соседние кадры даже как материал синтеза или pseudo-labeling. Изучение unlabeled целевой камеры для адаптации меняет постановку: это уже не доказательство pure unseen-camera DG. [S099]

**F080. Случайный Copy-Paste — условный challenger, а не безопасный default.** Есть положительный ablation на COCO с instance masks [S093] и отрицательный на малом VOC [S094]; особенно полезен документированный провал обучения только на вставленных маленьких объектах [S095]. Для СИЗ дополнительно важна связь предмета с человеком: каска на полу и каска на голове — разные факты для event logic. Объектный AP не подтверждает правильную связь PPE→person.

**F080. Для видео обязательна проверка семантики преобразования клипа.** Покадровая геометрическая случайность порождает искусственное движение; temporal reversal превращает падение в подъём. Одна функция, корректно меняющая boxes, ещё не гарантирует правильные event boundaries, track IDs, ROI и timestamp. Рекомендации по видео ниже — инженерный вывод, не измеренный эффект на кейсе.


## F081 — W1-08: Карта failure modes → допустимый кандидат → способ поймать провал

- Происхождение/locator: [W1-08](_WORK/W1_08.md), раздел «Карта failure modes → допустимый кандидат → способ поймать провал»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S095, S097, S098, S100.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Ниже — **собственные инженерные рекомендации**, мотивированные наблюдаемыми рисками и источниками выше. Численные диапазоны не выдаются за найденный оптимум. Сначала измерить train-примеры и реальные decode outputs: объект в исходном разрешении и после letterbox — разные размеры.

| Failure mode | Первая проверяемая аугментация | Семантический gate и отрицательный результат |
|---|---|---|
| Экспозиция, тени, смена дня/ночи, цветовая температура | Умеренные brightness/contrast/gamma, white-balance/color jitter; сохранить долю real clean frames | Не превращать цветной класс в другой; не стирать reflective strips/пламя/дым. Сильная гамма не создаёт реальный low-light noise. Проверить day/night отдельно; clean quality может упасть. |
| Сжатие, низкий bitrate, изменение масштаба потока | JPEG и downsample→upsample как дешёвый screening; отдельное реальное video re-encoding train-клипов с разрешённым codec/config | JPEG не моделирует H.264/H.265 GOP, temporal residuals, packet loss. Записать actual codec/bitrate/GOP/resolution и порядок resize/compression; принять только при улучшении на реальном потоке, а не JPEG-suite. |
| Defocus, грязное стекло, motion blur | Ограниченный defocus/Gaussian и направленный motion kernel, параметры из train fail cases | Motion blur направлением/длиной должен соответствовать движению/экспозиции; одинаковый blur всего кадра не равен движению одного человека. Если каска/сигарета исчезла для человека-разметчика, это visibility/ignore case, а не новый надёжный positive. |
| Малый телефон/СИЗ, дальняя зона | Scale jitter с контролем min object pixels; отдельный object-aware crop/ROI challenger; oversampling разнообразных small-object эпизодов | Измерять bbox short-side и area **после** preprocess. Не увеличивать только одних людей/одну камеру. Crop удаляет контекст PPE→person или создаёт обрезанный head; aggressive zoom-out/Mosaic уничтожает и без того малый target. Oversampling может снижать large-object quality [S095]. |
| Окклюзия, тесные группы | Сначала реальные occluded clips; mask-aware occluder/Copy-Paste как отдельный challenger | Окклюдер закрывает только видимые пиксели; требуется политика visible vs amodal boxes. Отсутствие видимости каски ≠ отсутствие каски. Random erasing головы не создаёт достоверную метку «без каски». |
| Новый фон, другой цех | Реальные train-камеры/фоновые negatives; осторожное paste человека целиком на разрешённые train backgrounds | Сохранять PPE/person relation, масштаб относительно пола, тени, контакт ног, правдоподобную оптику. Прямоугольный crop несёт старый фон и может выдать shortcut. Новый фон не создаёт новый ракурс объекта. |
| Погода открытого цеха | Мягкие fog/rain/brightness как stress и затем train challenger, если такие условия есть в задаче | 2D overlay без depth/occlusion не равно атмосферному рассеянию; туман с низким contrast не заменяет пыль/дым/конденсат. Не менять метку «дым» синтетическим fog, если они семантически пересекаются. Требуется real weather holdout. |
| Изменение наклона, перспективы, высоты/объектива камеры | Небольшой affine/perspective jitter, если правдоподобен; сбор реальных viewpoints предпочтительнее экстремального warp | Гомография 2D не открывает невидимые детали каски/привязи и не моделирует 3D self-occlusion. Для геометрических правил обязателен перенос ROI/линий либо исключение этого transform из event pipeline. Калибровку не переобучать по синтетике. |

### Partial labels и малые объекты: обязательный аудит до sweep

**F081. Отличать частично видимый объект от частично размеченного датасета.** В первом случае нужны договорённости о bbox/visibility; во втором обычный detector может учить видимый неразмеченный объект как background [S100]. Copy-Paste добавляет ещё и смешанные политики разметки двух кадров. Person crop, содержащий неразмеченные телефон, каску и соседа, не является полностью размеченным negative для этих классов.

Для каждого train sample хранить `verified_classes`, неизвестные/ignore regions, visibility/truncation, источник и parent group. Если trainer не поддерживает ignore/partial losses, сначала довести нужные классы до полной разметки либо исключить непригодный sample; просто стереть bbox недостаточно. Это особенно существенно для narrow PPE datasets при union ontology W1-06. Не использовать `no_helmet` как автоматический результат удаления каски из изображения: нужно достоверно видеть голову и согласовать label policy.

В transform audit считать по классам и размерам: сколько объектов сохранено, отброшено crop/filter, стало менее выбранного min-visible размера, перекрыто и превращено в ignore. Проверить aligned boxes/classes/masks/track IDs после фильтра. S097 показывает, что даже корректно исполняемый pipeline имеет конкретный size/area cutoff; не называть его универсально правильным. Коэффициент retained area bbox не равен видимости предмета: узкий ремень может занимать малую часть большого bbox.

Для bbox-only Copy-Paste не обещать обновление настоящей видимой формы: прямоугольники дают лишь грубое пересечение. Начать с non-overlap или собственных проверенных masks; не переносить mask-based published gain на box paste. Не вставлять isolated helmet в случайное место и одновременно учить PPE compliance: можно учить отдельный object class при сохранённой object label, но человек-ассоциация требует иного annotation contract.

### Temporal transforms: что должно сохраняться

**F081. Разделить frame detector training и обучение/оценку последовательности.** Для независимого frame detector покадровая фотометрия может быть допустима; для tracker/action model и downstream event validation она моделирует дополнительные скачки. Нельзя сравнивать разные режимы, скрыв различие за общим словом augmentation.

1. На один клип один sampled crop/flip/warp и согласованные boxes/keypoints/masks во всех кадрах. Иначе искусственный camera shake меняет скорость и траекторию. Использовать повтор параметров через functional API или гарантированное clip-level применение; unit-preview фактического результата важнее имени библиотеки [S098].
2. Brightness/blur параметры либо постоянны на клип, либо меняются плавно по заранее заданному процессу. Независимый сильный jitter каждого кадра похож на мерцание; это отдельный реальный failure mode, а не бесплатный default. Track IDs и association не переставлять.
3. Временной crop positive-клипа может исключить само нарушение: пересчитать label по оставшемуся интервалу и evidence frames. Короткий клип с последствием падения не обязательно содержит начало падения. Сохранить исходные timestamps и event boundaries.
4. Speed jitter, frame dropping и subsampling меняют наблюдаемую длительность/разрешение во времени. При сохранении real timestamps интервалы действительно пропущены; при перенумерации кадров меняется скорость. Порог «N кадров» и порог секунд неэквивалентны. Для устойчивости к stream drops отдельно измерять late/missed alerts; UniformTemporalSubsample может повторять кадры при недостатке T [S098], что не создаёт нового движения.
5. Reversal, shuffle и произвольная перестановка кадров выключены для fall/approach/entry/exit. Reversal меняет направление процесса; flip без переноса left/right labels и зон меняет правило. Горизонтальный flip для person detection допустим только при отсутствии зависимого знака/стороны; vertical flip и 90° rotation создают неправдоподобную позу или имитацию падения.
6. Mosaic/MixUp/CutMix нескольких видео не включать в temporal/event baseline: они смешивают камеры, траектории, действия, timestamps, зоны и идентичности. Положительный frame-detection опыт не доказывает корректность такого action/track обучения. Синтетическая траектория требует собственной согласованной разметки, включая event truth.


## F082 — W1-08: Синтетика и domain randomization: три разных продукта

- Происхождение/locator: [W1-08](_WORK/W1_08.md), раздел «Синтетика и domain randomization: три разных продукта»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S093, S095, S096.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F082. Не смешивать procedural rendering, annotated copy-paste и random text-to-image.** S096 рандомизирует управляемый рендер с известной геометрией и labels; S093 оперирует размеченными instance masks; случайный генеративный кадр не имеет гарантии ни геометрии, ни полноты labels. Все могут быть полезными train inputs, но это разные гипотезы.

Для генеративных изображений нужны provenance/model-version/rights, human audit анатомии, реальности предмета, количества объектов, вида СИЗ, contact/occlusion и labels. Prompt «рабочий без каски» не является ground truth. Возможны фантазийные ремни, каска как часть головы, неверные руки/телефон, печатные артефакты и скрытые positives. Нельзя оценивать победу на изображениях того же генератора/шаблона и называть её реальной устойчивостью. Не рекомендуется тратить ранний бюджет команды на массовую случайную синтетику до выявления недостатка конкретных train conditions.

Если есть renderer/маски и права, сильнее проверяемый кандидат: варьировать известные nuisance factors и сохранять causal labels, включая relation/visibility. Разделять не только seed рендера, но source assets/background families; копии одного человека с разными фонами не независимы. Для realistic view augmentation рендер должен менять 3D pose/camera, а не только warp картинки. Какая доля synthetic/real оптимальна — неизвестно; сохранять original+synthetic и проверять synthetic-only лишь как исследовательский отрицательный контроль. S095 прямо показывает, почему augmented-only validation опасна.


## F083 — W1-08: Различающий эксперимент: есть ли реальный перенос, а не узнавание артефактов?

- Происхождение/locator: [W1-08](_WORK/W1_08.md), раздел «Различающий эксперимент: есть ли реальный перенос, а не узнавание артефактов?»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S093, S094.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос:** улучшает ли выбранный пакет nuisance augmentation пропуски малых/закрытых объектов на реальных held-out camera groups при приемлемом FP/camera-hour и сохранении clean качества? Если да, добавляет ли mask-aware Copy-Paste пользу сверх него? Это **план**, не проведённый опыт.

**Входы и ресурсы:** согласованный detector и checkpoint из W1-02, schedule/init из W1-06, разрешённые train видео с полными target labels, codec metadata, независимые real validation/SELECT/lockbox группы, instance masks при Copy-Paste, доступный GPU и воспроизводимое окружение. Нужны GPU smoke и реальное разрешение на ресурсы до запуска; 1–2 RTX3090 — возможный ресурс, не проверенный fit и не разрешение аренды. Оценка после экспорта/квантования и LinQ latency передаётся соседней ветке. Не назначается вымышленный срок run.

**Split до извлечения кадров и производства синтетики:**

- Объединить в один `camera_group` физически связанные камеры/перекрывающиеся ракурсы одной сцены; переносимая камера с тем же помещением не становится независимой от смены ID. Один episode, соседние кадры, crops, cutouts и их synthetic descendants принадлежат одному split. Проверить exact/near duplicates и scene lineage вручную на спорных случаях.
- Train: только его backgrounds/cutouts/synthesis. Validation: реальные отдельные группы для pipeline/threshold/checkpoint/hyperparameter выбора; optional SELECT — другие группы для выбора финалистов. Lockbox: отдельные camera/scene groups, доступ после фиксации всего recipe, без tuning по его ошибкам. Synthetic stress variants имеют parent real split и не являются дополнительным независимым n.
- Если камер недостаточно для всех уровней, не выдавать random frame split за DG. Использовать source-camera leave-group-out folds для screening, затем выделить реально новый camera/scene test; честно указать отсутствие возможности надёжной оценки при малом числе групп. Отдельно можно измерить within-camera temporal transfer, не смешивая его с unseen-camera результатом.

**Порядок:**

1. Провести label/transform audit: contact sheets до/после с bbox/видимостью/track/ROI; histogram final pixels; счётчики dropped labels. Договориться об ignore и определить запрещённые transforms по каждому сценарию. Зафиксировать all config defaults: если stock baseline уже имеет Mosaic/HSV, это часть A, а не «без аугментаций».
2. Сравнить **A** explicit baseline; **B** A + lighting/codec/blur nuisance; **C** A + scale/crop policy; **D** A + B + C только после понимания одиночных эффектов. Init, split, optimizer updates, sampling exposure, resolution и checkpoint selection одинаковы. Не добавлять одновременно high-res и новый pretraining. Логировать actual updates/images/wall time: эпоха при oversampling не сопоставима автоматически.
3. При masks и достаточном independent positives: **E** лучший реалистичный режим + constrained Copy-Paste; дополнительный небольшой random-placement вариант проверяет S093/S094 на наших объектах. Сохранить долю оригинальных изображений. Отдельно учитывать relation-labels и разрешённость вставки конкретного предмета. Массовая генеративная синтетика — следующий отдельный challenger, если доказан пробел покрытия.
4. На real validation измерить clean и реальные nuisance slices; на fixed synthetic suite — отдельные severity curves, не основной критерий победы. Не выбирать severity по lockbox. Для отсечения сильного вреда сравнить и простую no-extra-transform ветку с тем же schedule. Повторить подходящие финалисты с seed вариацией по заранее доступному бюджету; один seed — screening.
5. Выбор по заранее согласованным event/retention constraints и real held-out metric; сохранить ошибочные эпизоды для анализа. После SELECT зафиксировать model/checkpoint/config/threshold/preprocess/event logic; открыть lockbox один раз. Не улучшать его результат подстройкой и сохранять прежнее название «независимый тест».

**Метрики:** per-class AP50:95 и recall; AP/recall по final-pixel size bins, visibility/occlusion, camera, light, codec и weather; clean-versus-corrupt deltas; worst-camera и macro-camera вместе с aggregate. Для enforcement — event recall при выбранном FP/camera-hour, duplicates, fragmentation, late/missed alerts, p50/p95 event-to-alert latency и real source-camera-hours. Считать uncertainty по camera/episode clusters, не по соседним кадрам; редкая группа без positives даёт недостаток evidence, а не recall=100%. Ошибки label policy отбирать в audit, а не механически записывать как model FP.

**Артефакты:** code SHA/environment lock; checkpoint hash/rights handoff; split manifest с camera_group/episode/parent lineage; ontology/verified labels/ignore contract; exact augmentation graph, probability, magnitude distributions, interpolation и порядок codec/resize; seed и sampled params для воспроизводимых previews; dropped-target counters; all raw predictions и per-group metrics; selection rule и число trials; GPU time/memory logs при реальном запуске; frozen bundle для LinQ parity. Не ограничиваться одной итоговой mAP картинкой.

**Исходы и решения:** real-camera improvement при сохранённых constraints → оставить самый простой подтверждённый пакет; synthetic-only improvement → отклонить заявление о реальном gain; small-object gain при large-object/clean/event вреде → решить по заранее согласованным приоритетам либо уменьшить силу/частоту; Copy-Paste gain только на pasted validation → отклонить; результат меньше межкамерной/seed вариативности → нет убедительной победы, сохранить baseline и собрать данные. Невозможность полноценных labels/independent groups — ограничение вывода, а не основание заменить real holdout синтетикой.

Успех этого опыта не доказывает промышленную безопасность, перенос на любое размещение камеры, различение всех действий, соответствие few-second latency, качество после INT8 или работоспособность на LinQ. Обучающие augmentation обычно не добавляют операций в inference, но TTA, crops/multiscale inference, restoration и super-resolution добавляют их; их latency — отдельное измерение.


## F084 — W1-08: Передача и неизвестные

- Происхождение/locator: [W1-08](_WORK/W1_08.md), раздел «Передача и неизвестные»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F084. Главные риски артефактов:** чрезмерное стилизование/цвет, disappearing tiny labels после resize, bbox filtering без ignore, прямоугольные вставки со старым фоном, ореолы mask blending, невозможные PPE/person relations, непрерывный случайный occluder, flat weather overlay, 2D warp вместо нового ракурса, покадровая геометрия, reversal/speed jitter без пересчёта времени, Mosaic/MixUp видео, повторение assets между splits и synthetic-only validation. Списки должны стать transform allowlist по scenario, а не общим переключателем «strong augment».

Передача **W1-02/06**: сохранять stock augmentation defaults, small-target drop audit и replay/union-label contract; не менять init/compute одновременно с augmentation. **W1-04/evaluation**: camera_group manifests, real vs synthetic metrics, worst-group и cluster uncertainty, SELECT/lockbox. **Data**: masks/verified classes/visibility, отдельные реальные negatives, условия съёмки и source lineage. **Video/behavior**: временные метки, event intervals, track IDs, PPE relation labels и запрет небезопасных temporal transforms. **Calibration**: перенос зон/линий при геометрии и настоящие новые viewpoints; **LinQ**: фиксированный preprocessing/resolution, parity и реальная задержка, включая codec/crops при их наличии.

Точные вопросы до запуска: сколько независимых сцен/камер и каких размеров PPE после decode/letterbox; какие codecs, bitrate/GOP и реальные blur/light/weather failures; какие classes полностью verified и как размечены скрытые/обрезанные объекты; являются ли цвет СИЗ, направление движения и положение зоны частью label; есть ли права на cutouts/backgrounds и instance masks; какой FP/event budget и допустимый clean/retention loss; доступно ли enough real camera groups для SELECT+lockbox; какая LinQ конфигурация и финальный разрешённый inference graph. Без этих ответов можно предложить кандидаты, но нельзя обещать величину или вероятность target gain.


## F085 — W1-09: Решение для команды

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Решение для команды»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S104.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F085. Начать с class-specific рабочих точек и короткой причинной FSM на замороженном детекторе, сохранив вариант без дополнительного подтверждения.** Порог, NMS и persistence выбирать совместно по своевременным событиям и ложным уведомлениям на непрерывном validation-видео. Требования на recall к дедлайну, latency и coverage действуют одновременно с high precision. Если допустимой точки нет, не выдавать отсутствие уведомлений за качество: менять признаки/модель/сценарий либо честно ограничивать поддерживаемые условия. Это инженерное решение; выигрыш на данных команды ещё не установлен.

**F085. Calibration не обязательна для выбора порога и не создаёт различающую способность.** Для одного класса строго возрастающее скалярное преобразование score сохраняет ранжирование и множество достижимых threshold-решений до временной агрегации. Поэтому сначала сравнить identity + tuned threshold с calibration + tuned threshold. Улучшенный ECE сам по себе не доказывает более точные тревоги. Для EMA, score averaging, multiclass softmax, объединения камер и WBF указанная эквивалентность уже не гарантируется.

**F085. Не превращать маленький validation в таблицу сотен независимых порогов камера×класс.** Базовый fallback — общий порог на класс; camera override допускается по заранее фиксированному правилу и только с отдельными размеченными development-данными этой камеры и проверкой на других сессиях. Новая камера без меток получает общий fallback и статус неподтверждённой переносимости. Данные lockbox запрещено использовать даже для «лёгкой подстройки» без обучения backbone.

**F085. Hard NMS — baseline, Soft-NMS — ограниченная проверяемая альтернатива для перекрывающихся объектов, WBF — резерв для ансамбля, прошедшего LinQ/latency gate.** У WBF есть важный опубликованный отрицательный результат на raw outputs одиночного детектора; это не универсальная замена NMS [S104]. Никакого подтверждённого прироста event precision у наших камер нет.

Метрики целого pipeline и matching берём из `_WORK/W1_01.md`, causal timestamps/новые наблюдения — `_WORK/W1_04.md`, lifecycle ID/event UUID/rearm — `_WORK/W1_05.md`. Здесь не повторяется их общий обзор. Основание кейса — `_WORK/CASE_NOTES.md`, прямое визуальное чтение root: с. 5, 7, 13 требуют качества, нескольких секунд до сообщения, dedup и измерения LinQ. PDF в этой ветке отдельно не рендерился. CPU+TPU — сообщение команды, точная конфигурация неизвестна.


## F086 — W1-09: Что подтверждено источниками, а что остаётся гипотезой

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Что подтверждено источниками, а что остаётся гипотезой»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S101, S102, S103, S104, S105, S106.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


| Приём | Проверенное основание | Следствие для решения и граница |
|---|---|---|
| Temperature scaling | Guo et al.: scalar `T>0`, fit NLL на validation, улучшение classification calibration в исследованных задачах [S101] | Кандидат при доступных корректных logits; не доказательство detector/event calibration или большей полноты |
| Detection-aware calibration | Küppers et al.: корректность включает класс и локализацию; исследованы confidence/location/scale, D-ECE [S102] | Нужны bbox GT и фиксированный matching; один score не обещает одинаковой надёжности по размеру/камере |
| Threshold tuning | sklearn 1.5.2 разделяет scores и decision threshold и запрещает fit/tune на тех же данных [S105] | Используем принцип, а не случайный frame-level CV и не default binary scorer для событий |
| Soft-NMS | Bodla et al.: уменьшение score соседей вместо немедленного удаления; опубликованы AP-улучшения без переобучения [S103] | Альтернатива при crowd/occlusion; сохранённые дубликаты и рескоринг требуют полного replay |
| WBF | Solovyev et al.: fusion координат ансамблей; в §7 одиночный raw detector ухудшился относительно NMS [S104] | Не включать автоматически; ensemble inference/TTA увеличивают работу и могут не пройти deadline |
| Persistence/hysteresis/ROI | В данной ветке нет эксперимента на целевых industrial alarms, подтверждающего оптимальные настройки | Прозрачные инженерные эвристики с обязательными абляциями; конкретные секунды/пороги не выдаём за научный стандарт |
| Camera recalibration | Ovadia et al. показывают ухудшение uncertainty при shift и ограничения in-domain post-hoc scaling [S106] | Камерная адаптация требует отдельного испытания; эта статья не доказывает лучший алгоритм адаптации камер |

**F086 — отрицательные результаты и противоречия.** В [S102, §5.2] лучший метод зависит от цели: confidence-only и box-sensitive calibration дают разные сравнительные результаты. Следовательно, успех temperature scaling на классификации [S101] не устанавливает победителя для детекции. В [S104, §7] raw RetinaNet ResNet152 на Open Images: оптимизированный NMS `mAP@0.5=0.4906`, WBF `0.4532`; это авторские измерения, не наши. В той же статье Eq. (7) напечатана с `TP+FP+FN` в знаменателе precision; такую формулу не переносить: для precision использовать `TP/(TP+FP)` по W1-01. Хорошее объединение ансамблей не оправдывает ошибку метрической записи. Soft-NMS не устраняет все дубликаты: после rescore действует cutoff; его сравнение должно включать downstream tracking и события.


## F087 — W1-09: Различать три confidence и место calibration

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Различать три confidence и место calibration»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S101.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


1. **Detector score**: выход конкретного artifact/runtime. Записать, что это: class sigmoid, softmax, objectness×class, качество локализации, иной combined score. Нельзя подать произведение двух вероятностей как raw logit в формулу из [S101]. Для sigmoid с настоящим logit допустим `sigmoid(z/T)`; для softmax — `softmax(z/T)` по всей векторной размерности. Если доступны лишь scores, положительный monotone logistic fit на `logit(clip(s,eps,1-eps))` — отдельная модель калибровки combined score; она не воспроизводит исходные скрытые logits.
2. **Detection correctness probability**: условная корректность сохранённой детекции по заранее заданным классу, IoU и one-to-one GT matching. Fit после фиксированной структурной постобработки, до alarm cutoff. Дубликат, уже занявший GT, не становится вторым TP. FN не исчезают из event recall из-за отсутствия строки среди кандидатов.
3. **Event/alert confidence**: вероятность того, что конкретный кандидат эпизода соответствует определению события и, если так задано, успеет к дедлайну. Это иной target и population. `max(frame_p)`, произведение `p` или `1-product(1-p)` коррелированных кадров не являются автоматически event probability. Для первой версии называть их `evidence_score`, без вероятностного обещания. Отдельный event calibrator — только после стабилизации proposal generator на независимых CAL-кандидатах; он не исправляет пропущенные proposals.

Предлагаемый минимальный порядок: фиксированный decode/resize → low candidate floor и top-k → class-aware NMS → при необходимости score calibration → tracker с отдельным low-score pool → ownership/visibility/ROI → причинная FSM → event UUID/dedup → сообщение. Это **выбор архитектуры**, не универсальный закон. Если calibration вставить до NMS, она может менять межклассовое ранжирование, class-agnostic suppression и состав candidates; требуется новая полная проверка. Soft-NMS меняет scores, WBF меняет scores и bbox: старый calibrator и old threshold после такой замены не считаются действительными.

Не повышать общий upstream detector cutoff ради high-precision alarms: это может удалить low-score pool трекера (handoff W1-05), ухудшить ID и persistence. `det_candidate_floor`, `track_high/low`, `new_track_threshold`, `alarm_on_threshold` — разные параметры с разными целями. Floor/top-k ограничивают измеряемое пространство: по cache с floor=0.3 нельзя проверить 0.1, а после необратимого NMS нельзя честно сравнить его с другой IoU-настройкой.


## F088 — W1-09: Validation-only protocol v0.1

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Validation-only protocol v0.1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


Ниже — предлагаемый воспроизводимый протокол, не выполненная работа и не процедура с доказанной гарантией precision.

### A. До просмотра кривых

- Зафиксировать scenario semantics, onset/observable/end, matching/dedup, timestamps и SLA из W1-01/04/05. Зафиксировать пределы `B_c` для ложных сообщений/наблюдаемый camera-hour, минимальную timely полноту `Rmin_c`, дедлайн `D_c` и правило выбора при ничьей. Если заказчик не определил значения — показывать Pareto-фронт без «победителя по accuracy».
- Заморозить detector weights/hash, preprocessing, runtime/quantization, class map, source sampling и schedules tracker/rule. Изменение любого из них после tuning создаёт новую версию кандидата. Финальный neural inference обязателен на LinQ; preliminary score replay не измеряет LinQ latency.
- Составить manifest `train / development / optional SELECT / lockbox`. CAL/TUNE/CHECK ниже — роли **внутри development**, а не разрешение трогать lockbox. Разбивать по независимым site/scene/camera/session/event, а не кадрам. При заявлении unseen-camera целая камера и одинаковая сцена не пересекают development/lockbox; при same-camera future-session это отдельный, явно более узкий estimand. Соседние части одного непрерывного эпизода не независимы. Нужны time gaps, отсутствие перекрывающихся clips и документация повторов.
- Сформировать малый список семейств и диапазоны до итоговой оценки. Рекомендуемый ablation shortlist: A0 identity + hard NMS + immediate event; A1 class thresholds; A2 A1 + короткая timestamp-aware persistence/hysteresis; A3 A2 + scalar calibration; A4 Soft-NMS вместо hard NMS, если найдена crowd-ошибка. WBF добавляется отдельной веткой лишь после доказанной полезности второго LinQ-compatible inference. Это предложенные варианты, не предустановленные оптимальные числа.

### B. Если независимых development-групп достаточно

**CAL:** fit только calibration parameters. Для каждого фиксированного NMS/fusion-кандидата построить его собственные postprocess outputs и matching. Базовая модель — identity; дополнительный кандидат — положительно монотонная scalar map (или корректная temperature scaling там, где доступны logits). Class-specific fit разрешать только при наличии обоих исходов и достаточных независимых групп; размер достаточности задаётся через требуемую неопределённость, не число кадров. Per-camera map в первую итерацию не нужна. Калибровка backbone weights не меняет, но всё равно является обучаемым этапом.

**TUNE:** calibrator frozen. Для каждого варианта прогнать весь непрерывный поток, сбрасывая состояние только в заранее объявленных границах сессий. Кандидаты порогов — уникальные score boundaries или заранее заданная грубая сетка; фиксировать comparator `>=`/`>` и tie policy. Сетка `on/off`, dwell/window, allowed gap, expiry, rearm и NMS должна быть небольшой; не подбирать тысячи комбинаций по единичным ошибкам. При каждом изменении NMS/floor/association пересчитывать tracker и FSM целиком. Кэш inference допускается, кэш старых треков — нет.

Для каждой полной конфигурации измерить W1-01 показатели по классам/камерам: timely event recall, FP notifications/camera-hour, notification precision с числом сообщений, duplicates, onset-to-receipt latency включая misses и coverage. Строить точки trade-off полного pipeline. Для threshold внутри FSM эти точки не обязаны образовывать монотонную PR-кривую: изменение числа срабатываний меняет rearm/dedup/association. В частности, снижение порога может раньше включить cooldown и скрыть последующее истинное событие.

Отбрасывать нарушающие latency/coverage/min-recall варианты; среди допустимых выбирать максимальную timely полноту при ограничении на FP/hour, затем меньшую задержку/сложность по заранее заданному tie rule. Для high-precision цели можно дополнительно требовать нижнюю границу precision, но только с явными статистическими предпосылками. Нельзя заменить FP/hour precision из искусственно сбалансированных положительных клипов. Когда ограничения несовместимы или границы слишком широки — результат `not demonstrated`, а не `best meets target`.

**CHECK или заранее выделенный SELECT:** один независимый development-проход замороженного победителя и baseline. Проверить разницу и неопределённость; не refit calibrator и не менять пороги после просмотра без признания CHECK частью TUNE. Если SELECT уже используется командой для model/checkpoint selection, не объявлять его повторно независимым подтверждением. При новой итерации нужен новый независимый CHECK либо честная маркировка exploratory. Lockbox остаётся нетронутым; окончательный frozen artifact на нём оценивается только по общему контракту root.

### C. Если development слишком мал

Не дробить несколько эпизодов на три якобы надёжных набора. Предпочтительный baseline — identity calibration + один порог на класс + минимальная FSM. Для сравнения семейств использовать nested group CV: внешняя группа полностью недоступна fit/tune, во внутренней части разделяются CAL и TUNE либо работает только identity. Все семейства/пороги/override policy выбираются во внутреннем цикле; во внешнем проверяется **процедура выбора**, а не заранее подобранный на всём development победитель. Folds по камерам при unseen-camera задаче; по независимым session/site при соответствующем узком estimand.

Если групп или положительных событий для nested CV нет — сравнение exploratory, без out-of-sample гарантии. Использовать leave-one-group-out stability как диагностику: меняется ли выбор при удалении одной камеры/эпизода, остаётся ли выигрыш на каждом независимом блоке. Не считать тысячи окон дополнительными испытаниями. Финальный calibrator/threshold при fit на расширенном development — новый артефакт; внешние CV-оценки относятся к процедуре, не являются независимым тестом именно этих refit параметров. Его предсказания проверяются на новом независимом материале либо остаются предварительными. Это лучше, чем скрыто использовать lockbox из-за нехватки данных.


## F089 — W1-09: Практические варианты постобработки

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Практические варианты постобработки»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


| Узел | Минимальная настройка для проверки | Failure condition и измеряемая цена |
|---|---|---|
| Per-class threshold | Свой `theta_on[c]`; общий baseline сохраняется | Редкий класс без данных не получает убедительный optimal threshold; high-score систематические ошибки остаются |
| Hard NMS | Class-aware baseline; фиксировать IoU, top-k, cutoff, tie order, bbox coordinate convention | Слишком агрессивное подавление теряет двух близких людей; слабое даёт дубли и ID; class-agnostic может подавить вложенные person/PPE/phone |
| Soft-NMS | Linear либо Gaussian как разные кандидаты, с отдельными Nt/sigma/cutoff | Нельзя оставить старый threshold: scores изменены. Дополнительные boxes могут увеличить FP/association cost; отсутствие переобучения не означает нулевую задержку |
| WBF | Один и тот же кадр, одна система координат/классов; полный config: constituent detector threshold/NMS, `skip_box_thr`, fusion `iou_thr`, model weights, `conf_type`, final event thresholds; всё выбирается на development/SELECT | Неверное fusion близких людей, смещение бокса через ROI, неравные score scales; ensemble/TTA cost. Не объединять соседние кадры как независимые модели |
| ROI/size/visibility | Только семантически обоснованные allow/deny regions, explicit unknown при невидимости | Отсечение маленьких объектов может удалить именно PPE/дальних людей. ROI граница и zoom должны проверяться отдельно; «за ROI не опасно» требует условия задачи |
| Persistence | Trailing time window, число **новых** валидных observations и duration в секундах; `dwell=0` control | Краткое истинное нарушение исчезает; persistent FP проходит. Независимость ошибок кадров не предполагать |
| Hysteresis | `theta_off < theta_on`; отдельные подтверждения входа/выхода и unknown policy | Снижает chatter состояния, но само по себе не гарантирует меньше ложных **начал**; может держать ложную тревогу и затруднять rearm |
| Causal EMA | `a(dt)=1-exp(-dt/tau)`, update только по новым observations; описать missing policy | Сглаживание задерживает переход и растягивает ошибку; не усреднять tracker score с detector score без определения смысла |

Все значения здесь подбираются на development; таблица не утверждает проверенную эффективность на целевых камерах. Не вводить геометрический threshold «метры» из пикселей; camera geometry — соседняя ветка.

**Предлагаемая спецификация FSM, чтобы tuning был однозначен.** Состояния `CLEAR → CANDIDATE → ACTIVE → CLEAR`, emitted flag привязан к event UUID. Вход в CANDIDATE только по свежему валидному свидетельству `s>=theta_on`. CANDIDATE накапливает подтверждение с ограничением максимального gap; повтор stale bbox не даёт ни нового голоса, ни бесконечной положительной длительности. Для duration-based правила явно задать, сколько времени observation покрывает до следующего (`max_evidence_age`); остальное — unknown. Проверка `covered_positive_duration>=dwell_on` плюс минимум новых observations — один возможный, проверяемый вариант, а не обязательная комбинация для всех событий. Для мимолётных пересечений нужен отдельный transition rule с быстрым входом. ACTIVE выдаёт одно сообщение. Выход требует свежего отрицательного/`s<=theta_off` в течение `dwell_off`; при unknown политика отдельно: сохранить pending event с ограниченным expiry или закончить как `visibility_lost`, но не считать доказанной нормой. Реарм и перенос state между tracklets строго из W1-05.

Чистая нижняя граница добавленной задержки dwell относительно первого подходящего наблюдения — примерно заданная выдержка плюс ожидание следующих новых observations; это не оценка LinQ wall-clock. Общую задержку считать от GT onset/observable до receipt, без заднего переноса timestamp на начало подтверждённого окна. Никакая настройка не должна скрывать long misses из latency-статистики.


## F090 — W1-09: Маленькая выборка: что можно и нельзя утверждать

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Маленькая выборка: что можно и нельзя утверждать»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S107, S108.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F090. Нулевые ошибки недостаточны без знаменателей и независимости.** Для заранее фиксированной конфигурации, `n` независимых идентично распределённых Bernoulli trials и `n` успехов односторонняя 95% exact нижняя граница вероятности успеха равна `0.05^(1/n)` [S107; частный случай биномиальной инверсии]. Арифметические примеры: 10/10 → около 0.741; 20/20 → 0.861; 59/59 → 0.9505. Для recall trial — независимый GT episode; для precision — alert, если такие trials действительно допускают binomial model. 59 кадров одной ложной/истинной ситуации не дают 59 независимых событий. Если уведомлений нет, precision undefined, а не 100%.

При нуле ложных сообщений за `H` наблюдаемых camera-hours в **стационарной Poisson-модели** односторонняя 95% верхняя граница rate — `-ln(0.05)/H ≈ 2.996/H` [S108; вывод из вероятности нулевого счёта]. Например, 10 часов без FP дают примерно `<0.30/hour`, а не доказанный нулевой rate. Для проверки заданного `B` при нуле FP ориентир экспозиции `H>=2.996/B`; это планирование при предпосылках модели, не обещание объёма данных. При clustered lighting/steam/ID ошибки homogeneous Poisson сомнителен: показывать rate по session/camera, paired cluster bootstrap для разницы конфигураций, а при нескольких кластерах признавать неопределённость неоценённой. Обычный bootstrap с нулём FP не создаёт честную ненулевую верхнюю границу.

Интервалы на TUNE после перебора множества вариантов — descriptive, не номинальная 95% гарантия выбранной системы. CHECK, nested selection и заранее фиксированный shortlist уменьшают selection bias; они не делают плохую выборку репрезентативной. Не выбирать удобный seed/fold/bin count. Для calibration показывать reliability bins с числом независимых групп/событий, NLL/Brier и распределение scores рядом с operating region. ECE, особенно со скудными/выброшенными bins, может выглядеть хорошо при плохой rare-event надёжности. Положительные постановочные ролики с переизбытком нарушений не воспроизводят deployment prevalence; precision при другом базовом rate меняется даже при тех же TPR/FPR. Не маскировать это pooled precision.


## F091 — W1-09: Адаптация камеры без использования lockbox

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Адаптация камеры без использования lockbox»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S106.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F091. Два разных испытания нельзя смешивать.** (1) Frozen general policy на unseen camera; никаких её кадров/меток для selection. (2) Camera onboarding: заранее выделенная размеченная `adapt`-сессия → фиксированный алгоритм override → другая будущая `evaluate`-сессия. Вторая задача показывает пользу адаптации известной камеры, но не zero-shot перенос. В обоих случаях lockbox не участвует в выборе. Если разрешённый только финальный lockbox не содержит отдельного adaptation protocol, camera-specific fit по нему запрещён.

Предложенный override: сначала общий class threshold. На adapt разрешить лишь маленькую заранее заданную сетку смещений к нему, без новых ROI/семантических исключений после каждого FP; выбрать по тому же constrained event objective. При недостатке данных, отсутствии позитивов или нестабильности group checks — общий fallback, статус `camera not validated`, запрос дополнительной разметки в operational процессе. Shrinkage offset к общему порогу с фиксированной/внутренне выбранной регуляризацией — возможный последующий вариант; в этой ветке нет доказанного оптимального коэффициента. Нулевые positives в adapt позволяют обнаружить часть background FP, но не проверить recall после повышения порога.

Unlabeled production scores пригодны для drift monitoring, а не для доказательства precision: снижение числа alarm не показывает, что опасностей нет. Не повышать порог автоматически, чтобы «не более N тревог/час»: это может скрыть реальное увеличение нарушений. Feedback только по emitted alarms смещён — misses не видны; для переоценки нужны и случайные непрерывные интервалы, и hard negatives, и проверка GT violations независимо от срабатываний. После перемещения камеры/zoom/света/нового runtime адаптацию версионировать, старую оценку не наследовать автоматически [S106 — общий риск shift; конкретная политика является нашей рекомендацией].


## F092 — W1-09: Различающий эксперимент и пакет передачи

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Различающий эксперимент и пакет передачи»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**Вопрос:** уменьшает ли class threshold + ограниченная temporal FSM ложные сообщения по сравнению с immediate baseline при сохранении timely recall и реальной LinQ задержки; даёт ли calibration сверх простого переноса threshold пользу на независимых сессиях?

**Входы:** размеченные непрерывные development-сессии с normal work и hard negatives; независимые краткие и длительные нарушения; источник/PTS/visibility; замороженный LinQ-compatible artifact; candidate outputs до необратимого NMS при сравнении NMS; полный event matcher W1-01; сценарные SLA и допустимый FP budget. Наличие GPU не является предпосылкой postprocess tuning; второй detector/WBF требует дополнительного neural inference и отдельного разрешённого compute, но аренда не предлагается как обязательная.

**Процедура:** выполнить A–C выше; сравнивать конфигурации на одних непрерывных сессиях, а не разных нарезках. Обязательные challenge-срезы: короткое истинное событие; устойчивый hard-negative; дрожание вокруг threshold; один пропуск/длинная окклюзия; два перекрывающихся человека; ID split/merge; второй участник во время active event; ROI boundary; VFR/burst drops; camera shift. Затем на LinQ замерить финальные shortlist по тем же schedules, input load и timestamps; не переносить latency из Python score-cache replay.

**Артефакты:** `split_manifest` с группами и hashes; `candidate_cache_schema` с floor/top-k/raw scores/logits; versioned `calibrator` с target и fit roles; полный `postprocess_config`; trial ledger всех проверенных настроек; per-alert и per-GT таблицы matching/misses/duplicates/latency; exposure/coverage по сессиям; PR/FP-rate–timely-recall/latency таблицы с числителями и знаменателями; paired comparison и sensitivity по группам; final freeze manifest. Это список требуемых будущих артефактов, не созданные файлы текущего исследования.

**Результаты решения:** (a) A2 уменьшает FP с допустимой своевременной полнотой и проходит LinQ → выбрать A2; (b) A3 улучшает NLL/ECE, но не event constraints → оставить более простой A2, не продавать calibration как прирост accuracy; (c) A2 теряет короткие события → class-specific bypass/transition rule и новый development-cycle; (d) все варианты проваливают feasibility → вернуть модели/семантике/наблюдаемости, а не продолжать бесконечную настройку; (e) данных мало → результат feasibility/exploratory, без заявления industrial precision.

**Что успех не доказывает:** качество unseen site, любых камер и освещения; устойчивость при quantization/model update; метрическую точность зоны/дистанции; переносимость COCO AP на alarm; safety certification; корректность неразмеченных сценариев; заявленную latency вне проверенного LinQ load. Нет данных — нет численного прогноза выигрыша или вероятности успеха.


## F093 — W1-09: Handoffs и оставшиеся вопросы

- Происхождение/locator: [W1-09](_WORK/W1_09.md), раздел «Handoffs и оставшиеся вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


- **W1-01:** принять его matcher/SLA/coverage, передать выбор constrained operating point и запрет номинальных post-selection CI. Требуются согласованные `B_c/Rmin_c/D_c`; без них возможен только фронт.
- **W1-04:** согласовать точное покрытие positive evidence между observations, `max_evidence_age`, gaps/unknown и подтверждение коротких событий; timestamp каждого notification остаётся фактическим receipt.
- **W1-05:** сохранить low-score tracker pool, тестировать ID/cooldown независимо от detector threshold; event UUID не равен track ID. Уточнить разрешённый rearm после visibility loss и нового участника.
- **LinQ/export/quantization ветка:** доступны ли настоящие logits, outputs до NMS и управление встроенным NMS/top-k? Идентичен ли score post-export? На каком узле исполняется CPU postprocessing, сколько потоков и как учитывается доставка? Ни один ответ не установлен этой веткой; после artifact change повторить calibration/tuning check.
- **Данные/камеры/разметка:** имеются ли непрерывные отрицательные camera-hours, независимые положительные эпизоды, bbox GT и отдельные адаптационные сессии? Если только положительные короткие ролики — можно проверить recall/feasibility, но нельзя обосновать deployment precision/FP budget. Геометрию камер и metric-distance правила здесь не решаем.

Итоговый status: **исследование завершено; практический validation-only протокол подготовлен, экспериментальные выигрыши команды неизвестны**.


## F094 — W1-10: Решение сначала

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Решение сначала»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S110, S113, S114.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F094.** Рекомендуемый порядок для команды из пяти инженеров: зафиксировать один совместимый с LinQ detector baseline и событийный CPU-конвейер; затем испытать **одну** добавку, выбранную по ошибкам. Если detector уже видит нарушителя, но путает похожие состояния, первым кандидатом служит crop specialist. Если различие определяется последовательностью, сначала сравнить простое временное правило с temporal verifier. Если detector не видит мелкий объект, verifier на его отфильтрованных detections проблему не решит: нужны более широкие person proposals/ROI или независимый второй detector. Это инженерное решение, а не опубликованный результат на наших данных.

**F094.** Модель с двумя нейросетями означает два обязательства реального запуска на LinQ, включая редкий verifier и вспомогательные pose/ReID/flow-сети, если они добавлены. CPU для декодирования, геометрии, crop, NMS/WBF, ассоциации без embeddings, накопления свидетельств и дедупликации — разумный кандидат. CPU для **нейронного** verifier допустим как финальный путь только если он действительно выполняется в разрешённой среде LinQ и организаторы подтверждают трактовку требования. Это не способ спрятать вторую сеть на внешнем GPU. Точные CPU/TPU, SDK, операторы, memory и политика fallback неизвестны.

**F094.** WBF — кандидат сравнения fusion двух detector. Опубликованный single-model контрпример: **mAP@0.5 .4532 WBF против .4906 NMS**; условия ниже. Бесплатное улучшение не установлено. [S110]

**F094.** Teacher→student — основной способ сохранить один inference-граф, если offline teacher даёт проверяемый прирост, а ансамбль не проходит latency/совместимость. Но distillation требует дополнительного обучения; vanilla classification KD не является готовым решением detector KD. Отрицательный результат fine-grained imitation paper: полное imitation features может ухудшать detector. [S113, S114]

**F094.** Нельзя выбирать ансамбль по COCO AP и объявлять улучшение безопасности. Основное сравнение: event recall при согласованном FP/camera-hour и допустимой event-to-alert latency, отдельно короткие события, окклюзии, tiny objects, очереди и пропуски. Нужны held-out сцены/камеры и финальный lockbox. Повышение precision одним строгим verifier может скрывать падение recall; снижение числа уведомлений может быть просто более агрессивной дедупликацией.

Условия официального кейса здесь взяты из `_WORK/CASE_NOTES.md`, визуально прочитанного root: p5,7,13 — несколько секунд до уведомления, баланс precision/recall, один продолжающийся инцидент→одно уведомление, обязательные LinQ inference и измерение скорости. Это переданная локальная provenance, **не мой повторный просмотр raster PDF**. Устный приоритет accuracy не задаёт официального численного objective.


## F095 — W1-10: Пять условных архитектур

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Пять условных архитектур»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S110, S111, S112, S113, S114, S115, S116, S117.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Все пять — варианты для отбора, не предложение объединить их в один MVP. `D` — выбранный detector, `V` — crop verifier, `T` — временная сеть, `S_j` — сценарный specialist. Реальные checkpoint, лицензии и LinQ recipe detector выбираются вместе с W1-02; его отчёт не заменяет новый parity-check конкретной комбинации.

| Вариант | Поток и механизм предполагаемой пользы | Нейронные обязательства в production | Когда отклонить / место в очереди |
|---|---|---|---|
| **A. High-recall proposal → crop specialist** | `frame→D(person/объект, низкий proposal threshold)→expanded crop→V(целевое состояние/unknown)→CPU event`. Независимый classifier учится на ошибках, похожих объектах и трудных отрицательных crop | **D + V на LinQ**; resize/crop/сопоставление на CPU; learned ReID/pose не предусмотрены | Первый challenger, если у D высокая coverage и FP визуально проверяемы в crop. Отклонить при недостаточном proposal recall, плохой crop visibility или burst overload |
| **B. Общий detector → сценарные experts** | `D→CPU rules/router→S_j` только для включённых сценариев/зон; разные признаки и разметка для разных состояний | D и **каждый реально вызываемый S_j** должны иметь допустимый LinQ путь; максимум активных experts учитывается | Добавлять один сценарий за раз. Не выбирать универсальный learned router или большой bank experts до доказательства пользы; routing FN и смешение классов могут перечеркнуть gain |
| **C. Два различных detector → fusion** | `frame→D1,D2→единые координаты/классы→NMS либо WBF→tracker→events`; независимый второй путь может найти пропущенные объекты | **D1 + D2 на LinQ**; fusion на CPU. Без подтверждения параллелизма считать общую TPU занятость суммой | Только после измерения complementarity и ресурсов; наиболее рискованный online challenger. Один teacher-only ensemble допустим без production D2 |
| **D. Detector/tracks → temporal verifier** | `D→простая ассоциация→past-only crop/scene clip→T→event`; последовательность может отличить движение/жест/действие от одной позы | **D + T на LinQ**; ring buffer/track association на CPU. Pose/flow/ReID добавляют новые сети, если выбраны | Для сценария, где время несёт информацию. Сначала сравнить CPU persistence/hysteresis. Отклонить, если нужен будущий контекст, неподдерживаемый graph, мало target clips или подавляются короткие события |
| **E. Offline teacher/ensemble → один student** | teacher labels/logits/features на train/transfer data; обучить экспортируемый student; в runtime только `student→CPU events` | **Один student на LinQ**. Teacher и train-only adapters не нужны в runtime, если проверено их удаление | Когда teacher лучше на development data, а runtime ансамбль слишком дорог. Отклонить, если нет времени/данных на сравнимый KD experiment или student после конверсии теряет gain |

### A. Что именно должен проверять crop specialist

Это предлагаемый рецепт. Использовать **человека/голову/руки как proposal там, где целевой мелкий объект часто пропускается**, а не запускать phone classifier только после уже найденного телефона. Иначе второй этап не исправит основной FN. Выбрать умеренно расширенный crop с сохранением контекста: слишком тесный crop может обрезать предмет; слишком широкий уменьшает эффективный размер tiny object и включает соседних людей. Величина расширения — параметр VAL, а не произвольная гарантия качества.

Входы обучения V должны отражать реальное распределение proposals: crop от текущего D, его смещения/дубли/окклюзии, трудные отрицательные объекты и отдельное unknown/insufficient evidence. Обучение только на идеальных GT-crop и тестирование на ошибочных detector-crop создаёт mismatch. Позитивный classifier не может восстановить пиксели, которых нет; enlargement не равно восстановлению информации. Предобучение даёт старт, но target negatives обязательны.

Предлагается сравнить два правила: strict `proposal AND V-positive` и selective `уверенный D→сразу event evidence; ambiguous→V`. Второе уменьшает число V-вызовов, но сохраняет ошибки high-confidence D; первое легче интерпретировать, но добавляет FN на всех positives. Не считать selective mode заведомо безопасным. Если uncertainty плохо калибрована, редкий false negative или опасный high-confidence FP не попадёт на проверку. `unknown` не превращать автоматически в «безопасно»; нужен явный режим интерфейса/журнала и правила тревоги по сценарию.

NoScope подтверждает сам принцип conditional execution/specialization, но его задача — приближать бинарные ответы reference network на фиксированных камерах, не доказывать безопасность crop verifier. [S112] Cascade R-CNN отдельно подтверждает проблему несоответствия качества proposals и detector stages; он не эквивалентен нашему независимому classifier после D. [S117]

### B. Experts: не путать специализированность и ансамбль

Предлагаемый практический вариант: конфиг камеры включает только выбранные сценарии, а CPU-router выбирает expert по зоне/наличию необходимых объектов; общий D повторно не запускается отдельно для каждого сценария. Для опасной зоны может хватить D+геометрии без нового expert; отсутствие второй сети — полноценный baseline. Если событие требует иной информации, например контекста движения, не объявлять phone classifier универсальным specialist для всех нарушений.

Классы разных experts должны иметь договорённую семантику: `phone-visible`, `phone-in-hand` и «опасное использование телефона возле оборудования» — разные выходы; последние требуют контекста/правила события. Температуры и scores разных experts нельзя усреднять без определения, что это вероятность одного и того же target. Confusion matrix на development data помогает выбрать одну трудную пару, но не создаёт target negatives сама.

Hinton et al. используют generalist и specialists по путаемым классам, выбирая relevant specialists по generalist; это историческое доказательство идеи, не промышленный benchmark. Авторы **не заявили**, что в этой работе уже дистиллировали bank specialists обратно в generalist. [S113, §7–8] Поэтому «обучим десяток experts, затем гарантированно сожмём» не является готовым хакатонным рецептом.

Предлагаемый режим отказа router: если полигон/ракурс/конфиг непригодны, не выдавать тишину за negative; писать причину неоценимости. Проверять source-of-truth событий на всех видео, включая не прошедшие router, а не только на выбранных experts clips. При независимой оценке новой камеры нельзя обучить на ней camera-specific expert и затем назвать этот же результат camera-generalization.

### C. Два detector, diversity и WBF

Разные architecture names не гарантируют независимость ошибок. D1/D2 могут иметь одинаковый pretraining, разметку, resize, tiny-object failure и негативный перенос. Предлагаемый отбор до полноценного обучения ансамбля: таблица GT событий `нашёл D1 / нашёл D2 / оба / никто`, совпадающие FP, camera/small-object strata; затем оценка качества fusion. Замена architecture без анализа ошибок — слабое основание удвоить compute.

Опубликованный single-model test: RetinaNet R152, Open Images, 500 raw boxes; NMS IoU=.5→.4902, tuned .47→.4906; tuned WBF IoU=.43, skip=.21→.4532. Ансамблевые constituent outputs уже проходили NMS. Это **контрпример универсальному улучшению**, не доказательство, что WBF всегда хуже. [S110, §6.1, §7]

Pinned реализация `weighted_boxes_fusion` ожидает одинаковые class IDs и normalized `xyxy` в [0,1], принимает веса моделей, `iou_thr`, `skip_box_thr`, `conf_type`; варианты confidence включают `avg`, `max`, `box_and_model_avg`, `absent_model_aware_avg`. Matching ограничен одним классом; CPU NumPy-код не запускает detector. [S111] В proposed experiment отдельно нормализовать letterbox/resize каждого D; «уже normalized» не означает одну систему координат, если padding не снят.

Инженерные риски fusion: неправильное объединение рядом стоящих людей, усреднение семантически разных объектов, дубли после слабого IoU, suppression редкой находки одной модели, доминирование переуверенного D, снижение стабильности track ID. Не применять WBF одновременно по соседним кадрам как будто это синхронные predictions: движение создаёт другой объектный geometry; temporal association — отдельная задача. Не считать WBF-дедупликацию объектов заменой дедупликации событий.

Контроль сравнения: лучший одиночный D1/D2; union+classwise NMS; WBF с разрешённым небольшим search на VAL/SELECT. Настройка pre-NMS/head mode конкретного detector — отдельная переменная. **Не удалять NMS у каждой модели по умолчанию**, исходя только из названия fusion. Для end-to-end detector без dense NMS-output рецепт фиксировать отдельно. Не переносить числа из разных WBF benchmarks и mAP@.5 в COCO mAP@.5:.95.

TTA — альтернативный ансамбль forward-проходов одной сети, а не новая бесплатная сеть. `m` views означают примерно `m` model calls с отдельным preprocess/inverse transform; точная скорость неизвестна. При дефиците времени не включать TTA вместе с D2, чтобы не спутать причины gain. Горизонтальный flip допустим только при корректном преобразовании выходов и семантики сценария.

### D. Temporal verifier и причинность

Предлагаемая иерархия проверки: (1) detector+CPU event machine; (2) тот же D+causal temporal net; (3) более сложные actor/context clips только при измеряемом остаточном FN/FP. Клип должен содержать нужный контекст; узкий crop человека может убрать станок/движущийся транспорт. Удержание track при окклюзии и сброс состояния при ID switch — обязательные ablations. Результат не должен переноситься от одного человека к другому при reuse ID.

TSM имеет offline bidirectional и online unidirectional версии: первая использует будущие features, вторая — прошлые. Авторы отдельно предупреждают, что «zero FLOPs» shift всё же вызывает data movement и latency overhead. [S115, Fig.1, §3.2, §4.2] Для нашего online-path это основание проверить causal/stateful graph; не обещание его LinQ поддержки. Состояния должны быть явными входами/выходами либо управляться допустимым runtime. Подмена offline pretrained графа простым переключением causal-флага без обучения/проверки не принята.

X3D — альтернативная компактная spatiotemporal family с опубликованным trade-off пространственных/временных размеров, ширины и глубины; это не готовый classifier промышленного события. [S116] Низкий FLOP не предсказывает TPU latency; 3D/group/depthwise operators, layout и конверсия — отдельные gates. X3D или TSM здесь **альтернативы T**, не совместный ансамбль. Полный подбор action weights/datasets передаётся соседней behavioral ветке.

Для window `K` frames с шагом `s` при sample rate `f` накопление пустого буфера занимает `(K−1)s/f` секунд. Если буфер непрерывно содержит прошлое, такого ожидания при trigger может не быть; модель всё равно может потребовать post-onset evidence. Offline centered window требует реального ожидания будущей половины — это часть event latency, даже если forward очень быстрый. Добавить время sampling, очереди, crop, сети, event confirmation. Нет доказательства, что «несколько секунд подтверждения» приемлемо для каждого краткого опасного эпизода.

### E. Teacher→student: что переносим и чего не обещаем

Teacher выбирается по качеству на development data и целевым ошибкам. Он может быть большим D2 или offline ensemble; его LinQ compile необязателен, **если он нигде не используется во время финального inference**. Для студентского runtime остаются все его реальные вспомогательные сети. Если учитель нужен для каждого ambiguous кадра online, это вариант каскада с дополнительной production-сетью, не один student.

Для crop classification базовый план — сравнить одинаковый student с supervised loss и с добавкой soft-target KD, меняя только training recipe. Общая запись `L=(1−α)L_GT+α·T² KL(p_teacher^T || p_student^T)` описывает механизм, не закрепляет оптимальные α/T. Softmax-KD естественна для mutually exclusive classifier; sigmoid multilabel outputs требуют соответствующей постановки. Hinton et al. дают temperature/soft targets и совместное обучение с истинными labels. [S113, §2]

Для detector нельзя непосредственно считать весь массив boxes/logits matching между разными architecture: разные anchors/queries/assignments и localization loss. Выбрать поддержанный данным framework KD-рецепт; если реализовать его за оставшееся время нельзя, честно ограничиться supervised student baseline или offline pseudo-labeling с ручным контролем. Fine-grained imitation использует informative near-object locations; авторы нашли слабый эффект vanilla KD и ухудшение от полного imitation features. [S114, §1, §4.2] Этот отрицательный результат особенно важен против самодельного «MSE всех teacher/student tensors».

Pseudo-labeling и KD различать: filtered hard boxes — дополнительная разметка, soft distributions/features — иной signal. Нельзя очищать pseudo-label set от всех teacher FN и затем утверждать, что student научился rare positives. Для редких классов нужны GT и ручная проверка. При train-only teacher soft predictions могут систематически копировать фон/камеру; при доступе teacher к lockbox labels/кадрам итоговый student уже не независим.

У student **нет математического обязательства быть хуже teacher по GT**: supervised signal и regularization могут изменить ошибки. Но нет и гарантии сохранить teacher recall. Практический потолок конкретного transfer-set возникает, если нужные positives отсутствуют и ни teacher, ни GT не дают соответствующий signal. Отдельно измерять student до и после LinQ conversion; KD не исправляет неизвестные quantization/export losses автоматически.


## F096 — W1-10: Recall ceilings и распространение ошибок

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Recall ceilings и распространение ошибок»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S112.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Ниже — собственный вероятностный разбор для проектирования эксперимента, не числа из papers. Все вероятности условны на **истинном событии E**, совпадающих критериях видимости, matching и допустимом сроке уведомления. Величины надо измерить на target video.

**F096 — strict verifier.** Пусть `G` означает «для события был создан пригодный proposal вовремя», `A` — «V принял хотя бы необходимую evidence», `H` — «трек/событийное правило/доставка сохранили её». Тогда:

`R_event = P(G|E) · P(A|G,E) · P(H|A,G,E) ≤ P(G|E)`.

Это chain rule, **не предположение независимости**. Умножать отдельно измеренный detector frame recall на V accuracy из идеальных GT crops неправильно. Ошибки связаны: трудные окклюзии портят обе стадии. Proposal ceiling следует оценивать на уровне доступной для события возможности, а не detector AP. Crop classifier может исправить FP, но не событие, не получившее proposal. `P(H|...)` включает дедупликацию, которая может ошибочно слить двух пострадавших/повторное событие.

Для FP strict cascade `P(G,A|¬E)=P(G|¬E)P(A|G,¬E)` при заданной единице candidate. Снижение этой вероятности не задаёт FP/camera-hour, пока не учтены число candidates и clustering в события; массовое снижение proposal threshold может увеличить суммарные FP и verifier load.

**F096 — routed expert.** Если expert обязателен, событие теряется также при неправильном router: `R ≤ P(correct route and usable evidence | E)`. Camera-config router может вовсе выключить сценарий. Показать confusion router и conditional expert recall отдельно. Если несколько experts запущены параллельно и событие принимается по OR, recall зависит от совместных ошибок, precision — от общей частоты FP; majority/AND часто уменьшает recall редких событий.

**F096 — ensemble.** Для множеств GT событий, покрытых D1/D2 до fusion, `R_union=R1+R2−R_both`; полезно непосредственно считать добавочные D2-only positives. При AND без новых evidence `R_intersection≤min(R1,R2)`. OR не гарантирует полезную precision. Для WBF **не объявлять matched-box union строгим потолком AP/IoU recall**: усреднение координат способно превратить две неточные boxes в одну, проходящую IoU matching. Более корректный information ceiling — существование относящихся к событию input proposals; WBF не создаёт визуальных наблюдений там, где обе сети ничего не выдали. Fusion может и разрушить две хорошие boxes. После него обязательно новый matching, event evaluation и tracking.

**F096 — temporal.** В strict D→tracks→T цепочке `R≤P(пригодная последовательность сформирована вовремя|E)`. Этот ceiling включает sampling, окклюзии, ID switches, crop quality, сбросы буфера и backlog. Temporal smoothing может восстановить единичный пропуск, если прошлый track жив; оно не гарантирует обнаружение короткого события между sampled frames. При `k` требуемых подтверждениях нельзя писать `p^k` без независимости ошибок: соседние кадры сильно зависимы.

**F096 — distillation.** У E нет proposal ceiling teacher в runtime, потому что teacher там отсутствует, но остаются student detection failures и training-signal bias. Отчёт «teacher/student agreement» измеряет имитацию, не GT event recall. NoScope также определяет ошибки относительно reference-model answers; это важное ограничение при переносе идей экономии вычислений в safety. [S112, §4]


## F097 — W1-10: Ресурсная модель без выдуманных ms, VRAM и цен

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Ресурсная модель без выдуманных ms, VRAM и цен»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Пусть `N` — камеры, `f` — анализируемых кадров/с/камеру; `n_t` — число proposals, отправленных V на кадре; `q` — доля направляемых ambiguous candidates, если selective gate; `λ_T` — temporal clips/с по всем tracks; `c_X` — **измеренные на целевом runtime** device-seconds на вызов X с выбранными shapes/batch; `b_X` — batch. Эта модель учёта требует измерений, а не предсказывает fit.

| Вариант | Требуемые вызовы и память | Условие, которое реально измерить |
|---|---|---|
| Baseline | D: `Nf` calls/s; weights+activation; CPU decode/preprocess/tracker/event | Латентность и очередь при заданном числе камер, occupancy и resolution |
| A | D как baseline; V: `Nf·E[n_t]` calls/s либо соответствующие batches. Если `n_t` определён до ambiguity, selective умножает его условную интенсивность на q, учитывая зависимость, а не произведение без проверки | Средний **и peak** поток crop, blank/one-person/crowd. Batch экономит вызовы, но ожидание наполнения batch входит в latency. Хранение двух graphs или model switching |
| B | D + `Σ_j λ_j` expert calls/s; resident weights каждого включённого expert, activation и переключения | Одновременность нескольких сценариев. Experts с нулевой активностью на demo не доказывают устойчивый multiscenario throughput |
| C | D1/D2 по `Nf` calls/s; CPU fusion; обе weights и конкурирующие activations | Один TPU не обязан исполнять graphs параллельно; на общем устройстве учитывать `Nf(c_D1+c_D2)`, transfers и scheduler. При реальном независимом параллелизме path может приближаться к max, но доказательств пока нет |
| D | D + `λ_T` calls/s T; RGB ring buffer порядка `tracks·K·H·W·channels·bytes`; stateful T хранит отдельные caches, иногда decode buffer можно разделить | Sliding overlap повторяет обработку frames; cache reuse только при реализованном streaming graph. Peak tracks и restart/ID-switch, cold-start window |
| E | Runtime только student; обучение teacher generation + storage soft targets/features + backward student | Online память/throughput student измерить отдельно. Training teacher+student совместно может требовать больше VRAM; sequential cached outputs сокращают совместную residency, но features storage и I/O могут стать узким местом |

При общем последовательном accelerator приблизительная необходимая занятость `U≈Σ_X λ_X c_X` (c в секундах) должна быть меньше доступной занятости устройства с запасом на вариативность. `U<1` само по себе **не гарантирует p95 latency**; очереди и bursts важнее средних. c зависит от batch/shape и разделения CPU/TPU, поэтому использовать реальные совместные measurements. Если реальный runtime перекрывает transfers и compute, дополнительно измерить его scheduler, а не складывать несовместимые standalone timings как точную модель.

Полный event path: `sampling/arrival + decode + preprocessing + queues/transfers + all required neural stages + postprocess/tracking + evidence/confirmation + notification`. Средние model FPS и latency одного пустого кадра не равны этому пути. Следить за timestamps source frame и времени доставки: drops могут улучшить измеренный inference latency, одновременно ухудшив event recall.

Для каждого production graph нужен manifest: source code commit, checkpoint URL/SHA256 и лицензия, classes, input shape/layout/range, output semantics, export opset/converter/compiler version, precision, calibration data provenance, CPU fallback, supported batch, memory residency и benchmark logs. Без этого «вторая сеть маленькая» не является ресурсным обоснованием. Quantization и calibration не исследуются здесь заново; это handoff W1-16/калибровочной ветке.

**CPU вопрос формулировать явно:** может ли V/T выполняться на CPU **того же LinQ-сервера**, засчитывается ли это как требуемый neural inference LinQ, и как измеряются CPU fallback/потоки/приоритеты? До ответа безопасная плановая обязанность — экспорт/запуск всех production-сетей в организаторском LinQ-пути. Разрешение CPU не отменит необходимости измерить tail latency под decoder+GUI+verifier load.


## F098 — W1-10: Предлагаемый различающий эксперимент

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Предлагаемый различающий эксперимент»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос:** какая одна добавка даёт устойчиво больше распознанных истинных событий при фиксированном допустимом FP/camera-hour и deadline на LinQ: crop specialist, temporal verifier, второй detector или KD student? Для experts сначала ограничить сравнение одним проблемным сценарием; не смешивать пять новых систем в неконтролируемом search.

**Входы/предпосылки.** Точная taxonomy и правила события, согласованные бюджеты `B_FP`, `L_max`, допустимая деградация recall `δ` и/или минимальный полезный gain `Δ`; положительные/отрицательные video sessions с event boundaries, person/object labels и visibility/uncertainty; доступ к LinQ CPU/TPU/SDK; зафиксированный baseline detector и разрешённый compute для обучения. Значения бюджетов задаются с командой, а не выдумываются в этом отчёте. Несколько сотен соседних кадров одной сцены не заменяют независимые события.

1. **Manifest/splits до model selection.** `train` для detector/verifier/KD; `VAL` для threshold/KD recipe; при достаточных данных `SELECT` для выбора architecture; финальный `lockbox` из независимых cameras/scenes/sessions по заявленному уровню generalization. Разнести исходные видео до нарезки frames/crops/clips. Не допускать одних людей/действий в перекрывающихся clips по обе стороны split. Для camera-generalization одни и те же камеры/сцены не пересекаются; known-camera future-time тест честно так и называть. Все near-duplicates и публичные ролики с неизвестным train overlap пометить.
2. **LinQ feasibility gate каждого графа.** Compile/static-shape batch1, parity reference→export→runtime на development examples; пустые frames, crowd, tiny crop, unsupported stateful op. Записать fallback. Кандидат без допустимого runtime — offline teacher либо reject как финальная архитектура. Не тратить основной training бюджет на пару непроверенных graphs.
3. **Baseline и oracle-диагностика.** Получить event recall/FP-hour/latency; построить cause tags FN: no proposal / bad crop / wrong class / track / temporal rule / queue / delivery. Для A оценить oracle V, принимающий все действительно релевантные proposals: это ceiling на измеренной выборке, не deployable result. Для D — oracle пригодной sequence; для C — event coverage union и D2-only rescue до fusion. Оценку oracle считать по разметке вне обучения, не выдавать её за качество модели.
4. **Узкий controlled ablation.** A: одинаковые D/preprocessing, baseline vs strict vs selective V. B: D+rules vs D+один S. C: D1 vs D2 vs union+NMS vs WBF; TTA отключить. D: D+CPU persistence vs D+T при одинаковом input schedule/causal constraints. E: одинаковый student init/train data/budget, supervised vs KD; teacher quality отдельно. Выбирать только те ветки, которые соответствуют dominant errors, с заранее ограниченной сеткой.
5. **VAL/SELECT tuning.** Записать detector confidence, proposal threshold, per-model NMS, crop margin, V/T threshold, WBF weights/IoU/skip/conf_type, gate, sampling/window, event persistence/cooldown и association params. Все решения только VAL/SELECT. Вычислять metrics и при одинаковом FP-budget, и operating curves, чтобы не принять обычный threshold shift за architecture gain. Передать W1-09 вопрос calibration на том же split.
6. **Target runtime с реальными нагрузками.** Одно и несколько streams; пустой, штатный и crowded/одновременные события; decoder+GUI+all neural stages. Warmup отдельно, затем p50/p95/p99 event-to-alert, per-stage service/queue, input/output FPS, drops, age of processed frame, peak CPU/RAM/device memory, verifier calls/camera-hour, cache resets/model switching. Считать late-positive как нарушивший deadline по согласованному правилу, а не silently successful.
7. **Freeze и один lockbox run.** Freeze architecture, weights/hash, export, all thresholds, event rules и metrics script до открытия. Посчитать uncertainty по независимым events/camera-sessions, например cluster bootstrap, а не frame bootstrap. При малом числе событий показать denominators и wide intervals. После провала не донастраивать на том же lockbox под прежним названием независимого теста.

**Метрики:** event recall с deadline и без него; event precision и FP/camera-hour; event PR/FROC operating curve; по сценарию/камере/размеру/освещению/окклюзии; пропуски коротких эпизодов; duplicate notifications/event; ошибочные merges разных events; latency distributions; proposal coverage и conditional verifier recall; D1/D2 joint error/rescue; cost per analyzed camera-hour и нейронные calls. Detector AP — вспомогательная локализационная метрика; classifier accuracy на отобранных crops — не главный endpoint.

**Артефакты эксперимента:** immutable split/group manifest; provenance/annotation protocol; configs/commits/checkpoint hashes/licenses; raw predictions с frame timestamps/model identity; candidate/route/reject logs; fusion/temporal/event logs с объяснением suppression; export/compiler/parity logs; load trace и hardware inventory; таблица ablations/thresholds; error atlas с source session; freeze manifest; отдельный lockbox report. Это список будущих артефактов: они в этом исследовании не созданы.

**Интерпретация исходов.** A уменьшает FP и сохраняет deadline recall в согласованных пределах — оставить A; пропадает много истинных proposals после V — изменить route/задачу или reject. C не даёт D2-only rescue либо fusion gain исчезает при fixed FP — сохранить лучший одиночный D. C качественнее, но queue deadline провален — использовать ensemble как teacher, не как финальный runtime. D выигрывает только на длинных эпизодах, теряя короткие — сузить сценарий или отклонить. E сохраняет gain после conversion и выигрывает у такого же supervised student — обоснован один production graph; иначе выигрыш KD не доказан. Любой вариант без LinQ pass не готов к защите как финальный.

**Чего даже успешный эксперимент не докажет:** промышленную сертификацию, пригодность к неизвестным ракурсам/пылевым режимам, новые классы вне разметки, все невидимые нарушения, другие масштабы multistream, устойчивость при смене camera layout, перенос GPU throughput на TPU, независимость от источников pretraining, абсолютную гарантию не пропустить инцидент. Это ограниченный target test, а не обещание безопасности.


## F099 — W1-10: Передачи и точные открытые вопросы

- Происхождение/locator: [W1-10](_WORK/W1_10.md), раздел «Передачи и точные открытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


- **Root / выбор MVP:** выбрать dominant error и одну проверяемую добавку. По умолчанию online C с двумя непроверенными detector не брать. Вопросы для решения: какие конкретные события приоритетны, каков `B_FP`, `L_max`, допустимый trade-off recall/precision, сколько streams и людей одновременно? Не считать «accuracy важнее» численным ответом.
- **W1-02 detector:** какой pinned D реально сохраняет high-recall proposal mode после export; какие головы/NMS/custom classes; можно ли получить person proposals независимо от tiny target score; какие checkpoints/лицензии входят в финальную пару? Нужен и более сильный offline teacher, и одинаковый supervised student контроль.
- **W1-09 calibration:** разделить detector threshold, proposal gate, verifier score, model weights, WBF IoU/skip/conf_type и event thresholds; калибровать на development data, оценить rare one-model positives и calibration после fusion. После появления `_WORK/W1_09.md` сверены релевантные разделы: WBF negative result, тот же pinned SHA и необходимость заново проверять calibration после изменения fusion согласованы. Уточнение для общего протокола: использовать роли development **CAL/TUNE/CHECK**, trial ledger и cache до необратимых cutoff/NMS; V/T и WBF добавляют собственный selection search. `avg` не равна автоматически calibrated probability. Вопрос к W1-09: есть ли достаточно независимых групп для такой вложенной настройки; иначе ограничить shortlist, оставить identity+threshold baseline и признать exploratory результат.
- **LinQ / W1-16:** exact CPU/TPU/SDK/operators/static shapes/precision, одновременная residency двух graphs, model-switch overhead, CPU fallback visibility; streaming state inputs/outputs для TSM; 3D/group ops для X3D; можно ли neural V/T на CPU именно этого сервера считать допустимым LinQ inference? Ответ должен содержать target compile/parity/quality/load evidence, а не общее «ONNX поддерживается».
- **Video/event architecture:** anti-ID-reuse reset, max candidates, burst handling, timestamps и late events; один инцидент→одна тревога без merging независимых людей. Сравнить CPU temporal baseline до neural T. Нельзя скрывать dropped evidence через красивый FPS.
- **Behavior/datasets:** только запрос подходящей causal task/target clips, visibility labels и hard negatives. Полный exhaustive поиск behavioral weights/datasets здесь не повторялся. Geometry/calibration camera-specific rules переданы соответствующей ветке; они не заменяются WBF.

Готовность ветки: **пять условных архитектур, отрицательные результаты, recall ceilings, ресурсные обязательства и различающий протокол сформированы; production choice заблокирован неизвестными target quality и LinQ execution, которые должны быть измерены будущим экспериментом.** Это завершённое исследование решения, а не выполненный benchmark.


## F100 — W1-11: Решение

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Решение»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S119, S123, S125, S129.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F100. Организовать последовательный портфель решений, а не общий sweep архитектура×данные×разрешение×LR.** Очередь: контракт данных/метрик → smoke с проверкой возобновления → одна полная baseline recipe → максимум две обусловленные ошибками абляции → при оставшемся бюджете один challenger → подтверждение лучшей конфигурации и incumbent → фиксация всего pipeline → однократный lockbox. Число «две» — предлагаемое организационное ограничение первой итерации, не научный оптимум. Новая гипотеза заменяет ещё не начатую в очереди; не автоматически расширяет бюджет. Конкретная исполнимая очередь ниже.

**F100. Для первой пары YOLO/DETR не применять агрессивный ASHA по первым эпохам.** Источники не устанавливают сохранение раннего detector ranking для наших данных. Более того, pinned recipe явно меняет фазы по горизонту. Сначала нужна хотя бы одна завершённая допустимая траектория; early-rank screening использовать только внутри одной семейной recipe и после проверки на завершённых траекториях. Если такая проверка стоит столько же, сколько оставшиеся полезные runs, обойтись ручной очередью без ASHA. [S119–S123]

**F100. Главный дефицит — возможность принять и проверить решение до дедлайна.** До запуска следующего training job зарезервировать время и ресурс на подтверждение, внешний evaluator, экспорт/parity и измерение inference на LinQ. Рост detector AP без допустимого полного пути не является победой по кейсу. Латентность, своевременный event recall, FP/экспозицию, дубли и coverage считать по согласованному контракту evaluation/video веток; конкретные лимиты должны быть утверждены, здесь они не придуманы.

**F100. При 1–2 GPU полезнее прозрачный manifest+FIFO и узкие controlled comparisons, чем инфраструктура массового HPO.** Optuna подходит как журнал и последующий ограниченный search; Ray — когда уже есть надёжный trainable, несколько независимых trials и обоснованный pruning. TPE не даёт бесплатного знания при нескольких завершённых trials: default startup=10, а Hyperband делит историю по brackets. Это не аргумент запускать дополнительные десятки trials ради алгоритма. [S125–S129]


## F101 — W1-11: Что именно сравниваем

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Что именно сравниваем»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S132.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F101. Один trial — неизменяемый контракт исполнения и оценивания.** Перед baseline фиксировать: code SHA, env lock/container digest, checkpoint source+SHA256+license path, ontology/class order, annotation/split hashes, camera/scene/episode groups, preprocessing, physical/effective batch, AMP, accumulation, optimizer с явными LR/WD, полный schedule+warmup+augmentation phases, checkpoint-selection rule, seed, validation cadence, evaluator version. Весовой license каждого кандидата — handoff W1-02; этот отчёт не разрешает использовать неподтверждённые веса.

Нужны два разных вопроса и разные таблицы:

1. **Resource-bounded product comparison:** какой *полный recipe+pipeline* лучше к дедлайну при измеренном доступном бюджете? Архитектурам допустимы разные штатные optimizer/schedules; это сравнение готовых вариантов, не причинный вывод об архитектуре.
2. **Ablation:** что меняет один выбранный фактор на данном recipe? Остальное одинаково, парные seeds и группы. Если изменение фактора требует другого batch/LR/schedule, это новый bundle; описать его целиком либо разрешить одинаково ограниченный nuisance search для обоих вариантов. По одному LR для разных архитектур нельзя заявлять «архитектура объективно хуже». [S132]

Честность не равна одинаковому числу эпох. При изменении train sampling/replay количество images и optimizer updates за epoch меняется; считать фактические processed images, optimizer steps и wall time. При большем входе эпоха дороже. При ином GPU equal wall time не изолирует recipe. Парные comparisons по возможности выполнять на одной модели GPU/окружении; если оборудование сменилось, маркировать block и измерять time заново. Разделить equal-updates ablation и equal-wall-time product test.

Metrics contract до просмотра результатов: primary — timely event recall по выбранным сценариям при согласованном FP/camera-hour, dedup/latency/coverage ограничении; secondary — per-class AP/recall и small-object slices для диагностики, retention старых нужных классов, per-camera/lighting/occlusion. Если event evaluator ещё не готов, detector criterion честно помечается proxy и не определяет окончательного победителя. Все пороги, temporal persistence, cooldown, checkpoint, TTA/ensemble являются объектами отбора и учитываются в журнале, даже если не требуют GPU training.


## F102 — W1-11: Исполнимая очередь с воротами и результатами

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Исполнимая очередь с воротами и результатами»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**Это адаптивная очередь ограниченной ширины: следующая строка исполняется только после решения предыдущей. Номера runs ниже — предел предлагаемых действий, не заявленные измерения или обязательство потратить бюджет.**

| Шаг | Вход и действие | Пропуск дальше / остановка | Артефакт и смысл |
|---|---|---|---|
| **0. Contract** | Выбрать priority scenarios, полную ontology; train/DEV/SELECT при достатке групп/lockbox. Утвердить practical gain δ, FP budget, latency/retention/coverage gates и deadline | Нет независимых positives/полных labels/прав на данные — исправление данных до HPO. Не делить соседние кадры для красивого n | Immutable manifest и evaluation specification; предотвращает неопределённый target |
| **1. Smoke** | Один выбранный pretrained baseline. На разрешённом доступном GPU: трудные размеры/плотность целей, несколько optimizer steps+EMA, validation, save/reload и короткое resume сравнение. Отдельно ранняя LinQ compatibility проверка у соседней ветки | NaN, неверный mapping, OOM или broken resume — остановка и исправление; после изменения batch/input новый smoke. Не сравнивать accuracy smoke subsets | Logs peak memory, actual step/LR trace, checksums и resume status; это проверка осуществимости, не модели |
| **2. Baseline** | B0: одна полностью заданная pretrained YOLO26s recipe из W1-06, с явным optimizer и горизонтом H, а не auto/time-adaptive schedule. Полный DEV по согласованной cadence; сохранить phase checkpoints/raw predictions | При technical fail не считать проигрышем accuracy. При incomplete labels исправлять dataset version и заново сделать B0. При нормальном run довести через предусмотренную late phase, кроме hard deadline/валидного safety stop | Первая завершённая learning curve и fixed error audit; измеренные setup/train/val/save costs |
| **3. Targeted A1** | По baseline audit выбрать **один** главный механизм из ранжированного списка ниже. Один comparator B1 против B0, seed и данные парные | Нет ожидаемой ошибки в audit — эту гипотезу не запускать. Не проходит mandatory retention/latency — reject product candidate; шум/широкие интервалы — unresolved, не победа | Таблица paired differences по событиям/группам, цена изменения |
| **4. Targeted A2 (optional)** | Только если есть другой независимый значимый residual gap и после reserve остаётся ресурс: B2 относительно текущего incumbent; либо проверка interaction, если B1 эффект зависит от nuisance LR | Нельзя проверить исход/интегрировать до deadline — skip. Не добавлять третий фактор ради удобства настройки | Один ответ на следующую decision-changing неопределённость |
| **5. Challenger (optional)** | Только если baseline family не решает нужный gap и challenger проходит resource/export prerequisites: одна D-FINE-M recipe, RF-DETR-M **заменяет** её при блокере; не оба автоматически | Нельзя вместить полный согласованный schedule с поздней фазой и проверку — не запускать. Ранняя AP слабость без model-specific evidence — не pruning proof | Product comparison конкретных recipes с одинаковыми split/evaluator; не чистая architecture ablation |
| **6. Confirmation** | Заморозить ≤2 recipes: incumbent и выбранный кандидат. Новые парные seeds на том же train/DEV; SELECT используется ограниченно для окончательного выбора recipes при заранее указанном числе финалистов | Если бюджет допускает только одну повторную пару, так и сообщить: малая устойчивость, без убедительного seed distribution. Нет повторов — result remains screening. При неразличимости выбрать простой прошедший gates incumbent | Все seeds, не лучший seed; frozen selection rationale, неопределённость по независимым группам |
| **7. Lockbox/deployment** | Зафиксировать checkpoint/preprocess/pipeline/thresholds; LinQ parity и полный path measurement; один lockbox для выбранной конечной системы | Ничего не подкручивать по lockbox. Неудача — честный fail и новый цикл с новым независимым тестом, если доступен; не «открыть снова» | Final manifest, predictions/events/latencies, coverage, boundary of evidence |

Начальная обязательная training нагрузка — B0; B1 назначается только после audit; optional rows не расширяют срок. Confirmation — резервируемая работа, не всё, что останется после бесконечного поиска. Freeze→unfreeze из W1-06 допускается как конкретная recipe-гипотеза; одинаковый общий compute/число updates и независимая проверка важнее красивого числа эпох.


## F103 — W1-11: Ранжирование гипотез и ценность информации

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Ранжирование гипотез и ценность информации»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


Ранги — инженерная рекомендация для предполагаемого PPE/phone/safety pipeline; фактический error audit может переставить2–5. Не присвоены выдуманные probabilities, expected AP gains или GPU-hours.

| Приоритет | Гипотеза и различающий опыт | Stop/accept/reject | Ценность информации и opportunity cost |
|---|---|---|---|
| **H0 — до runs** | Ошибка class map, missing labels/независимости или evaluator сильнее модельного gap. Просмотреть фиксированный DEV error corpus, проверить parent lineage, outputs и полную target-разметку | Исправлять реальную ошибку и bump manifest; старые цифры не смешивать с новыми. Нельзя называть correction model gain | Очень высокая: может обесценить весь sweep; требует прежде всего annotation/evaluator времени |
| **H1 — blocker** | Recipe реально исполнима и artifact возобновим/переносим. Smoke и ранний LinQ gate | Не прошёл — technical fix/fallback, без accuracy ranking | Самая высокая до baseline: предупреждает покупку бесполезного обучения |
| **H2 — после audit** | Маленькие СИЗ теряются из-за spatial signal. B0 vs один higher input **или** person ROI/crops с правильной lineage; не менять оба | Если small-object miss не доминирует — skip. Есть recall gain, но latency/coverage fail — не принять product variant. Новая association проверяется отдельно | Может решить целевой bottleneck; дорого по train/inference, поэтому сначала наличие ошибки и memory smoke |
| **H3** | Адаптация теряет person/phone/технику: new-only vs replay/mixed при одинаковой union ontology и сопоставимом updates budget | Нет полной разметки — dataset fix до опыта. Нарушение retention floor — reject; target gain без retention недостаточен | Высокая, когда downstream зависит от старых классов; дополнительные эпохи не исправляют скрытые labels |
| **H4** | Малый домен переобучается: full vs ограниченный freeze→unfreeze **или** один уровень augmentation; LR nuisance зафиксирован с ограничением вывода | Train/DEV gap отсутствует — не автоматически запускать. Слишком сильный freeze не адаптируется — вернуть full. Не обрезать до unfreeze/clean phase | Умеренный implementation cost, интерпретируемый ответ; нельзя одновременно ослабить augmentations и поменять init |
| **H5** | Есть underfit/optimization gap: узкий явный LR comparison на текущем recipe, либо продолжение фиксированного schedule | Только если labels/spatial diagnosis исключены и кривые оправдывают. Плоский noisy DEV не доказательство LR проблемы. Не хватает полного horizon — skip | Часто дешевле architecture replacement; цена — та же validation adaptation и ещё один полный run |
| **H6 — conditional challenger** | Один иной detector family исправляет устойчивый residual miss при приемлемом полном пути | Только после compatibility/memory gate и полного recipe. Не проходит LinQ или неразличим — оставить incumbent | Высокая только при конкретном family bottleneck; максимальная integration+training цена |
| **H7 — обычно отложить** | Ensemble/TTA/teacher/distillation даст полезный gain | Не делать при невыполненной latency или отсутствии frozen single-model baseline; сначала измеримый upper-bound gap и права на веса | Сложность и inference cost могут поглотить всю проверку; низкий приоритет в первой итерации |

**F103. Ценность информации оценивать через изменение решения, а не через обещание роста mAP.** Для каждой карточки записать: какая неизвестная блокирует выбор; какие наблюдаемые исходы меняют действие; минимальный различающий опыт; train+engineer+validation+integration cost; что придётся отложить. Если при любом исходе остаётся тот же допустимый pipeline, training trial почти не даёт decision value. Если baseline не запускается на LinQ, ещё одна тонкая LR точка имеет меньшую ценность, чем compatibility experiment. Если кандидаты различаются меньше, чем позволяет число независимых эпизодов, новая разметка независимых событий полезнее ещё одного nearby LR.

Формальный EVSI требует вероятностной модели исходов и utility решений; таких данных нет. Не выдавать ordinal high/medium/low за денежную expected value. Допускается прозрачная таблица subjective priority, пересматриваемая после результатов. Бюджет сокращает ширину, а не разрешает убрать независимую оценку.


## F104 — W1-11: Бюджет, deadline и прекращение поиска

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Бюджет, deadline и прекращение поиска»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F104. Планировать wall time из измеренного smoke/baseline, а не «50эпох≈Nчасов».** После baseline записать setup/download-data/environment time, train step distributions, val time, phase-transition/EMA/checkpoint overhead, upload и восстановление. Не скачивать большие данные до отдельного resource/data authorization. Из будущих затрат отделить расходуемый GPU-budget, календарный critical path и время инженера.

До optional trial вычислить консервативную осуществимость:

`remaining_calendar >= setup_i + complete_recipe_i + eval_i + artifact_i + integration_i + confirmation_reserve + final_eval_reserve + interruption_margin`.

Для GPU-лимита — отдельное ограничение суммарных GPU-seconds; два параллельных one-GPU trials расходуют сумму, не половину. Все слагаемые — измеренные оценки/диапазоны, unknown явно unknown; запас на прерывание задаётся командой, не выдумывается в отчёте. Если верхняя разумная оценка не укладывается, следующий trial не начинать. Если estimates отсутствуют, сначала measurement task меньшего масштаба. Полученная авторизация на исследование не разрешает аренду Vast.

При одной GPU — FIFO с приоритетом подтверждения incumbent; baseline не прерывать новым speculative challenger. При двух одинаковых проверенных GPU — парный baseline/comparator либо confirmation pair; concurrency=2 только после измеренного RAM/I/O и сохранения artifacts. Не делить одну GPU дробными Ray allocations без отдельной fit/contestion проверки; scheduler resource token не измеряет VRAM. Один DDP trial на обеих картах конкурирует с двумя independent trials; выбор по измеренному wall time и вопросу опыта, не по числу карт. DDP не трактуется как объединённая24+24 GB память.

Три класса stop reason в журнале:

- **INVALID/FAIL:** corrupt mapping/data/evaluator, NaN, OOM, checkpoint/resume defect. Не считать низким objective; не позволять surrogate «учиться» на произвольном нуле вместо failed score. Сохранить затраты и причину; исправленный recipe получает новую версию.
- **RESOURCE_STOP:** deadline/лимит/host loss. Сохранить continuation artifact и статус incomplete. «Не успел» — допустимый product вывод о ресурсе, но не доказательство низкого финального качества архитектуры.
- **PERFORMANCE_STOP:** заранее обоснованный pruning/futility по DEV и согласованной resource phase. Plateaus не обрезают обещанную позднюю фазу. Sequential просмотры DEV — exploratory; не обычные независимые p-values.

Глобальные остановки: достигнут приемлемый pipeline и дальнейшая гипотеза не меняет решение; нет времени на confirmation+LinQ; все оставшиеся кандидаты нарушают обязательный gate; прирост не различим на доступных независимых группах. Сигнал «два последовательных targeted comparisons без practically meaningful gain» можно использовать как **предлагаемое управленческое правило** завершить exploration, но это не статистическая гарантия отсутствия лучшей конфигурации. Не продолжать до первого случайно удачного seed.


## F105 — W1-11: ASHA: когда допустим и где ломается интерпретация

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «ASHA: когда допустим и где ломается интерпретация»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S119, S120, S121, S122, S124, S128, S129.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


ASHA распределяет ресурс по rungs, опираясь на промежуточный scalar ranking, и уменьшает ожидание stragglers; полезность ранней метрики остаётся предпосылкой практического применения. Опубликованный большой parallel speedup нельзя переносить на 1–2 GPU. В Ray cutoff считается по уже поступившим rung results: одинаковый search seed при ином порядке завершения не гарантирует ту же историю; при малом количестве trials cutoff особенно нестабилен. [S119,S120,S128]

**F105. Проверять переносимость early ranking ретроспективно до pruning.** На уже завершённых admissible runs собрать ранги DEV в кандидатных rungs и на фиксированном финальном horizon/checkpoint rule; посмотреть Spearman/Kendall **и** сохранение будущих top-k, число ошибочно удаляемых practically good candidates. Одной высокой correlation мало: потеря единственного нужного кандидата скрывается aggregate correlation. Не оценивать только survivors — у pruned отсутствуют финальные outcomes. Если потребуется pilot, заранее выделить небольшую контрольную долю non-survivors до полного горизонта; стоимость pilot/аудита входит в бюджет. На двух-трёх кривых корреляция описательная, не надёжная валидация ASHA.

Условие допуска: одна family/init/data recipe, сопоставимая progress axis, завершённый warmup, достигнута значимая phase, future winners не исчезают на калибровочных runs, остаётся экономический смысл pruning. При rank reversal, late clean-phase recovery или отсутствии независимого подтверждения — увеличить grace либо выключить pruning. Если grace приходится ставить почти в H, экономия мала; FIFO проще. Cross-family YOLO/DETR rankings и разные pretrained starts не смешивать. Контрпример detector literature показывает разные скорости сходимости, но не измеряет наш ranking. [S124]

В pinned Ultralytics H меняет LR trajectory; `epochs` влияет на расчёт iterations и `optimizer=auto` может выбрать другой optimizer. `close_mosaic` привязан к концу. `time` даже переоценивает horizon после epochs. Поэтому run `epochs=10` — не первые10эпох `epochs=100`; для low-fidelity прерывать **изначально заданный H schedule**, а не каждый rung заново с новымH. Альтернатива — специально сжатая короткая recipe; тогда она оценивает другую recipe, требуется отдельный transfer check. У D-FINE132/120 с поздней reload/EMA стадией ранний stop вообще не видел финальную фазу. [S121,S122]

Для Ray 2.59.0 проверены `ASHAScheduler(time_attr="optimizer_steps", metric="dev_proxy", mode="max", max_t=H_steps, grace_period=G_steps, reduction_factor=2, brackets=1)` и `tune.report({"optimizer_steps": step, "dev_proxy": score}, checkpoint=...)`. **Это API-шаблон, не запущенный trainable.** H/G должны быть заполнены из full recipe/рангового pilot; значение2 — осторожный предлагаемый коэффициент, не оптимум. `optimizer_steps` монотонен и присутствует при каждом decision report; ASHA max_t не меняет внутренний LR schedule. `training_iteration` растёт на каждый report, а не на каждую эпоху. При rare validation rung может быть перескочен; зафиксировать report cadence и валидировать попадание. Missing metric/time key в этом коде приводит к CONTINUE, поэтому integration smoke должен проверять schema. [S128,S129]

Не принимать документационное «top half» за точное число surviving trials при async small-n. Ray здесь выполняет STOP/CONTINUE, не автоматическое доказательство сохранения лучших. Монотонные optimizer steps улучшают progress comparison, но не делают одинаковым compute разных разрешений/архитектур. Wall-time metric отвечает другому resource-bounded вопросу и на неодинаковых/загруженных GPU дополнительно смешивает hardware effects.


## F106 — W1-11: Optuna/Ray и multi-objective без устаревших примеров

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Optuna/Ray и multi-objective без устаревших примеров»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S125, S126, S127.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F106. Зафиксировать API версии, не копировать4.x defaults.** В Optuna 5.0 default sampler изменён: single-objective multivariate и constant-liar поведение, multi-objective default теперь TPE. Для воспроизводимости указывать sampler явно. `TPESampler(seed=..., n_startup_trials=10, multivariate=True, constant_liar=True)` — проверенная5.0 signature, но при малом search budget использовать явный RandomSampler/ручной список обычно честнее, чем обещать обученный surrogate. Hyperband имеет несколько bracket histories, усиливая startup overhead. [S125,S127]

Одноцелевой scalar objective с pruning: `trial.suggest_float("lr", lo, hi, log=True)`, `trial.report(dev_proxy, step=optimizer_step)`, затем `if trial.should_prune(): raise optuna.TrialPruned()`. Шаг неотрицательный integer; одинаковый step нельзя переиспользовать для другого checkpoint, новая запись не заменяет первую. Без прошедшего early-rank gate — `NopPruner`, без intermediate pruning. Параллельные trials и seed не обеспечивают одинаковый порядок sampler suggestions; журналировать actual configs. [S126]

Для полного Pareto search API: `create_study(directions=["maximize", "minimize"], sampler=..., pruner=NopPruner(), storage=..., study_name=..., load_if_exists=True)`; objective возвращает `(timely_recall, measured_linq_p95_latency)`. В5.0 `trial.set_constraint("false_alert_rate", observed_fp_rate - fp_limit)` и аналогично coverage/retention; feasible при всех<=0. `constraints_func` в sampler deprecated. **`Trial.report`/`should_prune` multi-objective не поддерживают**; нельзя выдать обычную Optuna pruning интеграцию за готовый многокритериальный ASHA. Unknown LinQ latency нельзя заменять desktop GPU surrogate и считать ограничение измеренным. [S125–S127]

На этом кейсе предпочтительнее **feasibility gates + Pareto ledger**, а не дорогое автоматическое Pareto exploration: собрать detector candidates на DEV, измерить полный LinQ pipeline у 2 финалистов и выбрать допустимый recall/FP/latency tradeoff. Hard constraint не превращать в вес scalar score, где лишний AP компенсирует неприемлемую задержку. Latency, coverage, FP и recall связаны; единый universal «accuracy score» кейсом не задан. Training wall time — search cost, inference latency — свойство product pipeline: не смешивать оси.

Если понадобится Ray+Optuna интеграция, отдельно проверить адаптер на установленных версиях: в этом исследовании не доказана совместимость их integration wrappers с Optuna 5.0. Комбинация двух scheduler/pruner механизмов не назначается автоматически. Для 1–2 GPU один orchestrator и простой persistent manifest уменьшают число незаметных stopping policies.


## F107 — W1-11: Многократный отбор и независимость

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Многократный отбор и независимость»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S130.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F107. Repeated DEV — обучающий сигнал для команды, поэтому его победный score оптимистичен.** Cawley/Talbot показывают сам механизм selection overfit; он относится не только к LR: просмотр ошибок, подбор threshold/event persistence/checkpoint/seed/ensemble тоже выбирает по finite sample. Больше кадров из того же эпизода не создаёт больше независимых наблюдений. [S130]

Практический протокол:

1. Split по camera/scene/episode lineage **до** frame/crop extraction. Тот же человек/сцена/neighbor frames по обе стороны отменяют соответствующее заявление независимости. Если камер мало, честно писать within-camera temporal holdout; unseen-camera evidence отсутствует.
2. DEV разрешает checkpoint/threshold/event-policy tuning; хранить полный selection ledger, все trials и все просмотры. Правило выбора checkpoint одинаковое для сравниваемых runs; фиксировать eval cadence и число кандидатов, иначе run с большим числом checkpoint lotteries получает преимущество.
3. Если достаточно групп, SELECT отделить для заранее ограниченного списка ≤2 финалистов. Пороги фиксировать на DEV; SELECT выбирает готовый pipeline по тому же критерию. SELECT после просмотра уже selection data, не независимая оценка конечного качества. Не добавлять десятки новых вариантов после проигрыша.
4. Confirmation сравнивает recipes на новых парных seeds; не выбирать лучший seed как доказательство. Разброс по seeds и неопределённость по camera/episode — разные источники. Одинаковый seed уменьшает часть variation, не делает стохастику идентичной между implementations.
5. Для нескольких утверждений о приростах заранее ограничить confirmatory contrasts. Если нужны p-values, использовать подходящий correction для заданного семейства сравнений и план проверок; обычные 95% интервалы после adaptive selection не являются selection-adjusted. В малом хакатоне надёжнее показать paired differences/cluster intervals и осторожный вывод, чем десятки неучтённых значимостей.
6. Lockbox не открывать до фиксации всего пути. Один выбранный pipeline и заранее заданная отчётность по обязательным slices. Если lockbox повлиял на выбор/порог, он перестал быть lockbox; не переименовывать его обратно. Не refit train+DEV после test без признания нового artifact и новой проверки.

Если независимых групп не хватает на 4 части, не делать четыре микроскопических псевдотеста. Возможен train/DEV/lockbox с меньшим числом гипотез; либо nested grouped evaluation при достаточном ресурсе. Ограничение power остаётся; «не доказали отличие» не означает эквивалентность. При неоднозначности предпочесть простую допустимую recipe и сообщить uncertainty. Practical δ и floors утверждать до результатов, исходя из scenario utility, не выбирать после красивой разницы.


## F108 — W1-11: Различающий эксперимент W1-11-E1

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Различающий эксперимент W1-11-E1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**Вопрос:** даёт ли один обусловленный baseline-ошибкой фактор практически полезное улучшение полного pipeline, и можно ли сократить subsequent search ранним pruning без потери будущего допустимого победителя?

**Входы:** pinned baseline из W1-06; разрешённые weights/license; immutable train/DEV/(SELECT)/lockbox с group lineage; evaluation contract W1-01/04/05; реально доступный авторизованный GPU; LinQ runtime/SDK у deployment-ветки; measured time ledger. Утверждённых H, δ, FP/latency limits здесь нет, заполняются до запуска.

**Процедура:** после contract/smoke завершить B0. Провести fixed error audit. Выбрать один H2/H3/H4 и B1, полный H и late phase сохранить. Выполнить B1 с парным seed; оценить raw predictions одним evaluator. Если эффект полезен и gates пройдены, выделить confirmation pair на новых seeds. По уже завершённым learning curves ретроспективно проверить кандидатный G: кого ASHA остановил бы, и потерян ли practically good/final winner. При недостатке кривых ответ о безопасном pruning — unknown; новый sweep ради доказательства не обязателен. Freeze candidate pipeline; выполнить LinQ parity/latency и SELECT/final lockbox по очереди выше.

**Метрики:** timely event recall при FP budget; duplicates/late alerts/coverage; p50/p95 полного event-to-alert path и source-camera exposure; per-class detector/retention/small-object diagnosis; paired differences по независимым группам; seed variability; measured GPU/calendar/engineer cost; для раннего отбора top-k retention и false-prune count. Detector AP и train loss не заменяют event metrics.

**Артефакты:** hypothesis card с ожидаемым механизмом и stop rule; полные resolved configs+SHA/env; weights provenance+SHA256; split/annotation/lineage hashes; LR/optimizer-step/augmentation-phase traces; checkpoint paths+hashes и selection rule; smoke/resume/memory logs; per-group predictions/events, exposure/latency; all-trial status+cost ledger; frozen threshold/event logic; final decision record; export/parity handoff. Сохранять не только лучший summary CSV.

**Исходы:** B1 устойчиво улучшает δ и проходит full-path gates — принять recipe; gain только в AP — продолжить event diagnosis, не объявлять product win; gain исчезает на confirmation или неразличим — incumbent и bounded claim; early pruning теряет будущего победителя — выключить/сдвинуть G; не проходит LinQ — fallback/совместимость; data contamination — аннулировать независимое сравнение и исправить split. Успех не доказывает промышленную безопасность, generalization на неизвестные камеры, корректность калибровки, качество INT8 или соблюдение ограничений на иной LinQ конфигурации.


## F109 — W1-11: Противоречия, отрицательные находки и передача

- Происхождение/locator: [W1-11](_WORK/W1_11.md), раздел «Противоречия, отрицательные находки и передача»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.


**F109. Нет проверенного универсального `grace_period=5/10`, числа эпох, VRAM-fit или оптимального количества runs для этого кейса.** Удобный пример ASHA — API demonstration. Заголовок D-FINE recipe «Early stop» из соседней ветки не заменяет adaptive stopping logic; прочитанная M custom recipe фиксирована 132/120. Официальный short-tuning guide сам предупреждает о transfer bias. Разные источники рекомендуют разные brackets: статья ASHA обсуждает3 агрессивных brackets, Ray scheduler guide рекомендует 1; для исполнения важна pinned implementation, а не смешение defaults. TPE defaults старых руководств не относятся автоматически к 5.0.

При поиске найден detector-NAS paper A. Kot *Minimum Fidelity…* (DOI 10.18372/1990-5548.88.20966); открыта [страница автора/abstract](https://jrnl.kai.edu.ua/index.php/ESU/article/view/20966). Полный paper в этой ячейке не прочитан, поэтому его числа epochs/rank thresholds не используются как доказательство или готовая настройка. Нет primary evidence, что ранний AP нашей YOLO/DETR пары сохраняет финальный ranking. Неверно трактовать этот пробел как доказанную бесполезность ASHA вообще.

Передачи:

- **W1-01/evaluation, W1-04/05/video/events:** утвердить unit of independence, δ/floors/FP budget, timely-event rule, exposure и cluster uncertainty; определить достаточность SELECT и confirmation. Дедуп и cooldown входят в selection ledger.
- **W1-06/training:** baseline immutable recipe, explicit optimizer, H и late phases; одинаковые manifests; shape/class-map logs; контроль replay/retention. Не переносить final H recipe на rung, меняя H.
- **W1-02/models и W1-10/LinQ/export:** один conditional challenger; права на конкретные веса; compatibility до дорогой адаптации; latency/parity у 2 финалистов, unknown TPU не считать Coral. Quantization и camera calibration вне этой ячейки.
- **W1-14/15/resources/reproducibility:** measured setup/val/artifact/resume overhead и реальный checkpoint continuation; reserve/stop rules; хранить INVALID отдельно от PRUNED/RESOURCE_STOP. Не авторизованы аренда/платежи.

Открытые вопросы, меняющие решение: какой deadline и реально разрешённый compute budget; какое число независимых камер/положительных эпизодов; есть ли полная ontology/разметка старых классов; согласованы ли objective и mandatory limits; какой exact LinQ runtime и возможность раннего smoke; сколько полных recipes и парных повторов укладывается после measured baseline; даёт ли rank pilot практическую экономию. Пока ответы неизвестны, исполнимы contract и подготовка manifest; обещание «50 experiments» не является планом.


## F110 — W1-12: Решение прежде деталей

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Решение прежде деталей»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


**Vast.ai остаётся практическим кандидатом для обучения, но закупочная единица — конкретный оффер с диском, сетью и сроком, а не «3090 по фиксированной цене».** Публичный endpoint реально вернул 1× и 2× RTX 3090 с `gpu_ram=24576`, `rentable=true`, `rented=false`. Это наблюдаемая доступность в момент ответа, не резерв и не гарантия будущей цены. Для команды разумна первая проверка **одной on-demand GPU**, затем решение о второй по измеренному time-to-result и стоимости. Это рекомендация исследователя, не уже выполненная закупка [F110–F04].

Не выбирать автоматически минимум: предварительный поиск без reliability-порога показывал verified-хосты около 75% исторической надёжности и ограниченную мощность GPU. Формальная верификация не равна надёжному выполнению именно нашей задачи. Цены ниже относятся только к повторяемой выборке reliability ≥99%, 100 GB и on-demand. Финальная нейросетевая обработка по условиям команды должна работать на LinQ; успешная тренировка на CUDA ничего не доказывает о CPU/TPU LinQ [F110].


## F111 — W1-12: Наблюдения и источники цен

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Наблюдения и источники цен»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


**F110.** GET `https://console.vast.ai/api/v0/bundles/` с URL-параметром `q` вернул HTTP 200 **без Authorization/cookies/credentials**. Запрос, полный исходный JSON и HTTP Date сохранены в [offers_1gpu_100gb.json](_WORK/W1_12_MATERIALS/offers_1gpu_100gb.json), [offers_2gpu_100gb.json](_WORK/W1_12_MATERIALS/offers_2gpu_100gb.json). Время HTTP Date немного раньше локального получения: `Fri, 23 Oct 2026 17:04:32 GMT` и `17:04:33 GMT`; не подменяю его временем аренды.

Общие фильтры: `verified eq true`, `external eq false`, `rentable eq true`, `rented eq false`, `gpu_name eq "RTX 3090"`, `num_gpus eq 1/2`, `reliability gte 0.99`, `disk_space gte 100`, `allocated_storage=100`, `type="on-demand"`, `limit=3`, `order=[["dph_total","asc"]]`. Это ограниченная выдача, не перепись мирового рынка. Три результата не означают три независимых физических GPU; два оффера ниже относятся к одной машине.

**F111. Снимок цен, USD; источник каждой строки — указанный исходный API JSON.** `Run` уже включает 100 GB storage и исключает usage-based bandwidth. `Disk` — `storage_total_cost` в $/h, не цена за GB. Ставки округлены здесь; полный precision сохранён в JSON.

| Оффер / machine / host | GPU / страна | Compute `dph_base`, $/h | Disk 100 GB, $/h | Run `dph_total`, $/h | Ingress / egress, $/TB | Reliability |
|---|---|---:|---:|---:|---:|---:|
| 55729405 / 28164 / 159579 | 1× / India | 0.186667 | 0.031481 | 0.218148 | 0.666667 / 0.666667 | 99.70434% |
| 45174323 / 144003 / 451840 | 1× / CN (регион пуст) | 0.213333 | 0.027778 | 0.241111 | 2.666667 / 4.000000 | 99.81753% |
| 47272935 / 36023 / 102063 | 1× / Taiwan | 0.240000 | 0.027778 | 0.267778 | 26.666667 / 26.666667 | 99.94703% |
| 45174324 / 144003 / 451840 | 2× / CN (та же машина) | 0.426667 | 0.027778 | 0.454444 | 2.666667 / 4.000000 | 99.81753% |
| 56506123 / 117305 / 446310 | 2× / Oregon | 0.480000 | 0.055556 | 0.535556 | 4.000000 / 6.666667 | 99.24482% |
| 57219980 / 140986 / 492668 | 2× / Taiwan | 0.533333 | 0.027778 | 0.561111 | 2.666667 / 4.000000 | 99.08642% |

`internet_down_cost_per_tb` — вход на rented machine; `internet_up_cost_per_tb` — выход с неё. Следовательно загрузка датасета с локального компьютера = ingress Vast; скачивание checkpoint на LinQ/локально = egress Vast. Нельзя ориентироваться только на направления кнопок браузера. Единицы API/CLI исторически подписаны TB/GB; для посрочного сверения invoices надо подтвердить byte divisor, а не молча смешивать SI TB и TiB.

**F111.** Во всех шести ответах `verification="verified"`, `hosting_type=0`. Secure Cloud здесь **не подтверждён**; числовой enum без отдельной документированной расшифровки не выдаю за сертификат. Во всех `bw_nvlink=0`; не предполагаем NVLink. Оффер 55729405 заявлял 18 effective CPU, `cpu_ram=64322`, disk BW 1299.1 MB/s, PCIe BW 10.1 GB/s, power 300 W, driver 580.126.09. У 2× 56506123 — только 8 effective CPU, disk BW 1615.98 MB/s, PCIe 6 GB/s, power 275 W. Это характеристики выдачи, не измерения исследователя. Цена второй GPU не доказывает ускорение вдвое.


## F112 — W1-12: Как считать до покупки

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Как считать до покупки»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


**F112. Формула для конкретного оффера (собственная бухгалтерская модель).** Пусть `G` — ставка compute за **весь оффер**, `D` — выбранный размер, `Srun(D)`/`Sstop(D)` — почасовой storage в соответствующем состоянии, `Trun`/`Tstop` — часы, `Vin`/`Vout` — оплачиваемые единицы TB, `Bin`/`Bout` — сетевые ставки. Тогда:

```text
C_vast = G*Trun + Srun(D)*Trun + Sstop(D)*Tstop
       + Bin*Vin + Bout*Vout
       + Σ(volume_hourly_i * volume_billable_hours_i)
C_project = C_vast + external_storage + external_egress + payment/FX/tax_if_applicable
```

Не умножать `G` ещё раз на число GPU, если взят `dph_base` multi-GPU оффера. Не добавлять storage повторно к `dph_total`: у снимков `dph_total = dph_base + storage_total_cost = search.totalHour`. В ответах `search.diskHour` и `instance.diskHour` совпали; `instance.gpuCostPerHour=0` — это структура расчёта оффера, **не доказательство состоявшегося stopped-инвойса**.

`storage_cost` имеет подпись CLI `$/Gb/Month`. Для 100 GB во всех шести строках наблюдается `storage_total_cost = storage_cost * 100 / 720`. 720 — восстановленный из этих ответов расчётный месяц, не календарное обещание и не основание игнорировать разные stopped-тарифы. Для точного расчёта предпочтителен готовый `diskHour` для нужного D. Код CLI фиксирован: [vast.py, commit 42c3a47…, строки 774 и 4369–4448](https://github.com/vast-ai/vast-python/blob/42c3a47b44603775a5e31f54de0fce3994bd3f11/vast.py#L774); он задаёт `allocated_storage=args.storage`. Локальная выдержка: [vast_cli_units_excerpt.txt](_WORK/W1_12_MATERIALS/vast_cli_units_excerpt.txt).

**Арифметическая иллюстрация, не прогноз времени обучения:** оффер 55729405, условные 10 running hours, 14 stopped hours, 0.1 тарифицируемой TB ingress и 0.02 TB egress, без volumes, при допущении одинакового diskHour: `10*0.218148148 + 14*0.031481481 + 0.12*0.666666667 = $2.702222`. Эти часы/объёмы выбраны только для проверки формулы. Допущение stopped-rate должно быть подтверждено перед оплатой; цена не включает неизвестные внешние налоги/FX/сервисы.

| Статья / риск | Что включить | Как ограничить до покупки |
|---|---|---|
| Compute | Настройка, подготовка и idle при running тоже занимают оплачиваемое время | Подготовить pinned образ/скрипт заранее; бюджет и время задаёт команда |
| Storage running/stopped | Размер allocation, не только занятые файлами байты | Выбрать D под image, данные, cache, optimizer, checkpoints; проверить оба rate |
| Ingress | Dataset, weights, package/image downloads, повторная миграция в пределах правил metering | Сохранить network rates; выяснить включение image pull в счёт, не считать его бесплатным без доказательства |
| Egress | Checkpoints, exports, logs, backup, передача на LinQ | Оценить количество копий; учесть также счёт источника внешнего хранилища |
| Volumes | Самостоятельный ресурс после destroy instance | Отдельно проверить и впоследствии удалить ненужные volumes |
| Срыв / expiry / outbid | Повторный прогон, повторные transfer и setup | Независимый backup, воспроизводимый resume, запас до deadline |
| Credits / autobilling | Предоплата и возможные автосписания | Не считать нулевой баланс spending cap; состояние аккаунта должен проверить его владелец |
| Reserved | Locked credits, ранняя отмена | Для первого smoke-test не требуется; отдельно сверить cancellation preview |
| FX, налоги, платёж | Не определены публичным оффером | Не заявлять итоговую сумму в рублях без способа оплаты/инвойса |


## F113 — W1-12: Lifecycle и противоречия документации

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Lifecycle и противоречия документации»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S134, S135, S136, S137, S138, S139, S140, S142, S143.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


**F110.** Compute не тарифицируется «по проценту GPU utilization»: активный экземпляр оплачивается по времени, даже когда dataloader/декодирование ждёт CPU. GPU exclusive, stopped не резервирует GPU; CPU/RAM baseline выделяются пропорционально доле GPU машины, burst сверх baseline не гарантирован. Память выше allocation может закончиться OOM. Поэтому таблица offer должна учитывать выделенные CPU/RAM, а не полный сервер [S139].

**F113.** Stop сохраняет container data, но оставляет storage charges; restart может ждать GPU неопределённо. Destroy уничтожает container data. Локальный volume переживает destroy экземпляра, но остаётся платным и привязан к физической машине — это не offsite backup. Размер container allocation фиксируется при создании. Перед destroy требуется проверенная выгрузка результатов [S137, S138].

**F113.** On-demand имеет фиксированные условия данного контракта и высокий приоритет, однако не иммунитет от отказа хоста. Interruptible уступает on-demand/более высокой ставке и требует checkpoint/resume. По завершении max duration экземпляр останавливается; текущая документация допускает удаление expired через 48 часов, не гарантирует 48-часовой safe backup window. Reserved credits привязаны к instance/host; ранняя отмена включает clawback скидки и 5% fee по разделу Refunds. Скидка «до 50%» — предел маркетингового описания, не применённая к нашим офферам скидка [S136, S142].

**F113. Существенные расхождения, не скрывать:**

- Current Billing, Pricing, строки 195–196: storage начисляется в online-состояниях, **offline исключён**. Legacy `console.vast.ai/faq/`, Billing → How does pricing work?, прямо включает offline/broken. Для планирования использовать консервативный резерв storage до destroy; актуальное исключение offline не является способом гарантированно уменьшить бюджет [S134, S143].
- Current Billing → Loading, строки 339–341 говорит об отсутствии charge; общий Pricing там же описывает storage во всех online states. Managing Instances также говорит «not charged during loading». Поэтому не утверждаю точную state-by-state бесплатность storage/bandwidth loading без сверки Charges; до покупки запросить уточнение [S134, S137].
- Security FAQ описывает ISO 27001 и Tier 3/4; Find & Rent → Machine Tiers — TIER 2/3 **или** ISO 27001. Нельзя превращать общий secure badge в подтверждение конкретного стандарта конкретной площадки [S135, S140].
- Billing Refunds сначала допускает возврат unspent credits «в большинстве случаев», далее отдельно исключает crypto; решение о возврате не закладывать в budget как гарантированное [S134].


## F114 — W1-12: Community / verified / secure и доступ без аккаунта

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Community / verified / secure и доступ без аккаунта»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S135, S137, S140, S141, S144.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


Unverified не прошёл внутреннее тестирование; verified прошёл тесты Vast. Это классификация машины, не независимый SLA и не право передавать любые промышленные видео. Community-среда может принадлежать частному хосту. Secure Cloud означает проверенный datacenter и отдельный фильтр; точное подтверждение сертификата/региональной политики нужно по выбранной площадке. Docker isolation защищает от соседних клиентов, но документация признаёт технический доступ владельца машины к файлам. Для данных с ограничениями нужен отдельный ответ владельца данных; бюджетный community training допустим только с разрешёнными материалами [S135, S137, S140].

**F114.** Без аккаунта реально проверены документация, официальный CLI source, описанный GET offers. Поисковик показывал индексированные карточки cloud.vast.ai, однако прямое открытие выдачи через web либо возвращало пустой JS-shell, либо ошибку доступа инструмента. Эти индексированные цены не использованы как live-offer. Документированный API пример содержит Bearer token, но наш GET оказался публично доступен; это наблюдение, не обещание бессрочного anonymous API. Аккаунтные Balance, Charges, Invoice, финальные условия оплаты и реальная возможность rent не проверялись. Отдельного auth gate для offers в нашем опыте нет; для остального не выдаём отсутствие проверки за отказ авторизации [S141, S144].


## F115 — W1-12: Практическая таблица проверки оффера перед разрешением расходов

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Практическая таблица проверки оффера перед разрешением расходов»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


Ниже — собственный протокол команды; численные hardware-пороги кроме выбранной GPU и памяти должны выйти из smoke-test, а не быть выдуманы из названия модели.

| Проверка | Записать | Reject / вопрос до покупки |
|---|---|---|
| Идентичность | UTC+МСК, URL/query, offer ID, machine ID, host ID, rental type | Нет повторно полученного актуального ответа |
| Доступность | rentable/rented, end_date, duration | Не хватает времени на загрузку, обучение, backup и восстановление |
| GPU | 1/2× RTX 3090; per-GPU 24576 MiB, power, driver/CUDA | Конфигурация не совместима с pinned framework/image; VRAM-fit неизвестен до smoke-test |
| CPU/RAM/disk | Effective CPU, allocated RAM, D, disk BW, free allocation | Размер не вмещает measured manifest+cache+checkpoints; опора на burst |
| 2 GPU | PCIe/NVLink, DDP recipe, per-device batch | Нет измеримого преимущества для time-to-result / полезного независимого эксперимента |
| Reliability | Значение и дата, verified, secure badge, outage history если доступна | Считать score вероятностью успеха данного run нельзя |
| Сеть | Up/down speeds, обе ставки с единицами, схема backup | Утечка видео/секретов; непосильный worst-case transfer cost |
| Цена | G, Srun, Sstop, D, bandwidth, taxes/FX отдельно | Неясен stopped rate; стоимость записана только как headline $/h |
| Восстановление | Resume checkpoint, RNG/optimizer/scheduler, offsite hash | Результат существует только на одном диске хоста |
| Завершение | Выгрузка, hash, archive, destroy instance и проверка volumes | Stop ошибочно принят за конец расходов |
| Платёжная граница | Утверждённый лимит, владелец, balance/autobilling | Нет отдельного разрешения расходов — ничего не арендовать |

### Шаблон фиксации будущего выбора

```text
observed_at_utc / observed_at_msk:
query + raw_response_file + HTTP Date:
offer_id / machine_id / host_id / country / rental_type:
GPU count / per-GPU VRAM / power / driver / CUDA / image digest:
effective CPU / allocated RAM / allocated disk D / disk BW / PCIe / NVLink:
verified / secure evidence / reliability / end_date:
compute whole-offer $/h / storage running $/h / stopped $/h:
ingress $/TB / egress $/TB / unit conversion:
planned running/stopped hours / measured bytes in/out / backup copies:
volumes / external costs / FX/tax unknowns / total range:
spend authorization owner + limit (currently NONE):
checkpoint location + hash / planned destroy deadline:
```


## F116 — W1-12: Предлагаемый различающий эксперимент (не выполнен)

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Предлагаемый различающий эксперимент (не выполнен)»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


Вопрос: оправдывает ли 2×3090 доплату по отношению к 1× для выбранного CV-training recipe, и безопасен ли resume? Предпосылки: отдельное разрешение аренды/лимит, разрешённые данные, pinned image digest и code commit, dataset manifest, training owner, внешний backup. **В этой работе только публичные read-only проверки; эксперимент не запускается.**

Входы: одинаковый model/checkpoint, train split и validation, preprocessing, seed, сопоставимый budget оптимизационных шагов; 1-GPU baseline и корректная DDP-конфигурация 2-GPU. Сначала короткий representative batch/epoch smoke-test: VRAM peak, CPU/RAM, GPU utilization, data wait, samples/s, checkpoint save/load, bytes transfers. После сохранения проверить восстановление состояния, hashes, отсутствие повторной загрузки всего датасета. Оценить `cost per completed comparable run` и time-to-result по фактическому ledger; отдельно влияние batch/world-size на convergence, не путать throughput с accuracy.

Метрики/артефакты: elapsed/setup/training/backup time, peak memory, utilization trace, failures/retries, validation metric, exact steps/examples processed, manifest, configs, logs, checkpoint hashes, счета compute/disk/bandwidth, offer snapshots. Success: воспроизводимый run и resume с согласованной стоимостью; затем выбрать 1 GPU, 2 GPU для DDP либо две независимые задачи по наблюдениям. Failure: OOM, dataloader starvation, плохое масштабирование, budget overrun, нестабильный host, несовместимый driver — изменить recipe/offer и повторно оценить, а не объявлять модель непригодной.

Успех не докажет качество на других камерах, готовность industrial deployment или скорость LinQ. Lockbox не загружается для подбора batch/threshold/checkpoint; train/validation/optional SELECT/lockbox разделяются по сценам/камерам/соседним кадрам согласно общему протоколу. GPU benchmark использует train-only/синтетические репрезентативные формы, не lockbox. При выборе победителя по validation многократные попытки фиксируются.


## F117 — W1-12: Передача и открытые вопросы

- Происхождение/locator: [W1-12](_WORK/W1_12.md), раздел «Передача и открытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.


- Training strategy: сформировать размер D из реальных manifests/cache/checkpoint policy; определить, нужен DDP или независимые runs. Hardware minima, VRAM-fit и длительность пока неизвестны.
- Dataset/privacy owner: разрешение на перенос промышленных видео/лиц на конкретный host/регион; public marketplace не решает права/конфиденциальность.
- Evaluation owner: удержать independence splits; определить cost-to-validation-target без использования lockbox для выбора.
- LinQ/export owner: CUDA training artifact → поддерживаемый формат/операторы/quantization и **реальный** CPU/TPU latency benchmark. Конфигурация LinQ неизвестна.
- Финансовому владельцу: перед отдельным разрешением оплаты сверить stopped storage, loading metering, TB divisor, конкретные secure credentials, taxes/FX и account autobilling. Неизвестные не заполнены вымышленными числами. Офферы необходимо перечитать непосредственно перед решением.


## F118 — W1-13: Решение

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Решение»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


**Единица воспроизводимости — immutable training bundle, а не название Vast template.** Рекомендую собственный образ с закреплённым digest, training code commit и полностью разрешёнными зависимостями; данные и outputs отдельно от образа, внешний проверяемый backup отдельно от Vast host. `last.pt` для recovery и `best.pt` для inference — разные роли. Минимального каталога файлов с manifest достаточно; MLflow/DVC/W&B не являются обязательным условием для пяти человек [F118–F08].

Уже найдена конкретная основа: `pytorch/pytorch:2.14.1-cuda12.6-cudnn9-runtime` для `linux/amd64`, digest **`sha256:1262abc856a428933c0477b4be87079173a0b087b7691c47fcb396b7b5775c56`**. Это реально полученная metadata, **не проверка содержимого или совместимости с trainer**. Использовать как candidate base; итоговый derived image также закрепить собственным digest после разрешения полного lock и smoke-test. Без этого называть рецепт полностью собранным/pinned неверно. Точные model weights/data и их лицензии выбирают соответствующие владельцы; незаполненный provenance блокирует production run [F118, F05].

Не обещать exact continuation штатного Ultralytics resume: проверенный trainer сохраняет EMA, а не online model; финальная обработка модифицирует last/best. Восстановление «продолжает обучение» и побитовое совпадение с непрерванным run — разные требования. Для первого Vast теста проверять epoch-boundary recovery; строгий replay требует дополнительного кода и отдельного доказательства [F118].


## F119 — W1-13: Наблюдения и версии

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Наблюдения и версии»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S146, S147, S148, S149, S150, S151, S152, S153, S154, S155, S156, S157, S158, S159, S162.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


**F118. Окружение можно зафиксировать, но latest/automatic недостаточны.** Public Docker Hub API вернул runtime и devel варианты PyTorch 2.14.1, CUDA 12.6/13.0/13.2. Выбранный выше runtime имеет `os=linux`, `architecture=amd64`, `last_pushed=2026-09-30T19:52:35.410847622Z`. Raw metadata — [docker_tags.json](_WORK/W1_13_MATERIALS/docker_tags.json). При данном исследовании layers не скачивались. Tag может измениться, digest фиксирует конкретный image. Сопоставление image с исходным Dockerfile не является доказанным воспроизведением upstream build.

GitHub API подтвердил PyTorch **v2.14.1**, release `2026-09-30T19:14:48Z`, commit `5c4886908584029761b579af026dcfb627c84070`; torchvision **v0.29.1**, release `2026-09-30T19:42:48Z`, commit `1f1a920d685d46dfbe187934b785b7ecb7a182f2`. Vision release явно сообщает совместимость с 2.14.1. Закреплённый PyTorch Dockerfile использует Python 3.12 paths и default Ubuntu 24.04, но фактический Python micro-version/OS image выбранного registry digest надо снять при запуске: не подменять этим выводом runtime inventory. Файлы releases/tag API и Dockerfile лежат в [materials](_WORK/W1_13_MATERIALS/).

**Негативное evidence:** live `previous-versions` при открытии показывала верхней версией 2.6.0, тогда как официальные release API и Docker Hub уже содержат 2.14.1. Поэтому её старый install command не использован как «актуальный latest». Любая команда `pip install torch torchvision` или `[Automatic]` в Vast меняет рецепт во времени [S146, S147, S148, S155].

**F119. Host driver остаётся внешней частью среды.** Контейнер не закрепляет NVIDIA host kernel driver. NVIDIA документирует CUDA 12.x minimum family >=525 и CUDA 13.x >=580, с ограничениями minor compatibility, новыми функциями/PTX. Это необходимая предварительная проверка, не достаточный acceptance test. Строка `CUDA Version` в `nvidia-smi` не является версией установленного torch runtime. Записывать driver, `torch.__version__`, `torch.version.cuda`, cuDNN, GPU model/UUID, compute capability, device count; затем реальный forward/backward выбранной модели. Для custom CUDA extensions нужен toolchain/devel recipe; runtime image не предполагается достаточным для компиляции [S149].

**F119. Vast Docker — контейнер на чужом host.** SSH/Jupyter launch mode заменяет исходный entrypoint инъекцией платформенных scripts; значит entrypoint собственного образа может не исполниться. Custom env не всегда попадает в SSH/tmux session. Не применять пример docs `env >> /etc/environment`: можно разнести секреты. В bootstrap экспортировать только явно разрешённые несекретные переменные. Disk allocation и `/dev/shm` ограничены платформой; размер container disk нельзя потом просто увеличить. CPU/RAM и shared memory зависят от доли GPU, следовательно OOM DataLoader может быть system/shared-memory, а не CUDA OOM [S150].

**F119. CLI документирован, но copy завершение нужно доказывать отдельно.** Исследован текущий `vast.py` commit **`42c3a47b44603775a5e31f54de0fce3994bd3f11`** от `2026-10-23T02:10:38Z`; latest release API — **v1.9.0**, `2026-10-20T21:31:52Z`, tag commit `28bde4827374ef658694db5a1e1e61508b966e2f`. Это разные revisions: приведённые ниже детали кода закреплены на первом SHA, не автоматически на PyPI 1.9.0. Для выполнения выбрать один CLI artifact и сохранить его hash/dependencies; production lock сейчас не создан.

В current code `copy()` поддерживает `local:path`, `C.ID:path`, legacy `ID:path`, volume/cloud locations; local transfer вызывает внешние `rsync`/`ssh` через `shell=True`. Результат `subprocess.run` записывается, но его `returncode` далее не проверяется в функции. Команда также включает `StrictHostKeyChecking=no`. Поэтому HTTP success, отсутствие Python exception и даже exit status обёртки **не доказывают backup success**; нужны destination manifest/hash и загрузка checkpoint. Не передавать недоверенные/неэкранированные пути; предпочтительны простые каталоги без shell metacharacters. Native Windows `pip install vastai` не устанавливает автоматически POSIX rsync/shell; для такого copy нужен подготовленный Linux/WSL control host либо отдельно проверенный SSH/SFTP/SCP transfer с проверкой host key. Источник: `vast.py` 1594–1707, особенно 1678–1697 [S151].

**F119. Source code license не заменяет weights/data license.** Ultralytics current SHA **`de290d865035acbfa4bb24cc88960d8b52c26e45`**, `2026-10-23T15:51:48Z`, содержит AGPL-3.0 LICENSE и `pyproject.toml` с широкими `torch>=1.8.0`, `torchvision>=0.9.0` и export extras. Установка этой ревизии без lock разрешит меняющиеся транзитивные пакеты. TorchVision отдельно предупреждает о собственных условиях pretrained weights и training datasets; `Weights.DEFAULT` может менять смысл между версиями. Полное исследование лицензий конкретных weights/data передаётся владельцам; в этой ячейке нет утверждения, что любой checkpoint разрешён. Не включать приватные кадры в публичный image/repo. Pin checkpoint URL/revision плюс SHA256 фактического файла, его model card/LICENSE и происхождение pretraining отдельно от кода [S152, S153].

**F119. venv и контейнер решают разные слои.** venv изолирует Python packages, но не OS/driver; его не надо копировать между hosts/путями. Создавать заново из lock. Внутри готового training image отдельный venv обычно избыточен; если создать обычный isolated venv поверх PyTorch image, torch base packages в нём не видны. Выбор system Python в immutable image или полный venv lock должен быть явным. `pip freeze` — inventory, а не гарантия тех же bytes и источников. Hash mode требует pinned requirements и hashes **всех** dependencies; полезен wheelhouse под конкретные Python ABI/Linux/architecture, с отдельным контролем локального training wheel [S154, S156].

**F118. Resume contract проверяется по trainer.** Ultralytics docs подтверждают `YOLO(last_path).train(resume=True)`; default checkpoint появляется на epoch boundary, т.е. прерывание до конца первого epoch ещё не даёт recovery. В pinned code `save_model()` 768–837 сохраняет `model=None`, EMA half, optimizer и metadata; `final_eval()` 1005–1014 вызывает `strip_optimizer` для last/best. Это recovery по правилам библиотеки, а не полный online training state. Минимум: отдельная recovery-копия до final_eval, never overwrite, проверка optimizer/epoch/args, parent checkpoint hash, restore test. Не утверждать, что весь optimizer FP16: детали сохраняемых FP32 состояний разобраны в W1-14. Для strict replay дополнительно нужны online weights, optimizer/scheduler/scaler, EMA отдельно, RNG всех библиотек и CUDA devices, sampler/dataloader progress и прочее состояние update loop. Штатный `seed` не сохраняет текущую позицию генераторов. PyTorch не гарантирует равенства между releases/platforms/CPU/GPU даже с тем же seed [S152, S157, S158; handoff W1-14].

**F119. Storage persistence не равна backup.** Stop сохраняет disk data, но оставляет storage billing и теряет резерв GPU. Start может неопределённо ждать GPU. Destroy удаляет container data. Local volume живёт отдельно, но привязан к физической машине, не переносится как подключаемый диск на другой host и остаётся отдельным ресурсом. В live docs написано «local volumes only», хотя CLI source уже содержит network volume commands: наличие CLI команды не доказывает доступность/семантику cross-host network storage. Базовый plan не зависит от такой функции. Cloud Sync credentials временно копируются на host с предоставленными правами; docs рекомендуют scoped credentials и Secure Cloud. Для первого опыта проще инициировать transfer с доверенной стороны, не оставляя Vast API/cloud master keys в training container [S159–S162].


## F120 — W1-13: Сравнение вариантов упаковки

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Сравнение вариантов упаковки»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S155.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


| Вариант | Когда использовать | Главный предел |
|---|---|---|
| Готовый Vast PyTorch template + provisioning script | Быстрая проверка подключения/доступности библиотек | Template ID и live script URL не фиксируют bytes; bootstrap может смениться |
| Собственный Docker image от pinned official base | Рекомендуемый training run: code+deps готовы до оплачиваемого GPU | Требуется сборка, загрузка в registry и проверка Vast launch mode; final digest пока отсутствует |
| Pinned base + venv/lock на каждом запуске | Допустимый резерв при невозможности своего registry | Больше сетевой зависимости и setup; venv надо пересоздавать, bootstrap должен быть idempotent |
| Runtime vs devel image | Runtime при wheels; devel при реальной необходимости nvcc/compiler | Больший devel image сам по себе не повышает accuracy; необходимость определяет trainer |

Обновление security patch делается новой версией bundle и сравнительным smoke-test, не скрытым `apt upgrade`/`pip -U` в продолжающемся run. Идентичный digest сохраняет старые уязвимости вместе с воспроизводимостью; это организационный tradeoff, а не обещание актуальности навсегда [S155].


## F121 — W1-13: Контракт bootstrap → run → resume → export → stop

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Контракт bootstrap → run → resume → export → stop»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S163, S164.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


Ниже **процедура для будущего выполнения после отдельного разрешения ресурсов**, не журнал выполненных операций. `DOC` означает подтверждённый интерфейс; `GATE` — обязательная проверка конкретного пакета/host; `TEAM` — предлагаемый командный контракт.

### 0. До аренды: собрать immutable bundle

1. **TEAM:** Выбрать scenario/model/weights и разрешённый train+validation dataset snapshot. Закрепить train/validation/optional SELECT/lockbox manifests; рядом сохранить labels/class mapping и group IDs camera/scene/video. Приватный lockbox не класть в training bundle. Не делать автоматический frame-level random split.
2. **DOC/TEAM:** Base — digest выше; training source — выбранный SHA (для условного Ultralytics пути выше); все дополнительные wheels и зависимости, включая exporter, фиксировать по версии и SHA256. Зафиксировать Git submodules, LFS OIDs, patch для dirty tree либо требовать clean commit. Само имя release/tarball без hash недостаточно. Зафиксировать decoder/FFmpeg/OpenCV, NumPy, augmentations и preprocessing.
3. **TEAM/GATE:** В builder/CI сформировать dependency lock и derived image; все apt/system пакеты также окажутся в final image digest. Сохранить Dockerfile, lock, build log, final image digest, installed inventory и версию Python. Не записывать придуманные hashes незагруженных weights/packages.
4. **DOC:** Для готового **полного** lock допустим интерфейс `python -m pip install --require-hashes --only-binary :all: -r requirements.lock`. Сам lock здесь не создан; для собственного source проекта собрать wheel и отдельно закрепить его hash/build dependencies. Если wheels отсутствуют, fail и выбрать явную source-build ветку, не снимать проверку молча.
5. **TEAM:** `.dockerignore`/build context исключают credentials, `.env`, `.ssh`, private media, outputs, caches. Secrets не передавать Dockerfile `ARG`/`ENV`; если private registry нужен build-time, использовать поддерживаемые BuildKit secret/SSH mounts. Public derived image допустим только без private code/data/weights, если их условия этого не разрешают [S163].

### 1. Bootstrap / connection

**DOC:** Live Vast CLI Hello World подтверждает `vastai --help`, `vastai create instance`, `show instance`, `ssh-url`, `copy`, `stop instance`, `destroy instance`; отдельная reference подтверждает `start instance`. CLI account setup/SSH public key registration выполняет уполномоченный владелец, а не исследователь; API key хранится на доверенном control host, не в образе/onstart/командном логе. SSH private key не загружается на Vast; не включать agent forwarding без отдельной необходимости.

Пример **только схемы** CLI; `OFFER_ID`, `DISK_GB`, `INSTANCE_ID` заменяются после утверждения. Не выполнять строки подряд как script. Create является платной операцией, которая в данной работе не авторизована.

```text
vastai create instance OFFER_ID --image REGISTRY/TEAM_IMAGE:IMMUTABLE_TAG --disk DISK_GB --ssh --direct --onstart bootstrap.sh
vastai show instance INSTANCE_ID --raw
vastai ssh-url INSTANCE_ID
```

`--onstart` читает локальный файл и отправляет его contents; `--onstart-cmd` — альтернативный документированный literal. `--direct` требует подходящего offer/портов, иначе выбрать подтверждённый proxy SSH mode. **GATE:** Docker сам поддерживает digest reference, current Vast CLI передаёт `--image` строку в API без собственного tag validator (`vast.py` 2516–2519), но публичная template docs описывает `repository/image:tag`. Поэтому `REGISTRY/IMAGE@sha256:…` предпочтительно проверить в разрешённом smoke-test; до такой проверки не обещать, что Vast GUI/backend его примет. Если используется tag, сохранять ожидаемый digest и проверять backend/image identity; отказ от silent fallback на `latest`.

**TEAM:** Bootstrap проверяет конфигурацию, готовит отдельные `/inputs`, `/outputs/RUN_ID`, cache; не скачивает непроверенный `main` script и не стартует автоматически новый full train при каждом reboot. Запуск через один owner/process supervisor и явный RUN_ID. Существующий RUN_ID требует ветки resume, а не `exist_ok=True` с затиранием. Bootstrap должен быть повторяемым без удаления checkpoints. SSH disconnect не должен быть механизмом остановки обучения; tmux/supervisor выбирается и pin-ится в image, exit status/logs сохраняются.

**GATE:** После `running` проверить доступность SSH, runtime imports, CUDA/torchvision ops, разрешения каталогов, free disk/inodes/RAM, `/dev/shm`, forward/backward на train-only representative batch. Снять `python -VV`, package inventory, torch/CUDA/cuDNN и `nvidia-smi` output без dump всех env. Переход в `running` не доказывает успешный bootstrap. Polling с deadline и обработкой offline/exited/unknown; endless loop недопустим. Размер диска рассчитывается из unpacked data+labels, image/cache, optimizer/recovery retention и exports, а не из числа GPU.

### 2. Input transfer и run

**DOC:** Подтверждённый current CLI interface, для подготовленного control host:

```text
vastai copy local:./inputs/ C.INSTANCE_ID:/workspace/inputs/
vastai copy C.INSTANCE_ID:/workspace/outputs/RUN_ID/ local:./archive/RUN_ID/
```

`C.INSTANCE_ID` здесь placeholder типа `C.11824`, не буквальное ID. Local-volume путь `/data` из GUI не универсален: mount point определяется actual config. Для прямого mounted volume сначала подтвердить mount, owner, capacity и filesystem; иначе сохранение в незамонтированный каталог даёт ложную persistence. Remote-to-remote transfer асинхронен; проверять destination после завершения. Никаких copy destination `/` или `/root`.

**TEAM:** Перед train проверить hashes и counts files/labels против manifest, размеры/shape samples, ordered class map и отсутствие пересечения split/group IDs. Read-only inputs; никаких встроенных auto-download/auto-split без записанного разрешения. Если trainer создаёт cache labels, cache должен содержать dataset fingerprint или пересоздаваться при изменении labels/split, иначе stale cache ломает provenance.

Условный **DOC** Python интерфейс Ultralytics (не рекомендация конкретной архитектуры и не выполненный run):

```python
from ultralytics import YOLO

model = YOLO("/workspace/inputs/init.pt")
results = model.train(
    data="/workspace/inputs/dataset.yaml",
    cfg="/workspace/inputs/train.yaml",
    project="/workspace/outputs",
    name="RUN_ID",
    device=0,
)
```

`init.pt` должен уже быть локальным, hash-verified и разрешённым checkpoint; отсутствие файла должно останавливать подготовку, а не молча загружать другой вес. `train.yaml` фиксирует epochs/steps, batch, imgsz, optimizer/LR/schedule, augmentation, workers, seed, deterministic, save/save_period, AMP и validation policy. Сохранять **effective** config после defaults/overrides, не только пользовательский YAML. Для двух GPU документирован `device=[0,1]`, но world-size/batch/LR и RNG/sampler становятся другой конфигурацией; нельзя обещать тот же trajectory или удвоение throughput. 2×24 GB не являются одной 48 GB памятью для обычного DDP.

### 3. Checkpoint и resume

**TEAM:** Запись recovery сначала в temporary file на том же filesystem, flush/fsync по возможности, затем atomic replace; checksum только завершённого immutable файла. Периодически копировать такую snapshot на доверенный storage и записывать backup receipt. Период задаётся допустимой потерей steps/time и размером checkpoint; конкретные минуты не выдуманы. Concurrent sync изменяемого `last.pt` может дать непоследовательную копию.

**DOC:** Для всё ещё пригодного recovery checkpoint Ultralytics:

```python
from ultralytics import YOLO
results = YOLO("/workspace/recovery/last.pt").train(resume=True)
```

**GATE:** До resume проверить parent hash, code/image/config/dataset/class-map fingerprints, completed epoch/global step и optimizer state. Восстановление при изменении datasets, image, world-size, LR/scheduler либо только weights — отдельный дочерний run с явно описанным warm-start, а не приписанный exact resume. В любом случае записать откуда началось фактическое продолжение. Для штатного Ultralytics сохранять recovery до финального strip, а не считать final `last.pt` достаточным. Строгий checkpoint schema для собственного trainer описан ниже; обещание stock exactness отвергнуто [F118].

Если stop был на той же машине, **DOC** `vastai start instance INSTANCE_ID`, затем status/SSH и явная resume-ветка. Если GPU недоступен/host потерян — новый отдельно разрешённый instance, тот же image/bundle и внешний backup. Volume на старой машине не является гарантированным recovery source. Переносить архив и данные, а не копировать live venv.

### 4. Export / проверка / передача LinQ

**DOC:** `YOLO("/workspace/outputs/RUN_ID/weights/best.pt").export(format="onnx")` — подтверждённый интерфейс. Это лишь минимальный пример: выпускать артефакт с плавающими defaults недопустимо. Перед реальным export зафиксировать supported target format/opset, batch/shapes, precision, NMS/raw outputs, simplify и exporter dependencies; `torch.onnx.export` 2.14 по умолчанию `dynamo=True`, `external_data=True`, старые recipes с `fallback` уже не совпадают с этим API [S164].

**TEAM/GATE:** Выделить export environment/lock отдельно, если exporter конфликтует с training dependencies. Забрать весь export directory: ONNX может ссылаться на external tensor files, одного `.onnx` недостаточно. Сохранить training best и recovery независимо; не уничтожать optimizer checkpoint ради компактного deployment. Сохранить preprocessing/postprocessing (RGB/BGR, scaling/normalization, letterbox, class order, NMS, координаты), input/output schema, golden train/validation examples+predictions и exporter log. Сравнить исходные/экспортированные outputs и task metrics на фиксированной validation части; tolerance установить до измерения.

LinQ CPU/TPU неизвестен: ONNX file не доказывает поддерживаемые operations, TPU компиляцию, размещение графа или latency. Quantization/calibration и целевой compiler — handoff владельцу LinQ; calibration берётся из разрешённого train/calibration subset, не lockbox. Эталонная GPU accuracy не переносится автоматически после quantization. Не выбирать TensorRT engine как единственный deliverable для CPU/TPU.

### 5. Завершение и billing lifecycle

1. **TEAM/GATE:** Завершить/приостановить training на подтверждённой checkpoint boundary, дождаться writer/exporter, заморозить manifest. Copy outputs на независимый destination; проверить каждый размер+hash, загрузить checkpoint в доверенном совместимом окружении и повторить один inference sample. Пока этого нет, backup отмечается `unverified`, не `complete`.
2. **DOC:** `vastai stop instance INSTANCE_ID` останавливает compute, но продолжает storage billing. **GATE:** перечитать actual state; возврат CLI не равен достигнутому stopped. Закрытие SSH, терминала или окончание train не является stop экземпляра.
3. **DOC:** `vastai destroy instance INSTANCE_ID` уничтожает container data; применять только после подтверждённого external archive и отдельной авторизации lifecycle. **GATE:** перечитать inventory/state; отдельно проверить оставшиеся volumes и их charges. Destroy instance не означает удаление самостоятельного volume и всех сторонних storage bills.
4. **TEAM:** Записать finish reason, последний step, destroyed/stopped timestamp, owner и remaining resources. Pricing/offers, stopped rate и account settings — [W1-12](_WORK/W1_12.md). Не повторять rent из retry-loop без budget/count cap и повторной проверки разрешённого лимита.


## F122 — W1-13: Минимальный registry / обязательные артефакты

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Минимальный registry / обязательные артефакты»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


Предлагаемая структура — контракт команды, **не существующие созданные training файлы**:

```text
registry/
  runs.jsonl
  RUN_ID/
    run.json
    source/commit.txt, patch.diff, submodules.txt, source.sha256
    environment/Dockerfile, image.json, requirements.lock, inventory.json
    inputs/weights.json, dataset.json, files.sha256, labels.sha256
    inputs/classes.json, dataset.yaml, train.yaml, effective_config.yaml
    inputs/train.txt, val.txt, select.txt, split_groups.json
    checkpoints/recovery_STEP.pt, best.pt, checkpoint_manifest.json
    metrics/history.jsonl, summary.json, selection_decision.json
    predictions/val_predictions.*, eval_config.json
    exports/FORMAT_VERSION/...
    logs/bootstrap.log, train.log, export.log, hardware.json
    archive/manifest.sha256, backup_receipt.json, lifecycle.json
```

`select.txt` опционален; lockbox manifest/labels/media хранятся у независимого evaluation owner и не требуются trainer. В registry допустим только fingerprint/ID lockbox без его содержания. Actual labels/dataset — в ограниченном хранилище; публичный registry содержит разрешённые hashes/metadata, не private кадры.

| Сущность | Минимально необходимые поля / почему |
|---|---|
| Run | Уникальный ID, owner, UTC timestamps, purpose, scenario, parent ID/checkpoint hash, status, seed, effective config hash, code/image/dependency/dataset/weights IDs; `planned/observed` различать |
| Environment | Final/base image digests, OS/arch, Python exact version, installed wheels hashes и pip inventory, torch/vision/CUDA/cuDNN/driver, GPU count, CPU/RAM/shm limits; inventory host отдельно от immutable image |
| Weights provenance | Original URL/repo+revision, local SHA256/size, model family/architecture version, original class mapping/preprocessing, license/model card snapshot, pretraining datasets/known contamination risks, permission status |
| Dataset provenance | Origin/version/license/permission, raw files+labels SHA256/counts, labeling schema/revision, classes ordered, camera/scene/video/time group, extraction fps/timestamps и source video hash, split manifest hash; transforms/derived data lineage |
| Recovery state | Online model (если strict), EMA отдельно, optimizer+LR scheduler+AMP scaler, epoch/global step/examples, accumulation micro-step+pending grads если checkpoint mid-update, RNG Python/NumPy/torch CPU/all CUDA, sampler epoch/order/cursor и dataloader generator, train/eval mode; собственные loss/memory-bank состояния |
| Evaluation/selection | Per-class и aggregate metrics, validation predictions scores/boxes/timestamps, evaluator version/config, IoU/conf/event/dedup rules, chosen checkpoint/threshold и источник решения. Только validation/SELECT selection; все trials сохраняются |
| Export | Parent checkpoint hash, exporter version/lock, format/opset/precision/shapes/NMS, все external files hashes, preprocessing/class schema, parity report, golden sample hashes; LinQ benchmark отдельно |
| Backup/lifecycle | Destination logical URI без signed token, immutable manifest hash, verified bytes/counts, restore test result/time, last safe checkpoint, instance/offer/machine IDs и разрешённые billing snapshots; никаких secret env dumps |

Для stock trainer сохраняется фактически доступное состояние; отсутствие RNG/online state отмечается `not_saved`, а не выдумывается полнота. Список recovery-state выше — требование строгого replay, не заявленная возможность каждого framework. Минимум для practical recovery: проверенный framework checkpoint до strip + exact bundle/inputs/effective args + документированная допустимая потеря progress. Материалы registry не должны включать untrusted Python pickle checkpoints без проверки происхождения: hash удостоверяет bytes, но не доверенность автора.


## F123 — W1-13: Различающий эксперимент — после разрешения, сейчас не выполнен

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Различающий эксперимент — после разрешения, сейчас не выполнен»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


**Вопрос:** способен ли конкретный immutable bundle на выбранном 1×3090 host пройти bootstrap → epoch checkpoint → interruption → restore → export → verified archive без скрытой смены code/data и без потери обязательных артефактов? Дополнительный вопрос strict replay — только если trainer заявляет полный state.

**Входы/ресурсы:** утверждённые лимит/owner/offer, подходящий driver+disk+RAM/shm, разрешённый representative train subset и validation subset без lockbox, выбранные weights+license/hash, built image digest, full dependency lock, control host с SSH/rsync либо проверенным transfer, независимое хранилище, доступный target CPU runtime для export parity. Время, стоимость, VRAM fit и throughput заранее не известны.

**Процедура:** (1) В чистом контейнере bootstrap и input hash checks, representative forward/backward; (2) короткий run до документированной checkpoint boundary, сохранить immutable recovery и внешний hash-verified backup; (3) завершить training process, восстановить тем же bundle, зафиксировать parent/epoch/optimizer/LR и следующие sample IDs; (4) сравнить с непрерванным контролем при одинаковом числе optimizer updates и одинаковой конфигурации; (5) export выбранного checkpoint и parity на validation; (6) выгрузить полный artifact tree и восстановить на независимом destination; (7) отдельно, при разрешении, проверить stop/start и недоступность прежнего GPU как failure mode; уничтожение source допускается только после подтверждения архива.

**Метрики:** bootstrap exit/status, фактические versions/digests, mismatch counts manifest, completed optimizer steps/examples, sample order, сохранённый/восстановленный LR/optimizer/scaler/RNG, loss/parameter deltas (если full replay заявлен), validation per-class metrics и prediction deltas, export parity, peak VRAM/system RAM, disk peak/free, setup/train/checkpoint/backup time, bytes transferred, retry/failure ledger. Равенство checkpoint file hashes после двух run не единственный критерий: serialization metadata/ordering могут отличаться; compare semantic tensors/state с заранее выбранными tolerances.

**Различающие исходы:** checksum/load failure → run не готов; stock Ultralytics продолжил с EMA, но отличается от uninterrupted → practical recovery может быть принят, exact continuation отклонён; missing optimizer/epoch после strip → checkpoint только для inference/warm-start, не recovery; exporter/ops fail → новый exporter/model target recipe, не утверждение о непригодности всех GPU; data/hash mismatch → остановка и новая версия inputs, не автоматическое продолжение. Успех подтверждает только исследованный bundle+host+subset и процедуру восстановления. Он не доказывает accuracy на других камерах, LinQ TPU compatibility/latency, privacy/security конкретного host и SLA платформы.


## F124 — W1-13: Передача W1-14 и открытые go/no-go

- Происхождение/locator: [W1-13](_WORK/W1_13.md), раздел «Передача W1-14 и открытые go/no-go»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A. W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.


- **[W1-14 reliability](_WORK/W1_14.md):** проверять copy destination даже после CLI success; current CLI не проверяет rsync returncode. Recovery snapshot до final_eval; stock EMA resume не exact continuation. Финальная соседняя ячейка прочитана: подтверждает Ultralytics 8.4.184 того же SHA, immutable snapshot через `on_model_save`, режим `native_ema`, отдельные controller/verifier и receipt. Нужно реализовать ownership writer/retention/backup и recovery drill до платного большого run; это контракт разработки, не уже реализованный hook.
- **W1-12 finance/offer:** подтвердить driver, allocated CPU/RAM/shm, disk under actual expanded bundle, network rates, loading/stopped billing и возможность прямого SSH. Public offers быстро устаревают; никаких новых цен не выдумано.
- **Model/training owner:** выбрать архитектуру и checkpoint, разрешить license/model card/pretraining provenance, собрать полный lock/final image, решить stock recovery или собственный strict checkpoint; текущая кандидатная 2.14.1 основа не прошла совместимость trainer.
- **Data/evaluation owner:** утвердить content hashes/labels/class order и group split; одинаковые камеры/сцены/соседние frames не должны создавать ложную независимость. Все selection/threshold/ensemble trials только на val/SELECT; lockbox не для настройки среды/quantization.
- **LinQ owner:** получить точные CPU/TPU/OS/compiler/runtime versions и поддерживаемый export contract; провести real parity+latency на LinQ. До этого ONNX — промежуточный кандидат, не готовый deployment.

Главные ещё не подтверждённые пункты: final derived image digest/full dependency lock; настоящий Python micro-version внутри image; приём digest reference Vast backend; конкретный model/data provenance; фактический stop/start/restore/export на разрешённом GPU и LinQ runtime. Это ограниченные проверяемые gates, не скрыто выполненные эксперименты.


## F125 — W1-14: Решение сначала

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Решение сначала»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S165, S166, S170, S172, S173, S174.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


**F125. Для 1–2 тренировочных GPU достаточно одного контроллера очереди на машине команды, одного worker на GPU/на DDP job и внешнего каталога артефактов.** Контроллер хранит manifest заданий и журнал переходов; worker запускает один дочерний training process и публикует heartbeat, завершённые snapshots и receipts. Новая платформа orchestration не обоснована. Основная защита — транзакция публикации артефактов и независимый verifier, а не наличие dashboard. Это инженерная рекомендация.

**F125. В pinned Ultralytics стандартный `resume` следует обозначать как native recovery, а не точное продолжение online-траектории.** В checkpoint `model=None`, model weights представлены half-EMA; сохраняются optimizer/scaler/epoch/EMA updates/stopper. Часть optimizer tensor states может округляться до FP16; `step`, `exp_avg`, `exp_avg_sq`, `square_avg` специально сохраняются FP32. RNG/sampler cursor и полный scheduler state в словаре `save_model` не обнаружены. `final_eval()` изменяет `last.pt`/`best.pt`, удаляя training state. Поэтому до него нужна отдельная неизменяемая recovery-копия. [S165–S166]

**F125. Диск остановленной машины — рабочая копия, не backup.** Stop сохраняет данные, destroy удаляет container storage; volumes локальны конкретной физической машине. Истечение контракта и host outage требуют внешней копии заранее. Stopped storage продолжает оплачиваться; тариф может быть выше running storage. Выбор interruptible допустим только после проверенного recovery-drill; срок возобновления после outbid не гарантирован. [S170–S172]

**F125. `exit_code=0`, существующий `best.pt`, завершившийся SSH shell или ответ API copy не означают успешное обучение.** `SUCCEEDED` выставляет контроллер только после проверки run identity, разрешённой причины остановки, final validation, содержимого checkpoint, SHA256 полученных вне хоста файлов и receipt. `TRAINED_UNARCHIVED` — отдельное состояние: при сбое выгрузки повторяется transfer, а не training. Проверка качества модели и готовность LinQ — отдельные решения.

**F125. Нужны два различных обещания восстановления.** Минимальное: native checkpoint с проверенной загрузкой и продолжением на новой попытке, возможно с изменённой траекторией. Усиленное: специально сохранённые online model + EMA + optimizer/schedulers/scaler + RNG + data ordering на согласованной границе. Даже усиленное обещание требует численного теста в закреплённой среде и не гарантирует bitwise equality между GPU, релизами и платформами. [S173–S174]


## F126 — W1-14: Проверенные recipes: что действительно находится в checkpoint

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Проверенные recipes: что действительно находится в checkpoint»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S165, S166, S167, S168, S169, S175.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Ниже номера строк **локальных raw-копий** из `W1_14_MATERIALS`; web-render может перенумеровывать строки. Все копии получены по полным commit SHA.

| Recipe | Подтверждённая семантика | Следствие для recovery |
|---|---|---|
| Ultralytics 8.4.184, SHA `de290d865035acbfa4bb24cc88960d8b52c26e45` | `trainer.py` L775–836: EMA serialization, training metadata и прямое `write_bytes` в last/best/periodic; L1071–1086 загрузка optimizer/scaler/EMA/stopper; L1128–1145 epoch resume. `torch_utils.py` L895–959 final stripping. [S165–S166] | `last.pt` во время обучения и после finalization имеют разный контракт. Snapshot immutable recovery в `on_model_save` после полного сохранения и до следующей записи. Для exact online continuation потребуется собственный adapter; sidecar без online weights этого не исправляет. |
| D-FINE, SHA `956d1709314c2c6a4df6f34de232054578a7449f` | `_solver.py` L165–183 создаёт optimizer и schedulers перед resume; L201–247 сериализует объекты с `state_dict`, включая model/EMA/scaler/optimizer/schedulers, плюс `last_epoch`; недостающие состояния могут лишь печататься. `det_solver.py` L99–105 пишет last только до `stop_epoch`; L139–170 использует stage best и внутренние перезагрузки. [S167–S168] | Не выбирать автоматически `last.pth` по имени/mtime: во второй стадии он может устареть. Требуются stage/epoch в manifest и проверка обязательных ключей. Stage-best не равно последнему recovery state. RNG/data cursor и best-selection bookkeeping дополнить либо честно принять non-exact resume. |
| RF-DETR 1.12.0.dev snapshot, SHA `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb` | `training/trainer.py` L370–403 создаёт epoch `.ckpt` и interval archives; при `checkpoint_interval=1` отдельный `last` callback не добавляется. L464–465 сохраняет CSV history. EMA callback L459–471 сохраняет average state и update step. [S169] | Брать полноценный Lightning training `.ckpt`, не inference best `.pth` по похожему названию. Проверять наличие optimizer/scheduler/EMA callback state; pin точную Lightning dependency. Документация stable показывает 2.7.0.dev, это не доказательство installed version. [S175] |

Вывод о resume не выбирает победителя detector accuracy. У D-FINE и RF-DETR более полный native training state не доказывает точную последовательность данных; это проверяется отдельно. Веса/лицензии/датасеты остаются по W1-06: здесь новые веса не выбирались и не загружались. Заголовки прочитанных исходников: Ultralytics AGPL-3.0; RF-DETR Apache-2.0. Это не полная юридическая проверка pretrained-артефактов.

В pinned RF-DETR `pyproject.toml` L7 подтверждает `1.12.0.dev`; L56 задаёт диапазон `pytorch_lightning>=2.6,<3,!=2.6.2,!=2.6.3`. Диапазон не является lock-файлом. Не брать произвольный пример с другой Lightning и не устанавливать исключённые версии; exact dependency lock и smoke остаются W1-13/training owner.


## F127 — W1-14: Минимальный контракт задания и очередь

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Минимальный контракт задания и очередь»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Предлагаемая структура на контроллере: `jobs/<job_id>/spec.json`, append-only `events.jsonl`, `attempts/<attempt_id>/status.json`, `remote-receipts/`. Один SQLite-файл с транзакциями удобен при нескольких workers; один writer и JSON достаточны для последовательного запуска. SQLite/JSON хранить на стабильном диске команды, не на исчезающем GPU-host. Не использовать сетевой файл как распределённый lock без отдельной проверки его семантики.

`job_id` определяется зафиксированной спецификацией; `attempt_id` уникален для каждого запуска. Spec содержит code SHA и dirty patch hash, image digest, lock-файл зависимостей, pretrained hash/source/license, dataset/split manifests и label map, effective train config, seed, precision, world_size, allowed resume mode, endpoint архива, expected budget/stop reason, required artifacts, временной и денежный лимиты, владельца. Данные lockbox не входят в training job.

Состояния:

```text
QUEUED → PREPARING → RUNNING → TRAINED_UNARCHIVED → VERIFYING → SUCCEEDED
                    ↘ FAILED_RETRYABLE / FAILED_CONFIG / CANCELLED
                    ↘ UNKNOWN_HOST_STATE → reconcile → RUNNING / INTERRUPTED
INTERRUPTED → CHECKPOINT_SELECTED → PREPARING (новый attempt_id)
```

Worker эксклюзивно занимает GPU UUID/набор UUID; DDP занимает обе карты как одно задание. Два независимых job нельзя случайно запустить на каждой из тех же карт одновременно. Все child ranks и dataloader workers принадлежат process group одного attempt. Контроллер различает живой worker, живой trainer и рост `optimizer_step`: heartbeat shell сам по себе не доказывает прогресс training.

Потеря SSH/heartbeat переводит попытку в UNKNOWN, а не в FAILED и не немедленно в новый запуск. Сначала проверить process identity, instance state и receipts. Истёкшая lease не доказывает смерть удалённого процесса. Для предотвращения двух publishers контроллер выдаёт increasing attempt generation; поздние receipts старой generation не могут завершить новую. Если старый worker нельзя подтвердить остановленным, новая попытка изолируется по каталогам, учитывается как потенциально дублирующая расходы, автоматический запуск приостанавливается до разрешения неопределённости. Никакой скрытой бессрочной autoretry.

Retry разрешён только при классифицированном transient failure, наличии валидного recovery checkpoint и оставшемся лимите. Backoff, число retries и maximum recovery wait задать в spec. Изменение batch/imgsz/workers/world_size/optimizer — новая конфигурация с отдельной записью, даже если framework разрешает override в resume. `parent_attempt`, исходный checkpoint SHA и число повторно обработанных шагов сохраняются.


## F128 — W1-14: Протокол checkpoint: от безопасной границы до внешней копии

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Протокол checkpoint: от безопасной границы до внешней копии»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S176, S177, S178.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Это предлагаемый adapter, его нет в виде проверенного скрипта. Начать с **epoch-boundary recovery**, поскольку это упрощает data cursor и accumulation. Если одна эпоха превышает допустимую потерю работы, выбрать step-boundary adapter и проверить его отдельно; изменение `save_period` не превращает epoch save в sub-epoch recovery.

1. Достичь согласованной границы: завершён optimizer step, EMA update, scaler update и принятый scheduler step; нет незавершённой accumulation. Для DDP согласовать все ranks и собирать rank-specific RNG/data state; один rank-0 файл без этих состояний не даёт exact DDP continuation. Signal handler только ставит флаг request checkpoint/stop. Нельзя вызывать несогласованный `torch.save` из signal handler во время collective/optimizer mutation. На SIGKILL/обрыв питания handler не поможет.
2. Зафиксировать snapshot: `schema_version`, job/attempt/generation, completed epoch/step, online model и persistent buffers, EMA и updates, optimizer с param-group order, scheduler(s), warmup, AMP scaler, early-stop/best state, RNG Python/NumPy/Torch CPU/CUDA (для каждого rank), sampler generator/epoch/ordering, dataset/config hashes. Для custom mid-epoch — cursor, consumed batches, prefetch/worker augmentation states или явно определённый replay от границы. Без контроля prefetch нельзя обещать exact continuation одними RNG seeds.
3. Snapshot должен быть независим от последующих mutable tensors: синхронное сохранение либо стабильные clones/копии. Асинхронный uploader не читает model state и не копирует перезаписываемый `last.pt` одновременно с writer. Native callback после завершения save делает уникальную копию, проверяет её и лишь затем enqueue upload.
4. Записать `checkpoint.tmp` в том же filesystem, выполнить flush + file fsync, закрыть; проверить загрузку/обязательные ключи/формы/finite tensors и лишь затем rename/`os.replace` в уникальный `recovery-step-N.pt`; на Linux выполнить fsync каталога. `os.replace` атомарен при успешном same-filesystem rename, но эта операция одна не гарантирует durability host storage. Не полагаться на rename между mount points или на object-store rename. [S176]
5. SHA256 и byte length считать **после** закрытия окончательного immutable файла; включить в `manifest.json`, отдельно hash самого manifest. В локальном каталоге checkpoint помечается READY только после выполнения пунктов 1–4. Reader игнорирует `.tmp` и неполные manifests.
6. Сначала загрузить immutable payload и manifest в `jobs/<id>/attempts/<id>/checkpoints/<step>-<hash>/`. Повторная передача по тому же содержимому идемпотентна. Использовать copy, а не destructive mirror/sync. `.partial` и незавершённые multipart uploads не считаются checkpoint. При сетевом сбое оставить local READY и предыдущую подтверждённую remote версию.
7. На стороне назначения проверить список файлов, lengths и **SHA256 прочитанных destination bytes**; затем CPU-load recovery в закреплённом loader и schema check. Для первичного smoke и финального кандидата сделать round-trip на независимую машину; `rclone check --download` полезен как проверка потока байтов, но не заменяет собственный SHA256 manifest. S3 multipart ETag не является обычным MD5 файла; отсутствие общего remote hash не разрешает size-only принять за integrity. [S177–S178]
8. Контроллер сохраняет receipt `{checkpoint_sha256, manifest_sha256, bytes, verified_at, verifier_version, destination_uri, step, generation, load_status}`. Лишь после receipt обновить указатель `latest_verified`; хранить хотя бы предыдущий проверенный recovery snapshot до проверки следующего. Best inference и final candidates защищены от retention отдельно.

Hash доказывает согласованность выбранных байтов, не корректность границы optimizer step, не истинность labels, не provenance при злоумышленной подмене и не способность продолжить обучение. Доверенные hashes должны храниться вне GPU-host. Checkpoint с pickle/object serialization загружать только из доверенного pipeline в закреплённом окружении; успешное десериализование не делает сторонний файл доверенным.

Для Ultralytics минимальный вариант не меняет trainer: immutable copy native last через `on_model_save`, включая последний epoch до `final_eval`. Этот snapshot объявить `resume_mode=native_ema`, не exact. Усиленный adapter сохраняет online state отдельно **до** приведения к half/EMA; его loader обязан восстановить online state после framework model setup и не дать native EMA initialization снова его затереть. Это небольшая, но реальная разработка с regression drill, а не готовая команда.

Важная граница YOLO: `resume_training` требует `0 < start_epoch < epochs`. Даже не stripped snapshot уже полностью завершённого расписания нельзя штатно «resume» в то же расписание. Проверка recovery должна использовать промежуточный checkpoint; сохранить также финальный full snapshot для анализа, а продолжение сверх исходного budget оформить как новый эксперимент. На случай падения final validation сохранять previous verified промежуточный state и финальные веса, не объявляя отсутствие очередной training эпохи ошибкой завершённого плана.

Для D-FINE adapter сохраняет stage-aware recovery каждый согласованный epoch, включая stage2, независимо от native `last.pth`. Внутреннюю stage refresh логику recipe не заменять автоматически. Для RF-DETR использовать full `.ckpt`; проверять конкретный actual filename и callback state, не предполагать `last.ckpt` при любом `checkpoint_interval`.


## F129 — W1-14: Cadence, RPO/RTO и стоимость

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Cadence, RPO/RTO и стоимость»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S172.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Измерить: `C_local` — пауза training на snapshot/serialize/fsync; `U` — очередь+передача+destination verify; `T` — интервал прогресса между durable local snapshots; `R` — загрузка среды+данных+checkpoint+выход на следующий optimizer step. Отдельно RPO процесса (потеря RAM при доступном диске) и RPO хоста (диск недоступен, остаётся external checkpoint).

При ограниченном `U` и регулярной cadence ориентировочная верхняя потеря внешне защищённого прогресса — `T+U`; это **не гарантия**, если upload backlog неограничен, clock/step mapping неправильны или все последние checkpoints повреждены. Мониторить реальный `current_step - latest_verified_step` и elapsed compute с последнего verified boundary; возраст checkpoint во время idle не равен потерянному compute. Условие допуска в interruptible: measured backlog не нарушает выбранный RPO, проверен restore вне исходного instance, существует budget на replay.

Для интуиции можно минимизировать `C_local/T + λ·T/2` (одинаковые единицы времени): первый член — доля checkpoint overhead, второй — expected replay при редких равномерных независимых отказах с rate λ. Получаем `T≈sqrt(2C_local/λ)`. **Это собственная простая модель, не оценка Vast failure rate и не рекомендация численного интервала**: не включает upload lag, preemption correlation, restore cost, stage lengths, deadline. При неизвестной λ выбрать cadence из допустимой потери работы и measured overhead; не выводить λ из advertised reliability score.

Планировать disk по measured sizes: dataset+cache+environment/log reserve+две подтверждённые recovery версии+новый snapshot+temporary serialization/staging+выбранные best/final. In-memory BytesIO/CPU clones тоже потребляют RAM. На границе записи может одновременно существовать больше двух копий. В `T` включать validation/save boundary, а в календарный deadline — setup, upload, verify и восстановление; train loop wall time не весь rental time.

Стоимость считать в одной единице времени по actual offer/W1-12: `H_run·(G + D·s_run) + H_stop·D·s_stop + ingress_bytes·b_in + egress_bytes·b_out + external_storage + requests + verify/download + volume_cost`. Если storage-rate уже агрегирован на весь allocation, не умножать второй раз на D. Rates, units, charged states и налоговые/FX компоненты перепроверить перед арендой. Уменьшение занятого места внутри фиксированного allocation освобождает workspace, но само не уменьшает оплачиваемый D. Источник pricing — W1-12; свои цены/сроки здесь не придуманы.

Стоимость простоя: отсутствие optimizer progress при RUNNING включает GPU+running disk; stop может снять compute charge, но оставить иной disk rate; при host offline применять текущую billing policy, а не историческую console FAQ. [S172] Потерянный результат также требует повторного setup/transfer/replay и может не уложиться в deadline. Более дешёвый interruptible имеет смысл только если фактическая полная стоимость успешно архивированного сопоставимого run лучше on-demand; этого пока не измеряли.

Конкретное расхождение: current Billing, Pricing web L195–196 / pinned raw `vast_billing.mdx` L81–85, исключает active rental и storage charge для состояния `offline`; legacy console FAQ утверждает storage независимо от offline. Для расчёта брать current policy и реальный ledger, не считать отключённую SSH-сессию состоянием billing `offline`. Нулевой баланс также не является retention policy: current docs предупреждают о риске удаления данных.

Очистка: удалять воспроизводимые cache/build/temp files по allowlist после проверки пути и отсутствии active writer; сначала самый дешёвый для восстановления cache. Не удалять единственный checkpoint, manifests, split assignments, logs ошибки и еще не подтверждённые uploads. Retention выполняется по receipt, а не по расширению/mtime. Logs ротировать с ограничением объёма и внешними порциями; ошибки/exit records сохранять. Низкий disk reserve → не начинать новый epoch; сохранить в имеющийся безопасный reserve и завершить попытку как interrupted. Не пытаться лечить ENOSPC бесконечными повторными сериализациями.


## F130 — W1-14: Строгое правило SUCCEEDED

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Строгое правило SUCCEEDED»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Контроллер применяет следующий предлагаемый predicate, а не анализирует красивую последнюю строку stdout:

```text
success = correct_attempt_and_generation
       AND training_process_exit == 0
       AND declared_stop_reason in job.allowed_success_stop_reasons
       AND observed_progress_matches_declared_budget_or_allowed_early_stop
       AND final_validation_completed_on_declared_split
       AND expected_counts_and_metric_schema_valid_and_finite
       AND candidate_checkpoint_identity_matches_validation_identity
       AND all_required_artifacts_verified_at_destination
       AND recovery_contract_verified
       AND controller_committed_SUCCESS_receipt
```

Разрешённые причины окончания заранее: например, полный budget или ранняя остановка по фиксированному validation criterion. Time cap/OOM/network loss/user cancel по умолчанию не success; если time-budget experiment специально так определён, его завершение обязано иметь checkpoint, final evaluation и declared budget accounting. Process exit 0 при нуле epochs, exception swallowed или отключённой validation gate не проходит. Accuracy ниже цели может быть **успешно выполненным отрицательным экспериментом**: execution success не равно model accepted.

Обязательные артефакты: resolved spec и hashes; pinned environment; dataset/split manifests и ontology; logs/stdout/stderr+exit/signal records; per-attempt step history и resume lineage; selected inference checkpoint и selection rule; отдельный recovery checkpoint или документированная native-recovery граница; validation predictions/metrics с количеством samples и checkpoint hash; manifest+receipt. Финальный SUCCESS JSON хранит job/attempt/generation, stop reason, effective steps/epochs, validation split hash, artifact manifest hash, recovery mode, verifier version. Он публикуется **последним контроллером**, а не worker сразу после `train()`.

Число строк metrics CSV не универсальный счётчик epochs: final eval может добавить записи, retries могут повторять epoch. Проверять framework-specific counters и event lineage. Пустые/усечённые/NaN metrics, подмена старым `best.pt`, несовпадение label map и checkpoint, validation другого attempt → reject.

Worker failure record сохранять через finally/trap, но SUCCESS из trap не писать. Лучше запускать subprocess напрямую с stdout/stderr в файлы и дождаться именно trainer PID/process group. Если используется `train | tee`, нужно проверять exit training процесса, а не только tee. Документация GNU Bash по web в этой сессии дважды timeout; данный shell-пункт — рекомендация, команды lifecycle и tested wrappers принадлежат W1-13.

Дополнение от W1-13 (handoff, здесь повторно не анализировалось): в vast.py SHA `42c3a47b44603775a5e31f54de0fce3994bd3f11`, `copy()` L1678–1697 rsync вызывается через shell, subprocess result не является доказательством успешной доставки; отключён StrictHostKeyChecking. Native Windows требует отдельно доступного транспорта/POSIX tooling. Поэтому API acceptance/CLI return недостаточен для архива; gate требует destination bytes/hash/load. Не подменять root-level transfer security предположением о надёжности CLI.


## F131 — W1-14: Мониторинг без отдельной большой платформы

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Мониторинг без отдельной большой платформы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S179, S180.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


Один JSONL heartbeat и resource sampler, читаемые контроллером; interval и deadlines задать после smoke по обычным длительностям train/validation/checkpoint phases. Логи должны включать `phase`, чтобы долгий validation/save не ошибочно признать deadlock. Clock timestamps UTC плюс monotonic durations внутри worker.

| Сигналы | Что обнаруживают и реакция |
|---|---|
| GPU UUID, driver, temperature.gpu, memory.used/total, utilization.gpu, power draw, clocks, throttle/event reasons, Xid при доступе | NVIDIA документирует selective queries, N/A и driver dependence. [S179] Sustained thermal slowdown + ухудшение steps/s → сохранить recovery и разбираться/менять host через владельца. Не назначать универсальную «опасную» температуру по названию RTX3090; использовать поддерживаемые hardware limits. Memory junction на GeForce может быть недоступна. Не менять clocks/power самовольно. |
| Torch allocated/reserved/peak, CPU RSS, free RAM, `/dev/shm`, worker deaths, exit signal | Различить CUDA OOM, host RAM OOM, shared-memory failure; `nvidia-smi memory.used` не заменяет torch allocator accounting. Сохранить traceback/config/input shape. OOM не лечить бесконечным retry той же конфигурации; меньший batch/shape — новая recipe revision. Exit137 без kernel/container evidence ещё не доказывает OOM. |
| Free bytes + free inodes, checkpoint measured size, ENOSPC/I/O errors, write/verify time | Reserve должен выдерживать следующий save/staging. Рост checkpoint latency → риск превышения cadence/deadline. Проверять реальный output mount; соседний volume не означает свободное место на root. |
| epoch, optimizer_step, samples_seen, finite loss, LR, scaler scale/skipped updates, EMA updates | Progress heartbeat от training code; NaN/Inf и пустые steps должны блокировать SUCCESS. Проверить, не был ли шаг пропущен AMP scaler; batch counter не тождествен optimizer step. |
| data wait/compute time, worker liveness, batch identifiers, decode errors, CPU/I/O wait, GPU utilization | Низкая GPU utilization может означать pipeline starvation, validation или upload, а не неисправную GPU. Нет batches при живых PID → dump stacks, loader worker logs; диагностическая попытка с workers=0, отдельно от сравниваемого run. `DataLoader.timeout>0` ограничивает ожидание batch от workers, но не является общим watchdog всех зависаний. [S180] |
| oldest upload, pending bytes, latest local/verified step, retries/errors, external verifier heartbeat | Сетевой outage не должен блокировать прежние verified artifacts. При backlog больше RPO/места приостановить новые epochs; training finished → TRAINED_UNARCHIVED. Не отмечать uploads успешными по log «started». |
| Instance state, lifetime remaining, stopped duration, balance/budget ledger и cost rate | Host offline/expiry и платный idle требуют решения контроллера. Lifetime reserve ≥ measured archive/verify/migration time плюс явно выбранный запас. Не рассчитывать на возможность рестарта после expiry. |

Минимальная read-only команда для будущего Linux worker, **здесь не выполнялась**:

```bash
nvidia-smi --query-gpu=timestamp,uuid,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw --format=csv -l 10
```

`10` секунд — пример sampling, не оптимальный интервал и не SLA; поля предварительно сверить `--help-query-gpu` установленного driver. Хранить N/A как missing, не ноль. Для поддерживаемого thermal/performance detail можно читать `nvidia-smi -q -d TEMPERATURE,PERFORMANCE`; не все поля доступны в контейнере/на GeForce. Команды stop/start/copy/remove переданы W1-13, здесь их не дублируем.


## F132 — W1-14: Предлагаемый различающий эксперимент: failure-injection drill

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Предлагаемый различающий эксперимент: failure-injection drill»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


**Вопрос:** предоставляет ли выбранный recipe обещанный recovery mode, теряется ли не больше согласованного прогресса, и отклоняет ли verifier ложное «обучение закончено»? Пререквизиты: отдельное разрешение расходов, pinned image/code/dependencies, разрешённые данные, train-only representative subset или synthetic shapes, внешнее хранилище и независимый verifier, измеренные checkpoint/disk sizes. Не использовать lockbox. GPU smoke нужен для CUDA/RNG/AMP/DDP; CPU-тест одних файлов этого не заменяет.

Порядок:

1. На одной GPU сделать короткий непрерывный reference run; сохранить step IDs/LR/optimizer moments/scaler/online+EMA hashes на общей границе. Зафиксировать deterministic режим и его ограничения. Для выбранного native recipe честно отметить ожидаемые неточности.
2. От общей границы продолжить reference на несколько заранее выбранных train steps. В другой попытке завершить process после verified boundary, загрузить **полученную вне хоста** копию в том же image и продолжить те же batches. Сравнить next input IDs/augmentations, online/EMA tensors, optimizer states, LR/scaler и losses. Допуски задать до сравнения; для exact претензии различия data ordering/online state — failure. Для native EMA recovery отличие не маскировать, оценить последующее validation отдельно.
3. Инъекции в отдельные attempts: kill во время временной записи; разрыв сети до receipt; повреждение одного байта внешнего файла; missing optimizer; stale best от другого attempt; zero-epoch exit0; train child exit nonzero при живом wrapper; validation с NaN/неверным count; disk reserve exhaustion на тестовом небольшом quota; подвисший loader. Не проводить destructive tests на единственных копиях реальных результатов.
4. Проверить переходы состояний: повреждённый snapshot не становится latest; остаётся предыдущий verified; нулевой/ошибочный job не становится SUCCEEDED; сетевой сбой после train повторяет upload; controller restart восстанавливает очередь и receipts без повторной тренировки; поздний receipt старой generation не завершает новое задание.
5. Restore на новом instance/другом диске при утрате исходного host — ключевой пункт. Проверка stop/start на том же диске недостаточна. Для 2-GPU DDP повторить лишь если этот режим выбран: восстановить rank RNG и согласованные counters; смена world_size считается изменением конфигурации.

Метрики: local/remote checkpoint cadence и lag; фактически потерянные/replayed optimizer steps и samples; serialize/upload/verify pause и bytes; restore-to-first-successful-step time; tensor max-abs/relative differences; input ordering identity; число false-success (приёмка требует ноль во всех запланированных negative cases); retries/duplication; total billed compute/storage/transfer по ledger. Артефакты: manifests, hashes, receipts, injected-fault script/config, logs, state comparisons, validation identity, actual source versions и costs.

Исходы: (A) native restore проходит, numerical equivalence не проходит — пригодно для fault-tolerant approximate experiments с маркировкой; (B) enhanced adapter подтверждает выбранную точность в закреплённой среде — можно включить соответствующий resume mode; (C) integrity/gate fails — не допускать interruptible и длинные runs до исправления; (D) upload устойчиво медленнее cadence — уменьшить частоту/размер, улучшить транспорт или ужесточить pause policy по измерениям. Успех drill не доказывает надёжность host в будущем, 24GB fit полноценного датасета, detector accuracy, independence split, экспортную совместимость или задержку LinQ.


## F133 — W1-14: Операционный чеклист

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Операционный чеклист»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


- До запуска: pin code/image/dependencies/weights hashes; проверить split/ontology; задать budget, стоп-причины, resume mode, output mount и disk/RAM reserve; проверить внешний write/read/verify путь на небольшом несекретном payload.
- После первого checkpoint: проверить optimizer/scaler/scheduler/EMA contract выбранного recipe, external hash и load, выполнить controlled resume до нескольких steps. До этого длительный/interruptible run не принят.
- Во время: следить за progress, thermal/performance, data wait, OOM, disk/inodes, upload backlog, lifetime и стоимостью idle; сохранять failure evidence; не менять recipe без записи.
- При разрыве: UNKNOWN до reconcile; выбирать latest VERIFIED compatible checkpoint по step/stage, не mtime; сохранять parent lineage; не повторять целый job ради ошибки transfer.
- При завершении: независимая final validation с identity; recovery до stripping; destination read-back/hash/load; commit SUCCESS последним. Отдельно передать candidate на LinQ parity/speed.
- До release оплачиваемого ресурса: получить receipt всех уникальных результатов и подтвердить recovery/архив; lifecycle действия и проверку отсутствия оставшихся оплачиваемых volumes выполнять по W1-13/W1-12 и авторизованному лимиту. В этой работе никаких release/destroy действий нет.


## F134 — W1-14: Противоречия, отрицательные находки и handoff

- Происхождение/locator: [W1-14](_WORK/W1_14.md), раздел «Противоречия, отрицательные находки и handoff»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.


«Checkpoint существует» конфликтует с тремя реальными случаями: YOLO final stripping, D-FINE stale stage1 last, RF-DETR отсутствие отдельного last при interval1. Поэтому универсальный путь `last.pt`/`last.pth`/`last.ckpt` без manifest отвергнут. `best` — выбор качества, recovery — последний согласованный state; нельзя менять смысл filename по удобству.

Vast pages говорят о сохранении stopped data, но это не гарантия доступности после host failure; те же docs требуют backup и предупреждают о возможном удалении expired instances. Документированные 48 часов не использовать как обещанное окно восстановления. Подтверждённого notification/grace period перед preemption в открытых здесь primary pages не найдено; проектировать на abrupt stop, без final handler.

Открытые вопросы и передачи:

- **W1-06 / training owner:** выбрать native_ema против enhanced adapter для YOLO; stage-aware D-FINE; full RF-DETR checkpoint; pin PyTorch/Lightning actual versions и провести recovery drill. Отдельно решить, насколько numerical deviation приемлема для сравнения recipes.
- **W1-13:** реализовать lifecycle и runner/transport по авторизованным лимитам; сохранить trainer exit code, process group identity, безопасное host-key поведение, detached execution и status polling. Read-only monitoring command выше передан как пример; Windows rsync caveat получен от W1-13.
- **W1-12:** точные `s_run/s_stop`, charged allocation, transfer/request costs, offline billing, expiry и idle deadline в cost ledger; платежи в этой работе не разрешены.
- **Evaluation:** final validation specification и artifact identity; не объявлять target accuracy по successful job. Split по камерам/сценам/эпизодам, без соседних кадров; retry/selection/checkpoint cadence не основание трогать lockbox. Все adaptive recipe revisions и model selections учитывать как попытки.
- **LinQ:** передать hash выбранного inference checkpoint, label map, preprocessing и validation reference; затем отдельно измерить parity и latency CPU/TPU на реальном LinQ. GPU training success ни совместимость, ни скорость финального решения не подтверждает.
- **Data/security owner:** разрешённый внешний archive endpoint, retention и права переноса видео; secrets не записывать в spec/log/manifest. Storage destination здесь не создавался и аккаунты не менялись.

До принятия протокола неизвестны реальные checkpoint sizes, pause/upload/load time, частота failures, пропускная способность/стоимость backup и пределы host telemetry. Эти неизвестные разрешаются коротким согласованным drill до дорогостоящей серии, а не вымышленной универсальной cadence или reliability probability.


## F135 — W1-15: Решение прежде деталей

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Решение прежде деталей»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S181, S184, S185, S187, S188, S189.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F135. Базовая схема — одна GPU, законченный baseline и последовательные targeted ablations по W1-11.** Вторая нужна только при двух уже готовых независимых полезных работах либо измеренной очереди оценки. Пока bottleneck — независимая разметка, ontology, исправление evaluator или LinQ-совместимость, вторая CUDA-карта не снимает ограничение. Это рекомендация по зависимостям проекта, не результат hardware benchmark.

**F135. Если две GPU доступны и разрешены, первая предпочтительная схема — два независимых jobs, а не DDP.** Примеры: две заранее зафиксированные recipes подтверждающей пары; два paired seeds; baseline и comparator, только когда comparator уже обоснован предыдущим audit. На разных hosts каждому достаточно локальной копии разрешённого immutable набора и pinned environment; синхронизации градиентов между hosts нет. На одном host обязательно измерить совместную RAM/CPU/disk нагрузку: throughput двух jobs не равен сумме изолированных по определению.

**F135. Train/eval полезен при готовом потоке checkpoints и достаточно дорогой внешней оценке; штатная validation trainer не становится асинхронной от наличия второй GPU.** Внешний worker оценивает завершённые immutable checkpoints и полную downstream-систему на DEV. Нельзя без проверки убрать встроенную validation, если от неё зависят EMA/best/early stopping/переходы фаз. CPU-метрики на сохранённых detections можно считать отдельно без второй GPU. [S185, S188, S189]

**F135. DDP занимает обе карты одним опытом, не объединяет 24+24 GB в 48 GB.** Рассматривать только для одной действительно приоритетной длинной recipe, которая помещается на каждом rank с его batch, когда measured end-to-end time-to-result лучше альтернатив и совместная загрузка ресурсов допустима. DDP сохраняет реплики; model/state sharding — другой режим и отдельная разработка, не запасной переключатель готового recipe. [S181–S184]

**F135. Два hosts сложнее двух карт одного host.** У pinned D-FINE обнаружено использование global rank как CUDA device: для двух однокарточных hosts процесс rank1 выбирает несуществующую локальную `cuda:1`. Это статический вывод по коду, не воспроизведённая авария. Автозапуск DDP Ultralytics тоже задаёт локальное число процессов, а не готовую конфигурацию двух hosts. Поэтому multi-node DDP для наших pinned recipes не считать готовым до отдельной проверки и при необходимости исправления launcher/device mapping. [S185–S187]

**F135. Решение о второй GPU принимается по календарному выигрышу полезного завершённого решения, полной цене и доступному резерву, не по `GPU utilization` или абстрактному x2.** Формальные критерии и поля измерения приведены ниже. Успех CUDA-обучения не доказывает скорость и переносимость нейросетевого inference на CPU/TPU LinQ.


## F136 — W1-15: Первичные источники и границы доказательств

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Первичные источники и границы доказательств»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S181, S182, S183, S184, S185, S186, S187, S188, S189, S190, S191, S192.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Все S ниже открыты 2026-10-23. Live pages без даты публикации так и обозначены; дата crawl не используется как дата версии. PyTorch stable в момент чтения перенаправлял на **2.14**; приведены адреса `/2.14/`, а не плавающий stable. Это версия документации, **не выбранное или установленное окружение** команды. У training repositories закреплены snapshots из W1-06; `pip install latest` не является их воспроизведением. Нумерация кода — строки открытого raw-файла, при GitHub UI возможен сдвиг; названия функций являются основным locator.

| ID | Автор, версия, URL | Locator, evidence и условия |
|---|---|---|
| **S181** | PyTorch contributors, **2.14**, [DistributedDataParallel API](https://docs.pytorch.org/docs/2.14/generated/torch.nn.parallel.DistributedDataParallel.html) | Описание и Notes/Warnings, L554–660; `no_sync`, L791–808. Синхронизация градиентов, явное распределение input, отдельный процесс/GPU, требования одинакового графа/параметров и collective order. Документированная семантика, не speedup нашей задачи. |
| **S182** | Will Constable, Wei Feng / PyTorch, [Distributed Overview](https://docs.pytorch.org/tutorials/beginner/dist_overview.html), updated **2025-07-20**, страница tutorials 2.14.0+cu130 | *Applying Parallelism To Scale Your Model*, L299–322. Разделяет replicated DDP и sharding/model parallel при нехватке памяти. Не turnkey FSDP recipe для наших detectors. |
| **S183** | PyTorch contributors, **2.14**, [torch.utils.data](https://docs.pytorch.org/docs/2.14/data.html) | *Single- and Multi-process Data Loading*, L3851–3867; *Memory Pinning*, L3889–3895; `DistributedSampler`, L4440–4482. Workers, RAM, pinned buffers; padding/drop tail и `set_epoch`. API-контракт, не оптимальное число workers. |
| **S184** | PyTorch contributors, **2.14**, [CUDA semantics](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | *Asynchronous execution*, L592–608; *Memory management*, L702–707. CUDA timers/synchronize, allocated/reserved peak, ограничения empty_cache. Не доказательство fit по одному nvidia-smi. |
| **S185** | Ultralytics contributors, SHA **de290d865035acbfa4bb24cc88960d8b52c26e45**, [engine/trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py) | `train`, `_setup_ddp`, `_build_train_pipeline`, `_do_train`, `validate`: raw L173–179,217–299,409–416,604–610,860+. Код: explicit multi-device DDP, batch/world-size, nbs-based accumulation, train/val в одном цикле; Multi-GPU AutoBatch запрещён. Это инспекция, не выполнение. |
| **S186** | Ultralytics, тот же SHA, [utils/dist.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/dist.py) | `generate_ddp_command`, raw L106–133; `generate_ddp_file`, L46–104. Автогенерация локального launcher с `--nproc_per_node` и `--master_port`; удаляет save_dir нового запуска. Не готовое multi-node orchestration. Требуются уникальные каталоги runs. |
| **S187** | D-FINE authors/Peterande, SHA **956d1709314c2c6a4df6f34de232054578a7449f**, [misc/dist_utils.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/misc/dist_utils.py) | `setup_distributed`, raw L24–59: `set_device(rank)` после `get_rank`; `warp_model`, L118–144: `device_ids=[rank]`; `warp_loader`, L150–162. Global/local rank mismatch — проверенное наличие кода, предполагаемый multi-node failure — вывод, а не наш runtime log. |
| **S188** | D-FINE, тот же SHA, [core/yaml_config.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/core/yaml_config.py), [solver/det_engine.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py) | Первый: `get_rank_batch_size`, raw L145–170: total_batch_size делится на world_size, batch_size является per-rank. Второй: `train_one_epoch`, raw L54–108, optimizer step каждый batch; `evaluate`, L135+. Два первичных файла, не демонстрация memory fit. |
| **S189** | Roboflow/RF-DETR, SHA **5b22dfc0940697ce1abdfa681a5f7392b3eddbfb**, [training/trainer.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py) | `build_trainer`, raw L687–690,758–826,855–920. DDPStrategy/find_unused_parameters; static_graph guard при accumulation; devices/num_nodes; штатная validation и standalone evaluate используют общий COCO callback. Detection accumulation передаётся Lightning; keypoint manual optimization — иной путь. Код содержит собственный L4 benchmark comment, его числа здесь не переносятся на 3090. |
| **S190** | PyTorch contributors, **2.14**, [torchrun](https://docs.pytorch.org/docs/2.14/elastic/run.html) | *Single-node multi-worker*, *Stacked single-node multi-worker*, *Fault tolerant*, L3738–3780; *Important Notices* далее. Local ranks, rendezvous endpoints, отдельные ports/job IDs и конфигурация multi-node. Generic launcher не исправляет ошибочный rank mapping trainer. |
| **S191** | PyTorch contributors, [Profiler recipe](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html), tutorials 2.14.0+cu130, live | *Using profiler to analyze execution time*, CPU/CUDA activities; scheduled profiling/trace export. Основание для диагностики по trace; overhead profiler надо отделять от основного throughput measurement. |
| **S192** | Vast.ai, [Pricing](https://docs.vast.ai/guides/instances/pricing), live, явная publication date не установлена | *How Pricing Works*, *Cost Components*, *Billing Basics*. Compute, storage и transfers отдельны; ставки рыночные. W1-12 хранит собственные read-only quotes, не полученные здесь заново и не гарантированные к будущей аренде. |

Веса не скачивались, checksum и license actual binary здесь не подтверждены. W1-02/06 передают weight provenance и ограничения; до execution сохранить checksum/точные terms конкретного initialization. Эта ветка не добавляет новых checkpoint candidates. Смена кода/weights/dependencies требует новой версии recipe и smoke, особенно для dev RF-DETR. PyTorch 2.14 docs нельзя смешивать с неподтверждённой старой установленной версией без сверки API.


## F137 — W1-15: Формальные различия четырёх схем

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Формальные различия четырёх схем»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S181, S183, S184, S185, S188, S189.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Пусть `J` — jobs с DAG-зависимостями; `T_j` — измеренное wall time полностью завершённого job, включая обязательную оценку/артефакты; `R_j` — CPU/RAM/storage/network требования; `M_j` — peak CUDA footprint при реальных worst-case train/val input. Все величины сейчас неизвестны.

| Схема | Когда допустима и что ускоряет | Что не позволяет / failure condition |
|---|---|---|
| 1 GPU, последовательные ablations | Полный B0 → audit → обоснованный B1 → confirmation. Низкая orchestration сложность; все jobs имеют валидный fit | Критический путь может не уложиться; нельзя спасать его удалением final evaluation или скрытым сокращением model-specific schedule |
| 2 независимых jobs | Нет edge зависимости между текущими jobs, разные output dirs/GPU assignments, общие версии данных/evaluator; `M_j` помещается на своей карте; суммарные `R_j` допустимы | Нельзя запускать «adaptation after audit» до audit. Если RAM/I/O contention уничтожает календарный выигрыш либо нет второго полезного ready job — вернуться к одной |
| GPU0 train, GPU1 external eval | Есть атомарно опубликованные checkpoints, внешний evaluator и DEV; внешняя оценка блокирует выбор следующей работы | Штатный train loop не меняет устройство сам. Eval lag/очередь, transfer и duplicate validation могут сделать схему дороже; нельзя использовать частично записанный checkpoint или lockbox |
| DDP, обе GPU одним job | Один приоритетный job; корректные rank/device/sampler/reduction; измеренное масштабирование end-to-end; per-rank fit | VRAM не pool; синхронизация зависит от медленного rank; multi-node network/launcher и batch semantics могут обнулить выигрыш или изменить optimization experiment |

Для двух независимых jobs A/B без shared-resource overhead идеализированная работа меняется с `T_A+T_B` на `max(T_A,T_B)`. Это **модель нижней границы**, а не обещанный wall time: прибавляются provisioning/data staging, contention, backup и ожидание инженера. Если B зависит от результата A, `T_A+T_B` остаётся зависимостью даже при второй карте. Для частично GPU-параллелизуемого workflow последовательная часть ограничивает общий speedup; грубая оценка Amdahl `1/((1-f)+f/s)` применима только после определения доли `f` и не учитывает новые overheads.

### DDP и размер batch

У обычного data parallel для полных одинаковых microbatches номинальный effective batch `B_eff = world_size × batch_per_rank × accumulation_steps`. Это счётчик samples/update, не гарантия математической эквивалентности: loss normalization, последний batch, разные число объектов на изображениях, BatchNorm, AMP, RNG и optimizer schedules имеют значение. Число actual samples/updates и LR trace хранить отдельно.

При сравнении hardware scaling сначала удержать одинаковый global effective batch, число updates/processed examples и fixed horizon/phase transitions. Если оставить прежний per-GPU batch при world_size=2, global batch растёт: это одновременно hardware и optimization change. LR linear scaling не применять автоматически. При необходимости большего global batch сделать это отдельной гипотезой качества.

В Ultralytics `batch` — total physical batch, делится на world_size; `nbs` определяет накопление и scaled decay. В D-FINE различать `total_batch_size` и per-rank `batch_size`; в прочитанном engine нет штатного accumulation цикла. В RF-DETR detection накопление передаётся Lightning. Поэтому переносить одинаковый literal `batch=...` между implementations нельзя. [S185,S188,S189]

DDP не распределяет input автоматически. Проверить train sampler, корректный epoch shuffle, повторение/padding tail и отсутствие дублирования validation image IDs в aggregate. Не усреднять per-rank AP как global AP: evaluator собирает predictions/GT и вычисляет метрику согласованно. Последовательные temporal clips сохраняют boundaries; rank shard не даёт права разорвать event sequence. Эти проверки обязательны для proposed experiment, не утверждение, что в каждом trainer есть такой defect. [S181,S183]

### Память и topology

24 GB — отдельный budget карты: параметры, optimizer/gradients, activations, AMP master/scale state, EMA, communication buffers и validation peaks проверять целиком. DDP уменьшает input batch на rank при фиксированном global batch, но оставляет replicated model/state и добавляет communication overhead. Это может помочь activation-limited run, но не доказывает fit model-state-limited run. Не считать NVLink автоматическим pooling; наличие bridge, PCIe topology/P2P и доступный interconnect конкретного offer неизвестны. FSDP/model parallel потребуют отдельной совместимости optimizer, EMA, checkpoint, export и LinQ; не включать их в исходный короткий план.

В предлагаемом smoke измерять `max_memory_allocated` и `max_memory_reserved` отдельно на каждом device, плюс device-level usage других процессов. Проверить трудные размеры/число объектов и validation, не только первый train batch. `empty_cache` не освобождает живые tensors. Измерение CUDA kernel intervals — CUDA events/синхронизация, wall time всего job — монотонный clock; синхронизация каждого шага сама меняет pipeline и должна быть отделена от обычного throughput run. [S184]

Два hosts: одинаковые code/environment/dataset hashes, но отдельные local paths допустимы; data staging завершить до начала DDP. Не читать каждую train batch через межхостовый интернет. Independent jobs пересылают только manifests/завершённые checkpoints/metrics. DDP требует достижимого rendezvous и работоспособных collectives между hosts, а не только speedtest internet download; network latency/bandwidth и stragglers измеряются на реальном collective path. Один пропавший rank влияет на весь distributed job. У разных hosts может отличаться CPU, power limit, clocks, driver: одинаковое имя GPU не делает пару однородной.


## F138 — W1-15: Расписания без вымышленных минут

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Расписания без вымышленных минут»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Используются **ворота**, не выдуманное календарное расписание. Исходный DAG W1-11: contract → smoke/LinQ compatibility → B0 → audit → targeted B1 → optional B2/challenger → frozen confirmation → final LinQ/lockbox. Поскольку case deadline по CASE_NOTES — 25.10 10:00 МСК, текущий план должен сначала зарезервировать integration/final evaluation; никакой длительности run из числа epochs не выводится.

### Одна GPU

| Окно/зависимость | GPU | CPU/люди параллельно | Условие следующего окна |
|---|---|---|---|
| Contract | Не занята обучением | Независимые splits/ontology, разрешения данных, pinned recipes, evaluator contract | Разметка и split manifest заморожены; есть согласованные quality/latency gates |
| Smoke | B0 representative train+val+save/reload | Data QA, подготовка immutable staging, LinQ gate у соседней ветки | Полный required path работоспособен; не просто successful forward |
| B0 | Полная выбранная YOLO26s recipe W1-06 с fixed schedule | Готовить evaluator/event rules и error-report pipeline; labels менять только новой dataset version | Завершённый B0 и валидный DEV audit |
| B1 | Одна targeted ablation относительно B0 | Анализ frozen B0 predictions; подготовка integration | Полный B1; принять/reject/unresolved по заранее заданным gates |
| Reserve/confirmation | Incumbent/candidate paired repeats последовательно; optional challenger только если резерв сохраняется | Сведение всех seeds и deployment packaging | Заморожен окончательный pipeline/checkpoint, принят selection rationale |
| Final | Только необходимые финальные reference predictions | LinQ full-path parity/speed и lockbox у ответственного evaluator | Артефакты и отчёт; никакой настройки по lockbox |

### Две GPU: предпочтительные независимые jobs

| Окно | GPU0 | GPU1 | Ограничение |
|---|---|---|---|
| Contract/smoke | Smoke B0 | Не заполнять спекулятивным sweep; при готовности отдельный compatibility smoke | Нельзя назвать простаивание достаточным основанием аренды |
| Первый B0 | B0 | Внешняя DEV/retention/reference evaluation прежнего immutable checkpoint, если она уже нужна; иначе свободна | B1 из audit ещё не готов; второй B0 seed допустим только при заранее выбранной confirmation цели |
| После B0 audit | Targeted B1 | Повтор incumbent с парным seed, если требуется confirmation и обе specs готовы | Разные факторы/seed changes фиксируются; не смешать screening и confirmation |
| Frozen finalists | Incumbent, seed k | Candidate, seed k | Одинаковые data/evaluator, сопоставимые full recipes; затем при наличии бюджета следующая pair |
| Завершение | Выбранная подтверждающая работа | External event/retention eval завершённых outputs или освобождение ресурса | Не превращать spare GPU в бесконечный HPO; final LinQ gate неизбежен |

Если после audit заранее существуют две независимые ablations, допустим parallel B1/B2 от **одного** immutable B0. Нельзя назвать B2 «улучшением B1», пока B1 не оценён; interaction/combined recipe — отдельный последующий run. Если разные GPU/hosts по-разному влияют на доступную batch/recipe, comparison требует контроля этого nuisance или честной маркировки product recipe comparison.

### Две GPU: pipeline train/eval

GPU0 выполняет зафиксированный train loop со своей обязательной validation. После согласованных milestones публикует checkpoint `READY`; GPU1 берёт queued checkpoint → inference на DEV/retention → downstream event metrics → публикует связанный report. CPU может одновременно считать rules/metrics на уже сохранённых predictions, не повторяя neural inference. На same host checkpoints можно передать через локальный диск; на другом — staging transfer с checksum и только затем READY. Горизонт train, best-rule и early stopping не зависят от запаздывающего worker без отдельной реализованной управляющей логики.

Условие устойчивости очереди: если checkpoint production rate `λ` и среднее полное обслуживание evaluation `E` измерены в согласованных единицах, для одного eval worker требуется `λE < 1` в длительном режиме. Это необходимая planning модель, не гарантия при bursts. Ограничить pending queue и cadence до запуска, обязательные phase/final checkpoints не терять; если evaluation отстаёт, зафиксировать lag и дождаться нужных outputs до selection. Нельзя незаметно выбирать best из только успевших оцениться checkpoints. На старте нет checkpoint stream — схема не ускоряет пустую очередь.

### Две GPU: условное DDP-окно

После отдельного smoke обе карты резервируются одному frozen job; independent queue ждёт. Только после завершения/сохранения/обязательной оценки перейти к следующему job. Для D-FINE ограничиться single-host multi-GPU до исправления global/local rank issue; для Ultralytics не считать `device=0,1` способом подключить удалённый host. Для RF-DETR зафиксировать Lightning/dependencies, explicit devices/num_nodes и smoke actual strategy; наличие параметра num_nodes — лишь интерфейс, не наша проверка сети. DDP выбирается не одновременно с изменением архитектуры, разрешения и dataset.


## F139 — W1-15: Где настоящий bottleneck

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Где настоящий bottleneck»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S183.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


Это гипотезы классификации работ, не результаты профилирования текущего проекта.

| Работа | Вероятное ограничение | Различающее наблюдение и действие |
|---|---|---|
| Annotation/ontology/independent split, adjudication событий | Люди и покрытие данных | Нет полноразмеченных independent positives/negatives — не арендовать вторую ради sweep; исправить labels/сцены |
| Decode, resize, CPU augmentations, JSON parsing, many tiny files | CPU/I/O/RAM в зависимости от implementation | Trace показывает data wait/GPU gaps, CPU saturation либо disk wait; отдельно сравнить локальный immutable cache и настройки loaders |
| Forward/backward большого detector при готовом input | Возможно GPU compute/memory | Долгие kernels при коротком data wait; протестировать fit/throughput конкретной recipe, не выводить из parameter count |
| Crops/ROI generation и video sampling | Decode+CPU либо GPU, зависит от pipeline | Измерить stages по PTS/bytes; сохранять lineage; распараллеливать подготовку до аренды без нарушения split |
| Event matching, dedup rules, error reports на сохранённых detections | Часто CPU/инженер/evaluator | Если neural outputs уже есть, второй inference job может ничего не дать; оценить CPU worker |
| Checkpoint save/load/upload, dataset staging | Storage/network | Измерить bytes и durable completion; реже обязательной cadence не сохранять ради красивого training throughput |
| LinQ conversion/parity/full-path measurement | SDK/operator support и реальный LinQ | Дополнительная RTX не заменяет целевой CPU/TPU; hardware gate у LinQ-ветки |

У DataLoader workers multiplies по числу одновременно работающих ranks/jobs; prefetch и pinned memory увеличивают pressure на host RAM/shared memory. Увеличивать `num_workers` до plateau, не применять число «на GPU» без суммарного resource budget. При shared disk оба jobs могут одновременно распаковывать/читать одни файлы; предварительная подготовка одного immutable cache и проверка concurrent performance обязательны. Pinned memory/non_blocking — проверяемая optimization, не гарантия overlap для произвольного custom batch. [S183]


## F140 — W1-15: Измеримый критерий второй GPU / второй машины

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Измеримый критерий второй GPU / второй машины»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S192.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F140. Формализованное решение команды после будущего разрешённого pilot.** Сейчас `UNKNOWN`, вторая машина не арендована и не рекомендована безусловно. Перед pilot назначить `deadline D`, денежный предел `B`, минимально полезное сокращение календаря `Δ_min`, допустимую цену дополнительного завершённого decision-changing результата `K_max`, quality/retention/latency gates и резерв интеграции `R`. Значения задаёт команда исходя из case и доступного бюджета, здесь они не вымышляются.

Для каждой схемы `m` из real pilot/baseline получить консервативный диапазон remaining makespan `T_m`, полный remaining cost `C_m` и число **admissible completed comparisons** `N_m`: завершена вся recipe, обязательные eval/backup, нет technical invalid, вопрос действительно меняет выбор. Raw trials/epochs — не `N_m`. Цена включает setup, running, сохранённый диск, ingress/egress, eval и retries; GPU-hours обеих карт суммируются. Инженерное время хранить отдельным ресурсом, не притворяться, что оно бесплатно.

Предлагаемые правила:

1. **Ready-work gate:** есть второй job на готовых разрешённых данных без зависимости от ещё не полученного результата, либо измеренный eval backlog, либо DDP single-job critical path. Нет — одна GPU.
2. **Feasibility gate:** per-GPU memory, joint RAM/CPU/I/O, valid evaluator, durable artifacts и LinQ prerequisites пройдены. Unknown не трактуется как pass.
3. **Deadline gate:** верхняя обоснованная оценка `T_2 + R ≤ D-now`; переход не съедает confirmation/final reserves. Сравнить с `T_1 + R`, а не с bare train duration.
4. **Value gate:** консервативное `T_1-T_2 ≥ Δ_min` при том же полезном результате **либо** `N_2>N_1` до deadline и дополнительные comparisons заранее признаны полезными; не награда за бесполезный sweep.
5. **Budget gate:** `C_2≤B`. Если `N_2>N_1`, проверить `(C_2-C_1)/(N_2-N_1)≤K_max`; при равных N оценивать доплату за календарный выигрыш напрямую. Если разность costs отрицательна, это лишь измеренный сценарий, не обещание экономии.
6. **Stop gate:** после первого нового representative window проверить, что предсказание сохраняется; starvation, eval lag, failures, исчезновение ready queue или новый LinQ blocker → освобождать второй ресурс по авторизованному lifecycle. В этой ветке никаких lifecycle действий не выполнено.

Для DDP дополнительно `S=T_1/T_DDP`, efficiency `S/2`, но считать их для **сопоставимого полного workload**. Для экономии compute-only при per-hour prices `p1,p2` необходимо `S>p2/p1`; это алгебра, без storage/transfer/setup недостаточная для полного решения. Из W1-12 snapshot одной и той же machine 144003: run 1 GPU `$0.241111/h`, run 2 GPU `$0.454444/h`, обе с 100 GB, следовательно price ratio ≈**1.885**. Это иллюстративный порог равной running cost для разных офферов на одном host, **не измеренный attainable speedup**, не текущая quote и не цена второй отдельной машины. Проверить оффер заново перед любой оплатой. Для двух отдельных hosts суммировать собственные compute/storage/transfer ставки; не удваивать `dph_base`, уже относящийся ко всему multi-GPU offer. [S192; F111]


## F141 — W1-15: Различающий эксперимент — пока только проект

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Различающий эксперимент — пока только проект»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S184, S191.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**Вопрос:** какая схема даёт больше валидных decision-changing результатов к deadline с известной полной стоимостью: последовательные 1-GPU jobs, independent 2-GPU jobs, train/eval или DDP одного критического job?

**Предпосылки:** отдельная авторизация ресурса/лимита; разрешённые данные; независимые manifests; frozen baseline recipe W1-06; evaluator W1-11; actual weights provenance/licenses; pinned container/dependencies; доступ к LinQ у соседней ветки. Не нужен доступ к lockbox для hardware profiling.

**Входы:** один train-only representative subset с трудными shapes/target counts и полностью замороженный DEV; одинаковый initialization и paired seeds, разрешённые варианты batch; два готовых jobs для independent ветки; fixed checkpoints/PTS для eval. Для microbenchmark допустимы synthetic inputs соответствующих shapes, но они не заменяют end-to-end loader и quality test.

**Порядок будущей процедуры:**

1. На одной GPU smoke train+loss+backward+optimizer/EMA, val, save/reload/resume; проверить mapping, shapes, AMP/NaNs, peak memory. Изолированно замерить каждый planned job и external eval. Cold staging и warm steady state хранить отдельно.
2. Получить завершённый B0 с fixed horizon и phase checkpoints, оценить реальный error gap и очередь W1-11. Только теперь выбрать полезную вторую работу; если её нет, эксперимент выбора второй GPU завершён отрицательно без concurrency.
3. При разрешённом втором ресурсе провести representative concurrent window independent jobs. На same host сравнить каждый job isolated/concurrent; на разных hosts записать hardware differences. Сохранить суммарный throughput, а также календарь завершённых обязательных evaluations и checkpoint backups.
4. Train/eval проверить на заранее выбранном потоке immutable checkpoints: equivalence external predictions/metrics встроенному evaluator в согласованном режиме (EMA vs base, preprocessing, score settings), transfer time, queue lag. Async report не управляет train loop без явной реализации.
5. DDP пробовать только если остался single-job critical path. Correct sampler/device/reduction; одинаковый B_eff и workload; actual LR/updates/sample counts. Сначала same-host; multi-node для данного D-FINE snapshot требует исправленного кода, нового SHA и отдельного correctness smoke. Не расходовать pilot на заведомо неготовый multi-node launcher.
6. После profiling выбранной схемы нужен полный сопоставимый run и DEV quality/retention comparison; throughput window не показывает convergence. По формулам выше выбрать mode, сохранить причины и ranges uncertainty.

**Метрики:** wall time от ready job до опубликованного проверенного результата; cold setup/data staging; train/eval/save/transfer intervals; examples/s и optimizer updates/s с количеством фактически обработанных данных; p50/p95 step/data wait; per-device memory peaks; CPU/RAM/disk/network traces; collective/straggler time для DDP; queue length/eval lag; completed/invalid/resource-stopped jobs; фактический ledger costs. Quality: paired event precision/recall/F1, FP/camera-hour, retention и independent-group uncertainty по протоколу соседей. LinQ latency/full-path FPS отдельно на целевом hardware. Mean GPU utilization не равен доказанному GPU-bound.

**Артефакты:** manifests и hashes, exact recipes/commits/image/dependencies, seeds/RNG, optimizer/scheduler/EMA checkpoint state, raw predictions и PTS/event outputs, profiler traces, timing logs, offer snapshot/ledger, registry lifecycle, resume verification. Profile с warmup и ограниченным collection отдельно от основного throughput, чтобы overhead не выдавался за обычное время. [S184,S191]

**Интерпретации:** independent jobs уменьшают measured critical path и проходят joint resource gate → второй GPU для независимой очереди; eval доминирует и pipeline устойчив → train/eval; только один длинный job и проверенная DDP экономит нужный календарь при admissible cost/quality → DDP; data starvation/annotation/нет очереди → одна GPU и исправление данных/CPU pipeline. OOM/NaN/broken launcher — technical invalid, не «архитектура менее точная». Broad intervals/no completed matched workload → unresolved, не победа двух GPU.

**Что успех не доказывает:** переносимость результата на другие cameras/scenes; достаточное число independent events; LinQ execution/latency; одинаковый final accuracy при другом batch; гарантированное время/цену следующего Vast host. Показатели pilot не являются SLA.


## F142 — W1-15: Один lightweight authoritative registry

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Один lightweight authoritative registry»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F142. Для 1–2 GPU достаточно одного coordinator и append-only JSONL/CSV registry плюс immutable run directories; отдельный tracking server/аккаунт не нужен.** Это предлагаемая структура, здесь каталоги/registry не создавались. Единственный writer назначает `run_id`, spec и device/host lease. Workers пишут только свои logs/artifacts и возвращают completion manifest; coordinator проверяет checksum/наличие обязательных outputs и атомарно меняет статус. Не позволять двум hosts одновременно редактировать общий JSONL по сетевому диску. UI таблица/ноутбук — производное представление, не второй источник истины.

```text
experiment_root/
  registry.jsonl                 # один writer, история всех попыток
  contracts/{split,evaluator,selection}_vN.json
  recipes/<recipe_id>/config.yaml
  runs/<run_id>/
    spec.json                   # immutable до dispatch
    environment.json
    lifecycle.jsonl             # сообщения worker; coordinator импортирует
    train_metrics.jsonl
    resource_trace.*
    checkpoints/<sha256>.*
    eval/<checkpoint_sha>/<evaluator_sha>/<split_sha>/
      predictions.*
      events.*
      metrics.json
    complete_manifest.json      # hashes обязательных outputs
    READY                       # после проверки завершённой публикации
  decisions/<decision_id>.json
```

Обязательные поля записи: `run_id`, `attempt_id`, `parent_run/checkpoint`, `hypothesis`, `decision_id`, `recipe_id/hash`, `code_sha`, `weight_origin/hash/license`, `dataset/split/ontology hashes`, `evaluator_sha`, `seed`, `precision`, `imgsz`, physical/per-rank/global batch, accumulation, actual processed examples/updates, schedule/phase state, devices/world_size/strategy, host/offer/image/dependency identifiers, timestamps UTC, costs components, metrics pointers, `selection_role`, `status`, `stop_reason`, artifacts checksums, owner. Значения unknown сохранять `null`, не заполнять нулями. Fixed spec не перезаписывается после OOM-reduced batch: изменённая recipe получает новую запись и связь с исходной.

Статусы: `PLANNED→READY_TO_RUN→RUNNING→ARTIFACT_READY→EVALUATED→COMPLETE`; отдельные `INVALID`, `RESOURCE_STOP`, `CANCELLED`. Потеря heartbeat даёт `UNKNOWN/STALE`, пока не выяснено состояние; нельзя автоматически запускать дубль и считать два completion независимыми seeds. DDP — один run с rank logs, не два независимых trials. Idempotent eval key — checkpoint+split+evaluator+pipeline hashes. `COMPLETE` означает завершён required protocol, не acceptance качества; rejected result тоже сохраняется.

Checkpoint publish: записать временный файл → закрыть/проверить checksum → атомарно переименовать на локальной FS либо закончить upload → coordinator публикует manifest/READY. Remote worker проверяет checksum после staging; не читает изменяемый `last.pt` в момент записи. Для resume сохранить полный optimizer/scheduler/EMA/RNG, а deployment-weight отдельно пометить; простая загрузка best weights не равна resume.


## F143 — W1-15: Независимость, противоречия и открытые вопросы

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Независимость, противоречия и открытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S181, S185, S186, S187, S189, S190.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


**F143. Параллелизм не увеличивает статистическую независимость данных.** Train/DEV/optional SELECT/lockbox должны отделять соседние frames, identical scenes/camera lineage по заявленной независимости; crops наследуют parent split. Paired seeds на одном split проверяют optimization variability, не camera generalization. Все попытки, включая ручные rules/threshold/checkpoint/ensemble changes, регистрируются как selection history. External GPU1 worker не получает lockbox для удобного ежедневного отчёта. Lockbox остаётся у одного evaluator, frozen final system оценивается по заранее заданному протоколу; после просмотра нельзя подбирать checkpoint/threshold и продолжать называть результат независимым.

Негативные findings/расхождения:

- Generic PyTorch поддерживает multi-node DDP [S181,S190], но pinned D-FINE использует global rank для локального device [S187]. Возможность framework не подтверждает readiness trainer; нужен patch/new SHA или single-host/independent jobs.
- Публикации/инструкции multi-GPU старого YOLOv5 не используются как инструкция текущему YOLO26 trainer. У текущего snapshot есть собственные batch/DDP/validation semantics [S185,S186].
- `2×24 GB` не означает один 48 GB адресуемый budget; переносимость FSDP/EMA/export здесь не проверена. Падение при OOM нельзя исправлять заявлением о pooling.
- Есть code comments о RF-DETR DDP измерениях на L4 [S189], но не замеры 3090 и не наше evidence выигрыша end-to-end. Не использовать чужой процент для аренды.
- Более высокая samples/s при увеличенном global batch не доказывает такой же time-to-quality; короткий smoke не заменяет полный fixed schedule, особенно freeze/unfreeze/clean late phase из W1-06/11.
- Цены W1-12 наблюдались ранее в текущем дне; это snapshot, не зарезервированные GPU. Второй ресурс не решает отсутствие разрешения на обработку видео на конкретном внешнем host.

Точные unknowns: реальные data volume/codec/decode cost и loader worker count; число готовых hypotheses; actual per-rank memory с worst-case val; CPU/RAM/storage allocation и interconnect конкретного offer; доступность одновременных GPU; времена full recipe/EMA/val/save/transfer; evaluator stage costs; разрешённый бюджет/Δ_min/K_max; точный LinQ SDK/TPU/operators и целевая latency capacity. Ни один unknown не превращён в придуманное число.


## F144 — W1-15: Передачи соседним веткам

- Происхождение/locator: [W1-15](_WORK/W1_15.md), раздел «Передачи соседним веткам»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.


- **W1-06 / W1-02:** frozen recipe IDs, exact model weights/hash/terms, accumulation/global batch interpretation, phase transitions и mandatory checkpoint set; fit/resume smoke остаётся prerequisite. Challenger не запускается ради загрузки spare GPU.
- **W1-11:** использовать её DAG и confirmation reserve; передать ready queue, practical δ/gates, число допустимых finalists, полную selection history. ASHA не включать автоматически из-за появления второй карты.
- **W1-12:** передать измеренные `T_m,C_m,N_m`, host topology/CPU/RAM/I/O и byte volumes, а не требование «две 3090». До отдельного разрешения никаких rent/start/stop/destroy. Price refresh и lifecycle — у ответственного за ресурс.
- **Evaluation/data:** authoritative split/evaluator hashes, event/retention protocol, independent-group uncertainty, closed lockbox; GPU1 external eval только DEV/разрешённый SELECT по frozen procedure.
- **LinQ/integration:** compatibility и measured full-path performance — отдельный gate. Наличие CUDA pretrained/train success либо RF-DETR XLA code не доказывает совместимость с неизвестным TPU LinQ.

Итоговое действие в текущем состоянии: подготовить immutable data/recipe/evaluator/registry contract и очередь одной GPU; вторую планировать условно по F07 после реальных разрешённых измерений. В этой работе выпущен только исследовательский документ, execution/rental решения не исполнялись.


## F145 — W1-16: Решение

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Решение»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S193, S194, S197, S199, S200, S202, S203, S204.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


**F145. Единица отбора — конкретный deployment bundle, а не семейство или CUDA checkpoint.** Минимальная идентичность: checkpoint hash + code SHA + config/class schema + фактическая inference head + exporter implementation/mode/flags + preprocessing/decoder + сериализованный граф + target compiler/runtime versions + размещение каждой runtime-сети. При изменении любого из этих полей прежний parity pass не переносится автоматически. Начать с YOLO26s W1-02, но рассматривать dense и one-to-one как разные варианты; D-FINE-M и RF-DETR-M — условные challengers после export gate. Альтернатива при лицензионном/интеграционном стопе — YOLOX-s; его переносимость также требует проверки.

**F145. Запрошенный `nms` и фактическая head различаются.** На Ultralytics `de290d…` `nms=False` запрашивает one-to-one; однако head getter способен сохранить one-to-one после fusion, удалившей one-to-many. Поэтому `nms=None` само по себе не доказывает dense output. Сохранять отдельно request, actual pre-export head и actual serialized output contract; reference должен выполнять ту же голову. [S193,S194]

**F145. RF-DETR требует явного class-slot contract и selection contract.** `labels` в ONNX — logits, не class IDs. Фоновый slot определяется training mapping; `argmax per query` из компактного примера и global query/class top-k из reference decoder — разные алгоритмы. Любая их подмена требует новой оценки, а не объяснения разницы «ошибкой TPU». [S197,S199]

**F145. Проверка состоит минимум из четырёх раздельных ворот:** PyTorch той же deployment-головы → floating ONNX с тем же входным тензором → target-converted representation → реальный LinQ с полной событийной цепочкой. ONNX checker не проверяет численный parity; ORT execution не доказывает TPU execution; компиляция и совпадение одного класса не доказывают качество детектора. [S200–S204; проект процедуры ниже]

**F145. Для каждой runtime-сети каскада требуется собственный LinQ gate.** Обязательства охватывают detector, crop classifier, temporal verifier, pose, ReID, optical-flow network, learned router, fusion model — всё, что реально делает neural inference. Редкость вызова не является исключением. CPU decode/crop/NMS/association без learned embeddings/event logic допустимы как проектное размещение; допустимость neural CPU path внутри сервера LinQ должна быть установлена у организаторов и подтверждена запуском. Внешняя CUDA inference не закрывает требование кейса.

**F145. Публичный документированный путь LinQ найден, но он исторический.** Руководство оператора **IVA H1, 2025, `RU.РМДВ.04.06.014-03 34 01`** описывает ONNX→TensorFlow→внутреннюю quantized representation→TPU program→SDK inference. Это первичное свидетельство существования пути, а не current SDK recipe для неизвестного сервера 2026. Не установлены supported opset, dtype/shape restrictions, операторное покрытие, допустимость fallback и actual SKU. Ни один из этих unknowns не заменён числом. [S202,S203]


## F146 — W1-16: Исходные требования и версии

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Исходные требования и версии»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


По переданному `_WORK/CASE_NOTES.md` root визуально прочитал официальный raster case: p5/p7 — качество, уведомление через несколько секунд и дедупликация; p13 — inference на LinQ и измерение скорости. Я PDF кейса повторно не просматривал. Устный accuracy-приоритет не задаёт формулу и не снимает latency gate. CPU+TPU — сообщение команды, точная конфигурация неизвестна.

Для согласования с W1-02 заново открыты именно эти ревизии:

| Кандидат | Code identity | Checkpoint identity на входе проверки | Что требуется дополнительно |
|---|---|---|---|
| YOLO26s | Ultralytics `8.4.184`, SHA `de290d865035acbfa4bb24cc88960d8b52c26e45` | `assets/releases/download/v8.4.0/yolo26s.pt`; W1-02 фиксирует GitHub metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b` | Проверить hash полученных байтов; custom fine-tuned checkpoint получает свой hash; package wheel и git checkout не объявлять идентичными без проверки |
| D-FINE-M | `956d1709314c2c6a4df6f34de232054578a7449f` | `dfinev1.0/dfine_m_coco.pth` из W1-02, отдельно от O365→COCO | Hash бинарника; выбран EMA/model state; full include config; custom class mapping |
| RF-DETR-M / L2026 | `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`, W1-02 package snapshot `1.12.0.dev` | `rf-detr-medium.pth` / `rf-detr-large-2026.pth` | SHA256 реальных весов и schema; Large2026 не legacy Large |
| RT-DETRv2-S / DSP, резерв совместимости | `df2a96c8c3a098567a1149bf0248da6efe6d495d` | S rerun и DSP — разные checkpoint W1-02 | Не заменять sampling флагом у обычных весов без новой оценки |
| YOLOX-s, запасной baseline | `6ddff4824372906469a7fae2dc3206c7aa4bbaee` | release `0.1.1rc0/yolox_s.pth` | Config/weights hash, явный decode flag и decoder parity |

Hash YOLO приведён как **переданное W1-02 release metadata**, не мой hash скачанного checkpoint. В этой ветке нет байтов весов. Source SHA закрепляет исходник, но не Python/Torch/ONNX/ORT/onnxslim/onnxsim dependencies. Нужны resolved lock и container digest.

Лицензионный gate наследует юридический manifest W1-02: у Ultralytics AGPL/Enterprise; RF-DETR N/S/M/L имеют Apache-designated путь, расширенные variants нельзя автоматически приравнивать; у D-FINE/RT-DETRv2/YOLOX Apache code не заменяет проверку provenance конкретных весов/данных. Перед передачей сохранить исходные license/notices, terms checkpoint/backbone/dataset и выбранный способ использования. Этот абзац — handoff, а не новая юридическая экспертиза. При неопределённой лицензии статус `unresolved`, не «разрешено».


## F147 — W1-16: Проверенные exporter-различия, влияющие на parity

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Проверенные exporter-различия, влияющие на parity»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S193, S195, S196, S197, S198, S199, S200, S201, S205, S206, S207.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


### YOLO26: отдельные варианты dense / one-to-one / embedded NMS

Прочитаны `Exporter.__call__`, `export_onnx`, `Detect.end2end`, `Detect.forward`, `Detect.postprocess` и `torch2onnx` на pinned SHA. [S193–S195]

| Поле | Контракт этой ревизии и следствие |
|---|---|
| Requested head | `nms=False` запрашивает end2end; `nms=None` обычно оставляет raw dense путь, с исключениями actual head/fusion. `nms=True` запрашивает NMS wrapper и может быть переопределён exporter. Это не флаг одинаковой семантики для всех YOLO |
| Actual head | Проверить наличие `one2one_cv2`, наличие/отсутствие `cv2`, фактическое `head.end2end`; уже fused checkpoint может иметь только one-to-one. Записать до/после export, logs и metadata |
| Dense output | В обычной Detect inference `[B,4+C,A]`: decoded box coordinates и sigmoid probabilities; это не необработанные regression logits. Обычный box mode `xywh`, если не задано иное; NMS и inverse geometry должны быть явно определены |
| One-to-one output | `[B,K,6]`, `xyxy,score,class_index`; postprocess включает top-k/gather. «Без NMS» не означает отсутствие операций выбора/декодирования |
| Serialized contract | `images`, `output0` для detection. Реальные dtype/shape/K/head inspect из artifact; строка `nms=False` не служит доказательством. Integer-valued class column в общем float tensor не превращать в quantized score |
| Export mode | Wrapper `torch2onnx` явно использует `dynamo=False`, если доступен соответствующий Torch API. Generic совет новых PyTorch docs о `dynamo=True` не является исполненным рецептом этой библиотеки |

**Предлагаемый первый опыт, не выполненная команда:** static batch1 FP32 ONNX для одного выбранного head mode, `dynamic=False`, `simplify=False` до первого parity; сохранить unsimplified graph. Если simplification полезна, создать отдельный artifact и повторить проверку. Явно передать `nms` в Python: CLI/конфигурационный parser должен сохранять различие `None`/`False`. Установить opset после получения compiler matrix LinQ, а не копировать максимум установленного ONNX. Размер 640² — baseline W1-02, не доказанный optimum для tiny PPE.

**Negative finding:** metadata/head intent полезны, но не заменяют output tensor inspection и сравнение с PyTorch после deployment transformation. Для dense/e2e нужны отдельные quality points; сравнить reference dense против exported e2e и назвать разницу «export drift» методически неверно. Для бесконечного video stream без event dedup даже one-to-one выдаёт повторяющиеся detections по кадрам.

### D-FINE: официальный exporter уже включает postprocessor

В `tools/deployment/export_onnx.py` разворачиваются `cfg.model.deploy()` и `cfg.postprocessor.deploy()`, inputs `images`/`orig_target_sizes`, outputs `labels`/`boxes`/`scores`, opset16; dummy images batch32, dynamic batch axis. EMA выбирается при его наличии. Пример inference `onnx_inf.py` делает RGB letterbox640 с нулевым padding, `ToTensor`, передаёт размер padded image как `[H,W]`, затем вычитает padding и делит boxes на ratio. [S196,S205]

Следовательно, нельзя одновременно подать реальный исходный `[H,W]` в граф, уже масштабировавший boxes на него, и ещё раз применить inverse letterbox по чужому примеру. В manifest задать **семантику** `orig_target_sizes`, не просто dtype `[1,2]`. Начальный fixed batch1 требует небольшого зафиксированного patch к авторскому exporter; opset16 — факт рецепта, не заявленная поддержка LinQ. Если split graph до postprocessor нужен для совместимости, он становится новым exporter variant с собственным comparator. Сохранять deploy state и сравнивать тот же wrapped PyTorch, а не training dict outputs.

Отдельный риск современного окружения: этот скрипт не фиксирует `dynamo`; default зависит от Torch. Не считать старый вызов с `dynamic_axes` воспроизводимым после произвольного upgrade. Получить actual export mode и env lock; выбор иной реализации занести в diff. Проверка `--check` включает structural checker, а не численное сравнение. [S196,S200,S201]

### RF-DETR: raw outputs и два разных decoder policy

Pinned `OnnxConfig` default opset17, optional dynamic batch; `_trace` явно выбирает legacy `dynamo=False`, если API предоставляет параметр. Экспорт использует подготовленный graph и его input/output names; сохранить preparation config вместе с export config. [S198]

| Поле | Что записать / проверить |
|---|---|
| Input | FP32 NCHW; input name получить из graph, авторский docs example использует `input`. RGB, /255 и ImageNet mean/std. Resize reference: bilinear half-pixel, `antialias=False`; PIL resize не автоматически эквивалентен torchvision |
| Boxes/logits | `dets` — normalized `cxcywh`; `labels` — неактивированные logits; sigmoid применяется один раз. Сопоставлять по точным names из manifest |
| Background | `background_class_id=None` для official sparse COCO; финальный slot для contiguous 0-based/active-first layouts; legacy background-first — slot0. Не выводить фон из ширины tensor или слова «fine-tuned» |
| Class mapping | Сохранить slot→dataset category ID→project class; holes/foreground masks и порядок после исключения background. При трёх custom classes оба выходных last-dim=4: запретить silent shape guessing |
| Selection | Отдельное обязательное поле `selection_policy`: global query/class top-k reference либо per-query argmax; `num_select`, threshold/comparison direction, order selection/threshold, duplicate-class policy. Для parity использовать reference policy |
| Decoder boundary | Graph не выдаёт готовые detections. CPU decoder — отдельный versioned компонент, его runtime и box transform измеряются |

В reference helper есть fallback на shapes и даже positional order при неоднозначности. Для нашего deployment предлагается **fail closed при нарушении manifest names**, а не наследование этого fallback: после compiler rename обязательно сохранить проверенную rename table. Это инженерное ужесточение контракта, не утверждение об ошибке author code. [S197,S199]

### Резервные пути

RT-DETRv2 sampling utils действительно разделяют default `grid_sample` и `discrete` indexing, с source `FIX ME? for rectangle input`. Это конкретная проверка операционного различия, а не гарантия TPU. Для DSP сначала square input с отдельными DSP weights; возможный Gather/indexing path также передать LinQ. [S206]

YOLOX exporter default opset11, batch1, static shapes, `decode_in_inference` по умолчанию false и опциональная simplification. Поэтому output decoder обязан знать, были ли grid/stride decoding выполнены внутри. `opset11` не означает гарантированно лучший LinQ path; legacy `_export` отдельно проверяется на locked Torch. [S207]

Произвольные custom CUDA ops, TensorRT plugins, FlashAttention, custom deformable attention kernels в training dependencies не равны runtime dependency. Для каждого реально экспортированного inference path сделать operator inventory `domain::op_type/opset/attrs/dtypes/shapes`, custom domain и external library manifest. Отсутствие CUDA kernel в target окружении — blocker только если он требуется финальному neural execution, а не исключительно train-time loss/teacher. Не приписывать весь риск Transformer семейству: конкретный exported graph решает.


## F148 — W1-16: Минимальный input/output/deployment contract

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Минимальный input/output/deployment contract»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


Следующая таблица — предлагаемый **обязательный handoff**, а не найденная гарантия производителя. Пустое поле должно иметь `unknown + owner + gate`, а не молчаливый default.

| Блок | Минимальные обязательные поля | Проверка согласованности |
|---|---|---|
| Identity | Model/cascade node ID; architecture/config SHA; code SHA/package; checkpoint URL/hash; EMA vs raw weights; num_classes/head/task; notices/licenses; artifact hashes | Reload ровно этих байтов; сопоставить lineage train→deploy→export→compile |
| Environment/export | OS/Python/Torch/torchvision/ONNX/ORT/exporter/simplifier versions; dependency lock/container; exporter entrypoint+patch; explicit/effective flags; dynamo/legacy; opset imports **всех domains** и ONNX IR; external-data file list+hash | Дамп `ModelProto` и resolved env; запрещено считать `.onnx` без sidecar полным bundle |
| Head | `requested_head`, `requested_nms`, `actual_head_before_export`, `fusion_state`, `actual_serialized_head`, `graph_postprocess_boundary` | Отдельные comparator для dense/one-to-one. Проверить фактические shape/semantics и tensor values |
| Input | Exact input names, count, dtype, shape/layout, batch/time axes; fixed/dynamic bounds; value range; aux inputs и их семантика | Golden ndarray hash; shape/dtype validation; reject unknown shape/aux mismatch |
| Preprocess | Decoder/color order/range; resize kernel+coordinate transform/antialias; letterbox/stretch/crop, integer rounding/padding; normalization; source→model matrix и inverse; library versions | Один и тот же **готовый** тензор подать всем runtimes; отдельно сравнить preprocess implementations на одинаковых decoded pixels |
| Raw output | Exact names/rename table, dtype/shape/axes; box encoding/reference frame/unit; logits/probabilities/objectness semantics; class column; padding/valid-count convention | Сохранить необработанные ndarray, не только annotated JPEG; finite values и no axis swapping |
| Class/decoder | Slot/category/project mapping, background index/null, activation; objectness×class если применимо; global top-k/per-query argmax; K; confidence/IoU thresholds; class-aware/agnostic NMS; max_det/ties/threshold inclusivity | Synthetic schema tests + annotated development frames. Не применять sigmoid/NMS/grid decoding дважды |
| Temporal | Список последовательных input frames/PTS, clip length/stride/FPS contract; causal/lookahead; masks/padding; hidden state/reset/camera key; warm-up; outputs timestamp policy | Проверить пропуски/дубликаты/перестановку кадров, scene cut, reconnect, несколько камер; reset без переноса state между ними |
| Deployment | Actual LinQ SKU/CPU/TPU/RAM; Framework/Compiler/Runtime/driver/firmware versions; hardware target; compiled artifacts; per-node precision/layout; host vs accelerator placement; fallback policy+logs; model residency/scheduling | На реальном предоставленном сервере подтвердить каждый neural node и declared path; имя устройства/успешный compile недостаточны |
| Evaluation | Development fixture manifest и split provenance; reference output hashes; tolerance/budgets **до оценки**; evaluator version; frame/event metrics; target stream/crop load; latency boundaries | Lockbox закрыт до freeze. Исходный reference quality и retention оцениваются раздельно |

Для stateless frame detector `temporal.required=false`, `state=none`. Это явный факт выбранной architecture, а не разрешение игнорировать chronology событий. Для каскада crop inverse transform должен включать frame→crop→network и возвращать coordinates в систему исходного кадра; crop padding/expansion/association routing записываются. Для temporal сети tensor может быть `[B,C,T,H,W]` или другим — не навязывать универсальный layout, inspect конкретную модель.

**Минимальный machine-readable фрагмент** (шаблон, не готовый конфиг запуска; null означает незаполненное обязательство):

```yaml
contract_version: 1
candidate_id: null
source: {repo_sha: null, config_sha256: null, weights_sha256: null}
export:
  implementation: null
  environment_lock_sha256: null
  requested_flags: null
  effective_flags: null
  exporter_mode: null
  opset_imports: null
  ir_version: null
  graph_sha256: null
head:
  requested: null
  actual_before_export: null
  fusion_state: null
  actual_serialized: null
  postprocess_boundary: null
inputs: []  # name, dtype, shape, layout, semantic, value_range
outputs: [] # name, dtype, shape, semantic, coordinate_space
preprocess: {code_sha256: null, parameters: null, golden_tensor_sha256: null}
decoder:
  code_sha256: null
  background_class_id: null # отдельно background_policy_known обязателен
  background_policy_known: false
  slot_to_class: null
  selection_policy: null
  num_select: null
  nms_policy: null
temporal: {required: null, clip_policy: null, state_policy: null}
deployment:
  linq_release_identity: null
  neural_nodes: [] # для КАЖДОГО: artifact, placement, precision, parity, execution evidence
  fallback_policy: null
acceptance: {tensor_tolerances: null, quality_budgets: null, latency_budget: null}
evidence: {fixture_manifest_sha256: null, parity_report: null, device_trace: null}
status: unverified
```


## F149 — W1-16: Что именно доказывает найденная документация LinQ

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Что именно доказывает найденная документация LinQ»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S202, S203, S204.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


Свежая страница `/docs` ссылается на framework operator guide. Руководство 2025: §3.3 p11 содержит Converter; §3.4 pp11–21 показывает classification example с раздельными original/quantized/TLM/TPU проверками, p20 — program `.tpu` как границу Framework→SDK, p21 — `inference.sync`. В конце перечислены tested networks, включая `yolo5s`, а не наш YOLO26. Сохранён fresh extracted text+links+metadata в `W1_16_materials/LINQ_PRIMARY_FETCH.json`. **PDF screenshots не снимались, PDF bytes не получены**: это text evidence, не визуальная проверка. [S202,S203]

У этого пути три существенных ограничения:

1. Converter boundary может менять names/layout/representation. Его выход нужно сравнить отдельно; слово ONNX на входе не гарантирует поддержку нашего IR/opset/operator attributes.
2. В manual классификационный smoke проверяет top1, а TLM сообщает estimate. Это недостаточно для detection boxes/rare-class/event parity и не является измеренной LinQ latency нашего проекта.
3. Дата и код документа установлены, current paired Framework/Compiler/Runtime/driver и hardware у команды — нет. Не переносить старый `pytpu`, `TPU_128x128_PARAMS` или примеры NHWC как обязательный current API/layout. Примеры не подтверждают compatibility YOLO26/D-FINE/RF-DETR.

Публичные главная/даташит HPS заявляют PyTorch через ONNX и собственный compiler/profiler. Это vendor statements и продуктовая линейка; они не идентифицируют сервер хакатона. Datasheet HPS не является основанием назначить нашему серверу память/число concurrent models/latency/precision. [S204]

По доступному каталогу tools не найден специализированный LinQ TPU connector/tool (`linq|pytpu` по name/description дал пусто). Это наблюдение сессии, а не утверждение об отсутствии такого продукта вообще. Сходные Linq messaging/Automata SDK исключены как другие платформы. Доступ/credentials не запрашивались и сообщения производителю не отправлялись.

**Передача следующему LinQ research:** получить actual SDK bundle/container, release notes/operator matrix, accepted input formats и supported opset/IR отдельно; определить layout и required aux dtype; names mapping/scale handling; допустимые graph cuts/CPU operations; как доказать target placement/fallback; supported concurrency/state/memory; точный sample build/run. Затем проверить полученный bundle. Полное исследование PTQ/QAT/calibration algorithms/INT8 operator coverage здесь намеренно не проводится. Нужен frozen FP32 baseline и calibration manifest из development/train без lockbox; numerical precision contract следующая ветка заполняет на фактической поставке.


## F150 — W1-16: Предлагаемый дискриминирующий эксперимент E16

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Предлагаемый дискриминирующий эксперимент E16»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S195, S198, S200, S201.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


**Вопрос:** сохраняет ли конкретный export/compiler/runtime bundle полезные detections и события выбранной CUDA reference при разрешённой нагрузке и размещении всех neural nodes на LinQ? Это план; результата нет.

**Входы/ресурсы.** Зафиксированный checkpoint и разрешение на его использование; locked inference environment с достаточными CPU/RAM/storage для reference/export; реальный SDK/compiler/runtime LinQ и доступный сервер; source/config/evaluator manifests W1-02/W1-11; independently grouped development fixtures. Разрешённый CUDA device полезен для original CUDA reference и сравнения с CPU FP32, но аренда и конкретный VRAM/время здесь не назначаются. Доступ к lockbox не нужен для отладки. Определить до запуска численные tolerance/quality/latency/memory budgets совместно с владельцами метрик и организаторами; неизвестный budget не равен pass.

**Набор fixtures.** Реальные разрешённые development frames/clips: пустые кадры, tiny PPE/phone, плотные пересечения людей, края кадра, сильный letterbox/нечётные размеры, разные aspect ratios, сложные отрицательные сцены и near-threshold scores. Добавить отдельные schema fixtures для 3-class RF-DETR, background slots, reordered outputs, missing names, нулевых detections/valid count, ties top-k/NMS; synthetic schema fixtures не заменяют target quality. Для temporal/cascade — bursts нескольких людей/cameras, track interruption, холодный старт, недостающие кадры и worst-case routing. Хранить исходные PTS/monotonic timestamps и event ground truth.

**Процедура:**

1. Freeze artifact identity и budgets. Выполнить original PyTorch deployment forward `eval` с отключёнными training-only stochastic paths; сохранить actual head/fusion/config. Сопоставить CUDA reference с FP32 reference, если они разные precision, чтобы AMP drift не приписывать exporter.
2. Preprocess отдельно: одинаковые decoded RGB pixels → reference и target adapters; сохранить intermediate pixel/tensor hashes, geometry metadata. Затем **один и тот же готовый ndarray** подать reference и ONNX. Отличающийся JPEG decoder не должен маскироваться сравнением postprocessed boxes.
3. Экспортировать static batch1 floating graph; сохранить unsimplified artifact, sidecars, effective flags, log и operator inventory. Выполнить checker/full shape checks в доступном ONNX и явный ORT provider baseline. Если exporter поддерживает `verify/report`, сохранить их; у legacy wrappers выполнить свой comparator, не приписывать `verify=True` чужому entrypoint. [S195,S198,S200,S201]
4. Сравнить raw float tensors: names/shapes/dtypes, NaN/Inf, max/mean/p95 absolute error и relative error со стабилизирующим denominator. Показать distributions по каналам/классам и worst examples. Для одинакового query/anchor order сравнивать поэлементно; переставленные top-k/ties сопоставлять класс+box с фиксированным matching, отдельно сообщать selection disagreements. Не объявлять произвольное число `allclose` универсальным detector критерием.
5. Применить один versioned decoder к обоим outputs; сравнить matched IoU, center/size error в исходных pixels, score drift, per-class FN/FP, top-k/threshold/NMS boundary flips. Проверить inverse geometry. Далее считать absolute reference и candidate AP/recall и paired event recall/precision/FP per camera-hour по протоколу W1-11, включая tiny/occlusion slices. Малый tensor error не снимает event gate.
6. На предоставленном target release пройти conversion/compilation. Сохранить converter name/layout map, compiler logs, unsupported operators, replacements, target precision, host/TPU partition, artifact hashes. Если путь проходит через TF/quantized intermediate, добавить comparator на соответствующих границах. Подбор calibration/precision — работа следующего research; никакие авторские ONNX INT8 exports автоматически не считать совместимыми с LinQ.
7. Выполнить реальный LinQ inference для **каждого** neural node, скопировать outputs с корректным ownership/lifetime и сравнить с предыдущими границами. Сначала serial correctness, затем concurrency, которую допускает actual runtime. Сохранить placement evidence; внешний GPU отключён для финального inference path. Во время target tests не менять decoder/threshold для компенсации ошибок по lockbox.
8. Прогнать полную video/event цепочку под заявленным числом streams и burst crops. Раздельно измерить cold initialization, steady p50/p95/p99 neural/transfer/preprocess/postprocess/queue time, frame age, sustained throughput, drops, CPU/RAM и event-onset→alert-ready. Inference timer должен ожидать documented completion, а не только async submit. Для temporal network учитывать clip collection/lookahead, для каскада очереди и максимальное число одновременно вызываемых experts. Указать длительность измерения/число samples и policy drop/backpressure.
9. После freeze всей цепочки провести окончательную независимую оценку по lockbox у его владельца; не менять recipe по её результатам. Development parity/debug suite остаётся development и не получает название независимого теста.

**Артефакты:** bundle manifest; input pixel/tensor fixtures+hashes; raw outputs каждой границы; decoder outputs и rename map; schema failures; graph inventory/sidecars; env lock; exporter/compiler logs; per-node target execution trace; quality parity report с absolute reference metrics, class/group slices и неопределённостью; event ledger и latency/resource trace; решение pass/fail/blocked с причиной и владельцем.

**Различающие исходы:**

| Наблюдение | Решение |
|---|---|
| Floating ONNX уже расходится при идентичных ndarray | Исправлять head/export/decoder/names/geometry до LinQ tuning |
| FP32 parity есть, target conversion ломает редкие классы | Изолировать boundary, передать precision/converter defect в LinQ research; не скрывать средним AP |
| Target correctness есть, burst crops создают очередь и latency failure | Снизить scope/число neural stages или routing load и заново проверить quality+latency; не объявлять kernel FPS сквозной скоростью |
| Challenger лучше на development, но нет target neural path | Оставить offline teacher/research candidate; выбрать прошедший baseline для финального deployment |
| Bundle проходит gates и даёт meaningful gain | Продвигать именно этот immutable bundle в freeze; не весь model family |

**Чего успех не доказывает:** generalization на новые камеры/сцены, достаточность редких positive events, соответствие ещё не объявленной официальной формуле, совместимость другой head/opset/SDK release, fit любой другой LinQ SKU, SLA при иной нагрузке. Fixture parity не является statistical quality validation, compile success не является device benchmark.


## F151 — W1-16: Export-readiness и kill criteria

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Export-readiness и kill criteria»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


Разделять `blocked` (не хватает обязательного evidence) и `killed for this deployment` (проверенный провал). Блокер SDK не доказывает, что архитектура принципиально несовместима. До снятия blocker нельзя выдавать кандидата за готовый.

| Gate | Условие допуска | Kill / stop для финального кандидата |
|---|---|---|
| Provenance/license | Hash lineage, право использования/передачи, полные dependencies | Неустранимая несовместимость с выбранным способом поставки; неизвестные условия → blocked |
| Export identity | Все обязательные contract fields; actual head и graph совпадают с reference | Silent head switch/fusion mismatch, неверный schema/decoder или невоспроизводимая зависимость: stop до исправления; если не исправлено в integration window — выбрать резерв |
| Graph support | Actual LinQ release принимает конкретный graph/operators/attrs/dtypes/shapes | Unsupported required op/custom CUDA dependency без проверенного permitted replacement; timeout/compile error не назвать успехом |
| Neural placement | У каждого runtime node есть разрешённый и выполненный LinQ путь | Любая сеть остаётся на внешнем CUDA либо не проходит свой gate; редкий verifier/learned ReID также kill каскада |
| Numerical/schema | Correct named outputs, class mapping, geometry, допустимый drift на frozen suite | Перепутанные tensors/background, NaN/Inf, corrupted class IDs/coords; существенное расхождение вне заранее принятого budget |
| Task retention | Absolute quality и conversion loss по важным классам/событиям внутри budgets | Reference уже непригодна или target loss выбивает выбранный rare-class/event gate; mean retention не компенсирует это |
| Full latency/capacity | Заявленные streams/crops/temporal windows выдержаны на реальном сервере | Дедлайн alert/queue age/memory нарушается, нескончаемо растёт backlog, недопустимые drops; среднее kernel время не оправдание |
| Operational repeatability | Reload/restart/state reset и длинный поток воспроизводимы | Cross-camera hidden state contamination, невосстанавливаемые ошибки/расхождение после reload; неподтверждённый concurrency path |
| Independence | VAL/SELECT/debug/calibration отделены от lockbox по группам | Threshold/export/precision tuning по lockbox лишает его независимости; нужен новый test для последующей итерации |

Резервировать integration window — ответственность общего плана; конкретные часы/лимиты здесь не выдуманы. Если экспортируемый one-to-one не проходит TopK, проверяем dense+CPU NMS как **другой** deployment candidate, включая его accuracy/runtime. Если Transformer не проходит graph gate, совместимый detector/student или уменьшение scenario scope предпочтительнее обещания «позже портируем». Distillation — отдельный эксперимент, его успех заранее неизвестен.


## F152 — W1-16: Передачи и bounded unknowns

- Происхождение/locator: [W1-16](_WORK/W1_16.md), раздел «Передачи и bounded unknowns»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.


- **W1-02:** exact SHA/weights и две головы YOLO; сохранить request vs actual head/fusion. Вернуть выбор runtime bundle, а не общий рейтинг COCO. W1-02 фраза о quantization handoff сюда уточняется: эта ветка задаёт readiness/parity contract; полноценный LinQ quantization research остаётся следующей работой.
- **W1-03/04/05:** tiny PPE/crops/action models обязаны иметь exact preprocessing/output/temporal contract. Любые добавленные pose/ReID/flow — отдельные runtime nodes с собственным target gate. Detector COCO class не превращается в поведенческое событие без ontology/event logic.
- **W1-10:** передать полный DAG каскада: вызовы/частоты/worst-case fan-out, ordering/coordinates/selection policies. У каждого D/V/T/S_j проверить LinQ; external teacher допустим только вне финального inference.
- **W1-11/evaluation:** численные acceptance budgets и independent group manifests, matching/tie policy, rare-class quality и event latency boundary. Никакого tuning на lockbox, соседних кадрах того же события или той же камере под независимой меткой.
- **W1-15/Vast:** GPU training success не снимает target gate; второй RTX не исправляет unsupported LinQ graph. Не начинать дорогой run, если export feasibility остаётся критическим blocker, который можно проверить до обучения.
- **Следующий LinQ research / `research_link_platform`:** актуальные delivered SDK/SKU/operators/formats, precision/scales, actual layout/name mapping и размещение; manual2025 и старые pytpu только historical leads. Передать `W1_16_materials/LINQ_PRIMARY_FETCH.json` и manifest template.

Неизвестны: реальные предоставленные CPU/TPU/RAM и лимиты streams, compiler/runtime pairing, opset+IR/operator attribute support, precision и mixed host/TPU rules, разрешённость neural CPU fallback, concurrency/memory residency, actual target quality/latency. Все они влияют на финальное решение. Нет оснований обещать конкретный opset, TPU family, throughput, допустимый INT8 loss или срок портирования.


## F153 — W2-A: Решение и статус критики

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Решение и статус критики»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F153. Выбрать native_ema как дешёвое приблизительное восстановление, но любой native OOM retry, NaN epoch replay и repair/sanitize весов исключать из неизменяемого A/B trial.** Сохранять результат для диагностики либо отдельно оценённого product candidate; для продолжения создавать дочерний run с объявленной историей. Для чистой ablation перезапускать с исходного immutable initialization и новой recipe. Не строить exact-resume controller. Это предлагаемое правило, его реализация и runtime проверка ещё не выполнены.

**K001: документальная часть закрыта; runtime применимость открыта.** Исходное замечание `CRITIC.md`, K001, сохраняется: W1 пропустила внутренние изменения, exit0+CSV недостаточны. Новые факты расширяют критику: первая NaN-эпоха может продолжиться без rollback; save имеет отдельное исправление/санитизацию; callbacks с именами optimizer_step/on_before_zero_grad в stock loop не вызываются. Закрыт вопрос «какое правило принять и где наблюдать», но не доказано исполнение будущего adapter/архива на реальном host. RPO не подтверждён.

**K011: применимость уточнена, глобально остаётся открыта у сборщика.** Минимум W2-A — pinned trainer, небольшой fail guard, append-only events/progress, immutable копия native recovery snapshot до stripping, внешний bytes/hash/load receipt. Строгий replay/controller отложить. Наша ветка не выбирает за всю команду сценарий, owners и freeze times; это задача root. GPU-часы не рассчитаны.


## F154 — W2-A: Первичные свидетельства

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Первичные свидетельства»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S210, S211, S212, S213, S214, S215, S216, S217.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


L далее — **1-based строки сохранённых raw файлов**, совпадающих с pinned GitHub blob; web-парсер сжимает пустые строки. Полные полученные исходники и URL/SHA256: [materials](_WORK/W2_A_MATERIALS/sources.json). Все S — статический код/документация, политики и эксперименты — рекомендации.

| ID | Автор, версия, точный locator | Evidence/ограничение |
|---|---|---|
| S210 | Ultralytics contributors, [trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), L301–339, 450–466, 474–640, 651–685 | OOM/pipeline/warmup. SHA тот же, что W1, получен заново; код не исполнялся. |
| S211 | Тот же source, L768–837, 909–920, 1005–1022, 1071–1145 | save/repair, scaler/EMA, NaN/resume; control flow, не docstring. |
| S212 | Ultralytics, [default.yaml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml) целиком; [cfg/__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/__init__.py), get_cfg L350+, check_dict_alignment L638–685 | Stock keys и rejection неизвестных overrides; отрицательный результат только для данного SHA. |
| S213 | Ultralytics [callbacks/base.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/callbacks/base.py), L31–40,61–64,127–147; [Callbacks](https://docs.ultralytics.com/usage/callbacks), Trainer Callbacks/Forward Hooks | Pinned registry плюс live docs. Docs прямо отмечают reserved callbacks; live page не recipe pin. |
| S214 | Ultralytics [model.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py), train L807+,888; [Advanced Customization](https://docs.ultralytics.com/usage/engine), BaseTrainer/Using YOLO with Custom Trainers | Публичный subclass entrypoint; private recovery methods не стабильный API. |
| S215 | PyTorch contributors [AMP examples 2.14](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html), Gradient clipping/accumulation; [GradScaler v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/amp/grad_scaler.py), raw L364–479,486–556 | Generic skip и fused special path. Tag, не выбранная установленная dependency. GitHub API resolution SHA получила 403 rate limit; tag не выдаём за независимо проверенный SHA. Raw bytes сохранены. |
| S216 | PyTorch [step_post_hook 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.optim.Optimizer.register_step_post_hook.html), signature/description; [Adam v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/optim/adam.py), raw L104–107,810–899 | Hook означает вызов step, не гарантию applied update; fused found_inf корректирует state steps. |
| S217 | Ultralytics [torch_utils.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py), strip_optimizer L895–959; [__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py) L3 | Stripping/version; runtime artifact contents предстоит load-verify. |

**F154 — control-flow границы.** OOM retry относится к `epoch == start_epoch`, включая первую эпоху resume, только `RANK == -1`, catch вокруг forward/backward. Backend literals отдельны от case-insensitive OOM. Batch1 тоже может retry без уменьшения. NaN gate проверяет текущие loss/fitness, а не всю tensor history; start epoch возвращает False. Save ремонтирует live EMA, затем санитизирует half copy. Поэтому finite checkpoint не доказывает clean trajectory. EMA cadence не обусловлена applied optimizer update. S210/S211; реальных аварий не наблюдалось.


## F155 — W2-A: Trigger → mutation → detection → status → next action

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Trigger → mutation → detection → status → next action»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S210, S211.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Таблица — **наш контракт**, statuses не являются Ultralytics flags. Events хранить вне resettable counters trainer.

| Trigger | Mutation/locator | Detection | Allowed status | Next action |
|---|---|---|---|---|
| First-start-epoch RuntimeError: OOM либо CUBLAS_STATUS_ALLOC_FAILED, CUDNN_STATUS_INTERNAL_ERROR, unable to find an engine | Halve batch floor1; rebuild; optimizer сохранён; S210 L566–640 | Warning + _oom_retries>0 на повторном epoch start; batch diff недостаточен | FAILED_TECH для A/B; RECOVERED_NONCOMPARABLE для product | Stop до новых batches; child recipe; чистый initialization для ablation |
| Поздний OOM, RANK!=-1, четвёртый retry, OOM в val/optimizer/save | Этот recovery не применяется | Exception/exit/stderr | FAILED_TECH | Устранить причину; новая attempt/recipe |
| Поздние nonfinite loss/fitness | Last EMA→online, state restore, epoch replay; S211 L1088–1126,658–661 | Guard до handler; persistent replay event | FAILED_TECH; salvage child native_ema | Не зачислять в исходный equal-updates trial |
| Nonfinite start epoch | Native continuation без rollback | Per-batch loss guard и fitness до handler | FAILED_TECH | Fail, не ждать max retries |
| Nonfinite EMA/overflow half snapshot | Save repair/sanitize; S211 L775–795 | Pre-save online/EMA/half guard | FAILED_TECH | Finite bytes не снимают failure |
| AMP nonfinite gradients | Skip/backoff, EMA cadence продолжается | Attempts, scale trace, проверенный applied observer | CLEAN только при заранее разрешённой AMP политике, иначе INCOMPLETE_OBSERVABILITY | Не выводить updates из EMA/epochs |
| Native external resume | EMA continuation, pending gradients потеряны | Parent hash/receipt, boundary, resume_mode | Child/attempt RESUMED_APPROX | DEV evaluation; не обещать exact |
| Gap event/progress log | История неизвестна | Sequence/heartbeat/final seal | INCOMPLETE_OBSERVABILITY | Блокировать SUCCEEDED_COMPARABLE до reconcile |

OOM — не только новый batch: прежние online/optimizer/EMA изменения сохраняются, примеры повторяются. Rebuild меняет validation loader, accumulation/decay, nb/nw, scheduler cadence и mosaic gate. После успешного прохода retry counter обнуляется. NaN last может быть старше предыдущей эпохи при редком save; raw online в checkpoint отсутствует. Эти детали определяют policy, но не означают failure на наших данных.


## F156 — W2-A: Stock switches и маленький guard

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Stock switches и маленький guard»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S212, S214.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F156. В S212 нет stock fail_on_oom, disable_oom_recovery, nan_recovery=False или max_retries=0; нужных config branches нет и в trainer.** Не добавлять вымышленные flags. amp=False не отключает OOM/NaN handler; resume=False не запрещает внутреннее recovery; explicit integer batch не запрещает halving. AutoBatch setup и runtime retry — разные механизмы. save=False не является запретом NaN и final save; deterministic не даёт exact resume. DDP не использовать как способ отключить recovery.

Предлагаемый минимум — **pinned guard subclass DetectionTrainer** через документированный `model.train(trainer=...)` (S214). Не копировать loop и не реализовывать RNG/scheduler replay. Спецификация, **не готовая реализация**:

1. В `_build_train_pipeline` до super проверять `getattr(self,'_oom_retries',0)>0`, записывать fail и raise отдельное исключение. Batch assignment уже произошла, но rebuild и новые batches ещё нет. Не мутировать приватный retry counter ради отключения handler.
2. В `_handle_nan_recovery` до super проверять finite loss/fitness и fail, включая start epoch. Отдельный per-batch loss guard нужен для transient NaN, позднее перезаписанной loss. Batch-end guard срабатывает после backward/возможного step; invalid становится вся attempt.
3. В `save_model` до super проверять online/EMA и выбранную half policy. Простой строгий режим отклоняет непредставимые FP16 values; это дополнительное ограничение, не native guarantee. Guard conversion/overflow отдельно проверить drill.
4. В `on_model_save` синхронно создать immutable recovery copy до final_eval stripping, записать bytes/hash/checkpoint epoch; внешний load receipt закрывает архивирование. Mutable last.pt не архив. on_train_end для этой копии уже поздно.
5. Append-only JSONL events/progress и final seal вне CSV. Использовать add_callback, не стирать интеграционные handlers через set_callback.

Stock-only fallback без времени на guard: warnings, repeated epochs и persistent config counters плюс новый run. Это **не полная гарантия**, особенно против save sanitize/аварии до flush. При неполной наблюдаемости — INCOMPLETE_OBSERVABILITY, не «вероятно clean». Product salvage можно разрешить отдельно. Adapter здесь не создан: перед эксплуатацией нужен pin/review/drill.


## F157 — W2-A: Accumulation boundary и actual progress

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Accumulation boundary и actual progress»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S210, S211, S213, S215, S216.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F157. Native epoch checkpoint не lossless accumulation boundary.** Нет обязательного tail flush: после последнего step остаются gradients, используемые следующей непрерывной эпохой. Они не сериализованы; resume начинает с zero_grad и новой локальной cadence. nbs>batch не гарантирует делимость, warmup меняет accumulate. nbs=batch тоже не решает EMA/raw, RNG/loader/precision отличия. S210/S211 — отсутствие гарантии, не измеренная потеря.

Невыполненный арифметический контрпример: warmup0, nb5, accumulate3, epoch0, last_opt_step=-1. Условие делает step на ni2; ni3,4 pending. Непрерывная следующая эпоха делает step на ni5 с тремя microbatches. Resume теряет pending, сбрасывает last_opt_step и делает иной step на первом batch. Это вывод из исходника, не запуск модели.

Sidecar ниже — **предложение**. Неизвестное null с причиной, не epoch×dataset. Обязательны monotonic consumed work и restored state frontier: rollback не уменьшает затраченный ресурс.

| Поля | Смысл/получение |
|---|---|
| run_id, attempt_id, parent_run_id, parent_checkpoint_sha256, recipe_hash, code_sha, adapter_sha, env_lock_hash | Lineage; fixed spec не перезаписывается effective config |
| event_seq, UTC, monotonic_time, rank/process, epoch_index, epoch_visit | Повтор эпохи получает новый visit; время/seq не сбрасываются |
| requested/resolved/per_rank_batch, actual_batch_len, nbs, accumulate_current, loader_len, warmup, LR/decay groups | Реальная длина из image tensor, не числа cls |
| batches_entered, images_entered, backward_completed_observed, images_backward_completed_observed | Preprocess/forward entry против batch-end observation; exception/time-break промежутки censored |
| optimizer_step_attempts, optimizer_step_calls, optimizer_updates_applied, update_observer_kind, skipped_updates | Разные события; applied только при проверенном observer, иначе null |
| ema_updates, scaler_enabled, scale_before/after, nonfinite_loss/grad/model/ema events | Диагностика, не замена applied counter |
| pending_microbatches/images, pending_gradients_present, boundary_kind | Нет точной наблюдаемости — unknown; epoch label недостаточен |
| oom_events_total, nan_events_total, save_repair_events, recovery_events, replayed_images_observed, rollback_frontier | Append-only history; native resettable counters только дополнение |
| checkpoint_state_epoch, state_frontier_updates, snapshot_sha256/bytes, external_receipt, resume_mode | State может отставать от consumed work |
| comparison_eligible, status, stop_reason, observability_gaps, final_seal | Exit0 — одно из условий приёмки |

**F157. Callback по имени optimizer_step создаёт ложную измеримость.** S213 помечает optimizer_step/on_before_zero_grad/on_params_update reserved; stock trainer их не dispatch. Для attempts нужен override метода с super, не одноимённый callback. PyTorch post-hook подтверждает вызов step, однако fused CUDA Adam/AdamW здесь передаёт overflow внутрь kernel. S215/S216 показывают special path: hook count не автоматически applied updates. Равенство весов также не доказывает skip: легитимный update бывает нулевым.

Дешёвый resource-bounded контракт: публиковать attempts/known skips, applied оставлять null до проверки observer. Для equal-applied-updates ablation null блокирует допуск: сначала actual optimizer state-step/skip drill. Не менять optimizer/fused молча ради счётчика — это новая recipe. Сохранённый nominal effective batch не отменяет физическую batch mutation.


## F158 — W2-A: Будущий negative drill — не выполнен

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Будущий negative drill — не выполнен»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**Вопрос:** отклоняет ли guard ложный clean-success и сохраняет ли native recovery честную lineage? Входы: разрешённый tiny train-only/synthetic набор с batch IDs, pinned executable environment+guard, disposable output, маленький внешний archive endpoint. Нужны отдельное поручение исполнения и при необходимости разрешение ресурсов. Без lockbox, sweeps, реального исчерпания GPU памяти/диска на единственной копии.

1. Однократный synthetic RuntimeError в forward/backward после успешного update: четыре recognized messages. Контроль без guard наблюдает native dispatch; guard должен fail и не выполнять следующие batches. Повтор batch1 проверяет detector без batch diff. Это тест dispatch, не реального fit.
2. Nonfinite loss/fitness в start и поздней эпохе; поздней дать tiny last. Guard должен fail до accepted save. Отдельно transient NaN одного batch, позже перезаписанная loss.
3. Перед save испортить EMA tensor при finite online; отдельно непредставимое half значение. Guard отклоняет accepted snapshot даже если stock контроль запишет finite bytes. Только disposable model.
4. nb5/accumulate3: pending metadata на epoch boundary, normal continuation против native_ema resume. Совпадения не обещать, отклонения документировать; actual warmup учитывать.
5. AMP overflow: сравнить attempts, hook calls, state-step delta, EMA и scale trace. Неверный applied observer для fused path блокирует equal-updates claims. CPU без AMP не подтверждает этот пункт.
6. Final save: immutable pre-strip copy → внешние bytes/hash/load → finalization. Corrupted/stale duplicate не должна пройти receipt; хорошую единственную копию не портить.

Метрики/артефакты: false clean-success (приёмка 0 для выполненных negative cases); next-batches-after-fail (0); event classification/seq; attempts/applied/EMA traces; pending/replayed counters; code/adapter/env hashes; checkpoint manifests и receipts. Время/размеры только после измерения.

Успех подтверждает проверенный scope guard; не доказывает реальный 24GB train/val fit, crash RPO, exact resume, independent accuracy, license acceptance, export, LinQ parity/latency, надёжность Vast. Trace mismatch исправляет observer, не переписывает историю.


## F159 — W2-A: Отрицательные находки и handoffs

- Происхождение/locator: [W2-A](_WORK/W2_A.md), раздел «Отрицательные находки и handoffs»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- K001 подтверждён; W1 SUCCEEDED дополнить event/observability gate, исходную критику сохранить.
- Backend engine/internal error не доказательство физического OOM: native код объединяет сообщения, причина требует диагностики.
- Native_ema допустим, но требует parent, replayed work, changed recipe и DEV evaluation. History не восстановить из sanitized checkpoint.
- W2-B/training owner: actual Torch/optimizer stack и adapter pin; Ultralytics source SHA установлен, binary/runtime lock отсутствует. PyTorch2.14 здесь механизм, не рекомендация менять согласуемый stack.
- Registry/W1-14/15: comparison_eligible, persistent recovery events, unknown-progress semantics; не строить новую controller platform.
- Root/K011: без закрытых data/runtime/license gates default путь без обучения; один fine-tune после gates; challenger после измеренного обязательного резерва. Native snapshot+receipt — минимум, exact replay deferred.
- Evaluation: salvage candidate оценивать с историей; retries/checkpoint selection не дают доступ к lockbox. Train/DEV/SELECT/lockbox разделять по independent camera/scene/episode, без соседних кадров.
- LinQ: передавать accepted checkpoint hash+label map+preprocessing; recovery success не evidence финального inference.

Открыто: owner guard, actual environment/optimizer, archive endpoint, размеры/latency checkpoints, applied observer, target recovery behaviour. Public research не закрывает runtime вопросы. Расходы и запуски отчёт не авторизует.


## F160 — W2-B: Решение и изменение решения W1

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Решение и изменение решения W1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S218, S219, S221, S222, S224, S225, S228, S229.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


**F160.** Не брать W1-13 image `torch2.14.1` как готовый общий trainer/exporter. Для первой проверяемой реализации выбрать **два изолированных model environments** с одним небольшим, согласованным core: Linux x86_64, Python **3.11.9**, Torch **2.5.1**, torchvision **0.20.1**. Train: официальные cu124 wheels; export: такие же версии CPU wheels. Проекты и их extras не смешивать в одном env. Это выбранный **compatibility envelope**, не installed lock и не доказанная комбинация. PyTorch официально публикует эту пару и индексы; Python взят из native D-FINE setup. Не требуется контейнер со всеми семействами. [S218–S221]

**F160.** Общий floating export baseline: NumPy **1.26.4**, ONNX **1.17.0**, ORT CPU **1.20.1**; для image utilities OpenCV **4.10.0.84**. Выбор конкретных pins — **INFERRED**, существование версий/declared metadata — **DOC**, imports/parity — **UNRUN**. Python3.11 удовлетворяет metadata ONNX/transformers; ONNX требует numpy>=1.20 и protobuf>=3.20.2; ORT требует numpy>=1.21.6. ORT1.20 матрица содержит opset21/IR10, что покрывает выбранные opset16/18 по версии, но не гарантирует наличие всех kernels/численный parity. Фактический IR надо прочитать из экспортированного файла. [S225–S228]

**F160.** YOLO export — explicit legacy `dynamo=False` внутри native wrapper; D-FINE export — небольшой зафиксированный adapter к native script, static batch1, `dynamo=False`, без simplification. D-FINE stock CLI **не даёт выключить** simplify: `store_true` вместе с `default=True`; отсутствие `--simplify` не отключает его. Этот новый факт меняет команду W1: для первого unsimplified parity нельзя просто убрать флаг. [S222–S224]

**F160.** Conservative fallback: **Torch2.4.1 / torchvision0.19.1**, Python3.11.9, те же NumPy/ONNX/ORT и изоляция; official cu124 train / CPU export indexes. YOLO fallback export opset17, D-FINE16, legacy mode; это другой recipe ID, fresh smoke обязателен. В 2.4.1 `torch.onnx.export` действительно принимает `dynamo=False`. Не использовать Torch2.4.0 на Windows: pinned Ultralytics явно исключает эту комбинацию. Возврат к2.4.1 не является утверждением о неправильности2.14.1 или гарантией fit. [S218,S219,S229]


## F161 — W2-B: K-ID: исходная критика сохранена

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «K-ID: исходная критика сохранена»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


**K002, CRITIC.md, P0**: pinned base/digest и SHA разных проектов не образуют согласованную Python/Torch/vision/exporter/ONNX/ORT recipe; D-FINE наследует Torch exporter default, YOLO явно задаёт legacy; installed lock нельзя выдумывать. Эта критика **подтверждена**, не переписана. Статус после W2-B: **закрыто документально в части source-backed выбранных envelopes и entrypoints; runtime часть остаётся открытой**. Новые evidence: native requirements, explicit2.5.1 API, версия пары vision, D-FINE CLI-default trap, release BC changes и PyPI metadata. На сегодня ни один manifest ниже не имеет статуса `installed`/`tested`.

**K001, CRITIC.md, P0**: native Ultralytics OOM/NaN recovery может менять recipe внутри exit0; accumulation/native EMA resume не обещают lossless continuation. Статус здесь: **уточнена применимость, не закрыто этой веткой**. Сохранение того же Ultralytics SHA сохраняет проблему независимо от выбранного Torch. Передача W2-A обязательна: нельзя «закрыть» её сменой package pins. Root сообщил, что `optimizer_step`/`on_before_zero_grad` hooks stock loop не вызывает; здесь такие hooks не предлагаются как работающие. Успех установки не является доказательством immutable trial.


## F162 — W2-B: Манифест A: YOLO26s baseline

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Манифест A: YOLO26s baseline»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S223, S230.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


Статусы: **DOC** — прямо прочитано в первичном источнике; **INFERRED** — наш выбор внутри объявленных ограничений; **UNRUN** — практическая проверка не проведена. Поле может иметь одновременно `DOC + INFERRED + UNRUN`: наличие API документировано, значение выбрано нами, исполнение неизвестно.

| Поле | Значение / статус |
|---|---|
| Source | Ultralytics SHA `de290d865035acbfa4bb24cc88960d8b52c26e45`, snapshot `8.4.184`; **DOC**, install **UNRUN**. Ставить из checkout этого SHA, не floating pip release |
| Python / OS | Linux x86_64 + Python3.11.9; project declares Python>=3.8, выбранная micro-version **INFERRED**, runtime inventory **UNRUN** |
| Train core | torch2.5.1 / torchvision0.20.1 official cu124 pair **DOC**; выбор **INFERRED**, driver/GPU/ABI/import **UNRUN** |
| Export core | Python3.11.9 + torch2.5.1 / torchvision0.20.1 CPU, NumPy1.26.4, ONNX1.17.0, ORT CPU1.20.1; pins **INFERRED**, availability/requirements частично **DOC**, исполнение **UNRUN** |
| Init | `https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt`; W1-02 metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b`; байты и hash **UNRUN**, source asset identity передана W1-02/W2-C |
| Exposure / license | W2-C сообщает O365v1→COCO recipe и AGPL/Enterprise; **handoff**, не объявлять COCO-only или permissive. Сохранить exact W2-C source record и notices до запуска |
| Training entrypoint | `from ultralytics import YOLO; YOLO(LOCAL_INIT).train(data=LOCAL_DATA_YAML, imgsz=640, batch=B, epochs=E, optimizer="AdamW", lr0=0.0003, nbs=N, seed=0, device=0, amp=True, resume=False)`; API **DOC**, recipe values **INFERRED**, весь run **UNRUN** |
| Physical/effective batch | B/N определяет qualification; E — заранее выбранное окно после данных. Не брать auto batch и не считать B=2 проверенным fit; все эти поля до qualification **UNRUN**. Ограничить val отдельно |
| Export entrypoint | `YOLO(LOCAL_SELECTED_PT).export(format="onnx", imgsz=640, batch=1, dynamic=False, simplify=False, half=False, nms=False, opset=18, device="cpu")`; API/mode semantics **DOC**, значения **INFERRED**, artifact **UNRUN** |
| Head | `nms=False` выбирает one-to-one/e2e в этой ревизии; `images`→`output0`, ожидаемый `[B,K,6]` = xyxy/score/class. Это **DOC expected contract**, actual head/fusion/dtype/shape **UNRUN** |
| Exporter mode | native `ultralytics/utils/export/engine.py::torch2onnx`, TORCH>=2.4 передаёт `dynamo=False`; **DOC**, actual call/artifact **UNRUN** |
| Simplifier | Не устанавливать `[export-base]` ради первого несжатого графа: он затягивает onnxslim>=0.1.82. При `simplify=False` native ONNX branch требует ONNX, ORT можно поставить отдельно для comparator; **DOC/INFERRED**, run **UNRUN** |
| Recovery | native OOM/NaN path требует W2-A fail/fork policy; **UNRUN**. Смена B/N/AMP после ошибки = новый recipe/run; exit0 недостаточен |

Первый экспорт намеренно не содержит embedded NMS. One-to-one всё ещё содержит top-k/gather. Если LinQ не принимает этот путь, отдельный dense artifact с `nms=None` допустим **только при наличии one-to-many head в фактическом checkpoint**. `Detect.end2end` getter сохраняет e2e, если fusion уже удалил `cv2`: одно присваивание/флаг не восстанавливает отсутствующие веса. Dense `[B,4+C,A]` и e2e нельзя сравнивать как одну голову; нужны отдельные reference и качество. [S223,S230]

Пример будущей установки core, **не исполнен**:

```bash
# В train env A, после создания Python3.11.9 окружения:
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124
# В отдельном export env A:
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
# После применения выбранных constraints к установке pinned проекта:
python -m pip install numpy==1.26.4 onnx==1.17.0 onnxruntime==1.20.1 opencv-python==4.10.0.84
```

Эти команды фиксируют core, **не образуют полный install script/lock**. В editable install проекта тоже передать constraints, чтобы resolver не заменил core. Собрать собственный wheel/lock и image digest только после resolution; `pip check`, freeze и smoke обязательны. Нельзя подменить2.14.1 base установкой2.5.1 поверх и продолжать называть image готовым2.14.1 recipe.


## F163 — W2-B: Манифест B: D-FINE-M challenger

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Манифест B: D-FINE-M challenger»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S224, S231.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


| Поле | Значение / статус |
|---|---|
| Source | `Peterande/D-FINE@956d1709314c2c6a4df6f34de232054578a7449f`; **DOC**, install **UNRUN** |
| Native requirements | torch>=2.0.1, torchvision>=0.15.2, faster-coco-eval>=1.6.6, PyYAML, tensorboard, scipy, calflops, transformers, loguru; **DOC**, без верхних границ/lock |
| Python/core | Native README Python3.11.9 **DOC**; выбранные Torch2.5.1/vision0.20.1 cu124 train, CPU export удовлетворяют declared minima **INFERRED**, фактическая совместимость **UNRUN** |
| Ancillary constraints | transformers4.44.2, calflops0.3.2 — выбранные **INFERRED** candidates, PyPI versions/metadata **DOC**; остальной полный lock ещё **UNRUN**. calflops тянет accelerate>=0.22.0 и HF hub; transformers требует hub>=0.23.2,<1.0 и tokenizers>=0.19,<0.20. Их пересечение не является resolved env |
| Init / exposure | `https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth` — primary README model-zoo **DOC**. Отдельно от obj365/obj2coco; hash полученных байтов **UNRUN**, веса не скачаны |
| Config | `configs/dfine/custom/dfine_hgnetv2_m_custom.yml` плюс все include: custom_detection/runtime/dataloader/optimizer/dfine_hgnetv2; HGNetv2 B2,4 decoder layers **DOC** |
| Data adaptation | Собственный frozen config меняет `num_classes:777`, train/val paths и class mapping; original custom YAML содержит placeholders. Это необходимая **INFERRED** работа, **UNRUN**; нельзя запускать placeholder config как target training |
| Training entrypoint | `python train.py -c configs/team/dfine_m_target.yml -t LOCAL_DFINE_M_COCO --use-amp --seed 0 --output-dir output/RUN_ID`; flags **DOC**, path/recipe **INFERRED**, запуск **UNRUN**. `-t` = tuning, не `-r` resume |
| Train mutations | frozen config Btrain/Bval/epochs/stop_epoch/optimizer/AMP/EMA; native stage transition `stop_epoch` reloads `best_stg1.pth` и меняет EMA decay. Сократить epochs без согласования stop_epoch — другой recipe; **DOC/INFERRED**, execution **UNRUN** |
| Export entrypoint | stock `python tools/deployment/export_onnx.py -c SAME_CONFIG -r LOCAL_SELECTED_PTH`; **DOC**, но для выбранного первого gate использовать `tools/deployment/export_onnx_static_w2b.py` с нижеследующим diff **INFERRED, UNRUN** |
| Export envelope | CPU torch2.5.1/vision0.20.1, numpy1.26.4, onnx1.17.0, ORT CPU1.20.1; **INFERRED, UNRUN**. onnxsim0.4.36 — только отдельный optional simplified artifact |
| State / head | Native предпочитает `checkpoint["ema"]["module"]`, иначе `["model"]`, затем `model.deploy()+postprocessor.deploy()`; **DOC**. Reference обязан использовать этот же wrapper/state |
| Inputs / outputs | FP32 `images[1,3,640,640]`, int64 `orig_target_sizes[1,2]`; `labels/boxes/scores`; в выбранном adapter static batch1/opset16/legacy **INFERRED**, native names/opset **DOC**, actual graph **UNRUN** |
| Postprocess | native focal sigmoid→global query/class top-k→boxes gather, deploy outputs без train evaluator remap. Сохранить num_top_queries, category mapping, semantic size и inverse transform; **DOC**, parity **UNRUN** |

Минимальный **предлагаемый, не созданный/неисполненный executable adapter diff** к S224 (до исполнения сохранить patch bytes+hash):

```diff
- data = torch.rand(32, 3, 640, 640)
+ data = torch.rand(1, 3, 640, 640)
  size = torch.tensor([[640, 640]])
+ model.eval()
...
- dynamic_axes=dynamic_axes,
+ dynamic_axes=None,
  opset_version=16,
+ dynamo=False,
...
- default=True,  # в parser --simplify
+ default=False, # --simplify opt-in; первоначально не передавать
```

`size` здесь задаёт выбранную координатную систему640², не автоматически исходное H/W кадра; preprocessor/CPU inverse geometry обязаны ей соответствовать. В исходнике dummy batch32 при size batch1 допускает broadcasting; изменение наbatch1 убирает этот ненужный квалификационный ресурсный фактор, но не доказывает fit обучения. `--check` остаётся structural checker. Simplified граф сохранить под другим именем, не перезаписывать единственную unsimplified копию; такой output-name patch также versioned. [S224,S231]


## F164 — W2-B: Конкретные несовместимости/негативные результаты

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Конкретные несовместимости/негативные результаты»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S218, S219, S220, S221, S224, S227, S229, S232, S233, S234, S235, S236, S237, S238.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


**F164.** Native D-FINE source не объявляет ONNX/ORT/onnxsim в requirements. Установка `-r requirements.txt` не устанавливает полный export path. Более того, imports `src` могут тянуть training dependencies и при export; нельзя обещать «экспортный env состоит из Torch+ONNX» без import smoke. Выбранные transformers/calflops pins уменьшают дрейф, но не подтверждены авторами как их installed stack. [S220,S224,S232,S233]

**F164.** PyTorch2.6 официально изменил default `torch.load` на `weights_only=True`. В D-FINE local tuning/resume и exporter вызовы не задают `weights_only`. Следовательно, произвольный upgrade меняет semantics загрузки. Это **риск**, а не доказательство, что все D-FINE checkpoints сломаются: plain state_dict может загрузиться. Torch2.5.1 обходит именно эту смену default, но разрешает старую pickle semantics: использовать только установленное trusted происхождение/hash. Не прописывать глобальное отключение защит загрузки ради непроверенного файла. [S234,S235]

**F164.** Текущий Ultralytics pyproject содержит нижние границы и platform markers, а не lock; extras могут принести новые зависимости. `export-base` требует onnxslim>=0.1.82 и Python>=3.11 ORT>=1.20; выбранные ORT1.20.1/ONNX1.17 это допускают. Но simplifier намеренно исключён из первого пути. Зафиксировать NumPy1.26.4 + OpenCV4.10.0.84 полезно для legacy envelope: нельзя поставить произвольный current OpenCV и считать NumPy pin автоматически совместимым. PyPI4.10.0.84 metadata для Python3.11 требует numpy>=1.23.5. [S219,S227,S236]

Версия2.14.1 из W1-13 не опровергнута: её metadata существование не является доказательством применимости D-FINE old exporter. Live previous-versions при новом открытии уже показывает2.13.0 выше2.6.0; прежний W1 stale view не переносить как актуальное состояние. Рекомендация2.5.1 основана на конкретной exporter/load семантике и официальной паре, а не гонке за latest.2.4.1 fallback также UNRUN. [S218,S221,S229,S234]

Дополнительное ограничение K001 у challenger: `det_engine.py` при AMP сохраняет `NaN.pth`, если boxes содержат NaN/Inf, но этот block сам не прерывает обучение; дальше scaler может пропустить optimizer step. `det_solver.py` меняет state на stage boundary. Поэтому «нет YOLO recovery» не означает immutable D-FINE progress. Требуется journal nonfinite/skipped-step/stage-reload; ожидаемый stage transition заранее часть recipe, неожиданное recovery/NaN — failed trial. Это статическое чтение, negative drill не выполнен. [S237,S238]


## F165 — W2-B: Один будущий discriminating experiment, без аренды сейчас

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Один будущий discriminating experiment, без аренды сейчас»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


**Вопрос:** достаточно ли выбранных source-compatible envelopes для одного полного train→save/reload→same-head floating ONNX→ORT пути, или несовместимость локализуется в dependency/import/load/trace/runtime? Сначала проверять экспорт pretrained, чтобы не тратить training run на неизвестный exporter. Данные — небольшой разрешённый DEV fixture с raw frames и golden RGB/normalized tensors, explicit class mapping и geometry. Synthetic tensor разрешён для shape/smoke, но не для quality evidence.

1. В отдельно разрешённой подготовке создать A/B environments из frozen source и выбранных constraints; записать resolver report, wheel hashes, Python/build/platform, `pip check`, imports. Разрешать зависимости без бесконтрольной замены core. При конфликте остановиться с отчётом, затем новый manifest ID; не редактировать старый lock. Записать полный resolved lock и image digest лишь после факта.
2. Trusted init download/hash, показать key/missing/unmatched logs. D-FINE custom nc/path placeholders заменить frozen target config. До training экспортировать same-deploy reference наCPU, checker, ORT CPU comparator для golden tensor. Проверить head/state/names/dtype/shapes/opset/IR/operator inventory. Численные tolerance задать заранее по box/score, top-k ties сравнивать отдельно; несовпадения не скрывать одним mAP.
3. Только после разрешения hardware smoke: конкретная3090, inventory driver/CUDA/cuDNN/device, representative forward/backward, native val, save/reload. Btrain/Bval увеличить лишь в отдельном qualification run; измерить peak allocated/reserved и параметры реального batch/accumulation, AMP skipped/nonfinite steps.24GB fit и длительность до этого unknown.
4. После training повторить export/parity именно выбранного checkpoint и state; отдельно LinQ gate W2-F. Не считать экспорт до fine-tune достаточным для final model, другой head/precision/input требует нового gate.
5. Если2.5.1 path ломается на API/trace, пробовать fallback2.4.1/vision0.19.1 с новым ID; если ломается LinQ operator, смена Torch сама по себе не решение. Сначала локализовать op; conditional dense/CPU postprocess/new graph policy, затем новый parity. Unsupported required neural graph ⇒ baseline/challenger blocked для этого deployment, не ложный quality failure.

**Артефакты:** constraints+resolved lock, install logs, source/patch/config/checkpoint/tensor/ONNX hashes, raw comparator outputs, traces/операторы, recovery/step log, memory train/val, exact hardware, decision PASS/FAIL/BLOCKED и locator. **Метрики**: imports/checker/runtime errors; max/quantiles absolute/relative score и box error; label/ranking differences near ties; actual completed optimizer updates; nonfinite/skipped steps; peaks. Никаких invented времени/VRAM/вероятностей.

**Успех не доказывает:** target accuracy, tiny PPE recall, multi-camera latency, LinQ compilation/placement/quantization, независимость dataset splits, точный lossless resume или совместимость другой версии. DEV export fixes/threshold/checkpoint tuning не проводить на lockbox. TRAIN/VAL/SELECT/lockbox должны быть separated по incident/camera/scene lineage, соседние кадры не независимые samples.


## F166 — W2-B: Хэндoff и оставшиеся блокеры

- Происхождение/locator: [W2-B](_WORK/W2_B.md), раздел «Хэндoff и оставшиеся блокеры»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.

- Применимость после интеграции: После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.


- **W2-A/K001:** применить fail/fork policy к этому же Ultralytics SHA; confirmed-loop hooks вместо выдуманных callbacks, не приравнивать EMA updates к успешным optimizer steps. D-FINE stage reload и AMP skips явно учесть.
- **W2-C:** checkpoint bytes hash/license/exposure; O365 provenance YOLO26 и D-FINE COCO/obj2coco разделить. Source licenses не выдают target-data permission.
- **W2-F:** передать distinct graph contracts A-one2one-opset18 / A-dense-conditional / B-static-postprocess-opset16; реальные supported IR/opset/layout/input dtypes/TopK/Gather/GridSample/LinQ SDK остаются внешними Q. Никаких TPU claims из ORT CPU.
- **Владелец реализации:** создать два environment constraints, недостающий full lock и небольшой D-FINE adapter; Python3.11.9 availability/Linux base digest/host driver — inventory. Нужны разрешённые данные, trusted weights, доступный CPU для import/export и отдельно GPU для train smoke. Никакие расходы настоящим документом не разрешены.
- Незакрытые package decisions: build isolation setuptools/wheel; все noncore dependencies Ultralytics (включая ultralytics-platform дляPython>=3.11), D-FINE faster-coco-eval/scipy/PyYAML/tensorboard/loguru; transitive accelerate/HF/tokenizers/safetensors/protobuf; wheel tags/GLIBC/CPU libs. Нет основания писать «все SHA pinned ⇒ stack runnable».


## F167 — W2-C: Решение и изменение после W1

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Решение и изменение после W1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S241, S244, S251.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F167. D-FINE-M остаётся условным инженерным challenger, но основание «лучше решит мелкие/закрытые phone/PPE» понижается до непроверенной гипотезы.** Новое численное size evidence есть; controlled pairwise YOLO26s↔D-FINE-M по target errors нет. Перед challenger поставить аудит меток/visibility и одну spatial ablation той же baseline. Если аудит обнаружит преимущественно ошибки локализации видимых объектов нормального размера, D-FINE имеет содержательную мотивацию как regression alternative; если объект потерян resize, дополнительные bins/attention не возвращают исчезнувшие пиксели. Это наша рекомендация, не выполненный опыт.

**F167. Самое существенное уточнение provenance — `yolo26s.pt` нельзя считать COCO-only control.** Pinned авторский training-recipe сообщает Objects365v1 pretraining 150 epochs → COCO S70, batch128, 640, MuSGD; начальный файл `yolo26s-objv1-150.pt`. Это не чтение нами train_args самого бинарника, а заявленная авторами lineage. Следовательно, отделять «D-FINE O365» от baseline как единственный дополнительный external-data фактор неверно. Не следует также приравнивать два Objects365 режима друг к другу. [S241]

**F167. Весовой grant D-FINE существенно уточнён; YOLOX fallback остаётся условным.** В author HF model repository найдено явное `license: apache-2.0` и exact M checkpoint с LFS SHA256. Это сильнее одного code LICENSE. У native HGNetv2-B2 init отдельный weight grant не установлен. У YOLOX есть Apache code/license и официальный release, но специального grant выбранному `.pth` не найдено; на первичной issue #1865 вопросы об этом остаются без видимого ответа maintainer. Это не доказательство запрета. Нельзя писать «YOLOX гарантированно permissive weights». [S244–S251]

**Статус исходных K:**

| K / исходное замечание | Статус W2 | Что изменилось / что не закрыто |
|---|---|---|
| K003 P0: code LICENSE вместо exact detector checkpoint/backbone provenance; доступность только ссылками | **Applicability clarified, частично закрыто; общий K остаётся open** | Все три native assets доступны по HEAD; для D-FINE есть author model-repo grant и hash metadata, для YOLO explicit model scope. YOLOX weight scope, B2 init grant, acceptance способа поставки и SHA256 реально полученных байтов остаются gates. Нельзя закрыть K публичным поиском целиком |
| K004 P1: порядок challengers основан на общем AP/удобстве вместо comparable dominant-error evidence | **Документальная часть закрыта по разрешённой ветке downgrade; target superiority open** | Получены native size/pretraining/exposure данные, ограничения и конкретная ablation. Порядок больше не заявляется как доказанный accuracy ranking. Исходная критика была верной на момент W1, её provenance не переписан |


## F168 — W2-C: Минимальное pairwise сопоставление

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Минимальное pairwise сопоставление»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S240, S241, S242, S243, S248, S250, S252.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Все числа ниже опубликованы авторами; мои измерения отсутствуют. Размер входа одинаков по стороне, но preprocess, train exposure, head и model capacity не выровнены.

| Поле | YOLO26s released | D-FINE-M COCO | D-FINE-M O365→COCO | YOLOX-s 0.1.1rc0 fallback |
|---|---|---|---|---|
| Native reported eval | COCO val2017, AP50:95 | COCO val2017, COCO metrics | тот же COCO split | README val/test разделены; retained val40.5 |
| Eval input / head | 640; dense+NMS **либо** o2o e2e | 640×640 Resize, e2e 300 queries | тот же | 640; dense+NMS |
| AP / APsmall | 48.6 dense / **29.5**; e2e AP47.8, exact released e2e APsmall не установлен | 52.3 / **33.2** | 55.1 / **37.9** | AP40.5; exact new asset APsmall не установлен |
| Capacity | 9.5M fused | HGNetv2-B2, ~19.2M, 4 decoder layers | тот же | 9.0M; depth0.33,width0.50 |
| Detector/backbone exposure | См. F02 | ImageNet backbone → COCO; paper120+4 epochs, pinned config **132/stop120** | paper M29 O365 +49 COCO; pinned obj2coco config **56/stop48** | paper trained from scratch COCO300; exact release обновлённый preprocessing, code max_epoch300/no_aug15 |
| Native train input | 640 plus scale/mosaic recipe | resize640 + collate multiscale | то же, другая schedule/init | base640, multiscale |
| Occlusion evidence | Отдельного quantitative occlusion benchmark этой пары не найдено | Fig5 **X**, qualitative selected examples; не M benchmark | не установлено отдельно | не установлен для exact asset |
| Target phone/PPE / short fine-tune | **unknown** | **unknown** | **unknown** | **unknown** |

Локаторы: YOLO paper Table7/S8 [S240]; training guide [S241]; D-FINE paper Appendix A.1, Tables6–7/Fig5 [S242]; configs [S243]; YOLOX paper §2.1/Table3 и native code/release [S248–S250]. Published COCO numbers не дают controlled архитектурного эффекта. YOLO26s↔D-FINE-M отличается примерно двукратной ёмкостью и lineage. D-FINE-M COCO↔O365 действительно показывает опубликованный прирост size/AP, но не изолирует архитектуру и не обещает быстрый target transfer. Разница paper/native schedules — причина использовать фактически pinned merged config и load-log, а не смешивать их как один рецепт.

**F168. APsmall не является измерением окклюзии или «всех объектов меньше 32px после resize640».** В COCO evaluator `Params.setDetParams` area ranges используют annotation area0…32²; `evaluateImg` сравнивает `g['area']` с `aRng`, `iscrowd` влияет на ignore. Это площадь исходной аннотации, не видимость, не short-side remap и не вся foreground occupancy в resized tensor. Порог площади не отделяет телефон у лица от каски/ремня, а pooled AP смешивает классы. Для target нужны два независимых поля: размеры после actual preprocess и visibility/occlusion по согласованной разметке. [S252]

YOLO STAL ablation даёт ограничивающий контрпример универсальному «назначение для small всегда лучше»: Table6 на **YOLO11s baseline**, TAL APsmall29.0 → STAL ref16 29.6, ref8 **27.7**, ref32 **28.3**. Это механизм/чувствительность, не отдельный доказанный прирост released YOLO26s на PPE. [S240] Значение APsmall29.5 в TableS8 относится dense48.6 строке; не комбинировать его с e2e latency/AP.

**F168. Нативное короткое дообучение не имеет доказанного одинакового «ценника».** Предлагаемые ранее короткие schedules остаются авторскими/нашими adaptations с разными optimizer/LR/augmentation late stage. Ни published long training AP, ни число epochs не измеряют target convergence за одинаковое время. Нужны реальные counts optimizer steps, processed images, wall time, validation/EMA/checkpoint overhead, peak VRAM и outcome по независимым группам. Нельзя из README вывести fit на3090 либо вероятность успеть. Не расширять сравнение ещё одним семейством: RF-DETR для разрешения данного вопроса не понадобился.


## F169 — W2-C: Точный asset / доступность / license scope

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Точный asset / доступность / license scope»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S241, S243, S244, S245, S246, S247, S248, S251, S253.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F169. HEAD реально наблюдён, полный бинарный GET не выполнялся.** Stable URL →302→200; GitHub final host `release-assets.githubusercontent.com`, HF final host `us.aws.cdn.hf.co`; везде `application/octet-stream`. `Content-Disposition` содержит ожидаемое имя. Таблица — наблюдение HTTP metadata, не проверка checkpoint tensors, внутренней модели, malware, load success либо вечной доступности. См. `HEAD_SUMMARY.json` и raw `head_metadata.json`. Размеры — bytes по HTTP, не оценка RAM/VRAM.

| Asset, точный источник | Content-Length | Published/metadata checksum | Статус прав и scope |
|---|---:|---|---|
| [yolo26s.pt v8.4.0](https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt) | 20,422,725 | GitHub asset340096060; SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b`; updated2026-01-13T19:59:22Z | **explicit grant:** pinned docs явно code/models/docs AGPL-3.0 или Enterprise. Реальное соответствие выбранной поставки не принято командой; закрытая proprietary поставка без другой лицензии — **incompatible with chosen use** по заявлению поставщика, если такой use выбран [S245,S246] |
| [dfine_m_coco.pth GitHub dfinev1.0](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth) | 79,108,938 | GitHub digest API получить не удалось (403); byte hash неизвестен | Native GitHub asset: **project-level claim** Apache storage/project LICENSE. Для сильнее установленного grant выбрать exact HF artifact в следующей строке; не объявлять равенство байтов по размеру |
| [dfine_m_coco.pth author HF@19214e9](https://huggingface.co/Peterande/D-FINE/resolve/19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth) | 79,108,938 | LFS SHA256 **`b44a7586bf490858c7b8bce9e44bd025cb88724df9a07a8deb3ae1c12e608195`** | **explicit grant (model-repo designation):** model card Apache-2.0. Это scope размещённых в model-repo весов, а не отдельный assurance всех upstream прав; license text/notice сохранить вместе с card [S244] |
| [dfine_m_obj2coco.pth GitHub](https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_obj2coco.pth) | 79,117,378 | HF repo содержит одноимённый asset с LFS SHA256 `183caeb10b3266b62b9bc36917f8b7c0b10c14d3ed2dc4c9ce776ea14e3ec1d8`; это **не** самостоятельно проверенный GitHub hash | GitHub **project-level claim**; HF **explicit designation**, но **unresolved** dataset scope для выбранного коммерческого use; pinned README предупреждает о Objects365 [S244,S247] |
| [PPHGNetV2_B2_stage1.pth](https://github.com/Peterande/storage/releases/download/dfinev1.0/PPHGNetV2_B2_stage1.pth) | 24,362,501 | отдельный hash не установлен | **project-level claim / unresolved weight-specific grant**. Есть авторская Apache storage LICENSE и известная ImageNet lineage, но индивидуального grant/конверсии конкретного stage1 не найдено [S243,S247] |
| [yolox_s.pth 0.1.1rc0](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth) | 72,089,125 | digest API403; byte SHA256 неизвестен; HEAD Last-Modified2021-12-08 — это не дата публикации paper | **project-level claim** Apache code repository; **unresolved** explicit checkpoint scope. Условный fallback, не юридически подтверждённый permissive weight bundle [S248–S251] |

HF author provenance проверено: профиль **Peterande/Yansong Peng** ведёт на GitHub Peterande; тот же автор и владелец D-FINE. Model-repo SHA **19214e91f5ce4c1e609022c38b1fc953c47404e7**, card modified2024-10-30T12:10Z; M weights upload commit **a5f35932343b83c470bfe8659b439108080e6206**, 2024-10-30T11:46:47Z. LFS oid — content SHA256 metadata; Xet hash/HTTP ETag **другие** и не должны подменять его. Самостоятельный SHA256 всех реально полученных байтов остаётся gate. Одинаковые длина/имя GitHub/HF не доказывают byte identity.

Native D-FINE include выставляет `HGNetv2.pretrained: True`; constructor при initialization скачивает **отдельный** B2 stage1. Поэтому нельзя считать, что передача detector `-t` автоматически устранила dependency: конкретный path construction/loading нужно согласовать с W2-B. Если предлагается отключить backbone-download при полноценном detector-init, это adapter/config change, требующий smoke и полного load-log; здесь изменение не исполнялось. Прочитанный backbone header ведёт к PaddleDetection HGNetV2 implementation, но не устанавливает conversion chain exact B2 weights. [S243]

**F169. Objects365 lineage касается и baseline, а не только D-FINE challenger.** Official dataset download terms говорят academic-purpose-only; annotations/site CC-BY4.0, image rights отдельно, перераспространение изображений запрещено. Ultralytics dataset page shorthand CC-BY4.0 относится к слишком широкому заголовку, тогда как upstream разделяет типы материалов. Эти тексты не дают мне основания самостоятельно объявить обученные detector weights запрещёнными; они требуют сохранить unresolved upstream/use scope. Enterprise grant самого YOLO нельзя автоматически растянуть на чужой dataset. Для COCO-only D-FINE branch дополнительного detector-O365 exposure в опубликованной lineage нет, но ImageNet backbone остаётся. [S241,S247,S253]

Для YOLO26 **предлагаемый**, ещё не принятый командой путь поставки: весь доступный к передаче проект и исходные изменения/configs/training/export artifacts сохраняются с AGPL-3.0 и требуемыми notices; dataset bytes не публикуются автоматически. Если команда не готова к этому режиму или правила передачи проекта его исключают, retained YOLO path блокируется до иной разрешённой лицензии; покупка/обращение лицензиарам здесь не разрешались и не выполнялись. Нельзя объявить AGPL compliance фактом лишь наличием README/LICENSE. У Apache paths сохранить upstream texts, applicable attribution/NOTICE и отметить изменения; discovery отдельного NOTICE не завершён, отсутствие не заявляется.


## F170 — W2-C: Отрицательные результаты и противоречия

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Отрицательные результаты и противоречия»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S249, S250.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


1. Нет controlled target small/occlusion comparison, одинакового short-adaptation budget и выполненного LinQ gate. Не найден quantitative occlusion result именно D-FINE-M против YOLO26s; X qualitative gallery не переносится на M.
2. D-FINE paper M COCO120+4 против pinned YAML132/stop120; paper obj-pretrain+FT29+49 против current obj2coco56/stop48. Это различающиеся рецепты, не доказанная ошибка paper. Нельзя записать paper epochs как фактически исполненные released weights без training logs/metadata inspection.
3. YOLOX paper small S39.6 — legacy; chosen release README40.5. Release notes удаляют mean/std normalization и предупреждают об incompatibility старых weights; поэтому старый APsmall/препроцессинг нельзя автоматически приклеить к new `.pth`. [S249,S250]
4. YOLOX issue #1865 — вопрос пользователя, не grant/ответ проекта. Third-party LibreYOLO/SkillSafe cards называют веса Apache; они не выбраны доказательством прав upstream official asset.
5. GitHub release APIs D-FINE/YOLOX вернули403; повтор с cache query не исправил. Открытые release страницы и HEAD успешны. API failure не назван отсутствием assets. YOLO metadata API и HF API успешны; обхода accounts/auth не было.
6. Нет контроля содержимого HEAD-asset: правильный MIME/размер не доказывает пригодность, а опубликованный checksum не является моим checksum байтов. `torch.load` не вызывался.


## F171 — W2-C: Один различающий эксперимент — proposed, not run

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Один различающий эксперимент — proposed, not run»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**Вопрос:** доминирующие пропуски видимого телефона/малого PPE вызваны потерей spatial evidence/метками либо остаются после сохранения пикселей и требуют смены detector? Эксперимент проверяет обоснованность следующего challenger run, а не выбирает target winner заранее.

**Входы:** разрешённые target исходные видео и полные метки выбранных классов; visibility/ignore contract; train/VAL/optional SELECT/lockbox manifests; exact license-accepted checkpoint/code; доступный разрешённый training resource только для будущей adaptation; реальный LinQ SDK/CPU+TPU и telemetry для deployment gate. Число GPU, VRAM fit, длительность, бюджет/аренда и sample size здесь не выдуманы.

1. До обучения провести DEV error audit на имеющихся train/development примерах. Для каждого critical FN сохранить исходный crop, actual preprocessed view, bbox short side/area, видимость и annotation completeness. Неразличимый предмет пометить unknown/ignore по принятому правилу, а не автоматически no-PPE. Найти proportions spatial-loss / occlusion / annotation / classification / localization / association. Результат — observed counts, а не предположение о доминировании tiny объектов.
2. **A:** один baseline640 с exact head. **B:** тот же checkpoint/head, одна фиксированная spatial policy (например, higher-resolution full frame или заранее определённые ROI tiles; выбрать один вариант по audit), без смены весов на первом диагностическом проходе. Эффект B отвечает на pixel-budget question, но zero-shot B не доказывает optimal fine-tune. Crops оцениваются в исходной системе координат, дубли merging/ROI coverage не удаляются из событийной ошибки; routing использует только разрешённую информацию.
3. Если B исправляет spatial-loss, следующий ограниченный target training comparison A/B использует одинаковые train groups/labels, optimizer-update бюджет и selection policy; actual pixel/compute cost различается и журналируется. Если основная ошибка — missing labels, сначала исправить train/DEV разметку и перезапустить один baseline. Не вводить label fix+highres+новую архитектуру одновременно.
4. Только при сохраняющейся нужной ошибке и пройденных license/export gates добавить **C D-FINE-M COCO exact HF asset**, native adaptation manifest от W2-B. Те же split/ontology и product resource cap; равные updates для отдельной causal training ablation, но native product comparison явно допускает разные recipes и не называется pure architecture trial. O365 variant не добавлять в этот первый C как четвёртую степень свободы.
5. Threshold/checkpoint/ROI policy выбрать на VAL; если есть SELECT, отбор всей ограниченной recipe на нём; без SELECT честно указать повторное использование VAL. После freeze bundle единожды lockbox; не возвращать ошибку lockbox в tuning. Сравнить именно финальные LinQ-converted bundles по quality и сквозной latency, включая routing/crops/queue/event logic.

**Метрики:** per-class recall при согласованном FP budget; AP50:95 вспомогательно; size bins actual input pixels отдельно от original-COCO area; visibility/lighting/camera slices; event timely recall, FP/camera-hour, false no-PPE при occlusion, duplicates, missed short events, p95 capture→alert, queue age/drop rate. Counts/uncertainty по независимым episodes/cameras; соседние кадры не независимые samples. Scope/resolution/crop сравнивать на одной исходной exposure, с полным учётом пропущенной зоны.

**Артефакты:** license+source snapshot manifest, actual bytes hashes, actual merged config/load log, split lineage+near-duplicate audit, FN gallery с original/preprocessed view, per-image raw predictions и full event ledger, accepted thresholds/selection history, exposure/updates/wall/VRAM logs, target compiler/parity/operator placement и latency traces. Предварительно команда задаёт абсолютные acceptance floors и meaningful-gain budget; здесь численных порогов нет.

| Наблюдаемый будущий исход | Изменение решения |
|---|---|
| Ошибки следуют pixel-loss; B улучшает нужный recall при FP/latency floor | Приоритет spatial/data ветке; C откладывается |
| Изображение видимо/метки полны; C даёт устойчивый gain на independent groups после conversion | Продвигать конкретный C bundle; не всё семейство и не COCO ranking |
| C лучше reference, LinQ graph/precision/latency не проходит | C offline research/teacher; для финального пути блокируется до исправления |
| Не хватает независимых positives либо интервалы слишком широки | Нельзя объявить победу; сохранить простой прошедший bundle и расширять evidence |
| Все пути не видят закрытый предмет | Уточнить visibility/scenario contract; не учить отсутствие PPE из невидимости |

Успех не доказывает распознавание phone-use по одному phone bbox, безопасность всех камер/цехов, приемлемость всех upstream прав, cross-camera generalization сверх split, память любого3090, переносимость иных heads/opsets либо adequate few-second latency при большей нагрузке.


## F172 — W2-C: Передачи и точные незакрытые вопросы

- Происхождение/locator: [W2-C](_WORK/W2_C.md), раздел «Передачи и точные незакрытые вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- **Root/product/license:** принять конкретный способ AGPL поставки, не считать YOLOX автоматически очищенным fallback. Для D-FINE выбрать HF pinned asset как источник с stronger explicit scope; требуется actual byte verification и notices. Применимость upstream terms к предполагаемому использованию не решена этим отчётом.
- **W2-B/training stack:** YOLO S init есть O365; записать это в manifests. D-FINE native constructor скачивает B2 даже до tuning; нужна явная resolved init chain. Paper/native schedules не смешивать; short recipe не равна author benchmark.
- **W2-A/recovery:** в пространственном A/B сравнениях automatic batch/NaN recovery также меняет trial. Логировать actual exposure и fail/fork policy.
- **Data/evaluation:** actual input-size/visibility slices; per-class completeness и association. Камера/сцена/эпизод и parent frames/crops отделены между independent splits; no neighboring frames, no identical scenes/cameras при cross-camera claims. Public pretrain contamination полностью исключить нельзя.
- **LinQ/video:** spatial policy — изменение общего workload. Проверить каждый neural crop-stage на LinQ, actual head и постпроцессинг; не переносить T4/V100 latency. Калибровка геометрии и quantization остаются отдельным handoff.


## F173 — W2-D: Решение и изменение ближайшего шага

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Решение и изменение ближайшего шага»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S255, S256, S257.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F173 [решение].** При отсутствии инвентаризации видео команды стартовать с одного условного scope: **наблюдаемое лежачее состояние человека в фиксированном ракурсе, одно уведомление на продолжающийся эпизод**. Не обещать «падение», «неподвижность» или «потерю сознания» по одной лежачей позе. Первое исследование — pretrained frontend + причинная логика, без нового обучения. Для разрешённого некоммерческого академического feasibility есть конкретная пара URFD `fall-01-cam0.mp4` / `adl-01-cam0.mp4`, однако её содержимое и event labels ещё надо проверить. При непринятом NC-режиме этот маршрут не объявлять разрешённым: переключить первый scope на **вход/нахождение человека в пользовательском полигоне** только после получения разрешённого видео команды. Геометрический полигон — операционное правило, не доказательство физической опасности.

**F173 [новый ограничивающий факт].** CAUCAFall v5 имеет полезные fall/no-fall segmentation labels и CC BY 4.0, но авторы прямо описывают **motion-triggered DVR recording**. Следовательно, даже все его клипы вместе не являются непрерывной записью рабочего фона. Нельзя восстановить negative camera-hours из количества PNG или заявленной частоты камеры. Конкретный AVI не получен: web-страница открывается, Python/API получает 403. Это резерв для размеченных состояний/объектов, а не готовый production event benchmark. [S256]

**F173 [новое наблюдение].** У точного URFD `fall-01-data.csv` получено 160 строк: номера 1…160, время 0…5305 ms, соседние разности 33/34 ms. Это **5.305 s между первым и последним timestamp**, не измеренная длительность падения или лежания, не FPS видеодекодера. Длинную выдержку вроде 10 s этот временной ряд уже не поддерживает; для короткой выдержки нужно отдельно проверить наблюдаемый post-state и EOF. CSV не даёт права заменять PTS MP4 равномерной сеткой: связность двух представлений ещё не проверена. [S255, S257]

**Что меняется:** training queue пока не получает новый разрешённый и полностью размеченный object package. Зато ближайшая работа становится конкретной: принять use scope; получить/просмотреть одну точную пару; создать frame-to-time mapping и несколько event labels; реализовать таблицу ниже на oracle observations; затем проверить frontend. Не ждать сотен событий для feasibility и не считать эту пару независимым подтверждением качества.


## F174 — W2-D: Происхождение исходного замечания и статус K

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Происхождение исходного замечания и статус K»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Исходная критика сохранена в `CRITIC.md`, контроль 2026-10-23 20:25:26 Moscow, разделы K005/K006/K007/K011; история первой волны не переписана. Прочитаны назначенный `PROMPT_W2_D.md`, релевантные контракты `W1_01/04/07/09/11.md`, `CASE_NOTES.md`. Secondary leads: соседний behavioral `_WORK/W1-09.md` (URFD, CAUCAFall, точные границы доступа и различие lying/fall) и datasets `_WORK/W2-08.md`; они используются как указатели, а не как новые собственные измерения. Проверены только **два primary data sources**, URFD и CAUCAFall; полный каталог не повторялся.

| K и исходная проблема | Статус этой ветки | Что закрыто / что осталось |
|---|---|---|
| K005: нет выбранного реально доступного data package | **Применимость уточнена; prerequisite остаётся открытым** | Есть exact obtainable URFD pair + timing CSV и конкретная CAUCAFall граница. Нет подтверждённых rights выбранного use, decoded mapping, event labels и private/team inventory. Training-ready package не заявлен |
| K006: SELECT/CAL/TUNE/CHECK имеют разные роли | **Предложен единый минимальный контракт; принятие сборщиком открыто** | train/DEV/lockbox; optional SELECT только для заранее frozen pipelines. В нынешней паре нет достаточного lineage для независимых частей, значит только DEV feasibility |
| K007: нет короткого causal acceptance входа | **Спецификация закрыта; исполнение открыто** | Ниже 10 изолированных fixtures, единицы времени, ожидаемые counts, phase replay. Ни fixture runner, ни реальные episode labels ещё не созданы |
| K011: нет узкого маршрута при незакрытых gates | **Data-часть уточнена; общий маршрут открыт у сборщика** | A: pretrained/rules; B: fine-tune только после labels/runtime; C: challenger deferred. Owners/cutoff/reserve не выдуманы |


## F175 — W2-D: Два проверенных источника: что именно доступно

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Два проверенных источника: что именно доступно»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S255, S256, S257, S258.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**S255.** Michal Kępski / University of Rzeszow, [UR Fall Detection Dataset](https://fenix.ur.edu.pl/~mkepski/ds/uf.html). Версия страницы не указана; связанная авторская статья Kwolek/Kępski — December 2014. Доступ 2026-10-23. Локаторы: вводное описание, synchronization paragraph, license, Fall row 01, ADL row 01, Extracted features. Вид: primary dataset documentation. Коротко: 30 fall/40 ADL sequences; два вида fall и один ADL; отдельные PNG streams; время в ms от начала sequence, независимые камеры сведены ближайшими timestamps. Разметка posture в depth-derived features имеет отдельные лежит/не лежит/переход. Это не RGB bbox/track/онлайн-event GT. Условия: CC BY-NC-SA 4.0, academic/noncommercial scope; commercial use требует отдельного согласования с авторами, контактов не было. Сохранён оригинальный HTML, SHA256 `cb6d171be52c086ece579457b9ee752abb25e335b12aae25ee28714fb94aae83`. Обобщение на industrial камеры и разрешение конкретного конкурсного режима не установлены.

**S256.** Jose Camilo Eraso, Elena Muñoz, Mariela Muñoz, Jesus Pinto, [Dataset CAUCAFall v5](https://data.mendeley.com/datasets/7w7fccy7ky/5), DOI **10.17632/7w7fccy7ky.5**, опубликован **18 March 2025**. Доступ 2026-10-23. Локаторы: Description paragraphs 2–4; Steps to reproduce paragraphs 1–2; Licence. Вид: versioned primary dataset card. Коротко: subject/activity folders, AVI/PNG/TXT, manually labeled fall/no-fall segmentation; CC BY 4.0. Камера nominal 23 FPS, 1080×960; это описание capture, не проверка каждого AVI. DVR начинает motion-triggered запись при входе. Камера/incident/session lineage, event onset/observable и negative exposure ещё требуют просмотра/manifest. Синхронного primary file list/конкретного видео не получили. Web open успешен; независимый `urllib` page/API 403, отражено в `fetch.json`. Наличие repository card не приравнено к скачанному архиву.

**S257.** URFD, [fall-01-data.csv](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-data.csv), малый первичный synchronization artifact, revision отсутствует. Доступ 2026-10-23; HTTP 200, 2466 bytes; SHA256 **60e156223725e401155b4fd25a672c498ed5b4e17897337c6971d90041818bcc**. Локатор: все 160 строк, столбцы frame/time/accelerometer, смысл по S255. Собственная read-only проверка CSV, без медиадекодирования. Сохранён `urfd_fall01.csv`; вычисленные границы в `observations.json`. Acceleration не подаётся как RGB-признак и не считается event label.

**S258.** Exact URFD asset metadata: [fall-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4) и [adl-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4). Собственный HEAD 2026-10-23: оба 200 `video/mp4`, Content-Length соответственно **1,299,104 / 1,194,846 bytes**, Last-Modified 2020-02-25 17:13:37 / 17:13:38 GMT. Header metadata сохранено, full-byte SHA и decode отсутствуют. Дата mtime файла — не дата записи инцидента. MP4 являются удобными кандидатами; original PNG+CSV предпочтительны, если MP4 не сохраняет соответствие исходному времени. У всех производных одной sequence один parent incident group.


## F176 — W2-D: Label/readiness/missing matrix

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Label/readiness/missing matrix»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S258.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F176 [синтез].** Разделить два пакета. Object fine-tune требует exhaustive labels именно выбранных train classes и ignore policy. Event evaluation требует непрерывного времени, event identity, observability, negatives и дедлайна. Один пакет не возникает автоматически из другого.

| Сценарий / asset | Object fine-tune input | Event evaluation input | Готовность / минимально недостающее |
|---|---|---|---|
| **Приоритет: лежачее состояние**, URFD exact pair S258 | RGB есть по указателю, person/lying bbox или pose GT не подтверждены; depth features не substitute | Synchronization CSV подтверждён только fall-01; ADL candidate есть. Onset/observable/end/ID/negative intervals отсутствуют | **Obtaining/reannotation required**; принять NC use, получить exact pair, декодировать и проверить mapping; вручную описать состояние, negative и censoring. Только feasibility |
| Fall transition, те же assets | Object bbox не задаёт переход | Sequence fall class не локализует onset и не доказывает distinguishability до deadline | Не стартовый claim; потребуется переходная разметка и matched intentional lying/bending controls. Нельзя переименовать lying alert в fall detection |
| Fall/lying, CAUCAFall v5 | Существуют per-frame segmentation fall/no-fall по card; для person bbox нужен проверенный конвертер и полнота; исходная семантика fall может смешивать переход/позу | Есть action AVI по card; точных доступных файлов и PTS не получили. ADL task clips не равны background camera-hours | **Reserve**, exact acquisition/rights notice/annotation manual/границы ещё missing; nominal FPS не использовать как проверенный timebase |
| **Зона / длительное нахождение**, разрешённый team video | Pretrained person detector может дать первый inference без fine-tune; train labels нужны только после error audit | Нужен реальный static-camera clip с entry/stay/exit, inside/outside controls, затем второй actor | **Team asset unknown**. Ни выбранные public clips, ни case p8 не подтверждают наличие команды. Если есть файл — меньше specialist dependencies, допустим fallback priority |
| Долгая неподвижность / unconsciousness | Лежачие labels недостаточны | Нужны fresh input, видимое motion/unknown и реальная длительность нужного hold; сознание часто не видно | **Out of first scope**; нельзя расширять клип повторением последнего кадра |

Полей private data не заполняли догадкой. Для владельца данных нужны ответы: exact files и права использования; камера/сессия/исходный parent; положительные и полные обычные интервалы; timestamp/FPS/provenance; известные trims и перезаписи; exhaustive label coverage. При недоступности ответов статус остаётся `unknown`, не «достаточно negatives».


## F177 — W2-D: Минимальный реальный development corpus и ручная работа

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Минимальный реальный development corpus и ручная работа»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S258.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F177 [предлагаемый пакет D0].** Не квота для статистической достаточности. Сначала достаточно собрать **один видимый positive эпизод + один контрастный negative**, затем добавить **один episode с окончанием/повторным входом и один с двумя людьми**, если доступные/разрешённые файлы это содержат. Отсутствующий case честно остаётся synthetic-only coverage. Для лежачего scope первый exact positive candidate S258 и его ADL pair ещё должны пройти review; ADL-01 не объявлен заранее hard negative «намеренно лёг». Если он не контрастен, не подменять его содержимое названием файла, выбрать другой ADL после просмотра.

Не требовать всех четырёх реальных эпизодов до первого frontend feasibility. Но первая пара проверяет лишь работоспособность пути, а не rearm/identity, quality или factory FP rate. Ни длительность доступных negative intervals, ни число независимых subjects/камер в выбранной паре пока не установлены. Независимость между fall-01/adl-01 также не предполагается.

Минимальная инструкция annotator:

1. Сохранить original bytes/hash/source/license; для каждого кадра index, original timestamp/timebase и decoded PTS. Для PNG использовать documented CSV mapping только после сверки номера/пропусков. `timestamp_origin` отличает camera/sync metadata от derived CFR. Не считать MP4 PTS временем физической экспозиции без основания.
2. Просмотреть исходный эпизод целиком. Разметить `actor_gt_id`, интервал наблюдаемой лежачей позы, `onset_bounds`, `first_observable`, `end_bounds`, `unknown/occluded`, left/right censor. Для зоны — polygon/rule version и anchor convention. При неоднозначности сохранить interval/ignore, не заставлять annotator угадывать причину.
3. Все рассматриваемые интервалы пометить `positive / verified_negative / unknown / out_of_scope`; сохранить полноту review `(class,interval,ROI)`. Проверить всех людей в ROI, а не только найденного моделью. Negative clip допустим только для этого observable scope, не для всех нарушений.
4. Для first frontend run bbox/pose dense GT необязателен: event annotations и несколько hand-reviewed failure frames достаточны для diagnosis. Для fine-tune отдельно полностью разметить выбранные train frames/instances и все обучаемые классы. Не писать пустые label files на partial data.
5. Второй человек проверяет границы и спорные labels; разногласия решаются до сравнения. Записать reviewer/version; не строить GT из output оцениваемой модели. Все crops/windows/sampling variants наследуют parent split.

Минимальный manifest: `asset_id, source_url, original_hash, rights_status, parent_incident, camera, session, subject_if_known, lineage_confidence, split_role, native_time_kind, timebase, pts_mapping_status, label_version, exhaustive_scope, eligible_negative_intervals, unknown_intervals`. Поля unknown разрешены, но ограничивают claims. Для события: `gt_event_id, scenario, actor_gt_id, onset_lo/hi, observable, end_lo/hi, censor_reason`. Для production timestamp bounds отдельная передача runtime-ветке.


## F178 — W2-D: Один протокол data roles вместо семи обязательных subsets

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Один протокол data roles вместо семи обязательных subsets»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F178 [согласование K006].** Основной вариант **train / DEV / lockbox** по lineage. CAL/TUNE/CHECK не создавать как обязательные физические части на нынешней паре. Если выполняется только pretrained feasibility, train пуст и оба clips имеют роль DEV; независимого lockbox результата пока нет.

| Решение | Допустимая роль | Лимит/варианты на старте | Статус после просмотра |
|---|---|---|---|
| Ручная семантика/ошибки, threshold, dwell/gap, model/checkpoint choice | DEV | Один incumbent; одна заранее описанная policy alternative после найденной ошибки | Development, результаты exploratory; все просмотры/изменения в ledger |
| Fine-tune weights | Train, validation внутри DEV | Только один B0 после data/runtime gate; ablations решает сборщик | Labels и gradients никогда из lockbox; смена recipe — новый artifact |
| Calibration | DEV либо отдельные grouped DEV folds при достаточных группах | В первом scope отсутствует | Fitted data не становятся independent CHECK |
| Выбор законченного pipeline | Optional SELECT, только при оставшихся независимых группах | ≤2 готовых frozen pipelines, без настройки по результатам | После просмотра selection data. Если меняются threshold/rules — tuning data |
| Независимая оценка | Lockbox после freeze одного artifact | Один frozen pipeline, одна planned evaluation | После использования для исправлений это новый DEV; нужны новые группы для новой независимой проверки |
| Refit train+DEV | Только после отдельного решения | Не назначен на старте | Новая identity; прежний test не подтверждает автоматически новый artifact |

Внешнее разрешение pretraining exposure проверить по weight provenance соседней ветки. Камера не становится unseen из-за другого номера клипа. URFD cam0/cam1 одного падения всегда одна incident group; возможный общий actor/scene между fall и ADL исключает сильное unseen-scene заявление. CAUCAFall subject folders — полезный уровень, но десять subjects не означают десять независимых камер. Пока grouping не установлен — не делить кадры случайно. «Мало групп» ведёт к DEV feasibility, а не к четырём псевдонезависимым частям.


## F179 — W2-D: Малый synthetic event-ledger acceptance corpus

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Малый synthetic event-ledger acceptance corpus»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F179 [спецификация, не выполненный тест].** Fixtures проверяют evaluator и FSM, **не detector quality**. Единицы — секунды source timeline с отдельной `available_at` replay timeline. Все числа ниже искусственные test constants, не промышленные dwell/deadline. Для простоты known identity A/B и один camera epoch; правила и ожидаемые результаты одинаковы для lying-state и zone-state через абстрактный `positive` input.

Контракт fixture v0: deadline `D=2.0` от GT onset; граница включительна. Event interval полуоткрытый `[onset,end)`. ACTIVE достигается после двух свежих положительных observations с `t2-t1>=0.5` и без positive gap `>0.75`; unknown обрывает candidate support, но ACTIVE не rearms. Fresh negative observations, покрывающие 1.0 s с gaps ≤0.75, заканчивают ACTIVE и разрешают rearm. Каждый observation имеет уникальный source ID; дубли и extrapolated stale bbox не дают support. Сначала oracle ledger отдельно тестирует matching, затем FSM из observations должен породить ожидаемый production ledger. Emit time — реальное время решения, не время первого positive.

Matcher: применить W1-01 one-to-one maximum cardinality по class/camera/GT actor и допустимому времени, сначала максимизировать число timely matches, затем минимизировать суммарную задержку, затем lexical `(gt_event_id,alert_id)`. Неверный actor не match. Additional alert той же продолжающейся GT ситуации — duplicate, не второй TP; alert без подходящего GT — semantic FP. Для тестов late допускается до end эпизода; позднее end+grace **не допускается**, grace=0 в fixture v0. Публиковать timely/late/missed/duplicate отдельно, поздний alert оставляет deadline miss. Ниже scenarios изолированы, их clocks не складываются в один stream.

| Fixture | GT / input / output ledger | Ожидаемый результат |
|---|---|---|
| C01 timely + boundary | A `[1,8)`; fresh positives 1,1.5 → emit1.5. Отдельный evaluator boundary variant emit3.0 | 1 timely TP; boundary также timely. Нет backdating emit к1 |
| C02 late | Тот же GT; oracle alert3.01, causal decision3.01 | timely0; late1; deadline miss1; eventual matched1. Не semantic FP |
| C03 duplicate ongoing | A `[1,8)`; alerts1.5 и2.0 A | timely1, duplicate1; production FSM обязан emit только1.5 |
| C04 two actors | A `[1,8)`, B `[2,7)`; positives A1/1.5, B2/2.5 | Два timely alerts1.5/2.5, global cooldown не глушит B |
| C05 rearm | A event1 `[1,3)`, negatives3/3.5/4, event2 `[5,8)` positives5/5.5 | Два разных event UUID и два timely alerts; negative support подтверждает rearm |
| C06 ID split | GT A `[1,8)`; track x1/x2 принадлежат A, identity bridge доступен causal к2; positives1/1.5, затем track x2 в2 | 1 alert; смена track ID не создаёт новое событие и не очищает emitted flag |
| C07 ID merge | GT A `[1,8)`, B `[2,7)`; raw tracker объединяет IDs, resolver получает `ambiguous` | Не присваивать B доказательство A. Если B не восстановлен к4, B deadline miss; один alert не match двум GT. Не выдумывать oracle bridge для production |
| C08 unknown gap | A `[1,8)`, candidate positive1, unknown1.2…3, fresh positives3/3.5 | emit3.5, late1/deadline miss1. Unknown не подтверждает dwell. Variant после ACTIVE: unknown не rearm и не создаёт дубль при возврате A |
| C09 short between samples | A `[1.1,1.4)`, samples1.0/1.5 negative; complete readable source GT известен | timely0, missed1; sampling miss остаётся E2E miss. Positive duration0.3 s не расширять до next sample. FSM baseline может также не поддерживать столь короткое состояние — это явная граница scope |
| C10 EOF censor | A starts7, EOF8, deadline9, no alert | right-censored1; исключён из timely denominator по predeclared rule, не timely/обычный FN. Variant starts5.5, EOF8 (deadline7.5 уже прошёл) → missed1, не censored |

Дополнительный boundary в C08: когда GT неизвестен в gap, интервал `unknown` не добавляется к verified negative exposure; нельзя назначить FN реального события без независимого GT. При ID merge corpus знает две GT identity, а production input может оставаться ambiguous: этот fixture проверяет честный пропуск, а не обязательное «идеальное восстановление». Для tie-policy отдельная перестановка входных alert rows не должна менять итог.

Критерий приемки logic: точное совпадение counts, UUID/rearm/causal cutoff и censor flags всех fixtures; любое несовпадение блокирует сравнение thresholds. Артефакты будущей реализации: `fixtures.json`, `expected_ledger.csv`, `actual_ledger.csv`, matcher/FSM config hashes и diff. В этой ветке это **табличная спецификация**, не созданный/пройденный runner.


## F180 — W2-D: Replay на реальном времени и различающий эксперимент

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Replay на реальном времени и различающий эксперимент»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**W2-D-E01 — вопрос:** поддерживает ли выбранный видимый lying-state и причинное подтверждение нужную своевременность на доступных коротких real episodes, или наблюдения/выдержка делают scope неработоспособным ещё до обучения?

Входы: принятые rights выбранной exact pair, полностью decoded frame/PTS mapping, ручные episode labels, pretrained frontend разрешённого deployment bundle, один fixed immediate baseline и одна FSM policy. На начальном oracle этапе frontend не нужен; LinQ нужен позже для deadline, не для проверки matcher.

1. Пройти synthetic logic acceptance. Затем проиграть **oracle real observations** на исходной frame/time grid, используя только префикс. Проверить, есть ли физически наблюдаемый support до EOF/deadline. При отсутствии нужной длительности не тюнить «лучший hold» на обрезанном файле: укоротить заявленный scope или получить продолжение/другой episode.
2. Зафиксировать sampler period `Δ` как экспериментальный параметр, а не universal min FPS. Для каждого интересующего Δ использовать несколько равномерных фаз `φ∈[0,Δ)`; выбрать первый доступный исходный кадр с timestamp ≥ `φ+kΔ`, не дорисовывать кадры. Для коротких событий дополнительно включить фазы сразу по обе стороны onset/end. Дедуплировать повторно выбранный frame ID. Все phase variants одной sequence — один statistical group.
3. Выполнить causal replay frozen frontend observations: native grid против subsampling; immediate policy против FSM. Логировать число **различных свежих** observations до deadline, timing support, observable/censored events, phase-specific misses, late/duplicate alerts и eligible negative seconds. При oracle успехе, но frontend провале — диагноз модели; при обоих провалах — семантика/schedule/hold, fine-tune не первый ответ.
4. После DEV freeze — отдельный **wall-clock LinQ run** с тем же decode/scheduling/delivery, traces `source_pts, available_at, inference_end, decision, emit, receive`. Cached replay не доказывает deadline. Метрики actual throughput/capture delay не подставлять из nominal source FPS. При отсутствии capture mapping назвать задержку replay-to-receipt, а не glass-to-alert.

Метрики: поэпизодные timely/late/missed/censored counts; duplicates и wrong-actor; per-phase sensitivity; fresh observations к deadline; unknown/stale intervals; реальные negative seconds. На этой малой curated pair FP/hour — лишь описательная частота на известных reviewed интервалах, **не factory rate**; если таких интервалов ещё нет, rate `N/A`. Не публиковать p95 по нескольким событиям как устойчивый tail estimate. Native timestamps и duration distribution реальных нарушений, кроме исследованного metadata span, пока unknown.

Артефакты: hash exact media/labels/manifest, mapping table, phase schedules, oracle/frontend observation caches с provenance, full GT/alert ledgers, trial/view ledger, paired diagnostic report, LinQ trace отдельно. Результат успеха — исполнимость конкретного causal пути на этих эпизодах. Он не доказывает detector accuracy в цехе, unseen camera generalization, fall cause, сознание, private deployment prevalence или LinQ performance иной конфигурации.


## F181 — W2-D: Узкий маршрут, stops и передачи

- Происхождение/locator: [W2-D](_WORK/W2_D.md), раздел «Узкий маршрут, stops и передачи»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F181 [предлагаемый data route для K011].** A: права/asset check → labels/time mapping → oracle acceptance → pretrained real replay → LinQ run → freeze. Это может завершиться demo feasibility без обучения. B: только если frontend errors подтверждены человеком, есть exhaustive train labels с независимым DEV, выбран совместимый stack и пройдены runtime gates, разрешить один fine-tune. C: challenger, второй specialist, calibration, расширение сценариев и вторая GPU остаются deferred до готового A/B и реально измеренного резерва. Эта ветка не разрешает аренду и не оценивает часы.

Stop rules: нет разрешённого media — продолжать synthetic logic и private inventory, не заменять реальный результат; нет timestamp mapping — event-time claims отложить; нет independent groups — feasibility/DEV claim; нет continuous negatives — industrial FP/hour не заявлять; нет LinQ inference/speed — не считать case requirement закрытым. Если короткое lying-state не различимо от intentional lying, сохранить observable state label или сузить scope, а не автоматически брать более крупный detector. Новые hypotheses прекращаются при общем cutoff сборщика; обязательные LinQ/submission reserves не съедаются optional data search.

Точные handoffs:

- **Сборщику/root:** принять один первый scope и role table; назначить владельца team asset inventory и annotator/reviewer. Не открывать SELECT/lockbox только ради красивого количества subsets; теперь доступен конкретный obtaining/reannotation path, но production package отсутствует.
- **W2-A/W2-F runtime:** добавить к их минимальным traces source/available/decision/received timestamps, repeated-frame freshness, camera epoch и identity ambiguity; cache replay отделить от LinQ wall time.
- **Weights/stack-веткам:** pretrained route потребляет конкретный разрешённый artifact; отсутствие fine-tune не отменяет license/export/Neural-on-LinQ gates. CAUCAFall segmentation classes не автоматически равны detector ontology.
- **Evaluation/FSM:** принять включительную deadline boundary, half-open event intervals, one-to-one tie rule и censoring; при другой policy обновить expected fixtures до запуска, не после результата.

Остающиеся вопросы с владельцами, которые интернет не закроет: права конкретного конкурсного use URFD (root/use owner); exact team videos, lineage и отрицательные интервалы (data owner); scenario deadline и выбранная семантика состояния (product/evaluation owner); supported LinQ frontend и реальная частота (runtime owner). Публичные источники дают стартовый путь и обнаруженные ограничения, но не подменяют ответы команды.


## F182 — W2-E: Решение и статусы критики

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Решение и статусы критики»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S259, S260, S262, S264, S267, S270.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F182.** Единственный конкретный initialization: **`timm/mobilenetv3_small_100.lamb_in1k`**, publisher HF revision **`1824797e7887cbec1990e4adbd6675960a36c589`**, код **timm v1.0.22**, SHA **`78c3724f4545c0067d0b4d2f7df6337196be01ce`**. Это карточка для будущего supervised fine-tune компактного crop classifier, **не готовый verifier нарушений**. Сохранять условно; **не включать в первые baseline runs** и не делать обязательной стадией MVP. Переходить к нему лишь после доказанного остаточного типа ошибок на видимых, пригодных crops и данных для обучения. Generic ImageNet-1k initialization не распознаёт автоматически наши `phone_use`, `fall`, `no_helmet` события. [S259–S264]

**F182.** Neural temporal branch **defer**. Для ближайшего запуска достаточно выбранного detector stack W2-B + причинной CPU-логики/FSM W1-04. Одна контрпроверка TSM показывает, почему брать произвольные video weights опасно: обычный `ops/temporal_shift.py` использует будущий timestep, тогда как online-demo имеет другой модуль, внешний state и Jester checkpoint. Это не взаимозаменяемые causal/offline recipes. Полного behavior survey, второй temporal модели и KD/ensemble здесь нет. [S267–S270]

**F182.** Найдено реальное противоречие лицензирования: точная HF model card обозначена `apache-2.0`, но pinned timm README для авторских ImageNet weights просит предполагать применимость исходной лицензии dataset. Поэтому итог по выбранным весам — **`unresolved`**, а не «все веса Apache». Код — Apache-2.0; доступность asset документально подтверждена HEAD, target ability и разрешённость конкретной формы поставки этим не подтверждены. [S259,S260,S262]

| K | Исходная критика, provenance | Статус этой волны |
|---|---|---|
| **K008** | `CRITIC.md`, P1: verifier назван без family/checkpoint/trainer; temporal shortlist — архитектуры, а не воспроизводимые online weights | **Закрыто документально в предусмотренном заданием объёме:** один pinned initialization, trainer/input/classes/export/state/data contract; обоснованный defer temporal. Практическая пригодность V остаётся открытой. Исходное замечание было справедливым, не исправляется задним числом |
| **K003, specialist** | `CRITIC.md`, P0 до передачи/распространения: code license недостаточна для checkpoint/backbone | **Применимость уточнена, не закрыто:** exact model card + asset metadata/HEAD найдены, но retained conditional weights имеют конфликт model-level designation/project notice. Разрешение условий и hash полученных байтов остаются gate; detector часть — W2-C |
| **K009, V/T boundary** | `CRITIC.md`, P0: исторический LinQ путь не доказывает работу всех neural nodes; neural CPU boundary неизвестен | **Уточнена граница:** V отсутствует в первом baseline, T отложен; при добавлении V требуется отдельный LinQ pass. Actual SDK, CPU policy, compile/parity/concurrency остаются открытыми у W2-F/организаторов. Здесь K009 не объявляется закрытым |

Прочитаны исходное назначение и релевантные части CRITIC, W1-02/03/04/10/16, CASE_NOTES; ограничения кейса переданы через визуальные наблюдения root, без собственного повторного просмотра PDF. W2-B использован как handoff выбранного envelope, не как собственный выполненный smoke. W2-D пока не подменяется предположением о наличии пригодной разметки.


## F183 — W2-E: Карточка единственного crop кандидата

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Карточка единственного crop кандидата»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F183. Зачем именно такой initialization.** Узкая проверяемая гипотеза — уменьшение ошибок различения *видимого* головного СИЗ и визуально похожих головных уборов/фона на detector-generated head/upper-body crops. Это будущий вариант для остаточных FP, а не доказанный dominant error: K005 требует сначала error atlas. Если главная причина FN — нет proposal, голова невидима или мало исходных пикселей, V не исправляет её; увеличение до 224² не создаёт деталей. При отсутствии пригодного crop или условных меток отказаться от V. Полный person crop может сделать голову слишком малой; crop schema должна быть зафиксирована до обучения.

| Поле | Точный контракт / степень готовности |
|---|---|
| Architecture/code | `mobilenetv3_small_100`; timm v1.0.22, SHA выше; commit date **2025-11-04T23:15:00Z** из GitHub API. Это выбранный release, не latest claim |
| Publisher/model revision | `timm/mobilenetv3_small_100.lamb_in1k@1824797e7887cbec1990e4adbd6675960a36c589`; HF createdAt **2022-12-16**, lastModified **2025-10-19T16:12:11Z**. Даты репозитория не являются датами обучения |
| Exact asset | `https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/resolve/1824797e7887cbec1990e4adbd6675960a36c589/model.safetensors` |
| Asset metadata | HF API: **10,241,912 bytes**; LFS SHA256 **`46d2c063b18125884c48937afa4c49e18128869e52e8db96df48bf0a4d7ff697`**. HEAD после redirect: HTTP200, `application/octet-stream`, `content-length: 10241912`, filename `model.safetensors`. Содержимое/тензоры не проверены. CDN ETag отличается и **не подменяет** LFS SHA256 |
| Alternate file | В том же repo есть `pytorch_model.bin`; он **не выбран**. Не переключаться молча: другой file/hash. Старый `.pth` URL в timm registry тоже не выбран |
| Pretraining lineage | Model card: ImageNet-1k, обучение в timm; LAMB recipe, EMA, без CutMix, ступенчатый exponential schedule с warmup. Это описание template, не полный exact historical command. Дополнительный action dataset не заявлен; начальные 1000 logits относятся к ImageNet |
| Compactness | Model card сообщает округлённые **2.5M params / 0.1 GMAC / input224²**. Это свойства авторской карточки, не наш VRAM/latency result и не прогноз fit на 24GB |
| Source input | FP32 NCHW RGB `[B,3,224,224]`, `/255`, mean `(0.485,0.456,0.406)`, std `(0.229,0.224,0.225)`; bicubic; crop_pct **0.875**, center crop. Стандартный eval transform: shorter side256 → center224 для квадратного target. CPU crop/resize/normalize **снаружи** neural graph |
| Original classes/output | `num_classes=1000`, `num_features=1024`, classifier `classifier`; output `[B,1000]` logits; softmax — отдельный postprocess. Это не target event schema |
| Target head, наш проект | Предлагаемые взаимоисключающие crop labels: `helmet_visible`, `bare_head_visible`, `unassessable`. Точный порядок в mapping.json. Новый classifier `num_classes=3`, CE; head переинициализируется. `unassessable` означает abstention/неполное наблюдение, а не подтверждённое отсутствие СИЗ. Это **наша будущая разметка**, не классы исходных weights |
| Temporal state | У eval crop model нет temporal buffer, hidden state или зависимости от следующего crop. BatchNorm running statistics — параметры inference, не per-track memory. `model.eval()` обязателен; train mode меняет поведение и контракт |
| Reset | Neural per-track reset не требуется. Внешние cached crop/score и FSM обязаны иметь `(camera, stream_epoch, track_id, generation)`, PTS и TTL; reset при ID reuse, reconnect, seek, большом gap, смене crop/model schema. Это проект приложения, не встроенный timm reset API |
| Deployment | Только условный второй graph; native ONNX exporter есть, но **не LinQ exporter**. Device-unverified. Crop classifier может выполняться только в подтверждённом допустимом LinQ runtime path; CPU внутри сервера не объявляется автоматически разрешённым |

Для head crop не следует слепо center-crop удалить каску на краю. Сначала определить расширение crop и допустимые границы, посмотреть coverage на development set. Замена native eval geometry на letterbox/direct resize — отдельная согласованная train/eval/export recipe, а не «тот же preprocessing». Не использовать `phone visible` как label `phone use` или `lying` как label `fall`. Статичная фотография не задаёт причинный переход падения.


## F184 — W2-E: Лицензии, provenance и фактическая доступность

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Лицензии, provenance и фактическая доступность»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F184.** У publisher model card есть именно model-level Apache обозначение, поэтому одного отсутствия отдельного LICENSE в model repo недостаточно, чтобы автоматически запретить кандидата. Однако официальное противоположное замечание maintainer в том же выбранном code release нельзя игнорировать. Здесь не делается общий юридический вывод о любых ImageNet weights: фиксируется конфликт первичных утверждений выбранного publisher.

| Компонент | Evidence | Классификация | Следствие |
|---|---|---|---|
| timm source SHA | LICENSE Apache2.0, copyright Ross Wightman2019; README §Code | **explicit grant (code)** | Сохранить LICENSE, attribution и notices применимых файлов; отметить собственные изменения |
| Exact HF weights repository | Pinned README YAML `license: apache-2.0`, training dataset ImageNet-1k | **explicit model-level license designation**, но не безусловный итог | Сохранить exact card/revision вместе с весами; не выдавать code LICENSE за единственное основание |
| Те же авторские ImageNet pretrained weights | Pinned timm README §Pretrained Weights, строки744–745 локальной копии | **project-level limiting claim** | Сопоставить с model card; выяснить применимость к выбранной исследовательской/демонстрационной/redistribution форме использования до передачи bundle |
| Итоговый выбранный checkpoint | Два предшествующих официальных свидетельства одновременно | **unresolved** | Не называть permissive-cleared; conditional research candidate. При невозможности разрешить условия — оставить baseline без V; не добавлять вторую непроверенную модель ради замены |
| Target crops/labels | Ещё не получены этой веткой | **unresolved** | W2-D: права, происхождение и независимость split; model card не лицензирует target video |

Точный model repo содержит README/config/два формата weights, отдельного LICENSE/NOTICE API не перечисляет. В timm root `NOTICE` ответил404; это только наблюдение выбранного пути, не доказательство отсутствия notices в dependencies. Доставка будущего V должна включать code LICENSE, pinned model card/config, source revisions, asset hash, сведения о target annotations и перечень модификаций. Для artifact retrieval требуется вычислить hash фактически полученных байтов и проверить совпадение с metadata, затем проверить load/key mismatch; **ничего из этого сейчас не выполнено**.


## F185 — W2-E: Trainer и точная граница export

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Trainer и точная граница export»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S263, S264, S265, S266.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F185.** В этом release есть официальный `train.py`, а не только API архитектуры. Поддерживаются `--pretrained`, **`--pretrained-path`**, `--num-classes`, `--initial-checkpoint`, `--resume`. Для 1000→3 transfer использовать pretrained-path, не произвольный strict initial-checkpoint: `train.py` добавляет `pretrained_cfg_overlay.file` и `num_classes=-1`, builder удаляет несовпадающий classifier, helpers умеет читать `.safetensors`. Это зафиксированное source evidence, не проверенный load. Missing keys допустимы только для намеренно заменённой головы; неожиданные backbone keys — stop. [S263,S264]

**Предлагаемый supervised entrypoint, НЕ выполнен**, после license/data/export gates:

```bash
python train.py /LOCAL/CROPS \
  --model mobilenetv3_small_100.lamb_in1k \
  --pretrained --pretrained-path /LOCAL/model.safetensors \
  --num-classes 3 --input-size 3 224 224 \
  --train-split train --val-split validation \
  --smoothing 0 --mixup 0 --cutmix 0 \
  --config /LOCAL/approved_crop_recipe.yaml
```

`/LOCAL` — placeholder. Config обязана зафиксировать B, epochs/updates, optimizer, LR/schedule, seed, crop policy, augmentations, EMA/raw selection, eval selection и sampling весов классов; **числа не назначаются до target data и qualification**. Это конкретный trainer/init/loss contract, а не выдуманный полный готовый рецепт. `train.py` при smoothing=0, mixup=0, CutMix=0 и отсутствии JSD/BCE выбирает обычный CE. Взаимоисключающие три label требуют single-label dataset; stock `--bce-loss` сам по себе не делает папку single-label произвольным multilabel dataset. KD/teacher не нужны.

Source dependencies: Python>=3.8, `torch`, `torchvision`, `pyyaml`, `huggingface_hub`, `safetensors`, без узких pins в pyproject. Поэтому **не установленный lock**. Предлагаемый отдельный env наследует W2-B envelope: Linux/Python3.11.9, Torch2.5.1/vision0.20.1, train cu124; CPU export NumPy1.26.4/ONNX1.17.0/ORT1.20.1. Это выбранная совместимая по декларациям гипотеза, не испытанная комбинация. Не устанавливать timm extras в уже собранный detector env без constraints. Полный resolved lock, safe checkpoint load, forward/backward и 24GB fit остаются unrun.

**F185. Новая отрицательная находка в native exporter.** `onnx_export.py` создаёт `exportable=True`, eval по умолчанию, принимает checkpoint/num_classes/input_size, вызывает `timm.utils.onnx.onnx_export`. Но helper **всегда задаёт dynamic axis0** для input/output, даже без `--dynamic-size` и при `--batch-size 1`. CLI `--dynamic-size` относится к H/W, не отключает dynamic batch. Кроме того, `use_dynamo=False` выбирает ветку `torch.onnx.export`, но в самом вызове не передаётся `dynamo=False`; фактический default наследуется от Torch. Его нельзя считать универсальным legacy guarantee на произвольном новом Torch. [S265,S266]

В W2-B Torch2.5.1 envelope default legacy уже зафиксирован соседней веткой. Тем не менее для static1 LinQ probe нужен **небольшой записанный adapter**: `model.eval()`, `exportable=True`, FP32 dummy `[1,3,224,224]`; явные `dynamo=False`, `dynamic_axes=None`, `input_names=['input0']`, `output_names=['output0']`, `export_params=True`; выбранный compiler-supported opset; training EVAL; без ATen fallback и simplification. Не добавлять `--dynamo`: та ветка source использует отдельный старый `torch.onnx.dynamo_export`. Исходный helper checker проверяет структуру; optional forward comparator проверяет один случай до decimal3, а не target acceptance. Adapter/ONNX **здесь не созданы и не выполнены**.

Export boundary: normalized tensor → network → `[1,3]` target logits. Вне graph: crop geometry/color/normalization, softmax/abstention thresholds, cache/router, track association, event FSM, GUI. Никакого NMS, future frame или temporal state в V graph не требуется. Depthwise/group Conv, hard activation, squeeze-excite/global pooling требуют реального compiler probe; «стандартный CNN» не доказывает поддержку LinQ и отсутствие fallback. Quantization calibration/quality — handoff W2-F, без повторного общего PTQ/QAT обзора.


## F186 — W2-E: Единственная temporal контрпроверка: почему defer, а не фиктивный causal checkpoint

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Единственная temporal контрпроверка: почему defer, а не фиктивный causal checkpoint»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S267, S268, S269, S270.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F186.** На pinned TSM SHA `1f6a834b02120441d99fa706b7a13ccc5293c6fa` обычная `TemporalShift.shift` (локальный `TSM_shift.py`, L27–42) присваивает части output(t) каналы input(t+1). Следовательно, это bidirectional clip operation. Завершённое trailing window можно обработать без ещё не пришедших кадров, но тогда необходимо приписать результат концу окна и учитывать накопление/семантику window; нельзя объявить прежний timestep output доступным раньше будущего sample. Простая смена sampling не превращает этот checkpoint в frame-by-frame online initialization. [S267]

**F186.** Настоящий официальный online-demo есть: `online_demo/main.py::get_executor` загружает **`mobilenetv2_jester_online.pth.tar`**, `MobileNetV2(n_class=27)`, десять shift buffers; `InvertedResidualWithShift.forward` объединяет сохранённый прошлый buffer с текущими каналами и возвращает новую историю. Это причинный интерфейс `[frame, states] → [logits, next_states]`, отличающийся от clip-модуля. Jester gestures не дают target phone-use/fall способности. Code MIT не устанавливает автоматически отдельный grant внешнего `.pth.tar`. URL найден в source, бинарник/HEAD/weight hash намеренно не проверялся: **это deferred negative example, не второй retained initialization**. [S268–S270]

Дополнительная проблема интеграции: в compile example входные torch buffers нулевые, но live runtime `main` создаёт TVM buffers через **`tvm.nd.empty`**, а не явный zero fill. Нет реализованного per-track lifecycle/reset в показанном single-camera demo; есть отдельная история logits и ручной postprocess. Это статическое отсутствие гарантии zero-reset, **не наблюдённый runtime failure**. Модельный causal forward сам по себе не делает всю demo систему готовой для произвольных per-person streams. [S269]

Поэтому neural temporal **не включать в ближайшие runs**. Для возобновления ветки необходимы: подтверждённая ошибка FSM, которую различает именно порядок доступных кадров; independent untrimmed target clips с onset/end/visibility/background, ID и PTS; подходящий online training/checkpoint/license contract; объяснимые schedule/reset/gap semantics; compiler-supported state I/O; label contract, проверяющий тревогу к дедлайну вместо clip top1. Новый temporal search не назначается автоматически.


## F187 — W2-E: Один различающий эксперимент, сначала дешёвый отказ

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Один различающий эксперимент, сначала дешёвый отказ»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**Вопрос:** на оставшихся ошибках helmet scenario даёт ли этот один supervised V полезное снижение FP/camera-hour при сохранении timely event recall и несколькихсекундного дедлайна — относительно того же detector+FSM?

**Входы и ранний gate.** Зафиксированный baseline W2-B; developer video sessions/crops с исходными PTS и event/onset/visibility labels; источники и разрешения W2-D; согласованные B_FP, L_max, допустимая потеря recall δ/минимальный полезный gain Δ; SDK/SKU/operators и допустимое размещение neural V от W2-F. Значения и количество событий сейчас неизвестны, не заменяются обещанием «несколько сотен crops». До training сделать error atlas baseline: no proposal / head invisible / low resolution / wrong visible class / tracking / event rule / queue. Если нет существенной категории пригодных wrong-class crops, **остановить V без обучения**.

1. **Split до crop extraction.** Train/validation/optional SELECT/lockbox разнести по source session и заявленному уровню camera/site generalization. Соседние frames/crops/tracklets, GT и detector crops одного исходного видео не пересекают независимые split. Hard negatives извлекаются только из разрешённого train/development. Lockbox не используется для порогов, crop margin, checkpoint, route или выбора гиперпараметров.
2. **Oracle ceiling до V.** На development оценить долю GT events с пригодным и своевременным detector crop и отличимым helmet state. V не спасает события вне этой доли. Сравнить идеальные GT crops и реальные detector crops отдельно; качества на GT crops недостаточно.
3. **Export-first probe.** После разрешения asset gate получить exact weights/hash, проверить schema/head load; собрать untrained3-head только для operator/parity smoke, не как распознающую violations модель. Adapter static1 → floating ONNX → target compiler/runtime с тем же normalized tensor. Операторный pass не доказывает target quality; fine-tuned graph требует повторной проверки.
4. **Один supervised trial specification.** Train только на train, validation для checkpoint/порогов; frozen D/preprocessing/crop policy. Не делать из полного исторического ImageNet LAMB training обязательную часть fine-tune. Нет KD, второго backbone и ensemble. Label `unassessable` и overlap/visibility disagreements проверить вручную по протоколу W2-D.
5. **Три маршрута на development:** D+FSM baseline, strict V, selective V только на согласованном ambiguity route. Unknown/малый/невидимый crop не превращать в safe clear; сохранить explicit unknown и причину. Threshold-only detector comparator обязателен при том же B_FP, иначе можно принять обычный threshold shift за архитектурный gain.
6. **Freeze → один lockbox и отдельный LinQ wall-clock run.** Freeze weights/hash, decoder, class mapping, V threshold/router, FSM/cooldown, input schedule, metrics. Измерить реальные streams/crowd bursts, peak calls/cache age/queue/drop и все neural nodes совместно. Cached replay проверяет качество и логику; не имитирует реальную end-to-end задержку.

**Метрики:** timely event recall, FP/camera-hour, precision, duplicates/event, wrong-person association, пропуски/late alerts, conditional V recall на реальных proposals, abstention/coverage, strata исходного размера головы/окклюзий/камер; p50/p95/p99 event-to-alert и queue age; calls/camera-hour и peak concurrency; качество FP32→target-converted отдельно. Crop accuracy вспомогательна. CI считать по независимым events/sessions, показывать denominators; соседние crops не независимые испытания.

**Будущие артефакты:** split/lineage manifest, label protocol и mapping, error atlas, exact init/card/license record, resolved lock, training config/raw-vs-EMA selection/checkpoint hash, adapter diff/export graph/hash/operator inventory, parity tensors/results, route/unknown/reset log, predictions с PTS, event ledger, device traces, frozen selection manifest и lockbox report. Эти артефакты не представлены как уже созданные; сохранены только source materials исследования.

**Исходы:** нет пригодных proposals/labels или unresolved redistribution условия — оставить D+FSM; V уменьшает FP, но режет своевременные TP — reject strict route, оценивать заранее ограниченный selective comparator; gain исчезает при равном B_FP — V не обоснован; target graph/parity/load не проходит — V не production, возможно offline исследование по отдельно согласованным условиям; только устойчивый quality gain + device pass + допустимые условия дают основание добавить второй graph. Даже успех не доказывает phone-use/fall ability, невидимые нарушения, другие камеры, промышленную сертификацию или fit/latency других чисел streams.


## F188 — W2-E: Handoffs и оставшиеся точные вопросы

- Происхождение/locator: [W2-E](_WORK/W2_E.md), раздел «Handoffs и оставшиеся точные вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- **Root:** baseline не зависит от verifier. K008 documentary закрыт, K003 weights unresolved честно сохранён. Не переносить привлекательные 2.5M/0.1GMAC в обещание 24GB fit, низкой задержки или accuracy. Выбрать V только по error mechanism, не по наличию модели.
- **W2-D:** есть ли независимые sessions и `helmet_visible/bare_head_visible/unassessable` labels именно для detector crops; сколько видимых heads и hard negatives, какого исходного размера; права/lineage? Отсутствие меток означает defer V, а не обучение на guessed pseudo-labels. PTS/event fixtures W2-D остаются общими для baseline и V.
- **W2-B / implementation:** наследуется только candidate core envelope в отдельном env; timm immutable source/weights pin добавить к lock. Учесть `--pretrained-path` head adaptation, native dynamic-batch trap, explicit legacy/static adapter. Imported stack/safe load/backward/export всё ещё unrun.
- **W2-C / artifact owner:** exact HF model license designation конфликтует с timm project weights notice. Нужен документированный результат разрешения именно выбранной формы использования/передачи; не заменять решением о detector license.
- **W2-F / LinQ owner:** V static224 batch1 normalized input→3 logits, no neural temporal state; проверить supported ops/opset/quantization, фактический fallback, совместную residency и burst latency с D. Допустим ли neural CPU на выданном сервере? До ответа/проверки V не финальный production node.
- **Temporal будущий gate:** требуется доказанная недостаточность причинного FSM и подходящие causal labels. Не подавать generic bidirectional TSM веса как готовую online fall model. При возобновлении нужно обнуление каждого state и внешних logits history на lifecycle boundaries; `empty` demo не является политикой reset.

Итог готовности: **одна конкретная условная initialization-карточка получена; specialist license conflict найден, не замаскирован; temporal обоснованно отложен; никакой дополнительный neural node не стал обязательным MVP.**


## F189 — W2-F: Решение и изменение по отношению к W1

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Решение и изменение по отношению к W1»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S273, S274.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F189. Историческое доказательство уже, чем можно заключить по соседству абзацев: worked end-to-end пример manual — ResNet50 classification; `yolo5s` — только имя в списке протестированных сетей на p22.** В manual нет worked detection decoder, checkpoint URL/hash, upstream version/commit или export command для `yolo5s`. Поэтому «LinQ manual демонстрирует наш запасной YOLOv5s bundle» было бы неверно. F145 правильно нашёл исторический путь, но он не устанавливает идентичность воспроизводимого YOLO fallback. [S274]

**F189. Новое публичное подтверждение: текущая vendor-страница `/tech` перечисляет `yolo5s`, `yolo8`, `yolo11`, а также `torch_resnet50` и `torch_mobilenet_v2`.** Это добавляет документированные направления запроса SDK examples. Страница без даты и version matrix; названия не определяют варианты n/s/m, head/task/weights/opset. Не заменять ею compiler acceptance и не распространять на YOLO26/YOLOX или произвольный classifier. [S273]

**F189. Ранний smoke следует выбирать из фактически выданного vendor example bundle, если он есть, сохраняя его точные bytes и expected outputs.** При выборе из одного лишь manual первым диагностическим кандидатом служит его ResNet50 классификационный пример, а не произвольно скачанный YOLOv5s. Это инфраструктурный smoke; он не становится baseline промышленной безопасности. Detection fallback должен быть отдельным подтверждённым graph+weights+decoder bundle. Основной YOLO26s и запасной YOLOX-s пока **device-unverified**; автоматической смены baseline здесь нет.

**F189. CPU neural ban не найден как буквальное официальное требование кейса.** По переданным визуальным CASE_NOTES p13 обязательны inference на LinQ и измерение скорости; это не тождественно утверждению «каждая neural operation только на TPU». CPU decode/geometry/NMS/tracking без learned embeddings/event logic — предлагаемые host stages. Neural CPU fallback внутри выданной среды требует отдельной трактовки организаторов и фактического trace. Нельзя ни объявлять его запрещённым публичными документами, ни молча считать разрешённым. [локальная provenance CASE_NOTES; не мой повторный визуальный просмотр кейса]

**F189. Одна загруженная программа и `sync` в manual не устанавливают multi-model residency/concurrency.** STAGING optimizations касаются внутренних TPU pipelines/DDR/cache; это не обещание одновременных независимых inference sessions нескольких моделей. До измерения учитывать serial occupancy и отдельно проверять load/unload, переключения и burst crops. Утверждение `/tech` о RNN не определяет state API, reset или изоляцию камер. [S273,S274]


## F190 — W2-F: Статусы исходных K и сохранение критики

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Статусы исходных K и сохранение критики»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


| K, исходная provenance | Что исходная критика говорила | Статус после этой ветки |
|---|---|---|
| **K009**, CRITIC.md §K009, P0 | Публичный LinQ путь исторический; нет проверенного запасного baseline и не разрешён neural CPU boundary; manual без PDF visual; unknown issued SDK не закрывается поиском | **Уточнена применимость / закрыта граница публичного evidence.** Добавлены current family claims и точная негативная идентификация `yolo5s`; actual SDK/device/fallback/policy **остаются открыты**. Критика подтверждается, не отменяется |
| **K002**, CRITIC.md §K002, P0 | Один pinned base и набор SHA не образуют согласованный training/export recipe | **Handoff W2-B**, не закрывается W2-F. Выбранные в W2-B Torch2.5.1/vision0.20.1/legacy envelopes и fallback2.4.1 остаются UNRUN и не становятся LinQ compiler matrix |
| **K008**, CRITIC.md §K008, P1 | Architecture shortlist не даёт готового causal temporal/crop verifier candidate | **Handoff W2-E** для identity/weights/data semantics. Здесь уточнены обязательства каждого retained neural node и состояния; отсутствие готового target path не исправлено словом «лёгкий» |

Это сохраняет исходную критику CRITIC, а не ретроспективно объявляет W1 исполненным smoke. Actual package/access/SKU неизвестны; публичным поиском они не установлены.


## F191 — W2-F: Что именно документировано и что не воспроизводится

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Что именно документировано и что не воспроизводится»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


| Evidence level | Конкретное свидетельство | Граница |
|---|---|---|
| **historically demonstrated, vendor document** | Manual2025 pp11–21: ResNet50 ONNX classification, TF conversion, quantization, compile, `.tpu`, runtime test; p24 опубликован пример class agreement | Это описание/пример производителя, не наблюдение нашего выполнения. p24 TLM time является оценкой TLM, не wall-clock latency выданного TPU |
| **historically tested-name** | Manual §3.4 списка pp21–22 содержит `yolo5s`, FlowNet и др. | Нет версии YOLO, graph/weights digest, task decoder, pipeline или testing protocol; нельзя восстановить exact fallback identity |
| **publicly documented, current live claim** | `/tech` Supported networks: `yolo5s/yolo8/yolo11` | Нет конкретного downloadable ready bundle, supported op attributes или delivered SDK version. «Current» означает прочитано сегодня, не дату успешной поддержки |
| **source-inferred / recommended** | Сначала bundled known-good vendor example, затем выбранный detection graph; serial execution до измерения concurrency | Наш порядок диагностики, не vendor гарантия и не выполненный тест |
| **device-unverified** | YOLO26s e2e/dense, YOLOX-s; будущие classifier/temporal/pose/ReID; даже точный historical example на сервере2026 | Ни compilation, ни runtime placement, quality/latency/residency не проверены |

Manual имеет version identity **2025, `RU.РМДВ.04.06.014-03 34 01`**, титульные 28 листов. Его условия p5: Ubuntu20.04, Python3.11, RAM не менее32GB, указан i7-7700. Это опубликованный historical environment, **не inventory команды и не ограничение выбранного W2-B export env**. Framework wheel указан общим именем `tpu_framework-py3-none-any.whl`, точная release/hash отсутствуют. В sample log p23 остаётся путь Python3.8: не выводить actual runtime version по одному перенесённому log.

Точная устанавливаемая по тексту identity worked example:

- p11 называет ResNet50 ONNX; p12 одновременно приводит имя `torch_resnet50.onnx` и путь `/auto/tests/frozen_graphs/resnet_50.onnx`. Это не доказательство одинаковых байтов; upstream training/weights source не определён.
- p12 демонстрирует ImageNet JPEG с known expected class; p13 RGB crop/resize224 и mean subtraction, NHWC batch1; postprocess прибавляет единицу к argmax. Значение class257 не переносится на zero-based decoder без этого правила. Class agreement одного изображения не доказывает numerical parity/quality.
- Входное имя в extract p12 имеет подозрительные пробел/индекс; converter p11 возвращает граф и rename dictionary, но упрощённый текст далее использует conversion как одно значение. Суффиксы tensor/op names на pp17–21 преобразуются вручную. Поэтому текст не copy-paste runnable recipe; брать реальный sample source из SDK и сверять names/shapes с artifact.
- p19 задаёт input shape `(1,224,224,3)` и аппаратный preset; pp20–21 показывают list/open/load/inference/synchronous execution. Область context manager в примере ограничивает lifetime объектов, но buffer ownership/thread safety, memory limits и reload/reset semantics не определены.
- p10 различает DEFAULT и STAGING и предупреждает о возможных неверных программах/долгой компиляции STAGING. Для первого нового graph уместен documented DEFAULT, если это соответствует выданной версии; это не новый рецепт PTQ/QAT.


## F192 — W2-F: PDF: фактическая попытка и ограничение visual

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «PDF: фактическая попытка и ограничение visual»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Использован skill PDF, read-only. `/docs` вновь подтверждает официальный link provenance manual; TinyFish извлёк полный текст. Однако прямой web open HTTPS/HTTP отказал; screenshot p12 не смог разрешиться как PDF. PowerShell Invoke-WebRequest и curl Schannel завершились TLS handshake error; Python requests получил SSL unexpected EOF; HTTP connection закрылся без ответа. **PDF bytes, SHA256 PDF, page PNG и визуальная проверка не получены.** Не созданы фиктивные screenshots и не превращён extract в «visual». Повторять TLS без новой возможности бессмысленно; критичные p11–13,17,19–22,24 следует визуально сверить владельцу actual PDF/SDK перед переносом команд. На сегодня уверенность в пунктуации/отступах и подозрительных literals ограничена extract.

Материал нового чтения: `_WORK/W2_F_MATERIALS/primary_fetch.json` — raw connector result с URL, metadata, text и link list; это извлечение, **не оригинальные байты PDF**. Отсутствие публичной ссылки на wheel или конкретный YOLO artifact в прочитанных `/docs`/`/tech`/manual не означает их отсутствия в выданном SDK или у производителя.


## F193 — W2-F: Точный bundle для владельца выданного SDK

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Точный bundle для владельца выданного SDK»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Ниже спецификация будущей передачи, **не существующий исполненный пакет**. Неизвестное поле: `unknown + owner + gate`; не подставлять предположения.

1. **Target manifest:** OS/arch/kernel, CPU/RAM; SKU/число TPU/firmware/driver, board memory; framework/compiler/converter/runtime wheel versions и hashes, supported pairing, доступ через local device либо remote service, quotas/timeouts. Из SDK сохранить официальный sample source/config/model+hash, expected fixture+hash, license/notices и фактический output contract. Для remote service нужны server-side placement/version records, одного client HTTP200 недостаточно.
2. **Каждый graph:** node ID/role, code/config/checkpoint hashes и licenses; preprocessing golden tensor; input/output names/dtypes/layouts/static shapes; IR, все domain::opset, external files hashes; requested/actual head; selected EMA/raw; exporter mode+effective flags+patch/env lock; полный inventory ops с attrs/dtypes/shapes, не только перечень названий.
3. **Boundary manifest:** ONNX→TF rename/layout/shape map, converted artifact hashes, precision/scales/rescale rules и compiled target hash; graph partition/CPU subgraphs/replacements; decoder version/class slots/background/selection policy/NMS/box inverse transform; state tensor schema и ownership/lifetime. Calibration data provenance передаётся владельцу precision; здесь новый quantization research не выполняется.
4. **Runtime DAG и нагрузка:** detector/V/T/pose/ReID/flow/learned router/fusion перечислены явно; teacher-only узлы исключены только если их действительно нет онлайн. Для каждого stream/camera/track описать call trigger, максимальный fan-out, deadline, queue/drop policy, thread/session, resident/load-on-demand policy, state/reset key. Обычная CPU-ассоциация без learned embeddings отличается от neural ReID.
5. **Acceptance и trace:** fixed development fixtures, allowed parity/quality budgets, declared stream/crop load, cold/warm runs, timestamps и task match policy; все error/status logs. Нельзя вписать универсальный допустимый процент drift, p95 deadline или supported opset без соответствующего решения/измерения.


## F194 — W2-F: Короткая последовательность различающих probes (всё UNRUN)

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Короткая последовательность различающих probes (всё UNRUN)»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


| Шаг / вопрос | Вход и процедура | Метрики, обязательный artifact и вывод |
|---|---|---|
| **P0 SDK identity / policy** | Read-only inventory issued package/service; сопоставить versions/hashes; получить именно существующий known-good sample. У владельца кейса установить допустимость neural CPU внутри LinQ и automatic fallback | Manifest и отдельная policy provenance: TPU-required / permitted-host-neural / unresolved. Не начинать трактовку policy по названию CPU+TPU |
| **P1 Known-good serial smoke** | Bundled vendor sample, его source/weights/preprocess/fixture; compiler defaults выданной release; device list→load→one serial call с documented completion | Import/compile/load/runtime status, actual outputs vs expected, compiler/runtime logs, real target execution trace. Если падает sample, сначала environment/service defect; это ещё не провал YOLO26 |
| **P2 Graph acceptance** | W2-B A-e2e-opset18 static1, conditional A-dense, B-D-FINE-static-postprocess-opset16 **после их фактического export/parity**; inspect IR и inventory. Проверить required ops/shapes/attrs/dtypes/layout/rename, включая TopK/Gather и sampling operators где они реально есть | Compiler rejection/partition map/required replacement, exact offending node и diagnostic. Tiny op-isolation fixture допустим как диагностика только с теми же attrs/shapes/dtypes; pass отдельного op не доказывает whole graph |
| **P3 Output/decoder correctness** | Один golden tensor на reference той же deployment head, float graph, target intermediate и real device; manifest names, no positional guessing | Raw outputs+hashes; schema/finite checks, distributions tensor/box/score errors, ties/ranking/threshold flips, class mapping и geometry. Внешний CPU decoder отдельно измеряется; совпадение top1 sample недостаточно |
| **P4 Backend / CPU interpretation** | Compiler partition report + runtime trace на real target; explicit placement request если API позволяет; обнаружить fallback по каждой neural stage. На приватном API не выдумывать disable-fallback flag | Per-node backend и copied bytes/host times, unsupported/host subgraphs. Low CPU usage/наличие `.tpu`/импорт `pytpu`/ORT success не являются доказательством исполнения всех nodes на TPU. При отсутствии trace статус placement-unverified, не automatic PASS |
| **P5 State and isolation** | Только для retained stateful route: reset, sequence A отдельно/B отдельно/A-B interleaved, track expiry/reuse, camera switch, seek/reconnect/gap/out-of-order, restart/reload. Stateless window model тоже проверить на ring-buffer leakage; задавать past-only timestamps | State input/output schema/hash, reset reason, session/camera/track key, output sequence agreement при одинаковом context; bounded buffer growth. Без future frames; allowed warmup отражать как unavailable, не safe-negative |
| **P6 Residency and switching** | Detector один; V/T один; sequential D→V→D с одинаковыми fixtures; попытка совместной residency только в documented limits; repeated load/unload и server restart | Host+device memory peaks и доступный allocator/accounting, load/unload/switch/copy latency, reload output parity, errors; число реально resident models. Нет гарантий из размера файла/числа параметров или tensor-cache STAGING |
| **P7 Burst / permitted concurrency** | После serial correctness: realistic fixed arrival trace с detector frames и correlated verifier crops; serial baseline; поддерживаемые concurrent sessions/streams только отдельным вариантом | p50/p95/p99 service/queue/copy/end-to-end time, frame age, backlog slope, drops/timeouts/errors, per-camera fairness, event onset→alert-ready, CPU/RAM/TPU memory и utilization где доступны. Submit timestamp не completion; ограничить queue и записать drop/backpressure policy |
| **P8 Event replay / frozen deployment** | Development replay на исходной временной сетке; затем wall-clock LinQ run с теми же temporal sampling/rules, отдельно lockbox после freeze | Event recall, FP/camera-hour, duplicate alerts, short-event capture, alerts lateness; trace связывает frame/crop→neural node→event. Cached outputs проверяют event logic, но не runtime deadline |

CPU policy и backend evidence — независимые оси: разрешённый neural CPU, который не измерили, всё равно непроверен; успешно измеренный CPU путь с unresolved policy не считается разрешённым финалом. Neural state может физически храниться в host RAM при вычислении graph на TPU: надо разделять storage placement и execution placement, а не запрещать ring buffer из-за слова state.

**Различающие исходы:** vendor sample failure→SDK/environment gate; sample pass + YOLO rejection→конкретный graph/ops issue; e2e TopK failure→conditional dense другой bundle с собственным reference, только если one-to-many weights существуют; numerical pass + burst queue growth→scope/router/residency change и повтор quality/latency; state cross-contamination→остановить temporal route; отсутствует разрешённый neural path хотя бы одного required node→каскад blocked, возможно detector+CPU rules или offline teacher. Переход к исторической сети допустим только после нового exact identity/license/target acceptance, не по одному имени `yolo5s`.

**Успех этого эксперимента не докажет** generalization на другие камеры, target phone-use/fall ability generic ResNet/YOLO, достаточность редких positives, допустимость другой SDK/head/opset, capacity при иной нагрузке либо право использовать иные weights/data. Нет оценок времени/VRAM/стоимости и вероятностей успеха.


## F195 — W2-F: Передачи и bounded unknowns

- Происхождение/locator: [W2-F](_WORK/W2_F.md), раздел «Передачи и bounded unknowns»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


- **Root / K009:** пометить historical worked **ResNet50**, tested-name **yolo5s**, live vendor-name **yolo8/yolo11** раздельно. K009 закрыт как граница публичной применимости; доступ/исполнение/policy остаются Q, их нельзя объявлять решёнными.
- **W2-B / K002:** передать actual exported graph и IR/op inventory/flags, не только constraints. Версии opset18/16 — выбранные export contracts, не supported LinQ. Train/export env и target SDK env можно изолировать; согласование serialized boundary проверяется отдельно.
- **W2-E / K008:** retained verifier/temporal route предоставляет node manifest, causal/window/state/reset contract и precise input/classes. Generic initialization не получает target ability от того, что vendor написал CNN/RNN. Если route отложен, не включать его скрыто в latency budget.
- **W2-D / evaluation:** runtime trace P5–P8 на исходной временной сетке; source timestamps отдельно от processing wall clock. Export/decoder/precision/calibration/threshold debugging ведутся на development; train/val/SELECT/lockbox независимы по incident/scene/camera lineage, соседние кадры не независимые испытания. Calibration из разрешённого train/calibration subset, не lockbox.
- **SDK owner:** точные доступные SKU/package/API versions, accepted formats/IR/opsets/layouts/attrs/dtypes/shapes; license/provenance bundled sample; actual placement; CPU policy; per-model memory/session/thread/buffer lifetime; concurrent residency/load switching; state reset и measured burst/event latency. Каждый пункт имеет observable probe выше. Ресурсы: предоставленные SDK/service/hardware access, доверенный vendor sample, выбранные actual graphs/golden inputs, разрешённые development clips и owner policy. Эти ресурсы сейчас не подтверждены.

Изменены только `_WORK/W2_F.md` и собственный `_WORK/W2_F_MATERIALS/primary_fetch.json`. Полный quantization survey, hardware/export и внешняя переписка не проводились.


## F196 — W2-G: Решение и статус критики

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «Решение и статус критики»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S276, S277, S278, S279, S282, S285.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F196. Выбрать фактически опубликованный wheel `vastai-1.9.0-py3-none-any.whl`, а не произвольный `pip install vastai` и не legacy `vast.py`.** Его SHA256 **`dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b`**, 324493 bytes, совпал с digest официального release asset. Entry point: `vastai = vastai.cli.main:main`; Python `>=3.10,<4.0`. Wheel сохранён [здесь](_WORK/W2_G_MATERIALS/vastai-1.9.0-py3-none-any.whl), metadata/entrypoint — рядом. Это pin CLI artifact, **не готовый dependency lock и не проверенная установка** [S276/S277].

**F196. Legacy вывод W1-13 о `shell=True` исправляется для выбранного wheel:** modular copy передаёт список аргументов `subprocess.run`, а не shell string. Но проверка exit code отсутствует и `StrictHostKeyChecking=no` сохраняется; внешний destination bytes/hash/load остаётся обязательным независимо от CLI success. Wheel destroy дополнительно имеет интерактивное подтверждение `y/N`, которого в исследованном legacy пути не было [S278/S279].

**F196. Billing неизвестность сузилась, но loading не закрыт:** новая найденная current FAQ явно включает loading в storage billing, одновременно current main Billing/Managing обещают отсутствие начисления при Loading. Уверенно объявлять loading полностью бесплатным нельзя. Две current страницы исключают compute/storage при offline, legacy FAQ включает offline storage. Для текущего документального default принимаем явную current offline-оговорку; фактический ledger ещё не наблюдался [S282–S285].

Исходная критика **K010** сохранена в [CRITIC.md](CRITIC.md), раздел «Lifecycle/стоимость…». Её ключевой тезис: «Даже valid copy command не отменяет destination hash/load». W2 не отрицает историческую правильность анализа legacy HEAD; он уточняет применимость к executable artifact. **Статус K010: закрыто документально по выбору artifact, командам и контролю integrity; уточнено по состояниям; остаётся открытым только фактический contract/Charges/payment и current loading contradiction.** Ни старый quote, ни этот runbook не авторизуют расходы/удаление.

**K011: уточнена применимость, интеграция остаётся у сборщика.** До аренды достаточно документальных/data/export gates и готового внешнего архива; VRAM qualification на конкретной 3090 — отдельная первая оплачиваемая стадия после разрешения. Не превращать full dependency engineering/strict recovery controller в обязательный новый проект. Вклад W2-G в minimal route: один CLI artifact, проверяемая внешняя копия, небольшой ledger; ни второй GPU, ни DDP для этого не требуются. Выбор сценария, людей, freeze и относительных reserves зависит от W2-A…F и сборки K011.


## F197 — W2-G: Release против HEAD: реальный исполняемый путь

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «Release против HEAD: реальный исполняемый путь»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S276, S277, S278, S279, S280, S281.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F197.** Release v1.9.0 опубликован `2026-10-20T21:31:52Z`, tag commit **`28bde4827374ef658694db5a1e1e61508b966e2f`**. Сравниваемый HEAD из W1 — **`42c3a47b44603775a5e31f54de0fce3994bd3f11`**, не плавающее имя master. GitHub compare содержит два промежуточных изменения: API-key/team notes и serverless disk metrics. Важнее этого перечня проверка bytes: извлечённые из wheel `cli/commands/{storage,instances,offers,billing}.py`, `api/client.py`, `cli/util.py` совпали с release source **и** этим HEAD; `api/{storage,instances,offers,billing}.py` совпали с HEAD. Результаты и hashes: [wheel_source_comparison.json](_WORK/W2_G_MATERIALS/wheel_source_comparison.json), [additional_manifest.json](_WORK/W2_G_MATERIALS/additional_manifest.json). Legacy целевые function bodies также совпадают между SHA, но это вспомогательное наблюдение, не доказательство wheel semantics [S276–S281].

| Интерфейс wheel | Реальный запрос / поведение | Locator выбранного source |
|---|---|---|
| `search offers` | По умолчанию POST `/api/v0/bundles/`; `--new` переключает PUT `/api/v0/search/asks/`. `--storage` задаёт `allocated_storage`; `--raw` возвращает offers list | `cli/commands/offers.py` L127–200; `api/client.py`, URL construction |
| `show instance ID` | GET `/api/v0/instances/ID/?owner=me`; возвращённая row преобразуется. Отсутствие в raw — объект `instances:null`, это не доказательство оплаты/уничтожения | `cli/commands/instances.py` L41–65; `api/instances.py` L83–91 |
| `show instances --raw` | Без explicit pagination собирает все v1 pages в flat list; `--limit`/`--next-token` меняют контракт на одну страницу | CLI instances L1054–1065; API instances L31–58 |
| `copy` | API PUT rsync при одном ID `None`, иначе copy_direct; local transfer запускает внешний rsync. Remote→remote ответ означает initiation | CLI storage L78–128; API storage L53–67 |
| `stop instance ID` / `start instance ID` | PUT `/api/v0/instances/ID/`, JSON state stopped/running. CLI печатает request result; polling состояния требуется отдельно | API instances L320–339; CLI instances L277–347 |
| `destroy instance ID` | Подтверждение по умолчанию; API DELETE `/api/v0/instances/ID/`, JSON `{}`. `-y` обходит prompt | CLI instances L212–248; API instances L309–317 |

**F197. Два важных различия с legacy и документационными примерами.** CLI wheel default search включает verified/external/rentable, **не `rented=false`**; SDK helper/legacy включает rented. Наш точный query ниже явно задаёт все четыре фильтра. `local:path` поддерживается help/parser, но API dispatch проверяет только `None`, поэтому explicit `local` идёт через `copy_direct`, в отличие от unprefixed local Unix path через `rsync`. Это доказанное ветвление кода, **не наблюдённая ошибка сервера**: не утверждаем, что сервер обязан отказать. Для первого transfer выбираем legacy numeric remote + unprefixed local path, не нуждающийся в этом предположении [S278/S280/S281].

`subprocess.run(cmd)` в wheel copy не использует `check=True` и не исследует `returncode`. HTTP success может закончиться ошибкой rsync, тогда function возвращает `None`; main dispatcher завершает такой путь без доказательства копирования. `--raw` не превращает copy в integrity receipt. Аналогично wrappers start/stop/destroy не возвращают пользователю helper result как надёжный lifecycle status. Не строить контроллер на одном exit code [S278/S279/S277].


## F198 — W2-G: Точные команды — только будущие, здесь не выполнялись

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «Точные команды — только будущие, здесь не выполнялись»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S278, S281, S286, S287, S288, S289.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


Среда выполнения примеров — **Linux/WSL control host**, POSIX paths; `.venv-vast190/bin/vastai` означает executable от выбранного wheel. Он должен быть отдельно установлен владельцем, затем его version и путь сопоставлены с manifest. GitHub asset уже скачан исследователем только как файл; его код не импортировался. Для установки будущий оператор может использовать:

```bash
python3 -m venv .venv-vast190
.venv-vast190/bin/python -m pip install ./vastai-1.9.0-py3-none-any.whl
.venv-vast190/bin/vastai --version
.venv-vast190/bin/python -m pip freeze --all > control-installed.txt
```

Перед install проверять SHA256 выше. Wheel METADATA закрепляет часть dependency versions, остальные — ranges; такая установка не воспроизводит транзитивные bytes во времени. Для повторного принятого control environment сохранить resolved lock/hashes/Python/OS и inventory. Это внешний runtime gate, не документальный пробел выбора CLI. Не использовать auto-update/installer с плавающим URL. API key настраивает владелец на control host; ключей в примерах и training image нет.

Read-only примеры после account setup владельцем; `INSTANCE_ID` и даты — placeholders, не существующие ресурсы этого исследования:

```bash
.venv-vast190/bin/vastai search offers 'gpu_name=RTX_3090 num_gpus=1 verified=true external=false rentable=true rented=false reliability>=0.99 disk_space>=100' --type on-demand --storage 100 --order dph_total --limit 3 --raw
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
.venv-vast190/bin/vastai show instances --raw
.venv-vast190/bin/vastai show volumes --raw
.venv-vast190/bin/vastai show invoices-v1 --charges --start-date START_UTC_UNIX --end-date END_UTC_UNIX --limit 100 --raw
.venv-vast190/bin/vastai show invoices-v1 --invoices --start-date START_UTC_UNIX --end-date END_UTC_UNIX --limit 100 --raw
```

Это рецепт обновления **той же** quote specification W1, не новый market survey. Перед будущей арендой сохранить полный ответ с UTC/query/D/offer/machine/host/type/end_date и отдельными rate fields. Для 2 GPU меняется `num_gpus=2`, но в minimal route вторая GPU не обязательна. Полный raw show может содержать `extra_env`, connection tokens/onstart: evidence storage должен быть приватным, а review copy редактируется без потери resource/state/rate полей. Установка и эти запросы здесь отсутствуют.

На каждом billing raw ответе следовать `next_token` до null, повторяя **тот же** date/filter запрос с `--next-token NEXT_TOKEN`; это одна страница в raw, а не гарантированно вся история. UNIX bounds — UTC, оба inclusive в выбранном helper. При агрегации соседних окон избегать двойного включения границы. История invoices — платежи/пополнения, **не** замена per-resource charges [S286/S287/S288].

Отдельный lifecycle после самостоятельного разрешения, не выполнять как один script:

```bash
.venv-vast190/bin/vastai copy INSTANCE_ID:/workspace/archive/run_id/ /srv/team_archive/run_id/
.venv-vast190/bin/vastai stop instance INSTANCE_ID
.venv-vast190/bin/vastai show instance INSTANCE_ID --raw
.venv-vast190/bin/vastai start instance INSTANCE_ID
```

Первая команда выбирает содержимое immutable source directory, согласно trailing slash semantics Data Movement. Transfer возможен при ограничениях доступности ports/host; обычный SSH/SCP требует работающего sshd и не является универсальной заменой stopped-instance transfer. На native Windows установка Python package сама по себе не предоставляет rsync; `WINDOWS_DRIVE:\...` также нельзя переносить в этот Unix-path протокол. В WSL использовать проверенные Linux paths и доступные `rsync`/`ssh`. Wheel улучшил shell handling, но `-e` по-прежнему содержит SSH command string и отключённую проверку host key: для доверенного backup предпочесть отдельно проверенный SSH/SFTP route с verified host key либо явно принять ограничения CLI; тождество hash при ошибочно доверенном источнике не удостоверяет происхождение [S278/S281/S289].

**Предлагаемый TEAM gate, отдельный от CLI:** до transfer trainer делает native recovery snapshot **до stripping**, закрывает его запись, фиксирует run/attempt/parent, список filenames, byte sizes и SHA256; manifest становится immutable. На внешнем destination независимый reader сверяет полный список/bytes/hash и загружает trusted checkpoint выбранным trainer для проверки expected state/epoch/optimizer и идентичности. Partial output, missing file, mismatch или load failure => `TRAINED_UNARCHIVED`, сохраняется прошлый verified snapshot. Никаких lockbox данных в smoke/архивном тестовом payload.

Receipt содержит source instance/run/attempt/checkpoint hash, destination identity/path/object-version при наличии, verified file list/bytes/hash, load-check environment/result, UTC и verifier identity. Только после receipt всех уникальных outputs и отдельного lifecycle поручения допустима будущая команда:

```bash
.venv-vast190/bin/vastai destroy instance INSTANCE_ID
```

Prompt не проверяет receipt автоматически. `--yes` не входит в минимальный ручной runbook. Перед запросом сохранить state/rates/receipt и точный ID; после — отдельно reconcile instance absence и полный список оставшихся volumes/charges. Destroy instance не является delete volume. Copy success, state request acceptance и archive acceptance — три разных факта.


## F199 — W2-G: State-by-state: политика, конфликт, проверка

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «State-by-state: политика, конфликт, проверка»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S282, S283, S284, S285, S286, S288, S290.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**F199.** Таблица — документальная интерпретация, не наблюдение списаний. `G` — compute **всего offer**, `Srun/Sstop` — storage allocation, `Bin/Bout` — usage network. Current main Billing задаёт секундный учёт active compute и online storage; bandwidth отдельно. Внутренний расчётный engine публично не проверен [S282].

| Состояние | Документальное начисление | Конфликт/граница | Точная будущая проверка |
|---|---|---|---|
| running/active connected | G + allocation storage + metered network | Idle/0% utilization не скидка | `gpu`, `disk`, `bwd`, `bwu`; rate×duration/volume против полного contract |
| loading | Compute явно не active; FAQ включает online storage; main Billing/Manage обещают «не charged» | **Current-current конфликт storage/transfer scope** | Синхронный state timeline и items `disk/bwd/bwu` за image pull interval; попросить exact metering exclusion |
| stopped/inactive online | Compute не active; storage продолжается; transfers отдельно | Sstop может быть выше Srun | Hover actual stopped price + `disk`; не подставлять Srun по умолчанию |
| offline | Current main+FAQ исключают active и storage | Legacy FAQ включает storage offline/broken; reserve консервативный | State interval, `gpu/disk` entries и corrections, не имитировать outage |
| expired | Contract останавливается; restart запрещён; возможное удаление через 48h | Отдельный expired storage тариф не найден; online/stopped трактовка условна | end_date/expiry→deletion timeline; `disk` и contract closure. 48h не backup SLA |
| destroyed | Container data удалены; прежний allocation больше не существует | Независимые volumes и delayed ledger ещё возможны | Deletion acknowledgement/absence, затем latest disk accrual end и все volume IDs |
| volume attached/detached | Отдельно тарифицируется, переживает instance destroy | Instance offline exemption не доказан для separate volume | `type=volume`, соответствующий `source`, `disk` до own removal; отдельный contract/rate |

Источники таблицы: current main Billing Pricing L191–196 и Loading L339–341 [S282]; current FAQ Pricing L123–128, **explicit loading** [S283]; legacy FAQ Billing L255–257 [S284]; Managing Instances L217–238, L338–347 [S285]; Storage Types Costs L191–197 [S290]. Offline documentation precedence — наше решение по актуальным страницам, не официальное разрешение противоречия. Для loading такого разрешения нет; бюджетировать storage/transfer консервативно до Charges/официального уточнения.

**F199. Новая schema позволяет проверять узко.** Public Show Charges OpenAPI `info.version:1.0.0` описывает GET `/api/v0/charges/`, required `select_filters.day` UTC Unix seconds; resource `type`, `source`, start/end, amount и nested items с enum **`gpu,disk,bwd,bwu`**. Contract amount округлён до 3 decimals. Полей guaranteed raw byte counter/rate/unit-divisor/schema currency declaration в просмотренном charge-item блоке нет; description — строка, не типизированная metering formula. Поэтому дробные totals и округление не восстанавливают SI/TiB divisor. Сервер допускает max500/page, выбранный CLI cap100/page — ограничения разных уровней, не конфликт [S286/S288].


## F200 — W2-G: Units и точные оставшиеся вопросы

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «Units и точные оставшиеся вопросы»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: S280, S282, S283, S287.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


W1-12 quote остаётся наблюдением **17:04:35–17:04:37 UTC 2026-10-23**, не будущим договором. Его `dph_total = dph_base + storage_total_cost` и `storage_cost × D /720` — наблюдённые равенства тех JSON. Не умножать multi-GPU `dph_base` на GPU count повторно, не добавлять storage к dph_total ещё раз. CLI `--storage` подписан **GiB**, field help `storage_cost` — $/GB/month, main billing — $/GB/hour, bandwidth — $/TB. Отсюда **не следует** общий byte divisor для allocation/transfer. 720 — арифметика снимков, не календарный месяц. Эти W1 факты не переизмерялись [F111/F04; S280/S282].

Будущий владелец аккаунта проверяет, не меняя settings ради исследования:

1. **Q-G01 Loading:** какая точная строка `disk` покрывает loading timestamps; входит ли image pull в `bwd`, с какого network interface и учитывается ли повторное скачивание cached layers? Противоречащие current sections приложить. Отсутствие крупной charge при маленьком test не доказывает exemption из-за округления/задержки.
2. **Q-G02 Rates/units:** contract running/stopped `diskHour`, allocation quantity и единица GiB/GB; `$ /GB/month` denominator; `bwd/bwu` quantity, bytes divisor TB/TiB, per-direction rates. Включены ли pip/apt/weights ingress и request/storage backend charges? Для package transfers общий network policy есть; исключения/точное metering image pull не доказаны.
3. **Q-G03 State:** коррелировать actual/intended/cur/next state, UTC transitions и charge interval; какое состояние реально использует billing? `intended_status=stopped` после PUT ещё не подтверждает stopped compute. Для offline/expired не устраивать платные/failure эксперименты без нужды: проверить лишь естественно возникшие интервалы либо официальный ответ.
4. **Q-G04 Payments:** Charges всех pages объясняет resource usage; `/api/v1/invoices/` — top-ups/transfers/payment records. Проверить saved-card/autobilling/negative balance policy, tax/FX/payment terms и предел порученных расходов. Zero balance не считать cap; current FAQ также описывает возможное погашение отрицательного баланса картой [S283/S287].
5. **Q-G05 Closure:** конец начисления source container после destroy, существование volumes, corrections и последующие charges сверять по resource ID и interval, не только по времени появления записи. Уничтожение не обещает немедленный нулевой total balance.


## F201 — W2-G: Минимальный будущий различающий эксперимент

- Происхождение/locator: [W2-G](_WORK/W2_G.md), раздел «Минимальный будущий различающий эксперимент»; прочитанный snapshot 2026-10-23.

- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.

- Источники: source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact.

- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.

- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.


**Вопрос:** позволяет ли выбранный wheel безопасно получить independently verified archive и reconciled lifecycle/cost evidence? Предпосылки: отдельное разрешение расходов/stop/start, pinned control runtime с rsync/ssh, разрешённый archive destination, owner-controlled contract, небольшой несекретный test directory, native snapshot schema владельца trainer. Destroy не нужен для первого integrity drill; его stage возможен позднее только после receipt и отдельного lifecycle scope.

1. До аренды read-only source/artifact checks уже выполнены. Будущий оператор локально проверяет version/path/deps и transport, пишет immutable small fixture+manifest. Это без-GPU preparation; fit здесь не заявляется.
2. На отдельно разрешённом instance копирует fixture, получает destination bytes/hash; проверяет заведомо повреждённую **вторую тестовую копию**, которая обязана быть отвергнута. Transfer лог и CLI exit сохраняются раздельно с verifier result.
3. Для реального native checkpoint выполняет destination trusted load и фиксирует его state/parent. На short qualification отдельно измеряет worst-case train+val memory: успешный transfer этого не заменяет.
4. Если разрешены stop/start, сохраняет state/rate snapshots до/после, ждёт actual status и доступность, не считает request ответ финалом. Billing сохраняет с полной pagination и последующим refresh после учётной задержки; расход сопоставляет с timeline/bytes/rates и округлением.

Метрики/артефакты: bytes/hash agreement, verifier false accepts (нужен ноль в planned negative fixture), load outcome, source/destination identity, transfer duration/retries, actual transition lag, archive receipt, rate+quantity units, `gpu/disk/bwd/bwu` amount и unresolved residual. **Успех** — целая загружаемая внешняя копия и объяснимый ledger; **failure** — любой missing/hash/load mismatch, непринятый state или необъяснённые units/charges => не запускать длинную серию/не удалять единственную копию. CLI exit0 при rejected destination — подтверждение необходимости независимого gate, а не успешный backup.

Этот опыт не доказывает future host reliability, exact numerical resume, целевой accuracy, 24GB fit полной задачи, выигрыш второй GPU или LinQ compatibility/latency. Lockbox не используется ни для fixture, ни для qualification/train selection. Training owner получает native pre-strip snapshot/lineage requirement (W2-A), stack owner — отсутствие runtime lock (W2-B), LinQ owner — hash проверенного inference artifact (W2-F), сборщик K011 — minimal one-GPU qualification без нового controller проекта. Оставшиеся actual rates/invoice/owner permissions не закрываются публичным поиском.

