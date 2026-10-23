# Состояние запуска

topic: camera_calibration_geometry
started_at: 2026-10-23T19:33:12+03:00
context_version: mosprom-research-v1
stage: complete
completed_at: 2026-10-23T20:03:09+03:00
pipeline: six_research_agents_one_wave_then_orchestrator_synthesis
review_mode: orchestrator_synthesis_only; no_independent_critic; no_second_wave

Оба входных файла прочитаны целиком; итоговые имена берутся из тематического файла. PDF кейса и соседних отчётов в текущем каталоге нет. Основной репозиторий не изменяется; работа только в папке исследования. Расходов, обучения и разработки приложения нет.

Делегирование доступно: collaboration.spawn_agent поддерживает model, reasoning_effort и fork_turns. Всего четыре слота, включая корневой. Исследователям будет явно назначено gpt-6.1-sol / medium / none. Модель и effort уже работающего корневого агента инструментом не переназначаются; запрошен профиль оркестратора High, независимой runtime-телеметрии его effort нет. Не заявляем неподтверждённое переключение.

Интернет: tools.web__run доступен; shell network доступен для чтения первоисточников при необходимости. Внешние аккаунты не используются.

## Промежуточные находки

- A01: findHomography threshold имеет единицы destination coordinates; direction-aware fit обязателен. Четыре точки без независимых controls не доказывают accuracy.
- A01: /4.x redirected to 4.13.0, но это не доказательство latest; найдены противоречащие сведения releases. Итог будет привязан к реально прочитанному tag, без утверждения latest.
- A02: fSpy/GeoCalib не устраняют потребность в метрическом эталоне; автоматизация intrinsics/gravity отдельно от metric floor mapping.
- A03: PTS/source time отдельно от processing time; repeated temporal sampler frames не заменяют наблюдения. MVP label «быстрое перемещение» отделяется от «бег».
- Оркестратор выполнил небольшой аналитический toy calculation (GEOMETRY_SANITY.py), результат сохранён; не video/LinQ benchmark. Формулы и соглашения для синтеза в FORMULAE.md.

Число запущенных субагентов: ровно 6 из 6. Все завершены: /root/a01_geometry, /root/a02_calibration, /root/a03_speed, /root/a04_proximity, /root/a05_complex, /root/a06_tools. Подробные AGENT_01…06 файлы сохранены. Все шесть созданы gpt-6.1-sol / medium / fork_turns=none. Одновременно работало максимум три исследователя с корневым оркестратором, запуск очередями в одной волне. Других агентов не создавали. Задачи: AGENT_PROMPTS.md.

Все шесть агентских результатов прочитаны полностью, включая повторное чтение обрезанных диапазонов. Синтез завершён. В корне ровно шесть итоговых артефактов плюс два неизменённых входа: SOURCES.md, RAW_FACTS.md, CRITIC.md, OPEN_QUESTIONS.md, report_human_camera_calibration_geometry.md, report_machine_camera_calibration_geometry.md. Сохранены 62 S-ID, 78 F-ID, 12 собственных K-ID, 20 Q-ID, 10 предлагаемых E-ID. Исходные Axx-ID сопоставлены с общими ID. A03_SOURCES, A05_SOURCES и A06_EVIDENCE содержат сохранённые исходники/metadata.

Обычная аккуратность автора: локальные Markdown paths/anchors, последовательность S/F и YAML front matter проверены скриптом CHECK_ARTIFACTS.py; результат AUTHOR_CHECK_RESULT.json, issues=[]; YAML parsed PyYAML. Первое срабатывание проверки оказалось распознаванием матричной записи внутри inline code как ссылки; исправлен только parser служебной проверки. Проверка не получала новых сетевых доказательств и не являлась дополнительной исследовательской стадией/ролью. Сохранённые package manifests локально подтверждают NumPy conflict. Число ответов в YAML answers: 8; body их покрывает. Числа токенизации не измерялись и не заявляются.

Отдельного критика, второй волны, автора/редактора/сжимателя/аудитора-субагента не создавали. Все эти действия выполнены корневым оркестратором в согласованном синтезе.

Не выполнены и не заявляются: установка/resolver/import целевого стека, CV/GUI/model запуск, получение видео/датасетов/весов, survey, обучение/benchmark, export/quantization, доступ LinQ или проверка реального SDK. Единственное локальное вычислительное наблюдение — небольшой synthetic arithmetic example GEOMETRY_SANITY.py, не camera/video benchmark. Платные ресурсы и аккаунты не использовались, сообщения внешним людям не отправлялись, приложение не создавалось.

Главные остающиеся вопросы: официальный case/event contract, измеренный floor scale/controls, source coordinate/time pipeline, наблюдаемость контактов, CPU-rule permission и фактический LinQ output/execution, совместимый lock. Дальнейшая работа направляется Q/E, не скрытой второй волной.
