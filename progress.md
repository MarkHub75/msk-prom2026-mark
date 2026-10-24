# progress.md

- state: S2 закрыт, следующий S3
- tech.md: v1
- base branch: main
- remote: github.com/MarkHub75/msk-prom2026-mark
- updated: 2026-10-24

## open

- владелец: положить заводские и сгенерированные видео в `data/videos/` (mp4 H.264, иначе браузер не сыграет эфир).
- long-lead: доступ к LinQ только через SSH-туннель к ноутбуку Матвея; обрыв — работа на фейке, строка `долг`, повтор позже.
- long-lead: ответ организаторов, какие стадии обязаны быть на LinQ; сейчас все нейросети на LinQ, трекинг и правила на CPU.
- long-lead: вопросы организаторам из `docs/linq/LINQ_CONTRACT.md` §8 (честное время TPU, вход uint8, число TPU и квоты, изоляция брокера, второй VPN-логин).
- long-lead: дообученные модели ML-части (огонь, дым, сигарета, погрузчик, привязь); подключаются записью в `config/models.yaml` и `pipeline.extra`, работают с S10.
- long-lead: фронт Егора по `contract/openapi.json` к 10:00 24.10; заменяет папку `frontend/`.
- R5: в живом прогоне проверить, что воркер LinQ держит около 20 кадров/с (ограничение потоков), а не 0,6.
- GAP: S0, тело ошибок в OpenAPI, `router = APIRouter(responses={"4XX": {"model": ApiError}, 501: {"model": ApiError}})`: схема `ApiError` попала в `contract/openapi.json` и `schema.d.ts` (иначе фронт не знает тела ошибки; 4XX заменяет `HTTPValidationError` у 422).
- GAP: S0, `registry.resolve(ref: str, models: list[ModelSpec] | None = None) -> ModelSpec` (необязательный список, чтобы не читать yaml на каждую ссылку); `registry.MODELS_FILE`.
- GAP: S0, `texts.py` сверх 7: `SCENARIO_TITLES: dict[str, str]` (названия 8.3, плагины S5/S10 берут отсюда), `PRODUCT_TITLE`, `REQUEST_INVALID`, `ROLE_REQUIRED`, `ACTOR_INVALID`, `NOT_IMPLEMENTED = "Функция появится в слайсе {slice}"`, `VIDEOS_DIR_MISSING`, `DEMO_SECTORS`, `DEMO_CAMERAS`, `DEMO_ZONE_NAMES`, `DEMO_REASONS`, `DEMO_RESOLVE_COMMENTS`.
- GAP: S0, помощники вне 6.x: `store.conn()` (ленивое соединение живёт в `store._conn`, а не в `services`), `store.insert(table, values) -> int`, `store.demo_world_exists()`, `store.demo_counts()`, `store.demo_cameras()`; `seed.seed_demo() -> SeedReport` и `seed.demo_camera_ids()` (фасад `services.seed_demo` зовёт их); `config.ENV_NAMES: dict[str, str]` (имя ключа `.env` для doctor); `cli.contract_texts() -> dict[str, str]`; `fakes.remote.auto_scene(filename) -> str`; `hub.Client` (`role`, `queue`, `dropped`); `services.ACTOR_MAX` объявлена в S0 (её читает `api`).
- GAP: S0, фронт: `WsMessage` в `src/api/ws.ts` — свой тип `{type, at, data: unknown}` (WS-схемы нет в openapi); `useMeta()` и контекст `/api/meta` в `components/AppShell.tsx` (бейджи и переключатель роли берут названия из meta); `roles.ts` ещё экспортирует `ROLES`, `getRole`, `setRole`.
- GAP: S1, константы `services` вне 6.6: `ROLE_ACTIONS: dict[Role, list[HumanAction]]` (таблица прав 6.2), `TERMINAL_STATUSES: frozenset[EventStatus]` (8.6), `LEVEL_COLORS: dict[Level, str] = {"yellow": "#FFC400", "red": "#FF3B30"}` (цвета темы 8.14 для `LevelMeta.color`).
- GAP: S1, `texts.py`: `FORBIDDEN_ROLE`, `NAME_INVALID`, `DESCRIPTION_INVALID`, `SECTOR_NOT_FOUND`, `CAMERA_NOT_FOUND`, `SECTOR_NAME_TAKEN`, `SECTOR_NOT_EMPTY`, `SECTOR_HAS_HISTORY`.
- GAP: S1, `sector_delete` сектора, на который ссылаются только удалённые камеры или события (FK, у секторов нет `deleted_at`): 409 `sector_not_empty` с текстом `texts.SECTOR_HAS_HISTORY` вместо 204.
- GAP: S1, `store`: `sectors()`, `sector(id)`, `sector_name_taken(name, except_id=None) -> bool`, `sector_update(id, name, sort_order)`, `sector_has_cameras(id) -> bool`, `sector_delete(id)`, `cameras(sector_id=None)` и `camera(id)` (строки без удалённых, с `has_calibration`, `zones_count`, `videos_count` одним запросом), `camera_update(id, values: dict)`, `camera_delete(id, at)` (`deleted_at` и `playing`-эфир → `stopped`); в `services` приватные `_require(role, allowed)`, `_name`, `_description`.
- GAP: S1, фронт: `Modal({title, onClose, children})`, `FormField({label, children})`, `FormModal({title, error, submitText, onSubmit, onClose, children})` (форма в модалке с текстом ошибки API), `ConfirmDialog({text, error, onConfirm, onClose})`; `NavItem.screen?: ComponentType` в `nav.ts`, `App.tsx` рендерит `screen` вместо `StubNotice`; `DataTable` — generic-перегрузка над негенерик-реализацией.
- R5: S5 — `services.meta()` должен брать `scenarios` из `rules.scenario_metas()`; в S1 там пустой список.
- R10: S6 — `camera_delete` останавливает `playing`-эфир только в базе; S6 добавляет WS `broadcast.state` и проверяет это своим тестом.
- долг: S2, критерий 17 (живой прогон), прогон дошёл до TPU (загрузка файлов и видео в `~/work/baseline/`, старт воркера, опрос, хвост лога), но TPU не ответил на первый запрос за 120 с (`TimeoutError: no TPU reply for 1 task(s) in 120 s`, задача `retry_wait`/`remote_error`, воркер сам остановился); кадр/с и RTT не замерены. Лимит один прогон на шаг: повтор в R5.
- R5: повторить живой прогон S2 (`uv run poe live`, `tests/live/test_linq_live.py`): если TPU снова молчит — проверить очередь `input` и логин в URI программы (`JUPYTERHUB_USER` в процессе воркера); записать кадр/с, RTT p50/p90 и время всего.
- GAP: S2, `media.VideoProbe` (pydantic: `width`, `height`, `fps`, `frame_count`, `duration_ms`, `codec`, `browser_playable`) и `media.probe_video(path) -> VideoProbe | None` (`None` — видео не читается); `media.CODEC_ALIASES = {"fmp4": "mp4v"}`: OpenCV отдаёт для mp4v имя FFmpeg `FMP4`, без замены критерий `codec = "mp4v"` не выполним.
- GAP: S2, `LinqBackend` (8.1): «хвост лога содержит `status -3` или `not readable` → `model_missing`» → «только `not readable` → `model_missing`»: лог фейка `remote_error` по 6.1 содержит `status -3` и обязан давать `remote_error`.
- GAP: S2, `LinqBackend`: `.progress` не JSON, пока воркер `RUNNING`, — повтор опроса (воркер переписывает файл на месте), `bad_output` только при `STOPPED`; `--classes` ставится по `model.task == "detect"` (S10 отличит `pipeline.extra`); `upload_s` — проверка размера и загрузка видео; `remote_out` с раскрытым `$HOME` из `# sw:home`; `LinqBackend.check()` → `NotImplementedError("slice 3")`; `WORKER_FILES`, `_load_module(path)`.
- GAP: S2, `inference.make_backend` с `local` → `NotImplementedError("slice 3")`; `config.Settings.inference_backend = Field(default="linq", validation_alias="INFERENCE_BACKEND")` (искомая строка 6.7).
- GAP: S2, `services` вне 6.2: `analysis_step(fps) -> int` (шаг 8.1), `ERROR_TEXT_MAX = 500`, `RETRYABLE: frozenset[JobErrorCode]`, ленивый `_backend` (сбрасывает фикстура `conn`); `Job.metrics` строится из `artifacts.metrics_json` задачи, `cached = artifacts.created_at < jobs.started_at`; повторная загрузка `failed`-видео ставит видео в `uploaded`; без `pipeline.pose` стадия pose пропускается.
- GAP: S2, `store`: `video`, `video_by_sha`, `video_filename(sha256)`, `videos`, `video_update`, `job`, `jobs(status, limit)`, `camera_jobs`, `video_last_job`, `next_job(now)`, `job_update`, `job_progress` (прогресс не убывает), `artifact`, `artifact_update`; `cli.import_video(path, camera_id) -> int`.
- GAP: S2, `FakeRemoteShell`: сцена `auto` берёт исходное имя через `store.video_filename(<стем uploads/<sha256><ext>>)`, иначе имя локального файла (закрывает заметку R5 от S0).
- GAP: S2, `texts.py`: `VIDEO_EXTENSION`, `VIDEO_UNREADABLE`, `VIDEO_TOO_LARGE`, `VIDEO_NOT_FOUND`, `FILE_NOT_FOUND`, `JOB_NOT_FOUND`, `LIMIT_INVALID`.
- GAP: S2, фронт: `uploadVideo(cameraId, file, onProgress)` в `src/api/client.ts` (XMLHttpRequest: у fetch нет прогресса загрузки).

## log

<!-- Append-only. Заголовок читает scripts/contract_check.py, формат не менять:
### S<N>: <name> (YYYY-MM-DD, PR #K | local, tech vX)
- отклонения: <что и почему> | отклонений нет
- решения вне контракта: <что должна знать следующая сессия> | нет
- проверено вживую: <сервисы> | не проверено: <сервисы без ключей>
- [проверить]: <пункт: итог> | нет
- следующему: <появившиеся скрипты, фикстуры, хелперы> | нет

Ревью: ### R<K>: review (YYYY-MM-DD, PR #K, tech vX), строки «найдено и исправлено», «оставлено», «GAP перенесены», «чек-лист 17», «следующему».
Откат: ### S<N> откат: <причина> (ссылка на старую запись).
-->

### S0: skeleton (2026-10-24, PR #1, tech v1)
- отклонения: `.venv/pyvenv.cfg` содержал `uv = 0.13.0`, но это venv инструментов LinQ на Python 3.11 (torch, ultralytics): перенесён в `.venv-linq` всё равно, иначе `uv sync` его пересоздал бы; строка шаблона `data/` в `.gitignore` не добавлена (спрятала бы `data/videos/README.md`), вместо неё `data/app/`, плюс `!frontend/.env.mock` (правило репо `.env.*`); раздел README вставлен сразу под заголовком; `seed_demo` не пишет `camera_rules` (плагинов нет, нет строки — настройки по умолчанию).
- решения вне контракта: настройки все модули читают через `config.get_settings()` (фикстуры `core`/`fake_core` подменяют его там); тесты не читают `.env` (`Settings.model_config["env_file"] = None` в conftest) и чистят `LINQ_*`; `create_app` монтирует `frontend/dist` на `/` с откатом на `index.html`, кроме `/api/*`; doctor до S3 пишет «связь с LinQ: не проверено»; тест `serve` запускает `cli.main` в дочернем `python -c` с `data_dir` в `tmp_path` (у `.venv/Scripts/python.exe` pid сервера — дочерний процесс лаунчера).
- проверено вживую: нет (S0 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: FastAPI 0.162, uvicorn 0.54 (без `[standard]`, на Windows ProactorEventLoop), starlette 1.9 `FileResponse` отвечает на `Range` (206); фронт: vite 7.3, vitest 3.2, react 18.3, react-router-dom 6.30, openapi-typescript 7.13, openapi-fetch 0.17, typescript 5.9 (6+ не брал из-за peer-зависимостей), prism-cli 5.15; poe `shell` на Windows через Git Bash работает; actions: checkout v7.0.1, setup-uv v10.3.2, setup-node v7.1.0 (`gh api .../releases/latest`).
- следующему: фикстуры `client`, `fake_clock`, `make_video(tmp_path, seconds, fps, size, luma, name)`; `FakeRemoteShell` принимает `$HOME/work/baseline/...` и `baseline/...`, на путь вне `baseline/` бросает `ValueError`; `contract/*.json` пересобирает `uv run safewatch contract`, `schema.d.ts` — `npm run api:gen --prefix frontend`; в S1 `meta()` включит названия ролей, уровней и статусов на фронте.

### S1: cameras (2026-10-24, PR #3, tech v1)
- отклонения: правлены файлы вне списка слайса, без которых экран не открывается или `main` красный: `frontend/src/App.tsx` (рендер `screen`), `frontend/src/App.test.tsx` (`stub_screens_show_slice` пропускает маршруты с экраном), `frontend/src/theme.css` (стили модалки и таблицы), `tests/test_api_skeleton.py` (501 проверяется на `/api/system` вместо заработавшего `/api/meta`).
- решения вне контракта: `PUT /api/sectors/{id}` заменяет сектор целиком (`sort_order` по умолчанию 0); `PATCH` камеры пропускает поля со значением `null`; несуществующий сектор в теле камеры — 422, в `?sector_id=` — 404; сценарии в `meta` пусты до S5; хаб в S1 ничего не публикует (WS-типа для секторов и камер нет).
- проверено вживую: нет (S1 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: в `tests/test_cameras.py` хелперы `_sector`, `_camera`, `_error` и `_playing_broadcast` (видео, артефакт, анализ, эфир через `store.insert`); экраны подключаются полем `screen` в `nav.ts`, дымовой тест экрана — в `frontend/src/screens/screens.test.tsx` с `vi.mock("../api/client")`.

### S2: videos (2026-10-24, PR #4, tech v1)
- отклонения: правлены файлы вне списка слайса: `fakes/remote.py` (сцена `auto` по исходному имени, заметка R5), `config.py` (alias `INFERENCE_BACKEND` ради строки 6.7), `tests/conftest.py` (сброс `services._backend`, фикстура `linq_tails`), `tests/test_api_skeleton.py` (пример 501: `/api/models` вместо заработавшего `/api/jobs`); ссылки со списка камер на `/admin/cameras/:id` нет (экран открывается по адресу).
- решения вне контракта: временный файл загрузки `uploads/.tmp-<uuid>` без расширения (OpenCV читает по содержимому); `video_import` хеширует и копирует исходник; прогресс бэкенда из потока идёт в базу через `loop.call_soon_threadsafe`; мутации: сдвиг индекса отката и `>=` в лимите размера, обе пойманы.
- проверено вживую: LinQ Jupyter (вход, загрузка, старт и опрос воркера, лог) | не проверено: ответ TPU (таймаут 120 с, строка `долг`)
- [проверить]: нет
- следующему: фикстура `linq_tails` (пустые хвосты ONNX под подменённым `linq.ROOT`); в тестах бэкенд со сценарием: `monkeypatch.setattr(services, "_backend", LinqBackend(settings, FakeRemoteShell([...])))`; `_tune(monkeypatch, settings, section={...})` в `tests/test_jobs.py` копирует секцию, а не мутирует общий объект; живой прогон: `uv run poe live` (ключи берёт из `.env` сам тест).

## night

<!-- Пишет только оркестратор /night-shift. Строка на шаг:
- HH:MM <шаг>: ок | ок со второй попытки (<причина>) | закрыт с долгом (<что>), PR #K[, #M]
В конце ночи: ### итог ночи (YYYY-MM-DD), до 15 строк.
-->
- 05:05 S0: ок, PR #1
- 05:12 S0 CI: ок со второй попытки (ubuntu: `safewatch stop` ждал зомби), PR #1, #2
- 05:22 S1: ок, PR #3
