# W1-05 — импорт модели и контракт model_stack

Проверка: 23.10.2026, примерно 04:18–04:24 Europe/Moscow; системные часы отдельно проверены: 2026-10-23 01:23:02 UTC. Исследовательская ветка, без установки SDK, экспорта, компиляции и аппаратного запуска. Просмотр документа не равен проверке исполнимости его примеров.

## Главный вопрос и вывод

Какой точно артефакт должен передать model_stack в стек LinQ и какие условия экспорта уже установлены?

Документирован старый подробный маршрут IVA H1 редакции -03 (2025): замороженный TensorFlow GraphDef либо ONNX ModelProto → собственный конвертер ONNX в TensorFlow → квантование с калибровочными ndarray → внутренняя квантованная модель `.qm` → внутренний `Network` → компилятор → исполняемая программа `.tpu` → отдельный TPU SDK. Сайт LinQ прямо связывает название IVA H1 с ПО для LinQ H. Это подтверждает происхождение маршрута, но не бинарную/программную совместимость с доступом хакатона.

Текущие /sol и презентация 2026 сохраняют PyTorch через ONNX; новый benchmark называет TPU Framework 2026.8.43 и TPU Runtime 16.18.6. Публичной таблицы opset/IR/operators/dynamic-shape для этих версий не найдено. **Числовой opset нельзя назначать от имени LinQ.** На /sol указаны PyTorch ≥2.0.0 и ONNX ≥1.15.0, но только внутри блока HX. Версия Python/ONNX-пакета, opset модели и версия IR — разные параметры.

Практически до SDK следует готовить модель с воспроизводимым ONNX-экспортом, явными именами и I/O metadata, статическим кандидатом batch=1, точной предобработкой, эталонными тензорами и калибровочной выборкой. Это инженерная стратегия снижения числа неизвестных, **не установленное требование компилятора**. Не переучивать всю команду под NHWC по одному примеру ResNet: универсальность layout не доказана. Не выдавать snippet guide за готовую программу: extraction показывает несколько внутренних расхождений API, требующих сверки PDF и реального SDK.

## Источники и область применимости

| ID | URL, название, автор | Дата документа; локатор | Доступ и ограничения |
|---|---|---|---|
| W1-05-S01 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — «Фреймворк IVA H1. Руководство оператора», ООО «ХайТэк»; metadata author «ХТ» | 2025; RU.РМДВ.04.06.014-03 34 01; печатные стр.4–25 | TinyFish fetch успешно получил полный текст; web open в этой ветке дал Internal Error. Сверено с сохранённым W1-03 extraction. Это два чтения текста, не два независимых первоисточника и не визуальная сверка. На титуле «Листов 28», извлечение имеет страницы 1–27; точную пагинацию PDF требуется проверить. |
| W1-05-S02 | https://lin-q.ru/sol — «Модули ускорения LinQ», ООО «ХайТэк» | Дата публикации отсутствует; блоки HP/HPD/HPQ/HPS/HX и «Программное обеспечение» | web open успешно 23.10.2026. Рекламные заявления, без матрицы совместимости. |
| W1-05-S03 | https://lin-q.ru/tech — «Технологический стек процессора LinQ», ООО «ХайТэк» | Дата отсутствует; «Поддерживаемые сети», «Оригинальный framework» | web open успешно. Семейства сетей без weights/exporter/opset/input size. |
| W1-05-S04 | https://lin-q.ru/docs — «LinQ_Документация», ООО «ХайТэк» | Дата отсутствует; «Фреймворк» | TinyFish успешно, web open Internal Error. Публичная ссылка на S01 подтверждена; закрытая загрузка ПО не означает закрытый manual. |
| W1-05-S05 | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — «Российские решения для аппаратного ускорения работы нейронных сетей», ООО «ХайТэк»; metadata Сергей Севрюков | 2026; p4 benchmark, p5 список, p7–11 продукты | TinyFish извлечение успешно. Версии runtime/framework относятся к описанному benchmark, не нашему будущему аккаунту. |
| W1-05-S06 | https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf — LinQ HPS datasheet, ООО «ХайТэк» | На просмотренном тексте дата не установлена; первая часть и таблица технических характеристик | TinyFish успешно, но кириллица кодируется `/uniXXXX`; прочитана после механического Unicode-декодирования. Поисковая дата crawl/publication не принята за дату документа. |
| W1-05-S07 | https://onnx.ai/onnx/repo-docs/Versioning.html — ONNX Versioning, проект ONNX | Страница маркирована ONNX 1.24.0 при чтении; Versioning Principles | web open/find успешно. Используется только для определения терминов, не как версия доступного LinQ. |
| W1-05-S08 | https://onnx.ai/onnx/repo-docs/IR.html — ONNX IR Specification, проект ONNX | TensorShapeProto, Static tensor shapes and names | web open/find успешно. Стандарт допускает символические размерности; это не подтверждает их поддержку LinQ. |
| W1-05-S09 | https://docs.pytorch.org/docs/2.14/onnx.html — torch.onnx, PyTorch contributors | Секция torch.onnx.export, параметр opset_version | stable URL при чтении редиректит к 2.14. Используется только общее правило согласования opset с backend; не рекомендация использовать 2.14 для LinQ. |

Все сетевые источники проверены 23.10.2026 около 04:18–04:24 MSK. Точное время отдельных HTTP-ответов инструмент не предоставил; не следует приписывать им секунды системной проверки.

## Подробные факты

Для всех F ниже статус проверки «просмотрен документ», если явно не указано другое. Ни один факт не имеет статуса «выполнен экспорт/компиляция/запуск». Тип указан отдельно.

### Форматы и версии

- W1-05-F01, primary_documentation, S01 p4: программа -03 названа доработанной и расширенной относительно -02. Следовательно, API из старого FW_TPU_H или -02 нельзя автоматически считать API -03 либо Framework 2026.8.43.
- W1-05-F02, primary_documentation, S01 p7,14,25: вход — замороженный граф с обученными весами, форматы protobuf или ONNX. Для TensorFlow пример читает бинарный файл через GFile и ParseFromString в `tf.compat.v1.GraphDef`. Для ONNX — `onnx.load(GRAPH_PATH)`. Формальная документация квантователя принимает GraphDef. Не подтверждены `.pt`, TorchScript, state_dict, Keras H5, SavedModel directory как непосредственные входы этого API. Отсутствие доказательства не является доказательством невозможности другого актуального API.
- W1-05-F03, primary_documentation, S01 p11: конвертер из модуля `onnx_direct` принимает `onnx.ModelProto`; описаны TensorFlow-граф и служебный словарь переименования слоёв. Это собственный документированный компонент; не надо подменять его сторонним onnx-tf/onnx2tf, совпадение назначения не означает эквивалентность.
- W1-05-F04, vendor_statement, S02 блоки ускорителей: PyTorch интегрируется через ONNX. В блоке HX указаны нижние границы PyTorch 2.0.0 и ONNX 1.15.0. Эти условия не являются opset=15 и не показывают верхнюю совместимую версию. Для HP/HPQ такого числового диапазона на странице нет.
- W1-05-F05, vendor_statement, S06: HPS заявляет интеграцию TensorFlow 2.x и PyTorch через ONNX. Это совместимо с использованием `tf.compat.v1.GraphDef` внутри TensorFlow 2, но не доказывает прямой импорт любого SavedModel/Keras артефакта.
- W1-05-F06, reported_measurement, S05 p4: benchmark автора использует Ubuntu 24.04, Intel Core i7-10700K @3.80 GHz, TPU Runtime 16.18.6, TPU Framework 2026.8.43. В этой версии заявлены результаты yolo5s batch1 и yolov8n_pose batch1. Размер входа, exporter, opset, веса и границы постобработки не раскрыты. Никакой локальный benchmark не проводился.
- W1-05-F07, primary_documentation, S07: стандарт отдельно версионирует IR, операторы и саму модель; release-пакета имеет ещё собственную схему версии. Inference: пакет ONNX≥1.15.0 из S02 не устанавливает допустимый opset/IR конкретного parser LinQ.
- W1-05-F08, unknown: поддерживаемые ONNX opsets/domains, maximum IR, custom ops, external tensor data, control flow и ограничения на initializers для поставки хакатона не установлены. Также не обнаружены публичные source code/commit для используемых `onnx_direct`, `tpu_framework`, `dnn_quant`.

### Контракт квантования, shapes и batch

- W1-05-F09, primary_documentation, S01 p7–9: `QuantizedModel.quantize` принимает исходный TF GraphDef, описание входных форм, выходных узлов и словарь калибровочных ndarray. Возвращаемый тип `_InMemoryQuantizedModel`. `save(file_path)` сохраняет модель; терминологический раздел именует архив `.qm`. `as_graph` отдаёт GraphDef для проверки; этот GraphDef не тождественен программе TPU.
- W1-05-F10, primary_documentation, S01 p8: аннотация `input_shapes` содержит Mapping имён в Tuple с `Optional[int]`, а `output_nodes` может быть списком имён, списком словарей или None. Не даны полная схема словарей, правила inference shape, разрешённые None и ограничения рангов. Это недостаточно для вывода «LinQ поддерживает произвольные динамические H/W».
- W1-05-F11, primary_documentation, S01 p7–8: `batch_axis=0`, `explicit_batch_value=None`; explicit_batch_value предназначен для сетей, не поддерживающих неявный batch. `as_graph` имеет batch_size и batch_axis. Пример на p16 описывает явный batch; p19 передаёт форму `(1,224,224,3)`. Термины explicit/implicit не раскрывают, меняется ли batch без перекомпиляции и какие batch sizes разрешены аппаратно.
- W1-05-F12, reported_measurement, S05 p3–4: автор приводит ResNet и ряд сетей при batch1 и batch8. Это свидетельство заявленных конкретных batch-режимов, не подтверждение универсального динамического batching. Для yolov8n_pose в таблице только batch1.
- W1-05-F13, primary_documentation, S08: ONNX различает целочисленные размерности, именованные символические размерности, неизвестные размерности и отсутствие shape. Inference: валидный ONNX с символическим N ещё не является контрактом компилятора; нужно раздельно выяснить допустимость symbol при импорте и изменение N у готовой TPU программы.
- W1-05-F14, primary_documentation, S01 p15 и25: демонстрационный calibration использует два изображения для простоты, терминологический раздел рекомендует 100 образцов. Это не минимально допустимый размер и не доказательство достаточности 100 для промышленной камеры. Подготовка образцов должна повторять предобработку модели.

### Layout, dtype, имена

- W1-05-F15, primary_documentation, S01 p13–15: пример preprocess конвертирует изображение в RGB, делает центральный crop на 85% короткой стороны, resize 224×224, переводит в float32, вычитает `[123.68,116.779,103.939]`, добавляет ось0. Калибровка явно названа NHWC; concatenation axis0. Эти параметры относятся к показанному ResNet50, не рекомендуются автоматически для YOLO. Не показан общий переключатель layout и не описано, как конвертер обрабатывает исходный NCHW ONNX.
- W1-05-F16, primary_documentation, S01 p16: `rescale(data)` готовит вход квантованного TF-графа и возвращает выход к пользовательскому формату; фактический dtype определяется операциями квантованного графа. Float32 на границе исходной модели не означает FP32 аппаратное исполнение. Runtime-пример p20–21 передаёт исходный test_input_dict без явного rescale; значит нельзя копировать процедуру rescale квантованного TF-графа на SDK без сверки фактической metadata.
- W1-05-F17, vendor_statement, S03 и S06: основной аппаратный тип int8; HPS datasheet относит fp16/bfloat16 к перспективе (extraction искажает слово bfloat16 как `b/f_loat16`). Точные dtype входа/выхода `.tpu`, accumulation, rounding, saturation и поддержка signed/unsigned не установлены.
- W1-05-F18, primary_documentation, S01 p17–21: показана граница имён: TensorFlow tensors имеют суффикс `:0`, SDK/TLM пользуются OP names; helper удаляет/добавляет нулевой суффикс. Переименование конвертером требует отдельного mapping. Не следует «обрезать всё после двоеточия» без проверки: документирован только `:0`, а пример INPUT_TENSOR_NAME extraction содержит необычное `' input:1'`.
- W1-05-F19, primary_documentation, S01 p15–21: входы/выходы исходной модели, квантованного графа, TLM и TPU проверяются одной процедурой. Демонстрационная проверка — top1 класса, не численное равенство всех значений. Для детектора нужен собственный parity protocol до NMS и task metrics после NMS.

### Компилятор и runtime boundary

- W1-05-F20, primary_documentation, S01 p9,19–20: `Network.from_quantized_model(quantized_model)` создаёт внутреннее представление. Компилятор принимает ModelParameters, Network, CompileParameters и optional slicing_scheme; возвращает пару Executable и словарь TensorDescription. Последний важен для проверки контракта тензоров; его точные fields в manual не раскрыты.
- W1-05-F21, primary_documentation, S01 p9–10: `get_hw_params(tpu_type)` и preset `TPU_128x128_PARAMS` относятся к выбору hardware target. DEFAULT предлагается для новой сети, STAGING может давать неверные программы или слишком долго компилировать. Target FPGA и ASIC нельзя выбирать по дефолту из противоречивого snippet.
- W1-05-F22, primary_documentation, S01 p20: `TpuProgram.from_executable(*tlm_program)` и `to_file(...)` создают `.tpu`. Документ прямо проводит границу: Framework принимает исходную модель и выпускает TPU программу, SDK принимает TPU программу и исполняет на данных. `.qm` и `.tpu` — разные этапы. ONNX не показан как непосредственный вход `Device.load`.
- W1-05-F23, primary_documentation, S01 p20–21: пример SDK перечисляет устройства `tpu.Device.list_devices()`, открывает первое, загружает `.tpu`, создаёт inference context и вызывает `inference.sync(input_dict_with_op_names)`. Это локальный API устройства, а не публичный облачный REST/gRPC контракт. Автор guide описывает также TLM; симуляция не доказывает фактический LinQ inference.

## Расхождения и опасные переносы

| Расхождение | Точная локализация | Интерпретация и нужная проверка |
|---|---|---|
| Converter return vs caller | S01 p11: `Tuple[tensorflow.Graph, Dict[str, str]]`; p19: `original_graph_def = onnx_to_tf(original_graph_def)`; затем quantize ожидает GraphDef | Два текстовых извлечения показывают одинаковое расхождение, но PDF визуально не просмотрен. Возможны ошибка документа, упрощённый пример или extraction loss. Не утверждать реальный runtime bug. Вторая волна: визуально p11/19, затем inspect signature, type returned object и действительный пример поставки. |
| Default platform | S01 p7: signature `platform='64x64_fpga'`, prose default `128x128_asic` | Не выбирать ни одно значение по этой строке. Проверить actual installed signature и hardware parameters целевой платы. |
| Python requirement vs site/log | S01 p5 Python3.11, p23 log path python3.8; S02 ПО API Python3.8 | Текст смешивает требования и пример журнала; журнал не спецификация. Не установлено, какой вариант соответствует Framework2026.8.43. |
| Тип и имена примера | S01 p14 `onnx.ModeProto` (в API p11 ModelProto); p12 INPUT содержит `input:1`; позднее удаляется только `:0` | Возможны опечатки/extraction. Сохранить raw literal, сверить визуально. Не вставлять в runnable code. |
| Неполнота end-to-end | S01 p19–20 описывает компиляцию, но extraction переходит к использованию `tlm_program`, полного присваивания результата компилятора в данном фрагменте нет | Не восстанавливать недостающий вызов от имени производителя. Попросить исходный end_to_end.py именно поставляемой версии. |
| TF2 claim vs GraphDef API | S06 TF2.x; S01 tf.compat.v1.GraphDef | Может сосуществовать в одном стеке, не прямое логическое противоречие. Вопрос — какие сохранённые TF артефакты импортирует текущий frontend. |

## Контракт передачи для соседнего model_stack (рекомендация, inference)

Пока нет SDK, model_stack должен передавать пакет кандидата с: точной реализацией/commit и hash весов; версиями torch/onnx/exporter и всеми export flags; `.onnx` плюс внешними данными при их наличии; `ir_version`, всей `opset_import` по domains, перечнем op_type/attributes; names, shape, dtype всех входов/выходов; описанием layout и порядка цветовых каналов; нормализацией/letterbox/padding и inverse coordinate transform; набором одинаковых test inputs и исходных outputs; представительными калибровочными данными после той же предобработки; split границ decode/NMS.

Сделать отдельный статический кандидат batch1 и фиксированного H×W как удобный первый диагностический маршрут. Никакие H×W или opset не объявлять «LinQ-compatible» до vendor sample либо фактической компиляции. Не считать внешнюю INT8 ONNX с Q/DQ эквивалентом `.qm`: S01 документирует собственный quantizer, правила импорта готового Q/DQ не найдены. Не считать CPU/ONNX Runtime parity аппаратной проверкой.

## Неизвестные, которые меняют решение

1. Точный установленный Framework/Runtime/driver и hardware target онлайн-стенда, их compatibility matrix и Python/TensorFlow/ONNX lockfile.
2. Версия и supported opset/IR `onnx_direct`; список operators/attributes, custom domains и правила dynamic shape. Поддержка ONNX package не заменяет эти ответы.
3. Актуальный frontend всё ещё ONNX→TF или новый direct ONNX importer? Доступен ли reference converter с mapping имён/layout?
4. Можно ли менять N/H/W без новой компиляции? Каковы допустимые batch и максимальные размеры? Как связаны batch_axis, explicit_batch_value и compiled tensor descriptions?
5. Layout/dtype/quantization parameters фактических `.tpu` входов/выходов; где runtime делает scaling, transpose и casts?
6. Как импортируются exported detector heads, decode и NMS? Не установлены ни встроенный NMS, ни CPU fallback, ни необходимость host-NMS.
7. Совместимы ли `.qm`/`.tpu` между версиями и платами? Нужна ли перекомпиляция; какие сведения о compiler target встроены в артефакт?

## Поиск, доступ и остаток

Самостоятельно открыты /tech и /sol, затем /docs и Framework_manual_H1.pdf через TinyFish. Просмотрены presentation2026 и HPS datasheet. Поиски: `site:lin-q.ru ONNX opset`, `site:lin-q.ru "Framework" "ONNX"`, `"onnx_direct" "onnx_to_tf"`, `"tpu_framework" "input_shapes"`, `"IVA" "ONNX" "opset"`, `"LinQ" "opset"`, `"tpu_framework" github`, `"onnx_direct" TPU`, точные одиночные имена пакетов и `site:hi-tech.org ONNX opset`. Выдача либо официальный маркетинг, либо нерелевантные ONNX/.NET/другие TPU. Найденный LocalAI `onnx_direct` — одноимённый режим и не включён в доказательства LinQ. Не найден публичный relevant GitHub source; это описание охвата поиска, а не утверждение закрытости всех репозиториев.

Попытки TinyFish получить https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-rukovodstvo-polzovatelya.pdf и https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-instrukcziya-po-ustanovke.pdf завершились `target_unreachable` именно для этих запросов. Не объявляю документы исчезнувшими. Альтернатива — подтверждённый публичный S01 и соседняя ветка истории продукта.

## Конкретные следующие проверки и handoff

- Вторая волна: визуально сверить p7,11,12,14,19–20 S01; особенно tuple/GraphDef, ModeProto и platform defaults. Не тратить время на попытку запустить буквальный extraction.
- Первые минуты доступа: сохранить package versions, vendor sample и type/signature converter; прогнать неизменённый официальный ResNet sample, сохранить `.onnx/.qm/.tpu` hashes, compiler target, input/output TensorDescription и выходы всех стадий.
- Далее один detector candidate: сначала проверить original PyTorch↔ONNX, затем ONNX↔converted TF до quantization, quantized↔TLM, TLM↔device. На каждом шаге одинаковые тензоры и отдельный numeric tolerance, затем task metrics. Это локализует importer/layout bug отдельно от quantization error и runtime error.
- Только после базового прохода исследовать дополнительный opset, batch8, dynamic axes, H/W, Q/DQ и оптимизации STAGING. Каждая переменная отдельно; ошибки сохранять с минимальным graph reproducer.
- Для branch моделей: YOLO5s, YOLO8/11 имеют vendor evidence; только yolov8n_pose и yolo5s привязаны к версии benchmark2026.8.43. Полные варианты, exporter и preprocessing не установлены; не переносить support на любую fine-tuned голову.

Краткая передача: подтвердился подробный исторический API и граница `.tpu`, но не актуальный совместимый opset. Самые ценные вопросы инженеру — текущий ONNX importer/opset/IR, I/O tensor metadata и исходный end-to-end пример; самые опасные ложные выводы — NHWC для всех моделей, ONNX1.15 как opset15, статический batch как доказанный запрет dynamic и буквальная исполнимость PDF кода.
