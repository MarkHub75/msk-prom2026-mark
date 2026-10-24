# checkpoint-demo: демонстрационный контур SafeWatch

Stateful-мок критического пути (REST + WS), режиссёр сценария, синтетические кадры и smoke для мока и настоящего бэкенда. Показ проходит без обученной CV-модели и без готового бэкенда. В 10:00 одна команда скажет, готов ли бэкенд: `.\smoke.cmd --target real`.

Запуск, сбои на показе, замена кадров: [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md). Расхождения и допущения: [GAPS.md](GAPS.md).

## 0. Аудит (05:10–05:25, main `d4709bea`, S0 и S1 закрыты)

| Что есть | Что даёт | Почему мало для демо |
| --- | --- | --- |
| Prism (`npm run mock`, порт 4010) | ответы-примеры по `contract/openapi.json` | stateless: POST не меняет последующие GET, статусы не двигаются, нет связи с WS |
| `frontend/mock/ws-mock.mjs` (4011) | `hello` и по кругу `ws-examples.json` раз в 3 с всем ролям | события из ниоткуда, `notification` уходит всем ролям, не связан с REST |
| `seed_demo` (бэкенд, S0) | 4 сектора, 8 камер, 7 зон, 240 исторических событий | только запись в базу; экраны операторов и мастера на бэкенде — 501 до S6–S8 |
| фейк бэкенда (`SAFEWATCH_FAKE=1`, `FakeRemoteShell`, сцена `demo`) | детекции без LinQ | нужен S2 (загрузка), S5 (эпизоды), S6 (эфир), S7 (действия); сейчас 501 |

Вывод: полного сценария не даёт ни один инструмент. Мок повторяет мир сида (те же секторы, камеры, зоны, тексты из `texts.py`) и историю сцены `demo`. Сид и фейк бэкенда не дублирует: smoke real использует их через API.

Контрактная проверка **пройдена для мока**: каждый ответ REST проверен по `contract/openapi.json`, каждое WS-сообщение — по `contract/ws.schema.json` (Ajv, JSON Schema 2020-12). Контракт 1.0.0 с 05:10 не менялся.

## 1. Что готово

| Часть | Файл | Состояние |
| --- | --- | --- |
| stateful-мок REST 4010 + WS 4011/ws, CORS для localhost/127.0.0.1 | `src/server.mjs`, `src/state.mjs`, `src/world.mjs` | готово, smoke 30/30 |
| переходы 8.6, `allowed_actions` по роли, журнал `EventAction`, красный confirm = 2 записи | `src/state.mjs` | готово |
| состояния камер и секторов 8.9, лента 8.8, уведомления по `audience` | `src/state.mjs` | готово (без эфира: GAPS A1) |
| автоэскалация 8.7 за флагом `--escalation` | `src/state.mjs` | проверена на подменённых часах: 44,9 с — нет, 45,0 с — да |
| мир сида: 4 сектора, 8 камер, 7 зон, 18 исторических событий (терминальные, полная история) | `src/world.mjs` | готово |
| режиссёр `next / reset / status / ws-drop / fault` | `bin/demo.mjs`, `demo.cmd` | готово |
| синтетические кадры с рамкой по bbox | `evidence/` | готово |
| smoke `--target mock / real` | `bin/smoke.mjs`, `smoke.cmd` | готово |
| фронт main (S1) против мока в браузере | — | проверено: CORS, meta, `/admin/cameras`, WS из origin 5173 |

## 2. Запуск

```powershell
cd tools\checkpoint-demo
.\mock.cmd                       # окно 1: мок (сам сделает npm install при первом запуске)
cd ..\..\frontend; npm run dev:mock   # окно 2: фронт против мока
.\demo.cmd next                  # окно 3: жёлтое, потом ещё раз — красное
.\smoke.cmd --target mock        # проверка контура: код 0
```

## 3. Эндпоинты мока

| Маршрут | Ответ |
| --- | --- |
| `GET /api/health`, `/api/meta` | `Health`, `Meta` (`fake=true`, `running` и `fall` — `active`) |
| `GET /api/operator/dashboard`, `/api/operator/feed` | `OperatorDashboard`, `list[EventSummary]` |
| `GET /api/sectors/{id}/view` | `SectorView` (плитки камер без эфира) |
| `GET /api/events/{id}` | `EventDetail`, `allowed_actions` по `X-Role` |
| `POST /api/events/{id}/actions` | `EventDetail`; 400/403/404/409/422 по 6.4 |
| `GET /api/master/inbox`, `/api/master/shift` | `MasterInbox`, `ShiftSummary` |
| `GET /api/evidence/{id}/image` | `image/jpeg` (1 — жёлтый кадр, 2 — красный), 404 при `fault evidence-404` |
| `GET /api/events`, `/api/journal/facets` | `EventPage` с фильтрами `EventFilter`, `JournalFacets` |
| `GET /api/sectors`, `/api/cameras`, `/api/cameras/{id}`, `/api/admin/cameras` | данные мира (экран S1 фронта) |
| остальные маршруты контракта | 501 `not_implemented`, тело `ApiError` |
| `WS /ws?role=` | `hello`; неизвестная роль → close 4400; `event.created/updated`, `notification` (только `audience`), `camera.state`, `sector.state` |
| `/__demo/*` | служебные маршруты режиссёра, вне контракта |

## 4. Сценарии и результаты smoke (24.10, 05:27)

Позитив: health → meta → dashboard → WS hello (operator, master) → жёлтое → `event.created` + `notification` у operator, у master нет → карточка и view сектора → confirm → красное → takeover-уведомление (siren) только оператору → у мастера нет confirm → «Подтверждаю» (`X-Actor` «Иван Петров») → `sent_to_master` → уведомление мастеру (chime) → входящие мастера → accept → resolve с комментарием → история `published → confirmed → sent_to_master → master_accepted → resolved` → событие в `/api/events`.
Негатив: неизвестная `X-Role` → 400; WS с неизвестной ролью → 4400; неверный переход → 409; чужая роль → 403; `X-Actor` длиннее 60 → 422; resolve без комментария → 422; кадр 404 при fault; fault 500 → `ApiError`; разрыв WS → новое подключение получает `hello`, REST совпадает с ожидаемым. Последний шаг — сводка проверок по схемам.

| Таргет | Итог | Код |
| --- | --- | --- |
| mock | PASS 30 · FAIL 0 · SKIP 0; проверено по схемам 26 ответов и 32 WS-сообщения | 0 |
| real (main `d4709bea`, S1, `SAFEWATCH_FAKE=1 serve --seed`) | PASS 7 · FAIL 0 · SKIP 21: health, WS hello, `X-Role` 400, WS 4400, `X-Actor` 422, переподключение, схемы — PASS; meta без сценариев (S5), dashboard 501 (S6), загрузка видео 501 (S2), actions 501 (S7) — SKIP | 3 (не готов) |

Коды smoke: 0 — готов к показу, 1 — FAIL, 3 — FAIL нет, но есть SKIP. Smoke real не грузит видео, если бэкенд на настоящем LinQ (`fake=false`).

## 5. Для Codex (интеграция фронта)

- Мок: `VITE_API_BASE=http://127.0.0.1:4010`, `VITE_WS_URL=ws://127.0.0.1:4011/ws` — это `frontend/.env.mock` как есть, `npm run dev:mock`. Не запускать вместе с `npm run mock`.
- Бэкенд: `npm run dev` (прокси Vite → 8000). У бэкенда нет CORS (GAPS G4).
- `Evidence.url` относительный: добавлять `VITE_API_BASE` (G5).
- `view` слать, только если он есть в `allowed_actions`, иначе 409 (G6).
- Кадр события есть только в `episode.evidence`. У живых событий мока `episode` заполнен синтетикой, у исторических — `null` (G1). Экран должен переживать `episode: null`.
- Уведомление с `takeover: true` открывает `/events/:id?takeover=1`. `notification.id`: `<id>-yellow`, `<id>-red`, `<id>-master`.
- После `demo reset` мок рвёт WS: фронт переподключается и перечитывает экран по REST (как при коде 1013).
- Тексты ошибок показывать из `ApiError.message` как есть.
- Полный список расхождений: [GAPS.md](GAPS.md).

## 6. Ограничения

- В моке нет эфира, видео, HUD, превью, калибровки и статистики: `broadcast`, `preview_url`, `video_id` — `null`. Камеры «наблюдаемы» по флагу (GAPS A1).
- Все события и кадры синтетические и помечены: `is_demo=true`, `provenance.fake=true`, в «Почему» — «Синтетическое демо-событие, не результат нейросети», на кадре — «СИНТЕТИЧЕСКИЙ КАДР». Рамка на кадре — ручная разметка.
- Показателей LinQ, FPS и точности здесь нет и быть не должно.
- Smoke real на 05:27 доходит только до S1. Полный прогон станет возможен после S2, S5, S6, S7, S8. На бэкенде жёлтое закрывается само примерно через 4 с после публикации (G3): smoke подтверждает его сразу, ведущему на показе тоже нужно успеть.
- Мок хранит состояние в памяти: перезапуск = `reset`.
