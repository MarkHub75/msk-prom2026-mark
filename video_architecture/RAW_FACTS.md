# Подробная доказательная база video_architecture

Дата сборки и подтверждённая дата обращения: **2026-10-23 Europe/Moscow (UTC+3)**. Collector не получал новую сеть, не запускал приложения/камеры/SDK/LinQ и не выполнял предложенные E. W1 закончена до прерывания и не повторялась; несохранённый первый critic не восстанавливался. Сохранённый CRITIC создан отдельным fresh-context critic_resume, затем выполнены шесть W2 по K001–K010. Нет полного кейса, issued SDK/grant, actual LinQ output и runtime benchmark. Ранние интервалы W1_01/03 приблизительны: они не являются точным журналом отдельных обращений. SHA snapshot доказывает состав сохранённых bytes, а не неизменность current upstream или работу программы.

## Как читать базу

CLAIM — заявление автора; DOC — первичная документация; CODE — прочитанный код; MEASURED — чужое опубликованное измерение с условиями; LOCAL — реально полученные локальные metadata/арифметика; INFERENCE — наш инженерный проект/вывод; HYPOTHESIS — кандидат; UNKNOWN — не установлено. Тип и исполнение раздельны. Любые runtime-команды и конфигурации здесь **proposed, не запускались**. Локальные арифметические расчёты не benchmark.

Сохранены исследовательские пересказы и точные параметры/команды обеих волн; это не копии внешних страниц. Повтор одного primary chain не даёт независимого подтверждения. W2 уточняет область W1; исходная W1 не является release lock. Каждый F имеет явный HTML anchor. Полная обратная карта — [_WORK/ID_MAP.md](_WORK/ID_MAP.md).

## Тематический навигатор

- 01 LinQ: доступ, размещение, происхождение
- 02 Ingress, RTSP, decode, clocks и library knobs
- 03 Payload, JPEG quality, transport и bandwidth
- 04 Scheduler, bounded work, state и temporal contract
- 05 Каталог проектов: version, license, hardware, reuse
- 06 Events, brokers, outbox, concurrency и DB boundaries
- 07 Evidence: сегменты, generations, mapping, pins и finite policy
- 08 Browser: identity, transport, render-credit и lifetime
- 09 Resilience, measurement и интерпретация benchmark
- 10 Поставка, Astra Linux и безопасность
- 11 Capacity50/500 и полный resource inventory
- 12 Адресные передачи и отрицательные результаты
- 13 Conditional minimum45ч: placement, owners, gates, latency

# 01 LinQ: доступ, размещение, происхождение

<a id="f001"></a>

## F001 — Отсутствие issued bundle/device access в соседнем linq_platform; CPU/mock не device run

**Тип основания:** LOCAL/UNKNOWN. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S001](SOURCES.md#s001). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L19](_WORK/W1_01.md); W1-01-F01.

- **F001 [LOCAL прочитано / UNKNOWN execution]**: пакет прямо сообщает отсутствие proprietary matched SDK/native/driver/firmware bundle и реального LinQ доступа. Собственные ONNX CPU и fake-native проверки относятся к другим границам. Локатор: machine YAML `hardware_access`, `sdk_access`, `tested_here`; RAW linq_platform:F333.

<a id="f002"></a>

## F002 — Условные access modes и разделение host decode vs TPU в linq_platform

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S001](SOURCES.md#s001). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L20](_WORK/W1_01.md); W1-01-F02.

- **F002 [INFERENCE из соседнего пакета]**: linq_platform:F312 различает custom-model service, ready-model catalog, shell/container, job-only и managed-video. Там service-only может быть достаточен без SSH; shell не доказывает root/Docker/ports/daemon lifetime. linq_platform:F332 различает dataset image runner и RTSP service, HPS optional video encode и HX/RK3588 decode. Использовать как исходную карту, не как предоставленные возможности.

<a id="f003"></a>

## F003 — Незакрытые issued-access/I-O/quota/recovery вопросы соседнего linq_platform

**Тип основания:** UNKNOWN. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S001](SOURCES.md#s001). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L21](_WORK/W1_01.md); W1-01-F03.

- **F003 [UNKNOWN]**: соседние linq_platform:Q001–linq_platform:Q005 адресно локализуют режим/обновление своей модели; matched release; I/O; quotas/lifecycle/network; принятую NN-границу и execution evidence. linq_platform:Q004 содержит payload/inflight/batch/QPS, timeouts/cancel, CPU/RAM/storage/persistence и camera reachability. linq_platform:Q025 concurrency/fairness и linq_platform:Q028 recovery scope также открыты. Не повторять исследование SDK: получить actual delivery contract и передать его соседям.

<a id="f004"></a>

## F004 — Корпоративный HPS SLA и вакансии не устанавливают hackathon API/SLA

**Тип основания:** CLAIM/DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S001](SOURCES.md#s001). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L22](_WORK/W1_01.md); W1-01-F04.

- **F004 [DOC/CLAIM в соседнем пакете]**: linq_platform:F030 относит 24/7 support HPS к корпоративному SLA, не к хакатону; linq_platform:F031/linq_platform:F032 описывают разные варианты вакансии, не действующий inference API. Такие зацепки не основания для нашего SLA/API.

<a id="f005"></a>

## F005 — Homepage предлагает заказать демонстрацию и получить тестовую среду. `/tech` описывает преобразование модели/квантование/граф/TPU и вычислитель…

**Тип основания:** CLAIM. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S002](SOURCES.md#s002), [S003](SOURCES.md#s003). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L57](_WORK/W1_01.md); W1-01-F05.

**F005 [CLAIM, S002/S003, прочитано]**. Homepage предлагает заказать демонстрацию и получить тестовую среду. `/tech` описывает преобразование модели/квантование/граф/TPU и вычислитель int8; это не описание сетевого сервиса. Ни это предложение, ни технологический список не устанавливают выданные команде протокол, CPU, codec, endpoint или способ загрузки модели. [LinQ](https://lin-q.ru/), [technology](https://lin-q.ru/tech).

<a id="f006"></a>

## F006 — В разделе HPS опциональны платы аппаратного **видеокодирования** H.264/H.265. В разделе HX вычислитель LinQ H соседствует с RK3588; перечисленные…

**Тип основания:** CLAIM. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S004](SOURCES.md#s004), [S003](SOURCES.md#s003). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L59](_WORK/W1_01.md); W1-01-F06.

**F006 [CLAIM, S004, прочитано]**. В разделе HPS опциональны платы аппаратного **видеокодирования** H.264/H.265. В разделе HX вычислитель LinQ H соседствует с RK3588; перечисленные возможности decode находятся в блоке CPU, отдельно от TPU. Это не основание приписать decoder чипу LinQ H, любой PCIe-плате или удалённому стенду. Заявленные максимумы кодеков не измеряют наш многопоточный pipeline. [HPS/HX](https://lin-q.ru/sol).

<a id="f007"></a>

## F007 — ПО на `/sol` предоставляет Python 3.8 API и CLI для quantize/compile; download требует регистрации **и** верификации. Это не доказательство…

**Тип основания:** CLAIM/DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S004](SOURCES.md#s004). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L61](_WORK/W1_01.md); W1-01-F07.

**F007 [DOC/CLAIM, S004, прочитано]**. ПО на `/sol` предоставляет Python 3.8 API и CLI для quantize/compile; download требует регистрации **и** верификации. Это не доказательство текущего Python runtime стенда и не grant на устройство. В этой ветке формы не отправлялись. [Software section](https://lin-q.ru/sol).

### Compose: конкретные эксплуатационные ловушки

<a id="f134"></a>

## F134 — `POST /v1/submitjob` возвращает `jobId`, `jobArn`, `jobName`. В прочитанной полной схеме нет `clientToken`/idempotency key или заявленной гарантии…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S106](SOURCES.md#s106). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L33](_WORK/W2_01.md); W2-01-F01.

**F134 [DOC + INFERENCE, S106].** `POST /v1/submitjob` возвращает `jobId`, `jobArn`, `jobName`. В прочитанной полной схеме нет `clientToken`/idempotency key или заявленной гарантии deduplicate submit. `jobName` документирован как имя с ограничениями формата; считать его ключом идемпотентности нельзя. Это **отсутствие документированного обещания**, а не измеренное доказательство, что каждый повтор обязательно создаёт дубль. Практическое следствие: для этого аналога same-name retry нельзя считать безопасным восстановлением lost ack. `x-amzn-RequestId` из HTTP response — идентификатор вызова, не заявленная замена клиентскому idempotency key. Наш `request_id` сам по себе не меняет семантику внешнего сервера.

<a id="f135"></a>

## F135 — DescribeJobs принимает список до 100 job IDs и отдаёт список job details, в том числе статус. Операция требует известного ID; endpoint не описан…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S107](SOURCES.md#s107). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L35](_WORK/W2_01.md); W2-01-F02.

**F135 [DOC, S107].** DescribeJobs принимает список до 100 job IDs и отдаёт список job details, в том числе статус. Операция требует известного ID; endpoint не описан как lookup по нашему request UUID. Метаданные job не являются тензорным inference result. Для аналогичного interface отдельно нужны location/format/retention артефакта результата. Нет выполненного poll и нет измеренного QPS/consistency bound.

<a id="f136"></a>

## F136 — CancelJob работает для SUBMITTED/PENDING/RUNNABLE; PENDING может ожидать завершения dependencies. Для STARTING/RUNNING cancellation не происходит,…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S108](SOURCES.md#s108). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L37](_WORK/W2_01.md); W2-01-F03.

**F136 [DOC, S108].** CancelJob работает для SUBMITTED/PENDING/RUNNABLE; PENDING может ожидать завершения dependencies. Для STARTING/RUNNING cancellation не происходит, но операция всё равно может успешно ответить HTTP200. Следствие: cancel acknowledgement не terminal proof; race «status runnable → cancel → starting» должен разрешаться повторной проверкой. Наш ledger хранит `cancel_requested`, а credit остаётся занятым.

<a id="f137"></a>

## F137 — TerminateJob переводит STARTING/RUNNING в FAILED; более ранние состояния отменяет. HTTP200 имеет пустой body. Наш вывод: отправка terminate —…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S109](SOURCES.md#s109). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L39](_WORK/W2_01.md); W2-01-F04.

**F137 [DOC, S109].** TerminateJob переводит STARTING/RUNNING в FAILED; более ранние состояния отменяет. HTTP200 имеет пустой body. Наш вывод: отправка terminate — намерение, terminal observation и его сохранение — отдельный шаг; documentation API call не даёт нам измеренной upper bound времени окончательного освобождения всех ресурсов.

<a id="f138"></a>

## F138 — По умолчанию job timeout отсутствует. `attemptDurationSeconds` ≥60 s применяется после `startedAt`; termination best effort, возможна…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S110](SOURCES.md#s110). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L41](_WORK/W2_01.md); W2-01-F05.

**F138 [DOC, S110].** По умолчанию job timeout отсутствует. `attemptDurationSeconds` ≥60 s применяется после `startedAt`; termination best effort, возможна дополнительная задержка. SIGTERM затем SIGKILL через 30 s — описанная последовательность, не жёсткий deadline облачного scheduler. Timeout-killed job не повторяется, иной failed attempt при разрешённых retries получает новый отсчёт. Поэтому этот механизм не является полным TTL от submit до освобождения.

<a id="f139"></a>

## F139 — RUNNABLE может оставаться неопределённо долго; STARTING не включён в timeout. RUNNING с оставшимися retry attempts может вернуться в RUNNABLE:…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S111](SOURCES.md#s111). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L43](_WORK/W2_01.md); W2-01-F06.

**F139 [DOC, S111].** RUNNABLE может оставаться неопределённо долго; STARTING не включён в timeout. RUNNING с оставшимися retry attempts может вернуться в RUNNABLE: failure попытки ещё не terminal job. Terminal SUCCEEDED/FAILED history хранится **не менее** 7 дней. Это минимальная retention истории, не верхняя execution TTL и не обещание удаления точно на 7-й день. Попытка заменить unknown обязательным release через «достаточно подождать timeout/7days» опровергается этими условиями.

<a id="f140"></a>

## F140 — Полезный контраргумент к «lost job ID навсегда»: ListJobs имеет case-insensitive JOB_NAME filter и пагинацию; при filter jobStatus игнорируется и…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S112](SOURCES.md#s112). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L45](_WORK/W2_01.md); W2-01-F07.

**F140 [DOC → INFERENCE, S112].** Полезный контраргумент к «lost job ID навсегда»: ListJobs имеет case-insensitive JOB_NAME filter и пагинацию; при filter jobStatus игнорируется и возвращаются все статусы. Без filter/status по умолчанию только RUNNING — такой scan пропустил бы очередь/terminal. Наш уникальный lowercase nonce в имени помогает положительно найти job и затем DescribeJobs. Однако документация здесь не даёт atomic create-if-absent, уникальности имени и finite visibility bound. Ноль найденных совпадений не доказывает, что submit не был принят; нельзя на этом основании release/re-submit. Несколько совпадений — reconcile всех, а не выбрать первый. List permissions/retention/page completeness — дополнительные prerequisites. Это ограниченный recovery aid, не доказанная замена идемпотентности.

<a id="f141"></a>

## F141 — Triton позволяет отдельно запросить output binary (`binary_data`, общий `binary_data_output`); size задаётся `binary_data_size`, metadata…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S045](SOURCES.md#s045). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L47](_WORK/W2_01.md); W2-01-F08.

**F141 [DOC, S045].** Triton позволяет отдельно запросить output binary (`binary_data`, общий `binary_data_output`); size задаётся `binary_data_size`, metadata описывает shape/datatype. Binary blocks идут после JSON в порядке outputs; native-size little-endian row-major без padding. Пример `[3,2] FP32` имеет 24 B tensor body. В absence output binary flag данные могут возвращаться JSON; размер JSON numeric arrays нельзя считать как `numel*sizeof(dtype)`. Это конкретный протокол Triton, не обнаруженная возможность LinQ.

<a id="f142"></a>

## F142 — Triton ensemble описывает preprocessing→inference→postprocessing на сервере и уменьшение передачи intermediate tensors между client/server. Это…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S058](SOURCES.md#s058). **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L49](_WORK/W2_01.md); W2-01-F09.

**F142 [DOC, S058].** Triton ensemble описывает preprocessing→inference→postprocessing на сервере и уменьшение передачи intermediate tensors между client/server. Это первичный архитектурный пример возможности server-side postprocess. Он не подтверждает доступность Triton, Python backend, NMS operator или install permissions на стенде LinQ. Для нашего placement нужен actual contract; не переносить ensemble config как готовый рецепт.

<a id="f143"></a>

## F143 — Минимум — один local durable DB writer и один scheduler/dispatcher owner на `(service_endpoint, tenant/quota_domain)`. Если несколько процессов…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L53](_WORK/W2_01.md); W2-01-F10.

**F143 [INFERENCE, опирается на F134, F135, F136, F137, F138, F139, F140 и F093].** Минимум — один local durable DB writer и один scheduler/dispatcher owner на `(service_endpoint, tenant/quota_domain)`. Если несколько процессов могут отправлять jobs, они атомарно claim-ят строки/credits в общей подходящей БД либо только один процесс является submit owner. DB transaction не охватывает внешнюю сеть: намерение commit-ится до send, ack commit-ится после. Это предотвращает потерю обязанности, но само по себе не обеспечивает exactly-once submit. Durability/backup DB — W2-E/K008; ниже гарантии предполагают сохранность ledger commit, а не любой disk loss.

В row хранить:

- `request_id` — UUID, стабильный для одного неизменного logical request; full `(camera_id,stream_epoch,frame_id[,crop_id])`, `model_revision`, `preprocess_revision`, payload hash/size и `request_contract_revision`.
- `endpoint_id`, `tenant_id`, `quota_scope`, `state`, `state_version`; `remote_job_id` nullable и отдельные attempt records, если внешний backend допускает несколько actual jobs. `UNIQUE(endpoint,tenant,request_id)` и unique known job ID в его namespace. Повтор с тем же ID и другим hash запрещён до сети.
- `remote_credit_held`/weight, `submit_intent_committed_at_utc`, `first_possible_send_at_utc`, `last_attempt_at`, `live_deadline_utc` с clock-domain/uncertainty; monotonic deadlines лишь внутри текущего run. После restart не вычитать старый monotonic из нового run.
- `idempotency_scope`, key, contract validity window, `server_expiry_at` **только если документирован**, `last_remote_state`, `last_poll_at`, `next_reconcile_at`, `cancel_requested_at`, `unknown_reason`, `terminal_reason`, `terminal_evidence_ref`.
- `result_state` отдельно: `not_available/pending_fetch/fetched/invalid/expired/unavailable`, artifact locator/hash/bytes, `live_disposition=eligible/stale/epoch_mismatch/...`. `applied_to_camera`/dedup key нужен отдельно от credit. Не хранить многомегабайтные tensors в каждой event/outbox row; bounded fetch/spool policy.

Идентичность quota tenant/service сохранять даже при смене токена/URL alias. Нельзя «получить свободные credits», создав новый endpoint label для того же удалённого лимита.

### Состояния и разрешённые переходы

| Наше состояние | Что достоверно известно | Credit | Переход и граница |
|---|---|---:|---|
| `not_submitted` | Intent ещё не мог уйти в сеть | 0 | Атомарно проверить budget, claim owner, записать `submitting`+credit; commit успешен **до** network send. Просроченное удалить/закончить `terminal/not_sent` без send |
| `submitting` | Намерение сохранено; send мог произойти, ack ещё не сохранён | 1 | Valid ack+job ID → `accepted`; доказанный non-acceptance → `terminal/rejected`; ambiguous error/timeout/crash → `unknown`. Это резерв даже если crash фактически был до send |
| `accepted` | Job identity подтверждена и сохранена; backend принял обязанность | 1 | Status queued/starting остаётся accepted с detailed remote state; running → `running`; terminal proof → `terminal`; невозможность проверить → `unknown` |
| `running` | Последнее подтверждение исполнения, не обещание текущей активности | 1 | Может стать queued/accepted при backend retry; terminal → `terminal`; timeout/error status → `unknown`. Local result expiry не меняет credit |
| `unknown` | Мог быть принят/работать/завершиться; неизвестность причинно записана | 1 | Status/idempotent lookup/resolved owner evidence восстанавливают `accepted/running/terminal`; без доказательства credit удержать. Неизвестное новое status enum, пустой lookup/404/auth failure — не terminal |
| `terminal` | Доказана невозобновляемая финальность **всего job**, либо job точно не был принят/отправлен | 0 после commit | Сохранить evidence+release одной transaction/CAS ровно один раз. Успешный job может иметь потерянный результат; failed job может оставить diagnostic artifact. Terminal не переводится обратно по запоздалому nonterminal poll |

`terminal/not_sent` и `terminal/rejected` — локальные итоги без remote job, не выдуманные статусы провайдера. Rejection освобождает credit только при контракте «эта ошибка означает не принят», а не по произвольному HTTP400/500. Cancellation intent — поле/command, не отдельное доказательство terminal. Polls одного job сериализовать; late старый ответ не понижает уже доказанное terminal, конфликтующие terminal сведения сохранять для escalation.

### Инварианты двух независимых бюджетов

<a id="f144"></a>

## F144 — Пусть `K_remote` — наш консервативный cap разрешённых outstanding jobs/весов, не придуманная квота LinQ. Для одноэлементных jobs без array/fan-out

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L80](_WORK/W2_01.md); W2-01-F11.

**F144 [INFERENCE].** Пусть `K_remote` — наш консервативный cap разрешённых outstanding jobs/весов, не придуманная квота LinQ. Для одноэлементных jobs без array/fan-out:

`held = count(state in {submitting,accepted,running,unknown}) <= K_remote`.

`free_remote = K_remote - held`; атомарное резервирование необходимо до возможного send. При весах использовать сумму задокументированных worst-case weights; неизвестный неограниченный fan-out не укладывается в обещание bounded work. Для batch job credit может ограничивать jobs, но нужен ещё лимит frames/bytes/work внутри job. Наш cap ограничивает нашу порождённую работу, не чужие jobs и не время ожидания в shared queue.

`local_submit_calls <= K_submit_calls`, `local_control_calls <= K_control_calls`, `local_fetch_calls <= K_fetch_calls`; отдельные byte caps для input upload и result fetch/postprocess. Local slot возвращается после фактического прекращения клиентской операции/освобождения его ресурсов; истечение app deadline без завершения blocked native thread ещё не освобождает его память/socket. Удалённый credit при этом остаётся. При process crash local calls исчезают, persisted held не уменьшается.

Новые свежие frames отправлять только при обоих доступных ресурсах, fair camera admission и живом deadline. Для poll/cancel/reconcile выделить control capacity отдельно: занятые inference slots не должны лишать систему возможности освободить known credits. Bounded retries/backoff+jitter, rate cap и очередь control IDs, а не tensor payloads. Допустимо останавливаться с меньшим количеством доступных credits из-за unknown, но нельзя возвращать их «для прогресса» без основания.

Без доказанной idempotency один фактический network submit attempt — одна возможная remote обязанность. Скрытые SDK/proxy retries должны быть выключены/учтены; иначе один ledger credit может породить несколько jobs. Новая попытка без dedup должна сначала резервировать **ещё один** credit и отдельный attempt, что сохраняет bound, но не решает дубль/устаревший кадр; минимум45ч такую повторную отправку не делает. При подтверждённой idempotency несколько попыток одного immutable key в его действующей scope/window покрываются одной обязанностью, лишь если сервер гарантирует single job и lookup того же outcome. Результат дедуплицируется отдельно.

### Fault/restart traces

<a id="f145"></a>

## F145 — Примеры ниже — ожидаемый проектный trace, не log выполненного эксперимента

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L94](_WORK/W2_01.md); W2-01-F12.

**F145 [INFERENCE].** Примеры ниже — ожидаемый проектный trace, не log выполненного эксперимента.

| Сбой/гонка | Правильное восстановление | Запрещённое сокращение |
|---|---|---|
| Timeout до submit ack, ID неизвестен | `submitting → unknown`, held остаётся. Query по client key, если контракт есть. Same-key submit допустим только при действующей server dedup и ещё живом frame deadline; если request уже stale, query-only предпочтителен, чтобы не создать впервые устаревшую работу | Новый request ID сразу после timeout; reset semaphore = reset remote jobs |
| Server accepted, process crash до persist job ID | После restart row всё ещё submitting/unknown с прежним UUID/hash/credit. Lookup по ключу возвращает ID. Если лишь AWS-подобное имя — положительный paginated search помогает, zero match не разрешает release | Считать job непринятым, потому что в DB `job_id=null` |
| Crash после intent commit до send | Неотличим от предыдущего случая без provider evidence; консервативно unknown. При valid idempotency и свежести можно same-key retry; иначе hold/escalate | «Row submitting старше 5 s, значит send не было» |
| Retry того же request ID | Проверить hash/model/scope/key window; повторный ack того же job не увеличивает число obligations, terminal effect idempotent. При неизвестной idempotency не retry автоматически | Дедуплицировать только result, оставив дубли remote work |
| Job ID известен, local timeout/epoch reset | Live waiter получает Gap; старый result не идёт в tracker/UI. Collector по ID продолжает status/cancel до terminal | Возвращать remote credit при очистке reorder buffer/смене camera epoch |
| Cancel HTTP success, статус ещё running | Cancel intent записан; credit удержан; poll/поддержанный terminate по policy. Только documented terminal/полный expiry proof → release | Принять HTTP200 cancel за остановку kernel/job |
| Restart всех client processes | Admission закрыт при старте; проверить ledger/quota namespace, восстановить held, переclaim собственных leases, reconcile known IDs, submitting → unknown. Старые video epochs не восстанавливать как live; новые latest frames ждут free credits | Начинать с held=0, чистить «старые» rows или создавать второй scheduler owner |
| Job исчез/404/lookup empty; result TTL прошёл | `unknown`, reason и последняя надёжная remote observation. Оператор/owner resolution либо доказанный full TTL. Result unavailable и execution unknown — разные поля | 404=SUCCEEDED, отсутствие результата=FAILED, ошибка auth=job deleted |
| Terminal наблюдён, crash до local release commit | После restart status/reconcile повторяется; CAS/transaction записывает terminal и освобождение ровно один раз | Release в RAM до DB commit, затем повтор release после restart |
| DB commit error/disk full при полученном ack | Остановить новые submit; сохранить diagnostic где возможно. Предыдущий persisted submitting credit остаётся; не терять обязанность и не «продолжать без ledger» | Разрешить новую отправку, считая failed ack persistence будто remote не принял |

После startup reconciliation допустимо возобновить только на **доказанно свободном остатке** budget; не требуется ждать всех unknown при наличии free credits, но unresolved credits всегда учитываются. Если unknown возрастает до `K_remote`, admission=STOPPED. Если есть системный риск недостоверности ledger/namespace, stop сразу. UI: `analysis unavailable / remote jobs unresolved`, счётчик known/unknown и last fresh result age; live video может продолжаться. Escalation — подготовленный локальный incident packet, а не отправленное здесь сообщение владельцу.

### Когда TTL действительно позволяет release

<a id="f146"></a>

## F146 — Различать: (1) client RPC deadline; (2) frame live deadline; (3) execution-attempt timeout; (4) максимальную жизнь job от acceptance, включая…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L113](_WORK/W2_01.md); W2-01-F13.

**F146 [INFERENCE, ограничено F138/F139].** Различать: (1) client RPC deadline; (2) frame live deadline; (3) execution-attempt timeout; (4) максимальную жизнь job от acceptance, включая queued/starting/retry; (5) retention status/results; (6) retention idempotency record. Только документированный полный job expiry/release contract может заменить terminal observation для remote accounting. Для unknown-before-ack нужен ещё bound последнего возможного acceptance: зависший proxy/запоздалый send не должен создать job после локального решения об expiry. Требуются серверный `not_after`/lease или эквивалентный доказанный acceptance cutoff, clock-error margin и запрет поздних retries. Client timestamp+длительность сами по себе этого не доказывают.

При key-retention expiry same-key retry может стать **новым** submit; не отправлять старый UUID после окна как средство reconciliation. Если terminal record может исчезнуть раньше восстановления, нужны собственный persisted terminal witness/поддержанный audit lookup; иначе UNKNOWN даже при известном ID. AWS-подобные running timeout и ≥7-day terminal history не дают такой полной гарантии. Следовательно bounded ресурсное состояние возможно ценой остановки; **bounded непрерывное автоматическое обслуживание и auto-resume без idempotent submit/lookup/полного TTL в общем случае не доказуемы**. Предпочтение для live — сервис с проверяемым request lifecycle либо разрешённый свой worker, который можно корректно ограничить; недоступный contract не исправляется частыми fresh submits.

<a id="f208"></a>

## F208 — Условная матрица доступа и размещения

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L105](_WORK/W1_01.md); дополнительная тематическая выписка.

## Условная матрица доступа и размещения

Все строки **[INFERENCE/UNKNOWN]**, а не предсказание выдачи. Общая очередь/квоты — дополнительная ось, которая может сочетаться с SSH, API и GUI. VPN — сетевой транспорт/доступность, не право запуска кода. GUI может давать underlying shell либо только форму; факт GUI сам по себе не классифицирует capability.

| Режим | Наблюдаемые признаки выбора | У команды | На стороне LinQ | Что проверять прежде переноса; главный предел |
|---|---|---|---|---|
| SSH/VPN + свой long-running process | Именная shell/учётная запись, рабочий каталог, documented runtime, разрешённый собственный процесс; отдельно выделены device/quota/ports | UI, event DB, clips и источник; либо только UI, если remote persistence разрешён | Наш минимальный adapter/worker; decode/preprocess рядом с accelerator, **если** CPU/codec и compressed-video ingress доступны; tracking/rules можно рядом с worker, чтобы не возвращать tensors через WAN | SSH не подтверждает Docker/root, входящие порты, install, RTSP reachability из LAN команды, session persistence или exclusive device. Если контейнер нельзя — supplied venv/process. Через outbound connection/разрешённый tunnel можно ограничиться одним каналом, без открытия camera VLAN |
| Image/frame API | Документирован encoded image MIME/format, dimensions/max bytes, result schema, auth, request IDs | Ingest/decode, sampling, временное состояние, события, клипы/UI; JPEG encoding only if API accepts | Decode encoded image и NN по API; preprocess/NMS только согласно contract | JPEG не универсален; проверить small-PPE quality. Server roundtrip включает queue/codec. API-only может быть достаточен без собственного SDK, но нужен свой model version/update или достаточный catalog, accepted execution evidence |
| Tensor API | Names/layout/dtype/shape/scales явно заданы; endpoint принимает bytes/tensors | Decode, resize/letterbox/color/layout/packing; tracking/rules/events/UI | NN worker и documented pre/post; не приписывать JPEG decoder | Стоимость raw tensor WAN, exact dtype/contiguity и output sizes. Подмена input format запрещена логикой контракта, а не удобством клиента. Нужны bounded inflight и неизменяемая модель |
| Shared queue / job service | submit → job ID → pending/running/terminal; slots/lease/rate quota/429 либо лимиты в инструкции | Fair per-camera scheduler, latest/deadline admission, collector результатов, все persistent state/UI | Managed queue + worker; файл/тензоры, при наличии видео — server decoder | Предел задают turnaround p95/p99 и чужая нагрузка. App timeout не равен cancel. Поздний terminal result можно игнорировать для live overlay, но до terminal job может потреблять quota; не дублировать запрос. Если turnaround неприемлем, честный offline анализ, а не надпись realtime |
| Ограниченная GUI/remote desktop | Только upload/run/download/настройка model; нет поддержанного callable API/процесса | Источник/подготовка файлов, UI продукта и обработка выгруженных результатов, если они машиночитаемы | Ручной запуск supplied pipeline/model | Первым делом проверить скрытую за GUI разрешённую автоматизацию/CLI/API, модель updates, outputs/timestamps и session lifetime. Если их нет, unattended live integration не подтверждена; GUI smoke/witnessed LinQ run не доказывает live product. Автоматизация кликов сама по себе не снимает квоты/ограничения |
| Managed video endpoint (соседняя условная альтернатива) | Принимает stream URL/upload video; отдаёт timestamped detections/events; documented codecs | Gateway для доступности камеры, хранение/продуктовый UI по договорённости | Ingest/decode/NN, иногда tracking/rules | Нужен действующий выданный продукт, не ссылка на отдельный IVA CV. Узнать, как передать свои классы/model revision, сохранить source timestamps и доказать NN execution |

### Порядок выбора за первые минуты доступа

1. **Control plane**: что можно загрузить/скомпилировать/выбрать и как обновить собственную версию модели? Выданный endpoint готовых моделей не автоматически достаточен для PPE. Сохранить immutable model/artifact/config hashes и baseline golden input.
2. **Execution grant**: свой process/container либо managed call/job? Узнать allowed own restart и запрет на reset shared device. Не требовать SSH, если custom service всё покрывает.
3. **Payload + outputs**: encoded image/tensor/video, размер, dtype/layout/batch, pre/post responsibility, detections/raw outputs/events и geometry. Получить minimal request, result и один подтверждённый terminal success.
4. **Network**: из какого направления разрешены TCP-сессии; доступ к localhost worker через разрешённый tunnel; upload bandwidth/RTT; camera URL с remote host может быть недостижим. Не публиковать камеры в интернет для обхода NAT.
5. **Lifecycle/quota**: max payload/batch/inflight/QPS, lease/TTL/session, очередь между командами, cancellation semantics, disk persistence, CPU/RAM, compiler quota. Протокол подтверждён инструкцией/ответом владельца и коротким тестом, не рекламой продукта.
6. Измерить полезный двухкамерный маршрут с реальной очередью и затем выбрать decoder placement. Ни успешный `ssh`, ни `docker ps`, ни device utilization по отдельности не подтверждают inference нашей NN на LinQ.

### Бюджет, который можно считать до доступа

**[INFERENCE, арифметика; не benchmark]**: для tensor `[1,3,640,640]` float32 размер `1×3×640×640×4 = 4 915 200 B`; при 10 sampled frames/s это `49 152 000 B/s`, или `393.216 Mbit/s` без transport overhead **на одну камеру**. Для uint8 — `1 228 800 B/frame`, `98.304 Mbit/s` при 10 fps; uint8 допустим только по input contract. Значения не требования кейса. JPEG требует измерить размер на actual frames и качество; compressed video — codec/decoder/network support. Host/queue latency не выводится из LinQ TOPS или PCIe bandwidth.

Для последовательного single-inflight запроса throughput ограничен `1 / T_roundtrip` frame/s; при concurrency `C` верхняя арифметическая граница `C / T_roundtrip`, лишь если нет других bottleneck/quota. `T_roundtrip` в секундах включает очередь и payload, а не только accelerator time. Это помогает соседям V04/V05 сравнить network placement, но не разрешает повышать C без поддержанного runtime contract.

# 02 Ingress, RTSP, decode, clocks и library knobs

<a id="f025"></a>

## F025 — Для 45 часов принять базу: MediaMTX как общий RTSP ingress/разветвитель и имитатор камер; отдельный worker чтения/декодирования на камеру; внутри…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L7](_WORK/W1_02.md); W1-02-F01.

**INFERENCE F025.** Для 45 часов принять базу: MediaMTX как общий RTSP ingress/разветвитель и имитатор камер; отдельный worker чтения/декодирования на камеру; внутри worker PyAV/FFmpeg с ограниченными timeout и непрерывным чтением, после decode — слот последнего кадра; LinQ adapter потребляет кадры с назначенной частотой. OpenCV оставить для обработки массивов и быстрого smoke test, не назначать его `CAP_PROP_BUFFERSIZE=1` механизмом надёжности. Основания: F026, F027, F028, F029, F030, F031, F032, F033, F034, F035, F036, F037, F038, F039. GStreamer предпочтителен, если в команде уже уверенно используют его bus/state machine и если нужен управляемый аппаратный pipeline; осваивать весь GStreamer впервые во время 45 часов — дополнительный интеграционный риск (наш вывод, не измерение).

Необязательно ставить decode рядом с LinQ. При API кадров decode остаётся на стороне команды. При SSH на хост и разрешённой установке пакетов/доступе к RTSP можно перенести весь ingress/decode туда и передавать сжатое видео; CPU/GPU/NPU на том хосте неизвестны. Наличие RTX 4070 у команды позволяет проверить NVDEC как локальный decode, но не доказывает CUDA на удалённом хосте и не заменяет обязательный inference на LinQ. При WAN передаче размер выходного изображения и формат согласуются с V04; нельзя декодировать в BGR и бессистемно отправлять весь исходный FPS.

<a id="f026"></a>

## F026 — RTSP demuxer умеет RTP через UDP и TCP interleaved; HTTP/HTTPS tunneling — отдельные варианты. `rtsp_transport tcp` задаёт TCP, `rtsp_flags…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S024](SOURCES.md#s024). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L47](_WORK/W1_02.md); W1-02-F02.

**F026 — DOC, S024, прочитано.** RTSP demuxer умеет RTP через UDP и TCP interleaved; HTTP/HTTPS tunneling — отдельные варианты. `rtsp_transport tcp` задаёт TCP, `rtsp_flags prefer_tcp` лишь предпочитает его, когда доступен. `reorder_queue_size` измеряется пакетами; `buffer_size` — байтами socket buffer; `max_delay` — не тот же параметр. UDP reorder отключается при `max_delay=0`. Current docs задают RTSP `timeout` как TCP socket I/O timeout в микросекундах, `listen_timeout` как секунды ожидания входящего подключения (включает listen mode). Общий `rw_timeout` также µs. Следствие: timeout ограничивает операцию, не выполняет полноценный reconnect и не ограничивает end-to-end age кадра. TCP удобен в сети с неизвестным NAT/firewall, но транспорт сам не гарантирует свежесть; UDP допускает потери, поэтому минимальная буферизация меняет устойчивость картинки.

<a id="f027"></a>

## F027 — В n8.0 option `timeout` записывается во внутреннее поле `stimeout`, default0; внешнего AVOption `stimeout` в прочитанной таблице нет.…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S025](SOURCES.md#s025). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L49](_WORK/W1_02.md); W1-02-F03.

**F027 — CODE, S025, не выполнено.** В n8.0 option `timeout` записывается во внутреннее поле `stimeout`, default0; внешнего AVOption `stimeout` в прочитанной таблице нет. `listen_timeout` default−1; `reorder_queue_size` default−1 (авто). TCP URL получает `?timeout=...`; `udp_read_packet` также использует stimeout в poll loop и возвращает ETIMEDOUT. Это важное уточнение к краткому тексту DOC, называющему timeout TCP: в конкретной n8.0 реализации он участвует и в UDP ожидании. Не переносить этот вывод на все версии/обёртки. В популярных старых ответах 2014 года встречается `-stimeout`; перед применением проверять **именно установленный** `ffmpeg -h demuxer=rtsp`. FFmpeg CLI версия может отличаться от встроенного FFmpeg в PyAV/OpenCV.

Предлагаемый начальный **smoke test**, FFmpeg n8.0, числа — проектные, не оптимальные:

```sh
ffmpeg -hide_banner -rtsp_transport tcp -timeout 5000000 -i rtsp://HOST:8554/cam1 -map 0:v:0 -an -f null -
```

Для сравнения UDP:

```sh
ffmpeg -hide_banner -rtsp_transport udp -timeout 5000000 -max_delay 100000 -reorder_queue_size 64 -i rtsp://HOST:8554/cam1 -map 0:v:0 -an -f null -
```

Здесь 5 000 000 µs=5s; 100 000 µs=100ms и 64 пакета — старт эксперимента. Сначала убедиться, что сеть/камера умеет выбранный транспорт; затем варьировать задержку, а не применять `nobuffer/low_delay/probesize=32/analyzeduration=0` пачкой без теста. Слишком малый probe может лишить декодер параметров потока. `-f null` всё ещё предполагает декодирование при выбранном стандартном output codec; это не тест одного demux.

### GStreamer: три независимых очереди, а не один latency

<a id="f028"></a>

## F028 — rtspsrc сам поднимает RTP manager с reorder/jitter/RTCP. Default transport negotiation UDP unicast → UDP multicast → TCP; ограничивается…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S026](SOURCES.md#s026). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L67](_WORK/W1_02.md); W1-02-F04.

**F028 — DOC, S026, прочитано.** rtspsrc сам поднимает RTP manager с reorder/jitter/RTCP. Default transport negotiation UDP unicast → UDP multicast → TCP; ограничивается `protocols`. `latency` — миллисекунды, default2000; `drop-on-latency` defaultfalse ограничивает jitterbuffer заданным latency. `tcp-timeout` — µs, default20 000 000; `timeout` — µs ожидания UDP до попытки TCP, а не общий read timeout. `GstRTSPSrcTimeout` в docs поддержан только для RTCP-triggered timeout. Нельзя полагаться только на это сообщение для обнаружения зависшей камеры: нужен watchdog поступления декодированных кадров и обработка bus ERROR/EOS.

<a id="f029"></a>

## F029 — Долгий TCP stream может накапливать задержку из-за drift RTP clock относительно client clock. `tcp-timestamp=true` timestamp-ит RTP по времени…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S026](SOURCES.md#s026), [S029](SOURCES.md#s029). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L69](_WORK/W1_02.md); W1-02-F05.

**F029 — DOC, S026+S029, прочитано.** Долгий TCP stream может накапливать задержку из-за drift RTP clock относительно client clock. `tcp-timestamp=true` timestamp-ит RTP по времени получения и обходит этот механизм drift; при burst-отправке сервером способен создать другие проблемы. GStreamer release1.24.10 (2024-12-03) содержит backport этой возможности; прочитанная текущая API-страница точно указывает since1.24.10 и defaultfalse. Это **режим для сравнения в soak test**, не универсальное включение. Проверить доступность `gst-inspect-1.0 rtspsrc` в установленной версии.

<a id="f030"></a>

## F030 — `queue` создаёт отдельный поток. По умолчанию блокируется при первом из лимитов 200 buffers / 10MB / 1second. `leaky=downstream` (2) выбрасывает…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S027](SOURCES.md#s027). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L71](_WORK/W1_02.md); W1-02-F06.

**F030 — DOC, S027, прочитано.** `queue` создаёт отдельный поток. По умолчанию блокируется при первом из лимитов 200 buffers / 10MB / 1second. `leaky=downstream` (2) выбрасывает старые buffers; `upstream` (1) — новые. Для latest-frame аналитики после decode логичен downstream. Задать `max-size-buffers=1 max-size-bytes=0 max-size-time=0` — значит лимитировать кадрами и выключить другие лимиты, а не оставить тройной default. Dropping encoded buffers перед decoder может разрушать межкадровые зависимости: raw leaky queue ставить **после** decoder. Jitter drop до decode — другая, сознательная плата потерями изображения.

<a id="f031"></a>

## F031 — `appsink` имеет собственную очередь даже после `queue`; `max-buffers=0` означает unlimited. Медленное извлечение raw samples способно съесть…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S028](SOURCES.md#s028). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L73](_WORK/W1_02.md); W1-02-F07.

**F031 — DOC, S028, прочитано.** `appsink` имеет собственную очередь даже после `queue`; `max-buffers=0` означает unlimited. Медленное извлечение raw samples способно съесть память. Старый интерфейс `max-buffers=1 drop=true` выбрасывает старые; с1.28 `drop` deprecated в пользу `leaky-type`, тоже since1.28. Нельзя скопировать `leaky-type` в старую GStreamer1.24 и считать pipeline переносимым. `try-pull-sample` даёт timeout; приложение должно освобождать GstSample/GstBuffer и корректно делать unmap.

Предлагаемый H.264 CPU pipeline для интеграции с appsink (набор элементов проверить через gst-inspect; **не запущен**):

```text
rtspsrc location=rtsp://HOST:8554/cam1 protocols=tcp latency=100 drop-on-latency=true tcp-timeout=5000000
 ! rtph264depay ! h264parse ! avdec_h264
 ! queue max-size-buffers=1 max-size-bytes=0 max-size-time=0 leaky=downstream
 ! videoconvert ! video/x-raw,format=BGR
 ! appsink max-buffers=1 drop=true sync=false
```

`latency=100` — гипотеза для теста. `sync=false` снимает ожидание sink clock; не устраняет encoder delay, jitter, decode reorder и накопление вне appsink. Для H.265 нужны h265 depay/parser/decoder; наличие plugin и поддержка профиля — отдельно. CPU videoconvert/BGR может стать дороже собственно аппаратного decode. Для production raw latest-frame pool лучше одной из нескольких очередей; callback appsink должен быстро передать владение/ссылку и вернуться.

### OpenCV: почему CAP_PROP_BUFFERSIZE не является настройкой RTSP

<a id="f032"></a>

## F032 — `CAP_PROP_OPEN_TIMEOUT_MSEC` и `READ_TIMEOUT_MSEC` — **open-only**, применимы к FFmpeg/GStreamer backend; передаются params в constructor/open.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S030](SOURCES.md#s030). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L89](_WORK/W1_02.md); W1-02-F08.

**F032 — DOC, S030, прочитано.** `CAP_PROP_OPEN_TIMEOUT_MSEC` и `READ_TIMEOUT_MSEC` — **open-only**, применимы к FFmpeg/GStreamer backend; передаются params в constructor/open. `CAP_PROP_HW_ACCELERATION` тоже open-only и backend-specific. Работа свойства зависит от backend/драйвера/сборки. Практика `cap.set(READ_TIMEOUT...)` после open не равна настройке timeout. Нужно логировать `cv2.__version__`, `getBuildInformation`, `getBackendName`/CAP_PROP_BACKEND, а не просто версию pip пакета.

<a id="f033"></a>

## F033 — `CvCapture_FFMPEG::setProperty` в4.13.0 обрабатывает POS_MSEC/FRAMES/AVI_RATIO, FORMAT и CONVERT_RGB; default возвращает false. **BUFFERSIZE не…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S031](SOURCES.md#s031). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L91](_WORK/W1_02.md); W1-02-F09.

**F033 — CODE, S031, прочитано.** `CvCapture_FFMPEG::setProperty` в4.13.0 обрабатывает POS_MSEC/FRAMES/AVI_RATIO, FORMAT и CONVERT_RGB; default возвращает false. **BUFFERSIZE не обработан.** Нет основания рекомендовать `cap.set(CAP_PROP_BUFFERSIZE,1)` для RTSP+FFmpeg как исправление задержки. Установленный другой backend может иметь другое поведение. `read`/`grabFrame` поддерживают decoder state и вызывают FFmpeg read/decode, поэтому цикл «sleep1s, read один кадр» отстаёт от live source, если чтение не продолжается независимо.

Проект smoke test на соответствующей сборке, **не исполнен**:

```python
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG,
    [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000,
     cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000])
```

Это не обещание, что API вернётся ровно через3s в любом native состоянии; внешний watchdog процесса всё ещё полезен. Для демо отдельный reader постоянно забирает frames и перезаписывает latest slot. `grab` не считать бесплатным пропуском H.264 decode: реальная работа зависит от backend.

### PyAV: точные таймауты, PTS и границы контроля

<a id="f034"></a>

## F034 — v16.0.1 `av.open(..., timeout=(open_s,read_s))` использует секунды, float/tuple, и interrupt callback с monotonic clock. Это **не µs FFmpeg…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L105](_WORK/W1_02.md); W1-02-F10.

**F034 — CODE, S032, прочитано.** v16.0.1 `av.open(..., timeout=(open_s,read_s))` использует секунды, float/tuple, и interrupt callback с monotonic clock. Это **не µs FFmpeg AVOption**. `buffer_size` — байты Python I/O, действует при file-like object, не «сколько RTSP кадров копить». В input constructor timeout включается также вокруг `avformat_find_stream_info`; demux заново запускает read timeout перед каждым `av_read_frame`. Следствие: timestamp/age и watchdog — отдельные механизмы; поток, непрерывно выдающий старые кадры, не обязан нарушить read timeout.

<a id="f035"></a>

## F035 — `timeout=(5,3)` не обязательно означает полное wall-clock open≤5s: `avformat_open_input` и find_stream_info имеют отдельные запуски таймера.…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L107](_WORK/W1_02.md); W1-02-F11.

**F035 — INFERENCE на S032.** `timeout=(5,3)` не обязательно означает полное wall-clock open≤5s: `avformat_open_input` и find_stream_info имеют отдельные запуски таймера. Реконнект реализуется владельцем worker, который ловит EOF/error/timeout, закрывает container и создаёт новый. PyAV даёт доступ к Packet/Frame/PTS/time_base и поэтому удобнее raw pipe/OpenCV для непротиворечивого `camera_id,epoch,seq,source_pts,time_base,received_monotonic,decoded_monotonic`. PTS — временная шкала media, не автоматически UTC capture time.

<a id="f036"></a>

## F036 — В v16.0.1 caveats предупреждают о reference cycles и позднем auto-close множества Containers: применять `with av.open(...)`/`Container.close()`…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L109](_WORK/W1_02.md); W1-02-F12.

**F036 — DOC, S032, прочитано.** В v16.0.1 caveats предупреждают о reference cycles и позднем auto-close множества Containers: применять `with av.open(...)`/`Container.close()` при каждом reopen. Поддержка sub-interpreters неполная; C callbacks/логирование могут вызвать lockups. В **этой** версии документ говорит, что logging disabled by default; старые caveats могут описывать другую политику. Не запускать native decoder в произвольном WSGI sub-interpreter и не удерживать все ndarray кадры в истории.

<a id="f037"></a>

## F037 — Утверждение «PyAV совсем не поддерживает hardware decoding» устарело для v16.0.1: HWAccel принимает cuda/qsv/vaapi/d3d11va и др.; поддерживается…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L111](_WORK/W1_02.md); W1-02-F13.

**F037 — CODE, S032, прочитано.** Утверждение «PyAV совсем не поддерживает hardware decoding» устарело для v16.0.1: HWAccel принимает cuda/qsv/vaapi/d3d11va и др.; поддерживается путь AV_CODEC_HW_CONFIG_METHOD_HW_DEVICE_CTX. `allow_software_fallback=True` — default. Поэтому запрос acceleration без проверки не доказывает фактический GPU decode; для эксперимента запретить fallback и логировать используемый stream/codec/hw config. Наличие кода не доказывает совместимость конкретного wheel, драйвера или zero-copy в NumPy. Decode/transfer/resize/цвет измерять отдельно.

Проект Python reader:

```python
# Основание интерфейсов: PyAV v16.0.1 S032; это пример, не выполненный код.
with av.open(url, timeout=(5.0, 3.0),
             options={"rtsp_transport": "tcp"}) as container:
    stream = container.streams.video[0]
    for frame in container.decode(stream):
        # Декодирование продолжается с source FPS.
        # Latest slot/таймстемпы/решение sampling реализует приложение.
        pass
```

### MediaMTX и честная имитация RTSP камер

<a id="f038"></a>

## F038 — Официальный пример v1.21.2 публикует бесконечный MP4 loop как RTSP: `ffmpeg -re -stream_loop -1 -i file.mp4 -c copy -f rtsp…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L128](_WORK/W1_02.md); W1-02-F14.

**F038 — DOC/CODE, S033, прочитано.** Официальный пример v1.21.2 публикует бесконечный MP4 loop как RTSP: `ffmpeg -re -stream_loop -1 -i file.mp4 -c copy -f rtsp rtsp://localhost:8554/mystream`. Это клиент publisher, а не RTSP server внутри FFmpeg. `-re` ограничивает чтение примерно source rate; `-stream_loop -1` зацикливает файл; `-c copy` ремультиплексирует, сохраняя encoded stream. Проверять source codec/profile и timestamp continuity на границе loop. Повтор одинаковых изображений не означает stuck camera. Нужен в демо явный source_type=`looped_file`; это не live industrial camera.

<a id="f039"></a>

## F039 — В config1.21.2 глобальные `rtspTransports` — список разрешённых transports server, per-path `rtspTransport` — транспорт pull от upstream; это…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L130](_WORK/W1_02.md); W1-02-F15.

**F039 — CODE, S033, прочитано.** В config1.21.2 глобальные `rtspTransports` — список разрешённых transports server, per-path `rtspTransport` — транспорт pull от upstream; это разные ключи. Config имеет `runOnInit/runOnInitRestart`; допустим автоматический publisher. Server read/write timeouts default10s, они не определяют срок восстановления worker. Для нескольких потребителей MediaMTX может быть одним upstream connection к камере; actual fanout/limits проверить. Не утверждать, что MediaMTX автоматически транскодирует любой кодек ради браузера.

Рекомендуемый тестовый комплект (**проект**, FFmpeg n8.0 + MediaMTX1.21.2; media commands не запускались):

```yaml
# mediamtx.yml — минимальный fragment к полной конфигурации этой версии
rtspTransports: [tcp]
paths:
  cam1:
    source: publisher
```

```sh
ffmpeg -re -stream_loop -1 -i demo_h264.mp4 -map 0:v:0 -an -c:v copy -rtsp_transport tcp -f rtsp rtsp://127.0.0.1:8554/cam1
```

С TCP-only MediaMTX недостаточно убрать UDP только у reader: publisher тоже должен явно получить `-rtsp_transport tcp`. Для camera pull вместо publisher:

```yaml
paths:
  cam1:
    source: rtsp://CAMERA/PROFILE
    rtspTransport: tcp
```

Учётные данные и реальный URL задавать через секреты/локальную конфигурацию, не сохранять в публикуемые логи. Если исходный файл не подходит по кодеку/профилю, подготовить H.2648-bit yuv420p **один раз** до прогона, а потом loop+copy. Re-encode во время live теста смешивает нагрузку publisher и decoder. Не обещать одинаковую задержку MP4-loop и реальной камеры: у камеры отдельные sensor/encoder/GOP/buffering.

### ONVIF discovery не читает видеопоток

<a id="f040"></a>

## F040 — Discovery основан на WS-Discovery; его результат — device service address, после чего запрашивают capabilities/services. Это control plane.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S034](SOURCES.md#s034). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L159](_WORK/W1_02.md); W1-02-F16.

**F040 — DOC, S034, прочитаны релевантные разделы PDF, не conformance test.** Discovery основан на WS-Discovery; его результат — device service address, после чего запрашивают capabilities/services. Это control plane. Non-discoverable mode допустим; отсутствие ответа discovery не доказывает отсутствие камеры. Для хакатона конфигурация RTSP URL вручную должна работать без discovery. Discovery через обычный интернет/NAT не следует считать гарантированным.

<a id="f041"></a>

## F041 — Media service получает URI выбранного profile (`GetStreamUri`), затем RTSP DESCRIBE/SETUP/PLAY открывают реальное media session; RTP/RTCP несут…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S035](SOURCES.md#s035). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L161](_WORK/W1_02.md); W1-02-F17.

**F041 — DOC, S035, прочитаны §4/5.1.1/5.2.1 и схема.** Media service получает URI выбранного profile (`GetStreamUri`), затем RTSP DESCRIBE/SETUP/PLAY открывают реальное media session; RTP/RTCP несут video/audio/metadata. RTSP control поверх TCP не означает, что RTP media тоже TCP: согласованный media transport может быть UDP. Это объясняет ситуацию «порт554 доступен, ONVIF видит устройство, а кадров нет» — проверять media negotiation, UDP/firewall/маршруты и credentials отдельными тестами. Документ17.12 старый, выбран ради стабильной схемы и не используется как перечень всех возможностей ONVIF2026.

### GOP и что на самом деле экономит sampling

<a id="f042"></a>

## F042 — FFmpeg описывает streamcopy как путь без decode/encode, а фильтры fps/select получают **декодированные frames**. Уменьшение выдачи до5fps после…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S025](SOURCES.md#s025). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L165](_WORK/W1_02.md); W1-02-F18.

**F042 — DOC/CODE, S025, прочитано.** FFmpeg описывает streamcopy как путь без decode/encode, а фильтры fps/select получают **декодированные frames**. Уменьшение выдачи до5fps после decode не означает, что H.26425fps поток стоил как5fps. Межкадровый codec хранит reference state; FFmpeg H.264 skip logic различает non-reference NAL, а не позволяет произвольно пропустить9 из10 compressed packets без последствий. Конкретная экономия skip modes зависит от codec/profile/reference structure. `fps=5` экономит downstream conversion/inference/network, но не весь decoder input.

<a id="f043"></a>

## F043 — Полезны три разных регулятора: (a) camera substream с более низким resolution/FPS — снижает сеть и decode; (b) decoder `skip_frame` с учётом…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S025](SOURCES.md#s025), [S036](SOURCES.md#s036). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L167](_WORK/W1_02.md); W1-02-F19.

**F043 — INFERENCE на S025/S036.** Полезны три разных регулятора: (a) camera substream с более низким resolution/FPS — снижает сеть и decode; (b) decoder `skip_frame` с учётом зависимостей — ограниченный компромисс; (c) sampling **после** decode — ограничивает inference, сохраняя decode continuity. Короткий GOP ускоряет доступ к независимо декодируемой точке после reconnect/loss, но может увеличить bitrate при том же качестве; B frames могут вносить reorder delay. Модель «максимальное ожидание следующей keyframe примерно G/f секунд» применима лишь при регулярных независимо доступных random-access точках с периодом G frames и source f fps; open GOP/I-frame не всегда эквивалент IDR. Это не точная latency guarantee.

<a id="f044"></a>

## F044 — Cookbook демонстрирует `stream.codec_context.skip_frame="NONKEY"`; предлагает использовать frame.pts, а не индекс output. Это даёт keyframe-only,…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S036](SOURCES.md#s036). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L169](_WORK/W1_02.md); W1-02-F20.

**F044 — DOC, S036, прочитано и сверено с новой веткой там, где указано.** Cookbook демонстрирует `stream.codec_context.skip_frame="NONKEY"`; предлагает использовать frame.pts, а не индекс output. Это даёт keyframe-only, а не произвольные5fps. Если GOP50 при25fps и равномерных keyframes, получится около0.5 keyframe/s (арифметика нашего примера), что может пропустить короткое нарушение. FRAME/AUTO threading увеличивает delay между packet input и frame output; SLICE threading работает внутри frame. Упоминание cookbook «примерно5× быстрее на машине автора» **не используется как benchmark**: нет полной аппаратной/медиаконфигурации, к тому же stable9.0.2. Измерять p95 age, а не только максимальный FPS.

### CPU, NVDEC, Quick Sync: что найдено количественно

<a id="f045"></a>

## F045 — Table NVDEC Decoding Performance SDK13.0 даёт indicative **1920×1080, YUV4:2:0**, Windows11, SDK13.0; video clocks2160MHz для Ada: H.264903fps,…

**Тип основания:** CLAIM/MEASURED. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S037](SOURCES.md#s037). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132), [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L173](_WORK/W1_02.md); W1-02-F21.

**F045 — MEASURED_BY_VENDOR + CLAIM, S037, не локально.** Table NVDEC Decoding Performance SDK13.0 даёт indicative **1920×1080, YUV4:2:0**, Windows11, SDK13.0; video clocks2160MHz для Ada: H.264903fps, HEVC1641fps, HEVC Main10 1520fps, AV1 1018fps. Это не benchmark полной видеоаналитики: нет конкретного SKU, bitstream/GOP, bitrate, CPU/driver, host transfer/resize/inference, stream count/latency distribution. Следовательно это полезная калибровка возможностей **архитектуры Ada**, а не обещание30 камер1080p30 на нашей RTX4070. Даже деление903/30=30.1 — только арифметический верхний ориентир по суммарному decode FPS при тех условиях, непригодный для SLA. NVIDIA указывает ограничение доступной памятью и производительностью; несколько decode contexts поддержаны. Число NVDEC engines может различаться между SKU, нельзя умножать табличный FPS на выдуманное количество.

**Происхождение:** [_WORK/W1_06.md:L41](_WORK/W1_06.md); W1-06-F02.

MEASURED/CLAIM: повторное чтение той же NVDEC13.0 primary таблицы, не независимое измерение. Дополнение к F045: показатели на один NVDEC engine, зависят от GPU class/video clock; floor(903/25)=36 — только арифметика, не доказанный лимит камер. RTX4070 VRAM, actual clocks/driver/contexts/copies/CPU остаются UNKNOWN.

<a id="f046"></a>

## F046 — В **decode** таблице GeForce RTX4070 (Desktop) и RTX4070 Laptop перечислены Ada/5thGen, total NVDEC1. Для обычного H.2644:2:0 8bit и HEVC…

**Тип основания:** CLAIM/DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S038](SOURCES.md#s038). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L175](_WORK/W1_02.md); W1-02-F22.

**F046 — DOC/CLAIM, S038, прочитано.** В **decode** таблице GeForce RTX4070 (Desktop) и RTX4070 Laptop перечислены Ada/5thGen, total NVDEC1. Для обычного H.2644:2:0 8bit и HEVC Main/Main10 поддержка есть; H.26410bit/4:2:2 не следует считать поддержанными по имени H.264. Таблица capability не говорит установленный VRAM. Нужно установить фактический SKU/driver/capabilities `nvidia-smi`, `ffmpeg -hwaccels`, `ffprobe` и пробным decode; драйверу/сборке требуется совместимость. NVENC concurrent-session limit из соседней **encode** таблицы не использовать как лимит NVDEC streams.

<a id="f047"></a>

## F047 — NVIDIA guide рекомендует `-hwaccel cuda -hwaccel_output_format cuda` для удержания frames на GPU; `scale_cuda`/`scale_npp` позволяют resize без…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S039](SOURCES.md#s039). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L177](_WORK/W1_02.md); W1-02-F23.

**F047 — DOC, S039, прочитано.** NVIDIA guide рекомендует `-hwaccel cuda -hwaccel_output_format cuda` для удержания frames на GPU; `scale_cuda`/`scale_npp` позволяют resize без CPU download. Для сборки нужны nvcodec headers, minimum driver зависит от SDK; CUDA toolkit требуется для описанной сборки, но не для запуска готового binary. Это не означает, что любой pip OpenCV wheel использует CUDA. Путь decode→GPU-resize→download маленького image может снизить transfer; путь decode→download1080p→CPU BGR→resize добавляет копии. В данной системе итог передаётся LinQ, поэтому «zero-copy на RTX» заканчивается на границе передачи/CPU API; не называть всю систему zero-copy.

<a id="f048"></a>

## F048 — Intel VPL — dispatcher/API для hardware decode/encode/processing; требуется отдельно runtime implementation. Intel перечисляет VPL GPU Runtime для…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S040](SOURCES.md#s040). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L179](_WORK/W1_02.md); W1-02-F24.

**F048 — DOC/CODE, S040, прочитано.** Intel VPL — dispatcher/API для hardware decode/encode/processing; требуется отдельно runtime implementation. Intel перечисляет VPL GPU Runtime для IrisXe/newer и MediaSDK для legacy; таблица выбора зависит от поколения/OS/backend. Наличие Intel CPU само по себе не подтверждает доступный и включённый iGPU/QuickSync. Для ноутбука сначала инвентаризировать GPU, драйвер, Linux `/dev/dri` либо Windows API, codec profiles и поставку FFmpeg с qsv. `libvpl` на неизвестном LinQ host не предполагается.

<a id="f049"></a>

## F049 — Переносимое число «720p/1080p H.264/H.265 потоков на CPU-core» и decode-only QuickSync benchmark с полной конфигурацией для нашего неизвестного…

**Тип основания:** UNKNOWN. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S041](SOURCES.md#s041), [S042](SOURCES.md#s042). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L181](_WORK/W1_02.md); W1-02-F25.

**F049 — UNKNOWN после поиска + отрицательные результаты.** Переносимое число «720p/1080p H.264/H.265 потоков на CPU-core» и decode-only QuickSync benchmark с полной конфигурацией для нашего неизвестного CPU **не установлены**. Искались official Intel sample_decode/oneVPL, FFmpeg benchmark decode и primary practitioner results. QuickSync Benchmarks авторов ironicbadger/cptmorgan показывает много чисел и CPU моделей, но About прямо определяет `h264_1080p_cpu` как CPU **encode**, а h264/hevc tests — hardware encode/transcode. Нельзя использовать его244fps i5-12400 как decode-only. Smelter приводит g4dn.xlarge4vCPU/T4 и g4dn.2xlarge8vCPU/T4, 720p24/1080p30 CPU/GPU stream count; это pipeline **decode+encode+composition**, а не per-core decode, без зафиксированной версии/bitstream здесь. Эти источники полезны для программы теста, их числа не используются в сайзинге. Не найденное число — не доказательство невозможности QuickSync; пробел закрывается локальным benchmark E003.

### Противоречия, эксплуатационные ловушки и статус доказательств

<a id="f050"></a>

## F050 — Issue#28638 открыт10марта2026: macOS Darwin25.2.0, OpenCV4.8.0+, Python3.9+, CAP_FFMPEG; автор сообщает silent corrupted frames спустя15–30s при…

**Тип основания:** CLAIM. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S043](SOURCES.md#s043). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L185](_WORK/W1_02.md); W1-02-F26.

**F050 — CLAIM пользователя issue / maintainer hypothesis, S043.** Issue#28638 открыт10марта2026: macOS Darwin25.2.0, OpenCV4.8.0+, Python3.9+, CAP_FFMPEG; автор сообщает silent corrupted frames спустя15–30s при MediaMTX-loop и медленном чтении, `read` возвращаетTrue. `BUFFERSIZE` вернулFalse. Contributor12марта просит сопоставимый FFmpeg тест и предполагает saturation buffer, если consumer не успевает. Это **не установленный bug всех версий и не наше воспроизведение**. Но это конкретный контрпример подходу «ret=True достаточно» и основание тестировать непрерывность, frame age/decoder errors и memory, а не периодически reopen без диагностики.

<a id="f051"></a>

## F051 — PyAV#584 от2019 описывает hanging open при камере с лимитом3clients и четвёртом соединении без media; PyAV7dev, Ubuntu18.04, libavformat57.83.100.…

**Тип основания:** CLAIM/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S044](SOURCES.md#s044), [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L187](_WORK/W1_02.md); W1-02-F27.

**F051 — исторический CLAIM/CODE trace, S044+S032.** PyAV#584 от2019 описывает hanging open при камере с лимитом3clients и четвёртом соединении без media; PyAV7dev, Ubuntu18.04, libavformat57.83.100. Закрыт через#589. В v16.0.1 InputContainer timeout вокруг find_stream_info действительно присутствует. Нельзя повторять историческое «timeout PyAV сломан» как актуальную характеристику; сохраним конкретный failure injection — RTSP control отвечает, media не приходит. MediaMTX fanout может снизить число обращений к реальной камере, но лимит upstream отдельно проверить.

<a id="f052"></a>

## F052 — Для отдельного camera worker использовать состояния CONNECTING→STREAMING→STALE/ERROR→BACKOFF→CONNECTING. Таймер отсутствия **нового decoded…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L189](_WORK/W1_02.md); W1-02-F28.

**F052 — INFERENCE / проект восстановления.** Для отдельного camera worker использовать состояния CONNECTING→STREAMING→STALE/ERROR→BACKOFF→CONNECTING. Таймер отсутствия **нового decoded frame** отличается от network read timeout; дополнительно считать age выбранного кадра и никогда молча отправлять бесконечно прошлый frame. После error закрыть native container/pipeline; parent watchdog завершает зависший worker и перезапускает процесс. Backoff например0.5,1,2,4…до10s с jitter — проектные числа, не найденные оптимумы. Ошибку credentials/unsupported codec показывать как configuration error, не бесконечно маскировать reconnect. После восстановления увеличить `stream_epoch`, сбросить decoder state/latest-slot, уведомить tracker о gap; не склеивать одинаковые PTS из разных соединений/loops. PTS reset допустим, поэтому идентификатор кадра `(camera_id,epoch,seq)` надёжнее одного PTS.

Сохранять метрики по каждому stream: input/decode/selected FPS; last_frame_age_seconds; source PTS interval и reset count; reconnect count/reason; queue depth/drop count; worker RSS; CPU; для GPU decode utilization/memory/video clock. Отдельно source wallclock если он достоверно есть. Age=`now_monotonic−received_monotonic` — измеряет возраст **с момента приёма**, не sensor-to-alert latency. Использовать watermark/визуальные часы E002, чтобы обнаружить уже старые кадры на ingress.

<a id="f212"></a>

## F212 — Адресные передачи

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L240](_WORK/W1_02.md); дополнительная тематическая выписка.

## Адресные передачи

- **linq_platform / V01:** Q003, F045, F046, F047, F048. Не приписывать LinQ NVDEC/QuickSync/RK3588 video capabilities на основании нашей4070. Запросить разрешение пакетов/RTSP ingress и наличие decode API, затем отдельно измерить.
- **V04 transfer:** F042, F043, F044/F047. Sampling после decode экономит WAN/inference; GPU resize до download может экономить local transfer. Для cost model нужны actual source FPS decode и выбранный FPS inference, это разные числа.
- **V05 scheduler / V07 tracking:** F035/F052. Latest-slot требует `camera_id,epoch,seq,pts,time_base,received/decoded_monotonic`; gap/discontinuity после reconnect, результаты старого epoch отбрасывать. Decoder не должен ждать remote inference.
- **V09 clips / V10 display:** F038/F043. Сохранять encoded branch без повторного decode и не забыть GOP random access; loop files — явно simulated sources. MediaMTX — fanout и protocol bridge, не универсальный transcoder.
- **evaluation / violation_methods:** F043/F044/E004. Keyframe-only легко оказывается0.5fps приGOP50/25fps; произвольное sampling может пропустить краткий акт. Метрики возраста от receive не равны sensor-to-alert; видимые часы/trace нужны отдельно.
- **market_deployment / V14 sizing:** F045/F049/E003. NVDEC903fps — vendor indicative Ada1080p; CPU/QuickSync portable per-core число не получено. Не строить500-camera budget на encode FPS.
- **hackathon_strategy:** F038/E002. Демо с file→RTSP loop воспроизводимо, но должно быть подписано. Для доказательства live ingress показать recovery и freshness; это независимо от подтверждения inference LinQ.

<a id="f213"></a>

## F213 — Границы и незавершённые сетевые зацепки

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S132](SOURCES.md#s132). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_02.md:L250](_WORK/W1_02.md); дополнительная тематическая выписка.

## Границы и незавершённые сетевые зацепки

Главные вопросы ingress/decode получили ответ либо локализованный пробел. Не исследовались GStreamer zero-copy на конкретной AstraLinux и RK3588 MPP/LinQHX: аппаратная конфигурация стенда неизвестна, риск бесполезного переноса. Intel corporate oneVPL URL дал500/404 redirect через web; README Intel libvpl получен напрямую, поэтому зависимость runtime проверена, но производительность не установлена. API GitHub commit resolution для FFmpeg/PyAV дал403 rate-limit; материалы закреплены tag и сохранены, hash не выдуман. Прочитаны relevant sections первичных спецификаций/документов и функции исходников; документы не исполнялись и не проходили conformance testing.

# 03 Payload, JPEG quality, transport и bandwidth

<a id="f063"></a>

## F063 — JPEG особенно опасен для tiny/small; thermal study [MEASURED publication, S055]

**Тип основания:** MEASURED. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S055](SOURCES.md#s055). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L75](_WORK/W1_03.md); W1-03-F11.

### F063 — JPEG особенно опасен для tiny/small; thermal study [MEASURED publication, S055]

Авторы проверяли Cascade R-CNN, FSAF, Deformable DETR (ResNet-50) на FLIR thermal 640×512, train/test 7859/1360, классы Person/Bicycle/Car; качества 95/75/50/15/10/5. Tiny: площадь ≤20² px, small ≤32² px (tiny включён в small, не взаимно исключающие bins). Table 6: Cascade R-CNN, обучение original, тест Q95/Q50/Q15/Q5: mAP 0.822/0.789/0.623/0.109; original baseline 0.823. При retraining Q5 результат 0.613. Метрика здесь описана авторами как IoU>0.5, её нельзя выдавать за COCO mAP50:95. §5.3 сообщает большую чувствительность tiny/small. Thermal дорожные объекты и указанные архитектуры не устанавливают допустимый JPEG quality для RGB каски/респиратора/сигареты.

<a id="f064"></a>

## F064 — независимый RGB study: precision может скрывать рост пропусков [MEASURED publication, S056]

**Тип основания:** MEASURED. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S056](SOURCES.md#s056). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L79](_WORK/W1_03.md); W1-03-F12.

### F064 — независимый RGB study: precision может скрывать рост пропусков [MEASURED publication, S056]

Исследование COCO val2017: 5000 images, 9 Detectron2 RetinaNet/Faster R-CNN вариантов, ImageMagick JPEG Q=1..100, без spatial transforms; исходные изображения уже JPEG (Q96/Q90/Q80), поэтому это recompression. При Tc=0.5 precision оставалась относительно стабильной, ухудшение связано преимущественно с recall; AP small падает быстрее medium/large. В §3.3.4 производная AP ускоряет спад ниже около Q40, в заключении recall — ниже около Q30: это разные метрики, не противоречивые универсальные пороги. Q100 также не lossless. Авторы дают код и raw detections, но нами они не запускались. Человеческая визуальная приемлемость JPEG и неизменная precision не доказывают сохранение recall мелких СИЗ.

<a id="f067"></a>

## F067 — base64 не бесплатен [DOC, S059; INFERENCE arithmetic]

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S059](SOURCES.md#s059). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L91](_WORK/W1_03.md); W1-03-F15.

### F067 — base64 не бесплатен [DOC, S059; INFERENCE arithmetic]

RFC4648 §4 отображает 3 input bytes в 4 символа. Для n байт обычный padded base64 занимает `4*ceil(n/3)` ASCII bytes без JSON-обёртки, то есть около +33.3% при большом n. Binary HTTP/gRPC/WebSocket не нуждаются в этой надбавке. Это не означает, что любой endpoint принимает бинарный payload: надо выполнить его контракт.

<a id="f068"></a>

## F068 — расчёты передачи, явно наш вывод [INFERENCE]

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L95](_WORK/W1_03.md); W1-03-F16.

## F068 — расчёты передачи, явно наш вывод [INFERENCE]

Пусть N — камер; f — отобранных кадров/с на камеру; W,H — px; k — каналов; d — bytes/channel; J — фактический средний encoded size bytes/frame; h — metadata+transport bytes/request. Полезный uplink без запаса:

`R_raw = 8*N*f*W*H*k*d` bit/s; `R_JPEG = 8*N*f*(E[J]+h)` bit/s. Считать E[J] по реальным кадрам; p95(J) и burst важны для очереди и памяти. JPEG Q не является compression ratio. Дополнительный TLS/TCP/IP overhead, retransmits и конкурирующий трафик учитывать по измерениям. Если измеренный полезный goodput B bit/s, условие устойчивости `R_payload < B`; равенство оставляет нулевой запас на вариацию.

Примеры арифметики, **не измерение**: RGB uint8 1920×1080 = 6,220,800 bytes/frame; 5 fps = 248.832 Mbit/s/camera. NV12 8-bit nominal 1.5 bytes/pixel = 124.416 Mbit/s при 5 fps (если формат поддержан). Tensor FP32 RGB 640×640 = 4,915,200 bytes/frame и 196.608 Mbit/s при 5 fps; uint8 того же размера — 49.152 Mbit/s. Перенос нормализации FP32 на клиента может увеличить канал в 4 раза относительно uint8, несмотря на меньший spatial size.

Иллюстрация JPEG: **допущение** J=150,000 bytes/frame, 5 fps, без h: 6 Mbit/s/camera; 50 камер — 300 Mbit/s, 500 — 3 Gbit/s. При J=50,000 bytes это 2/100/1000 Mbit/s соответственно. Ни размер, ни качество такой картинки не установлены. При B=20 Mbit/s сериализация одного кадра 150 kB требует минимум `8*150000/20000000 = 60 ms`, raw 1080p RGB — 2.48832 s; RTT добавляется отдельно. Ускоритель не может отменить это время передачи.

Для ROI-кропов с r regions/frame и размерами encoded J_j: `R_ROI = 8*N*f*E[sum_j(J_j+h_j)] + R_discovery`. Если crop raw: заменить J_j на w_j*h_j*k*d. `R_discovery` — периодические полные кадры или first-stage detector, без которого неизвестно, где вырезать ROI. Crop-area fraction не равен JPEG-size fraction; overlapping crops могут дублировать пиксели, r может резко вырасти в толпе. Если каждый crop resize-ится в один и тот же модельный input, меньший сетевой payload не означает меньше accelerator work. Нужны ROI coordinates, scale/letterbox transform, parent frame_id и track_id; crop классификация относится к исходному времени родительского кадра.

Для H.264/H.265 передаётся encoded stream: `R_video≈N*b` при измеренном bitrate b bit/s; это потенциально экономнее независимых JPEG за счёт межкадрового кодирования. Но серверу нужны demux/decode и корректное восстановление reference frames. Это другой input contract, который может быть невозможен у API, принимающего только tensors. WebP/QUIC/ZeroMQ не исследованы до рекомендации: отсутствие измерений CPU, совместимости endpoint и требования замены транспорта не оправдывает расширение протокольного стека в 45 часов.

<a id="f147"></a>

## F147 — Обязательный output contract включает tensor names/count, per-batch/per-frame shapes, dtype/layout/endian, quantization scale/zero-point,…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L119](_WORK/W2_01.md); W2-01-F14.

**F147 [INFERENCE, F141/F142 + F068].** Обязательный output contract включает tensor names/count, per-batch/per-frame shapes, dtype/layout/endian, quantization scale/zero-point, decode-head semantics (logits/objectness/class scores/box encoding), batch/frame/crop correlation, coordinate space и inverse letterbox/ROI transform. Для compact detections нужны class mapping/version, box format, confidence definition, threshold/top-K, class-aware/agnostic NMS, IoU threshold, max detections, truncation flag, postprocess implementation/config revision. NMS может отсутствовать в end-to-end detector — не добавлять его дважды по привычке. Masks/keypoints/embeddings — отдельные размеры, а не «маленькие metadata».

| Actual output / access | Где decode-head/filter/NMS | Последствия и проверка |
|---|---|---|
| API отдаёт только raw heads, свой код на remote нельзя | На клиенте после binary download/dequantize | Downlink, CPU и RAM могут доминировать. Проверить все heads, scales и reference parity; cap result bytes до выделения памяти. Новый dtype без согласования запрещён |
| Разрешён свой remote wrapper + есть host CPU/runtime | Рядом с inference; вернуть compact boxes | Кандидат45ч: меньше WAN; серверные CPU/queue/permissions unknown. Принятый inference evidence отдельно от CPU postprocess. Golden comparison обоих placement при одинаковых thresholds |
| API уже возвращает boxes | По подтверждённому server contract | Не делать повторный NMS без причины. Проверить server truncation/coordinates/class mapping; если меняются thresholds, это смена config revision |
| API возвращает только events | Правила/tracking уже внутри сервиса | Не предполагать доступность per-frame detections/своего temporal state. Может не покрыть необходимые классы/клипы/processed view; route условный |

Ни одно placement не установлено для LinQ. Перенос NMS на клиент может упростить интеграцию, но требует сначала посчитать response size, затем проверить полезный FPS/age и качество. Перенос на remote без изменения NN может быть допустимым инженерно, но accepted обязательная NN-граница определяется выдачей/кейсом, не этим аналогом.

### Формулы, polling и memory bounds

<a id="f148"></a>

## F148 — Для уникальных completed frames rate `N*f`, raw tensor bytes/frame `O = Σ_t product(shape_t_per_frame)*bytes(dtype_t)`; при batch не умножать…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L132](_WORK/W2_01.md); W2-01-F15.

**F148 [INFERENCE].** Для уникальных completed frames rate `N*f`, raw tensor bytes/frame `O = Σ_t product(shape_t_per_frame)*bytes(dtype_t)`; при batch не умножать batch dimension дважды. Binary request response metadata `h_out` и wire overhead считать отдельно. Для переменного output считать **измеренное** `E[O]`, p95/p99/max и burst, а не только fixed average.

`R_return = 8*N*f*E[output_bytes]` bit/s — именно remote→client inference data. Для raw binary `output_bytes≈O+h_out`; JSON/base64 брать фактический wire size (base64 как F067 добавляет около 1/3 к binary, JSON numeric arrays имеют другую надбавку). Retries/download repeats увеличивают фактический rate; f здесь не camera source FPS и не число повторных completions.

Для J наблюдаемых jobs, каждого с poll interval Δ и server-supported batch query до b IDs: грубая upper planning rate `q_poll≈ceil(J/b)/Δ` calls/s при полном обходе; exact variable scheduling считать суммой реальных poll rates. Status-response bytes зависят от количества jobs/attempts/fields. Добавить `R_status_down=8*q_poll*E[status_response_bytes]`, `R_status_up=8*q_poll*E[status_request_bytes]`, submit ack, cancel/control, result locator requests и фактические result downloads. Если status endpoint повторяет полный output, каждый такой poll заново вносит O: нельзя считать «poll metadata мало». Callback/webhook вместо polling требует authenticated delivery/dedup/reconcile и не отменяет ledger.

При идеальном periodic polling обнаружение уже завершённого job ждёт ещё [0,Δ), среднее Δ/2 **только** при равномерной независимой фазе; quota/backoff/outage разрушают bound. Δ относится ко времени результата клиента, не accelerator compute. Успешный poll latency не доказывает terminal visibility delay. Использовать status-only response по доступному контракту; fetch successful artifact один раз с bounded retry/dedup/hash. Дефицит result fetch capacity должен создавать bounded spool/drop/unavailable outcome, не бесконечные completed tensors.

Client postprocess требование: `N*f*E[cpu_seconds_post/frame] < available_post_cpu_seconds/s` с измеренными concurrency/copy costs. RAM: `M_output >= K_fetch*O_max + K_post*O_max + compact_results + decoder/copy overhead` — считать реальное владение буферами, переиспользуемые ссылки не суммировать дважды. NMS top-K/output cap ограничивает память, но меняет recall; выбирать совместно с evaluation. Лимиты payload/result bytes, parse timeout и tensor shape validation нужны до trust внешнему size; truncated output явно маркировать.

### Один условный shape/dtype пример — арифметика, НЕ модель LinQ

<a id="f149"></a>

## F149 — Допустим один raw head `[1,84,8400]` FP32, batch1, 84 условно = 4 box components + 80 class scores. Это **не утверждение о выбранной модели**, не…

**Тип основания:** LOCAL/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S137](SOURCES.md#s137). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_01.md:L144](_WORK/W2_01.md); W2-01-F16.

**F149 [INFERENCE/LOCAL arithmetic].** Допустим один raw head `[1,84,8400]` FP32, batch1, 84 условно = 4 box components + 80 class scores. Это **не утверждение о выбранной модели**, не import из LinQ и не стандарт для любого detector. Binary body `1*84*8400*4=2,822,400 B/frame`. FP16 при **поддержанном** другом контракте дал бы 1,411,200 B; произвольный client cast меняет численность/качество, его не считаем разрешённым.

Альтернатива после postprocess: максимум100 detections, каждая 4×FP32 координаты + FP32 score + INT32 class =24 B; fixed packed records `[M,24 bytes]`, M≤100, плюс count INT32=4B: при M=100 это2404 B/frame. Это проектный binary формат **до** envelope/HTTP/TLS; не JSON объекты и не masks. Объявленные class count/max detections — допущения примера, не требования кейса.

| Только return tensor/packed payload, analysis5 FPS | 1 камера | 50 камер | 500 камер |
|---|---:|---:|---:|
| Raw head FP32 2,822,400B |112.896 Mb/s|5.6448 Gb/s|56.448 Gb/s|
| Compact M=100,2404B |0.09616 Mb/s|4.808 Mb/s|48.08 Mb/s|

Арифметика проверена небольшим локальным Python-расчётом; результаты сохранены в [ARITHMETIC.json](_WORK/MATERIALS/W2_01/ARITHMETIC.json). Это не benchmark. SI decimal units. Отношение payload ≈1174.04× здесь обусловлено допущениями raw/compact, не универсальная compression ratio. Если input JPEG условно100kB из W1-06, raw return в этом примере в 28.224 раза больше input payload. При local→remote JPEG варианте uplink input и downlink output — разные направления; их нельзя выдать за одно симметричное требование. При remote decode эти tensors могут остаться в LAN/host и через WAN идут только compact metadata. Viewer fanout отдельно добавляет browser egress — это часть W2-F, не замена R_return.

Условный polling пример: J=50 известных jobs, Δ=0.5s, b=1 →100 polls/s; request1kB и status response2kB →0.8Mb/s вверх и1.6Mb/s вниз. Это допущения bytes/interval, не AWS/LinQ measured quota. При b=100 и таком контракте число calls меньше, но response на50jobs крупнее; нельзя делить traffic ровно на100. У poll interval0.5s идеальная дополнительная средняя задержка250ms, край <500ms только при указанных идеальных условиях. Не назначать этот Δ как готовый режим стенда.

# 04 Scheduler, bounded work, state и temporal contract

<a id="f053"></a>

## F053 — HTTP может передавать тензоры без JSON-массива чисел [DOC, S045]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S045](SOURCES.md#s045). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L35](_WORK/W1_03.md); W1-03-F01.

### F053 — HTTP может передавать тензоры без JSON-массива чисел [DOC, S045]

Triton binary extension кладёт JSON metadata перед бинарными тензорами в теле HTTP; порядок бинарных блоков соответствует metadata. Тензор — little-endian, row-major, без stride/padding; BYTES element содержит 4-байтовую длину и затем данные. `binary_data_size` — размер тензора в байтах, `Inference-Header-Content-Length` — длина JSON, `Content-Length` — всего тела. Поддержка объявляется в Server Metadata как `binary_tensor_data`. Raw binary request имеет дополнительные ограничения: единственный input и выводимая форма; для BYTES требуется shape [1]. Это свойство Triton, не универсальная возможность HTTP API. Бинарные JPEG bytes не становятся автоматически входом детектора: серверу нужен decoder/preprocessor или модель с соответствующим контрактом.

<a id="f054"></a>

## F054 — batch delay не ограничивает весь путь [DOC, S046]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S046](SOURCES.md#s046). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L39](_WORK/W1_03.md); W1-03-F02.

### F054 — batch delay не ограничивает весь путь [DOC, S046]

В Triton dynamic batcher предназначен для stateless models и конфигурируется по модели. Default batching не добавляет ожидание ради заполнения. `max_queue_delay_microseconds` задаёт ожидание формирования полного/preferred batch; по истечении отправляется неполный batch. `max_queue_size` и `default_timeout_microseconds`/`timeout_action` относятся к политике очереди. `preserve_ordering` управляет порядком ответов. Приоритеты внутри model queue не равны справедливости между камерами. Sequence batcher нужен stateful-модели с привязкой запросов последовательности к одному model instance и управляющими start/end/correlation ID. Документация рекомендует сначала измерять default batching; `preferred_batch_size` большинству моделей задавать не рекомендует. Образец не доказывает, что LinQ принимает произвольный batch size.

<a id="f055"></a>

## F055 — async и streaming имеют разные свойства [DOC, S047]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S047](SOURCES.md#s047). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L43](_WORK/W1_03.md); W1-03-F03.

### F055 — async и streaming имеют разные свойства [DOC, S047]

gRPC рекомендует переиспользовать channels/stubs. Лимит concurrent HTTP/2 streams может создавать невидимую приложению клиентскую очередь. Long-lived stream после открытия не балансируется между серверами; streaming усложняет recovery. В Python sync streaming создаёт дополнительные потоки получения/отправки и описан как более медленный относительно unary; asyncio может помочь. Поэтому нельзя объявить «gRPC streaming всегда быстрее HTTP». Документация не даёт сравнительных FPS для нашего payload, языка, RTT или LinQ.

<a id="f056"></a>

## F056 — gRPC сам не назначает deadline [DOC, S048]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S048](SOURCES.md#s048). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L47](_WORK/W1_03.md); W1-03-F04.

### F056 — gRPC сам не назначает deadline [DOC, S048]

По умолчанию клиент может ждать ответ без срока. Deadline нужно задавать явно и проверять нагрузочным тестом. При превышении клиентского срока сервер может уже исполнять работу; серверный код должен прекращать запущенные им операции, когда запрос отменён. При передаче deadline дальше elapsed time вычитается из оставшегося timeout, что помогает при различии часов. Это не замена timestamp кадра.

<a id="f057"></a>

## F057 — транспортный flow control не является freshness policy [DOC, S049; INFERENCE]

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S049](SOURCES.md#s049). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L51](_WORK/W1_03.md); W1-03-F05.

### F057 — транспортный flow control не является freshness policy [DOC, S049; INFERENCE]

gRPC flow control применим к streaming RPC. Возврат из write означает передачу сообщения framework, а не подтверждённую отправку по сети. Framework может буферизовать или блокировать запись. Наш вывод: нужен отдельный предел app-level outstanding/bytes и age check; иначе свежие кадры останутся за старыми в транспортной очереди даже при идеально ограниченной camera queue.

<a id="f058"></a>

## F058 — готовые клиенты существуют, но cancellation version-sensitive [DOC, S050]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S050](SOURCES.md#s050). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L55](_WORK/W1_03.md); W1-03-F06.

### F058 — готовые клиенты существуют, но cancellation version-sensitive [DOC, S050]

Triton Python HTTP/gRPC clients предоставляют AsyncIO, обозначенный в прочитанной странице Beta. Python gRPC cancellation inflight запросов документирован с r23.10; можно отменить AsyncIO task `infer()`, streaming iterator либо все запросы при stop_stream. Это API клиента и не доказательство мгновенного прекращения kernel на accelerator. Версии клиента и сервера надо фиксировать вместе; текущая документация содержит более поздние изменения API, поэтому копирование примера без pin опасно.

<a id="f059"></a>

## F059 — WebSocket даёт framing, остальные гарантии проектирует приложение [DOC, S051; INFERENCE]

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S051](SOURCES.md#s051). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L59](_WORK/W1_03.md); W1-03-F07.

### F059 — WebSocket даёт framing, остальные гарантии проектирует приложение [DOC, S051; INFERENCE]

RFC определяет двусторонний TCP protocol с handshake и text/binary messages; клиентские frames маскируются. WebSocket не задаёт model schema, per-frame correlation, freshness deadline, admission, retry idempotency и camera fairness. Эти поля и восстановление нужно строить в своём application protocol. Один ordered TCP stream не устраняет head-of-line задержку потерянных TCP bytes. Это подходящий вариант, когда он уже предоставлен стендом либо нужен собственный bidirectional gateway; технического основания делать его обязательным нет.

<a id="f060"></a>

## F060 — source-aware batch полезнее общего FIFO [DOC, S052]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S052](SOURCES.md#s052). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L63](_WORK/W1_03.md); W1-03-F08.

### F060 — source-aware batch полезнее общего FIFO [DOC, S052]

DeepStream nvstreammux формирует batch до заполнения либо timeout, отсчитываемого с первого buffer. По умолчанию сбор round-robin; metadata сохраняет source ID, исходное разрешение и PTS. `max-same-source-frames` ограничивает долю одного источника. В текущей версии часть per-source priority/fps ключей deprecated. Применять параметры старого и нового muxer как взаимозаменяемые нельзя. Прочитанный 9.2 — фактическая версия страницы при доступе, а не утверждение, что такая версия стоит у команды. Образец даёт принцип «не ждать вечно исчезнувшую камеру», не библиотеку для LinQ.

<a id="f061"></a>

## F061 — SDK NPU тоже разделяет threshold/timeout/priority [CODE: docstrings и Python wrappers прочитаны, S053]

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S053](SOURCES.md#s053). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L67](_WORK/W1_03.md); W1-03-F09.

### F061 — SDK NPU тоже разделяет threshold/timeout/priority [CODE: docstrings и Python wrappers прочитаны, S053]

В HailoRT v4.20.0 `set_scheduler_threshold` задаёт число send requests до готовности network; timeout может сделать готовой сеть с хотя бы одним запросом без достижения threshold. `set_scheduler_priority`: большее число — более высокий приоритет, что отличается от ряда других API. `ConfiguredInferModel` имеет `get_async_queue_size`, `wait_for_async_ready`, `run_async`; комментарии требуют сохранять буферы до окончания работы и callback. Здесь проверено только наличие Python wrappers/docstrings, не реальное поведение железа, fairness или обещанный upper bound под перегрузкой. Никакие эти методы не приписываются LinQ.

<a id="f062"></a>

## F062 — latest-frame policy уже встречается в production-oriented коде, но есть ловушка барьера [CODE, S054]

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S054](SOURCES.md#s054), [S066](SOURCES.md#s066). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133), [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L71](_WORK/W1_03.md); W1-03-F10.

### F062 — latest-frame policy уже встречается в production-oriented коде, но есть ловушка барьера [CODE, S054]

В LoadStreams.update при `buffer=False` список камеры заменяется на `[im]`; при чтении берётся последний кадр, остальные очищаются. При `buffer=True` используется FIFO с буфером до 30 изображений. При этом __next__ последовательно ожидает наличия кадра у каждой камеры: замерший источник может задержать batch других. Из этого не следует копировать загрузчик: полезна именно политика последнего кадра, тогда как общий барьер надо исключить для живой многокамерной системы. AGPL-3.0 — дополнительная причина брать принцип, а вопрос заимствования кода решать отдельно.

**Происхождение:** [_WORK/W1_04.md:L118](_WORK/W1_04.md); W1-04-F12.

CODE: тот же latest-frame/barrier pattern, что F062, дополнительно прочитан в HEAD e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 (S066). Unique observations: retrieve failure выдаёт zero image и cap.open; умерший thread приводит к StopIteration/закрытию loader. Return sources/images/info не содержит PTS/epoch. Это два snapshots одной implementation chain, не LinQ runtime.

<a id="f065"></a>

## F065 — cross-model admission является отдельной задачей [DOC, S057]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S057](SOURCES.md#s057). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L83](_WORK/W1_03.md); W1-03-F13.

### F065 — cross-model admission является отдельной задачей [DOC, S057]

Triton rate limiter работает поперёк загруженных моделей. Без него доступный model instance может начать исполнение сразу; одновременные модели иногда превышают memory budget. Лимитер задаёт ресурсы/count per device или global и откладывает исполнение instances, учитывая priorities. Это не аналог ограничения requests/sec для каждой камеры. Нашему scheduler всё равно нужны camera quotas и предел fan-out каскада. Совместимость механизма с LinQ неизвестна.

<a id="f066"></a>

## F066 — каскад может накапливать промежуточные задачи [DOC, S058]

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S058](SOURCES.md#s058). **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L87](_WORK/W1_03.md); W1-03-F14.

### F066 — каскад может накапливать промежуточные задачи [DOC, S058]

В current Triton Ensemble docs описан `max_inflight_requests` для каждого шага; лимит общий для активных requests ensemble, default 0 — без ограничения. При достижении порога новый шаг ждёт downstream capacity. Документация прямо описывает риск memory growth, если upstream быстрее downstream; ограничение не отменяет и не timeout-ит intermediate requests, а end-to-end latency может вырасти. Версия появления не установлена, переносить параметр в старый Triton нельзя. Для собственного person→PPE cascade нужен такой же ограниченный fan-out/admission, независимо от выбранного backend.

<a id="f069"></a>

## F069 — RTT, concurrency и batch fill [INFERENCE, проверяемая модель]

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L109](_WORK/W1_03.md); W1-03-F17.

## F069 — RTT, concurrency и batch fill [INFERENCE, проверяемая модель]

Обозначения: λ — требуемая нагрузка requests/s; L — среднее время от отправки до завершения request (s), включая сеть, серверные queue/compute и ответ; C — число concurrent outstanding requests. Little-like steady-state соотношение `C≈λ*L`, поэтому необходимая нижняя оценка по одной сети `C≥λ*RTT` (RTT в s). При заданном лимите C возможная rate не выше примерно `C/L`. Это планировочная оценка, не гарантия p99 и не замена измерению. При batching B кадров/request λ_requests=λ_frames/B, но L включает batch fill и batch compute; bytes не исчезают.

Пример: 10 камер×5 fps=50 frame requests/s; RTT=0.1 s → не меньше 5 in-flight только для заполнения сетевого пути. Если measured end-to-end L=0.16 s → среднее outstanding 8. Один sequential request даёт не более 6.25 fps при L=160 ms. Увеличение C сверх bottleneck service capacity увеличивает очередь, а не throughput. Нужны отдельные пределы request count и bytes; 8 raw FP32 кадров — уже около 39 MB payload без копий.

Для детерминированного потока совместимых запросов rate λ и batch B максимальное ожидание первого элемента до заполнения `(B-1)/λ` s, среднее приблизительно `(B-1)/(2λ)`. Для Poisson это ожидаемое fill time, без жёсткой верхней границы. Например, один источник 5 fps и B=8: первый ждёт до 1.4 s в равномерной модели. Объединение камер одной модели даёт большую λ, но не должно ждать выключенный источник. Отправлять partial batch по batch_wait_deadline; наличие partial batch должно быть поддержано моделью/backend, иначе стартовать с B=1 или заранее совместимых фиксированных batch profiles. Padding/duplication требует маски и учёта effective FPS, не выдавать повторы за новые кадры.

Latency budget для fresh result: `age_at_enqueue + local_queue + encode + upload + remote_queue + decode/preprocess + infer + download + postprocess ≤ T_fresh`. Client и server могут каждый иметь batch delay; их сумма расходует один budget. Таймер server batch wait не включает клиентскую очередь и не гарантирует отсутствие remote backlog.

<a id="f070"></a>

## F070 — Рекомендуется модульный монолит приложения с типизированными интерфейсами, отдельным готовым медиаретранслятором и LinQ adapter. Один…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L9](_WORK/W1_04.md); W1-04-F01.

**F070 [INFERENCE].** Рекомендуется модульный монолит приложения с типизированными интерфейсами, отдельным готовым медиаретранслятором и LinQ adapter. Один последовательный владелец временного состояния на камеру; общий ограниченный inference scheduler; полная корреляция request/result. Монолит может иметь несколько worker processes: это не требует отдельных микросервисов/сетевого брокера на каждую стадию. Event + outbox сохранять одной транзакцией. Брокер в минимуме необязателен. Основания: capture/detection/storage Frigate, adapters/lifecycle Savant, live/file policies Roboflow/Ultralytics, ограничения DB/delivery ниже.

<a id="f071"></a>

## F071 — Готовым процессом брать MediaMTX **или** go2rtc. Frigate — сильный образец NVR/state/storage, но переделка всего приложения под неизвестный LinQ…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L11](_WORK/W1_04.md); W1-04-F02.

**F071 [INFERENCE].** Готовым процессом брать MediaMTX **или** go2rtc. Frigate — сильный образец NVR/state/storage, но переделка всего приложения под неизвестный LinQ за45ч рискованна. DeepStream/Savant и DL Streamer — образцы и baseline на соответствующем железе, не подтверждение LinQ. Roboflow/Ultralytics — локальная прототипизация модели/потоков, а не готовое выполнение обязательного inference path.

<a id="f082"></a>

## F082 — Actor per camera — логический единственный владелец temporal state, accepted watermark, health, активных candidates. Это coroutine с mailbox либо…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L135](_WORK/W1_04.md); W1-04-F14.

**F082 [INFERENCE].** Actor per camera — логический единственный владелец temporal state, accepted watermark, health, активных candidates. Это coroutine с mailbox либо worker process с несколькими независимыми camera state objects; процесс на каждую камеру не обязателен. Stateless inference обслуживает общий scheduler, results маршрутизируются обратно полным ключом. Согласуется с соседним `_WORK/W1_03.md` (сообщение корня: request/result key, transforms, latest per camera, bounded inflight/deadlines); соседний файл не редактировался и не является независимым сетевым доказательством этой ветки.

Псевдо-API модулей:

```text
FrameSource.next() -> FrameEnvelope | StreamStatus
InferenceAdapter.submit(InferenceRequest) -> Future[InferenceResult]
CameraState.apply(OrderedResult | Gap | EpochReset) -> [EventMutation]
EventRepository.commit(mutations, outbox_records) -> durable_commit
NotificationDispatcher.deliver(outbox_record) -> attempt_result
MediaStore.resolve(camera,epoch,media_interval) -> evidence_reference/status
```

Крупные frames/clips не идут durable event bus. Передаём ссылки/компактный envelope, а image payload лишь выбранным transport. Shared-memory pool требует ownership/lifetime: слот не перезаписывать до окончания потребления, либо сделать immutable copy на admission. Frigate slot protocol не даёт бесплатного zero-copy по интернету.

<a id="f083"></a>

## F083 — Минимальная идентичность/время

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L150](_WORK/W1_04.md); W1-04-F15.

**F083 [INFERENCE].** Минимальная идентичность/время:

| Поле | Семантика |
|---|---|
| schema_version | Версия нашего контракта |
| camera_id | Стабильный logical source, не IP/pad/session |
| stream_epoch | Новый UUID/generation при reset/fresh session; не переиспользовать0 после restart |
| frame_id | Возрастающий uint64 в epoch; назначить на decoded frame до sampling, чтобы gaps видны; не счётчик completed inference |
| pts,time_base | Исходные integer presentation timestamp и rational seconds/tick, если доступны |
| media_time_ns | Нормализованное presentation time в epoch, ns; может быть null; original PTS сохранить |
| timestamp_source | camera_pts/file_pts/host_decode_monotonic/estimated; fallback явно маркировать |
| captured_at_utc | Только при известной source clock привязке; иначе null |
| received_at_utc | Наш host receive/decode time, не exposure timestamp |
| ingest_monotonic_ns | Только duration в одном clock domain; domain/run id отдельно |
| width,height,transform_id | Оригинальная geometry и обратимость resize/letterbox/ROI |
| request_id,model_revision,preprocess_revision | Корреляция и воспроизводимость |

Ключ `(camera_id,stream_epoch,frame_id)` обязателен и в result. Track id при наличии scoped как camera:epoch:local_track_id. Event_id отдельный неизменный UUID; retries используют тот же UUID; event_revision возрастает, чтобы UI не заменил новое старым update. Semantic candidate fingerprint согласовать с violation_methods; transport dedup не решает повторное аналитическое распознавание того же эпизода.

<a id="f084"></a>

## F084 — Разделить presentation/decode order, admission order, arrival order remote results. Frame_id назначается после decoder reorder, не на packets/DTS.…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S077](SOURCES.md#s077). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L169](_WORK/W1_04.md); W1-04-F16.

**F084 [INFERENCE].** Разделить presentation/decode order, admission order, arrival order remote results. Frame_id назначается после decoder reorder, не на packets/DTS. Минимум45ч: максимум1inflight на camera, несколько cameras параллельно. Это упрощает порядок, но FPS одной камеры ограничен roundtrip+service. Для большего FPS — bounded reorder buffer.

Outstanding order хранить из **реально отправленных** ids, не ожидать last+1: sampling пропускает номера. Ready map ограничена; head completed/timeout продвигает watermark; timeout создаёт Gap и освобождает ожидание. Старые epoch, duplicate request, result ниже applied watermark, results после live deadline — reject из state update с метрикой. Не применять frame103, потом101. Offline replay допускает иную late policy, отдельный режим.

<a id="f085"></a>

## F085 — Gap не отрицательная детекция. Temporal delta считать по media_time; потеря2s не означает2s доказанного отсутствия каски. Передавать…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L173](_WORK/W1_04.md); W1-04-F17.

**F085 [INFERENCE].** Gap не отрицательная детекция. Temporal delta считать по media_time; потеря2s не означает2s доказанного отсутствия каски. Передавать Gap(start/end,reason,known_count,duration_or_unknown) и coverage. Короткий gap может сохранять candidate с неполным coverage, длинный — interrupted/unknown, а не safe/resolved. max_gap_s зависит от сценария/FPS и принадлежит violation_methods/evaluation. При VFR/неизвестном PTS нельзя переводить skipped count в секунды фиксированным FPS.

<a id="f086"></a>

## F086 — RTSP reconnect, seek/file loop, decoder restart, source replacement, backward PTS discontinuity создают новый epoch, если непрерывность нельзя…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L175](_WORK/W1_04.md); W1-04-F18.

**F086 [INFERENCE].** RTSP reconnect, seek/file loop, decoder restart, source replacement, backward PTS discontinuity создают новый epoch, если непрерывность нельзя доказать. Сериализовать StreamReset(old,new,reason). Outstanding старого epoch obsolete, reorder buffer очистить, volatile tracking/candidates сбросить, активные events завершить interrupted по договорённости. Model/preprocess/rule revision или geometry change — явная state invalidation соответствующей части. После crash восстановить incidents/outbox, создать новый epoch/run и warmup; bbox не checkpoint opaque tracker. Полный checkpoint/replay требует versioned state и обычно избыточен за45ч. UI различает ingest alive/inference alive/delivery backlog; frozen overlay не свежий результат.

<a id="f172"></a>

## F172 — Простого сочетания «PTS в envelope + один inflight на камеру + latest-frame» недостаточно для корректной временной модели. У проверенного…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L7](_WORK/W2_04.md); W2-04-F01.

**F172 [INFERENCE].** Простого сочетания «PTS в envelope + один inflight на камеру + latest-frame» недостаточно для корректной временной модели. У проверенного ByteTrack фиксированный `dt=1` на update, возраст tracks в update count, `frame_rate` регулирует только lost buffer. Для minimum45ч: один actor/camera, один parent frame в обработке, timestamps/coverage в собственном state; opaque tracker **не обязателен**. Включать этот reference tracker только после отдельного допуска фиксированного source cadence и reset при нарушении cadence/наблюдаемости. Если методы требуют устойчивый ID, а gate не пройден, соответствующий сценарий остаётся unsupported/degraded, а не становится методом без ID. Основания F173, F174, F175, F176, F177, F178 и F084, F085, F086.

<a id="f173"></a>

## F173 — В pinned ByteTrack `KalmanFilter.__init__` задаёт `ndim, dt = 4, 1.` и один раз строит motion matrix. `predict`/`multi_predict` используют её;…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S117](SOURCES.md#s117). **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L9](_WORK/W2_04.md); W2-04-F02.

**F173 [CODE].** В pinned ByteTrack `KalmanFilter.__init__` задаёт `ndim, dt = 4, 1.` и один раз строит motion matrix. `predict`/`multi_predict` используют её; elapsed seconds/PTS параметра нет. `BYTETracker.update(output_results,img_info,img_size)` также не принимает время, делает `self.frame_id += 1`, затем один `STrack.multi_predict` для tracked+lost pool. Следовательно, два вызова после source delta 0.2s и 2s оба дают один шаг модели. Порядок применения по PTS сохраняет причинность, но не меняет этот dt. Проверено чтением S117/S117, не прогоном. Временной шум/covariance также обновляется на шаг; просто заменить значение в motion matrix недостаточно, чтобы доказать корректный variable-dt tracker.

<a id="f174"></a>

## F174 — `BYTETracker.__init__`: `buffer_size=int(frame_rate/30.0*args.track_buffer)`; `max_time_lost=buffer_size`. Удаление проверяется как…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S117](SOURCES.md#s117). **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L11](_WORK/W2_04.md); W2-04-F03.

**F174 [CODE].** `BYTETracker.__init__`: `buffer_size=int(frame_rate/30.0*args.track_buffer)`; `max_time_lost=buffer_size`. Удаление проверяется как `self.frame_id-track.end_frame > self.max_time_lost`, где BaseTrack.end_frame возвращает последний frame_id track. Никакого wall-clock таймера нет. `frame_rate=5, track_buffer=30` даёт 5 update steps, не универсальную секунду: примерно 1s только при фактических 5 update/s без gaps. При 2 update/s те же 5 шагов соответствуют примерно 2.5s; strict `>` и порядок стадий добавляют границы. В update association/re-activation идёт **раньше** удаления old lost tracks: expiry не следует использовать как строгий запрет re-association через заданное число физических секунд. Изменение frame_rate не меняет KF dt. Основание S117 L146–160, L270–288; S117 L30–37.

<a id="f175"></a>

## F175 — Valid empty observation отличается от отсутствия наблюдения. Ветка `output_results.shape[1]==5` допускает NumPy массив `(0,5)`; empty detections…

**Тип основания:** CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S117](SOURCES.md#s117). **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L13](_WORK/W2_04.md); W2-04-F04.

**F175 [CODE/INFERENCE].** Valid empty observation отличается от отсутствия наблюдения. Ветка `output_results.shape[1]==5` допускает NumPy массив `(0,5)`; empty detections проходят predict/association, unmatched confirmed tracks становятся Lost, unconfirmed — Removed, frame counter растёт, существующие lost проверяются на expiry. Matching явно обрабатывает пустую cost matrix. Это вывод по коду S117/S117, **не smoke test API**; shape `(0,)`, `None` или error response не эквивалентны `(0,5)` и не подходят этому API. Пустой выход detector означает «в обработанном кадре не осталось подходящих детекций», а не физическое доказательство отсутствия человека/нарушения. Threshold filtering может также превратить непустые raw outputs в пустые detections.

<a id="f176"></a>

## F176 — Если при timeout/gap вообще не вызывать update, frame_id, predict и lost aging не продвигаются в этот промежуток. Следующий valid result будет…

**Тип основания:** CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L15](_WORK/W2_04.md); W2-04-F05.

**F176 [CODE/INFERENCE].** Если при timeout/gap вообще не вызывать update, frame_id, predict и lost aging не продвигаются в этот промежуток. Следующий valid result будет одним шагом, даже после минуты outage. Если вместо этого подать empty detection на каждом отсутствующем tick, библиотека воспримет отсутствие измерения как unmatched observation и изменит жизненный цикл tracks. Это не нейтральный способ передать Gap. У проверенного публичного API нет `gap(dt)`, `predict_only(dt)` или аргумента source frame_id. Собственный wrapper обязан сохранить отдельный Gap/coverage и явно reset либо использовать проверенную другую реализацию; synthetic empty updates не объявлять отрицательными наблюдениями.

<a id="f177"></a>

## F177 — В прочитанных BYTETracker/STrack/BaseTrack нет публичного `reset()`. Новый BYTETracker очищает собственные lists/frame_id/KF; глобальный…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S117](SOURCES.md#s117). **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L17](_WORK/W2_04.md); W2-04-F06.

**F177 [CODE].** В прочитанных BYTETracker/STrack/BaseTrack нет публичного `reset()`. Новый BYTETracker очищает собственные lists/frame_id/KF; глобальный `BaseTrack._count` продолжает расти. Безопасный minimum reset — заменить instance только в последовательном actor, поднять собственный `tracking_generation`, обнулить temporal candidates согласно domain contract, старые результаты отвергать. Не сбрасывать class-wide ID counter из actor одной камеры: он общий для instances в процессе. Subject identity: `(camera_id,stream_epoch,tracking_generation,local_track_id)`, поскольку tracking reset может случиться без source reconnect. S117/S117. Это проектный wrapper contract, не существующий ByteTrack API.

<a id="f178"></a>

## F178 — Reference не является автоматически лёгкой готовой dependency для нашего окружения: tracker импортирует torch, matching —…

**Тип основания:** CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S117](SOURCES.md#s117). **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L19](_WORK/W2_04.md); W2-04-F07.

**F178 [CODE/INFERENCE].** Reference не является автоматически лёгкой готовой dependency для нашего окружения: tracker импортирует torch, matching — scipy/lap/cython_bbox/OpenCV, используются старые `np.float`; полный README содержит detector/training dependencies. «Лёгкий» относится к рассматриваемой классической tracking схеме, не доказанному footprint/installability. Новая библиотека/порт только ради этого сравнения не нужны. README Any detector показывает integration boundary с detections; это не выбор detector. License прочитан MIT с исходным copyright, но dependencies/weights имеют отдельный scope. S117/S117/S117; установка не производилась.

<a id="f179"></a>

## F179 — Проверены три возможных опровержения fixed-dt риска: (1) передать actual FPS constructor — он меняет buffer, dt остаётся 1; (2) передать source…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L37](_WORK/W2_04.md); W2-04-F08.

**F179 [INFERENCE, попытка опровержения].** Проверены три возможных опровержения fixed-dt риска: (1) передать actual FPS constructor — он меняет buffer, dt остаётся 1; (2) передать source frame_id — update такого аргумента не имеет; (3) не обновлять на dropped frames — это сохраняет state в памяти, но останавливает aging/predict, не учитывает физическую паузу. Следовательно, эти обходы не дают variable-time semantics. Равномерная задержка ответа сама по себе не меняет source cadence, если применяются все результаты по source order; **нерегулярный sampling, timeout/drop или source discontinuity меняют**. Поэтому нужно измерять source deltas и application freshness отдельно.

Предлагаемый контракт допуска opaque reference tracker:

1. Метод согласовал `f_track`, допустимую погрешность интервала `eps_cadence`, `max_gap_media_s`, `max_live_age_s`, минимальный coverage, warmup и reset/interruption semantics. Числа сейчас UNKNOWN; 5fps — сценарный target W1, не требование кейса.
2. Source media_time известен и монотонен в epoch. Равномерный sampler выбирает реальный кадр на tick; duplicate/held frame не подменяет новое наблюдение. Измеряются `delta_media=t_current-t_last_observation`, deviation от `1/f_track`; если нужно bound ошибки выбора кадра, фиксируется source FPS/PTS uncertainty.
3. В tracker поступают success observations, включая **реальные** empty detections, последовательно с заданным cadence по source time. Late arrival допустим только в live deadline и пределах reorder budget. Между ними нет unresolved missing tick. Эквивалентность фиксированного cadence реальному видео остаётся проверяемым допущением, не обещанием ID quality.
4. При missed tick/cadence violation/unknown timestamps/слишком длинном gap wrapper делает explicit tracking reset **до** следующего accepted observation, отмечает coverage interruption. Нельзя продолжить прошлый dwell только потому, что новый track визуально похож. Не требуется новый source epoch при обычном inference drop: отдельная tracking_generation сохраняет честную source identity.
5. Если reset происходит так часто, что downstream метод не может набрать required coverage/ID lifetime, включается degraded/unsupported для этого метода. На minimum без tracker допускаются только методы, которым он не требуется, после согласования violation_methods; универсальная замена трекинга per-frame boxes не заявляется.

Это строгая минимальная политика, которая может терять эпизоды/часто сбрасываться. Более мягкая «перенести tracker через короткий gap» требует отдельной validation с подходящим gap-aware tracker/адаптацией динамики и noise; ни PTS envelope, ни rename аргументов её не доказывают. Dwell и coverage в собственном state измеряются media seconds, не update count; неизвестное время не засчитывается как доказанное наблюдение нарушения или безопасности.

<a id="f180"></a>

## F180 — Пусть `L_i` — measured steady parent-frame cycle камеры от занятия её slot до возможности admit следующего: local encode/preprocess, transport,…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L51](_WORK/W2_04.md); W2-04-F09.

**F180 [INFERENCE/arithmetic].** Пусть `L_i` — measured steady parent-frame cycle камеры от занятия её slot до возможности admit следующего: local encode/preprocess, transport, remote queue/infer, return, **client postprocess/NMS**, необходимый cascade, ordered application; плюс локальные ожидания, если slot удерживается ими. Для максимум одного такого slot на камеру средний throughput `f_i <= 1/E[L_i]` в насыщенном renewal-like режиме. Если между release и следующим admission есть scheduling delay, реальный FPS ниже. Это ceiling по среднему, а не worst-case max gap или доказательство p95. Если прежнее L означало только RPC, его нельзя подставлять в формулу полного cycle. Источник арифметики — F069, F133 с уточнением K005 и handoff W2_01.

| Условный постоянный полный L, ms | Ceiling при p_i=1, fps | Target 5fps: sequential | Идеальный нижний p_i для 5fps | Что разрешает переход к p_i>1 |
|---:|---:|---|---:|---|
| 50 | 20 | арифметически возможен, проверить load/gaps | 1 | не нужен ради target |
| 100 | 10 | возможен при запасе и fairness | 1 | не нужен ради target |
| 160 | 6.25 | возможен, но небольшой tail может сорвать tick | 1 | только после measured necessity |
| 200 | 5 | нулевой запас, не admission guarantee | 1 | запас/variance gate всё равно нужен |
| 300 | 3.33 | невозможен при одном slot | 2 | endpoint stateless/concurrent, bounded ordered buffer, credits, deadline |
| 500 | 2 | невозможен | 3 | те же prerequisites, measured throughput растёт |
| 1000 | 1 | невозможен | 5 | те же; freshness/gap могут уже исключить live |

Числа — **не LinQ измерения**, `p_min=ceil(f_target*L)` только детерминированная нижняя оценка occupancy. Несколько inflight помогают заполнить путь только при backend capacity/concurrency; remote queue может увеличить L при росте p. Для arbitrary-delay backend нет finite p, который гарантирует live age/max gap. Нельзя вычислять tail guarantee как `1/p95(L)` или складывать stage p95.

<a id="f181"></a>

## F181 — В F133 перед `floor(min(...))` добавить отдельный **per-camera feasibility gate**: для каждой admit камеры `f_req_i <= p_i/E[L_i]` как necessary…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140), [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L65](_WORK/W2_04.md); W2-04-F10.

**F181 [INFERENCE].** В F133 перед `floor(min(...))` добавить отдельный **per-camera feasibility gate**: для каждой admit камеры `f_req_i <= p_i/E[L_i]` как necessary mean check, затем measured fresh ordered FPS, max media gap, wall inter-result gap и age в целевом workload. При p=1,L=300ms target5fps не допускается даже для N=1; глобальное K=100 эту камеру не исправляет. Уменьшить target можно только если это проходит методический min-FPS/max-gap contract, иначе reduce camera count не решит single-camera latency. Потолок по bandwidth/compute также остаётся.

Для однородного пути без каскада к W1 Nmax terms можно оставить `K_a/(f_req*E[L_a])` для app parent slots **при определённом lifecycle L_a**, но отдельно проверить `p_i`, queue/reorder bytes, remote credits. С W2_01 нельзя считать live Gap/reset доказанным remote terminal. Поэтому реальный admission — пересечение availability локальных parent slots, outstanding byte budgets, server quota/credits и per-camera temporal gates; pending old remote jobs продолжают занимать remote credits после local slot release. При неизвестной terminal occupancy автоматический бесконечный resume не допускается.

**Происхождение:** [_WORK/W2_06.md:L75](_WORK/W2_06.md); W2-06-F05.

INFERENCE: интеграционное подтверждение F181, не новый независимый факт. Necessary per-camera f_required_i≤p_i/E[L_i] с full cycle и aggregate occupancy не заменяют remote-held cap/temporal tails. Cinf LinQ/Cdec/Cpre/CPU_post/Kremote и targetFPS/maxgap UNKNOWN. TOPS→N, чужой NVDEC→4070 и225person-hours→feasibility недопустимы.

<a id="f182"></a>

## F182 — Для каскада считать не detector frames только. Пусть `q_j` — calls stage j на parent frame, bounded by explicit `q_j_max`; `L_rj` — residency…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L69](_WORK/W2_04.md); W2-04-F11.

**F182 [INFERENCE].** Для каскада считать не detector frames только. Пусть `q_j` — calls stage j на parent frame, bounded by explicit `q_j_max`; `L_rj` — residency remote credit одного такого job. Necessary mean remote occupancy:

`sum_i f_i * E[sum_over_jobs_per_parent(L_rj)] <= K_remote`.

Не заменять ожидание произведения `E[q_j*L_rj]` произведением средних при crowd-dependent latency без проверки. Это occupancy, а compute CPU/model/upload/downlink capacity считаются отдельно. Для однородных камер при установленном среднем per-parent residency `A_r` remote term `N <= K_remote/(f_req*A_r)`. Для server-side batched jobs считать quota в **фактических единицах контракта**, не воображаемых frame credits.

Локально caps: parent frames/camera `p_i`, primary/secondary job counts, ROI/frame `q_max`, ROI/camera, aggregate inflight bytes, ready-result count/bytes, client postprocess queue. Parent completion должен быть определён: если для temporal observation нужны secondary results, parent не считается complete до их usable completion или explicit partial/error/gap. Если tracker питается primary раньше, secondary имеет свой sent-id/order/coverage и не может задним числом незаметно менять уже закрытый live rule state. Отсечённый ROI по quota — unknown secondary evidence, не отрицательный PPE result. Worst crowd fanout/correlation проверять E005; базовый detector резервировать от starvation.

<a id="f183"></a>

## F183 — Минимум p=1 проще, но p>1 допустим только для stateless inference либо явно поддержанного stateful sequencing. Один camera actor применяет…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L79](_WORK/W2_04.md); W2-04-F12.

**F183 [INFERENCE].** Минимум p=1 проще, но p>1 допустим только для stateless inference либо явно поддержанного stateful sequencing. Один camera actor применяет наблюдения. При send в ledger добавляется `(request_id,parent_frame_id,source_time,deadline,epoch,tracking_generation_at_admission)` в **реальном admission order**, согласованном с source presentation order. Source IDs sparse: при sampling25→5fps нормальная последовательность 100,105,110; ждать101 нельзя. Offload вне порядка допускается только если ledger заранее хранит source order selected requests.

Ready map ограничена count<=p_i и отдельными bytes; результат после validation correlation/version/epoch помещается в ready. Применять можно только head outstanding. Если head ready и ещё fresh — apply и advance; если expired/error — emit Gap с известными временем/reason, advance, tracking policy reset при необходимости. Готовый следующий result повторно проверяется на freshness после reorder wait; deadline не продлевается от его arrival. Если head hanging, actor должен получить timeout/wakeup независимо от arrival следующих replies. Новые admissions прекращаются при исчерпании parent/ready/remote caps: иначе bounded reorder queue превращается в скрытый backlog.

Local terminal Gap завершает ожидание **live state**, но remote ledger/credit освобождается только по W2_01 terminal/reconcile contract. Поздний ответ не снимает already persisted Gap и не продолжает прежний dwell. Он может быть сохранён в отдельную offline ветку, если разрешены storage/evidence policy и correlation; live replay истории не производится. Старый epoch/model/duplicate/watermark rejection причины логируются отдельно. Reset/tracking_generation на missing head влияет на дальнейший apply: будущий ready result не следует отвергать лишь потому, что его admission был до локального reset; wrapper должен явно переадресовать пригодный source observation в новую generation после gap, сохранив trace. Старый source epoch при этом по-прежнему отвергается.

### Проект trace, не выполненный результат

Media times 0.0/0.2/0.4s принадлежат одному epoch E1; IDs100/105/110. p=3, все три реально отправлены, local deadline head в условный wall500ms. Ответ110 приходит wall150ms,105 wall180ms; оба ready, apply пока нет. Ответ100 до500ms не пришёл. В500ms head превращается в Gap(timeout), **remote job100 остаётся outstanding unknown**; actor делает tracking reset, затем применяет105,110 по порядку только если каждый ещё fresh и cadence policy разрешает старт/warmup новой generation. Ответ100 в700ms live отвергается `already_gapped/late`; terminal remote reconcile может освободить его credit. По clock domains wall deadlines не сравниваются напрямую с media PTS. Если max_live_age105 уже истёк в500ms, он тоже Gap — даже если пришёл180ms. До обработки очереди нет обещания, что результат105 станет live.

На source reconnect E2 старые E1 callbacks лишь завершают remote lifecycle и/или offline запись; они не обновляют E2 actor. Если source PTS delta после100 до105 неожиданно2s вместо0.2s, **даже ordered replies** требуют gap/cadence reset до apply105. Если valid result105 содержит `(0,5)` — это Observation(empty), а не Gap(timeout). Эти случаи должны отличаться в trace и coverage.

<a id="f184"></a>

## F184 — Передать не одно число «FPS», а versioned temporal contract каждого метода: `min_unique_observation_fps`, измерительное окно/coverage denominator,…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S140](SOURCES.md#s140). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_04.md:L93](_WORK/W2_04.md); W2-04-F13.

**F184 [INFERENCE].** Передать не одно число «FPS», а versioned temporal contract каждого метода: `min_unique_observation_fps`, измерительное окно/coverage denominator, `target_sample_period`, cadence tolerance, `max_media_gap_s`, `max_live_result_age_s`, warmup, dwell semantics, reset/unknown/partial/interrupted rules, ID continuity requirement, timestamp uncertainty и допустимость missing PTS. Mean5fps не исключает burst10frames+пауза2s; max gap и coverage обязательны. Критерий fresh-result FPS указывать и по applied source coverage, и по wall-time обслуживания; одинаковая средняя rate не даёт одинаковую оперативность.

Четыре разных величины: source/decode FPS; sampler admitted unique frames/s; completed valid RPC frames/s; **fresh ordered applied observations/s**. Secondary ROI/model calls — отдельная rate. Два тайминга: delta source time соседних accepted observations для физической временной модели и wall inter-application/result age для доступности/оперативности. Arrival jitter не превращается в motion dt, а source gap не скрывается ранним buffered delivery. Без true source clock mapping это не sensor-to-operator SLA; использовать ingest-relative age с явным timestamp_source.

<a id="f214"></a>

## F214 — Предлагаемый scheduler для 45 часов [INFERENCE, не реализован]

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L119](_WORK/W1_03.md); дополнительная тематическая выписка.

## Предлагаемый scheduler для 45 часов [INFERENCE, не реализован]

1. Каждая camera session имеет monotonically increasing stream_epoch после reconnect и frame_id внутри session. Capture/decode выполняется независимо от infer. Для stateless detection — один pending latest-frame slot на камеру: новый кадр заменяет старый до отправки. Счётчик replacement обязателен. Decoder продолжает вычитывать поток, иначе очередь просто смещается в upstream. Архив/клип имеют отдельный pipeline: discard inference frame не означает уничтожить видеодоказательство.
2. Глобальный semaphore ограничивает outstanding requests и bytes; не создавать async task на каждый входной кадр, ожидающий semaphore с полным payload. Сначала выбрать eligible camera, затем забрать её latest slot. Для самого простого трекинга ограничить одним inflight frame/camera; суммарную concurrency получать разными камерами. Если одной камеры мало для заполнения RTT, разрешать несколько только с bounded reorder buffer и явной политикой timeout/gap. Сравнить оба режима экспериментом.
3. Eligible камеры обходить round-robin; f_target_i реализовать token bucket или next_due_i, но ограничить burst. В модельном пуле batch формируется только для одинаковых model/version/input contracts; максимум один кадр камеры за круг. Исчезнувшая камера не блокирует обход остальных. Это обеспечивает справедливость допуска, но не гарантирует одинаковый FPS при разной стоимости задач.
4. Начать с B=1 и нулевого намеренного batch wait, измерить saturation curve C. Затем пробовать только разрешённые backend batches и малые batch_wait budgets. Для нерегулярных каскадов допустимо отдельное семейство queues, но не бесконечная очередь каждого crop. Лимит ROI jobs/frame, ROI jobs/camera и общий cap; значения определяет измеренный load и требования методов.
5. Cross-model fairness: не выдавать busy model весь semaphore. Минимальный вариант — отдельные bounded quotas base detector / secondary classifier; global device execution gate, если runtime не thread-safe/не поддерживает параллелизм. Weighted round-robin/deficit scheduling можно строить по measured service ms, а не числу jobs: дешёвый classifier и тяжёлая pose модель имеют разную стоимость. Строгий priority только urgent jobs без квоты способен вытеснить базовую детекцию; нужна минимальная доля/aging. Конкретные веса не установлены.
6. До encode/send отклонять кадр, если freshness budget исчерпан; перед отправкой считать оставшийся budget. RPC timeout ограничивать оставшимся временем с резервом postprocess, а на сервере перед infer повторять проверку, если можем запускать свой код. Не сравнивать clocks разных хостов без установленной синхронизации: monotonic timestamp для local duration, source PTS + clock domain для событий, remaining budget для RPC.
7. Result admission: проверить request_id, epoch, model version, parent frame/crop transform; старый epoch не обновляет новое состояние камеры. Если frame_id ≤ last_applied, не кормить онлайн tracker задним числом. Просроченный результат может быть сохранён для offline evidence с признаком stale, но не должен молча рисоваться поверх live frame или считаться текущим состоянием безопасности. Late результат не равен «нарушения нет».
8. Stateful model — отдельный режим. Latest-frame discard может нарушить temporal input contract; sequence affinity, start/end/reset, допустимые gaps и eviction state согласовать с model_stack/violation_methods. Для external tracker CPU состояние удобно держать по camera+epoch независимо от stateless infer model. На reconnect явно reset/reinitialize; не связывать sequence identity со временем прибытия RPC response.
9. Timeout не означает, что server ничего не исполнил. Automatic retry устаревшего кадра выключить; при необходимости повторять с тем же request_id и дедупликацией результата, лишь пока frame freshness budget остаётся. После восстановления удалённого сервиса брать latest frames, не проигрывать очередь всей паузы.

Это предложение разделяет ответственность: scheduler — допуск/fairness/freshness; adapter — протокол/серверный контракт; tracker/rules — temporal state и семантика пропусков. Для multi-chip board после получения SDK распределять независимые камеры/модели через тот же interface. Не предполагать automatic load balancing, multi-chip affinity, shared model memory или разделение одного infer между кристаллами.

<a id="f215"></a>

## F215 — Контракт adapter, сохраняемый при смене доступа [INFERENCE]

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L133](_WORK/W1_03.md); дополнительная тематическая выписка.

## Контракт adapter, сохраняемый при смене доступа [INFERENCE]

`capabilities()` возвращает подтверждённые input formats, tensor shape/dtype/layout/color, max batch, variable-batch support, concurrency/thread safety, request size cap, timeout/cancel semantics, model names/versions. Неизвестное значение — unknown, не default true.

Request metadata: schema_version, request_id, camera_id, stream_epoch, frame_id, source_pts + units + clock_domain, ingest timestamp, remaining freshness budget, model_id/version, payload_format (JPEG/RGB/tensor), width/height, dtype/layout/color, preprocessing transform; ROI: parent_frame_id, roi_xyxy и track context. Бинарный payload отдельно от metadata. Result: те же correlation IDs, actual executed model version, detections в объявленной coordinate system, status/error, backend=LinQ/other, server stage durations при наличии. Для доказательства LinQ нужен дополнительный execution provenance от платформенной ветки, одного поля backend недостаточно.

| Вариант | Когда использовать | Что проверить первым | Цена реализации |
|---|---|---|---|
| HTTP request/response с binary body, reused session, bounded async concurrency | endpoint уже HTTP либо разрешён собственный wrapper на хосте | JPEG vs tensor, max body, auth, keepalive/proxy, errors/timeouts; конкретную Triton extension только после metadata/contract проверки | Простая диагностируемая граница; схема и бинарный формат явно описываются |
| gRPC unary async | есть protobuf/service definition либо собственный controlled wrapper | доступность HTTP/2 через сеть, channel/stream caps, message size, TLS/auth, cancellation, client/server versions | Typed schema, generated clients; streaming не обязателен для pipelining |
| gRPC bidirectional stream | сервер уже требует stream или реально выгодна долгоживущая sequence | queue depth в stream, backpressure, reconnect/reset, cancellation scope, correlation/out-of-order | Сложнее recovery и балансировка; сравнить с unary на том же payload |
| WebSocket binary | готовый endpoint или нужен собственный bidirectional gateway | фрейминг metadata+payload, ack/admission, queued bytes, max message, proxy idle timeout, reconnect epoch | Весь inference application protocol и отдельные deadlines строим сами |
| Local runtime process на LinQ host, кадры decode там | разрешён свой код и сервер видит camera/file stream | codec/network reachability, runtime safety, topology permissions | Убирает пересылку raw/tensor через WAN; большой инфраструктурный выигрыш зависит от доступа |

Скорость конкретного протокола не ранжировалась: сравнение без одинаковых payload, reuse connections, concurrency, compression, TLS, языка и RTT бессодержательно. При JPEG сначала оценивать codec size/quality/CPU; смена HTTP→gRPC не уменьшит сам JPEG на порядок.

# 05 Каталог проектов: version, license, hardware, reuse

<a id="f072"></a>

## F072 — Существенная свежая ловушка: текущий DeepStream Python Apps README уже заявляет SDK9.0 и deprecation Python bindings/no wheels начиная9.0; Savant…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S063](SOURCES.md#s063), [S067](SOURCES.md#s067). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L13](_WORK/W1_04.md); W1-04-F03.

**F072 [CODE].** Существенная свежая ловушка: текущий DeepStream Python Apps README уже заявляет SDK9.0 и deprecation Python bindings/no wheels начиная9.0; Savant README рекомендует production0.5.x/DS7.0 и отдельно development0.6.x/custom DS7.1/TRT10.9. Нельзя смешивать latest images и старые инструкции PyDS. S063/S067.

<a id="f073"></a>

## F073 — video_pipeline.md Overview/Detailed view: acquisition→decode→motion→object; recording может брать original stream. Пример5FPS — sampling…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S060](SOURCES.md#s060). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L36](_WORK/W1_04.md); W1-04-F04.

**F073 [DOC].** video_pipeline.md Overview/Detailed view: acquisition→decode→motion→object; recording может брать original stream. Пример5FPS — sampling illustration, не измерение/требование.

<a id="f074"></a>

## F074 — video/ffmpeg.py::capture_frames49–117 читает raw frame через readinto в shared memory, обнуляет timestamp слота до заполнения и ставит после,…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L38](_WORK/W1_04.md); W1-04-F05.

**F074 [CODE].** video/ffmpeg.py::capture_frames49–117 читает raw frame через readinto в shared memory, обнуляет timestamp слота до заполнения и ставит после, отправляет nonblocking только(frame_name,timestamp). При queue.Full увеличивается skipped FPS и слот переиспользуется. `datetime.now().timestamp()` берётся до pipe read: **это host timestamp, не camera PTS/exposure time**. Такой timestamp нельзя выдавать за source media_time.

<a id="f075"></a>

## F075 — camera/maintainer.py держит camera_processes/capture_processes по камере, создаёт CameraCapture/CameraTracker. comms/inter_process.py использует…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S060](SOURCES.md#s060). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L40](_WORK/W1_04.md); W1-04-F06.

**F075 [CODE].** camera/maintainer.py держит camera_processes/capture_processes по камере, создаёт CameraCapture/CameraTracker. comms/inter_process.py использует ZeroMQ REP/REQ+JSON (`ipc:///tmp/cache/comms`). Следовательно MQTT из README — integration channel, не доказанная общая шина сырых кадров. app.py/models.py подтверждают разделение capture/detector/record/events.

<a id="f076"></a>

## F076 — mediamtx.yml текущего HEAD: readTimeout10s, writeQueueSize512, metrics false; sourceOnDemand false; record false; recordFormat fmp4;…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S061](SOURCES.md#s061). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L53](_WORK/W1_04.md); W1-04-F07.

**F076 [CODE].** mediamtx.yml текущего HEAD: readTimeout10s, writeQueueSize512, metrics false; sourceOnDemand false; record false; recordFormat fmp4; recordPartDuration1s, recordSegmentDuration1h, recordDeleteAfter1d. Это default, не рекомендованная политика хранения. Part1s не равна segment1h. Recording не заменяет incident DB.

<a id="f077"></a>

## F077 — SourceInfoRegistry раздельно хранит logical source_id и pad index. pipeline.py::on_last_pad_eos874–923 проверяет source id, вызывает…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S063](SOURCES.md#s063). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L77](_WORK/W1_04.md); W1-04-F08.

**F077 [CODE].** SourceInfoRegistry раздельно хранит logical source_id и pad index. pipeline.py::on_last_pad_eos874–923 проверяет source id, вызывает buffer_processor.on_eos, удаляет frame attrs источника (включая dropped при teardown), выдаёт SinkEndOfStream и удаляет output elements через GLib. Практический смысл: reconnect/end — явное lifecycle событие с очисткой; pad index не стабильная camera identity.

<a id="f078"></a>

## F078 — gvametapublish.md intro: MQTT/Kafka reconnect поддержан, но metadata во время reconnect **не cached/not published**, проходит дальше pipeline.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S064](SOURCES.md#s064). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L90](_WORK/W1_04.md); W1-04-F09.

**F078 [DOC].** gvametapublish.md intro: MQTT/Kafka reconnect поддержан, но metadata во время reconnect **не cached/not published**, проходит дальше pipeline. Следовательно broker element не гарантирует сохранность alert до broker. max-reconnect-interval default30s, doubling с1s. По max-connect-attempts текст допускает-1, таблица unsigned1..10; это противоречие документа, проверить gst-inspect установленной версии, не копировать-1 вслепую.

<a id="f079"></a>

## F079 — video_source.py::_set_file_mode_buffering_strategies по умолчанию WAIT; _set_stream_mode_buffering_strategies — ADAPTIVE_DROP_OLDEST.…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S065](SOURCES.md#s065). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L103](_WORK/W1_04.md); W1-04-F10.

**F079 [CODE].** video_source.py::_set_file_mode_buffering_strategies по умолчанию WAIT; _set_stream_mode_buffering_strategies — ADAPTIVE_DROP_OLDEST. _consume_stream_frame имеет явные branches drop-oldest/drop-latest и updates с frame_id/source_id/timestamp/cause. Это подтверждает разные intent offline-complete/live-fresh и учёт dropped, не обязательный конкретный threshold.

<a id="f080"></a>

## F080 — stream/entities.py: ModelActivityEvent(frame_decoding_timestamp,event_timestamp,frame_id);…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S065](SOURCES.md#s065). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L105](_WORK/W1_04.md); W1-04-F11.

**F080 [CODE].** stream/entities.py: ModelActivityEvent(frame_decoding_timestamp,event_timestamp,frame_id); LatencyMonitorReport(source_id,frame_decoding_latency,inference_latency,e2e_latency); CompletionStatistics содержит process-local monotonic timestamp и комментарий сравнивать только snapshots одной pipeline. InferenceHandler получает list VideoFrame, SinkHandler — соответствующие prediction/frame. Нельзя вычитать process-local monotonic значения local/LinQ hosts.

<a id="f081"></a>

## F081 — test4 main253–320 создаёт filesrc/h264parse/nvv4l2decoder/nvstreammux/nvinfer/nvvideoconvert/nvdsosd/nvmsgconv/nvmsgbroker, tee+queues.…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S067](SOURCES.md#s067). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L131](_WORK/W1_04.md); W1-04-F13.

**F081 [CODE].** test4 main253–320 создаёт filesrc/h264parse/nvv4l2decoder/nvstreammux/nvinfer/nvvideoconvert/nvdsosd/nvmsgconv/nvmsgbroker, tee+queues. Probe157–204 берёт frame_meta.frame_num и кладёт в msg_meta.frameId; example публикует только first object на каждом30м кадре. Это демонстрация metadata/broker, не готовая полная incident logic.

<a id="f217"></a>

## F217 — W1-04-P01 Frigate — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S060](SOURCES.md#s060). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L25](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P01 Frigate

- project: Frigate NVR, Frigate Inc./blakeblackshear.
- version: dev HEAD `91e91c68efe504e17b7fd3fb437b34068b4387ca`, `2026-10-20T09:53:28-05:00`. Subject упоминает Axelera Metis detector v0.19; это не номер всего Frigate.
- license: MIT; торговые марки Frigate отдельно исключены README из MIT.
- layers: FFmpeg/go2rtc ingest; detect substream и main recording stream; decode/downscale/motion gating; отдельные detector processes; temporal object state, events/timeline, recording, WebRTC/MSE/browser, MQTT integration. app.py содержит RecordProcess, ReviewProcess, OutputProcess, ObjectDetectProcess и Event/Timeline handlers. models.py разделяет Event и Recordings.
- hardware: NVIDIA для всего NVR необязательна; README рекомендует GPU/AI accelerator, backends отдельные. Конкретный LinQ backend не найден в прочитанном.
- reuse: разделить запись исходного видео и частоту аналитики; ограниченные очереди/shared-memory frame slots; per-camera lifecycle/watchdog; metadata IPC вместо полного изображения.
- constraints: большой внутренне связанный NVR. Переделка detector/config/models под неизвестный SDK рискованна; Linux IPC endpoint не проверен на Windows. Motion gating не переносить автоматически на статические нарушения.
- sources: S060, F073, F074, F075.

<a id="f218"></a>

## F218 — W1-04-P02 MediaMTX — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S061](SOURCES.md#s061). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L42](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P02 MediaMTX

- project: MediaMTX, bluenviron.
- version: main HEAD `b37cdf55707f3ef0bab87b3e69985832ae6a6e9b`, `2026-10-22T16:39:14Z`.
- license: MIT.
- layers: media router: publish/read/proxy/record/playback, RTSP/WebRTC/HLS и другие protocols, API/metrics/hooks. Не inference/rules/incidents product.
- hardware: Go binary/container, NVIDIA для маршрутизации не требуется. Protocol conversion не гарантирует codec transcoding; оно отдельной цепочкой.
- reuse: готовый media process для RTSP mock cameras, единой ingest точки, browser outputs и recording/playback. На45ч предпочтительнее собственного RTSP proxy.
- constraints: frame identity/state/event DB/LinQ backend добавляет наше приложение; browser codecs/NAT/network config проверить. Latency/FPS не измерялись.
- sources: S061,F076.

<a id="f219"></a>

## F219 — W1-04-P03 go2rtc

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S062](SOURCES.md#s062). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L55](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P03 go2rtc

- project: go2rtc, Alexey Khit/AlexxIT.
- version: master HEAD `c245815e75e2a5fd60b4290f12bfc04e55a984d3`, `2026-07-13T13:54:05+03:00`.
- license: MIT.
- layers: RTSP/ONVIF/many camera protocol inputs; RTSP/WebRTC/MSE/HLS/MJPEG outputs, HTTP/WebSocket API; FFmpeg transcoding по необходимости.
- hardware: binaries Windows/macOS/Linux/FreeBSD, разные CPU architectures; FFmpeg отдельная зависимость нужных routes.
- reuse: компактный готовый camera gateway, особенно нестандартные камеры; альтернатива MediaMTX. Встроен в экосистему Frigate.
- constraints: не NVR/event DB/inference framework. Zero-delay в README — CLAIM, не нулевая end-to-end latency. Security/config важны: defaults API1984, RTSP8554, WebRTC8555 TCP/UDP не следует автоматически открывать интернету. Codec/FFmpeg лицензии отдельно.
- sources: S062 Configuration/Streaming input/output/Security/LICENSE.

<a id="f220"></a>

## F220 — W1-04-P04 Savant — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S063](SOURCES.md#s063). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L66](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P04 Savant

- project: Savant, InSight Platform.
- version: develop HEAD `24a3c8d82fc42cc04a903c71e62084ba7ee9f8a0`, `2026-09-04T17:31:50+02:00`. README production0.5.x отдельно от development0.6.x.
- license: Apache2.0 repo, NVIDIA dependencies отдельно.
- layers: DeepStream/GStreamer pipeline, YAML stages+Python callbacks; source/sink adapters и Client SDK, общий video+metadata protocol, dynamic sources, OTel/Prometheus, JSON/video/image/RTSP sinks.
- hardware: processing требует NVIDIA.0.5.x/DS7.0;0.6.x/custom DS7.1/TRT10.9, x86 driver570.133.20+ по README. LinQ не установлен.
- reuse: source adapters отдельно от pipeline, source registry, явные EOS/cleanup, общий correlation metadata/video; interface pattern сильнее самого runtime.
- constraints: новая NVIDIA framework dependency ради неизвестного LinQ не оправдана за45ч. README fault tolerance/performance — author claims до теста.
- sources: S063,F077.

<a id="f221"></a>

## F221 — W1-04-P05 DL Streamer — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S064](SOURCES.md#s064). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L79](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P05 DL Streamer

- project: Deep Learning Streamer, Intel/dlstreamer.
- version: main HEAD `51c317f8d969574784caae2ba02c494e40b62002`, `2026-10-22T10:59:48Z`.
- license: MIT repo, OpenVINO/GStreamer/models отдельно.
- layers: GStreamer video/audio pipelines; OpenVINO gvadetect/gvaclassify/gvainference; Python extensions; metadata conversion, watermark, MQTT/Kafka/file publishing, smart NVR samples.
- hardware: README явно Intel CPU/GPU/NPU. Слово NPU не означает любой NPU/LinQ.
- reuse: buffer+attached metadata→serialize→publication, Python callbacks; reference pipeline при навыке GStreamer/OpenVINO. Custom LinQ element — отдельная разработка.
- constraints: publication не равна durable incidents. Найден прямой loss-on-reconnect факт F078.
- sources: S064,F078.

<a id="f222"></a>

## F222 — W1-04-P06 Roboflow Inference — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S065](SOURCES.md#s065). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L92](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P06 Roboflow Inference

- project: Inference, Roboflow.
- version: main HEAD `15d1f4478e1b5cf531ec87ad6d55e30afe58ba0f`, `2026-10-22T13:03:20Z`. InferencePipeline теперь в interfaces/legacy_stream; video code выделен в stream_vision/streamvision.
- license: **не вся repo Apache**. Root LICENSE: LICENSE.core Apache2.0 по умолчанию, superseding licenses в subdirs, отдельно models/enterprise. Проверить nearest LICENSE конкретного пути и weights. Code рассматривается как образец, не как уже очищенная от license вопросов dependency.
- layers: self-hosted HTTP inference server+SDK, Workflows, pipeline source→inference handler→sink, video source/buffering/backpressure/monitoring. Полная production incident DB не доказана README.
- hardware: CPU и CUDA image routes; backends/model-specific. LinQ не установлен.
- reuse: VideoFrame envelope, status/drop updates, latency reports, sink callbacks, различие live/file buffering.
- constraints: package/API меняются; pin обязательно. Account/API/model downloads зависят от выбранного маршрута; offline-ready без подготовки не установлено. Полный Workflows engine избыточен, если основной риск transport LinQ.
- sources: S065,F079/F080.

<a id="f223"></a>

## F223 — W1-04-P07 Ultralytics — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S066](SOURCES.md#s066). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L107](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P07 Ultralytics

- project: Ultralytics Python package.
- version: main HEAD `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, `2026-10-22T22:27:18+02:00`.
- license: AGPL3.0; README предлагает Enterprise alternative. Не permissive MIT; weights/product composition отдельно передать market_deployment/model_stack.
- layers: model predict/export и streaming dataloaders/Results/annotation; не NVR/durable event application.
- hardware: CPU/GPU/export routes зависят от модели/формата; LinQ backend не установлен.
- reuse: быстрый локальный baseline и latest-frame pattern; наш FrameSource должен добавить epoch/PTS/correlation.
- constraints: общий loader может ждать stalled camera; return не полный media envelope. README performance tables не end-to-end наши измерения.
- sources: S066,F062.

<a id="f224"></a>

## F224 — W1-04-P08 DeepStream Python Apps — контекст

**Тип основания:** DOC/CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S067](SOURCES.md#s067). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L120](_WORK/W1_04.md); дополнительная тематическая выписка.

### W1-04-P08 DeepStream Python Apps

- project: NVIDIA-AI-IOT/deepstream_python_apps, NVIDIA; образцы/bindings SDK.
- version: master HEAD `8ad0349ed7a496fae35ebb21c350641727070b89`, `2026-04-01T14:16:03+05:30`. README SDK9.0, Ubuntu24.04, Python3.12, gst-python1.24.1. Package subject1.2.3 не версия всего SDK.
- license: Apache2.0 **sample/bindings repo**; не утверждать Apache для бинарного DeepStream SDK.
- layers: GStreamer sources/parser/NVIDIA decode→nvstreammux→nvinfer→metadata/OSD→video sink или nvmsgconv/nvmsgbroker; dynamic multi-source examples.
- hardware: NVIDIA DeepStream/CUDA, не arbitrary NPU runtime.
- reuse: batching, per-source metadata, tee с отдельными queues visualization/broker, source add/delete lifecycle.
- constraints: Python bindings deprecated; wheels с9.0 не выпускаются, рекомендован PyServiceMaker; README numpy2.x unsupported. На45ч без опыта/проверенной версии — архитектурный образец, не основная dependency.
- sources: S067,F072/F081.

# 06 Events, brokers, outbox, concurrency и DB boundaries

<a id="f087"></a>

## F087 — Два разных потока: frames/results с bounded loss ради freshness и подтверждённые event mutations с durable commit/retry/dedup. Process…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L179](_WORK/W1_04.md); W1-04-F19.

**F087 [INFERENCE].** Два разных потока: frames/results с bounded loss ради freshness и подтверждённые event mutations с durable commit/retry/dedup. Process Queue/asyncio mailbox не durable после reboot. WebSocket — projection, DB — source of truth. После browser reconnect snapshot из DB+cursor replay; live update может потеряться.

| Вариант | Первичное основание | Ограничение/решение45ч [INFERENCE] |
|---|---|---|
| Mailbox + SQLite outbox | Транзакционная local DB, ограничения F092 | Рекомендуемый минимум, один DB writer, небольшой dispatcher |
| Redis Streams | Consumer groups/Pending/XACK/XAUTOCLAIM | Если Redis уже нужен/знаком; events/control, не raw video; persistence/retention/reclaim всё равно настраивать |
| Core NATS | Ephemeral at-most-once | Live status подходит; единственный durable alert channel — нет |
| NATS JetStream | Persistence/replay/durable consumers/ack, pull batch/expires | Хорошая альтернатива Redis при знакомом NATS; выбрать один broker |
| MQTT5 | QoS/session state/retained per topic | Интеграция IoT/HA, не замена incident DB; QoS2 не атомарный внешний effect |
| Kafka | Partition log/replay, producer idempotence/transactions | Новый cluster не окупается для нескольких demo cameras; взять только готовый infrastructure/experience |

<a id="f088"></a>

## F088 — Redis XREADGROUP since5.0 делит сообщения между consumer group members, Pending хранит unacked. XAUTOCLAIM since6.2 меняет ownership idle pending.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S068](SOURCES.md#s068), [S069](SOURCES.md#s069). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L190](_WORK/W1_04.md); W1-04-F20.

**F088 [DOC].** Redis XREADGROUP since5.0 делит сообщения между consumer group members, Pending хранит unacked. XAUTOCLAIM since6.2 меняет ownership idle pending. Чтение только `>` не подбирает abandoned pending автоматически. Trimming способен удалить payload pending entry. Поэтому нужны reclaim/retention относительно backlog и ack после durable effect. Current docs unfrozen показывают новые options; не зависеть от синтаксиса новее установленного сервера. S068/S069.

<a id="f089"></a>

## F089 — NATS Core — ephemeral at-most-once/no storage; JetStream отдельный persistence/replay/per-reader ack слой. Pull consumer batch/expires…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S070](SOURCES.md#s070), [S071](SOURCES.md#s071). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L192](_WORK/W1_04.md); W1-04-F21.

**F089 [DOC].** NATS Core — ephemeral at-most-once/no storage; JetStream отдельный persistence/replay/per-reader ack слой. Pull consumer batch/expires ограничивают fetch. Фразы «у нас NATS» недостаточно: нужны Core/JetStream и storage/consumer config. Продвинутая exactly-once JetStream дедупликация этой веткой не заявляется. S070/S071.

<a id="f090"></a>

## F090 — MQTT5 Standard2019-03-07 §§4.3/4.4: QoS2 — протокольный подтверждаемый обмен; retry при session reconnect; retained §3.3.1.3 — заменяемое…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S072](SOURCES.md#s072). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L194](_WORK/W1_04.md); W1-04-F22.

**F090 [DOC/INFERENCE].** MQTT5 Standard2019-03-07 §§4.3/4.4: QoS2 — протокольный подтверждаемый обмен; retry при session reconnect; retained §3.3.1.3 — заменяемое сообщение на topic. [INFERENCE] QoS2 не транзакция нашей DB/Telegram. Для camera status retained полезен, журнал incidents требует event store. S072.

<a id="f091"></a>

## F091 — Kafka4.1 Design Message Delivery Semantics: producer idempotence устраняет producer retry duplicates в log, transactions атомарны в Kafka…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S073](SOURCES.md#s073). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L196](_WORK/W1_04.md); W1-04-F23.

**F091 [DOC].** Kafka4.1 Design Message Delivery Semantics: producer idempotence устраняет producer retry duplicates в log, transactions атомарны в Kafka partitions. External output требует координации consumer position с effect, например offset вместе с output. Это не exactly-once произвольного HTTP endpoint. S073.

<a id="f092"></a>

## F092 — SQLite WAL: readers одновременно с writer, но writer один; все процессы на одном host, не network filesystem. [INFERENCE] подходит local app с…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S074](SOURCES.md#s074), [S075](SOURCES.md#s075). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L198](_WORK/W1_04.md); W1-04-F24.

**F092 [DOC/INFERENCE].** SQLite WAL: readers одновременно с writer, но writer один; все процессы на одном host, не network filesystem. [INFERENCE] подходит local app с owner writer; не shared DB файл между local и LinQ host. Нельзя обещать Nкамер без event rate test. PostgreSQL18 Locking Clause: FOR UPDATE SKIP LOCKED полезен queue-like tables, но не строгий FIFO. Переходить при multi-host writers/сложных concurrent operator transactions, не ради схемы. S074/S075.

### Transactional outbox и side effects

<a id="f093"></a>

## F093 — Одна DB transaction: event mutation с unique(event_id,event_revision), outbox unique(event_id,event_revision,destination), commit. Dispatcher…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S075](SOURCES.md#s075). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L202](_WORK/W1_04.md); W1-04-F25.

**F093 [INFERENCE].** Одна DB transaction: event mutation с unique(event_id,event_revision), outbox unique(event_id,event_revision,destination), commit. Dispatcher отправляет, пишет attempt/result/delivered marker. Если receiver поддерживает idempotency key — стабильный ключ. Broker publish подтверждать publisher ack нужного режима, но повтор между acceptance и local marker возможен. Consumer inbox/dedup тоже durable.

| Crash point | Восстановление | Чего не обещать |
|---|---|---|
| До commit | Нет event/outbox; volatile candidate мог исчезнуть | Что каждый увиденный frame сохранён |
| После commit до send | Outbox pending, retry | Мгновенная доставка offline recipient |
| После send до delivered marker | Возможен duplicate send | Exactly-once внешнего effect без idempotency |
| Consumer effect до broker ack | Redelivery, inbox/unique предотвращают повторный DB effect | Что broker ack включает внешнюю transaction |
| Broker недоступен | DB alert существует, outbox backlog, health degraded | «Нарушений нет» при выключенном transport |

При нескольких dispatchers не держать row lock/transaction во время network timeout: lease/claim timestamp или короткая transaction SKIP LOCKED и отдельный completion. На45ч один dispatcher. Bounded retries+error/dead-letter, чтобы poison payload не остановил все alerts. Update не получает новый event_id. Clip ready — новая revision того же event; alert не ждёт post-event video.

### multiprocessing/asyncio

<a id="f094"></a>

## F094 — multiprocessing subprocesses обходят обычный CPython GIL; Queue сериализует передаваемые objects. asyncio.to_thread снимает blocking с event loop;…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S076](SOURCES.md#s076), [S077](SOURCES.md#s077). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L216](_WORK/W1_04.md); W1-04-F26.

**F094 [DOC].** multiprocessing subprocesses обходят обычный CPython GIL; Queue сериализует передаваемые objects. asyncio.to_thread снимает blocking с event loop; CPU-bound Python обычно не ускоряет из-за GIL, исключение native extensions с release GIL. Конкретный OpenCV/SDK path нельзя объявлять всегда освобождающим GIL без проверки. S076/S077.

<a id="f095"></a>

## F095 — asyncio — network/RPC/timeouts/mailboxes/API/dispatcher. Decode — subprocess/process либо thread с измеренным stall. CPU-heavy Python —…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S076](SOURCES.md#s076), [S077](SOURCES.md#s077). **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L218](_WORK/W1_04.md); W1-04-F27.

**F095 [INFERENCE].** asyncio — network/RPC/timeouts/mailboxes/API/dispatcher. Decode — subprocess/process либо thread с измеренным stall. CPU-heavy Python — process/native vectorized после измерения. Blocking LinQ SDK изолировать worker process, если свой код разрешён; API-only — async client с cap. Thread safety/multiprocess runtime LinQ неизвестны. Не наследовать native runtime/CUDA handle автоматически fork; spawn-compatible init и handle внутри worker, importable worker, main guard облегчают Windows/Linux. Большие images в multiprocessing.Queue копируются; shared memory лишь после измерения, с bounded pool/ownership/cleanup. Stop/drain protocol, watchdog, force terminate только recovery: принудительное завершение может портить queues/locks.

<a id="f096"></a>

## F096 — Согласовать schema/fixtures до готовности LinQ

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L222](_WORK/W1_04.md); W1-04-F28.

**F096 [INFERENCE].** Согласовать schema/fixtures до готовности LinQ:

```json
{
 "schema_version":1,"event_id":"uuid-created-once","event_revision":1,
 "kind":"violation.opened","camera_id":"cam-01","stream_epoch":"new-session-uuid",
 "rule_id":"configured-rule","rule_revision":"version-hash",
 "subject_id":"camera:epoch:local-track-id",
 "observed_interval":{"start_media_ns":1000000000,"end_media_ns":2300000000},
 "evidence_frames":[{"frame_id":42,"media_time_ns":2300000000}],
 "coverage":{"state":"partial","gap_count":1},
 "produced_at_utc":"2026-10-23T03:30:00Z","model_revision":"artifact-hash",
 "inference_backend":"linq","inference_run_id":"execution-log-id",
 "evidence":{"clip_status":"pending","snapshot_uri":null,"clip_uri":null},
 "correlation_id":"trace-id"
}
```

Интервал1.0–2.3s иллюстрирует units, не порог. Kinds opened/updated/closed/interrupted versioned; closed с reason. Coordinate_space/transforms в frame/result contract. backend=linq только с фактическим execution evidence; mock/CPU/RTX писать честно и показывать UI. Model/rule revisions нужны replay.

Возможное распределение5участников:1ingest/media/frame identity;2LinQ adapter/model/preprocess;3camera state/rules/events;4API/UI/DB/outbox;5media evidence/deploy/system metrics/integration. Contracts+fixtures+timeouts общие в первый час. Это проектный вариант, компетенции неизвестны.

<a id="f117"></a>

## F117 — SSE reconnect не равен durable replay

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S088](SOURCES.md#s088). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L181](_WORK/W1_05.md); W1-05-F21.

### F117 — DOC: SSE reconnect не равен durable replay

S088: EventSource получает UTF-8 `text/event-stream`; `id` задаёт last event ID, браузер передаёт Last-Event-ID при восстановлении; `retry` в ms меняет reconnect delay; heartbeat comment примерно каждые 15 s помогает против legacy proxy timeouts. INFERENCE: сервер обязан сам хранить последовательность событий и выполнить replay после cursor; одного EventSource недостаточно для гарантии. Держать одно multiplexed connection на страницу, history API для полного resync, конечный срок replay. Если cursor старше retention — вернуть/показать resync condition, а не молча потерять тревоги. EventSource constructor не предлагает произвольного Authorization header; same-origin cookie/session или другой обоснованный способ auth согласовать заранее.

<a id="f118"></a>

## F118 — WS не хранит события после disconnect

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S089](SOURCES.md#s089). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L185](_WORK/W1_05.md); W1-05-F22.

### F118 — DOC/INFERENCE: WS не хранит события после disconnect

S089 `bufferedAmount` описывает bytes, поставленные браузерным `send` в очередь и ещё не переданные сети; это не receiver ACK. Стандартный WS API не обеспечивает наш durable incident history/replay. Для server→browser смотреть очереди самого сервера, а не browser bufferedAmount, который относится к исходящему browser traffic. Проект: WS для двусторонних команд/частых обновлений, SSE для одностороннего event feed, REST для acknowledge и истории. Оба транспорта нуждаются в event_id, sequence/cursor, dedup и восстановлении состояния. Подтверждение UI renderer и подтверждение оператором — разные записи.

<a id="f119"></a>

## F119 — durable outbox на границе event/уведомление

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L189](_WORK/W1_05.md); W1-05-F23.

### F119 — INFERENCE: durable outbox на границе event/уведомление

В одной DB transaction сохранить incident и outbox rows по нужным каналам; иначе crash между DB commit и `send()` теряет уведомление или создаёт «призрачную» тревогу. Ключ job `(event_id, channel, recipient, message_kind/version)` уникален; worker читает persisted pending/retry rows, ставит попытку/lease, записывает result/external message ID, backoff и next_attempt. На 429 учитывать provider retry hint, на временный timeout повторять с exponential backoff+jitter, permanent auth/recipient error выводить в failed/dead state. Отдельно ограничивать общую и per-recipient частоту.

Сетевой timeout после принятия сообщения провайдером даёт uncertain outcome. Если API не предоставляет idempotency key с доказанной семантикой, exactly-once не обещать: возможен дубликат. В тексте event_id/ссылка помогут человеку и приложению распознать его, но не создадут provider-side дедупликацию. UI может обновлять одну карточку по event_id. Failed outbox не удаляется без следа. Pending clip job и pending notification — разные state machines.

Метрики разнести: `event_decided`, `event_committed`, `outbox_attempted`, `provider_accepted`, `browser_rendered`, `operator_acknowledged`. Длительность между разными host clocks не вычитать без синхронизации/оценки погрешности. Вебсокет send и Telegram Message response не означают прочтение человеком.

<a id="f120"></a>

## F120 — Telegram бесплатные лимиты не единый «30/s»

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S090](SOURCES.md#s090), [S091](SOURCES.md#s091). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L197](_WORK/W1_05.md); W1-05-F24.

### F120 — DOC: Telegram бесплатные лимиты не единый «30/s»

S090 FAQ: избегать более 1 сообщения/с в один чат; группы — не более 20/мин; рассылка — примерно 30/с бесплатно. Упомянуты paid broadcasts с иными условиями; для MVP на них не рассчитывать. S091 `sendVideo`: video до 50 MB, поддерживаемый Telegram-клиентами MPEG4, on success возвращает Message; `ResponseParameters.retry_after` — секунды до повторения после flood control. Это текущие server docs, не измеренные гарантии latency. Ссылка на защищённую карточку + thumbnail обычно быстрее/проще отправки полного clip; приватный production URL не будет автоматически доступен получателю или Telegram fetcher. Не класть camera credentials в ссылку.

<a id="f121"></a>

## F121 — MAX изменил endpoint/auth

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S092](SOURCES.md#s092). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L201](_WORK/W1_05.md); W1-05-F25.

### F121 — DOC: MAX изменил endpoint/auth

S092 Обзор: направлять запросы на `platform-api2.max.ru` вместо `platform-api.max.ru`; требуется доверие сертификату Минцифры по документации. Query token больше не поддерживается, нужен `Authorization: <access_token>`. Токен получают при создании бота на business platform/через указанный business workflow. Это не доказательство, что команда уже имеет право/аккаунт/работающий токен, и не основание отключать TLS verification. Проверка регистрации/доступа относится к первому часу, делать MAX обязательным единственным каналом до этого рискованно.

<a id="f122"></a>

## F122 — MAX send limit и attachments

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S093](SOURCES.md#s093). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L205](_WORK/W1_05.md); W1-05-F26.

### F122 — DOC: MAX send limit и attachments

S093 POST `/messages`: текст, image/video/audio/file и inline keyboard/share поддержаны документацией; лимит до 2 сообщений/с в один диалог, группу или канал; превышение требует очереди/задержки. Отдельный общий limit из прочитанных страниц не установлен. Нет достоверного p50/p95 времени доставки/доказательства read receipt. Не переносить лимиты Telegram на MAX. No messages sent; медиазагрузка не проверена.

<a id="f189"></a>

## F189 — WAL позволяет readers вместе с одним writer, но требует общий host и корректную local FS/shared-memory locking; network-mounted DB не является…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S074](SOURCES.md#s074), [S122](SOURCES.md#s122), [S123](SOURCES.md#s123). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L63](_WORK/W2_05.md); W2-05-F05.

**F189 [DOC; S074/S122/S123].** WAL позволяет readers вместе с одним writer, но требует общий host и корректную local FS/shared-memory locking; network-mounted DB не является этим minimum. `synchronous=NORMAL` в WAL сохраняет consistency и application-crash recovery, но подтверждённый transaction может исчезнуть после power loss/OS crash. `FULL` добавляет WAL sync на каждый commit и выбран для event/outbox/remote ledger/pin intents: потерянный admission ledger может разрешить лишние remote obligations. FULL зависит от честных VFS/fsync/storage и не восстанавливает потерянный диск. Media files не входят в SQLite transaction. Atomicity между несколькими ATTACH DB в WAL также не гарантируется как единый набор — держать связанные event/outbox/credits/pins в одной DB.

<a id="f190"></a>

## F190 — Proposed startup/config contract, не исполненные команды

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S122](SOURCES.md#s122), [S123](SOURCES.md#s123), [S126](SOURCES.md#s126). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L65](_WORK/W2_05.md); W2-05-F06.

**F190 [INFERENCE на S122/S123/S126].** Proposed startup/config contract, не исполненные команды:

```sql
-- Вне любой транзакции; проверить returned value и повторно прочитать настройки.
PRAGMA journal_mode=WAL;
PRAGMA synchronous=FULL;
PRAGMA foreign_keys=ON;
PRAGMA busy_timeout=1000;
PRAGMA wal_autocheckpoint=1000;
SELECT sqlite_version(), sqlite_source_id();
PRAGMA compile_options;
```

Busy1000ms и autocheckpoint1000pages — начальные настройки эксперимента, не latency SLA/размер WAL cap. `journal_mode` persistent, `foreign_keys`/busy/synchronous устанавливать и проверять на каждой соответствующей connection до transactions; foreign_keys change внутри transaction — no-op. Контролировать SQLite version и source_id именно через connection Python worker, не `sqlite3 --version` соседнего CLI. Не считать Python `sqlite3.version` версией движка. Runtime compile_options нужны для omitted-FK/locking/build provenance. На old vendor version с backport запросить vendor advisory/package release/hash, не отвергать/принимать автоматически по tuple.

Один dedicated DB writer thread/task с bounded input queue владеет connection; sync sqlite calls не блокируют WS event loop. Connection создана и используется своим thread, без необоснованного `check_same_thread=False`. Read connections short-lived queries/transactions, не держать cursor/snapshot при browser streaming, network await или ожидании LinQ. Long readers мешают checkpoint и могут растить WAL,1000pages — trigger, не hard bound. Метрики queue depth/oldest age, commit duration/errors, WAL bytes/checkpoint busy+remaining, free disk. При stall не добавлять unlimited writer tasks и не считать принятый в RAM event durable.

Для Python3.12 выбрать один явный transaction mode: `autocommit=sqlite3.LEGACY_TRANSACTION_CONTROL, isolation_level=None` и explicit SQL `BEGIN IMMEDIATE`/`COMMIT`/`ROLLBACK`; до config нет open transaction. Это сознательно зафиксированный compatibility mode, а не reliance на default. `autocommit=False` сразу открывает новую transaction после commit/rollback и потому требует аккуратного отдельного config phase; не смешивать два режима и `executescript` внутри event transaction. Prepared/bound params, короткие transactions, schema migrations при остановленном admission. Конкретный implementation не написан.

<a id="f191"></a>

## F191 — В одной transaction фиксировать incident revision, dedup key, outbox rows, durable clip admission+finite requested interval/byte reservation/refs,…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S123](SOURCES.md#s123), [S126](SOURCES.md#s126). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L84](_WORK/W2_05.md); W2-05-F07.

**F191 [DOC+INFERENCE; S123/S126].** В одной transaction фиксировать incident revision, dedup key, outbox rows, durable clip admission+finite requested interval/byte reservation/refs, а для remote submit — соответствующее admission/held intent до внешнего side effect поW2_01. Network send/decode/hash/export в эту DB transaction не включать. UI `event_committed`, `pin accepted`, remote credit reserved выдаются только после успешного COMMIT. Это разные state machines, но атомарно связанные DB rows. WS notification после commit — projection, её потеря восполняется history/reload; provider accept не operator read.

`BEGIN IMMEDIATE` может дать BUSY; bounded retry по overall operation deadline, затем visible persistence_unavailable/admission rejected. Busy timeout не общий deadline любого SQL. COMMIT может вернуть BUSY с transaction still active: не повторять все side effects; по policy retry commit либо rollback. FULL/IOERR/NOMEM могут отменить statement или всю transaction; проверить transaction state (`in_transaction` вPython), rollback если active, закрыть/восстановить suspect connection по error policy. Никакого success после catch. Если process погиб на границе commit и caller не знает исход, после recovery искать unique operation/event key и read durable row; не blindly repeat submit/send. IOERR с uncertain state требует reconcile, не «значит точно rollback».

**Попытка опровержения F189, F190, F191.** Даже single writer+FULL не устраняет: (a) old SQLite checkpoint race; (b) WAL starvation long read; (c) broken FS sync/physical disk loss; (d) successful remote action после ledger backup cutoff; (e) file bytes, опубликованные без fsync до durable DB row. Следовательно DB durability не равна end-to-end evidence/remote exactly-once. Исправленный runtime, bounded readers, separate file protocol и restore reconciliation обязательны; tests ниже различают эти failure classes.

<a id="f192"></a>

## F192 — Disk-full policy: reserve capacity под DB/WAL/status + bounded media reserve на основании inventory; clips/live image cache не могут съесть всё.…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S123](SOURCES.md#s123). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L90](_WORK/W2_05.md); W2-05-F08.

**F192 [INFERENCE; S123/W2_02].** Disk-full policy: reserve capacity под DB/WAL/status + bounded media reserve на основании inventory; clips/live image cache не могут съесть всё. Low-water threshold закрывает new evidence admissions/extensions и recorder, удаляет только expired unpinned/failed temporary derivatives, сообщает partial/unavailable. Если DB не коммитит, нельзя durable зафиксировать даже сообщение «disk full» в ней: сигнализировать UI/health и best-effort bounded external log; не объявлять statuses сохранёнными. Освободить резерв/устранить I/O, затем reopen/read-check/reconcile и вернуться к admission. Не повторять infinite commits и не удалять pinned originals для спасения иллюзии complete. SQLITE_FULL может относиться к DB/temp storage, не обязательно к одной media partition. Off-process export bounded by jobs/bytes, tmp files tracked.

<a id="f193"></a>

## F193 — Открытый `.db` нельзя считать надёжным backup через обычный copy. WAL содержит часть committed persistent state; отделение от hot WAL может…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S074](SOURCES.md#s074), [S124](SOURCES.md#s124), [S125](SOURCES.md#s125), [S126](SOURCES.md#s126). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L94](_WORK/W2_05.md); W2-05-F09.

**F193 [DOC; S074/S124/S125/S126].** Открытый `.db` нельзя считать надёжным backup через обычный copy. WAL содержит часть committed persistent state; отделение от hot WAL может потерять commits/повредить DB. Sequential copy `.db`/`-wal` во время записи не создаёт согласованный snapshot. `-shm` — восстанавливаемый wal-index, не замена WAL. Не удалять hot `-wal`/journal как «cleanup» и не заменять DB под работающими connections. Нормальное закрытие последней connection обычно checkpoint+remove, но нельзя предполагать это после crash.

Выбранный live backup primitive — Python `Connection.backup(target, pages=..., progress=..., sleep=...)`, основание S126; source/target distinct connections/files. C API S124: step может restart при concurrent external writes, `BUSY/LOCKED` retryable, I/O/ENOMEM/READONLY fatal; `backup_finish` без достигнутого DONE может вернуть OK при отмене, но destination transaction rollback. Поэтому success определяется завершённой операцией без exception и верифицированным destination, не фактом создания файла или закрытия handle. У Python backup `sleep` — интервал повторов, не общий timeout: отдельный maintenance worker с overall budget/progress/cancellation policy, не WS loop; не выдавать бесконечно busy backup за ready. `VACUUM INTO` — документированная альтернатива, не выбранная основная процедура; checkpoint не является backup.

<a id="f194"></a>

## F194 — Backup DB не делает атомарный snapshot DB+clips+remote world. Простая воспроизводимая процедура для45ч — короткое координированное maintenance…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S124](SOURCES.md#s124). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L98](_WORK/W2_05.md); W2-05-F10.

**F194 [INFERENCE; S124/W2_02/W2_01].** Backup DB не делает атомарный snapshot DB+clips+remote world. Простая воспроизводимая процедура для45ч — короткое координированное maintenance window (она пока не выполнена):

1. Stop new remote submissions/event mutations/clip admissions, stop retention deletion. Не обнулять unresolved held credits. Дождаться bounded writer drain; отметить уже существующие remote obligations и external side effects. Remote jobs могут продолжать работать; cutoff не делает их terminal.
2. Closed immutable media files и их validated index/hash/refs формируют backup inventory. Pending/open recording tails не объявлять complete; либо закрыть/validate bounded, либо включить intents и explicit unavailable tail. Повесить backup hold на нужные files до конца их копирования, finite owner/expiry/cap. Не блокировать весь live service бесконечно из-за postroll/remote task.
3. Запустить supported online backup в новый temporary destination при paused mutations; сохранить DB schema version, app/config/model hashes, runtime version/source_id и snapshot cutoff/operation IDs/remote account+deployment identity. Если поддерживаем live writes при более сложном будущем режиме, нужен общий versioned snapshot/hold protocol; здесь он не доказан.
4. Закрыть destination connection; открыть backup отдельно, выполнить `PRAGMA integrity_check` и `PRAGMA foreign_key_check`, проверить critical invariants (outbox/event unique keys, job refs, reservations). Integrity_check не проверяет FK вместо отдельного pragma, не доказывает наличие media или remote terminality. Успех только целиком; failed temp не назначать последним хорошим backup.
5. Копировать inventory immutable bytes, verify size+hash destination; missing file — incomplete backup, не удалять запись для скрытия ошибки. Нужны manifest с file hashes и status, backup DB checksum, cutoff и явный media coverage. Close/fsync/atomic rename публикуемого backup+manifest/directory sync — по exact OS/FS supported recipe; этот recipe ещё gate, особенноWindows. Hash не заменяет fsync и не доказывает provenance.
6. Сохранить комплект на другой failure domain при требовании disk-loss recovery. Копия рядом на том же диске восстанавливает accidental row deletion, но не disk loss. Секреты/ключи отдельно защищать и восстанавливать с нужными permissions; не класть tokens в manifest/log. По успешной публикации снять backup holds и возобновить mutations/retention; после abort holds снимаются только с owner/state учётом, finite TTL не permission удалять ещё используемые backup bytes.

RPO равен реальному cutoff последнего verified complete backup плюс отдельно установленные loss bounds, не нулю. RTO и backup interval UNKNOWN до размера/сети/диска/fixture. Online copy освобождает SQLite locks между steps, но наша cross-file процедура сознательно координирует mutations. Не обещать «zero downtime backup of everything».

<a id="f195"></a>

## F195 — Recovery сначала делает состояние безопасным, затем доступным. Все worker processes остановлены или fenced; единственный recovery owner, новая…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S074](SOURCES.md#s074), [S123](SOURCES.md#s123), [S126](SOURCES.md#s126), [S124](SOURCES.md#s124), [S125](SOURCES.md#s125). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L111](_WORK/W2_05.md); W2-05-F11.

**F195 [INFERENCE на S074/S123, S124, S125, S126/W2_01/W2_02].** Recovery сначала делает состояние безопасным, затем доступным. Все worker processes остановлены или fenced; единственный recovery owner, новая boot/deployment generation. Не запускать два экземпляра writer/retention над одним каталогом и не переносить обычный RAM lease между ними.

1. Сохранить повреждённый комплект DB/WAL/journal/media для диагностики, не repair in place исходную единственную копию. Restore проверенный backup в отдельный каталог; старые WAL/SHM другой DB generation туда не подмешивать. Если recover current crash DB, дать SQLite открыть её с соответствующим WAL/journal; не вручную обнулять их. При ошибке recovery — quarantine/verified restore, не создать пустую DB незаметно.
2. Сверить source_id/runtime/PRAGMAs/schema/config/model compatibility; integrity_check+foreign_key_check. Миграции versioned, backup до миграции. Writer admission/remote submit/retention пока закрыты. Старый backup может не знать фактов после cutoff; foreign keys внутри восстановленного DB не обнаружат потерянные external obligations.
3. Scan media+index: validated closed files сверить поhash/size/header/sample coverage. `creating/open` intents →recovering; truncated tails quarantine, usable prefix только отдельный validated derivative с original hash и partial reason. DB row→missing bytes: missing/partial/unavailable, не complete. File→нет row: orphan/quarantine, provenance/mapping unknown; не приписывать event по filename/mtime/UTC. Native archive остаётся mapping unknown. Hash совпал — целостность этого file, не полное событие.
4. Rebuild pins/reservations из durable jobs/manifests/manual holds/backup holds и finite future ranges, dedup unique bytes; refcount — derived cache, не единственная истина. Пока scan/rebuild не окончен — no retention deletion. При противоречии удержать ограниченный recovery quarantine reserve и отказать new admissions, не unlimited hold всех files. Для missing original manifest partial; released orphan temp удаляется лишь после owner reconciliation.
5. Leases: локальные outbox/clip leases с old boot owner fenced. OS monotonic timestamps после reboot не переиспользовать; persisted logical expiry/wall deadline + new monotonic budget и clamp policy, при unknown wall step — safe recovering/terminal bounded reason, не бессрочное ожидание. Только локальную idempotent работу можно переclaim после проверки durable job/dedup key; старый worker не должен поздно commit без owner generation compare. Outbox provider timeout — uncertain delivery/duplicate possible, не новая exactly-once гарантия.
6. Remote ledger W2_01: restore cutoff старый, значит jobs, принятые после него, могли сохраниться у server при полном отсутствии local rows. Не обнулять held и не re-submit по emptiness backup. Query/list/reconcile через documented provider contract, account/deployment ownership и external durable evidence; если list/idempotency/terminal нет — conservative unknown obligations, stop relevant admission и owner resolution. Expiry local lease не доказывает remote cancel/terminal. Новый deployment ID не стирает работу старого. Восстановленный ledger не является permission освободить shared device.
7. После consistency/fencing/reconciliation gates открыть read UI с явным recovering/stale, затем local idempotent jobs, затем inference admission и retention. Available evidence публиковать только после media validation + DB commit; историю не переписывать silently — revisions/status reasons. Сохранить recovery report: backup cutoff, missing/orphans, jobs/pins/refcounts before/after, held unresolved, lost intervals, operator-visible state. Если unresolved remote scope нельзя ограничить, LinQ admission остаётся закрытым; cached UI может работать.

<a id="f196"></a>

## F196 — Prospective DB↔file publish protocol: durable intent+reserved bytes → tmp write → trailer/close → validate coverage/hash → flush file and…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L121](_WORK/W2_05.md); W2-05-F12.

**F196 [INFERENCE; W2_02/K008 boundary].** Prospective DB↔file publish protocol: durable intent+reserved bytes → tmp write → trailer/close → validate coverage/hash → flush file and appropriate FS metadata → atomic rename same filesystem+directory persistence recipe → transaction marks closed_validated and commits refs/actual intervals. На failure после rename до DB commit получится orphan для reconcile; после intent до write — missing/pending, не complete. Atomic rename без durability recipe не power-loss guarantee. Delete: writer serializes pin-admission и mark `deleting` для unpinned file; после этого новые pin requests отвергаются/получают unavailable, затем unlink, затем DB tombstone commit. Crash оставляет pending deleting, повтор unlink идемпотентен по internal fileID+expected hash/path; нельзя после restart без recomputed refs удалять по старому счетчику. DB transaction не может атомарно commit обычный filesystem unlink. Never execute user-controlled path. У native recorder нет нашего pin protocol автоматически — это приложение/45ч scope gate.

| Failure class | Что DOC позволяет ожидать / проектная граница | Что остаётся UNKNOWN |
|---|---|---|
| Process crash/kill собственного app | SQLite WAL recovery сохраняет committed tx при корректной FS; uncommitted rollback. UI ack только после commit; файл/ledger reconcile обязателен | Actual code correctness, native library cleanup, lost uncommitted event, per-tail recoverability |
| Graceful host reboot | Drain/close улучшает shutdown, но реализация должна быть проверена отдельно; forced reboot как OS crash | Service order/FS/driver/lifecycle и реальные recovery duration |
| OS crash/hard reset/power loss | WAL+FULL требует honored sync, patched SQLite и storage; NORMAL не даёт такую durability. Media fsync отдельно | Hardware caches, device barriers, target FS, фактический полный стек; process kill это не проверяет |
| Disk loss/corruption | Нужен verified backup в другом failure domain, restore/reconcile remote obligations; FULL диск не дублирует | RPO/RTO, последний verified cutoff, потерянные media/ledger facts после него |

# 07 Evidence: сегменты, generations, mapping, pins и finite policy

<a id="f097"></a>

## F097 — длительность сегмента связана с GOP

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S079](SOURCES.md#s079). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L46](_WORK/W1_05.md); W1-05-F01.

### F097 — DOC: длительность сегмента связана с GOP

S079 §segment: новый сегмент обычно начинается ключевым кадром reference stream; если он не совпал с запрошенным временем, разбиение произойдёт на следующем. Segmenter лучше работает с одним CFR video. `segment_time_delta` допускает погрешность округления timestamps при force-keyframes. `reset_timestamps` сбрасывает начало сегмента близко к нулю, но документация оговаривает зависимость от muxer/codec. Эти параметры нельзя принять за гарантию точного окна или единой исходной шкалы времени.

<a id="f098"></a>

## F098 — обход keyframe меняет условие, не создаёт независимость кадров

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S081](SOURCES.md#s081), [S079](SOURCES.md#s079). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L50](_WORK/W1_05.md); W1-05-F02.

### F098 — CODE: обход keyframe меняет условие, не создаёт независимость кадров

S081 `seg_write_packet` проверяет reference stream, флаг keyframe (либо `break_non_keyframes`), число кадров и временное/кадровое условие; затем вызывает `segment_end` и `segment_start`. В таблице options `break_non_keyframes` по умолчанию 0. INFERENCE: переключение этого параметра не создаёт отсутствующий IDR и не устраняет межкадровые зависимости. Для доказательств нельзя считать любой маленький сегмент самостоятельно декодируемым только потому, что файл появился.

<a id="f099"></a>

## F099 — stream copy сохраняет компрессию, фильтры требуют raw frames

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S080](SOURCES.md#s080). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L54](_WORK/W1_05.md); W1-05-F03.

### F099 — DOC: stream copy сохраняет компрессию, фильтры требуют raw frames

S080 §3.1–3.3: stream copy передаёт пакеты из demuxer в muxer без decode/encode; фильтрация выполняется на decoded frames. INFERENCE: запись оригинала `-c copy` экономит вычисления, не меняет изображение повторным сжатием; наложение рамок, blur лиц, resize и frame-accurate переработка требуют иной ветви с декодированием/кодированием. Не обещать одновременно оригинальный битстрим и встроенное размытие.

<a id="f100"></a>

## F100 — два разных вида evidence export

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S080](SOURCES.md#s080), [S079](SOURCES.md#s079). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L58](_WORK/W1_05.md); W1-05-F04.

### F100 — DOC/INFERENCE: два разных вида evidence export

S080 `-ss`: input seek находит близкую точку до target; с transcoding и default accurate_seek лишнее декодируется/отбрасывается; со stream copy сохраняется. S079 fragmentation: обычный MP4 часто зависит от корректного финального metadata; fragmented MP4 устроен иначе и может сохранять полезные fragments при прерывании. Это не гарантия дисковой сохранности после power loss.

Рекомендуемый оригинал: покрывающие target interval исходные segments + manifest, фактические start/end, gaps. Производный клип: отдельно reencode/trim для просмотра, linked original IDs и provenance. Нельзя молча подписывать clip «ровно 5 секунд до», если его первый usable frame позже. При copy допускается больше материала до/после, но не меньше без `partial`.

<a id="f101"></a>

## F101 — MediaMTX уже умеет запись, но retention не знает наших incident pin

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S082](SOURCES.md#s082). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L64](_WORK/W1_05.md); W1-05-F05.

### F101 — DOC: MediaMTX уже умеет запись, но retention не знает наших incident pin

S082 Usage: `recordFormat: fmp4` или `mpegts`, `recordPartDuration: 1s`, `recordMaxPartSize: 50M`, `recordSegmentDuration: 1h`, `recordDeleteAfter: 1d`; это пример конфигурации, не наши выбранные значения. Документ называет part duration RPO и пишет о потере последней part при сбое. INFERENCE: для очень простого демо можно брать готовую запись MediaMTX вместо собственного remuxer. Нужно отдельно подтвердить recovery на выбранном FS/ОС. Автоудаление по времени не выражает pin инцидента: либо экспортировать incident в независимую папку до expiry, либо отключить auto-delete и управлять удалением самим. Длинный часовой segment неудобен для небольшого кольца и быстрых копий; это изменяемая настройка, не обязательный архитектурный выбор.

<a id="f102"></a>

## F102 — hooks есть, но finished segment может прийти позднее тревоги

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L68](_WORK/W1_05.md); W1-05-F06.

### F102 — DOC: hooks есть, но finished segment может прийти позднее тревоги

S033 tag v1.21.2 `runOnRecordSegmentCreate` / `runOnRecordSegmentComplete` позволяют внешней обработке реагировать на сегменты. `recordPartDuration` и `recordSegmentDuration` — разные сущности. INFERENCE: не ждать закрытия часового файла для первой тревоги. Сначала event + pending clip, после закрытия нужного interval — clip-ready update. Нельзя объявлять open file complete из одного факта появления имени.

<a id="f103"></a>

## F103 — Frigate даёт полезный контрпример «pre-roll настроен, но отсутствует»

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S083](SOURCES.md#s083). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L72](_WORK/W1_05.md); W1-05-F07.

### F103 — DOC: Frigate даёт полезный контрпример «pre-roll настроен, но отсутствует»

S083: Frigate пишет исходный поток без reencode, временно складывает segments в cache, валидирует и переносит по retention policy. Экспорты сохраняются отдельно и не удаляются retention. `pre_capture`/`post_capture` относятся к временному окну, но при `mode: motion` сохраняются только подходящие по motion segments. Следовательно, отсутствие движения до события может вырезать часть pre-roll. Это документированное поведение конкретной current версии, не проверка нашего приложения. Для evidence completeness выбирать непрерывную запись/`all` в нужном окне и явно проверять покрытие.

<a id="f104"></a>

## F104 — безопасный жизненный цикл кольца

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L76](_WORK/W1_05.md); W1-05-F08.

### F104 — INFERENCE: безопасный жизненный цикл кольца

Проект, а не найденная гарантия готового SDK:

* Recorder пишет immutable сегменты с уникальными именами `camera_id/stream_epoch/segment_seq`; не переиспользовать имя в кольце. Индекс содержит исходную шкалу PTS/time_base, фактический временной диапазон, stream profile, размер, decode/validation status. Файл сначала считается open, после финализации и проверки — closed/available. Временные имена/atomic rename полезны при одной ФС, но сохранность после питания требует отдельного теста fsync/FS.
* При событии с исходным временем `t_event` выбрать `[t_start-pre, t_end+post]`; для продолжающегося события `t_end` ещё изменяется. В одной согласованной операции добавить durable clip job и pins ссылок на существующие segments; pin относится также к будущему target interval. Сразу защищать pre-roll, не ждать post-roll.
* Возраст кольца должен превышать `pre + worst_case_event_arrival_delay + segment_close_delay + margin`, все в секундах. Если event-time пришёл с задержкой удалённого инференса больше глубины кольца, требуемый pre-roll уже утрачен. Буфер «10 секунд» недостаточен при 15-секундной задержке результата.
* Retention worker удаляет только closed, не pinned, не читаемый/не экспортируемый segment; pins и удаление координируются БД/одним owner. Одна проверка file existence перед экспортом не защищает от гонки удаления. Можно копировать в независимый immutable incident directory; hardlink подходит только с пониманием одной ФС и copy-on-delete semantics, не как универсальная инструкция.
* После post-roll собирается manifest доступных интервалов, выявляются gaps, отсутствующие boundary keyframes и decode failures. Clip status: pending → complete, либо partial с missing intervals/reason, либо failed. Полнота файла/временного окна и качество распознавания — отдельные свойства.
* При рестарте сверить индекс и ФС, open/truncated файлы отправить на validation/quarantine, восстановить незавершённые clip jobs; не проставлять complete всем .mp4. Pin должен жить на диске/в БД, не только в Python set.
* При исчерпании диска остановить/деградировать запись с явным storage fault; события и metadata сохранять по возможности. Не вытеснять pinned evidence молча. У pins отдельная квота/срок/ручное освобождение, иначе incident storm полностью заполняет диск.

Для 45 часов достаточно SQLite/PostgreSQL event table + segment index + одна очередь clip jobs и один retention owner; конкретный storage engine согласовать с владельцем V08. MinIO/S3 добавляет распределённость, но не решает lifecycle сам. Хэши и manifest доказывают неизменность сохранённого набора относительно хэшей, а не юридическую chain of custody и не отсутствие пропущенных кадров.

<a id="f105"></a>

## F105 — объём хранения в decimal GB

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L90](_WORK/W1_05.md); W1-05-F09.

### F105 — INFERENCE: объём хранения в decimal GB

При среднем суммарном video+audio bitrate `b` в Mbit/s (1 Mbit = 10^6 bit), непрерывной записи 86400 s/day:

`S_GB_per_day = b * 10^6 * 86400 / 8 / 10^9 = 10.8 * b`.

`S_total_GB = N * D_days * 10.8 * b * recording_fraction + derived_clips_GB + thumbnails_metadata_GB + reserve_GB`.

Это арифметическая оценка payload, без контейнеров, файловой системы, replication и эксплуатационного резерва. Для VBR измерить интеграл фактического размера за репрезентативное время, а не подставлять max bitrate как средний. Event fraction нельзя считать долей кадров с нарушениями: pre/post-roll и округление до segments расширяют запись; overlapping incidents могут делить исходные segments, но отдельные exports дублируют байты.

| Средний bitrate одной записи | 1 камера GB/day | 50 камер GB/day | 500 камер GB/day | 500 камер, 7 дней, decimal TB |
|---|---:|---:|---:|---:|
| 0.5 Mbit/s | 5.4 | 270 | 2700 | 18.9 |
| 1 Mbit/s | 10.8 | 540 | 5400 | 37.8 |
| 2 Mbit/s | 21.6 | 1080 | 10800 | 75.6 |
| 4 Mbit/s | 43.2 | 2160 | 21600 | 151.2 |
| 8 Mbit/s | 86.4 | 4320 | 43200 | 302.4 |

Пример-допущение: main 4 Mbit/s + substream 0.5 Mbit/s, если хранить оба, — 48.6 GB/day/camera; только main — 43.2. При 500 камерах main ingress 2 Gbit/s и payload write 250 MB/s, без overhead/резерва. Raw RGB ring 1920×1080×3 bytes ×25 frame/s ×10 s = 1,555,200,000 bytes ≈1.56 GB на камеру; compressed 4 Mbit/s ×10s /8 =5 MB. Поэтому кольцо evidence разумно держать encoded, а не весь raw frame history. Это расчёты, не измерение камеры или LinQ.

Main/substream экономят decode/network только на соответствующей ветви: substream для аналитики не уменьшает место main archive. Низкое разрешение может убрать мелкий респиратор/сигарету; это решение принимает evaluation/violation_methods. Между main и substream нельзя считать одинаковым frame_id или ROI alignment без проверки crop/FOV/clock.

<a id="f150"></a>

## F150 — Для заявляемого соответствия event→original segment выбрать одного владельца demux на камеру/профиль: те же encoded access units идут в decode и…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L7](_WORK/W2_02.md); W2-02-F01.

**F150 INFERENCE.** Для заявляемого соответствия event→original segment выбрать одного владельца demux на камеру/профиль: те же encoded access units идут в decode и indexed remux. MediaMTX1.21.2 — relay. Отдельный native recorder остаётся альтернативой, но его нельзя считать сопоставленным независимому PyAV decoder по UTC filename. Реализация своего remux не выполнена и её простота за45ч не доказана: ранний gate E009 обязателен. Если gate провален, честный scope cut — snapshot анализируемого кадра, native archive с mapping unknown; не «точный клип».

Новая находка: fMP4 v1.21.2 содержит custom `mtxi` с recorder StreamID, SegmentNumber, DTS, NTP. Это сильнее filename UTC, но не содержит source/decoder epoch. Native playback export эту UserData не сохраняет. Оригиналы и manifest нужны отдельно.

<a id="f151"></a>

## F151 — `recordSegmentDuration` — minimum, не maximum. H264 recorder ждёт IDR перед созданием DTSExtractor, сохраняет PTSOffset=`u.PTS-dts`, IDR как sync.…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L31](_WORK/W2_02.md); W2-02-F02.

**F151 DOC/CODE S033/S033.** `recordSegmentDuration` — minimum, не maximum. H264 recorder ждёт IDR перед созданием DTSExtractor, сохраняет PTSOffset=`u.PTS-dts`, IDR как sync. Новая граница в Track.write только при next sync sample и `nextDTS−segment.startDTS >= segmentDuration`. Long GOP делает2s setting длиннее2s; stalled source/нет следующего keyframe означает отсутствие конечного close bound. Отрицательная duration next DTS clamp0; sample с отрицательным basetime отбрасывается. Drift NTP vs DTS больше±5s вызывает reset/error; tolerance5s не означает accuracy5s. Контролируемый H264 B0/GOP≤1s — проектная fixture; произвольная камера требует GOP проверки. MediaMTX не создаёт отсутствующий IDR.

Проектная native configuration, не запущена:

```yaml
pathDefaults:
  record: yes
  recordFormat: fmp4
  recordPartDuration: 1s
  recordMaxPartSize: 50M
  recordSegmentDuration: 2s
  recordDeleteAfter: 0s
```

`0s` deletion допустим только с работающим bounded janitor. Part size cap — RAM part, не весь disk cap; превышение возвращает error. При проверенном GOP≤1s target2s даёт условно около2–3s segment при continuous input/bounded I/O, не unconditional SLA.

<a id="f152"></a>

## F152 — mtxi v0: StreamID16bytes, SegmentNumber uint64, DTS int64 в ns (Go duration), NTP int64 UnixNano. Init tracks дают Timescale, sample parts —…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L47](_WORK/W2_02.md); W2-02-F03.

**F152 CODE S033.** mtxi v0: StreamID16bytes, SegmentNumber uint64, DTS int64 в ns (Go duration), NTP int64 UnixNano. Init tracks дают Timescale, sample parts — relative BaseTime/PTSOffset. StreamID=`uuid.New()` при recorderInstance.initialize, а не source/decoder generation; segment sequence локальна format. mtxi не содержит original RTP SSRC/packet IDs/raw PTS/time_base/event ID. DTS уже после depacketization/codec extractor. Равенство PyAV raw timestamps и mtxi.DTS не установлено.

<a id="f153"></a>

## F153 — Create hook: MTX_PATH, MTX_SEGMENT_PATH, RTSP_PORT, regex G1…; complete добавляет MTX_SEGMENT_DURATION в seconds. Нет PTS/start…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L49](_WORK/W2_02.md); W2-02-F04.

**F153 CODE S033.** Create hook: MTX_PATH, MTX_SEGMENT_PATH, RTSP_PORT, regex G1…; complete добавляет MTX_SEGMENT_DURATION в seconds. Нет PTS/start NTP/StreamID/SegmentNumber/decoder epoch. External command Restart:false, не durable ack queue. Control APIRecordingSegment содержит только start; recording=name,segments; list=itemCount,pageCount,items. Для mtxi нужен parser исходного файла. Create вызывается после os.Create ДО writeInit: это не readable/complete file. Complete callback вызывается при успешном File.Close, даже если ранее closeCurPart/writeDuration сохранили error: hook не заменяет validation/coverage.

<a id="f154"></a>

## F154 — Native `/list?path&start&end` принимает RFC3339, отдаёт start/duration/url (возможно concatenated/clipped timespan).…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L51](_WORK/W2_02.md); W2-02-F05.

**F154 DOC/CODE S033/S033.** Native `/list?path&start&end` принимает RFC3339, отдаёт start/duration/url (возможно concatenated/clipped timespan). `/get?path&start&duration&format=fmp4|mp4` — download/remux primitive, не durable export job. MPEGTS в seekAndMux возвращает unsupported. FindSegments Start декодируется из recordPath filename, а не mtxi.NTP; startOffset также filename-based. Subsequent offsets с mtxi используют DTS difference. Concat mtxi требует same StreamID+consecutive SegmentNumber; legacy без mtxi — tracks ID/timescale/type и wall tolerance±1s. Output init передаёт Tracks, не UserData: экспорт теряет recorder mtxi provenance. Разрыв прерывает склейку; HTTP200/успешное открытие файла не доказывает полное окно. После начала ответа ошибка только логируется. Leading samples/negative offset не являются frame-accurate reencode trim; requested и actual decoded coverage различать.

<a id="f155"></a>

## F155 — Default useAbsoluteTimestamp:false заменяет incoming absolute time системным. True требует source absolute timestamps: ToStream пропускает packet…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L53](_WORK/W2_02.md); W2-02-F06.

**F155 DOC/CODE S033.** Default useAbsoluteTimestamp:false заменяет incoming absolute time системным. True требует source absolute timestamps: ToStream пропускает packet без PacketPTS; с true начальные packets без PacketNTP warning+skip. RTCP sender reports дают RTP/NTP pair+clock rate, но не гарантируют правильные camera clocks/эквивалентность независимых readers. Filename UTC не exposure time; event PTS нельзя сравнить с segment DTS без composition/reorder offsets.

<a id="f156"></a>

## F156 — fMP4 part сначала marshal в memory, потом Write; segment close переписывает duration header и Close. Явного File.Sync в этих функциях нет. Docs…

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L55](_WORK/W2_02.md); W2-02-F07.

**F156 CODE/DOC S033/S033/S033/S033.** fMP4 part сначала marshal в memory, потом Write; segment close переписывает duration header и Close. Явного File.Sync в этих функциях нет. Docs last-part-loss/RPO — documented normal flush цель, не проверенная power-loss guarantee на неизвестной ФС. Playback при header duration0 пытается вычислить duration из parts; это recovery primitive, не atomic snapshot растущего файла. Policy: open segment не complete, не копировать растущий original как финальное evidence. После crash complete moof+mdat prefix может стать recovered partial derivative с own hash/coverage; damaged original сохраняется. Close deadline истёк → partial/failed.

<a id="f157"></a>

## F157 — Cleaner удаляет segments по filename Start до now−deleteAfter, не учитывает incident pins/jobs/close state. Независимые native cleaner и custom…

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L57](_WORK/W2_02.md); W2-02-F08.

**F157 CODE S033.** Cleaner удаляет segments по filename Start до now−deleteAfter, не учитывает incident pins/jobs/close state. Независимые native cleaner и custom pin DB создают гонку. Выбрать одного janitor либо сохранять closed originals в отдельный evidence store до expiry. Hardlink сохраняет occupied blocks до последнего link, это не бесплатное место.

<a id="f158"></a>

## F158 — PyAV example назначает packet.stream и mux, пропускает flush packets dts=None. mux_one вызывает packet._rebase_time(output_stream.time_base),…

**Тип основания:** CODE/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032). **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L61](_WORK/W2_02.md); W2-02-F09.

**F158 CODE/INFERENCE S032.** PyAV example назначает packet.stream и mux, пропускает flush packets dts=None. mux_one вызывает packet._rebase_time(output_stream.time_base), меняя timestamps/time_base. Original values фиксировать ДО mux; один mutable Packet не передавать конкурентно decode/mux без copy/reference/lifetime strategy. Frame.pts/time_base — presentation timestamp; frame.dts — DTS packet, вызвавшего возврат frame, не надёжный identity того же image. B reorder/delay/flush нарушают 1packet=1frame. Наличие timestamps/контракта desired sampling time не доказывает mapping.

Минимальный проект — сначала H264 video-only, один профиль. Audio/VFR/H265 расширять после fixture:

1. Demux owner создаёт source_generation при open/reconnect/подтверждённой discontinuity. Packet row: packet_seq, original demux pts/dts/rational tb, codec/extradata hash, random-access, received_monotonic, gaps. RTSP demux PTS могут уже быть FFmpeg-normalized; label `ffmpeg-demux`, не raw RTP.
2. До изменения stream/mux фиксируется index. Encoded recorder создаёт recorder_generation и unique segment IDs, начинает на independently decodable IDR, закрывает на suitable IDR после target. Для decoder сохраняется separate packet ref/copy с исходной stream association. Queue overflow/mux error → recording gap; decode может продолжать, evidence partial.
3. Decode назначает decoder_generation, seq каждому yielded frame. Frame media time выводится из frame.pts×tb в source_generation, проверяется против indexed access-unit PTS/codec reorder. Не время текущего demux loop и не completion now. Duplicate/missing frame PTS → ambiguous/unknown, пока нет явной codec correlation. Flush frames тоже индексируются. Min/max span не доказывает отсутствие внутренних holes.
4. Event содержит IDs реально analyzed frames, rational times и onset uncertainty. Desired slot не evidence time. Mapping uncertainty отдельно от certainty violation.
5. Segment close: flush/trailer/bounded write; independent validation sample PTS/decode boundary/keyframe, output tb/rescale offset; hash финальных immutable bytes. Availability commit только после validation. Pending intent до публикации, после crash reconcile. Close/rename не гарантируют fsync/power-loss (K008).
6. Resolver выбирает camera+profile+source_generation, затем segments по presentation spans для [start−pre,end+post], плюс random access dependencies. Проверяет gaps/generation/codec change/coverage. Complete только при доказанном полном покрытии; partial с gaps либо unavailable/unknown mapping. Hook arrival/UTC filename для выбора не используются.

Псевдосхема manifest, не native API:

```json
{
 "camera_id":"cam1","profile_id":"main-h264","source_generation":"src-A",
 "decoder_generation":"dec-4","recorder_generation":"rec-7",
 "timestamp_domain":"ffmpeg-demux","original_time_base":[1,90000],
 "event":{"id":"ev1","frame_id":"src-A/250","pts":900000,"time_base":[1,90000],"media_interval_ns":[10000000000,10400000000]},
 "requested_media_interval_ns":[5000000000,15400000000],
 "segments":[{"id":"seg-uuid","state":"closed_validated","sha256":"computed-after-close","packet_seq_span":[100,399],"input_pts_span":[450000,1436400],"input_dts_span":[450000,1436400],"output_time_base":[1,90000],"pts_rebase_offset":-450000,"random_access_start":true}],
 "mapping":{"state":"fixture_pending","method":"same-demux-index","max_error_ns":null},
 "coverage":{"state":"pending","gaps":[],"actual_intervals_ns":[]}
}
```

Числа демонстрируют units, не полное покрытие; full index требует per-sample intervals. max_error=null значит не измерено. Rational rescale rounding/output sample grid проверяются E009.

| Случай | Обработка/граница |
|---|---|
| File loop/reset | Известный publisher loop counter либо detect discontinuity+new source_generation. Continuous PTS допустима та же timeline, simulated label обязателен. Repeated image не epoch. |
| PTS назад | B reorder отличать от reset по DTS/codec reorder; любой backwards PTS не reset автоматически. Неоднозначность → unknown/split. |
| Wrap | RTP32/container33/FFmpeg unwrapped разные domains. Не делать второй modulo unwrap без доказательства; raw domain требует modulus/clock/step trace. |
| Decoder restart | decoder_generation++, source_generation/recorder_generation могут остаться, decode gap. |
| Recorder restart | recorder_generation++, common demux source_generation может остаться; recording gap. mtxi StreamID именно об этом. |
| Missing pts/dts | Не синтезировать exact из FPS/host now; сохранить original/snapshot с unknown mapping, partial/unavailable. Synthesized clock отдельно flagged. |
| Main vs sub | MVP пишет и анализирует один профиль. Cross-profile exact unsupported до source-NTP offset/drift/marker calibration+uncertainty; bbox transform отдельно. |
| UTC step | Media time не пересортировывать по filename; new absolute mapping piece. Native filename collision тестировать; own IDs unique. |

<a id="f159"></a>

## F159 — Finite pre-roll невозможен при unbounded arrival delay. History row может прийти поздно; live state принимает только fresh same-generation;…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L102](_WORK/W2_02.md); W2-02-F10.

**F159 INFERENCE.** Finite pre-roll невозможен при unbounded arrival delay. History row может прийти поздно; live state принимает только fresh same-generation; complete evidence только при наличии actual indexed coverage в finite acceptance. Late result не возвращает удалённый original.

Проектные начальные bounds, не требования кейса/не LinQ SLA:

| Bound | Значение | Превышение |
|---|---:|---|
| A_live от frame local receipt | 2s | Reject live apply, late history; не sensor latency |
| L_evidence от самого раннего требуемого anchor до durable pin request | 20s | unavailable:late_evidence; оставшийся материал только partial |
| requested pre P / post Q | 5s / 5s | Проверить actual coverage |
| segment target S / verified IDR max gap G | 2s / ≤1s | Нет bounded G → нет close guarantee |
| close wait C после target postroll | 4s | Closed covered segments + partial:close_timeout |
| job wall deadline J | 30s | Terminal partial/failed, release temporary pins после commit |
| finite chunk window | ≤10s media | Длительный incident — серия jobs; не один unbounded job |
| ongoing manifest rollover R | 60s media | Child part того же incident, chunks независимо завершаются |
| per-incident retained media quota | 10min либо byte cap, что раньше | Stop evidence expansion; metadata incident продолжается, coverage_truncated |

L считать от EARLIEST anchor: долгий dwell означает, что start старше last analyzed frame. Можно provisional-onset заранее pin finite window; иначе старое начало partial. Postroll ждёт progress И monotonic deadline, stalled media не ждётся бесконечно. Job10s+post5+close4 помещается в J30 при bounded dispatch/validation; при превышении terminal partial. Global concurrent jobs/count/bytes также конечны, фактические caps после disk inventory.

<a id="f160"></a>

## F160 — Условный ring envelope

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L120](_WORK/W2_02.md); W2-02-F11.

**F160 INFERENCE.** Условный ring envelope:

`H >= P + L_evidence + S + G + C + maintenance_margin`.

Пример5+20+2+1+4+3=35s, выбрать H40s проектно. Условия: bounded input progress/I/O/G, mapping receipt→media проверен. Для separate recorder неизвестный offset требует дополнительной measured uncertainty. После durable admission future pin intent защищает postroll, не надо всё время расширять H на Q. Если future pins не реализованы, добавить Q/job envelope либо route не удовлетворяет контракту. Writer stall большой ring не исправляет.

`B_ring >= sum(max_bitrate_i/8 × H_i) + GOP_overshoot_bytes + open_part_buffers + FS/index_reserve`, плюс отдельный global B_evidence. Average bitrate недостаточен. Диск/битрейт неизвестны — число камер из40s не следует. Конечный byte cap имеет приоритет над обещанием полного окна.

<a id="f161"></a>

## F161 — lifecycle/low-space/recovery

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L128](_WORK/W2_02.md); W2-02-F12.

**F161 INFERENCE: lifecycle/low-space/recovery.**

1. Admission транзакционно сохраняет requested interval/generation, existing refs, finite future range, reserved bytes, deadline. DB commit failure не pin success; boundary K008.
2. pending→waiting_postroll→waiting_close→validating→complete|partial|failed|unavailable. Gaps/generation/deadline дают terminal reason. Event/notification не ждут clip.
3. Persisted pins: owner/refcount/max lifetime/bytes; terminal job передаёт finite-TTL manifest. Manual hold тоже имеет owner/expiry/cap. Shared refs dedup, quota по unique retained bytes.
4. Low space: удалить expired unpinned/temporary failed derivatives; reject new jobs/extensions; завершить pending partial по доступному coverage. Не удалять молча pinned originals. Reserve для metadata/status. При исчерпании остановить recorder с recording_unavailable:disk_full; live inference по возможности продолжить. Snapshot тоже bounded.
5. Crash: scan files↔index, open intents→recovering; hooks не источник истины. Validate hash/header/sample coverage; orphan index с unknown provenance, missing refs→partial. Stale jobs terminal по persisted deadline; tails quarantine/recover-prefix. Refcounts пересчитать из durable jobs/manifests до deletion. Process kill/reboot/power-loss/disk-loss разные guarantees; здесь не проверены.

<a id="f226"></a>

## F226 — Native export и свой minimum

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S138](SOURCES.md#s138). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_02.md:L136](_WORK/W2_02.md); дополнительная тематическая выписка.

## Native export и свой minimum

| Route | Реальное основание | Ограничение/выбор |
|---|---|---|
| MediaMTX native recorder/playback | Parts, mtxi recorder continuity, list/get MP4, hooks | Нет decoder source identity/pins/durable jobs/coverage verdict. Archive или mapped clips после gate. |
| Same-demux indexed remux | Можно удержать common packet lineage и own timestamp index | Требует packet refs/GOP/index/validation/recovery/quotas; не готовая бесплатная функция PyAV. |
| Minimal evidence после gate | Covering closed originals целиком+manifest, без reencode/blur | Longer-than-requested допустимо с actual interval. Friendly trim/download — derivative, не original provenance. |

# 08 Browser: identity, transport, render-credit и lifetime

<a id="f106"></a>

## F106 — кодек медиасервера не равен кодеку браузера

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S084](SOURCES.md#s084). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L114](_WORK/W1_05.md); W1-05-F10.

### F106 — DOC: кодек медиасервера не равен кодеку браузера

S084 предупреждает об ограниченной поддержке H265 браузерами и непригодности H264 с B-frames для WebRTC playback. Рекомендуется совместимый H264 без B-frames и Opus для звука. INFERENCE: для контролируемого демо выбрать и проверить один browser+OS+codec profile; если source несовместим — отдельная transcode ветвь для viewer. Перепаковка без reencode не исправляет B-frames. Не переносить способность RTX декодировать HEVC на browser другого ноутбука.

<a id="f107"></a>

## F107 — LL-HLS — полезный fallback с оговорками

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S033](SOURCES.md#s033). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L118](_WORK/W1_05.md); W1-05-F11.

### F107 — DOC: LL-HLS — полезный fallback с оговорками

S033 v1.21.2 HLS: default `hlsVariant: lowLatency`, minimum `hlsSegmentDuration: 1s`, `hlsPartDuration: 200ms`, `hlsSegmentCount: 7`. Документ пишет о player buffer обычно в 3 parts/segments, final segment duration зависит от IDR, count не управляет latency; TLS требуется для корректного LL-HLS на Apple devices. INFERENCE: 3×200ms=600ms — только иллюстрация part-buffer component из defaults, не end-to-end benchmark. Начало потока, GOP, decode, player и сеть добавляют задержку. Уменьшение count не является надёжной настройкой low latency.

<a id="f108"></a>

## F108 — iframe прост, собственный video нужен для синхронизации

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S085](SOURCES.md#s085). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L122](_WORK/W1_05.md); W1-05-F12.

### F108 — DOC: iframe прост, собственный video нужен для синхронизации

S085: HLS обычно имеет большую задержку, но меньше connectivity проблем, чем WebRTC. WebRTC iframe имеет query controls/muted/autoplay/playsInline, но не даёт website передавать credentials и напрямую обращаться к video tag. Документ предлагает `reader.js` и собственный `<video>` для динамических действий и auth; пример endpoint `http://mediamtx-ip:8889/mystream/whep`. INFERENCE: overlay canvas поверх чужого iframe по независимому таймеру не становится синхронным. Same-origin/модификация player могут изменить ограничения, но это отдельная интеграция, не свойство готового embed URL.

<a id="f109"></a>

## F109 — прокси должен пропускать lifecycle WHEP, а ICE media живёт отдельно

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S061](SOURCES.md#s061), [S084](SOURCES.md#s084). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L126](_WORK/W1_05.md); W1-05-F13.

### F109 — CODE: прокси должен пропускать lifecycle WHEP, а ICE media живёт отдельно

S061 код reader: OPTIONS запрашивает ICE servers в `Link`; POST `application/sdp` ожидает 201 и получает session URL из Location; PATCH `application/trickle-ice-sdpfrag`, DELETE на session URL; `#authHeader` поддерживает Basic/Bearer для начальных запросов; создаётся RTCPeerConnection, track отдаётся в callback; есть закрытие/перезапуск при ошибке. Прочитан этот код, reconnect не испытан. INFERENCE: reverse proxy должен сохранять methods, Location/Link/CORS headers и корректный session path; обычный GET-only proxy route сломает setup или cleanup. Следить за относительными/абсолютными URL после subpath proxying. Не копировать HEAD reader к произвольной старой версии сервера без smoke test.

S084 отдельно: static UDP media port по умолчанию 8189; TCP media port включается `webrtcLocalTCPAddress`; public/LAN адреса — `webrtcAdditionalHosts`; STUN и TURN задаются через `webrtcICEServers2`. Сигналинг HTTP и peer connection разные. STUN помогает обнаружить внешний адрес/пробить подходящий NAT, TURN ретранслирует media. Если UDP закрыт, возможен TCP/relay, но затраты/задержка и доступность не измерены. На demo network проверять реальный selected candidate pair, а не только HTTP 200.

<a id="f110"></a>

## F110 — go2rtc как альтернатива и ограничения доверия README

**Тип основания:** CLAIM/DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S062](SOURCES.md#s062). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L132](_WORK/W1_05.md); W1-05-F14.

### F110 — DOC/CLAIM: go2rtc как альтернатива и ограничения доверия README

S062 говорит, что go2rtc WebRTC media идут напрямую browser↔go2rtc, HTTP reverse proxies участвуют в установлении; default listener `:8555` TCP/UDP, кандидаты можно задавать вручную, TURN доступен. В config filters указано исключение Docker-like 172.16.0.0/12 candidates. README содержит «примерно 20% пользователей» с проблемой symmetric NAT — это CLAIM автора без методики/выборки, не пригодный коэффициент надёжности нашей сети. Там же есть широкое утверждение о непригодности UDP для 2K/4K через интернет — не принимать как универсальный технический запрет; конкретную потерю/bitrate проверять.

<a id="f111"></a>

## F111 — статус WHEP нельзя брать из случайного старого README

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S062](SOURCES.md#s062), [S094](SOURCES.md#s094). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L136](_WORK/W1_05.md); W1-05-F15.

### F111 — DOC: статус WHEP нельзя брать из случайного старого README

S062 называет старый WHEP заменённым WISH standard; это неточная формулировка, а WISH — рабочая группа/процесс. S094 на дату доступа показывает `draft-ietf-wish-whep-05`, active Internet-Draft, intended Proposed Standard. Использовать WHEP как реализованный media-server endpoint, привязанный к версии сервера/reader, не обещать полную совместимость с финальным RFC. Этот отрицательный результат меняет обещания в technical delivery, но не запрещает MediaMTX reader.

<a id="f112"></a>

## F112 — MJPEG требует MJPEG source или transcoding

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S062](SOURCES.md#s062). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L140](_WORK/W1_05.md); W1-05-F16.

### F112 — DOC: MJPEG требует MJPEG source или transcoding

S062: `/api/stream.mjpeg?src=...` и `/api/frame.jpeg?src=...` работают с MJPEG codec в source; H264/H265 нужно конвертировать через FFmpeg. INFERENCE: MJPEG не бесплатный wrapper над camera H264. Он прост для debug и server-burned boxes, но bandwidth proportional JPEG_bytes×FPS, нет эффективного межкадрового сжатия. Стандартный `<img src=...mjpeg>` не даёт приложению надёжного frame_id per displayed image; лучше собственный framed transport, если нужна точная связь metadata.

<a id="f113"></a>

## F113 — WebSocket transport может означать очень разные вещи

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S062](SOURCES.md#s062). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L144](_WORK/W1_05.md); W1-05-F17.

### F113 — DOC: WebSocket transport может означать очень разные вещи

S062 `/api/ws?src=...`: WebRTC SDP/candidates через JSON, MSE через `type:mse` с codec list, HLS playlist message, MJPEG `type:mjpeg`. INFERENCE: «видео по WS» надо расшифровывать: signaling-only WebRTC, fMP4/MSE, JPEG frames — разные buffering, codecs и sync. Для нашего простого JPEG протокола не приписывать go2rtc автоматическую передачу custom `frame_id`/LinQ results: это наша работа.

| Вариант | Когда брать в 45 часов | Главная цена/риск | Что честно показывать |
|---|---|---|---|
| WebRTC + MediaMTX native video | Нужен плавный original live, есть проверенная сеть | ICE/codec + доказанная timestamp mapping для overlay | original video; delayed analytics отдельно, пока mapping не проверена |
| WebRTC + go2rtc | Команда уже знает go2rtc/Frigate | Похожие NAT ограничения, другие ports/API | Та же честность; не выбирать два медиасервера одновременно без причины |
| HLS/LL-HLS | WebRTC не проходит firewall/proxy, нужен HTTP-only route | Больше буферизации; версии player и codec compatibility | Явная live delay и timestamp |
| HTTP MJPEG с server boxes | Один-два небольших debug вида | JPEG encode/bandwidth; `<img>` sync limitations | Кадр уже содержит собственные результаты |
| WebSocket JPEG+metadata envelope | Нужна быстрая faithful analyzed view | Частота/размер ограничены, очередь может накапливаться | FPS и age анализируемых кадров, не «25 FPS inference» из camera FPS |
| Server annotated H264 | Нужны плавный поток и burned-in boxes | Encode и необходимость ждать результатов/сопоставлять кадры | Processed delayed video, original отдельно |

<a id="f114"></a>

## F114 — requestVideoFrameCallback помогает, но не создаёт frame correspondence

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S086](SOURCES.md#s086). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L157](_WORK/W1_05.md); W1-05-F18.

### F114 — DOC: requestVideoFrameCallback помогает, но не создаёт frame correspondence

S086 §1/§2.2: callback при кадре, переданном compositor; best effort, иногда на один v-sync позднее, под нагрузкой кадры пропускаются. `mediaTime` — presentation timestamp в секундах media timeline, для live/WebRTC MAY быть нулём; `rtpTimestamp` SHOULD присутствовать для received WebRTC, не обязательно; `captureTime` — оценка с синхронизацией часов, не достоверные UTC часы камеры. `presentedFrames` даёт счётчик compositor frames, не camera frame ID. INFERENCE: нельзя использовать `Date.now()` результата как timestamp картинки или считать rVFC гарантией каждого кадра. Проверять feature/field availability на реальном браузере; callback обслуживать заново на каждый кадр. Не подменять mediaTime настенными миллисекундами.

<a id="f115"></a>

## F115 — relay может менять абсолютную шкалу времени

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S087](SOURCES.md#s087). **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L161](_WORK/W1_05.md); W1-05-F19.

### F115 — DOC: relay может менять абсолютную шкалу времени

S087: MediaMTX принимает/выдаёт absolute timestamps для RTSP/HLS/WebRTC, но по умолчанию заменяет входные absolute timestamps системными; `useAbsoluteTimestamp` позволяет сохранить входные. HLS использует EXT-X-PROGRAM-DATE-TIME; RTSP/WebRTC — RTCP SR c reference NTP/RTP. Формула документа: `frame_abs = ref_ntp + (frame_rtp-ref_rtp)/clock_rate`, seconds. INFERENCE: RTP timestamp — относительный счётчик с wrap/session semantics; один timestamp без SSRC/epoch/clock rate недостаточен. Даже включение preserve absolute timestamp не доказывает точные камеры UTC и соответствие с кадрами другой decoder branch.

<a id="f116"></a>

## F116 — минимальный контракт идентичности и геометрии

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S135](SOURCES.md#s135). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_05.md:L165](_WORK/W1_05.md); W1-05-F20.

### F116 — INFERENCE: минимальный контракт идентичности и геометрии

Рекомендуемый envelope (проект): `camera_id`, `source_stream_id`, `stream_epoch`, `frame_id`, `source_pts`, `source_time_base_num/den`, `source_capture_utc` nullable + provenance/uncertainty, `ingest_monotonic_ns` на конкретном host, `source_width/height`, crop/rotation/flip, resize scale и letterbox padding, модель/version, bbox coordinate space, `result_ready_monotonic_ns`, inference backend и trace/request ID. `frame_id` выдаёт ingest один раз; результаты сохраняют его неизменным; при reconnect новая epoch. Backend LinQ не подменяется другим незаметно.

Согласовано с полученной соседней ветвью: [W1_03.md](_WORK/W1_03.md), F057 и разделы scheduling/request metadata, прочитанные 2026-10-23. Её async adapter сохраняет ту же identity/transform и отдельный remaining freshness budget. Просроченный результат допустимо оставить для offline evidence с признаком stale, но нельзя применять как свежее состояние. Это локальное чтение работы соседа, не независимое сетевое подтверждение. Архивирование encoded source и пропуск inference frame разделены: latest-frame scheduling не должно уничтожать доказательство.

Точное совпадение:

* В JPEG+metadata WS один binary message содержит length/header + JPEG + detections того же `frame_id` (или пара сообщений с явным pair ID и bounded assembler). Рисовать image и boxes в один canvas pass после decode обоих; старый async JPEG decode не должен перезаписать более новый кадр. Бounded mailbox и drop policy избегают возрастающей задержки. Если нужно сохранить все inference results, сохранять их отдельно от live mailbox.
* В WebRTC original path нужно получить и проверить mapping source PTS/frame_id → outgoing RTP timestamp/SSRC/epoch → rVFC metadata. Mediator/reencode может сменить шкалу и frames. Совпадение «ближайшее время» допустимо только с объявленным max skew и метрикой; stale metadata скрывать/помечать. Результат, пришедший после показа source frame, нельзя наложить на уже прошедший кадр без задержки видео/повторного просмотра.
* Если camera 25 FPS, inference 5 FPS, не растягивать один box на все промежуточные кадры как measured result. Tracking/interpolation должны быть названы отдельно и иметь свой timestamp/age.

Геометрия: для letterbox `r=min(Wnet/Wsrc,Hnet/Hsrc)`, offsets `px,py` фактически применённого preprocess; `x_src=(x_net-px)/r`, `y_src=(y_net-py)/r`. Для viewport `object-fit:contain`, `s=min(Wcss/Wsrc,Hcss/Hsrc)`, `ox=(Wcss-sWsrc)/2`, `oy=(Hcss-sHsrc)/2`; `x_css=ox+s*x_src`, `y_css=oy+s*y_src`. Для `cover` вместо min — max, появляются обрезки. Crop offset, rotation, flips, pixel aspect ratio и DPR canvas учитывать явно; хранить применённую transform matrix и inverse, а не восстанавливать её из предположений. Формулы предполагают стандартные square pixels/отсутствие дополнительных transforms. Между sub/main одинаковое отношение размеров не гарантирует одинаковый FOV.

<a id="f162"></a>

## F162 — send completion означает flow-control completion, не render

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S113](SOURCES.md#s113). **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L31](_WORK/W2_03.md); W2-03-F01.

### F162 — CODE: send completion означает flow-control completion, не render

S113: bytes идут через `protocol.send_binary`, затем `send_context` вызывает `send_data`→`transport.write` и `await drain()`. `drain` ждёт только когда transport paused; иначе может завершиться сразу. `connection_made` передаёт write watermarks transport. Это подтверждает ограниченное backpressure, но не получение сообщения renderer и не пустые TCP/UA buffers. Write watermark допускает запись сообщения целиком до ожидания; `write_limit=32768` не запрещает один payload 512KiB. Не использовать `send` как ACK и не измерять по нему «browser latency». S113 отдельно описывает OS TCP buffers; их размер не равен write_limit.

<a id="f163"></a>

## F163 — directions лимитов различны

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S113](SOURCES.md#s113). **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L35](_WORK/W2_03.md); W2-03-F02.

### F163 — DOC/CODE: directions лимитов различны

S113 задаёт incoming `max_size`, receive-frame high/low `max_queue`, write watermarks, open/ping/close timeouts. Они не устанавливают outgoing image cap; его проверяет наше приложение. S113/S113: `broadcast()` не применяет send backpressure; наивная общая последовательная отправка блокирует быстрых медленным, task-per-frame может копить задачи. Поэтому выбираем отдельный долговечный sender/viewer, без `broadcast`, и общий immutable latest/camera. Клиентские control messages малы; pixel payload только server→client.

<a id="f164"></a>

## F164 — close, timeout и ping — разные сигналы

**Тип основания:** DOC/CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S113](SOURCES.md#s113). **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L39](_WORK/W2_03.md); W2-03-F03.

### F164 — DOC/CODE: close, timeout и ping — разные сигналы

S113 `close()` ждёт handshake/TCP termination; `send` cancellation discouraged, вместо неё рекомендовано close. На закрытом соединении recv/send дают ConnectionClosed; один receiver должен собирать control messages. Ping/Pong проверяет WS peer/network, а не JS decode/canvas. Browser network stack может отвечать Pong при зависшем renderer.

Важная ограничивающая CODE находка: `send_context`859+ вызывает `await drain`914 до блока `asyncio.timeout_at(close_deadline)`941+. Значит только чтения источника недостаточно, чтобы обещать жёсткое время полного teardown при полностью заблокированном transport. Это не заявленная воспроизведённая ошибка и не доказательство вечного hang: E012 обязан проверить сочетание ОС/TLS/прокси/event loop. `close_timeout` оставляем finite, но не называем wall-clock hard cap всех ресурсов. Не делать бесконечные reconnect/new send tasks после истечения этого срока.

<a id="f165"></a>

## F165 — browser API не даёт incoming queue gauge

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S089](SOURCES.md#s089), [S114](SOURCES.md#s114), [S115](SOURCES.md#s115). **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L45](_WORK/W2_03.md); W2-03-F04.

### F165 — DOC: browser API не даёт incoming queue gauge

S089 `bufferedAmount` относится к bytes из browser `send`, исключает часть нижних buffers; входящие WS messages создают tasks. Поэтому browser `bufferedAmount=0` не доказывает отсутствие очереди JPEG. S114 даёт async bitmap decode, bitmap close и transfer; ни одно не заменяет serial state в приложении. ACK после canvas draw является договорённостью нашего renderer, не доказательством физического scanout/прочтения человеком. S115 visibility позволяет приостановить view, но hidden/visible не равно operator awareness.

<a id="f166"></a>

## F166 — один конкретный route для45ч

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L49](_WORK/W2_03.md); W2-03-F05.

## F166 — INFERENCE: один конкретный route для45ч

Выбран **standalone `websockets.asyncio.server.serve`** в том же Python service/event loop, где живёт processed-view projection. Один публичный WSS path `/view/v1`, handler проверяет `ws.request.path`; camera selection в bounded HELLO, не создание dynamic route/task на каждую камеру. Этот route не требует ASGI/FastAPI/Starlette/Uvicorn или Werkzeug routing extras. HTTP static UI/history/event APIs могут обслуживаться уже выбранным приложением; данный выбор не навязывает второй HTTP framework. Reverse proxy, если он нужен, обязан поддерживать Upgrade и finite connection/admission limits; конкретный proxy здесь не выбран.

Prospective config, не runnable implementation:

```python
from websockets.asyncio.server import serve

# handler/auth/renderer/projection не реализованы этим research.
async with serve(
    handler, host, port,
    origins=[ui_origin], subprotocols=["processed-view.v1"],
    compression=None,
    max_size=4096, max_queue=(4, 1), write_limit=(32768, 8192),
    open_timeout=5, ping_interval=20, ping_timeout=10, close_timeout=2,
):
    await stop_event.wait()
```

`compression=None`: JPEG уже сжат, WS deflate здесь лишний state/CPU. Указанные watermarks — настройка early backpressure, не hard RSS limit. `max_size=4096` ограничивает incoming HELLO/ACK, не JPEG. Application дополнительно ограничивает control rate, schema/key lengths, active/closing connection count, viewing sessions per authenticated user и global outbound bytes/s. Origin allowlist не заменяет authentication/camera authorization. Login/cookies проверяются до подписки; camera credentials в HELLO/URL не попадают.

Исходные проектные caps для fixture: envelope≤512KiB, metadata≤16KiB, JPEG≤496KiB; width≤1280, height≤720, pixels≤921600; bbox count≤200; one camera/tile и максимум4 tiles/page; максимум3 simultaneously admitted viewer connections для smoke. Это настройка демонстрационного профиля; если нужная деталь/quality не помещается, выбрать иной разрешённый профиль/снизить view FPS/число tiles, или показать `view_unavailable:size_cap`, не бесконечно повышать cap. Analytics JPEG/preprocess quality — отдельный evaluation contract; view resize не должен менять inference input.

Все permissions/admission и latest cache операции сериализуются одним owner/event loop. Encode делается один раз на accepted analyzed frame, не на каждого viewer. Сам encoder job имеет bounded slot/count/bytes; task-per-result до semaphore недопустим. Медленный viewer не владеет raw кадром камеры.

<a id="f167"></a>

## F167 — wire contract и state machine

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S113](SOURCES.md#s113), [S116](SOURCES.md#s116). **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L75](_WORK/W2_03.md); W2-03-F06.

## F167 — INFERENCE: wire contract и state machine

Один binary WS message: `[u32 big-endian header_bytes][bounded UTF8 JSON header][JPEG]`. Проверять total length, exact JPEG length и header schema до decode; не split JSON/JPEG на независимые сообщения. Никакого base64. JSON uint64 IDs представлены decimal strings во избежание JS Number precision loss. Содержимое header:

```json
{
  "v":1, "view_epoch":"new-uuid-per-connection",
  "delivery_seq":"7", "credit_nonce":"unpredictable-per-send",
  "camera_id":"cam-01", "stream_epoch":"source-generation",
  "frame_id":"1042", "media_time_ns":"41680000000",
  "jpeg_bytes":123456, "width":1280, "height":720,
  "geometry_revision":"transform-hash", "bbox_space":"jpeg_pixels",
  "boxes":[], "analysis_backend":"linq-or-honest-other",
  "server_age_at_send_ms":132, "server_clock_domain":"ingest-run-uuid",
  "source_capture_utc":null, "capture_uncertainty_ms":null
}
```

`analysis_backend=linq` только при настоящем execution evidence из adapter. `frame_id`/`stream_epoch` — source identity; `view_epoch`/`delivery_seq` — доставка этому connection. `credit_nonce` не auth token, нужен для строгого matching и затруднения ACK ещё не полученного message. Source epoch reset не меняет identity старого outstanding delivery: следующий send выбирает только новый valid source epoch; старый нельзя применить к новой camera session.

Состояния viewer owner:

| State | Разрешённое действие / переход | Что нельзя делать |
|---|---|---|
| NEW | Бounded HELLO/auth/profile/subscription за5s; server назначает view_epoch; один initial READY | Никаких изображений до допуска; repeated READY не создаёт credits |
| READY | Когда есть новый latest и rate budget, проверить freshness/size; атомарно записать outstanding key/deadline, перейти SENDING и вызвать ровно один send task | Нельзя взять второй frame или создать waiting tasks |
| SENDING | Await send с отдельным watchdog; ACK receiver работает одновременно. Early valid ACK можно запомнить как boolean | ACK не разрешает второй send, пока первый send ещё pending; timers не запускают replacement send |
| WAIT_ACK | send завершён; deadline от времени admission/send-start продолжает идти; точный ACK→READY | send complete не меняет credit; ACK timeout не возвращает READY |
| CLOSING | При send deadline/ACK deadline/hidden/error перейти terminal, invalidate generation, инициировать close; счётчик connection остаётся занят до cleanup | Ни поздний ACK, ни latest arrival не возобновляют connection |
| CLOSED | finally снять подписку/refs, завершить принадлежащие connection tasks, записать reason; новый connection получает новый epoch | Нельзя вернуть старый credit/cursor в новый connection |

ACK: `{"v":1,"type":"rendered","view_epoch":"…","delivery_seq":"7","credit_nonce":"…","camera_id":"cam-01","stream_epoch":"…","frame_id":"1042"}`. Сервер принимает только exact currently outstanding key и только неистёкший deadline в SENDING/WAIT_ACK. Duplicate, future, wrong nonce, old epoch, unsolicited ACK не увеличивают credit; логируются/rate limited, систематические нарушения закрывают connection. Receiver не доверяет присланным counts/timestamps/memory claims. Matching/transition и таймер не гоняются разными несериализованными owner tasks.

Проектные сроки: send_progress deadline1s, render-ACK overall deadline2s от начала send, закрытие grace2s. Значения надо настроить по E011/E012; медленная разрешённая сеть может требовать иной профиль. Watchdog при первом deadline делает connection terminal и вызывает `close`; **не** `wait_for(send)` с автоматическим cancel и повтором в том же WS. `asyncio.wait`/shield или самостоятельный tracked send task позволяет не отменить send из-за deadline автоматически. В finally все задачи учтены и наблюдаются; исключения не теряются.

Если public close не завершился за grace: connection остаётся closing и учитывается в admission cap; не продолжать расширение списка таких connections. Видимый stale/connection failure и bounded отказ новым viewer предпочтительнее скрытого неограниченного накопления. Такой policy ограничивает наши новые allocations; hard release transport требует E012. Experimental option отдельно: public `create_connection` factory→узкий pinned `ServerConnection` subclass, сохранить passed asyncio transport в override `connection_made`, hard teardown через documented asyncio WriteTransport.abort. Это **не public websockets abort API**, требует code-level coupling/test/ownership review, не часть обязательного45ч minimum. Source S113/S116 подтверждает механизм, но не выполнение/безопасность на нашем стенде.

<a id="f168"></a>

## F168 — почему протокол bounded и где кончается доказательство

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L112](_WORK/W2_03.md); W2-03-F07.

## F168 — INFERENCE: почему протокол bounded и где кончается доказательство

Пусть B — envelope cap, J≤B — JPEG cap, V — active+closing admitted connections, C — subscribed cameras. READY→SENDING единственный переход, создающий image send; outstanding устанавливается до вызова. Ни send completion, ни timeout не добавляют credit. Единственный ACK привязан к одному key; send_done AND ack_valid нужны одновременно для READY. Поэтому для каждого connection не больше1 ещё не ACKed image message, включая queued transport/browser bytes этого изображения. За интервал renderer pause сервер может положить в поток не больше одного нового B, затем замолчит/закроется. Это существенное отличие от mailbox1 с непрерывным drain/send.

Server app live image refs: до C shared latest JPEG slots + V distinct historical outstanding payloads + bounded encoding/result admission slots. При грубом учёте immutable bytes без sharing ≤(C+V)B плюс metadata/copies/encoder scratch. Если full binary envelope создаётся отдельно для каждого view_epoch/nonce, это до ещё V×B копий; выбрать сборку одного bounded bytes и явно учесть её. Нельзя называть `(C+V)B` process RSS: сериализация WS/TLS, transport, OS, Python allocator и codec scratch добавляются. Incoming receive max_queue — high watermark, возможно overshoot parsed frames из одной read; controls малы, malformed/flood ограничены admission/rate/global resource policy и E.

Browser honest implementation: не больше1 decoding/awaiting draw frame, плюс текущее canvas и bounded message/JPEG buffers. Main canvas и один bitmap при RGBA8 требуют номинально до `2×W×H×4` bytes (~7.37MB при1280×720), плюс encoded buffers/UA/decoder/GPU copies; это арифметика representation, не hard browser RSS. Canvas backing dimension также ограничен, DPR/UI resize не создаёт неограниченный canvas. Никакого frame history/Promise.all, каждый bitmap закрывается. Физический memory cap браузерного процесса стандартом не предоставлен.

**Попытка опровержения:** злой клиент ACK immediately-on-receive способен лгать о render. Одно credit без server-side max FPS/byte rate тогда не ограничит накопление в его собственном renderer. Протокол не доказывает render у недоверенного клиента. Поэтому server caps outbound rate/connection count остаются нужны, ACK является telemetry/frontend contract, не evidence операторского просмотра. Future/precomputed ACK не credit благодаря nonce/key; ACK после получения может лгать, это принципиально не устраняется nonce. Для доверенного frontend успех E011 подтверждает serial implementation, не противодействие всем client modifications.

Другой контрпример: reconnect быстрее завершения старого decode создаёт новые decoder jobs. Поэтому browser имеет один lifecycle controller **через поколения connections**, а server admission учитывает closing connections. Не сбрасывать busy на onclose до завершения старого decode; новое подключение/initial READY разрешить только после его cleanup. Если decode бесконечно не завершается — view unavailable/reload, не бесконечное создание новых decoders.

<a id="f169"></a>

## F169 — browser renderer, hidden и resync

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L124](_WORK/W2_03.md); W2-03-F08.

## F169 — INFERENCE: browser renderer, hidden и resync

Minimum frontend без worker/package: `binaryType="arraybuffer"`; единый synchronous `onmessage` проверяет generation, cap и busy **до первого await**, затем ставит busy. `async onmessage` без явного busy mutex неверен: event dispatcher не ждёт предыдущий Promise. Неожиданный второй image при busy — protocol violation/close, а не ещё один decode.

Последовательность: validate envelope/limits → один `createImageBitmap(Blob(jpeg))` → проверить bitmap dimensions, generation/visibility → один rAF callback → снова проверить generation/visibility → clear/drawImage и boxes того же envelope в одном canvas callback → `bitmap.close()` в finally → очистить compressed refs/busy → отправить один ACK только если draw завершён и connection всё ещё тот же/OPEN. Canvas coordinates используют bbox_space/transform_revision; source boxes не предполагаются уже JPEG-space. Если metadata уже превышает box cap — отклонить на сервере, не создавать огромный JSON.

До decode сервер гарантирует image profile; length header сам по себе не защищает от JPEG с огромными внутренними dimensions. Для недоверенного JPEG endpoint понадобилась бы валидация JPEG dimensions до decode; наш сервер отправляет только собственный bounded encoder output из trusted admitted frames. После decode dimension mismatch закрывает view и показывает ошибку. Это отдельная граница trust, не обещание защитить любой browser от произвольного JPEG.

Ошибки decode/draw не подтверждаются rendered; close/resync, видимый failure. При source epoch switch/old generation resolving bitmap закрыть без draw/ACK. rAF callback handles не копить; при hide отменить ожидающий rAF и cleanup bitmap. Потребляемая canvas snapshot stale до нового кадра; overlay age продолжает возрастать.

`visibilitychange`→hidden: invalidate local render generation, не ACK pretend-rendered, остановить подписку/закрыть view. Если сообщение hidden не дошло или JS заморожен, серверный ACK deadline всё равно останавливает дальнейшие изображения; Ping/Pong этого не заменяет. На visible: дождаться старого decode cleanup, новый WS/view_epoch и initial READY; server выбирает только current latest подходящего возраста/epoch, не сохранённый cursor. После длительной паузы incident history грузится отдельно из durable API, не replay JPEG.

**Защита от позднего TCP кадра до close event:** контроллер хранит `credit_issued_local_ms=performance.now()` непосредственно перед отправкой initial READY и затем каждого valid rendered ACK, который даёт разрешение следующему send. Это начало очередного client credit cycle. Следующий кадр этого connection не мог быть отправлен раньше, чем сервер получил этот credit. На receive и ещё раз непосредственно перед canvas draw проверить `now_local-credit_issued_local_ms≤T_cycle` (например2s fixture). При нарушении не рисовать, закрыть view/resync. JS timer сам может запоздать при заморозке, поэтому обязательна проверка elapsed после возобновления, не только setTimeout callback. Не обнулять cycle timer при receive/decode. При отсутствии свежих кадров цикл тоже истекает: это намеренное `no_fresh_frame` с backoff, а не тихое удержание статуса live. Дубликаты/незапрошенные messages не обновляют начало cycle. Ограничение относится к честному frontend; malicious client не обязан исполнять его.

Worker — optional perf experiment, не mandatory route. Если нужен decode в DedicatedWorker, отправлять один transferred ArrayBuffer, максимум один busy decode и один transferred bitmap; main ACK только после своего draw, не по worker message `decoded`. Не создавать worker/postMessage на каждый кадр. Old worker/generation результаты не рисуются. Terminate/recreate worker — отдельный E: стандарт API не обещает мгновенное освобождение process RSS/codec allocation. Не выдавать перенос decode в worker за устранение browser backlog.

<a id="f170"></a>

## F170 — retained source frame ≠ retained viewer JPEG

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L140](_WORK/W2_03.md); W2-03-F09.

## F170 — INFERENCE: retained source frame ≠ retained viewer JPEG

| Владение | Когда нужно изображение | Release / late policy |
|---|---|---|
| Decoder latest raw slot | До admission либо замены свежим кадром | Перезапись только когда нет consumer lease; иначе immutable copy/другой bounded slot |
| Remote input operation | До доказанного окончания использования локальных bytes/native buffer | Python timeout future сам по себе не освобождает native borrow. SDK/API release/copy contract UNKNOWN; см.W2_01/K001 |
| Retained source для processed view | Пока ждём result, чтобы JPEG и bbox относились к исходному кадру | Один immutable source representation/request, count+byte cap+TTL. Не сохранять на каждый viewer |
| Processed accepted result | JPEG+own-frame boxes, latest/camera и existing view outstanding | Raw source можно отпустить после encode; viewer ACK держит JPEG, не raw ndarray |
| Timed-out/obsolete result | Для live view больше не нужен | Удалить retained-view bytes/reference по TTL, оставить маленький tombstone/key ledger; поздний result drop/metadata-only, никогда bbox поверх current frame |
| Evidence | Encoded recorder/manifest/pins | Не зависит от ACK/view drop; другой retention lifecycle W2_02 |

Удерживать full raw frame до результата не всегда обязательно: при admission можно сохранить ограниченный view JPEG/thumbnail исходного кадра и geometry, отдельно отправить требуемый tensor/jpeg в LinQ. Это снижает retention, но snapshot profile не становится inference input profile. Если view должен иметь точно те же pixels, которые дал detector, сохранить нужное представление и transform; thumbnail не объявлять original evidence. Повторно читать «текущий» frame после delayed result запрещено.

Raw retained budget `R_view≤N_pending×S_view_cap`; например RGB1080p=6,220,800 bytes/frame до allocator/copies, ×8inflight≈49.77MB. При JPEG retention cap512KiB ×8≈4MiB encoded, но decode/encode/input tensors отдельно. Это LOCAL arithmetic/INFERENCE, не измерение LinQ. Native borrowed input lifetime — отдельный `R_input_borrowed` член, его нельзя снять вместе с view TTL. Если SDK не устанавливает safe buffer release при timeout, bounded count сохраняется до terminal/reconcile, либо выбрать доказанный copying API/process isolation; нельзя возвращать shared-memory slot сразу после timeout. Аналогичные Hailo требования W1 не устанавливают контракт LinQ.

Отдельные счётчики: decoded, analytics_admitted, analytics_latest_replaced, remote_timeout, result_late_or_epoch_reject, retained_view_bytes/current/peak, borrowed_input_bytes/current/unknown_terminal; processed_frames_available; **per viewer** frames_sent, rendered_ack, latest_skipped, size_reject, send_deadline, ack_deadline, hidden_disconnect, late_ack, connection_closing_age. `latest_skipped` этого viewer — разность processed available/selected, не потеря inference и не отсутствие violations. Drop просмотра не ухудшает persisted incidents/evidence; analytics drop меняет coverage/quality и учитывается отдельно.

<a id="f171"></a>

## F171 — age без ложной общей шкалы

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S139](SOURCES.md#s139). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_03.md:L157](_WORK/W2_03.md); W2-03-F10.

## F171 — INFERENCE: age без ложной общей шкалы

Если ingest и view sender в одном clock domain, `server_age_at_send_ms=(send_start_mono-ingest_frame_mono)/1e6`: возраст с ingest/decode на нашем host до send, не exposure→screen. Если ingest другой host, не вычитать его monotonic из sender monotonic; поле nullable или называть `projection_age`, явно указав меньший участок. Durations inference/input-server stages каждый маркируются clock_domain. `media_time_ns` нужен для source ordering, не вычитается из browser performance.now.

Browser измеряет `decode_ms`, `receive_to_draw_ms` и `since_last_draw_ms` своим performance.now. Сервер измеряет `send_start_to_valid_ack_ms` своим monotonic, включает сеть/renderer/обратный путь и не равен one-way display lag. `server_age_at_send_ms + browser_receive_to_draw_ms` — лишь нижняя оценка участков с отсутствующей сетью, не честный end-to-end timestamp. Не подписывать её total age. Можно показывать «server age at send:132ms; rendered locally:…; transport age unknown».

Полезная проверяемая bound по ACK: на момент получения валидного честного ACK на сервере `now_server-ingest_server` — верхняя оценка возраста при уже завершённом canvas draw, если ingest тот же clock domain и тот же frame. Это telemetry после факта, не guarantee следующего кадра и не sensor age. Для live порога sender отбрасывает latest, уже старше T_fresh_server; renderer отдельно закрывает view по local credit-cycle budget из F169. Можно получить консервативную оценку без cross-host subtraction: `ingest_to_draw_upper_ms = server_age_at_send_ms + (draw_local_ms-credit_issued_local_ms)`, поскольку send_start следует за получением credit и local cycle duration включает весь участок send_start→draw (плюс ожидание credit/server/latest). Предполагаются корректные duration clocks с известной единицей/при необходимости запасом на drift; ingest и sender обязаны иметь один clock domain. Проверка непосредственно перед draw `upper≤T_display` может переотбрасывать нормальные кадры из-за ожидания latest, но не скрывает неизвестный transit за точной цифрой. Эта оценка не даёт exposure age, не является measured one-way latency и не ограничивает delay физического compositor после callback. При unknown server_age поле upper тоже unknown. Source UTC и uncertainty показывать только при доказанном camera mapping из W2_02; иначе null.

# 09 Resilience, measurement и интерпретация benchmark

<a id="f123"></a>

## F123 — MEASURED (измерил NVIDIA), DeepStream 7.1 T4

**Тип основания:** MEASURED. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S095](SOURCES.md#s095). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L35](_WORK/W1_06.md); W1-06-F01.

### F123 — MEASURED (измерил NVIDIA), DeepStream 7.1 T4

S095, точные разделы в реестре. CPU dual Intel Xeon E5-2650 v4 2.20 GHz, 48 threads; Tesla T4, GPU clock 1513 MHz; RAM `360448Mb (22x16384) DDR42666, 2400MHz` (единица сохранена как у автора). Ubuntu 22.04, driver 535.161.08, CUDA 12.2, TensorRT 8.6.1.6. Конфиг `source4_1080p_dec_infer-resnet_tracker_sgie_tiled_display_int8.txt`; N потоков sample_1080p_h265.mp4 либо sample_1080p_h264.mp4, 1080p30. PGIE `resnet18_trafficcamnet_pruned.onnx`, batch=N, interval=0; IOU tracker 960×544; две SGIE ResNet18 VehicleTypes/VehicleMake 224×224, batch32, asynchronous. Tiler/rendering/OSD отключены. Опубликовано 45 H.265 потоков (CPU51.81%, GPU100%) и 31 H.264 (CPU2.72%, GPU61.23%).

**INFERENCE:** это throughput всего указанного headless-конвейера, не чистая latency модели; 45×30=1350 и31×30=930 aggregate processed FPS нельзя объявлять обслуживанием наших правил. Таблица не даёт WAN, реальных RTSP камер, браузера, notification latency, p95/p99, длительности опыта, распределения объектов, серийных сбоев. Даже достаточно подробный vendor benchmark имеет эти пробелы; сохранять их. Не масштабировать эти числа по TOPS на LinQ. Дополнительные PeopleNet/YOLO таблицы прочитаны, но для задачи достаточно полного T4 протокола.

<a id="f124"></a>

## F124 — DOC VMS sizing

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S096](SOURCES.md#s096). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L45](_WORK/W1_06.md); W1-06-F03.

### F124 — DOC VMS sizing

S096: Milestone допускает все компоненты на одном сервере при достаточном железе; 50–100 камер **depending on hardware and configuration** могут работать на одном сервере. Для >100 рекомендует выделенные серверы для всех или части компонентов; архитектура разделяет задачи для тысяч камер/нескольких площадок. **INFERENCE:** 50 не повод автоматически разворачивать кластер, а500 — повод делить ingest/recording/compute по площадкам и узлам. Этот совет не содержит стоимости LinQ inference и не разрешает обещать 500 на одном устройстве. У числа камер должен быть профиль нагрузки.

<a id="f125"></a>

## F125 — DOC glass-to-glass

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S097](SOURCES.md#s097). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L49](_WORK/W1_06.md); W1-06-F04.

### F125 — DOC glass-to-glass

S097 определяет sensor-to-screen как от захвата кадра до показа этого кадра. §3 предлагает камеру направить на собственный экран с timestamp overlay (`%T:%f`) и сравнить прямой/loop timestamps; ошибка до frame interval, при25 FPS это40ms, при1 FPS метод груб. §4 разбирает camera/network/client contributions, клиентская буферизация способна доминировать. **INFERENCE:** loop-тест даёт видео latency, не время от нарушения до тревоги. Нужен отдельный журнал event onset и UI alarm; оба endpoint должны быть определены.

<a id="f126"></a>

## F126 — DOC clocks

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S098](SOURCES.md#s098). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L53](_WORK/W1_06.md); W1-06-F05.

### F126 — DOC clocks

S098: monotonic не идёт назад и не меняется от установки системного времени; reference point undefined, валидны разности. `perf_counter` включает sleep и подходит коротким duration; `_ns` избегает float precision loss. Windows implementation monotonic — QueryPerformanceCounter. **INFERENCE:** локальные этапы измерять monotonic_ns; UTC хранить для корреляции, а не вычитать как гарантированную latency между хостами. Нельзя вычитать monotonic разных компьютеров. Process CPU-time не wall latency.

<a id="f127"></a>

## F127 — DOC quantiles

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S099](SOURCES.md#s099). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L57](_WORK/W1_06.md); W1-06-F06.

### F127 — DOC quantiles

S099: summary заранее вычисляет quantiles, которые нельзя агрегировать как общую quantile нескольких workers; histogram сохраняет распределение/счётчики бакетов для объединения. Count+sum позволяют среднее. **INFERENCE:** не усреднять p95 камер/воркеров. Для суммарного p95 объединить сырые durations либо совместимые histograms, а per-camera p95 оставить отдельной метрикой fairness. Приближённые histogram quantiles подписывать, границы бакетов выбирать возле SLA.

<a id="f128"></a>

## F128 — DOC patterns и ограничение circuit breaker

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S100](SOURCES.md#s100), [S101](SOURCES.md#s101). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L61](_WORK/W1_06.md); W1-06-F07, W1-06-F08.

### F128 — DOC patterns и ограничение circuit breaker

S100: Closed пропускает вызовы и считает failures в окне; Open быстро отклоняет; Half-Open пропускает ограниченное число проб и закрывается после успешных проб. Нужно различать ресурсы, исключения, время восстановления. S101: connection/request timeouts, capped exponential backoff+jitter, ограничение retries и единственная точка повторов уменьшают retry amplification; timeout не доказывает отсутствие побочного эффекта. AWS отдельно предупреждает, что breaker добавляет modal behavior и может задерживать восстановление; token bucket — альтернатива ограничению retries. **INFERENCE:** для45 часов достаточно одного простого breaker на inference endpoint плюс bounded retry budget; не городить общий breaker на все камеры. Проверить все переходы fault injection, не считать этот pattern автоматической надёжностью.

<a id="f129"></a>

## F129 — DOC watchdog, container и RTSP

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S102](SOURCES.md#s102), [S007](SOURCES.md#s007), [S103](SOURCES.md#s103), [S104](SOURCES.md#s104). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L65](_WORK/W1_06.md); W1-06-F09, W1-06-F10, W1-06-F11.

### F129 — DOC watchdog, container и RTSP

S102 watchdog выдаёт bus error, если buffers не проходили timeout (ms), default1000,0 выключает; docs называют основным контекстом transcoding. Это детектор пропавшего потока буферов, не готовый reconnection controller и не детектор повторяющегося изображения.

S007: `unless-stopped` перезапускает вышедший контейнер, сохраняя намеренный stop; `on-failure` — только nonzero exit и не restart daemon. S103 HEALTHCHECK добавляет starting/healthy/unhealthy и health_status event; может обнаружить зависший процесс. **INFERENCE из совместного чтения:** standalone Docker restart policy + HEALTHCHECK сами по себе не гарантируют перезапуск unhealthy живого процесса. Требуется внешний supervisor/action или прикладной self-exit после неустранимого зависания; восстановление отдельной камеры предпочтительнее убийства всего сервиса.

S104 Source Group: `rtsp-reconnect-interval-sec` — секунды с последнего data до forced reconnect,0 выключает; `rtsp-reconnect-attempts=-1` — бесконечно; действуют для RTSP source type4. Это DeepStream-специфичные параметры, не универсальные FFmpeg флаги. Выбор TCP/UDP не заменяет application freshness watchdog.

<a id="f130"></a>

## F130 — CODE watchdog из работающего проекта, не наш выполненный тест

**Тип основания:** CODE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S105](SOURCES.md#s105). **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L73](_WORK/W1_06.md); W1-06-F12.

### F130 — CODE watchdog из работающего проекта, не наш выполненный тест

S105 Frigate v0.16.2: CameraWatchdog отдельно контролирует detection capture и recording subprocesses. L277–282: если от `current_frame` прошло >20s, обнуляет camera_fps и reset_capture_thread. L298–309: recording без новых segments120s перезапускается отдельно. L60–67: graceful stop имеет timeout30s, затем kill. L158–162: full frame queue увеличивает skipped counter, кадр пропускается. **INFERENCE:** проверка liveness PID недостаточна; прогресс detection и записи надо наблюдать отдельно, потери считать. Их20/120/30s — продуктовые параметры Frigate, а не рекомендованные SLA нашего оперативного контроля. Часы и окружение этого проекта не копировать вслепую.

<a id="f131"></a>

## F131 — минимальная модель состояний и восстановления

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L77](_WORK/W1_06.md); W1-06-F13.

## F131 — INFERENCE: минимальная модель состояний и восстановления

Предложение для прототипа, не установленное поведение LinQ. Хранить независимо `video_state`, `analysis_state`, `recording_state`, `delivery_state`; в метаданных `camera_id`, `stream_epoch`, `frame_seq`, `source_pts`, `received_monotonic_ns`, `sampled_monotonic_ns`, `request_id`, `backend`, `model_version`, `last_success_age_s`, error reason.

| Сбой/наблюдение | Обнаружение | Автодействие | Правдивое состояние UI/событий |
|---|---|---|---|
| Camera disconnect/decoder EOF | read error + age последнего decoded frame | закрыть worker, bounded backoff с jitter, reopen; на успех новый stream_epoch | Video unavailable; последний кадр с явным временем и затемнением |
| TCP открыт, decoder завис, data нет | watchdog прогресса decoded sequence; не только socket/PID | reconnect worker, после bounded attempts escalation | Video stale, analysis unavailable от этой камеры |
| Идентичные картинки продолжают идти с новыми timestamps | progression нормальный, image similarity/entropy — отдельный подозрительный сигнал | отдельное camera-health событие, ручная проверка; static industrial scene может быть нормальной | Suspected frozen/tampered; не выдавать как доказанную потерю камеры |
| LinQ API недоступно/timeout/overload | request deadlines, age последнего пригодного результата, breaker state | остановить накопление старых кадров; latest-frame slot на камеру; Half-Open probe; учитывать server retry hints если они есть | Video live, inference unavailable; нет «нарушений не обнаружено» |
| LinQ вернул поздний/старый/неверный result | frame_id, epoch, deadline, model/backend match | отвергнуть late result, считать reason; не применять к новой сессии | История подтверждает провал/пропуск, не рисует старые рамки |
| Один поток overload | per-camera queue/age/FPS | max1 pending frame, round-robin/deficit scheduler, max inflight | Degraded analysis FPS с фактическим значением |
| Worker завис/упал | heartbeat прогресса + timeout; process exit | локальный restart, persist settings/rules; предел restart storm | Worker recovering; downtime входит в denominator availability |
| Диск заполнен/recording не движется | free bytes, write failures, segment-age | retention/удаление только по политике; остановить новые клипы при невозможности | Analysis может работать, evidence unavailable отдельно |
| SSE/WebSocket/operator offline | ack/connection telemetry где доступна | reconnect + события из durable outbox, idempotent ID | Событие создано ≠ доставлено ≠ просмотрено человеком |

Backoff — наш стартовый параметр для эксперимента, например `U(0,min(30s,0.5s*2^k))`, а не норматив. Reset counter только после устойчивого восстановления; полный DNS/connect/TLS/read deadline должен быть конечным. Долгий retry старого inference кадра обычно хуже, чем новая проба на свежем кадре; события/уведомления, напротив, нуждаются в durable retry и дедупликации.

Состояние временных правил после gap: не считать неизвестное время доказанным непрерывным нарушением; сбросить/пометить unknown согласно договору с violation_methods. Не делать отрицательное заключение из отсутствия результатов. CPU/RTX fallback разрешён для разработки/демо только с баннером `backend=CPU`/`backend=RTX`, отдельными counters и событиями; доля LinQ inference, время деградации, результаты fallback сохраняются раздельно. Успех fallback не доказывает обязательный LinQ маршрут.

<a id="f132"></a>

## F132 — протокол измерений, годный для слайда

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L97](_WORK/W1_06.md); W1-06-F14.

## F132 — INFERENCE: протокол измерений, годный для слайда

### Определения и timestamp contract

Для каждого кадра логировать входы/выходы ingest, decode, sampling, JPEG/preprocess, queue, request send/receive, remote service queue/infer (только если SDK действительно возвращает их), postprocess/rule, event persisted, UI received/rendered. Все same-host durations — разности monotonic. RTT клиента включает сериализацию/передачу/очередь/сервер/обратный путь и не равен чистому inference. На другом host длительность inference измеряется его локальными start/end и передаётся как duration. Сквозная source-to-operator latency требует синхронизации clocks и оценки offset/drift/error, либо оптического same-clock теста. UTC сам по себе синхронизацию не доказывает. Если A и B clocks имеют ошибки ≤εA,≤εB, разность timestamps имеет неопределённость до εA+εB; сохранять этот предел, не рисовать точность1ms при неизвестном clock sync.

Отдельно публиковать:

- **camera/ingest FPS** — уникальные captured/received frames за wall time; не inference FPS;
- **decode FPS** — decoded frames/s, включая отброшенные после decode;
- **scheduled/sample FPS** — кадры, отобранные sampler; **completed valid inference FPS** — уникальные своевременные результаты/s; retry не считать новым кадром;
- **model invocation FPS** — вызовы определённой модели; каскадный classifier/crops не равен source frames;
- **aggregate FPS** и per-camera min/p50/p95 FPS, max inter-result gap; aggregate250 FPS может означать50×5 либо одну камеру250;
- **render FPS** — показ в браузере; smooth25 FPS video при inference5 FPS не является analysis25 FPS;
- FPS файлов без real-time pacing — throughput; FPS real-time cameras — sustained useful service under offered load.

### От physical onset до тревоги

`L_alarm = L_capture/codec/ingest + L_sampling + L_queue + L_transport + L_backend + L_post/rule + L_delivery/render`, но пересечения этапов и определения endpoints должны быть явно описаны; нельзя складывать независимо измеренные p95 этапов и называть это p95 суммы. Начало события `t0` задаётся разметкой/управляемым физическим стимулом; отдельно указывать first qualifying frame и время, когда dwell rule стала выполненной. Полезны две метрики: `t_ui - t0` и `t_ui - t_rule_eligible`.

При идеальном равномерном5 FPS Δ=200ms: ожидание первого sampled frame в[0,200ms), среднее100ms только при равномерной независимой фазе события. Если правило требует k последовательных положительных кадров, добавляется (k−1)×200ms после первого. Если правило требует physical dwell D секунд, обнаружение не раньше t0+D, а квантование eligible момента sampler даёт дополнительный интервал; точный bound зависит от того, отсчитывается D от physical onset или первой положительной выборки. Drops/переменный FPS ломают идеальный bound. Не переводить1s dwell в «5 кадров» без согласованного semantics и gap handling. События короче sampling interval могут не попасть ни в один кадр — latency успешных детекций эту потерю скрывает.

### p50/p95/p99, потери и цензура

Сохранять raw log/совместимые histogram buckets, sample count, длительность, warm-up, offered camera count/FPS, фактически обработанные камеры, backend/model/hash/precision/batch/input size, CPU/OS/driver/VRAM, канал/RTT, queue cap. Отдельные прогоны cold start и steady state; не выкидывать startup/reconnect из reliability отчёта. p99 маленькой выборки нестабилен; публиковать n, без обещания универсального p99.

В каждую заранее запланированную пробу дать ID. Зафиксировать offered, sampled-out, queue-replaced, request timeout, server error, late rejected, completed, event not detected, session ended pending. У completed могут быть p50/p95/p99 условных latency. Timeout — наблюдение `latency > deadline`/failure, а не нулевая latency и не пропуск строки; конец опыта при pending — right-censoring с границей времени. При более чем1% незавершённых/timeout нельзя заявлять unconditional p99 ниже deadline на основе успешного подмножества. Дополнительно `fraction of offered events alerted within SLA` с полным denominator и time-in-unavailable. Deadline exceed counters и camera downtime нужны даже при красивом success-only p95.

Нагрузку подавать независимо от ответов (paced cameras), иначе slow system получает меньше работы и выглядит быстрой. Изолированные stage benchmarks полезны для поиска bottleneck; итоговый SLA измерять вместе с ingest, evidence recording, UI и фактическим числом потоков. Отдельно проверить стек без inference, с mocked network delay и с реальным LinQ — первый и второй не доказывают третий.

Glass-to-glass: камера снимает changing timestamp/LED stimulus и display; высокочастотная внешняя запись включает source и monitor в одном кадре, либо Axis loop-overlay. Сохранить исходную запись, frame rate измерительной камеры/основной камеры/монитора и метод подсчёта, оценку квантования. Это покрывает видео. Для alarm latency тем же наблюдением снять физический onset и появление тревоги либо сопоставить метки с доказанным clock sync.

<a id="f201"></a>

## F201 — Axis Image Health Analytics документирует blocked/redirected/blurred/underexposed и learns scene. Контрпримеры производителя: свет/IR transition…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S129](SOURCES.md#s129). **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L79](_WORK/W2_06.md); W2-06-F06.

**F201 DOC, S129.** Axis Image Health Analytics документирует blocked/redirected/blurred/underexposed и learns scene. Контрпримеры производителя: свет/IR transition меняет alarm; припаркованный грузовик закрывает обзор без установленного умысла; намеренный camera move тоже redirected. В сцене без деталей detector признаёт unsuitable; blocked/blurred/redirected events недоступны. Это product example с пределами, не качество наших heuristics. [Axis health](https://help.axis.com/en-us/axis-image-health-analytics).

<a id="f202"></a>

## F202 — Простой tampering detector требует неподвижную сфокусированную сцену с контурами и учит reference перед readiness. Trigger on dark images не…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S130](SOURCES.md#s130). **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L81](_WORK/W2_06.md); W2-06-F07.

**F202 DOC, S130.** Простой tampering detector требует неподвижную сфокусированную сцену с контурами и учит reference перед readiness. Trigger on dark images не отличает закрытую линзу от сходного изменения освещения. Это предел причинной интерпретации конкретного продукта. [Q9216 manual](https://help.axis.com/en-us/axis-q9216-slv).

<a id="f203"></a>

## F203 — Для45ч обязательны decode/result progress/age и раздельные failure states. Image-health ниже — кандидаты suspected_anomaly, не…

**Тип основания:** INFERENCE/HYPOTHESIS. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S129](SOURCES.md#s129). **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L83](_WORK/W2_06.md); W2-06-F08.

**F203 INFERENCE/HYPOTHESIS.** Для45ч обязательны decode/result progress/age и раздельные failure states. Image-health ниже — кандидаты suspected_anomaly, не ML-detector/универсальные thresholds. Сигналы на bounded downsample/частоте с per-scene baseline/ROI/config revision; плохая картинка не означает «нарушений нет».

|Симптом|Дешёвый наблюдаемый сигнал / clock|Контрпример / следствие|
|---|---|---|
|Transport dead|Socket/decoder error, age последнего decoded frame local monotonic, sequence stalled|RTSP control/PID жив, media нет. Decoder stall и network outage не всегда различимы; video unavailable/stale с reason|
|Stale PTS|MediaPTS не движется при новых reads/отстаёт от доказанного mapping|Missing/synthesized PTS, B reorder, wrap/loop/reset; сначала clock anomaly, не frozen pixels|
|Repeated image|Equal decoded checksum либо устойчивая малая difference/perceptual distance по ROI|Статичная сцена нормальна; noise/AE меняют frozen content; loop имеет движение/PTS. Suspected repeated content, simulated label отдельно|
|Black/underexposed|Доля тёмных pixels, luma percentiles/variance, изменение от baseline|Ночь/lights-off/dark wall/privacy mask. Cause tamper не установлена; unsuitable→unknown|
|Overexposure|Доля saturated luma/channels, потеря contrast в ROI|White wall/снег/сварка/блик/AE transient. Наш optional кандидат, не заявленная S129 capability|
|Blur|Падение gradient/high-frequency/Laplacian statistic против same-scale baseline|Blank wall, compression, motion blur, resize, noise reduction; единого порога нет|
|Scene shift|Background feature/registration residual к approved reference, orientation/config event|Погрузчик перекрыл сцену, legitimate PTZ. Maintenance/relearn period unknown; нужна проверка человеком|

Сигналы могут сосуществовать, «причину» не выбирать автоматически. Static camera сохраняет transport healthy. Image health не заменяет качество inference: sharp image может иметь слишком мало pixels для СИЗ. Демо loop не доказывает frozen/tamper detector.

# 10 Поставка, Astra Linux и безопасность

<a id="f008"></a>

## F008 — `healthcheck` определяет состояние healthy; `restart` применяется при termination. `init: true` помогает передавать сигналы/reap процессов.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S005](SOURCES.md#s005). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L65](_WORK/W1_01.md); W1-01-F08.

**F008 [DOC, S005, прочитано]**. `healthcheck` определяет состояние healthy; `restart` применяется при termination. `init: true` помогает передавать сигналы/reap процессов. `image` поддерживает digest. `pull_policy: never` требует локальный cache, иначе fail; `latest` может подтягиваться даже при missing. Для file-backed secrets `uid/gid/mode` в Compose игнорируются из-за bind mount. [Service reference](https://docs.docker.com/reference/compose-file/services/).

<a id="f009"></a>

## F009 — Обычный `depends_on` задаёт порядок, а running не означает ready. `condition: service_healthy` ждёт успешную проверку dependency при старте.…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S006](SOURCES.md#s006). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L67](_WORK/W1_01.md); W1-01-F09.

**F009 [DOC, S006, прочитано]**. Обычный `depends_on` задаёт порядок, а running не означает ready. `condition: service_healthy` ждёт успешную проверку dependency при старте. Вложенное `depends_on: ... restart: true` относится к явной Compose операции над dependency, например `docker compose restart`, и не является универсальным наблюдателем её падений. Приложение всё равно должно переподключаться к БД/сервису самостоятельно. [Startup order](https://docs.docker.com/compose/how-tos/startup-order/).

<a id="f010"></a>

## F010 — `on-failure[:max-retries]` действует на ненулевой exit code и не восстанавливает контейнер только из-за рестарта daemon. `unless-stopped`…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S007](SOURCES.md#s007). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L69](_WORK/W1_01.md); W1-01-F10.

**F010 [DOC, S007, прочитано]**. `on-failure[:max-retries]` действует на ненулевой exit code и не восстанавливает контейнер только из-за рестарта daemon. `unless-stopped` сохраняет намеренное выключение. Документация отдельно описывает successful start минимум 10 секунд перед действием политики и поведение manual stop. Эти условия надо проверить на поставленной версии, а не считать policy лечением любого сбоя. [Restart policies](https://docs.docker.com/engine/containers/start-containers-automatically/).

<a id="f011"></a>

## F011 — Compose предоставляет secrets только перечисленным сервисам как файлы `/run/secrets/<name>`; файловый bind mount поддерживается здесь для Linux…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S008](SOURCES.md#s008), [S005](SOURCES.md#s005). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L71](_WORK/W1_01.md); W1-01-F11.

**F011 [DOC + INFERENCE, S008/S005, прочитано]**. Compose предоставляет secrets только перечисленным сервисам как файлы `/run/secrets/<name>`; файловый bind mount поддерживается здесь для Linux containers. `_FILE` — соглашение конкретных образов, не автоматическая функция любого приложения. Отсюда наш выбор: camera password читает ingest, LinQ token — adapter, private TLS key — ingress; не общий `.env`, не image layer и не git. File-backed Compose secret не следует описывать как зашифрованное хранилище: исходный файл и резервные копии защищает host. [Secrets guide](https://docs.docker.com/compose/how-tos/use-secrets/).

<a id="f012"></a>

## F012 — `docker image save -o images.tar IMAGE...` сохраняет image repository/layers/tags; `docker image load -i images.tar` восстанавливает images/tags,…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S009](SOURCES.md#s009), [S010](SOURCES.md#s010). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L73](_WORK/W1_01.md); W1-01-F12.

**F012 [DOC, S009/S010, прочитано]**. `docker image save -o images.tar IMAGE...` сохраняет image repository/layers/tags; `docker image load -i images.tar` восстанавливает images/tags, включая поддержанные сжатые архивы. Platform filtering требует Docker API 1.48+, а выбранная архитектура должна уже присутствовать в локальном image store/archive. Не переносить этот новый флаг на произвольную выданную Astra/Docker версию. [Save](https://docs.docker.com/reference/cli/docker/image/save/), [load](https://docs.docker.com/reference/cli/docker/image/load/).

<a id="f013"></a>

## F013 — Для запуска готовой поставки есть `docker compose up -d --no-build --pull never`; `--wait`/`--wait-timeout` ждут running/healthy и не доказывают…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S011](SOURCES.md#s011), [S005](SOURCES.md#s005). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L75](_WORK/W1_01.md); W1-01-F13.

**F013 [DOC, S011, прочитано]**. Для запуска готовой поставки есть `docker compose up -d --no-build --pull never`; `--wait`/`--wait-timeout` ждут running/healthy и не доказывают правильность модели или LinQ execution. Все флаги сверять `--help` фактической версии. [Compose up](https://docs.docker.com/reference/cli/docker/compose/up/).

<a id="f014"></a>

## F014 — Документация ALSE 1.8 различает privileged и рекомендуемый rootless режим, при котором daemon/containers не получают host root. В таблице…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S012](SOURCES.md#s012). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L77](_WORK/W1_01.md); W1-01-F14.

**F014 [DOC, S012, прочитано]**. Документация ALSE 1.8 различает privileged и рекомендуемый rootless режим, при котором daemon/containers не получают host root. В таблице одновременно есть `docker-compose 1.29.2-3+b1` и `docker-compose-v2 25.0.5.astra2+ci3`; это **версии пакетов Astra**, не доказательство upstream Compose 25 или гарантии всех current Docker docs features. [Astra Docker](https://docs.astralinux.ru/latest/guide/virtual/docker/).

<a id="f015"></a>

## F015 — Страница Docker-compose-v2 рекомендует его начиная с обновления 1.8.3 и указывает пакет `docker-compose-v2`; предварительные шаги отличают старый…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S013](SOURCES.md#s013). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L79](_WORK/W1_01.md); W1-01-F15.

**F015 [DOC, S013, прочитано]**. Страница Docker-compose-v2 рекомендует его начиная с обновления 1.8.3 и указывает пакет `docker-compose-v2`; предварительные шаги отличают старый `docker-compose`. Выбор v2 и реальный `docker compose version` важнее бездумного переноса `version: "3"` из примера. [Astra Compose v2](https://docs.astralinux.ru/latest/guide/virtual/docker/compose2/).

<a id="f016"></a>

## F016 — В Astra есть отдельная настройка Docker на пониженном уровне целостности; по документации она не включена по умолчанию. Для privileged Docker дан…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S014](SOURCES.md#s014). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L81](_WORK/W1_01.md); W1-01-F16.

**F016 [DOC, S014, прочитано]**. В Astra есть отдельная настройка Docker на пониженном уровне целостности; по документации она не включена по умолчанию. Для privileged Docker дан отдельный рецепт memory cgroups, изменяющий параметры загрузки и требующий reboot. Это инструкция для администратора конкретной ОС, **не наша команда на общем сервере**. Мандатные метки, mounts, cgroups и device permissions — самостоятельные integration gates. [Astra restrictions](https://docs.astralinux.ru/latest/guide/virtual/docker/restrictions/).

### Что именно совместимо с Astra

<a id="f017"></a>

## F017 — Первичный релиз Astra сообщает об успешной интеграции **LinQ HP + Astra Linux Server**. Тестирование всей линейки описано как дальнейший план. Не…

**Тип основания:** CLAIM. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S015](SOURCES.md#s015). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L85](_WORK/W1_01.md); W1-01-F17.

**F017 [CLAIM, S015, 13.11.2025]**. Первичный релиз Astra сообщает об успешной интеграции **LinQ HP + Astra Linux Server**. Тестирование всей линейки описано как дальнейший план. Не приведены конкретные driver/runtime/kernel версии, полный перечень SKU, container digest или наш Python/FFmpeg stack. Нельзя заменить это фразой «LinQ сертифицирован под Astra, поэтому наш стек совместим». [Astra release](https://astra.ru/about/press-center/news/gruppa-astra-i-khaytek-obedinyayut-usiliya-dlya-razvitiya-otechestvennykh-ii-resheniy/).

<a id="f018"></a>

## F018 — Другой релиз описывает совместное решение **LinQ HX + Astra Linux Embedded**. Упоминание сертификатов ФСТЭК/Минобороны/ФСБ относится в тексте к…

**Тип основания:** CLAIM. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S016](SOURCES.md#s016). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L87](_WORK/W1_01.md); W1-01-F18.

**F018 [CLAIM, S016, 07.10.2026]**. Другой релиз описывает совместное решение **LinQ HX + Astra Linux Embedded**. Упоминание сертификатов ФСТЭК/Минобороны/ФСБ относится в тексте к **операционной системе Embedded**. Это не сертификация нашего приложения, соединения с удалённым LinQ, контейнера, всей линейки ускорителей или архитектуры. Фактический сертификат конкретного изделия/конфигурации не получен. [HX/Embedded release](https://astra.ru/about/press-center/news/khaytek-i-gruppa-astra-razrabatyvayut-sovmestnoe-reshenie-na-osnove-rossiyskogo-ii-uskoritelya-dlya-/).

### Камеры и промышленная сеть

<a id="f019"></a>

## F019 — Axis рекомендует отдельную учётную запись клиента с ограниченными правами; HTTPS вместо незащищённого доступа, при его отсутствии Digest вместо…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S017](SOURCES.md#s017). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L91](_WORK/W1_01.md); W1-01-F19.

**F019 [DOC, S017, July 2026]**. Axis рекомендует отдельную учётную запись клиента с ограниченными правами; HTTPS вместо незащищённого доступа, при его отсутствии Digest вместо Basic. Видеозащита рассматривается отдельно: SRTP/RTSPS поддерживается Axis начиная с AXIS OS 7.40 при поддержке VMS; administrative traffic должен защищаться HTTPS отдельно. Следствие: authentication/Digest не означает шифрования видео, HTTPS web interface не означает защищённый RTSP stream. Возможности Axis нельзя перенести на неизвестную камеру: проверяется camera firmware + client/relay. [Axis hardening](https://help.axis.com/en-us/axis-os-hardening-guide).

<a id="f020"></a>

## F020 — NIST §6.2.1.3 предлагает разделение по функции/расположению физическими switches либо VLAN и разрешение явных необходимых потоков через…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S018](SOURCES.md#s018), [S019](SOURCES.md#s019). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L93](_WORK/W1_01.md); W1-01-F20.

**F020 [DOC, S018/S019, final r3 September 2023]**. NIST §6.2.1.3 предлагает разделение по функции/расположению физическими switches либо VLAN и разрешение явных необходимых потоков через gateways/firewalls после карты потоков. §6.2.1.4.4 рассматривает MFA как best practice удалённого доступа к OT с учётом возможностей компонентов. Это архитектурная рекомендация, не сертификат соответствия IEC 62443. На landing 21.09.2026 уже указана initial public draft Revision 4; использован final r3, а не присвоенный draft статус final. [NIST final](https://doi.org/10.6028/NIST.SP.800-82r3), [version status](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

<a id="f021"></a>

## F021 — Docker volumes — самостоятельные persistent host stores с отдельными backup/restore процедурами. Вместе с F012 это означает: image tar не является…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S020](SOURCES.md#s020). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L95](_WORK/W1_01.md); W1-01-F21.

**F021 [DOC/INFERENCE, S020]**. Docker volumes — самостоятельные persistent host stores с отдельными backup/restore процедурами. Вместе с F012 это означает: image tar не является полной резервной копией БД событий, clips, mounted models/config/secrets. Воспроизводимая поставка должна перечислять эти артефакты отдельно. [Volumes](https://docs.docker.com/engine/storage/volumes/).

<a id="f022"></a>

## F022 — Docker отмечает daemon attack surface и связь privileged management с host access; rootless помещает daemon и containers в user namespace. Для…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S021](SOURCES.md#s021). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L97](_WORK/W1_01.md); W1-01-F22.

**F022 [DOC/INFERENCE, S021]**. Docker отмечает daemon attack surface и связь privileged management с host access; rootless помещает daemon и containers в user namespace. Для нашего UI/API нельзя пробрасывать Docker socket ради перезапуска worker. Предоставление `--privileged` или всех `/dev` не считать обычной частью переносимого приложения. Применимость rootless к actual LinQ device не проверена. [Docker security](https://docs.docker.com/engine/security/), [rootless](https://docs.docker.com/engine/security/rootless/).

### Узкая проверка расписания и критериев

<a id="f023"></a>

## F023 — Официальный сайт 2026 повторяет обязательный inference на LinQ и онлайн-доступ без технических условий. Расписание: публикация кейсов 23 октября…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S022](SOURCES.md#s022). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L101](_WORK/W1_01.md); W1-01-F23.

**F023 [DOC + INFERENCE, S022, live 23.10.2026]**. Официальный сайт 2026 повторяет обязательный inference на LinQ и онлайн-доступ без технических условий. Расписание: публикация кейсов 23 октября 13:00, дедлайн решений 25 октября 10:00. Разность даёт **45 ч**; это планировочное окно по опубликованному расписанию, не обещание 45 ч непрерывного эксклюзивного LinQ доступа. Полный кейс/participant account не читались. [Official case/schedule](https://hackathon2026.otkroimosprom.ru/).

<a id="f024"></a>

## F024 — Положение оценивает соответствие заявленной и фактической функциональности прототипа (§6.4.1), решение основной проблемы, соотношение эффекта и…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S023](SOURCES.md#s023). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L103](_WORK/W1_01.md); W1-01-F24.

**F024 [DOC, S023, §6.4 PDF p10]**. Положение оценивает соответствие заявленной и фактической функциональности прототипа (§6.4.1), решение основной проблемы, соотношение эффекта и затрат на разработку/внедрение (§6.4.3), UX/UI, второстепенные проблемы (§6.4.6). Отсюда наш приоритет работающего LinQ маршрута, видимого unavailable/stale статуса и понятного восстановления оправдан архитектурно. Критерии не устанавливают Docker, Astra, минимальный FPS, SLA или требование production security certification. [Official regulation](https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf).

<a id="f185"></a>

## F185 — Согласованный кандидат: MediaMTX1.21.2 relay, PyAV16.0.1 для Python decode, CPython3.12.15 source baseline для собственного клиентского…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L9](_WORK/W2_05.md); W2-05-F01.

**F185 [INFERENCE].** Согласованный кандидат: MediaMTX1.21.2 relay, PyAV16.0.1 для Python decode, CPython3.12.15 source baseline для собственного клиентского приложения, standalone `websockets==17.0.1` для processed view, встроенный модуль `sqlite3` с отдельно подтверждённым SQLite runtime. Один DB writer, local evidence directory, native browser WebSocket/Canvas. Это совместимые по declared Python requirements кандидаты, а не протестированный lock. Full-chain golden fixture и issued LinQ matrix остаются gate. Remote LinQ может иметь другой Python/native ABI и отдельный supplied environment: не обновлять его до3.12 ради нашего клиента.

W2_02 final: MediaMTX — relay; prospective same-demux indexed remux допускается лишь после раннего E009. До успеха gate — analyzed snapshot + native archive с `mapping=unknown`, без обещания exact event→native segment. PyAV не даёт готовый durable recorder/pin lifecycle. W2_03 final pin17.0.1 учтён; FastAPI/Starlette/Uvicorn для processed-view route не добавлены. Reviewable structured manifest: `MATERIALS/W2_05/PROVISIONAL_ARTIFACT_MANIFEST.json`; там expected hashes/artifact URLs и явные UNKNOWN. Для WS universal candidate `websockets-17.0.1-py3-none-any.whl`, SHA256 `c6be9cba65c65cc76dfa3d4619e359ff02a4476c74e179b215236c11a0b32345`; сведения изW2_03, не новый download. Native MediaMTX reader берётся из того же tag и является optional live, а не отдельной обязательной JS dependency.

<a id="f186"></a>

## F186 — Нельзя выбрать «SQLite из Python3.12» без версии native runtime. В current SQLite WAL docs описана WAL-reset corruption race: уязвимый…

**Тип основания:** DOC/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S074](SOURCES.md#s074), [S121](SOURCES.md#s121), [S120](SOURCES.md#s120). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L13](_WORK/W2_05.md); W2-05-F02.

**F186 [DOC+INFERENCE; S074, S120, S121].** Нельзя выбрать «SQLite из Python3.12» без версии native runtime. В current SQLite WAL docs описана WAL-reset corruption race: уязвимый диапазон3.7.0–3.51.2, исправление3.51.3 и backports3.44.6/3.50.7; две connection в разных threads/processes с совпадением write/checkpoint — условие. Single writer не заменяет патч, если checkpoint/backup/read connections остаются. На дату доступа current release —3.54.1 (16.10.2026), не3.53.4 из stale `current.html` search cache;3.54.0 имеет исправленный в3.54.1 heap overflow на32bit.3.52.0 withdrawn. Принятый provisional runtime pin для собственного клиента: SQLite3.51.3 с точным source_id из S120; это консервативная исправленная ветка, не «latest» и не установленная здесь библиотека. При target distro backport выбрать documented patched artifact с vendor provenance и изменить manifest, не сравнивать один version string. Если получить согласованный3.51.3 невозможно, owner выбирает новый vetted runtime artifact; не monkey-patch DLL от CLI.

<a id="f187"></a>

## F187 — PyAV wrapper BSD-3-Clause не покрывает native wheel bundle. В проверенном Linux cp312 manylinux_2_28 wheel есть libavcodec62.11.100,…

**Тип основания:** CODE/LOCAL/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S032](SOURCES.md#s032), [S119](SOURCES.md#s119), [S118](SOURCES.md#s118). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L15](_WORK/W2_05.md); W2-05-F03.

**F187 [LOCAL+CODE+INFERENCE; S032, S118, S119].** PyAV wrapper BSD-3-Clause не покрывает native wheel bundle. В проверенном Linux cp312 manylinux_2_28 wheel есть libavcodec62.11.100, libavformat62.3.100, libavutil60.8.100, x264/x265/gnutls и другие библиотеки. Frozen build workflow использует vendor `8.0-2`. Binary strings заявляют LGPL version3 or later и configure flags с x264/x265; это metadata, не юридическое заключение о согласованности лицензирования всех связанных компонентов. Полный список и строки сохранены. Требуется transitive notices/source/license review выбранного wheel перед передачей bundle; обозначать всю поставку только BSD/MIT нельзя. Standalone ffmpeg CLI n8.0 — отдельный optional process artifact, он не меняет linked libav wheel.

<a id="f188"></a>

## F188 — Версия исходника, binary artifact и установленное окружение — три записи. У каждой release-поставки сохранять `component`, `role`, `reuse_mode`,…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S118](SOURCES.md#s118), [S120](SOURCES.md#s120). **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L43](_WORK/W2_05.md); W2-05-F04.

**F188 [INFERENCE].** Версия исходника, binary artifact и установленное окружение — три записи. У каждой release-поставки сохранять `component`, `role`, `reuse_mode`, `source_version/commit`, `artifact filename/url/sha256`, `platform/ISA/ABI`, `direct_license`, `transitive_scope`, `build_flags`, `notices/source location`, `selection_status`, `installation_evidence`. Здесь везде `selection_status=provisional`, `installation_evidence=none`. SHA из PyPI — expected digest; Linux PyAV additionally проверен собственным download digest. Target/platform не угадывать по Windows рабочей папке.

| Компонент / pin | Роль / reuse_mode | Артефакт / license scope / gate |
|---|---|---|
| MediaMTX1.21.2 SHA914e395… | relay `used-as-process`; optional native archive | MIT direct repo, Go dependency notices отдельно (`go.mod`). Target official release binary или image по digest выбирается после ISA/OS; release tag не checksum binary. Не добавить go2rtc/Frigate. Native reader если нужен — тот же tag, тогда served/copied-code с MIT notice; сейчас optional, не silent HEAD reader |
| CPython3.12.15 | собственный backend, `dependency/runtime` | Source artifact selected поS14: `Python-3.12.15.tar.xz`, SHA256 `c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a`. Binary build/platform пока UNKNOWN: security-only release source-only, официального Windows installer3.12.15 нет. Source pin не означает prepared target binary. Final package/image+SHA и linked SQLite фиксируются при inventory, PSF license+bundled components. Это coherent source candidate с PyAV>=3.10 и WS>=3.11, не законченный lock; proprietary LinQ Python отдельно |
| av==16.0.1 SHA7687256… | decode + prospective indexed remux, `dependency` | Linux cp312 manylinux_2_28_x86_64 wheel/hash S118; glibc>=2.28/ABI/ISA gate. Windows cp312 win_amd64 candidate SHA256 `0c669b6b6668c8ae74451c15ec6d6d8a36e4c3803dc5d9910f607a174dd18f17`, upload13.10.2025; только metadata, не проверен ZIP. Не переносить Linux native list на Windows. BSD wrapper, full native bundle отдельно |
| linked libav из выбранного av wheel | `dependency`, уже включён в artifact | vendor8.0-2 по frozen workflow; Linux observed codec62.11.100/device62.1.100/filter11.4.100/format62.3.100/util60.8.100/swresample6.1.100/swscale9.1.100. Runtime `av.library_versions`, `av.ffmpeg_version_info` и internal `av._core.library_meta` (configuration/license; pinned coupling) ещё не читались. LGPLv3 strings плюс third-party bundle review; codec support и NVDEC flags не обещание working hardware decode |
| standalone ffmpeg n8.0 / ffprobe | file-loop publisher/diagnostic/export derivative, optional `used-as-process` | отдельный W1 source tag, build vendor/platform/hash UNKNOWN. FFmpeg mostly LGPL2.1+, GPL/version3/nonfree flags меняют scope; выбрать distributable build+notices, записать `-version/-buildconf`. CLI n8.0 не задаёт версии libav PyAV. Не нужен CLI для самого PyAV import |
| websockets==17.0.1 SHAfd3f16cc… | standalone asyncio processed view, `dependency` | BSD-3-Clause direct; use pinned artifact metadata изW2_03. Python>=3.11. Без ASGI extras, native WS/Canvas без JS package; no FastAPI/Starlette/Uvicorn addition. Browser exact version/OS — runtime inventory gate, не npm lock |
| SQLite3.51.3 source_id S120 | local single DB, `dependency` через stdlib sqlite3 | SQLite core public domain, Python wrapper PSF. Actual binary package/build/compile_options/hash UNKNOWN. Стандартного `pip install sqlite3` для pin нет. CPython build/distro package/image должен реально link этот runtime; альтернативный documented vendor backport требует manifest amendment. Не менять issued SDK libraries |
| Собственный app/schema | future authored code | artifact/source hash появится при реализации; external copied-code сейчас none. Schema migration revision и user_version закрепить вместе с DB |
| Roboflow/Frigate/Savant/DL Streamer/Ultralytics catalog | `idea-only` для architecture patterns | не импортируются в этот minimum. Нет причины добавлять лицензию целого Roboflow repo как shipped dependency. Если скопирован конкретный path — nearest license и notices отдельно. Ultralytics weights/training/export/licenses → model_stack, не считать model weights MIT |
| LinQ SDK/native/driver/firmware/model compiler/runtime | proprietary bundle UNKNOWN | supplied exact release/OS/ISA/redistribution/container permission, hashes и license texts отсутствуют. Used-as-process или dependency зависит от grant. Публичная Astra compatibility news не закрывает target matrix |
| Model weights/datasets | scope UNKNOWN | точные weights/hash/source/license отдельно →model_stack/datasets; repo license не покрывает веса/данные автоматически. ONNX/OpenCV/NumPy/Pillow добавлять только по реальному import, потом pin/transitives; ни один не является автоматически mandatory web dependency |

Offline bundle должен включать все выбранные wheels+native libs/notices, app/config/static assets, source/license material where needed, model artifacts при разрешении, images по digest/ISA и отдельно DB+media backup. Не CDN, runtime pip/apt или model auto-download. Docker/Compose/host drivers не входят в image save. Astra edition/update/kernel/ISA/mandatory policy/device mapping задаются поставкой; соответствующий W1_01 gate остаётся открытым. Ни manifest, ни offline tar не обеспечивают сеть до обязательного remote LinQ.

<a id="f209"></a>

## F209 — Упаковка для 45-часового окна

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S009](SOURCES.md#s009), [S011](SOURCES.md#s011), [S010](SOURCES.md#s010). **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L133](_WORK/W1_01.md); дополнительная тематическая выписка.

## Упаковка для 45-часового окна

**[INFERENCE]** Разделить два deployment units: собственный service bundle (ingest/backend/UI, event storage и media process по фактическому выбору соседних ячеек) и один inference adapter, который бывает remote client либо worker на supplied host. Изменение access mode не должно менять event schema, tracker или frontend. Broker/Kubernetes не нужен только ради remote LinQ: он не исправит внешнюю quota. Если соседняя V08 выберет модульный монолит, этот интерфейс остаётся межмодульным; IPC/network вводится там, где проходит actual host boundary.

Состав reviewable release bundle: исходный commit; `compose.yaml`/override для режима; Dockerfiles и lock dependencies; полный перечень image tags/IDs/digests и platform; model manifest/artifacts/golden samples; camera/source config без passwords; миграция/инициализация БД; каталог clips с retention; local TLS CA/public cert и отдельно выдаваемый private key; operator runbook с проверкой sample-to-event; перечень secret files; примеры ответов actual adapter. Это перечень будущей реализации, не созданный здесь готовый продукт/код до хакатона.

Офлайн процедура на отдельном тестовом хосте, **предлагаемая, не выполненная**:

```text
# После online подготовки на разрешённой машине с нужными images:
docker image save -o images.tar team/backend:release team/worker:release
# На целевом Linux host после проверки archive hash и наличия engine/compose:
docker image load -i images.tar
docker compose up -d --no-build --pull never
```

Имена images иллюстративны, команды основаны на S009, S010, S011. Нужны все транзитивные сервисы, не только два примера. Bundle hash проверяет целостность передачи, а не происхождение/подлинность без доверенного канала. Digest pin и загруженный tar следует сверить на чистом target: `image ID` и `RepoDigest` не взаимозаменяемы, не обещать, что любой архив автоматически восстановит все registry metadata. Модели и manifests при bind mounts переносятся отдельно; volume/DB backup/restore отдельно. На запуске нет `pip install`, `apt`, model auto-download или frontend CDN. Engine/Compose/host driver тоже должны быть заранее разрешены и установлены из подходящей поставки, но их наличие не входит магически в image tar.

Windows development не определяет целевую ОС: Linux containers могут служить средой собственных сервисов; native LinQ compile/runtime/ISA остаются в supplied Linux environment до получения support matrix. Перенос x86-64 image на ARM HX нельзя считать рабочим без подходящих image/native artifacts и проверки. Образ не несёт kernel driver target host.

### Health/restart политика приложения

- **Liveness** проверяет, что наш процесс/event loop отвечает; **readiness** сообщает актуальную пригодность inference/model/зависимостей. Потеря remote LinQ делает inferencing unavailable, но не должна запускать бесконечный restart API/БД, которые могут продолжать показывать сохранённые события.
- **Progress** измеряет последний successful frame/result по каждой камере, age, inflight, pending jobs и quota backoff. Живой HTTP не доказывает продвижение pipeline. Health probe не должен загружать NN в общий слот или создавать бесконтрольные inference jobs.
- Worker остановить admission → дождаться documented terminal/drain → закрыть собственную session → завершиться. Срок app deadline не доказывает освобождение native buffers/job; shared reset только оператору владельца. Отдельный local process supervisor не следует смешивать с competing Docker supervisor над одним процессом.
- `restart: unless-stopped` — возможный выбор для собственных обычных сервисов; bounded `on-failure` может быть у экспериментального worker, если supported lifecycle позволяет. Отсутствие automatic restart на `unhealthy` необходимо компенсировать нашим watchdog/exit policy только для разрешённого safe failure, не сбросом общей платы.

### Astra integration gate

До обещания «развёртывается на Astra» зафиксировать edition/update, kernel, ISA, Docker/Compose фактические версии, privilege/rootless mode, мандатный профиль, permissions на models/clips/secrets/device и supplied driver/runtime pairing. Затем по отдельности: обычный web/container start; persistent event write/restart; camera decoder и codec; LinQ worker import/load/run; полный результат/geometry/event. Успех UI в Astra container не устанавливает driver support; успех HP на Server в новости не устанавливает HX/ARM, а успех Embedded не устанавливает наш x86 сервер. Не отключать мандатную защиту или reboot shared host как «починку Docker». Запросить согласованную конфигурацию владельца.

<a id="f210"></a>

## F210 — Достаточная граница безопасности без выдуманной сертификации

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L164](_WORK/W1_01.md); дополнительная тематическая выписка.

## Достаточная граница безопасности без выдуманной сертификации

**[INFERENCE, применение F019/F020/F022]** Целевая схема: camera VLAN/segment → ограниченный ingest/gateway → application segment → разрешённый outbound remote LinQ channel. Browser проходит через authenticated HTTPS application endpoint; не получает camera credentials, administrative URL или LinQ token. DB/queue/worker порты не публикуются наружу без необходимости. Management/VPN/jump host — отдельный административный путь с MFA там, где поддерживается; пользовательский и machine-to-machine доступ имеют разные credentials.

Список разрешённых потоков конкретизируется по inventory, а не правилом «любые порты внутри VPN»: ingest → camera только необходимые streaming/control protocols; backend → LinQ endpoint; backend → storage; ingress → backend; администратор → management. Port 554/TCP относится к типичному RTSP, RTP/UDP может использовать динамические порты; не открыть весь UDP «чтобы заработало». Если camera/client умеют безопасный stream transport, проверить его отдельно от HTTPS управления. Если не умеют, изолированный локальный участок и защищённый gateway-to-remote tunnel ограничивают область plaintext; это не end-to-end encryption камеры до worker.

В prototype достаточно явно реализовать защищённый единый вход; разграничить viewer/operator/admin так, чтобы viewer не мог менять camera/rules/config и выгружать произвольный файл. Проверять auth у clip/event endpoints и stream subscription, а не только скрывать кнопку UI. URLs камеры, пароли, bearer tokens и query strings не должны попадать в frontend payload/logs/trace. Для clip filenames использовать внутренние IDs и controlled lookup, не путь из запроса. Retention, файловые разрешения и server-side authorization защищают клипы; TLS защищает передачу, а шифрование host storage/ключей — отдельный механизм и отдельная проверка восстановления.

VPN/TLS не решают доверие к стороннему inference server, срок хранения upload или доступ других участников. Минимизировать передаваемые данные до нужного payload; спросить remote retention, tenant isolation, log contents и delete policy. Не хранить camera credentials на чужом server, если выбран tensor/frame API и ingest остаётся локальным. Этот принцип уменьшает последствия компрометации worker и упрощает demo setup. Никаких заявлений о соответствии IEC 62443 или сертифицированном ПАК без actual scope не делать.

<a id="f227"></a>

## F227 — Отрицательные результаты и передача

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S141](SOURCES.md#s141). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_05.md:L154](_WORK/W2_05.md); дополнительная тематическая выписка.

## Отрицательные результаты и передача

Предполагаемый `.github/workflows/wheels.yml` уPyAV v16.0.1 вернул404; git tree найден и прочитан реальный `.github/workflows/tests.yml`. Git tag SHA получен `git ls-remote`, filtered shallow no-checkout clone использован только для source read. `scripts/build-deps` локального developer build включает GPL/nonfree conditional flags, но НЕ является тем же pipeline, что published wheel: не выдавать его за точную конфигурацию PyPI artifact. ZIP read был повторён из-за Unicode console-print ошибки; оба download digest совпали, не было import/install. Final saved metadata/strings достаточны для найденной licensing границы; source/ABI/codec equivalence не проверены.

→Корню/автору: coherent provisional manifest F185, F186, F187, F188; actual SQLite gate F186/F190; нельзя «SQLite3 изPython»/«весьPyAV BSD»; backup F193, F194, restore F195 и file boundary F196. →W2_01: old backup не снимает remote held, postcutoff obligations могут не иметь local rows; owner reconcile до admission. →W2_02: validation/hash/rename не power durability, durable intents/reservations и rebuild pins до retention, exact clips только послеearlyE. →W2_03: pin17.0.1 сохранён, CPython3.12.15 source candidate, no ASGI dependency. →W2_06: minimum45ч содержит recovery/backup gate, не HA; exact native bundle/targetFS остаются unknown. →model_stack/datasets: веса и proprietary runtime не очищены MIT/BSD architecture repo license.

# 11 Capacity50/500 и полный resource inventory

<a id="f133"></a>

## F133 — INFERENCE/LOCAL arithmetic: прозрачный sizing50/500

**Тип основания:** LOCAL/INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S136](SOURCES.md#s136). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_06.md:L129](_WORK/W1_06.md); W1-06-F15.

## F133 — INFERENCE/LOCAL arithmetic: прозрачный sizing50/500

Все числа ниже — **сценарные допущения**, не измеренные камеры/ускоритель. SI decimal:1kB=1000bytes,1MB=10^6bytes,1GB=10^9bytes,1TB=10^12bytes;1Mb/s=10^6bits/s. Сжатый main:1920×1080,25FPS,4Mb/s; substream:1280×720,25FPS,**1Mb/s принято для расчёта**, не свойство720p; sample analysis5FPS; JPEG100kB **независимо от resolution только в этом сценарии**. Реальный JPEG зависит от качества/текстуры/размера, его надо измерить. Raw NV12/YUV4208bit=1.5B/pixel; RGB8=3B/pixel, без stride/padding/copy overhead. Потребность в frame copies/pinned memory выше нижней оценки.

### Ingest/WAN и compressed storage

`B_compressed=N*b` [Mb/s]. `B_JPEG=8*N*f_a*J/10^6` [Mb/s]. `S=N*b*10^6/8*T/10^12` [TB]. Compressed recording не требует decode, если пишется исходный поток; декодирование только analytics substream может быть отдельной задачей.

| Путь | На1 камеру | 50 камер | 500 камер |
|---|---:|---:|---:|
| main compressed ingest4Mb/s |4Mb/s;0.5MB/s|200Mb/s;25MB/s|2000Mb/s;250MB/s|
| substream compressed1Mb/s |1Mb/s;0.125MB/s|50Mb/s;6.25MB/s|500Mb/s;62.5MB/s|
| main+sub, если оба получаем в этот узел |5Mb/s|250Mb/s|2500Mb/s|
| JPEG100kB ×5FPS |4Mb/s;0.5MB/s|200Mb/s;25MB/s|2000Mb/s;250MB/s|
| raw1080p NV12 ×5FPS |124.416Mb/s|6.2208Gb/s|62.208Gb/s|
| raw1080p RGB ×5FPS |248.832Mb/s|12.4416Gb/s|124.416Gb/s|
| raw720p NV12 ×5FPS |55.296Mb/s|2.7648Gb/s|27.648Gb/s|
| raw720p RGB ×5FPS |110.592Mb/s|5.5296Gb/s|55.296Gb/s|

Если ingest main уже4Mb/s, JPEG WAN4Mb/s — **два разных участка**; у исходящего JPEG нет экономии относительно пересылки main в заданных допущениях. Main+sub ingest5Mb/s и JPEG outbound4Mb/s нельзя бесконтекстно складывать как требование одного full-duplex линка: нужны направления и расположение узлов. Relay нескольким клиентам умножает egress и нагрузку; централизовать повторное получение одного camera stream.

При выбранном инженерном target utilization70% (допущение, не стандарт) для полезных2Gb/s требуется не менее2/0.7=2.857Gb/s измеренной доступной полосы до protocol overhead/VBR burst; номинальный1GbE заведомо не подходит. Для50 JPEG потоков полезные200Mb/s требуют286Mb/s при том же запасе; это ещё не гарантирует WAN latency. Local NV12 raw не обязательно пересылается по сети, но таблица показывает цену неудачного remote API.

| Хранение | На1 камеру / сутки | 50 / сутки | 500 / сутки | 50 /30сут | 500 /30сут |
|---|---:|---:|---:|---:|---:|
| main4Mb/s, непрерывно |43.2GB|2.16TB|21.6TB|64.8TB|648TB|
| sub1Mb/s, непрерывно |10.8GB|0.54TB|5.4TB|16.2TB|162TB|
| все JPEG100kB×5FPS |43.2GB|2.16TB|21.6TB|64.8TB|648TB|

Это video payload, без RAID parity/replication, free-space reserve, FS/index/metadata, retrieval/backup IO. Для событийных клипов: `Sclips=N*events_per_cam_day*clip_seconds*b/8` [MB/day при b вMb/s]. Пример20 событий/камеру/сутки ×30s ×4Mb/s =300MB/камеру/сутки;50=15GB/сутки,500=150GB/сутки. Overlap клипов может дедуплицироваться через segments; без дедупликации остаётся приведённая верхняя сумма. Нельзя обещать event-only savings без измеренного event rate/клип-политики. Pre-event ring10s4Mb/s=5MB/камеру;50=250MB,500=2.5GB compressed payload.

### Raw и decode

`Pdecode=N*W*H*f_source` [pixels/s]; анализ5FPS после полного decode25FPS не уменьшает автоматически decode до5FPS. Interframe dependencies и реализация decoder/drop mode определяют экономию. Без подтверждённого selective decode считать25FPS. Substream с camera-native5FPS может снизить эту стоимость, если доступен и пригоден правилам.

| Нагрузка | 1 | 50 | 500 |
|---|---:|---:|---:|
| full decode1080p25 |51.84MPix/s|2.592GPix/s|25.92GPix/s|
| full decode720p25 |23.04MPix/s|1.152GPix/s|11.52GPix/s|
| actual frames inference5FPS |5/s|250/s|2500/s|
| raw1080p NV12 full25FPS bytes |77.76MB/s|3.888GB/s|38.88GB/s|
| raw1080p RGB full25FPS bytes |155.52MB/s|7.776GB/s|77.76GB/s|
| raw720p NV12 full25FPS bytes |34.56MB/s|1.728GB/s|17.28GB/s|
| raw720p RGB full25FPS bytes |69.12MB/s|3.456GB/s|34.56GB/s|

1 raw1080p NV12 frame=3.1104MB, RGB=6.2208MB. Один latest slot на500=1.5552GB NV12/3.1104GB RGB без pool/decoder surfaces. Очередь10 кадров умножает это на10 и добавляет stale latency. Если бы raw хранился постоянно:1080p NV1225FPS=6.718464TB/камера/сутки,50=335.9232TB,500=3359.232TB; sampled5FPS=1.3436928TB/камера/сутки. RGB вдвое; поэтому raw — transient memory/API consideration, а не разумный архив. 720p NV1225FPS=2.985984TB/камера/сутки,5FPS=0.5971968TB; ×50/500 по той же формуле. Арифметика проверена локальным Python; это LOCAL calculation, не performance test.

### Compute, concurrency, fairness и max capacity

Для однородного пути обозначим измеренные в нужном SLA/конфиге ресурсы: `Cinf` usable frames/s всей model chain на узел; `Cdec` pixels/s для данного codec/profile/resolution; `Cpre` resize/JPEG frames/s; `Cin` usable ingest bits/s; `Cwan` usable WAN bits/s; `Cwrite` sustained record bytes/s с параллельным replay; `Susable` bytes; retention `T` seconds; `Musable` transient bytes, `mcam` измеренные bytes/camera; API max concurrency `K`, measured request cycle `L` seconds при такой concurrency. Для ресурсов нужны данные sustained worst relevant mix, а не isolated maximum. Тогда:

`Nmax <= floor(min(Cinf/f_a, Cdec/(W*H*f_source), Cpre/f_a, Cin/b_in, Cwan/(8*J*f_a), Cwrite/(b_record/8), Susable/((b_record/8)*T), Musable/mcam, K/(f_a*L)))`.

Здесь b_in и b_record вbits/s, J вbytes; WAN term выбран для JPEG и заменяется при другом transport. Неиспользуемый bottleneck term убрать. K/(f_aL) — необходимая concurrency/throughput оценка, не гарантия p95: dynamic queue/server sharing меняют L. Little-law применение требует устойчивой нагрузки и согласованных средних; tail latency проверять отдельно. Если C заданы peak benchmarks, сначала ввести доступную долю u и накладные расходы, затем проверить under offered load.

Для нескольких моделей/каскадов primary workload `N*f_a`; secondary workload `N*f_a*E[crops/frame]*fraction_routed` с реальным crowd distribution. При ops/frame `O` требуемая арифметика `N*f_a*O` ops/s; TOPS theoretical не измеряет support ops, copies, precision/compilation и scheduler. UNKNOWN LinQ `Cinf`, Cdec, quotas, K, batch, VRAM/runtime. **Нет основания назвать количество LinQ плат** до теста.

Гипотетический пример исключительно для объяснения: если один узел **измеренно** выдержал Cinf=300frames/s нужной цепочки и заложили u=0.7, effective210/s:50 камер требуют250/s → минимумceil(250/210)=2 узла;500 требуют2500/s →12. Если другой опыт дал Cinf=1000, effective700 →1 и4. Это условные переменные, не фактические LinQ/RTX параметры; остальные bottlenecks могут увеличить число. Если scheduler разрешает одному запросу за раз и roundtrip100ms, максимум10frames/s на эту связь независимо от compute TOPS;250FPS требуют в среднем ≥25 одновременных requests при100ms cycle,2500FPS ≥250 — поддержку такого K нельзя предполагать.

Fairness: по1 latest-slot/camera, выбирать round-robin с deadline/freshness, per-camera token rate5FPS; batch максимум один кадр на камеру до второго круга, если нужна равная доля. Admission control: заявлять5FPS только для камер, которые помещаются в измеренный budget; при перегрузе управляемо снизить target для всех или явно выбранных приоритетов. Считать delivered useful FPS, inter-result gaps, stale drops и очередь каждой камеры. Per-camera minimum — критерий, иначе aggregate claim вводит в заблуждение.

Архитектура роста: для50 проверить один local ingest/recording host с отдельным inference adapter; для500 разделить по площадкам и shard camera groups, сохранить main recording на объекте, отправлять substream/JPEG по измеренному WAN, централизовать metadata/events. Edge LinQ HX остаётся условным вариантом размещения до подтверждения SDK/decode/memory/сетей; этот research не устанавливает его доступную производительность. N+1/failover требует spare capacity под потерю узла и проверенной реконнекции камер, а не только RAID.

<a id="f197"></a>

## F197 — NVDECODE выделяет decode surfaces по sequence-specific minimum; больше surfaces увеличивает память/конвейеризацию. Output surfaces — отдельный…

**Тип основания:** DOC. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** [S128](SOURCES.md#s128). **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L27](_WORK/W2_06.md); W2-06-F01.

**F197 DOC, S128.** NVDECODE выделяет decode surfaces по sequence-specific minimum; больше surfaces увеличивает память/конвейеризацию. Output surfaces — отдельный максимум одновременно mapped outputs. После обработки требуется unmap; забытый release исчерпывает mappings. CUDA contexts имеют overhead; руководство предлагает делить контексты между sessions. Это опровергает модель «один latest image = вся память камеры». Bytes/camera, предел4070 и настройка LinQ из документа не следуют. Проверено чтение разделов, runtime не исполнен. [NVDEC guide](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.0/nvdec-video-decoder-api-prog-guide/index.html).

<a id="f198"></a>

## F198 — Ресурсы учитывать по host/stage/owner, отдельно RAM и device memory; shared references не считать физическими копиями. Для host h

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L29](_WORK/W2_06.md); W2-06-F02.

**F198 INFERENCE, F197+F042, F043, F044, F045, F046, F047+F170.** Ресурсы учитывать по host/stage/owner, отдельно RAM и device memory; shared references не считать физическими копиями. Для host h:

`M_h = M_base(processes,libs,contexts) + M_demux/parser/jitter + M_decoder(DPB/reorder/surfaces) + M_latest_pool + M_borrowed_inputs + M_retained_view + M_pre/post/scratch + M_outputs + M_view_connections + M_db/index/cache + margin`.

Все члены — bytes, измеряемые на actual backend. Нельзя подставить фиксированные bytes/camera из raw frame. Для GPU нужны actual pitch/alignment/bitdepth/resolution, surfaces и число CUDA contexts; CPU decoder тоже имеет references/reorder/thread scratch. `N*W*H*1.5` NV12 или `N*W*H*3` RGB8 — лишь nominal latest-slot representation без stride, не RSS/VRAM.

| Inventory / owner | Что растёт / измерить | Ограничение/отказ |
|---|---|---|
| Reader processes/threads | Process-per-camera P=N; при sharding P<N. Codec threads/process, stacks, CPU seconds/frame, RSS/PSS/private/shared, handles, restart rate | P/thread budgets.500 процессов не обязательны; camera actors логические в P workers. Shard снижает overhead, расширяет blast radius native hang |
| Sessions/sockets/FD | Upstream connections по profile; relay consumers decode/recorder/native viewers; inference channels/pools; status/fetch; active+closing WS; DB/WAL/log/index/segment files, IPC/pipes | OS process/system limits и camera client cap отдельно. RTSP/TCP interleaved и RTP/UDP имеют разный count; fixed FD/camera неизвестен |
| Decoder/context | Codec/profile/sourceFPS/GOP/reference frames; streams/process/GPU; parser, reorder/DPB, contexts/surfaces; resolution-change maxima | Не снижать required codec buffers ради cap. OOM/reconfigure failure → reject/degraded, release по contract. NVENC cap не NVDEC cap |
| Pools/borrows | Raw latest, immutable admitted frame/JPEG, input tensor copies/pinned memory, output tensors+postprocess scratch | Count AND byte caps. View expiry освобождает view retention, native borrow — только safe release; remote unresolved ledger остаётся |
| Ports/control | Listeners, outbound tuples/ephemeral ports/TIME_WAIT, proxy/NAT table, reconnect rate, query rate | Reuse sessions, finite connect/reconnect budgets.1port/camera не универсальная модель; actual protocols учитывать |
| Recorder/index/storage | Open segments, unique pins, validation/clip jobs, commits/WAL checkpoint, metadata/inode/file count | One recorder owner; finite segment/job/byte policy W2_02. Tmp/derivatives тоже считаются |
| Disk/replay/backup | Append B/s, random IOPS/latency, concurrent export/HTTP reads, validation/hash, backup/checkpoint, derived writes | Запись проверять вместе с replay. `sum(b_i/8)` не disk capability; cache-hit replay не cold-disk throughput |
| Browser/projection | Encode once/source frame, subscribed latest C, active+closing V, historical outstanding payloads, TLS/TCP, bitmap/canvas scratch | W2_03 caps/admission; no per-viewer raw frame. Closing connection занимает budget до cleanup |

<a id="f199"></a>

## F199 — Для viewers v и одновременно выбранных tiles c

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L46](_WORK/W2_06.md); W2-06-F03.

**F199 INFERENCE.** Для viewers v и одновременно выбранных tiles c:

`R_view = 8 * Σ_v Σ_c(selected(v)) f_vc * E[J_vc + header_vc]` bit/s.

Фактическая rate ограничена processed availability, server cap и одним connection credit W2_03; это requested/upper planning budget, не гарантированная выдача. Для native compressed feed вместо JPEG подставить `Σ_vΣ_c b_vc`; новый renderer/transcoding route отдельно. Даже shared JPEG encode не отменяет Vcopies NIC. Replay/clip playback добавляются независимо.

Пример assumptions/LOCAL arithmetic:3viewers×4tiles×2fps×100000B=19.2Mb/s. И при50, и при500 registered cameras будет19.2Mb/s, если selection одинаков.3viewers×500tiles×2fps дали бы2.4Gb/s, такой UI/admission minimum запрещает. При одном outstanding message НА CONNECTION четыре tiles не получают четыре credits:2fps/tile требуют8rendered messages/s/connection и ACK cycle≤125ms в идеальной serial модели. Иначе снизить viewFPS/tiles. Registry500 metadata/recovery/health load сохраняется даже при12visible tiles.

При W2_03 shared C latest + V outstanding + bounded encoder slots дают грубый payload bound `(C+V)*B` для envelope capB, плюс envelope copy если есть. Transport/TLS/kernel/browser buffers не входят. Resource failure → stale/unavailable; hard teardown guarantee до E019 W2_03 нет.

### Направленные50/500 и размещение

<a id="f200"></a>

## F200 — INFERENCE**, дополнение F133/F147, F148, F149. Сценарий: mainH2641080p25=4Mb/s; analysis5fps; JPEG100000B; raw output `[1,84,8400]FP32`=2822400B…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L58](_WORK/W2_06.md); W2-06-F04.

**F200 INFERENCE**, дополнение F133/F147, F148, F149. Сценарий: mainH2641080p25=4Mb/s; analysis5fps; JPEG100000B; raw output `[1,84,8400]FP32`=2822400B ИЛИ compact≤100detections=2404B. Всё условно: JPEG quality для СИЗ и LinQ head не установлены. Реальные links требуют measured goodput/VBR/payload tails/overhead/reserve.

| Участок/направление |50камер|500камер|Условие topology|
|---|---:|---:|---|
|Camera→site gateway main|200Mb/s|2Gb/s|Внутренний ingest, один профиль minimum. Main+sub4+1Mb/s дал бы250Mb/s/2.5Gb/s; industrial option|
|Site gateway→remote, frameAPI JPEG|200Mb/s|2Gb/s|Decode local. Это uplinkAPI, иной участок, чем cameraLAN|
|Remote→site gateway, raw output|5.6448Gb/s|56.448Gb/s|Пример W2_01; return CPU/NMS/bytes caps обязательны|
|Remote→site gateway, compact output|4.808Mb/s|48.08Mb/s|Только packed detections, не analyzed image|
|Site gateway→remote, compressed remote-decode|200Mb/s|2Gb/s|Тот же main4Mb/s. Sampling после decode этот link не уменьшает|
|App host→browser, processed view|19.2Mb/s|19.2Mb/s|3×4selected tiles F199. Если app рядом с LinQ — remote WAN egress|
|App host→viewer replay|`Σ playback bitrates`|`Σ playback bitrates`|Concurrent downloads/seeks сверх live budget|
|Gateway↔remote control|`R_status_up/down + ACK + locators`|Та же формула по outstanding/polling|Зависит от J/Δ/batching. Unknown jobs могут давать control load после live stop|

В принятом сценарии JPEG5fps=4Mb/s равен main4Mb/s: remote-decode uplink saving нет. Если remote decoder возвращает каждый sampled JPEG100kB плюс boxes на site gateway для собственного processed view, **добавляется200Mb/s/2Gb/s downlink**. Из avoid raw tensors не следует «WAN только metadata». Вариант — remote projection и лишь selected tiles браузеру; archive export отдельно. Remote privacy/reachability/persistence — prerequisite.

Для sites s: `N=ΣN_s`; cameraLAN_s=`Σ_i b_source_i`; WAN_s↑/↓ по реально пересекающим границу данным; central link — сумма фактических направлений.500=10sites×50 не отменяет10×traffic в центре. Для50 кандидат один ingest/recording host после E;500 — shards по площадкам с local recording и measured limits, central events/control. Это roadmap, не готовый minimum на500; число LinQ плат неизвестно.

# 12 Адресные передачи и отрицательные результаты

<a id="f211"></a>

## F211 — Адресные передачи

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S131](SOURCES.md#s131). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_01.md:L203](_WORK/W1_01.md); дополнительная тематическая выписка.

## Адресные передачи

- **V03 decode / V04 transfer**: F006 и matrix — HX decoder относится host/RK3588, HPS optional encode не TPU decode. Не обещать аппаратный decoder выданного server. Tensor bandwidth считать по actual dtype/shape, а JPEG только с подтверждённым decoding endpoint и quality test. E005 даёт точную развилку.
- **V05 scheduler / V12 recovery**: общая очередь — независимая ось; Q002 и E007. Не увеличивать native concurrency из количества камер; deadline не cancel. Compose F008, F009, F010 не watchdog зависшей модели.
- **V08 component boundaries / V17 architecture**: один inference adapter с control/data/lifecycle contract, два deployment units; GUI-only остаётся отдельным ограниченным route. Backend/UI/storage не обязательно на той же машине, что device.
- **linq_platform**: Q001, Q003, Q002, Q015 дополняют уже существующие Q001/Q004/Q005/Q025/Q028; нужен issued host/network/lifecycle contract, не повторное SDK исследование. Новые F017/F018 уточняют scopes Astra; F014, F015, F016 помогают deployment gate.
- **evaluation**: отдельный прогон server roundtrip и pipeline age; opaque API не даёт accelerator compute time. F023 45 ч — разность расписания, не resource grant. Успешный device smoke не latency SLA и не полный video quality.
- **operator_product**: viewer/operator/admin и clip auth; доступность camera/inference/очереди и age показываются отдельно, сохранённый кадр явно устаревший. Потеря LinQ не скрывается GPU fallback badge; playback не называется live.
- **market_deployment**: network/data-flow/storage требования и scopes F017, F018, F019, F020; правовую квалификацию не делал. Сертификаты отдельной ОС не переносить на систему.
- **hackathon_strategy**: F023/F024 первично подтверждают публикуемое окно и критерии. Готовый Docker image/данные должны быть описаны как будущая упаковка/учебная проверка, не созданный до старта конкурсный код; общие правила не исследовались сверх узких архитектурных locator.

Ветка достаточна для выбора условной topology/packaging. Оставшийся пробел локализован в actual issued grant/SDK-host pairing и параметрах камер; публичная реклама не заменяет этот контракт. Практические проверки перечислены с границами, ни одна не выдана за выполненную.

<a id="f216"></a>

## F216 — Отрицательные результаты и ограничения получения

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S133](SOURCES.md#s133). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_03.md:L187](_WORK/W1_03.md); дополнительная тематическая выписка.

## Отрицательные результаты и ограничения получения

- PMC browser page вернула reCAPTCHA; MDPI publisher page HTTP429, PDF недоступен web-инструменту. Это не «статья закрыта»: полный XML получен успешно через Europe PMC REST, сохранён и прочитан. Первое декодирование ответа PowerShell показало mojibake для некоторых символов; затем копия скачана непосредственно в файл и корректно разобрана как UTF-8 XML. SHA256 сохранённого XML: `85579DBC38E3821DF7A3B2FC93D6FB651AF3A6320E89BEE673ADB958B0F49251`.
- CVF PDF `...Bhowmik_Lost_in_Compression...paper.pdf` вернул 403; тот же первичный труд прочитан через arXiv HTML/PDF v1. Это одна публикация, не независимые подтверждения.
- DeepStream 8.0 URL перенаправился на недоступный архив; current docs явно 9.2. Никакие version-specific ключи 9.2 не объявлены работающими в 8.0 или на нашем оборудовании.
- Поиск JPEG+hard-hat/PPE не дал в этой ветке первичного контролируемого сравнения с условиями, пригодного для назначения безопасного Q. Две прочитанные работы дают механизм риска, но не числовую гарантию для кейса.
- Не проводились transport benchmarks и оценка JPEG на выбранной модели. Нет сравнимых measured HTTP/gRPC/WebSocket latency, нет фактических LinQ limits, нет вывода о числе поддерживаемых камер. Все такие численные обещания должны оставаться открытыми до E005/E004.

<a id="f225"></a>

## F225 — Адресные передачи

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S134](SOURCES.md#s134). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W1_04.md:L268](_WORK/W1_04.md); дополнительная тематическая выписка.

## Адресные передачи

→linq_platform/V01/V04/V05: полный frame key/opaque request echo, concurrency bounds и runtime execution evidence; F083/F084/F096.
→violation_methods: gaps как unknown, scoped track id, reset, motion gate требует решения; F074/F085/F086/Q005.
→evaluation: decoded/admitted/completed/late/dropped counters отдельно, coverage и order тест E006; F079, F080, F062/F084.
→V09/operator_product: запись независимо от detector FPS, incident before clip-ready, stable event_id/revision; F073/F093/F096.
→V10/V13: Frigate timestamp до pipe read не PTS; Roboflow monotonic process-local; stale overlay; F074/F080/F083.
→market_deployment/model_stack: licenses P01–P08, Roboflow heterogeneous, Ultralytics AGPL, SDK/weights отдельно.
→hackathon_strategy: показать restart/reconnect/backlog и настоящий backend; новый Kafka cluster не нужен без готовой инфраструктуры.

# 13 Conditional minimum45ч: placement, owners, gates, latency

<a id="f204"></a>

## F204 — INFERENCE**, F070, F082, F083, F084, F085, F086, F087, F088, F089, F090, F091, F092, F093, F094, F095, F096 и W2_01..05. Модульное приложение с…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L99](_WORK/W2_06.md); W2-06-F09.

**F204 INFERENCE**, F070, F082, F083, F084, F085, F086, F087, F088, F089, F090, F091, F092, F093, F094, F095, F096 и W2_01..05. Модульное приложение с camera workers, adapter client/worker, одним DB writer, state actors, HTTP/history/projection и standalone websockets17.0.1 listener. MediaMTX1.21.2 — relay. Один H264 video-only профиль через одного demux owner идёт в decode и prospective indexed remux; сначала одна камера, затем две для isolation. B=1,1parent inflight/camera, global request/byte/remote-held caps. Fresh same-generation/model/geometry result применяется по source order; Gap не negative result. Deadline не remote release.

Основной view — analyzed JPEG+own-frame metadata; shared encode once,1outstanding/connection, ACK после draw, active+closing caps, hidden→close/resync. Backend/age/appliedFPS/coverage видны. История из БД, WS не durable event transport. Event list можно обновлять history/revision refresh без отдельного брокера. Одна local evidence directory, snapshot сразу; clip асинхронно pending→complete/partial/unavailable. Одна SQLite DB хранит event/outbox/job ledger/pins/index; filesystem coordination требует W2_05 recovery, не distributed transaction.

| Выданный режим | Minimum placement / prerequisite | Admission/cut |
|---|---|---|
|Frame/image или tensor API|Team app host: ingest/decode/remux/DB/state/UI. Remote: LinQ NN и documented pre/post. Client удерживает same-frame view representation|Actual input/output/model updates/correlation/accepted execution witness. Downlink/postprocess sizing. Ledger intent до send, held через timeout/restart|
|Shell с remote decode|Только при grant own daemon/code/packages/source ingress/CPU/codec/persistent storage/listener/tunnel: **весь app data plane/DB/recorder/projection рядом с decoder** на supplied host; proprietary worker отдельный deployment unit. Team browser получает selected images/events|Один DB/recorder owner, same-demux. Нет remote persistence/lifecycle → local decode + thin remote worker, не скрытая distributed DB. Source ingress, selected preview, archive/backup links считать|
|Shell, но только ephemeral NN process|Team app host как API variant, разрешённый thin worker на supplied host|Shell сама не доказывает remote DB/recording. После session loss lifecycle reconcile; remote-decode minimum не заявлен|
|Job API|Local app + persisted ledger/collector. Queue+poll+fetch входят в полный cycle|Live лишь после freshness/per-cameraFPS/maxgap gate и lifecycle contract. Unknown/unbounded queue→stop/degraded; complete pre-roll не обещать|
|GUI/manual или job без usable outputs/turnaround|Witnessed/offline LinQ run; replay/mock demonstration только с явной маркировкой|**Unsupported-live**. Click automation/CPU/RTX fallback не закрывают real-time LinQ path|

Shell placement условен, не поручение устанавливать web/DB на чужой shared host. Без grant остаётся frame transfer. Output-only events service не равен per-frame adapter. Полный кейс определяет достаточность классов/FPS/dwell/evidence и каждого cut.

<a id="f205"></a>

## F205 — Из F172, F173, F174, F175, F176, F177, F178, F179, F180, F181, F182, F183, F184: tracker optional; ByteTrack reference fixed dt=1/update,…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L113](_WORK/W2_06.md); W2-06-F12.

INFERENCE: окончательное согласование A–E: tracker optional по cadence/reset gate (F172, F173, F174, F175, F176, F177, F178, F179, F180, F181, F182, F183, F184); полный cycle включает postprocess, remote credits не снимаются local Gap. Prospective artifact baseline и SQLite advisory/backup/restore — F185, F186, F187, F188, F189, F190, F191, F192, F193, F194, F195, F196. Общие contracts до параллельной разработки: FrameEnvelope/StreamStatus; InferenceRequest/Result+transforms; JobLedger; OrderedResult/Gap/EpochReset/TrackingReset; EventMutation/revision/coverage; EvidenceManifest/status; processed wire/ACK. Positive/empty/error/late/old-generation fixtures обязательны. Это согласование proposals, не новый runtime факт.

<a id="f206"></a>

## F206 — Часы относительно публикации полного кейса, не времени research.225person-hours не взаимозаменяемы и не доказывают успеваемость. Golden LinQ run…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L123](_WORK/W2_06.md); W2-06-F10.

**F206 INFERENCE.** Часы относительно публикации полного кейса, не времени research.225person-hours не взаимозаменяемы и не доказывают успеваемость. Golden LinQ run выше новых фич; каждый owner интегрирует свои contracts.

|Owner|Основная ответственность|Критический handshake|
|---|---|---|
|1 media|Source/relay/demux/decode, identity/clocks, recorder index/validation|Lineage/snapshot; ранний recorder proof с5; placement с2|
|2 LinQ/model|Issued capability contract, golden input/output/provenance, pre/post reference, adapter/quotas|Real result→3/4; bytes/lifecycle/ownership→5|
|3 temporal|Scheduler/fairness/per-camera admission, gap/state/rules, remote credit machine вместе с5|Ordered contract2; event revisions/coverage→4|
|4 product|HTTP/auth/history/UI, processed WS/renderer/ACK, event cards/degraded states|Same-frame lifetime1/2; DB/outbox contract5|
|5 integration/storage|Single DB writer/recovery, ledger/pins/outbox persistence, package/licenses, metrics/runbook|Unified trace/fixture, DB failure boundary со всеми; evidence gate1|

|Интервал|Integration gate / требуемое доказательство|Cut при fail / приоритет|
|---|---|---|
|0–2ч|Case→required minimum; issued grant/model/network/quotas/CPU/OS; один **real LinQ golden run** с hashes/output/accepted witness; contracts+tinyfixtures|Нет supported automated path→unsupported-live и адресная эскалация missing grant. Mock параллельно tagged. Optional убрать|
|2–6ч|1source→LinQ→own-frame view→event commit→history; freshness/geometry/backend trace. **Ранний E009 same-demux remux proof**; actual SQLite runtime/advisory gate|Remux fail→snapshot+clip unavailable, no exact pre-roll. Tracker gate fail→no opaque tracker/ID-method degraded. Не добавлять второй model до slice|
|6–18ч|2cameras/stalled source; held через timeout/restart; gaps/epochs/no staleboxes; DB/outbox/pin reconciliation; measured cycle подходит rules|Cut native live/messenger/cascade/tracking-dependent extra; cameras/viewrate/profile менять лишь с quality gate. Каждый model/preprocess change повторяет golden|
|18–32ч|Required route под sustainable offered load: per-cameraFPS/maxgap/age, event/evidence outcomes, slow browser, restart/storage faults|Target не проходит→явный admission/degraded. Camera count reduction не лечит p1 single-camera cycle ceiling. Не скрывать gaps aggregateFPS|
|32–40ч|Freeze model/stack; clean-target/offline-client smoke, restore DB+media+ledger reconcile; demo rehearsal/реальная сеть площадки|Core/package/recovery fixes; optional cut. Нет currentLinQ доступа→сохранённый witnessed run с honest replay status, no current-live claim|
|40–45ч|Только regression demo/artifacts/submitassets; walkthrough: backend→event→evidence/status→failure/recovery→metrics|Feature freeze, reproducible runbook. Replay не подменяет live requirement полного кейса|

Optional после core gates: native WebRTC original live; messenger лишь с доступом/authorized tests; blur/reencode derivative; object storage; broker; image-health heuristics; дополнительный tracker/cascade; камеры сверх tested admission. Если exact clips обязательны полным кейсом, failing recorder gate — **blocker**, snapshot cut не означает исполненного требования. Ни snapshot, ни remux route не доказаны как feasible45ч.

Recorder route выбирается один: после успешного gate — custom indexed remux; после fail его отключить, оставить snapshot. Если native archive полезен отдельно, включить только его recorder вместо custom, с `mapping=unknown`; два параллельных recorder не входят в minimum и не создают доказанного mapping.

<a id="f207"></a>

## F207 — INFERENCE**, F132/W2_01/W2_03/W2_04. Ни фиксированного LinQ milliseconds, ни sum(stagep95). `L_result` — доusable actor result; `L_video` — own…

**Тип основания:** INFERENCE. **Фактически проверено:** сохранённые источники/код прочитаны исследователями; collector прочитал сохранённую запись. Арифметика — локально вычислено, если явно указано ниже. Runtime/предлагаемые commands/configs: **не запускалось**.

**Основание/контекст:** INFERENCE/LOCAL по аналитическому источнику и связанным F ниже. **Сохранённый аналитический источник:** [S142](SOURCES.md#s142). Версия, units, условия, ограничения и связи — в извлечении.

**Происхождение:** [_WORK/W2_06.md:L148](_WORK/W2_06.md); W2-06-F11.

**F207 INFERENCE**, F132/W2_01/W2_03/W2_04. Ни фиксированного LinQ milliseconds, ни sum(stagep95). `L_result` — доusable actor result; `L_video` — own frame доcanvas draw (physicalscreen отдельно); `L_alarm` — physical onset довыбранной delivered границы. SLO покаUNKNOWN. Same-host duration monotonic(run/host); sourcePTS дляordering/dwell при корректной шкале; remote stage timings — reported local durations, не cross-host subtraction.

|Stage|FrameAPI|Shell/remote decode|JobAPI|Clock/status; bound/failure|
|---|---|---|---|---|
|Exposure→ingress|Camera encode+network+relay|Camera encode+compressedWAN+relay|По input route|Sensor ageUNKNOWN; sourceUTC лишь calibrated. Optical/watermark. Read timeout не bound sensor age|
|Decode/pre/sample|Local decode+resize/encode/pack|Remote decode+preprocess|Local prep либо supplied videojob|Host monotonic после E. Continuous sourceFPS decode. Caps backlog; timeout→Gap/stale|
|Scheduler|Local fair admission|Remote scheduler|Local intent+submit|Local duration; count/byte/held caps. Age deadline→drop, не remote release|
|Upload/submit|InputWAN/client|CompressedWAN уже выше, runtimeIPC|Upload+submitack|Client roundtripobservable, one-wayunknown. Ambiguous→unknownledger|
|Remotequeue|Opaque servicequeue|Own worker+shareddevice contention|Pending/starting queue|UNKNOWN без issued timings; Kboundedwork не boundwait. No terminal contract→boundedstop|
|NN/post|RemoteNN; raw return/localpost либо compact|NN+hostpost|JobNN/outputs|Server/runtime clock; actual model/parity gate. Caps tensors/crops; invalid не successfulFPS|
|Return/collect|WAN+parse/post|HostIPC state|Poll visibility+fetch+post|Full per-cameraL. Ideal poll extra[0,Δ) лишь periodic/nooutage assumption. Late→history/unavailable|
|Rules/DB|Ordered localstate+DB|Colocated state+DB|Local aftercollector|Dwell source clock; duration local. Commit success before eventcommitted. Gap→unknown; diskfull→notcommitted|
|Processedvideo|Retainframe→encode→WS→browser|Remote projection→selectedJPEG WAN|Freshresult либо historical|Sender/browser clocks отдельно.1credit limits appqueue, not physicalscreen; hide/timeout→close/stale|
|UIalarm|Commit→projection/history→render|То же плюс WAN|После collector|RenderACK/optical отдельно от send. Alarm не ждёт clip, reconnect→history|
|Messenger optional|Outboxwait→provideraccept|То же|То же|Rate/retry/backoff; accept не read. Humanack отдельный endpoint, finitehumanresponse нет|
|Clipready|Pin→postroll→close→validate→commit|Same-demux на remote app host|Finite acceptance для late|W2_02 bounds conditional onGOP/progress/IO; deadline→partial/unavailable, не initialalarmlatency|

Суммы ниже для **одного trace**, с frame age до admission ровно один раз:

`L_result_API = ingress_age + decode/pre + local_admission + upload + remote_queue + NN + output_download + post + ordered_apply`.

`L_result_shell = compressed_ingress_age + remote_decode/pre + remote_admission + shared_device_wait + NN + host_post + IPC_apply`. Если state остался укоманды, добавляются serializedresult И retainedimage return; это отдельный разнесённый contract, не выбранный minimum.

`L_result_job = input_prep + local_admission + upload/submit + job_queue/start + job_run + terminal_visibility + poll_detection + fetch + post + ordered_apply`. Completedjob ещё не usableclientresult. ДляGUI/manual `L_result_live` как supported automated budget не определён.

`L_video_processed = own-frame_to_usable-result + projection/encode_wait + send/transit + browser_decode/draw (+ compositor/display)`; browserFPS может быть ниже inferenceFPS. Native originalvideo если добавлен имеет иной path без ожиданияNN, не analyticslatency.

`L_alarm_onset = sampling/onset_uncertainty + dwell_qualification + eligible_observation_processing + commit + alarm_delivery` только при явных semantics без doublecount. Идеальный periodicΔ: firsthit[0,Δ); kpositive observations добавляют(k−1)Δ только безdrops/regularcadence. Physical dwellD не completioncount. ОтсчётD отphysicalonset и отfirst observed positive имеет разное квантование. Gap→unknown/interrupted; shortevents могут пропускаться. Сохранять onset→alarm иrule-eligible→alarm отдельно, misses/timeouts/censoring сполнымdenominator. p95total из end-to-end traces/совместимыхhistograms, не сумма независимыхstagep95.
