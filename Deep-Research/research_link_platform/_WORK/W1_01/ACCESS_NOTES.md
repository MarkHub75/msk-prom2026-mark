# W1-01 — заметки о получении доказательств

Время завершения записи: 2026-10-23 01:21:45 UTC / 04:21:45 Europe/Moscow. Полные статьи не копируются; подробный собственный пересказ и реестр источников — в соседнем W1_01_RESULT.md.

## Основные успешные получения

- web open: lin-q.ru `/`, `/tech`, `/press`, `/sol`, `/hr`; tpost `loley0om21-freimvork-dlya-tenzornogo-protsessora-li`, `n1g409mdu1-haitek-anonsiruet-na-forume-mikroelektro`, `e3s9mtzvl1-minpromtorg-vklyuchil-tenzornii-protsess`; партнёрские страницы РСК и «Гравитона»; iva.ru/ru/news/108; Habr/VK 895432. URL и локаторы перечислены в результате.
- TinyFish fetch_content: исторические service-страницы FW_TPU_H и FW_TPU_E. Итоговые адреса `https://hi-tech.org/local/get/?ACTION=SERVICE&EL=663/` и `https://hi-tech.org/local/get/?ACTION=SERVICE&EL=664/`. Извлечены описание, API Python3.8/CLI, OEM-условия, ссылки на руководства/инструкции. Published_date и author отсутствовали.
- web PDF index: Hitech_Integr_2023.pdf на ivolgacap.ru, 18 страниц. Дата на титуле март 2023; PDF page 4 — история, page 6 — направления, page14 — юридическая структура. Запрошены screenshots page index3 и5.
- web PDF index: старое руководство FW_TPU_H, 61 страница, 2021, титульное обозначение `RU.РМДВ.04.06.003-01 97 01`. Последующий запрос по тому же адресу вернул HTML «Хайтэк-Интеграция»; текущий live PDF не сохранён и не подтверждён.

## Недоступное и статус

- Сборник НИИМЭ со статьёй Осипенко/Увкина: индексированный поисковый фрагмент содержит авторов, DOI и аннотацию с IVA H/E. Full open отклонён web: Content length is too large, 18837434 bytes. TinyFish timeout, CLI PowerShell/curl/Python TLS handshake/SSLEOFError; HTTP соединение закрыто сервером. Ни одного локального PDF не создано. Нельзя ссылаться на невиденные таблицы стр.87–88.
- Минцифры list URL: search index содержит IVA H/E; web 502, TinyFish timeout. Номера реестра 12903/12904 — зацепки, не подтверждённые карточки.
- Старые service URL: web inaccessible, TinyFish успешен. Поэтому недоступность одним инструментом не трактуется как отсутствие материала.
- docs: web inaccessible в этой ветке; соседняя W1-03 получила публичную страницу другим каналом. Не делается вывод о закрытости всех руководств.

## Уровень проверки

Сетевое чтение/извлечение документов выполнено. Установка пакетов, выполнение команд из руководств, запуск компилятора, доступ к физическому устройству и собственные замеры не выполнялись.
