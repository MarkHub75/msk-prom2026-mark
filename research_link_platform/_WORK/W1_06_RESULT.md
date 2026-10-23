# W1-06 — операторы, преобразования графа и компилятор LinQ

Проверка: 23 октября 2026, примерно 04:19–04:30 Europe/Moscow. Ветка выполняла самостоятельный web/GitHub-поиск и чтение открытых первоисточников. SDK не установлен; экспорт, квантование, компиляция и запуск на LinQ не выполнялись. Локально выполнены клонирование двух публичных репозиториев, поиск по исходникам и AST-проверка одного идентификатора. Это исследование, а не прототип.

## Главный вопрос и вывод

Какие конкретные условия графа и compiler позволяют заранее отсеять тупиковый экспорт детектора, и что известно об автоматическом выполнении неподдерживаемых операторов на host?

Открытая документация даёт реальный путь ONNX → TensorFlow → квантованное внутреннее представление → TPU executable, параметры компиляции и конкретное предупреждение о некорректных программах при агрессивных оптимизациях. Но публичную матрицу операторов с атрибутами, opset, shapes и типами для Resize/Gather/NMS/Reshape/Transpose/Concat установить не удалось. Нельзя объявлять эти операции неподдерживаемыми. Нельзя считать успешный ONNX export доказательством прохождения конвертера и компилятора. Автоматический CPU fallback/partitioning не документирован в просмотренных материалах; его отсутствие также не доказано.

Особенно полезен независимо найденный публичный код `sherstpasha/linq-cv-bench`: есть self-build YOLOv8, vendor TinyYOLO3 и чётко вынесенный host NMS. Это воспроизводимая карта API и контрактов, но не готовый гарантированно рабочий пример: закрытые компоненты и программы не приложены, а в YOLOv8 runtime найден конкретный дефект идентификатора. При выборе модели нужно требовать точный экспорт и пример для выданной версии SDK, а не опираться на название семейства YOLO.

## Источники и область применения

**W1-06-S01.** ООО «ХайТэк», «Фреймворк для работы тензорного процессора IVA H1…», руководство оператора, RU.РМДВ.04.06.014-03 34 01, 2025, 27 PDF-страниц. [PDF](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf). Прочитан текст, сохранённый W1-03, и независимо проверено извлечение через TinyFish; встроенный web open вернул inaccessible. Локаторы: §3.1 pp7–8, §3.2 pp9–10, §3.3 p11, пример pp11–21, сети pp21–22, сообщения pp23–24, термины p25. Документ на современном официальном домене; название IVA H1 связано с LinQ H официальной /sol, но совместимость конкретных релизов не следует из этой связи.

**W1-06-S02.** ООО «ХайТэк», «Российские решения для аппаратного ускорения работы нейронных сетей», 2026; PDF metadata author Сергей Севрюков. [Презентация](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf). TinyFish извлёк весь текст, официальный /press ссылается на файл. p4 содержит версионный benchmark-контекст; p5 перечень сетей; pp7–9 compiler/cloud claims. Дата внутри 2026, точная дата публикации не установлена. Это vendor/reported evidence, не наш тест.

**W1-06-S03.** ООО «ХайТэк», [LinQ /tech](https://lin-q.ru/tech), дата публикации неизвестна; просмотрено TinyFish 2026-10-23. Разделы «Поддерживаемые сети», «Оригинальный framework». Список семейств и схема процесса, без operator support matrix.

**W1-06-S04.** ООО «ХайТэк», [LinQ /sol](https://lin-q.ru/sol), дата неизвестна; просмотрено TinyFish 2026-10-23. Разделы HPS и ПО. LinQ Compiler, DNN Quant, Graph Optimizer — заявления производителя. Python3.8 API/CLI и доступ к ПО после регистрации/верификации. Связывает IVA H1 framework с OEM LinQ H.

**W1-06-S05.** ООО «ХайТэк», [LinQ /docs](https://lin-q.ru/docs), дата неизвестна; TinyFish 2026-10-23. Публичный каталог содержит hardware manuals и один framework guide S01; отдельной таблицы операторов среди извлечённых ссылок нет. `noindex,nofollow` в metadata помогает объяснить слабый поиск, но не доказывает полноту каталога.

**W1-06-S06.** Павел Шерстнев / GitHub sherstpasha, [linq-cv-bench, pinned tree](https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140). Проверен git commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, 2026-04-03 12:44:54 +0700. [Профиль автора](https://github.com/sherstpasha) указывает Pavel Sherstnev и Candidate of Technical Sciences; связи с ООО «ХайТэк» на просмотренном профиле/в README не установлено. Первичный код автора, сторонняя работа. Клонирован целиком, не запускался. Нет приложенных `.tpu`, `.qm`, wheel SDK, JSON результатов/логов в просмотренном git tree. Не приписывать коду фактический успешный прогон.

**W1-06-S07.** Илья Биро / sttell, [IVA_compiler_runner pinned](https://github.com/sttell/IVA_compiler_runner/tree/543ab4a0e53b4efb851af5c592f8089b5685ec70), commit 2022-04-03. Авторский C++ GUI/automation вокруг custom IVA compiler. Связь с текущим LinQ SDK не доказана. Read-only clone, source review; не установлен/не собран. [Fork FeeeLyX](https://github.com/FeeeLyX/IVA_compiler_runner) — та же линия происхождения, не независимое подтверждение.

Дополнительные открытые следы: [iva-tpu 11.2.6](https://pypi.org/project/iva-tpu/11.2.6/) (2021-08-31) и [pytpu 15.0.21](https://pypi.org/project/pytpu/15.0.21/) (2023-10-30). Они показывают исторические API, но не таблицу операторов compiler и не совместимость с Runtime16.18.6. Для выводов о текущих операторах не использованы.

## Установленные факты: основание отдельно от проверки

| ID | Факт | Тип основания | Наша проверка | Источник |
|---|---|---|---|---|
| F01 | Руководство описывает ONNX→TF до квантования, затем внутреннюю модель для compiler и `.tpu` как границу Framework/SDK | primary_documentation | просмотрен документ | S01 §§3.1–3.4 |
| F02 | Compiler принимает `hardware_parameters`, `Network`, `CompileParameters`, optional `slicing_scheme`; возвращает executable + описания тензоров | primary_documentation | просмотрен документ | S01 p9 |
| F03 | Есть DEFAULT и STAGING; STAGING включает pipeline parallelism, второй DDR, cache placement, layer fusion и slicing | primary_documentation | просмотрен документ | S01 p10 |
| F04 | Документ предупреждает о недопустимых программах/долгой компиляции STAGING; рекомендует возврат DEFAULT и сообщение об ошибке | primary_documentation | просмотрен документ, не воспроизведено | S01 p10 |
| F05 | SoftwareNetwork добавляет quantization/rescaling/graph operations; HardwareNetwork повторяет TPU-операции в TF | primary_documentation | просмотрен документ | S01 pp7–8 |
| F06 | Современный список содержит YOLO8/YOLO11, SSD MobileNet, SCRFD; p4 presentation приводит yolov8n_pose и yolo5s | vendor_statement / reported_measurement | прочитан источник, не запущено | S02 pp4–5, S03 |
| F07 | Benchmark-контекст: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K | reported_measurement | только просмотрен источник | S02 p4 |
| F08 | Сторонний YOLOv8 export задаёт opset13 по умолчанию и `nms=False`; динамические оси включаются отдельным флагом | source_code | просмотрен pinned файл | S06 `scr/detection/export_yolov8s_to_onnx.py` |
| F09 | Тот же build принудительно задаёт статическую форму `(1,3,H,W)`, calibrate/quantize, затем set_batch и compiler | source_code | просмотрен pinned файл | S06 `build_yolov8_program.py` |
| F10 | Runtime YOLOv8 после inference.sync выполняет NMS на host через PyTorch/Ultralytics | source_code | просмотрен код, без TPU запуска | S06 `run_yolov8_tpu.py`:109–112, 279–290 |
| F11 | Для этого кода TPU backend требует отдельные libtpu/tpu-dkms/pytpu/tpu_framework/mlperf; реальное устройство обязательно | primary_documentation автора | просмотрен RUN_SCENARIO | S06 `RUN_SCENARIO.txt`:12–44 |
| F12 | В YOLOv8 runtime есть атрибут args с тайскими символами вместо parser destination; likely AttributeError | source_code + inference | локальный ast.parse подтвердил точный Unicode literal, не executed runtime | S06 `run_yolov8_tpu.py`:206 |
| F13 | Public operator matrix и автоматический CPU partitioning для получаемого SDK не установлены | unknown | targeted search + просмотр перечисленных документов | S01–S07 |

## Что именно известно о compiler и преобразованиях

Сигнатуры из S01, которые следует сверить с реальной средой:

- `compile_(hardware_parameters, network, parameters, slicing_scheme=None)`;
- `get_hw_params(tpu_type)`; строковый пример `128x128_asic`;
- `QuantizedModel.quantize(original_graph_def, input_shapes, output_nodes, calibration_dict, percentile=100.0, batch_axis=0, explicit_batch_value=None)`;
- `onnx_to_tf(onnx_model: onnx.ModelProto)` с заявленным результатом `Tuple[tensorflow.Graph, Dict[str,str]]`;
- `Network.from_quantized_model`, `TpuProgram.from_executable`, `to_file`.

Практический вывод (inference): компиляция — не простой перевод ONNX операторов один-в-один. Есть отдельный importer, quantization/перемасштабирование, hardware representation, memory layout/slicing и планирование. Успешный importer ещё не доказывает, что внутренний graph полностью компилируется. Пример правильного уровня диагностики: сохранить оригинальный ONNX и перечень его узлов; результат конвертации и mapping имён; `.qm`; quantized graph; compile preset и target; exit/traceback; `.tpu` и tensor descriptions. Это рекомендуемые артефакты будущего теста, а не обещанные экспортные функции всех версий.

Описанные в S01 STAGING fusion/slicing относятся к размещению и выполнению TPU частей графа. Их нельзя переименовывать в CPU/TPU graph partitioning. Документированный путь при проблеме STAGING — смена настроек компилятора. Исполнение оригинальной/квантованной модели через TF в end-to-end example — отдельная эталонная проверка, не скрытый host fallback hardware inference.

В S06 код адаптируется к несовпадениям API: сначала import converter из tpu_framework, затем onnx_direct; retry `try_simplify=True`, `False`, без аргумента; поддерживает tuple/graph результат; перебирает output names с/без `:0`; при TypeError повторяет calibrate без percentile. Это поведение конкретного скрипта. Оно не гарантирует, что каждый retry лечит ошибку operator, и может маскировать различие версий. Сохранять первый traceback, выбранный вариант и mapping обязательно для будущего эксперимента.

S06 build использует `RegularModel(..., anchors_mapping=mapping)` при наличии mapping, `RegularModel.calibrate`, `RegularModel.quantize`, `QuantizedModel.save(file_dir=..., file_name=...)`, `network, _ = Network.from_quantized_model(...)`, `network.set_batch`. В guide более простой вызов from_quantized_model показан как одиночный network, save(file_path), quantize class method. Это достаточное основание не копировать guide буквально в неизвестный SDK. Не доказано, в каком релизе менялись API. O1/O5 из `tpu_compiler.compiler` в S06 — сторонний код; семантика O1/O5 и их эквивалентность DEFAULT/STAGING не установлены.

## Матрица конкретных операторов и границы вывода

| Узел/область | Что реально найдено | Что остаётся неизвестным | Предлагаемый тест после доступа |
|---|---|---|---|
| Resize | Никакого перечня modes/attributes для LinQ не найдено | nearest/bilinear, coordinate_transform, scales vs sizes, opset versions, динамический output | минимальные ONNX графы для атрибутов именно выбранного экспорта; сравнение чисел с эталоном |
| Gather | Нет таблицы support | constant/dynamic indices, axis, negative indices, shape graph handling | отдельно constant foldable и data-dependent варианты |
| NonMaxSuppression | S06 избегает graph NMS (`nms=False`) и делает host NMS | поддержка ONNX NMS в compiler и конкретная семантика не установлены | сначала raw-head model и host NMS; затем отдельный NMS graph если нужен |
| Reshape | Общие API shapes; нет operator constraints | dynamic shape input, -1/0 semantics, compile-time folding | сравнить фиксированный экспорт и граф с shape tensor, не объявлять dynamic support заранее |
| Transpose | В терминах S01 транспонирование названо примером high-level слоя | какие permutations/ranks/dtypes компилируются | граф с перестановками из настоящей head; verify layout по контрольным значениям |
| Concat | В терминах S01 объединение названо примером слоя; operator matrix нет | axis/rank/alignment, mixed quant scales | реальные feature maps, несколько inputs, nontrivial quant ranges |
| Detector head | Списки сетей, benchmark yolov8n_pose; S06 raw output boundary | включены ли decode/DFL/NMS, точные веса/exporter/input sizes | просить поддерживаемый vendor artifact + IO descriptors и воспроизвести его до custom export |

Все строки unknown — локализованное отсутствие доказательств, не ограничение самого процессора. Наличие семейства YOLO в списке не разрешает вывести поддержку каждого из этих операторов с произвольными атрибутами. Аналогично появление `np.transpose` или `np.concatenate` в runtime code означает host preprocessing/postprocessing, а не доказанную поддержку ONNX Transpose/Concat в TPU graph.

## Найденный открытый путь YOLO и его реальные пробелы

Pinned ссылки:

- [YOLO exporter](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py).
- [Build](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py).
- [Runtime](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py).
- [Detector README](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/README.md).
- [Execution scenario](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt).

В TinyYOLO3 README автор называет подтверждённым контрактом vendor artifact `tiny_yolo3_b8_o5_128x128_asic.tpu`: input `input_1:0`, NHWC `(8,416,416,3)`, float32 `0..1`. Это заявленный автором контракт конкретного готового файла; сам файл в git не найден. Для self-build YOLOv8 другой контракт — NCHW, letterbox, RGB float /255, default 640, batch1/8. Нельзя переносить TinyYOLO preprocessing в YOLOv8 только из-за общего слова YOLO.

README разделяет Model Zoo ONNX baseline, strict raw-head TinyYOLO3 из pjreddie cfg/weights, и vendor TPU программу. Эти маршруты полезны для сравнения, но не доказывают одинаковые веса и графы. `fallback` в RUN_SCENARIO означает вспомогательный CPU/CUDA Model Zoo baseline при проблемах strict export. Это не runtime operator fallback и не исполнение на LinQ.

Окружения автора: TPU/H1 `linq_venv311`; отдельное CPU/CUDA; отдельное TensorFlow+tf2onnx для strict TinyYOLO3. Документ явно требует реального TPU host, иначе предлагает пропустить TPU секции. Он не даёт способ получить облачный доступ к LinQ или SDK. `requirements.txt` содержит numpy1.26.4, onnx~1.16.0, onnxruntime~1.18.0, tensorflow2.14.1 и другие общие зависимости, но отдельно требуются vendor packages/driver/mlperf; ultralytics импортируется YOLO скриптами, но отсутствует в requirements. Это незамкнутая среда, не lockfile рабочего SDK.

Локальная AST-проверка pinned runtime выявила `args.output_tens\u0e2d\u0e23\u0e4c_name` на строке206 (видимо: `args.output_tensอร์_name`). Parser создаёт `output_tensor_name`. При достижении этого места ожидается AttributeError ещё до Device.list_devices; это inference из кода, не воспроизведённый TPU exception. Исправление в будущем локальном experiment допустимо, но его нужно явно записать как patch; исходный репозиторий и общий код здесь не менялись.

S07 даёт исторические ошибки JSON/weights/padding/input/output и custom compiler orchestration, но не современный ONNX importer. Нельзя выдавать его `CompileError` за официальный каталог ошибок LinQ2026 или переносить ограничения четырёхмерных map на текущую платформу. Практическая ценность ограничена исторической зацепкой; глубокое расширение этой ветки проигрывает S06.

## Противоречия и неизвестные

1. Guide2025 требует Python3.11, а /sol описывает Python3.8 API; debug path guide всё ещё содержит python3.8. Причина не установлена. S06 Python3.11 env является независимой зацепкой, не официальной compatibility matrix.
2. `as_graph` в S01 имеет literal default `platform='64x64_fpga'`, но prose говорит default128x128_asic. Надо задавать target явно после сверки реального API. Это документальная неоднозначность.
3. Возврат converter в guide описан tuple, а end-to-end использует будто graph. S06 явно разбирает tuple. До доступа нельзя решить, где documentation typo, а где изменившийся API.
4. В S01 показан from_quantized_model как один Network; в S06 два результата. Требуется версия wheel и inspect.signature из реально выданной среды.
5. Список протестированных сетей2025 короче современного (заканчивается yolo5s); это различие охвата/возраста, а не доказанный регресс/противоречие.
6. Нет установленной версии onnx opset для текущего compiler; ONNX package≥1.15.0 в /sol HX — не opset13/18 compatibility. S06 opset13 — выбранная настройка автора, не универсальный лимит LinQ.
7. Нет сведений об автоматической CPU partitioning, отчёте coverage по узлам, error codes unsupported op, возможности custom kernels, динамических shapes, symbolic dimensions, multi-output graph boundaries и decode/NMS placement официального YOLO8/11 пути.

## Где искали и ошибки доступа

Поиск web и альтернативный search_service: точные `LinQ Compiler`, `dnn_quant`, `onnx_direct`, `tpu_framework`, `TPU_128x128_PARAMS`; русские «операции/компилятор», `LinQ NMS`, доменные запросы lin-q.ru/hi-tech.org с Resize/Gather/Transpose. Название LinQ сильно загрязнено .NET LINQ; такие результаты отсеяны. Общий web search точных API практически пуст; GitHub code search точного сочетания `onnx_direct onnx_to_tf` обнаружил S06. Repository search IVA TPU обнаружил S07. Это важный путь повторного поиска.

Прочитаны /docs, /tech, /sol, /press и современный PDF через TinyFish. Built-in web open трижды вернул inaccessible для /docs и файлов PDF; это ограничение инструмента, не закрытый сайт. TinyFish успешно прочёл современные источники. Старый hi-tech.org guide вернул `target_unreachable`; без содержимого не использован. GitHub fetch `/users/sherstpasha` отвергнут инструментом как unsupported endpoint, но публичный профиль открыт web. Clone обоих repo успешен. Первое чтение root README S06 failed (там README в scr/); исправлено. Первый stdout Unicode проверки упал из-за cp1251; повтор с ascii() успешен. Эти ошибки не относятся к LinQ SDK.

Собственные материалы: `_WORK/W1_06/primary_navigation.json`, `_WORK/W1_06/SOURCE_EXCERPTS.md`, pinned git clones `_WORK/W1_06/linq-cv-bench` и `IVA_compiler_runner`. Полные статьи в report не копировались.

## Конкретные будущие проверки и передача

**Приоритет доступа:** попросить wheel/version manifest compiler/framework/runtime + matching examples; operator matrix с атрибутами и supported opset; точную target platform; raw detector program и tensor metadata; объяснение CPU partitioning, если такая возможность есть; способы получить compiler logs/coverage. Задать отдельно: выполняется ли NMS/decode на host в заявленных YOLO benchmarks и входит ли это время в latency.

**Первый практический цикл:** получить один vendor known-good детектор и проверочный input/output, подтвердить `.tpu` load и аппаратный inference; сохранить IO names/layout/scales и hashes; повторить на неизменённом export с точно выданным build example. Затем custom модель с тем же exporter/input boundary. Для новой сети начать DEFAULT; сравнивать точность после converter, quantization, TLM и TPU. STAGING/O5 вводить только после правильного baseline и измерения полной latency.

**Если custom export не проходит:** локализовать последний удачный этап; сохранить первый error и минимальный subgraph; пробовать конкретную документированную настройку или vendor exporter. Raw-head + host postprocessing — обоснованный маршрут проверки, поддержанный S06, но ещё требующий подтверждения на целевой SDK и условиями кейса. Не подменять обязательный LinQ inference CPU baseline.

**До доступа:** можно статически описать экспорт (opset, оператор/атрибут inventory, symbolic shapes, head boundary); проверить эталонные outputs и preprocessing на обычном CPU/GPU; подготовить тестовые inputs для Resize/Gather/reshape/transpose/concat именно из выбранного графа. Это не подтвердит LinQ compatibility. Полезнее получить exact artifact/SDK у постановщика, чем перебирать произвольные YOLO поколения по одному названию.

Handoff для моделей: не ограничивать выбор вымышленным запретом Resize/Gather/NMS. Для runtime: использовать S06 как карту API, заранее учесть Unicode bug, missing packages и разные NHWC/NCHW контракты. Для performance: timing run_once в S06 не включает последующий NMS/preprocessing, поэтому reported graph throughput нельзя считать скоростью готовой видеоаналитики. Для второй волны: приоритет — искать публичные результаты/доклад автора S06 и официальные matched SDK examples, а не повторять общие рекламные запросы.
