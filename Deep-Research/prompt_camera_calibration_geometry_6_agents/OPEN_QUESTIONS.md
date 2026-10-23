# Открытые вопросы и следующая практическая работа

Все вопросы относятся к `camera_calibration_geometry`. Они получены после **одной** волны шести исследователей и синтеза оркестратора. Это не поручения внешним людям: сообщения организаторам/авторам не отправлялись. Все E001–E010 ниже — **предлагаемые и не выполненные** эксперименты. Фактически выполненный небольшой аналитический расчёт описан отдельно в [F004–F006](RAW_FACTS.md#f004).

## Сначала получить пять входов

1. **Q001:** официальный кейс, точные определения событий и оцениваемые метрики.
2. **Q002:** измеренные XY пола и физически другие независимые controls.
3. **Q003/Q004:** исходное видео, coordinate chain, PTS и смысл требования к FPS/latency.
4. **Q005:** фактические правила CPU postprocessing, SDK/model outputs и серверная среда LinQ.
5. **Q006/Q007:** наблюдаемость контактов, machine state и разрешённые операции.

Без Q002 остаётся image-zone MVP; без temporal/identity quality нельзя честно включать metric speed; без Q005 путь исполнения остаётся архитектурной гипотезой.

## Реестр вопросов

| ID / приоритет | Точный вопрос | Что известно и почему ответа нет | Решение и способ закрытия |
|---|---|---|---|
| **Q001 / P0** | Как PDF кейса определяет бег, сближение, «под грузом», падение, нарушения зон и итоговую метрику? | Вход содержит пересказ/список сценариев, PDF отсутствует: F002/F003, K001/K005 | Получить актуальный официальный файл и экспертную онтологию labels; выбрать fast-motion vs running, configured zone vs actual under-load; не заменять их общими классами объектов |
| **Q002 / P0** | Есть ли для каждой камеры 4+ невырожденных measured XY пола и отдельные контрольные точки/отрезки, с точностью survey? | Теория/API установлены, размеров сцены нет: F021/F022/F030, K002 | Артефакт/обследование: таблица XY+units+plane membership, фото/план, отдельный hold-out; E002. При отсутствии — отключить метры |
| **Q003 / P0** | Что именно считается raw/analysis изображением: resolution, rotation, crop, sensor mode, letterbox, dewarping, K/D/Knew, zoom/PTZ? | Контракт нужен, конкретный pipeline неизвестен: F023/F038/F040 | Видео+metadata+one-frame overlay детекций и контролей; подтвердить inverse preprocessing ровно один раз. E002/E007 |
| **Q004 / P0** | «1 FPS» — throughput или выбранные source frames? Каковы source PTS, VFR/freeze/resets и допустимые event latency/длительности? | F007–F017 различают режимы, но записи нет; K004 | Получить исходник без transcode, ffprobe metadata (F020), clock contract и ответ эксперта; E004/E006. Меняет sampling/window/online claim |
| **Q005 / P0** | Разрешены ли CPU tracking/geometry после LinQ, какие outputs и execution artifacts даёт SDK, каковы OS/Python/CPU/memory/runtime? | Только пересказ сервера, ни SDK, ни правила не прочитаны: F002/F078 | Официальный документ+реальный SDK example/device session; E001/E010. Не выдумывать interface/paths и не считать CPU neural model обычной геометрией |
| **Q006 / P0** | Видны ли стопы/колёса и что означает bbox при occlusion: visible-only или full-body prediction? | Reference-point bias установлен, свой материал отсутствует: F026/F065 | Репрезентативные кадры и paired annotations contact/visibility/bbox semantics, E003; выбрать bbox/pose/segmentation и abstention gates |
| **Q007 / P0** | Для каждой зоны известны active/maintenance/isolation/guard state, разрешённые операции/роли и источник их времени? | Proximity не равно violation: F043/F053/F055 | Эксперт участка, state API или подтверждённый ввод с provenance; normal-work videos. E005. Unknown state не подменять запретом/разрешением без явной policy |
| **Q008 / P1** | Можно ли получить форму/размеры/anchor/heading/груз погрузчика, включая reverse/rear swing/выступающие вилы? | Formula footprint есть, physical inputs нет: F047–F051 | Survey/паспорт/разметка видимых ground anchors, E008; при отсутствии — corridor/conservative candidate либо отказ от metric moving-gap |
| **Q009 / P0** | Каковы допустимые ошибки позиции/зазора/скорости, event recall, FAR, latency и минимальный coverage у каждого правила? | Нет universal thresholds; F041/F077 | Эксперт и команда согласуют budgets до tuning/test с учётом цены ошибок; E002–E008. Результат задаёт mask, пороги и название функции |
| **Q010 / P1** | Каковы реальная вибрация/zoom/PTZ и доступные неподвижные anchors для drift checks? | ECC/fiducial route документирован, камера не видна: F037/F038 | Спокойное видео и контролируемые изменения профиля/положения; E007. Решение: fixed profile/presets/suspend, не обещание автоисправления |
| **Q011 / P1** | Есть ли высоты/плоскости платформ, конвейерный просвет, load geometry/telemetry, visible top/base и известные вертикальные размеры? | F056–F058 допускают условную метрологию; произвольная 3D не установлена | План/scene survey/second view/датчик; E009. Выбор manual envelope, multi-plane, special metrology или indeterminate |
| **Q012 / P1** | Какова лицензия exact metric Hypersim Large weights при расхождении root README и HF revision 7972080? | F064, K009: оба metadata прочитаны, авторское разъяснение не получено | Зафиксировать weights hash/revision и условия наследования, получить однозначную author license. До этого commercial suitability UNKNOWN; не блокирует geometry MVP |
| **Q013 / P1** | Какой tracker и lock реально совместимы с целевой средой и LinQ SDK? | Manifest conflict F068, legacy ByteTrack F069; installation не было | Resolver/import на фактическом Python, exact builds/hashes, E001; choose another compatible build/adapter/isolation. Не обходить deps как доказательство |
| **Q014 / P2** | Разрешены ли публичный питч/сохранение/продуктовое использование выбранных EPFL/Brno assets, доступны ли сами архивы? | EPFL research-use, Brno download/contact и license UNKNOWN: F072/F073 | Exact archive terms/license/доступ; согласованное получение у автора только отдельным поручением. Собственный разрешённый материал предпочтительнее |
| **Q015 / P0** | Какой независимый GT позиции/скорости и времени можно получить, с какой uncertainty? | Одни labels из той же H не проверяют scale; gate average≠instant speed: F030/F077 | Measured marks, optical gates/другой измеритель/синхронный survey; E002/E004. Дефиниция GT определяет сравниваемую величину |
| **Q016 / P1** | Есть ли полные positive/negative sessions с разрешённой работой и достаточно camera-hours для FAR? | Только опубликованные demos, собственного event test нет: F055/F075/F076 | Получить/согласованно записать материалы, double-label спорные эпизоды, split by session; E005/E006. Ноль ошибок на коротком клипе не достаточен |
| **Q017 / P1** | Какой exact pose/action/depth checkpoint реально переносится на промышленный ракурс и LinQ после export/quantization? | Документы/код изучены; device/domain experiments отсутствуют: F009–F012/F059–F063 | Exact weights/preprocessing/skeleton/temporal contract, held-out clips и реальное execution proof, E003/E009/E010; → model_stack, quantization/export |
| **Q018 / P1** | Как маршрутизировать indeterminate и продолжать эпизод после утраты видимости, как это оценивает жюри/оператор? | Три статуса предложены, policy не согласована: F041/F065/F066/F076 | Эксперт+operator_product+evaluation, replay cases; E005/E007. Последнее положительное свидетельство не стирать при исчезновении |
| **Q019 / P1 для prediction** | Тревога журналирует, зовёт оператора или управляет остановкой? Каковы measured L и a_min по грузу/полу/режиму? | F052 — условная кинематика, фактической реакции/торможения нет | Владелец процесса и безопасные проверенные траектории/latency measurements, E008/E010. Без них не обещать collision avoidance |
| **Q020 / P2** | Почему archive/GitHub metadata OpenCV дают разные даты 5.0.0 и какой build будет закреплён командой? | F042 сохраняет расхождение, нужный API исследован на 4.13.0 | Для практики выбрать exact verified build в E001; date-history уточнять лишь если влияет на воспроизводимость. Не требуется для вывода о H |

## Программа экспериментов: предложено, не выполнено

Каждый опыт сохраняет исходные hashes, environment/версии, frozen config, разметку и сырые результаты. Успех сравнивается с **заранее согласованными** budgets Q009; здесь нет выдуманных значений точности, FPS или event quality.

### E001 — Совместимая среда и контракт вывода

**Решение:** какой минимальный стек и адаптер возможны на реальном сервере (Q005/Q013). Входы: OS/architecture/Python, exact LinQ SDK и модельный output example, wheel/source manifests. Последовательность: получить версии → разрешить dependencies без `--no-deps` → lock с hashes → tiny import/API checks OpenCV/Shapely/GEOS → проверить shape/units/frame mapping sample detections. Сохранить resolver log, lock, cv2 build/GEOS/runtime metadata. Если конфликт — другой проверенный build/версия, изоляция или иной tracker; без SDK проверить только geometry environment. Успех не доказывает accuracy/throughput или реальный LinQ inference.

### E002 — Независимая метрическая приёмка пола

**Решение:** можно ли включать метры и где mask (Q002/Q003/Q009/Q015). Входы: fixed profile, planar survey с uncertainty, раздельные fit/control points и отрезки near/mid/far/left/right. Подогнать G/H по fit, заморозить, измерить hold-out position MAE/RMSE/median/P95/max/X–Y bias и distance errors по длине/направлению; повторные клики/perturbations отдельно. Сохранить correspondence table, units/direction, K/D/Knew/ROI, inliers/parameters, residual map и raw controls. При провале региона сократить mask/перемерить, при unknown scale — image-only. Если controls использованы для правки, нужен новый hold-out. Успех не доказывает локализацию людей, другой plane или arbitrary 3D.

### E003 — Bbox, foot keypoints и segmentation на одном материале

**Решение:** какой reference point даёт пригодную full-chain ошибку/coverage (Q006/Q017). Входы: frozen H из E002, независимо размеченные реальные контакты и visibility, варианты модели с точными checkpoint/preprocessing. На тех же кадрах сравнить bbox bottom-center, доступные foot points и маски; отдельно occlusion/truncation/top-down/near/far/platform/shadows. Сохранить paired pixel/world errors, raw outputs, visibility flags, abstention и точную семантику точки. Не штрафовать метод за unknown скрытый contact как будто GT известен. Если нет устойчивого контакта — ограничить metric rule. Успех не доказывает gait или attachment.

### E004 — Время и физическая скорость

**Решение:** включать ли fast-motion и с каким окном (Q004/Q015). Входы: исходное видео+PTS, independent time/position/segment-speed GT, oracle tracks и реальный tracker. Проверить metadata F020; replay с разной вычислительной задержкой, drops/stale/out-of-order/reset; затем пройти измеренные маршруты по направлениям/глубине/поворотам. Сравнивать одинаковые интервальные величины, измерить speed MAE/bias/quantiles, ID errors, valid-window coverage и причинную задержку окна. Сохранить source/processing timelines и generation IDs. Processing delays не должны менять физические оценки одинаковых q/t. При плохом времени/ID — abstain. Gate average успех не доказывает instantaneous peak speed и «бег».

### E005 — События, нормальная работа и лавина дублей

**Решение:** пригоден ли выбранный rule для оператора (Q001/Q007/Q009/Q016/Q018). Входы: полные independent sessions с agreed event labels и hard negatives F055. Заморозить пороги/dwell/merge/matching; one-to-one сопоставить episodes F075. Считать P/R/F1 с zero-denominator policy, duplicates, onset/offset error, FAR по full/negative timeline, eligible/valid camera-hours, recall всех/observable GT и coverage. Сохранить disagreement/контекст/visibility, unmatched lists и event evidence. При false alerts от нормальной работы изменить смысл зоны/state rule на development, затем новый test. Успех не доказывает unseen hazards и предотвращение травм.

### E006 — Sampling rate, phase и краткие движения

**Решение:** допустимая selected frequency для каждого события (Q004/Q017). Входы: один неизменный плотный timestamped source, события/visibility/GT. Выбрать schedules, например 1/2/5/10 FPS и исходный baseline — это точки sweep, не требования. Повторить разные phase offsets; выбрать по PTS, сохранить unique frame IDs/gaps, оценить geometry-only oracle tracks и full chain. Метрики: event recall/timing/coverage/ID errors, speed error и latency отдельно от throughput. Добавить короткий вход, run-return, slow run/fast walk и пропущенный trigger. Если событие исчезает между кадрами, увеличить sampling/сменить claim. Успех не доказывает, что нужная частота достижима на LinQ.

### E007 — Drift, camera profile и отказы наблюдаемости

**Решение:** когда suspend rules и нужна новая калибровка (Q003/Q010/Q018). Входы: fixed anchors, нормальная вибрация/свет, controlled camera shifts/zoom/crop/resolution changes, occlusion/new-plane cases. Изменять по одному фактору; измерить hold-out degradation, drift warning miss/delay, false invalidations, indeterminate coverage и ложное «нет опасности» в blind intervals. Проверить сохранение старых event versions. При неизвестном изменении блокировать зависимые metric rules, не молча автокомпенсировать. Успех не доказывает корректную auto-recalibration произвольного PTZ.

### E008 — Footprint, current gap и prediction отдельно

**Решение:** добавлять ли moving proximity/TTC (Q008/Q019). Входы: dimensions/load/anchor/heading, измеренный floor frame, timestamps, безопасные архивные манёвры/статичные постановки, state/response contract. Сначала измерить anchor/shape/orientation/gap error; отдельно reverse/standstill/turn/rear swing. Затем проверить TCA+d_CA/TTC и simultaneous footprints на approaching/parallel/near-pass/diverging примерах. Если нужен stopping envelope, отдельно получить реальные L/a_min по режимам. Сохранить model assumptions, age/horizon, GT semantics, lead-time и errors. При провале оставить fixed corridor/zone или conservative candidate. Успех в constant-velocity replay не доказывает collision avoidance или верность реакции людей.

### E009 — Контрпримеры 3D и optional depth/metrology

**Решение:** чем подтверждать сложный сценарий (Q011/Q012/Q017). Входы: известные floor/platform/load geometry, independent 3D/depth GT, допустимые weights, sync extra view если есть. Сравнить «перед/под/за», разные уровни, похожие 2D silhouettes, hidden attachment, normal floor work. Для metric depth не подгонять scale/shift по test GT: optional calibration split отдельно, frozen transform. Измерять errors критических clearance/edges и event decisions, не только average depth RMSE; проверить honest indeterminate. Для load сравнить actual projection и configured operation envelope как разные targets. Никаких людей под реальным опасным грузом ради GT. Успех не подтверждает скрытые детали, полную 3D и LinQ export.

### E010 — Реальный LinQ route и минимальная доказательная демонстрация

**Решение:** что можно заявлять end-to-end (Q005/Q019). Входы: доступ/разрешение устройства, SDK, exact model/runtime, server-uploaded video, approved config, проверенные E002–E007. Зафиксировать model/weights/input/output/device artifacts; связать исходные frame IDs/PTS с реальным LinQ выводом, затем replay CPU geometry. Показать кадр калибровки+independent controls, расстояние на полу, реальное движение, один зональный эпизод, legitimate negative и отказ при occlusion/camera shift. Измерить source/sample/inference rates, queue/window/wall latency и replay rate. Сохранить hashes, logs, raw detections, coordinates/rule reasons, versions и evidence clip. Ручные tracks допускаются только как явно подписанный отдельный geometry test. Успех доказывает конкретный route/материал, не все models/cameras и не safety certification.

## Адресная передача соседним исследованиям

| Тема | Что передать и какое решение меняется | Основания |
|---|---|---|
| `model_stack`, `violation_methods` | Contact-point semantics, bbox visible/full-body, foot visibility/skeleton, inverse preprocessing, neural pose/action/depth как отдельные графы; speed≠gait | F009–F016, F023/F026, F059–F066; E003/E006 |
| `linq_platform`, `quantization/export` | Coordinate/temporal fidelity после export, factual device execution; CPU geometry permission и совместимость exact SDK/lock | F068/F069/F078; Q005/Q013/Q017; E001/E010 |
| `video_architecture` | Uploaded source video, PTS/epochs/gaps/stale flags, separate clock domains и one-time coordinate inverse; calibration invalidation | F007/F013/F017/F038/F040; E004/E007 |
| `evaluation` | Separate geometry/contact/track/event layers, spatial strata, independent GT, all/conditional recall, FAR denominators и coverage | F018/F030/F075–F077; E002–E009 |
| `datasets`, `behavioral_models + datasets` | Visibility/plane/GT requirements, gait hard negatives, actual-under-load vs manual envelope; EPFL/Brno limits/terms | F055/F066/F072/F073; Q014–Q017 |
| `operator_product` | Rule-specific indeterminate reason, last confirmed evidence vs current visibility, immutable event config; state/permission вместо blanket exceptions | F041/F043/F065/F066; Q007/Q018; E005/E007 |
| `hackathon_strategy` | Три проверяемые MVP функции, conditional claims, 1 FPS observability distinction, reproducible demo/failure evidence | F017/F039/F078; E010 |

Соседние отчёты в этом запуске не получены; их содержание и фактические пути не предполагаются. Передача означает эти файлы и ID, а не запуск других исследований или сообщения во внешние чаты.
