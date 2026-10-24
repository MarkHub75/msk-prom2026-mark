# progress.md

- state: tech v5, второй прогон: S16 закрыт, следующий S17
- tech.md: v5
- base branch: main
- remote: github.com/MarkHub75/msk-prom2026-mark
- updated: 2026-10-24

## open

- владелец: положить заводские и сгенерированные видео в `data/videos/` (mp4 H.264, иначе браузер не сыграет эфир).
- long-lead: доступ к LinQ только через SSH-туннель к ноутбуку Матвея; обрыв — работа на фейке, строка `долг`, повтор позже.
- long-lead: ответ организаторов, какие стадии обязаны быть на LinQ; сейчас все нейросети на LinQ, трекинг и правила на CPU.
- long-lead: вопросы организаторам из `docs/linq/LINQ_CONTRACT.md` §8 (честное время TPU, вход uint8, число TPU и квоты, изоляция брокера, второй VPN-логин).
- long-lead: дообученные модели ML-части (огонь, дым, сигарета, погрузчик, привязь); подключаются записью в `config/models.yaml` и `pipeline.extra`, работают с S10.
- long-lead: фронт Егора (`front/argus-main` и `front/final-*`) по `contract/openapi.json`; с S16 — контракт 1.1.0; заменить папку `frontend/` в `main` — решение владельца.
- long-lead: ресёрч доп-сценариев `docs/research/EXTRA_SCENARIOS_<дата>.md`, нужен к S31; нет файла — S31 закрывается без кода.
- long-lead: файлы моделей Матвея (`models/matvey/...`, архив из `docs/ML_HANDOFF_MATVEY.md` ветки `matvey_cv`) — для проверки S20 на `local`; без них записи реестра есть, `doctor` пишет «нет файла».
- владелец: перед S21 запустить Docker Desktop (иначе `docker build` снова уйдёт в `долг`).
- владелец: удалить мусорные логи вне репо `D:\npm1.log` и `D:\scratch_fe.log` (удаление заблокировала защита Claude Code).
- долг: S15, docker build, демон Docker не запущен (`docker info`: нет `dockerDesktopLinuxEngine`); Dockerfile и compose не собирались ни разу.
- долг: R5, `JupyterShell` не закрывает kernel: каждый процесс (сервер, doctor, живой тест) оставляет один idle kernel на общем аккаунте, `_drop` закрывает его только при ошибке; нужен `close()` в `RemoteShell` из lifespan и doctor. Перенесено из R15: проверяется только вживую, живых прогонов в R15 нет (3.1); владелец: до правки гасить idle kernels в Jupyter вручную.
- долг: R5, прогон, прерванный остановкой сервера, оставляет удалённый `video_worker.py` живым; повтор с тем же `<out>` запустит второй воркер в тот же файл (`# sw:start` не гасит старый pid). Перенесено из R15: проверяется только вживую; владелец: перед повтором живого прогона проверить процессы `video_worker.py` в терминале Jupyter.
- долг: R5, `backend_check`: Jupyter отдал HTML через `JupyterError` → сейчас `unreachable`, по 6.2 — `bad_answer`. Перенесено из R15: не воспроизводится (R5: `ok`, 2 из 2 программ).
- долг: S5, сцена `demo` теряет id трекера в момент падения (падение подтверждается веткой «лежит неподвижно», бег закрывается `track_lost_timeout`). Перенесено из R15: нужна проверка на заводском видео, его нет (строка `владелец` выше).
- долг: S6, лента и состояния камер считают демо-события сида: жёлтые `confirmed` открыты и попадают в ленту оператора с приоритетом 1 (до `feed.limit`). Перенесено из R15: флаг `include_demo` есть только у журнала и статистики (S12–S13), у ленты его нет в контракте 6.2; на демо сид наполняет экран оператора — решает владелец вместе с фронтом Егора.
- долг: S10, `explain` новых плагинов — одна строка правила и `why_common`; в `explain` зоны proximity нет единицы дистанции (берётся `reason_text`). Перенесено из R15: косметика экрана события, ночью не правится.
- долг: R5, загрузка большого файла целиком ложится на диск до проверки роли и размера (Starlette `UploadFile`). Перенесено из R15: нужен потоковый приём в `api.py`, вне ночного объёма.
- долг: S11, `services._freshness` читает `hud.jsonl` анализа один раз в потоке event loop (потом кэш `_frames_ts`). Перенесено из R15: чтение разовое (10 мин при 10 кадр/с — 6000 строк, миллисекунды), `to_thread` требует асинхронных `camera_states` во всех экранах.
- долг: S14, CLI `eval` при запущенном сервере пишет `artifacts` в ту же базу вторым процессом (WAL, `busy_timeout = 1000`; `database is locked` при долгой записи сервера не проверен); `eval_run` синхронный (`asyncio.run`) и из API не вызывается; любая `InferenceError`, в том числе pose, → exit 4 без отката на анализ без pose (6.10). Перенесено из R15: владелец запускает `safewatch eval` при остановленном сервере.
- долг: S15, очередь доставок `_deliveries` живёт в памяти: доставки, поставленные перед остановкой сервера, теряются; уровень канала берётся на момент `deliveries_flush` (жёлтое, эскалированное в окне одного `broadcast.tick_ms`, уходит `published` уже красным); две записи `delivery.webhooks` с одним `name` делят ключ `webhook:<name>`, вторая не получает ничего. Перенесено из R15: очередь в базе — новая схема; владельцу — уникальные имена webhook в `config/user.yaml`.
- владелец: передать Егору: контракт 1.1.0 — маршруты `GET /api/demo/packs`, `GET /api/calculator/defaults`, `POST /api/calculator/rollout`, `POST /api/calculator/scale`, `GET /api/datasets/false-alarms`, `GET /api/datasets/false-alarms/export.zip`, `PATCH /api/events/{event_id}/identity`, `GET /api/stats/people`, `GET /api/cameras/{camera_id}/passport`, `GET /api/master/shift.pdf` (до своего слайса отвечают 501); поля `Video.web_playable`, `Job.status_text`/`eta_s`/`rate_fps`, `EventSummary.clip`/`person_name`/`person_position`/`crew`, `EventDetail.can_identify`, `Analysis.auto_calibration`, `CameraSetupView.auto_calibration`, `HudObject.projection`, `Delivery.delivered_at`/`status_text`, `ModelSpec.nc`/`input_name`, `Channel.kind` + `call`, `LogAction` + `identified`; `meta.product_name = Argus`, 3 новых типа зон (`helmet_required`, `respirator_required`, `walkway`); файл `contract/openapi.json`, снимок 1.0.0 — `contract/openapi.1.0.0.json`.

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

### S3: backend status (2026-10-24, PR #5, tech v1)
- отклонения: правлены файлы вне списка слайса: `store.py` (SQL очереди и восстановления), `texts.py`, `inference/__init__.py` (`local` → `LocalBackend`), `frontend/src/nav.ts`, `frontend/src/App.test.tsx` (заглушка WebSocket), `tests/conftest.py` (сброс `_backend_status`), `tests/test_jobs.py` (`make_backend("local")`), `tests/test_api_skeleton.py` (примеры 501: `/api/videos/1/analysis`, `/api/ohs/rules` вместо заработавших `/api/system`, `/api/models`); фейк не менялся: `unreachable` и `bad_answer` тесты задают через `shell.fault` и подмену `_check`.
- решения вне контракта: `backend_check` идёт через ленивый `services._backend` (тот же, что у задач); бейдж шапки появляется только после первого `backend.status` (до проверки шапка показывает только бэкенд из `meta`); `system_view.models` — активные модели; `latency` — нули до S6.
- проверено вживую: нет (S3 без LinQ, лимит) | не проверено: LinQ Jupyter (`check`, `ls`)
- [проверить]: нет
- следующему: в тестах бэкенд со своим шеллом: `monkeypatch.setattr(services, "_backend", LinqBackend(settings, FakeRemoteShell()))`, недоступность в проверке — `shell.fault = "unavailable"`; `LocalBackend` прогоняется в `tests/test_local_backend.py` на `models/*.onnx` (локально есть, в CI пропуск).

### S4: tracking (2026-10-24, PR #6, tech v1)
- отклонения: правлены файлы вне списка слайса: `texts.py` (подписи HUD), `frontend/src/api/client.ts` (`videoUrl`); `geometry.ioa`, `point_rect_distance`, `point_segment_distance` из раздела 7 не написаны: их первый потребитель — плагины S10, сейчас это мёртвый код; подписи наблюдений `P` в HUD не написаны (плагинов нет до S5).
- решения вне контракта: в S4 техника трекается (`VehicleState` с `speed_vh_s=None`, `footprint=None`), прочие классы — объекты без трека; подписи скорости в м/с, калибровка и зоны — S9; плеер вкладки «Видео» показывает видео с `active_analysis_id`, кнопка «Смотреть с HUD».
- проверено вживую: нет (S4 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `pipeline.analyze` уже строит `FrameContext` на кадр: S5 вызывает плагины и `EpisodeManager` в том же цикле и добавляет подписи наблюдений в `build_hud`; в тестах анализ на синтетике — `scenes.render(scene, 800, 240, 25, n, 2, "detect")` и `analyze(det, None, Path("unused.mp4"), cfg, None, model)` (`tests/test_tracking.py::_people`); готовый анализ через задачу — `_analyzed` в `tests/test_tracks_api.py`.

### S5: episodes (2026-10-24, PR #7, tech v1)
- отклонения: правлены файлы вне списка слайса: `types.py` (`AnalysisConfig.duration_ms`), `analysis/hud.py` (теги наблюдений), `analysis/geometry.py` (расстояния), `texts.py`, `frontend/src/api/client.ts` (`apiUrl`), `frontend/src/theme.css`, `frontend/src/components/{Timeline,EvidenceImage}.tsx` по разделу 7, `tests/test_{hud,tracking}.py` (новые аргументы), `tests/test_cameras.py` (сценарии в meta), `tests/test_api_skeleton.py` (пример 501: `/api/operator/feed` вместо заработавшего `/analysis`); заметка R5 от S1 закрыта: `meta()` берёт `rules.scenario_metas()`.
- решения вне контракта: пересчёт до S9 даёт тот же снимок (зон, калибровки и правил камеры ещё нет), `superseded` нет; мутации: сдвиг порога `end_after_s` (`>=` → `>`) и перевёрнутое условие перехода в `fall`, обе пойманы.
- проверено вживую: нет (S5 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: в `tests/test_analysis_api.py` хелперы `_textured(path, seed)` (видео 20 с, 10 fps, 1600×300 с шумом) и `_demo_job` (задача на сцене `demo`: жёлтый бег и красное падение); `tests/test_rule_running.py`: `person(**update)`, `context(p, zones, vehicles, ts_ms)`, `zone(kind)`, `truck(x1, footprint)` (импорт `from test_rule_running import ...`); эпизоды анализа для эфира S6 — `store.episodes(analysis_id)`.

### R5: review (2026-10-24, PR #8, tech v2)
- найдено и исправлено: цикл задач `worker.run_forever` умирал на любом исключении вне `try` (например, `database is locked` в `next_job`) и останавливал очередь до перезапуска — теперь лог и повтор через `idle_poll_ms`, `_video_row` внутри `try`; `JupyterShell` держал мёртвую сессию и kernel после обрыва (повторы не могли пройти) — `_drop()`; диагностика TPU: строка очереди `input` и URI в `<out>.log`, счётчик `unmatched replies` в таймауте.
- оставлено: kernel Jupyter не закрывается, порог HUD для S9, дубли `recompute`, осиротевший удалённый воркер, HTML от Jupyter → `unreachable` (строки `R10` в `## open`); загрузка большого файла целиком ложится на диск до проверки роли и размера (Starlette `UploadFile`), ночью не правится; `hub.Client.dropped` не читается — оставлен под наблюдаемость S11.
- GAP перенесены: 44 строки S0–S5 → tech.md v2 (6.8, 11 строк 6.7, 8.1, 8.2, 7); решения: `PUT` сектора по `SectorIn` и `PATCH` камеры без `null` соответствуют контракту, `model_missing` только по `not readable`, жёлтая скорость при `≥`, doctor без ключей не зовёт `backend_check`.
- чек-лист 17: 1–2 ок (`poe contract` 338 элементов, `safewatch contract --check` чистый; `poe api` не запускался); 3 ок, кроме импортов `clock`/`registry`/`worker` в `api.py` (узаконены в 6.8); 5, 7, 11 ок; 8: `vulture` — только `Client.dropped`; 14: CI PR #1 ubuntu красный, починен PR #2; #2–#7 зелёные в обеих ОС.
- проверено вживую: LinQ Jupyter (`backend_check` через doctor: `ok`, 2 из 2 программ `mosprom_*`), загрузка и старт воркера | не проверено: ответ TPU (очередь `input` без консьюмеров, строка `долг`); итог прогона: 0 кадров, 2 мин 6 с, эпизодов нет, минут TPU 0.
- следующему: `linq_tpu.py ping` из `~/work/baseline/` — первая проверка перед живым прогоном; тест цикла задач с подменой `services.run_next_job` — `tests/test_jobs.py::test_job_loop_survives_unexpected_error`.

### S6: broadcast (2026-10-24, PR #9, tech v2)
- отклонения: правлены файлы вне списка слайса: `frontend/src/api/ws.ts` (`WsNotification`), `frontend/src/theme.css` (плитки, лента, всплывашки, оверлей), `tests/conftest.py` (сброс синглтонов), `tests/test_jobs.py` (цикл задач без базы: подмена `broadcast_tick`; `broadcast.state` автостарта в тесте прогресса), `tests/test_system.py` (`cameras` = `camera_states()`), `tests/test_api_skeleton.py` (пример 501: `/api/master/inbox` вместо заработавшего `/api/operator/feed`); вкладка «Эфир» — секция страницы `CameraSetup`, как и «Видео» (вкладок там нет).
- решения вне контракта: строки `GAP: S6` в `## open`; мутации: сдвиг порога публикации (`confirm_ms > pos` → `>=`) и пропущенная запись действия `published`, обе пойманы (8 и 6 падений `test_broadcast.py`).
- проверено вживую: нет (S6 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: хелперы `tests/test_broadcast.py`: `ready_video(camera_id, episodes, duration_ms)` (готовое видео с активным анализом, эпизоды поверх `EPISODE`), `camera(sector)`, `playing(episodes, loop, duration_ms)` (id эфира), `drain(hub_client)`, `events()`, `actions(event_id)`, `at(fake_clock, started_at, ms)`, `started(broadcast_id)`; `tests/test_operator_views.py::event(camera_id, **values)` (строка события с одним действием, `last_action_at`); `screens.test.tsx::wsHandlers()` доставляет WS-сообщение всем подписчикам `useWs`; события создаёт только `broadcast_tick`, S7 читает их через `store.event` и `_summary`.

### S7: event actions (2026-10-24, PR #10, tech v2)
- отклонения: правлены файлы вне списка слайса: `frontend/src/components/EvidenceImage.tsx` (рамка и выноска, отложенные из S5 по 6.8), `frontend/src/screens/operator/CameraScreen.tsx` (проп `cameraId`), `frontend/src/theme.css`, `tests/test_worker.py` (третий цикл `escalation_tick`), `tests/test_api_skeleton.py` (пример 501: `/api/master/shift` вместо заработавшего `/api/events/5`; действие с допустимым `X-Actor` теперь 404); тест сверх списка `test_escalation.py::test_decision_counts_only_after_red_at` (ветка «нет решения оператора после `red_at`»).
- решения вне контракта: строки `GAP: S7` в `## open`; мутации: сдвиг порога таймаута (`red_at <= ?` → `<`) и пропущенная запись действия человека в `event_actions`, обе пойманы (8 и 26 падений).
- проверено вживую: нет (S7 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_event_actions.py`: `ROWS` (человеческие строки 8.6), `journal(event_id)` (действия после `published`: роль, действие, из, в), `row(event_id)`; `tests/test_escalation.py::red(fake_clock, **values)` (красное событие с `red_at = now`); уведомление мастеру на `sent_to_master` уже шлют `event_action` и `escalation_tick` (S8 проверяет критерий 2); `event_detail` на эпизоде требует валидный `config_json` анализа (хелпер `ready_video` пишет `{}` — для карточки бери `_demo_job`).

### S8: master (2026-10-24, PR #11, tech v2)
- отклонения: правлены файлы вне списка слайса: `frontend/src/theme.css` (карточки мастера в одну колонку), `tests/test_api_skeleton.py` (примеры 501: `/api/journal/facets`, `/api/stats/ohs` вместо заработавших `/api/master/inbox`, `/api/master/shift`); тесты сверх списка: `test_master.py::test_master_notified_when_his_event_turns_red` (строка 4 таблицы 8.8, закрыта заметка R10 от S6), `test_shift.py::test_other_timezone_moves_the_window`; пишущих функций в S8 нет — права ролей `accept`/`resolve` уже покрыты `test_event_actions.py::test_roles_enforced` (S7).
- решения вне контракта: строки `GAP: S8` в `## open`; мутаций нет (10.1).
- проверено вживую: нет (S8 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_master.py`: `handed(event_id, action, at)` (строка журнала передачи), `stamp(minute)`, `inbox(client)`; `tests/test_shift.py::utc(day, hour, ...)`; сквозной тест `tests/test_e2e.py::test_upload_to_master_flow` (загрузка через API, `run_next_job`, тики эфира на `fake_clock` по 0,5 с до красного) — образец для R10.

### S9: calibration (2026-10-24, PR #12, tech v2)
- отклонения: правлены файлы вне списка слайса: `analysis/hud.py` (порог по правилу камеры, заметка R10), `texts.py`, `tests/test_hud.py` (новая сигнатура `build_hud`), `tests/test_videos.py` (`rules` в `CameraSetupView`), `tests/test_api_skeleton.py` (пример 501: `/api/events` вместо заработавшего `/api/ohs/rules`), `screens.test.tsx::camera_setup_timeline_renders` (две кнопки «Пересчитать события»); гомография — DLT numpy вместо `cv2.findHomography` (строка GAP); `footprint` и м/с техники не считаются (8.2 п. 6 — S10).
- решения вне контракта: строки `GAP: S9`; мутаций нет (10.1); закрыты заметки R10: порог HUD, дубли `recompute`, пример 501.
- проверено вживую: нет (S9 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_calibration.py`: `camera()` (нужен `core` или `client`), `body(image, world, control)`, `SQUARE`, `FLOOR`, `_walk(x0)` (человек 100 px/с), `_config(calibration, rules)`; плагины S10 получают зоны снимка через `ctx.zones`, метры — `PersonState.ground`; тесты пересчёта — `tests/test_recompute.py` (события на эпизодах `_demo_job` через `test_operator_views.event`).

### S10: zone scenarios (2026-10-24, PR #13, tech v2)
- отклонения: правлены файлы вне списка слайса: `services.py` (третий проход extra, `rules.plugin`), `inference/local.py` (`nc` модели extra), `fakes/remote.py` (`--nc` → пустые кадры), `texts.py`, `tests/test_{analysis_api,camera_rules,cameras,videos}.py` (список из 10 сценариев вместо двух S5), `tests/test_geometry.py` (свойства `ioa`, `segment_crossing`); `PLUGINS` из словаря стал списком по строке 6.7; пересчёт без моделей extra — строка `долг`.
- решения вне контракта: строки `GAP: S10`; мутаций нет (10.1); живых прогонов нет; критерий 7 проверен запуском `video_worker.main()` с заглушками `linq_tpu`/`yolo_io` (`tests/test_plugin_status.py::test_worker_nc_argument`).
- проверено вживую: нет (S10 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: хелперы `tests/test_rule_phone.py`: `worker()` (человек 200 px), `ctx_with(people, objects, zones, ts_ms)`, `phone(cx, cy)`; `tests/test_rule_proximity.py::truck(distance_bh, vh_s, m_s, footprint, x1)`; фикстура `extra_registry` в `tests/test_plugin_status.py` (реестр с моделью огня `fire-test@1`, хвост в `linq_tails`).

### R10: review (2026-10-24, PR #14, tech v3)
- найдено и исправлено: `test_jobs.py::test_job_loop_survives_unexpected_error` без фикстуры гонял `worker.run_forever`, чей третий цикл `escalation_tick` (S7) открывал настоящую `data/app/safewatch.db` (отсюда mtime `data/app` на каждом гейте) — тест получил `core`, а `tests/conftest.py` — autouse `no_real_data` (создание `data/app` или `connect` к базе в ней валит тест); долг S10 закрыт: `AnalysisConfig.extra_artifact_ids` в `config_json`, `recompute` берёт артефакты `pipeline.extra` без новой схемы; правило, HUD и `explain` берут параметры снимка (`defaults | effective | params`), а не текущие defaults (заметка S9); длина `X-Actor` проверяется только в `services` (заметка S7, порядок проверок S7 соблюдён); имя камеры в списке — ссылка на `/admin/cameras/:id` (заметка R5); сквозной тест находит красное событие через `/api/operator/feed`, а не через `store`.
- оставлено: 9 заметок перенесены в `R15:` с причиной (kernel Jupyter, осиротевший воркер, HTML Jupyter — только вживую; потеря id в `demo` — нужно заводское видео; `latency` и `Client.dropped` — S11; демо-события в ленте; HUD для `pair:`/`zone:`/`fire` — `hud.py` в файлах S11; `explain` новых плагинов; загрузка на диск до проверки роли); 4 WebSocket на вкладку закрыто без правки: фронт минимальный (8.14, 10.1), его заменяет фронт Егора; `Job.metrics` без прохода extra — по 6.9 (колонок нет); `_analysis_inputs` читает артефакт extra по одному запросу на модель (моделей единицы).
- GAP перенесены: 37 строк S6–S10 → tech.md v3 (6.9, 3 строки 6.7: `rules.plugin`, `geometry.ioa`, `AnalysisConfig.extra_artifact_ids`); решения R10 там же.
- чек-лист 17: 1–2 ок (`poe contract` 447 элементов, `poe api` чистый, `contract/openapi.json` не менялся); 3 ок; 5 ок, кроме записи `superseded` по событию в цикле `_recomputed` (записи, не чтения); 7 ок (`to_thread` пишет только файлы); 8: `vulture` — заглушки S13–S15 и параметры обработчиков ошибок; 11 ок; 12 нет пунктов; 13 закрыт; 14: CI PR #9–#13 зелёные в обеих ОС (PR #13 проверен в R10). Коммит закрытия S6 ушёл в `refactor(feed)`, а не в `docs(progress): close slice 6` (squash скрыл, не правилось).
- проверено вживую: нет (живых прогонов в R10 нет) | не проверено: LinQ Jupyter; `data/app` владельца после полного прогона тестов не изменилась (mtime 08:02 до и после).
- следующему: autouse `no_real_data` валит тест, который открывает базу без `core`/`conn`; пересчёт с extra — `tests/test_plugin_status.py::test_extra_model_enables_fire_without_code`; `CameraRule` в тестах можно строить с `effective={}` (поверх идут defaults и `params`).

### S11: observability (2026-10-24, PR #15, tech v3)
- отклонения: правлены файлы вне списка слайса: `tests/conftest.py` (сброс `_frames_ts`), `tests/test_{broadcast,cameras,operator_views}.py` (ручные анализы пишут `hud.jsonl` через `test_broadcast.hud_file`, иначе `freshness_ms` не читает кадры); `SectorTile.tsx`, `hud.py`, `scenes.py` не менялись (плитки уже показывают `reason_text` сервера, сцена `dark` есть); критерий 5 проверен в `system_screen_renders` (таблица свежести, «Слишком темно»), `operator_dashboard_renders` уже проверяет причину сектора.
- решения вне контракта: строки `GAP: S11`; мутаций нет (10.1); живых прогонов нет; `latency` и `Client.dropped` не тронуты (нет в критериях), заметки `R15` уточнены.
- проверено вживую: нет (S11 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_broadcast.py::hud_file(name, frames_ts)` (HUD-файл ручного анализа); `tests/test_observability.py`: фикстура `luma` (что `sample_luma` вернёт в `analyze`), `_run(mean, std, start, end, duration)`, `_episodes(scene, det_drop, speed_bh_s)`; `tests/test_camera_state.py::_at_position(pos, *setup)` (камера с `GAPS` на позиции эфира).

### S12: journal (2026-10-24, PR #16, tech v3)
- отклонения: правлены файлы вне списка слайса: `types.py` (`EventSummary.evidence_url`, строка GAP), `texts.py` (тексты журнала и CSV), `contract/*.json` и `schema.d.ts` (пересборка), `tests/test_api_skeleton.py` (примеры 501: только `/api/stats/*`); стили фильтров не добавлены (`theme.css` вне списка, фронт минимальный 8.14); тестов прав ролей нет: в S12 только чтение, роли по 6.2 не проверяются.
- решения вне контракта: строки `GAP: S12`; мутаций нет (10.1); живых прогонов нет; `test_e2e.py`: сценарий S8 вынесен в `_flow(...) -> (camera_id, event_id)`, его зовут оба теста.
- проверено вживую: нет (S12 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_journal.py`: `world()` (2 сектора, 2 камеры, зона, 6 событий: бег, красное падение в зоне, ложный телефон, `superseded`, демо, «50% · a_b»), `page(client, **params)`, `found(client, **params)`; `tests/test_export.py::rows(body)` (CSV с BOM → строки); S13 может брать `store.journal_where` для фильтров статистики.

### S13: stats (2026-10-24, PR #17, tech v3)
- отклонения: правлены файлы вне списка слайса: `texts.py` (период, тексты тренда, `weeks_span`), `frontend/package.json` и `package-lock.json` (`recharts`), `tests/test_api_skeleton.py` (501 проверяется подменой фасада: незаконченных маршрутов не осталось); стили графиков не добавлены (`theme.css` вне списка, 8.14); тестов прав ролей нет: статистика только читает, роли по 6.2 не проверяются; тесты сверх списка: `test_stats_ohs.py::test_period_invalid`, `test_stats_management.py::test_weeks_validation` (критерий 6 и строка 9 «статистика»).
- решения вне контракта: строки `GAP: S13`; мутаций нет (10.1); живых прогонов нет.
- проверено вживую: нет (S13 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_stats_ohs.py`: `cameras()` (2 сектора, по камере), `act(event_id, seconds, role, action)` (действие через `seconds` после `AT`), `counts(rows)`, `stats(client, **params)`, `DAY`; `tests/test_stats_management.py::sector(name, cameras)`; `fake_clock` — суббота 2026-10-24, текущая неделя с 2026-10-19 МСК.

### S14: eval (2026-10-24, PR #18, tech v3)
- отклонения: правлены файлы вне списка слайса: `texts.py` (тексты отчёта и ошибок разметки); в `services.py` оценка переиспользует `_infer` (`job_id=None`) и общий с `_analyze` снимок `_analysis_config`, `video_import` берёт `_sha256`; правило 4 для `eval.deadline_s` — в `test_report_files_written` (20 с → tp, 0,001 с → fn).
- решения вне контракта: строки `GAP: S14`; мутаций нет (10.1); живых прогонов нет.
- проверено вживую: нет (S14 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `tests/test_eval.py`: `episode(confirm_s, scenario)` (черновик эпизода), `labels_file(tmp_path, data, name)`, `shell(monkeypatch, script)` (бэкенд на `FakeRemoteShell`), `row(rows, scenario)`; README S15: `uv run safewatch eval config/eval.example.yaml`.

### S15: delivery (2026-10-24, PR #19, tech v3)
- отклонения: правлены файлы вне списка слайса: `texts.py` (ошибки доставки), `tests/conftest.py` (сброс `_deliveries`), `tests/test_worker.py` (четвёртый цикл `deliveries_flush`, 12 пауз вместо 9); критерий 5 — `docker build` не запускался (демон Docker не запущен, строка `долг`); в README дополнен только раздел «Приложение SafeWatch».
- решения вне контракта: строки `GAP: S15`; мутаций нет (10.1); живых прогонов нет; webhook в тестах — только `respx`.
- проверено вживую: нет (S15 без LinQ и без Docker) | не проверено: LinQ Jupyter, `docker build`
- [проверить]: нет
- следующему: `tests/test_delivery.py`: `hooks(monkeypatch, core, (name, url, levels), ...)` (каналы `delivery.webhooks`), `bodies(route)` (JSON запросов respx), `deliveries()`; доставку события в тесте ставят `services._deliveries.append((event_id, kind))`.

### R15: review (2026-10-24, PR #20, tech v4)
- найдено и исправлено: `system_view.latency` отдавал нули — считается по событиям эфира (`store.publish_latencies`, `services._latency`, тест `test_latency_counts_published_events`); HUD подписывал только `track:<id>` — подписи на `pair:` (человек и техника), `zone:` и `fire` (8.2 п. 8, `hud._keys`); плохой `url` в `delivery.webhooks` (`http://[::1`) ронял каждый `deliveries_flush` после очистки очереди (`httpx.InvalidURL` не `HTTPError`) и `system_view` (500) — проверка в `WebhookConfig` при загрузке; курсор `"²"` проходил `isdigit()` и давал 500 вместо 422; нет `hud.jsonl` → `_freshness` валил состояния всех камер — теперь `None`; мёртвое `hub.Client.dropped` удалено; пустой цикл `App.test.tsx::stub_screens_show_slice` — тест проверяет, что у каждого маршрута есть экран; подпись «По» статистики при невключаемом `date_to` → «До (не включая)», как в журнале.
- оставлено: 13 заметок `R15:` — 3 закрыты правкой (latency, HUD, тест заглушек), 10 перенесены в `долг:` с причиной и действием владельца (kernel, осиротевший воркер и HTML Jupyter — только вживую; потеря id в `demo` — нет заводского видео; демо-события в ленте; `explain`; загрузка на диск; `_freshness` в event loop; `eval` вторым процессом и без отката pose; очередь доставок в памяти, уровень на момент flush, одинаковые имена webhook); `stale` начинается с кадра до разрыва (по GAP S11, 8.10 не фиксирует); `master_accept_s` от `timeout_escalated` — по GAP S13 (`HANDOVERS`); тесты прав ролей S12–S14 не нужны (функции чтения без `role`, 6.10); поиск журнала шлёт запрос на каждое нажатие и стилей фильтров нет — фронт минимальный (8.14), его заменяет фронт Егора; фасеты журнала — только живые камеры (GAP S12).
- GAP перенесены: 25 строк S11–S15 → tech.md v4 (6.10, 5 строк 6.7: `observability.Luma`, `media.LUMA_WIDTH`, `store.publish_latencies`, `services.DELIVERED`, `delivery.target`); решения R15 там же.
- чек-лист 17: 1–2 ок (`poe contract` 480 элементов, `poe api` чистый, `contract/openapi.json` не менялся); 3 ок (SQL только в `store`/`db`, `analysis/`/`rules/` без базы и сети); 4 ок (webhook только через `WebhookChannel`); 5 ок (`deliveries_flush` пишет по строке — записи, не чтения); 7 ок (`to_thread` в доставке не пишет в базу); 8: `vulture` — только параметры `request` обработчиков ошибок; 11 ок; 12 нет пунктов; 13 закрыт; 14: CI PR #15–#19 зелёные в обеих ОС (PR #19 проверен в R15).
- проверено вживую: нет (живых прогонов в R15 нет, 3.1) | не проверено: LinQ Jupyter, `docker build`.
- готово к демо (`SAFEWATCH_FAKE=1` или `local`): камеры и секторы, загрузка и обработка видео, трекинг и HUD, сценарии на классах COCO (бег, падение, зоны, техника, телефон; огонь и курение, привязь, груз ждут дообученных моделей из long-lead), эфир с лентой, захватом экрана и сиреной, решения оператора и автоэскалация, мастер смены, калибровка и зоны с пересчётом, наблюдаемость и свежесть, журнал с CSV, статистика ОТ и менеджмента, `safewatch eval`, webhook-доставка, экран IT с задержкой уведомлений; контракт фронта Егора `contract/openapi.json`.
- долги на конец: живой прогон на TPU (очередь `input` без консьюмеров, кадр/с и RTT не замерены); `docker build` не собирался (владелец: запустить Docker Desktop, `docker compose build`); 10 строк `долг:` из R15 в `## open`; заводских видео нет.
- следующему: `tests/test_hud.py::test_label_on_every_positive_subject` (наблюдения `pair:`/`zone:`/`fire`); `tests/test_broadcast.py::test_latency_counts_published_events` (задержка публикации на `fake_clock`).

### S16: contract v5 (2026-10-24, PR #22, tech v5)
- отклонения: правлен файл вне списка слайса `tests/test_cli.py` (версия контракта в `/api/health`); `texts.py` не менялся: новых текстов в S16 нет (`SCENARIO_MODEL_MISSING` и `SCENARIO_TITLES` v5 — S20); проверка уникальности имён каналов в `DeliveryConfig` не написана (по 6.11.8 это S23); `demo.pack` хранится как есть, без разрешения от корня репо (решает S17, первый читатель); маршруты zip и pdf описаны в `openapi.json` как CSV и картинка улики первой ночи (`application/json` с пустой схемой; тип ответа — в таблице 6.11.6).
- решения вне контракта: заглушки фасада v5 бросают `NotImplementedError("slice N")` по столбцу «Слайс» 6.11.4 (`backend_close` — 28); заголовок `FastAPI(title="SafeWatch API")` не менялся (не путь и не поле контракта); в `ws-examples.json` у всех `event.*` есть `clip`, у `event.updated` заполнена идентификация, `hello.contract` = 1.1.0; мутаций нет (10.3); живых прогонов нет.
- проверено вживую: нет (S16 без LinQ) | не проверено: LinQ Jupyter
- [проверить]: нет
- следующему: `contract/openapi.1.0.0.json` — снимок для `test_openapi_only_grows`, не пересобирать; `tests/test_api_skeleton.py::V5_REQUESTS` — запрос на каждый маршрут 6.11.6: слайс, который строит маршрут, убирает его строку (когда список опустеет, тест 501 переходит на подмену фасада, как в S13); `tests/test_contract_files.py::V5_FIELDS` — поля 6.11.3; база версии 1 в тесте — `executescript` файла `0001_init.sql` (`tests/test_db.py::test_migrate_v5_tables_and_columns`).

## night

<!-- Пишет только оркестратор /night-shift. Строка на шаг:
- HH:MM <шаг>: ок | ок со второй попытки (<причина>) | закрыт с долгом (<что>), PR #K[, #M]
В конце ночи: ### итог ночи (YYYY-MM-DD), до 15 строк.
-->
- 05:05 S0: ок, PR #1
- 05:12 S0 CI: ок со второй попытки (ubuntu: `safewatch stop` ждал зомби), PR #1, #2
- 05:22 S1: ок, PR #3
- 05:42 S2: закрыт с долгом (живой прогон: TPU не ответил за 120 с, повтор в R5), PR #4
- 05:54 S3: ок, PR #5
- 06:09 S4: ок, PR #6
- 06:31 S5: ок, PR #7
- 06:42 R5: закрыт с долгом (живой прогон: у очереди `input` 0–1 консьюмер, TPU молчит), PR #8
- 07:00 S6: ок, PR #9
- 07:14 S7: ок, PR #10
- 07:25 S8: ок, PR #11
- 07:44 S9: ок, PR #12
- 08:04 S10: закрыт с долгом (recompute теряет модели extra: нет колонки артефактов extra), PR #13
- 08:18 R10: ок, PR #14
- 08:34 S11: ок, PR #15
- 08:46 S12: ок, PR #16
- 08:58 S13: ок, PR #17
- 09:07 S14: ок, PR #18
- 09:16 S15: закрыт с долгом (docker build: демон Docker не запущен), PR #19
- 09:28 R15: ок, PR #20
### итог ночи (2026-10-24)
- Очередь раздела 16 пройдена целиком (04:37–09:30): S0–S15, R5, R10, R15, PR #1–#20, все squash в main; R10 закрыт в 08:18 (цель была 10:00).
- CI: все 20 PR зелёные на ubuntu и windows; PR #1 на ubuntu был красный (`safewatch stop` ждал зомби), починен PR #2.
- Гейт на main после каждого шага зелёный; финальный: 352 pytest, 25 vitest, сверка контракта 480 элементов; tech.md v4.
- GAP: все перенесены в tech.md (v2 → 6.8, v3 → 6.9, v4 → 6.10), в `## open` строк GAP нет.
- Живые прогоны LinQ: 2 (S2, R5), оба без ответа TPU: у очереди `input` 0–1 консьюмер вместо 16, причина в среде; конвейер проверен на `SAFEWATCH_FAKE=1`.
- Долги: живой прогон LinQ; `docker build` (демон Docker не запущен); 10 долгов R15 (kernel Jupyter не закрывается, осиротевший удалённый воркер, HTML Jupyter → `unreachable`, сцена `demo` теряет трек при падении, демо-события в ленте, упрощённый `explain`, загрузка на диск до проверки роли, `_freshness` в event loop, `eval` вторым процессом, очередь доставок в памяти).
- Происшествие: тест S7 открывал настоящую `data/app/safewatch.db`, тест S9 записал туда строки (удалены точечно); R10 поставил autouse `no_real_data`, гейт `data/app` больше не трогает.
- Утром владельцу: спросить Матвея или организаторов про консьюмеров очереди `input`, потом `uv run poe live`; остановить idle kernels `e03fcb40…`, `475771bb…` и kernel `doctor`; удалить `D:\npm1.log`, `D:\scratch_fe.log`; запустить Docker Desktop и `docker compose build`; положить заводские видео в `data/videos/`.
- Результат: main `6a65f377`, запуск `uv run safewatch serve --seed` (README, раздел «Приложение SafeWatch»), контракт фронта `contract/openapi.json`.
