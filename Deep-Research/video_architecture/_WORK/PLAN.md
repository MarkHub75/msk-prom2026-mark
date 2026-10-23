# План video_architecture

2026-10-23 06:09 +03:00. Контракт mosprom-research-v1, оба входа прочитаны полностью. Эта папка — итоговая папка темы. Вход Context-prompt.md соответствует упомянутому Context Prompt.md.

Конвейер: план → W1 → fresh-context critic → W2 → collector → author → editor → machine compressor. Отдельной финальной проверки нет. Интернет получают только Medium-исследователи. Три агента одновременно (четвёртый слот — корень), очереди задач. Шесть заданий W1 охватывают 15 самостоятельных исследовательских ячеек V01–V16 (V15/V16 объединены как deployment/security); V17 — синтез автором. Это группировка связанных вопросов, а не сокращение охвата.

- W1_01: V01 удалённый LinQ, V15 упаковка/ОС, V16 безопасность; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_01.md.
- W1_02: V02 ingest/RTSP, V03 decode; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_02.md.
- W1_03: V04 транспорт удалённых кадров, V05 scheduler; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_03.md.
- W1_04: V06 образцы проектов, V07 tracking state, V08 разделение/шина; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_04.md.
- W1_05: V09 хранение клипов, V10 браузер и синхронизация, V11 тревоги; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_05.md.
- W1_06: V12 resilience, V13 measurement, V14 50/500 capacity; владелец — отдельный gpt-6.1-sol/medium, результат _WORK/W1_06.md.

Каждому исследователю переданы полный контракт, контекст и самостоятельный вопрос. После W1 отдельный критик gpt-6.1-sol/high без истории прочитает входы/результаты, создаст CRITIC.md с K-ID. W2 формируется по его конкретным пробелам. Collector нормализует S/F/Q/E и provenance; author пишет русский черновик; editor финальный русский; compressor английский с YAML и каталогом. Все эти роли — отдельные агенты gpt-6.1-sol/high с последовательным владением файлами.

## Карта 15 ячеек

| Ячейка | Направление входа | Решение и ожидаемое знание | Владелец/файл |
|---|---|---|---|
| A01 | V01 | Топология SSH/API/shared queue/GUI; признаки выбора и размещение decode/state | W1_01 |
| A02 | V15+V16 | Воспроизводимое offline развёртывание, ОС/device permissions, TLS/secrets/network boundaries | W1_01 |
| A03 | V02 | RTSP/file relay, timeout/reconnect/buffering, исходный код backend | W1_02 |
| A04 | V03 | Decode/sample/preprocess placement, первичные измерения с границами переноса | W1_02 |
| A05 | V04 | Payload/protocol/RTT/concurrency/compression tradeoffs | W1_03 |
| A06 | V05 | Много камер/моделей: admission, fairness, deadlines, batch wait | W1_03 |
| A07 | V06 | Каталог образцов с version/license/hardware/reuse | W1_04 |
| A08 | V07 | Per-camera state, media clocks, gaps/ordering/restart | W1_04 |
| A09 | V08 | Компоненты и event contract, durable delivery/outbox, цена bus | W1_04 |
| A10 | V09 | Ring segments/pre-postroll/keyframes/retention/storage | W1_05 |
| A11 | V10 | Browser codecs/NAT/sync, точная привязка overlay к кадру | W1_05 |
| A12 | V11 | Техническая доставка тревоги, retries/idempotence/limits | W1_05 |
| A13 | V12 | Failure states/recovery and honest degraded demo | W1_06 |
| A14 | V13 | FPS/age/e2e latency/stage clocks/drop metrics and test evidence | W1_06 |
| A15 | V14 | Сеть/decode/compute/storage50/500 и unknown LinQ capacity | W1_06 |

V17 формируется High-автором из обеих волн: схема45ч, интерфейсы,5владельцев, integration checkpoints и промышленный рост. Новая сеть для него — только в W2 по критику. Соседние отчёты используются как вторичная передача с первичным происхождением; отсутствующие результаты не блокируют ячейки.

## W2 после fresh-context critic (возобновление)
Исходный critic сохранён в CRITIC.md, K001–K010. Выбраны шесть групп из CRITIC_HANDOFF, без повторного обзора достаточно установленных веток. W2_01–03 работают первыми, затем04–06. W2_06 завершает интеграционные условия после чтения01–05; это часть второй волны, не новая проверочная стадия. Все сетевые роли medium, остальные роли high. Потенциально неподдерживаемый GUI/job live режим будет явно ограничен, а неизвестные параметры LinQ не заменяются аналогами.

Обновлённые решения: remote credits должны переживать local timeout/restart; event–record mapping требует явного индекса/uncertainty; finite disk означает finite evidence acceptance; processed view требует bounded per-viewer render-credit; per-camera ceiling1/L отдельно от aggregate; bundle prospective до smoke install. Collector назначает стабильные S/F/Q/E и сохраняет первоначальные K без ретроспективной правки.
