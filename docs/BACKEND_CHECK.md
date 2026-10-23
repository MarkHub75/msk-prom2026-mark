# Проверка backend: POST, ACK, журнал, evidence

Backend Марка пока не найден в рабочем дереве; URL и формат GET-журнала не предоставлены. GitHub-коннектор вернул 404, чтение удалённых веток существующим Git-доступом завершилось ошибкой. Авторизация, VPN, SSH и main не менялись. Ниже подготовленный инструмент, а не утверждение, что сервис Марка подключён.

Существующий формат сохраняется: EventMutation v1 — `ml/contracts/schemas/event.schema.json`; ACK — `ml/contracts/schemas/ack.schema.json`. Receiver сохраняет `(event_id, revision)` до ACK, создаёт одно оповещение на эпизод и не откатывает журнал поздней старой ревизией. Конкурентные разные тела одной пары должны проверяться транзакционно.

## Данные от backend-команды

Нужны фактические URL POST, чтения инцидента/журнала с `{event_id}`, имя JSON-поля с EventMutation при наличии обёртки и работающий media-префикс. Альтернатива — ветка/папка backend и команда запуска. Секреты не присылать: достаточно пути к runtime-конфигурации; токен читается из `MOSPROM_BACKEND_TOKEN`.

После подтверждения маршрутов:

```bash
PYTHONPATH=/workspace/project /workspace/.venvs/linq-client/bin/python \
  -m ml.pipeline.backend_probe \
  --event-url 'https://BACKEND/CONFIRMED-INGEST-PATH' \
  --journal-url 'https://BACKEND/CONFIRMED-JOURNAL-PATH/{event_id}' \
  --event-file /workspace/artifacts/backend-integration-001/template.linq-fixture.json \
  --evidence-base-url 'https://MEDIA/CONFIGURED-ARTIFACT-PREFIX' \
  --evidence-file /workspace/artifacts/video-mvp/repeated-image-control-001/evidence/ff39a481-0876-48d9-aac4-f0fe5f6ceeda.jpg \
  --state-dir /workspace/artifacts/backend-mark-check-001
```

Маршруты не угадываются. Если GET возвращает `{"items":[EventMutation]}`, явно добавить `--journal-key items`. Ожидается сохранённый канонический payload v1, один инцидент и точная revision. Для другого DTO нужен адаптер по фактической документации backend. Journal bearer отправляется только тому же origin, что POST; другому media-origin backend-токен не пересылается. Redirects и credentials в URL запрещены.

Инструмент принимает явно тестовый event (`synthetic-test` либо `repeated-image-fixture`), один раз сохраняет новый incident UUID и intent, доставляет через существующий Outbox/HttpEventSink, повторяет ту же ревизию для проверки ACK, читает журнал и сверяет JPEG по SHA256. Повтор команды сохраняет identity. Это проверка транспорта, не новый инференс или подтверждение промышленного нарушения; исходная model/source provenance fixture сохраняется.

`report.json` — последняя успешная проверка; `last-attempt.json` — последний запуск, включая ошибки preflight. В диагностике нет URL, токенов, целых серверных ответов и текстов исключений. Сам ACK не доказывает, что backend не отправил два push: отдельно проверить notification storage/UI. На local-test получателе счётчик проверен, на backend Марка — нет.

## Уже выполнено

`/workspace/artifacts/backend-integration-001/local-contract-review.json`: настоящий loopback POST/ACK/GET-журнал/GET-JPEG на явно тестовом сервере. Event взят из сохранённого labelled LinQ fixture; новых нейросетевых запросов в этой проверке 0. Две отправки и повтор команды оставили 1 committed revision и 1 notification; JPEG совпал по SHA256. Это **LOCAL_TEST_NOT_MARK_BACKEND**.

Отказные тесты: COMMIT выполнен, ACK потерян; повтор после restart сохраняет payload/UUID/revision без второго инцидента. Смена receiver/media-prefix блокируется до запроса, в outbox хранится только digest. ACK с bool/float revision отвергается. TEST-журнал возвращает MAX revision после позднего старого POST; два конкурентных разных тела одной ревизии не могут оба получить ACK.

Для старого outbox с delivered-строками без destination digest новое связывание при pending запрещено. Для настоящего backend использовать отдельный state-dir. ACK-нутые локальным получателем строки не переотправляются другому сервису автоматически; не сбрасывать delivered вручную.
