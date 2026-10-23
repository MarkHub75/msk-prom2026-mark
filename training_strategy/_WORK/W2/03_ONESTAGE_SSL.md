# W2-03 — One-stage SSOD: UTv2 FCOS и один YOLOv5 route

**K003; P1; training_strategy.** Проверка 23.10.2026, начало 07:31 Europe/Moscow (04:31 UTC), фиксация 07:41 Europe/Moscow (04:41 UTC). Это время доступа, не публикаций. Назначенная роль gpt-6.1-sol/medium, fresh context; делегирования нет. Полностью прочитаны Context-prompt.md, prompt-training-strategy.md, PLAN; общий вывод/K003/таблица внешних неизвестных CRITIC; W1-09 полностью, W1-03 F10–F12/E03. Выполнены новый search+open первичных страниц, получение commits/tree metadata и raw-кода по SHA. Код только прочитан: зависимости/weights/datasets не устанавливались и не скачивались, training/inference/export не выполнялись. Служебная HTTP/текстовая обработка выполнялась в памяти.

## Ответ для решения команды

One-stage online SSOD имеет конкретные авторские реализации. UTv2 — **FCOS с изменённой regression head**, отдельными pseudo targets для classification/regression и uncertainty comparison; это не обычный FCOS trainer плюс EMA-флаг. Стандартный eval выбирает teacher. Uncertainty-ветвь **остаётся в фактическом Python eval forward**: при стандартном test scoring её значение не определяет ranking boxes, но возвращается дополнительным полем `Instances`. Автоматическое получение обычного FCOS export не доказано.

Для потенциального anchor-based YOLOv5 ближе **AlibabaResearch/EfficientTeacher**, чем порт Listen2Student из FCOS. На проверенном SHA доступны custom config, pseudo assigner/loss, paired loader, EMA checkpoint и exporter с явным удалением domain heads. Это условная ветка для YOLOv5 family, **не установленная поддержка современного Ultralytics YOLO8/11/26**. README перечисляет несколько families; проверенный online teacher forward для иного `model_type` явно заканчивается `NotImplementedError`.

Сначала W1-09-E01 и runnable supervised baseline; полностью исправленные labels идут обычным supervised route W1-09-E02. Online имеет смысл ставить в очередь при достаточном U_train, прошедшем audit teacher, compatible exact trainer и заранее понятном inference artifact. Ни время, ни VRAM, ни target gain этим чтением не измерены.

## Первичные источники

Дата доступа всех источников — **2026-10-23**. `UT` ниже: SHA `93bb1256e8eb69103214b1d47db7f8297cb6b2c7`, commit **2022-07-27 03:33:41 UTC**. `ET`: SHA `64165e24a30cd6dc1dd893cc861c1feab0a536ee`, commit **2023-03-28 12:13:12 UTC**. SHA/date повторно получены commits API. Code-read означает raw по SHA и чтение указанных функций, а не исполнение; весь репозиторий и зависимости не проверялись.

| ID | Автор / первичный источник / версия | Что получено, локатор |
|---|---|---|
| W2-03-S01 | Liu, Ma, Kira, *Unbiased Teacher v2*, CVPR2022; [arXiv v1](https://arxiv.org/abs/2206.09500v1), 2022-06-19; [author project](https://ycliu93.github.io/projects/unbiasedteacher2.html) | Новые open metadata/project. Paper §3 ранее прочитан W1-09-S12; повторное полное чтение PDF в W2 не заявляется. Ownership/Listen2Student. |
| W2-03-S02 | Meta/facebookresearch UT [README](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/README.md), [INSTALL](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/INSTALL.md), [10% config](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/configs/FCOS/coco-standard/fcos_R_50_ut2_sup10_run0.yaml), [Base-FCOS](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/configs/FCOS/Base-FCOS.yaml) | Полные перечисленные configs/docs и FCOS defaults `ubteacher/config.py`; F01/F02. |
| W2-03-S03 | UT [trainer.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/engine/trainer.py) | `UBTeacherTrainer.__init__`, `run_step_full_semisup`, `_update_teacher_model`, `build_hooks`, строки 38–608; RCNN route не исследован; F02/F04/F06. |
| W2-03-S04 | UT [dataset_mapper.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/data/dataset_mapper.py), [build.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/data/build.py), [detection_utils.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/data/detection_utils.py) | Mapper целиком, loader relevant functions, strong augmentation целиком; F03. |
| W2-03-S05 | UT [fcos.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/modeling/fcos/fcos.py), [fcos_outputs.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/modeling/fcos/fcos_outputs.py), [pseudo_generator.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/modeling/pseudo_generator.py), [kl_loss.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/layers/kl_loss.py) | FCOS/head целиком; outputs assignment, supervised/pseudo losses, decode/NMS; pseudo generator целиком; NLLoss; F04/F05/F07. |
| W2-03-S06 | UT [one_stage_detector.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/modeling/one_stage_detector.py), [train_net.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/train_net.py), [ts_ensemble.py](https://github.com/facebookresearch/unbiased-teacher-v2/blob/93bb1256e8eb69103214b1d47db7f8297cb6b2c7/ubteacher/modeling/meta_arch/ts_ensemble.py) | Целиком: pseudo inputs, normalization/postprocess, eval-only/modelTeacher, namespaces; F06/F07. |
| W2-03-S07 | Xu, Chen, Guan, Hu, *Efficient Teacher: Semi-Supervised Object Detection for YOLOv5*, [arXiv v3](https://arxiv.org/abs/2302.07577v3); v1 2023-02-15, v3 2023-03-14; linked Alibaba [README](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/README.md) | Новые search+open paper metadata/abstract и README; author link устанавливает ownership. PDF numerical results не извлекались; F08. |
| W2-03-S08 | ET [custom config](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/configs/ssod/custom/yolov5l_custom_ssod.yaml), [10% config](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/configs/ssod/coco-standard/yolov5l_coco_ssod_10_percent.yaml), [defaults](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/configs/defaults.py), [requirements](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/requirements.txt) | Два configs/requirements целиком, SSOD defaults; F08/F09/F11. |
| W2-03-S09 | ET [ssod_trainer.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/trainer/ssod_trainer.py), [datasets_ssod.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/utils/datasets_ssod.py), [self_supervised_utils.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/utils/self_supervised_utils.py) | Trainer build/load/train_instance/save/update; fake labels/paired views; FairPseudoLabel/online_label_transform. LabelMatch inspected как contrast, не выбран в route; F09/F10/F12. |
| W2-03-S10 | ET [ssod_loss.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/models/loss/ssod/ssod_loss.py), [yolo_anchor_assigner.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/models/assigner/yolo_anchor_assigner.py) | `ComputeStudentMatchLoss` non-OTA active path, select_targets/default_loss; assigner forward/build_targets/build_uc_targets_aug; F11. |
| W2-03-S11 | ET [yolo_ssod.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/models/detector/yolo_ssod.py), [yolov5_head.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/models/head/yolov5_head.py), [export.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/export.py), [model_convert.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/deploy/model_convert.py) | Model forward/domain heads, Detect forward/post_process, export loader/--da/head.export, ONNX function; F13/F14. |
| W2-03-S12 | ET [torch_utils.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/utils/torch_utils.py), [general.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/utils/general.py), [val.py](https://github.com/AlibabaResearch/efficientteacher/blob/64165e24a30cd6dc1dd893cc861c1feab0a536ee/val.py) | EMA classes, strip_optimizer, val_ssod forward; F12/F13. |

Сбои: широкий stdout был усечён, нужные trainer/loss/geometry диапазоны перечитаны отдельно. Python cp1251 stdout упал на Unicode comment; повтор UTF-8 успешен. Guessed `assigner/yolo_anchor_assigner.py` дал404; tree установила реальный `models/assigner/yolo_anchor_assigner.py`, он прочитан. Это сбои вывода/пути, не отсутствие реализации. Binary model zoo/checkpoints не получены.

## UTv2 actual FCOS contract

### W2-03-F01 — Available implementation и неоднородные зависимости

**DOC/CODE-READ; S02.** README: Linux/macOS, Python≥3.7, PyTorch≥1.10 с соответствующим torchvision, Detectron2≥0.6, ссылка v0.6. Локальный старый INSTALL: Python3.6/PyTorch1.4/`detectron2-semi` fork без pin. Не воспроизводить смешанное окружение. Кандидат — README/v0.6 boundary плюс новый lock перед smoke. Это не доказанная работа Windows/current torch. README model zoo ещё «Coming soon»: recipe доступен, готовый FCOS detector checkpoint не получен. Tree также содержит standalone `configs/FCOS/R_50_1x.yaml` со ссылкой на отсутствующий `Base-GFocal.yaml`; выбранный ниже route его не использует.

### W2-03-F02 — Head/config и расход входов

**CODE-READ; S02/S03/S05/S06.** Выбран `configs/FCOS/coco-standard/fcos_R_50_ut2_sup10_run0.yaml` → `Base-FCOS.yaml`: OneStageDetector→R50/FPN→FCOS; p3–p7, strides8/16/32/64/128; default80 foreground classes. Начальные веса `detectron2://ImageNetPretrained/MSRA/R-50.pkl` — backbone, не готовый target detector. Class map и `MODEL.FCOS.NUM_CLASSES` менять совместно, head/checkpoint transfer проверить отдельно.

L/U global batches8/8, 180000 iterations, burn-up30000, LR.01, AMPtrue, 10% fully labeled COCO images/остальные U, seed1, val каждые2000. `CENTER_SAMPLE=False`, resize short-side range400–1200. Это literals source recipe, не назначение бюджета для команды. Студент получает обе L views; teacher Uweak, student Ustrong: стоимость не равна одному mixed supervised forward. Время/VRAM по числу passes не установлены.

### W2-03-F03 — Общая геометрия позволяет копировать pseudo boxes

**CODE-READ; S04/S03.** `build_detection_semisup_train_loader_two_crops` делит L/U seeded manifest либо cross-dataset streams; отдельные samplers/loaders, aspect ratio grouping. RFS здесь NotImplementedError. Mapper сначала делает общий Detectron2 geometric transform изображения и annotations. Strong строится из **уже преобразованного weak**: ColorJitter/Grayscale/GaussianBlur/три RandomErasing, без новой отдельной geometry; H/W совпадают. Trainer удаляет U `instances`, присваивает одни pseudo Instances обоим views. Матрица teacher→student здесь не нужна именно благодаря общей geometry. Добавление student-only crop/mosaic нарушит contract.

COCO U annotations могли присутствовать при mapper/split, но `teacher_weak` их не использует, перед student они удаляются. Это не разрешение передавать target validation в U. Custom registration и filtering пустых кадров проверять в resolved config.

### W2-03-F04 — Разные pseudo sets и разные confidence definitions

**CODE-READ; S03/S05.** No-grad teacher даёт dense outputs. Classification NMS criterion `cls`: sigmoid class score, cutoff.5. Regression второй NMS по тем же outputs `cls_n_loc`: class score×mean четырёх `1-sigmoid(reg_pred_std)`, затем sqrt и cutoff.5. Два cutoff.5 относятся к разным scores. Centerness отдельно; обычный test `cls_n_ctr` использует sqrt(class×centerness). Не сводить три режима к одному «teacher confidence».

При `REG_DISCRETE=True`: regression4×(16+1) channels, softmax+Integral; `bbox_pred_std`4 channels, centerness1 channel. Uncertainty обучается supervised NLLoss: sigma=sigmoid(std), regression error/log variance и IoU weighting, вес.05. Это не jitter SoftTeacher. `instances_class` задаёт cls/ctr, `instances_reg` — loc supervision.

### W2-03-F05 — Boundary selection не решает все missing positives

**CODE-READ; S05.** Assignment: l/t/r/b grid locations, inside-box/size-of-interest по FPN; минимальная площадь при нескольких boxes; center sampling выключен. Regression selection **по каждой стороне**: teacher confidence>.8 и >student confidence+.1. По выбранным entries `smooth_l1_loss(beta=0)`; если select пуст, явный CUDA zero. Псевдорегрессия включена, в отличие от UTv1 W1-09-F09.

Trainer: supervised cls/ctr делится на3, pseudo cls/ctr×2/3; supervised loc делится на1.2, pseudo loc×.2/1.2. Это не один общий unsup coefficient для всех terms.

Pseudo classification target нулевой по всем locations/classes с единицами на assigned positives; sigmoid focal суммирует остальные negatives. Пропущенный teacher объект не получает автоматически ignore. При empty bbox set assignment all-background; pseudo cls path не фильтрует `keep_locations`, в отличие от supervised path. Assertion в trainer `len(unlabel_data)!=0` проверяет **dictionary, не число boxes**, вопреки тексту сообщения. Empty-positive fallbacks есть; finite/gradient correctness all-empty batch не выполнена. SSOD не считать общим SAOD/partial-label fix (W1-03-F10).

### W2-03-F06 — Teacher/student и extraction

**CODE-READ; S03/S06.** Teacher отдельный, сразу `.eval()`; комментарий train step о не-переключении режима не отменяет initialization. На burn-up keep_rate0, затем EMA.9999 каждый iteration по **state_dict**, включая buffers, до teacher forward данного шага. Backprop/optimizer student, teacher no-grad. Wrapper имеет namespaces `modelTeacher`/`modelStudent`, checkpointer сохраняет его с optimizer/scheduler.

Hooks оценивают обе ветви: student metric suffix `_student`, teacher без suffix. `train_net.py --eval-only` в ubteacher route явно оценивает **modelTeacher**. Нельзя выбрать по teacher AP, экспортировать student и присвоить ему AP. Выбор best по нашей critical metric в route не установлен: нужны iteration/config и обе оценки. Структура позволяет извлечь отдельную submodule/state_dict; ready exporter в tree не найден. Ни extraction, ни reload здесь не выполнены.

### W2-03-F07 — Uncertainty остаётся Python eval branch

**CODE-READ + INFERENCE; S05/S06.** `FCOSHead.forward` без условия training вызывает bbox_pred_std при KL_LOSStrue; FCOS eval передаёт std в predict_proposals, который сохраняет `boxlist.reg_pred_std`. OneStageDetector postprocess возвращает Instances. Утверждение «training-only branch автоматически удалена» неверно на этом SHA.

При `cls_n_ctr` std не входит в boxes/scores/NMS. Наш вывод: detection-only export wrapper мог бы удалить unused computation либо отдельный inference build с KL disabled мог бы загрузить совпадающие веса без std keys. **Ни один вариант не реализован/не измерен**. Strict load, auxiliary fields, normalization/resize, Integral/postprocess/NMS и равенство outputs проверить. Это изменённый FCOS inference build, не гарантия загрузки в произвольный standard FCOS/YOLO.

## Один YOLO-specific lead: EfficientTeacher

### W2-03-F08 — Почему выбран этот lead и где family claim заканчивается

**DOC/CODE-READ; S07–S09.** Авторская arXiv entry ссылается на AlibabaResearch repo; название прямо YOLOv5. README заявляет YOLOv5/YOLOX/v6/v7/v8 library, conversion из YOLOv5 v6.0+, custom YOLOv5 configs, ONNX/back-conversion scripts. Их binaries/conversion parity не проверены. В active `SSODTrainer.train_instance` teacher path реализован при `model_type in ['yolov5']`; остальные здесь `NotImplementedError`. Выбран конкретный **P5 anchor-based YOLOv5l**, depth/width1/1, три anchor sets, Head YoloV5. Наличие YoloV8Detect в builder не доказывает полный online SSOD support этой головы.

README описывает проверенный авторами Modelscope container Ubuntu20.04/CUDA11.3/Python3.7/torch1.11; requirements разрешает torch≥1.9/torchvision≥.8.1, это не lock. Это candidate environment, не runnable stack команды. Современный Ultralytics package не dependency interface данного trainer. Lead полезен потому, что позволяет проверить существующий YOLOv5 recipe вместо самостоятельного переноса FCOS uncertainty/assignment.

### W2-03-F09 — Config routes и полнота labels

**CODE-READ; S08/S09.** Custom config: train/val/test/target image lists, nc/names, input640; BGR→RGB CHW, `/255`; ComputeLoss для L, ComputeStudentMatchLoss для U. Custom YAML имеет20 epochs/burn10, COCO10% YAML300/burn0, README общая инструкция говорит про burn220. Эти literals нельзя соединять в один recipe. Здесь выбран custom route с явным warm-start/burn contract; sample hyperparameters не назначаются для СИЗ.

Custom `ssod_hyp.with_gt=False` создаёт fake labels U; COCO config True для GT diagnostics. `FairPseudoLabel.create_pseudo_label_online_with_gt` строит targets из teacher predictions/NMS, GT использует только в debug plots; trainer при target_with_gt также считает diagnostic matching. Для реального U False, независимый audit не передавать loss. L проходит обычный supervised loss, значит нужны полностью проверенные labels по task ontology. Partial L не становится безопасным автоматически. Скрытые U positives ниже threshold также могут стать objectness negatives.

### W2-03-F10 — Geometry требует metadata interface

**CODE-READ; S09.** LoadImagesAndFakeLabels возвращает `(strong, labels, path, shapes, original_weak, M_s)`; teacher использует weak, student strong. Weak может быть mosaic canvas; strong — recorded perspective/scale/translation, HSV/flips и conditional cutout/autoaugment. M_s хранит image index, 3×3 matrix, scale, flip flags. FairPseudoLabel делает NMS, xywh→xyxy, transform четырёх углов M, clipping/box_candidates filtering, normalization и отдельные flips. У online_label_transform perspective default0: matrix fidelity должна соответствовать chosen augmentation settings.

Некоторые cutout/autoaugment выполняются только если `len(labels)>0`; при fake-empty U это может быть no-op. Реальные transforms проверять с **with_gt=False**, а не только в COCO diagnostic режиме. Штатный loader не является доказанным semantics-preserving augmentation для wearing/association задач.

### W2-03-F11 — Soft objectness и граница missing-positive treatment

**CODE-READ; S08/S10.** Effective default `pseudo_label_type='FairPseudoLabel'`: custom/10% YAML его не меняют. Dynamic GMM thresholds из LabelMatch нельзя приписать этому route. NMS conf.1/IoU.65, low/high.1/.6. select_targets делит по final confidence: high reliable, intermediate uncertain. При pseudo_label_with_obj uncertain target использует teacher objectness, а не final class product. Optional uncertain regression допускается при objectness≥.99; optional uncertain cls при class confidence≥.99. Custom включает uncertain bbox и выключает uncertain cls.

YOLOAnchorAssigner использует anchor-size ratio cutoff anchor_t и соседние grid offsets; это не FCOS assignment и не современный task-aligned assigner. Reliable: IoU box loss, class BCE на matched anchors, objectness target=detached IoU. Все tobj сначала **нули**. На uncertain matched anchors `ignore_obj=True` поставил бы -1 и исключил BCE; config здесь **False**, значит soft teacher score и BCE. Остальные anchors/не найденные teacher объекты остаются negatives. Название ignore thresholds не означает spatial-ignore всей неопределённой области.

Whole batch без proposals даёт invalid_target_shapeTrue, trainer ставит unsup loss0. Кадр без proposals внутри непустого batch требует проверки objectness negatives. Корректность чисел/градиентов не выполнена; никакого гарантированного решения всех missing boxes здесь нет.

### W2-03-F12 — Два уровня EMA и разные роли checkpoints

**CODE-READ; S09/S12.** `self.model` — оптимизируемый student; `self.ema=ModelEMA(student)` создаёт pseudo labels. После optimizer step обновляется EMA, затем secondary `self.semi_ema` обновляется **от self.ema.ema**. Первая EMA имеет ramp decay, secondary — cosine от.999 к.9999 либо fixed. После burn-in trainer оценивает raw student, затем secondary semi_ema. Второй результат заменяет self.results, определяет fitness/best. Checkpoint model=raw student, ema=secondary после burn, плюс optimizer/epoch/updates; updates относится к первой EMA. Полное возобновление обоих EMA/adaptor состояний этим набором не доказано.

Финальный strip_optimizer заменяет model на ema, зануляет optimizer/ema/updates, epoch=-1. Export loader также предпочитает ema. Default final/export — secondary smoothed detector, **не raw student и не online pseudo teacher**. Нужны branch manifest и validation/export parity именно выбранной ветви. Raw student отдельно сохранить до stripping. Epoch-adaptor меняет число batches на длину U loader; equal epochs не equal L exposure/updates/compute.

### W2-03-F13 — Domain heads сохраняются даже при нулевом loss

**CODE-READ; S09/S11/S12.** yolo_ssod.Model всегда создаёт det_8/det_16/det_32; _forward_once вычисляет их и возвращает detector_out + domain features. При with_da_lossFalse trainer умножает domain losses на0, но модули/forward остаются. Поэтому actual inference object не буквально standard YOLOv5 без extraction.

Найден concrete extraction path: `export.py --da` заменяет forward на forward_export, удаляет три det_*; forward_export выполняет backbone→neck→head. Это прочитанный path, **не успешный export**. Без --da могут остаться дополнительные outputs/operators. Флаг нужен по actual class graph, даже если domain loss был выключен.

### W2-03-F14 — Export head возвращает raw levels до decode

**CODE-READ; S11.** Export loader предпочитает EMA, fuse/eval, ставит Detect exportTrue. В yolov5_head.py этот режим возвращает list raw per-level tensors `B×anchors×(H*W)×(nc+5)` при np0, **до sigmoid/grid/anchor decode**. Обычный eval возвращает decoded concat + raw levels, существуют post_process methods. Нельзя объявить output standard decoded xywh/objectness/classes только по имени YOLOv5.

deploy.model_convert.export_onnx задаёт один output name и generic dynamic axes, хотя head отдаёт несколько levels; это место future shape/name проверки, не доказанный баг выполнения. Run API default opset12, CLI default9: сохранять resolved invocation. Decode/NMS/class map и actual output schema требуют parity gate. ONNX не является LinQ proof. Back-conversion scripts из README не audited.

## Матрица переноса и цена interfaces

| Interface / ресурс | UTv2 FCOS code-observed | ET YOLOv5 code-observed | Переносимость / ограничение |
|---|---|---|---|
| Данные | fully labeled L + image-level U, D2 Instances/two crops | L labels + U list/fake labels, paired canvas/M_s | Группы/audit reusable; partial L не становится exhaustive |
| Class/head | sigmoid classes, centerness, discrete ltrb/std | anchor-based objectness/classes/xywh | Ontology переносима; channels/assignment/std не переносятся флагом |
| Missing positive | focal negatives вне pseudo positives | objectness0 вне matched reliable/uncertain anchors | Audit omissions обязателен; threshold не добавляет отсутствующий сигнал |
| Regression | relative per-boundary uncertainty, NLL head | IoU и confidence/objectness selection | FCOS findings не дают готовый modern YOLO loss |
| Geometry | common resize/flip; strong photometric/erase | weak/mosaic + M/flip mapping | Нужны overlays/known boxes; не смешивать mapper/loss repos |
| State/compute | student+teacher, L2 views/Uweak/Ustrong | student+EMA+secondary EMA, U epoch adaptor | Измерять extra forward, memory, loader queues, audit/debug |
| Final graph | std остаётся eval field; fixed test score не использует её | --da удаляет auxiliaries; raw outputs требуют decode | Нет измеренной готовности standard exported model |
| Families | FCOS R50 route | YOLOv5l P5 route | Не доказаны current Ultralytics/LinQ |
| Простая альтернатива | W1-09-E02 | W1-09-E02 | Полные labels + обычный supervised loss требуют меньше новых interfaces; время не измерено |

ET уточняет K003: если model_stack выбирает compatible YOLOv5 и получает baseline/conversion parity, нет необходимости сначала писать FCOS port. Если выбран иной head либо SDK не принимает exact graph, corrected supervised route остаётся предпочтительным по интеграционным prerequisites. Само наличие ET не оправдывает смену всего стека.

## W2-03-E01 — Дополнение correctness gate W1-09-E03

**Proposed, не выполнено.** Это детализация существующего gate, не отдельный mandatory benchmark. Вопрос: можно ли получить воспроизводимый single-detector inference artifact из exact online route до назначения большого SSOD trial?

**Входы:** один UT/ET SHA, resolved config/dependency lock, compatible supervised checkpoint/classes/preprocessing; небольшой полностью проверенный diagnostic набор с known boxes: empty, tiny, overlapping classes, edge box. U_train/V/H из независимых допустимых групп; audit/calibration отдельно. Diagnostic GT доступен контролёру, U loss его не получает. Inventory GPU/OS/VRAM и SDK/export prerequisites отдельно. Не проводить оба routes ради покрытия.

**Действия/контроль:**

1. Проверить identifiers/role exposure/class IDs, effective augmentation при U with_gtFalse, отсутствие L/V/H в U. Known boxes: UT общий transform identity между views; ET M/flips/mosaic borders/clipping/removal. Сохранить overlays и численные координаты. Sentinel/perturbed U GT не должен менять pseudo targets/loss, если GT лишь diagnostic.
2. На будущих minimal steps проверить teacher no-grad/eval, student grads/update, EMA formula/timing. UT отдельно cls/reg sets, boundary masks, empty positives; ET reliable/intermediate/no proposals, objectness mask/soft targets. Проверить no proposals на одном image mixed batch и whole batch, boxes исчезли после transform, rare pseudo class отсутствует, all-negative L. Требовать finite losses/gradients, логировать background вклад на hidden known positive. Отсутствие exception не доказывает missing-positive safety.
3. Save/reload **до stripping**: выбранные student/online teacher/secondary EMA, optimizer/iteration/scheduler/scaler/threshold/adaptor metadata по реально поддержанному интерфейсу. Сравнить predictions до/после reload. Не обещать bitwise continuation. UT wrapper→modelStudent/modelTeacher; ET raw/online EMA/secondary EMA с hashes. При отсутствующем state заранее указать custom saver requirement.
4. Final extraction: UT штатный std eval→proposed detection-only wrapper/std removal с cls_n_ctr; ET chosen raw/secondary→--da removal→raw levels→exact decode/NMS. Одинаковые images/preprocess/precision; boxes/classes/scores в заранее заданной numerical tolerance и совпадение post-NMS outcomes. Проверить names/shapes/operators/graph outputs, не только ONNX existence. Успех CPU/ORT не доказывает LinQ.
5. Только после correctness/deploy gate — W1-09-E03 paired supervised-vs-online. Equal init/data/validation policy плюс L/U exposures, updates, teacher passes/wall-clock: equal epochs недостаточно. W1-09-E02 annotation control — альтернатива по human budget, не обязательная третья arm. Teacher drift audit W1-09-E01; H не используется threshold/checkpoint/adaptor selection.

**Метрики/артефакты:** coordinate/gradient/state/branch parity traces, per-class accepted counts и missing-positive supervision, обе UT validation оценки либо явно названные три ET weight states; resolved config/env/hash, manifests/tensor examples/overlays, export hash/operators/output schema, decode/NMS revision. Раздельные T_setup/T_loader/T_step/T_audit/T_save-reload/T_extract/T_export-parity, peak VRAM и human debugging minutes. Числа измерять, не угадывать по RTX4070.

**Исходы/stop:** geometry/leakage/gradient/nonfinite/extraction mismatch — stop, исправление в bounded engineering budget либо fallback E02. Нет явной ветви/final target path — long online не запускать. Correctness pass разрешает только controlled trial, принятие по V critical constraints и независимому H protocol W1-09. Critical degradation/исчезновение редких pseudo classes — rollback. Спорный effect относительно group/seed variation — repeat только если решение ещё актуально. Успех не доказывает target gain, экономию annotation, events или LinQ.

## Остаточные неизвестные

| ID / тип / приоритет | Неизвестное и уже установленное | Закрытие / решение |
|---|---|---|
| W2-03-Q01 artifact/environment P1 | UT model zoo Coming soon; точный lock/pretrained detector не получен; ET weight links не binary check | Получить weights/provenance/lock и bounded E01; не считать уже runnable |
| W2-03-Q02 experiment P1 | UT std removal не входит в score, но parity/load/export не выполнены; ET --da/raw decoder code прочитан, ONNX schema не проверена | Extraction/export parity до long trial; определяет пригодность/цену single detector |
| W2-03-Q03 case/data P0 | Ontology/adaptation permission/teacher critical coverage/independent groups неизвестны | Кейс + datasets audit/W1-09-E01; разрешает online вообще |
| W2-03-Q04 experiment/selection P1 | Полезность raw/teacher/EMA на target неизвестна | Раздельные V metrics/branch manifest, controlled E03/H protocol; не переносить teacher AP на student |
| W2-03-Q05 SDK P0 | FCOS/ET exported graph, Integral/GN/shape/raw postprocess совместимость LinQ неизвестны | Versioned SDK и actual compile/run; может исключить route до training |
| W2-03-Q06 experiment/state P1 | Empty/mixed U gradients, real semantics-preserving transforms, full resume двух EMA/adaptor не проверены | E01 diagnostics/reload; unmet budget→corrected supervised |

## K003 outcome и передача

**Implementation gap закрыт чтением в указанной области; target correctness/benefit открыты.** Установлены concrete FCOS и более близкий YOLOv5 public route. W1-09-F12 дополнен retained std eval branch, scoring/assignment/loss и teacher selection. W1-09-Q02 сузился до выбранной exact family/head/environment, не закрыт для любого YOLO. E03 дополнен dictionary-vs-box assertion, negative supervision, двойной EMA и raw export head gates.

**→ model_stack:** S03/S05/S06/S09–S12: exact family, conversion, loader/loss, chosen branch/extraction/raw decode. Это узкий contract, не обзор всего model_stack.

**→ datasets/evaluation:** fully labeled L отдельно U, audit teacher misses/no-proposal/class coverage. ET epoch length зависит U, считать exposures. Unlabeled exposure не independent transfer test.

**→ linq_platform/video_architecture:** извлечённая branch/preprocessing/output schema; UT std и ET domain/raw outputs сами не исчезают. Нужны graph/postprocess parity и actual target execution.

**→ очередь/автор:** один compatible route достаточен, если U даёт новое разнообразие и baseline/audit/deploy gates пройдены. Source gain/название метода не делает online обязательным. Сравнивать полную цену loader/head/EMA/saver/extraction/audit с fully corrected supervised route и сохранять его для rollback.
