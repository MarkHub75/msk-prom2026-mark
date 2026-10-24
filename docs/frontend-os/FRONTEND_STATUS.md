# SafeWatch — статус frontend

Обновлено: **2026-10-24 06:37 МСК**. Ветка: **codex/safewatch-frontend-v1**.
Последний опубликованный коммит на момент обновления: `d3f9e4b1` (дизайн-ассеты и первичный статус).
Текущий этап: фиксация полного проверенного приложения и интеграционного слоя. Gate и source-bound browser QA завершены; следующим коммитом публикуется этот этап.

Frontend Hackathon OS 4.0: **HUMAN_PRODUCT_REVIEW**; run `safewatch-20261024-working-r3`. Концепция `signal-post` утверждена человеком, рабочие экраны ещё не утверждены.

| Функция | Статус | Проверка | Ограничения |
|---|---|---|---|
| Дизайн-система, App Shell, пять ролей | Работает на локальных fixtures | Chromium; gate PASS | Первое продуктовое human review ожидается |
| Пульт, красные/жёлтые тревоги, секторы | Работает только на локальных fixtures | 1440×900, 1280×800, 390×844 | Внешний stateful-мок ещё не проверен |
| Incident Focus и разрешённые действия | Работает только на локальных fixtures | confirm → sent_to_master; false_alarm | Настоящий S0 business API — 501 |
| Мобильный мастер | Работает только на локальных fixtures | accept → обязательные меры → resolved; reload | Поле мер ниже первого экрана |
| Камера, запись, HUD | Работает только на локальных fixtures | Видео декодируется; play/pause/HUD | Синтетический статичный повтор, не live/LinQ |
| REST health и WS hello | Работает с настоящим backend S0 | health 200, hello по WS-схеме | Остальные бизнес-методы S0 — 501 |
| Внешний stateful-мок Claude | В разработке | Ветка origin/demo/checkpoint доступна | Браузерный E2E ещё не выполнен |
| Полноценный журнал | Не начато | — | Нужен для нового критического пути |

## Качество

Основной `npm run gate` PASS: generated API check, ESLint, TypeScript, 14 тестов, production build. Независимая рабочая интерпретация: 16 тестов PASS. Browser QA и anti-slop PASS; HRE — по 44 screenshots/4 recordings на вариант. Подробные доказательства: [VERIFICATION.md](VERIFICATION.md). Human Product Review: **PENDING**, окончательной приёмки нет.

Проверены critical/normal/error/empty/offline/501/WS disconnected, сквозной fixture-сценарий и три разрешения. Известные P2: доступность поля мер после принятия, пересоздание плеера при REST-обновлении. Original font OFL тексты сохранены побайтно, включая исходный пробел в конце строки лицензии.

## Интеграция и координация

Подключены настоящие REST DTO и `allowed_actions`, X-Role/X-Actor, относительные URL медиа, `/ws` с проверкой схемы и переподключением. WS слой принимает hello/notification/event.created/event.updated/camera.state/sector.state/broadcast.state/backend.status/job.progress; применимость отдельных экранов проверяется в E2E. Новое hello вызывает повторное получение REST.

Fetch 06:32 МСК: origin/main `7313e04b` (S5), origin/demo/checkpoint `f7520320`. `contract/openapi.json`, `ws.schema.json`, `ws-examples.json` не изменились относительно нашей базы S0. `progress.md`, CLAUDE.md и чужой frontend прочитаны; merge не выполнялся. Backend, mock и серверные контракты не изменялись.

Зависимости от Марка: готовность S6–S8 и уведомлений для настоящего бизнес-E2E. От Матвея: реальные результаты CV/LinQ и заводские медиа для проверки качества детекции; для UI-E2E они не требуются. Готовность настоящего backend на S5 в этой ветке пока не подтверждена запуском; старый факт 501 относится к проверенному S0.

## Следующие шаги

1. Закоммитить и опубликовать текущие assets, приложение и HRE-документацию в собственной ветке.
2. Изолированно запустить внешний mock из origin/demo/checkpoint, прочитать README/GAPS.
3. В браузере: operator → yellow → red → Incident Focus → confirm/handoff → mobile accept → resolve с комментарием → журнал; проверить nullable episode, relative evidence URL и reset/reconnect/REST reconciliation.
4. Исправлять только подтверждённые несовместимости frontend; новый код — новый source-bound HRE revision по поддерживаемому пути OS. Существующий рабочий HRE v1 и исходные концепции сохраняются.

Блокеры: проверенного бизнес-E2E против настоящего backend нет; сейчас это не блокирует проверку внешнего stateful-мока. HRE концепты/скриншоты/сырые доказательства сохранены локально в OS run и в versioned archive; тяжёлые review-артефакты не добавляются в Git. [Точки входа, пакет и команды](FIRST-READ.md).
