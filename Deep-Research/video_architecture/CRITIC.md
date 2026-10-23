# Независимая критика первой волны video_architecture

Дата исходной критики: 2026-10-23, 07:33 Europe/Moscow (+03:00). Роль: отдельный fresh-context critic, gpt-6.1-sol/high. Прочитаны полностью `Context-prompt.md`, `prompt-video-architecture.md`, `_WORK/PLAN.md`, `_WORK/W1_01.md` … `_WORK/W1_06.md`. Мнение оркестратора из RUN_STATE не читалось. Новые сетевые материалы, практические прогоны и дополнительные агенты не использовались. Это анализ сохранённых результатов, а не независимое повторение их веб-получения.

## Исходная критика — сохранять неизменной после W2

Все замечания ниже относятся к состоянию **до второй волны**. Наличие замечания не означает установленную ошибку библиотеки или LinQ. Там, где речь о нашем предлагаемом прототипе, это незакрытая инженерная связь между уже известными механизмами. P0 — влияет на возможность обещать работающий обязательный маршрут/полноту доказательства; P1 — влияет на выбор реализации или предел применимости; P2 — полезное ограниченное дополнение. Приоритет не превращает открытый вопрос о недоступном устройстве в обязанность добыть его публичным поиском.

### Что уже достаточно установлено

1. **Матрица доступа и границы LinQ.** W1_01 не путает VPN с правом запуска, SSH с Docker/root, HPS encode с HX/RK3588 decode, корпоративный SLA с выдачей хакатона. Использование соседнего `linq_platform` явно вторично, его CPU/mock-пробы не выданы за запуск на устройстве. `W1-01-S01/F01–F04`, новые первичные `S02–S04/F05–F07` и актуальные scopes Astra `F17/F18` достаточны для условной топологии. Повторный обзор рекламных страниц не закроет actual access contract.
2. **Приём и декодирование.** W1_02 даёт практические параметры и контрпримеры: единицы timeout, open-only OpenCV settings, неподдержанный BUFFERSIZE в конкретном backend, независимые очереди GStreamer/appsink, PyAV timeout/close, loop publisher и transport TCP с обеих сторон. Различие полного decode и downstream sampling объяснено. Это существенно лучше общего совета «сделать очередь на один кадр».
3. **Транспорт и допуск.** W1_03 достаточно обосновывает бинарные payload, переиспользование соединений, bounded count/bytes, независимость batch wait/RPC timeout/freshness, fair per-camera admission и ограничения каскада. HTTP/gRPC/WS обоснованно не ранжированы без общего benchmark. Нужен adapter под выданный контракт, а не предварительное объявление Triton совместимым с LinQ.
4. **Каталог проектов.** Восемь записей W1_04 уже имеют snapshot/version, license scope, hardware и конкретный reuse. Не нужно добавлять Shinobi/ZoneMinder/Viseron только ради списка из исходного промпта. Уместно брать архитектурный образец, а не переносить целый NVR или NVIDIA runtime под неизвестный LinQ.
5. **Состояние и доставка.** W1_04 хорошо разделяет volatile frames и durable events, camera/epoch/frame identity, order реально отправленных кадров, gap как unknown, reset opaque tracker и восстановление event/outbox. MQTT QoS/Kafka idempotence/SSE reconnect не выданы за атомарную внешнюю доставку. Это достаточная основа модульного монолита без нового брокера.
6. **Клипы и UI.** W1_05 правильно различает segment и part, keyframe alignment и frame-accurate export, pending/partial clips, pin и retention. Совпадающий JPEG+metadata processed view — уже содержательно обоснованный безопасный минимум. Безопасность WebRTC overlay не обещана без mapping, WHEP не выдан за финальный RFC. Telegram/MAX — дополнительные каналы с явно ограниченными гарантиями.
7. **Измерения и 50/500.** W1_06 разделяет source/decode/sample/valid-result/render FPS, разные clock domains, successful-only latency и потери/цензуру. Числа хранения и трафика имеют SI units и явные допущения; 500 камер не объявлены возможностями одной платы. Чужие NVDEC/DeepStream цифры сохранены с условиями и запретом переноса. Условная арифметика полезна уже сейчас.

**Не требовать от W2 выдуманной полноты.** Применимого CPU/QuickSync decode-only числа для неизвестного компьютера нет; W1-02-F25 и E02 являются честным результатом. Без реальных frames/model нет допустимого JPEG Q для каски/сигареты; две статьи W1-03-S11/S12 устанавливают риск, а не универсальный порог. Нет измеренных здесь WebRTC/LL-HLS/ботовых миллисекунд, native thread safety или LinQ FPS. Оставить эти пункты как адресные Q/E; новый обзор похожего железа не сделает их нашими измерениями.

### Покрытие вопросов и направлений

| Вопрос тематического задания | Покрытие W1 / V-направления | Что требуется дальше |
|---|---|---|
| 1. Режимы LinQ | W1_01, V01 | Достаточная условная матрица; K001 уточняет долгоживущие jobs |
| 2. Камеры/файлы/RTSP | W1_02, V02 | Достаточно для выбора ingress; версия поставки — K007 |
| 3. Decode720/1080 и placement | W1_02 + W1_06, V03 | Честно ограниченные vendor numbers и E; не требовать переносимого per-core ответа |
| 4. Payload/protocol/quality | W1_03, V04 | Обратное направление/raw outputs — K006 |
| 5. Много камер/моделей | W1_03 + W1_06, V05 | Remote lifecycle K001 и per-camera предел K005 |
| 6. Готовые проекты | W1_04, V06 | Каталог достаточен; выбранный reuse pin/license — K007 |
| 7. Temporal state | W1_04, V07 | Основной контракт достаточен; variable-FPS tracker — K005 |
| 8. Компоненты/шина | W1_04, V08 | Достаточно по границам; actual DB durability — K008 |
| 9. Evidence/storage | W1_05 + W1_06, V09 | Сквозная шкала K002 и конечная retention policy K003 |
| 10. Browser/sync | W1_05, V10 | Выбрать processed-view минимум и ограничить весь путь — K004 |
| 11. Отказы | W1_06 + W1_01/02/04/05, V12; тревоги V11 | Strong failure matrix; незавершённые jobs K001, camera tamper K009 |
| 12. Performance/latency | W1_06, V13 | Достаточный протокол; единый по режимам бюджет — K010 |
| 13. 50/500 | W1_06 + W1_03/05, V14 | Калибровка и арифметика достаточны; return/view/connection costs — K006 |
| 14. Deploy/offline/Astra | W1_01, V15/V16 | Scope Astra установлен; конкретная поставка и durability — K007/K008 |
| 15. Прототип45ч | W1_04/05, V17 как синтез | Пока набор разумных частей; минимальный маршрут, owners/gates/cuts — K010 |

V11 покрыт отдельной ветвью уведомлений W1_05; V16 — ограниченной security/data-flow схемой W1_01. Ни один из них не потерян из-за отсутствия отдельного номера среди 15 основных вопросов. Главный остаток — связность выбранного пути, а не отсутствие ещё одного обзора каждого слоя.

### K001 — App timeout не освобождает удалённый job: нужен учёт неизвестного terminal state

- **Приоритет:** P0. **Группа:** W2-A.
- **Места:** W1_01, матрица «Shared queue/job service», lifecycle policy, `W1-01-Q03/E04`; W1_03, `F04/F06/F17`, scheduler пп.2/6/9 и `Q02`; W1_04 `F16/F18`; W1_06 `F13`. Основания: `W1-03-S04/S06`, `W1-01-S01` как вторичная передача о неизвестном lifecycle.
- **Проблема:** верно сказано, что timeout/cancel task не доказывает остановку backend. Но нет конкретного инварианта, связывающего локальный semaphore, удалённую quota и перезапуск клиента. Если после каждого timeout освободить локальный slot и отправить свежий кадр, bounded local inflight может сосуществовать с растущим числом ещё работающих remote jobs. Перезапуск приложения может потерять даже известные job IDs. Circuit breaker и latest slot этого не устраняют.
- **Последствие:** shared service исчерпывает quota или продолжает оплачиваемую/занятую работу; восстановление создаёт новый storm. В job-only режиме обещание bounded resources пока не доказано.
- **Недостающее доказательство:** первичный конкретный async-job lifecycle с submit/status/cancel/terminal/TTL semantics, а для LinQ — явный unknown до выдачи. Нужен наш согласованный ledger/credit protocol, включая timeout-before-submit-ack и crash-before-persist-job-id.
- **Точное задание W2:** исследовать один релевантный документированный job API как аналог и его ограничивающие условия; не собирать ещё каталог облаков. Составить state machine `not_submitted/submitting/accepted/running/unknown/terminal`, раздельно local call slots и remote outstanding credits. Показать, когда допустим новый submit, как poll/reconcile идёт после restart, как хранить request/job IDs, что делать без idempotent submit/status/cancel/TTL. Если bounded continuation без контракта невозможно — stop admission/escalation как явный результат. Предложить короткий fake-job fault fixture; не исполнять нагрузку на общий стенд.
- **Закрытие:** конкретный ledger и проверяемые инварианты либо явно признанный неподдерживаемый автоматический resume; реальные LinQ limits остаются Q, а не догадкой из аналогичного API.

### K002 — Frame/event time ещё не связан с временем реально записанных сегментов

- **Приоритет:** P0. **Группа:** W2-B.
- **Места:** W1_02 `F11/F14/F28`; W1_04 `F15/F18/F28`; W1_05 `F05/F06/F08/F19/F20`, `Q02–Q04`. Источники: `W1-02-S12/S13`, `W1-05-S04/S05/S14`, Frigate timestamp counterexample `W1-04-S01/F05`.
- **Проблема:** camera epoch/media_time определены в decoder, а recorder предлагается отдельной encoded-ветвью, потенциально в MediaMTX. Не установлен механизм, которым конкретный closed segment получает диапазон именно **этой** шкалы. Hooks/имя файла/host UTC не автоматически дают исходные PTS. MediaMTX может заменять absolute timestamps; recorder и decoder могут переподключиться независимо. `camera_id + время в имени файла` не достаточно, чтобы вырезать доказательство нужного кадра.
- **Последствие:** event с корректным frame_id может ссылаться на другой проход loop, другой GOP или неполный интервал. Ошибка не обнаруживается тем, что файл успешно открывается. При main/sub различиях одна геометрия и относительные секунды также не доказывают соответствие.
- **Недостающее доказательство:** путь record-time → source PTS/epoch для одного выбранного pinned recorder. Нужны точные поля hook/API/segment metadata либо явно ограниченный способ построить mapping; не обещать поля, которых API не отдаёт.
- **Точное задание W2:** проследить первичную документацию и нужный код MediaMTX v1.21.2 по timestamp/recording/playback/hooks, сопоставить с уже полученными FFmpeg/PyAV. Выбрать минимальный маршрут: один общий demux owner с remux index **либо** отдельный recorder с доказанной mapping и measurable uncertainty. Дать пример manifest и trace: original PTS/time_base, event media time, record interval, decoder/recorder generation. Разобрать PTS reset/wrap, loop, отдельный restart recorder, missing timestamps и main/sub; не сводить разные discontinuities к одному неподтверждённому epoch. Не требовать exact native WebRTC overlay, если минимум выбирает atomic processed frame.
- **Закрытие:** алгоритм разрешения одного event interval в конкретные original segments с обнаружением unknown/partial; непроверенная точность остаётся E, а аппаратные UTC часы не предполагаются.

### K003 — Конечное кольцо не покрывает неограниченную задержку remote queue и бесконечное событие

- **Приоритет:** P0 для promises evidence; P1 для расширенных политик. **Группа:** W2-B.
- **Места:** W1_05 `F06/F08/F09`, `Q01/Q03/Q06`; W1_01 shared-queue matrix; W1_06 `F15` (10s ring как сценарная арифметика). Источники `W1-05-S04–S06` достаточны для исходного механизма; числового worst-case от LinQ нет.
- **Проблема:** полезная формула `ring > pre + worst_case_event_arrival_delay + close_delay + margin` не задаёт политику, когда worst-case неизвестен/неограничен. Late result можно сохранять offline, но его pre-roll уже может быть удалён. Продолжающийся event также может непрерывно расширять pins; quota pins упомянута, но при её исчерпании не выбран порядок деградации. Default hour-long segment делает даже малое кольцо и быстрый export условными.
- **Последствие:** система либо обещает недоступный pre-roll, либо незаметно перестаёт быть кольцом и заполняет диск. Редкий длинный queue delay ломает аккуратный happy path.
- **Недостающее доказательство:** конечный контракт live/evidence acceptance и реально поддержанная настройка recorder: segment close semantics, безопасное извлечение части открытого fMP4, если оно вообще выбирается, и crash recovery.
- **Точное задание W2:** определить отдельные максимумы live age, evidence lookback, ожидания post-roll/close и длительности одного evidence job; выбрать rollover ongoing incidents/частичные клипы/явный reject late evidence. Рассчитать ring при заданном конечном bound; при отсутствии bound прямо перечислить, чего нельзя гарантировать. Уточнить pinned version настройки короткого recording segment и ключевых кадров; сравнить самостоятельный export с native playback/export без написания всего продукта. Дать порядок действий при low space/pin quota, repair после crash и ручном удержании. Только проектные числа с маркировкой, без SLA LinQ из воздуха.
- **Закрытие:** bounded disk и job lifecycle с явным partial/unavailable исходом, в том числе при задержке больше кольца и продолжающемся многочасовом event.

### K004 — Atomic JPEG+metadata решает correspondence, но ещё не ограничивает очередь доставки в браузер

- **Приоритет:** P1; P0 если processed view объявляется оперативным control view. **Группа:** W2-C.
- **Места:** W1_05, главные решения п.3, `F16–F22`, `E03/E04`; W1_03 `F05` про framework buffers; W1_04 `F14` про frame lifetime. Источники `W1-05-S13/S16`, `W1-03-S05/S07`.
- **Проблема:** server mailbox≤1 не предотвращает backlog уже переданных в WS/TCP messages, очередь async JPEG decode в браузере и удержание исходных frames до inference result. При slow/hidden tab или нескольких viewers network send может «успеть» лишь в buffer. WS `bufferedAmount` браузера описывает другое направление. Синхронные image+boxes могут быть идеально совпадающими, но секундной давности.
- **Последствие:** основной рекомендованный 45ч view скрыто теряет freshness и RAM, даже если inference scheduler bounded. Smooth UI/atomic message не доказывают актуальность.
- **Недостающее доказательство:** конкретный поддержанный способ server send/backpressure/ack в одной выбранной библиотеке, cap на retained payload и browser decode/render state; absolute sensor age неизвестен без clock mapping.
- **Точное задание W2:** найти первичные API для одного предполагаемого Python ASGI/WS stack, включая send completion semantics, queue/size/timeout и disconnect. Предложить простой latest-only протокол с не более одного outstanding displayed-frame credit на viewer либо иной доказуемо bounded вариант, ACK после render, sequence/epoch, cap bytes, send timeout и reconnect resync. Разделить per-viewer drop и analytics drop. Проверить, нужен ли retained source image на каждый inflight request и как освободить его после timeout/late result. Задать slow-browser/hidden-tab/multiple-viewer fixture. Не проводить полный обзор медиапротоколов заново.
- **Закрытие:** bounded memory и возраст по всем app-owned буферам; то, что нельзя ограничить внутри TCP/browser, приводит к disconnect/drop и видимому stale status, а не обещанию exact latency.

### K005 — Выбор «один inflight/камера» и переменного sample FPS ещё не сведен с temporal/tracker контрактом

- **Приоритет:** P0. **Группа:** W2-D.
- **Места:** W1_03 `F17`, scheduler пп.2/7/8, `Q03/Q05`; W1_04 `F16/F17/F18`, `Q02`; W1_06 `F14/F15`, max-capacity formula; W1_02 `F19/F20`. Источники scheduling аналогов `W1-03-S02/S08–S10`; конкретный tracker пока не выбран.
- **Проблема:** один inflight/камера упрощает ordering, но даёт отдельный bound `f_camera <= 1 / L_camera`. Например, при cycle300ms это максимум около3.33fps независимо от глобального K и числа других камер. Формула Nmax с глобальным `K/(f_a*L)` сама по себе этот предел не отражает. Ещё важнее: внешний tracker может считать возраст/динамику в update count при фиксированном dt; передача PTS в envelope не заставляет библиотеку учитывать переменные интервалы или gaps.
- **Последствие:** обещанные условные5fps могут быть невыполнимы по каждой камере при достаточном aggregate FPS. На редких/нерегулярных updates меняются track lifetime/velocity и episode continuity, даже без перестановки результатов.
- **Недостающее доказательство:** точный temporal contract одного пригодного минимального tracker либо обоснование маршрута без обязательного opaque tracker; для реального минимального FPS нужен полный кейс/соседняя evaluation, это не закрывается публичным поиском.
- **Точное задание W2:** проверить pinned code/docs одного лёгкого reference tracker (не выбирать модель детекции заново): где dt, lost age, frame count, reset и empty update; различить absence observation и no detection. Составить таблицу `L → per-camera fps ceiling → sequential или bounded reorder` и условия `min FPS/max gap` для scheduler. Если конкретный tracker нельзя корректно адаптировать к dt, предложить ограниченный фиксированный sampling contract/явный reset либо оставить Q. Уточнить Nmax/admission для per-camera cap и cascade jobs. Подготовить traces с delayed/reordered ответами и long gaps; не заявлять измеренное качество ID/re-ID.
- **Закрытие:** temporal data path учитывает реальные интервалы или явно ограничен проверяемыми предпосылками; source FPS, sampled FPS и per-camera fresh-result FPS не взаимозаменяются.

### K006 — В 50/500 нет завершённого бюджета result-return, viewer fanout и control-plane ресурсов

- **Приоритет:** P1. **Группа:** W2-A (return) + W2-F (сводный sizing).
- **Места:** W1_03 `F01/F16/F17`, adapter result schema; W1_01 tensor API matrix; W1_06 `F15` min-resource formula и рост; W1_05 `F09/F20`. Источники `W1-03-S01`, `W1-06-S03`; actual output tensors LinQ неизвестны.
- **Проблема:** тщательно рассчитан upload input, но return от API может быть raw multi-head tensor, decoded boxes либо state/events. При raw outputs локальный postprocess/NMS и downlink могут стать новым bottleneck. Browser egress умножается на число viewers/tiles независимо от числа analysed frames. 500 camera workers также имеют OS processes/FD/decoder contexts/surfaces, которые не сводятся к одному raw latest slot. Общая формула допускает измеренные mcam/Cwrite, но текущие примеры не дают читателю границ этих пропущенных слагаемых.
- **Последствие:** ошибочный placement NMS/decoder, заниженный WAN downlink/view egress/RAM и преждевременная экстраполяция от одного потока к500. Это не делает уже верную input/storage арифметику неверной.
- **Недостающее доказательство:** конкретный sample response/schema либо параметрическое описание возвращаемого payload; первичные примеры размещения postprocess. Реальные LinQ output shapes/precision остаются вопросом поставки.
- **Точное задание W2:** добавить `R_return=8*N*f*E[output_bytes]`, query/poll traffic и result CPU; сравнить raw outputs с compact detections, дать один явно условный арифметический пример с перечисленными shapes/dtypes. Вычислить viewer egress как число одновременных выбранных tiles×bitrate/fps/bytes и показать, что500 registered cameras не означают500 tiles каждому оператору. Расписать per-process/per-stream resource inventory, pool/decoder buffers, open sessions, files/ports и IO replay; без выдуманного bytes/camera коэффициента. Свести50/500 по участкам и направлениям линков, отдельно от compute unknown.
- **Закрытие:** нет единственного числа «нужна сеть X» без топологии; недоступные величины явно остаются переменными/измерениями.

### K007 — Каталог snapshots достаточен, но выбранного согласованного release bundle пока нет

- **Приоритет:** P1. **Группа:** W2-E.
- **Места:** W1_02 `S02/S08–S13/S17` (FFmpeg n8.0, OpenCV4.13, PyAV16.0.1, stable docs9.0.2, MediaMTX1.21.2); W1_04 `P01–P08/F03/F24/F27`; W1_05 `S05/S09/F13` (server tag и reader HEAD разные); W1_01 packaging/Astra gate.
- **Проблема:** snapshots хорошо маркированы, но они ещё не один совместимый install target. Приведённые интерфейсы могут относиться к внешнему FFmpeg n8, встроенным libav wheel и разным MediaMTX reader/server; Docker docs — current, Astra packages — конкретные. Catalog license repo не заменяет license фактически bundled wheels/binary codecs/weights. В Roboflow nearest superseding LICENSE оставлен открытым, хотя code-reuse и pattern-only routes различаются.
- **Последствие:** будущий developer может принять весь набор прочитанного за готовый requirements lock и потратить45ч на несовместимые API. При offline поставке особенно важно знать, что именно сохранять/распространять.
- **Недостающее доказательство:** узкий prospective baseline со stable tag/commit и поддержанными APIs; не обязательно устанавливать его сейчас. Нужен manifest типов artifacts/лицензий, а proprietary LinQ bundle остаётся условным.
- **Точное задание W2:** для минимального route из K010 проверить первичные release/code metadata MediaMTX server+reader **одной версии**, PyAV/встроенный FFmpeg vs CLI binary, Python и выбранную web/DB библиотеку. Отметить exact pins/architecture и unknown installability; не обновлять все проекты до latest. Отдельно `used as process/dependency/copied code/idea only`, direct license и dependencies/weights unknown. Nearest Roboflow license проверять только если предлагается конкретное копирование/import; иначе оставить pattern-only и не продолжать чужую license ветку ради полноты. Фактический smoke install — будущий E, не сочинённый статус теста.
- **Закрытие:** один reviewable provisional manifest и compatibility gates; catalog сохраняет dev snapshots как evidence, а не заменяет ими release selection.

### K008 — Durable outbox нуждается в выбранной DB/FS durability и процедуре backup/recovery

- **Приоритет:** P1. **Группа:** W2-E.
- **Места:** W1_04 `F24/F25`, `E02/E04`, `S15/S16`; W1_05 `F08/F23`, `E02`; W1_01 `F21` и offline bundle. W1 не обещает power-loss durability, но слово durable должно получить конкретную область.
- **Проблема:** одна транзакция устраняет разрыв event/outbox, но сохранность commit зависит от DB settings/storage и обработки disk-full/commit error. SQLite WAL имеет sidecar files/checkpoint и ограничения snapshots; image tar не backup. Сейчас нет выбранного restart/backup recipe, согласующего event rows, clip manifests/pins и ФС.
- **Последствие:** после восстановления могут появиться event без evidence, потерянные pending pins или outbox, который был показан оператору до успешного commit. Тест kill процесса не закрывает питание/ФС, что W1 верно отмечает.
- **Недостающее доказательство:** первичные SQLite WAL/backup/durability документы и текущие version/patch caveats для рекомендуемого SQLite route, либо соответствующая scope-модель PostgreSQL при его выборе. Нужен минимальный согласованный recovery.
- **Точное задание W2:** уточнить выбранные journal/synchronous/busy/foreign-key/one-writer настройки как проект, без утверждения успешной конфигурации на неизвестной ФС; проверить supported backup API/online backup и restore с WAL. Не рекомендовать просто копировать открытый `.db`. Задать commit success boundary, disk-full failure action, DB–clip index reconciliation, stale lease recovery и что живёт только volatile. Развести process crash, host reboot, power loss, disk loss; расширять гарантию только при соответствующем доказательстве. Сохранить короткую текущую version advisory проверку, не обзор всех БД.
- **Закрытие:** понятные пределы durable commit и воспроизводимая proposed backup/restore procedure; SQLite не объявлен автоматически надёжнее/ненадёжнее PostgreSQL без условий.

### K009 — Camera tamper покрыт только repeated/frozen frame, остальные симптомы не разобраны

- **Приоритет:** P2, не blocker LinQ MVP. **Группа:** W2-F, ограниченная подзадача.
- **Места:** V12 тематического промпта; W1_06 `F09/F13`, заключительная граница «camera tamper classification не исследована как модель качества»; W1_02 `F14/F26/F28`.
- **Проблема:** watchdog absence/progression и image similarity не покрывают чёрный/засвеченный кадр, расфокус и сдвиг камеры. При этом статическая сцена и loop-file легко дают ложный frozen alert. Эти функции не обязательны по полному кейсу, которого нет, но исходное направление остаётся реально частичным.
- **Последствие:** нельзя писать «мониторинг исправности камер» так, будто все перечисленные случаи доказанно определяются; можно ограничиться availability/staleness и явно показать suspected image anomaly.
- **Недостающее доказательство:** один первичный эксплуатационный пример camera-health/tamper checks с условиями/ограничениями, без исследования нового detector.
- **Точное задание W2:** коротко разделить transport dead/frozen timestamps/repeated image/black/overexposure/blur/scene shift, дешёвый наблюдаемый signal и главные контрпримеры. Указать scope45ч: обязательны progress/age, image health опционален и имеет статус suspected; thresholds зависят от сцены, искусственный loop отдельно. Если полезного первичного материала нет — оставить точную границу покрытия, не строить ML-модель и не назначать универсальные thresholds.
- **Закрытие:** честный scope camera health и E с контролируемыми corrupt/black/static/loop samples; качество tamper detector остаётся вне доказанного.

### K010 — Синтез45ч ещё должен принять решения о минимуме и бюджете каждого режима

- **Приоритет:** P0 для окончательной рекомендации. **Группа:** W2-F; финальное изложение — High author, не новый исследовательский отчёт W2.
- **Места:** W1_04 `F01/F14–F19/F28`, распределение5участников; W1_05 practical scope45ч; W1_01 матрица/два deployment units; W1_03 scheduler; W1_06 `F14/F15` и proposed SLA. Утверждение PLAN, что V17 аналитичен, разумно, но не снимает интеграционные неизвестные выше.
- **Проблема:** в совокупности предлагаются отдельные reader workers, relay, scheduler/adapter, actor state, DB/outbox, segment index/pins/retention/clip worker, WS processed view, возможно native WebRTC, notifier и packaging/security. Это правдоподобный набор, но ещё не минимальный проверяемый vertical slice с порядком cuts. «Работает в каждом вероятном режиме» требует исключения GUI-only/job-only без машиночитаемого результата/приемлемой очереди. Там не всегда возможно реализовать live продукт заменой одного adapter.
- **Последствие:** автор может неявно пообещать лишние функции/параллельную интеграцию за45ч и представить неизвестный remote queue budget как фиксированные миллисекунды. Реальная работа из пяти человек не равна автоматически225 взаимозаменяемым person-hours.
- **Недостающее доказательство:** для плана — инженерная связка уже найденных механизмов; новая сеть нужна только узким implementation gaps K001–K008. Нужны конечные contracts/fixtures, входные prerequisites и go/no-go gates, а не доказательство будущих трудозатрат.
- **Точное задание W2:** подготовить автору одну минимальную conditional topology с API/frame и shell/remote-decode variants, явной unsupported-live веткой GUI/job limitations. Выбрать основной analyzed view, одну БД, один recorder route; отметить optional native live/messenger/blur/object storage. Дать owners5 и integration gates в интервалах0–2/2–6/6–18/18–32/32–40/40–45ч как план, критерии сокращения scope и приоритет real LinQ golden run. Свести per-access-mode budget таблицей `stage / local or remote clock / measured or unknown / resource bound / failure`, отдельно sampling+dwell, video view и alarm. Не суммировать stage p95 как p95 end-to-end, не выдумывать задержки. Сформировать компактный набор discriminating E, объединяя дубли W1, и указать, что успешный mock/media test не подтверждает LinQ.
- **Закрытие:** из материалов можно дать последовательное действие в первый час и честно назвать режим, в котором real-time пока невозможно. Это проектный маршрут, а не заявление, что45ч feasibility уже экспериментально доказана.

### Рекомендованные группы второй волны

Группы — содержательные задания, не требование шести одновременных агентов. Каждая использует уже прочитанные W1 и сохраняет результат отдельно. Для всех: Medium при получении новой сети; DOC/CODE/CLAIM/MEASURED/LOCAL/INFERENCE/UNKNOWN раздельно; не запускать приложение/крупные benchmarks, не отправлять сообщения и не получать закрытый доступ от имени пользователя.

| Группа / рекомендуемый файл | K-ID | Самостоятельные вопросы и результат |
|---|---|---|
| **W2-A Remote lifecycle и return path** — `_WORK/W2_01.md` | K001, return-часть K006 | Persisted remote-job credits/reconciliation; opaque API fallback; result tensor/downlink/postprocess placement. Один точный документированный job-service аналог, без повторного LinQ SDK поиска |
| **W2-B Recording clocks и bounded evidence** — `_WORK/W2_02.md` | K002, K003 | Source↔recorder epoch/time mapping; short-segment/export primitive pinned MediaMTX; конечная retention/ongoing-event/late-result policy |
| **W2-C Processed view под slow browser** — `_WORK/W2_03.md` | K004 | Конкретный WS stack, per-viewer credits/timeout/drop и source-image lifetime; native WebRTC только если найден узкий useful mapping, не новый общий обзор |
| **W2-D Temporal state и per-camera feasibility** — `_WORK/W2_04.md` | K005 | Один pinned lightweight tracker/dt/gap/reset контракт; per-camera inflight/RTT/FPS bound, bounded reorder options, E с нерегулярными наблюдениями |
| **W2-E Поставка и DB recovery** — `_WORK/W2_05.md` | K007, K008 | Узкий coherent version/artifact/license manifest; DB durability/backup/restore/reconcile. Astra/native LinQ compatibility остаётся exact supplied-config gate |
| **W2-F Capacity extensions и handoff45ч** — `_WORK/W2_06.md` | view/resource-часть K006, K009, K010 | Дополненная topology50/500 с viewer/control/decoder-resource variables; ограниченный camera-health scope; synth-ready minimum/owners/gates/budgets/объединённые E |

W2-F может начать с W1, но финальные integration prerequisites должны учитывать результаты A–E. Не требуется ждать их, чтобы получить независимый короткий материал по camera health и недостающим sizing terms. W2-E pin selection согласуется с B/C, не создаёт третий медиасервер или ещё одну web framework. При нулевом новом доказательстве узкий пункт становится Q/E, а не запускает бесконечную замену агентами.

### Реально открытые вопросы, которые W2 не должна притворно закрывать

- Issued LinQ grant: custom model/update/version, allowed code/daemon lifecycle, API payload/output/pre/post, queue fairness/quota/terminal/cancel/TTL, ports/reachability, CPU/RAM/ISA/storage и accepted execution evidence. Ответ постановщика + конкретный артефакт/первый тест. Публичный аналог даёт проектную политику, не значения этих параметров.
- Full-case sources/classes/event onset/dwell/minimum FPS/max gap/required freshness, evidence window/retention и обязательные deliverables. Материалы анонса — примеры, не полное ТЗ.
- Exact team/remote CPU/GPU/VRAM/OS/driver/decoder build, доступный WAN/RTT и сеть площадки. Это inventory/измерение, не числа по имени RTX4070.
- Целевой RGB PPE codec/resize quality и event recall на пропусках кадров; actual LinQ full-chain throughput при нужной свежести. Сохранить программы E, не подставлять FLIR/COCO/NVIDIA измерения.
- Credentials/accounts/permission для мессенджера, сертификаты/turn media route, конкретная камера firmware/security и power-loss durability. Ни один future authorized practice шаг не выдать за выполненный.

## Результаты обработки после W2

Этот раздел намеренно пуст до второй волны. Collector добавляет для каждого K-ID статус `закрыто / уточнена область / противоречие / осталось открытым / потеряло значение`, новые W2/source/fact IDs, что изменилось в рекомендации и сохраняемую неизвестность. Исходный раздел выше не переписывается. Это учёт обработки критики, не финальный аудит отчётов.


## Collector: результаты содержательной W2 (2026-10-23)

Исходный раздел критики выше сохранён byte-for-byte; нижние статусы относятся только к последующей обработке. Это не финальный аудит отчётов. Новых сетевых или runtime доказательств collector не получал. `Закрыто как proposal` не означает выполненный эксперимент.

<a id="k001-w2"></a>

### K001 — Уточнена область; проектный пробел закрыт, LinQ lifecycle остаётся открыт

**Результат W2 / изменение решения:** AWS Batch даёт конкретное ограничение cancel200/attempt timeout/history retention. Persisted intent+held до возможного send, separate local/control/fetch budgets, ambiguous submit и restart traces, finite STOPPED. Local deadline/Gap/source reset не release remote obligation; stale backup не held=0. Не требуется ждать всех unknown, если свободный остаток доказан; при недостоверном ledger/namespace stop.

**Доказательства и проверки:** [F134](RAW_FACTS.md#f134) [F136](RAW_FACTS.md#f136) [F138](RAW_FACTS.md#f138) [F139](RAW_FACTS.md#f139) [F143](RAW_FACTS.md#f143) [F144](RAW_FACTS.md#f144) [F145](RAW_FACTS.md#f145) [F146](RAW_FACTS.md#f146) [F170](RAW_FACTS.md#f170) [F195](RAW_FACTS.md#f195) [Q002](OPEN_QUESTIONS.md#q002) [E007](OPEN_QUESTIONS.md#e007) [E016](OPEN_QUESTIONS.md#e016).

**Сохраняемая неизвестность:** LinQ idempotency/lookup/quota/terminal/TTL/acceptance cutoff и borrowed-buffer release неизвестны; fake fixture не выполнен.

<a id="k002-w2"></a>

### K002 — Уточнена область; runtime exact mapping остаётся открыт

**Результат W2 / изменение решения:** Pinned MediaMTX mtxi сильнее UTC filename, но StreamID — recorder generation, не decoder/source epoch. Hooks/API не отдают необходимые lineage поля; native get теряет mtxi, HTTP200 не полнота. Preferred prospective route — один demux, packet index до mux rebase, distinct generations, independently validated coverage. Early E009 обязателен; fail→analyzed snapshot/native archive mapping unknown.

**Доказательства и проверки:** [F150](RAW_FACTS.md#f150) [F152](RAW_FACTS.md#f152) [F153](RAW_FACTS.md#f153) [F154](RAW_FACTS.md#f154) [F155](RAW_FACTS.md#f155) [F158](RAW_FACTS.md#f158) [Q010](OPEN_QUESTIONS.md#q010) [E009](OPEN_QUESTIONS.md#e009) [E018](OPEN_QUESTIONS.md#e018).

**Сохраняемая неизвестность:** Packet lifetime/reorder/rescale/missing PTS/main-sub uncertainty не испытаны. Если exact clips обязательны, snapshot cut остаётся blocker.

<a id="k003-w2"></a>

### K003 — Закрыто как bounded project policy; operational полнота открыта

**Результат W2 / изменение решения:** Finite evidence acceptance от EARLIEST anchor, post-roll monotonic deadline, bounded close/job/chunks/rollover/incident bytes, persisted future pins/reservations и low-space/crash lifecycle. Unbounded queue не покрывается finite ring. H40s и bounds20/5/5/2/1/4/30 — fixture assumptions, не LinQ SLA/кейс.

**Доказательства и проверки:** [F151](RAW_FACTS.md#f151) [F156](RAW_FACTS.md#f156) [F157](RAW_FACTS.md#f157) [F159](RAW_FACTS.md#f159) [F160](RAW_FACTS.md#f160) [F161](RAW_FACTS.md#f161) [Q011](OPEN_QUESTIONS.md#q011) [Q012](OPEN_QUESTIONS.md#q012) [E010](OPEN_QUESTIONS.md#e010) [E016](OPEN_QUESTIONS.md#e016).

**Сохраняемая неизвестность:** Actual GOP/max bitrate/FS/close/dispatch bounds, evidence requirements и real result delay неизвестны; no false-complete/byte/lifetime tests не выполнены.

<a id="k004-w2"></a>

### K004 — Уточнена область; DOC/CODE/project часть закрыта, runtime открыта

**Результат W2 / изменение решения:** Выбран standalone websockets17.0.1 asyncio route. Credit занят ДО send, один outstanding/connection, exact ACK после draw, serial sender/renderer, active+closing cap, immutable latest/history payloads, hidden→close/latest resync, local credit-cycle guard и source/view lifetime раздельны. Timeout terminal, не новый credit. send/drain/ping/browser bufferedAmount не renderer evidence.

**Доказательства и проверки:** [F162](RAW_FACTS.md#f162) [F163](RAW_FACTS.md#f163) [F164](RAW_FACTS.md#f164) [F165](RAW_FACTS.md#f165) [F166](RAW_FACTS.md#f166) [F167](RAW_FACTS.md#f167) [F168](RAW_FACTS.md#f168) [F169](RAW_FACTS.md#f169) [F170](RAW_FACTS.md#f170) [F171](RAW_FACTS.md#f171) [Q013](OPEN_QUESTIONS.md#q013) [E011](OPEN_QUESTIONS.md#e011) [E012](OPEN_QUESTIONS.md#e012).

**Сохраняемая неизвестность:** App-owned bytes bound не process/kernel/browser total RSS; public close_timeout не hard teardown guarantee. Experimental transport.abort subclass не public WS API; physical display/read/actual network/SDK borrowing открыты.

<a id="k005-w2"></a>

### K005 — Противоречие timestamp-only гипотезе установлено; область исправлена, quality открыто

**Результат W2 / изменение решения:** Pinned ByteTrack dt1/update; constructor frame_rate меняет lost buffer, no-call останавливает aging, real empty(0,5) меняет track state. PTS envelope не исправляет динамику. Minimum tracker optional по fixed-cadence/reset gate, separate tracking_generation; ID-dependent метод без gate degraded/unsupported. Per-camera1/E[L] с NMS/cascade/apply отдельно от aggregateK; sparse sent-ID reorder и независимый timeout wakeup.

**Доказательства и проверки:** [F173](RAW_FACTS.md#f173) [F174](RAW_FACTS.md#f174) [F175](RAW_FACTS.md#f175) [F176](RAW_FACTS.md#f176) [F177](RAW_FACTS.md#f177) [F179](RAW_FACTS.md#f179) [F180](RAW_FACTS.md#f180) [F181](RAW_FACTS.md#f181) [F182](RAW_FACTS.md#f182) [F183](RAW_FACTS.md#f183) [F184](RAW_FACTS.md#f184) [Q005](OPEN_QUESTIONS.md#q005) [Q007](OPEN_QUESTIONS.md#q007) [Q021](OPEN_QUESTIONS.md#q021) [E006](OPEN_QUESTIONS.md#e006).

**Сохраняемая неизвестность:** Domain minFPS/maxgap/dwell/ID quality, installability и real full cycle неизвестны; code read не measured tracker quality.

<a id="k006-w2"></a>

### K006 — Параметрический пробел закрыт; actual capacity остаётся открыта

**Результат W2 / изменение решения:** R_return, raw/compact shape example, polling/status/fetch CPU/RAM добавлены отдельно от input uplink. Viewer fanout по selected tiles, не registered camera count. Complete memory/process/FD/session/DPB/surfaces/pool/IO replay+backup inventory. Directional50/500; remote decode с local processed projection добавляет analyzed JPEG return либо требует granted colocated app data plane.

**Доказательства и проверки:** [F147](RAW_FACTS.md#f147) [F148](RAW_FACTS.md#f148) [F149](RAW_FACTS.md#f149) [F197](RAW_FACTS.md#f197) [F198](RAW_FACTS.md#f198) [F199](RAW_FACTS.md#f199) [F200](RAW_FACTS.md#f200) [F181](RAW_FACTS.md#f181) [Q022](OPEN_QUESTIONS.md#q022) [Q025](OPEN_QUESTIONS.md#q025) [E005](OPEN_QUESTIONS.md#e005) [E008](OPEN_QUESTIONS.md#e008).

**Сохраняемая неизвестность:** Actual output/model profiles, WAN↑↓/goodput/tails, LinQ Cinf/Kremote и OS/resource coefficients не measured. Нет числа плат/500-camera guarantee.

<a id="k007-w2"></a>

### K007 — Уточнена область; coherent provisional manifest есть, installability не доказана

**Результат W2 / изменение решения:** Выбраны MediaMTX1.21.2 server+optional same-tag reader, PyAV16.0.1, CPython3.12.15 source candidate, websockets17.0.1, linked patched SQLite3.51.3/source_id gate. CLI FFmpeg и wheel libav разные artifacts. Linux wheel read-only inspected с native library/license strings; wrapper BSD не весь bundle. Used-as-process/dependency/copied-code/idea-only и exact expected hashes в manifest.

**Доказательства и проверки:** [F185](RAW_FACTS.md#f185) [F186](RAW_FACTS.md#f186) [F187](RAW_FACTS.md#f187) [F188](RAW_FACTS.md#f188) [Q015](OPEN_QUESTIONS.md#q015) [Q016](OPEN_QUESTIONS.md#q016) [E015](OPEN_QUESTIONS.md#e015).

**Сохраняемая неизвестность:** CPython source-only, actual binary/ABI/OS/ISA/images/SQLite linkage/transitive notices/weights/proprietary bundle неизвестны. No install/smoke; W1 catalog не lockfile.

<a id="k008-w2"></a>

### K008 — DB/backup/reconcile proposal закрыт; operational durability открыта

**Результат W2 / изменение решения:** Одна local SQLite DB/one writer, WAL+FULL/FK/bounded busy и successful COMMIT boundary, patched engine gate. Long reads/WAL/checkpoint и disk-full учтены. Supported Connection.backup + verified closed-media inventory/holds/cutoff; restore fences owners, проверяет DB/FK/media, rebuild pins до deletion и reconciles remote obligations после old backup. File publish/delete — отдельный protocol.

**Доказательства и проверки:** [F186](RAW_FACTS.md#f186) [F189](RAW_FACTS.md#f189) [F190](RAW_FACTS.md#f190) [F191](RAW_FACTS.md#f191) [F192](RAW_FACTS.md#f192) [F193](RAW_FACTS.md#f193) [F194](RAW_FACTS.md#f194) [F195](RAW_FACTS.md#f195) [F196](RAW_FACTS.md#f196) [Q012](OPEN_QUESTIONS.md#q012) [Q015](OPEN_QUESTIONS.md#q015) [E016](OPEN_QUESTIONS.md#e016).

**Сохраняемая неизвестность:** Actual FS/VFS/cache/sync, runtime code, power/disk-loss, RPO/RTO не tested. FULL/hash/atomic rename не универсальная сохранность; старый backup не release remote work.

<a id="k009-w2"></a>

### K009 — Уточнена область; scope gap закрыт, threshold quality открыта

**Результат W2 / изменение решения:** Первичный Axis product example с unsuitable/lighting/occlusion/legitimate move ограничениями. Разделены transport dead, stale PTS, repeated content, black/underexposed, overexposure, blur, scene shift и counterexamples. Mandatory progress/age; optional image signals only suspected_anomaly с per-scene baseline, suitability и CPU budget.

**Доказательства и проверки:** [F201](RAW_FACTS.md#f201) [F202](RAW_FACTS.md#f202) [F203](RAW_FACTS.md#f203) [Q023](OPEN_QUESTIONS.md#q023) [E019](OPEN_QUESTIONS.md#e019).

**Сохраняемая неизвестность:** Не испытаны actual камеры/сцены/heuristics; нет universal thresholds/causal tamper proof. Overexposure candidate — наш hypothesis, не заявленная Axis capability.

<a id="k010-w2"></a>

### K010 — Закрыто как последовательный conditional engineering proposal; real feasibility открыта

**Результат W2 / изменение решения:** Одна модульная app topology, bounded scheduler/actor, actual LinQ adapter, one SQLite writer, early-gated same-demux remux или snapshot cut, own-frame processed view. Per-access placement, unsupported-live GUI/job,5owners, gates/cuts0–45ч, per-mode stage/clock/bound/failure budgets и discriminating E сформированы с finalW2_01..05. Golden real LinQ run приоритетен.

**Доказательства и проверки:** [F204](RAW_FACTS.md#f204) [F206](RAW_FACTS.md#f206) [F207](RAW_FACTS.md#f207) [F205](RAW_FACTS.md#f205) [Q001](OPEN_QUESTIONS.md#q001) [Q005](OPEN_QUESTIONS.md#q005) [Q024](OPEN_QUESTIONS.md#q024) [E001](OPEN_QUESTIONS.md#e001) [E018](OPEN_QUESTIONS.md#e018).

**Сохраняемая неизвестность:** Нет полного кейса/grant/actual golden/full-chain prototype/effort proof.2camera не50/500,225person-hours не schedule feasibility; обязательный exact clip нельзя закрыть необязательным snapshot.
