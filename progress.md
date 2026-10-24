# progress.md

- state: S1 начат
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
- R5: `FakeRemoteShell` выбирает сцену `auto` по имени локального файла, а `LinqBackend` загружает `uploads/<sha256><ext>`, где исходного имени нет: в S2 сцена `auto` даст `demo`, если бэкенд не передаст имя. Проверить, что S2 решил это (например, `FakeRemoteShell(scene=...)` в тестах или имя видео в команде).

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

## night

<!-- Пишет только оркестратор /night-shift. Строка на шаг:
- HH:MM <шаг>: ок | ок со второй попытки (<причина>) | закрыт с долгом (<что>), PR #K[, #M]
В конце ночи: ### итог ночи (YYYY-MM-DD), до 15 строк.
-->
- 05:05 S0: ок, PR #1
