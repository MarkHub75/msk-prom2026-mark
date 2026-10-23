# W2-D — минимальный data package и causal acceptance corpus

Дата исследования: **2026-10-23**, проверенные часы хоста при фиксации наблюдений: **20:40:59 +03:00**. Интернет-страницы действительно открыты, малый CSV получен, HEAD двух MP4 выполнен. Видео, weights и большие архивы в этой ветке не скачивались; обучение, экспорт, model replay, LinQ и тесты FSM не запускались. `W2_D_MATERIALS/` содержит только собственные малые свидетельства. Ниже отделены новые наблюдения, выводы и предлагаемые проверки.

## Решение и изменение ближайшего шага

**W2-D-F01 [решение].** При отсутствии инвентаризации видео команды стартовать с одного условного scope: **наблюдаемое лежачее состояние человека в фиксированном ракурсе, одно уведомление на продолжающийся эпизод**. Не обещать «падение», «неподвижность» или «потерю сознания» по одной лежачей позе. Первое исследование — pretrained frontend + причинная логика, без нового обучения. Для разрешённого некоммерческого академического feasibility есть конкретная пара URFD `fall-01-cam0.mp4` / `adl-01-cam0.mp4`, однако её содержимое и event labels ещё надо проверить. При непринятом NC-режиме этот маршрут не объявлять разрешённым: переключить первый scope на **вход/нахождение человека в пользовательском полигоне** только после получения разрешённого видео команды. Геометрический полигон — операционное правило, не доказательство физической опасности.

**W2-D-F02 [новый ограничивающий факт].** CAUCAFall v5 имеет полезные fall/no-fall segmentation labels и CC BY 4.0, но авторы прямо описывают **motion-triggered DVR recording**. Следовательно, даже все его клипы вместе не являются непрерывной записью рабочего фона. Нельзя восстановить negative camera-hours из количества PNG или заявленной частоты камеры. Конкретный AVI не получен: web-страница открывается, Python/API получает 403. Это резерв для размеченных состояний/объектов, а не готовый production event benchmark. [S02]

**W2-D-F03 [новое наблюдение].** У точного URFD `fall-01-data.csv` получено 160 строк: номера 1…160, время 0…5305 ms, соседние разности 33/34 ms. Это **5.305 s между первым и последним timestamp**, не измеренная длительность падения или лежания, не FPS видеодекодера. Длинную выдержку вроде 10 s этот временной ряд уже не поддерживает; для короткой выдержки нужно отдельно проверить наблюдаемый post-state и EOF. CSV не даёт права заменять PTS MP4 равномерной сеткой: связность двух представлений ещё не проверена. [S01, S03]

**Что меняется:** training queue пока не получает новый разрешённый и полностью размеченный object package. Зато ближайшая работа становится конкретной: принять use scope; получить/просмотреть одну точную пару; создать frame-to-time mapping и несколько event labels; реализовать таблицу ниже на oracle observations; затем проверить frontend. Не ждать сотен событий для feasibility и не считать эту пару независимым подтверждением качества.

## Происхождение исходного замечания и статус K

Исходная критика сохранена в `CRITIC.md`, контроль 2026-10-23 20:25:26 Moscow, разделы K005/K006/K007/K011; история первой волны не переписана. Прочитаны назначенный `PROMPT_W2_D.md`, релевантные контракты `W1_01/04/07/09/11.md`, `CASE_NOTES.md`. Secondary leads: соседний behavioral `_WORK/W1-09.md` (URFD, CAUCAFall, точные границы доступа и различие lying/fall) и datasets `_WORK/W2-08.md`; они используются как указатели, а не как новые собственные измерения. Проверены только **два primary data sources**, URFD и CAUCAFall; полный каталог не повторялся.

| K и исходная проблема | Статус этой ветки | Что закрыто / что осталось |
|---|---|---|
| K005: нет выбранного реально доступного data package | **Применимость уточнена; prerequisite остаётся открытым** | Есть exact obtainable URFD pair + timing CSV и конкретная CAUCAFall граница. Нет подтверждённых rights выбранного use, decoded mapping, event labels и private/team inventory. Training-ready package не заявлен |
| K006: SELECT/CAL/TUNE/CHECK имеют разные роли | **Предложен единый минимальный контракт; принятие сборщиком открыто** | train/DEV/lockbox; optional SELECT только для заранее frozen pipelines. В нынешней паре нет достаточного lineage для независимых частей, значит только DEV feasibility |
| K007: нет короткого causal acceptance входа | **Спецификация закрыта; исполнение открыто** | Ниже 10 изолированных fixtures, единицы времени, ожидаемые counts, phase replay. Ни fixture runner, ни реальные episode labels ещё не созданы |
| K011: нет узкого маршрута при незакрытых gates | **Data-часть уточнена; общий маршрут открыт у сборщика** | A: pretrained/rules; B: fine-tune только после labels/runtime; C: challenger deferred. Owners/cutoff/reserve не выдуманы |

## Два проверенных источника: что именно доступно

**W2-D-S01.** Michal Kępski / University of Rzeszow, [UR Fall Detection Dataset](https://fenix.ur.edu.pl/~mkepski/ds/uf.html). Версия страницы не указана; связанная авторская статья Kwolek/Kępski — December 2014. Доступ 2026-10-23. Локаторы: вводное описание, synchronization paragraph, license, Fall row 01, ADL row 01, Extracted features. Вид: primary dataset documentation. Коротко: 30 fall/40 ADL sequences; два вида fall и один ADL; отдельные PNG streams; время в ms от начала sequence, независимые камеры сведены ближайшими timestamps. Разметка posture в depth-derived features имеет отдельные лежит/не лежит/переход. Это не RGB bbox/track/онлайн-event GT. Условия: CC BY-NC-SA 4.0, academic/noncommercial scope; commercial use требует отдельного согласования с авторами, контактов не было. Сохранён оригинальный HTML, SHA256 `cb6d171be52c086ece579457b9ee752abb25e335b12aae25ee28714fb94aae83`. Обобщение на industrial камеры и разрешение конкретного конкурсного режима не установлены.

**W2-D-S02.** Jose Camilo Eraso, Elena Muñoz, Mariela Muñoz, Jesus Pinto, [Dataset CAUCAFall v5](https://data.mendeley.com/datasets/7w7fccy7ky/5), DOI **10.17632/7w7fccy7ky.5**, опубликован **18 March 2025**. Доступ 2026-10-23. Локаторы: Description paragraphs 2–4; Steps to reproduce paragraphs 1–2; Licence. Вид: versioned primary dataset card. Коротко: subject/activity folders, AVI/PNG/TXT, manually labeled fall/no-fall segmentation; CC BY 4.0. Камера nominal 23 FPS, 1080×960; это описание capture, не проверка каждого AVI. DVR начинает motion-triggered запись при входе. Камера/incident/session lineage, event onset/observable и negative exposure ещё требуют просмотра/manifest. Синхронного primary file list/конкретного видео не получили. Web open успешен; независимый `urllib` page/API 403, отражено в `fetch.json`. Наличие repository card не приравнено к скачанному архиву.

**W2-D-S03.** URFD, [fall-01-data.csv](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-data.csv), малый первичный synchronization artifact, revision отсутствует. Доступ 2026-10-23; HTTP 200, 2466 bytes; SHA256 **60e156223725e401155b4fd25a672c498ed5b4e17897337c6971d90041818bcc**. Локатор: все 160 строк, столбцы frame/time/accelerometer, смысл по S01. Собственная read-only проверка CSV, без медиадекодирования. Сохранён `urfd_fall01.csv`; вычисленные границы в `observations.json`. Acceleration не подаётся как RGB-признак и не считается event label.

**W2-D-S04.** Exact URFD asset metadata: [fall-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4) и [adl-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4). Собственный HEAD 2026-10-23: оба 200 `video/mp4`, Content-Length соответственно **1,299,104 / 1,194,846 bytes**, Last-Modified 2020-02-25 17:13:37 / 17:13:38 GMT. Header metadata сохранено, full-byte SHA и decode отсутствуют. Дата mtime файла — не дата записи инцидента. MP4 являются удобными кандидатами; original PNG+CSV предпочтительны, если MP4 не сохраняет соответствие исходному времени. У всех производных одной sequence один parent incident group.

## Label/readiness/missing matrix

**W2-D-F04 [синтез].** Разделить два пакета. Object fine-tune требует exhaustive labels именно выбранных train classes и ignore policy. Event evaluation требует непрерывного времени, event identity, observability, negatives и дедлайна. Один пакет не возникает автоматически из другого.

| Сценарий / asset | Object fine-tune input | Event evaluation input | Готовность / минимально недостающее |
|---|---|---|---|
| **Приоритет: лежачее состояние**, URFD exact pair S04 | RGB есть по указателю, person/lying bbox или pose GT не подтверждены; depth features не substitute | Synchronization CSV подтверждён только fall-01; ADL candidate есть. Onset/observable/end/ID/negative intervals отсутствуют | **Obtaining/reannotation required**; принять NC use, получить exact pair, декодировать и проверить mapping; вручную описать состояние, negative и censoring. Только feasibility |
| Fall transition, те же assets | Object bbox не задаёт переход | Sequence fall class не локализует onset и не доказывает distinguishability до deadline | Не стартовый claim; потребуется переходная разметка и matched intentional lying/bending controls. Нельзя переименовать lying alert в fall detection |
| Fall/lying, CAUCAFall v5 | Существуют per-frame segmentation fall/no-fall по card; для person bbox нужен проверенный конвертер и полнота; исходная семантика fall может смешивать переход/позу | Есть action AVI по card; точных доступных файлов и PTS не получили. ADL task clips не равны background camera-hours | **Reserve**, exact acquisition/rights notice/annotation manual/границы ещё missing; nominal FPS не использовать как проверенный timebase |
| **Зона / длительное нахождение**, разрешённый team video | Pretrained person detector может дать первый inference без fine-tune; train labels нужны только после error audit | Нужен реальный static-camera clip с entry/stay/exit, inside/outside controls, затем второй actor | **Team asset unknown**. Ни выбранные public clips, ни case p8 не подтверждают наличие команды. Если есть файл — меньше specialist dependencies, допустим fallback priority |
| Долгая неподвижность / unconsciousness | Лежачие labels недостаточны | Нужны fresh input, видимое motion/unknown и реальная длительность нужного hold; сознание часто не видно | **Out of first scope**; нельзя расширять клип повторением последнего кадра |

Полей private data не заполняли догадкой. Для владельца данных нужны ответы: exact files и права использования; камера/сессия/исходный parent; положительные и полные обычные интервалы; timestamp/FPS/provenance; известные trims и перезаписи; exhaustive label coverage. При недоступности ответов статус остаётся `unknown`, не «достаточно negatives».

## Минимальный реальный development corpus и ручная работа

**W2-D-F05 [предлагаемый пакет D0].** Не квота для статистической достаточности. Сначала достаточно собрать **один видимый positive эпизод + один контрастный negative**, затем добавить **один episode с окончанием/повторным входом и один с двумя людьми**, если доступные/разрешённые файлы это содержат. Отсутствующий case честно остаётся synthetic-only coverage. Для лежачего scope первый exact positive candidate S04 и его ADL pair ещё должны пройти review; ADL-01 не объявлен заранее hard negative «намеренно лёг». Если он не контрастен, не подменять его содержимое названием файла, выбрать другой ADL после просмотра.

Не требовать всех четырёх реальных эпизодов до первого frontend feasibility. Но первая пара проверяет лишь работоспособность пути, а не rearm/identity, quality или factory FP rate. Ни длительность доступных negative intervals, ни число независимых subjects/камер в выбранной паре пока не установлены. Независимость между fall-01/adl-01 также не предполагается.

Минимальная инструкция annotator:

1. Сохранить original bytes/hash/source/license; для каждого кадра index, original timestamp/timebase и decoded PTS. Для PNG использовать documented CSV mapping только после сверки номера/пропусков. `timestamp_origin` отличает camera/sync metadata от derived CFR. Не считать MP4 PTS временем физической экспозиции без основания.
2. Просмотреть исходный эпизод целиком. Разметить `actor_gt_id`, интервал наблюдаемой лежачей позы, `onset_bounds`, `first_observable`, `end_bounds`, `unknown/occluded`, left/right censor. Для зоны — polygon/rule version и anchor convention. При неоднозначности сохранить interval/ignore, не заставлять annotator угадывать причину.
3. Все рассматриваемые интервалы пометить `positive / verified_negative / unknown / out_of_scope`; сохранить полноту review `(class,interval,ROI)`. Проверить всех людей в ROI, а не только найденного моделью. Negative clip допустим только для этого observable scope, не для всех нарушений.
4. Для first frontend run bbox/pose dense GT необязателен: event annotations и несколько hand-reviewed failure frames достаточны для diagnosis. Для fine-tune отдельно полностью разметить выбранные train frames/instances и все обучаемые классы. Не писать пустые label files на partial data.
5. Второй человек проверяет границы и спорные labels; разногласия решаются до сравнения. Записать reviewer/version; не строить GT из output оцениваемой модели. Все crops/windows/sampling variants наследуют parent split.

Минимальный manifest: `asset_id, source_url, original_hash, rights_status, parent_incident, camera, session, subject_if_known, lineage_confidence, split_role, native_time_kind, timebase, pts_mapping_status, label_version, exhaustive_scope, eligible_negative_intervals, unknown_intervals`. Поля unknown разрешены, но ограничивают claims. Для события: `gt_event_id, scenario, actor_gt_id, onset_lo/hi, observable, end_lo/hi, censor_reason`. Для production timestamp bounds отдельная передача runtime-ветке.

## Один протокол data roles вместо семи обязательных subsets

**W2-D-F06 [согласование K006].** Основной вариант **train / DEV / lockbox** по lineage. CAL/TUNE/CHECK не создавать как обязательные физические части на нынешней паре. Если выполняется только pretrained feasibility, train пуст и оба clips имеют роль DEV; независимого lockbox результата пока нет.

| Решение | Допустимая роль | Лимит/варианты на старте | Статус после просмотра |
|---|---|---|---|
| Ручная семантика/ошибки, threshold, dwell/gap, model/checkpoint choice | DEV | Один incumbent; одна заранее описанная policy alternative после найденной ошибки | Development, результаты exploratory; все просмотры/изменения в ledger |
| Fine-tune weights | Train, validation внутри DEV | Только один B0 после data/runtime gate; ablations решает сборщик | Labels и gradients никогда из lockbox; смена recipe — новый artifact |
| Calibration | DEV либо отдельные grouped DEV folds при достаточных группах | В первом scope отсутствует | Fitted data не становятся independent CHECK |
| Выбор законченного pipeline | Optional SELECT, только при оставшихся независимых группах | ≤2 готовых frozen pipelines, без настройки по результатам | После просмотра selection data. Если меняются threshold/rules — tuning data |
| Независимая оценка | Lockbox после freeze одного artifact | Один frozen pipeline, одна planned evaluation | После использования для исправлений это новый DEV; нужны новые группы для новой независимой проверки |
| Refit train+DEV | Только после отдельного решения | Не назначен на старте | Новая identity; прежний test не подтверждает автоматически новый artifact |

Внешнее разрешение pretraining exposure проверить по weight provenance соседней ветки. Камера не становится unseen из-за другого номера клипа. URFD cam0/cam1 одного падения всегда одна incident group; возможный общий actor/scene между fall и ADL исключает сильное unseen-scene заявление. CAUCAFall subject folders — полезный уровень, но десять subjects не означают десять независимых камер. Пока grouping не установлен — не делить кадры случайно. «Мало групп» ведёт к DEV feasibility, а не к четырём псевдонезависимым частям.

## Малый synthetic event-ledger acceptance corpus

**W2-D-F07 [спецификация, не выполненный тест].** Fixtures проверяют evaluator и FSM, **не detector quality**. Единицы — секунды source timeline с отдельной `available_at` replay timeline. Все числа ниже искусственные test constants, не промышленные dwell/deadline. Для простоты known identity A/B и один camera epoch; правила и ожидаемые результаты одинаковы для lying-state и zone-state через абстрактный `positive` input.

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

## Replay на реальном времени и различающий эксперимент

**W2-D-E01 — вопрос:** поддерживает ли выбранный видимый lying-state и причинное подтверждение нужную своевременность на доступных коротких real episodes, или наблюдения/выдержка делают scope неработоспособным ещё до обучения?

Входы: принятые rights выбранной exact pair, полностью decoded frame/PTS mapping, ручные episode labels, pretrained frontend разрешённого deployment bundle, один fixed immediate baseline и одна FSM policy. На начальном oracle этапе frontend не нужен; LinQ нужен позже для deadline, не для проверки matcher.

1. Пройти synthetic logic acceptance. Затем проиграть **oracle real observations** на исходной frame/time grid, используя только префикс. Проверить, есть ли физически наблюдаемый support до EOF/deadline. При отсутствии нужной длительности не тюнить «лучший hold» на обрезанном файле: укоротить заявленный scope или получить продолжение/другой episode.
2. Зафиксировать sampler period `Δ` как экспериментальный параметр, а не universal min FPS. Для каждого интересующего Δ использовать несколько равномерных фаз `φ∈[0,Δ)`; выбрать первый доступный исходный кадр с timestamp ≥ `φ+kΔ`, не дорисовывать кадры. Для коротких событий дополнительно включить фазы сразу по обе стороны onset/end. Дедуплировать повторно выбранный frame ID. Все phase variants одной sequence — один statistical group.
3. Выполнить causal replay frozen frontend observations: native grid против subsampling; immediate policy против FSM. Логировать число **различных свежих** observations до deadline, timing support, observable/censored events, phase-specific misses, late/duplicate alerts и eligible negative seconds. При oracle успехе, но frontend провале — диагноз модели; при обоих провалах — семантика/schedule/hold, fine-tune не первый ответ.
4. После DEV freeze — отдельный **wall-clock LinQ run** с тем же decode/scheduling/delivery, traces `source_pts, available_at, inference_end, decision, emit, receive`. Cached replay не доказывает deadline. Метрики actual throughput/capture delay не подставлять из nominal source FPS. При отсутствии capture mapping назвать задержку replay-to-receipt, а не glass-to-alert.

Метрики: поэпизодные timely/late/missed/censored counts; duplicates и wrong-actor; per-phase sensitivity; fresh observations к deadline; unknown/stale intervals; реальные negative seconds. На этой малой curated pair FP/hour — лишь описательная частота на известных reviewed интервалах, **не factory rate**; если таких интервалов ещё нет, rate `N/A`. Не публиковать p95 по нескольким событиям как устойчивый tail estimate. Native timestamps и duration distribution реальных нарушений, кроме исследованного metadata span, пока unknown.

Артефакты: hash exact media/labels/manifest, mapping table, phase schedules, oracle/frontend observation caches с provenance, full GT/alert ledgers, trial/view ledger, paired diagnostic report, LinQ trace отдельно. Результат успеха — исполнимость конкретного causal пути на этих эпизодах. Он не доказывает detector accuracy в цехе, unseen camera generalization, fall cause, сознание, private deployment prevalence или LinQ performance иной конфигурации.

## Узкий маршрут, stops и передачи

**W2-D-F08 [предлагаемый data route для K011].** A: права/asset check → labels/time mapping → oracle acceptance → pretrained real replay → LinQ run → freeze. Это может завершиться demo feasibility без обучения. B: только если frontend errors подтверждены человеком, есть exhaustive train labels с независимым DEV, выбран совместимый stack и пройдены runtime gates, разрешить один fine-tune. C: challenger, второй specialist, calibration, расширение сценариев и вторая GPU остаются deferred до готового A/B и реально измеренного резерва. Эта ветка не разрешает аренду и не оценивает часы.

Stop rules: нет разрешённого media — продолжать synthetic logic и private inventory, не заменять реальный результат; нет timestamp mapping — event-time claims отложить; нет independent groups — feasibility/DEV claim; нет continuous negatives — industrial FP/hour не заявлять; нет LinQ inference/speed — не считать case requirement закрытым. Если короткое lying-state не различимо от intentional lying, сохранить observable state label или сузить scope, а не автоматически брать более крупный detector. Новые hypotheses прекращаются при общем cutoff сборщика; обязательные LinQ/submission reserves не съедаются optional data search.

Точные handoffs:

- **Сборщику/root:** принять один первый scope и role table; назначить владельца team asset inventory и annotator/reviewer. Не открывать SELECT/lockbox только ради красивого количества subsets; теперь доступен конкретный obtaining/reannotation path, но production package отсутствует.
- **W2-A/W2-F runtime:** добавить к их минимальным traces source/available/decision/received timestamps, repeated-frame freshness, camera epoch и identity ambiguity; cache replay отделить от LinQ wall time.
- **Weights/stack-веткам:** pretrained route потребляет конкретный разрешённый artifact; отсутствие fine-tune не отменяет license/export/Neural-on-LinQ gates. CAUCAFall segmentation classes не автоматически равны detector ontology.
- **Evaluation/FSM:** принять включительную deadline boundary, half-open event intervals, one-to-one tie rule и censoring; при другой policy обновить expected fixtures до запуска, не после результата.

Остающиеся вопросы с владельцами, которые интернет не закроет: права конкретного конкурсного use URFD (root/use owner); exact team videos, lineage и отрицательные интервалы (data owner); scenario deadline и выбранная семантика состояния (product/evaluation owner); supported LinQ frontend и реальная частота (runtime owner). Публичные источники дают стартовый путь и обнаруженные ограничения, но не подменяют ответы команды.
