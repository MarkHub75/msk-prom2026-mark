# W2-K — IVA CV: промышленная интеграция и граница видео

Назначенные вопросы: K016, K017, K019, K018. Фактическая проверка: 23.10.2026, 05:03–05:09 Europe/Moscow (02:03–02:09 UTC; времена запросов Python зафиксированы в HTTP_LOG.json). Исторический контекст: подготовка команды из пяти разработчиков к 45-часовому хакатону. RUN_STATE на начало ветки не содержит предоставленного SDK/устройства/режима онлайн-доступа. Изучены оригинальное задание, CRITIC, W2_K_PROMPT, W1_14_RESULT и актуальный RUN_STATE. Никакого SDK-install, container pull, компиляции, device run, входа в registry, регистрации или переписки не было.

## Решение

**Готовый публично воспроизводимый PPE-пайплайн IVA CV на актуальном H1M не установлен.** Документированный LinQ-вариант контейнерного узла существует, но SKU/runtime/model manifest и связь с ПАК ОТПБ не опубликованы в прочитанных источниках. Переносимы разделение сервисов и порядок развёртывания; модели/конфигурация/доступ/права должны быть поставлены отдельно.

**Существенное исправление W1:** `walkers-node:0.1.310` — почти наверняка артефакт склейки номера следующей страницы `10` к тегу `0.1.3`. Два новых извлечения TinyFish сохраняют `0.1.3` и отдельную границу страницы, а web extraction склеивает их. Это исправление текстового чтения, **не визуально подтверждённое чтение PDF**. Не переносить `0.1.310` в рецепт как установленный version literal. Аналогичные склейки обнаружены у других контейнеров.

## Факты и границы доказательства

### W2-K-F01 — Версия образа: исправление извлечения, а не найденный новый release

S01, админ-guide, печатные p9–10, раздел 6. Сохранённое HTML-извлечение содержит конец блока `ivacv.tech:15444/common/walkers-node:0.1.3</p>` и следующий блок `<p>10`. Повторное Markdown-извлечение независимо по вызову также даёт `0.1.3`. Web-text показывает `0.1.310` на переходе P8–P9. Аналогично:

| Компонент | Page-separated extraction | Слипшийся web-text | Следующая печатная страница |
|---|---|---|---|
| walkers-node | `0.1.3` | `0.1.310` | 10 |
| ivacv-service-node-cuda | `0.7.8` | `0.7.811` | 11 |
| edge-api | `0.3.10` | `0.3.1012` | 12 |
| vdms-api | `0.5.22` | `0.5.2214` | 14 |
| vdms-ui | `0.3.2` | `0.3.218` | 18 |

Не существует полученного image digest или registry-ответа, подтверждающего любой из этих тегов как доступный артефакт. Пока нет PDF bytes/render, для документационного примера использовать **`0.1.3 (по извлечению с границами страниц; визуальное подтверждение не получено)`**, а для настоящего запуска — выданный matching digest. Полные извлечения сохранены в ADMIN_GUIDE_EXTRACT.json и ADMIN_GUIDE_MARKDOWN_EXTRACT.json. SHA256 этих файлов фиксирует именно наши представления текста, не оригинальный PDF.

### W2-K-F02 — Generic TPU-гипотеза частично опровергнута; H1M/PPE-связь остаётся неизвестной

S01, p9: непосредственно перед примером присутствует подпись «с использованием Linq TPU». Следовательно, весь смысл LinQ-примера не выведен только из имени `/dev/tpu0`. Одновременно p2 использует прежнее обозначение IVA (TPU), p5 — Linq; ни H1, ни H1M, ни HPD, ни версии TPU driver/runtime/compiler в извлечении не установлены. Документ не имеет найденной внутри даты/номера редакции. Дата каталога uploads/2026/05 не датирует содержащуюся в нём команду.

Проверено в текущей HTML-странице S02: она называет LinQ среди поддерживаемых чипов, но список NN runtimes отдельного TPU runtime не содержит. В ней Linux kernel >=6.1, тогда как PDF >=6.0. Это две несогласованные спецификации общего продукта, а не современная ABI-матрица. Нельзя ни объявить пример устаревшим только по слову IVA, ни объявить его совместимым с H1M только по слову LinQ.

S03 (новость интегратора 19.06.2026) явно связывает ПАК ОТПБ, LinQ и контроль СИЗ. Однако в тексте и извлечённых ссылках нет контейнерного тега/digest, перечня моделей, runtime, конфигурации или протокола измерения. Наличие LinQ в промышленной новости и LinQ в общем руководстве не устанавливает идентичность сборки. Tenant `cbr`, имя `walkers-node` и CUDA-пример другого project namespace не доказывают ни PPE-состав, ни deployment у названного заказчика.

Статус: primary documentation + vendor statement; исполнения не наблюдалось. Это уточнение W1, а не новое аппаратное подтверждение.

### W2-K-F03 — Переносимый состав поставки и конкретный порядок развёртывания

S01 p6–20: общие каталоги, MongoDB replica-set, Edge-api, проектный videoanalytics node, VDMS-api, VDMS-ui. Документированный порядок старта: MongoDB → Edge-api → видеоаналитика → VDMS-api → VDMS-ui. Установка включает импорт дефолтной БД и настройку справочников, а не только `docker run` NN-контейнера.

Из LinQ-примера пригодны для сопоставления поставки следующие литералы: `IVA_CONFIG` из `config-patch.json`; `IVA_ENABLE_INSTALLER=0`; `IVA_TENANT="cbr"` (пример); `IVA_EDGE_SERVER="edge-api-1:16000"`; `IVA_EDGE_SERVER_WS="ws://edge-api-1:9001/datahub"`; mapping `/dev/tpu0:/dev/tpu0`; общий host-каталог `/msdata/shared` в `/app/msdata/shared` и `/app/msdata/data`; temp/logs mounts. Полная команда находится в сохранённом source extraction; мы не предлагаем запускать её на выданном сервисе без согласованной поставки.

**Неполученные обязательные части matching deploy:** actual images и digests; `config-patch.json`; project NN models/weights/compiled programs; внутренняя конфигурация `/app/msdata/config`; default DB dump и справочники; service scripts; драйвер/runtime для конкретного TPU и инструкция host/container ABI; ключи API и разрешённые методы; разрешение использовать поставку в требуемой среде. PDF говорит о проектной сборке vendor, следовательно, восстановить эти assets из общих названий невозможно.

Для воспроизведения после получения поставки: сначала зафиксировать manifest и права, подготовить matching host+driver+Docker/каталоги/пользователя, импортировать и настроить MongoDB, настроить Edge-api, затем videoanalytics с выданным конфигом, VDMS-api/UI. После старта документ требует отдельной функциональной проверки UI и тестовой видеоаналитики с камерами/файлами/API. Прохождение UI не доказывает TPU execution; нужно дополнительно связать NN-вызовы, устройство и результаты.

### W2-K-F04 — Где проходит граница video/event, и где она не раскрыта

По S01 p8–16, без вывода скрытой реализации:

| Стадия | Что документировано | Чего документ не устанавливает |
|---|---|---|
| Вход | Videoanalytics component получает камеры/файлы/другие видеопотоки | Codec, decoder, транспорт/буферы, reconnect, частота анализа |
| Decode/preprocess | Общий перечень hardware video decode/encode support p5 | Нельзя распределить decode по каждому перечисленному чипу; нет конкретного LinQ decode API/BOM |
| Нейросети | Проектная сборка включает NN, code, config; LinQ device mapping p9 | Имена NN, opset/input/output, TPU coverage, fallback, batch/scheduler |
| Tracking/rules | Узел обрабатывает pipeline и отдаёт события/изображения/видео | Где выполняются NMS/tracker/PPE-association, temporal debounce/rules |
| Приём результатов | Edge-api принимает данные узлов и сохраняет в MongoDB; REST/WS/gRPC | Payload schema, acknowledgement, дедупликация и идемпотентность API |
| Обработка событий | VDMS-api содержит job очереди событий, её recovery-настройку | Полная queue semantics, delivery guarantee, end-to-end latency |
| Просмотр/архив | VDMS-api транслирует UI-видео, включает/выключает muxers, архивирует/удаляет данные; UI — static frontend через nginx | UI FPS не измеряет NN FPS; video retention не queue depth |

**Новый конкретный lesson:** VDMS `eventsProcessorJobIntervalMs` приведён с примером `500`, `eventsProcessorStuckRestartSec` — `10`. Это интервал job и срок перезапуска незавершённой обработки записи после аварийного остановa, не обещание event latency 500 ms и не device inference timeout 10 s. `streamMonitorJobIntervalMs` управляет мониторингом realtime muxers, а не обязательным NN sampling. `dataCleanupStreamsKeepHours` пример `0.5` относится к хранению видеоданных. См. source p14–15 и ключи в ADMIN_GUIDE_EXTRACT.json.

UI event filters из S04 (13-page guide, PDF p6–7) включают каску/жилет/опасную зону/сигарету/дым/телефон, однако список UI не раскрывает вычислитель каждой NN или правила формирования события. Параметр `defaultVisibleEventTypes` в серверном guide регулирует видимость типов для пользователей, а не набор запущенных моделей. API-control (`apps`, `appsAccess`, `apiMethods`, WS `topics/messages`) также является частью конфигурации и не даёт готового публичного inference endpoint.

Статус таблицы: documented process/service boundaries. Называть все эти стадии host CPU некорректно: сервисы находятся вне доказанного NN-вычисления, но внутреннее CPU/device распределение не опубликовано. Наличие RTSP и слова decode в общей документации **не доказывает LinQ silicon decode**. Ускоритель/remote SDK хакатона может принимать только тензоры, это вопрос отдельного access contract.

### W2-K-F05 — Multi-camera условия, которые реально можно перенести

S01/S04 поддерживают камеры/несколько окон, общие медиакаталоги, streams/frames/crops/chunks и проектные compute nodes. Из этого нельзя вывести допустимое N камер: нет codec, bitrate/resolution, analysis FPS, CPU/RAM/device quota, fairness, очереди кадров, timestamp policy или benchmark. Минимальные 8 GB RAM/256 GB disk в PDF — общие требования платформы, не sizing под N PPE-камер.

**Наш условный adapter/эксперимент**, а не функция IVA/LinQ SDK: bounded per-camera queue, явный drop policy, сохранение camera/frame/source timestamps, reconnect без накопления старого видео; замер age каждого кадра и event delay по каждой камере. Чтобы разделить decode и inference, прогнать один и тот же clip с реальным источником и заранее подготовленными входами при одинаковом NN sampling; добавить камеры до роста age или потерь и измерить host CPU/network отдельно. Записывать cold start, decode/preprocess, queue/batch wait, inference, NMS/tracker/rules, delivery/VDMS polling раздельно. Никаких численных performance ожиданий из материалов IVA CV не выводится.

### W2-K-F06 — Доступ/лицензия: конкретная коммерческая поставка, неизвестные права

S02 прямо выделяет стоимость лицензий платформы/модулей, внедрения и поддержки. S01 описывает отдельный project/customer repository и набор приложений/config/models. Публичное руководство доступно для чтения; open-source sample, license/EULA для `walkers-node`, условия anonymous pull, права на изменение/копирование weights или redistributing image в открытом submission не найдены в targeted поиске и прочитанных ссылках. Это **UNKNOWN**, не доказанный запрет исполнения.

URL `ivacv.tech:15444` и `pull.sh` не являются grant of access/license. Registry endpoint не проверялся: отсутствие полученной поставки/разрешения на конкретный image сделало probing образов бесполезным для нынешнего решения. Не предпринимались auth attempts, token guessing, обходы или обращения к людям.

Минимум, меняющий route: разрешение запуска командой в данном host/cloud; доступ пяти разработчиков; возможность изменять pipeline/config; условия использования/выгрузки weights/compiled artifacts; что разрешено публиковать в source/submission (свои adapters и ссылки на поставку либо также binaries). Эти права нужны отдельно для платформы, TPU runtime и моделей; privacy policy формы не заменяет их. До ответа architecture lessons переносимы, turnkey commercial product route остаётся условным.

### W2-K-F07 — Видео не просмотрено; четырёхсетевой показ не стал multi-stream test

S05 открыта web и TinyFish: interview page 09.07.2025, Владислав Николаев, AQserv + LinQ HPD, описание four-network show. TinyFish HTML-output имеет `Video file`, но не возвращает playable source/iframe (iframe_links=[]); Python HTTPS fetch страницы завершился TLS EOF, HTTP — RemoteDisconnected. Targeted search Rutube/интервью не дал доступного проверенного media record с содержанием технического показа. **Аудиовидео не просмотрено/не прослушано, таймкодов нет.** Аннотация не повышена до наблюдения стенда. Партнёрский анонс Aquarius из W1 не повторно считается независимым post-event test.

## Новая зацепка, которая сужает ошибочное чтение «СИЗ»

W2-K-S06 — отдельный старый официальный пользовательский guide IVA CV **1.8**, 71 PDF page, filename 2021.07.22 (дата имени не равна доказанной дате публикации). Прочитан раздел 6, PDF P20 / печатная p21: «СИЗ на лицах» означает медицинские маски и COVID-19 mask regime; это не доказательство industrial helmet/respirator detector или его TPU execution. Старое руководство не следует смешивать с текущим 13-page UI guide и админ-конструктором. Новый источник добавляет версионный контекст продуктовой семантики, но не независимый аппаратный protocol.

## Реестр источников и lineage

Все источники первичные по авторам, кроме отсутствующего direct test. Дата доступа W2 — 23.10.2026 около 05:03–05:09 MSK. Источники S01–S05 совпадают с lineage W1-14; новый fetch — не новое независимое execution evidence.

- **W2-K-S01:** Когнитив Солюшнс / IVA CV, «Руководство администратора», 20 pages, дата/редакция не найдены. https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf . Прочитан полный text по web + два TinyFish extraction, relevant locators p5–20 выше. PDF bytes не получены. Визуальной проверки нет. Локальные файлы ADMIN_GUIDE_EXTRACT.json (SHA256 `3F843267267952EC5856CBE9035FE3B4AAF606974C8E61D3F19B89A4C2D74F38`) и ADMIN_GUIDE_MARKDOWN_EXTRACT.json (`20051FD9ED9164B9EAAEF5BDE95A731356E290DCDEFF2DA0FF448EEDA1494597`). Это hashes extracted representation, не hash PDF.
- **W2-K-S02:** Когнитив Солюшнс, «Платформа», undated. https://ivacv.ru/platforma/ . Технологический стек, лицензии и ссылки на guides. Web + live TinyFish (ttl=0), PLATFORM_EXTRACT.json. Другая страница того же vendor; не independent runtime test.
- **W2-K-S03:** тот же интегратор, новость ПАК ОТПБ, metadata published `2026-06-19T11:00:29+03:00`. https://ivacv.ru/когнитив-солюшнс-представили-свой-па/ . Current page + metadata/links, INDUSTRIAL_EXTRACT.json. Vendor statement, без manifest/logs.
- **W2-K-S04:** IVA CV, «Руководство пользователя», 13 pages, undated/version unidentified. https://ivacv.ru/wp-content/uploads/2026/05/Руководство-пользователя-сайт.pdf . Web-text PDF p6–10; UI semantics, не execution.
- **W2-K-S05:** Global Digital Space / Владислав Николаев («ХайТэк»), «Лира: ИИ-комплекс для задач искусственного интеллекта», 09.07.2025. https://gdspace.ru/interview/2391 . Web + TinyFish metadata `ср, 07/09/2025 - 08:31`, VIDEO_PAGE_EXTRACT.json. Только описание записи; авторский комментарий/аннотация, не video viewing.
- **W2-K-S06:** ООО «ИВА Когнитив», «Руководство пользователя IVA CV 1.8», 71 pages, filename includes 2021.07.22. https://ivacv.ru/wp-content/uploads/2024/03/2021.07.22__Руководство_пользователя_IVA-CV_1.8.X-—-v2.pdf . Web extraction, relevant complete section 6 at PDF page21; source version established by internal repeating heading. Publication date not established. This older guide is new W2 primary material, but same vendor lineage and no modern LinQ proof.

## Негативные попытки и статус наблюдения

1. Direct requests.get к обоим current PDF, platform page и video page: TLS `UNEXPECTED_EOF_WHILE_READING`; результаты, UTC timestamps и URL в HTTP_LOG.json. HTTP video-page alternate: RemoteDisconnected. Ошибка transport не доказывает отсутствие страниц.
2. Direct unencoded PDF open сначала internal error; click по реальной ссылке на странице platform затем открыл полный web-text. URL encoding/retrieval channel действительно меняет доступность.
3. Web screenshot current guide PDF P8/P3, затем повтор P8: вернулись только ссылки/citation refs, ни image bytes, ни видимого изображения. Ничего не объявлено визуально прочитанным; PDF skill применён, render невозможен без bytes. Нельзя по этому запуску подтвердить графику схемы p4 или точное расположение команд.
4. TinyFish fetch (html и markdown, ttl=0) вернул полный text и границы абзацев/страниц, но не PDF bytes/ETag/Last-Modified. Это допустимая дополнительная текстовая сверка и источник исправления version glue; не два независимых документа.
5. Targeted searches: exact `walkers-node`/`0.1.310`, ivacv.tech + license, IVA CV + GitHub/license/TPU/ONNX, site:ivacv.ru LinQ H1, LinQ модели, интервью/Рутуб. Публичный matching source/config/model license/runtime manifest не установлен. Нерелевантные generic walkers/TPU и сторонние пресс-перепечатки не включены как подтверждение.

## Разрешение оставшихся unknown и эксперименты

Самый короткий вопрос постановщику/интегратору после выдачи среды: «Есть ли доступная нашей команде согласованная PPE-сборка IVA CV для выданного LinQ; дайте SKU+driver/runtime manifest, image digest, config+model inventory, event API schema и права на запуск/изменение/сдачу». Это информационный запрос для root/user, мы его не отправляли.

Если такая сборка выдана: (1) проверить device selection/loading per NN и установить fallback policy; (2) одиночный file→event smoke test с известным положительным и отрицательным clip; (3) сверить event payload, кадр/координаты/время и видимость в UI; (4) добавить второй поток и обрыв камеры/повторное соединение, измерить age/fairness; (5) проверить recovery event job на незавершённой записи в отдельной разрешённой тестовой среде. Простой remove-device negative test не доказывает coverage всех NN; нужны backend logs/per-node inventory и содержательная проверка результатов. Ни один эксперимент здесь не выполнен.

Если готовой PPE-сборки нет, переносить только интерфейсное разделение `camera/file ingest → NN adapter → rule/event layer → storage/API/UI` и реализовывать наш adapter в разрешённой среде. Не пытаться заменить supplied LinQ inference API на IVA Edge-api: это разные контракты. До подтверждения полного кейса не утверждать допустимость host tracking/NMS или обязательный список классов.

## Компактный root handoff

- Исправить `image0.1.310`: вероятная PDF page-number glue; page-separated text даёт **0.1.3**. Visual/registry confirmation не достигнуты. Другие теги также склеены с page numbers.
- `/dev/tpu0` пример прямо назван LinQ, но современный SKU/H1M, PPE build и NN coverage не установлены. Это частичное опровержение «generic unnamed TPU», без доказательства полной совместимости.
- Новое прикладное знание: отдельные event-processing/recovery jobs и realtime muxer monitor; `500 ms`/`10 s` в примерах относятся к серверной обработке очереди, не к TPU inference или end-to-end SLA.
- Recipe переносим только при поставке images+digest, configs/models, DB seed, scripts, runtime и прав. Commercial license cost явно указан; public redistributable image/model license не найден, запрет исполнения не установлен.
- Видео не просмотрено, таймкодов нет. Старый guide1.8 с «СИЗ» касается COVID-масок, не доказательства текущих промышленных моделей.

