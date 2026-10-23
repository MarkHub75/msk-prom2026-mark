# W2_C — K002, K007, K008

Вторая волна, 23.10.2026, MSK. Контроль времени:06:22:11 MSK. Исходные Context-prompt.md/prompt-violation-methods-v2.md, PLAN, CRITIC K002/K007/K008, W1_C и SOURCES_C прочитаны; новые источники получены через web и прямое скачивание primary PDF. Модели/benchmark/приложение не запускались. [Первичные выписки и точные локаторы](SOURCES_W2C/EVIDENCE.md), [журнал поиска](SOURCES_W2C/SEARCH_LOG.md). Семантическое уточнение K001 получено от W2_A и принято: unconfirmed smoking≠false, off-body item≠unprotected bodypart.

## Что изменилось

1. **K002 — уточнена область, существенная часть закрыта.** Теперь есть реальный RGB manual Domination и две прочитанные object-detection работы, одна industrial. Поэтому object baseline имеет первичное основание и конкретный product envelope. Однако matched object-only/gesture-only/object+temporal comparison на eat/drink/phone/adjustPPE, camera-disjoint scenes и event FP denominator **не найден**. Условные маршруты остаются экспериментом W2-C-E01; AP сигарет не ранжирует smoking events.
2. **K007 — уточнена область и исправляется чрезмерное обобщение.** HDS не только presence detector: fulltext различает пять типов подвеса, включая незакрытый hook. Но это визуальные class labels без mechanical ground truth protocol. Temporal fall разобран по двум первичным методам; lying persistence — cue/отдельный endpoint, не необходимое определение всех падений.
3. **K008 — существование прямых каскадных следов установлено, net benefit остаётся открытым.** Найдены operational NVIDIA verifier и промышленная alarm-recheck публикация с доступным abstract. Fulltext YOLO+Florence2 CCTV показывает gain recall одновременно с loss precision. Нельзя писать ни «paired evidence нет вообще», ни «VLM гарантирует меньше false alarms». Наш выбор остаётся W2-C-E04.

## K002: какой RGB маршрут теперь можно обосновать

Исходный дефицит — W1 сравнивала RGB варианты преимущественно по слабой20clip работе, патенту и thermal manual. W2-C-F01 даёт связное руководство с face+cigarette постановкой; F02/F03 показывают, что многие работы с названием smoking detection на самом деле размечают cigarette box в одном изображении. **Название задачи не определяет GT.** F04 — читабельный pinned fusion code, позволяющий проверить, что «temporal» действительно означает в реализации. Эти источники не являются согласованным benchmark.

| Маршрут | Наблюдаемый вывод | Окно и нейронагрузка | Какие отрицательные случаи различимы | Что ещё не доказано |
|---|---|---|---|---|
| Cigarette object-only | Видимый cigarette-shaped object | Один image pass на каждый selected frame/ROI; temporal buffer не обязателен | Может отделить крупную бутылку/телефон, если cigarette действительно читаема; pens/fingers/tools остаются трудными | Текущий puff, принадлежность человеку, lit/unlit, smoking session, event FP/h |
| Face→cigarette-near-face | Предмет нужного вида в face ROI | Face calls + object calls на readable faces; число зависит от людей и sampling | Дальняя сигарета на столе отсекается геометрией; face occlusion уменьшает coverage | Drink/eat/PPE adjustment confusion в manual не измерена; скрытый рот — unknown |
| Gesture-only/keypoints sequence | Pattern hand-to-mouth конкретного track | Pose/hand keypoints на selected observations + sequence head/temporal aggregation; buffer/timestamps обязательны | Динамика может помочь, но eat/drink/phone/adjustPPE тоже дают hand-to-face | Без matched test это action candidate, не доказанный smoking; мелкие руки могут потеряться раньше сигареты |
| Object+temporal per-track | Согласованные cues предмета и движения на одном человеке | Детектор/ROI+pose либо clip head; дополнительные inputs и latency | Можно явно требовать owner consistency, объект и отрицательную классификацию соседних действий | Нет доказанного выигрыша именно нашей камеры; temporal confirmation сохраняет длительные systematic FP |

Таблица — наш методический вывод и предлагаемое сравнение, не ranking опубликованных AP. Числа neural calls следует считать через `selected frame rate × faces/persons/tiles × heads`, а не через FPS единственной сети. CPU-геометрия после keypoints не делает сам pose inference бесплатным. Video classifier добавляет sampling/buffer; число кадров клипа не равно wallclock duration без timestamps.

**Условный baseline A:** если original-image crop позволяет людям-разметчикам уверенно различить cigarette от pen/tool и рот виден, начать с object/face ROI, owner association и temporal evidence aggregation. Это самый короткий объяснимый маршрут; Domination показывает, что коммерческий аналог тоже ограничивает сцену. Его optimum100px не наш universal minimum; новый camera не допускается автоматически по совпадению одного числа.

**Условный baseline B:** если сигарета часто скрыта, но траектория рук читается, сравнить per-track action candidate с object+temporal route. Выход candidate не называть confirmed smoking. Если оба cue нечитаемы, отказаться от решения; VLM и crop upscale не восстановят отсутствующий сигнал. End-to-end candidate recall теряется и на gate/association/качества ROI, поэтому его нельзя вывести из action-head score.

F04 запрещает копировать популярный fusion prototype без аудита: history общая для сцены, первые object boxes не связаны с человеком, skipped-frame окно легко ошибочно назвать20кадровым. Это не признанный production defect; это проверяемый code-inspection counterexample к тезису «добавили pose+20frames — решили ownership и false positives».

**Семантика:** `smoking_action AND hazardous_zone` с temporally overlapping evidence. Inside+unknown smoking→unknown; smoking true+outside zone→false именно этого compound rule; smoking true+zone unknown→unknown. Negative smoking — отдельный контракт видимого отрицательного действия/окна, не отсутствие сигаретного box. Зона предоставляется заказчиком; внешний вид закрытой ёмкости не доказывает горючее содержимое.

### W2-C-E01 — paired smoking route selection, развитие C-E01

**Решение:** нужен ли дополнительный action/pose stage при целевой камере. **Минимальные входы:** original-resolution videos с capture timestamps, camera identity, GT на person/track, видимость лица/рук/сигареты, action intervals и configured hazardous ROI. Не формировать test из соседних кадров train; split по людям/клипам и отдельной камере/ракурсу. Достаточность объёма определяется доверительными интервалами и покрытием негативов, заранее произвольного N нет.

**Шаги:** один candidate pool, одинаковая association/event logic; сравнить object-only, gesture-only и object+temporal, подбирая thresholds только calibration split. Разметить eat/drink/phone/adjustPPE отдельно, включая один cue без другого, сигарету в руке без puff, соседнего курильщика, industrial pen/tool, occlusion и blur. Считать reject/unknown явно; проверить кадр пропуска/ID-switch/два человека. Отдельно raw-object и compound-event result.

**Метрики:** paired TP retained/lost, FP removed/added по baseline event IDs; event precision/recall и FP per negative camera-hour, time-to-first-alert по source clock; coverage/abstention; errors per hard-negative category; source crop sizes, calls/second, p50/p95 total latency. Короткий balanced clip test не заменяет отрицательные camera-hours. **Stop:** если human GT не видит нужный cue, это observability failure, не слабая модель; если B не даёт event benefit в доступной latency, оставить A+unknown. Успех не доказывает transfer на ночной/IR или новые камеры и LinQ compile.

## K007: hook и fall — отдельные endpoints

Исходный дефицит — fulltext HDS не проверен, fall positive formulation общая и ошибочно требует persistence. **W2-C-F05** сужает отрицательный W1 вывод: status classification визуального подвеса существует. Safe label нельзя механически раскрывать как «сертифицированно валидный anchor, несущая связь, закрытый и запертый gate». Отсутствуют hard-negative GT «внешне соприкасается, но механически не зацеплен» и physical inspection protocol. Нельзя смешивать эту supervised taxonomy с общим detector `hook`.

Для case-added hook условный маршрут — объявить нужный observable class contract и показать camera crop, где он различим; только после этого labels и test. `hook_visible=false` при закрытом карабине означает unknown. `Not closed` — реальный camera-visible target при соответствующем ракурсе, а `gate_locked` остаётся отдельным потенциально ненаблюдаемым свойством. Fulltext не доказывает наше исполнение на LinQ.

**W2-C-F06** даёт простой временной метод с lying negatives, но его inactivity confirmation сознательно исключает часть быстрых восстановлений и коротких клипов. **F07** даёт motion-stack formulation и конкретные boundary/rare-case errors. Это не повод переносить готовый old optical-flow graph в45часов; это основание правильно определить цель.

Предлагаемый контракт:

- `person_lying` — posture observation; включить намеренную работу лёжа как отдельную policy/context category.
- `suspected_fall_transition` — наблюдаемое резкое изменение позы/опоры с evidence before/during/after; быстрое восстановление не отменяет уже наблюдённый переход.
- `post_fall_immobility` — дополнительный temporal observation, повышающий приоритет при принятой policy.
- `medical_emergency` и фактическая травма не выводятся автоматически.

Начало клипа уже лёжа, occlusion всего перехода или track break сохраняет unknown о transition, даже если lying=true. Медленное намеренное укладывание — negative transition при видимом процессе. Быстрое намеренное укладывание/тренировочное падение может быть визуально неразличимо без контекста; не обещать восстановить намерение по RGB.

### W2-C-E02 — fall/hook supplemental slices

Для fall нужны onset/end GT отдельно от lying interval; сравнить slow intentional lying, fast intentional lying, fall+fast recovery, fall+immobility, kneeling/sliding/quadruped, maintenance lying, lost-before-transition. Считать transition recall/latency отдельно от lying and immobility, включая короткие и occluded clips вместо их удаления. Для hook нужны same-geometry attached/unattached/open-gate pairs и physical GT от эксперта, class confusion/unknown/visibility; camera crop, где невозможно различить, фиксирует stop. Находки P2 не расширяют обязательный перечень анонса.

## K008: что установлено о detector→VLM

Исходный дефицит — generic hallucination benchmark не отвечает на пользу verifier. **F10** закрывает существование настоящего upstream-candidate→clip-verification workflow, включая parsing/timeouts/short clips как инженерные отказы. **F09** — прямой industrial alarm study, но прочитан только abstract: нельзя объявлять его цифры paired proof. **F08** — полный CCTV experiment, показавший, что другая fusion objective повышает recall ценой precision. Это важное опровержение общей формулы «+VLM⇒FA↓»; данные не подтверждают обратную формулу «VLM бесполезен».

| Требование K008 | Доступный след | Остаток |
|---|---|---|
| Candidate selection | NVIDIA upstream detector/analytics; Kim использует each-frame VLM и threshold adaptation | Наш smoke/PPE candidate selection и miss rate |
| Model/version/prompt | Kim Florence2large fp16 + короткий smoke/fire prompt; NVIDIA configurable service | Exact checkpoint revisions, prompts для нашего rule/unknown |
| Crop/context/clip | NVIDIA alert snippets; Kim frame-level global context | Минимальный достаточный контекст/frames, owner consistency |
| Paired FP rescue / TP loss | Kim reports aggregate before/after P/R с иной decision rule | Reject-only verifier paired table отсутствует |
| Unit/split | Kim per-image, real+synthetic image mix; power-plant abstract alarm images | Event units, camera-disjoint split и negative camera-hour denominator |
| Latency/hardware | Kim deployment4FPS и latency table; NVIDIA timeouts | Нет достоверной latency нашей chain на предоставленном LinQ |

Следствие для45часов: detector+rules остаётся самостоятельным baseline. Verifier — отдельная optional ветка только при доступном execution path и paired benefit. Не замалчивать rejected/unverified/timeouts; unknown не превращать в отрицательный факт. Наш alarm policy при failed verification выбирает заказчик, а метрики считают этот случай отдельной строкой.

### W2-C-E04 — обязательный остаток выбора verifier, развитие C-E04

Зафиксировать baseline detector+rules **до** включения VLM. На одном immutable candidate pool сохранить event ID, GT, full context crop/clip, selected frames, model+revision, exact prompt, settings/output/parser verdict и latency. Split по камерам/клипам; prompt tuning только calibration. В test включить трудные baseline FP и TP, видимые/unknown scenes, два человека, мелкие СИЗ, разрешённую работу лёжа, display/fire reflections, decode failures и timeouts.

Таблица paired outcomes: baseline TP→accepted/rejected/unverified; baseline FP→accepted/rejected/unverified. Главные величины — FP rescue count/rate и TP loss count/rate со знаменателями, event precision/recall after fixed policy, coverage, p50/p95 end-to-end latency, calls/event и GPU/accelerator memory. Candidate-missed events не могут быть «спасены» reject-only verifier; считать upstream recall отдельно. Проверить повторяемость ответа на тех же inputs, prompt boundary и schema failure. **Stop:** без приемлемого TP loss и latency не включать suppressor; можно сохранить secondary review с явной неопределённостью. Успех на dataset не означает все нужные neural operations на LinQ.

## Остатки постановщику / соседним темам

**W2-C-Q01:** что именно smoking GT: видимый lit cigarette, puff, session, vape; какое окно допустимо считать отрицательным; как оценивают unknown? **Q02:** какие камеры/original streams и hazardous ROI; нужно ли видеть actual flammable material или это заданная зона? **Q03:** если добавлены fall/hook, transition и mechanical connection какой именно endpoint? **Q04:** должен ли VLM/pose/вся auxiliary chain исполняться на LinQ и какой runtime artifact допускается?

`datasets/training_strategy`: раздельные cigarette/object, smoking_action, visibility и hard-negative labels, camera/clip split. `evaluation`: image AP не event metric; paired tables E01/E04 и transition/lying endpoints. `model_stack/linq_platform`: сначала fixed object baseline, потом измеряемая цена face/pose/clip/VLM; spectral/DCT, attention, optical flow и hand pipeline не гарантированы публичным YOLO-family claim. `operator_product`: показывать причину unknown, исходный cue и verification-failed, не заменять неизвестное зелёным compliance.
