# progress.md

- state: S6 закрыт, следующий S7
- tech.md: v2
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
- долг: R5, живой прогон (критерий 17 S2, повтор), TPU снова не ответил за 120 с (`TimeoutError: no TPU reply for 1 task(s) in 120 s, unmatched replies 0`, задача `retry_wait`/`remote_error`); `linq_tpu.py ping` очереди `input`: до прогона consumers 1, messages 0; на старте воркера consumers 0, messages 1; после — consumers 1, messages 0 (у TPU-сервиса должно быть около 16). Путь до TPU совпадает со smoke 21b24555, причина в среде; кадр/с (цель около 20), RTT и эпизоды на LinQ не замерены. Повтор — когда ping покажет около 16 консьюмеров.
- владелец: спросить Матвея или организаторов, почему у очереди `input` брокера 0–1 консьюмер вместо 16 (TPU молчит с ~05:40); в Jupyter открыт `examples/Untitled.ipynb`, он может читать общую очередь.
- владелец: остановить в Jupyter idle kernels без ноутбука от наших прогонов `e03fcb40…` (05:39, S2) и `475771bb…` (06:36, R5), плюс kernel от `safewatch doctor` R5; удаление на общем аккаунте заблокировала защита Claude Code.
- владелец: удалить мусорные логи вне репо `D:\npm1.log` и `D:\scratch_fe.log` (удаление заблокировала защита Claude Code).
- R10: `JupyterShell` не закрывает kernel: каждый процесс (сервер, doctor, живой тест) оставляет один idle kernel на общем аккаунте; `_drop` закрывает его только при ошибке. Нужен `close()` из lifespan и doctor (расширение `RemoteShell`, строка `GAP`).
- R10: S9 — HUD берёт порог бега из `settings.scenarios.running`, правило — `defaults | camera_rules`; с правилами камеры подпись и правило разойдутся: передать действующие параметры `running` (и `speed_m_s`) в `build_hud`.
- R10: `video_recompute` не проверяет уже поставленную задачу `recompute`: повторные клики ставят N задач.
- R10: прогон, прерванный остановкой сервера, оставляет удалённый `video_worker.py` живым; повтор с тем же `<out>` запустит второй воркер в тот же файл (`# sw:start` не гасит старый pid).
- R10: `backend_check`, Jupyter отдал HTML через `JupyterError`: сейчас `unreachable`, по 6.2 — `bad_answer`; вживую не воспроизвелось (R5: `ok`, 2 из 2 программ).
- R10: сцена `demo` теряет id трекера в момент падения (падение подтверждается веткой «лежит неподвижно», бег закрывается `track_lost_timeout`); проверить на заводском видео, когда оно появится (в R5 заводских нет).
- GAP: S6, `services` вне 6.2: `PRIORITY = {"red_pending": 3, "yellow_pending": 2, "open": 1, "terminal": 0}` и `_priority(level, status)`; синглтоны `_camera_seen: dict[int, CameraState]`, `_sector_seen: dict[int, SectorState]`, `_preview_cache: dict[int, tuple[datetime, bytes]]` (сбрасывает фикстура `conn`); помощники `_broadcast`, `_broadcast_by_id`, `_broadcast_insert`, `_stop_playing`, `_autostart`, `_play`, `_summary`, `_event_summary`, `_system_action`, `_operator_alert`, `_camera_state`, `_sector_state`, `_sector_states`, `_feed`; `broadcast_tick` возвращает число записанных действий (`published`, `level_escalated`, `auto_finished`); `Notification.id = "e<event>:published|escalated"`.
- GAP: S6, `store`: `broadcast(id)`, `camera_broadcast(camera_id)` (играющий эфир, иначе последний), `latest_broadcasts()`, `playing_broadcasts()`, `broadcast_update`, `last_ready_video(camera_id)`, `event(id)` (с `camera_name`, `sector_name`, `zone_name`), `broadcast_events(broadcast_id, cycle)`, `event_update`, `feed(closed_after, sector_id=None)`, `camera_state_rows()` (входы правил 8.9 всех камер одним запросом).
- GAP: S6, `texts.py`: `STATE_NORMAL = "Норма"`, `SECTOR_NO_OBSERVATION = "Нет наблюдения: {n} из {total} камер"`, `SECTOR_EMPTY = "В секторе нет камер"`, `NO_READY_VIDEO`, `PREVIEW_NOT_FOUND`, `NOT_CONFIRMED_SUFFIX`; `reason_text` камеры и сектора: red/yellow — `LEVEL_TITLES`, normal — «Норма».
- GAP: S6, эфир: `broadcast_get` и поле `broadcast` у `CameraTile`, `CameraLiveView`, `CameraSetupView` — играющий эфир камеры, иначе последний любого статуса, иначе `null`; `broadcast_start` с чужим или несуществующим `video_id` → 404 `not_found`, `ready` без `active_analysis_id` → 409 `video_not_ready`; остановленный при старте эфир шлёт свой `broadcast.state` (`stopped`); `broadcast_stop` без играющего эфира → 204 без сообщения; `camera_delete` шлёт `broadcast.state` остановленного эфира (закрыта заметка R10 от S1).
- GAP: S6, лента: «терминальные за последние `recent_closed_min`» — по времени последнего действия события (`max(event_actions.at)`); жёлтое, опубликованное уже закончившимся (догоняющий тик), сразу получает `ended_at` и по 8.5 дословно не получает `auto_finished`.
- GAP: S6, превью: кадр `round(position_ms / 1000 × fps)` играющего эфира, иначе кадр 0 последнего `ready` видео; JPEG `evidence.jpeg_quality`, ширина `preview.max_width`; `CameraTile.preview_url` есть при `videos_count > 0`; `CameraState.freshness_ms = None` до S11.
- GAP: S6, `worker`: `_jobs(stop, idle_s)` и `_broadcasts(stop, tick_s)` в `asyncio.TaskGroup`, паузы через `asyncio.sleep` (остановка в пределах одного периода); исключение тика — лог `broadcast tick`, цикл продолжается.
- GAP: S6, фронт: `WsNotification` в `src/api/ws.ts` (нагрузка `notification`: WS-типов нет в openapi); `playSound(kind)` возвращает функцию остановки, `soundBlocked()` и `unlockSound()` в `components/sound.ts` (кнопка «Включить звук» в шапке); `STATE_ICON` из `components/SectorTile.tsx`; `Toasts` и `TakeoverOverlay` без пропсов, сами слушают `useWs`; `BroadcastPanel` внутри `CameraSetup.tsx`.
- R10: S8 — уведомление мастеру на эскалацию уровня события в `sent_to_master`/`master_accepted` (8.8, строка 4) `broadcast_tick` не шлёт: в S6 действий оператора нет.
- R10: `system_view.latency` (`notify_delay_s`, `publish_lag_ms`) всё ещё нули: критерия ни в одном слайсе до S11 нет.
- R10: лента и состояния камер считают демо-события: жёлтые `confirmed` сида открыты и попадают в ленту оператора с приоритетом 1 (до `feed.limit`).
- R10: каждый компонент с `useWs` (шапка, `Toasts`, `TakeoverOverlay`, экран) открывает свой WebSocket: у оператора 4 соединения на вкладку.

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
