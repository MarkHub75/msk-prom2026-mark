# План behavioral_safety_feasibility

Полностью прочитаны оба входных файла. 16 реальных Medium-исследователей запускаются очередями до 3 одновременно.

- W1-01: Падение, лежание, неподвижность; владелец _WORK/W1-01.md; полное задание PROMPT_W1-01.md.
- W1-02: Бег и резкие перемещения в цеху; владелец _WORK/W1-02.md; полное задание PROMPT_W1-02.md.
- W1-03: Опасное сближение с механизмами и транспортом; владелец _WORK/W1-03.md; полное задание PROMPT_W1-03.md.
- W1-04: Телефон при работе и передвижении; владелец _WORK/W1-04.md; полное задание PROMPT_W1-04.md.
- W1-05: Курение и открытый огонь вне разрешённого места; владелец _WORK/W1-05.md; полное задание PROMPT_W1-05.md.
- W1-06: Перелезание через ограждения, проход под конвейером/подвешенным грузом; владелец _WORK/W1-06.md; полное задание PROMPT_W1-06.md.
- W1-07: Работа на высоте без привязи + дополнительная переноска груза; владелец _WORK/W1-07.md; полное задание PROMPT_W1-07.md.
- W1-08: Реальные готовые модели и весовые артефакты; владелец _WORK/W1-08.md; полное задание PROMPT_W1-08.md.
- W1-09: Видео падений и неподвижности; владелец _WORK/W1-09.md; полное задание PROMPT_W1-09.md.
- W1-10: Видео и разметка людей рядом с транспортом, техникой и барьерами; владелец _WORK/W1-10.md; полное задание PROMPT_W1-10.md.
- W1-11: Телефоны, курение, огонь, страховочные средства, прыжки/перелезания; владелец _WORK/W1-11.md; полное задание PROMPT_W1-11.md.
- W1-12: Качество данных, демонстрационные эпизоды, права и тестовый протокол; владелец _WORK/W1-12.md; полное задание PROMPT_W1-12.md.
- W1-13: Фактические интерфейсы LinQ и доступ, предоставляемый организаторами; владелец _WORK/W1-13.md; полное задание PROMPT_W1-13.md.
- W1-14: Модельные графы, экспорт и квантование под LinQ; владелец _WORK/W1-14.md; полное задание PROMPT_W1-14.md.
- W1-15: Производительность, FPS, пропущенные кадры и latency события; владелец _WORK/W1-15.md; полное задание PROMPT_W1-15.md.
- W1-16: Реальные сквозные reference pipelines и пути fallback; владелец _WORK/W1-16.md; полное задание PROMPT_W1-16.md.

Далее: отдельный fresh High-критик → адресная Medium-вторая волна по K-ID → отдельный High-сборщик SOURCES/RAW_FACTS/OPEN_QUESTIONS и обновление CRITIC → отдельный High-автор → отдельный High-редактор → отдельный High-сжиматель. Никакого финального аудитора. Ровно шесть согласованных итоговых Markdown в текущей папке.

## Единые поля синтеза

Для всех 8 сценариев сборщик сохраняет operational definition; observed object/state vs violation; positive/negative video evidence and rights; exact model/weights/revision and code/weight licenses; I/O/class mapping/pre-post; temporal tracking/geometry/confirmation/end/dedup; LinQ evidence level; measured performance scope; missing links; integration components; FP/FN/occlusion/scale/domain shift; demo conditions; verdict.

Уровни LinQ: vendor family named; exact source/export inspected; graph exported; compiled; actual device execution evidenced. Нельзя перескакивать уровни. Недостающий доступ локализовать, не превращать в доказанную несовместимость.

Метрики события: event-level TP/FP/FN с правилом сопоставления интервалов; false alerts per observed safe hour с длительностью знаменателя; duplicate notifications per incident; time-to-first-confirmed-event; notification latency; processed frame age. Предлагаемые пороги являются гипотезами, не измеренным качеством. Смена трека и пропуски времени требуют явного unknown/reset/reassociation поведения.

Все критические артефакты и проверки должны иметь фактический статус: fetched bytes / HEAD metadata only / source inspected / reported measurement / proposed not run / unavailable. Нельзя приравнивать доступную карточку к полученному архиву, LICENSE кода к лицензии весов/пикселей, чужой CPU benchmark к LinQ.

## Вторая волна по свежей критике

- W2-01: Актуальная публичная граница LinQ 2026 и оригинал performance PDF; собственный _WORK/W2-01.md; полное задание PROMPT_W2-01.md.
- W2-02: Превратить core artifact shortlist в один точный вход для первого smoke; собственный _WORK/W2-02.md; полное задание PROMPT_W2-02.md.
- W2-03: Закрыть fall data gap, не подменяя неподвижность концом ролика; собственный _WORK/W2-03.md; полное задание PROMPT_W2-03.md.
- W2-04: Moving-forklift interaction: реальные samples и юридический scope весов; собственный _WORK/W2-04.md; полное задание PROMPT_W2-04.md.
- W2-05: Running/fast movement: matched sequences и точный смысл результата; собственный _WORK/W2-05.md; полное задание PROMPT_W2-05.md.
- W2-06: Проверить огонь как полноценную альтернативу третьему сценарию; собственный _WORK/W2-06.md; полное задание PROMPT_W2-06.md.
- W2-07: Права core-поставки и четырёх review videos без обнуления CC BY; собственный _WORK/W2-07.md; полное задание PROMPT_W2-07.md.
- W2-08: Один temporal/tracker/event route, выдерживающий gaps и повторную доставку; собственный _WORK/W2-08.md; полное задание PROMPT_W2-08.md.

Все8W2 исполняются очередями по3, modelgpt-6.1-sol medium fork_turnsnone. Затем только согласованные High-роли сборщик→автор→редактор→сжиматель.
