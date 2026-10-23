# W1-15 — наблюдаемость и доказательство исполнения LinQ

Главный вопрос: какие открыто подтверждённые признаки позволяют связать результаты нашей модели с фактическим исполнением на конкретном LinQ, какие profiler/counters доступны и как исключать незамеченный CPU fallback?

Контекст: исследование, а не реализация прототипа. Пять участников, около 45 часов; точные устройство, runtime, SDK, права удалённого доступа и критерий жюри ещё не выданы. Проверка источников этой веткой: 2026-10-23 примерно 04:34–04:42 Europe/Moscow (+03:00). Точное время одной сетевой загрузки зафиксировано CLI: 04:38:28+03:00; время итоговой проверки файла 04:41:35+03:00. Собственного аппаратного запуска, экспорта, компиляции, замера LinQ или удалённого сервисного запроса не было.

## Вывод и инженерное значение

Открытые материалы позволяют подготовить **цепочку свидетельств исполнения**, но не дают готовой современной команды вроде `linq-smi`, документированной схемы аппаратных счётчиков или публичного no-fallback переключателя. Такие команды нельзя придумывать. Официальный HPS datasheet действительно называет Performance Profiler и DNN Stat; это основание запросить инструменты, а не утверждать их доступность в выданном окружении.

Самая конкретная доступная реализация — исторический `pytpu 15.0.24`, опубликованный 2023-11-27. В ней обнаружение устройства — лишь фильтрация имён каталога `/dev`; импорт пакета не загружает native библиотеку. Более сильный путь проходит через создание и инициализацию native device, загрузку `.tpu`, синхронный запуск и проверку статуса. Присутствуют `Device.info()` и `Program.info()`, но Python-код не определяет содержимое device JSON. Совместимость этого пакета с TPU Runtime 16.18.6 и Framework 2026.8.43 из современной презентации не установлена.

Для защиты решения нужен связанный набор: идентификация выданного оборудования/сервиса и версии → hash скомпилированного артефакта → явный binding конкретного устройства → одинаковый input hash в клиентском и серверном протоколе → успешная native completion и output hash → независимое свидетельство работы нужного устройства в тот же интервал → контролируемая ошибка при недоступности разрешённого нам устройства. Сила доказательства определяется всей связью, а не отдельным скриншотом `/dev/tpu0` или API-ответом.

## Реестр источников

Все даты доступа ниже — 2026-10-23 Europe/Moscow. Неизвестную дату публикации не заменяли датой обхода поисковиком.

| ID | Источник, автор, дата | URL и локатор | Фактическая доступность и ограничения |
|---|---|---|---|
| W1-15-S01 | LinQ HPS datasheet, LinQ/«ХайТэк», дата версии в извлечённом документе не установлена | https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; PDF p1, p3, p4 | Самостоятельно открыт и прочитан web, 4 страницы текстового извлечения. Это продуктовая документация/заявления; руководства profiler и API в ней нет. Визуальная проверка не проводилась. |
| W1-15-S02 | «Фреймворк … IVA H1», руководство пользователя, 2025, RU.РМДВ.04.06.014-03 34 01 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf ; §§3.3–4, PDF p20–24 | Прочитан сохранённый W1-03 текст `_WORK/W1_03/Framework_manual_H1_extracted.txt`. Собственный web open docs/PDF вернул internal inaccessible; это не доказательство закрытости документа. |
| W1-15-S03 | PyPI `pytpu 15.0.24`, карточка автора IVA-Tech / owner IvaTechnologies, upload 2023-11-27T09:41:37.939987Z | https://pypi.org/pypi/pytpu/15.0.24/json ; поля info, urls | Самостоятельно прочитан полный JSON через web и CLI. README внутри metadata описывает старые сущности `iva_tpu`; не считать его актуальным reference для найденного кода. |
| W1-15-S04 | Source distribution `pytpu-15.0.24.tar.gz`, IVA-Tech, 2023 | https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz ; `pytpu/_bindings.py`, строки 28–159, 180–253, 270–425 | Собственная сетевая загрузка успешна, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`; архив сохранён `_WORK/W1_15/PYTPU_15_0_24.tar.gz`. Код прочитан в уже распакованном `_WORK/W1_09/PYTPU_SOURCE`. Содержимого native `libtpu` здесь нет. |
| W1-15-S05 | `linq-cv-bench`, GitHub-автор sherstpasha, commit 3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140, 2026-04-03 | https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py ; строки 102–105, 172–215, 248–257, summary в конце | Самостоятельно прочитан raw URL через web, локально проверен AST клона W1-06. Сторонний авторский пример, связь автора с производителем не установлена; собственный run не выполнен. |
| W1-15-S06 | MLPerf inference results v0.7, submission IVATech, 2020; repo mlcommons, pinned tree 89260c7a0bb2bb86f4adaf1d88e0307162eb602b | https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech ; `systems/iva-fpga-1.json`, `results/iva-fpga-1/resnet/SingleStream/performance/run_1/mlperf_log_summary.txt` | Самостоятельно скачаны raw JSON/log через CLI. Сохранены `_WORK/W1_15/MLPERF_SYSTEM.txt`, `MLPERF_LOG.txt`. GitHub web tree был restricted; raw и GitHub API tree работают. Это историческое опубликованное измерение чужого устройства, не наш тест. |
| W1-15-S07 | Код IVATech submission, авторский header mmoroz, 2020-07-09 | https://github.com/mlcommons/inference_results_v0.7/blob/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech/code/resnet/v1/IvaTPUSystemUnderTest.cpp ; `submitBatch`, `IssueQuery`, `inferenceWorkerThread`, `completeInferences` | Самостоятельно скачан raw после уточнения регистра имени по GitHub API. Сохранён `MLPERF_SUT.txt`, `MLPERF_MAIN.txt`. Описывает старый C API; не reference SDK2026. |
| W1-15-S08 | «Адаптированные нейросетевые алгоритмы на отечественных процессорах», рассказ Сергея Нефёдова о работе с Русланом Качмазовым и Львом Бабинцевым, VK/ВШЭ; размещено аккаунтом fivanov 2025-03-30 06:23 | https://habr.com/ru/companies/vk/articles/895432/ ; раздел IVA TPU и абзац об отсутствии встроенного подсчёта операций | Самостоятельно прочитана полная страница web. Первичный авторский рассказ об экспериментах, не официальный SDK guide; версии TPU/runtime и исходный протокол не раскрыты. Числа производительности здесь не использованы. |
| W1-15-S09 | IVA CV, руководство администратора, дата размещения URL 2026/05; дата версии самим исследователем не подтверждена | https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf ; p9 по handoff | Собственный web open inaccessible. Не выдаём за самостоятельно прочитанный документ; контейнерное свидетельство передано родителем, подробная интеграция у W1-14. |
| W1-15-S10 | LinQ 2026 presentation, производитель, 2026 по имени/документу соседней ветки | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf ; p4 по W1-03 | Используется только как handoff о версиях benchmark, самостоятельно повторно не загружалось этой веткой. Нужен для постановки вопроса о поколениях, не для вывода о версиях нашего будущего сервера. |

## Подробные факты и степень проверки

Тип основания ниже отделён от статуса. «Прочитан код» означает анализ исходника; не означает, что соответствующий native вызов или модель запускались.

### A. Что известно об инструментах наблюдения

**W1-15-F01 — официальные имена найдены.** Тип `vendor_statement`, S01 p1/p3; статус: самостоятельно прочитан документ. HPS datasheet называет Performance Profiler, DNN Stat; profiler описан как мониторинг скорости и загрузки вычислительных блоков. Также заявлены Power Monitor, температурный контроль, watchdog и управление частотой. Руководства запуска, формат отчёта, доступные counters, единицы времени, kernel-level trace и привязка к request ID не опубликованы в этом документе. Нельзя из этой записи получить интерфейс SDK либо считать все эти функции выданными команде.

**W1-15-F02 — framework debug logs не тождественны runtime telemetry.** Тип `primary_documentation`, S02 §4 p23–24; статус: прочитан сохранённый текст, не запуск. Документ описывает служебный вывод конвертера, квантователя и компилятора; стандартный Python `logging` может полностью его убрать. Следовательно, отсутствие debug output не диагностирует отсутствие TPU, а наличие compiler logs не доказывает execution. В образце печатаются результаты original/quantized/TLM/TPU и оценка `TLM estimates execution time: 5627.364001024086 us`. Это оценка TLM, не измеренная аппаратная задержка. Число не использовать как benchmark нашего решения.

**W1-15-F03 — старый README содержит конкретные statistics, но расходится с implementation.** Тип `primary_documentation` для README, `source_code` для сравнения; S03/S04; статус: самостоятельно прочитаны JSON и source. README описывает `TPUDevice`, `TPUInference`, `result.timings`, `queue_timings` для трёх очередей transfer-to/executor/transfer-from, `execution_timing` и `device.stats["mem"]`. В actual классе `Device` 15.0.24 нет метода/свойства `stats`, а `Inference.sync` возвращает словарь NumPy outputs, не описанный README status-result. Поэтому копирование этих snippets в API `Device.open()` необоснованно. Это историческая зацепка для запроса актуального API, не подтверждённая метрика 2026. Семантика и единицы timing надо запросить вместе с reference, не угадывать по имени.

### B. Что фактически делает pytpu15.0.24

**W1-15-F04 — импорт не handshake.** Тип `source_code`, S04 `_bindings.py:28–51`; статус: код прочитан, native библиотека не загружалась нами. `_LIB_TPU_SO_PATH='/usr/lib/libtpu.2.so'`, `_LibTPUBinder` связывается лениво при доступе к property `libtpu`. Успешный `import pytpu` не проверяет наличие `.so`, драйвера, hardware и исправность устройства. `pip show` столь же слабое свидетельство.

**W1-15-F05 — `list_devices()` не device enumeration protocol.** Тип `source_code`, S04 строки 201–204; статус: прочитан код и выполнена изолированная локальная проверка return expression с mock `/dev`. Реализация выбирает entries по `re.match(r'tpu.', f) and len(f)==4`, возвращая `/dev/...`. Не выполняет native вызов, `stat`, проверку char device, permissions, PCI identity или ioctl. Дополнительно она пропускает `tpux`/`tpu.` и исключает `tpu10`. Это поведение данной старой Python-функции, а не утверждение об именовании или числе устройств LinQ2026.

Изолированная проверка `STATIC_SOURCE_CHECK.py` / `.json`: для mock entries `tpu0,tpu9,tpu10,tpux,tpu.,tpu,nvidia0` возвращены `/dev/tpu0,/dev/tpu9,/dev/tpux,/dev/tpu.`. Тип `local_observation`, реальная локальная операция без импорта пакета и без аппаратного вызова. Первый запуск скрипта завершился FileNotFoundError из-за неверного собственного relative root; путь исправлен, повторный запуск успешен. Это не ошибка SDK.

**W1-15-F06 — native binding начинается при открытии и сильнее списка путей.** Тип `source_code`, S04 строки 185–229; статус: прочитан код. `Device.open(dev_name)` передаёт строку в `tpu_create_device`, затем constructor вызывает `tpu_init_device` и `tpu_is_device_valid`. При неуспехе — `ValueError` с `Invalid init code ...` либо `Invalid device: ...` и native message. Это позволяет связать session с явно выбранным путем. Однако Python-код не раскрывает, как native библиотека проверяет реальное устройство.

**W1-15-F07 — информация устройства и программы доступна через native JSON.** Тип `source_code`, S04 строки 228–229, 273–295; статус: прочитан код. `Device.info()` вызывает `tpu_get_device_info` и JSON decode. `Program.info()` — `tpu_get_program_info`; constructor использует metadata keys `inputs['1']`, `outputs['2']`, `hardware_parameters`. Схема `Device.info()` здесь не задана; нет основания обещать serial, PCI address, firmware, driver version, execution counter, температурный датчик или даже их имена. Нужно сохранить фактически возвращённый JSON и разобрать его по актуальному reference.

**W1-15-F08 — загрузка и inference имеют явные проверки ошибок.** Тип `source_code`, S04 строки 235–253, 373–425; статус: прочитан код, не вызвано. `load(path)` создаёт native program, проверяет valid program, вызывает `tpu_load_program`, проверяет device error string. `_run` передаёт указатели device/inference и mode в `tpu_run_inference`; ненулевой return code вызывает `InferenceError`. После копирования outputs `sync` вызывает `_check_status()` → `tpu_get_inference_status`; ненулевой status тоже ошибка. Наличие успешного sync в логе сильнее печати произвольной метки `TPU`, но закрытый native runtime остаётся доверенной частью цепочки.

**W1-15-F09 — внешний sync timer не чистый compute counter.** Тип `source_code` + `inference`, S04 `Inference.sync`/`_load_inference`/`_get_inference`; статус: source analysis. Внутри sync резервируются buffers, загружаются данные, выполняется `_run`, формируются/копируются NumPy outputs и проверяется status. Стандартный mode `ProcessingMode.FULL=3`; определены также RAW=0, PRE_PROCESS=1, POST_PROCESS=2. Эти enum не доказывают перенос всех преобразований на CPU или TPU. Время вокруг sync включает Python/runtime и обработку buffers; нельзя подписывать его «время TPU ядра» без separate timing reference.

**W1-15-F10 — в просмотренном Python binding нет пути автоматического CPU-model fallback.** Тип `source_code`, S04; статус: просмотрен файл. Здесь нет вызова TensorFlow/ONNX Runtime/PyTorch для исполнения исходного neural graph в ветке ошибки устройства. Важное ограничение: это не доказывает отсутствие fallback в native `.so`, сервисной оболочке, обновлённом SDK или коде нашего приложения. Не найденный CPU-path не равен установленной невозможности mixed execution.

### C. Авторский CV пример и историческое измерение

**W1-15-F11 — сторонний YOLO runner не является готовым доказательством запуска.** Тип `source_code`, S05 pinned строки 191–203; статус: самостоятельно прочитан remote source и AST локального клона. Parser создаёт `output_tensor_name`, а `main` до `list_devices()` обращается к `args.output_tensอร์_name`. При обычном argparse Namespace атрибута нет: ожидается AttributeError, если выполнение уже прошло предыдущие проверки файлов/импортов/COCO. Полный runner нами не запускался. AST нашёл именно не-ASCII attribute; дефект стороннего примера не переносится на SDK.

**W1-15-F12 — граница host/TPU в этом примере видима.** Тип `source_code`, S05; статус: remote source прочитан. Device можно явно задать через `--device`, иначе берётся первый путь. Runner открывает device и `.tpu`, выполняет `run` при наличии, иначе `sync`. Замер perf_counter обрамляет runtime call; NMS вызывается после него через NumPy→torch и Ultralytics на host. Это отдельная постобработка, не установленный CPU fallback графа. Summary в JSON, созданный самим runner, остаётся application report, а не аппаратным attestation. Даже после исправления typo нужен реальный execution protocol.

**W1-15-F13 — исторический MLPerf связывает machine description, harness и logs, но относится к FPGA.** Тип `reported_measurement` + `source_code`, S06/S07; статус: самостоятельно скачаны и прочитаны raw files, benchmark не запускался нами. System JSON: `iva-fpga-1`, accelerator `IVA_FPGA_1`, 250MHz, Alveo U200, Ubuntu18.04, Tensorflow1.15.0; stack `iva_tpu4.1.4`, `libtpu7.1.15`, `tpu_quantize3.2.1`, `tpu-compiler13.1.0`. SingleStream summary сообщает VALID, p90 12,230,138ns, min duration60,000ms, query samples1. Это полезный образец воспроизводимого пакета доказательств, не производительность LinQ H2026.

**W1-15-F14 — submit/completion counts в historical harness не аппаратные utilization counters.** Тип `source_code`, S07; статус: скачан и прочитан source. `tpu_inference_submit`, `tpu_inference_wait`, получение output tensors и `QuerySamplesComplete` образуют проверяемую цепочку completion. `inferenceSubmitedCount_` и `inferenceCompletedCount_` — переменные harness, debug queue messages печатает spdlog. Они не доказывают наличие equivalent counters в современных firmware. MLPerf summary `VALID` сообщает о критериях данного benchmark; сам по себе не удостоверяет request/device identity нашего сервиса.

**W1-15-F15 — авторы VK/ВШЭ не имели встроенного счётчика операций/с в доступной им среде.** Тип `reported_measurement` для описанного опыта, S08; статус: самостоятельно прочитана статья, измерения не воспроизводились. Авторы считали операции модели и FPS вручную. Описаны remote GUI, preload performance, последовательная подача для latency, batch1/2/4/8 и STAGING. Версии и identity не даны. Это не опровержение profiler в HPS datasheet: отличаются время, окружение и смысл метрики. Derived ops/s не становятся аппаратным counter, а preload-результат — задержкой нашего видеосервиса.

**W1-15-F16 — контейнерный device mapping только предоставляет доступ.** Тип `inference` из handoff S09, не самостоятельное чтение. Указанные родителем p9 литералы `--device /dev/tpu0:/dev/tpu0` и image `ivacv.tech:15444/common/walkers-node:0.1.310` объясняют binding контейнера к host device node. Даже подтверждённый docker inspect/compose с таким mapping доказывал бы возможность доступа, а не обращение inference к этому устройству. Full integration и независимая проверка документа у W1-14.

## Практический протокол после выдачи доступа

Следующие пункты — предлагаемые эксперименты (`inference`/`hypothesis`), **не уже выполненные проверки и не документированные команды LinQ2026**. Необходимо адаптировать к реальному reference и разрешённым правам; никакой перезагрузки сервера или отказа устройства других участников.

### 1. Согласовать предмет доказательства

В первые минуты запросить: что именно требуется выполнять на LinQ — весь neural graph, detector backbone/head, несколько моделей? Допустимы ли host decoding/NMS/tracking? Как жюри принимает evidence: server runtime log, profiler export, live run, подпись инженера? Где заканчивается обязательный inference и начинается вспомогательная логика? Согласовать один технический критерий до оптимизации.

### 2. Получить manifest фактического окружения

Сохранить timestamp/timezone, hostname или server instance ID, user/session ID без секретов, точный образ и digest, версии SDK/runtime/driver/firmware доступными официальными методами. Не подставлять version из презентации. Для SSH/контейнера — согласованную инженером связь device path с physical identifier: PCI BDF/serial/chip ID, если существует. Для service-only доступа — backend instance ID и официальный способ получить execution trace. `Device.info()` запускать только после сверки с выданной API версией; сохранить JSON без предположений о ключах.

`ls /dev/tpu*`, `lspci`, device permissions и container mapping пригодны как инвентаризация. Даже корректные IDs не доказывают, что выбранная модель использовала этот PCI device. Generic `/proc/<pid>/fd` или system-call trace, если разрешены и нужны, могут дополнительно связать runtime process с device node, но не раскрывают инструкций нейросети и не заменяют vendor telemetry.

### 3. Связать модель, вход и вызов

Сохранить исходные weights/export hashes и compile settings/report, затем SHA256 точного `.tpu` или фактически выдаваемого runtime artifact. Сохранить input tensor hash, dtype, shape, layout, preprocessing version, input/frame ID. Назначить run ID, записать явно выбранный device ID. Не выбирать silently `devices[0]` при нескольких ускорителях без recording actual selection.

Из wrapper log должны быть видны load begin/end, native/API exception и return status, submitted/completed counts, output hash. Не заменять exception CPU inference; если приложение имеет отдельный baseline, его backend/результат помечать отдельно. Raw outputs хранить хотя бы для контрольных inputs, чтобы связать преобразования и выводимый детекторный результат.

### 4. Получить независимое временное свидетельство работы устройства

Запросить у инженера актуальные Performance Profiler/DNN Stat и пример запуска именно нашего runtime. Желательные поля: physical device ID, время, model/artifact ID, execution count или task ID, busy/idle, transfer-to/executor/transfer-from timings, memory occupancy, errors. Не все они доказанно существуют. Снимать baseline и run в одном временном интервале; разницу correlated utilization считать поддерживающим свидетельством, особенно при shared accelerator, а не доказательством конкретного запроса. Power/temperature alone ещё слабее: их меняет чужая нагрузка и DVFS.

На общем устройстве нужен per-process/per-task trace либо выделенный слот. Aggregate counter с чужими заданиями не связывает нашу модель с execution. Device timer также надо проверить: units, clock, queue wait inclusion, reset semantics, counter rollover, accumulated vs per-inference, global vs session.

### 5. Выполнить безопасный отрицательный контроль

В отдельном своём процессе/контейнере, не трогая shared host driver, повторить тот же запрос с заведомо отсутствующим device path либо без разрешённого ему device mapping — если это допустимо режимом доступа. Ожидается явная ошибка на открытии/load/inference и отсутствие успешного модельного ответа. Неудачный open подтверждает fail-closed на этой точке; он не исключает fallback, который включается лишь для отдельной unsupported операции или после run failure.

Чтобы исключать **частичный** fallback, нужен compiler partition/report и runtime trace с привязкой операций либо официальная гарантия no-fallback для данного API/артефакта. Если reference допускает strict mode, применить документированную опцию и сохранить её значение; сейчас такой опции не найдено. Не выдумывать `--no-cpu-fallback`. Можно попросить инженера воспроизвести unsupported-operation case и показать диагностическое поведение, но не переносить ошибки стороннего runtime.

Для service-only режима invalid-device клиентский тест может ничего не значить: сервер выбирает backend сам. Требовать server-side correlation по request ID и model hash, backend/device ID, runtime version и исполнению. Поле `backend: LinQ`, latency или HTTP200 — утверждение сервиса; без trusted server evidence оно не подтверждает hardware. При отсутствии telemetry честно оформить ограничение и получить приемлемый для жюри способ верификации.

### 6. Разделить correctness и performance

Три времени: preprocessing/NMS/tracking на host; runtime call including transfers/buffers; end-to-end от camera/frame timestamp до события. Если есть аппаратный timer — четвёртая отдельная метрика с документированной границей. Warmup, batch, число measured frames, concurrency, queue depth, padding batch, shared load и версии сохранять. Correctness сравнивать по raw outputs/детекциям с допусками квантования на одинаковом input, а не только top1. Совпадение outputs нужно для качества; оно не устанавливает физическое устройство.

Минимальный reviewable пакет: `ENVIRONMENT`, `MODEL_MANIFEST`, `COMPILE_REPORT`, `RUN_LOG`, `INPUT_OUTPUT_MANIFEST`, `PROFILER_EXPORT` (если доступен), `NEGATIVE_CONTROL`, краткая инструкция повтора. Это предложения по именам будущих артефактов, не созданный здесь прототип.

## Противоречия и ограничения

- PyPI README старого `iva_tpu` и actual `pytpu Device` API существенно различаются. Источник опубликован как один package; приоритет для наблюдения поведения отдан implementation, а возможности старого README не перенесены на новый класс.
- «Нет встроенного подсчёта operations/s» в статье2025 и «Performance Profiler/DNN Stat» в HPS datasheet не обязаны противоречить: profiler загрузки/скорости не обязательно аппаратный счётчик арифметических операций; разные products/версии не идентифицированы.
- Framework guide2025 описывает debug logging, TLM и native TPU execution path, но не политику fallback; из документа нельзя вывести полноту graph execution на TPU по каждой операции.
- Из modern presentation handoff известны Runtime16.18.6 и Framework2026.8.43 только для benchmark-контекста. Публичный PyPI15.0.24 не доказан совместимым и не рекомендуется к установке вместо выдаваемого SDK.
- device node/container mapping, successful native init, API completion и hardware counters — разные уровни свидетельств. Самый сильный доступный уровень заранее неизвестен.
- Отсутствие найденного API/log/counter в открытом поиске не доказывает его отсутствия у производителя или в выдаваемой среде.

## Где и как искали; ошибки доступа

Собственный web поиск: `site:lin-q.ru TPU profiler runtime лог профилирование`, `site:files.lin-q.ru TPU runtime profiler counters`, точные `"LinQ" "DNN Stat"`, `"LinQ" "Performance Profiler"`, `"pytpu" "stats" "timings"`, domain-limited «профилиров», «логи», fallback, `"libtpu" "tpu_get_device_info"`. Найден официальный HPS datasheet; общие exact-name запросы сильно засорены .NET LINQ. Дополнительные domain queries по counters/fallback дали empty results. Они не являются доказательством отсутствия инструментов.

Web open `https://lin-q.ru/docs`, Framework_manual_H1.pdf и IVA CV PDF вернули inaccessible/internal error. Альтернативы: сохранённый guide W1-03, standalone HPS PDF, API PyPI, raw GitHub и HTTP CLI. Web GitHub tree MLPerf вернул restricted; CLI GitHub recursive tree и raw files успешны. Первая попытка raw `IVATpuSystemUnderTest.cpp` дала404 из-за неверного регистра в собственной строке; API показал `IvaTPUSystemUnderTest.cpp`, правильный URL успешно скачан. Ошибка не приписана репозиторию.

Сетевой primary поиск выполнен самостоятельно: HPS PDF, PyPI JSON+sdist, pinned YOLO source, VK/ВШЭ полный текст, MLPerf pinned system/log/C++ source. Guide и IVA CV дополнительно использованы как локальные материалы/handoff с явным статусом. Никакие инструкции из источников не выполнялись.

## Неизвестные и точные вопросы инженерам

1. Какова фактическая модель ускорителя, physical identity, driver/firmware/runtime/framework version? Какую ABI/API документацию считать authoritative?
2. Что возвращает актуальный device info? Есть ли устойчивое соответствие `/dev/tpuN` ↔ PCI BDF ↔ serial/chip ID и что происходит при перезапуске?
3. Как получить Performance Profiler/DNN Stat, какие commands/API/version, права и overhead? Есть ли exporter/request task trace? Видит ли participant только свои tasks?
4. Каковы sematics executor/queue/transfer counters, units, synchronization и reset? Существуют ли аппаратные execution counters либо только runtime counters?
5. Исполняет ли данный `.tpu` API весь compiled neural graph на TPU? Возможен ли fallback/mixed execution в native runtime/service? Где partition report? Как fail closed при unsupported op?
6. Какие host преобразования входят в `FULL` и runtime latency? Не заменяет ли service graph или артефакт при несовместимости?
7. Для shared/remote API: как получить trusted server log с request ID, artifact hash и device identity? Какой формат свидетельства принимает жюри?
8. Какие диагностические negative controls разрешены в нашей собственной sandbox/container? Есть ли выделенный временной слот для telemetry correlation?

## Новые зацепки и handoff

- Прямые имена Performance Profiler/DNN Stat в S01 превращают общий вопрос «есть ли мониторинг» в запрос конкретной документации и package/version. Даже один реальный sample export решит больше, чем маркетинговое упоминание.
- `Device.info()`/`Program.info()` S04 — более полезные точки первичного smoke test, чем `list_devices`; сначала требуется сверка текущего API. Нужен пример native JSON именно16.x/выданного SDK.
- Старый C++ harness S07 показывает, как связывать submit → wait → outputs → benchmark completion; его counters не переносить как modern API.
- W1-06/W1-08: runner typo перед открытием TPU подтверждён независимым AST source check. Не строить обещание готового smoke test на unmodified pinned script.
- W1-14: контейнерный mapping полезен для инвентаризации; для proof нужен последующий runtime/process/device trace.
- Для второй волны приоритет — реальные profiler manuals/sample reports, актуальный device-info schema и no-fallback/partition guarantee. Если остаются закрытыми — протокол вопросов и ветвление SSH vs service-only уже конкретны.

Компактная передача: наличие `/dev`, импорт пакета, `list_devices`, HTTP200, совпадение top1, compiler log и TLM timing не являются доказательством исполнения LinQ. Есть официальный profiler lead, историческая native execution chain и открытый образец evidence bundle MLPerf. Подтверждение современного выполнения требует выданной среды, связанного runtime/device trace и согласованного критерия жюри. Собственного аппаратного теста в этой ветке нет.
