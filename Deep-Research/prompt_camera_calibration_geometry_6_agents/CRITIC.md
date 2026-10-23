# Доказательные ограничения и сопоставление оркестратора

`review_mode: orchestrator_synthesis_only; no_independent_critic; no_second_wave`

Автор всех K-ID — корневой оркестратор. Это собственное сопоставление результатов **одной** волны, а не замечания несуществующего независимого критика. Никакой второй волны/заключительного аудита не проводилось. Исходные результаты: [01](_WORK/AGENT_01_GEOMETRY.md), [02](_WORK/AGENT_02_CALIBRATION.md), [03](_WORK/AGENT_03_SPEED.md), [04](_WORK/AGENT_04_PROXIMITY.md), [05](_WORK/AGENT_05_COMPLEX.md), [06](_WORK/AGENT_06_TOOLS.md).

## K001 — Вход пользователя не равен официально прочитанному кейсу

Происхождение: осмотр папки, A01–A06, [F001–F003](RAW_FACTS.md#f001). PDF/видео/SDK отсутствуют. Сценарии и приоритет accuracy берутся из тематического задания; LinQ+CPU — пересказ команды. Последствие: нельзя заявлять официальный перечень правил, разрешённость CPU и фактический hardware route. **Результат сопоставления:** контекст сохранён с происхождением, архитектура условна. **Осталось:** Q001/Q004/Q005, E001/E010.

## K002 — Четыре клика и training residual не доказывают метры

Происхождение: A01-F02/F05/F10, A02 workflows, A06-F13; [F022](RAW_FACTS.md#f022), [F025](RAW_FACTS.md#f025), [F030](RAW_FACTS.md#f030). Неизвестные world XY, вырождение или неверный scale могут дать визуально красивый BEV. Те же опоры нельзя использовать как независимый hold-out. **Уточнено:** известные метрические correspondences, overdetermined fit и другие measured controls; неверные цели RANSAC не исправляет. **Осталось:** Q002/Q009/Q015, E002. Расширять mask за проверенный участок не рекомендовано.

## K003 — Правильная H не исправляет неверную точку/плоскость

Происхождение: A01 reference study, A04 critical reading, A05 ray–plane; [F026–F029](RAW_FACTS.md#f026), [F045](RAW_FACTS.md#f045). Торс/плечи/ankle выше пола, visible-only bbox при occlusion и platform дают systematic bias. **Уточнено:** detector/pose/segmentation сравнивают full-chain на одной семантике контакта; pose не объявлен универсально лучшим. **Осталось:** Q006/Q011, E003/E009. Локальный pinhole расчёт — иллюстрация, не camera benchmark.

## K004 — 1 FPS и tensor length не доказывают temporal observability

Происхождение: A03 documentation/code, A05 fall/climbing, A06 sampling; [F007–F017](RAW_FACTS.md#f007). Processing FPS отличается от selected-source FPS; повторение кадров заполняет тензор без новых фаз. **Уточнено:** source PTS, unique observations, span/gaps и phase sweep; fast motion отдельно от gait. **Осталось:** Q004/Q017, E004/E006. Универсальный минимум FPS и порог бега не выведены.

## K005 — Proximity не тождественно нарушению или 3D clearance

Происхождение: A04-F01–F06/F14, A05 complex matrix; [F043–F048](RAW_FACTS.md#f043), [F053](RAW_FACTS.md#f053). У пульта, сигнальщика и штатного прохода может быть законная близость; feet не измеряют reach-in руками. **Уточнено:** geometric observation и semantic rule context разделены; body radius/error/protective margin разные. **Осталось:** Q001/Q007/Q008, E005/E008. Само разрешение работ не используется как универсальное подавление риска.

## K006 — TTC, TCA и swept overlap имеют разный смысл

Происхождение: A04 own derivation, FHWA terminology; [F049–F052](RAW_FACTS.md#f049). `gap/relative_speed` не general TTC, пересечение swept areas без одновременности не collision. Остановочная зона требует measured reaction/braking, а не только скорости. **Уточнено:** отдельные формулы, horizon, constant-velocity assumptions, age/ID/turning gates; prediction вынесен в extension. **Осталось:** Q008/Q019, E008. Предотвращение столкновения не подтверждено.

## K007 — «Одна камера никогда не измеряет высоту» было бы чрезмерно

Происхождение: A01/A02/A05 прочитали одну цепочку Criminisi ICCV1999, [F056–F058](RAW_FACTS.md#f056). Дополнительные vanishing geometry/known height или calibrated scene позволяют условные измерения. **Уточнено:** запрет касается произвольной высоты из одной floor H, а не любой single-view metrology. Повторы одной статьи не считаются независимым подтверждением; ICCV1999 и IJCV2000 не смешаны. **Осталось:** Q011, E009. Для реального груза/платформы опоры отсутствуют.

## K008 — Metric depth — обученная оценка с отдельной проверкой

Происхождение: A02 GeoCalib, A05 V2/Metric3D; [F036](RAW_FACTS.md#f036), [F061–F064](RAW_FACTS.md#f061). Camera calibration/relative depth/metric depth решают разные задачи; default focal и per-test GT scale fit способны исказить вывод. **Уточнено:** depth — optional research route; independent test без скрытой scale alignment. **Осталось:** Q011/Q012/Q017, E009/E010. Скрытые объекты и attachment relation не восстанавливаются фактом наличия depth map.

## K009 — Лицензии зависят от конкретного артефакта

Происхождение: A02 licenses, A05 HF/root conflict, A06 data terms; [F034–F036](RAW_FACTS.md#f034), [F059](RAW_FACTS.md#f059), [F064](RAW_FACTS.md#f064), [F072–F074](RAW_FACTS.md#f072). fSpy GPL, OpenPose restrictions и dataset research-use не равны permissive reusable package. V2 Large root wording расходится с exact metric HF card. **Уточнено:** код/weights/dataset/зависимости учитываются отдельно, универсальный правовой вывод не сделан. **Осталось:** Q012/Q014; применимость конкретного использования до выбора artifact UNKNOWN.

## K010 — Source tag/API и совместимый package lock различаются

Происхождение: A01 release metadata, A06 manifests; [F042](RAW_FACTS.md#f042), [F068–F069](RAW_FACTS.md#f068). `/4.x` не latest; прочитанная API-версия не означает установленный package. Norfair2.3 и OpenCV wheel4.13 конфликтуют по NumPy; original ByteTrack содержит legacy dependencies. **Уточнено:** минимальное geometric ядро без обязательного tracker, никаких непроверенных pip-рецептов. **Осталось:** Q005/Q013/Q020, E001. Manifest conflict установлен чтением, installer/resolver не запускался.

## K011 — Abstention не должна улучшать качество скрытым исключением

Происхождение: A03 metrics, A05 policy, A06 matching; [F018](RAW_FACTS.md#f018), [F065–F066](RAW_FACTS.md#f065), [F075–F077](RAW_FACTS.md#f075). Invalid geometry/NaN/occlusion не safe. FAR на коротком/выбранном видео и precision только по удобным кадрам искажают полезность. **Уточнено:** end-to-end/conditional recall, all eligible/valid camera-hours, indeterminate reasons, one-to-one events и duplicates. **Осталось:** Q009/Q016/Q018, E005/E007. Полевая частота тревог не измерена.

## K012 — Найденные демонстрации и GT не устанавливают качество MVP

Происхождение: A04 12-minute showcase; A06 official demo/EPFL/Brno; [F045](RAW_FACTS.md#f045), [F071–F073](RAW_FACTS.md#f071). Image-to-image warp не метрическая проверка, discrete grid не continuous speed GT, vehicle LiDAR benchmark не person/forklift violation GT. **Уточнено:** собственный survey/time/event protocol; demos использованы как building blocks, не полевое доказательство. **Осталось:** Q015/Q016, E002–E010. Реальный deployment evidence систематически не установлен в этой волне; отсутствие подтверждения не означает отсутствия решений.
