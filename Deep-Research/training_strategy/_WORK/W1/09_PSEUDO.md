# W1-09 — Pseudo-labels и semi-supervised detection

Исследовательская ветка training_strategy. Доступ: 2026-10-23, начало сетевой проверки 03:54:58 UTC / 06:54:58 Europe/Moscow. Это дата чтения, не публикации. Прочитаны входные Context-prompt.md, prompt-training-strategy.md, PLAN.md и индивидуальное W1-09. Ни обучение, ни инференс на целевых данных, ни экспорт не выполнялись. Статусы ниже: **paper** — измерение/описание авторов; **code-read** — просмотр кода без исполнения; **inference** — наш вывод; **proposed** — будущая проверка.

## Решение для команды

При наличии целевого неразмеченного видео первым кандидатом считаю **offline-предразметку с полным ручным исправлением небольших независимых порций**. Это предложенный инженерный маршрут, а не доказанный выигрыш на нашем кейсе. До массового принятия автоматических boxes нужен аудит учителя, включающий объекты, которых учитель вообще не предложил. При слабом редком классе сначала разметить его реальные примеры; высокий глобальный confidence threshold может оставить этот класс без обучения.

Online Soft Teacher / Unbiased Teacher — отдельные реализации обучения, а не название операции «сгенерировать labels и вызвать train». Их стоит пробовать только после работающего supervised baseline, независимого validation и подтверждения поддержки нужной архитектуры. Наличие Faster R-CNN/FCOS реализации не устанавливает поддержку выбранного YOLO, Ultralytics или LinQ. Два teacher/student прохода, matching views, EMA, loss и checkpoint state создают интеграционную работу; оценка её времени/VRAM пока отсутствует.

## Реестр первичных источников

Для всех S-ID дата доступа — 2026-10-23. Публикации и commit dates указаны отдельно. GitHub SHA получены через официальный commits API; raw-файлы читались по этим SHA. Ссылки ниже постоянные; внешние страницы не считались инструкциями.

| ID | Источник, версия, что действительно открыто | Локатор / поддержка |
|---|---|---|
| W1-09-S01 | Xu et al., *End-to-End Semi-Supervised Object Detection with Soft Teacher*, ICCV 2021. arXiv v1 2021-06-16, v3 2021-08-06. [metadata](https://arxiv.org/abs/2106.09018), [PDF v3](https://arxiv.org/pdf/2106.09018v3). PDF получен и прочитан в релевантных разделах. | §3, §4.1–4.3, Tables 2–4; F01. |
| W1-09-S02 | microsoft/SoftTeacher, commit `0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe`, commit date 2022-08-31. [README](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/README.md); открыта и главная страница. | Main Results, Notes, Requirements; F02. На странице GitHub наблюдался archive notice 2026-10-06. |
| W1-09-S03 | Тот же SoftTeacher SHA, [ssod/models/soft_teacher.py](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/ssod/models/soft_teacher.py), raw прочитан. | `forward_train`, `foward_unsup_train` (написание авторов), `unsup_rcnn_cls_loss`, `unsup_rcnn_reg_loss`, `compute_uncertainty_with_aug`, `extract_teacher_info`, `aug_box`; F03. |
| W1-09-S04 | SoftTeacher SHA выше, [configs/soft_teacher/base.py](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/configs/soft_teacher/base.py), raw прочитан. | `semi_wrapper`, weak/strong/test pipelines, `custom_hooks`, optimizer/runner/lr_config; F04. |
| W1-09-S05 | SoftTeacher SHA выше, [partial 180k config](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/configs/soft_teacher/soft_teacher_faster_rcnn_r50_caffe_fpn_coco_180k.py), [launch script](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/tools/dist_train_partially.sh), raw прочитаны. | `samples_per_gpu`, paths с fold/percent, sampler; F05. |
| W1-09-S06 | SoftTeacher SHA выше, [MeanTeacher hook](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/ssod/utils/hooks/mean_teacher.py), [multi_stream_detector.py](https://github.com/microsoft/SoftTeacher/blob/0423bb2fe43f4fbe0e6704b1011d865cc3d2fdbe/ssod/models/multi_stream_detector.py), raw прочитаны. | `before_run`, `before_train_iter`, `momentum_update`; `model`, `forward_test`; F06. |
| W1-09-S07 | Liu et al., *Unbiased Teacher for Semi-Supervised Object Detection*, ICLR 2021; arXiv v1 2021-02-18. [metadata](https://arxiv.org/abs/2102.09480), [PDF](https://arxiv.org/pdf/2102.09480). Открыты §3–4 и appendix A.2/A.4. | §3.2–3.3, Table 1, §4, Appendix A.2.2/A.4/Table 5; F07. |
| W1-09-S08 | facebookresearch/unbiased-teacher, SHA `6977c6f77c812fae4064dc1b3865658c2ed247b1`, 2021-07-18. [README](https://github.com/facebookresearch/unbiased-teacher/blob/6977c6f77c812fae4064dc1b3865658c2ed247b1/README.md); открыта главная страница. | Prerequisites, Training, Evaluation; F08. GitHub notice: archived 2023-10-31. |
| W1-09-S09 | UT SHA выше, [ubteacher/engine/trainer.py](https://github.com/facebookresearch/unbiased-teacher/blob/6977c6f77c812fae4064dc1b3865658c2ed247b1/ubteacher/engine/trainer.py), raw прочитан. | `UBTeacherTrainer.run_step_full_semisup`, `threshold_bbox`, `_update_teacher_model`, `build_hooks`; F09. |
| W1-09-S10 | UT SHA выше, [1% run1 config](https://github.com/facebookresearch/unbiased-teacher/blob/6977c6f77c812fae4064dc1b3865658c2ed247b1/configs/coco_supervision/faster_rcnn_R_50_FPN_sup1_run1.yaml), [Base-RCNN-FPN.yaml](https://github.com/facebookresearch/unbiased-teacher/blob/6977c6f77c812fae4064dc1b3865658c2ed247b1/configs/Base-RCNN-FPN.yaml), raw прочитаны. | MODEL / SEMISUPNET / SOLVER / INPUT / TEST; F10. |
| W1-09-S11 | Sohn et al. авторский STAC repo google-research/ssl_detection, SHA `00d52272f61b56eade8d5ace18213cba6c74f6d8`, 2020-12-01. [README](https://github.com/google-research/ssl_detection/blob/00d52272f61b56eade8d5ace18213cba6c74f6d8/README.md), открыта главная страница. | Training steps 1–3, `train_stg1.py`, `predict.py`, `train_stg2.py`; F11. GitHub notice archived 2024-05-28. |
| W1-09-S12 | Liu, Ma, Kira, *Unbiased Teacher v2*, CVPR 2022, arXiv v1 2022-06-19. [metadata](https://arxiv.org/abs/2206.09500), [PDF](https://arxiv.org/pdf/2206.09500v1). Веб-reader отверг PDF по размеру; получен напрямую Python urllib в память, текст pp.4–5 прочитан через pymupdf. | §3.2–3.3, Figures 2–4, Tables 2–3; F12. |
| W1-09-S13 | [UTv2 author repo](https://github.com/facebookresearch/unbiased-teacher-v2), SHA `93bb1256e8eb69103214b1d47db7f8297cb6b2c7`, 2022-07-27. README открыт; код обучения не анализировался. | FCOS configuration examples / framework prerequisites; F12, граница интеграции. |

**Сбои доступа:** Soft Teacher CVF PDF вернул web-reader `403 Forbidden`; независимый arXiv v3 PDF успешно открыт. UTv2 CVF PDF также `403`; arXiv PDF web-reader: `400 Content length is too large: 15209891`; прямое получение в память успешно. Первый вывод pymupdf в Windows stdout завершился `UnicodeEncodeError`, повтор с UTF-8 stdout дал текст. Ничего из этого не означает недоступность самих исследований. Полные чужие PDF в рабочие файлы не копировались.

## Факты и пределы переноса

### W1-09-F01 — Soft Teacher: измерение статьи, не наш результат

**paper; S01, §4.1–4.3/Tables 2–4.** COCO train2017: около 118k изображений; partial setting: 1/5/10% изображений размечены, остальные скрыты; пять folds, среднее на val2017 (5k), COCO AP. Faster R-CNN/FPN, ImageNet ResNet-50. Baseline → Soft Teacher: `10.0±0.26 → 20.46±0.39`; `20.92±0.15 → 30.74±0.08`; `26.94±0.111 → 34.04±0.14`. Partial: 180k iterations, 8 GPUs × 5 images, SGD LR .01, drops 110k/160k, momentum .9, WD .0001. Full: все train2017 + 123k unlabeled2017, `40.9 → 44.5`, 720k iterations, 8×8 images, drops 480k/680k. Foreground threshold .9; labeled sampling ratio .2/.5, сокращается к нулю в последние 10k/20k. Jitter: 10, threshold .02; статья описывает uniform ±6%. Teacher получает слабые, student сильные преобразования. Критерий выбора лучшего checkpoint явно не восстановлен; нельзя молча назвать это одним last/best checkpoint. Это COCO detection, не CCTV events и не оценка RTX 4070.

### W1-09-F02 — Нельзя смешивать результаты README, статьи и inference threshold

**code-read/documentation; S02, Main Results/Notes/Requirements.** README сообщает для 1% baseline 10.0, ours 21.62 (`thr=5e-2`) / 22.64 (`thr=1e-3`); для 5% — 20.92 / 30.42 / 31.7; для 10% — 26.94 / 33.78 / 34.7. `thr` здесь именно **`model.test_cfg.rcnn.score_thr`**, а не teacher confidence cutoff. Все модели README обучены на 8×V100. Окружение авторов: Python 3.6, PyTorch 1.9.0, MMDetection `2.16.0+fe46ffe`, MMCV 1.3.9, Ubuntu 16.04. Доступность старого репозитория не доказывает его работоспособность в нашем пока неизвестном окружении. Причину всех расхождений README–paper одним score threshold не установлено; сохранять обе версии раздельно.

### W1-09-F03 — Что Soft Teacher реально делает с пропусками и координатами

**code-read; S03, названные функции.** Teacher заморожен для градиентов; labeled training выполняет student. Для unlabelled views сопоставляются filename, boxes переводятся матрицей teacher→student. На student proposals, назначенных background, `unsup_rcnn_cls_loss` заменяет вес на teacher background score. Так неоднозначный пропущенный positive не получает такой же жёсткий отрицательный вес, как уверенный background. Regression использует отдельный фильтр normalized uncertainty; `compute_uncertainty_with_aug` считает std координат после teacher regression относительно размеров boxes. Это не доказательство истинности box.

В `extract_teacher_info` не-float `pseudo_label_initial_score_thr` приводит к `NotImplementedError("Dynamic Threshold is not implemented yet.")`. Поэтому class-aware/dynamic threshold не следует выдавать за готовый аргумент этого кода. `aug_box` использует **`torch.randn × box_scale × frac`**, а не uniform распределение из F01. Это обнаруженное различие paper/code; для воспроизведения нужно выбрать и зафиксировать реализацию, а не смешать описания. Чтение не включало численную проверку jitter.

### W1-09-F04 — Версионный config SoftTeacher

**code-read; S04.** В `semi_wrapper.train_cfg`: `pseudo_label_initial_score_thr=0.5`, `rpn_pseudo_threshold=0.9`, `cls_pseudo_threshold=0.9`, `reg_pseudo_threshold=0.02`, `jitter_times=10`, `jitter_scale=0.06`, `unsup_weight=4.0`, `use_teacher_proposal=False`. Разные cutoff выполняют разные задачи; их нельзя свести к одному confidence.

`base.py`: Caffe-style R50, frozen norm; BGR normalize mean `[103.530,116.280,123.675]`, std `[1,1,1]`. Resize range `(1333,400)`–`(1333,1200)`, ratio preserved; weak: resize/flip, strong: дополнительно photometric/geometric/erase. Test `(1333,800)`, без flip, pad divisor 32. `SemiDataset` и branches `sup`, `unsup_teacher`, `unsup_student`; sampler `[1,4]`. `MeanTeacher(momentum=.999, interval=1, warm_up=0)`; SGD .01/.9/.0001, LR steps **120k/160k**, runner 180k; evaluation/checkpoint every 4k, fp16 dynamic loss scaling. LR 120k отличается от paper 110k. Это recipe на данном SHA, не «универсальные defaults» и не оптимум для СИЗ.

### W1-09-F05 — Partial config и запуск не адаптируют метод к новой голове автоматически

**code-read; S05.** Partial config задаёт 5 samples/GPU, 5 workers, JSON paths `instances_train2017.${fold}@${percent}.json` и `...-unlabeled.json`, `[1,4]`; default fold=1, percent=1. Launcher выбирает разные baseline/semi configs, параметры fold/percent передаются в MMDetection config. Для новой таксономии дополнительно требуются dataset registration/num_classes/checkpoint mapping и проверка loss, а для YOLO — иной интерфейс assignment/head; это наша интеграционная задача, отсутствующая в проверенных файлах.

### W1-09-F06 — EMA и inference stream — отдельные решения

**code-read; S06.** Hook клонирует student→teacher при нулевой итерации; фактический momentum на шаге — `min(momentum, 1-(1+warm_up)/(iter+1+warm_up))`, то есть заданные .999 не означают постоянные .999 с первого шага. Обновляются `named_parameters`. `MultiSteamDetector` направляет inference в выбранную submodule, а F04 задаёт `inference_on="student"`. Следствие: wrapper не требует двойного inference, но извлечение/экспорт одной ветви и совпадение выходов ещё нужно проверить; весь checkpoint teacher+student нельзя считать готовой LinQ моделью.

### W1-09-F07 — Unbiased Teacher v1: иной протокол и результат

**paper; S07, §3–4/Table 1/A.4.** COCO-standard: .5/1/2/5/10% размеченных изображений, остальные unlabeled; Faster R-CNN/FPN ImageNet R50, AP50:95. Для 1% supervised `9.05±.16`, UT `20.75±.12`; для 10% `23.86±.81 → 31.50±.10`. Оценивается **teacher**, поэтому эти значения не являются качеством student. 180k iterations, labeled/unlabeled batches 32/32; burn-in 1/2/6/12/20k соответственно доле разметки; SGD LR .01, momentum .9. Threshold .7, EMA .9996, unsup weight 4. Weak flip; strong color/grayscale/blur/cutout, без дополнительных geometry. Class-wise NMS, focal ROI classifier; unsupervised regression исключён: class confidence не измеряет качество координат. Appendix A.2.2: высокий .9 даёт мало boxes, слишком низкий threshold приводит к шуму/несходимости в исследованном режиме. COCO-additional: train2017 + unlabeled2017; Appendix A.4 описывает 360k включая 90k burn-in. Число независимых folds и точное best/last правило в прочитанном протоколе не установлены; знак ± не следует самостоятельно объявлять стандартным отклонением по пяти folds.

### W1-09-F08 — Авторский UT recipe и библиотека

**documentation; S08.** Авторский repo использует Detectron2; README требует Python ≥3.6, PyTorch ≥1.5 и совместимый torchvision, Linux/macOS. Пример запуска: 8 GPUs и overrides `SOLVER.IMG_PER_BATCH_LABEL 16`, `...UNLABEL 16`, хотя config F10 содержит 32/32. Поэтому «команда README + config» и «чистый config» — разные effective batch. Сборку текущих зависимостей и работу на Windows не проверяли. Не выводить совместимость из минимальных требований README.

### W1-09-F09 — UT online integration по trainer

**code-read; S09.** Loader возвращает четыре группы strong/weak labeled/unlabeled. Истинные labels unlabeled удаляются. До burn-up используются только labeled strong+weak; на границе teacher копирует student (`keep_rate=0`), затем EMA по config. Teacher no-grad на weak unlabeled, ROI predictions фильтруются scalar threshold, их hard boxes/classes передаются strong student. `loss_rpn_loc_pseudo` и `loss_box_reg_pseudo` явно умножаются на **0**, другие pseudo losses — на `UNSUP_LOSS_WEIGHT`; затем backprop/optimizer только student. Это supervised regression по labeled данным, а не полное отключение regression сети.

`threshold_bbox` для ROI использует `scores > thres`; class-wise threshold dictionary здесь нет. `build_hooks` раздельно оценивает student (суффикс `_student`) и teacher. Сохранить обе оценки и явно назвать экспортируемую ветвь; прирост teacher нельзя приписывать student. EMA не добавляет отсутствующие классы автоматически и не заменяет ручной контроль.

### W1-09-F10 — Точный UT 1% config

**code-read; S10.** `TwoStagePseudoLabGeneralizedRCNN`, `PseudoLabRPN`, `StandardROIHeadsPseudoLab`, ROI `FocalLoss`, RPN `CrossEntropy`; R50 weights `detectron2://ImageNetPretrained/MSRA/R-50.pkl`. Config: MAX_ITER 180000, steps `(179990,179995)`, LR .01, labeled/unlabeled 32/32, SUP_PERCENT 1.0, RANDOM_DATA_SEED 1, BBOX_THRESHOLD .7, BURN_UP_STEP 2000, EMA_KEEP_RATE .9996, TEACHER_UPDATE_ITER 1, UNSUP_LOSS_WEIGHT 4.0, evaluation every 1000, test `coco_2017_val`. Base INPUT short sides `(640,672,704,736,768,800)`; полный resolved preprocessing зависит также от Detectron2 version/defaults, не восстановлен. Почти весь run до двух последних LR drops имеет constant LR; сохранять literal config, не заменять его пересказом «обычный schedule».

### W1-09-F11 — Offline pseudo-labeling существует отдельно от EMA

**documentation; S11, Training steps 1–3.** STAC author workflow: обучить detector labeled → предсказать boxes/classes на unlabeled → обучить STAC с labeled+pseudo-labels и strong augmentation. README использует сохранённый `pseudo_data.npy`, `TRAIN.CONFIDENCE=.9`, `TRAIN.WU=2` и Faster R-CNN. Такой offline artifact можно инспектировать до обучения; это не автоматическое доказательство качества его labels. Предлагаемая нами ручная полная коррекция — дополнительная процедура, а не часть доказанного STAC recipe.

### W1-09-F12 — Почему перенос к one-stage нельзя считать заменой пары флагов

**paper; S12, §3.2–3.3 pp.4–5; documentation S13.** UTv2 разбирает FCOS: centerness×classification score и center sampling могут вести себя хуже при noisy pseudo-labels, чем соответствующие упрощения. Listen2Student сравнивает uncertainties teacher/student для отбора regression supervision; uncertainty требует добавленной ветви и специального обучения. Это свидетельство зависимости SSL от head/assignment, а не основание переносить FCOS вывод на любую версию YOLO. Код этой дополнительной ветви и её фактическое удаление/сохранение при экспорте здесь не проверялись.

## W1-09-F13 — Практический вывод: confidence ≠ correctness

**inference из F03/F07/F09/F12.** Score — внутренний выход модели после её обучения и postprocessing. Без отдельной эмпирической проверки на целевом домене он не равен вероятности «класс и bbox верны», тем более вероятности нарушения. Даже калиброванный class score не подтверждает IoU, полноту набора objects и правильную person–PPE association.

Аудит только принятых boxes оценивает precision, но скрывает missed positives. Аудит только uncertain frames скрывает confident errors и easy negatives. Для полноты нужна отдельная полностью вручную размеченная выборка кадров из train-domain с реальными негативами и независимыми сценами; инспектор должен искать все классы без подсказок teacher хотя бы на контрольной части. Считать one-to-one совпадения correct class + заранее заданный IoU, отдельно локализацию при верном классе и пропущенные объекты. Объекты ниже cutoff всё ещё могут быть positive, пустой output не подтверждает negative frame.

Class-aware threshold — **proposed**, выбирать по precision/coverage на calibration/audit данных; редкий класс с недостатком примеров оставлять в human review. Нельзя снижать cutoff только ради одинаковых counts по классам: распределение сцен может быть реально неравным. Если выбранный supervised loader трактует неуказанные объекты как background, одобрение отдельных boxes без дорисовки остальных создаёт partial-label проблему. Нужны полная коррекция кадра либо реально поддержанный ignore/masking loss; наличие ignore следует проверить в выбранном model_stack.

## Предлагаемые проверки следующей практической волны

Все E ниже **proposed, не выполнены**. Численные критерии принятия задаёт команда после получения классов/метрики и до просмотра сравнительных результатов; здесь не выдуман универсальный безопасный порог precision. Отсутствие достаточного числа редких positive — ограничение вывода, а не нулевая ошибка.

### W1-09-E01 — Аудит учителя и выбор политики допуска labels

**Вопрос/решение:** годится ли teacher как помощник предразметки, как источник unchecked pseudo-labels или только как средство отбора на ручную работу?

**Входы:** версия teacher/checkpoint, class map/box contract, целевой U_train, небольшие полностью размеченные audit/calibration frames из независимых camera/session/time групп; U_train не включает validation/holdout. До отбора зафиксировать sampling: случайные независимые сцены + страты размера/ночь/окклюзия/камеры/редкие positive/пустые outputs. Запись реальной частоты random части нужна, чтобы не выдать oversampled hard subset за общую частоту ошибок. Числа кадров — по фактическому наличию и бюджету.

**Действия:** (1) Сохранить raw predictions до cutoff, post-NMS predictions и preprocessing. (2) На части кадров сделать слепую полную human annotation, затем adjudication расхождений. (3) По нескольким заранее заданным cutoffs считать correct-class one-to-one precision, retained recall/coverage, IoU distribution/AP75-sensitive localization, counts accepted/rejected/FN по class/size/camera. (4) Оценить ручное время на пустую разметку и исправление предразметки на сопоставимых группах. (5) Если достаточно GT, отдельно проверить reliability score bins; не называть это универсальной калибровкой.

**Контроль:** одинаковые изображения, matching/IoU, NMS и preprocessing для всех cutoff; не менять teacher. Thresholds выбираются на calibration/audit, не на holdout. Если audit labels потом пойдут в train, они теряют независимый статус.

**Артефакты:** manifest split/group IDs, teacher hashes, raw outputs, audited GT, correction logs, таблицы TP/FP/FN/IoU с denominators, policy cutoff per class или route-to-review, annotator time. Отдельно фиксировать число независимых сцен, не только boxes.

**Исходы/stop:** если даже high score даёт систематический неверный class/box либо редкий класс почти не имеет coverage — запретить unattended auto-accept для этой страты, перейти к полной ручной коррекции/разметке. Если human correction не экономит время или создаёт omissions — отказаться от предразметки для этой страты. При малом числе positives вывод «не установлено», добрать независимые примеры, а не принять класс по общей precision. Успех подтверждает качество конкретной партии teacher outputs, но ещё не улучшение student и не LinQ.

### W1-09-E02 — Offline audited loop против обычного supervised adaptation

**Гипотеза:** исправленная teacher предразметка даёт полезные дополнительные сцены и экономит annotation time. **Входы:** прошедший E01 teacher, runnable baseline student от model_stack, labeled L_train, фиксированный U_train, V_validation и закрытый H_holdout из других сессий/камер согласно целевому claims. Кадры одной сцены/track не разносить по этим частям. Для adaptation claim заранее объявить, какие target streams участвовали в подготовке.

**Контроль и действия:** A — student на исходном L; B — тот же student на L + полностью исправленных pseudo-preannotations. Зафиксировать architecture/checkpoint, preprocessing, optimizer budget, seed, augmentations, class map, validation cadence и inference thresholds. Дополнительный полезный контроль C — та же annotation time на обычную ручную разметку без teacher; не смешивать «тот же набор изображений» и «тот же человеческий бюджет», отчёт должен показать оба ограничения. Студента обучать с supervised losses, если labels полностью исправлены; это не воспроизведение Soft Teacher. При проверке unchecked labels завести отдельную D-arm с явным статусом noisy/partial и поддержанным loss, не подмешивать их в B.

**Метрики:** student AP50:95/per-class AP, critical-class recall при одинаковом FP budget, AP small/IoU/localization, validation slices новых камер и прежнего домена, annotation minutes/corrected positive, время обучения. Выбор checkpoint и cutoff только по V. Сначала сравнить на V; H открыть для зафиксированного кандидата по принятому evaluation protocol, не использовать H для следующего выбора threshold/кадров. Повтор seed/group comparison — если первый эффект мал относительно наблюдаемой вариативности и остаётся время.

**Артефакты:** A/B/C configs, corrected dataset version и provenance каждого label, исключённые frames, teacher prediction/correction trail, seeds/logs, выбранный **student** checkpoint, class map, inference-output examples; export manifest отдельно.

**Исходы/stop:** принять B, если заранее заданный practically useful validation gain/annotation benefit достигнут без запрещённой регрессии критичных slices и подтверждён выбранным holdout протоколом. Если validation деградирует/critical recall падает — вернуть A, анализировать ошибки labels до следующего прогона. Ограничить заранее число итераций и compute/annotation budget; две порции подряд без заранее заданного полезного изменения — основание закончить эту ветку (предлагаемое правило, не paper recommendation). После просмотра H, если нужно менять модель, следующий результат требует нового нетронутого тестового материала или честного статуса повторно использованного holdout. Успех FP student не подтверждает export/quantized/LinQ и event quality.

### W1-09-E03 — Gate для online EMA integration

**Вопрос:** стоит ли цена online teacher/student training последующего полноценного trial? **Входы:** runnable exact pinned repo/совместимый trainer, L/U/V/H как E02, supervised checkpoint, confirmed available VRAM/OS, известный deployable student path. В отсутствие runnable implementation для выбранной головы остановить online-ветку, продолжить E02.

**Действия:** сначала небольшой инженерный smoke check: labelled/unlabelled separation; отсутствие скрытого GT в U; геометрическое соответствие weak→strong boxes; no-grad teacher; обновление student и EMA; loss weights; empty pseudo-label batch; сохранение/reload teacher/student/optimizer/iteration. Для SoftTeacher проверить normalized jitter и source-code Gaussian/paper uniform discrepancy; для UT v1 проверить нулевые pseudo regression losses при ненулевом supervised regression. Затем ограниченный paired trial supervised vs online с тем же student backbone, L/U groups, доступным training budget и одинаковым inference policy; отличия compute считать, а не скрывать.

**Teacher quality audit:** фиксированные независимые audit frames E01 проверять в заданные checkpoint моменты, логировать per-class accepted counts/precision/coverage/localization. Рост числа confident boxes без роста correct coverage — сигнал feedback bias. Audit используется для диагностики/selection и не является H.

**Метрики/артефакты:** раздельные teacher/student V metrics, loss traces, teacher drift/EMA state, pseudo class histogram с denominators, actual wall-clock/peak VRAM, full resolved config/repo/dependency lock, выбранный отдельный student, raw output contract и reload parity. Нельзя выбрать teacher по V, экспортировать student и сообщить teacher AP.

**Stop:** ошибки labels/splits/transforms/gradient routing, nonfinite losses, систематическое исчезновение редких pseudo classes или ухудшение критичного validation slice — остановить, исправить integration либо вернуться к supervised/offline route. Если smoke check/короткий trial исчерпал заранее отведённый инженерный бюджет без пригодного student — не превращать оставшиеся часы в переписывание trainer. Финальный допуск только после полной controlled comparison; короткий успех подтверждает работоспособность loop, не published gain, не LinQ и не редкие события.

## Открытые вопросы и адресная передача

- **W1-09-Q01 → datasets/evaluation (высокий):** какие классы действительно наблюдаемы и полностью размечены; что означает absence/no-helmet, где ignore/occlusion; разрешено ли использовать предоставленный unlabeled target stream для adaptation? Полный кейс и audit E01, не поиск универсального threshold.
- **W1-09-Q02 → model_stack (высокий):** какая конкретная student architecture/version имеет runnable supervised trainer, class/box contract и export? Есть ли проверенная SSOD implementation именно этой головы и partial-label loss? Проверенные здесь Faster R-CNN repos и FCOS UTv2 не закрывают вопрос YOLO.
- **W1-09-Q03 → evaluation (высокий):** независимые camera/session группы для audit/calibration/V/H и минимально полезное изменение/критичная регрессия; сколько фактических positive для каждой редкой страты? Увеличение коррелированных кадров не закрывает нехватку независимых событий.
- **W1-09-Q04 → model_stack/W2:** paper/code discrepancies: SoftTeacher LR 110k vs 120k, uniform vs Gaussian jitter; README AP vs paper AP; UT reader commands 16/16 vs config 32/32; точное checkpoint selection и run/fold variability. Для воспроизведения выбрать один полностью resolved recipe и сравнивать внутри него, не объединять удобные части.
- **W1-09-Q05 → linq_platform/video_architecture:** извлечённый student checkpoint, preprocessing, shape/class map, postprocessing и output contract должны пройти реальный export/runtime путь. Teacher работает offline/при обучении и не обязан исполняться на LinQ; это не снимает требований к student. Доступа/измерений LinQ у этой ветки нет.
- **W1-09-Q06 → violation_methods:** teacher boxes не являются подтверждённым нарушением. Ошибка связи person–PPE, temporal state, опасной зоны и невидимого объекта может не устраняться pseudo-labeling; audit должен отделить detector failure от отсутствия наблюдаемого сигнала/ошибки правила.

Ветка даёт основание начать с E01 и выбрать E02 либо E03. Она не устанавливает наличие target data, допустимые классы, качество какого-либо teacher на заводских камерах, экономию времени в минутах, достижимый прирост student или поддержку LinQ.
