# SafeWatch — статус frontend

Обновлено: **2026-10-24 06:53:47 МСК**. Ветка: **codex/safewatch-frontend-v1**.
Последний опубликованный коммит на момент обновления: `3c7a5e5d` (внешний mock smoke); OS/HRE — `ae499962`, приложение — `8e390c34`, ассеты — `d3f9e4b1`.
Первый рабочий проход опубликован. HUMAN_PRODUCT_REVIEW **KEEP** получен от человека и зарегистрирован штатным `single-product-completion`. Выполнены точечные исправления; идёт повторный браузерный E2E внешнего мока, без встроенного reviewFetch.

Frontend Hackathon OS 4.0: **SINGLE_PRODUCT_BUILD**; run `safewatch-20261024-working-r3`, base `signal-post-command`. Рабочая основа утверждена с конкретными исправлениями. Глобальный редизайн запрещён; финальная приёмка исправленного продукта ещё впереди. [Фактическое человеческое решение](receipts/working-v1/human-product-keep.md), [штатный completion packet](receipts/working-v1/human-product-keep.json).

| Функция | Статус | Проверка | Ограничения |
|---|---|---|---|
| Дизайн-система, App Shell, пять ролей | Работает на локальных fixtures | Chromium; gate PASS | Первое продуктовое human review ожидается |
| Пульт, красные/жёлтые тревоги, секторы | Работает на stateful-моке, baseline | WS yellow/red/takeover; 1440/1280/390 | Исправленный вариант сейчас на повторном E2E |
| Активная очередь / завершённая история | Работает на локальных fixtures | normal: активных 0, завершённых 4; meta terminal | Серверные статусы не меняются |
| Incident Focus и разрешённые действия | Работает на stateful-моке, baseline | confirm → sent_to_master, две записи истории | Исправлены stale actions после reset/404; повторный E2E идёт |
| Мобильный мастер | Работает на stateful-моке, baseline | accept → обязательные меры → resolved; reload, явный actor | Повторный E2E новой identity UX идёт |
| Явное имя перед действием | Реализовано, браузерная проверка идёт | Unit: нет фиктивного имени/POST; отмена; ввод → действие | После сохранения — X-Actor с введённым именем |
| Камера, запись, HUD | Работает только на локальных fixtures | Видео декодируется; play/pause/HUD | Синтетический статичный повтор, не live/LinQ |
| REST health и WS hello | Работает с настоящим backend S0 | health 200, hello по WS-схеме | Остальные бизнес-методы S0 — 501 |
| Внешний stateful-мок Claude | Работает частично; полный E2E перепроверяется | Upstream smoke **30/30**; baseline UI core PASS, три дефекта выявлены | Новая ревизия проверяется отдельно |
| Журнал | Реализовано; повторный E2E идёт | Реальные GET events/facets, cursor, фильтры; 2 unit tests PASS | CSV/расширенная аналитика не реализованы |

## Качество

Текущий `npm run gate` **PASS: 19 тестов**, generated API check, ESLint, TypeScript и production build `index-BudDY7eU.js`. Дополнительные регрессии покрывают явный actor, удаление stale actions при REST404 и фильтры/cursor журнала. Предыдущий HRE working-v1 остаётся неизменным; его доказательства — [VERIFICATION.md](VERIFICATION.md). Новый source-bound HRE будет зарегистрирован после внешнего E2E.

Baseline внешнего E2E: основной цикл PASS, но **FAIL3** — журнал был stub; Incident сохранял действия после reset+404; evidence не восстанавливался по тому же URL. [Полный исходный summary](receipts/external-mock-v1/summary.json). Все три исправлены в коде, подтверждение повторным E2E ещё ожидается. У fixture «Падение» убраны неподходящие кадр и ролик; доказательство честно недоступно. На 1440×900 оба медиа-блока теперь видны в первом экране. HUD использует только реальные objects/bbox DTO, после декодирования изображения. Original OFL сохранён, включая исходный пробел лицензии.

## Интеграция и координация

Подключены настоящие REST DTO и `allowed_actions`, X-Role/X-Actor, относительные URL медиа, `/ws` с проверкой схемы и переподключением. WS слой принимает hello/notification/event.created/event.updated/camera.state/sector.state/broadcast.state/backend.status/job.progress; применимость отдельных экранов проверяется в E2E. Новое hello вызывает повторное получение REST.

Fetch 06:32 МСК: origin/main `7313e04b` (S5), origin/demo/checkpoint `f7520320`. `contract/openapi.json`, `ws.schema.json`, `ws-examples.json` не изменились относительно нашей базы S0. `progress.md`, CLAUDE.md и чужой frontend прочитаны; merge не выполнялся. Backend, mock и серверные контракты не изменялись.

Мок запущен из отдельного detached worktree `/mnt/d/templates/msk-promhack/safewatch-checkpoint-mock` (f7520320), REST 4010 / WS 4011. Frontend dev:mock — 5185, свежий browser context и `review=real`. Smoke выполнялся перед UI-сценарием, потому что он сбрасывает мир. [Raw smoke с SHA256](receipts/external-mock-v1/upstream-smoke.json). Мок не реализует camera view/video/HUD; это ограничение его покрытия. До исправлений требуют runtime-проверки риски устаревшей Incident-карточки после reset и повторной загрузки evidence после 404.

Зависимости от Марка: готовность S6–S8 и уведомлений для настоящего бизнес-E2E. От Матвея: реальные результаты CV/LinQ и заводские медиа для проверки качества детекции; для UI-E2E они не требуются. Готовность настоящего backend на S5 в этой ветке пока не подтверждена запуском; старый факт 501 относится к проверенному S0.

## Следующие шаги

1. Завершить повторный браузерный E2E внешнего мока с новой identity UX, журналом, reset/404 и evidence retry.
2. Отдельно перепроверить доступный настоящий backend; результаты не смешивать с моковыми.
3. Зафиксировать frozen source, независимую проверку, новый HRE только изменённых экранов через `final-product` текущего OS run.
4. Остановиться на следующем настоящем human checkpoint, без самостоятельной финальной приёмки.

Блокеры: проверенного бизнес-E2E против настоящего backend нет; сейчас это не блокирует проверку внешнего stateful-мока. HRE концепты/скриншоты/сырые доказательства сохранены локально в OS run и в versioned archive; тяжёлые review-артефакты не добавляются в Git. [Точки входа, пакет и команды](FIRST-READ.md).
