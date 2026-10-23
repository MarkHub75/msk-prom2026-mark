# SOURCES — cv_accuracy_vast

Реестр собран только из сохранённых результатов 16 веток W1 и 7 веток W2. Нового интернет-поиска сборщик не делал. Дата доступа сетевых свидетельств — **2026-10-23**; точное время, если известно, указано в карточке/исходном branch. Дата публикации, release, commit и Last-Modified отделены от доступа. Если дата или версия не названа в карточке, значение — **unknown**; «live» не является версией. Полный source SHA, tag, опубликованный digest и вычисленный digest полученных байтов — разные поля. Карточки сохраняют эту границу.

S-ID обозначает конкретное чтение/набор тесно связанных первичных локаторов внутри branch. Повтор одного URL в разных ветках сохранён отдельным evidence record: это позволяет не смешивать разные версии, состав прочитанного и происхождение. Несколько URL внутри одной карточки перечислены явно, их отдельные роли описаны в locator. Автор и название приводятся в сохранённой карточке; если они там не установлены — **unknown**, а не угаданы по домену. Нет оснований автоматически называть первичным содержимое issue пользователя, соседний отчёт или выполненным тестом API/docs.

F-связи ниже — точные ссылки из соответствующих записей плюс branch-level контекст. Исходные определения всех source-ID сохранены; подробное обратное соответствие — [_WORK/ID_MAP.md](_WORK/ID_MAP.md). Методологические выводы и предлагаемые процедуры не являются опубликованными результатами источников.

## S001 — Официальный кейс LinQ, визуальные наблюдения root

- Автор/издатель: ООО «ХайТэк» / организаторы «Открой#Моспром» 2026. Название: «КЕЙС_LinQ.pdf»; явная версия файла/дата публикации внутри просмотренного документа **unknown**. Контекст выдачи — 23.10.2026, это отдельное сообщение задания.
- URL официальной страницы соревнования: https://hackathon2026.otkroimosprom.ru/ . Публичный direct URL точных PDF bytes **unknown**. Локальный первоисточник находился в соседнем исследовании; сохранённая переносимая provenance: [_WORK/CASE_NOTES.md](_WORK/CASE_NOTES.md).
- Доступ/визуальное чтение: 2026-10-23, все 20 raster pages, отдельно читаемые p5/7/13. PDF size 8,320,969 bytes; SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Root дополнительно локально сверил CASE_PROVENANCE и exact-byte INPUT copy: hash совпал с original, пять sheets созданы из этого PDF. Это локальное input/provenance observation, не новая сеть. Сборщик не выполнял повторный просмотр PDF.
- Locator: pp5,7,8,9,12,13,15,18,19. Тип: прямое визуальное наблюдение root, переданное в локальной записи; не OCR и не новый runtime test.
- F-связи: F001–F004, F008, F013, F017.

## S002 — Исходный договор и тематическое поручение

- Автор: пользователь / исследовательская программа команды. Названия: [Context-prompt.md](Context-prompt.md), [prompt_cv_accuracy_vast_research.md](prompt_cv_accuracy_vast_research.md). Версия общего договора `mosprom-research-v1`; точная дата редакции файлов unknown. URL: не опубликован, локальные первичные инструкции.
- Доступ: 2026-10-23. Locator: тематические §§0–3,8–11 и общий контекст §§2–6. Тип: заданный контекст, полномочия и team reports; не hardware inventory и не официальная scoring formula.
- F-связи: F002–F004, F017–F020.

## S003 — Журнал фактически выполненного исследования

- Автор: root и самостоятельные исследовательские ветки. Источник: [_WORK/RUN_STATE.md](_WORK/RUN_STATE.md), [_WORK/W2_RESOLUTION_MAP.md](_WORK/W2_RESOLUTION_MAP.md), [CRITIC.md](CRITIC.md) и сохранённые ветки. URL: локальные рабочие свидетельства, не публичные источники.
- Версия/дата: запуск с 2026-10-23T19:36:01+03:00; W2 закончена 20:50:48+03:00; collector начат 20:51:04+03:00. Доступ сборщика: 2026-10-23. Locator: хронология W1→critic→W2; K001–K011.
- Тип: процессная provenance. Фактические действия: сетевое read-only чтение primary code/docs/metadata; public offers; малый URFD CSV; release CLI wheel bytes и статическое сравнение. Не было model training/export/benchmark/GPU rental/LinQ execution.
- F-связи: F002, F010–F013, F017–F020; все branch sections ниже.

## S004 — W1-01-S01 / локальное свидетельство (W1-01-S01)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://cocodataset.org/dataset/detection-eval.htm>.

- F-связи: F022, F023.


**S004 — COCO Consortium, Detection Evaluation.** URL: https://cocodataset.org/dataset/detection-eval.htm . Версия: живая официальная документация, даты/commit страницы не закреплены; доступ 2026-10-23. Локатор: §2 Metrics, AP Across Scales, пункты 1, 2, 5–7; §3 Evaluation Code. Вид: официальный протокол. Подтверждает AP/AR по IoU и размерам, категорийное усреднение и ограничение числа detections. Условие: COCO detection evaluation, не event monitoring. Ограничение: не pinned implementation recipe, не latency-протокол; для реализации нужно закрепить evaluator commit/config.


## S005 — W1-01-S02 / локальное свидетельство (W1-01-S02)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `ebc8aebb4018a758c4efb35bb7ab547d31b1eb1e`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/activitynet/ActivityNet/ebc8aebb4018a758c4efb35bb7ab547d31b1eb1e/Evaluation/eval_detection.py>.

- F-связи: F022.


**S005 — ActivityNet authors, eval_detection.py.** Пермалинк: https://raw.githubusercontent.com/activitynet/ActivityNet/ebc8aebb4018a758c4efb35bb7ab547d31b1eb1e/Evaluation/eval_detection.py . Commit `ebc8aebb4018a758c4efb35bb7ab547d31b1eb1e`, file-last-change 2018-05-04T14:07:57Z по GitHub commits API, открыт 2026-10-23. Локатор: `ANETdetection.__init__`, `evaluate`, `compute_average_precision_detection`, особенно `lock_gt`, `tiou_thresholds`, cumulative precision/recall. Вид: первичный код. Подтверждает temporal IoU thresholds 0.5…0.95, mean AP и запрет повторного TP для одного GT. Код содержит старый Python синтаксис/urllib2; не предлагаем выполнять без адаптации. Лицензия кода здесь не проверена, копирование/интеграция не произведены, веса отсутствуют. Официальная challenge-страница найдена поиском, но повторные открытия дали timeout; фактическая опора — открытый pinned code.


## S006 — W1-01-S03 / локальное свидетельство (W1-01-S03)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://actev.nist.gov/pub/TRECVID_ActEV_2020_EvaluationPlan.pdf>.

- F-связи: F022.


**S006 — NIST, TRECVID ActEV 2020 Evaluation Plan.** URL: https://actev.nist.gov/pub/TRECVID_ActEV_2020_EvaluationPlan.pdf . Идентификатор протокола: 2020; PDF 21 стр., отдельная дата revision на доступной титульной части не установлена; доступ 2026-10-23. Локатор: §6, §6.1 и §6.2, печатные с. 11–15 (PDF indexes 10–14). Вид: официальный план/формулы. Подтверждает Pmiss по экземплярам, TFA по избыточному instance-time, non-reference denominator, one-to-one matching. У TFA повторные неперекрывающиеся фрагменты не повышают сумму длительности; совпадающие экземпляры дают кратность. Минимальный overlap протокола: 1 секунда либо половина короткого GT. Ограничение: это чужая задача/правило matching; для кратких промышленных угроз не заимствовать 1 s автоматически. Этот источник не задаёт требования к нашему FP notifications/hour.


## S007 — W1-01-S04 / локальное свидетельство (W1-01-S04)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://actev.nist.gov/sdl>.

- F-связи: F022.


**S007 — NIST, ActEV’21 Sequestered Data Leaderboard.** URL: https://actev.nist.gov/sdl . Версия evaluation 2021, живая страница без закреплённого revision; доступ 2026-10-23. Локатор: Summary; Metrics; Facilities; NIST Independent Evaluation Infrastructure. Вид: официальный протокол. Подтверждает real-time-or-faster оценку, ограничение засчитываемого вывода при runtime сверх real time, отдельные known/unknown facility задачи. Ограничение: это не измерение LinQ и не современный speed benchmark моделей; оборудование NIST не переносится на TPU. Их time-limited score также не равен нашей per-event end-to-end задержке.


## S008 — W1-01-S05 / локальное свидетельство (W1-01-S05)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.hse.gov.uk/humanfactors/topics/alarm-management.htm>.

- F-связи: F022, F024.


**S008 — UK Health and Safety Executive, Alarm management.** URL: https://www.hse.gov.uk/humanfactors/topics/alarm-management.htm . Живая страница, дата публикации не указана; доступ 2026-10-23. Локатор: Key principles of alarm management, пункты 1–5. Вид: первичная ведомственная guidance. Подтверждает связь сигнала с нужным действием, временем для ответа и возможностями человека. Ограничение: guidance по alarm management; нет порогов accuracy или FP/камеро-час для CV. Отсюда не следует конкретная вероятность правильного ответа оператора.


## S009 — W1-01-S06 / локальное свидетельство (W1-01-S06)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm>.

- F-связи: F022.


**S009 — UK HSE, Control systems.** URL: https://www.hse.gov.uk/comah/sragtech/techmeascontsyst.htm . Живая Technical Measure guidance, дата revision не установлена; доступ 2026-10-23. Локатор: Alarm systems → Alarm processing; Alarm system management procedures; Alarm settings. Вид: первичная guidance. Подтверждает необходимость контроля повторных/кратких alarm, нагрузки, response time, документированных параметров и контролируемого suppression. Ограничение: контекст process safety/COMAH; описанные safety requirements не означают сертификацию CV-прототипа. Пороговые числа и SIL claims в наше решение не перенесены.


## S010 — W1-01-S07 / локальное свидетельство (W1-01-S07)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432>.

- F-связи: F024.


**S010 — Takaya Saito, Marc Rehmsmeier (2015).** The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. PLOS ONE 10(3), e0118432, опубликовано 2015-03-04. URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432 . Доступ 2026-10-23. Локатор: Abstract; Introduction; Results, comparison of balanced and imbalanced datasets. Вид: первичная исследовательская статья/симуляции. Подтверждает необходимость смотреть precision/recall при дисбалансе и осторожно интерпретировать ROC. Условия: бинарные классификаторы и рассмотренные датасеты, не industrial event alarms. Наша формула prevalence и контрпример — алгебраические иллюстрации, не опубликованные измерения на заводе.


## S011 — W1-01-S08 / локальное свидетельство (W1-01-S08)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `7.2.4.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm>.

- F-связи: F022, F025.


**S011 — NIST/SEMATECH e-Handbook, §7.2.4.1 Confidence intervals.** URL: https://itl.nist.gov/div898/handbook/prc/section2/prc241.htm . Живая страница без зафиксированной даты редакции; доступ 2026-10-23. Локатор: Wilson interval formula и Exact Intervals for Small Numbers of Failures. Вид: официальное статистическое руководство. Подтверждает Wilson и проблемы обычного normal interval, exact binomial подход при малой выборке/ошибках. Условия: binomial sampling; не доказывает независимость видеоэпизодов.


## S012 — W1-01-S09 / локальное свидетельство (W1-01-S09)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf>.

- F-связи: F025.


**S012 — Zhan-Qian John Lu, NIST Technical Note 2119.** Estimating Instrument Performance: with Confidence Intervals and Confidence Bounds, September 2020, DOI 10.6028/NIST.TN.2119. URL: https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf . Доступ 2026-10-23. Локатор: §§1.1–1.4; 2.3; 2.5; 3.1–3.3; 4.1. Вид: техническая монография статистики испытаний. Подтверждает различение probability of detection/false alarm и интервальных границ, Wilson/exact подходы, осторожность при rare events. Ограничение: не готовая процедура clustered video bootstrap и не гарантия field reliability; такую часть выше мы предлагаем отдельно.


## S013 — W1-01-S10 / локальное свидетельство (W1-01-S10)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cipoisson.html>.

- F-связи: F022, F025.


**S013 — R survival maintainers, cipoisson manual.** URL: https://stat.ethz.ch/R-manual/R-devel/library/survival/html/cipoisson.html . На открытой странице указан package `survival 3.8-6`, доступ 2026-10-23; `R-devel` — подвижный URL. Локатор: Usage, arguments `k`, `time`, `p`, `method`; Details; Examples. Вид: первичная документация статистического пакета. Подтверждает оценивание CI интенсивности Poisson по count и exposure и различие exact/Anscombe. Ограничение: не pinned execution environment; код не запускался. Применимость к пачкам зависимых ложных тревог не гарантирована.


## S014 — W1-01-S11 / локальное свидетельство (W1-01-S11)

- Provenance: [W1-01](_WORK/W1_01.md); исходная карточка `W1-01-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards>.

- F-связи: F021, F022, F023, F024, F025, F026, F027, F028, F029.


**S014 — ISA, ISA-18 Series of Standards, каталог.** URL: https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards . Доступ 2026-10-23. Локатор: перечисления ISA-18.2-2016 и TR18.2.5-2022. Вид: официальный каталог, а не прочитанный полный стандарт. Использование ограничено проверкой названия/редакции; количественные таблицы не заимствованы. Полный стандарт за paywall не приобретался, не скачивался и не объявлен выполненным. Поиск возвращал сторонние таблицы «допустимых alarms/hour», но они не приняты как норматив нашего CV и не использованы для выбора порогов.


## S015 — YOLO26 docs pinned (W1-02-S01)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo26.md>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py>.

- F-связи: F030, F033, F036, F037.


| S015 | Ultralytics, [YOLO26 docs pinned](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo26.md), `Supported Tasks`, `Dual-Head Architecture`, P2/P6 note, `Availability and Licensing`; [init version](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py), line3 | Авторская документация+Code; n/s/m/l/x, fine-tune/export; нет target-доказательств |


## S016 — performance macro (W1-02-S02)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`, `v8.4.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/macros/yolo-det-perf.md>; <https://api.github.com/repos/ultralytics/assets/releases/tags/v8.4.0>.

- F-связи: F030, F033, F035, F037.


| S016 | Ultralytics, [performance macro](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/macros/yolo-det-perf.md), строки1–7; [asset API](https://api.github.com/repos/ultralytics/assets/releases/tags/v8.4.0), assets yolo26n/s/m `digest`, `updated_at` | Reported COCO dense/e2e и T4 TensorRT10; release metadata SHA256, бинарник не скачан |


## S017 — D-FINE README pinned (W1-02-S03)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/LICENSE>.

- F-связи: F030, F033, F036.


| S017 | Yansong Peng et al., [D-FINE README pinned](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md), `Model Zoo/COCO/Objects365`, latency/license note; [LICENSE](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/LICENSE) | Reported AP/latency T4 batch1 FP16 TRT10.4; official checkpoint links, O365 caveat. Авторское demo не controlled robustness benchmark |


## S018 — export_onnx.py (W1-02-S04)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/dfine_hgnetv2_m_coco.yml>.

- F-связи: F030, F035.


| S018 | D-FINE authors, [export_onnx.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py), `Model`, dummy tensor, `dynamic_axes`, `torch.onnx.export`; [M config](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/dfine_hgnetv2_m_coco.yml), `optimizer`, `epochs` | Code: deploy+postprocessor, batch32 dummy/dynamic0/opset16; config includes должны сохраняться. Это прочитанный экспортный рецепт, не выполненный экспорт |


## S019 — README pinned (W1-02-S05)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/README.md>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/pyproject.toml>.

- F-связи: F030, F033, F037.


| S019 | Roboflow, [README pinned](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/README.md), `Benchmarks/Detection`, `License`; [pyproject](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/pyproject.toml), version/dependencies | Reported in-house SAB COCO val2017 5000, T4 FP16 TensorRT batch1; development snapshot; внешняя валидность ограничена |


## S020 — exporter.py pinned (W1-02-S06)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py>.

- F-связи: F030, F035.


| S020 | Ultralytics, [exporter.py pinned](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py), `model.end2end = self.args.nms is False`, backend override block, TensorRT compatibility block | Code; доказывает семантику именно этого SHA, не любой версии; backend может переопределить head |


## S021 — weights registry (W1-02-S07)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/assets/model_weights.py>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/config.py>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/exports/onnx.md>.

- F-связи: F033, F035, F037.


| S021 | Roboflow, [weights registry](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/assets/model_weights.py), `ModelWeightAsset`, `RF_DETR_LARGE_2026`, SMALL/MEDIUM; [config](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/config.py), RFDETR*Config; [ONNX contract](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/exports/onnx.md), raw outputs/class layout | Code+docs; MD5 authored registry, current resolution/checkpoint; raw contract; не реальная проверка байтов/паритета |


## S022 — train/index.md (W1-02-S08)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/learn/train/index.md>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/learn/train/advanced.md>.

- F-связи: F030, F034.


| S022 | Roboflow, [train/index.md](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/learn/train/index.md), `Quick Start`, batch/memory note; [advanced](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/learn/train/advanced.md), memory/training options | Авторский fine-tune API; CUDA auto batch/accumulation. Не GPU-fit evidence. FP8 инструкции не используются как рецепт для 3090 |


## S023 — v2 PyTorch README (W1-02-S09)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `df2a96c8c3a098567a1149bf0248da6efe6d495d`, `8.5.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/README.md>; <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/LICENSE>.

- F-связи: F030, F033.


| S023 | Wenyu Lyu / RT-DETR authors, [v2 PyTorch README](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/README.md), `Model Zoo`, `Different Sampling Methods`, `Usage`; [LICENSE](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/LICENSE) | Reported T4 batch1 FP16 TRT≥8.5.1, configs/weights/recipes. DSP AP и обычный S AP относятся к разным checkpoint |


## S024 — v2 exporter (W1-02-S10)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `df2a96c8c3a098567a1149bf0248da6efe6d495d`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/tools/export_onnx.py>; <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/src/zoo/rtdetr/utils.py>; <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/configs/rtdetrv2/rtdetrv2_r18vd_dsp_3x_coco.yml>.

- F-связи: F035.


| S024 | RT-DETR authors, [v2 exporter](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/tools/export_onnx.py), `dynamic_axes`/`opset_version`; [sampling utils](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/src/zoo/rtdetr/utils.py), `deformable_attention_core_func_v2`; [DSP config](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/configs/rtdetrv2/rtdetrv2_r18vd_dsp_3x_coco.yml) | Code; sampling operator distinction, rectangle FIXME, dynamic batch; никакой LinQ compatibility claim |


## S025 — README (W1-02-S11)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `55fefaaed7efe2a5f72d0a18fd4e05965e35c292`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/README.md>; <https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/LICENSE>.

- F-связи: F030, F033.


| S025 | RT-DETRv4 authors, [README](https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/README.md), `Model Zoo`, `Training`, DINOv3 teacher settings; [LICENSE](https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/LICENSE) | Reported T4 metrics, configs/Google Drive links; full latency stack и отдельная license weight manifest не установлены |


## S026 — YOLOX README (W1-02-S12)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6ddff4824372906469a7fae2dc3206c7aa4bbaee`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/README.md>; <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE>.

- F-связи: F030, F033.


| S026 | Zheng Ge et al./Megvii, [YOLOX README](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/README.md), `Standard Models`, `Deployment`; [LICENSE](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE) | Reported V100, COCO val/test отдельно; anchor-free CNN fallback, ссылки export; возраст и новая target-точность не скрыты |


## S027 — YOLO27 preview pinned (W1-02-S13)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo27.md>; <https://docs.ultralytics.com/models>.

- F-связи: F030, F037.


| S027 | Ultralytics, [YOLO27 preview pinned](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo27.md), `Coming Soon`/availability; [models live](https://docs.ultralytics.com/models) | Отрицательная находка: preview не released candidate. Live page использована только для проверки наличия, не pinned recipe |


## S028 — COCO class schema (W1-02-S14)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/datasets/coco.yaml>.

- F-связи: F030.


| S028 | Ultralytics, [COCO class schema](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/datasets/coco.yaml), `names` | Code, 80-class schema; доказывает наличие phone/person и отсутствие PPE в данной голове, не невозможность fine-tuning |


## S029 — DEIMv2 LICENSE.md (W1-02-S15)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `f005f50ce565e63f6c298feccb51901a98c3d035`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Intellindust-AI-Lab/DEIMv2/blob/f005f50ce565e63f6c298feccb51901a98c3d035/LICENSE.md>; <https://github.com/Intellindust-AI-Lab/DEIMv2/blob/f005f50ce565e63f6c298feccb51901a98c3d035/README.md>.

- F-связи: F033, F037.


| S029 | INTELLINDUST, [DEIMv2 LICENSE.md](https://github.com/Intellindust-AI-Lab/DEIMv2/blob/f005f50ce565e63f6c298feccb51901a98c3d035/LICENSE.md), §§1–6; [README](https://github.com/Intellindust-AI-Lab/DEIMv2/blob/f005f50ce565e63f6c298feccb51901a98c3d035/README.md), Updates2026-10-22/2026-01-07, Model Zoo | Прямой license text и reported compatibility warning; non-commercial материалы/веса, не Apache. FLOPs correction — отрицательная находка о старых сравнениях |


## S030 — EdgeCrafter README (W1-02-S16)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `d8752b75c9beaecfcdd0e5cd207bae3b6946ae23`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Intellindust-AI-Lab/EdgeCrafter/blob/d8752b75c9beaecfcdd0e5cd207bae3b6946ae23/README.md>; <https://github.com/Intellindust-AI-Lab/EdgeCrafter/blob/d8752b75c9beaecfcdd0e5cd207bae3b6946ae23/LICENSE.md>.

- F-связи: F033, F037.


| S030 | INTELLINDUST / Longfei Liu et al., [EdgeCrafter README](https://github.com/Intellindust-AI-Lab/EdgeCrafter/blob/d8752b75c9beaecfcdd0e5cd207bae3b6946ae23/README.md), detection table; [LICENSE.md](https://github.com/Intellindust-AI-Lab/EdgeCrafter/blob/d8752b75c9beaecfcdd0e5cd207bae3b6946ae23/LICENSE.md), §§2/5/6 | Reported T4 batch1 FP16 TRT10.6; own non-commercial license; reserve, не proven target candidate |


## S031 — arXiv:2509.20787v4 (W1-02-S17)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S17`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2509.20787v4>.

- F-связи: F037.


| S031 | Shihua Huang et al., [arXiv:2509.20787v4](https://arxiv.org/abs/2509.20787v4), submitted2025-09-25/revised2026-01-26, abstract | Paper: DEIMv2 DINOv3/STA vs lightweight HGNetv2, AP/params; не industrial benchmark |


## S032 — arXiv:2511.09554v2 (W1-02-S18)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S18`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2511.09554v2>.

- F-связи: F037.


| S032 | Isaac Robinson, Peter Robicheaux, Matvei Popov, Deva Ramanan, Neehar Peri, [arXiv:2511.09554v2](https://arxiv.org/abs/2511.09554v2), v1 2025-11-12/v2 2026-02-03, abstract/domain adaptability | Paper, RF100-VL/NAS claims; не наш dataset, не LinQ; paper numbers не смешаны с newer weights |


## S033 — YOLOX ONNXRuntime README pinned (W1-02-S19)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S19`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6ddff4824372906469a7fae2dc3206c7aa4bbaee`, `0.1.1rc0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/README.md>; <https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx>.

- F-связи: F030, F031, F032, F033, F034, F035, F036, F037, F038, F039, F040.


**S033.** Megvii, [YOLOX ONNXRuntime README pinned](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/README.md), `Convert Your Model to ONNX`: `tools/export_onnx.py -n yolox-s -c yolox_s.pth`, default opset11, dummy batch1, custom experiment через `-f`. Это авторский рецепт, не выполненный экспорт. Есть [готовая авторская ONNX-ссылка](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx); её hash/байты/совместимость не проверялись.


## S034 — M config pinned (W1-02-S20)

- Provenance: [W1-02](_WORK/W1_02.md); исходная карточка `W1-02-S20`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `55fefaaed7efe2a5f72d0a18fd4e05965e35c292`, `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/configs/rtv4/rtv4_hgnetv2_m_coco.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dfine_hgnetv2.yml>.

- F-связи: F030, F031, F032, F033, F034, F035, F036, F037, F038, F039, F040.


**S034.** RT-DETRv4 authors, [M config pinned](https://github.com/RT-DETRs/RT-DETRv4/blob/55fefaaed7efe2a5f72d0a18fd4e05965e35c292/configs/rtv4/rtv4_hgnetv2_m_coco.yml), include `../dfine/dfine_hgnetv2_m_coco.yml`, teacher DINOv3, optimizer, `epoches:102`; дочерние include ведут к `eval_spatial_size:[640,640]`. D-FINE authors, [D-FINE inference config](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dfine_hgnetv2.yml), `eval_spatial_size:[640,640]`. Code, подтверждение размеров и training-only teacher, не latency/VRAM evidence.


## S035 — Полный HTML v2 (W1-03-S01)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2303.07399v2>.

- F-связи: F041, F042, F043, F044, F045, F046, F047.


### S035 — RTMPose paper

Tao Jiang et al., *RTMPose: Real-Time Multi-Person Pose Estimation based on MMPose*, arXiv **2303.07399v2**, 2023-07-03 (v1 2023-03-13). [Полный HTML v2](https://arxiv.org/html/2303.07399v2), локаторы §2, §3.5, §4/Table 4 и Tables 8–10. Вид: авторская статья и опубликованные измерения. Прочитан основной текст, включая сравнение paradigm и inference pipeline.

Свидетельство: RTMPose — top-down; SimCC разделяет координатное предсказание. В §3.5 описаны skip-frame detector, pose-based boxes между детекциями, OKS NMS и OneEuro smoothing. В Table 4 при одинаковом RTMPose-m результат с RTMDet-nano 73.2 AP, с RTMDet-m 75.7 AP: detector materially affects pipeline. Главный предел — COCO, чужая аппаратура и определенный pipeline; эти AP/FPS не обосновывают recall industrial falls или LinQ speed. Основной вывод F02 не зависит от переноса их цифр.


## S036 — Demo (W1-03-S02)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v1.3.2`, `5408bc76f5b848cf925a0d1857899011d8c5b497`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/demo/topdown_demo_with_mmdet.py>; <https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/configs/body_2d_keypoint/rtmpose/coco/rtmpose-s_8xb256-420e_coco-256x192.py>.

- F-связи: F044.


### S036 — MMPose интеграционный код и config

OpenMMLab contributors, MMPose **v1.3.2 / 5408bc76f5b848cf925a0d1857899011d8c5b497**. [Demo](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/demo/topdown_demo_with_mmdet.py), локатор `process_one_image`, `--save-predictions`; [config](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/configs/body_2d_keypoint/rtmpose/coco/rtmpose-s_8xb256-420e_coco-256x192.py), локаторы `codec`, `model`, `val_pipeline`. Вид: чтение исходников; raw файлы успешно получены по HTTPS через PowerShell.

Подтверждает цепь detector→filter/NMS→pose и явные параметры преобразования данных. Demo — не production tracker и не event detector; порядок результатов и track identity нужно реализовать. Наличие Python API не означает поддержку графа на LinQ TPU.


## S037 — RTMPose README (W1-03-S03)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5408bc76f5b848cf925a0d1857899011d8c5b497`, `1.8.1`, `1.14.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/projects/rtmpose/README.md>; <https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/LICENSE>; <https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/LICENSES.md>; <https://github.com/open-mmlab/mmpose/tree/5408bc76f5b848cf925a0d1857899011d8c5b497/projects/rtmpose/examples/onnxruntime>.

- F-связи: F047.


### S037 — model zoo, условия скорости, лицензии

OpenMMLab contributors, тот же pinned commit. [RTMPose README](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/projects/rtmpose/README.md), локаторы `Pipeline Performance / Notes`, `Model Zoo / AIC+COCO`, `Body8`; [LICENSE](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/LICENSE), [LICENSES.md](https://github.com/open-mmlab/mmpose/blob/5408bc76f5b848cf925a0d1857899011d8c5b497/LICENSES.md); [ORT example](https://github.com/open-mmlab/mmpose/tree/5408bc76f5b848cf925a0d1857899011d8c5b497/projects/rtmpose/examples/onnxruntime). Вид: авторские инструкции/таблицы и статический код.

Главный факт: pipeline latency дана при detection interval=5 frames и без flip test; рядом model zoo применяет flip test. Не сравнивать эти колонки как одинаковые испытания. `Body8` включает OCHuman для evaluation сверх семи обучающих наборов — это не доказательство обучения на OCHuman. ORT README/requirements расходятся по версиям CPU runtime (1.8.1/1.14.1), dependencies и MMDeploy clone не полностью pinned. Пример полезен как описание преобразований, не готовый lockfile. Отдельная лицензия конкретных RTMPose весов не установлена.


## S038 — Полный HTML v2 (W1-03-S04)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1812.00324v2>.

- F-связи: F044.


### S038 — толпа и перепутанные суставы

Jiefeng Li et al., *CrowdPose: Efficient Crowded Scenes Pose Estimation and A New Benchmark*, **arXiv 1812.00324v2, 2019-01-23**, CVPR 2019 pp.10863–10872. [Полный HTML v2](https://arxiv.org/html/1812.00324v2), локаторы §1/Fig.1/Fig.3, §4 crowd index, §5.4. Вид: статья с авторскими экспериментами.

Свидетельство: ошибки в crowd — неправильное объединение суставов разных людей и дубли pose; ухудшение затрагивает top-down и bottom-up. Статья мотивирует отдельный benchmark crowd. Исторические разницы AP не переносить как размер деградации RTMPose в цехе. Причина использовать источник — виды отказов и необходимость стратификации, а не выбор их старой модели.


## S039 — Авторский PDF (W1-03-S05)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pengzhansun.github.io/files/1484.pdf>.

- F-связи: F041, F042, F043, F044, F045, F046, F047.


### S039 — невидимые точки и редкая поза лежа

Pengzhan Sun, Kerui Gu, Yunsong Wang, Linlin Yang, Angela Yao, *Rethinking Visibility in Human Pose Estimation: Occluded Pose Reasoning via Transformers*, WACV **2024**, pp.5903–5912. [Авторский PDF](https://pengzhansun.github.io/files/1484.pdf), локаторы §1 pp.1–2, §5.4/Table 5, §6/Fig.5 pp.7–8 PDF (printed 5909–5910). Вид: первичная статья.

Свидетельство: невидимые суставы не имеют прямого визуального подтверждения; авторы разделяют visibility prediction и координатное reasoning. В собственных limitations остаются severe occlusion и редкая лежащая поза, когда видимых точек недостаточно. Это особенно существенно для fall branch: хорошие средние показатели pose не гарантируют качество именно конечного положения события. Не заявляется, что данный модуль внедрен в RTMPose или у нас.


## S040 — Издатель (W1-03-S06)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `4.3.2`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.mdpi.com/1424-8220/20/23/6966>; <https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7729773/fullTextXML>.

- F-связи: F045.


### S040 — временная логика на геометрии

Kun Han, Qiongqian Yang, Zefan Huang, *A Two-Stage Fall Recognition Algorithm Based on Human Posture Features*, Sensors **2020, 20(23),6966**, published 2020-12-05, DOI 10.3390/s20236966. [Издатель](https://www.mdpi.com/1424-8220/20/23/6966), [полный XML первичной статьи через Europe PMC](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7729773/fullTextXML), локаторы §3.3–3.4/Algorithm 4, §4.1, §4.3.2, §4.4/Table 3. XML реально прочитан HTTPS-запросом; MDPI open дал 429, PMC HTML — browser check. Вид: статья, не независимая репликация.

Свидетельство: углы/отношения позы дополняются временной стадией и SVM для разделения падений и похожих ADL. Для FDD указаны 191 видео, 25 FPS, 320×240; классификаторы сравниваются на трехfold CV выбранных фрагментов. Камера-/сцена-/subject-disjoint split для такого выбора в прочитанном описании не установлен. Публикация не обосновывает заимствование фиксированных углов и окон в наш FPS. Ее высокий reported accuracy не используется как ожидаемый результат или вероятность успеха.


## S041 — Полный HTML (W1-03-S07)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2004.00797v2>.

- F-связи: F041, F045.


### S041 — контрпример тезису «single-frame fall models не существуют»

Umar Asif, Stefan Von Cavallar, Jianbin Tang, Stefan Harrer (IBM Research Australia), *SSHFD: Single Shot Human Fall Detection with Occluded Joints Resilience*, **arXiv 2004.00797v2, 2020-04-03**. [Полный HTML](https://arxiv.org/html/2004.00797v2), локаторы §3.1–3.5, §4.2, Table 1, Fig.6. Вид: авторская статья.

Свидетельство: модель классифицирует fall/no-fall из одного изображения, используя 2D/восстановленную 3D позу и synthetic training. Fig.6 иллюстрирует неоднозначность 2D проекций; §3.5 — распространение ошибок исходного pose на downstream. Это подтверждает существование single-frame классификации, но не наблюдение причины лежания или temporal event onset. Learned 3D prior не равен измеренной глубине. На внедрение SSHFD с лицензированными весами/воспроизводимым запуском здесь не претендуем.


## S042 — Pose docs (W1-03-S08)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v8.3.0`, `6e43d1e1e5db72afbf686dee6745669bcb124b0a`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/docs/en/tasks/pose.md>; <https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/results.py>; <https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/LICENSE>; <https://www.ultralytics.com/license>.

- F-связи: F044.


### S042 — Ultralytics versioned pose и missing coordinates

Ultralytics contributors, **v8.3.0 / 6e43d1e1e5db72afbf686dee6745669bcb124b0a**, 2024-09-30 tag. [Pose docs](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/docs/en/tasks/pose.md), [results.py](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/results.py), локатор `class Keypoints`, `__init__`, `conf`; [LICENSE](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/LICENSE). Вид: чтение кода; tag разрешен через GitHub API, исходники открыты raw HTTPS.

17 COCO points и API дают короткий альтернативный путь. В `Keypoints.__init__` coordinates при score<0.5 обнуляются; mask обязательна. Репозиторий AGPL-3.0. [Текущая официальная политика весов](https://www.ultralytics.com/license), локатор FAQ «Are Ultralytics YOLO trained models licensed under the AGPL-3.0 license?», прочитана отдельно; это live page 2026, не versioned model card старого checkpoint.


## S043 — source keypoints-eval.htm (W1-03-S09)

- Provenance: [W1-03](_WORK/W1_03.md); исходная карточка `W1-03-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/keypoints-eval.htm>.

- F-связи: F041, F042, F043, F044, F045, F046, F047.


### S043 — COCO OKS не удостоверяет дальнего человека

COCO Consortium, официальная страница evaluation, [source keypoints-eval.htm](https://raw.githubusercontent.com/cocodataset/cocodataset.github.io/master/dataset/keypoints-eval.htm); live master, commit **не закреплен**, поэтому источник определений, не исполнимый рецепт. Локаторы §1.2, §2/Metrics и примечания 4–6. Вид: официальная спецификация метрики.

Описаны v=0/1/2 в GT и OKS, зависящий от масштаба объекта. Predicted visibility не входит в OKS. Для keypoints показаны medium/large; small с segment area<32² не имеют keypoint annotations, crowd/без точек обрабатывается lenient matching. Следовательно, обычный общий COCO AP не является прямым свидетельством пригодности на дальних людях и не калибрует confidence для отказа от решения.


## S044 — arXiv:1811.08383v2 (W1-04-S01)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1811.08383v2>; <https://github.com/mit-han-lab/temporal-shift-module/tree/1f6a834b02120441d99fa706b7a13ccc5293c6fa>; <https://raw.githubusercontent.com/mit-han-lab/temporal-shift-module/1f6a834b02120441d99fa706b7a13ccc5293c6fa/LICENSE>.

- F-связи: F048, F049.


**S044 — Ji Lin, Chuang Gan, Song Han, TSM.** [arXiv:1811.08383v2](https://arxiv.org/html/1811.08383v2), 2019-03-28; ICCV paper отдельно найден. Локатор §3.2, §4.1–4.2/Fig.4, §5.5. Вид: первичная статья. Bi/uni-directional shift, cached features и memory movement; результаты на action benchmarks/их hardware, не LinQ. [Code commit](https://github.com/mit-han-lab/temporal-shift-module/tree/1f6a834b02120441d99fa706b7a13ccc5293c6fa) разрешён GitHub API; [LICENSE](https://raw.githubusercontent.com/mit-han-lab/temporal-shift-module/1f6a834b02120441d99fa706b7a13ccc5293c6fa/LICENSE) открыт: MIT, copyright 2021 MIT HAN Lab. Веса не выбраны; это не проверка прав каждого checkpoint.


## S045 — arXiv:2103.11511v2 (W1-04-S02)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `3.2.2`, `4.3.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2103.11511v2>; <https://arxiv.org/pdf/2103.11511.pdf>.

- F-связи: F048, F049, F050.


**S045 — Dan Kondratyuk et al., Google Research, MoViNets.** [arXiv:2103.11511v2](https://arxiv.org/html/2103.11511v2), 2021-04-18, CVPR 2021; [PDF](https://arxiv.org/pdf/2103.11511.pdf) открыт. Локатор §3.2–3.2.2, §4.3.1, Appendix B.1/C.4–C.6. Вид: статья/измерения авторов. Stream buffers/causal ops дают последовательное исполнение с memory footprint, постоянным по полной длине. Это не отсутствие state. Частоты/длины проверены на action datasets, не arbitrary stream gaps. Квантованный TFLite/CPU benchmark не доказывает LinQ. Deployment checkpoint/license не выбраны.


## S046 — arXiv:1812.03982v3 (W1-04-S03)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1812.03982v3>.

- F-связи: F048, F050.


**S046 — Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, Kaiming He, SlowFast.** [arXiv:1812.03982v3](https://arxiv.org/html/1812.03982v3), 2019-10-29, ICCV 2019. Локатор §3.1–3.4/Table1, §4–5. Вид: статья. Разные temporal rates для semantics и fine motion; конкретные clip/stride. Kinetics/Charades/AVA не определяют sampling для короткого цехового события. Архитектурный comparator, не pinned deployment weights/recipe.


## S047 — arXiv:2104.13586v2 (W1-04-S04)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2104.13586v2>.

- F-связи: F048, F049, F050.


**S047 — Haodong Duan, Yue Zhao, Kai Chen, Dahua Lin, Bo Dai, Revisiting Skeleton-based Action Recognition.** [arXiv:2104.13586v2](https://arxiv.org/html/2104.13586v2), 2022-04-02, CVPR 2022. Локатор §3.1–3.3, §4.2/Tables4–5. Вид: статья/controlled tests. PoseC3D heatmap volume, clip-based crop/uniform sampling. Perturbation удаляет отдельные keypoints, **не burst frames/IDs**. Head FLOPs не равны detector+pose cost. Live sampling/crop требуют причинного варианта и переоценки; веса не выбраны.


## S048 — arXiv:2110.06864v3 (W1-04-S05)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2110.06864v3>; <https://github.com/FoundationVision/ByteTrack>.

- F-связи: F048, F051.


**S048 — Yifu Zhang et al., ByteTrack.** [arXiv:2110.06864v3](https://arxiv.org/html/2110.06864v3), версия 2022-04-07, ECCV 2022; локатор §3, AppendixD/Table11, AppendixE. Вид: статья. Second association использует low-score boxes; interpolation t1–t2 использует будущий конец gap. Отказ от неё для live — наш вывод. [Official README](https://github.com/FoundationVision/ByteTrack) открыт: test instructions вызывают `tools/interpolation.py`, местами предлагают per-sequence tuning. Такой test tuning запрещён нашим lockbox контрактом. MOT score не доказывает event alarm quality.


## S049 — Manual (W1-04-S06)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://gstreamer.freedesktop.org/documentation/application-development/advanced/clocks.html>; <https://gstreamer.freedesktop.org/documentation/additional/design/synchronisation.html>.

- F-связи: F050.


**S049 — GStreamer maintainers, Clocks and synchronization.** [Manual](https://gstreamer.freedesktop.org/documentation/application-development/advanced/clocks.html), [Synchronization design](https://gstreamer.freedesktop.org/documentation/additional/design/synchronisation.html). Живые страницы без revision; локаторы Clock/Buffer running-time, Timestamps. Вид: официальная документация. Timestamp интерпретируется вместе с SEGMENT; clock/base-time задают running-time. Не доказывает точный exposure timestamp камеры. Концептуальное основание, не pinned pipeline recipe.


## S050 — API (W1-04-S07)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://gstreamer.freedesktop.org/documentation/coreelements/queue.html>.

- F-связи: F050.


**S050 — GStreamer queue.** [API](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), live без revision. Локаторы Description, `current-level-time`, `max-size-*`, `leaky`/`Queue-leaky`; `notify-levels`: Since 1.26. Вид: official docs. Queue может блокировать или удалять old/new buffers; levels наблюдаемы. API не означает установленную версию. Concrete pipeline/SDK проверить на LinQ.


## S051 — Official tutorial (W1-04-S08)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `f8af2291cced43fc9f1d9b41ddbf772ae7b0d7d2`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.tensorflow.org/hub/tutorials/movinet>.

- F-связи: F049.


**S051 — TensorFlow authors, MoViNet streaming tutorial.** [Official tutorial](https://www.tensorflow.org/hub/tutorials/movinet), live; локаторы Streaming model/`init_states`, frame-by-frame `logits, states`. Вид: пример авторов, **не запускался здесь**. Явные state I/O и preprocessing, не industrial background detector. Labels/assets привязаны внутри tutorial к `tensorflow/models` commit `f8af2291cced43fc9f1d9b41ddbf772ae7b0d7d2`; это не pin runtime/weights. Старые pip-команды без compatibility check не переносить.


## S052 — 4.13.0 tutorial (W1-04-S09)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `4.13.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html>.

- F-связи: F051.


**S052 — OpenCV authors, Optical Flow.** [4.13.0 tutorial](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html); `/4.x/` перенаправился сюда. Локаторы Optical Flow assumptions, Lucas-Kanade, Dense Flow. Вид: official docs. Apparent motion возникает от объекта/камеры; assumptions интенсивностей/сходства соседнего motion. Это не classifier нарушения и не оценка нашей точности.


## S053 — byte_tracker.py (W1-04-S10)

- Provenance: [W1-04](_WORK/W1_04.md); исходная карточка `W1-04-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py>; <https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py>; <https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/LICENSE>.

- F-связи: F051.


**S053 — FoundationVision/ByteTrack implementation.** Commit `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`, date 2022-12-11; main разрешён GitHub API 2026-10-23. Открыты [byte_tracker.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py), строки 133–147 и association; [kalman_filter.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py), строки 21–49; [LICENSE](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/LICENSE): MIT, copyright 2021 Yifu Zhang. Вид: чтение кода без выполнения. TTL в update frames, dt=1. Конкретная версия, не все реализации. Detector weights/rights не проверены.


## S054 — W1-05-S01 / локальное свидетельство (W1-05-S01)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `07.04.2022`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2110.06864v3>.

- F-связи: F055, F057.


| S054 | Yifu Zhang et al., **2110.06864v3**, 07.04.2022, ECCV2022 | https://arxiv.org/html/2110.06864v3 — §3 Algorithm 1, §4, appendix D | Paper: low-score association; MOT17/V100 author-system claims |


## S055 — W1-05-S02 / локальное свидетельство (W1-05-S02)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`, `11.12.2022`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/FoundationVision/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99>.

- F-связи: F055, F058.


| S055 | FoundationVision/ByteTrack, **d1bf0191adff59bc8fcfeaa0b33d3d1642552a99**, 11.12.2022 | https://github.com/FoundationVision/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99 — `yolox/tracker/byte_tracker.py`: BYTETracker.__init__/update, STrack.re_activate, remove_duplicate_stracks; `kalman_filter.py::__init__`; LICENSE | Read code, MIT. Buffer/frame units/dt. Duplicate track removal не равно event dedup |


## S056 — W1-05-S03 / локальное свидетельство (W1-05-S03)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `07.07.2022`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2206.14651v2>.

- F-связи: F055, F056, F057, F058, F059, F060, F061, F062, F063.


| S056 | Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky, **2206.14651v2**, 07.07.2022 | https://arxiv.org/html/2206.14651v2 — §§3.1–3.3, §4.4 | Paper: KF/GMC/ReID и failure of GMC при нехватке background |


## S057 — W1-05-S04 / локальное свидетельство (W1-05-S04)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `251985436d6712aaf682aaaf5f71edb4987224bd`, `30.10.2022`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/NirAharon/BoT-SORT/tree/251985436d6712aaf682aaaf5f71edb4987224bd>.

- F-связи: F055, F058.


| S057 | NirAharon/BoT-SORT, **251985436d6712aaf682aaaf5f71edb4987224bd**, 30.10.2022 | https://github.com/NirAharon/BoT-SORT/tree/251985436d6712aaf682aaaf5f71edb4987224bd — tracker/bot_sort.py BOTSORT.__init__/update, STrack.update_features; kalman_filter.py; LICENSE | Read code, MIT. Encoder gated with_reid; fixed frame counts; не TPU certification |


## S058 — W1-05-S05 / локальное свидетельство (W1-05-S05)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `16.03.2023`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2203.14360v3>.

- F-связи: F057.


| S058 | Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani, **2203.14360v3**, 16.03.2023, CVPR2023 | https://arxiv.org/html/2203.14360v3 — §§3–4, §5.1, appendix B.2 | Paper: ORU/OCM/OCR; OCR для stops/short loss; speed excludes detector; offline interpolation отдельно |


## S059 — W1-05-S06 / локальное свидетельство (W1-05-S06)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `8462e7e729a93ccd3bd995c0a79a890336cb3a0b`, `21.04.2026`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/noahcao/OC_SORT/tree/8462e7e729a93ccd3bd995c0a79a890336cb3a0b>.

- F-связи: F055, F058.


| S059 | noahcao/OC_SORT, **8462e7e729a93ccd3bd995c0a79a890336cb3a0b**, 21.04.2026 | https://github.com/noahcao/OC_SORT/tree/8462e7e729a93ccd3bd995c0a79a890336cb3a0b — trackers/ocsort_tracker/ocsort.py, KalmanBoxTracker/OCSort.update/k_previous_obs; LICENSE | Read code, MIT. Новый refactored pin не тождественен artifact CVPR2023; F/age/history step-based |


## S060 — W1-05-S07 / локальное свидетельство (W1-05-S07)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `23.02.2023`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2302.11813v1>.

- F-связи: F062.


| S060 | Gerard Maggiolino, Adnan Ahmad, Jinkun Cao, Kris Kitani, **2302.11813v1**, 23.02.2023 | https://arxiv.org/html/2302.11813v1 — §§3.2–3.4, 4.1–4.2 | Paper: CMC/dynamic appearance/adaptive weighting; §4.1 авторы называют benchmark online без offline postprocessing |


## S061 — W1-05-S08 / локальное свидетельство (W1-05-S08)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6bb51d027b137233f5c520b6fcc4f2ae387a6ba9`, `06.05.2023`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/GerardMaggiolino/Deep-OC-SORT/tree/6bb51d027b137233f5c520b6fcc4f2ae387a6ba9>.

- F-связи: F055, F062.


| S061 | GerardMaggiolino/Deep-OC-SORT, **6bb51d027b137233f5c520b6fcc4f2ae387a6ba9**, 06.05.2023 | https://github.com/GerardMaggiolino/Deep-OC-SORT/tree/6bb51d027b137233f5c520b6fcc4f2ae387a6ba9 — README Installation/Evaluation; LICENSE.md | Read recipe, MIT. README --post/_post, external FastReID/weights; не смешивать с paper online claims |


## S062 — W1-05-S09 / локальное свидетельство (W1-05-S09)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `20.08.2025`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2408.13003v2>.

- F-связи: F055.


| S062 | Vukašin Stanojević, Branimir Todorović, **2408.13003v2**, 20.08.2025 | https://arxiv.org/html/2408.13003v2 — §§2–4, 5.2 | Paper: soft BIoU/boost/frame threshold schedule; YOLOX-X/FastReID/ECC/GBI, i9-13900K+RTX3080 авторов |


## S063 — W1-05-S10 / локальное свидетельство (W1-05-S10)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `fb5bfc3a8f067476565e753b3a73df4d757c9d03`, `05.03.2026`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vukasin-stanojevic/BoostTrack/tree/fb5bfc3a8f067476565e753b3a73df4d757c9d03>.

- F-связи: F062.


| S063 | vukasin-stanojevic/BoostTrack, **fb5bfc3a8f067476565e753b3a73df4d757c9d03**, 05.03.2026 | https://github.com/vukasin-stanojevic/BoostTrack/tree/fb5bfc3a8f067476565e753b3a73df4d757c9d03 — README run/evaluation/bug notice; LICENSE | Read recipe, MIT. `_post_gbi`, shape_similarity_v1/default vs --s_sim_corr; installation workaround, не запускался |


## S064 — W1-05-S11 / локальное свидетельство (W1-05-S11)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da`, `24.09.2025`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/kamkyu94/TrackTrack/tree/ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da>.

- F-связи: F055, F058.


| S064 | Kyujin Shim et al., TrackTrack CVPR2025, **ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da**, 24.09.2025 | https://github.com/kamkyu94/TrackTrack/tree/ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da — README; 3. Tracker/trackers/tracker.py init_tracks/update/update_without_detections; LICENSE | Official code, MIT. TAI/iterative_assignment/two pools/frame expiry. CVF paper endpoint 403: API выводы по коду |


## S065 — W1-05-S12 / локальное свидетельство (W1-05-S12)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/kamkyu94/TrackTrack/ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da/3.%20Tracker/trackers/cmc.py>.

- F-связи: F055.


| S065 | kamkyu94/TrackTrack, тот же pin | https://raw.githubusercontent.com/kamkyu94/TrackTrack/ee7f1c5fcbdcac48ed8bfab38d52c0006bf304da/3.%20Tracker/trackers/cmc.py — CMC.__init__/get_warp_matrix | Read code. Читает GMC-<vid_name>.txt; ограничение artifact для live integration, не доказательство offline метода |


## S066 — W1-05-S13 / локальное свидетельство (W1-05-S13)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `11.06.2020`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2006.06669v1>.

- F-связи: F055, F059.


| S066 | Dandan Shan, Jiaqi Geng, Michelle Shu, David Fouhey, CVPR2020, **2006.06669v1**, 11.06.2020 | https://arxiv.org/html/2006.06669v1 — §4.1 | Paper: FasterRCNN/contact/offset association, не industrial phone-use validation |


## S067 — W1-05-S14 / локальное свидетельство (W1-05-S14)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `29.09.2020`, `12c8791b303e0a0b50f753af204249e622d0281a`, `29.11.2022.`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2009.07736v2>; <https://github.com/JonathonLuiten/TrackEval/tree/12c8791b303e0a0b50f753af204249e622d0281a>.

- F-связи: F061.


| S067 | Jonathon Luiten et al., IJCV, **2009.07736v2**, 29.09.2020 | https://arxiv.org/html/2009.07736v2 — §§5–7, 9.1; https://github.com/JonathonLuiten/TrackEval/tree/12c8791b303e0a0b50f753af204249e622d0281a — README/metrics | Paper+official eval pin **12c8791b303e0a0b50f753af204249e622d0281a**, 29.11.2022. HOTA/AssA/DetA; event metrics отдельно |


## S068 — W1-05-S15 / локальное свидетельство (W1-05-S15)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `15.10.2026`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2610.22306v1>.

- F-связи: F055.


| S068 | Girish Kumar Adari, **2610.22306v1**, 15.10.2026 | https://arxiv.org/html/2610.22306v1 — abstract, §§3.6/3.8 | Fresh preprint: IMM/uncertainty/deferred commitment; long merge offline; abstract promises future code, runnable artifact не установлен |


## S069 — W1-05-S16 / локальное свидетельство (W1-05-S16)

- Provenance: [W1-05](_WORK/W1_05.md); исходная карточка `W1-05-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.ultralytics.com/modes/track>.

- F-связи: F062.


| S069 | Ultralytics live docs, unpinned | https://docs.ultralytics.com/modes/track — Supported trackers/Shared args/ReID | Vendor docs на дату доступа с расширенным набором/defaults. Lead, не воспроизводимый package recipe и не свойства upstream pins |


## S070 — fine-tuning guide (W1-06-S01)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`, `8.4.184`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/finetuning-guide.md>.

- F-связи: F064, F065, F066.


| **S070** | Ultralytics, [fine-tuning guide](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/finetuning-guide.md), SHA `de290d865035acbfa4bb24cc88960d8b52c26e45`, snapshot версии 8.4.184 | Строки 94–106 optimizer; 108–183 freeze и две стадии; 203–213 augmentation/forgetting. Официальные рекомендации, не результаты на наших данных. Пример 20+30 эпох иллюстрирует workflow, не оптимум. |


## S071 — trainer.py (W1-06-S02)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F065.


| **S071** | Ultralytics, [trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), тот же SHA | `_setup_scheduler` L268–279; `_build_train_pipeline` L301–334; freeze L381–408; warmup L520–538; frozen BN L760–766; optimizer auto L1177–1186. Исполняемая семантика, без фактического выполнения. |


## S072 — tasks.py (W1-06-S03)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/tasks.py>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/models/yolo/detect/train.py>.

- F-связи: F064, F067.


| **S072** | Ultralytics, [tasks.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/tasks.py), [detect/train.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/models/yolo/detect/train.py), тот же SHA | `BaseModel.load` L326–364, `_remap_cls_by_names` L382–450; `set_model_names_for_load` L145–149. Код умеет переносить совпавшие по имени строки классификатора, а остальные веса фильтруются по совместимым тензорам. Это initialization, не доказательство retention после обучения. |


## S073 — default.yaml (W1-06-S04)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/metrics.py>.

- F-связи: F064, F065, F066.


| **S073** | Ultralytics, [default.yaml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml), [metrics.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/metrics.py), тот же SHA | YAML L13–36 и 94–114; detection `Metric.fitness` L1011–1014. Defaults и код критерия, не готовая настройка target-задачи. |


## S074 — M custom YAML (W1-06-S05)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/objects365/dfine_hgnetv2_m_obj2custom.yml>.

- F-связи: F064, F065, F066, F069.


| **S074** | Peng et al./Peterande D-FINE, [M custom YAML](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml), [O365→custom YAML](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/objects365/dfine_hgnetv2_m_obj2custom.yml), SHA `956d1709314c2c6a4df6f34de232054578a7449f` | Оба файла прочитаны целиком, L1–60/66. Официальные конфиги, M: HGNetv2 B2, 4 decoder layers. У O365 есть `pretrained: False`, предполагается явная загрузка detector checkpoint через tuning. |


## S075 — optimizer.yml (W1-06-S06)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/optimizer.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dataloader.yml>.

- F-связи: F065, F066.


| **S075** | D-FINE, [optimizer.yml](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/optimizer.yml), [dataloader.yml](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dataloader.yml), тот же SHA | Оба целиком: optimizer L1–36, loader L1–39. MultiStepLR milestone500; LinearWarmup500 iterations; AMP/EMA, clipping0.1; вход640, batch32 total train/64 validation. Эти batch опубликованы для исходного рецепта, не одной 3090. |


## S076 — solver (W1-06-S07)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py>.

- F-связи: F064, F065, F066, F067.


| **S076** | D-FINE, [solver](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py), [det_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py), [det_engine.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py), тот же SHA | `load_tuning_state` L249–274, `_matched_state` L276–290, head mapping L292–336; solver L64–171; engine L97–119. Это важнее комментариев YAML: отдельные стадии best checkpoint/EMA restart и optimizer step каждый batch. |


## S077 — config.py (W1-06-S08)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`, `1.12.0.dev`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/config.py>.

- F-связи: F065.


| **S077** | Roboflow, [config.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/config.py), SHA `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`, development snapshot `1.12.0.dev` | ModelConfig L694–744, M/L L1052–1090; TrainConfig L1224–1401, L1520–1525. API/defaults, не валидация памяти. `grad_accum_steps=1` сопровождается явным комментарием об изменении прежнего default4. |


## S078 — training/trainer.py (W1-06-S09)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py>.

- F-связи: F065, F066.


| **S078** | Roboflow, [training/trainer.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py), тот же SHA | `_append_training_callbacks` L407–454; Trainer L970–983. `best_model_metric` определяет monitor, early stopping opt-in, accumulation пробрасывается в Lightning для detection. Не переносить на keypoint manual optimization. |


## S079 — официальные параметры обучения (W1-06-S10)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://rfdetr.roboflow.com/latest/learn/train/training-parameters/>; <https://rfdetr.roboflow.com/latest/cookbooks/custom-optimizer-scheduler/>.

- F-связи: F064, F065, F066.


| **S079** | Roboflow, [официальные параметры обучения](https://rfdetr.roboflow.com/latest/learn/train/training-parameters/), [custom optimizer cookbook](https://rfdetr.roboflow.com/latest/cookbooks/custom-optimizer-scheduler/) | Разделы Learning Rate/Resolution/early stopping; live docs без pinned release, сверены с S077–S078. API-ориентир; совет LR halve при нестабильности не экспериментальное доказательство улучшения. |


## S080 — Incremental Learning of Object Detectors without Catastrophic Forgetting (W1-06-S11)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1708.06977v1>.

- F-связи: F064, F067.


| **S080** | Konstantin Shmelkov, Cordelia Schmid, Karteek Alahari, [Incremental Learning of Object Detectors without Catastrophic Forgetting](https://arxiv.org/html/1708.06977v1), arXiv v1 2017-08-23, ICCV2017 | §§1,3.2,4 и Fig1: классическая detector-distillation, Fast R-CNN/VOC/COCO. Первичная работа показывает проблему и альтернативу replay; не turnkey loss для YOLO26/DETR. Прямой CVF PDF вернул 403, использован официальный arXiv HTML. |


## S081 — Rethinking ImageNet Pre-training (W1-06-S12)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1811.08883v1>.

- F-связи: F064.


| **S081** | Kaiming He, Ross Girshick, Piotr Dollár, [Rethinking ImageNet Pre-training](https://arxiv.org/html/1811.08883v1), arXiv v1 2018-11-21, ICCV2019 | §§3.1–3.2,5.1–5.2. Mask R-CNN, подходящая нормализация, достаточно длинное обучение: pretraining ускоряет начало, scratch может догнать. Не сравнение современных detector-pretrained YOLO26/D-FINE и не основание учить с нуля в нашем бюджете. |


## S082 — Ultralytics license (W1-06-S13)

- Provenance: [W1-06](_WORK/W1_06.md); исходная карточка `W1-06-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`, `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.ultralytics.com/license>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/README.md>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/LICENSE>.

- F-связи: F069.


| **S082** | [Ultralytics license](https://www.ultralytics.com/license), live; D-FINE [pinned README](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md); RF-DETR [pinned README](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/README.md), [LICENSE](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/LICENSE) | Ultralytics dual AGPL/Enterprise, включая fine-tuned использование по условиям поставщика; D-FINE README L137 предупреждает об Objects365 terms; RF README L306–311 различает Apache-designated weights и PML Plus. Не юридическое заключение о конкретном формате хакатона. |


## S083 — Открытый PDF CVF (W1-07-S01)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shrivastava_Training_Region-Based_Object_CVPR_2016_paper.pdf>.

- F-связи: F070.


**S083 — OHEM.** Abhinav Shrivastava, Abhinav Gupta, Ross Girshick, *Training Region-Based Object Detectors With Online Hard Example Mining*, CVPR 2016, pp. 761–769. [Открытый PDF CVF](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shrivastava_Training_Region-Based_Object_CVPR_2016_paper.pdf), §4.1, PDF p4; §6. Вид: первичная peer-reviewed статья. После forward RoI сортируются по loss, correlated overlapping RoI подавляются NMS; backward использует выбранные. Условия: Fast R-CNN style, VOC/COCO, размеченные training images. Ограничение: это не selection unlabeled clips и не готовая модификация произвольного современного detector. Открытие того же PDF на `openaccess.thecvf.com` вернуло 403; доступен официальный `cv-foundation.org` URL. Результаты в нашей среде не воспроизводились.


## S084 — 2012.01950v2 (W1-07-S02)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2012.01950v2>; <https://arxiv.org/html/2012.01950v2>.

- F-связи: F070, F073.


**S084 — Sparse instance labels.** Tiancai Wang, Tong Yang, Jiale Cao, Xiangyu Zhang, *Co-mining: Self-Supervised Learning for Sparsely Annotated Object Detection*, AAAI 2021; arXiv [2012.01950v2](https://arxiv.org/abs/2012.01950v2), версия 2021-10-14; [полный HTML](https://arxiv.org/html/2012.01950v2), Introduction, Related Work/SAOD, Co-mining framework, Table 3. Вид: первичная статья. Пропущенные instances дают ошибочную supervision; Siamese branches на исходном/аугментированном изображении генерируют друг другу pseudo-labels. Условия: искусственно sparse COCO, RetinaNet/FCOS. Ограничение: benchmark не устанавливает надёжность pseudo-labels phone/tool/mannequin в новом цехе; shared teacher mistakes сохраняются. Рецепт здесь не внедрён.


## S085 — arXiv 2211.13993v3 (W1-07-S03)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2211.13993v3>; <https://arxiv.org/html/2211.13993v3>.

- F-связи: F070.


**S085 — Label QA.** Krystian Chachuła, Jakub Łyskawa, Bartłomiej Olber, Piotr Frątczak, Adam Popowicz, Krystian Radlak, *Combating noisy labels in object detection datasets*, [arXiv 2211.13993v3](https://arxiv.org/abs/2211.13993v3), 2023-12-11, первоначально 2022-11-25; [полный HTML](https://arxiv.org/html/2211.13993v3), §III algorithm, §IV experiments и abstract. Вид: первичная исследовательская статья/preprint. CLOD связывает predictions/boxes и оценивает четыре вида label problems; результат — список подозрений и предложений исправления. Ограничение: заметные авторские gains относятся к их датасетам и искусственному возмущению labels, не прогноз нашей accuracy; human review предпочтительнее автоматической замены. В статье заявлена подача в ICDE 2024, статус публикации сверх этого здесь не подтверждён.


## S086 — arXiv 1809.09875v1 (W1-07-S04)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/1809.09875v1>.

- F-связи: F070.


**S086 — Detection active learning.** Clemens-Alexander Brust, Christoph Käding, Joachim Denzler, *Active Learning for Deep Object Detection*, [arXiv 1809.09875v1](https://arxiv.org/abs/1809.09875v1), 2018-09-26, abstract и full-paper link. Вид: первичный preprint; открыта arXiv landing page, подробный алгоритм PDF в этой ветке не разобран. Подтверждены постановка uncertainty-based selection, учёт class imbalance и evaluation на VOC2012. Ограничение: источник поддерживает направление, но не наш конкретный mixture score, эффективность video diversity или численный бюджет.


## S087 — arXiv 2008.08115v2 (W1-07-S05)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2008.08115v2>; <https://arxiv.org/html/2008.08115v2>.

- F-связи: F071.


**S087 — Error taxonomy.** Daniel Bolya, Sean Foley, James Hays, Judy Hoffman, *TIDE: A General Toolbox for Identifying Object Detection Errors*, [arXiv 2008.08115v2](https://arxiv.org/abs/2008.08115v2), 2020-08-31, [полный HTML](https://arxiv.org/html/2008.08115v2), §2.2/2.3, §3.4 и appendix. Вид: первичная статья. Шесть категорий detection error и изолированные oracle corrections позволяют различать причины потери AP. Условия: predictions + корректный GT; объектная детекция/segmentation. Ограничение: GT может быть неверен; вклад oracle не обещает retraining gain; temporal alert semantics вне инструмента. Код не устанавливался, commit не выбирался.


## S088 — официальный LVIS PDF (W1-07-S06)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.lvisdataset.org/assets/challenge_reports/2020/CenterNet2.pdf>.

- F-связи: F073.


**S088 — Category-level partial annotation.** Xingyi Zhou, Vladlen Koltun, Philipp Krähenbühl, *Technical Report: CenterNet2*, Joint COCO/LVIS workshop ECCV 2020, [официальный LVIS PDF](https://www.lvisdataset.org/assets/challenge_reports/2020/CenterNet2.pdf), PDF p2 §3 и p4 Table 2. Вид: первичный challenge technical report, не независимое воспроизведение. Federated Loss использует все positive classes и выборку negative classes, остальные игнорирует; авторы объясняют конфликт между overly pessimistic negatives и слабым background learning. Условия: LVIS federated annotations, CenterNet2/CascadeRCNN. Ограничение: не переносить число sampled classes/табличные AP на несколько safety-классов; не универсальное решение instance-sparse labels. Документ привязан к workshop 2020, точная дата revision/commit не указана.


## S089 — Quality control (W1-07-S07)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.80.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.cvat.ai/docs/qa-analytics/quality-control/>.

- F-связи: F074.


**S089 — QA workflow.** CVAT.ai maintainers, [Quality control](https://docs.cvat.ai/docs/qa-analytics/quality-control/), live documentation, видимая ветка `develop`, locator `How to enable quality control`, `How to enable immediate job feedback`, `How to check task quality metrics`. Вид: первичная документация инструмента. GT jobs, review и quality reports поддерживают QA; immediate feedback и analytics на странице отмечены Online/Enterprise. Ограничение: не обещать все функции в Community/имеющейся версии; стоимость/доступ/установка не проверялись. Версия `v2.80.0` присутствовала в переключателе, но отсутствие pinned working installation не позволяет считать это воспроизводимым рецептом.


## S090 — Consensus-based annotation (W1-07-S08)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.cvat.ai/docs/qa-analytics/consensus/>.

- F-связи: F074.


**S090 — Independent annotation.** CVAT.ai maintainers, [Consensus-based annotation](https://docs.cvat.ai/docs/qa-analytics/consensus/), live documentation/develop, `Basics` и верхние Notes. Вид: первичная документация. Replica jobs и merge нескольких независимых аннотаций; 2D, кроме cuboids; tasks/jobs, не projects. Ограничение: reviewers могут разделять общий bias; majority не устанавливает невидимую причину и требует дополнительных затрат. Наш ручной adjudication protocol не требует именно этой реализации.


## S091 — How to identify duplicate video (W1-07-S09)

- Provenance: [W1-07](_WORK/W1_07.md); исходная карточка `W1-07-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://dataeval.readthedocs.io/en/latest-known-good/notebooks/h2_deduplicate_video.html>.

- F-связи: F076.


**S091 — Video duplicate integrity.** DataEval maintainers, [How to identify duplicate video](https://dataeval.readthedocs.io/en/latest-known-good/notebooks/h2_deduplicate_video.html), live `latest-known-good` documentation, разделы `Detecting train-test leakage`, `Acting on the results`, `Triaging the dataset`. Вид: первичный tutorial с демонстрационными данными. Показывает shared segments, re-sampling/alignment и grouping by sequence; одних точных hashes недостаточно для изменённых copies. Ограничение: tutorial не доказывает отсутствие leakage в нашем pool; API/threshold не pinned и не исполнялись. Similarity thresholds нужно подбирать на development и проверять вручную, не оптимизировать по final metric.


## S092 — arXiv 1907.07484v2 (W1-08-S01)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1907.07484v2>.

- F-связи: F080, F081, F082, F083, F084.


| **S092** — Michaelis, Mitzkus, Geirhos, Rusak, Bringmann, Ecker, Bethge, Brendel, *Benchmarking Robustness in Object Detection*, [arXiv 1907.07484v2](https://arxiv.org/html/1907.07484v2), v2 **2020-03-31**; первая подача 2019-07-17 | §§3.3–3.5, Tables 2/4/5. Faster R-CNN, COCO val2017: standard clean/corrupted AP **36.3/18.2**, stylized-only **21.5/14.1**, clean+stylized **34.6/20.4**. Следовательно, лучшее relative retention может скрывать худшее абсолютное качество. BDD day→night clean/combined night AP **21.5/22.5**; авторы отдельно предупреждают о мягких weather labels. | Detection, но старое семейство и дорожные данные; стилизация не равна произвольному сильному HSV. Synthetic corruption и реальное ночное видео рассмотрены раздельно. Это основание проверить trade-off, не перенести проценты на цех. |


## S093 — arXiv 2012.07177v2 (W1-08-S02)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2012.07177v2>.

- F-связи: F080, F082, F083.


| **S093** — Ghiasi, Cui, Srinivas, Qian, Lin, Cubuk, Le, Zoph, *Simple Copy-Paste*, [arXiv 2012.07177v2](https://arxiv.org/html/2012.07177v2), **2021-06-23**, CVPR 2021 | §3, §4.1, Appendix A/Table 10. Mask R-CNN EfficientNet-B7 FPN 640: baseline box/mask AP **48.5/42.7**, random-subset Copy-Paste **50.0/43.7**; без blending те же **50.0/43.7**; вставка только одного объекта **49.1/43.1**. Метод обновляет masks/boxes при перекрытии. В §4.1 режимы обучают до convergence, сильный LSJ+Copy-Paste может требовать более длинного schedule. | Хорошая causal ablation конкретного метода; COCO instance segmentation, masks и конкретный training setup. Не доказательство box-only реализации или одинакового compute budget; прирост полного recipe нельзя приписать одной операции. |


## S094 — arXiv 1807.07428v1 (W1-08-S03)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1807.07428v1>.

- F-связи: F080, F083.


| **S094** — Dvornik, Mairal, Schmid, *Modeling Visual Context is Key to Augmenting Object Detection Datasets*, [arXiv 1807.07428v1](https://arxiv.org/html/1807.07428v1), **2018-07-19**, ECCV 2018 | §§4.1–4.3, Table 1, §4.5. BlitzNet/ResNet50, 300², 1,464 VOC12train-seg→VOC07-test; отдельная модель на категорию, одинаковые 6k iterations. Random-DA вставляет до двух объектов в negative background; авторы находят среднюю деградацию и зависимость от класса; context placement лучше random и baseline в среднем. | Прямой контрпример тезису «случайный фон всегда помогает». Небольшой single-category режим отличается от COCO multi-instance S093; противоречие нельзя разрешить выбором понравившейся статьи. |


## S095 — arXiv 1902.07296v1 (W1-08-S04)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1902.07296v1>.

- F-связи: F080, F081, F082.


| **S095** — Kisantal, Wojna, Murawski, Naruniec, Cho, *Augmentation for small object detection*, [arXiv 1902.07296v1](https://arxiv.org/html/1902.07296v1), **2019-02-19** | §§4–6, Tables 3/4. Mask R-CNN/COCO: baseline small/large detection AP **0.167/0.393**; 3× oversampling **0.177/0.382**; 4× хуже 3×. Замена оригиналов pasted-изображениями снижает small AP до **0.161**, original+aug даёт **0.179**. §6.2: на augmented validation впечатление лучше, чем на оригинальном; авторы связывают это с артефактами вставки. Используют non-occluded cutouts и исключают overlap. | Самый прямой negative finding для small objects. Опубликованное объяснение механизма связано с anchors/RPN; не переносить его буквально на anchor-free detector. Десятичные AP здесь шкалы 0–1. |


## S096 — arXiv 1703.06907v1 (W1-08-S05)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1703.06907v1>.

- F-связи: F082.


| **S096** — Tobin, Fong, Ray, Schneider, Zaremba, Abbeel, *Domain Randomization*, [arXiv 1703.06907v1](https://arxiv.org/html/1703.06907v1), **2017-03-20** | §III-A, §IV-C/Table II. Рандомизируют textures, освещение, distractors, camera pose и другие параметры рендера. При 20k synthetic samples real localization error с distractors: full **1.8±1.7 cm**, без train distractors **7.2±4.5 cm**; без camera randomization **2.4±2.3 cm**. Добавление noise имеет небольшой эффект в этом опыте. Fig.5 показывает зависимость от texture diversity. | Узкая tabletop localization/robotics, известные геометрические формы, не PPE/video-events и не заводской detection AP. Успех процедурного рендера не является доказательством качества случайных text-to-image картинок. |


## S097 — augment.py (W1-08-S06)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`, `8.4.184`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/data/augment.py>.

- F-связи: F081.


| **S097** — Ultralytics, [augment.py](https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/data/augment.py), commit **de290d865035acbfa4bb24cc88960d8b52c26e45**, версия **8.4.184** по W1-02; версия кода независимо открыта | `RandomPerspective.apply_instances`, `box_candidates` (около L1133–1140, L1275–1313), `CopyPaste.__call__` (L1785–1788). Отсев boxes по width/height >2, aspect <100 и area ratio: 0.10 для boxes / 0.01 при segments. CopyPaste возвращает исходное при отсутствии segments. | Исполняемая семантика закреплённого кода, не оценка качества. Default filtering может удалить small/truncated target; box-only dataset не получает автоматически paper Copy-Paste. Header AGPL-3.0; веса не использовались и их лицензия здесь не проверялась. |


## S098 — Transforms 0.24 (W1-08-S07)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/vision/0.24/transforms.html>; <https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.v2.UniformTemporalSubsample.html>; <https://pytorch.org/blog/extending-torchvisions-transforms-to-object-detection-segmentation-and-video-tasks/>.

- F-связи: F081.


| **S098** — PyTorch/TorchVision maintainers, [Transforms 0.24](https://docs.pytorch.org/vision/0.24/transforms.html), [UniformTemporalSubsample 0.24](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.v2.UniformTemporalSubsample.html); официальные versioned API docs, дата публикации страницы не указана | Поддержка Video, boxes, masks; random transform сэмплирует параметры при вызове, functional API позволяет явно повторить параметры. UniformTemporalSubsample выбирает индексы оси T, а при запросе больше кадров — nearest-neighbor sampling. Открыт также [официальный блог](https://pytorch.org/blog/extending-torchvisions-transforms-to-object-detection-segmentation-and-video-tasks/) о согласованных случайных transforms всех входов. | Документация API, не доказательство сохранения temporal labels; временные метки/ROI не преобразуются магически. Versioned docs не фиксируют wheel, runtime или все зависимости; для реализации нужен environment lock и тест на своём формате клипов. |


## S099 — arXiv 2007.01434v1 (W1-08-S08)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2007.01434v1>.

- F-связи: F080.


| **S099** — Gulrajani, Lopez-Paz, *In Search of Lost Domain Generalization*, [arXiv 2007.01434v1](https://arxiv.org/html/2007.01434v1), **2020-07-02** | §§2–3: различие DG без train-доступа к test domain и adaptation с unlabeled target; выбор гиперпараметров — часть метода, test-domain oracle следует обозначать отдельно. Прочитан первичный текст, а не только абстракт. | Методологическое evidence, в основном classification benchmarks; отсюда не следует, что ERM всегда выигрывает у detector DG. В этой ячейке не воспроизводится DomainBed. |


## S100 — SparseDet author project (W1-08-S09)

- Provenance: [W1-08](_WORK/W1_08.md); исходная карточка `W1-08-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.cs.umd.edu/~sakshams/SparseDet/>.

- F-связи: F081.


| **S100** — Suri, Rambhatla, Chellappa, Shrivastava, [SparseDet author project](https://www.cs.umd.edu/~sakshams/SparseDet/), **ICCV 2023**, live page, дата версии не указана | Introduction/Abstract/Approach Overview: missing foreground labels превращаются в отрицательные обучающие сигналы; noisy pseudo-labels при высокой sparsity также проблемны. Авторы используют отдельный mining/supervision механизм. | Авторский первичный project description, не кодовый рецепт; никакой SparseDet checkpoint не выбран. Само наличие augmentation не исправляет partial annotations. |


## S101 — Страница публикации (W1-09-S01)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://proceedings.mlr.press/v70/guo17a.html>; <https://proceedings.mlr.press/v70/guo17a/guo17a.pdf>.

- F-связи: F086, F087.


- **S101.** Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger, *On Calibration of Modern Neural Networks*, ICML/PMLR 70, 2017. [Страница публикации](https://proceedings.mlr.press/v70/guo17a.html), [PDF](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf). Локаторы: §4.2, Eq. (9), PDF p.6; §5, Table 1/Fig.4. Тип: paper, опубликованный experiment classification calibration. Условия — их vision/NLP classifiers и splits. Ограничения: не detector events и не камеры LinQ; scalar softmax scaling сохраняет argmax, что не означает все виды rank invariance. В этой ветке заимствованы принцип и формула, не значения temperature.


## S102 — arXiv v1, 28.04.2020 (W1-09-S02)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28.04.2020`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/2004.13546v1>; <https://arxiv.org/pdf/2004.13546v1>.

- F-связи: F086.


- **S102.** Fabian Küppers, Jan Kronenberger, Amirhossein Shantia, Anselm Haselhoff, *Multivariate Confidence Calibration for Object Detection*, CVPR Workshops 2020; [arXiv v1, 28.04.2020](https://arxiv.org/abs/2004.13546v1), [PDF](https://arxiv.org/pdf/2004.13546v1). Локаторы: §3.1–3.2 — TP/localization target; §5.1–5.2, Table 1, Fig.4 — confidence/box-sensitive comparison и binning. Тип: paper, авторские detector calibration experiments. Условия — исследованные detector/COCO outputs и IoU; многомерные bins требуют данных. D-ECE не event metric; улучшение не доказывает timely recall. CVF PDF открылся с 403, прочитан arXiv PDF.


## S103 — arXiv v2, 08.08.2017 (W1-09-S03)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `08.08.2017`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/1704.04503v2>; <https://arxiv.org/pdf/1704.04503v2>.

- F-связи: F086.


- **S103.** Navaneeth Bodla, Bharat Singh, Rama Chellappa, Larry S. Davis, *Soft-NMS — Improving Object Detection With One Line of Code*, ICCV2017; [arXiv v2, 08.08.2017](https://arxiv.org/abs/1704.04503v2), [PDF](https://arxiv.org/pdf/1704.04503v2). Локаторы: §4 rescore linear/Gaussian; §5–6 results/sensitivity. Тип: алгоритм и авторские VOC/COCO эксперименты. Условия — конкретные detector outputs и cutoffs. Ограничения: AP не alarm precision, CPU cost не LinQ benchmark; параметры всё равно существуют. CVF PDF 403; прочитан arXiv.


## S104 — arXiv v3, 06.02.2021 (W1-09-S04)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `06.02.2021`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/abs/1910.13302v3>; <https://arxiv.org/pdf/1910.13302v3>.

- F-связи: F085, F086.


- **S104.** Roman Solovyev, Weimin Wang, Tatiana Gabruseva, *Weighted boxes fusion: Ensembling boxes from different object detection models*, [arXiv v3, 06.02.2021](https://arxiv.org/abs/1910.13302v3), [PDF](https://arxiv.org/pdf/1910.13302v3), Image and Vision Computing 2021, 104117. Локаторы: §3 Eqs.(1–5), §6 Table 5, §7 одиночный RetinaNet и negative result; §5 Eq.(7) ошибочная запись precision. Тип: paper, авторские Open Images/COCO эксперименты. Их измерения и параметры не наш recipe/benchmark. Попытка HTML v5 дала 404; реальная последняя указанная версия v3.


## S105 — *Tuning the decision threshold for class prediction*, version 1.5.2 (W1-09-S05)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1.5.2`, `3.3.1`, `3.3.1.2`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://scikit-learn.org/1.5/modules/classification_threshold.html>.

- F-связи: F086.


- **S105.** scikit-learn developers, [*Tuning the decision threshold for class prediction*, version 1.5.2](https://scikit-learn.org/1.5/modules/classification_threshold.html). Локаторы: §3.3.1, §3.3.1.2 и warning `cv="prefit"`. Тип: versioned official docs; `TunedThresholdClassifierCV` добавлен в 1.5. Подтверждает раздельные scores/decisions и риск same-data fit/tune. Ограничение: binary sample classifier, не готовый event evaluator. Найденная dev1.10/stable1.9 страница намеренно не используется как pinned implementation recipe.


## S106 — Официальная статья (W1-09-S06)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://papers.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html>; <https://papers.nips.cc/paper_files/paper/2019/file/8558cb408c1d76621371888657d2eb1d-Paper.pdf>.

- F-связи: F086, F091.


- **S106.** Yaniv Ovadia et al., *Can You Trust Your Model’s Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift*, NeurIPS32, 2019. [Официальная статья](https://papers.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html), [PDF](https://papers.nips.cc/paper_files/paper/2019/file/8558cb408c1d76621371888657d2eb1d-Paper.pdf). Локаторы: §4 image experiments/Figs.2–3; §5 recommendations. Тип: эксперимент classification uncertainty under shift. Ограничения: не исследование конкретного per-camera industrial threshold; не основание обещать пользу ансамбля при LinQ budget.


## S107 — PDF/DOI (W1-09-S07)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://doi.org/10.6028/NIST.TN.2119>.

- F-связи: F090.


- **S107.** Zhan-Qian John Lu, NIST Technical Note 2119, *Estimating Instrument Performance: with Confidence Intervals and Confidence Bounds*, September2020. [PDF/DOI](https://doi.org/10.6028/NIST.TN.2119). Локаторы: §4.1, печатные p.14–16 / PDF pp.23–25, Clopper–Pearson inversion/Example8. Тип: первичная техническая статистическая рекомендация. Условия — binomial trials. Числа 10/10,20/20,59/59 в отчёте — наш расчёт частного случая, не наблюдаемые данные; независимость видеоэпизодов отдельно не доказана.


## S108 — §8.4.5.1 Constant repair rate (HPP/exponential) model (W1-09-S08)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `8.4.5.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm>.

- F-связи: F090.


- **S108.** NIST/SEMATECH e-Handbook, [§8.4.5.1 Constant repair rate (HPP/exponential) model](https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm), live, дата версии не указана. Локатор: `Confidence interval equation and "zero fails" case`. Тип: official model-based statistical reference. Используем модель нулевого счёта для планирования экспозиции; предположение constant rate не подтверждено для камер. Это не pinned recipe библиотеки.


## S109 — Исходник (W1-09-S09)

- Provenance: [W1-09](_WORK/W1_09.md); исходная карточка `W1-09-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `796d4b1b6125ebef795cf14363dae00da78d5a1c`, `23.10.2026.`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/ensemble_boxes/ensemble_boxes_wbf.py>; <https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/LICENSE>.

- F-связи: F085, F086, F087, F088, F089, F090, F091, F092, F093.


- **S109.** ZFTurbo/Roman Solovyev, Weighted-Boxes-Fusion, pinned commit `796d4b1b6125ebef795cf14363dae00da78d5a1c`, commit time `2026-10-09T06:50:48Z`, получен read-only GitHub API 23.10.2026. [Исходник](https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/ensemble_boxes/ensemble_boxes_wbf.py), [MIT license](https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/LICENSE). Локаторы: `prefilter_boxes`, `get_weighted_box`, `find_matching_box_fast`, `weighted_boxes_fusion`, lines143–225. Тип: прочитанный код; не установлен/не запущен. Контракт: normalized xyxy `[0,1]`, одинаковые labels, `weights`, `iou_thr`, `skip_box_thr`, `conf_type`, `allows_overflow`; defaults не признаны нашими оптимальными настройками. Output confidence зависит от вида fusion и наличия моделей; не является автоматически calibrated event probability. MIT относится к этому коду, не к произвольным detector weights.


## S110 — Weighted boxes fusion, arXiv:1910.13302v3 (W1-10-S01)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/pdf/1910.13302v3>.

- F-связи: F094, F095.


| **S110** | Roman Solovyev, Weimin Wang, Tatiana Gabruseva, [Weighted boxes fusion, arXiv:1910.13302v3](https://arxiv.org/pdf/1910.13302v3), revision **2021-02-06**, v1 2019-10-29; §3 pp2–3 algorithm; §6.1 p4 constituent NMS; §7 p7 single-model comparison | Опубликованный метод и benchmark. Single-model counterexample относится к RetinaNet/Open Images, не всему detection. В paper §5 формула, подписанная Precision, содержит FN в знаменателе: **не копировать её как definition precision**; использовать стандартный GT evaluator. Методологическая опечатка не отменяет опубликованного отрицательного результата, но не переносить самодельный evaluator из текста |


## S111 — WBF code (W1-10-S02)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `796d4b1b6125ebef795cf14363dae00da78d5a1c`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/ensemble_boxes/ensemble_boxes_wbf.py>; <https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/LICENSE>.

- F-связи: F095.


| **S111** | ZFTurbo/Roman Solovyev, [WBF code](https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/ensemble_boxes/ensemble_boxes_wbf.py), SHA **796d4b1b6125ebef795cf14363dae00da78d5a1c**, `prefilter_boxes`, `get_weighted_box`, `find_matching_box_fast`, `weighted_boxes_fusion` lines ~8–231; [LICENSE](https://github.com/ZFTurbo/Weighted-Boxes-Fusion/blob/796d4b1b6125ebef795cf14363dae00da78d5a1c/LICENSE) | Прочитанный код, **MIT**, copyright 2020. Реальные API/confidence режимы. Это postprocessing, собственных neural weights нет; speed на LinQ не измерена |


## S112 — NoScope (W1-10-S03)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://people.eecs.berkeley.edu/~matei/papers/2017/vldb_noscope.pdf>.

- F-связи: F095, F096.


| **S112** | Daniel Kang, John Emmons, Firas Abuzaid, Peter Bailis, Matei Zaharia, [NoScope](https://people.eecs.berkeley.edu/~matei/papers/2017/vldb_noscope.pdf), PVLDB **2017**, Vol10(11), pp1586–1597; §3–6 cascade/optimizer, §4 definition reference errors, §8 pp1591–1592 limitations | Опубликованная cascade-система. Binary presence tasks, fixed-angle video, согласие с teacher, assumption distribution stability. Их speedup не прогноз для LinQ и safety events. Разрешение статьи не равно лицензии их code/weights; готовый code recipe не выбран |


## S113 — Distilling the Knowledge in a Neural Network (W1-10-S04)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.cs.toronto.edu/~hinton/absps/distillation.pdf>.

- F-связи: F094, F095.


| **S113** | Geoffrey Hinton, Oriol Vinyals, Jeff Dean, [Distilling the Knowledge in a Neural Network](https://www.cs.toronto.edu/~hinton/absps/distillation.pdf), **arXiv:1503.02531v1, 2015-03-09**; §2 pp2–3 temperature/loss; §7–8 pp7–9 specialists/discussion | Первичная основа soft-target KD; MNIST/speech/specialists, не наш detector benchmark. Specialist→single distillation авторы в работе ещё не показали. Конкретные веса не предлагаются |


## S114 — Fine-grained Feature Imitation (W1-10-S05)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/pdf/1906.03609v1>.

- F-связи: F094, F095.


| **S114** | Tao Wang, Li Yuan, Xiaopeng Zhang, Jiashi Feng, [Fine-grained Feature Imitation](https://arxiv.org/pdf/1906.03609v1), **2019-06-09**, CVPR2019 pp4933–4942; §1 limitation of full imitation, §3 location masks, §4.2 KD/hint comparison | Detector-specific KD и отрицательный full-feature result на рассмотренных anchor/Faster R-CNN экспериментах; не универсальный recipe для современных query detectors. Код/weights не включены в deployment shortlist, их лицензия не проверена |


## S115 — TSM (W1-10-S06)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/pdf/1811.08383v3>; <https://github.com/mit-han-lab/temporal-shift-module/tree/1f6a834b02120441d99fa706b7a13ccc5293c6fa>.

- F-связи: F095.


| **S115** | Ji Lin, Chuang Gan, Song Han, [TSM](https://arxiv.org/pdf/1811.08383v3), **2019-08-22**, ICCV2019; Fig.1, §3.2, §4.2/Fig.4 | Метод, causal/offline различие и overhead памяти; авторские hardware measurements не LinQ. [Код](https://github.com/mit-han-lab/temporal-shift-module/tree/1f6a834b02120441d99fa706b7a13ccc5293c6fa), SHA **1f6a834b02120441d99fa706b7a13ccc5293c6fa**, GitHub license metadata MIT; конкретный checkpoint/weight license не выбран и не проверен, поэтому это architecture lead, не готовая weight recipe |


## S116 — X3D (W1-10-S07)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `287ec0076846560f44a9327e931a5a2360240533`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/pdf/2004.04730v1>; <https://github.com/facebookresearch/SlowFast/tree/287ec0076846560f44a9327e931a5a2360240533>; <https://github.com/facebookresearch/SlowFast/blob/287ec0076846560f44a9327e931a5a2360240533/LICENSE>.

- F-связи: F095.


| **S116** | Christoph Feichtenhofer, [X3D](https://arxiv.org/pdf/2004.04730v1), **2020-04-09**, CVPR2020; §3 axes/expansion, §4 tables accuracy/complexity | Peer-reviewed architecture lead, action benchmarks. [SlowFast code](https://github.com/facebookresearch/SlowFast/tree/287ec0076846560f44a9327e931a5a2360240533), SHA **287ec0076846560f44a9327e931a5a2360240533**, [LICENSE Apache-2.0](https://github.com/facebookresearch/SlowFast/blob/287ec0076846560f44a9327e931a5a2360240533/LICENSE). Прочитаны LICENSE и MODEL_ZOO; это не подтверждает автоматически лицензию любого внешнего checkpoint или поддержку TPU. Weights не выбраны |


## S117 — Cascade R-CNN (W1-10-S08)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/pdf/1712.00726v1>.

- F-связи: F095.


| **S117** | Zhaowei Cai, Nuno Vasconcelos, [Cascade R-CNN](https://arxiv.org/pdf/1712.00726v1), **arXiv v1 2017-12-03**, работа CVPR2018 pp6154–6162; abstract/§1/§3 | Последовательное refinement и proposal-quality mismatch. Это другой каскад внутри detector; не доказательство эффективности независимого crop verifier. Не рекомендован как дополнительный production graph; code/weights не предлагаются |


## S118 — CASE_NOTES — root visual observations (W1-10-S09)

- Provenance: [W1-10](_WORK/W1_10.md); исходная карточка `W1-10-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: **unknown / локальная provenance, см. карточку**.

- F-связи: F094, F095, F096, F097, F098, F099.


| **S118** | `_WORK/CASE_NOTES.md`, root visual observations, 2026-10-23, p5/7/13 официального raster case; hash оригинала в этом файле | Переданная первичная визуальная проверка root, не независимый повторный просмотр W1-10. Обязательства latency/LinQ/дедупликации; CPU+TPU exact config остаётся командным сообщением |


## S119 — полный HTML (W1-11-S01)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1810.05934v5>.

- F-связи: F100, F105.


| **S119** | Liam Li et al., *A System for Massively Parallel Hyperparameter Tuning*, arXiv v5 **2020-03-16**, MLSys2020; [полный HTML](https://arxiv.org/html/1810.05934v5) | §§3.1–3.3, Algorithms1–2, §5.1/default settings и §5.4. Первичная статья ASHA: resource r/R, rungs, async promotions, неправильные ранние promotions и checkpoint state. Изучены большие search/parallel settings; не эксперимент на YOLO26/D-FINE и не гарантия на двух 3090. |


## S120 — полный PDF (W1-11-S02)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://jmlr.org/papers/volume18/16-558/16-558.pdf>.

- F-связи: F105.


| **S120** | Lisha Li et al., *Hyperband*, JMLR18(185), **2018**, [полный PDF](https://jmlr.org/papers/volume18/16-558/16-558.pdf) | §3 и Algorithm1; PDF pp.5–10, §3.6. Первичный метод адаптивного распределения заранее определённого ресурса. Несколько brackets страхуют выбор initial resource; эффект опубликован на своих задачах, не универсальная экономия GPU-часов. |


## S121 — trainer.py (W1-11-S03)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F105.


| **S121** | Ultralytics, SHA **de290d865035acbfa4bb24cc88960d8b52c26e45**, snapshot8.4.184; [trainer.py](https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py) | Web raw L246–252 scheduler; L295–310 iterations/optimizer; L454–475 late mosaic; L629–634 time mode; L1093–1102 optimizer auto. Прочитанный исполняемый код, без выполнения. Учитывать именно этот SHA: номера строк соседних отчётов могут отличаться от web-нумерации. |


## S122 — M custom YAML (W1-11-S04)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/Peterande/D-FINE/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml>; <https://raw.githubusercontent.com/Peterande/D-FINE/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py>.

- F-связи: F105.


| **S122** | D-FINE authors/Peterande, SHA **956d1709314c2c6a4df6f34de232054578a7449f**; [M custom YAML](https://raw.githubusercontent.com/Peterande/D-FINE/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml), [det_solver.py](https://raw.githubusercontent.com/Peterande/D-FINE/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py) | YAML L46–56:132 epochs, policy epoch 120, stop_epoch 120. Solver L59–68: на границе возврат best_stg1 и refresh EMA. Первичная recipe/логика, не оптимальное окно для custom PPE. |


## S123 — hyperparameter-tuning.md (W1-11-S05)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/hyperparameter-tuning.md>.

- F-связи: F100.


| **S123** | Ultralytics, тот же SHA; [hyperparameter-tuning.md](https://raw.githubusercontent.com/ultralytics/ultralytics/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/hyperparameter-tuning.md) | Разделы *Iterations and Population Size*, *Custom Search Space Example*, warning о short/small-scale tuning. Официальный guide: iterations — число отдельных runs; short tuning может предпочесть быструю сходимость. Не эмпирическая калибровка безопасного grace_period. |


## S124 — полный HTML (W1-11-S06)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/1811.08883v1>.

- F-связи: F105.


| **S124** | Kaiming He, Ross Girshick, Piotr Dollár, *Rethinking ImageNet Pre-training*, arXiv v1 **2018-11-21**, [полный HTML](https://arxiv.org/html/1811.08883v1) | §§3.2,5.1, Fig1. Detector-specific контрпример переносу ранней сходимости на конечное качество: Mask R-CNN/COCO и разные initialization/schedules. Не доказательство, что конкретный современный transformer обгонит YOLO, и не рекомендация обучать с нуля. |


## S125 — release (W1-11-S07)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v5.0.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/optuna/optuna/releases/tag/v5.0.0>; <https://optuna.readthedocs.io/en/v5.0.0/reference/samplers/generated/optuna.samplers.TPESampler.html>.

- F-связи: F100, F106.


| **S125** | Optuna contributors, **v5.0.0**, [release](https://github.com/optuna/optuna/releases/tag/v5.0.0), [TPESampler versioned API](https://optuna.readthedocs.io/en/v5.0.0/reference/samplers/generated/optuna.samplers.TPESampler.html) | Signature; `n_startup_trials`, `multivariate`, `constant_liar`, `constraints_func` и release *Major Enhancements/Core APIs*. В5.0 изменились defaults; `constraints_func` deprecated. Это API, не утверждение превосходства TPE для малого detector portfolio. |


## S126 — Trial API (W1-11-S08)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v5.0.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://optuna.readthedocs.io/en/v5.0.0/reference/generated/optuna.trial.Trial.html>; <https://raw.githubusercontent.com/optuna/optuna/v5.0.0/optuna/trial/_trial.py>; <https://optuna.readthedocs.io/en/v5.0.0/reference/pruners.html>.

- F-связи: F106.


| **S126** | Optuna **v5.0.0**, [Trial API](https://optuna.readthedocs.io/en/v5.0.0/reference/generated/optuna.trial.Trial.html), [pinned source](https://raw.githubusercontent.com/optuna/optuna/v5.0.0/optuna/trial/_trial.py), [pruners](https://optuna.readthedocs.io/en/v5.0.0/reference/pruners.html) | `report`, `should_prune`, `set_constraint`, `constraints`. Ограничение single-objective pruning, повторный report того же step сохраняет первое значение; constraints feasible при всех<=0. Проверены docs+код, никакой Optuna study здесь не запускался. |


## S127 — HyperbandPruner code (W1-11-S09)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v5.0.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/optuna/optuna/v5.0.0/optuna/pruners/_hyperband.py>; <https://optuna.readthedocs.io/en/v5.0.0/reference/generated/optuna.create_study.html>.

- F-связи: F106.


| **S127** | Optuna **v5.0.0**, [HyperbandPruner code](https://raw.githubusercontent.com/optuna/optuna/v5.0.0/optuna/pruners/_hyperband.py), [create_study](https://optuna.readthedocs.io/en/v5.0.0/reference/generated/optuna.create_study.html) | Hyperband L35–58: startup trials отдельно по bracket, формула количества brackets. create_study signature, persistence storage и directions. Предупреждение implementation-specific; не вывод о минимально необходимом числе trials для любой задачи. |


## S128 — async_hyperband.py (W1-11-S10)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.59.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/ray-project/ray/ray-2.59.0/python/ray/tune/schedulers/async_hyperband.py>; <https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.ASHAScheduler.html>.

- F-связи: F105.


| **S128** | Ray contributors, release tag **ray-2.59.0**, [async_hyperband.py](https://raw.githubusercontent.com/ray-project/ray/ray-2.59.0/python/ray/tune/schedulers/async_hyperband.py); [live API, заголовок2.59.0](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.ASHAScheduler.html) | L26–65 signature/time_attr; L137–149 missing-key/max_t; L215–251 rungs/cutoff; L264 alias. Реальная Ray реализация early termination, не буквально promotion loop статьи. Tag фиксирует source recipe лучше `/latest`. |


## S129 — trainable_fn_utils.py (W1-11-S11)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.59.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://raw.githubusercontent.com/ray-project/ray/ray-2.59.0/python/ray/tune/trainable/trainable_fn_utils.py>; <https://docs.ray.io/en/latest/tune/api/doc/ray.tune.report.html>.

- F-связи: F100, F105.


| **S129** | Ray **ray-2.59.0**, [trainable_fn_utils.py](https://raw.githubusercontent.com/ray-project/ray/ray-2.59.0/python/ray/tune/trainable/trainable_fn_utils.py); [report API](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.report.html) | L18–30: `report(metrics: Dict, *, checkpoint=None)`; каждый report увеличивает training_iteration; единица не обязательно epoch. Первичная signature/докстрока. Versioned docs URL `releases-2.59.0` не открылся; latest сначала открыт, повторный запрос429; семантика дополнительно проверена pinned raw. |


## S130 — полный PDF (W1-11-S12)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf>.

- F-связи: F107.


| **S130** | Gavin Cawley, Nicola Talbot, *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, JMLR11, **2010**, [полный PDF](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf) | Введение pp.2079–2081 и разделы о model selection/performance evaluation. Первичная статистическая аргументация: finite selection criterion сам переобучается; сравнивать весь selection procedure. Нет универсального количества безопасных просмотров validation. |


## S131 — страница работы (W1-11-S13)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.jmlr.org/papers/v13/bergstra12a.html>.

- F-связи: F100, F101, F102, F103, F104, F105, F106, F107, F108, F109.


| **S131** | James Bergstra, Yoshua Bengio, *Random Search for Hyper-Parameter Optimization*, JMLR13(10), **2012**, [страница работы](https://www.jmlr.org/papers/v13/bergstra12a.html) | Abstract pp.281–305: empirical/theoretical comparison grid/random на своих NN/DBN задачах; случайный поиск полезен при неравной важности dimensions. Не доказательство превосходства над expert targeted ablations в нашем бюджете; использован как ограниченный аргумент против полного grid. |


## S132 — scientific approach (W1-11-S14)

- Provenance: [W1-11](_WORK/W1_11.md); исходная карточка `W1-11-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook/scientific>; <https://github.com/google-research/tuning_playbook/blob/main/README.md>.

- F-связи: F101.


| **S132** | Varun Godbole, George Dahl, Justin Gilmer, Christopher Shallue, Zachary Nado; Google Research tuning playbook, [scientific approach](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook/scientific), live; [авторство/оговорки](https://github.com/google-research/tuning_playbook/blob/main/README.md) | *Pick a goal*, *Identify scientific, nuisance, fixed hyperparameters*. Рекомендации опытных авторов, живой текст, не pinned executable recipe и не controlled study нашего кейса. Например, LR может требовать retuning после изменения scientific factor; фиксирование ограничивает вывод. |


## S133 — Pricing (W1-12-S01)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/pricing>.

- F-связи: F110, F111, F112, F113, F114, F115, F116, F117.


| S133 | [Pricing](https://docs.vast.ai/guides/instances/pricing), How Pricing Works; Cost Components; Billing Basics, строки 108–125, 148–172, 225–230 | Live policy: рынок, разные компоненты, per-second; не live quote |


## S134 — Billing (W1-12-S02)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/reference/billing>.

- F-связи: F113.


| S134 | [Billing](https://docs.vast.ai/guides/reference/billing), Negative Balances; Pricing 191–196; Refunds; Loading 339–341; Charges 273; bandwidth 354–355 | Политика расходов/аккаунта, не наш invoice |


## S135 — Finding & Renting (W1-12-S03)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/choosing/find-and-rent>.

- F-связи: F113, F114.


| S135 | [Finding & Renting](https://docs.vast.ai/guides/instances/choosing/find-and-rent), Machine Tiers; Card Details; Instance Disk Size | Определения; не независимый аудит хоста |


## S136 — Instance Types (W1-12-S04)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/choosing/instance-types>.

- F-связи: F113.


| S136 | [Instance Types](https://docs.vast.ai/guides/instances/choosing/instance-types), On-demand Key Considerations; Interruptible; Priority Levels | Приоритет и expiry; не гарантия отсутствия outage |


## S137 — Managing Instances (W1-12-S05)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/manage-instances>.

- F-связи: F113, F114.


| S137 | [Managing Instances](https://docs.vast.ai/guides/instances/manage-instances), Starting/Stopping; Restart; Offline; Contract Expiration; Security | Lifecycle; не выполненная операция |


## S138 — Storage Types (W1-12-S06)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/types>.

- F-связи: F113.


| S138 | [Storage Types](https://docs.vast.ai/guides/instances/storage/types), 129–146, Volumes 169–197, How avoid charges | Allocation и отдельные volumes, не проверенный stopped ledger |


## S139 — Docker Environment (W1-12-S07)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/docker-environment>.

- F-связи: F113.


| S139 | [Docker Environment](https://docs.vast.ai/guides/instances/docker-environment), Resource Allocation 120–155 | Exclusive GPU / CPU RAM baseline, не measured utilization |


## S140 — Security FAQ (W1-12-S08)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/reference/faq/security>.

- F-связи: F113, F114.


| S140 | [Security FAQ](https://docs.vast.ai/guides/reference/faq/security), Data Protection; What is Secure Cloud | Заявления платформы; сертификат площадки не получен |


## S141 — Search offers API (W1-12-S09)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/api-reference/search/search-offers>.

- F-связи: F114.


| S141 | [Search offers API](https://docs.vast.ai/api-reference/search/search-offers), endpoint `/api/v0/bundles`, examples and response schema | Документирован POST+Bearer, поля; наш GET описан отдельно |


## S142 — Reserved Instances (W1-12-S10)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/choosing/reserved-instances>.

- F-связи: F113.


| S142 | [Reserved Instances](https://docs.vast.ai/guides/instances/choosing/reserved-instances), Important Considerations; Refunds 200–208; Stop 263–265 | Условия commitment; не конкретная скидка |


## S143 — Legacy console FAQ (W1-12-S11)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://console.vast.ai/faq/>.

- F-связи: F113.


| S143 | [Legacy console FAQ](https://console.vast.ai/faq/), Billing → How does pricing work? | Негативное evidence: конфликт с current offline billing |


## S144 — CLI search offers (W1-12-S12)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `42c3a47b44603775a5e31f54de0fce3994bd3f11`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/cli/reference/search-offers>; <https://github.com/vast-ai/vast-python/blob/42c3a47b44603775a5e31f54de0fce3994bd3f11/vast.py#L4369>.

- F-связи: F114.


| S144 | [CLI search offers](https://docs.vast.ai/cli/reference/search-offers), Usage, defaults, storage option; [pinned CLI source](https://github.com/vast-ai/vast-python/blob/42c3a47b44603775a5e31f54de0fce3994bd3f11/vast.py#L4369) | Синтаксис и единицы, код не запускался для rent |


## S145 — Public bundles endpoint (W1-12-S13)

- Provenance: [W1-12](_WORK/W1_12.md); исходная карточка `W1-12-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://console.vast.ai/api/v0/bundles/>.

- F-связи: F110, F111, F112, F113, F114, F115, F116, F117.


| S145 | [Public bundles endpoint](https://console.vast.ai/api/v0/bundles/), JSON query и локальные raw snapshots | Собственное наблюдение HTTP 200 и цен; быстро устаревает |


## S146 — release 2.14.1 (W1-13-S01)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.14.1`, `v2.14.1`, `0.29.1`, `v0.29.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/pytorch/pytorch/releases/tag/v2.14.1>; <https://github.com/pytorch/vision/releases/tag/v0.29.1>.

- F-связи: F119.


| S146 | PyTorch maintainers: [release 2.14.1](https://github.com/pytorch/pytorch/releases/tag/v2.14.1); [Vision 0.29.1](https://github.com/pytorch/vision/releases/tag/v0.29.1), Release/Packaging | 2026-09-30, exact commits F01; published version compatibility, не наш test |


## S147 — public tags API (W1-13-S02)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.14.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://hub.docker.com/v2/repositories/pytorch/pytorch/tags?page_size=30&name=2.14.1>.

- F-связи: F119.


| S147 | PyTorch Docker Hub [public tags API](https://hub.docker.com/v2/repositories/pytorch/pytorch/tags?page_size=30&name=2.14.1), selected result name/images/digest | Собственное HTTP read, registry metadata; не layer inspection |


## S148 — previous versions (W1-13-S03)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.6.0`, `5c4886908584029761b579af026dcfb627c84070`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/get-started/previous-versions/>; <https://github.com/pytorch/pytorch/blob/5c4886908584029761b579af026dcfb627c84070/Dockerfile>.

- F-связи: F119.


| S148 | PyTorch [previous versions](https://docs.pytorch.org/get-started/previous-versions/), верхний v2.6.0; [pinned Dockerfile](https://github.com/pytorch/pytorch/blob/5c4886908584029761b579af026dcfb627c84070/Dockerfile), official/python-deps stages | Live page inconsistency; versioned code, не доказательство точного upstream image build |


## S149 — Minor Version Compatibility (W1-13-S04)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html>.

- F-связи: F119.


| S149 | NVIDIA [Minor Version Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/minor-version-compatibility.html), table 1/Application Considerations | Live official compatibility docs; driver floor с условиями, не model benchmark |


## S150 — Docker Execution Environment (W1-13-S05)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/docker-environment>.

- F-связи: F119.


| S150 | Vast.ai [Docker Execution Environment](https://docs.vast.ai/guides/instances/docker-environment), Resource Allocation/Launch Modes/Environment Variables | Live platform contract; host limits и injected scripts |


## S151 — CLI source (W1-13-S06)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `42c3a47b44603775a5e31f54de0fce3994bd3f11`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-python/blob/42c3a47b44603775a5e31f54de0fce3994bd3f11/vast.py#L1594>.

- F-связи: F119.


| S151 | Vast.ai [CLI source](https://github.com/vast-ai/vast-python/blob/42c3a47b44603775a5e31f54de0fce3994bd3f11/vast.py#L1594), copy 1594–1707; create 2441–2564; start/stop 3949–4039; destroy 3152–3166; show 5720–5753 | Exact SHA 2026-10-23; source read, CLI не запускался; production release SHA отдельно F04 |


## S152 — pinned trainer (W1-13-S07)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py#L768>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py#L753>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/pyproject.toml>.

- F-связи: F119.


| S152 | Ultralytics [pinned trainer](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py#L768), save_model/final_eval/resume_training; [model.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py#L753), export/train; [pyproject](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/pyproject.toml); LICENSE | Exact SHA 2026-10-23; code/license/dependency evidence, не generic гарантия всех versions |


## S153 — Models and pre-trained weights (W1-13-S08)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/vision/stable/models.html>.

- F-связи: F119.


| S153 | TorchVision maintainers [Models and pre-trained weights](https://docs.pytorch.org/vision/stable/models.html), General information/Initializing/Pre-trained models | Page header 0.29; лицензии weights отдельно, DEFAULT mutable, preprocessing matters |


## S154 — venv 3.12 docs (W1-13-S09)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `3.12.15`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.python.org/3.12/library/venv.html>.

- F-связи: F119.


| S154 | Python [venv 3.12 docs](https://docs.python.org/3.12/library/venv.html), introduction/How venvs work | Page header 3.12.15; среда disposable/nonportable; не версия Python контейнера |


## S155 — Building best practices (W1-13-S10)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.docker.com/build/building/best-practices/>.

- F-связи: F119, F120.


| S155 | Docker [Building best practices](https://docs.docker.com/build/building/best-practices/), Pin base image versions | Live docs; digest vs mutable tag, не доступность Vast digest input |


## S156 — Secure installs (W1-13-S11)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `26.2.2`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pip.pypa.io/en/stable/topics/secure-installs/>.

- F-связи: F119.


| S156 | PyPA [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/), Hash-checking Mode/Additional restrictions | Header pip 26.2.2; pinned+hash всех dependencies, не готовый lock |


## S157 — Train (W1-13-S12)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.ultralytics.com/modes/train>; <https://docs.ultralytics.com/modes/export>.

- F-связи: F119.


| S157 | Ultralytics [Train](https://docs.ultralytics.com/modes/train), Usage/Resuming Interrupted Trainings; [Export](https://docs.ultralytics.com/modes/export), Usage/Arguments | Live docs (YOLO26, YOLO27 preview); интерфейсы сопоставлены pinned model/trainer/default.yaml, не accuracy claims |


## S158 — Reproducibility 2.14 (W1-13-S13)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.14.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/notes/randomness.html>; <https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html>.

- F-связи: F119.


| S158 | PyTorch [Reproducibility 2.14](https://docs.pytorch.org/docs/2.14/notes/randomness.html), opening/Controlling randomness/DataLoader; [Saving and Loading Models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html), General Checkpoint | Versioned docs + live tutorial header 2.14.0+cu130; seed limits/checkpoint basics, не полный strict replay всех trainers |


## S159 — Managing Instances (W1-13-S14)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/manage-instances>.

- F-связи: F119.


| S159 | Vast.ai [Managing Instances](https://docs.vast.ai/guides/instances/manage-instances), Starting/Stopping/Destroying, Restart Behavior/Data Persistence | Live lifecycle contract; actual state не наблюдался |


## S160 — Volumes (W1-13-S15)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/volumes>; <https://docs.vast.ai/guides/instances/storage/data-movement>.

- F-связи: F118, F119, F120, F121, F122, F123, F124.


| S160 | Vast.ai [Volumes](https://docs.vast.ai/guides/instances/storage/volumes), opening/Deleting/CLI; [Data Movement](https://docs.vast.ai/guides/instances/storage/data-movement), Instance copy/Constraints | Local-machine binding и transfer интерфейс; не backup/SLA |


## S161 — Cloud Sync (W1-13-S16)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/cloud-sync>.

- F-связи: F118, F119, F120, F121, F122, F123, F124.


| S161 | Vast.ai [Cloud Sync](https://docs.vast.ai/guides/instances/storage/cloud-sync), credentials warning immediately after introduction | Live docs: temporary host credentials/full granted access; ни один ключ не читался |


## S162 — CLI Hello World (W1-13-S17)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S17`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `626149741ba46f195c775b2f4c89b7329de2d902`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/cli/hello-world>; <https://docs.vast.ai/cli/reference/start-instance>.

- F-связи: F119.


| S162 | Vast.ai [CLI Hello World](https://docs.vast.ai/cli/hello-world), sections 1–10; [start instance](https://docs.vast.ai/cli/reference/start-instance), Usage | Live current syntax; docs repo HEAD `626149741ba46f195c775b2f4c89b7329de2d902` отдельно сохранён, deployed=HEAD не доказано |


## S163 — Build secrets (W1-13-S18)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S18`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.docker.com/build/building/secrets/>.

- F-связи: F121.


| S163 | Docker [Build secrets](https://docs.docker.com/build/building/secrets/), opening/Using build secrets | Live official docs: ARG/ENV persistence, secret/SSH mounts; не доверенная enclave на чужом host |


## S164 — torch.onnx 2.14 (W1-13-S19)

- Provenance: [W1-13](_WORK/W1_13.md); исходная карточка `W1-13-S19`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/onnx.html>.

- F-связи: F121.


| S164 | PyTorch [torch.onnx 2.14](https://docs.pytorch.org/docs/2.14/onnx.html), API signature/Changed in 2.9/2.11 | Page metadata Last Updated 2025-09-10 при header 2.14; version/API реальное evidence, дата metadata не версия runtime |


## S165 — trainer.py (W1-14-S01)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F125, F126.


| S165 | Ultralytics, [trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), SHA de290d8…, 2026-10-23 15:51:48Z; L670–685, L775–836, L1005–1022, L1071–1086, L1128–1145; версия в `ultralytics/__init__.py` L3 | Исполняемый checkpoint/restore/finalization код; не запускался. |


## S166 — torch_utils.py (W1-14-S02)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py>.

- F-связи: F125, F126.


| S166 | Ultralytics, [torch_utils.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py), тот же SHA; `strip_optimizer` L895–959; conversion L963–984 | Точные исключения FP32, удаление optimizer/scaler/epoch; не переносить на другие версии. |


## S167 — solver (W1-14-S03)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py>.

- F-связи: F126.


| S167 | Peterande/D-FINE, [solver](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py), SHA956d170…, 2026-08-19 15:08:14Z; L165–183, L201–247 | State discovery и load, permissive missing keys; реальное содержимое зависит от instantiated config. |


## S168 — det_solver.py (W1-14-S04)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py>.

- F-связи: F126.


| S168 | D-FINE, [det_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py), тот же SHA; L99–105,139–170 | Stage-specific saves/refresh; отсутствие универсального last-every-epoch. |


## S169 — trainer.py (W1-14-S05)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py>; <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/callbacks/ema.py>.

- F-связи: F126.


| S169 | Roboflow, [trainer.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py), L370–403,464–465; [EMA callback](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/callbacks/ema.py), L459–471; SHA5b22dfc…, 2026-10-16 05:38:07Z | Callback construction/state, статический анализ; actual Lightning version надо pin отдельно. |


## S170 — Managing Instances (W1-14-S06)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/manage-instances>.

- F-связи: F125.


| S170 | Vast.ai, [Managing Instances](https://docs.vast.ai/guides/instances/manage-instances), Starting/Stopping, Restart, Data Persistence, Contract Expiration | Live policy: stop/destroy, scheduling, expiry deletion; не SLA или выполненные операции. |


## S171 — Storage Types (W1-14-S07)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/types>.

- F-связи: F125, F126, F127, F128, F129, F130, F131, F132, F133, F134.


| S171 | Vast.ai, [Storage Types](https://docs.vast.ai/guides/instances/storage/types), Container Characteristics; Volume Limitations; Storage Costs | Local volume не cross-host backup; fixed allocation и separate billing. |


## S172 — Instance Types (W1-14-S08)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/choosing/instance-types>; <https://docs.vast.ai/guides/reference/billing>.

- F-связи: F125, F129.


| S172 | Vast.ai, [Instance Types](https://docs.vast.ai/guides/instances/choosing/instance-types), Interruptible/priority; [Billing](https://docs.vast.ai/guides/reference/billing), Pricing/Charges | Live условия, не live offer/invoice. Docs repo HEAD6261497…, 2026-10-21, не доказательство равенства deployed docs. Legacy FAQ отличается по offline charging; тарифы перед оплатой сверить по W1-12. |


## S173 — Saving/Loading tutorial (W1-14-S09)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html>.

- F-связи: F125.


| S173 | PyTorch team, [Saving/Loading tutorial](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html), General Checkpoint, displayed2.14.0+cu130 | Model-only недостаточно optimizer recovery. Tutorial не проверяет custom EMA/data cursor. |


## S174 — Reproducibility2.14 (W1-14-S10)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/notes/randomness.html>.

- F-связи: F125.


| S174 | PyTorch team, [Reproducibility2.14](https://docs.pytorch.org/docs/2.14/notes/randomness.html), introductory caveat, RNG и DataLoader; page Created/Updated May14,2026 | Ограничения across release/platform, worker reseeding; не обещание exact resume. |


## S175 — Checkpoint basic (W1-14-S11)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://lightning.ai/docs/pytorch/stable/common/checkpointing_basic.html>; <https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html>.

- F-связи: F126.


| S175 | Lightning team, [Checkpoint basic](https://lightning.ai/docs/pytorch/stable/common/checkpointing_basic.html), Contents и Resume; [ModelCheckpoint](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html), save_weights_only/every_n_epochs; displayed2.7.0.dev | Документирует full optimizer/scheduler/callback state и fit ckpt_path; unpinned live dependency docs. |


## S176 — os (W1-14-S12)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.python.org/3/library/os.html#os.replace>.

- F-связи: F128.


| S176 | Python Software Foundation, [os](https://docs.python.org/3/library/os.html#os.replace), `fsync`, `replace`; displayed3.15.1 | OS primitives, atomic same-filesystem rename; не гарантия hardware durability. Worker Python version здесь не выбрана. |


## S177 — check (W1-14-S13)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://rclone.org/commands/rclone_check/>.

- F-связи: F128.


| S177 | rclone authors, [check](https://rclone.org/commands/rclone_check/), Synopsis `--download`, `--one-way`, `--size-only` | Read-only content check, backend hash limits; live docs. Repo HEAD81e7372… 2026-10-20 — provenance, не pin установленного binary. |


## S178 — S3 (W1-14-S14)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://rclone.org/s3/>.

- F-связи: F128.


| S178 | rclone authors, [S3](https://rclone.org/s3/), Hashes, Multipart, Further checking | ETag/multipart caveat и read-back; реальные backend/encryption settings надо проверять. |


## S179 — nvidia-smi (W1-14-S15)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.nvidia.com/deploy/nvidia-smi/index.html>.

- F-связи: F131.


| S179 | NVIDIA, [nvidia-smi](https://docs.nvidia.com/deploy/nvidia-smi/index.html), SELECTIVE QUERY, Temperature, Clocks Event Reasons, memory, utilization | Официальный manual без pinned host driver; N/A/GeForce ограничения. Не наши temperature/performance измерения. |


## S180 — DataLoader2.14 (W1-14-S16)

- Provenance: [W1-14](_WORK/W1_14.md); исходная карточка `W1-14-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/data.html>.

- F-связи: F131.


| S180 | PyTorch team, [DataLoader2.14](https://docs.pytorch.org/docs/2.14/data.html), class DataLoader parameters timeout/worker_init_fn/generator/prefetch_factor, web L3924–3958 | Timeout относится к batch collection workers; не all-purpose hang recovery. |


## S181 — DistributedDataParallel API (W1-15-S01)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/generated/torch.nn.parallel.DistributedDataParallel.html>.

- F-связи: F135, F136, F137, F143.


| **S181** | PyTorch contributors, **2.14**, [DistributedDataParallel API](https://docs.pytorch.org/docs/2.14/generated/torch.nn.parallel.DistributedDataParallel.html) | Описание и Notes/Warnings, L554–660; `no_sync`, L791–808. Синхронизация градиентов, явное распределение input, отдельный процесс/GPU, требования одинакового графа/параметров и collective order. Документированная семантика, не speedup нашей задачи. |


## S182 — Distributed Overview (W1-15-S02)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.14.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/tutorials/beginner/dist_overview.html>.

- F-связи: F136.


| **S182** | Will Constable, Wei Feng / PyTorch, [Distributed Overview](https://docs.pytorch.org/tutorials/beginner/dist_overview.html), updated **2025-07-20**, страница tutorials 2.14.0+cu130 | *Applying Parallelism To Scale Your Model*, L299–322. Разделяет replicated DDP и sharding/model parallel при нехватке памяти. Не turnkey FSDP recipe для наших detectors. |


## S183 — torch.utils.data (W1-15-S03)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/data.html>.

- F-связи: F136, F137, F139.


| **S183** | PyTorch contributors, **2.14**, [torch.utils.data](https://docs.pytorch.org/docs/2.14/data.html) | *Single- and Multi-process Data Loading*, L3851–3867; *Memory Pinning*, L3889–3895; `DistributedSampler`, L4440–4482. Workers, RAM, pinned buffers; padding/drop tail и `set_epoch`. API-контракт, не оптимальное число workers. |


## S184 — CUDA semantics (W1-15-S04)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/notes/cuda.html>.

- F-связи: F135, F136, F137, F141.


| **S184** | PyTorch contributors, **2.14**, [CUDA semantics](https://docs.pytorch.org/docs/2.14/notes/cuda.html) | *Asynchronous execution*, L592–608; *Memory management*, L702–707. CUDA timers/synchronize, allocated/reserved peak, ограничения empty_cache. Не доказательство fit по одному nvidia-smi. |


## S185 — engine/trainer.py (W1-15-S05)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F135, F136, F137, F143.


| **S185** | Ultralytics contributors, SHA **de290d865035acbfa4bb24cc88960d8b52c26e45**, [engine/trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py) | `train`, `_setup_ddp`, `_build_train_pipeline`, `_do_train`, `validate`: raw L173–179,217–299,409–416,604–610,860+. Код: explicit multi-device DDP, batch/world-size, nbs-based accumulation, train/val в одном цикле; Multi-GPU AutoBatch запрещён. Это инспекция, не выполнение. |


## S186 — utils/dist.py (W1-15-S06)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/dist.py>.

- F-связи: F136, F143.


| **S186** | Ultralytics, тот же SHA, [utils/dist.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/dist.py) | `generate_ddp_command`, raw L106–133; `generate_ddp_file`, L46–104. Автогенерация локального launcher с `--nproc_per_node` и `--master_port`; удаляет save_dir нового запуска. Не готовое multi-node orchestration. Требуются уникальные каталоги runs. |


## S187 — misc/dist_utils.py (W1-15-S07)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/misc/dist_utils.py>.

- F-связи: F135, F136, F143.


| **S187** | D-FINE authors/Peterande, SHA **956d1709314c2c6a4df6f34de232054578a7449f**, [misc/dist_utils.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/misc/dist_utils.py) | `setup_distributed`, raw L24–59: `set_device(rank)` после `get_rank`; `warp_model`, L118–144: `device_ids=[rank]`; `warp_loader`, L150–162. Global/local rank mismatch — проверенное наличие кода, предполагаемый multi-node failure — вывод, а не наш runtime log. |


## S188 — core/yaml_config.py (W1-15-S08)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/core/yaml_config.py>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py>.

- F-связи: F135, F136, F137.


| **S188** | D-FINE, тот же SHA, [core/yaml_config.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/core/yaml_config.py), [solver/det_engine.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py) | Первый: `get_rank_batch_size`, raw L145–170: total_batch_size делится на world_size, batch_size является per-rank. Второй: `train_one_epoch`, raw L54–108, optimizer step каждый batch; `evaluate`, L135+. Два первичных файла, не демонстрация memory fit. |


## S189 — training/trainer.py (W1-15-S09)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py>.

- F-связи: F135, F136, F137, F143.


| **S189** | Roboflow/RF-DETR, SHA **5b22dfc0940697ce1abdfa681a5f7392b3eddbfb**, [training/trainer.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/training/trainer.py) | `build_trainer`, raw L687–690,758–826,855–920. DDPStrategy/find_unused_parameters; static_graph guard при accumulation; devices/num_nodes; штатная validation и standalone evaluate используют общий COCO callback. Detection accumulation передаётся Lightning; keypoint manual optimization — иной путь. Код содержит собственный L4 benchmark comment, его числа здесь не переносятся на 3090. |


## S190 — torchrun (W1-15-S10)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/elastic/run.html>.

- F-связи: F136, F143.


| **S190** | PyTorch contributors, **2.14**, [torchrun](https://docs.pytorch.org/docs/2.14/elastic/run.html) | *Single-node multi-worker*, *Stacked single-node multi-worker*, *Fault tolerant*, L3738–3780; *Important Notices* далее. Local ranks, rendezvous endpoints, отдельные ports/job IDs и конфигурация multi-node. Generic launcher не исправляет ошибочный rank mapping trainer. |


## S191 — Profiler recipe (W1-15-S11)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `2.14.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html>.

- F-связи: F136, F141.


| **S191** | PyTorch contributors, [Profiler recipe](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html), tutorials 2.14.0+cu130, live | *Using profiler to analyze execution time*, CPU/CUDA activities; scheduled profiling/trace export. Основание для диагностики по trace; overhead profiler надо отделять от основного throughput measurement. |


## S192 — Pricing (W1-15-S12)

- Provenance: [W1-15](_WORK/W1_15.md); исходная карточка `W1-15-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/pricing>.

- F-связи: F136, F140.


| **S192** | Vast.ai, [Pricing](https://docs.vast.ai/guides/instances/pricing), live, явная publication date не установлена | *How Pricing Works*, *Cost Components*, *Billing Basics*. Compute, storage и transfers отдельны; ставки рыночные. W1-12 хранит собственные read-only quotes, не полученные здесь заново и не гарантированные к будущей аренде. |


## S193 — engine/exporter.py (W1-16-S01)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py>.

- F-связи: F145, F147.


| S193 | Ultralytics, [engine/exporter.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py), SHA `de290d…`, `Exporter.__call__` raw L690–707,779–786,958–965; `export_onnx` L1080–1120 | Code: exact flags/head metadata/ONNX names. Это проверка логики, не состоявшийся экспорт |


## S194 — nn/modules/head.py (W1-16-S02)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py>.

- F-связи: F145.


| S194 | Ultralytics, [nn/modules/head.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py), тот же SHA, `Detect.end2end` L145–155, `forward/_inference` L166–208, `postprocess/get_topk_index` L229+ | Code: actual head/fusion и output semantics. Source docs не подменяют artifact inspection |


## S195 — utils/export/engine.py (W1-16-S03)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/export/engine.py>.

- F-связи: F147, F150.


| S195 | Ultralytics, [utils/export/engine.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/export/engine.py), тот же SHA, `torch2onnx` L83–118, `best_onnx_opset` L57–80 | Code: legacy mode и env-dependent default opset; не LinQ limits |


## S196 — export_onnx.py (W1-16-S04)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py>.

- F-связи: F147.


| S196 | D-FINE authors/Peterande, [export_onnx.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py), SHA `956d170…`, L27–50,54–91 | Code: EMA, deploy wrapper, batch32/dynamic batch, opset16, checker/simplify. Actual checker/ORT/TPU run не было |


## S197 — docs/exports/onnx.md (W1-16-S05)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/exports/onnx.md>.

- F-связи: F145, F147.


| S197 | Roboflow, [docs/exports/onnx.md](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/docs/exports/onnx.md), SHA `5b22df…`, `ONNX Inference` L5–12,59–61 | Pinned docs: raw tensors, class-layout background, names ambiguity и argmax vs global pairs. Quantization раздел не использован как LinQ recipe |


## S198 — export/_onnx/exporter.py (W1-16-S06)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/export/_onnx/exporter.py>.

- F-связи: F147, F150.


| S198 | Roboflow, [export/_onnx/exporter.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/export/_onnx/exporter.py), тот же SHA, `OnnxConfig` L29–42, `_trace` L146–171 | Code: opset17 default, actual exporter mode/config. Это snapshot, не установленный wheel |


## S199 — export/_onnx/inference.py (W1-16-S07)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/export/_onnx/inference.py>.

- F-связи: F145, F147.


| S199 | Roboflow, [export/_onnx/inference.py](https://github.com/roboflow/rf-detr/blob/5b22dfc0940697ce1abdfa681a5f7392b3eddbfb/src/rfdetr/export/_onnx/inference.py), тот же SHA, `_run_inference` L91–128,139–179 | Code+docstring: exact preprocess, selection arguments и name/shape/positional fallback. Предлагаемый fail-closed manifest — наше решение |


## S200 — torch.onnx API 2.14 (W1-16-S08)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/onnx.html>.

- F-связи: F145, F147, F150.


| S200 | PyTorch contributors, [torch.onnx API 2.14](https://docs.pytorch.org/docs/2.14/onnx.html), versioned docs, raw web L3782–3823, раздел `torch.onnx APIs`; publication date страницы не установлена | Docs: opset выбирать под backend, dynamo/default и `verify`/`report` applicability. Не dependency pin кандидатов и не accelerator test |


## S201 — onnx.checker (W1-16-S09)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1.24.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://onnx.ai/onnx/api/checker.html>.

- F-связи: F147, F150.


| S201 | ONNX contributors, [onnx.checker](https://onnx.ai/onnx/api/checker.html), docs показывают **1.24.0**, `check_model` L1428–1444 | Docs: consistency/IR/opset/custom-domain/shape check; отсутствие numerical/target proof — наша граница выводов |


## S202 — Технологический стек /docs (W1-16-S10)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://lin-q.ru/docs>.

- F-связи: F145, F149.


| S202 | ООО «ХайТэк»/LinQ, [Технологический стек /docs](https://lin-q.ru/docs), live undated; раздел `Фреймворк` → `Руководство оператора. Фреймворк` | Fresh TinyFish text+links+metadata; source confirms link provenance. Web direct не смог открыть, это не отсутствие страницы |


## S203 — IVA H1 operator manual (W1-16-S11)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `04.06.014-03`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf>.

- F-связи: F145, F149.


| S203 | ООО «ХайТэк», [IVA H1 operator manual](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), **2025**, `RU.РМДВ.04.06.014-03 34 01`, 28 листов; §3.3 p11; §3.4 pp11–21; tested models pp21–22; sample output p24 | Fresh full PDF text extraction через TinyFish, не screenshot. Исторический conversion/compile/runtime/parity example; не current SDK и не проверка современных detectors |


## S204 — главная (W1-16-S12)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://lin-q.ru/>; <https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf>.

- F-связи: F145, F149.


| S204 | LinQ/ООО «ХайТэк», [главная](https://lin-q.ru/), `ПРОИЗВОДИТЕЛЬНОСТЬ/ИНТЕГРАЦИЯ`; [HPS datasheet](https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf), p1 программный стек/p2 formats; revision/date в открытом тексте не установлены | Vendor claims PyTorch via ONNX/compiler/profiler. Не идентификация оборудования кейса, не наш runtime/precision measurement |


## S205 — onnx_inf.py (W1-16-S13)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/inference/onnx_inf.py>.

- F-связи: F147.


| S205 | D-FINE authors, [onnx_inf.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/inference/onnx_inf.py), SHA `956d170…`, `resize_with_aspect_ratio`, `process_image`, `draw`, L11–66 | Code: padding/size/ToTensor/inverse geometry. Не доказательство совпадения со всеми training/test pipelines |


## S206 — utils.py (W1-16-S14)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `df2a96c8c3a098567a1149bf0248da6efe6d495d`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/src/zoo/rtdetr/utils.py>.

- F-связи: F147.


| S206 | Wenyu Lyu/RT-DETR authors, [utils.py](https://github.com/lyuwenyu/RT-DETR/blob/df2a96c8c3a098567a1149bf0248da6efe6d495d/rtdetrv2_pytorch/src/zoo/rtdetr/utils.py), SHA `df2a96…`, `deformable_attention_core_func_v2`, L83–112 | Code: grid_sample/discrete distinction и rectangle FIXME. Не inferred LinQ operator support |


## S207 — export_onnx.py (W1-16-S15)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6ddff4824372906469a7fae2dc3206c7aa4bbaee`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/tools/export_onnx.py>.

- F-связи: F147.


| S207 | Megvii/YOLOX authors, [export_onnx.py](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/tools/export_onnx.py), SHA `6ddff4…`, parser L26–53, main L75–100 | Code: opset11/batch1/static/decode flag/legacy export. Не готовый современный Torch/LinQ рецепт |


## S208 — engine/predictor.py (W1-16-S16)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/predictor.py>.

- F-связи: F145, F146, F147, F148, F149, F150, F151, F152.


| S208 | Ultralytics, [engine/predictor.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/predictor.py), SHA `de290d…`, `preprocess` L168–190 | Code: tensor input уже normalized/RGB vs list BGR uint8. Основание хранить actual preprocessor и golden tensor, не считать путь PIL/OpenCV эквивалентным |


## S209 — Execution Providers (W1-16-S17)

- Provenance: [W1-16](_WORK/W1_16.md); исходная карточка `W1-16-S17`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://onnxruntime.ai/docs/execution-providers/>; <https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html>.

- F-связи: F145, F146, F147, F148, F149, F150, F151, F152.


| S209 | Microsoft/ONNX Runtime contributors, [Execution Providers](https://onnxruntime.ai/docs/execution-providers/), live undated, L169–190; [Profiling tools](https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html), `Performance profiling` | Docs: node/subgraph allocation и profiler mechanism. Наличие ORT/provider не доказывает LinQ execution; не утверждается наличие LinQ EP |


## S210 — trainer.py (W2-A-S01)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F154, F155, F157.


| S210 | Ultralytics contributors, [trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), L301–339, 450–466, 474–640, 651–685 | OOM/pipeline/warmup. SHA тот же, что W1, получен заново; код не исполнялся. |


## S211 — W2-A-S02 / локальное свидетельство (W2-A-S02)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py>.

- F-связи: F154, F155, F157.


| S211 | Тот же source, L768–837, 909–920, 1005–1022, 1071–1145 | save/repair, scaler/EMA, NaN/resume; control flow, не docstring. |
URL того же source: https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py . Locator L768–837,909–920,1005–1022,1071–1145.


## S212 — default.yaml (W2-A-S03)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/__init__.py>.

- F-связи: F154, F156.


| S212 | Ultralytics, [default.yaml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml) целиком; [cfg/__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/__init__.py), get_cfg L350+, check_dict_alignment L638–685 | Stock keys и rejection неизвестных overrides; отрицательный результат только для данного SHA. |


## S213 — callbacks/base.py (W2-A-S04)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/callbacks/base.py>; <https://docs.ultralytics.com/usage/callbacks>.

- F-связи: F154, F157.


| S213 | Ultralytics [callbacks/base.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/callbacks/base.py), L31–40,61–64,127–147; [Callbacks](https://docs.ultralytics.com/usage/callbacks), Trainer Callbacks/Forward Hooks | Pinned registry плюс live docs. Docs прямо отмечают reserved callbacks; live page не recipe pin. |


## S214 — model.py (W2-A-S05)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py>; <https://docs.ultralytics.com/usage/engine>.

- F-связи: F154, F156.


| S214 | Ultralytics [model.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py), train L807+,888; [Advanced Customization](https://docs.ultralytics.com/usage/engine), BaseTrainer/Using YOLO with Custom Trainers | Публичный subclass entrypoint; private recovery methods не стабильный API. |


## S215 — AMP examples 2.14 (W2-A-S06)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.14.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/notes/amp_examples.html>; <https://github.com/pytorch/pytorch/blob/v2.14.0/torch/amp/grad_scaler.py>.

- F-связи: F154, F157.


| S215 | PyTorch contributors [AMP examples 2.14](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html), Gradient clipping/accumulation; [GradScaler v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/amp/grad_scaler.py), raw L364–479,486–556 | Generic skip и fused special path. Tag, не выбранная установленная dependency. GitHub API resolution SHA получила 403 rate limit; tag не выдаём за независимо проверенный SHA. Raw bytes сохранены. |


## S216 — step_post_hook 2.14 (W2-A-S07)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.14.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.pytorch.org/docs/2.14/generated/torch.optim.Optimizer.register_step_post_hook.html>; <https://github.com/pytorch/pytorch/blob/v2.14.0/torch/optim/adam.py>.

- F-связи: F154, F157.


| S216 | PyTorch [step_post_hook 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.optim.Optimizer.register_step_post_hook.html), signature/description; [Adam v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/optim/adam.py), raw L104–107,810–899 | Hook означает вызов step, не гарантию applied update; fused found_inf корректирует state steps. |


## S217 — torch_utils.py (W2-A-S08)

- Provenance: [W2-A](_WORK/W2_A.md); исходная карточка `W2-A-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py>.

- F-связи: F154.


| S217 | Ultralytics [torch_utils.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py), strip_optimizer L895–959; [__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py) L3 | Stripping/version; runtime artifact contents предстоит load-verify. |


## S218 — Previous versions (W2-B-S01)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.5.1`, `v2.4.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pytorch.org/get-started/previous-versions/>.

- F-связи: F160, F164.


| **S218** | PyTorch contributors, live [Previous versions](https://pytorch.org/get-started/previous-versions/), sections v2.5.1/v2.4.1 | Official Torch/vision pairs + cu124/CPU install indexes; release versions, не installed env |


## S219 — pyproject.toml (W2-B-S02)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/pyproject.toml>.

- F-связи: F160, F164.


| **S219** | Ultralytics, SHA de290d…, [pyproject.toml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/pyproject.toml), project/dependencies/export-base/export-legacy-torch | Declared constraints/markers; не whole dependency resolution |


## S220 — requirements.txt (W2-B-S03)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/requirements.txt>.

- F-связи: F164.


| **S220** | Peng et al., SHA956d170…, [requirements.txt](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/requirements.txt), весь9-line file | Native minimal requirements; ONNX stack отсутствует |


## S221 — torch/onnx/__init__.py (W2-B-S04)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.5.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/pytorch/pytorch/blob/v2.5.1/torch/onnx/__init__.py>.

- F-связи: F160, F164.


| **S221** | PyTorch, tagv2.5.1, [torch/onnx/__init__.py](https://github.com/pytorch/pytorch/blob/v2.5.1/torch/onnx/__init__.py), export signature dynamo=False | Versioned API, not model compatibility |


## S222 — utils/export/engine.py (W2-B-S05)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/export/engine.py>.

- F-связи: F160.


| **S222** | Ultralytics, de290d…, [utils/export/engine.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/export/engine.py), torch2onnx/best_onnx_opset | Explicit legacy and version-dependent automatic opset |


## S223 — engine/exporter.py (W2-B-S06)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py>.

- F-связи: F162.


| **S223** | Ultralytics, de290d…, [engine/exporter.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py), Exporter.__call__/export_onnx | Head selection/native package checks/output names; local fresh copy preserved |


## S224 — export_onnx.py (W2-B-S07)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py>.

- F-связи: F160, F163, F164.


| **S224** | Peng et al.,956d170…, [export_onnx.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py), main/parser | EMA/deploy/batch32/opset16/dynamic axes/defaultTrue simplify; no explicit dynamo |


## S225 — PyPI1.17.0 metadata (W2-B-S08)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1.17.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pypi.org/pypi/onnx/1.17.0/json>.

- F-связи: F160.


| **S225** | ONNX contributors, [PyPI1.17.0 metadata](https://pypi.org/pypi/onnx/1.17.0/json), info.requires_python/requires_dist/urls | Declared distributions only; saved JSON |


## S226 — PyPI1.20.1 metadata (W2-B-S09)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1.20.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pypi.org/pypi/onnxruntime/1.20.1/json>.

- F-связи: F160, F161, F162, F163, F164, F165, F166.


| **S226** | Microsoft ORT contributors, [PyPI1.20.1 metadata](https://pypi.org/pypi/onnxruntime/1.20.1/json), requires_dist/urls | CPU distribution, not provider/hardware performance |


## S227 — compatibility (W2-B-S10)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v1.20.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://onnxruntime.ai/docs/reference/compatibility.html>; <https://github.com/microsoft/onnxruntime/blob/v1.20.1/docs/Versioning.md>.

- F-связи: F164.


| **S227** | Microsoft ORT, [compatibility](https://onnxruntime.ai/docs/reference/compatibility.html), ONNX opset support row1.20; [versioned v1.20.1 policy](https://github.com/microsoft/onnxruntime/blob/v1.20.1/docs/Versioning.md) | Version/opset/IR necessary bounds, no exhaustive environment guarantee |


## S228 — README (W2-B-S11)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md>.

- F-связи: F160.


| **S228** | Peng et al.,956d170…, [README](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md), Quick start/Setup + model zoo M | Python3.11.9; COCO checkpoint URL; no Torch pin |


## S229 — torch/onnx/utils.py (W2-B-S12)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.4.1`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/pytorch/pytorch/blob/v2.4.1/torch/onnx/utils.py>.

- F-связи: F160, F164.


| **S229** | PyTorch, v2.4.1, [torch/onnx/utils.py](https://github.com/pytorch/pytorch/blob/v2.4.1/torch/onnx/utils.py), export signature L176–196 | Fallback API accepts dynamo=False, not executed |


## S230 — head.py (W2-B-S13)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py>.

- F-связи: F162.


| **S230** | Ultralytics, de290d…, [head.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py), Detect.end2end/forward/fuse/postprocess | Fusion/head conditional; actual checkpoint not inspected |


## S231 — postprocessor.py (W2-B-S14)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/zoo/dfine/postprocessor.py>.

- F-связи: F163.


| **S231** | Peng et al.,956d170…, [postprocessor.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/zoo/dfine/postprocessor.py), forward/deploy | scaling/query selection/early deploy return before remap |


## S232 — transformers4.44.2 metadata (W2-B-S15)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `4.44.2`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pypi.org/pypi/transformers/4.44.2/json>.

- F-связи: F164.


| **S232** | Hugging Face team, [transformers4.44.2 metadata](https://pypi.org/pypi/transformers/4.44.2/json), info.requires_python/requires_dist | Candidate pin, not D-FINE authors tested env |


## S233 — calflops0.3.2 metadata (W2-B-S16)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S16`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `0.3.2`, `0.4.36`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pypi.org/pypi/calflops/0.3.2/json>; <https://pypi.org/pypi/onnxsim/0.4.36/json>.

- F-связи: F164.


| **S233** | MrYXJ/calflops contributors, [calflops0.3.2 metadata](https://pypi.org/pypi/calflops/0.3.2/json); [onnxsim0.4.36 metadata](https://pypi.org/pypi/onnxsim/0.4.36/json) | Dependency edges; onnxsim optional in our adapter |


## S234 — v2.6.0 release notes (W2-B-S17)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S17`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v2.6.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/pytorch/pytorch/releases/tag/v2.6.0>.

- F-связи: F164.


| **S234** | PyTorch, [v2.6.0 release notes](https://github.com/pytorch/pytorch/releases/tag/v2.6.0), Backwards Incompatible changes / Flip default torch.load | Documented behavior change, not observed D-FINE failure |


## S235 — _solver.py (W2-B-S18)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S18`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py>.

- F-связи: F164.


| **S235** | Peng et al.,956d170…, [_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py), load_resume_state/load_tuning_state | torch.load without explicit weights_only; strict/mismatched state rules |


## S236 — opencv-python4.10.0.84 metadata (W2-B-S19)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S19`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `10.0.84`, `4.10.0.84`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://pypi.org/pypi/opencv-python/4.10.0.84/json>.

- F-связи: F164.


| **S236** | OpenCV wheels maintainers, [opencv-python4.10.0.84 metadata](https://pypi.org/pypi/opencv-python/4.10.0.84/json) | Python-conditioned numpy minimum; no binary import test |


## S237 — det_engine.py (W2-B-S20)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S20`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py>.

- F-связи: F164.


| **S237** | Peng et al.,956d170…, [det_engine.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py), train_one_epoch AMP/nonfinite | Save NaN.pth, scaler step/update, not runtime audit |


## S238 — det_solver.py (W2-B-S21)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S21`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py>.

- F-связи: F164.


| **S238** | Peng et al.,956d170…, [det_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py), stop_epoch block | Native best_stg1 reload/EMA decay mutation |


## S239 — train.py (W2-B-S22)

- Provenance: [W2-B](_WORK/W2_B.md); исходная карточка `W2-B-S22`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/train.py>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dataset/custom_detection.yml>.

- F-связи: F160, F161, F162, F163, F164, F165, F166.


| **S239** | Peng et al.,956d170…, [train.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/train.py), parser/main; [M custom](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml); [custom dataset](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dataset/custom_detection.yml) | Exact flags/config includes and placeholder class/path; recipes not run |


## S240 — paper (W2-C-S01)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `4.3.4`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2606.03748v1>.

- F-связи: F168.


| S240 | Ultralytics, [paper](https://arxiv.org/html/2606.03748v1), arXiv2606.03748v1, **2026-06-02**; §4.3.4/Table6, Table7, Supplement S4/TableS8 | Published model/ablation results; не наш paired benchmark. Selected claims ограничены small/head comparison |


## S241 — training recipe pinned (W2-C-S02)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`, `8.4.184`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/yolo26-training-recipe.md>.

- F-связи: F167, F168, F169.


| S241 | Ultralytics [training recipe pinned](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/guides/yolo26-training-recipe.md), SHA de290d865035acbfa4bb24cc88960d8b52c26e45 /8.4.184; Training Overview, Stage1, optimizer table S column | Author recipe/lineage claim, не инспекция бинарника; локально yolo_recipe.txt |


## S242 — D-FINE paper (W2-C-S03)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2410.13842v1>.

- F-связи: F168.


| S242 | Yansong Peng et al., [D-FINE paper](https://arxiv.org/html/2410.13842v1), 2024-10-17; A.1/Table6, A.1.2, A.2/Fig5, A.3/Table7 | Published size/split/schedules/qualitative; quantitative occlusion для M отсутствует в проверенных местах |


## S243 — M config (W2-C-S04)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/dfine_hgnetv2_m_coco.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/objects365/dfine_hgnetv2_m_obj2coco.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dfine_hgnetv2.yml>; <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/nn/backbone/hgnetv2.py>.

- F-связи: F168, F169.


| S243 | D-FINE [M config](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/dfine_hgnetv2_m_coco.yml), [O365→COCO config](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/objects365/dfine_hgnetv2_m_obj2coco.yml), [include](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/include/dfine_hgnetv2.yml), [backbone](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/nn/backbone/hgnetv2.py); SHA956d1709314c2c6a4df6f34de232054578a7449f; HGNetv2 arch_configs/B2, constructor pretrained branch; loader Resize/base_size | Pinned code/static read. Explicit schedule/load defaults, не доказанная native artifact execution |


## S244 — HF model card pinned (W2-C-S05)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `19214e91f5ce4c1e609022c38b1fc953c47404e7`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://huggingface.co/Peterande/D-FINE/blob/19214e91f5ce4c1e609022c38b1fc953c47404e7/README.md>; <https://huggingface.co/api/models/Peterande/D-FINE/tree/19214e91f5ce4c1e609022c38b1fc953c47404e7?expand=true>; <https://huggingface.co/Peterande>.

- F-связи: F167, F169.


| S244 | Yansong Peng/Peterande, [HF model card pinned](https://huggingface.co/Peterande/D-FINE/blob/19214e91f5ce4c1e609022c38b1fc953c47404e7/README.md), [tree API](https://huggingface.co/api/models/Peterande/D-FINE/tree/19214e91f5ce4c1e609022c38b1fc953c47404e7?expand=true), [author profile](https://huggingface.co/Peterande); revision19214e9… /2024-10-30; YAML license, M file lfs oid/lastCommit | Explicit model-repo designation+metadata, linked author identity. No weight bytes read; `safe` scanner labels не использованы как гарантия |


## S245 — pinned model docs (W2-C-S06)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`, `v8.4.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo26.md>; <https://api.github.com/repos/ultralytics/assets/releases/tags/v8.4.0>.

- F-связи: F169.


| S245 | Ultralytics [pinned model docs](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/models/yolo26.md), Availability and Licensing; [release API](https://api.github.com/repos/ultralytics/assets/releases/tags/v8.4.0), asset340096060 | Explicit code/models/docs scope; metadata digest. Release tag/code revision разные вещи |


## S246 — license page (W2-C-S07)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.ultralytics.com/license>.

- F-связи: F169.


| S246 | Ultralytics [license page](https://www.ultralytics.com/license), live undated, Choosing your license / proprietary use / custom-trained use | Vendor scope statement; не независимое legal opinion и не принятие условий командой |


## S247 — D-FINE README pinned (W2-C-S08)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `956d1709314c2c6a4df6f34de232054578a7449f`, `39a3115d4b1183b9035e333e57655f018272ebbe`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md>; <https://github.com/Peterande/storage/blob/39a3115d4b1183b9035e333e57655f018272ebbe/LICENSE>.

- F-связи: F169.


| S247 | Peterande [D-FINE README pinned](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md), ModelZoo Notes/License note; [storage LICENSE](https://github.com/Peterande/storage/blob/39a3115d4b1183b9035e333e57655f018272ebbe/LICENSE), release dfinev1.0→commit39a3115d4b1183b9035e333e57655f018272ebbe; Apache §2/4 | Project/storage grant, dataset caveat; автоматического exact-backbone grant не выводим |


## S248 — YOLOX README pinned (W2-C-S09)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6ddff4824372906469a7fae2dc3206c7aa4bbaee`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/README.md>; <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE>.

- F-связи: F168, F169.


| S248 | Megvii, [YOLOX README pinned](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/README.md), StandardModels current/Legacy; [LICENSE](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE) | Author checkpoint provenance/claimed benchmark; Apache code, не explicit individual weight designation |


## S249 — YOLOX paper (W2-C-S10)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `6ddff4824372906469a7fae2dc3206c7aa4bbaee`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://arxiv.org/html/2107.08430v2>; <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/exp/yolox_base.py>.

- F-связи: F170.


| S249 | Zheng Ge et al., [YOLOX paper](https://arxiv.org/html/2107.08430v2), **2021-08-06**; §2.1 training/pretrain, §2.2/Table3; [base exp](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/exp/yolox_base.py), max_epoch/no_aug/input_size | Paper legacy lineage + current code defaults; не точные training logs выбранного release |


## S250 — 0.1.1rc0 release (W2-C-S11)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `0.1.1rc0`, `e1052df71842031413f6030723c3607b839c80ce`, `6ddff4824372906469a7fae2dc3206c7aa4bbaee`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/releases/tag/0.1.1rc0>; <https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/docs/updates_note.md>.

- F-связи: F168, F170.


| S250 | Megvii [0.1.1rc0 release](https://github.com/Megvii-BaseDetection/YOLOX/releases/tag/0.1.1rc0), commit e1052df71842031413f6030723c3607b839c80ce, 2021; [updates_note pinned](https://github.com/Megvii-BaseDetection/YOLOX/blob/6ddff4824372906469a7fae2dc3206c7aa4bbaee/docs/updates_note.md), Breaking changes | Primary release, preprocessing incompatibility; HEAD asset last-modified не release date |


## S251 — issue1865 (W2-C-S12)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/Megvii-BaseDetection/YOLOX/issues/1865>.

- F-связи: F167, F169.


| S251 | YOLOX repository [issue1865](https://github.com/Megvii-BaseDetection/YOLOX/issues/1865), uenishi-tech2026-03-31 + wjkim812026-10-14, description/activity | Primary record of unresolved questions; users не уполномоченные licensors. Видимого ответа maintainer не обнаружено |


## S252 — COCOeval (W2-C-S13)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py>.

- F-связи: F168.


| S252 | Tsung-Yi Lin/Piotr Dollár, [COCOeval](https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py), live master, toolbox2.0; Params.setDetParams, evaluateImg gt area/ignore | Metric semantics; upstream commit API403, поэтому это **не pinned evaluator recipe**. Для будущего собственного benchmark evaluator pin обязателен |


## S253 — download/terms (W2-C-S14)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `de290d865035acbfa4bb24cc88960d8b52c26e45`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://www.objects365.org/download.html>; <https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/datasets/detect/objects365.md>.

- F-связи: F169.


| S253 | Objects365 Consortium, [download/terms](https://www.objects365.org/download.html), live undated; academic purpose, Annotations & Website, Images; Ultralytics [Objects365 pinned page](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/docs/en/datasets/detect/objects365.md), YAML license vs pretrained section | Primary upstream terms против abbreviated secondary project labeling. Вывод о правовом статусе обученных весов не сделан |


## S254 — W2-C-S15 / локальное свидетельство (W2-C-S15)

- Provenance: [W2-C](_WORK/W2_C.md); исходная карточка `W2-C-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v8.4.0`, `19214e91f5ce4c1e609022c38b1fc953c47404e7`, `0.1.1rc0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt>; <https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth>; <https://huggingface.co/Peterande/D-FINE/resolve/19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth>; <https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_obj2coco.pth>; <https://github.com/Peterande/storage/releases/download/dfinev1.0/PPHGNetV2_B2_stage1.pth>; <https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth>.

- F-связи: F167, F168, F169, F170, F171, F172.


| S254 | HTTP HEAD exact asset URLs в таблице; локально HEAD_SUMMARY.json/head_metadata.json, 2026-10-23T17:34Z | **Наше наблюдение metadata**, 302→200, MIME/length/disposition; больших response bodies не скачивалось |
Точные HEAD URL: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt ; https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth ; https://huggingface.co/Peterande/D-FINE/resolve/19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth ; https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_obj2coco.pth ; https://github.com/Peterande/storage/releases/download/dfinev1.0/PPHGNetV2_B2_stage1.pth ; https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth .


## S255 — UR Fall Detection Dataset (W2-D-S01)

- Provenance: [W2-D](_WORK/W2_D.md); исходная карточка `W2-D-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://fenix.ur.edu.pl/~mkepski/ds/uf.html>.

- F-связи: F173, F175.


**S255.** Michal Kępski / University of Rzeszow, [UR Fall Detection Dataset](https://fenix.ur.edu.pl/~mkepski/ds/uf.html). Версия страницы не указана; связанная авторская статья Kwolek/Kępski — December 2014. Доступ 2026-10-23. Локаторы: вводное описание, synchronization paragraph, license, Fall row 01, ADL row 01, Extracted features. Вид: primary dataset documentation. Коротко: 30 fall/40 ADL sequences; два вида fall и один ADL; отдельные PNG streams; время в ms от начала sequence, независимые камеры сведены ближайшими timestamps. Разметка posture в depth-derived features имеет отдельные лежит/не лежит/переход. Это не RGB bbox/track/онлайн-event GT. Условия: CC BY-NC-SA 4.0, academic/noncommercial scope; commercial use требует отдельного согласования с авторами, контактов не было. Сохранён оригинальный HTML, SHA256 `cb6d171be52c086ece579457b9ee752abb25e335b12aae25ee28714fb94aae83`. Обобщение на industrial камеры и разрешение конкретного конкурсного режима не установлены.


## S256 — Dataset CAUCAFall v5 (W2-D-S02)

- Provenance: [W2-D](_WORK/W2_D.md); исходная карточка `W2-D-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://data.mendeley.com/datasets/7w7fccy7ky/5>.

- F-связи: F173, F175.


**S256.** Jose Camilo Eraso, Elena Muñoz, Mariela Muñoz, Jesus Pinto, [Dataset CAUCAFall v5](https://data.mendeley.com/datasets/7w7fccy7ky/5), DOI **10.17632/7w7fccy7ky.5**, опубликован **18 March 2025**. Доступ 2026-10-23. Локаторы: Description paragraphs 2–4; Steps to reproduce paragraphs 1–2; Licence. Вид: versioned primary dataset card. Коротко: subject/activity folders, AVI/PNG/TXT, manually labeled fall/no-fall segmentation; CC BY 4.0. Камера nominal 23 FPS, 1080×960; это описание capture, не проверка каждого AVI. DVR начинает motion-triggered запись при входе. Камера/incident/session lineage, event onset/observable и negative exposure ещё требуют просмотра/manifest. Синхронного primary file list/конкретного видео не получили. Web open успешен; независимый `urllib` page/API 403, отражено в `fetch.json`. Наличие repository card не приравнено к скачанному архиву.


## S257 — fall-01-data.csv (W2-D-S03)

- Provenance: [W2-D](_WORK/W2_D.md); исходная карточка `W2-D-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-data.csv>.

- F-связи: F173, F175.


**S257.** URFD, [fall-01-data.csv](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-data.csv), малый первичный synchronization artifact, revision отсутствует. Доступ 2026-10-23; HTTP 200, 2466 bytes; SHA256 **60e156223725e401155b4fd25a672c498ed5b4e17897337c6971d90041818bcc**. Локатор: все 160 строк, столбцы frame/time/accelerometer, смысл по S255. Собственная read-only проверка CSV, без медиадекодирования. Сохранён `urfd_fall01.csv`; вычисленные границы в `observations.json`. Acceleration не подаётся как RGB-признак и не считается event label.


## S258 — fall-01-cam0.mp4 (W2-D-S04)

- Provenance: [W2-D](_WORK/W2_D.md); исходная карточка `W2-D-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4>; <https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4>.

- F-связи: F175, F176, F177.


**S258.** Exact URFD asset metadata: [fall-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4) и [adl-01-cam0.mp4](https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4). Собственный HEAD 2026-10-23: оба 200 `video/mp4`, Content-Length соответственно **1,299,104 / 1,194,846 bytes**, Last-Modified 2020-02-25 17:13:37 / 17:13:38 GMT. Header metadata сохранено, full-byte SHA и decode отсутствуют. Дата mtime файла — не дата записи инцидента. MP4 являются удобными кандидатами; original PNG+CSV предпочтительны, если MP4 не сохраняет соответствие исходному времени. У всех производных одной sequence один parent incident group.


## S259 — Publisher model card (W2-E-S01)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1824797e7887cbec1990e4adbd6675960a36c589`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/blob/1824797e7887cbec1990e4adbd6675960a36c589/README.md>.

- F-связи: F182.


| **S259** | [Publisher model card](https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/blob/1824797e7887cbec1990e4adbd6675960a36c589/README.md), HF revision выше; YAML license, Model Details, Recipe details, Model Usage | Официальное model-level обозначение Apache, lineage/input/stats, не target result. Raw сохранён `hf_README.md`; web pinned raw отказал, HTTPS resolve отдельно успешно прочитан |


## S260 — HF API model metadata (W2-E-S02)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://huggingface.co/api/models/timm/mobilenetv3_small_100.lamb_in1k?blobs=true>.

- F-связи: F182.


| **S260** | [HF API model metadata](https://huggingface.co/api/models/timm/mobilenetv3_small_100.lamb_in1k?blobs=true), `sha`, `lastModified`, `siblings/model.safetensors/lfs`; pinned asset URL в карточке | Read-only JSON + HEAD; `hf_metadata.json`, `weights_HEAD.json`. API live, payload SHA закреплён. HTTP200/content type/size не доказывают содержимое/качество |


## S261 — Pinned config (W2-E-S03)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1824797e7887cbec1990e4adbd6675960a36c589`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/blob/1824797e7887cbec1990e4adbd6675960a36c589/config.json>.

- F-связи: F182, F183, F184, F185, F186, F187, F188.


| **S261** | [Pinned config](https://huggingface.co/timm/mobilenetv3_small_100.lamb_in1k/blob/1824797e7887cbec1990e4adbd6675960a36c589/config.json), весь586-byte JSON | `hf_config.json`: architecture/classes/normalization/geometry; не fitted target config |


## S262 — timm LICENSE (W2-E-S04)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/LICENSE>; <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/README.md#licenses>.

- F-связи: F182.


| **S262** | [timm LICENSE](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/LICENSE), §§2,4; [README Licenses](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/README.md#licenses), локальныеL739–748 | Code explicit grant и противоречивое weights notice. Не юридическое решение о любых pretrained weights |


## S263 — train.py (W2-E-S05)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/train.py>.

- F-связи: F185.


| **S263** | [train.py](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/train.py), L89–125 flags, L494–522 model create, L683–715 datasets, L879–910 loss | Конкретный official trainer и transfer API; native defaults не наши оптимальные hyperparams |


## S264 — builder load_pretrained (W2-E-S06)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/_builder.py>; <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/_helpers.py>; <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/mobilenetv3.py>.

- F-связи: F182, F185.


| **S264** | [builder load_pretrained](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/_builder.py), `load_pretrained` file/classifier branches; [helpers](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/_helpers.py), L62–65; [mobilenetv3](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/models/mobilenetv3.py), reset_classifier, forward, registry `small_100.lamb_in1k` | Статический load/head/architecture contract; не выполненный load |


## S265 — onnx_export.py (W2-E-S07)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/onnx_export.py>.

- F-связи: F185.


| **S265** | [onnx_export.py](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/onnx_export.py), CLI args, create_model и helper call | Native entrypoint; preprocessing не входит в graph |


## S266 — timm/utils/onnx.py (W2-E-S08)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/utils/onnx.py>.

- F-связи: F185.


| **S266** | [timm/utils/onnx.py](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/utils/onnx.py), L35–39 eval; L55–87 names/dynamic axes/export branch; L89–95 check | Обязательный dynamic batch и неявный Torch exporter default; source observation, не export failure |


## S267 — TSM shift (W2-E-S09)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/ops/temporal_shift.py>.

- F-связи: F182, F186.


| **S267** | [TSM shift](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/ops/temporal_shift.py), `TemporalShift.shift` L27–42 локального raw | Прямое future-read evidence; offline clip не равен online recurrence |


## S268 — Online TSM implementation (W2-E-S10)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/mobilenet_v2_tsm.py>.

- F-связи: F186.


| **S268** | [Online TSM implementation](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/mobilenet_v2_tsm.py), `InvertedResidualWithShift.forward` L93–96, `MobileNetV2.forward` L145–157 | Явные входы/выходы истории, причинность по source; не измерение target |


## S269 — Online TSM main (W2-E-S11)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/main.py>.

- F-связи: F186.


| **S269** | [Online TSM main](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/main.py), get_executor L76–99; main L286–316; process_output и history_logit | Jester27 file, state/export/runtime boundary, empty buffers; static negative finding. Ни checkpoint, ни demo не запускались |


## S270 — Online demo README (W2-E-S12)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `1f6a834b02120441d99fa706b7a13ccc5293c6fa`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/README.md>; <https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/LICENSE>.

- F-связи: F182, F186.


| **S270** | [Online demo README](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/online_demo/README.md), Overview/Supported Gestures; [MIT LICENSE](https://github.com/mit-han-lab/temporal-shift-module/blob/1f6a834b02120441d99fa706b7a13ccc5293c6fa/LICENSE) | Исторический Nano/TVM demo и code license; авторские FPS не цитируются как LinQ прогноз |


## S271 — timm pyproject (W2-E-S13)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/pyproject.toml>; <https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/data/transforms_factory.py>.

- F-связи: F182, F183, F184, F185, F186, F187, F188.


| **S271** | [timm pyproject](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/pyproject.toml), requires-python/dependencies; [transforms_factory](https://github.com/huggingface/pytorch-image-models/blob/78c3724f4545c0067d0b4d2f7df6337196be01ce/timm/data/transforms_factory.py), `transforms_imagenet_eval` | Ограничения dependencies и eval geometry, не installed lock |


## S272 — tag API (W2-E-S14)

- Provenance: [W2-E](_WORK/W2_E.md); исходная карточка `W2-E-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v1.0.22`, `78c3724f4545c0067d0b4d2f7df6337196be01ce`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://api.github.com/repos/huggingface/pytorch-image-models/git/ref/tags/v1.0.22>; <https://api.github.com/repos/huggingface/pytorch-image-models/commits/78c3724f4545c0067d0b4d2f7df6337196be01ce>.

- F-связи: F182, F183, F184, F185, F186, F187, F188.


| **S272** | [tag API](https://api.github.com/repos/huggingface/pytorch-image-models/git/ref/tags/v1.0.22), [commit API](https://api.github.com/repos/huggingface/pytorch-image-models/commits/78c3724f4545c0067d0b4d2f7df6337196be01ce), сохранены JSON | Источник точного SHA и commit date; не утверждение latest |


## S273 — Технологический стек (W2-F-S01)

- Provenance: [W2-F](_WORK/W2_F.md); исходная карточка `W2-F-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://lin-q.ru/tech>.

- F-связи: F189.


| **S273** | [Технологический стек](https://lin-q.ru/tech), live undated; `ПОДДЕРЖИВАЕМЫЕ СЕТИ`, web lines58–95; `СОБСТВЕННОЕ IP-ЯДРО` | Fresh web open + TinyFish full text. Vendor family-support/RNN claims; no exact graph or current SDK mapping. Сохранено primary_fetch |


## S274 — Framework manual IVA H1 (W2-F-S02)

- Provenance: [W2-F](_WORK/W2_F.md); исходная карточка `W2-F-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `04.06.014-03`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf>.

- F-связи: F189.


| **S274** | [Framework manual IVA H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf),2025 `RU.РМДВ.04.06.014-03 34 01`; pp5–7,10–13,17–24 | Fresh TinyFish full extract; historical example/tested-name evidence. PDF bytes/visual unavailable; flags/indent/name literals требуют сверки. Detailed paraphrase, не выдуманный runnable script |


## S275 — Документация (W2-F-S03)

- Provenance: [W2-F](_WORK/W2_F.md); исходная карточка `W2-F-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://lin-q.ru/docs>.

- F-связи: F189, F190, F191, F192, F193, F194, F195.


| **S275** | [Документация](https://lin-q.ru/docs), live undated; `Фреймворк → Руководство оператора. Фреймворк` и link list | Fresh TinyFish source/link provenance. Не package index и не обещание public SDK download |


## S276 — release v1.9.0 (W2-G-S01)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S01`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v1.9.0`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/releases/tag/v1.9.0>; <https://api.github.com/repos/vast-ai/vast-cli/releases/tags/v1.9.0>.

- F-связи: F196, F197.


| S276 | Vast.ai, [release v1.9.0](https://github.com/vast-ai/vast-cli/releases/tag/v1.9.0), [API metadata](https://api.github.com/repos/vast-ai/vast-cli/releases/tags/v1.9.0); published 2026-10-20, tag 28bde482… | release.json, wheel asset digest/size, tag identity; не запуск |


## S277 — official wheel asset (W2-G-S02)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S02`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `v1.9.0`, `1.9.0-py3-none-any.whl`, `28bde4827374ef658694db5a1e1e61508b966e2f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/releases/download/v1.9.0/vastai-1.9.0-py3-none-any.whl>; <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/main.py>.

- F-связи: F196, F197.


| S277 | Vast.ai, [official wheel asset](https://github.com/vast-ai/vast-cli/releases/download/v1.9.0/vastai-1.9.0-py3-none-any.whl), wheel METADATA/entry_points, [main.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/main.py), `main/run_command` | Реально скачанные bytes; статическое извлечение, не установка |


## S278 — CLI storage.py (W2-G-S03)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S03`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28bde4827374ef658694db5a1e1e61508b966e2f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/storage.py#L78>.

- F-связи: F196, F197, F198.


| S278 | [CLI storage.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/storage.py#L78), L78–128 | subprocess argv/no checked result, host-key option; wheel совпал с source |


## S279 — CLI instances.py (W2-G-S04)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S04`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28bde4827374ef658694db5a1e1e61508b966e2f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/instances.py>; <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/instances.py>.

- F-связи: F196, F197.


| S279 | [CLI instances.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/instances.py), L41–65,212–347,1054–1065; [API instances](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/instances.py), L31–91,309–339 | source control flow, не измерение transitions |


## S280 — CLI offers.py (W2-G-S05)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S05`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28bde4827374ef658694db5a1e1e61508b966e2f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/offers.py#L127>; <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/offers.py>.

- F-связи: F197, F200.


| S280 | [CLI offers.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/offers.py#L127), L22–33,127–200; [API offers](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/offers.py), L12–56 | CLI vs SDK default filters, storage units/endpoint |


## S281 — API storage.py (W2-G-S06)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S06`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28bde4827374ef658694db5a1e1e61508b966e2f`, `42c3a47b44603775a5e31f54de0fce3994bd3f11`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/storage.py#L53>; <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/utils.py#L87>; <https://api.github.com/repos/vast-ai/vast-cli/compare/28bde4827374ef658694db5a1e1e61508b966e2f...42c3a47b44603775a5e31f54de0fce3994bd3f11>.

- F-связи: F197, F198.


| S281 | [API storage.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/storage.py#L53), L53–67; [utils](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/utils.py#L87), L87–119; [compare](https://api.github.com/repos/vast-ai/vast-cli/compare/28bde4827374ef658694db5a1e1e61508b966e2f...42c3a47b44603775a5e31f54de0fce3994bd3f11) | URI parsing/dispatch and release vs HEAD; no server copy test |


## S282 — Current Billing (W2-G-S07)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S07`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/reference/billing>.

- F-связи: F196, F199, F200.


| S282 | [Current Billing](https://docs.vast.ai/guides/reference/billing), Pricing L191–196, Transactions L266–278, Loading L339–341 | current policy/units; actual invoice unknown |


## S283 — Current FAQ Billing (W2-G-S08)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S08`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/reference/faq/billing>.

- F-связи: F199, F200.


| S283 | [Current FAQ Billing](https://docs.vast.ai/guides/reference/faq/billing), Pricing L123–128, Billing L107–116 | Новое explicit loading storage + offline exclusion; contradiction сохранён |


## S284 — Legacy FAQ (W2-G-S09)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S09`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://console.vast.ai/faq/>.

- F-связи: F199.


| S284 | [Legacy FAQ](https://console.vast.ai/faq/), Billing→Pricing L255–257 | competing offline policy, дата публикации не установлена |


## S285 — Managing Instances (W2-G-S10)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S10`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/manage-instances>.

- F-связи: F196, F199.


| S285 | [Managing Instances](https://docs.vast.ai/guides/instances/manage-instances), Operations/Restart/Loading/Expiration L217–238,287–303,338–347 | lifecycle policy, отсутствие гарантии рестарта/48h preservation |


## S286 — Show Charges (W2-G-S11)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S11`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/api-reference/billing/show-charges>; <https://docs.vast.ai/api-reference/openapi/yaml/show_charges.yaml>.

- F-связи: F198, F199.


| S286 | [Show Charges](https://docs.vast.ai/api-reference/billing/show-charges), [OpenAPI YAML](https://docs.vast.ai/api-reference/openapi/yaml/show_charges.yaml), info.version1.0.0; YAML L108–179 | typed items enum/source/rounded amount; не actual account charges |


## S287 — Show Invoices (W2-G-S12)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S12`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/api-reference/billing/show-invoices>; <https://docs.vast.ai/api-reference/openapi/yaml/show_invoices.yaml>.

- F-связи: F198, F200.


| S287 | [Show Invoices](https://docs.vast.ai/api-reference/billing/show-invoices), [YAML](https://docs.vast.ai/api-reference/openapi/yaml/show_invoices.yaml), route/query/schema | Payments vs usage, UTC filter/pagination; no account access |


## S288 — CLI billing.py (W2-G-S13)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S13`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: `28bde4827374ef658694db5a1e1e61508b966e2f`. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/billing.py>; <https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/billing.py#L66>.

- F-связи: F198, F199.


| S288 | [CLI billing.py](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/cli/commands/billing.py), L346–438; [API billing](https://github.com/vast-ai/vast-cli/blob/28bde4827374ef658694db5a1e1e61508b966e2f/vastai/api/billing.py#L66), L66–167 | Exact date flags/raw pagination/endpoint/cap; не выполнен |


## S289 — Data Movement (W2-G-S14)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S14`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/data-movement>.

- F-связи: F198.


| S289 | [Data Movement](https://docs.vast.ai/guides/instances/storage/data-movement), CLI Copy, trailing slash paragraph, SCP, VM Constraints | Transports и ограничения; отдельный VM-only constraints не переносится на Docker |


## S290 — Storage Types (W2-G-S15)

- Provenance: [W2-G](_WORK/W2_G.md); исходная карточка `W2-G-S15`. Доступ: **2026-10-23**.

- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.

- Версия/commit/tag: **unknown / live undated**, если карточка не устанавливает иной идентификатор. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.

- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.

- URL: <https://docs.vast.ai/guides/instances/storage/types>.

- F-связи: F199.


| S290 | [Storage Types](https://docs.vast.ai/guides/instances/storage/types), Characteristics/Limitations/Costs L129–197 | charged allocation, separate local volumes, possible higher stopped rate |

