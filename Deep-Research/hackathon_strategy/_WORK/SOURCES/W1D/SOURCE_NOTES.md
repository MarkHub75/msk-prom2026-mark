# W1D — сохранённые выписки и журнал доступа

Дата доступа: 2026-10-23; окно исследования с 09:41 Europe/Moscow. Локальные IDs отчёта W1D_EXECUTION.md. Ни один проект, SDK или устройство не запускались. Ни один PDF не использован/не скачан в самостоятельном поиске этой ветки; PDF-правила потреблены только как соседний отчёт W1A с его оговорками.

## W1D-S01 — авторское объяснение walking skeleton

URL: https://groups.google.com/g/growing-object-oriented-software/c/uKtktAVhWLM

Название: “Start Each feature with an Acceptance Test” => end-to-end ? Авторы ветки Steve Freeman, Nat Pryce и другие; использованы конкретно ответы Nat Pryce 16 и 18 июня 2013. Google Groups отображает часы в своей локали; календарная дата сообщения надёжнее часа. Локаторы web-текста: 156–164, 779–809, 884–916. Raw: DETAIL.json и PRIMARY.json. Прочитаны реальные сообщения, не только поисковая выдача. Pryce объясняет, что ранние сквозные тесты позволяют обнаружить свойства инфраструктуры, которые иначе усложнили бы адаптеры; walking skeleton нужен для внешних границ системы/команды и пути разработки/развёртывания. Собственную внутреннюю БД можно отложить. Это авторская инженерная методика, не контролируемое исследование хакатонов.

## W1D-S02 — первичная методика Continuous Integration

URL: https://martinfowler.com/articles/continuousIntegration.html

Martin Fowler, Continuous Integration, дата текущей редакции в HTML 18 January 2024. Прочитаны разделы Everyone Pushes Commits To the Mainline Every Day; Every Push to Mainline Should Trigger a Build; Fix Broken Builds Immediately, а также вводное определение. Локаторы web 252–280 и далее; raw INTEGRATION_SLEEP_SCHEDULE.json. Интеграция требует возврата изменений в общую ветку, а не только подтягивания общей ветки в персональные; семантические конфликты не исчерпываются git merge. Проверенная сборка необходима. Частота для наших 45 часов в отчёте — наша адаптация; статья её не измеряла.

## W1D-S03 — контролируемое исследование ограничения сна, только abstract

URL: https://pubmed.ncbi.nlm.nih.gov/12683469/?dopt=Abstract

Hans P. A. Van Dongen, Greg Maislin, Janet M. Mullington, David F. Dinges. The cumulative cost of additional wakefulness: dose-response effects on neurobehavioral functions and sleep physiology from chronic sleep restriction and total sleep deprivation. Sleep. 2003 Mar 15;26(2):117–126. DOI 10.1093/sleep/26.2.117, PMID12683469. Авторы, Design/Setting/Participants/Interventions/Results/Conclusions авторского abstract прочитаны через PubMed. Всего48 здоровых взрослых21–38; рандомизация4/6/8ч time in bed на14 ночей, отдельный эксперимент0ч на3 ночи; baseline/recovery по3 дня, лабораторный мониторинг. Авторы сообщают накопление ухудшения выполнения когнитивных задач при4/6ч и ограниченную способность субъективной сонливости отражать ухудшение. Полный текст/таблицы не прочитаны. Первое успешное чтение есть в SEARCH_INITIAL.json; повторные open иногда возвращают только HHS footer (INTEGRATION_SLEEP_SCHEDULE.json), что отдельно сохранено. Нельзя выдать исходный14-дневный дизайн за опыт двух ночей хакатона.

## W1D-S04 — procedural placekeeping, только abstract

URL: https://pubmed.ncbi.nlm.nih.gov/31750712/

Michelle E. Stepan, Erik M. Altmann, Kimberly M. Fenn. Effects of total sleep deprivation on procedural placekeeping: More than just lapses of attention. Journal of Experimental Psychology: General149(4),800–806, April2020; online2019-11-21. DOI10.1037/xge0000717. Локаторы239–242 author abstract и177–191 metadata; raw INTEGRATION_SLEEP_SCHEDULE.json. N=138 contributing data, rested/sleep-deprived условия; PVT и UNRAVEL. Авторы сообщают ухудшение placekeeping и memory maintenance сверх влияния внимания. Статистики и полные методы не получены из статьи, величины «вдвое» не используются. Нельзя непосредственно оценить риск наших git-ошибок.

## W1D-S05 — первичный рассказ команды о поздней интеграции/сдаче

URL: https://josy0ee-newsletter.beehiiv.com/p/lessons-learned-from-a-24-hour-hackathon

Jiaxin Zhang, Lessons learned from a 24-hour Hackathon,29.04.2026; событие25–26.04.2026, Whale×Anthropic, по рассказу автора. Прочитан основной текст: временные отметки25April12:00–26April12:00 и Outcome; raw DETAIL.json/PRIMARY.json. Трое разделили UI/development/storytelling, к утру часть функций не работала у автора; коллега записала работу на своём устройстве; монтаж/экспорт заняли больше ожидаемого, вставить ссылку в submission sheet не удалось, ссылку оставили рядом с кодом. Команда не победила по словам автора. Независимого протокола/репозитория нет; не причинное доказательство поражения. Право на запись и предварительное обсуждение чужого события к Моспром не переносится.

## W1D-S06 — первичный рассказ AgroCode

URL: https://habr.com/ru/articles/653497/

NapoleonIT, автор представляется Вовой, команда LateDev. Как за40 часов распознать всех поросят с помощью компьютерного зрения. Решение задачи на AgroCode Hack.28.02.2022; событие2021. Прочитан основной текст, особенно Постановка задач и ресурсы/Техническое решение; web22–44, raw PRIMARY.json. Три роли DS/frontend/ML engineer; общий проверяющий сервер/установка фреймворка поменяли решение; DeepSort изменял координаты, маски искажались, причину поняли после события. Автор связывает случайное удаление обучения с недосыпом; это его атрибуция. В W1C-S09/F07 тот же первоисточник — не независимое подтверждение.

## W1D-S07 — официальный публичный график

URL: https://hackathon2026.otkroimosprom.ru/

АНО Моспром; дата публикации/редакции страницы неизвестна, год2026. Раздел Расписание, web643–708; raw INTEGRATION_SLEEP_SCHEDULE.json и PRIMARY.json.23October13:00 кейс,16:30 открытие,18:00 CP1;24October11:00 CP2,18:00 CP3,19:00–19:45 прожарка;25October10:00 сдача,12:00–17:30 защиты. Раскладка по датам сопоставлена с W1A-F03. Точные слоты команды и изменения ЛК неизвестны.

## Дополнительные и неиспользованные зацепки

https://www.growing-object-oriented-software.com/ — web timeout; https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/ch10.html — прочитан только открытый preview главы10, авторы Freeman/Pryce,October2009. Полная глава требует подписки; выводы основаны на S01, а не на якобы прочитанной книге. https://alistair.cockburn.us/ — сохранилась стартовая страница, оригинальную статью walking skeleton не получили; не приписываем ему дословных определений из вторичных пересказов.

Microsoft Community Hub, материал с заголовком What’s the secret to winning hackathons? A great idea,22 hours without sleep and Microsoft Azure, URL https://techcommunity.microsoft.com/blog/studentdeveloperblog/what8217s-the-secret-to-winning-hackathons-a-great-idea-22-hours-without-sleep-a/311698/ — поиск сообщил о поочерёдном сне участников, но прямое открытие вернуло TimeoutError. Этот рассказ не включён в доказательства ротации.

https://pmc.ncbi.nlm.nih.gov/articles/PMC12884582/ — поисковая выдача дала подробный текст Caffeine Selectively Mitigates Cognitive Deficits Caused by Sleep Deprivation, но прямое open дал recaptcha. Не объявлен полностью прочитанным, не использован для назначения кофеина/дозировок. По выдаче placebo-группы перекрываются со Stepan2020, поэтому даже успешное получение не дало бы второго независимого N138. Сохранённая зацепка нужна только если W2 считает лекарства/полные методы существенными; текущая стратегия обходится без них.

Поиск: walking skeleton Cockburn/Pryce/GOOS, Fowler integration; Van Dongen restriction48/4/6/8/14days; Stepan placekeeping138; русские хакатон+интеграция+сон; первичные рассказы о поздней сборке. Не найдено сравнительного исследования сна пяти разработчиков за45ч или подтверждённого оптимума смен. Поисковые примеры не превращены в научную схему ротации.
