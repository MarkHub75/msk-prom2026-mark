# W1-05 — Аугментации промышленных камер

Исследование: 23.10.2026, 03:47–03:50 UTC (06:47–06:50 Europe/Moscow); дата доступа ко всем источникам ниже — 23.10.2026. Это дата чтения, а не дата публикации. Входы Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md и W1-05 из _WORK/AGENT_PROMPTS.md прочитаны как UTF-8. Статус: интернет-поиск, открытие первичных страниц, чтение исходников и GitHub metadata; обучение, импорт библиотек, запуск transforms и измерения качества НЕ выполнялись. Содержание E-ID — программа будущей проверки.

## Решение команды

Выбирать аугментации по наблюдаемому дефекту камеры и смыслу разметки. Для CCTV первыми кандидатами являются умеренные вариации экспозиции/контраста, компрессии и размытия, если именно такие дефекты есть в train/рабочем потоке. Геометрия, mosaic, mixup, occlusion и copy-paste требуют отдельного решения по классам. Сохранение bbox математически не гарантирует сохранения значения «каска надета», «респиратор снят», «человек в зоне» или «курение». Рецепт по умолчанию Ultralytics — доступный контроль, но не установленный оптимум для нашего кейса.

Наиболее практические ограничения реализации: `copy_paste` не действует на обычные bbox-only labels без segments; `erasing`/`auto_augment` относятся к classification; default JPEG-like compression в дополнительном Albumentations pipeline выключена; `close_mosaic` закрывает четыре mix-операции; `rect` меняет реально применяемые probabilities. Современный сайт Albumentations и архивная библиотека 2.0.8 имеют разные имена аргументов. Ни совместимость среды, ни качество на CCTV, ни исполнение на LinQ этим чтением не подтверждены.

## Источники

Все URL открыты web-инструментом либо получены HTTP-чтением первичного raw-кода; поиск использован как навигация. Для кода указан путь и функция, что надёжнее номера строки при переносе.

| ID | Источник / версия / дата | Прямой URL и локатор | Поддерживает |
|---|---|---|---|
| W1-05-S01 | Ultralytics, `8.4.184`, commit `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`; committer 2026-10-22T20:27:18Z, версия дополнительно сверена в `ultralytics/__init__.py` | [default.yaml](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/default.yaml), блоки Train settings и Hyperparameters; [metadata](https://api.github.com/repos/ultralytics/ultralytics/commits/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8); [version](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/__init__.py) | F01, F02 |
| W1-05-S02 | Ultralytics, тот же pinned commit | [data/augment.py](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/augment.py): `Mosaic` L435, `MixUp` L784, `CutMix` L886, `RandomPerspective` L1062 / `box_candidates` L1410, `RandomHSV`, `CopyPaste` L1937, `Albumentations` L2101, `v8_transforms` L2832 (номера 1-based при HTTP-чтении) | F03–F07 |
| W1-05-S03 | Ultralytics, тот же pinned commit | [data/dataset.py](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/dataset.py): `YOLODataset.build_transforms`, `close_mosaic` | F08 |
| W1-05-S04 | Ultralytics official guide, rolling web version; дата публикации/конкретный package version страницы не установлены | [Data Augmentation](https://docs.ultralytics.com/guides/yolo-data-augmentation), Advanced Augmentation Features / FAQ / disabling augmentations | F09; сверка с S01–S03 обязательна |
| W1-05-S05 | Albumentations team, tag `2.0.8`, commit `4d2cf04b6635663275a747333754410ef255e54c`, committer 2025-05-27T20:55:21Z | [bbox_utils.py](https://github.com/albumentations-team/albumentations/blob/4d2cf04b6635663275a747333754410ef255e54c/albumentations/core/bbox_utils.py): `BboxParams.__init__`, `BboxProcessor`, `filter_bboxes`, `clip_bboxes`; [release](https://github.com/albumentations-team/albumentations/releases/tag/2.0.8); [tag metadata](https://api.github.com/repos/albumentations-team/albumentations/git/ref/tags/2.0.8) | F10, F11 |
| W1-05-S06 | Albumentations official live docs, rolling revision/package version не установлены | [Bounding boxes](https://albumentations.ai/docs/3-basic-usage/bounding-boxes-augmentations/): BboxParams Reference, Handling Imperfect Annotations; [Supported Targets](https://albumentations.ai/docs/reference/supported-targets-by-transform/): Image-Only / Dual Transforms | F12 |
| W1-05-S07 | Albumentations 2.0.8, pinned commit S05 | [pixel/transforms.py](https://github.com/albumentations-team/albumentations/blob/4d2cf04b6635663275a747333754410ef255e54c/albumentations/augmentations/pixel/transforms.py): `ImageCompression`, `RandomBrightnessContrast`; [blur/transforms.py](https://github.com/albumentations-team/albumentations/blob/4d2cf04b6635663275a747333754410ef255e54c/albumentations/augmentations/blur/transforms.py): `MotionBlur` | F13 |
| W1-05-S08 | Albumentations 2.0.8, pinned commit S05 | [dropout/coarse_dropout.py](https://github.com/albumentations-team/albumentations/blob/4d2cf04b6635663275a747333754410ef255e54c/albumentations/augmentations/dropout/coarse_dropout.py): `CoarseDropout`; [dropout/transforms.py](https://github.com/albumentations-team/albumentations/blob/4d2cf04b6635663275a747333754410ef255e54c/albumentations/augmentations/dropout/transforms.py): `BaseDropout.apply_to_bboxes` | F14 |
| W1-05-S09 | Michaelis et al., *Benchmarking Robustness in Object Detection: Autonomous Driving when Winter is Coming*, arXiv v1 2019-07-17, прочитана v2 2020-03-31 | [paper v2 HTML](https://arxiv.org/html/1907.07484v2), §§2.1–2.2, 3.3, Table 2, Appendix A; [version history](https://arxiv.org/abs/1907.07484) | F15 |
| W1-05-S10 | Авторы S09, benchmark repository; default HEAD при проверке `aecde7ba8966a94708a5b031b0df91891cb05cdc`, committer 2019-07-20T09:22:53Z | [author repo](https://github.com/bethgelab/robust-detection-benchmark), README Evaluation details / Leaderboard; [pinned README](https://github.com/bethgelab/robust-detection-benchmark/blob/aecde7ba8966a94708a5b031b0df91891cb05cdc/README.md) | F16 |

Сбой доступа: Windows PowerShell `Invoke-WebRequest` без `-UseBasicParsing` дал `NullReferenceException` для raw.githubusercontent.com. Повтор с `-UseBasicParsing` успешно получил нужный код; это сбой способа чтения, не недоступность репозитория. Live docs доступны. Содержательного закрытого первичного источника в этой ветке не осталось.

## Факты реализации и границы

**W1-05-F01 — code/config observation, S01.** Буквальные значения pinned default.yaml:

```yaml
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.5
bgr: 0.0
mosaic: 1.0
mixup: 0.0
cutmix: 0.0
copy_paste: 0.0
copy_paste_mode: flip
close_mosaic: 10
rect: False
multi_scale: 0.0
auto_augment: randaugment
erasing: 0.4
```

**W1-05-F02 — interpretation of config, S01/S02.** Не все числа — probabilities: degrees/shear — углы, translate — доля сдвига, scale — диапазон масштаба относительно единицы; `copy_paste` связан с долей eligible objects. Последние два параметра блока (`auto_augment`, `erasing`) предназначены classification; нельзя выдавать `erasing=0.4` за включённую bbox-окклюзию. Эти defaults не измерение и не recommendation optimum. `multi_scale` — отдельный параметр изменения размеров обучения; его нельзя незаметно добавить в тест фотометрии.

**W1-05-F03 — code observation, S02/v8_transforms.** Порядок: pre-transform mosaic/affine и copy-paste, затем MixUp, CutMix, Albumentations, HSV, vertical/horizontal flips. Поэтому отдельные изменения не независимы от оставленного pre-transform; для чистой ablation необходимо зафиксировать остальную цепочку. Здесь не проверялся tensor graph экспортера: это pipeline training data, что само по себе не добавляет операцию аугментации к inference, но не доказывает поддержку модели на LinQ.

**W1-05-F04 — code observation, S02/Albumentations.** При наличии optional библиотеки default extra list: Blur/MedianBlur/ToGray/CLAHE по `p=0.01`; RandomBrightnessContrast, RandomGamma и ImageCompression по `p=0.0` (у последнего задан `quality_range=(75,100)`). Custom list заменяет именно этот список, сохраняя другие операции Ultralytics. Spatial transforms распознаются рекурсивно через DualTransform/BaseCompose; bbox поля: `format="yolo"`, `label_fields=["class_labels","idx"]`. ImportError пропускается; другие ошибки initialization логируются. Значит, config и успешное обучение ещё не подтверждают наличие нужной операции: сохранить версии, startup log и фактические samples. Наличие лишь минимальной version check 1.0.3 не доказывает совместимость любой более новой библиотеки.

**W1-05-F05 — code observation, S02/RandomPerspective.box_candidates.** После преобразования и clipping фильтр detection требует ширину и высоту строго больше 2 px, отношение площадей new/old строго больше 0.10, aspect ratio строго меньше 100. Для сегментов используется area threshold 0.01. Это геометрический фильтр, а не оценка видимости СИЗ/состояния. Маленькие сигареты/части лица могут систематически выпадать после scale/crop; нужен счётчик survival по классам и исходным размерам, а не только visual mosaic.

**W1-05-F06 — code observation, S02/CopyPaste.__call__.** При `len(instances.segments)==0` или p==0 операция возвращает исходные labels. У bbox-only detect изменение `copy_paste` поэтому не создаёт полноценный paste. Перенос по маске требует segments/соответствующей подготовки. Даже корректный mask не даёт автоматической семантики ношения. Самостоятельный bbox-rectangle paste — уже другой метод со своей проверкой, не свойство этого флага.

**W1-05-F07 — code observation, S02/MixUp/CutMix.** MixUp использует Beta(32,32) для смешивания. CutMix выбирает область без перекрытия destination boxes; source selection требует достаточную долю объекта внутри области (0.1 для boxes, 0.01 при segments). Эти эвристики не валидируют взаимодействие человека, СИЗ и опасной зоны. Отсутствие пересечения bounding boxes не означает физическую корректность сцены.

**W1-05-F08 — code observation, S03.** `rect=True` в YOLODataset.build_transforms обнуляет mosaic/mixup/cutmix; `close_mosaic` обнуляет mosaic/copy_paste/mixup/cutmix и перестраивает transforms. При сравнении поздних эпох это несколько операций, а не одно изменение mosaic. Сохранить фактически resolved configuration и epoch schedule.

**W1-05-F09 — documentation claim, S04.** Руководство предлагает учитывать постоянство точки обзора и допустимость частичных объектов при выборе геометрии/mosaic. Оно также описывает custom Albumentations через Python API. Это рекомендации разработчика библиотеки, без измерения пользы на нашем CCTV. Команда должна связать их с последующими E-ID.

**W1-05-F10 — code observation, S05.** Для Albumentations 2.0.8 правильные имена — `BboxParams(format=..., clip=...)`. Defaults `min_area=min_visibility=min_width=min_height=0.0`, `check_each_transform=True`, `clip=False`, `filter_invalid_bboxes=False`, `max_accept_ratio=None`. `label_fields` связывает labels с удаляемыми boxes. В `filter_bboxes` clipping выполняется перед проверками площади/размеров; площадь и размер считаются в пикселях по shape. Default аргументы самой helper-функции для min_width/min_height равны 1.0, а BboxParams передаёт свои 0.0: нельзя смешивать эти defaults.

**W1-05-F11 — inference from S05, not measurement.** `min_visibility` фильтрует по геометрии конкретной операции: обычное clipping сравнивает площадь clipped bbox с bbox до clipping, а не распознаёт, видна ли каска за человеком. Это доля bbox, не confidence правильности класса. `filter_invalid_bboxes` и clip не заменяют исправление аннотаций: тихое удаление дефектных labels меняет распределение редких классов. Логировать до/после и причину каждого удаления; число удалённых объектов отдельно от числа кадров без labels.

**W1-05-F12 — docs observation, S06.** Live reference использует `coord_format`, `clip_bboxes_on_input`, `clip_after_transform` и расширенные targets. Это не signature 2.0.8. Не копировать live snippet в pinned env без сверки; не объявлять текущую major version сайта установленной. Наличие transform в общей таблице означает поддержку типа target в этой библиотеке, но не интеграцию каждого target в конкретный trainer.

**W1-05-F13 — code observation, S07.** В pinned Alb 2.0.8 ImageCompression — ImageOnlyTransform с JPEG/WebP (`compression_type="jpeg"` по умолчанию), `quality_range=(99,100)`, `p=0.5`; RandomBrightnessContrast также image-only; MotionBlur существует и строит направленный blur. Имена можно использовать в custom Python transform list после smoke-check. JPEG/WebP не являются точной моделью временной деградации H.264/H.265: для CCTV сохранять реальные decoded frames и codec/bitrate metadata, если доступны. Последнее — инженерное ограничение применимости, не измерение эквивалентности кодеков.

**W1-05-F14 — code observation, S08.** CoarseDropout наследует BaseDropout; bbox handling через `filter_bboxes_by_holes` использует min_area/min_visibility bbox processor. Таким образом, blanket утверждение «dropout никогда не меняет targets» для 2.0.8 неверно. Но даже survival по площади не гарантирует сохранение visual evidence конкретного PPE-состояния. Удаление helmet box не превращает соответствующий person в `no_helmet` автоматически.

**W1-05-F15 — published measurement, S09 §§2.1–2.2/3.3 Table2, не наш тест.** Faster R-CNN R50-FPN, COCO train2017 → val2017, полная доступная instance-разметка, не few-shot budget. Для standard / combined standard+stylized training: clean AP 36.3 / 34.6, corruption-mean mPC 18.2 / 20.4, relative rPC 50.2% / 58.9%. Проверка по 15 типам corruptions, 5 severity; это AP, не AP50. Appendix A: short edge 800, 12 epochs, LR schedule 8/11, фактически четыре GPU по две картинки/GPU с linear LR scaling. Правило выбора лучшего checkpoint и точная модель GPU здесь не восстановлены. Пример показывает trade-off clean/robustness; не доказывает, что stylization нужна для PPE или что такая же прибавка будет у YOLO. Для быстрого CCTV-плана полезнее отдельный clean и degraded slice.

**W1-05-F16 — provenance caution, S10/S09.** README автора в Evaluation details называет COCO metric mAP50, тогда как Table2 paper и leaderboard COCO подписаны AP. Для чисел F15 использована версия paper v2; не смешивать metric labels README с таблицей статьи. Отдельный локальный benchmark этой веткой не выполнялся.

## Физика и label semantics: условия допуска преобразований

Следующие W1-05-F17–F22 — наши проектные выводы/гипотезы из постановки и F01–F16. Они не являются опубликованными результатами PPE-experiments.

| ID / группа | Когда есть смысл пробовать | Семантический gate и риск |
|---|---|---|
| W1-05-F17 photometric | Разница света/экспозиции, тени, режим день/ночь в реальных train-camera samples | Если цвет кодирует тип каски/жилета, aggressive hue и gray могут изменить label evidence. Оставлять texture/края лица различимыми; HSV не имитирует IR night mode физически. Сверять целые составные transforms, не только каждый отдельно. |
| W1-05-F18 blur/compression/noise | Размытый человек в движении, дефокус, низкий bitrate действительно встречаются | Boxes могут остаться точными, а сигарета/ремни/респиратор исчезнуть. Не требовать от модели распознавания невидимого состояния; отдельно annotation policy unknown/ignore. JPEG proxy проверять на реальном видеопотоке. |
| W1-05-F19 геометрия/scale/crop/flips | Неуверенность в положении человека, несколько ракурсов, небольшая вибрация камеры | Синхронно менять boxes, masks, keypoints и ROI-полигоны, если labels зависят от них. Для фиксированной камеры image-space zone нельзя оставить на старом месте после flip/affine. Вертикальный flip/сильная перспектива обычно не соответствует монтажу камеры; допускать только при реальном сценарии. Crop человека может убрать head/person association. |
| W1-05-F20 mosaic/mixup | Гипотеза о детекции объектов на разных масштабах/фонах; проверяется отдельно | Четыре сцены не имеют единого физического пола/зоны; прозрачные люди MixUp не являются реальной окклюзией. Не переносить person-PPE relations через границы patches; event label целого кадра нельзя просто конкатенировать. Падение small-object survival — причина снизить/выключить. |
| W1-05-F21 occlusion/CoarseDropout/CutMix | Реальные перекрытия корпусами, оборудованием; object detection с согласованной политикой visibility | Закрыть голову не равно снять каску. Для `no_helmet` нужен видимый непокрытый head согласно ontology. Удаление части маски/box не создаёт достоверное нарушение. Для person-state bbox нужна проверка evidence region головы/лица, не доли person bbox. |
| W1-05-F22 copy-paste | Есть masks, правильные физические масштабы/позиции и конкретная нехватка сцен | Переносить связку person+PPE+relations, либо контролируемо создавать состояние с повторной верификацией labels. Вклеенная каска рядом с головой не означает «надета». Footpoint/zone relation считать заново. Детали синтетического data generation — передача W1-11, не отдельное обещание здесь. |

Для smoking наличие маленького предмета не тождественно событию: руки/рот/временной контекст могут быть решающими. Покадровая аугментация не решает отсутствие события во времени. Для event/track-модели случайные пространственные параметры должны быть согласованы на клипе, если метод не предусматривает иной протокол; независимые скачки кадров создадут искусственное движение. Это вопрос к violation_methods/video_architecture.

## Практическая программа: всё ниже предложено, не выполнено

### W1-05-E01 — semantic/data-pipeline gate до обучения

Вопрос: действительно ли candidate transform действует и сохраняет пригодную разметку? Входы: pinned model/trainer/package lock, train-only изображения с boxes и необходимыми relations/ROI, annotation policy. Включить редкие и маленькие объекты, кадры с частичной видимостью и пустые кадры. Validation/test в training pipeline не подмешивать.

Действия (псевдопроцедура, без выдуманного trainer API): зафиксировать seed и список train IDs; получить before/after из настоящего dataloader для каждой группы отдельно и для полной композиции; сохранить transform parameters/replay, overlays, bbox/class/association arrays. Сопоставить ID объектов до/после. Проверить диапазон/формат координат, label alignment, clipping, пустые targets и отсутствие ошибки при реальном использовании. Для spatial custom transforms сохранить startup log: успешный import недостаточен.

Метрики: survival и удаление labels по классу/исходной pixel area; доля кадров без targets; invalid coords; ручное число semantic failures, где исчезло evidence или сломалась связь. Артефакты: package versions, config, seed, sample manifest, overlays и список причин отказа. Stop rule: не начинать дорогой trial при воспроизводимой геометрической/семантической ошибке; уменьшить strength, исключить transform или определить ignore-policy. Нулевая найденная ошибка на выборке разрешает ablation, но не доказывает глобальную корректность и не измеряет качество модели.

### W1-05-E02 — минимальная содержательная ablation

Входы: один подходящий pretrained checkpoint, фиксированный train/validation split по camera/session или независимым клипам; одинаковые classes, labels, imgsz, batch/optimizer/compute budget, seed, checkpoint-selection rule и inference thresholds. Заранее определить critical-class metric и допустимое ухудшение clean slice вместе с evaluation, без выдуманного численного порога сейчас.

Контроли: (B0) текущий воспроизводимый default recipe с явной фиксацией optional Albumentations; (B1) согласованный conservative recipe с выключенными mix-операциями/ненужной геометрией. B1 является кандидатом, не установленно лучшим baseline. Далее относительно выбранного фиксированного контроля: (P) одна фотометрическая группа; (D) compression/blur группа; (G) небольшая геометрия/scale, только если E01 допускает; (M) mosaic отдельно; mixup и occlusion только после конкретной гипотезы ошибки. Не запускать сразу полный factorial grid. Для редких classes главный вопрос — улучшение на независимых видимых instances, а не средний train loss.

Наблюдения: per-class AP/recall и precision при фиксированной рабочей настройке, размерные bins PPE, clean/degraded и camera slices, critical misses, ложные тревоги на независимом видео с фиксированным event logic; измерить epoch/wall-clock cost. Для suppression conf/NMS оставить одинаковыми. Если inference threshold позже настроен отдельно, это отдельное вмешательство.

Артефакты: diff конфигов, manifest/checksums данных, seed, versions, checkpoint selection log, prediction files, per-slice metrics и before/after error examples. Исходы: устойчивый useful gain → сохранить candidate; только synthetic-corruption gain без real-camera gain → исследовать mismatch, не объявлять внедрённым улучшением; потеря clean/critical class → ослабить или отвергнуть. Stop rule: не расширять группу при broken E01 либо ухудшении заранее согласованного critical gate; ключевой выигрыш повторить на другом seed/независимой группе, если size/variance делают выбор неустойчивым. Один trial подтверждает только этот split/seed/budget; совместимость LinQ остаётся отдельной.

### W1-05-E03 — проверить маленький объект и фильтрацию

Входы: train subset с маленькими PPE/сигаретами, сохранённый размер после resize/letterbox, pinned source F05/F10. Контроль: та же модель/входной размер без добавленной spatial augmentation. Действия: отдельно включить scale/crop/mosaic, вывести распределения размеров и survival; вручную сопоставить исчезнувшие/оставшиеся labels. Не менять библиотечный filter ради формального роста survival, пока не установлена visual labelability.

Метрики: survival small-instance/class, доля evidence-erased-but-label-retained, per-class small recall на untouched real validation, стоимость загрузчика. Артефакты: object-ID table, overlays на границах фильтра, config/code revision. Исходы: labels исчезают массово → уменьшить strength или пересмотреть масштаб наблюдения с W1-06; видимость утрачена без фильтрации → semantic gate/ignore, не синтетическое `no_PPE`; размеры сохранены, real recall не вырос → прекращать эту ветку. Stop rule: после обнаружения систематического удаления критичного класса прекратить длительный training candidate до коррекции. Это проверяет pipeline и конкретную гипотезу, не устанавливает минимальный детектируемый размер любой модели.

### W1-05-E04 — clean / real degraded / controlled corruptions

Входы: независимое реальное validation-видео разных освещений/качества с проверенными labels; от train отделено до аугментаций. Если реальных плохих условий нет, добавить контролируемые corruptions как диагностический secondary set, явно с общими original IDs. Контроль: clean originals с тем же preprocessing. Метрики и артефакты E02 плюс severity, тип transform/codec, camera/session IDs и парные predictions. Не считать corrupted copies независимыми observations.

Исход: synthetic robustness без подтверждения на реальном потоке оставляет transfer открытым; деградация clean запускает trade-off review; выигрыш real target подтверждает лишь представленные режимы. Stop rule: прекратить подбор strengths по lockbox; фиксировать strengths по train/validation, окончательный test использовать после выбора. Проверка кадра не подтверждает event-level false alarms или temporal robustness.

## Открытые вопросы и адресные передачи

- **W1-05-Q01, P0, полный кейс / datasets / violation_methods:** object labels или person states/events? Видимый head без каски и невидимый head — разные состояния? Какие ignore/unknown/occlusion правила? Изменяет допуск F17–F22; получить ontology и примеры аннотатора до mixing/occlusion.
- **W1-05-Q02, P0, artifact/runtime:** какой фактический checkpoint, trainer и package lock? Поддерживает ли будущая среда custom list без тихого skip? Известны source signatures; нужен E01, не ещё одно предположение по live docs. → model_stack/W1-12: F01–F08, особенно bbox-only copy-paste, classification erasing и фактический смысл close_mosaic.
- **W1-05-Q03, P0, target data:** реальный размер evidence в пикселях, blur/lighting/codec и independent cameras? Без samples нельзя назначить compression quality, kernel size и силу scale. → datasets/W1-06: E03 и список требуемых difficult slices.
- **W1-05-Q04, P1, evaluation:** какие critical-class gates и допустимый clean/robustness trade-off? → evaluation/W1-15: E02/E04, F15/F16; synthetic severities и соседние frames не независимый test.
- **W1-05-Q05, P1, violation_methods/video_architecture:** используются ли camera-fixed ROI, tracks или клипы? Для них transforms должны включать ROI/relations и temporal coherence. Иначе ограничить вмешательство обучением object detector с отдельным неизменным event layer.
- **W1-05-Q06, P1, W1-11:** есть ли masks и валидированные person-PPE group relations для copy-paste? Передавать F06/F22; просто включить `copy_paste` для bbox-only недостаточно.
- **→ linq_platform/model_stack:** перечисленные data augmentations не являются доказательством исполнения на ускорителе. Сохранять итоговый checkpoint и фактические input shape/preprocessing; экспорт/квантизацию/target runtime проверять отдельно. Ни timings RTX4070, ни память, ни поддержка LinQ не установлены.

Ветка завершена на уровне research: установлены фактические switches/version boundaries, семантические риски и наблюдения, которые разрешают или отвергают вмешательство. Универсальная вероятность/strength для отсутствующих данных намеренно не объявлена найденной.
