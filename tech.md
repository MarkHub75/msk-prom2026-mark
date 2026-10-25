# tech.md: Argus (msk-prom2026-mark, пакет safewatch)

## 0. Версия

**Версия: v10** (2026-10-25)

Changelog:
- v10 (UPGRADE v3, этап 1, 25.10): фронт Егора из PR #36 становится основным; Docker хранит SQLite в отдельном именованном томе, монтирует пользовательский конфиг read-only и не переопределяет URL LinQ. Проверка реального пакета, production-медиа/WS и пользовательского пути обязательна; результат и внешние ограничения — `docs/handoff/upgrade-v3-stage-1.md`. Этапы 2 (дедупликация, аудит, сценарии) и 3 (калькулятор v2) ещё не реализованы, API остаётся 1.1.0.
- v1: первая версия. Заморожены: разделы 5 и 6 (схема БД, типы, фасад, CLI, REST, WebSocket, конфиг, трассировка) и контракт фронтенда `contract/openapi.json` версии 1.0.0.
- v2 (ревью R5): 44 строки `GAP` S0–S5 перенесены в 6.8 и строки трассировки 6.7; 8.1: `model_missing` только по `not readable`; 8.2: жёлтая скорость при `≥` порога; 7: `registry.resolve(ref, models=None)`, `HudCanvas({ops, size})`; решения R5: `PUT` сектора, `PATCH` камеры, doctor без ключей, импорты `api.py`, устойчивость цикла задач и сессии Jupyter, диагностика очереди TPU.
- v3 (ревью R10): 37 строк `GAP` S6–S10 перенесены в 6.9, 3 строки трассировки 6.7; решения R10: `AnalysisConfig.extra_artifact_ids` (пересчёт с моделями `pipeline.extra` без изменения схемы), параметры правил из `CameraRule.effective` снимка, длина `X-Actor` проверяется только в `services`, ссылка на настройку камеры из списка, autouse-защита `data/app` в `tests/conftest.py`.
- v4 (ревью R15): 25 строк `GAP` S11–S15 перенесены в 6.10, 5 строк трассировки 6.7 (`observability.Luma`, `media.LUMA_WIDTH`, `store.publish_latencies`, `services.DELIVERED`, `delivery.target`); решения R15: `LatencyStats` экрана IT по событиям эфира, подписи HUD на `pair:`/`zone:`/`fire`, проверка URL webhook при загрузке, `hub.Client` без `dropped`, тест маршрутов без заглушек, права ролей только у пишущих слайсов.
- v5 (владелец, второй прогон по `UPGRADE_v1.md`): продукт называется Argus, пакет и CLI остаются `safewatch`; контракт фронта 1.1.0 только добавляет (раздел 6.11: миграция `0002_v5.sql`, 24 типа, 10 маршрутов, ключи конфига, поля существующих типов); новые слайсы S16–S32 и ревью R20, R25, R30, R32 (раздел 16): демо-пакет с детекциями LinQ, клип события и H.264, автокалибровка в м/с, каска и респиратор, модели Матвея, Docker, телефон по зонам, проекция груза, звонок мастеру и оператор с телефона, калькулятор окупаемости, датасет ложных срабатываний, ручная идентификация, паспорт камеры, LinQ под медленную очередь, пробелы `docs/ML_INTEGRATION.md`, отчёт смены в PDF, все долги `## open`; учтён `docs/ML_INTEGRATION.md` (коммит `5d940ba2`, дополнен Матвеем в `f6b5358a`: COCO-80 у детектора, extra-классы, программы `mosprom_matvey_*`, новая `version` при любой смене модели, 19 пробелов, решение по каждому — 8.30); второй прогон — раздел 10.3; лимит живых прогонов — S17, S28, R32.
- v6 (ревью R20): 17 строк `GAP` S17–S20 перенесены в 6.12, 7 строк трассировки 6.7 (`services.Source`, `services._stage`, `services._web_copy`, `services._clip`, `running.AUTOCAL_SAMPLES`, `texts.AUTOCAL_ONE_ROW`, pad нечётного кадра); решения R20: ffmpeg демо-импорта до транзакции (`_stage`), H.264-копия видео до S18 при повторной загрузке, `pad` нечётного кадра в `media.transcode`, СИЗ: при `no_<сиз>` и `<сиз>` на одной голове побеждает больший `score`, текст `AUTOCAL_ONE_ROW`, фейк LinQ не открывает базу вне `uploads/`, `texts.PRODUCT_TITLE` удалён, заголовок страницы и шапки — Argus.
- v7 (ревью R25): 16 строк `GAP` S22–S25 перенесены в 6.13, 16 строк трассировки 6.7 (`texts.HUD_LOAD_PROJECTION`, `delivery.phone_mask`, `store.delivery_enqueue`, `delivery_dequeue`, `services._delivery`, `texts.CALL_DELIVERED_STUB`, `services.CALC_EXAMPLE`, `CALC_DIVISORS`, `texts.CALC_OVERRIDDEN`, `store.linq_metrics`, `broadcast_event_counts`, `dataset.item_path`, `dataset.MANIFEST`, `store.dataset_pending`, `api.ZIP_FILE`, `api.PDF_FILE`); решения R25: тело webhook с текстом по уровню строки очереди, телефон: danger и vehicle_path побеждают `walkway`/`rest`, `async def dataset_export` (zip в `to_thread`), `application/zip` и `application/pdf` в `contract/openapi.json` (искомая строка маршрута без закрывающей скобки), необязательный `.env` в compose (Compose 2.24+), «живая камера» калькулятора — камера с событиями.
- v8 (ревью R30): 28 строк `GAP` S26–S30 перенесены в 6.14, 20 строк трассировки 6.7 (`texts.IDENTITY_TOO_LONG`, `identity_comment`, `services._stats_period`, `passport.ZONE_REQUIRED`, `texts.PASSPORT_SUITABLE`, `linq.job_timeout_s`, `rate_eta`, `services._live`, `texts.JOB_WAIT_TPU`, `rules.ANY_VEHICLE`, `store._JOBS` с метриками extra, откат extra в `eval_run`, `services.video_upload_check`, `api._UploadGuard`, `cli._server_running`, `texts.EVAL_SERVER_RUNNING`, `services.shift_report_name`, `texts.WHY_FENCE`, `Tracker._reattach`, `async def shift_report_pdf`); решения R30: PDF смены строится в `asyncio.to_thread` (300 событий — 0,9 с в потоке event loop), метрики extra-моделей задачи — в одном запросе `store._JOBS` (без чтений на задачу), `eval_run` идёт без упавшей extra-модели, `demo_build` падает целиком (8.19 п. 4), приняты риски `# sw:start` по pid, ETA в начале прогона, `UPLOAD_PATH`, этап 3 трекера, чтение HUD паспорта в потоке event loop; разобрана сцена ur-fall-03 (код верен); раздел 16: S31 и S32 сняты владельцем (25.10), после R30 идёт только R32 — финальная проверка (короткий живой прогон, готовность к демо).
- v9 (ревью R32): строк `GAP` нет; решения R32 в 6.15: `backend_close` в CLI `demo build` и `eval` (idle kernel LinQ), раскладка демо-пакета с одинаковыми именами видео → `ValidationFailed`; оставлено: зоны пакета не пишутся на камеру сида с зонами.

Правило версий: любое изменение контракта (разделы 5–6), состава слайсов (16) или правил (10–18) поднимает версию и добавляет строку в changelog. Правку коммитит в `main` владелец или ревью, которое переносит строки `GAP` (раздел 14), коммитом `docs(tech): vN <что>`. Сессия сверяет версию в шапке `progress.md` с этой; расхождение: прочитай changelog от своей версии и обнови шапку.

---

## 1. Как читать этот файл

**Актуальный процесс UPGRADE v3 (решение владельца, 25.10).** Работа ведётся по трём самостоятельным этапам, сейчас только этап 1. Историческая очередь S/R, Night Shift, запрет агенту править спецификацию, ритуал GAP, запрет браузера, «CI не ждать» и закрытие невыполненного критерия долгом не применяются. Предметные контракты, тестовая изоляция и машинно читаемые якоря ниже сохраняются. Исправления идут через рабочую ветку и PR, актуальный CI проверяется, развёртывание принимается фактическим запуском и браузером. Общий ориентир владельца — 25.10 08:30 МСК; прежние 10:00 ниже — история.

- Это источник истины проекта. Читай его перед каждой задачей и подчиняйся дословно.
- `docs/brief.md` объясняет, зачем строится проект. При расхождении прав этот файл. Факты о LinQ берутся из `docs/linq/LINQ_CONTRACT.md`: он главнее и брифа, и этого файла; расхождение с ним оформляй строкой `GAP`.
- Имена таблиц, полей, типов, функций, маршрутов и ключей конфига берутся отсюда и из строк `GAP` в `## open` файла `progress.md`. Свои варианты молча не придумывай.
- Нужного контракта нет: `CONTRACT GAP` (раздел 14), работа не останавливается.
- Файл меняет владелец или ревью, переносящее строки `GAP`. Сессия слайса его не редактирует.
- Один слайс за заход. Очередь в разделе 16, иди сверху вниз.
- Пометка **[проверить]**: перед кодом сверься с актуальной документацией сервиса или библиотеки и запиши итог одной строкой в запись слайса в `progress.md`.
- v5: контракт второго прогона — раздел 6.11, поведение — 8.19–8.33, правила прогона — 10.3. Они наравне с 5–6 и 8; `было → стало` в 6.11 заменяет сказанное выше. Контракт ML ↔ приложение для ML-части — `docs/ML_INTEGRATION.md`: он описывает текущий код, а не задаёт контракт; при расхождении прав этот файл, расхождение — строка `GAP`.

---

## 2. Проект

Argus (до v5 — SafeWatch; пакет, CLI и префикс переменных остаются `safewatch` / `SAFEWATCH_`): веб-сервис видеоконтроля промышленной безопасности для кейса «Открой#Моспром 2026» (ООО «ХайТэк», ускорители LinQ). Сервис принимает видео камер, один раз прогоняет нейросети на LinQ TPU, превращает детекции в эпизоды нарушений, оповещает оператора и мастера без дублей, ведёт неизменяемый журнал с доказательными кадрами и считает статистику.

Пользователи: оператор/диспетчер (главный герой, лента событий), мастер смены (телефон), специалист по охране труда (журнал, правила, статистика), менеджмент (тренды), IT/администратор (камеры, калибровка, зоны, замеры LinQ). Работник у станка интерфейсом не пользуется.

Режим работы: «анализ видеоархива / эмуляция потока». Видео загружается в сервис, обрабатывается внутри LinQ Jupyter (стримить кадры на LinQ запрещено), результат детекций кэшируется. «Эфир» камеры воспроизводит запись по серверным часам; событие публикуется, когда воспроизведение доходит до момента его подтверждения. Так красный захват экрана, автоэскалация и уведомление мастера работают в реальном времени на честно обработанной записи.

Это baseline: полный каркас продукта со всеми функциями брифа. День после ночи уходит на точность моделей, полировку UI, презентацию. Чем baseline не является:
- не live RTSP: архитектура это допускает (те же стадии инкрементально), но не делаем;
- не обучает модели: дообученные веса подключаются записью в `config/models.yaml`;
- нет логина и паролей: роль выбирается переключателем в шапке, сервер доверяет заголовку `X-Role`;
- нет реальной телефонии, Telegram, SMS, громкоговорителя, ламп и сирен: звонок мастеру — канал доставки с заглушкой-провайдером (v5, S23), лампы и сирены — точка расширения webhook (S15);
- нет автоматического распознавания людей и справочника работников: ФИО, должность и бригаду у события по желанию проставляет человек (v5, S26), статистика по людям — только по заполненным;
- не нативное мобильное приложение: мастер и оператор работают в адаптивном вебе;
- нет VLM «второго мнения», тепловой карты риска, экрана «Качество системы», размытия лиц, раскладки на несколько мониторов, «режима защиты» одной кнопкой (отвергнуто в `UPGRADE_v1.md`, раздел 6);
- не заявляет «первые на LinQ», снижение травматизма и цифры-иллюстрации кейса как факты; заглушки подписаны, цифры калькулятора — подписанные допущения.

Второй прогон (v5, раздел 16, S16–S32). Мотивы, на которые опираются решения, не описанные здесь: жюри видит почти продовое решение — открыл, и завод уже «живёт» (демо-пакет с реальными видео и детекциями LinQ); демо-путь «событие → оператор → мастер → журнал», контракт фронта и фронт Егора не ломаются; порядок слайсов по ценности, чтобы обрыв прогона оставил главное; заглушки подписаны, цифры настоящие; точность важнее скорости, но красное не приходит через минуту; внедрение на существующих камерах, железо — опциональный уровень. Ответственность: модели, датасеты, пороги и компиляция под LinQ — Матвей (стык — `docs/ML_INTEGRATION.md`, сценарий читает детекции по имени класса); приложение — этот прогон; фронтенд Argus и презентация — Егор по `contract/openapi.json`. Плохое освещение и ночь лечит модель, а не бэкенд: бэкенд честно пишет «Слишком темно».

Обязательные требования кейса (слайд 13) и где они закрыты:

| Требование | Слайс | Как |
| --- | --- | --- |
| Приём видео | 2 | загрузка файла камеры, очередь обработки |
| Распознавание нейросетями | 2, 4, 5, 10 | YOLOv8n и YOLOv8n-pose на LinQ, правила-плагины |
| Оперативное уведомление с кадром, камерой, временем, типом | 6, 7, 8 | WebSocket, лента, захват экрана, мастер |
| Одно нарушение — одно оповещение | 5, 6 | менеджер эпизодов, идемпотентная публикация |
| Журнал с фильтрами по типу, камере, зоне, времени и кадрами | 12 | `/ohs/journal`, CSV |
| Инференс на LinQ с замерами скорости | 2, 3 | адаптер `linq`, экран IT; вживую 24.10 14:52: детектор ~12,4 кадра/с, pose ~12,7 кадра/с, RTT TPU p50/p90 ~290/~380 мс на 400 кадрах |
| Предзагруженный «живой» завод (v5) | 17 | демо-пакет: реальные видео и детекции, посчитанные на LinQ |
| Разработка и внедрение (v5) | 21, 24 | Docker одной командой, калькулятор окупаемости и масштабирования |

### Допущения

- Режим ночи (поправка владельца 24.10, около 04:00): весь план выполняется примерно за 6 часов, к 10:00 МСК. Поэтому тесты облегчены (раздел 10.1), ручных проверок в браузере нет, ревью идёт раз в 5 слайсов, CI проверяется только на ревью, фронт простой: днём его заменит фронт Егора по тому же контракту.
- Файлы скилла: бриф просит `spec.md` и `PROGRESS.md`, пайплайн пишет `tech.md` и `progress.md`; везде, где бриф говорит `PROGRESS.md`, имеется в виду `progress.md` (нет в брифе).
- Имя продукта и пакета: `SafeWatch` / `safewatch`, префикс переменных `SAFEWATCH_` (нет в брифе).
- Python 3.12 вместо 3.11 из брифа: шаблон слайса 0 проверен на 3.12; код, который исполняется в LinQ Jupyter (Python 3.11), остаётся в `tools/linq/` и пакет `safewatch` туда не попадает.
- SQLite через `sqlite3` и SQL-миграции вместо SQLAlchemy + Alembic: шаблон проверен, весь SQL в одном `store.py`, переход на Postgres меняет `db.py` и `store.py`.
- Трекер свой, в духе ByteTrack (два порога, IoU, TTL в секундах): `supervision` и `ultralytics` тянут `opencv-python` и torch, а TTL по времени источника рекомендует ресёрч.
- Pose и детектор — две программы TPU и два прохода `video_worker.py` по видео; кадры совмещаются по `frame_idx`.
- Удалённая папка baseline в Jupyter — `~/work/baseline/`, файлы с префиксом `baseline_`, как требуют правила параллельной работы с Матвеем; smoke test пользовался `~/work/mosprom_work/`.
- Наборы изображений (слайд 13 разрешает «потоки или наборы изображений») не принимаем: достаточно видеофайлов (нет в брифе).
- Время в базе — UTC ISO 8601 с миллисекундами; статистика и смены считаются в `Europe/Moscow` (нет в брифе).
- Смены: дневная 08:00–20:00, ночная 20:00–08:00 (нет в брифе).
- Пороги правил (раздел 6.6) — стартовые значения без обоснованного источника: ресёрч чисел не дал, их подбирает ML-часть днём инструментом оценки (S14).
- Текст уведомления: `<уровень> · <сектор> · <причина>`; сектор берётся до первого « · » в названии сектора (нет в брифе).
- Повтор эфира по кругу (`loop`) создаёт новые события на каждом цикле: это новый «показ» записи (нет в брифе).
- «Пересчитать события» переводит нетронутые людьми события этого видео в статус `superseded` и перезапускает эфир камеры (нет в брифе в такой форме).
- Лимит живых прогонов: в брифе нет, взят из правил параллельной работы: одна задача baseline на TPU одновременно, один прогон LinQ на шаг.
- Мок-режим фронта: Prism по `contract/openapi.json` + скрипт фейковых WS-событий (нет конкретики в брифе).
- CSV-экспорт: разделитель `;`, UTF-8 с BOM, чтобы русский Excel открыл файл без настройки (нет в брифе).
- Звук браузера (сирена, сигнал) генерируется WebAudio без файлов; до первого клика браузер звук не пустит, UI показывает кнопку «Включить звук» (нет в брифе).
- Каталог данных приложения — `data/app/`, чтобы не смешивать с `data/videos/` и `data/coco128/` (нет в брифе).

Допущения v5 (второй прогон, `UPGRADE_v1.md`; владелец принял):
- Имя продукта Argus меняет только `product_name` и тексты; пакет `safewatch`, CLI, переменные `SAFEWATCH_*`, пути и имена контракта не переименовываются: переименование сломало бы контракт фронта и сверку 6.7.
- Номера слайсов продолжаются с S16: сверка контракта читает закрытые слайсы по заголовкам `### S<N>` в `## log`, повтор номеров смешал бы старые и новые элементы.
- Ревью — раз в 5 слайсов, как в первом прогоне (R20, R25, R30), последнее — R32 после двух слайсов «если останется время».
- Новые типы и маршруты v5 записаны в 6.11, а не в 5.2 и 6.4: тесты `test_types_export_contract_names` и `test_every_contract_route_is_declared` разбирают эти разделы, и `main` покраснел бы до кода. S16 расширяет оба теста на 6.11.
- Схема меняется только добавлением: новая миграция `0002_v5.sql`, таблицы 5.1 не пересоздаются (CHECK существующих колонок не трогаются).
- Демо-пакет живёт в `data/demo/<name>/` вне git (видео и детекции весят мегабайты); на другую машину его копирует владелец (раздел 8.32). В git — только `data/demo/README.md` и `config/demo.example.yaml`.
- Камеры демо-пакета привязываются к секторам и камерам сида по названию; нет такой — создаются. События эфира демо-пакета — настоящие (`is_demo = 0`): детекции посчитаны на LinQ. Синтетическая история сида для статистики остаётся.
- Клип события — окно `[start − clips.pre_s, confirm + clips.post_s]` исходного видео (не больше `clips.max_s`): «5 с после» отсчитываются от подтверждения, чтобы клип показывал момент, когда сработало правило. Файлов клипов нет: плеер играет `#t=<от>,<до>`.
- Перекодирование — ffmpeg из пакета `imageio-ffmpeg` (без установки ffmpeg в систему), только если кодек не из `media.BROWSER_CODECS`; инференс и ключ кэша идут по исходному файлу.
- Автокалибровка — линейная модель «рост в пикселях = a + b · низ рамки по вертикали» по стоящим людям; масштаб «метры на пиксель» = 1,7 м / рост в этой строке кадра. Точность около ±20 %, для порога бега (2,5 м/с при шаге ~1,4 м/с) достаточно.
- Модели респиратора нет ни у кого: плагин `no_respirator` честно в статусе `model_missing` до модели с классом `no_respirator`. Каска — по модели Матвея `matvey-helmet-yolov8n` (классы `helmet`, `no_helmet`).
- Телефон в зоне `danger` и `vehicle_path` остаётся красным (как в v4); в разрешённых зонах (`walkway`, `rest`) событий нет; везде остальное — жёлтое после `hold_s`.
- Проекция груза — упрощённая: столбец кадра под рамкой груза до низа кадра. Это ровно та область, по которой правило `suspended_load` даёт красное (8.3), поэтому HUD объясняет событие честно.
- Цены калькулятора (ускоритель, сервер, лампы, громкоговорители, камеры) и доля снижения инцидентов — подписанные допущения команды с источником «уточнить у поставщика» или «гипотеза, проверяется пилотом»; пропускная способность ускорителя — наш замер 24.10 или медиана замеров приложения.
- Датасет ложных срабатываний складывается файлами в `data_dir/datasets/false_alarms/`, формат строк детекций — тот же `FrameDetections`, что у артефактов (`docs/ML_INTEGRATION.md` раздел 4).
- Идентификацию нарушителя ставят роли `ohs` и `management` («охрана труда или аналитик»).
- Шрифт PDF с кириллицей — `DejaVuSans.ttf` (свободная лицензия), лежит в пакете: в образе python:3.12-slim системных шрифтов с кириллицей нет.
- Файлы моделей Матвея (`models/matvey/...`) в git не идут; без них записи реестра есть, но `doctor` честно показывает «нет файла». Ветку `matvey_cv` только читают (`git show origin/matvey_cv:<путь>`).
- v10: основной `frontend/` — фронт Егора (PR #36, squash `e80a550436ad0452f2c2ca829dcc6e6a253ab639`). Функциональные исправления разрешены без смены дизайна; API 1.1.0 сохранён. Исторические описания минимального фронта ниже не требуют возвращать его структуру.

## 3. Стек

| Слой | Выбор |
| --- | --- |
| Язык и сборка | Python 3.12, uv, poethepoet; пакет `safewatch` в `src/`, консольная команда `safewatch` |
| Веб | FastAPI, uvicorn (без `[standard]`) + `websockets`, `python-multipart` **[проверить]** версии и поддержку Range в `FileResponse` |
| Данные | `sqlite3` из stdlib, WAL, SQL-миграции по `PRAGMA user_version` |
| Модели и конфиг | pydantic v2, pydantic-settings, PyYAML |
| CV | numpy, scipy (`linear_sum_assignment`), opencv-python-headless (декод, кадры, JPEG, гомография), onnxruntime (бэкенд `local`) |
| LinQ | `tools/linq/jupyter_remote.py` (импорт по пути) и его зависимости: requests, websocket-client, python-dotenv; `tools/linq/remote/video_worker.py`, `linq_tpu.py`, `yolo_io.py` загружаются в Jupyter |
| Прочее | httpx (webhook), psutil (pid и время старта процесса), tzdata (часовой пояс на Windows) |
| Тесты и проверки | pytest, pytest-asyncio, pytest-timeout, hypothesis, respx, ruff, mypy `--strict`, types-pyyaml, types-requests, types-psutil |
| Фронтенд | Node 24, React 18, Vite, TypeScript strict, react-router-dom 6, openapi-typescript + openapi-fetch, recharts; vitest + @testing-library/react + jsdom; eslint с typescript-eslint; мок: @stoplight/prism-cli, ws, concurrently **[проверить]** актуальные версии, фиксирует `package-lock.json` |
| Реалтайм | WebSocket `/ws` |
| Контейнер | Dockerfile (сборка фронта на node, рантайм python:3.12-slim) и docker-compose.yml (S15, запуск одной командой — S21) |
| v5 | `imageio-ffmpeg` (бинарник ffmpeg для перекодирования в H.264, S18) **[проверить]** версию и наличие колёс для Windows и manylinux; `fpdf2` (PDF сводки смены, S30) **[проверить]** версию и `add_font` для TTF; шрифт `DejaVuSans.ttf` в `src/safewatch/assets/fonts/` **[проверить]** лицензию |

Без: ORM и Alembic; Celery, Redis и отдельного процесса воркера (одна фоновая asyncio-задача в процессе сервера); ultralytics, torch и supervision в рантайме; стейт-менеджера и react-query на фронте (свой хук `useApi`); CSS-фреймворка (CSS-переменные темы); авторизации; системного ffmpeg (v5: ffmpeg только из `imageio-ffmpeg` и только для H.264-копии, S18); matplotlib и reportlab (PDF — `fpdf2`); VLM и облачных моделей.

### 3.1 LinQ: правила работы

- Факты, форматы, тензоры, ловушки: `docs/linq/LINQ_CONTRACT.md`. Код smoke test: `tools/linq/`.
- Доступ только через SSH-туннель к ноутбуку Матвея: `tools\linq\tunnel\Connect-LinQ.cmd`, Jupyter `http://127.0.0.1:8888/`. Туннель упал: перезапусти `Connect-LinQ.cmd`; две попытки не помогли — работай на `SAFEWATCH_FAKE=1`, в `## open` строка `долг: <шаг>, проверка на LinQ, туннель недоступен`, позже попробуй снова. На ноутбуке Матвея ничего не меняй.
- Аккаунт Jupyter один на команду, Матвей работает в нём параллельно (папка `matvey/`). Наше — только `~/work/baseline/`, видео и выходы с префиксом `baseline_`.
- Программы `mosprom_*_cut_ap9999_b1_o1_h1m.tpu` в `/auto/cache/hackathon70007/` общие: использовать, не перезаписывать, свои с такими именами не загружать. Чужие программы (`helmet-v1.tpu`, `pose-split-v1.tpu`), очереди, папки и ноутбуки не читать и не трогать.
- Брокер RabbitMQ общий для 37 команд (`guest/guest`). Бэкенд baseline к нему не подключается: запросы к TPU шлёт только `video_worker.py` внутри Jupyter.
- Квота CPU контейнера 1,5 общая с Матвеем: воркер ограничивает потоки (`OMP_NUM_THREADS=1`, OpenCV и onnxruntime по 1 потоку — уже в `video_worker.py`), `--inflight 4`, одна задача baseline на TPU одновременно.
- Перекомпиляция программ TPU и обучение на ноутбуке капитана запрещены: мало памяти, программы уже на LinQ.
- Секреты только в `.env` (`LINQ_*`): не печатать, не логировать, не коммитить, не писать в `tech.md`, `progress.md`, тексты ошибок.
- v5, второй прогон: приоритет на LinQ у Матвея (он учит и проверяет модели). Прогон делает на LinQ только короткие живые проверки и сборку демо-пакета, по одной задаче (лимит в `CLAUDE.md`). Очередь бывает медленной: RTT TPU p50 до ~10,6 с на запрос (площадка общая на ~37 команд); таймауты и повторы считаются от этого (8.29).
- Программы Матвея называются `mosprom_matvey_*` (загрузчик `tools/linq/upload_program.py` сам добавляет `mosprom_`): прогон их не загружает, не перезаписывает и не удаляет, только ссылается на них в `config/models.yaml`.
- Ветка Матвея `matvey_cv`: только чтение файлов `git show origin/matvey_cv:<путь>` (например `ml/models.matvey.yaml`, `ml/pipeline.matvey.yaml`, `docs/ML_HANDOFF_MATVEY.md`); checkout, merge, cherry-pick и push в неё запрещены.
- Ноутбук Матвея — VPN-шлюз: с него только туннель.

### 3.2 Платформа: Windows 11, Git Bash, PowerShell 5.1

Репозиторий и файлы
- Репозиторий существует и содержит 2339 файлов исследований с CRLF. Слайс 0 не включает `* text=auto eol=lf` на весь репозиторий (это пометит их изменёнными), а кладёт в `.gitattributes` правила `text=auto eol=lf` для путей приложения (раздел 4). Гейт падает, если `git ls-files --eol` по этим путям показывает `i/crlf` (`scripts/eol_check.py`).
- Код проекта пишет текст в UTF-8 и LF: `write_text(..., encoding="utf-8", newline="\n")`.
- `pyproject.toml`: `[tool.ruff] extend-exclude = ["*.md"]`; цели гейта перечисляют пути явно (`ruff format src tests scripts`), а не `.`.
- `.gitignore` включает `.env`, `config/user.yaml`, `data/app/`, `.venv-linq/`, `frontend/node_modules/`, `frontend/dist/`, кеши тестов (`.hypothesis/`).

Вывод и кодировки
- Точка входа CLI первой строкой переключает stdout и stderr на UTF-8 (`reconfigure(encoding="utf-8")`). Тест пишет в поток с cp1252.
- Служебный Python агенты запускают с `-X utf8` (при `-I` переменная `PYTHONIOENCODING` не действует).

Время и конкурентность
- Интервалы, дедлайны, лимитеры: `time.perf_counter`, не `time.monotonic` (на Windows шаг 15,6 мс). Стеночное время продукта: только `clock.now()` (тесты подменяют его).
- Тест времени работает на `fake_clock` (10.1); тест с реальным временем фиксирует гарантированное событие, допуск не меньше 16 мс.
- Дочерние задачи с побочными эффектами только в `asyncio.TaskGroup`. `gather` только с `return_exceptions=True`.
- sqlite: пишет один поток — поток event loop сервера. Все обработчики `api.py` объявлены `async def`; блокирующая работа (инференс, OpenCV, анализ) уходит в `asyncio.to_thread`, получает данные аргументами и в базу не пишет. Тесты пишут данные только через `services` и `store`.
- sqlite: `connect` регистрирует SQL-функцию `casefold` (поиск по кириллице без учёта регистра). LIKE экранирует `_` и `%`.

Процессы
- Сервер на ProactorEventLoop без `reload`; тест запуска `safewatch serve` подпроцессом в слайсе 0.
- Ядро не запускает дочерних процессов. Удалённый воркер LinQ живёт в Jupyter и останавливается командой `kill` по своему pid-файлу.
- v5, было → стало: единственный дочерний процесс ядра — ffmpeg перекодирования (S18): `subprocess.run([...], timeout=transcode.timeout_s, check=False)` без shell, в `asyncio.to_thread`, вывод в `DEVNULL`; таймаут убивает процесс (`subprocess.run` сам вызывает `kill`), внуков у ffmpeg нет. Тест: таймаут не оставляет процесса и не роняет загрузку.
- `safewatch serve` пишет `data/app/server.pid` с pid и временем старта процесса; `safewatch stop` сверяет оба (`psutil`) и чужой процесс не трогает.
- Пока работает сервер, CLI проекта вызывается как `.venv/Scripts/safewatch.exe` или `uv run --no-sync safewatch`. `uv sync` только при остановленном сервере.

CI
- `gate.yml`: триггеры `pull_request` и `push` в `main`, матрица `windows-latest` + `ubuntu-latest`, `timeout-minutes: 20` у job.
- Actions закреплены точным тегом (пример: `astral-sh/setup-uv@v10.3.0`), тег проверен через `gh api`.
- Проверка CI шага: `gh pr checks <N>`. Красный CI после мёрджа запускает ремонт до следующего шага.

## 4. Структура папок

Репозиторий `D:\msk-prom2026-mark` (`github.com/MarkHub75/msk-prom2026-mark`) уже существует. Ниже только то, что добавляет приложение; существующее перечислено в конце.

```
.github/workflows/gate.yml
.gitattributes .gitignore .env.example        # существуют: слайс 0 дополняет, не заменяет
.python-version pyproject.toml uv.lock
README.md                                      # существует: слайс 0 добавляет раздел «Приложение SafeWatch»
tech.md CLAUDE.md progress.md docs/brief.md
Dockerfile docker-compose.yml .dockerignore    # слайс 15
config/
  default.yaml                                 # раздел 6.6, целиком
  user.example.yaml
  models.yaml                                  # реестр моделей, раздел 6.6
  eval.example.yaml                            # слайс 14
contract/
  openapi.json                                 # генерирует `safewatch contract`
  ws.schema.json                               # генерирует `safewatch contract`
  ws-examples.json                             # пример каждого WsType, пишется руками
scripts/
  contract_check.py                            # из шаблона
  eol_check.py
src/safewatch/
  __init__.py __main__.py
  cli.py            # serve, stop, seed, doctor, contract, import, eval
  config.py         # Settings: .env + yaml
  types.py          # контракт 5.2 и протоколы 6.1
  errors.py         # AppError и наследники, InferenceError
  texts.py          # все русские тексты продукта
  clock.py          # now(), iso(), parse()
  db.py             # connect, migrate
  migrations/0001_init.sql
  store.py          # весь SQL
  services.py       # фасад
  api.py            # FastAPI: маршруты, WebSocket, статика фронта
  hub.py            # раздача WS-сообщений по ролям
  worker.py         # фоновые циклы: задачи, тик эфира, тик эскалации
  registry.py       # загрузка config/models.yaml, активные модели
  media.py          # probe_video, read_frame, encode_jpeg, sample_luma
  seed.py           # демо-данные
  doctor.py
  evaluate.py       # слайс 14
  delivery.py       # слайс 15
  inference/
    __init__.py     # make_backend(settings)
    artifacts.py    # cache_key, чтение и проверка JSONL
    linq.py         # JupyterShell, LinqBackend
    local.py        # LocalBackend
  analysis/
    __init__.py
    pipeline.py     # analyze(): детекции → треки → признаки → наблюдения → эпизоды
    tracking.py
    geometry.py
    features.py
    episodes.py
    observability.py
    hud.py
  rules/
    __init__.py     # PLUGINS, scenario_metas(), plugin(id)
    base.py         # общие помощники плагинов
    running.py proximity.py phone.py fall.py fence.py under.py
    fire.py harness.py suspended_load.py load_carrying.py
  fakes/
    __init__.py
    remote.py       # FakeRemoteShell
    scenes.py       # синтетические сцены → JSONL детекций
tests/
  conftest.py
  test_*.py         # имена из слайсов раздела 16
  live/test_linq_live.py
frontend/
  package.json package-lock.json tsconfig.json vite.config.ts eslint.config.js index.html .env.example .env.mock
  mock/ws-mock.mjs
  scripts/api-check.mjs
  src/
    main.tsx App.tsx nav.ts roles.ts theme.css
    api/schema.d.ts   # генерирует openapi-typescript
    api/client.ts api/ws.ts api/useApi.ts
    components/       # раздел 7
    screens/operator/ screens/events/ screens/master/ screens/ohs/ screens/management/ screens/admin/
    **/*.test.ts(x)
```

Добавляет v5 (раздел 6.11, слайсы S16–S32):

```
src/safewatch/
  migrations/0002_v5.sql      # S16, раздел 6.11.1
  demo.py                     # S17: чтение и запись демо-пакета (manifest.json, файлы)
  calculator.py               # S24: формулы калькулятора, чистые функции
  dataset.py                  # S25: файлы датасета ложных срабатываний (блокирующий ввод-вывод)
  report_pdf.py               # S30: PDF сводки смены
  assets/fonts/DejaVuSans.ttf # S30
  analysis/autocal.py         # S19: автокалибровка, чистые функции
  analysis/passport.py        # S27: паспорт пригодности камеры, чистые функции
  rules/ppe.py                # S20: HelmetPlugin, RespiratorPlugin
config/
  demo.example.yaml           # S17: раскладка демо-пакета по секторам и камерам
  user.matvey.example.yaml    # S20: включение моделей Матвея в config/user.yaml
data/demo/README.md           # S17: что лежит в data/demo/<name>/, как собрать и перенести
docs/DEPLOY.md                # S21: развёртывание на другой машине
frontend/src/components/ClipPlayer.tsx                 # S18
frontend/src/screens/operator/OperatorMobile.tsx       # S23
frontend/src/screens/operator/OperatorMobileEvent.tsx  # S23
tests/test_{demo_pack,clips,autocal,rule_ppe,docker_files,calculator,dataset,identity,passport,ml_gaps,shift_pdf,camera_shift}.py
```

`.gitignore` v5: `data/demo/*/` (кроме `data/demo/README.md`). `.gitattributes` v5: `*.ttf binary`, `*.zip binary`.

Правила размещения v5: `demo.py`, `dataset.py`, `report_pdf.py`, `media.transcode` — блокирующий ввод-вывод, вызываются из `services` через `asyncio.to_thread` (CLI — напрямую), в базу не пишут; `calculator.py`, `analysis/autocal.py`, `analysis/passport.py` — чистые функции без базы, сети и часов.

Существующее, не трогать: `Deep-Research/`, `secrets/`, `vendor/`, `models/`, `results/`, `data/coco128/`, `data/videos/` (кроме видео, которые кладёт капитан), `INDEX.md`, `SUMMARY.md`. `docs/linq/` и `docs/ENVIRONMENT.md` только дополнять. `tools/linq/` менять точечно и обратно совместимо (слайс 10 добавляет `--nc` в `video_worker.py`; слайс 0 правит путь `.venv` в README).

Правила размещения:
- `api.py`, `cli.py`, `worker.py` зовут только функции фасада `services.py` (раздел 6.2); `api.py` ещё держит WS-подключения через `hub`.
- `services.py`: права ролей, смысловая валидация, транзакции через `store`, публикация в `hub`. SQL живёт только в `store.py` и `db.py`; `seed.py` пишет через `store`.
- `analysis/`, `rules/`, `inference/artifacts.py`, `geometry.py`: чистая логика без базы, сети и часов; на вход данные, на выход данные.
- `inference/linq.py`, `inference/local.py`, `media.py`: блокирующий ввод-вывод, вызываются из `services` через `asyncio.to_thread`, в базу не пишут.
- `fakes/` используется только тестами и режимом `SAFEWATCH_FAKE=1`.
- Русские тексты продукта только в `texts.py`; фронт получает их через API.
- Фронтенд: сетевые вызовы только в `src/api/`; `screens/` собираются из `components/`; бизнес-правил на фронте нет: уровни, статусы, тексты, разрешённые действия, сценарии и типы зон приходят с бэкенда.
- `.gitattributes` с правилом `text=auto eol=lf` для: `/src/**`, `/tests/**`, `/scripts/**`, `/config/**`, `/contract/**`, `/frontend/**`, `/.github/**`, `/pyproject.toml`, `/uv.lock`, `/tech.md`, `/CLAUDE.md`, `/progress.md`, `/docs/brief.md`, `/Dockerfile`, `/docker-compose.yml`; `binary` для `*.png *.jpg *.ico *.pdf *.db *.mp4 *.onnx *.tpu`; существующие строки LFS сохраняются.

## 5. Контракт данных (заморожен)

### 5.1 Схема базы: `src/safewatch/migrations/0001_init.sql`

Время во всех колонках `*_at` — текст UTC ISO 8601 с миллисекундами и `Z` (`clock.iso()`). Булевы — `INTEGER` 0/1. Колонки без комментария пишет функция фасада, чьё имя совпадает с таблицей (раздел 6.2).

```sql
CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_demo INTEGER NOT NULL DEFAULT 0,          -- пишет: seed.seed_demo
    created_at TEXT NOT NULL
);

CREATE TABLE cameras (
    id INTEGER PRIMARY KEY,
    sector_id INTEGER NOT NULL REFERENCES sectors(id),
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    is_demo INTEGER NOT NULL DEFAULT 0,          -- пишет: seed.seed_demo
    created_at TEXT NOT NULL,
    deleted_at TEXT                              -- пишет: services.camera_delete; события ссылаются на удалённую камеру
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    filename TEXT NOT NULL,                      -- исходное имя файла
    sha256 TEXT NOT NULL,
    path TEXT NOT NULL,                          -- от data_dir: uploads/<sha256><ext>
    size_bytes INTEGER NOT NULL,
    width INTEGER NOT NULL,                      -- пишет: media.probe_video через services.video_upload
    height INTEGER NOT NULL,
    fps REAL NOT NULL,
    frame_count INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    codec TEXT NOT NULL,                         -- FourCC в нижнем регистре
    browser_playable INTEGER NOT NULL,           -- codec из media.BROWSER_CODECS
    status TEXT NOT NULL CHECK (status IN ('uploaded', 'processing', 'ready', 'failed')),
    active_analysis_id INTEGER REFERENCES analyses(id),  -- пишет: services.run_next_job, последняя версия анализа
    created_at TEXT NOT NULL,
    UNIQUE (camera_id, sha256)
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('process', 'recompute')),
    video_id INTEGER NOT NULL REFERENCES videos(id),
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),
    fake INTEGER NOT NULL,                       -- Settings.fake на момент постановки
    status TEXT NOT NULL CHECK (status IN ('queued', 'running', 'retry_wait', 'done', 'failed')),
    stage TEXT NOT NULL CHECK (stage IN ('queued', 'inference_detect', 'inference_pose', 'analysis', 'evidence', 'done')),
    progress REAL NOT NULL DEFAULT 0,            -- 0..1 по всем стадиям (раздел 8.1)
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at TEXT,                        -- пишет: services.run_next_job при retry_wait
    error_code TEXT,                             -- JobErrorCode
    error_text TEXT,                             -- до 500 символов, без секретов
    det_artifact_id INTEGER REFERENCES artifacts(id),   -- пишет: services.run_next_job
    pose_artifact_id INTEGER REFERENCES artifacts(id),  -- пишет: services.run_next_job; NULL, если pose выключен или упал
    analysis_id INTEGER REFERENCES analyses(id),        -- пишет: services.run_next_job (с слайса 4)
    analysis_ms INTEGER,                         -- пишет: services.run_next_job, время стадии анализа
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT
);

CREATE TABLE artifacts (
    id INTEGER PRIMARY KEY,
    cache_key TEXT NOT NULL UNIQUE,              -- inference.artifacts.cache_key(...)
    video_sha256 TEXT NOT NULL,
    model_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    task TEXT NOT NULL CHECK (task IN ('detect', 'pose')),
    input_size INTEGER NOT NULL,
    step INTEGER NOT NULL,
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),
    fake INTEGER NOT NULL,                       -- 1: детекции синтетические (FakeRemoteShell)
    path TEXT NOT NULL,                          -- artifacts/<cache_key>.jsonl
    frames INTEGER NOT NULL,
    metrics_json TEXT NOT NULL,                  -- InferenceMetrics без поля cached
    created_at TEXT NOT NULL
);

CREATE TABLE analyses (
    id INTEGER PRIMARY KEY,
    video_id INTEGER NOT NULL REFERENCES videos(id),
    version INTEGER NOT NULL,
    det_artifact_id INTEGER NOT NULL REFERENCES artifacts(id),
    pose_artifact_id INTEGER REFERENCES artifacts(id),
    config_json TEXT NOT NULL,                   -- AnalysisConfig: снимок калибровки, зон и правил на момент анализа
    hud_path TEXT NOT NULL,                      -- analyses/<video_id>-v<version>/hud.jsonl
    gaps_json TEXT NOT NULL,                     -- list[ObservabilityGap]
    duration_ms INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (video_id, version)
);

CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    analysis_id INTEGER NOT NULL REFERENCES analyses(id),
    scenario TEXT NOT NULL,
    subject TEXT NOT NULL,                       -- "track:12" | "pair:12-7" | "zone:12-3" | "fire"
    zone_id INTEGER REFERENCES zones(id),
    level_initial TEXT NOT NULL CHECK (level_initial IN ('yellow', 'red')),
    level_max TEXT NOT NULL CHECK (level_max IN ('yellow', 'red')),
    start_ms INTEGER NOT NULL,                   -- первое позитивное наблюдение
    confirm_ms INTEGER NOT NULL,                 -- подтверждение: момент публикации в эфире
    escalate_ms INTEGER,                         -- жёлтое → красное внутри эпизода
    end_ms INTEGER NOT NULL,
    end_reason TEXT NOT NULL CHECK (end_reason IN ('observed_exit', 'track_lost_timeout', 'video_end')),
    reason_code TEXT NOT NULL,
    reason_text TEXT NOT NULL,                   -- короткий нейтральный текст причины, texts.py
    method TEXT NOT NULL,                        -- "pose" | "bbox" | "calibrated" | "relative" | "zone" | "model"
    confidence REAL NOT NULL,
    metrics_json TEXT NOT NULL,                  -- dict[str, float]: пики признаков за эпизод
    uncertain_ms INTEGER NOT NULL DEFAULT 0      -- сумма интервалов U внутри эпизода
);

CREATE TABLE evidence (
    id INTEGER PRIMARY KEY,
    episode_id INTEGER NOT NULL REFERENCES episodes(id),
    kind TEXT NOT NULL CHECK (kind IN ('confirm', 'escalate')),
    frame_idx INTEGER NOT NULL,
    ts_ms INTEGER NOT NULL,
    path TEXT NOT NULL,                          -- evidence/<episode_id>-<kind>.jpg
    sha256 TEXT NOT NULL,                        -- sha256 JPEG-файла
    objects_json TEXT NOT NULL,                  -- list[HudObject] этого кадра
    UNIQUE (episode_id, kind)
);

CREATE TABLE broadcasts (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    video_id INTEGER NOT NULL REFERENCES videos(id),
    analysis_id INTEGER NOT NULL REFERENCES analyses(id),
    started_at TEXT NOT NULL,                    -- стеночное время позиции 0 цикла 0
    loop INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('playing', 'stopped', 'ended')),
    cycle INTEGER NOT NULL DEFAULT 0,            -- пишет: services.broadcast_tick
    position_ms INTEGER NOT NULL DEFAULT 0,      -- пишет: services.broadcast_tick, последняя обработанная позиция
    stopped_at TEXT                              -- пишет: services.broadcast_stop, broadcast_start, video_recompute, camera_delete
);
CREATE UNIQUE INDEX broadcasts_one_playing ON broadcasts (camera_id) WHERE status = 'playing';

CREATE TABLE zones (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    kind TEXT NOT NULL,                          -- id из zone_kinds в config/default.yaml
    name TEXT NOT NULL,
    points_json TEXT NOT NULL,                   -- [[x, y]] нормированные 0..1; polygon 3..32 точек, line ровно 2
    created_at TEXT NOT NULL,
    deleted_at TEXT                              -- пишет: services.zone_delete
);

CREATE TABLE calibrations (
    camera_id INTEGER PRIMARY KEY REFERENCES cameras(id),
    image_points_json TEXT NOT NULL,             -- [[u, v]] нормированные 0..1, 4..8 точек
    world_points_json TEXT NOT NULL,             -- [[x, y]] метры на полу
    control_json TEXT NOT NULL,                  -- list[ControlPoint], 0..8
    homography_json TEXT NOT NULL,               -- 3×3: нормированное изображение → пол в метрах
    fit_rmse_m REAL NOT NULL,
    control_rmse_m REAL,                         -- NULL: контрольных точек нет
    updated_at TEXT NOT NULL
);

CREATE TABLE camera_rules (
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    scenario TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    params_json TEXT NOT NULL,                   -- переопределения параметров сценария, dict[str, float]
    updated_at TEXT NOT NULL,
    PRIMARY KEY (camera_id, scenario)
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    pub_key TEXT NOT NULL UNIQUE,                -- "b<broadcast>:c<cycle>:e<episode>" | "demo:<n>"
    episode_id INTEGER REFERENCES episodes(id),  -- NULL у демо-событий
    broadcast_id INTEGER REFERENCES broadcasts(id),  -- NULL у демо-событий
    cycle INTEGER NOT NULL DEFAULT 0,
    video_id INTEGER REFERENCES videos(id),
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    sector_id INTEGER NOT NULL REFERENCES sectors(id),  -- сектор камеры на момент публикации
    zone_id INTEGER REFERENCES zones(id),
    scenario TEXT NOT NULL,
    title TEXT NOT NULL,                         -- название сценария на момент публикации
    reason_text TEXT NOT NULL,
    level TEXT NOT NULL CHECK (level IN ('yellow', 'red')),
    status TEXT NOT NULL CHECK (status IN ('new', 'viewed', 'confirmed', 'false_alarm', 'sent_to_master',
                                            'master_accepted', 'resolved', 'auto_finished', 'superseded')),
    operator_verdict TEXT NOT NULL DEFAULT 'none' CHECK (operator_verdict IN ('none', 'confirmed', 'false_alarm')),
    escalated_by_timeout INTEGER NOT NULL DEFAULT 0,
    started_at TEXT NOT NULL,                    -- стеночное время начала эпизода
    published_at TEXT NOT NULL,
    red_at TEXT,                                 -- пишет: services.broadcast_tick (публикация красным или эскалация)
    ended_at TEXT,                               -- пишет: services.broadcast_tick (конец эпизода в эфире)
    video_start_ms INTEGER,
    video_end_ms INTEGER,
    is_demo INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX events_published ON events (published_at);
CREATE INDEX events_status ON events (status);
CREATE INDEX events_camera ON events (camera_id);

CREATE TABLE event_actions (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    at TEXT NOT NULL,
    actor_role TEXT NOT NULL CHECK (actor_role IN ('operator', 'master', 'ohs', 'management', 'admin', 'system')),
    actor_name TEXT NOT NULL,                    -- заголовок X-Actor или texts.DEMO_ACTOR[role]; "система"
    action TEXT NOT NULL,                        -- LogAction
    from_status TEXT,
    to_status TEXT,
    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX event_actions_event ON event_actions (event_id);
CREATE TRIGGER event_actions_no_update BEFORE UPDATE ON event_actions
BEGIN SELECT RAISE(ABORT, 'event_actions is append-only'); END;
CREATE TRIGGER event_actions_no_delete BEFORE DELETE ON event_actions
BEGIN SELECT RAISE(ABORT, 'event_actions is append-only'); END;

CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    channel TEXT NOT NULL,                       -- "webhook:<name>"
    kind TEXT NOT NULL CHECK (kind IN ('published', 'escalated', 'to_master')),
    status TEXT NOT NULL CHECK (status IN ('sent', 'failed')),
    http_status INTEGER,
    error TEXT NOT NULL DEFAULT '',
    at TEXT NOT NULL,
    UNIQUE (event_id, channel, kind)
);
```

`db.connect` ставит `PRAGMA foreign_keys = ON`, для файла `journal_mode = WAL`, `synchronous = FULL`, `busy_timeout = 1000` и регистрирует `casefold(text)`.

### 5.2 Типы: `src/safewatch/types.py`

Модели ответа API, модели входа API и внутренние типы конвейера. Протоколы внешних клиентов здесь же (6.1). Каждое поле обязательно, если не указано значение по умолчанию.

```python
"""Contract types (tech.md 5.2) and protocols (tech.md 6.1). Names here are frozen."""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel

Level = Literal["yellow", "red"]
Role = Literal["operator", "master", "ohs", "management", "admin"]
ActorRole = Literal["operator", "master", "ohs", "management", "admin", "system"]
EventStatus = Literal[
    "new", "viewed", "confirmed", "false_alarm", "sent_to_master",
    "master_accepted", "resolved", "auto_finished", "superseded",
]
Verdict = Literal["none", "confirmed", "false_alarm"]
HumanAction = Literal["view", "confirm", "false_alarm", "send_to_master", "accept", "resolve"]
LogAction = Literal[
    "published", "viewed", "confirmed", "false_alarm", "sent_to_master", "level_escalated",
    "timeout_escalated", "master_accepted", "resolved", "auto_finished", "superseded",
]
EventMode = Literal["replay", "demo"]
CameraStateKind = Literal["normal", "yellow", "red", "no_observation"]
NoObservationReason = Literal["no_source", "processing", "failed", "ended", "stale", "dark", "obstructed"]
VideoStatus = Literal["uploaded", "processing", "ready", "failed"]
JobKind = Literal["process", "recompute"]
JobStatus = Literal["queued", "running", "retry_wait", "done", "failed"]
JobStage = Literal["queued", "inference_detect", "inference_pose", "analysis", "evidence", "done"]
JobErrorCode = Literal[
    "linq_unavailable", "timeout", "remote_error", "bad_output",
    "model_missing", "video_unreadable", "artifacts_missing", "internal",
]
Fault = Literal["unavailable", "timeout", "remote_error", "bad_output"]
BackendName = Literal["linq", "local"]
BackendState = Literal["ok", "models_missing", "unreachable", "bad_answer", "unchecked"]
ModelTask = Literal["detect", "pose"]
ObsState = Literal["P", "N", "U"]
EndReason = Literal["observed_exit", "track_lost_timeout", "video_end"]
ScenarioStatus = Literal["active", "model_missing", "skeleton"]
BroadcastStatus = Literal["playing", "stopped", "ended"]
ZoneGeometry = Literal["polygon", "line"]
ObjectKind = Literal["person", "vehicle", "phone", "other"]
Posture = Literal["upright", "lying", "unknown"]
Sound = Literal["siren", "chime", "none"]
DeliveryKind = Literal["published", "escalated", "to_master"]
WsType = Literal[
    "hello", "event.created", "event.updated", "event.escalated", "notification",
    "camera.state", "sector.state", "job.progress", "broadcast.state", "backend.status",
]

Point = tuple[float, float]  # normalized image coords (0..1) or meters on the floor
Box = tuple[float, float, float, float]  # x1, y1, x2, y2
Keypoint = tuple[float, float, float]  # x, y, conf


# --- common, meta ------------------------------------------------------------------------
class ApiError(BaseModel):
    code: str
    message: str  # Russian, shown to the user as is
    details: dict[str, str | int | float | None] = {}


class Health(BaseModel):
    status: Literal["ok"]
    contract: str


class LevelMeta(BaseModel):
    id: Level
    title: str
    color: str


class StatusMeta(BaseModel):
    id: EventStatus
    title: str
    terminal: bool


class RoleMeta(BaseModel):
    id: Role
    title: str
    actions: list[HumanAction]


class ZoneKindMeta(BaseModel):
    id: str
    title: str
    color: str
    geometry: ZoneGeometry
    description: str


class ScenarioParam(BaseModel):
    key: str
    title: str
    unit: str
    default: float
    min: float
    max: float


class ScenarioMeta(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    default_level: Level
    status: ScenarioStatus
    status_text: str
    required_classes: list[str]
    zone_kinds: list[str]
    params: list[ScenarioParam]


class Meta(BaseModel):
    product_name: str
    contract: str
    inference_backend: BackendName
    fake: bool
    timezone: str
    roles: list[RoleMeta]
    levels: list[LevelMeta]
    statuses: list[StatusMeta]
    zone_kinds: list[ZoneKindMeta]
    scenarios: list[ScenarioMeta]


class SeedReport(BaseModel):
    skipped: bool
    sectors: int
    cameras: int
    zones: int
    events: int
    videos: int


# --- sectors, cameras --------------------------------------------------------------------
class Sector(BaseModel):
    id: int
    name: str
    sort_order: int
    is_demo: bool


class SectorIn(BaseModel):
    name: str
    sort_order: int = 0


class Camera(BaseModel):
    id: int
    sector_id: int
    name: str
    description: str
    is_demo: bool
    has_calibration: bool
    zones_count: int
    videos_count: int


class CameraIn(BaseModel):
    sector_id: int
    name: str
    description: str = ""


class CameraPatch(BaseModel):
    sector_id: int | None = None
    name: str | None = None
    description: str | None = None


class CamerasAdminView(BaseModel):
    sectors: list[Sector]
    cameras: list[Camera]


# --- videos, jobs, models ----------------------------------------------------------------
class Video(BaseModel):
    id: int
    camera_id: int
    filename: str
    sha256: str
    size_bytes: int
    width: int
    height: int
    fps: float
    frame_count: int
    duration_ms: int
    codec: str
    browser_playable: bool
    status: VideoStatus
    active_analysis_id: int | None
    created_at: datetime


class InferenceMetrics(BaseModel):
    backend: BackendName
    fake: bool
    model_id: str
    model_version: str
    task: ModelTask
    input_size: int
    step: int
    frames_processed: int
    wall_s: float  # processing time without upload and polling
    throughput_fps: float
    preprocess_ms: float | None
    postprocess_ms: float | None
    tpu_rtt_p50_ms: float | None  # linq only
    tpu_rtt_p90_ms: float | None
    upload_s: float | None  # linq only
    total_s: float  # end to end: upload, start, polling, download
    cached: bool


class Job(BaseModel):
    id: int
    kind: JobKind
    video_id: int
    camera_id: int
    backend: BackendName
    fake: bool
    status: JobStatus
    stage: JobStage
    progress: float
    attempts: int
    next_attempt_at: datetime | None
    error_code: JobErrorCode | None
    error_text: str | None
    metrics: list[InferenceMetrics]
    analysis_id: int | None
    analysis_ms: int | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None


class UploadResult(BaseModel):
    video: Video
    job: Job | None  # None: the same file is already processed for this camera
    reused: bool


class ModelSpec(BaseModel):
    id: str
    version: str
    task: ModelTask
    input_size: int
    conf: float  # floor written to JSONL; rule thresholds live in class_conf
    iou: float
    classes: dict[int, str]  # kept classes: id -> name used by rules
    linq_program: str | None
    linq_tail: str | None  # local path of the tail ONNX, uploaded next to the worker
    local_onnx: str | None


class ModelsView(BaseModel):
    backend: BackendName
    fake: bool
    active: list[ModelSpec]
    available: list[ModelSpec]


class BackendStatus(BaseModel):
    backend: BackendName
    fake: bool
    state: BackendState
    checked_at: datetime | None
    latency_ms: float | None
    present: list[str]  # programs or model files found
    missing: list[str]
    message: str


# --- HUD, analysis -----------------------------------------------------------------------
class HudTag(BaseModel):
    code: str  # "speed", "zone", "lying", "still", "phone", "feet_hidden", "too_small", "<scenario>"
    text: str  # "бег 3,1 м/с"
    level: Level | None


class HudObject(BaseModel):
    track_id: int | None
    kind: ObjectKind
    label: str  # "человек", "грузовик", "телефон"
    score: float
    bbox: Box  # normalized 0..1
    kpts: list[Keypoint] | None  # normalized x, y and conf, 17 COCO points
    tags: list[HudTag]


class HudFrame(BaseModel):
    frame_idx: int
    ts_ms: int
    objects: list[HudObject]


class TracksWindow(BaseModel):
    video_id: int
    analysis_id: int
    from_ms: int
    to_ms: int
    frames: list[HudFrame]


class ObservabilityGap(BaseModel):
    start_ms: int
    end_ms: int
    reason: NoObservationReason  # stale | dark | obstructed


class Evidence(BaseModel):
    id: int
    kind: Literal["confirm", "escalate"]
    frame_idx: int
    ts_ms: int
    url: str
    sha256: str
    objects: list[HudObject]


class Episode(BaseModel):
    id: int
    analysis_id: int
    scenario: str
    scenario_title: str
    subject: str
    zone_id: int | None
    level_initial: Level
    level_max: Level
    start_ms: int
    confirm_ms: int
    escalate_ms: int | None
    end_ms: int
    end_reason: EndReason
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    uncertain_ms: int
    evidence: list[Evidence]


class Analysis(BaseModel):
    id: int
    video_id: int
    version: int
    created_at: datetime
    duration_ms: int
    pose_used: bool
    episodes: list[Episode]
    gaps: list[ObservabilityGap]


# --- calibration, zones, rules -----------------------------------------------------------
class ControlPoint(BaseModel):
    image: Point
    world: Point


class CalibrationIn(BaseModel):
    image_points: list[Point]
    world_points: list[Point]
    control_points: list[ControlPoint] = []


class Calibration(BaseModel):
    camera_id: int
    image_points: list[Point]
    world_points: list[Point]
    control_points: list[ControlPoint]
    fit_rmse_m: float
    control_rmse_m: float | None
    grid: list[tuple[Point, Point]]  # normalized segments of the 1 m floor grid
    updated_at: datetime


class Zone(BaseModel):
    id: int
    camera_id: int
    kind: str
    name: str
    points: list[Point]


class ZoneIn(BaseModel):
    kind: str
    name: str
    points: list[Point]


class ZonePatch(BaseModel):
    name: str | None = None
    points: list[Point] | None = None


class CameraRule(BaseModel):
    camera_id: int
    scenario: str
    enabled: bool
    params: dict[str, float]  # overrides
    effective: dict[str, float]  # defaults from config + overrides
    status: ScenarioStatus


class CameraRuleIn(BaseModel):
    enabled: bool
    params: dict[str, float] = {}


class RulesScreenRow(BaseModel):
    camera: Camera
    rules: list[CameraRule]


class RulesScreenView(BaseModel):
    scenarios: list[ScenarioMeta]
    rows: list[RulesScreenRow]


# --- broadcast, states -------------------------------------------------------------------
class Broadcast(BaseModel):
    id: int
    camera_id: int
    video_id: int
    analysis_id: int
    status: BroadcastStatus
    loop: bool
    cycle: int
    started_at: datetime
    position_ms: int
    duration_ms: int
    server_now: datetime


class BroadcastIn(BaseModel):
    video_id: int | None = None  # None: the latest ready video of the camera
    loop: bool | None = None  # None: broadcast.loop_default


class CameraState(BaseModel):
    camera_id: int
    sector_id: int
    state: CameraStateKind
    reason: NoObservationReason | None
    reason_text: str
    freshness_ms: int | None
    open_yellow: int
    open_red: int


class SectorState(BaseModel):
    sector_id: int
    name: str
    state: CameraStateKind
    reason_text: str
    cameras_total: int
    cameras_no_observation: int
    open_yellow: int
    open_red: int


class CameraSetupView(BaseModel):
    camera: Camera
    videos: list[Video]
    jobs: list[Job]
    calibration: Calibration | None
    zones: list[Zone]
    rules: list[CameraRule]
    broadcast: Broadcast | None


# --- events ------------------------------------------------------------------------------
class EventSummary(BaseModel):
    id: int
    scenario: str
    title: str
    level: Level
    status: EventStatus
    status_title: str
    operator_verdict: Verdict
    escalated_by_timeout: bool
    mode: EventMode
    camera_id: int
    camera_name: str
    sector_id: int
    sector_name: str
    zone_id: int | None
    zone_name: str | None
    reason_text: str
    notification_text: str
    started_at: datetime
    published_at: datetime
    red_at: datetime | None
    ended_at: datetime | None
    duration_s: float  # until ended_at, or until now while the episode lasts
    priority: int
    is_demo: bool


class OperatorDashboard(BaseModel):
    sectors: list[SectorState]
    feed: list[EventSummary]
    server_now: datetime


class CameraTile(BaseModel):
    camera: Camera
    state: CameraState
    broadcast: Broadcast | None
    preview_url: str | None


class SectorView(BaseModel):
    sector: SectorState
    cameras: list[CameraTile]
    feed: list[EventSummary]


class CameraLiveView(BaseModel):
    camera: Camera
    state: CameraState
    broadcast: Broadcast | None
    video: Video | None
    analysis: Analysis | None
    zones: list[Zone]
    calibration: Calibration | None


class WhyItem(BaseModel):
    label: str
    value: str


class EventAction(BaseModel):
    id: int
    at: datetime
    actor_role: ActorRole
    actor_name: str
    action: LogAction
    from_status: EventStatus | None
    to_status: EventStatus | None
    comment: str


class Provenance(BaseModel):
    backend: BackendName | None
    fake: bool
    det_model: str | None  # "det-yolov8n@640-ap9999"
    pose_model: str | None
    job_id: int | None
    video_sha256: str | None
    analysis_version: int | None
    rule_params: dict[str, float]
    evidence_sha256: str | None


class Delivery(BaseModel):
    channel: str
    kind: DeliveryKind
    status: Literal["sent", "failed"]
    http_status: int | None
    error: str
    at: datetime


class EventDetail(BaseModel):
    event: EventSummary
    episode: Episode | None  # None for demo events
    why: list[WhyItem]
    actions: list[EventAction]
    allowed_actions: list[HumanAction]  # for the X-Role of the request
    provenance: Provenance
    deliveries: list[Delivery]
    video_id: int | None
    video_start_ms: int | None
    video_end_ms: int | None
    broadcast: Broadcast | None  # current broadcast of the camera, for the live half


class ActionIn(BaseModel):
    action: HumanAction
    comment: str = ""


class EventFilter(BaseModel):
    level: Level | None = None
    scenario: str | None = None
    status: EventStatus | None = None
    sector_id: int | None = None
    camera_id: int | None = None
    zone_id: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    q: str | None = None
    include_demo: bool = True
    include_superseded: bool = False
    limit: int = 50
    cursor: str | None = None


class EventPage(BaseModel):
    items: list[EventSummary]
    total: int
    next_cursor: str | None


class FacetItem(BaseModel):
    id: str
    title: str


class JournalFacets(BaseModel):
    scenarios: list[FacetItem]
    levels: list[FacetItem]
    statuses: list[FacetItem]
    sectors: list[FacetItem]
    cameras: list[FacetItem]
    zones: list[FacetItem]


class MasterInbox(BaseModel):
    active: list[EventSummary]  # sent_to_master, master_accepted
    recent_resolved: list[EventSummary]
    server_now: datetime


class CountRow(BaseModel):
    key: str
    title: str
    count: int
    confirmed: int
    false_alarm: int


class ShiftSummary(BaseModel):
    shift_id: str
    title: str
    start: datetime
    end: datetime
    total: int
    by_sector: list[CountRow]
    by_scenario: list[CountRow]
    events: list[EventSummary]


# --- stats, system -----------------------------------------------------------------------
class Percentiles(BaseModel):
    n: int
    pending: int
    p50: float | None
    p95: float | None


class DayRow(BaseModel):
    date: str  # YYYY-MM-DD in Europe/Moscow
    yellow: int
    red: int
    confirmed: int
    false_alarm: int


class OhsStats(BaseModel):
    date_from: datetime
    date_to: datetime
    include_demo: bool
    total: int
    by_status: list[CountRow]
    by_scenario: list[CountRow]
    by_sector: list[CountRow]
    by_camera: list[CountRow]
    by_shift: list[CountRow]
    by_hour: list[CountRow]
    by_day: list[DayRow]
    reviewed: int
    false_alarm_share: float | None
    review_coverage: float | None
    operator_reaction_s: Percentiles
    master_accept_s: Percentiles
    master_resolve_s: Percentiles


class WeekRow(BaseModel):
    week_start: str  # Monday, YYYY-MM-DD in Europe/Moscow
    yellow: int
    red: int
    confirmed: int
    false_alarm: int


class RateRow(BaseModel):
    key: str
    title: str
    cameras: int
    confirmed: int
    per_camera: float | None


class TrendSummary(BaseModel):
    previous: int
    recent: int
    change_pct: float | None
    text: str


class ManagementStats(BaseModel):
    weeks: list[WeekRow]
    top_sectors: list[RateRow]
    top_scenarios: list[CountRow]
    yellow_trend: TrendSummary


class LatencyStats(BaseModel):
    notify_delay_s: Percentiles  # published_at - started_at
    publish_lag_ms: Percentiles  # published_at - planned confirm wall time


class Channel(BaseModel):
    name: str
    kind: Literal["ws", "webhook"]
    target: str  # host only, never a full URL with secrets
    levels: list[Level]


class SystemView(BaseModel):
    backend: BackendName
    fake: bool
    backend_status: BackendStatus
    queue: list[Job]
    recent_jobs: list[Job]
    cameras: list[CameraState]
    models: list[ModelSpec]
    latency: LatencyStats
    channels: list[Channel]
    server_now: datetime


# --- realtime ----------------------------------------------------------------------------
class Notification(BaseModel):
    id: str
    event_id: int
    level: Level
    text: str
    audience: list[Role]
    sound: Sound
    takeover: bool


class WsHello(BaseModel):
    server_now: datetime
    contract: str
    role: Role


class WsMessage(BaseModel):
    type: WsType
    at: datetime
    data: (
        WsHello | EventSummary | Notification | CameraState | SectorState
        | Job | Broadcast | BackendStatus
    )


# --- pipeline (internal) -----------------------------------------------------------------
class Detection(BaseModel):  # one item of an artifact JSONL line, pixels of the source frame
    cls: int
    name: str
    score: float
    bbox_xyxy: Box
    kpts: list[Keypoint] | None = None


class FrameDetections(BaseModel):  # one artifact JSONL line
    frame_idx: int
    ts_ms: float
    detections: list[Detection]


class PersonState(BaseModel):
    track_id: int
    bbox: Box  # pixels
    score: float
    foot: Point  # pixels, bbox bottom center
    anchor: Point  # pixels: lowest visible ankle, else foot
    feet_visible: bool
    ground: Point | None  # meters, only inside the calibrated hull
    height_px: float
    ref_height_px: float  # H_ref: median upright height, frozen while lying
    speed_bh_s: float | None
    speed_m_s: float | None
    posture: Posture
    posture_method: Literal["pose", "bbox"]
    torso_deg: float | None  # torso angle from vertical, pose only
    last_upright_ms: int | None  # last frame where posture was upright
    lying_since_ms: int | None  # start of the current continuous lying run
    still_since_ms: int | None  # since when the bbox center stays within features.still_motion_bh
    prev_anchor: Point | None  # anchor at the previous observation of this track
    prev_ts_ms: int | None
    kpts: list[Keypoint] | None  # pixels


class VehicleState(BaseModel):
    track_id: int
    name: str
    bbox: Box
    score: float
    footprint: tuple[Point, Point] | None  # meters: bottom edge on the floor
    height_px: float
    speed_vh_s: float | None  # own bbox heights per second
    speed_m_s: float | None


class ObjectState(BaseModel):  # untracked objects: phones and extra-model classes
    name: str
    bbox: Box
    score: float


class FrameContext(BaseModel):
    frame_idx: int
    ts_ms: int
    width: int
    height: int
    persons: list[PersonState]
    vehicles: list[VehicleState]
    objects: list[ObjectState]
    zones: list[Zone]
    calibrated: bool


class Observation(BaseModel):
    scenario: str
    subject: str
    state: ObsState
    level: Level
    hold_s: float  # how long P must last before the episode is confirmed at this level
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    zone_id: int | None
    anchor: Point | None  # pixels, used to merge a track id switch
    ref_height_px: float | None


class AnalysisConfig(BaseModel):  # snapshot stored in analyses.config_json
    width: int
    height: int
    fps: float
    step: int
    calibration: Calibration | None
    zones: list[Zone]
    rules: dict[str, CameraRule]  # by scenario
    class_conf: dict[str, float]
    active_classes: list[str]  # class names provided by the active models


class EpisodeDraft(BaseModel):
    scenario: str
    subject: str
    zone_id: int | None
    level_initial: Level
    level_max: Level
    start_ms: int
    confirm_ms: int
    escalate_ms: int | None
    end_ms: int
    end_reason: EndReason
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    uncertain_ms: int
    confirm_frame_idx: int
    escalate_frame_idx: int | None


class AnalysisResult(BaseModel):
    hud: list[HudFrame]
    episodes: list[EpisodeDraft]
    gaps: list[ObservabilityGap]
    pose_used: bool


# --- evaluation (slice 14) ---------------------------------------------------------------
class ExpectedEvent(BaseModel):
    scenario: str
    start_s: float
    end_s: float


class EvalVideo(BaseModel):
    path: str
    camera_id: int | None = None  # take calibration, zones, rules of this camera; None: defaults
    expected: list[ExpectedEvent]


class EvalLabels(BaseModel):
    deadline_s: float | None = None  # None: eval.deadline_s
    videos: list[EvalVideo]


class EvalMetrics(BaseModel):
    scenario: str  # "*" for the total row
    expected: int
    episodes: int
    tp: int
    fn: int
    fp: int
    duplicates: int
    late: int
    precision: float | None
    recall: float | None
    f1: float | None
    fp_per_hour: float | None
    delay_s: Percentiles


class EvalReport(BaseModel):
    created_at: datetime
    labels: str
    hours: float
    deadline_s: float
    rows: list[EvalMetrics]
    out_dir: str


# --- protocols (tech.md 6.1) -------------------------------------------------------------
class RemoteShell(Protocol):  # LinQ Jupyter: inference/linq.JupyterShell, fakes/remote.FakeRemoteShell
    def upload(self, local: Path, remote: str) -> None: ...
    def download(self, remote: str, local: Path) -> int: ...
    def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]: ...
    def size(self, remote: str) -> int | None: ...


class InferenceBackend(Protocol):  # inference/linq.LinqBackend, inference/local.LocalBackend
    name: BackendName

    def run(
        self, video: Path, video_sha256: str, model: ModelSpec, step: int, out: Path,
        progress: Callable[[float], None],
    ) -> InferenceMetrics: ...
    def check(self) -> BackendStatus: ...


class ScenarioPlugin(Protocol):  # rules/*.py
    meta: ScenarioMeta  # status and status_text are filled by rules.scenario_metas()

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]: ...
    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]: ...


class DeliveryChannel(Protocol):  # delivery.WebhookChannel
    name: str

    def deliver(self, event: EventSummary, kind: DeliveryKind) -> tuple[bool, int | None, str]: ...
```

### 5.3 Файлы на диске

Корень данных — `data_dir` из конфига (`data/app/`), путь в базе хранится относительно него.

| Путь | Что | Пишет |
| --- | --- | --- |
| `safewatch.db` | база | `db`, `store` |
| `server.pid` | `{"pid": int, "create_time": float}` | `cli serve` |
| `uploads/<sha256><ext>` | исходное видео | `services.video_upload` |
| `artifacts/<cache_key>.jsonl` | детекции по кадрам, формат ниже | `inference.linq`, `inference.local` |
| `artifacts/<cache_key>.summary.json` | сводка воркера + `end_to_end_s` | `inference.linq`, `inference.local` |
| `analyses/<video_id>-v<version>/hud.jsonl` | одна строка `HudFrame` на анализированный кадр | `services.run_next_job` (данные от `analysis.pipeline`) |
| `evidence/<episode_id>-<kind>.jpg` | доказательный кадр, ширина до `evidence.max_width` | `services.run_next_job` (кадр от `media.read_frame`) |
| `eval/<YYYYMMDD-HHMMSS>/report.json`, `report.md` | отчёт оценки | `services.eval_run` |

Строка артефакта (формат `video_worker.py`, `LINQ_CONTRACT.md` §6.4), одна на обработанный кадр, `frame_idx` строго растёт:
```json
{"frame_idx": 12, "ts_ms": 480.0, "detections": [{"cls": 0, "name": "person", "score": 0.91, "bbox_xyxy": [143.6, 372.1, 289.8, 635.1], "kpts": [[273.46, 409.45, 0.5], "... 17 точек"]}]}
```
Поле `name` из JSONL не используется: имя класса берётся из `ModelSpec.classes` (у pose воркер пишет `"0"`).

Ключ кэша: `cache_key = sha256(f"{CACHE_SCHEMA}|{video_sha256}|{model.id}|{model.version}|{model.input_size}|{step}|{backend}|{int(fake)}")`, hex.

### 5.4 Каких полей нет

Нет пользователей, паролей, сессий и токенов. Нет ссылки на работника в событиях (v5, было → стало: работник — три текстовых поля события, заполняемых человеком вручную, без справочника работников, S26). Нет видеоклипов (доказательство — кадры) (v5, было → стало: клип — окно исходного видео `Clip`, отдельных файлов клипов нет, S18). Нет сырых тензоров. Нет таблицы настроек: всё в yaml. Нет отдельного поля «принятые меры»: это комментарий действия `resolve`. Нет SLA-полей и сроков. Нет признака «отложено». Понадобилось поле → `CONTRACT GAP`.

## 6. Интерфейсы (заморожены)

### 6.1 Внешние клиенты и бэкенды инференса

Внешний сервис один: LinQ Jupyter (через туннель). Его протокол `RemoteShell` (5.2). Реализации:

```python
# src/safewatch/inference/linq.py
class JupyterShell:  # RemoteShell over JupyterRemote from tools/linq/jupyter_remote.py
    def __init__(self, settings: Settings) -> None: ...  # lazy: logs in on the first call

class LinqBackend:  # InferenceBackend
    name: BackendName = "linq"
    def __init__(self, settings: Settings, shell: RemoteShell) -> None: ...

# src/safewatch/inference/local.py
class LocalBackend:  # InferenceBackend: onnxruntime on CPU, same JSONL as the worker
    name: BackendName = "local"
    def __init__(self, settings: Settings) -> None: ...

# src/safewatch/inference/__init__.py
def make_backend(settings: Settings) -> InferenceBackend: ...
# linq + fake=False -> LinqBackend(JupyterShell); linq + fake=True -> LinqBackend(FakeRemoteShell());
# local -> LocalBackend (fake does not apply: no external service)

# src/safewatch/fakes/remote.py
class FakeRemoteShell:  # RemoteShell
    def __init__(self, script: list[Fault | None] | None = None, scene: str = "auto") -> None: ...
    calls: list[str]  # markers of executed commands ("home", "start", "poll", "log", "kill"), for tests

# src/safewatch/fakes/scenes.py
SCENES = ("demo", "walk", "running", "fall", "lying_still", "phone", "vehicle", "fence",
          "under", "two_walkers_crossing", "dark", "empty")
def render(scene: str, width: int, height: int, fps: float, frame_count: int, step: int,
           task: ModelTask, seed: int = 0) -> list[FrameDetections]: ...
def to_jsonl(frames: list[FrameDetections]) -> str: ...
```

`JupyterShell` импортирует `JupyterRemote` из `<linq.tools_dir>/jupyter_remote.py` по пути и создаёт его конструктором `JupyterRemote(url, user, password, token)` из полей `Settings`, а не через `from_env()`. Исключения `requests.ConnectionError`, `requests.Timeout`, `websocket.WebSocketException`, `OSError`, `JupyterError` превращаются в `InferenceError("linq_unavailable", <текст без секретов>)`; превышение `timeout` у `exec` — в `InferenceError("timeout", ...)`. `size(remote)` возвращает размер файла по Contents API или `None`.

Команды `LinqBackend` к `RemoteShell`. Каждая заканчивается маркером `# sw:<имя>`: фейк узнаёт команду по маркеру. `<abs>` — `$HOME/work/<linq.remote_dir>`, `<out>` — `<abs>/out/<file_prefix><cache_key[:16]>_<task>.jsonl`.

| Шаг | Вызов |
| --- | --- |
| домашняя папка | `exec("echo $HOME  # sw:home")` |
| файлы воркера | `upload(<tools_dir>/linq_tpu.py, baseline/linq_tpu.py)`, так же `yolo_io.py` и `remote/video_worker.py` |
| хвост модели | `upload(<model.linq_tail>, baseline/tails/<имя файла>)` |
| видео | если `size(baseline/videos/<file_prefix><sha256[:12]><ext>)` не равен размеру файла: `upload(...)` |
| старт | `exec("mkdir -p <abs>/out && cd <abs> && rm -f <out>.progress && (setsid nohup python video_worker.py --video videos/<имя> --program <model.linq_program> --out <out> --size <input_size> --step <step> --task <task> --conf <model.conf> --iou <model.iou> --inflight <linq.inflight> [--classes <ключи model.classes через запятую>] --tail tails/<имя> > <out>.log 2>&1 < /dev/null & echo $! > <out>.pid) && echo started  # sw:start")` |
| опрос раз в `linq.poll_interval_s` | `exec("cat <out>.progress 2>/dev/null; echo; kill -0 $(cat <out>.pid) 2>/dev/null && echo RUNNING \|\| echo STOPPED  # sw:poll")` |
| хвост лога при STOPPED без finished | `exec("tail -30 <out>.log  # sw:log")` |
| остановка при таймауте | `exec("kill $(cat <out>.pid) 2>/dev/null; echo killed  # sw:kill")` |
| результат | `download(<out относительно ~/work>, artifacts/<cache_key>.jsonl)` и `.summary.json` |
| проверка связи (`check`, S3) | `exec("echo ok  # sw:check")`, ответ ровно `ok` |
| программы (`check`, S3) | `exec("ls -1 <linq.programs_dir>  # sw:ls")`, имена файлов по строке |

Таймаут каждого `exec` — `linq.call_timeout_s`; весь прогон — `linq.job_timeout_s`. `--classes` передаётся только для детектора из `pipeline.detector`; модели `pipeline.extra` отдают все свои классы и получают `--nc <число классов>` (S10). Фейк на `# sw:check` отвечает `ok`, на `# sw:ls` — имена программ всех моделей реестра.

Поведение `FakeRemoteShell` по записи сценария. Запись берётся на команде `# sw:home` (с неё начинается каждый прогон), последняя запись повторяется, пустой сценарий — всё `None`:

| Запись | Фейк | Итог задачи (8.1) |
| --- | --- | --- |
| `None` | файлы в памяти; `# sw:start` строит JSONL через `scenes.render` по метаданным загруженного видео и сцене; `# sw:poll` сразу отдаёт `{"done": N, "finished": true}` и `STOPPED` | `done` |
| `unavailable` | каждый вызов прогона бросает `InferenceError("linq_unavailable", ...)` | `retry_wait`, после `jobs.max_attempts` → `failed` (`linq_unavailable`) |
| `timeout` | `# sw:poll` всегда `{"done": 0}` и `RUNNING` | по `linq.job_timeout_s` команда `# sw:kill`, `retry_wait` (`timeout`) |
| `remote_error` | `# sw:poll` без `finished` и `STOPPED`; `# sw:log` отдаёт `RuntimeError: TPU error frame 0: status -3` | `retry_wait` (`remote_error`) |
| `bad_output` | `finished`, но в JSONL строка `not json` | `failed` (`bad_output`) |

Сцена `auto` выбирается по имени загруженного файла: `run`/`бег` → `running`, `fall`/`пад` → `fall`, `phone`/`тел` → `phone`, `truck`/`car`/`погруз` → `vehicle`, `fence`/`забор` → `fence`, `dark` → `dark`, иначе `demo` (идёт 3 с, бежит 3 с, идёт 2 с, падает и лежит неподвижно 12 с).

Канал доставки (точка расширения для ламп и сирен), слайс 15:

```python
# src/safewatch/delivery.py
class WebhookChannel:  # DeliveryChannel: POST JSON to delivery.webhooks[i].url, timeout from config
    def __init__(self, name: str, url: str, levels: list[Level], timeout_s: float) -> None: ...
```

### 6.2 Фасад: `src/safewatch/services.py`

API, CLI и `worker.py` зовут только эти функции. Синхронные функции выполняются в потоке event loop; асинхронные отдают блокирующую работу в `asyncio.to_thread`.

```python
def health() -> Health: ...
def seed_demo(videos_dir: Path | None = None) -> SeedReport: ...
def meta() -> Meta: ...
def cameras_admin_view() -> CamerasAdminView: ...
def sectors_list() -> list[Sector]: ...
def sector_create(data: SectorIn, role: Role | None) -> Sector: ...
def sector_update(sector_id: int, data: SectorIn, role: Role | None) -> Sector: ...
def sector_delete(sector_id: int, role: Role | None) -> None: ...
def cameras_list(sector_id: int | None = None) -> list[Camera]: ...
def camera_get(camera_id: int) -> Camera: ...
def camera_create(data: CameraIn, role: Role | None) -> Camera: ...
def camera_update(camera_id: int, data: CameraPatch, role: Role | None) -> Camera: ...
def camera_delete(camera_id: int, role: Role | None) -> None: ...
async def video_upload(
    camera_id: int, filename: str, chunks: AsyncIterator[bytes], role: Role | None
) -> UploadResult: ...
def video_import(camera_id: int, path: Path) -> UploadResult: ...
def videos_list(camera_id: int) -> list[Video]: ...
def video_get(video_id: int) -> Video: ...
def video_file(video_id: int) -> Path: ...
def jobs_list(status: JobStatus | None = None, limit: int = 50) -> list[Job]: ...
def job_get(job_id: int) -> Job: ...
async def run_next_job() -> Job | None: ...
def camera_setup_view(camera_id: int) -> CameraSetupView: ...
def job_retry(job_id: int, role: Role | None) -> Job: ...
def recover_jobs() -> int: ...
async def backend_check(force: bool = False) -> BackendStatus: ...
def models_view() -> ModelsView: ...
def system_view() -> SystemView: ...
def video_tracks(video_id: int, from_ms: int, to_ms: int) -> TracksWindow: ...
def video_analysis(video_id: int) -> Analysis: ...
def video_recompute(video_id: int, role: Role | None) -> Job: ...
def evidence_file(evidence_id: int) -> Path: ...
def broadcast_get(camera_id: int) -> Broadcast | None: ...
def broadcast_start(camera_id: int, data: BroadcastIn, role: Role | None) -> Broadcast: ...
def broadcast_stop(camera_id: int, role: Role | None) -> None: ...
def broadcast_tick() -> int: ...
def camera_states() -> list[CameraState]: ...
def operator_dashboard_view() -> OperatorDashboard: ...
def operator_feed() -> list[EventSummary]: ...
def sector_view(sector_id: int) -> SectorView: ...
def camera_live_view(camera_id: int) -> CameraLiveView: ...
async def camera_preview(camera_id: int) -> bytes: ...
def event_detail(event_id: int, role: Role | None) -> EventDetail: ...
def event_action(event_id: int, data: ActionIn, role: Role | None, actor: str | None) -> EventDetail: ...
def escalation_tick() -> int: ...
def master_inbox_view() -> MasterInbox: ...
def shift_summary_view(at: datetime | None = None) -> ShiftSummary: ...
def calibration_get(camera_id: int) -> Calibration | None: ...
def calibration_set(camera_id: int, data: CalibrationIn, role: Role | None) -> Calibration: ...
def calibration_delete(camera_id: int, role: Role | None) -> None: ...
def zones_list(camera_id: int) -> list[Zone]: ...
def zone_create(camera_id: int, data: ZoneIn, role: Role | None) -> Zone: ...
def zone_update(zone_id: int, data: ZonePatch, role: Role | None) -> Zone: ...
def zone_delete(zone_id: int, role: Role | None) -> None: ...
def camera_rules(camera_id: int) -> list[CameraRule]: ...
def camera_rule_set(camera_id: int, scenario: str, data: CameraRuleIn, role: Role | None) -> CameraRule: ...
def rules_screen_view() -> RulesScreenView: ...
def events_list(f: EventFilter) -> EventPage: ...
def events_export_csv(f: EventFilter) -> str: ...
def journal_facets() -> JournalFacets: ...
def ohs_stats_view(
    date_from: datetime | None = None, date_to: datetime | None = None,
    sector_id: int | None = None, camera_id: int | None = None, include_demo: bool = True,
) -> OhsStats: ...
def management_view(weeks: int | None = None, include_demo: bool = True) -> ManagementStats: ...
def eval_run(labels: Path, out_dir: Path | None = None) -> EvalReport: ...
async def deliveries_flush() -> int: ...
```

Исключения (`src/safewatch/errors.py`): `AppError(message: str, **details)` с полями `code` и `status`; наследники `NotFound` (`not_found`, 404), `ValidationFailed` (`validation`, 422), `Conflict(code, message)` (409, код из таблицы ниже), `Forbidden` (`forbidden_role`, 403), `RoleRequired` (`role_required`, 400), `TooLarge` (`too_large`, 413), `UnsupportedVideo` (`unsupported_video`, 415). Отдельно `InferenceError(code: JobErrorCode, message: str)`: бросают бэкенды и `RemoteShell`, ловит `run_next_job` и превращает в статус задачи (8.1), наружу он не выходит. `NotImplementedError` из незаконченного слайса API превращает в 501 `not_implemented`. Тело любой ошибки — `ApiError`.

Коды `Conflict`: `name_taken`, `sector_not_empty`, `job_not_failed`, `video_not_ready`, `no_ready_video`, `artifacts_missing`, `invalid_transition`.

| Функция | Пишет в хранилище | Исключения | Код: REST | Код: CLI | Слайс |
| --- | --- | --- | --- | --- | --- |
| `health()` | нет | нет | — | — | 0 |
| `seed_demo(videos_dir)` | sectors, cameras, zones, camera_rules, events, event_actions (`is_demo=1`); с `videos_dir` ещё videos, jobs | `NotFound` (нет папки) | — | exit 3 | 0 |
| `meta()` | нет | нет | — | — | 1 |
| `cameras_admin_view()` | нет | нет | — | — | 1 |
| `sectors_list()` | нет | нет | — | — | 1 |
| `sector_create(data, role)` | sectors | `RoleRequired`, `Forbidden`, `ValidationFailed`, `Conflict(name_taken)` | 400, 403, 422, 409 | — | 1 |
| `sector_update(sector_id, data, role)` | sectors | те же + `NotFound` | 400, 403, 422, 409, 404 | — | 1 |
| `sector_delete(sector_id, role)` | sectors | `RoleRequired`, `Forbidden`, `NotFound`, `Conflict(sector_not_empty)` | 400, 403, 404, 409 | — | 1 |
| `cameras_list(sector_id)` | нет | `NotFound` (сектор) | 404 | — | 1 |
| `camera_get(camera_id)` | нет | `NotFound` (нет или удалена) | 404 | — | 1 |
| `camera_create(data, role)` | cameras (правил не пишет: нет строки `camera_rules` — значит настройки по умолчанию, 8.3) | `RoleRequired`, `Forbidden`, `ValidationFailed` (имя, нет сектора) | 400, 403, 422 | — | 1 |
| `camera_update(camera_id, data, role)` | cameras | `RoleRequired`, `Forbidden`, `NotFound`, `ValidationFailed` | 400, 403, 404, 422 | — | 1 |
| `camera_delete(camera_id, role)` | cameras.deleted_at; играющий эфир → `stopped` | `RoleRequired`, `Forbidden`, `NotFound` | 400, 403, 404 | — | 1 |
| `video_upload(camera_id, filename, chunks, role)` | файл `uploads/`, videos, jobs | `RoleRequired`, `Forbidden`, `NotFound`, `TooLarge`, `UnsupportedVideo` | 400, 403, 404, 413, 415 | — | 2 |
| `video_import(camera_id, path)` | то же | `NotFound` (камера, файл), `TooLarge`, `UnsupportedVideo` | — | exit 3, 2, 2 | 2 |
| `videos_list(camera_id)` | нет | `NotFound` | 404 | — | 2 |
| `video_get(video_id)` | нет | `NotFound` | 404 | — | 2 |
| `video_file(video_id)` | нет | `NotFound` | 404 | — | 2 |
| `jobs_list(status, limit)` | нет | `ValidationFailed` (limit вне 1..`jobs.list_max`) | 422 | — | 2 |
| `job_get(job_id)` | нет | `NotFound` | 404 | — | 2 |
| `run_next_job()` | jobs, artifacts, videos; с S4 analyses и файл HUD; с S5 episodes, evidence; с S6 broadcasts (автостарт); с S9 events (`superseded`) | нет: ошибки бэкенда становятся статусом задачи (8.1) | — | — | 2 |
| `camera_setup_view(camera_id)` | нет | `NotFound` | 404 | — | 2 |
| `job_retry(job_id, role)` | jobs | `RoleRequired`, `Forbidden`, `NotFound`, `Conflict(job_not_failed)` | 400, 403, 404, 409 | — | 3 |
| `recover_jobs()` | jobs: `running` → `queued` | нет | — | — | 3 |
| `backend_check(force)` | нет (кэш в памяти) | нет: исход в `BackendStatus.state` | — | `doctor` exit 4 | 3 |
| `models_view()` | нет | нет | — | — | 3 |
| `system_view()` | нет | нет | — | — | 3 |
| `video_tracks(video_id, from_ms, to_ms)` | нет | `NotFound`, `Conflict(video_not_ready)`, `ValidationFailed` (окно) | 404, 409, 422 | — | 4 |
| `video_analysis(video_id)` | нет | `NotFound`, `Conflict(video_not_ready)` | 404, 409 | — | 5 |
| `video_recompute(video_id, role)` | jobs | `RoleRequired`, `Forbidden`, `NotFound`, `Conflict(video_not_ready, artifacts_missing)` | 400, 403, 404, 409 | — | 5 |
| `evidence_file(evidence_id)` | нет | `NotFound` | 404 | — | 5 |
| `broadcast_get(camera_id)` | нет | `NotFound` (камера) | 404 | — | 6 |
| `broadcast_start(camera_id, data, role)` | broadcasts: прежний `playing` → `stopped`, новая строка | `RoleRequired`, `Forbidden`, `NotFound`, `Conflict(no_ready_video, video_not_ready)` | 400, 403, 404, 409 | — | 6 |
| `broadcast_stop(camera_id, role)` | broadcasts | `RoleRequired`, `Forbidden`, `NotFound` | 400, 403, 404 | — | 6 |
| `broadcast_tick()` | broadcasts (cycle, position_ms, status), events, event_actions | нет | — | — | 6 |
| `camera_states()` | нет | нет | — | — | 6 |
| `operator_dashboard_view()` | нет | нет | — | — | 6 |
| `operator_feed()` | нет | нет | — | — | 6 |
| `sector_view(sector_id)` | нет | `NotFound` | 404 | — | 6 |
| `camera_live_view(camera_id)` | нет | `NotFound` | 404 | — | 6 |
| `camera_preview(camera_id)` | нет | `NotFound` (камера или нет видео) | 404 | — | 6 |
| `event_detail(event_id, role)` | нет | `NotFound` | 404 | — | 7 |
| `event_action(event_id, data, role, actor)` | events, event_actions | `RoleRequired`, `Forbidden`, `NotFound`, `Conflict(invalid_transition)`, `ValidationFailed` (комментарий, actor) | 400, 403, 404, 409, 422 | — | 7 |
| `escalation_tick()` | events, event_actions | нет | — | — | 7 |
| `master_inbox_view()` | нет | нет | — | — | 8 |
| `shift_summary_view(at)` | нет | нет | — | — | 8 |
| `calibration_get(camera_id)` | нет | `NotFound` (камера) | 404 | — | 9 |
| `calibration_set(camera_id, data, role)` | calibrations | `RoleRequired`, `Forbidden`, `NotFound`, `ValidationFailed` | 400, 403, 404, 422 | — | 9 |
| `calibration_delete(camera_id, role)` | calibrations | `RoleRequired`, `Forbidden`, `NotFound` | 400, 403, 404 | — | 9 |
| `zones_list(camera_id)` | нет | `NotFound` | 404 | — | 9 |
| `zone_create(camera_id, data, role)` | zones | `RoleRequired`, `Forbidden`, `NotFound`, `ValidationFailed` | 400, 403, 404, 422 | — | 9 |
| `zone_update(zone_id, data, role)` | zones | те же | 400, 403, 404, 422 | — | 9 |
| `zone_delete(zone_id, role)` | zones.deleted_at | `RoleRequired`, `Forbidden`, `NotFound` | 400, 403, 404 | — | 9 |
| `camera_rules(camera_id)` | нет | `NotFound` | 404 | — | 9 |
| `camera_rule_set(camera_id, scenario, data, role)` | camera_rules | `RoleRequired`, `Forbidden`, `NotFound` (камера, сценарий), `ValidationFailed` (параметр) | 400, 403, 404, 422 | — | 9 |
| `rules_screen_view()` | нет | нет | — | — | 9 |
| `events_list(f)` | нет | `ValidationFailed` (фильтр) | 422 | — | 12 |
| `events_export_csv(f)` | нет | `ValidationFailed` | 422 | — | 12 |
| `journal_facets()` | нет | нет | — | — | 12 |
| `ohs_stats_view(...)` | нет | `ValidationFailed` (date_from > date_to) | 422 | — | 13 |
| `management_view(weeks, include_demo)` | нет | `ValidationFailed` (weeks вне 1..52) | 422 | — | 13 |
| `eval_run(labels, out_dir)` | artifacts (кэш инференса), файлы `eval/` | `NotFound` (labels, видео), `ValidationFailed` (схема labels); бэкенд недоступен → `InferenceError` | — | exit 3, 2, 4 | 14 |
| `deliveries_flush()` | deliveries | нет: ошибка канала → строка `failed` | — | — | 15 |

Права ролей. Пишущая функция с `role=None` бросает `RoleRequired`, с ролью вне строки — `Forbidden`. Чтение доступно без роли.

| Функция | Роли |
| --- | --- |
| `sector_create`, `sector_update`, `sector_delete`, `camera_create`, `camera_update`, `camera_delete`, `video_upload`, `job_retry`, `broadcast_start`, `broadcast_stop`, `calibration_set`, `calibration_delete` | admin |
| `video_recompute`, `zone_create`, `zone_update`, `zone_delete`, `camera_rule_set` | admin, ohs |
| `event_action` с `view`, `confirm`, `false_alarm`, `send_to_master` | operator |
| `event_action` с `accept`, `resolve` | master |

Ситуации на границах:

| Ситуация | Фасад | Код: REST | Код: CLI |
| --- | --- | --- | --- |
| неизвестный id | `NotFound` | 404 | exit 3 |
| нет `X-Role` у пишущего вызова | `RoleRequired` | 400 | — |
| роль без права | `Forbidden` | 403 | — |
| недопустимый переход статуса | `Conflict(invalid_transition)` | 409 | — |
| маршрут слайса, который ещё не сделан | `NotImplementedError` | 501 `not_implemented` | — |
| LinQ недоступен (туннель, VPN, логин) | задача `retry_wait`, `error_code=linq_unavailable`; после `jobs.max_attempts` — `failed`; `BackendStatus.state=unreachable` | 200 со статусом задачи | `doctor` exit 4 |
| ответ LinQ неожиданного вида (JSONL не парсится, число строк не равно `frames_processed`, `.progress` не JSON, Jupyter отдал HTML вместо API) | задача `failed`, `error_code=bad_output`, в логе строка `linq: bad_output <что>`; `backend_check` → `state=bad_answer` | 200 со статусом задачи | `doctor` exit 4 |
| нет программы TPU или хвоста ONNX | `backend_check` → `models_missing`; задача `failed` (`model_missing`) | 200 | `doctor` exit 4 |
| pose-модель упала, детектор отработал | анализ идёт без ключевых точек, `Analysis.pose_used=false`, методы `bbox` | 200 | — |
| webhook ответил не 2xx или таймаут | строка deliveries `failed`, событие не меняется | — | — |
| WS-клиент не успевает читать (`hub.CLIENT_QUEUE`) | клиент отключается кодом 1013, фронт переподключается и перечитывает экран по REST | — | — |

Функции чтения экранов (маршруты фронта — раздел 8.14):

| Экран | Функция | Модель |
| --- | --- | --- |
| шапка всех экранов | `meta()` | `Meta` |
| `/operator` | `operator_dashboard_view()` | `OperatorDashboard` |
| `/operator/sectors/:sectorId` | `sector_view(sector_id)` | `SectorView` |
| `/operator/cameras/:cameraId` | `camera_live_view(camera_id)` | `CameraLiveView` |
| `/events/:eventId`, `/master/events/:eventId` | `event_detail(event_id, role)` | `EventDetail` |
| `/master` | `master_inbox_view()` | `MasterInbox` |
| `/master/shift` | `shift_summary_view(at)` | `ShiftSummary` |
| `/ohs/journal` | `events_list(f)`, `journal_facets()` | `EventPage`, `JournalFacets` |
| `/ohs/rules` | `rules_screen_view()` | `RulesScreenView` |
| `/ohs/stats` | `ohs_stats_view(...)` | `OhsStats` |
| `/management` | `management_view(...)` | `ManagementStats` |
| `/admin/cameras` | `cameras_admin_view()` | `CamerasAdminView` |
| `/admin/cameras/:cameraId` | `camera_setup_view(camera_id)`; вкладки зовут `video_analysis`, `video_tracks` | `CameraSetupView` |
| `/admin/system` | `system_view()` | `SystemView` |

### 6.3 CLI: `src/safewatch/cli.py`

Точка входа `safewatch = "safewatch.cli:main"`, `python -m safewatch` то же. Парсер — `argparse`, подкоманды через `add_parser`.

| Команда | Фасад | Выход | Коды | Слайс |
| --- | --- | --- | --- | --- |
| `safewatch serve [--host H] [--port P] [--seed]` | `migrate`, `recover_jobs` (с S3), `seed_demo` при `--seed` и пустой базе; uvicorn на ProactorEventLoop, пишет `server.pid` | лог в stdout | 0 после остановки, 2 порт занят | 0 |
| `safewatch stop` | — | `stopped <pid>` или `not running` | 0; 1 pid в файле принадлежит другому процессу (файл удаляется, процесс не трогается) | 0 |
| `safewatch seed [--videos DIR]` | `seed_demo` | JSON `SeedReport` | 0; 3 нет папки | 0 |
| `safewatch doctor` | `backend_check(force=True)` (с S3), проверки 8.17 | таблица проверок, ключи только «есть/нет» | 0 всё в порядке; 4 есть проблема | 0 |
| `safewatch contract [--check]` | — | пишет или сверяет `contract/openapi.json` и `contract/ws.schema.json` | 0; 1 расхождение при `--check` | 0 |
| `safewatch import FILE --camera ID` | `video_import` | JSON `UploadResult` | 0; 2 формат или размер; 3 нет файла или камеры | 2 |
| `safewatch eval LABELS [--out DIR]` | `eval_run` | путь к отчёту и таблица метрик | 0; 2 схема; 3 нет файла; 4 бэкенд недоступен | 14 |

### 6.4 REST: `src/safewatch/api.py`

`router = APIRouter()`, приложение `create_app(settings: Settings) -> FastAPI`. Все обработчики `async def`. Заголовки: `X-Role` (значение `Role`, неизвестное → 400 `role_required`), `X-Actor` (имя, UTF-8 в percent-encoding, до `ACTOR_MAX` символов после декодирования). Тело ошибки — `ApiError`. Маршрут `/api/events/export.csv` объявлен раньше `/api/events/{event_id}`. Если существует `server.static_dir`, приложение раздаёт его на `/` с откатом на `index.html` для маршрутов фронта. Слайс 0 объявляет все маршруты; маршрут незакрытого слайса отвечает 501.

| Искомая строка декоратора | Фасад | Вход | Ответ | Ошибки | Слайс |
| --- | --- | --- | --- | --- | --- |
| `@router.get("/api/health")` | `health` | — | `Health` | — | 0 |
| `@router.websocket("/ws")` | `hub` | query `role` | поток `WsMessage` | close 4400 при неизвестной роли | 0 |
| `@router.get("/api/meta")` | `meta` | — | `Meta` | — | 1 |
| `@router.get("/api/admin/cameras")` | `cameras_admin_view` | — | `CamerasAdminView` | — | 1 |
| `@router.get("/api/sectors")` | `sectors_list` | — | `list[Sector]` | — | 1 |
| `@router.post("/api/sectors", status_code=201)` | `sector_create` | `SectorIn` | `Sector` | 400, 403, 409, 422 | 1 |
| `@router.put("/api/sectors/{sector_id}")` | `sector_update` | `SectorIn` | `Sector` | 400, 403, 404, 409, 422 | 1 |
| `@router.delete("/api/sectors/{sector_id}", status_code=204)` | `sector_delete` | — | — | 400, 403, 404, 409 | 1 |
| `@router.get("/api/cameras")` | `cameras_list` | query `sector_id` | `list[Camera]` | 404 | 1 |
| `@router.post("/api/cameras", status_code=201)` | `camera_create` | `CameraIn` | `Camera` | 400, 403, 422 | 1 |
| `@router.get("/api/cameras/{camera_id}")` | `camera_get` | — | `Camera` | 404 | 1 |
| `@router.patch("/api/cameras/{camera_id}")` | `camera_update` | `CameraPatch` | `Camera` | 400, 403, 404, 422 | 1 |
| `@router.delete("/api/cameras/{camera_id}", status_code=204)` | `camera_delete` | — | — | 400, 403, 404 | 1 |
| `@router.post("/api/cameras/{camera_id}/videos", status_code=201)` | `video_upload` | multipart, поле `file` | `UploadResult` | 400, 403, 404, 413, 415 | 2 |
| `@router.get("/api/cameras/{camera_id}/videos")` | `videos_list` | — | `list[Video]` | 404 | 2 |
| `@router.get("/api/videos/{video_id}")` | `video_get` | — | `Video` | 404 | 2 |
| `@router.get("/api/videos/{video_id}/file")` | `video_file` | заголовок `Range` | файл, 200 или 206 | 404 | 2 |
| `@router.get("/api/jobs")` | `jobs_list` | query `status`, `limit` | `list[Job]` | 422 | 2 |
| `@router.get("/api/jobs/{job_id}")` | `job_get` | — | `Job` | 404 | 2 |
| `@router.get("/api/admin/cameras/{camera_id}")` | `camera_setup_view` | — | `CameraSetupView` | 404 | 2 |
| `@router.post("/api/jobs/{job_id}/retry")` | `job_retry` | — | `Job` | 400, 403, 404, 409 | 3 |
| `@router.get("/api/system")` | `system_view` | — | `SystemView` | — | 3 |
| `@router.post("/api/system/backend-check")` | `backend_check(force=True)` | — | `BackendStatus` | — | 3 |
| `@router.get("/api/models")` | `models_view` | — | `ModelsView` | — | 3 |
| `@router.get("/api/videos/{video_id}/tracks")` | `video_tracks` | query `from_ms`, `to_ms` | `TracksWindow` | 404, 409, 422 | 4 |
| `@router.get("/api/videos/{video_id}/analysis")` | `video_analysis` | — | `Analysis` | 404, 409 | 5 |
| `@router.post("/api/videos/{video_id}/recompute", status_code=202)` | `video_recompute` | — | `Job` | 400, 403, 404, 409 | 5 |
| `@router.get("/api/evidence/{evidence_id}/image")` | `evidence_file` | — | `image/jpeg` | 404 | 5 |
| `@router.get("/api/cameras/{camera_id}/broadcast")` | `broadcast_get` | — | `Broadcast` или `null` | 404 | 6 |
| `@router.post("/api/cameras/{camera_id}/broadcast", status_code=201)` | `broadcast_start` | `BroadcastIn` | `Broadcast` | 400, 403, 404, 409 | 6 |
| `@router.delete("/api/cameras/{camera_id}/broadcast", status_code=204)` | `broadcast_stop` | — | — | 400, 403, 404 | 6 |
| `@router.get("/api/operator/dashboard")` | `operator_dashboard_view` | — | `OperatorDashboard` | — | 6 |
| `@router.get("/api/operator/feed")` | `operator_feed` | — | `list[EventSummary]` | — | 6 |
| `@router.get("/api/sectors/{sector_id}/view")` | `sector_view` | — | `SectorView` | 404 | 6 |
| `@router.get("/api/cameras/{camera_id}/view")` | `camera_live_view` | — | `CameraLiveView` | 404 | 6 |
| `@router.get("/api/cameras/{camera_id}/preview")` | `camera_preview` | — | `image/jpeg` | 404 | 6 |
| `@router.get("/api/events/{event_id}")` | `event_detail` | заголовок `X-Role` | `EventDetail` | 404 | 7 |
| `@router.post("/api/events/{event_id}/actions")` | `event_action` | `ActionIn`, `X-Role`, `X-Actor` | `EventDetail` | 400, 403, 404, 409, 422 | 7 |
| `@router.get("/api/master/inbox")` | `master_inbox_view` | — | `MasterInbox` | — | 8 |
| `@router.get("/api/master/shift")` | `shift_summary_view` | query `at` | `ShiftSummary` | 422 | 8 |
| `@router.get("/api/cameras/{camera_id}/calibration")` | `calibration_get` | — | `Calibration` или `null` | 404 | 9 |
| `@router.put("/api/cameras/{camera_id}/calibration")` | `calibration_set` | `CalibrationIn` | `Calibration` | 400, 403, 404, 422 | 9 |
| `@router.delete("/api/cameras/{camera_id}/calibration", status_code=204)` | `calibration_delete` | — | — | 400, 403, 404 | 9 |
| `@router.get("/api/cameras/{camera_id}/zones")` | `zones_list` | — | `list[Zone]` | 404 | 9 |
| `@router.post("/api/cameras/{camera_id}/zones", status_code=201)` | `zone_create` | `ZoneIn` | `Zone` | 400, 403, 404, 422 | 9 |
| `@router.patch("/api/zones/{zone_id}")` | `zone_update` | `ZonePatch` | `Zone` | 400, 403, 404, 422 | 9 |
| `@router.delete("/api/zones/{zone_id}", status_code=204)` | `zone_delete` | — | — | 400, 403, 404 | 9 |
| `@router.get("/api/cameras/{camera_id}/rules")` | `camera_rules` | — | `list[CameraRule]` | 404 | 9 |
| `@router.put("/api/cameras/{camera_id}/rules/{scenario}")` | `camera_rule_set` | `CameraRuleIn` | `CameraRule` | 400, 403, 404, 422 | 9 |
| `@router.get("/api/ohs/rules")` | `rules_screen_view` | — | `RulesScreenView` | — | 9 |
| `@router.get("/api/events")` | `events_list` | query: поля `EventFilter` | `EventPage` | 422 | 12 |
| `@router.get("/api/events/export.csv")` | `events_export_csv` | query: поля `EventFilter` | `text/csv; charset=utf-8` | 422 | 12 |
| `@router.get("/api/journal/facets")` | `journal_facets` | — | `JournalFacets` | — | 12 |
| `@router.get("/api/stats/ohs")` | `ohs_stats_view` | query `date_from`, `date_to`, `sector_id`, `camera_id`, `include_demo` | `OhsStats` | 422 | 13 |
| `@router.get("/api/stats/management")` | `management_view` | query `weeks`, `include_demo` | `ManagementStats` | 422 | 13 |

`contract/openapi.json` = `create_app(settings).openapi()` с `info.version = CONTRACT_VERSION`, JSON с отступом 2 и сортировкой ключей. `contract/ws.schema.json` = `TypeAdapter(WsMessage).json_schema()`. Изменения после заморозки только добавляют поля, маршруты и типы сообщений; удаление и переименование — по договорённости с фронтендером Егором, с поднятием `CONTRACT_VERSION` и строкой `GAP`.

### 6.5 WebSocket: `/ws?role=<Role>`

Сообщение — `WsMessage` в JSON. Сервер шлёт `hello` сразу после подключения. Клиент ничего не шлёт. `audience` пусто — сообщение получают все подключения; иначе только роли из списка.

| Тип | Публикует (модуль, слайс) | Нагрузка | Аудитория |
| --- | --- | --- | --- |
| `hello` | `api.py`, 0 | `WsHello` | подключившийся |
| `job.progress` | `services.run_next_job`, 2 | `Job` | все |
| `backend.status` | `services.backend_check`, 3 | `BackendStatus` | все |
| `event.created` | `services.broadcast_tick`, 6 | `EventSummary` | все |
| `event.updated` | `services.broadcast_tick` (6), `event_action`, `escalation_tick` (7), `run_next_job` (9, supersede) | `EventSummary` | все |
| `event.escalated` | `services.broadcast_tick`, 6 | `EventSummary` | все |
| `notification` | `services.broadcast_tick` (6), `event_action`, `escalation_tick` (7, 8) | `Notification` | `Notification.audience` |
| `camera.state` | `services.broadcast_tick` при изменении, 6 | `CameraState` | все |
| `sector.state` | `services.broadcast_tick` при изменении, 6 | `SectorState` | все |
| `broadcast.state` | `services.broadcast_start`, `broadcast_stop`, `broadcast_tick` при смене цикла и окончании, 6 | `Broadcast` | все |

### 6.6 Конфиг и константы

Ключи `.env` (`.env.example` хранит их с пустыми значениями; остальные ключи `LINQ_*` в файле нужны `tools/linq/`, приложение их не читает):

| Ключ | По умолчанию | Поле `Settings` | Читает |
| --- | --- | --- | --- |
| `INFERENCE_BACKEND` | `linq` | `inference_backend: BackendName` | `inference.make_backend`, `meta` |
| `SAFEWATCH_FAKE` | `0` | `fake: bool` | `inference.make_backend`, `meta` |
| `LINQ_JUPYTER_URL` | пусто | `linq_jupyter_url: str` | `JupyterShell`, `doctor` |
| `LINQ_JUPYTER_USER` | пусто | `linq_jupyter_user: str` | `JupyterShell`, логин в `linq.programs_dir` (в нижнем регистре) |
| `LINQ_JUPYTER_PASSWORD` | пусто | `linq_jupyter_password: str` | `JupyterShell` |
| `LINQ_JUPYTER_TOKEN` | пусто | `linq_jupyter_token: str` | `JupyterShell` |

Фронт: `frontend/.env.example` — `VITE_API_BASE=` (пусто: тот же origin), `VITE_WS_URL=` (пусто: `ws(s)://<host>/ws`); `frontend/.env.mock` — `VITE_API_BASE=http://127.0.0.1:4010`, `VITE_WS_URL=ws://127.0.0.1:4011/ws`.

`config/default.yaml` целиком. `config.py` описывает каждую секцию моделью pydantic с теми же именами полей и `extra="forbid"`: опечатка в ключе роняет запуск. `config/user.yaml` владельца переопределяет любой ключ; тесты его не читают.

```yaml
# Defaults (tech.md 6.6). config/user.yaml overrides any key; tests never read it.
product_name: SafeWatch
data_dir: data/app
timezone: Europe/Moscow

server:
  host: 127.0.0.1
  port: 8000
  static_dir: frontend/dist

upload:
  max_mb: 2048
  extensions: [".mp4", ".avi", ".mov", ".mkv"]

pipeline:
  target_analysis_fps: 12
  min_analysis_fps: 5
  detector: det-yolov8n@640-ap9999
  pose: pose-yolov8n@640-ap9999
  extra: []

class_conf:
  car: 0.35
  bus: 0.35
  truck: 0.35
  train: 0.35
  cell phone: 0.3
  fire: 0.35
  smoke: 0.3
  cigarette: 0.25
  no_harness: 0.35
  suspended_load: 0.35

tracker:
  high_thresh: 0.5
  low_thresh: 0.1
  new_track_thresh: 0.6
  min_iou: 0.2
  max_lost_s: 1.0
  min_hits: 2

pose:
  match_iou: 0.5
  kpt_conf: 0.3

features:
  ref_window_s: 2.0
  upright_hw: 1.2
  lying_wh: 1.3
  upright_torso_deg: 30
  lying_torso_deg: 60
  speed_window_s: 1.0
  speed_min_samples: 4
  speed_max_gap_s: 0.5
  still_motion_bh: 0.15
  still_after_s: 3.0
  min_person_px: 40

episodes:
  candidate_gap_s: 0.5
  end_after_s: 2.0
  lost_timeout_s: 5.0
  merge_dist_bh: 1.0

scenarios:
  running:
    speed_bh_s: 1.5
    speed_m_s: 2.5
    hold_s: 1.0
    red_hold_s: 0.5
    near_vehicle_bh: 3.0
    near_vehicle_m: 3.0
  proximity:
    yellow_bh: 2.0
    red_bh: 0.5
    yellow_m: 3.0
    red_m: 1.0
    moving_vh_s: 0.2
    moving_m_s: 0.5
    hold_s: 0.5
    red_hold_s: 0.3
    driver_ioa: 0.6
  phone:
    hold_s: 10.0
    danger_hold_s: 3.0
    min_person_px: 120
    upper_frac: 0.6
    wrist_dist_bh: 0.25
  fall:
    transition_s: 2.0
    confirm_s: 2.0
    still_s: 10.0
    allowed_still_s: 60.0
  fence_crossing:
    max_gap_s: 1.0
  restricted_under:
    under_hold_s: 0.5
  fire_smoking:
    fire_hold_s: 1.0
    smoking_hold_s: 3.0
  no_harness:
    harness_hold_s: 3.0
  suspended_load:
    load_hold_s: 0.5
  load_carrying: {}

zone_kinds:
  - id: danger
    title: Опасная зона / механизм
    color: "#FF453A"
    geometry: polygon
    description: Станок, пресс, конвейер, зона работы техники. Вход человека — красное событие.
  - id: fence
    title: Ограждение
    color: "#FF9F0A"
    geometry: line
    description: Линия, которую нельзя пересекать.
  - id: under_load
    title: Под конвейером / грузом
    color: "#BF5AF2"
    geometry: polygon
    description: Проход под конвейером или зона подъёма груза.
  - id: fire_allowed
    title: Огонь разрешён
    color: "#FF6B00"
    geometry: polygon
    description: Печь, сварочный пост. Огонь здесь не нарушение.
  - id: lying_allowed
    title: Лежать допустимо
    color: "#30D158"
    geometry: polygon
    description: Ремонт под станком или вагоном. Тревога только при долгой неподвижности.
  - id: rest
    title: Зона отдыха
    color: "#64D2FF"
    geometry: polygon
    description: Места отдыха. В baseline правила её не используют.
  - id: height
    title: Работа на высоте
    color: "#FFD60A"
    geometry: polygon
    description: Площадки и лестницы, где нужна страховочная привязь.
  - id: vehicle_path
    title: Пути транспорта
    color: "#98989D"
    geometry: polygon
    description: Проезды погрузчиков и машин.

escalation:
  enabled: true
  timeout_s: 45
  tick_ms: 500

broadcast:
  tick_ms: 250
  loop_default: true
  autostart: true

feed:
  limit: 100
  recent_closed_min: 30

observability:
  stale_after_ms: 2000
  sample_s: 1.0
  dark_mean: 35
  obstructed_std: 12
  min_duration_s: 3.0

evidence:
  jpeg_quality: 85
  max_width: 1280

preview:
  cache_s: 2.0
  max_width: 640

hud:
  window_max_ms: 10000

jobs:
  max_attempts: 3
  retry_backoff_s: [30, 120]
  idle_poll_ms: 500
  list_max: 200

linq:
  tools_dir: tools/linq
  remote_dir: baseline
  file_prefix: baseline_
  programs_dir: /auto/cache/{login}
  inflight: 4
  poll_interval_s: 3.0
  job_timeout_s: 1800
  call_timeout_s: 60
  check_cache_s: 30

local:
  threads: 2

shifts:
  - id: day
    title: Дневная смена
    start: "08:00"
    end: "20:00"
  - id: night
    title: Ночная смена
    start: "20:00"
    end: "08:00"

stats:
  default_days: 30
  weeks_default: 8
  trend_weeks: 4

journal:
  page_max: 200
  export_max_rows: 10000

master:
  recent_resolved: 20

delivery:
  webhooks: []   # [{name: lamp-1, url: "http://10.0.0.5/alarm", levels: [red], timeout_s: 3}]

eval:
  deadline_s: 5.0
```

`config/models.yaml` — реестр моделей. Новая модель = новая запись + ссылка `id@version` в `pipeline.detector`, `pipeline.pose` или `pipeline.extra` (в `config/user.yaml`), без правки кода. Модель из `pipeline.extra` — детектор с собственными классами (огонь, сигарета, погрузчик, привязь); её имена классов включают плагины (8.3).

```yaml
models:
  - id: det-yolov8n
    version: 640-ap9999
    task: detect
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: person, 2: car, 5: bus, 6: train, 7: truck, 67: cell phone}
    linq_program: mosprom_det640_cut_ap9999_b1_o1_h1m.tpu
    linq_tail: models/linq/det640_cut_ap9999/det640_cut_ap9999_tail.onnx
    local_onnx: models/yolov8n_640_op13.onnx
  - id: det-yolov8n
    version: 960-ap9999
    task: detect
    input_size: 960
    conf: 0.1
    iou: 0.45
    classes: {0: person, 2: car, 5: bus, 6: train, 7: truck, 67: cell phone}
    linq_program: mosprom_det960_cut_ap9999_b1_o1_h1m.tpu
    linq_tail: models/linq/det960_cut_ap9999/det960_cut_ap9999_tail.onnx
    local_onnx: models/yolov8n_960_op13.onnx
  - id: pose-yolov8n
    version: 640-ap9999
    task: pose
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: person}
    linq_program: mosprom_pose640_cut_ap9999_b1_o1_h1m.tpu
    linq_tail: models/linq/pose640_cut_ap9999/pose640_cut_ap9999_tail.onnx
    local_onnx: models/yolov8n-pose_640_op13.onnx
```

Именованные константы в коде (числа, влияющие на поведение, вне yaml):

| Константа | Значение | Единица | Читает | Поведение |
| --- | --- | --- | --- | --- |
| `api.CONTRACT_VERSION = "1.0.0"` | 1.0.0 | версия | `api`, `openapi.json`, `hello` | 6.4 |
| `media.BROWSER_CODECS = ("avc1", "h264", "vp09", "av01")` | — | FourCC | `media.probe_video` | 8.1 |
| `inference.artifacts.CACHE_SCHEMA = "jsonl-v1"` | — | — | `cache_key` | 5.3 |
| `hub.CLIENT_QUEUE = 1000` | 1000 | сообщений | `hub` | 6.2 |
| `services.NAME_MAX = 80` | 80 | символов | валидация | 9 |
| `services.DESCRIPTION_MAX = 300` | 300 | символов | валидация | 9 |
| `services.COMMENT_MAX = 500` | 500 | символов | валидация | 9 |
| `services.ACTOR_MAX = 60` | 60 | символов | валидация | 9 |
| `services.ZONE_NAME_MAX = 60` | 60 | символов | валидация | 9 |
| `services.ZONE_POINTS_MAX = 32` | 32 | точек | валидация | 9 |
| `services.QUERY_MAX = 100` | 100 | символов | валидация | 9 |
| `services.PRIORITY = {"red_open": 3, "yellow_new": 2, "open": 1, "closed": 0}` | — | ранг | лента | 8.8 |
| `analysis.geometry.MIN_CAL_POINTS = 4` | 4 | точек | калибровка | 8.11 |
| `analysis.geometry.MAX_CAL_POINTS = 8` | 8 | точек | калибровка | 8.11 |
| `analysis.geometry.MIN_AREA = 1e-4` | 0.0001 | доля кадра² | вырожденные точки и полигоны | 9 |
| `seed.SEED = 2026` | 2026 | — | сид | 8.16 |
| `seed.DAYS = 42` | 42 | дней | сид | 8.16 |
| `seed.EVENTS = 240` | 240 | событий | сид | 8.16 |

### 6.7 Трассировка

Каждый элемент разделов 5–6 — строка таблицы. Строка без слайса — ошибка генерации. Таблицу читает `scripts/contract_check.py` (раздел 11): имена столбцов не менять, одна строка — один файл, `|` в ячейке пишется `\|`. «Слайс» — шаг, в котором элемент начинает работать и получает тест; объявления схемы, типов, маршрутов и ключей конфига появляются уже в слайсе 0. Тест вида `frontend/...::имя` — имя теста vitest в snake_case.

| Элемент | Слайс | Потребитель | Файл | Искомая строка | Тест |
| --- | --- | --- | --- | --- | --- |
| таблица `sectors` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE sectors (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `cameras` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE cameras (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `videos` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE videos (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `jobs` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE jobs (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `artifacts` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE artifacts (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `analyses` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE analyses (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `episodes` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE episodes (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `evidence` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE evidence (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `broadcasts` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE broadcasts (` | `tests/test_db.py::test_migrate_creates_tables` |
| индекс `broadcasts_one_playing` | 0 | `services.broadcast_start` | `src/safewatch/migrations/0001_init.sql` | `CREATE UNIQUE INDEX broadcasts_one_playing` | `tests/test_db.py::test_one_playing_broadcast_per_camera` |
| таблица `zones` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE zones (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `calibrations` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE calibrations (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `camera_rules` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE camera_rules (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `events` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE events (` | `tests/test_db.py::test_migrate_creates_tables` |
| таблица `event_actions` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE event_actions (` | `tests/test_db.py::test_migrate_creates_tables` |
| триггер `event_actions_no_update` | 0 | журнал действий | `src/safewatch/migrations/0001_init.sql` | `CREATE TRIGGER event_actions_no_update` | `tests/test_db.py::test_event_actions_are_append_only` |
| триггер `event_actions_no_delete` | 0 | журнал действий | `src/safewatch/migrations/0001_init.sql` | `CREATE TRIGGER event_actions_no_delete` | `tests/test_db.py::test_event_actions_are_append_only` |
| таблица `deliveries` | 0 | `store` | `src/safewatch/migrations/0001_init.sql` | `CREATE TABLE deliveries (` | `tests/test_db.py::test_migrate_creates_tables` |
| `db.connect` | 0 | `store`, `conftest` | `src/safewatch/db.py` | `def connect(` | `tests/test_db.py::test_connect_registers_casefold` |
| `db.migrate` | 0 | `cli serve`, `conftest` | `src/safewatch/db.py` | `def migrate(` | `tests/test_db.py::test_second_migrate_changes_nothing` |
| тип `Level` | 0 | все слои | `src/safewatch/types.py` | `Level = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Role` | 0 | `services`, `api` | `src/safewatch/types.py` | `Role = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ActorRole` | 0 | журнал действий | `src/safewatch/types.py` | `ActorRole = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventStatus` | 0 | события | `src/safewatch/types.py` | `EventStatus = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Verdict` | 0 | события | `src/safewatch/types.py` | `Verdict = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `HumanAction` | 0 | `event_action` | `src/safewatch/types.py` | `HumanAction = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `LogAction` | 0 | журнал действий | `src/safewatch/types.py` | `LogAction = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventMode` | 0 | `EventSummary` | `src/safewatch/types.py` | `EventMode = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraStateKind` | 0 | состояния | `src/safewatch/types.py` | `CameraStateKind = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `NoObservationReason` | 0 | наблюдаемость | `src/safewatch/types.py` | `NoObservationReason = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `VideoStatus` | 0 | видео | `src/safewatch/types.py` | `VideoStatus = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `JobKind` | 0 | задачи | `src/safewatch/types.py` | `JobKind = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `JobStatus` | 0 | задачи | `src/safewatch/types.py` | `JobStatus = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `JobStage` | 0 | задачи | `src/safewatch/types.py` | `JobStage = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `JobErrorCode` | 0 | задачи | `src/safewatch/types.py` | `JobErrorCode = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Fault` | 0 | фейк, бэкенды | `src/safewatch/types.py` | `Fault = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `BackendName` | 0 | бэкенды | `src/safewatch/types.py` | `BackendName = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `BackendState` | 0 | `backend_check` | `src/safewatch/types.py` | `BackendState = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ModelTask` | 0 | реестр | `src/safewatch/types.py` | `ModelTask = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ObsState` | 0 | плагины, эпизоды | `src/safewatch/types.py` | `ObsState = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EndReason` | 0 | эпизоды | `src/safewatch/types.py` | `EndReason = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ScenarioStatus` | 0 | плагины | `src/safewatch/types.py` | `ScenarioStatus = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `BroadcastStatus` | 0 | эфир | `src/safewatch/types.py` | `BroadcastStatus = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ZoneGeometry` | 0 | зоны | `src/safewatch/types.py` | `ZoneGeometry = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ObjectKind` | 0 | HUD | `src/safewatch/types.py` | `ObjectKind = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Posture` | 0 | признаки | `src/safewatch/types.py` | `Posture = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Sound` | 0 | уведомления | `src/safewatch/types.py` | `Sound = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `DeliveryKind` | 0 | доставка | `src/safewatch/types.py` | `DeliveryKind = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `WsType` | 0 | `hub`, фронт | `src/safewatch/types.py` | `WsType = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Point` | 0 | геометрия | `src/safewatch/types.py` | `Point = tuple[float, float]` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Box` | 0 | детекции | `src/safewatch/types.py` | `Box = tuple[float, float, float, float]` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Keypoint` | 0 | pose | `src/safewatch/types.py` | `Keypoint = tuple[float, float, float]` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ApiError` | 0 | `api` | `src/safewatch/types.py` | `class ApiError(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Health` | 0 | `health` | `src/safewatch/types.py` | `class Health(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `LevelMeta` | 0 | `meta` | `src/safewatch/types.py` | `class LevelMeta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `StatusMeta` | 0 | `meta` | `src/safewatch/types.py` | `class StatusMeta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `RoleMeta` | 0 | `meta` | `src/safewatch/types.py` | `class RoleMeta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ZoneKindMeta` | 0 | `meta` | `src/safewatch/types.py` | `class ZoneKindMeta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ScenarioParam` | 0 | `meta`, правила | `src/safewatch/types.py` | `class ScenarioParam(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ScenarioMeta` | 0 | `meta`, плагины | `src/safewatch/types.py` | `class ScenarioMeta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Meta` | 0 | `meta` | `src/safewatch/types.py` | `class Meta(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `SeedReport` | 0 | `seed_demo` | `src/safewatch/types.py` | `class SeedReport(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Sector` | 0 | секторы | `src/safewatch/types.py` | `class Sector(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `SectorIn` | 0 | секторы | `src/safewatch/types.py` | `class SectorIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Camera` | 0 | камеры | `src/safewatch/types.py` | `class Camera(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraIn` | 0 | камеры | `src/safewatch/types.py` | `class CameraIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraPatch` | 0 | камеры | `src/safewatch/types.py` | `class CameraPatch(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CamerasAdminView` | 0 | экран камер | `src/safewatch/types.py` | `class CamerasAdminView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Video` | 0 | видео | `src/safewatch/types.py` | `class Video(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `InferenceMetrics` | 0 | бэкенды, экран IT | `src/safewatch/types.py` | `class InferenceMetrics(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Job` | 0 | задачи | `src/safewatch/types.py` | `class Job(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `UploadResult` | 0 | загрузка | `src/safewatch/types.py` | `class UploadResult(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ModelSpec` | 0 | реестр | `src/safewatch/types.py` | `class ModelSpec(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ModelsView` | 0 | `models_view` | `src/safewatch/types.py` | `class ModelsView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `BackendStatus` | 0 | `backend_check` | `src/safewatch/types.py` | `class BackendStatus(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `HudTag` | 0 | HUD | `src/safewatch/types.py` | `class HudTag(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `HudObject` | 0 | HUD | `src/safewatch/types.py` | `class HudObject(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `HudFrame` | 0 | HUD | `src/safewatch/types.py` | `class HudFrame(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `TracksWindow` | 0 | `video_tracks` | `src/safewatch/types.py` | `class TracksWindow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ObservabilityGap` | 0 | наблюдаемость | `src/safewatch/types.py` | `class ObservabilityGap(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Evidence` | 0 | доказательства | `src/safewatch/types.py` | `class Evidence(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Episode` | 0 | эпизоды | `src/safewatch/types.py` | `class Episode(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Analysis` | 0 | `video_analysis` | `src/safewatch/types.py` | `class Analysis(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ControlPoint` | 0 | калибровка | `src/safewatch/types.py` | `class ControlPoint(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CalibrationIn` | 0 | калибровка | `src/safewatch/types.py` | `class CalibrationIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Calibration` | 0 | калибровка | `src/safewatch/types.py` | `class Calibration(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Zone` | 0 | зоны | `src/safewatch/types.py` | `class Zone(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ZoneIn` | 0 | зоны | `src/safewatch/types.py` | `class ZoneIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ZonePatch` | 0 | зоны | `src/safewatch/types.py` | `class ZonePatch(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraRule` | 0 | правила | `src/safewatch/types.py` | `class CameraRule(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraRuleIn` | 0 | правила | `src/safewatch/types.py` | `class CameraRuleIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `RulesScreenRow` | 0 | экран правил | `src/safewatch/types.py` | `class RulesScreenRow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `RulesScreenView` | 0 | экран правил | `src/safewatch/types.py` | `class RulesScreenView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Broadcast` | 0 | эфир | `src/safewatch/types.py` | `class Broadcast(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `BroadcastIn` | 0 | эфир | `src/safewatch/types.py` | `class BroadcastIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraState` | 0 | состояния | `src/safewatch/types.py` | `class CameraState(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `SectorState` | 0 | состояния | `src/safewatch/types.py` | `class SectorState(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraSetupView` | 0 | экран настройки камеры | `src/safewatch/types.py` | `class CameraSetupView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventSummary` | 0 | события | `src/safewatch/types.py` | `class EventSummary(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `OperatorDashboard` | 0 | экран оператора | `src/safewatch/types.py` | `class OperatorDashboard(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraTile` | 0 | экран сектора | `src/safewatch/types.py` | `class CameraTile(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `SectorView` | 0 | экран сектора | `src/safewatch/types.py` | `class SectorView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CameraLiveView` | 0 | экран камеры | `src/safewatch/types.py` | `class CameraLiveView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `WhyItem` | 0 | экран события | `src/safewatch/types.py` | `class WhyItem(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventAction` | 0 | журнал действий | `src/safewatch/types.py` | `class EventAction(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Provenance` | 0 | экран события | `src/safewatch/types.py` | `class Provenance(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Delivery` | 0 | доставка | `src/safewatch/types.py` | `class Delivery(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventDetail` | 0 | экран события | `src/safewatch/types.py` | `class EventDetail(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ActionIn` | 0 | `event_action` | `src/safewatch/types.py` | `class ActionIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventFilter` | 0 | журнал | `src/safewatch/types.py` | `class EventFilter(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EventPage` | 0 | журнал | `src/safewatch/types.py` | `class EventPage(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `FacetItem` | 0 | журнал | `src/safewatch/types.py` | `class FacetItem(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `JournalFacets` | 0 | журнал | `src/safewatch/types.py` | `class JournalFacets(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `MasterInbox` | 0 | экран мастера | `src/safewatch/types.py` | `class MasterInbox(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `CountRow` | 0 | статистика | `src/safewatch/types.py` | `class CountRow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ShiftSummary` | 0 | сводка смены | `src/safewatch/types.py` | `class ShiftSummary(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Percentiles` | 0 | статистика | `src/safewatch/types.py` | `class Percentiles(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `DayRow` | 0 | статистика | `src/safewatch/types.py` | `class DayRow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `OhsStats` | 0 | статистика ОТ | `src/safewatch/types.py` | `class OhsStats(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `WeekRow` | 0 | менеджмент | `src/safewatch/types.py` | `class WeekRow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `RateRow` | 0 | менеджмент | `src/safewatch/types.py` | `class RateRow(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `TrendSummary` | 0 | менеджмент | `src/safewatch/types.py` | `class TrendSummary(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ManagementStats` | 0 | менеджмент | `src/safewatch/types.py` | `class ManagementStats(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `LatencyStats` | 0 | экран IT | `src/safewatch/types.py` | `class LatencyStats(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Channel` | 0 | экран IT | `src/safewatch/types.py` | `class Channel(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `SystemView` | 0 | экран IT | `src/safewatch/types.py` | `class SystemView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Notification` | 0 | уведомления | `src/safewatch/types.py` | `class Notification(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `WsHello` | 0 | WebSocket | `src/safewatch/types.py` | `class WsHello(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `WsMessage` | 0 | WebSocket | `src/safewatch/types.py` | `class WsMessage(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Detection` | 0 | артефакты | `src/safewatch/types.py` | `class Detection(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `FrameDetections` | 0 | артефакты | `src/safewatch/types.py` | `class FrameDetections(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `PersonState` | 0 | признаки | `src/safewatch/types.py` | `class PersonState(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `VehicleState` | 0 | признаки | `src/safewatch/types.py` | `class VehicleState(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ObjectState` | 0 | признаки | `src/safewatch/types.py` | `class ObjectState(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `FrameContext` | 0 | плагины | `src/safewatch/types.py` | `class FrameContext(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `Observation` | 0 | плагины, эпизоды | `src/safewatch/types.py` | `class Observation(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `AnalysisConfig` | 0 | анализ | `src/safewatch/types.py` | `class AnalysisConfig(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EpisodeDraft` | 0 | эпизоды | `src/safewatch/types.py` | `class EpisodeDraft(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `AnalysisResult` | 0 | анализ | `src/safewatch/types.py` | `class AnalysisResult(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `ExpectedEvent` | 0 | оценка | `src/safewatch/types.py` | `class ExpectedEvent(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EvalVideo` | 0 | оценка | `src/safewatch/types.py` | `class EvalVideo(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EvalLabels` | 0 | оценка | `src/safewatch/types.py` | `class EvalLabels(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EvalMetrics` | 0 | оценка | `src/safewatch/types.py` | `class EvalMetrics(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| тип `EvalReport` | 0 | оценка | `src/safewatch/types.py` | `class EvalReport(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| протокол `RemoteShell` | 0 | `LinqBackend` | `src/safewatch/types.py` | `class RemoteShell(Protocol):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| протокол `InferenceBackend` | 0 | `services` | `src/safewatch/types.py` | `class InferenceBackend(Protocol):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| протокол `ScenarioPlugin` | 0 | `rules` | `src/safewatch/types.py` | `class ScenarioPlugin(Protocol):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| протокол `DeliveryChannel` | 0 | `delivery` | `src/safewatch/types.py` | `class DeliveryChannel(Protocol):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| `errors.AppError` | 0 | `api` | `src/safewatch/errors.py` | `class AppError(Exception):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.NotFound` | 0 | `services` | `src/safewatch/errors.py` | `class NotFound(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.ValidationFailed` | 0 | `services` | `src/safewatch/errors.py` | `class ValidationFailed(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.Conflict` | 0 | `services` | `src/safewatch/errors.py` | `class Conflict(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.Forbidden` | 0 | `services` | `src/safewatch/errors.py` | `class Forbidden(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.RoleRequired` | 0 | `services`, `api` | `src/safewatch/errors.py` | `class RoleRequired(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.TooLarge` | 0 | `services` | `src/safewatch/errors.py` | `class TooLarge(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.UnsupportedVideo` | 0 | `services` | `src/safewatch/errors.py` | `class UnsupportedVideo(AppError):` | `tests/test_api_skeleton.py::test_app_errors_map_to_status_codes` |
| `errors.InferenceError` | 0 | бэкенды, `run_next_job` | `src/safewatch/errors.py` | `class InferenceError(Exception):` | `tests/test_fakes.py::test_fake_remote_faults` |
| клиент `JupyterShell` | 2 | `LinqBackend` | `src/safewatch/inference/linq.py` | `class JupyterShell:` | `tests/test_linq_backend.py::test_jupyter_shell_maps_errors` |
| бэкенд `LinqBackend` | 2 | `run_next_job` | `src/safewatch/inference/linq.py` | `class LinqBackend:` | `tests/test_linq_backend.py::test_commands_use_baseline_dir_and_registry` |
| бэкенд `LocalBackend` | 3 | `run_next_job` | `src/safewatch/inference/local.py` | `class LocalBackend:` | `tests/test_local_backend.py::test_local_matches_jsonl_format` |
| `inference.make_backend` | 2 | `services` | `src/safewatch/inference/__init__.py` | `def make_backend(` | `tests/test_jobs.py::test_make_backend_by_settings` |
| `artifacts.cache_key` | 2 | `services` | `src/safewatch/inference/artifacts.py` | `def cache_key(` | `tests/test_jobs.py::test_cache_hit_skips_remote` |
| `artifacts.read_jsonl` | 2 | бэкенды, анализ | `src/safewatch/inference/artifacts.py` | `def read_jsonl(` | `tests/test_linq_backend.py::test_jsonl_validation_rows` |
| фейк `FakeRemoteShell` | 0 | `make_backend`, тесты | `src/safewatch/fakes/remote.py` | `class FakeRemoteShell:` | `tests/test_fakes.py::test_fake_remote_faults` |
| `scenes.render` | 0 | фейк, тесты | `src/safewatch/fakes/scenes.py` | `def render(` | `tests/test_fakes.py::test_scenes_are_valid_and_deterministic` |
| канал `WebhookChannel` | 15 | `deliveries_flush` | `src/safewatch/delivery.py` | `class WebhookChannel:` | `tests/test_delivery.py::test_webhook_sent_on_red` |
| `services.health` | 0 | `GET /api/health` | `src/safewatch/services.py` | `def health(` | `tests/test_api_skeleton.py::test_health_ok` |
| `services.seed_demo` | 0 | CLI `seed`, `serve --seed` | `src/safewatch/services.py` | `def seed_demo(` | `tests/test_seed.py::test_seed_creates_demo_world_once` |
| `services.meta` | 1 | `GET /api/meta` | `src/safewatch/services.py` | `def meta(` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
| `services.cameras_admin_view` | 1 | `GET /api/admin/cameras` | `src/safewatch/services.py` | `def cameras_admin_view(` | `tests/test_cameras.py::test_cameras_admin_view_shape` |
| `services.sectors_list` | 1 | `GET /api/sectors` | `src/safewatch/services.py` | `def sectors_list(` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `services.sector_create` | 1 | `POST /api/sectors` | `src/safewatch/services.py` | `def sector_create(` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `services.sector_update` | 1 | `PUT /api/sectors/{sector_id}` | `src/safewatch/services.py` | `def sector_update(` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `services.sector_delete` | 1 | `DELETE /api/sectors/{sector_id}` | `src/safewatch/services.py` | `def sector_delete(` | `tests/test_cameras.py::test_sector_delete_with_cameras_conflicts` |
| `services.cameras_list` | 1 | `GET /api/cameras` | `src/safewatch/services.py` | `def cameras_list(` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `services.camera_get` | 1 | `GET /api/cameras/{camera_id}` | `src/safewatch/services.py` | `def camera_get(` | `tests/test_cameras.py::test_unknown_ids_are_404` |
| `services.camera_create` | 1 | `POST /api/cameras` | `src/safewatch/services.py` | `def camera_create(` | `tests/test_cameras.py::test_camera_rejects_bad_input` |
| `services.camera_update` | 1 | `PATCH /api/cameras/{camera_id}` | `src/safewatch/services.py` | `def camera_update(` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `services.camera_delete` | 1 | `DELETE /api/cameras/{camera_id}` | `src/safewatch/services.py` | `def camera_delete(` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `services.video_upload` | 2 | `POST /api/cameras/{camera_id}/videos` | `src/safewatch/services.py` | `def video_upload(` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| `services.video_import` | 2 | CLI `import`, `seed_demo` | `src/safewatch/services.py` | `def video_import(` | `tests/test_videos.py::test_import_cli` |
| `services.videos_list` | 2 | `GET /api/cameras/{camera_id}/videos` | `src/safewatch/services.py` | `def videos_list(` | `tests/test_videos.py::test_upload_same_file_reuses_video` |
| `services.video_get` | 2 | `GET /api/videos/{video_id}` | `src/safewatch/services.py` | `def video_get(` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| `services.video_file` | 2 | `GET /api/videos/{video_id}/file` | `src/safewatch/services.py` | `def video_file(` | `tests/test_videos.py::test_video_file_supports_range` |
| `services.jobs_list` | 2 | `GET /api/jobs` | `src/safewatch/services.py` | `def jobs_list(` | `tests/test_jobs.py::test_job_runs_detect_then_pose` |
| `services.job_get` | 2 | `GET /api/jobs/{job_id}` | `src/safewatch/services.py` | `def job_get(` | `tests/test_jobs.py::test_job_runs_detect_then_pose` |
| `services.run_next_job` | 2 | `worker` | `src/safewatch/services.py` | `def run_next_job(` | `tests/test_jobs.py::test_job_runs_detect_then_pose` |
| `services.camera_setup_view` | 2 | `GET /api/admin/cameras/{camera_id}` | `src/safewatch/services.py` | `def camera_setup_view(` | `tests/test_videos.py::test_camera_setup_view_shape` |
| `services.job_retry` | 3 | `POST /api/jobs/{job_id}/retry` | `src/safewatch/services.py` | `def job_retry(` | `tests/test_jobs_retry.py::test_manual_retry` |
| `services.recover_jobs` | 3 | CLI `serve` | `src/safewatch/services.py` | `def recover_jobs(` | `tests/test_jobs_retry.py::test_recover_running_jobs` |
| `services.backend_check` | 3 | `POST /api/system/backend-check`, `doctor` | `src/safewatch/services.py` | `def backend_check(` | `tests/test_backend_check.py::test_check_four_states` |
| `services.models_view` | 3 | `GET /api/models` | `src/safewatch/services.py` | `def models_view(` | `tests/test_system.py::test_models_view` |
| `services.system_view` | 3 | `GET /api/system` | `src/safewatch/services.py` | `def system_view(` | `tests/test_system.py::test_system_view_metrics` |
| `services.video_tracks` | 4 | `GET /api/videos/{video_id}/tracks` | `src/safewatch/services.py` | `def video_tracks(` | `tests/test_tracks_api.py::test_tracks_window_bounds` |
| `services.video_analysis` | 5 | `GET /api/videos/{video_id}/analysis` | `src/safewatch/services.py` | `def video_analysis(` | `tests/test_analysis_api.py::test_job_creates_episodes_and_evidence` |
| `services.video_recompute` | 5 | `POST /api/videos/{video_id}/recompute` | `src/safewatch/services.py` | `def video_recompute(` | `tests/test_analysis_api.py::test_recompute_creates_new_version` |
| `services.evidence_file` | 5 | `GET /api/evidence/{evidence_id}/image` | `src/safewatch/services.py` | `def evidence_file(` | `tests/test_analysis_api.py::test_evidence_404_and_sha` |
| `services.broadcast_get` | 6 | `GET /api/cameras/{camera_id}/broadcast` | `src/safewatch/services.py` | `def broadcast_get(` | `tests/test_broadcast.py::test_start_stop_conflicts_and_messages` |
| `services.broadcast_start` | 6 | `POST /api/cameras/{camera_id}/broadcast` | `src/safewatch/services.py` | `def broadcast_start(` | `tests/test_broadcast.py::test_start_stop_conflicts_and_messages` |
| `services.broadcast_stop` | 6 | `DELETE /api/cameras/{camera_id}/broadcast` | `src/safewatch/services.py` | `def broadcast_stop(` | `tests/test_broadcast.py::test_stop_halts_publication` |
| `services.broadcast_tick` | 6 | `worker` | `src/safewatch/services.py` | `def broadcast_tick(` | `tests/test_broadcast.py::test_publish_at_confirm_time_not_before` |
| `services.camera_states` | 6 | экраны оператора, IT | `src/safewatch/services.py` | `def camera_states(` | `tests/test_operator_views.py::test_camera_state_precedence` |
| `services.operator_dashboard_view` | 6 | `GET /api/operator/dashboard` | `src/safewatch/services.py` | `def operator_dashboard_view(` | `tests/test_operator_views.py::test_dashboard_and_sector_view_shape` |
| `services.operator_feed` | 6 | `GET /api/operator/feed` | `src/safewatch/services.py` | `def operator_feed(` | `tests/test_operator_views.py::test_feed_priority_order` |
| `services.sector_view` | 6 | `GET /api/sectors/{sector_id}/view` | `src/safewatch/services.py` | `def sector_view(` | `tests/test_operator_views.py::test_dashboard_and_sector_view_shape` |
| `services.camera_live_view` | 6 | `GET /api/cameras/{camera_id}/view` | `src/safewatch/services.py` | `def camera_live_view(` | `tests/test_operator_views.py::test_camera_live_view_shape` |
| `services.camera_preview` | 6 | `GET /api/cameras/{camera_id}/preview` | `src/safewatch/services.py` | `def camera_preview(` | `tests/test_operator_views.py::test_preview_jpeg` |
| `services.event_detail` | 7 | `GET /api/events/{event_id}` | `src/safewatch/services.py` | `def event_detail(` | `tests/test_event_detail.py::test_detail_why_history_provenance` |
| `services.event_action` | 7 | `POST /api/events/{event_id}/actions` | `src/safewatch/services.py` | `def event_action(` | `tests/test_event_actions.py::test_transition_table` |
| `services.escalation_tick` | 7 | `worker` | `src/safewatch/services.py` | `def escalation_tick(` | `tests/test_escalation.py::test_timeout_boundary_45s` |
| `services.master_inbox_view` | 8 | `GET /api/master/inbox` | `src/safewatch/services.py` | `def master_inbox_view(` | `tests/test_master.py::test_inbox_contains_only_master_statuses` |
| `services.shift_summary_view` | 8 | `GET /api/master/shift` | `src/safewatch/services.py` | `def shift_summary_view(` | `tests/test_shift.py::test_shift_summary_counts` |
| `services.calibration_get` | 9 | `GET /api/cameras/{camera_id}/calibration` | `src/safewatch/services.py` | `def calibration_get(` | `tests/test_calibration.py::test_homography_maps_points` |
| `services.calibration_set` | 9 | `PUT /api/cameras/{camera_id}/calibration` | `src/safewatch/services.py` | `def calibration_set(` | `tests/test_calibration.py::test_calibration_validation` |
| `services.calibration_delete` | 9 | `DELETE /api/cameras/{camera_id}/calibration` | `src/safewatch/services.py` | `def calibration_delete(` | `tests/test_calibration.py::test_homography_maps_points` |
| `services.zones_list` | 9 | `GET /api/cameras/{camera_id}/zones` | `src/safewatch/services.py` | `def zones_list(` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `services.zone_create` | 9 | `POST /api/cameras/{camera_id}/zones` | `src/safewatch/services.py` | `def zone_create(` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `services.zone_update` | 9 | `PATCH /api/zones/{zone_id}` | `src/safewatch/services.py` | `def zone_update(` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `services.zone_delete` | 9 | `DELETE /api/zones/{zone_id}` | `src/safewatch/services.py` | `def zone_delete(` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `services.camera_rules` | 9 | `GET /api/cameras/{camera_id}/rules` | `src/safewatch/services.py` | `def camera_rules(` | `tests/test_camera_rules.py::test_rule_params_override_and_ranges` |
| `services.camera_rule_set` | 9 | `PUT /api/cameras/{camera_id}/rules/{scenario}` | `src/safewatch/services.py` | `def camera_rule_set(` | `tests/test_camera_rules.py::test_rule_params_override_and_ranges` |
| `services.rules_screen_view` | 9 | `GET /api/ohs/rules` | `src/safewatch/services.py` | `def rules_screen_view(` | `tests/test_camera_rules.py::test_rules_screen_view` |
| `services.events_list` | 12 | `GET /api/events` | `src/safewatch/services.py` | `def events_list(` | `tests/test_journal.py::test_filters_each_dimension` |
| `services.events_export_csv` | 12 | `GET /api/events/export.csv` | `src/safewatch/services.py` | `def events_export_csv(` | `tests/test_export.py::test_csv_columns_and_history` |
| `services.journal_facets` | 12 | `GET /api/journal/facets` | `src/safewatch/services.py` | `def journal_facets(` | `tests/test_journal.py::test_facets_lists` |
| `services.ohs_stats_view` | 13 | `GET /api/stats/ohs` | `src/safewatch/services.py` | `def ohs_stats_view(` | `tests/test_stats_ohs.py::test_counts_by_dimensions` |
| `services.management_view` | 13 | `GET /api/stats/management` | `src/safewatch/services.py` | `def management_view(` | `tests/test_stats_management.py::test_weeks_and_top_sectors_per_camera` |
| `services.eval_run` | 14 | CLI `eval` | `src/safewatch/services.py` | `def eval_run(` | `tests/test_eval.py::test_report_files_written` |
| `services.deliveries_flush` | 15 | `worker` | `src/safewatch/services.py` | `def deliveries_flush(` | `tests/test_delivery.py::test_webhook_sent_on_red` |
| CLI `serve` | 0 | владелец, Docker | `src/safewatch/cli.py` | `add_parser("serve"` | `tests/test_cli.py::test_serve_starts_and_stops` |
| CLI `stop` | 0 | владелец, сессии | `src/safewatch/cli.py` | `add_parser("stop"` | `tests/test_cli.py::test_stop_ignores_foreign_pid` |
| CLI `seed` | 0 | владелец | `src/safewatch/cli.py` | `add_parser("seed"` | `tests/test_seed.py::test_seed_cli_reports_counts` |
| CLI `doctor` | 0 | сессии | `src/safewatch/cli.py` | `add_parser("doctor"` | `tests/test_cli.py::test_doctor_fake_mode_ok` |
| CLI `contract` | 0 | гейт | `src/safewatch/cli.py` | `add_parser("contract"` | `tests/test_contract_files.py::test_contract_check_detects_drift` |
| CLI `import` | 2 | владелец, сид | `src/safewatch/cli.py` | `add_parser("import"` | `tests/test_videos.py::test_import_cli` |
| CLI `eval` | 14 | ML-часть | `src/safewatch/cli.py` | `add_parser("eval"` | `tests/test_eval.py::test_eval_cli_exit_codes` |
| `GET /api/health` | 0 | фронт, Docker | `src/safewatch/api.py` | `@router.get("/api/health")` | `tests/test_api_skeleton.py::test_health_ok` |
| `WS /ws` | 0 | фронт | `src/safewatch/api.py` | `@router.websocket("/ws")` | `tests/test_api_skeleton.py::test_ws_hello_and_unknown_role` |
| `GET /api/meta` | 1 | шапка фронта | `src/safewatch/api.py` | `@router.get("/api/meta")` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
| `GET /api/admin/cameras` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.get("/api/admin/cameras")` | `tests/test_cameras.py::test_cameras_admin_view_shape` |
| `GET /api/sectors` | 1 | фронт | `src/safewatch/api.py` | `@router.get("/api/sectors")` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `POST /api/sectors` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.post("/api/sectors", status_code=201)` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `PUT /api/sectors/{sector_id}` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.put("/api/sectors/{sector_id}")` | `tests/test_cameras.py::test_sector_crud_and_unique_name` |
| `DELETE /api/sectors/{sector_id}` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.delete("/api/sectors/{sector_id}", status_code=204)` | `tests/test_cameras.py::test_sector_delete_with_cameras_conflicts` |
| `GET /api/cameras` | 1 | фронт | `src/safewatch/api.py` | `@router.get("/api/cameras")` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `POST /api/cameras` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.post("/api/cameras", status_code=201)` | `tests/test_cameras.py::test_camera_rejects_bad_input` |
| `GET /api/cameras/{camera_id}` | 1 | фронт | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}")` | `tests/test_cameras.py::test_unknown_ids_are_404` |
| `PATCH /api/cameras/{camera_id}` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.patch("/api/cameras/{camera_id}")` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `DELETE /api/cameras/{camera_id}` | 1 | `/admin/cameras` | `src/safewatch/api.py` | `@router.delete("/api/cameras/{camera_id}", status_code=204)` | `tests/test_cameras.py::test_camera_crud_soft_delete` |
| `POST /api/cameras/{camera_id}/videos` | 2 | `/admin/cameras/:cameraId` | `src/safewatch/api.py` | `@router.post("/api/cameras/{camera_id}/videos", status_code=201)` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| `GET /api/cameras/{camera_id}/videos` | 2 | фронт | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/videos")` | `tests/test_videos.py::test_upload_same_file_reuses_video` |
| `GET /api/videos/{video_id}` | 2 | фронт | `src/safewatch/api.py` | `@router.get("/api/videos/{video_id}")` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| `GET /api/videos/{video_id}/file` | 2 | видеоплеер | `src/safewatch/api.py` | `@router.get("/api/videos/{video_id}/file")` | `tests/test_videos.py::test_video_file_supports_range` |
| `GET /api/jobs` | 2 | `/admin/system` | `src/safewatch/api.py` | `@router.get("/api/jobs")` | `tests/test_jobs.py::test_job_runs_detect_then_pose` |
| `GET /api/jobs/{job_id}` | 2 | фронт | `src/safewatch/api.py` | `@router.get("/api/jobs/{job_id}")` | `tests/test_jobs.py::test_job_runs_detect_then_pose` |
| `GET /api/admin/cameras/{camera_id}` | 2 | `/admin/cameras/:cameraId` | `src/safewatch/api.py` | `@router.get("/api/admin/cameras/{camera_id}")` | `tests/test_videos.py::test_camera_setup_view_shape` |
| `POST /api/jobs/{job_id}/retry` | 3 | `/admin/system` | `src/safewatch/api.py` | `@router.post("/api/jobs/{job_id}/retry")` | `tests/test_jobs_retry.py::test_manual_retry` |
| `GET /api/system` | 3 | `/admin/system` | `src/safewatch/api.py` | `@router.get("/api/system")` | `tests/test_system.py::test_system_view_metrics` |
| `POST /api/system/backend-check` | 3 | `/admin/system`, шапка | `src/safewatch/api.py` | `@router.post("/api/system/backend-check")` | `tests/test_backend_check.py::test_check_four_states` |
| `GET /api/models` | 3 | `/admin/system` | `src/safewatch/api.py` | `@router.get("/api/models")` | `tests/test_system.py::test_models_view` |
| `GET /api/videos/{video_id}/tracks` | 4 | `VideoWithHud` | `src/safewatch/api.py` | `@router.get("/api/videos/{video_id}/tracks")` | `tests/test_tracks_api.py::test_tracks_window_bounds` |
| `GET /api/videos/{video_id}/analysis` | 5 | `Timeline` | `src/safewatch/api.py` | `@router.get("/api/videos/{video_id}/analysis")` | `tests/test_analysis_api.py::test_job_creates_episodes_and_evidence` |
| `POST /api/videos/{video_id}/recompute` | 5 | `/admin/cameras/:cameraId` | `src/safewatch/api.py` | `@router.post("/api/videos/{video_id}/recompute", status_code=202)` | `tests/test_analysis_api.py::test_recompute_creates_new_version` |
| `GET /api/evidence/{evidence_id}/image` | 5 | `EvidenceImage` | `src/safewatch/api.py` | `@router.get("/api/evidence/{evidence_id}/image")` | `tests/test_analysis_api.py::test_evidence_404_and_sha` |
| `GET /api/cameras/{camera_id}/broadcast` | 6 | плееры | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/broadcast")` | `tests/test_broadcast.py::test_start_stop_conflicts_and_messages` |
| `POST /api/cameras/{camera_id}/broadcast` | 6 | `/admin/cameras/:cameraId` | `src/safewatch/api.py` | `@router.post("/api/cameras/{camera_id}/broadcast", status_code=201)` | `tests/test_broadcast.py::test_start_stop_conflicts_and_messages` |
| `DELETE /api/cameras/{camera_id}/broadcast` | 6 | `/admin/cameras/:cameraId` | `src/safewatch/api.py` | `@router.delete("/api/cameras/{camera_id}/broadcast", status_code=204)` | `tests/test_broadcast.py::test_stop_halts_publication` |
| `GET /api/operator/dashboard` | 6 | `/operator` | `src/safewatch/api.py` | `@router.get("/api/operator/dashboard")` | `tests/test_operator_views.py::test_dashboard_and_sector_view_shape` |
| `GET /api/operator/feed` | 6 | `EventFeed` | `src/safewatch/api.py` | `@router.get("/api/operator/feed")` | `tests/test_operator_views.py::test_feed_priority_order` |
| `GET /api/sectors/{sector_id}/view` | 6 | `/operator/sectors/:sectorId` | `src/safewatch/api.py` | `@router.get("/api/sectors/{sector_id}/view")` | `tests/test_operator_views.py::test_dashboard_and_sector_view_shape` |
| `GET /api/cameras/{camera_id}/view` | 6 | `/operator/cameras/:cameraId` | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/view")` | `tests/test_operator_views.py::test_camera_live_view_shape` |
| `GET /api/cameras/{camera_id}/preview` | 6 | плитки камер | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/preview")` | `tests/test_operator_views.py::test_preview_jpeg` |
| `GET /api/events/{event_id}` | 7 | `/events/:eventId`, `/master/events/:eventId` | `src/safewatch/api.py` | `@router.get("/api/events/{event_id}")` | `tests/test_event_detail.py::test_detail_why_history_provenance` |
| `POST /api/events/{event_id}/actions` | 7 | экран события, мастер | `src/safewatch/api.py` | `@router.post("/api/events/{event_id}/actions")` | `tests/test_event_actions.py::test_transition_table` |
| `GET /api/master/inbox` | 8 | `/master` | `src/safewatch/api.py` | `@router.get("/api/master/inbox")` | `tests/test_master.py::test_inbox_contains_only_master_statuses` |
| `GET /api/master/shift` | 8 | `/master/shift` | `src/safewatch/api.py` | `@router.get("/api/master/shift")` | `tests/test_shift.py::test_shift_summary_counts` |
| `GET /api/cameras/{camera_id}/calibration` | 9 | вкладка «Калибровка» | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/calibration")` | `tests/test_calibration.py::test_homography_maps_points` |
| `PUT /api/cameras/{camera_id}/calibration` | 9 | вкладка «Калибровка» | `src/safewatch/api.py` | `@router.put("/api/cameras/{camera_id}/calibration")` | `tests/test_calibration.py::test_calibration_validation` |
| `DELETE /api/cameras/{camera_id}/calibration` | 9 | вкладка «Калибровка» | `src/safewatch/api.py` | `@router.delete("/api/cameras/{camera_id}/calibration", status_code=204)` | `tests/test_calibration.py::test_homography_maps_points` |
| `GET /api/cameras/{camera_id}/zones` | 9 | вкладка «Зоны», HUD | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/zones")` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `POST /api/cameras/{camera_id}/zones` | 9 | вкладка «Зоны» | `src/safewatch/api.py` | `@router.post("/api/cameras/{camera_id}/zones", status_code=201)` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `PATCH /api/zones/{zone_id}` | 9 | вкладка «Зоны» | `src/safewatch/api.py` | `@router.patch("/api/zones/{zone_id}")` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `DELETE /api/zones/{zone_id}` | 9 | вкладка «Зоны» | `src/safewatch/api.py` | `@router.delete("/api/zones/{zone_id}", status_code=204)` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| `GET /api/cameras/{camera_id}/rules` | 9 | вкладка «Правила» | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/rules")` | `tests/test_camera_rules.py::test_rule_params_override_and_ranges` |
| `PUT /api/cameras/{camera_id}/rules/{scenario}` | 9 | вкладка «Правила», `/ohs/rules` | `src/safewatch/api.py` | `@router.put("/api/cameras/{camera_id}/rules/{scenario}")` | `tests/test_camera_rules.py::test_rule_params_override_and_ranges` |
| `GET /api/ohs/rules` | 9 | `/ohs/rules` | `src/safewatch/api.py` | `@router.get("/api/ohs/rules")` | `tests/test_camera_rules.py::test_rules_screen_view` |
| `GET /api/events` | 12 | `/ohs/journal` | `src/safewatch/api.py` | `@router.get("/api/events")` | `tests/test_journal.py::test_filters_each_dimension` |
| `GET /api/events/export.csv` | 12 | `/ohs/journal` | `src/safewatch/api.py` | `@router.get("/api/events/export.csv")` | `tests/test_export.py::test_csv_columns_and_history` |
| `GET /api/journal/facets` | 12 | `/ohs/journal` | `src/safewatch/api.py` | `@router.get("/api/journal/facets")` | `tests/test_journal.py::test_facets_lists` |
| `GET /api/stats/ohs` | 13 | `/ohs/stats` | `src/safewatch/api.py` | `@router.get("/api/stats/ohs")` | `tests/test_stats_ohs.py::test_counts_by_dimensions` |
| `GET /api/stats/management` | 13 | `/management` | `src/safewatch/api.py` | `@router.get("/api/stats/management")` | `tests/test_stats_management.py::test_weeks_and_top_sectors_per_camera` |
| WS `hello` | 0 | фронт | `src/safewatch/api.py` | `"hello"` | `tests/test_api_skeleton.py::test_ws_hello_and_unknown_role` |
| WS `job.progress` | 2 | `/admin/cameras/:cameraId`, `/admin/system` | `src/safewatch/services.py` | `"job.progress"` | `tests/test_jobs.py::test_job_progress_published` |
| WS `backend.status` | 3 | шапка, `/admin/system` | `src/safewatch/services.py` | `"backend.status"` | `tests/test_backend_check.py::test_check_publishes_status` |
| WS `event.created` | 6 | лента, журнал | `src/safewatch/services.py` | `"event.created"` | `tests/test_broadcast.py::test_publish_at_confirm_time_not_before` |
| WS `event.updated` | 6 | лента, экран события, мастер | `src/safewatch/services.py` | `"event.updated"` | `tests/test_broadcast.py::test_yellow_auto_finishes_red_stays` |
| WS `event.escalated` | 6 | лента, захват экрана | `src/safewatch/services.py` | `"event.escalated"` | `tests/test_broadcast.py::test_escalation_updates_same_event` |
| WS `notification` | 6 | `Toasts`, `TakeoverOverlay`, мастер | `src/safewatch/services.py` | `"notification"` | `tests/test_notifications.py::test_notification_texts_and_sounds` |
| WS `camera.state` | 6 | плитки камер | `src/safewatch/services.py` | `"camera.state"` | `tests/test_operator_views.py::test_state_changes_published` |
| WS `sector.state` | 6 | плитки секторов | `src/safewatch/services.py` | `"sector.state"` | `tests/test_operator_views.py::test_state_changes_published` |
| WS `broadcast.state` | 6 | плееры | `src/safewatch/services.py` | `"broadcast.state"` | `tests/test_broadcast.py::test_start_stop_conflicts_and_messages` |
| ключ `.env` `INFERENCE_BACKEND` | 2 | `make_backend` | `.env.example` | `INFERENCE_BACKEND=` | `tests/test_jobs.py::test_make_backend_by_settings` |
| ключ `.env` `SAFEWATCH_FAKE` | 0 | `make_backend` | `.env.example` | `SAFEWATCH_FAKE=` | `tests/test_config.py::test_settings_carry_no_keys_and_no_fakes` |
| ключ `.env` `LINQ_JUPYTER_URL` | 0 | `JupyterShell`, `doctor` | `.env.example` | `LINQ_JUPYTER_URL=` | `tests/test_cli.py::test_doctor_reports_missing_keys` |
| поле `Settings.inference_backend` | 2 | `make_backend` | `src/safewatch/config.py` | `validation_alias="INFERENCE_BACKEND"` | `tests/test_jobs.py::test_make_backend_by_settings` |
| поле `Settings.fake` | 0 | `make_backend`, `meta` | `src/safewatch/config.py` | `validation_alias="SAFEWATCH_FAKE"` | `tests/test_config.py::test_settings_carry_no_keys_and_no_fakes` |
| `config.Settings` | 0 | все | `src/safewatch/config.py` | `class Settings(BaseSettings):` | `tests/test_config.py::test_owner_user_yaml_does_not_reach_tests` |
| `config.get_settings` | 0 | все | `src/safewatch/config.py` | `def get_settings(` | `tests/test_config.py::test_relative_data_dir_resolves_from_the_repo` |
| ключ `product_name` (v5: Argus) | 16 | `meta` | `config/default.yaml` | `product_name: Argus` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
| ключ `data_dir` | 0 | `services`, `cli` | `config/default.yaml` | `data_dir: data/app` | `tests/test_config.py::test_relative_data_dir_resolves_from_the_repo` |
| ключ `timezone` | 8 | смены, статистика | `config/default.yaml` | `timezone: Europe/Moscow` | `tests/test_shift.py::test_shift_window_boundaries` |
| секция `server` | 0 | `cli serve` | `config/default.yaml` | `port: 8000` | `tests/test_cli.py::test_serve_starts_and_stops` |
| секция `upload` | 2 | `video_upload` | `config/default.yaml` | `max_mb: 2048` | `tests/test_videos.py::test_upload_limit_boundary` |
| секция `pipeline` | 2 | `run_next_job` | `config/default.yaml` | `target_analysis_fps: 12` | `tests/test_jobs.py::test_step_from_fps` |
| ключи `pipeline.detector`, `pipeline.pose` | 0 | `registry` | `config/default.yaml` | `detector: det-yolov8n@640-ap9999` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| секция `class_conf` | 4 | `analysis.pipeline` | `config/default.yaml` | `truck: 0.35` | `tests/test_tracking.py::test_class_conf_filters_before_tracking` |
| секция `tracker` | 4 | `analysis.tracking` | `config/default.yaml` | `max_lost_s: 1.0` | `tests/test_tracking.py::test_lost_longer_than_ttl_gets_new_id` |
| секция `pose` | 4 | `analysis.features` | `config/default.yaml` | `match_iou: 0.5` | `tests/test_features.py::test_pose_attached_by_iou` |
| секция `features` | 4 | `analysis.features` | `config/default.yaml` | `speed_window_s: 1.0` | `tests/test_features.py::test_speed_body_heights_per_second` |
| секция `episodes` | 5 | `analysis.episodes` | `config/default.yaml` | `end_after_s: 2.0` | `tests/test_episodes.py::test_end_after_negatives_and_rearm` |
| параметры `scenarios.running` | 5 | `RunningPlugin` | `config/default.yaml` | `speed_bh_s: 1.5` | `tests/test_rule_running.py::test_running_threshold_boundary` |
| параметры `scenarios.fall` | 5 | `FallPlugin` | `config/default.yaml` | `still_s: 10.0` | `tests/test_rule_fall.py::test_lying_still_without_transition` |
| параметры `scenarios.proximity` | 10 | `ProximityPlugin` | `config/default.yaml` | `yellow_bh: 2.0` | `tests/test_rule_proximity.py::test_moving_vehicle_distance_levels` |
| параметры `scenarios.phone` | 10 | `PhonePlugin` | `config/default.yaml` | `danger_hold_s: 3.0` | `tests/test_rule_phone.py::test_phone_hold_boundary` |
| параметры `scenarios.fence_crossing` | 10 | `FencePlugin` | `config/default.yaml` | `max_gap_s: 1.0` | `tests/test_rule_fence.py::test_crossing_detected_once` |
| параметры `scenarios.restricted_under` | 10 | `UnderPlugin` | `config/default.yaml` | `under_hold_s: 0.5` | `tests/test_rule_under.py::test_under_zone_red_after_hold` |
| параметры `scenarios.fire_smoking` | 10 | `FirePlugin` | `config/default.yaml` | `fire_hold_s: 1.0` | `tests/test_rule_fire.py::test_fire_outside_allowed_zone_red` |
| параметры `scenarios.no_harness` | 10 | `HarnessPlugin` | `config/default.yaml` | `harness_hold_s: 3.0` | `tests/test_plugin_status.py::test_status_follows_active_model_classes` |
| параметры `scenarios.suspended_load` | 10 | `SuspendedLoadPlugin` | `config/default.yaml` | `load_hold_s: 0.5` | `tests/test_plugin_status.py::test_status_follows_active_model_classes` |
| параметры `scenarios.load_carrying` | 10 | `LoadCarryingPlugin` | `config/default.yaml` | `load_carrying: {}` | `tests/test_plugin_status.py::test_skeletons_listed_with_texts` |
| секция `zone_kinds` | 1 | `meta`, зоны | `config/default.yaml` | `- id: danger` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
| секция `escalation` | 7 | `escalation_tick` | `config/default.yaml` | `timeout_s: 45` | `tests/test_escalation.py::test_timeout_key_changes_behavior` |
| секция `broadcast` | 6 | `broadcast_tick`, `worker` | `config/default.yaml` | `tick_ms: 250` | `tests/test_worker.py::test_loop_periods_from_config` |
| секция `feed` | 6 | `operator_feed` | `config/default.yaml` | `recent_closed_min: 30` | `tests/test_operator_views.py::test_feed_priority_order` |
| секция `observability` | 11 | `analysis.observability` | `config/default.yaml` | `dark_mean: 35` | `tests/test_observability.py::test_dark_and_obstructed_gaps` |
| секция `evidence` | 5 | `run_next_job` | `config/default.yaml` | `jpeg_quality: 85` | `tests/test_analysis_api.py::test_evidence_404_and_sha` |
| секция `preview` | 6 | `camera_preview` | `config/default.yaml` | `cache_s: 2.0` | `tests/test_operator_views.py::test_preview_jpeg` |
| секция `hud` | 4 | `video_tracks` | `config/default.yaml` | `window_max_ms: 10000` | `tests/test_tracks_api.py::test_tracks_window_bounds` |
| секция `jobs` | 2 | `run_next_job` | `config/default.yaml` | `max_attempts: 3` | `tests/test_jobs.py::test_backoff_and_max_attempts` |
| ключи `linq.remote_dir`, `linq.file_prefix`, `linq.inflight` | 2 | `LinqBackend` | `config/default.yaml` | `remote_dir: baseline` | `tests/test_linq_backend.py::test_commands_use_baseline_dir_and_registry` |
| ключ `linq.job_timeout_s` | 2 | `LinqBackend` | `config/default.yaml` | `job_timeout_s: 1800` | `tests/test_jobs.py::test_timeout_kills_remote_worker` |
| ключ `linq.check_cache_s` | 3 | `backend_check` | `config/default.yaml` | `check_cache_s: 30` | `tests/test_backend_check.py::test_check_is_cached` |
| секция `local` | 3 | `LocalBackend` | `config/default.yaml` | `threads: 2` | `tests/test_local_backend.py::test_local_matches_jsonl_format` |
| секция `shifts` | 8 | `shift_summary_view`, статистика | `config/default.yaml` | `- id: day` | `tests/test_shift.py::test_shift_window_boundaries` |
| секция `stats` | 13 | статистика | `config/default.yaml` | `trend_weeks: 4` | `tests/test_stats_management.py::test_yellow_trend_text` |
| секция `journal` | 12 | журнал | `config/default.yaml` | `page_max: 200` | `tests/test_journal.py::test_filter_validation` |
| секция `master` | 8 | `master_inbox_view` | `config/default.yaml` | `recent_resolved: 20` | `tests/test_master.py::test_recent_resolved_limit` |
| секция `delivery` | 15 | `deliveries_flush` | `config/default.yaml` | `webhooks: []` | `tests/test_delivery.py::test_webhook_sent_on_red` |
| секция `eval` | 14 | `eval_run` | `config/default.yaml` | `deadline_s: 5.0` | `tests/test_eval.py::test_matching_deadline_boundary` |
| реестр: детектор 640 | 0 | `registry` | `config/models.yaml` | `linq_program: mosprom_det640_cut_ap9999_b1_o1_h1m.tpu` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| реестр: pose 640 | 0 | `registry` | `config/models.yaml` | `linq_program: mosprom_pose640_cut_ap9999_b1_o1_h1m.tpu` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| реестр: детектор 960 | 0 | `registry` | `config/models.yaml` | `linq_program: mosprom_det960_cut_ap9999_b1_o1_h1m.tpu` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| `registry.load_models` | 0 | `services`, `doctor` | `src/safewatch/registry.py` | `def load_models(` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| константа `CONTRACT_VERSION` (v5: 1.1.0) | 16 | `api`, контракт | `src/safewatch/api.py` | `CONTRACT_VERSION = "1.1.0"` | `tests/test_api_skeleton.py::test_health_ok` |
| константа `BROWSER_CODECS` | 2 | `probe_video` | `src/safewatch/media.py` | `BROWSER_CODECS = (` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| константа `CACHE_SCHEMA` | 2 | `cache_key` | `src/safewatch/inference/artifacts.py` | `CACHE_SCHEMA = "jsonl-v1"` | `tests/test_jobs.py::test_cache_hit_skips_remote` |
| константа `CLIENT_QUEUE` | 0 | `hub` | `src/safewatch/hub.py` | `CLIENT_QUEUE = 1000` | `tests/test_hub.py::test_queue_overflow_drops_client` |
| константа `NAME_MAX` | 1 | валидация | `src/safewatch/services.py` | `NAME_MAX = 80` | `tests/test_cameras.py::test_camera_rejects_bad_input` |
| константа `DESCRIPTION_MAX` | 1 | валидация | `src/safewatch/services.py` | `DESCRIPTION_MAX = 300` | `tests/test_cameras.py::test_camera_rejects_bad_input` |
| константа `COMMENT_MAX` | 7 | валидация | `src/safewatch/services.py` | `COMMENT_MAX = 500` | `tests/test_event_actions.py::test_resolve_requires_comment` |
| константа `ACTOR_MAX` | 7 | валидация | `src/safewatch/services.py` | `ACTOR_MAX = 60` | `tests/test_event_actions.py::test_actor_header_limits` |
| константа `ZONE_NAME_MAX` | 9 | валидация | `src/safewatch/services.py` | `ZONE_NAME_MAX = 60` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| константа `ZONE_POINTS_MAX` | 9 | валидация | `src/safewatch/services.py` | `ZONE_POINTS_MAX = 32` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| константа `QUERY_MAX` | 12 | валидация | `src/safewatch/services.py` | `QUERY_MAX = 100` | `tests/test_journal.py::test_filter_validation` |
| константа `PRIORITY` | 6 | лента | `src/safewatch/services.py` | `PRIORITY = {` | `tests/test_operator_views.py::test_feed_priority_order` |
| константа `MIN_CAL_POINTS` | 9 | калибровка | `src/safewatch/analysis/geometry.py` | `MIN_CAL_POINTS = 4` | `tests/test_calibration.py::test_calibration_validation` |
| константа `MAX_CAL_POINTS` | 9 | калибровка | `src/safewatch/analysis/geometry.py` | `MAX_CAL_POINTS = 8` | `tests/test_calibration.py::test_calibration_validation` |
| константа `MIN_AREA` | 9 | калибровка, зоны | `src/safewatch/analysis/geometry.py` | `MIN_AREA = 1e-4` | `tests/test_zones.py::test_zone_crud_and_geometry_rules` |
| константы сида `SEED`, `DAYS`, `EVENTS` | 0 | `seed_demo` | `src/safewatch/seed.py` | `EVENTS = 240` | `tests/test_seed.py::test_seed_creates_demo_world_once` |
| `seed.build_demo` | 0 | `seed_demo` | `src/safewatch/seed.py` | `def build_demo(` | `tests/test_seed.py::test_seed_creates_demo_world_once` |
| `clock.now` | 0 | все слои | `src/safewatch/clock.py` | `def now(` | `tests/test_clock.py::test_iso_roundtrip_utc_millis` |
| `hub.Hub` | 0 | `api`, `services` | `src/safewatch/hub.py` | `class Hub:` | `tests/test_hub.py::test_audience_filtering` |
| `texts.STATUS_TITLES` | 1 | `meta`, события | `src/safewatch/texts.py` | `STATUS_TITLES = {` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
| `texts.notification_text` | 6 | уведомления | `src/safewatch/texts.py` | `def notification_text(` | `tests/test_notifications.py::test_notification_texts_and_sounds` |
| `media.probe_video` | 2 | `video_upload` | `src/safewatch/media.py` | `def probe_video(` | `tests/test_videos.py::test_upload_rejects_bad_files` |
| `media.read_frame` | 5 | доказательства, превью | `src/safewatch/media.py` | `def read_frame(` | `tests/test_analysis_api.py::test_job_creates_episodes_and_evidence` |
| `media.encode_jpeg` | 5 | доказательства, превью | `src/safewatch/media.py` | `def encode_jpeg(` | `tests/test_analysis_api.py::test_evidence_404_and_sha` |
| `media.sample_luma` | 11 | наблюдаемость | `src/safewatch/media.py` | `def sample_luma(` | `tests/test_observability.py::test_dark_and_obstructed_gaps` |
| `analysis.pipeline.analyze` | 4 | `run_next_job` | `src/safewatch/analysis/pipeline.py` | `def analyze(` | `tests/test_tracks_api.py::test_tracks_window_contents` |
| `analysis.tracking.Tracker` | 4 | `analyze` | `src/safewatch/analysis/tracking.py` | `class Tracker:` | `tests/test_tracking.py::test_single_walker_keeps_one_id` |
| `geometry.point_in_polygon` | 4 | признаки, плагины | `src/safewatch/analysis/geometry.py` | `def point_in_polygon(` | `tests/test_geometry.py::test_point_in_polygon_properties` |
| `geometry.homography` | 9 | калибровка, признаки | `src/safewatch/analysis/geometry.py` | `def homography(` | `tests/test_calibration.py::test_homography_maps_points` |
| `geometry.segment_crossing` | 10 | `FencePlugin` | `src/safewatch/analysis/geometry.py` | `def segment_crossing(` | `tests/test_rule_fence.py::test_crossing_detected_once` |
| `features.person_states` | 4 | `analyze` | `src/safewatch/analysis/features.py` | `def person_states(` | `tests/test_features.py::test_speed_body_heights_per_second` |
| `features.vehicle_states` | 10 | `analyze` | `src/safewatch/analysis/features.py` | `def vehicle_states(` | `tests/test_rule_proximity.py::test_stationary_vehicle_negative` |
| `episodes.EpisodeManager` | 5 | `analyze` | `src/safewatch/analysis/episodes.py` | `class EpisodeManager:` | `tests/test_episodes.py::test_confirm_after_hold` |
| `observability.find_gaps` | 11 | `analyze` | `src/safewatch/analysis/observability.py` | `def find_gaps(` | `tests/test_observability.py::test_stale_gap_from_missing_frames` |
| `hud.build_hud` | 4 | `analyze` | `src/safewatch/analysis/hud.py` | `def build_hud(` | `tests/test_hud.py::test_tags_texts_russian_format` |
| `rules.scenario_metas` | 5 | `meta`, правила | `src/safewatch/rules/__init__.py` | `def scenario_metas(` | `tests/test_analysis_api.py::test_meta_lists_running_and_fall` |
| `rules.PLUGINS` | 10 | `analyze`, `meta` | `src/safewatch/rules/__init__.py` | `PLUGINS: list[ScenarioPlugin] = [` | `tests/test_plugin_status.py::test_skeletons_listed_with_texts` |
| `rules.plugin` | 10 | `analyze`, `event_detail` | `src/safewatch/rules/__init__.py` | `def plugin(` | `tests/test_plugin_status.py::test_skeletons_listed_with_texts` |
| `geometry.ioa` | 10 | `proximity`, `no_harness` | `src/safewatch/analysis/geometry.py` | `def ioa(` | `tests/test_geometry.py::test_ioa_properties` |
| поле `AnalysisConfig.extra_artifact_ids` | 10 | `recompute` | `src/safewatch/types.py` | `extra_artifact_ids: list[int] = []` | `tests/test_plugin_status.py::test_extra_model_enables_fire_without_code` |
| плагин `running` | 5 | `analyze` | `src/safewatch/rules/running.py` | `class RunningPlugin:` | `tests/test_rule_running.py::test_running_threshold_boundary` |
| плагин `fall` | 5 | `analyze` | `src/safewatch/rules/fall.py` | `class FallPlugin:` | `tests/test_rule_fall.py::test_fall_transition_red` |
| плагин `proximity` | 10 | `analyze` | `src/safewatch/rules/proximity.py` | `class ProximityPlugin:` | `tests/test_rule_proximity.py::test_moving_vehicle_distance_levels` |
| плагин `phone` | 10 | `analyze` | `src/safewatch/rules/phone.py` | `class PhonePlugin:` | `tests/test_rule_phone.py::test_phone_hold_boundary` |
| плагин `fence_crossing` | 10 | `analyze` | `src/safewatch/rules/fence.py` | `class FencePlugin:` | `tests/test_rule_fence.py::test_crossing_detected_once` |
| плагин `restricted_under` | 10 | `analyze` | `src/safewatch/rules/under.py` | `class UnderPlugin:` | `tests/test_rule_under.py::test_under_zone_red_after_hold` |
| плагин `fire_smoking` | 10 | `analyze` | `src/safewatch/rules/fire.py` | `class FirePlugin:` | `tests/test_rule_fire.py::test_fire_outside_allowed_zone_red` |
| плагин `no_harness` | 10 | `analyze` | `src/safewatch/rules/harness.py` | `class HarnessPlugin:` | `tests/test_plugin_status.py::test_status_follows_active_model_classes` |
| плагин `suspended_load` | 10 | `analyze` | `src/safewatch/rules/suspended_load.py` | `class SuspendedLoadPlugin:` | `tests/test_plugin_status.py::test_status_follows_active_model_classes` |
| плагин `load_carrying` | 10 | `meta` | `src/safewatch/rules/load_carrying.py` | `class LoadCarryingPlugin:` | `tests/test_plugin_status.py::test_skeletons_listed_with_texts` |
| `worker.run_forever` | 6 | `api` lifespan | `src/safewatch/worker.py` | `async def run_forever(` | `tests/test_worker.py::test_loop_periods_from_config` |
| `doctor.run` | 0 | CLI `doctor` | `src/safewatch/doctor.py` | `def run(` | `tests/test_cli.py::test_doctor_fake_mode_ok` |
| `evaluate.match_episodes` | 14 | `eval_run` | `src/safewatch/evaluate.py` | `def match_episodes(` | `tests/test_eval.py::test_matching_deadline_boundary` |
| воркер LinQ: аргумент `--nc` | 10 | `LinqBackend` для моделей `pipeline.extra` | `tools/linq/remote/video_worker.py` | `"--nc"` | `tests/test_plugin_status.py::test_extra_model_enables_fire_without_code` |
| файл `contract/openapi.json` | 0 | фронт, мок | `contract/openapi.json` | `"openapi"` | `tests/test_contract_files.py::test_openapi_matches_app` |
| файл `contract/ws.schema.json` | 0 | фронт | `contract/ws.schema.json` | `"WsMessage"` | `tests/test_contract_files.py::test_ws_schema_matches_types` |
| файл `contract/ws-examples.json` | 0 | мок WS | `contract/ws-examples.json` | `"event.created"` | `tests/test_contract_files.py::test_ws_examples_cover_every_type` |
| `scripts/eol_check.py` | 0 | гейт | `scripts/eol_check.py` | `def main(` | `tests/test_contract_files.py::test_eol_check_flags_crlf` |
| `scripts/contract_check.py` | 0 | гейт | `scripts/contract_check.py` | `def trace_rows(` | `tests/test_contract_check.py::test_closed_slice_element_not_found_is_red` |
| фронт: клиент API | 0 | экраны | `frontend/src/api/client.ts` | `export const api =` | `frontend/src/App.test.tsx::client_sends_role_header` |
| фронт: `useApi` | 0 | экраны | `frontend/src/api/useApi.ts` | `export function useApi(` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: `useWs` | 0 | экраны | `frontend/src/api/ws.ts` | `export function useWs(` | `frontend/src/App.test.tsx::ws_connects_with_role` |
| фронт: роль | 0 | шапка, клиент | `frontend/src/roles.ts` | `export function useRole(` | `frontend/src/App.test.tsx::role_switcher_changes_nav` |
| фронт: `AppShell` | 0 | все экраны | `frontend/src/components/AppShell.tsx` | `export function AppShell(` | `frontend/src/App.test.tsx::role_switcher_changes_nav` |
| фронт: `RoleSwitcher` | 0 | `AppShell` | `frontend/src/components/RoleSwitcher.tsx` | `export function RoleSwitcher(` | `frontend/src/App.test.tsx::role_switcher_changes_nav` |
| фронт: `StubNotice` | 0 | экраны-заглушки | `frontend/src/components/StubNotice.tsx` | `export function StubNotice(` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: `LevelBadge` | 0 | лента, журнал | `frontend/src/components/Badges.tsx` | `export function LevelBadge(` | `frontend/src/App.test.tsx::badges_show_text_and_icon` |
| фронт: `StatusBadge` | 0 | лента, журнал | `frontend/src/components/Badges.tsx` | `export function StatusBadge(` | `frontend/src/App.test.tsx::badges_show_text_and_icon` |
| фронт: маршрут `/operator` | 0 | навигация | `frontend/src/nav.ts` | `path: "/operator"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/operator/sectors/:sectorId` | 0 | навигация | `frontend/src/nav.ts` | `path: "/operator/sectors/:sectorId"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/operator/cameras/:cameraId` | 0 | навигация | `frontend/src/nav.ts` | `path: "/operator/cameras/:cameraId"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/events/:eventId` | 0 | навигация | `frontend/src/nav.ts` | `path: "/events/:eventId"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/master` | 0 | навигация | `frontend/src/nav.ts` | `path: "/master"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/master/events/:eventId` | 0 | навигация | `frontend/src/nav.ts` | `path: "/master/events/:eventId"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/master/shift` | 0 | навигация | `frontend/src/nav.ts` | `path: "/master/shift"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/ohs/journal` | 0 | навигация | `frontend/src/nav.ts` | `path: "/ohs/journal"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/ohs/rules` | 0 | навигация | `frontend/src/nav.ts` | `path: "/ohs/rules"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/ohs/stats` | 0 | навигация | `frontend/src/nav.ts` | `path: "/ohs/stats"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/management` | 0 | навигация | `frontend/src/nav.ts` | `path: "/management"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/admin/cameras` | 0 | навигация | `frontend/src/nav.ts` | `path: "/admin/cameras"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/admin/cameras/:cameraId` | 0 | навигация | `frontend/src/nav.ts` | `path: "/admin/cameras/:cameraId"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: маршрут `/admin/system` | 0 | навигация | `frontend/src/nav.ts` | `path: "/admin/system"` | `frontend/src/App.test.tsx::stub_screens_show_slice` |
| фронт: экран `CamerasScreen` | 1 | `/admin/cameras` | `frontend/src/screens/admin/CamerasScreen.tsx` | `export function CamerasScreen(` | `frontend/src/screens/screens.test.tsx::cameras_screen_renders` |
| фронт: `Modal`, `FormField` | 1 | формы | `frontend/src/components/Form.tsx` | `export function Modal(` | `frontend/src/screens/screens.test.tsx::cameras_screen_renders` |
| фронт: `DataTable` | 1 | таблицы | `frontend/src/components/DataTable.tsx` | `export function DataTable(` | `frontend/src/screens/screens.test.tsx::cameras_screen_renders` |
| фронт: экран `CameraSetup` | 2 | `/admin/cameras/:cameraId` | `frontend/src/screens/admin/CameraSetup.tsx` | `export function CameraSetup(` | `frontend/src/screens/screens.test.tsx::camera_setup_renders` |
| фронт: экран `SystemScreen` | 3 | `/admin/system` | `frontend/src/screens/admin/SystemScreen.tsx` | `export function SystemScreen(` | `frontend/src/screens/screens.test.tsx::system_screen_renders` |
| фронт: `layoutHud` | 4 | `HudCanvas` | `frontend/src/components/hud.ts` | `export function layoutHud(` | `frontend/src/components/hud.test.ts::callouts_stay_inside_frame` |
| фронт: `HudCanvas` | 4 | плееры, кадры | `frontend/src/components/HudCanvas.tsx` | `export function HudCanvas(` | `frontend/src/components/hud.test.ts::hidden_hud_draws_nothing` |
| фронт: `VideoWithHud` | 4 | плееры | `frontend/src/components/VideoWithHud.tsx` | `export function VideoWithHud(` | `frontend/src/screens/screens.test.tsx::camera_setup_player_renders` |
| фронт: `Timeline` | 5 | настройка камеры, камера | `frontend/src/components/Timeline.tsx` | `export function Timeline(` | `frontend/src/screens/screens.test.tsx::camera_setup_timeline_renders` |
| фронт: `EvidenceImage` | 5 | экран события, мастер | `frontend/src/components/EvidenceImage.tsx` | `export function EvidenceImage(` | `frontend/src/screens/screens.test.tsx::camera_setup_timeline_renders` |
| фронт: `playSound` | 6 | уведомления | `frontend/src/components/sound.ts` | `export function playSound(` | `frontend/src/screens/screens.test.tsx::takeover_on_red_notification` |
| фронт: `Toasts` | 6 | `AppShell` | `frontend/src/components/Toasts.tsx` | `export function Toasts(` | `frontend/src/screens/screens.test.tsx::operator_dashboard_renders` |
| фронт: `TakeoverOverlay` | 6 | `AppShell` оператора | `frontend/src/components/TakeoverOverlay.tsx` | `export function TakeoverOverlay(` | `frontend/src/screens/screens.test.tsx::takeover_on_red_notification` |
| фронт: `EventFeed` | 6 | оператор | `frontend/src/components/EventFeed.tsx` | `export function EventFeed(` | `frontend/src/screens/screens.test.tsx::operator_dashboard_renders` |
| фронт: `SectorTile` | 6 | оператор | `frontend/src/components/SectorTile.tsx` | `export function SectorTile(` | `frontend/src/screens/screens.test.tsx::operator_dashboard_renders` |
| фронт: экран `OperatorDashboard` | 6 | `/operator` | `frontend/src/screens/operator/OperatorDashboard.tsx` | `export function OperatorDashboard(` | `frontend/src/screens/screens.test.tsx::operator_dashboard_renders` |
| фронт: экран `SectorScreen` | 6 | `/operator/sectors/:sectorId` | `frontend/src/screens/operator/SectorScreen.tsx` | `export function SectorScreen(` | `frontend/src/screens/screens.test.tsx::sector_screen_renders` |
| фронт: экран `CameraScreen` | 6 | `/operator/cameras/:cameraId` | `frontend/src/screens/operator/CameraScreen.tsx` | `export function CameraScreen(` | `frontend/src/screens/screens.test.tsx::camera_screen_renders` |
| фронт: экран `EventScreen` | 7 | `/events/:eventId` | `frontend/src/screens/events/EventScreen.tsx` | `export function EventScreen(` | `frontend/src/screens/screens.test.tsx::event_screen_renders` |
| фронт: экран `MasterInbox` | 8 | `/master` | `frontend/src/screens/master/MasterInbox.tsx` | `export function MasterInbox(` | `frontend/src/screens/screens.test.tsx::master_inbox_renders` |
| фронт: экран `MasterEvent` | 8 | `/master/events/:eventId` | `frontend/src/screens/master/MasterEvent.tsx` | `export function MasterEvent(` | `frontend/src/screens/screens.test.tsx::master_event_renders` |
| фронт: экран `ShiftSummaryScreen` | 8 | `/master/shift` | `frontend/src/screens/master/ShiftSummaryScreen.tsx` | `export function ShiftSummaryScreen(` | `frontend/src/screens/screens.test.tsx::shift_summary_renders` |
| фронт: `PolygonEditor` | 9 | калибровка, зоны | `frontend/src/components/PolygonEditor.tsx` | `export function PolygonEditor(` | `frontend/src/screens/screens.test.tsx::camera_setup_zones_renders` |
| фронт: экран `RulesScreen` | 9 | `/ohs/rules` | `frontend/src/screens/ohs/RulesScreen.tsx` | `export function RulesScreen(` | `frontend/src/screens/screens.test.tsx::rules_screen_renders` |
| фронт: `FiltersBar` | 12 | журнал | `frontend/src/components/FiltersBar.tsx` | `export function FiltersBar(` | `frontend/src/screens/screens.test.tsx::journal_renders` |
| фронт: экран `Journal` | 12 | `/ohs/journal` | `frontend/src/screens/ohs/Journal.tsx` | `export function Journal(` | `frontend/src/screens/screens.test.tsx::journal_renders` |
| фронт: графики | 13 | статистика | `frontend/src/components/Charts.tsx` | `export function BarChartCard(` | `frontend/src/screens/screens.test.tsx::ohs_stats_renders` |
| фронт: экран `OhsStats` | 13 | `/ohs/stats` | `frontend/src/screens/ohs/OhsStats.tsx` | `export function OhsStats(` | `frontend/src/screens/screens.test.tsx::ohs_stats_renders` |
| фронт: экран `ManagementDashboard` | 13 | `/management` | `frontend/src/screens/management/ManagementDashboard.tsx` | `export function ManagementDashboard(` | `frontend/src/screens/screens.test.tsx::management_renders` |
| тип `media.VideoProbe` | 2 | `probe_video` | `src/safewatch/media.py` | `class VideoProbe(BaseModel):` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| константа `media.CODEC_ALIASES` | 2 | `probe_video` | `src/safewatch/media.py` | `CODEC_ALIASES = {"fmp4": "mp4v"}` | `tests/test_videos.py::test_upload_probes_and_queues_job` |
| `media.encode_jpeg` | 5 | доказательства | `src/safewatch/media.py` | `def encode_jpeg(` | `tests/test_analysis_api.py::test_job_creates_episodes_and_evidence` |
| `registry.MODELS_FILE` | 0 | `registry`, `doctor` | `src/safewatch/registry.py` | `MODELS_FILE = ` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| `registry.resolve` со списком моделей | 0 | `services`, `rules` | `src/safewatch/registry.py` | `def resolve(ref: str, models: list[ModelSpec] \| None = None) -> ModelSpec:` | `tests/test_config.py::test_models_registry_resolves_active_models` |
| `config.ENV_NAMES` | 0 | `doctor` | `src/safewatch/config.py` | `ENV_NAMES = {` | `tests/test_config.py::test_settings_carry_no_keys_and_no_fakes` |
| `texts.SCENARIO_TITLES` | 5 | `meta`, плагины | `src/safewatch/texts.py` | `SCENARIO_TITLES: dict[str, str] = {` | `tests/test_analysis_api.py::test_meta_lists_running_and_fall` |
| `rules.defaults` | 5 | `analyze`, правила | `src/safewatch/rules/__init__.py` | `def defaults(` | `tests/test_rule_running.py::test_running_threshold_boundary` |
| `geometry.point_rect_distance` | 5 | `running` | `src/safewatch/analysis/geometry.py` | `def point_rect_distance(` | `tests/test_rule_running.py::test_running_red_in_danger_zone` |
| `JupyterShell._drop` | 2 | `LinqBackend` | `src/safewatch/inference/linq.py` | `def _drop(` | `tests/test_linq_backend.py::test_jupyter_shell_starts_fresh_session_after_network_error` |
| цикл задач переживает ошибку шага | 2 | `api` lifespan | `src/safewatch/worker.py` | `log.exception("job loop")` | `tests/test_jobs.py::test_job_loop_survives_unexpected_error` |
| `observability.Luma` | 11 | `analyze` | `src/safewatch/analysis/observability.py` | `Luma = tuple[int, float, float]` | `tests/test_observability.py::test_uncertain_time_in_why` |
| `media.LUMA_WIDTH` | 11 | `sample_luma` | `src/safewatch/media.py` | `LUMA_WIDTH = 160` | `tests/test_observability.py::test_dark_and_obstructed_gaps` |
| `store.publish_latencies` | 11 | `system_view.latency` | `src/safewatch/store.py` | `def publish_latencies(` | `tests/test_broadcast.py::test_latency_counts_published_events` |
| `services.DELIVERED` | 15 | `broadcast_tick` | `src/safewatch/services.py` | `DELIVERED: dict[WsType, DeliveryKind] = {` | `tests/test_delivery.py::test_webhook_sent_on_red` |
| `delivery.target` | 15 | `system_view.channels` | `src/safewatch/delivery.py` | `def target(` | `tests/test_delivery.py::test_channels_in_system_view` |
| v5: таблица `delivery_queue` | 16 | `deliveries_flush` | `src/safewatch/migrations/0002_v5.sql` | `CREATE TABLE delivery_queue (` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: таблица `dataset_items` | 16 | `datasets_flush` | `src/safewatch/migrations/0002_v5.sql` | `CREATE TABLE dataset_items (` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: таблица `demo_packs` | 16 | `demo_import` | `src/safewatch/migrations/0002_v5.sql` | `CREATE TABLE demo_packs (` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: колонка `videos.web_path` | 16 | `video_file` | `src/safewatch/migrations/0002_v5.sql` | `ALTER TABLE videos ADD COLUMN web_path TEXT;` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: колонка `analyses.autocal_json` | 16 | `video_analysis` | `src/safewatch/migrations/0002_v5.sql` | `ALTER TABLE analyses ADD COLUMN autocal_json TEXT;` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: колонки идентификации `events` | 16 | `event_identify` | `src/safewatch/migrations/0002_v5.sql` | `ALTER TABLE events ADD COLUMN crew TEXT NOT NULL DEFAULT '';` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: колонка `deliveries.delivered_at` | 16 | `deliveries_flush` | `src/safewatch/migrations/0002_v5.sql` | `ALTER TABLE deliveries ADD COLUMN delivered_at TEXT;` | `tests/test_db.py::test_migrate_v5_tables_and_columns` |
| v5: тип `SpeedSource` | 16 | признаки, HUD | `src/safewatch/types.py` | `SpeedSource = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `PassportVerdict` | 16 | паспорт | `src/safewatch/types.py` | `PassportVerdict = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `CalcTier` | 16 | калькулятор | `src/safewatch/types.py` | `CalcTier = Literal[` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `AutoCalibration` | 16 | анализ, экран настройки | `src/safewatch/types.py` | `class AutoCalibration(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `Clip` | 16 | события | `src/safewatch/types.py` | `class Clip(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoArtifact` | 16 | демо-пакет | `src/safewatch/types.py` | `class DemoArtifact(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoVideo` | 16 | демо-пакет | `src/safewatch/types.py` | `class DemoVideo(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoCamera` | 16 | демо-пакет | `src/safewatch/types.py` | `class DemoCamera(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoManifest` | 16 | демо-пакет | `src/safewatch/types.py` | `class DemoManifest(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoLayout` | 16 | сборка демо-пакета | `src/safewatch/types.py` | `class DemoLayout(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoPack` | 16 | `GET /api/demo/packs` | `src/safewatch/types.py` | `class DemoPack(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DemoImportReport` | 16 | CLI `demo import` | `src/safewatch/types.py` | `class DemoImportReport(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `CalcAssumption` | 16 | калькулятор | `src/safewatch/types.py` | `class CalcAssumption(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `RolloutIn` | 16 | калькулятор | `src/safewatch/types.py` | `class RolloutIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `TierResult` | 16 | калькулятор | `src/safewatch/types.py` | `class TierResult(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `RolloutResult` | 16 | калькулятор | `src/safewatch/types.py` | `class RolloutResult(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `ScaleIn` | 16 | калькулятор | `src/safewatch/types.py` | `class ScaleIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `ScaleResult` | 16 | калькулятор | `src/safewatch/types.py` | `class ScaleResult(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `CalculatorDefaults` | 16 | калькулятор | `src/safewatch/types.py` | `class CalculatorDefaults(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DatasetItem` | 16 | датасет | `src/safewatch/types.py` | `class DatasetItem(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `DatasetView` | 16 | датасет | `src/safewatch/types.py` | `class DatasetView(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `IdentityIn` | 16 | идентификация | `src/safewatch/types.py` | `class IdentityIn(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `PeopleStats` | 16 | статистика по людям | `src/safewatch/types.py` | `class PeopleStats(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `PassportScenario` | 16 | паспорт | `src/safewatch/types.py` | `class PassportScenario(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: тип `CameraPassport` | 16 | паспорт | `src/safewatch/types.py` | `class CameraPassport(BaseModel):` | `tests/test_contract_files.py::test_types_export_contract_names` |
| v5: поле `Video.web_playable` | 16 | плеер | `src/safewatch/types.py` | `web_playable: bool = False` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `Job.status_text` | 16 | очередь, загрузка | `src/safewatch/types.py` | `status_text: str = ""` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `Job.eta_s` | 16 | очередь | `src/safewatch/types.py` | `eta_s: float \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `EventSummary.clip` | 16 | лента, журнал, мастер | `src/safewatch/types.py` | `clip: Clip \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поля идентификации `EventSummary` | 16 | журнал, статистика | `src/safewatch/types.py` | `person_position: str = ""` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `EventDetail.can_identify` | 16 | экран события | `src/safewatch/types.py` | `can_identify: bool = False` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `auto_calibration` (`Analysis`, `CameraSetupView`) | 16 | экран настройки | `src/safewatch/types.py` | `auto_calibration: AutoCalibration \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `speed_source` (`PersonState`, `VehicleState`) | 16 | признаки, HUD | `src/safewatch/types.py` | `speed_source: SpeedSource = "relative"` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `HudObject.projection` | 16 | HUD | `src/safewatch/types.py` | `projection: list[Point] \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `Delivery.delivered_at` | 16 | экран события | `src/safewatch/types.py` | `delivered_at: datetime \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `ModelSpec.nc` | 16 | реестр, бэкенды | `src/safewatch/types.py` | `nc: int \| None = None` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: поле `ModelSpec.input_name` | 16 | бэкенды | `src/safewatch/types.py` | `input_name: str = "images"` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: `LogAction` `identified` | 16 | журнал действий | `src/safewatch/types.py` | `"identified"` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: `Channel.kind` `call` | 16 | экран IT | `src/safewatch/types.py` | `kind: Literal["ws", "webhook", "call"]` | `tests/test_contract_files.py::test_v5_fields_present` |
| v5: файл `contract/openapi.json` 1.1.0 | 16 | фронт Егора | `contract/openapi.json` | `"version": "1.1.0"` | `tests/test_contract_files.py::test_openapi_matches_app` |
| v5: конфиг, секции v5 | 16 | `config.py` | `src/safewatch/config.py` | `class AutocalConfig(_Section):` | `tests/test_config.py::test_v5_sections_load` |
| v5: `services.demo_import` | 17 | CLI `demo import`, `serve --seed` | `src/safewatch/services.py` | `def demo_import(` | `tests/test_demo_pack.py::test_import_creates_world_without_inference` |
| v5: `services.demo_build` | 17 | CLI `demo build` | `src/safewatch/services.py` | `def demo_build(` | `tests/test_demo_pack.py::test_build_writes_manifest_and_artifacts` |
| v5: `services.demo_packs` | 17 | `GET /api/demo/packs` | `src/safewatch/services.py` | `def demo_packs(` | `tests/test_demo_pack.py::test_import_is_idempotent` |
| v5: `services.artifact_import` | 17 | `demo_import`, CLI `import-artifact` | `src/safewatch/services.py` | `def artifact_import(` | `tests/test_demo_pack.py::test_import_creates_world_without_inference` |
| v5: `demo.read_manifest` | 17 | `demo_import` | `src/safewatch/demo.py` | `def read_manifest(` | `tests/test_demo_pack.py::test_build_writes_manifest_and_artifacts` |
| v5: `demo.write_manifest` | 17 | `demo_build` | `src/safewatch/demo.py` | `def write_manifest(` | `tests/test_demo_pack.py::test_build_writes_manifest_and_artifacts` |
| v5: CLI `demo` | 17 | владелец | `src/safewatch/cli.py` | `add_parser("demo"` | `tests/test_demo_pack.py::test_cli_build_and_import` |
| v5: `GET /api/demo/packs` | 17 | шапка, экран IT | `src/safewatch/api.py` | `@router.get("/api/demo/packs")` | `tests/test_demo_pack.py::test_import_is_idempotent` |
| v5: секция `demo` | 17 | `serve --seed` | `config/default.yaml` | `pack: data/demo/argus` | `tests/test_demo_pack.py::test_serve_autoloads_pack` |
| v5: пример раскладки | 17 | `demo build` | `config/demo.example.yaml` | `cameras:` | `tests/test_demo_pack.py::test_example_layout_is_valid` |
| v5: `texts.job_status_text` | 17 | `Job.status_text` | `src/safewatch/texts.py` | `def job_status_text(` | `tests/test_jobs.py::test_status_text_for_retry_and_failure` |
| v5: лента без демо-событий сида | 17 | `operator_feed`, состояния камер | `src/safewatch/store.py` | `is_demo = 0` | `tests/test_operator_views.py::test_feed_skips_seed_demo_events` |
| v5: `media.transcode` | 18 | `video_upload`, `video_import` | `src/safewatch/media.py` | `def transcode(` | `tests/test_clips.py::test_transcode_makes_browser_codec` |
| v5: константа `media.WEB_SUFFIX` | 18 | `transcode`, `video_file` | `src/safewatch/media.py` | `WEB_SUFFIX = ".web.mp4"` | `tests/test_clips.py::test_video_file_serves_web_copy` |
| v5: секция `clips` | 18 | `EventSummary.clip` | `config/default.yaml` | `pre_s: 3.0` | `tests/test_clips.py::test_clip_window_bounds` |
| v5: секция `transcode` | 18 | `media.transcode` | `config/default.yaml` | `preset: veryfast` | `tests/test_clips.py::test_transcode_disabled_key` |
| v5: фронт `ClipPlayer` | 18 | экран события, мастер | `frontend/src/components/ClipPlayer.tsx` | `export function ClipPlayer(` | `frontend/src/screens/screens.test.tsx::event_screen_plays_clip` |
| v5: `autocal.fit` | 19 | `analyze` | `src/safewatch/analysis/autocal.py` | `def fit(` | `tests/test_autocal.py::test_fit_recovers_height_line` |
| v5: `autocal.scale_at` | 19 | признаки | `src/safewatch/analysis/autocal.py` | `def scale_at(` | `tests/test_autocal.py::test_speed_auto_m_s_within_20pct` |
| v5: секция `autocal` | 19 | `autocal.fit` | `config/default.yaml` | `person_height_m: 1.7` | `tests/test_autocal.py::test_too_few_samples_not_ok` |
| v5: подписи HUD автокалибровки | 19 | `hud.build_hud` | `src/safewatch/texts.py` | `HUD_SPEED_M_AUTO = ` | `tests/test_autocal.py::test_hud_labels_auto_and_calibration` |
| v5: плагин `no_helmet` | 20 | `analyze` | `src/safewatch/rules/ppe.py` | `class HelmetPlugin:` | `tests/test_rule_ppe.py::test_no_helmet_in_zone_yellow_after_hold` |
| v5: плагин `no_respirator` | 20 | `analyze` | `src/safewatch/rules/ppe.py` | `class RespiratorPlugin:` | `tests/test_rule_ppe.py::test_respirator_model_missing_text` |
| v5: `rules.base.head_objects` | 20 | плагины СИЗ | `src/safewatch/rules/base.py` | `def head_objects(` | `tests/test_rule_ppe.py::test_head_unseen_unknown` |
| v5: параметры `scenarios.no_helmet` | 20 | `HelmetPlugin` | `config/default.yaml` | `head_frac: 0.35` | `tests/test_rule_ppe.py::test_no_helmet_in_zone_yellow_after_hold` |
| v5: тип зоны `helmet_required` | 20 | зоны, `HelmetPlugin` | `config/default.yaml` | `- id: helmet_required` | `tests/test_rule_ppe.py::test_outside_zone_no_event` |
| v5: тип зоны `respirator_required` | 20 | зоны, `RespiratorPlugin` | `config/default.yaml` | `- id: respirator_required` | `tests/test_rule_ppe.py::test_respirator_model_missing_text` |
| v5: текст `SCENARIO_MODEL_MISSING` | 20 | `scenario_metas` | `src/safewatch/texts.py` | `Модель не подключена: нужны классы {classes}` | `tests/test_rule_ppe.py::test_respirator_model_missing_text` |
| v5: реестр: каска Матвея | 20 | `registry` | `config/models.yaml` | `linq_program: mosprom_matvey_helmet_yolov8n_640-v1-5c3af1f3b855.tpu` | `tests/test_config.py::test_matvey_models_resolve` |
| v5: реестр: pose Матвея | 20 | `registry` | `config/models.yaml` | `linq_program: mosprom_matvey_pose_yolov8n_640-v1-acc5f51228b9.tpu` | `tests/test_config.py::test_matvey_models_resolve` |
| v5: пример включения моделей Матвея | 20 | владелец | `config/user.matvey.example.yaml` | `matvey-helmet-yolov8n@640-v1-5c3af1f3b855` | `tests/test_config.py::test_matvey_models_resolve` |
| v6: тип `services.Source` | 17 | `_infer`, `_enqueue`, `demo_import` | `src/safewatch/services.py` | `Source = tuple[BackendName, bool]` | `tests/test_demo_pack.py::test_import_creates_world_without_inference` |
| v6: `services._stage` | 17 | `video_import`, `demo_import` | `src/safewatch/services.py` | `def _stage(` | `tests/test_demo_pack.py::test_import_transcodes_outside_transaction` |
| v6: `services._web_copy` | 18 | `video_upload`, `_stage` | `src/safewatch/services.py` | `def _web_copy(` | `tests/test_clips.py::test_transcode_makes_browser_codec` |
| v6: `services._clip` | 18 | `_summary` | `src/safewatch/services.py` | `def _clip(` | `tests/test_clips.py::test_clip_window_bounds` |
| v6: pad нечётного кадра | 18 | `media.transcode` | `src/safewatch/media.py` | `pad=ceil(iw/2)*2:ceil(ih/2)*2` | `tests/test_clips.py::test_odd_frame_and_late_copy` |
| v6: константа `running.AUTOCAL_SAMPLES` | 19 | `RunningPlugin.explain` | `src/safewatch/rules/running.py` | `AUTOCAL_SAMPLES = "autocal_samples"` | `tests/test_autocal.py::test_hud_labels_auto_and_calibration` |
| v6: текст `AUTOCAL_ONE_ROW` | 19 | `autocal.fit` | `src/safewatch/texts.py` | `AUTOCAL_ONE_ROW = ` | `tests/test_autocal.py::test_too_few_samples_not_ok` |
| v5: compose с демо-пакетом | 21 | владелец, Docker | `docker-compose.yml` | `./data/demo:/app/data/demo:ro` | `tests/test_docker_files.py::test_compose_mounts_demo_and_data` |
| v10: SQLite в именованном томе | 21 | Docker | `docker-compose.yml` | `argus_data:/app/data/app` | `tests/test_docker_files.py::test_compose_mounts_demo_and_data` |
| v10: конфиг только при запуске | 21 | Docker | `docker-compose.yml` | `create_host_path: false` | `tests/test_docker_files.py::test_user_config_is_mounted_not_baked_and_env_keeps_priority` |
| v5: образ стартует с сидом | 21 | Docker | `Dockerfile` | `"--seed"` | `tests/test_docker_files.py::test_image_starts_with_seed_and_health` |
| v5: инструкция развёртывания | 21 | владелец | `docs/DEPLOY.md` | `docker compose up -d --build` | `вручную: docker compose up -d --build, GET /api/health` |
| v5: телефон разрешён в зонах | 22 | `PhonePlugin` | `src/safewatch/rules/phone.py` | `ALLOWED_KINDS = ("walkway", "rest")` | `tests/test_rule_phone.py::test_phone_allowed_in_walkway_and_rest` |
| v5: тип зоны `walkway` | 22 | зоны, `PhonePlugin` | `config/default.yaml` | `- id: walkway` | `tests/test_rule_phone.py::test_phone_allowed_in_walkway_and_rest` |
| v5: проекция груза в HUD | 22 | фронт | `src/safewatch/analysis/hud.py` | `projection=` | `tests/test_hud.py::test_suspended_load_projection` |
| v7: текст `HUD_LOAD_PROJECTION` | 22 | `hud.build_hud` | `src/safewatch/texts.py` | `HUD_LOAD_PROJECTION = ` | `tests/test_hud.py::test_suspended_load_projection` |
| v5: канал `CallChannel` | 23 | `deliveries_flush` | `src/safewatch/delivery.py` | `class CallChannel:` | `tests/test_delivery.py::test_call_stub_on_red_to_master` |
| v5: конфиг звонков | 23 | `deliveries_flush` | `config/default.yaml` | `provider: stub` | `tests/test_delivery.py::test_call_stub_on_red_to_master` |
| v5: очередь доставок в базе | 23 | `deliveries_flush` | `src/safewatch/store.py` | `FROM delivery_queue` | `tests/test_delivery.py::test_queue_survives_restart` |
| v5: фронт: маршрут `/m/operator` | 23 | навигация оператора | `frontend/src/nav.ts` | `path: "/m/operator"` | `frontend/src/screens/screens.test.tsx::operator_mobile_renders` |
| v5: фронт: маршрут `/m/operator/events/:eventId` | 23 | навигация оператора | `frontend/src/nav.ts` | `path: "/m/operator/events/:eventId"` | `frontend/src/screens/screens.test.tsx::operator_mobile_event_renders` |
| v5: фронт: экран `OperatorMobile` | 23 | `/m/operator` | `frontend/src/screens/operator/OperatorMobile.tsx` | `export function OperatorMobile(` | `frontend/src/screens/screens.test.tsx::operator_mobile_renders` |
| v5: фронт: экран `OperatorMobileEvent` | 23 | `/m/operator/events/:eventId` | `frontend/src/screens/operator/OperatorMobileEvent.tsx` | `export function OperatorMobileEvent(` | `frontend/src/screens/screens.test.tsx::operator_mobile_event_renders` |
| v7: `delivery.phone_mask` | 23 | `system_view` | `src/safewatch/delivery.py` | `def phone_mask(` | `tests/test_delivery.py::test_call_channel_in_system_view` |
| v7: `store.delivery_enqueue` | 23 | `broadcast_tick`, `event_action`, `escalation_tick` | `src/safewatch/store.py` | `def delivery_enqueue(` | `tests/test_delivery.py::test_queue_survives_restart` |
| v7: `store.delivery_dequeue` | 23 | `deliveries_flush` | `src/safewatch/store.py` | `def delivery_dequeue(` | `tests/test_delivery.py::test_queue_survives_restart` |
| v7: `services._delivery` | 23 | `event_detail` | `src/safewatch/services.py` | `def _delivery(` | `tests/test_delivery.py::test_call_stub_on_red_to_master` |
| v7: текст `CALL_DELIVERED_STUB` | 23 | `Delivery.status_text` | `src/safewatch/texts.py` | `CALL_DELIVERED_STUB = ` | `tests/test_delivery.py::test_call_stub_on_red_to_master` |
| v5: `calculator.rollout` | 24 | `calculator_rollout` | `src/safewatch/calculator.py` | `def rollout(` | `tests/test_calculator.py::test_rollout_three_tiers_formulas` |
| v5: `calculator.scale` | 24 | `calculator_scale` | `src/safewatch/calculator.py` | `def scale(` | `tests/test_calculator.py::test_scale_accelerators_from_measured` |
| v5: `services.calculator_defaults` | 24 | `GET /api/calculator/defaults` | `src/safewatch/services.py` | `def calculator_defaults(` | `tests/test_calculator.py::test_defaults_list_sources` |
| v5: `services.calculator_rollout` | 24 | `POST /api/calculator/rollout` | `src/safewatch/services.py` | `def calculator_rollout(` | `tests/test_calculator.py::test_rollout_three_tiers_formulas` |
| v5: `services.calculator_scale` | 24 | `POST /api/calculator/scale` | `src/safewatch/services.py` | `def calculator_scale(` | `tests/test_calculator.py::test_scale_accelerators_from_measured` |
| v5: `GET /api/calculator/defaults` | 24 | экран калькулятора Егора | `src/safewatch/api.py` | `@router.get("/api/calculator/defaults")` | `tests/test_calculator.py::test_defaults_list_sources` |
| v5: `POST /api/calculator/rollout` | 24 | экран калькулятора Егора | `src/safewatch/api.py` | `@router.post("/api/calculator/rollout")` | `tests/test_calculator.py::test_roles` |
| v5: `POST /api/calculator/scale` | 24 | экран калькулятора Егора | `src/safewatch/api.py` | `@router.post("/api/calculator/scale")` | `tests/test_calculator.py::test_roles` |
| v5: секция `calculator` | 24 | `calculator` | `config/default.yaml` | `- key: accelerator.capacity_fps` | `tests/test_calculator.py::test_overrides_and_unknown_key` |
| v7: пример `services.CALC_EXAMPLE` | 24 | `calculator_defaults` | `src/safewatch/services.py` | `CALC_EXAMPLE = RolloutIn(` | `tests/test_calculator.py::test_defaults_list_sources` |
| v7: `services.CALC_DIVISORS` | 24 | `_calc_assumptions` | `src/safewatch/services.py` | `CALC_DIVISORS = frozenset(` | `tests/test_calculator.py::test_overrides_and_unknown_key` |
| v7: текст `CALC_OVERRIDDEN` | 24 | `_calc_assumptions` | `src/safewatch/texts.py` | `CALC_OVERRIDDEN = ` | `tests/test_calculator.py::test_overrides_and_unknown_key` |
| v7: `store.linq_metrics` | 24 | `calculator_defaults`, `calculator_scale` | `src/safewatch/store.py` | `def linq_metrics(` | `tests/test_calculator.py::test_scale_accelerators_from_measured` |
| v7: `store.broadcast_event_counts` | 24 | `calculator_defaults`, `calculator_rollout` | `src/safewatch/store.py` | `def broadcast_event_counts(` | `tests/test_calculator.py::test_defaults_list_sources` |
| v5: `dataset.build_item` | 25 | `datasets_flush` | `src/safewatch/dataset.py` | `def build_item(` | `tests/test_dataset.py::test_item_files_and_label` |
| v5: `dataset.export_zip` | 25 | `dataset_export` | `src/safewatch/dataset.py` | `def export_zip(` | `tests/test_dataset.py::test_export_zip_manifest` |
| v5: `services.datasets_flush` | 25 | `worker` | `src/safewatch/services.py` | `def datasets_flush(` | `tests/test_dataset.py::test_false_alarm_creates_item_once` |
| v5: `services.datasets_view` | 25 | `GET /api/datasets/false-alarms` | `src/safewatch/services.py` | `def datasets_view(` | `tests/test_dataset.py::test_false_alarm_creates_item_once` |
| v5: `services.dataset_export` | 25 | CLI `dataset export`, API | `src/safewatch/services.py` | `def dataset_export(` | `tests/test_dataset.py::test_export_zip_manifest` |
| v5: `GET /api/datasets/false-alarms` | 25 | экран IT, Егор | `src/safewatch/api.py` | `@router.get("/api/datasets/false-alarms")` | `tests/test_dataset.py::test_false_alarm_creates_item_once` |
| v5: `GET /api/datasets/false-alarms/export.zip` | 25 | ML-часть | `src/safewatch/api.py` | `@router.get("/api/datasets/false-alarms/export.zip"` | `tests/test_dataset.py::test_export_zip_manifest` |
| v5: CLI `dataset` | 25 | ML-часть | `src/safewatch/cli.py` | `add_parser("dataset"` | `tests/test_dataset.py::test_cli_export` |
| v5: цикл датасета в `worker` | 25 | `api` lifespan | `src/safewatch/worker.py` | `datasets_flush` | `tests/test_worker.py::test_loop_periods_from_config` |
| v5: секция `datasets` | 25 | `datasets_flush` | `config/default.yaml` | `max_frames: 40` | `tests/test_dataset.py::test_item_files_and_label` |
| v7: `dataset.item_path` | 25 | `datasets_flush`, `build_item` | `src/safewatch/dataset.py` | `def item_path(` | `tests/test_dataset.py::test_item_files_and_label` |
| v7: константа `dataset.MANIFEST` | 25 | `export_zip` | `src/safewatch/dataset.py` | `MANIFEST = "manifest.json"` | `tests/test_dataset.py::test_export_zip_manifest` |
| v7: `store.dataset_pending` | 25 | `datasets_flush` | `src/safewatch/store.py` | `def dataset_pending(` | `tests/test_dataset.py::test_false_alarm_creates_item_once` |
| v7: `api.ZIP_FILE` | 25 | `GET /api/datasets/false-alarms/export.zip` | `src/safewatch/api.py` | `ZIP_FILE: dict[` | `tests/test_contract_files.py::test_openapi_only_grows` |
| v5: `services.event_identify` | 26 | `PATCH /api/events/{event_id}/identity` | `src/safewatch/services.py` | `def event_identify(` | `tests/test_identity.py::test_identify_writes_fields_and_history` |
| v5: `services.people_stats_view` | 26 | `GET /api/stats/people` | `src/safewatch/services.py` | `def people_stats_view(` | `tests/test_identity.py::test_people_stats_only_filled` |
| v5: константа `IDENTITY_MAX` | 26 | валидация | `src/safewatch/services.py` | `IDENTITY_MAX = 80` | `tests/test_identity.py::test_identify_limits` |
| v5: `PATCH /api/events/{event_id}/identity` | 26 | экран события Егора | `src/safewatch/api.py` | `@router.patch("/api/events/{event_id}/identity")` | `tests/test_identity.py::test_identify_roles` |
| v5: `GET /api/stats/people` | 26 | статистика Егора | `src/safewatch/api.py` | `@router.get("/api/stats/people")` | `tests/test_identity.py::test_people_stats_only_filled` |
| v5: `passport.build_passport` | 27 | `camera_passport` | `src/safewatch/analysis/passport.py` | `def build_passport(` | `tests/test_passport.py::test_verdicts_by_person_height` |
| v5: `services.camera_passport` | 27 | `GET /api/cameras/{camera_id}/passport` | `src/safewatch/services.py` | `def camera_passport(` | `tests/test_passport.py::test_no_analysis_unknown` |
| v5: `GET /api/cameras/{camera_id}/passport` | 27 | экран камеры Егора | `src/safewatch/api.py` | `@router.get("/api/cameras/{camera_id}/passport")` | `tests/test_passport.py::test_no_analysis_unknown` |
| v5: секция `passport` | 27 | `build_passport` | `config/default.yaml` | `person_partial_px: 80` | `tests/test_passport.py::test_dark_share_partial` |
| v5: `JupyterShell.close` | 28 | lifespan, doctor | `src/safewatch/inference/linq.py` | `def close(` | `tests/test_linq_backend.py::test_close_shuts_kernel` |
| v5: `services.backend_close` | 28 | lifespan, doctor | `src/safewatch/services.py` | `def backend_close(` | `tests/test_linq_backend.py::test_close_shuts_kernel` |
| v5: ключи `linq.reply_timeout_s`, `linq.slow_rtt_s` | 28 | `LinqBackend` | `config/default.yaml` | `slow_rtt_s: 12.0` | `tests/test_linq_backend.py::test_job_timeout_scales_with_frames` |
| v5: воркер LinQ: аргумент `--reply-timeout` | 28 | `LinqBackend` | `tools/linq/remote/video_worker.py` | `"--reply-timeout"` | `tests/test_linq_backend.py::test_reply_timeout_passed` |
| v5: старт гасит прежний воркер | 28 | `LinqBackend` | `src/safewatch/inference/linq.py` | `def _start_command(` | `tests/test_linq_backend.py::test_start_kills_previous_worker` |
| v5: текст прогресса задачи | 28 | `Job.status_text` | `src/safewatch/texts.py` | `JOB_PROGRESS = ` | `tests/test_linq_backend.py::test_eta_and_rate_text` |
| v5: CLI `import-artifact` | 29 | ML-часть | `src/safewatch/cli.py` | `add_parser("import-artifact"` | `tests/test_ml_gaps.py::test_import_artifact_cli_and_cache` |
| v5: ключ `pipeline.vehicle_classes` | 29 | `analyze`, `proximity` | `config/default.yaml` | `vehicle_classes: [car, bus, truck, train]` | `tests/test_ml_gaps.py::test_vehicle_classes_from_config` |
| v5: ключ `local.providers` | 29 | `LocalBackend` | `config/default.yaml` | `providers: [CPUExecutionProvider]` | `tests/test_ml_gaps.py::test_local_providers_key` |
| v5: имя входа модели | 29 | `LinqBackend` | `src/safewatch/inference/linq.py` | `--input-name` | `tests/test_ml_gaps.py::test_input_name_passed` |
| v5: `report_pdf.shift_pdf` | 30 | `shift_report_pdf` | `src/safewatch/report_pdf.py` | `def shift_pdf(` | `tests/test_shift_pdf.py::test_pdf_has_cyrillic_summary` |
| v5: `services.shift_report_pdf` | 30 | `GET /api/master/shift.pdf` | `src/safewatch/services.py` | `def shift_report_pdf(` | `tests/test_shift_pdf.py::test_pdf_has_cyrillic_summary` |
| v5: `GET /api/master/shift.pdf` | 30 | мастер, Егор | `src/safewatch/api.py` | `@router.get("/api/master/shift.pdf"` | `tests/test_shift_pdf.py::test_pdf_route_and_bad_at` |
| v5: шрифт PDF | 30 | `report_pdf` | `src/safewatch/report_pdf.py` | `FONT = "DejaVuSans.ttf"` | `tests/test_shift_pdf.py::test_pdf_has_cyrillic_summary` |
| v5: ключ `tracker.reattach_bh` | 30 | `Tracker` | `config/default.yaml` | `reattach_bh: 1.0` | `tests/test_tracking.py::test_fall_keeps_track_id` |
| v7: `api.PDF_FILE` | 30 | `GET /api/master/shift.pdf` | `src/safewatch/api.py` | `PDF_FILE: dict[` | `tests/test_contract_files.py::test_openapi_only_grows` |
| v8: текст `IDENTITY_TOO_LONG` | 26 | `event_identify` | `src/safewatch/texts.py` | `IDENTITY_TOO_LONG = ` | `tests/test_identity.py::test_identify_limits` |
| v8: `texts.identity_comment` | 26 | `event_identify` | `src/safewatch/texts.py` | `def identity_comment(` | `tests/test_identity.py::test_identify_writes_fields_and_history` |
| v8: `services._stats_period` | 26 | `ohs_stats_view`, `people_stats_view` | `src/safewatch/services.py` | `def _stats_period(` | `tests/test_identity.py::test_people_stats_only_filled` |
| v8: `passport.ZONE_REQUIRED` | 27 | `build_passport` | `src/safewatch/analysis/passport.py` | `ZONE_REQUIRED = (` | `tests/test_passport.py::test_zone_missing_partial` |
| v8: текст `PASSPORT_SUITABLE` | 27 | `build_passport` | `src/safewatch/texts.py` | `PASSPORT_SUITABLE = ` | `tests/test_passport.py::test_verdicts_by_person_height` |
| v8: `linq.job_timeout_s` | 28 | `LinqBackend` | `src/safewatch/inference/linq.py` | `def job_timeout_s(` | `tests/test_linq_backend.py::test_job_timeout_scales_with_frames` |
| v8: `linq.rate_eta` | 28 | `services._job` | `src/safewatch/inference/linq.py` | `def rate_eta(` | `tests/test_linq_backend.py::test_eta_and_rate_text` |
| v8: `services._live` | 28 | `services._job` | `src/safewatch/services.py` | `_live: dict[int, tuple[int, int, float]] = {}` | `tests/test_linq_backend.py::test_eta_and_rate_text` |
| v8: текст `JOB_WAIT_TPU` | 28 | `Job.status_text` | `src/safewatch/texts.py` | `JOB_WAIT_TPU = ` | `tests/test_linq_backend.py::test_eta_and_rate_text` |
| v8: `rules.ANY_VEHICLE` | 29 | `scenario_metas` | `src/safewatch/rules/__init__.py` | `ANY_VEHICLE = {"proximity"}` | `tests/test_ml_gaps.py::test_proximity_any_vehicle` |
| v8: метрики extra в `store._JOBS` | 29 | `services._job` | `src/safewatch/store.py` | `AS extra_metrics` | `tests/test_ml_gaps.py::test_extra_metrics_in_job` |
| v8: откат extra в `eval_run` | 29 | `safewatch eval` | `src/safewatch/services.py` | `"eval: %s, extra %s: %s"` | `tests/test_eval.py::test_eval_extra_fallback` |
| v8: `services.video_upload_check` | 30 | `api._UploadGuard` | `src/safewatch/services.py` | `def video_upload_check(` | `tests/test_videos.py::test_upload_rejected_before_body` |
| v8: `api._UploadGuard` | 30 | `create_app` | `src/safewatch/api.py` | `class _UploadGuard:` | `tests/test_videos.py::test_upload_rejected_before_body` |
| v8: `cli._server_running` | 30 | `cli.evaluate` | `src/safewatch/cli.py` | `def _server_running(` | `tests/test_eval.py::test_eval_refuses_running_server` |
| v8: текст `EVAL_SERVER_RUNNING` | 30 | `cli.evaluate` | `src/safewatch/texts.py` | `EVAL_SERVER_RUNNING = ` | `tests/test_eval.py::test_eval_refuses_running_server` |
| v8: `services.shift_report_name` | 30 | `GET /api/master/shift.pdf` | `src/safewatch/services.py` | `def shift_report_name(` | `tests/test_shift_pdf.py::test_pdf_route_and_bad_at` |
| v8: текст `WHY_FENCE` | 30 | `FencePlugin.explain` | `src/safewatch/texts.py` | `WHY_FENCE = ` | `tests/test_rule_proximity.py::test_explain_has_units` |
| v8: `Tracker._reattach` | 30 | `Tracker.update` | `src/safewatch/analysis/tracking.py` | `def _reattach(` | `tests/test_tracking.py::test_fall_keeps_track_id` |
| v8: PDF смены в `asyncio.to_thread` | 30 | `GET /api/master/shift.pdf` | `src/safewatch/services.py` | `async def shift_report_pdf(` | `tests/test_shift_pdf.py::test_pdf_has_cyrillic_summary` |
| v5: `media.frame_shift` | 32 | паспорт камеры | `src/safewatch/media.py` | `def frame_shift(` | `tests/test_camera_shift.py::test_shift_detected_above_threshold` |
| v5: секция `shift` | 32 | `camera_passport` | `config/default.yaml` | `max_px: 20` | `tests/test_camera_shift.py::test_shift_detected_above_threshold` |

### 6.8 Дополнения v2 (строки `GAP` S0–S5 и решения R5)

Перенесены ревью R5 из `## open` файла `progress.md`. Эти имена и формы — часть контракта наравне с 6.1–6.6. Строка: `<слайс>, <что>, <точная форма>`; `было → стало` заменяет сказанное выше.

**5.2 Типы**

- S5, `AnalysisConfig.duration_ms: int` (= `videos.duration_ms`, конец эпизода `video_end`; тип внутренний, в openapi его нет).

**6.1 Бэкенды инференса и фейк**

- S2, `LinqBackend` (8.1): «хвост лога содержит `status -3` или `not readable` → `model_missing`» → «только `not readable` → `model_missing`»: лог фейка `remote_error` по 6.1 содержит `status -3` и обязан давать `remote_error`.
- S2, `LinqBackend`: `.progress` не JSON, пока воркер `RUNNING`, — повтор опроса (воркер переписывает файл на месте), `bad_output` только при `STOPPED`; `--classes` ставится по `model.task == "detect"` (S10 отличит `pipeline.extra`); `upload_s` — проверка размера и загрузка видео; `remote_out` с раскрытым `$HOME` из `# sw:home`; `LinqBackend.check()` → `NotImplementedError("slice 3")`; `WORKER_FILES`, `_load_module(path)`.
- S2, `inference.make_backend` с `local` → `NotImplementedError("slice 3")`; `config.Settings.inference_backend = Field(default="linq", validation_alias="INFERENCE_BACKEND")` (искомая строка 6.7).
- S2, `FakeRemoteShell`: сцена `auto` берёт исходное имя через `store.video_filename(<стем uploads/<sha256><ext>>)`, иначе имя локального файла (закрывает заметку R5 от S0).
- S3, `LinqBackend.check`: `present` — найденные программы активных моделей, `missing` — недостающие программы и пути хвостов; любая `InferenceError` → `unreachable`; код возврата `ls` не проверяется (нет папки — все программы в `missing`); `latency_ms` — время `# sw:check`; помощник `_finish(status, state, text, names=None)`.
- S3, `LocalBackend`: `PROGRESS_EVERY = 25`, `_yolo_io(tools_dir)` (импорт по пути), `fake=False` в метриках и статусе, нет видео → `video_unreadable`, `check()`: `ok`/`models_missing` по файлам `local_onnx` активных моделей, текст `LOCAL_*`.

**6.2 Фасад `services`**

- S1, константы `services` вне 6.6: `ROLE_ACTIONS: dict[Role, list[HumanAction]]` (таблица прав 6.2), `TERMINAL_STATUSES: frozenset[EventStatus]` (8.6), `LEVEL_COLORS: dict[Level, str] = {"yellow": "#FFC400", "red": "#FF3B30"}` (цвета темы 8.14 для `LevelMeta.color`).
- S1, `sector_delete` сектора, на который ссылаются только удалённые камеры или события (FK, у секторов нет `deleted_at`): 409 `sector_not_empty` с текстом `texts.SECTOR_HAS_HISTORY` вместо 204.
- S2, `services` вне 6.2: `analysis_step(fps) -> int` (шаг 8.1), `ERROR_TEXT_MAX = 500`, `RETRYABLE: frozenset[JobErrorCode]`, ленивый `_backend` (сбрасывает фикстура `conn`); `Job.metrics` строится из `artifacts.metrics_json` задачи, `cached = artifacts.created_at < jobs.started_at`; повторная загрузка `failed`-видео ставит видео в `uploaded`; без `pipeline.pose` стадия pose пропускается.
- S3, `services`: `RECENT_JOBS = 20`; синглтон `_backend_status: BackendStatus | None` (последняя реальная проверка, сбрасывает фикстура `conn`), `_unchecked()`; кэш живёт, пока `now - checked_at < linq.check_cache_s` (ровно на границе — новая проверка); `job_retry` ставит `stage=queued`, `progress=0`, `attempts=0`, чистит `error_*`, `next_attempt_at`, `finished_at`, видео → `uploaded`, шлёт `job.progress`; `recover_jobs` меняет только `status`.
- S5, `services`: `_enqueue(video_id, kind: JobKind = "process")`, `_evidence`, `_evidence_files`, `_stored_artifact`, `_analysis_inputs(video)` (артефакты активного анализа; нет строки или файла → `None`: `video_recompute` 409 `artifacts_missing`, задача `recompute` → `failed`, `artifacts_missing`); задача `recompute` берёт модели из строк `artifacts` (`model_id@model_version`), не из `pipeline`; `_analyze` возвращает `(эпизоды с id, hud)`; `video_recompute`: роль (admin, ohs) → 404 → 409 `video_not_ready` (статус не `ready` или нет активного анализа) → 409 `artifacts_missing`; `evidence_file`: нет строки или файла → 404.

**6.2 Хранилище `store` и помощники слоёв**

- S0, помощники вне 6.x: `store.conn()` (ленивое соединение живёт в `store._conn`, а не в `services`), `store.insert(table, values) -> int`, `store.demo_world_exists()`, `store.demo_counts()`, `store.demo_cameras()`; `seed.seed_demo() -> SeedReport` и `seed.demo_camera_ids()` (фасад `services.seed_demo` зовёт их); `config.ENV_NAMES: dict[str, str]` (имя ключа `.env` для doctor); `cli.contract_texts() -> dict[str, str]`; `fakes.remote.auto_scene(filename) -> str`; `hub.Client` (`role`, `queue`, `dropped`); `services.ACTOR_MAX` объявлена в S0 (её читает `api`).
- S1, `store`: `sectors()`, `sector(id)`, `sector_name_taken(name, except_id=None) -> bool`, `sector_update(id, name, sort_order)`, `sector_has_cameras(id) -> bool`, `sector_delete(id)`, `cameras(sector_id=None)` и `camera(id)` (строки без удалённых, с `has_calibration`, `zones_count`, `videos_count` одним запросом), `camera_update(id, values: dict)`, `camera_delete(id, at)` (`deleted_at` и `playing`-эфир → `stopped`); в `services` приватные `_require(role, allowed)`, `_name`, `_description`.
- S2, `store`: `video`, `video_by_sha`, `video_filename(sha256)`, `videos`, `video_update`, `job`, `jobs(status, limit)`, `camera_jobs`, `video_last_job`, `next_job(now)`, `job_update`, `job_progress` (прогресс не убывает), `artifact`, `artifact_update`; `cli.import_video(path, camera_id) -> int`.
- S3, `store`: `queue_jobs()` (`queued`, `running`, `retry_wait` по `created_at`), `finished_jobs(limit)` (`done`, `failed` по `finished_at` убыв.), `jobs_recover() -> int`.
- S4, `store`: `artifact_path(artifact_id) -> str`, `analysis_next_version(video_id) -> int`, `analysis(analysis_id)`; `services._analyze(job_id, video, det, pose)` и `_analysis_files(...)` (поток: чтение артефактов, `analyze`, запись `hud.jsonl`); `video_tracks`: сначала 404, потом 422 (`field="to_ms"`), потом 409; `analyses.duration_ms` = длительность видео.
- S5, `store`: `artifact_by_id`, `episodes(analysis_id)`, `analysis_evidence(analysis_id)`, `evidence(evidence_id)`.

**6.3 CLI и doctor**

- S3, `doctor._linq_check(settings)`: без `LINQ_JUPYTER_URL` или `LINQ_JUPYTER_USER` — FAIL «нет ключей» без `backend_check` (с пустым URL `JupyterShell` падает не сетевой ошибкой); строка `связь с LinQ: <state>` с `BackendStatus.message`; `serve` печатает число возвращённых в очередь задач.

**6.4 REST**

- S0, тело ошибок в OpenAPI, `router = APIRouter(responses={"4XX": {"model": ApiError}, 501: {"model": ApiError}})`: схема `ApiError` попала в `contract/openapi.json` и `schema.d.ts` (иначе фронт не знает тела ошибки; 4XX заменяет `HTTPValidationError` у 422).

**6.6 Константы и тексты `texts.py`**

- S0, `texts.py` сверх 7: `SCENARIO_TITLES: dict[str, str]` (названия 8.3, плагины S5/S10 берут отсюда), `PRODUCT_TITLE`, `REQUEST_INVALID`, `ROLE_REQUIRED`, `ACTOR_INVALID`, `NOT_IMPLEMENTED = "Функция появится в слайсе {slice}"`, `VIDEOS_DIR_MISSING`, `DEMO_SECTORS`, `DEMO_CAMERAS`, `DEMO_ZONE_NAMES`, `DEMO_REASONS`, `DEMO_RESOLVE_COMMENTS`.
- S1, `texts.py`: `FORBIDDEN_ROLE`, `NAME_INVALID`, `DESCRIPTION_INVALID`, `SECTOR_NOT_FOUND`, `CAMERA_NOT_FOUND`, `SECTOR_NAME_TAKEN`, `SECTOR_NOT_EMPTY`, `SECTOR_HAS_HISTORY`.
- S2, `texts.py`: `VIDEO_EXTENSION`, `VIDEO_UNREADABLE`, `VIDEO_TOO_LARGE`, `VIDEO_NOT_FOUND`, `FILE_NOT_FOUND`, `JOB_NOT_FOUND`, `LIMIT_INVALID`.
- S3, `texts.py`: `JOB_NOT_FAILED`, `BACKEND_UNCHECKED`, `BACKEND_FAKE = "Фейк: детекции синтетические. {text}"` (префикс сообщения фейка), `LINQ_OK`, `LINQ_UNREACHABLE`, `LINQ_MODELS_MISSING`, `LINQ_BAD_ANSWER`, `LOCAL_OK`, `LOCAL_MODELS_MISSING`.
- S4, `texts.py`: `HUD_SPEED_BH`, `HUD_RUN_BH`, `HUD_LYING`, `HUD_STILL`, `HUD_FEET_HIDDEN`, `HUD_TOO_SMALL`, `OBJECT_LABELS: dict[str, str]` (класс → подпись, нет ключа → имя класса), `VIDEO_NOT_READY`, `TRACKS_WINDOW_INVALID`.
- S5, `texts.py`: `SCENARIO_DESCRIPTIONS`, `SCENARIO_ACTIVE`, `SCENARIO_MODEL_MISSING`, `PARAM_TITLES: dict[str, tuple[str, str]]` (ключ → подпись, единица), `RUN_BH`, `RUN_M`, `IN_ZONE`, `NEAR_VEHICLE`, `FALL_SEEN`, `LYING_STILL`, `IN_REPAIR_ZONE`, `WHY_RULE`, `WHY_RUN_BH`, `WHY_RUN_M`, `WHY_FALL`, `WHY_LYING`, `WHY_METHOD`, `WHY_CONFIDENCE`, `WHY_UNCERTAIN`, `WHY_SECONDS`, `METHOD_TITLES`, `METRIC_TITLES`, `EVIDENCE_NOT_FOUND`, `ARTIFACTS_MISSING`.

**Компоненты анализа, реестра и правил (разделы 7, 8.2–8.4)**

- S0, `registry.resolve(ref: str, models: list[ModelSpec] | None = None) -> ModelSpec` (необязательный список, чтобы не читать yaml на каждую ссылку); `registry.MODELS_FILE`.
- S2, `media.VideoProbe` (pydantic: `width`, `height`, `fps`, `frame_count`, `duration_ms`, `codec`, `browser_playable`) и `media.probe_video(path) -> VideoProbe | None` (`None` — видео не читается); `media.CODEC_ALIASES = {"fmp4": "mp4v"}`: OpenCV отдаёт для mp4v имя FFmpeg `FMP4`, без замены критерий `codec = "mp4v"` не выполним.
- S4, `analysis.pipeline.analyze` берёт секции `tracker`, `pose`, `features` и порог `scenarios.running.speed_bh_s` (жёлтая подпись скорости) из `config.get_settings()`: в `AnalysisConfig` их нет; параметр `config` сохранён по 8.2, модуль импортирован как `app_config`; `VEHICLES = ("car", "bus", "truck", "train")`; `pose_used = pose is not None`.
- S4, `Tracker(cfg: TrackerConfig, ids: itertools.count[int])`, `Tracker.update(ts_ms, dets) -> list[tuple[int, Detection]]` (подтверждённые и сопоставленные в кадре); id выдаётся при подтверждении (предварительный трек без id), открывающая детекция — первое попадание; трек живёт, пока `ts − last_seen ≤ max_lost_s` (ровно 1,0 с — прежний id).
- S4, `features.History = dict[int, list[tuple[int, PersonState]]]`, `features.attach_keypoints(boxes, poses, match_iou) -> dict[int, list[Keypoint]]` (индекс рамки → точки), `features.person_states(tracks, kpts, ts_ms, frame_height, history, cfg, kpt_conf) -> list[PersonState]` (дописывает кадр в `history`); `ANKLES`, `SHOULDERS_HIPS`, `FRAME_EDGE_PX = 2`; H_ref до первой вертикальной позы — текущая высота, в позе `lying` — прежний, нет вертикальных точек в окне — прежний.
- S4, `hud.build_hud(ctx: FrameContext, run_bh_s: float, cfg: FeaturesConfig) -> HudFrame`; скорость `speed_bh_s ≥ run_bh_s` → «бег <v> роста/с», `yellow` (как у правила `running`), иначе «<v> роста/с» без уровня; «неподвижен» при `ts − still_since > still_after_s`; координаты обрезаются в [0, 1]; подписи наблюдений `P` придут с плагинами S5.
- S5, `hud.build_hud(ctx, run_bh_s, cfg)` → `build_hud(ctx, run_bh_s, cfg, observations: list[Observation])` (тег `code=<scenario>`, текст причины и уровень на каждое `P` у человека `track:<id>`).
- S5, `EpisodeManager(cfg: EpisodesConfig)`, `update(frame_idx, ts_ms, observations)`, `finish(duration_ms) -> list[EpisodeDraft]` (по `start_ms`); `U` = нет наблюдения; слияние смены id — только с подтверждённым эпизодом, по `anchor` и `ref_height_px` его последнего `P`; удержание красного для эскалации сбрасывает любой кадр без красного `P`; `uncertain_ms` копится покадрово (ts − ts прошлого кадра); `{duration_s}` подставляется при выдаче черновика.
- S5, `rules`: `defaults(scenario) -> dict[str, float]`, `scenario_metas(active_classes: list[str] | None = None)` (снимок анализа; `None` → `registry.active_classes`); статус `skeleton` и «любой класс» для `fire_smoking` — в S10; `rules/base.py`: `param(key, lo, hi) -> ScenarioParam` (`default` ставит `scenario_metas`), `obs(scenario, person, state, *, level, hold_s, reason_code, reason_text, method, metrics, zone_id) -> Observation` (субъект `track:<id>`, `confidence` = score), `why_common(episode) -> list[WhyItem]`; `RunningPlugin`, `FallPlugin` с `ID`, `running.DANGER_KINDS`; `reason_code`: `running`, `running_zone`, `running_vehicle`, `fall`, `lying_still`, `lying_still_allowed`; `method`: running `relative`/`calibrated`, fall — `posture_method`.
- S5, `fall`: «человек меньше `features.min_person_px`» → `ref_height_px < min_person_px` (рамка лежащего низкая по природе), порог из `config.get_settings()`.
- S5, `geometry.point_rect_distance(p, box) -> float`, `point_segment_distance(p, a, b) -> float`; `ioa` не написан (потребитель — S10).
- S5, `media.read_frame(path, frame_idx) -> np.ndarray` (кадр не читается → `ValueError` → задача `internal`), `media.encode_jpeg(img, quality, max_width) -> bytes`.

**Фронт (разделы 7, 8.14)**

- S0, фронт: `WsMessage` в `src/api/ws.ts` — свой тип `{type, at, data: unknown}` (WS-схемы нет в openapi); `useMeta()` и контекст `/api/meta` в `components/AppShell.tsx` (бейджи и переключатель роли берут названия из meta); `roles.ts` ещё экспортирует `ROLES`, `getRole`, `setRole`.
- S1, фронт: `Modal({title, onClose, children})`, `FormField({label, children})`, `FormModal({title, error, submitText, onSubmit, onClose, children})` (форма в модалке с текстом ошибки API), `ConfirmDialog({text, error, onConfirm, onClose})`; `NavItem.screen?: ComponentType` в `nav.ts`, `App.tsx` рендерит `screen` вместо `StubNotice`; `DataTable` — generic-перегрузка над негенерик-реализацией.
- S2, фронт: `uploadVideo(cameraId, file, onProgress)` в `src/api/client.ts` (XMLHttpRequest: у fetch нет прогресса загрузки).
- S3, фронт: бейдж `data-testid="backend-state"` в `AppShell` (по WS `backend.status`, текст `message`, иконка ●/▲), `SystemScreen` подключён в `nav.ts`; `App.test.tsx` подменяет `WebSocket` в `beforeEach`.
- S4, фронт: `DrawOp` (`rect`, `label`, `path`), `Size`, `CHAR_W`, `LINE_H`, `PAD` в `components/hud.ts`; `HudCanvas({ops, size})` (размер холста нужен, ops в пикселях); `videoUrl(videoId)` в `src/api/client.ts`; `VideoWithHud` берёт окна `/tracks` по 5000 мс; клавиша H (и Р в русской раскладке).
- S5, фронт: `apiUrl(path)` в `src/api/client.ts` (URL сервера для `Evidence.url`); блок `Episodes` внутри `CameraSetup.tsx`; `EvidenceImage` в S5 — миниатюра с подписью (время, число объектов), рамка и выноска — S7.

**Решения R5**

- `PUT /api/sectors/{id}` заменяет сектор целиком по `SectorIn` (`sort_order` по умолчанию 0): так требуют 6.4 и 5.2, фронт шлёт `sort_order` всегда.
- `PATCH /api/cameras/{id}` пропускает поля со значением `null`: поля `CameraPatch` в 5.1 `NOT NULL`, очистка описания — пустая строка `""`.
- 8.1, `model_missing`: только хвост лога с `not readable` (ошибка LinQ `-3 … TPU program file is not readable`, `docs/linq/LINQ_CONTRACT.md`); голый `status -3` (лог фейка `remote_error` в 6.1) → `remote_error`. Текст 8.1 исправлен.
- 8.2, HUD: жёлтая подпись скорости при `speed_bh_s ≥` порога `scenarios.running.speed_bh_s`, как у правила `running` (8.3). Текст 8.2 исправлен.
- doctor без `LINQ_JUPYTER_URL` или `LINQ_JUPYTER_USER`: FAIL «нет ключей», `backend_check` не вызывается (с пустым URL `JupyterShell` падает не сетевой ошибкой). Принято.
- `api.py` кроме `services` и `hub` импортирует `worker` (lifespan, слайс 0), `clock` (время `hello` в `/ws`) и `registry` (`active_models` при старте `create_app`). Допустимо.
- `worker.run_forever`: исключение шага пишется в лог (`job loop`), цикл ждёт `jobs.idle_poll_ms` и продолжает; `_video_row` в `run_next_job` внутри `try` (задача не остаётся `running`).
- `JupyterShell._drop()`: сетевая ошибка или `JupyterError` сбрасывают сессию (`shutdown_kernel` без гарантий), следующий вызов входит заново и открывает новый kernel.
- `tools/linq/remote/video_worker.py` перед первым кадром пишет в stderr (`<out>.log`) строку `{"input_queue": {"messages", "consumers"}, "uri": <program_uri>}`; `TimeoutError` из `TpuClient.collect` оканчивается `unmatched replies <n>` (`TpuClient.unmatched` — ответы без известного id).

---

### 6.9 Дополнения v3 (строки `GAP` S6–S10 и решения R10)

Перенесены ревью R10 из `## open` файла `progress.md`. Статус тот же, что у 6.8: часть контракта наравне с 6.1–6.6; `было → стало` заменяет сказанное выше.

**5.2 Типы**

- R10, `AnalysisConfig.extra_artifact_ids: list[int] = []` — артефакты моделей `pipeline.extra` этого анализа (схема 5.1 не меняется: ссылки живут в `analyses.config_json`); задача `recompute` берёт их отсюда, нет строки или файла → `artifacts_missing`, как у детектора. Старый снимок без поля — пересчёт без extra.

**6.1 Бэкенды инференса и фейк**

- S10, модели `pipeline.extra`: проход каждой модели — сразу после детектора, стадия `inference_detect`, доля 0,45; `LinqBackend` и `LocalBackend` узнают модель extra по `id@version` в `pipeline.extra`: `--nc len(classes)` без `--classes` (local: `nc = len(classes)`, `classes=None`); `FakeRemoteShell` с `--nc` отдаёт кадры без детекций (сцены в id COCO); `Job.metrics` по-прежнему только детектор и pose (колонок для extra в `jobs` нет).

**6.2 Фасад `services`**

- S6, `services` вне 6.2: `PRIORITY = {"red_pending": 3, "yellow_pending": 2, "open": 1, "terminal": 0}` и `_priority(level, status)`; синглтоны `_camera_seen: dict[int, CameraState]`, `_sector_seen: dict[int, SectorState]`, `_preview_cache: dict[int, tuple[datetime, bytes]]` (сбрасывает фикстура `conn`); помощники `_broadcast`, `_broadcast_by_id`, `_broadcast_insert`, `_stop_playing`, `_autostart`, `_play`, `_summary`, `_event_summary`, `_system_action`, `_operator_alert`, `_camera_state`, `_sector_state`, `_sector_states`, `_feed`; `broadcast_tick` возвращает число записанных действий (`published`, `level_escalated`, `auto_finished`); `Notification.id = "e<event>:published|escalated"`.
- S6, эфир: `broadcast_get` и поле `broadcast` у `CameraTile`, `CameraLiveView`, `CameraSetupView` — играющий эфир камеры, иначе последний любого статуса, иначе `null`; `broadcast_start` с чужим или несуществующим `video_id` → 404 `not_found`, `ready` без `active_analysis_id` → 409 `video_not_ready`; остановленный при старте эфир шлёт свой `broadcast.state` (`stopped`); `broadcast_stop` без играющего эфира → 204 без сообщения; `camera_delete` шлёт `broadcast.state` остановленного эфира.
- S6, лента: «терминальные за последние `recent_closed_min`» — по времени последнего действия события (`max(event_actions.at)`); жёлтое, опубликованное уже закончившимся (догоняющий тик), сразу получает `ended_at` и по 8.5 дословно не получает `auto_finished`.
- S6, превью: кадр `round(position_ms / 1000 × fps)` играющего эфира, иначе кадр 0 последнего `ready` видео; JPEG `evidence.jpeg_quality`, ширина `preview.max_width`; `CameraTile.preview_url` есть при `videos_count > 0`; `CameraState.freshness_ms = None` до S11.
- S7, `services` вне 6.2: `VERDICTS: dict[HumanAction, Verdict]`, `Step = tuple[LogAction, EventStatus]`, `_steps(action, row) -> list[Step] | None` (человеческие строки 8.6; `None` — пары нет), `_event_row(id)`, `_provenance(episode)`, `_evidence_item(row)` и `_episode(row, evidence)` (общие с `video_analysis`).
- S7, журнал действий: `confirm` красного пишет две строки цепочкой — `confirmed` (`<статус> → confirmed`), затем `sent_to_master` (`confirmed → sent_to_master`); `confirm` после таймаута — `confirmed` (`sent_to_master → sent_to_master`); комментарий — в первой строке действия, хранится обрезанным, длина `COMMENT_MAX` считается до обрезки; `actor_name` — обрезанный `X-Actor` или `texts.DEMO_ACTOR[role]`, длину проверяет только `services` (`ValidationFailed`, поле `X-Actor`).
- S7, порядок проверок `event_action`: роль (400, 403 по `ROLE_ACTIONS`) → комментарий (422) → имя (422) → 404 → 409; `event.updated` на любое действие, включая `view`; уведомление мастеру (8.8, строка 3) — при переходе в `sent_to_master` (оператором и в `escalation_tick`); `confirm`/`false_alarm` после таймаута — только `event.updated`.
- S7, `event_detail`: `provenance.backend`/`fake` — из артефакта детектора анализа; `rule_params` = `rules.defaults(scenario) | effective` правила камеры из снимка `AnalysisConfig.rules`; `why` = `explain` плагина над `EpisodeDraft` эпизода (`confirm_frame_idx`/`escalate_frame_idx` из кадров доказательств); демо-событие: `why = [WhyItem("Причина", reason_text)]`, `provenance` пустой (`fake=false`, `rule_params={}`); `broadcast` — `store.camera_broadcast` камеры события (у удалённой камеры не 404); без роли `allowed_actions = []`; `deliveries = []` до S15.
- S7, S8, уведомления мастеру: `_master_alert(summary, kind="to_master")` (`Notification.id = "e<event>:<kind>"`, аудитория `master`, `chime`, без захвата); строка 4 таблицы 8.8: `level_escalated` в `broadcast_tick` у события в `sent_to_master`/`master_accepted` шлёт мастеру `Notification.id = "e<event>:master_escalated"` (сирена оператору остаётся).
- S8, `services` вне 6.2: `_shift_window(at) -> (id, title, start, end)`, `_count_rows(events, key, titles) -> list[CountRow]`.
- S8, `shift_summary_view`: `at` без часового пояса считается UTC; `start`/`end` в UTC; смена с `end <= start` идёт через полночь; `CountRow.key` сектора — `str(sector_id)`, строки по убыванию `count`, затем по `title`; `confirmed`/`false_alarm` — по `operator_verdict`; `events` — события с `operator_verdict = confirmed` по `started_at`; демо-события считаются (флага нет), `superseded` нет.
- S8, входящие мастера: «по времени передачи» — новые передачи первыми; `recent_resolved` включает демо-события сида.
- S9, `services` вне 6.2: `WORLD_MIN_AREA = 0.01`, `_in_frame(points, field)`, `_collinear(points, min_area)`, `_rmse(h, pairs)`, `_calibration(row)`, `_calibration_of(camera_id)` (без проверки камеры: снимок анализа), `_zone(row)`, `_zone_name`, `_zone_points(kind, points) -> str`, `_zone_row(zone_id)`, `_rules(camera_id, rows, metas) -> list[CameraRule]`, `_range(x)`, `_recomputed(video_id) -> (id событий superseded, [остановленный, новый эфир])`; `_system_action(..., comment="")`.
- S9, валидация: калибровка — число точек кадра (`image_points`) → число мировых равно (`world_points`, `CAL_POINTS_MISMATCH`) → контрольных до 8 (`CAL_CONTROL_MAX`) → точки кадра и контрольные в [0, 1] → коллинеарность (`image_points`); `fit_rmse_m`, `control_rmse_m` — СКО расстояния в метрах; `PUT` заменяет калибровку целиком, `DELETE` без калибровки — 204. Зона: роль → 404 камеры → тип → точки в кадре → геометрия типа; имя 1..60 после обрезки (`ZONE_NAME_INVALID`); вырожденный полигон `ZONE_DEGENERATE`; `PATCH` тип не меняет, точки проверяются по типу зоны; удалённая зона или зона удалённой камеры → 404 `ZONE_NOT_FOUND`. Правило: роль → 404 камеры → 404 сценария (`SCENARIO_NOT_FOUND`) → 422 параметра (`field="params.<key>"`, `PARAM_UNKNOWN`, `PARAM_RANGE`); `PUT` заменяет `params` целиком; без строки в базе `enabled = status == "active"`, `effective = rules.defaults | params`.
- S9, пересчёт: `superseded` получают события видео в `new`/`auto_finished`, чей эпизод из другой версии анализа; эфир перезапускается, только если камера играет это видео, с прежним `loop`, WS `broadcast.state` остановленного и нового; `video_recompute` при задаче `recompute` этого видео в `queued` возвращает её (после проверок 409); `CameraSetupView.rules` — строка на каждый плагин.
- S10, `services._analysis_files(..., hud_path, extra)`, `_analyze(job_id, video, det, pose, extra)`; R10: `_analysis_inputs(video)` → `(det, pose, extra) | None` (extra из `AnalysisConfig.extra_artifact_ids`).

**6.2 Хранилище `store` и помощники слоёв**

- S6, `store`: `broadcast(id)`, `camera_broadcast(camera_id)` (играющий эфир, иначе последний), `latest_broadcasts()`, `playing_broadcasts()`, `broadcast_update`, `last_ready_video(camera_id)`, `event(id)` (с `camera_name`, `sector_name`, `zone_name`), `broadcast_events(broadcast_id, cycle)`, `event_update`, `feed(closed_after, sector_id=None)`, `camera_state_rows()` (входы правил 8.9 всех камер одним запросом).
- S7, `store`: `episode(id)`, `episode_evidence(episode_id)`, `analysis_job(analysis_id)` (задача с этим `analysis_id`), `event_actions(event_id)` (по `at`, `id`), `escalation_due(red_before)` (условия 8.7; «после `red_at`» — `at >= red_at`, считаются только строки `actor_role = operator`).
- S8, `store`: `master_active()` (`sent_to_master`, `master_accepted`; красные первыми, затем по последнему действию `sent_to_master`/`timeout_escalated` от нового к старому), `master_resolved(limit)` (по последнему действию `resolved`, новые первыми), `shift_events(start, end)` (`started_at` в `[start, end)`, без `superseded`, по `started_at`).
- S9, `store`: `supersedable_events(video_id, analysis_id)`, `calibration(camera_id)`, `calibration_put(values)`, `calibration_delete(camera_id)`, `zones(camera_id)`, `zone(zone_id)`, `zone_update(zone_id, values)`, `camera_rules(camera_id=None)` (все камеры одним запросом), `camera_rule_put(values)`.

**6.4 REST и воркер**

- R10, `api._actor` только декодирует `X-Actor` (percent-encoding); длину 1..`ACTOR_MAX` после обрезки проверяет `services.event_action` после роли (порядок S7). `services.ACTOR_MAX` читает только `services`.
- S6, `worker`: `_jobs(stop, idle_s)` и `_broadcasts(stop, tick_s)` в `asyncio.TaskGroup`, паузы через `asyncio.sleep` (остановка в пределах одного периода); исключение тика — лог `broadcast tick`, цикл продолжается.
- S7, `worker._escalations(stop, tick_s)` — третья задача `TaskGroup`, период `escalation.tick_ms`, исключение тика — лог `escalation tick`, цикл продолжается.

**6.6 Константы и тексты `texts.py`**

- S6, `texts.py`: `STATE_NORMAL = "Норма"`, `SECTOR_NO_OBSERVATION = "Нет наблюдения: {n} из {total} камер"`, `SECTOR_EMPTY = "В секторе нет камер"`, `NO_READY_VIDEO`, `PREVIEW_NOT_FOUND`, `NOT_CONFIRMED_SUFFIX`; `reason_text` камеры и сектора: red/yellow — `LEVEL_TITLES`, normal — «Норма».
- S7, `texts.py`: `EVENT_NOT_FOUND`, `INVALID_TRANSITION`, `COMMENT_REQUIRED = "Опишите принятые меры"`, `COMMENT_TOO_LONG = "Комментарий: до 500 символов"`, `WHY_REASON = "Причина"`.
- S9, `texts.py`: `CAL_POINTS_COUNT`, `CAL_POINTS_MISMATCH`, `CAL_CONTROL_MAX`, `CAL_COLLINEAR`, `POINTS_OUTSIDE`, `ZONE_KIND_UNKNOWN`, `ZONE_NAME_INVALID`, `ZONE_LINE_POINTS`, `ZONE_POLYGON_POINTS`, `ZONE_DEGENERATE`, `ZONE_NOT_FOUND`, `SCENARIO_NOT_FOUND`, `PARAM_UNKNOWN = "Неизвестный параметр {key}"`, `PARAM_RANGE = "Параметр {key}: от {lo} до {hi}"`, `RECOMPUTE_COMMENT = "Пересчёт: версия анализа {n}"`.
- S10, `texts.py`: `SCENARIO_SKELETON`, `VEHICLE_WITH`, `PROXIMITY_BH`, `PROXIMITY_M`, `PERSON_IN_ZONE`, `PHONE_HELD`, `FENCE_CROSSED`, `FENCE_UNSEEN = ": момент не виден"`, `FIRE_OUTSIDE`, `SMOKING`, `NO_HARNESS`, `UNDER_LOAD`, `WHY_PROXIMITY_BH`, `WHY_PROXIMITY_M`, `WHY_HOLD = "{rule} дольше {s} с"`; описания, подписи параметров, метрики (`distance_bh`, `distance_m`, `score`) и `OBJECT_LABELS` классов огня, дыма, сигареты, привязи, груза.

**Компоненты анализа и правил (разделы 7, 8.2–8.3)**

- S9, `analysis/geometry`: `homography(image_pts, world_pts) -> np.ndarray | None` — нормированный DLT numpy (Хартли, SVD) вместо `cv2.findHomography` метод 0: LM-уточнение OpenCV останавливается на ~1e-7 относительной ошибки (1e-6 м на полу 17 м), а критерий 1 S9 требует < 1e-6; `apply_h(h, p) -> Point`, `hull_contains(points, p) -> bool` (граница внутри), `grid_segments(h, world_pts) -> list[tuple[Point, Point]]` (целые метры в прямоугольнике мировых точек, отсечение `_clip` по [0, 1]), `polygon_area(points) -> float`.
- S9, `features.person_states(..., kpt_conf)` → `person_states(..., kpt_conf, ground: Callable[[Point], Point | None] | None = None)` (пиксель → метры внутри оболочки, иначе `None`); `speed_m_s` — то же окно и те же условия, что у `speed_bh_s`, по `ground` первой точки окна и текущей; `pipeline._ground(config)` строит `ground` из снимка калибровки.
- S9, `hud.build_hud(ctx, run_bh_s, cfg, observations)` → `build_hud(ctx, running: dict[str, float], cfg, observations)`: действующие параметры `running` камеры; при `speed_m_s` подпись `HUD_SPEED_M = "{v} м/с"` / `HUD_RUN_M = "бег {v} м/с"` и порог `speed_m_s`.
- R10, параметры правила в анализе, HUD и `event_detail`: `rules.defaults(id) | CameraRule.effective | CameraRule.params` снимка (было `defaults | params`): правило работает с параметрами на момент анализа, а не с текущими значениями по умолчанию; `defaults` и `params` по краям нужны снимкам без полного `effective`.
- S10, `rules.PLUGINS: dict[str, ScenarioPlugin]` → `PLUGINS: list[ScenarioPlugin]` (строка 6.7, порядок таблицы 8.3) и `rules.plugin(scenario) -> ScenarioPlugin` (`KeyError` без плагина; раздел 4); `rules.ANY_CLASS = {"fire_smoking"}` (достаточно одного из `required_classes`); статус `skeleton` берётся из `meta.status` плагина, текст `texts.SCENARIO_SKELETON`; `required_classes`: proximity `person, car, bus, truck, train`, phone `person, cell phone`, no_harness `person, no_harness`, suspended_load `person, suspended_load`, fire_smoking `fire, smoke, cigarette`, load_carrying `[]`.
- S10, `geometry.ioa(a, b) -> float` (доля площади `a` внутри `b`), `segment_crossing(p, q, a, b) -> bool` (точка на прямой считается отрицательной стороной: шаг на линию и шаг с неё — одно пересечение; пересечение вне отрезка `a-b` — нет).
- S10, `features.VehicleHistory = dict[int, list[tuple[int, VehicleState]]]`, `features.vehicle_states(tracks, ts_ms, history, cfg, ground=None) -> list[VehicleState]` (`speed_vh_s` — центр рамки, те же окно и условия, что у человека; `footprint` — нижняя кромка через `ground`, обе точки внутри оболочки; `speed_m_s` — середина `footprint` по тому же окну); `_recent` стал обобщённым.
- S10, `rules/base.attach_objects`: «внутри верхней доли» — `x1 ≤ cx ≤ x2`, `y1 ≤ cy ≤ y1 + upper_frac × h`; «ближе к запястью» — строго `<`, запястье видно при `conf ≥ pose.kpt_conf`; `ambiguous` перекрывает привязку; `WRISTS = (9, 10)`; сигарета `fire_smoking` привязывается по `upper_frac`, `wrist_dist_bh` из `scenarios.phone` (в `scenarios.fire_smoking` таких ключей нет).
- S10, субъекты и коды: proximity `pair:<p>-<v>` (`reason_code` `proximity`/`proximity_red`, `metrics` `distance_bh`/`distance_m`, метод `relative`/`calibrated`; скорость техники: `speed_m_s` важнее `speed_vh_s`) и `zone:<p>-<z>` (`proximity_zone`, N на каждую зону danger вне неё); водитель (`ioa(person, vehicle) ≥ driver_ioa` любой техники) исключён из proximity целиком; phone `phone`/`phone_zone`, U `too_small` (по `height_px`), `owner_ambiguous`, `metrics.score`; fence — одно наблюдение на человека (первая пересечённая линия), `fence_crossing`/`fence_unseen`, разрыв — `ts − prev_ts_ms > max_gap_s`; under `under_zone`; fire_smoking — субъект `fire` (одно наблюдение на кадр, `anchor=None`) и `track:<id>` (`smoking`/`smoking_zone`, удержание `smoking_hold_s` и в зоне danger); no_harness — пересечение рамок `ioa > 0`; suspended_load — `x1 ≤ anchor.x ≤ x2` и `anchor.y > y2` груза.
- S10, `analyze(..., det_model, extra: list[tuple[ModelSpec, list[FrameDetections]]] | None = None)`: классы моделей extra → `ObjectState` по `class_conf`, иначе `ModelSpec.conf`.

**Фронт (разделы 7, 8.14)**

- S6, фронт: `WsNotification` в `src/api/ws.ts` (нагрузка `notification`: WS-типов нет в openapi); `playSound(kind)` возвращает функцию остановки, `soundBlocked()` и `unlockSound()` в `components/sound.ts` (кнопка «Включить звук» в шапке); `STATE_ICON` из `components/SectorTile.tsx`; `Toasts` и `TakeoverOverlay` без пропсов, сами слушают `useWs`; `BroadcastPanel` внутри `CameraSetup.tsx`.
- S7, фронт: `TakeoverOverlay` без своего оверлея (заменяет оверлей S6): красное уведомление сразу открывает `/events/:id?takeover=1`, сирену играет `EventScreen` до действия (кроме `view`) или «Свернуть»; `CameraScreen({cameraId?})` — живая половина экрана события; `EvidenceImage` рисует рамки объектов кадра с выноской (подпись и теги); `view` отправляется сам, если он в `allowed_actions`; кнопки — `allowed_actions` без `view`, клавиши 1–3 по порядку; поле «Принятые меры» при `resolve`.
- S8, фронт: `place(event)` экспортирует `screens/master/MasterInbox.tsx` (сектор · камера · зона, общий для экранов мастера); звук уведомления мастера играет `Toasts` шапки, `MasterInbox` добавляет `navigator.vibrate(300)` и браузерное `Notification` при выданном разрешении (разрешение не запрашивает); `MasterEvent` берёт `/api/events/{event_id}`; на `/master/shift` кнопки «Предыдущая смена» (`at = start − 1 мс`) и «Текущая смена».
- S9, фронт: `PolygonEditor({image, mode, value, onChange, maxPoints, grid?})` — необязательная сетка калибровки под точками; кадр редактора — `/api/cameras/{id}/preview`; `CalibrationPanel`, `ZonesPanel`, `RulesPanel` внутри `CameraSetup.tsx` секциями страницы (вкладок нет, как в S6); контрольные точки вводит только API; параметр правила сохраняется по `blur`; «Пересчитать события» в «Правилах» — для видео плеера; на `/ohs/rules` переключатель сценария не `active` выключен.
- R10, фронт: имя камеры в списке `/admin/cameras` — ссылка на `/admin/cameras/:id`.

**Тесты (раздел 10.2)**

- R10, `tests/conftest.py`: autouse-фикстура `no_real_data` — создание `data/app` или открытие базы в ней (`Path.mkdir`, `store.connect`, `doctor.connect`) валит тест: тесту с `services`/`store` нужна фикстура `core` или `conn`.

### 6.10 Дополнения v4 (строки `GAP` S11–S15 и решения R15)

Перенесены ревью R15 из `## open` файла `progress.md`. Статус тот же, что у 6.8 и 6.9: часть контракта наравне с 6.1–6.6; `было → стало` заменяет сказанное выше.

**5.2 Типы**

- S12, `EventSummary.evidence_url: str | None = None` — `/api/evidence/<id>/image` кадра `confirm` эпизода (демо и событие без кадра — `None`), миниатюра журнала; `store._EVENTS` добавляет `LEFT JOIN evidence ev ... kind = 'confirm'` (`evidence_id`, `evidence_sha256`); поле добавлено в `contract/openapi.json` и `ws.schema.json`.
- R15, `LatencyStats` экрана IT считается по всем событиям эфира (`is_demo = 0`, с эпизодом): `notify_delay_s` — `published_at − started_at` в секундах, `publish_lag_ms` — `published_at` минус плановое время подтверждения `started_at + (confirm_ms − video_start_ms)` в мс; `pending = 0`, ранги `_percentiles` (8.13); `store.publish_latencies()`, `services._latency()` (было: нули до S6).

**6.1 Внешние клиенты и каналы доставки**

- S15, `WebhookChannel`: атрибуты `name`, `url`, `levels`, `timeout_s`; тело: `sector`/`camera`/`zone` — названия (`zone` может быть `null`), `text` — `notification_text`, `at` — `clock.now()` в момент отправки; успех — 2xx; таймаут (`httpx.TimeoutException`) → `texts.DELIVERY_TIMEOUT` «таймаут», `http_status = None`; не 2xx → `texts.DELIVERY_HTTP` «ответ HTTP <код>» с `http_status`; прочая `httpx.HTTPError` → `texts.DELIVERY_UNREACHABLE` «нет связи (<тип исключения>)»: текст исключения может нести URL с учётными данными.

**6.2 Фасад `services`**

- S11, `store.camera_state_rows()` добавляет `position_ms`, `analysis_id`, `gaps_json`, `hud_path` играющего эфира (`LEFT JOIN`); `services._freshness(analysis_id, hud_path, pos) -> int | None` (до первого кадра анализа — `None`), синглтон `_frames_ts: dict[int, list[int]]` (сбрасывает фикстура `conn`).
- S12, журнал: период и порядок по `started_at` (`date_from ≤ started_at < date_to`, как статистика 8.13), страница `started_at DESC, id DESC`; курсор — `str(id)` последнего события страницы (не цифры → 422, поле `cursor`); фильтр `status=superseded` не отменяет скрытие (нужен `include_superseded=true`); `date_from`/`date_to` без пояса — UTC; 422 — `ValidationFailed(texts.FILTER_INVALID.format(field=...), field=...)`, поля `limit`, `q`, `date_from`, `cursor`.
- S12, CSV: `events_export_csv` проверяет фильтр целиком, но `limit` и `cursor` не применяет: до `journal.export_max_rows` строк в порядке журнала; заголовки `texts.CSV_COLUMNS`, строки `\r\n`; время в `timezone` как `YYYY-MM-DD HH:MM:SS`; сценарий — `title` события; уровень, статус, вердикт — русские названия (`texts.VERDICT_TITLES`); `texts.YES`/`texts.NO`; длительность с одной цифрой и запятой; sha256 — кадр `confirm`; история `<время> <роль>: <действие>[ (<комментарий>)]` через «; », роль — `texts.ROLE_TITLES` или «система», действие — `texts.ACTION_TITLES: dict[LogAction, str]`.
- S12, `journal_facets`: сценарии — `texts.SCENARIO_TITLES`, уровни и статусы — все значения, секторы — `store.sectors()`, камеры — живые, зоны — живые зоны живых камер с названием `<камера> · <зона>`; `FacetItem.id = str(id)`.
- S13, `ohs_stats_view`: `date_to` по умолчанию `now`, `date_from` — `date_to − stats.default_days` дней, время без пояса — UTC; период `date_from ≤ started_at < date_to`; `date_from > date_to` (после умолчаний) → 422 `ValidationFailed(texts.PERIOD_INVALID, field="date_from")`, `weeks` вне 1..52 → то же с `field="weeks"`; `sector_id`/`camera_id` — через `store.journal_where`; `by_status`/`by_scenario`/`by_sector`/`by_camera` — `_count_rows` (по убыванию `count`); `by_day` — каждый день МСК периода с нулями; `by_hour` — 24 строки `key="00".."23"`, `title="08:00"`; `by_shift` — смены `shifts` по порядку с нулями (окно `_shift_window`).
- S13, реакция: первое действие с `actor_role = operator` и `action ∈ OPERATOR_DECISIONS` (`viewed` не считается), `pending` — нетерминальные события без него; `master_accept_s` — от последней передачи до первого `master_accepted`, передача — `HANDOVERS = {sent_to_master, timeout_escalated}` (эскалация по таймауту тоже передаёт мастеру), `pending` — статус `sent_to_master`; `master_resolve_s` — от `master_accepted` до `resolved`, `pending` — статус `master_accepted`; ранг `x[ceil(round(p·n, 9)) − 1]` (округление гасит ошибку `0,95·n` в float).
- S13, `management_view`: окно `weeks` — с понедельника МСК `weeks − 1` недель назад по текущую неделю; `top_sectors` — все секторы `store.sectors()` (демо-секторы скрыты при `include_demo=false`), `confirmed` по `operator_verdict` за последние `trend_weeks` недель включая текущую, `cameras` — живые камеры сектора, порядок: `per_camera` по убыванию, `None` в конце, затем `title`; `top_scenarios` — `_count_rows` за окно `weeks`; тренд: в тексте `round(|change_pct|)`, `0` → «без изменений», `previous = 0` → `change_pct = None`, текст `texts.TREND_NO_DATA` без оговорки.
- S14, `eval_run`: синхронный, `asyncio.run` на каждое видео; порядок: файл разметки (`NotFound`) → YAML и схема `EvalLabels` (`ValidationFailed`, `field` — путь pydantic через точку, `yaml` при ошибке разбора, `labels` у пустого файла) → `start_s < end_s` (`field="videos.<i>.expected.<j>"`) → все файлы видео (относительный путь — от корня репо `config.ROOT`) и `camera_id` (`NotFound`) до инференса; видео в `videos` не пишется, только строки `artifacts`; нечитаемое видео → `UnsupportedVideo` (CLI exit 2); любая `InferenceError`, в том числе pose, → exit 4 (отката на анализ без pose, как у задачи, нет); `--out DIR` — отчёт прямо в `DIR`, без него `data_dir/eval/<YYYYMMDD-HHMMSS>` по `clock.now()` в UTC; CLI печатает путь и `report.md`, ошибки — в stderr (`InferenceError` как `<code>: <message>`).
- S15, очередь доставок `services._deliveries: list[tuple[int, DeliveryKind]]` (event id, kind; сбрасывает фикстура `conn`): `published` и `escalated` ставит `broadcast_tick` после коммита по `services.DELIVERED: dict[WsType, DeliveryKind] = {"event.created": "published", "event.escalated": "escalated"}`; `to_master` — `event_action` (переход в `sent_to_master`) и `escalation_tick` (эскалация по таймауту тоже передача мастеру); в очередь идёт публикация любого уровня, фильтр — `level` события на момент `deliveries_flush` среди `levels` канала.
- S15, `deliveries_flush`: одна попытка на `(event_id, channel, kind)`, `failed` не повторяется; `channel = "webhook:<name>"`; каналы строятся из `delivery.webhooks` на каждый вызов; отправка — `asyncio.to_thread(channel.deliver, summary, kind)` по одной, строку `deliveries` пишет поток event loop; результат — число записанных строк; `worker._delivery(stop, tick_s)` — четвёртая задача `TaskGroup`, период `broadcast.tick_ms` (своего ключа нет), исключение — лог `delivery flush`, цикл продолжается.
- R15, `_journal_where`: курсор — только цифры ASCII (`isascii() and isdigit()`; `"²"` → 422 `cursor`, а не 500); `_freshness`: нет файла `hud.jsonl` → `None` (очищенная папка данных не валит состояния всех камер).

**6.2 Хранилище `store` и помощники слоёв**

- S12, `store` вне 6.x: `journal_where(equal, date_from, date_to, q, include_demo, include_superseded) -> (sql, args)`, `journal(where, after_id, limit) -> (rows, total)`, `journal_actions(event_ids)` (один запрос через `json_each`), `all_zones()`; `services`: `_utc(dt)`, `_journal_where(f)` (проверки 9 и экранирование `q`), `_msk(dt)`.
- S13, вне 6.x: `store.events_where(where)` (все события фильтра `journal_where`, по `started_at, id`); `services`: `OPERATOR_DECISIONS`, `HANDOVERS`, `_percentiles(values, pending)`, `_reactions(events)`, `_fixed_rows(pairs, keyed)`, `_add_levels(row, e)`, `_share(part, whole)`, `_trend(previous, recent, weeks)`; `texts`: `PERIOD_INVALID`, `TREND_CAVEAT`, `TREND_LESS`, `TREND_MORE`, `TREND_SAME`, `TREND_NO_DATA`, `weeks_span(n)` («4 недели к 4 неделям», «1 неделя к 1 неделе», «5 недель к 5 неделям»).
- S14, вне 6.x: `services._infer(job_id: int | None, ..., video: sqlite3.Row | dict[str, Any])` (`None` — без стадии и прогресса задачи), `_analysis_config(video, camera_id: int | None, extra_ids) -> AnalysisConfig` (общий для `_analyze` и оценки; без камеры: без калибровки и зон, правила `_rules(0, [], metas)`), `_sha256(path)` (и `video_import`), `_eval_labels(path) -> EvalLabels`, `_eval_episodes(path, camera_id) -> (episodes, duration_ms)`, `_eval_rows(outcomes, hours) -> list[EvalMetrics]`; `cli.evaluate(labels, out) -> int`; `texts`: `EVAL_LABELS_INVALID`, `EVAL_INTERVAL_INVALID`, `EVAL_TITLE`, `EVAL_COLUMNS`, `EVAL_FOOTNOTE`.
- S15, вне 6.x: `delivery.target(url) -> str` (`host[:port]` для `Channel.target`, без схемы, пути, query и учётных данных); `store.events_by_ids(ids)`, `store.event_deliveries(event_id)` (по `at, id`), `store.delivery_keys(ids) -> set[tuple[int, str, str]]`; `system_view.channels` — только webhook-каналы конфига (`kind="ws"` не показывается).

**6.5 WebSocket**

- S11, WS `camera.state` уходит только при смене состояния без учёта `freshness_ms` (`_camera_seen` хранит копию с `freshness_ms=None`): свежесть меняется каждый тик, её читают через REST (`system_view`, плитки).
- R15, `hub.Client` (`role`, `queue`, `dropped`) → `hub.Client` (`role`, `queue`): поле `dropped` никто не читал; отключение медленного клиента — маркер `None` в очереди (закрытие 1013).

**6.6 Конфиг**

- R15, `WebhookConfig`: `url` проверяется при загрузке конфига (`model_validator`): схема `http`/`https`, есть хост, порт в диапазоне, иначе `ValueError` «url must be http(s)://host»: плохой адрес не роняет каждый `deliveries_flush` и `system_view`.

**Компоненты анализа и оценки (разделы 7, 8.10, 8.18)**

- S11, `ObservabilityGap` — полуинтервал `[start_ms, end_ms)`; `stale` — между соседними кадрами анализа (`start_ms` кадр до разрыва, `end_ms` кадр после; начало и хвост видео не проверяются, `min_duration_s` к `stale` не применяется: иначе 2001 мс не считался бы); серия `dark`/`obstructed` длится до первого хорошего сэмпла или до `duration_ms`; список по `(start_ms, stale < dark < obstructed)`, интервалы `dark` и `obstructed` могут перекрываться, камера берёт первый содержащий позицию.
- S11, `observability.Luma = tuple[int, float, float]` (`ts_ms, mean, std`), помощник `_runs`; `media.LUMA_WIDTH = 160`, уменьшение `INTER_NEAREST` (усреднение `INTER_AREA` гасит разброс шума и текстуры: тестовое видео с шумом становилось `obstructed`); `sample_luma` нечитаемого файла → `[]`.
- S11, `analyze`: кадры внутри `dark`/`obstructed` не дают наблюдений (`U` у всех субъектов, 8.10); `stale` отдельно не обрабатывается — менеджер эпизодов сам добавляет разрыв `ts − ts прошлого кадра` в `uncertain_ms` и проверяет `lost_timeout_s`.
- S14, `evaluate`: `OutcomeKind = Literal["tp", "fn", "fp", "duplicate", "late"]`, `Outcome = tuple[str, OutcomeKind, float | None]` (сценарий, исход, задержка tp в с), `match_episodes(expected: list[ExpectedEvent], episodes: list[EpisodeDraft], deadline_s: float) -> list[Outcome]` (одно видео: tp на пару, fn на эталон без пары, исход на каждый несопоставленный эпизод), `report_md(report: EvalReport) -> str`; границы сравниваются в целых мс (`round(s × 1000)` против `confirm_ms`): ровно `deadline_s` — tp без ошибки float.
- S14, сопоставление: несопоставленный эпизод внутри эталона, у которого уже есть пара, — `duplicates` (даже позже дедлайна); внутри только эталонов без пары — `late`; `episodes = tp + fp + duplicates + late`, `expected = tp + fn`; строки — сценарии эталонов и эпизодов по алфавиту, затем `*`; `f1 = None`, если precision или recall `None` или их сумма 0; `fp_per_hour` — на сумму длительностей всех видео разметки (одна для всех строк), 0 часов → `None`; `delay_s = _percentiles(задержки tp, 0)`.
- R15, `hud.build_hud`: подпись на каждое `P` (8.2 п. 8) через `hud._keys(subject)`: `pair:<p>-<v>` — человек `p` и техника `v`, `zone:<p>-<z>` — человек `p`, `fire` — каждый объект `rules.fire.FLAMES` кадра, `track:<id>` — сам человек (было: только `track:<id>`).

**Фронт (разделы 7, 8.14)**

- S12, фронт: `FiltersBar.tsx` экспортирует тип `JournalFilter` (query `GET /api/events`); дата фильтра — день МСК (полночь +03:00), `date_to` не включается; «Показать ещё» дозагружает по `next_cursor`; «Экспорт CSV» — ссылка с query фильтра; строка открывает `/events/:id` (для `ohs` `allowed_actions` пуст — только чтение).
- S13, фронт: `recharts@2.15.4` в `frontend/package.json`; графики фиксированного размера 640×240 без `ResponsiveContainer` (ему нужен `ResizeObserver`, в jsdom его нет); `BarChartCard({title, data: {name, value}[]})`, `StackedDaysCard({title, days})`, `LineChartCard({title, weeks})`, `PercentilesCard({title, value})`; фильтры сектора и камеры экрана статистики — из `/api/journal/facets`; `test_api_skeleton.py::test_unbuilt_route_returns_501` подменяет `services.management_view` заглушкой `NotImplementedError` (с S13 построены все маршруты).

**Docker (разделы 4, 16 слайс 15)**

- S15, Docker: `node:24-slim` (сборка фронта), `python:3.12-slim` + `ghcr.io/astral-sh/uv:0.13.0`, `uv sync --locked --no-dev` (проект editable, `config.ROOT = /app`), команда `uv run --no-sync safewatch serve --host 0.0.0.0 --port 8000`; compose: `extra_hosts: host.docker.internal:host-gateway` (для Linux-хоста), тома `./data/app:/app/data/app`, `./models:/app/models:ro`; `.dockerignore` исключает `.env*`, `secrets/`, `data/`, `models/`, `vendor/`, `results/`, `Deep-Research/`, `.git/`, `.venv*`.

**Тесты (раздел 10.2, 10.1)**

- S13, `tests/test_api_skeleton.py::test_unbuilt_route_returns_501` подменяет `services.management_view` заглушкой `NotImplementedError`: с S13 построены все маршруты, 501 проверяется подменой фасада.
- R15, `frontend/src/App.test.tsx::stub_screens_show_slice` проверяет, что у каждого маршрута `nav.ts` есть экран (заглушек с S13 нет; новый маршрут без экрана валит тест); строки 6.7 маршрутов остаются на этом тесте.
- R15, права ролей (10.1 «один тест без роли и один с чужой ролью на слайс») относятся к слайсам с пишущими функциями: журнал, статистика и оценка (S12–S14) только читают, `role` в их сигнатурах 6.2 нет, тестов прав нет.

---

### 6.11 Контракт v5: второй прогон (Argus)

Записан владельцем (v5) до кода, по `UPGRADE_v1.md`. Часть контракта наравне с 5.1–6.6; `было → стало` заменяет сказанное выше. Слайс S16 объявляет всё из этого раздела: миграцию, типы, поля, маршруты (незакрытые отвечают 501), секции конфига и модели `config.py`; остальные слайсы наполняют поведение. Контракт фронта только расширяется: ни один путь, тип и поле `contract/openapi.json` 1.0.0 не удаляются и не переименовываются.

#### 6.11.1 Схема: `src/safewatch/migrations/0002_v5.sql`

```sql
-- v5 (tech.md 6.11.1): additive only, rows of 0001 keep working.
ALTER TABLE videos ADD COLUMN web_path TEXT;           -- пишет: services.video_upload, video_import (S18); uploads/<sha256>.web.mp4, NULL — исходник играет в браузере
ALTER TABLE analyses ADD COLUMN autocal_json TEXT;     -- пишет: services.run_next_job (S19); AutoCalibration или NULL (анализ до v5)
ALTER TABLE events ADD COLUMN person_name TEXT NOT NULL DEFAULT '';      -- пишет: services.event_identify (S26)
ALTER TABLE events ADD COLUMN person_position TEXT NOT NULL DEFAULT '';  -- пишет: services.event_identify (S26)
ALTER TABLE events ADD COLUMN crew TEXT NOT NULL DEFAULT '';             -- пишет: services.event_identify (S26)
ALTER TABLE deliveries ADD COLUMN delivered_at TEXT;   -- пишет: services.deliveries_flush (S23), канал call

CREATE TABLE delivery_queue (                          -- пишет: services.broadcast_tick, event_action, escalation_tick; читает и чистит deliveries_flush (S23)
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    kind TEXT NOT NULL CHECK (kind IN ('published', 'escalated', 'to_master')),
    level TEXT NOT NULL CHECK (level IN ('yellow', 'red')),  -- уровень на момент постановки
    created_at TEXT NOT NULL,
    UNIQUE (event_id, kind)
);

CREATE TABLE dataset_items (                           -- пишет: services.datasets_flush (S25)
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL UNIQUE REFERENCES events(id),
    scenario TEXT NOT NULL,
    label TEXT NOT NULL CHECK (label IN ('false_alarm')),
    path TEXT NOT NULL,                                -- datasets/false_alarms/<event_id>/ от data_dir
    frames INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE demo_packs (                              -- пишет: services.demo_import (S17)
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,                              -- sha256 файла manifest.json
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),  -- бэкенд артефактов пакета
    fake INTEGER NOT NULL,                             -- 1: хоть один артефакт синтетический
    cameras INTEGER NOT NULL,
    videos INTEGER NOT NULL,
    imported_at TEXT NOT NULL
);
```

Чего в схеме v5 нет: файлов клипов, справочника работников, таблицы калькулятора (расчёт не хранится), таблицы паспортов (паспорт считается на запрос), ролей `call` в `deliveries.kind` (канал звонка различается по `channel = "call:<name>"`).

#### 6.11.2 Типы: `src/safewatch/types.py`, новые имена

```python
SpeedSource = Literal["calibration", "auto", "relative"]  # m/s from the homography, m/s from autocal, body heights/s
PassportVerdict = Literal["suitable", "partial", "unsuitable", "unknown"]
CalcTier = Literal["base", "extended", "max"]


class AutoCalibration(BaseModel):  # analyses.autocal_json (S19, tech.md 8.21)
    ok: bool
    reason: str  # Russian; "" when ok
    samples: int  # standing people kept after outlier rejection
    a_px: float  # person height in px at foot y = 0
    b: float  # px of height per px of foot y
    rmse_px: float
    r2: float
    person_height_m: float


class Clip(BaseModel):  # window of the source video (S18, tech.md 8.20)
    video_id: int
    url: str  # /api/videos/<id>/file#t=<start_s>,<end_s>
    start_ms: int
    end_ms: int
    playable: bool  # the served file plays in a browser


class DemoArtifact(BaseModel):  # one model run of one video inside a demo pack (S17)
    model: str  # id@version
    task: ModelTask
    input_size: int
    step: int
    backend: BackendName
    fake: bool
    file: str  # artifacts/<cache_key>.jsonl, relative to the pack
    frames: int
    metrics: InferenceMetrics


class DemoVideo(BaseModel):
    file: str  # videos/<name> in a pack; a path under --videos in a layout
    sha256: str = ""
    artifacts: list[DemoArtifact] = []


class DemoCamera(BaseModel):
    sector: str  # matched by name, created when missing
    name: str  # matched by name inside the sector, created when missing
    description: str = ""
    videos: list[DemoVideo]
    calibration: CalibrationIn | None = None
    zones: list[ZoneIn] = []
    rules: dict[str, CameraRuleIn] = {}


class DemoManifest(BaseModel):  # data/demo/<name>/manifest.json
    name: str
    created_at: datetime
    contract: str
    cameras: list[DemoCamera]


class DemoLayout(BaseModel):  # config/demo.example.yaml: input of `safewatch demo build`
    name: str
    cameras: list[DemoCamera]


class DemoPack(BaseModel):  # GET /api/demo/packs
    id: int
    name: str
    sha256: str
    backend: BackendName
    fake: bool
    cameras: int
    videos: int
    imported_at: datetime


class DemoImportReport(BaseModel):
    skipped: bool  # the pack with this name is already imported
    name: str
    cameras: int
    videos: int
    jobs: int


class CalcAssumption(BaseModel):  # every number of the calculator is one of these (S24, tech.md 8.25)
    key: str
    title: str
    value: float
    unit: str
    source: str  # where the number comes from, Russian
    editable: bool = True


class RolloutIn(BaseModel):
    workshops: int
    cameras: int
    shifts_per_day: int
    workers: int
    operators: int
    incidents_per_year: float
    downtime_cost_rub: float  # per incident
    fine_cost_rub: float
    treatment_cost_rub: float
    lawsuit_cost_rub: float
    overrides: dict[str, float] = {}  # CalcAssumption.key -> value


class TierResult(BaseModel):
    tier: CalcTier
    title: str
    accelerators: int
    servers: int
    capex_rub: float
    opex_rub_year: float
    savings_rub_year: float
    payback_months: float | None  # None: savings do not exceed opex
    items: list[WhyItem]  # breakdown lines


class RolloutResult(BaseModel):
    incident_cost_rub: float
    incidents_per_1000_workers: float | None
    events_per_operator_shift: float | None  # from the journal, None without data
    tiers: list[TierResult]
    assumptions: list[CalcAssumption]


class ScaleIn(BaseModel):
    cameras_now: int
    new_cameras: int
    overrides: dict[str, float] = {}


class ScaleResult(BaseModel):
    cameras_total: int
    analysis_fps: float
    capacity_fps: float  # per accelerator
    capacity_source: str
    accelerators_now: int
    accelerators_total: int
    servers_total: int
    capex_rub: float  # for the added part only
    items: list[WhyItem]
    assumptions: list[CalcAssumption]


class CalculatorDefaults(BaseModel):
    rollout: RolloutIn
    scale: ScaleIn
    assumptions: list[CalcAssumption]
    measured: list[CalcAssumption]  # numbers from LinQ runs and the journal, editable=False


class DatasetItem(BaseModel):  # S25, tech.md 8.26
    event_id: int
    scenario: str
    label: Literal["false_alarm"]
    frames: int
    path: str
    created_at: datetime


class DatasetView(BaseModel):
    items: list[DatasetItem]
    total: int
    frames: int


class IdentityIn(BaseModel):  # S26, tech.md 8.27; empty string clears the field
    person_name: str = ""
    person_position: str = ""
    crew: str = ""


class PeopleStats(BaseModel):
    date_from: datetime
    date_to: datetime
    include_demo: bool
    total: int
    identified: int
    by_person: list[CountRow]
    by_crew: list[CountRow]


class PassportScenario(BaseModel):  # S27, tech.md 8.28
    scenario: str
    title: str
    verdict: PassportVerdict
    reason: str


class CameraPassport(BaseModel):
    camera_id: int
    analysis_id: int | None
    frames: int
    person_height_px_p50: float | None
    small_object_px_p50: float | None
    person_frames_share: float | None
    dark_share: float | None
    empty_share: float | None
    shift_px: float | None = None  # S32
    shift_text: str = ""  # S32
    scenarios: list[PassportScenario]
```

#### 6.11.3 Поля, добавленные к типам 5.2

Каждое поле — со значением по умолчанию: старые ответы и снимки остаются валидными.

| Тип | Поле | Слайс | Значение |
| --- | --- | --- | --- |
| `Video` | `web_playable: bool = False` | 18 | `browser_playable` или есть H.264-копия `web_path` |
| `Job` | `status_text: str = ""` | 17 | понятный текст состояния (8.19), с S28 — прогресс LinQ (8.29) |
| `Job` | `eta_s: float \| None = None`, `rate_fps: float \| None = None` | 28 | 8.29 |
| `EventSummary` | `clip: Clip \| None = None` | 18 | 8.20; демо-событие сида — `None` |
| `EventSummary` | `person_name: str = ""`, `person_position: str = ""`, `crew: str = ""` | 26 | 8.27 |
| `EventDetail` | `can_identify: bool = False` | 26 | роль запроса из 8.27 |
| `Analysis` | `auto_calibration: AutoCalibration \| None = None` | 19 | 8.21 |
| `CameraSetupView` | `auto_calibration: AutoCalibration \| None = None` | 19 | автокалибровка активного анализа последнего готового видео |
| `PersonState`, `VehicleState` | `speed_source: SpeedSource = "relative"` | 19 | 8.21 |
| `HudObject` | `projection: list[Point] \| None = None` | 22 | 8.23, нормированный полигон |
| `Delivery` | `delivered_at: datetime \| None = None`, `status_text: str = ""` | 23 | 8.24 |
| `Channel` | `kind: Literal["ws", "webhook"]` → `kind: Literal["ws", "webhook", "call"]` | 23 | 8.24 |
| `LogAction` | + `"identified"` | 26 | 8.27 |
| `ModelSpec` | `nc: int \| None = None`, `input_name: str = "images"` | 29 | 8.30 |
| `RemoteShell`, `InferenceBackend` | метод `close(self) -> None` | 28 | 8.29 |

#### 6.11.4 Фасад v5: `src/safewatch/services.py`

```python
def demo_build(layout: Path, videos_dir: Path, out: Path, allow_fake: bool = False) -> DemoManifest: ...
def demo_import(path: Path) -> DemoImportReport: ...
def demo_packs() -> list[DemoPack]: ...
def artifact_import(
    video_id: int, model_ref: str, jsonl: Path, backend: BackendName, fake: bool,
    metrics: InferenceMetrics | None = None,
) -> int: ...  # artifact id
def calculator_defaults() -> CalculatorDefaults: ...
def calculator_rollout(data: RolloutIn, role: Role | None) -> RolloutResult: ...
def calculator_scale(data: ScaleIn, role: Role | None) -> ScaleResult: ...
async def datasets_flush() -> int: ...
def datasets_view() -> DatasetView: ...
def dataset_export(out: Path | None = None) -> Path: ...  # zip file
def event_identify(event_id: int, data: IdentityIn, role: Role | None, actor: str | None) -> EventDetail: ...
def people_stats_view(
    date_from: datetime | None = None, date_to: datetime | None = None, include_demo: bool = True,
) -> PeopleStats: ...
def camera_passport(camera_id: int) -> CameraPassport: ...
def shift_report_pdf(at: datetime | None = None) -> bytes: ...
def backend_close() -> None: ...
```

| Функция | Пишет в хранилище | Исключения | Код: REST | Код: CLI | Слайс |
| --- | --- | --- | --- | --- | --- |
| `demo_build(layout, videos_dir, out, allow_fake)` | файлы пакета в `out` (база не меняется) | `NotFound` (раскладка, видео), `ValidationFailed` (схема раскладки, фейк без `allow_fake`, папка `out` не пуста); бэкенд недоступен → `InferenceError` | — | exit 3, 2, 4 | 17 |
| `demo_import(path)` | sectors, cameras, zones, calibrations, camera_rules, videos, artifacts, jobs, demo_packs; файлы `uploads/`, `artifacts/` | `NotFound` (папка, `manifest.json`, файл пакета), `ValidationFailed` (схема, модель пакета не в реестре, sha256 видео не совпал) | — | exit 3, 2 | 17 |
| `demo_packs()` | нет | нет | — | — | 17 |
| `artifact_import(video_id, model_ref, jsonl, backend, fake, metrics)` | artifacts, файл `artifacts/` | `NotFound` (видео, файл), `ValidationFailed` (ссылка не в реестре, JSONL не проходит `read_jsonl`) | — | exit 3, 2 | 17 |
| `calculator_defaults()` | нет | нет | — | — | 24 |
| `calculator_rollout(data, role)` | нет | `RoleRequired`, `Forbidden`, `ValidationFailed` (число < 0, `cameras` или `workshops` 0, неизвестный ключ `overrides`) | 400, 403, 422 | — | 24 |
| `calculator_scale(data, role)` | нет | те же | 400, 403, 422 | — | 24 |
| `datasets_flush()` | dataset_items, файлы `datasets/` | нет: ошибка кадра → лог, повтор на следующем тике | — | — | 25 |
| `datasets_view()` | нет | нет | — | — | 25 |
| `dataset_export(out)` | файл zip | нет | — | exit 0 | 25 |
| `event_identify(event_id, data, role, actor)` | events, event_actions (`identified`) | `RoleRequired`, `Forbidden`, `ValidationFailed` (длина поля, actor), `NotFound` | 400, 403, 422, 404 | — | 26 |
| `people_stats_view(...)` | нет | `ValidationFailed` (`date_from > date_to`) | 422 | — | 26 |
| `camera_passport(camera_id)` | нет | `NotFound` (нет или удалена) | 404 | — | 27 |
| `shift_report_pdf(at)` | нет | нет | — | — | 30 |
| `backend_close()` | нет | нет | — | — | 28 |

Права ролей v5 (дополняют таблицу 6.2; чтение по-прежнему без роли):

| Функция | Роли |
| --- | --- |
| `calculator_rollout` | management |
| `calculator_scale` | management, admin |
| `event_identify` | ohs, management |

Ситуации на границах v5:

| Ситуация | Фасад | Код: REST | Код: CLI |
| --- | --- | --- | --- |
| перекодирование упало или вышло по таймауту | видео принято, `web_path = NULL`, `web_playable = browser_playable`, лог `transcode: <что>` | 201 | 0 |
| пакет уже импортирован (то же `name`) | `DemoImportReport.skipped = true`, база не меняется | — | 0 |
| модель пакета не в `config/models.yaml` | `ValidationFailed`, ничего не записано | — | exit 2 |
| LinQ недоступен при сборке пакета | `InferenceError`, файлы пакета не пишутся | — | exit 4 |
| звонок: провайдер `stub` | строка deliveries `sent`, `delivered_at = at`, текст «Звонок доставлен (заглушка)» | — | — |
| ответ Jupyter — HTML вместо API | `InferenceError("bad_output")`; `backend_check` → `bad_answer` (было: `unreachable`, долг R5) | 200 | `doctor` exit 4 |
| паспорт камеры без готового видео | все сценарии `unknown`, причина «Нет обработанного видео» | 200 | — |

#### 6.11.5 CLI v5: `src/safewatch/cli.py`

| Команда | Фасад | Выход | Коды | Слайс |
| --- | --- | --- | --- | --- |
| `safewatch demo build LAYOUT --videos DIR --out DIR [--allow-fake]` | `demo_build` | JSON `DemoManifest` без артефактов (имена, число кадров) | 0; 2 схема или фейк; 3 нет файла; 4 бэкенд недоступен | 17 |
| `safewatch demo import DIR` | `demo_import` | JSON `DemoImportReport` | 0; 2 схема, модель, sha256; 3 нет папки или файла | 17 |
| `safewatch serve --seed` | v5: после `seed_demo` — `demo_import(demo.pack)`, если `demo.autoload` и папка есть | лог | как в 6.3 | 17 |
| `safewatch dataset export [--out DIR]` | `dataset_export` | путь к zip | 0 | 25 |
| `safewatch import-artifact FILE --video ID --model REF [--backend linq\|local] [--fake]` | `artifact_import` | id артефакта | 0; 2 формат или модель; 3 нет файла или видео | 29 |
| `safewatch eval LABELS [--out DIR]` | v5: при живом процессе из `server.pid` — отказ | — | v5: 5 сервер запущен (было: запуск вторым процессом, долг S14) | 30 |

#### 6.11.6 REST v5: `src/safewatch/api.py`

Колонки как в 6.4; тест маршрутов S16 считает строки этой таблицы вместе с 6.4: всего 65 маршрутов. Маршрут `/api/master/shift.pdf` и `/api/datasets/false-alarms/export.zip` объявлены рядом с соседями без конфликта путей.

| Искомая строка декоратора | Фасад | Вход | Ответ | Ошибки | Слайс |
| --- | --- | --- | --- | --- | --- |
| `@router.get("/api/demo/packs")` | `demo_packs` | — | `list[DemoPack]` | — | 17 |
| `@router.get("/api/calculator/defaults")` | `calculator_defaults` | — | `CalculatorDefaults` | — | 24 |
| `@router.post("/api/calculator/rollout")` | `calculator_rollout` | `RolloutIn`, `X-Role` | `RolloutResult` | 400, 403, 422 | 24 |
| `@router.post("/api/calculator/scale")` | `calculator_scale` | `ScaleIn`, `X-Role` | `ScaleResult` | 400, 403, 422 | 24 |
| `@router.get("/api/datasets/false-alarms")` | `datasets_view` | — | `DatasetView` | — | 25 |
| `@router.get("/api/datasets/false-alarms/export.zip")` | `dataset_export` | — | `application/zip` | — | 25 |
| `@router.patch("/api/events/{event_id}/identity")` | `event_identify` | `IdentityIn`, `X-Role`, `X-Actor` | `EventDetail` | 400, 403, 404, 422 | 26 |
| `@router.get("/api/stats/people")` | `people_stats_view` | query `date_from`, `date_to`, `include_demo` | `PeopleStats` | 422 | 26 |
| `@router.get("/api/cameras/{camera_id}/passport")` | `camera_passport` | — | `CameraPassport` | 404 | 27 |
| `@router.get("/api/master/shift.pdf")` | `shift_report_pdf` | query `at` | `application/pdf` | 422 | 30 |

Было → стало в существующих маршрутах: `GET /api/videos/{video_id}/file` отдаёт H.264-копию `web_path`, если она есть, иначе исходник (S18); `POST /api/cameras/{camera_id}/videos` проверяет `X-Role` и заголовок `Content-Length` (больше `upload.max_mb` → 413) до чтения тела (S30, долг R5).

#### 6.11.7 WebSocket v5

Новых типов `WsType` нет. Новые поля `EventSummary` (клип, идентификация) приходят в `event.created` и `event.updated`. `event_identify` публикует `event.updated`; `deliveries_flush` после строки канала `call` публикует `event.updated` этого события (карточка перечитывает `deliveries`). `contract/ws.schema.json` пересобирается в S16 и S18, S26 (новые поля), `contract/ws-examples.json` получает новые поля в примерах `event.*`.

#### 6.11.8 Конфиг и константы v5

Добавления в `config/default.yaml` (S16 кладёт их целиком, `config.py` описывает каждую секцию моделью с `extra="forbid"`):

```yaml
product_name: Argus                # было: SafeWatch

pipeline:
  vehicle_classes: [car, bus, truck, train]   # S29: было константой analysis.pipeline.VEHICLES

class_conf:                        # дополнительно к v4
  helmet: 0.35
  no_helmet: 0.35
  respirator: 0.35
  no_respirator: 0.35

tracker:
  reattach_bh: 1.0                 # S30: этап 3 трекера, 8.31

scenarios:
  no_helmet:
    hold_s: 3.0
    head_frac: 0.35
    min_person_px: 80
  no_respirator:
    hold_s: 3.0
    head_frac: 0.35
    min_person_px: 80

zone_kinds:                        # дополнительно к v4; описание rest v5: «Места отдыха. Телефон здесь разрешён.»
  - id: helmet_required
    title: Обязательна каска
    color: "#FF9500"
    geometry: polygon
    description: Цех или участок, где без каски нельзя. Человек без каски дольше порога — жёлтое событие.
  - id: respirator_required
    title: Обязателен респиратор
    color: "#5E5CE6"
    geometry: polygon
    description: Участок с пылью или парами. Человек без респиратора дольше порога — жёлтое событие.
  - id: walkway
    title: Проход («зелёная линия»)
    color: "#34C759"
    geometry: polygon
    description: Безопасный проход. Телефон здесь разрешён.

autocal:
  person_height_m: 1.7
  min_samples: 30
  min_person_px: 40
  edge_px: 2
  max_residual: 0.15               # доля роста: точка дальше 15 % от линии отбрасывается
  iterations: 3

clips:
  pre_s: 3.0
  post_s: 5.0
  max_s: 30.0

transcode:
  enabled: true
  crf: 23
  preset: veryfast
  timeout_s: 600

demo:
  pack: data/demo/argus
  autoload: true

delivery:
  webhooks: []
  calls:                           # S23: только kind=to_master
    - {name: master, to: "", levels: [red], provider: stub}

datasets:
  tick_ms: 2000
  max_frames: 40

passport:
  min_frames: 50
  person_partial_px: 80
  small_object_px: 12
  dark_partial: 0.2
  dark_unsuitable: 0.5
  empty_partial: 0.8

shift:                             # S32
  max_px: 20
  sample_width: 320

linq:                              # дополнительно к v4
  reply_timeout_s: 120
  slow_rtt_s: 12.0

local:
  providers: [CPUExecutionProvider]   # S29; CUDAExecutionProvider — для GPU-машины ML-части

calculator:
  assumptions:
    - {key: accelerator.capacity_fps, title: "Пропускная способность одного ускорителя LinQ", value: 12.4, unit: "кадр/с", source: "замер LinQ 24.10 14:52: детектор 640, inflight 4, общая очередь площадки"}
    - {key: models_per_frame, title: "Запросов к TPU на кадр", value: 2, unit: "шт.", source: "конвейер Argus: детектор и pose"}
    - {key: accelerators_per_server, title: "Ускорителей в одном сервере", value: 4, unit: "шт.", source: "допущение команды, уточнить у ХайТэк"}
    - {key: accelerator.price_rub, title: "Цена ускорителя LinQ", value: 500000, unit: "₽", source: "допущение команды: цена не опубликована, заменить ценой поставщика"}
    - {key: server.price_rub, title: "Цена сервера под ускорители", value: 350000, unit: "₽", source: "допущение команды, уточнить у поставщика"}
    - {key: integration_rub, title: "Пусконаладка и подключение камер", value: 300000, unit: "₽", source: "допущение команды"}
    - {key: support_share_year, title: "Поддержка в год, доля от вложений", value: 0.15, unit: "доля", source: "допущение команды"}
    - {key: light_sound_rub, title: "Световой и звуковой сигнал у зоны", value: 25000, unit: "₽ за зону", source: "допущение команды, уточнить у поставщика"}
    - {key: zones_per_camera, title: "Сигнальных зон на камеру", value: 1, unit: "шт.", source: "допущение команды"}
    - {key: speaker_rub, title: "Громкоговоритель в цех", value: 40000, unit: "₽ за цех", source: "допущение команды, уточнить у поставщика"}
    - {key: new_camera_rub, title: "Новая IP-камера с монтажом", value: 30000, unit: "₽", source: "допущение команды, уточнить у поставщика"}
    - {key: new_cameras_share, title: "Доля новых камер на максимальном уровне", value: 0.2, unit: "доля", source: "допущение команды"}
    - {key: reduction.base, title: "Снижение инцидентов: базовый уровень", value: 0.2, unit: "доля", source: "гипотеза команды, проверяется пилотом; доказанного эффекта нет"}
    - {key: reduction.extended, title: "Снижение инцидентов: расширенный уровень", value: 0.3, unit: "доля", source: "гипотеза команды, проверяется пилотом; доказанного эффекта нет"}
    - {key: reduction.max, title: "Снижение инцидентов: максимальный уровень", value: 0.4, unit: "доля", source: "гипотеза команды, проверяется пилотом; доказанного эффекта нет"}
```

Модели `config.py` v5: `AutocalConfig`, `ClipsConfig`, `TranscodeConfig`, `DemoConfig`, `CallConfig` (`name: str`, `to: str`, `levels: list[Level]`, `provider: Literal["stub"]`), `DatasetsConfig`, `PassportConfig`, `ShiftCheckConfig`, `CalcAssumptionConfig`, `CalculatorConfig`; `ScenariosConfig` получает `no_helmet`, `no_respirator`; `PipelineConfig.vehicle_classes`, `TrackerConfig.reattach_bh`, `LinqConfig.reply_timeout_s`, `slow_rtt_s`, `LocalConfig.providers`, `DeliveryConfig.calls`. `DeliveryConfig` проверяет при загрузке, что имена каналов (`webhooks` и `calls` вместе) уникальны, иначе `ValueError` «delivery: channel names must be unique» (S23, долг S15).

`config/models.yaml` v5 (S20) дописывает две записи Матвея из `ml/models.matvey.yaml` ветки `matvey_cv`, ключи `classes` — целые:

```yaml
  - id: matvey-pose-yolov8n
    version: 640-v1-acc5f51228b9
    task: pose
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: person}
    linq_program: mosprom_matvey_pose_yolov8n_640-v1-acc5f51228b9.tpu
    linq_tail: models/matvey/matvey-pose-yolov8n/640-v1-acc5f51228b9/matvey_pose_yolov8n_640-v1-acc5f51228b9_tail.onnx
    local_onnx: models/matvey/matvey-pose-yolov8n/640-v1-acc5f51228b9/matvey_pose_yolov8n_640-v1-acc5f51228b9.onnx
  - id: matvey-helmet-yolov8n
    version: 640-v1-5c3af1f3b855
    task: detect
    input_size: 640
    conf: 0.1
    iou: 0.45
    classes: {0: helmet, 1: no_helmet}
    linq_program: mosprom_matvey_helmet_yolov8n_640-v1-5c3af1f3b855.tpu
    linq_tail: models/matvey/matvey-helmet-yolov8n/640-v1-5c3af1f3b855/matvey_helmet_yolov8n_640-v1-5c3af1f3b855_tail.onnx
    local_onnx: models/matvey/matvey-helmet-yolov8n/640-v1-5c3af1f3b855/matvey_helmet_yolov8n_640-v1-5c3af1f3b855.onnx
```

`pipeline` по умолчанию не меняется: модели Матвея включает `config/user.yaml` по образцу `config/user.matvey.example.yaml` (`pipeline.pose: matvey-pose-yolov8n@640-v1-acc5f51228b9`, `pipeline.extra: [matvey-helmet-yolov8n@640-v1-5c3af1f3b855]`).

Именованные константы v5:

| Константа | Значение | Единица | Читает | Поведение |
| --- | --- | --- | --- | --- |
| `api.CONTRACT_VERSION = "1.1.0"` (было `"1.0.0"`) | 1.1.0 | версия | `api`, `openapi.json`, `hello`, `meta` | 6.11 |
| `media.WEB_SUFFIX = ".web.mp4"` | — | — | `transcode`, `video_file` | 8.20 |
| `demo.MANIFEST = "manifest.json"` | — | — | `demo_build`, `demo_import` | 8.19 |
| `rules.phone.ALLOWED_KINDS = ("walkway", "rest")` | — | типы зон | `PhonePlugin` | 8.23 |
| `services.IDENTITY_MAX = 80` | 80 | символов | валидация | 8.27 |
| `report_pdf.FONT = "DejaVuSans.ttf"` | — | — | `shift_pdf` | 8.31 |
| `texts.SCENARIO_MODEL_MISSING = "Модель не подключена: нужны классы {classes}"` (было «Нет модели с классами: {classes}») | — | — | `scenario_metas` | 8.22 |

#### 6.11.9 Компоненты анализа и правил v5

```python
# src/safewatch/analysis/autocal.py (S19)
def fit(frames: list[FrameDetections], person_cls: set[int], width: int, height: int,
        cfg: AutocalConfig, upright_hw: float, high_thresh: float) -> AutoCalibration: ...
def scale_at(cal: AutoCalibration, foot_y_px: float) -> float | None: ...  # m per px; None if not ok or height <= 0

# src/safewatch/analysis/passport.py (S27)
def build_passport(camera_id: int, analysis_id: int | None, hud: list[HudFrame], gaps: list[ObservabilityGap],
                   duration_ms: int, height: int, metas: list[ScenarioMeta], zones: list[Zone],
                   cfg: PassportConfig, min_person_px: int, phone_min_person_px: float) -> CameraPassport: ...

# src/safewatch/rules/base.py (S20)
def head_objects(ctx: FrameContext, name: str, head_frac: float) -> dict[int, ObjectState | Literal["ambiguous"]]: ...

# src/safewatch/rules/ppe.py (S20)
class HelmetPlugin: ...      # ScenarioPlugin, ID = "no_helmet"
class RespiratorPlugin: ...  # ScenarioPlugin, ID = "no_respirator"

# src/safewatch/calculator.py (S24)
def rollout(data: RolloutIn, assumptions: dict[str, CalcAssumption], analysis_fps: float,
            events_per_camera_day: float | None) -> RolloutResult: ...
def scale(data: ScaleIn, assumptions: dict[str, CalcAssumption], analysis_fps: float,
          capacity_fps: float, capacity_source: str) -> ScaleResult: ...

# src/safewatch/dataset.py (S25)
def build_item(root: Path, event: EventSummary, episode: Episode, video: Path, det: Path, pose: Path | None,
               hud: Path, frame_ms: list[int], label: dict[str, object]) -> int: ...  # frames written
def export_zip(root: Path, items: list[DatasetItem], out: Path) -> Path: ...

# src/safewatch/demo.py (S17)
def read_manifest(path: Path) -> DemoManifest: ...
def write_manifest(path: Path, manifest: DemoManifest) -> str: ...  # sha256 of the file

# src/safewatch/media.py (S18, S32)
def transcode(src: Path, dst: Path, cfg: TranscodeConfig) -> bool: ...
def frame_shift(reference: np.ndarray, current: np.ndarray, sample_width: int) -> float: ...  # px of the reference size

# src/safewatch/delivery.py (S23)
class CallChannel:  # DeliveryChannel: provider "stub" answers delivered at once
    def __init__(self, name: str, to: str, levels: list[Level], provider: Literal["stub"]) -> None: ...

# src/safewatch/report_pdf.py (S30)
def shift_pdf(summary: ShiftSummary, product_name: str, tz: str) -> bytes: ...
```

`rules.PLUGINS` v5: в конец списка `HelmetPlugin`, `RespiratorPlugin` (порядок таблицы 8.3 и 8.22). `texts.SCENARIO_TITLES` v5: `no_helmet` «Без каски в зоне обязательной каски», `no_respirator` «Без респиратора в зоне обязательного респиратора».

---

### 6.12 Дополнения v6 (строки `GAP` S16–S20 и решения R20)

Перенесены ревью R20 из `## open` файла `progress.md`. Статус тот же, что у 6.8–6.10: часть контракта наравне с 6.1–6.6 и 6.11; `было → стало` заменяет сказанное выше.

**6.2 Фасад `services`: демо-пакет (8.19)**

- S17, `texts.job_status_text`: `def job_status_text(job: Job, tz: str) -> str` (8.19: `job_status_text(job)`; `tz` = `Settings.timezone`, `texts` не читает конфиг); `failed` для кодов вне 8.19: `timeout` «LinQ не ответил вовремя: попробуйте позже», `remote_error` = `bad_output` «Неожиданный ответ LinQ», `artifacts_missing` = `texts.ARTIFACTS_MISSING`; `retry_wait` с другим кодом — «Повтор в ЧЧ:ММ».
- S17, `services._infer(job_id, stage, span, model, video, source: Source | None = None)`, `Source = tuple[BackendName, bool]`: сначала ищется ключ задачи (`jobs.backend`, `jobs.fake`), потом ключ текущего бэкенда; прогон пишет артефакт под ключом текущего бэкенда (`backend.name`, `Settings.fake`), не задачи; `_enqueue(video_id, kind, source)`, `_register(camera_id, filename, sha256, size, probe, web_path, source=None)`.
- R20, `video_import(camera_id, path)` → проверка файла, `camera_get`, `_register(camera_id, path.name, *_stage(path))`; `_stage(path) -> tuple[str, int, VideoProbe, str | None]` (sha256, размер, проба, `web_path`) — проверки 8.1, копия в `uploads/` и H.264-копия 8.20, без базы (было: `_video_import(camera_id, path, source)`).
- S17, `demo_build`: бэкенд — `services._backend_instance()` (ленивый `make_backend(settings)`, тесты подменяют `_backend`); видео пакета — `out/videos/<имя файла>`, модель считается один раз на sha256 видео (то же видео у второй камеры берёт тот же артефакт); модели по порядку `detector`, `extra`, `pose`; все видео раскладки проверяются (`NotFound`, `UnsupportedVideo`) до создания `out`.
- S17, `demo_import`: одна транзакция на пакет; сектор и камера — `sector_create`/`camera_create`, калибровка, зоны, правила — `calibration_set`/`zone_create`/`camera_rule_set` с ролью `admin` (зоны пакета — только если у камеры нет ни одной, правило — если нет строки сценария); `DemoPack.backend` — бэкенд первого артефакта (нет артефактов — `Settings.inference_backend`), `fake` — хоть один артефакт фейк; `DemoImportReport.jobs` — новые задачи; `artifact_import`: шаг ключа — `metrics.step`, без `metrics` — `analysis_step(fps)` и нулевые замеры; файл копируется в `artifacts/<cache_key>.jsonl`, строка с тем же ключом обновляется.
- R20, `demo_import`: `_stage` каждого файла видео пакета (один раз на файл) — до транзакции, внутри неё `_register(..., source)`: ffmpeg не держит блокировку базы (было: перекодирование внутри транзакции). Откат транзакции оставляет в `uploads/` и `artifacts/` файлы без строк: имена по sha256 и ключу кэша, следующий импорт или загрузка того же файла берут их же; удалять их на откате нельзя — их может делить загрузка работающего сервера.
- S17, CLI: `demo build` печатает `DemoManifest` без `metrics` артефактов; `serve --seed` вызывает `cli.seed_on_serve()`: `seed_demo`, затем `demo_import`, относительный `demo.pack` — от корня репо (`config.ROOT`), битый пакет — строка в stderr, сервер стартует.
- S17, `store.demo_pack(name)`, `store.demo_packs()` (по `imported_at, id`), `store.sector_by_name(name)`, `store.camera_by_name(sector_id, name)`; `demo.write_manifest` пишет `model_dump_json(indent=2)` + `\n`; тексты `texts.DEMO_*`, `ARTIFACT_INVALID`, `JOB_*`, `JOB_FAILED_TEXTS`.
- R20, фейк LinQ ищет исходное имя видео (`store.video_filename`) только у файлов `uploads/<sha256><ext>`: `demo build` на фейке не открывает базу `data_dir`.

**6.2 Фасад `services`: клип и H.264 (8.20)**

- S18, `services._web_copy(src, sha256, probe) -> str | None`: копия только при `codec` не из `BROWSER_CODECS` и `transcode.enabled`; готовый `uploads/<sha256>.web.mp4` (от прошлой загрузки того же файла, в том числе на другую камеру) берётся без ffmpeg.
- R20, `_register`: новая строка видео получает `web_path`; существующая строка с `web_path = NULL` (видео до S18) получает копию при повторной загрузке или импорте того же файла (было: копия только новой строке).
- S18, `media.transcode`: ffmpeg пишет `<dst>.part` (`-y -v error ... -f mp4`), после проверки `probe_video` файл переименовывается в `dst`; любой отказ удаляет `.part`; лог `transcode: <что>` — логгер `safewatch.media`, уровень WARNING; `RuntimeError` imageio-ffmpeg (нет ffmpeg) = отказ.
- R20, `media.transcode` добавляет `-vf pad=ceil(iw/2)*2:ceil(ih/2)*2` (8.20: команда без фильтра): libx264 с `yuv420p` не кодирует нечётную сторону; копия получает чёрный столбец или строку справа или снизу, пиксели HUD на месте, кадры и длительность прежние.
- S18, `store._EVENTS` добавляет `LEFT JOIN episodes ep`, `analyses an`, `videos v` и столбцы `clip_start_ms`, `clip_confirm_ms`, `clip_video_id`, `clip_duration_ms`, `clip_browser_playable`, `clip_web_path`; `services._clip(row)` строит `Clip` (нет эпизода — `None`), `services._video(row)` — `Video.web_playable = browser_playable or web_path`; `ClipPlayer` с `aria-label="Клип события"`, на экране события — под кадром доказательства, у мастера — после кадра.

**Компоненты анализа и правил: автокалибровка (8.21)**

- S19, `FrameContext.auto_calibration: AutoCalibration | None = None`, `AnalysisResult.auto_calibration: AutoCalibration | None = None`; `pipeline.analyze` вызывает `autocal.fit` по кадрам детектора (классы `person` из `ModelSpec.classes`) на каждом анализе и пересчёте, при ручной калибровке тоже; `services._analyze` пишет `analyses.autocal_json` из `result.auto_calibration`.
- S19, `features.person_states(..., ground=None, autocal: AutoCalibration | None = None)`, `features.vehicle_states(..., ground=None, autocal=None)`: `speed_source = "calibration"` только при метрах по гомографии; иначе при `speed_bh_s`/`speed_vh_s` не `None` и `scale_at` не `None` — `"auto"`; ручная калибровка с точкой вне оболочки → автокалибровка.
- S19, `autocal.fit`: меньше 2 замеров или нулевой разброс `y2` (все ноги в одной строке) — линии нет, `a_px = b = rmse_px = r2 = 0`; «Мало стоящих людей…» проверяется первым; `r2 = 1` при нулевом разбросе высот; «стоит по рамке» — `w > 0` и `h/w ≥ upright_hw`; отступ — минимум из четырёх краёв.
- R20, `autocal.fit`: замеров `≥ min_samples`, а линии нет (все ноги в одной строке) → `texts.AUTOCAL_ONE_ROW = "Все люди стоят в одном ряду кадра: перспективу не оценить"`; `AUTOCAL_PERSPECTIVE` — только `ĥ(0) ≤ 0` или `ĥ(height) ≤ 0` (было: «перспектива» и без линии).
- S19, `Observation.method` = `Episode.method` = `"auto"` у `running` и `proximity` при автокалибровке (`"calibrated"` остаётся за гомографией); `running` пишет в `metrics` наблюдения `autocal_samples` (`running.AUTOCAL_SAMPLES`), `explain` бега берёт N оттуда и убирает её из строк `why_common`; строка `WhyItem("Скорость", ...)` только при `auto` и `calibrated`; `running.near_vehicle_*` при автокалибровке по-прежнему в ростах; `proximity` при `auto` — `distance_m`, `PROXIMITY_M`, `WHY_PROXIMITY_M`.
- S19, тексты `texts.AUTOCAL_FEW = "Мало стоящих людей в кадре: {n} из {need}"`, `AUTOCAL_PERSPECTIVE = "Рост людей не согласуется с перспективой"`, `WHY_SPEED = "Скорость"`, `WHY_SPEED_AUTO = "автокалибровка по росту людей ({n} замеров, точность около ±20 %)"`, `WHY_SPEED_CALIBRATION = "по калибровке камеры"`, `METHOD_TITLES["auto"] = "автокалибровка"`; причина бега при `auto` — прежний `RUN_M` «Бег {v} м/с» (без «≈»).
- S19, `CameraSetupView.auto_calibration`: первое видео `status = ready` с `active_analysis_id` в порядке `store.videos` (новые первыми); `services._autocal(analysis_id) -> AutoCalibration | None` — `None` без анализа и при `autocal_json IS NULL`.

**Компоненты анализа и правил: СИЗ (8.22)**

- S20, тексты `texts.NO_HELMET = "Без каски в зоне «{zone}»"`, `NO_RESPIRATOR = "Без респиратора в зоне «{zone}»"` (имя первой зоны под `anchor`), `SCENARIO_DESCRIPTIONS["no_helmet"] = "Человек без каски в зоне, где каска обязательна."`, `["no_respirator"] = "Человек без респиратора в зоне, где респиратор обязателен."`, `PARAM_TITLES["head_frac"] = ("Верхняя доля рамки человека (голова)", "")`; параметры обоих плагинов: `hold_s` 0..60, `head_frac` 0..1, `min_person_px` 0..2000; `reason_code` P — id сценария, U — `too_small`, `head_unseen`, `owner_ambiguous`.
- S20 и R20, порядок проверок `rules.ppe`: `anchor` вне зоны → `N` (рост не проверяется); рост `< min_person_px` → `U too_small`; к голове привязаны и `no_<сиз>`, и `<сиз>` → побеждает больший `score`, равенство — `no_<сиз>` (было: всегда `P`; модель, колеблющаяся между классами, давала ложный жёлтый); `no_<сиз>` у головы `ambiguous` → `U owner_ambiguous`; `no_<сиз>` привязан → `P`; `<сиз>` `ambiguous` → `U owner_ambiguous`; `<сиз>` привязан → `N`; иначе `U head_unseen`; `explain` — «{reason_text} дольше {hold_s} с» и `why_common`.

**Имя продукта (раздел 2, 6.11.8)**

- R20, `texts.PRODUCT_TITLE` удалён (6.8: не читался с S0; имя продукта — `product_name`); `frontend/index.html` `<title>Argus</title>`, шапка до ответа `meta` — «Argus»; `FastAPI(title="SafeWatch API")` и `info.title` в `contract/openapi.json` не меняются: имя контракта не переименовывается (раздел 2, «Допущения»).

**Тесты (10.3)**

- R20, `tests/test_clips.py::test_odd_frame_and_late_copy` (нечётный mp4v 321×241 пишет сам ffmpeg через `lavfi`: OpenCV пишет только чётные стороны), `tests/test_demo_pack.py::test_import_transcodes_outside_transaction` (`store._depth` в момент `media.transcode`), `tests/test_rule_ppe.py::test_surer_class_wins_on_one_head`.

### 6.13 Дополнения v7 (строки `GAP` S21–S25 и решения R25)

Перенесены ревью R25 из `## open` файла `progress.md`. Статус тот же, что у 6.8–6.12: часть контракта наравне с 6.1–6.6 и 6.11; `было → стало` заменяет сказанное выше.

**Развёртывание (8.32)**

- R25, `docker-compose.yml`: `.env` необязателен — `env_file: [{path: .env, required: false}]` (было: `env_file: .env`, compose без файла не стартовал): сид и демо-пакет ключей не требуют, стенд поднимается на чистой машине; нужен Docker Compose 2.24 или новее (`docs/DEPLOY.md`, «Требования»). `healthcheck` — `python -c` с `urllib.request` из образа (8.32: curl в `python:3.12-slim` нет).

**Компоненты анализа и правил: телефон и груз (8.23)**

- S22, текст тега проекции груза `texts.HUD_LOAD_PROJECTION = "зона под грузом"`; тег `HudTag(code="load_projection", text=HUD_LOAD_PROJECTION, level=None)` у каждого объекта `suspended_load` HUD (имя — `rules.suspended_load.ID`), полигон — из нормированной рамки с обрезкой 0..1; `projection` у остальных объектов `None`.
- S22 и R25, порядок проверок `PhonePlugin`: рост `< min_person_px` → `U too_small`; телефон `ambiguous` → `U owner_ambiguous`; телефона нет → `N`; `anchor` в danger или vehicle_path → красный, `danger_hold_s`, `zone_id` первой такой зоны; иначе `anchor` в `walkway`/`rest` → `N` без `zone_id` и `reason_code`; иначе жёлтый, `hold_s` (было, S22: разрешённая зона побеждает и при перекрытии с danger — проход через пути транспорта гасил красный).

**6.2 Фасад `services`: звонок мастеру и очередь доставок (8.24)**

- S23, `delivery.phone_mask(to: str) -> str` для `Channel.target` звонка: цифры номера; от 11 цифр — `+<код> <3 цифры> ***-**-<2 последние>` («+7 (900) 123-45-12» → `+7 900 ***-**-12`), меньше 11 — `***-**-<2 последние>`, без цифр — `texts.CALL_NO_NUMBER = "заглушка"`; `texts.CALL_SENT = "Звонок отправлен"`, `texts.CALL_DELIVERED_STUB = "Звонок доставлен (заглушка)"`.
- S23, `store.delivery_enqueue(event_id, kind, level, at)` (`INSERT OR IGNORE`, в транзакции вызывающего), `store.delivery_queue()` (по `id`), `store.delivery_dequeue(queue_id)`; `services._delivery(row) -> Delivery` (`status_text` только у `call:<name>`, у webhook `""`); `services._deliveries` удалён (было 6.10 S15), сброс в `tests/conftest.py` убран.
- S23, постановка: `broadcast_tick` — `level` из `EventSummary` сообщения `event.created`/`event.escalated` внутри транзакции тика; `event_action` и `escalation_tick` — `level` строки события, `created_at` — `clock.now()`.
- S23, `deliveries_flush`: каналы `webhook:<name>` по порядку `delivery.webhooks`, затем `call:<name>` по `delivery.calls`; строка очереди удаляется после всех каналов, в том числе когда каналов нет или ни один не подошёл; `event.updated` — после каждой строки канала `call`; `CallChannel.deliver` → `(True, None, "")`, `delivered_at = at` только у успешного звонка.
- S23 и R25, тело webhook — `EventSummary` с `level` строки очереди и `notification_text = texts.notification_text(<level строки>, sector_name, reason_text, escalated_by_timeout and <level строки> = level события)` (было, S23: текущий текст события — жёлтая публикация, эскалированная до flush, уходила с `level: yellow` и текстом «Красная опасность …»). `reason_text` — текущий: текста на момент постановки очередь не хранит.
- S23, `system_view.channels`: webhook-каналы, затем каналы звонка (`kind="call"`); фронт: пункт меню оператора «С телефона» (`/m/operator`), `EventScreen` показывает `status_text` непустых доставок под историей, `ACTION_TITLES` экспортирован из `EventScreen` (кнопки `OperatorMobileEvent`); `MasterInbox` открывает карточку только на уведомление с `id`, оканчивающимся на `:to_master`.

**6.2 Фасад `services`: калькулятор (8.25)**

- S24, `overrides` заменяет у `CalcAssumption` и `value`, и `source`: `texts.CALC_OVERRIDDEN = "задано в расчёте"` (иначе число пользователя шло бы с подписью конфига).
- S24, проверка чисел: `ValidationFailed(texts.CALC_INVALID = "Неверное значение: {field}", field=<поле>)`, у `overrides` поле `overrides.<ключ>`; 0 у делителей `accelerator.capacity_fps`, `accelerators_per_server` (`services.CALC_DIVISORS`) тоже 422; `ScaleIn.cameras_now` и `new_cameras` — от 0 (0 текущих — новое внедрение); роль проверяется до чисел.
- S24, строки расчёта: последний `WhyItem` каждого `TierResult.items` — `("Окупаемость", "<fmt_num> мес.")` или `("Окупаемость", "Не окупается при этих допущениях")`; строки вложений по уровню нарастают (`texts.CALC_ACCELERATORS`, `CALC_SERVERS`, `CALC_INTEGRATION`, `CALC_LIGHT_SOUND`, `CALC_SPEAKERS`, `CALC_NEW_CAMERAS`), `texts.fmt_rub(x)` («500 000 ₽»), количество — целое или `fmt_num`; `texts.CALC_TIER_TITLES` «Базовый», «Расширенный», «Максимальный»; `ScaleResult.items` — добавленные ускорители, серверы, новые камеры; `calculator._ceil` округляет до 9 знаков перед `ceil` (шум float).
- S24, замеры: `store.linq_metrics()` (`metrics_json` артефактов `backend = linq`, `fake = 0`, новые первыми), учитываются только `throughput_fps > 0` (артефакт, импортированный без `metrics`, даёт 0 и делил бы на ноль); `CalculatorDefaults.measured` — ключи `measured.capacity_fps` (медиана, источник `texts.measured_jobs(n)` «замер приложения: N задач»), `measured.tpu_rtt_p50_ms` (медиана `tpu_rtt_p50_ms` последних `RECENT_JOBS` = 20 артефактов), `measured.events_per_camera_day` (`texts.CALC_EVENTS_SOURCE`); нет данных — строки нет; `calculator_scale` берёт `measured.capacity_fps` целиком (значение и подпись).
- S24 и R25, «живая камера» 8.25 — камера, у которой есть событие эфира в окне: `events_per_camera_day = события / камеры с событиями / stats.default_days`, окно `[now − default_days, now)` по `started_at`, `store.broadcast_event_counts(start, end) -> Row(events, cameras)`; подпись `CALC_EVENTS_SOURCE` так и говорит («на камеру с событиями»). R25 оставил это чтение: камеру «в эфире» в окне точно не посчитать — у строки `broadcasts` со статусом `ended` нет времени конца; тихие камеры в эфире завышают нагрузку на оператора, это сторона запаса.
- S24, подпись примера «пример для демо, замените своими» показывает экран Егора: у `CalculatorDefaults` поля под неё нет, текст в `texts` не заведён (был бы мёртвым кодом); пример завода — `services.CALC_EXAMPLE`, `ScaleIn` — 8 + 8. На допущениях 6.11.8 пример даёт базовый уровень «не окупается» (экономия 1 200 000 ₽ ≤ поддержка 1 455 000 ₽ в год), расширенный — 377,1 мес., максимальный — 134,8 мес.: это расчёт по контракту, числа для показа меняет владелец (`config/user.yaml` или `overrides`).

**6.2 Фасад `services`: датасет ложных срабатываний (8.26)**

- S25, `dataset.item_path(event_id)` → `datasets/false_alarms/<event_id>/` (колонка `dataset_items.path`), `dataset.MANIFEST = "manifest.json"`; `store.dataset_pending()` (события `false_alarm` по статусу или вердикту, с эпизодом, без строки `dataset_items`, по `id`), `store.dataset_items()` (по `id`); `build_item(root, event, episode, video, det, pose, hud, frame_ms, label)`: `frame_ms` — `ts_ms` отобранных проанализированных кадров (отбор в `services._dataset_files` в том же потоке: кадры `hud.jsonl` в окне клипа `[start_ms, end_ms]` включительно, при избытке `window[i * n // max_frames]`), `label` — `video_sha256`, `video_filename`, `models`, `analysis_version`, `comment`; остальные поля `label.json` `build_item` берёт из события и эпизода.
- S25, `label.json`: `start_ms`/`end_ms` — эпизода (время видео), `models` — `model_id@model_version` артефактов анализа (детектор, pose, extra), `comment` — комментарий последнего действия `false_alarm`; JPEG кадров полного размера (`max_width` = ширина кадра), качество `evidence.jpeg_quality` `dataset.py` читает из конфига.
- S25, `datasets_flush` ловит `OSError` и `ValueError` (кадр, файл): лог `dataset: event <id>: <что>`, папка элемента меняется только после чтения всех кадров; следующий тик повторяет.
- S25 и R25, `async def dataset_export(out: Path | None = None) -> Path` (было, 6.11.4: `def`; zip на 40 кадров элемента писался в потоке event loop и останавливал эфир и WebSocket): элементы читаются в потоке event loop, `dataset.export_zip` — в `asyncio.to_thread`; пишет `<out>/false_alarms.zip`, без `out` — `data_dir/datasets/false_alarms.zip`; пути в zip от `data_dir` (как `DatasetItem.path`), `manifest.json` в корне; CLI `dataset export` — `asyncio.run(services.dataset_export(out))`.

**6.4 REST: файловые маршруты (6.11.6)**

- R25, `api.ZIP_FILE`, `api.PDF_FILE` — `responses` декоратора `{200: {"content": {"application/zip": {}}}}` и то же с `application/pdf`: `contract/openapi.json` описывает тип файла рядом с прежним `application/json` (только добавление, фронт Егора 1.1.0 не ломается); искомая строка трассировки 6.7 маршрута — `@router.get("<путь>"` без закрывающей скобки (было: `@router.get("<путь>")`, `responses=` её ломал). `GET /api/master/shift.pdf` получил `PDF_FILE` заранее (S30 строит маршрут).

**Тесты (10.3)**

- R25, `tests/test_rule_phone.py::test_phone_allowed_in_walkway_and_rest` (проход поверх danger и vehicle_path — красный), `tests/test_delivery.py::test_level_fixed_at_enqueue` (текст тела по уровню строки), `tests/test_contract_files.py::test_openapi_only_grows` (`application/zip`, `application/pdf` у файловых маршрутов).

### 6.14 Дополнения v8 (строки `GAP` S26–S30 и решения R30)

Перенесены ревью R30 из `## open` файла `progress.md`. Статус тот же, что у 6.8–6.13: часть контракта наравне с 6.1–6.6 и 6.11; `было → стало` заменяет сказанное выше.

**6.2 Фасад `services`: идентификация нарушителя (8.27)**

- S26, тексты идентификации: `texts.IDENTITY_TOO_LONG = "Поле: до 80 символов"` (`ValidationFailed(..., field=<поле IdentityIn>)`), `texts.IDENTITY_CLEARED = "Идентификация очищена"`, `texts.identity_comment(person_name, person_position, crew) -> str` — «ФИО: …; должность: …; бригада: …», пустое поле — `texts.IDENTITY_EMPTY = "—"`, все три пустые — `IDENTITY_CLEARED`.
- S26, журнал: `texts.ACTION_TITLES` + `"identified": "идентификация"` (история CSV падала бы `KeyError`); `texts.CSV_COLUMNS` + «ФИО», «Должность», «Бригада» в конце (значения `EventSummary.person_name`, `person_position`, `crew`).
- S26, `services._stats_period(date_from, date_to) -> tuple[datetime, datetime]` — период и проверка `PERIOD_INVALID` `ohs_stats_view` вынесены для `people_stats_view` без изменения поведения.
- S26, `PeopleStats.total` — все события периода (как `OhsStats.total`: без `superseded`, демо по `include_demo`); `by_person`/`by_crew` — `CountRow` с `key = title` = значение поля; `X-Actor` по умолчанию — `texts.DEMO_ACTOR[role]`, как у `event_action`; `event.updated` только при изменении.
- R30, одновременные `PATCH /identity`: `event_identify` синхронна и идёт в потоке event loop целиком (без `await`), второй запрос сравнивает поля с уже записанными первым; разные значения дают две строки `identified`, последняя побеждает, как у `event_action`.

**Компоненты анализа: паспорт камеры (8.28)**

- S27, `build_passport` получает ширину кадра (большая сторона рамки `cell phone` в px, рамки HUD нормированы по ширине и высоте): `..., duration_ms: int, height: int, metas, ...` → `..., duration_ms: int, width: int, height: int, metas, ...`; `services.camera_passport` передаёт `width`/`height` строки видео и `int(features.min_person_px)` (в конфиге float, в сигнатуре int).
- S27, `passport.ZONE_REQUIRED = ("fence_crossing", "restricted_under", "no_harness", "no_helmet", "no_respirator")`, `passport.PHONE = "phone"`; правило 6 — у камеры нет ни одной живой зоны из `ScenarioMeta.zone_kinds`; типы в «Нет зон: …» — `title` из `config.get_settings().zone_kinds` через «, » в порядке `zone_kinds`.
- S27, тексты `texts.PASSPORT_NO_VIDEO`, `PASSPORT_MODEL_MISSING`, `PASSPORT_FEW_FRAMES`, `PASSPORT_DARK`, `PASSPORT_PEOPLE_TINY`, `PASSPORT_NO_PEOPLE`, `PASSPORT_PHONE_POOR`, `PASSPORT_NO_ZONES` — дословно 8.28; правило 7: `PASSPORT_PEOPLE_SMALL = "Люди мелкие для уверенной оценки: {px} px"`, `PASSPORT_DARK_PARTIAL = "Темно или камера закрыта {pct} % времени"`, `PASSPORT_EMPTY = "Пустые кадры: {pct} % записи"`, несколько причин — через «; »; `PASSPORT_SUITABLE = "Годна"`; N px — целая часть, N % — `round(доля × 100)`; `skeleton` → `ScenarioMeta.status_text`.
- S27, расчёт: «сценарий на людях» — `person` в `required_classes`; правило 7 по росту только для них, тёмная и пустая доли — для всех; медианы px округляются до 0,1 (нормированные рамки дают 79,99999 вместо 80); `dark_share` — сумма интервалов `dark`/`obstructed`, обрезанных по `[0, duration_ms]`, делённая на `duration_ms` (`stale` не считается); телефон без рамок `cell phone` в записи — проверка объекта правила 5 пропускается (рост людей проверяется); статусы плагинов — текущие `rules.scenario_metas()`, а не снимок анализа; без анализа метрики `None`, `frames = 0`.
- R30, `camera_passport` читает `hud.jsonl` анализа в потоке event loop (маршрут `async def`), оставлено: ~28 мкс на кадр (сцена PPE, 261 кадр — 7 мс; 10 минут при 12 кадр/с — около 0,2 с), ролики демо до 60 с.
- R30, S32 снят владельцем (раздел 16): `CameraPassport.shift_px = None`, `shift_text = ""` всегда; поля, ключи `shift.*` и `media.frame_shift` остаются в контракте 1.1.0 (контракт только растёт), строки трассировки S32 сверка не проверяет (слайс не закрыт).

**6.1 Бэкенд LinQ под медленную очередь (8.29)**

- S28, таймаут: `linq.job_timeout_s(linq: LinqConfig, frames: int) -> float` и `linq.START_S = 120` (формула 8.29); `frames` — `ceil(frame_count / step)`, `frame_count` из `media.probe_video` (видео не читается — 0, остаётся `job_timeout_s`); отсчёт, как и раньше, от начала `run` (с загрузкой).
- S28, прогресс: `linq.rate_eta(done, total, elapsed_s) -> (rate_fps, eta_s)` (`None, None` при `done = 0`; rate округлён до 0,01, eta до 0,1 с); `LinqBackend.live: tuple[int, int, float] | None` — (done, total, секунды с `# sw:start`) текущей модели, `total = ceil(n_total / step)` из `.progress`, до первого файла — из пробы видео; колбэк прогресса `services._infer` читает `backend.live` (только `LinqBackend`) и передаёт `_progress(job_id, value, live=None)`; `services._live: dict[int, tuple[int, int, float]]` в памяти (сброс в фикстуре `conn`, `pop` после `run`); `_job` у задачи `running` с записью в `_live` заполняет `rate_fps`, `eta_s`, `status_text`.
- S28, тексты: `texts.JOB_WAIT_TPU = "LinQ: ждём первый ответ TPU (очередь площадки)"`, `texts.job_progress_text(done, total, rate_fps, eta_s) -> str`; минуты `max(1, round(eta_s / 60))`, кадр/с — `fmt_num` (одна цифра после запятой).
- S28, `LinqBackend._start_command(absdir, remote_out, args) -> str` (staticmethod); гашение в фигурных скобках `{ [ -f <out>.pid ] && kill $(cat <out>.pid) 2>/dev/null; rm -f <out>.pid; } &&`, до `rm -f <out>.progress`; `FakeRemoteShell._start` разбирает команду от `(setsid`.
- S28, HTML: `JupyterError`, в тексте которого `<html` без учёта регистра, или `requests.JSONDecodeError` → `InferenceError("bad_output")` и сброс сессии (`_drop`), как у сетевой ошибки; `LinqBackend.check` на `bad_output` → `bad_answer` с `texts.LINQ_BAD_ANSWER`.
- S28, `close()`: `JupyterShell.close` = `_drop()` (`shutdown_kernel`, ошибки глушатся, без сессии — ничего); `LocalBackend.close` ничего не делает (сессия onnxruntime живёт один прогон); `services.backend_close()` не обнуляет `_backend`; doctor зовёт его в `finally` вокруг проверок, lifespan — `asyncio.to_thread` после остановки цикла задач.
- R30, `# sw:start` гасит pid из `<out>.pid`, не проверяя, что это воркер: риск попасть в чужой процесс с тем же pid принят (`<out>` уникален по ключу кэша, файл pid живёт один прогон, живой прогон R32 проверяет команду как есть).
- R30, `rate_fps` и `eta_s` считаются от `# sw:start` и включают запуск воркера и первую пачку: в начале ETA завышена (S28: 61 с на 25 кадрах при 34 с факта), это сторона запаса, оставлено.

**6.2 Фасад и анализ: пробелы `docs/ML_INTEGRATION.md` (8.30)**

- S29, откат extra-модели и на `model_missing` (нет программы TPU, хвоста или ONNX): 8.30 п. 10 `remote_error`/`bad_output` → `remote_error`/`bad_output`/`model_missing`; модель огня Матвея без `linq_program` на `linq` иначе валила бы задачу. `error_text` готовой задачи — откаты через «; » (extra в порядке `pipeline.extra`, затем `pose: …`), обрезка до `ERROR_TEXT_MAX`.
- S29, `services._analysis_config(video, camera_id, extra_ids: list[int])` → `_analysis_config(video, camera_id, extra: list[tuple[ModelSpec, int]])`; `active_classes` — классы `registry.active_models` без моделей `pipeline.extra`, которых нет в `extra` (откат; пересчёт снимка, сделанного до добавления модели в `extra`).
- S29, `Job.metrics`: детектор, pose, затем extra в порядке `AnalysisConfig.extra_artifact_ids` анализа задачи (`jobs.analysis_id`; без анализа — без extra), `cached` по правилу `created_at < started_at`.
- S29, `rules.ANY_VEHICLE = {"proximity"}`; `scenario_metas` отдаёт у `proximity` `required_classes = ["person", *pipeline.vehicle_classes]`, текст `model_missing` без техники перечисляет все `vehicle_classes`; `analysis.pipeline.VEHICLES` удалён.
- S29, команда воркера: `--input-name` только при `input_name != "images"`; детектор с `nc` — `--nc <nc>` и `--classes` из id `classes` меньше `nc`; `LocalBackend`: `nc = model.nc or 80` для detect и тот же фильтр; `FakeRemoteShell` отдаёт пустые кадры только при `--nc` без `--classes`.
- S29, CLI `import-artifact`: без `--backend` — `INFERENCE_BACKEND`; вывод — id артефакта одной строкой; `NotFound` → 3, `ValidationFailed` → 2.
- S29, `config/models.yaml` + запись `matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4` (пакет video-first v2: detect, 640, conf 0.25, iou 0.45, `{0: smoke, 1: fire}`, `linq_program: null`, хвост и ONNX в `models/matvey/matvey-fire-smoke-yolov8n/640-s04-v1-4c9f5d05c4d4/`), в `pipeline` `default.yaml` не входит; `config/user.matvey.example.yaml` — включение комментарием; в реестре 6 моделей.
- R30, `store._JOBS` получает столбец `extra_metrics` — `json_group_array(json_array(e.key, x.metrics_json, x.created_at))` по `json_each(analyses.config_json, '$.extra_artifact_ids')` анализа задачи; `services._job` сортирует по индексу снимка (было, S29: чтение `analyses` и `artifacts` на каждую задачу, `jobs_list` до 50 × (1 + число extra) запросов).
- R30, `eval_run`: extra-модель с `remote_error`/`bad_output`/`model_missing` → анализ без неё, `log.warning("eval: <файл>, extra <ref>: <текст>")`, её сценарии — `model_missing` в этом анализе (было: exit 4). `demo_build` на ошибке extra по-прежнему падает целиком и удаляет `out` (8.19 п. 4: полупакета нет; текст ошибки называет модель).

**Отчёт смены и долги приложения (8.31)**

- S30, трекер: этап 3 `Tracker._reattach(tracks, dets, ts_ms)` после двух этапов IoU: треки без пары (подтверждённые и предварительные) и детекции `score ≥ high_thresh` без пары; расстояние центров прогноза трека и детекции `< reattach_bh × высота рамки трека`, назначение венгерским алгоритмом по расстоянию; `reattach_bh = 0` — этап ничего не сопоставляет (прежнее поведение).
- S30, `explain`: `proximity_zone` → `texts.WHY_HOLD` с `red_hold_s` («Человек в зоне «X» дольше N с»); `fence_crossing` → `texts.WHY_FENCE = "{rule}; момент виден при разрыве наблюдения до {s} с"` (`max_gap_s`); `phone`, `restricted_under`, `fire_smoking`, `no_harness`, `suspended_load` уже давали правило с порогом в секундах (`WHY_HOLD`), измеренное значение — строки `why_common` (`METRIC_TITLES` с единицей), зона — в тексте причины.
- S30, загрузка: `services.UPLOAD_SLACK = 64 × 2^10` (рамка multipart сверх файла), `services.video_upload_check(role: Role | None, content_length: int | None) -> None`: роль как у `video_upload`, `Content-Length > upload.max_mb × 2^20 + UPLOAD_SLACK` → `TooLarge`; точная проверка размера файла при записи (8.1) прежняя, граница `test_upload_limit_boundary` не изменилась. `api._UploadGuard` — ASGI-middleware на `POST` пути `api.UPLOAD_PATH = re.compile(r"/api/cameras/[^/]+/videos")`: FastAPI разбирает multipart во временные файлы до зависимостей. Порядок ошибок загрузки: роль (400/403) → `Content-Length` (413) → камера (404) → расширение (415).
- S30, `cli._server_running() -> bool` (процесс `server.pid` жив и `create_time` совпадает); `cli.evaluate` проверяет его первым: exit 5, stderr `texts.EVAL_SERVER_RUNNING = "Остановите сервер: uv run safewatch stop"`.
- S30, `eval_run`: pose `remote_error`/`bad_output` → анализ без точек и `log.warning` (в отчёте не отражается); остальные коды pose и любая ошибка детектора → `InferenceError`, exit 4, как раньше.
- S30, PDF: `services.shift_report_name(at: datetime) -> str` — `shift-<YYYY-MM-DD>-<shift_id>.pdf`, дата — локальная (`timezone`) дата начала смены; маршрут берёт один момент `at or clock.now()` для файла и имени. `report_pdf`: шрифт одним начертанием (заголовки таблиц не жирные), ширины колонок 85/35/35/35 и 25/35/35/65/30 мм; тексты `texts.PDF_TITLE = "{product} · Сводка смены"`, `PDF_SHIFT = "Смена: {title}"`, `PDF_PERIOD = "Период: с {start} до {end} (МСК)"` (`ДД.ММ.ГГГГ ЧЧ:ММ`), `PDF_TOTAL = "Всего событий: {n}"`, `PDF_BY_SECTOR = "По секторам"`, `PDF_BY_SCENARIO = "По сценариям"`, `PDF_SECTOR = "Сектор"`, `PDF_SCENARIO = "Сценарий"`, `PDF_COUNT_HEAD = ("Всего", "Подтверждено", "Ложные")`, `PDF_CONFIRMED = "Подтверждённые события"`, `PDF_EVENTS_HEAD = ("Время", "Сектор", "Камера", "Причина", "Статус")`; время события `ДД.ММ ЧЧ:ММ` по `timezone`.
- S30, зависимости: `fpdf2>=2.8.9` (тянет `pillow`, `fonttools`, `defusedxml`), dev `pypdf` (текст PDF в тесте); `.gitattributes` + `*.ttf binary`; `tests/test_api_skeleton.py::test_unbuilt_route_returns_501` подменяет `services.shift_report_pdf` заглушкой `NotImplementedError("slice 30")` (все маршруты построены, как в S13), `V5_REQUESTS` удалён.
- R30, `async def shift_report_pdf(at: datetime | None = None) -> bytes` (было, 6.11.4: `def`): сводка читается в потоке event loop, `report_pdf.shift_pdf` — в `asyncio.to_thread`; маршрут ждёт `await`. Замер: 2 события — 50–80 мс, 100 — 0,3 с, 300 — 0,9 с, 1000 — 2,9 с; в потоке event loop это останавливало эфир и WebSocket.
- R30, `api.UPLOAD_PATH` сверяет путь отдельно от маршрута FastAPI, оставлено: переименование маршрута загрузки ловит `tests/test_videos.py::test_upload_rejected_before_body` (тест идёт по пути маршрута).
- R30, этап 3 трекера: риск, что детекция соседа ближе `reattach_bh` роста перенимает id трека, потерявшего пару по IoU, принят; `tracker.reattach_bh: 0` выключает этап.
- R30, сцена ur-fall-03-cam0 (UR Fall, 320×240, рост человека ~230 px, `local`, COCO pose и pose Матвея): эпизода падения нет, код верен по 8.2–8.4. Человек падает на 6,05 с, ролик кончается на 7,17 с, а `confirm_s = 2,0` с; угол торса после падения скачет между `lying`, `unknown` и `upright` (6,40–6,47 с: торс < 30° при рамке шире высоты в 1,8 раза), `N` сбрасывает кандидата. При `confirm_s = 0,2` эпизод есть (6,10–6,30 с). Демо падения требует ролика, где человек лежит после падения не меньше `confirm_s`.

**Очередь (16)**

- Владелец, 25.10: S31 и S32 сняты из очереди; после R30 идёт только R32 — финальная проверка (короткий живой прогон LinQ, готовность к демо). Строка long-lead про ресёрч доп-сценариев снята вместе с S31.

**Тесты (10.3)**

- R30, `tests/test_eval.py::test_eval_extra_fallback` (extra-модель `remote_error` в `eval`: отчёт без неё, детектор и pose на месте).

### 6.15 Решения R32 (v9)

Строк `GAP` после R30 нет. Решения ревью R32; статус тот же, что у 6.8–6.14.

- R32, CLI (8.29, было → стало): `services.backend_close()` зовут ещё `cli.demo_build` и `cli.evaluate` в `finally` — процесс CLI с бэкендом `linq` оставлял idle kernel на общем аккаунте Jupyter. Тест: `tests/test_demo_pack.py::test_cli_build_and_import`.
- R32, раскладка демо-пакета (8.19 п. 1, было → стало): два видео раскладки с одним именем файла в разных папках (`a/original.mp4`, `b/original.mp4`) → `ValidationFailed(texts.DEMO_LAYOUT_INVALID.format(field="file"), field="file")` до записи; было: второе видео молча получало копию первого (`out/videos/<имя>`). Тест: `tests/test_demo_pack.py::test_build_writes_manifest_and_artifacts`.
- R32, оставлено: зоны пакета не пишутся на камеру, у которой уже есть зоны (8.19 п. 3); у камер сида 1.1, 1.2, 2.1, 3.1, 3.2, 4.1 свои зоны, поэтому раскладка с реальной сценой берёт новую камеру или камеру сида без зон (2.2, 4.2).

---

## 7. Общие компоненты

Компонент собирается в слайсе из столбца «Слайс» (0 — каркас; иначе первый слайс, которому он нужен) и дальше переиспользуется, а не пишется заново. Компонент, который не использует ни один слайс, не пишется.

| Компонент | Где | Интерфейс | Слайс | Используют |
| --- | --- | --- | --- | --- |
| ошибки | `errors.py` | `AppError(message, **details)`, наследники 6.2, `InferenceError(code, message)` | 0 | все слои |
| часы | `clock.py` | `now() -> datetime` (UTC), `iso(dt) -> str`, `parse(s) -> datetime`, `local(dt, tz) -> datetime` | 0 | все слои |
| хранилище | `store.py` | `tx()` (контекст транзакции), `one(sql, *args)`, `all(sql, *args)`, `run(sql, *args) -> int`; функции запросов по сущностям | 0 (функции — по слайсам) | `services`, `seed` |
| тексты | `texts.py` | словари `STATUS_TITLES`, `LEVEL_TITLES`, `ROLE_TITLES`, `DEMO_ACTOR`, `NO_OBSERVATION_TEXTS`; `fmt_num(x) -> "3,1"`; `notification_text(...)` (S6) | 0 | `services`, `analysis/hud`, `rules` |
| WS-хаб | `hub.py` | `Hub.connect(role) -> Client`, `Hub.disconnect(client)`, `Hub.publish(type: WsType, data: BaseModel, audience: list[Role] \| None = None)`; очередь клиента `CLIENT_QUEUE` | 0 | `api`, `services` |
| реестр моделей | `registry.py` | `load_models(path) -> list[ModelSpec]`, `resolve(ref: str, models: list[ModelSpec] \| None = None) -> ModelSpec`, `active_models(settings) -> list[ModelSpec]`, `active_classes(settings) -> list[str]` | 0 | `services`, `doctor`, `rules` |
| фейки | `fakes/remote.py`, `fakes/scenes.py` | 6.1 | 0 | тесты, режим `SAFEWATCH_FAKE=1` |
| фикстуры тестов | `tests/conftest.py` | `conn`, `settings`, `core`, `fake_core`, `client` (FastAPI с lifespan, README шаблона), `fake_clock` (подменяет `clock.now`, `advance(s)`), `make_video(tmp_path, seconds, fps, size) -> Path` (OpenCV пишет mp4v), `side_effects` | 0 | все тесты |
| медиа | `media.py` | `probe_video(path) -> VideoProbe` (S2), `read_frame(path, frame_idx) -> ndarray` и `encode_jpeg(img, quality, max_width) -> bytes` (S5), `sample_luma(path, every_s) -> list[tuple[int, float, float]]` (S11) | 2 | `services`, `analysis` |
| артефакты | `inference/artifacts.py` | `cache_key(...)`, `read_jsonl(path, expected_frames: int \| None) -> list[FrameDetections]` | 2 | бэкенды, `analysis` |
| геометрия | `analysis/geometry.py` | `point_in_polygon`, `iou`, `ioa`, `point_rect_distance`, `point_segment_distance` (S4); `homography`, `apply_h`, `hull_contains`, `grid_segments` (S9); `segment_crossing` (S10) | 4 | `features`, `rules`, `services` |
| помощники плагинов | `rules/base.py` | `zones_at(ctx, point, kinds) -> list[Zone]`, `attach_objects(ctx, name, params) -> dict[int, ObjectState \| Literal["ambiguous"]]` (S10), `obs(...)` — сборка `Observation` | 5 | `rules/*` |
| фронт: API | `frontend/src/api/client.ts`, `useApi.ts`, `ws.ts` | `api` (openapi-fetch с типами `schema.d.ts`, заголовки `X-Role` и `X-Actor`), `apiError(e) -> {code, message}`, `useApi(fn, deps) -> {data, error, loading, reload}`, `useWs(handler)` с переподключением через 1, 2, 4, 8 с | 0 | все экраны |
| фронт: роль | `frontend/src/roles.ts` | `useRole() -> [role, setRole]`, хранение в `localStorage` в try/catch | 0 | шапка, клиент |
| фронт: каркас | `components/AppShell.tsx`, `RoleSwitcher.tsx`, `StubNotice.tsx`, `Badges.tsx` | `AppShell` (шапка: продукт, роль, бейдж бэкенда и «фейк», часы МСК), `RoleSwitcher`, `StubNotice({slice, title})`, `LevelBadge({level})`, `StatusBadge({status})` | 0 | все экраны |
| фронт: формы и таблицы | `components/Form.tsx`, `DataTable.tsx` | `Modal`, `FormField`, `ConfirmDialog`, `DataTable<T>({columns, rows, empty})` | 1 | админка, журнал |
| фронт: HUD | `components/hud.ts`, `HudCanvas.tsx`, `VideoWithHud.tsx` | `layoutHud(frame, zones, grid, size, visible) -> DrawOp[]` (чистая функция), `HudCanvas({ops, size})`, `VideoWithHud({videoId, src, positionMs?, zones, grid})`; клавиша `H` и кнопка скрывают HUD | 4 | камера, событие, мастер, настройка |
| фронт: эпизоды | `components/Timeline.tsx`, `EvidenceImage.tsx` | `Timeline({episodes, durationMs, onSeek})`, `EvidenceImage({evidence, hudVisible})` | 5 | настройка камеры, камера, событие, мастер |
| фронт: оповещения | `components/sound.ts`, `Toasts.tsx`, `TakeoverOverlay.tsx`, `EventFeed.tsx`, `SectorTile.tsx` | `playSound(kind: Sound)` (WebAudio), `Toasts`, `TakeoverOverlay`, `EventFeed({items})`, `SectorTile({state})` | 6 | оператор, мастер |
| фронт: редактор точек | `components/PolygonEditor.tsx` | `PolygonEditor({image, mode: "points" \| "polygon" \| "line", value, onChange, maxPoints})` | 9 | калибровка, зоны |
| фронт: фильтры | `components/FiltersBar.tsx` | `FiltersBar({facets, value, onChange, onReset, shown, total})` | 12 | журнал |
| фронт: графики | `components/Charts.tsx` | `BarChartCard`, `LineChartCard`, `StackedDaysCard`, `PercentilesCard` (recharts) | 13 | статистика, менеджмент |
| v5: демо-пакет | `demo.py` | `read_manifest`, `write_manifest`, `MANIFEST` (6.11.9) | 17 | `demo_build`, `demo_import` |
| v5: перекодирование | `media.py` | `transcode(src, dst, cfg) -> bool`, `WEB_SUFFIX` | 18 | `video_upload`, `video_import`, `demo_import` |
| v5: автокалибровка | `analysis/autocal.py` | `fit`, `scale_at` | 19 | `analyze`, `features`, паспорт |
| v5: привязка к голове | `rules/base.py` | `head_objects(ctx, name, head_frac)` | 20 | плагины СИЗ |
| v5: калькулятор | `calculator.py` | `rollout`, `scale` | 24 | `services` |
| v5: датасет | `dataset.py` | `build_item`, `export_zip` | 25 | `services` |
| v5: паспорт | `analysis/passport.py` | `build_passport` | 27 | `services` |
| v5: PDF | `report_pdf.py` | `shift_pdf(summary, product_name, tz) -> bytes` | 30 | `services` |
| v5: фронт: клип | `components/ClipPlayer.tsx` | `ClipPlayer({clip})`: `<video>` с `src = apiUrl(clip.url)`, пауза на `end_ms`, подпись «Видео не воспроизводится браузером», если `playable=false` | 18 | экран события, мастер, оператор с телефона |

## 8. Поведение

### 8.1 Загрузка и обработка видео

Загрузка (`video_upload`, `video_import`):
1. Расширение (без учёта регистра) не из `upload.extensions` → `UnsupportedVideo`.
2. Поток пишется во временный файл `uploads/.tmp-<uuid>` с подсчётом sha256 и размера. Размер больше `upload.max_mb × 2^20` байт → файл удаляется, `TooLarge`.
3. `media.probe_video` открывает файл OpenCV: не открылся, `frame_count ≤ 0`, `fps ≤ 0` или первый кадр не читается → файл удаляется, `UnsupportedVideo` («Видео не читается»). `codec` — FourCC в нижнем регистре, `browser_playable = codec in BROWSER_CODECS`.
4. Файл переименовывается в `uploads/<sha256><ext>` (существующий такой файл не перезаписывается).
5. Видео с тем же `sha256` у этой камеры уже есть: `reused=true`; статус `ready` → `job=None`; `uploaded`/`processing` → текущая задача; `failed` → новая задача `process`.
6. Новое видео: статус `uploaded`, задача `process` (`backend` и `fake` из `Settings` на момент постановки), WS `job.progress`.

Шаг кадров: `step = max(1, floor(fps / pipeline.target_analysis_fps))`. При 25 fps шаг 2 (12,5 кадра/с), при 30 — 2, при 60 — 5, при 10 — 1. Конфиг, где `target_analysis_fps < min_analysis_fps`, не загружается (ошибка запуска).

`run_next_job` (одна задача за раз, вызывает `worker`):
1. Берёт самую старую задачу `queued` или `retry_wait` с `next_attempt_at ≤ now`; ставит `running`, `attempts += 1`, `started_at`; видео → `processing`.
2. Стадии и доля прогресса: `inference_detect` 0–0,45; `inference_pose` 0,45–0,85; `analysis` 0,85–0,95; `evidence` 0,95–1. До слайса 4 после pose задача сразу `done`. Каждый вызов `progress` бэкенда и смена стадии публикуют `job.progress`.
3. Для детектора и pose-модели: `cache_key`; есть строка `artifacts` и файл → бэкенд не вызывается (`cached=true`). Иначе `await asyncio.to_thread(backend.run, ...)`, затем строка `artifacts`. Задача `recompute` инференс не запускает: артефактов нет → `failed`, `artifacts_missing`.
4. Ошибка `InferenceError` детектора или `linq_unavailable`/`timeout` у pose-модели:
   - `linq_unavailable`, `timeout`, `remote_error`: `attempts < jobs.max_attempts` → `retry_wait`, `next_attempt_at = now + retry_backoff_s[min(attempts − 1, len − 1)]`; иначе `failed`;
   - `bad_output`, `model_missing`, `video_unreadable`: сразу `failed`;
   - любое другое исключение: `failed`, `internal`, в `error_text` первая строка, полный трейс в лог.
5. Ошибка pose-модели `remote_error` или `bad_output`: анализ идёт без ключевых точек, `pose_artifact_id = NULL`, `error_text = "pose: <текст>"`, задача не падает.
6. С слайса 4: стадия `analysis` (`await asyncio.to_thread(analysis.pipeline.analyze, ...)`), новая строка `analyses` (версия = последняя + 1), файл HUD, `videos.active_analysis_id`; с слайса 5 эпизоды и стадия `evidence`; с слайса 6 автостарт эфира (8.5); с слайса 9 `superseded` для задачи `recompute` (8.12).
7. Конец: `done`, `progress=1`, `finished_at`, видео `ready`; при `failed` видео `failed`.

`LinqBackend.run`: команды и опрос по 6.1. Тихих ретраев внутри нет: повтор делает очередь. Перед стартом проверяет локальный файл хвоста: нет → `InferenceError("model_missing")`. Хвост лога содержит `not readable` (ошибка LinQ `-3 … TPU program file is not readable`) → `model_missing`; `status -3` без этих слов → `remote_error` (v2). `.progress` → доля `done / ceil(n_total / step)`; `finished` → 1. Остановка без `finished` → `remote_error` с последней строкой лога. Таймаут прогона → `# sw:kill`, затем `timeout`. Скачанный JSONL проверяет `read_jsonl(path, expected_frames=summary.frames_processed)`: строка не JSON, нет поля, `frame_idx` не растёт, число строк не равно ожидаемому → `bad_output`. Метрики берутся из summary воркера и `end_to_end_s`.

`LocalBackend.run`: тот же цикл, что `video_worker.py`, но в процессе: OpenCV читает каждый `step`-й кадр, `yolo_io.preprocess` → onnxruntime (`model.local_onnx`, `intra_op_num_threads = local.threads`) → `yolo_io.postprocess` с `conf`, `iou`, `classes` из реестра → та же строка JSONL; summary с `throughput_fps`, `preprocess_ms`, `postprocess_ms`, без RTT и upload. Нет файла ONNX → `model_missing`. Прогон на `local` в UI подписан «CPU, не LinQ».

### 8.2 Анализ: от детекций к признакам

`analysis.pipeline.analyze(det, pose, video_path, config: AnalysisConfig, pose_model, det_model) -> AnalysisResult` — чистая функция без базы и часов (видео читается только в S11 для `sample_luma`).

1. Кадры детектора и pose совмещаются по `frame_idx`; кадра pose нет → у людей этого кадра нет ключевых точек. Имена классов берутся из `ModelSpec.classes`; класс вне карты отбрасывается.
2. Люди — детекции `person` со `score ≥ tracker.low_thresh`. Ключевые точки прикрепляются жадно по IoU рамок детектора и pose ≥ `pose.match_iou`.
3. Техника — `car`, `bus`, `truck`, `train` со `score ≥ class_conf[name]`. Остальные классы (телефон, классы моделей `pipeline.extra`) — объекты без трекинга со `score ≥ class_conf[name]` (нет ключа → `ModelSpec.conf`).
4. Трекер (`Tracker`, отдельный экземпляр для людей и для техники, общий счётчик id с 1):
   - перед сопоставлением удаляет треки, у которых `ts − last_seen > tracker.max_lost_s` (строгий TTL по времени источника);
   - прогноз рамки: постоянная скорость центра по двум последним обновлениям, размер прежний;
   - этап 1: детекции `score ≥ high_thresh` против треков, стоимость `1 − IoU`, `linear_sum_assignment`, пары с `IoU < min_iou` отбрасываются;
   - этап 2: оставшиеся треки против детекций `low_thresh ≤ score < high_thresh`;
   - несопоставленные детекции `score ≥ new_track_thresh` открывают предварительный трек; он подтверждается после `min_hits` сопоставлений подряд, предварительный трек без сопоставления удаляется;
   - наружу выходят только подтверждённые треки, сопоставленные в этом кадре; прогноз — не наблюдение.
5. Признаки человека (`features.person_states`):
   - `foot` — низ-центр рамки; `anchor` — нижняя видимая лодыжка (точки 15, 16 с `conf ≥ pose.kpt_conf`), иначе `foot`; `feet_visible` — видна лодыжка, а без pose — низ рамки не касается нижнего края кадра (отступ больше 2 px);
   - поза: с pose (плечи 5, 6 и бёдра 11, 12 видимы) угол торса от вертикали `torso_deg`; `≥ lying_torso_deg` → `lying`, `< upright_torso_deg` → `upright`, иначе `unknown`; без pose по рамке: `h/w ≥ upright_hw` → `upright`, `w/h ≥ lying_wh` → `lying`, иначе `unknown`;
   - `ref_height_px` (H_ref): медиана высот рамки за последние `ref_window_s` в позе `upright`; в позе `lying` замораживается; до первой вертикальной позы — текущая высота;
   - скорость: точки `foot` за последние `speed_window_s`; нужно не меньше `speed_min_samples` точек, разрывы не больше `speed_max_gap_s` и охват окна не меньше половины; иначе скорость `None`. `speed_bh_s = |p_last − p_first| / dt / H_ref`; при калибровке и обеих точках внутри оболочки калибровочных точек `speed_m_s` по точкам на полу;
   - `ground` — точка `foot` на полу через гомографию, только внутри оболочки калибровочных точек;
   - `last_upright_ms`, `lying_since_ms`; `still_since_ms` — самое раннее время, с которого центр рамки не отходит от текущего дальше `still_motion_bh × H_ref`;
   - `prev_anchor`, `prev_ts_ms` — предыдущее наблюдение этого трека.
6. Признаки техники (`features.vehicle_states`, S10): `speed_vh_s` — смещение центра рамки за `speed_window_s` в высотах её рамки в секунду; при калибровке `footprint` (нижняя кромка на полу) и `speed_m_s`.
7. Плагины включённых сценариев со статусом `active` получают `FrameContext` и эффективные параметры камеры (8.3), возвращают `Observation`. Менеджер эпизодов (8.4) собирает эпизоды.
8. HUD (`hud.build_hud`): на каждый кадр `HudFrame`. Координаты нормированы делением на ширину и высоту кадра. Подписи людей:
   - скорость `"<v> роста/с"` или `"<v> м/с"`, уровень `yellow`, если скорость не ниже порога бега (`≥`, как у `running` в 8.3);
   - `"лежит <N> с"` в позе `lying`; `"неподвижен <N> с"` при неподвижности дольше `still_after_s`;
   - `"ноги не видны"` (`feet_hidden`), `"слишком мелко"` (`too_small`, высота меньше `min_person_px`);
   - на каждое наблюдение `P` подпись с кодом сценария, текстом причины и уровнем.
   Числа в подписях — с запятой и одним знаком (`texts.fmt_num`), секунды — целые.
9. Доказательства (S5): для эпизода кадр `confirm_frame_idx` и, если был, `escalate_frame_idx`: `media.read_frame`, уменьшение до `evidence.max_width`, JPEG `evidence.jpeg_quality`, sha256 файла, объекты кадра из HUD.

### 8.3 Сценарии (плагины)

Плагин — модуль `rules/<id>.py` с классом из 6.7 и полем `meta`; регистрация — строка в `rules.PLUGINS`. Параметры и значения по умолчанию — `scenarios.<id>` в `config/default.yaml`; `ScenarioMeta.params` перечисляет их с подписью, единицей и диапазоном. Эффективные параметры камеры = значения по умолчанию + `camera_rules.params_json`. Нет строки `camera_rules` → сценарий включён, если его статус `active`.

Статус: `skeleton` — у плагина нет логики; `model_missing` — ни одна активная модель не даёт классы из `required_classes` (достаточно одного из перечисленных для `fire_smoking`, всех — для остальных); иначе `active`. Плагин со статусом не `active` в анализе не участвует, UI показывает `status_text`.

Наблюдение: `P` — нарушение видно, `N` — видно, что нарушения нет, `U` — данных недостаточно. Отсутствие детекции — не `N`.

| id | Название, иконка | Классы, зоны | P (уровень, удержание) | N | U | Причина (`reason_text`) |
| --- | --- | --- | --- | --- | --- | --- |
| `running` | «Бег и резкие перемещения», `run` | person; danger, vehicle_path | жёлтый: `speed_m_s ≥ speed_m_s` при калибровке, иначе `speed_bh_s ≥ speed_bh_s`, удержание `hold_s`; красный: то же и `anchor` в зоне danger/vehicle_path или до любой техники не дальше `near_vehicle_bh` (`near_vehicle_m`), удержание `red_hold_s` | скорость известна и ниже порога | скорость `None` | «Бег 2,4 роста/с», «Бег 3,1 м/с», + « в зоне «Пресс»» или « рядом с техникой» |
| `proximity` | «Опасное сближение с техникой», `truck` | person, car/bus/truck/train; danger | субъект `pair:<p>-<v>`: техника движется (`speed_m_s ≥ moving_m_s` или `speed_vh_s ≥ moving_vh_s`) и дистанция `≤ red_m` / `≤ red_bh` → красный, `red_hold_s`; `≤ yellow_*` → жёлтый, `hold_s`. Субъект `zone:<p>-<z>`: `anchor` в зоне danger → красный, `red_hold_s` | техника стоит или дальше `yellow_*`; человек вне зоны | скорость техники `None` | «Сближение с грузовиком: 0,4 роста», «… 0,8 м», «Человек в зоне «Пресс»» |
| `phone` | «Телефон при работе», `phone` | person, cell phone; danger, vehicle_path | телефон привязан к человеку: жёлтый, `hold_s`; привязан и `anchor` в danger/vehicle_path: красный, `danger_hold_s` | человек не меньше `min_person_px`, телефона нет | человек меньше `min_person_px` (`too_small`); телефон подходит двум людям (`owner_ambiguous`) | «Телефон в руке {duration_s} с» |
| `fall` | «Падение и неподвижность», `fall` | person; lying_allowed | вне зоны lying_allowed: поза `lying` и `lying_since − last_upright ≤ transition_s` → красный «падение», удержание `confirm_s`; поза `lying`, перехода не видно, неподвижен `≥ still_s` → красный «лежит», удержание 0; в зоне lying_allowed: неподвижен `≥ allowed_still_s` → красный, удержание 0 | поза `upright`; лежит, но условия P не выполнены | поза `unknown` или человек меньше `features.min_person_px` | «Зафиксировано падение», «Человек лежит неподвижно 15 с», «… в зоне ремонта» |
| `fence_crossing` | «Перелезание через ограждение», `fence` | person; fence (линия) | отрезок `prev_anchor → anchor` пересекает линию ограждения (`segment_crossing`) → красный, удержание 0; разрыв `> max_gap_s` → причина «момент не виден» | человек виден, пересечения нет | нет `prev_anchor` | «Пересечение ограждения «Забор у пресса»» |
| `restricted_under` | «Проход под конвейером или грузом», `conveyor` | person; under_load | `anchor` в зоне → красный, `under_hold_s` | вне зоны | — | «Человек в зоне «Под конвейером»» |
| `fire_smoking` | «Курение и открытый огонь», `fire` | fire, smoke, cigarette (любой); fire_allowed, danger | субъект `fire`: огонь или дым с центром вне всех зон fire_allowed → красный, `fire_hold_s`; сигарета привязана к человеку → жёлтый, `smoking_hold_s`, а в зоне danger — красный | огня нет или он в разрешённой зоне | сигарета подходит двум людям | «Открытый огонь вне разрешённой зоны», «Курение» |
| `no_harness` | «Высота без страховочной привязи», `harness` | no_harness; height | `anchor` в зоне height и объект `no_harness` пересекается с рамкой человека → жёлтый, `harness_hold_s` | в зоне height без такого объекта | — | «Работа на высоте без привязи» |
| `suspended_load` | «Под подвешенным грузом», `crane` | suspended_load | `anchor` ниже рамки груза и в её горизонтальных границах → красный, `load_hold_s` | иначе | — | «Человек под подвешенным грузом» |
| `load_carrying` | «Переноска груза с нарушением», `box` | — | логики нет, статус `skeleton`, текст «Сценарий уточняется: правила переноски не определены» | — | — | — |

Привязка объекта к человеку (`rules/base.attach_objects`, телефон и сигарета): центр объекта внутри верхней доли `upper_frac` рамки человека или ближе `wrist_dist_bh × H_ref` к видимому запястью (точки 9, 10). Подходит одному человеку — привязан; двум и больше — `ambiguous` для каждого. Водитель исключается из `proximity`: доля рамки человека внутри рамки техники `≥ driver_ioa`. Дистанция без калибровки — от `foot` до прямоугольника рамки техники (0 внутри), делённая на H_ref; с калибровкой — от `ground` до отрезка `footprint` в метрах.

`{duration_s}` в тексте причины менеджер эпизодов заменяет целыми секундами `confirm_ms − start_ms` (при эскалации — `escalate_ms − start_ms`).

v5, было → стало в таблице: `running` — жёлтый по `speed_m_s ≥ speed_m_s`, если `speed_m_s` есть (ручная калибровка или автокалибровка, 8.21), иначе по `speed_bh_s`; метод `calibrated`, `auto` или `relative`. `proximity` — дистанция в метрах и при автокалибровке (8.21); статус `active` при `person` и хотя бы одном классе из `pipeline.vehicle_classes` (S29, было: все пять имён). `phone` — в зонах `ALLOWED_KINDS` (`walkway`, `rest`) наблюдение `N` (8.23). Плагины `no_helmet` и `no_respirator` — 8.22.

`explain(episode, params)` возвращает строки «почему» для экрана события: правило с порогом («Бег: скорость выше 1,5 роста/с дольше 1 с»), измеренные значения из `metrics`, метод («поза» или «рамка», «калибровка» или «в ростах человека»), уверенность детекции, зона, `uncertain_ms` («Потеря видимости 2 с»).

### 8.4 Менеджер эпизодов

Состояние ведётся на пару (сценарий, субъект). Время — `ts_ms` кадров источника. Параметры — секция `episodes`, удержание — `Observation.hold_s`.

| Ситуация | Правило |
| --- | --- |
| `P` при отсутствии эпизода | кандидат, `start_ms = ts` |
| `P` у кандидата, `ts − start_ms ≥ hold_s` текущего наблюдения | активный эпизод: `confirm_ms = ts`, `level_initial` = уровень наблюдения, `confirm_frame_idx` |
| `N` у кандидата | кандидат сброшен |
| нет наблюдения или `U` у кандидата дольше `candidate_gap_s` | кандидат сброшен |
| `P` красного уровня у активного жёлтого эпизода держится `≥ hold_s` красного наблюдения | `escalate_ms = ts`, `level_max = red`, тот же эпизод |
| `N` у активного | начало закрытия с первого `N`; `N` подряд `≥ end_after_s` → эпизод закрыт, `end_ms` = первый `N`, `observed_exit` |
| `P` во время закрытия | закрытие отменено |
| нет наблюдения или `U` у активного | интервал добавляется в `uncertain_ms`; дольше `lost_timeout_s` → эпизод закрыт, `end_ms` = последний `P`, `track_lost_timeout` |
| конец видео при активном | `end_ms` = длительность видео, `video_end` |
| новый субъект с `P` того же сценария, пока прежний субъект активного эпизода не наблюдается, его `anchor` не дальше `merge_dist_bh × H_ref` от последнего `anchor` прежнего | продолжение того же эпизода (смена track id), субъект добавляется как синоним |
| `P` после закрытия | новый кандидат и новый эпизод; таймера тишины нет |

Два человека с одновременными `P` — два эпизода (субъекты наблюдаются оба, слияния нет). `confidence` эпизода — максимум за эпизод, `metrics` — пики. `reason_text` фиксируется при подтверждении и обновляется при эскалации.

### 8.5 Эфир и публикация событий

Эфир — проигрывание проанализированного видео камеры по серверным часам. Одна запись `playing` на камеру. Длительность `D = videos.duration_ms`. На каждом тике (`broadcast.tick_ms`) для каждого `playing`:
- `t = now − started_at`; при `loop`: `cycle = t // D`, `pos = t % D`; без `loop`: `cycle = 0`, `pos = min(t, D)`, и при `t ≥ D` после обработки статус `ended`;
- `cycle` вырос: сначала прежний цикл дообрабатывается до `pos = D`, затем новый с 0; пропущенные целиком циклы (сервер был выключен) не публикуются;
- база цикла `base = started_at + cycle × D`; для каждого эпизода активного анализа:
  - `confirm_ms ≤ pos` и нет события с `pub_key = "b<id>:c<cycle>:e<episode>"` → событие `new`: уровень красный, если `level_initial = red` или `escalate_ms ≤ pos`; `started_at = base + start_ms`, `published_at = now`, `red_at = now` для красного, `ended_at = base + end_ms`, если `end_ms ≤ pos`; действие `published`; WS `event.created` и `notification`;
  - событие жёлтое и `escalate_ms ≤ pos` → уровень красный, `red_at = now`, действие `level_escalated`, WS `event.escalated` и красное `notification` с захватом экрана;
  - `end_ms ≤ pos` и `ended_at` пусто → `ended_at = base + end_ms`; жёлтое в статусе `new` или `viewed` → `auto_finished` (действие); WS `event.updated`;
- `position_ms`, `cycle` записываются; при смене цикла и окончании — WS `broadcast.state`; состояния камер и секторов пересчитываются, изменившиеся уходят в `camera.state` и `sector.state`.

Тик идемпотентен: повтор с теми же часами ничего не создаёт (`pub_key UNIQUE`), перезапуск сервера продолжает эфир с того же `started_at`.

`broadcast_start`: видео не указано → последнее `ready` видео камеры, нет такого → `Conflict(no_ready_video)`; указанное видео не `ready` → `Conflict(video_not_ready)`. Прежний `playing` этой камеры → `stopped`. Новый эфир: `started_at = now`, `analysis_id = videos.active_analysis_id`, `loop` из запроса или `broadcast.loop_default`. `broadcast_stop` → `stopped`, публикации прекращаются. Автостарт: задача `process` завершилась, у камеры нет `playing`, `broadcast.autostart = true` → эфир этого видео.

Синхронизация плеера: фронт берёт `Broadcast` (`server_now`, `started_at`, `duration_ms`, `loop`) и ставит `currentTime = ((server_now − started_at) + прошедшее с ответа) mod D`; расхождение больше 0,5 с исправляется перемоткой.

### 8.6 Статусы события

Терминальные статусы: `false_alarm`, `resolved`, `auto_finished`, `superseded`. Открытые — остальные. Каждый переход пишет строку `event_actions` (кто, роль, когда, из какого статуса, в какой, комментарий).

| Действие | Роль | Уровень | Из статусов | В статус | Вердикт | Запись журнала |
| --- | --- | --- | --- | --- | --- | --- |
| `view` | operator | любой | `new` | `viewed` | — | `viewed` |
| `confirm` | operator | жёлтый | `new`, `viewed` | `confirmed` | `confirmed` | `confirmed` |
| `confirm` | operator | красный | `new`, `viewed`, `confirmed` | `sent_to_master` | `confirmed` | `confirmed`, затем `sent_to_master` |
| `confirm` | operator | красный | `sent_to_master` с `escalated_by_timeout=1` и вердиктом `none` | без изменения | `confirmed` | `confirmed` |
| `false_alarm` | operator | любой | `new`, `viewed`, `confirmed` | `false_alarm` | `false_alarm` | `false_alarm` |
| `false_alarm` | operator | любой | `sent_to_master` с `escalated_by_timeout=1` и вердиктом `none` | `false_alarm` | `false_alarm` | `false_alarm` |
| `send_to_master` | operator | любой | `new`, `viewed`, `confirmed` | `sent_to_master` | `confirmed`, если был `none` | `sent_to_master` |
| `accept` | master | любой | `sent_to_master` | `master_accepted` | — | `master_accepted` |
| `resolve` | master | любой | `master_accepted` | `resolved` | — | `resolved`, комментарий обязателен |
| публикация | system | — | — | `new` | — | `published` |
| эскалация уровня | system | жёлтый → красный | любой открытый | без изменения | — | `level_escalated` |
| таймаут оператора | system | красный | 8.7 | `sent_to_master`, `escalated_by_timeout=1` | — | `timeout_escalated` |
| автозавершение | system | жёлтый | `new`, `viewed`, эпизод закончился | `auto_finished` | — | `auto_finished` |
| пересчёт | system | любой | `new`, `auto_finished`, событие старой версии анализа | `superseded` | — | `superseded` |

Любая другая пара (действие, статус) → `Conflict(invalid_transition)`. `allowed_actions` в `EventDetail` — действия из таблицы, допустимые для роли запроса и текущего статуса. Мастер видит событие в статусах `sent_to_master`, `master_accepted`, `resolved`; изменения вердикта оператора после таймаута приходят ему в той же карточке (`event.updated`).

### 8.7 Автоэскалация красного

Флаг `escalation.enabled`, таймаут `escalation.timeout_s`, проверка каждые `escalation.tick_ms`. Красное событие эскалируется, когда одновременно:
- статус `new`, `viewed` или `confirmed`;
- после `red_at` нет действий оператора `confirmed`, `false_alarm`, `sent_to_master` (`viewed` реакцией не считается);
- `now − red_at ≥ timeout_s` (44,9 с — нет, 45,0 с — да).

Итог: статус `sent_to_master`, `escalated_by_timeout = 1`, действие `timeout_escalated` от `system`, WS `event.updated` и уведомление мастеру с припиской «· Не подтверждено оператором». Флаг выключен — ничего не происходит.

### 8.8 Уведомления, тексты, лента

`texts.notification_text(level, sector_name, reason_text, escalated_by_timeout)`:
- `<уровень> · <сектор> · <причина>`, где уровень — «Жёлтая опасность» или «Красная опасность», сектор — часть названия до первого « · », причина — `reason_text`;
- с `escalated_by_timeout` в конце добавляется « · Не подтверждено оператором».
Примеры: «Жёлтая опасность · Сектор 5 · Бег 2,4 роста/с», «Красная опасность · Сектор 7 · Человек лежит неподвижно 15 с».

| Повод | Аудитория | Звук | Захват экрана |
| --- | --- | --- | --- |
| публикация жёлтого | operator | `chime` | нет |
| публикация красного, эскалация до красного | operator | `siren` | да |
| `sent_to_master` (оператором или по таймауту) | master | `chime` | нет |
| эскалация уровня у события в `sent_to_master` или `master_accepted` | master | `chime` | нет |

Приоритет события (`PRIORITY`): красное открытое без решения оператора (`new`, `viewed`) — 3; жёлтое `new` или `viewed` — 2; прочее открытое — 1; терминальное — 0. Лента оператора (`operator_feed`): открытые события и терминальные за последние `feed.recent_closed_min` минут, кроме `superseded`, по убыванию `priority`, затем `published_at`; не больше `feed.limit`. `duration_s` = `ended_at − started_at` или `now − started_at`, пока эпизод идёт.

### 8.9 Состояние камеры и сектора

Камера (удалённые не учитываются), первое подходящее правило сверху:
1. есть открытое красное событие → `red`;
2. есть открытое жёлтое событие с `ended_at = NULL` → `yellow`;
3. нет `playing`-эфира: задача камеры `queued`/`running`/`retry_wait` → `no_observation` (`processing`); последняя задача `failed` → `failed`; последний эфир `ended` → `ended`; иначе `no_source`;
4. позиция эфира внутри интервала `gaps` активного анализа → `no_observation` с причиной интервала (`stale`, `dark`, `obstructed`; S11);
5. иначе `normal`.

`reason_text` для `no_observation` — `texts.NO_OBSERVATION_TEXTS`: «Нет источника видео», «Видео обрабатывается», «Обработка не удалась», «Запись закончилась», «Данные анализа устарели», «Слишком темно», «Камера закрыта или не в фокусе». `freshness_ms` = позиция эфира − `ts_ms` последнего проанализированного кадра не позже позиции (`None` без эфира).

Сектор: `red`, если есть красная камера; иначе `yellow`, если есть жёлтая; иначе `no_observation`, если хоть одна камера без наблюдения (текст «Нет наблюдения: 1 из 2 камер») или камер нет; иначе `normal`. Отсутствие событий не выдаётся за безопасность.

### 8.10 Наблюдаемость (S11)

`observability.find_gaps(frames_ts, luma, duration_ms, params) -> list[ObservabilityGap]`:
- `stale`: разрыв между соседними проанализированными кадрами больше `stale_after_ms`;
- `dark`: средняя яркость кадра (`sample_luma` раз в `sample_s`, серый, уменьшенный кадр) `< dark_mean` подряд `≥ min_duration_s`;
- `obstructed`: стандартное отклонение яркости `< obstructed_std` подряд `≥ min_duration_s` (крышка, расфокус, однотонная сцена).

Интервал короче `min_duration_s` не считается. Камера в интервале — `no_observation` (8.9). Эпизод, попавший в интервал, продолжается по правилам 8.4 (это `U`), его `uncertain_ms` растёт; экран события пишет «Потеря видимости N с».

### 8.11 Калибровка и зоны (S9)

Калибровка: 4–8 точек на полу в нормированных координатах кадра и их координаты в метрах. Гомография `geometry.homography(image_pts, world_pts)` — `cv2.findHomography` методом 0 (наименьшие квадраты), отображает нормированные координаты в метры. `fit_rmse_m` — СКО отклонения пересчитанных точек от введённых; `control_rmse_m` — то же на контрольных точках, не участвующих в подгонке (без них UI пишет «нет контрольных точек: точность не проверена»). `grid` — линии сетки через 1 м в пределах прямоугольника мировых точек, переведённые обратно в кадр и обрезанные по [0, 1]. Метры и м/с считаются только для точек внутри выпуклой оболочки калибровочных точек; без калибровки система работает в ростах человека, и это нормальный режим.

Зоны: тип из `zone_kinds`, геометрия типа (`polygon` 3..`ZONE_POINTS_MAX` точек, `line` ровно 2), координаты нормированные. Удаление мягкое (`deleted_at`); эпизоды и события ссылаются на зону по id. Правила видят зоны снимка `AnalysisConfig`, а не текущие.

### 8.12 Пересчёт событий

`video_recompute` ставит задачу `recompute`: те же артефакты, текущие калибровка, зоны и правила камеры, новая версия анализа (снимок в `config_json`). После успешного анализа (`run_next_job`, S9):
1. события этого видео из прежних версий анализа в статусах `new` и `auto_finished` → `superseded` (действие от `system`, комментарий «Пересчёт: версия анализа N»), WS `event.updated`;
2. события, с которыми работали люди, не меняются, их история сохраняется;
3. если эфир камеры играет это видео — он останавливается и стартует заново с новым анализом.

### 8.13 Статистика (S13)

Общее: события без `superseded`; демо-события учитываются при `include_demo=true` (UI показывает пометку «включая демо-данные»). Группировка по дате, часу и смене — по `started_at` в `timezone`. Смена — интервал из `shifts`, ночная переходит через полночь.
- `reviewed` — события с вердиктом не `none`; `false_alarm_share = false_alarm / reviewed`; `review_coverage = reviewed / total` (знаменатель 0 → `None`).
- `operator_reaction_s` — от `published_at` до первого действия оператора `confirmed`/`false_alarm`/`sent_to_master`; `pending` — открытые без такого действия. `master_accept_s` — от последнего `sent_to_master` до `master_accepted`; `master_resolve_s` — от `master_accepted` до `resolved`.
- Процентили — ближайший ранг: отсортированный `x[ceil(p·n) − 1]`; `n = 0` → `None`.
- Менеджмент: недели с понедельника в `timezone`, последние `weeks` недель включая текущую. `top_sectors` — подтверждённые за последние `stats.trend_weeks` недель и `per_camera = confirmed / cameras` (сырые счётчики вводят в заблуждение). `yellow_trend`: `recent` — жёлтые события без `false_alarm` за последние `trend_weeks` полных недель, `previous` — за столько же недель до них, `change_pct = (recent − previous) / previous × 100`; текст «Жёлтых нарушений стало меньше на 23 % (4 недели к 4 неделям). Сравнение до и после не доказывает причину.» (или «больше на …», «без изменений»).

### 8.14 Экраны

Основной фронт — фронт Егора из PR #36, собирается из `frontend/` внутри Docker. Дизайн сохраняется; функциональные ошибки исправляются. Таблица ниже сохраняет предметное поведение экранов и историческую трассировку. Старые ограничения минимального фронта и запрет браузерной проверки отменены владельцем.

Тёмная тема по умолчанию (CSS-переменные в `theme.css`: фон `#0B0F14`, поверхность `#121821`, текст `#E6EDF3`, жёлтый `#FFC400`, красный `#FF3B30`, норма `#2BB673`, нет наблюдения `#7A8794`, акцент `#3BA7FF`). Уровень и состояние всегда текстом и иконкой, не только цветом. Цели нажатия не меньше 24×24 px. Интерфейс на русском. Каждый экран имеет состояния загрузки, пустоты («Событий нет — это не значит, что всё безопасно, если камера без наблюдения») и ошибки (текст `ApiError.message`). Работает на одном мониторе от 1280 px; экраны мастера — от 360 px.

Шапка (`AppShell`): название продукта, переключатель роли (5 ролей из `meta.roles`), бейдж бэкенда («LinQ TPU», «CPU (local)», «Фейк: детекции синтетические»), часы МСК, кнопка «Включить звук», если браузер заблокировал звук. Навигация роли — `nav.ts`.

| Маршрут | Роль | Слайс | Блоки и действия |
| --- | --- | --- | --- |
| `/operator` | operator | 6 | сетка плиток секторов (номер, название, состояние текстом, счётчики жёлтых и красных, «нет наблюдения: N из M»); справа лента событий как чаты (уровень, сектор, причина, время, длительность, статус); всплывашка со звуком на жёлтое; клик по плитке → сектор, по событию → `/events/:id` |
| `/operator/sectors/:sectorId` | operator | 6 | плитки камер с превью (`/preview` раз в `preview.cache_s`), состоянием и причиной «нет наблюдения»; лента событий сектора |
| `/operator/cameras/:cameraId` | operator | 6 | большой плеер эфира с HUD (`VideoWithHud`), зоны и сетка калибровки на оверлее, таймлайн эпизодов, кнопка «Скрыть HUD» (клавиша H) |
| `/events/:eventId` | все | 7 | экран делится по горизонтали. Верх слева: доказательный кадр с рамкой и выноской (`EvidenceImage`); верх справа: тип, уровень, сектор и камера, начало и длительность, «Почему» (`why`), история эпизода (жёлтое → красное), действия людей, происхождение (бэкенд, модели, задача, sha256 кадра, режим «запись»), кнопки `allowed_actions` («Подтверждаю», «Ложное срабатывание», «Передать мастеру»; клавиши 1, 2, 3). Низ: эфир камеры сейчас с HUD. Открытие оператором отправляет `view`. Режим захвата (`?takeover=1`): на весь экран, сирена до действия или «Свернуть» |
| `/master` | master | 8 | мобильный список: активные (`sent_to_master`, `master_accepted`) крупными карточками, ниже решённые; новое уведомление — звук и вибрация (`navigator.vibrate`), браузерное `Notification`, если разрешено |
| `/master/events/:eventId` | master | 8 | кадр с рамкой, где (сектор, камера, зона), причина, пометка «Не подтверждено оператором»; кнопки «Принял, иду» и «Решено» с обязательным комментарием о мерах |
| `/master/shift` | master | 8 | сводка текущей или прошедшей смены: всего, по секторам, по сценариям, список подтверждённых |
| `/ohs/journal` | ohs | 12 | фильтры (тип, уровень, статус, сектор, камера, зона, период, поиск, демо, пересчитанные), «показано X из Y», «Сбросить», таблица с миниатюрой кадра, открытие карточки (история только для чтения), «Экспорт CSV» |
| `/ohs/rules` | ohs | 9 | матрица камеры × сценарии: переключатели, статус сценария («Модель не подключена»), переход к параметрам камеры |
| `/ohs/stats` | ohs | 13 | период и фильтры; по дням (жёлтые и красные), по сценариям, секторам, камерам, сменам, часам; доля ложных и охват проверкой с n; реакция оператора и мастера (p50, p95, n, ожидают) |
| `/management` | management | 13 | тренд по неделям, топ секторов на камеру, топ сценариев, текст тренда жёлтых с оговоркой о причинности |
| `/admin/cameras` | admin | 1 | секторы и камеры: создать, переименовать, удалить (с подтверждением), привязать камеру к сектору; ошибки валидации у полей |
| `/admin/cameras/:cameraId` | admin, ohs | 2 | вкладки: «Видео» (S2: загрузка с прогрессом, список видео, задачи с прогрессом и замерами; S4: плеер с HUD; S5: таймлайн эпизодов, «Пересчитать события»), «Эфир» (S6: старт, стоп, повтор), «Калибровка», «Зоны», «Правила» (S9). Вкладка незакрытого слайса — `StubNotice` |
| `/admin/system` | admin | 3 | бэкенд и его состояние, кнопка «Проверить LinQ»; очередь и последние задачи с замерами (кадров, кадр/с, мс на кадр: пре, пост, RTT p50 и p90; загрузка; всего); модели (id@версия, программа, хвост); задержка уведомлений (p50, p95, n); свежесть анализа по камерам (S11); каналы доставки (S15) |
| `/m/operator` (v5) | operator | 23 | мобильная лента оператора одной колонкой от 360 px, как `/master`: карточки жёлтых и красных (уровень, сектор, причина, время, статус); уведомление — звук и `navigator.vibrate`; тап → `/m/operator/events/:eventId` |
| `/m/operator/events/:eventId` (v5) | operator | 23 | кадр доказательства, клип (`ClipPlayer`), место, причина, кнопки `allowed_actions` («Подтверждаю», «Ложное срабатывание», «Передать мастеру»); открытие отправляет `view` |

v5 на существующих экранах (фронт минимальный, остальное делает Егор по 6.11): `EventScreen` и `MasterEvent` показывают `ClipPlayer`, если у события есть `clip` (S18); `MasterInbox` на уведомление `to_master` сам открывает `/master/events/:id` (S23); строка доставки `call:<name>` в карточке события — текст `status_text` (S23). Экраны калькулятора, паспорта камеры, датасета, идентификации и статистики по людям — только API (Егор).

Маршрут незакрытого слайса рендерит `StubNotice` «Экран появится в слайсе N».

### 8.15 Контракт фронта, мок-режим, заменяемый фронт

- Фронт ходит в бэкенд только через `src/api/` по `contract/openapi.json`; типы генерирует `openapi-typescript` в `src/api/schema.d.ts` (`npm run api:gen`), гейт фронта сверяет их с контрактом (`npm run api:check`).
- Мок: `npm run mock` поднимает Prism (`prism mock -d ../contract/openapi.json -p 4010`) и `mock/ws-mock.mjs` на 4011, который по кругу раз в 3 с шлёт сообщения из `contract/ws-examples.json`; `npm run dev:mock` запускает Vite с `.env.mock`. Бэкенд для этого не нужен.
- Логика продукта только на бэкенде. Фронт можно удалить и заменить фронтом Егора: бэкенд не зависит от `frontend/`, кроме раздачи `server.static_dir`, если папка есть. Замене нужен скрипт `npm run gate` (или строка `долг` в `## open`).

### 8.16 Демо-данные (сид)

`seed_demo` создаёт мир, если в базе нет ни одного сектора с `is_demo=1` (иначе `skipped=true`), детерминированно (`random.Random(SEED)`):
- 4 сектора: «Сектор 1 · Прессовый участок», «Сектор 2 · Склад и погрузка», «Сектор 3 · Сборочный цех», «Сектор 4 · Ремонтная зона»;
- по 2 камеры в секторе с понятными именами («Камера 1.1 · Пресс №2»), у части камер зоны (danger, fence, under_load, lying_allowed, vehicle_path);
- `EVENTS` событий за последние `DAYS` дней до вчерашнего дня, 80 % жёлтых, число жёлтых по неделям убывает примерно на 6 % в неделю; статусы: жёлтые — 50 % `confirmed`, 15 % `false_alarm`, 35 % `auto_finished`; красные — 70 % `resolved` с полной историей и комментарием мастера, 20 % `false_alarm`, 10 % `resolved` после `timeout_escalated`; `pub_key = "demo:<n>"`, `is_demo=1`, `mode=demo`;
- с `videos_dir`: каждое видео папки по имени по порядку импортируется (`video_import`) в демо-камеры по кругу.

### 8.17 doctor

`safewatch doctor` печатает таблицу проверок «что — итог — подсказка» и выходит с 4, если хоть одна проверка провалилась:
- ключи `.env` из 6.6: «есть» или «нет» (значения не печатаются);
- `INFERENCE_BACKEND` и `SAFEWATCH_FAKE`;
- файлы активных моделей для выбранного бэкенда (хвосты для `linq`, ONNX для `local`);
- `linq.tools_dir` с `jupyter_remote.py`, `linq_tpu.py`, `yolo_io.py`, `remote/video_worker.py`;
- для `linq` без фейка: `backend_check(force=True)` (S3; до S3 — вход в Jupyter и `echo ok`), программы активных моделей в `linq.programs_dir`;
- база открывается и мигрирует.
В режиме фейка проверки LinQ пропускаются с пометкой «фейк».

### 8.18 Оценка качества (S14)

Файл разметки (`config/eval.example.yaml` — пример):
```yaml
deadline_s: 5
videos:
  - path: data/videos/fall_01.mp4
    camera_id: 3          # необязательно: калибровка, зоны и правила этой камеры
    expected:
      - {scenario: fall, start_s: 12.0, end_s: 30.0}
```
`eval_run` для каждого видео: инференс через выбранный бэкенд с кэшем артефактов (как `run_next_job`), анализ, сопоставление `evaluate.match_episodes`:
- пара допустима, если сценарий совпадает и `start_s ≤ confirm_s < end_s` и `confirm_s − start_s ≤ deadline_s` (ровно `deadline_s` — допустимо, `confirm_s = end_s` — нет);
- сопоставление жадное по возрастанию задержки; эталон получает не больше одного эпизода; лишние эпизоды того же эталона — `duplicates`; эпизоды внутри эталона, но позже дедлайна — `late` (и FN, если других нет); остальные эпизоды — FP; эталоны без пары — FN;
- метрики по сценарию и строка `*`: `precision = tp / (tp + fp)`, `recall = tp / (tp + fn)`, `f1`, `fp_per_hour = fp / часы видео`, задержка подтверждения p50 и p95 с n.
Отчёт: `eval/<время>/report.json` (`EvalReport`) и `report.md` (таблица и сноска: «recall валиден только при полной разметке видео»).

### 8.19 Демо-пакет и «живой» завод (S17)

Цель: открыл Argus (Docker или публичный адрес) — завод уже работает: секторы, камеры с реальными видео, эфир по кругу с HUD, события в ленте, красный захват, наполненные журнал и статистика. Показ не зависит от VPN и LinQ, но детекции настоящие: они посчитаны на LinQ заранее.

Пакет — папка `data/demo/<name>/`:
```
manifest.json          # DemoManifest (6.11.2)
videos/<file>          # исходные видео, как в раскладке
artifacts/<cache_key>.jsonl, <cache_key>.summary.json
```

Сборка `demo_build(layout, videos_dir, out, allow_fake)` (CLI `safewatch demo build`):
1. Раскладка — YAML `DemoLayout` (пример `config/demo.example.yaml`: камера `synthetic_coco_40x1s.mp4` в «Сектор 1 · Прессовый участок» с зоной danger). Нет файла → `NotFound`; схема → `ValidationFailed`; `out` существует и не пуст → `ValidationFailed`.
2. Бэкенд — `make_backend(settings)`. `Settings.fake = true` без `allow_fake` → `ValidationFailed` «Демо-пакет на фейке: добавьте --allow-fake» (честность: фейк подписан в пакете и в `DemoPack.fake`).
3. Для каждого видео: `media.probe_video` (не читается → `UnsupportedVideo`), sha256, шаг 8.1, прогон каждой активной модели (`pipeline.detector`, `pose`, `extra`) через `backend.run` в `out/artifacts/<cache_key>.jsonl` с проверкой `read_jsonl`, одна задача на TPU за раз (3.1). Видео копируется в `out/videos/`.
4. `manifest.json` пишется последним; любая ошибка бэкенда → `InferenceError`, папка `out` удаляется (не остаётся полупакета).

Импорт `demo_import(path)` (CLI `safewatch demo import`, `serve --seed` при `demo.autoload` и существующей папке `demo.pack`):
1. Пакет с тем же `name` уже в `demo_packs` → `skipped=true`, ничего не меняется (идемпотентно).
2. Проверки до записи: схема, каждая `model` пакета есть в реестре, sha256 каждого видео совпадает с файлом, все файлы артефактов есть.
3. Сектор и камера ищутся по названию (камеры сида «Камера 1.1 · Пресс №2» и т. п.), нет — создаются (`is_demo = 0`). Калибровка, зоны и правила камеры пакета записываются, если у камеры их нет (поверх существующих не пишет).
4. Видео — `video_import`; артефакты — `artifact_import` с `backend`, `fake` пакета; задача `process` ставится с `backend` и `fake` пакета (было: из `Settings`). Ключ кэша `run_next_job` считает по `jobs.backend` и `jobs.fake` (так было по 8.1 п. 6 — «на момент постановки»), поэтому задача находит артефакты пакета и не вызывает бэкенд (`cached=true`). Модель, активная сейчас, но без артефакта в пакете, считается обычным путём.
5. Строка `demo_packs`; отчёт `DemoImportReport`. Дальше обычный путь: анализ, эфир по кругу (`broadcast.autostart`), события.

Лента и состояния без демо-событий сида (долг S6, было → стало): `operator_feed`, `sector_view.feed`, `camera_states` и `sector` состояния не учитывают события `is_demo = 1`; журнал и статистика учитывают их по `include_demo`, как раньше. События эфира демо-пакета — настоящие и в ленте есть.

«Загрузить своё видео» — существующая загрузка (8.1) честно идёт на выбранном бэкенде. `Job.status_text` (`texts.job_status_text(job)`): `queued` «В очереди», `running` «Обработка на LinQ» (или «на CPU (local)»), `retry_wait` с `linq_unavailable` «LinQ недоступен, повтор в ЧЧ:ММ», `retry_wait` с `timeout` «LinQ не ответил вовремя, повтор в ЧЧ:ММ», `failed` — текст кода ошибки («LinQ недоступен: попробуйте позже», «Нет программы модели на LinQ», «Неожиданный ответ LinQ», «Видео не читается», «Внутренняя ошибка»), `done` «Готово». Время — `timezone`.

`GET /api/demo/packs` — импортированные пакеты по `imported_at`; шапка и экран IT показывают «Демо-пакет <name>: детекции LinQ» или «… фейк».

### 8.20 Клип события и H.264 (S18)

Клип — окно исходного видео, без перекодирования на событие. Для события эфира с эпизодом: `start_ms = max(0, episode.start_ms − clips.pre_s·1000)`, `end_ms = min(duration_ms, episode.confirm_ms + clips.post_s·1000, start_ms + clips.max_s·1000)`; `url = "/api/videos/<video_id>/file#t=<start_s>,<end_s>"` (секунды с одним знаком, точка), `playable = Video.web_playable`. Демо-событие сида (нет видео) — `clip = None`. Клип есть в `EventSummary` (лента, журнал, мастер) и `EventDetail.event`; стоп-кадр `evidence` остаётся превью.

Перекодирование: `video_upload`, `video_import` после проверки 8.1 п. 3: `codec` не из `BROWSER_CODECS` и `transcode.enabled` → `media.transcode(src, uploads/<sha256>.web.mp4, cfg)` в `asyncio.to_thread` (импорт — напрямую): ffmpeg `imageio_ffmpeg.get_ffmpeg_exe()`, `-c:v libx264 -preset <preset> -crf <crf> -pix_fmt yuv420p -movflags +faststart -an`, кадры и длительность прежние. Успех — `videos.web_path`; итог проверяется `probe_video(dst).codec ∈ BROWSER_CODECS`, иначе файл удаляется и `web_path = NULL`. Ошибка, таймаут `transcode.timeout_s` или выключенный ключ → видео принято без копии (6.11.4). `video_file` отдаёт копию, если она есть. Инференс, sha256 и ключ кэша — по исходнику.

v10: FourCC и `Range` (206) дополняют обязательную браузерную проверку: кадры видео действительно меняются, клип играет и перематывается локально и через публичный HTTPS. HTTP 200 и сборка сами по себе этого не доказывают.

### 8.21 Автокалибровка и скорость в м/с (S19)

`autocal.fit` по кадрам детектора (до трекинга, чистая функция):
1. Замеры — люди со `score ≥ tracker.high_thresh`, стоящие по рамке (`h/w ≥ features.upright_hw`), рамка не касается краёв кадра (отступ больше `autocal.edge_px`), высота `≥ autocal.min_person_px`. Замер — пара (низ рамки `y2`, высота `h`) в пикселях.
2. Подгонка `h = a + b·y2` наименьшими квадратами; `autocal.iterations` раз отбрасываются замеры с `|h − ĥ| > max_residual · ĥ` (присевшие, закрытые, обрезанные), затем повторная подгонка.
3. `ok = true`, если осталось `≥ min_samples` замеров и `ĥ(y) > 0` на всей высоте кадра; иначе `ok = false` и `reason` («Мало стоящих людей в кадре: N из 30», «Рост людей не согласуется с перспективой»). Пишутся `samples`, `a_px`, `b`, `rmse_px`, `r2`, `person_height_m`.
4. `scale_at(cal, y) = person_height_m / ĥ(y)` метров на пиксель в строке пола `y`.

Скорость (было → стало 8.2 п. 5, 6): окно и условия прежние. Есть ручная калибровка и обе точки внутри оболочки → `speed_m_s` по гомографии, `speed_source = "calibration"`; иначе автокалибровка `ok` → `speed_m_s = |Δfoot| / dt · scale_at(cal, (y_first + y_last)/2)`, `speed_source = "auto"`; иначе `speed_m_s = None`, `speed_source = "relative"` (запасной режим в ростах в секунду). Техника — так же по середине нижней кромки рамки. Дистанция `proximity` при автокалибровке — пиксели от `foot` до рамки техники × `scale_at(cal, foot.y)`. Ручная калибровка всегда главнее.

HUD (было → стало 8.2 п. 8): «≈2,9 м/с (авто)» и «бег ≈2,9 м/с (авто)» при `auto`, «2,9 м/с (калибровка)» и «бег 2,9 м/с (калибровка)» при `calibration`, «2,4 роста/с» при `relative`. Тексты `texts.HUD_SPEED_M_AUTO`, `HUD_RUN_M_AUTO`, `HUD_SPEED_M` (`"{v} м/с (калибровка)"`, было `"{v} м/с"`), `HUD_RUN_M` (`"бег {v} м/с (калибровка)"`). `explain` бега: строка «Скорость: автокалибровка по росту людей (N замеров, точность около ±20 %)» или «по калибровке камеры». Результат подгонки — `analyses.autocal_json`, `Analysis.auto_calibration`, `CameraSetupView.auto_calibration`; пересчёт (8.12) подгоняет заново.

### 8.22 СИЗ: каска и респиратор; модели Матвея (S20)

| id | Название, иконка | Классы, зоны | P (уровень, удержание) | N | U | Причина |
| --- | --- | --- | --- | --- | --- | --- |
| `no_helmet` | «Без каски в зоне обязательной каски», `helmet` | person, no_helmet (обязательны); helmet (необязателен); helmet_required | `anchor` в зоне helmet_required и объект `no_helmet` привязан к голове → жёлтый, `hold_s` | вне зоны; в зоне и к голове привязан `helmet` | человек меньше `min_person_px` (`too_small`); к голове ничего не привязано (`head_unseen`); объект подходит двум людям (`owner_ambiguous`) | «Без каски в зоне «Цех 2»» |
| `no_respirator` | «Без респиратора в зоне обязательного респиратора», `mask` | person, no_respirator (обязательны); respirator; respirator_required | то же с `no_respirator` и зоной respirator_required | то же с `respirator` | то же | «Без респиратора в зоне «Покрасочная»» |

Привязка к голове (`rules/base.head_objects`): центр объекта в горизонтальных границах рамки человека и в верхней доле `head_frac` её высоты; подходит одному человеку — привязан; двум и больше — `ambiguous` у каждого. Без модели плагин в статусе `model_missing`, текст `texts.SCENARIO_MODEL_MISSING` v5 «Модель не подключена: нужны классы no_respirator» (было «Нет модели с классами: …»; меняется для всех плагинов).

Модели Матвея (`docs/ML_HANDOFF_MATVEY.md`, ветка `matvey_cv`): две записи 6.11.8 дописываются в `config/models.yaml` (существующие записи не меняются); `config/user.matvey.example.yaml` включает pose Матвея и каску как extra. Механизм проверяется без кода: в тестовом реестре каска в `pipeline.extra` делает `no_helmet` `active`, команда воркера для неё — `--nc 2` без `--classes`. Файлов `models/matvey/...` в репо нет: `doctor` с этим `user.yaml` честно пишет «нет файла» по каждому; есть файлы — `INFERENCE_BACKEND=local uv run safewatch doctor` и `eval` (запись слайса: итог).

### 8.23 Телефон по зонам; проекция груза (S22)

Телефон (было → стало строка `phone` 8.3): `anchor` в зоне `walkway` или `rest` (`rules.phone.ALLOWED_KINDS`) → `N` (событий нет, «зелёная линия»: позвонить начальнику, сфотографировать для отчёта); в зоне danger или vehicle_path — красный, `danger_hold_s` (как в v4); вне этих зон («рабочая зона») — жёлтый, `hold_s`. `ScenarioMeta.zone_kinds` телефона: `danger`, `vehicle_path`, `walkway`, `rest`. Сигнал «телефон в руках» по-прежнему привязка `attach_objects`; модель Матвея с классом `cell phone` подключается как extra без кода.

Проекция груза (HUD, упрощённо): объект `suspended_load` получает `HudObject.projection` — нормированный полигон `[(x1, y2), (x2, y2), (x2, 1), (x1, 1)]` (столбец под рамкой груза до низа кадра) и тег `load_projection` «зона под грузом»; это та же область, по которой правило `suspended_load` даёт красное (8.3). Рисует фронт. Без объекта груза полигона нет.

### 8.24 Звонок мастеру, очередь доставок, оператор с телефона (S23)

Когда событие переходит в `sent_to_master` (оператор подтвердил красное или передал, или автоэскалация по таймауту), мастер одновременно получает: WS `notification` (8.8), открытую карточку на телефоне (`/master` сам открывает `/master/events/:id`) и «звонок» — доставку `to_master` по каналам `delivery.calls`.

Очередь доставок в базе (было → стало 6.10 S15: `services._deliveries` в памяти): постановка — `INSERT OR IGNORE INTO delivery_queue (event_id, kind, level, created_at)` в той же транзакции, что и событие или действие (`level` — уровень события на момент постановки). `deliveries_flush`: строки очереди по `id`; для каждой — каналы `webhook:<name>` (все `kind`) и `call:<name>` (только `to_master`), у которых `level` строки входит в `levels`, без строки `deliveries` с тем же `(event_id, channel, kind)`; отправка в `asyncio.to_thread` по одной; строка `deliveries` и удаление строки очереди — в потоке event loop. Перезапуск сервера очередь не теряет. Имена каналов уникальны (6.11.8).

`CallChannel` с провайдером `stub`: реальной телефонии нет, `deliver` сразу отвечает успехом; строка `deliveries` `sent`, `delivered_at = at`; `Delivery.status_text` — «Звонок отправлен» (без `delivered_at`) или «Звонок доставлен (заглушка)». `Channel` для звонка: `kind = "call"`, `target` — номер с маской (`+7 900 ***-**-12`, пустой номер — «заглушка»). Подключение реального провайдера — новый `provider` и класс, без изменения очереди.

Оператор с телефона: экраны `/m/operator` и `/m/operator/events/:eventId` (8.14) поверх существующих `operator_feed`, `event_detail`, `event_action`; новых маршрутов API нет.

### 8.25 Калькулятор окупаемости и масштабирования (S24)

Все числа — `CalcAssumption` из `calculator.assumptions` (6.11.8) с подписью источника; `overrides` запроса заменяют значение по ключу (неизвестный ключ или отрицательное → 422). Ниже `A[key]` — действующее значение, `fps = pipeline.target_analysis_fps`.

Режим «Внедрение» (`calculator_rollout`, роль management):
- `incident_cost = downtime + fine + treatment + lawsuit`; `incidents_per_1000_workers = incidents_per_year / workers × 1000` (`workers = 0` → `None`);
- `accelerators = ceil(cameras × fps × A[models_per_frame] / A[accelerator.capacity_fps])`, `servers = ceil(accelerators / A[accelerators_per_server])`;
- `base`: `capex = accelerators × A[accelerator.price_rub] + servers × A[server.price_rub] + A[integration_rub]` (камеры существующие);
- `extended`: `base.capex + cameras × A[zones_per_camera] × A[light_sound_rub]`;
- `max`: `extended.capex + workshops × A[speaker_rub] + ceil(cameras × A[new_cameras_share]) × A[new_camera_rub]`;
- каждый уровень: `opex_year = capex × A[support_share_year]`, `savings_year = incidents_per_year × incident_cost × A[reduction.<tier>]`, `payback_months = capex / (savings_year − opex_year) × 12` при `savings_year > opex_year`, иначе `None` и строка «Не окупается при этих допущениях»; `items` — строки расчёта («Ускорители LinQ: 3 × 500 000 ₽»);
- `events_per_operator_shift = events_per_camera_day × cameras / (operators × shifts_per_day)`, где `events_per_camera_day` — события эфира (`is_demo = 0`, без `superseded`) за `stats.default_days` дней на живую камеру в день; данных нет или `operators × shifts_per_day = 0` → `None`.

Режим «Масштабирование» (`calculator_scale`, роли management, admin): `capacity_fps` — медиана `throughput_fps` артефактов `backend = linq`, `fake = 0` (подпись «замер приложения: N задач»), нет таких — `A[accelerator.capacity_fps]` с его источником; `accelerators_now` и `accelerators_total` — формула выше для `cameras_now` и `cameras_now + new_cameras`; `servers_total`; `capex = (accelerators_total − accelerators_now) × price + (servers_total − servers(cameras_now)) × server.price + new_cameras × new_camera_rub`.

`calculator_defaults`: пример завода (`RolloutIn`: 2 цеха, 8 камер, 2 смены, 200 работников, 2 оператора, 4 инцидента в год, простой 500 000 ₽, штраф 200 000 ₽, лечение 300 000 ₽, суды 500 000 ₽ — подпись «пример для демо, замените своими»), `ScaleIn` (8 + 8), допущения и `measured` (замер пропускной способности, RTT p50 последних задач LinQ, события на камеру в день). Экран делает Егор.

### 8.26 Ложное срабатывание → датасет (S25)

`datasets_flush` (пятая задача `TaskGroup` в `worker`, период `datasets.tick_ms`): события со статусом или вердиктом `false_alarm`, с эпизодом и без строки `dataset_items` → `dataset.build_item` в `asyncio.to_thread`, затем строка `dataset_items` (`UNIQUE event_id`: ровно один раз). Демо-событие сида (нет эпизода) пропускается.

Состав `datasets/false_alarms/<event_id>/`:
- `frames/<frame_idx>.jpg` — проанализированные кадры окна клипа (8.20), равномерно не больше `datasets.max_frames`, JPEG `evidence.jpeg_quality`;
- `detections.jsonl` — строки `FrameDetections` артефакта детектора для этих кадров, `pose.jsonl` — то же для pose (если был); формат `docs/ML_INTEGRATION.md` раздел 4;
- `hud.jsonl` — строки `HudFrame` этих кадров;
- `label.json` — `{event_id, label: "false_alarm", scenario, level, reason_text, video_sha256, video_filename, start_ms, end_ms, models: [id@version], analysis_version, comment}` (комментарий оператора из действия `false_alarm`).

Экспорт: `dataset_export(out)` и `GET /api/datasets/false-alarms/export.zip` — zip всех элементов и `manifest.json` (список `DatasetItem`); CLI `safewatch dataset export --out DIR`. `GET /api/datasets/false-alarms` — `DatasetView`.

### 8.27 Ручная идентификация нарушителя (S26)

`event_identify` (роли ohs, management): поля `IdentityIn` обрезаются по краям, длина каждого до `IDENTITY_MAX` (81 → 422 «Поле: до 80 символов»), пустая строка очищает поле. Порядок проверок как у `event_action` (S7): роль → поля → actor → 404. Есть изменение → `events.person_name`, `person_position`, `crew`, строка `event_actions` `identified` (`from_status = to_status` = текущий статус, комментарий «ФИО: …; должность: …; бригада: …» или «Идентификация очищена»), WS `event.updated`; изменений нет → 200 без строки журнала. Статус события не меняется; терминальные события тоже можно идентифицировать. `EventDetail.can_identify` — роль запроса ohs или management.

`people_stats_view`: период и демо — как `ohs_stats_view` (S13); `identified` — события с непустым `person_name` или `crew`; `by_person` — по `person_name` (ключ — имя), `by_crew` — по `crew`, `_count_rows` по убыванию; пустые значения не попадают в строки. CSV журнала (S12) получает в конце колонки «ФИО», «Должность», «Бригада» (добавление).

### 8.28 Паспорт пригодности камеры (S27)

`camera_passport(camera_id)`: активный анализ последнего `ready` видео камеры; нет → все сценарии `unknown` «Нет обработанного видео». Из HUD анализа (`build_passport`):
- `person_height_px_p50` — медиана высоты рамок людей в пикселях; `small_object_px_p50` — медиана большей стороны рамок `cell phone`; `person_frames_share` — доля кадров с людьми; `dark_share` — доля длительности в интервалах `dark` и `obstructed`; `empty_share` — доля кадров без объектов; `frames` — число кадров анализа.

Вердикт по каждому плагину (первое подходящее сверху):
1. статус не `active` → `unknown` «Модель не подключена» (или текст `skeleton`);
2. `frames < passport.min_frames` → `unknown` «Мало кадров для оценки»;
3. `dark_share > dark_unsuitable` → `unsuitable` «Слишком темно или камера закрыта N % времени»;
4. сценарий на людях и `person_height_px_p50 < features.min_person_px` → `unsuitable` «Люди слишком мелкие: N px»; нет людей → `unknown` «В записи нет людей»;
5. `phone`: `person_height_px_p50 < scenarios.phone.min_person_px` или `small_object_px_p50 < small_object_px` → `partial` «Телефон виден плохо: N px»;
6. у сценария есть `zone_kinds`, а у камеры нет ни одной зоны нужного типа, где без зоны сценарий не срабатывает (`fence_crossing`, `restricted_under`, `no_harness`, `no_helmet`, `no_respirator`, `fall` не требует) → `partial` «Нет зон: <типы>»;
7. `person_height_px_p50 < person_partial_px` или `dark_share > dark_partial` или `empty_share > empty_partial` → `partial` с причиной;
8. иначе `suitable` «Годна».

S32 добавляет `shift_px` и `shift_text` (8.33). v8: S32 снят владельцем, `shift_px = None`, `shift_text = ""` (6.14).

### 8.29 LinQ под медленную очередь (S28)

RTT TPU бывает до ~10,6 с на запрос (3.1). Было → стало:
- Таймаут прогона: `max(linq.job_timeout_s, 120 + ceil(frames / linq.inflight) × linq.slow_rtt_s)` секунд, где `frames = ceil(frame_count / step)` (для 720 кадров — 2280 с).
- Воркер получает `--reply-timeout <linq.reply_timeout_s>` (новый аргумент `video_worker.py`, по умолчанию 120 — прежнее поведение; `client.collect(..., timeout=reply_timeout)`).
- Прогресс честно виден: из `.progress` (`done`) и времени с `# sw:start` считаются `Job.rate_fps` и `Job.eta_s` (`(total − done) / rate`), `Job.status_text` — `texts.JOB_PROGRESS` «LinQ: 120 из 720 кадров · 3,1 кадр/с · осталось ~3 мин»; пока `done = 0` — «LinQ: ждём первый ответ TPU (очередь площадки)».
- `# sw:start` сначала гасит прежний воркер того же `<out>`: `[ -f <out>.pid ] && kill $(cat <out>.pid) 2>/dev/null; rm -f <out>.pid` (долг R5: осиротевший воркер); команда строится `LinqBackend._start_command(...)`.
- `RemoteShell.close()` и `InferenceBackend.close()`: `JupyterShell.close` закрывает kernel и сессию Jupyter (`shutdown_kernel`), повторный вызов — без ошибки; `services.backend_close()` зовут lifespan при остановке сервера и `doctor` в конце (долг R5: idle kernel на общем аккаунте). `FakeRemoteShell.close` пишет маркер `close`.
- `JupyterShell`: `JupyterError` с телом-HTML (`<html` без учёта регистра) или ответ не JSON → `InferenceError("bad_output")`; `backend_check` → `bad_answer` (долг R5).
- Живая проверка (лимит): ролик до 60 с, одна задача, `--inflight 4`; итог (кадр/с, RTT p50/p90, `eta_s` в начале и конце) — в запись слайса.

### 8.30 Пробелы `docs/ML_INTEGRATION.md` (S29)

Решение по каждому пункту раздела 9 документа (19 пунктов после дополнения Матвея). Слайс S29 закрывает отмеченные «S29», остальные оставлены с причиной; S29 дописывает в раздел 9 документа строку итога у каждого пункта.

| № | Пробел | Решение |
| --- | --- | --- |
| 1 | нет импорта внешних артефактов (Vast) | S29: CLI `import-artifact` поверх `artifact_import` (S17); провенанс — `--backend`, `--fake` |
| 2 | детектор жёстко COCO-80 | S29: `ModelSpec.nc` — у детектора с `nc` воркер получает `--nc <nc>`, `--classes` фильтрует ID внутри `0..nc−1` |
| 3 | имена техники зашиты, extra-техника не трекается | S29: `pipeline.vehicle_classes`; класс из списка у extra-модели — техника с трекингом |
| 4 | `proximity` требует все пять имён | S29: `person` и хотя бы один класс из `vehicle_classes` |
| 5 | нет сценария СИЗ | S20: `no_helmet`, `no_respirator` |
| 6 | `no_harness` ждёт негативный класс | оставлено осознанно: отсутствие рамки привязи не доказывает её отсутствие; ML-часть обучает `no_harness` |
| 7 | хвост обязателен | S29: `linq_tail: null` → воркер без `--tail`, проверка хвоста пропускается |
| 8 | имя входа жёстко `images` | S29: `ModelSpec.input_name` → `--input-name` |
| 9 | кэш не знает о весах | оставлено: смена `CACHE_SCHEMA` обнулит кэш демо-пакета и истории; правило «переобучил — подними `version`» в силе |
| 10 | падение extra валит задачу | S29: `remote_error`/`bad_output` extra-модели → анализ без неё, `error_text = "extra <ref>: <текст>"`, её классы не входят в `active_classes` снимка (сценарии — `model_missing` в этом анализе) |
| 11 | метрики extra не видны | S29: `Job.metrics` включает extra-модели (по `AnalysisConfig.extra_artifact_ids`) |
| 12 | `upload_program.py` навязывает префикс и staging | оставлено: инструмент ML-части и общая инфраструктура LinQ, прогон его не меняет (3.1) |
| 13 | fake не умеет extra-классы | оставлено: демо огня и груза — через демо-пакет с настоящими детекциями (8.19) |
| 14 | `local` только на CPU | S29: `local.providers` |
| 15 | pose зашит на 17 точек COCO | оставлено: других схем точек нет |
| 16 | файлы моделей без проверки целостности | оставлено: манифест — у ML-части (`MATVEY_MANIFEST.json`); `doctor` проверяет наличие |
| 17 | `active` не проверяет роль источника класса | оставлено частично: с S29 техника из extra трекается (п. 3); людей даёт только детектор |
| 18 | ограничения scorer `eval` | оставлено: метрики ML-части; отчёт сохраняет сноску о полноте разметки |
| 19 | калибровка compile-helper привязана к COCO128 | оставлено: инструмент компиляции ML-части, на ноутбуке капитана компиляция запрещена (3.1) |

### 8.31 Отчёт смены в PDF и долги приложения (S30)

`shift_report_pdf(at)` → `report_pdf.shift_pdf(shift_summary_view(at), product_name, timezone)`: A4, шрифт `DejaVuSans.ttf` (кириллица), заголовок «<продукт> · Сводка смены», смена и период по МСК, всего, таблицы по секторам и сценариям, список подтверждённых (время, сектор, камера, причина, статус). `GET /api/master/shift.pdf?at=` — `application/pdf`, `Content-Disposition: attachment; filename="shift-<YYYY-MM-DD>-<id>.pdf"`; `at` не разбирается → 422.

Долги `## open` (решение по каждому):

| Долг | Решение |
| --- | --- |
| R5: живой прогон, TPU не отвечал | закрыт 24.10 14:52 вживую (раздел 2); S28 и R32 — короткие проверки |
| S5: сцена `demo` теряет трек при падении | S30: этап 3 трекера — несопоставленный трек и несопоставленная детекция `score ≥ high_thresh`, центр ближе `tracker.reattach_bh × высота трека` → тот же id (смена позы «стоя → лёжа» меняет рамку, IoU падает); падение в сцене `demo` подтверждается веткой перехода «Зафиксировано падение» |
| S6: демо-события сида в ленте | S17 (8.19) |
| S10: `explain` новых плагинов, нет единицы дистанции у зоны | S30: строки «почему» каждого плагина S10 — правило с порогом и единицей, измеренное значение, зона |
| R5: загрузка ложится на диск до проверки роли и размера | S30: `X-Role` и `Content-Length` до чтения тела (6.11.6); поток без `Content-Length` — проверка размера при записи, как в 8.1 |
| S11: `_freshness` в потоке event loop | оставлено осознанно: чтение разовое, миллисекунды (запись R15) |
| S14: `eval` вторым процессом, без отката pose | S30: `eval` при живом сервере → exit 5 «Остановите сервер: uv run safewatch stop»; pose `remote_error`/`bad_output` → анализ без точек, как у задачи |
| S15: очередь доставок в памяти, уровень на момент flush, одинаковые имена | S23 (8.24) |
| S15: `docker build` не собирался | S21 (8.32) |
| R5: kernel Jupyter, осиротевший воркер, HTML → `unreachable` | S28 (8.29) |
| владелец: idle kernels, логи `D:\npm1.log`, `D:\scratch_fe.log` | остаются за владельцем: удаление на общем аккаунте и вне репо блокирует защита Claude Code |

### 8.32 Docker и развёртывание одной командой (S21; v10 — этап 1)

Подготовленный checkout запускается `docker compose up -d --build`. Подготовка: Docker Desktop/Engine и Compose 2.24+, свободный порт 8000, настоящий пакет в `data/demo/<name>/`, локальный `config/user.yaml` по `config/docker.example.yaml`. Сервис `safewatch`, рабочий каталог `/app`, Python 3.12 slim, frontend на Node 24 с lock-файлами; runtime включает исходники, config, contract, tools/linq, шрифт и собранный `frontend/dist`. Host dist не используется.

- SQLite и медиа приложения — именованный том `argus_data` в `/app/data/app`, имя `${ARGUS_DATA_VOLUME:-argus-upgrade-v3-stage1-data}`. `./data/app` хоста не монтируется и не удаляется. Старые тома не уничтожаются; новый показ с чистой БД получает отдельно выбранное имя тома.
- `./data/demo:/app/data/demo:ro` и `./models:/app/models:ro` сохраняются. Пользовательский `./config/user.yaml` монтируется в `/app/config/user.yaml` read-only, bind `create_host_path: false`: отсутствующий файл — ошибка подготовки, а не созданный каталог. Он исключён из build context вместе с `.env*`, данными, моделями и исследованиями. Изменение конфига применяется после пересоздания контейнера (`up -d --force-recreate`); пересборка образа из-за него не нужна.
- Пути конфига — Linux-пути внутри контейнера. Порядок YAML: default → user.example → user; неизвестные ключи запрещены. Демо-профиль: `data_dir: data/app`, `server.static_dir: frontend/dist`, `demo.pack: data/demo/argus-real-v2`, detector/pose `640-ap9999`, `pipeline.extra: []`, target 12 FPS. Запасной пакет — `data/demo/argus-real`; проверяется в отдельном томе, не поверх рабочего.
- `.env` необязателен (`required: false`). Compose не задаёт `LINQ_JUPYTER_URL` через environment: значение владельца из env_file сохраняется. Настоящий кэш не требует Jupyter и не требует `SAFEWATCH_FAKE=1`. Происхождение каждой задачи и пакета проверяется как `linq`, `fake=false`, `cached=true` для обеих моделей. `extra` без артефакта может вызвать живой инференс, поэтому демопрофиль указан явно.
- `serve --seed` идемпотентно создаёт мир и импортирует пакет; synthetic история `is_demo=1` не является доказательством LinQ. Проверяется `/api/demo/packs`, четыре готовых видео v2, реальные зоны/правила/калибровки относительно manifest. Импорт одноимённого пакета не обновляет его содержимое; существующие настройки камер не перезаписываются.
- Healthcheck использует Python urllib без curl. Приёмка дополнительно проверяет runtime-импорты, OpenCV-декод, ffmpeg/H.264/yuv420p/faststart и нечётные размеры, миграции/WAL/целостность, WS hello и доставку события, UI оператора → мастера → журнал. Неуспешная внешняя проверка остаётся невыполненной.
- `restart`, обычный `down` и `up` сохраняют БД, решения и настройки; повторный seed/import не размножает сущности. `down -v`, Purge и удаление host data не являются штатным запуском.
- Публичный адрес — существующий Tuna-хост на локальный порт 8000, не сервис Феди. Новый хост не создаётся. URL и токены не публикуются в репозитории; локальная передача отдельно. Готовность HTTPS требует REST, медиа и WebSocket на текущем origin, без mock/localhost/mixed content. Нет доступа к существующему Tuna — точный блокер, а не PASS.

Инструкция с нуля — `docs/DEPLOY.md`, фактические результаты — `docs/handoff/upgrade-v3-stage-1.md`. Исправление повторов эфира, полный аудит и калькулятор v2 относятся к следующим этапам; в этапе 1 они не заявляются готовыми.

### 8.33 Сдвиг камеры (S32, снят владельцем, v8)

При `calibration_set`, `zone_create` и `zone_update` сохраняется эталон — кадр превью камеры `data_dir/reference/<camera_id>.jpg`. `camera_passport` сравнивает эталон с текущим кадром превью (`media.frame_shift`: оба кадра в серый, ширина `shift.sample_width`, фазовая корреляция OpenCV, сдвиг в пикселях эталона): `shift_px`; `shift_px > shift.max_px` → `shift_text` «Камера сдвинута на N px: проверьте зоны и калибровку»; эталона нет → `shift_px = None`, `shift_text = ""`. Новой модели нет.

## 9. Валидация

Форма запроса проверяется моделями pydantic (FastAPI → 422 `validation`, сообщение «Неверные данные запроса», в `details` поле). Смысл проверяется в `services` (`ValidationFailed` с полем и русским текстом). Коды ошибок английские, тексты русские, без технических деталей и секретов.

| Вход | Правило | Ошибка и текст |
| --- | --- | --- |
| название сектора | обрезка пробелов, 1..`NAME_MAX` | 422 «Название: от 1 до 80 символов» |
| название сектора | уникально | 409 `name_taken` «Сектор с таким названием уже есть» |
| камера: имя | обрезка, 1..`NAME_MAX` | 422 «Название: от 1 до 80 символов» |
| камера: описание | до `DESCRIPTION_MAX` | 422 «Описание: до 300 символов» |
| камера: `sector_id` | сектор существует | 422 «Сектор не найден» |
| файл видео | расширение из `upload.extensions` | 415 «Формат не поддерживается: нужен mp4, avi, mov или mkv» |
| файл видео | размер до `upload.max_mb` | 413 «Файл больше 2048 МБ» |
| файл видео | читается OpenCV, есть кадры | 415 «Видео не читается» |
| окно треков | `0 ≤ from_ms < to_ms`, `to_ms − from_ms ≤ hud.window_max_ms` | 422 «Окно треков: до 10 с» |
| калибровка | `MIN_CAL_POINTS..MAX_CAL_POINTS` точек, число мировых равно числу точек кадра, координаты кадра в [0, 1], никакие три точки (кадра или мира) не на одной прямой (площадь треугольника `< MIN_AREA` для кадра, `< 0,01 м²` для мира), контрольных до 8 | 422 «Нужно от 4 до 8 точек», «Три точки на одной прямой», «Точки вне кадра» |
| зона | тип из `zone_kinds`; имя 1..`ZONE_NAME_MAX`; polygon 3..`ZONE_POINTS_MAX` точек, площадь `≥ MIN_AREA`; line ровно 2 разные точки; координаты в [0, 1] | 422 «Неизвестный тип зоны», «Линия — ровно 2 точки», «Полигон: от 3 до 32 точек» |
| параметры правила | ключи из `ScenarioMeta.params`, значение в [min, max] | 422 «Параметр hold_s: от 0 до 60» |
| сценарий в пути | есть в `rules.PLUGINS` | 404 «Сценарий не найден» |
| действие | комментарий до `COMMENT_MAX`; `resolve` — непустой после обрезки | 422 «Опишите принятые меры» |
| `X-Actor` | после декодирования 1..`ACTOR_MAX` | 422 «Имя: до 60 символов» |
| `X-Role` | значение из `Role` | 400 `role_required` «Выберите роль» |
| фильтр журнала | `limit` 1..`journal.page_max`; `date_from ≤ date_to`; `q` до `QUERY_MAX`; курсор от сервера | 422 «Неверный фильтр: <поле>» |
| статистика | `date_from ≤ date_to`; `weeks` 1..52 | 422 «Неверный период» |
| `jobs_list` | `limit` 1..`jobs.list_max` | 422 |
| разметка оценки | схема `EvalLabels`, `start_s < end_s`, файлы видео существуют | CLI exit 2 или 3 с текстом |
| v5: раскладка демо-пакета | схема `DemoLayout`; файлы видео существуют; `out` пуст; фейк только с `--allow-fake` | CLI exit 2 или 3 с текстом |
| v5: демо-пакет | схема `DemoManifest`; модели в реестре; sha256 видео совпадает; файлы артефактов есть | CLI exit 2 «Пакет повреждён: <что>» или 3 |
| v5: калькулятор | числа `≥ 0`; `cameras ≥ 1`, `workshops ≥ 1`; ключи `overrides` из `calculator.assumptions` | 422 «Неверное значение: <поле>» |
| v5: идентификация | каждое поле после обрезки до `IDENTITY_MAX` | 422 «Поле: до 80 символов» |
| v5: статистика по людям | `date_from ≤ date_to` | 422 «Неверный период» |
| v5: `import-artifact` | ссылка в реестре; JSONL проходит `read_jsonl`; видео существует | CLI exit 2 или 3 |
| v5: загрузка видео | `X-Role` и `Content-Length` до чтения тела | 400, 403, 413 до записи на диск |

Поиск `q`: `casefold(title || ' ' || reason_text || ' ' || camera_name) LIKE casefold('%' || q || '%') ESCAPE '\'` с экранированием `%`, `_`, `\`.

---

## 10. Тесты

Тесты выводятся из критериев приёмки слайса (раздел 16), а не из готового кода. Тест кодирует критерий, а не повторяет реализацию. Если установлен skill `engineering:testing-strategy`, следуй ему.

Запрещённый вид теста: «сохранили и проверили, что сохранилось» без теста на отказ.

На каждый слайс:
- **По критериям приёмки.** На каждый критерий с проверяемым условием: тест. На каждый критерий с отказом: тест на отказ.
- **Контрактные на стыках.** Ответы `services` и API валидируются моделями из 5.2; `contract/openapi.json` совпадает с приложением.
- **Идемпотентность.** Миграции, сид, тик эфира, повторная загрузка того же файла, повторная доставка webhook: эффект ровно один.
- **Путь ошибки.** `FakeRemoteShell` отдаёт каждый `Fault`; код даёт осмысленный статус задачи.
- **Property-based (hypothesis)** для геометрии (`point_in_polygon`, гомография) и трекера.

Тесты выводятся из критериев приёмки и из чисел и таблиц контракта (разделы 5–6) и поведения (раздел 8). Обязательно:

1. **Каждое число** (порог, лимит, TTL, таймаут, доля, размер) имеет тест на границе: значение ровно на пороге и на шаг ниже или выше. Для нечётких порогов (fuzzy, доли) нужна пара примеров по обе стороны в пределах 5% от порога. Число без такого теста считается непроверенным, слайс не закрывается.
2. **Каждая строка таблицы** (доменные правила, исходы, роли, маршруты) имеет свой тест или параметр в общем параметризованном тесте. Критерий может ссылаться на таблицу целиком: «все строки 8.2».
3. **Каждая ветка отказа** (каждый исход, кроме `ok`, каждый статус, каждое состояние лимита) имеет тест, где ветка срабатывает, и тест, где соседнее значение её не включает.
4. **Каждый ключ конфига, который читает код слайса**, имеет тест: другое значение ключа меняет поведение.
5. **Внешний ответ** (health, API, файл настроек) проверяется в четырёх состояниях: наш и ожидаемый; наш с другим значением; недоступен; ответ есть, но не наш или без нужного поля. Если в контракте нет поведения для последнего случая, это `CONTRACT GAP`.
6. **Тест, ждущий состояния, имеет таймаут** (`pytest-timeout` или аналог стека в гейте, по умолчанию 60 с; `timeout-minutes` у job в CI). Регрессия даёт красный, а не зависание.
7. **Условие, которое не различает ни один критерий**, удаляется или получает тест со сценарием, где оно меняет результат.
8. **Перед закрытием слайса нужна мутационная проверка**: 5 ручных мутаций на числах и ветках отказа слайса (сдвиг порога на 1, перевёрнутое условие, пропущенная запись в хранилище). Каждая ловится гейтом. Пропущенная мутация означает недостающий тест, а не повод закрыть слайс с долгом. Мутации откатываются, в коммиты не попадают.

### 10.1 Режим ночи (поправка владельца, главнее правил выше)

На ночь 24.10 время важнее полноты тестов. Правила 1–8 выше смягчаются так:
- Правила 1–3 (границы чисел, строки таблиц, ветки отказа) действуют полностью только для ядра: менеджер эпизодов (8.4), плагины (8.3), статусы (8.6), автоэскалация (8.7), публикация эфира (8.5), `LinqBackend` и политика повторов (8.1), состояние камеры и сектора (8.9), сопоставление оценки (8.18). Остальное (CRUD, экраны чтения, статистика, журнал): один положительный тест и один тест на отказ на функцию или группу функций; права ролей — один тест без роли и один с чужой ролью на слайс.
- Правило 4 — только для ключей ядра. Правило 5 — только для `backend_check` и `LinqBackend`.
- Правило 8: две мутации и только в слайсах 2, 5, 6, 7. В остальных слайсах мутаций нет.
- Ручных проверок в браузере нет. Критерий проверяется автотестом или запросом к API. Тесты времени используют `fake_clock`; реальные `sleep` в тестах запрещены, повтор теста 20 раз не нужен.
- Фронт: `frontend/src/App.test.tsx` (слайс 0), `frontend/src/components/hud.test.ts` (слайс 4) и по одному дымовому тесту на экран в `frontend/src/screens/screens.test.tsx`: экран рендерится с подменённым `api` и показывает ключевой текст. Других тестов фронта не пишем.
- Живые прогоны LinQ — только в слайсе 2 и в ревью R5 (раздел 16). Второй прогон — 10.3.

### 10.3 Второй прогон v5 (поправка владельца, главнее 10.1 там, где они расходятся)

Ночь 24.10 → 25.10, около 7 часов, сдача 25.10 10:00 МСК. Капитана нет; Матвей периодически заглядывает в ноутбук. Правила 10.1 действуют, кроме:
- Ядро для правил 1–3 v5 дополнительно: автокалибровка (8.21), плагины СИЗ (8.22), телефон по зонам (8.23), очередь доставок и звонок (8.24), формулы калькулятора (8.25 — каждая строка формулы и граница «окупается / не окупается»), вердикты паспорта (8.28 — каждая строка порядка), таймаут прогона LinQ (8.29).
- Правило 8: две мутации только в слайсах 19, 20, 23, 24.
- Демо-путь «событие → оператор → мастер → журнал» прикрыт регрессией: `tests/test_e2e.py` зелёный в каждом слайсе; S17 добавляет тот же путь от демо-пакета (`tests/test_demo_pack.py::test_demo_flow_reaches_master_and_journal`).
- Контракт только расширяется: каждый слайс, который пересобирает `contract/openapi.json`, проверяет, что пути и поля 1.0.0 на месте (`tests/test_contract_files.py::test_openapi_only_grows`, S16 кладёт снимок `contract/openapi.1.0.0.json`).
- Живые прогоны LinQ — только S17 (сборка демо-пакета на `data/videos/`), S28 и R32 (короткая проверка): по одной задаче, ролик до 60 с, `--inflight 4`. Приоритет TPU у Матвея: очередь `input` занята или туннель недоступен → работа на `SAFEWATCH_FAKE=1` и строка `долг`, повтор в следующем разрешённом шаге.
- Ноутбук капитана слабый (мало RAM, нет GPU): никакого обучения и перекомпиляции программ TPU; `local` в тестах — на маленьких фикстурах.
- Блокер, который снимает только человек, — строка `владелец: <что сделать>` в `## open` одной фразой: что нажать или запустить и зачем.
- Фронт: дымовой тест на каждый новый экран и компонент (`event_screen_plays_clip`, `operator_mobile_renders`, `operator_mobile_event_renders`, `master_opens_card_on_notification`).

### 10.2 Окружение

`tests/conftest.py`, собирается в слайсе 0:
- База: `connect(":memory:")` + `migrate()`, свежая на каждый тест. `data/` тесты не трогают: `data_dir` в `tmp_path`.
- Изоляция от машины владельца: ключи из `.env` и окружения обнуляются (`NO_KEYS`), `config/user.yaml` не читается, браузер подменён autouse-фикстурой `side_effects`. Новый побочный эффект добавляется в `SIDE_EFFECTS` в том слайсе, где появился.
- Ленивые синглтоны `services` (соединение, бэкенд, реестр, кэш `backend_check`, кэш превью, очередь доставок) сбрасывает фикстура `conn`. Новый синглтон добавляется туда же в своём слайсе.
- Сеть: тест без маркера `live` в сеть не ходит. LinQ — `FakeRemoteShell`, webhook — `respx`.
- Фейки: `SAFEWATCH_FAKE=1` даёт `LinqBackend(FakeRemoteShell())`. Фейк проверяет входы и умеет каждый `Fault`.
- Время: `fake_clock` подменяет `clock.now`, `advance(seconds)`; тики (`broadcast_tick`, `escalation_tick`) тесты вызывают напрямую.
- Видео: `make_video(tmp_path, seconds, fps, size, luma=None)` пишет mp4 (FourCC `mp4v`) через OpenCV; детекции — `fakes.scenes.render`. В репозиторий видео не кладутся.
- API: фикстура `client` (httpx `ASGITransport` + lifespan, как в README шаблона, фоновый `worker` в тестах выключен); WebSocket — `starlette.testclient.TestClient`.
- Модели: тест, которому нужны файлы `models/*.onnx`, пропускается (`pytest.mark.skipif` с причиной), если файлов нет; в CI их нет.
- Таймаут: `pytest-timeout`, `timeout = 60` в `[tool.pytest.ini_options]`.
- `tests/live/`: маркер `live`, пропуск без `LINQ_JUPYTER_URL` или при недоступном туннеле. В гейт не входят, запускаются `uv run poe live`.
- Фронт: vitest + jsdom + @testing-library/react; `api` подменяется `vi.mock`; рисование HUD проверяется через чистую `layoutHud`, canvas не тестируется.

---

## 11. Гейт, CI, ветки

`pyproject.toml`, задачи poe:
```
format   = "ruff format src tests scripts"
lint     = ["ruff format --check src tests scripts", "ruff check src tests scripts"]
check    = "mypy --strict src"
test     = "pytest -m 'not live'"
contract = "python scripts/contract_check.py"
api      = "safewatch contract --check"
eol      = "python scripts/eol_check.py"
frontend = { shell = "npm --prefix frontend run gate" }
gate     = ["lint", "check", "test", "contract", "api", "eol", "frontend"]
live     = "pytest -m live"
```
Запуск: `uv run poe gate`. ruff исключает `*.md` и требует LF. `pytest-timeout` валит зависший тест через 60 с. mypy: `ignore_missing_imports` для `cv2`, `onnxruntime`, `scipy.*`, `jupyter_remote`, `yolo_io`. **[проверить]** задачу `shell` у poe на Windows (Git Bash). Не работает — выбери самую простую рабочую форму вызова `npm` и запиши строку `GAP`.

Фронт, `frontend/package.json`: `gate = "npm run api:check && npm run lint && npm run typecheck && npm run test && npm run build"`; `api:gen = "openapi-typescript ../contract/openapi.json -o src/api/schema.d.ts"`; `api:check` — `scripts/api-check.mjs` генерирует типы во временный файл и сравнивает с `schema.d.ts`.

v10: при наличии файла `frontend/FRONT_OWNER` пропускаются только строки трассировки с путями `frontend/`: их заменяет gate Егора (`api:check`, lint, typecheck, vitest, build). Без маркера прежняя трассировка действует. Backend, REST/WS, тесты и другие пути не исключаются. Vitest ограничен двумя параллельными workers для воспроизводимости рядом с Docker: все тесты и прежние таймауты сохранены.

Сверка контракта (`scripts/contract_check.py`): читает таблицу 6.7 «Трассировка» и закрытые слайсы из `## log` файла `progress.md` (заголовки `### S<N>: ...`). Для каждой строки закрытого слайса ищет «искомую строку» в «файле», тест вида `путь::имя` проверяет по файлу и имени. Не нашёл: гейт красный с перечнем. Строки незакрытых слайсов пропускаются.

`scripts/eol_check.py`: `git ls-files --eol -- src tests scripts config contract frontend .github pyproject.toml uv.lock tech.md CLAUDE.md progress.md docs/brief.md`; строка с `i/crlf` → код 1 с перечнем.

CI: `.github/workflows/gate.yml` на `pull_request` и на `push` в `main`, матрица `windows-latest` и `ubuntu-latest`, `timeout-minutes: 20`. Шаги: checkout, `astral-sh/setup-uv`, `actions/setup-node` (Node 24, кэш npm по `frontend/package-lock.json`), `npm ci --prefix frontend`, `uv sync --locked`, `uv run poe gate`. Теги actions закрепить и проверить через `gh api`.

Защиты веток нет (нужен GitHub Pro). Контракт держит сверка в гейте. В `main` напрямую коммитятся только коммиты `docs(progress)` и `docs(tech)`. Ветку Матвея (`matvey_cv`) не трогать.

Цикл слайса:
1. `git checkout main && git pull`.
2. `git checkout -b slice-<N>-<short-name>` (ревью: `review-r<K>`, починка: `fix-<шаг>`).
3. Коммит `docs(progress): start slice N`.
4. Коммиты по ходу работы.
5. `uv run poe gate` зелёный локально (локальная машина на Windows, это половина матрицы CI).
6. Коммит `docs(progress): close slice N`.
7. `git push -u origin HEAD`, `gh pr create`, `gh pr merge --squash --delete-branch`, `git checkout main && git pull`, удалить локальную ветку. CI не ждать.
8. CI в режиме ночи проверяют только слайс 0 и ревью: первым делом `gh pr checks` по PR всех шагов с прошлого ревью. Красный CI: ветка `fix-<шаг>` от `main`, PR `fix: <что>`, тот же цикл.
9. Нет remote или `gh`: `git checkout main && git merge --squash <ветка> && git commit`, ветку удалить, в `## open` строка «нет remote».

Ожидание: ни одна команда не ждёт молча дольше 4 минут. Долгое (живой прогон, установка, долгие тесты) запускается в фоне и проверяется кусками: `timeout 230 bash -c 'until <проверка>; do sleep 5; done'`, потом снова. Конструкцию `sleep N; команда` Claude Code блокирует. Причина: кеш промпта живёт 5 минут, промах переписывает весь контекст по цене записи.

---

## 12. Конвенция текста

- Код, комментарии, коммиты, заголовки и описания PR, логи: по-английски. Интерфейс, отчёты, `progress.md`: по-русски.
- Коммиты: Conventional Commits, `type(scope): summary`; `type` из `feat|fix|test|refactor|chore|docs`; `summary` в императиве, со строчной буквы, без точки, до 50 символов; тело только чтобы объяснить почему.
- Коммить по ходу работы маленькими логическими шагами.
- PR: заголовок `slice N: <name>` (`review: R<K>`, `fix: <что>`). Тело: что делает, какие контракты затрагивает, чем покрыт тестами. До десяти строк.
- Комментарий в коде объясняет причину решения, не пересказывает строку. Закомментированный код не оставлять.
- Проза: активный залог, конкретика, без вводных оборотов, без длинного тире, без наречий-усилителей. Если установлен skill `stop-slop`, следуй ему.
- Кодировка и концы строк: файлы читаются и пишутся с `encoding="utf-8"`, текст пишется с `newline="\n"`. Точка входа CLI переключает `stdout` и `stderr` на UTF-8: консоль и пайп Windows в cp1252 падают на кириллице. Пути приложения в репо только в LF (`.gitattributes`, `scripts/eol_check.py`).

---

## 13. Definition of Done одного слайса

1. Критерии приёмки слайса из раздела 16 выполнены и проверены автотестами или запросами к API. Браузер не открывается.
2. Живые проверки LinQ — только там, где их требует слайс (S2, R5; v5: S17, S28, R32), в пределах лимита из `CLAUDE.md`. Туннель недоступен — строка `долг` в `## open`, слайс закрывается.
3. Тесты выведены из критериев по разделам 10, 10.1 и 10.3, мутации — только в слайсах 2, 5, 6, 7 (v5: 19, 20, 23, 24); `uv run poe gate` зелёный локально (вместе со сверкой контракта).
4. PR смёрджен squash без ожидания CI, ветка удалена (или локальный путь из 11, пункт 9).
5. Новых файлов и абстракций сверх раздела 4 нет.
6. Мёртвого кода нет: неиспользуемых экспортов, функций, шаблонов, стилей.
7. Коммиты по разделу 12, файлы в LF.
8. `tech.md` внутри слайса не изменён.
9. `progress.md` обновлён коммитом `docs(progress): close slice N` до мёрджа.

---

## 14. CONTRACT GAP

`CONTRACT GAP`: нужного контракта нет в `tech.md` или существующий мешает критерию приёмки. Работа не останавливается.

1. Выбери самую простую форму, совместимую с `tech.md`, и следуй ей. Можно добавить элемент или изменить существующий.
2. Изменение существующего контракта: код и тесты всех затронутых слайсов правятся в этом же слайсе. Гейт зелёный, сверка контракта (раздел 11) тоже.
3. Запиши строку в `## open` файла `progress.md`:
   - добавление: `GAP: <слайс>, <что>, <точная форма>` (сигнатура, колонка с типом, форма ответа);
   - изменение: `GAP: <слайс>, <что>, <было> → <стало>`.
4. Следующие сессии считают строку `GAP` контрактом наравне с `tech.md`.
5. Ревью стадии переносит все строки `GAP` в `tech.md` отдельным коммитом `docs(tech): vN`: разделы 5–6 и строки трассировки, новая версия и changelog в разделе 0. Потом убирает строки из `## open` и обновляет версию в шапке `progress.md`.
6. Тип, поле или функция в коде без контракта и без строки `GAP` — нарушение. Ревью их ищет.

Для фронта: изменение `contract/openapi.json` — тоже `CONTRACT GAP`. Разрешено только добавлять поля, маршруты и типы сообщений; удаление и переименование ломают фронт Егора и делаются только владельцем.

---

## 15. Правила поведения в сессии

- Думай до кода: назови допущения, при неоднозначности назови допущение и запиши его (запись слайса в `## log` или строка `GAP`). Владелец не сидит у терминала: вопросов не задавай.
- Простота: ничего сверх запрошенного, никаких абстракций под одноразовый код, никакой обработки ошибок, которых не бывает.
- Хирургические правки: соседний рабочий код не улучшай. Каждая изменённая строка следует из текущего слайса.
- Проверяемость: слайс готов, когда выполнены критерии и гейт зелёный, а не когда «выглядит готово».
- Один слайс или одно ревью за заход.
- Скорость ночи: бэкенд и контракт важнее фронта; фронт — минимально рабочий (8.14).
- Реальные настройки владельца (Claude Code, профиль, ОС) не трогай: команды, которые их меняют, запускай только с путём на временный файл.
- Долгие команды по правилу ожидания из раздела 11. Сервер для проверки запускай в фоне и останавливай `uv run --no-sync safewatch stop`.
- Ключи: их состояние показывает `uv run safewatch doctor` (`.env` в шелле не читай).
- LinQ — по правилам 3.1: только `~/work/baseline/`, чужое не трогать, одна задача на TPU.
- `main` всегда зелёный. Критерий не выполняется: сделай максимум, остальное в `## open` строкой `долг: <слайс>, <критерий>, <что не так>`, часть выключи явно (флаг конфига или `pytest.mark.skip(reason=...)`), слайс закрой.
- Если установлен skill Karpathy, следуй ему.

---

## 16. Очередь и слайсы

Порядок жёсткий, сверху вниз. Один шаг за заход. Слайс вертикальный: от хранения до пользователя. Половина слайса не закрывается. Порядок идёт по демо-пути: загрузили видео → LinQ → эпизоды → эфир и красный захват → решение оператора → мастер → журнал и статистика.

Ревью (раздел 17) в режиме ночи — после стадии из 5 слайсов, называется по последнему слайсу: `R5`, `R10`, `R15`; v5: `R20`, `R25`, `R30`, `R32`. После слайса 0 ревью нет: его чек-лист «каркас готов» и есть ревью.

Очередь: `S0, S1, S2, S3, S4, S5, R5, S6, S7, S8, S9, S10, R10, S11, S12, S13, S14, S15, R15, S16, S17, S18, S19, S20, R20, S21, S22, S23, S24, S25, R25, S26, S27, S28, S29, S30, R30, R32`

v5: S0–S15 и R5, R10, R15 закрыты в первую ночь (24.10). Второй прогон начинается с S16. Порядок S16–S32 — по ценности (`UPGRADE_v1.md`, раздел 4): обрыв прогона оставляет главное. S31 и S32 — «если останется время». v8: владелец снял S31 и S32 (25.10); после R30 идёт только R32 — финальная проверка.

---

### Слайс 0: каркас

**Файлы:** из шаблона: `pyproject.toml`, `.python-version`, `.gitignore`, `.gitattributes`, `.env.example`, `.github/workflows/gate.yml`, `config/default.yaml`, `config/user.example.yaml`, `src/safewatch/{__init__,config,types,db,services}.py`, `src/safewatch/migrations/0001_init.sql`, `src/safewatch/fakes/{__init__,remote}.py`, `tests/conftest.py`, `scripts/contract_check.py`, `tests/test_contract_check.py`. Проектные: `config/models.yaml`, `contract/{openapi.json,ws.schema.json,ws-examples.json}`, `scripts/eol_check.py`, `src/safewatch/{__main__,cli,errors,texts,clock,store,api,hub,worker,registry,seed,doctor}.py`, `src/safewatch/fakes/scenes.py`, `src/safewatch/rules/__init__.py` (пустой `PLUGINS`), `tests/test_{db,config,contract_files,api_skeleton,fakes,seed,cli,hub,clock}.py`, фронт: `frontend/{package.json,package-lock.json,tsconfig.json,vite.config.ts,eslint.config.js,index.html,.env.example,.env.mock}`, `frontend/mock/ws-mock.mjs`, `frontend/scripts/api-check.mjs`, `frontend/src/{main.tsx,App.tsx,App.test.tsx,nav.ts,roles.ts,theme.css}`, `frontend/src/api/{schema.d.ts,client.ts,useApi.ts,ws.ts}`, `frontend/src/components/{AppShell,RoleSwitcher,StubNotice,Badges}.tsx`; раздел в `README.md`.

**Что делает:**
1. Репозиторий `D:\msk-prom2026-mark` уже есть (remote `origin`, базовая ветка `main`): `git checkout main && git pull`, ветка `slice-0-skeleton`. В worktree оркестратора пути те же от корня.
2. `.venv`: если в `.venv/pyvenv.cfg` нет строки `uv = ` (это venv инструментов LinQ на Python 3.11), `mv .venv .venv-linq` и в `tools/linq/README.md`, `docs/ENVIRONMENT.md` заменить `.venv\Scripts\python.exe` на `.venv-linq\Scripts\python.exe`. Других правок в этих файлах нет.
3. Шаблон поверх существующих файлов: `mv .gitignore .gitignore.repo`, так же `.gitattributes` и `.env.example`; затем
   `python -X utf8 "C:/Users/user/.claude/skills/slice-start/template/new_project.py" . project=safewatch package=safewatch "description=SafeWatch: video safety monitoring on LinQ TPU" ENV_PREFIX=SAFEWATCH`.
   Слияние: `.gitignore` = строки репо + строки шаблона, которых нет, + `data/app/`, `.venv-linq/`, `frontend/node_modules/`, `frontend/dist/`; `.gitattributes` = правила раздела 4 + строки LFS репо (без BOM), без глобального `* text=auto eol=lf`; `.env.example` = ключи репо + `SAFEWATCH_FAKE=0`, `INFERENCE_BACKEND=linq`, без `EXAMPLE_API_KEY`. Файлы `*.repo` удалить.
4. Убрать пример шаблона: `Item`, `SourceClient`, `FakeSource`, `search`, таблицу `items`, секцию `example`, `tests/test_services.py` (тесты `test_settings_carry_no_keys_and_no_fakes` и `test_browser_never_opens` перенести в `tests/test_config.py`), переписать `tests/test_fakes.py` под `FakeRemoteShell`.
5. `pyproject.toml`: зависимости раздела 3, `[project.scripts] safewatch = "safewatch.cli:main"`, задачи poe и настройки mypy раздела 11. `uv sync` (создаёт `.venv` на 3.12 и `uv.lock`).
6. Бэкенд: конфиг 6.6 целиком (`config.py` с секциями и `extra="forbid"`, `default.yaml`, `models.yaml`); `types.py` 5.2 целиком; схема 5.1 целиком; `errors.py`, `texts.py`, `clock.py`, `store.py` (`tx`, `one`, `all`, `run`), `registry.py`, `hub.py`; `services.py` со всеми сигнатурами 6.2: работают `health` и `seed_demo`, остальные `raise NotImplementedError("slice N")`; `api.py`: `create_app`, все маршруты 6.4 (обработчики уже зовут фасад), зависимости `X-Role` и `X-Actor`, перевод ошибок в `ApiError` и коды 6.2, 501 для `NotImplementedError`, `/ws` с `hello`, раздача `server.static_dir`, lifespan запускает `worker.run_forever` (в слайсе 0 цикл только ждёт остановки); `cli.py`: `serve`, `stop`, `seed`, `doctor`, `contract`; `doctor.py` по 8.17 (без `backend_check`); `seed.py` по 8.16; фейки 6.1 (`FakeRemoteShell`, `scenes`); `contract/*` сгенерированы, `ws-examples.json` написан руками; `scripts/eol_check.py`.
7. Фронт (минимально, 8.14–8.15): Vite + React + TS strict; `nav.ts` со всеми маршрутами раздела 8.14, каждый рендерит `StubNotice` с номером слайса; `AppShell` с переключателем роли, бейджем бэкенда (из `/api/meta`, до S1 — «нет данных») и часами МСК; `roles.ts`; `api/client.ts` (заголовки `X-Role`, `X-Actor`), `useApi`, `useWs`; `Badges`; тема `theme.css`; мок `npm run mock` и `npm run dev:mock`; `api:gen`, `api:check`, `gate`. `vite.config.ts` проксирует `/api` и `/ws` на `127.0.0.1:8000`.
8. CI `gate.yml` по разделу 11.
9. `README.md`: в начало раздел «Приложение SafeWatch»: запуск на Windows (`uv sync`, `npm ci --prefix frontend`, `npm run build --prefix frontend`, `uv run safewatch serve --seed`, открыть `http://127.0.0.1:8000`), мок-режим для фронтендера, переключение бэкенда (`INFERENCE_BACKEND`, `SAFEWATCH_FAKE`), куда класть видео (`data/videos/` + `safewatch import` или загрузка в UI), где контракт (`contract/openapi.json`, `contract/ws.schema.json`). Существующий текст README не меняется.
10. PR `slice 0: skeleton`, мёрдж по разделу 11; CI этого PR проверяется `gh pr checks` (это «тривиальный PR» чек-листа).

**Критерии приёмки (чек-лист «каркас готов»):**
1. `uv run poe gate` зелёный: lint, mypy, pytest, сверка контракта, `api`, `eol`, `frontend`.
2. CI зелёный на PR слайса в обеих ОС (`gh pr checks <PR>`), или локальный режим записан в `## open`.
3. `migrate()` на чистой базе создаёт все таблицы 5.1; повторный вызов ничего не меняет; `UPDATE` и `DELETE` в `event_actions` падают; второй `playing`-эфир той же камеры падает на индексе; `casefold` зарегистрирована.
4. `FakeRemoteShell` ведёт себя по таблице 6.1 для каждой записи сценария (`None` и все 4 `Fault`); `scenes.render` даёт строки, проходящие `FrameDetections`, одинаковые при одном `seed`.
5. `Settings.fake` читается из `SAFEWATCH_FAKE`; в тестах `fake=False` и ключи пустые.
6. Тесты не видят ключей `.env` и `config/user.yaml` владельца; браузер в тестах не открывается.
7. Каждый общий компонент раздела 7 со слайсом 0 используется хотя бы в одном месте кода или теста.
8. `uv run poe eol` проходит; файл с CRLF в путях приложения валит проверку (тест во временном git-репо).
9. `safewatch serve --port <свободный>` подпроцессом отвечает на `GET /api/health` `{"status":"ok","contract":"1.0.0"}` за 20 с, пишет `server.pid`; `safewatch stop` останавливает сервер и удаляет файл; занятый порт → exit 2.
10. `safewatch stop`: pid-файл с чужим временем старта → exit 1, процесс жив, файл удалён; нет файла → exit 0 «not running».
11. Все маршруты 6.4 объявлены; маршрут незакрытого слайса отвечает 501 `not_implemented`; каждый наследник `AppError` даёт свой код (тест на временном маршруте); ошибка формы запроса → 422 `validation`.
12. `safewatch contract --check` → 0, `openapi.json` и `ws.schema.json` совпадают с приложением; изменённая модель → 1. В `ws-examples.json` по примеру на каждый `WsType`, каждый проходит `WsMessage`.
13. `/ws?role=operator` присылает `hello` с ролью и версией контракта; `/ws?role=boss` закрывается кодом 4400. `Hub`: сообщение с `audience=["master"]` не доходит до оператора; `CLIENT_QUEUE` сообщений без чтения — клиент жив, на одно больше — отключён.
14. `safewatch seed` на пустой базе: 4 сектора, 8 камер, зоны, `EVENTS` событий с историей действий (первое действие `published`, статус равен итогу истории), всё `is_demo=1`; повторный запуск: `skipped=true`, счётчики не меняются; вывод — JSON `SeedReport`.
15. `safewatch doctor` при `SAFEWATCH_FAKE=1` → 0; без ключей, бэкенд `linq`, без фейка → 4 и строка «LINQ_JUPYTER_URL: нет»; значение ключа (тест ставит секрет) в выводе не появляется.
16. `clock.iso` и `clock.parse` — круговое преобразование UTC с миллисекундами и `Z`.
17. `registry` превращает `pipeline.detector` и `pipeline.pose` в `ModelSpec`; неизвестная ссылка — ошибка запуска с текстом.
18. Фронт: `npm --prefix frontend run gate` зелёный; переключатель роли меняет навигацию на пункты роли; каждый маршрут показывает `StubNotice` с номером слайса; клиент шлёт `X-Role` текущей роли; `useWs` подключается к `/ws?role=<роль>`; бейджи уровня и статуса показывают текст и иконку.
19. Каталоги `Deep-Research/`, `docs/linq/`, `secrets/`, `vendor/`, `models/`, `results/` не изменены: `git diff --stat main -- Deep-Research docs/linq secrets vendor models results` пуст.

**Тесты** (имена совпадают с таблицей 6.7, сверка контракта проверит их при закрытии слайса):
- `tests/test_db.py`: 3 — `test_migrate_creates_tables`, `test_second_migrate_changes_nothing`, `test_event_actions_are_append_only`, `test_one_playing_broadcast_per_camera`, `test_connect_registers_casefold`;
- `tests/test_fakes.py`: 4 — `test_fake_remote_faults`, `test_scenes_are_valid_and_deterministic`;
- `tests/test_config.py`: 5, 6, 17 — `test_settings_carry_no_keys_and_no_fakes`, `test_browser_never_opens`, `test_owner_user_yaml_does_not_reach_tests`, `test_relative_data_dir_resolves_from_the_repo`, `test_models_registry_resolves_active_models`;
- `tests/test_contract_files.py`: 8, 12 — `test_eol_check_flags_crlf`, `test_openapi_matches_app`, `test_contract_check_detects_drift`, `test_ws_schema_matches_types`, `test_ws_examples_cover_every_type`, `test_types_export_contract_names` (все имена из 5.2 есть в `safewatch.types`);
- `tests/test_cli.py`: 9, 10, 15 — `test_serve_starts_and_stops`, `test_stop_ignores_foreign_pid`, `test_doctor_fake_mode_ok`, `test_doctor_reports_missing_keys`;
- `tests/test_api_skeleton.py`: 11, 13 — `test_health_ok`, `test_every_contract_route_is_declared`, `test_unbuilt_route_returns_501`, `test_app_errors_map_to_status_codes`, `test_ws_hello_and_unknown_role`;
- `tests/test_hub.py`: 13 — `test_audience_filtering`, `test_queue_overflow_drops_client`;
- `tests/test_seed.py`: 14 — `test_seed_creates_demo_world_once`, `test_seed_cli_reports_counts`;
- `tests/test_clock.py`: 16 — `test_iso_roundtrip_utc_millis`;
- `tests/test_contract_check.py` из шаблона без изменений (`test_closed_slice_element_not_found_is_red` и остальные);
- `frontend/src/App.test.tsx`: 18 — `role_switcher_changes_nav`, `stub_screens_show_slice`, `client_sends_role_header`, `ws_connects_with_role`, `badges_show_text_and_icon`.

**Не делать:** логику слайсов 1+ (кроме `health` и сида); реальные вызовы LinQ; ORM; авторизацию; правки `tools/linq/` кроме пути `.venv` в README; полировку фронта; коммиты видео, моделей, `data/app/`.

---

### Слайс 1: секторы и камеры (эталон)

Эталонная вертикаль. Слайсы 2+ повторяют её структуру: функции `store` → фасад `services` (права, валидация, транзакция, публикация в `hub`) → маршрут `api` (объявлен в S0, теперь работает) → экран фронта из общих компонентов → тесты через `client` (HTTP) и дымовой тест экрана.

**Файлы:** `src/safewatch/{store,services,texts}.py`, `frontend/src/screens/admin/CamerasScreen.tsx`, `frontend/src/components/{Form,DataTable}.tsx`, `frontend/src/nav.ts`, `tests/test_cameras.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** реализует `meta`, `sectors_list`, `sector_create`, `sector_update`, `sector_delete`, `cameras_list`, `camera_get`, `camera_create`, `camera_update`, `camera_delete`, `cameras_admin_view` и экран `/admin/cameras`.

**Критерии приёмки:**
1. `GET /api/meta`: `product_name`, `contract = "1.0.0"`, бэкенд и `fake` из `Settings`, 5 ролей с русскими названиями и действиями по таблице прав 6.2 (оператор: `view`, `confirm`, `false_alarm`, `send_to_master`; мастер: `accept`, `resolve`; остальные пусто), 2 уровня, 9 статусов с названиями и флагом терминальности по 8.6, 8 типов зон из конфига, сценарии из `rules.scenario_metas()` (до слайса 5 — пусто).
2. Сектор: создание админом → 201; имя обрезается; пустое или 81 символ → 422, 80 — ок; повтор имени → 409 `name_taken`; переименование `PUT`; список по `sort_order`, затем по имени.
3. Удаление сектора с неудалёнными камерами → 409 `sector_not_empty`; пустого → 204.
4. Камера: имя 1..80, описание до 300, несуществующий сектор → 422 «Сектор не найден»; ответ с `has_calibration=false`, `zones_count=0`, `videos_count=0`.
5. `PATCH` камеры меняет только переданные поля, в том числе сектор.
6. `DELETE` камеры → 204; затем `GET` → 404, камеры нет в списках и в `cameras_admin_view`; строка в базе осталась с `deleted_at`; играющий эфир (появится в S6) останавливается.
7. Пишущий вызов без `X-Role` → 400 `role_required`; с ролью `operator` → 403.
8. Неизвестный id → 404 `not_found` с русским текстом.
9. `cameras_admin_view` отдаёт секторы и камеры со счётчиками.
10. Экран `/admin/cameras`: список секторов и камер, создание сектора и камеры в модальной форме, текст ошибки API у формы, удаление с подтверждением.

**Тесты:** `tests/test_cameras.py`: 1 `test_meta_lists_roles_statuses_zone_kinds`; 2 `test_sector_crud_and_unique_name`; 3 `test_sector_delete_with_cameras_conflicts`; 4 `test_camera_rejects_bad_input`; 5, 6 `test_camera_crud_soft_delete`; 7 `test_writes_require_admin_role`; 8 `test_unknown_ids_are_404`; 9 `test_cameras_admin_view_shape`. `frontend/src/screens/screens.test.tsx::cameras_screen_renders`: 10.

**Не делать:** загрузку видео, правила и зоны камер, пагинацию, сортировку в UI, цвета секторов.

---

### Слайс 2: загрузка видео и обработка на LinQ

**Файлы:** `src/safewatch/{services,store,media,worker,cli,api}.py`, `src/safewatch/inference/{__init__,artifacts,linq}.py`, `frontend/src/screens/admin/CameraSetup.tsx`, `frontend/src/nav.ts`, `tests/test_{videos,jobs,linq_backend}.py`, `tests/live/test_linq_live.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** загрузка и импорт видео (8.1), очередь задач с политикой повторов, `make_backend`, `JupyterShell`, `LinqBackend` (команды 6.1, таймаут прогона с остановкой воркера), кэш артефактов, `run_next_job` до стадии `inference_pose`, отдача файла видео с Range, CLI `import`, вкладка «Видео» экрана настройки камеры, цикл задач в `worker`.

**Критерии приёмки:**
1. Загрузка mp4 (`make_video` 3 с, 25 fps, 320×240) админом → 201: видео `uploaded` с метаданными (fps 25, 75 кадров, длительность 3000 ± 40 мс), `codec = "mp4v"`, `browser_playable=false`; задача `process` `queued`; файл `uploads/<sha256>.mp4`; WS `job.progress`.
2. Тот же файл той же камере → `reused=true`, то же видео, текущая задача; после `done` — `job=None`. Тот же файл другой камере — новое видео.
3. `.txt` → 415; мусор с расширением `.mp4` → 415 «Видео не читается», в `uploads/` ничего не осталось; несуществующая камера → 404; без роли → 400.
4. Лимит (`upload.max_mb = 1` в тесте): поток ровно 1 МиБ проходит проверку размера (дальше 415 от проверки видео), 1 МиБ + 1 байт → 413, временный файл удалён.
5. `run_next_job` в режиме фейка: стадии `inference_detect` → `inference_pose`, прогресс не убывает и доходит до 1, задача `done`, видео `ready`, в `metrics` два элемента (`detect`, `pose`) с `backend=linq`, `fake=true`, `frames_processed = ceil(frame_count / step)`; две строки `artifacts` и их файлы.
6. Кэш: второе видео с тем же sha256 → у фейка нет команды `start`, `cached=true`; смена `pipeline.detector` на `det-yolov8n@960-ap9999` → новый прогон.
7. Шаг (`target_analysis_fps` 12): 25 fps → 2, 30 → 2, 60 → 5, 10 → 1, 12 → 1, 24 → 2; при `target_analysis_fps = 6` и 25 fps → 4; конфиг с `target_analysis_fps < min_analysis_fps` не загружается.
8. Команды `LinqBackend` (по записям фейка): папка `baseline`, файлы с префиксом `baseline_`, `--inflight 4`, программа и размер из реестра, `--conf 0.1`, `--classes 0,2,5,6,7,67` только у детектора, `--tail tails/<имя>`; строки `mosprom_work` нет; повторный прогон того же видео не загружает видео снова (размер совпал).
9. `read_jsonl` (параметризованно): валидный файл → кадры; не JSON, нет поля, `frame_idx` не растёт, число строк не равно ожидаемому → `bad_output`.
10. Политика повторов (8.1): `unavailable` → `retry_wait`, `next_attempt_at = now + 30 с`; вторая неудача → `+120 с`; третья (`max_attempts` 3) → `failed`, `linq_unavailable`, видео `failed`; `bad_output` → сразу `failed`; `jobs.max_attempts = 1` → `failed` с первой неудачи. Нет файла хвоста → `failed`, `model_missing`. Pose `remote_error` → задача `done` без pose, `error_text` начинается с `pose:`.
11. `timeout`: при `linq.job_timeout_s = 0.2` и `poll_interval_s = 0.01` фейк получает `kill`, задача `retry_wait` с `timeout`.
12. `JupyterShell` превращает `requests.ConnectionError` и ошибку входа в `InferenceError("linq_unavailable")`; пароля в тексте нет.
13. `GET /api/videos/{id}/file` с `Range: bytes=0-99` → 206, 100 байт, `Content-Range`; без Range → 200.
14. `safewatch import FILE --camera ID` → 0 и JSON; нет файла или камеры → 3; плохой формат → 2.
15. `camera_setup_view`: камера, видео и задачи по убыванию даты, `calibration=None`, `zones=[]`, `rules=[]`, `broadcast=None` до своих слайсов.
16. Вкладка «Видео»: загрузка с прогресс-баром, список видео со статусом, прогресс задачи по WS, таблица замеров после `done`, бейдж «фейк», предупреждение «Браузер может не воспроизвести кодек mp4v: нужен H.264», если `browser_playable=false`.
17. Живой прогон (один, по лимиту): `INFERENCE_BACKEND=linq`, без фейка, туннель поднят: `safewatch import data/videos/synthetic_coco_40x1s.mp4 --camera <id>` и обработка задачи → `done`; кадр/с, RTT p50/p90 и время всего записаны в запись слайса. Туннель недоступен → `долг`.

**Тесты:** `tests/test_videos.py`: 1 `test_upload_probes_and_queues_job`, 2 `test_upload_same_file_reuses_video`, 3 `test_upload_rejects_bad_files`, 4 `test_upload_limit_boundary`, 13 `test_video_file_supports_range`, 14 `test_import_cli`, 15 `test_camera_setup_view_shape`; `tests/test_jobs.py`: 5 `test_job_runs_detect_then_pose` и `test_job_progress_published`, 6 `test_cache_hit_skips_remote`, 7 `test_step_from_fps`, 10 `test_backoff_and_max_attempts`, 11 `test_timeout_kills_remote_worker`, `test_make_backend_by_settings`; `tests/test_linq_backend.py`: 8 `test_commands_use_baseline_dir_and_registry`, 9 `test_jsonl_validation_rows`, 12 `test_jupyter_shell_maps_errors`; `tests/live/test_linq_live.py::test_linq_processes_short_clip`: 17; `screens.test.tsx::camera_setup_renders`: 16. Мутации: 2.

**Не делать:** анализ и HUD, ручной повтор задачи, `LocalBackend`, проверку состояния LinQ, параллельные задачи, перекодирование видео, изменение `tools/linq/`.

---

### Слайс 3: локальный бэкенд, состояние LinQ и замеры

**Файлы:** `src/safewatch/{services,doctor,cli}.py`, `src/safewatch/inference/{local,linq}.py`, `frontend/src/screens/admin/SystemScreen.tsx`, `frontend/src/components/AppShell.tsx`, `tests/test_{local_backend,backend_check,system,jobs_retry}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `LocalBackend` (8.1), `backend_check` (команды `check` и `ls` из 6.1, кэш, WS `backend.status`), `job_retry`, `recover_jobs` в `serve`, `models_view`, `system_view` (камеры появятся в S6, каналы доставки — в S15), экран `/admin/system`, бейдж состояния бэкенда в шапке, `doctor` через `backend_check`.

**Критерии приёмки:**
1. `backend_check` для `linq` в четырёх состояниях: всё на месте → `ok`, `present` — программы активных моделей, `latency_ms`; нет программы или файла хвоста → `models_missing` со списком; `unavailable` → `unreachable`; ответ `check` не равен `ok` (Jupyter отдал HTML) → `bad_answer`. Для `local`: ONNX есть → `ok`, нет → `models_missing`. Фейк → `ok` с текстом «фейк».
2. Повторный вызов в пределах `linq.check_cache_s` не ходит в LinQ; `force=True` ходит; после истечения (`fake_clock`) ходит снова. Каждая реальная проверка публикует `backend.status`.
3. `LocalBackend` (тест пропускается без ONNX): JSONL проходит `read_jsonl`, кадров `ceil(n / step)`, классы из реестра; нет ONNX → `model_missing`.
4. `job_retry`: задача `failed` → `queued`, `attempts = 0`, ошибка очищена; не `failed` → 409 `job_not_failed`; оператор → 403.
5. `recover_jobs`: `running` → `queued`, возвращает число; `serve` вызывает при старте.
6. `system_view`: бэкенд, `fake`, последний статус бэкенда (или `unchecked`), очередь, последние 20 завершённых задач с метриками, модели; `models_view`: активные и все из реестра.
7. Экран `/admin/system`: состояние бэкенда текстом («LinQ доступен, 2 из 2 программ», «LinQ недоступен: туннель или VPN», «Нет программ: …», «Неожиданный ответ Jupyter»), кнопка «Проверить LinQ», очередь и задачи с замерами (кадров, кадр/с, мс на кадр: пре, пост, RTT p50 и p90, загрузка, всего), «Повторить» у упавших, модели. Шапка показывает бейдж бэкенда по `backend.status`.
8. `doctor` для `linq` без фейка вызывает `backend_check(force=True)` и выходит с 4 при состоянии не `ok`.

**Тесты:** `tests/test_backend_check.py`: 1 `test_check_four_states`, 2 `test_check_is_cached` и `test_check_publishes_status`; `tests/test_local_backend.py::test_local_matches_jsonl_format`: 3; `tests/test_jobs_retry.py`: 4 `test_manual_retry`, 5 `test_recover_running_jobs`; `tests/test_system.py`: 6 `test_system_view_metrics`, `test_models_view`; `tests/test_cli.py::test_doctor_reports_missing_keys` дополняется случаем 8; `screens.test.tsx::system_screen_renders`: 7.

**Не делать:** графики замеров, историю проверок LinQ, прямые запросы к RabbitMQ, батч больше 1, загрузку программ TPU.

---

### Слайс 4: трекинг, признаки и HUD

**Файлы:** `src/safewatch/analysis/{__init__,pipeline,tracking,geometry,features,hud}.py`, `src/safewatch/{services,store}.py`, `frontend/src/components/{hud.ts,HudCanvas.tsx,VideoWithHud.tsx}`, `frontend/src/screens/admin/CameraSetup.tsx`, `tests/test_{tracking,features,hud,tracks_api,geometry}.py`, `frontend/src/components/hud.test.ts`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** стадия `analysis` в `run_next_job` (8.1, 8.2 пункты 1–5, 8): трекер, признаки людей, HUD-кадры, строка `analyses`, файл `hud.jsonl`; `video_tracks`; плеер с HUD во вкладке «Видео».

**Критерии приёмки:**
1. Сцена `walk` (10 с) → один трек человека на всю сцену.
2. Сцена `two_walkers_crossing` → два трека, после пересечения id не меняются местами.
3. Человек пропал на 1,1 с (`max_lost_s` 1,0) → новый id; на 0,9 с → прежний.
4. Детекции со `score` 0,1–0,5 продлевают трек, но не открывают; 0,59 не открывает, 0,6 открывает.
5. `class_conf.truck` 0,35: грузовик 0,34 отброшен, 0,35 принят.
6. Скорость 2,0 роста/с на синтетике → `speed_bh_s` в пределах ±5 %; 3 точки в окне → `None`; разрыв 0,6 с в окне → `None`.
7. Ключевые точки прикрепляются при IoU 0,5, не прикрепляются при 0,49.
8. Поза: торс 65° → `lying`, 25° → `upright`, 45° → `unknown`; по рамке: `h/w` 1,2 → `upright`, `w/h` 1,3 → `lying`. H_ref не меняется, пока человек лежит.
9. HUD: координаты в [0, 1]; подписи «бег 2,4 роста/с», «лежит 12 с», «ноги не видны», «слишком мелко» при высоте 39 px и нет подписи при 40 px.
10. Задача проходит стадию `analysis`: `analyses` версии 1, строк в `hud.jsonl` столько же, сколько кадров, у задачи `analysis_id` и `analysis_ms`.
11. `GET /tracks`: окно `[from, to)` отдаёт кадры этого окна; 10000 мс — ок, 10001 → 422; `from ≥ to` → 422; видео без анализа → 409 `video_not_ready`; нет видео → 404.
12. `point_in_polygon` (hypothesis): точка, построенная внутри выпуклого полигона, внутри; точка вне его рамки — снаружи.
13. Фронт: `layoutHud` держит выноски в кадре и при скрытом HUD возвращает пустой список; плеер во вкладке «Видео» с HUD и клавишей H.

**Тесты:** `tests/test_tracking.py`: 1 `test_single_walker_keeps_one_id`, 2 `test_crossing_people_keep_ids`, 3 `test_lost_longer_than_ttl_gets_new_id`, 4 `test_low_score_only_extends_tracks`, 5 `test_class_conf_filters_before_tracking`; `tests/test_features.py`: 6 `test_speed_body_heights_per_second`, 7 `test_pose_attached_by_iou`, 8 `test_posture_from_pose_and_bbox`; `tests/test_hud.py::test_tags_texts_russian_format`: 9; `tests/test_tracks_api.py`: 10 `test_tracks_window_contents`, 11 `test_tracks_window_bounds`; `tests/test_geometry.py::test_point_in_polygon_properties`: 12; `frontend/src/components/hud.test.ts` (`callouts_stay_inside_frame`, `hidden_hud_draws_nothing`) и `screens.test.tsx::camera_setup_player_renders`: 13.

**Не делать:** правила, эпизоды, калибровку, трекинг объектов без класса техники, ReID, рисование HUD на сервере.

---

### Слайс 5: эпизоды, бег и падение

**Файлы:** `src/safewatch/analysis/{episodes,pipeline}.py`, `src/safewatch/rules/{__init__,base,running,fall}.py`, `src/safewatch/{services,store,media}.py`, `frontend/src/components/{Timeline,EvidenceImage}.tsx`, `frontend/src/screens/admin/CameraSetup.tsx`, `tests/test_{episodes,rule_running,rule_fall,analysis_api}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** менеджер эпизодов (8.4), плагины `running` и `fall` (8.3), регистрация в `rules.PLUGINS`, `scenario_metas`, стадия `evidence` (8.2 п. 9), `video_analysis`, `video_recompute` (без `superseded`, это S9), `evidence_file`; таймлайн эпизодов и кнопка «Пересчитать события».

**Критерии приёмки:**
1. Подтверждение: удержание 1,0 с; `P` длится 0,99 с → эпизода нет; 1,0 с → `confirm_ms = start + 1000`.
2. `N` сбрасывает кандидата; разрыв без наблюдений 0,5 с кандидата сохраняет, 0,6 с — сбрасывает.
3. Активный: без наблюдений до 5,0 с — эпизод жив, `uncertain_ms` растёт; 5,1 с → закрыт `track_lost_timeout`, `end_ms` = последний `P`.
4. `N` подряд 2,0 с → закрыт `observed_exit`, `end_ms` = первый `N`; `N` 1,9 с и снова `P` → тот же эпизод.
5. После закрытия новый `P` сразу открывает новый эпизод (нет таймера тишины).
6. Красный `P` у жёлтого эпизода, удержанный `red_hold_s`, → `escalate_ms`, тот же id, `level_max = red`.
7. Смена id: трек 1 пропал, трек 2 появился в 0,9 H_ref от последней точки → тот же эпизод; в 1,1 H_ref → новый; два человека видны одновременно → два эпизода.
8. Конец видео закрывает эпизод с `video_end`.
9. `running`: 1,5 роста/с → `P`, 1,49 → `N`; скорость `None` → `U`; `speed_m_s` в контексте → порог 2,5 м/с; `anchor` в зоне danger или техника ближе `near_vehicle_bh` → красный.
10. `fall`: переход стоя → лёжа через 0,5 с → красный «Зафиксировано падение», подтверждение через 2,0 с; лежит с первого кадра и неподвижен 9,9 с → `N`, 10,0 с → красный «Человек лежит неподвижно 10 с»; в зоне lying_allowed 59,9 с → `N`, 60 с → `P`; стоя → `N`; поза `unknown` → `U`.
11. Сцена `demo` даёт жёлтый эпизод бега и красный эпизод падения; стадия `evidence` пишет JPEG с sha256 файла; `GET /analysis` отдаёт эпизоды с доказательствами; `GET /evidence/{id}/image` → `image/jpeg`, неизвестный → 404; `evidence.jpeg_quality` 30 против 85 меняет размер файла.
12. `POST /recompute` → 202, задача `recompute`, затем версия анализа 2 активна, у фейка нет `start`; видео без артефактов → 409 `artifacts_missing`; не готово → 409 `video_not_ready`; `ohs` — можно, `operator` → 403.
13. `meta.scenarios` содержит `running` и `fall` со статусом `active` и параметрами из конфига; `explain` даёт строки «почему» обоих.
14. Вкладка «Видео»: таймлайн эпизодов цветом и текстом уровня, клик перематывает плеер, миниатюры доказательств, кнопка «Пересчитать события».

**Тесты:** `tests/test_episodes.py`: 1 `test_confirm_after_hold`, 2 `test_negative_resets_candidate`, 3 `test_gap_tolerance_and_lost_timeout`, 4, 5 `test_end_after_negatives_and_rearm`, 6 `test_escalation_keeps_same_episode`, 7 `test_id_switch_merges_but_two_people_do_not`, 8 `test_video_end_closes_episode`; `tests/test_rule_running.py`: 9 `test_running_threshold_boundary`, `test_running_red_in_danger_zone`; `tests/test_rule_fall.py`: 10 `test_fall_transition_red`, `test_lying_still_without_transition`, `test_lying_allowed_zone_threshold`; `tests/test_analysis_api.py`: 11 `test_job_creates_episodes_and_evidence`, `test_evidence_404_and_sha`, 12 `test_recompute_creates_new_version`, 13 `test_meta_lists_running_and_fall`; `screens.test.tsx::camera_setup_timeline_renders`: 14. Мутации: 2.

**Не делать:** события и эфир, остальные сценарии, видеоклипы, рисование рамок на JPEG, пересчёт с `superseded`.

---

### Ревью R5

По разделу 17, охватывает слайсы 1–5. Дополнительно: `gh pr checks` по PR слайсов 1–5; один живой сквозной прогон: видео из `data/videos/` (если капитан положил заводское — его, иначе `synthetic_coco_40x1s.mp4`) через LinQ до эпизодов; итог (кадр/с, эпизоды) в записи ревью.

---

### Слайс 6: эфир, лента и захват экрана оператора

**Файлы:** `src/safewatch/{services,store,texts,worker}.py`, `frontend/src/components/{sound.ts,Toasts.tsx,TakeoverOverlay.tsx,EventFeed.tsx,SectorTile.tsx,AppShell.tsx}`, `frontend/src/screens/operator/{OperatorDashboard,SectorScreen,CameraScreen}.tsx`, `frontend/src/nav.ts`, вкладка «Эфир» в `CameraSetup.tsx`, `tests/test_{broadcast,operator_views,notifications,worker}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** эфир и публикация (8.5), автостарт, состояния камер и секторов (8.9 пункты 1–3, 5), лента (8.8), уведомления с текстами, превью (кадр позиции эфира или первый кадр последнего готового видео, кэш `preview.cache_s`), экраны оператора, всплывашки, звук, захват экрана (в S6 — оверлей на весь экран с текстом и кнопкой «Открыть событие»), циклы `worker`.

**Критерии приёмки:**
1. `confirm_ms = 5000`: тик на позиции 4999 → событий нет; 5000 → одно событие `new` нужного уровня, `started_at = base + start_ms`, действие `published`, WS `event.created` и `notification`.
2. Повторный тик с тем же временем ничего не создаёт; новые синглтоны `services` на той же базе (перезапуск) дублей не дают.
3. Жёлтое событие на `escalate_ms` → тот же id, уровень красный, `red_at`, действие `level_escalated`, WS `event.escalated` и красное уведомление с `takeover=true`, `sound=siren`.
4. На `end_ms`: `ended_at`; жёлтое `new`/`viewed` → `auto_finished`; красное остаётся открытым.
5. Повтор: на `t = D + confirm_ms` второе событие с `cycle=1`; без повтора при `t ≥ D` эфир `ended`, камера `no_observation` («Запись закончилась»), событий больше нет.
6. `broadcast_stop` → `stopped`, тики ничего не публикуют.
7. Автостарт после задачи `process`, если у камеры нет эфира; `broadcast.autostart=false` → эфира нет; играющий эфир не меняется.
8. Старт без готового видео → 409 `no_ready_video`; видео не готово → 409 `video_not_ready`; старт при играющем → прежний `stopped`, новый `playing`; WS `broadcast.state` на старт и стоп; оператор → 403.
9. Состояние камеры по правилам 8.9 (параметризованно: красное > жёлтое > `processing`/`failed`/`ended`/`no_source` > `normal`); сектор: красный, жёлтый, «Нет наблюдения: 1 из 2 камер», пустой сектор — `no_observation`.
10. `camera.state` и `sector.state` публикуются только при изменении.
11. Лента: порядок по `PRIORITY`, затем `published_at` по убыванию; терминальное событие 29,9 мин назад в ленте, 30,1 мин — нет; `superseded` нет; не больше `feed.limit`.
12. Уведомления по таблице 8.8: тексты ровно «Жёлтая опасность · Сектор 5 · Бег 2,4 роста/с» и «Красная опасность · Сектор 7 · Человек лежит неподвижно 15 с»; WS-клиент мастера их не получает.
13. `operator_dashboard_view`, `sector_view`, `camera_live_view` отдают модели 5.2; превью — JPEG, второй запрос в пределах `preview.cache_s` не читает видео; камера без видео → 404.
14. `worker.run_forever` вызывает `broadcast_tick` раз в `broadcast.tick_ms` и `run_next_job` раз в `jobs.idle_poll_ms` при пустой очереди (подменённый `asyncio.sleep` записывает интервалы).
15. Фронт: плитки секторов с состоянием текстом и иконкой, лента, всплывашка на жёлтое со звуком; красное уведомление у оператора открывает оверлей на весь экран со звуком до клика; экран камеры играет эфир синхронно с сервером, с HUD и таймлайном.

**Тесты:** `tests/test_broadcast.py`: 1 `test_publish_at_confirm_time_not_before`, 2 `test_tick_is_idempotent_across_restart`, 3 `test_escalation_updates_same_event`, 4 `test_yellow_auto_finishes_red_stays`, 5 `test_loop_cycle_republishes`, 6 `test_stop_halts_publication`, 7 `test_autostart_after_job`, 8 `test_start_stop_conflicts_and_messages`; `tests/test_operator_views.py`: 9 `test_camera_state_precedence`, 10 `test_state_changes_published`, 11 `test_feed_priority_order`, 13 `test_dashboard_and_sector_view_shape`, `test_camera_live_view_shape`, `test_preview_jpeg`; `tests/test_notifications.py::test_notification_texts_and_sounds`: 12; `tests/test_worker.py::test_loop_periods_from_config`: 14; `screens.test.tsx`: 15 (`operator_dashboard_renders`, `sector_screen_renders`, `camera_screen_renders`, `takeover_on_red_notification`). Мутации: 2.

**Не делать:** действия оператора и экран события (S7), уведомления мастеру, причины `stale`/`dark`/`obstructed` (S11), видеостену из живых плееров на плитках.

---

### Слайс 7: экран события и решения оператора

**Файлы:** `src/safewatch/{services,store,texts,worker}.py`, `frontend/src/screens/events/EventScreen.tsx`, `frontend/src/components/TakeoverOverlay.tsx`, `frontend/src/nav.ts`, `tests/test_{event_actions,escalation,event_detail}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `event_detail` (почему, история, происхождение, разрешённые действия), `event_action` по таблице 8.6, автоэскалация (8.7) и её цикл в `worker`, экран события (8.14) и режим захвата.

**Критерии приёмки:**
1. Все строки таблицы 8.6 с ролью человека (параметризованно): итоговый статус, вердикт и записи журнала в порядке таблицы.
2. Любая другая пара (действие, статус) для оператора и мастера → 409 `invalid_transition`.
3. Мастер не может `confirm` (403), оператор не может `accept` (403); без роли → 400.
4. `resolve`: пустой или из пробелов комментарий → 422 «Опишите принятые меры»; 500 символов — ок, 501 → 422.
5. `X-Actor` (percent-encoded UTF-8) сохраняется в `actor_name`; 60 символов — ок, 61 → 422; без заголовка — `texts.DEMO_ACTOR[role]`.
6. Автоэскалация: `red_at + 44,9 с` → ничего; `+ 45,0 с` → `sent_to_master`, `escalated_by_timeout=1`, действие `timeout_escalated`, уведомление мастеру с « · Не подтверждено оператором»; `escalation.enabled=false` → ничего и через 100 с; `timeout_s = 10` → эскалация на 10,0 с.
7. Действие оператора `confirm`, `false_alarm` или `send_to_master` после `red_at` до срока отменяет эскалацию; один `view` — не отменяет.
8. После эскалации по таймауту: `confirm` оператора → статус прежний, вердикт `confirmed`; `false_alarm` → статус `false_alarm`, WS `event.updated`.
9. `event_detail`: `why` из `explain` плагина, история по времени, `allowed_actions` по роли и статусу, `provenance` (бэкенд, `fake`, модели `id@version`, задача, sha256 видео, версия анализа, параметры правила, sha256 кадра), видео и текущий эфир камеры; демо-событие: `episode=None`, `why` из причины, поля происхождения пустые.
10. Экран события: верх — кадр с HUD и описание с «Почему», историей и кнопками `allowed_actions` (клавиши 1, 2, 3), низ — эфир камеры с HUD; открытие оператором отправляет `view`; красное уведомление открывает `/events/:id?takeover=1` на весь экран с сиреной до действия или «Свернуть».

**Тесты:** `tests/test_event_actions.py`: 1 `test_transition_table`, 2 `test_forbidden_transitions_conflict`, 3 `test_roles_enforced`, 4 `test_resolve_requires_comment`, 5 `test_actor_header_limits`; `tests/test_escalation.py`: 6 `test_timeout_boundary_45s`, `test_flag_off_no_escalation`, `test_timeout_key_changes_behavior`, 7 `test_operator_action_before_deadline_prevents`, 8 `test_operator_decision_after_escalation`; `tests/test_event_detail.py`: 9 `test_detail_why_history_provenance`, `test_demo_event_detail`; `screens.test.tsx::event_screen_renders`: 10. Мутации: 2.

**Не делать:** экраны мастера, массовое подтверждение, редактирование истории, статус «отложено», громкоговоритель.

---

### Слайс 8: мастер смены (мобильный веб)

**Файлы:** `src/safewatch/{services,store}.py`, `frontend/src/screens/master/{MasterInbox,MasterEvent,ShiftSummaryScreen}.tsx`, `frontend/src/nav.ts`, `tests/test_{master,shift,e2e}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `master_inbox_view`, `shift_summary_view`, уведомления мастеру (8.8), экраны мастера одной колонкой, сквозной API-тест демо-истории.

**Критерии приёмки:**
1. Входящие: `active` — `sent_to_master` и `master_accepted`, красные первыми, затем по времени передачи; `recent_resolved` — последние `master.recent_resolved` (из 21 решённого — 20 новых).
2. Уведомление мастеру на `sent_to_master` (оператором и по таймауту), аудитория `master`, `sound=chime`.
3. Смена: в 07:59:59 МСК — ночная (20:00 вчера – 08:00), в 08:00:00 — дневная; сводка считает события с `started_at` в окне: всего, по секторам, по сценариям, список подтверждённых; другой `timezone` сдвигает окно.
4. Сквозной сценарий через API (фейк, сцена `demo`): загрузка → задачи → тики эфира до падения → красное событие → оператор `confirm` → событие во входящих мастера → `accept` → `resolve` с комментарием → история: `published`, `confirmed`, `sent_to_master`, `master_accepted`, `resolved`.
5. Экраны мастера: карточки входящих, карточка события с кадром, местом и причиной, «Принял, иду», «Решено» (кнопка неактивна без комментария), сводка смены; на уведомление — звук и `navigator.vibrate`.

**Тесты:** `tests/test_master.py`: 1 `test_inbox_contains_only_master_statuses`, `test_recent_resolved_limit`, 2 `test_master_notification_on_send_and_timeout`; `tests/test_shift.py`: 3 `test_shift_window_boundaries`, `test_shift_summary_counts`; `tests/test_e2e.py::test_upload_to_master_flow`: 4; `screens.test.tsx`: 5 (`master_inbox_renders`, `master_event_renders`, `shift_summary_renders`).

**Не делать:** нативное приложение, звонки, Telegram, SMS, push через сервис, отправку отчёта мастеру.

---

### Слайс 9: калибровка, зоны, правила камеры и пересчёт

**Файлы:** `src/safewatch/{services,store}.py`, `src/safewatch/analysis/{geometry,features,pipeline}.py`, `frontend/src/components/PolygonEditor.tsx`, `frontend/src/screens/admin/CameraSetup.tsx` (вкладки «Калибровка», «Зоны», «Правила»), `frontend/src/screens/ohs/RulesScreen.tsx`, `frontend/src/nav.ts`, `tests/test_{calibration,zones,camera_rules,recompute}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** калибровка и зоны (8.11), правила камеры (8.3), снимок конфигурации в анализе, метры и м/с в признаках, пересчёт с `superseded` и перезапуском эфира (8.12), экран `/ohs/rules`.

**Критерии приёмки:**
1. Гомография по 4 точкам известной перспективы переводит точки в метры с ошибкой меньше 1e-6; `fit_rmse_m ≈ 0`; с контрольными точками считается `control_rmse_m`; сетка в [0, 1].
2. 3 или 9 точек → 422; 4 и 8 — ок; разное число точек → 422; точка 1,01 → 422; три точки на одной прямой → 422 «Три точки на одной прямой».
3. Калибровка: нет → `null`; `PUT` — только админ; `DELETE` → снова `null`.
4. Зоны: полигон 3 и 32 точки — ок, 2 и 33 → 422; линия 2 точки — ок, 3 → 422; неизвестный тип → 422; имя 60 — ок, 61 → 422; вырожденный полигон → 422; удаление мягкое; `ohs` может, `operator` → 403.
5. Правила: `GET` даёт строку на каждый плагин со значениями по умолчанию без строк в базе; `PUT` переопределяет параметр в диапазоне; неизвестный ключ или вне диапазона → 422; неизвестный сценарий → 404; выключенный сценарий не даёт эпизодов после пересчёта.
6. `rules_screen_view`: сценарии и строка на каждую камеру.
7. Пересчёт: события старой версии в `new` и `auto_finished` → `superseded` с действием и `event.updated`; события с действиями людей не меняются; играющий эфир камеры перезапускается с новым анализом; `config_json` хранит зоны, калибровку и правила момента анализа, поздняя правка зоны его не меняет.
8. С калибровкой: `ground` и `speed_m_s` есть внутри оболочки точек и `None` вне её (метод `relative`); `running` берёт порог в м/с.
9. Фронт: вкладка «Калибровка» (кадр превью, 4–8 точек мышью и поля метров, сетка на оверлее, текст ошибки и «нет контрольных точек»), «Зоны» (рисование полигона и линии по типу, список, удаление), «Правила» (переключатели, параметры с единицами, «Пересчитать события»); экран `/ohs/rules` — матрица камер и сценариев со статусом сценария.

**Тесты:** `tests/test_calibration.py`: 1 `test_homography_maps_points`, 2 `test_calibration_validation`, 8 `test_running_uses_m_s_with_calibration`; `tests/test_zones.py::test_zone_crud_and_geometry_rules`: 4; `tests/test_camera_rules.py`: 5 `test_rule_params_override_and_ranges`, 6 `test_rules_screen_view`; `tests/test_recompute.py`: 7 `test_recompute_supersedes_untouched_events`, `test_config_snapshot_stored`; критерий 3 — в `test_homography_maps_points`; `screens.test.tsx`: 9 (`camera_setup_zones_renders`, `rules_screen_renders`).

**Не делать:** автокалибровку по росту людей, 3D-расстояния до частей тела, матрицу политик телефона по зонам, расширенную сетку с настройками, правку калибровки по видео в реальном времени.

---

### Слайс 10: сценарии на зонах и объектах

**Файлы:** `src/safewatch/rules/{__init__,base,proximity,phone,fence,under,fire,harness,suspended_load,load_carrying}.py`, `src/safewatch/analysis/{features,geometry,pipeline}.py`, `src/safewatch/inference/linq.py`, `tools/linq/remote/video_worker.py` (аргумент `--nc`), `tests/test_{rule_proximity,rule_phone,rule_fence,rule_under,rule_fire,plugin_status}.py`.

**Что делает:** признаки техники, привязка объектов к людям, плагины по таблице 8.3, статусы плагинов от классов активных моделей, модели `pipeline.extra` в конвейере (третий проход воркера с `--nc`, без `--classes`).

**Критерии приёмки:**
1. `proximity`: техника движется, дистанция 0,5 роста → красный, 0,51 → жёлтый, 2,0 → жёлтый, 2,01 → `N`; стоящая техника рядом → `N`; скорость техники `None` → `U`; водитель внутри рамки (доля 0,6) не учитывается; `anchor` в зоне danger → красный; два человека у одной машины → два эпизода.
2. `phone`: 9,99 с → нет эпизода, 10,0 с → жёлтый; в зоне danger 2,99 → нет, 3,0 → красный; человек 119 px → `U` (`too_small`), 120 px → наблюдается; телефон между двумя людьми → `U` (`owner_ambiguous`).
3. `fence_crossing`: переход через линию → один красный эпизод; появление сразу за линией — не пересечение; пересечение прямой вне отрезка не считается; разрыв 1,1 с → `P` с причиной «момент не виден».
4. `restricted_under`: в зоне 0,49 с → нет, 0,5 с → красный.
5. `fire_smoking`: огонь вне fire_allowed → красный; внутри → `N`; сигарета у человека → жёлтый.
6. Статусы: без классов `fire`/`smoke`/`cigarette` у активных моделей `fire_smoking` → `model_missing` с текстом; `no_harness` и `suspended_load` так же; `load_carrying` → `skeleton` с текстом; модель `pipeline.extra` с классами `fire, smoke` в тестовом конфиге включает `fire_smoking` без правки кода, команда воркера для неё содержит `--nc 2` и не содержит `--classes`.
7. `video_worker.py --nc N` использует N классов; без `--nc` поведение прежнее (80 для detect, 1 для pose).

**Тесты:** `tests/test_rule_proximity.py`: 1 `test_moving_vehicle_distance_levels`, `test_stationary_vehicle_negative`, `test_driver_excluded`, `test_danger_zone_entry_red`, `test_two_people_two_episodes`; `tests/test_rule_phone.py`: 2 `test_phone_hold_boundary`, `test_small_person_unknown`; `tests/test_rule_fence.py`: 3 `test_crossing_detected_once`, `test_appearing_inside_is_not_crossing`; `tests/test_rule_under.py::test_under_zone_red_after_hold`: 4; `tests/test_rule_fire.py::test_fire_outside_allowed_zone_red`: 5; `tests/test_plugin_status.py`: 6 `test_status_follows_active_model_classes`, `test_skeletons_listed_with_texts`, `test_extra_model_enables_fire_without_code`, 7 — проверка аргументов воркера в том же файле.

**Не делать:** обучение и подбор моделей огня, привязи, погрузчика; TTC и прогноз траекторий; проекцию груза на HUD; правило переноски груза.

---

### Ревью R10

По разделу 17, охватывает слайсы 6–10. Дополнительно: `gh pr checks` по PR слайсов 6–10; сквозной тест `tests/test_e2e.py::test_upload_to_master_flow` проходит в режиме фейка.

---

### Слайс 11: наблюдаемость и свежесть

**Файлы:** `src/safewatch/analysis/{observability,pipeline,hud}.py`, `src/safewatch/{media,services,store}.py`, `src/safewatch/fakes/scenes.py` (сцена `dark` уже есть), `frontend/src/components/SectorTile.tsx`, `frontend/src/screens/admin/SystemScreen.tsx`, `tests/test_{observability,camera_state}.py`.

**Что делает:** `sample_luma`, `find_gaps` (8.10), причины `stale`/`dark`/`obstructed` в состоянии камеры (8.9 п. 4), `freshness_ms`, свежесть по камерам на экране IT, причина «нет наблюдения» на плитках, «Потеря видимости N с» в «почему».

**Критерии приёмки:**
1. Разрыв между кадрами 2001 мс → интервал `stale`; 2000 мс → нет.
2. Яркость 34 в течение 3,0 с → `dark`; 2,9 с → нет; яркость 35 → нет. Отклонение яркости 11 в течение 3 с → `obstructed`.
3. Камера в интервале на позиции эфира → `no_observation` с причиной и текстом 8.9; вне интервала — по прочим правилам; `freshness_ms` равен позиции минус время последнего кадра анализа.
4. Эпизод через интервал не закрывается раньше `lost_timeout_s`, `uncertain_ms` растёт, `why` содержит «Потеря видимости N с».
5. Плитки секторов и камер показывают причину; экран IT — таблицу свежести по камерам.

**Тесты:** `tests/test_observability.py`: 1 `test_stale_gap_from_missing_frames`, 2 `test_dark_and_obstructed_gaps`, 4 `test_uncertain_time_in_why`; `tests/test_camera_state.py`: 3 `test_all_no_observation_reasons`, `test_freshness_ms`; 5 — проверка текста причины в `screens.test.tsx::operator_dashboard_renders`.

**Не делать:** паспорт пригодности камеры, детектор сдвига камеры, оценку резкости по эталону сцены.

---

### Слайс 12: журнал охраны труда

**Файлы:** `src/safewatch/{services,store}.py`, `frontend/src/components/FiltersBar.tsx`, `frontend/src/screens/ohs/Journal.tsx`, `frontend/src/nav.ts`, `tests/test_{journal,export,e2e}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `events_list` с фильтрами, поиском и курсором, `events_export_csv`, `journal_facets`, экран журнала.

**Критерии приёмки:**
1. Каждый фильтр (уровень, сценарий, статус, сектор, камера, зона, период: `date_from` включительно, `date_to` не включительно) отбирает ровно свои события.
2. Поиск по кириллице без учёта регистра; `%` и `_` в запросе ищутся буквально.
3. Курсор: при `limit=2` страницы покрывают все события без повторов; `total` верен.
4. `include_demo=false` скрывает демо; `superseded` скрыты по умолчанию и видны с `include_superseded=true`.
5. `limit` 0 и 201 → 422, 200 — ок; `q` 101 символ → 422; `date_from > date_to` → 422.
6. `journal_facets` перечисляет сценарии, уровни, статусы, секторы, камеры, зоны с названиями.
7. CSV: `;`, UTF-8 с BOM, колонки: id, опубликовано (МСК), начало, сектор, камера, зона, сценарий, уровень, статус, вердикт, эскалация по таймауту, причина, длительность (с), демо, sha256 кадра, история («время роль: действие; …»); `journal.export_max_rows = 2` даёт 2 строки данных.
8. Событие сквозного сценария S8 находится в журнале по камере и сценарию, его история полная.
9. Экран: фильтры, «Сбросить», «показано X из Y», таблица с миниатюрой кадра, открытие карточки события только для чтения, «Экспорт CSV».

**Тесты:** `tests/test_journal.py`: 1 `test_filters_each_dimension`, 2 `test_search_cyrillic_case_insensitive`, 3 `test_cursor_pagination`, 4 `test_superseded_and_demo_flags`, 5 `test_filter_validation`, 6 `test_facets_lists`; `tests/test_export.py`: 7 `test_csv_columns_and_history`; `tests/test_e2e.py::test_flow_lands_in_journal`: 8; `screens.test.tsx::journal_renders`: 9.

**Не делать:** PDF-отчёты, редактирование событий, удаление событий, полнотекстовый индекс.

---

### Слайс 13: статистика охраны труда и менеджмента

**Файлы:** `src/safewatch/{services,store}.py`, `frontend/src/components/Charts.tsx`, `frontend/src/screens/ohs/OhsStats.tsx`, `frontend/src/screens/management/ManagementDashboard.tsx`, `frontend/src/nav.ts`, `tests/test_{stats_ohs,stats_management}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `ohs_stats_view`, `management_view` по 8.13, два экрана с графиками.

**Критерии приёмки:**
1. На наборе событий с известным распределением счётчики по статусам, сценариям, секторам, камерам верны; `superseded` не учитываются; `include_demo=false` исключает демо.
2. Событие в 20:59 UTC относится к дате и часу 23 МСК, в 21:00 UTC — к следующему дню; ночная смена захватывает события после полуночи.
3. `false_alarm_share` и `review_coverage` верны; при нуле в знаменателе — `None`.
4. Процентили ближайшего ранга: для 5 значений p50 — третье, p95 — пятое; `n` и `pending` верны.
5. Недели с понедельника МСК; `top_sectors` с `per_camera`; текст тренда для уменьшения, роста, без изменений и при `previous = 0` («Недостаточно данных для сравнения»).
6. `weeks` 0 и 53 → 422.
7. Экраны: графики по дням, сценариям, секторам, часам, доля ложных и реакция с n; менеджмент — недели, топ секторов на камеру, текст тренда с оговоркой.

**Тесты:** `tests/test_stats_ohs.py`: 1 `test_counts_by_dimensions`, 2 `test_shift_and_hour_grouping_msk`, 3 `test_false_share_and_coverage`, 4 `test_reaction_percentiles_nearest_rank`; `tests/test_stats_management.py`: 5 `test_weeks_and_top_sectors_per_camera`, `test_yellow_trend_text`, 6 — в том же файле; `screens.test.tsx`: 7 (`ohs_stats_renders`, `management_renders`).

**Не делать:** LTIFR и TRIR, причинные выводы, персональную статистику работников, выгрузку отчётов.

---

### Слайс 14: инструмент оценки качества

**Файлы:** `src/safewatch/{evaluate,services,cli}.py`, `config/eval.example.yaml`, `tests/test_eval.py`.

**Что делает:** `eval_run` и CLI `eval` по 8.18.

**Критерии приёмки:**
1. Схема разметки: `start_s ≥ end_s` или нет поля → exit 2; нет файла разметки или видео → exit 3; бэкенд недоступен (фейк `unavailable`) → exit 4.
2. Сопоставление: задержка ровно `deadline_s` → TP; на 0,001 с больше → `late` и FN; подтверждение ровно в `end_s` → не сопоставлено; второй эпизод того же эталона → `duplicates`; эпизод вне эталонов → FP.
3. Метрики `precision`, `recall`, `f1`, `fp_per_hour`, задержка p50 и p95 с n по сценарию и строка `*`; знаменатель 0 → `None`.
4. Отчёт `report.json` (проходит `EvalReport`) и `report.md` с таблицей и сноской о полноте разметки; второй прогон берёт артефакты из кэша (нет `start` у фейка); `camera_id` подставляет калибровку, зоны и правила камеры.

**Тесты:** `tests/test_eval.py`: 1 `test_labels_schema_errors`, `test_eval_cli_exit_codes`, 2 `test_matching_deadline_boundary`, `test_duplicates_and_false_alarms`, 3 — в тех же тестах, 4 `test_report_files_written`.

**Не делать:** tIoU-метрики, графики, интерфейс разметки, подбор порогов автоматически.

---

### Слайс 15: доставка во внешние системы, Docker, README

**Файлы:** `src/safewatch/{delivery,services,store,worker}.py`, `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `README.md`, `tests/test_delivery.py`.

**Что делает:** `WebhookChannel` и `deliveries_flush` (точка расширения для ламп, сирен, громкоговорителей): тик эфира и действия кладут доставки в очередь, `worker` отправляет их в потоке; каналы в `system_view`, доставки в `event_detail`; Docker; README.

**Критерии приёмки:**
1. Канал из `delivery.webhooks` получает POST JSON `{event_id, kind, level, scenario, title, sector, camera, zone, text, at}` на публикацию красного, эскалацию и передачу мастеру, если уровень есть в `levels` канала.
2. Ответ 200 → строка `sent`; 500 → `failed` с `http_status`; таймаут → `failed` с текстом «таймаут»; событие от этого не меняется.
3. Повторный `deliveries_flush` не шлёт уже отправленное (`UNIQUE`).
4. `system_view.channels` показывает имя, тип, хост без пути и учётных данных, уровни; `event_detail.deliveries` — попытки.
5. Исторический критерий S15: `Dockerfile` (сборка фронта на node, рантайм python:3.12-slim с `uv`, копирует `src`, `config`, `contract`, `tools/linq`, `frontend/dist`) и `docker-compose.yml` (порт 8000, том `data/app`, том `models` только чтение, `env_file: .env`, `LINQ_JUPYTER_URL=http://host.docker.internal:8888`); `docker build` проходит, если демон Docker запущен, иначе строка `долг`. В v10 требования хранения, приоритета URL и обязательной фактической приёмки заменены разделом 8.32; прежняя запись не является инструкцией запуска.
6. README: запуск на Windows и в Docker, мок-режим, переключение бэкенда, куда класть видео, оценка качества (`safewatch eval`), подключение новой модели через `config/models.yaml`.

**Тесты:** `tests/test_delivery.py`: 1 `test_webhook_sent_on_red`, 2 `test_webhook_failure_recorded_event_unaffected`, 3 `test_delivery_idempotent`, 4 `test_channels_in_system_view`; 5 — `docker build` вручную по возможности; 6 — без теста.

**Не делать:** реальные интеграции с лампами и сиренами, звонки, Telegram, хостинг сервиса, HTTPS.

---

### Ревью R15

По разделу 17, охватывает слайсы 11–15. Дополнительно: `gh pr checks` по PR слайсов 11–15; финальный `uv run poe gate`; в `## log` сводка того, что готово к демо и что осталось долгом.

---

### Слайс 16: контракт 1.1.0 первым шагом

Фронт Егора строит экраны новых функций сразу: всё из 6.11 объявляется и публикуется в `contract/openapi.json` до реализации, незакрытые маршруты отвечают 501, как в первую ночь.

**Файлы:** `src/safewatch/migrations/0002_v5.sql`, `src/safewatch/{types,config,api,services,texts}.py`, `config/default.yaml`, `contract/{openapi.json,ws.schema.json,ws-examples.json,openapi.1.0.0.json}`, `frontend/src/api/schema.d.ts`, `tests/test_{db,contract_files,api_skeleton,config,cameras}.py`.

**Что делает:**
1. `contract/openapi.1.0.0.json` — копия текущего `contract/openapi.json` до изменений (снимок для проверки «только растёт»).
2. Миграция `0002_v5.sql` по 6.11.1 целиком.
3. `types.py`: все имена 6.11.2 и поля 6.11.3 (со значениями по умолчанию; `RemoteShell.close` и `InferenceBackend.close` — в S28, не здесь).
4. Конфиг: все ключи 6.11.8 в `config/default.yaml`, модели секций в `config.py` (`extra="forbid"`), `product_name: Argus`.
5. `api.py`: `CONTRACT_VERSION = "1.1.0"`, все маршруты 6.11.6 зовут фасад; `services.py`: все сигнатуры 6.11.4 с `raise NotImplementedError("slice N")`.
6. `safewatch contract` пересобирает `openapi.json` и `ws.schema.json`; `npm run api:gen --prefix frontend` — `schema.d.ts`; примеры `event.*` в `ws-examples.json` получают новые поля.
7. Тесты, которые разбирают `tech.md`, читают и 6.11: `test_types_export_contract_names` — ещё первый блок `python` под `#### 6.11.2`; `test_every_contract_route_is_declared` — ещё таблицу `#### 6.11.6`, всего 65 маршрутов.
8. `progress.md`: в запись слайса и строкой `владелец: передать Егору: контракт 1.1.0 — <маршруты и поля одной строкой>` в `## open`.

**Критерии приёмки:**
1. `migrate()` на базе версии 1 применяет `0002_v5.sql`: новые таблицы и колонки есть, старые строки читаются, у `events` новые поля пустые; повторный вызов ничего не меняет.
2. Все имена 6.11.2 есть в `safewatch.types`; поля 6.11.3 есть у своих типов со значениями по умолчанию; старый JSON `EventSummary` 1.0.0 проходит модель.
3. `GET /api/health` → `{"status":"ok","contract":"1.1.0"}`; `meta.product_name = "Argus"`.
4. Все 10 маршрутов 6.11.6 объявлены и отвечают 501 `not_implemented`; маршрутов всего 65.
5. `safewatch contract --check` → 0; каждый путь, метод и поле схем `openapi.1.0.0.json` есть в новом `openapi.json` (ничего не удалено и не переименовано).
6. Конфиг 6.11.8 загружается; опечатка в новом ключе роняет загрузку.
7. `uv run poe gate` зелёный, фронт собирается с новым `schema.d.ts`.

**Тесты:** `tests/test_db.py::test_migrate_v5_tables_and_columns`: 1; `tests/test_contract_files.py`: 2 `test_types_export_contract_names`, `test_v5_fields_present`, 5 `test_openapi_matches_app`, `test_openapi_only_grows`; `tests/test_api_skeleton.py`: 3 `test_health_ok`, 4 `test_every_contract_route_is_declared`, `test_unbuilt_route_returns_501`; `tests/test_config.py::test_v5_sections_load`: 6; `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` (Argus): 3.

**Не делать:** логику S17+; удаление и переименование чего-либо в контракте; правки фронта кроме `schema.d.ts`.

---

### Слайс 17: демо-пакет и «живой» завод

**Файлы:** `src/safewatch/{demo,services,store,cli,api,texts}.py`, `config/demo.example.yaml`, `data/demo/README.md`, `.gitignore`, `tests/test_{demo_pack,operator_views,jobs}.py`.

**Что делает:** `demo_build`, `demo_import`, `demo_packs`, `artifact_import` (8.19), CLI `demo build` и `demo import`, автозагрузка пакета в `serve --seed`, ключ кэша по `jobs.backend`/`jobs.fake`, лента и состояния без демо-событий сида, `Job.status_text`; сборка настоящего пакета `data/demo/argus` на LinQ из `data/videos/`.

**Критерии приёмки:**
1. `demo build` на фейке без `--allow-fake` → exit 2; с ним — пакет: `manifest.json` проходит `DemoManifest`, видео и артефакты каждой активной модели, `read_jsonl` проходит, `fake=true` в артефактах; непустой `--out` → exit 2; нет видео → 3; фейк `unavailable` → 4, папка `out` не остаётся.
2. `demo import` на пустой базе с сидом: камера пакета привязана к камере сида по названию, новая создана; зоны и калибровка записаны; задача `process` с `backend`/`fake` пакета проходит без команды `start` у фейка (`cached=true`), затем анализ и автостарт эфира.
3. Повторный импорт → `skipped=true`, счётчики таблиц не меняются; `GET /api/demo/packs` — одна строка с `fake` пакета.
4. Пакет с моделью вне реестра или с чужим sha256 видео → exit 2, база не меняется.
5. `serve --seed` при `demo.autoload=true` и существующей `demo.pack` импортирует пакет; `autoload=false` — нет.
6. Лента оператора и состояния камер не содержат событий `is_demo = 1`; журнал с `include_demo=true` их показывает.
7. `Job.status_text` по каждой строке 8.19 (`retry_wait` `linq_unavailable` с временем повтора, `failed` с текстом кода).
8. Сквозной путь от пакета: импорт → тики эфира до красного → `confirm` → мастер `accept`, `resolve` → событие в журнале с клипом-заглушкой `None` до S18.
9. Живая сборка (лимит): `INFERENCE_BACKEND=linq`, без фейка, туннель поднят: `uv run safewatch demo build config/demo.example.yaml --videos data/videos --out data/demo/argus` → пакет с `fake=false`; кадр/с и RTT — в запись слайса. Туннель недоступен или очередь занята Матвеем → пакет на фейке с `--allow-fake` и строка `долг: S17, сборка на LinQ, <причина>`; `владелец: пересобрать data/demo/argus на LinQ одной командой выше`.

**Тесты:** `tests/test_demo_pack.py`: 1 `test_build_writes_manifest_and_artifacts`, `test_build_refuses_fake_without_flag`, 2 `test_import_creates_world_without_inference`, 3 `test_import_is_idempotent`, 4 `test_import_rejects_broken_pack`, 5 `test_serve_autoloads_pack`, 8 `test_demo_flow_reaches_master_and_journal`, `test_cli_build_and_import`, `test_example_layout_is_valid`; `tests/test_operator_views.py::test_feed_skips_seed_demo_events`: 6; `tests/test_jobs.py::test_status_text_for_retry_and_failure`: 7; 9 — вживую, итог в записи.

**Не делать:** выбор итоговых видео и числа камер (решит команда после моделей Матвея); синтетическую историю сида (остаётся); импорт пакета через UI; коммит `data/demo/<name>/`.

---

### Слайс 18: клип события и H.264

**Файлы:** `src/safewatch/{media,services,store}.py`, `pyproject.toml` (`imageio-ffmpeg`), `uv.lock`, `frontend/src/components/ClipPlayer.tsx`, `frontend/src/screens/{events/EventScreen,master/MasterEvent}.tsx`, `tests/test_clips.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `Clip` у событий (8.20), `media.transcode`, `web_path`, отдача H.264-копии, плеер клипа на экране события и у мастера.

**Критерии приёмки:**
1. Окно клипа: эпизод `start 1000`, `confirm 2000` → `[0, 7000]`; `start 10000`, `confirm 11000` → `[7000, 16000]`; конец обрезается длительностью видео и `max_s`; `url` = `/api/videos/<id>/file#t=7.0,16.0`.
2. Демо-событие сида → `clip = None`; событие с эпизодом в ленте, журнале, у мастера и в `EventDetail` несёт тот же `clip`.
3. Загрузка mp4v (`make_video`) → `web_path` есть, `probe_video` копии даёт `avc1`/`h264`, `Video.web_playable = true`, `GET /file` с `Range` → 206 из копии; исходник для инференса и sha256 прежний.
4. `transcode.enabled=false` → копии нет, `web_playable = browser_playable`; ffmpeg падает (подменённый путь) или таймаут → видео принято, `web_path = NULL`, процесса ffmpeg нет.
5. H.264 на входе не перекодируется.
6. Экран события и мастер показывают `ClipPlayer`; `playable=false` → подпись.

**Тесты:** `tests/test_clips.py`: 1 `test_clip_window_bounds`, 2 `test_clip_none_for_seed_demo`, `test_clip_in_feed_journal_detail`, 3 `test_transcode_makes_browser_codec`, `test_video_file_serves_web_copy`, 4 `test_transcode_disabled_key`, `test_transcode_failure_keeps_video`, 5 `test_h264_not_transcoded`; `screens.test.tsx::event_screen_plays_clip`: 6. Тест с настоящим ffmpeg пропускается (`skipif`), если `imageio_ffmpeg.get_ffmpeg_exe()` недоступен.

**Не делать:** нарезку файлов клипов, перекодирование на каждое событие, аудио, поток HLS.

---

### Слайс 19: автокалибровка и м/с

**Файлы:** `src/safewatch/analysis/{autocal,features,pipeline,hud}.py`, `src/safewatch/rules/{running,proximity}.py`, `src/safewatch/{services,store,texts}.py`, `tests/test_autocal.py`.

**Что делает:** `autocal.fit`, `scale_at`, скорость и дистанция в метрах при автокалибровке, `speed_source`, подписи HUD и «почему» (8.21), `analyses.autocal_json`, `Analysis.auto_calibration`, `CameraSetupView.auto_calibration`.

**Критерии приёмки:**
1. Синтетика: 40 стоящих людей на линии `h = 50 + 0,4·y` → `ok`, `a_px` и `b` в пределах 2 %; 30 замеров — `ok`, 29 — `ok=false` с текстом.
2. 20 % выбросов (присевшие `h × 0,6`, обрезанные краем) отбрасываются, линия в пределах 3 %; рамка в 2 px от края не берётся, в 3 px — берётся.
3. Человек 1,7 м идёт 2,9 м/с на синтетике с перспективой → `speed_m_s` в пределах ±20 %, `speed_source = "auto"`; при ручной калибровке — `"calibration"`; без обеих — `None`, `"relative"`.
4. `running` при автокалибровке: 2,5 м/с → `P`, 2,49 → `N`, метод `auto`; без неё — по ростам в секунду, как в v4.
5. HUD: «≈2,9 м/с (авто)», «бег ≈2,9 м/с (авто)», «2,9 м/с (калибровка)», «2,4 роста/с»; `explain` содержит строку источника скорости.
6. `proximity` при автокалибровке считает дистанцию в метрах (пороги `yellow_m`, `red_m`).
7. Анализ пишет `autocal_json`; `GET /analysis` и `camera_setup_view` отдают `auto_calibration`; пересчёт подгоняет заново.

**Тесты:** `tests/test_autocal.py`: 1 `test_fit_recovers_height_line`, `test_too_few_samples_not_ok`, 2 `test_outliers_rejected`, 3 `test_speed_auto_m_s_within_20pct`, `test_manual_calibration_wins`, 4 `test_running_uses_auto_threshold`, 5 `test_hud_labels_auto_and_calibration`, 6 `test_proximity_meters_with_autocal`, 7 `test_analysis_stores_autocal`. Мутации: 2.

**Не делать:** калибровку по технике или разметке пола, 3D-оценку высоты, ручной ввод роста на камеру, правку ручной калибровки по авто.

---

### Слайс 20: каска, респиратор и модели Матвея

**Файлы:** `src/safewatch/rules/{ppe,base,__init__}.py`, `src/safewatch/texts.py`, `config/models.yaml`, `config/user.matvey.example.yaml`, `tests/test_{rule_ppe,config,plugin_status}.py`.

**Что делает:** плагины `no_helmet`, `no_respirator` и `head_objects` (8.22), новый текст `model_missing`, записи моделей Матвея в реестре и пример их включения.

**Критерии приёмки:**
1. `no_helmet`: человек в зоне helmet_required с `no_helmet` у головы 2,99 с → нет эпизода, 3,0 с → жёлтый «Без каски в зоне «…»»; вне зоны → `N`.
2. К голове привязан `helmet` → `N`; к голове ничего → `U` (`head_unseen`); объект ниже `head_frac` рамки не привязан; объект между двумя головами → `U` (`owner_ambiguous`); человек 79 px → `U` (`too_small`), 80 — наблюдается.
3. `no_respirator` — те же строки с `no_respirator`, `respirator` и зоной respirator_required.
4. Без классов у активных моделей оба плагина `model_missing`, текст «Модель не подключена: нужны классы no_helmet» и «… no_respirator»; у прочих плагинов текст тоже новый.
5. `config/models.yaml` содержит обе записи Матвея, `registry.resolve` находит их по `id@version`; с `pipeline.extra: [matvey-helmet-yolov8n@640-v1-5c3af1f3b855]` в тестовом конфиге `no_helmet` → `active`, команда воркера — `--nc 2` без `--classes`; `doctor` без файлов `models/matvey/...` пишет «нет файла».
6. Файлы моделей Матвея есть (`models/matvey/`) → `INFERENCE_BACKEND=local uv run safewatch doctor` и короткий `eval` на `data/videos/synthetic_coco_40x1s.mp4`, итог в запись слайса; нет — «не проверено: файлов нет».

**Тесты:** `tests/test_rule_ppe.py`: 1 `test_no_helmet_in_zone_yellow_after_hold`, `test_outside_zone_no_event`, 2 `test_helmet_seen_is_negative`, `test_head_unseen_unknown`, `test_ambiguous_and_small`, 3 `test_respirator_rows`, 4 `test_respirator_model_missing_text`, 5 `test_helmet_model_activates_plugin`; `tests/test_config.py::test_matvey_models_resolve`: 5; 6 — вручную при наличии файлов. Мутации: 2.

**Не делать:** обучение моделей СИЗ, жилет, позитивный вывод «каски нет» без класса `no_helmet`, переключение `pipeline` в `default.yaml`, загрузку программ на LinQ.

---

### Ревью R20

По разделу 17, охватывает слайсы 16–20. Дополнительно: `gh pr checks` по PR слайсов 16–20; `test_openapi_only_grows` зелёный; Егору в `## open` уже есть строка про контракт 1.1.0.

---

### Слайс 21: Docker одной командой

**Файлы:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `docs/DEPLOY.md`, `README.md`, `tests/test_docker_files.py`.

**Что делает:** образ собирается и стартует с сидом и демо-пакетом (8.32), инструкция развёртывания на другой машине.

**Критерии приёмки:**
1. Статически: compose монтирует `./data/app`, `./data/demo:ro`, `./models:ro`, порт 8000, `healthcheck` на `/api/health`; Dockerfile стартует `serve ... --seed`; `.dockerignore` не исключает `data/demo/README.md`, но исключает `data/`, `.env*`, `models/`.
2. `docker info` отвечает: `docker compose up -d --build` → `GET http://127.0.0.1:8000/api/health` 200 за 120 с; `GET /api/demo/packs` не пуст, если пакет есть; `docker compose down`. Не отвечает → строка `долг: S21, docker build, Docker Desktop не запущен` и `владелец: запустить Docker Desktop, затем docker compose up -d --build`.
3. `docs/DEPLOY.md` по 8.32; README ссылается на него.

**Тесты:** `tests/test_docker_files.py`: 1 `test_compose_mounts_demo_and_data`, `test_image_starts_with_seed_and_health`; 2 — вручную, итог в записи; 3 — без теста.

**Не делать:** публикацию образа в реестр, HTTPS, обратный прокси, настройку сервиса Феди.

---

### Слайс 22: телефон по зонам и проекция груза

**Файлы:** `src/safewatch/rules/phone.py`, `src/safewatch/analysis/hud.py`, `src/safewatch/texts.py`, `config/default.yaml` (описание `rest`), `tests/test_{rule_phone,hud}.py`.

**Что делает:** телефон в `walkway`/`rest` разрешён, в рабочей зоне жёлтый, в danger красный (8.23); полигон проекции груза в HUD.

**Критерии приёмки:**
1. Телефон в руках в зоне walkway 20 с → `N`, эпизода нет; в зоне rest — то же; на границе зоны (`anchor` внутри) — разрешено.
2. Вне зон 9,99 с → нет, 10,0 с → жёлтый; в danger 3,0 с → красный (v4 сохранён).
3. `meta.scenarios` телефона перечисляет зоны `danger`, `vehicle_path`, `walkway`, `rest`.
4. Объект `suspended_load` в HUD несёт `projection` `[(x1, y2), (x2, y2), (x2, 1), (x1, 1)]` в нормированных координатах и тег `load_projection`; человек внутри полигона даёт красный по правилу `suspended_load`.

**Тесты:** `tests/test_rule_phone.py`: 1 `test_phone_allowed_in_walkway_and_rest`, 2 `test_phone_in_work_zone_yellow`, 3 — в том же файле; `tests/test_hud.py::test_suspended_load_projection`: 4.

**Не делать:** классификатор «телефон в руках» по позе, разговор и фото как разные нарушения, 3D-проекцию груза.

---

### Слайс 23: звонок мастеру, очередь доставок, оператор с телефона

**Файлы:** `src/safewatch/{delivery,services,store,config,texts,worker}.py`, `frontend/src/screens/operator/{OperatorMobile,OperatorMobileEvent}.tsx`, `frontend/src/screens/master/MasterInbox.tsx`, `frontend/src/nav.ts`, `tests/test_{delivery,worker}.py`, `frontend/src/screens/screens.test.tsx`.

**Что делает:** `CallChannel` (заглушка), очередь `delivery_queue` вместо памяти, уровень на момент постановки, уникальные имена каналов, `Delivery.delivered_at`/`status_text`, экраны оператора с телефона, мастер открывает карточку на уведомление (8.24).

**Критерии приёмки:**
1. Оператор `confirm` красного → `to_master` в очереди → канал `call:master` пишет `sent` с `delivered_at`, `status_text` «Звонок доставлен (заглушка)»; то же при автоэскалации; жёлтое `send_to_master` при `levels: [red]` → звонка нет; публикация (`published`) звонок не даёт.
2. Webhook получает доставки по-прежнему (тесты S15 зелёные без правки смысла).
3. Перезапуск (новые синглтоны на той же базе) после постановки и до `deliveries_flush` → доставка уходит; повторный flush ничего не шлёт.
4. Жёлтое, эскалированное до красного между постановкой и flush, уходит `published` с уровнем `yellow` (уровень строки очереди).
5. Два канала с одним `name` (webhook и call) → конфиг не загружается с текстом.
6. `system_view.channels` показывает канал звонка `kind="call"`, номер с маской; `event_detail.deliveries` — строку звонка.
7. Фронт: `/m/operator` — лента одной колонкой, тап открывает карточку с кнопками `allowed_actions`; мастер на уведомление `to_master` открывает `/master/events/:id`.

**Тесты:** `tests/test_delivery.py`: 1 `test_call_stub_on_red_to_master`, `test_yellow_send_no_call`, 2 (существующие), 3 `test_queue_survives_restart`, 4 `test_level_fixed_at_enqueue`, 5 `test_duplicate_channel_names_rejected`, 6 `test_call_channel_in_system_view`; `tests/test_worker.py::test_loop_periods_from_config` (без изменений числа задач, если `datasets` ещё нет); `screens.test.tsx`: 7 `operator_mobile_renders`, `operator_mobile_event_renders`, `master_opens_card_on_notification`. Мутации: 2.

**Не делать:** реальную телефонию, SMS, Telegram, push-сервис, громкоговоритель, повтор неудачной доставки.

---

### Слайс 24: калькулятор окупаемости и масштабирования

**Файлы:** `src/safewatch/{calculator,services,store,texts}.py`, `tests/test_calculator.py`.

**Что делает:** `calculator_defaults`, `calculator_rollout`, `calculator_scale` по 8.25, маршруты 6.11.6. Экран делает Егор.

**Критерии приёмки:**
1. Пример `calculator_defaults` (8 камер, `fps` 12): `accelerators = ceil(8 × 12 × 2 / 12,4) = ceil(15,48) = 16`, `servers = ceil(16 / 4) = 4`; три уровня с `capex`, `opex_year`, `savings_year`, `payback_months` ровно по формулам 8.25 (каждая строка формулы — свой assert).
2. `savings_year ≤ opex_year` → `payback_months = None` и строка «Не окупается при этих допущениях»; на шаг выше — число.
3. `overrides` меняет результат (`accelerator.price_rub` 0 → `capex` меньше на `accelerators × цену`); неизвестный ключ → 422; отрицательное значение или `cameras = 0` → 422.
4. Масштабирование: без замеров `capacity_fps = 12,4` с источником из конфига; с двумя артефактами `linq`, `fake=0` (`throughput_fps` 10 и 14) — медиана 12 и подпись «замер приложения: 2 задачи»; `capex` только на добавленную часть.
5. Роли: `rollout` — только management (admin → 403), `scale` — management и admin (ohs → 403), без роли → 400; `defaults` без роли.
6. `defaults` перечисляет каждое допущение с непустым `source`; `measured` — с `editable=false`; `events_per_operator_shift` считается по событиям эфира и `None` без них.

**Тесты:** `tests/test_calculator.py`: 1 `test_rollout_three_tiers_formulas`, 2 `test_payback_none_when_not_profitable`, 3 `test_overrides_and_unknown_key`, 4 `test_scale_accelerators_from_measured`, 5 `test_roles`, 6 `test_defaults_list_sources`. Мутации: 2.

**Не делать:** экран калькулятора, сохранение расчётов, валюты кроме ₽, «факты» без подписи источника.

---

### Слайс 25: ложное срабатывание → датасет

**Файлы:** `src/safewatch/{dataset,services,store,worker,cli,api}.py`, `tests/test_{dataset,worker}.py`.

**Что делает:** `datasets_flush` в `worker`, `datasets_view`, `dataset_export`, CLI `dataset export`, маршруты 6.11.6 (8.26).

**Критерии приёмки:**
1. `false_alarm` оператора по событию эфира → после тика один элемент `dataset_items`; повторный тик не создаёт второй; демо-событие сида → нет элемента.
2. Папка элемента: `frames/` (не больше `max_frames`; `max_frames = 3` в тесте → 3 кадра), `detections.jsonl` (строки проходят `FrameDetections`, `frame_idx` из окна клипа), `hud.jsonl`, `label.json` с полями 8.26 и комментарием оператора.
3. `GET /api/datasets/false-alarms` → `DatasetView` с `total` и суммой кадров.
4. Экспорт zip содержит `manifest.json` и файлы каждого элемента; CLI `dataset export --out DIR` → 0 и путь.
5. Ошибка чтения кадра → лог, элемента нет, следующий тик повторяет.
6. `worker.run_forever` запускает пятую задачу с периодом `datasets.tick_ms`.

**Тесты:** `tests/test_dataset.py`: 1 `test_false_alarm_creates_item_once`, `test_demo_event_no_item`, 2 `test_item_files_and_label`, 3 — в первом тесте, 4 `test_export_zip_manifest`, `test_cli_export`, 5 `test_frame_error_retries`; `tests/test_worker.py::test_loop_periods_from_config`: 6.

**Не делать:** разметку в UI, автодообучение, отправку датасета куда-либо, позитивные примеры.

---

### Ревью R25

По разделу 17, охватывает слайсы 21–25. Дополнительно: `gh pr checks` по PR слайсов 21–25; сквозной тест демо-пакета зелёный; если Docker Desktop запущен — `docker compose up -d --build` и health.

---

### Слайс 26: ручная идентификация нарушителя

**Файлы:** `src/safewatch/{services,store,texts,api}.py`, `tests/test_{identity,export}.py`.

**Что делает:** `event_identify`, `people_stats_view`, поля идентификации в `EventSummary`, `can_identify`, колонки CSV (8.27).

**Критерии приёмки:**
1. `PATCH /identity` ролью ohs: поля записаны с обрезкой, строка `identified` с комментарием, статус события прежний, WS `event.updated`; повтор тех же значений → 200 без новой строки; пустые строки очищают с комментарием «Идентификация очищена».
2. Роли: management — можно, operator → 403, без роли → 400; `can_identify` по роли.
3. 80 символов — ок, 81 → 422; несуществующее событие → 404.
4. `GET /api/stats/people`: только заполненные; `identified` и строки по людям и бригадам верны; `date_from > date_to` → 422.
5. CSV журнала: колонки «ФИО», «Должность», «Бригада» в конце.

**Тесты:** `tests/test_identity.py`: 1 `test_identify_writes_fields_and_history`, 2 `test_identify_roles`, 3 `test_identify_limits`, 4 `test_people_stats_only_filled`; `tests/test_export.py::test_csv_has_identity_columns`: 5.

**Не делать:** автоматическое распознавание, справочник работников, фото лица, экран (делает Егор).

---

### Слайс 27: паспорт пригодности камеры

**Файлы:** `src/safewatch/analysis/passport.py`, `src/safewatch/{services,store,texts,api}.py`, `tests/test_passport.py`.

**Что делает:** `build_passport`, `camera_passport`, маршрут 6.11.6 (8.28).

**Критерии приёмки:**
1. Каждая строка порядка вердиктов 8.28 (параметризованно): медиана роста 39 px → `unsuitable` для сценариев на людях, 79 → `partial`, 80 → `suitable`.
2. `dark_share` 0,21 → `partial`, 0,51 → `unsuitable`; 0,2 → нет.
3. Плагин `model_missing` → `unknown` «Модель не подключена»; камера без готового видео → все `unknown`; `frames < min_frames` → `unknown`.
4. `fence_crossing` без зоны fence → `partial` «Нет зон: Ограждение»; телефон с медианой объекта 11 px → `partial`.
5. Неизвестная или удалённая камера → 404.

**Тесты:** `tests/test_passport.py`: 1 `test_verdicts_by_person_height`, 2 `test_dark_share_partial`, 3 `test_model_missing_unknown`, `test_no_analysis_unknown`, 4 `test_zone_missing_partial`, 5 — в `test_no_analysis_unknown`.

**Не делать:** оценку точности моделей по камере, рекомендации по установке камеры, хранение паспортов.

---

### Слайс 28: LinQ под медленную очередь

**Файлы:** `src/safewatch/inference/{linq,local}.py`, `src/safewatch/fakes/remote.py`, `src/safewatch/{types,services,api,doctor,texts}.py`, `tools/linq/remote/video_worker.py` (аргумент `--reply-timeout`), `tests/test_{linq_backend,backend_check,jobs}.py`, `tests/live/test_linq_live.py`.

**Что делает:** таймауты от медленного RTT, `--reply-timeout`, `rate_fps`, `eta_s`, текст прогресса, гашение прежнего воркера, `close()` для kernel, HTML → `bad_answer` (8.29); короткая живая проверка.

**Критерии приёмки:**
1. Таймаут прогона: 720 кадров, `inflight 4`, `slow_rtt_s 12` → 2280 с; 10 кадров → `job_timeout_s` (1800); другое `slow_rtt_s` меняет итог.
2. Команда старта содержит `--reply-timeout 120` и гашение прежнего pid до запуска; `video_worker.py --reply-timeout N` передаёт N в `collect`, без аргумента — 120.
3. Прогресс фейка `done` 120 из 720 за 40 с → `rate_fps = 3,0`, `eta_s = 200`, текст «LinQ: 120 из 720 кадров · 3,0 кадр/с · осталось ~3 мин»; `done = 0` → «ждём первый ответ TPU».
4. `close()`: `JupyterShell` вызывает `shutdown_kernel` один раз, повтор без ошибки; lifespan и `doctor` зовут `backend_close`; у фейка маркер `close`.
5. `JupyterError` с HTML → `bad_output`, `backend_check` → `bad_answer`.
6. Живая проверка (лимит): ролик до 60 с через LinQ, итог в записи; недоступно → `долг`.

**Тесты:** `tests/test_linq_backend.py`: 1 `test_job_timeout_scales_with_frames`, 2 `test_reply_timeout_passed`, `test_start_kills_previous_worker`, 3 `test_eta_and_rate_text`, 4 `test_close_shuts_kernel`, 5 `test_html_answer_is_bad_answer`; `tests/live/test_linq_live.py::test_linq_processes_short_clip`: 6.

**Не делать:** прямые запросы к RabbitMQ, параллельные задачи на TPU, `--inflight` больше 4, загрузку программ, правки `tools/linq/` кроме аргумента воркера.

---

### Слайс 29: пробелы `docs/ML_INTEGRATION.md`

**Файлы:** `src/safewatch/inference/{linq,local}.py`, `src/safewatch/analysis/pipeline.py`, `src/safewatch/rules/{__init__,proximity}.py`, `src/safewatch/{services,cli,registry}.py`, `docs/ML_INTEGRATION.md` (раздел 9: итог у каждого пункта), `tests/test_ml_gaps.py`.

**Что делает:** пункты 1, 2, 3, 4, 7, 8, 10, 11, 14 таблицы 8.30; итог по всем 19 пунктам в документе.

**Критерии приёмки:**
1. `import-artifact FILE --video ID --model REF --backend local` → строка `artifacts`; следующая задача того же видео на `local` берёт её из кэша; плохой JSONL → exit 2; нет видео → 3.
2. Детектор с `nc: 2` → `--nc 2`, `--classes` в пределах `0..1`; без `nc` — как в v4.
3. `input_name: input0` → `--input-name input0`; по умолчанию аргумента нет (воркер берёт `images`).
4. `linq_tail: null` → команда без `--tail`, `model_missing` не возникает.
5. `pipeline.vehicle_classes: [truck, forklift]` и extra-модель с классом `forklift` → техника с трекингом, `proximity` видит её; `proximity` `active` при `person` и одном классе техники.
6. Extra-модель отвечает `remote_error` → задача `done`, `error_text` начинается с `extra `, её сценарий в этом анализе `model_missing`; `bad_output` — так же.
7. `Job.metrics` содержит метрики extra-модели.
8. `local.providers: [CUDAExecutionProvider, CPUExecutionProvider]` передаётся в onnxruntime (подменённая сессия).
9. В `docs/ML_INTEGRATION.md` у каждого из 19 пунктов строка итога из 8.30.

**Тесты:** `tests/test_ml_gaps.py`: 1 `test_import_artifact_cli_and_cache`, 2 `test_detector_nc_passed`, 3 `test_input_name_passed`, 4 `test_tail_optional`, 5 `test_vehicle_classes_from_config`, `test_proximity_any_vehicle`, 6 `test_extra_failure_falls_back`, 7 `test_extra_metrics_in_job`, 8 `test_local_providers_key`; 9 — вручную.

**Не делать:** пункты «оставлено» таблицы 8.30, смену `CACHE_SCHEMA`, правки `upload_program.py` и `compile_yolo.py`.

---

### Слайс 30: отчёт смены в PDF и долги приложения

**Файлы:** `src/safewatch/{report_pdf,services,api,cli}.py`, `src/safewatch/assets/fonts/DejaVuSans.ttf`, `pyproject.toml` (`fpdf2`), `uv.lock`, `.gitattributes`, `src/safewatch/analysis/tracking.py`, `src/safewatch/rules/{proximity,phone,fence,under,fire,harness,suspended_load}.py` (`explain`), `tests/test_{shift_pdf,tracking,videos,eval,rule_proximity}.py`.

**Что делает:** PDF сводки смены и долги таблицы 8.31.

**Критерии приёмки:**
1. `GET /api/master/shift.pdf` → `application/pdf`, файл начинается с `%PDF`, текст страницы (извлечённый `fpdf2`/`pypdf` в тесте, если есть, иначе поиск подстроки в несжатом потоке) содержит «Сводка смены» и название сектора по-русски; `at=мусор` → 422.
2. Сцена `demo`: один id трека через падение, эпизод падения подтверждён веткой перехода («Зафиксировано падение»); `reattach_bh = 0` возвращает прежнее поведение.
3. Загрузка без `X-Role` или с `Content-Length` больше лимита → 400 / 413, во временной папке ничего не появилось.
4. `eval` при живом процессе `server.pid` → exit 5 с текстом; pose `remote_error` в `eval` → отчёт без точек.
5. `explain` каждого плагина S10 содержит правило с порогом и единицей.

**Тесты:** `tests/test_shift_pdf.py`: 1 `test_pdf_has_cyrillic_summary`, `test_pdf_route_and_bad_at`; `tests/test_tracking.py::test_fall_keeps_track_id`: 2; `tests/test_videos.py::test_upload_rejected_before_body`: 3; `tests/test_eval.py`: 4 `test_eval_refuses_running_server`, `test_eval_pose_fallback`; `tests/test_rule_proximity.py::test_explain_has_units`: 5.

**Не делать:** PDF журнала и статистики, отправку отчёта мастеру, оформление PDF сверх таблиц.

---

### Ревью R30

По разделу 17, охватывает слайсы 26–30. Дополнительно: `gh pr checks` по PR слайсов 26–30; каждая строка `долг:` из `## open` закрыта или перенесена с причиной по 8.31; есть заводские видео в `data/videos/` → регрессия: импорт, анализ, эпизоды без падений задачи, итог в записи.

---

### Слайс 31: 1–2 новых сценария из ресёрча (снят владельцем, v8)

**Файлы:** `src/safewatch/rules/<id>.py`, `src/safewatch/rules/__init__.py`, `src/safewatch/texts.py`, `config/default.yaml` (секция `scenarios.<id>`), `tests/test_rule_<id>.py`.

**Что делает:** нет `docs/research/EXTRA_SCENARIOS_*.md` в `main` → запись слайса «файла нет, сценариев нет», без кода, слайс закрыт. Есть → 1–2 сценария, которые делаются на существующих сигналах (поза, трек, зоны, время): плагин по образцу `rules/fall.py`, строка таблицы 8.3 в записи слайса, имена — строками `GAP` (контракт сценария: `id`, классы, зоны, параметры, тексты). Сценарию нужна новая модель → плагин с понятным классом и статусом `model_missing`.

**Критерии приёмки:**
1. Каждое число сценария — тест на границе, каждая строка P/N/U — тест (10.1, ядро).
2. `meta.scenarios` перечисляет сценарий с параметрами из конфига; `explain` даёт «почему».
3. Строки `GAP` в `## open` для каждого нового имени.

**Тесты:** `tests/test_rule_<id>.py` по критериям.

**Не делать:** сценарии, которым нужна новая модель с логикой (только заглушка `model_missing`), больше двух сценариев.

---

### Слайс 32: сдвиг камеры (снят владельцем, v8)

**Файлы:** `src/safewatch/{media,services}.py`, `src/safewatch/analysis/passport.py`, `tests/test_camera_shift.py`.

**Что делает:** эталон кадра при калибровке и зонах, `media.frame_shift`, `shift_px` и `shift_text` в паспорте (8.33).

**Критерии приёмки:**
1. Кадр, сдвинутый на 25 px (`max_px` 20), → `shift_text` «Камера сдвинута на 25 px…»; на 15 px → пусто; без эталона → `shift_px = None`.
2. `calibration_set` и `zone_create` сохраняют эталон.

**Тесты:** `tests/test_camera_shift.py::test_shift_detected_above_threshold`: 1, `test_reference_saved_on_calibration`: 2.

**Не делать:** автоматический перенос зон, детектор вибрации, новую модель.

---

### Ревью R32

По разделу 17, охватывает весь второй прогон (v8: S31 и S32 сняты, нового кода после R30 нет). Дополнительно: `gh pr checks` по PR после R30; финальный `uv run poe gate`; короткая живая проверка LinQ (лимит); `test_openapi_only_grows` зелёный; в `## log` сводка: что готово к демо (по разделу 4 `UPGRADE_v1.md`), что осталось долгом, что владельцу сделать утром (Docker Desktop, пересборка демо-пакета на LinQ, файлы моделей Матвея, фронт Егора).

---

## 17. Ревью R<K>

Отдельным заходом после последнего слайса стадии и зелёного гейта. Охватывает все слайсы с прошлого ревью. Задача: искать проблемы, а не хвалить написанное. Если установлен skill `engineering:code-review`, следуй ему.

Чек-лист:
1. Выдуманных типов нет, всё из разделов 5–6 и строк `GAP`.
2. Вывод сверки контракта (`uv run poe contract`) чистый, `uv run poe api` чистый. Строки `GAP` сверены с кодом.
3. Слои: SQL только в `store.py` и `db.py`; `api.py`, `cli.py`, `worker.py` зовут только `services`; `analysis/` и `rules/` без базы, сети и `clock`; в базу пишет только поток event loop; фронт ходит в сеть только через `src/api/`.
4. Внешние вызовы только через `RemoteShell` и каналы доставки; правила LinQ из 3.1 соблюдены (папка `baseline/`, чужое не трогается).
5. Запросов к базе в цикле нет.
6. Тесты проверяют критерии, а не реализацию; правила разделов 10 и 10.1 соблюдены; тесты не ходят в сеть, не читают `.env` и `config/user.yaml`.
7. Конкурентность: при исключении одной задачи остальные дожидаются; блокирующая работа в `to_thread` не пишет в базу.
8. Мёртвого кода нет (можно `uvx vulture src`).
9. Файлов и абстракций сверх раздела 4 нет.
10. Обработки ошибок, которых не бывает, нет.
11. Файлы приложения в LF: `uv run poe eol`.
12. Пункты **[проверить]** сверены и записаны в `progress.md`.
13. Долги (`долг:`) и заметки `R<K>:` из `## open`: закрыты или перенесены с причиной.
14. CI шагов стадии проверен `gh pr checks`; красный чинится в этом же заходе.
15. v5: контракт фронта только растёт: `test_openapi_only_grows` зелёный, ни один путь и поле `contract/openapi.1.0.0.json` не пропали.
16. v5: демо-путь цел: `tests/test_e2e.py` и `tests/test_demo_pack.py::test_demo_flow_reaches_master_and_journal` зелёные.
17. v5: правила LinQ второго прогона (3.1, 10.3): живых прогонов не больше лимита, программы `mosprom_*` и `mosprom_matvey_*` не тронуты, ветка `matvey_cv` не менялась.

Находки правятся в том же заходе веткой `review-r<K>`, PR `review: R<K>`, потом гейт заново. Затем все строки `GAP` переносятся в `tech.md` отдельным коммитом `docs(tech): vN` (раздел 14). Запись в `## log`: `### R<K>: ...`, что найдено и исправлено, что оставлено и почему.

---

## 18. Журнал прогресса

Файл `progress.md` в корне. Содержит только то, чего нет в git log и в `tech.md`: состояние слайсов, отклонения от плана, строки `GAP`, долги и long-lead. Пересказ сделанного и список файлов не пишутся.

Структура:
- шапка (изменяемая): `state`, версия `tech.md`, базовая ветка, remote, дата;
- `## open` (изменяемый): строки `GAP`, `долг`, заметки для ревью, long-lead, действия владельца;
- `## log` (append-only): записи не редактируются и не удаляются;
- `## night` (append-only): журнал ночи. Пишет только оркестратор `/night-shift`, сессии слайсов и ревью его не трогают.

Строки `## open`:
- `GAP: <слайс>, <что>, <точная форма>` или `GAP: <слайс>, <что>, <было> → <стало>` (раздел 14);
- `долг: <слайс>, <критерий>, <что не так>`;
- заметка для будущего ревью: `R<K>: <что>`. Чужие записи `## log` не трогать;
- действие владельца: `владелец: <что сделать>`;
- long-lead: `long-lead: <что>, <срок или условие>`. Списка ключей не держать: их состояние показывает `safewatch doctor`. Только ключ, который владелец обещал добавить, с датой.

События:
- слайс начат: шапка, коммит `docs(progress): start slice N`;
- слайс закрыт: запись в `## log` и шапка, коммит `docs(progress): close slice N`;
- GAP поднят: строка в `## open`; перенесён ревью в `tech.md`: строка убрана, версия в шапке обновлена;
- long-lead или долг закрыт: строка убрана, в записи слайса или ревью сказано, где закрыт;
- слайс откачен: новая запись `### S<N> откат: <причина>` в `## log` со ссылкой на старую.

Запись закрытого слайса, до десяти строк. Заголовок читает сверка контракта, формат не менять:
```
### S<N>: <name> (YYYY-MM-DD, PR #K | local, tech vX)
- отклонения: <что и почему> | отклонений нет
- решения вне контракта: <что должна знать следующая сессия> | нет
- проверено вживую: <сервисы> | не проверено: <сервисы без ключей>
- [проверить]: <пункт: итог> | нет
- следующему: <появившиеся скрипты, фикстуры, хелперы> | нет
```

Строка `## night`: `- HH:MM <шаг>: ок | ок со второй попытки (<причина>) | закрыт с долгом (<что>), PR #K[, #M]`.
