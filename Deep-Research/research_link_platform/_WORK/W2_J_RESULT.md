# W2-J — доказательство исполнения, profiler и граница полного графа

Связанные замечания: **K013, K009, K014**. Исследовательский контекст: ночь 23 октября 2026, пять опытных инженеров, 45 часов, обязательный LinQ inference. Actual source access этой ветки: 2026-10-23 примерно 02:03–02:09 UTC / 05:03–05:09 MSK; точные HTTP timestamps в `W2_J/HTTP_LOG.json`, финальная clock check02:09:25UTC. Прочитаны оригинальный prompt, индивидуальный W2 prompt полностью, K013/K009/K014 критика, W1-15, W2-G и RUN_STATE. Доступ команды к SDK, native runtime и физическому устройству не подтверждён. Здесь выполнены новые web searches, alternate retrieval и статический разбор двух дополнительно скачанных source distributions; ни SDK, ни compiler, ни native library, ни device job не запускались.

## Решение и изменение после W1

**Готовый современный profiler/manual/export с per-request device correlation не найден; цепочка доказательства должна иметь два независимых звена: происхождение/coverage модели и completion на выданном устройстве.** Название profiler и даже положительный device timer сами по себе не закрывают оба звена. Точное ограничение — нет matching modern report schema, units/clock semantics, artifact/request/device IDs и guarantee покрытия графа. Это неизвестное содержание поставки, а не доказательство отсутствия инструментов у LinQ.

Новый полезный результат: legacy README содержит не просто обещание statistics, а различает transfer-to/executor/transfer-from queues, idle/work, last/average/maximum и отдельное execution timing. Но фраза single inference в заголовке не делает каждую цифру per-request: average/max прямо накоплены по inferences объекта device. Источники README и actual binding расходились уже в 14.7.0, а в 13.0.13 реализация вообще делегирована внешнему бинарнику. Перенос этих полей в 16.18.6 или HPS недопустим. [W2-J-F02–F04]

Утверждение «есть TPU instructions artifact, значит частичный fallback невозможен» **не установлено**. Официальный datasheet описывает компиляцию в машинный код tensor cores, но не гарантирует, что каждый source operation отражён там, и не описывает host pre/post program. Source mapping/coverage остаётся отдельным недостающим документом. FULL и RAW эту гарантию не создают. [W2-J-F01,F05,F06]

От W1 неизменно: явные native load/run/status существенно сильнее одной метки UI, но current native boundary неизвестна; invalid-device control проверяет fail-closed в этой точке и не исключает partial partition; aggregate utilisation на shared ускорителе может принадлежать другим пользователям. Service-only может быть достаточен без shell, если организатор предоставляет приемлемую корреляцию и управление нужной моделью. Ни attestation, ни root privileges, ни отдельный profiler не объявляются обязательными правилами конкурса без ответа жюри.

## Источники, версии, даты, locators

Все новые вспомогательные материалы находятся только в `W2_J/`; исходные downloaded filenames сохранены. Таблица описывает evidence type отдельно от actual test status.

| ID | Первичный источник и версия | Locator / реальная проверка |
|---|---|---|
| W2-J-S01 | [LinQ HPS datasheet](https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf), LinQ/ХайТэк, 4 страницы, документ не сообщает revision/date на просмотренном text layer | Fresh web open200, page3 «Программный стек и инструменты», lines96–108; p1 инструменты и p4 перечисление документации. Дата search index не принимается за дату документа. Web screenshot request вернул лишь ссылку, actual image не получен/не просмотрен. urllib TLS EOF и curl schannel failure: local binary не скачан, визуальная проверка этой веткой не заявляется. PDF skill прочитан для read-only workflow. |
| W2-J-S02 | [pytpu13.0.13 metadata](https://pypi.org/pypi/pytpu/13.0.13/json), author Maxim Moroz; upload2021-12-01T15:38:07.719729Z | Fresh JSON200 и actual sdist200: [pytpu-13.0.13.tar.gz](https://files.pythonhosted.org/packages/0a/dc/92d61f0abe5dd5a41a6c60f52dd0f9bec208d5d7fb3438d43fe06913df3a/pytpu-13.0.13.tar.gz), SHA256 `39c394e3b3529b54227cd0d086e46e6309e1941b66f934e1d43255c6e1310853`. `SOURCE_13.0.13/`, complete tar member list `TREE_13.0.13.json`, README86–100; `pytpu/pytpu/__init__.py`1–19; `tools/get_fps.py`. |
| W2-J-S03 | [pytpu14.7.0 metadata](https://pypi.org/pypi/pytpu/14.7.0/json), author Alexey Antipin; upload2023-04-11T18:52:35.459665Z | Fresh JSON200 and actual sdist200: [pytpu-14.7.0.tar.gz](https://files.pythonhosted.org/packages/ba/5d/847666d4b956e100175f2c1fb92e1bf8a2bfa3a79c213ff4167edd95fe28/pytpu-14.7.0.tar.gz), SHA256 `54e63e4ecc787ab16e2ee3f32b3a4188928121b3954dfdf4334d9c7441b60f49`. `SOURCE_14.7.0/`, complete `TREE_14.7.0.json`, README86–100; `pytpu/pytpu/libtpu_bindings.py` and `tools/get_fps.py`. Method line spans/hashes in `SOURCE_LOCATORS.json`. |
| W2-J-S04 | [pytpu15.0.24 project](https://pypi.org/project/pytpu/15.0.24/), IVA-Tech, upload2023-11-27 | Fresh web project open/search + reused actual W1 sdist, SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. `_WORK/W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py`; W2-G exact AST/source locators and RAW/FULL analysis. Не загружался native binary. |
| W2-J-S05 | [LinQ Documentation](https://lin-q.ru/docs), LinQ, publication date absent | Fresh native urllib TLS EOF; web open inaccessible; **TinyFish fetch_content successfully read live navigation and links**, saved `DOCS_ALTERNATE.json`. Title «LinQ_Документация», robots noindex,nofollow. Navigation lists hardware manuals and Framework operator manual, not a profiler manual link. Это ограничение данной navigation, не всех файлов сервера. |
| W2-J-S06 | [MLCommons IVATech2020 harness](https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech), mmoroz/IVATech, pinned commit `89260c7a0bb2bb86f4adaf1d88e0307162eb602b` | Reused actual W1-15 source/log/system bytes и W2-G complete subtree. `IvaTPUSystemUnderTest.cpp`, submit/wait→QuerySamplesComplete; FPGA AlveoU200. Новая broad загрузка не повторялась. Это историческоеreported measurement, не наш hardware test. |

`SEARCH_1.json`…`SEARCH_5.json` сохраняют результаты новых targeted query batches; это index/search evidence, не live содержимое каждого результата. `FETCH.py` — helper download/read, `LOCATORS.py` — static AST/hashes. Они не моделируют SDK и не проверяют hardware. Несколько rg вызовов с Windows wildcard/неверным ожидаемым source path дали own path errors; исправлены прямым чтением complete tar member lists, никаких SDK ошибок из них не выводится.

## Факты с ограничениями

### W2-J-F01 — HPS profiler заявлен как мониторинг, а scope trace не описан

Тип `vendor_claim`, S01, page3. Performance Profiler описан как средство наблюдения скорости и загрузки вычислительных блоков. Power Monitor относится к мощности/тепловому режиму; DNN Stat назван на page1. Ни syntax запуска, ни пример export, ни единицы/источник измерения, ни request/model IDs в этих разделах не заданы. Поэтому **ни «только host estimates», ни «измеренные аппаратные per-request счётчики» из datasheet не следуют**. Наличие слова profiler не разрешает выбрать любую из этих интерпретаций. Page4 перечисляет User/Installation Guide, Developer SDK и Hardware Software Reference, но не предоставляет их содержимого. Вывод bounded до этого документа.

### W2-J-F02 — legacy timing shape имеет явно накопленные компоненты

Тип `historical_documentation`, S02/S03 README86–100, source not executed. Три очереди именуются `QUEUE_TRANSFER_TO`, `QUEUE_EXECUTOR`, `QUEUE_TRANSFER_FROM`; далее idle/work и тройка last/average/maximum. Average/maximum описываются как значения по всем inferences объекта device. Отдельно показаны `execution_timing` и глобальное `device.stats["mem"]`. Не установлены units, wall/device clock, reset/rollover, thread safety, serialization order, global across all processes vs this object, mapping last к вызову в concurrency. Даже если modern API повторяет shape, среднее/maximum нельзя приложить к requestN как его персональную latency. Само поле last без correlation тоже двусмысленно при overlapping requests. Описание execution on TPU в README — историческое API claim, не увиденная register instrumentation.

### W2-J-F03 — actual archives не содержат реализации обещанных timings

Тип `source_code`, S02/S03, actual downloaded files inspected. В13.0.13 `pytpu/pytpu/__init__.py` создаёт spec для `/usr/lib/pytpu.so` и экспортирует старые TPUDevice/TPUProgram/TPUProgramInfo. Полного native source/binary нет в tar member list. Поэтому numerical/timing implementation там восстановить нельзя.

В14.7.0 `pytpu/pytpu/__init__.py` импортирует `libtpu_bindings`, где CDLL target `/usr/lib/libtpu.2.so`, Device methods — create/init/info/load/run/submit; statuses получаются native. Static source не реализует README `load_inference_sync`/`result.timings`/`device.stats`; отдельные host helpers относятся уже к другому API. Это **более ранний конкретный пример README/source mismatch**, дополняющий W1 замечание о15.0.24. Он опровергает shortcut «возьмём любую из описанных статистик из public pip и получим current profiler». Не доказывает, что timings отсутствуют в отдельных иных native releases.

`disable_static_checker` присутствует только в старом README configuration example. Значение true отключает некий checker; ни semantic purpose, ни relation к fallback/partition coverage не описаны. Это **не strict/no-fallback flag**, и применять его ради доказательства исполнения нельзя.

### W2-J-F04 — `Estimated FPS` старого helper — host-derived throughput

Тип `source_code`, S02/S03 `tools/get_fps.py`; не выполнялся. Оба helper формируют задания, запускают asyncio tasks, окружают их host `time()` и делят `n_queries * batch` на elapsed. В13.0.13 per-call path включает load, awaited status.is_success, get outputs. В14.7.0 get outputs закомментирован, и используются иные native binding calls. Это показанная формула пропускной способности выбранного harness; она не отдельный аппаратный operations counter, не реализация Performance Profiler и не измеренный tensor-core-only time. Не переносить результаты разных code paths в одну latency table. Корректность work count/генерации данных/мульти-input здесь не проверялась; running helper на чужом устройстве не выполнялся.

### W2-J-F05 — executable artifact — полезная lineage boundary, но не whole-graph proof

Тип `vendor_claim` + `inference`, S01/S04. Машинный код tensor cores заявлен официально; `.tpu` передаётся в native program load, Python reference не исполняет fallback TensorFlow/PyTorch neural graph. Это усиливает свидетельство по сравнению с произвольным backend label. Но ZIP с metadata и weights не предоставляет проверяемую ISA semantics; наличие машинного кода внутри не доказывает отсутствие других stages или полноту lowering source graph.

Для покрытия нужны: source graph/weights hashes → compile configuration/target/version → report о преобразованных/fused/eliminated операциях и местах выполнения → hash loaded program. Операция может исчезнуть при корректном constant folding/fusion, поэтому наивное равенство числа nodes числу TPU instructions не является coverage criterion. Если compiler по конструкции выдаёт только цельную TPU программу или error, matching release documentation этой гарантии может заменить подробный partition report; такой документ пока не получен. Если format допускает host program, его штатные стадии требуют описания. Отсутствие Python CPU-model path не доказывает native guarantee.

### W2-J-F06 — FULL/RAW и host processing не классифицируют fallback

Тип `source_code` + `inference`, S04/W2-G-F03,F04. Enum передаётся native; Python allocations/reshapes зависят от artifact RAW heuristic, а numerical converter вызывается через отдельный `tpu_tlm_is` codec. Не установлены actual FULL stage placement и units timing. Поэтому host scaling/transpose/packing нельзя автоматически назвать hidden model fallback, а FULL нельзя развернуть в обещание all stages TPU. До ответа поставщика модельный graph boundary, штатный runtime tensor codec и отдельно написанные decode/NMS должны записываться раздельно. Correct numerical output и FULL↔RAW parity проверяют correctness, но не physical execution.

### W2-J-F07 — per-request evidence возможно без profiler, но требует доверенной корреляции

Тип `engineering_inference`, S04/S06, не продуктовая capability claim. Matching runtime completion trace, связанный с exact loaded artifact и согласованным physical device mapping, может быть сильнее aggregate profiler chart. Если организатор принимает live witnessed run в выделенном слоте с device identity, model load hash и контролируемым входом, отдельная profiler утилита не логически обязательна. Ни такой критерий, ни server trace capability сейчас не подтверждены. Приложение, runtime и организатор — разные trust boundaries; свои JSON поля сами по себе не становятся аппаратным подтверждением.

## Попытка опровержения и отрицательные результаты

Проверены пять targeted query batches: exact Performance Profiler/DNN Stat + LinQ/IVA; domain files.lin-q.ru profiler; русские профилировщик/профилирование; tpu_framework statistics/stat; legacy queue_timings, iva_tpu timings, disable_static_checker; compiler report/machine code; LinQ CPU fallback. Relevant primary результат — HPS datasheet и historical PyPI. Generic .NET LINQ, unrelated IVA и Google TPU results отвергнуты. Это достаточная локализация public evidence gap, не доказательство закрытости продукта.

**H1 «profiler — измеренная трасса именно нашего запроса».** Не подтверждено: datasheet не сообщает attribution, legacy averages имеют накопленный scope. Но гипотеза «profiler только estimates» тоже не доказана; инструмент не получен.

**H2 «можно взять timings из старого public API».** Shortcut опровергнут source mismatch и missing native implementation. Историческая форма statistics осталась пригодной для адресного запроса документации, не реализации.

**H3 «CPU fallback невозможен по формату инструкции».** Поиск поддерживает наличие machine-code compilation, но не гарантию whole graph или native stage exclusion. Гипотеза не опровергнута технически и не доказана; нужно release-matched statement/report. Формат `.tpu` и clear Python path недостаточны.

**H4 «для доказательства непременно нужен SSH».** Логически опровергается достаточным service contract: сервер может связать revision/artifact и requests с backend/device completion, а независимый инженер или live replay может подтвердить mapping. Но actual LinQ2026 service contract не получен, это условная архитектура. SSH тоже не гарантирует trace rights/эксклюзивность.

Alternate retrieval действительно выполнен: web читает PDF text, но прямые urllib/curl downloads не прошли TLS; screenshot tool вернул ссылку без image. Docs web/native не прошли, **TinyFish успешно получил навигацию**. Binary PDF/visual proof из этого не выдуманы. PyPI JSON и source bytes доступны, а внешний native implementation из source архивов не появляется. Credentials/регистрация/сообщения производителю не использованы.

## Адаптируемый протокол SSH/container

Это **наш будущий experimental design**, а не documented CLI LinQ. Ни один пункт не означает уже выполненную проверку.

1. **Предмет и критерий.** Получить от организатора ответ, какой graph обязан работать на LinQ и допустимы ли host pre/post/NMS/tracking. Согласовать минимально принимаемый пакет: witnessed run, native log, profiler export или engineer-confirmed mapping. Hardware attestation не навязывать.
2. **Inventory в пределах прав.** Сохранить actual SDK/runtime/compiler/driver/firmware/image digest и описание allocated device. Через поддерживаемый reader получить device JSON и объяснённое инженером соответствие path/instance физическому SKU/chip/PCI endpoint, если оно доступно. Названия serial/PCI JSON keys не угадывать. Device mapping контейнера означает доступ, а не исполнение.
3. **Lineage.** Для одного known-good custom artifact сохранить source/export/weights SHA256, compiler settings/version/target, full compile log и coverage report/guarantee при наличии. Хешировать actual loaded bytes, не только путь. В отчёте явно назвать необъяснённые host stages; не обещать whole graph без сведения F05.
4. **Один коррелируемый run.** Свой single-worker/process, разрешённый device, ограниченная последовательность valid inputs A/B с fresh run IDs. Для каждого: canonical tensor byte hash, dtype/shape/layout, frame/preprocess revision, load/program handle correlation при доступности, submit/completion timestamps+clock, native status/error, raw output hash. Если runtime сам не возвращает IDs, приложение связывает интервалы последовательно, и это отмечается как app attribution. Не выдавать app run ID за hardware task ID.
5. **Независимое звено.** Предпочесть официальную native/device trace с task/program/device correlation. При её отсутствии — согласованный выделенный слот и witnessed load/run с сохранёнными runtime outputs и mapping. Busy/power/temperature baseline+run — вспомогательное свидетельство; на shared device оно не исключает чужие задания. Если отчёт содержит last/avg/max, сохранить весь raw export и units/scope definitions, использовать только документированную per-call часть.
6. **Безопасный control.** В отдельном собственном disposable процессе повторить с заведомо отсутствующим device path **только если current API это поддерживает и обращение permitted**; либо новый свой контейнер без device mapping, если разрешено создание контейнера. Не отключать рабочее устройство, не менять host permissions/driver/modules и не снимать чужой mapping. Ожидать явную ошибку и отсутствие успешного модельного результата; success требует расследования, а не автоматического обвинения fallback. Если mapping скрыт/нельзя менять, пропустить control с причиной. Это контроль whole-path fail-closed в данной конфигурации, не unsupported-op partition test.
7. **Coverage gate отдельно.** Сверить actual compile report с agreed graph boundary; при наличии documented strict policy записать exact spelling/version из поставки. Сейчас такой опции нет в evidence. Vendor-supported unsupported-op compile example возможен только отдельным согласованным экспериментом, не fault injection на shared runtime.

Сильное сочетание: independently confirmed device identity + exact compiled lineage/coverage + runtime completion for our valid inputs. Слабое сочетание: application label + /dev listing + utilisation screenshot. Если доступ ограничен, сохранить реально достигнутый уровень и согласованное принятие жюри; не подменять gap декоративным индикатором.

## Адаптируемый протокол service-only

**Shell не является prerequisite**, если доступ поддерживает нужную custom модель и audit trail. Ни поля, ни endpoints ниже не утверждаются существующими; это требуемая информация контракта или поля нашего журнала.

1. Получить actual API/job documentation, authentication без записи secrets, permitted custom model format/upload/update/compile process, immutable revision/version selection, quotas/timeouts/concurrency, model retention и возможность получить logs. Отдельно выяснить, является API inference или simulation/demo; этот ответ подтверждает организатор. Имена endpoints не угадывать.
2. Зафиксировать mapping **client artifact hash → server accepted model revision → compiled artifact hash/target**. Если сервер компилирует сам и compiled bytes не выдаёт, достаточно server manifest с происхождением в рамках принятой trust model, но нельзя записать хеш исходного ONNX как хеш executable `.tpu`. Для prepared-only сервиса нельзя обещать исполнение наших weights.
3. Послать ограниченную последовательность двух-трёх valid distinct inputs с client run IDs, preserve exact submitted payload hash и tensor/preprocessing contract. Сохранить server request/job IDs, model revision echoed/read-back, receipt/queue/start/end/complete states, output body/hash. Результаты A/B должны меняться ожидаемо, а reference проверяется с numerical tolerance. Это проверяет соответствие входов/ответов; outputs можно вычислить и на CPU, поэтому correctness не physical proof.
4. Попросить доступный server-side trace/export либо demonstrator/engineer live verification, связывающий **server request ID → loaded revision/artifact → runtime completion → backend instance/device mapping**. Если отсутствует per-request hardware ID, server runtime owner может подтвердить mapping instance+временной слот и queue isolation. Какого уровня достаточно — решение жюри. Недоверенный `backend=LinQ` не подменяет этот ответ.
5. Negative control без отказа устройства: запрос к заведомо несуществующей model revision **только через documented selector и безопасную documented error path**. Он должен отклониться без результата другой default модели. Это проверяет fail-closed выбора модели, не устройство. Если revision selector отсутствует, не изобретать параметр и не посылать malformed native tensor. Дополнительный harmless control — локально в собственном клиенте не отправлять запрос, UI должен показать отсутствие inference result/новый status, а не старый cached output; аппаратного вывода из этого нет.
6. При разрешённом custom update можно в новом своём revision переключить known-good modelA→modelB и предъявить server acceptance/hash + различимые valid outputs. Это помогает выявлять подмену/необновление модели, но без trace не доказывает LinQ. Не удалять общие модели, не вызывать отказ сервиса, не менять backend чужих jobs.

Service-only sufficient branch: custom artifact/update semantics + exact revision selection + request/log correlation + accepted device evidence. Branch с prepared-only моделью или opaque backend требует решения организатора о допустимом scope; shell сам по себе эту проблему не решит. При full opaque service честная формулировка: «запрос отправлен в предоставленный организатором LinQ service, аппаратное исполнение подтверждается оператором/не независимо проверено» — выбрать верную часть после actual ответа.

## Матрица силы свидетельств

| Свидетельство | Что поддерживает | Что не закрывает |
|---|---|---|
| Successful versioned native open/load/status | Работа соответствующего runtime path | Реализацию native, whole graph, исходные weights |
| Artifact hash + compile coverage/guarantee | Lineage и выбранную границу graph lowering | Физическое выполнение конкретного request |
| Per-task completion с program/device mapping | Attribution выполнения в данной trust boundary | Верность compiler coverage и неподменённость source |
| Legacy last timing с подтверждённым scope | Один документированно сопоставленный timing | Attribution при concurrency без task ID |
| Average/max, FPS, aggregate utilisation | Нагрузку/throughput указанного scope | Per-request latency, our model identity, no fallback |
| Output parity/golden tensor | Numerical correctness данного input/path | Physical device identity |
| Invalid device/no mapping failure | Fail-closed данной точки/configuration | Частичный graph fallback и server model substitution |
| Unknown service revision rejection | Fail-closed model selection | Device execution или no-fallback native policy |
| Live engineer/jury witness в согласованном scope | Практическое принятие обязательного inference | Невыданные technical internals за пределами witness |

## Точные unknown и решающий будущий эксперимент

**U-J1:** matching release Performance Profiler/DNN Stat manual и один raw report. Нужны available launch method, version, privileges, measured vs estimated origin, units/clocks, queue inclusion, per-task/process/device scope, concurrency/reset/last semantics, overhead и program/device attribution. Resolution: выданный SDK docs/sample report или ответ engineer; сейчас manual отсутствует в полученной navigation/артефактах, не «не существует».

**U-J2:** compiler whole-graph/no-fallback guarantee, coverage/partition report или описанная executable ISA/host program semantics для actual release. Нужны fusion/elimination mapping, unsupported-op failure policy и отдельно placement FULL pre/post. Resolution: compile report одной нашей модели и matching reference; current binary native не восстанавливать по Python enum.

**U-J3:** actual access and accepted competition criterion. Resolution: root-owned onboarding/organizer question, не контактировать от пользователя самостоятельно. Точный вопрос: «Какая часть нашей нейросети должна исполняться на LinQ; допустимы ли host tensor conversion/NMS; какое свидетельство для SSH и service-only вы принимаете — runtime trace с artifact/request/device, live run с инженером или иной предоставляемый вами протокол?» Уточнение не навязывает attestation.

**E-J1, решающий controlled valid run после выдачи:** один approved custom artifact, source/compiled lineage, один явно выбранный endpoint/session, sequential A/B inputs, trace/native completion и observed device mapping; в отдельном своём контексте один разрешённый negative control. Перед стартом выяснить report units и correlation semantics. После сравнить IDs/hash chain и согласованную graph coverage. Success трактуется двумя независимыми statements: (a) данный artifact/input completion связан с этим LinQ; (b) compiler report/guarantee покрывает agreed graph boundary. Успех только (a) не закрывает (b). Если современный native trace недоступен, заранее согласованный witnessed run является практическим alternative acceptance, а степень независимости описывается явно.

## Компактная передача root

W2 добавил exact historical timing scope и проверил два дополнительных actual sdist:13.0.13 — external pytpu.so,14.7.0 — новый ctypes path без README timings, public modern profiler не получен. `disable_static_checker` не strict flag. `Estimated FPS` — host formula в helper, не device counter. Live docs navigation повторно получена alternate TinyFish, profiler guide link не обнаружен в ней; PDF visual verification не достигнута и не заявлена. Выполнена попытка опровержения machine-code/no-fallback shortcut: compiler machine code claim есть, whole-graph/host stages guarantee нет. Полные conditional SSH/service-only протоколы и safe controls выше. Для K013 нужно отдельно closed-model coverage и per-request physical attribution; FULL и numerical parity K009 их не заменяют. Для K014 shell не обязателен, но server custom revision+correlation+accepted evidence критичны. Hardware/SDK/compile/test успехов нет.
