# Статическое демо

Включается только при сборке с `VITE_STATIC_DEMO=1`. Обычная сборка продолжает работать с API.
Сборка, установка Playwright и проверка выполняются в `.github/workflows/pages.yml` на GitHub runner.
Локально устанавливать зависимости и собирать демо не требуется.

`mock/state.mjs`, `mock/world.mjs`, `routes.mjs`, метаданные и кадры перенесены из
`origin/demo/checkpoint:tools/checkpoint-demo/` (коммит `43465c2361271cd2fc781af7c2653da6eae0f8fb`, state/world/server, previews и evidence).
Из логики удалены Node.js, файловая система и прокси к бэкенду. SHA-256 кадров сохранены в `mock/evidence.json`.
Ручная разметка кадров и сценарий синтетические; они не подтверждают работу нейросети.
Название берётся из `src/brand.ts`.

Режиссёр публикует жёлтый бег, затем красное падение. Второй шаг явно завершает предыдущее событие
так же, как `publishNext({force: true})` исходного мока. Подтверждение красного события передаёт его мастеру;
мастер принимает его, указывает меры и завершает. Через 45 секунд без решения оператора работает
автоэскалация исходного мока. Состояние живёт в памяти одной вкладки, сохраняется при переключении ролей
и сбрасывается кнопкой «Сбросить» либо перезагрузкой. Разные вкладки не синхронизируются.

## Ручки

Работают локально в браузере:

- GET `/api/health`, `/api/meta`, `/api/operator/dashboard`, `/api/operator/feed`.
- GET `/api/sectors`, `/api/sectors/{id}/view`, `/api/cameras`, `/api/cameras/{id}`, `/api/admin/cameras`.
- GET `/api/events`, `/api/events/{id}`, `/api/journal/facets`, `/api/master/inbox`, `/api/master/shift`.
- POST `/api/events/{id}/actions` с проверкой ролей, переходов и обязательных мер при завершении.
- Кадры `/api/cameras/{id}/preview` и `/api/evidence/{id}/image`; в ответах URL заменены на статические
  `demo/previews/` и `demo/evidence/`, чтобы работали обычные `<img>`.
- WebSocket `/ws?role=...`: hello, события, состояния камер/секторов, уведомления по роли — в памяти браузера.

Все остальные `/api/*`, включая аналитику `/api/stats/*`, `/api/ohs/rules`, `/api/system`, `/api/models`,
`/api/jobs`, живое видео `/api/cameras/{id}/view`, настройки камер, экспорт CSV/PDF, загрузку видео и
неподдерживаемые записи, возвращают 501 `not_implemented`: «Недоступно в статическом демо».
У исходного мока нет этих реализаций; обращения к настоящему серверу не выполняются.
Некорректные действия и отсутствующие события/кадры возвращают соответствующие 400/403/404/409/422.

## GitHub Pages

Публичный адрес после включения Pages и успешного deploy:
`https://markhub75.github.io/msk-prom2026-mark/#/operator`.
HashRouter обеспечивает работу переходов и обновления страницы под `/msk-prom2026-mark/`.
Сгенерированный `404.html` переводит прямой `/msk-prom2026-mark/operator` на канонический `#/operator`.

Если Pages ещё не включён, сборка и smoke проходят, артефакт `github-pages` сохраняется, deploy пропускается
с предупреждением. Владельцу или администратору репозитория нужно:

1. Settings → Pages → Build and deployment → Source → **GitHub Actions**.
2. Если GitHub требует тариф: для Pages приватного репозитория нужен GitHub Pro/Team/Enterprise.
3. Settings → Environments → github-pages → Deployment branches and tags: разрешить ветку **front/pages**.
4. В Actions открыть последний **Pages** для **front/pages**, нажать **Re-run all jobs**.
   Если ручной запуск workflow пока не отображается в UI, повторный push в `front/pages` тоже запускает его.

Проверка Pages API: `gh api repos/MarkHub75/msk-prom2026-mark/pages`.
Включение администратором: `gh api --method POST repos/MarkHub75/msk-prom2026-mark/pages -f build_type=workflow`.
Ссылка выше — ожидаемый адрес; до успешного deploy это не опубликованный сайт.
