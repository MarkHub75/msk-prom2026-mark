# RAW_FACTS — подробная инженерная база

Собрано из всех 15 W1 и 7 W2, критики и сохранённых первичных материалов, 2026-10-23 Europe/Moscow. Сборщик не получает новых сетевых доказательств. Изученные версии — объекты чтения, не установленное окружение команды. Ни source/export/import/PTQ/QAT/compiler/device/task/event тест здесь не выполнен. Все E — [PROPOSED/UNRUN](OPEN_QUESTIONS.md#experiment-program).

Каждая карточка F содержит исходное assertion с locator/conditions/limitation/practical implication и явный actual checked scope. Встроенные “предпочесть”, “нужно”, “решение”, “expected”, “proposal/inference” — методические выводы/проекты команды; они не меняют status извлечённого факта. Неполные данные/сигнатуры отмечены UNKNOWN, не UNSUPPORTED. В S карточках сохранены publication/version отдельно от доступа.

Повторные наблюдения одной реализации сохранены, когда они несут разные условия (shape, timing, semantics, version seam). Это перекрывающиеся основания, не независимые подтверждения. W2 уточнения имеют приоритет над обобщением W1 в тех же границах; [распоряжения автора](_WORK/AUTHOR_HANDOFF.md) отдельно фиксируют supersession.

<a id="F001"></a>
## F001

**Assertion:** Кейс требует полезных своевременных уведомлений с доказательством, подавления дублей, LinQ inference и замера скорости. На с.8 обещаны VM и service; grant/API/custom upload из обещания не следуют. С.5 говорит о нескольких секундах, с.12 иллюстрация 30 секунд не универсальный норматив; с.19 нет mAP/δ/FPS/α.

**Evidence / checked scope / limitation / implication:** LOCAL primary case reading root; S001/S002, с.5/7/8/12/13/19. Проверены PDF hash и визуальные рендеры; модели/доступы не проверены. Следствие: quality, event utility и device proof нужны отдельно, budgets принимаются командой.

<a id="F002"></a>
## F002

**Assertion:** Фактически выполнена исследовательская работа W1 (15 отдельных задач, 12 general+3 LinQ), fresh critic и W2 (7 задач). Модельные и hardware эксперименты не выполнялись.

**Evidence / checked scope / limitation / implication:** LOCAL process evidence S004, wave manifests/RUN_STATE. Проверены сохранённые 22 результата; actual target stack/model/GT/access неизвестны. Следствие: ни один E или proposed route не обозначать прошедшим.

<a id="F003"></a>
## F003

**Assertion:** Существующие материалы соседних topics — вторичные leads; их результаты не являются выполненными нами экспериментами.

**Evidence / checked scope / limitation / implication:** LOCAL provenance S004/S002 и source records веток. Сборщик не переносит соседние F001 без topic namespace. Для закрытого catalog без checkpoint возможен только service-to-GT claim, не checkpoint fidelity; отдельные actual grants требуются в Q001/Q002.

## W1-01 — Эталон, provenance, golden pack и воспроизводимый baseline — нормализованные наблюдения

<a id="F004"></a>
### F004 — `W1-01-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

PyTorch не гарантирует полную воспроизводимость между releases/commits/platforms и CPU/GPU при одинаковом seed. [S005](SOURCES.md#S005): строки 6–8. Настройки deterministic algorithms и reseeding DataLoader разобраны в соответствующих разделах

Documentation, прочитано. Seed фиксировать вместе с runtime/device; сначала измерить повторяемость самого baseline. Детерминированные алгоритмы могут замедлять работу или отсутствовать

**S support:** [S005](SOURCES.md#S005). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F005"></a>
### F005 — `W1-01-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Восстановление `state_dict` требует создания класса модели; `model.eval()` меняет режим dropout/BatchNorm. Полная pickle-модель привязана к классу/структуре каталогов; `strict=False` допускает несовпадающие ключи. [S006](SOURCES.md#S006): Inference / Entire Model / Warmstarting

Documentation, прочитано. Сохранить архитектуру и режим; успешная частичная загрузка не подтверждает тождество модели. Optimizer нужен для возобновления обучения, не обязателен для отдельного inference baseline

**S support:** [S006](SOURCES.md#S006). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F006"></a>
### F006 — `W1-01-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

ONNX tests разделены на node и model; model test включает модель и пары входов/выходов. [S007](SOURCES.md#S007): строки 13–24

Documentation, прочитано. Поддерживает конструкцию сериализованных fixtures, но тесты ONNX не дают гарантии качества целевой производственной задачи

**S support:** [S007](SOURCES.md#S007). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F007"></a>
### F007 — `W1-01-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Runner при отсутствии ранее сохранённых expected outputs может вычислить их через `onnx.reference.ReferenceEvaluator(onx)`; затем пишет `output_i.pb`. [S008](SOURCES.md#S008): строки 427–447

Code observation, не выполнено. Reference от ONNX не является независимым свидетельством корректности самого экспорта

**S support:** [S008](SOURCES.md#S008). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F008"></a>
### F008 — `W1-01-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Runner сравнивает число выходов, shape, dtype и численную близость с переданными `rtol`, `atol`; fixtures читает как `test_data_set*/input_i.pb`, `output_i.pb`. [S008](SOURCES.md#S008): `assert_similar_outputs`, строки 185–229 и 468–489

Code observation, не выполнено. Переносимый образец интерфейса проверки; допуски ONNX-тестов не переносить автоматически на detector/pose/event

**S support:** [S008](SOURCES.md#S008). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F009"></a>
### F009 — `W1-01-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Информация теста не должна использоваться для выбора модели или fit преобразований; split следует сделать до обучения preprocessing. [S009](SOURCES.md#S009): §12.2

Documentation, прочитано. Отдельно держать training/calibration/tuning и закрытую оценку; одинаковый transform при inference не означает обучение transform на всех данных

**S support:** [S009](SOURCES.md#S009). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F010"></a>
### F010 — `W1-01-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

GroupShuffleSplit разделяет по заданным группам, размеры относятся к группам; тестовые множества разных случайных folds могут пересекаться. Integer random_state даёт воспроизводимое разбиение. [S010](SOURCES.md#S010): строки 638–670

Documentation, прочитано. Один раз сохранить готовые manifests; не считать несколько вызовов split независимыми наборами и не делить соседние кадры как независимые наблюдения

**S support:** [S010](SOURCES.md#S010). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F011"></a>
### F011 — `W1-01-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

ONNX допускает metadata для описания модели/producer/version; tensor имеет тип, форму и данные. [S011](SOURCES.md#S011): Metadata / Supported Types

Documentation, прочитано. Метаданные полезны для связи с внешним manifest, но сами по себе не доказывают происхождение весов и не заменяют хеши файлов

**S support:** [S011](SOURCES.md#S011). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F012"></a>
### F012 — `W1-01-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

По конспекту root кейс требует уведомления с доказательством/камерой/временем/типом, подавления дублей и замера LinQ; на с.8 заявлен удалённый VM/сервис. Формул mAP/event recall, допуска квантования и точного минимального FPS в конспекте нет. [S002](SOURCES.md#S002): с.5/7/8/13/19

Внутрикомандное свидетельство по локальному кейсу. Golden pack должен включать outputs уведомлений и timestamps; обещанный VM не считать полученным доступом или установленным API

**S support:** [S002](SOURCES.md#S002). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-01](_WORK/W1_01.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-02 — PyTorch → ONNX: выбор экспортёра и проверка эквивалентности — нормализованные наблюдения

<a id="F013"></a>
### F013 — `W1-02-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

PyTorch 2.9: `dynamo=True` default; с 2.7 `optimize=True` default. В 2.6 training/operator_export_type/do_constant_folding deprecated, folding всегда включён. [S012](SOURCES.md#S012), API / versionchanged

Явно записывать exporter и optimize. Совет «выключить constant folding» не универсален для новых версий

**S support:** [S012](SOURCES.md#S012). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 32.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F014"></a>
### F014 — `W1-02-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Любые non-Tensor args hard-coded; opset выбирать по backend. `dynamic_shapes` предназначен для dynamo, `dynamic_axes` для legacy. [S012](SOURCES.md#S012), parameters args/opset/dynamic_shapes

Флаг `scale`, Python bool, list/int или `.item()`-зависимая логика требуют аудита; динамическая ось не превращает Python-константу в runtime input

**S support:** [S012](SOURCES.md#S012). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 33.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F015"></a>
### F015 — `W1-02-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

`torch.jit.trace` записывает выполненные Tensor-операции, не записывает if/loops и фиксирует поведение training/eval при trace. [S013](SOURCES.md#S013), Warning, строки веб-документа 82–86

Формально допустимая модель может тихо выдавать неверную ветку. Смена `.eval()` после trace не возвращает исходную семантику

**S support:** [S013](SOURCES.md#S013). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 34.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F016"></a>
### F016 — `W1-02-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Ultralytics helper `torch2onnx`, [S017](SOURCES.md#S017):37–48, использует `dynamo=False` при TORCH_2_4 и `dynamic_axes`; [S018](SOURCES.md#S018):629–666 вызывает его

Не приписывать Ultralytics новые capture-гарантии только из версии torch

**S support:** [S017](SOURCES.md#S017), [S018](SOURCES.md#S018). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 35.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F017"></a>
### F017 — `W1-02-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

PyTorch 2.9 exporter вызывает verification на example_inputs, если args/kwargs отдельно не заданы. [S015](SOURCES.md#S015):149–185. [S016](SOURCES.md#S016):1592–1628 сравнивает max_abs>=5e-3 и max_rel>=1e-1, выдаёт warnings и output_accuracy=False; комментарий называет порог arbitrary

Эти числа — **внутренние диагностические пороги данной версии**, не допуск для детекции/pose и не обещание качества. CI должен отдельно читать статус/метрики и запрещать регрессию

**S support:** [S015](SOURCES.md#S015), [S016](SOURCES.md#S016). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F018"></a>
### F018 — `W1-02-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Ultralytics [S018](SOURCES.md#S018):438–452: нулевой пример с export batch и imgsz, deepcopy, `.eval()`, `.float()`, `.fuse()`

Сравнение только на нулях недостаточно. Промежуточное сравнение после подготовки модели позволяет отделить fusion/export-mode от ONNX translation

**S support:** [S018](SOURCES.md#S018). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F019"></a>
### F019 — `W1-02-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019) Detect.forward:114–124 возвращает Tensor в export, `(y,x)` в обычном eval. `_inference`:159–167: DFL decode + class sigmoid. Pose.forward:355–363 добавляет keypoints; kpts_decode:365–383 имеет отдельные export/non-export ветви

Сравнивать согласованный первый inference Tensor, а не произвольный tuple. «Raw ONNX» здесь уже содержит decode boxes и sigmoid, но без NMS. Повторный sigmoid/DFL — ошибка контракта

**S support:** [S019](SOURCES.md#S019). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F020"></a>
### F020 — `W1-02-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019):349–350 задаёт `nk=kpt_shape[0]*kpt_shape[1]`; export keypoints декодируются с anchors/strides, при ndim=3 confidence sigmoid. Обычный Detect формирует 4+nc каналов, Pose добавляет nk

Нельзя жёстко предполагать 80 классов, 17×3 keypoints или отдельный objectness для custom head. Для этой ветки ожидается B×(4+nc+nk)×A без NMS, B×(4+nc)×A для Detect; архитектуры end2end имеют другой путь

**S support:** [S019](SOURCES.md#S019). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F021"></a>
### F021 — `W1-02-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S018](SOURCES.md#S018):645–653 динамические input B/H/W; для NMS удаляется динамическая anchors-ось output. [S018](SOURCES.md#S018):1392–1400 содержит padding к export batch и loop `for i in range(bs)`, комментарий о loop unroll; выход 1398–1448 padded до max_det

«dynamic=True» не обещает произвольный batch для NMS. Превышение export batch запрещать на уровне интерфейса до доказательного теста; наличие symbolic batch в metadata недостаточно

**S support:** [S018](SOURCES.md#S018). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F022"></a>
### F022 — `W1-02-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S018](SOURCES.md#S018):671–680 вызывает onnxslim и перехватывает ошибку; 687–690 понижает `ir_version` до 10 при большем значении

Учитывать успешность pass по логам/графу. Понижение IR header кодом библиотеки не является общим рецептом совместимости и не доказывает корректность

**S support:** [S018](SOURCES.md#S018). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F023"></a>
### F023 — `W1-02-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S014](SOURCES.md#S014) tutorial: prerequisites torch>=2.8; обычный data-dependent conditional не проходит capture; демонстрируется refactor через `torch.cond`

Предпочитать явную ошибку capture тихой специализации, но refactor проверять на обоих исходах и на целевом runtime. Поддержка ONNX If у LinQ неизвестна

**S support:** [S014](SOURCES.md#S014). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F024"></a>
### F024 — `W1-02-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

ONNX checker [S020](SOURCES.md#S020): `check_model` проверяет consistency; `full_check=True` дополнительно shape inference; custom domains по умолчанию не проверяются. [S021](SOURCES.md#S021) Resize показывает разные coordinate_transformation_mode и nearest_mode

Валидность ONNX не равна численной эквивалентности. При смене opset/интерполяции проверять ramp/impulse, границы и размеры, включая вырожденные

**S support:** [S020](SOURCES.md#S020), [S021](SOURCES.md#S021). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-02](_WORK/W1_02.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-03 — безопасное преобразование ONNX-графа — нормализованные наблюдения

<a id="F025"></a>
### F025 — `W1-03-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D/C [S022](SOURCES.md#S022): IR и версия операторов развиваются независимо; `check_model(..., full_check=True)` дополнительно запускает проверку shape inference. Checker проверяет consistency, не сравнивает выходы с исходной моделью.

Не понижать вручную `ir_version`/`opset_import`, не считать checker доказательством качества.

**S support:** [S022](SOURCES.md#S022). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F026"></a>
### F026 — `W1-03-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D/C [S023](SOURCES.md#S023): shape inference неполон, динамический Reshape может остановить распространение; не каждый оператор имеет inference. `strict_mode=True` сообщает ошибки вместо молчаливой остановки; `data_prop` ограничен частью операций.

Неизвестная промежуточная форма сама по себе не означает некорректную сеть; конкретную форму проверять исполнением и контрактом.

**S support:** [S023](SOURCES.md#S023). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F027"></a>
### F027 — `W1-03-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

C [S024](SOURCES.md#S024), [S025](SOURCES.md#S025): API/CLI default `check_n=0`; compare сначала вызывает checker, затем `for i in range(n_times)`, после цикла возвращает True.

`check_ok=True` при0 = структурная проверка без численного inference. Зафиксировать число реально проверенных входов.

**S support:** [S024](SOURCES.md#S024), [S025](SOURCES.md#S025). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F028"></a>
### F028 — `W1-03-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

C [S025](SOURCES.md#S025): проверка onnxsim использует CPUExecutionProvider, отключённую ORT graph optimization, случайные uniform-входы либо `input_data`, `np.allclose(rtol=1e-4, atol=1e-5)`.

Это sanity check инструмента, не target-runtime test. Значения допусков не переносить в командный gate; повторение одного `input_data` не расширяет покрытие.

**S support:** [S025](SOURCES.md#S025). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F029"></a>
### F029 — `W1-03-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S026](SOURCES.md#S026): Softmax11 логически приводит вход к2D относительно axis (default1);13 нормирует непосредственно по axis (default−1).

Даже с явно заданным одинаковым axis семантика для rank>2 может отличаться. Проверять DFL/attention/class-axis при смене opset.

**S support:** [S026](SOURCES.md#S026). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F030"></a>
### F030 — `W1-03-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S021](SOURCES.md#S021): Resize13 half_pixel: `(x+0.5)/scale−0.5`; asymmetric: `x/scale`; align_corners зависит от концов интервала; nearest_mode отдельный параметр.

Замена Resize/интерполяции требует сравнения координат выборки. Одинаковый H×W не гарантирует равенства feature maps.

**S support:** [S021](SOURCES.md#S021). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F031"></a>
### F031 — `W1-03-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S021](SOURCES.md#S021): Resize13 использует либо scales, либо sizes; mode/coordinate transformation/nearest rounding — отдельные свойства; cubic_coeff_a по умолчанию−0.75.

При замене scales→sizes проверить округление размеров и эквивалентный sampling; нельзя считать nearest и bilinear взаимозаменяемыми.

**S support:** [S021](SOURCES.md#S021). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F032"></a>
### F032 — `W1-03-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S027](SOURCES.md#S027), [S028](SOURCES.md#S028): Transpose переставляет оси; без perm обращает их порядок. Reshape сохраняет число элементов;0 обычно копирует соответствующий размер,−1 выводится; allowzero меняет смысл0.

Reshape не заменяет NCHW↔NHWC. Формы и значения проверять раздельно, особенно нулевые/единичные измерения.

**S support:** [S027](SOURCES.md#S027), [S028](SOURCES.md#S028). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F033"></a>
### F033 — `W1-03-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S029](SOURCES.md#S029), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031): Gather выдаёт rank `q+r−1`; Slice зависит от starts/ends/axes/steps и их знаков; Concat требует равенства остальных измерений и сохраняет порядок входов.

Scalar index и `[index]` меняют rank по-разному. После layout rewrite перевести axis, shape/index tensors и ветви concat согласованно.

**S support:** [S029](SOURCES.md#S029), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 58.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F034"></a>
### F034 — `W1-03-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S032](SOURCES.md#S032): стандартный ONNX Conv описывает N,C,spatial layout и веса M,C/group,spatial; SAME_UPPER/LOWER различаются стороной дополнительного padding при нечётном паддинге.

Перевод layout не сводится к размерности входа. При замене auto_pad→pads важны stride/dilation/group и асимметрия геометрии.

**S support:** [S032](SOURCES.md#S032). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 59.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F035"></a>
### F035 — `W1-03-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D [S033](SOURCES.md#S033), [S034](SOURCES.md#S034): Sigmoid — поэлементная функция. NMS11 принимает boxes `[B,N,4]`, scores `[B,C,N]`, возвращает индексы `[K,3]`; default max_output_boxes_per_class=0 означает отсутствие выбранных боксов.

Дублирование/удаление Sigmoid и замена NMS меняют контракт. Для center_point_box=0 порядок — y1,x1,y2,x2; индексы — batch,class,box.

**S support:** [S033](SOURCES.md#S033), [S034](SOURCES.md#S034). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 60.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F036"></a>
### F036 — `W1-03-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D/C [S035](SOURCES.md#S035), [S036](SOURCES.md#S036): ORT различает Basic/Extended/Layout; offline optimization зависит от EP/options/hardware. В v1.23.2 constant folding исполняет CPU kernel; Shape folding опирается на concrete shape.

Сохранять portable исходник отдельно от runtime-optimized артефакта. Статическая специализация может материализовать форму; неверный input contract превращается в неверные константы.

**S support:** [S035](SOURCES.md#S035), [S036](SOURCES.md#S036). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 61.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F037"></a>
### F037 — `W1-03-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

R [S037](SOURCES.md#S037): автор сообщает на мини-графе FP16 Conv→Add→Cast→Reciprocal при указанном окружении: fusion даёт V=0 и +Inf вместо ненулевого V и конечного Y; checker full_check проходит; отключение ConvAddFusion восстанавливает результат. Мы не воспроизводили.

Контрпример универсальной гарантии «fusion сохраняет числа»; проверить cancellation/малые значения и finite-mask после fuse. Нельзя объявлять все версии ORT/LinQ дефектными.

**S support:** [S037](SOURCES.md#S037). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 62.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F038"></a>
### F038 — `W1-03-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

R [S038](SOURCES.md#S038): автор сообщает Range(3,−1,−1)→Gather: Extended/All дают пустой выход, Disabled/Basic/отключённый GatherToSliceFusion — ожидаемые4 значения. Проверено автором, не нами.

Shape/index rewrites тестировать на отрицательных шагах, boundary indices и zero-sized outputs; изолировать конкретный pass.

**S support:** [S038](SOURCES.md#S038). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 63.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F039"></a>
### F039 — `W1-03-F15`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

C [S039](SOURCES.md#S039): extract_model использует точные имена tensor inputs/outputs; граница не должна разрезать subgraph If/Loop. convert_version может завершиться RuntimeError для неподдержанного adapter.

Диагностические подграфы строить по тензорам и легальным границам. Наличие converter не гарантирует downgrade любой модели.

**S support:** [S039](SOURCES.md#S039). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 64.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F040"></a>
### F040 — `W1-03-F16`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

D/C [S040](SOURCES.md#S040)/S22: ORT выбирает подграфы по capability и приоритету EP; регистрация провайдера не означает исполнение всех узлов на нём. Внутренний disabled_optimizers существует в проверенной версии.

CPU fallback — диагностическая возможность ORT; LinQ fallback неизвестен. Логировать placement; точечное отключение pass версионно закреплять.

**S support:** [S040](SOURCES.md#S040), [S042](SOURCES.md#S042). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-03](_WORK/W1_03.md), строка 65.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-04 — Detection/Pose outputs, decoder и NMS — нормализованные наблюдения

<a id="F041"></a>
### F041 — `W1-04-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S043](SOURCES.md#S043) `run_yolov8_tpu.py:176–183`, code observation: rank=3 обязателен; только `shape[1] in (84,85)` либо `shape[2] in (84,85)`

Для обычного custom Detect C=1/2/3 обе стандартные ориентации с большим A отвергаются. Если A случайно 84/85, эвристика может принять неверную ось. Форму выводить из manifest, не из COCO-констант

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F042"></a>
### F042 — `W1-04-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S043](SOURCES.md#S043):164–173 `pick_output` после попытки exact-name может выбрать единственный output либо первый ndarray rank≥3. [S043](SOURCES.md#S043):206 читает `args.output_tensอร์_name`, тогда как CLI объявляет `--output-tensor-name`

Второе — статически видимый AttributeError для обычного Namespace на этом пути, до inference. Первое — опасная неоднозначность для segmentation/multihead: требовать совпадение объявленных output names, dtype, shape и semantic role

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F043"></a>
### F043 — `W1-04-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S043](SOURCES.md#S043):272–279 modern Ultralytics NMS вызывается без `nc`; 284–305 готовые class_idx отображаются через COCO80_TO_91. Зависимость runtime Ultralytics не зафиксирована этим файлом

C=85 принят normalizer, но при применении проверенного NMS [S045](SOURCES.md#S045) он интерпретируется как 81 class channel, не YOLOv5 objectness+80. У custom классов COCO mapping семантически неверен даже после починки shape. Это условный вывод по связке двух кодов; установленная версия на реальном LinQ неизвестна

**S support:** [S043](SOURCES.md#S043), [S045](SOURCES.md#S045). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F044"></a>
### F044 — `W1-04-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019) `Detect.__init__:87–108`, `forward:114–124`, `_inference:159–167`, `decode_bboxes:182–189`; [S044](SOURCES.md#S044) `DFL:58–80`. Code observation, Ultralytics 8.3.230

Export до NMS уже имеет DFL expectation, decode и sigmoid. Anchor-free здесь не означает отсутствие anchor **points** в decode. R=16 не равно количеству anchor boxes. Не применять YOLOv5 anchor formulas

**S support:** [S019](SOURCES.md#S019), [S044](SOURCES.md#S044). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F045"></a>
### F045 — `W1-04-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019) `Pose.forward/kpts_decode:349–383`: nk=K·D; xy=(raw×2+anchor−0.5)×stride; D=3 confidence sigmoid. [S045](SOURCES.md#S045):73–76,112: extras определяются по заданному nc

Без явного nc pose coordinates могут стать «классами» с confidence>1. Сохранить K,D, суставную схему и принадлежность keypoints выбранному box

**S support:** [S019](SOURCES.md#S019), [S045](SOURCES.md#S045). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F046"></a>
### F046 — `W1-04-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019) `Segment.forward:253–262`: export возвращает concatenated detection+mask coefficients и prototypes

Нельзя обрабатывать segmentation как обычный Detect, выводить C по сумме каналов или выбрасывать второй output. Это также контрпример стратегии «первый output всегда достаточен»

**S support:** [S019](SOURCES.md#S019). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F047"></a>
### F047 — `W1-04-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S046](SOURCES.md#S046) `Detect:44–79`, [S047](SOURCES.md#S047) `non_max_suppression:909–910,946–959`. YOLOv5 v7.0: C+5, BNC, objectness filter и product с class confidence

Даже одинаковое C или похожие названия не означают идентичный decoder. Для obj=.5,class=.8 ожидается score=.4, у v8 probability=.8 остаётся .8; это арифметический пример, не измерение

**S support:** [S046](SOURCES.md#S046), [S047](SOURCES.md#S047). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F048"></a>
### F048 — `W1-04-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S019](SOURCES.md#S019) `forward_end2end:126–147`, `postprocess:191–213`; [S045](SOURCES.md#S045):66–70

End2end output N×6 означает готовые score/class и обход обычного NMS. Эвристика [S045](SOURCES.md#S045) `shape[-1]==6` неоднозначна: ошибочно транспонированный custom nc=2 B×A×6 тоже попадёт сюда, но его последние каналы — два class scores, а не score+class_idx

**S support:** [S019](SOURCES.md#S019), [S045](SOURCES.md#S045). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F049"></a>
### F049 — `W1-04-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S045](SOURCES.md#S045):13–28,73–86,114–164: defaults conf=.25, IoU=.45, multi_label=False, agnostic=False, max_det=300, max_nms=30000, max_wh=7680; strict score>; class offsets; time_limit=2+.05·B при defaults; при превышении break

Эти числа — defaults конкретной библиотеки, не целевые пороги кейса. Если остановка по времени сработала, следующие элементы batch могут остаться пустыми. Логи превышения — FAIL полноты processing, а не доказательство отсутствия объектов

**S support:** [S045](SOURCES.md#S045). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F050"></a>
### F050 — `W1-04-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S018](SOURCES.md#S018):465–470 экспортёр выставляет `m.xyxy=self.args.nms and not coreml`. NMSModel:1390–1448 использует max-class, score>conf, class-aware/agnostic, max_det, zero padding. Для TF/ONNX OBB предварительный top-k min(max_det×5,A); для обычного ONNX axis-aligned этой ветки нет

NMSModel не всегда равен внешнему non_max_suppression с произвольными параметрами: нет multi-label пути, другая pre-NMS cap/time policy, уже xyxy от головы. Padding нельзя принимать за реальные detections. Динамический export batch ограничен trace/unroll — см. W1_02

**S support:** [S018](SOURCES.md#S018). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F051"></a>
### F051 — `W1-04-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S048](SOURCES.md#S048) ONNX NonMaxSuppression opset 11, `Operators.md:21322–21364`: boxes B×A×4, scores B×C×A, center_point_box=0 означает y1,x1,y2,x2; =1 cxcywh; max_output_boxes_per_class default 0; output int64 [batch,class,box]

Не подставлять ONNX output в decoder готовых N×6. Лимит per-class не равен глобальному max_det. Нужны Gather, score lookup, sorting и global cap по оговорённой политике

**S support:** [S048](SOURCES.md#S048). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F052"></a>
### F052 — `W1-04-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S048](SOURCES.md#S048):21325 описывает удаление score ниже threshold, тогда как [S045](SOURCES.md#S045) использует strict >. [S049](SOURCES.md#S049) torchvision nms docs, Parameters/Returns: xyxy, suppression IoU>threshold, индексы по score descending

Ровно threshold — обязательный boundary test: документация ONNX не заменяет проверку effective runtime. Не объединять score cutoff, IoU cutoff и event confidence в один параметр

**S support:** [S045](SOURCES.md#S045), [S048](SOURCES.md#S048), [S049](SOURCES.md#S049). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F053"></a>
### F053 — `W1-04-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S049](SOURCES.md#S049) Warning: при equal scores выбранные индексы CPU/GPU не обязаны совпадать. [S045](SOURCES.md#S045):150–156 также выбирает torchvision или TorchNMS по наличию torchvision в sys.modules

Tie handling зависит от конкретного пути; наличие импортированного пакета меняет реализацию без изменения аргументов. Логировать implementation/backend; для exact-match gate нужны deterministic policy либо оговорённая tie-equivalence

**S support:** [S045](SOURCES.md#S045), [S049](SOURCES.md#S049). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F054"></a>
### F054 — `W1-04-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S050](SOURCES.md#S050) DETR `PostProcess:269–286`: softmax; убрать последний канал no-object; cxcywh→xyxy; ×W/H; без NMS. [S019](SOURCES.md#S019) RTDETRDecoder:981–982 и [S051](SOURCES.md#S051) predictor:54–72: sigmoid concatenation, max-class/sort/max_det и original-scale output

DETR и RT-DETR нельзя обслуживать единственным «transformer decoder», не проверив конкретный output. Автоматический softmax на RT-DETR меняет scores

**S support:** [S019](SOURCES.md#S019), [S050](SOURCES.md#S050), [S051](SOURCES.md#S051). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F055"></a>
### F055 — `W1-04-F15`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S052](SOURCES.md#S052) FasterRCNN class docstring:61–73, [S053](SOURCES.md#S053) RoIHeads.postprocess_detections:671–726: softmax, убрать background label0, class-wise NMS, detections_per_img

Высокоуровневый eval output уже postprocessed. Если для parity нужен pre-NMS stage, выводить его специальным проверенным wrapper; не притворяться, что доступен готовый YOLO-style raw

**S support:** [S052](SOURCES.md#S052), [S053](SOURCES.md#S053). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F056"></a>
### F056 — `W1-04-F16`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S054](SOURCES.md#S054) SimCCLabel.decode:156–200; [S055](SOURCES.md#S055) get_simcc_maximum:41–105: axis argmax, опциональный softmax, score=min(max_x,max_y), invalid coords=-1 при score≤0; coords /split_ratio, optional DARK/visibility

Keypoint score не является универсальной sigmoid probability; сохранять codec config. Нельзя применять YOLO keypoint formulas к SimCC и наоборот

**S support:** [S054](SOURCES.md#S054), [S055](SOURCES.md#S055). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-04](_WORK/W1_04.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-05 — предобработка, обратная геометрия и временная идентичность кадра — нормализованные наблюдения

<a id="F057"></a>
### F057 — `W1-05-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F057](RAW_FACTS.md#F057) [[S057](SOURCES.md#S057), 122–132; code observation].** Для списка numpy кадров preprocess меняет BGR→RGB, BHWC→BCHW, делает contiguous, переводит в floating type и делит на 255. Для уже переданного torch tensor цвет/раскладка и `/255` в этой функции пропускаются. Условие: конкретный BasePredictor v8.3.0. Следствие: сравнение numpy и tensor API требует отдельно сформировать равный тензор; dtype float ещё не гарантирует правильный диапазон.

**S support:** [S057](SOURCES.md#S057). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F058"></a>
### F058 — `W1-05-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F058](RAW_FACTS.md#F058) [[S057](SOURCES.md#S057), 154–156; [S056](SOURCES.md#S056), 1563–1588; code observation].** Минимальный rectangle включается по сочетанию same_shapes и backend `.pt`; letterbox округляет resized dimensions и делит остаток padding, а `auto` берёт остаток по stride. `scaleFill` использует разные отношения по x/y, `scaleup=False` ограничивает увеличение. Следствие: записывать фактическую shape, настройки и все четыре паддинга; название `imgsz640` недостаточно.

**S support:** [S056](SOURCES.md#S056), [S057](SOURCES.md#S057). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F059"></a>
### F059 — `W1-05-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F059](RAW_FACTS.md#F059) [[S058](SOURCES.md#S058), 88–123 и 749–760; [S059](SOURCES.md#S059), 50–52; code observation].** В этой версии pose boxes после scale_boxes ещё округляются; points проходят scale_coords. При отсутствии ratio_pad box pad восстанавливается через round(...−0.1), point pad — дробно. Следствие: отличать intended reference behavior от собственного «исправления»: изменение округления только в новом runtime разрушит parity. Также эти helpers используют один gain; для stretch/crop нельзя без проверки применять их как общий inverse.

**S support:** [S058](SOURCES.md#S058), [S059](SOURCES.md#S059). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F060"></a>
### F060 — `W1-05-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F060](RAW_FACTS.md#F060) [[S058](SOURCES.md#S058), clip_boxes и xywh2xyxy; code observation].** В xywh2xyxy x/y — центр, ширина/высота делятся пополам; clipping допускает правую/нижнюю геометрическую границу W/H. Следствие: именовать формат `cxcywh`, `tlwh` или `xyxy`; bbox boundary W не равна индексу последнего pixel W−1. Тест 1×1 отличает соглашения площади с `+1` и без него. Не менять соглашения GT/decoder молча.

**S support:** [S058](SOURCES.md#S058). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F061"></a>
### F061 — `W1-05-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F061](RAW_FACTS.md#F061) [[S060](SOURCES.md#S060); code observation].** GeneralizedRCNNTransform требует floating images и применяет `(image−mean)/std`, resize min/max и bilinear align_corners=False; batch padding добавляется справа/снизу нулями уже в нормализованном пространстве. Postprocess возвращает боксы и keypoints к original sizes с отношениями каждой оси, а третий компонент keypoints не масштабирует. Условие: не все torchvision модели, именно использующие этот transform. Следствие: внешний mean/std/resize может задвоиться при экспорте полного wrapper; «нулевой padding» здесь не означает чёрный raw RGB.

**S support:** [S060](SOURCES.md#S060). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F062"></a>
### F062 — `W1-05-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F062](RAW_FACTS.md#F062) [[S061](SOURCES.md#S061); schema documentation].** Resize задаёт разные отображения центров пикселей: half_pixel `(u+0.5)/s−0.5`, asymmetric `u/s`, align_corners `u*(Nin−1)/(Nout−1)`, а pytorch_half_pixel отдельно обрабатывает длину выхода 1. Следствие: совпадающий размер и слово bilinear не устанавливают одинаковые пиксели. Проверять actual node attributes, scales/sizes, antialias и nearest rounding; значения и наличие атрибутов зависят от schema. Не переносить атрибут новой schema на старую модель.

**S support:** [S061](SOURCES.md#S061). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F063"></a>
### F063 — `W1-05-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F063](RAW_FACTS.md#F063) [[S062](SOURCES.md#S062); code observation].** OpenCV FFmpeg backend при включённой конверсии выбирает BGR24, хотя property называется CONVERT_RGB; rotation properties и обработка PTS зависят от backend/версии. Следствие: проверять реальный результат цветовым fixture, логировать backend/build information и возвращённые значения properties. Этот факт не гарантирует поведение GStreamer, камеры или сервиса LinQ.

**S support:** [S062](SOURCES.md#S062). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F064"></a>
### F064 — `W1-05-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F064](RAW_FACTS.md#F064) [[S063](SOURCES.md#S063); API documentation].** PTS — время презентации в единицах time_base; frame имеет sample aspect ratio и display matrix metadata. Следствие: frame index/FPS нельзя считать универсальным источником времени VFR; decoded raster и display orientation — отдельные сущности. Для потока фиксировать источник/единицы timestamp, эпоху reconnect и missing timestamps. API-комментарий time_base предупреждает о контекстных ограничениях; нельзя предполагать заполненность каждого поля каждым декодером.

**S support:** [S063](SOURCES.md#S063). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F065"></a>
### F065 — `W1-05-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F065](RAW_FACTS.md#F065) [[S064](SOURCES.md#S064); documentation].** FFmpeg CLI autorotate включён по умолчанию; cfr fps_mode дублирует/удаляет кадры, passthrough передаёт timestamps, muxer может их дополнительно менять. Следствие: повторное ручное вращение после autorotate — проверяемая гипотеза; выгрузка с `-r` не является нейтральным способом заморозить sample IDs. Это свойства CLI, не автоматическое обещание всех libav consumers.

**S support:** [S064](SOURCES.md#S064). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F066"></a>
### F066 — `W1-05-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F066](RAW_FACTS.md#F066) [[S065](SOURCES.md#S065), 85–135; [S066](SOURCES.md#S066), 150–156; code observation].** TopdownAffine меняет bbox aspect ratio, использует center/scale/rotation и UDP/non-UDP warp, сохраняет input metadata. TopdownPoseEstimator восстанавливает предсказанные точки через input_size/input_scale/input_center. Следствие: для RTMPose нужен отдельный ledger каждого actor crop; YOLO scale_coords не заменяет этот путь. Не применять простую формулу восстановления вне условий выбранной test pipeline, особенно при произвольном вращении.

**S support:** [S065](SOURCES.md#S065), [S066](SOURCES.md#S066). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-05](_WORK/W1_05.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-06 — FP32/FP16/BF16: численные расхождения и метод выбора допусков — нормализованные наблюдения

<a id="F067"></a>
### F067 — `W1-06-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S067](SOURCES.md#S067): математически эквивалентные вычисления не обязаны совпадать побитно; CPU/GPU, разные версии и batch/slice могут различаться

Documentation. Не диагностировать любой FP32 diff как поломку экспорта; фиксировать batch и backend

**S support:** [S067](SOURCES.md#S067). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F068"></a>
### F068 — `W1-06-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S067](SOURCES.md#S067) §§TF32/GEMM: FP32-вход не исключает TF32; промежуточное накопление GEMM может частично сокращать точность и давать Inf

Documentation. Тип файла не описывает всё исполнение; записывать compute/accumulator policy

**S support:** [S067](SOURCES.md#S067). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F069"></a>
### F069 — `W1-06-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S068](SOURCES.md#S068): autocast выбирает dtype по операции; `.half()` модели не равно autocast. In-place, `out=` и явный `dtype=` имеют особые правила

Documentation. Проверять фактические типы узлов и границы; не переносить autocast policy в экспорт автоматически

**S support:** [S068](SOURCES.md#S068). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F070"></a>
### F070 — `W1-06-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S069](SOURCES.md#S069): одинаковые seeds не гарантируют CPU/GPU parity; отключение convolution benchmark и deterministic algorithms решают разные задачи

Documentation. Повторяемость проверять внутри каждого стека отдельно

**S support:** [S069](SOURCES.md#S069). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F071"></a>
### F071 — `W1-06-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S070](SOURCES.md#S070) `convert_np_to_float16`: перед `np.float16` константы клипуются с сохранением знака; defaults `min_positive_val=1e-7`, `max_finite_val=1e4`; ноль/NaN/±Inf сохраняются

Code observation, не исполненный тест. Это параметры конкретного конвертера, **не границы формата FP16 и не допуски качества**

**S support:** [S070](SOURCES.md#S070). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F072"></a>
### F072 — `W1-06-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S070](SOURCES.md#S070): преобразуются tensor float_data/raw_data; `keep_io_types` управляет Cast около интерфейса, `op_block_list`/`node_block_list` оставляют выбранные узлы FP32. Default list включает NMS, TopK, RoiAlign, Resize

Code observation. Внешний FP32-выход не доказывает FP32 внутри; default block list не гарантирует всех чувствительных узлов

**S support:** [S070](SOURCES.md#S070). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F073"></a>
### F073 — `W1-06-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S071](SOURCES.md#S071): auto mixed precision принимает `feed_dict`, `validate_fn`, `rtol`/`atol` и делит неуспешные кластеры

Documentation. Успех на предоставленном sample не равен независимому качеству. Примерные rtol/atol страницы не использовать как acceptance budget

**S support:** [S071](SOURCES.md#S071). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F074"></a>
### F074 — `W1-06-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S072](SOURCES.md#S072) Table 1: BF16 имеет существенно больший диапазон, чем FP16, но больший unit roundoff. Shifted softmax избегает overflow экспонент; математически эквивалентные формулы имеют разные ошибки

Теория документа, не измерение нашей модели. BF16 не универсально точнее FP16; безопасная формула не восстанавливает уже округлённые logits

**S support:** [S072](SOURCES.md#S072). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F075"></a>
### F075 — `W1-06-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S073](SOURCES.md#S073): `isclose(a,b)` использует `abs(a-b) <= atol + rtol*abs(b)` и несимметричен; default atol непригоден для некоторых малых величин

Documentation. Явно выбрать reference и единицы; около нуля выводить absolute error отдельно

**S support:** [S073](SOURCES.md#S073). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F076"></a>
### F076 — `W1-06-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S049](SOURCES.md#S049): при equal scores подходящий для NMS бокс может различаться CPU/GPU

Documentation. Отдельно фиксировать tie/order и retained IDs; совпадение score-распределений недостаточно

**S support:** [S049](SOURCES.md#S049). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F077"></a>
### F077 — `W1-06-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S074](SOURCES.md#S074): FP16 weights LiteRT на описанном CPU-пути повышаются до FP32 перед первым inference; I/O по умолчанию float

Documentation. Сжатое хранение весов не доказывает FP16 arithmetic; этот CPU-путь не доказывает GPU/LinQ fidelity

**S support:** [S074](SOURCES.md#S074). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F078"></a>
### F078 — `W1-06-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

CASE_NOTES.md, кейс с.5/7/13: мелкие СИЗ, ложные тревоги, оперативность и подавление дублей относятся к задаче; формула допустимой потери не дана

Вторичная передача первичного чтения root. Нужен событийный gate, не выдуманный регламент допустимой ошибки

**S support:** [S002](SOURCES.md#S002). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-06](_WORK/W1_06.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-07 — PTQ и калибровка: выбор по реализации и независимая проверка — нормализованные наблюдения

<a id="F079"></a>
### F079 — `W1-07-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F079](RAW_FACTS.md#F079) — документация, [S075](SOURCES.md#S075); Static/Dynamic Quantization, Debugging.** Static фиксирует activation scales по calibration inputs, dynamic вычисляет их при inference. Сопоставление intermediate tensors помогает локализации потери. Условия: ORT, конкретный supported graph/EP; не LinQ. Проверено чтением. Значение: разделить ошибку export и PTQ; одинаковый input сохранять до quantizer.

**S support:** [S075](SOURCES.md#S075). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F080"></a>
### F080 — `W1-07-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F080](RAW_FACTS.md#F080) — code observation, [S076](SOURCES.md#S076); local calibrate.py:154–158,297+,691+,725+,1173+.** Указаны три INT8-релевантных метода; factory percentile=99.999, symmetric=True; constructor/docstring расходятся по defaults. Distribution описан для float8; [S077](SOURCES.md#S077) имеет соответствующий guard. Проверено чтением, без исполнения. Значение: сохранять resolved calibration settings, не только CLI.

**S support:** [S076](SOURCES.md#S076), [S077](SOURCES.md#S077). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F081"></a>
### F081 — `W1-07-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F081](RAW_FACTS.md#F081) — code observation, [S077](SOURCES.md#S077); quantize_static signature/options.** QDQ, per_channel=False и MinMax — defaults этой функции; доступны W/A type, symmetry и node exclusions. Значение: per-channel нельзя предполагать по факту применения INT8; фактическую ось/scale проверять в графе. Реальный kernel/EP и допустимость на LinQ неизвестны.

**S support:** [S077](SOURCES.md#S077). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F082"></a>
### F082 — `W1-07-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F082](RAW_FACTS.md#F082) — документация, [S078](SOURCES.md#S078); Tune quantization parameters.** PERFORMANCE и MIXED различают symmetry; subset_size default=300, fast_bias_correction=False включает более точную коррекцию для OpenVINO/ONNX representations. Значение: число 300 — настройка инструмента; коррекцию держать отдельным фактором эксперимента. Факт улучшения именно нашей модели не проверен.

**S support:** [S078](SOURCES.md#S078). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F083"></a>
### F083 — `W1-07-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F083](RAW_FACTS.md#F083) — code observation, [S079](SOURCES.md#S079)/S06; перечисленные классы.** Range estimator разделяет per-sample statistic и cross-sample aggregation. AdvancedQuantizationParameters содержит раздельные activation/weight range settings. Значение: записывать единицу sample, batch и reduction axes; одно имя «minmax» не идентифицирует effective method. Доступность комбинации определяется backend constraints, она здесь не исполнена.

**S support:** [S079](SOURCES.md#S079), [S080](SOURCES.md#S080). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F084"></a>
### F084 — `W1-07-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F084](RAW_FACTS.md#F084) — документация, [S081](SOURCES.md#S081); Accuracy Control.** `validation_fn` и `validation_dataset` участвуют в выборе восстановления точности; `max_drop` может задаваться ABSOLUTE/RELATIVE; недостижимость ограничения приводит к ошибке. Пример использует один loader для calibration/validation. Значение: validation этой процедуры — tuning, не независимый финальный test. Default 0.01 не норматив кейса и требует определения шкалы метрики.

**S support:** [S081](SOURCES.md#S081). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F085"></a>
### F085 — `W1-07-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F085](RAW_FACTS.md#F085) — документация, [S082](SOURCES.md#S082); integer-only/fallback.** Representative inputs нужны для диапазонов intermediates; fallback может оставлять float operations. Integer-only example ограничивает `supported_ops` до `TFLITE_BUILTINS_INT8` и задаёт I/O dtype. Tutorial использует MNIST, take(100), допускает overlap с evaluation. Значение: это API-пример, не универсальное N и не основание нарушать наш независимый test.

**S support:** [S082](SOURCES.md#S082). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F086"></a>
### F086 — `W1-07-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F086](RAW_FACTS.md#F086) — code observation, [S084](SOURCES.md#S084)/S11; _feed_tensors/MinMax::Update.** Поддерживаются list, input-name dict и signature-key+dict; MinMax накапливает extrema, NaN предупреждает. Значение: проверить порядок/name/dtype всех inputs и отсутствие NaN/Inf до калибровки. Это исследованный путь TensorFlow 2.20.0, не доказательство единственного алгоритма всех LiteRT-путей.

**S support:** [S084](SOURCES.md#S084), [S085](SOURCES.md#S085). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F087"></a>
### F087 — `W1-07-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F087](RAW_FACTS.md#F087) — спецификация, [S083](SOURCES.md#S083); Conv/Depthwise.** Per-axis weight scales и per-tensor activations имеют operator-specific axes/zero-points; bias scale связан с input×weight. Значение: ошибки axis/dequantization способны выглядеть как плохая calibration; сравнивать реальную метаинформацию.

**S support:** [S083](SOURCES.md#S083). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 58.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F088"></a>
### F088 — `W1-07-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F088](RAW_FACTS.md#F088) — первичная авторская работа, [S086](SOURCES.md#S086); §§3.4,4.1–4.2, Appendix A.1.** Авторы рассматривают конфликт clipping/rounding, показывают зависимость метода от модели и чувствительность per-tensor weights после BN folding. Calibration бралась из training splits, Jasper — dev с отдельным test; объёмы различались по задаче. Здесь не переносим их численные accuracy/speed: hardware/runtime/checkpoint/input условия не воспроизведены. Значение: глобальный «лучший calibrator» и «достаточно N» из paper не следуют.

**S support:** [S086](SOURCES.md#S086). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 59.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F089"></a>
### F089 — `W1-07-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F089](RAW_FACTS.md#F089) — документация, [S075](SOURCES.md#S075) Int4/UInt4 и [S087](SOURCES.md#S087) introduction.** Weight-only имеет другой scope, чем W/A PTQ; ORT ограничивает blockwise INT4 конкретными constant-input ops, OpenVINO сохраняет float activations. Значение: полезный отдельный путь/контроль, но target support необходимо подтвердить отдельно.

**S support:** [S075](SOURCES.md#S075), [S087](SOURCES.md#S087). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 60.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F090"></a>
### F090 — `W1-07-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

- **[F090](RAW_FACTS.md#F090) — собственный методический вывод из [F079](RAW_FACTS.md#F079),[F082](RAW_FACTS.md#F082),[F084](RAW_FACTS.md#F084),[F085](RAW_FACTS.md#F085),[F088](RAW_FACTS.md#F088).** Калибровочные данные влияют на выбранную модель даже без labels. Использование test inputs для диапазонов делает оценку адаптированной к test distribution; многократный выбор percentile по test labels усиливает leakage. В нашей схеме calibration и tuning полностью отделены от sealed test по источникам видео. Это предлагаемый строгий протокол, не требование API.

**S support:** [S075](SOURCES.md#S075), [S076](SOURCES.md#S076), [S077](SOURCES.md#S077), [S078](SOURCES.md#S078), [S079](SOURCES.md#S079), [S080](SOURCES.md#S080), [S081](SOURCES.md#S081), [S082](SOURCES.md#S082), [S083](SOURCES.md#S083), [S084](SOURCES.md#S084), [S085](SOURCES.md#S085), [S086](SOURCES.md#S086), [S087](SOURCES.md#S087). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-07](_WORK/W1_07.md), строка 61.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-08 — восстановление качества после PTQ: коррекции, QAT и экспорт — нормализованные наблюдения

<a id="F091"></a>
### F091 — `W1-08-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F091](RAW_FACTS.md#F091) — QAT зависит от backend.** [Documentation; [S088](SOURCES.md#S088), backend Quantizer и Conclusion.] PT2E вставляет fake quantization и QAT fusion; после `convert_pt2e` требуется lowering. Пример XNNPACK не является экспортёром LinQ. Практически: выбирать quantizer после получения численного контракта целевой платформы. Общая обучаемость модели в PyTorch — отдельный вопрос от допустимости результата для компилятора.

**S support:** [S088](SOURCES.md#S088). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F092"></a>
### F092 — `W1-08-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F092](RAW_FACTS.md#F092) — состояние BN/observer требует контроля.** [Documentation; [S088](SOURCES.md#S088), Training Loop, note after capture.] Документ предлагает управление observer и BN statistics во время обучения; после capture обычные `train()/eval()` не являются корректным переключателем экспортированной модели. Практически: не копировать старый eager QAT loop в PT2E; сохранять конкретные режимы и проверять повторную загрузку checkpoint.

**S support:** [S088](SOURCES.md#S088). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F093"></a>
### F093 — `W1-08-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F093](RAW_FACTS.md#F093) — QAT и range learning имеют разные ресурсы.** [Documentation; [S089](SOURCES.md#S089), Variants, API/export.] AIMET описывает варианты с фиксированными и обучаемыми activation ranges; второй требует больше памяти. Экспорт может содержать обычную модель и отдельный JSON encodings, опционально ONNX; в API упомянут embedded fakequant export. ONNX QAT непосредственно в этом интерфейсе не поддержан. Практически: ONNX PTQ-инструмент не автоматически предоставляет градиенты для дообучения.

**S support:** [S089](SOURCES.md#S089). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F094"></a>
### F094 — `W1-08-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F094](RAW_FACTS.md#F094) — экспортируемый ONNX недостаточен без параметров.** [Documentation; [S090](SOURCES.md#S090), On-target inference.] AIMET документирует модель вместе с encodings min/max/scale/offset и конкретный Qualcomm importer. Практически: команда должна выяснить, принимает ли LinQ соответствующий второй артефакт либо эквивалентные QDQ. Документация Qualcomm не устанавливает LinQ-совместимость.

**S support:** [S090](SOURCES.md#S090). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F095"></a>
### F095 — `W1-08-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F095](RAW_FACTS.md#F095) — AdaRound оптимизирует rounding, не требует обычного end-to-end fine-tuning.** [Paper/method; [S091](SOURCES.md#S091) §3.3.] Локальная реконструкция обучает мягкое решение округлить вес вверх/вниз, затем делает его жёстким; используются неразмеченные примеры. В формуле присутствует заданный scale, поэтому смена сетки меняет решаемую задачу. Практически: разумный кандидат при подтверждённой чувствительности весов, но не обещание исправить clipping активаций.

**S support:** [S091](SOURCES.md#S091). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F096"></a>
### F096 — `W1-08-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F096](RAW_FACTS.md#F096) — AdaRound доступен как инструмент, а не только paper.** [Documentation; [S092](SOURCES.md#S092) notebook/guide.] AIMET 2.20.0 демонстрирует ONNX-путь с quantization simulation и AdaRound. Пример классификации ResNet18/ImageNet не является готовым рецептом detector/pose. Практически: проверить конкретную архитектуру и поддержку операторов, не считать notebook доказательством восстановления маленьких СИЗ.

**S support:** [S092](SOURCES.md#S092). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F097"></a>
### F097 — `W1-08-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F097](RAW_FACTS.md#F097) — BRECQ имеет существенные условия.** [Paper method/setup; [S093](SOURCES.md#S093) Appendix B.4.4.] В ImageNet-опыте: 1024 калибровочных изображения 224×224, batch 32, 20000 итераций на блок, BN folding/freeze. В detection: 256 изображений MS COCO; ResNet input 800/max1333, MobileNetV2 600/max1000. Block reconstruction применяется к backbone, прочие части реконструируются по слоям. Это условия статьи, не минимальные требования и не размеры нашей выборки.

**S support:** [S093](SOURCES.md#S093). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F098"></a>
### F098 — `W1-08-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F098](RAW_FACTS.md#F098) — original BRECQ не универсальный drop-in.** [Code observation; [S094](SOURCES.md#S094).] `quant/quant_model.py:15–43` оборачивает Conv2d/Linear и учитывает ReLU/ReLU6; `quant/quant_block.py:179+` содержит конкретные блоки ResNet/MobileNet/RegNet. `main_imagenet.py:155–156` задаёт 1024/20000 по умолчанию. `block_recon.py:10–14,82+` содержит CUDA и локальную оптимизацию. README отдельно предупреждает о специальном multi-GPU пути. Практически: DETR attention, RT-DETR decoder, RTMPose head, torchvision ROI operators или современный YOLO нельзя считать покрытыми по наличию Conv/Linear.

**S support:** [S094](SOURCES.md#S094). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F099"></a>
### F099 — `W1-08-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F099](RAW_FACTS.md#F099) — bias correction исправляет среднее, не всю ошибку.** [Paper method; [S095](SOURCES.md#S095) §4.2, Appendix D.] Оценивается средний сдвиг quantized-versus-float output и компенсируется bias. Аналитическая оценка использует BN и предположения о распределении/активации; эмпирическая — данные. Equalization опирается на scale-equivariance, поэтому перенос правила ReLU на SiLU/GELU требует отдельного обоснования. Практически: применять по диагнозу постоянного сдвига каналов, не ждать восстановления утраченных из-за clipping редких признаков.

**S support:** [S095](SOURCES.md#S095). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F100"></a>
### F100 — `W1-08-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F100](RAW_FACTS.md#F100) — bias correction реально есть в AIMET 2.20.0.** [Code observation; [S096](SOURCES.md#S096) `correct_bias`:243+, `disable_output_quantizers`:332–346.] API по умолчанию выбирает empirical correction, создаёт float reference copy, работает с Conv/Linear и отключает output activation quantizers при коррекции; в конце удаляет quant wrappers. Практически: этот конкретный путь не следует выдавать за общую коррекцию полного W8A8 runtime. Даже без labels dataloader в коде ожидает пару input/placeholder и свой `batch_size`.

**S support:** [S096](SOURCES.md#S096). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F101"></a>
### F101 — `W1-08-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F101](RAW_FACTS.md#F101) — ORT различает QDQ и QOperator.** [Documentation; [S075](SOURCES.md#S075) representations/method selection.] QAT-экспорт может содержать QDQ; такой граф не требуется снова прогонять через quantization tool. ORT здесь не предоставляет retraining; обучение происходит в исходном framework. Практически: повторный PTQ поверх готового QAT — отдельное преобразование с повторной валидацией, а не обязательный этап.

**S support:** [S075](SOURCES.md#S075). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F102"></a>
### F102 — `W1-08-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F102](RAW_FACTS.md#F102) — TFMOT служит полезным контрпримером «fake quant работает → backend работает».** [Documentation; [S097](SOURCES.md#S097) support matrix.] Документ ограничивает типы Keras-моделей и слоёв, а произвольное изменение bitwidth отделяет от поддерживаемого deployment path. Практически: TFLite QAT возможен для подходящей исходной TF-модели, но не обосновывает цепочку PyTorch→TF→TFLite→LinQ.

**S support:** [S097](SOURCES.md#S097). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 58.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F103"></a>
### F103 — `W1-08-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F103](RAW_FACTS.md#F103) — distillation увеличивает training-side требования.** [Documentation; [S098](SOURCES.md#S098) QAT/QAD.] NVIDIA описывает quantized student, frozen teacher и KL loss, сохранение PTQ-конфигурации; teacher добавляет compute/memory. Документ в основном про HF/Megatron/LLM, BF16 teacher и агрессивные форматы. Практически: это подтверждение доступного механизма, но не готовый QAD-рецепт промышленной CV и не основание выбирать BF16 для 3090.

**S support:** [S098](SOURCES.md#S098). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 60.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F104"></a>
### F104 — `W1-08-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F104](RAW_FACTS.md#F104) — опубликованную скорость BRECQ нельзя переводить в наши GPU-часы.** [Inference from [S093](SOURCES.md#S093) conditions and [S094](SOURCES.md#S094) implementation.] Статья и репозиторий исследуют другие модели, входы и окружение; часть latency-исследования Appendix B.4.3 использует simulator и ARM implementation. Поэтому рекламируемые paper speedup и низкая битность не доказывают ни ускорения LinQ, ни времени на RTX 3090. Численный прогноз в этой ветке не даётся.

**S support:** [S093](SOURCES.md#S093), [S094](SOURCES.md#S094). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 62.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F105"></a>
### F105 — `W1-08-F15`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F105](RAW_FACTS.md#F105) — контракт LinQ остаётся unknown.** [Unknown/local scope.] Ни документация общего framework, ни наличие `.onnx` не отвечают, сохраняет ли выданный компилятор trained scales, signedness, per-channel axis и границы quantize/dequantize. Ответ определяет полезность всей GPU-работы; закрывается SDK/примером экспорта и target test, а не ещё одной общей статьёй QAT.

**S support:** [S075](SOURCES.md#S075), [S088](SOURCES.md#S088), [S089](SOURCES.md#S089), [S090](SOURCES.md#S090), [S091](SOURCES.md#S091), [S092](SOURCES.md#S092), [S093](SOURCES.md#S093), [S094](SOURCES.md#S094), [S095](SOURCES.md#S095), [S096](SOURCES.md#S096), [S097](SOURCES.md#S097), [S098](SOURCES.md#S098). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-08](_WORK/W1_08.md), строка 64.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-09 — Mixed precision: адресное восстановление и ограниченные абляции — нормализованные наблюдения

<a id="F106"></a>
### F106 — `W1-09-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S099](SOURCES.md#S099) `quantize_static` имеет `nodes_to_quantize`, `nodes_to_exclude`, `op_types_to_quantize`. BaseQuantizer сначала проверяет allowlist/type, затем exclusion; exclusion возвращает False

Code observation. Реальная селекция по exact exported node.name; составить manifest имён после подготовки. Python module name до fusion недостаточен. Пустая allowlist в этом predicate не означает «квантовать ноль узлов»

**S support:** [S099](SOURCES.md#S099). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F107"></a>
### F107 — `W1-09-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S099](SOURCES.md#S099) L559–577: `OpTypesToExcludeOutputQuantization` выключает output quantization для op type, `DedicatedQDQPair` управляет общими/раздельными input QDQ

Code observation. Node exclusion, output exclusion и consumer-specific boundary — разные вмешательства. Не представлять любой из них как сохранение всей head в FP32

**S support:** [S099](SOURCES.md#S099). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F108"></a>
### F108 — `W1-09-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S100](SOURCES.md#S100) `compute_activation_error` L375+ отдельно считает `qdq_err` между pre/post QDQ и `xmodel_err` между float/post QDQ

Code observation. Помогает отделить локальное округление на границе от накопленного расхождения upstream. Сначала проверить, что tensors действительно соответствуют

**S support:** [S100](SOURCES.md#S100). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F109"></a>
### F109 — `W1-09-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S100](SOURCES.md#S100) L341–362: default error function возвращает SQNR = 20 log10(norm(reference)/norm(diff)), с epsilon floor

Code observation. Несмотря на имя `*_err`, большее значение лучше. Это не AP, не recall; concatenation/нормирование может скрыть редкий head/channel

**S support:** [S100](SOURCES.md#S100). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F110"></a>
### F110 — `W1-09-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S075](SOURCES.md#S075) §Debugging: graph optimization во время quantization мешает matching intermediate tensors; рекомендуется preprocessing отдельно

Documentation. Сравнивать один prepared FP graph со своими quantized descendants; большие diff по несопоставимым узлам недоказательны

**S support:** [S075](SOURCES.md#S075). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F111"></a>
### F111 — `W1-09-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S102](SOURCES.md#S102) L369–409: accuracy control работает с OpenVINO/ONNX backend, прочие dispatch заканчиваются UnsupportedBackendError; ignored_scope передается implementation

Code observation. Наличие обычного `quantize` для TensorFlow/PyTorch не распространяет accuracy-control API на них; нет поддержки LinQ в этом dispatch

**S support:** [S102](SOURCES.md#S102). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F112"></a>
### F112 — `W1-09-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S103](SOURCES.md#S103): ranker группирует quantizers, restoration жадно снимает группу, валидирует, допускает шаг назад и пересчёт ranking

Code observation. Это реальное снятие квантизаторов, не только sensitivity score. Не обещает глобального optimum и не гарантирует additive recovery

**S support:** [S103](SOURCES.md#S103). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F113"></a>
### F113 — `W1-09-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S103](SOURCES.md#S103) advanced parameters: `max_num_iterations`, `ranking_subset_size`, `tune_hyperparams=False`, `restore_mode`; ONLY_ACTIVATIONS сохраняет int8 weights для weighted operations

Code observation. Можно ограничить restoration budget. Бюджет iterations не равен числу всех inference: ranking и validation отдельно стоят времени. ONLY_ACTIVATIONS не равно полностью FP block

**S support:** [S103](SOURCES.md#S103). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F114"></a>
### F114 — `W1-09-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S081](SOURCES.md#S081): calibrated/validation datasets и пользовательская higher-is-better metric; `max_drop` absolute/relative; рекомендует `compress_to_fp16=False` при сохранении восстановленных FP32 операций

Documentation. Не копировать default 0.01 как норматив кейса. После save/load снова проверить выигрыш: сжатие весов до FP16 способно изменить восстановленный вариант

**S support:** [S081](SOURCES.md#S081). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F115"></a>
### F115 — `W1-09-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S071](SOURCES.md#S071) утверждает GPU requirement auto mixed precision; [S101](SOURCES.md#S101) L153–165 явно создаёт ORT sessions с CPUExecutionProvider и комментарием о проблеме CUDA для intermediate outputs

Неразрешённый docs/code mismatch разных артефактов. v1.16.0 не запускался; нельзя заявить ни успешный GPU путь, ни универсальную невозможность CPU FP16. Нужны exact installed package/version, ORT kernel support и smoke-test перед автоматическим поиском

**W2 refinement:** категорический GPU-only вывод не применять; provider-selectable model-path API и CPU casts уточнены в [F225](RAW_FACTS.md#F225), [F226](RAW_FACTS.md#F226), [F227](RAW_FACTS.md#F227), [F228](RAW_FACTS.md#F228), [F229](RAW_FACTS.md#F229).

**S support:** [S071](SOURCES.md#S071), [S101](SOURCES.md#S101). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F116"></a>
### F116 — `W1-09-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S101](SOURCES.md#S101): search делит неуспешные сегменты; validate_fn и allclose при заданном rtol применяются совместно; проверяется финальная модель

Code observation. Не считать заявленный в docstring minimum доказанным глобальным минимумом; один feed_dict — search fixture, не независимый test. Это FP32↔FP16 conversion, не INT8 selective PTQ

**S support:** [S101](SOURCES.md#S101). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F117"></a>
### F117 — `W1-09-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S104](SOURCES.md#S104): QDQ может двигаться/сливаться; лишние границы мешают fusion, а не все low-precision kernels доступны. QLinearConv/QLinearMatMul/ConvInteger/MatMulInteger не равны поддерживаемому QDQ import

Documentation. ONNX float Conv между QDQ может стать quantized compute; float storage dtype сам не доказывает FP computation. Подтверждать compiled graph и фактический device

**S support:** [S104](SOURCES.md#S104). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F118"></a>
### F118 — `W1-09-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S105](SOURCES.md#S105) Inspector при DETAILED показывает layer/tensor formats/precision/tactics; [S106](SOURCES.md#S106) runtime model содержит выбранные kernels/types/layouts

Documentation. Это конкретные наблюдаемые артефакты для известных backend. Их имена не становятся командами LinQ; даже такой report не гарантирует конкретный accumulator, если поле не раскрыто

**S support:** [S105](SOURCES.md#S105), [S106](SOURCES.md#S106). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F119"></a>
### F119 — `W1-09-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S107](SOURCES.md#S107) §§2.1–2.3: trace-weighted sensitivity учитывает спектр Hessian и quantization perturbation; Pareto выбирает precision среди кандидатов; теоретический вывод имеет условия локального минимума/PSD Hessian и специальной формы perturbation в базисе eigenvectors (Assumption 1, Eq.3)

Теория/авторский метод. Требует differentiable loss, исходного trainable model и разрешённых битностей; это более дорогая альтернатива, а не первый шаг при неизвестном compiler

**S support:** [S107](SOURCES.md#S107). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-09](_WORK/W1_09.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-10 — мелкие объекты, перекрытия, pose и чувствительные решения — нормализованные наблюдения

<a id="F120"></a>
### F120 — `W1-10-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S108](SOURCES.md#S108) §3: нарезка уменьшает последующий downsampling малых объектов; мелкий crop может не вместить крупный объект

Published method; не LinQ measurement

Для малых признаков логировать размер в исходнике, после resize и в crop; сравнить ROI/full frame как отдельные конфигурации

**S support:** [S108](SOURCES.md#S108). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F121"></a>
### F121 — `W1-10-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S108](SOURCES.md#S108) §4: overlap может ухудшать large AP; full-image pass полезен крупным объектам

Published observation на aerial data

Tiling нельзя вводить как бесплатное универсальное восстановление: проверить обрезанных людей, дубли и потерю контекста

**S support:** [S108](SOURCES.md#S108). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F122"></a>
### F122 — `W1-10-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S109](SOURCES.md#S109) `get_sliced_prediction`: default GREEDYNMM/IOS, full pass включён; цикл batch=1

Code observation, не benchmark

Статья с NMS и конкретная библиотечная конфигурация не тождественны; сохранить merge settings и весь бюджет кадра

**S support:** [S109](SOURCES.md#S109). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F123"></a>
### F123 — `W1-10-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S110](SOURCES.md#S110) Eq.1–2: subpixel offset в heatmap масштабируется в исходные координаты

Published mathematical method; coordinate discretisation

Указать пространство ошибки; 0.5 heatmap pixel и 0.5 source pixel — разные величины

**S support:** [S110](SOURCES.md#S110). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F124"></a>
### F124 — `W1-10-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S111](SOURCES.md#S111) Fig.1, §4.1: перекрытие провоцирует чужие суставы/дубли; Crowd Index опирается на принадлежность суставов

Published analysis; не industrial/quantization claim

Срез «два человека рядом» должен проверять owner wrists/objects, а не только число найденных людей

**S support:** [S111](SOURCES.md#S111). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F125"></a>
### F125 — `W1-10-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S112](SOURCES.md#S112) §2.1 разделяет blur/noise/digital/weather и severity; отдельные искажения выделены для validation

Published evaluation protocol

Различать естественные заводские условия и синтетические диагностические варианты; не подгонять параметры на final stress set

**S support:** [S112](SOURCES.md#S112). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F126"></a>
### F126 — `W1-10-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S113](SOURCES.md#S113) `setKpParams` и pose `summarize`: all/medium/large, нет готового small pose summary

Code observation

Добавить собственные tiny-person/short-limb срезы; не выдавать их за стандартный COCO small AP

**S support:** [S113](SOURCES.md#S113). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F127"></a>
### F127 — `W1-10-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S113](SOURCES.md#S113) `computeOks`: когда размеченные точки есть, выбирается `vg>0`, ошибка нормируется площадью и per-joint sigmas

Code observation; обычная COCO семантика требует сверки с нашим GT

v=1 annotated occluded и v=2 visible нужно анализировать раздельно; средний OKS не отражает каждый важный сустав

**S support:** [S113](SOURCES.md#S113). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F128"></a>
### F128 — `W1-10-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S114](SOURCES.md#S114): argmax используется в heatmap/SimCC; SimCC делится на split_ratio; score берётся как min максимумов двух осей

Code observation соответствующего codec

Проверить tie/argmax, scale, score convention; нельзя заменить confidence произвольным средним и считать decoder эквивалентным

**S support:** [S114](SOURCES.md#S114). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F129"></a>
### F129 — `W1-10-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S114](SOURCES.md#S114) `refine_keypoints_dark`: blur→clip→log→производные→обратный Hessian при ненулевом determinant

Code observation; не универсальная рекомендация decoder

Почти плоские/многопиковые heatmaps требуют диагностики; механическая замена codec может сама поменять baseline

**S support:** [S114](SOURCES.md#S114). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F130"></a>
### F130 — `W1-10-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S115](SOURCES.md#S115) COCO class list содержит cell phone, не содержит cigarette/safety harness

Code observation словаря, не проверка наших весов

До precision-абляций проверить реальные class_names/head; отсутствие нужного класса — отдельная причина отсутствия detections

**S support:** [S115](SOURCES.md#S115). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-10](_WORK/W1_10.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-11 — Сохранение трекинга и событий после переноса модели — нормализованные наблюдения

<a id="F131"></a>
### F131 — `W1-11-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

BYTE повторно связывает низкоуверенные детекции с треками, а не просто удаляет их; [S116](SOURCES.md#S116) §3

Авторский алгоритм, не наше измерение. Агрессивный detector confidence cutoff до трекера может удалить нужный recovery pool

**S support:** [S116](SOURCES.md#S116). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F132"></a>
### F132 — `W1-11-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S117](SOURCES.md#S117): `frame_id += 1`; `buffer_size=int(frame_rate/30*track_buffer)`; Kalman `dt=1`

Code observation. Число вызовов и физическое время различаются; VFR-aware поведение здесь не доказано

**S support:** [S117](SOURCES.md#S117). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F133"></a>
### F133 — `W1-11-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S117](SOURCES.md#S117): high `score>track_thresh`, low `score>0.1` и `<track_thresh`; новый трек требует `track_thresh+0.1`

Code observation. Drift confidence влияет на recovery и рождение ID по-разному. Ровно равный `track_thresh` score исключён из обоих пулов в этой реализации

**S support:** [S117](SOURCES.md#S117). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F134"></a>
### F134 — `W1-11-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S116](SOURCES.md#S116) Appendix D: восстановление бокса использует координаты до и после пропуска

Documentation/algorithm observation. Это офлайн-процедура с будущим наблюдением; не доказательство causal online recall

**S support:** [S116](SOURCES.md#S116). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F135"></a>
### F135 — `W1-11-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S118](SOURCES.md#S118) §3: motion/appearance/CMC; §4.4: нехватка фоновых keypoints в динамически плотных сценах может нарушать camera motion estimation

Авторское описание ограничения. BoT-SORT не гарантирует устойчивость к любому shake/толпе

**S support:** [S118](SOURCES.md#S118). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F136"></a>
### F136 — `W1-11-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S119](SOURCES.md#S119): при `with_reid` создаётся encoder и выполняется `encoder.inference(img,dets)`; GMC вызывается до matching. Счётчик/буфер/dt устроены аналогично [F132](RAW_FACTS.md#F132)

Code observation. Дополнительные ветви, входные изображения и веса должны быть в replay/provenance; ReID — дополнительный inference

**S support:** [S119](SOURCES.md#S119). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F137"></a>
### F137 — `W1-11-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S120](SOURCES.md#S120): PTS — время показа в единицах соответствующего time base; DTS — иной timestamp; best effort — оценка эвристиками в stream time base

Documentation/code comments. Восстановленную временную шкалу надо маркировать, не выдавать за исходный PTS

**S support:** [S120](SOURCES.md#S120). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F138"></a>
### F138 — `W1-11-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S121](SOURCES.md#S121): greedy IoU/OKS matching с прошлым списком, строгий порог, удаление сопоставленного кандидата; нет аргумента timestamp

Code observation. Keypoint/score/area drift может менять ID; этот helper не обеспечивает устойчивый long-gap pose tracking

**S support:** [S121](SOURCES.md#S121). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F139"></a>
### F139 — `W1-11-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S122](SOURCES.md#S122): predictions сортируются по score; tIoU сопоставление с GT в video, один GT блокируется после TP для данного порога; лишняя prediction получает FP

Code observation. Основа для проверки сегментов и дублей, но штатный matcher не проверяет actor и время доставки уведомления

**S support:** [S122](SOURCES.md#S122). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F140"></a>
### F140 — `W1-11-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S123](SOURCES.md#S123) вводит баланс detection/association/localization и их разложение

Авторское описание метрики. HOTA/DetA/AssA полезны для локализации ошибки; не заменяют event recall

**S support:** [S123](SOURCES.md#S123). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F141"></a>
### F141 — `W1-11-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S124](SOURCES.md#S124): ROI использует detector output; line crossing/direction требуют track ID/history; геометрическая точка — низ по центру бокса

Documentation. При проверке event parity надо закрепить anchor point, а не предполагать любой центр эквивалентным

**S support:** [S124](SOURCES.md#S124). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F142"></a>
### F142 — `W1-11-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S002](SOURCES.md#S002): один продолжающийся инцидент должен давать одно уведомление; окно нескольких секунд иллюстративно, общего опубликованного FPS/допуска нет

Внутрикомандное чтение кейса. Нельзя выдавать 1 FPS или произвольные секунды за официальный норматив

**S support:** [S002](SOURCES.md#S002). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-11](_WORK/W1_11.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-12 — Межплатформенный fidelity gate и парная оценка — нормализованные наблюдения

<a id="F143"></a>
### F143 — `W1-12-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F143](RAW_FACTS.md#F143) — CODE, [S125](SOURCES.md#S125) `collect_activations` L115–165.** Без явных опций выбираются `ORT_DISABLE_ALL` и `CPUExecutionProvider`; input reader используется для сбора augmented outputs. Этот debug CPU-path не доказывает выполнение production graph или TPU. Логировать provider/опции и отдельно проверять нетронутый целевой artifact.

**S support:** [S125](SOURCES.md#S125). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 33.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F144"></a>
### F144 — `W1-12-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F144](RAW_FACTS.md#F144) — DOC, [S075](SOURCES.md#S075) Quantization Debugging.** ORT предлагает сравнивать соответствующие веса/активации; graph optimization во время quantization затрудняет соответствие. Фиксировать graph до/после преобразования и первую наблюдаемую расходящуюся границу, не называть весь эффект «INT8 потерей».

**S support:** [S075](SOURCES.md#S075). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 35.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F145"></a>
### F145 — `W1-12-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F145](RAW_FACTS.md#F145) — CODE, [S126](SOURCES.md#S126) `Params/evaluateImg/accumulate`.** Bbox defaults: IoU .50:.05:.95, 101 recall points, maxDets 1/10/100; per-image matching score-ordered, aggregation pooled; без GT sentinel −1. Это не mean frame precision и не произвольный Hungarian. Pin evaluator/config; при bootstrap пересчитать pooled AP; для пустого класса отдельно показать FP/exposure.

**S support:** [S126](SOURCES.md#S126). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F146"></a>
### F146 — `W1-12-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F146](RAW_FACTS.md#F146) — CODE, [S126](SOURCES.md#S126) `computeOks/setKpParams`.** OKS использует GT area, visibility `v>0`, per-keypoint sigmas; стандартный профиль 17 точек. Согласовать skeleton, order, visibility, scale, sigmas для RTMPose/custom pose; произвольный skeleton не оценивать молча как COCO17.

**S support:** [S126](SOURCES.md#S126). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F147"></a>
### F147 — `W1-12-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F147](RAW_FACTS.md#F147) — DOC, [S049](SOURCES.md#S049) description.** Для одинаковых scores PyTorch не гарантирует одинаково выбранный overlapping box на CPU/GPU. Raw tensor parity и set matching нужны отдельно от сравнения индексов NMS; tie-case логировать. Это не оправдание missed critical event.

**S support:** [S049](SOURCES.md#S049). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F148"></a>
### F148 — `W1-12-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F148](RAW_FACTS.md#F148) — CODE, [S127](SOURCES.md#S127) `eval_sequence/_compute_final_fields`.** HOTA разделяет DetA/AssA; matching сочетает global association alignment и local similarity. Число/строки track IDs не доказывают tracking quality; нужен независимый GT continuity. HOTA не измеряет timely delivery.

**S support:** [S127](SOURCES.md#S127). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F149"></a>
### F149 — `W1-12-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F149](RAW_FACTS.md#F149) — DOC/CODE, [S128](SOURCES.md#S128) paired/Notes; [S129](SOURCES.md#S129) L214.** `paired=True` переиспользует индексы для массивов; BCa может дать NaN при вырождении. Индекс должен означать допустимый cluster, а не соседний кадр. NaN и undefined draws раскрывать; увеличение resamples не добавляет камер.

**S support:** [S128](SOURCES.md#S128), [S129](SOURCES.md#S129). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F150"></a>
### F150 — `W1-12-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F150](RAW_FACTS.md#F150) — PUB, [S130](SOURCES.md#S130) Introduction/VI.A/C.3.** Внутрикластерная корреляция способна занизить обычные standard errors; при few clusters асимптотика и некоторые bootstrap остаются ненадёжны; важны degenerate draws и чувствительность к clusters. Camera/site/episode dependence важнее числа frames. Wild regression bootstrap автоматически не переносится на AP/event matching.

**S support:** [S130](SOURCES.md#S130). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F151"></a>
### F151 — `W1-12-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F151](RAW_FACTS.md#F151) — DOC, [S131](SOURCES.md#S131) Advanced usages.** LiteRT различает local float/quant op comparison при общем предшествующем quantized input и whole-model verify разделённых моделей; доступны layer/model metrics. «Ошибка слоя» зависит от его входов; debug artifact не заменяет production. Internal APIs помечены нестабильными. Selective quantization может фрагментировать accelerator execution и увеличить transfers.

**S support:** [S131](SOURCES.md#S131). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F152"></a>
### F152 — `W1-12-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F152](RAW_FACTS.md#F152) — secondary local / UNKNOWN, [S002](SOURCES.md#S002).** Кейс требует LinQ и полезных уведомлений; универсального процента деградации нет. Device evidence в нашей ветке отсутствует. До связанного artifact/completion/device trace статус device=UNVERIFIED.

**S support:** [S002](SOURCES.md#S002). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-12](_WORK/W1_12.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-13 — LinQ: действительный путь модели, версии и доступ — нормализованные наблюдения

<a id="F153"></a>
### F153 — `W1-13-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) §2.1 с.5: Ubuntu20.04, i7-7700, RAM≥32GB, Python3.11; wheel обозначен generic `tpu_framework-py3-none-any.whl`, допускается числовой спецификатор версии

Это требования данного guide. Они не доказывают минимальность каждой аппаратной характеристики и не задают номер установленного wheel.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F154"></a>
### F154 — `W1-13-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) §3.1 и §3.3: TF GraphDef — вход quantizer; ONNX сначала проходит `onnx_to_tf`; `.qm` содержит внутреннее представление для compile

Не передавать arbitrary ONNX напрямую runtime. `.qm` не стандартный ONNX QDQ-файл.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F155"></a>
### F155 — `W1-13-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) §3.2 с.9: `compile_(hardware_parameters, network, parameters, slicing_scheme=None)` возвращает executable + tensor descriptions; hardware target можно получать `get_hw_params(tpu_type)`

Compile target должен совпасть с выданным устройством. Не выводить target из названия своей модели.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F156"></a>
### F156 — `W1-13-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) с.20–21: `.tpu` разделяет Framework и SDK; `Device.list_devices/open`, `load`, `program.inference`, `inference.sync`

Compile и runtime — разные этапы. Работа TF-эмуляции не доказывает TPU execution.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F157"></a>
### F157 — `W1-13-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) с.16,19: as_graph с explicit batch; quantized model batch-sensitive, пример фиксирует `(1,224,224,3)`

Нельзя отправлять произвольный batch/size только потому, что исходный ONNX динамический.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F158"></a>
### F158 — `W1-13-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation + code observation**, [S133](SOURCES.md#S133) с.10 и [S139](SOURCES.md#S139) L170–181: guide DEFAULT/STAGING; сторонний код O1/O5/DEFAULT

Эквивалентность O1↔DEFAULT или O5↔STAGING не установлена. STAGING документированно может порождать неверную программу/долго компилироваться; для новой сети guide рекомендует DEFAULT.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F159"></a>
### F159 — `W1-13-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation seam**, [S133](SOURCES.md#S133) с.7: signature as_graph platform `64x64_fpga`, prose default `128x128_asic`; с.11 converter заявляет tuple(Graph,mapping), с.19 пример присваивает результат одному graph-like объекту

Найдены расхождения **в извлечённом тексте**. Они могут включать документальную/экстракционную ошибку; не являются доказанными багами SDK. Сверять actual signature, return types и target.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F160"></a>
### F160 — `W1-13-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S138](SOURCES.md#S138) L18–21,62–72: opset13 default, batch1, imgsz640, dynamic/simplify включаются флагами, nms=False

Параметры конкретного exporter skeleton. Ни opset13, ни package onnx1.16 не являются общей матрицей LinQ support.

**S support:** [S138](SOURCES.md#S138). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F161"></a>
### F161 — `W1-13-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S139](SOURCES.md#S139) L98–111,225,245: graph input переписан в `(1,3,H,W)`; calibration NCHW; compile после `network.set_batch`, defaults batches1,8

Статический self-build route. Переписать input metadata не равно доказать согласованность всех shape-dependent узлов; нужен повторный parity test изменённого graph.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F162"></a>
### F162 — `W1-13-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S139](SOURCES.md#S139) L114–139: importer tpu_framework, fallback onnx_direct; try_simplify True→False→без аргумента; поддерживает tuple или graph return

Адаптация автора к версиям. Broad retries могут менять преобразование и скрывать первопричину. Фиксировать effective branch и первый traceback.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F163"></a>
### F163 — `W1-13-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S139](SOURCES.md#S139) L275–281: calibrate с percentile, при любом TypeError повтор без percentile; save(file_dir,file_name); L292 from_quantized_model распакован в пару

Отличается от guide quantize class method/save(file_path)/single Network. Точный релиз переходов неизвестен. Summary сохраняет requested настройки не полностью effective execution; особенно percentile нельзя считать доказанным по CLI.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F164"></a>
### F164 — `W1-13-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S139](SOURCES.md#S139) L218–224,255–272: выбирается первый ONNX output, затем один output_candidate

Этот skeleton не универсален для multi-output pose/segmentation/DETR. Все необходимые выходы должны войти в explicit contract.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F165"></a>
### F165 — `W1-13-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043) L206 против parser L47: обращение `args.output_tensอร์_name`, destination обычного `--output-tensor-name` иной

Вероятный AttributeError до Device.open при обычном parser path; мы его не запускали. Достаточная причина не называть скрипт готовым публично воспроизводимым successful example.

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F166"></a>
### F166 — `W1-13-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043) L109–112,209–220,273–282: настоящий pytpu device path и host torch/Ultralytics NMS

Наличие CPU NMS не доказывает host fallback нейросетевых слоёв. Свой adapter нужно проверять отдельно (W1-04).

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F167"></a>
### F167 — `W1-13-F15`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Author reported status**, [S140](SOURCES.md#S140) §§3,5: final detection использует готовый vendor TinyYOLO3; self-build segmentation O5 not finalized

Не выдавать наличие YOLOv8 build source за опубликованное доказательство successful TPU detection. Авторские статусы не наши measurements.

**S support:** [S140](SOURCES.md#S140). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F168"></a>
### F168 — `W1-13-F16`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation автора**, [S141](SOURCES.md#S141) vendor contract: `.tpu` tiny_yolo3 batch8, NHWC416×416×3, float32 0..1

Конкретный готовый файл имеет иной IO, чем self-build YOLOv8 NCHW640. Упаковка float IO не означает float вычисления всех слоёв. Файл здесь не предоставлен.

**S support:** [S141](SOURCES.md#S141). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 58.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F169"></a>
### F169 — `W1-13-F17`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Vendor reported benchmark**, [S137](SOURCES.md#S137) блок performance: Ubuntu24.04, i7-10700K, Runtime16.18.6, Framework2026.8.43; указаны HP/HPQ, batches, yolov8n_pose

Это контекст опубликованного benchmark; exact model hashes/exporter/opset/accuracy dataset и raw logs не установлены. Не наши версии, не proof custom weights, не event-quality measurement.

**S support:** [S137](SOURCES.md#S137). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 59.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F170"></a>
### F170 — `W1-13-F18`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Vendor access statement**, [S134](SOURCES.md#S134) ПО: download после регистрации и верификации; сайт предлагает demo access

Публичный guide не равен публичному SDK distributive. Не входили и не подавали заявку. Нельзя трактовать TLS EOF как auth denial.

**S support:** [S134](SOURCES.md#S134). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 60.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F171"></a>
### F171 — `W1-13-F19`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Primary historical package documentation**, [S143](SOURCES.md#S143)/S13 metadata/examples: 2021/2023 API использует другие классы/методы

Нельзя делать `pip install pytpu` как подтверждённый способ собрать Runtime16.18.6. Совместимость со свежими libtpu/driver/compiler не установлена.

**W2 refinement:** stale PyPI README не описание всего source15.0.24; [F203](RAW_FACTS.md#F203), [F204](RAW_FACTS.md#F204).

**S support:** [S143](SOURCES.md#S143), [S144](SOURCES.md#S144). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 61.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F172"></a>
### F172 — `W1-13-F20`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown**, targeted read [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S135](SOURCES.md#S135), [S136](SOURCES.md#S136), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S043](SOURCES.md#S043), [S140](SOURCES.md#S140), [S141](SOURCES.md#S141), [S142](SOURCES.md#S142), [S143](SOURCES.md#S143), [S144](SOURCES.md#S144): exact importer/operator matrix, supported ONNX IR/opsets, dynamic ranges/batch maxima, TF supported versions, custom op registration и auto CPU partitioning не установлены

Это точные вопросы поставщику, не доказанное отсутствие возможностей. Не переносить сюда TensorRT/ORT/OpenVINO APIs.

**S support:** [S043](SOURCES.md#S043), [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S135](SOURCES.md#S135), [S136](SOURCES.md#S136), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S140](SOURCES.md#S140), [S141](SOURCES.md#S141), [S142](SOURCES.md#S142), [S143](SOURCES.md#S143), [S144](SOURCES.md#S144). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-13](_WORK/W1_13.md), строка 62.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-14 — LinQ: effective calibration, выходы и численные границы — нормализованные наблюдения

<a id="F173"></a>
### F173 — `W1-14-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) §3.1 с.7–8: порог рассчитывается по calibration tensor, создаются SoftwareNetwork с quantization/rescale/quantized weights и HardwareNetwork как TF-модель операций TPU. `calibration_dict: Dict[str, ndarray]`. **Documentation**

Есть документированный data-dependent путь и численный reference stage. Не установлены текущие алгоритмы minmax/KL/MSE, granularity, signedness, rounding, accumulator, saturation, bias precision.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 35.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F174"></a>
### F174 — `W1-14-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Там же описание percentile относится к ограничению весовых коэффициентов, тогда как вся процедура использует calibration tensor. Default в сигнатуре 100.0. **Documentation + unknown scope**

Нет основания считать этот percentile аналогом activation histogram percentile ORT. Не доказана и ошибка документа: параметр может действовать лишь на веса. Формула, scope и denominator неизвестны.

**S support:** [S043](SOURCES.md#S043), [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S135](SOURCES.md#S135), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S145](SOURCES.md#S145), [S146](SOURCES.md#S146). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F175"></a>
### F175 — `W1-14-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S139](SOURCES.md#S139) L275–280: try calibrate с percentile → любой TypeError → calibrate без него → quantize(thresholds). L304–325 не сохраняют percentile/retry/thresholds/version. **Code observation**

Исключение может быть и внутри поддерживаемого вызова; повтор не доказывает отсутствие keyword. Первый вызов мог изменить состояние. Нужны fail-closed вызов и fresh model при новой попытке; requested/effective параметры раздельно.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F176"></a>
### F176 — `W1-14-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S139](SOURCES.md#S139) L38–95: sorted recursive file list, взять первые N; default N=500, chunk=128. Float32 memmap `(N,3,H,W)`, letterbox→BGR/RGB reversal→CHW→/255. Все данные передаются одним calibration_dict. **Code observation**

Chunk относится к подготовке memmap, не доказывает streaming SDK или ограничение RAM. Первые отсортированные файлы не являются репрезентативной выборкой. 500/128 — defaults скрипта, не нормативы производителя.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F177"></a>
### F177 — `W1-14-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.14–15: NHWC float32, два изображения ради простоты классификационного примера; [S139](SOURCES.md#S139) принудительно NCHW `(1,3,H,W)` и затем `set_batch` при compile. **Documentation/code**

Не смешивать NHWC guide с NCHW YOLO. Calibration sample axis N не равен compile batch B. Каждая реально используемая compiled batch/shape требует проверки собственного выхода.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F178"></a>
### F178 — `W1-14-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.16: rescale input перед quantized TF, rescale output обратно; с.17–21 TLM и TPU принимают user-format test input без такого ручного шага. **Documentation**

Rescale зависит от границы. Нельзя автоматически добавлять к device output преобразование из TF-reference примера. Дополнительный rescale уже user-format выхода способен изменить результат. Точный текущий FULL/RAW contract неизвестен.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F179"></a>
### F179 — `W1-14-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S145](SOURCES.md#S145) `sync` default FULL, `_run` передаёт mode native; входной адрес `POINTER(c_uint8)`, output byte buffer; `_get_inference` view по user_dtype/reshape user_shape. Отдельно RAW program определяется отсутствием user_dtype. **Historical code observation**

Указатель uint8 не означает INT8 numerical tensor. `view` — reinterpret bytes, не dequantization. RAW program и RAW ProcessingMode различны. Native arithmetic и placement PRE/POST этим Python-кодом не установлены; не переносить на текущую ABI.

**S support:** [S145](SOURCES.md#S145). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F180"></a>
### F180 — `W1-14-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S146](SOURCES.md#S146) helper берёт фиксированный `output_node_1`, `pos_scale`, `pos_shift`, возвращает scale×2^shift; dequantize возвращает data×scale. **Historical code observation**

Точная старая формула имеет узкую область. Нет fpga_data.pickle и dtype/shape проверки: это не доказательство per-channel/symmetric quantization нынешнего LinQ и не универсальное средство восстановить float output.

**S support:** [S146](SOURCES.md#S146). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F181"></a>
### F181 — `W1-14-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S043](SOURCES.md#S043) L176–183 normalizer принимает rank3, только channel dimension84/85; L206 читает `args.output_tensอร์_name`, parser объявляет output_tensor_name. **Code observation, original pinned source**

Для обычного decoded Detect nc1/2/3 получается 5/6/7 каналов: обе обычные ориентации с большим A отвергаются. При A=84/85 возможен ложный выбор оси. Unicode typo на обычном argparse Namespace ведёт к AttributeError до runtime path. Это дефекты примера, не SDK.

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F182"></a>
### F182 — `W1-14-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S043](SOURCES.md#S043) L164–173 выбирает preferred name, иначе единственный/первый rank≥3 ndarray; L272–279 NMS без explicit nc; L284–305 COCO80_TO_91. [S138](SOURCES.md#S138) export nms=False. **Code observation**

Нет общего custom/multi-output контракта. Исправить только shape недостаточно: нужна явная nc/class map и detection/proto/pose roles. В этом примере NMS host-side, но это не доказывает невозможность NMS в LinQ graph.

**S support:** [S043](SOURCES.md#S043), [S138](SOURCES.md#S138). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F183"></a>
### F183 — `W1-14-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.9–10 DEFAULT/STAGING и предупреждение о неверных программах/долгой compile в STAGING; [S139](SOURCES.md#S139) L169–181 default CLI O1, отдельные O1/O5 imports. **Documentation/code**

O1/O5 нельзя объявить эквивалентами DEFAULT/STAGING. Начать с подтверждённого preset, сохранить фактический объект/config, сравнивать одинаковый quantized parent при смене preset.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F184"></a>
### F184 — `W1-14-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Guide classmethod `QuantizedModel.quantize(...)`, `save(file_path)`, один результат `Network.from_quantized_model`; пример2026 `RegularModel.calibrate/quantize`, save(file_dir,file_name), tuple unpack. Guide as_graph в signature указывает 64x64_fpga, описание default —128x128_asic. **Documentation/code discrepancy**

Это конкретные version/document seams. Не собирать API из разных поколений. Номер wheel, matching docs/example и actual target platform необходимы. Не доказано, когда менялись API или ошибочна ли извлечённая сигнатура.

**S support:** [S043](SOURCES.md#S043), [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S135](SOURCES.md#S135), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S145](SOURCES.md#S145), [S146](SOURCES.md#S146). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F185"></a>
### F185 — `W1-14-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.18 проверяет ожидаемый top-1 class и печатает TOP16; не проверяет tensor-level allclose или AP/recall. [S137](SOURCES.md#S137) содержит версии только benchmark environment. **Documentation/vendor report scope**

Такой smoke check полезен, но не gate переноса custom detector/pose. Не объявлять Runtime16.18.6/Framework2026.8.43 полученной командой средой.

**S support:** [S133](SOURCES.md#S133), [S137](SOURCES.md#S137). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-14](_WORK/W1_14.md), строка 47.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W1-15 — Серверное видео, acceptance и доказательства LinQ — нормализованные наблюдения

<a id="F186"></a>
### F186 — `W1-15-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) с.20–21: `.tpu` разделяет Framework и SDK; `Device.list_devices`, `Device.open`, `device.load`, `program.inference`, затем `inference.sync(input_dict)` как blocking call

Есть документированный локальный hardware путь на tensors. Ни file transfer, ни video decoder, ни формат HTTP job из него не выводятся. Имена методов сверить с реально выданной версией

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F187"></a>
### F187 — `W1-15-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S133](SOURCES.md#S133) с.17–21: TLM `model_execute` и исполнение на TPU — разные стадии; аппаратный результат проверяется той же `_assert_output_dictionary`, что reference/quantized

TLM estimates execution time — симуляция, не measured TPU latency. Демонстрационный most-probable-class assert не является достаточной fidelity/GT проверкой детектора

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F188"></a>
### F188 — `W1-15-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043) `main`:209–220, `run_once`:109–112

Явно перечисляет устройства, открывает выбранное и грузит `.tpu`; `run_once` сначала вызывает `.run`, если атрибут есть, иначе `.sync`. Семантика `.run` в установленном SDK неизвестна; completion barrier нельзя выводить по имени. Не переносить guide `.sync` на ветку `.run` без подтверждения

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F189"></a>
### F189 — `W1-15-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043):239–266,281–310,319–340

`cv2.imread` failure → `continue`; no det → `continue`; `images=len(img_ids)` — запрос, не обработанное число. `predictions.json` имеет COCO image_id/category_id/bbox/score, без PTS, статуса пустого кадра или failed-job ledger. Нужен отдельный census, иначе failure похож на negative result

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 39.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F190"></a>
### F190 — `W1-15-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043):269–280,311–317,329–333

Timer окружает только `run_once`, NMS и обратная геометрия снаружи. При warmup boundary внутри batch в denominator берётся часть изображений, в time — весь batch. Итоговая цифра не end-to-end video FPS и не точный steady-state benchmark без уточнения warmup/batch accounting

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 40.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F191"></a>
### F191 — `W1-15-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043):206 против parser:47; `pick_output`:164–173; `normalize_prediction_shape`:176–183

`args.output_tensอร์_name` не совпадает с parser destination `output_tensor_name`: обычный main должен остановиться до открытия устройства; это статический вывод. Первый ndarray rank≥3 и C=84/85 — эвристики, не строгий output contract. Не запускать «как готовый пример» без исправления и проверки

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 41.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F192"></a>
### F192 — `W1-15-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043):226–230,251–252,270; [S147](SOURCES.md#S147) `letterbox`:19–38

В этом адаптере image decode/resize/pad/RGB conversion/layout/float32 scaling — host; input NCHW float32 `/255`, pad114, linear resize. Это конкретный adapter, не универсальный контракт LinQ; служба может требовать другой dtype/layout/scale

**S support:** [S043](SOURCES.md#S043), [S147](SOURCES.md#S147). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F193"></a>
### F193 — `W1-15-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code observation**, [S043](SOURCES.md#S043):273–305

NMS через host torch/Ultralytics, COCO80→91 mapping, inverse `(x−pad)/scale`, clipping, width/height≤1 отбрасываются. Для custom nc/pose/multihead перенос этого adapter некорректен без отдельного contract; подробные decoder доказательства в W1-04, повторное обучение этого не исправляет

**S support:** [S043](SOURCES.md#S043). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 43.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F194"></a>
### F194 — `W1-15-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S148](SOURCES.md#S148) Main options: `-show_format`, `-show_streams`, `-show_frames`, `-count_frames`, JSON writer; `-read_intervals` предупреждает о неточном seek

ffprobe позволяет обследовать media, но sample interval после seek не обязательно начинается ровно на заданном времени. Для frozen frame roster сохранять фактически декодированные timestamps/indices, не только requested interval

**S support:** [S148](SOURCES.md#S148). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 44.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F195"></a>
### F195 — `W1-15-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation**, [S149](SOURCES.md#S149) Load/run и Data I/O: providers имеют priority; CPU I/O является default, profiling включается SessionOptions

В ORT GPU provider в конфигурации не гарантирует каждый op на GPU; CPU ndarray не доказывает CPU neural inference. Для LinQ требуются его собственные execution evidence; ORT примеры не переносим

**S support:** [S149](SOURCES.md#S149). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 45.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F196"></a>
### F196 — `W1-15-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Local root observation**, CASE_NOTES с.5/7/8/13/19

Скорость нужна вместе с качеством/ложными/дублями/оперативностью; formulas/δ/FPS minima не заданы. Server access обещан, но interface неизвестен. Окончательные пределы — версия acceptance contract, а не выдуманные «допустимые 1%»

**S support:** [S002](SOURCES.md#S002). Полный source locator/version/provenance — в карточках S и в исходной записи [W1-15](_WORK/W1_15.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-01 — K001: версии и интерфейсы LinQ после адресной перепроверки — нормализованные наблюдения

<a id="F197"></a>
### F197 — `W2-01-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.5 против [S134](SOURCES.md#S134) section ПО; [S150](SOURCES.md#S150)/S05 metadata

**Documentation:** guide2025 требует3.11; сайт пишет3.8. **Code/metadata:** pytpu15.0.24 объявляет>=3.6; setup.py включает numpy без exact pin. Прочитано, не импортировано.

Это разные области: Framework requirements, живая продуктовая страница, runtime packaging. Нельзя назвать их двумя установленными несовместимыми SDK. Поддержка Python3.11 всех native компонентов не доказана. Q01.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S150](SOURCES.md#S150), [S151](SOURCES.md#S151). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 29.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F198"></a>
### F198 — `W2-01-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) титул, с.4 §1.2.1

**Documentation:** код изделия оканчивается-03; текст сам сравнивает его с предыдущей редакцией-02.

Это реальная документированная линия редакций, но нет mapping-03→номер wheel→release date→API diff. «2025» не exact package version. Запросить mapping в Q01.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 30.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F199"></a>
### F199 — `W2-01-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.7–8 и пример с.19; [S139](SOURCES.md#S139) L274–280

**Documentation:** guide показывает `QuantizedModel.quantize` с calibration_dict. **Code:** сторонний пример создаёт RegularModel, отдельно calibrate и quantize; TypeError переводит calibrate на вызов без percentile.

Доказаны разные тексты вызовов, не удаление старого API или дата миграции. Возможны совместно поддержанные фасады; нет исходников/сигнатур exact Framework, чтобы выбрать. Не смешивать recipes, не считать retry проверкой поддержки percentile. Q02.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 31.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F200"></a>
### F200 — `W2-01-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.8–9 save, с.20 пример; [S139](SOURCES.md#S139) L281,L292

**Documentation:** guide save с file_path, пример присваивает Network одному имени. **Code:** сторонний save с file_dir/file_name, from_quantized_model распакован в два результата.

Из присваивания одному имени нельзя доказать Python return type: оно допустимо и для tuple. Но последующее использование Network должно быть объяснено. Нет сигнатуры реализации ни одной Framework версии; нельзя объявить tuple breaking change по примеру. Q03 просит exact return schema и migration.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 32.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F201"></a>
### F201 — `W2-01-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.7 as_graph, с.9 get_hw_params, с.19 target; [S139](SOURCES.md#S139) L285,L294–299

**Documentation extraction:** signature as_graph содержит64x64_fpga, prose default128x128_asic; guide compile example и сторонний code явно используют TPU_128x128_PARAMS. В [S139](SOURCES.md#S139) as_graph target не передан.

Target quantized reference и target compiler — отдельные места настройки; explicit compile constant не исправляет default as_graph. Ошибка extraction против ошибки оригинала не различена без PDF bytes. Не выбирать default по удобному фрагменту. Q04.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 33.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F202"></a>
### F202 — `W2-01-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133) с.9–10; [S139](SOURCES.md#S139) L169–181

**Documentation:** guide описывает DEFAULT/STAGING и риск STAGING. **Code:** пример отдельно импортирует DEFAULT из tpu_framework и O1/O5 из tpu_compiler.compiler.

Раздельные imports не задают equivalence или отличие значений; alias возможен. Ни O1=DEFAULT, ни O5=STAGING не доказаны. Exact resolved config+vendor-supported baseline запросить Q05.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 34.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F203"></a>
### F203 — `W2-01-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S150](SOURCES.md#S150) latest15.0.24; [S151](SOURCES.md#S151) `_bindings.py` L180–253,L307,L332–387

**Code, fresh archive:** имеются Device.list_devices/open/load, Program.inference, Inference.sync; это стиль runtime guide2025. [S151](SOURCES.md#S151) PKG-INFO long_description показывает старый пример iva_tpu/TPUDevice.

**Уточняет [F171](RAW_FACTS.md#F171):** старая документация PyPI не доказывает, что весь pytpu использует только старые классы. Прочитанный source15.0.24 не подтверждает связь Framework2025/2026, neural precision или native compatibility.

**S support:** [S150](SOURCES.md#S150), [S151](SOURCES.md#S151). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 35.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F204"></a>
### F204 — `W2-01-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S151](SOURCES.md#S151) `_bindings.py` L28,L34–51; setup.py install_requires/python_requires

**Code:** библиотека `/usr/lib/libtpu.2.so` загружается лениво через CDLL; setup metadata не закрепляет native driver/runtime version. Source inspection, не native load.

Даже import Python пакета не обязательно проверяет наличие/ABI native library. Номер pytpu и `python_requires` недостаточны для допуска. В Q01 обязательны native build/hash и known-good load/infer.

**S support:** [S151](SOURCES.md#S151). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F205"></a>
### F205 — `W2-01-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[S133](SOURCES.md#S133), [S136](SOURCES.md#S136), [S134](SOURCES.md#S134), [S150](SOURCES.md#S150), [S151](SOURCES.md#S151), [S152](SOURCES.md#S152), [S139](SOURCES.md#S139) + access.json

**Local observation/unknown:** exact Framework distributive, release migration, совместимый compiler/runtime/driver и golden artifact не получены. Каталог [S136](SOURCES.md#S136) снова ссылается на тот же guide.

Нет основания объявлять совместимость или несовместимость. Для нашего сервера состояние UNKNOWN; дальнейший широкий web search прекращён. Следующий шаг ARTIFACT+TEST.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S136](SOURCES.md#S136), [S139](SOURCES.md#S139), [S150](SOURCES.md#S150), [S151](SOURCES.md#S151), [S152](SOURCES.md#S152). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-01](_WORK/W2_01.md), строка 37.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-02 — один Detect/Pose contract и незакрытая граница ONNX→TF — нормализованные наблюдения

<a id="F206"></a>
### F206 — `W2-02-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F206](RAW_FACTS.md#F206) — preparation→ONNX, тип code observation; [S018](SOURCES.md#S018)/S03/S09

Для иллюстрации выбран fixed static FP32 input `images`, shape **[1,3,640,640]**, RGB unit float. Предлагаемые параметры: `format="onnx", imgsz=(640,640), batch=1, dynamic=False, half=False, nms=False, simplify=False`; **opset задаётся явно после подтверждения importer**, не как «универсальный LinQ opset». Номер opset13 в стороннем export script не является подтверждением compatibility этого контракта.

Exporter делает deepcopy→to(device)→requires_grad=False→eval→float→fuse, выставляет каждому Detect/Pose `export=True`, `dynamic=False`, `format="onnx"`, `xyxy=False`; C2f меняет forward на forward_split. Обычный fuse сворачивает Conv+BN через `fuse_conv_and_bn` и заменяет forward на fused; это отдельная граница сравнения ordinary eager→prepared eager. Затем два dry runs на zero tensor. При nms=False `NMSModel` не оборачивает модель. `torch2onnx` вызывает legacy `torch.onnx.export`, с `dynamo=False` для torch>=2.4, constant folding=True, input_names=[images].

Export_onnx задаёт один `output0` для обоих task; два выхода указаны только для segment. `simplify=False` исключает именно onnxslim pass, а не folding/BN fusion/C2f rewrite. Exporter также ограничивает `ir_version` до10, если header выше: сохранить именно фактические bytes и IR после этой операции. Ограничение: source reading не доказывает parity fusion или export. Решение: golden boundary ordinary eager→prepared eager→ONNX, на одном готовом tensor pack; не смешивать проблему подготовки с quantization.

**S support:** [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S157](SOURCES.md#S157). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F207"></a>
### F207 — `W2-02-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F207](RAW_FACTS.md#F207) — input/preprocess, тип code observation + proposal; [S153](SOURCES.md#S153)/S05

Канонический исходник здесь — трёхканальный HWC uint8 BGR ndarray после отдельно зафиксированного decoder. Выбран **явный** LetterBox `(640,640), auto=False, scale_fill=False, scaleup=True, center=True, stride=32, padding_value=114, interpolation=cv2.INTER_LINEAR`. Далее stack BHWC→BGR/RGB swap→BCHW transpose→contiguous→FP32→`/255`. Граф начинается с такого тензора; image decoding/letterbox/channel swap не надо автоматически считать встроенными в ONNX. Переданный готовый torch tensor в BasePredictor обходит pre_transform/channel conversion и `/255`; значения и оси должен обеспечить вызывающий код.

Растровая геометрия: `r=min(Htarget/Hsrc,Wtarget/Wsrc)`; resized `(round(Wsrc*r),round(Hsrc*r))`; centered pad делится пополам; sides `round(d−0.1),round(d+0.1)`. Хранить actual resized W/H, sides, r и canonical frame ID. Для сравнения backends использовать один подготовленный FP32 tensor, затем отдельно проверять полную image pipeline.

**Существенное условие wrapper:** native `pre_transform` в v8.3.230 включает auto только при `same_shapes && args.rect && (model.pt || (model.dynamic && !model.imx))`. `Model.predict` по умолчанию добавляет `rect=True`, несмотря на `default.yaml rect=False`; caller overrides могут заменить его. Для данного worked contract задать rect=False либо пользоваться одним frozen preprocessing. Нельзя сравнивать default .pt predict с static ONNX predict только по одинаковому imgsz640.

Внешние зависимости явно отделены: cv2.resize/copyMakeBorder — OpenCV; ndarray/stack/rounding — NumPy/Python; tensor ops и export — PyTorch/ONNX; возможный torchvision NMS — Torchvision. Их установленная exact version, builds/device и lock **UNKNOWN**. Все внутренние Ultralytics helpers закреплены одним commit; битовое равенство между незакреплёнными external builds не заявлено.

**S support:** [S153](SOURCES.md#S153), [S154](SOURCES.md#S154). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F208"></a>
### F208 — `W2-02-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F208](RAW_FACTS.md#F208) — decoded output, тип code observation; [S019](SOURCES.md#S019)/S09/S10

Для обычного non-end2end head: flatten каждого уровня в `[B,no,H_i*W_i]`, concatenate по candidate axis в порядке уровней; anchors из meshgrid(y,x), offset0.5, row-major внутри уровня. DFL: softmax по16 bins и ожидание bin index, затем dist2bbox и multiplication на stride. Detect default `xyxy=False` означает **cx,cy,w,h в пикселях model-input**, затем **nc independent sigmoid probabilities**. Отдельного objectness нет.

| Task/условие | Единственный ONNX tensor | Смысл каналов, без NMS |
|---|---|---|
| Detect | `output0`: `[B,4+nc,A]` | 0:4 cxcywh;4:4+nc class probabilities |
| Pose | `output0`: `[B,4+nc+K*D,A]` | те же box/classes; остаток reshape `[B,K,D,A]` в порядке keypoint identity из manifest |

Pose export вычисляет xy `(raw_xy*2 + anchor−0.5)*stride`; при D3 третий компонент проходит sigmoid, это confidence/visibility score, не depth и не categorical GT visibility label. При D2 третьего компонента нет. Box и keypoints одного candidate должны сохраняться вместе через любую фильтрацию.

Для **конкретных** P3/8–P5/32 configs при640×640 `A=80²+40²+20²=8400` (аналитический shape result): Detect nc1/2/3 даёт [1,5/6/7,8400]; Pose K17,D3 даёт [1,56/57/58,8400]. Для другого input/architecture A берётся по actual graph;8400 не универсальная константа. Например640×384 при тех же strides даёт80×48+40×24+20×12=5040. Nc/role/kpt_shape не угадываются по этим числам. Ограничение: это семантика прочитанного head, не actual model metadata. Решение: отвергать неожиданный output count/layout/channel count до decoder, не повторять decode или sigmoid.

**S support:** [S019](SOURCES.md#S019), [S157](SOURCES.md#S157), [S158](SOURCES.md#S158). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F209"></a>
### F209 — `W2-02-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F209](RAW_FACTS.md#F209) — один общий NMS, тип code observation + proposal; [S045](SOURCES.md#S045)/S08

Один и тот же host postprocessor получает **BCN**, явный `nc=manifest.nc`, `end2end=False`, `rotated=False`, объявленные confidence/IoU thresholds, classes filter, agnostic/multi_label/max_det/max_nms/max_wh и выбранный NMS implementation. Threshold values решает команда; source defaults .25/.45 не quality budgets кейса. Для исходного predictor multi_label=False; нельзя молча заменить его True только на TPU ветке.

v8.3.230 NMS сначала проверяет `prediction.shape[-1]==6 or end2end` и тогда принимает BNC final detections. На правильном BCN для данного640 head последняя ось8400, поэтому Detect nc2 **не** попадает в shortcut. Ошибочный transpose `[1,8400,6]` попадает; в этом случае даже `nc=2,end2end=False` shortcut **не отключают**. Нужна проверка schema до вызова; не «ремонтировать» runtime угадыванием по шести каналам. Редкий actual A=6 также сталкивается с shortcut, поэтому общий adapter обязан сверять этот инвариант/использовать явно проверенный path.

Далее NMS выводит class axis из nc, считает extra=C−4−nc (Pose K*D), применяет strict score `>conf`, BCN→BNC, cxcywh→xyxy, best-class либо объявленный multi-label, class filter, confidence cap30000 по default и class offset max_wh7680 по default. Выбранный candidate сохраняет весь extra tail. Выход на кадр `[N,6+extra]`: xyxy,confidence,class,extras. Важно: NMS изменяет coordinate view **in-place**; сохранить raw dump/использовать независимую копию до сравнения или повторного вызова.

Новая версия выбирает `torchvision.ops.nms`, если torchvision уже есть в sys.modules, иначе TorchNMS.nms. Для второго площадь без+1 и keep при IoU<=threshold; exact tie order зависит от sort/runtime. Поэтому «тот же Ultralytics commit» ещё не гарантирует одну NMS ветвь. Решение: общий явный postprocessor плюс записанный backend/dependency lock, synthetic tie/threshold/crowd fixtures; при time-limit warning не считать необработанные элементы batch валидными пустыми кадрами. Вызов native DetectionPredictor использует nc=0 для detect (вывод из channel count) и len(names) для Pose; в нашем admission adapter явный nc обязателен для обоих, как проверка manifest. Обычный Detect без extras эквивалентен этому native inference при согласованном schema.

**S support:** [S045](SOURCES.md#S045), [S156](SOURCES.md#S156). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 69.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F210"></a>
### F210 — `W2-02-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F210](RAW_FACTS.md#F210) — inverse и Results, тип code observation; [S155](SOURCES.md#S155)/S08/S11

После NMS boxes уже xyxy. Native Detect.construct_result вызывает scale_boxes с img.shape[2:],orig_img.shape; Pose наследует этот шаг, потом view extras в `[N,K,D]` и вызывает scale_coords. Для centered letterbox и ratio_pad=None:

- boxes: gain=min(Hin/Hsrc,Win/Wsrc), `pad_x/y=round((input_dim−source_dim*gain)/2−0.1)`, вычесть pads, разделить на gain, clip x к[0,Wsrc],y к[0,Hsrc]; **без .round()** результата;
- keypoint xy: тот же gain, но pad=(input_dim−source_dim*gain)/2 **без округления**, subtract/divide/clip; confidence геометрия не меняет;
- Results.Keypoints в этом commit хранит эти координаты, `xy` возвращает data[..., :2]; low confidence само по себе **не вызывает zeroing** в исполняемом коде. Docstrings про masking/<.5 этому коду не соответствуют.

Для G01 source853×481→640×640 `r=640/853`, box pad_y139, point pad_y≈139.55451348. Для fabricated input-space y200 box inverse81.3015625, point inverse80.5625; разница .7390625 source pixel. Это аналитика кода, не ошибка модели. Старый Pose дополнительно округлил бы box y до81. Эта асимметрия **сохраняется**; заменить обе формулы на свой общий geometric inverse можно лишь отдельным versioned policy change, одинаковым для всех ветвей.

Ограничение: такой inverse не покрывает arbitrary crop, stretch, rotations или top-down pose. Ledger должен хранить actual frame space; downstream tracker/rules получают float canonical coordinates и отдельно объявленную visibility policy. Трекер/события сюда не добавлены: W1-11 source не становится частью данного Ultralytics contract по совпадению названия ByteTrack/BoT-SORT.

**S support:** [S155](SOURCES.md#S155), [S156](SOURCES.md#S156), [S159](SOURCES.md#S159). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 79.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F211"></a>
### F211 — `W2-02-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F211](RAW_FACTS.md#F211) — G01–G04: что сохранить, что перевыпустить

Тип: source comparison + analytic expected, **NOT_RUN**. Старый primary commit `6e43d1e1e5db72afbf686dee6745669bcb124b0a` (W1-05), новый `389b87…93db`; [S153](SOURCES.md#S153)/S05/S07/S08/S11. Оба исходных тела функций просмотрены, AST использован только для текстового diff, не импортировался Ultralytics.

| Fixture | Expected в v8.3.230 | Delta и практическое действие |
|---|---|---|
| G01 landscape853×481, fixed auto=False RGB3 | resize640×361, pads L/T/R/B=0/139/0/140;640²; RGB red/255=[1,0,0];114/255≈.4470588 | **Сохранить** image geometry/norm expected. Новые padding_value/interpolation defaults не меняют выбранный профиль. Image labels path отличается: ratio_pad и label update теперь получают integer left/top вместо fractional dw/dh; если fixture включает annotations, expected надо отдельно обновить. |
| G02 portrait481×853 | resize361×640,139/0/140/0 | **Сохранить** image-only expected. Та же граница для label path. |
| G03 auto=True explicit LetterBox,stride32 |640×384,pads0/11/0/12 | Арифметика **сохранена**. Но wrapper matrix **перевыпустить**: same_shapes+rect=True+.pt→auto; same_shapes+rect=True+dynamic non-IMX non-.pt→тоже auto; rect=False→нет auto; static non-.pt→нет auto; mixed-shape→нет auto. Старая формулировка «только .pt» устарела. |
| G04 fractional/boundary boxes,keypoints,visibility0 | Clip boundary box[−3,−2,855,483] в source space к[0,0,853,481] сохраняется; default box/point fractional pad difference сохраняется; no confidence rescaling | **Перевыпустить** Pose box expected без .round(); low-conf Results expected сохраняет xy вместо zero; confidence0 остаётся0. Raw output/inverse и Results construction проверять отдельными assertions. Degenerate/tie policy не выводить из этого fixture. |

Уточнение `scale_boxes`: для используемого xyxy path арифметика сохраняется, но новая версия при `xywh=True` возвращает boxes без clip; не переносить этот delta в наш xyxy expected. LetterBox `scaleFill` переименован в `scale_fill`, появились configurable padding_value/interpolation и multispectral handling; для RGB3 image-only G01–G04 это не меняет выбранную геометрию. Pixel bit equality требует тех же внешних OpenCV/NumPy builds.

**S support:** [S153](SOURCES.md#S153), [S154](SOURCES.md#S154), [S155](SOURCES.md#S155), [S156](SOURCES.md#S156), [S159](SOURCES.md#S159). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 91.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F212"></a>
### F212 — `W2-02-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F212](RAW_FACTS.md#F212) — идентичность importer: что найдено и что осталось UNKNOWN

Тип: documentation / code observation / unknown с ограниченным поиском; [S133](SOURCES.md#S133)/S13/S16.

**Первичное документированное имя:** guide2025 §3.4 с.11 прямо указывает `from onnx_direct import onnx_to_tf`. §3.3 обещает tuple(tf.Graph, rename dictionary). Но собственный пример на с.19 присваивает return одному `original_graph_def` и далее передаёт его как graph. Это наблюдаемый doc/example seam, не доказанная ошибка фактического SDK. В guide нет достаточного определения direction dictionary по ONNX Value name/Node name, сохранения output ports, NCHW/NHWC transformations, shape inference, graph pruning/cut и accepted operators/attributes для нашего head.

**Сторонний pinned build:** сначала пробует `from tpu_framework import onnx_to_tf`, при любом Exception — `from onnx_direct import onnx_to_tf`; затем conversion kwargs try_simplify=True→False→без kwargs. Tuple интерпретируется как graph и optional dict; fallback {}. Mapping применяется `mapping.get(name,name)`, то есть предполагается ONNX→TF direction и value-name keys. Затем `RegularModel` получает input_shapes[NCHW], output_nodes и optional anchors_mapping. Это assumptions автора adapter, не опубликованный контракт mapping конкретного поставщика.

**Что новый адресный поиск проверил:** свежий pinned build получен и совпал по SHA с W1; official tech content открыт, но importer details там нет. Запросы точных `"onnx_direct" "onnx_to_tf"`, `"tpu_framework" "onnx_to_tf"` и PyPI+GitHub/LinQ qualifiers не дали пригодного первичного importer source/release metadata. Встреченный unrelated LocalAI engine с именем onnx_direct исключён. PyPI JSON endpoints `onnx-direct` и `tpu-framework` вернули404 2026-10-23 (имена нормализуются дефис/underscore). Это отсутствие public distribution **под этими именами в этой проверке**, не доказательство отсутствия модуля/закрытого wheel или функции. REST GitHub rate-limit и PDF TLS EOF записаны отдельно; не выданы за auth denial.

**Итог identity:** module import path известен документально; владелец actual installed callable, wheel/distribution, version/build/hash, module `__file__`, callable `__module__`, aliases/reexports и dependency versions **UNKNOWN**. Нет основания отождествить его с ONNX-TensorFlow/onnx-tf или PINTO0309/onnx2tf. Ultralytics собственный TF export использует onnx2tf; это **другая ветвь**, не замена LinQ importer. Решение: не тратить GPU на recovery до importer admission; запросить именно module/distribution mapping supplied bundle, а не установить найденный одноимённый converter.

**S support:** [S133](SOURCES.md#S133), [S135](SOURCES.md#S135), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 104.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F213"></a>
### F213 — `W2-02-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F213](RAW_FACTS.md#F213) — graph surgery и tensor/port admission

Тип: code observation + proposal; [S133](SOURCES.md#S133), [S139](SOURCES.md#S139), [S160](SOURCES.md#S160), [S161](SOURCES.md#S161). **Фактического semantic mapping для нашего graph нет**, потому что graph/SDK не предоставлены. Следующая таблица — обязательные поля admission, не выдуманные заполненные TF/QM names.

| Role | ONNX side после подтверждённого static export | TF side, заполняется из actual importer | QM/TPU side, заполняется из actual descriptors |
|---|---|---|---|
| Input model RGB tensor | graph.input `images`, FLOAT,[1,3,640,640],NCHW; producer=external graph input, output-port=N/A | exact tensor name **с port**, producing op+output index, shape,dtype; actual layout; rename/transpose record; соответствующий feed key | user/raw name+index,shape/layout,dtype,byte size, batch axis; numeric conversion/PRE owner и параметры; связь с TF input |
| Detect decoded candidates | graph.output `output0`; graph-output ordinal0; producer node and its output index из actual NodeProto; FLOAT,[1,4+nc,8400],BCN | **UNKNOWN name/port/shape/layout**; role должен остаться decoded cxcywh+class probabilities; список inserted Transpose/Reshape/Cast и output boundary | **UNKNOWN descriptor**; output order/role, user/raw scale/zero-point/packing; обратно привести к declared BCN без повторного decode |
| Pose decoded candidates+keypoints | graph.output `output0`, ordinal0; actual producer+port; FLOAT,[1,4+nc+K*D,8400],BCN | **UNKNOWN**; class channels и point identity/flatten order должны сохраниться; tail не отдельный aux выход | **UNKNOWN**; все K*D значения того же candidate доступны в declared format; нельзя молча обрезать до4+nc |
| Любой дополнительный actual output | зафиксировать **все** graph.output, имя,ordinal,producer output index,dtype/shape/role | каждая строка сопоставляется явно либо removal объявлен отдельным graph cut | каждый required role присутствует либо доказательно восстановлен; unexplained missing output=FAIL admission |

Обычные Detect и Pose по выбранному source имеют один output каждый, поэтому отсутствие второго само по себе здесь не дефект. Однако проверять нужно actual graph: custom wrapper/cut может добавить/разделить outputs; script не имеет права их незаметно терять.

**Name≠port:** ONNX Value namespace отличается от Node namespace; node.name не является обязательным именем выходного значения. Graph outputs positionally ссылаются на Value names; producing-node output index сохраняется отдельно. ONNX `output0` — имя значения, не доказательство TF `output0:0`. TF различает get_operation_by_name и get_tensor_by_name; удаление суффикса `:1` не сохраняет идентичность tensor. Guide's helper `_add_zero_suffix` для конкретного classification example не устанавливает правило port0 для произвольного imported graph.

**Почему имеющийся build не проходит этот contract без доработки:**

1. `force_static_onnx_input_shape`98–110 принудительно ставит B1,C3,H/W=img_size только в input metadata. Это не runtime specialization и не доказательство согласования внутренних shape computations/output dims. Затем conversion/simplification получают уже изменённую in-memory модель. Источник и изменённый parent **не сериализуются отдельно** в данном path.
2. Defaults216–224 берут только graph.input[0]/graph.output[0], summary хранит только этот выбор; остальные outputs не проходят admission.
3. `tensor_name_to_node_name`155–156 отбрасывает port; candidate list248–255 перебирает mapped tensor→stripped node→original ONNX value→original+:0. Конструктор может принять существующий, но семантически неверный endpoint; успешный return не сравнивает значения.
4. Summary сохраняет mapped names и selected_output_node, но не полный mapping, actual callable identity/kwargs, rewritten ONNX bytes/hash, float TF output signature/values, op/attribute delta или выбранный layout adapter. Его `input_layout="nchw"` — literal автора, не наблюдение TF placeholder.

**Предлагаемый artifact chain:** `parent0` exact exported ONNX bytes/hash → `parent1` static-shape modified bytes/hash+exact changed fields → optional `parent2` simplified bytes/hash+tool version/effective flags → converted float TF GraphDef bytes/hash+mapping and IO table → QM→TPU hashes/descriptors. Если static export уже имеет нужный input, metadata surgery исключить либо документировать её как no-op с проверенным graph diff. Для каждого parent checker/shape audit и float parity на **одних сохранённых** input tensors; flags `try_simplify` фиксировать по реальному вызову и результату. Никаких молчаливых retry/выбора другого output при admission. Допуски численной parity назначаются до практического теста; exactness имён/числа/roles/port mapping — структурное условие.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139), [S160](SOURCES.md#S160), [S161](SOURCES.md#S161). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-02](_WORK/W2_02.md), строка 116.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-03 — LinQ percentile, consumer QAT/QDQ и ORT mixed precision — нормализованные наблюдения

<a id="F214"></a>
### F214 — `W2-03-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Guide2025 `QuantizedModel.quantize`: **weights по текстовому описанию**; direct activation scope не установлен

**Documentation, [S133](SOURCES.md#S133) с.7–8**. В сигнатуре default `100.0`; отдельно говорится о calibration tensor для порога. Формула, величина, которую ограничивают, процент retained/rejected, signed/absolute tails и numeric domain не раскрыты.

Текст нельзя расширить до histogram activation percentile. Даже трактовка «100=no clipping» пока не подтверждена формулой. Matching current implementation и PDF visual verification остаются необходимыми.

**S support:** [S133](SOURCES.md#S133). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 33.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F215"></a>
### F215 — `W2-03-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

Современный сторонний `RegularModel.calibrate`: **не установлено**

**Static code, [S139](SOURCES.md#S139) L275–281**. CLI value передаётся в calibrate; при любом TypeError — повтор без percentile; quantize получает thresholds. Summary не сохраняет requested percentile, retry branch и effective thresholds.

Разные CLI X не доказывают разных policies. Нельзя считать успешный retry способом установить unsupported keyword: ошибка могла быть внутри вызова, состояние могло измениться.

**S support:** [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 34.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F216"></a>
### F216 — `W2-03-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

ORT v1.22.0 Percentile: activation histogram; NNCF v2.17.0 quantile: задаваемая range-estimator статистика и отдельная агрегация

**Saved primary code через [S076](SOURCES.md#S076)/S05**, не новое независимое подтверждение. Реализации не эквивалентны LinQ по имени.

Сохранить отдельные поля `object=weights/activations/unknown`, algorithm, sample aggregation, tail convention, policy version. Нельзя добавить LinQ в общий список одноимённых activation calibrators.

**S support:** [S076](SOURCES.md#S076), [S162](SOURCES.md#S162). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 35.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F217"></a>
### F217 — `W2-03-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Confirmed documentation/code path**: [S133](SOURCES.md#S133); сторонний [S139](SOURCES.md#S139)

Есть предусмотренный native PTQ workflow; текущая исполнимость для нашей модели UNKNOWN. Это первый кандидат после получения known-good sample.

**S support:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 49.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F218"></a>
### F218 — `W2-03-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Confirmed vendor claim**, [S134](SOURCES.md#S134)

Не устанавливает W/A signedness, bias/accumulator, scales, rounding, saturation, all-op kernel matrix или per-node overrides. Не заполнять их «стандартным INT8».

**S support:** [S134](SOURCES.md#S134). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F219"></a>
### F219 — `W2-03-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown**, [S133](SOURCES.md#S133), [S139](SOURCES.md#S139), [S134](SOURCES.md#S134) + targeted search

Общий ONNX/PyTorch integration claim не является QDQ numerical contract. Требовать accepted graph **и** numerical preservation evidence.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 51.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F220"></a>
### F220 — `W2-03-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown**

Не найден официальный LinQ parser/schema, import option либо training/export recipe. Способ экспорта AIMET другого производителя не consumer LinQ.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 52.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F221"></a>
### F221 — `W2-03-F08`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown**

Нужны W/A/bias/accumulator types, granularity/axis, zp, rounding/clipping/saturation и documented lowering. Внутренний quantizer может быть fixed grid; неизвестное не запрещает QAT, но не оправдывает его GPU budget.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 53.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F222"></a>
### F222 — `W2-03-F09`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown**

int8 IP claim не доказывает запрета всех других операций, но и не обещает FP islands. Требуются allowed dtype/op combinations и real placement.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 54.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F223"></a>
### F223 — `W2-03-F10`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Unknown support and acceptance**

Наличие CPU на сервере не подтверждает автоматический fallback или допустимость вынесенной neural branch. Нужны device report и правило постановщика.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 55.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F224"></a>
### F224 — `W2-03-F11`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Contradicted as an inference**

Parser acceptance не несёт этого доказательства: возможны fold/recalibration/requantization. Это логическая граница evidence, не найденный дефект LinQ.

**S support:** [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S139](SOURCES.md#S139). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 56.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F225"></a>
### F225 — `W2-03-F12`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code, [S101](SOURCES.md#S101) v1.16.0**: ModelProto `auto_convert_mixed_precision(model, feed_dict, ...)` не принимает provider, обе sessions создаются с CPU

Наличие GPU в машине не переключает данный API на CUDA. Прямое следование live GPU совету без проверки API не устраняет конфликт.

**S support:** [S101](SOURCES.md#S101). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 70.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F226"></a>
### F226 — `W2-03-F13`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code, [S162](SOURCES.md#S162) v1.16.0**: отдельный `auto_convert_mixed_precision_model_path(source_model_path, input_feed, target_model_path, provider, ...)` проводит provider и через FP32, и через trial validation

Есть официальный provider-selectable path в том же exact tag; подменять им ModelProto функцию молча нельзя. Это подтверждённая структура кода, не проверенный запуск GPU/CPU.

**S support:** [S162](SOURCES.md#S162). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 71.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F227"></a>
### F227 — `W2-03-F14`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Documentation/code, [S164](SOURCES.md#S164)/S08 ORT v1.23.2**: CPU Conv/MatMul в таблице не имеют FP16 kernel; Cast и отдельные другие операции FP16 поддерживают. Transformer предусматривает FP16→FP32 CPU fallback casts для подходящих unassigned nodes

«CPU не имеет вообще ни одного FP16 op» слишком широко для этого tag. «FP16 graph на CPU невозможен» также не следует из kernel table: graph rewrite может дать путь. Не все operators/subgraphs/types гарантированно обслуживаются.

**S support:** [S164](SOURCES.md#S164), [S165](SOURCES.md#S165). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 72.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F228"></a>
### F228 — `W2-03-F15`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Code inference из [S101](SOURCES.md#S101)/S08**: CPU validation может проверять преобразованный граф с FP32 compute/cast rewrites, а CUDA — другой execution graph

Успех CPU auto search не доказывает CUDA numerical equivalence, native FP16 speed либо LinQ selective precision. Проверять final artifact на реально целевом provider; search fixture не independent test.

**S support:** [S101](SOURCES.md#S101), [S165](SOURCES.md#S165). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 73.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F229"></a>
### F229 — `W2-03-F16`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**Metadata, [S163](SOURCES.md#S163)**: converter v1.16.0 не pin ORT; live docs [S071](SOURCES.md#S071) не удалось получить на release tag

Нельзя утверждать единую проверенную пару по имени converter. Здесь **статически сопоставлены converter1.16.0 и ORT1.23.2**, но их совместная работа UNRUN. Live GPU sentence остаётся documentation/code mismatch, не молча «исправленной документацией».

**S support:** [S071](SOURCES.md#S071), [S163](SOURCES.md#S163). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-03](_WORK/W2_03.md), строка 74.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-04 — K006: опубликованные CV PTQ/recovery измерения — нормализованные наблюдения

<a id="F230"></a>
### F230 — `W2-04-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F230](RAW_FACTS.md#F230) — Wu: EfficientNet-b0, два действительно разных пути recovery

**Тип: published measurement; [S086](SOURCES.md#S086), Tables 2/6/7/9/10; §4, §5.1–5.2, Appendix A.**

| Поле | Сообщено авторами |
|---|---|
| Model/data/input | EfficientNet-b0; TensorFlow weights converted to PyTorch; ImageNet2012 val; 224×224; 1024 train calibration images |
| Precision/scope | W8A8 для вычислительных операций; weights per-channel max, activations entropy; остальные операции обычно float; custom PyTorch quantization |
| Metric | Top-1 %, higher better |
| Float → PTQ | 76.85 → 72.06; −4.79 процентного пункта |
| Partial recovery | 76.35: исключены 10 из 82 convolution layers; +4.29 п.п. к PTQ, −0.50 п.п. к float |
| QAT recovery | 76.95: +4.89 п.п. к PTQ, +0.10 п.п. к float; отдельная ветвь от best PTQ, не после partial |
| Cost | QAT 15 epochs, SGD, initial LR 1e−3, batch256; partial требует sensitivity evaluations |
| Unknown | Checkpoint hash, PyTorch version, accuracy hardware/eval batch, wall/GPU hours |

**Решение/inference:** partial precision и QAT здесь полезны уже при INT8. Увеличение top-1 над float не доказывает регуляризацию: дополнительное обучение/вариативность остаются объяснениями. Partial route требует возможности сохранить float-островки; W8A8 label не означает весь граф integer. LinQ-совместимость обоих путей UNKNOWN.

**S support:** [S086](SOURCES.md#S086). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-04](_WORK/W2_04.md), строка 21.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F231"></a>
### F231 — `W2-04-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F231](RAW_FACTS.md#F231) — BRECQ: detection recovery преимущественно в low-bit режиме

**Тип: published measurement; [S093](SOURCES.md#S093) Table5, Appendix B.4.4.**

| Поле | Сообщено авторами |
|---|---|
| Model/data/input | Faster-RCNN / ResNet50; MS COCO; 256 train calibration images; resize800/max1333; eval split и checkpoint hash не уточнены в этих локаторах |
| Metric | Bounding-box mAP, шкала таблицы 0–100 |
| Float | 38.55 (32/32) |
| W4A8 PTQ alternatives | Bias correction* 0.25; AdaRound* 37.58; BRECQ 38.29 |
| Differences | BRECQ−AdaRound +0.71 п.п.; BRECQ−float −0.26 п.п. |
| Bitwidth limit | BRECQ W8A8 38.54; W2A8 34.23, то есть −4.32 п.п. от float |
| Reconstruction/cost | Blocks в backbone, layer reconstruction в остальных частях; batch32; 20000 iterations/block; Adam weight-rounding LR1e−3, activation-step LR4e−5 |
| Unknown | Per-operator exclusions/real integer coverage, software versions, hardware, detection wall/GPU hours и eval batch |

**Решение/inference:** это сравнение независимых PTQ recipes, а не последовательность «bias→AdaRound→BRECQ» на одном восстановляемом артефакте. Большой выигрыш над неудачным baseline не равен такой же выгоде для уже хорошего INT8. Время ImageNet BRECQ нельзя присвоить detector.

**Отдельный source check, [S166](SOURCES.md#S166) Usage:** авторский README для ResNet18 W2A4 сообщает before-BRECQ 0.13599999248981476, weight-only 66.32799530029297, full W2A4 65.21199798583984 (accuracy %). Это не detector и не строка paper с тем же run identity. Числа оставлены как author-reported example, не склеиваются с float другой таблицы в выдуманный paired experiment. Они подтверждают наличие опубликованного recovery outcome в официальном source, но не воспроизведение.

**S support:** [S093](SOURCES.md#S093), [S166](SOURCES.md#S166). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-04](_WORK/W2_04.md), строка 38.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F232"></a>
### F232 — `W2-04-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F232](RAW_FACTS.md#F232) — MMDeploy: отрицательный detection outcome для YOLOX INT8

**Тип: published deployment measurement; [S167](SOURCES.md#S167) Accuracy benchmark / mmdet / YOLOX.**

| Поле | Сообщено / UNKNOWN |
|---|---|
| Model/dataset | YOLOX; accuracy row linked to yolox_s_8x8_300e_coco.py; COCO2017; точный split/checkpoint hash UNKNOWN |
| Metric/results | box AP: PyTorch FP32 40.5; TensorRT FP32 40.3; FP16 40.3; INT8 29.3 |
| Difference | TRT INT8−TRT FP32 = −11.0 AP пункта; против PyTorch = −11.2 |
| Recovery | Не приведено |
| Quantization | INT8 backend label; exact W/A coverage, exclusions, calibration size/method UNKNOWN |
| Input/batch/hardware/software/cost | Для accuracy row UNKNOWN; dynamic configs по Notes. Не подставлять static latency dimensions/batch/T4/TensorRT7.2.3.4 как точный setup этой accuracy строки |

Проверены оба hyperlink: latency YOLOX указывает **tiny**, accuracy — **s**. Поэтому брать 416×416 и latency из строки tiny в карточку accuracy модели s было бы ложной склейкой.

**Решение/inference:** official deploy не гарантирует малую INT8 деградацию даже внутри известного backend. Эти числа — ограничивающий пример для обязательного собственного task gate, а не доказательство причины ошибки или свойств современной YOLOX/LinQ.

**S support:** [S167](SOURCES.md#S167). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-04](_WORK/W2_04.md), строка 57.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F233"></a>
### F233 — `W2-04-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F233](RAW_FACTS.md#F233) — MMDeploy/ncnn: прямое pose FP32→INT8 evidence найдено

**Тип: published deployment measurement; [S168](SOURCES.md#S168) Pose detection.**

| Поле | Сообщено / UNKNOWN |
|---|---|
| Backend/model | ncnn quantization, S-ViPNAS-MobileNetV3 |
| Dataset/metric | COCO2017, keypoint AP в шкале 0–1 |
| Float → INT8 | 0.687 → 0.683; −0.004 AP = −0.4 пункта шкалы 0–100 |
| Limiting condition | Та же model family, COCO Wholebody: 0.459 → 0.445; −0.014 AP = −1.4 пункта шкалы 0–100 |
| Controls | flip_test=False; linked config filename vipnas_mbv3_coco_256x192.py указывает 256×192, но measured model/config hash не опубликован |
| UNKNOWN | Exact eval split, batch, W/A/operator coverage и float exclusions, ncnn/MMPose version, hardware, calibration method/size конкретно pose, quantization/recovery time |
| Recovery | Не сообщено |

Не переносить note про 4000/50000 ImageNet samples на COCO pose. Note про 512 train calibration images расположен у mmseg; его применимость к pose здесь не доказана. Не переносить современный 1.x benchmark stack на этот 0.x результат.

**Решение/inference:** pose INT8 evidence больше не общий UNKNOWN: в указанном ограниченном backend/model setup есть прямые числа. Это не RTMPose, не YOLO-Pose и не доказательство безопасности падений/дрожания позы. DARK как coordinate refinement не используется вместо evidence; выбранная основная строка не имеет suffix dark.

**S support:** [S168](SOURCES.md#S168). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-04](_WORK/W2_04.md), строка 74.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-05 — Что именно опубликовано о LinQ и что завершает runtime inference — нормализованные наблюдения

<a id="F234"></a>
### F234 — `W2-05-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F234](RAW_FACTS.md#F234) — Vendor TinyYOLO3: author reported completion, artifact unavailable

**Объект:** готовый vendor `tiny_yolo3_b8_o5_128x128_asic.tpu`, не self-build YOLOv8. [S140](SOURCES.md#S140) §3.4 L138–159, §5 L304–329; [S171](SOURCES.md#S171) README Vendor. Автор обозначает путь final valid, а в completion list — done для HP1M/HPD1M. Одновременно статус MLPerf с qps2000 сформулирован как expected. Это совместимые по смыслу авторские сообщения о workflow, но **не прочитанный raw VALID log**.

**Условия из команд/кода:** Python env `linq_venv311`; MLPerf path содержит `mlperf-16.16.12-Source`, что не доказывает фактически установленную библиотеку; TPU program имя b8/o5/128x128_asic; input `(8,416,416,3)` NHWC float32 0..1, input_1:0 — контракт по README автора. COCO2017 val, instances_val2017.json, limit5000; conf .001, IoU .45, max_det300. Класс80 и COCO mapping/YOLO anchors — defaults adapter, не описание наших классов.

**Разделены две процедуры:** accuracy direct TPU→host decoder/NMS→COCOeval (`bbox` AP@[.50:.95], AP50/AP75, size AP, AR); performance — отдельный executable MLPerf offline/performance, qps2000 в scenario, runs3. Orchestrator пишет `results_summary.json`, `accuracy_summary.json`, `metrics.json/txt`, `predictions.json`, `performance/b8/summary.json`; run directories ожидают `mlperf_log_summary.txt`, stdout/stderr. `--batch-size` в performance wrapper задаёт path/metadata, но не отдельный CLI argument нативному binary: actual batch определяется program/native runner. QPS — запрос config, не измеренный FPS.

**Что реально опубликовано:** код и авторский статус; **числа AP/FPS и actual MLPerf result UNKNOWN**, поскольку перечисленные JSON/logs не присутствуют в проверенном [S169](SOURCES.md#S169). Не найден release/Actions artifact, который закрывал бы gap. Отсутствие файлов не опровергает successful vendor run и не доказывает неработоспособность LinQ detection. Практическое решение: vendor-ready branch допустим как кандидат для первого smoke, но custom checkpoint fidelity/quality невозможно принять по имени TinyYOLO3. Нужен Q01.

**S support:** [S140](SOURCES.md#S140), [S169](SOURCES.md#S169), [S171](SOURCES.md#S171). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 26.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F235"></a>
### F235 — `W2-05-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F235](RAW_FACTS.md#F235) — Self-build YOLOv8s: source code / proposed route, published successful measurement unestablished

**Объект:** exporter/build/run YOLOv8s с NCHW640 route, PIN [S043](SOURCES.md#S043); отличается от NHWC416 vendor TinyYOLO3 по архитектуре, artifact, input и decoder. [S140](SOURCES.md#S140) final detection plan выбирает TinyYOLO3; списка successful self-build YOLOv8 results в [S140](SOURCES.md#S140) нет. В [S169](SOURCES.md#S169) нет `.qm/.tpu`, build summary, completed output/log или quality JSON этого YOLOv8. Поэтому «published verified YOLOv8 transfer» не установлено.

Статические проблемы runner из W1 подтверждены свежим raw: Unicode имя `args.output_tensอร์_name` L206 отличается от argparse destination; `run_once` предпочитает `.run`, затем `.sync`; shape decoder для84/85 каналов; NMS host. Они не являются результатом исполнения, не доказывают отсутствие работающего исправленного авторами варианта и не опровергают отдельный TinyYOLO3. Практическое решение: использовать как материал для implementation review после получения matching bundle; не как baseline measured validity и не как rescue от unknown custom compiler support. Q01/Q02.

**S support:** [S043](SOURCES.md#S043), [S140](SOURCES.md#S140), [S169](SOURCES.md#S169). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 36.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F236"></a>
### F236 — `W2-05-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F236](RAW_FACTS.md#F236) — Остальной авторский result set: reported status с недоступными metrics

[S140](SOURCES.md#S140) §§3.1–3.5/5 заявляет done: self-build ResNet50 O1/O5 HP1M/HPD1M, self-build FCN-ResNet50 O1 HP1M/HPD1M, vendor ResNet50 comparison, TinyYOLO3 vendor, ONNX CPU/CUDA baselines. Segmentation O5 explicitly not finalized, не входит в final result set; Model Zoo detection auxiliary, не strict final comparison. §8 содержит предлагаемые parallel classification runs scales1/2/3/4 и перечень обнаруженных устройств по автору; выполненность всех этих scaling commands не следует из текста.

[S169](SOURCES.md#S169) не содержит ни одного указанного result JSON. Численные outcomes этих веток в этом scope **artifact unavailable**, не «нулевые», не «не запускались». Сравнение strict TinyYOLO3 ONNX из pjreddie cfg/weights и vendor `.tpu` требует equality model/weights/decoder; фраза strict сама её не доказывает. Проверенные общие имена источников не заменяют hashes. Практическое решение: не строить таблицу LinQ/NVIDIA из планируемых paths и не смешивать два detector baseline.

**S support:** [S140](SOURCES.md#S140), [S169](SOURCES.md#S169). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 42.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F237"></a>
### F237 — `W2-05-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F237](RAW_FACTS.md#F237) — Vendor presentation: actually reported numerical throughput/latency, без fidelity accuracy

[S137](SOURCES.md#S137) extraction даёт отдельные численные результаты; ниже только строки, полезные для CV выбора. Все строки — vendor-reported measurement по сноске, с **непроверенным визуально извлечением**.

| Network label | Batch | HP throughput FPS | HP latency ms | HPQ throughput FPS | HPQ latency ms |
|---|---:|---:|---:|---:|---:|
| ssd_mobilenet_v2 | 1 | 556.7 | 3.54 | 2226.8 | 3.54 |
| ssd_mobilenet_v2 | 8 | 428 | — | 1712 | — |
| yolo5s | 1 | 106.1 | 23.71 | 424.4 | 23.71 |
| yolov8n_pose | 1 | 104.8 | 21.51 | 419.2 | 21.51 |

**Setup сноски:** Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43; заявлена методика MLCommons MLPerf. Это не автоматически официальная submission/VALID result. Точный input resolution/shape, weights hash, exporter/version/opset, dataset/split, accuracy, latency scenario/percentile, preprocessing/copy/NMS scope, warmup, completed sample count и native completion trace не раскрыты в прочитанной таблице/сноске. INT8 фигурирует в характеристиках платформы, но per-model effective precision/compiler recipe этой таблицей не фиксируется.

HPQ throughput в этих строках равен4×HP, latency равна HP; нельзя установить, что каждая HPQ строка независимо измерена, или восстановить параллелизм/очереди. Нельзя принимать `1000/FPS` за latency таблицы: для yolov8n_pose это около9.54ms, тогда как reported latency21.51ms; несовпадение не доказывает ошибку, поскольку границы/методика могут различаться. Здесь не восстанавливается скрытая методика делением. Batch8 SSD медленнее batch1 по reported throughput: batch не гарантирует speedup даже в vendor таблице.

**Практическое решение:** yolov8n_pose — полезное официальное свидетельство существования benchmark для такого label, но не доказательство сохранения keypoints/OKS/AP после custom quantization, не число поддерживаемых video streams и не SLA событий. Числа не переносить на наши веса, 3090, unknown VM или наш E2E pipeline. Для представления перед жюри нужны собственные completed measurements. Нужен Q03; до bytes полная визуальная table verification остаётся open.

**S support:** [S137](SOURCES.md#S137). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 48.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F238"></a>
### F238 — `W2-05-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F238](RAW_FACTS.md#F238) — Исторический completion call chain конкретнее общего слова sync

[S145](SOURCES.md#S145) `_bindings.py` L373–425: `sync(inputs, mode=FULL)` выделяет input/output buffers, задаёт user pointers, вызывает native `tpu_run_inference(device,inference,mode.value)`, затем читает output, проверяет `tpu_get_inference_status`, возвращает dictionary. Nonzero run/status превращаются в InferenceError. Python source не содержит отдельного barrier/wait внутри sync; completion должен обеспечиваться контрактом вызываемого native run, а не интерпретацией имени Python метода. C declaration содержит также `tpu_submit_inference` с callback, но один объявленный символ не доказывает доступный high-level async API, используется ли он или его текущие guarantees.

[S133](SOURCES.md#S133) guide2025 с.21 явно описывает `inference.sync` как blocking. [S145](SOURCES.md#S145) packaged ResNet50 test ожидает usable result сразу после sync, но **исходник теста не test result**. PyPI README остаётся смешанным историческим описанием (`iva_tpu`, старые классы/futures), не подтверждением API16. Текущая `.run` ветка [S172](SOURCES.md#S172)/S07 не получает blocking semantics из guide `.sync`. Timeout/cancel/retry/reset и thread-safety фактически выданного SDK UNKNOWN. Нельзя заявить завершение через device inventory или return enqueue.

**S support:** [S043](SOURCES.md#S043), [S133](SOURCES.md#S133), [S145](SOURCES.md#S145), [S172](SOURCES.md#S172). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 67.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F239"></a>
### F239 — `W2-05-F06`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F239](RAW_FACTS.md#F239) — FULL mode и RAW program различаются; появился конкретный RAW debug dependency

[S145](SOURCES.md#S145) enum L165–169: RAW0, PRE_PROCESS1, POST_PROCESS2, FULL3. `sync` передаёт mode нативной функции; Python не реализует quant arithmetic PRE/POST и не раскрывает место CPU/TPU этих этапов. `_load_inference` передаёт byte pointers, а `_get_inference` для non-raw program интерпретирует bytes через `view(user_dtype)` и reshape(user_shape). Указатель uint8 — адрес байтов, не объявление numerical INT8; `view` не выполняет dequantization.

Отдельно `_is_raw_metadata` L506–518 определяет **RAW program** по отсутствию user_dtype в metadata, а raw output reshapes bytes по ddr_word_len. Это свойство program metadata, не то же, что mode=RAW. Для обычного program просто передать RAW mode ещё не означает, что sizes/reshape/output семантика Python стали raw: выбор размеров/интерпретации привязан к `_program._is_raw`.

**Новый факт beyond W1:** `_converter_to_raw.py` L29–40,76–140 содержит `Codec.encode/decode` с delegation в `tpu_tlm_is.models.iotools.tpu_encode/tpu_decode`; восстанавливает TensorDescription из user/tpu shape/order/dtype, padding, scales, anchor. `convert_to_raw` требует **internal tpu_tlm_is**, переписывает metadata для raw program и возвращает Codec. Без internal dependency выдаёт явный ImportError. Публичный Python пакет поэтому показывает предполагаемый debug route и нужные descriptors; он не содержит здесь арифметику tpu_encode/decode/native processing и не доказывает доступность этого route в выданной VM. Historical hardware mappings в helper ограничены тремя вариантами размеров слов, совместимость с новым target неизвестна.

**Практическое решение:** не делать собственный `astype(int8)` или универсальный scale из byte output; не добавлять второй rescale к user-format FULL output. Запрашивать matching `.tpu` descriptors + codec/native manual; FULL↔documented RAW+codec parity проверять лишь поддержанным текущим механизмом. Наличие старого helper позволяет сформулировать более точный Q02, не объявить current feature supported.

**S support:** [S145](SOURCES.md#S145). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 73.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F240"></a>
### F240 — `W2-05-F07`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F240](RAW_FACTS.md#F240) — Timing bug есть и в vendor direct adapter; он не переносится автоматически на MLPerf

[S172](SOURCES.md#S172) L770–793: timer охватывает только `run_once`, decode/NMS после t1; preprocessing/aux preparation до t0; load/probe и COCOeval вне timer. Первый input-name probe может вызвать несколько inference попыток, не включённых в измерение. Значение throughput_img_per_sec поэтому runtime-call throughput при условии blocking run, а не end-to-end FPS.

Warmup default10 images, batch8. На втором batch processed16, в numerator добавляются6 реальных images, но в denominator — время полного8 batch. При N5000 и без ошибок/padding numerator4990, timed calls624 batches =4992 slots. Это **аналитическое следствие кода, не benchmark**; при равном времени full batches относительный коэффициент4990/4992≈0.999599, не измеренная величина ошибки для произвольных timings. При малом тесте N16 коэффициент6/8=.75 — потенциально большой bias. Финальный неполный batch повторяет последнюю картинку до B; полезные completed frames не равны padded slots. Warmup следует исключать целыми batches или измерять точные общие границы; useful FPS считать по реально completed IDs.

[S173](SOURCES.md#S173) performance wrapper использует иной pipeline: native `-s offline -m performance -p program -q qps`, не данный Python timer. Поэтому **нельзя переносить Python warmup defect на vendor presentation или native MLPerf logs без их реализации**. Его Python `is_valid` требует текст VALID и распарсенное Samples per second, но не `returncode==0`; returncode только записан. Existing run directory используется повторно, summary file не удаляется заранее: статически возможна stale-log интерпретация. Это причина требовать свежий run identity, полный raw log/config и successful return code; не установленный факт случившегося неправильного измерения. Нативный warmup/sample denominator/completion этой обёрткой не раскрывается.

**S support:** [S172](SOURCES.md#S172), [S173](SOURCES.md#S173). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-05](_WORK/W2_05.md), строка 83.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-06 — два конкретных альтернативных export route cards, K008 — нормализованные наблюдения

<a id="F241"></a>
### F241 — `W2-06-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F241](RAW_FACTS.md#F241) [code / inference; [S174](SOURCES.md#S174), [S018](SOURCES.md#S018), [S051](SOURCES.md#S051), [S175](SOURCES.md#S175)].** Точная source identity — U, `rtdetr-l.yaml`: HG backbone + AIFI + RepC3/FPN/PAN + `RTDETRDecoder`; `nc=80`, default `nq=300`, hidden256, heads8, points4, decoder6. Это не Paddle RT-DETR и не upstream lyuwenyu export wrapper с тремя outputs и `orig_target_sizes`. Нельзя смешивать их signatures.

| Поле | Exact route / actual status / ограничение |
|---|---|
| Checkpoint identity | Кандидат `rtdetr-l.pt`; pinned downloads source формирует [assets/v8.3.0/rtdetr-l.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/rtdetr-l.pt). Это конкретный locator из кода, **не полученные bytes**; SHA256 weights, manifest classes и matching YAML нужно зафиксировать до запуска. Одинаковое имя файла не гарантирует одинаковые weights. |
| Exporter | Ultralytics8.3.230/U `Exporter.export_onnx→utils/export/engine.torch2onnx`. Выбранный **PROPOSED** профиль: format=onnx, imgsz=640, batch=1, dynamic=False, half=False, simplify=False, nms=False, opset=16, device=cpu. В ONNX accepted args нет int8; добавлять `int8=True` к этой ветви как готовую PTQ нельзя. Exact установленный PyTorch/ONNX/Python lock ещё отсутствует: source допускает диапазоны, а не задаёт уникальный exporter binary. |
| Export behavior | Source deepcopy/eval/fuse; `RTDETRDecoder.export=True`; dry forwards, torch.onnx legacy tracer, `dynamo=False` для torch>=2.4, constant foldingTrue. Это не modern dynamo default по текущему PyTorch. `nms=True` exporter принудительно меняет наFalse для RTDETR. simplifyFalse исключает ещё одно преобразование; при его включении нужен отдельный parent/hash/parity. |
| Input | Declared expected `images: float32[1,3,640,640]` NCHW RGB/255; исходные BGR image arrays преобразуются BasePredictor. Перед этим `LetterBox(auto=False,scale_fill=True)` — растяжение до640², без aspect-preserving padding. Не копировать fixed letterbox114/pad inverse из W2-02. Тензорный input bypass image preprocessing требует уже готового того же tensor. |
| Output | Source-derived expected `output0: float32[1,300,84]` **BNC**. Последняя ось4 normalized cxcywh +80 **sigmoid probabilities**. Нет no-object logit, отдельной objectness, DFL или вспомогательного pose tail. В custom nc это `[1,300,4+nc]`, при подтверждённых изменённых weights/classes. Actual exported NodeProto/IR/op inventory/IO ещё не получены. |
| Host decoder | `xywh2xyxy` на нормированных координатах; максимум по классу для каждого query; strict score>conf, optional class filter; sort descending, global max_det; x×original_width, y×original_height. Нет NMS и повторного sigmoid/softmax. Query duplicate/tie behavior фиксируется separately; добавление NMS — изменение policy, а не repair. |
| Shape/ops | При640² feature levels80²+40²+20²=8400 positions; TopK300 выбирает queries **внутри neural graph**. [S175](SOURCES.md#S175) реализует `GridSample` bilinear/zeros/align_cornersFalse, а также MatMul/self-attention/Softmax/LayerNorm, dynamic index/gather, reshape/transpose, inverse-sigmoid/log/refinement. Это source requirements, не actual ONNX inventory: точные lowerings Norm/attention зависят от PyTorch. |
| Specific GridSample contract | На B1: heads8, head_dim32, Q=300, points4; sampler X примерно `[8,32,H_l,W_l]`, grid `[8,300,4,2]`, output `[8,32,300,4]`, уровни80/40/20. `grid=2*sampling_locations−1`; out-of-bound zeros. ONNX GridSample-16 — стандартная4D операция, но стандартность не означает поддержку LinQ. Перейти наopset13 без rewrite этой операции нельзя считать нейтральным решением. |
| Quantization scope | Этот route создаёт float ONNX. Ultralytics engine/OpenVINO/TF INT8 branches существуют отдельно и не создают LinQ QM/TPU. LinQ PTQ должен быть только matched SDK из W2-01/03; QDQ/QAT/mixed exclusions consumer неизвестен. Сохранять float head outputs/attention diagnostics до решения о calibration. Internal TopK changes могут давать дискретную смену query от небольшой numeric ошибки. |
| LinQ evidence | **UNKNOWN** exact import/opset16/GridSample attributes/attention coverage/output mapping, float TF parity, quantization и actual TPU execution. Нет нашей модели/SDK/компиляции. W2-05 vendor pose/YOLO labels не распространяются на RTDETR. |

**S support:** [S018](SOURCES.md#S018), [S051](SOURCES.md#S051), [S174](SOURCES.md#S174), [S175](SOURCES.md#S175). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-06](_WORK/W2_06.md), строка 31.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F242"></a>
### F242 — `W2-06-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F242](RAW_FACTS.md#F242) [proposal; [S174](SOURCES.md#S174), [S018](SOURCES.md#S018), [S051](SOURCES.md#S051), [S175](SOURCES.md#S175), [S176](SOURCES.md#S176)] — когда prefer/reject.** Предпочесть как проверяемый альтернативный detector, если текущий bottleneck действительно DFL/NMS/output decode, а supplier подтвердил и micro-test проверил GridSample16 + exact internal TopK/attention path. Отвергнуть как быстрый fallback, если importer ограничен низким opset, sampler или dynamic gathers не проходят float admission, единственный обход — обучаемый attention decoder на CPU, либо доступен лишь vendor service с фиксированной моделью. Перенос CPU **постобработки** не удаляет внутренний deformable attention. Не объявлять эту архитектуру «более простой для LinQ».

**S support:** [S018](SOURCES.md#S018), [S051](SOURCES.md#S051), [S174](SOURCES.md#S174), [S175](SOURCES.md#S175), [S176](SOURCES.md#S176). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-06](_WORK/W2_06.md), строка 46.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F243"></a>
### F243 — `W2-06-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F243](RAW_FACTS.md#F243) [code; [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S054](SOURCES.md#S054), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180)].** Точная модель — MMPose1.3.2/M config `configs/body_2d_keypoint/rtmpose/coco/rtmpose-m_8xb256-420e_coco-256x192.py`, не wholebody/animal/RTMO и не произвольный SimCC. Codec `SimCCLabel`, input_size=(192,256) **W,H**, split_ratio2, normalizeFalse, use_darkFalse, K17; CSPNeXt-m P5, `RTMCCHead` in768, final conv7, feature6×8, GAU hidden256/s128, no relative bias/rotary positional encoding. Config test flipTrue отдельно от forward export.

| Поле | Exact route / actual status / ограничение |
|---|---|
| Checkpoint | Primary metafile даёт [rtmpose-m_simcc-coco_pt-aic-coco_420e-256x192-d8dd5ca4_20230127.pth](https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-m_simcc-coco_pt-aic-coco_420e-256x192-d8dd5ca4_20230127.pth). Не путать backbone pretrain URI из init_cfg с final pose checkpoint. Bytes/hash не получены, доступность weight URI не проверена скачиванием. |
| Exporter identity | MMDeploy1.3.1/D, `tools/deploy.py`/ONNX export API; stock `configs/mmpose/pose-detection_simcc_onnxruntime_dynamic.py`; base opset11. Именно D регистрирует `mmpose.models.heads.RTMCCHead.forward` и `BasePoseEstimator.forward→_forward`; название rewrite file `simcc_head.py` не исключает RTMPose. |
| Version seam | Это **source-pinned proposal M1.3.2+D1.3.1**, не утверждение tested supported lock. D requirements/codebases ставит mmpose==1.0.0,mmdet==3.0.0. При этом D backend pack_result читает input_center/input_scale — они есть в M1.3.2 TopdownAffine; M1.0.0 их не записывает и свой inverse читает gt_instances bbox_centers/scales. Поэтому blindly install requirements+new example опасно. До исполнения нужен явный dependency override/lock (M/appropriate mmdet/mmcv/mmengine/torch/onnx), registry/import/metadata smoke. Одного совпадения major или support-tableY недостаточно. |
| Static specialization | Stock config fixed H/W, но dynamic batch axis0 на input и обоих outputs. Отдельный guessed stock static filename дал404. Сохранён [PROPOSED derived config](_WORK/MATERIALS_W2_06/pose-detection_simcc_ort_static_b1_PROPOSED.py): наследовать stock, `onnx_config.dynamic_axes=None`, input_shape[192,256], optimizeFalse, export_postprocessFalse; экспортный пример B1. Это новый config **до tracing**, не перепись dim_param готового ONNX. [S179](SOURCES.md#S179) get_dynamic_axes возвращаетNone и exporter передаёт его torch.onnx.export; actual B1 shapes всё равно проверяются на artifact. |
| Input tensor | Expected `input: float32[1,3,256,192]` NCHW, **уже нормализованный RGB**: `(pixel−mean)/std`, mean123.675/116.28/103.53, std58.395/57.12/57.375; нет отдельного `/255` перед этими параметрами. Нормализация/crop снаружи `_forward` графа. Owner preprocessor должен быть один, без дублирования LinQ PRE. |
| CPU crop / ownership | Upstream person detector/track→bbox→GetBBoxCenterScale(default padding1.25)→aspect ratio192/256→TopdownAffine(use_udpFalse, rotation0 в test, cv2.INTER_LINEAR)→crop. Один crop на человека, metadata center/scale/input_size/warp и personID сохраняются. Это отдельный dependency: отсутствие детекции нельзя исправить точным pose. MMDeploy create_input по умолчанию строит dummy **full-image bbox**, не извлекает людей из видео. Для валидной production проверки нужны реальные detector boxes или строго одинаковые GT boxes в обеих ветках. |
| Neural outputs | Expected `simcc_x: float32[1,17,384]`, `simcc_y: float32[1,17,512]`; это raw Linear outputs, не17 xyv и не probabilities с гарантией0..1. `export_postprocess=False` возвращает оба без CPU/Numpy decoder. Swapping axes допустимо не эвристически, а только по explicit manifest. |
| CPU decoder | Для каждой точки argmax по x иy; score=min(max_x,max_y); если score<=0, helper ставит coords−1, затем codec делит на2 (invalid sentinel становится−.5 до inverse). No default softmax, no DARK; не заменять score на visibility/objectness. Геометрия M1.3.2/D: `xy/image_input_size * input_scale + input_center −.5*input_scale` для test rotation0; из input tensor координат обратно в original frame, не просто прибавить левый верх bbox. Invalid/low-score policy downstream фиксировать отдельно до event rules. |
| Operators/shape limits | GAU содержит ScaleNorm L2 norm/clamp/div, Linear/MatMul, split/unbind/transposes, SiLU, batched QK matmul, ReLU-square kernel, второй batched matmul, multiplication/residual; softmax **не** тот же GAU kernel. Backbone CSPNeXt channel attention включён. No ROIAlign/GridSample требуется для описанного host crop, но это не доказательство all-convolution network. Spatial6×8 flatten→Linear48→256 фиксирован выбранной конфигурацией; заменить192×256 на arbitrary H/W только dynamic_axes нельзя. Exact ONNX lowerings/custom domains/constant folding проверяются после экспорта. |
| Export postprocess caveat | D rewrite при export_postprocessTrue добавляет get_simcc_maximum и деление split_ratio, утверждая use_darkFalse; outputs становятся pts/scores и требуют других names/shapes. Эту ветку не смешивать с нашими simcc_x/y. CPU decode сuse_darkTrue теоретически другая ветка, но не выбранный контракт; название SimCC не гарантирует coverage любого codec. |
| Flip seam | M config flip_testTrue, обычный predict делает два forwards и averaging после flip_vectors. D forward rewrite вызывает `_forward`, без predictor TTA. Для fidelity baseline явно **flip_test=False** в исходной validation, либо реализовать и измерить эквивалентный host TTA двумя TPU crops с correct COCO left/right indices. Разница single-pass и flip AP — изменение inference policy, не доказательство INT8 degradation. |
| PTQ/QAT tooling scope | Наш D ORT config float, без PTQ recipe. D SimCC TRT config описывает2 outputs/batch1–4; generic pose TRT INT8 config наследует single-output base и сам по себе не готовая RTMCC/SimCC INT8 chain. Это backend-specific building blocks, не LinQ converter. MMDeploy ncnn rewrite ScaleNorm/GAU прямо адаптирует broadcast/FP16 overflow дляncnn; он не включается автоматически для ORT/LinQ. Ни поддержка QDQ/QAT trained ranges, ни head float exclusions LinQ здесь не установлены. Calibrate только на тех же нормализованных **person crops** с целевыми масштабом/окклюзиями, не full frames, под видом proposal. |
| LinQ evidence | **UNKNOWN** import opset11/lowerings, ScaleNorm/GAU quantization,2 outputs preservation/layout/scales, variable number crops scheduling, target precision, compiled quality. Нет publicly pinned RTMPose/SimCC program+log в этой ветке. Vendor yolov8n_pose label из W2-05 — другая модель/выходной контракт. |

**S support:** [S054](SOURCES.md#S054), [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-06](_WORK/W2_06.md), строка 50.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F244"></a>
### F244 — `W2-06-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F244](RAW_FACTS.md#F244) [inference/proposal; [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S054](SOURCES.md#S054), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180), [S181](SOURCES.md#S181), [S182](SOURCES.md#S182), [S183](SOURCES.md#S183)].** Prefer P, если нужно независимо заменить one-stage pose head, уже есть надёжные person boxes и supplier принимает network raw two-output contract, а CPU crop/codec разрешены. Reject как быстрый fallback, если сервис выдаёт только фиксированные детекции/готовые keypoints, запрещены custom weights/two outputs, crop count×latency не укладывается в измеренный deadline, отсутствует person detector или input resolution не сохраняет нужные суставы/объекты. Модель17 keypoints не распознаёт телефон/сигарету/СИЗ сама; смена pose не закрывает эти detector classes. Если dependency seam не закрыт первым smoke, не тратить GPU на QAT этого пути.

**S support:** [S054](SOURCES.md#S054), [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180), [S181](SOURCES.md#S181), [S182](SOURCES.md#S182), [S183](SOURCES.md#S183). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-06](_WORK/W2_06.md), строка 68.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F245"></a>
### F245 — `W2-06-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

[F245](RAW_FACTS.md#F245) — сравнение с рабочими ветками и stop-loss

Тип: inference/proposal из двух cards плюс **secondary** W2-02/W2-05; эти соседние отчёты не являются нашими execution results.

| Ветка | Чем может помочь | Реальная цена/ограничение | Приоритет до GPU |
|---|---|---|---|
| W2-02 static Ultralytics Detect/Pose | Уже связанный U contract и common exporter/source; меньше изменений инфраструктуры | Exact importer/port/layout и real artifact всё ещё unknown; shape BCN8400, другой decoder | Сначала выданный SDK identity и float importer gate. Если текущее препятствие только adapter, исправлять этот seam. |
| D RT-DETR-l | Нет external NMS/DFL; BNC300 прост для host | GridSample16/attention/TopK внутри сети; changing architecture/weights/training | Только после supplier admission sampler/attention; не автоматический второй выбор. |
| P RTMPose-m/SimCC | Raw fixed17 axis vectors; crop/argmax/inverse наCPU | dependency seam, GAU/ScaleNorm,2 outputs, detector miss/crop scaling, flip baseline | Сначала dependency/metadata smoke и float paired crop pack; затем LinQ import. |
| W2-05 vendor-ready TinyYOLO3 / available supplied program | Потенциально первый target smoke без custom export | Авторская completed status без прочитанных AP/logs/hashes; чужие classes/anchors/input; не эквивалент custom detector. Published yolov8n_pose throughput не даёт pose-quality proof | При реально выданном artifact и подходящих classes разумно приоритетнее exploratory architecture replacement для демонстрации LinQ execution; качество отдельно проверять. |

Stop-loss не назначается выдуманными часами: если на **первой** concrete unsupported-op/source-version границе нет документированного эквивалентного lowering, route ставится BLOCKED_FOR_ADMISSION; повторный QAT/training до устранения не разрешает этот дефект. Если обе neural ветки возможно скомпилировать, окончательный выбор по одинаковому GT/camera split и event budget, назначаемому командой. Нет универсального допуска «1%» и нет прогноза FPS/3090/LinQ.

**S support:** [S018](SOURCES.md#S018), [S051](SOURCES.md#S051), [S054](SOURCES.md#S054), [S174](SOURCES.md#S174), [S175](SOURCES.md#S175), [S176](SOURCES.md#S176), [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180), [S181](SOURCES.md#S181), [S182](SOURCES.md#S182), [S183](SOURCES.md#S183). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-06](_WORK/W2_06.md), строка 70.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

## W2-07 — Ноль ошибок: сила вывода и единая запись приёмки — нормализованные наблюдения

<a id="F246"></a>
### F246 — `W2-07-F01`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F246](RAW_FACTS.md#F246) — documentation/code, [S184](SOURCES.md#S184), [S185](SOURCES.md#S185).** SciPy exact означает Clopper–Pearson. `proportion_ci` получает направление из результата `binomtest`; в pinned source two-sided использует `(1−confidence_level)/2`, less/greater — `1−confidence_level`. `less` даёт верхнюю границу вероятности counted outcome, `greater` — нижнюю. Это проверено чтением ветвей, не запуском SciPy. Практическое решение: явно писать counted outcome, confidence и sidedness; default two-sided не называть one-sided 95%.

**S support:** [S184](SOURCES.md#S184), [S185](SOURCES.md#S185). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-07](_WORK/W2_07.md), строка 23.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F247"></a>
### F247 — `W2-07-F02`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F247](RAW_FACTS.md#F247) — inference из [S185](SOURCES.md#S185) и Bernoulli model.** Зафиксируем до evaluation `n>0` независимых одинаково распределённых observable GT эпизодов с одной бинарной оценкой на эпизод, frozen policy/matcher/deadline и complete follow-up. Если `M~Binomial(n,p_miss)` и `M=0`, то `Pr(M=0)=(1−p_miss)^n`. Инверсия `Pr(M=0)=α` даёт односторонний exact upper bound `U_miss=1−α^(1/n)` и lower recall `L_recall=α^(1/n)`. “Exact” здесь означает coverage не ниже nominal в объявленной модели, не отсутствие uncertainty. Frequentist confidence не является posterior вероятностью того, что параметр лежит в данном наблюдённом интервале. Для `n=0` нет информативной оценки recall: не подставлять ноль в формулу и не писать 100%.

**S support:** [S185](SOURCES.md#S185). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-07](_WORK/W2_07.md), строка 25.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F248"></a>
### F248 — `W2-07-F03`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F248](RAW_FACTS.md#F248) — inference из [S186](SOURCES.md#S186), [S187](SOURCES.md#S187).** Если полный count adjudicated false alerts `F~Poisson(λT)` для заранее фиксированного exposure `T>0`, независимых increments и постоянной общей intensity λ, `Pr(F=0)=exp(−λT)` даёт `U_λ=−ln(α)/T`. Это reciprocal нулевой HPP MTBF bound NIST. False-alert процесс CV должен отдельно соответствовать модели; HPP не дан природой задачи. При T=0 rate undefined, не 0. Rate не probability и не precision. NIST zero-row таблиц с two-sided headers нельзя механически читать как тот же номинальный one-sided level.

**S support:** [S186](SOURCES.md#S186), [S187](SOURCES.md#S187). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-07](_WORK/W2_07.md), строка 27.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F249"></a>
### F249 — `W2-07-F04`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F249](RAW_FACTS.md#F249) — local observation, [S003](SOURCES.md#S003).** На с.5 указаны сложные условия, малые СИЗ, окклюзии и несколько секунд от фиксации до уведомления без точного D. На с.7 приоритет реального инцидента/false burden и одно продолжающееся нарушение→одно сообщение. С.13 требует alert evidence, journal, LinQ и speed measurement; разрешает выбрать приоритетные сценарии. С.19 не задаёт mAP/recall/δ/α. Следствие: acceptance budgets и exact episode/deadline semantics должен принять владелец риска с командой; web не закроет K010.

**S support:** [S003](SOURCES.md#S003). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-07](_WORK/W2_07.md), строка 29.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="F250"></a>
### F250 — `W2-07-F05`

**Assertion, evidence type, locator, version/conditions, limitation и practical implication:**

**[F250](RAW_FACTS.md#F250) — published methodology [S130](SOURCES.md#S130) + application inference [S188](SOURCES.md#S188).** Внутрикластерная корреляция и малое число clusters ограничивают inference; много observations на cluster не заменяет много независимых clusters. Для видео нельзя объявить соседние кадры trials или подставить число кадров в [F247](RAW_FACTS.md#F247). Здесь не предложена regression correction как готовый CI для AP. Claim при неизвестной зависимости — descriptive либо INCONCLUSIVE; нужен дизайн/manifest происхождения.

**S support:** [S130](SOURCES.md#S130), [S188](SOURCES.md#S188). Полный source locator/version/provenance — в карточках S и в исходной записи [W2-07](_WORK/W2_07.md), строка 31.

**Actual checked scope:** чтение сохранённой документации/кода/авторского measurement/аналитики согласно явно указанному выше типу; сборщик прочитал сохранённую запись, не выполнял описываемый код. Models/export/import/quantization/device execution: **NOT RUN**. Если наблюдение LOCAL — это ровно описанное чтение/metadata/hash/аналитическая арифметика, без расширения до hardware test.

<a id="engineering-annex"></a>
# Инженерные таблицы, условия методов и протоколы

Все инструкции в приложении — **PROPOSED/UNRUN**. Они сохраняют детали для авторского синтеза; единая программа обязательств только E001–E012 в OPEN_QUESTIONS. Локальные веточные E остаются историческими указателями, а не новыми общими E.

## Контекст W1-01

Основания: [F004](#F004), [F005](#F005), [F006](#F006), [F007](#F007), [F008](#F008), [F009](#F009), [F010](#F010), [F011](#F011), [F012](#F012). Source scope и статус сохраняются.

## Предлагаемый baseline contract

Ниже — **наш проект контракта**, а не найденный стандарт LinQ. Поля заполняются реальными значениями после получения модели. Неизвестное записывать как `unknown`, а не брать типичные параметры семейства.

| Объект контракта | Что зафиксировать | Что блокирует достоверное сравнение |
|---|---|---|
| Identity | URL/поставщик, дата получения, лицензия и ограничения, исходное имя, SHA-256 checkpoint и всех sidecar/external-weight файлов, model ID, checkpoint kind: raw/EMA/averaged/fused | Перезапись исходного файла; неизвестный выбор EMA; путаница между одноимёнными версиями |
| Architecture | Репозиторий, immutable commit, локальный diff, класс/constructor/config, head configuration, число и **порядок** классов, keypoint schema/visibility, anchors/strides при наличии | Вывод числа классов из одной формы тензора без подтверждения semantics |
| Load | Команда/entry point фактической загрузки, выбранный раздел checkpoint, полный журнал missing/unexpected keys, режим eval, device, параметры fusion | Молчаливый partial load; изменение BN/fusion одновременно с экспортом |
| Environment | OS, Python, framework/build, exporter/runtime и backend/provider, версии numpy/image/video decoder, dependency lock/revisions, CUDA/cuDNN/driver при применимости, container digest и локальный diff | Один `requirements.txt` с диапазонами без фактических разрешённых версий |
| Compute | Batch и порядок, shape каждого input, layout, dtype, device, autocast/TF32/precision flags, seeds библиотек и worker setup, deterministic flags | «FP32» как единственное описание, если фактические матричные вычисления используют иной режим |
| Input transform | RGB/BGR, decode/rotation/colorspace, interpolation и antialias, resize/letterbox rounding, padding value/placement, normalization/range, layout, contiguous representation | Только строка «resize to 640»; backend самостоятельно повторно декодирует и трансформирует файлы |
| Output/decoder | Имена выходов и оси, raw logits/probabilities, bbox/keypoint encoding, units/coordinate frame, decode code commit, NMS variant/IoU/confidence/max detections/class policy, обратная геометрия | Сравнение списков боксов без исходных тензоров и зафиксированной постобработки |
| Video/state | Stream/clip ID, timestamps/time base, frame indices, sampling manifest, tracker/event configs, reset/warmup policy, dropped frames and failure accounting | Только одинаковое число кадров при разных временных точках; state из предыдущего клипа |
| Evaluation | Dataset/annotation revision и hashes, ordered sample IDs, split/group IDs, metrics implementation/version/config, slice definitions, accepted risk and gates | Автоматическое исключение backend failures; перестройка выборки после просмотра результата |

Контракт должен получать новый ID при любой изменённой строке. Новый export/graph/precision/compiler artifact ссылается на ID родителя и записывает ровно выполненное преобразование, версии, параметры, хеши входа/выхода и лог. Исходные веса и исходный golden pack остаются неизменяемыми; восстановление от предыдущего этапа не заменяет проверку относительно исходной модели.

Хеш подтверждает неизменность конкретных байтов, не корректность/лицензию/авторство. Для тензоров отдельно сохранять имя, dtype, shape, порядок элементов и хеш канонических данных: хеш двух разных контейнеров с тем же tensor может различаться. Все sidecar-файлы также входят в manifest.


## Golden pack: входы, выходы, разметка

Рекомендуемая структура — проект методики; перечисленные файлы пока **не созданы и не получены**:

```text
BASELINE_<id>/
  contract.json                  # конфигурация и происхождение
  artifact_manifest.json         # пути, роли, размеры, hashes
  samples.jsonl                  # фиксированные ID, порядок, source/time/group/split/slices
  media/                         # исходные клипы с правами использования
  decoded_frames/                # канонические lossless pixels + timestamps
  model_inputs/                  # exact preprocessed tensors, shape/dtype/layout
  source_runtime_outputs/        # raw outputs из исходного checkpoint runtime
  onnx_reference_outputs/        # если нужны, отдельная роль и происхождение
  decoded_predictions/           # bbox/keypoint outputs от закреплённого decoder
  temporal_reference/            # reset/state policy, tracks/events на клипах
  annotations/                   # человеческий ground truth + revision/protocol
  logs/                          # загрузка, повторяемость, environment, ошибки
```

Две дорожки запуска устраняют неоднозначность:

1. **Tensor replay:** все backend получают один сериализованный `model_inputs` sample, при необходимости с явно записанным эквивалентным layout/quantization adapter. Выходы сравниваются до NMS. Проверяет модель/преобразования/runtime, отделяя decode/resize.
2. **End-to-end replay:** все получают те же исходные файлы и временной manifest; сохраняются decoded pixels и model inputs каждого пути. Проверяет реальную цепочку включая декодер видео/предобработку. Если LinQ API не принимает tensors, tensor replay пока недоступен: это ограничение наблюдаемости, а не доказательство корректного preprocess.

Reference outputs генерировать из доступного исходного runtime после проверки конфигурации, а не из экспортированного графа. Аннотации создаются отдельно: исходные предсказания не считать ground truth. Выходы после NMS не сравнивать только по индексу строки: набор детекций может изменять порядок; нужен согласованный matcher и независимое сравнение raw tensors. Подробный matcher/threshold — ветки 04/12.


## Выборка и предотвращение leakage

Это предлагаемый протокол для видеозадачи, расширяющий общие правила [S009](SOURCES.md#S009)/S06.

1. Зарегистрировать исходное видео до извлечения кадров: origin, acquisition/source license, camera/site/session, timestamps, file hash, restrictions; для публичного материала — URL и revision. Нельзя представлять синтетику как реальное заводское видео.
2. Определить единицу независимого разделения под вопрос обобщения. Минимум — исходная сессия/инцидент и все производные кадры вместе. Если заявляется перенос на новые камеры/площадки, группировать по камере/площадке; split по клипу одной сцены этого не проверяет. Связанные многокамерные записи одного события поместить в общую группу.
3. До sampling и augmentations сохранить train/calibration/tuning/held-out manifests. Калибровка не использует закрытую оценку; конкретную допустимую связь с training задаёт W1-07. Все crops, повторные encode и аугментации наследуют group/split родителя. Проверить exact duplicates по хешам и near-duplicates по изображениям/времени; отрицательный exact-hash check не исключает визуальные дубли.
4. Сформировать `normal` из заранее определённой рабочей популяции. `hard` выделять по независимым признакам сцены либо по ошибкам на tuning. `edge` включает boundary/необычные входы. `regression` хранит минимальный воспроизводимый пример каждого обнаруженного сбоя с bug ID. Это membership tags: один sample может входить в несколько slices, поэтому суммы пересечений не трактовать как число уникальных кадров.
5. При анализе held-out ошибки допускается сохранить её как открытый regression example, но после использования для настройки она больше не служит независимой оценкой обобщения. Сохранять закрытую независимую оценку или честно обозначить отсутствие новой.
6. Для всех backend загружать один materialized ordered manifest, проверять missing/extra/duplicate IDs, входные hashes, total и порядок внутри клипа. Seed не заменяет этот артефакт. Для temporal runs фиксировать timestamps и не shuffle. Невыполненный sample — ошибка запуска/пропуск по заранее заданной политике, а не тихое уменьшение denominator.

Обязательная матрица покрытия; числа примеров назначить после знакомства с данными, а не выдумывать универсальный размер golden pack:

| Slice | Что сохранить | Почему может изменить решение |
|---|---|---|
| Normal | люди/техника на обычных дистанциях и освещении | Показать рабочее качество и типичный перенос |
| Small/occluded | телефон/небольшие средства защиты, дальние люди, частичные перекрытия, pose visibility | Потеря редких признаков может исчезнуть в среднем показателе |
| Boundary | объекты у края, odd aspect ratios, пустой кадр, много объектов/перекрывающиеся боксы | Быстро проявляет padding/coordinate/NMS ошибки |
| Hard negative | безопасное приседание/наклон, рука у головы без телефона, люди рядом с границей без нарушения | Нужен контроль ложных событий, а не только recall |
| Critical clips | падение и похожие движения, вход/выход из опасной зоны, короткое сближение; контекст до/после события | Сохранить время/траекторию; один удачный кадр не доказывает обнаружение события |
| Regression | исходный failing input, exact tensor, output, версия ошибки и ожидаемое поведение | Позволяет проверить исправление без потери воспроизводимости |

GT для клипов должен содержать интервал события, критерий начала/конца, зону/версию геометрии и допустимую неопределённость разметки. Окклюзии и неполная видимость отмечаются явно. Спорные критические случаи просматривает другой участник; сохраняется решение и revision, а не молча меняется label. Набор стрессовых примеров не является оценкой распространённости событий в эксплуатации; показывать его отдельно от представительной normal-выборки.


## Неполная история весов и конфигурации

**A: есть рабочий исходный inference.** Сохранить весь полученный пакет и окружение, подтвердить фактическую загрузку, захватить exact inputs/outputs. Такой observed baseline пригоден для fidelity относительно выбранной точки. История training/pretraining остаётся unknown; утверждение «нет leakage» запрещено без данных об источниках обучения.

**B: есть веса и вероятная архитектура, но нет working inference.** Проверить ключи и формы без молчаливого partial load; восстановить классы и preprocessing из model/config/source/авторского example; проверить каждую гипотезу на независимой размеченной выборке. Сохранить конкурирующие варианты и основание выбора. Настроенный вариант становится **новым реконструированным baseline**, а не доказанным исходным поведением. Совпадающие формы не доказывают правильный порядок классов или normalization.

**C: есть только ONNX/compiled model.** Начать fidelity ladder от доступного артефакта и явно сократить scope: можно сравнивать дальнейшие преобразования и итоговую задачу относительно GT; нельзя доказать fidelity до недоступного checkpoint. Не заменять неизвестные параметры «стандартом YOLO».

Если неизвестность касается label semantics, input range или decoder, baseline не готов для утверждения о сохранении качества. Если неизвестен только optimizer training, это не мешает фиксированному inference при восстановленных весах/архитектуре/режиме [[F005](RAW_FACTS.md#F005)]. При несогласованной или неизвлекаемой исходной модели лучше выбрать другую проверяемую модель, чем расходовать GPU на квантование неопределённого эталона.


## Контекст W1-02

Основания: [F013](#F013), [F014](#F014), [F015](#F015), [F016](#F016), [F017](#F017), [F018](#F018), [F019](#F019), [F020](#F020), [F021](#F021), [F022](#F022), [F023](#F023), [F024](#F024). Source scope и статус сохраняются.

## Матрица реально подтверждённых путей

| Путь | Проверенная версия и параметры | Что сохраняется / ограничение | Когда выбирать и как допускать |
|---|---|---|---|
| `torch.onnx.export(..., dynamo=True)` | PyTorch 2.9; `dynamic_shapes`, `report`, `verify`, `dump_exported_program`, `custom_translation_table` | Использует ExportedProgram; Python-логика устраняется с ограничениями форм. Не является исполнением произвольного Python в ONNX | Кастомная архитектура: сначала capture/translation report; потом несколько независимых значений и форм |
| `torch.onnx.export(..., dynamo=False)` | Legacy TorchScript exporter; для динамики `dynamic_axes` | Tracing фиксирует выполненную ветку; нет гарантии сохранения data-dependent if/loops | Нужен существующей библиотеке или совместимости; обязательны альтернативные ветви и формы |
| TorchScript ScriptModule → legacy ONNX | В API 2.9 принимается ScriptModule/ScriptFunction; документация trace предлагает scripting при control flow | Это документированный тип входа, но не гарантия поддержки всех scripted операторов и целевого runtime | Только если нужен конкретный поддержанный scripted граф; не предлагать scripting как универсальный ремонт ONNX |
| `YOLO(...).export(format="onnx", ...)` | Ultralytics v8.3.230, release 2025-11-21; helper принудительно legacy для torch>=2.4 | Exporter меняет модель: deepcopy, eval, float, fuse, export flags; dynamic input axes и выходы задаются библиотекой | Модели этой библиотеки: сравнить обычный PyTorch, подготовленную export-модель и ONNX; исключить ошибку fusion/export head до обвинения ONNX |
| Ultralytics ONNX с `nms=True` | v8.3.230: NMSModel + torchvision NMS, output с padding до max_det | Меняется семантика выходов; loop по batch разворачивается; dynamic batch рассчитан на заданный export batch | Только после проверки операторов целевого runtime и batch contract; тесты batch=1, export batch, выше export batch |
| Ultralytics ONNX с `simplify=True` | v8.3.230 вызывает onnxslim, требует `onnxslim>=0.1.71` | Ещё одна модификация графа; exception приводит к warning, поэтому аргумент не доказывает фактический результат | Сохранить отдельные before/after артефакты и сравнить на одном pack; детали graph surgery — W1-03 |

Ограничение актуальности: при доступе `docs/stable/onnx.html` перенаправлял на документацию **2.14**, ONNX сайт показывал **1.24.0**. Это фактически увиденные маркировки веб-документов, **не утверждение о дате релиза пакетов**. Рекомендации, требующие воспроизводимой версии, привязаны к 2.9.0 и тегу Ultralytics 8.3.230. Текущая документация Ultralytics уже содержит другой интерфейс export/новые модели; переносить её параметры задним числом на 8.3.230 нельзя.


## Тихие поломки: признак → проверка → решение

Эта таблица — наши диагностические выводы из [F013](RAW_FACTS.md#F013), [F014](RAW_FACTS.md#F014), [F015](RAW_FACTS.md#F015), [F016](RAW_FACTS.md#F016), [F017](RAW_FACTS.md#F017), [F018](RAW_FACTS.md#F018), [F019](RAW_FACTS.md#F019), [F020](RAW_FACTS.md#F020), [F021](RAW_FACTS.md#F021), [F022](RAW_FACTS.md#F022), [F023](RAW_FACTS.md#F023), [F024](RAW_FACTS.md#F024), а не каталог измеренных инцидентов.

| Признак | Наиболее различающая проверка | Решение при подтверждении |
|---|---|---|
| Совпадает только пример экспорта | Другой знак/значение при той же форме; обе ветви if | Удалить зависимость от Python scalar; корректный torch.cond или версионно подтверждённый другой capture path |
| Совпадает 640×640, расходится прямоугольный вход | Одинаковые входные тензоры нескольких допустимых H/W; проверить output A и anchors | Зафиксировать форму либо исправить shape logic/cache; повторить весь pack |
| Только второй элемент batch неверен | Прогнать [a,b], [b,a], каждый отдельно, повтор a; compare per-image | Найти loop unroll/broadcast/cross-batch state; зафиксировать B=1 либо нужный максимум |
| Detector похож, pose систематически смещён | Раздельно boxes/classes/keypoint xy/keypoint confidence до NMS и обратной геометрии | Исправить signature/reshape/decode; не менять precision в качестве первого шага |
| До NMS совпадает, после различается | Один CPU decoder/NMS для обоих raw outputs; сравнить threshold boundary fixtures | Выравнять threshold, class-aware policy, max_det и padding; при допустимости оставить NMS вне графа |
| Ошибка появилась при simplify/смене opset | Повторить тот же pack на сохранённых before/after ONNX | Вернуть pass, локализовать operator rewrite; не обучать модель для маскировки ошибки |
| Export вернул объект/файл, лог содержит ❌ accuracy | Прочитать report и свой numeric gate | Считать артефакт недопущенным независимо от успешного return |

NMS вне графа — полезная диагностическая граница: меньше дискретных операций в первом сравнении. Это не утверждение, что CPU/NMS разрешены интерфейсом соревнования; нейросетевой inference всё равно должен быть на LinQ.


## Контекст W1-03

Основания: [F025](#F025), [F026](#F026), [F027](#F027), [F028](#F028), [F029](#F029), [F030](#F030), [F031](#F031), [F032](#F032), [F033](#F033), [F034](#F034), [F035](#F035), [F036](#F036), [F037](#F037), [F038](#F038), [F039](#F039), [F040](#F040). Source scope и статус сохраняются.

## Карта операций: что сверять при graph surgery

Следующие expected checks — методические выводы из фактов, а не опубликованные измерения.

| Изменяемая область | Что сохранить | Диагностический вход и ожидаемая проверка |
|---|---|---|
| Opset / domain / custom op | IR; opset_import каждого domain; effective operator schema; типы входов и атрибутов; local functions | Schema inventory до/после. Если converter вставил Reshape/Transpose вокруг Softmax — не удалять их как «лишние». Структурная валидность обоих файлов плюс paired outputs. |
| Dynamic→static | Семантический порядок N,C,H,W; договорённый batch/resolution; внутренние shape tensors | На той же фиксированной форме original dynamic и specialized должны совпасть в согласованных допусках. Другую форму specialized обязан отвергать на внешнем входе; такой отказ ожидаем, а не деградация качества. |
| Resize | mode; coordinate_transformation_mode; nearest_mode; sizes/scales/roi; cubic/extrapolation; для новых схем antialias/axes/aspect policy | Ramp по X/Y, единичный импульс, шахматная решётка; odd H/W, нецелый scale, выходная сторона1. Проверять индекс максимума/границы и карту значений, не только shape. |
| Gather / Slice / Range | Rank и dtype индексов; axis; отрицательные индексы/steps; clamp; конечные границы | Тензор с уникальным значением в каждом элементе; scalar и vector index; отрицательный step; last index; пустой легальный результат. Проверять точное равенство индексных тензоров. |
| Transpose / Reshape / Flatten / Squeeze / Unsqueeze | perm; reshape shape; channel/candidate axis;−1/0; axes; memory order | Несимметричный `[1,3,5,7]` с кодом канала/координаты в значении: квадратный или константный вход способен скрыть ошибку. Поэлементное совпадение после явного inverse permutation. |
| Concat / Split | Порядок ветвей; axis; соответствие stride/head/class/channel | Разные константные метки в каждой ветви и разные длины: в выходе ожидаются те же сегменты в том же порядке. |
| Conv / Pad / BatchNorm folding | Веса, bias, group/depthwise, stride/dilation, pads/auto_pad; BN epsilon и inference statistics | Impulse у границ, odd spatial size, ненулевой bias; сравнить до/после fold на той же precision. Граница сместилась при одинаковом shape — проверить padding, а не начинать QAT. |
| Softmax / Sigmoid / Mul / Exp / ReduceSum | Точка применения активации; axis; broadcasting; stable formulation | Отличающиеся logits по каждой оси, отрицательные и большие значения; finite-mask. Сумма1 только вдоль оси Softmax; Sigmoid не обеспечивает сумму1. Нельзя заменять Softmax на независимые Sigmoid. |
| NMS / TopK / выходной decode | Формат/axis scores; thresholds; class handling; max_output; индексирование/порядок выходов | Несколько классов, overlapping boxes, пустые detections, равные scores, threshold boundary; сравнивать выбранные наборы индексов и далее детекции. Точные правила/допуски W1-04. |

Любая layout-трансформация должна перенести всю согласованную область: axis-aware операции, broadcast-константы, weights там, где изменён формат соответствующей операции, shape computation и boundary transposes. Нельзя просто изменить shape input с `[N,C,H,W]` на `[N,H,W,C]`, оставив стандартный Conv прежним. Если compiler сам перестраивает внутренний layout и контракт границ прежний, дополнительный ручной Transpose не нужен.

Замена unsupported op — отдельная математическая реализация. Примеры опасных сокращений: Slice вместо Gather без проверки индексов; Pad+Conv вместо Conv с auto_pad без проверки нечётных размеров; ручной Exp/ReduceSum вместо устойчивой Softmax без проверки overflow; clip вместо правильного padding; вынос NMS без воспроизведения его контракта. Совпадение на одном изображении не подтверждает общую эквивалентность.


## Пошаговая локализация расхождений

1. **Зафиксировать границы сравнения.** Вход — один и тот же сохранённый препроцессированный tensor с именем, dtype, shape, hash и параметрами preprocessing. Отдельно хранить real fixtures: промышленные кадры с мелкими СИЗ, дымом/бликами, окклюзиями, hard negatives, пустыми сценами. Синтетические индексные/ramp inputs диагностируют операции; representative fixtures проверяют применимость к задаче. Один набор не заменяет другой.
2. **Создать inventory до изменения.** SHA256 модели и external-data файлов; IR/opset domains; producer; input/output имена/типы/формы; последовательность узлов, domain/op_type/name; input/output edges; атрибуты; dtype/shape/hash initializers; subgraphs/functions. Порядок узлов/имена могут поменяться без изменения функции: графовый diff должен показывать и смысловые поля, не только текстовый protobuf diff.
3. **Минимальная структурная проверка.** `onnx.checker.check_model(model, full_check=True)`. Затем на копии `onnx.shape_inference.infer_shapes(model, check_type=True, strict_mode=True, data_prop=True)` и проверка полученных/неизвестных форм [[S022](SOURCES.md#S022), [S023](SOURCES.md#S023)]. Не отключать opset compatibility check ради «зелёного» результата. Ошибка custom domain может означать отсутствие схемы у checker, её нельзя автоматически объявить дефектом модели.
4. **Дешёвый контроль runtime без дополнительных optimizer passes.** Выполнить original и transformed ONNX в одной версии ORT на CPU с `ORT_DISABLE_ALL`, на идентичных feeds [[S025](SOURCES.md#S025)/S15]. Сначала сравнить количество/имена/shape/dtype outputs, маски NaN/Inf; для indices/shape integers — точное равенство. Для float логировать max/quantile abs error, relative error с явным near-zero handling, координаты худших элементов и их исходные значения. Thresholds устанавливает команда по baseline/рискам, а не onnxsim.
5. **Если выходы различаются, найти первую границу.** Извлечь подмодели через `onnx.utils.extract_model(input_path, output_path, input_names, output_names)` [[S039](SOURCES.md#S039)]. Сначала outputs backbone/neck/head; затем между соседними операциями проблемной ветви. Сравнивать одинаковые семантические точки, а не предполагаемый одинаковый порядковый номер слоя. При layout change применить документированное inverse permutation только для сравнения. При fusion сравнивать boundary fused block с unfused block; имена внутренних тензоров могли исчезнуть.
6. **Не путать накопление с источником.** Если входы блока уже расходятся, подать эталонный вход в обе реализации выделенного блока. Если после этого выход совпал — источник выше. Если нет — сохранить минимальный подграф, вход и атрибуты первого проблемного блока. Не разрезать If/Loop; получать необходимые промежуточные value_info, не угадывать shape/dtype.
7. **Отдельно включать runtime transformations.** На неизменном ONNX и тех же inputs пройти Disable→Basic→Extended→All. Сохранить каждый optimized graph через `SessionOptions.optimized_model_filepath`, сравнить inventory и outputs. Если первая потеря появляется на уровне Extended, не исправлять checkpoint до установления pass. `disabled_optimizers={"..."}` — внутренний API проверенной ORT версии, использовать только в закреплённом диагностическом окружении [[S042](SOURCES.md#S042)]; для LinQ эта команда неприменима без его SDK.
8. **Проверить влияние инструментирования.** Дополнительный output может блокировать fusion, поэтому «ошибка исчезла после добавления debug outputs» не доказывает исправление. Повторить на неизменённом deployable graph и compare block boundaries; хранить оба артефакта.
9. **Вернуться к реальному выходу.** После raw tensors сравнить decode и геометрию детекций/keypoints; затем W1-12/11 проверяют event outcomes. Успешный CPU replay доказывает эквивалентность именно в этом runtime, не поддержку LinQ.

Короткий пример конфигурации контрольной ORT-сессии (предлагаемый, не выполнен):

```python
options = ort.SessionOptions()
options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
session = ort.InferenceSession(model_path, sess_options=options,
                               providers=["CPUExecutionProvider"])
outputs = session.run(None, feeds)  # feeds = сохранённые tensor inputs
```

Основание — [S025](SOURCES.md#S025)/S15. Это не самостоятельный тест: необходимы обе модели, fixtures, сравнение output contract и отчёт о допусках. Shape helper [S041](SOURCES.md#S041) позволяет зафиксировать символическое измерение:

```text
python -m onnxruntime.tools.make_dynamic_shape_fixed --dim_param batch --dim_value 1 model.onnx model.fixed.onnx
```

Команда дословно соответствует документации; здесь `batch` — пример реального имени из модели документации, а не установленное имя нашего неизвестного ONNX. Выполнять только после inventory. Фиксация batch1 не означает разрешения менять разрешение/растягивать кадр. Никакие инструменты в ходе исследования не устанавливались.


## Допуск преобразования и решение «чинить или нет»

| Наблюдение при будущем тесте | Действие |
|---|---|
| Исходный ONNX и transformed совпадают; LinQ importer сообщает конкретную unsupported schema/shape | Уточнить версию/ограничение; минимальная адресная замена или специализация; снова сравнить. Правка оправдана подтверждённым ограничением. |
| Checker проходит, после simplification расходятся CPU raw outputs | Откатить; разнести folding/shape inference/optimizer passes; проверить check_n и input contract. Не переходить к INT8/QAT. |
| Изменились shape/axis/candidate order после Transpose/Reshape/Concat | Исправить layout/индексы и output adapter. Это структурно-семантическая ошибка. |
| Только optimizer-enabled runtime расходится | Установить первый плохой pass, сохранить reproducer; временно отключить pass при допустимой latency, закрепить версию. Переписывать модель необязательно. |
| Только FP16/fused реализация расходится, структура эквивалентна | Отдельная precision/fusion диагностика W1-06; не называть это автоматически INT8 calibration error. |
| Raw outputs совпадают, боксы/события нет | Передать decoder/preprocessing/tracking владельцам; graph surgery не обоснована. |
| ONNX shape inference оставил неизвестные промежуточные формы, а импортёр/исполнение поддерживают их | Оставить граф; отсутствие annotation не является доказанной ошибкой. |
| Нет фактического ограничения target, исходный граф проходит gate | Оставить исходник. Меньше обязательных преобразований — меньше незакрытых переходов в fidelity ladder. |

Каждый принятый патч сопровождается записью: причина и diagnostic evidence; model hashes до/после; script/tool commit; точные параметры; перечень изменённых узлов/атрибутов/констант; input contract; проверенные реальные/синтетические fixtures; raw и decoded differences; target placement/latency; решение и границы допуска. Случайный sanity PASS, representative-fixture PASS и target PASS отражать разными полями.


## Fallback и ограничения переноса на LinQ

ORT умеет разделять граф по EP capability; CPU fallback может помочь выделить unsupported часть [[S040](SOURCES.md#S040)]. Но `get_providers()` показывает зарегистрированные провайдеры, не полный placement. Требуются логи/profiling; «модель запустилась с ускорителем в списке» не подтверждает обязательный inference на LinQ. Вынесение NMS/decoder на CPU — архитектурный кандидат после подтверждения правил и интерфейса, а не установленная возможность текущего сервера.

Уже optimized под конкретный ORT/CPU/GPU граф не считать универсальным входом импортёра LinQ. Сначала portable ONNX, затем только требуемые изменения target compiler. Изученные bugs ORT не переносятся на LinQ и не дают универсального запрета fusion. Их польза — конкретные тесты boundary cases и разделение структурной/численной проверки.


## Контекст W1-04

Основания: [F041](#F041), [F042](#F042), [F043](#F043), [F044](#F044), [F045](#F045), [F046](#F046), [F047](#F047), [F048](#F048), [F049](#F049), [F050](#F050), [F051](#F051), [F052](#F052), [F053](#F053), [F054](#F054), [F055](#F055), [F056](#F056). Source scope и статус сохраняются.

## Модель → выход → decoder → готовая детекция

Обозначения: B — batch, A — число пространственных кандидатов после конкатенации уровней, C — число классов, K×D — число keypoints × размерность, M — число mask coefficients, Q — queries. «Raw» без уточнения запрещён: различать **сырые conv/logits**, **декодированный выход до NMS** и **готовый post-NMS output**. Типовые размеры ниже выводятся из кода, не измерены на LinQ.

| Семейство/версия | Фактический выход на указанной границе | Остаточная интерпретация | Готовая запись и критическая граница |
|---|---|---|---|
| YOLOv8/YOLO11 Detect, Ultralytics 8.3.230, обычный не-end2end, export без NMS | B×(4+C)×A; первые 4 — decoded cx,cy,w,h в input-pixel coordinates при обычном `xyxy=False`; далее class probabilities | Транспонировать в B×A×(4+C) только согласно contract; cxcywh→xyxy один раз; best-class или multi-label; NMS | N×6: xyxy, score, class_idx. Нет дополнительного умножения на objectness и повторного sigmoid/DFL |
| Та же Detect до `_inference` | По уровням B×(4R+C)×Hᵢ×Wᵢ; R=16 в этой реализации | Для каждой стороны softmax по R bins, математическое ожидание расстояния; anchor points + stride → box; sigmoid классов | Это отдельный decoder, не совместимый с уже decoded 4+C. Одинаковое название модели не определяет место graph cut |
| Ultralytics Pose 8.3.230 без NMS | B×(4+C+K·D)×A; decoded keypoints; при D=3 третий компонент sigmoid | NMS получает явное C; extra channels переносятся с выбранным кандидатом; reshape K×D, затем обратная геометрия | N×(6+K·D). Keypoint confidence не заменяет detection confidence; K, D, порядок суставов и flip permutation — из конфигурации |
| Ultralytics Segment 8.3.230 без NMS | Два выхода: B×(4+C+M)×A и prototype tensor | C задаётся явно; mask coefficients не являются class scores; сохранить prototype и согласовать индексы кандидатов | N×(6+M) плюс prototypes → masks штатным mask decoder. Первый ndarray rank≥3 недостаточен для выбора output |
| YOLOv5 v7.0 Detect export | B×A×(5+C), уже decoded cxcywh и sigmoid objectness/classes | score_c=obj×class_c; затем cxcywh→xyxy, threshold, NMS | YOLOv8 decoder на этом выходе сдвигает классы и теряет семантику objectness. Для нестандартной головы проверять код отдельно |
| Ultralytics end2end/v10-style head 8.3.230 | B×min(max_det,A)×6 после head postprocess/top-k; xyxy задаётся веткой decode, хотя docstring postprocess описывает xywh | Это уже scores/class index, а не C-channel probabilities; generic NMS обходит подавление | Не выводить семантику только по последней размерности 6. Отключение дополнительного NMS здесь связано с конкретной one-to-one моделью, а не со всеми outputs такого shape |
| torchvision FasterRCNN 0.24.0, обычный eval | List[Dict] по изображениям: boxes, scores, labels, уже postprocessed | Внутри RoI: decode, softmax, удалить background 0, class-wise NMS, global detections_per_img; результат геометрически возвращается моделью | Повторное YOLO decode/NMS и вычитание единицы из labels без карты классов запрещены; собственный ONNX wrapper может менять flatten/signature |
| Оригинальный DETR, commit 29901c5 | Dict pred_logits B×Q×(C+1), pred_boxes B×Q×4 | Softmax по C+1; исключить последний no-object канал; normalized cxcywh→xyxy; масштабировать исходными W,H | Штатный PostProcess без NMS. Добавление NMS меняет baseline, даже если уменьшает дубликаты |
| Ultralytics RTDETRDecoder 8.3.230 | B×Q×(4+C): decoded normalized boxes + sigmoid class scores | Его predictor делает cxcywh→xyxy, best-class threshold, sort/max_det, ×original W/H, без NMS | Это не DETR softmax/no-object и не YOLO BCN input-pixel layout. Predictor использует scale_fill=True; чужой letterbox обратный transform даст другой результат |
| MMPose 1.3.2 SimCC codec, применимый к соответствующим RTMPose-конфигурациям | Два массива N×K×Wₓ и N×K×Wᵧ, а не детекции | `get_simcc_maximum`, опциональный DARK refinement, деление на simcc_split_ratio; отдельная опциональная visibility ветка | K×2 и keypoint scores в пространстве входного crop; возвращать в кадр по affine/crop metadata. Конкретный RTMPose checkpoint/config должен подтвердить этот codec |

Граница применимости: это точные реализации, а не универсальные свойства всех моделей с названием YOLO/DETR/RTMPose. Новые YOLO head variants, rotated boxes, TensorFlow Lite Detection_PostProcess и vendor custom plugin требуют собственного контракта; их совместимость здесь не подтверждена. OBB нельзя подавлять обычным axis-aligned IoU/NMS. ONNX/operator support сам по себе не доказывает наличие нужного host decoder в сервисе LinQ.


## Таблица критических договорённостей

Это предлагаемый **manifest**, не существующий LinQ API. Его можно хранить JSON/YAML рядом с hash артефакта.

| Поле/договорённость | Что обязательно записать | Что отвергать до расчёта метрик |
|---|---|---|
| Provenance | checkpoint hash, архитектура/head class, library commit/tag, export args, graph hash | Неизвестную голову и несвязанные веса/manifest |
| Outputs | Все имена, dtype, shape/layout, dynamic axes, semantic stage каждого output; aliases только явные | Первый попавшийся tensor, восстановление оси по 84/85, silently ignored extra outputs |
| Quantized boundary | Является ли выход float/dequantized; для integer — scale/zero-point/axis от реального SDK | `astype(float)` вместо корректной dequantization, sigmoid над integer codes; параметры LinQ здесь неизвестны |
| Class schema | nc, ordered names, model_idx→dataset/event ID; background/no-object/objectness отдельно | COCO80_TO_91 для custom classes, классы из K·D/M extras, score вне оговорённого диапазона |
| Boxes | cxcywh/xyxy/yxyx/ltwh, normalized/input-pixel/original-pixel; stride, anchor point convention; graph decode included? | Повторный DFL/stride scaling, перестановку x/y, двойное undo-letterbox |
| Pose/masks | kpt_shape, joint order, xy confidence semantics, crop/affine IDs; mask coefficients/prototypes names | Смешивание людей после NMS; потерю выбранного candidate index; COCO17 как неявный default |
| NMS | In/out graph, implementation+version, class-aware/agnostic, multi-label, classes filter, strictness, conf, IoU, pre-top-k/max_nms, max_det | Разные политики у baseline и target, второй NMS поверх final outputs |
| Final cardinality | Ragged vs padded, valid count/mask, valid rows definition, empty output representation | Zero padding как объект; class_idx float без проверки целочисленности/диапазона |
| Ordering/ties | Score descending? deterministic secondary key? preserving source candidate index? | Сравнение по номеру строки без matching и объявленного порядка |
| Batch | Per-frame output alignment; shape-specific A; real frame count vs padded batch | Padded frames в журнале событий, cross-batch suppression, time-limit truncation как пустой кадр |

Схему классов нельзя надёжно восстановить по одному shape: B×A×6 может быть final detections, YOLOv5 nc=1 до NMS или YOLOv8 nc=2 после ошибочной смены оси. Даже C=84 не доказывает COCO semantics. Manifest вместе с graph/code observation является источником истины, форма — проверкой согласованности.


## Ограничения, контрпримеры и следующий шаг

1. **NMS вне графа — не универсальное production-решение.** Нужны фактические API сервиса, доступ к decoded outputs и разрешённый host processing. Если сервис отдаёт только final detections, можно сравнить этот stage, но нельзя заявлять проверку pre-NMS parity. Нейросетевой inference всё равно на LinQ.
2. **Декодирование в head не всегда переносимо на произвольный graph cut.** Поддержка Sigmoid/Softmax/Gather/Reshape/NonMaxSuppression у LinQ и точная доступность выходов неизвестны. Если compiler требует вырезать decode, host implementation необходимо сверять с конкретным head и shape/stride, а не добавлять generic YOLO decoder.
3. **Equal-score tie — реальная граница exact gate.** Незначительная numeric perturbation может поменять выбранного overlapping человека при практически совпадающих тензорах. Либо общий фиксированный NMS, либо объявленный deterministic policy в обоих путях; добавление epsilon по индексу само меняет near-ties и требует явного согласования.
4. **Class offsets требуют диапазонных предпосылок.** В [S045](SOURCES.md#S045) offset max_wh=7680, а в exporter [S018](SOURCES.md#S018) — нормализация/offset по числу классов. Проверять реальные coordinates, negative/out-of-frame decoded boxes и допустимый размер входа: магическое offset не является общим доказательством отсутствия межклассового overlap.
5. **Прочитанный linq-cv-bench — сторонний исходный код.** Его дефекты не доказывают дефект SDK, отсутствие custom output support или провал реального запуска. Не переносить известные helper probes соседей на наше исследование. Дату pinned commit 2026-04-03 сообщил соседний материал; наша повторная GitHub API проверка даты получила HTTP 403 rate limit, поэтому дата не считается независимо подтверждённой здесь. Сам raw-код именно указанного hash получен и прочитан.

Открытые вопросы, необходимые перед практической работой:

- Q-DEC01: какие точные checkpoint/head/task/nc/names/kpt_shape, версии и export flags будут выбраны?
- Q-DEC02: какие output tensors/names/dtypes/scales реально предоставляет LinQ artifact/service: conv logits, decoded pre-NMS или final detections? Доступен ли multi-output?
- Q-DEC03: где NMS, какие per-class/global limits и valid-count protocol? Кто применяет inverse geometry? Можно ли сохранить pre-NMS output для golden pack?
- Q-DEC04: фиксирована ли зависимость Ultralytics в выбранном adapter; исправлены ли shape/class mapping/output-name defects до запуска модели?
- Q-DEC05: какой policy baseline принят для multi-label, tie-equivalence, confidence/IoU, crowd cases и event thresholds? Эти параметры не заданы кейсом.

Следующее действие: получить реальный model manifest и один named-output dump, проверить contract E-DEC01/06, затем same-tensor decoder/NMS pack E-DEC02–05 и paired replay E-DEC07. Если output только final, явно ограничить доказательства этой границей. До этого нельзя интерпретировать разницу mAP/event recall как деградацию квантования.


## Контекст W1-05

Основания: [F057](#F057), [F058](#F058), [F059](#F059), [F060](#F060), [F061](#F061), [F062](#F062), [F063](#F063), [F064](#F064), [F065](#F065), [F066](#F066). Source scope и статус сохраняются.

## Геометрический ledger и два разных эталона

Для каждого кадра сохранять: source/stream/frame ID, source PTS и time_base, capture/receive time раздельно; coded size, decoded size, SAR, rotation/mirror, canonical size; crop origin/extent; фактические resized W/H; pad left/top/right/bottom; output shape/layout; dtype/channel order; последовательность normalization; affine и inverse; coordinate convention и единицы выходов. Для pose добавить actor ID, bbox center/scale, crop rotation, codec/input dimensions, confidence/visibility convention. Для batch — собственный ledger каждого изображения, а не первый scale на весь batch.

Для axis-aligned resize/crop/letterbox геометрия непрерывных bbox boundaries имеет вид `x' = sx*(x−crop_x)+left`, `y' = sy*(y−crop_y)+top`. Обратное — вычесть pad, разделить по соответствующей оси и вернуть crop offset. При rotate/mirror преобразовывать все углы бокса, затем брать envelope; точки сохраняют identity. Композицию преобразований выполнять в правильном порядке и обращать целиком. Clip — после перевода в нужную frame space; целочисленное округление — только на оговорённой границе отображения/индексации, если reference не требует иного.

**Граница:** этот общий геометрический ledger и **точная воспроизводимость существующего predictor — разные задачи**. Ultralytics ratio использует nominal scalar r, хотя растровая высота округляется. Не подменять reference r на `rounded_height/H` при восстановлении только одной ветки. Формула центров пикселей Resize также не является автоматически формулой перевода bbox boundaries. Нужны отдельные проверки pixel values и output geometry.


## Диагностический pack: состав и expected checks

Спецификация сохранена в `MATERIALS_W1_05/DIAGNOSTIC_SPEC.json`. Файлы изображений/видео не генерировались. Ниже ожидаемые результаты аналитические, а не PASS выполненного теста.

| ID | Fixture и условия | Expected checks / что локализует |
|---|---|---|
| G01 | Lossless RGB 853×481, асимметричные углы, чистые красный/зелёный/синий квадраты; float ramps; fixed centered letterbox640, auto=False, scaleup=True | r=640/853≈0.7502930832; resize640×361; L/T/R/B=0/139/0/140; output640×640. Красный raw RGB [255,0,0] при RGB /255 даёт [1,0,0]; uint8→float без деления даёт 255 и FAIL. Pad114→114/255≈0.4470588 при таком профиле. Не использовать JPEG для побитового цветового эталона. |
| G02 | Portrait481×853, те же маркеры | resize361×640; pad139/0/140/0. Ловит H/W interchange, транспозицию и реконструкцию padding из неверной оси. |
| G03 | G01 с auto=True,stride32; затем single-shape/mixed-shape batch; `.pt`/non-pt wrappers | auto размер640×384, pad0/11/0/12; auto=False640×640. Сравнить shape и tensor bytes ещё до inference. Static engine ожидающий640×640 должен отвергнуть384 height, а не молча растягивать без записи. |
| G04 | Synthetic floating boxes и named keypoints поверх G01: fractional coords, границы, box[-3,−2,855,483], 1×1 и zero-area; точка с visibility=0 | Сначала forward/inverse float без clip для interior; затем ожидаемый clip [0,0,853,481] для boundary box. Проверить degenerate policy отдельно; confidence/visibility не менять геометрией. Прогнать одинаковые fabricated outputs через оба postprocessor без модели; точки и боксы проверять раздельно. |
| G05 | Tiny17×13→11×7: impulse, checkerboard, x/y ramps; отдельный output-axis length1 | Сравнить tensor arrays/interior/edge pixels, фактический resize profile и schema, не только thumbnails. Для оси17→11, output u=3: half_pixel даёт input54/11≈4.90909, asymmetric51/11≈4.63636, align_corners4.8. Это различные координаты выборки при одинаковом output size. |
| G06 | Одна асимметричная сцена: физически повёрнутый растр; тот же coded raster + display rotation90; mirror; SAR≠1 | После выбранной канонизации orientation одинаковая ровно один раз, размеры90° меняются местами; ROI/overlay/annotations находятся в этой же frame space. Семантика знака90° устанавливается по угловым маркерам, не угадывается из имени metadata. Сравнивать семантическую ориентацию; lossy видео не обязано иметь равные bytes. |
| G07 | Клип с вшитыми frame IDs и PTS[0,40,80,200,240,1240] ms, коротким событием и отдельным reconnect epoch | Δt=[40,40,120,40,1000] ms; фиксировать фактический selected ID list; source-time события не вычислять по времени arrival/inference. Duplicate PTS, пропуск, out-of-order и missing PTS должны быть видимыми состояниями. Одинаковый frame index после независимого decoding не доказывает одинаковый кадр. |
| G08 | RTMPose actor crop: фиксированный bbox, затем сдвиг center/scale, поворот crop, точки с идентичностью left/right | Проверить affine landmarks и exact configured inverse/decoder, crop ledger на каждого actor; upstream detector bbox заморожен. Полный detection→pose повторить отдельно: изменение crop способно объяснить pose drift при неизменной pose модели. |

Для G05 правильная арифметика half_pixel при 17→11, u=3: `(3+0.5)*17/11−0.5 = 54/11≈4.90909`; asymmetric `51/11≈4.63636`; align_corners `3*16/10=4.8`.

Для G04 отдельный аналитический counterexample: theoretical keypoint pad `(640−481*640/853)/2≈139.55451348`, box pad139. Для одного fabricated interior y difference обратных формул `0.55451348/r≈0.7390625` исходного пикселя; дополнительный `.round()` бокса — отдельная ступень. Это не означает, что реальные keypoints должны совпадать с box corner: тест специально подаёт одну известную координату в обе формулы.

Дополнительный профиль crop/stretch: у center-crop отсутствующий участок исходного изображения восстановить невозможно; ожидаемый результат outside-crop — не «нет детекции модели». Для stretch проверить независимые sx/sy; для предварительного downscale записать оба resize, потому что resize(A→B→C) по пикселям в общем не равен resize(A→C). Малые объекты на с.5 кейса делают этот выбор существенным, но численной потери recall здесь не измерено.


## End-to-end parity checklist и порядок допуска

1. **До модели:** сохранить исходные bytes/hash, decoder/backend/build/options; выбрать один orientation/SAR policy; сопоставить frame IDs/PTS; получить decoded canonical frames. Идентичные bytes входного файла не гарантируют идентичный кадр после разных decoder.
2. **Preprocess contract:** проверить H/W, RGB/BGR, layout/contiguity, dtype, диапазон; порядок `/255`, mean/std, quant input scaling; наличие Cast/Div/Sub/Resize/Pad/Transpose в exported graph и wrapper. Normalization должен иметь одного владельца. Для уже quantized input нельзя автоматически делить integer на255 — нужен выданный quantization contract. Возможности LinQ здесь неизвестны.
3. **Pixel parity:** uint8 стадии одной реализации — exact equality; тензоры одинакового dtype одной последовательности — exact where deterministic. При намеренной смене библиотек/precision сохранять max/mean absolute difference, map по каналам/границам; допуск выбирать по reference, не придумывать универсальный epsilon. Тест на mean/std считать из фактического config: `(channel/255−mean_c)/std_c` только если именно такой порядок установлен.
4. **Model-only:** один готовый тензор, одинаковая shape/batch, разные runtime; сырые выходы перед decoder/NMS/clip. Если интерфейс сервера принимает только JPEG/video, model-only parity недоступен без серверного debug dump — это локализованное препятствие, не автоматический FAIL модели.
5. **Output-only:** одинаковые fabricated boxes/keypoints/logits подать обоим decoder; freeze thresholds/class mapping/NMS отдельно с W1-04. Проверить координаты до/после inverse, clip и round. Это отделяет export/precision от геометрии.
6. **Full path:** только после предыдущих ступеней replay одной последовательности и общий decoder/tracker/rules. Проверить ROI entry, footpoint и overlay в canonical source frame, event time по source clock. Для физической floor geometry дальнейшая homography применима только к своей плоскости — соседний отчёт является зацепкой, количественные выводы не перенесены.

Симптомы: перестановка каналов меняет цветные patches; почти постоянный translation указывает на pad/crop; ошибка, растущая по координате — на scale/axis; зеркальная поза — rotation/mirror/left-right convention; drift только pose — crop/codec/inverse; разный recall коротких событий при похожих кадрах — сначала проверить sampling/PTS. Это диагностические гипотезы, не взаимно исключающие доказанные причины.


## Контекст W1-06

Основания: [F067](#F067), [F068](#F068), [F069](#F069), [F070](#F070), [F071](#F071), [F072](#F072), [F073](#F073), [F074](#F074), [F075](#F075), [F076](#F076), [F077](#F077), [F078](#F078). Source scope и статус сохраняются.

### Числа формата — ориентир представимости, не допуск переноса

Из [S072](SOURCES.md#S072) Table 1, округлены как в статье. Unit roundoff — характеристика отдельного округления при соответствующей модели арифметики; не предел накопленной ошибки сети.

| Формат | Unit roundoff u | Минимальное положительное normal | Минимальное positive subnormal | Примерный maximum finite |
|---|---:|---:|---:|---:|
| FP32 | 5.96e-8 | 1.18e-38 | 1.40e-45 | 3.40e38 |
| FP16 | 4.88e-4 | 6.10e-5 | 5.96e-8 | 6.55e4 |
| BF16 | 3.91e-3 | 1.18e-38 | 9.18e-41 | 3.39e38 |

Вывод: BF16 может помочь при overflow FP16, одновременно сильнее округляя близкие scores. Фактическая обработка subnormal/flush-to-zero и точность math kernels на LinQ неизвестны; таблица формата этого не устанавливает.


## Диагностика: симптом → минимальное различающее наблюдение

Следующая таблица — **методический вывод**, а не опубликованные измерения. Изменение конфигурации допустимо только если соответствующая операция поддерживается фактическим runtime.

| Этап / симптом | Кандидат причины | Минимальная диагностика | Исправление и оставшаяся граница |
|---|---|---|---|
| После dtype conversion исчезли детали / scores стали равны | Округление; underflow; clipping конвертера | Initializer/Constant diff до запуска; count изменённых значений, signed zeros, диапазоны; сопоставить с чистым round cast | Исправить параметры преобразования либо сохранить чувствительную ветвь в FP32; оценить target заново |
| Появились NaN/Inf | Overflow промежуточного sum/matmul/square/exp; некорректный input | Первое расхождение finite mask по семантическим границам; диапазоны входа/выхода; референсный вход блока в обе реализации | FP32 island / иной поддержанный kernel / стабильная формула. Финальный finite output не исключает промежуточный сбой |
| Все значения конечны, выросли нули или точные 0/1 вероятности | Underflow/округление/насыщение; двойной sigmoid | Снять pre-activation logits и probabilities; проверить output schema до численной гипотезы | Не добавлять sigmoid, пока не установлен контракт; после FP32 вычисления итоговый cast тоже может потерять хвосты |
| Только optimized/fused граф расходится | Новый порядок округлений/редукции; иной kernel; compiler defect | Тот же dtype/input и controlled fusion/optimization ablation; сравнить границы блока | Откат pass или precision constraint; изменение debug outputs способно само отключить fusion |
| Первый FP32 alternate-runtime diff до FP16 | Backend math/TF32, экспорт, fusion, layout/schema | Сверить exact tensor input, фактический compute policy и FP32 unsimplified graph | Не исправлять PTQ/calibration, пока причина раньше precision-stage |
| Дрейф между повторами одного артефакта | Нондетерминизм, state, Dropout/train mode, динамическое batching | `eval`, фиксированные входы и state reset; повторные runs в одном стеке, отдельно fresh process | Изолировать state/random/kernel selection. Идентичный seed не делает разные платформы идентичными |
| Raw tensors близки, пропадают детекции | Confidence/top-k/NMS граница; tie | Before/after threshold masks, retained candidate IDs, score margins, IoU-to-NMS-threshold | Согласованный decoder/tie policy; не подгонять threshold под test |
| Координаты близки, мелкий объект не матчится | IoU чувствителен к масштабу; rounding/clip; неверная geometry | Matched boxes в исходных pixels; endpoint drift и unmatched списки; tiny-object slice | Исправить coordinate convention/precision или модель; средний IoU крупных людей проблему скрывает |
| Pose немного дрожит, зона/событие меняется | Keypoint validity, rule threshold, actor association | Координаты + visibility до/после decoder, margin правила, causal sequence replay | FP32 чувствительная ветвь/decoder, если поддержано; затем отдельный event gate |

Нельзя объяснять sigmoid лозунгом «любое малое изменение logits усиливается». Наш математический вывод: в вещественной арифметике `sigmoid'(z)=p(1-p)<=1/4`, то есть абсолютная локальная чувствительность ограничена. Практический риск — конечная арифметика exp, потеря малых вероятностей, округление около 0/1 и последующее дискретное решение. Softmax аналогично требует отличать математическую чувствительность, алгоритм вычисления и argmax/threshold. При logits, уже совпавших после округления, FP32 softmax не восстановит исходный ranking.

Наш вывод об арифметике fusion: выражения `round(round(a*b)+c)` и `round(a*b+c)` могут различаться, поскольку fused multiply-add убирает промежуточное округление. Это может **улучшать** локальную точность, поэтому любое отличие fused/unfused не есть автоматически регрессия. При сложении величин с разными знаками cancellation делает относительную ошибку малого остатка большой; порядок reduction тогда особенно важен. FP32 accumulator также не восстанавливает разницу уже округлённых FP16/BF16 inputs и не устраняет финальное округление output. Нужен независимый outcome-check; ближайший к одному runtime вариант не обязательно ближе к математической функции или GT.


## Как читать метрики и выбирать допуски

Все рекомендации этого раздела — проектируемый метод. Не получены распределения ошибок, позволяющие назначить числа.

| Метрика | Что сохранять | Что она не доказывает |
|---|---|---|
| Max absolute error | Значение, index/sample/channel, единицы, reference/target значения; mean/quantiles отдельно | Один максимум не описывает долю ошибок; общий максимум смешанных logits и pixel boxes бессмысленен |
| Relative error | Явную формулу; near-zero bin отдельно. Если используется `abs(diff)/max(abs(ref), scale_floor)`, scale_floor обосновать и записать | Огромная ошибка относительно почти нуля может быть малой абсолютной; большой denominator маскирует важный drift |
| Fraction exceeding tolerance | Знаменатель, конечные элементы отдельно, per-head/per-class slices | Маленькая доля может содержать весь редкий критичный класс; NaN не прятать в усреднение |
| Cosine similarity | Нормы обоих векторов, нулевые нормы как отдельный случай; отдельно heads/channels | Для `target=c*reference`, c>0, cosine равен 1 даже при изменившихся confidence; фон/крупные активации доминируют |
| Box IoU / IoU drift | Согласованный matching и unmatched counts; class-aware и диагностический class-agnostic варианты; pixels и size slices | Среднее matched IoU игнорирует пропавшие объекты; IoU двух runs не есть IoU с GT |
| Class flip | Candidate identity/matched object, top-1/top-2 margin, class-specific counts | Процент совпадений на фоне не доказывает recall нужного класса |
| Keypoint drift | Pixels на original frame; normalized-by-person scale отдельно; visibility/validity changes | Среднее по всем суставам скрывает единственную опорную точку правила |
| Event delta | Missed/late/wrong actor/duplicate/false alerts, denominator/exposure и timestamps | Согласие с source не доказывает correctness без независимого GT |

Предлагаемая процедура назначения численных бюджетов:

1. **Разделить сравниваемые значения.** Для каждого semantic output задать schema, units, shape, dtype, reference, режим flatten/matching. Сначала finite mask и structural invariants, затем ошибки; не разрешать `equal_nan=True` скрывать invalid outputs.
2. **Измерить собственную повторяемость baseline.** Повторы на неизменном golden pack и окружении показывают noise envelope. Если уже source нестабилен, сначала локализовать; нельзя автоматически расширить acceptance до этой нестабильности.
3. **Назначить budget из задачи.** Отдельно допустимая геометрия, class/confidence, pose, critical-event recall, false alerts и latency. Решение подписывает владелец качества. Эмпирический tensor percentile не заменяет риск-решение.
4. **Привязать numeric к решениям.** Для threshold `t` писать margin `abs(score_ref-t)`, для argmax — gap двух лидеров, для NMS — расстояние IoU до threshold. Прогнать near-boundary subset и остальную выборку отдельно.
5. **Проверить proposed budgets на development split.** Подбор precision policy и численных допусков проводится здесь; независимый held-out split не используется для подгонки. Сохранять все решения, в том числе failed.
6. **Заморозить budgets и policy.** На held-out выполнить paired detection/pose и sequence evaluation; неопределённость считать с учётом коррелированности кадров/камер совместно с W1-12. Пока precision artifact не прошёл оба уровня, численный PASS остаётся диагностическим.

Для одного threshold наш достаточный математический критерий: если известна **покомпонентная** граница `abs(score_target-score_ref)<=epsilon` и `abs(score_ref-t)>epsilon`, знак решения сохраняется. Для top-1 — достаточен исходный gap `>2*epsilon` при такой границе на каждый class score. Эти условия не универсальные допуски: нужно доказать bound, включить арифметику decoder и отдельно обработать ties/NaN. Квантиль ошибки bound для каждого объекта не доказывает. Для NMS цепочка ranking и подавлений требует отдельного replay.

**Наглядные контрпримеры, аналитические, не наши тесты:** значения по разные стороны любого threshold могут быть сколь угодно близки; пропажа единственного bbox маленького телефона почти не изменит cosine всего output; один изменённый сустав может пересечь линию зоны; потерянный кадр в правиле «несколько подтверждений» может сбросить накопленное состояние. Поэтому tensor allclose и одинаковый mAP не доказывают одинаковые события или отсутствие дублей.

Для двух одинаковых квадратных боксов со стороной `w`, сдвинутых только по горизонтали на `d`, `0<d<w`, геометрически `IoU=(w-d)/(w+d)`. Один и тот же pixel drift даёт разные IoU для разных размеров. Это аналитическая иллюстрация потребности size slices, не опубликованный эффект конкретной модели и не норма допустимого смещения.


## Переносимость и границы реализации

Метод applicable не только YOLO: у torchvision detection отдельно сравнивать proposal/ROI/class/box outputs, у DETR/RT-DETR — query logits/boxes и background/no-object interpretation, у pose — координаты/visibility/heatmaps по реальному контракту. Это диагностические точки, не обещание возможности выгрузить их любым SDK. Для attention-моделей дополнительно фиксировать выбранный SDPA/backend; из одного dtype файла нельзя вывести фактическую математику. Детали конкретных checkpoint/output signatures принадлежат W1-02/04.

LiteRT CPU-контроль с FP16-хранением и FP32 arithmetic [[S074](SOURCES.md#S074)] полезен для отделения округления весов от low-precision исполнения. ORT mixed precision [[S071](SOURCES.md#S071)] — возможный инструмент подготовки, если его версия/EP доступны; найденная им policy не переносится автоматически на другой compiler. Нельзя считать ORT default block list каталогом чувствительности модели или поддержки LinQ.

Для LinQ неизвестны FP32/FP16/BF16 support, внутренний accumulator, subnormal semantics, доступность raw/intermediate outputs и управление fusion. В режиме полного SDK E02–E05 можно реализовать в пределах его реального API; в режиме ограниченного сервера доступны лишь вход/выход и sequence checks; при готовой модели без исходных весов checkpoint fidelity не устанавливается. CPU+TPU partition и upload custom models не считаются данным интерфейсом. Никаких придуманых LinQ-команд здесь нет.


## Контекст W1-07

Основания: [F079](#F079), [F080](#F080), [F081](#F081), [F082](#F082), [F083](#F083), [F084](#F084), [F085](#F085), [F086](#F086), [F087](#F087), [F088](#F088), [F089](#F089), [F090](#F090). Source scope и статус сохраняются.

## Проверенные реализации и границы

| Объект | Реально доступное в прочитанном пути | Практический выбор и граница |
|---|---|---|
| ORT, pinned v1.22.0, Python static quantizer | `quantize_static`, QDQ/QOperator; `per_channel`, activation/weight types, node exclusions, symmetry через options. MinMax, Entropy, Percentile. | Для ONNX удобно выделять влияние quantizer на одном float graph. Проверять конкретный EP и kernel coverage. Получить QDQ-файл недостаточно для утверждения INT8 execution. |
| ORT v1.22.0 calibrators | MinMax: глобальные extrema либо moving average; Entropy: histogram и поиск KL; Percentile: histogram clipping. Дополнительный `Distribution` относится к float8-сценарию. | Не включать Distribution в список альтернатив INT8. В factory Percentile default 99.999, хотя docstring пишет 99.99: задавать эффективные параметры явно. |
| OpenVINO docs 2025 + NNCF v2.17.0 | `nncf.quantize`: PERFORMANCE — symmetric W/A; MIXED — symmetric weights и asymmetric activations. Advanced API позволяет отдельно задавать quantization/range parameters для W/A. | MIXED здесь **не** означает смесь FP16/INT8. Target constraints могут ограничивать параметры; сравнивать фактический graph, а не название preset. |
| NNCF v2.17.0 range estimator | Статистика внутри sample: min/max/abs-max/quantile и др.; агрегатор между samples: min/max/mean/median и др.; готовые MINMAX, MEAN_MINMAX, MEDIAN_MINMAX, MEAN_QUANTILE. | Среднее minima/maxima отличается от глобальных extrema; mean quantile отличается от percentile объединённой гистограммы ORT. Фиксировать обе ступени. |
| TFLite/LiteRT, TensorFlow v2.20.0 calibration path | `_feed_tensors` подаёт representative inputs в C++ wrapper; просмотренный `MinMax::Update` накапливает extrema. В официальном full integer flow — representative dataset, integer-only ops restriction и I/O dtype. | В этом интерфейсе не установлен публичный переключатель Entropy/Percentile/MSE. Не выдумывать его по аналогии с ORT. MLIR/другие внутренние пути могут отличаться; фиксировать actual converter configuration. |
| TFLite INT8 op specification | Conv weights symmetric per-axis с zero-point=0; activations per-tensor с допускаемым ненулевым zero-point. Conv axis=0, Depthwise axis=3; bias INT32 с сопряжённым scale. | «Все symmetric» и «везде per-channel» здесь не взаимозаменяемые варианты. У каждой операции собственные ограничения. |

**Weight-only не тождественно static activation+weight INT8.** OpenVINO `compress_weights` сохраняет float activations и представлен прежде всего как путь для LLM. ORT blockwise INT4/UINT4 поддерживает конкретные constant-input MatMul/Gather, со своими форматами/операторами; это не автоматическое ускорение CNN Conv. В TFLite tutorial dynamic range начинается с quantized fixed parameters без representative set, а full integer требует диапазонов intermediates. Нельзя считать weight-only диагностическую модель доказательством пригодности integer-only target. Алгоритмы data-aware weight compression могут требовать данные даже при float activations; «не нужна activation range calibration» не равно «никакие данные никогда не нужны».

**MSE**: в проверенных публичных селекторах ORT calibration method, NNCF range estimator и рассмотренном TFLite representative path отдельный generic MSE-calibrator не установлен. Поэтому MSE здесь — допустимая диагностическая ошибка между float/dequantized tensors, но не предлагаемое имя API. Не утверждаем отсутствие MSE-оптимизации во всех версиях, внутренних алгоритмах NNCF или сторонних quantizers. Для её добавления нужен точный backend/version/function и проверка результата target compiler. Аналогично PyTorch observer с похожим названием нельзя подменить им реально используемый calibrator.


## Как выбрать calibration subset за ограниченное время

Следующее — **проект протокола**, не результаты выполненного эксперимента.

1. Составить manifest доступных исходных клипов: camera/site/дата-смена/scene, timestamps/PTS, preprocessing version и file hashes. Сначала разделить группы, затем извлекать кадры. Для оценки нового времени на известных камерах держать будущие смены/эпизоды; для оценки новой камеры дополнительно нужен holdout камеры/площадки. Эти два утверждения обобщения различать.
2. Сохранить calibration pool отдельно от tuning clips и sealed test. Дубликаты и near-duplicates искать внутри и между splits. Ни один кадр эпизода sealed test не брать для диапазонов, выбора количества/percentile, ignored_scope, threshold или «только просмотра ошибок». Повторная адаптация после test требует нового независимого test либо явной маркировки exploratory результата.
3. В calibration pool выделить strata: камеры и геометрия; день/ночь/тени/блики; дым/пар/пыль; пустая площадка и обычная работа; расстояние/размер человека и СИЗ; окклюзии/число людей; позы и быстрые переходы; hard negatives вроде бликов вместо огня, руки у лица без телефона, обычного наклона вместо падения. Для DETR/RT-DETR учитывать crowded scenes и query competition; для pose — распределение crops/scale/visibility. Это требования покрытия, не обещание конкретного quantizer.
4. Отбирать temporally spread representatives; не платить бюджетом за сотню почти одинаковых кадров одной камеры. Rare safety scenes включать при наличии в разрешённом calibration pool, но оставлять независимые эпизоды тех же типов для tuning/test. У обычного background тоже должен быть вклад: clipping ложных активаций на нём может изменить FP/hour.
5. Сделать базовый natural-frequency набор и отдельный coverage-oriented набор **одинакового N**. Последний намеренно перепредставляет редкие strata; не называть его репрезентативным по эксплуатационной частоте. Разметка классов помогает coverage audit, но PTQ калибрует tensors, а не class priors напрямую.
6. Сформировать заранее детерминированные вложенные размеры N₁<N₂<N₃ в рамках реально доступного времени, добавляя новые независимые клипы/условия. Числа выбрать по стоимости одного calibration pass и покрытию, записать до просмотра оценок. Считать не только samples, но и cameras/clips/episodes/minutes/unique frames. Для batch loader явно установить, означает subset_size картинки или элементы loader в выбранном backend.
7. Повторить маленькие/средние наборы с заранее зафиксированными seeds/выборками. Остановку определяют стабильность tuning-метрик на опасных strata и диапазонов при добавлении независимых условий, стоимость и оставшееся покрытие. Плато общей mAP не закрывает пустой rare slice. Если ресурсов на повторения нет, прямо указать неизмеренную вариативность выбора subset.


### Почему больше/разнообразнее может ухудшить PTQ

При global MinMax добавление экстремального, но валидного кадра расширяет range: уменьшается clipping на нём, но увеличивается шаг квантизации остальных значений. Не относящиеся к deployment данные, неверная нормализация, corrupt кадры или искусственные сцены могут расширить его без практической пользы. Percentile/entropy могут лучше описать массу распределения, при этом обрезать активации редкого критического объекта. При mean/quantile aggregation важны доли strata: oversampling пустых кадров или одной камеры меняет итог, даже если N вырос. Эти механизмы — выводы из описанных алгоритмов; величина вреда для наших моделей неизвестна.

И наоборот, маленький «чистый» набор может случайно дать хорошую среднюю mAP, не представляя ночную камеру/опасную позу. Более широкий pool может обнаружить проблему и снизить численную метрику на tuning, хотя лучше отражает реальную эксплуатацию. Нельзя выбросить валидный опасный кадр только потому, что после его добавления mAP ухудшилась: проверить replay ошибки, clipping/sensitivity и target constraints, а затем выбирать recovery. Synthetic/augmented inputs — отдельный ablation; не добавлять в базовую calibration незадокументированные train augmentations.


## Deliberate paired matrix: изменения, которые можно интерпретировать

Единая платформа каждого блока: один checkpoint, input shape/batch, frozen float graph/fusions, ordered input bytes, preprocessing, decoder/NMS thresholds, class map, tracker/time rules, runtime/version/EP и оценочный manifest. Сравнивать **все кандидаты на тех же tuning clips и GT**. Между runtime блоками сначала свой float baseline; raw ORT–OpenVINO delta не является чистым эффектом calibration.

| Блок | Парные варианты | Что фиксировать | Вывод и ограничение |
|---|---|---|---|
| A. Export control | source float ↔ exported float | Те же model inputs и decoder | Пока float gate FAIL, PTQ-рецепт не выбирать: quantizer не объясняет export error. |
| B. Range method | ORT MinMax ↔ Entropy ↔ несколько заранее заданных Percentile; отдельно NNCF global ↔ mean-minmax/mean-quantile | Тот же calibration manifest/N/order/batch, W/A scheme и scope | Это эффект range estimator внутри одного backend. Не смешивать с bias correction или layer exclusions. |
| C. Coverage | natural-frequency ↔ stratified coverage того же N | Один method, target scheme и compute budget | Устраняет confounding «больше данных»; изменить только selection policy. |
| D. Size | вложенные N₁ ↔ N₂ ↔ N₃ одной policy | Один method, одно правило allocation, записанные additions | Показать, какие новые камеры/условия добавлены; эффект N всё равно связан с добавляемым содержимым. |
| E. Rare/hard negatives | базовый ↔ замена части кадров rare/negative при том же N; отдельно добавление этих кадров | В варианте замены неизменен N, в добавлении явно другой N | Разделить пользу coverage и бюджет. Не удалять rare slice из оценки ради выигрыша средней метрики. |
| F. Variability/order | независимые заранее заданные subsets; отдельно перестановка ровно тех же samples | Все PTQ options и оценка | Сначала sensitivity к выборке; для moving average отдельно проверить order и chunking. Перестановка не должна одновременно менять subset. |
| G. Scheme | per-tensor W ↔ per-channel W; symmetric A ↔ asymmetric A | Тот же subset/method/graph, одна переменная за сравнение | Выполнять только поддерживаемые комбинации; недопустимый target вариант отмечать UNSUPPORTED, не quality FAIL. |
| H. Recovery | выбранный PTQ ↔ bias correction/исключение выявленной sensitive области | Тот же tuning pack и остальные settings | Отдельный эффект recovery, согласовать с W1-08/09; проверить compile coverage и latency. |
| I. Target | выбранная модель до compiler ↔ LinQ compiled execution | Входные bytes и postprocess contract | Проверяет перенос; чужой backend не доказывает сохранность LinQ. При встроенном quantizer зафиксировать его параметры как новый вариант. |

Не запускать полный декартов продукт. При жёстком времени выполнить A, B с одной неизменной calibration, C для двух лучших рецептов, затем D/F для устойчивости; G/H только по диагностике. Финалистов отбирать по заранее объявленным safety constraints на tuning, затем фиксировать recipe и один раз раскрывать test. Другой порядок допускается как заранее записанное изменение плана, а не задним числом после test.

Причинность ограничена интервенцией: улучшение при единственной смене manifest на тех же входах/GT поддерживает вывод о **данной selection policy**. Оно не доказывает, что помог именно редкий класс: одновременно могли измениться освещение и расстояния. Для этого нужен matched replacement внутри сопоставимых strata либо отдельный ablation. Не считать тысячи коррелированных кадров тысячами независимых повторов: неопределённость оценивать парно по клипам/эпизодам, с учётом камеры, а не независимо по кадрам. Промежуточный tensor MSE не заменяет causal evidence на event outcomes.


## Рецепты по условиям

- **CNN detector/pose с поддерживаемым INT8 target:** сначала float parity, затем per-channel symmetric weights и допустимая target activation scheme; небольшой matched comparison MinMax и histogram clipping, если реализованы. Small-object/pose/event slices обязательны, иначе рецепт не доказан для СИЗ/падения. Weight per-tensor оставлять контрольным или target-constrained вариантом.
- **Модель с non-ReLU/асимметричными activations, например Transformer head:** не переносить CNN recipe автоматически. В OpenVINO начать с допустимого MIXED; для ORT отдельно проверить symmetry в фактическом EP. `model_type=Transformer` применять по документированному совместимому backend и модели; название RT-DETR само по себе не доказывает applicability всех BERT-настроек.
- **Экстремальные lighting/outliers:** не обрезать всё «для красивой средней ошибки». Отдельно MinMax и доступный clipping method, natural/coverage calibration и critical-slice checks. Если полезные редкие активации обрезаются, проверить target-supported sensitive-layer recovery.
- **TFLite full integer:** использовать representative inputs с реальной preprocessing и input signatures; принудительно ограничить INT8 builtins, если target этого требует, проверить I/O scales/zp и отсутствие float fallback. Не внедрять неподтверждённый «KL parameter». Edge TPU в tutorial — другой ускоритель, не LinQ.
- **Нет representative domain data:** float/weight-only diagnostic допустимы как временные результаты, но заявлять готовую W/A PTQ безопасность нельзя. Лучше получить разрешённые production-like calibration clips, чем считать generic COCO или synthetic frames доказанной заменой.
- **PTQ не проходит критические slices:** локализовать слой/decoder/loader, проверить ignored scope/коррекции при доступной поддержке, затем передать W1-08/09 с ошибочными golden fixtures. Не арендовать GPU и не начинать QAT только из-за среднего расхождения до этих проверок.


## Контекст W1-08

Основания: [F091](#F091), [F092](#F092), [F093](#F093), [F094](#F094), [F095](#F095), [F096](#F096), [F097](#F097), [F098](#F098), [F099](#F099), [F100](#F100), [F101](#F101), [F102](#F102), [F103](#F103), [F104](#F104), [F105](#F105). Source scope и статус сохраняются.

## Как выбирать метод по симптомам

Это инженерные выводы и предлагаемые проверки, не выполненные эксперименты.

| Симптом после корректной FP32-цепочки | Первый кандидат | Что должно стать лучше | Контрпример/ограничение |
|---|---|---|---|
| Постоянный средний сдвиг выходов отдельных каналов при квантовании весов | Empirical bias correction | Mean error каналов и downstream метрика | Нулевое среднее не означает малую дисперсию; output clipping остаётся |
| Сильный разброс диапазонов каналов соседних Conv | Поддерживаемый per-channel либо CLE | Меньше занулённых малых весов | CLE требует доказанной алгебраической допустимости и учёта ветвлений; для SiLU нельзя механически использовать ReLU-правило |
| Ошибка в основном от weight rounding, выбранный grid стабилен | AdaRound | Меньше reconstruction error на независимых кадрах | Новый compiler scale, folding после оптимизации или clipping активаций меняют задачу |
| Ошибка накапливается внутри residual block | BRECQ-подобная реконструкция | Ошибка выхода блока и целевые task slices | Требуется корректное определение блоков, memory cache и архитектурная адаптация |
| Широкая task degradation при допустимом graph/numerics | QAT | Detection/pose и события, а не только tensor MSE | Ошибки разметки, нехватка редких сценариев, несовпадающая target arithmetic |
| Есть хороший float teacher, labels ограничены | QAT + task-aware distillation | Student на тех же hard slices | Teacher может ошибаться на мелких СИЗ; повторять его ошибки недостаточно для GT-качества |
| Недопустимые operators/dtypes/границы графа | Совместимая модель/голова или согласованная замена op | Компиляция и проверяемый output contract | QAT не превращает unsupported operator в поддержанный |

В detector/pose distillation нельзя слепо применять CE/KL к финальному массиву после NMS. Нужны согласованные class order, box parameterization, keypoints и соответствие кандидатов teacher/student; для DETR семейства — учёт сопоставления query/предсказаний. Возможные losses на features, pre-decoder outputs, boxes или keypoints являются проектными вариантами; конкретный рабочий CV-рецепт для неизвестной модели здесь не подтверждён. Distillation в float тоже может улучшить базу, но не равна QAT: студент должен видеть нужную simulated quantization, если цель — именно компенсация quantization error.

Обычный fine-tuning float checkpoint после неудачного PTQ — обучение новой float-модели с последующим новым PTQ. Он может помочь domain adaptation, но не оптимизирует quantized task loss автоматически. Полное выключение quantizers при обучении и включение только при экспорте не даёт оснований называть процедуру QAT.


## Дерево решений PTQ → correction → QAT → другая модель

1. Зафиксировать checkpoint, input tensors, preprocessing и decoder. Сравнить исходный framework и FP32 export на одинаковых tensors. Если деградация уже здесь — исправлять export/graph/decoder, не начинать QAT.
2. Получить минимальный compile/run неизвестной пока платформы. Если custom model upload или нужный формат не разрешён — переориентировать работу на разрешённые модели, не тренировать неразвёртываемый artifact.
3. Выполнить PTQ с отдельной representative calibration и независимой validation. Если проходит согласованные task/event gates и LinQ latency — остановить эскалацию.
4. Если PTQ не проходит: раздельно исследовать weight-only/activation-only simulation, сдвиги каналов, clipping, чувствительные блоки. Разрешённое compiler mixed precision рассматривать вместе с веткой W1-09. Нельзя приписывать LinQ такое разрешение заранее.
5. При адресном симптоме выбрать **одну** correction, сохранить baseline и повторить export/compile. Если локальная метрика улучшилась, но реальная task/event метрика нет, correction не допущена. Не складывать несколько коррекций без ablation.
6. Если поддерживается QAT numerical contract и остаётся task degradation — ограниченный QAT trial с фиксированным validation, checkpoint rollback, управлением BN/observer и минимумом изменяемых hyperparameters. Нужны training labels или проверенный teacher-based loss; test set остаётся закрытым для выбора конфигурации.
7. После trial сравнить fake-quant, exported representation и LinQ. Хорошая fake-quant модель при плохом LinQ результате означает новый вопрос к lowering/quant contract. Продление обучения пока не обосновано.
8. Если законный экспорт отсутствует, отсутствует достаточная data coverage либо QAT не проходит gates, выбирать более совместимую/устойчивую архитектуру или менять разрешённую точность. Новый кандидат вновь проходит FP32→PTQ→LinQ, а не наследует чужой PASS.


## Что именно нужно согласовать с downstream export

До QAT сохранить таблицу: weight/activation bitwidth; int8/uint8; symmetric/asymmetric; per-tensor/per-channel и axis; scale/zero-point dtype; narrow/full range; clipping; rounding tie rule; bias/accumulator dtype; saturation; requantization; fusion graph; разрешённые float islands; fixed/dynamic shapes; quantized input/output contract. Для каждой строки — ссылка на версию SDK либо проверочный micrograph, либо `unknown`.

Два возможных маршрута требуют разного доказательства:

- **Explicit quantization:** импорт QDQ/QOperator или документированных encodings. Проверить, что compiler не игнорирует scales и не меняет арифметику необъявленно; проверить соответствие tensor names после folding/simplification.
- **Float import + compiler quantization:** выяснить, можно ли передать/fix ranges и воспроизвести compiler quantization в training. Если нельзя, полезность QAT остаётся гипотезой. Bias/CLE меняют float weights и могут быть легче передаваемы, но также требуют новой target evaluation. Для AdaRound изменение grid особенно существенно.

Не удалять Q/DQ или sidecar лишь ради успешной компиляции без повторной численной проверки. Входящая float-модель, из которой исчезли simulation ops, может быть правильным AIMET export **при наличии поддерживаемого sidecar consumer**; внешне похожий artifact без такого consumer не подтверждает тот же quantized model.


## 1–2 RTX 3090: стоимость, память и время без выдуманных оценок

Ни fitting в 24 ГБ, ни число эпох, ни часы, ни качество не установлены. Размер checkpoint не равен памяти обучения: нужны параметры, gradients, optimizer states, activations, fakequant intermediates, workspace и, для distillation, teacher. Два устройства не образуют автоматически единый пул 48 ГБ; обычная data parallel схема реплицирует модель. Специальная BRECQ multi-GPU процедура также не даёт автоматического линейного ускорения.

| Путь | Данные | Главные ресурсы | Вариант при двух GPU | Как получить честную оценку |
|---|---|---|---|---|
| Bias/CLE | CLE может быть без данных в допустимых графах; empirical bias требует representative input | Несколько forward/reference проходов, graph engineering | Независимая validation/ablation | Измерить отдельно подготовку, correction, export/compile |
| AdaRound | Unlabeled reconstruction data + отдельный GT eval | Локальная оптимизация и caching | Независимые гипотезы или поддержанный distributed path | Замерить выбранный слой/блок и число таких единиц; не экстраполировать только по параметрам |
| BRECQ | Reconstruction data, модельные block definitions | Повторная оптимизация блоков/activation scales, cache RAM/VRAM | Только проверенная реализация synchronization | Учесть weight pass, activation pass, caching и target validation |
| QAT | Task labels, reproducible training/eval | Backprop всей или выбранной части модели | DDP при поддержке модели/quantizers; либо два контролируемых опыта | Измерить warm steady-state step time, peak memory и validation/export overhead |
| QAT + distillation | Inputs, teacher; labels желательно для контроля task quality | Student backward + teacher forward; хранение targets/features | Teacher cache или отдельное устройство — только после проверки корректности | Сравнить online teacher против frozen cache и учесть generation/storage cost |

Плановая формула стоимости: `C = Σ(rate_gpu_i × billable_hours_i) + storage + transfer + прочие условия площадки`. Ставку конкретной Vast.ai машины и billed time в этой ветке не получали. Формула времени: `setup + data/cache + measured_step_time × selected_steps + eval + export + compile + target_eval`. Это способ оценивания после разрешённого pilot, а не нынешний прогноз. Выбор между одним и двумя GPU делается по measured wall time и стоимости, с одинаковым effective batch и одинаковой validation.


## Контекст W1-09

Основания: [F106](#F106), [F107](#F107), [F108](#F108), [F109](#F109), [F110](#F110), [F111](#F111), [F112](#F112), [F113](#F113), [F114](#F114), [F115](#F115), [F116](#F116), [F117](#F117), [F118](#F118), [F119](#F119). Source scope и статус сохраняются.

## Матрица техник и выбора блоков

Следующие строки — **наши инженерные гипотезы**, которые источники делают проверяемыми; это не найденный универсальный список чувствительных слоёв.

| Техника | Что меняем и что измеряем | Когда полезна / контрпример / цена |
|---|---|---|
| Single-block rescue | На общем Q baseline вернуть один цельный блок в исходную FP precision; сравнить objective и stress slices | Даёт conditional recovery в контексте остальных quantized блоков. Если вход уже потерял информацию, отсутствие recovery не оправдывает квантование блока |
| One-block quantization | На FP baseline квантовать только подозреваемый блок с той же quantization policy | Изолирует способность блока переносить noise; не отражает совместный эффект всей Q модели. Дорог при O(N) всех layers — применять только к двум спорным группам |
| FP output islands | Отдельно classification, bbox regression, objectness при наличии, keypoint coordinates/heatmaps/visibility, decode softmax/expectation | Устранение class flip, small-box drift, keypoint error. Поднять весь head недостаточно при QDQ перед head; сравнивать input-boundary и branch отдельно |
| FP activation/reduction islands | FP вокруг найденного разрыва SQNR или near-threshold nonlinear/reduction блока | LayerNorm/softmax в DETR/RT-DETR — кандидаты, не автоматическое исключение. BatchNorm мог быть folded в Conv: исключать несуществующий BN бессмысленно. SiLU после weighted op — отдельная граница, [S104](SOURCES.md#S104) |
| Сохранение high-resolution branch | Один блок/ветвь, которая несёт мелкие объекты, по реальному graph mapping | Проверять AP/recall мелких СИЗ и keypoints в исходных pixels. «Последний слой важнее» не объясняет early-feature loss |
| NNCF accuracy control | Metric-driven quantizer-group removal с `max_num_iterations`; логировать restored scope и окончательный граф | Готовая реализация для ONNX/OpenVINO. Одна scalar metric может скрыть падение критического класса; holdout и отдельные hard gates обязательны |
| FP16/FP32 conversion blocklist | [S071](SOURCES.md#S071)/S05 node/op exclusions и Cast; clipping конвертера зафиксировать по W1_06-S04/F05 | Восстанавливает FP16 failure, а не INT8 scales. Не смешивать clipping/initializer changes с эффектом selective PTQ |
| Hessian trace / Pareto | Анализ loss и поиск по реально поддерживаемым precision candidates | Разумно при доступном trainable checkpoint и compile contract; неоправданно стартовать с 2/4/6 bits, если target даёт только один quantized format |

Переносимость: для torchvision Faster/Mask/Keypoint R-CNN отделить backbone/FPN, proposal/ROI processing и heads; фактическая exportability — W1-02/03. Для DETR/RT-DETR сохранить semantic boundaries attention/reductions и logits/bbox branches; не назначать им YOLO decoder. Для RTMPose исследовать его реальные coordinate-distribution outputs, если такой checkpoint выбран. Для TensorFlow/LiteRT границы quantizer/delegate другие; API [S099](SOURCES.md#S099)/S06 не выдаётся за TFLite conversion API. Модели здесь не выбраны, эти группы не обещают существование всех named modules.


## Почему FP island может оказаться фикцией

Если `z = DQ(Q(x))`, вычисление `head_FP32(z)` не является `head_FP32(x)`: поднятие dtype не отменяет округление/срез диапазона x. Это математическое следствие quantization, не измерение нашего head. Нужна пара: (A) FP head с QDQ на его входе; (B) FP head и feature producer с границей перенесённой до producer. Если помогает B, а A нет, причинный кандидат находится раньше; не делать вывод «mixed precision бесполезна».

На shared tensor граница может влиять сразу на две ветви. В residual add ошибки ветвей взаимодействуют; результат объединения двух «полезных» exclusions не обязан быть суммой результатов. На этапе compiler QDQ может быть fused и propagated, а FP cast — удалён как избыточный или заменить execution type в пределах правил backend. Поэтому manifest должен хранить edge names, scale/axis/zero-point, dtype и consumers до/после. Нельзя просто вручную стереть Q/DQ из произвольного графа: могут остаться integer initializer или нарушиться контракт consumer. Вновь строить вариант из одного FP parent через supported quantizer безопаснее и лучше локализует изменение.

FP islands также могут разбить accelerator subgraph, добавить host/device transfers и синхронизацию. Если latency растёт, это не доказательство дороговизны FP арифметики: причина может быть partition/reformat. И наоборот, fewer INT8 ops иногда помогают fusion или уменьшают transfers; по доле quantized nodes нельзя предсказывать FPS. CPU decoder допустим только в рамках реального контракта и не подменяет обязательный neural inference на LinQ; neural CPU fallback требует отдельного раскрытия и acceptance, а не замалчивания.


## Короткий план абляций и expected checks

Все E-ID имеют статус **PROPOSED / UNRUN**. Число шесть/две — наш ограниченный бюджет исследования, не эмпирически оптимальный параметр и не KPI конкурса.

| ID | Действие | Expected check / решение |
|---|---|---|
| W1-09-E01 | Зафиксировать checkpoint, export/prepared graph hash, input tensors, decoder, PTS, calibration set, scale policy, compiler flags и версии; FP source→FP export→FP target parity | Ошибка до quantization: FAIL diagnosis и возврат W1-02/03/05/06, не запуск precision search. Нет FP target: reference scope явно слабее, target parity UNKNOWN |
| W1-09-E02 | Проверить target на малом реальном фрагменте выбранной модели: quantized producer→FP block→quantized consumer и shared/residual boundary, только после доступа к поддерживаемому API | Compile success плюс execution report с dtype/device/partitions; проверить raw outputs. Принятие graph без evidence фактического исполнения — INCONCLUSIVE |
| W1-09-E03 | Один фиксированный PTQ baseline Q против FP на dev-search; затем debug-копии на малой frozen подвыборке, collect/match intermediate activations | Первый устойчивый разрыв `xmodel_err`, локальный `qdq_err`, per-channel и branch residual; не считать largest tensor-MSE layer автоматически виновником AP loss. Augmented debug graph может менять fusion — final latency измерять по обычному графу |
| W1-09-E04 | Выбрать до шести неперекрывающихся semantic groups по E03 + ошибочным outcomes; выполнить шесть single-group rescue из общего Q baseline | Для каждой: delta bbox/class/keypoint metrics по paired inputs, critical slices, число unmatched, latency/transfer cost и actual restored scope. Ранжировать по recovery при соблюдении gates, не только по SQNR |
| W1-09-E05 | Для двух лучших/неясных групп провести максимум две дополнительные проверки: одна boundary-before-producer или one-block quantization и одна combined rescue | Установить upstream loss или interaction. Если combination не помогает, не суммировать isolated gains. Если все rescue слабы — пересмотреть calibration/экспорт/decoder прежде QAT |
| W1-09-E06 | Пересобрать лучший вариант из clean FP parent, сохранить/load, скомпилировать production graph без debug outputs | Expected exact scope, preserved FP weights там, где это требовалось; для OpenVINO сохранение учитывать [S081](SOURCES.md#S081). Если точность после save/compile потерялась — FAIL transfer, не заявлять успех на simulated QDQ |
| W1-09-E07 | Одна независимая holdout-проверка winner vs FP и Q с неизменными thresholds/decoder, камерами/клипами вне search; replay одинаковых событий при reset tracker | Detection/pose, event recall, false/duplicate alerts и alert latency раздельно. Gate/budgets заранее согласовать с W1-12; поиск по test запрещён. Малый holdout без редких событий даёт INCONCLUSIVE для них |
| W1-09-E08 | После E07 профиль target: warmup отдельно, фиксированные input shape/batch, одинаковый frame sampling, operator/device/transfer logs, latency distribution | Проверить, что улучшение не куплено CPU neural fallback или пропуском кадров; обязательное LinQ исполнение подтверждать W1-15 evidence. Pipeline bottleneck: decode/preprocess, accelerator, transfer, decoder, tracker отдельно |

Расчёты для rescue: при higher-is-better metric M записывать `R_g = M(Q с FP group g) - M(Q)` и остаточную потерю `M(FP) - M(variant)`; при error metric знак меняется. Вместе хранить абсолютные значения, paired failures и count/exposure, а не только проценты восстановления. Ranking и состав групп выбирать по dev-search. Calibration freeze важен: если для каждого варианта меняются scales других слоёв, вывод становится эффектом всей процедуры, а не одного exclusion. Где quantizer пересчитывает downstream scales неизбежно, сохранить scale diff и честно обозначить эту ширину вмешательства.

Остановка: (a) первый прошедший все quality/target/latency gates вариант; (b) исчерпаны шесть rescue + две проверки без приемлемого результата; (c) target не умеет нужную границу. В (b) передача W1-07 для fixed-calibration диагностики или W1-08 для обоснованного QAT; GPU не расходовать на неподдерживаемую precision policy. В (c) выбрать поддерживаемый целиком FP/quantized вариант либо совместимую модель — конкретный выбор только после SDK. Acceptance thresholds в этой ветке не выдумываются.


## Контекст W1-10

Основания: [F120](#F120), [F121](#F121), [F122](#F122), [F123](#F123), [F124](#F124), [F125](#F125), [F126](#F126), [F127](#F127), [F128](#F128), [F129](#F129), [F130](#F130). Source scope и статус сохраняются.

## Где 0.5–2 pixel становятся изменением события

Ниже **аналитические придуманные примеры**, не кадры и не результаты моделей/LinQ. Пиксели — непрерывные координаты боксов, без integer-inclusive convention. Они показывают механизм, а не ожидаемую величину ошибки.

1. Для двух квадратов стороны `s`, сдвинутых на `d` по обеим осям, `IoU=(s-d)^2/[2*s^2-(s-d)^2]`, при `0≤d<s`. Для `s=4` и `d=0.5/1/2` это примерно `0.620/0.391/0.143`; для `s=8` — `0.784/0.620/0.391`. Таким образом, один пиксель может перевести tiny box через IoU=0.5 при неизменном визуальном классе. Это влияет на оценку matching и на системы, где используется IoU association; не означает автоматически, что событие пропущено.
2. Пусть network resize имеет scale `1/3`. Ошибка 1–2 pixel **в model input** соответствует 3–6 source pixels. Для heatmap дополнительно учитывать stride, crop affine и inverse transform: при stride=4 сдвиг 0.25 heatmap pixel даёт 1 input pixel. У реальной камеры коэффициенты необходимо прочитать из pipeline, а не предположить.
3. Если правило принимает `score≥0.25`, изменения `0.251→0.249` достаточно для пропажи кандидата. Пиксели здесь вообще не меняются. Сохранить score до threshold/NMS: иначе отсутствие объекта ошибочно выглядит как грубая регрессия localization. Порог иллюстративный, не предлагаемый норматив.
4. Две соседние heatmap/SimCC позиции с почти равными значениями могут сменить argmax или превратиться в tie после округления. Например, `0.5001` и `0.4999` при шаге округления `0.01` обе дают `0.50`. Фактический сдвиг зависит от tie ordering, формы peaks и codec. Это условный арифметический пример, не установленный quantizer LinQ.
5. Направление короткого сегмента `(10,0)` после ошибки endpoint `(10,2)` поворачивается на `atan(2/10)≈11.31°`. Для `(100,0)→(100,2)` это около `1.15°`. Поэтому angle rule на foreshortened limb может смениться при небольшом jitter. При ошибках обоих концов ситуация иная; rotation одного сегмента не равна ошибке полного коленного угла.
6. Если signed distance опорной ankle/foot точки до границы ROI меняется `+0.5→−0.5` source pixel, классификация inside/outside меняется. После homography метрическая ошибка зависит от локальной геометрии и плоскости; переносить единый «пиксель→сантиметр» коэффициент нельзя. См. W1-05 и W1-11 для inverse geometry и temporal rules.
7. Phone box может остаться правильным, но wrist другого человека окажется ближе после 1–2 px сдвига. Ошибка возникает в owner/interaction association: глобальный detection mAP может остаться почти тем же, а уведомление уйдёт не тому actor. Проверить person/object/hand связи отдельно.


## Приоритетные stress slices

Следующие границы — **проект протокола**, не научно установленные safe thresholds. Срезы допускают пересечения; по каждому сохранять число уникальных клипов, людей, объектов и событий. Не считать соседние кадры независимыми примерами. Размер задавать по GT и неизменной геометрии pipeline, а не по target predictions — иначе исчезнувшие объекты выпадут из среза.

| Приоритет / ID | Как отбирать и размечать | Ожидаемые проверки |
|---|---|---|
| P0 / ST10-01 tiny/thin | На model input: `min(w,h)` в корзинах `<4`, `4–<8`, `8–<16`, `≥16` px; одновременно площадь, aspect ratio и source size. Корзины предварительные | Per-class recall/AP; matched box dx/dy/IoU; disappearance before/after NMS. Отдельно thin cigarette/strap: одна площадь не отражает толщину |
| P0 / ST10-02 low contrast + tiny | Тот же объект: естественный тёмный фон/одежда, блик/дым, compression; отмечать человеческую различимость и ambiguity | Парное `Δrecall` target−reference внутри среза; score margins и missed GT. Не объявлять невидимое «отсутствующим» |
| P0 / ST10-03 owner under overlap | Несколько людей, руки/телефоны пересекаются; отдельно контакты с оборудованием. GT owner_id и interaction interval | Верный объект + неверный actor; switches wrist owner; wrong-person event count; случаи correct detection/incorrect rule |
| P0 / ST10-04 occluded event joints | Wrist/ankle/hip: visible, annotated occluded, unlabelled/unknowable, out-of-frame; дополнительно источник перекрытия | Per-joint coordinate error, confidence/dropout, left/right swaps, angle stability. Не штрафовать неизвестный GT как точное положение |
| P0 / ST10-05 threshold margin | Независимый общий set и дополнительный диагностический набор малых reference margins для score/NMS/ROI/angle/association | Доля decision flips; score vs box vs rule причина. Margin-поднабор не использовать для оценки частоты отказов в эксплуатации |
| P1 / ST10-06 partial person | В кадре нет стоп/головы/части торса; человек за станком, под грузом, у границы crop | Pose missingness и fall/lying false alarms; det crop vs pose decomposition; нет вывода «лежит» только из короткого видимого bbox |
| P1 / ST10-07 blur/compression | Естественное движение и defocus раздельно, различная компрессия; controlled variants с записанными kernel/seed/codec отдельно | Reference и target получают один и тот же вариант изображения. Вычислить interaction: ухудшается ли именно parity при искажении, а не только абсолютная точность обоих |
| P1 / ST10-08 rare class/pose | Редкие классы, наклон/спина к камере, приседание/лестница/переноска, foreshortened limbs | Macro/per-class recall; event evidence sufficiency; число GT обязательно. Отсутствие примеров = unknown, не PASS |
| P1 / ST10-09 hard negatives | Рация/инструмент/перчатка у лица, еда/питьё, ручка/кабель, ремень вместо привязи; наклон/ремонт/сидение вместо падения; пар/сварка/блик вместо курения | FP на нужном человеке, false events per camera-hour на непрерывном видео, near-miss specificity; empty frames отдельно |
| P1 / ST10-10 recovery | Короткие клипы до/во время/после перекрытия или исчезновения tiny object; фиксированные PTS | Max dropout run, reacquisition time, event delay/miss/duplicates при одном событии; интеграция с W1-11 |
| Conditional / ST10-11 tiling seams | Только если ROI/tiling реально принят: объект/человек на шве crop, large body + tiny phone, несколько соседних tiles | Shift coordinates, дубли и merge, owner context, target throughput всей стратегии; full-pass и sliced settings frozen |

Матрицу не нужно реализовывать полным декартовым произведением. Сначала основные clean контроли и одиночные стрессоры, затем сочетания tiny×blur, tiny×low-contrast, overlap×wrist-visibility и partial-person×pose-rule. Редкие критичные сочетания проверять явно; среднее по частым лёгким кадрам их не заменяет.


## Ограничения и контрпримеры

- Окклюзия скрывает факты. Видна привязь ≠ доказано крепление к анкеру; не видна тонкая стропа ≠ доказано её отсутствие. Телефон рядом с человеком ≠ доказано использование; wrist у рта ≠ доказано курение. Нужны размеченные interaction/evidence и состояние «недостаточно данных», иначе parity способна сохранить ложную интерпретацию.
- Большой объект у границы зоны тоже может быть чувствительным к одному пикселю. Малый размер увеличивает относительную геометрическую ошибку, но downstream margin часто важнее абсолютного размера.
- Рост precision не создаёт детали, потерянные камерой, blur или resize. Tiling увеличивает пиксельный бюджет модели относительно full-frame resize, но не возвращает невидимый сигнал и может уничтожить контекст взаимодействия.
- Публикации SAHI — drone/satellite; CrowdPose — повседневные человеческие сцены; Robust Detection включает общие/дорожные данные и синтетические искажения. Фабрика отличается optics, fixed viewpoint, СИЗ, дымом, объектами, освещением и частотой событий. Ни проценты улучшения, ни severity, ни ranking моделей прямо не переносятся.
- Общая программа срезов применима к YOLO, torchvision detection, DETR/RT-DETR и heatmap/SimCC pose. Raw tensor layouts, presence/absence NMS, score semantics, coordinate conventions и codec для каждого семейства разные. MMPose decoder нельзя приписать YOLO pose; NMS-проверка не навязывается NMS-free head.
- Без LinQ intermediate tensors не доказать конкретный layer culprit. Без достаточного GT не доказать absolute/event accuracy. Без исполнения и runtime evidence нельзя объявить поддержку tiling/mixed precision или фактическую TPU-работу.


## Контекст W1-11

Основания: [F131](#F131), [F132](#F132), [F133](#F133), [F134](#F134), [F135](#F135), [F136](#F136), [F137](#F137), [F138](#F138), [F139](#F139), [F140](#F140), [F141](#F141), [F142](#F142). Source scope и статус сохраняются.

## Как небольшая ошибка становится ошибкой события — инженерный вывод

Следующая таблица — **наша причинная модель и диагностические предложения**, а не измеренная статистика. Она применима к любому detector/pose backend с приведённым к общему контракту выходом: YOLO, torchvision detection, DETR/RT-DETR, RTMPose, TFLite, OpenVINO, ORT. Реализованный adapter и доступность модели на LinQ пока не установлены.

| Первое изменение | Промежуточный эффект | Событийный сбой | Что логировать до исправления |
|---|---|---|---|
| Score около confidence/NMS/association threshold | Меняется состав кандидатов или ветка high/low; новый ID не рождается | Не набирается confirmation; поздняя тревога | Score до отсечения, причина отбрасывания, high/low/new-track решения |
| Бокс дрожит возле границы ROI | Bottom-center перескакивает границу | Повторы входа/выхода, ложный crossing | Anchor, signed distance до границы, наблюдение/предсказание, состояние зоны |
| Keypoint дрожит, пропадает либо меняется visibility | Меняются угол, высота корпуса, OKS или связь с человеком | Ложное падение/пропуск, ownership flip | Keypoint index/schema, координаты, score/mask, derived feature, actor |
| Dropout, окклюзия, разрыв ID | Сбрасывается накопленное время либо история переносится неверно | Дубликат/событие не того человека/пропуск | Track lifecycle, parent/reassociation, gap seconds, reset reason |
| Близкие люди и техника | Перепутана пара участников | Верная геометрия при неверной принадлежности | Обе entity ID, классы, pair key, физическая/пиксельная система координат |
| Неправильный Δt или скрытый skipped frame | Скорость/время подтверждения ошибочны | Ложный бег/опасное сближение, преждевременная тревога | Source PTS, Δt, skip reason, velocity units, observation age |
| Queue/backpressure/reordered completion | Данные устарели или пришли не по времени | Позднее уведомление, обращённая траектория | Capture/decode/enqueue/infer/rule/notification timestamps, stream sequence |

Дифференцирование усиливает геометрический шум: если каждая из двух координат имеет ошибку по норме не более ε, то при правильном фиксированном Δt ошибка разности скоростей ограничена `2ε/Δt`. Это математическое условие, не оценка нашей модели. При редкой выборке уменьшается этот вклад шума, но теряются короткие движения и растёт неоднозначность association; поэтому «больше FPS всегда лучше» и «меньше FPS точнее» одинаково недостаточны. Пиксельная скорость зависит от перспективы; измерять м/с без калибровки и правильных наземных точек нельзя. Поза и бокс требуют отдельных masks: отсутствующий keypoint не следует заменять координатой `(0,0)` как реальным наблюдением.


## Предлагаемый причинный replay: разделить модель, трекер, правила, планировщик

**Статус всех шагов этого раздела: PROPOSED / NOT RUN.** Минимальные входы: клипы с исходными timestamp, независимая GT-разметка событий/участников, baseline weights/runtime, candidate artifact, замороженные preprocess/decoder/tracker/rules. Пока их нет, возможен только дизайн проверки.

1. Сохранить manifest каждого декодированного кадра: `clip_id, stream_id, decode_sequence, source_pts, time_base_num/den, media_time_seconds, timestamp_origin, frame_hash, selection_reason`. Порядок replay — порядок отображения/исходного события после корректного decode, не DTS и не порядок завершения асинхронного inference. Невалидные/немонотонные timestamps, discontinuity, reconnect и одинаковый PTS обрабатывать явно, по отдельному stream epoch. Не подменять их `index/nominal_fps` без метки синтетического времени.
2. На **одних и тех же сохранённых кадрах** получить baseline B и candidate C; сохранить tensors и canonical detections/pose до трекера. Заморозить threshold/NMS/decoder. При многокомпонентной модели по одному менять detector, pose, ReID, temporal head. Не менять одновременно precision, preprocessing и policy.
3. Убедиться в детерминизме replay B→B: одинаковое начальное состояние, конфигурация, seed и tie-breaking. Сбрасывать tracker/event/global ID allocator между клипами и парными ветками. Для mid-stream replay нужен одинаковый causal warm-up prefix или один сериализованный state checkpoint; cold start прямо перед инцидентом меняет задачу.
4. Прогнать B→T→E и C→**тот же T**→**тот же E**, с identical PTS/selection. Наблюдаемая разница — совместный эффект модельного вывода через трекер/правила при фиксированных прочих условиях. Сохранять первое расхождение: detection/pool → assignment → track → primitive predicate → FSM → notification. Простое «mAP не изменился» не закрывает эту ветку.
5. Для локализации выполнить замену одного типа данных: B boxes+C scores; C boxes+B scores; baseline/candidate keypoints на **фиксированных person crops/actor associations**; baseline/candidate features на фиксированных detections. Это искусственные диагностические вмешательства; они не являются валидными production предсказаниями и не обязаны давать аддитивную декомпозицию из-за threshold/nonlinear interactions.
6. Отдельно replay фиксированных canonical detections через старый/новый tracker; фиксированных tracks/predicates через старые/новые event rules. GT tracks или принудительные baseline associations допустимы для диагностики, но такой oracle-run нельзя включать в онлайн quality score. Изменение association между B и C — один из искомых эффектов, его нельзя навсегда скрыть фиксацией ID.
7. Только после fixed-input проверки добавить реальные captured LinQ outputs и schedule: lateness, dropped frames, batching, fallback, competing streams. Это уже **system-level** ветка. Записать, где исполняется каждая нейросеть. Изменение schedule проверять отдельно от изменения модели.

Для абсолютного качества обе ветки оцениваются на одной независимой GT. Сырые числовые track IDs между запусками могут различаться без ошибки: сопоставлять траектории и участников по GT/геометрии, а не требовать равенства ID-номеров. События двух участников требуют пары правильных физических entities. На уровне событий хранить также `miss_both`, `baseline_only_TP`, `candidate_only_TP`, `TP_both`, новые FP/дубли и распределение задержек; это не позволяет скрыть регрессию усреднением улучшений на иных клипах.


## Контракт времени и автомата событий — предложение

**Медиавремя и wall clock различаются.** В replay длительность определяется `source_pts × соответствующий time_base`. Для реального latency нужны capture/event time и момент доступного пользователю уведомления в сопоставленных часах. Media PTS обычно не является UTC; без привязки часов абсолютная capture-to-notify задержка неизвестна. Замерить отдельно decode/queue/infer/rule/delivery; длительность офлайн-обработки файла сама по себе не равна задержке события. Если PTS отсутствует и используется best effort, сохранить происхождение и статус timestamp; для VFR не делить порядковый номер кадра на nominal FPS.

Предлагаемые состояния: `CLEAR → CANDIDATE → ACTIVE → CLEAR_PENDING → CLOSED`; `UNKNOWN`/quality flag при нехватке наблюдений. Хранить event identity отдельно от transient track ID. Это спецификация для реализации, не установленный API LinQ.

| Параметр | Что задавать явно | Основная проверка |
|---|---|---|
| Confirmation | Непрерывное наблюдаемое время, K из N, доля support или интеграл evidence; отдельные правила для разных событий | Два отдалённых positive кадра не должны автоматически доказывать непрерывное нарушение между ними |
| Maximum observation gap | Допустимый промежуток и что происходит при его превышении: pause/reset/unknown | Долгий пропуск не закрывается бесконечным last-value hold |
| Hysteresis | Разные enter/exit thresholds, пространственная margin, единицы координат | Boundary jitter не создаёт серию событий; реальный короткий вход всё ещё обнаруживается |
| Debounce / clear duration | Время устойчивого отрицания перед закрытием; не путать с минимальной длительностью до открытия | Короткий dropout не разрывает эпизод; два самостоятельных инцидента не сливаются |
| Minimum event duration | Длительность фактического нарушения по определению класса | Если правило требует длительность дольше самого события, пропуск является следствием policy, а не обязательно модели |
| Cooldown / dedup | Ключ camera/epoch/type/actor(s)/zone + правила re-ID/merge | Смена ID внутри одного эпизода не создаёт дубль; другой человек не подавляется глобальным cooldown |
| ROI/crossing/proximity | Геометрическая точка, граница/направление, расстояние/система координат, max gap | Пересечение между двумя точками — гипотеза о траектории; при слишком большом gap оно неизвестно |
| Predictions vs measurements | Возраст последнего измерения и допускается ли predicted state в evidence | Kalman prediction может поддерживать continuity, но не выдаётся за наблюдение телефона/позы/СИЗ |

Записывать как минимум `event_onset_estimate`, `first_observed_positive`, `confirmation_time`, `alert_emitted`, `alert_available`, `clear_time`, `last_support_pts`. Ретроспективный onset может предшествовать подтверждению, но не означает, что система уведомила тогда. Любая smoothing/interpolation, использующая будущие кадры, должна иметь отдельную offline метку и не улучшать causal latency задним числом. Для temporal neural model дополнительно фиксировать source PTS каждого входа окна, его receptive field, padding/missing mask, hidden-state reset, causal/noncausal режим: одинаковое число кадров при ином FPS задаёт иной физический интервал.


## Редкая выборка, 1 FPS и fallback — предложение с математической границей

При идеальных мгновенных наблюдениях с интервалом Δ и событии длительности d, **если фаза начала равномерна относительно решётки**, вероятность хотя бы одного попадания `min(1,d/Δ)`. Для как минимум k наблюдений: `clamp(d/Δ − (k−1), 0, 1)`. Это аналитическая модель покрытия, **не измеренный recall и не предположение о реальном распределении фаз**. Пограничные совпадения времени зависят от принятой включённости концов интервала. Реальные распознавание, окклюзии и требования confirmation могут лишь добавить ошибки к идеальному покрытию.

При 1 FPS событие 0.2 s в этой модели имеет лишь 0.2 вероятности одного наблюдения, а при неблагоприятной фазе — ни одного. Если событие должно иметь два подтверждающих кадра, интервал менее секунды может не дать их вообще. При неравномерной обработке важнее максимальный интервал без полезного наблюдения, а не средний FPS. Средние 1 FPS могут содержать как равномерную выборку, так и многосекундный blackout с последующей пачкой кадров; задачи различны.

Предлагаемый sweep:

- Взять размеченные короткие клипы с точными onset/end, обычным поведением, persistent events, двумя близкими эпизодами, двумя людьми, окклюзией и движущейся техникой. Не создавать клипы только около известных GT onset для основного causal score.
- Для каждой проверяемой частоты прогнать **все дискретные фазы, доступные на исходной PTS-шкале**, либо заранее фиксированную сетку фаз; отдельно contiguous burst drops, нерегулярные пропуски и реальные traces очереди. Указывать покрытую фазовую сетку, worst phase, per-class duration slices и max gap. Частоты выше 1 FPS — кандидаты измерения, не заранее известное решение.
- При постоянных кадрах менять policy confirmation/hysteresis; при постоянной policy менять sampling. Иначе эффект модели, события и подсистемы времени смешиваются. Отдельно сообщать `observable GT` для диагностики, но **основной recall имеет знаменатель всех размеченных целевых событий**, включая полностью пропущенные sampling.
- Adaptive sampling проверять причинно: триггер доступен только из уже обработанных данных, с собственной latency и FN. Если короткое событие начинается и кончается между low-rate кадрами, последующее повышение FPS его не спасает. Ring buffer даёт ретроспективный материал только если запись велась достаточно часто, буфер сохранился и replay успевает; он не делает тревогу мгновенной.
- Fallback заморозить как отдельную версию policy: что его вызывает, какой artifact/backend, как меняются calibration/thresholds, где neural inference, как согласуются IDs/state/PTS, как возвращается основной путь. CPU fallback нейросети не считать автоматически разрешённым при обязательном LinQ inference. Альтернатива — сохранение видео/статус degraded без заявления подтверждённого события.
- Под нагрузкой считать processed FPS, source FPS, sample FPS, максимальный gap, dropped count/reasons, effective frame age и latency. Прошедший офлайн sweep не доказывает real-time throughput, а высокий throughput не доказывает event recall.

**Нельзя обещать «без потери полноты» при произвольном downsampling.** Такой результат требует ограниченного класса событий с известной минимальной наблюдаемой длительностью, допустимым gap, работающим распознаванием и подтверждённым запасом производительности; здесь эти условия не получены.


## Контекст W1-12

Основания: [F143](#F143), [F144](#F144), [F145](#F145), [F146](#F146), [F147](#F147), [F148](#F148), [F149](#F149), [F150](#F150), [F151](#F151), [F152](#F152). Source scope и статус сохраняются.

## Пять evidence-пакетов

Всё далее **PROPOSED**, не выданный SDK/API. `PASS(scope=...)` содержит hashes, shapes/dtypes/batch/scenarios. Нет данных — HOLD; нарушение — FAIL.

| Пакет | Сохранить | PASS доказывает | Не доказывает |
|---|---|---|---|
| Source | checkpoint/config/class/skeleton hashes, source commit, eval mode, sample/label manifest, provenance/license, effective exporter/runtime/compiler flags и versions, seeds/determinism | Объявленная lineage и воспроизводимые условия | Accuracy или target execution |
| Tensor | inference input bytes/hash, shape/layout/dtype, quant scale/zp/axis, named raw outputs до decoder, observable boundary mapping, finite masks, error distributions | Численная близость на этих входах/границах | GT quality или новые shapes |
| Task | independent GT, canonical predictions, evaluator/config, matches, per-class/slice counts/AP/OKS | Качество распознавания на corpus/operating point | Association, rules, delivered alerts |
| Event | complete replay/PTS/timebase, person/episode truth, rules/zones/resets, logical+visible IDs, consumed frames, delivery ledger, exposure | Полезность эпизодов/доставки в закрытом окне | Future safety и другие prevalence |
| Device | artifact/model ID/hash, actual device, request/completion/output/error correlation, profiler/partition/fallback evidence если доступно | Завершение конкретного artifact на заявленной платформе в проверенном scope | Весь graph на TPU по одному response или capacity |

Для атрибуции нужен ladder: source FP32 → export same dtype → alternative runtime same dtype → dtype-only → quantized/calibrated → compiler/runtime → full decoder → tracking/rules/delivery. Сохранять **adjacent-stage** и **source-to-final deltas**: несколько малых потерь могут превысить общий budget. Если platform не даёт float target/intermediates, не выдумывать этапы: confounded transition, более сильная end-to-end/GT проверка.


## Входы и измерения

Три роли данных: calibration; development/threshold/debug; untouched evaluation. Повторно используемый golden smoke — диагностический, не скрытый test. Split по происхождению: одно видео/эпизод, соседние frames, нарезки и синхронные камеры общего инцидента не пересекают holdout без явно иной цели. Camera-heldout для новых ракурсов; site-heldout для площадок. Frame split не создаёт независимость.

Golden pack **не получен**. Предлагается: positives/empty frames, small PPE/phone, multi-person ownership, occlusion, hard negatives, lighting, boundary crossing; continuous clips short event, re-entry/reset, ID switch, file-end/outage, ongoing incident/duplicates. Immutable IDs/provenance/license; synthetic явно synthetic. Smoke информативен, но не репрезентативен.

A/B должны иметь те же decoded frames/source sampling, crop/resize/pad/color/normalization/ROI, batch/shapes, class/skeleton map, score threshold/NMS/caps, tracker/rule/zone versions, resets/order/evaluator. Retuning на test не является изолированным эффектом quantization. Разрешённый retuning на development — отдельная система с новым policy hash.


### Tensor, detection, pose

1. Проверить наличие всех outputs, names/shapes/dtypes, batch indexing, valid coordinates, finite values и non-mutated inputs. Хеш сравнивать **на inference boundary**, не только у JPEG. Для INT8 входа хранить master float tensor и quantized bytes+scale/zp, проверять declared mapping, а не требовать одинаковые bytes разных dtype.
2. Для соответствующих `r,c`: absolute error, normalized RMSE с объявленным scale/epsilon, p50/p95/p99/max и его координата, per-channel/head/slice summaries. Возможное условие `abs(c-r)<=atol_j+rtol_j*abs(r)`; tolerances согласуются на dev по repeatability/dtype/head sensitivity. Универсальные `1e-3`, cosine/SQNR cutoffs не предлагаются. NaN/Inf — отдельный contract failure; cosine не определён на нуле и может скрыть локальную ошибку.
3. Сравнить pre-threshold scores/logits/boxes/keypoints и threshold-margin crossings. Малая численная ошибка может дискретно менять событие. Первая observable divergence — локатор, не доказательство причины внутри fused op.
4. Canonical decode outputs сравнивать **как множества**: class-consistent IoU edges, one-to-one maximum cardinality, затем максимум sum IoU, stable tie-break. Хранить пары/unmatched A/B, score/box/keypoint deltas, ties. Это diagnostic matcher, **не COCO evaluator**.
5. Независимые A→GT и B→GT: per-class/size/condition AP и precision/recall при frozen threshold; negatives/empty scenes. Pose — подходящий OKS и visible per-joint error/PCK с определёнными normalization/threshold; unknown/hidden и unmatched persons отдельно. B≈A не делает ошибочный A правильным.


### Tracking и events

Числовые track IDs не обязаны совпадать. A/B оцениваются относительно независимого GT person/episode roster с continuity/occlusion/re-entry/reset. HOTA/DetA/AssA, ID switches/fragments — отдельный отчёт. Два replay: (i) одинаковые source schedule/downstream, меняется prediction stream — model effect; (ii) фактическое расписание/delivery/load — operational effect. Их смешение скрывает sampling/queue проблему под quantization.

GT episode определять по camera/epoch/person-or-scene/type/zone, observable onset/end и sufficient causal evidence. Короткий эпизод не превращать в N independent positive frames. Useful-alert edge требует совместимые ключи/личность, consumed evidence и deadline D в общей elapsed-time шкале; active-at-delivery либо after-event reporting — отдельное заранее выбранное правило. Freeze one-to-one matcher/tie-break. Duplicates, late, wrong-person/type, after-end, unresolved сохранять отдельно от strict unmatched. GT нельзя порождать тестируемым tracker/cooldown.

Только для **общего complete closed universe**: TP=#matches, FN=#GT−TP, FP=#delivered−TP; timely critical recall=TPcritical/NGTcritical. При разных boundary cohorts TP precision/recall может отличаться — общий F1 недопустим. Нужны sufficient follow-up и delivery close; incomplete logs/censored events не превращать в успех. Onset uncertainty хранить interval, не midpoint. Latency quantiles показывать с n и misses/late/unresolved: success-only p95 страдает survivor bias.

Semantic false delivered records/source-camera-hour = adjudicated false visible records / union duration заявленных source intervals по камерам в часах. Для этого нужен полный delivery census и review каждого assertion; recall дополнительно требует независимого GT discovery, включая silence. Duplicate burden отдельно. Не делить на positive clips, wall replay hours или только обработанные frames без другого имени endpoint. Outage при полном GT/logs — operational miss. Нет универсального TN/camera-hour определения specificity.


## Парная uncertainty и acceptance contract

До evaluation задать population (fixed corpus либо новые камеры), primary endpoints, допустимые losses δ, абсолютные floors/caps, alpha/one-sided bounds, critical slices, budget/stop rule. Полностью просмотренный fixed corpus с полными deterministic A/B имеет наблюдаемую разницу; bootstrap не нужен, чтобы сделать её «реальной», и не расширяет corpus на будущие заводы.

Для higher-is-better `Dq=qB−qA`: non-inferiority PASS при `L(Dq)>=−δq` и absolute floor B. Для lower-is-better `Dc=cB−cA`: `U(Dc)<=δc` плюс absolute cap. Для **двусторонней equivalence** весь CI внутри заранее заданных `[−δlow,+δhigh]`; это иной, более сильный вопрос. Недостоверный CI не даёт PASS. CI пересекает допустимую и недопустимую области → INCONCLUSIVE. Нарушен hard invariant/подтверждён budget violation → FAIL. Незаполненные δ/floors/caps → HOLD, не «1% по умолчанию».

Возможен узкий **PASS(fixed golden fixtures)** с нулём новых пропусков по frozen critical roster; это engineering invariant, не будущий recall=100%. Baseline ниже absolute floor нельзя одобрить за fidelity.

- Сохранить эпизодные A+/B+, A+/B− (regressed), A−/B+ (improved), A−/B−, unknown/incomplete; counts/denominators по cameras/classes/exposure/positive episodes/groups.
- Выбрать релевантный независимый cluster: site, camera-session или общий incident, объединяя связанные камеры. Для fixed-camera temporal claim блоки/эпизоды требуют обоснования границ зависимости. Hierarchical camera→episode resampling — только под соответствующий design. Миллион adjacent frames не равен миллиону trials.
- В каждом paired cluster-resample выбирать одинаковые clusters для A/B/GT; пересчитать **весь** pooled AP, TP/GT ratio, event matching, false/exposure, quantiles. Копии повторно выбранного cluster namespace по GT/person/event IDs. Mean per-camera AP вместо pooled AP меняет estimand.
- Сохранить RNG/software/draw count/scheme/weights/units, undefined/zero-positive fraction, histogram и leave-one-cluster-out sensitivity. Undefined recall нельзя молча удалить. BCa может выродиться; percentile [0,0] на нулевых ошибках не доказывает zero risk. При few clusters — descriptive sensitivity, HOLD generalization и сбор других камер/смен; магического minimum N нет.
- Overlap отдельных CI не является CI разности. `p>0.05` равенства не доказывает non-inferiority. McNemar без cluster model не исправляет видеокорреляцию; AP/latency не binary outcomes. Повторы deterministic inference проверяют nondeterminism, не добавляют камер.
- Primary endpoints/slices freeze; exploratory post-hoc findings подтвердить новым holdout. Все required gates должны пройти; для simultaneous coverage нескольких CI заранее выбрать multiplicity procedure. Подбор лучшего candidate на test создаёт selection optimism.


## Диагностика и stop-loss

| Симптом | Дешёвая проверка | Ограничение |
|---|---|---|
| Исчезли detections | input hash/dtype/range/layout, output count/semantics, score activation/threshold | QAT до контракта не нужен |
| Boxes смещены/зеркальны | одинаковый raw output одним decoder; xyxy/xywh/normalization/pad/inverse transform | Хороший tensor не гарантирует geometry |
| Классы перемешаны | class hash, score axis/nc, synthetic per-class fixture | COCO84/85 не универсальны для custom nc |
| Малые tensor deltas, разные NMS/events | margins/ties/caps/order, set matching, downstream state replay | Row mismatch не обязательно quantization damage |
| Общий AP сохранён, small/pose/event хуже | critical size/joint/occlusion slices, paired downstream | Средний AP не закрывает critical gate |
| Source/export проходят, target нет | input bytes/quant params/output map/completion/device, first observed boundary | Без target intermediates причина partly UNKNOWN |
| Real replay хуже frozen | source sampling/drops/age/resets/overload/retries | Throughput не равен временной coverage |

Первое нарушенное required invariant останавливает переход. Сохранить failed bundle и minimal reproducer ID. Сначала contract/geometry/decoder и observable transition, затем calibration/precision repair на dev. Обучение/QAT — отдельное решение после локализации с ресурсным budget; в этой ветке не запускается. Если observability не разделяет причины, честно записать confounded edge.


## Контекст W1-13

Основания: [F153](#F153), [F154](#F154), [F155](#F155), [F156](#F156), [F157](#F157), [F158](#F158), [F159](#F159), [F160](#F160), [F161](#F161), [F162](#F162), [F163](#F163), [F164](#F164), [F165](#F165), [F166](#F166), [F167](#F167), [F168](#F168), [F169](#F169), [F170](#F170), [F171](#F171), [F172](#F172). Source scope и статус сохраняются.

## Карта цепочки с версионными швами

| Этап/место | Подтверждено документацией / source | Версии и недостающее звено | Условие допуска |
|---|---|---|---|
| Checkpoint → export, подготовительный CPU/GPU host | [S138](SOURCES.md#S138) вызывает Ultralytics YOLO.export; [S142](SOURCES.md#S142) имеет общие зависимости | Exact weights/hash, torch и Ultralytics не pinned; `onnx~=1.16.0` не exact package lock; opset13 — default автора | Зафиксировать checkpoint/config/classes, exporter commit+packages, полную export call, ONNX hash/IR/opsets |
| ONNX → TF, framework host | [S133](SOURCES.md#S133) importer onnx_direct; [S139](SOURCES.md#S139) может tpu_framework/onnx_direct, simplification retries | Название importer установлено; его версия и accepted op attributes неизвестны | Сохранить importer version, исходный/изменённый graph, mapping, errors; сопоставить float outputs на одинаковых тензорах |
| TF → QM, framework host | [S133](SOURCES.md#S133) QuantizedModel.quantize; [S139](SOURCES.md#S139) RegularModel.calibrate/quantize | API поколений расходятся; exact precision scheme и supported external QDQ/QAT imports не установлены | Подтверждённые actual signatures; calibration list/hash/preprocess; actual effective ranges/settings, tensor parity |
| QM → Network → executable, framework host | compile_ и target, tensor descriptions; [S139](SOURCES.md#S139) set_batch | Guide document-ID не wheel release. O1/O5 semantics не установлены; compatibility target/driver/runtime неизвестна | Compile report + target+batch+preset+versions; сохранить .qm и .tpu hash; compiler success не заменяет quality test |
| executable → .tpu | [S133](SOURCES.md#S133) TpuProgram boundary Framework→SDK | Binary compatibility across releases/targets неизвестна | Один tested package bundle или явная vendor compatibility matrix |
| .tpu → device predictions, LinQ host | [S133](SOURCES.md#S133)/S08 pytpu.Device/open/load/inference.sync | Real server interface, permissions, SKU/count, firmware/driver/libtpu/runtime unknown | Устройство реально обнаружено, actual .tpu загружен; finite outputs, полный IO, raw predictions и timing/log evidence |
| predictions → detector/pose/event, host | [S043](SOURCES.md#S043) host NMS; [S133](SOURCES.md#S133) отдельный пользовательский preprocess/postprocess | Custom nc/pose output contract неизвестен до реального graph. Tracking/events — вне compiler example | Explicit class/schema/geometry/NMS; staged gate W1-04/05/11/12 и event replay |

Framework preparation **не требует GPU по приведённому guide**: указан обычный Linux host с CPU/RAM. Но guide не доказывает возможность произвольной cross-compilation на Windows, ARM или без всех закрытых зависимостей. Runtime example перечисляет локальные TPU devices; удалённый сервис не является тем же интерфейсом. Отдельная машина компиляции и машина inference возможны как архитектурный вывод из `.tpu` boundary, но разрешение remote custom upload и совместимость должны быть выданы явно.


## Какие «поколения» нельзя смешивать

| Контекст | Дата/обозначение | Что точно означает |
|---|---|---|
| Старый Python runtime | iva-tpu11.2.6, 2021; pytpu15.0.21, 2023 | Исторические PyPI metadata/examples. Их API не руководство по current SDK. |
| Официальный operator guide | 2025, RU.РМДВ.04.06.014-03 34 01 | Версия документа/программы по обозначению; не доказанный номер wheel. Python3.11. |
| Официальная страница software | Публикация неизвестна; Python3.8 | Маркетингово-описательная страница, не lockfile. Противоречие guide требует актуального package manifest. |
| Сторонний bench source | Commit 2026-04-03; сценарий dated 2026-03-25 | Exact исходники и ряд ожидаемых dependencies, без exact SDK environment; есть адаптация к несовместимым вариантам API. |
| Официальный benchmark | Презентация 2026; Runtime16.18.6, Framework2026.8.43 | Версии конкретного опубликованного тестового окружения, не гарантированно выдаваемого хакатону. |
| HX раздел сайта | PyTorch≥2.0, ONNX≥1.15; RK3588 | Сведения именно HX; не общая нижняя/верхняя граница importer для любого LinQ H1 host. |

Общее имя `libtpu` нельзя использовать как достаточную идентичность пакета: в стороннем LinQ сценарии требуется vendor stack. Google Cloud TPU — другая платформа; её XLA/JAX/Cloud TPU возможности и пакеты в эту карту не входят.


## Сценарии доступа и действия без выдуманных интерфейсов

Полный кейс уже найден: `_WORK/INPUT/CASE_LINQ.pdf`; сведения о с.8 взяты из первичного локального конспекта root `CASE_NOTES.md`, без повторного визуального чтения этим агентом. Организаторы обещают удалённую VM с LinQ и inference service. Фактический grant здесь не получен. SSH, REST endpoint, token type, custom model upload, quotas и file upload protocol **в кейсе не определены**. CPU+TPU и загружаемое видео — рабочие предпосылки команды, не установленный API.

| Возможный grant | Что можно реально доказать при получении | Чего недостаточно для custom deployment |
|---|---|---|
| Только готовый inference service | Выполнение перечисленной service model; reproducible inputs/outputs; provider-side version/device evidence, если сервис их отдаёт | Нельзя обещать собственные веса, export/compiler control, raw outputs или layer diagnostics |
| VM + runtime + готовые .tpu | Проверить vendor example и фактическое TPU execution; применять postprocessing/events на host | Нужен framework/compiler доступ либо готовый custom artifact от authorized pipeline |
| VM + framework/compiler/runtime | Строить полный staged route в утверждённом окружении | Нужны operator constraints, compatible package manifest и raw artifacts; root/admin права не подразумеваются |
| Local preparation SDK + remote runtime | Compile на разрешённом preparation host и передать .tpu | Требуется binary compatibility и явно разрешённый upload; не выдумывать SCP/REST команды |


## Статусы доказательств

- **Marketing/vendor claim:** официальный family list, PyTorch через ONNX, full stack, Cloud TPU/demonstration availability.
- **Documented interface:** [S133](SOURCES.md#S133) ONNX/TF/QM/Network/compiler/TPU boundary и runtime example; точный SDK release не закреплён.
- **Public source example:** [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S043](SOURCES.md#S043), [S140](SOURCES.md#S140), [S141](SOURCES.md#S141), [S142](SOURCES.md#S142) — реальные readable scripts с pinned commit. **Полностью публичная executable reproduction с приложенным SDK/weights/QM/TPU/outputs не установлена.**
- **Published third-party result:** [S140](SOURCES.md#S140) автор сообщает завершённые vendor TPU runs и незавершённый segmentation O5; это авторский статус, без изученных raw metric artifacts. Не используем его как свою измеренную accuracy/FPS. [S137](SOURCES.md#S137) — vendor benchmark, иной evidence class.
- **Actual test by our team:** модели/TPU/compile не тестировались. Подтверждены только metadata, HTTP source retrieval и равенство 6 raw files pinned blobs.
- **Unknown/requires access:** конкретная предоставленная среда, custom graph support, operator matrix, formats beyond documented TF/ONNX, numeric scheme details, binary compatibility и remote API.

Пересечения: W1-02 определяет фактический exporter; W1-04 — полный output contract и дефекты custom-nc adapters; W1-07 — effective calibration; W1-08 — QDQ/QAT границы; W1-09 — mixed precision. Их общие APIs не приписываются LinQ. Соседний linq_platform дал полезные leads; его shape/helper probes и аппаратные заявления не присвоены этой веткой.

## Контекст W1-14

Основания: [F173](#F173), [F174](#F174), [F175](#F175), [F176](#F176), [F177](#F177), [F178](#F178), [F179](#F179), [F180](#F180), [F181](#F181), [F182](#F182), [F183](#F183), [F184](#F184), [F185](#F185). Source scope и статус сохраняются.

## Fidelity risk register LinQ

Серьёзность — наша инженерная оценка при данном кейсе, не опубликованный severity производителя. Признаки — ожидаемые механизмы, не наблюдённые у нас аппаратные ошибки.

| Risk-ID / серьёзность | Признак | Основание | Проверка | Обход/следующее действие |
|---|---|---|---|---|
| R14-01 critical: custom output | Shape error/AttributeError либо неверные классы после успешной TPU загрузки | [F181](RAW_FACTS.md#F181)/F10 | E01: nc1/2/3, обе оси, shuffled multioutput | Явный manifest и named outputs; исправить адаптер до PTQ. |
| R14-02 high: percentile ignored | Разные requested policies имеют одинаковые thresholds/outputs; успешный summary без effective config | [F174](RAW_FACTS.md#F174)/F03 | E02/E03 | Не ловить blanket TypeError; получить matching API и сохранить effective args/branch/error. |
| R14-03 critical: wrong numeric boundary | Значения scores/boxes неверного масштаба, integer codes как probabilities или двойное scale | [F178](RAW_FACTS.md#F178), [F179](RAW_FACTS.md#F179), [F180](RAW_FACTS.md#F180) | E04 | Получить `.tpu` user/raw spec; native supported boundary adapter ровно один раз. |
| R14-04 high: calibration selection/preprocess | Качество страдает на пыли/дальних СИЗ/других камерах, а общий smoke top1 проходит | [F176](RAW_FACTS.md#F176)/F05/F13; кейс с.5 | E02/E06 | Сохранить фактические hashes preprocessed tensors и coverage manifest; calibration/tuning/test по эпизодам. Методику W1-07 не заменять первыми500 COCO. |
| R14-05 high: SDK generations | Конвертер работает только через retry, API/signatures отличаются; ambiguous platform | [F183](RAW_FACTS.md#F183)/F12 | E02 | Pin wheel/native/compiler + matching example; не подставлять старые helpers. |
| R14-06 high: unsupported precision/QAT | QDQ принимается, но scales/границы/precision перестроены; quality rescue не доходит до TPU | Unknown target support; W1-08/09 | E05 | До обучения маленький semantic import/compile proof с inspectable encodings; иначе vendor PTQ либо совместимая архитектура. |
| R14-07 high: compiler numeric drift | Quantized reference проходит, TLM/TPU расходится; меняется после preset | [F183](RAW_FACTS.md#F183)/F13 | E04/E05 | Один `.qm` parent, сравнить supported baseline preset и optimized; сохранить report/logs. |
| R14-08 high: скрытое усечение/NMS | Слабые/перекрытые кандидаты исчезают при схожих raw tensors | [F182](RAW_FACTS.md#F182); W1-04 | E01/E06 | Проверить graph output stage; один закреплённый postprocessor для диагностической пары, production отдельно. |


## Контекст W1-15

Основания: [F186](#F186), [F187](#F187), [F188](#F188), [F189](#F189), [F190](#F190), [F191](#F191), [F192](#F192), [F193](#F193), [F194](#F194), [F195](#F195), [F196](#F196). Source scope и статус сохраняются.

## Три условных маршрута

Ни один маршрут пока не подтверждён. Выбор определяется выданной инструкцией и capability smoke, а не названием VM.

| Режим | Реально допустимая процедура после выдачи доступа | Граница вывода / когда HOLD |
|---|---|---|
| **Полный SDK + custom models** | Зафиксировать installed versions/device; compile/run только разрешённые custom artifacts; checkpoint→export→quantized→compiled lineage; replay одинаковых tensors на source и target; dumps на доступных границах; затем server video run. Принимаем выбранные shapes/batches/classes, независимо GT и E2E | Отсутствующий float target/intermediate оставляет причинную attribution неполной; наличие SDK не обещает FP32/mixed precision. Custom upload до подтверждения недопустим как факт. Требуются все нейросетевые artifacts, включая pose/ReID/temporal, а не только detector |
| **Ограниченный сервер** | Использовать доступные executable/service/config и разрешённые файлы. Сохранить checksum доступного artifact, version output, stdout/stderr, job IDs; frozen frame или clip replay через существующий путь. Если raw outputs нет, сравнивать canonical boxes/events и GT; попросить готовый trace по выдаваемому интерфейсу, без внешней связи в этом исследовании | Нельзя локализовать quantization/compiler отдельно от скрытых preprocess/decoder. Нет доказательства lineage или device → HOLD соответствующего claim, хотя end-to-end качество можно измерить |
| **Только каталог моделей/готовый сервис** | Закрепить catalog model ID+revision+service version+config, поддерживаемый input, job/result IDs. Выбрать только объявленные классы/сценарии. Проверять black-box качество/время/пустые и ошибочные ответы на независимых clips; использовать supplied reference только при точной версии | Если исходные weights/config неизвестны, **«качество переноса checkpoint→LinQ сохранено» не проверяемо**. Можно утверждать лишь качество конкретного сервиса на corpus. Даже тот же display name pretrained-модели не baseline. Нет source reference → baseline fidelity N/A, не fabricated PASS; device скрыт → proof HOLD |

Во всех режимах neural inference на LinQ обязателен по кейсу. Предлагаемое host распределение: demux/decode, geometric preprocessing, очереди, canonical decode/NMS, tracking/rules/journal — CPU, neural graph — TPU. Это **проектная гипотеза**, а не установленное распределение сервиса. Если NMS встроен в граф, не выполнять повторно; CPU Kalman/rules не равны CPU fallback нейросети. Дополнительные neural pose/ReID требуют своего target proof.


## Контракт данных и журналов для приёмки

Следующие поля — **предлагаемая схема артефактов команды**, не существующий LinQ API. Недоступное поле писать `unknown` с причиной, не заполнять догадкой. Различать `not_applicable`, `not_exposed`, `not_collected`.

- `run_manifest`: run_id, source/candidate IDs, exact source commit/checkpoint/export/compiled hash либо service revision, decoder/preprocess/class-map/skeleton/tracker/rules/config hashes, compiler/runtime/driver/OS реально полученные versions, hardware/device model/ID, capabilities/access restrictions, calibration IDs отдельно от evaluation, shape/batch/dtype/quant parameters, warmup/concurrency/scheduler policy, acceptance-contract ID.
- `media_manifest`: immutable clip_id, original bytes hash+size, supported container/codec/profile/pixel-format/bit-depth/dimensions/rotation/color metadata, time_base/start/time origin, decode library+build+backend, license/provenance, camera/session/epoch, source intervals. Extension `.mp4` не определяет codec/profile. Transcode — новый artifact с hash и source mapping; baseline обязан получить тот же decoded content или сравнение явно confounded.
- `frame_ledger`: clip/stream/epoch/frame_uid, presentation index, original PTS и time_base, effective presentation time, decode status, rotation/color/resize/pad/ROI transform, decoded pixel hash и input tensor hash+name/shape/dtype/layout/range/quant scale+zero point+axis; schedule/enqueue/start/complete/output status и reason. Повторяющиеся PTS требуют уникального frame_uid. Packet DTS не заменяет presentation PTS. Missing timestamps — явная согласованная synthesis policy, не молчаливый `index/FPS` для VFR.
- `job_ledger`: immutable job/model/artifact/device IDs, batch slot→frame_uid, real/padded slots, retry/attempt IDs, submit/start/complete/timeout, output count/schema/hash, transport/service/runtime errors, device-trace link, stale/duplicate/reordered status. Timeout не доказывает cancel; поздний ответ сохранять и не применять повторно. Zero detections — успешный явный `empty`, не отсутствие строки.
- `prediction_ledger`: именованные raw outputs, dtype/shape/finite checks/quant metadata где доступны; decoded boxes/pose/score/class, image coordinates convention и clipping, original W/H, inverse transform, pre/post threshold/NMS settings; rejected candidate reasons. Если сервис даёт только final boxes, raw boundary `not_exposed`.
- `event_delivery_ledger`: camera/epoch/actor/episode/type/zone, evidence frame IDs+PTS, state transitions/reasons, event onset/end uncertainty, created/submitted/received/visible times с clock domain, dedup/retry/ack, payload hash/screenshot/clip path. Evidence не из будущего, delivery не подменять временем file PTS.

Полнота по batch slots сверяется set-wise: каждый scheduled frame имеет terminal status — completed(nonempty/empty), rejected, decode failure, dropped или unresolved. Retries не увеличивают число исходных кадров. Padded копии не превращаются в processed source frames. Для finite fixed run сумма статусов и roster должна замыкаться; unresolved означает незавершённую приёмку, даже если средние метрики хороши.


## Лестница доказательств TPU и ограничения

Это предложенная классификация свидетельств, не vendor стандарт:

1. **Specification:** кейс требует TPU, vendor обещает поддержку. Доказывает постановку, не run.
2. **Inventory/config:** runtime/version/device перечислен, модель выбрана. Доказывает наличие/выбор, не завершение.
3. **Correlated hardware run:** конкретный artifact/session/device/input/output completion и доступные runtime logs. Основной engineering proof для открытого SDK.
4. **Placement evidence:** compiler/partition/execution/profiler trace покрывает neural graph, включая additional heads/ReID. Позволяет ограниченное утверждение о размещении; device-wide utilization — только corroboration.
5. **Service attestation:** если 3/4 скрыты, supplied job/model/device trace либо подтверждение оператора — косвенное свидетельство с названным происхождением. Нельзя повышать его до собственного hardware observation.

Проверять признаки fallback по фактическому contract: изменился backend/model revision, kernel placement, runtime предупреждение о CPU neural execution, device error→успешный ответ другого neural path. Отсутствие предупреждения не доказывает absence fallback. В проверенном [S043](SOURCES.md#S043) нет явной автоматической CPU neural ветки; **это чтение конкретного файла**, не доказательство отсутствия fallback внутри библиотеки или production service. TLM/TF reference сами по себе не fallback; наличия torch на host недостаточно для обвинения в GPU inference.


## Контекст W2-07

Основания: [F246](#F246), [F247](#F247), [F248](#F248), [F249](#F249), [F250](#F250). Source scope и статус сохраняются.

## Аналитические примеры: не результаты нашей модели

Чистая арифметика в JavaScript `Math.pow/Math.log`, без model/runtime/SciPy execution; исходные числа и полная точность в [analytical_examples.json](_WORK/MATERIALS_W2_07/analytical_examples.json). **α=.05 выбрано только для иллюстрации**, не требование кейса. Каждый пример предполагает один заранее заданный endpoint/фиксированный n или T, отсутствие selection и описанные [F247](RAW_FACTS.md#F247)/F03 модели.

| Гипотетические независимые положительные эпизоды n, все обнаружены | 95% one-sided U miss | L recall |
|---:|---:|---:|
| 5 | 45.07% | 54.93% |
| 10 | 25.89% | 74.11% |
| 20 | 13.91% | 86.09% |
| 50 | 5.82% | 94.18% |
| 100 | 2.95% | 97.05% |
| 300 | 0.994% | 99.006% |

Таким образом, “все 20 прошли” честно описывает roster, но в iid модели нижняя 95% граница recall — лишь 86.09%. Верхний endpoint стандартного **двустороннего** 95% CP при 0/20 был бы 16.84%, поскольку там α/2: различие не исправляется переименованием интервала.

Для условной будущей цели `U_miss≤p*` при нуле miss нужно `n≥ceil(ln α / ln(1−p*))`, `0<p*<1`. Только иллюстрации: p*=10%→29, 5%→59, 1%→299 независимых эпизодов. Это план при лучшем исходе 0 miss, не обещание мощности, не минимальное число клипов кейса и не гарантия PASS: если появятся miss, расчёт и требуемый n изменятся. План должен заранее включать stop rule; наращивать n до первого красивого CI и применять fixed-n coverage нельзя.

| Гипотетическое полное exposure T, false=0 | 95% upper false/camera-hour |
|---:|---:|
| 1 camera-hour | 2.99573 |
| 10 camera-hours | 0.29957 |
| 100 camera-hours | 0.02996 |
| 300 camera-hours | 0.00999 |

Для условной rate cap `λ*` при нуле false: `T≥−ln α/λ*`; например λ*=0.01/camera-hour требует не менее 299.573 camera-hours **в данной модели**, а не “300 часов гарантируют безопасность”. Exposure — сумма длительности объединения заявленных исходных интервалов по камерам; не время ускоренного replay и не сумма длительности дублирующих нарезок одной камеры. Full alert census и adjudication обязательны; если count относится только к negative intervals, назвать его `false rate on declared negative exposure`, не general all-stream burden. Duplicates хранить отдельно. Отсутствие срабатываний без complete GT не доказывает recall.


## Парная regression: выигранный TP не отменяет новый miss

Гипотетически у 100 GT эпизодов frozen A/B: A+/B+=79, A+/B−=1, A−/B+=1, A−/B−=19. A и B имеют по 80 TP, net Δrecall=0; **один новый miss есть**. Если этот ID входит в заранее must-pass roster, его FAIL не компенсируется gained TP. Это не измерение и не предложенный must-pass норматив.

Нужно хранить четыре клетки, сами ID и unknown/incomplete, отдельно absolute B recall, новые потери и gains. Если интересует `p_reg=Pr(B− | A+,GT+)`, denominator — baseline-success GT episodes, не все GT и не все disagreements. При **нуле** regressions среди гипотетических 80 независимых baseline-success эпизодов upper bound был бы 3.675%; это условный риск, не B absolute miss rate и не CI разности recall. Условный denominator допустим лишь при fixed A/политике и обоснованном iid sampling этой условной группы. Если A слаб, даже идеальная fidelity не закрывает absolute quality.

Binomial CP не является универсальным interval для AP, OKS, HOTA или paired Δrecall. Для nonzero misses SciPy pinned route позволяет exact CP с теми же независимыми предпосылками. Образец API **не исполнен** (основание [S185](SOURCES.md#S185)): `binomtest(k=misses,n=n,alternative='less').proportion_ci(confidence_level=1-alpha,method='exact')`; для lower detection probability считать successes и `alternative='greater'`. Значение тестового p по умолчанию не участвует в расчёте этого CI; его p-value не служит доказательством эквивалентности.


## Где exact population claim прекращается

1. **Clustering.** Один incident с 1000 кадрами — не 1000 trials. Общие камера/смена/свет/человек/синхронные камеры создают зависимости. “У нас 300 событий” без lineage ничего не устанавливает об эффективной независимости. Нельзя вычислить произвольное `n_eff` и назвать подставленный CP exact. Если redefining trial как “cluster содержит хотя бы одну ошибку” обоснован и clusters iid, bound относится к cluster failure probability, а не event recall. Его нужно назвать иначе.
2. **Heterogeneity.** Camera mix, sites, day/night и severity требуют заявленного estimand/weights. Независимые Bernoulli с разными p_i — уже не один Binomial(n,p). Independent Poisson источники с разными фиксированными rates можно суммировать для exposure-weighted mean на этом фиксированном mix, но pooled bound не гарантирует cap каждой камеры или нового site. Bursts/overdispersion, cooldown, outage, human review delays могут нарушить Poisson assumptions. Сохранить counts/exposure per camera/session; при неизвестной модели — descriptive и сбор независимых сессий.
3. **Selection.** Calibration/thresholds/precision/candidate selection на test делает final fixed-policy claim неподтверждённым. Winner freeze на dev→новый independent holdout. Несколько required endpoints/slices, совместное confidence и correction/stop plan определить заранее; четыре отдельных 95% interval не превращаются автоматически в одновременное 95% утверждение. Не превращать post-hoc “удачный редкий класс” в primary endpoint.
4. **Missingness.** Необработанные кадры, censored follow-up, потерянные replies, неизвестная visibility/identity не считаются успехом или нулём ошибок. В complete GT operational replay outage может быть miss; если truth/logs incomplete, итог INCONCLUSIVE. Пропущенные разделы record нельзя скрыть средним AP или success-only latency.


## Единый acceptance record W2-07-AR01 — заполняемый, сейчас OPEN

**Тип: proposal, не подписанный quality contract.** Одна запись связывает detection+pose+tracking+events и device evidence. Она должна получить `record_id/version/date/approvers`, immutable A/B bundle hashes, scope claim, dataset/GT/evaluator/policy versions, measurement ledger и итог по каждому required gate. Заполнение numeric budgets происходит **до** evaluation/winner selection. Сейчас реальные outputs/GT/device trace отсутствуют; “measured=0 errors” нигде не заполнено.

Статусы полей независимы: **TEAM_DECISION_PENDING** — нужен выбор владельца; **DATUM_MISSING** — конкретный артефакт не получен; **NOT_EXPOSED** — полученный интерфейс действительно не раскрывает поле, с observed evidence и датой; **MEASURED** — значения из actual run с IDs/logs. Неизвестный будущий интерфейс — DATUM_MISSING/observability unknown, а не уже установленное NOT_EXPOSED. **NOT_APPLICABLE** разрешается только с записанной причиной и сужением claim.

| Поле одной записи | Что должно быть заполнено | Текущий factual status | Адресат/способ закрытия |
|---|---|---|---|
| Claim/scope | сценарии/исключения; fixed roster или population; камеры/условия; критические slice/ID; intended deployment | TEAM_DECISION_PENDING | Product/risk owner + CV lead; approved scope и изменение claim при исключениях |
| Truth/data | licensed source IDs/hashes, camera/site/session/incident lineage, train/calib/dev/holdout split, frozen sample list, negative intervals, independent labels/review/unknown, complete follow-up | DATUM_MISSING | Data/annotation owner; manifests+GT, права и independent adjudication; source predictions не GT |
| A/B contract | checkpoint/config/classes/skeleton, preprocess/decoder/NMS/thresholds, tracker/rules/zones/reset, source/export/quant/compiler versions/hashes; same source schedule | DATUM_MISSING | Model/CV and platform owner; lineage bundles; нельзя назвать comparison quantization-only при confounded chain |
| Acceptance policy | α/sidedness/estimand, δ/non-inferiority, absolute floors/caps, critical invariants, split/selection/multiplicity/stop plan, minimum observable duration, deadlines and alert boundary | TEAM_DECISION_PENDING | Risk owner + evaluation lead; signature/version before test. Уточнение “несколько секунд” у постановщика |
| Detection | canonical output + independent GT; evaluator/config; per-class/size/occlusion/light AP, frozen TP/FP/FN, A/B-only IDs, absolute B и Δ | DATUM_MISSING; actual measurements NOT RUN | CV/evaluation owner; paired runs и full ledger, denominator/empty slice явно |
| Pose | skeleton/order/sigmas/visibility/scale; GT joints and unmatched people; OKS/PCK либо chosen metric/units, critical joint slices, A/B delta | DATUM_MISSING; NOT RUN | Pose/evaluation owner. Если pose не используется, approved NOT_APPLICABLE со scope; hidden joints не считать видимыми |
| Tracking | GT identity/continuity/re-entry; fixed reset/order, DetA/AssA/HOTA или выбранный metric, switches/fragments, wrong-person IDs | DATUM_MISSING; NOT RUN | Tracking/annotation owner; continuous labelled clips; track numeric ID equality не gate |
| Events/alerts | episode/person/type/zone/onset/end truth; causal evidence, deadline/matcher; four paired cells+IDs; timely recall, late/unknown/missed; false and duplicate burden/exposure; alert content/journal | DATUM_MISSING; NOT RUN | Event/product/evaluation owners; complete source→visible-alert census и follow-up. Count/duration matching policy согласовать |
| Timing/completeness | source PTS/epoch, actual consumed/dropped frames, submit/completion/delivery boundary, clock mapping, timeout/drain/close, latency quantiles+n+misses | DATUM_MISSING; NOT RUN | Runtime/architecture owner; trace closed window; finite clocks и boundary contract |
| LinQ/device + observability | granted interface/version, artifact/model ID, actual device/completion/output correlation, partition/fallback/profiler/raw/intermediates availability | DATUM_MISSING; exposure unknown; actual device UNVERIFIED | LinQ engineer/platform owner; matched trace and interface inventory. После получения mark truly NOT_EXPOSED boundaries; не выдумывать API |
| Actual outcomes | metric estimates+uncertainty assumptions, counts/exposure/independent groups, limit comparisons, worst IDs, source→final и adjacent deltas, required gate statuses, not-exposed/confounded edges | **MEASURED: none; NOT RUN**, acceptance HOLD | Evaluation lead assembles evidence; missing/inconclusive gates нельзя отмечать PASS |
| Decision/rollback | PASS(scope)/FAIL/HOLD/INCONCLUSIVE по каждому gate и overall, approver/date, unresolved risk owner, rollback complete bundle | **HOLD: contract/data/device inputs missing** | Team approver; all required gates passed only within explicit scope. Нет автоматического production/safety release |

Decision semantics: confirmed hard invariant/approved budget failure→FAIL; absent agreed policy/artifacts→HOLD; valid measurement but insufficient precision/coverage/model assumptions→INCONCLUSIVE. Narrow fixed-fixture PASS допустим только после actual complete replay и заранее определённого engineering criterion. Если интерфейс не раскрывает intermediate tensors, parity там NOT_EXPOSED; end-to-end quality при независимом GT остаётся возможна. Если исходный artifact недоступен, source-to-target fidelity не становится “0 loss”.


### Три ограничивающих исхода для того же AR01

| Реально возможный будущий сценарий | Допустимый claim после actual run | Нельзя заключить | Что остаётся/владелец |
|---|---|---|---|
| Малый фиксированный regression pack, ранее использованный для debug | “На перечисленных complete fixtures при policy hash X новых regressions R; все frozen must-pass прошли” — лишь если ledger это показывает | Population recall=100%, безопасность, independent test accuracy | Coverage/generalization INCONCLUSIVE; data owner собирает другие независимые cameras/sessions/rare episodes; risk owner определяет scope |
| Independent grouped holdout есть, rare class имеет 0 или несколько GT positives | Для n=0: “recall редкого класса не оценён”; при n>0: descriptive count и допустимый CI только при assumptions; остальные slices отдельно | Overall PASS обязательного rare endpoint из общего mAP или из нуля наблюдаемых misses; negatives не добавляют positives | Data owner/постановщик дают rare GT; evaluator планирует additional untouched sample/design; risk owner принимает ограниченный scope или ждёт, не “докупает” significance ретестами |
| Каталог готовых моделей, source checkpoint/config/raw outputs не выданы | Измеренное service-to-GT качество на corpus + документированный model ID; доступная completion/device attribution отдельно | Source→export→quant fidelity и причинная “потеря INT8”; весь graph на TPU по одному API response | LinQ engineer запрашивается artifact mapping/checkpoint/reference outputs/partition evidence; unavailable boundaries NOT_EXPOSED после факта; team выбирает service-quality claim и отмечает fidelity unavailable |

