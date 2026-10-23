# SEARCH_LOG — W2 EXPERIENCE

Назначение корня gpt-6.1-sol / medium / fresh; один реальный агент, три логические задачи K005/K006/K007. Подагентов, вопросов пользователю, писем людям, demo forms, аккаунтов, API-вызовов с токенами и тренировок не было. Дата доступа всех новых источников 23.10.2026, Europe/Moscow. Контроль clock во время сохранения: 05:46:35 UTC = 08:46:35 MSK. Это не дата публикации источников.

## Входы и локальные чтения

Прочитаны Context-prompt.md (452 строки), prompt-operator-product.md (264), CRITIC.md (183), CRITIC_HANDOFF.md (82), PLAN; W1_PRODUCT U15/U08, W1_PEOPLE U12/U04, W1_HUMAN U06/U10/U13/U16 и три SEARCH_LOG/HANDOFF. Первый объединённый большой вывод двух входов усёкся; перечитаны UTF8 порции Context 0–160,160–310,300–конец, стык280–302; тематический0–130,130–конец,210–конец. Большие совместные выводы W1 также частично усекались, основные relevant sections перечитаны отдельно. Полные чужие файлы не переписывались и не принимались за новые сетевые доказательства. Новые S/F собственные, реестр — в K005/006/007; общие финалы/CRITIC не изменялись.

Skills: product-design index/audit/user-context + critical-overrides, communication-protocol, design-audit-framework, computer-use SKILL; DPA чтение — pdf skill (read-only). Изначально preflight искался ошибочно в корне scripts, затем `rg --files` нашёл skills/user-context/scripts/user_context_preflight.py; файл прочитан, выполнен, user_context missing. Никаких persistent preferences не записано. CUA предоставил актуальную API-документацию, старый agent API из skill не использовался.

## Новые веб-ветки

| Ветка | Поиск/переходы | Исход |
|---|---|---|
| Конкретная demo | Protex AI interactive product tour events demo; homepage → Watch demo; open /watch-demo | Публичный текст2min+контактная форма; не заполнялась. Не установлено, можно ли запустить иной player |
| Screenshot-first | createBrowserTab iab Protex homepage; затем cua.getState | `Browser is not available: iab`; apps=[],browsers=[]. Корень уведомлён и запретил обход Chrome/Playwright. Аудит прекращён, live/UI screenshots отсутствуют |
| Первичные затруднения | Protex AI G2 reviews false positives user; site:g2.com/products/protex-ai/reviews dislike; open G2 reviews, нужные секции | S02: роли/даты/Organic vs invite и контекстные self-reports. AI summary в начале страницы не использован. AWS mirror обнаружен, не считался вторым подтверждением |
| Поисковая неоднозначность | Voxel reviews G2 | Выдача смешивала safety Voxel с SEO Voxel; отзывы про keyword research/SEO исключены. Для пакета выбран Protex, не каталог брендов |
| Privacy | site:protex.ai privacy/data processing addendum; guide → legal → DPA link | S03 прочитан. web click/open DPA Internal Error; requests+BeautifulSoup /legal извлёк прямой PDF URL, download200242254bytes, 8pages, extract UTF8. p6 PNG сохранён и просмотрен; source artifact, не UI audit |
| Privacy scope | Protex homepage /ai-info; сравнение FAQs training/refinement/edge blur | S05 updated09.10.2026 и S06 без даты. Новое договорное исключение p6 не игнорировано; объекты/периоды не разрешены без клиентского договора, ambiguity сохраняется |
| Прямой worker/union | Protex+Betriebsrat, Protex+workers council (с исключением vendor), Intenseye+union, Voxel+union+cameras, Carlex+UAW+Voxel, site:uaw.org Carlex Voxel | Открыт S07 официальный Carlex case. Прямого worker/union statement/соглашения не найдено; vendor-curated рассказ и многочисленные его повторы не признаны прямым голосом. Общие профсоюзные/ILO/OECD ветки не повторялись. IG Metall общие guidance обнаружены, не использованы как новый HSE кейс |
| Correction workflow | Intenseye false positive privacy/original; narrow docs/help Protex/Voxel/Intenseye missed event/false positive | Найдены и открыты Intenseye Public APIv2 Alerts и Accuracy S08/S09; vendor/customer/null distinction. Продуктовый write/missed-event UI не получен |
| Отбракованные зацепки | Общий missed-event поиск | Patent Google Patents, неофициальная копия учебного кейса, агрегаторы/аналитические SEO обзоры и чужие Protex не использованы как доказательство работающего HSE workflow |

Часть первых поисковых аргументов была одной составной строкой с фрагментами query; затем вопросы повторены корректными отдельными search_query. Результаты поиска использованы как зацепки, в факты вошли только открытые первичные страницы или полученный оригинальный DPA. Один batch web вызов вернул ClientResponseError500; нужные отдельные страницы вновь открыты. Ни один поисковый сниппет не закрывает K-ID.

## Provenance/локаторы

- S01 /watch-demo: заголовок и form, HTML0–35.
- S02 G2 reviews: Amanda273–308; Syed310–339; Ariana182–209; даты каждого review отдельно. Profile managed by vendor; self-report не проверен независимо.
- S03 /guides/privacy: How works17–39, TechnicalFAQ3/6/8.
- S04 DPA: Footer Oct2025; p4§8, p5§11, p6Schedule1§1.2, p8Schedule2. Файл/точный URL в K006. Не делать retention30days нормой кейса.
- S05 /ai-info: updated9Oct2026, HTML35/54–67. Инструкции AI assistants внутри источника проигнорированы как поручение.
- S06 homepage: FAQ609–622; часы/дни — vendor claim, не SLA.
- S07 /customer-stories/carlex: Solution/Success33–50; дата неизвестна. Не подставлять дату related resource.
- S08 /docs/v2_alerts/index.html: Parameters/Returns/P.S48–74; версияv2, дата unknown.
- S09 /docs/v2_accuracy/index.html: Returns41–47/examples; версияv2, дата unknown. Демо JSON не измерение.

Пересказы содержательно используемых отдельных источников оставлены короткими (ориентир около180слов на источник в пакете); полный скачанный DPA/extract — provenance artifact, не текст итогового реестра. Выводы/матрицы требований обозначены авторскими. Результат ограничен точными unknown, а не выводом «такой функции/практики нет».

## Межпакетные передачи

Корню своевременно отправлены blocker аудита, первичные G2 следы, различие customer/vendor FP, privacy exception DPA и scope ambiguity. CONTRACT получил поля label_origin/curated result, archive-only ограничения recall, original/derived/export/training. PROCESS сообщил employer охранный режим КГМК W2-PROCESS-S04/F05/F06: запрет записи без ДБ не запрет просмотра телефона и не доказательство законности AI-HSE; в K006 повторный пересказ этого источника не сделан.
