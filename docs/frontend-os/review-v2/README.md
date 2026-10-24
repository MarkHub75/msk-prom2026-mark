# Реальные captures внешнего stateful-мока

Это неизменённая выборка из браузерного прогона **SafeWatch frontend + внешний checkpoint-demo REST/WS**, не локальные review fixtures. [Протокол PASS 8/8](../receipts/external-mock-v2/summary.json). PNG сохранены побайтно, SHA256 — в `capture-sha256.json`.

- [Пульт после reset](01-operator-empty-1440.png), [жёлтое событие](02-yellow-incident-1440.png), [красный takeover](03-red-takeover-1440.png), [Incident после подтверждения и передачи](04-red-handoff-1440.png).
- Мастер 390×844: [поручение](06-master-pending-390.png), [явное имя](06a-identity-dialog-master-390.png), [обязательный отчёт](07-master-accepted-390.png), [завершено](08-master-resolved-390.png).
- [Журнал с серверными фильтрами](10b-journal-filtered-390.png), [reset → 404 без старых действий](16-incident-reset404.png), [восстановленный кадр](18-evidence-off-refresh.png).

Все данные, доказательства и ручная разметка внешнего мока синтетические. Его камеры не имеют видео/эфира/HUD. Проверка мока не доказывает готовность настоящего backend или качество CV. Это компактные материалы для команды; настоящий HRE создаёт штатный контроллер OS и открывает утверждённый renderer. [Текущий статус и точки входа](../FRONTEND_STATUS.md).
