# W1-06 — масштаб объектов, разрешение, crops и каскады

Проверено 2026-10-23, начало сетевого исследования 03:48 UTC / 06:48 Europe/Moscow. Тема: training_strategy. Входы: Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, раздел W1-06 _WORK/AGENT_PROMPTS.md. Это исследование источников и проект экспериментов; training, inference benchmark, экспорт и исполнение на LinQ **не выполнялись**. Целевые кадры, полный кейс, SDK и runtime LinQ отсутствуют.

## Решение для команды

Сначала установить, теряет ли pipeline уже имеющиеся в исходном кадре детали при уменьшении изображения. Если да, сравнить увеличение входа, tiles и person/head crops на одинаковой полной разметке кадров. Если отличительный признак неразличим уже в исходном видео, resize сам по себе не доказывает его восстановление: нужна другая камера/ракурс, иной признак события или честное состояние «не наблюдается». Число эпох не исправляет отсутствие доказательного визуального сигнала. Это вывод о проверяемой постановке, а не установленный предел конкретного CCTV.

SAHI — доступная реализация гипотезы сохранения масштаба. Публикационные gains получены на aerial detection; они не гарантируют gain для респиратора/сигареты и не устанавливают совместимость LinQ. Person/head cascade имеет дополнительный предел: пропуск или плохая локализация первого stage исключают правильный crop; качество второго stage на oracle crops не равно качеству системы.

## Источники с версиями и локаторами

Все источники ниже открыты 2026-10-23; короткие выписки представлены собственным пересказом. Время версии отличается от даты доступа. REP — чтение кода, PUB — измерение авторов, INF — наш вывод, PROP — будущая проверка.

| ID | Первичный источник, версия, прямой URL | Локаторы / использование |
|---|---|---|
| W1-06-S01 | Akyon, Altinuc, Temizel, *Slicing Aided Hyper Inference and Fine-tuning for Small Object Detection*, arXiv **2202.06934v5, 24 Oct 2022**, ICIP 2022. [HTML](https://arxiv.org/html/2202.06934v5), [PDF](https://arxiv.org/pdf/2202.06934v5), [history](https://arxiv.org/abs/2202.06934) | §3, §4, Tables 1–2, Fig.2; W1-06-F01–F02. Не смешивать с первоначально открытой v2 от 15 Feb 2022; рабочие выводы сверены с v5. |
| W1-06-S02 | Авторский benchmark, GitHub fcakyon/small-object-detection-benchmark, commit **d923428f380763dec2bd809cd4f7d532c6e00d03**, committer date **2025-01-17**. [README](https://github.com/fcakyon/small-object-detection-benchmark/blob/d923428f380763dec2bd809cd4f7d532c6e00d03/README.md), [requirements](https://raw.githubusercontent.com/fcakyon/small-object-detection-benchmark/d923428f380763dec2bd809cd4f7d532c6e00d03/requirements.txt), [eval script](https://raw.githubusercontent.com/fcakyon/small-object-detection-benchmark/d923428f380763dec2bd809cd4f7d532c6e00d03/eval_tools/predict_evaluate_analyse.py), [VisDrone TOOD config](https://raw.githubusercontent.com/fcakyon/small-object-detection-benchmark/d923428f380763dec2bd809cd4f7d532c6e00d03/mmdet_configs/visdrone_tood/tood_crop_480_960_cls_60.py) | requirements; `INFERENCE_SETTING_TO_PARAMS`, `predict`, `evaluate`; `train_pipeline`, `runner`, `checkpoint_config`, `evaluation`, `load_from`. F03. Репозиторий переименован: исходный sahi-benchmark перенаправляет сюда. |
| W1-06-S03 | SAHI **0.12.8**, commit **80ebdb699851facf87def03c0597e1aeb87a9a2d**, committer date **2026-09-30T16:52:41Z**. [predict.py](https://raw.githubusercontent.com/obss/sahi/80ebdb699851facf87def03c0597e1aeb87a9a2d/sahi/predict.py) | `get_sliced_prediction`, F04. Tag/commit/date получены GitHub API `/repos/obss/sahi/tags?per_page=5` и `/commits/80eb...`; это зафиксированная доступная версия, не promise версии хакатона. |
| W1-06-S04 | Тот же SAHI commit. [slicing.py](https://raw.githubusercontent.com/obss/sahi/80ebdb699851facf87def03c0597e1aeb87a9a2d/sahi/slicing.py) | `get_slice_bboxes`, `process_coco_annotations`, `slice_image`, `slice_coco`; F05. |
| W1-06-S05 | Тот же SAHI commit. [models/base.py](https://raw.githubusercontent.com/obss/sahi/80ebdb699851facf87def03c0597e1aeb87a9a2d/sahi/models/base.py) | `DetectionModel.perform_batch_inference`, F06. |
| W1-06-S06 | Singh, Davis, *An Analysis of Scale Invariance in Object Detection — SNIP*, arXiv **1711.08189v2, 25 May 2018**, CVPR 2018. [PDF](https://arxiv.org/pdf/1711.08189v2), [CVF entry](https://openaccess.thecvf.com/content_cvpr_2018/html/Singh_An_Analysis_of_CVPR_2018_paper.html) | §§4–7, Table 1, Table 2, pp.4–7 PDF; F07. CVF PDF URL и papers_backup дали 403 в web.open; arXiv PDF получен успешно. |
| W1-06-S07 | Singh, Najibi, Davis, *SNIPER: Efficient Multi-Scale Training*, NeurIPS **2018**, proceedings version. [PDF](https://proceedings.neurips.cc/paper/2018/file/166cee72e93a992007a89b39eb29628b-Paper.pdf) | §§3.3, 3.5, 4.1–4.4, Tables 1–2, pp.4–7; F08. Дата revision PDF не установлена. |

Механизмы получения: SAHI paper/PDF и SNIPER открыты web.open; код прочитан прямым HTTPS через PowerShell `Invoke-WebRequest -UseBasicParsing`, metadata — `Invoke-RestMethod`. Обычный Invoke-WebRequest дал локальный NullReferenceException, после `-UseBasicParsing` чтение успешно. Попытки guessed tags `v0.11.36`/`v0.11.23` дали 404; они не являются evidence отсутствия SAHI. После запроса фактических tags применён существующий 0.12.8 без префикса v. Код прочитан, пакет не устанавливался.

## Извлечённые факты

### W1-06-F01 — SAHI: опубликованный протокол и единицы [PUB; S01 §4]

VisDrone: 6471 train, 548 val images; Table 1 — **test-dev**. xView: random 75/25 train/val. Это размеченные aerial datasets, не few-shot PPE. FCOS/VFNet/TOOD, MMDetection; original images плюс sliced patches. Train patch ranges: 480–640 px VisDrone, 300–500 px xView; resize с сохранением aspect ratio, 800–1333 px. Inference: 640×640 и 400×400 px соответственно; PO=25% overlap, NMS IoU=0.5. Метрика **AP50**, IoU=0.5, maxDets=500, не AP50:95. GPU/time и правило checkpoint selection из статьи не установлены.

### W1-06-F02 — gains и ограничения SAHI [PUB + арифметический INF; S01 Tables 1–2]

VisDrone TOOD: FI=29.4; SAHI=31.9; SAHI+PO=32.5; SAHI+FI+PO=34.7; SF+FI=36.8; SF+SAHI+FI+PO=43.5 AP50. Для large: FI=50.0, SAHI+PO=43.6. Следовательно, crop может ухудшать large/context. Для FCOS FI=25.8→SAHI+FI+PO=31.0 (**+5.2 п.п.**, abstract говорит 6.8); TOOD combined 43.5−29.4=**14.1 п.п.**, abstract говорит 14.5. Сохранять табличные числа и расхождение. xView TOOD SF+SAHI+PO=20.6, с добавленным FI=20.4: полный проход не гарантирует улучшение. Это авторские результаты, не наши измерения.

### W1-06-F03 — реальный benchmark не тождествен бумажному recipe [REP; S02]

`requirements.txt`: sahi==0.9.3, mmdet==2.21.0, mmcv-full==1.4.3; README: PyTorch1.10.0/torchvision0.11.1/CUDA11.3. Eval script: confidence=0.01, NMS/IOU=.5, class_agnostic=False, force_postprocess_type=True, max_detections=500. TOOD config: RandomCrop absolute_range=(480,960), Resize=(1333,800), keep_ratio=True; 24 epochs, steps16/22, warmup500, `save_best="auto"`; COCO TOOD R50-FPN checkpoint `tood_r50_fpn_1x_coco_20211210_103425-20e20746.pth`. Crop range **480–960** отличается от статьи 480–640. Нельзя заявлять буквальную репликацию бумаги по текущему commit; нужна историческая revision/config-to-result связь. Значение `save_best="auto"` не устанавливает выбранный авторами конкретный checkpoint.

### W1-06-F04 — актуальная SAHI API имеет иные merge defaults [REP; S03]

`get_sliced_prediction`: overlap_height_ratio=overlap_width_ratio=0.2, perform_standard_pred=True, postprocess_type="GREEDYNMM", postprocess_match_metric="IOS", match_threshold=.5, class_agnostic=False, batch_size=1. Сначала slices, затем batch inference, shift predictions в координаты кадра, optional standard pass при num_slices>1, merge. При model confidence<0.1 автоматически переключается на NMS/IOU, если force_postprocess_type=False. Поэтому изменение confidence способно незаметно изменить merge. Сравнение должно фиксировать оба механизма. `durations_in_seconds` даёт slice/prediction/postprocess, но не удостоверяет полную задержку нашего сервиса.

### W1-06-F05 — обработка crop GT и grid [REP; S04]

`get_slice_bboxes`: шаг — tile dimension минус `int(overlap_ratio*dimension)`; граничные окна сдвигаются к краю. `process_coco_annotations` обрезает annotation и сохраняет её при cropped_area/original_area>=min_area_ratio. `slice_image` и `slice_coco` default min_area_ratio=0.1; у `slice_coco` ignore_negative_samples=False. Эта геометрическая фильтрация не знает семантику «правильно надет респиратор»: оставшиеся 10% bbox не гарантируют наблюдаемость состояния. Нужен аудит обрезанных positives/ignore policy, иначе видимые фрагменты могут превратиться в ошибочные negatives.

### W1-06-F06 — batch API не равно batch на устройстве [REP; S05]

Базовый `perform_batch_inference` сохраняет images; последующая конвертация вызывает одиночный `perform_inference` для каждого изображения. Native batch требует override адаптера; docstring приводит Ultralytics/HuggingFace. Наличие параметра batch_size не доказывает уменьшение accelerator invocations или latency для иного runtime. Адаптер LinQ в этой ветке не установлен и не проверен.

### W1-06-F07 — просто multi-scale и selective-scale различаются [PUB; S06 §§4–7, Tables 1–2]

R-FCN ResNet50 ablation, proposals Deformable-RFCN ResNet101; COCO. Для small (<32×32 px) при test1400×2000 Table1: 800all=19.6, 1400all=19.9, MST=19.5, SNIP=21.4 mAP; small-only training=16.4. Нельзя принять большее разрешение/случайный multi-scale за гарантированное улучшение. SNIP selectively ignores gradients объектов вне scale range, использует их на подходящих масштабах. Table2: single-scale AP34.5/APS16.3; MS train/test35.6/19.5; SNIP37.8/21.4. Данные: 123k train, 20,288 test-dev; 118k/5k minival для proposal recall. RCN7 epochs, RPN6; проверенные baseline8/9 epochs были хуже7. Это специальный detector/trainer, не универсальный YOLO flag. Размер `<32×32` относится к dataset convention, не к физическому пределу видимости сигареты.

### W1-06-F08 — crop training должен видеть трудный фон [PUB; S07 §§3–4, Table2]

SNIPER Faster-RCNN/ResNet101, COCO: AP43.4 без negative chips против46.1 с ними; 2 scales43.3. RPN recall при этом AR65.4 в обоих вариантах: recall не отражает FP. Chips512² px, около5/image, примерно30% больше pixels, чем single800×1333; batch128,6 epochs, LR.015. Негативные chips выбирает отдельно обученный RPN. Timing авторов:14h training на8×V100 плюс2h RPN; около5 images/s наV100 при parallel processes, average batch100. Эти числа не являются нашей оценкой RTX4070/LinQ. Чипы/негативный mining требуют специального pipeline, не только генерации положительных crops; checkpoint-selection rule здесь не установлен.

## Выводы и сравнение полной системы

### W1-06-F09 — геометрия масштаба [INF из координат resize; не эксперимент]

Для letterbox без растяжения scale r=min(Winput/Wsource,Hinput/Hsource), а объект w×h исходных px занимает rw×rh входных px до padding. Например, **условный** исходный 1920×1080 и вход640²: объект12×6 px становится4×2 px; crop640²→input640² сохраняет12×6 px. Новые наблюдённые детали при интерполяции не появляются. Это расчёт, а не минимальный допустимый размер детектора. Нужны distributions min(w,h), area, blur, visibility в исходном и фактическом model input, отдельно по классам/камерам/дистанции. Размер человека не заменяет размер респиратора.

### W1-06-F10 — стоимость вызовов [INF; S03–S05]

При W,H>=tile s и фиксированном overlap o оценка grid по оси: n=1+ceil((D−s)/(s−floor(os))); проверять реальные координаты S04 на границах. Число tiles NxNy, плюс optional full frame. Иллюстрация, **не runtime measurement**: 1920×1080,640²,25%:4×2=8 crops; с FI=9 image forwards при batch1. Для true batch B число групп ceil(8/B)+1, но объём изображений остаётся9; fallback адаптер может выполнить9 одиночных вызовов. Считать image forwards, API requests и accelerator launches раздельно. Увеличение входа640→1280 увеличивает canvas area в4 раза; это не доказательство4× latency или memory.

| Вмешательство | Сохранение сигнала и риски | Что учитывать в полной стоимости |
|---|---|---|
| Full frame большее input | Меньше downsampling; контекст остаётся; меняется scale distribution и input graph | Decode, resize, transfer, engine, NMS; отдельная compiled shape, memory и качество |
| Fixed tiles | Не зависит от person recall; border truncation, duplicates, мало контекста | Все tile forwards, optional FI, merge, host crops, передача, batching, RAM и queue |
| Person→head/PPE crop | Выбор области сохраняет больше px для лица; FP/FN person/head stage, промах crop, occlusion | Stage1+variable number crops; idle/crowded scenes; две модели/две shapes, batching и swap |
| GT/oracle crops | Диагностика второго stage при идеальной локализации | Нельзя выдавать за deployable result; upstream cost и misses исключены |
| Crop training + original frames | Scale alignment, но больше correlated examples; label/context/negative coverage | Единый исходный split до slicing, число exposures, iterations и annotation audit |

### W1-06-F11 — cascade recall и контекст [INF; предлагаемый accounting]

Для системы без fallback, у которой положительный результат возможен только при пригодном upstream crop: R_end=P(usable crop|positive)×P(correct final|positive,usable crop). Это chain rule, без допущения независимости. End recall не выше usable-crop coverage. Head crop может исключить руку/сигарету, person crop — расположение относительно опасной зоны или горючих материалов; какой контекст необходим, задаёт класс/событие. Сохранить полные координаты, parent IDs и внешний контекст. Классификация crop «маска есть» не равна событию «респиратор надет правильно». Если GT — отношение/событие, одной object AP недостаточно.

Одинаковый threshold contract означает одинаковые классы, matching/ignore regions/maxDets, frame GT, merge rules и заранее выбранное правило operating point. Численно одинаковый confidence у разных cascade stages не означает одинаковый смысл score. Сначала фиксированный low-score detection export и одинаковый scorer; затем thresholds каждого кандидата выбираются **на validation** по одному требованию FP/recall и замораживаются. Не сравнивать oracle-positive crops с full-frame negatives. Merge/NMS изменения выделять отдельно от training gain.

Полная задержка измеряется от выбранной точки поступления кадра до готового результата/события, с одинаковой границей: decode+preprocess+queue/network+все stages+transfer+merge+event logic. Для async pipeline сумма средних stage times не заменяет p95 latency/throughput. FPS, p50/p95 ms/frame, frames dropped, calls/frame, bytes/frame, peak host/device memory и crowd dependence — отдельные единицы. Все значения для нашей системы пока неизвестны.

## Предлагаемые E-процедуры (ни одна не выполнена)

### W1-06-E01 — имеется ли достаточный исходный сигнал?

**Входы:** целевые original decoded frames/видеокодек, timestamps, GT/class semantics, mapping независимых camera/session, исходный checkpoint от model_stack. **Контроль:** фиксированный audit subset, original и точный input tensor одного и того же кадра. **Действия:** измерить original/input object px distributions; вручную независимо оценить visible/occluded/ambiguous/unobservable; наложить GT после resize/letterbox и проверить coordinate round-trip. Отдельно размечать дым/руку/сигарету, если эти признаки действительно заданы кейсом. **Метрики:** доля positives с потерянным различимым признаком после resize, agreement аудита, размеры px, recall по bin и доля ambiguous. **Артефакты:** frame manifest, crop gallery, pixel histograms, original→tensor transform, reasons. **Исход:** если detail сохраняется в native crop, E02; если отсутствует в original, вопрос постановщику/violation_methods о наблюдаемости. **Stop:** не подбирать числовой «минимальный размер» по одному примеру; прекратить увеличение размера, если оно лишь интерполирует неразличимые pixels. **Предел:** аудит наблюдаемости не устанавливает достижимый AP и допустимость камеры.

### W1-06-E02 — контролируемая resolution/tiles абляция

**Входы:** frozen checkpoint+hash, полностью проверенная full-frame GT, исходные video/session splits до нарезки, validation/lockbox, runtime вне/на LinQ по отдельным стадиям доступа. **Контроль:** общий scorer/GT/maxDets/ignore/threshold-selection contract из F11. Начать без fine-tuning: A full-frame штатный размер; B один больший подтверждённый input; C tiles без FI; D те же tiles+FI. Один небольшой tile/overlap набор выбирается по E01; размеры — гипотезы, не рекомендованные defaults. Merge фиксировать явно, не полагаться на F04 auto switch.

**Действия:** сохранить predictions в исходных координатах; посчитать per-class AP50 и AP50:95, recall/precision на согласованном operating point, original-size bins и контекстные подгруппы; учесть border/duplicate/large-object errors; измерить всё из F10–F11. **Артефакты:** configs/hashes/input shape, tile origins, raw/merged predictions, CPU/device/runtime version, warmup/synchronization/timestamp contract, latency traces, gallery discordant pairs. **Исходы:** gain без приемлемой системной цены не принимается; отсутствие gain закрывает slicing данной модели/камеры, а не весь метод. **Stop:** прекратить расширение grid при нарушении согласованного latency/memory/calls budget либо если improvement исчезает на независимой session. **Предел:** удачный результат на RTX/CPU не подтверждает LinQ, inference gain не доказывает training gain.

### W1-06-E03 — локализовать ошибку person/head каскада

**Входы:** frames с полным GT, parent person/head boxes и связями к PPE/событию, реальные stage1 predictions; stage2 checkpoint. **Контроль:** одинаковый stage2 и crop margin/resize, одинаковый scorer и негативные кадры. **Действия:** сравнить GT/oracle crops, GT crops с измеренной по validation jitter моделью, predicted crops; затем полный cascade с upstream miss accounting. Sweep margin лишь на validation; сохранять закадровый padding и clip policy. Oracle subset не подменяет end-to-end test.

**Метрики:** usable-crop coverage, stage1 recall, crop inclusion/containment, stage2 conditional recall и end-to-end recall/precision; FP/video-hour и event delay при наличии событийного GT; errors miss-parent/miscenter/context/association; costs от0 до crowded max crops/frame. **Артефакты:** parent-child IDs, crop origins, upstream misses, score/threshold manifest, per-frame invocation traces. **Исход:** oracle good/predicted bad→исправлять локализацию/coverage; оба bad→данные/семантика/сигнал/stage2; crop good/event bad→контекст/правила. **Stop:** reject cascade, если coverage ceiling ниже нужного recall или системный бюджет нарушен; budget и target recall ещё должны быть заданы. **Предел:** хороший oracle тест не доказывает deployment; хороший person detection не подтверждает head/PPE localization.

### W1-06-E04 — нужно ли scale-matched обучение?

**Входы:** победившая/перспективная E02/E03 preprocessing схема, проверенный trainer и dataset. **Контроль:** тот же исходный checkpoint, исходные изображения/GT/split, comparable optimizer updates/exposures и seeds; явно учесть, что crops увеличивают число примеров. **Действия:** A original-frame fine-tune; B original+train crops с negatives и audited truncation; обе модели оценивать одним фиксированным inference режимом. Отдельно при необходимости factorial training crop × inference crop, чтобы разделить эффекты. Multi-scale только при подтверждённой реализации и отдельной ablation; не имитировать SNIP простым random resize. **Метрики/артефакты:** E02 metrics + train exposures/iterations/wall-clock, crop GT audit, dataset/config/checkpoint hashes и checkpoint-selection rule. **Исход/stop:** принимать лишь independent gain, не ухудшающий критичные classes/context; если negatives/labels некорректны — остановить до исправления. **Предел:** не доказывает export/quantized equivalence, SDK compatibility или value на другой камере.

## Открытые вопросы и адресные передачи

| ID / адресат | Точное недостающее и решение | Получение / приоритет |
|---|---|---|
| W1-06-Q01 → datasets, violation_methods | Есть ли в исходном видео наблюдаемые сигарета/респиратор и корректные состояния; какие camera/session и полные negatives/parent relations доступны? E01/F09/F11 определяют, нужен crop или иной признак. | Полный кейс+целевые данные+annotation audit; P0. |
| W1-06-Q02 → linq_platform | Какие статические/dynamic NCHW shapes, batch sizes, число одновременно resident models/engines; размещение resize/crop/NMS; fixed-shape padding, remote request overhead, допустимость host stages? | SDK/version+device access, небольшой compile/run позже; P0. Ни одна из этих возможностей в исследовании не установлена. |
| W1-06-Q03 → model_stack | Какой checkpoint/class map/input stride и export route реально доступны; adapter может native batch или делает loop; multiscale/crop training поддерживает корректные ignored/clipped labels? | Проверка конкретной pinned реализации; F03–F06, E02–E04; P0. |
| W1-06-Q04 → evaluation | Зафиксировать full-frame/event GT, operating-point policy, matching/maxDets/ignore; original-size bins, группировка session/camera. Каков допустимый FP/hour и recall/latency budget? | Кейс+контракт оценки до E02; P0. |
| W1-06-Q05 → video_architecture | Реальный frame rate/число потоков/person count distribution и стоимость network/queue/crops/model swaps; поддерживаются ли timestamps каждого stage? | E02/E03 на целевой конфигурации; P0. Нельзя объявлять tile FPS model-only скоростью сервиса. |
| W1-06-Q06 → training_strategy W2 | Нужна ли буквальная SAHI replication? Если да, найти исторический commit и конкретные config/result/checkpoint, разрешить crop480–640 vs480–960 и abstract/table deltas. | Открытые git history/result metadata; P1 при выборе SAHI, иначе известная граница, не blocker. |

Ближайший полезный выбор: после получения кадров выполнить E01, затем небольшую E02 без обучения. К E04 переходить после обнаруженного scale/input mismatch и работоспособного пути исполнения. Такой порядок проверяет причину ошибки и не выдаёт сохранение масштаба за гарантированный результат дообучения.
