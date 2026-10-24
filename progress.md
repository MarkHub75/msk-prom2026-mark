# progress.md

- state: S14 закрыт, следующий S15
- tech.md: v3
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
- R15: `JupyterShell` не закрывает kernel: каждый процесс (сервер, doctor, живой тест) оставляет один idle kernel на общем аккаунте; `_drop` закрывает его только при ошибке. Нужен `close()` из lifespan и doctor (расширение `RemoteShell`, строка `GAP`). Перенесено из R10: проверка только вживую, а в R10 живых прогонов нет.
- R15: прогон, прерванный остановкой сервера, оставляет удалённый `video_worker.py` живым; повтор с тем же `<out>` запустит второй воркер в тот же файл (`# sw:start` не гасит старый pid). Перенесено из R10: правка проверяется только вживую.
- R15: `backend_check`, Jupyter отдал HTML через `JupyterError`: сейчас `unreachable`, по 6.2 — `bad_answer`; вживую не воспроизвелось (R5: `ok`, 2 из 2 программ). Перенесено из R10: нет воспроизведения.
- R15: сцена `demo` теряет id трекера в момент падения (падение подтверждается веткой «лежит неподвижно», бег закрывается `track_lost_timeout`); проверить на заводском видео, когда оно появится (заводских видео всё ещё нет).
- R15: `system_view.latency` (`notify_delay_s`, `publish_lag_ms`) всё ещё нули; в критериях S11 их нет (S11 — свежесть и интервалы), оставлено ревью.
- R15: лента и состояния камер считают демо-события: жёлтые `confirmed` сида открыты и попадают в ленту оператора с приоритетом 1 (до `feed.limit`); решать вместе с флагом демо в S12–S13.
- R15: S10 — HUD (`build_hud`) подписывает только наблюдения субъекта `track:<id>`: `pair:`/`zone:` (proximity) и `fire` на кадре не видны; 8.2 п. 8 просит подпись на каждое `P`. Перенесено: `analysis/hud.py` — файл S11, но в критериях S11 подписей HUD нет, не сделано.
- R15: S10 — `explain` новых плагинов: одна строка правила + `why_common`; без единицы дистанции в `explain` зоны proximity (берётся `reason_text`).
- R15: загрузка большого файла целиком ложится на диск до проверки роли и размера (Starlette `UploadFile`, с R5); `hub.Client.dropped` не читается — в критериях S11 потребителя нет, решить в R15 (удалить или показать на экране IT).
- R15: S11 — `services._freshness` читает `hud.jsonl` анализа один раз в потоке event loop (потом кэш `_frames_ts`); для длинных видео перенести чтение в `to_thread`.
- GAP: S11, `ObservabilityGap` — полуинтервал `[start_ms, end_ms)`; `stale` — между соседними кадрами анализа (`start_ms` кадр до разрыва, `end_ms` кадр после; начало и хвост видео не проверяются, `min_duration_s` к `stale` не применяется: иначе 2001 мс не считался бы); серия `dark`/`obstructed` длится до первого хорошего сэмпла или до `duration_ms`; список по `(start_ms, stale < dark < obstructed)`, интервалы `dark` и `obstructed` могут перекрываться, камера берёт первый содержащий позицию.
- GAP: S11, `observability.Luma = tuple[int, float, float]` (`ts_ms, mean, std`), помощник `_runs`; `media.LUMA_WIDTH = 160`, уменьшение `INTER_NEAREST` (усреднение `INTER_AREA` гасит разброс шума и текстуры: тестовое видео с шумом становилось `obstructed`); `sample_luma` нечитаемого файла → `[]`.
- GAP: S11, `analyze`: кадры внутри `dark`/`obstructed` не дают наблюдений (`U` у всех субъектов, 8.10); `stale` отдельно не обрабатывается — менеджер эпизодов сам добавляет разрыв `ts − ts прошлого кадра` в `uncertain_ms` и проверяет `lost_timeout_s`.
- GAP: S11, `store.camera_state_rows()` добавляет `position_ms`, `analysis_id`, `gaps_json`, `hud_path` играющего эфира (`LEFT JOIN`); `services._freshness(analysis_id, hud_path, pos) -> int | None` (до первого кадра анализа — `None`), синглтон `_frames_ts: dict[int, list[int]]` (сбрасывает фикстура `conn`).
- GAP: S11, WS `camera.state` уходит только при смене состояния без учёта `freshness_ms` (`_camera_seen` хранит копию с `freshness_ms=None`): свежесть меняется каждый тик, её читают через REST (`system_view`, плитки).
- GAP: S12, `EventSummary.evidence_url: str | None = None` — `/api/evidence/<id>/image` кадра `confirm` эпизода (демо и событие без кадра — `None`), миниатюра журнала; `store._EVENTS` добавляет `LEFT JOIN evidence ev ... kind = 'confirm'` (`evidence_id`, `evidence_sha256`); поле добавлено в `contract/openapi.json` и `ws.schema.json`.
- GAP: S12, журнал: период и порядок по `started_at` (`date_from ≤ started_at < date_to`, как статистика 8.13), страница `started_at DESC, id DESC`; курсор — `str(id)` последнего события страницы (не цифры → 422, поле `cursor`); фильтр `status=superseded` не отменяет скрытие (нужен `include_superseded=true`); `date_from`/`date_to` без пояса — UTC; 422 — `ValidationFailed(texts.FILTER_INVALID.format(field=...), field=...)`, поля `limit`, `q`, `date_from`, `cursor`.
- GAP: S12, `store` вне 6.x: `journal_where(equal, date_from, date_to, q, include_demo, include_superseded) -> (sql, args)`, `journal(where, after_id, limit) -> (rows, total)`, `journal_actions(event_ids)` (один запрос через `json_each`), `all_zones()`; `services`: `_utc(dt)`, `_journal_where(f)` (проверки 9 и экранирование `q`), `_msk(dt)`.
- GAP: S12, CSV: `events_export_csv` проверяет фильтр целиком, но `limit` и `cursor` не применяет: до `journal.export_max_rows` строк в порядке журнала; заголовки `texts.CSV_COLUMNS`, строки `\r\n`; время в `timezone` как `YYYY-MM-DD HH:MM:SS`; сценарий — `title` события; уровень, статус, вердикт — русские названия (`texts.VERDICT_TITLES`); `texts.YES`/`texts.NO`; длительность с одной цифрой и запятой; sha256 — кадр `confirm`; история `<время> <роль>: <действие>[ (<комментарий>)]` через «; », роль — `texts.ROLE_TITLES` или «система», действие — `texts.ACTION_TITLES: dict[LogAction, str]`.
- GAP: S12, `journal_facets`: сценарии — `texts.SCENARIO_TITLES`, уровни и статусы — все значения, секторы — `store.sectors()`, камеры — живые, зоны — живые зоны живых камер с названием `<камера> · <зона>`; `FacetItem.id = str(id)`.
- GAP: S12, фронт: `FiltersBar.tsx` экспортирует тип `JournalFilter` (query `GET /api/events`); дата фильтра — день МСК (полночь +03:00), `date_to` не включается; «Показать ещё» дозагружает по `next_cursor`; «Экспорт CSV» — ссылка с query фильтра; строка открывает `/events/:id` (для `ohs` `allowed_actions` пуст — только чтение).
- GAP: S13, `ohs_stats_view`: `date_to` по умолчанию `now`, `date_from` — `date_to − stats.default_days` дней, время без пояса — UTC; период `date_from ≤ started_at < date_to`; `date_from > date_to` (после умолчаний) → 422 `ValidationFailed(texts.PERIOD_INVALID, field="date_from")`, `weeks` вне 1..52 → то же с `field="weeks"`; `sector_id`/`camera_id` — через `store.journal_where`; `by_status`/`by_scenario`/`by_sector`/`by_camera` — `_count_rows` (по убыванию `count`); `by_day` — каждый день МСК периода с нулями; `by_hour` — 24 строки `key="00".."23"`, `title="08:00"`; `by_shift` — смены `shifts` по порядку с нулями (окно `_shift_window`).
- GAP: S13, реакция: первое действие с `actor_role = operator` и `action ∈ OPERATOR_DECISIONS` (`viewed` не считается), `pending` — нетерминальные события без него; `master_accept_s` — от последней передачи до первого `master_accepted`, передача — `HANDOVERS = {sent_to_master, timeout_escalated}` (эскалация по таймауту тоже передаёт мастеру), `pending` — статус `sent_to_master`; `master_resolve_s` — от `master_accepted` до `resolved`, `pending` — статус `master_accepted`; ранг `x[ceil(round(p·n, 9)) − 1]` (округление гасит ошибку `0,95·n` в float).
- GAP: S13, `management_view`: окно `weeks` — с понедельника МСК `weeks − 1` недель назад по текущую неделю; `top_sectors` — все секторы `store.sectors()` (демо-секторы скрыты при `include_demo=false`), `confirmed` по `operator_verdict` за последние `trend_weeks` недель включая текущую, `cameras` — живые камеры сектора, порядок: `per_camera` по убыванию, `None` в конце, затем `title`; `top_scenarios` — `_count_rows` за окно `weeks`; тренд: в тексте `round(|change_pct|)`, `0` → «без изменений», `previous = 0` → `change_pct = None`, текст `texts.TREND_NO_DATA` без оговорки.
- GAP: S13, вне 6.x: `store.events_where(where)` (все события фильтра `journal_where`, по `started_at, id`); `services`: `OPERATOR_DECISIONS`, `HANDOVERS`, `_percentiles(values, pending)`, `_reactions(events)`, `_fixed_rows(pairs, keyed)`, `_add_levels(row, e)`, `_share(part, whole)`, `_trend(previous, recent, weeks)`; `texts`: `PERIOD_INVALID`, `TREND_CAVEAT`, `TREND_LESS`, `TREND_MORE`, `TREND_SAME`, `TREND_NO_DATA`, `weeks_span(n)` («4 недели к 4 неделям», «1 неделя к 1 неделе», «5 недель к 5 неделям»).
- GAP: S13, фронт: `recharts@2.15.4` в `frontend/package.json`; графики фиксированного размера 640×240 без `ResponsiveContainer` (ему нужен `ResizeObserver`, в jsdom его нет); `BarChartCard({title, data: {name, value}[]})`, `StackedDaysCard({title, days})`, `LineChartCard({title, weeks})`, `PercentilesCard({title, value})`; фильтры сектора и камеры экрана статистики — из `/api/journal/facets`; `test_api_skeleton.py::test_unbuilt_route_returns_501` подменяет `services.management_view` заглушкой `NotImplementedError` (с S13 построены все маршруты).
- R15: S13 — `App.test.tsx::stub_screens_show_slice` стал пустым циклом (заглушек в `nav.ts` больше нет); решить: удалить тест вместе со строками трассировки 6.7 или оставить как защиту от новой заглушки.
- GAP: S14, `evaluate`: `OutcomeKind = Literal["tp", "fn", "fp", "duplicate", "late"]`, `Outcome = tuple[str, OutcomeKind, float | None]` (сценарий, исход, задержка tp в с), `match_episodes(expected: list[ExpectedEvent], episodes: list[EpisodeDraft], deadline_s: float) -> list[Outcome]` (одно видео: tp на пару, fn на эталон без пары, исход на каждый несопоставленный эпизод), `report_md(report: EvalReport) -> str`; границы сравниваются в целых мс (`round(s × 1000)` против `confirm_ms`): ровно `deadline_s` — tp без ошибки float.
- GAP: S14, сопоставление: несопоставленный эпизод внутри эталона, у которого уже есть пара, — `duplicates` (даже позже дедлайна); внутри только эталонов без пары — `late`; `episodes = tp + fp + duplicates + late`, `expected = tp + fn`; строки — сценарии эталонов и эпизодов по алфавиту, затем `*`; `f1 = None`, если precision или recall `None` или их сумма 0; `fp_per_hour` — на сумму длительностей всех видео разметки (одна для всех строк), 0 часов → `None`; `delay_s = _percentiles(задержки tp, 0)`.
- GAP: S14, `eval_run`: синхронный, `asyncio.run` на каждое видео; порядок: файл разметки (`NotFound`) → YAML и схема `EvalLabels` (`ValidationFailed`, `field` — путь pydantic через точку, `yaml` при ошибке разбора, `labels` у пустого файла) → `start_s < end_s` (`field="videos.<i>.expected.<j>"`) → все файлы видео (относительный путь — от корня репо `config.ROOT`) и `camera_id` (`NotFound`) до инференса; видео в `videos` не пишется, только строки `artifacts`; нечитаемое видео → `UnsupportedVideo` (CLI exit 2); любая `InferenceError`, в том числе pose, → exit 4 (отката на анализ без pose, как у задачи, нет); `--out DIR` — отчёт прямо в `DIR`, без него `data_dir/eval/<YYYYMMDD-HHMMSS>` по `clock.now()` в UTC; CLI печатает путь и `report.md`, ошибки — в stderr (`InferenceError` как `<code>: <message>`).
- GAP: S14, вне 6.x: `services._infer(job_id: int | None, ..., video: sqlite3.Row | dict[str, Any])` (`None` — без стадии и прогресса задачи), `_analysis_config(video, camera_id: int | None, extra_ids) -> AnalysisConfig` (общий для `_analyze` и оценки; без камеры: без калибровки и зон, правила `_rules(0, [], metas)`), `_sha256(path)` (и `video_import`), `_eval_labels(path) -> EvalLabels`, `_eval_episodes(path, camera_id) -> (episodes, duration_ms)`, `_eval_rows(outcomes, hours) -> list[EvalMetrics]`; `cli.evaluate(labels, out) -> int`; `texts`: `EVAL_LABELS_INVALID`, `EVAL_INTERVAL_INVALID`, `EVAL_TITLE`, `EVAL_COLUMNS`, `EVAL_FOOTNOTE`.
- R15: S14 — CLI `eval` при запущенном сервере пишет `artifacts` в ту же базу вторым процессом (WAL; `database is locked` не проверялся); `eval_run` зовёт `asyncio.run` и из работающего event loop (API) не вызывается.

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
