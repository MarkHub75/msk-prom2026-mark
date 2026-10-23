from pathlib import Path
import re,json
R=Path(__file__).resolve().parent.parent
def put(p,t): (R/p).write_text(t.strip()+'\n',encoding='utf-8')
def links(t):
    # Shared IDs are linked locally and remain understandable when retrieved separately.
    return re.sub(r'(?<![\w/#\[\-])([FSQE]\d{3})(?![\w\]])',lambda m:'['+m[1]+']('+({'F':'RAW_FACTS.md','S':'SOURCES.md','Q':'OPEN_QUESTIONS.md','E':'OPEN_QUESTIONS.md'}[m[1][0]])+'#'+m[1].lower()+')',t)

qs=[
('Q001','P0','Какие СИЗ/типы и части тела действительно обязательны?',
'''Известно: анонс перечисляет примеры, а не полный ТЗ; medical face cover, industrial cartridge, high-vis garment, generic vest и corrective glasses не взаимозаменяемы. Наличие предмета не гарантирует нужное покрытие/защиту. 3M требует fit/seal процедур, недоказуемых обычным RGB. Искали в PPE papers, реальных YAML/JSON, manuals и manufacturer instruction; основания F005/F007/F016/F017/F069/F072/F073/F119.

Неизвестно: approved respirator/glasses/garment types, допустимые альтернативы, нужны ли две перчатки, ремень каски, положения/контексты, где требование активно. Это политика заказчика, а не недостаток нового общего поиска. Решение: taxonomy, labels, отрицательный класс, eligibility и перечень обещаний. Закрытие: полный кейс/ответ эксперта с примерами allowed/disallowed/unknown, затем E001/E003. До ответа неподдерживаемый тип=U. Связь: K001/K003.'''),
('Q002','P0','«Снят респиратор» означает состояние uncovered или наблюдённое снятие?',
'''Известно: видимый респиратор на шее/в руке описывает item, а не отсутствие другого надетого; C=F и item-doffing D различны. Вход человека уже с открытым лицом может нарушать state-rule без наблюдённого transition. Через blind gap можно получить bounds изменения, но не observed removal/точный onset. W2 просмотрел industrial head-state и реальные SH17/R2PPE exports; direct transition artifact не получен. F066–F075/F100/F102.

Неизвестно: нужен именно item-doffing, coverage-loss или состояние, оценивают ли начало клипа без предыстории. Решение: A face-state против B temporal association, GT и neural workload. Закрытие: заказчик фиксирует endpoint, затем E016 с отдельными C(t)/D(t)/visibility. K003. Не требовать нахождения снятого предмета для установления видимого uncovered state.'''),
('Q003','P0','Что означает опасная/горючая зона и условие допуска?',
'''Известно: floor contact, любая часть тела, 3D envelope, direction crossing и proximity — разные предикаты. Bbox overlap не floor occupancy; barrel detection не содержимое/flammability; trackID/цвет жилета не permission. Manuals Frigate/Supervision/DeepStream и monocular proximity прочитаны; F027/F036/F038/F039/F046/F103/F104/F109.

Неизвестно: image floor ROI или dangerous volume, событие входа либо длительное присутствие, предоставлена ли flammable ROI, активность техники/наряд/authorization. Решение: anchor, external inputs, wording, onset и priority. Закрытие: полный кейс + схема сцены от постановщика; E006/E007/E010. При отсутствии внешнего контекста честный output «человек в Z», а необходимые неизвестные предикаты U. K001/K002/K005.'''),
('Q004','P0','Наблюдаемы ли нужные части тела/сигарета в фактических native streams?',
'''Известно: Macroscop/Bosch/Axxon/Domination дают разные product-specific size/angle/FPS units. Невидимое лицо не устанавливает ни presence, ни absence facePPE; real IR не эквивалент grayscale augmentation. Источники F018/F048/F076–F081/F084/F090/F112/F122; журналы W1/W2 проверяли manuals и preprocessing, не камеры кейса.

Неизвестно: исходные resolution/codec/bitrate/exposure/IR, native head/hand/cigarette sizes, topview/occlusion, camera motion, доступность original ROI и checkpoint. Решение: admit camera-region/class, crop/tiles budget, исключение либо другой ракурс. Закрытие: файлы/stream metadata от организаторов + E003/E013 и smoking E011. До этого product minimum не гарантия. K002/K003/K004.'''),
('Q005','P0','Какие нейросетевые этапы обязаны исполняться на LinQ?',
'''Известно только общее условие model inference on LinQ из официального анонса F065; CPU geometry/tracking without ReID/rules не neural inference. Pose, ReID, crop classifier, temporal network и VLM — дополнительные нейроэтапы, F116/F117.

Неизвестно: разрешён ли внешний verifier/локальный auxiliary inference, допустимая граница CPU decode/NMS/postprocess, какие proof artifacts ждут. Поиск публичной LinQ страницы не определяет правила конкретного кейса. Решение: допустимость всей chain и optional VLM. Закрытие: прямой ответ постановщика + linq_platform, зафиксированный execution contract; затем E015. Отсутствие ответа не разрешение обойти обязательный LinQ. K008.'''),
('Q006','P0','Какой exact graph реально compile/execute на назначенном LinQ?',
'''Известно: vendor lists int8/CNN/RNN/yolo5s/yolo8/yolo11 и ONNX/Compiler/DNN Quant, но без checkpoints/shapes/opsets/postprocess boundary. HPS — конкретная линейка; fp16/bfloat16 обозначены перспективой. F063/F064/F114/F116/F117.

Неизвестно: назначенные устройство/SDK/compiler/runtime, artifacts, static/dynamic shapes, attention/3D conv/keypoint heads/QDQ, mixed precision/float outputs/fallback, доступ и RPC. Это не доказанная unsupported возможность. Решение: простой detector против каскада/pose/OVD/VLM. Закрытие: получить SDK/device, предъявить hash и ops конкретного ONNX, выполнить четыре gate E015. Передача linq_platform/model_stack. Ни один export/compile/run в исследовании не выполнен.'''),
('Q007','P0','Каковы source timestamps, jitter, drops и реальная cadence результатов?',
'''Известно: ByteTrack update step и fixed dt не становятся variable-time от frame_rate; Frigate source frames могут не доходить, stationary reuse даёт текущий timestamp без нового neural observation. F040/F041/F085–F088/F105.

Неизвестно: PTS/capture clock, out-of-order handling, реальный LinQ throughput/queue/network cadence, короткие burst losses и latency. Решение: tracker, duration support, max gap/stale TTL, confirmation и измерение delay. Закрытие: linq_platform/video_architecture записывают capture/inference/receive/publish trace; E008/E009/E015. Configured FPS не измерение. K006.'''),
('Q008','P0','Как определены приёмка, знаменатели, latency и unknown?',
'''Известно: itdf требует95/98/90% «достоверности» без достаточного denominator; OIL GEM/2026/B/7902194 quoted7.13 требует90% ideal/80% challenging, встречается вопрос о95%, методика отложена на Design/approval. SAT/signoff запланированы, actual results не получены. F025/F082/F083/F107.

Неизвестно: event/person-frame unit, GT count/split, минимум эпизода, maximum delay/source clock origin, negative camera-hours, FP/duplicate/unknown definitions, excluded cameras, границы occlusion/scene change. Решение: threshold selection, temporal tradeoff и честное демо. Закрытие: постановщик даёт ПМИ либо подписывает E010; evaluation определяет matching/availability/coverage до теста. Чужие проценты не наша цель автоматически. Связь K005; E009/E010/E011/E014.'''),
('Q009','P0','Что именно smoking-positive и наблюдаемый smoking-negative?',
'''Известно: cigarette object, hand-to-mouth, puff/session и smoke — разные cues/units. DAHD/CDPA — image cigarette boxes; Domination face→cigarette manual не раскрывает action window/hard-negative evaluation; clip study16/32frames неоднозначна. Missing cigarette/action не F; S AND H требует совпадающего времени. F051/F090–F093/F100/F108/F123.

Неизвестно: lit cigarette/puff/session/vape, допустимое отрицательное окно, handling concurrent drinking+smoking, длительность important event и hazardous context. Решение: object baseline A против gesture/temporal B, output candidate/confirmed/U. Закрытие: эксперт задаёт GT contract; E011 camera/clip-disjoint paired comparison. K001/K002. Искомая ACM fusion paper403; matched primary industrial route comparison не получено, не объявлено отсутствующим во всём мире.'''),
('Q010','P1','Где actual SH17 extended tags и какой semantic remap нужен данным?',
'''Известно: YAML indices helmet10/hands11/head12/face-mask5 не порядок Table2. Два VOC+два YOLO examples прочитаны; TXT5columns, XML object fields без wearer/on-off/relation. Firefighter helmet off-body и head вне кадра — coverageU. Repo/tree/releases/Kaggle API inspected, inventory partial. F005/F007/F066–F068/F101.

Неизвестно: отдельный extended export/guide и доступный wearer/visibility mapping всего набора; SHWD actual XML/partial-Pictor GT также требуют acceptance. Решение: positive-object-only, relabel/ignore либо готовый state GT. Закрытие: конкретный авторский архив + E001; datasets получает точные field checks. No entry не negative; отсутствие найденного extended asset не доказательство несуществования. K003.'''),
('Q011','P1','Доступны ли industrial neck/hand/removal annotations целевого типа?',
'''Известно: YOLOv8-LPE fulltext даёт industrial3M front/side wear/no_wear/wrong + back_head, но files/guide не получены и neck/hand/transition нет. R2PPE actual123751 annotation schema медицинская, без track/wearer/relation и neck/hand/remove; FMR-DB abstract-only. F069–F075/F102.

Неизвестно: готовые target GT/weights для off-neck/hand и наблюдённого снятия; сколько случаев реально видно нашим камерам. Поиск RU/EN/Chinese и официальных archives завершён точным остатком. Решение: state-only, собственная разметка/съёмка или отказ от B. Закрытие: авторский артефакт либо target clips/экспертные labels, E001/E016. K003. Успех generic mask dataset не закрывает industrial policy.'''),
('Q012','P1','Оправдывает ли pose/HOI цену на target ownership?',
'''Известно: same-detector APkeypoint .675 vs refitDT .664 и direct .663, но APsmall .211 хуже .222/.248; это не crowded ownership accuracy. Containment/one-to-one head matching/pose имеют разные failure modes. F009/F010/F011/F120.

Неизвестно: relation errors при crowd/leaning/held/spare PPE с одинаковыми detections и GTowner/part. Решение: включать ли дополнительный neural stage и какие classes. Закрытие: E002 сначала oracle boxes, затем actual model; calibration/test scene split. Нужны relation labels, не ещё один общий pose обзор.'''),
('Q013','P1','Какая unknown/aging/best-frame политика сохраняет coverage и recall?',
'''Известно: U не negative/safe, stale wearing не current wearing; pure best-score может выбрать единичный FP или старый кадр до снятия. Теория risk–coverage i.i.d. не гарантирует correlated video transfer. F015/F100/F105–F107/F121.

Неизвестно: pause/reset/expire windows, допускаемая age, длительность signal/track loss, условия same-incident return и цена abstention на target stream. Решение: confirmation, technical end/censoring и объём охвата. Закрытие: E004/E005/E009 + operator_product policy; фиксировать FA на observable и scheduled hours с availability. При loss не писать observed_exit.'''),
('Q014','P1','Кто источник hazard_active/authorization, каков TTL/outage?',
'''Известно: person/equipment geometry не даёт equipment activation/permission. Стационарная машина может работать; helmet color/tracker ID не identity/access. F104/F107; источники VMS дают primitives, не готовую factory policy.

Неизвестно: PLC/API/schedule/наряд/СКУД, соответствие человеку, validity interval, отказ внешнего feed. Решение: «в зоне» против «несанкционированно в активной зоне», unknown conjunction и evidence. Закрытие: постановщик и integration contract; E010 проверяет provenance/TTL/invalid rule. Не заменять недоступный feed ложным permission.'''),
('Q015','P1','Каков реальный event effect pinned Frigate ledgers?',
'''Известно: W2 замкнула all counter writes/caller/init/reset/end/new ID и same-commit docs cfa08c56b23d23280c3d0a218e5a43182c97445b. Ordinary-zone counters не обнуляются на out в прочитанном path; zone anchor last measured box, не estimate; stationary reuse может выглядеть fresh. Ручная in,out,in при inertia3 ещё не даёт entry, следующий in даёт. F085–F088.

Неизвестно: runtime Norfair lifetime, actual cadence/queue path и видимые события в выбранной конфигурации. Решение: своя explicit temporal policy, а не сообщение о reproduced bug. Закрытие: E017, затем E009 на собственном GT. K006 static scope закрыт; runtime открыт. Нового общего аудита VMS не нужно.'''),
('Q016','P1','Можно ли получить ПМИ/actual SAT и полный OIL SoW?',
'''Известно: official NIT8p и prebid97p получены,94 numbered content; original SoW hyperlink извлечён из NIT, но download failed. Prebid quotes точны в своём источнике; signed SAT/award/operation metrics не найдены. K005 теперь имеет промышленный procurement chain, но denominator/method deferred. F082–F084/S068/S069.

Неизвестно: полный SoW1786430899.pdf, окончательная версия criteria, accepted quality/FAhours и camera-specific exclusions. Решение: область внешнего практического сравнения и наш запрос к клиенту. Закрытие: получить конкретный документ от OIL/автора/постановщика либо оставить unsupported. Дальнейший сетевой поиск не выполнялся сборщиком. Источник requirement не measurement.'''),
('Q017','P2','Доступны ли целевые RegistryKeys/VMDA таблицы нужной версии?',
'''Известно: S036 metadata/оглавление частично прочитаны, целевой body502/TLS EOF. Snippets VMDA.oneAlarmPerTrack/LongInZoneTimeout2/report_frequency не достаточны для defaults. Искали в W1A/B, exact URLs/logs сохранены.

Неизвестно: surrounding table, версия, units и реальные defaults. Решение: только optional external comparison; базовый event contract не блокируется. Закрытие: получить полный документ и проверить exact page/version либо исключить параметры. Не превращать1/10s/3000ms из индекса в F.'''),
('Q018','P2','Если fall/hook добавлены в кейс, какой endpoint реально нужен?',
'''Известно: Macroscop ищет lying, Lim не распознал малый hook и connection не реализовал; HDS fulltext имеет Wrong place/Safe/Wrong tie/Too thin/Not closed с staged data/split caveat. Temporal fall methods включают свои exclusions и не измеряют fast-recovery отдельно. F049/F050/F054/F094–F096/F124.

Неизвестно: нужен posture, fall-transition, post-fall immobility либо gate/anchor mechanical truth; читается ли hook target camera, physical GT protocol. Решение: не обещать emergency/connection по posture/harness. Закрытие: полный кейс/эксперт, E012; short/occluded/fast-recovery не выбрасывать ради красивой accuracy. W1 C-Q06 fulltext вопрос закрыт W2, но physical endpoint открыт. K007.'''),
('Q019','P2','Даёт ли reject-only VLM verifier paired net benefit?',
'''Известно: NVIDIA VSS3.3.0 operational candidate→clip workflow и failure traces прочитаны; Guo alarm-recheck1068images только abstract claims; Kim fulltext использует each-frame Florence2 + adaptive threshold .5→.3 и precision↓/recall↑, не reject-only matched table. F058/F097–F099/F115/F125.

Неизвестно: наш exact checkpoint/prompt/context, TP lost vs FP rescued, upstream miss, unknown/failure policy, camera-disjoint event metrics и LinQ execution. Решение: suppressor, secondary review или отключить. Закрытие: E014 и Q005/Q006. Прямые каскадные traces существуют; положительный net effect нашей chain не установлен. K008.'''),
('Q020','P1','Как INT8 меняет малые PPE/keypoints и события нашего artifact?',
'''Известно: PTQ4ViT показывает механизм post-softmax/GELU и успешные specialised8bit; PeopleNet example FP32→PTQ/QAT даёт spurious boxes и существенные mAP различия, но не LinQ/YOLO/PPE. F061/F062/F118.

Неизвестно: target calibration representativeness, raw tensor/coordinate drift, confidence/NMS/tracker/event effects, поддержка mixed precision/QAT/float heads. Решение: graph/precision route и фактический promised scope. Закрытие: E015 на exact assigned device с reference frames/GT; class/size/night/crowd slices. Не путать heatmap coordinate discretization с arithmetic INT8 и не переносить чужой процент потери.''')]

experiments=[
('E001','Semantic annotation acceptance до обучения','Q001/Q010/Q011; K001/K003','''**Решение:** использовать export как state/coverage/removal GT, remap/relabel/ignore либо оставить positive objects.

**Входы/доступы:** actual archive+guide/YAML выбранных SHWD/SH17/CHV/Pictor/R2PPE/industrial sources, реальная небольшая стратифицированная выборка: tiny/partial/back/head out-of-frame/on-face/neck/hand/spare/occlusion. Approved-type policy и два независимых разметчика.

**Шаги:** (1) зафиксировать hash/revision и annotation unit; (2) сверить реальные IDs с YAML, а не порядком статьи; (3) проверить поля wearer/track/time/relation/on-off; (4) отдельно разметить item relation, part coverage, visibility, requirement, zone, rule-result; (5) согласовать disagreements и distinguish omission vs visible negative. Специально повторить spare-on-face+off-body и head-out-of-frame counterexamples. Не делать ambiguity negative.

**Метрики/наблюдения:** wrong-unit fraction, taxonomy conflicts, unknown wrongly-negative, adjudicated ambiguity по сценам, field presence и inter-annotator disagreement; universality numeric cutoff не назначен.

**Сохраняемое доказательство:** mapping table, actual sample annotations/crops с разрешённым происхождением, guide locator, disagreement adjudication, hash и decision log.

**Исходы/последствия:** доступный state artifact → перейти к выбранной модели; object-only → собственная coverage/relations разметка; противоречивые labels → relabel/ignore/exclude. Успех не доказывает transfer, лицензии/weights availability или LinQ. W2 уже читала два SH17 примера и R2PPE schema; это узкая инспекция, **не выполненный E001**.'''),
('E002','Ownership на одинаковых detections','Q012; F009/F120','''**Решение:** достаточно geometry или нужен pose/HOI stage для конкретных failure groups.

**Входы:** одна и та же GTowner/part выборка с isolation/crowd crossing/leaning/held/table/spare/donning, person/head/PPE boxes и доступный pose output; calibration и отдельная test-сцена.

**Шаги:** сначала oracle boxes отделяют relation error; сравнить containment/normalized head distance, one-to-one head matching, pose anchors. Затем одинаковый actual detector для full chain. Пороги выбирать на calibration, не на test. Invisible keypoint не считать observed part. Learned HOI добавлять только при actual relation data/export path, не как обязательный третий baseline.

**Метрики:** owner accuracy на resolved links и denominator links, ambiguity/U fraction, false compliance from held/neighbor item, missed violation, ошибки по crowd/pose/native head size, latency и crops/calls per person.

**Доказательства:** immutable detections, relation GT, overlays, assignment traces/threshold/version, paired error examples, timing.

**Исходы:** оставить самый дешёвый вариант при приемлемых event requirements; pose лишь там, где выигрыш подтверждён и цена допустима; ambiguous → U. Постановочные clips не доказывают deployment crowds, oracle stage не end-to-end detector quality.'''),
('E003','Наблюдаемость каждого PPE и empirical supported region','Q001/Q004; F018/F048/F119','''**Решение:** какие camera-region/part/type admitted, нужен ли checkpoint.

**Входы:** native target camera videos, approved PPE/GT; реальные расстояния/ракурсы/dayIR/occlusion, размеры head/face/hands/PPE на source и tensor; controlled degradation только отдельной серией.

**Шаги:** два разметчика отмечают visible positive/visible negative/unobservable. На одном GT сравнить fullframe с native part crop, head-state с face/hand classifier; отдельно helmet/respirator/protective vs corrective glasses/gloves left-right. Добавить neck/hand/spare, unsupported type/visor. Calibration определяет eligibility, held-out camera проверяет область.

**Метрики:** state confusion, violation precision/recall, false compliance, unknown/person-time по size/angle/condition, source/tensor extents, neural input counts. Не заменять реальную дальность synthetic downsample.

**Доказательства:** camera/preprocess metadata, source/crop pairs, visibility GT и reasonsU, frozen gate settings, per-slice tables.

**Исходы:** admitted empirical region, более крупный crop/другой ракурс/checkpoint, либо исключённый predicate. Успех в выбранной size-bin не физический universal threshold и не fit/seal certification. Общий camera workload/crop сравнивает E013; данные можно использовать совместно без двойного счёта измерений.'''),
('E004','Temporal unknown и best-evidence aging','Q002/Q013; F100/F121','''**Решение:** recent evidence windows, pause/reset/expire и stale limits по part.

**Входы:** временные GT/tracks wear→remove→hold→occlude→rewear, already uncovered, pureU/negative, duplicate item, реальные capture timestamps/gaps.

**Шаги:** сравнить per-frame, recent eligible aggregation, quality-selected frames и unknown pause/reset/expiry. Calibration/test split по clip/camera; best frame не выбирается по testGT. Хранить age каждого part, не склеивать incompatible time snapshots. Отдельно correct/ambiguous re-association.

**Метрики:** event precision/recall/FA per negative camera-hour, observable-onset delay, false observed-clear under occlusion, stale age, decision coverage/person-time, evidence interpretability.

**Доказательства:** predicate/evidence selection timelines, timestamps/crops, GT visibility intervals и end reasons, chosen settings.

**Исходы:** policy с объявленным coverage/recall tradeoff; ложное clear при U исключить. Успех synthetic trace не исправляет detector и не доказывает deployment distribution; общий lifecycle проверяется E009.'''),
('E005','Selective prediction и camera/domain shift','Q013; F015/F121','''**Решение:** полезен ли отказ и чем ранжировать eligibility.

**Входы:** calibration camera и unseen held-out camera/shift, T/F/U GT включая unsupported PPE и длительные occlusions.

**Шаги:** ungated, confidence-only, visibility+size, combined gates на одинаковых inputs; freeze thresholds перед test, risk–coverage curves и event consequences. Отдельно OOD и signal loss, весь required person-time остаётся в coverage denominator.

**Метрики:** selective error/coverage, event FA, recall including abstentions, unknown by reason, calibration error и extra neural calls.

**Доказательства:** immutable splits/gates, all-denominator tables, curves, representative rejected/accepted mistakes.

**Исходы:** gate включить при приемлемом реальном tradeoff; иначе корректировать supported region/не маскировать плохой detector почти полным abstention. I.i.d. theorem не гарантия для correlated CCTV или другого цеха.'''),
('E006','Anchor и boundary hysteresis статической зоны','Q003/Q004; F103','''**Решение:** bottom center достаточен, нужны visible ankles/иной viewpoint или другой смысл зоны.

**Входы:** fixed camera/scene_version, утверждённый polygon и semantics, clips прохода/наклона/одной ноги/occluded feet/crowd/перед станком, GT contact и U.

**Шаги:** frozen detections: bbox intersection против bottom center против ankle-any/mean при доступном pose. Не менять semantics «одна стопа» на среднее. Затем actual detector errors. Sweep boundary band только calibration; проверить finite line crossing/direction/track already inside, camera resize/shift invalidation.

**Метрики:** false/missed entry, boundary localization error, delay, unknown coverage, CPU/neural calls.

**Доказательства:** overlays anchor/polygon/GT, source timestamps и predicate traces, calibration/scene config.

**Исходы:** simplest admitted anchor+hysteresis; invisible feet/invalid scene U; pose только при достаточном gain. Успех не доказывает3D volume/руку в механизме либо геометрию другой камеры.'''),
('E007','Метрическая proximity и moving envelope','Q003/Q004/Q014; F039/F046/F104','''**Решение:** можно ли показывать meters/speed либо только image-zone.

**Входы:** реальные floor correspondences/размеры/контрольные отметки, independent distance/time reference, safe recorded person/equipment trajectories, footprint/heading/рабочий орган; никаких опасных сближений.

**Шаги:** calibration на известных points, held-out контроль near/far/edges; compare footprint/envelope distance vs centers, turn/occlusion/raised fork/different height; perturb calibration/camera pose. Time-correct velocity, body orientation не тождествен motion direction; error budget и domain validity зафиксировать.

**Метрики:** distance p50/p95/max error, threshold crossing FP/FN, speed error, U fraction, missed envelope events, delay.

**Доказательства:** calibration matrix/version/units/distortion procedure, independent reference, overlays/residuals/trajectories, outside-validity cases.

**Исходы:** metric claim лишь в validated region с запасом к ошибке; иначе image ROI и U для метров/3D. Успех не stopping-distance certification, collision prevention или future TTC guarantee.'''),
('E008','Tracker choice на реальной cadence и loss patterns','Q007/Q012; F040–F042/F105','''**Решение:** ByteTrack/OC-SORT/BoT-SORT, нужен ли ReID.

**Входы:** одинаковый cached detection stream с low scores, GTactor/event IDs и capture timestamps; measured LinQ cadence после доступа; exact tracker commits/config и ReID artifact.

**Шаги:** одинаковые detections каждому tracker, ReID on/off отдельно. Full cadence, равномерные10/5/2FPS **стресс-режимы**, burst loss/jitter с тем же средним, reconnect и crossing. Tuning только calibration. Все max_age/buffers записывать и в updates, и в physical time; variable dt не включается одним frame_rate.

**Метрики:** IDS/Frag/IDF1/HOTA вместе с event F1/misses/duplicates, transferred wrong PPE state, latency, CPU time и ReID crops/calls.

**Доказательства:** detection cache/version, sampling schedules, track/event ledgers, switches/fragmentation clips, timing и neural budget.

**Исходы:** минимально дорогой вариант при событийных целях; ReID только при demonstrated benefit; ambiguity не переносит уверенный coverage на соседа. Cached benchmark не end-to-end LinQ/network measurement.'''),
('E009','Автомат confirmation/clear/loss/dedup','Q007/Q008/Q013; F106/F107','''**Решение:** timestamp temporal operator, entry/exit/gap, technical end, dedup/cooldown/merge.

**Входы:** deterministic predicate traces + actual positive/long-negative videos; jitter boundary, one-frame FP, real short intrusion, exit/reentry, stationary, occlusion, IDswitch, scene shift, signal loss/reconnect/out-of-order; GT event semantics согласована.

**Шаги:** trace replay без inference, затем video chain. Compare consecutive, N/M с явным denominator/U, positive supported duration/window, continuous observed duration с max gap. Предлагаемый sweep: confirm0/0.5/1/2s, exit0/0.5/1s, gap0/один expected interval/две expected samples; N/M1/1,2/3,3/5. Это гипотезы, не defaults/нормы. Cooldown сначала off для raw duplicates, потом event-ID delivery suppression и merge separately. Active U не accumulates positive и не observed-clear; technical end censored. New track incarnation не identity continuity автоматически.

**Метрики:** FP/FN/duplicates, short-event miss, confirmation/notification delay, censored end reasons, U fraction, resampling physical-time invariance, event-ID/revision stability.

**Доказательства:** config/version+source-time trace, per-event observed_start/confirmed_at/end_reason, crops/clip, manual expected states и implementation outputs.

**Исходы:** reject stale-confirming/loss-as-clear logic; выбрать tradeoff согласно минимальному important episode/latency. Логически верный автомат не чинит detector/hazard semantics. Узкое Frigate воспроизведение — E017; это не требование использовать Frigate.'''),
('E010','Typed rule schema и event evaluator acceptance','Q001/Q003/Q008/Q014; F100/F107','''**Решение:** однозначны ли правила и метрики для полного кейса.

**Входы:** полный case, expert policy, proposed rule/event schema, hand-made GT/predictions: split/merge, wrong actor, two overlapping people, duplicated messages, point-crossing, interval state, censored clip boundary.

**Шаги:** эксперт фиксирует endpoints/applicability. Проверить Strong Kleene AND/NOT и пять counterexamples F100, units/scene/rule versions, unavailable inputs/TTL. Независимо вручную actor-aware one-to-one match; compare evaluator. Point events onset collar отдельно от interval tIoU; thresholds до test, без заимствования DCASE200ms как нормы. Extra duplicate predictions FP, unmatched GT FN.

**Метрики:** annotation ambiguity, evaluator/manual divergence, invalid rules accepted, wrong-actor/duplicate FP; GT/event/negative-hour counts и availability. Live capture→publish latency отдельно от offline observable-onset delay.

**Доказательства:** signed semantics examples/GT contract, hand-calculated matching table, rule validation decisions, exact denominator specification.

**Исходы:** disputed rule disabled/U до clarification, evaluator corrected before CV score. Успех проверяет контракт/учёт, не распознавание. DCASE — audio protocol example, не industrial acceptance standard.'''),
('E011','Paired RGB smoking route selection','Q004/Q008/Q009; K002; F090–F093/F123','''**Решение:** object/face ROI baseline A или gesture/object+temporal B, что можно называть confirmed smoking.

**Входы:** original-resolution videos/capture timestamps/camera IDs, GT person/action intervals и cigarette/face/hand visibility, supplied hazardous ROI/material context. Раздельные calibration/test по людям/клипам и held-out camera/view; объём по CI и negative coverage, произвольный universal N не назначен.

**Шаги:** один candidate pool/association/event logic; object-only, gesture-only, object+temporal. Thresholds только calibration. Negatives eat/drink/phone/adjustPPE, pen/tool/finger, pocket/table/cigarette in hand without puff, neighbor smoker, vape, steam/dust/welding, blur/occlusion/IDswitch; include cue без второго cue. Source frame sampling и processed window явно в timestamps. Raw object output и compound S AND H оценивать отдельно. Human-unobservable →U, не forced-negative.

**Метрики:** paired TP retained/lost, FP removed/added, event P/R/F1, FP per negative camera-hour, time-to-first-alert, U/coverage, per-negative-category errors, native/tensor crop sizes, calls/s, p50/p95 total latency.

**Доказательства:** immutable pool+GT, exact model/config/prompt if any, raw detections/pose/association/temporal traces, clips and per-route paired table, timing.

**Исходы:** если human GT не видит cue — observability stop/checkpoint. Если B не улучшает event outcome в latency budget — A+U. Короткий balanced test не заменяет negative camera-hours; успех RGB не transfer nightIR/новая камера и не LinQ compile. Cues/ROI не доказывают фактическое содержимое закрытой ёмкости.'''),
('E012','Дополнительные fall/hook slices с раздельными endpoints','Q018; K007; F094–F096/F124','''**Решение:** при наличии в полном кейсе поддерживать posture/fall-transition/immobility и какой hook predicate наблюдаем.

**Входы/безопасность:** безопасно разыгранные клипы, без опасных реальных падений; slow/fast intentional lying, kneel/sliding/quadruped, under-machine maintenance, fall-like transition+fast recovery/immobility, occlusion/lost-before. Hook rig с same-geometry attached/unattached/open-gate/occluded pairs и physical GT эксперта, known anchor map; target camera/native crops.

**Шаги:** отдельно GT onset/end transition, lying intervals и post-fall immobility; короткие/закрытые клипы не удалять — U/coverage учитывать. Compare chosen temporal model with posture-only; fast recovery не отменяет observed transition. Hook сначала human observability admission; затем class contract, presence/relationship/open-gate отдельно от mechanical locking/anchor strength. HDS Safe не универсальная метка safety.

**Метрики:** transition recall/latency и intentional-lying confusion отдельно от lying/immobility; missed fast recovery/short clips; hook-state class confusion/precision/recall, U by size/angle, false attachment from mere proximity.

**Доказательства:** separate endpoint GT/timelines, before/during/after clips, physical inspection record и rig pair photos, camera/size/config, uncertainty reasons.

**Исходы:** только readable posture → `person_lying`; temporal evidence → `suspected_fall_transition`; hook only harness visible → harness presence. Unobservable gate →U/не обещать connection. Успех не medical emergency/intent/trauma diagnosis, не anchor load certification и не обязательный сценарий анонса.'''),
('E013','Camera/preprocessing admission и crop/tiles budget','Q004/Q007; K004; F076–F081/F112/F113/F122','''**Решение:** supported camera-region/mode и fullframe/crops/tiles при ограниченной нагрузке.

**Входы:** native streams+camera/ROI/scene versions, daycolor/actual nightIR/exposure/gain/codec/bitrate/QP если доступен, exact model preprocessing и timestamps. Paired clear/degraded observations с target size/visibility/action GT; реальные условия отдельно от synthetic resize/codec/blur sweeps.

**Шаги:** измерить source/analytics/native-crop/tensor pixels, letterbox scale и target extent. На одинаковых candidates/GT compare fullframe, bounded original head/person/hand crops, tiles+optional fullframe с merge/NMS. По одному фактору, включая moving vs static PPE, topview, occlusion, steam/dust/process background. Записать number of forwards, batching, P/person refresh, queues; best frames имеют bounded age.

**Метрики:** paired state/event P/R/FA per negative camera-hour, U coverage per predicate/condition, duplicate/miss from tile border/context loss, p50/p95 latency, forwards/s/neural inputs/s и crop budget.

**Доказательства:** source→crop→tensor examples/metadata, frozen splits/preprocess, per-condition errors, workload/latency logs и admitted region/mode list.

**Исходы:** crop помогает лишь при сохранённых native details и приемлемом budget; иначе camera/light/stream/checkpoint или исключённый predicate. Ни upscale, ни synthetic daygrayscale не гарантируют IR/dust/depth/distance transfer. Bosch pre-encoder compression independence не переносится на decoded RTSP. E003 уточняет per-PPE gate, общий материал можно разделять без выдуманной независимости.'''),
('E014','Reject-only VLM verifier: FP rescue против TP loss','Q005/Q006/Q019; K008; F097–F099/F115/F125','''**Решение:** включать suppressor, оставить secondary review либо исключить VLM.

**Входы:** зафиксированный detector+rules baseline, immutable candidate event pool+GT (включая baseline FP и TP), source fullframe/context crop/clip, отдельные camera/clip calibration/test; execution path разрешён по Q005. Exact model/revision, prompts/settings/parser/output schema и latency instrumentation.

**Шаги:** baseline freeze до VLM. На каждом candidate сохранить event ID, original context и selected frames, exact prompt/raw answer/verdict, model/hash/settings, timing/parser status. Prompt tuning только calibration. Include two people/owner ambiguity, tiny PPE, allowed maintenance lying, reflections/displays, smoke/steam, unknown view, timeouts/decode/schema failures. Повторить одинаковые inputs для answer stability. Enum supported/contradicted/not_visible; failed verification отдельное состояние, не negative.

**Метрики:** paired table baseline TP→accepted/rejected/unverified и FP→accepted/rejected/unverified. FP-rescue count/rate с denominator baselineFP, TP-loss count/rate с denominator baselineTP; после фиксированной failure policy event P/R/FAh, coverage, p50/p95 end-to-end latency, calls/event, accelerator memory. Upstream missed events отдельно: reject-only stage не спасает missing candidate.

**Доказательства:** immutable baseline/pool/split/GT, all raw requests/responses/context, parser outcomes, exact revisions, paired error ledger и timing.

**Исходы/stop:** без acceptable TP loss/latency suppressor не включать; secondary review может показывать uncertainty без подавления. Изменение candidate pool/threshold objective требует отдельного сравнения, Kim adaptive .5→.3 не reject-only evidence. Успех dataset не доказывает full-stream recall или всю neural chain на LinQ. Нельзя обещать FA↓ из самого факта VLM.'''),
('E015','Exact LinQ export/compile/execute/accuracy gates','Q005/Q006/Q007/Q020; F061–F064/F116–F118','''**Решение:** какой exact artifact/precision route можно честно обещать на assigned device.

**Входы/доступ:** назначенный hardware/SDK/compiler/runtime/ONNX opset, execution account и proof method; hash графа/checkpoint/class mapping/preprocess/postprocess; reference float outputs и representative calibration/test clips всех critical size/angle/dayIR/crowd slices. Нет подходящих SDK команд — не выдумывать API.

**Шаги:** (1) export/reference correctness; (2) inspect actual ops/shapes/head/decoder boundaries; (3) compile с сохранением report/fallback, не считать compilation запуском; (4) execute с артефактом фактического LinQ исполнения; (5) одинаковые frames raw tensors→detections→tracks→events против reference. Особо small cigarette/head, neck, backlight/IR/blur, keypoint displacement, NMS/score drift; QAT/mixed precision только если реально доступно. RPC/queue/crop throughput измерить отдельно от device inference.

**Метрики:** export/compile/pass и unsupported/fallback operations, execution proof, raw tensor drift, APsmall/coordinate error, false compliance/FAh/event recall, calls and p95 capture→publish latency, availability.

**Доказательства:** artifact hashes, compiler/runtime/device version, exact calibration manifest, compile report/log, execution log/proof, raw output pairs и event ledgers/timing.

**Исходы:** plain detector→cascade/fixed OVD только по прошедшим gate; compiler failure изменить graph, quality failure — calibration/QAT/precision/model/scope согласно доступным опциям. Успех одного checkpoint не whole-family support, один offline run не online SLA. PeopleNet/ViT проценты не предсказывают наш эффект. Все gate в исследовании не выполнялись.'''),
('E016','Респиратор: state против transition на одних клипах','Q001/Q002/Q011; K003; F100/F102','''**Решение:** поддержать A visibly-uncovered state, B coverage-loss, строгий item-doffing либо ограничить demo.

**Входы:** native target type clips/timestamps с GT C(t), D_item(t), visibility/approved policy, R/Z separately. Wear→remove→neck/hand→rewear, already-uncovered entrance, hidden removal/gaps, duplicate/spare/swap, neighbor item, IDswitch.

**Шаги:** сначала ручная observability/adjudication. Затем A face/head-state и B sequence/item association сравнить на одинаковых clips; B требует достоверного до/после/continuity и item link для строгого D. Снятие одного из двух предметов может дать D=T,C=T,Vppe=F. Blind gap: onset bounds, removalU; stateF отдельно может быть наблюдаем. Нет before-state не forced-negative transition.

**Метрики:** state confusion/false compliance, U/person-time, state/transition event recall, FA/camera-hour, observable-onset delay/bounds, false-removal rate from blind gaps и missing before-state.

**Доказательства:** separate C/D/R/Z timelines, item/part/track association, source frame/clip evidence before/after, gap/adjudication record, model/config and paired outcomes.

**Исходы:** camera читается только state → назвать state; transition включать при endpoint agreement/benefit; face not readable → checkpoint/U. Успех staged videos не plant transfer/fit-seal и не exact item identity во всех occlusions.'''),
('E017','Узкое воспроизведение pinned Frigate ledgers','Q015/Q007; K006; F085–F088','''**Решение:** подтвердить runtime scope static counter/caller trace и выбрать собственную temporal policy E009.

**Входы:** окружение Frigate cfa08c56b23d23280c3d0a218e5a43182c97445b/v0.18.2, config/ordinary enabled zone/person/no speed/filter-pass, fps, exact timestamped detections и Norfair state. Среда ещё не запускалась.

**Шаги:** отдельно после constructor: A inertia3/L0 in,out,in,in; B inertia1/fps5/L1s частичный dwell,out,reentry; C prediction-only со last measured inside vs outside, пока tracker возвращает ID; D stationary reuse/no new detector. Добавить removed/end/finished/newID, disabled camera/resolution reset, frame unavailable/queue drop. Не приписывать entry самой тройке in,out,in приI3. Логировать caller gates и фактический neural measurement flag.

**Метрики/наблюдения:** incoming box/centroid/estimate/frame_time/currenttime, P=presence/L=loitering/C=current/E=entered, ID/end_time, update counts/Norfair lifetime; divergence от manual ledger. На собственных videos затем onset/end/duplicates/FAh/censor reasons, не до этого.

**Доказательства:** exact code/config hash, runtime trace/log и video overlays, expected vs actual state ledger, drops/measurement provenance.

**Исходы:** совпало → runtime подтверждён только указанный path; не совпало → уточнить caller/lifetime/filter assumptions и ослабить вывод. Даже совпадение не safety suitability Frigate и не дефект всех релизов; выбор explicit timestamp policy остаётся проектным решением. Это предложенный replay, **не выполненный тест**.''')]

header='''# OPEN_QUESTIONS — violation_methods

Состояние после двух исследовательских волн и сборки:2026-10-23, Europe/Moscow (+03:00). Полный кейс, native видео, назначенные LinQ hardware/SDK и программа приёмки не предоставлены. Нового поиска сборщик не выполнял. Вопросы ниже не скрытая третья волна: указан конкретный способ закрытия после получения артефакта/доступа/ответа/практической проверки.

**Все E001–E017 — предлагаемые процедуры, ни один E не выполнен.** В волнах читались документы/код/metadata и отдельные XML/JSON/изображения; это не model benchmark, не полный semantic acceptance и не runtime VMS test. Связанные E могут использовать один набор клипов/GT, но отвечают разным решениям и не считаются независимыми измерениями.

## Короткая P0-группа для первого контакта

1. Q001/Q002: обязательные СИЗ и approved types; «снят» как state или transition; что делать без предыстории.
2. Q003/Q009: смысл зоны/flammable context/smoking-positive и наблюдаемого negative; activation/authorization.
3. Q004: original streams, camera modes/ракурсы/native target size, возможен ли checkpoint.
4. Q005/Q006: граница всех neural stages на LinQ и exact назначенный hardware/SDK/artifact proof.
5. Q007/Q008: timestamps/cadence и acceptance unit, minimal episode/max delay, FP/duplicates/unknown/negative hours.

Первые15–20минут после кейса:0–4мин выписать обязательные endpoints/метрики/политику;4–8мин проверить глазами native face/head/feet/cigarette и camera mode;8–12мин сопоставить каждому endpoint простой method+U gate и missing inputs;12–16мин предъявить exact graph/access вопросы LinQ;16–20мин выбрать admitted scope/fallbacks и вопросы первого чек-поинта. Это предлагаемый маршрут, не обещание реализовать chain за20минут. Подробная карта — [_WORK/COLLECTOR_HANDOFF.md](_WORK/COLLECTOR_HANDOFF.md).

## Подробные вопросы
'''
out=[links(header)]
for q,p,title,body in qs:
    out += [f'<a id="{q.lower()}"></a>\n### {q} — {title}',f'**Приоритет:**{p}. **Статус:** открыто в указанной области; факты и границы поиска ниже.',links(body)]
out+=['## Полные процедуры практической волны','Все параметры sweeps ниже — **PROP**. Чужие vendor defaults сохраняются в RAW_FACTS и не становятся рекомендованными порогами. Thresholds выбираются calibration/по policy, test не используется для подгонки. Сохраняются source-time, actor association, unknown/availability и знаменатели. Ни один эксперимент не выполнен.']
for e,title,related,body in experiments:
    out += [f'<a id="{e.lower()}"></a>\n### {e} — {title}',links('**Связи:** '+related+'. **Статус:** PROP; не выполнено.'),links(body)]
put('OPEN_QUESTIONS.md','\n\n'.join(out))

critic=R/'CRITIC.md'
text=critic.read_text(encoding='utf-8-sig')
marker='## Добавление COLLECTOR: результаты двух волн'
if marker in text: text=text.split(marker)[0].rstrip()
add='''

## Добавление COLLECTOR: результаты двух волн

Дата сборки:2026-10-23, Europe/Moscow(+03:00). Исходный текст критики выше сохранён без ретроспективной правки. Ниже обработка реальных W2_A/B/C, а не финальный аудит или новая исследовательская волна. Новых сетевых запросов, моделей и подагентов сборщик не выполнял; все E остаются предложениями.

<a id="k001"></a>
### K001 — закрыто семантически; качество получения предикатов не измерено

W2_A разделила item observation и target coverage; coverageT может дать любой надетый approved item, spare off-body не даёт coverageF. Полные Strong Kleene AND/NOT таблицы факторизуют27 C/R/Z и81 с action; пять ручных counterexamples разобраны. F100/F102/F119, источники S007/S008 и локальный counterexample F067. W1_C фраза «ни action, ни нарушение зоны не подтверждены→compliant» **superseded**. Missing cue→U, F compound-rule не global compliance; observed negative требует отдельного контракта. Остаток Q001/Q008/Q009/Q013; E001/E010/E011/E016. Ручные логические трассы не benchmark.

<a id="k002"></a>
### K002 — область существенно уточнена; matched route benefit открыт

W2_C получила parsed primary RGB Domination1.17 §8.8 (F090/S072, visual QA недоступна), две fulltext cigarette object работы (F091/F092), pinned fusion code с global history/first boxes/no ownership (F093). Это обосновывает условный face/object route и ограничение scene/face size, а также опровергает автоматический вывод из слова smoking/temporal. Product optimum100px не universal minimum; thermal TP-LINK5–10m остаётся иной модальностью. Matched object/gesture/object+temporal test с eat/drink/phone/adjustPPE, camera-disjoint и eventFP denominator не получен. Методический выбор F123; Q004/Q009, E011. Нельзя ранжировать маршруты по AP несопоставимых cigarette images.

<a id="k003"></a>
### K003 — состояние/transition и actual artifact уточнены; industrial off-neck/hand/removal остаётся открытым

W2_A реально прочитала2VOC+2YOLO SH17 и off-body image (F066–F068), article/YAML mapping (F007), industrial3M head-state fulltext (F069/F070), R2PPE guide+actualJSON (F072/F073). Статья extended и base export разнесены; не заявляется, что tags нигде нет. Medical mask/R2PPE healthcare не cartridge workshop. Source files промышленной head-state не получены, neck/hand/transition GT отсутствует в полученном материале. F101/F102 дают два маршрута A visible uncovered state/B observed transition, stop при невидимом лице/нет before-state/IDswitch; item-doffing отдельно от coverage-loss. Q001/Q002/Q010/Q011, E001/E003/E016. K003 не закрыто обещанием готовой модели или LinQ.

<a id="k004"></a>
### K004 — первичные условия среды усилены; target degradation curves неизвестны

W2_B добавила independent Axxon VL4.5 manual conditions (F076/F077), Axis nearIR/blur/compression (F078), Bosch pre-encoder boundary (F079), Frigate upscale developer claim и resize code (F080/F081), industrial OIL survey/remediation/dispute/exclusions (F084). Symptom→compensation→abstain table F122 задаёт проверку, не достигнутую компенсацию. RGB/NIR/thermal не смешиваются, source/native/tensor pixels разнесены. Прямых measured PPE dust/steam/topview curves и качества камер кейса нет. Q004, E003/E013. Числа manuals — свойства версии, не наши admission guarantees.

<a id="k005"></a>
### K005 — industrial procurement chain найдена; приёмочная формула/результаты открыты

Oil India Limited GEM/2026/B/7902194 от11.08.2026: official NIT8p и prebid meeting25.08, published01.10.2026,97p/94numbered content получены (S068/S069,F082–F084). Quoted SoW7.13 требует90% ideal/80% challenging, вопрос о95% не снимает неопределённость. Ответы оставляют per-use-case Design/approval и SAT/UAT criteria during implementation. Full SoW по hyperlink не получен; signed SAT/achieved performance/FAhours нет. Это частичное закрытие industrial customer→procurement→acceptance planning, не доказательство90/95% работы. Q008/Q016,E010. itdf остаётся grant КД-ТЗ; DCASE — audio matching example, не CCTV standard.

<a id="k006"></a>
### K006 — pinned static chain закрыта в указанном scope; runtime effect открыт

W2_B прочитала all writes, caller/Norfair/stationary reuse/init/reset/end/newID и same-commit docs cfa08c56b23d23280c3d0a218e5a43182c97445b. F085–F088/S070 содержат точные ledgers/строки. Out сохраняет presence P, не reset; ordinary zone читает last measured box, **не estimate**. Timestamp equality может возникнуть от stationary reuse без нового detector invocation. In,out,in при inertia3 само ещё не entry; следующий in даёт entry в описанных условиях. Новая incarnation имеет чистые counters; removed/end не observed_exit. Это статическое DOC/CODE расхождение с ручными трассами, **не воспроизведённый runtimebug**. Q007/Q015,E017/E009. Actual Norfair lifetime/cadence/queue impact не измерены.

<a id="k007"></a>
### K007 — чрезмерное обобщение исправлено; case-specific endpoint/physical GT открыты

W2_C fulltext HDS (F094/S076) различает exact Wrong place/Safe/Wrong tie/Too thin/Not closed, а не только presence.9738 после augmentation8:1:1 не доказывает source-disjoint split; physical gate-lock/anchor protocol не дан. Поэтому не утверждаем, что attachment vision вообще не решают, но не раскрываем Safe в механическую сертификацию. Temporal fall Iazzi/Núñez-Marcos (F095/F096) имеют разные endpoints/exclusions/units. W1 требование устойчивого последующего lying **superseded**: fast recovery не отменяет observed transition, lying/immobility отдельно (F124). Q018,E012; необязательная ветка не расширяет автоматически анонс.

<a id="k008"></a>
### K008 — direct cascade traces найдены; net benefit нашего verifier открыт

W2_C получила NVIDIA VSS3.3.0 candidate→clip workflow/parser/timeout failure trace (F099/S081), Guo industrial recheck abstract (F098/S080) и Kim fulltext (F097/S079). Поэтому direct traces существуют; утверждение «paired evidence нет вообще» слишком широко. Guo numbers abstract-only без TP-loss/split audit; Kim each-frame Florence2/adaptive YOLO threshold .5→.3 повышает recall ценой precision, не reject-only rescue table. F125/Q019/E014 задают paired baseline TP/FP→accepted/rejected/unverified, upstream recall и latency; Q005/Q006 сохраняют LinQ boundary. Detector+rules остаётся baseline, verifier optional по измерению. Ни FA↓, ни пригодность LinQ не установлены.

### Результат сборки для дальнейших ролей

Нормализованы81S и125F,20Q и17E; повторные чтения одной цепочки не стали независимыми экспериментами. Полные процедуры находятся в OPEN_QUESTIONS.md; source/fact registry — SOURCES.md/RAW_FACTS.md. Полные old→new mapping и author handoff — _WORK/ID_MAP.md и _WORK/COLLECTOR_HANDOFF.md. Приоритет доказательств и W2 supersession явно заданы. Ни один E не выполнен; новое неизвестное после двух волн передано Q, скрытой третьей волны нет.
'''
critic.write_text(text.rstrip()+'\n\n'+links(add).strip()+'\n',encoding='utf-8')
print('OPEN_QUESTIONS and appended CRITIC written; 20 Q / 17 E.')
