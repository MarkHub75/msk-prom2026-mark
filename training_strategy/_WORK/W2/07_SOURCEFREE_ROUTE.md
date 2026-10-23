# W2-07 — Один source-free route: simple-SFOD, AdaBN + Fixed SF-FM

K007 / P2. Исследование 23.10.2026, начало чтения сети около 07:50 Europe/Moscow (UTC+3); дата доступа всех новых источников — 23.10.2026. Контекст mosprom-research-v1. Роль: исследователь W2, gpt-6.1-sol/medium, fresh context по заданию оркестратора. Прочитаны оба входных промпта, PLAN, общий вывод/внешние неизвестные/K007 CRITIC, W1-07 целиком, W1-02 E02, W1-09 F13/E03. Выполнены primary search, web open, read-only HTTP GitHub metadata/raw code. Training, inference, установка окружения, скачивание weights, export и LinQ не выполнялись. Меняется только этот файл.

## Ответ, меняющий очередь

Авторский public route найден: **EPFL-IMOS/simple-SFOD, AdaBN → фиксированный COCO pseudo-label artifact → Faster R-CNN с сильной аугментацией**. Это более ясная реализационная зацепка, чем неустановленный repo SFOD2021. Однако это **не готовая воспроизводимая команда**: weights локальные, JSON pseudo-labels заменяется вручную, eval entrypoint выполняет AdaBN, зависимости неполно зафиксированы. K007 получает статус **уточнена область применимости; public implementation найден, runnable artifact/selection contract частично открыт**. Польза для наших камер неизвестна.

До очереди качества нужны допустимость adaptation по кейсу, совпадающая ontology и рабочий source checkpoint, независимые target labels для выбора, исключение скрытого GT/source exposure из loader/hooks, проверенная BN/eval граница и обычный inference/export route. При отсутствии этих условий сохранить frozen baseline и направить небольшой бюджет на полную ручную разметку диагностических кадров. Online adaptation не назначается.

## Источники и происхождение

Все кодовые URL ниже закреплены на `ee24594869bde0069947540275a28eebb3d4a540` (далее P), commit 2024-11-27T14:04:14Z. Они реально получены через raw HTTP; это чтение, не исполнение. Для компактности GitHub blob links фиксируют тот же P.

| ID | Автор, документ, версия/дата; прямой URL | Получено и локатор |
|---|---|---|
| W2-07-S01 | Xianfeng Li et al., AAAI2021 *A Free Lunch…*; publisher 2021-05-18; arXiv v1 2020-12-10. [Publisher](https://ojs.aaai.org/index.php/AAAI/article/view/17029), [PDF](https://cdn.aaai.org/ojs/17029/17029-13-20523-1-2-20210518.pdf), [arXiv](https://arxiv.org/abs/2012.05400v1) | Страницы/PDF открыты; author/artifact trace. В извлечённом publisher/PDF не найдено `github`/`code`; поиск exact title/author handle не дал author repo. Не доказательство отсутствия кода. |
| W2-07-S02 | Yan Hao, Florent Forest, Olga Fink, ECCV2024 *Simplifying Source-Free Domain Adaptation for Object Detection…*. [Proceedings PDF](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/07083.pdf) | §§3.4, 4.2, 4.6; Fig.3–4. PDF напрямую связывает авторов с repo. |
| W2-07-S03 | EPFL-IMOS, [repo README at P](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/README.md) | Requirements, Adaptation; [commit metadata](https://api.github.com/repos/EPFL-IMOS/simple-SFOD/commits/ee24594869bde0069947540275a28eebb3d4a540), [tree](https://api.github.com/repos/EPFL-IMOS/simple-SFOD/git/trees/ee24594869bde0069947540275a28eebb3d4a540?recursive=1), [releases](https://api.github.com/repos/EPFL-IMOS/simple-SFOD/releases). Дерево и metadata прочитаны. |
| W2-07-S04 | EPFL-IMOS, [train_net.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/train_net.py), [base.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/engine/trainers/base.py) | `main`, `BaseTrainer.__init__`, `test_refinement`, `adabn_refinement`, `reset_bn_stats`; eval и AdaBN state. |
| W2-07-S05 | EPFL-IMOS, [fixed config](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/configs/faster_rcnn_VGG_cityscapes_foggy_source_wq.yaml), [source config](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/configs/faster_rcnn_VGG_cityscapes_source_new.yaml), [config.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/config.py) | Полные YAML; `add_config`, default `VGG.BN=True`, `TEST.VAL_LOSS=True`. |
| W2-07-S06 | EPFL-IMOS, [prediction_to_gt.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/cityscapes-to-coco-conversion/prediction_to_gt.py), [datasets.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/data/datasets.py) | Полные файлы; JSON replacement/registration и target GT ambiguity. |
| W2-07-S07 | EPFL-IMOS, [base_wq.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/engine/trainers/base_wq.py), [strong_aug.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/data/mappers/strong_aug.py), [detection_utils.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/data/detection_utils.py) | `BaseWQTrainer`, `run_step`, `build_hooks`, local loader; `BaseWQDetection.__getitem__`; `build_strong_augmentation`. |
| W2-07-S08 | EPFL-IMOS, [vgg.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/modeling/meta_arch/vgg.py), [convert_vgg_bn.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/convert_pretrained_model/convert_vgg_bn.py), [val_loss.py](https://github.com/EPFL-IMOS/simple-SFOD/blob/ee24594869bde0069947540275a28eebb3d4a540/daod/engine/hooks/val_loss.py) | Backbone BN construction; local pretraining conversion; validation hook forwarding mode. |

Search navigation включала exact SFOD2021 title, `lockonlxf`, `2012.05400`, source-free official code. Выбран S02 по прямой paper→author repo связи и более простому fixed-label варианту; другие новые SFOD методы не исследовались. API `/license` вернул 404; право использования конкретного code package здесь не установлено, чужую лицензию AT из W1 автоматически не переносить.

## Новые факты и пределы

Легенда: **paper** — описание авторов; **code** — статическое чтение P; **local** — полученная metadata; **inference** — наш вывод; **proposed** — будущая процедура.

### W2-07-F01 — Маршрут существует, weights не образуют готовый package

**code/local**, S03/S05/S08. README требует PyTorch≥1.12, Detectron20.6. Fixed recipe выбирает `TRAINER: base_wq`, `GeneralizedRCNN`, VGG backbone, обычные `RPN`/`StandardROIHeads`, 8 classes, `MASK_ON: False`. Source recipe начинает с локального `vgg16_bn.pkl`; fixed recipe — `/cluster/scratch/username/weights/adabn_weight2/adabn.pth`. Conversion helper читает локальный torchvision `vgg16_bn.pth` и переименовывает keys; это не source-trained detector checkpoint. В tree P нет опубликованного `.pth`/`.pkl`, API releases возвращает пустой список; README не предоставляет source detector download. Не проверялись внешние неуказанные хранилища.

**inference:** команда должна получить/создать законный source-trained detector с точной схемой keys/BN buffers/classes. До adaptation source images не требуются, но source training knowledge и pretraining остаются. Recipe не добавляет семантику новых PPE классов: одинаковые численные 8 classes не доказывают одинаковый порядок и смысл. YOLO checkpoint не загружается в этот Faster R-CNN по сходству задачи. Связь с W1-07-F07/Q04 становится конкретнее, вопрос target compatibility остаётся.

### W2-07-F02 — AdaBN entrypoint меняет модель даже под именем eval-only

**code**, S04/S08. `main(args.eval_only)` строит model, загружает weights, затем вызывает **`base.test_refinement`**, а не закомментированный `Trainer.test`. Там `model.train()`, `torch.no_grad()`, batches из `BaseTrainer(cfg)` train loader, остановка при `i > 1400`, затем test и `DetectionCheckpointer(model).save("adabn")`. На непустом бесконечном train loader это до 1401 forward; это не буквальная одна epoch. Optimizer step отсутствует. BN слои создаются через `nn.BatchNorm2d`; no-grad не фиксирует running buffers. Affine/conv weights не оптимизируются этим loop, но BN state меняется.

Функция `adabn_refinement` отдельно сбрасывает BN statistics и дважды вызывает recursive traversal; **активный entrypoint её не вызывает**. Поэтому нельзя описать активный код как reset→exact full-dataset moments. Batch order, repeated images, momentum, batch size и исходные buffers входят в интервенцию. `TRAIN`, а не сам факт наличия `TRAIN_TARGET`, задаёт этот loader. Если взять source config для target AdaBN без проверки, loader будет source.

**inference:** frozen baseline нельзя получать слепым запуском этого `--eval-only`; нужен проверенный обычный eval path, равенство state до/после и запрет BN updates на holdout. Это новая конкретизация W1-02-E02 и W1-07-E02.

### W2-07-F03 — Fixed pseudo-label artifact имеет ручной и неоднозначный стык

**code**, S06. Converter читает predictions `coco_instances_results.json`, отбрасывает scores `<0.7`, переносит `image_id`, `bbox`, `category_id`, присваивает annotation ID. Он читает существующий dataset JSON, **заменяет целиком `annotations`**, сохраняя images/categories, пишет другой жёстко заданный путь. `area`, `iscrowd`, confidence в новые annotations не добавляются. Возможный loader compatibility вопрос нужно проверить, не объявлять автоматически ошибкой.

`datasets.py` для Foggy train использует обычное `instancesonly_filtered_gtFine_train_foggy_beta_0.02.json`; строка специального `_adabn_pred.json` закомментирована. Следовательно, сам config не доказывает обучение по pseudo-labels: необходимо подтвердить, что этот JSON действительно заменён, и сохранить original отдельно. Иначе можно случайно использовать target GT, сохранив название source-free. Категории и image IDs должны соответствовать predictions; ручная подмена чужого JSON без проверки недопустима. Converter cutoff0.7 — факт этого helper, не универсальная confidence calibration.

### W2-07-F04 — Fixed training использует обычный detector и все возвращаемые loss terms

**code**, S05/S07/S08. `BaseWQTrainer` строит один model/optimizer/loader; teacher network/EMA в выбранном route нет. `run_step` суммирует все keys с `loss` и без suffix `val`, делает backward/optimizer step. Здесь нет selective zeroing pseudo regression и нет source replay. RPN/RoI являются штатными detection modules согласно YAML. Отсутствующий pseudo box не получает специального ignore только потому, что данные unlabeled; spatial missing-label проблему этот path не решает.

`BaseWQDetection` оборачивает mapped dataset, применяет strong photometric/erasing augmentation к image, сохраняет instances. `mosaic=True` в wrapper — не доказательство четырёхкадрового Mosaic: в прочитанном `__getitem__` его композиции нет. Есть `yolox` imports и debug `cv2.imwrite` в локальный авторский путь; README requirements неполны для этой цепочки. VGG создаёт BN, а trainer не задаёт специальной fixed-statistics policy: после отдельного AdaBN BN следует train/eval режимам модели и hooks. Полную маску `requires_grad` выбранного установленного Detectron2 надо снять при будущем smoke, а не называть все backbone layers обучаемыми без учёта freeze defaults.

### W2-07-F05 — Checkpoint/selection interface не равно zero-label выбору лучшего качества

**code**, S05/S07/S08. Fixed config: LR0.0025, batch4, `MAX_ITER:100000`, warmup1000, checkpoint period1000, eval period100, seed42; test datasets source val и foggy val. `build_hooks` добавляет PeriodicCheckpointer и EvalHook, но не BestCheckpointer по quality; `last`/финальный checkpoint не означает лучший. `TEST.VAL_LOSS=True` по add_config включает ValLossHook на `TEST[0]`, здесь **source validation**. Hook делает forward под no-grad, не переключая модель в eval. Это label exposure для validation loss; при train-mode BN также возможен state exposure. Отсутствие gradient не превращает такую ветку в строгий source-data-free protocol. Этот hook необходимо отключить/проверить до строгого испытания, а source retention оценивать отдельно без изменения adapted state.

**paper**, S02 §§3.4/4.2/4.6, ограничивающий protocol: авторы предлагают fixed pseudo-labels после AdaBN; backbone Faster R-CNN/VGG16-BN и ImageNet pretraining. Для SF-UT сообщают шаг4000, выбранный по наблюдаемому оптимальному early stopping трёх задач; при этом прямо отмечают недопустимость test-set early stopping в чисто unsupervised режиме. Fig.4 показывает collapse self-training вариантов, а AdaBN+Fixed SF-FM устойчивее в данном опыте. Это не новый label-free checkpoint selector. Порог confidence не валидирует локализацию и пропуски. Published settings: target LR0.0025, batch4, threshold0.8, V10032GiB; metric AP/mAP при IoU0.5, дорожные benchmarks. Числа качества здесь не перенесены на CCTV. Точная last/best процедура для fixed-variant табличной строки не установлена.

**inference:** step4000 не переносить в наш schedule как обоснованный optimum. Code100000 не выдавать за точное повторение выбранного paper checkpoint. SED W1-07-F07 ищет pseudo-label threshold, а не заменяет независимую model selection. Снижение entropy, loss или увеличение confident box counts не закрывает качество; даже detector confidence безошибочно не измеряет отсутствие unseen positives.

### W2-07-F06 — Final graph и source retention

**code/inference**, S05/S07/S08. Для fixed route checkpoint содержит один стандартный `GeneralizedRCNN`: VGG16-BN→RPN→RoI head→boxes/classes/scores, с адаптированными weights/BN buffers. Нет teacher ensemble, source loader или pseudo-label generation в inference. Backbone custom registration нужен для загрузки; это не доказательство совместимости обычного YOLO exporter или LinQ. В deploy важны и model parameters, и BN buffers, config, category mapping, preprocessing/NMS. Не выполнять AdaBN при final holdout inference.

Без независимых old-domain данных нельзя измерить сохранение source качества. Source-free алгоритм не доказывает отсутствие forgetting; frozen fallback сохранять отдельно. Малый source retention evaluator не превращается в разрешение source-data access при adaptation: роли и state effects разнести явно.

## Контракт кандидата: найдено / отсутствует

| Звено | Статус после W2 | Следствие |
|---|---|---|
| Paper→author repo | Установлено S02→S03, pin P | Public route перестал быть только названием |
| Source-trained checkpoint | Локальные пути; публичный artifact в tree/releases/README не найден | Нужен compatible artifact; ImageNet backbone недостаточен |
| AdaBN stage | Код прочитан, current eval entrypoint делает refinement | Исправить role boundary, dataset order/budget/buffer audit до quality queue |
| Fixed pseudo-label generation | Converter есть; полный готовый invocation/artifact chain отсутствует | Explicit prediction export→conversion→registration и hidden-GT check |
| Target updates | Один detector, ordinary loss, strong aug, no replay/EMA | Возможны missing-positive negatives; аудит обязателен |
| Selection | Paper SF-UT4000 observation, periodic eval/save code; no validated unsupervised selector | V с labels либо только feasibility claim; fixed-row last/best остаётся gap |
| Deploy | Один Faster R-CNN с BN; export/target не выполнены | Отдельный graph/export/LinQ gate |
| Target benefit | Не измерено | Никакого gain claim |

## W2-07-E01 — Дополнение W1-07-E02: допуск fixed-label source-free маршрута

**PROPOSED, не выполнено.** Не новая обязательная сетка. Решение: заслуживает ли этот legacy Faster R-CNN route quality trial по сравнению с frozen detector и небольшой supervised веткой. Если рабочая модель YOLO и нет соответствующего author port, не тратить время на перенос только ради SFOD.

**Входы/gates до очереди:** разрешённый кейсом adaptation pool U; exact checkpoint hash, config/P/dependencies, class order/semantics; usable source detector в этой architecture; проверенная infer/export feasibility; независимые группы A (полностью размеченный audit внутри adaptation domain), V (размеченные отдельные sessions для selection), H (закрытые new-session/new-camera groups); old-domain holdout R только если требуется retention и доступ разрешён. A/V/H роли не смешивать. U включает только разрешённые train images. При отсутствии V разрешён correctness/audit pilot, но не quality selection по proxy.

**Порядок будущего smoke, процедурный псевдокод:**

1. Получить frozen predictions с обычным eval, проверить неизменность всех parameters и BN buffers. Не использовать активный `train_net.py --eval-only` как frozen оценку. Сохранить исходную модель отдельно.
2. На копии модели выполнить явно ограниченный AdaBN по U; проверить отсутствие optimizer updates, state diff только ожидаемых BN buffers, порядок/число exposures. Не вызывать source train loader или ValLossHook на R/V/H. Сопоставить режим сброса statistics с задуманной процедурой; не выдавать1401 shuffled batches за полный pass.
3. Export predictions по U, явно фиксируя class map, NMS/cutoff; конвертировать в отдельный pseudo JSON. Проверить IDs/categories, bbox format, required COCO metadata, images с нулём retained boxes. Хэш/провенанс подтверждают, что train loader не читает target GT. На A полностью проверить не только accepted boxes, но все пропущенные objects/negatives; A не становится H.
4. Проверить loader/strong aug, BGR/RGB/dtype, small-box survival, empty-pseudo handling и actual freeze/BN mask; импорт YOLOX/debug-write issues — engineering gate. Снять отдельные RPN/RoI cls/reg losses и expected gradients; обычный pseudo JSON может наказывать пропущенные positives. Если аудит неприемлем, перейти к полной ручной коррекции, а не только повышать cutoff.
5. Только после gate разрешить один ограниченный quality comparison: B0 frozen; B1 small fully corrected supervised subset из train-role групп; B2 chosen fixed-pseudo source-free candidate. B1 — явная альтернатива с другой ценой labels, не «unsupervised победитель». Сохранить одинаковый initializer/model/input/inference settings; считать human minutes, unique groups, labels, exposures, training/integration/validation/export time. AdaBN-only как диагностический arm добавлять лишь если BN причина действительно остаётся открытой (reuse W1-02-E02), не обязательный trial.
6. Selection checkpoint/threshold/budget только по V и заранее согласованной constrained metric; если V labels используются, так и назвать target-supervised selection. Окончательно выбранный model+BN state заморозить, затем один H evaluation против B0. Одинаковые detector postprocessing/event rules; при event labels — event recall/FP per hour, иначе только detection metrics с явным IoU. Проверить per-class/per-size/per-camera recall/FP и R при наличии. Reload predictions parity, затем actual export/target quality gate.

**Артефакты:** source/BN/pseudo/final hashes; repo/dependency lock и исправления entrypoint; resolved configs; split/exposure manifests; pseudo raw scores+JSON+accepted/rejected counts; A GT и ошибки; buffer/weight/gradient deltas; checkpoint iteration/selection reason; V/H predictions; actual time/human minutes; final detector and exporter contract.

**Stop/rollback:** incompatible ontology/weights, hidden GT или source exposure, изменение H/BN при eval, неправильные IDs/geometry, необработанные empty batches, критичный pseudo recall failure — остановить до качества. Если quality gate на V не проходит или путь не успевает дать reviewable artifact в отведённый integration budget — B0/B1, без поиска удачного proxy/checkpoint на H. Положительный H исход поддержит только этот protocol/модель/группы; не доказывает arbitrary new-camera gain, отсутствие source forgetting без R, безопасность редких событий либо LinQ execution без actual test.

## Оставшиеся вопросы

| ID | Тип; точный gap | Что меняет и как закрыть |
|---|---|---|
| W2-07-Q01 | Artifact: source detector weights и exact preprocessing/class-map | Compatible checkpoint от model_stack/авторов либо отдельный source training вне текущей волны; до этого no runnable package claim |
| W2-07-Q02 | Public/protocol: fixed-row checkpoint selection, exact AdaBN sampling/reset/momentum и cutoff0.7 helper vs intended recipe | Full resolved run/config от авторов или собственный заранее заданный V-based protocol; не объединять несовпадающие code/paper настройки |
| W2-07-Q03 | Implementation: JSON replacement, hidden GT/source hooks, import dependencies, empty-pseudo images, ordinary eval и BN state | Только reviewed smoke E01; статическое чтение уже локализовало пути, дополнительный общий обзор SFOD не требуется |
| W2-07-Q04 | Case/data: разрешение target exposure, taxonomy/visual signal, U/A/V/H/R | Полный кейс, inventory и audit; выбирает допустимость adaptation и силу выводов |
| W2-07-Q05 | Experiment: target benefit и retention | Paired E01 с independent labels; unlabeled loss не закрывает вопрос |
| W2-07-Q06 | SDK: исполнение VGG/Faster R-CNN graph | linq_platform/model_stack actual export/compile/run; backend paper не доказательство LinQ |

## Передача K007

**Для сборщика:** сохранить отдельные уровни: public algorithm и pinned training code найдены; ready artifact частично отсутствует; current eval/GT/hooks требуют проверки; польза неизвестна. Закрывать K007 формулировкой «найдена условная public implementation, уточнён selection предел», а не «source-free полезен/готов». Gap SFOD2021 author repo остаётся локализованным; развивать второй каталог методов не нужно.

**→ model_stack:** S04–S08/F01–F06: local checkpoints, `--eval-only`→AdaBN, JSON registration, source validation hook, custom backbone и дополнительные imports — concrete integration work. **→ evaluation/datasets:** V labels и independent H нужны отдельно от U/A; source validation loss нельзя скрывать под строгим source-free названием. **→ linq_platform/video_architecture:** final candidate — один frozen detector с BN buffers; online training loop и teacher не нужны, target support открыт. **→ очередь W2-12:** P2, не ставить до compatible runnable checkpoint, role/BN correctness gate и independent selection labels; frozen+малый supervised audit/annotation путь сохраняется первой альтернативой.
