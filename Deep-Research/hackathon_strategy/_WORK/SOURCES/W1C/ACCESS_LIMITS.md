# W1C: пределы получения

Проверено 2026-10-23, начало 09:32 Europe/Moscow.

* `https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf`: web открыл PDF, извлёк текст с номерами P0–P12 (сохранено в LINQ3.json). Оригинал пытались скачать Invoke-WebRequest и curl.exe. Первый вернул `Базовое соединение закрыто: Непредвиденная ошибка при передаче`, второй `curl: (35) schannel: failed to receive handshake, SSL/TLS connection failed`. Python requests для lin-q.ru/press также дал `SSLEOFError [SSL: UNEXPECTED_EOF_WHILE_READING]`. Локальный оригинал PDF НЕ получен. Вызов web screenshot страницы P3 вернул только ссылку на изображение во внутренней истории инструмента; доступного локального PNG не получено, визуальная проверка таблицы не заявляется. Нужно отдельно скачать PDF в рабочей сети.
* `https://t.me/s/linq_h`: web сообщил `URL ... is not accessible via this tool`. Не читался как первичный канал; Telemetr — вторичное зеркало, используется только зацепкой.
* `https://lin-q.ru/sitemap.xml`: web сообщил URL inaccessible. /press прочитан, но динамическая лента новостей в извлечении отсутствует. Из этого не следует отсутствие публикаций.
* GitHub ссылки с `/tree/main` для Black Duck и Nornickel сначала дали `Failed to fetch restricted URL`. Корневые URL после этого открылись; git clone успешно получил оба проекта и AgroCode. Black Duck history получена через `git fetch --unshallow`. Окружения проектов не устанавливались, инференс не запускался.
* Rutube e17c8aaec991510b49c87689eca5a3e6: прочитаны название, описание, главы автора. Само видео не просмотрено; таймкоды из описания не являются наблюдением просмотра или вопросами жюри. Это ЛЦТ-2024, другая команда/кейc, не доказательство LinQ-соревнования СЗФО-2024.
