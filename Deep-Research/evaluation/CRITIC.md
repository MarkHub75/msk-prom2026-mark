# Промежуточная критика первой волны — evaluation

Дата: 2026-10-23, Europe/Moscow, UTC+03:00. Начальная критика сформирована после чтения завершённой W1; последующие ответы второй волны должны добавляться отдельными dispositions, не заменяя этот текст. Это промежуточная исследовательская роль, не финальный аудит отчётов.

## Основание и границы

Прочитаны целиком UTF-8: `Context-prompt.md`, `prompt-evaluation.md`, `_WORK/CRITIC_INPUT.md`, `_WORK/ROLE_PROMPTS.md`, `_WORK/PLAN.md`, `_WORK/RUN_STATE.md`, `_WORK/AGENT_PROMPTS.md`, все пятнадцать `_WORK/W1_01.md`–`W1_15.md`. Дополнительно просмотрены сохранённые исходники и результаты: COCO `_prepare/evaluateImg` и ограниченные fixtures; sed_eval matching/validators и примеры; CLEAR и его fixtures; LoadGen completion callback; результаты статистических и весовых иллюстраций; локальные retrieval-записи W1_15. Нового сетевого получения доказательств критик не выполнял. Локальные чтения, а не повторное исполнение, служат основанием этой критики.

Первая волна уже даёт сильную методическую базу. Основные риски находятся на стыках предложенных договоров: какая экспозиция нужна конкретному утверждению, как привязать доставленную тревогу к исходному времени, как выбирать непрерывные интервалы для проверки пропусков и как реализовать собственный matcher. Не обнаружено оснований повторять все пятнадцать обзоров. Четыре целевые задачи W2 ниже достаточно содержательны, чтобы получить новые доказательства и уточнить применимость. Они не заменяют будущую проверку на данных и устройстве.

Обозначения приоритетов: **P0** — влияет на допустимость ключевого утверждения или обязательного LinQ-пути; **P1** — влияет на воспроизводимость и маршрут при ограниченной разметке. Все K-ID ниже первоначально имеют статус **ожидает W2**. Вопросы, которым нужны частные артефакты, выделены отдельно: их нельзя объявить закрытыми публичной документацией.

## Что уже покрыто достаточно

| Область | Конкретное достаточное основание W1 | Что сохранять при сборке |
|---|---|---|
| Объект → человек → эпизод → доставленная тревога | W1-01-F02/P01; W1-03-P03–P07 и пример инвариантного object AP при смене владельца каски; W1-05-F01/P01 | Не повышать уровень утверждения без новой единицы истины. Oracle-GT-person и matched-person результаты остаются условными; пропущенный GT-человек остаётся в full-chain знаменателе. |
| Unknown, отсутствие и неполная разметка | W1-01-F01–F06/P01–P03; W1-03-P02/P06; W1-04 наблюдаемость опоры | Скрытая голова не является bare-head GT. Not reviewed, out of scope, GT unknown, model abstention и техническая недоступность различаются. Нужны counts/coverage рядом со score. |
| Точный AP и несовместимость evaluator | W1-02-F03–F10, pinned COCO/VOC source и E01; W1-14-F02–F04 | Сохранить greedy matching, координаты, maxDets, crowd/ignore, absent-class sentinel, AP interpolation и scale. TIDE AP50/ΔAP не автоматически COCO AP50:95; его prediction-only class convention отличается от COCO. Ограниченные fixtures не выполняли loader/compiled IoU/full summary. |
| Геометрия | W1-04-F01–F06 и четыре слоя проверки | Полигон/anchor rule, floor membership и physical body intrusion — разные истины; boundary equality, missing zone, holes, inverse transform и camera drift уже разобраны. Не нужен ещё один общий обзор point-in-polygon. |
| Дубли, split/merge и цензурирование | W1-05-F02–F08/X01–X03/P02 | Дубли могут не менять интерполированный AP. Cooldown не переписывает GT. Left-censored onset и right-censored follow-up отделены; известное короткое событие не тождественно оборванному наблюдению. K005 уточняет только ещё не операционализированную часть. |
| Трекинг | W1-09-F03–F12 и воспроизводимый узкий CLEAR counterexample | HOTA/IDF1/MOTA не читают wearer state и delivery. Frag=0 в указанной версии не доказывает непрерывность. Numeric track ID не удостоверяет личность. Full-ID/no-ID маршруты уже есть. |
| Leakage, split и test tuning | W1-07-F01–F18, pinned sklearn, WILDS correction; W1-08-P01 | Lineage до нарезки, защищённые dependency components, claim-specific camera/site/session grouping, temporal windows, declared adaptation и GT corrections уже покрыты. Отдельного общего поиска leakage не требуется. |
| Порог, калибровка и abstention | W1-08-F01–F09/P01–P02/C01–C09 | Нужна замороженная полная alert policy. Classification ECE не является вероятностью полезного события; shift и отбор меняют область калибровки. Replay необходим для каждого temporal configuration. |
| Ноль ошибок и малое число групп | W1-06-D01–D02; W1-13-F01–F07 и сохранённые расчёты | Пуассоновский 2.995732/H — условный односторонний 95% bound; не гарантия и не допущение по умолчанию. Одна камера не даёт тысячи независимых кадров. Paired cluster bootstrap, undefined resamples, few-group sensitivity и selection optimism уже разобраны. |
| Parity | W1-10-P0–P6, F02–F07, output contracts | Совпадение тензоров, детекций, GT quality и target placement различаются. Preprocess/NMS/threshold discontinuities, fixed-policy и retuned candidate отделены. Нет измеренного качества модели или доказанного target parity. |
| Latency survivor bias, очереди и часы | W1-11-F03–F11; W1-12-P01–P05 | Submit не равно completion; throughput не равно latency. Successful-only percentiles сопровождаются outcome/deadline counts; scheduled time не исчезает. Clock domains, RTP/NTP uncertainty, file pace и RTSP receiver proxy уже разобраны. K001/K002 уточняют интеграцию, не требуют заново изучать CUDA. |
| Покрытие и деградация | W1-12-F01–F07/P02–P05 | Независимый expected-work ledger, logical/attempt/batch units, retries, unresolved/drain, per-camera masks и end-to-end recall во всём requested footage уже даны. Меньше тревог при меньшем анализе не установлено как улучшение. |
| Ошибки и причинность | W1-14-F01–F10/E01–E04 | TIDE oracle — metric counterfactual; GT replacement не гарантирует достижимый upper bound. Диагностическая подборка отличается от probability sample; paired regressions и альтернативные причины сохраняются. |
| Harness, demo и фактическое исполнение | W1-15-P01–P04 | Manifest/config/prediction/timestamp/run артефакты и smoke/regression/demo/independent evaluation разведены. Только публичная документация подтверждена; ни установка, ни device run, ни LinQ performance не выполнены. |

Эта достаточность относится к исследованию методов. Она не означает, что выбран официальный matcher, известны допустимые deadlines, проверены реальные аннотации или выполнен промышленный тест.

## K001 — Публичный LinQ-путь найден поздно и ещё не встроен в общую доказательную картину

**Приоритет / вид пробела:** P0; публичная документация и version applicability, отдельно частный runtime/access unknown.

**Проблема и затронутые материалы.** W1-15-F03/F05 и S06 устанавливают существование публичного руководства IVA H1 2025 `RU.РМДВ.04.06.014-03 34 01`: показаны `inference.sync(...)` и TLM estimated `execution_time_us`. W1-11-F02 и ряд финальных unknowns W1_10/12 писались до этой находки. Их буквальное «SDK/version не supplied» остаётся верным; но при сборке нельзя превратить это в «completion API вообще неизвестен/публичных инструкций нет». Обратный скачок к «наш backend теперь поддержан и время известно» также неверен. Дополнительно локальная папка W1_15 содержит только retrieval failures; положительные чтения были web-only. Свежий критик не может проверить текст руководства по сохранённому первичному snapshot, хотя branch-report добросовестно сообщает положительный web-access.

**Последствие для решения.** Команда может потерять полезный documented local-host smoke route либо принять compiler/TLM estimate за измеренную target latency. Версии Python 3.8 на overview и 3.11 в manual, список yolo5s против yolo8/yolo11 на tech page не доказывают применимость ни одного пути к выданному устройству.

**Недостающее доказательство.** Повторно доступный первичный текст/снимок руководства с точными locator/version; подробный разбор границы `sync`, происхождения output и estimate, available timeout/error/async/device/placement сведений в этом документе; таблица «документировано в public revision / неизвестно для assigned runtime». Нужны именно приведённые документом свойства, без вывода API по аналогии с CUDA/ORT. Наличие wheel/SDK, удалённого endpoint, target hardware, действительных device logs и измеренного времени остаётся отдельным входом.

**Задание W2_01 (medium).** Получить и изучить public manual `https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf`, связанную `/docs` и ровно те дополнительные официальные материалы, которые проясняют эти границы. Сохранить текст/byte snapshot и provenance, если транспорт позволяет; при очередном сбое сохранить точный вид отказа и подробные locator-выписки из фактически прочитанного источника. Разобрать install/compile/load/submit/sync/output path, quantization calibration inputs, TLM versus physical device time, target identity/placement/fallback evidence и наблюдаемость ошибок. Обновить только область применимости W1, не утверждать установленность SDK или измеренное исполнение. Сформировать адресный checklist для → linq_platform/model_stack/video_architecture.

**Наблюдение для закрытия.** Есть проверяемая matrix с первичным основанием для каждой documented операции и ясными пустыми клетками. W1-11 unknown уточнён до неизвестной совместимости и actual remote semantics; TLM везде помечен estimate. Если публичный документ не описывает требуемое свойство, задача закрыта локализацией отсутствующего звена и маршрутом получения SDK/device evidence, а не утверждением отсутствия capability.

## K002 — Нет единого правила отнесения доставленных тревог к source-time экспозиции и границам прогона

**Приоритет / вид пробела:** P0; методический стык source timeline, wall time и evaluation cohort; решаем до доступа к данным.

**Проблема и затронутые материалы.** W1-06-P01/P02 считает source camera-hours и notifications «within H_eval»; W1-05-P01 использует фактический delivery timestamp; W1-11 описывает media-to-paced-replay mapping; W1-12 требует cutoff/drain и carry-in accounting. Однако эти части не задают единый cohort rule: тревога с evidence кадром перед концом source interval может прийти в drain, поздняя очередь из предыдущего интервала может прийти в текущий, retry может создать новый visible record после границы. Непонятно, к какому числителю и exposure они относятся. В as-fast-as-possible replay source seconds и operator wall seconds заведомо различаются. Общие формулировки не дают разрешения вычитать delivery wall timestamp из onset PTS.

**Последствие для решения.** Две реализации могут показать разную false-delivery rate или delay только из-за конца записи/длительности drain. Сбрасывание очереди за границей искусственно улучшит precision/latency; смешение исходных часов и реального wall workload может создать неверную операторскую нагрузку. Независимо от правильности всех отдельных clocks общая метрика останется невоспроизводимой.

**Недостающее доказательство.** Согласованный ledger с двумя отдельными estimands: нагрузка на единицу исходной source camera-time фиксированного input cohort и фактически видимые interruptions на wall interval. Нужны правила evidence ownership, original release, batch/retry, carry-in/out, accounting close, late delivery и left/right follow-up. Нужна явно выбранная допустимость live delay claim для unpaced, paced и true-live routes.

**Задание W2_02 (medium, вместе с K003).** Сопоставить W1-05/06/11/12/15 с первичными continuous-video и loadgen/end-to-end accounting основаниями; попытаться получить exact ActEV time-based protocol, ранее недоступный W1_06, только если он помогает показать отличие false-active duration от notification count. Не переносить ActEV score как наш delivery metric. Разработать original cohort/attribution proposal и toy ledger минимум для carry-in, arrival in drain, retry duplicate after close, result after timeout, changed replay speed и missing clock map. Использовать ограниченные арифметические/log fixtures, не строить сервис. Зафиксировать, какие исходные записи нужны, чтобы воспроизвести числитель.

**Наблюдение для закрытия.** Для каждого toy input однозначны numerator, exposure, unresolved/censored count и clock domain. Одни и те же данные нельзя незаметно улучшить укорочением follow-up. Source-hour burden и wall-hour interruptions имеют разные названия; unpaced replay не выдаётся за live latency. При недостаточном follow-up результат помечается неполным, а не нулём ошибок.

## K003 — Требования к полноте review сформулированы как будто у всех rates один знаменатель

**Приоритет / вид пробела:** P0; несогласованные условия применимости метрик, не недостаток реальной разметки как таковой.

**Проблема и затронутые материалы.** W1-06-P03.2 верно объясняет: полный просмотр каждого non-alert кадра логически не обязателен для false-delivery numerator, если все delivered items проверены с достаточным event context. Его P01 одновременно строит H_eval как пересечение analyzed/reviewed/observable времени. W1-12-P03/P04 и W1-15-P03 формулируют «fully reviewed camera-hours / never unreviewed hours» так, что при чтении отдельно это можно принять за обязательную сплошную событийную разметку для любого alert rate. Между тем workload, semantic false notifications, useful/timely unmatched alerts, event recall и false-active duration требуют разных reference evidence. Пересечение с A также меняет estimand при отказах; W1_12 уже предлагает requested и conditional view, но ещё не согласует их с W1_06. Unknown PPE у отдельного человека не обязательно делает весь camera-hour неизвестным для всех вопросов.

**Последствие для решения.** Можно либо без необходимости заблокировать полезную оценку false-alert burden из complete delivery log, либо, наоборот, заявить event recall/«normal negative exposure» после просмотра только тревог. Исключая интервалы на основании model success или unresolved alerts, легко получить благоприятный условный rate с изменённым denominator.

**Недостающее доказательство.** Таблица metric-specific sufficiency: требуется ли полный alert log, adjudication каждого alert, все GT onsets, состояние в каждом instant, независимая вероятность review, identity/context по соседним эпизодам, operational A/F mask. Для каждого — фиксированная source population, numerator, denominator, unknown handling, что остаётся неизмеренным. Нужно сохранять semantic false, excess duplicate и timely-usefulness failure как разные поля, даже если собственный matcher группирует их в FP endpoint.

**Задание W2_02 (medium).** Разрешить эти формулировки через первичные surveillance/statistical verification основания и собственный чётко помеченный measurement contract. Привести контрастные полные записи: все alerts проверены, non-alert intervals не размечены; отдельные event-unknown alerts; полностью просмотренные отрицательные интервалы; отказ анализа при известном исходном GT; отказ при незаписанном исходном видео. Для each claim указать supported / conditional / unavailable. Проверить, не привязана ли eligibility к output tested model.

**Наблюдение для закрытия.** Собранный текст позволяет честно сказать «F adjudicated false delivered records / H fixed logged source hours, all delivery records accounted for, missed-event recall unknown» при выполнении перечисленных предпосылок. Он не называет эту экспозицию полностью размеченным normal video. При unknown items даёт bounds/coverage или restricted claim, без автоматических TP/FP. Requested-footage и analyzed-only rates остаются двумя подписанными измерениями.

## K004 — Probability sample для поиска пропущенных событий пока не задан на уровне эпизода

**Приоритет / вид пробела:** P1; открытый methodological/public gap. Применимость к конкретным данным требует их получения.

**Проблема и затронутые материалы.** W1-06-P03.4 справедливо требует известные inclusion probabilities; W1-14-E02 показывает Σ y_i/π_i для alert population и отдельно требует non-alert intervals. Но нет законченного дизайна для длительного частично размеченного видео: что является sampled unit, как находить episodes на краях выбранного окна, как не пересчитать одно событие дважды, как длина эпизода меняет шанс попадания при правиле «пересекает окно», как оценивать ratio recall и handling zero sampled positives. Alert-population estimator нельзя непосредственно применить к неизвестному полному списку GT episodes.

**Последствие для решения.** Команда с длинным unlabelled видео может случайно предпочесть длинные, заметные эпизоды и завысить recall, потерять короткие события на границах или объявить ноль найденных пропусков доказательством отсутствия пропусков. Такое направление прямо входит в условные сценарии задания, поэтому общей рекомендации «sample randomly and weight» мало.

**Недостающее доказательство.** Первичный survey/event-in-time sampling method либо прозрачно выведенный original protocol с определённым event inclusion rule. Желателен простой маршрут с disjoint source-time cores и context margins, где событие принадлежит core по заранее выбранному onset/entry rule; отдельно left-censored pre-existing episodes. Для пересекающих окно событий нужна именно их inclusion probability, а не автоматически window probability. Ratio estimator, variance/uncertainty assumptions и неопределённость при few positive groups должны быть названы.

**Задание W2_03 (medium).** Исследовать design-based оценку totals/ratios и обнаружение событий в probability-sampled continuous intervals. Сравнить практически выполнимые designs, выбрать один условный минимальный маршрут и привести вычисленный tiny finite-population example с короткими/длинными событиями, двумя окнами, edge censoring и oversampling alerts. Развести all-alert review и independent interval review; не предполагать исчерпывающий GT roster до разметки. Указать что считается и чего нельзя оценить при convenience sample, неизвестной π, unresolved onset, нуле найденных positives или отсутствии достаточного context. Новые source snapshots/locators обязательны; маленькая конечная иллюстрация разрешена, модель не нужна.

**Наблюдение для закрытия.** Дизайн позволяет другому человеку построить sampling frame, сохранить draw/weights/context, найти каждый eligible event ровно по заявленному ownership rule и пересчитать totals/ratio. Пример демонстрирует/исправляет duration inclusion bias и не выдаёт ratio estimate за гарантированно unbiased quantity. Если точность не обоснована, итог — descriptive sampled evidence и конкретное ограничение, без выдуманного confidence interval.

## K005 — Interval-valued onset, unknown gaps и censored follow-up ещё не превращены в точные eligible/match outcomes

**Приоритет / вид пробела:** P1; собственный протокол требует формализации и проверки, industrial acceptance остаётся неизвестным.

**Проблема и затронутые материалы.** W1-01-P01/P03 и W1-04 задают onset bounds/unknown gaps. W1-05-P01.4 предлагает bounded delay/sensitivity, P02 правильно различает censored и короткие полностью наблюдённые эпизоды. Но обычный P01 matcher принимает точные start/end и delivered time. Не указано, как построить edge и eligible denominator при onset в [l,u], delivery в unknown gap, uncertainty конца или clip-end до deadline. Нет tiny expected-answer ledger, связывающего эту неопределённость с precision/recall. Сокращение для машинного отчёта особенно легко потеряет это условие.

**Последствие для решения.** Выбор удобного endpoint внутри onset interval меняет timely TP/FN и latency; исключение только censored failures завысит recall; неизвестный промежуток может стать фиктивной безопасностью или фиктивным reset. Это касается именно observable truth и follow-up, не только clock error.

**Недостающее доказательство.** Детерминированные варианты exact-boundary и interval-boundary endpoint: guaranteed / possible / unresolved eligibility/matching, conservative sensitivity/bounds и accounting полного censored stratum. Нужно отдельно рассмотреть совместимость person/zone keys, annotation unknown, unavailable processing, short event ending before D и observation ending before required follow-up. Границы, полученные из возможных GT вариантов, не являются sampling confidence intervals.

**Задание W2_04 (medium, вместе с K006).** На основе сохранённых benchmark sources, при необходимости новых первичных interval-censor/matching источников, формализовать original interval treatment без вымышленного промышленного допуска. Проверить tiny cases: точный onset; onset interval по обе стороны deadline; delivery до первого достаточного evidence; короткий episode с известным концом; right-censored до deadline с success и без success; occlusion gap; повторный вход после доказанного safe reset; reconnect и late result. Дать полный counts/eligibility table, не только сюжетный текст.

**Наблюдение для закрытия.** Для каждого случая заранее известны supported/unsupported/unknown outcome и denominator. Нельзя получить хороший recall, включив наблюдённые censored successes и исключив такие же censored non-successes из того же endpoint. Вариант с interval truth либо выдаёт честные sensitivity/bounds, либо оставляет named unknown; ни один endpoint не выдаётся за стандарт жюри.

## K006 — Собственные person/alert assignment objectives ещё не имеют проверенного deterministic implementation contract

**Приоритет / вид пробела:** P1; воспроизводимость собственного метода, не доказанная ошибка benchmark-кода.

**Проблема и затронутые материалы.** W1-03-P05, W1-10 detection agreement и W1-05-P01.5 предлагают maximum-cardinality, затем maximum summed IoU / minimum summed delay, затем stable-ID tie-break. Сохранённые W1_05 fixtures выполняют sed_eval cardinality matcher и collar validators, но не этот новый lexicographic algorithm; COCO fixtures выполняют другой greedy matcher. «Hungarian» без dummy/invalid-edge objective и fixed IDs сам по себе не реализует заявленную последовательность приоритетов.

Для delay есть дополнительное ограничение (собственная арифметика критика, не model test): если все четыре edges совместимы, GT onsets 0 и 2, alerts at 3 и 4 допускают delays [3,2] или [4,1]. Сумма обеих пар 5, maxima 3 и 4. Вообще при одинаковом выбранном множестве GT/alerts сумма d−s не зависит от перестановки пар. Поэтому secondary objective не обязательно разрешает неоднозначность или минимизирует хвост latency; deterministic tie rule остаётся существенным. Этот abstract graph не утверждает, что любые person-keyed episodes совместимы; реальные keys могут устранить ambiguity.

**Последствие для решения.** Два автора evaluator могут получить разные TP и per-event delays на одних outputs либо одинаковый count при разных tail delay. Невозможно воспроизвести parity/person/event результаты только по названию solver; offline reassignment нельзя интерпретировать как реальную online policy или доказательство меньшего physical delay.

**Недостающее доказательство.** Точное lexicographic objective, handling invalid edges/unmatched nodes, ordering/stable key, numeric tolerance, reproducible solver/version либо ясный original pseudocode. Нужны small graph counterexamples, expected pair lists, TP/FP/FN и delay distribution; проверка максимальной мощности отдельно от суммы IoU/cost и tie-break.

**Задание W2_04 (medium).** Прочитать первичный API/код выбранного доступного assignment solver; определить способ реализации objectives без случайных epsilon или необоснованной big-M величины. Можно использовать исчерпывающий tiny oracle для проверки маленьких graphs и отдельно помеченную solver fixture. Сравнить с chronological greedy/score-ordered policy на контрпримере. Включить empty sets, two-by-two ambiguous graph, cardinality-versus-cost conflict, equal-score/equal-IoU ties, invalid edges, duplicate outputs, wrong person/class, interval edges K005 и input permutation. Не менять official COCO/sed_eval semantics; собственный matcher получает отдельное имя/версию.

**Наблюдение для закрытия.** Есть точные пары и counts, сохраняемые на fixtures; результат инвариантен к input permutation при неизменных stable IDs либо зависимость прямо объявлена частью протокола. Если библиотека не гарантирует stable tied optimum, добавлена явная процедура или это ограничение сохранено. Sum-delay objective назван именно суммой, без обещания оптимального p95; measured online latency остаётся отдельным наблюдением.

## Неизвестные, которые нельзя закрыть новой публичной ссылкой

| Нужный вход / owner | Что уже есть | Какое решение меняет и что сохранить |
|---|---|---|
| Полный кейс/официальный evaluator/постановщик | Краткий официальный brief и regulation evidence W1-15-F01/F02; не обнаружено основания для числовой AP/FPS формулы жюри | Таксономия, observability, target population, deadlines, score units, allowed adaptation. Получить оригинал/version и отдельно воспроизвести mandated scoring; supplemental protocol не объявлять официальным. |
| Реальные datasets/annotation provenance | Методические schema и import checks W1_01/03/07 | Exhaustiveness, ownership, source lineage, independent cameras/sites/episodes и negative exposure устанавливаются по файлам/разметке. Отсутствие их в папке не означает, что они не будут выданы. |
| Compatible LinQ package/allocated hardware/remote service | Public API manual W1_15, ожидаемое уточнение K001 | SDK revision, endpoint/job semantics, actual device/placement, supported graph/precision/debug outputs, timer и fallback. Сохранить package/build/artifact hashes, request/output logs; public document не закрывает actual execution. |
| Native model, exported/compiled artifacts и calibration data | Staged parity W1_10 | Actual tensor schema, preprocess, operator lowering и task degradation allowance. До получения артефактов не заявлять export compatibility или качество. |
| Target video + independent annotations + deployment population | Proposed splits, exposure и uncertainty W1_06/07/13 | Нужны независимые группы и их выборка; ни «достаточное N», ни narrow CI, ни future-camera rate нельзя установить по методической статье. |
| Camera clock/PTS/sync, request/alert delivery logs | Clock and outcome contract W1_11/12 | Capture age и UI delivery могут остаться неизвестными при доступном client RTT. Не приписывать camera timestamp semantics по одному RTSP URL. |
| Product/task owner: unknown action, reminder utility, duplicate policy, delay limits | Разделение action/GT/time уже предложено | Выбор metric endpoint и provisional Pareto choice; нельзя выбрать универсальный D или цену FN/FP из чужого benchmark. |

Эти входы следует превратить в Q-ID/experiment gates при сборке. Их существование не блокирует четыре W2 research-задачи и не требует паузы до получения private access.

## Передача второй волне и сборщику

Приоритетная карта: **W2_01 → K001; W2_02 → K002/K003; W2_03 → K004; W2_04 → K005/K006**. Подробные самостоятельные задания и closure criteria находятся в `_WORK/CRITIC_HANDOFF.md`. W2_01–03 независимы и могут идти одновременно; W2_04 использует существующий W1 corpus и не должен ждать готовности остальных, но финальный текст согласуется с source-time/exposure definitions W2_02.

Сборщику: сохранить branch IDs и mapping в единый F/S/Q/E реестр, подписывать DOC/CODE/LOCAL MATH/PROPOSAL/UNKNOWN отдельно от факта выполнения. Не исправлять исходную критику задним числом. После W2 добавить под K-ID статус, основания, новый вывод и остающийся Q-ID, если нужен. Публичный источник может закрыть public-gap часть и оставить artifact-specific часть открытой.

Экспериментальные карточки должны использовать уже подготовленные W1 процедуры: evaluator fixtures; staged target parity; person–PPE full chain; temporal policy selection/freeze; continuous exposure false burden; paired A/B; load/failure/coverage; unknown/adverse/recovery. До данных/устройства это предлагаемые E-карточки. Локальные source-level fixtures и придуманные числовые примеры не являются измерениями модели, LinQ, реальных камер или промышленной безопасности. После W2 следует согласованная сборка/авторство/редактура/сжатие, без нового финального аудитора.


# Обработка замечаний после завершённой W2

Добавлено сборщиком 23 октября 2026, Europe/Moscow (+03:00). Исходная критика выше сохранена без переписывания. Это reconciliation результатов четырёх назначенных W2, не новый аудит/третья волна. Статусы относятся к методическим/публичным пробелам; actual application/device evidence не приписывается.

## K001 — Публичный пробел закрыт; actual applicability открыта
<a id="k001"></a>

[W2_01](_WORK/W2_01.md), [S124](SOURCES.md#s124), [S121](SOURCES.md#s121)–[S123](SOURCES.md#s123), [F002](RAW_FACTS.md#f002), [F216](RAW_FACTS.md#f216)–[F223](RAW_FACTS.md#f223). Сохранён первичный numbered manual L0–L650, printed pp5–10/17/19–25: local list/open/load/inference/blocking sync и returned outputs документированы. TLM execution_time_us — estimate, не physical measurement. Python3.11/3.8, compile defaults/family list и sample-fragment расхождения сохранены. Поэтому широкое W1 «completion API unknown» заменено неизвестной совместимостью actual package/remote interface. SDK/device run не выполнен. Открыты [Q009](OPEN_QUESTIONS.md#q009)–[Q012](OPEN_QUESTIONS.md#q012): wheel/build/working example/assigned endpoint, completion/error/placement/timer contract. [E002](OPEN_QUESTIONS.md#e002) закрывает только реально исполненные уровни.

## K002 — Методический attribution/close пробел закрыт; instrumentation открыта
<a id="k002"></a>

[W2_02](_WORK/W2_02.md), [F003](RAW_FACTS.md#f003), [F225](RAW_FACTS.md#f225), [F230](RAW_FACTS.md#f230)–[F234](RAW_FACTS.md#f234); event/processing-time analogy [S128](SOURCES.md#s128), не industrial standard. Договор version1 задаёт immutable latest-consumed-input anchor при first logical alert creation, original release, attempt/logical/visible IDs, source cohort versus receiver wall window, E/C/drain/carry-in/out и post-close deltas. Executed invented ledger даёт source6→7 records и receiver8→9 при close112→120, сохраняя late retry/timeout/pending; variable replay schedule не подменяет capture age. Delivered-by-C snapshot не eventual total, unresolved retry не finite upper duplicate bound. Открыт [Q013](OPEN_QUESTIONS.md#q013) и remote [Q010](OPEN_QUESTIONS.md#q010): actual logs/clocks/closure evidence. [E005](OPEN_QUESTIONS.md#e005)/[E007](OPEN_QUESTIONS.md#e007).

## K003 — W1 review wording согласовано по конкретному estimand
<a id="k003"></a>

[W2_02](_WORK/W2_02.md), [F224](RAW_FACTS.md#f224), [F226](RAW_FACTS.md#f226)–[F234](RAW_FACTS.md#f234), [S127](SOURCES.md#s127), [S129](SOURCES.md#s129). Complete delivery census плюс sufficient all-alert adjudication устанавливает named fixed-source semantic false burden без exhaustive non-alert GT. Это не verified-normal exposure/recall/false-active duration. Useful one-to-one precision требует complete matching neighborhood; sampled review — свой design. ActEV extracted function подтверждает excess instance-time (toy20/80=.25), а не point notifications; full scorer не выполнялся. Source-owned precision и onset-owned recall могут иметь разные boundary TP, F1 допустим только shared closed universe. W1 fully-reviewed-hours wording ограничено соответствующими более строгими endpoints. Actual reference/logs/utility остаются [Q001](OPEN_QUESTIONS.md#q001), [Q013](OPEN_QUESTIONS.md#q013), [Q014](OPEN_QUESTIONS.md#q014); [E005](OPEN_QUESTIONS.md#e005)/[E010](OPEN_QUESTIONS.md#e010).

## K004 — Sampling protocol закрыт методически; real audit/precision открыты
<a id="k004"></a>

[W2_03](_WORK/W2_03.md), [F004](RAW_FACTS.md#f004), [F235](RAW_FACTS.md#f235)–[F249](RAW_FACTS.md#f249), [S131](SOURCES.md#s131), [S117](SOURCES.md#s117), [S132](SOURCES.md#s132). Disjoint exhaustive cores, stratified SRSWOR/draw/pi/pairwise law, independent full-core review/onset ownership/context и component closure определены. HT totals design-unbiased для fixed corpus без iid contents; ratio generally biased, tiny enumeration mean.5625 versus true.3. Any-overlap length bias, zero positives, n_h1 variance absence, unresolved selected-unit nonresponse и uncertainty limits сохранены. Context discoveries не дополнительные selected samples; fixed margin не доказывает closure. Future cameras требуют отдельного population inference. Открыты actual source/manual/budget [Q002](OPEN_QUESTIONS.md#q002)/[Q004](OPEN_QUESTIONS.md#q004), complete outcomes [Q014](OPEN_QUESTIONS.md#q014), target population [Q015](OPEN_QUESTIONS.md#q015); [E010](OPEN_QUESTIONS.md#e010).

## K005 — Область уточнена / частично закрыто; general truth solver не заявлен
<a id="k005"></a>

[W2_04](_WORK/W2_04.md), [F006](RAW_FACTS.md#f006), [F253](RAW_FACTS.md#f253), [F262](RAW_FACTS.md#f262)–[F265](RAW_FACTS.md#f265), own exact fixtures [results](_WORK/W2_04_SOURCES/results.json). Definite/possible/forbidden interval edges, raw/eligible delay ranges, active-at-delivery/causal evidence, short complete opportunities и entire incomplete component quarantine определены. Censored observed successes исключаются из narrow primary вместе с comparable non-successes; отдельный observed-by-F endpoint включает обе стороны. Возможный union graph даёт только outer count bound: linked-onset example individually possible2, jointly feasible max1. Не создан general solver по jointly feasible onset/identity/roster/clock worlds; unknown roster меняет denominator. Поэтому K005 не объявляется полностью решённым для arbitrary uncertainty. [Q001](OPEN_QUESTIONS.md#q001)/[Q014](OPEN_QUESTIONS.md#q014)/[Q013](OPEN_QUESTIONS.md#q013) требуют actual policy/joint truth/log follow-up; [E001](OPEN_QUESTIONS.md#e001), [E010](OPEN_QUESTIONS.md#e010).

## K006 — Tiny deterministic reference закрывает воспроизводимость; scale/official scope открыты
<a id="k006"></a>

[W2_04](_WORK/W2_04.md), [F005](RAW_FACTS.md#f005), [F251](RAW_FACTS.md#f251)–[F261](RAW_FACTS.md#f261), [S133](SOURCES.md#s133)–[S135](SOURCES.md#s135). lex-offline-v1 exact Fraction/DP objective (-cardinality,sum cost,stable pair list), invalid/unmatched/empty semantics и immutable IDs определены. Выполнены13 named graphs/permutations и all5123×3 cardinality comparisons versus SciPy1.17.1 plus independent partial-injection oracle для трёх objectives. Это tiny reference, не production benchmark/scalable matcher. Sum delay не min-max/p95: fixed chosen subsets дают permutation-invariant sum. Offline reassignment не online policy; official COCO/ActivityNet/sed_eval semantics не изменены. Открыты policy/truth [Q001](OPEN_QUESTIONS.md#q001)/[Q014](OPEN_QUESTIONS.md#q014), scalable implementation [Q016](OPEN_QUESTIONS.md#q016), [E001](OPEN_QUESTIONS.md#e001).
