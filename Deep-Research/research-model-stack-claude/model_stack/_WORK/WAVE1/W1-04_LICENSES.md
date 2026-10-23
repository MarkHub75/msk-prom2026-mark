# W1-04 LICENSES — условия использования кода, весов и данных

- ID ячейки: W1-04. Запрошено: Claude Sonnet 5.5, effort medium.
- Фактическая модель (из системного окружения): «Sonnet 5.5», model ID `claude-sonnet-5-5`.
- Время: начало 2026-10-23 ~04:43 MSK, конец ~05:10 MSK. Все проверки URL — 2026-10-23.
- Это карта опубликованных условий, не юридическое заключение.

## FLASH
1. Ultralytics (ultralytics.com/license): AGPL-3.0 заявлена на «the models produced by that training code»; дообученные/кастомные модели в проприетарной/коммерческой среде названы триггером Enterprise License. Про экспортированные модели и выводы (outputs) страница ничего не говорит (ONNX-экспорт — unknown). Ultralytics-путь для пилота = открывать весь проект под AGPL-3.0 либо Enterprise.
2. Apache-2.0 по коду: RT-DETR, D-FINE, DEIM, YOLOX, PaddleDetection, mmdetection, NanoDet; RF-DETR N/S/M/L — Apache-2.0 и код, и «Apache-designated» веса. D-FINE прямо предупреждает: чекпоинты Objects365 (`*_obj365`, `*_obj2coco`) «should not be assumed to be commercially cleared». RF-DETR Atto/Femto/Pico/XL/2XL — PML 1.0 (текст PML не читан).
3. YOLO-NAS: код super-gradients Apache-2.0, но веса под лицензией Deci: «you may not use the Software for any commercial use». Пример «лицензия кода ≠ лицензия весов».
4. Copyleft по коду: GPL-3.0 — WongKinYiu/yolov7, yolov9, meituan/YOLOv6, mmyolo, PaddleYOLO; AGPL-3.0 — THU-MIG/yolov10, sunsmarterjie/yolov12. MIT — MultimediaTechLab/YOLO.
5. Данные: ImageNet, CrowdHuman — non-commercial research/education; Objects365 — academic only; SH17 — CC BY-NC-SA 4.0; COCO — аннотации CC BY 4.0, изображения под Flickr ToU (права не даёт).
6. Общий разрыв: цепочка «условия обучающих данных -> веса» первичными документами не разрешена нигде, кроме отдельных замечаний (D-FINE, torchvision).

## Резюме для оркестратора
- Для каждого кандидата разделены код / веса / данные (таблица §2).
- Самое чёткое и самое ограничивающее заявление — у Ultralytics; GitHub, сайт и HF-карточки (`Ultralytics/YOLO11`, `YOLOv8`: agpl-3.0) согласованы, противоречий нет.
- Наименее ограничивающие по найденным документам: Apache-2.0 код (RT-DETR/D-FINE/DEIM/YOLOX/RF-DETR N-L). У большинства условия весов не заявлены (категория «сведений нет», не разрешение). Вопрос по данным (COCO/Flickr, Objects365) остаётся.
- PPE-наборы: SHWD — MIT только на репозиторий, права на изображения не заявлены; SH17 — NC; CHV, Pictor-PPE, GDUT-HWD — лицензии нет; Hard Hat Workers — страницы Roboflow отдали 403, лицензия только вторично (Public Domain).
- Главные разрывы: (a) регламент хакатона/IP и условия пилота (полного кейса нет); (b) AGPL для сетевого сервиса и ONNX-экспорта — нужен юрист/запрос вендору; (c) не получены тексты PML 1.0 и ImageNet access agreement; (d) лицензии конкретных чекпоинтов (YOLOX, Paddle, RT-DETR, DEIM, NanoDet) не найдены.
- Inference (не юр. вывод): основной путь держать на Apache-кодовых кандидатах, Ultralytics — как явно оговорённый вариант; обучать на наборе с известной лицензией, фиксируя лицензию каждого источника.
- Файлов W1-05/W1-16 в WAVE1 на момент работы не было — PPE-веса из них не проверены.

## 1. Факты

| ID | Утверждение | Основание | Источник | Применимость / статус проверки |
|---|---|---|---|---|
| W1-04-F01 | Ultralytics: «All Ultralytics YOLO trained models fall under the AGPL-3.0 License by default.»; «The AGPL-3.0 License covers the training code and the models produced by that training code.» | author_statement | S01 | сайт на 2026-10-23, даты редакции нет; прочитано через WebFetch (пересказ инструментом, не побуквенная сверка) |
| W1-04-F02 | Триггер Enterprise License: «Using custom-trained or fine-tuned YOLO models in a proprietary or commercial setting»; соблюдение AGPL = публикация полного исходного кода производной работы и «where applicable, model weights». | author_statement | S01 | то же |
| W1-04-F03 | Страница S01 не упоминает экспортированные модели и outputs; docs FAQ и guides/model-deployment-options лицензионных формулировок не содержат. | unknown | S01, S02 | охват: ultralytics.com/license, docs.ultralytics.com/help/FAQ/, guides/model-deployment-options/, README ultralytics@e6d5fc5 |
| W1-04-F04 | Код ultralytics, yolov5, assets: LICENSE = GNU AGPL v3. README: Enterprise License «enables seamless integration of Ultralytics software and AI models into business products and services … bypassing the open-source requirements of AGPL-3.0». | artifact_metadata + author_statement | S02, S03 | ultralytics@e6d5fc5918f5…, yolov5@b64813c026a0…, assets@af08ba156fd5… (HEAD на проверке); LICENSE прочитан |
| W1-04-F05 | HF `Ultralytics/YOLO11` (sha 8b8ac7d1…) и `Ultralytics/YOLOv8` (sha 27f858f2…): cardData.license = agpl-3.0; совпадает с GitHub/сайтом. | artifact_metadata | S04 | API получен |
| W1-04-F06 | ultralytics/assets: последний релиз v8.4.0 «New YOLO26 Models Release» (2026-01-13); v8.3.0 — YOLO11 (2024-09-29). | artifact_metadata | S03 | gh release list |
| W1-04-F07 | Maintainer в issue #2129 (по поисковой выдаче): обучающий код и модели под AGPL; пользователь в треде оспаривал. | author_statement + мнение третьего лица | S05 | только snippet поиска, не открывалось |
| W1-04-F08 | YOLOX: корневой LICENSE Apache-2.0; в README лицензии весов нет; веса — GitHub release 0.1.1rc0 (`yolox_s.pth`…). | artifact_metadata; веса — unknown | S06 | main, pushed 2025-06-08; SHA не фиксирован |
| W1-04-F09 | PaddleDetection: README «PaddlePaddle is provided under the Apache 2.0 license»; MODEL_ZOO_en: «the LICENSE of PaddleYOLO is GPL 3.0». Условия весов model zoo не найдены. | primary_documentation | S07 | release/2.9; README прочитаны |
| W1-04-F10 | mmdetection Apache-2.0; mmyolo GPL-3.0 (GitHub API). Веса не проверялись. | artifact_metadata | S08 | только метаданные |
| W1-04-F11 | torchvision: код BSD-3-Clause; docs: «The pre-trained models provided in this library may have their own licenses or terms and conditions derived from the dataset used for training. It is your responsibility to determine whether you have permission to use the models for your use case.» | primary_documentation | S09 | docs/source/models.rst, main |
| W1-04-F12 | tensorflow/models: SPDX NOASSERTION; корневой LICENSE начинается «Copyright 2022 Google LLC… All files in the following folders:» (составная). Лицензия весов TF OD Zoo не проверена. | artifact_metadata | S10 | только начало LICENSE |
| W1-04-F13 | yolov7 LICENSE.md = GPL-3.0; yolov9 = GPL-3.0 (API); README про веса лицензий не содержат. | artifact_metadata; веса — unknown | S11 | main |
| W1-04-F14 | MultimediaTechLab/YOLO README: «This is the official YOLO model implementation with an MIT License.» Веса отдельно не проверены. | author_statement | S12 | main, pushed 2026-03-16 |
| W1-04-F15 | THU-MIG/yolov10 AGPL-3.0; sunsmarterjie/yolov12 AGPL-3.0; meituan/YOLOv6 GPL-3.0 (GitHub API). | artifact_metadata | S13 | только метаданные |
| W1-04-F16 | YOLO-NAS: код super-gradients Apache-2.0; `LICENSE.YOLONAS.md`: «non-exclusive, revocable, non-sublicensable, non-transferable … limited right»; запрещено «distribute the Software»; «you may not use the Software for any commercial use, including in connection with any models used in a production environment» (кроме отдельного соглашения/Terms of Use). | primary_documentation | S14 | master, pushed 2026-02-24; файл прочитан |
| W1-04-F17 | RT-DETR (lyuwenyu): Apache-2.0 код; релизы предобученных на Objects365 моделей (R18/R50/R101). Условия весов не заявлены. | artifact_metadata | S15 | main |
| W1-04-F18 | D-FINE: Apache-2.0; README: «Checkpoints trained or pretrained on Objects365 (*_obj365, *_obj2coco) may be subject to the Objects365 dataset terms and should not be assumed to be commercially cleared under the D-FINE license.» | author_statement | S16 | master; README прочитан |
| W1-04-F19 | DEIM: LICENSE «DEIM is licensed under the Apache License» (INTELLINDUST…); SPDX NOASSERTION. Условия весов не найдены. | artifact_metadata | S17 | main |
| W1-04-F20 | RF-DETR: «The open-source `rfdetr` package and Apache-designated models are released under Apache 2.0, while Plus components (`rfdetr_plus`, including RF-DETR-Atto/Femto/Pico/XL/2XL detection models) are licensed under PML 1.0.» В таблице README: N/S/M/L — Apache 2.0, A/F/P — PML 1.0. | author_statement | S18 | develop, pushed 2026-10-22; текст PML не получен |
| W1-04-F21 | NanoDet: Apache-2.0 (API); PicoDet — часть PaddleDetection (F09). Веса не проверены. | artifact_metadata | S19 | main, 2024-08-08 |
| W1-04-F22 | COCO Terms of Use: аннотации и сайт «licensed under a Creative Commons Attribution 4.0 License»; «The COCO Consortium does not own the copyright of the images. Use of the images must abide by the Flickr Terms of Use.» | primary_documentation | S20 | репо сайта @5e1c4da (2023-11-09), dataset/termsofuse.htm |
| W1-04-F23 | Objects365: аннотации CC BY 4.0; изображения — Flickr ToU; «available for the academic purpose only»; «You will NOT distribute the above images». | primary_documentation | S21 | страница прочитана |
| W1-04-F24 | CrowdHuman: «You will use the data only for non-commercial research and educational purposes.» | primary_documentation | S22 | страница прочитана |
| W1-04-F25 | ImageNet: текст «terms of access» на первичной странице подключён PHP-include и не отдался; главная: «The data is available for free to researchers for non-commercial use.»; по перепечаткам в поиске: «Researcher shall use the Database only for non-commercial research and educational purposes», работодатель-коммерсант тоже связан. | primary_documentation (главная) + вторичные перепечатки | S23 | соглашение напрямую не получено |
| W1-04-F26 | SH17: «released under CC BY-NC-SA 4.0»; «intended for educational, research, and analysis purposes only»; изображения из Pexels (ссылка на Pexels license). | author_statement | S24 | @2f832c2; README прочитан |
| W1-04-F27 | SHWD: LICENSE репозитория MIT (2019 njvisionpower); README: «The positive objects got from goolge or baidu»; прав на изображения не заявлено. | artifact_metadata + author_statement | S25 | @c952631 |
| W1-04-F28 | CHV: «The dataset is open for free use»; файла LICENSE нет; изображения из интернета и открытых датасетов. | author_statement | S26 | @907fafd |
| W1-04-F29 | Pictor-PPE: README лицензии не содержит; Pictor-v3 = 774 crowd-sourced + 698 web-mined изображений, Google Drive. | artifact_metadata | S27 | @8f41c95 |
| W1-04-F30 | GDUT-HWD: в wujixiu/helmet-detection (код Apache-2.0 по API); README лицензии на изображения не заявляет. | artifact_metadata | S28 | @8eff5c5 |
| W1-04-F31 | Hard Hat Workers (Roboflow): public.roboflow.com -> 301 на universe.roboflow.com/joseph-nelson/hard-hat-workers; fetch страниц Universe вернул 403. По поисковой выдаче — «Public Domain», автор Northeastern University – China; на копиях встречается CC BY 4.0. | hypothesis (вторично) | S29 | первичное подтверждение отсутствует |

## 2. Карта условий

Категории: A = явно разрешено в тексте; B = опубликованные условия с ограничениями; C = сведений нет; D = противоречие.

| Кандидат | Код | Веса | Данные (база весов) | Значение |
|---|---|---|---|---|
| Ultralytics YOLOv5/8/11/26 | B: AGPL-3.0 (F04) | B: AGPL «by default», в т.ч. fine-tuned (F01-F02); экспорт/outputs — C (F03) | COCO: аннотации A, изображения B (F22) | Пилот/коммерция = публикация под AGPL или Enterprise |
| YOLOX | A: Apache-2.0 (F08) | C | COCO | веса молчат |
| PaddleDetection / PicoDet | A: Apache-2.0 (F09) | C | COCO/Objects365 (по конфигу) | PaddleYOLO — GPL-3.0 (B) |
| mmdetection | A: Apache-2.0 (F10) | C | по чекпоинту | mmyolo — GPL-3.0 (B) |
| torchvision | A: BSD-3 (F11) | B: «may have their own licenses» | COCO, ImageNet-init | прямое предупреждение автора |
| TF OD API | B/D: составная (F12) | C | COCO | читать полный LICENSE при выборе |
| yolov7 / yolov9 | B: GPL-3.0 (F13) | C | COCO | |
| WongKinYiu/YOLO | A: MIT (F14) | C | COCO | какие веса — проверить |
| YOLOv10 / v12 / v6 | B: AGPL / AGPL / GPL (F15) | C | COCO | |
| YOLO-NAS | A: Apache-2.0 | B: no commercial use (F16) | — | D между кодом и весами |
| RT-DETR | A: Apache-2.0 (F17) | C | COCO; Obj365-варианты B (F23) | |
| D-FINE | A: Apache-2.0 (F18) | B: предупреждение для obj365 (F18) | COCO/Obj365 | брать чекпоинты без Obj365 или оценить риск |
| DEIM | A: Apache-2.0 (F19) | C | COCO | |
| RF-DETR | A: Apache-2.0 (N/S/M/L); B: PML 1.0 (A/F/P/XL/2XL) (F20) | A для Apache-designated; PML не читан | COCO / RF100-VL | |
| NanoDet | A: Apache-2.0 (F21) | C | COCO/VOC | |

| Набор | Аннотации | Изображения | Категория |
|---|---|---|---|
| COCO | CC BY 4.0 | Flickr ToU | B |
| Objects365 | CC BY 4.0 | Flickr ToU, academic only | B |
| ImageNet | — | non-commercial research (по перепечаткам) | B |
| CrowdHuman | NC research/education | то же | B |
| SH17 | CC BY-NC-SA 4.0 | Pexels license | B |
| SHWD | репозиторий MIT | происхождение google/baidu, права не заявлены | C |
| CHV | «open for free use», без лицензии | интернет + открытые датасеты | C |
| Pictor-PPE | нет | crowd-sourced + web-mined | C |
| GDUT-HWD | нет | нет | C |
| Hard Hat Workers | Public Domain (вторично) | — | D / недоступно |

## 3. Противоречия
1. YOLO-NAS: код Apache-2.0 vs веса «no commercial use» — выбор: не брать веса.
2. SH17: CC BY-NC-SA vs «free» Pexels — эффективно строже (NC).
3. Hard Hat Workers: Public Domain vs CC BY 4.0 на разных копиях (вторично); оригинал 403.
4. Ultralytics: позиция вендора однозначна; оспаривание в issue #2129 — мнение третьего лица.
5. D-FINE/RT-DETR: код Apache-2.0, но Obj365-чекпоинты несут академические условия данных (оговаривает только D-FINE).

## 4. Открытые вопросы
1. Регламент хакатона/ХайТэк: права на решение, IP, допустимость AGPL/сторонних весов, условия пилота — полный кейс 23.10 13:00.
2. AGPL §13 для сетевого сервиса и статус ONNX-экспорта/outputs — юрист или запрос в Ultralytics Licensing.
3. Текст PML 1.0 — получить у Roboflow.
4. Первичный ImageNet access agreement — через image-net.org.
5. Лицензии конкретных чекпоинтов (YOLOX release 0.1.1rc0, Paddle model zoo, RT-DETR, DEIM, NanoDet) — страница релиза/карточка каждого выбранного файла.
6. Допустимость COCO-обученных весов — первичные документы COCO о весах молчат.
7. Лицензия конкретных проектов Roboflow Universe — только браузером (fetch 403); Universe terms не читались.

## 5. Источники (проверка 2026-10-23, ~04:45–05:10 MSK)
- S01: Ultralytics License, https://www.ultralytics.com/license (WebFetch).
- S02: ultralytics/ultralytics @e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 (LICENSE; README, раздел License ~строки 276-281).
- S03: ultralytics/assets @af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce (README License; releases); ultralytics/yolov5 @b64813c026a0a8924b193afa2badba244696f0ee.
- S04: https://huggingface.co/api/models/Ultralytics/YOLO11 (sha 8b8ac7d1fae7468f85dbf89670dd66f41f485aab), …/Ultralytics/YOLOv8 (sha 27f858f2dc238503a66ce10248cf7ec71a3ded5d).
- S05: https://github.com/ultralytics/ultralytics/issues/2129 (snippet поиска); community.ultralytics.com тред 1193; blog.roboflow.com/why-agpl-3-0-is-a-risk-for-computer-vision-teams/ (не открывались).
- S06: Megvii-BaseDetection/YOLOX (LICENSE, README, main). S07: PaddlePaddle/PaddleDetection README_en.md, docs/MODEL_ZOO_en.md (release/2.9). S08: mmdetection, mmyolo (API). S09: pytorch/vision LICENSE, docs/source/models.rst (main). S10: tensorflow/models LICENSE. S11: WongKinYiu/yolov7 LICENSE.md, yolov9 (API). S12: MultimediaTechLab/YOLO README. S13: THU-MIG/yolov10, sunsmarterjie/yolov12, meituan/YOLOv6 (API). S14: Deci-AI/super-gradients LICENSE.YOLONAS.md, README (master). S15: lyuwenyu/RT-DETR README. S16: Peterande/D-FINE README. S17: ShihuaHuang95/DEIM LICENSE. S18: roboflow/rf-detr README, LICENSE (develop). S19: RangiLyu/nanodet (API).
- S20: cocodataset/cocodataset.github.io dataset/termsofuse.htm @5e1c4da72464b1c6f068df0c02c91e3000ea62c4. S21: https://www.objects365.org/download.html. S22: https://www.crowdhuman.org/download.html. S23: https://www.image-net.org/download.php (+ перепечатки в поиске).
- S24: ahmadmughees/SH17dataset @2f832c2. S25: njvisionpower/Safety-Helmet-Wearing-Dataset @c952631. S26: ZijianWang-ZW/PPE_detection @907fafd. S27: ciber-lab/pictor-ppe @8f41c95. S28: wujixiu/helmet-detection @8eff5c5. S29: universe.roboflow.com/joseph-nelson/hard-hat-workers (403), public.roboflow.com/object-detection/hard-hat-workers (301), universe.roboflow.com/cs-workspace-gkdyk/hard-hat-workers-dp7ei (403).
(SHA в S02-S03 и S24-S28 — полные/сокращённые HEAD GitHub API на момент проверки; ветки изменяемые.)

## 6. Предлагаемые эксперименты (проверки документов)
- Для выбранного кандидата сверить лицензию конкретного чекпоинта (релиз/HF-карточка, sha256 из метаданных) с лицензией корня репозитория; без запуска чужого кода. Остановка: найдена явная формулировка либо зафиксировано отсутствие.
- Письменный запрос организаторам по IP и допустимым лицензиям после публикации кейса.

## 7. Передачи
- -> datasets: SH17 NC; CrowdHuman/Objects365/ImageNet NC/academic; SHWD/CHV/Pictor/GDUT без лицензии на изображения; Hard Hat Workers — читать лицензию проекта в браузере.
- -> training_strategy: избегать Objects365-инициализации при требовании чистоты; веса YOLO-NAS исключить.
- -> hackathon_strategy / operator_product: вопрос организаторам по IP, AGPL и пилоту; для жюри использовать карту §2.
- -> linq_platform: не наложены ли лицензионные условия SDK/компилятора LinQ на веса и граф (unknown).

## 8. Запросы эскалации
- Юридическая оценка AGPL-3.0 для Ultralytics-весов и ONNX-экспортов в пилоте города и цепочки COCO/Objects365/ImageNet -> веса. Материалы: F01-F03, F18, F22-F25.
