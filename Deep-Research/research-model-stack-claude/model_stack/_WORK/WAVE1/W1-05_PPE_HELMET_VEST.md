# W1-05 PPE_HELMET_VEST — готовые доменные веса: каски, головы, жилеты, person

- Ячейка: W1-05 (волна 1). Запрошено: Claude Sonnet 5.5, effort medium.
- Фактическая модель (из системного окружения): **Sonnet 5.5, model ID `claude-sonnet-5-5`**.
- Время: начало ~04:44 MSK, конец ~05:20 MSK, 2026-10-23.
- Мои вспомогательные скрипты: `W1-05_files\pickle_strings_static.py` (статический разбор `data.pkl` из .pt через `pickletools.genops`, БЕЗ исполнения и без десериализации), `W1-05_files\hf_meta.py` (HF API: sha/размеры/LFS oid).

## FLASH
1. **Единственный артефакт с полностью прослеживаемой цепочкой (статья → данные → split-списки → классы → веса → метрики): SH17** (github.com/ahmadmughees/SH17dataset, release v1, 16 чекпойнтов YOLOv8/9/10 n..x). Но класса «no helmet» там нет: нарушение = `head` без `helmet`, выводится ассоциацией (inference). Данные CC BY-NC-SA 4.0 + условия Pexels; код Ultralytics AGPL-3.0. Метрики — на собственном test-split (1620 фото), не на CCTV.
2. Остальные HF-«PPE» веса любительские: классы и версия библиотеки читаются из самого чекпойнта, датасет чаще лишь по имени Roboflow-экспорта либо не назван, метрики самозаявлены. Карточки местами расходятся с чекпойнтами (см. Противоречия).
3. → linq_platform: готовых LinQ/int8 PPE-весов не найдено; все кандидаты — Ultralytics PyTorch `.pt` (у Hexmon ещё `best.onnx`, не проверялся). AXERA `.axmodel` — другая NPU.
4. → datasets: «Roboflow construction-site-safety»-таксономия (`Hardhat/NO-Hardhat/Safety Vest/NO-Safety Vest/Person…`) встречается в нескольких независимых весах; наборы классов различаются (таблица).
5. Версии Ultralytics в чекпойнтах: 8.0.23 (keremberke, старые пути модулей `ultralytics.yolo.utils`), 8.2.38 (SH17), 8.3.232 / 8.3.236 / 8.4.2 / 8.4.21 / 8.4.30. Загрузка 8.0.23-чекпойнта современным ultralytics — hypothesis, не проверялось.

## Резюме для оркестратора
- Ответ на главный вопрос: **да, ровно один полноценный кандидат — SH17 с 16 весами**; остальные частично прослеживаемы или не прослеживаемы.
- Решение: как стартовую точку брать COCO-pretrained базу + fine-tune на собранном датасете; SH17-веса — как эталон/альтернативная инициализация и как источник таксономии `person/head/helmet/safety-vest`. Лицензия SH17 (NC) — вопрос к hackathon_strategy.
- Для «человек без каски» нужны person + head (+helmet). По таксономии подходят: SH17, leeyunjai/yolo11-ppe (helmet,no-helmet,no-vest,person,vest), melihuzunoglu (helmet,human,no-helmet,vest), Hansung-Cho/Hexmon (…NO-Hardhat…Person…). Без person: keremberke yolov8 (Hardhat/NO-Hardhat), leeyunjai helmet-* (helmet/face) — связь с человеком только геометрией.
- Метрики несопоставимы (разные датасеты, val самого датасета); ни один вес не проверен на производственном/CCTV видео. SH17 cross-domain на Pictor-PPE: mAP50 ~58.8 (yolo9e, авторы) против 70.9 на своём test — деградация на чужом домене.
- Слабое место даже SH17: safety-vest mAP50 57.7 (yolo9e), helmet 77.0.
- Локально сделано: скачано 10 небольших `.pt` (каталог SCRATCH-уровня `%TEMP%\w105\dl\…`, не ROOT), sha256 сверены с LFS oid (HF) там, где oid известен; классы/версия/args прочитаны статическим разбором pickle-кода. Ничего не загружалось через torch/ultralytics и не запускалось; пакет onnx не ставился, ONNX не качался (наименьший — Hexmon, 103 МБ, не нужен).

## Факты
Формат: ID | утверждение | основание | источник | оговорки/статус.

- **W1-05-F01** | SH17: 8099 изображений, 75994 экземпляра, 17 классов; фото с Pexels (запросы вроде «manufacturing worker», «industrial worker»); макс. разрешение 8192×5462, мин. 1920×1002. | author_statement | S01, S02 | прочитано; сами изображения не скачивались.
- **W1-05-F02** | SH17 split: тест (в README «val») 1620 изображений / 15358 экземпляров, случайная выборка (80/20); списки `train_files.txt` / `test_files.txt` идут с датасетом (Kaggle). | author_statement | S01, S02 | списки не скачивали. Сводка статьи получена через WebFetch (не дословно).
- **W1-05-F03** | SH17 обучение: transfer от COCO, 200 эпох, imgsz 640, batch 128 (n) … 32 (крупные). В чекпойнтах yolo8n/9t/10n: epochs=200, imgsz=640, batch=128, `data: .../safe_human.yaml`. | author_statement + local_observation | S02, S03 | args читаются статически.
- **W1-05-F04** | SH17 классы и порядок в **чекпойнте** (yolo8n, yolo9t, yolo10n идентичны) и в `sh17.yaml`: 0 person, 1 ear, 2 ear-mufs, 3 face, 4 face-guard, 5 face-mask, 6 foot, 7 tool, 8 glasses, 9 gloves, 10 helmet, 11 hands, 12 head, 13 medical-suit, 14 shoes, 15 safety-suit, 16 safety-vest. | source_code (sh17.yaml @2f832c28) + local_observation | S01, S03 | нумерованный список в README даёт другой порядок — см. Противоречия.
- **W1-05-F05** | SH17 метрики (README, test 1620 фото, imgsz 640, среднее по 17 классам), mAP50/mAP50-95: yolo8n 58.0/36.6; yolo8s 63.7/41.7; yolo8m 66.6/45.7; yolo8l 68.0/47.0; yolo8x 69.3/47.2; yolo9t 58.5/37.5; yolo9s 65.3/42.9; yolo9m 68.6/46.5; yolo9c 67.7/46.5; yolo9e 70.9/48.7; yolo10n 57.2/35.9; yolo10x 67.8/46.7. Для yolo9e по классам (статья) mAP50/50-95: helmet 77.0/57.6, head 93.5/74.3, person 92.1/77.9, safety-vest 57.7/38.1. | reported_measurement (авторы) | S01, S02 | не воспроизводилось.
- **W1-05-F06** | SH17 cross-domain: yolo9e на Pictor-PPE (654 изображения, 3477 экз.; worker→Person, hat→Helmet, vest→Safety-vest) mAP50 58.8–58.9; person 85.5, helmet 55.5, safety-vest 35.5. | reported_measurement | S02 | не воспроизводилось.
- **W1-05-F07** | SH17 веса: release `v1` (2024-07-04), 16 файлов `yolo{8,9,10}*.pt`; размеры по API: yolo8n 6 252 377 B, yolo9t 4 647 738 B, yolo10n 5 771 812 B, yolo8x 136 735 401 B, yolo9e 117 283 098 B. Мои sha256: yolo8n `5449f62bd7cf30c01c7fd138db2729a38abcb4d5120449773fba475d54f30b62`; yolo9t `2de24c4ed24cc4b516c40e25e6d9f3cee91803ddddf2d398db91b5a17a91962a`; yolo10n `8a7e282066c8d0944a9fc8eac47c803439825056c50beb192ef8c36816b4a556`. В чекпойнтах: ultralytics `8.2.38`, даты 2024-06-22/24/25, AGPL-3.0. Архитектурные классы (из глобалов pickle): yolo8n — C2f/DFL/SPPF/Detect; yolo9t — RepNCSPELAN4/ELAN1/AConv/SPPELAN; yolo10n — C2fCIB/SCDown/PSA/v10Detect. | artifact_metadata + local_observation | S01, S03 | файлы получены (размер yolo8n на диске 6 252 377 B совпал с API); модель не загружалась. Release API не отдаёт digest.
- **W1-05-F08** | README SH17 требует `ultralytics==8.0.38`, чекпойнты содержат `version 8.2.38` (YOLOv9/v10 в 8.0.38 не существовали). | author_statement vs local_observation | S01, S03 | вероятно опечатка README (hypothesis).
- **W1-05-F09** | SH17 лицензия данных: CC BY-NC-SA 4.0 + правила Pexels; файла LICENSE в репо нет (contents API: 404). Лицензия весов отдельно не заявлена; в чекпойнте строка AGPL-3.0 (Ultralytics). | author_statement + local_observation | S01, S03 | юридический вывод не делался.
- **W1-05-F10** | keremberke/yolov8n-hard-hat-detection @`287bafa2feb311ee45d21f9e9b33315ff6ff955d`: `best.pt` 6 229 688 B, sha256 `05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c` (= LFS oid, мой хеш совпал); классы в чекпойнте `['Hardhat','NO-Hardhat']`; ultralytics 8.0.23; `model: yolov8n.yaml`; `data: D:\dev\yolov5\datasets\Hard-Hats-2/data.yaml`; optimizer SGD; imgsz 640; batch 8; epochs в args = 2; карточка: mAP@0.5(box) 0.83633, split validation, input_size 640. Person нет. | artifact_metadata + local_observation + author_statement | S04, S05 | epochs=2 сомнителен (возможно resume); не уточнено. Существуют также yolov8s (890 загр.), yolov8m (@65c3a88d, 52 007 840 B).
- **W1-05-F11** | Датасет keremberke/hard-hat-detection = экспорт Roboflow «Hard Hats» v2 (`roboflow-universe-projects/hard-hats-fhbh5`, экспорт 2023-01-16): labels `['hardhat','no-hardhat']`, train 13782 / valid 3962 / test 2001; CC BY 4.0. | author_statement | S06 | страница Roboflow недоступна (HTTP 403). Размер train, вероятно, включает аугментации экспорта — hypothesis.
- **W1-05-F12** | keremberke/yolov5{n,s,m}-construction-safety (yolov5 7.0.6; v5n @`5470ce96`): 17 классов (Barricade, Dumpster, EXCAVATORS, Gloves, Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Net, Safety Shoes, Safety Vest, dump truck, mini-van, truck, wheel loader — из чекпойнта v5n); mAP@0.5 val = 0.3654 (n); датасет Roboflow construction-site-safety v1: train 307 / valid 57 / test 34. | author_statement + local_observation | S07, S08 | слишком мал; отброшен.
- **W1-05-F13** | Hansung-Cho/yolov8-ppe-detection @`ac0027bd38bc619d5ce4f52b4cc01beb87d8b958`: `best.pt` 6 250 090 B, sha256 `2419700bbe3b8d38f9000655d9cf952a4bc93ef6c143baf8b49a0abde5d0760f` (= LFS oid); карточка MIT; чекпойнт: ultralytics 8.3.232, 2025-11-26, `model: yolov8n.pt`, epochs 30, batch 16, imgsz 640; классы (10) в порядке чекпойнта: Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, vehicle. Карточка: mAP50 0.744, mAP50-95 0.436, P 0.831, R 0.685 (Validation, «Kaggle public datasets», без имени). | local_observation + author_statement | S09 | датасет не атрибутирован; совпадение классов с Roboflow «construction site safety» — hypothesis.
- **W1-05-F14** | Hexmon/vyra-yolo-ppe-detection @`08895b33d95d2587423ebe4f7c1b9c41beebd642` (2026-02-18): YOLOv8m, `best.pt` 52 056 210 B (LFS oid `2b33d4d016f9751c5a25f4a72ce050e0a7e4e140b11c1669978d7154003a4f61`, не скачивался), `best.onnx` 103 655 282 B (oid `b99fed37…f246`), `args.yaml` (model yolov8m.pt, imgsz 640, epochs 100, batch 16, `data: ppe_dataset/data.yaml`), results.csv, эпоха 100: P 0.714, R 0.846, mAP50 0.7827, mAP50-95 0.5395 (val-split обучения). Классы (14) по карточке: 0 Fall-Detected, 1 Gloves, 2 Goggles, 3 Hardhat, 4 Ladder, 5 Mask, 6 NO-Gloves, 7 NO-Goggles, 8 NO-Hardhat, 9 NO-Mask, 10 NO-Safety Vest, 11 Person, 12 Safety Cone, 13 Safety Vest. Датасет по карточке: Roboflow «PPE Combined Model v4», CC BY 4.0. | artifact_metadata + author_statement | S10 | классы только из карточки, чекпойнт не скачивался; Roboflow недоступен; карточка говорит batch 32, args 16.
- **W1-05-F15** | leeyunjai/yolo11-ppe @`b530c9be5f366bac778c1499abee354f029b7ca1`: `ppe-11s.pt` 19 195 674 B (sha `5dd199a9562f6d001234ed3620574cd152e896fa9600388a2789114cc877553d`), `ppe-11x.pt` 114 409 305 B; классы в чекпойнте и карточке: helmet, no-helmet, no-vest, person, vest; ultralytics 8.3.236, 2025-12-16, base `yolo11s.pt`, epochs 300, batch 50, imgsz 640; `data: /home/circulus/datasets/construction safety.v2-release.yolov11/data.yaml` (имя Roboflow-экспорта). Метрик для ppe-* нет, лицензия не указана. | local_observation + artifact_metadata | S11 | датасет не атрибутирован. Заголовок карточки — копипаст «Number and Operator Detection».
- **W1-05-F16** | leeyunjai/yolo11-helmet @`ae517931186c4dba2a3ea9b0f5dcfff6284dff74`: helmet-11{s,m,x}.pt (11s 19 195 226 B, sha `4ab0aec8a351bf051e61966652afcd1e7990b85a8bb789826d811151d7cb1172`); классы чекпойнта: `helmet`, `face` (карточка: «helmet / face (no helmet)»); ultralytics 8.4.21, 2026-03-25, base `ul://ultralytics/yolo11/yolo11s`, epochs 1000, batch 32, project `yunjai-lee/helmet-3`. Карточка: mAP50 0.9586, mAP50-95 0.6495, P 0.913, R 0.930 для «yolo11x», split не указан. Аналог leeyunjai/yolo26-helmet @`b6e44912` (helmet-26s.pt sha256 `e746f67fd459f38839fcd5207324fb5c503b0aaeae51b751b260e730e03f6a6d`): ultralytics 8.4.30, base `yolo26s`, epochs 650, batch 77, те же классы helmet/face. | local_observation + author_statement | S12, S13 | датасет не опубликован; person нет.
- **W1-05-F17** | melihuzunoglu/ppe-detection @`aed7807c358836eef5a6f67af27dd970ade6fb18`: `best.pt` 5 475 290 B (sha `a00b6fce124e63c5d23f44792593983b70e646008b58bc54cf5b0a1c87ba2119`), карточка AGPL-3.0; чекпойнт: ultralytics 8.4.2, 2026-01-15, base `yolo11n.pt`, epochs 50, batch 16, imgsz 640, `data: /kaggle/working/PPE-Detection-2/data.yaml`; классы чекпойнта: helmet, human, no-helmet, vest; «No-Vest» как класса нет (логика: отсутствие vest в боксе human); метрик нет. | local_observation + author_statement | S14 | датасет не атрибутирован.
- **W1-05-F18** | Лицензии: код Ultralytics в чекпойнтах AGPL-3.0; карточки: MIT (Hansung-Cho), CC-BY-4.0 (Hexmon; фактически датасет), AGPL-3.0 (melih, AXERA), не указана (keremberke, leeyunjai). Лицензия весов ≠ лицензия данных. | artifact_metadata | S04–S16 | юридический вывод не делался.
- **W1-05-F19** | qualcomm/PPE-Detection (`gear_guard_net`; ai-hub-models tag v0.65.0 → commit `18659f27b115a1daf5bca255225e86434b48e9c9`): архитектура Qualcomm, anchor-based декодирование YOLOv5-стиля, strides 8/16/32; вход 320×192; 6.19M параметров; 2 выходных класса; обучена на «proprietary dataset»; веса из asset store Qualcomm; BSD-3. Docstring model.py «person/face detection», `app.py` берёт `get_class_names("ppe")` с примером «helmet, vest». | primary_documentation + source_code | S15 | список имён «ppe» не читал. Данные и метрики недоступны → не прослеживается.
- **W1-05-F20** | AXERA-TECH/Helmet-axera @`c48ec87e8e0c65618560d790d598c1081a857d92`: 4 класса helmet, head, e-bike, bike; сценарий — водители двухколёсного транспорта; `.axmodel` для AX620E/AX650 (w8a16), AGPL-3.0. | author_statement + artifact_metadata | S16 | не подходит.
- **W1-05-F21** | Датасет Kaggle «Hard Hat Detection» (andrewmvd; зеркало Voxel51/hard-hat-detection HF): 5000 изображений, VOC, классы Helmet / Person / Head, cc0-1.0; происхождение — makeml.app «Hard Hat Workers». Отдельных весов не прослеживал (HF-модели `*detr-resnet-50-hardhat-finetuned` — учебные DETR). | author_statement | S17 | Kaggle не открывался.
- **W1-05-F22** | SHWD: 7581 изображений; классы `hat` (в каске) и `person` (голова без каски, «normal head»); 9044 positive, 111514 negative; источники Google/Baidu и SCUT-HEAD; VOC; MIT; предобученные модели — MXNet GluonCV YOLOv3 (darknet53 mAP 88.5, mobile1.0 86.3, mobile0.25 75.0). | author_statement | S18 | `person` в SHWD = голова. Условия оценки mAP в README не проверялись.
- **W1-05-F23** | GDUT-HWD, CHV, Pictor-PPE: полные размеры и классы в этом запуске не подтверждены (поиск не вернул); из статьи SH17 известно только: тест Pictor-PPE 654 изображения / 3477 экз., классы worker/hat/vest. | reported_measurement (частично) + unknown | S02 | → datasets. Поиск HF по `gdut`/`shwd` готовых моделей не дал (0 моделей).

## Источники
- W1-05-S01: ahmadmughees/SH17dataset (GitHub), default branch `master`, commit `2f832c289f9deea063367045ed8230b26e3e7ea9`; README, `sh17.yaml`, releases tag `v1` (2024-07-04T20:23:53Z). Проверено 2026-10-23 ~04:55 MSK; доступ полный.
- W1-05-S02: Ahmad & Rahimi, «SH17: A dataset for human safety and PPE detection in manufacturing industry», arXiv 2407.04590 v1; J. Safety Sci. Resilience, doi 10.1016/j.jnlssr.2024.09.002. Прочитано через сводку WebFetch (не дословно). ~04:57.
- W1-05-S03: локальные `yolo8n.pt`, `yolo9t.pt`, `yolo10n.pt` из S01 release v1; статический разбор data.pkl.
- W1-05-S04: HF `keremberke/yolov8n-hard-hat-detection` rev `287bafa2…`; создан 2023-01-29; также `yolov8m` rev `65c3a88dc3fda5dd22711a55c46d079e2c95e2cf`.
- W1-05-S05: локальный best.pt из S04.
- W1-05-S06: HF dataset `keremberke/hard-hat-detection` README.
- W1-05-S07: HF `keremberke/yolov5n-construction-safety` rev `5470ce96c992f609fae66d14e219c3b010b172c0`.
- W1-05-S08: HF dataset `keremberke/construction-safety-object-detection` README (Roboflow `roboflow-universe-projects/construction-site-safety` v1).
- W1-05-S09: HF `Hansung-Cho/yolov8-ppe-detection` rev `ac0027bd…` (GitHub Hansung-Cho/YOLO_PPE упомянут, не открывался).
- W1-05-S10: HF `Hexmon/vyra-yolo-ppe-detection` rev `08895b33…`: README, args.yaml, results.csv.
- W1-05-S11: HF `leeyunjai/yolo11-ppe` rev `b530c9be…`.
- W1-05-S12: HF `leeyunjai/yolo11-helmet` rev `ae517931…`.
- W1-05-S13: HF `leeyunjai/yolo26-helmet` rev `b6e44912…`.
- W1-05-S14: HF `melihuzunoglu/ppe-detection` rev `aed7807c…`.
- W1-05-S15: HF `qualcomm/PPE-Detection` rev `64bcb058…`; GitHub qualcomm/ai-hub-models tag v0.65.0 (`src/qai_hub_models/models/gear_guard_net/{model.py,app.py,manifest.yaml}`).
- W1-05-S16: HF `AXERA-TECH/Helmet-axera` rev `c48ec87e…`.
- W1-05-S17: HF dataset `Voxel51/hard-hat-detection` README.
- W1-05-S18: github.com/njvisionpower/Safety-Helmet-Wearing-Dataset (сводка WebFetch; commit не фиксировал).
- Недоступно: universe.roboflow.com (HTTP 403 у WebFetch); Kaggle не открывался. Поиск HF-API: запросы helmet, hardhat, hard-hat, ppe, safety vest, construction-safety, sh17, shwd, yolo11 ppe, yolov8 ppe, yolov10 helmet, rtdetr ppe (сортировка downloads — только для обнаружения).

## Таблица таксономий (порядок = индекс, где источник — чекпойнт)
| Артефакт | Классы | person | «без каски» | vest |
|---|---|---|---|---|
| SH17 (чекп.) | person, ear, ear-mufs, face, face-guard, face-mask, foot, tool, glasses, gloves, helmet, hands, head, medical-suit, shoes, safety-suit, safety-vest | да | нет; head без helmet | safety-vest, no-vest нет |
| keremberke yolov8 (чекп.) | Hardhat, NO-Hardhat | нет | явный | нет |
| keremberke yolov5 (чекп.) | 17 классов с Hardhat, NO-Hardhat, Person, Safety Vest, NO-Safety Vest, Mask, NO-Mask и техникой | да | явный | оба |
| Hansung-Cho (чекп.) | Hardhat, Mask, NO-Hardhat, NO-Mask, NO-Safety Vest, Person, Safety Cone, Safety Vest, machinery, vehicle | да | явный | оба |
| Hexmon (карточка) | 14 классов, см. F14 | да | явный | оба |
| leeyunjai ppe (чекп.) | helmet, no-helmet, no-vest, person, vest | да | явный | оба |
| leeyunjai helmet-*/yolo26 (чекп.) | helmet, face | нет | face = голова без каски (по карточке) | нет |
| melihuzunoglu (чекп.) | helmet, human, no-helmet, vest | да | явный | no-vest не класс |
| SHWD (датасет) | hat, person(=голова без каски) | нет | person-голова | нет |
| Kaggle Hard Hat (датасет) | Helmet, Person, Head | да | Head без Helmet | нет |

«Hardhat/NO-Hardhat» в Roboflow-наборах — бокс на голове/каске, а `Person` — на всё тело (по классовой семантике названий; границы боксов не проверялись → inference). Ассоциация «нарушение = person, у которого голова без каски» делается геометрически: head/NO-Hardhat-бокс внутри верхней части person-бокса и нет helmet-бокса, перекрывающего head (inference, не опробовано).

## Разборы
**1. SH17 (эталон/инициализация).** Цепочка: статья → Pexels-данные (Kaggle) → `sh17.yaml` + train/test-списки → Ultralytics 8.2.38 → 16 `.pt` → метрики. Плюсы: person/head/helmet/safety-vest, сильные head (93.5) и person (92.1) у 9e; малые варианты (yolo8n 6.25 МБ). Минусы: нет no-*; vest слабый; лицензия NC; фото Pexels не CCTV (ракурс авторами не указан); 17 классов, из которых большинству не нужны; обучение на 640. Для нас: remap в {person, head, helmet, vest}, остальные классы игнорировать, fine-tune на своих кадрах.

**2. keremberke hard-hat (быстрый baseline).** Два класса без person; ultralytics 8.0.23; датасет Roboflow Hard Hats v2 (CC BY 4.0); mAP50 0.836 на val датасета. Годится для смоук-теста, не как эталон (нет person; старый формат; split/дубликаты не проверены).

**3. Hexmon vyra (ближайшая «violation»-таксономия).** Hardhat/NO-Hardhat/Safety Vest/NO-Safety Vest/Person + Mask/Gloves/Goggles; mAP50 0.783 на val; есть args.yaml и results.csv, ONNX. Датасет заявлен, но не проверен; per-class метрик не получено; есть классы, относящиеся к W1-16 (Fall-Detected, Ladder).

**4. leeyunjai (yolo11-ppe, yolo11-helmet, yolo26-helmet).** Свежие версии, размеры s/m/x, классы согласованы с карточкой. Но датасеты не опубликованы, лицензия не указана, метрика только helmet-11x (mAP50 0.9586, split не указан). Baseline, не эталон.

**5. Hansung-Cho и melihuzunoglu.** Любительские: YOLOv8n/10 классов/30 эпох (mAP50 0.744 по карточке) и YOLO11n/4 класса/50 эпох без метрик.

**Отброшено:** keremberke yolov5 (датасет 307 фото, mAP50 0.365); qualcomm PPE-Detection (2 класса неясной семантики, данные proprietary, вход 320×192); AXERA Helmet (другая NPU, мотоциклисты); DETR/RT-DETR hardhat fine-tune'ы (десятки учебных копий; архитектура не из списка LinQ, inference); DETA helmet; пустые репозитории с 0 загрузок (`kucheroleksii777/PPE_DETECTION_SCORE*`, `wesjos/Yolo-hard-hat-safety-vest`) — не открывались.

## Противоречия
1. SH17 README `ultralytics==8.0.38` против чекпойнтов `8.2.38` (F08): для воспроизведения брать версию из чекпойнта; закрыть экспериментом E1.
2. SH17 README: нумерованный список классов (Person, Head, Face … Helmet=15) ≠ порядок в sh17.yaml/чекпойнте (helmet=10, head=12, person=0). Использовать индексы чекпойнта.
3. Hexmon: batch 32 (карточка) vs 16 (args.yaml); CC BY 4.0 в карточке относится к датасету.
4. keremberke yolov8n: epochs=2 в args при mAP50 0.836 — не согласуется с обучением с нуля; полный args не разбирался.
5. qualcomm gear_guard_net: «person/face» (docstring) vs «helmet, vest» (app.py) vs 2 класса.
6. SHWD `person` = голова без каски, в остальных наборах `person` = всё тело: прямое слияние ломает смысл.
7. leeyunjai: заголовок карточки (числа/операторы) не соответствует содержимому; ориентироваться на чекпойнт.

## Открытые вопросы
1. Как в SH17 размечена `head` у человека в каске (есть ли head одновременно с helmet)? Статья не говорит. Закрыть: Kaggle-датасет, подсчёт пересечений head/helmet по меткам.
2. Состав и дубликаты Roboflow-наборов (Hard Hats v2, PPE Combined Model v4, construction safety v2): число уникальных фото, ракурс, утечка train/val. Roboflow недоступен (403); закрыть: открыть в браузере / зеркало.
3. Per-class метрики Hexmon/Hansung-Cho: локальный val на нашем наборе.
4. Принимает ли компилятор LinQ графы YOLOv8/9/10/11 из этих весов (DFL, Concat, Resize, NMS-free v10 head) — → linq_platform.
5. Юридическая допустимость SH17 (NC-SA, Pexels) и AGPL-весов на хакатоне — → hackathon_strategy.
6. Публичные веса на GDUT-HWD/CHV/Pictor-PPE: HF не показал; GitHub глубоко не искался (`gh search repos` по запросу SH17 вернул пусто).

## Предлагаемые эксперименты
- **E1 (воспроизведение SH17).** Вопрос: воспроизводятся ли метрики yolo8n (mAP50 58.0) на SH17 test. Кандидат: SH17dataset@2f832c28, `v1/yolo8n.pt` (sha 5449f62b…). Окружение: venv в SCRATCH, ultralytics 8.2.38 (по чекпойнту; доступность версии проверить). Шаги: получить датасет с Kaggle (нужен доступ), поправить пути в списках скриптом репо (сначала прочитать), запустить `model.val(data="sh17.yaml", imgsz=640)` как в README. Измерять P/R/mAP по классам, особенно helmet/head/person/safety-vest. Не подтверждает: перенос на наш CCTV и совместимость с LinQ. Стоп: при недоступности датасета не подменять другим без пометки.
- **E2 (видео заказчика, когда будет).** Прогнать SH17-yolo8n/yolo9t и leeyunjai ppe-11s как baseline на 100–200 вручную размеченных кадрах; метрика на уровне нарушения (person без каски), не mAP.
- **E3 (ассоциация person↔head/helmet).** На SH17 val посчитать, для какой доли person-боксов находится head-бокс внутри верхней части person; порог доли площади; псевдокод: для каждого head найти person с максимальной долей площади head внутри person; head без перекрывающего helmet — нарушение. Сохранить confusion по парам.
- **E4 (экспорт ONNX yolo8n SH17).** Только после согласования с linq_platform (opset, форма входа, NMS внутри/вне графа); в этом запуске не выполнялся.

## Передачи соседям
- → datasets: первичные наборы и таксономии (SH17; Kaggle Hard Hat Helmet/Person/Head 5000; SHWD hat/person(=голова) 7581; Roboflow Hard Hats v2; Roboflow construction-site-safety 17 классов; «PPE Combined Model v4» и «construction safety v2» не проверены; GDUT-HWD/CHV/Pictor-PPE размеры не подтверждены). Проверить head при каске в SH17, ракурсы, лицензии (SH17 NC-SA + Pexels; Roboflow CC BY 4.0; Kaggle Hard Hat CC0 по зеркалу).
- → training_strategy: инициализация COCO-base vs SH17; ремап person/head/helmet/vest; `no-helmet` как класс или вывод из head-без-helmet; при imgsz 640 маленькие головы на 1920×1080 CCTV теряют пиксели.
- → evaluation: метрика уровня нарушения; опубликованные mAP получены на фото-наборах; ориентир деградации SH17→Pictor-PPE 58.8 mAP50.
- → linq_platform: все кандидаты — Ultralytics PyTorch; нужно уточнить, какие реализации стоят за yolo5s/yolo8/yolo11 на lin-q.ru и совпадают ли с головами Ultralytics (v8 DFL Detect, YOLO11 C3k2/C2PSA); Hexmon публикует best.onnx (не проверен).
- → video_architecture: двухстадийная схема (person → crop головы → классификатор каски) против единого детектора.
- → hackathon_strategy: лицензионные риски SH17 (NC-SA) и Ultralytics (AGPL).

## Запросы эскалации
- Критичных нет. Желательно более сильному исследователю: (а) состав Roboflow-наборов (403 для меня); (б) полный E1 с Kaggle-данными.

Критерий завершения выполнен: есть артефакт (SH17) с прослеживаемыми классами/данными/архитектурой; для остальных указано, что именно мешает.
