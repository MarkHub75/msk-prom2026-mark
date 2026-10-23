# OPEN_QUESTIONS — violation_methods

Состояние после двух исследовательских волн и сборки:2026-10-23, Europe/Moscow (+03:00). Полный кейс, native видео, назначенные LinQ hardware/SDK и программа приёмки не предоставлены. Нового поиска сборщик не выполнял. Вопросы ниже не скрытая третья волна: указан конкретный способ закрытия после получения артефакта/доступа/ответа/практической проверки.

**Все [E001](OPEN_QUESTIONS.md#e001)–[E017](OPEN_QUESTIONS.md#e017) — предлагаемые процедуры, ни один E не выполнен.** В волнах читались документы/код/metadata и отдельные XML/JSON/изображения; это не model benchmark, не полный semantic acceptance и не runtime VMS test. Связанные E могут использовать один набор клипов/GT, но отвечают разным решениям и не считаются независимыми измерениями.

## Короткая P0-группа для первого контакта

1. [Q001](OPEN_QUESTIONS.md#q001)/Q002: обязательные СИЗ и approved types; «снят» как state или transition; что делать без предыстории.
2. [Q003](OPEN_QUESTIONS.md#q003)/Q009: смысл зоны/flammable context/smoking-positive и наблюдаемого negative; activation/authorization.
3. [Q004](OPEN_QUESTIONS.md#q004): original streams, camera modes/ракурсы/native target size, возможен ли checkpoint.
4. [Q005](OPEN_QUESTIONS.md#q005)/Q006: граница всех neural stages на LinQ и exact назначенный hardware/SDK/artifact proof.
5. [Q007](OPEN_QUESTIONS.md#q007)/Q008: timestamps/cadence и acceptance unit, minimal episode/max delay, FP/duplicates/unknown/negative hours.

Первые15–20минут после кейса:0–4мин выписать обязательные endpoints/метрики/политику;4–8мин проверить глазами native face/head/feet/cigarette и camera mode;8–12мин сопоставить каждому endpoint простой method+U gate и missing inputs;12–16мин предъявить exact graph/access вопросы LinQ;16–20мин выбрать admitted scope/fallbacks и вопросы первого чек-поинта. Это предлагаемый маршрут, не обещание реализовать chain за20минут. Подробная карта — [_WORK/COLLECTOR_HANDOFF.md](_WORK/COLLECTOR_HANDOFF.md).

## Подробные вопросы


<a id="q001"></a>
### Q001 — Какие СИЗ/типы и части тела действительно обязательны?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: анонс перечисляет примеры, а не полный ТЗ; medical face cover, industrial cartridge, high-vis garment, generic vest и corrective glasses не взаимозаменяемы. Наличие предмета не гарантирует нужное покрытие/защиту. 3M требует fit/seal процедур, недоказуемых обычным RGB. Искали в PPE papers, реальных YAML/JSON, manuals и manufacturer instruction; основания [F005](RAW_FACTS.md#f005)/F007/F016/F017/F069/F072/F073/F119.

Неизвестно: approved respirator/glasses/garment types, допустимые альтернативы, нужны ли две перчатки, ремень каски, положения/контексты, где требование активно. Это политика заказчика, а не недостаток нового общего поиска. Решение: taxonomy, labels, отрицательный класс, eligibility и перечень обещаний. Закрытие: полный кейс/ответ эксперта с примерами allowed/disallowed/unknown, затем [E001](OPEN_QUESTIONS.md#e001)/E003. До ответа неподдерживаемый тип=U. Связь: K001/K003.

<a id="q002"></a>
### Q002 — «Снят респиратор» означает состояние uncovered или наблюдённое снятие?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: видимый респиратор на шее/в руке описывает item, а не отсутствие другого надетого; C=F и item-doffing D различны. Вход человека уже с открытым лицом может нарушать state-rule без наблюдённого transition. Через blind gap можно получить bounds изменения, но не observed removal/точный onset. W2 просмотрел industrial head-state и реальные SH17/R2PPE exports; direct transition artifact не получен. [F066](RAW_FACTS.md#f066)–[F075](RAW_FACTS.md#f075)/F100/F102.

Неизвестно: нужен именно item-doffing, coverage-loss или состояние, оценивают ли начало клипа без предыстории. Решение: A face-state против B temporal association, GT и neural workload. Закрытие: заказчик фиксирует endpoint, затем [E016](OPEN_QUESTIONS.md#e016) с отдельными C(t)/D(t)/visibility. K003. Не требовать нахождения снятого предмета для установления видимого uncovered state.

<a id="q003"></a>
### Q003 — Что означает опасная/горючая зона и условие допуска?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: floor contact, любая часть тела, 3D envelope, direction crossing и proximity — разные предикаты. Bbox overlap не floor occupancy; barrel detection не содержимое/flammability; trackID/цвет жилета не permission. Manuals Frigate/Supervision/DeepStream и monocular proximity прочитаны; [F027](RAW_FACTS.md#f027)/F036/F038/F039/F046/F103/F104/F109.

Неизвестно: image floor ROI или dangerous volume, событие входа либо длительное присутствие, предоставлена ли flammable ROI, активность техники/наряд/authorization. Решение: anchor, external inputs, wording, onset и priority. Закрытие: полный кейс + схема сцены от постановщика; [E006](OPEN_QUESTIONS.md#e006)/E007/E010. При отсутствии внешнего контекста честный output «человек в Z», а необходимые неизвестные предикаты U. K001/K002/K005.

<a id="q004"></a>
### Q004 — Наблюдаемы ли нужные части тела/сигарета в фактических native streams?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: Macroscop/Bosch/Axxon/Domination дают разные product-specific size/angle/FPS units. Невидимое лицо не устанавливает ни presence, ни absence facePPE; real IR не эквивалент grayscale augmentation. Источники [F018](RAW_FACTS.md#f018)/F048/F076–[F081](RAW_FACTS.md#f081)/F084/F090/F112/F122; журналы W1/W2 проверяли manuals и preprocessing, не камеры кейса.

Неизвестно: исходные resolution/codec/bitrate/exposure/IR, native head/hand/cigarette sizes, topview/occlusion, camera motion, доступность original ROI и checkpoint. Решение: admit camera-region/class, crop/tiles budget, исключение либо другой ракурс. Закрытие: файлы/stream metadata от организаторов + [E003](OPEN_QUESTIONS.md#e003)/E013 и smoking [E011](OPEN_QUESTIONS.md#e011). До этого product minimum не гарантия. K002/K003/K004.

<a id="q005"></a>
### Q005 — Какие нейросетевые этапы обязаны исполняться на LinQ?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно только общее условие model inference on LinQ из официального анонса [F065](RAW_FACTS.md#f065); CPU geometry/tracking without ReID/rules не neural inference. Pose, ReID, crop classifier, temporal network и VLM — дополнительные нейроэтапы, [F116](RAW_FACTS.md#f116)/F117.

Неизвестно: разрешён ли внешний verifier/локальный auxiliary inference, допустимая граница CPU decode/NMS/postprocess, какие proof artifacts ждут. Поиск публичной LinQ страницы не определяет правила конкретного кейса. Решение: допустимость всей chain и optional VLM. Закрытие: прямой ответ постановщика + linq_platform, зафиксированный execution contract; затем [E015](OPEN_QUESTIONS.md#e015). Отсутствие ответа не разрешение обойти обязательный LinQ. K008.

<a id="q006"></a>
### Q006 — Какой exact graph реально compile/execute на назначенном LinQ?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: vendor lists int8/CNN/RNN/yolo5s/yolo8/yolo11 и ONNX/Compiler/DNN Quant, но без checkpoints/shapes/opsets/postprocess boundary. HPS — конкретная линейка; fp16/bfloat16 обозначены перспективой. [F063](RAW_FACTS.md#f063)/F064/F114/F116/F117.

Неизвестно: назначенные устройство/SDK/compiler/runtime, artifacts, static/dynamic shapes, attention/3D conv/keypoint heads/QDQ, mixed precision/float outputs/fallback, доступ и RPC. Это не доказанная unsupported возможность. Решение: простой detector против каскада/pose/OVD/VLM. Закрытие: получить SDK/device, предъявить hash и ops конкретного ONNX, выполнить четыре gate [E015](OPEN_QUESTIONS.md#e015). Передача linq_platform/model_stack. Ни один export/compile/run в исследовании не выполнен.

<a id="q007"></a>
### Q007 — Каковы source timestamps, jitter, drops и реальная cadence результатов?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: ByteTrack update step и fixed dt не становятся variable-time от frame_rate; Frigate source frames могут не доходить, stationary reuse даёт текущий timestamp без нового neural observation. [F040](RAW_FACTS.md#f040)/F041/F085–[F088](RAW_FACTS.md#f088)/F105.

Неизвестно: PTS/capture clock, out-of-order handling, реальный LinQ throughput/queue/network cadence, короткие burst losses и latency. Решение: tracker, duration support, max gap/stale TTL, confirmation и измерение delay. Закрытие: linq_platform/video_architecture записывают capture/inference/receive/publish trace; [E008](OPEN_QUESTIONS.md#e008)/E009/E015. Configured FPS не измерение. K006.

<a id="q008"></a>
### Q008 — Как определены приёмка, знаменатели, latency и unknown?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: itdf требует95/98/90% «достоверности» без достаточного denominator; OIL GEM/2026/B/7902194 quoted7.13 требует90% ideal/80% challenging, встречается вопрос о95%, методика отложена на Design/approval. SAT/signoff запланированы, actual results не получены. [F025](RAW_FACTS.md#f025)/F082/F083/F107.

Неизвестно: event/person-frame unit, GT count/split, минимум эпизода, maximum delay/source clock origin, negative camera-hours, FP/duplicate/unknown definitions, excluded cameras, границы occlusion/scene change. Решение: threshold selection, temporal tradeoff и честное демо. Закрытие: постановщик даёт ПМИ либо подписывает [E010](OPEN_QUESTIONS.md#e010); evaluation определяет matching/availability/coverage до теста. Чужие проценты не наша цель автоматически. Связь K005; [E009](OPEN_QUESTIONS.md#e009)/E010/E011/E014.

<a id="q009"></a>
### Q009 — Что именно smoking-positive и наблюдаемый smoking-negative?

**Приоритет:**P0. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: cigarette object, hand-to-mouth, puff/session и smoke — разные cues/units. DAHD/CDPA — image cigarette boxes; Domination face→cigarette manual не раскрывает action window/hard-negative evaluation; clip study16/32frames неоднозначна. Missing cigarette/action не F; S AND H требует совпадающего времени. [F051](RAW_FACTS.md#f051)/F090–[F093](RAW_FACTS.md#f093)/F100/F108/F123.

Неизвестно: lit cigarette/puff/session/vape, допустимое отрицательное окно, handling concurrent drinking+smoking, длительность important event и hazardous context. Решение: object baseline A против gesture/temporal B, output candidate/confirmed/U. Закрытие: эксперт задаёт GT contract; [E011](OPEN_QUESTIONS.md#e011) camera/clip-disjoint paired comparison. K001/K002. Искомая ACM fusion paper403; matched primary industrial route comparison не получено, не объявлено отсутствующим во всём мире.

<a id="q010"></a>
### Q010 — Где actual SH17 extended tags и какой semantic remap нужен данным?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: YAML indices helmet10/hands11/head12/face-mask5 не порядок Table2. Два VOC+два YOLO examples прочитаны; TXT5columns, XML object fields без wearer/on-off/relation. Firefighter helmet off-body и head вне кадра — coverageU. Repo/tree/releases/Kaggle API inspected, inventory partial. [F005](RAW_FACTS.md#f005)/F007/F066–[F068](RAW_FACTS.md#f068)/F101.

Неизвестно: отдельный extended export/guide и доступный wearer/visibility mapping всего набора; SHWD actual XML/partial-Pictor GT также требуют acceptance. Решение: positive-object-only, relabel/ignore либо готовый state GT. Закрытие: конкретный авторский архив + [E001](OPEN_QUESTIONS.md#e001); datasets получает точные field checks. No entry не negative; отсутствие найденного extended asset не доказательство несуществования. K003.

<a id="q011"></a>
### Q011 — Доступны ли industrial neck/hand/removal annotations целевого типа?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: YOLOv8-LPE fulltext даёт industrial3M front/side wear/no_wear/wrong + back_head, но files/guide не получены и neck/hand/transition нет. R2PPE actual123751 annotation schema медицинская, без track/wearer/relation и neck/hand/remove; FMR-DB abstract-only. [F069](RAW_FACTS.md#f069)–[F075](RAW_FACTS.md#f075)/F102.

Неизвестно: готовые target GT/weights для off-neck/hand и наблюдённого снятия; сколько случаев реально видно нашим камерам. Поиск RU/EN/Chinese и официальных archives завершён точным остатком. Решение: state-only, собственная разметка/съёмка или отказ от B. Закрытие: авторский артефакт либо target clips/экспертные labels, [E001](OPEN_QUESTIONS.md#e001)/E016. K003. Успех generic mask dataset не закрывает industrial policy.

<a id="q012"></a>
### Q012 — Оправдывает ли pose/HOI цену на target ownership?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: same-detector APkeypoint .675 vs refitDT .664 и direct .663, но APsmall .211 хуже .222/.248; это не crowded ownership accuracy. Containment/one-to-one head matching/pose имеют разные failure modes. [F009](RAW_FACTS.md#f009)/F010/F011/F120.

Неизвестно: relation errors при crowd/leaning/held/spare PPE с одинаковыми detections и GTowner/part. Решение: включать ли дополнительный neural stage и какие classes. Закрытие: [E002](OPEN_QUESTIONS.md#e002) сначала oracle boxes, затем actual model; calibration/test scene split. Нужны relation labels, не ещё один общий pose обзор.

<a id="q013"></a>
### Q013 — Какая unknown/aging/best-frame политика сохраняет coverage и recall?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: U не negative/safe, stale wearing не current wearing; pure best-score может выбрать единичный FP или старый кадр до снятия. Теория risk–coverage i.i.d. не гарантирует correlated video transfer. [F015](RAW_FACTS.md#f015)/F100/F105–[F107](RAW_FACTS.md#f107)/F121.

Неизвестно: pause/reset/expire windows, допускаемая age, длительность signal/track loss, условия same-incident return и цена abstention на target stream. Решение: confirmation, technical end/censoring и объём охвата. Закрытие: [E004](OPEN_QUESTIONS.md#e004)/E005/E009 + operator_product policy; фиксировать FA на observable и scheduled hours с availability. При loss не писать observed_exit.

<a id="q014"></a>
### Q014 — Кто источник hazard_active/authorization, каков TTL/outage?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: person/equipment geometry не даёт equipment activation/permission. Стационарная машина может работать; helmet color/tracker ID не identity/access. [F104](RAW_FACTS.md#f104)/F107; источники VMS дают primitives, не готовую factory policy.

Неизвестно: PLC/API/schedule/наряд/СКУД, соответствие человеку, validity interval, отказ внешнего feed. Решение: «в зоне» против «несанкционированно в активной зоне», unknown conjunction и evidence. Закрытие: постановщик и integration contract; [E010](OPEN_QUESTIONS.md#e010) проверяет provenance/TTL/invalid rule. Не заменять недоступный feed ложным permission.

<a id="q015"></a>
### Q015 — Каков реальный event effect pinned Frigate ledgers?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: W2 замкнула all counter writes/caller/init/reset/end/new ID и same-commit docs cfa08c56b23d23280c3d0a218e5a43182c97445b. Ordinary-zone counters не обнуляются на out в прочитанном path; zone anchor last measured box, не estimate; stationary reuse может выглядеть fresh. Ручная in,out,in при inertia3 ещё не даёт entry, следующий in даёт. [F085](RAW_FACTS.md#f085)–[F088](RAW_FACTS.md#f088).

Неизвестно: runtime Norfair lifetime, actual cadence/queue path и видимые события в выбранной конфигурации. Решение: своя explicit temporal policy, а не сообщение о reproduced bug. Закрытие: [E017](OPEN_QUESTIONS.md#e017), затем [E009](OPEN_QUESTIONS.md#e009) на собственном GT. K006 static scope закрыт; runtime открыт. Нового общего аудита VMS не нужно.

<a id="q016"></a>
### Q016 — Можно ли получить ПМИ/actual SAT и полный OIL SoW?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: official NIT8p и prebid97p получены,94 numbered content; original SoW hyperlink извлечён из NIT, но download failed. Prebid quotes точны в своём источнике; signed SAT/award/operation metrics не найдены. K005 теперь имеет промышленный procurement chain, но denominator/method deferred. [F082](RAW_FACTS.md#f082)–[F084](RAW_FACTS.md#f084)/S068/S069.

Неизвестно: полный SoW1786430899.pdf, окончательная версия criteria, accepted quality/FAhours и camera-specific exclusions. Решение: область внешнего практического сравнения и наш запрос к клиенту. Закрытие: получить конкретный документ от OIL/автора/постановщика либо оставить unsupported. Дальнейший сетевой поиск не выполнялся сборщиком. Источник requirement не measurement.

<a id="q017"></a>
### Q017 — Доступны ли целевые RegistryKeys/VMDA таблицы нужной версии?

**Приоритет:**P2. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: [S036](SOURCES.md#s036) metadata/оглавление частично прочитаны, целевой body502/TLS EOF. Snippets VMDA.oneAlarmPerTrack/LongInZoneTimeout2/report_frequency не достаточны для defaults. Искали в W1A/B, exact URLs/logs сохранены.

Неизвестно: surrounding table, версия, units и реальные defaults. Решение: только optional external comparison; базовый event contract не блокируется. Закрытие: получить полный документ и проверить exact page/version либо исключить параметры. Не превращать1/10s/3000ms из индекса в F.

<a id="q018"></a>
### Q018 — Если fall/hook добавлены в кейс, какой endpoint реально нужен?

**Приоритет:**P2. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: Macroscop ищет lying, Lim не распознал малый hook и connection не реализовал; HDS fulltext имеет Wrong place/Safe/Wrong tie/Too thin/Not closed с staged data/split caveat. Temporal fall methods включают свои exclusions и не измеряют fast-recovery отдельно. [F049](RAW_FACTS.md#f049)/F050/F054/F094–[F096](RAW_FACTS.md#f096)/F124.

Неизвестно: нужен posture, fall-transition, post-fall immobility либо gate/anchor mechanical truth; читается ли hook target camera, physical GT protocol. Решение: не обещать emergency/connection по posture/harness. Закрытие: полный кейс/эксперт, [E012](OPEN_QUESTIONS.md#e012); short/occluded/fast-recovery не выбрасывать ради красивой accuracy. W1 C-Q06 fulltext вопрос закрыт W2, но physical endpoint открыт. K007.

<a id="q019"></a>
### Q019 — Даёт ли reject-only VLM verifier paired net benefit?

**Приоритет:**P2. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: NVIDIA VSS3.3.0 operational candidate→clip workflow и failure traces прочитаны; Guo alarm-recheck1068images только abstract claims; Kim fulltext использует each-frame Florence2 + adaptive threshold .5→.3 и precision↓/recall↑, не reject-only matched table. [F058](RAW_FACTS.md#f058)/F097–[F099](RAW_FACTS.md#f099)/F115/F125.

Неизвестно: наш exact checkpoint/prompt/context, TP lost vs FP rescued, upstream miss, unknown/failure policy, camera-disjoint event metrics и LinQ execution. Решение: suppressor, secondary review или отключить. Закрытие: [E014](OPEN_QUESTIONS.md#e014) и [Q005](OPEN_QUESTIONS.md#q005)/Q006. Прямые каскадные traces существуют; положительный net effect нашей chain не установлен. K008.

<a id="q020"></a>
### Q020 — Как INT8 меняет малые PPE/keypoints и события нашего artifact?

**Приоритет:**P1. **Статус:** открыто в указанной области; факты и границы поиска ниже.

Известно: PTQ4ViT показывает механизм post-softmax/GELU и успешные specialised8bit; PeopleNet example FP32→PTQ/QAT даёт spurious boxes и существенные mAP различия, но не LinQ/YOLO/PPE. [F061](RAW_FACTS.md#f061)/F062/F118.

Неизвестно: target calibration representativeness, raw tensor/coordinate drift, confidence/NMS/tracker/event effects, поддержка mixed precision/QAT/float heads. Решение: graph/precision route и фактический promised scope. Закрытие: [E015](OPEN_QUESTIONS.md#e015) на exact assigned device с reference frames/GT; class/size/night/crowd slices. Не путать heatmap coordinate discretization с arithmetic INT8 и не переносить чужой процент потери.

## Полные процедуры практической волны

Все параметры sweeps ниже — **PROP**. Чужие vendor defaults сохраняются в RAW_FACTS и не становятся рекомендованными порогами. Thresholds выбираются calibration/по policy, test не используется для подгонки. Сохраняются source-time, actor association, unknown/availability и знаменатели. Ни один эксперимент не выполнен.

<a id="e001"></a>
### E001 — Semantic annotation acceptance до обучения

**Связи:** [Q001](OPEN_QUESTIONS.md#q001)/Q010/Q011; K001/K003. **Статус:** PROP; не выполнено.

**Решение:** использовать export как state/coverage/removal GT, remap/relabel/ignore либо оставить positive objects.

**Входы/доступы:** actual archive+guide/YAML выбранных SHWD/SH17/CHV/Pictor/R2PPE/industrial sources, реальная небольшая стратифицированная выборка: tiny/partial/back/head out-of-frame/on-face/neck/hand/spare/occlusion. Approved-type policy и два независимых разметчика.

**Шаги:** (1) зафиксировать hash/revision и annotation unit; (2) сверить реальные IDs с YAML, а не порядком статьи; (3) проверить поля wearer/track/time/relation/on-off; (4) отдельно разметить item relation, part coverage, visibility, requirement, zone, rule-result; (5) согласовать disagreements и distinguish omission vs visible negative. Специально повторить spare-on-face+off-body и head-out-of-frame counterexamples. Не делать ambiguity negative.

**Метрики/наблюдения:** wrong-unit fraction, taxonomy conflicts, unknown wrongly-negative, adjudicated ambiguity по сценам, field presence и inter-annotator disagreement; universality numeric cutoff не назначен.

**Сохраняемое доказательство:** mapping table, actual sample annotations/crops с разрешённым происхождением, guide locator, disagreement adjudication, hash и decision log.

**Исходы/последствия:** доступный state artifact → перейти к выбранной модели; object-only → собственная coverage/relations разметка; противоречивые labels → relabel/ignore/exclude. Успех не доказывает transfer, лицензии/weights availability или LinQ. W2 уже читала два SH17 примера и R2PPE schema; это узкая инспекция, **не выполненный [E001](OPEN_QUESTIONS.md#e001)**.

<a id="e002"></a>
### E002 — Ownership на одинаковых detections

**Связи:** [Q012](OPEN_QUESTIONS.md#q012); [F009](RAW_FACTS.md#f009)/F120. **Статус:** PROP; не выполнено.

**Решение:** достаточно geometry или нужен pose/HOI stage для конкретных failure groups.

**Входы:** одна и та же GTowner/part выборка с isolation/crowd crossing/leaning/held/table/spare/donning, person/head/PPE boxes и доступный pose output; calibration и отдельная test-сцена.

**Шаги:** сначала oracle boxes отделяют relation error; сравнить containment/normalized head distance, one-to-one head matching, pose anchors. Затем одинаковый actual detector для full chain. Пороги выбирать на calibration, не на test. Invisible keypoint не считать observed part. Learned HOI добавлять только при actual relation data/export path, не как обязательный третий baseline.

**Метрики:** owner accuracy на resolved links и denominator links, ambiguity/U fraction, false compliance from held/neighbor item, missed violation, ошибки по crowd/pose/native head size, latency и crops/calls per person.

**Доказательства:** immutable detections, relation GT, overlays, assignment traces/threshold/version, paired error examples, timing.

**Исходы:** оставить самый дешёвый вариант при приемлемых event requirements; pose лишь там, где выигрыш подтверждён и цена допустима; ambiguous → U. Постановочные clips не доказывают deployment crowds, oracle stage не end-to-end detector quality.

<a id="e003"></a>
### E003 — Наблюдаемость каждого PPE и empirical supported region

**Связи:** [Q001](OPEN_QUESTIONS.md#q001)/Q004; [F018](RAW_FACTS.md#f018)/F048/F119. **Статус:** PROP; не выполнено.

**Решение:** какие camera-region/part/type admitted, нужен ли checkpoint.

**Входы:** native target camera videos, approved PPE/GT; реальные расстояния/ракурсы/dayIR/occlusion, размеры head/face/hands/PPE на source и tensor; controlled degradation только отдельной серией.

**Шаги:** два разметчика отмечают visible positive/visible negative/unobservable. На одном GT сравнить fullframe с native part crop, head-state с face/hand classifier; отдельно helmet/respirator/protective vs corrective glasses/gloves left-right. Добавить neck/hand/spare, unsupported type/visor. Calibration определяет eligibility, held-out camera проверяет область.

**Метрики:** state confusion, violation precision/recall, false compliance, unknown/person-time по size/angle/condition, source/tensor extents, neural input counts. Не заменять реальную дальность synthetic downsample.

**Доказательства:** camera/preprocess metadata, source/crop pairs, visibility GT и reasonsU, frozen gate settings, per-slice tables.

**Исходы:** admitted empirical region, более крупный crop/другой ракурс/checkpoint, либо исключённый predicate. Успех в выбранной size-bin не физический universal threshold и не fit/seal certification. Общий camera workload/crop сравнивает [E013](OPEN_QUESTIONS.md#e013); данные можно использовать совместно без двойного счёта измерений.

<a id="e004"></a>
### E004 — Temporal unknown и best-evidence aging

**Связи:** [Q002](OPEN_QUESTIONS.md#q002)/Q013; [F100](RAW_FACTS.md#f100)/F121. **Статус:** PROP; не выполнено.

**Решение:** recent evidence windows, pause/reset/expire и stale limits по part.

**Входы:** временные GT/tracks wear→remove→hold→occlude→rewear, already uncovered, pureU/negative, duplicate item, реальные capture timestamps/gaps.

**Шаги:** сравнить per-frame, recent eligible aggregation, quality-selected frames и unknown pause/reset/expiry. Calibration/test split по clip/camera; best frame не выбирается по testGT. Хранить age каждого part, не склеивать incompatible time snapshots. Отдельно correct/ambiguous re-association.

**Метрики:** event precision/recall/FA per negative camera-hour, observable-onset delay, false observed-clear under occlusion, stale age, decision coverage/person-time, evidence interpretability.

**Доказательства:** predicate/evidence selection timelines, timestamps/crops, GT visibility intervals и end reasons, chosen settings.

**Исходы:** policy с объявленным coverage/recall tradeoff; ложное clear при U исключить. Успех synthetic trace не исправляет detector и не доказывает deployment distribution; общий lifecycle проверяется [E009](OPEN_QUESTIONS.md#e009).

<a id="e005"></a>
### E005 — Selective prediction и camera/domain shift

**Связи:** [Q013](OPEN_QUESTIONS.md#q013); [F015](RAW_FACTS.md#f015)/F121. **Статус:** PROP; не выполнено.

**Решение:** полезен ли отказ и чем ранжировать eligibility.

**Входы:** calibration camera и unseen held-out camera/shift, T/F/U GT включая unsupported PPE и длительные occlusions.

**Шаги:** ungated, confidence-only, visibility+size, combined gates на одинаковых inputs; freeze thresholds перед test, risk–coverage curves и event consequences. Отдельно OOD и signal loss, весь required person-time остаётся в coverage denominator.

**Метрики:** selective error/coverage, event FA, recall including abstentions, unknown by reason, calibration error и extra neural calls.

**Доказательства:** immutable splits/gates, all-denominator tables, curves, representative rejected/accepted mistakes.

**Исходы:** gate включить при приемлемом реальном tradeoff; иначе корректировать supported region/не маскировать плохой detector почти полным abstention. I.i.d. theorem не гарантия для correlated CCTV или другого цеха.

<a id="e006"></a>
### E006 — Anchor и boundary hysteresis статической зоны

**Связи:** [Q003](OPEN_QUESTIONS.md#q003)/Q004; [F103](RAW_FACTS.md#f103). **Статус:** PROP; не выполнено.

**Решение:** bottom center достаточен, нужны visible ankles/иной viewpoint или другой смысл зоны.

**Входы:** fixed camera/scene_version, утверждённый polygon и semantics, clips прохода/наклона/одной ноги/occluded feet/crowd/перед станком, GT contact и U.

**Шаги:** frozen detections: bbox intersection против bottom center против ankle-any/mean при доступном pose. Не менять semantics «одна стопа» на среднее. Затем actual detector errors. Sweep boundary band только calibration; проверить finite line crossing/direction/track already inside, camera resize/shift invalidation.

**Метрики:** false/missed entry, boundary localization error, delay, unknown coverage, CPU/neural calls.

**Доказательства:** overlays anchor/polygon/GT, source timestamps и predicate traces, calibration/scene config.

**Исходы:** simplest admitted anchor+hysteresis; invisible feet/invalid scene U; pose только при достаточном gain. Успех не доказывает3D volume/руку в механизме либо геометрию другой камеры.

<a id="e007"></a>
### E007 — Метрическая proximity и moving envelope

**Связи:** [Q003](OPEN_QUESTIONS.md#q003)/Q004/Q014; [F039](RAW_FACTS.md#f039)/F046/F104. **Статус:** PROP; не выполнено.

**Решение:** можно ли показывать meters/speed либо только image-zone.

**Входы:** реальные floor correspondences/размеры/контрольные отметки, independent distance/time reference, safe recorded person/equipment trajectories, footprint/heading/рабочий орган; никаких опасных сближений.

**Шаги:** calibration на известных points, held-out контроль near/far/edges; compare footprint/envelope distance vs centers, turn/occlusion/raised fork/different height; perturb calibration/camera pose. Time-correct velocity, body orientation не тождествен motion direction; error budget и domain validity зафиксировать.

**Метрики:** distance p50/p95/max error, threshold crossing FP/FN, speed error, U fraction, missed envelope events, delay.

**Доказательства:** calibration matrix/version/units/distortion procedure, independent reference, overlays/residuals/trajectories, outside-validity cases.

**Исходы:** metric claim лишь в validated region с запасом к ошибке; иначе image ROI и U для метров/3D. Успех не stopping-distance certification, collision prevention или future TTC guarantee.

<a id="e008"></a>
### E008 — Tracker choice на реальной cadence и loss patterns

**Связи:** [Q007](OPEN_QUESTIONS.md#q007)/Q012; [F040](RAW_FACTS.md#f040)–[F042](RAW_FACTS.md#f042)/F105. **Статус:** PROP; не выполнено.

**Решение:** ByteTrack/OC-SORT/BoT-SORT, нужен ли ReID.

**Входы:** одинаковый cached detection stream с low scores, GTactor/event IDs и capture timestamps; measured LinQ cadence после доступа; exact tracker commits/config и ReID artifact.

**Шаги:** одинаковые detections каждому tracker, ReID on/off отдельно. Full cadence, равномерные10/5/2FPS **стресс-режимы**, burst loss/jitter с тем же средним, reconnect и crossing. Tuning только calibration. Все max_age/buffers записывать и в updates, и в physical time; variable dt не включается одним frame_rate.

**Метрики:** IDS/Frag/IDF1/HOTA вместе с event F1/misses/duplicates, transferred wrong PPE state, latency, CPU time и ReID crops/calls.

**Доказательства:** detection cache/version, sampling schedules, track/event ledgers, switches/fragmentation clips, timing и neural budget.

**Исходы:** минимально дорогой вариант при событийных целях; ReID только при demonstrated benefit; ambiguity не переносит уверенный coverage на соседа. Cached benchmark не end-to-end LinQ/network measurement.

<a id="e009"></a>
### E009 — Автомат confirmation/clear/loss/dedup

**Связи:** [Q007](OPEN_QUESTIONS.md#q007)/Q008/Q013; [F106](RAW_FACTS.md#f106)/F107. **Статус:** PROP; не выполнено.

**Решение:** timestamp temporal operator, entry/exit/gap, technical end, dedup/cooldown/merge.

**Входы:** deterministic predicate traces + actual positive/long-negative videos; jitter boundary, one-frame FP, real short intrusion, exit/reentry, stationary, occlusion, IDswitch, scene shift, signal loss/reconnect/out-of-order; GT event semantics согласована.

**Шаги:** trace replay без inference, затем video chain. Compare consecutive, N/M с явным denominator/U, positive supported duration/window, continuous observed duration с max gap. Предлагаемый sweep: confirm0/0.5/1/2s, exit0/0.5/1s, gap0/один expected interval/две expected samples; N/M1/1,2/3,3/5. Это гипотезы, не defaults/нормы. Cooldown сначала off для raw duplicates, потом event-ID delivery suppression и merge separately. Active U не accumulates positive и не observed-clear; technical end censored. New track incarnation не identity continuity автоматически.

**Метрики:** FP/FN/duplicates, short-event miss, confirmation/notification delay, censored end reasons, U fraction, resampling physical-time invariance, event-ID/revision stability.

**Доказательства:** config/version+source-time trace, per-event observed_start/confirmed_at/end_reason, crops/clip, manual expected states и implementation outputs.

**Исходы:** reject stale-confirming/loss-as-clear logic; выбрать tradeoff согласно минимальному important episode/latency. Логически верный автомат не чинит detector/hazard semantics. Узкое Frigate воспроизведение — [E017](OPEN_QUESTIONS.md#e017); это не требование использовать Frigate.

<a id="e010"></a>
### E010 — Typed rule schema и event evaluator acceptance

**Связи:** [Q001](OPEN_QUESTIONS.md#q001)/Q003/Q008/Q014; [F100](RAW_FACTS.md#f100)/F107. **Статус:** PROP; не выполнено.

**Решение:** однозначны ли правила и метрики для полного кейса.

**Входы:** полный case, expert policy, proposed rule/event schema, hand-made GT/predictions: split/merge, wrong actor, two overlapping people, duplicated messages, point-crossing, interval state, censored clip boundary.

**Шаги:** эксперт фиксирует endpoints/applicability. Проверить Strong Kleene AND/NOT и пять counterexamples [F100](RAW_FACTS.md#f100), units/scene/rule versions, unavailable inputs/TTL. Независимо вручную actor-aware one-to-one match; compare evaluator. Point events onset collar отдельно от interval tIoU; thresholds до test, без заимствования DCASE200ms как нормы. Extra duplicate predictions FP, unmatched GT FN.

**Метрики:** annotation ambiguity, evaluator/manual divergence, invalid rules accepted, wrong-actor/duplicate FP; GT/event/negative-hour counts и availability. Live capture→publish latency отдельно от offline observable-onset delay.

**Доказательства:** signed semantics examples/GT contract, hand-calculated matching table, rule validation decisions, exact denominator specification.

**Исходы:** disputed rule disabled/U до clarification, evaluator corrected before CV score. Успех проверяет контракт/учёт, не распознавание. DCASE — audio protocol example, не industrial acceptance standard.

<a id="e011"></a>
### E011 — Paired RGB smoking route selection

**Связи:** [Q004](OPEN_QUESTIONS.md#q004)/Q008/Q009; K002; [F090](RAW_FACTS.md#f090)–[F093](RAW_FACTS.md#f093)/F123. **Статус:** PROP; не выполнено.

**Решение:** object/face ROI baseline A или gesture/object+temporal B, что можно называть confirmed smoking.

**Входы:** original-resolution videos/capture timestamps/camera IDs, GT person/action intervals и cigarette/face/hand visibility, supplied hazardous ROI/material context. Раздельные calibration/test по людям/клипам и held-out camera/view; объём по CI и negative coverage, произвольный universal N не назначен.

**Шаги:** один candidate pool/association/event logic; object-only, gesture-only, object+temporal. Thresholds только calibration. Negatives eat/drink/phone/adjustPPE, pen/tool/finger, pocket/table/cigarette in hand without puff, neighbor smoker, vape, steam/dust/welding, blur/occlusion/IDswitch; include cue без второго cue. Source frame sampling и processed window явно в timestamps. Raw object output и compound S AND H оценивать отдельно. Human-unobservable →U, не forced-negative.

**Метрики:** paired TP retained/lost, FP removed/added, event P/R/F1, FP per negative camera-hour, time-to-first-alert, U/coverage, per-negative-category errors, native/tensor crop sizes, calls/s, p50/p95 total latency.

**Доказательства:** immutable pool+GT, exact model/config/prompt if any, raw detections/pose/association/temporal traces, clips and per-route paired table, timing.

**Исходы:** если human GT не видит cue — observability stop/checkpoint. Если B не улучшает event outcome в latency budget — A+U. Короткий balanced test не заменяет negative camera-hours; успех RGB не transfer nightIR/новая камера и не LinQ compile. Cues/ROI не доказывают фактическое содержимое закрытой ёмкости.

<a id="e012"></a>
### E012 — Дополнительные fall/hook slices с раздельными endpoints

**Связи:** [Q018](OPEN_QUESTIONS.md#q018); K007; [F094](RAW_FACTS.md#f094)–[F096](RAW_FACTS.md#f096)/F124. **Статус:** PROP; не выполнено.

**Решение:** при наличии в полном кейсе поддерживать posture/fall-transition/immobility и какой hook predicate наблюдаем.

**Входы/безопасность:** безопасно разыгранные клипы, без опасных реальных падений; slow/fast intentional lying, kneel/sliding/quadruped, under-machine maintenance, fall-like transition+fast recovery/immobility, occlusion/lost-before. Hook rig с same-geometry attached/unattached/open-gate/occluded pairs и physical GT эксперта, known anchor map; target camera/native crops.

**Шаги:** отдельно GT onset/end transition, lying intervals и post-fall immobility; короткие/закрытые клипы не удалять — U/coverage учитывать. Compare chosen temporal model with posture-only; fast recovery не отменяет observed transition. Hook сначала human observability admission; затем class contract, presence/relationship/open-gate отдельно от mechanical locking/anchor strength. HDS Safe не универсальная метка safety.

**Метрики:** transition recall/latency и intentional-lying confusion отдельно от lying/immobility; missed fast recovery/short clips; hook-state class confusion/precision/recall, U by size/angle, false attachment from mere proximity.

**Доказательства:** separate endpoint GT/timelines, before/during/after clips, physical inspection record и rig pair photos, camera/size/config, uncertainty reasons.

**Исходы:** только readable posture → `person_lying`; temporal evidence → `suspected_fall_transition`; hook only harness visible → harness presence. Unobservable gate →U/не обещать connection. Успех не medical emergency/intent/trauma diagnosis, не anchor load certification и не обязательный сценарий анонса.

<a id="e013"></a>
### E013 — Camera/preprocessing admission и crop/tiles budget

**Связи:** [Q004](OPEN_QUESTIONS.md#q004)/Q007; K004; [F076](RAW_FACTS.md#f076)–[F081](RAW_FACTS.md#f081)/F112/F113/F122. **Статус:** PROP; не выполнено.

**Решение:** supported camera-region/mode и fullframe/crops/tiles при ограниченной нагрузке.

**Входы:** native streams+camera/ROI/scene versions, daycolor/actual nightIR/exposure/gain/codec/bitrate/QP если доступен, exact model preprocessing и timestamps. Paired clear/degraded observations с target size/visibility/action GT; реальные условия отдельно от synthetic resize/codec/blur sweeps.

**Шаги:** измерить source/analytics/native-crop/tensor pixels, letterbox scale и target extent. На одинаковых candidates/GT compare fullframe, bounded original head/person/hand crops, tiles+optional fullframe с merge/NMS. По одному фактору, включая moving vs static PPE, topview, occlusion, steam/dust/process background. Записать number of forwards, batching, P/person refresh, queues; best frames имеют bounded age.

**Метрики:** paired state/event P/R/FA per negative camera-hour, U coverage per predicate/condition, duplicate/miss from tile border/context loss, p50/p95 latency, forwards/s/neural inputs/s и crop budget.

**Доказательства:** source→crop→tensor examples/metadata, frozen splits/preprocess, per-condition errors, workload/latency logs и admitted region/mode list.

**Исходы:** crop помогает лишь при сохранённых native details и приемлемом budget; иначе camera/light/stream/checkpoint или исключённый predicate. Ни upscale, ни synthetic daygrayscale не гарантируют IR/dust/depth/distance transfer. Bosch pre-encoder compression independence не переносится на decoded RTSP. [E003](OPEN_QUESTIONS.md#e003) уточняет per-PPE gate, общий материал можно разделять без выдуманной независимости.

<a id="e014"></a>
### E014 — Reject-only VLM verifier: FP rescue против TP loss

**Связи:** [Q005](OPEN_QUESTIONS.md#q005)/Q006/Q019; K008; [F097](RAW_FACTS.md#f097)–[F099](RAW_FACTS.md#f099)/F115/F125. **Статус:** PROP; не выполнено.

**Решение:** включать suppressor, оставить secondary review либо исключить VLM.

**Входы:** зафиксированный detector+rules baseline, immutable candidate event pool+GT (включая baseline FP и TP), source fullframe/context crop/clip, отдельные camera/clip calibration/test; execution path разрешён по [Q005](OPEN_QUESTIONS.md#q005). Exact model/revision, prompts/settings/parser/output schema и latency instrumentation.

**Шаги:** baseline freeze до VLM. На каждом candidate сохранить event ID, original context и selected frames, exact prompt/raw answer/verdict, model/hash/settings, timing/parser status. Prompt tuning только calibration. Include two people/owner ambiguity, tiny PPE, allowed maintenance lying, reflections/displays, smoke/steam, unknown view, timeouts/decode/schema failures. Повторить одинаковые inputs для answer stability. Enum supported/contradicted/not_visible; failed verification отдельное состояние, не negative.

**Метрики:** paired table baseline TP→accepted/rejected/unverified и FP→accepted/rejected/unverified. FP-rescue count/rate с denominator baselineFP, TP-loss count/rate с denominator baselineTP; после фиксированной failure policy event P/R/FAh, coverage, p50/p95 end-to-end latency, calls/event, accelerator memory. Upstream missed events отдельно: reject-only stage не спасает missing candidate.

**Доказательства:** immutable baseline/pool/split/GT, all raw requests/responses/context, parser outcomes, exact revisions, paired error ledger и timing.

**Исходы/stop:** без acceptable TP loss/latency suppressor не включать; secondary review может показывать uncertainty без подавления. Изменение candidate pool/threshold objective требует отдельного сравнения, Kim adaptive .5→.3 не reject-only evidence. Успех dataset не доказывает full-stream recall или всю neural chain на LinQ. Нельзя обещать FA↓ из самого факта VLM.

<a id="e015"></a>
### E015 — Exact LinQ export/compile/execute/accuracy gates

**Связи:** [Q005](OPEN_QUESTIONS.md#q005)/Q006/Q007/Q020; [F061](RAW_FACTS.md#f061)–[F064](RAW_FACTS.md#f064)/F116–[F118](RAW_FACTS.md#f118). **Статус:** PROP; не выполнено.

**Решение:** какой exact artifact/precision route можно честно обещать на assigned device.

**Входы/доступ:** назначенный hardware/SDK/compiler/runtime/ONNX opset, execution account и proof method; hash графа/checkpoint/class mapping/preprocess/postprocess; reference float outputs и representative calibration/test clips всех critical size/angle/dayIR/crowd slices. Нет подходящих SDK команд — не выдумывать API.

**Шаги:** (1) export/reference correctness; (2) inspect actual ops/shapes/head/decoder boundaries; (3) compile с сохранением report/fallback, не считать compilation запуском; (4) execute с артефактом фактического LinQ исполнения; (5) одинаковые frames raw tensors→detections→tracks→events против reference. Особо small cigarette/head, neck, backlight/IR/blur, keypoint displacement, NMS/score drift; QAT/mixed precision только если реально доступно. RPC/queue/crop throughput измерить отдельно от device inference.

**Метрики:** export/compile/pass и unsupported/fallback operations, execution proof, raw tensor drift, APsmall/coordinate error, false compliance/FAh/event recall, calls and p95 capture→publish latency, availability.

**Доказательства:** artifact hashes, compiler/runtime/device version, exact calibration manifest, compile report/log, execution log/proof, raw output pairs и event ledgers/timing.

**Исходы:** plain detector→cascade/fixed OVD только по прошедшим gate; compiler failure изменить graph, quality failure — calibration/QAT/precision/model/scope согласно доступным опциям. Успех одного checkpoint не whole-family support, один offline run не online SLA. PeopleNet/ViT проценты не предсказывают наш эффект. Все gate в исследовании не выполнялись.

<a id="e016"></a>
### E016 — Респиратор: state против transition на одних клипах

**Связи:** [Q001](OPEN_QUESTIONS.md#q001)/Q002/Q011; K003; [F100](RAW_FACTS.md#f100)/F102. **Статус:** PROP; не выполнено.

**Решение:** поддержать A visibly-uncovered state, B coverage-loss, строгий item-doffing либо ограничить demo.

**Входы:** native target type clips/timestamps с GT C(t), D_item(t), visibility/approved policy, R/Z separately. Wear→remove→neck/hand→rewear, already-uncovered entrance, hidden removal/gaps, duplicate/spare/swap, neighbor item, IDswitch.

**Шаги:** сначала ручная observability/adjudication. Затем A face/head-state и B sequence/item association сравнить на одинаковых clips; B требует достоверного до/после/continuity и item link для строгого D. Снятие одного из двух предметов может дать D=T,C=T,Vppe=F. Blind gap: onset bounds, removalU; stateF отдельно может быть наблюдаем. Нет before-state не forced-negative transition.

**Метрики:** state confusion/false compliance, U/person-time, state/transition event recall, FA/camera-hour, observable-onset delay/bounds, false-removal rate from blind gaps и missing before-state.

**Доказательства:** separate C/D/R/Z timelines, item/part/track association, source frame/clip evidence before/after, gap/adjudication record, model/config and paired outcomes.

**Исходы:** camera читается только state → назвать state; transition включать при endpoint agreement/benefit; face not readable → checkpoint/U. Успех staged videos не plant transfer/fit-seal и не exact item identity во всех occlusions.

<a id="e017"></a>
### E017 — Узкое воспроизведение pinned Frigate ledgers

**Связи:** [Q015](OPEN_QUESTIONS.md#q015)/Q007; K006; [F085](RAW_FACTS.md#f085)–[F088](RAW_FACTS.md#f088). **Статус:** PROP; не выполнено.

**Решение:** подтвердить runtime scope static counter/caller trace и выбрать собственную temporal policy [E009](OPEN_QUESTIONS.md#e009).

**Входы:** окружение Frigate cfa08c56b23d23280c3d0a218e5a43182c97445b/v0.18.2, config/ordinary enabled zone/person/no speed/filter-pass, fps, exact timestamped detections и Norfair state. Среда ещё не запускалась.

**Шаги:** отдельно после constructor: A inertia3/L0 in,out,in,in; B inertia1/fps5/L1s частичный dwell,out,reentry; C prediction-only со last measured inside vs outside, пока tracker возвращает ID; D stationary reuse/no new detector. Добавить removed/end/finished/newID, disabled camera/resolution reset, frame unavailable/queue drop. Не приписывать entry самой тройке in,out,in приI3. Логировать caller gates и фактический neural measurement flag.

**Метрики/наблюдения:** incoming box/centroid/estimate/frame_time/currenttime, P=presence/L=loitering/C=current/E=entered, ID/end_time, update counts/Norfair lifetime; divergence от manual ledger. На собственных videos затем onset/end/duplicates/FAh/censor reasons, не до этого.

**Доказательства:** exact code/config hash, runtime trace/log и video overlays, expected vs actual state ledger, drops/measurement provenance.

**Исходы:** совпало → runtime подтверждён только указанный path; не совпало → уточнить caller/lifetime/filter assumptions и ослабить вывод. Даже совпадение не safety suitability Frigate и не дефект всех релизов; выбор explicit timestamp policy остаётся проектным решением. Это предложенный replay, **не выполненный тест**.
