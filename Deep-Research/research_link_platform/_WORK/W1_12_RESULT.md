# W1-12 — диагностика, версии, совместимость и восстановление

Дата фактической проверки: 2026-10-23, 04:30–04:35 Europe/Moscow (UTC+3). Контекст подготовки: хакатон 23–25 октября 2026. Работа — исследование; LinQ, runtime, driver и compiler не установлены и не запускались. Прочитаны индивидуальный prompt и требования разделов 7, 9, 11 общего prompt.

## Главный вопрос и вывод

Как быстро отделить дефект окружения/примера от ошибки компилятора или устройства и восстановить работу, не подменяя неизвестный SDK2026 историческим ABI?

Подтверждены три разных слоя: (1) официальный guide 2025 с диагностикой установки, STAGING→DEFAULT и примером TensorFlow warning; (2) публичный исходник `pytpu==15.0.24` 2023 с реальными Python-ветвями обработки ошибок libtpu; (3) сторонний `linq-cv-bench` commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` с собственными исключениями и воспроизводимым дефектом имени аргумента. Совместимость этих слоёв с TPU Runtime16.18.6 / Framework2026.8.43 не установлена. Эти две современные версии прочитаны в benchmark-сноске производителя; они не являются выданным команде SDK.

Практический результат — последовательная локализация: окружение → framework import → наличие node/driver → runtime load/init → штатная vendor .tpu → свой compiled artifact → input contract → inference → postprocess. После ошибки не запускать бесконечный перебор имён входа: сторонний resolver подавляет любые exceptions, включая настоящие runtime failures.

## Факты и статус проверки

Тип утверждения ниже отделён от фактической проверки. `source_code` означает прочитанный код, а не воспроизведённую работу на TPU.

| ID | Установленное содержание и область применения | Тип | Проверка | Источник |
|---|---|---|---|---|
| W1-12-F01 | Guide2025 §2 требует Ubuntu20.04, RAM≥32GB, Python3.11; локальный wheel `tpu_framework-py3-none-any.whl`; проверка установки через `import tpu_framework` и exit0. Это проверка Python framework, не обнаружение устройства. | primary_documentation | Прочитан сохранённый полный extraction и заново получен официальный PDF через TinyFish; установка не выполнена | S01 |
| F02 | Guide2025 §3.2 различает DEFAULT/STAGING. STAGING может давать недопустимые программы или чрезмерно долгую компиляцию; документ предлагает вернуться к DEFAULT и отправить bug report. Упоминание DISABLED в следующем абзаце не задаёт здесь отдельную проверенную современную CLI-команду. | primary_documentation | Текст прочитан; compiler не запускался | S01, printed p10 |
| F03 | Guide2025 §4 помещает TensorFlow deprecation warning в пример штатного logging; наличие/отсутствие отладочного вывода допускается. Warning касается `Zeros.__init__` и аргумента `dtype`, не является сообщением о неподдерживаемой TPU operation. | primary_documentation | Прочитан полный контекст, включая продолжение p24 | S01, printed p23–24 |
| F04 | Презентация2026 слайд4: Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, i7-10700K в условиях заявленного измерения. | reported_measurement (только среда) | Заново прочитано через TinyFish, собственного benchmark нет | S02 |
| F05 | PyPI version15.0.24 опубликована 2023-11-27T09:41:37.939987Z, author IVA-Tech, Python≥3.6; sdist SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. README показывает `iva_tpu.TPUDevice`, фактический package экспортирует `Device`, `Program`, `Inference`, `InferenceError`. | primary_documentation / source_code | Открыт PyPI JSON, прочитаны локальные setup/init/bindings; sdist заново не устанавливался | S03/S04 |
| F06 | pytpu15.0.24 lazy-load `/usr/lib/libtpu.2.so` через ctypes.CDLL при первом обращении к binder; простой import не проверяет наличие .so, её symbols, driver или hardware. `Device.list_devices()` только фильтрует имена файлов `/dev`, а не открывает/проверяет TPU. | source_code | Прочитан `_bindings.py:28–51,185–206`; hardware нет | S04 |
| F07 | В старом binding есть отдельные init, valid-device, program, load, run-inference и inference-status error paths. Runtime message извлекается отдельными C API; таблицы значений status/init codes в sdist не найдено. | source_code / unknown | Прочитаны ветви, ни одна не вызвана на runtime | S04 |
| F08 | `test_HW_params_mismatch` использует `device.info()['axi_word_len']` и намеренно другой DDR/cache target, ожидая ValueError. Это подтверждает, что авторы тестируют аппаратную совместимость .tpu, но не задаёт совместимость compiler/runtime release. | source_code | Только inspection теста; test data/runtime нет | S05 |
| F09 | Старые generator context managers open/load/inference/buffer освобождают handles после yield без try/finally. При exception в теле with код после yield не гарантирован. Есть TODO о нестабильности destroy tensor buffer с ссылкой TPU2-2010. | source_code + inference о Python control flow | Source inspection; утечка на устройстве не измерялась | S04,185–253,306–322 |
| F10 | `test_watchdog_error.py` помечен skip; причина говорит о mem collision и нарушении работы device/других tests. В тесте есть старые закомментированные API и TODO. | source_code | Прочитан; опасный тест не запускался | S05 |
| F11 | Pinned third-party YOLOv8 runner объявляет `--output-tensor-name`, затем обращается к `args.output_tensอร์_name` до list_devices/open. Это дефект примера. | source_code + local_observation | AST и отдельный Namespace lookup воспроизвели AttributeError, полный runner не запускался | S06; auxiliary CHECK_EXAMPLE_ATTRIBUTE.py |
| F12 | Страница issues стороннего repo при проверке показала Open0 и отсутствие результатов текущего фильтра. Releases — без релизов. Это не официальный SDK tracker и не доказательство отсутствия closed issues/внутренних исправлений. | local_observation | Сетевые страницы открыты | S07/S08 |

## Точные диагностические сообщения и их владельцы

Следующие шаблоны взяты из локально прочитанного sdist15.0.24 (S04); переменные внутри фигурных скобок — фактические значения/сообщение C runtime, которого у нас нет. Не выдавать их за фактически полученный лог.

| Где | Python исключение / шаблон | Что действительно известно | Первое действие |
|---|---|---|---|
| Device.__init__, line218 | ValueError: `Invalid init code {init_code}: {message}` | C init вернул ненулевой код; расшифровка кода отсутствует | Сохранить полный message, версии .so/driver и node; vendor support |
| Device.__init__,221 | ValueError: `Invalid device: {message}` | После init проверка valid-device не прошла | Проверить node/access и штатный vendor sample; не считать автоматически PCIe failure |
| Program.__init__,285 | ValueError: `Invalid program: {message}` | C program validation не прошла | Проверить путь, hash, target/compiled metadata и версию toolchain |
| Device.load,250 | ValueError с device error message | Ошибка после load_program; Python не предоставляет отдельного классификатора | Сохранить точный C message, не заменять общим «нет TPU» |
| Inference._run,382 | InferenceError: `Invalid tpu_run_inference return code {status_code}: {message}` | Ненулевой результат C вызова запуска | Проверить штатную программу и input contract, прекратить resolver retries |
| Inference._check_status,422 | InferenceError: `Invalid inference status code {status_code}: {message}` | После sync status ненулевой | Отличать от ошибки initial run; собирать оба кода |
| Inference._load_inference,431 | ValueError: `Input data must be a mapping, got:{type}` | Host API получил не Mapping | Исправить input container до обращения за driver recovery |

Чистый Python layer также проверяет строковые типы dev/program path; lookup неизвестного tensor_name может дать KeyError, output reshape — обычную ошибку NumPy. Это не автоматически failure аппаратуры. В этом исходнике нет полноценной проверки shape/dtype входа перед передачей указателя: `_load_inference` берёт `tensor_data.ctypes.data_as(...)`; комментарий TODO прямо оставляет validation. Поэтому отсутствие раннего ValueError не доказывает правильность входа. Проверять shape, dtype, byte count и contiguous layout на стороне приложения необходимо до запуска; требования точного нового API получить у инженера.

Наличие `/dev/tpu0` и успешный `import pytpu` по отдельности не доказывают execution. В старом source list_devices фильтр `tpu.`/длина4 даже не является общим надёжным перечислением произвольного количества устройств.

### Сторонний runner: не путать с SDK

S06 имеет собственные ошибки для отсутствующего program file, dependencies, устройства, разрешения tensor names, формы prediction и чтения изображения. Они созданы Python-примером. Общий wrapper dependencies способен скрыть первопричину import error — нужен chained traceback. Resolver перебирает имена, ловит все Exception и оставляет лишь часть sample errors: ошибка устройства может выглядеть как неправильное имя тензора.

Локальная мини-проверка воспроизвела только lookup несуществующего Namespace attribute; она не доказывает runnable весь repo. Условия достижения дефекта: файл .tpu существует, imports и чтение COCO уже прошли. Если любое из них ломается раньше, пользователь увидит более раннюю ошибку. Рекомендуемый учебный patch — исправить имя на `output_tensor_name`, сохранить отдельный diff/commit; в этой research-ветке исходник repo не редактировался.

### TensorFlow warning и build warning

Guide2025 показывает deprecation `dtype` в TensorFlow initializer. Это warning host-компонента квантования, а не documented LinQ inference error. Проверять результат этапа и exit code; не скрывать все warnings глобально. Python3.8 в пути логов не доказывает, что требование Python3.11 ошибочно: возможен исторический пример. Точная dependency matrix остаётся вопросом.

В setup.py старого sdist условие VERSION==15.0.24 порождает предупреждение Invalid package version при сборке. Литерал совпадает с опубликованной версией: это артефакт build script/source, не признак повреждённого runtime или доказательство ложной версии PyPI. Ничего не переименовывать самостоятельно ради подавления warning.

## Совместимость: что нельзя смешивать

1. Guide2025 обозначает программу `RU.РМДВ.04.06.014-03` как развитие `-02`, но это обозначение документа/программы не release matrix ABI.
2. PyPI15.0.24 (2023), guide2025 и benchmark2026 — разные временные точки. Число16.18.6 в runtime не сообщает автоматически совместимый pytpu release. Имя `/usr/lib/libtpu.2.so` не удостоверяет, что установленная бинарная библиотека совпадает с ABI binding2023.
3. `/sol` рекламирует Python3.8, guide требует3.11, пример log содержит3.8. Здесь нет доказанного единого поддерживаемого Python для выданного доступа. Использовать установленный vendor environment и зафиксировать его, а не переустанавливать наугад.
4. .tpu target/hardware параметры и release compatibility — разные проверки. Исторический тест wrong DDR/cache не разрешает переносить .tpu между hardware или runtime releases.
5. STAGING/DEFAULT из guide2025 и O1/O5 стороннего repo не имеют установленного взаимно однозначного соответствия. Не назначать O1 «тем же DEFAULT» без release docs.

## Конкретный маршрут при получении доступа

Это предлагаемые будущие проверки (inference/engineering recommendation), не выполненные команды на LinQ.

**0. Снять паспорт среды до изменений.** Записать способ доступа (SSH/container/API), hostname/OS/kernel/architecture, `python -V`, `python -m pip freeze`, пути `tpu_framework.__file__`/`pytpu.__file__`, версии пакетов через importlib.metadata. Для Debian/Ubuntu запросить `dpkg-query -W libtpu tpu-dkms` с сохранением ошибок отсутствующих пакетов. Не подставлять пакеты Google libtpu по совпадению имени. Получить номер compiler/framework/runtime/driver/firmware от vendor environment и hash эталонной .tpu. Пустая metadata version — не заменять предположением.

**1. Проверить host/framework.** Vendor wheel в отдельном предусмотренном окружении; import и exit code. Если import не проходит, сохранить полный traceback, executable, sys.path, package locations. Этот этап не требует собственного экспорта модели. Для remote API аналог — authentication/health/version endpoint только из предоставленной документации, без выдуманного URL.

**2. Проверить устройство.** Для Linux с прямым доступом: `ls -l /dev/tpu*`, группы/права процесса, `lspci -nn`, driver/DKMS status и разрешённые kernel logs. Различать «нет PCI device», «PCI есть, node нет», «node есть, access denied», «init failure». В контейнере отсутствие node может быть issue passthrough/permissions. Команды hardware guide и PCI IDs брать из документа конкретной предоставленной платы; в облачном API host PCI часто недоступен и не нужен клиенту.

**3. Не путать listing с open.** Для API, действительно совпадающего с binding2023: list → open → info; сохранить C message при init. Для современного SDK выбрать эквивалент по его документации. Не проверять современную библиотеку старым ctypes-binding наугад.

**4. Эталонная программа той же поставки.** Запустить vendor .tpu и vendor input на одном устройстве; записать outputs, статус, latency и явный device identity. Сначала один процесс, один inference, без parallel. Если эталон ломается, собственный ONNX/compiler ещё не является первой подозреваемой причиной.

**5. Своя компиляция.** Сохранить source model hash, ONNX/opset, preprocessing, calibration data digest, target hardware, preset, compiler/framework versions и полный build log. Проверить входы/выходы из artifact metadata, а не перебором generic names. При проблемах STAGING на соответствующем guide2025 пути повторить DEFAULT в новых output paths, сравнить compile time/validation; не перезаписывать исходный artifact.

**6. Inference и output.** Сначала один заранее сохранённый input tensor с shape/dtype/byte count; затем несколько повторов и сверка reference/quantized/simulator/device там, где эти этапы реально доступны. Наличие TLM estimate или CPU/CUDA baseline не подтверждает TPU execution. Видеодекодирование и postprocess добавить после воспроизводимого single-frame success.

**7. Восстановление.** Сохранить первый traceback и runtime status до retries. После обычной ошибки завершить worker и попробовать новый процесс с эталонным artifact — это инженерная гипотеза для проверки, не документированная гарантия hardware recovery. В историческом binding exception-safe cleanup сомнителен, поэтому reuse того же процесса может сохранять повреждённое состояние. Не вызывать close вторично на уже освобождённых handles; это тоже не проверенный способ ремонта. Если новый worker/эталон не восстанавливает работу, инженер LinQ должен определить доступную команду reset, service restart, driver reload либо reboot и последствия для других пользователей. Публичной подтверждённой команды безопасного reset/recovery в прочитанных источниках нет. Самостоятельный unload driver/PCI reset на общем сервере не предлагается.

## Что спросить у инженеров в первые минуты

- Каков точный комплект совместимых compiler/framework/pytpu/runtime/driver/firmware и Python/OS? Есть ли lockfile/container digest, release notes и matrix .tpu backward/forward compatibility?
- Как получить version/device info штатным API2026 и полный status/error string? Где таблица error codes, runtime/kernel log и их retention?
- Нужна ли recompilation .tpu при обновлении runtime/framework, смене платы/числа чипов, target/DDR/cache? Как проверить metadata до load?
- Какие ошибки допускают retry того же inference/program/device, какие требуют new process, reset или администратора? Каков timeout/cancel API, что происходит с очередью при disconnect?
- Какой безопасный reset доступен участнику на shared online server и затрагивает ли он соседей? Есть ли reserved single device для recovery smoke-test?
- Какие штатные эталонные .tpu/input/output и команды monitoring дадут доказательство LinQ execution?

## Поиск, доступ и неизвестные

Выполнены реальные web search: `site.lin-q.ru TPU Framework ошибки runtime версия`, точный pytpu15.0.24, repo/issues, `site:lin-q.ru "release" "runtime"`, `site:lin-q.ru "ошибки" фреймворк`, `"pytpu" "watchdog"`, `"libtpu.2.so"`. Поиск exact libtpu дал много Google/Coral/Sophgo: эти сведения исключены как чужая платформа. Открыты PyPI JSON, pinned raw runner, repo issues/releases; локально прочитаны исходники sdist и pinned clone. `git rev-parse HEAD` совпал с заданным commit; status был чистый.

web open официального /docs и guide PDF возвращал not accessible; GitHub tree — restricted URL; PyPI JSON/raw runner/issues/releases доступны. API GitHub issues?state=all через web — inaccessible; закрытые issues поэтому не обследованы полностью. Старый homepage `git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk` inaccessible. TinyFish стал рабочей альтернативой для /docs, guide и presentation2026. Два первых TinyFish вызова были отвергнуты schema validation (обязательные параметры; format text); успешный вызов с urls/markdown получил материалы. Содержимое официального /docs — hardware manuals плюс framework guide; отдельный release notes/API troubleshooting index там не найден. Это не доказывает, что закрытого справочника или другого публичного URL нет.

Unknown: текущий ABI, безопасный reset/restart, .tpu format/version compatibility, список code values, watchdog recovery, concurrency/retry/cancel semantics, поставляемые участникам SDK/driver и ограничения online-доступа. Публичный source2023 даёт новые вопросы о cleanup и input validation; не превращать его TODO в объявление дефекта Runtime2026.

## Источники

Все access time: 2026-10-23 04:30–04:35 MSK; точного server publication timestamp нет там, где это прямо не указано.

| ID | URL / название / автор / дата | Локатор и ограничения |
|---|---|---|
| W1-12-S01 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — «Фреймворк IVA H1. Руководство оператора», официальный files.lin-q.ru, 2025 | RU.РМДВ.04.06.014-03 34 01; §2, §3.2 printed10, §4 printed23–24. Прочитан extraction `_WORK/W1_03/Framework_manual_H1_extracted.txt`, затем primary network TinyFish. Оригинальные PDF bytes/визуальный screenshot этим агентом не проверялись; текстовые выводы не зависят от таблиц/графиков. |
| W1-12-S02 | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — «Российские решения для аппаратного ускорения работы нейронных сетей», ООО «ХайТэк», 2026; PDF metadata author Сергей Севрюков | Слайд4 сноска условий benchmark; TinyFish network primary reading. Не release notes, не runtime verification. |
| W1-12-S03 | https://pypi.org/pypi/pytpu/15.0.24/json — PyPI release metadata, author IVA-Tech, upload2023-11-27 | info/version/requires_python/home_page и urls/digest; сетевое чтение. README расходится с actual API. PyPI metadata сама по себе не доказывает современную LinQ attribution/ABI. |
| W1-12-S04 | https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz — IVA-Tech source, 2023 | Локальный `_WORK/W1_09/PYTPU_SOURCE/pytpu-15.0.24`: `_bindings.py`, `__init__.py`, `setup.py`; установленный точный sdist digest из S03. Только source inspection, libtpu отсутствует/не вызывался. |
| W1-12-S05 | Тот же sdist S04, `pytpu_tests/unit/test_inference_error.py`, `test_watchdog_error.py`, `test_tpu_exists.py` | Тесты — свидетельство ожиданий автора; не собственные выполненные измерения. Watchdog test skipped/неполон. Test data и бинарный runtime не проверены. |
| W1-12-S06 | https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py — sherstpasha, commit2026-04-03 | Pinned local source line206 (web renderer нумерует логические строки иначе); parse_args, main, resolve_runtime_input_name. Raw network прочитан. Сторонний repo, не официальный SDK; локально сделан только Namespace probe. |
| W1-12-S07 | https://github.com/sherstpasha/linq-cv-bench/issues — авторский GitHub tracker, дата публикации не задана | Проверен default open filter; closed issues не установлены. |
| W1-12-S08 | https://github.com/sherstpasha/linq-cv-bench/releases — GitHub releases | При проверке нет releases. Не tracker производителя. |
| W1-12-S09 | https://lin-q.ru/docs — «LinQ_Документация», ООО «ХайТэк», без даты | TinyFish прочитан список manuals и реальный link framework. Отдельная публичная таблица совместимости/release notes в этой навигации не найдена. |
| W1-12-S10 | http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk — homepage из PyPI | Web inaccessible; содержимое не прочитано и не приписывается. |

## Handoff

Оркестратору: включить в первые эксперименты паспорт поставки и vendor known-good artifact раньше собственного detector. Разнести в troubleshooting «framework import», «node present», «device opened», «inference success». Ошибка `output_tensอร์_name` — воспроизведённый host-example defect; TensorFlow `dtype` — documented warning; init/program/inference errors — source2023 templates; современная code/recovery matrix — unknown. При подозрении на STAGING guide2025 даёт конкретную альтернативу DEFAULT. Для версий2026 требуется ответ производителя, а не установка публичного старого PyPI. Новая зацепка для второй волны — получить release notes/cleanup semantics и исключить повторное использование worker после runtime exception до проверенного recovery.

