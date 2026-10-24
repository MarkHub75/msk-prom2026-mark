# tech.md: SafeWatch (msk-prom2026-mark)

## 0. Версия

**Версия: v3** (2026-10-24)

Changelog:
- v1: первая версия. Заморожены: разделы 5 и 6 (схема БД, типы, фасад, CLI, REST, WebSocket, конфиг, трассировка) и контракт фронтенда `contract/openapi.json` версии 1.0.0.
- v2 (ревью R5): 44 строки `GAP` S0–S5 перенесены в 6.8 и строки трассировки 6.7; 8.1: `model_missing` только по `not readable`; 8.2: жёлтая скорость при `≥` порога; 7: `registry.resolve(ref, models=None)`, `HudCanvas({ops, size})`; решения R5: `PUT` сектора, `PATCH` камеры, doctor без ключей, импорты `api.py`, устойчивость цикла задач и сессии Jupyter, диагностика очереди TPU.
- v3 (ревью R10): 37 строк `GAP` S6–S10 перенесены в 6.9, 3 строки трассировки 6.7; решения R10: `AnalysisConfig.extra_artifact_ids` (пересчёт с моделями `pipeline.extra` без изменения схемы), параметры правил из `CameraRule.effective` снимка, длина `X-Actor` проверяется только в `services`, ссылка на настройку камеры из списка, autouse-защита `data/app` в `tests/conftest.py`.

Правило версий: любое изменение контракта (разделы 5–6), состава слайсов (16) или правил (10–18) поднимает версию и добавляет строку в changelog. Правку коммитит в `main` владелец или ревью, которое переносит строки `GAP` (раздел 14), коммитом `docs(tech): vN <что>`. Сессия сверяет версию в шапке `progress.md` с этой; расхождение: прочитай changelog от своей версии и обнови шапку.

---

## 1. Как читать этот файл

- Это источник истины проекта. Читай его перед каждой задачей и подчиняйся дословно.
- `docs/brief.md` объясняет, зачем строится проект. При расхождении прав этот файл. Факты о LinQ берутся из `docs/linq/LINQ_CONTRACT.md`: он главнее и брифа, и этого файла; расхождение с ним оформляй строкой `GAP`.
- Имена таблиц, полей, типов, функций, маршрутов и ключей конфига берутся отсюда и из строк `GAP` в `## open` файла `progress.md`. Свои варианты молча не придумывай.
- Нужного контракта нет: `CONTRACT GAP` (раздел 14), работа не останавливается.
- Файл меняет владелец или ревью, переносящее строки `GAP`. Сессия слайса его не редактирует.
- Один слайс за заход. Очередь в разделе 16, иди сверху вниз.
- Пометка **[проверить]**: перед кодом сверься с актуальной документацией сервиса или библиотеки и запиши итог одной строкой в запись слайса в `progress.md`.

---

## 2. Проект

SafeWatch: веб-сервис видеоконтроля промышленной безопасности для кейса «Открой#Моспром 2026» (ООО «ХайТэк», ускорители LinQ). Сервис принимает видео камер, один раз прогоняет нейросети на LinQ TPU, превращает детекции в эпизоды нарушений, оповещает оператора и мастера без дублей, ведёт неизменяемый журнал с доказательными кадрами и считает статистику.

Пользователи: оператор/диспетчер (главный герой, лента событий), мастер смены (телефон), специалист по охране труда (журнал, правила, статистика), менеджмент (тренды), IT/администратор (камеры, калибровка, зоны, замеры LinQ). Работник у станка интерфейсом не пользуется.

Режим работы: «анализ видеоархива / эмуляция потока». Видео загружается в сервис, обрабатывается внутри LinQ Jupyter (стримить кадры на LinQ запрещено), результат детекций кэшируется. «Эфир» камеры воспроизводит запись по серверным часам; событие публикуется, когда воспроизведение доходит до момента его подтверждения. Так красный захват экрана, автоэскалация и уведомление мастера работают в реальном времени на честно обработанной записи.

Это baseline: полный каркас продукта со всеми функциями брифа. День после ночи уходит на точность моделей, полировку UI, презентацию. Чем baseline не является:
- не live RTSP: архитектура это допускает (те же стадии инкрементально), но не делаем;
- не обучает модели: дообученные веса подключаются записью в `config/models.yaml`;
- нет логина и паролей: роль выбирается переключателем в шапке, сервер доверяет заголовку `X-Role`;
- нет звонков, Telegram, SMS, громкоговорителя, ламп и сирен: есть только точка расширения webhook (S15);
- нет идентификации работников и персональной статистики;
- не заявляет «первые на LinQ», снижение травматизма и цифры-иллюстрации кейса как факты.

Обязательные требования кейса (слайд 13) и где они закрыты:

| Требование | Слайс | Как |
| --- | --- | --- |
| Приём видео | 2 | загрузка файла камеры, очередь обработки |
| Распознавание нейросетями | 2, 4, 5, 10 | YOLOv8n и YOLOv8n-pose на LinQ, правила-плагины |
| Оперативное уведомление с кадром, камерой, временем, типом | 6, 7, 8 | WebSocket, лента, захват экрана, мастер |
| Одно нарушение — одно оповещение | 5, 6 | менеджер эпизодов, идемпотентная публикация |
| Журнал с фильтрами по типу, камере, зоне, времени и кадрами | 12 | `/ohs/journal`, CSV |
| Инференс на LinQ с замерами скорости | 2, 3 | адаптер `linq`, экран IT |

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
| Контейнер | Dockerfile (сборка фронта на node, рантайм python:3.12-slim) и docker-compose.yml (S15) |

Без: ORM и Alembic; Celery, Redis и отдельного процесса воркера (одна фоновая asyncio-задача в процессе сервера); ultralytics, torch и supervision в рантайме; стейт-менеджера и react-query на фронте (свой хук `useApi`); CSS-фреймворка (CSS-переменные темы); авторизации; ffmpeg на ноутбуке (видео читает OpenCV, перекодирования нет).

### 3.1 LinQ: правила работы

- Факты, форматы, тензоры, ловушки: `docs/linq/LINQ_CONTRACT.md`. Код smoke test: `tools/linq/`.
- Доступ только через SSH-туннель к ноутбуку Матвея: `tools\linq\tunnel\Connect-LinQ.cmd`, Jupyter `http://127.0.0.1:8888/`. Туннель упал: перезапусти `Connect-LinQ.cmd`; две попытки не помогли — работай на `SAFEWATCH_FAKE=1`, в `## open` строка `долг: <шаг>, проверка на LinQ, туннель недоступен`, позже попробуй снова. На ноутбуке Матвея ничего не меняй.
- Аккаунт Jupyter один на команду, Матвей работает в нём параллельно (папка `matvey/`). Наше — только `~/work/baseline/`, видео и выходы с префиксом `baseline_`.
- Программы `mosprom_*_cut_ap9999_b1_o1_h1m.tpu` в `/auto/cache/hackathon70007/` общие: использовать, не перезаписывать, свои с такими именами не загружать. Чужие программы (`helmet-v1.tpu`, `pose-split-v1.tpu`), очереди, папки и ноутбуки не читать и не трогать.
- Брокер RabbitMQ общий для 37 команд (`guest/guest`). Бэкенд baseline к нему не подключается: запросы к TPU шлёт только `video_worker.py` внутри Jupyter.
- Квота CPU контейнера 1,5 общая с Матвеем: воркер ограничивает потоки (`OMP_NUM_THREADS=1`, OpenCV и onnxruntime по 1 потоку — уже в `video_worker.py`), `--inflight 4`, одна задача baseline на TPU одновременно.
- Перекомпиляция программ TPU и обучение на ноутбуке капитана запрещены: мало памяти, программы уже на LinQ.
- Секреты только в `.env` (`LINQ_*`): не печатать, не логировать, не коммитить, не писать в `tech.md`, `progress.md`, тексты ошибок.

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

Нет пользователей, паролей, сессий и токенов. Нет ссылки на работника в событиях. Нет видеоклипов (доказательство — кадры). Нет сырых тензоров. Нет таблицы настроек: всё в yaml. Нет отдельного поля «принятые меры»: это комментарий действия `resolve`. Нет SLA-полей и сроков. Нет признака «отложено». Понадобилось поле → `CONTRACT GAP`.

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
| ключ `product_name` | 1 | `meta` | `config/default.yaml` | `product_name: SafeWatch` | `tests/test_cameras.py::test_meta_lists_roles_statuses_zone_kinds` |
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
| константа `CONTRACT_VERSION` | 0 | `api`, контракт | `src/safewatch/api.py` | `CONTRACT_VERSION = "1.0.0"` | `tests/test_api_skeleton.py::test_health_ok` |
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
- R10, параметры правила в анализе, HUD и `event_detail`: `rules.defaults(id) | CameraRule.effective` снимка (было `| params`): правило работает с параметрами на момент анализа, а не с текущими значениями по умолчанию; `defaults |` нужен снимкам без `effective`.
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

Фронт baseline простой и рабочий: днём папку `frontend/` заменит фронт Егора, который пишется по тому же `contract/openapi.json`. Время слайса уходит на бэкенд и контракт. На фронте только функциональность из таблицы ниже: без анимаций, без визуальной полировки, без адаптивной вёрстки, кроме одной колонки у экранов мастера. Готовые компоненты библиотек не подбирать, стили — CSS-переменные темы и простая сетка.

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
- Живые прогоны LinQ — только в слайсе 2 и в ревью R5 (раздел 16).

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
2. Живые проверки LinQ — только там, где их требует слайс (S2, R5), в пределах лимита из `CLAUDE.md`. Туннель недоступен — строка `долг` в `## open`, слайс закрывается.
3. Тесты выведены из критериев по разделам 10 и 10.1, мутации — только в слайсах 2, 5, 6, 7; `uv run poe gate` зелёный локально (вместе со сверкой контракта).
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

Ревью (раздел 17) в режиме ночи — после стадии из 5 слайсов, называется по последнему слайсу: `R5`, `R10`, `R15`. После слайса 0 ревью нет: его чек-лист «каркас готов» и есть ревью.

Очередь: `S0, S1, S2, S3, S4, S5, R5, S6, S7, S8, S9, S10, R10, S11, S12, S13, S14, S15, R15`

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
5. `Dockerfile` (сборка фронта на node, рантайм python:3.12-slim с `uv`, копирует `src`, `config`, `contract`, `tools/linq`, `frontend/dist`) и `docker-compose.yml` (порт 8000, том `data/app`, том `models` только чтение, `env_file: .env`, `LINQ_JUPYTER_URL=http://host.docker.internal:8888`); `docker build` проходит, если демон Docker запущен, иначе строка `долг`.
6. README: запуск на Windows и в Docker, мок-режим, переключение бэкенда, куда класть видео, оценка качества (`safewatch eval`), подключение новой модели через `config/models.yaml`.

**Тесты:** `tests/test_delivery.py`: 1 `test_webhook_sent_on_red`, 2 `test_webhook_failure_recorded_event_unaffected`, 3 `test_delivery_idempotent`, 4 `test_channels_in_system_view`; 5 — `docker build` вручную по возможности; 6 — без теста.

**Не делать:** реальные интеграции с лампами и сиренами, звонки, Telegram, хостинг сервиса, HTTPS.

---

### Ревью R15

По разделу 17, охватывает слайсы 11–15. Дополнительно: `gh pr checks` по PR слайсов 11–15; финальный `uv run poe gate`; в `## log` сводка того, что готово к демо и что осталось долгом.

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
