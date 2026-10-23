# W1B доступы и границы чтения

Дата: 23.10.2026, Europe/Moscow. Исследование начато около 09:32. raw JSON сохраняет ответы инструментов и локаторы, не является утверждением, что вся поисковая выдача принята за доказательство.

## Неудачные каналы

- https://hackathon2025.otkroimosprom.ru/ — web: not accessible via this tool; домен предположен по текущему имени, его историческое использование не доказано.
- https://hackathon.otkroimosprom.ru/ — web: 404 Not Found.
- https://vk.ru/hack_mosprom — web: cannot be opened (non-retryable error).
- https://yandex.kz/video/preview/17734538559620535084 — metadata награждения прочитаны; переход на VK Video (ссылка 3) дал Internal Error. Видео не воспроизведено и не просмотрено.
- https://web.archive.org/cdx/search/cdx?url=hackathon.otkroimosprom.ru/*&output=json&filter=statuscode:200&collapse=urlkey — not accessible via this tool.
- https://lk2026.otkroimosprom.ru/ — not accessible via this tool. Аутентификация не проводилась.
- https://sova.media/ — not accessible via this tool.
- https://api.github.com/search/repositories?q=mosprom — web недоступен; успешно заменён GitHub connector search_repositories/search/fetch_file/fetch. Поиск mosprom и точных имён команд сохранён в GITHUB_SEARCH.json, GITHUB_REPOS_2.json, GITHUB_WINNER_SEARCH*.json.
- https://codepulse.ru/ : ссылка 90 «Отчетная презентация» в кейсе Моспром — web click Internal Error; целевой материал не прочитан. Не путать с повторяющимися ссылками других кейсов.
- https://www-1.banki.ru/dialog/articles/33819/ — web timeout 400; поисковый текст не назван прочитанной публикацией.
- https://companies.rbc.ru/news/ZSsWl8ZWGq/summit-group---pobeditel-hakatona-pravitelstva-moskvyi/ — web 401 Unauthorized.
- https://finolive.ru/docs/234/annual_report_2025.pdf — web 400 Content length is too large: 12384908. Поисковый след указывает с.20, но полный документ и страница не прочитаны; цифра 24 команд не повышена до установленного факта.
- Invoke-WebRequest сайта2026: «Базовое соединение закрыто: Непредвиденная ошибка при передаче». Python requests: SSL UNEXPECTED_EOF_WHILE_READING. Не сохранена успешная HTML-копия.
- curl.exe -L --max-time 20 https://otkroimosprom.ru/upload/polojenie2022.pdf -o _WORK/SOURCES/W1B/polojenie2022.pdf : exit1, curl(35) schannel failed to receive handshake, SSL/TLS connection failed. Оригинал PDF отсутствует; web-извлечение с P0–P5 сохранено в WEB_MKM_AND_2022_PDF.json. Не заявляется получение оригинальных байтов.
- CUA: создание iab вкладки вернуло Browser is not available: iab. Следующий getState вернул apps=[], browsers=[]. Браузерного способа просмотра/скачивания в этой среде не оказалось.

## Как читать GitHub-сохранения

GITHUB_READMES.json: объект {repos,rr}; индексы совпадают. fulfilled не равен успеху API: проверяйте value.isError. Некоторые README отсутствуют/репозитории пусты; это не отсутствие кода вообще. Полные полученные README доступны сборщику, но в отчёте использованы только явно названные и прочитанные части. GITHUB_PINNED.json закрепляет два содержательно разобранных README по commit. GITHUB_COMMITS.json — API-ответы с датами и SHA; content содержит JSON-строку. Коммиты после дедлайна и README поздней редакции не дают права обвинять команду в нарушении: статус финальной сдачи неизвестен.

## Поисковые ограничения

Поиск 2023/2024 смешивает бренд экскурсий/спартакиаду/ЛЦТ с хакатоном; отсутствие результатов не доказывает пропуск года. GitVerse и веб-поиск по точным именам не замкнули атрибуцию победителей2025. Репозиторий с подходящей темой не приписывается победителю без связующего источника. Страницы поисковой выдачи оставлены как маршруты, а не как самостоятельные доказательства метрик, внедрений или причин победы.
