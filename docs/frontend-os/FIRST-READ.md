# SafeWatch: первый проход через Frontend Hackathon OS

Первый проход начат штатным интерактивным контроллером OS 4.0. `present-concepts` выполнен: текущий этап — `HUMAN_CONCEPT_REVIEW`, требуется настоящий человеческий отзыв по конкретным изображениям. Продуктовая реализация ещё не начата. Это рабочий статус, а не отчёт о готовом фронтенде.

## Изоляция

- Ветка: `codex/safewatch-os-first-pass`.
- Worktree: `/mnt/d/templates/msk-promhack/safewatch-os-first-pass`.
- Основа: `origin/main`, `b3c52b276950250ab0bcca44c8ec457e996167bc`.
- Основное дерево команды: `/mnt/d/templates/msk-promhack/msk-prom2026-mark`; его файлы не изменялись.
- Sparse checkout исключает только тяжёлый `Deep-Research/`; исследования читаются из дерева команды.
- `FRONTEND_HANDOFF_v1.md` скопирован отдельно из локального незакоммиченного файла, не заменяет настоящий OpenAPI.

## Реальный запуск OS

OS: `/mnt/d/templates/frontend-hackathon-os`, HEAD `d67a9627e9c9c2ee16a6e51e615c63597672ede0`. Архитектура 4.0, Python package 0.1.0, HRE renderer 1.1.0; версии manifest/decision 1.0.0.

Активный run: `/mnt/d/templates/frontend-hackathon-os/production/runs/safewatch-20261024-first-pass-r2`.

Первоначальный `safewatch-20261024-first-pass` сохранён после реального сбоя: `concept-import` принял объект с промптами, затем writer отчёта упал, ожидая строку (`TypeError` в `report.py`). В соответствии с documented recovery создан новый run; настоящие исходные контексты, изображения и raw evidence импортированы повторно, поле prompt приведено к строковому представлению с сохранением исходного JSON. SQLite и root-bound store не копировались, повторной генерации изображений не было. `evidence/recovery.json` фиксирует происхождение. Все 12 PNG совпадают побайтно, что независимо проверено reviewer. Код OS не изменялся.

Использован поддерживаемый режим `interactive-codex` с `creative-freedom` и `interactive-native`. `init`, `next`, `drive`, регистрация reference/explosion receipts выполнены настоящим CLI. `drive` сообщает записанную стадию; автономного OS4 worker в этой версии нет. Код OS и существующее чужое изменение orchestrator не редактировались.

Из корня OS:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=production python3 -B -m hackathon_os.cli --run production/runs/safewatch-20261024-first-pass-r2 next
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=production python3 -B -m hackathon_os.cli --run production/runs/safewatch-20261024-first-pass-r2 status
```

Preflight после указания существующего Playwright/Chromium: `ready=true`; настоящая страница отрендерена. Browser plugin отсутствует, используется установленный Playwright 1.64.1 и Chromium 156.0.8078.4. Первоначальная ошибка разрешения `playwright` диагностирована и исправлена runtime-конфигом, без модификации OS.

## Источники продукта

`tech.md`, `docs/brief.md`, `INDEX.md`, `FRONTEND_HANDOFF_v1.md` изучены. На указанной исходной ревизии нет `contract/openapi.json`, `contract/ws.schema.json`, `contract/ws-examples.json`, `frontend/` или работающего backend/mock. JSON-контракты и generated types не выдумываются. Перед интеграцией нужно повторно проверить свежую удалённую ревизию, не перезаписывая дерево команды.

Целевые сценарии: диспетчер → сектор → камера → событие → серверное действие → поручение мастеру → принятие → отчёт. Incident Focus сохраняет договорённую композицию: доказательный кадр сверху слева, состояние/действия справа, воспроизведение записи с HUD снизу. Мобильный мастер получает отдельную композицию под работу одной рукой.

Все business copy, статусы, уровни, `allowed_actions` и переходы принадлежат backend. При воспроизведении записи нельзя заявлять live CCTV. HUD относится только к правильному кадру. Отсутствие наблюдения не означает безопасность. Синтетические fixtures остаются явно обозначенными.

## Визуальные доказательства и human checkpoints

В `run/evidence/reference-expedition/` сохранены 12 конкретных источников, исходные изображения, реальные браузерные captures и raw tool responses. `references.json` связывает механизм с тремя направлениями продукта и указывает, что отвергнуто. Это ограниченная завершённая экспедиция, без повторного масштабного Deep Research.

Шесть независимых image directions созданы: `signal-post`, `response-route`, `sector-atlas`, `evidence-desk`, `shift-ribbon`, `video-switchboard`. У каждого два настоящих raster frame, полные промпты, raw ответы генерации, independent-context и reference receipts. Инструмент `image_gen.imagegen` работал реально; точную модель он не сообщил (`unknown`). Concept images — иллюстрации, а не браузерные скриншоты реализации. После `present-concepts` контроллер остановился на `HUMAN_CONCEPT_REVIEW`. Реальная человеческая обратная связь регистрируется через `human-feedback`; её нельзя синтезировать от имени пользователя.

После concept feedback штатный цикл ведёт к компонентной экспедиции и рабочим продуктовым интерпретациям, затем `HUMAN_PRODUCT_REVIEW`. Дизайн окончательно не заморожен.

## Текущий пакет HRE

[Открыть HRE v3](http://127.0.0.1:8196/human_review/renderer/v1.1/index.html?manifest=../../../runs/safewatch-20261024-first-pass-r2/concept-review/v3/manifest.json).

Пакет: `run/concept-review/v3/`, review `safewatch-concepts`, revision 3, manifest SHA256 `fabd34e7ee30d4802c8aefa4743a63b0266e4635aa84e8f699c29dea79d799f3`. Настоящий неизменённый HRE renderer 1.1.0, существующие manifest/decision schemas 1.0.0 и штатный `validate-package.mjs`. В пакете 6 направлений, 12 исходных concept images, визуальные референсы, промпты, raw responses, независимая критика и явная проверка отсутствующих контрактов. Renderer и каждый artifact проверяют SHA256. Варианты reduced motion, recordings и baseline остаются MISSING; никакой подстановки нет. Логический concept canvas не выдаётся за browser viewport.

`package-concepts.py` только авторит данные существующего HRE manifest, не содержит renderer или replacement review engine. Это поддерживаемый image-concept checkpoint, не автоматический product `completed-change` lifecycle: продуктовой source revision пока нет. Пакеты v1/v2 сохранены как отклонённые schema-validation черновики; ни один не используется как current review. Человеческих решений в пакет не вложено, все 6 UNREVIEWED.

Штатная валидация: `run/evidence/hre-package-validation-v3.json` — PASS. Проверка в настоящем браузере: `run/evidence/hre-browser-v3/review-qa.json` — PASS, 12 изображений декодированы; проверены original-pixel inspection, Escape, сохранение MISSING для отсутствующих reduced-motion/recordings, отсутствие preselected votes и мобильный горизонтальный scroll. Окна HRE проверены на 1440×900, 1280×800 и 390×844. Файлы `hre-ui-*.png` показывают сам HRE, не работающий SafeWatch.

Независимое заключение: `run/evidence/concept-independent-review.json` и `run/evidence/REPORT.txt`. Рекомендация для обсуждения: `evidence-desk` — ясное различие закреплённого доказательства и более позднего воспроизведения; `signal-post` — обзор диспетчера; `response-route` — передача ответственности. Победитель и human approval не записаны. Ни один concept не доказывает полностью реализованный mobile accept→report journey. Замечания по хронологии, доступности камеры и неподдержанным действиям остаются видимыми.

Для повторного запуска локального read-only сервера из OS, если текущий процесс остановлен:

```bash
python3 -m http.server 8196 --bind 127.0.0.1 --directory production
```

Нужен конкретный настоящий human element feedback: что сохранить, убрать, усилить или сочетать. После ответа оператор создаёт отдельный feedback receipt с фактическим комментарием пользователя и регистрирует его через штатный `human-feedback`. Агент не заполняет человеческие решения самостоятельно.

## Проверка после реализации

React 18, Vite, TypeScript; output `frontend/dist/`; API-типы через `openapi-typescript` исключительно из настоящего JSON. `npm run gate` должен включать lint, typecheck, значимые тесты и сверку generated API types. Ошибки 501, network, empty, WS disconnect должны быть видимыми, без подмены данными.

Настоящий HRE lifecycle: pin `review-spec` → штатная регистрация sealed source revision → `completed-change` → `review-serve`. Capture recipe должна охватывать 1440×900, 1280×800, 390×844, normal/reduced motion и normal/red/error состояния. HRE использует same-origin deterministic fixtures; реальную REST/WS-интеграцию нужно доказать отдельными network/browser receipts. HRE captures не являются доказательством live backend.

На текущем этапе TS/lint/gate/build и пользовательские browser journeys продукта ещё не запускались, потому что реализации нет. Нельзя заменять их успешным preflight OS или концептами.
