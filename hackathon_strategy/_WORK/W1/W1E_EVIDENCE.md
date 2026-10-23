# W1E — вопросы, доказательство исполнения LinQ и честная подача качества

Дата исследования и доступа: 23.10.2026, Europe/Moscow (UTC+3); время отдельных HTTP-загрузок в файловых метаданных и MANIFEST.json. Даты версий источников указаны отдельно. Область: H10/H11/H12. Это исследовательские процедуры и банк вопросов, не сдаваемый сценарий, код или презентация. **Собственных SDK compile/LinQ inference/измерений качества или скорости не было.** Прочитаны исходные договор и тематическое задание, PLAN, релевантные соседние факты и открытые вопросы; аналоги заимствованы из W1B/W1C с сохранением их происхождения. Никаких вымышленных команд LinQ ниже нет.

## Что установлено и какое решение меняется

Сильное доказательство имеет две связанные части: происхождение и размещение вычислений модели, затем исполнение конкретного запроса на выданном устройстве. Полезный результат собственного UI, слова backend=LinQ, загрузка ускорителя и хеш ONNX по отдельности не закрывают эту цепочку. Для service-only возможна приемлемая проверка через оператора и серверную корреляцию; shell и аппаратная attestation не объявляются условиями конкурса. Уровень, принимаемый жюри, остаётся вопросом постановщику. Основание: linq_platform F287–F294, W1E-F04/F05 ниже.

До первого тяжёлого обучения следует получить реальный supported call на выданном доступе, договор о границе LinQ и формат доказательства. Успех штатной модели подтверждает путь доступа, но ещё не собственную модель и не полный обязательный кейс. Запись полезна лишь при разрешении съёмки и принятии её как свидетельства; она не становится заменой обязательного инференса автоматически. Основание правил: W1A-F07/F17; технические границы: W1E-F06.

## Реестр источников и происхождение

Все новые сетевые оригиналы/ответы сохранены в [SOURCES/W1E](../SOURCES/W1E/). Содержательная выписка — [EXTRACTS.md](../SOURCES/W1E/EXTRACTS.md); метаданные/хеши — [MANIFEST.json](../SOURCES/W1E/MANIFEST.json). Сохранённые источники соседей остаются в их папках; ссылки ниже относительны для переноса всего репозитория.

| ID | Источник, автор, дата/версия | URL и локатор; что прочитано |
|---|---|---|
| W1E-S01 | MLPerf Inference Rules, MLCommons; master commit `d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3`, commit date 2026-08-20T13:53:45Z, дата публикации отдельной редакции неизвестна | [Оригинал](https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/inference_rules.adoc). Локально `inference_rules.adoc`; §§2.2/2.7,3,5.1; строки60–100,139–154,402–419,465–477. Чтение web и raw, не выполнение benchmark |
| W1E-S02 | LoadGen README, MLCommons; commit `3fbc329939999c13d0a7b5e67fb2092287e06047`, commit date 2026-09-02T17:02:36Z | [README](https://github.com/mlcommons/inference/blob/3fbc329939999c13d0a7b5e67fb2092287e06047/loadgen/README.md). Локально оригинальное `README.md`; Introduction, Scope, Responsibilities, LoadGen over the Network. Web tree дал restricted fetch, raw HTTP успешно получен и прочитан; pinned bytes совпали. Не запуск |
| W1E-S03 | ONNX Runtime, Microsoft/ORT contributors; живая документация без даты/версии release на странице | [Execution Providers](https://onnxruntime.ai/docs/execution-providers/), разделы introductory architecture и Use Execution Providers; `ORT_PROVIDERS.html`. Сама страница не подтверждает наличие LinQ EP |
| W1E-S04 | ONNX Runtime, Microsoft/ORT contributors; живая документация без установленной release-версии | [Profiling tools](https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html), In-code profiling и EP Profiling; `ORT_PROFILING.html`. Только чтение, не наша trace |
| W1E-S05 | linq_platform, соседний research, 23.10.2026, источники 04:15–05:14 MSK | [RAW_FACTS](../../../research_link_platform/RAW_FACTS.md#f287) F287–F294; [W2-J](../../../research_link_platform/_WORK/W2_J_RESULT.md), source table и matrix. Первичное происхождение: S026 HPS datasheet p3, S063 pytpu15.0.24 upload2023-11-27, S075 IVATech2020 pinned subtree; это не три новых независимых подтверждения |
| W1E-S06 | evaluation, соседний research после W1/W2, 23.10.2026 | [OPEN_QUESTIONS](../../../evaluation/OPEN_QUESTIONS.md): Q001–Q015, E002/E005/E007/E008. [Human](../../../evaluation/report_human_evaluation.md), разделы «Какую разметку…», «Экспорт и LinQ…», «Быстрый граф…», «Минимальный набор…». Первичные основания восстановимы через F212–F234, не наш полевой тест |
| W1E-S07 | video_architecture, соседний research после W1/W2, 23.10.2026 | [OPEN_QUESTIONS](../../../video_architecture/OPEN_QUESTIONS.md#q001): Q001–Q005, E001/E018; различение issued grant, model boundary, accepted witness, источника/своего кадра и доставки события. Это proposed experiment, не выполненный slice |
| W1E-S08 | IVATech submission, MLCommons Inference results v0.7 (2020), pinned commit `89260c7a0bb2bb86f4adaf1d88e0307162eb602b` | [Subtree](https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech). Повторно прочитаны уже сохранённые `research_link_platform/_WORK/W1_15/MLPERF_SYSTEM.txt` и `MLPERF_LOG.txt`; S075 соседнего реестра. Не новая сеть и не наши измерения |
| W1E-S09 | W1C_ANALOGUES, эта волна, 23.10.2026 | [W1C](W1C_ANALOGUES.md): F01/F03/F05/F09; первичные S02, S05, S07, S13 и артефакты SOURCES/W1C. Официальные итоги/рассказ команды/таблица производителя различаются |
| W1E-S10 | W1A_RULES, эта волна, 23.10.2026 | [W1A](W1A_RULES.md) F07/F08/F09/F17 и реестр S01–S03: действующие FAQ и PDF, конфликт записи/съёмки и 6/7 критериев. Новое прочтение PDF мной не заявляется |

## Фактическая база

### W1E-F01 — правила benchmark определяют границу измерения

**Тип: первичная документация; прочитано, не запущено.** S01 требует согласованную систему/framework и воспроизводимость. В Single Stream следующий запрос зависит от завершения предыдущего; Offline измеряет поток заданной пачки. Latency задаётся от запланированной передачи запроса SUT до ответа LoadGen, а не только временем матричного ядра. Accuracy проверяется отдельным проходом с тем же кодом. Поэтому одно FPS без режима нельзя переводить в задержку или сравнивать с другим режимом. Локаторы: S01 §§2/3/5.1. Эти нормы относятся к MLPerf; не являются обязательным регламентом Моспрома. Заявлять «результат MLPerf» можно лишь при соблюдении его правил, включая требования к названию/логотипу; наш упрощённый тест следует называть своим тестом.

### W1E-F02 — LoadGen не удостоверяет модель, accuracy и устройство

**Тип: первичная документация + наш вывод; чтение README.** S02 различает генерацию/учёт запросов и ответственность пользователя за модель, форматы и оценку accuracy. Вывод для нас: VALID performance log не устанавливает correctness output, происхождение весов или физическое место исполнения. Network SUT имеет явно описанную границу timed processing; она не совпадает автоматически с нашей границей «кадр появился в интерфейсе». Локаторы: Scope, Responsibilities, Network. Даже реальный harness полезен только вместе с собственной реализацией SUT, metadata и accuracy evidence.

### W1E-F03 — зарегистрированный backend и фактическое покрытие графа различаются

**Тип: первичная документация; чтение ORT.** S03 описывает передачу поддержанных узлов/подграфов execution provider и порядок приоритетов, где неподдержанное первым может исполняться другим. Значит, список доступных/зарегистрированных providers не доказывает размещение каждого узла. S04 описывает JSON profiling с деталями выполнения; поддержка EP profiling зависит от EP/SDK. **Область:** это иллюстрация на ORT, не найденный LinQ интерфейс и не доказательство fallback в LinQ. Для actual LinQ нужен matching release документ или trace.

### W1E-F04 — LinQ profiler и старые Python поля не заменяют корреляцию

**Тип: сведения первичного документа/кода через соседний research.** S05/F287–F290: HPS datasheet называет Performance Profiler, но не задаёт request IDs, units, clock и scope. Legacy README разделяет transfer/executor queues и accumulated average/max; actual distributions расходятся с README. `Estimated FPS` helper вычислялся по host elapsed и количеству заданий; это не аппаратное время ядра. Не переносить старые поля и команды в текущую поставку. Реальная современная trace остаётся неизвестной.

### W1E-F05 — два звена доказательства и границы доверия

**Тип: инженерный вывод, не правило конкурса.** S05/F291–F294 дают две проверки: (1) исходный graph/weights → compile target/config/version → coverage/гарантия → loaded artifact; (2) конкретный input/request → completion этого artifact на mapped device → output. Хеш связывает bytes, но не устанавливает качество, placement, время создания и факт запуска. Correct output возможен на CPU; aggregate utilization может относиться к соседним заданиям. Для managed service серверный manifest и свидетельство оператора могут заменить недоступные bytes в рамках принятой жюри границы доверия. Это должно быть названо, а не выдано за независимую аппаратную верификацию.

### W1E-F06 — доступ к устройству и пригодность к демонстрации ещё открыты

**Тип: локализованное неизвестное.** S05 Q001–Q005, S07 Q001–Q003: shell/container, service, job, catalog — разные ветви. Публичная форма доступа не означает issued grant; full case, quotas, request schema, права custom model/update и accepted witness не выданы. Само SSH не гарантирует возможность установить daemon, открыть порты или получить RTSP. Модель из готового каталога может не иметь нужных классов. Поэтому в первые часы нужна проверка реального разрешённого пути, а не установка случайной версии SDK.

### W1E-F07 — исторический валидный benchmark не относится к современному LinQ

**Тип: опубликованный результат заинтересованной команды; локальное чтение сохранённых первичных metadata/log, не запуск.** S08 `system` указывает IVA_FPGA_1, Xilinx Alveo U200, 250MHz, host i7-7700K, Ubuntu18.04, Tensorflow1.15.0 и версии compiler/runtime. `log` — SingleStream Performance, 90th percentile 12,230,138 ns, VALID, max_async_queries1, min_duration60000ms. Этот хорошо оформленный набор связывает заявленный результат со старой конфигурацией, но не доказывает ASIC LinQ2026 и не предсказывает нашу скорость. Его 60 секунд также нельзя переносить как норматив длительности нового MLPerf (ср. S01). Не смешивать опубликованный historical result с фактическим тестом команды.

### W1E-F08 — качество событий и отсутствие тревог требуют разных оснований

**Тип: методические выводы соседнего evaluation.** S06/F214/F229–F234: AP объектов не равна правильности связи человек–СИЗ, событийной полноте или полезности доставки. Для semantic false records на фиксированный исходный камера-час нужны полный учёт доставленных записей и разбор каждой с достаточным контекстом; просмотр всего видео без тревог не обязателен для этого узкого показателя. Но он не устанавливает recall/нормальное время. Для recall нужна независимая GT или обоснованная вероятностная выборка. Дубликаты, поздние истинные записи и семантически ложные утверждения следует разделять. В source-view и operator wall-view разные знаменатели. Нельзя тихо вычеркнуть unknown/drops, чтобы улучшить результат.

### W1E-F09 — аналоги предупреждают о семантике требований, а не сообщают вкус нашего жюри

**Тип: происхождение из W1C.** РЖД2024/Black Duck, рассказ участника (W1C-F03/S05): вопросы о числе видео и распознаваемых нарушениях, низкий балл запускаемости за документацию. Норникель2024, рассказ участника (W1C-F05/S07): лучший итоговый score не стал первым общим местом; ограничения server environment. Кейс LinQ СЗФО2024 (W1C-F01/S02): требование использования платформы известно, способ доказательства победителей не установлен. Это аргументы задать точные вопросы о workload, обязательности и запуске; не «такие вопросы задаст жюри Моспрома». Сведения о live-записях вопросов с таймкодами в этой ветке не добыты.

## Матрица: что предъявлять и чего этим не доказать

Все строки ниже — предлагаемый protocol на основе F03–F08. Они не означают наличие перечисленных возможностей в SDK.

| Свидетельство | Что оно поддерживает | Чего оно не поддерживает само по себе |
|---|---|---|
| Device inventory и версия runtime | Идентичность среды в документированном scope | Что наша модель выполнилась на этом устройстве |
| Source/compiled hashes, target, compile config/report | Происхождение exact artifact, заявленное покрытие graph | Запуск конкретного входа, качество данных/разметки |
| Runtime load + request completion + program/device correlation | Исполнение указанного пути в данной trust boundary | Правильность всего lowering, отсутствие иных NN stages |
| Успешный ответ API с request/model revision | Корреляция сервиса и версии, если это server receipt | Physical device, если сервер не сообщает доверенное mapping |
| Device telemetry / utilization | Нагрузка указанного scope в интервале | Наш request/model на shared device, no fallback |
| Golden output / native-export-target parity | Численное согласие на данных входах с tolerance | Физическое устройство и обобщение на все видео |
| Live run с новым valid input | Реакция системы на этот вход в данный момент | LinQ без runtime/device mapping; долговременная устойчивость |
| Запись экрана с логом и таймкодом | Сохранённое наблюдение прошлого запуска | Разрешение съёмки, текущая доступность или обязательное live compliance |
| Хеш архива/исходников и git commit | Точный состав snapshot, declared history | Авторство, создание всего за хакатон, hardware execution |
| Нагрузка/latency trace | Производительность этой версии/workload/границ | Accuracy, число поддерживаемых камер в иных условиях |
| Свидетельство инженера/жюри в согласованном слоте | Принятие указанного исполнения в указанном scope | Нераскрытые внутренности платформы вне свидетельства |

## Предлагаемый ранний протокол E-W1E-01: один воспроизводимый LinQ run

**Вопрос/решение:** работает ли выданный путь, поддерживает ли он свою модель и как будет доказано обязательное исполнение? Входы: actual grant, matching sample/docs, разрешённые данные, модель и I/O contract. Не выполнен. Команды берутся только из issued инструкции.

1. Зафиксировать ответ постановщика о NN boundary и accepted witness; получить работающий штатный пример. Сохранить revision инструкции, mode доступа и версии. Авторизация/секреты не включаются в публичный архив.
2. Создать run ID и manifest: source code commit; source/export/compiled model hashes, каждый со своим stage; input video/frame/tensor hashes, class mapping, shape/dtype/layout, pre/post и threshold; actual target/runtime/compiler/driver/firmware, насколько это выдаётся. Для managed service — accepted revision и mapping operator manifest; неизвестные поля оставить unknown.
3. Выполнить один разрешённый штатный inference с documented completion и выгрузить output. Привязать client run/request, server job, model revision/artifact, device instance/slot и input/output. Сначала достаточно одного call; не начинать нагрузку shared-сервиса без выданных лимитов.
4. Затем провести tiny own-model smoke и 2–3 различных валидных входа, включая negative, сохраняя исходный ответ и привязку. Если есть reference, сравнить output с явно указанной tolerance. Это проверка wiring/parity, не статистика качества.
5. Получить available runtime trace/report или согласованное свидетельство инженера о request→device. Если доступны только клиентские timestamps, назвать результат service completed RTT; device-only latency unknown.
6. Сразу сохранить исходные логи, manifest, output и ошибки, затем hash snapshot в командном разрешённом хранилище. Фиксировать, что реально удалось: штатная модель / своя модель / end-to-end приложение. Запись экрана допускается только после разрешения конфликта F07/F17 W1A; текстовые логи также хранятся с учётом режима данных и правил публикации.

**Исходы:** штатный call работает → доступ smoke пройден; собственный graph не проходит → получить minimal failing report и supported fallback model route; service не даёт своих весов → немедленно уточнить допустимость catalog scope; непрозрачная device correlation → оформить trust boundary и согласовать witness. **Условие завершения:** один связанный manifest/input/completion/output и ясный список неизвестного. Успех не устанавливает полноту кейса, нагрузочную устойчивость или field accuracy.

### E-W1E-02: нестабильный доступ, evidence snapshot и запасной маршрут

Это предложение, не найденное правило. Первый успешный связанный прогон следует сохранять сразу и повторять после каждой существенной смены модели/runtime. После потери доступа сохранять последний verified version отдельно от текущей ветки: время последнего успеха, exact artifact, stage, request IDs, error log, open/outstanding requests и состояние очереди. Client timeout не равен отмене на устройстве; неизвестный outcome не записывается success/failure молча. Ретраи зависят от выданной idempotency/quota semantics (video_architecture Q002).

Дальше имеются три разные ветви: восстановить доступ и показать live; показать разрешённую запись/артефакты успешно выполненного LinQ run с честным временем; показать приложение на local reference отдельно с явной маркировкой «этот показ не LinQ». Последние две ветви требуют ответа постановщика о принятии технического доказательства при сбое; local CPU/GPU не выполняет обязательное условие вместо LinQ. При отсутствии успешного LinQ run нельзя создавать впечатление, что он был.

## Что публиковать рядом с цифрой скорости

На основе F01/F04/F08 и evaluation Q010–Q013 предлагается карточка измерения. Одна строка числа должна указывать модель и precision, source/resolution, target и версии, batch, inflight/concurrency, число потоков, warmup/cold-start, длительность и число завершённых samples, границы часов, p50/p95 (и n), throughput, drops/errors/outstanding, queue lag. Это рекомендуемые поля, не официальный threshold.

Разделить как минимум: **device inference interval**, только если документирован device timer; **completed service RTT** по одному клиентскому monotonic clock; **end-to-end frame→durable event/visible UI** с названной границей и согласованными clock domains; **throughput** фактически завершённых samples на wall duration. Отдельно назвать model-only и decode/pre/post/tracking/transport. Для batch throughput считают реальные samples, не padding; submissions/ACK не равны completions. При file replay сообщить скорость воспроизведения и source-time; accelerated replay не доказывает live real-time.

Не вычислять device latency вычитанием ping: inference request включает payload transfer, очередь, serialization и server processing, тогда как ping измеряет другую нагрузку. Не делить единицу на FPS для получения latency при batching/pipelining/concurrency. Warmup исключают только по заранее описанному правилу и показывают cold-start отдельно, если он влияет на эксплуатацию. При нестабильном shared доступе сообщают среду и queue effects, а не приписывают всю задержку чипу. Метрика по successful-only outputs идёт рядом с counts пропусков/ошибок и coverage, иначе «быстро» может означать «не обработали трудные кадры».

## Честная карточка качества для смешанного жюри

Это предложенная структура доказательства, не готовый слайд. Для каждого заявленного результата: (а) что предсказываем и для кого; (б) на каких независимых данных и сколько их; (в) что считаем успехом и при каком пороге; (г) измеренные значения и знаменатели; (д) где ломается и что проверять далее. Не заполнять цифры до измерения.

| Уровень claim | Что показать | Существенный предел |
|---|---|---|
| Кадр/объект | Class-specific precision/recall/AP, annotation completeness, IoU/threshold, object counts | Каска найдена ≠ принадлежит человеку ≠ нарушение |
| Человек/отношение | Correct wearer/ownership, observable/not observable, примеры crossing/occlusion | Закрытая голова/крепление/герметичность не могут стать уверенностью по отсутствию пикселей |
| Событие | Определение эпизода, dwell/cooldown/reset, temporal matching, TP/FP/FN/U и задержка вместе с misses | Красивый один клип не даёт recall; short events могут быть пропущены sampling |
| Доставка оператору | Semantic false records/исходный камера-час и отдельно burden за wall-hour; duplicate/late/unknown; E/C close | Отсутствие тревог не означает отсутствие нарушений; fixed source hours ≠ operator hours |
| Неблагоприятные условия | Отдельные night/backlight/small objects/occlusion/motion/reconnect cases и counts | Curated stress suite не оценка естественной частоты ошибок |

Происхождение теста следует объяснять: official holdout, свой frozen holdout, train/dev или illustrative demo. Разрезанные соседние кадры одного ролика не независимый unseen-camera test. Если полных событийных labels нет, честно сказать, какой узкий показатель удалось получить. «0 ложных на H часов» — наблюдение этого корпуса с counts и exposure, не гарантия отсутствия false alarms в будущем. Показ неудачи имеет смысл как проверяемое ограничение с текущим статусом «unknown/не поддержано» и способом снятия; универсального доказательства, что такое признание повышает балл нашего жюри, не найдено.

## Приоритетный банк вопросов и решения после ответа

Вопросы ниже — **предлагаемые вопросы команды**, а не реконструированные реплики с защит. Ответ фиксируется с автором/ролью, временем, версией кейса, точной формулировкой и каналом; устный ответ затем кратко подтверждается в разрешённом канале организаторов. Внешние сообщения этой веткой не отправлялись.

| ID / срок / кому | Точный вопрос | Какой выбор меняет ответ | Происхождение / закрытие |
|---|---|---|---|
| Q-E01 P0 первый час, platform engineer | Что именно выдано команде: shell/container, model API, job или catalog; где один рабочий пример и можно ли загружать/обновлять свои weights/graph? | Own detector route vs supported catalog; распределение человека на платформу | linq_platform Q001, video_arch Q001; issued sample + successful call |
| Q-E02 P0 первый час, постановщик | Какая именно NN-часть обязана исполняться на LinQ? Разрешены ли host decode/NMS/tracking и отдельные secondary NN на CPU/GPU? | Graph partition, число моделей и допустимость сокращённого scope | linq_platform Q005; письменная граница + task version |
| Q-E03 P0 первый час, постановщик/организатор | Какое свидетельство LinQ требуется на чек-поинте и защите: live run, server trace, инженер-свидетель или сохранённый run? Как принимается результат при общей недоступности? | Время раннего evidence capture, fallback, proof package | F05/F06, W1A-F07/F17; accepted witness без придуманной обязательной attestation |
| Q-E04 P0 первый час, platform engineer | Каков единый release/target и какие model I/O, supported export, preprocessing, decoder/NMS, golden inputs/outputs выданы? | Окружение и корректность собственного pipeline; заморозка модели | linq_platform Q002/Q003, evaluation Q009/Q011; versioned bundle/manifest |
| Q-E05 P0 первый час, постановщик | Какие нарушения обязательны, какие приоритетны, что именно считается нарушением/unknown и целевым полезным уведомлением? | Обязательный scope, labels, event state machine | evaluation Q001/Q003/Q008; full case + examples/acceptance |
| Q-E06 P0 первый час, постановщик | Как оценивается качество: official evaluator, единица/метрика/split/threshold; есть ли минимум FPS/latency и где их границы? | Что оптимизировать и на каких данных; отказаться от выдуманного общего F1 | evaluation Q001/Q014, F09; original evaluator/example |
| Q-E07 P0 первый час, данные/организатор | Какие видео и labels разрешено использовать, публиковать и записывать; есть ли camera/session lineage и negative time, можно ли менять split/добавлять данные? | Train/holdout/demo, правомерность evidence и доступность репозитория | evaluation Q002/Q005/Q006, W1A-F17; actual files/license/rules |
| Q-E08 P0 первый час, platform engineer | Каковы per-team quotas, concurrent requests/batch/payload, queue/timeout/cancel/retry semantics, persistence и network permissions? | Live vs job, sampling/camera admission, невозможность слепого retry | linq_platform Q004, video_arch Q002/Q003; issued limits + tiny benign check |
| Q-E09 P0 чек-поинт1, организатор | Какая форма оценивания действует для нашего технологического кейса: 6 или 7 критериев, веса/уровни 0–3, роль чек-поинтов, обязательный minimum scope? | Приоритеты работ и состав доказательств по критериям | W1A-F08/F09/F10; actual scoring sheet, не гипотеза равных весов |
| Q-E10 P0 до записи, организатор | Как согласуются разрешённое подготовленное видео и запрет самостоятельной съёмки? Какие screen/video/data/result материалы можно записывать и публиковать, кем и где? | Допустимость backup-recording и public artifacts | W1A-F17; конкретное разрешение, не общий совет «снять заранее» |
| Q-E11 P1 чек-поинт1, постановщик/пользователь | Кто получает тревогу, какое действие должен выполнить, какая цена пропуска/ложной и допустимая частота напоминаний; нужна ли интеграция? | UI, delivery, порог/dwell и убедительная пользовательская проверка | evaluation Q001/Q008, →operator_product; workflow acceptance |
| Q-E12 P1 чек-поинт1, platform engineer | Чем связать наш request/model revision с физическим устройством; что означает profiler/timer, есть ли coverage/fallback policy и trace export? | Сила claims, измерение device-only и доступность own-model proof | linq_platform Q005/Q012, F04/F05; matching report+docs либо accepted witness |
| Q-E13 P1 чек-поинт2, эксперт | Вот verified slice и таблица обязательных требований: какой конкретный незакрытый пункт блокирует зачёт/пилот; что достаточно показать к следующему этапу? | Сокращение необязательной работы, приоритет последнего дня | F09 и правила W1A; ответ привязать к артефакту, не «вам нравится?» |
| Q-E14 P1 чек-поинт2, evaluation/data expert | Согласны ли с нашим definition/split/unknown/close и тем, что числа являются supplemental, а не официальными? Где нужен отдельный negative/сложный пример? | Исправить неправомерный claim до финала, freeze политики | evaluation Q001/Q005/Q014/Q018; review manifest+metric card |
| Q-E15 P1 чек-поинт3, постановщик | Сохранённый LinQ run относится к модели X/version Y, текущий live status Z; достаточно ли этого свидетельства и какой short recheck нужен перед защитой? | Final proof/fallback, приоритет между retrain и закреплением verified version | F05/F06; конкретное принятие версии и статуса |

Первый час не превращается в пятнадцать последовательных интервью. P0 E01/E02/E03/E05/E06 определяют маршрут; release/данные/лимиты запрашиваются одним артефактным пакетом ответственным за платформу и данным. Остальные вопросы задаются после получения конкретного object: модели, журнала, оценочной формы. До ответа нельзя молча считать официальным локальный показатель, partial LinQ graph или backup video.

## Неизвестное, предел поиска и W2

1. **Accepted evidence / NN boundary** открыты из-за отсутствия полного кейса и issued access. Несколько публичных путей уже исследованы в linq_platform W2-J/W2-L; эта ветка не повторяет бесплодный общий поиск SDK. Следующий сильный шаг — exact full case/account docs/ответ инженера и E-W1E-01. Новая общая публикация о profiler не заменит missing contract.
2. **Кто на аналогах реально доказывал LinQ:** W1C нашёл СЗФО2024 winners/requirement, но не артефакт и не процедуру. Полезная W2 — targeted winner repo/release/video с действительным runtime log и таймкодом. При отсутствии закончить точным unknown, а не «победители показывали телеметрию».
3. **Запись/AI/помощь и 6/7 criteria:** противоречия ведёт W1A. До resolution не рекомендовать неразрешённую съёмку или арифметику 1/7 итогового балла. Здесь не найдено подтверждённой универсальной формы disclosure.
4. **Метрики**: наш тест ещё не выполнен; нужны фактические clips/model/output/logs. При W2 полезнее проверить карточку результата на supplied material, чем добавлять ещё общий benchmark tutorial.
5. **Новая сеть этой ветки:** MLCommons policy/LoadGen docs и ORT docs. Web tree LoadGen restricted, raw успешно получен; прочитанные оригиналы сохранены. Ничего закрытого не обходилось. Документы не подтверждают текущие инструменты LinQ. PDF этой веткой не открывались: ограничения производителя взяты с точным происхождением из уже сохранённого соседнего research.

## Адресная передача

- **linq_platform:** нужен matching release artifact→compile coverage→request/device completion. Принятый witnessed run может быть достаточен без собственного profiler; спросить E02/E03/E12. Не подменять server revision hash source ONNX hash.
- **evaluation:** карточка для жюри должна держать вместе metric definition, sample/группы, TP/FP/FN/U, exposure, E/C, latency+n+misses и placement. Не потерять W2-уточнение: false-delivered/source-hour не всегда требует exhaustively annotated no-alarm video.
- **video_architecture:** source/frame/request/model correlation и полный outstanding ledger нужны уже с первого slice; показывать late/stale status, не использовать успешные completions как единственный знаменатель. E01/E08 — input контракт.
- **W1F/defence:** доказательство LinQ следует отделить от пользовательского UI; backup recording только после разрешения E10. Вероятные темы вопросов можно выводить из рисков, но не атрибутировать нашему жюри без записи.
- **W1D/execution:** ранний milestone — verified one-call path + saved evidence; далее own-model slice. Смена модели после evidence snapshot создаёт новую версию, а не задним числом обновляет доказательство.
