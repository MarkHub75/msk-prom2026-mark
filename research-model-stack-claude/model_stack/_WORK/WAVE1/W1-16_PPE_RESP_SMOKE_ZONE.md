# W1-16 PPE_RESP_SMOKE_ZONE — респираторы/маски, курение, огонь/дым, зоны, падения

- ID: W1-16 (первая волна, ячейка выделена из 05)
- Запрошено: Claude Sonnet 5.5, effort medium
- Фактическая модель (из системного окружения): **Sonnet 5.5**, model ID **claude-sonnet-5-5**
- Время: начало ~04:43 MSK 2026-10-23, конец ~05:10 MSK (по часам shell; зона показана как RTZ, сдвиг к MSK не проверялся)
- Что делалось локально: HF API/tree/README, GitHub API, чтение .pt как zip БЕЗ unpickle (байтовый разбор data.pkl: names/version), чтение docs. Обучений, экспортов, загрузки моделей в ultralytics и запусков инференса НЕ было.

## FLASH
1. **SH17 не содержит класса «respirator».** ahmadmughees/SH17dataset@2f832c289f9deea063367045ed8230b26e3e7ea9: маска = `face-mask` (README: «Face-mask-medical»), рядом `face-guard`. Порядок классов в README и в sh17.yaml/чекпойнте РАЗНЫЙ (F01, F02). Лицензия датасета CC BY-NC-SA 4.0 (некоммерческая), картинки с Pexels.
2. **Прослеживаемых готовых весов «промышленный респиратор надет/снят» не найдено.** Есть медицинская маска (SH17), датасеты mask/no_mask/incorrect (Kaggle FMD) и датасеты с типами респираторов без весов (FMR-DB, WWMR-DB). «Снят респиратор» = собственная разметка + каскад.
3. **Для D-Fire-весов порядок классов `0 smoke, 1 fire`** (local_observation по чекпойнту rabahdev/fire-smoke-yolov8n, F07).
4. Все найденные cigarette-детекторы: один класс `cigarette`, YOLO11m, метрики автора (`verified: false`); в метаданных чекпойнта лицензия AGPL-3.0, в карточке HF — MIT (F09).
5. → W1-13: контракт зон. Ultralytics `RegionCounter` проверяет **центр bbox**, supervision `PolygonZone` по умолчанию **BOTTOM_CENTER** (F13, F14).

## Резюме для оркестратора
- «Вход в опасную зону»: person-детектор (COCO `person`) + полигон + (опц.) трекер; документированные примитивы есть (Ultralytics solutions, supervision). Специальных весов не нужно — самый реалистичный сценарий за 45 часов.
- «Снят респиратор»: одним детектором честно не решается. Нужны person → голова/лицо (кроп) → классификатор/детектор маски-респиратора → временной фильтр (K из N кадров). Готовых весов для промышленных респираторов нет; медицинская маска покрывается SH17 `face-mask` (NC-лицензия) и/или Kaggle FMD (3 класса, 853 изображения, CC0 по вторичным источникам). Метрик на дальнем CCTV не найдено.
- «Курение рядом с горючими»: минимум три компонента — cigarette-детектор (мелкий объект), опционально pose «рука у рта», и «горючее»/зона (готового класса нет → полигон или своя разметка) плюс правило «курение внутри зоны». Fire/smoke-веса (D-Fire) решают другую задачу («горит/дымит»), для сигаретного дыма не годятся (inference).
- Огонь/дым: D-Fire (CC0 для сборки, часть изображений под условиями провайдеров), YOLOv8n-веса с порядком smoke/fire, mAP50 0.754 (автор HF). Независимый бенчмарк FireViewer показывает flame AP50-95 0.0193 — обобщаемость на промышленные помещения не доказана.
- Падение: HF-веса есть (melihuzunoglu, leeyunjai), но датасеты «custom»/без прослеживаемого происхождения; в промышленности — только как идея + собственная проверка.
- Перчатки/очки: SH17 (`gloves`, `glasses`) и Ultralytics Construction-PPE (`gloves`, `goggles`, `no_gloves`, `no_goggle`), AGPL-3.0.
- Переносимость на LinQ не проверялась: в публичном перечне только названия yolo5s/yolo8/yolo11; pose/seg/NMS — unknown (→ linq_platform).
- Главные разрывы: нет CCTV-данных под сценарии; нет независимой оценки на промышленных видео; лицензии (SH17 NC, AGPL Ultralytics-весов, Roboflow-датасеты не проверены).

## Карта сценариев
| Сценарий | Реалистичный путь | Лучшие найденные артефакты | Чего нет | Нужные данные |
|---|---|---|---|---|
| Не надета каска | → W1-05 | — | — | — |
| Снят респиратор / маска | person → crop головы → детектор/классификатор «маска/респиратор/нет» + временной фильтр | SH17 `face-mask` (yolo8n..10x; NC); Kaggle FMD; FMR-DB/WWMR-DB (типы респираторов; лицензия не установлена) | веса для промышленного респиратора; оценка на CCTV | разметка своих кадров: `respirator_on`, `no_respirator`, возможно `respirator_below_chin` |
| Вход в опасную зону | person det + полигон (низ-центр bbox) + трек | Ultralytics `RegionCounter`/`ObjectCounter`; supervision `PolygonZone` | модельных пробелов нет | полигон по кадру; тестовое видео |
| Курение рядом с горючими | cigarette det + (pose рука-рот) + зона/класс горючего + правило | HF Beehzod/*, Enos-123/* (YOLO11m, `cigarette`); литература F10 | класс «горючее»; метрики на дальнем ракурсе | кадры с мелкой сигаретой при реальных ракурсах |
| Огонь/дым | детектор fire/smoke + временное подтверждение | D-Fire; rabahdev/fire-smoke-yolov8n; pedbrgs/Fire-Detection (YOLOv5 + AVT/TPT) | валидация в цеху | кадры цеха, источники ложных (пар, сварка) |
| Падение / лежащий | person+трек+правило (аспект bbox/неподвижность) или pose; либо готовый fall-детектор | melihuzunoglu/human-fall-detection; leeyunjai/yolo11-falldetect | прослеживаемые данные/лицензии | свои видео лежащих/присевших |
| Перчатки / очки | SH17, Construction-PPE | см. F01, F06 | — | — |

## Факты
Формат: ID — утверждение | тип основания | источник + локатор | область | статус проверки | оговорки.

- **W1-16-F01** — SH17: 8,099 изображений, 75,994 инстансов, 17 классов. README перечисляет Person, Head, Face, Glasses, Face-mask-medical, Face-guard, Ear, Earmuffs, Hands, Gloves, Foot, Shoes, Safety-vest, Tools, Helmet, Medical-suit, Safety-suit; `sh17.yaml` задаёт `0 person, 1 ear, 2 ear-mufs, 3 face, 4 face-guard, 5 face-mask, 6 foot, 7 tool, 8 glasses, 9 gloves, 10 helmet, 11 hands, 12 head, 13 medical-suit, 14 shoes, 15 safety-suit, 16 safety-vest`. Класса respirator нет. | author_statement | S01 (README.md, sh17.yaml @2f832c2) | SH17 | прочитан README/yaml | порядок и имена (`Face-mask-medical` vs `face-mask`, `Tools` vs `tool`) различаются; не «исправлять» по догадке.
- **W1-16-F02** — Чекпойнт `yolo8n.pt` (релиз v1 SH17) содержит `names`, совпадающие с sh17.yaml (17 классов, 5 face-mask, 16 safety-vest); train-arg `model: yolov8n.pt`, `data: /home/ifiveo/repos/mughees/train_y8/safe_human.yaml`; метаданные: ultralytics `8.2.38`, `AGPL-3.0`. Файл 6,252,377 байт, sha256 5449f62bd7cf30c01c7fd138db2729a38abcb4d5120449773fba475d54f30b62 (вычислен локально). | local_observation | S02 (разбор байтов best/data.pkl без unpickle) | yolo8n.pt SH17 v1 | получен артефакт; names прочитаны; в ultralytics не загружался | README пишет `ultralytics==8.0.38`, чекпойнт — 8.2.38; влияние на экспорт не проверено.
- **W1-16-F03** — Метрики SH17 (автор), val 1620 изображений / 15358 инстансов: YOLOv8n P 67.5 R 53.6 mAP50 58.0 mAP50-95 36.6; v8s 63.7/41.7; v8m 66.6/45.7; YOLOv9-e 70.9/48.7 (лучшая). | reported_measurement | S01 | усреднение по 17 классам; команда val: imgsz 640, batch 1 | прочитано; не воспроизведено | per-class AP для `face-mask` не опубликован в README → unknown.
- **W1-16-F04** — Лицензия SH17: CC BY-NC-SA 4.0; изображения Pexels (скрипт download_from_pexels.py, list_of_all_urls.csv); «для образовательных/исследовательских целей». | author_statement | S01 | датасет | прочитано | лицензия весов отдельно не заявлена; юридически не оценивалось.
- **W1-16-F05** — Релиз SH17 v1: yolo8{n,s,m,l,x}, yolo9{t,s,m,c,e}, yolo10{n,s,m,b,l,x}; yolo8n 6,252,377 байт; yolo8m 52,046,785; yolo9e 117,283,098. YOLO11/YOLO26 нет. | artifact_metadata | S01 (gh api releases) | v1 | список получен; digest в API пуст | —
- **W1-16-F06** — Ultralytics Construction-PPE: 11 классов `0 helmet,1 gloves,2 vest,3 boots,4 goggles,5 none,6 Person,7 no_helmet,8 no_goggle,9 no_gloves,10 no_boots`; 1,416 изображений (1132/143/141); AGPL-3.0; авторы Dalvi et al. 2025; масок/респираторов нет. | primary_documentation | S03 | страница доков на 2026-10-23 | прочитана; датасет не скачивался | пересечение с W1-05.
- **W1-16-F07** — rabahdev/fire-smoke-yolov8n @13017fe8af477c25f5298d168e2dfede4b000753: YOLOv8n, дообучение на D-Fire, классы `0 smoke, 1 fire`; best.pt 6,229,802 байт, LFS sha256 b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f (равен локально вычисленному); test 4,306: mAP50 0.754, mAP50-95 0.430 (smoke 0.499, fire 0.362), P 0.766, R 0.688; 50 эпох, imgsz 640; в карточке лицензия agpl-3.0. | artifact_metadata + author_statement + local_observation | S04; names `smoke`,`fire`, nc=2 и версия ultralytics `8.4.51` прочитаны из data.pkl без unpickle | этот revision | получен файл; инференс не запускался | метрики не проверены; обучение на Apple MPS.
- **W1-16-F08** — D-Fire (gaiasd/DFireDataset@3890a756b224855f4f7ef8d237a70bc1834a4714): >21,000 изображений: только fire 1,164; только smoke 5,867; оба 4,658; без 9,838; bbox fire 14,692, smoke 11,865; YOLO-формат; собственные камеры + веб + публичные (HPWREN, FESB, FireNet). LICENSE: CC0 1.0 для сборки; изображения с префиксом `PublicDataset` — под условиями исходных провайдеров. Загрузка через OneDrive/Kaggle-зеркало. | author_statement | S05 | D-Fire | прочитаны README/LICENSE; данные не скачивались | GitHub API license: NOASSERTION.
- **W1-16-F09** — Cigarette-детекторы HF (best.pt, YOLO11m, один класс `cigarette`): (a) Beehzod/smoke_cigarette-detection2-yolo11m @2bcdad62860498489e14954aa95c60f04ad0a9e4, 40,521,900 байт, LFS sha256 c4f887d26437ad00be5c6861547efef73ed84561da112710da67935bd3dd7d76 (равен локальному), Roboflow smoking-detection-5e8hh/smoking-detection-ggnhq v1 (1636/461/240), заявлено mAP50 0.9943, mAP50-95 0.7421, P 0.9811, R 0.9835; (b) Beehzod/best_smoke_cigarette-detection @8dd44e25a69b243e53f66b30c0e50889033dc391, Roboflow richie-lab/smoking-tasfx v2 (12046/318/122), mAP50 0.7898, mAP50-95 0.4617; (c) Beehzod/smoking-detection-finetuned @d81c4396e5e3f089e8144d8034a0d18025553495, Roboflow xu-wei/cigarette-all v1 (1613/203/201), mAP50 0.8698, R 0.7957; (d) Enos-123/smoking-detection @f6756f9c9cfe9fbbbeb69efcc801632636838ad2, Roboflow yolo-pdvpx/cigarette-h2p1m, mAP50 0.829, P 0.8562, R 0.7692. Карточки: license mit; метаданные чекпойнта (a): AGPL-3.0, ultralytics 8.4.155, names `cigarette`. | artifact_metadata + author_statement + local_observation (names/version для (a)) | S06 | указанные revision | проверены метаданные, README, один чекпойнт на names; инференс не запускался | Карточка (d) говорит «cigarette smoke», класс — `cigarette`. Метрики (a) 0.994 на 461 val-изображении, вероятно лёгкое распределение (inference). Лицензии Roboflow-датасетов не проверены; размер сигареты в пикселях — unknown.
- **W1-16-F10** — Подходы к курению: arXiv 2210.06682 (Wang, Liu, Lian, 2022) — двухстадийная схема (грубо: рука/сигарета/голова; точно: пальцы с сигаретой, область рта, сигарета), метрики и код не указаны в abstract; Singapore Inst. of Technology 2024 — поза тела, balanced accuracy 94.41% (по выдержке поиска); Bursa Technical Univ. (ICHORA 2025) — MediaPipe Pose рука-рот + скелет руки, >95% (доступ закрыт); патент CN115471916A — суставы руки + сигарета + рот на последовательности кадров. | author_statement (abstract/выдержки) | S07 | перечисленные работы | прочитан только abstract arXiv | полные тексты не читались; метрики вторичные.
- **W1-16-F11** — Kaggle «Face Mask Detection» (andrewmvd): 853 изображения; `with_mask`, `without_mask`, `mask_weared_incorrect`; CC0 по deepchecks/обзору (Roboflow-зеркало показывает CC BY 4.0). Медицинские маски, лица крупным планом (inference). | author_statement (вторичное) | S08 | — | Kaggle-страница не открывалась | —
- **W1-16-F12** — Респираторы по типам: FMR-DB (IEEE DataPort, DOI 10.21227/wg71-v415) — 2565 изображений из интернета по типам масок/респираторов (в т.ч. полнолицевые, полумаски, одноразовые с клапаном и без); WWMR-DB (DOI 10.21227/8atn-gn55) — ~1222 изображений, 8 способов ношения (под носом, под подбородком, на лбу и др.), YOLO/VOC-разметка; лицензия не получена; готовых весов не найдено. Roboflow «HalfFaceMask» ~446 изображений, CC BY 4.0 (выдержка). | author_statement (вторичное) | S09 | — | страницы целиком не открывались | число изображений WWMR различается в источниках (1222/1225).
- **W1-16-F13** — Ultralytics `solutions.RegionCounter`: центр bbox `((x0+x1)/2,(y0+y1)/2)` проверяется на `contains` в полигоне; region — список (x,y) или dict имя→точки, ≥3 точек; счёт покадровый; по умолчанию трекер `tracktrack.yaml`, conf 0.25, iou 0.7, imgsz 640. | source_code + primary_documentation | S10: ultralytics@e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8, `ultralytics/solutions/region_counter.py`, `RegionCounter.process` (строки ~125–127 в этом commit); docs region-counting | Ultralytics v8.4.184 (Latest, 2026-10-22), AGPL-3.0 | прочитан код/доки; не запускался | доки анонсируют «YOLO27», примеры используют `yolo26n.pt`.
- **W1-16-F14** — supervision `PolygonZone(polygon, triggering_anchors=(Position.BOTTOM_CENTER,), require_all_anchors=True)`; `trigger()` возвращает bool-массив; `reduce = np.all if require_all_anchors else np.any`. | source_code + primary_documentation | S11: roboflow/supervision@8402aa2fe2732b972224f15ad2e5988442fe3061, `src/supervision/detection/tools/polygon_zone.py` (class PolygonZone ~23, __init__ ~86–87, trigger ~131, reduce ~210) | supervision 0.31.1 (2026-10-20), MIT | прочитан код; не запускался | для «ноги в зоне» BOTTOM_CENTER логичнее центра bbox (inference).
- **W1-16-F15** — Fall-детекторы HF: melihuzunoglu/human-fall-detection @97261b03632a9715a27481b2cfdac6a78e26d2d9 (YOLO11, agpl-3.0, датасет «custom», классы включают Fallen и Sitting; полный список я не дочитал); leeyunjai/yolo11-falldetect @f240b740b7357b263204498ad405a88764d15f6d (falldetect-11x.pt, класс `Fall-Detected`, лицензия не указана). | author_statement + artifact_metadata | S12 | — | карточки прочитаны | происхождение данных не прослежено.
- **W1-16-F16** — pedbrgs/Fire-Detection@9d99b0e71fd4cc930da053a41b79de1c58aabdf2 (MIT): YOLOv5 s/l + временной анализ (AVT — улица, TPT — помещение); веса по ссылкам OneDrive; опубликован с статьями в Neural Computing and Applications 2022/2023. | author_statement | S13 | — | README прочитан, веса не получены | ссылки OneDrive вне контроля.
- **W1-16-F17** — fireviewer/fire-smoke-yolo11m-strict-v1 @e1c5ed92c19cb1dc7aa2cc7a814e77277807fa19: собственный независимый бенчмарк: COCO mAP50-95 0.1491, mAP50 0.2784, smoke AP50-95 0.2790, flame AP50-95 0.0193, holdout P/R/F1 0.4274/0.2488/0.3145, false-alarm rate на negative-изображениях 0.3391; авторы: «не квалифицирован для pointing»; model.pt 40,502,892, model.onnx 81,058,099 байт. | reported_measurement | S14 | их корпус и протокол | README прочитан | не сопоставимо с D-Fire.
- **W1-16-F18** — В COCO нет классов «cigarette», «lighter», «горючие материалы»; `person` есть. | inference | общеизвестный состав COCO, не перепроверялся | — | не проверено локально | при выборе весов сверять `model.names`.

## Источники
- **W1-16-S01** — SH17dataset (Ahmad, Rahimi), https://github.com/ahmadmughees/SH17dataset, master @2f832c289f9deea063367045ed8230b26e3e7ea9 (pushed 2024-12-04), README.md и sh17.yaml; release v1 (2024-07-04). Проверено 2026-10-23, доступно. Статья arXiv 2407.04590 (список классов и лицензия датасета на странице arXiv не указаны); JSSR doi 10.1016/j.jnlssr.2024.09.002.
- **W1-16-S02** — SH17 yolo8n.pt, https://github.com/ahmadmughees/SH17dataset/releases/download/v1/yolo8n.pt; копия в SCRATCH\w116\sh17n.
- **W1-16-S03** — Ultralytics Docs «Construction-PPE», https://docs.ultralytics.com/datasets/detect/construction-ppe/, 2026-10-23.
- **W1-16-S04** — HF rabahdev/fire-smoke-yolov8n @13017fe8af477c25f5298d168e2dfede4b000753 (lastModified 2026-06-08).
- **W1-16-S05** — D-Fire https://github.com/gaiasd/DFireDataset @3890a756b224855f4f7ef8d237a70bc1834a4714 (pushed 2026-10-18).
- **W1-16-S06** — HF: Beehzod/smoke_cigarette-detection2-yolo11m, Beehzod/best_smoke_cigarette-detection, Beehzod/smoking-detection-finetuned, Enos-123/smoking-detection (revision в F09), проверено 2026-10-23.
- **W1-16-S07** — arXiv 2210.06682; SIT 2024 (irr.singaporetech.edu.sg, «Enhancing Indoor Smoking Detection through Deep Learning in AI-Enabled Surveillance Systems»); Bursa (acikerisim.btu.edu.tr/items/25cc3b3f-7126-41d7-af74-80e7bebc33ce); патент CN115471916A. Только abstract/выдержки.
- **W1-16-S08** — Kaggle andrewmvd «Face Mask Detection» через docs.deepchecks.com и arXiv 2211.08030; Kaggle не открыт.
- **W1-16-S09** — IEEE DataPort FMR-DB, WWMR-DB; Roboflow HalfFaceMask https://universe.roboflow.com/workspace-xxnir/halffacemask; данные не открывались.
- **W1-16-S10** — ultralytics/ultralytics@e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8, release v8.4.184; https://docs.ultralytics.com/guides/region-counting/.
- **W1-16-S11** — roboflow/supervision@8402aa2fe2732b972224f15ad2e5988442fe3061 (develop), 0.31.1; https://supervision.roboflow.com/latest/detection/tools/polygon_zone/.
- **W1-16-S12** — HF melihuzunoglu/human-fall-detection, leeyunjai/yolo11-falldetect (revision в F15).
- **W1-16-S13** — https://github.com/pedbrgs/Fire-Detection @9d99b0e71fd4cc930da053a41b79de1c58aabdf2.
- **W1-16-S14** — HF fireviewer/fire-smoke-yolo11m-strict-v1 @e1c5ed92c19cb1dc7aa2cc7a814e77277807fa19 (2026-10-10).

## Противоречия
1. SH17: README (`Face-mask-medical`, свой порядок) vs sh17.yaml/чекпойнт (`face-mask`, другой порядок). Использовать `names` конкретного чекпойнта.
2. SH17 README `ultralytics==8.0.38` vs чекпойнт 8.2.38 — воспроизводимость обучения/экспорта.
3. Лицензии весов: карточки HF `mit` vs метаданные чекпойнта AGPL-3.0 (→ operator_product).
4. Карточка Enos-123 «cigarette smoke» vs класс `cigarette`.
5. D-Fire: CC0 для сборки vs условия третьих сторон; GitHub API NOASSERTION.
6. Fire/smoke метрики D-Fire-весов (0.754 mAP50) vs независимый FireViewer (flame AP50-95 0.0193): разные корпуса, несопоставимо.

## Открытые вопросы
1. Размер сигареты (px) и минимальный ракурс для F09 — искал карточки HF; закрыть: прогон на 30+ собственных кадрах.
2. per-class AP SH17 `face-mask`/`face-guard` — закрыть `model.val` на SH17 (Kaggle) или статьёй.
3. Лицензии/доступ FMR-DB, WWMR-DB, Roboflow-датасетов F09 — открыть страницы.
4. Принимает ли компилятор LinQ Ultralytics-ONNX head для найденных весов; нужны ли pose/seg; влияние малых объектов и входа >640 — → linq_platform (публично не установлено).
5. Третий класс и данные melihuzunoglu/human-fall-detection — прочитать README целиком/names чекпойнта.
6. Набор нарушений полного кейса (публикация 23.10 13:00 MSK) — unknown.

## Предлагаемые эксперименты
- **E1 cigarette на дальнем кадре.** Кандидаты F09(a),(b),(d). Окружение: ПК RTX 4070 (ПО не установлено; venv в SCRATCH). Шаги: инференс на 30+ реальных кадрах разных расстояний; сохранить размер bbox, conf, FP на людях без сигареты. Если сигарета мала (порядок десятков пикселей) — переход к pose/каскаду. Не подтверждает: LinQ, лицензию. Остановка: 2 ч.
- **E2 SH17 face-mask на CCTV.** yolo8n/s из S01; recall `face-mask` vs размер головы. Не различает респиратор/мед. маску.
- **E3 зона.** RegionCounter (центр) vs PolygonZone(BOTTOM_CENTER) на одном видео; ложные входы.
- **E4 D-Fire-веса и ложный огонь.** F07 на видео цеха (сварка, пар); частота FP.

## Передачи соседям
- → W1-13: контракты зон (F13, F14); двухстадийная идея «рука/рот/сигарета» (F10); temporal fire (F16).
- → linq_platform: принимает ли компилятор yolo8/yolo11 Ultralytics-ONNX head; pose/seg; ограничения на малые объекты и размер входа.
- → datasets: SH17 (NC), D-Fire, Kaggle FMD, FMR-DB, WWMR-DB, Construction-PPE, Roboflow cigarette-датасеты.
- → training_strategy: респиратор потребует дообучения; двухстадийный классификатор на кропе головы.
- → evaluation: метрики F09 не независимы; нужна общая контрольная выборка.
- → operator_product/hackathon_strategy: честно показываемы «зона» и «маска» с временным фильтром; «курение» — экспериментально; риски AGPL/NC.

## Запросы эскалации
- Переносимость мелкообъектного cigarette-детектора на реальный ракурс — после публикации полного кейса и появления кадров.
- Юридическая оценка NC (SH17) и AGPL для весов — вне моего участка.

## Ограничения запуска
- Не открыты: Kaggle, IEEE DataPort, Roboflow Universe (лицензии/данные только по выдержкам поиска).
- Ничего не запускалось на моделях; ultralytics не импортировался; три чекпойнта прочитаны байтово без десериализации (SCRATCH\w116).
