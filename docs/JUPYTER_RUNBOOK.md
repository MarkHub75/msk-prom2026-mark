# LQ-01: безопасный захват одного вызова из Jupyter LinQ

Обновление: пользователь успешно выполнил штатный пример — status_code=0, класс257, ответ0,39с. Актуальный комплект: linq-jupyter-kit.zip, инструкции docs/JUPYTER_KIT.md и README внутри ZIP. Код удалённого вызова из example.ipynb пока не передан; нижний пример остаётся явным шаблоном привязки, а не утверждением о сигнатуре сервиса.

Пользователь подтвердил доступ к аутентифицированному Jupyter и наличие штатного `example.ipynb` с программой ResNet50 TPU. Этот доступ не передан агенту. Старый preflight с Vast описывает только сеть и окружение Vast; он не опровергает доступ пользователя. Факт выполнения штатного вызова и его результаты нужно зафиксировать отдельно.

## Что сделать в существующей сессии

1. Открыть предоставленный `example.ipynb` и просмотреть код подготовки входа, загрузки программы и фактического вызова. Использовать уже выполненную штатную настройку. Не запускать неизвестный notebook целиком через «Run All».
2. Найти точные имена входных и выходных тензоров, путь к фактически загруженному `.tpu` и способ ожидания завершения вызова. Наличие переменной со старым результатом не заменяет новый вызов.
3. Загрузить небольшой подготовленный командой комплект `ml/` в рабочую папку Jupyter либо использовать уже доступную копию проекта. Helper требует только NumPy и стандартную библиотеку; он не устанавливает пакеты, не подключает VPN и не выполняет авторизацию. Если импорт не виден, добавить **явно выбранную папку комплекта** в `sys.path`; не печатать весь `sys.path`, окружение или состояние kernel.
4. Привязать код ниже к **существующему вызову из notebook**. Все обозначения в ВЕРХНЕМ РЕГИСТРЕ ниже — места явной привязки, а не предлагаемые имена переменных, методы SDK или удалённые API. Не выполнять ячейку, пока привязки не заполнены.

```python
from ml.linq.notebook import capture_call

# Bind these from the inspected example, without copying auth material:
# EXPLICIT_NUMERIC_INPUTS: dict of exact input names -> preprocessed numpy arrays
# EXACT_OUTPUT_NAMES: list of exact output names to capture
# EXISTING_TPU_PROGRAM_PATH: path of the program actually used by that call
# EXISTING_CALL: a callable wrapping the actual existing notebook call and waiting
#                for its real completion using the supplied example's semantics


def invoke_existing_call(named_inputs):
    # Replace this body with the EXISTING inspected inference expression.
    # Pass named_inputs into that expression at its actual input boundary.
    # Return ONLY the explicitly selected named numeric output arrays.
    # If the SDK returns extra metadata/list items, select the arrays explicitly;
    # do not return the entire result/session object.
    raise NotImplementedError("Bind the existing notebook inference call first")


capture = capture_call(
    run=invoke_existing_call,
    inputs=EXPLICIT_NUMERIC_INPUTS,
    output_names=EXACT_OUTPUT_NAMES,
    program_path=EXISTING_TPU_PROGRAM_PATH,
    output_dir="capture-stock-resnet50-001",  # must not exist already
    model_id="stock-resnet50",
    placement_attested=True,  # only when this is the supplied LinQ runtime call
)
print({"status": capture["status"],
       "call_completed": capture["call_completed"],
       "independently_verified": capture["hardware_placement"]["independently_verified"]})
```

В примере намеренно нет вымышленного `inference.run`, URL сервиса, имени пользователя или структуры ответа. Точное выражение берётся из доступного пользователю notebook. Если оно уже возвращает словарь только нужных массивов, wrapper может непосредственно вернуть этот словарь. Если вызов асинхронный, wrapper обязан дождаться результата штатным способом; отправленный job, Future или старый массив не подтверждает завершённый инференс.

Helper вызывает wrapper **ровно один раз**, без повторов. На вход wrapper получает копию явно переданных массивов; исходные входы сохраняются до вызова. Имя/shape/dtype и границы значений не угадываются, нормализация и деквантование не добавляются.

## Дополнительные явные проверки

При известных ABI можно передать `input_specs` и `output_specs`: словари `имя -> {"shape": [...], "dtype": "float32"}`. Это проверки, а не преобразование типа. `runtime_to_reference` задаёт точное отображение имён выходов runtime на имена эталона; оно должно покрывать все сохранённые выходы и быть взаимно однозначным. Если имена совпадают, карта не требуется. Не подбирать переименование по одинаковым размерам.

Для классификационного штатного примера проверка класса включается **только явно**:

```python
from ml.linq.notebook import ExpectedClass

# Add this argument to capture_call ONLY after checking the actual example:
# expected_class=ExpectedClass(
#     output_name=EXACT_CLASS_OUTPUT_NAME,
#     class_index=EXPECTED_CLASS_FROM_EXAMPLE,
#     axis=CLASS_AXIS_FROM_EXAMPLE,
#     class_offset=CLASS_OFFSET_FROM_EXAMPLE,
# )
```

Нельзя автоматически считать эталонным класс `257` или сдвиг `1`: эти значения встречаются в полученном публичном ResNet-примере, но должны совпасть с фактически запущенными программой, входом и кодом notebook. Не применять классификационный argmax к выходам YOLO.

Для последующего сравнения позы можно явно передать `original_transform` с восемью целочисленными полями: `original_width`, `original_height`, `input_width`, `input_height`, `resized_width`, `resized_height`, `left`, `top`. Это реальные параметры того же preprocessing. Не передавать туда произвольную metadata notebook. Без transform числовое сравнение возможно, а декодирование в исходный кадр должно быть пропущено.

## Что экспортировать

В новой папке захвата сохраняются только:

- `capture.json`: UUID, модель, хеш файла программы, факт возврата вызова, интервалы `call_ms`/`total_ms`, shape/dtype/nbytes и хеши явно выбранных массивов, SHA256 файлов артефактов; дополнительные map/transform только при явной передаче.
- `inputs.npz`: именованные числовые входы с исходными dtype и значениями.
- `outputs.npz`: именованные числовые выходы; существует только после проверки точных имён, типов и конечности значений.

Для чтения: `np.load(path, allow_pickle=False)`. Названия внутри NPZ — точные имена явно выбранных тензоров; не распаковывать ZIP вручную в файловую систему. Каталог создаётся с приватными правами; существующий захват не перезаписывается. Массивы могут содержать изображение: передавать выбранные числовые артефакты только разрешённым способом команды.

`status="completed"` означает возврат одного supplied callable, валидацию тензоров и сохранение артефактов. `call_completed=true` при `status="failed"` может означать, что вызов вернулся, но выходные тензоры не прошли проверку. Несовпадение явно ожидаемого класса даёт `validation_failed`, сохраняя числовые доказательства. Ошибка содержит только этап и тип исключения, без сообщения SDK. Прерывание kernel или неполный каталог не считается успешным захватом.

**Место исполнения — аттестация пользователя/предоставленного runtime.** Helper не доказывает аппаратное размещение независимо и всегда записывает `independently_verified=false`. `call_ms` включает всё, что делает wrapper, и не называется временем вычисления чипа. Вход/выход штатного ResNet не подтверждает работоспособность наших моделей.

Не экспортировать `.ipynb` с выводами, cookies, токены, credentials, конфигурацию VPN, переменные сессии, `globals()`, `locals()`, repr runtime или полные сообщения ошибок. Helper не читает эти источники.

## Если для адаптации нужен код notebook

Подготовить отдельную **копию только выбранного кода**, не notebook целиком. В существующей сессии вручную отобрать только ячейки импорта нужных модулей, preprocessing, вызова и извлечения числовых выходов. Удалить из их source любые логины, пароли, токены, cookies, частные адреса/параметры авторизации; заменить их комментариями без значений. Не выполнять и не передавать ячейки авторизации.

После ручной проверки можно собрать минимальный notebook из очищенных строк:

```python
import json

# Explicit manually reviewed code strings only. Never use all notebook cells.
REVIEWED_CODE_STRINGS = [
    # paste only the credential-free preparation/call snippets needed for adaptation
]
minimal = {
    "nbformat": 4, "nbformat_minor": 5, "metadata": {},
    "cells": [{"cell_type": "code", "metadata": {}, "execution_count": None,
               "outputs": [], "source": source.splitlines(keepends=True)}
              for source in REVIEWED_CODE_STRINGS],
}
with open("example-code-only.ipynb", "x", encoding="utf-8") as file:
    json.dump(minimal, file, ensure_ascii=False, indent=2)
```

Отсутствие outputs/metadata само по себе не очищает секреты, записанные в source; нужна проверка выбранных строк до передачи. Более простой вариант — передать эти же очищенные фрагменты как `.py`. Никаких учётных данных для адаптации не требуется.

## Передача CV Detection

Команде нужны только выбранные `capture.json`, `inputs.npz`, `outputs.npz` и соответствующий эталон/manifest модели. Числовое сравнение выполняет `ml.detection.compare_capture` с явной картой выходов. Проверка класса штатного ResNet — первый smoke; затем отдельно проверяются ABI и наши helmet/split-pose программы. До полученного реального захвата статус аппаратного запуска команды остаётся `NOT_RUN`.
