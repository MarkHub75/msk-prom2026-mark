# W2-01 — Native KD: package provenance, YOLO11 pair и student contract

**K001; P0.** Исследовано 23.10.2026, Europe/Moscow (UTC+3); завершающая фиксация первичных metadata 07:33:20+03:00. Context version: mosprom-research-v1. Это результат второй волны, а не практический trial.

**Ответ:** native KD стал конкретной условной опцией для `YOLO11n ← target-trained YOLO11s`, detect, стандартные P3–P5 YAML. На уровне прочитанного кода обе модели имеют согласованные feature grids, доступный head-score interface и штатный путь к обычному student. Опубликованный wheel `ultralytics==8.4.184` действительно содержит те же десять проверенных файлов, что W1 pin. Это существенно сильнее одной строки `__version__`, но ещё не installation/runtime/quality/export/LinQ success.

Фактически прочитаны Context-prompt.md и prompt-training-strategy.md полностью, общий блок W2_TASKS и W2-01, PLAN, общий вывод/K001/внешние неизвестные CRITIC, полностью W1-10, назначенные W1-02 F06–F12/E01 и W1-13 F13/F14/Q01/Q02. Новый поиск выполнен web search; реально открыты official docs, release, metadata и pinned raw code. Wheel размером 1 429 044 bytes прочитан HTTP→in-memory ZIP, SHA256 проверен; содержимое модулей сравнивалось как bytes. Никаких Python-модулей Ultralytics не импортировали и не исполняли. Не выполнялись pip install, скачивание weights, forward/backward, training, resume, export или target inference. Изменён только этот файл.

## 1. Решение и границы

Искали, есть ли native KD route ближе к публичному LinQ lead `yolo11`/`yolo8`, чем один пример YOLO26 из W1. Важны три разные проверки: опубликованный package содержит нужную реализацию; конкретная пара совместима по training tensors; финальный inference artifact действительно обычный student. Первая установлена по bytes, вторая по исходникам для стандартной пары, третья по lifecycle кода. Ни одна не доказывает качество на наших камерах или поддержку фактически выдаваемого LinQ.

`U = e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8` — W1 pin, commit 2026-10-22T20:27:18Z. `R = f7dd275e5853801674ca78ef51896617bb5362ba` — release commit, 2026-10-22T17:39:36Z. Далее все code locators относятся к U; десять перечисленных ниже package files побайтно совпадают с опубликованным wheel. Не исследуются полный model_stack, все teacher architectures, QAT или оптимальный `dis`.

## 2. Новые первоисточники и actual access

Доступ всех строк: **2026-10-23 MSK**. Автор кода/docs/package — Ultralytics. Дата публикации live docs не установлена; стабильный source Markdown привязан к U. `CODE` означает чтение, `META` — metadata, `LOCAL-BYTES` — наша служебная проверка содержимого архива; ни одна метка не означает выполнение detector.

| S-ID | Title / прямой URL | Version/date и locator | Что действительно получено |
|---|---|---|---|
| W2-01-S01 | [Knowledge Distillation guide](https://docs.ultralytics.com/guides/knowledge-distillation); [pinned Markdown](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/docs/en/guides/knowledge-distillation.md) | Live + U; Prerequisites, Recommended Model Pairs, FAQ Which tasks and models, Resuming, Training Output | Обе страницы прочитаны. Общая same-family support включает YOLOv8/YOLO11/YOLO26; рекомендованные именованные пары и опубликованный benchmark относятся к YOLO26. Это документация автора, не runtime test YOLO11. |
| W2-01-S02 | [tag ref](https://api.github.com/repos/ultralytics/ultralytics/git/ref/tags/v8.4.184), [annotated tag object](https://api.github.com/repos/ultralytics/ultralytics/git/tags/7e508d6f2249b60bf67e2108fc1678b93f504100), [release](https://github.com/ultralytics/ultralytics/releases/tag/v8.4.184), [release API](https://api.github.com/repos/ultralytics/ultralytics/releases/tags/v8.4.184) | tag v8.4.184 → tag object 7e508d6f2249b60bf67e2108fc1678b93f504100 → R; tagger 2026-10-22T17:39:54Z; release published 17:41:34Z | META: все API получены независимым HTTP; release HTML открыт web. `target_commitish: main` не использован как immutable pin — взят dereferenced tag. |
| W2-01-S03 | [R→U compare](https://api.github.com/repos/ultralytics/ultralytics/compare/f7dd275e5853801674ca78ef51896617bb5362ba...e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8), [U commit](https://api.github.com/repos/ultralytics/ultralytics/commits/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8) | U is ahead by one commit; message Standardize citation admonition titles across docs (#26844) | META: compare и file list получены; изменены docs paths, не перечисленные training files. Bytes comparison S04 — отдельная проверка нужных файлов. |
| W2-01-S04 | [PyPI version JSON](https://pypi.org/pypi/ultralytics/8.4.184/json); [wheel](https://files.pythonhosted.org/packages/9f/a6/9f12ea1984a10838e5771c530b3072fcff8e671ca2ebbbcb15d08fff2be4/ultralytics-8.4.184-py3-none-any.whl); [sdist](https://files.pythonhosted.org/packages/db/15/907181d03defbace7d2c710dc568c5a2b70875bf5d3c833a4bcdd7a179b2/ultralytics-8.4.184.tar.gz) | version 8.4.184; wheel uploaded 2026-10-22T17:42:28.108617Z; sdist 17:42:32.505239Z; both yanked=false | JSON и wheel реально получены; wheel ZIP просмотрен без установки. Sdist — только metadata, bytes не получены. Requirements metadata не является environment lock. |
| W2-01-S05 | [nn/distill_model.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/distill_model.py) | U; `__init__` L64–119, `get_distill_layers` L175–193, `train/_freeze_teacher` L195–208, `loss` L238–285, `loss_sl2` L287–307, `decouple_outputs` L337–355, `fuse` L225–236 | CODE: весь файл получен и прочитан; API и tensor trace. |
| W2-01-S06 | [YOLO11 YAML](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/models/11/yolo11.yaml), [YOLOv8 YAML](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/models/v8/yolov8.yaml), [YOLO26 YAML](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/models/26/yolo26.yaml) | U; scales, feature-layer indices, final Detect, end2end/reg_max | CODE: все три YAML полностью прочитаны. Каналы для n/s ниже выведены из YAML+parse_model, не сняты с запущенной модели. |
| W2-01-S07 | [nn/tasks.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/tasks.py), [nn/modules/head.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/modules/head.py), [detect/train.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/models/yolo/detect/train.py) | U; DetectionModel L522–552; load_checkpoint L2022–2068; parse_model L2086–2089/L2183–2205/L2241–2245; Detect init/forward_head/forward L108–204; DetectionTrainer attributes/get_model L139–149/L183–199 | CODE: fetched files, прочитанные функции class/head/load contract. |
| W2-01-S08 | [engine/trainer.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py), [utils/torch_utils.py](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/torch_utils.py), [default.yaml](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/default.yaml) | U; _setup_train L341–445; save_model L768–836; setup_model L873–907; final_eval L1005–1022; check_resume L1024–1068; ModelEMA L836–852; strip_optimizer L895–957; distill_model/dis defaults | CODE: integration, checkpoint/extraction lifecycle. Default YAML также побайтно проверен в wheel. |

**Сбои и их область.** Web open tag-ref API вернул tool Internal Error/URL not accessible; обычный read-only HTTP того же первичного endpoint успешно получил JSON. Search snippets показывали release list лишь до 8.4.183 и старую PyPI landing cache; они не приняты за отсутствие 8.4.184, поскольку version endpoints и bytes получены. Первая печать pinned Markdown через Python упала на локальном cp1251 UnicodeEncodeError; повтор с UTF-8 stdout прочитал текст. Это сбои навигации/вывода, не отсутствие native KD.

## 3. Package provenance — что теперь действительно воспроизводимо

### W2-01-F01 — Есть опубликованный пакет, но U не является release commit

**META + LOCAL-BYTES; S02–S04.** `__version__=8.4.184` в U было недостаточно. Теперь установлена цепочка annotated tag → R → release → PyPI wheel. U — следующий commit с изменениями docs. Поэтому запись «U есть тег 8.4.184» неверна; корректно: «U code contract для выбранных файлов совпадает с wheel 8.4.184».

- Wheel SHA256: `d04c80f27d335fe27a057dcf00f91c843b11f99d21e7b3017616959a523bfc8a`; computed digest равен PyPI JSON.
- Sdist SHA256 из metadata: `e556832d07f70ba2f73aa8140dceb2a8fb3d5e9a0d9c70827f22a658d292d0ad`; independently computed digest отсутствует, sdist не читался.
- Проверены exact bytes следующих десяти wheel entries относительно raw U: `ultralytics/nn/distill_model.py`, `engine/trainer.py`, `utils/torch_utils.py`, `nn/tasks.py`, `nn/modules/head.py`, `models/yolo/detect/train.py`, `cfg/models/11/yolo11.yaml`, `cfg/models/v8/yolov8.yaml`, `cfg/models/26/yolo26.yaml`, `cfg/default.yaml` (все пути после первого относительно `ultralytics/`). Все equal=True.
- Для ключевого `nn/distill_model.py` SHA256 bytes: `190311d996f9964a9f4302a41f43bd25f3b482516270e148df16f491b9d4fc9b`.

Это воспроизводимый **package artifact**, а не воспроизведённая установка. Metadata допускает Python >=3.8, torch>=1.8.0 с отдельным исключением torch==2.4.0 на Windows; множество зависимостей задаётся диапазонами. Для будущего smoke нужен собственный resolved dependency lock/driver record. Wheel не содержит доказательства, что любая разрешённая комбинация зависимостей успешно выполнит данный route. Архив прочитан в памяти; дополнительных source files на диске не создавали.

### W2-01-F02 — Documented support шире примера, runtime status уже

**DOC + CODE; S01/S05–S07.** Same-family detect для YOLOv8 и YOLO11 прямо назван в FAQ; это не только наше предположение из `isinstance(Detect)`. Но named recommended pairs и benchmark в guide — YOLO26. Следовательно, YOLO11n←YOLO11s имеет documented family support + code-supported конкретный tensor route, без опубликованного в этом guide YOLO11 pair benchmark и без нашего runtime test.

Constructor проверяет наличие Detect-family head и одинаковое число hooked entries (neck levels плюс head), но не family/task names, class semantics или равенство strides. Успех constructor сам по себе не расширяет documented matrix. Cross-family YOLO11↔YOLO26 оставляем unsupported по docs, даже если какие-то tensor формы могли бы пройти.

## 4. Concrete candidate: YOLO11n student ← YOLO11s teacher

### W2-01-F03 — Feature/head contract стандартных n/s

**CODE + INFERENCE FROM CODE; S05–S07.** Candidate checkpoint interface: unfused standard detect YOLO11n student initialization и отдельно уже обученный/проверенный на требуемом target task YOLO11s teacher `.pt`, с сохранёнными hash/YAML/ontology. Названия `yolo11n.pt`/`yolo11s.pt` описывают архитектуру; наличие готового target-trained teacher пока неизвестно. COCO teacher не объявляется PPE teacher.

| Contract field | Student YOLO11n | Teacher YOLO11s | Область подтверждения |
|---|---|---|---|
| YAML/scales | yolo11.yaml, n: depth .50, width .25, max_channels 1024 | тот же YAML, s: .50/.50/1024 | S06; стандартные YAML, без custom P2/P6/head |
| Detect inputs/head index | `[16,19,22]`, head 23 | `[16,19,22]`, head 23 | get_distill_layers возвращает `[16,19,22,23]` обеим |
| Neck strides | `[8,16,32]` | `[8,16,32]` | YAML geometry; DetectionModel вычисляет stride dummy forward в будущем выполнении |
| Neck channels | `[64,128,256]` | `[128,256,512]` | Выведены scaling в parse_model, не local tensor observation |
| Example grids at square 640 | `80×80,40×40,20×20` | те же | Аналитический пример: 640 кратно 32; всего N=8400 locations, это не batch benchmark |
| Channel adaptation | 3 отдельных Conv1×1→ReLU→Conv1×1 projector | teacher features — targets | Только channels; interpolation/resampling отсутствует |
| Head type | Detect, legacy=False, reg_max16, no dual o2o | то же | C3k2 выставляет legacy=False; YAML не задаёт end2end/reg_max, defaults parse_model дают false-like и 16 |
| Raw score interface | B×nc_student×N | B×nc_teacher×N | forward_head возвращает dict `boxes/scores/feats`; KD использует teacher `scores` |

Teacher и student получают **один и тот же `batch['img']`**, включая уже применённую геометрию/augmentation. На каждый batch hook features сопоставляются по порядку levels. Нужно равенство реальных H/W и layout для каждого level при каждом training shape. В wrapper нет compare stride/H/W и нет автоматического spatial align: flatten+MSE не является проверкой правильной геометрии. Число locations одинакового произведения H×W тоже не доказывает одинаковое пространственное соответствие.

Constructor делает отдельный zero dummy forward размером **2×ch×imgsz×imgsz**, чтобы определить channel dimensions; это дополнительная allocation даже до первого training batch. В штатном trainer imgsz предварительно нормализуется check_imgsz с max_dim=1. Ни факт наличия dummy forward в исходнике, ни наша арифметика не означают, что он помещается в имеющуюся VRAM.

### W2-01-F04 — Head scores: усредняются logits, равенство reg_max не проверяется KD

**CODE; S05 `loss/decouple_outputs`, S07 `Detect.forward_head/forward`.** В текущем общем Detect `scores` — pre-sigmoid class logits. Teacher eval возвращает `(decoded, raw)`; decouple_outputs берёт raw tuple[1].

- У стандартных YOLO8/11 raw dict не имеет `one2many/one2one` wrappers. Вызовы decouple_outputs для обеих branches возвращают **один и тот же** dict; `(scores+scores)/2` оставляет обычные logits неизменными. Поэтому отсутствие dual head не ломает feature KD route.
- У стандартного YOLO26 raw dict содержит обе branches. Wrapper усредняет **logits** one2many и one2one, затем делит locations по реальным teacher neck H×W, применяет sigmoid и max по class dimension. Это не среднее двух sigmoid probabilities и не веса после NMS/top-k.
- Получается score каждого location формы B×1×N_level. Он взвешивает squared error всех feature channels. Student class logits или box distributions в KD напрямую не сопоставляются; supervised detection criterion остаётся student criterion.
- `reg_max` участвует в устройстве собственной box branch Detect, но wrapper не требует teacher/student equality reg_max и не передаёт localization-distribution targets. Для безопасного candidate обе стандартные YOLO11 имеют reg_max16; YOLO26 имеет reg_max1. Не превращать это в поддержку cross-family: её docs исключают.
- Teacher checkpoint для dual-head route должен сохранять ожидаемые raw branches. Deploy-fused/обрезанный checkpoint, где one2many удалена, не следует автоматически допускать как teacher: wrapper обращается к обеим `scores`. Для конкретной YOLO11 пары сохраняем unfused training artifact; не используем arbitrary exported artifact.

### W2-01-F05 — Student получает target nc/names, teacher сохраняет свой task/class contract

**CODE; S05 `__init__`, S07 `DetectionTrainer.get_model/set_model_attributes/load_checkpoint`.** Student строится с dataset `nc`/`channels`; target names задаются до `model.load` для class-row remap, затем trainer attaches dataset names/nc/args. Это W1-02-F09/F10, теперь прослеженное до KD boundary.

Teacher загружается через `load_checkpoint(teacher_path)`: выбирается checkpoint EMA либо model, float/eval; dataset nc/names туда не передаются. Если teacher input channels не совпадают, wrapper **пересоздаёт teacher с ch student, но nc из teacher YAML**, затем `.load(weights)`. Это не target-class adaptation teacher. Такой channel rebuild может изменить/частично перенести входные weights; semantic/quality equivalence нового teacher не установлена. Для выбранного route gate требует одинаковые исходные channels и отсутствующий неожиданный rebuild.

В wrapper нет class-remap teacher→student и нет проверки равенства nc/names. Однако **разное nc само по себе не означает tensor error**: max по teacher class dimension сворачивает её до одного числа на location. Даже permutation teacher class rows оставляет max score тем же при неизменных features/logits. Поэтому W1 «зафиксировать совпадение ontology» следует понимать как conservative teacher-admission/interpretation gate, а не обязательное условие shape equality в loss.

Различаем случаи:

| Teacher/student class relation | Technical trace | Что можно утверждать о знании |
|---|---|---|
| Одна ontology и корректные target-trained teacher weights | Score weights/features технически согласуются при верной геометрии | Разумный основной candidate; качество teacher и student всё ещё измеряются |
| Те же nc, другой порядок имён | Wrapper не переставляет классы; max weighting permutation-invariant | Для этого feature loss порядок не создаёт logit matching error; metadata/inference semantics и supervised student row transfer отдельно проверить |
| Разные nc или subset/superset | Может пройти: teacher class axis сворачивается; student имеет собственный supervised loss | Feature guidance возможно, польза на новых классах неизвестна; это не передача их teacher logits |
| Те же имена, иной смысл или COCO без нужного target class | Никакой semantic error detector в wrapper нет | Load success не доказывает target competence; teacher может придавать вес нерелевантным объектам и смещать features |

Следствие для очереди: не переписывать teacher class count только ради nc equality и не называть случайный новый target head «готовым teacher». Сначала отдельно обучить/получить соответствующий teacher и подтвердить его полезность на development slices. Сохранить реальные source/target class definitions, даже если loss не использует их строки.

### W2-01-F06 — Limited support matrix

| Пара/режим | Documented | Code-observed на U / wheel 8.4.184 | Требует runtime / не установлено |
|---|---|---|---|
| **YOLO11n←YOLO11s detect** standard P3–P5 | Same family/task прямо разрешены; named recommendation для этой пары не дана | `[16,19,22,23]`, 3 grids, channel projectors, single raw-score dict; reg_max16; student-only extraction | Exact chosen checkpoints, old serialization compatibility, gradient/freeze/BN/VRAM/reload/export; target benefit и LinQ |
| YOLOv8n←YOLOv8s detect standard | Same-family support прямо названа | `[15,18,21,22]`, P3/8–P5/32; n→s channels `[64,128,256]→[128,256,512]`; legacy=True cls branch, reg_max16; тот же raw dict contract | Не второй обязательный trial; те же artifact/runtime gates; legacy checkpoint нельзя считать протестированным |
| YOLO26n←YOLO26s detect standard | Named recommended pair, guide example и benchmark | `[16,19,22,23]`, 3 levels; reg_max1; dual head, logits-average weighting | Native example сильнее по docs, но пригодность конкретного graph для LinQ неизвестна |
| YOLO11←YOLO26 / YOLO8←YOLO11 | Cross-family docs исключают | Constructor не проверяет family; отдельные совпадения tensors возможны | Не предлагается как supported route; требует самостоятельного исследовательского port/обоснования |
| Custom P2/P6, чужой head, deploy-only teacher | Не покрыто конкретным candidate contract | Количество levels проверяется, H/W/stride/branch semantics не полностью | Нельзя наследовать поддержку от названия family; отдельная проверка или stop |

Наличие двух code-compatible leads не означает требование обучить обе пары. Если model_stack выберет подтверждённый LinQ student YOLO11n, достаточно first smoke этой пары. Если выбран YOLO8, переносится логика admission и меняются pinned artifacts/indices; не обещается одинаковый результат.

## 5. Final artifact и resume

### W2-01-F07 — Teacher исчезает до final strip, projectors — при unwrap

**CODE; S05/S08.** Существенное уточнение W1-10-F06: стандартный `save_model` сериализует не полный live teacher, а deepcopy **EMA wrapper**, у которого ModelEMA.__init__ уже выставил `teacher_model=None`. На диске остаются student + projectors + wrapper/hook machinery и путь teacher в train_args. Teacher file нужен для **восстановления training**, а не содержится в обычном сохранённом EMA checkpoint.

| Стадия | Реальный model payload по коду | Teacher dependency / extraction |
|---|---|---|
| Live train | DistillationModel(student, frozen teacher, trainable projectors); teacher eval/no_grad | Teacher занимает память и выполняет forward каждого batch. Compile при KD отключается |
| EMA | Deepcopy wrapper → `teacher_model=None`; student+projectors retained | Отдельный дубликат teacher в EMA убран; это не unwrap student |
| save_model → last/best/epochN | `model=None`, `ema=half EMA wrapper`; epoch/optimizer/scaler/train_args и прочий state | Teacher weights из обычного payload отсутствуют; artifact ещё KD wrapper. Periodic files штатный final_eval не обрабатывает |
| setup_model из interrupted wrapper checkpoint | Новый dataset-driven student из weights.student_model; DistillationModel rebuilt; projector state restored | Teacher берётся из weights.teacher_model, если есть, иначе args.distill_model; нужен тот же сохранённый teacher artifact/path/hash |
| normal final_eval | strip_optimizer(last), strip_optimizer(best), затем final validation best | `_remove_feature_hooks()` → `model=student_model`; projectors вместе с wrapper больше не model graph |
| strip result | Model — student FP16, criterion=None, requires_grad=False; epoch=-1; optimizer/stopper/EMA/updates/scaler None | Стандартный inference artifact; train_args может всё ещё содержать строку distill_model. Само наличие строки не доказывает inference dependency |
| fuse() на wrapper | Удаляет hooks и возвращает student.fuse() | Вызвавший должен использовать **возвращённую** модель; это другой путь извлечения, не resume guarantee |

Прерывание до `final_eval` не получает student-only contract автоматически. Ветка с periodic/immutable checkpoint копией сохраняет возможность resume, тогда как нормальное финальное stripping last/best удаляет optimizer и projector training state вместе с wrapper. Это не exact bitwise continuation: полноценный scheduler/RNG/loader audit принадлежит W2-11. Здесь установлены только дополнительные KD зависимости.

`distill_model` входит в разрешённые check_resume overrides. Можно восстановить доступный путь к **тем же** teacher bytes; подмена teacher по новому path без hash verification меняет эксперимент, даже если загрузка проходит. После normal strip projectors восстановить из student нельзя. Новый supervised/KD run из финального student должен быть обозначен как warm start, а не продолжение старой KD оптимизации.

Final-only graph не подтверждён нашим export. Фраза docs об одинаковой скорости/размере — авторское утверждение о normal student graph; фактические file size, placement и latency должны сравниваться для выбранных artifacts/input/runtime. Метаданные, FP16 serialization и экспортные transformations тоже требуют осмотра.

## 6. Маршрут от метода к нашей пользе и outcome K001

| Уровень | Actual status | Что изменилось относительно K001 |
|---|---|---|
| Feature KD описан | Установлено W1, S01/S05 перечитаны | Не нужен новый общий обзор papers; механизм конкретно confidence-weighted neck L2 |
| Available implementation/package | **Установлено новым META+bytes evidence F01** | Не только source tree __version__: wheel доступен, SHA проверен, десять contract files совпадают с U |
| Candidate contract | **Code-supported, documented family support F02–F06** | YOLO11n←target-trained YOLO11s конкретизирован; class count не ложный runtime gate; head single/dual paths разведены |
| Student extraction/resume | **Code-observed F07**, не execution | Teacher отсутствует уже в EMA checkpoint; projectors живут до final unwrap; interrupted и final artifacts различаются |
| Target benefit | **Не установлено** | Нужны teacher audit и controlled student comparison W1-10-E02; новый benchmark gain не заявлен |
| Actual LinQ | **Не установлено** | Публичный vendor family lead W1-13-F13/F14 остаётся lead. YOLO11 standard graph/shape/quant contract требует SDK и target run |

**Рекомендуемый outcome для сборщика:** K001 «уточнена область / публичная contract-часть закрыта». Native KD — более конкретная условная опция, но не выбранный default и не готовое обещание прироста. Новых target measurements нет. Числа COCO из W1 не повторены и не перенесены на YOLO11.

## 7. W2-01-E01 — Первый smoke gate перед W1-10-E02/E03

**Статус PROPOSED, не выполнено.** Это дополнение operational detail к W1-10-E02/E03, а не ещё один quality trial. Решение: допускается ли ровно выбранная YOLO11 пара к controlled KD сравнению и final artifact проверке.

**Входы.** Wheel 8.4.184 с указанным SHA либо exact U checkout с dependency lock; установленная фактическая Python/PyTorch/CUDA/driver среда; unfused student initialization и target-trained teacher `.pt` с hashes и provenance; original YAML/scale/head attributes; одинаковые channels; согласованные target class definitions. Нужен небольшой корректный train-only diagnostic batch с полностью проверенными labels, включая допустимый empty image, и отдельные development inputs для reload parity. Camera/session holdout не участвует в debugging. Объём и compute budget назначаются после inventory, здесь не выдумываются.

**Контроль.** Supervised student из той же target-initialized state, тех же labels/geometry/batch/optimizer settings; во время correctness smoke он проверяет обычный head/loss/reload contract, а не superiority KD. Для последующего quality trial сохранить одинаковые sample/update budgets и отдельную цену времени, как W1-10-E02. Teacher выбирается до lockbox по релевантному audit, а не по финальному student result.

**Действия будущего инженера, процедурный псевдокод без нового CLI.**

1. Проверить установленную version/path и hashes перечисленных files; прочитать фактические student/teacher nc/names/task/channels и **head.nc**. Записать transfer/skipped tensors student; убедиться, что teacher не пересоздан неожиданно из-за channel mismatch. Сохранить полный teacher weight hash и доступный resume path.
2. После штатной trainer setup снять model types и hooks: для обеих `[16,19,22,23]`, actual stride `[8,16,32]`; зарегистрировать actual B/C/H/W каждого neck level. Проверить идентичный transformed input обеим моделям и равенство пространственных grids. Если включён multi_scale, повторить shape check на реально используемых крайних формах; square constructor check этого не заменяет.
3. Для стандартного YOLO11 head убедиться в raw `scores` B×nc_teacher×sum(HW) и отсутствии необходимости o2o. Проверить split sizes ровно H_i×W_i; score weights finite, в [0,1], имеют B×1×H_iW_i. Не интерпретировать их как вероятность корректной детекции. Сохранить отдельно supervised components и dis_loss.
4. Выполнить один разрешённый correctness forward/backward/update: teacher eval, все teacher requires_grad=False, gradients отсутствуют, weights и BN buffers не меняются; student/projector gradients finite и нужные trainable tensors обновляются. Проверить реальный compile=False и наличие projectors в optimizer. Записать peak memory, setup/dummy-forward cost и step time с явной timing boundary. Nonfinite/неожиданный rebuild/shape mismatch останавливают gate.
5. Сохранить отдельную immutable копию **pre-strip** checkpoint. В чистом training process проверить wrapper/projector reconstruction с тем же teacher hash; записать восстановленные keys/epoch/projectors. Это smoke resume, не bitwise equivalence promise. При недоступности teacher training resume должен быть признан неготовым; inference check final student от этого отделён.
6. Нормально завершить bounded smoke run; сравнить pre-strip и final last/best module manifests. Final не должен содержать DistillationModel/projector/FeatureHook в reachable model graph. Оставшаяся train_args.distill_model строка допустима как provenance. Отдельно periodic file не считать автоматически stripped.
7. Загрузить final artifact в новом process, где исходный teacher path недоступен, и выполнить **inference**, не `.train()`. Сравнить outputs с извлечённым тем же EMA student до stripping с учётом FP16 conversion, одинаковых inputs/decoding/NMS и заранее заданных numerical tolerances. Затем W1-10-E03 продолжает actual exporter/FP parity/SDK compile/target inference для выбранного student.

**Observables/артефакты.** Resolved environment, wheel+code hashes, original and resolved args, dataset/class maps, weight hashes, per-level tensors/strides, raw-score branches/split counts, requires_grad/BN snapshots, gradient/update summaries, optimizer groups, loss components, peak memory/time, immutable interrupted checkpoint, normal final checkpoint, module/key manifests, reload logs/raw outputs. Никаких обязательных AP claims из correctness batch.

**Исходы и next action.** Все contracts проходят → только тогда W1-10-E02 controlled KD vs supervised и W1-10-E03 deployment path. Wrapper/head/serialization failure → локализовать exact checkpoint/version и остановить KD, сохранить supervised candidate. Teacher слаб/нерелевантен → сначала data/teacher branch либо отказаться от KD; не увеличивать dis как автоматическое лечение. Нехватка памяти/времени → меньшее разрешённое batch/teacher или отказ от ветки после честного profiling, без выдуманного множителя затрат.

**Stop rule.** Ошибочный data/class transfer, spatial mismatch, teacher mutation, отсутствующий projector update, nonfinite loss, недоступный исходный teacher для resume, зависимость final inference от teacher или неустранимое нарушение resource cap запрещают promotion в большой run. SDK gap блокирует утверждение target success, но не маскируется как native KD failure.

**Предел подтверждения.** Успешный smoke означает корректность выбранных interfaces, сохранения и извлечения в данной среде. Он не доказывает convergence, качество редких классов/событий, преимущество KD, generalization новой камеры, export parity или LinQ execution. Порог practical gain и admissible degradation задаются case/evaluation, здесь не назначаются.

## 8. Открытые вопросы и адресная передача

| Q-ID / тип | Точный остаток | Значение/способ закрытия |
|---|---|---|
| W2-01-Q01 — artifact/experiment, P0 | Есть ли выбранные **реальные** student/teacher checkpoints стандартных YOLO11 с нужным task и разрешённым provenance? | model_stack фиксирует hashes/unfused artifacts/YAML; E01 проверяет old checkpoint compatibility. Public package route установлен, выбранных weights нет |
| W2-01-Q02 — case/data/experiment, P0 | Достаточно ли teacher лучше student именно на нужных class/size/camera errors? | teacher audit + W1-10-E02. Ни большее число parameters, ни target ontology equality сами по себе не ответ |
| W2-01-Q03 — SDK/target, P0 | Примет ли реальный LinQ exact final YOLO11n graph/input/postprocessing/quant representation? | linq_platform/model_stack получают build/op matrix/sample и выполняют compile/run. Vendor `yolo11` lead не закрывает |
| W2-01-Q04 — environment/runtime, P0 | Работают ли installed dependency set, wrapper setup, gradient path и serialization? | E01 на фактической машине с inventory; package bytes inspection не installation test |
| W2-01-Q05 — public artifact/experiment, P1 | Есть ли авторский complete YOLO11 KD recipe/quality evidence с teacher hashes и schedule/selection? | В просмотренном guide его нет; package contract позволяет собственный trial. Остаток не повод переносить YOLO26 gain или бесконечно ждать recipe |

**→ model_stack:** F01 даёт immutable package provenance; F03–F06 — минимальный YOLO11n←YOLO11s contract без custom loss port. Проверять actual chosen checkpoints, не только filenames. F07 требует хранить teacher+projectors до финализации; final inference получать из stripped student.

**→ datasets/evaluation:** F05 снимает ложное предположение, что mismatch nc обязательно вызывает crash; это повышает важность явного teacher-admission audit. Нужны определения classes и teacher quality по target errors; max weighting не решает semantic transfer. W1-10-E02 остаётся единственным quality comparison route, E01 лишь correctness prerequisite.

**→ linq_platform/video_architecture:** объект target проверки — обычный final YOLO11n с утверждённым input/preprocessing/decoding/NMS. Teacher не должен попадать в realtime pipeline. Исчезновение teacher/projectors по коду пока не является фактическим graph inspection или target benchmark.

**→ W2-11 / checkpoint control:** стандартный saved KD payload — EMA wrapper с teacher=None, projectors retained. `final_eval` last/best удаляет projectors через unwrap; periodic pre-strip checkpoint и exact teacher hash нужно сохранить заранее. `distill_model` path override допустим по check_resume, но другой teacher bytes — уже вмешательство.

**Для очереди W2-12:** native KD можно держать как одну conditional branch при уже пригодном небольшом student и сильном target teacher. Сначала E01 interface gate; затем reuse W1-10-E02/E03. Не требуется отдельное обязательное обучение YOLO8, YOLO11 и YOLO26 и не требуется готовить teacher с нуля ради проверки наличия KD.
