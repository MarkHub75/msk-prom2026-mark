# W1-01 FAMILIES — карта семейств и вариантов моделей для контроля СИЗ на LinQ

- ID ячейки: W1-01 (первая волна)
- Запрошено: Claude Sonnet 5.5, effort medium
- Фактическая модель (из системного окружения): **Sonnet 5.5**, model ID **claude-sonnet-5-5**
- Начало: 2026-10-23 04:43 MSK; конец: 2026-10-23 ~05:10 MSK (по системным часам окружения)
- Статус: завершено; глубина — каталогизация первичных материалов + чтение конфигов/кода в объёме, необходимом для карты (глубокий разбор кода — W1-06/07/10/15)

---

## FLASH (находки для соседей)

**FLASH-1 (→ linq_platform, все ячейки model_stack). Публичное руководство ХайТэк «Фреймворк IVA H1».**
`https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf` (27 стр.; Last-Modified 2025-11-25 08:34:47 GMT; 751083 байт; sha256 локально `ebe0ab67db2c65bbd10496553edc3a1d0b14c2e222dca0b8ff9869f452bb102a`; шифр RU.РМДВ.04.06.014-03 34 01; год на титуле 2025). Тип: primary_documentation. Текст выписан в `W1-01_files\Framework_manual_H1_pypdf_text.txt`. Из него следует цепочка (документация, не проверено запуском): **ONNX → `onnx_to_tf(onnx_model)` (конвертер в TensorFlow Graph + словарь переименований слоёв) → `dnn_quant.QuantizedModel.quantize(original_graph_def, input_shapes, output_nodes, calibration_dict, percentile=100.0, batch_axis=0, explicit_batch_value=None)` → `*.qm` → `compiler.compile_(hardware_parameters, network, parameters, slicing_scheme=None)` (`get_hw_params('128x128_asic')`, пресеты DEFAULT/STAGING) → `program.tpu` → `tpu.Device.open / load / inference().sync()`**. Калибровочный тензор — NHWC, рекомендовано ~100 образцов, предобработанных как при обучении. Среда в руководстве: Linux Ubuntu 20.04, Python 3.11, пакет `tpu_framework-py3-none-any.whl`. **Список поддерживаемых операторов в руководстве не приведён.**

**FLASH-2 (→ linq_platform, hackathon_strategy). Список «протестированных» сетей в руководстве уже, чем на сайте.** Руководство §3.4: FCN_8s, lenet5, vgg19, inception_v1, inception_v2, resnet50, mobilenet_v1, mobilenet_v2, tiny_yolo2, yolo2, tiny_yolo3, yolo3, resnet50_v2, seresnet50, flownet, REGNET_Y_800MF, anti_spoof_mn, **yolo5s**. **yolo8 и yolo11 в документе (2025) отсутствуют**; они есть только в маркетинговом списке lin-q.ru/tech. Для YOLO первичное документальное подтверждение имеют только tiny_yolo2/3, yolo2/3 и yolo5s. Это сдвигает приоритет с «yolo11/yolo8 по умолчанию» на «yolo5s и пути, проверяемые через конвертер».

**FLASH-3 (→ linq_platform, evaluation). Стороннее независимое использование того же стека.** GitHub `sherstpasha/linq-cv-bench` (commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, последний коммит 2026-04-03; автор — физическое лицо, не вендор; лицензии нет). Содержит скрипты: ResNet-50 и FCN-ResNet50 (свой build через `tpu_framework`), детекция `tiny_yolo3` по **готовой вендорской программе** `tiny_yolo3_b8_o5_128x128_asic.tpu` и **попытка собственного пути для YOLOv8s** (`export_yolov8s_to_onnx.py`: Ultralytics `model.export(format="onnx", imgsz=640, opset=13, batch=1, nms=False)`; `build_yolov8_program.py`: `onnx_to_tf` → `RegularModel(...)` → `calibrate` → `quantize` → `Network.from_quantized_model` → `compile_` с пресетами O1/O5/DEFAULT, батчи 1 и 8). **Но** в `RUN_SCENARIO.txt` (2026-03-25) «Final TPU plan» для детекции — только вендорский tiny_yolo3; YOLOv8s в финальном плане и списке результатов нет, файлов результатов в репозитории нет. Вывод (inference): скрипт YOLOv8s показывает, что путь пытались пройти; успех не подтверждён. Контракт вендорской программы tiny_yolo3 (по README стороннего автора, author_statement стороннего лица): вход `input_1:0`, форма `(8, 416, 416, 3)`, NHWC, float32 в диапазоне 0..1. Названия аппаратов в сценарии: HP1M и HPD1M; платформа `128x128_asic`.

**FLASH-4 (→ все). Пакет `pytpu` на PyPI:** `pytpu 15.0.24` (sdist, upload 2023-11-27, sha256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`; в метаданных home_page `http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk`, автор IVA-Tech). Это runtime-API устройства (в описании `TPUDevice/TPUProgram/TPUInference`), в руководстве 2025 импортируется как `tpu`/`pytpu`. Не клонировалось, код не читался.

**FLASH-5 (→ всё, training_strategy). Ultralytics уже выпустил YOLO26** (январь 2026; arXiv 2606.03748; на 2026-10-23 репозиторий ultralytics в версии 8.4.184, SHA main `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`). Отличия: `end2end: True`, `reg_max: 1` (DFL нет), опциональная NMS-free голова с TopK внутри графа; но в backbone остаётся C2PSA (self-attention блок) как в YOLO11. Документация Ultralytics также указывает, что YOLO27 «coming soon» (весов нет). Для нашей цепочки это означает: «новее» не равно «проще для LinQ» — attention-блок и TopK в голове являются неопределёнными операциями для конвертера LinQ.

---

## Резюме для оркестратора

1. Реалистичное пространство решений для LinQ определяется не «самой сильной моделью», а тем, что проходит ONNX → `onnx_to_tf` → `quantize` → `compile_`. Единственный известный нам первичный перечень совместимости — список «протестированных» сетей в руководстве IVA H1 (FLASH-2) и маркетинговый список сайта.
2. Из детекторов с первичным документальным подтверждением (руководство + сайт): **yolo5s**, yolo3/tiny_yolo3, yolo2/tiny_yolo2; только по сайту: **yolo8, yolo11, yolo4, ssd_mobilenet_v1/v2, scrfd 2.5g**. Это определяет 1-й эшелон.
3. Рекомендуемые 3–6 цепочек для первой проверки (подробно в разделе «Цепочки»): (A) **YOLOv5s** anchor-based (ultralytics/yolov5@v7.0 либо cfg `yolov5s.yaml`) — главный консервативный кандидат; (B) **YOLOv8n/s** (Ultralytics, C2f, без attention, есть DFL) — по сайту, есть сторонний скрипт сборки; (C) **YOLO11n/s** — по сайту, но C2PSA (attention) — риск; (D) **YOLOX-s/Tiny** (Apache-2.0, лицензионно чище, MIT-подобная экосистема) — кандидат вне списка LinQ, нужен как лицензионно чистая и anchor-free альтернатива; (E) **каскад person-детектор + классификатор вырезки** на сетях из списка LinQ (MobileNetV2/EfficientNet-B0/ResNet34/50) — самый низкий риск по операторам, т.к. это классические CNN-классификаторы, которые вендор явно тестировал (resnet50 — основной пример в руководстве); (F) **YOLO26n/s** как «исследовательская» ветка с экспортом one2many-головы и NMS на хосте (гипотеза), только после того как B/C докажут работоспособность конвертера.
4. Transformer-детекторы (RT-DETR, D-FINE, DEIM(v2), RF-DETR) отнесены ко второму эшелону/исключены для целевой модели: нет указаний в списках LinQ; сайт противоречиво говорит «CNN/RNN» (tech) и «CNN/Transformer» (sol); руководство тестирует только CNN. Использовать допустимо как teacher/разметка на GPU.
5. Open-vocabulary (YOLO-World, YOLOE/YOLOE-26, Grounding DINO, SAM 3) — инструменты авторазметки и teacher на нашей GPU, не целевая модель LinQ.
6. Pose и трекер — вспомогательные: трекер (ByteTrack/BoT-SORT/OC-SORT, все MIT) работает на CPU хоста и не требует LinQ; pose (RTMPose Apache-2.0 либо Ultralytics-pose AGPL) — вторая модель в рантайме, нужна только для правил «руки у лица», «человек в зоне» по ногам; приоритет ниже детектора СИЗ.
7. Малые объекты (каска вдалеке, сигарета): документированы P2-голова (`yolov8-p2.yaml`, `yolo26-p2.yaml` — только YAML, весов нет), больший imgsz (YOLOv6 N6/S6 при 1280, но GPL-3.0), SAHI-тайлинг (MIT; цифры в статье получены на VisDrone/xView на FCOS/VFNet/TOOD, не на YOLO и не на СИЗ), PP-YOLOE-SOD. Стоимость — рост вычислений ×(число тайлов); LinQ-латентность для детекторов не опубликована (unknown).
8. Главные разрывы: (i) список поддерживаемых операторов LinQ; (ii) что значит `yolo8` и `yolo11` на сайте (реализация, размер, вход, голова с DFL, постобработка на хосте или на TPU); (iii) layout входа после `onnx_to_tf` (руководство — NHWC для калибровки; сторонний скрипт YOLOv8 — NCHW); (iv) лицензионные ограничения весов (→ W1-04).
9. Первым экспериментом должно быть не обучение, а «проход конвертера» для 4–5 экспортированных ONNX (yolov5s, yolov8n/s, yolo11n, yolox_s, yolo26n one2many) — но у нас нет `tpu_framework`; значит запрос в linq_platform: получить wheel/доступ к конвертеру как можно раньше (после 13:00 MSK), а до этого — заранее подготовить ONNX (opset 11–13), статические формы, калибровочные наборы.

---

## Факты

Формат: ID — утверждение. Тип основания. Источник. Применимость. Статус проверки. Оговорки.

### LinQ и окружение

- **W1-01-F01** — Руководство «Фреймворк IVA H1» описывает конвейер ONNX → TF (`onnx_to_tf`) → квантование с калибровкой (`QuantizedModel.quantize`, параметры `input_shapes, output_nodes, calibration_dict, percentile=100.0, batch_axis=0, explicit_batch_value=None`) → `*.qm` → компиляция `compile_` в программу TPU → запуск через `tpu.Device`. Тип: primary_documentation. Источник: W1-01-S01, стр. 7–11, 20–21 (по номерам страниц PDF). Применимость: документ 2025, платформа `128x128_asic`. Статус: прочитан документ (текст извлечён); запуск не выполнялся. Оговорка: в документе есть и платформа `64x64_fpga` по умолчанию в сигнатуре `as_graph` при описании «128x128_asic по умолчанию» — внутренняя неоднозначность текста.
- **W1-01-F02** — В руководстве список протестированных сетей: FCN_8s, lenet5, vgg19, inception_v1, inception_v2, resnet50, mobilenet_v1, mobilenet_v2, tiny_yolo2, yolo2, tiny_yolo3, yolo3, resnet50_v2, seresnet50, flownet, REGNET_Y_800MF, anti_spoof_mn, yolo5s. Тип: primary_documentation. S01 §3.4 (стр. 21–22). Статус: прочитан. Оговорка: «протестированных», не «поддерживаемых»; отсутствие yolo8/yolo11/ssd/scrfd в этом документе не доказывает неподдержку (документ мог устареть).
- **W1-01-F03** — Сайт LinQ перечисляет в «ПОДДЕРЖИВАЕМЫЕ СЕТИ» дополнительно yolo4, yolo8, yolo11, ssd_mobilenet_v1/v2, scrfd 2.5g, efficientnet_b0..b3, inception_v3/v4, densenet121/169, resnet34/50/152 и др. Тип: primary_documentation (маркетинг). S02. Проверено WebFetch 2026-10-23. Оговорка: нет версии/размера/входа. Страница `/docs` содержит только датасеты-описания модулей и ссылки на руководства, SDK и компилятор не описаны.
- **W1-01-F04** — Преобразование из ONNX в руководстве названо «конвертером» `onnx_to_tf`; в примере используется `torch_resnet50.onnx`, вход `input:1`, выход `logits:0`, препроцесс центр-кроп + вычитание среднего (123.68, 116.779, 103.939), калибровочный тензор NHWC. Тип: primary_documentation. S01 стр. 12–14. Статус: прочитан.
- **W1-01-F05** — В примере руководства сравниваются 4 исполнения: исходная модель (TF), квантованная модель (TF), TLM (оценка времени) и TPU; для resnet50 «TLM estimates execution time: 5627.364001024086 us». Тип: primary_documentation (пример логов). S01 стр. 24. Оговорка: батч/режим не указан; не использовать как измерение производительности.
- **W1-01-F06** — Сторонний репозиторий `sherstpasha/linq-cv-bench` содержит путь сборки YOLOv8s для IVA H1 (export Ultralytics ONNX opset 13, imgsz 640, `nms=False`; single-output ONNX с формой, определяемой как `(N,84,8400)` или транспонированной в `normalize_prediction_shape`; NMS на хосте через `ultralytics.utils.nms.non_max_suppression`), использующий API `RegularModel`, `QuantizedModel`, `Network.from_quantized_model(...).set_batch(...)`, `tpu_compiler.compiler.O1/O5`. Тип: source_code (стороннее лицо). S03, commit 3ad1b7aa…, файлы `scr/detection/export_yolov8s_to_onnx.py`, `scr/detection/build_yolov8_program.py`, `scr/detection/run_yolov8_tpu.py`. Статус: прочитан код частично (экспорт, сборка, детали вывода); не запускался. Оговорка: API отличается от руководства 2025 (`RegularModel`, пресеты O1/O5, `anchors_mapping`) — вероятно более новая версия `tpu_framework`; результаты YOLOv8 в репозитории не найдены.
- **W1-01-F07** — В `RUN_SCENARIO.txt` (дата в файле 2026-03-25) итоговый план TPU: классификация (self-build ResNet-50, пресеты O1/O5), сегментация (self-build FCN-ResNet50, O1), **детекция — вендорская программа tiny_yolo3**, сравнение — vendor resnet50_mlperf; «not finalized: segmentation TPU self-build O5». Модули: HP1M, HPD1M. Тип: artifact_metadata/author_statement стороннего лица. S03. Статус: прочитан файл; числа результатов в репозитории отсутствуют.
- **W1-01-F08** — Вендорская программа tiny_yolo3: имя `tiny_yolo3_b8_o5_128x128_asic.tpu`, вход `input_1:0`, форма `(8,416,416,3)`, NHWC, float32 0..1. Тип: author_statement (сторонний README). S03 `scr/detection/README.md`. Статус: прочитан; артефакт не получен. Оговорка: файлы `linq_files/tpu_programs/` в репозитории отсутствуют; источник программы — вендор (не уточнён).
- **W1-01-F09** — Публичных упоминаний YOLO на LinQ в новостях об Иннопроме 2026 нет: статья Hi-Tech Mail 2026-07-08 сообщает LinQ HX «до 30 трлн оп/с, до 5 нейросетей одновременно, задержка 1,5–2,3 мс, ≤40 Вт, видеонаблюдение/робототехника/медицина», но о моделях и ПО ничего. Тип: reported_measurement/author_statement (пресс-релиз Департамента инвестиционной и промышленной политики Москвы). S04. Статус: прочитано.
- **W1-01-F10** — Публичного репозитория вендора с SDK и/или примерами YOLO на LinQ в GitHub не найдено: `gh search repos "linq tpu hitech"` → пусто; `gh search code "lin-q.ru"` → пусто; пользователь `lin-Q` — пустой личный аккаунт (0 репозиториев). `pytpu` на PyPI с `home_page=http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk` (внутренний git вендора, недоступность не проверялась). Тип: local_observation. Охват: GitHub search/API, PyPI JSON, WebSearch (русские и английские запросы).

### Ultralytics

- **W1-01-F11** — Ultralytics: на 2026-10-23 latest release `v8.4.184` (2026-10-22T17:41:34Z); SHA main = `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`; лицензия репозитория AGPL-3.0. Тип: artifact_metadata (`gh api`). S05. Статус: проверена доступность.
- **W1-01-F12** — YOLO26: релиз «January 2026», arXiv 2606.03748 «Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models»; заявлены удаление DFL, NMS-free end-to-end, ProgLoss, STAL (small-target-aware label assignment), MuSGD; таблица COCO @640 (n: 40.9/40.1 e2e mAP, 2.4M, 5.5 GFLOPs; s: 48.6/47.8, 9.5M, 20.9; m: 53.1/52.5, 20.4M, 68.4); «Prediction and validation default to the one-to-many head for accuracy»; лицензия AGPL-3.0 и Enterprise. Тип: author_statement. S06 (WebFetch 2026-10-23). Статус: прочитана страница; статья не открывалась.
- **W1-01-F13** — Конфиг `ultralytics/cfg/models/26/yolo26.yaml`@e6d5fc5: `end2end: True`, `reg_max: 1`; scales n/s/m/l/x; backbone C3k2 + SPPF + **C2PSA**; summary в комментариях: n 2 572 280 параметров/6.1 GFLOPs, s 10 009 784/22.8, m 21 896 248/75.4 (fused-значения на странице документации отличаются: 2.4M/5.5 и т.д.). Тип: source_code. S05. Статус: прочитан YAML. Есть также `yolo26-p2.yaml`, `yolo26-p6.yaml`, `yolo26-pose.yaml`, `yolo26-cls.yaml`, `yoloe-26.yaml`. Оговорка: документация: «yolo26-p2.yaml and yolo26-p6.yaml … shipped as YAML architectures only. No scale-specific … weights are released».
- **W1-01-F14** — `ultralytics/nn/modules/head.py`@e6d5fc5: `class Detect` (стр. 38), `max_det = 300` (83), `_grouped_topk` (92), при `end2end` строятся `one2one_cv2/cv3` (141–143), `postprocess` с `get_topk_index` (249–282). То есть NMS-free постобработка = TopK/gather в графе. Тип: source_code. Статус: прочитан код, экспорт не выполнялся. Вывод (inference): TopK в экспортируемом графе — потенциальный блок для конвертера LinQ; обход — экспорт one2many-ветки без end2end и NMS на хосте (hypothesis, механизм переключения не проверен на этом commit).
- **W1-01-F15** — `block.py`@e6d5fc5: классы `C2f` (291), `C3k2` (1069), `Attention` (1271), `PSABlock` (1337), `C2PSA` (1442). YOLOv8 yaml использует `C2f` + `SPPF` без attention; YOLO11/26 yaml — `C3k2` + `SPPF` + `C2PSA`; YOLOv5 yaml — `C3` + `SPPF`, (anchor-based Detect в оригинальном репозитории). Тип: source_code. S05. Статус: прочитан. Вывод (inference): у YOLOv8 в backbone/neck нет attention-блоков, у YOLO11/26 есть C2PSA.
- **W1-01-F16** — Экспорт ONNX в Ultralytics@e6d5fc5: функция `export_onnx` (стр. 1125 в `engine/exporter.py`), опция `opset` (по умолчанию выбирается `best_onnx_opset(onnx)`), минимум 9 (11 при `nms`, 16 для некоторых моделей), в 8.4.x есть параметр `quantize` (ONNX int8 в Ultralytics, стр. 1128). Тип: source_code. S05. Статус: прочитан фрагмент. Оговорка: Ultralytics int8 в стороннем runtime — не путь компилятора LinQ.
- **W1-01-F17** — Официальные веса (assets release `v8.4.0`, 2026-01-13T22:56:46Z, GitHub `ultralytics/assets`): yolo26n.pt 5544453 B sha256:9b09cc8b…4fef; yolo26s.pt 20422725 B sha256:646f8bc3…a1b; yolo26m.pt 44255705 B; yolo11n.pt 5613764 B sha256:0ebbc80d…ee1; yolo11s.pt 19313732 B; yolov8n.pt 6549796 B sha256:f59b3d83…b36; yolov8s.pt 22588772 B sha256:1f47a78b…78b; yolov5nu.pt 5562759 B; yolov5su.pt 18581255 B (anchor-free «u»-версия). Тип: artifact_metadata (поле `digest` из GitHub API, не вычислено). Статус: метаданные получены, файлы не скачивались. Лицензия весов — отдельный вопрос (→ W1-04).
- **W1-01-F18** — Семейство в документации Ultralytics: YOLO27 «Coming soon … no weights or package support yet»; YOLO12 «attention-centric community release, weights detection only»; YOLO11 «mature option for stable production use»; YOLOv5 и YOLOv3 в пакете Ultralytics — «u»-версии (anchor-free головы); YOLOv7 — «prediction only from exported ONNX/TensorRT». Тип: author_statement. S07. Статус: прочитана страница `models/`.
- **W1-01-F19** — Ultralytics YOLOv5 (отдельный репозиторий `ultralytics/yolov5`): latest release v7.0 (2022-11-22), SHA ветки master на момент проверки `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce`; в README таблица ссылается на веса `yolov5nu/yolov5su` (Ultralytics-платформа) — то есть актуальный README уже подталкивает к anchor-free «u»-вариантам; оригинальные anchor-based веса v7.0 остаются в release: yolov5n.pt 4062133 B, yolov5s.pt 14808437 B, yolov5m.pt 42806829 B; `models/yolov5s.yaml` содержит `depth_multiple: 0.33`, `width_multiple: 0.50`, `anchors:`. Параметры/FLOPs YOLOv5s 7.2M/16.5 GFLOPs, COCO mAP 37.4 (таблица README для 640). Тип: artifact_metadata + author_statement. S08. Статус: проверены метаданные; файлы не скачивались. Вывод (inference): вендорское «yolo5s» в руководстве, вероятнее всего, оригинальный anchor-based YOLOv5s (hypothesis; нужно уточнить у вендора, какой репозиторий/версия и какой вход).

### Другие детекторы (первичные таблицы)

- **W1-01-F20** — YOLOX (Megvii; Apache-2.0; arXiv 2107.08430; релиз 0.3.0 2022-04-22; SHA main `6ddff4824372906469a7fae2dc3206c7aa4bbaee`). README: YOLOX-s 640 → 40.5 mAP, 9.0M параметров, 26.8 GFLOPs; YOLOX-m 46.9/25.3M/73.8; YOLOX-Nano 416 → 25.8 mAP, 0.91M, 1.08 GFLOPs; YOLOX-Tiny 416 → 32.8, 5.06M, 6.45; конфиги `exps/default/yolox_s.py`, `yolox_nano.py`, `yolox_tiny.py`; веса в Releases (0.1.1rc0). Тип: author_statement. S09. Статус: прочитан README.
- **W1-01-F21** — YOLOv6 (Meituan; GPL-3.0; arXiv 2209.02976, 2301.05586; SHA `e86a483f3f6bded25d45970b56831345a99744a4`; последняя активность 2024-08). v4.0: YOLOv6-N 640 → 37.5 mAP, 4.7M, 11.4 GFLOPs; S 45.0/18.5M/45.3; M 50.0/34.9M/85.8; N6 (1280) 44.9/10.4M/49.8; S6 50.3/41.4M/198.0. В README также приведены INT8 RepOpt-варианты (PTQ с RepOpt: YOLOv6-N RepOpt INT8 34.8 mAP; S RepOpt 43.3) и Lite-модели для CPU/mobile. Тип: author_statement. S10.
- **W1-01-F22** — YOLOv7 (WongKinYiu/yolov7; GPL-3.0; arXiv 2207.02696; релиз v0.1 2022-07-07) и YOLOv9 (WongKinYiu/yolov9; GPL-3.0; arXiv 2402.13616; v0.1 2024-02-21): YOLOv9-T 640 → 38.3 mAP, 2.0M, 7.7 GFLOPs; S 46.8/7.1M/26.4; M 51.4/20.0M/76.3. Тип: author_statement. S11. Отдельный репозиторий `WongKinYiu/YOLO` (**MIT**, релиз v1.0 2025-12-30, SHA `c4cb5f6f56102eceeaa7d75e23e1125cd0373eaf`) — реимплементация YOLOv9/YOLOv7/YOLO-RD с MIT-лицензией кода; лицензия весов не проверялась (→ W1-04).
- **W1-01-F23** — YOLOv10 (THU-MIG; AGPL-3.0; arXiv 2405.14458; релиз v1.1 2024-05-26): N 640 → 38.5 mAP, 2.3M, 6.7 GFLOPs; S 46.3/7.2M/21.6; M 51.1/15.4M/59.1 (NMS-free через one-to-one head). Тип: author_statement. S12.
- **W1-01-F24** — YOLOv12 (sunsmarterjie; AGPL-3.0; arXiv 2502.12524; SHA `2abab7153a065fb2925e8088e9ca2b19016ab7d6`): n 640 → 40.4–40.6 mAP, 2.5–2.6M, 6.0–6.5 GFLOPs; s 47.6–48.0; «attention-centric». YOLOv13 (iMoonLab; AGPL-3.0; последняя активность 2025-11). Тип: author_statement. S13. Вывод (inference): архитектуры с attention ради небольшого прироста на COCO не соответствуют цели «меньше рисков для конвертера»; в Ultralytics YOLO12 документирован как community release.
- **W1-01-F25** — PP-YOLOE+ (PaddleDetection; Apache-2.0; arXiv 2203.16250; релиз v2.9.0 2026-03-19): PP-YOLOE+_s 640 → 43.7 mAP, 7.93M, 17.36 GFLOPs; PP-YOLOE+_m 49.8/23.43M/49.91; PP-YOLOE+_t-aux 39.9/4.85M/19.15; **вариант `ppyoloe_plus_crn_t_auxhead_relu_300e_coco.yml` (ReLU)** 36.4 mAP/3.60M/12.17 GFLOPs. В `configs/pphuman/` есть `ppyoloe_crn_s_36e_crowdhuman.yml`, `ppyoloe_crn_l_36e_crowdhuman.yml`, `ppyoloe_crn_s_80e_smoking_visdrone.yml` (детектор курения), `ppyoloe_plus_crn_t_auxhead_320_60e_pphuman.yml`. Тип: author_statement/source_code (список конфигов). S14. Статус: прочитаны таблица и список файлов. Оговорка: Paddle→ONNX через Paddle2ONNX (README PicoDet: opset 11, onnxsim), NMS в ONNX рекомендовано не включать.
- **W1-01-F26** — PicoDet (PaddleDetection; arXiv 2111.00902): PicoDet-S 416 → 32.5 mAP, 1.18M, 1.65 GFLOPs; PicoDet-M 416 → 37.5, 3.46M, 4.34; PicoDet-L 640 → 42.6, 5.80M, 16.81; QAT-пример для PicoDet-S 416: 31.5 mAP; есть конфиг `picodet_s_416_coco_npu.yml`. Тип: author_statement. S14 (WebFetch README_en release/2.8).
- **W1-01-F27** — NanoDet-Plus (RangiLyu; Apache-2.0; последний release v1.0.0 2023-03-21; последняя активность 2024-08): m 416 → 30.4 mAP, 1.17M, 1.52 GFLOPs; m-1.5x 416 → 34.1, 2.44M, 2.97. Тип: author_statement. S15. Вывод: слабая точность; малый размер; ShuffleNetV2 backbone (depthwise) — неблагоприятно для малых объектов.
- **W1-01-F28** — SSD-MobileNet (TF1 Detection Zoo): ssd_mobilenet_v1_coco 21 mAP, ssd_mobilenet_v2_coco 22, ssdlite_mobilenet_v2_coco 22; скорость на TITAN X @600×600; каждая загрузка содержит `frozen_inference_graph.pb`; страница предупреждает о фильтрации детекций ниже порога (~0.3) в замороженном графе. Лицензия на странице не указана. Тип: author_statement. S16. Вывод (inference): имена `ssd_mobilenet_v1/v2` на сайте LinQ совпадают с TF1-zoo (hypothesis, совпадение имён не доказывает использование).
- **W1-01-F29** — Совпадение имён: имена из списка LinQ `inception_v1..v4`, `mobilenet_v1`, `mobilenet_v2`, `nasnet_mobile`, `pnasnet_large`, `pnasnet_mobile`, `resnet50_v2`, `vgg19` (в нотации TF-Slim: «Inception V1–V4», «MobileNet_v1_1.0_224», «NASNet-A_Mobile_224», «PNASNet-5_Large_331», «PNASNet-5_Mobile_224», «ResNet V2 50», «VGG 19») соответствуют TF-Slim pretrained models; `torch_*` — torchvision-варианты; `tiny_yolo3/yolo3` — Darknet/Keras (сторонний репозиторий использует pjreddie cfg/weights + qqwweee/keras-yolo3 как reference); `scrfd 2.5g` — InsightFace. Тип: inference (по совпадению имён). S16, S03, S17. Гипотеза, не подтверждена вендором.
- **W1-01-F30** — SCRFD (InsightFace; arXiv 2105.04714; ICLR 2022; SHA ветки master `c6c3af7bd2d0a0bf4b78c78437357f3521aa5d52`): SCRFD_2.5G WIDERFACE Easy/Medium/Hard 93.78/92.16/77.87, 0.67M параметров, 2.5 GFLOPs; есть вариант с ключевыми точками `SCRFD_2.5G_KPS`. Задача — лица. Тип: author_statement. S17. Вывод: каски/респираторы/сигареты не детектирует; лицензия весов не установлена (в репозитории не обнаружен SPDX; → W1-04).
- **W1-01-F31** — RT-DETR (lyuwenyu; Apache-2.0; arXiv 2304.08069): RT-DETR-R18 640 → 46.5 mAP (49.2 с Objects365), 20M, 60 GFLOPs. D-FINE (Peterande; Apache-2.0; arXiv 2410.13842): D-FINE-N 42.8 mAP, 4M, 7 GFLOPs; S 48.5, 10M, 25. DEIM (Intellindust-AI-Lab; arXiv 2412.04234; лицензия NOASSERTION): N 42.8–43.0. DEIMv2 (arXiv 2509.20787; обновлён 2026-10-22; лицензия NOASSERTION): Atto 23.8 mAP/0.5M, Femto 31.0/1.0M, Pico 38.5/1.5M. RF-DETR (Roboflow; Apache-2.0 для N/S/M, часть крупных — PML 1.0; arXiv 2511.09554; релиз 1.11.2 2026-10-04): Nano 384×384 → 48.4 mAP, 30.5M параметров; Small 512 → 53.0; Medium 576 → 54.7. Тип: author_statement. S18. Вывод (inference): все содержат attention/deformable attention или DINOv2-backbone — оператор-риск для int8-компилятора со сверточной ориентацией; в списках LinQ отсутствуют.
- **W1-01-F32** — Open-vocabulary и teacher: YOLOE-26 (`yoloe-26.yaml` в Ultralytics@e6d5fc5; YOLOE arXiv 2503.07465), YOLO-World (AILab-CVC; GPL-3.0; arXiv 2401.17270; не обновлялся с 2025-02), GroundingDINO (IDEA-Research; Apache-2.0; arXiv 2303.05499; не обновлялся с 2024-08), SAM 3 (в списке документации Ultralytics как NEW; часть чекпойнтов требует approval на Hugging Face). Тип: author_statement/source_code (списки). S07, S19. Статус: проверена только активность и лицензия репозиториев.
- **W1-01-F33** — Pose/трекинг: MMPose (Apache-2.0; релиз v1.3.2 2024-07-12) содержит RTMPose, RTMO, RTMW; Ultralytics имеет `yolo26-pose.yaml`/`yolo11-pose.yaml`/`yolov8-pose.yaml`; трекеры: ByteTrack (MIT, arXiv 2110.06864, последняя активность 2024-06), BoT-SORT (MIT, 2024-08), OC-SORT (MIT, 2026-04); PaddleDetection `configs/mot` содержит bytetrack, botsort, ocsort, deepsort. Тип: artifact_metadata/source_code. S19, S14. Статус: проверены метаданные репозиториев.
- **W1-01-F34** — Малые объекты: (a) P2-головы: `yolov8-p2.yaml`, `yolov8-p6.yaml`, `yolov8-ghost-p2.yaml` (@e6d5fc5), `yolo26-p2.yaml` (только YAML, без весов); (b) STAL в YOLO26 (author_statement); (c) SAHI (obss; MIT; arXiv 2202.06934; версия 0.12.8 от 2026-09-30?): в статье AP +6.8/5.1/5.3% (FCOS/VFNet/TOOD) без fine-tuning и +12.7/13.4/14.5% с slicing-aided fine-tuning на VisDrone/xView; (d) YOLOv6 N6/S6 @1280 (F21); (e) PP-YOLOE-SOD (VisDrone, 38.5 mAP по README PaddleDetection). Тип: author_statement. S05, S20, S14. Оговорка: ни одна из цифр не относится к каскам/сигаретам на производственном видео; SAHI тестировался не на YOLO.

---

## Классы решений (по пункту 1 задания)

Число моделей в рантайме — число одновременно загруженных на LinQ программ. Известно (author_statement, S08/новость): «поддержка инференса нескольких моделей», «до пяти нейросетей одновременно» (маркетинг LinQ HX).

| Класс | Зачем | Когда работает | Когда нет | Моделей в рантайме |
|---|---|---|---|---|
| **K1. Единый мультиклассовый детектор** (person + helmet/head/vest/mask/…) | Одна программа, минимум латентности, проще интеграция | Крупные/средние объекты, много обучающих данных с нужными классами | Каска на дальнем плане: класс «голова без каски» часто мелкий; сигарета — почти недетектируема на 640 px при общем плане; нужна одна таксономия классов в датасете | 1 |
| **K2. Каскад person → crop → классификатор/детектор СИЗ** | Повышает разрешение на мелкую деталь, позволяет использовать малые классификаторы из списка LinQ | Когда человек достаточно крупный (или камера PTZ/высокого разрешения); когда нужна «объясняемость» нарушения человеку | Много людей в кадре → N кропов на кадр (стоимость пропорциональна числу людей, batch-программы нужны); ошибки person-детектора каскадируются | 2 (person-детектор + классификатор), опционально 3 |
| **K3. Pose/keypoints как вспомогательный модуль** | Привязка «голова/руки у лица» для каски/респиратора/курения; «ноги в зоне» | Когда нужны правила, зависящие от частей тела; вспомогательный источник ROI головы для K2 | Дополнительная модель, плохая видимость рук, ложные срабатывания «рука у лица»; для LinQ pose-голова (heatmap/DFL/декодирование) без подтверждённой поддержки операторов | +1 |
| **K4. Трекер + временные правила** | Сглаживает мерцание, считает длительность нарушения, снимает дубли | Всегда нужен поверх покадрового детектора | Нет (на CPU хоста) | 0 на LinQ (CPU) |
| **K5. Open-vocabulary/VLM (YOLO-World, YOLOE, GroundingDINO, SAM 3)** | Авторазметка, teacher, поиск трудных примеров | На нашей GPU до и во время хакатона | Как целевая модель LinQ — оснований нет (attention/text encoder, список LinQ) | 0 на LinQ |

Выводы (inference): базовая гипотеза решения — K1 для первого рабочего контура (минимум интеграции), K2 как усиление для малых объектов, K4 обязателен, K3 только при остатке времени, K5 только для разметки.

---

## Сопоставление списка LinQ с реализациями (пункт 3 задания)

Все строки в колонке «вероятное значение» — inference/hypothesis; подтверждение — только вендор или проход конвертера.

| Имя на lin-q.ru | В руководстве 2025? | Вероятная реализация | Размер/вход | Что не установлено |
|---|---|---|---|---|
| yolo5s | да | Ultralytics YOLOv5s (оригинал, anchor-based, v6/v7 `yolov5s.yaml`: Conv 6×6 s2, C3, SPPF) | 7.2M / 16.5 GFLOPs @640 (S08) — если это оно; вход (640? 416? 320?) не известен | какой репозиторий/версия; размер входа; голова на TPU или на хосте |
| yolo8 | нет | Ultralytics YOLOv8 (size? s — вероятно из-за стороннего скрипта YOLOv8s) | n/s/m/l/x: 3.2M/8.9G … 68.2M/258.5G (S05 yaml) | размер; opset; DFL/Softmax; пост-обработка |
| yolo11 | нет | Ultralytics YOLO11 (C3k2+C2PSA) | n..x: 2.6M/6.6G … 57.0M/196.0G | размер; поддержка C2PSA |
| yolo2/tiny_yolo2, yolo3/tiny_yolo3, yolo4 | yolo2, tiny_yolo2, yolo3, tiny_yolo3: да; yolo4: нет | Darknet-цепочка (pjreddie/AlexeyAB) через Keras/TF; сторонний репозиторий: tiny_yolo3 = pjreddie `yolov3-tiny.cfg/.weights`, вход 416, 8 батч | tiny_yolo3: вход 416×416 (F08) | yolo4: вход/активации (Mish→?) |
| ssd_mobilenet_v1/v2 | нет | TF1 Detection Zoo (`frozen_inference_graph.pb`) | 300×300 в оригинале SSD-MobileNet (число из памяти, не проверено в этом запуске) | вход; что с NMS-постобработкой в графе |
| scrfd 2.5g | нет | InsightFace SCRFD_2.5G | 2.5 GFLOPs @640 (по README) | лица, не СИЗ |
| mobilenet_v1/v2, torch_mobilenet_v2, efficientnet_b0..b3, resnet34/50/152, torch_resnet50, densenet121/169, inception_v1..v4, vgg19, xception, nasnet/pnasnet, lenet5 | частично (mobilenet_v1/v2, resnet50, resnet50_v2, vgg19, inception_v1/v2, lenet5) | классификаторы TF-Slim/Keras/torchvision | 224 (типично); не подтверждено | SE-блоки (seresnet50 в руководстве — значит SE работает), Swish (efficientnet) |

Первичная подсказка по контракту: пример руководства — `torch_resnet50.onnx`, вход NHWC после конвертации (калибровка NHWC), вычитание ImageNet-средних без деления (в примере), то есть preprocess входит в ответственность пользователя.

---

## Кандидаты: 6–10 наиболее перспективных вариантов (первичная карточка)

Лицензии — кратко (детали → W1-04). Параметры/FLOPs — по первичной таблице автора/документации (reported_measurement автора, условия — COCO val, входной размер указан).

| # | Вариант | Первичная публикация | Канонический код (commit) | Конфиги | Веса | Параметры/FLOPs, mAP COCO | Лицензия кода |
|---|---|---|---|---|---|---|---|
| 1 | **YOLOv5s** anchor-based | нет статьи (Jocher, Ultralytics); документация | github.com/ultralytics/yolov5 @ `af08ba156fd5…` (master), tag v7.0 | `models/yolov5s.yaml` | releases v7.0: `yolov5s.pt` 14 808 437 B | 7.2M / 16.5G, 37.4 @640 | AGPL-3.0 |
| 2 | **YOLOv8n/s** | нет статьи | ultralytics/ultralytics @ `e6d5fc59…` (8.4.184) | `cfg/models/v8/yolov8.yaml` (+ `yolov8-p2.yaml`) | assets v8.4.0: `yolov8n.pt` 6 549 796 B, `yolov8s.pt` 22 588 772 B | n 3.16M/8.9G, s 11.17M/28.8G (yaml summary); mAP на странице не снимался | AGPL-3.0 |
| 3 | **YOLO11n/s** | нет статьи | то же | `cfg/models/11/yolo11.yaml` | `yolo11n.pt` 5 613 764 B, `yolo11s.pt` 19 313 732 B | n 2.62M/6.6G, s 9.46M/21.7G | AGPL-3.0 |
| 4 | **YOLO26n/s** | arXiv 2606.03748 | то же | `cfg/models/26/yolo26.yaml`, `yolo26-p2.yaml` | `yolo26n.pt` 5 544 453 B, `yolo26s.pt` 20 422 725 B | n 2.4M/5.5G, 40.9 (e2e 40.1); s 9.5M/20.9G, 48.6 (e2e 47.8) | AGPL-3.0 |
| 5 | **YOLOX-s / Tiny / Nano** | arXiv 2107.08430 | Megvii-BaseDetection/YOLOX @ `6ddff4824372…` | `exps/default/yolox_s.py`, `yolox_tiny.py`, `yolox_nano.py` | releases 0.1.1rc0 | s 9.0M/26.8G, 40.5 @640; Tiny 5.06M/6.45G, 32.8 @416; Nano 0.91M/1.08G, 25.8 @416 | Apache-2.0 |
| 6 | **PP-YOLOE+ / PicoDet (ReLU-вариант t-aux-relu)** | arXiv 2203.16250 / 2111.00902 | PaddlePaddle/PaddleDetection (release/2.9 @ `b25522a0f4bd…`) | `configs/ppyoloe/…`, `configs/picodet/…` | Paddle (bcebos) | PP-YOLOE+_s 7.93M/17.36G, 43.7; t-aux-relu 3.60M/12.17G, 36.4; PicoDet-S 416 1.18M/1.65G, 32.5 | Apache-2.0 |
| 7 | **tiny_yolo3 / yolo3 (Darknet/Keras)** | arXiv 1804.02767 (из памяти; не проверялось) | pjreddie/darknet, qqwweee/keras-yolo3 (MIT) | cfg `yolov3-tiny.cfg` | `yolov3-tiny.weights` | (не снималось) | MIT (keras-yolo3, S03); darknet — не проверялась |
| 8 | **SSD-MobileNetV2 / SSDLite** | arXiv (из памяти не приводим) | tensorflow/models (TF1 zoo) | zoo config | frozen graphs | 22 mAP COCO (S16) | Apache-2.0 (лицензия репозитория `NOASSERTION` по API; детально → W1-04) |
| 9 | **YOLOv6 3.0 (n/s)** | arXiv 2301.05586 | meituan/YOLOv6 @ `e86a483f3f6b…` | `configs/yolov6n.py`/`yolov6s.py` (из README) | releases 0.4.0 | N 4.7M/11.4G, 37.5; S 18.5M/45.3G, 45.0 | GPL-3.0 |
| 10 | **Классификаторы вырезок: MobileNetV2, EfficientNet-B0, ResNet34/50** | MobileNetV2 arXiv 1801.04381 (из памяти) | torchvision / TF-Slim | — | — | — | BSD/Apache (не проверялось) |

Не включены в 6–10, но учтены: YOLOv7/9 (GPL; MIT-реимплементация `WongKinYiu/YOLO`), YOLOv10 (AGPL, NMS-free), NanoDet-Plus (слабая точность), RTMDet (MMDetection, Apache-2.0, `configs/rtmdet/` есть tiny/s/m; не снимался подробно).

---

## Цепочки для первой проверки (рекомендация, ранжирование — inference)

**Цепочка A — YOLOv5s anchor-based (главный консервативный кандидат).**
Основания: только yolo5s из семейства YOLO v5+ имеет подтверждение в руководстве 2025 (F02) и на сайте (F03); архитектура без attention и без DFL (F15); экспорт ONNX известен; лицензия кода AGPL (→ W1-04). Риски: AGPL; mAP ниже новых; anchor-based декодирование (Sigmoid, Mul, Concat, Reshape, Transpose, Gather/Slice в экспортируемом ONNX — перечень из знаний об экспорте, **не** проверялся в этом запуске); какой именно вариант «yolo5s» принят вендором — unknown. Что глубоко разбирать: ONNX-граф `yolov5s.pt` (opset 11–13; без декодирования/с декодированием) и операторы → W1-06.

**Цепочка B — YOLOv8n/s.** Основания: сайт (F03), нет attention, широко документирован экспорт; сторонний скрипт сборки существует (F06) — значит путь `onnx_to_tf` для этой архитектуры пытались пройти. Риски: DFL (Softmax/ReduceSum/Conv по 16 бинам и `Transpose`), `Resize` nearest, SiLU (Sigmoid+Mul); квантование DFL-ветки в int8 (hypothesis) — деградация boxes; успех/неуспех пути не известен (F07: в итоговый план не вошёл). Глубоко разбирать: C2f/Detect при экспорте (→ W1-06/07).

**Цепочка C — YOLO11n/s.** Основания: сайт (F03); большие модели не нужны, `n/s` дешёвые. Риски: C2PSA (Attention: матричное умножение, Softmax, reshape) — неопределённость конвертера (F15); при провале — замена C2PSA на identity/простой блок и переобучение (hypothesis, ухудшает перенос предобученных весов). Глубоко разбирать — только после результата B.

**Цепочка D — YOLOX-s/Tiny.** Основания: Apache-2.0 (чище AGPL), anchor-free, документированный ONNX-экспорт в репозитории (`tools/export_onnx.py` — имя из знаний, **не** проверялось в этом запуске), понятные конфиги `exps/default`. Риски: Focus-stem (slice+concat), decoupled head, SiLU; нет следа на сайте LinQ; последний релиз 2022. Нужна ради лицензионно-чистого пути и сравнения. Разбор → W1-04/06.

**Цепочка E — каскад: детектор person (любой из A–D) + классификатор вырезки из списка LinQ (MobileNetV2/EfficientNet-B0/ResNet34/50).** Основания: классификаторы — самая подтверждённая часть списка (resnet50 — центральный пример руководства; mobilenet_v1/v2 в списке тестированных; `torch_mobilenet_v2`, `torch_resnet50` на сайте). Подходит для задач «каска/без каски», «респиратор/нет» на вырезках головы/лица. Риски: два уровня ошибки; нужно разметить кропы; batch-программы (вендорский tiny_yolo3 имеет `b8`, F08; `Network.set_batch` — F06) для N людей на кадр.

**Цепочка F — YOLO26n/s с one2many-головой и NMS на хосте (исследовательская).** Основания: актуальный релиз, STAL для малых объектов (author_statement), нет DFL (`reg_max: 1`), свежие инструменты экспорта. Риски: C2PSA, TopK при end2end (F14), неизвестный механизм отключения end2end в экспорте на данном commit; AGPL. Пробовать после B/C.

Исключено/второй эшелон — см. «Причины исключения».

---

## Малые объекты и высокое разрешение (пункт 5)

- Больший imgsz для одного детектора: YOLOv6 N6/S6 @1280 дают 44.9/50.3 mAP (F21) против 37.5/45.0 при 640 — это цифры на COCO, не на малых СИЗ; цена — ×~4 FLOPs (N6 49.8G против 11.4G).
- P2-голова: готовые YAML `yolov8-p2.yaml` (весов предобучения нет в том же имени — предобучение нужно переносить из `yolov8*.pt` по слоям, что Ultralytics делает автоматически при совпадении слоёв; **не проверено**), `yolo26-p2.yaml` — только YAML.
- SAHI-тайлинг: MIT, активный (0.12.8, 2026-09-30); цифры статьи (F34) — не на YOLO/СИЗ. Для LinQ каждая плитка — отдельный инференс; тайлинг эффективнее по пропускной способности только при batch-программах.
- Двухступенчатый путь K2 (кроп головы по person bbox) — это тот же приём, что и тайлинг, но адресный; для сигареты дополнительно нужен кроп области лица/рук (K3) — документированных готовых моделей «cigarette detector» нет в этой карте; PaddleDetection имеет `ppyoloe_crn_s_80e_smoking_visdrone.yml` (конфиг, веса и датасет не снимались; → W1-05/16).
- Сигарета: при общем плане на 640 px объект порядка единиц пикселей; без кропа/высокого разрешения ожидание низкого recall (inference).

---

## Причины исключения слабых веток (кратко)

- RT-DETR/D-FINE/DEIM/DEIMv2/RF-DETR: attention/deformable attention/DINOv2; нет в списках LinQ; сайт противоречив («CNN и RNN» в tech vs «CNN/Transformer» в sol); у DEIM(v2) лицензия не указана (NOASSERTION). Оставлены как teacher на GPU.
- YOLOv7/v9 и YOLOv6: GPL-3.0; для v9 — GPELAN/RepNCSPELAN, сложнее нейтрального набора операторов; MIT-реимплементация `WongKinYiu/YOLO` содержит v7/v9 — единственный известный лицензионно чистый YOLO-подобный кандидат, но без следов LinQ.
- YOLOv10/12/13: NMS-free (v10) или attention (v12/13), AGPL; нет оснований в списках LinQ.
- SCRFD: лица; для СИЗ не подходит; допустим только как источник ROI лица (hypothesis).
- NanoDet-Plus: низкая точность (30–34 mAP @416), depthwise ShuffleNet; репозиторий давно не обновлялся.
- SSD-MobileNet: 21–22 mAP COCO; устаревшая точность; допустим только как fallback «детектор человека» с вендорским следом (сайт).
- YOLO-World/YOLOE/GroundingDINO/SAM 3: не для LinQ.

---

## Противоречия

1. **Сайт vs руководство по YOLO:** сайт — yolo8/yolo11; руководство 2025 — только yolo5s среди v5+. Возможное объяснение: руководство старее сайта (Last-Modified PDF 2025-11-25; дата сайта на 2026-10-23). Разрешение: запрос к вендору/организаторам, проход конвертера.
2. **Типы сетей:** tech — «CNN и RNN»; sol — «CNN/Transformer». Влияет на допустимость C2PSA/attention и всего transformer-семейства. Разрешение: linq_platform (список операторов).
3. **Layout входа:** руководство — калибровочный тензор NHWC, вендорская программа tiny_yolo3 — NHWC; сторонний скрипт YOLOv8 задаёт `input_shapes = (1,3,640,640)` и `input_layout: nchw` в build summary после `onnx_to_tf` с тем же графом. Не установлено, что делает конвертер с layout ONNX NCHW. Разрешение: запуск конвертера.
4. **API:** руководство — `QuantizedModel.quantize`, пресеты DEFAULT/STAGING; сторонний код — `RegularModel`, `calibrate`, `quantize`, `compile_` с `O1/O5`, `anchors_mapping`. Версии фреймворка различаются; нужно выяснить версию, доступную на хакатоне.
5. **«yolo5s»** в README Ultralytics теперь ведёт на `yolov5su` (anchor-free), а оригинал — anchor-based. Какой из них имеет в виду LinQ — unknown.

---

## Открытые вопросы (с указанием, где искали и чем закрыть)

1. Какие ONNX-операторы поддерживает `onnx_to_tf`/квантизатор/компилятор (Resize, Concat, Split, Sigmoid, Softmax, Slice, TopK, MatMul, LayerNorm, GELU, Mish)? Искали: руководство (нет), сайт (нет). Закрыть: SDK/конвертер/вендор → linq_platform.
2. Что за «yolo8» и «yolo11» на сайте (размер, вход, голова, постобработка)? Искали: сайт, руководство, GitHub (только сторонний скрипт). Закрыть: вендор или готовые вендорские `.tpu`-программы, если выдадут.
3. Есть ли готовые вендорские `.tpu` программы (как tiny_yolo3_b8_o5) для yolov5s/yolov8? Искали: репозиторий стороннего автора (программы не опубликованы). Закрыть: организаторы.
4. Работает ли путь YOLOv8s у стороннего автора, какие метрики? Искали: репозиторий (результатов нет). Закрыть: автор/эксперимент.
5. Поддерживается ли квантование per-channel, смешанная точность, QAT? Искали: руководство (описан percentile и калибровка; QAT не упомянут). Закрыть: SDK.
6. Какие размеры входа/батча применимы для детектора (`explicit_batch_value`, `set_batch`)? Закрыть: SDK/эксперимент.
7. Где проходит граница «на TPU» и «на хосте» для декодирования боксов и NMS? Закрыть: SDK; ориентир — сторонний код: NMS на хосте.
8. Лицензии весов (AGPL-код Ultralytics; веса Ultralytics; SCRFD; PP-Human) → W1-04.
9. Готовые домен-ориентированные веса (hard hat, PPE, CrowdHuman) → W1-05/W1-16 (не собирал).
10. Реальное качество малых объектов на СИЗ для вариантов P2/SAHI — нет опубликованных измерений на нашем домене; закрыть: эксперимент на данных (→ datasets, evaluation).

---

## Предлагаемые эксперименты

**Э1. «Совместимость графа» (CPU, до доступа к LinQ).** Вопрос: у каких экспортов нет операторов, которые гарантированно проблемны (TopK, GridSample, LayerNorm, Gelu и т.п.). Кандидаты: yolov5s.pt (v7.0), yolov8n/s.pt, yolo11n/s.pt, yolo26n.pt (one2many и end2end), yolox_s (Apache) — каждый из своего репозитория по зафиксированному commit/tag, экспорт ONNX opset 11–13, imgsz 640 и 416, batch 1, `dynamic=False`. Шаги (документированный интерфейс Ultralytics из чужого скрипта F06: `model.export(format="onnx", imgsz=..., opset=..., batch=1, dynamic=False, simplify=..., nms=False)`; остальное — псевдокод): загрузка → `onnx.checker.check_model` → перечисление `op_type` по графу → сохранение списка операторов в `W1-01_files`. Что измерять: множества операторов и их различия между кандидатами. Что сохранить: JSON с op_types, sha256 ONNX. Интерпретация: общий список даёт карту «минимально общих» операторов и пригодится для запроса к вендору. Что успех не подтверждает: приём графа компилятором LinQ, качество int8, скорость. Остановка: при невозможности скачать веса или несовместимости версий — зафиксировать.
**Э2. Конвертер LinQ.** Требует wheel `tpu_framework` (нет доступа). Пока — подготовка ONNX и калибровочных наборов (≥100 изображений из домена, препроцесс как в обучении; NHWC против NCHW — проверить обе формы).
**Э3. Малые объекты.** После появления датасета: сравнить imgsz 640 vs 960/1280 и P2 vs базовая голова на одном и том же сплите; метрики AP по размерным корзинам. Оговорка: ничего из этого не доказывает перенос на LinQ.

---

## Передачи соседям

- → **linq_platform:** (1) получить `tpu_framework` wheel и `tpu_compiler` (в сторонней коде импортируется `tpu_compiler.compiler.O1/O5`), версию, список операторов; (2) выяснить, существуют ли вендорские `.tpu` программы для yolo5s/yolo8/yolo11 и их входной контракт (аналог F08); (3) layout/нормировка входа после `onnx_to_tf`; (4) что внутри TPU, что на хосте (decode/NMS); (5) поддерживается ли attention/MatMul/Softmax/TopK; (6) документы `Framework_manual_H1.pdf`, datasheet HPS/HX, `pytpu` — прочитать полностью; в датасетах/ссылках страницы `/docs`: manual HP1M-01/02, HPD1M, HPQ.
- → **datasets:** классы для K1/K2 (person, helmet, no-helmet/head, vest, respirator/mask, cigarette), размер объектов, разрешение; нужны данные с малыми головами и сигаретами; кропы для K2.
- → **training_strategy:** выбор между YOLO-семействами от LinQ-совместимости; запрет «заморозить» backbone без проверки операторов; teacher-разметка YOLOE/GroundingDINO; QAT/PTQ калибровка (percentile параметр в `quantize`).
- → **evaluation:** метрики по размерным корзинам; сравнение float и int8 (F06 вывод: нужен общий протокол); не использовать COCO-цифры как оценку для СИЗ.
- → **video_architecture:** трекер вне LinQ (ByteTrack/BoT-SORT/OC-SORT MIT), batch-программы и мульти-модельный рантайм (до 5 по пресс-релизу, F09).
- → **operator_product/hackathon_strategy:** главный риск — сроки до получения конвертера; нужен fallback на вендорский tiny_yolo3-класс и каскад с классификатором.
- → **W1-04 (лицензии):** AGPL у Ultralytics, GPL у v6/v7/v9/v10, MIT у WongKinYiu/YOLO, Apache у YOLOX/PaddleDetection/D-FINE/RF-DETR(N-M), SCRFD веса, DEIM NOASSERTION.

---

## Запросы эскалации

1. **ЭС-1:** глубокий разбор экспортируемых ONNX-графов YOLOv5s/YOLOv8/YOLO11/YOLO26/YOLOX с точным списком операторов, динамикой форм и шагами упрощения (→ W1-06/07/10); материалы: SHA и пути из F11–F20.
2. **ЭС-2:** анализ стороннего репозитория `sherstpasha/linq-cv-bench@3ad1b7aa…` и пакета `pytpu` (PyPI) на предмет скрытых ограничений API (форма входа, `explicit_batch_value`, `anchors_mapping`, `output_nodes`), без запуска чужого кода без изоляции.
3. **ЭС-3:** независимый разбор поддержки attention/TopK/Softmax на LinQ, когда появится SDK.

---

## Источники

- **W1-01-S01** — «Фреймворк IVA H1. Руководство оператора» (RU.РМДВ.04.06.014-03 34 01), ООО «ХайТэк». URL: https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf. Тип: primary_documentation (PDF). Last-Modified 2025-11-25 08:34:47 GMT; 751083 B; sha256 локально `ebe0ab67…102a` (полностью в FLASH-1). Проверено: 2026-10-23 04:45 MSK; текст извлечён `pdftotext` и `pypdf` (локаторы: стр. 7–11 API, 12–21 пример, 21–22 список сетей, 23–24 вывод). Доступ: открыт.
- **W1-01-S02** — LinQ «Технологии» https://lin-q.ru/tech и документы https://lin-q.ru/docs (WebFetch). Тип: primary_documentation (маркетинг). Проверено 2026-10-23 ~04:50 MSK. Доступ: открыты. `files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf` — скачивание 8.5 МБ получено WebFetch, текст не извлекался (PDF бинарный; содержимое не прочитано).
- **W1-01-S03** — GitHub `sherstpasha/linq-cv-bench`, commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` (2026-04-03), автор Pavel Sherstnev (частное лицо), лицензии нет. Файлы: `RUN_SCENARIO.txt` (21177 B), `scr/detection/README.md`, `scr/detection/export_yolov8s_to_onnx.py`, `scr/detection/build_yolov8_program.py`, `scr/detection/run_yolov8_tpu.py`. Проверено 2026-10-23 ~04:50 MSK через `gh api`. Тип: source_code стороннего автора; недоверенные данные.
- **W1-01-S04** — Hi-Tech Mail, 2026-07-08, «На «Иннопроме» представили ИИ-ускоритель умных городских систем», https://hi-tech.mail.ru/news/150934-na-innoprome-predstavili-ii-uskoritel-umnyh-gorodskih-sistem/; также technomoscow.com/press-tsentr/novosti/79589/ и www1.ru (2026-07-12) (найдены поиском, не читались полностью). Тип: author_statement (пресс-релиз). Проверено WebFetch.
- **W1-01-S05** — Ultralytics: https://github.com/ultralytics/ultralytics, release v8.4.184, main `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`; файлы `ultralytics/cfg/models/{v5,v8,11,26,rt-detr}/*.yaml`, `ultralytics/nn/modules/head.py`, `block.py`, `engine/exporter.py`; `ultralytics/assets` release v8.4.0 (метаданные). Проверено 2026-10-23 ~04:45–04:55 MSK (`gh api`).
- **W1-01-S06** — https://docs.ultralytics.com/models/yolo26/ (WebFetch 2026-10-23). arXiv 2606.03748 не открывался.
- **W1-01-S07** — https://docs.ultralytics.com/models/ (WebFetch 2026-10-23).
- **W1-01-S08** — https://github.com/ultralytics/yolov5 (master `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce`, release v7.0 2022-11-22): README, `models/yolov5s.yaml`.
- **W1-01-S09** — https://github.com/Megvii-BaseDetection/YOLOX (main `6ddff4824372906469a7fae2dc3206c7aa4bbaee`, release 0.3.0).
- **W1-01-S10** — https://github.com/meituan/YOLOv6 (main `e86a483f3f6bded25d45970b56831345a99744a4`, release 0.4.1).
- **W1-01-S11** — https://github.com/WongKinYiu/yolov7, /yolov9 (v0.1), https://github.com/WongKinYiu/YOLO (MIT; main `c4cb5f6f56102eceeaa7d75e23e1125cd0373eaf`; release v1.0 2025-12-30).
- **W1-01-S12** — https://github.com/THU-MIG/yolov10 (v1.1).
- **W1-01-S13** — https://github.com/sunsmarterjie/yolov12 (main `2abab7153a065fb2925e8088e9ca2b19016ab7d6`), https://github.com/iMoonLab/yolov13.
- **W1-01-S14** — https://github.com/PaddlePaddle/PaddleDetection (release v2.9.0, release/2.9 `b25522a0f4bde8c80603f3ba5e3472059972e3b5`): `configs/ppyoloe/`, `configs/picodet/`, `configs/pphuman/`, `configs/mot/`; README PicoDet release/2.8 (WebFetch).
- **W1-01-S15** — https://github.com/RangiLyu/nanodet (v1.0.0, 2023-03-21).
- **W1-01-S16** — TF1 Detection Zoo https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md; TF-Slim https://github.com/tensorflow/models/blob/master/research/slim/README.md (WebFetch 2026-10-23).
- **W1-01-S17** — InsightFace SCRFD https://github.com/deepinsight/insightface/tree/master/detection/scrfd (master `c6c3af7bd2d0a0bf4b78c78437357f3521aa5d52`); arXiv 2105.04714.
- **W1-01-S18** — https://github.com/lyuwenyu/RT-DETR, https://github.com/Peterande/D-FINE, https://github.com/Intellindust-AI-Lab/DEIM, /DEIMv2, https://github.com/roboflow/rf-detr (release 1.11.2). Таблицы из README.
- **W1-01-S19** — https://github.com/AILab-CVC/YOLO-World, https://github.com/IDEA-Research/GroundingDINO, https://github.com/THU-MIG/yoloe, https://github.com/open-mmlab/mmpose (v1.3.2), ByteTrack, BoT-SORT, OC_SORT (метаданные репозиториев через `gh api`).
- **W1-01-S20** — SAHI https://github.com/obss/sahi (MIT, 0.12.8 от 2026-09-30); arXiv 2202.06934 (через WebSearch, фрагменты).
- **W1-01-S21** — PyPI `pytpu` 15.0.24: https://pypi.org/project/pytpu/ (JSON API, 2026-10-23).

Не проверено в этом запуске: arXiv API частично недоступен (rate limit/503) — идентификаторы статей сверены с README репозиториев (YOLOX, YOLOv6, YOLOv10, YOLOv12, RT-DETR, D-FINE, DEIM, DEIMv2, RF-DETR, PaddleDetection, NanoDet, YOLO-World, YOLOE, GroundingDINO, ByteTrack, MMDetection), а не через arXiv; arXiv ID Ultralytics YOLO26 — по странице документации.
