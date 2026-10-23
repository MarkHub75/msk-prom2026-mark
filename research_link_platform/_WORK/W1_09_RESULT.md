# W1-09 — LinQ: runtime API, артефакты и условные режимы online-доступа

Дата фактической проверки: 2026-10-23, 04:26–04:31 Europe/Moscow (01:26–01:31 UTC). Исходный контекст исследования — подготовка к хакатону 23–25 октября 2026. SDK не установлен; native runtime, LinQ и реквизиты удалённого доступа не предоставлены. Проверены сетевые первоисточники, сохранённые исходники и статические свойства кода. Аппаратный inference не выполнялся.

## Главный вопрос и ответ

Каким конкретным интерфейсом сервис сможет загрузить модель на LinQ, выполнить inference и получить результат, и что означает обещанный online-доступ?

Официальный guide документирует локальный Python-путь `pytpu`: перечисление устройств → открытие устройства → загрузка `.tpu` → создание inference session → блокирующий вызов со словарём входных ndarray → словарь выходов. `.tpu` — граница между подготовкой графа в TPU Framework и исполнением в TPU SDK; это инструкции с константами/весами, а не обычный ONNX или checkpoint. Сетевой протокол хакатона по найденным источникам установить нельзя. SSH, container, runtime-only и HTTP остаются сценариями архитектуры, а не реквизитами доступа. [W1-09-F01,F02,F12]

Новая самостоятельная находка — публичный **исторический `pytpu 15.0.24`** 2023 года: sdist содержит ровно семейство `Device/Program/Inference`, совпадающее с официальным guide, и ctypes bindings к `/usr/lib/libtpu.2.so`. При этом README/PyPI description показывает старый `iva_tpu/TPUDevice` интерфейс. Поэтому по README нельзя выбирать API, а `pip install pytpu` нельзя считать установкой работоспособного LinQ runtime 2026. Родство API подтверждается; совместимость ABI, `.tpu` и железа 2026 — нет. [W1-09-F03–F08]

Инженерное значение: заранее отделить host adapter, который принимает подготовленный tensor и возвращает raw model outputs, от декодера модели, NMS, трекинга и правил. После выдачи доступа сначала получить версионную матрицу и выполнить один официальный `.tpu` с известным входом/выходом; затем пробовать собственную модель. Нельзя проектировать интеграцию вокруг выдуманного HTTP endpoint.

## Метод и обозначения

Тип свидетельства (`primary_documentation`, `source_code`, `vendor_statement`, `local_observation`, `inference`, `unknown`) указан отдельно от выполненной проверки. Чтение кода не считается запуском. Source IDs локальные, источники описаны ниже. Ветки compiler/calibration/models принадлежат W1-06/07/08; здесь разобрана граница исполнения.

## Отдельные факты

### W1-09-F01 — официальный локальный Python runtime

- Тип: `primary_documentation`; выполненная проверка: прочитан сохранённый извлечённый текст guide; новый web open PDF вернул Internal Error.
- Источник: W1-09-S01, §3.4, печатные pp.20–21; extracted lines 547–592.
- `Device.list_devices()` описан как поиск устройств **в локальном хосте**. Далее используются context managers `Device.open(...)`, `device.load(path)`, `program.inference()` и `inference.sync(input_dict_with_op_names)`.
- `sync` — блокирующий вызов. Вход — именованный словарь; выход читается по имени операции. В ResNet примере удаляют суффикс `:0` перед вызовом и восстанавливают tensor name после. Это пример преобразования имен, не универсальное правило для всех экспортов.
- Guide не даёт публичную полную спецификацию runtime/C ABI, ошибки всех методов, потокобезопасность, multiprocess semantics или сетевой API.

### W1-09-F02 — `.tpu`, веса и место компилятора

- Тип: `primary_documentation`; проверено чтением S01 §3.4 pp.19–20.
- Framework строит квантованную модель, затем `Network.from_quantized_model(...)`; компиляция выдаёт TLM программу с инструкциями TPU и константами/весами. `TpuProgram.from_executable(...)` и `.to_file(...)` сохраняют `.tpu`.
- Guide прямо обозначает `.tpu` разделительной линией Framework → SDK. Следствие (`inference`): на runtime-only машине может быть достаточно согласованной `.tpu`, без исходного training framework и компилятора. Но возможность компилировать на другой машине и переносимость `.tpu` нужно подтвердить для конкретных версий и target.
- Передача нового `.pt`/ONNX сама по себе не является загрузкой исполняемой программы в этот API. Для обновлённых весов нужен новый совместимый артефакт подготовки, если поставщик не выдаст иной явно поддержанный путь.

### W1-09-F03 — открытый исторический пакет получен и проверен без установки

- Тип: `local_observation` + `source_code`; выполнено: HTTPS PyPI JSON, скачивание sdist, сверка SHA256, безопасное чтение/извлечение отдельных файлов; пакет не импортировался и не устанавливался.
- Источники S02/S03; версия `15.0.24`, release/upload 2023-11-27.
- SHA256: `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`, совпал с PyPI.
- Локально: `W1_09/PYTPU_METADATA.json`, `W1_09/pytpu-15.0.24.tar.gz`, `W1_09/PYTPU_SOURCE/pytpu-15.0.24/`, `W1_09/LOCAL_CHECKS.json`.
- Доступность source distribution не означает наличие native `.so`, драйвера, compiler или права считать пакет актуальным SDK LinQ.

### W1-09-F04 — происхождение и предел атрибуции `pytpu`

- Тип: `source_code`/metadata; проверено чтением PyPI, setup.py, archive manifest.
- PyPI maintainer: `IvaTechnologies`; author: `IVA-Tech`; `author_email='info@iva-tech.ru'`; homepage `http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk`.
- В `_bindings.py` есть ссылка разработчиков на `https://jira.hi-tech.org/browse/TPU2-2010`. Это внутренний locator в исходнике, не открытый проверенный issue.
- Независимая связь с исследуемым стеком: текущий официальный `/sol` связывает ПО IVA H1 с OEM на LinQ H; официальный S01 импортирует `pytpu` и показывает то же семейство методов. Этого достаточно для исторической технической зацепки, но не для утверждения, что PyPI upload — официально рекомендованный дистрибутив LinQ 2026, или что нынешняя компания контролирует PyPI account.
- В JSON license — пустая строка; license_expression отсутствует; `LICENSE` в sdist не найден; явной лицензии в setup.py нет. Правовой режим повторного использования не установлен. Публичность исходника не равна open-source лицензии.

### W1-09-F05 — реальное API sdist расходится с README

- Тип: `source_code`; проверено статическим чтением S03, `_bindings.py` lines 180–253, 270–425; `__init__.py`.
- Экспортируются `Device`, `Program`, `Inference`, `InferenceError`, `convert_to_raw`. README, напротив, описывает `from iva_tpu import TPUDevice, TPUProgram, TPUInference`; этих экспортов в `pytpu/__init__.py` нет. Исторические README snippets с queue stats нельзя переносить на реальный API пакета без проверки.
- Реальные сигнатуры: `Device.open(dev_name: str)`; `Device.list_devices() -> List[str]`; `Device.info() -> Dict`; `Device.load(program_path: str)`; `Program.info() -> Dict`; `Program.inference()`; `Inference.sync(inputs, mode=ProcessingMode.FULL) -> Dict[str,np.ndarray]`.
- Метода `Inference.run` в этом sdist нет. Его наличие в defensive `hasattr` стороннего кода S04 не доказывает новый API.
- `list_devices` лишь просматривает `/dev`, фильтруя regex `tpu.` и длину имени 4; не делает handshake с accelerator и не гарантирует usable device. Например, двухзначные имена этим историческим фильтром не обнаруживаются. `Device.open` вызывает native create/init/validation; именно это существенно сильнее простого списка файлов.

### W1-09-F06 — ctypes и native runtime

- Тип: `source_code`; проверено чтением S03 `_bindings.py` lines 28–159.
- Абсолютный путь native библиотеки: `/usr/lib/libtpu.2.so`; загрузчик `ctypes.CDLL` ленивый. Python dependency в setup.py — `numpy`; native driver/runtime в pip dependencies не поставляются.
- Поэтому успешный `import pytpu` по конструкции пакета **не доказывает** наличие libtpu, доступ к `/dev/tpuN` и исполнение модели. Аналогично framework import test из guide проверяет import Framework, а не аппаратный inference.
- Реальные native symbol names включают `tpu_create_device`, `tpu_init_device`, `tpu_load_program`, `tpu_create_program`, `tpu_create_inference`, `tpu_run_inference`, `tpu_get_inference_status`, `tpu_get_program_info`, `tpu_get_device_info`. Есть bindings `tpu_submit_inference` с callback, но это не доказательство поддержанного публичного Python async API.
- Для C/C++ это доказательство существования C boundary в исторической `.so`, а не достаточный header/ABI contract. Публичные headers, libtpu download, link flags и современный C++ example в этой ветке не найдены.

### W1-09-F07 — outputs и metadata: конкретный исторический контракт

- Тип: `source_code`; проверено S03 `_bindings.py` lines 270–300, 332–499.
- `Program.info()` возвращает JSON native metadata. Внутри читаются `metadata['inputs']['1']`, `metadata['outputs']['2']`, `metadata['hardware_parameters']`. Входные имена и выходные имена берутся из metadata, а не угадываются по названию ONNX.
- `sync` принимает Mapping; создаёт input/output buffers, вызывает native inference, проверяет return/status codes. Native ошибки оборачиваются в `InferenceError` с `Invalid tpu_run_inference return code ...` либо `Invalid inference status code ...`.
- Для обычной программы результат — dictionary ndarray: dtype через `user_dtype`, shape через `user_shape`. Это реальные model outputs, ещё не events или boxes обязательного прикладного формата. Int8 арифметика ядра не означает, что Python API всегда отдаёт int8.
- Для raw programme output reshapes по `ddr_word_len`; `_is_raw_program` читает ZIP member `metadata.json`, raw heuristic — отсутствие `user_dtype`. Это формат **этого** пакета; не гарантированная спецификация всех `.tpu` 2026.
- Input data передаются через ndarray pointer. Сам код содержит TODO валидации dtype. Следствие: до вызова необходимо явно сверять имена, shape, dtype и C-contiguity; silent preprocessing/layout mismatch нельзя исключить одним успешным вызовом. Не установлен современный zero-copy/lifetime contract.

### W1-09-F08 — CLI и packaging inconsistency

- Тип: `source_code` + `local_observation`; проверены setup.py и полный tar manifest.
- setup объявляет entrypoints `run_get_fps = pytpu.scripts.run_get_fps:main` и `pyrun_tpu = pytpu.scripts.pyrun_tpu_cli:main`. В опубликованном sdist директория `pytpu/scripts` отсутствует. Это статическое несоответствие упаковки: наличие entrypoint не доказывает runnable CLI; запуск не выполнен.
- `convert_to_raw` содержит условие internal dependency для debug conversion. Нельзя обещать пользователю полноценный RAW tooling из одного PyPI archive.

### W1-09-F09 — сторонний код 2026: что именно он добавляет

- Тип: `source_code`; проверен pinned S04 commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, локальный `git rev-parse HEAD` совпал.
- `run_yolov8_tpu.py`: тот же device/load/session; выбирает `run` при наличии, иначе `sync`, пробует несколько имён inputs. Это compatibility probing автора, не документация гарантированных SDK reflection методов.
- Inputs YOLO path: RGB, float32 /255, NCHW, letterbox. Outputs ожидаются rank3 с размерностью 84/85, далее host Ultralytics NMS. Последний batch дополняется повтором последнего изображения; лишние outputs отбрасываются. Эти контракты относятся к модели/runner, а не всем LinQ программам.
- Run-time timing обрамляет один runtime call; preprocessing/NMS за его пределами. Это не end-to-end latency сервиса. Готовых hardware logs этой веткой не получено.

### W1-09-F10 — Unicode defect независимо подтверждён AST

- Тип: `local_observation`; выполнено: `ast.parse` без импорта runner и без TPU, `argparse.Namespace` проверка; результат сохранён LOCAL_CHECKS.json.
- S04 `scr/detection/run_yolov8_tpu.py` line206 обращается к `args.output_tens\u0e2d\u0e23\u0e4c_name` (Unicode escape точного identifier); parser создаёт `output_tensor_name`.
- В Namespace с объявленным parser именем `hasattr` первого атрибута False, правильного True. Если выполнение пройдёт предыдущие file/dependency/COCO checks, обращение вызывает AttributeError **до** `Device.list_devices/open`. Полный runner не запускался; это доказанный identifier mismatch, условный путь к исключению.
- Исправление стороннего примера не доказывает совместимость с установленным runtime и не превращает YOLOv8 path в подтверждённый аппаратный результат.

### W1-09-F11 — практический CLI benchmark и требования хоста в стороннем repo

- Тип: `source_code`/author scenario, не собственное измерение.
- S05 RUN_SCENARIO.txt (2026-03-25) требует отдельное TPU окружение `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`; `/dev/tpu0` отсутствует → пропустить TPU sections. Указанный автором binary path содержит `mlperf-16.16.12-Source/build/mlperf`; это не версия предоставленного нам SDK.
- S06 `run_fcn_resnet50_performance.py` фактически собирает `mlperf -s offline -m performance -p <program.tpu> -q <QPS>`. Binary — внешняя зависимость, в git не поставляется. Авторский wrapper сохраняет stdout/stderr, returncode, `mlperf_log_summary.txt`, проверяет `VALID` и Samples/sec. Такое имя не доказывает официальный MLCommons submission.
- S07 TinyYOLO runner имеет параметры layout/range и host postprocessing разных output layouts. Это показывает, почему вместе с чужим `.tpu` нужны metadata и эталонный postprocess; отсутствие единственного выхода `boxes` не означает неработающий TPU.

### W1-09-F12 — online/cloud: доказано заявление о направлении, не API доступа

- Тип: `vendor_statement`; выполнено: самостоятельный web open текущего S08 `/hr`, S09 HPS datasheet.
- Официальная вакансия C++ говорит о Python prototype облачного inference и C++ пре-альфе. Требования/архитектуру сервиса ещё предлагают формализовать. Это свидетельство разработки cloud inference, но не public GA service и не режим хакатона.
- HPS datasheet p4 называет LinQ Cloud с контейнеризацией/виртуализацией ресурсов. Endpoint, schema, authentication, upload limits, quotas, scheduling и SDK версии там не установлены.
- Конкретные host/IP/token/SSH port, HTTP endpoint и container image для команды неизвестны. Отсутствие найденной публичной спецификации не доказывает, что закрытый сервис или документация не существуют.

## Версии и противоречия

| Материал | Что в нём установлено | Что переносить нельзя |
|---|---|---|
| `/sol`, текущая страница | Python3.8 + CLI для квантования/компиляции, IVA H1 ПО связано с LinQ H OEM | Это не полный runtime install contract |
| Guide 2025, программа `RU.РМДВ.04.06.014-03`, обновляет `-02` | Ubuntu20.04, RAM≥32GB, Python3.11, wheel `tpu_framework-py3-none-any.whl` | Python3.8 marketing и Python3.8 path в старом example log не отменяют формальные 3.11 requirements |
| PyPI `pytpu 15.0.24`, 2023-11-27 | Source API Device/Program/Inference, native `libtpu.2.so`; README старый | ABI с Runtime16.x, target LinQ2026, новый async/reflection API |
| Авторский RUN_SCENARIO 2026-03-25 | TPU venv311 и внешний mlperf-16.16.12 binary path | Наличие пакетов/железа у нас; валидные цифры без logs |
| Vendor presentation2026, сохранённая W1-03 | По handoff: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43 в benchmark context | Не версия обещанного online окружения; новый web open PDF в моей ветке не удался |

Не усреднять версии и не выбирать newest PyPI как обновление SDK. Запросить согласованные versions драйвера, libtpu, pytpu, Framework/compiler, target, Python и формат `.tpu`.

## Условные online режимы и размещение нашего сервиса

Все строки ниже — `hypothesis/inference`, **ни один режим не подтверждён для нашей команды**.

| Если выдадут | Где исполняется runtime adapter | Что необходимо проверить до архитектурного решения |
|---|---|---|
| SSH на TPU host | На удалённом Linux рядом с `/dev/tpuN`; UI/backend могут быть там же или отдельно | Разрешены ли установка deps, long-running service, port forwarding, загрузка моделей/данных; disk/RAM quotas; CPU для decoder/NMS |
| Container с device passthrough | В предоставленном контейнере | Совместимый native runtime, device permissions, host driver, image/venv, shared memory, mounts; обычный GPU-container флаг не является LinQ настройкой |
| Runtime-only session/job | В job на TPU host | Где compiler, кто компилирует `.tpu`, как передать артефакт, совместимость target, batch/shape и limits; доступ к raw outputs/logs |
| HTTP inference service | За vendor network API; наш backend клиент | Реальная спецификация, tensor/image payload, dtype/layout, upload/custom model policy, sync/async, errors/retries, quotas/queue, device execution proof |

Если канал камеры до TPU host неизвестен, не планировать RTSP reachability. Возможный fallback — передавать выбранные кадры с timestamp/frame_id; это наша архитектурная опция, не заявленный vendor transport. Сетевой transfer, decode, resize, inference, postprocess и event latency мерить отдельно. Shared remote accelerator может иметь очередь, поэтому offline throughput из benchmark не определяет tail latency сервиса.

## Проверки сразу после выдачи доступа

1. Получить от инженера exact target и версионную матрицу; записать `python --version`, package versions, путь реально загруженной libtpu и driver/runtime version согласованным с поставщиком способом. Нужен официальный рабочий example для этого окружения.
2. Уточнить тип доступа, compiler availability, разрешение на custom model, limits batch/input/model/disk/session/queue и сетевые ограничения. Если runtime-only — запросить compiler service или совместимый compiler package; не отправлять обычный ONNX в `device.load`.
3. Проверить import, devices, **реальный open + device.info** и загрузку известного `.tpu`; список `/dev` и import — только ранние ступени диагностики.
4. Снять `program.info()` или доступный документированный metadata API именно установленной версии. Зафиксировать input/output names, shapes, dtype, batch, preprocessing и output interpretation. Сохранить artifact SHA256.
5. Один известный вход → raw output arrays и сверка с golden/reference; отдельно postprocess. Если outputs неправильные, проверять layout/color/range/name/dtype/batch раньше, чем обвинять compiler.
6. Запустить несколько повторов после warmup; записать blocking call latency и end-to-end latency. Нагрузку поднимать после correctness, отдельно исследовать batch и очередь. Public async API нельзя выводить из внутренних symbols.
7. Сохранить stdout/stderr, версии, device info, metadata, hashes, raw I/O, timing и test image ID. Для доказательства LinQ использовать documented runtime/device path и подтверждение инженера/мониторинга; timing или имя JSON pipeline сами по себе не доказывают hardware execution. Проверить, что при отсутствии устройства inference падает, а не молча уходит на CPU, в пределах разрешённого окружения.

Это будущие проверки; ни одна не заявлена выполненной на оборудовании.

## Источники и доступ

Все сетевые просмотры этой ветки выполнены 2026-10-23 около 01:26–01:30 UTC. Для HTML без document date дата публикации неизвестна.

- **W1-09-S01** — «Фреймворк IVA H1. Руководство оператора», ООО «ХайТэк»/обозначение `RU.РМДВ.04.06.014-03 34 01`, 2025, https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf . Локальный extracted текст W1-03 `Framework_manual_H1_extracted.txt`; locators §2 pp5–6, §3.4 pp11–21. В моей ветке web open PDF дал Internal Error; не выдаю за повторное чтение оригинального PDF. Извлечённый текст местами содержит переносы/OCR пробелы.
- **W1-09-S02** — PyPI «pytpu 15.0.24», maintainer IvaTechnologies, author IVA-Tech, upload 2023-11-27, https://pypi.org/project/pytpu/15.0.24/ ; metadata https://pypi.org/pypi/pytpu/json . Web open + CLI HTTPS доступны; сохранён JSON. README исторически несогласован с source; publisher identity и права не аттестованы нами.
- **W1-09-S03** — `pytpu-15.0.24.tar.gz`, IVA-Tech (metadata), 2023-11-27, https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz . CLI HTTPS скачивание успешно, hash проверен. Locators `_bindings.py`, `__init__.py`, `setup.py`, tar manifest. Без установки, без libtpu и hardware теста. Author metadata и внутренняя доменная ссылка не доказывают актуальную поддержку.
- **W1-09-S04** — sherstpasha, `linq-cv-bench`, pinned commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` (2026-04-03 по handoff), https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py . Самостоятельный web open и чтение локального pinned кода; locals lines 108–112, 182–236, 260–345. Сторонний пример, не vendor SDK; hardware execution не установлен.
- **W1-09-S05** — sherstpasha, RUN_SCENARIO.txt, date in file 2026-03-25, https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt . Прочитан локальный pinned файл, sections1–3. Авторская инструкция и статусы, не наш тест и не предоставленный environment.
- **W1-09-S06** — sherstpasha, FCN performance wrapper, https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/segmentation/run_fcn_resnet50_performance.py . Локальное чтение lines75–130; CLI/validity logic; native binary недоступен.
- **W1-09-S07** — sherstpasha, TinyYOLO accuracy runner, https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_accuracy.py . Локальное чтение defaults, preprocessing, run_once, input resolution и decode; это recovery heuristics автора, не specification SDK.
- **W1-09-S08** — «Карьера в ХайТэк», ООО «ХайТэк», https://lin-q.ru/hr . Самостоятельный web search/open. Locator «Инженер-программист C++», абзацы Python prototype/C++ pre-alpha, анализ и формализация требований. Дата вакансии неизвестна; возможно страница не синхронна текущей зрелости сервиса.
- **W1-09-S09** — «LinQ HPS», vendor datasheet, https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf , p4 «Runtime и сервисы». Самостоятельный web open PDF доступен, 4pp; дата документа явно не установлена. Marketing statement, без API.
- **W1-09-S10** — «Модули ускорения LinQ», ООО «ХайТэк», https://lin-q.ru/sol . Самостоятельный web open доступен; locator «Программное обеспечение», «Описание», «Функционал». Связь IVA H1/LinQ H и Python3.8/CLI statement; не install manifest.
- **W1-09-S11** — vendor presentation2026 https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf . Новый web open дал Internal Error. Version details в этом файле отмечены только как handoff W1-03, без самостоятельной проверки оригинала.

## Где искали, ошибки и отброшенные совпадения

Самостоятельные web queries: `site:lin-q.ru runtime pytpu SSH API`, `"pytpu" "Device.open"`, `"pytpu" "IVA"`, `"TPU Runtime" "LinQ" API`, `site:lin-q.ru "SSH"`, `site:lin-q.ru "онлайн" "доступ"`, GitHub `"pytpu" "Device"`, общий `"LinQ" "API" "runtime"`. Последний загрязнён Microsoft LINQ, Linq messaging/iMessage API и Automata laboratory LINQ; эти продукты не имеют установленной связи с TPU LinQ и исключены. PyPI `linq-python` не является найденным LinQ accelerator SDK.

`/docs` и два прямых PDF в моей web-сессии дали Internal Error; альтернативы — уже сохранённый официальный guide W1-03 и доступный HPS PDF. PyPI JSON и files.pythonhosted HTTPS доступны. Локальный первичный вывод Unicode identifier в Windows cp1251 дал UnicodeEncodeError; повтор с JSON ASCII escapes успешен. Это console encoding проблема исследовательского check, отдельная от identifier defect runner. Попытка прочитать отсутствующий `pytpu/scripts/pyrun_tpu_cli.py` привела к проверке полного archive manifest и выявила реальное packaging inconsistency.

## Неизвестные и handoff

Не установлены: доступный команде accelerator, текущие libtpu/pytpu ABI и driver; install channels/licensing; portability старых `.tpu`; concurrency/session isolation; real metadata/async API; supported C/C++ API; network endpoint/auth/payload и limits; предоставление compiler; custom model policy; monitoring hardware execution.

Оркестратору: приоритетный вопрос инженерам — **какой фактический путь от нашего ONNX/весов до raw outputs поддержан в выданном окружении, с exact versions и официальным рабочим примером?** Затем спросить режим удалённого доступа и разрешённые способы доказать execution. W1-06 получает historical public source как опорный API boundary, W1-08 — AST confirmation Unicode defect и запрет считать YOLOv8 runner доказательством запуска. Вторая волна может проверить происхождение PyPI через исторический official vendor site и получить открытые native C headers, если таковые доступны; сама по себе новая версия README не решит ABI вопрос.
