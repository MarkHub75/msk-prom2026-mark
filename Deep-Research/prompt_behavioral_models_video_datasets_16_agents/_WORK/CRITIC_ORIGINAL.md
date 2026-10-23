# Независимая критика W1 и задания W2

**Срез до W2:** 2026-10-23, после 20:02 UTC / 23:02 Europe/Moscow. Роль: отдельный High-критик со свежим контекстом. Прочитаны оба исходных промпта, `_WORK/CASE_NOTES.md`, `_WORK/PLAN.md`, `_WORK/SYNTHESIS_CONTRACT.md`, карта `_WORK/TASKS.json` и результаты всех шестнадцати W1-веток M01–M08/D09–D16; выборочно проверены сохранённые конфиги, manifests и материалы соседнего feasibility как **вторичные указатели**. Критик не получал новых сетевых доказательств, не запускал модели и не создавал агентов.

Этот текст — исходная критика первой волны. Её нельзя переписывать под результаты W2. Сборщик позднее добавляет отдельные исходы K-ID со статусами `closed`, `scope_narrowed`, `contradiction`, `still_open`, `superseded` и доказательствами. Перечисленные рекомендации веток рассматриваются как гипотезы, а не обязательный shortlist.

## Вердикт и достаточность W1

W1 уже даёт полезную исследовательскую базу: конкретные доступные веса и исходный код, реально полученные небольшие видео, разобранные аннотации и предметные причины, почему исходный benchmark не равен промышленной тревоге. Это существенно больше перечня архитектур. Положительные результаты нельзя обнулить из-за отсутствия ещё не выданного LinQ: источник, полученный файл, статическая структура, инференс и измеренный causal event benchmark — разные ступени доказательства.

**Пока не установлена полная подтверждённая промышленная цепочка «точный checkpoint → целевое видео → независимая событийная GT → причинные тревоги → реальный LinQ».** Исследование не должно симулировать эту ступень. Но несколько связок можно довести до точного воспроизводимого *плана первого запуска* за счёт ограниченной работы с payload, временем и семантикой; именно на них направлена W2. Главная ценность W2 — не ещё семь обзоров, а уменьшение числа неизвестных между выбранным артефактом и конкретным файлом проверки.

Уже достаточно установлено и не требует нового общего исследования:

- M01 разделяет pose-модель, детектор и crop/decode; MoveNet максимум шесть людей в MultiPose, default `num_poses=1` у актуального MediaPipe не объявлен жёстким single-person пределом. GT-box OCHuman и пропуск detector frames у RTMPose правильно ограничены. Не нужно повторять pose leaderboard.
- M02 установил конкретные `None`/empty, internal/emitted/predicted и post-association expiry особенности, а также acausal GSI/интерполяцию. Отсутствие собственного tracker run честно обозначено. Повторное чтение тех же функций не заменит будущий lifecycle эксперимент.
- M03/D10/D15 доказательно разделяют падение, fallen/lying, намеренное укладывание и наблюдаемую неподвижность; у URFD ADL есть 1 470 lying-labelled строк. Это сильное контрдоказательство подмене fall статической позой. OmniFall `fallen` не является GT неподвижности, а `walk` включает run/jog.
- M04/D11 дают настоящую CCTV action-разметку и полезные ограничения: CAVIAR same-ID walk→run; BEHAVE групповые, частично перекрывающиеся действия; VIRAT минимальную длительность/хвост разметки. MEVA current exclusions не переносятся автоматически на старые VIRAT DIVA gait labels.
- M05 доказал 77 AVA person-timestamp phone+walk совпадений, а не 77 событий; UPT имеет реальный payload и различимую person–object пару, но это image HOI. D12 добавил фактически декодированный Charades donor и реальные недостатки P-DESTRE. Повторно считать AVA строки не нужно.
- D09 различает реальные видео, clip classes и настоящие event labels; SARD 4.txt, 42 Foundation Pit MP4 и printing-factory join проверены содержательно. D13 различает публичные real videos и withheld real GT у SmartSpaces. Нельзя превращать эти корпуса в готовый near-miss benchmark.
- M07/D14 локализовали ограничения climb/crawl/attachment/carry. Возврат на ту же сторону не доказывает completed climb; hook выше harness не доказывает соединение; SAFELIFT 176 `unknown`/6 `intermediate` не даёт бинарной unsafe GT. Эти отрицательные результаты заслуживают места в shortlist/stop-list.
- D15 уже содержит достаточный проект event schema, uncertain/censored matching и exposure accounting. D16 содержит первичные положительные **и отрицательные** transfer результаты. Ещё одна общая заметка о leakage, synthetic-to-real или «нужны hard negatives» не является полезной W2.

Положительные CC BY/CC0/Apache/MIT заявления надо сохранять в их реальном объёме. Не найденная отдельная лицензия весов — неизвестность области grant, а не доказательство запрета; ограниченная видимость предмета — неизвестность действия, а не отрицательный класс. В частности D14 нашёл актуальные official HMDB/HF CC BY4.0 statements: поздний синтез должен дополнить ими более раннюю неопределённость M04, сохранив отдельный вопрос upstream footage. Это уже доступное W1-разрешение локального расхождения, не повод для новой задачи.

## Покрытие восьми сценариев и разумные границы выбора

| Сценарий | Что реально добавлено W1 | Остаток, способный изменить решение |
|---|---|---|
| 1. Бег/резкое перемещение | HMDB SlowOnly run32/walk49 checkpoint; KTH triplet; CAVIAR и BEHAVE media+labels; VIRAT actor/action joins | CAVIAR/BEHAVE clock/overlay ещё не сертифицированы; gait не равен speed/acceleration; короткие промышленные рывки и fast-walk требуют target footage. K003 |
| 2. Движущийся механизм/транспорт | Exact temporal NearCollision donor с действительным HDF5; SmartSpaces реальные камеры и calibration; точные отрицательные policy cases | Ego TTC не pair-risk; реальное содержимое SmartSpaces не просмотрено, GT скрыта, release scope противоречива; нет полного real moving-near/stationary-near/driver pack. K005 |
| 3. Телефон при работе **или перемещении по цеху** | UPT pair/verbs; AVA same-person sparse co-labels; Charades temporal donor; P-DESTRE distant annotations | Нет просмотренного AVA same-person continuous clip, target radio/scanner controls и independent equipment state; P-DESTRE ID=-1/h-w unresolved. K004 |
| 4. Курение/открытый огонь вне разрешённых мест | Два decoded HMDB smoke clips; проверяемый smoking prototype с sampling flaws; MmodalFire mist/dry-ice lead | В W1 нет нового замкнутого fire checkpoint+continuous negative chain; прежний feasibility — указатель, не первичная текущая проверка. Нет target permit/steam/welding pack. K006 |
| 5. Ограждение/под конвейером/грузом | Публичные fence probes, exact pose rules; SynthSite votes/schema/results; SARD ladder donor | Происхождение fence media неизвестно, completion не доказан; синтетика не real validation; 3D under-load relation требует геометрии/другого ракурса/telemetry. Narrow configured corridor — отдельное имя события |
| 6. Высота без привязи | Harness/hook первичные papers и request-only CAAR/4-video leads | Known elevated surface + видимые straps/connector/anchor + policy не получены. Нельзя считать detector miss отсутствием; correct connection не следует из hook bbox. Внешний target/access gate |
| 7. Падение/лежание/неподвижность | OmniFall dense classes/splits; URFD lying ADLs; MCF erratum; реальный маленький temporal PT+ONNX pair и доказанные training-contract flaws | Нужна original-media/OmniFall time join и отдельная visible-low-motion GT. Прежде просмотренные Subject1/3 — dev. Нет обоснованного длительного hold и промышленного lockbox. K001/K002 |
| 8. Неправильная переноска | SAFELIFT8 decoded clips/physical endpoints; SARD carry tool/steel; UW-IOM action lead | Нет массы/частоты/согласованного handling rule, safe/unsafe target и carrying-route truth. Lift/lower action не универсальная unsafe-carry модель. Без target procedure — stop/reserve |

**Предварительная последовательность проверки, а не обязательная рекомендация:** (а) fall transition + separately lying/observed-low-motion; (б) visible flame outside an active allowed area, если K006 закрывает реальные controls; (в) один из gait/rapid-motion или moving-machine image-envelope, если соответствующий pack и target camera проходят gates. Нет оснований гарантировать три сценария. Один настроенный зональный/коридорный механизм считать одним переиспользуемым fallback, а не несколькими независимыми достижениями. Phone остаётся хорошим резервом при крупном видимом предмете; harness connection, physical under-load, общий unsafe carry, consciousness и тяжёлое temporal training не должны появляться в critical path без новых внешних входов.

Дополнительная apparent aggression из M08 имеет семантический AVA head/label путь, но без полученного видео, close-contact negatives и industrial holdout это **research extension**, не ready additional feature. Квоту 1–2 расширений нельзя заполнять core carrying/staggering или вторым именем одной зоны. W2 не должна открывать новый широкий поиск опасностей ради числа.

## K001 — рекомендованный pose frontend ещё не является одной согласованной поставкой

**Приоритет P0. Тип пробела:** интернет/артефакт/статическая проверка; фактические numerical parity и LinQ execution — отдельный будущий эксперимент.

**Затронуто:** M01-F009/F010/F011 и маршрут pose+track+rules M03/M08. M01-A01 — RTMPose-m AIC+COCO PTH; A02 — body7 ONNX ZIP. Аналогично RTMO A03 COCO PTH и A04 body7 ONNX ZIP различаются training mixture. M01 это правильно отметил, но provisional «RTMPose-m» всё ещё допускает случайное склеивание разных весов/конфигов. Для всех top-down маршрутов нужен внешний detector с собственным exact contract. Соседний tiny RTMPose SDK artifact уже глубоко исследовался; повторить его описание без нового различающего результата не нужно.

**Что доказано:** доступные конкретные publisher files, config/SimCC decode и значимые benchmark условия. Это достаточное основание рассматривать семейства, но не одна замкнутая build/reference поставка. HEAD не показывает actual graph, число outputs, postprocess notices или конкретные archive dependencies. Наличие ONNX не означает устройство LinQ.

**Последствие:** неверное RGB/affine/SimCC decode или незамеченная подмена body7 может испортить baseline до quantization и породить ложный вывод «pose не работает». Выбор larger m вместо уже доступного t должен иметь явную причину, а не случайное имя.

**W2_01 / Medium, результат `_WORK/W2_01.md`:** довести **один** RTMPose-m body7 ONNX SDK путь до проверенного полного static artifact contract; сравнить его с уже известным tiny route только по существенным различиям. Получить ZIP ограниченного размера, hash, file list, pipeline/deploy metadata, оба SimCC outputs, input shape/dtype/opset/operators, внешние файлы и применимые publisher notices; не выполнять модель/компиляцию. Отдельно указать точный person detector dependency из publisher recipe и его доступ/класс/веса; если он остаётся внешним unknown, явно оставить звено открытым. Не выдавать A01 PTH за source эквивалент A02. Точный teacher/corresponding training config искать по имени actual archive, а не по похожей строке.

Стартовать с уже проверенных:

- `https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/onnx_sdk/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip` (50 799 818 bytes metadata).
- `https://github.com/open-mmlab/mmpose/blob/759b39c13fea6ba094afc1fa932f51dc1b11cbf9/projects/rtmpose/README.md` и `projects/rtmpose/examples/onnxruntime/main.py` того же revision; `_WORK/M01/rtmpose*`, `ARTIFACT_HEAD.json`.
- Вторичный comparator: `../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md`, раздел RTMPose-t, и указанная там primary `https://huggingface.co/Tau-J/RTMPose/resolve/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/rtmposev1/onnx_sdk/rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip`. Не переносить его RGB/min-score вывод на новый archive без чтения actual pipeline.

**Нужное контрдоказательство:** несовпадающий graph/decoder, отсутствующая detector поставка, неясное происхождение export либо существенно более сложный input должны демотировать этот путь. PASS означает подготовленный exact reference bundle; он не доказывает целевую видимость суставов, скорость, события или LinQ.

## K002 — сильная fall-разметка пока не соединена с исходным clock и независимыми видимыми состояниями

**Приоритет P0. Тип:** bounded media/annotation proof по интернету и локальной визуальной сверке; промышленное качество, hold и независимая человеческая GT требуют будущей работы.

**Затронуто:** M03-F01–F03, D10-F04–F07/F12–F16, D15-F07. OmniFall GMD labels/splits разобраны, но исходное видео здесь не декодировано; пакет даёт rename/prepare route, а не доказанную эквивалентность каждого prepared/source PTS. Старая визуальная разметка Subject1/3 и новые OmniFall action seconds не взаимозаменяемы. Наличие fallen до EOF не подтверждает весь период low-motion. URFD ADL `0/+1` — полезные точные отрицательные leads, но действия в adl-10 не просмотрены.

**Что доказано:** 160 GMD paths, split train1/3,val2,test4, actual dense action CSV; 1 470 ADL lying rows URFD, sync adl-10. MCF исправленные камеры/времена и scenario23 contradiction локализованы. Нет необходимости скачивать 3.8 GB MCF или возвращаться к shallow Le2i search ради заполнения списка.

**Последствие:** без clock join нельзя честно измерять onset latency; случайно использовать знакомые Subject1/3 как «независимый тест» легко. Любое N=10/30 seconds нельзя валидировать коротким clipped tail или padding. Качество сомнительного temporal checkpoint не следует из наличия 30×5 input.

**W2_02 / Medium, `_WORK/W2_02.md`:** собрать маленький **проверенный development fixture**, а не заявленный blind holdout: (1) один уже известный GMD original положительный/намеренное укладывание и точная OmniFall join; (2) один ранее не просмотренный subject4 source из frozen test CSV как пример целевой структуры, после просмотра пометить development/reviewed; (3) URFD adl-10 видео и sync→frame/posture join. Получить только эти небольшие individual files, hash, полный decode PTS, несколько overlays/full interval review around transitions; сравнить decoded EOF и quoted boundaries. Отдельно описать observed transition, low posture и coarse low-motion evidence, видимость, recovery/EOF. Если независимых аннотаторов нет, не назвать свои intervals consensus GT. Не удлинять клипы; не исправлять original labels молча. Показать, какие длительности hold **вообще доступны**, а не выбрать N ради успеха.

Точные старты:

- `_WORK/W1_M03_EVIDENCE/hf_labels_GMDCSA24.csv`, `hf_splits_cs_gmdcsa24_test.csv`, `simplexsigil_src_omnifall__sources.py`, `hf_KNOWN_PITFALLS.md`.
- `https://huggingface.co/datasets/simplexsigil2/omnifall/resolve/83572a37b9e3081df8c06a56874b1d1f2a19386c/labels/GMDCSA24.csv` и `/splits/cs/gmdcsa24/test.csv`.
- Original source lead: `https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/tree/5abac7693229900cf80f722e878fbb119211fc1c`; первичный record `https://zenodo.org/records/13354453`. Установить конкретный subject4 member по CSV/tree, не выдумывать номер.
- `https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-cam0.mp4`, `https://fenix.ur.edu.pl/~mkepski/ds/data/adl-10-data.csv`, `https://fenix.ur.edu.pl/~mkepski/ds/data/urfall-cam0-adls.csv`; локальные originals в `_WORK/evidence_D10/`.

**Контрдоказательство:** неверное original/prepared time mapping, движение в fallen, добровольная lying ADL, короткий censor horizon или unknown visibility должны сузить scope. MCF scenario23 остаётся отдельным вопросом до осмысленного разрешённого видеоразбора; не требуется для закрытия этого fixture. Training flaws/неясные weight rights udayraj/Rchit уже достаточны для reserve; не тратить W2 на их full runtime reproduction.

## K003 — CCTV gait donors найдены, но их время/геометрия ещё не годятся для headline event metric

**Приоритет P0 для выбора running. Тип:** в основном независимая локальная проверка уже полученных media/labels; новые сетевые материалы только адресно, если нужны clock semantics.

**Затронуто:** M04-F02/F03/F08 и D11-F02/F03/F05/F06. CAVIAR decode содержит на один frame больше XML и необычные/повторяющиеся early PTS. BEHAVE XGTF `FRAMERATE1.0`/NUMFRAMES full source не совпадает с acquired25fps subclip; candidate global−35450 mapping и bbox scale не overlay-verified. Это реальные исследовательские предупреждения самих веток, не доказанные ошибки данных.

**Что доказано:** два CAVIAR same-ID перехода, реальное walk control видео, BEHAVE непрерывный 11 711-frame clip и exact group run labels. KTH native clock/segmentation даёт простой sanity fixture. VIRAT tails/minimum durations непригодны для unmodified short-burst truth; annotation-only DIVA000000 не должен незаметно заменять полученный другой source.

**Последствие:** ложный frame→seconds mapping создаст якобы большой latency/раннюю тревогу; group RunTogether может приписать gait человеку, которого не видно. Single lucky downsampling phase завысит low-FPS coverage. Высокая pixel velocity остаётся другой целью, чем run/jog.

**W2_03 / Medium, `_WORK/W2_03.md`:** на **уже локальных** CAVIAR Walk1/Fight_RunAway1 и BEHAVE35450–47160 сопоставить decoded order/frame identifiers/PTS и bbox overlays у начала, перехода и конца нескольких labels. Сохранить overlays и явный mapping/uncertainty. Не ограничиваться повтором XML parsing. Проверить несколько вариантов origin/scale по изображению, не выбирать offset только по лучшему model score. Для run episode указать, чьи действия источник действительно размечает; group rows не превращать автоматически в actor-complete GT. После alignment дать phase-sweep таблицу наблюдаемости native/1/2/5fps и случайные/бурстовые drops **без модели**; числа наблюдений не назвать recognition accuracy. Если early PTS нерегулярны, сохранить оригинал и отдельный documented canonical evaluation clock, а не «исправить» bytes.

Файлы: `_WORK/M04/caviarrun.mpg`, `caviarwalk.mpg`, `runxml.txt`, `walkxml.txt`, `video_annotation_checks.json`; `_WORK/D11/35450-47160.avi`, `35450-47160F.xgtf`, `markup.txt`, `behave_labels.json`, `behave_decode.json`.

Primary URLs при необходимости: `https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Fight_RunAway1/fra1gt.xml`, `https://homepages.inf.ed.ac.uk/rbf/CAVIARDATA1/Walk1/wk1gt.xml`, `https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/35450-47160F.xgtf`, `https://groups.inf.ed.ac.uk/vision/DATASETS/BEHAVEDATA/INTERACTIONS/markup.txt`.

**Контрдоказательство:** невозможность однозначного alignment или недостаточная per-actor gait видимость оставляет donor sanity-only. Не обязательно расширять задание на 65MB VIRAT acquisition/terms acceptance: если понадобится independent sustained-run reserve, его exact050301 путь уже в D11-S07–S10, с отдельным lawful access gate. Успех W2_03 не доказывает factory fast-walk, physical acceleration, source-disjoint generalization или достаточность1fps.

## K004 — phone semantically joined labels ещё не обеспечивают непрерывное same-actor видео

**Приоритет P1. Тип:** адресная media availability/visibility проверка; target confuser coverage и permission не выводятся из открытой разметки.

**Затронуто:** M05-F001–F004/F008; D12-F001–F003. AVA 77 совпадений по `(video,timestamp,person)` достаточны для наличия sparse co-labels, но ни одно соответствующее видео не получено. Charades2RFLZ действительно decoded, но его labels clip/interval-level без actor localization и phone/camera объединены. P-DESTRE phone bbox rows имеют ID=-1 и неразрешённый порядок h/w; общий -1 нельзя считать одной личностью. UPT HOI и AVA относятся к разным задачам.

**Последствие:** итоговая матрица может случайно соединить UPT weights, Charades temporal spans и AVA actor IDs в одну якобы tested chain. Phone at ear, carry, look/text, walk, equipment-work и разрешённый терминал должны остаться отдельными слоями. Сценарий из первичного кейса включает перемещение по цеху; нельзя сузить его до «только работа у станка» по тематическому пересказу.

**W2_04 / Medium, `_WORK/W2_04.md`:** из уже вычисленных 27 AVA candidate runs выбрать один-два точных person/time cases, проверить актуальную **официально допускаемую** media route/retrievability и, только если доступ разрешён, получить ограниченный clip с контекстом, hash/PTS, person-box overlays и полный short-interval review. Проверить cuts, phone visibility, same actor и actual walking. Не обходить авторизацию/платные стены/платформенные ограничения и не соглашаться с новыми пользовательскими договорами от лица команды. Если media не получена, это содержательный localized результат: не заменять её не связанным YouTube роликом. В таком случае использовать уже полученный Charades2RFLZ для полного bounded review и отдельно указать недостающую actor annotation. P-DESTRE 732MB member не скачивать ради попытки rescue без причины; exact bbox overlay — только если доступно ограниченное чтение нужных кадров и реально меняет camera-selection вывод.

Старты: `_WORK/W1_M05/ava_phone_walk_join.json`, `_WORK/W1_M05/ava_download.txt`, `_WORK/W1_D12/charades_2RFLZ.mp4`, `_WORK/W1_D12/charades_media_access.json` и остальная собственная evidence directory D12 `_WORK/W1_D12/`. Исходный выбранный AVA run `QTmwhrVal1g`,person91,1181–1190s; второй `WSPvfxtqisg`,person1,908–915s. URL идентификатора `https://www.youtube.com/watch?v=QTmwhrVal1g` — candidate media, доступ не установлен. Основная спецификация `https://sites.research.google/gr/ava/download/`; exact val CSV `https://research.google.com/ava/download/ava_val_v2.2.csv.zip` уже скачан, заново считать не нужно. Charades archive+member `https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip` / `Charades_v1_480/2RFLZ.mp4` уже получен D12.

**Контрдоказательство:** shot cut, слишком малый телефон, разные actor, непересекающиеся use/movement или unavailable media должны удержать scenario reserve. W2 не способна получить industrial radio/scanner/PPE negatives из отсутствующего класса; это target collection gate. При grants/visibility PASS всё равно нужны source-group split, dense actor GT и будущий causal model test; AVA +30frame future dependence не исчезает.

## K005 — приоритетный moving-machine сценарий нельзя ни подтвердить, ни окончательно снять без просмотра наиболее сильного real donor

**Приоритет P0. Тип:** интернет/media/release-scope; реальная near-miss GT, surveyed calibration и permitted test data — внешние gates.

**Затронуто:** M06-F01–F09, D13-F01–F05/F10; D09-F11. NearCollision реально содержит ordered windows/labels/checkpoint, но camera ego target и нет pair IDs/source groups; FP-TTC observation-plane TTC — другая задача. SmartSpaces eleven real video prefixes доступны, но ни один clip не decoded; положительные/отрицательные pair controls неизвестны. Публичный real media release противоречит privacy/Croissant тексту той же revision. D13 правильно различил challenge manual-label rule и универсальную data-license область; исходный unresolved статус нельзя превращать ни в blanket запрет, ни в беспрепятственное разрешение training/relabeling.

**Последствие:** можно ошибочно отказаться от действительно полезного real routine footage либо опереться на несуществующий driver/stationary-near control. Синтетические3D boxes и calibration reprojection «units» не дают независимую real safety GT/метры.

**W2_05 / Medium, `_WORK/W2_05.md`:** (1) по pinned release/current official change log/terms установить точную область real-video release и исключений вне AI City challenge; сохранить противоречие, если первичные тексты не разрешают его; не писать автору. (2) Если grant позволяет такой read/review, получить один-два individual MP4 **одной сцены**, сначала Camera0000, полный hash/decode/PTS и bounded full timeline review. Сохранить фактически видимых людей/технику, motion/stationary/driver-like/occluded segments как preliminary observed inventory, а не certified event GT. Выбирать вторую camera только для полезного наблюдения той же физической сцены; не считать её новым событием или независимыми exposure hours. Не добавлять manual challenge-test annotations для участия и не превращать challenge lockbox в training.

Точные старты: `_WORK/D13/real_tree.json`, `access.json`, `croissant.txt`, `smart_paper.txt`, оба calibration files; base `https://huggingface.co/datasets/nvidia/PhysicalAI-SmartSpaces/resolve/2cbe9563cbe9f47f846e5c871ee994572bbbc60e/MTMC_Tracking_2026/test/Warehouse_026/`, `videos/Camera_0000.mp4` (19 802 011 bytes), `calibration.json`; pinned `README.md`/`croissant.json` у repo root. Official scope sources `https://www.aicitychallenge.org/2026-faqs/` GeneralQ9 и `https://www.aicitychallenge.org/2026-track1/`. Бounded access при404/403 сохранять отдельно от отсутствия объекта.

Для detector звена взять **как вторичный lead** exact `https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt` и publisher `https://github.com/keremberke/awesome-yolov8-models/tree/fb4b7895a92913023ef222fdf0957b8ce2015766`: первично сверить model map0forklift/1person и scope grant/recipe, не повторять всю старую feasibility disassembly. Никакой инференс не требуется.

**Контрдоказательство:** отсутствие separate pedestrians/moving machines или неразрешимый reuse scope оставляет reserve и точный внешний вопрос. Даже если moving-near виден, это не independently certified collision/near-miss/policy violation. Нужны target stationary-near/moving-far/driver/turn/reverse/occlusion controls, ground envelope и actor-pair GT. Forklift-mounted request-only/non-profit paper не закрывается интернет-поиском; не расходовать W2 на его повторное чтение.

## K006 — fire/open-flame MVP пока наследует старую supply chain, а новые необходимые negatives не получены

**Приоритет P0, если open fire входит в shortlist; иначе P1. Тип:** адресный первичный artifact/media audit; target authorization policy и реальные factory controls — внешний эксперимент.

**Затронуто:** D14-F02–F05, M01-F012, D09-F13 и provisional fire preference, которую легко импортировать из соседнего feasibility. D14 дал новый smoking/action и MmodalFire lead, но не rechecked fire model+continuous test chain. Это не дефект его работы: ветка сознательно избегала повторения. Синтез текущего research обязан сохранить различие между текущей первичной проверкой и старым отчётом.

**Что доказано:** реальные HMDB smoke videos доступны/decoded, но это не открытый огонь и не dense smoking event GT; маленький smoking model имеет pose/timestamp/split flaws. MmodalFire public metadata/CC BY/4.93GB listed archive и описанные dry-ice/humidifier controls — primary evidence, но actual member/labels ещё не инспектированы. Предыдущий feasibility подробно показывал defects FURG XML, постоянное пламя от начала до конца и отсутствие smoke-only control; повторение тех же5 clips не исправит ignition/cessation/rearm gap.

**W2_06 / Medium, `_WORK/W2_06.md`:** независимо довести **одну** выбранную flame-perception supply chain до exact current primary card/labels/weight grant и bounded static payload confirmation; старые результаты использовать для адресного ограничения, не повторять generic fire detector catalog. Затем получить полный archive manifest и маленький подходящий nonfire mist/dry-ice member MmodalFire, если RAR/non-solid доступ позволяет bounded extraction, проверить labels/clock/полный short interval. Если all files huge/solid/условия мешают — остановить extraction и сохранить exact members/status. Найти в этом же release наличие настоящего onset/clear transition: binary sequence label не трактовать как dense interval. Новая ручная preliminary разметка должна быть отделена от original labels. Огонь на разрешённой печи/сварке, factory steam и inactive/active permit остаются target gates; laboratory mist их не заменяет.

Точные primary starts:

- `https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/13017fe8af477c25f5298d168e2dfede4b000753/best.pt` и card этого revision. Это **вторичный lead** из соседнего report, не W1 locally run model. Opposite label maps в чужих fire releases — причина проверить actual map, а не предположить0fire.
- `https://api.figshare.com/v2/articles/28804448`, `https://ndownloader.figshare.com/files/53696243`, `https://www.nature.com/articles/s41597-026-06810-6`; `_WORK/W1_D14_EVIDENCE/mmodalfire_figshare.txt`, `mmodalfire_article.txt`.
- Existing comparison evidence `../prompt_behavioral_safety_feasibility_16_agents/report_machine_behavioral_safety_feasibility.md`, раздел #4, и сохранённые там exact FURG/FIRESENSE locators. Не объявлять этих исходников независимым holdout от D-Fire-trained detector без provenance проверки.

**Контрдоказательство:** нет отдельного model grant/input map, mist визуально слишком иной, labels sparse/sequence-only или отсутствие onset/clear удерживают только narrow flame-region dev path. Даже полный PASS не показывает cigarette/smoker ownership, allowed industrial flame handling, tiny ignition recall, device export или real FP/hour. Smoking и open fire в итоговой матрице — две наблюдаемые задачи внутри одного case пункта.

## K007 — «каузальный streaming frontend» ещё не даёт task-specific temporal baseline

**Приоритет P1. Тип:** интернет/полный небольшой artifact/static graph; классификация событий, устойчивость state reset и CPU/LinQ стоимость — будущие эксперименты.

**Затронуто:** M08-F01–F06 и conditional route2. MoViNet-A0 Stream обоснован как causal architecture, но получены только headers15MB archive/27MB TFLite, не actual state signature/labels. README construction/current-legacy distinction и численные blog quantized условия не относятся автоматически к checked float binary. K600 classes не разложены на конкретные case semantics; готовый causal network не является pretrained industrial hazard detector. STGCN++/X3D точные sampling-contract flaws уже хорошо установлены; их не нужно заново обозревать.

**Последствие:** команда может выбрать сложный stateful classifier без релевантного head, перепутать per-scene с per-person state, принять накопленную10s classification за onset detector либо объявить blog int8 speed размером реально полученного float binary. Состояния/накопленное pooling могут переживать прекращение действия; causal не равно краткое/локальное/своевременное.

**W2_07 / Medium, `_WORK/W2_07.md`:** получить одну из двух небольших official поставок MoViNet-A0 Stream (предпочтительно TFLite для exact input/state contract), hash/version/storage generation, статически перечислить model signatures, state tensors, их matching input/output shape/dtype, quantization metadata/operators, class-map provenance и relevant/nonmatching case labels. Прочитать exact streaming/export/pooling/reset source pinned revision, объяснить что score фактически аккумулирует и как документация задаёт new-video reset. Не запускать TensorFlow/TFLite inference, модель/benchmark или генерацию ONNX. Отдельно найти, существует ли соответствующая advertised int8 file и explicit grant; если нет, не делать это причиной полного провала float reference. Показать один воспроизводимый first-run контракт и перечень future controls: cold-start, long normal prefix→event→clear, crop/actor/stream reset, state interruption, cadence change.

Точные старты: `https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tflite` (27 141 832 bytes); альтернативный `https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tar.gz` (15 165 440); `_WORK/M08/movinet.txt`, `artifact_heads.json`, `movinetblog.txt`; `https://github.com/tensorflow/models/tree/master/official/projects/movinet` как mutable locator, затем установить commit exact fetched source. Historical blog `https://blog.tensorflow.org/2022/04/video-classification-on-edge-devices.html` не текущий performance benchmark.

**Контрдоказательство:** signatures требуют неописанный state/layout, отсутствуют relevant labels, source/binary версии расходятся или score имеет неподходящую memory semantics — оставить generic training donor. PASS не показывает целевую superiority над rules, не создаёт target training data и не даёт LinQ поддержки. Nearest class name нельзя переименовать в policy violation.

## Карта W2, зависимости и критерии завершения

Все семь задач — отдельные Medium-задания с собственными evidence directories; результаты нельзя писать одновременно в общие итоговые файлы. Размер/число загрузок должны оставаться ограниченными; закончить на точном отрицательном результате допустимо. Никакого inference, training, аренды, outreach, новых пользовательских соглашений от лица команды или скрытой третьей волны. Модели выбираются по исходам, а не под заранее выбранный shortlist.

| Задача | K-ID | Решение, которое изменит | Главный deliverable |
|---|---|---|---|
| W2_01 exact pose bundle | K001 | m-body7 SDK versus existing tiny/alternative frontend | Static graph+pipeline+detector dependency+scope manifest |
| W2_02 fall media/clock fixture | K002 | Fall/lying/hold distinctions and first viable data pack | Original video↔CSV↔PTS join, bounded visible-duration/censoring evidence |
| W2_03 gait alignment | K003 | CCTV gait reserve versus narrow displacement proxy | Box overlays/origin/time mapping and phase/drops observability |
| W2_04 phone actor/video | K004 | Whether phone-use+movement has a concrete development sequence | Actual availability/visibility/actor continuity or exact localized failure |
| W2_05 real machine donor | K005 | Moving-machine reserve or narrow scene envelope | Release-scope counterevidence, observed real control inventory, exact detector link |
| W2_06 flame/confusers | K006 | Admit/demote visible-flame MVP branch | One exact perception supply chain + real mist/control and temporal-label boundary |
| W2_07 streaming temporal bundle | K007 | Whether to spend engineering time on MoViNet | Actual signatures/states/class-map/temporal memory contract |

W2_01/02 и W2_03 независимы и высокоприоритетны; W2_05 полезен рано, поскольку case приоритизирует dangerous proximity. W2_06 не надо откладывать, если flame предлагается вторым MVP. W2_04/07 — bounded reserves, не критическая цепочка доставки. W2_03 phase outputs должны питать общий E006; не переносить observed frame counts в model recall. Сборщик объединяет все donor aliases/parents/sync groups в единый provenance registry **до** называния какого-либо набора lockbox. Это сборка уже полученных оснований, а не новый поисковый этап.

Для каждого W2 outcome сохранить: точный новый ответ, новые source/fact IDs, что фактически сделано (source read/full bytes/static parse/decode/visual review), что опровергнуто, права по слоям, связь с K-ID, remaining practical gate. Не требовать `closed` там, где результат только сузил scope. Small fixture, просмотренный исследователем, становится development. Ни один известный W1 fixture после tuning не становится вновь blind holdout.

## Что остаётся внешним gate после любой успешной W2

Эти ограничения уже корректно найдены W1. Их нужно передать в OPEN_QUESTIONS/эксперименты; ещё один web-search их не закроет.

1. **Реальный LinQ доступ и accepted host/device boundary.** Нужны конкретный device/SDK/runtime/compiler, input/output API, возможности ops/shapes/states, permitted CPU tracker/rules и artifact+input+job+raw-output provenance. Затем exact graph compile/run, reference parity, post-export quality и measured end-to-end latency/FPS/drops. ONNX, статический parser, CPU/RTX, remote request accepted и device visibility не являются LinQ inference PASS. Не изобретать SDK-команды. Передача → `linq_platform`, `model_stack`, `model_fidelity_quantization`, `video_architecture`.
2. **Permissioned target footage и независимая событийная GT.** Person pixels/joint visibility, phone/cigarette/strap observability, реальные цеховые confusers, motion/driver state, survey/envelope и policy. Внешние donors — development/transfer/stress evidence; staging/synthetic отдельно. Длинное неподвижное лежание нельзя получить looping/EOF. Не ставить опасный near-miss для сбора данных. Передача → `datasets`, `evaluation`, `training_strategy`.
3. **Семантика нарушения и reaction deadline.** Уточнить gait-run versus rapid movement/acceleration; время отсчёта нескольких секунд (physical onset/first visible/confirmation), допустимые class-specific hold/gap/clear/rearm; телефон при movement и equipment work; активный permit; protection requirement/handling procedure. Устное «1 FPS» не отменяет temporal misses. Deadline/acceptable miss/false-alert thresholds не выдумывать. Передача → `operator_product`, `hackathon_strategy`, `evaluation`.
4. **Неизмеряемые из одного ракурса отношения.** Correct hook/anchor closure, actual suspended-load footprint, off-plane distance/height, load mass/effort и consciousness требуют дополнительных физических наблюдений/процедур либо более узкого observable event name. Generic pose/box/video classifier сам по себе этого не исправляет. Передача → `camera_calibration_geometry`, `violation_methods`.
5. **Разрешения, которых в открытом grant нет.** Author request, исходные consent/media rights и намеренное публичное использование/redistribution нельзя «подтвердить» доступностью URL. Сохранить scope уже существующих grants и отдельный unknown; не посылать авторам/организаторам сообщения и не принимать соглашения за команду. Передача → owners приложения/данных.

В первые инженерные часы полезнее разрешить exact artifact/input contract и взять один permissioned target clip, чем начать несколько тяжёлых trainings. Затем causal replay с source PTS, lifecycle ledger, one-to-one actor/pair matching, all-known/observable recall+coverage, unmatched alerts на reviewed service/negative hours, timely recall и duplicates. Редкие/короткие события требуют phase/dropout tests; detector failure не может делать видимый GT-event «неeligible». Реальная ещё не наблюдённая production false-alarm rate остаётся неизвестной после любого public-donor успеха.

## Место для последующих исходов W2

На момент создания этого файла W2-исходов нет. Сборщик добавляет ниже датированный блок по K001–K007, не меняя исходные замечания выше.
