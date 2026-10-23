# W2-05 — Teacher admission: localization, retained coverage и малый audit

K005; исследователь второй волны, gpt-6.1-sol/medium, fresh context. Дата доступа к новым источникам: 2026-10-23; локальное время зафиксировано командой `Get-Date -Format o`: 2026-10-23T07:44:39+03:00 (Europe/Moscow), работа продолжена после этой отметки. Это время исследования, не дата публикации papers и не расписание кейса.

Прочитаны UTF-8 Context-prompt.md и prompt-training-strategy.md последовательными диапазонами с дочитыванием усечённых частей; PLAN, общий вывод/К005/внешние неизвестные CRITIC, общий блок и W2-05 из W2_TASKS; указанные F/E и источники W1-09, W1-08, W1-10-E01, W1-15-F06/F07. Новые действия: primary web search/open, GitHub metadata/raw HTTP, получение PDF в память и извлечение текста. Training, teacher inference, реальный annotation audit, подбор cutoff, calibration fit и проверка student/LinQ **не выполнялись**. Изменён только этот файл.

## Ответ и изменение решения

Полная ручная коррекция допускает teacher как помощника без требования сначала построить calibrator. Unchecked pseudo-label branch нуждается в отдельных доказательствах правильности принятых boxes **и** сохранённой полноты на всех GT, включая кадры без detections. Публичный calibration route найден, но он не закрывает missed-positive audit. При нулевой/малой независимой поддержке нужной страты нельзя выдать допуск по хорошей средней precision.

K005 **уточнён и закрыт в публичной/методической части**: установлен detection-specific смысл calibration, её предел по no-detection misses, проект sampling/denominator contract и правила отказа. Actual target support, numerical acceptance и полезность teacher остаются case/experiment неизвестными W2-05-Q01–Q03. Ни один класс этим исследованием не разрешён для unattended labels.

## Источники: что действительно получено

| ID | Первичный источник, версия/дата | Реальный доступ и локатор |
|---|---|---|
| W2-05-S01 | Küppers, Kronenberger, Shantia, Haselhoff, *Multivariate Confidence Calibration for Object Detection*, CVPR Workshops 2020. [arXiv metadata v1](https://arxiv.org/abs/2004.13546v1), 2020-04-28; [PDF](https://arxiv.org/pdf/2004.13546v1) | Metadata и PDF открыты; §3.1 Eq.1, §4 Eq.13–14, §5.1, Fig.3 прочитаны. Авторская [project page](https://trustinai.github.io/confcal/) открыта, по её Code link найден S02. CVF PDF вернул 403; ошибочно проверенный v2 вернул 404, metadata устанавливает только v1; успешно прочитана arXiv v1. F01/F02. |
| W2-05-S02 | EFS-OpenSource/calibration-framework (netcal), author-linked implementation. SHA `34b677f42b83803aa35503c5b6fefb1387ea9167`, commit date `2026-04-16T08:30:48Z`, установлен официальным GitHub commits API | [Pinned README](https://github.com/EFS-OpenSource/calibration-framework/blob/34b677f42b83803aa35503c5b6fefb1387ea9167/README.md), §Detection (Confidence of Objects); [ECE.py](https://github.com/EFS-OpenSource/calibration-framework/blob/34b677f42b83803aa35503c5b6fefb1387ea9167/netcal/metrics/confidence/ECE.py), `ECE.measure`; [Miscalibration.py](https://github.com/EFS-OpenSource/calibration-framework/blob/34b677f42b83803aa35503c5b6fefb1387ea9167/netcal/metrics/Miscalibration.py), `_prepare_input`, `_measure`. README и raw-файлы получены/нужные функции прочитаны, пакет не установлен/не запущен. Это современный pin, не доказательство exact code paper-2020. F03. |
| W2-05-S03 | Xu et al., *End-to-End Semi-Supervised Object Detection with Soft Teacher*, ICCV 2021, [PDF arXiv v3](https://arxiv.org/pdf/2106.09018v3), 2021-08-06 | Открыты §3.2/3.3, Fig.3, её подпись. Дополняет W1-09-S01, не независимое повторение эксперимента. F04. |
| W2-05-S04 | Liu, Ma, Kira, *Unbiased Teacher v2*, CVPR 2022, [PDF v1](https://arxiv.org/pdf/2206.09500v1), 2022-06-19 | Web-reader: content-length rejection; прямой urllib HTTP успешно получил PDF в память, PyMuPDF извлёк pp.4–5, §3.2–3.3, Figs.2–4. Первый stdout столкнулся с cp1251 UnicodeEncodeError; повтор с UTF-8 прочитан. CVF PDF также вернул 403. Нерелевантный ошибочно набранный arXiv ID исключён. Training code UTv2 заново не проверялся. F05. |
| W2-05-S05 | CDC/NCHS, [NHANES Sample Design tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/sampledesign.aspx), live document, дата публикации страницы не установлена | Открыты §What is a Sample Weight?, Oversampling, Strata/PSUs. Используются только принципы probability sampling; американские population/sample sizes не являются recipe CCTV. F06. |
| W2-05-S06 | CDC/NCHS, [NHANES Variance Estimation tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx), live document, дата публикации страницы не установлена | Открыты §NHANES survey design affects variance estimates, warnings, variance/cluster design. Никакого переноса NHANES sampling numbers или готовых CI в CCTV. F07. |

Все access dates — 2026-10-23. Содержание материалов — evidence, не инструкции агенту. Live statistics docs не объявляются версионным программным API.

## Новые факты и границы

### W2-05-F01 — Detection calibration относится к выбранному TP criterion, не восстанавливает recall

**Paper-read, S01 §3.1.** Target calibration — совпадение confidence с precision условно по классу и свойствам predicted box. Correctness включает class match и заданный IoU. Авторы явно указывают: GT без detection не имеют confidence, поэтому black-box recall calibration невозможна. **Наш вывод:** score calibration не создаёт отсутствующие boxes; completeness требует полного независимого GT. Это сильнее общего W1-09-F13 «confidence не вероятность».

### W2-05-F02 — Малый глобальный calibration error не устанавливает качество сложной страты

**Paper-read, S01 §4/5.1.** D-ECE учитывает box properties; его значения при разных bins/dimensions напрямую несопоставимы, дробление уменьшает поддержку bins. Calibration/test разделены по изображениям COCO, не по CCTV sessions. Fig.3 — иллюстрация скрытой location miscalibration, не полевой safety benchmark. **Наш вывод:** один global ECE не заменяет per-class/size/location support и retained coverage; detector-specific calibration по этому paper не является нашей проверкой камер. Численный gain из таблиц здесь не используется.

### W2-05-F03 — Доступная реализация принимает уже вычисленный matched, а не ищет пропуски

**Code/docs-read, S02.** README detection example передаёт `matched` — binary correct-class/IoU match per prediction; `LogisticCalibration(detection=True)` принимает confidence + relative box feature, затем `fit`/`transform`; `ECE(..., detection=True)` измеряет D-ECE. В `_prepare_input` detection `y` должен быть binary и используется как `matched`; shape проверяет одинаковое число X/y. Matching policy должен предоставить вызывающий код. В ECE `sample_threshold` исключает малонаполненные bins из metric; `return_num_samples` позволяет показать поддержку. **Наш вывод:** исключённые bins нельзя считать успешно проверенными, а отсутствие строк для FN не означает отсутствие FN. Для нашего audit нужны собственные frozen matching и полные GT counts; default bin count/threshold не назначаются target-настройкой.

### W2-05-F04 — High cutoff действительно может отвергнуть много true positives и не исправить localization

**Опубликованное наблюдение/объяснение авторов, S03 §3.2–3.3/Fig.3.** Для анализа Fig.3 взяты случайные 10k unlabeled training images COCO train2017, модель обучена на 10% labeled images, используемый default detector работы — Faster R-CNN R50-FPN. Высокий foreground threshold даёт высокую precision и низкий retained recall; authors показывают слабую связь foreground score с IoU и вводят отдельный box-jitter regression filter. Это диагностический анализ teacher candidates, не independent CCTV benchmark и не универсальный cutoff. Точный checkpoint-selection для фигуры не установлен. **Наш вывод:** plain folder pseudo-labeling с высоким cutoff не воспроизводит Soft Teacher: отвергнутые positives могут стать background без соответствующего loss treatment. Числа precision/recall рисунка намеренно не превращены в наши expected rates.

### W2-05-F05 — Состав detector score и assignment влияют на то, что отбирается

**Paper-read, S04 §3.2–3.3.** UTv2 на FCOS разбирает centerness×classification score: высокий product может быть обусловлен ненадёжной centerness при ограниченных labels. Confidence threshold также не определяет надёжность каждой из четырёх regression boundaries; noisy box сдвигает assignment. Listen2Student вводит дополнительную uncertainty branch и сравнение teacher/student. **Наш вывод:** score semantics надо читать у выбранного teacher, а не переносить численный cutoff с Faster R-CNN на FCOS/YOLO/VLM. Новый head/calibrator не требуется для fully reviewed assistance. Здесь не предлагается портировать UTv2: evidence ограничивает универсальный scalar gate, numeric table gains не используются.

### W2-05-F06 — Oversampling требует сохранять вероятности отбора

**Первичная статистическая документация, S05.** Неравные вероятности отбора и deliberate oversampling меняют состав sample; population estimate требует sampling weights, design metadata и определённой population. **Наш проект применения:** отделить probability component от purposive diagnostics и применять явные веса только к известному probability design. У targeted находок с неизвестной inclusion probability нет корректного population weight, восстановимого одним делением на число boxes. См. W2-05-E01.

### W2-05-F07 — Больше boxes одной сцены не означает больше независимой поддержки

**Первичная статистическая документация, S06.** Внутрикластерная корреляция и differential weighting влияют на variance; simple-random/iid расчёт может занижать standard errors. **Наш вывод для teacher admission:** количество independent camera/session/episode groups надо показывать рядом с instance counts; bootstrap всех boxes без group design не обоснован. Выбор уровня resampling зависит от claim, см. E01. Документ не даёт универсальной нижней границы количества CCTV scenes.

## W2-05-E01 — Дополнение W1-09-E01: sampling, localization, retained coverage и claims

Это **будущая предлагаемая процедура, не исполненный эксперимент**, расширяющая существующий E01, а не дополнительный обязательный training trial. Использовать также W1-10-E01 для стоимости assistance и W1-09-E02 для последующей student-проверки.

**Решение.** Для каждого canonical class×доступной condition-stratum выбрать: fully reviewed assistance; manual annotation/route-to-review; либо ограниченный unchecked pseudo-label candidate trial. Внешнее numerical acceptance, допустимые regressions/ошибки и уровень неопределённости задаются требованиями кейса до выбора cutoff; сейчас они неизвестны. Safety admission без этих входов не установлен.

**Входы и зафиксированный контракт.** Нужны teacher family/version/config/checkpoint hash, prompt/phrase→class table для VLM, box coordinates, preprocessing, score composition, raw output floor/caps, NMS/order; доступный разрешённый train-domain pool с source hashes/camera/session/time/episode IDs; полная annotation guideline по visibility/ignore и in-scope classes; независимые calibration и confirmation groups. Student/loss interface от model_stack нужен до unchecked branch: что делает с отсутствующим box/непокрытым классом/empty annotation. GroundingDINO substring mapping W1-10-F15 не считается ontology resolver.

### 1. Сначала определить estimand и две части отбора

Population здесь — конкретный зафиксированный разрешённый pool/период/набор камер, а не все российские заводы или будущие камеры. Выбрать единицу: например, complete sampled frames с объектными counts внутри; либо episode-coverage с собственным определением. Frame-object recall не переименовывать в event recall. Уточнить macro-average по cameras/groups либо object-weighted metric: это разные denominators.

**P, probability component:** seeded random sample групп из полного sampling frame; полный просмотр выбранных кадров, включая teacher-empty. Если cameras — фиксированные страты, случайно выбирать sessions/episodes внутри каждой; если claim о новых cameras, нужны отдельные cameras и их sampling/holdout contract. При subset кадров внутри группы сохранить conditional frame inclusion probability и правило выбора, а не брать только moments с teacher hits. Counts и footage exposure берутся из sampling frame, не из числа предсказанных boxes.

**D, diagnostics component:** дополнительно взять rare-predicted, small/occluded, low/high-score errors, disagreement, output-empty, известные human-found positives. Membership назначается по наблюдаемым до полного GT признакам; «predicted rare» не значит «истинный rare». Сохранять причину/инструмент поиска, стоимость, overlaps, group IDs. Small/GT-rare страты становятся известны после полного annotation: допустимо анализировать их в P; post-hoc отбор богатых ими кадров в D не делает D случайным sample.

По умолчанию P и D репортить раздельно. Если D имеет заранее определённую probability sampling схему с известными frame sizes и probabilities, допустим единый design estimator с учётом пересечений. Нельзя просто слить две таблицы и усреднить precision. Если один frame выбран несколькими путями, deduplicate и учитывать его union inclusion probability; формула `1-(1-pP)(1-pD)` допустима только при реально независимых механизмах отбора. При неизвестном механизме сохранить P как estimator, D — diagnostics.

### 2. Весовой расчёт — предлагаемый estimator contract, не проверенная библиотечная команда

Для каждого sampled frame i сохранить полную inclusion probability `pi_i>0`, включая group и conditional within-group stages; `w_i=1/pi_i`. При исчерпывающем просмотре sampled frames и frozen matching вычислить для каждого класса/cutoff `TP_i`, `FP_i`, `FN_i`, `GT_i`, `A_i=TP_i+FP_i`. Предлагаемые weighted ratios:

`precision_hat = sum(w_i*TP_i) / sum(w_i*A_i)`;

`retained_recall_hat = sum(w_i*TP_i) / sum(w_i*GT_i)`.

Суммы inverse-probability weighted counts оценивают totals известной finite population при корректном design. Ratio estimates не объявлять точно unbiased finite-sample оценками; variance должна учитывать actual stratification/clustering. При равновероятном frame sample веса сокращаются; при равновероятном **group** sample с разным числом просмотренных кадров это нельзя предполагать без проверки второго этапа. Object-weighted recall использует GT-object denominator; среднее recalls групп оценивает другую величину. Для rates знаменатель — просмотренная/взвешенная exposure, не detections.

Если pi неизвестны для D, допустим только conditional-on-selected-slice отчёт counts и ошибок. Если sampling frame неполон/часть условий имеет pi=0, population claim ограничить покрытой частью, missing strata назвать. Число boxes в страте не заменяет inclusion probability. Не вычислять weighted D-ECE штатным netcal без проверки поддержки weights: S02 выше доказывает prediction-level интерфейс, не наш complex survey estimator.

### 3. Blind complete GT и одинаковое сопоставление

Разметчик на контрольной части сначала ищет **все** in-scope objects без teacher overlays, затем независимое adjudication; сохраняются uncertain/ignore и причины. Полный обзор teacher-empty frame обязателен. Для assistance отдельно проверять omissions после correction: подтверждение предложенных boxes не равно full review. Держать одинаковые geometry/NMS/caps/class map и matching для всех cutoff. Сохранить candidate outputs до admission cutoff; если detector уже отсёк outputs своим floor/cap/NMS, явно указать, что анализ не восстанавливает потерянные candidates.

TP — one-to-one correct class + заранее объявленный IoU criterion; duplicates — FP по frozen policy. Отдельный localization diagnostic на class-compatible сопоставлениях: IoU distribution, плохие границы/центры, borderline cases; правила такого matching объявить отдельно, не считать его relaxed matches за TP основного gate. Для каждого cutoff показать принятые/отвергнутые predictions, TP/FP, полное GT/FN; разделить GT, потерянные admission cutoff, и GT без usable исходного detection. При изменении cutoff переагрегировать matching по объявленному score order. «Доля оставленных predictions» `accepted/candidates` не называется recall: retained recall имеет denominator всех GT, в том числе не найденных вовсе.

### 4. Calibration diagnostic и независимое подтверждение cutoff

На calibration groups можно сравнить class-wise precision/retained-recall curves и, если support позволяет, reliability bins при фиксированном class+IoU target. Показать class/size/position/camera support каждого bin, excluded bins, raw counts, число positive groups; не сравнивать D-ECE с разным binning как улучшение. Не вводить новый calibrator, если простого cutoff/review policy достаточно для решения. Если calibrator обучается, отдельно сохранить fit data/parameters и проверить, что score reordering/NMS/order действительно часть frozen policy.

Выбранные на этих данных cutoff, bins, feature set и calibrator — selection. Их значения на той же выборке описательны, не независимое подтверждение. Заморозить policy и один раз применить к отдельным complete-GT confirmation groups, с собственным P/D design. Если confirmation использована для новой правки policy, она стала development: следующий independent claim требует новых нетронутых групп либо явного статуса reused evidence. Final student lockbox W1-09-E02 не расходовать на повторный teacher tuning; audit data после помещения в train теряют независимый статус.

### 5. Support и неопределённость: условия отказа

Для instance metrics кластером служит независимая единица отбора/переноса: episode/session при fixed cameras, camera при соответствующем camera-generalization claim. Несколько sessions одной камеры не превращаются в несколько независимых cameras. Сохранять оба уровня; тысячи boxes одного человека/смены не считаются тысячами независимых испытаний. CI/resampling design выбирается по реальному sampling plan; при достаточной поддержке пересчитывать weighted numerator/denominator по resampled independent groups с сохранением обеих compared policies. Простой iid binomial CI по boxes и обычный frame bootstrap не применять автоматически. Bootstrap observed groups также не обнаруживает отсутствующий в них failure mode.

| Наблюдение | Допустимый отчёт | Недопустимый допуск / следующий шаг |
|---|---|---|
| `GT_c=0` в independent confirmation | Recall/coverage класса N/A, positive support 0; observed FP возможны | Не «100% recall», не «0 misses доказано». Полный review/независимый целевой positive collection |
| Accepted predictions класса 0, `GT_c>0` | Precision N/A; retained recall 0 и реальные FN при объявленном matching | Не считать undefined precision идеальной. Unchecked branch не закрывает этот класс |
| Accepted predictions 0 и GT 0 | Обе метрики N/A, явная пустая support cell | Не auto-accept по отсутствию ошибок |
| Есть немного positives, почти все из одной группы | Counts/наблюдаемая point estimate и происхождение, uncertainty «не установлена», если design не поддерживает расчёт | Не переносить на новый camera/condition; искать новые independent groups, не соседние frames |
| Все observed successes либо failures, degenerate bootstrap/NaN | Raw TP/FP/FN, group counts, interval unavailable/неинформативен | Не интервал нулевой ширины как доказательство. Обоснованный иной estimator только с его design assumptions |
| D rare/empty/high-score диагностическая выборка, pi неизвестны | Selected-slice failure descriptions и counts | Не population precision/prevalence; остановить общий claim или использовать только P |
| На P редкий класс отсутствует, на D positives есть | P не оценивает recall класса; D подтверждает наличие failure/success на выбранных примерах | Не переносить conditional D recall на population и не вычислять частоту класса по D |
| Сводная precision высокая, critical slice имеет misses/плохой IoU | Сводка плюс отдельный запрет/неустановленный gate страты | Не скрывать отказ macro/pooled average; review этой страты |

Универсальные sample size, число bins, precision floor и минимальное количество групп не заданы. Нужный объём зависит от accept/reject margins, распределения ошибок/класса, design и independent support; это Q01/Q02. Если доступный support не разрешает требуемый claim, результат — **insufficient evidence**, а не принятие при нулевой наблюдённой ошибке. Даже валидный интервал не исправляет blind-spot неполного GT.

### 6. Ветви допуска и границы claims

| Ветка | Evidence gate до использования | Что можно заявить при успехе | Stop / предел |
|---|---|---|---|
| Fully reviewed assistance | Полный обзор каждого selected frame, исправление missing/wrong boxes/classes и ontology/geometry QA; controlled cost pilot против manual с одинаковой полнотой | Teacher помог получить reviewed labels; измеренная экономия полных human minutes на заявленных groups | Если omissions/anchoring bias или cost хуже manual — отключить подсказки для страты. Audit предсказаний не заменяет review каждого используемого кадра |
| Unchecked labels / отдельный SSL trial | Frozen policy, independent complete-GT confirmation с precision **и** retained coverage/localization/critical slices, достаточный design support по согласованным acceptance; runnable loss/ignore contract для dropped positives | Ограниченный кандидат на noisy-label training по конкретной frozen policy; происхождение остаётся pseudo | Неподдержанный critical class, unknown support или loader воспринимает omissions как negatives без обоснованной обработки — не auto-accept. Даже хороший audit не доказывает student gain/безопасность deployment |
| Manual route-to-review | Полные annotation instructions и independent QA, прогнозы могут только ранжировать очередь | Получены ручные labels/диагностированы ошибки без заявления качества unchecked teacher labels | Selector не должен исключить все no-detection frames. Расход поиска и review входит в human budget |

**Контроль стоимости:** помощь teacher против ручной разметки сравнивать при одинаковом определении «полностью готово», на сопоставимых/случайно назначенных группах и с учётом аннотатора/порядка работы. Одни и те же изображения последовательно одним человеком создают memory bias; не выдавать такое сравнение за слепой cost trial. Считать selection, drawing/correction, omissions search, review/adjudication/export QA; не только accept clicks. Экономия времени не подразумевает хороший unchecked branch.

**Артефакты:** frozen sampling frame/population/estimand, P/D manifests, probabilities/weights/overlaps и страты, source/group/frame hashes; teacher/checkpoint/config/prompt/class-map/score/NMS/cap versions; raw predictions, cutoff candidates и frozen choice; blind/adjudicated GT с provenance; per-group/class/size таблицы accepted/TP/FP/FN/GT/IoU/exposure и support/bin exclusions; calibration vs confirmation статус; human time/correction log; решение на каждую unsupported stratum, rollback policy. Derived labels не смешивать с human-reviewed labels без provenance.

**Исходы/stop:** assistance экономит полные минуты при сохранённой QA → W1-09-E02 B/C comparison; teacher пригоден только искать примеры → manual queue; unchecked candidate проходит согласованный gate → отдельная noisy-label D-arm с baseline, не подмешивание в fully corrected B; support/semantics/geometry/loss invalid → стоп этой ветки и ручная коррекция/уточнение. Новый teacher checkpoint/prompt/NMS/условия потока требуют пересмотра applicability, не молчаливого переноса gate. Успешный аудит характеризует frozen policy на объявленном материале, не универсальный safety threshold, student/event quality или исполнение LinQ.

## Маршрут и оставшиеся вопросы

| Уровень | Статус |
|---|---|
| Detection-specific calibration/selection paper | S01/S03/S04 прочитаны в нужных разделах; найдено прямое ограничение по recall/no-score и localization |
| Available implementation | S02 существует и pinned; интерфейс/нужные code sections прочитаны, не запускались |
| Candidate audit contract | W2-05-E01 proposed; требует actual outputs/GT/design/acceptance, не runnable experiment artifact |
| Target benefit/admission | Не установлен; нет target audit, cost pilot, выбранного teacher или numerical acceptance |

| Q-ID, приоритет, тип | Что неизвестно; что меняется; чем закрывается |
|---|---|
| W2-05-Q01, P0, case/data | Какие mandatory classes/visibility/ignore, critical conditions и допустимые precision/coverage/localization losses? Публичные papers не задают safety acceptance; полный кейс + annotation guideline + baseline устанавливают gate до cutoff tuning. Связь K005/F01/F04/E01 |
| W2-05-Q02, P0, data/experiment | Сколько independent positive groups и какая population/camera support реально доступны для calibration/confirmation? До получения pool неизвестны sampling probabilities, precision uncertainty и возможность independent claim. Inventory + blind complete E01; при нехватке — review, не численная фикция |
| W2-05-Q03, P1, artifact/experiment | Конкретный teacher/checkpoint, его floor/caps/NMS/score semantics и cost полного исправления? Проверить outputs/overlays и randomized cost pilot E01; устанавливает, полезнее assistance, manual либо отдельный unchecked trial. Published calibration recipe не выбирает teacher |
| W2-05-Q04, P0 до unchecked trial, implementation | Как chosen student criterion обрабатывает omitted positives/unknown classes/empty outputs? Нужен actual loader/assigner/loss trace из model_stack/W2-02, либо full corrected labels. Хорошая precision accepted boxes не закрывает negative supervision |

**Передачи.** → datasets: probability frame, inclusion metadata, blind completeness и independent positive support; target rare labels искать также вне predictions. → evaluation: выбрать estimand, matching/IoU и design-compatible uncertainty для frozen teacher admission, без нового общего evaluation research. → model_stack: S02 не делает matching/FN и не доказывает weighted survey support; проверить actual teacher score/floor/caps и Q04. → violation_methods: object/state/event ontology и наблюдаемость остаются отдельными. → очередь W2-12: E01 выбирает одну ветку, calibrator и unchecked SSL не обязательны; полностью reviewed assistance может идти без нового calibration fit. → автор/сборщик: сохранить N/A и selected-slice статус, не превратить «public protocol closed» в «teacher accepted».
