# W1-10 — Offline teachers, VLM и distillation

Исследование: 23.10.2026; фактический локальный timestamp во время сетевой проверки 2026-10-23T06:57:36+03:00. Контекст: mosprom-research-v1. Прочитаны Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md и W1-10 из _WORK/AGENT_PROMPTS.md. Здесь только ветка W1-10. Полного кейса, target data, установленной версии training stack и SDK LinQ нет. RTX 4070 не означает установленный объём VRAM.

**Решение:** в актуальном Ultralytics действительно есть штатная feature distillation; это установлено по конфигурации, trainer и отдельному модулю, а не только по статье. Условия ниже привязаны к `8.4.184`, commit `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`. Для нашей команды разумны два разных кандидата: offline предразметка grounded vision-language detector с проверкой человеком; либо KD от уже хорошего целевого детектора той же YOLO family к выбранному student. Их полезность ещё не проверена. Ни один путь не устанавливает поддержку student на LinQ.

Фактически выполнено: поиск в сети, открытие первичных docs/papers/code, чтение pinned raw файлов и GitHub API метаданных. Не выполнено: установка библиотек, загрузка весов, предсказания, annotation trial, обучение, export, benchmark, исполнение на LinQ. Все E-процедуры ниже — предложения следующей практической волне.

## 1. Какие механизмы нельзя смешивать

| Механизм | Что передаётся | Требования к сопоставлению | Что останется в deployment |
|---|---|---|---|
| Предразметка | Boxes, фразы, scores → исправленные labels | Ontology, геометрия координат, полнота разметки | Обычный обученный student; teacher может отсутствовать уже во время его обучения |
| Отбор кадров | Disagreement, неопределённость, найденные редкие объекты | Единица независимости, sampling budget, отдельный test | Student, обученный на выбранных и размеченных данных |
| Offline pseudo-label training | Неисправленные/отфильтрованные teacher boxes как targets | Class mapping, ignore для неполной разметки, качество labels | Student; детали SSL — → W1-09 |
| Feature KD | Intermediate tensors с дополнительным loss | Spatial strides/levels, channels, одинаковый преобразованный вход | Student без teacher/projectors при корректном извлечении |
| Logit KD | Soft class distributions | Одинаковая семантика и порядок классов, foreground/background, соответствие locations/queries | Student; один temperature из classification не решает matching детектора |
| Localization KD | Распределения координат/box regression outputs | Представление box, anchors/points, scale, bins, assignment | Student с исходным head, если inference path не изменён |
| Ensemble как teacher | Совмещённые detections либо отдельные feature teachers | Ontology, дубликаты, fusion/matching и confidence calibration | Один student только при отдельном обучении; ensemble inference сам по себе сжатием не является |

Таблица — наш инженерный вывод по найденным интерфейсам, не опубликованное сравнение эффективности. Grounding DINO с языковым grounding далее обозначен VLM-помощником; это не утверждение, что любая generative chat VLM выдаёт пригодные detection labels. Свободный текст о наличии каски нельзя автоматически превратить в bounding box или метку «человек без каски».

## 2. Реестр открытых первоисточников

У всех S-ID дата доступа **2026-10-23 MSK**. Commit dates отделены от даты доступа. Плавающие docs не равны установленному пакету команды. Raw-файлы реально получены; веса по указанным ссылкам не скачивались. Полные чужие тексты не сохранялись.

| S-ID | Источник, версия/дата | Direct URL и локатор | Основание |
|---|---|---|---|
| W1-10-S01 | Ultralytics, Knowledge Distillation; live docs, точная дата публикации не установлена (страница показывает относительные created/updated) | https://docs.ultralytics.com/guides/knowledge-distillation ; Quickstart, Performance, Prerequisites, Task Support, Training Output | Документация и заявленные автором benchmark; F01/F02 |
| W1-10-S02 | Ultralytics package metadata, pinned commit U=`e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, commit date 2026-10-22T20:27:18Z | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/__init__.py ; `__version__`; https://api.github.com/repos/ultralytics/ultralytics/commits/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 | Код/метаданные; F01 |
| W1-10-S03 | Ultralytics `default.yaml`, U | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/default.yaml ; `distill_model`, `dis`, `cls_remap` | Конфигурация; F01/F05 |
| W1-10-S04 | Ultralytics BaseTrainer, U | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py ; `_setup_train`, `setup_model`, `final_eval` | Реальная интеграция; F03/F06 |
| W1-10-S05 | Ultralytics DistillationModel, U | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/distill_model.py ; `__init__`, `get_distill_layers`, `loss`, `loss_sl2`, `decouple_outputs`, `fuse` | Чтение реализации; F04/F05 |
| W1-10-S06 | Ultralytics torch utils, U | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/torch_utils.py ; `ModelEMA.__init__`, `strip_optimizer` | Различие training checkpoint / final student; F06 |
| W1-10-S07 | YOLO26 architecture, U | https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/models/26/yolo26.yaml ; `nc`, `reg_max`, scales, layers 16/19/22/23 | Graph specification; F04/F12 |
| W1-10-S08 | Yang et al., Focal and Global Knowledge Distillation for Detectors, arXiv v2 2022-03-09, CVPR 2022 | https://arxiv.org/html/2111.11837v2 ; §4.1–4.3 Table 2, Appendix E | Published detection protocol; F07 |
| W1-10-S09 | Author FGD repo, commit F=`c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d`, 2022-09-04T12:09:36Z | https://github.com/yzd-v/FGD/tree/c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d ; README Install/Add and Replace/Test | Dependencies/integration; F08 |
| W1-10-S10 | FGD RetinaNet R101→R50 recipe, F | https://raw.githubusercontent.com/yzd-v/FGD/c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d/configs/distillers/fgd/fgd_retina_r101_fpn_2x_distill_retina_r50_fpn_2x_coco.py ; `teacher_pretrained`, `distill_cfg`, `student_cfg`, `teacher_cfg` | Concrete mapping; F08/F09 |
| W1-10-S11 | FGD distiller + losses, F | https://raw.githubusercontent.com/yzd-v/FGD/c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d/mmdet/distillation/distillers/detection_distiller.py ; `forward_train`, `simple_test`; https://raw.githubusercontent.com/yzd-v/FGD/c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d/mmdet/distillation/losses/fgd.py ; `FeatureLoss.forward` | Tensor/GT contract; F09 |
| W1-10-S12 | FGD checkpoint conversion, F | https://raw.githubusercontent.com/yzd-v/FGD/c03a6cf3b3cb3cbfd5554dbf4766e7135747d22d/pth_transfer.py ; `change_model` | Student extraction; F09 |
| W1-10-S13 | Zheng et al., Localization Distillation for Dense Object Detection, arXiv v3 2021-11-25, CVPR 2022 | https://arxiv.org/html/2102.12252v3 ; §3.2–3.4, §4.1, Tables 1–3 | Distribution vs boxes and controlled detection ablations; F10 |
| W1-10-S14 | Author LD repo, commit L=`4287990ca27f51f6f15dc66d28bb420a053c307e`, 2024-10-24T07:30:53Z | https://raw.githubusercontent.com/HikariTJU/LD/4287990ca27f51f6f15dc66d28bb420a053c307e/configs/ld/ld_r18_gflv1_r101_fpn_coco_1x.py ; https://raw.githubusercontent.com/HikariTJU/LD/4287990ca27f51f6f15dc66d28bb420a053c307e/mmdet/models/dense_heads/ld_head.py ; `loss_single`; https://raw.githubusercontent.com/HikariTJU/LD/4287990ca27f51f6f15dc66d28bb420a053c307e/mmdet/models/detectors/kd_one_stage.py ; `forward_train`, `__setattr__` | Concrete non-YOLO implementation; F11 |
| W1-10-S15 | Liu et al., Grounding DINO, arXiv v4 2023-03-20 (эта версия, не все последующие публикации) | https://arxiv.org/html/2303.05499v4 ; §4.2, Tables 1/2, Appendix I | Open-set teacher protocol; F13 |
| W1-10-S16 | Author GroundingDINO README, commit G=`856dde20aee659246248e20734ef9ba5214f5e44`, 2024-08-12T08:52:02Z | https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/856dde20aee659246248e20734ef9ba5214f5e44/README.md ; Explanations/Tips, Install, Demo | Config/weights and tool boundaries; F14 |
| W1-10-S17 | GroundingDINO inference API, G | https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/856dde20aee659246248e20734ef9ba5214f5e44/groundingdino/util/inference.py ; `load_image`, `predict`, `predict_with_classes`, `post_process_result`, `phrases2classes` | Coordinate/token/class conversion; F15 |

### Сбои доступа и маршрут проверки

`https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/utils/distillation.py` вернул 404: это был неверно угаданный path, а не свидетельство отсутствия KD. Открытый `engine/trainer.py` вывел к правильному `nn/distill_model.py`. Аналогично неверный FGD path `configs/fgd/fgd_faster_rcnn_r101_fpn_2x_coco.py` дал 404; GitHub tree API выявил `configs/distillers/fgd/...`. PowerShell `Invoke-WebRequest` без `-UseBasicParsing` дал локальный NullReferenceException; повтор с этим параметром получил raw-текст. Никаких отрицательных capability-выводов из этих сбоев не сделано.

## 3. Факты и конкретные маршруты

### W1-10-F01 — Штатный KD Ultralytics существует в проверенной версии

**Тип: docs + код, не запуск.** S01–S04. Guide открывается с redirect от URL с trailing slash к URL без него. `__version__ = "8.4.184"`; в defaults есть `distill_model` и `dis: 6.0`. BaseTrainer импортирует `DistillationModel` и при заданном teacher path создаёт wrapper. Это положительное доказательство реализации. Минимальный официальный пример: student `yolo26n.pt`, teacher `yolo26s.pt`, вызов `model.train(data="coco8.yaml", epochs=100, distill_model="yolo26s.pt")`. `coco8.yaml` — демонстрационный вход, не протокол оценки промышленного CCTV.

### W1-10-F02 — Поддержка и опубликованный benchmark имеют границы

**Тип: документация/измерение производителя.** S01. Docs требуют одну YOLO family и одинаковую task; cross-family не поддерживается. Реализованы detect/segment/pose/obb, но accuracy benefit экспериментально подтверждён автором только для detect; classify/semantic/depth/RT-DETR исключены. Таблица COCO val2017, single-model single-scale, 640 px: YOLO26n baseline 40.9 → distilled 41.5 mAP50–95; e2e 40.1 → 40.9. NMS/e2e пути различаются. Label budget, полный training compute, seed variance и checkpoint selection из этой таблицы не восстановлены. Это не обещание +0.6 AP на PPE.

### W1-10-F03 — Путь trainer и цена online KD

**Тип: чтение кода.** S04. `_setup_train` отключает `compile` при `distill_model`, защищает teacher parameters от размораживания, создаёт wrapper до EMA/optimizer; DDP использует `find_unused_parameters` при выключенном compile. `setup_model` при resume восстанавливает student и teacher по сохранённому `distill_model`, затем projector weights. Следствие: teacher path/веса нужно сохранять для продолжения training; готовый inference artifact этого требования иметь не должен. Exact wall-clock, VRAM и стоимость облака неизвестны. Нужны как минимум teacher forward на каждом batch плюс student forward/backward; это измеряемая дополнительная стоимость, а не универсальный множитель «вдвое».

### W1-10-F04 — Что конкретно сопоставляется у Ultralytics

**Тип: чтение кода.** S05/S07. `get_distill_layers` находит `Detect`, возвращает его входы и head. Для YOLO26: `[16,19,22,23]`, neck P3/8, P4/16, P5/32. Каждый student feature проходит Conv1×1→ReLU→Conv1×1 к teacher channels; затем score-weighted L2. Weight — максимум sigmoid teacher class score в location; для end-to-end head сначала усредняются one2many/one2one scores. Teacher frozen/eval/no_grad; обе модели видят один `batch["img"]`. Одинаковое число levels проверяется явно. Пространственный размер автоматически не ресемплируется. Это feature guidance, не KL logits и не teacher-box regression. Локаторы: `__init__`, `loss`, `loss_sl2`.

### W1-10-F05 — Class/head mapping нельзя считать решённым автоматически

**Тип: код + наш вывод.** S05/S03. В просмотренном wrapper нет semantic class remapping; confidence берётся через максимум по teacher classes. Поэтому совпадение `nc` само по себе недостаточно: до KD зафиксировать `class_id→name→definition` обеих моделей и task. `cls_remap` в defaults относится к переносу pretrained classifier rows при fine-tuning; это не доказательство semantic remapping teacher в KD. Нет явной проверки одинаковой family в прочитанном constructor: code-level возможность создать пару не расширяет documented support. Несовместимые spatial grids или head output contracts могут сломать loss; одинаковое число levels этого не исключает.

Практический условный путь: сильный **целевой** teacher той же family → student той же ontology/входных каналов/разрешения → обычные supervised losses + KD. Загруженный COCO teacher без требуемого PPE-класса не становится учителем этого класса от добавления `distill_model`.

### W1-10-F06 — Final student и промежуточный checkpoint различаются

**Тип: чтение кода.** S04/S06. EMA удаляет teacher из своей копии wrapper. Training checkpoint поэтому может всё ещё содержать wrapper/projectors и путь teacher для resume. В штатном `final_eval` вызывается `strip_optimizer` для last и best; там убираются feature hooks, wrapper заменяется `student_model`. `fuse` также возвращает student. Следовательно, нормальный законченный путь предназначен для стандартного student graph. Прерванный run/ручное сохранение нельзя объявить таким же artifact без осмотра. Реальный сохранённый .pt и ONNX в этой работе не проверялись. Приёмка должна отдельно доказать загрузку/инференс без teacher file и отсутствие KD узлов в exported graph (E03).

### W1-10-F07 — Detection-specific KD: FGD даёт доказательство идеи, а не рецепт YOLO

**Тип: опубликованное измерение.** S08, §4.1–4.3 Table 2. COCO, 80 classes, авторы описывают около 120k train и 5k validation images; supervised boxes, не few-shot. 24 epochs SGD, momentum 0.9, weight decay 0.0001; MMDetection. Teacher RetinaNet ResNet101: 38.9 AP; student ResNet50 baseline 37.4; FGD 39.6, с inheriting neck/head 39.7. APsmall: 20.6 baseline против 22.9 FGD без inheriting. Inheriting требует одинаковой head structure. Полная стоимость teacher training, GPU/time и критерий checkpoint selection здесь не установлены. Appendix E прямо отмечает риск наследования teacher biases. Исследованные здесь студенты не дают основания переносить величину gain на nano YOLO/PPE.

### W1-10-F08 — Конкретный FGD route и integration debt

**Тип: author repo/config.** S09/S10. Репозиторий требует `mmdet==2.11.0`, `mmcv-full==1.2.4`; необходимо добавлять distillation module и заменять `mmdet/apis/train.py`, `tools/train.py`. Это отдельный legacy training stack.

Recipe `configs/distillers/fgd/fgd_retina_r101_fpn_2x_distill_retina_r50_fpn_2x_coco.py`:

- teacher config `configs/retinanet/retinanet_r101_fpn_2x_coco.py`;
- teacher checkpoint `https://download.openmmlab.com/mmdetection/v2.0/retinanet/retinanet_r101_fpn_2x_coco/retinanet_r101_fpn_2x_coco_20200131-5560aee8.pth`;
- student config `configs/retinanet/retinanet_r50_fpn_2x_coco.py`;
- hooks `neck.fpn_convs.0.conv` … `.4.conv` ↔ одноимённые teacher modules, 256→256 channels; `init_student=True`;
- config: `temp=.5`, `alpha_fgd=.001`, `beta_fgd=.0005`, `gamma_fgd=.0005`, `lambda_fgd=.000005`, SGD lr .01, samples_per_gpu 2.

Здесь есть существенное расхождение recipe и paper: для anchor-based one-stage §4.2 paper сообщает gamma 0.001, а pinned recipe — 0.0005. Не исправлять молча; для воспроизведения выбирать и фиксировать конкретный recipe. Это ещё одна причина не подавать paper table как гарантированный результат произвольного переноса.

### W1-10-F09 — FGD использует GT geometry, extraction предусмотрен отдельно

**Тип: код.** S11/S12. Teacher извлекает features под no_grad, student считает свой supervised loss. FGD использует `gt_bboxes` и `img_metas` для foreground/background masks; `FeatureLoss` требует одинаковых H×W, при различии channels добавляет 1×1 align. Поэтому просто подать неполную VLM-предразметку как исчерпывающие GT boxes меняет маски и supervision. Semantic output KD в этом рецепте не выполняется; neck/head inheritance отдельно требует совместимых параметров и ontology. `simple_test` делегирует student; `pth_transfer.py` выбирает только ключи с prefix `student.`, снимает prefix и удаляет optimizer. Финальный graph должен быть обычный RetinaNet R50-FPN; export этого конвертированного checkpoint и LinQ не проверены.

### W1-10-F10 — Localization distribution KD отличается от hard boxes и class logits

**Тип: paper measurement.** S13 §4.1/Table 2–3. COCO train2017 118k, val2017 5k; ablations single-scale 1×=12 epochs, GFocal settings; baselines переобучены авторами в тех же условиях. GFocal R101 teacher → R50 student: 40.1 baseline → 42.1 AP при Main KD + Main LD + VLR LD; добавление VLR class KD даёт 42.0. Main class KD отдельно 40.2; Main LD 41.1. LD передаёт распределения границ, а не только decoded teacher box. Для R34→R18 в отдельной абляции pseudo-box regression 35.9 при baseline 35.8 против LD 36.3. Это протокол COCO, не наша оценка; seed variance, teacher-training budget и checkpoint selection не установлены.

### W1-10-F11 — Concrete LD mapping и причина не копировать loss в любой YOLO

**Тип: код/config.** S14. Recipe `ld_r18_gflv1_r101_fpn_coco_1x.py` строит student ResNet18-FPN/`LDHead`, teacher `configs/gfl/gfl_r101_fpn_mstrain_2x_coco.py`; checkpoint:

https://download.openmmlab.com/mmdetection/v2.0/gfl/gfl_r101_fpn_mstrain_2x_coco/gfl_r101_fpn_mstrain_2x_coco_20200629_200126-dd12f847.pth

Студент: 80 classes, 5 FPN levels, strides `[8,16,32,64,128]`, `reg_max=16`; LD KL weight .25/T=10. Input resize 1333×800 keep_ratio, normalization/pad32. `LDHead.loss_single` reshapes student и teacher box logits в `4*(reg_max+1)` и class logits в одинаковый `cls_out_channels`; locations сопоставляются по сетке/level. Teacher не регистрируется как nn.Module через `__setattr__`, forward_train получает teacher outputs без градиента. В inference используется student single-stage path. Это требует точного совпадения представления/сетки/классов, а не названия «детектор». Checkpoint/export отдельно не запускались.

### W1-10-F12 — DFL-free YOLO26 не является drop-in LD student

**Тип: architecture config + наш вывод.** S07/S14. В pinned YOLO26 `reg_max: 1`, `end2end: True`, три P3–P5 levels. В рассмотренном LD student reg_max16 и пять levels. Следствие: перенос localization-distribution loss требует другой реализации/head contract; установить один коэффициент LD в штатный YOLO trainer недостаточно. Нативный YOLO KD выше использует features и обходит это несовпадение. Менять head ради LD — значит заново исследовать graph/export/исполнение, что существенно для LinQ.

### W1-10-F13 — Grounding DINO измеряет open-set detection, не достоверность preannotation

**Тип: опубликованное измерение.** S15 §4.2/Table 2: Grounding-DINO-T/Swin-T, pretrain O365+GoldG+Cap4M, COCO val2017 zero-shot 48.4 AP, fine-tune 57.2. Именно T соответствует предлагаемому ниже OGC teacher path по README model zoo. Более известные 52.5 AP относятся к Swin-L/O365+OI+GoldG, а ODinW mean 26.1 — к другой L-модели с более широким pretraining. Их нельзя приписывать Swin-T checkpoint. Это не качество конкретной каски/респиратора на CCTV и не проверка student после pseudo-label training. Grounding pretraining помогает сформировать кандидатов; маленький/закрытый объект, отношения ношения и отрицательное состояние требуют целевого audit. Teacher benchmark его не заменяет.

### W1-10-F14 — Доступный offline teacher path

**Тип: author README.** S16. Доступны config `groundingdino/config/GroundingDINO_SwinT_OGC.py` и веса `https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth`. README описывает 900 candidate boxes с similarities к input words, `box_threshold` и `text_threshold`, разделение class names точками. Отмечены CPU-only inference и CUDA extension installation; training code в TODO не помечен завершённым. Не утверждается, что README установка работает на нашей ОС/GPU. Этот route выбирается для offline inference/предразметки, а не как доказательство готового fine-tuning trainer.

### W1-10-F15 — Слабое место VLM→class IDs конкретно видно в коде

**Тип: код.** S17. `predict` возвращает normalized cxcywh boxes, max token sigmoid scores и phrases; image resize short side800/max1333 с ImageNet normalization. `post_process_result` масштабирует исходными W/H, переводит cxcywh→xyxy. `predict_with_classes` соединяет class names через точки; `phrases2classes` выбирает первый class string, являющийся substring phrase, иначе None. Это не semantic ontology resolver: похожие имена/комбинированные phrases могут ошибочно сопоставиться. Предлагаемый путь в student: explicit phrase→canonical-class table + unknown/review + человек проверяет все целевые instances → YOLO/COCO labels → обычный fine-tuning выбранного student. Ни токен scores, ни совпадение фразы не превращают предразметку в GT.

## 4. Как выбирать route при неизвестных данных

Это условные рекомендации/выводы, не результаты наших испытаний.

| Наблюдаемая ситуация | Кандидат | Gate до дорогой работы | Цена/ограничение |
|---|---|---|---|
| Нет target labels, нужны boxes существующих визуальных объектов | GroundingDINO preannotation + human review | E01: полезность и correction cost по классам | Offline teacher GPU/CPU time, integration координат/ontology, исправление пропусков |
| Student уступает сильному target teacher той же family; data/ontology уже корректны | Native Ultralytics feature KD | E02 + E03 | Дополнительный forward и feature memory, compile disabled; teacher может не добавлять нужный сигнал |
| Плохая локализация при совместимом distribution head и уже есть MMDetection stack | LD как отдельная исследовательская ветка | Tensor contracts и baseline parity | Legacy dependencies, новый loss/trainer; не первый произвольный YOLO эксперимент |
| Нужен heterogeneous backbone teacher/student и есть рабочий legacy FGD stack | FGD | GT completeness, одинаковые feature grids, recipe/version | Porting/hooks/checkpoint conversion; paper improvement не переносится численно |
| Сильный teacher на том же материале тоже систематически пропускает маленький СИЗ | Data/scale/annotation диагностика → W1-06/08 | Видимость и независимый label audit | Копирование ошибки KD само по себе не добавит наблюдаемого сигнала |
| Ensemble/VLM видит «нарушение», но нет определения person-object/event relation | Уточнить observation/ontology → violation_methods | Действительно ли визуального кадра достаточно | Нельзя переносить scene-text response прямо в object-level labels |

Для native KD не требуется teacher в realtime pipeline. Для предразметки teacher вообще можно вынести в отдельную среду; student deployment cost определяется student graph, input size и postprocessing. Но «teacher offline» не отменяет затраты на обработку пула, хранение provenance и проверку. Если учитель обучается специально для KD, его training budget включается в стоимость route. Считать только финальную эпоху student было бы нечестно.

В 45-часовом кейсе нет установленного времени на интеграцию. Приоритет KD условен: он повышается, если target teacher и рабочий same-family trainer уже имеются; снижается, если сначала нужно обучить teacher, переносить legacy stack или выяснять ontology. Эти критерии полезнее неподтверждённого обещания «улучшим компактную модель за N часов».

## 5. Предлагаемые контролируемые E-процедуры

### W1-10-E01 — Ускоряет ли VLM-предразметка получение правильных target labels?

**Гипотеза/решение:** teacher экономит ручную работу без ухудшения labels. Входы: заранее определённые классы/определения, train-only pool независимых camera/session clips, маленький независимый вручную полностью размеченный audit subset, G commit/config/checkpoint hash. Test/lockbox не входит в pool. Нужны среда inference и annotation UI; точные размеры subset определяются доступными сценами, не выдумываются здесь.

**Контроль:** ручная разметка сравнимой группы с той же полнотой/инструкцией; распределение камер/scale/occlusion согласовать до сравнения. Изменение: только наличие предразметки. Зафиксировать prompts, token/class table, box/text thresholds на development audit; после выбора не менять их по lockbox.

**Действия/метрики:** проверить pixel-coordinate overlays после каждого resize/conversion, class/unknown mapping; измерить label precision/recall/IoU по классу и размеру, пропуски, ошибочные отрицательные состояния, время до полностью исправленного изображения/instance, число исправлений. Отдельно проверять кадры без detections — иначе пропуски скрыты. Correction cost сравнивать вместе с полнотой, а не только с количеством нарисованных boxes.

**Артефакты:** image hashes/splits, original teacher outputs, corrected labels, prompts/thresholds, code/config/weight hashes, времена и audit disagreements. **Исходы:** принять как annotation assistance; оставить только для отбора/поиска; отказать для конкретного класса. **Stop:** систематические неоднозначные состояния/пропуски не исправляются дешевле ручной разметки либо нарушена геометрия/полнота. **Предел:** хороший audit не доказывает качество student, event logic или LinQ; auto labels остаются predictions до проверки.

### W1-10-E02 — Даёт ли native feature KD пользу сверх обычного fine-tuning?

**Входы:** утверждённый train/val split по camera/session, полностью размеченные требуемые classes; baseline student/checkpoint; уже проверенный target teacher той же family/task, U commit или явно новая pinned версия; совместимые levels/shapes. Проверить teacher quality на development material отдельно; не выбирать его по final test. VRAM/драйверы устанавливаются измерением.

**Контроль:** A — supervised student, B — тот же student/init/data/transforms/optimizer/effective batch/resolution/seed/updates + `distill_model`, `dis=6.0` как versioned default, не оптимум. Любые дополнительные `dis` значения — отдельная заявленная абляция. Чтобы не спутать вычисления и метод, записать и одинаковые updates, и wall-clock; не выдавать сравнение разного числа updates за чистый loss effect.

**Действия:** сначала один batch: neck shapes/strides, class contracts, teacher eval и неизменность weights/BN, student/projector gradients, конечность loss, teacher no_grad. Затем небольшой диагностический training; только после корректности — сопоставимый trial. Логи: supervised components и dis_loss, peak allocated/reserved VRAM, step time с прогревом, data loading, весь teacher preparation cost. Validation: AP50–95/APsmall/per-class recall, false detections на релевантном фоне; итоговые event metrics передать evaluation. Threshold/NMS фиксируются в паре.

**Артефакты:** resolved args, package/commit, dataset/class map, seed, init/teacher hashes, logs, selected checkpoints, raw predictions, timing configuration. **Исходы:** B улучшает релевантные ошибки в пределах заранее заданной practical acceptance; эффекта нет; редкие классы ухудшаются; teacher bias наследуется. Повтор seed/группы оправдан, если наблюдаемый gain мал или нестабилен. **Stop:** контракты не сходятся, teacher не лучше на нужных ошибках, memory/time budget не позволяет сравнимый trial, или early validation показывает существенный вред critical class. **Предел:** один trial не доказывает перенос на другие камеры/классы; `.pt` качество не подтверждает export/LinQ.

### W1-10-E03 — Финальный artifact действительно содержит только student?

**Входы:** нормально завершённые A/B runs E02, immutable copies промежуточного и final checkpoint, точный export path из model_stack, target SDK от linq_platform. **Контроль:** student той же архитектуры без KD. **Действия:** сохранить manifest module types/keys/shapes/params; сравнить wrapper checkpoint до и final после `strip_optimizer`; загрузить финал в чистом процессе без teacher weights/доступа к его path; выполнить inference. Проверить отсутствие teacher/projector/hooks в final model и ONNX, входы/выходы, формы, decoding/NMS. Exported outputs сравнить с .pt на одних изображениях и одной обработке; затем выполнить реальную target compile/inference.

**Метрики:** reload success, dependency on teacher, file/parameter/graph-op counts, численные расхождения outputs, AP/critical recall до/после export и quantization, target latency/throughput/memory. **Артефакты:** source/final/export hashes, graph inspection, environment, compiler/runtime logs, raw outputs и реальное доказательство LinQ execution. **Исходы:** student-only artifact пригоден к дальнейшей target проверке; wrapper не снят; exporter/SDK отвергает graph; качество меняется после conversion. **Stop:** teacher требуется для inference, graph не соответствует утверждённому student или target path не получен. **Предел:** одинаковый parameter count/файл не доказывает одинаковую скорость; успешный ONNX Runtime тест не доказывает LinQ.

### W1-10-E04 — Только при наличии рабочего MMDetection: FGD/LD integration gate

**Входы:** pinned F или L env; выбранная recipe; train/val/classes, teacher weights; baseline в той же framework. **Контроль:** обычный student с теми же updates/preprocessing/initialization. Inheriting отделить от distillation: иначе эффект начальных neck/head weights смешан с KD. **Действия:** dry-run tensor/coordinate checks, один training batch, сохранение и student extraction; затем небольшой сопоставимый trial, если путь не требует перестройки выбранного deployment graph. **Метрики:** gradients/losses, memory/time, AP/critical errors; фиксировать paper/config gamma discrepancy для FGD. **Артефакты:** env lock, recipe diff, teacher/config hashes, converted student, validation predictions. **Исходы:** продолжить отдельный route или оставить как research evidence и использовать готовый native KD. **Stop:** legacy dependencies/портирование или head change поглощают выделенный integration budget. **Предел:** воспроизведение COCO recipe не доказывает PPE domain benefit; будущий экспорт всё равно отдельный gate.

## 6. Открытые вопросы и передачи

| Q-ID | Неизвестное и почему меняет решение | Как закрыть / адресат |
|---|---|---|
| W1-10-Q01 | Какая **фактически установленная** Ultralytics версия и выбранная family? Наличие KD в U не подтверждает старую среду команды | Version/commit + capability smoke test; → model_stack |
| W1-10-Q02 | Есть ли target teacher, превосходящий student по нужным class/scale/occlusion errors? Без этого KD может копировать bias | Независимый development audit; → datasets/evaluation/W1-09 |
| W1-10-Q03 | Полная ontology: object «каска», состояние ношения на человеке, event? Как сопоставлять phrases, class IDs, unknown и отсутствие наблюдения? | Полный кейс + annotation guideline; → datasets/violation_methods |
| W1-10-Q04 | Какой student graph и export ops разрешены фактическим LinQ SDK? YOLO26 end2end и LD head нельзя считать поддержанными | Получить SDK/compiler target specification и исполнить E03; → linq_platform/model_stack |
| W1-10-Q05 | Native KD table не задаёт полного training protocol/variance. Каковы seeds, schedule, teacher checkpoint provenance и selection? | Найти training artifact/config автора либо воспроизводить как новую собственную проверку; не заполнять пробел предположением |
| W1-10-Q06 | FGD paper gamma vs pinned recipe gamma: какой artifact дал опубликованную строку? | Авторский resolved config/checkpoint; до ответа считать два разных recipe |
| W1-10-Q07 | Реальная цена teacher pool inference и исправления; помещается ли teacher+student в доступную VRAM? | E01/E02 profiling на фактической конфигурации; → W1-14 |

**→ model_stack:** F01/F03/F06: штатный KD есть, но pin version, compile restriction, resume path и final unwrap обязательны. Не передавать training wrapper как финальный student. F12: LD bins/levels отличаются от YOLO26.

**→ datasets/W1-08/W1-09:** F15: substring class mapping — реальная точка отказа; нужен explicit ontology table, audit unknowns, полнота GT и provenance. VLM predictions не GT; исключённые boxes/необнаруженные объекты нельзя автоматически считать background.

**→ evaluation:** F02/F07/F10/F13 — разные published protocols. Сравнивать наши routes попарно при одинаковых data/updates/preprocessing и отдельно учитывать label/compute budget; event-level claim требует собственного evaluation. Учитель/пороги выбираются вне lockbox.

**→ linq_platform/video_architecture:** offline teacher не должен попасть в realtime graph; E03 требует реального exported student и target run. Поддержка same-family KD не устанавливает поддержку family на LinQ. Нужны ограничения static shape, output decoding и postprocessing.

**→ violation_methods/operator_product/hackathon_strategy:** отдельный object detection benchmark не доказывает «нарушение»: association, временная логика, видимость и определение события остаются самостоятельными условиями. В демонстрации корректно заявлять «предразметка с проверкой»/«student после KD» только по реально выполненному пути.


