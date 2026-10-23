# Common researcher brief — cv_accuracy_vast
You are an independent internet researcher, gpt-6.1-sol medium, explicitly assigned through the agent tool. Read the assigned prompt completely. You may read Context-prompt.md and prompt_cv_accuracy_vast_research.md if needed. Team: five strong engineers, industrial-safety video analytics hackathon, after first checkpoint on 2026-10-23. Final neural inference MUST run on LinQ, reported server has CPU+TPU (team report, exact configuration unknown). Vast.ai 1–2 RTX 3090 24GB are only contemplated for training, no rental or spending authorized. Experts emphasized accuracy verbally; this is not an official formula and does not remove latency constraints. Case pages 5,7,13 require balanced quality, few-second alert latency, deduplication, LinQ inference with speed measurement; priority scenarios may be selected. No local training, export, benchmark or hardware execution has been performed. Do not fabricate these.
Use real internet tools (discover with ALL_TOOLS where needed), search and OPEN primary docs/papers/code; do not rely on snippets or only previous summaries. Record source URL, author, publication/version vs access date, precise locator, evidence kind, conditions, limitations. Current host date should be recorded honestly. Repository versions/commits and weights licenses must be pinned when material. A live docs page without version is not a pinned recipe. Distinguish published claims/measurements from your own observations and recommendations. No verbatim copying of sources: preserve concise paraphrases and locators respecting source word limits. Do not download large model weights or datasets. No credentials, account changes, payments, external messages, or changes outside your own assigned _WORK files. You may expand strong leads relevant to the decision. Do not spawn agents; root coordinates.
Protect split independence: train/validation/optional SELECT/lockbox, no neighboring frames or identical scenes/cameras across independence claim, no threshold/checkpoint/ensemble tuning on lockbox. A stated procedure is not a performed experiment. No invented prices, VRAM fit, runtimes, accuracy or success probabilities. Keep camera calibration, LinQ quantization, and exhaustive behavioral weights/datasets as handoffs to neighboring research.
Your completion condition is a useful substantiated decision with alternatives, failure conditions, a proposed discriminating experiment and clearly bounded unknowns; no arbitrary link quota. Write detailed Russian research with exact English literals as needed. Include: decision-first findings; technical detail; candidate/recipe/protocol comparisons where relevant; evidence records with branch-local S/F IDs; contradictions/negative findings; experiment question, inputs, procedure, metrics, artifacts, outcomes, what success does not prove; handoffs and precise open questions. Save detailed work to your assigned path. In final response give brief findings, consequences, source versions, proposed experiment, resource prerequisites without invented estimates, leakage risks, cross-cell handoffs, and file path.
Available previous reports are in sibling topic folders (datasets, evaluation, training_strategy, research_link_platform, violation_methods, video_architecture, operator_product, hackathon_strategy, market_deployment, LinQ-case-analytics-research); existence is not proof of completeness. Use as leads, verify primary evidence anew. Official raster case: ../LinQ-case-analytics-research/КЕЙС_LinQ.pdf. Root visually read all 20 pages via existing sheets. See _WORK/CASE_NOTES.md.


# Second-wave requirements
Your exact W2 assignment and linked K IDs will follow. Read CRITIC.md and the specified W1 evidence fully enough to understand the gap. Do not repeat a general survey; obtain NEW primary evidence or actively seek limiting/counterexamples. Answer the concrete missing question and identify the decision changed. Explicitly report whether each K is closed, applicability clarified, contradicted, still open, or moot. Preserve the original criticism; never rewrite history. No need to force closure of device/account/target-data questions with public search. Save your own detailed W2 file and any concise primary material under your own directory. Branch-local IDs W2-xx-S/F, source/date/version/access/locator/provenance/conditions, proposed experiments vs actual observations, handoffs. No spending, training/export/device runs, account mutation or subagents. Practical examples must be documented and unexecuted unless explicitly observed read-only metadata.

# Assignment W2-D: Minimal data and causal acceptance corpus
Exclusive output: _WORK/W2_D.md. Branch IDs W2-D-Sxx/Fxx.

## Exact task
Read sibling datasets/behavioral report leads as secondary, recheck only 1–2 primary data sources that can support a first scenario, not full catalog. Separate object fine-tune inputs from event evaluation; rights, labels, group/incident/camera lineage, native timestamps/FPS, negatives, missing team assets. Choose a conditional initial scope and minimum annotation plan. Specify small synthetic event-ledger truth table: timely/late/duplicate/two actors/rearm/ID split-merge/unknown gap/short event between samples/EOF censoring; synthetic fixtures do not prove detector quality. Provide compact real development corpus readiness and phase replay plan. Do not force hundreds of events before feasibility or invent private data.

## Existing evidence
_WORK/W1_01.md, _WORK/W1_04.md, _WORK/W1_07.md, _WORK/W1_09.md, _WORK/W1_11.md; CRITIC.md; _WORK/CASE_NOTES.md.

## Original criticism (preserve provenance)
### K005 — Не определён минимальный реально доступный data package, поэтому training queue пока не имеет входа

**Приоритет / тип:** P0; общий недостающий prerequisite, не поручение повторить datasets research.

**Материал и доказательство.** W1-06/07/08 требуют union ontology, полные labels/replay и independent groups; W1-01/04/09 — непрерывные negatives, event onset и source timestamps. Но во всех этих планах они фигурируют как «нужны», без единого выбранного сейчас asset/manifest. `CASE_NOTES.md` p8 разрешает выбрать video/image sets, а не подтверждает выдачу достаточной размеченной выборки. `NEIGHBOR_LEADS.md` лишь перечисляет существование соседних reports, не переносит проверенный data package.

**Последствие.** Даже идеально организованные 3090 не выполнят baseline, которому одновременно нужны несогласованные object/event/ownership labels и replay. Программа может незаметно сменить основной сценарий на PPE, хотя официальные примеры включают действия/взаимодействия; статичная COCO-head не создаёт их GT.

**Точно недостающее доказательство.** Для одного начального сценария: какие конкретные разрешённые assets доступны/получаемы, что в них размечено, camera/incident lineage, native temporal resolution, continuous negative exposure, полнота нужных classes; какая часть требует людей и не обещана публичным архивом. Разделить object fine-tune package и end-to-end event evaluation package. Не обязательно найти идеальный заводской benchmark: допустим честно более узкий feasibility dataset.

**Задание второй волны / закрытие.** W2-D начать с адресных соседних findings и заново проверить только 1–2 первичных data sources, которые могут обеспечить первый опыт; без полного каталога поведенческих весов. Выдать readiness matrix для `зона/длительное состояние`, `падение/лежание` либо другой обоснованной пары, предложить один приоритет и минимальную доразметку. `нет independent background/positives` должно приводить к feasibility claim и ограничению scope, а не к выдуманной FP/hour. Файлы команды/частные видео, если недоступны роли, остаются Q с владельцем; интернет не заменяет их инвентаризацию.



### K006 — Роли SELECT/CAL/TUNE/CHECK расходятся между ветками

**Приоритет / тип:** P1; реальная интеграционная несогласованность корректных по отдельности альтернатив.

**Материал и доказательство.** W1-02, эксперимент шаг5, допускает выбор на SELECT семейства/input/crop/**порога/temporal rule**. W1-11-F10, пункт3, требует фиксировать пороги на DEV и на SELECT выбирать готовый pipeline. W1-09 вводит CAL/TUNE/CHECK внутри development и отдельно предупреждает, что SELECT, уже потраченный на model selection, нельзя повторно считать независимым CHECK. W1-03/07/08 по-разному называют групповые уровни. Эти варианты нельзя просто сложить в один обязательный конвейер из семи микроскопических subsets.

**Последствие.** Один и тот же SELECT может несколько раз обслужить выбор recipe, threshold, calibrator и затем ещё получить ярлык подтверждения. Либо команда потратит редкие независимые события на чрезмерное дробление и совсем не сможет оценить выбранный сценарий.

**Точно недостающее доказательство/решение.** Единый assignment table `decision → allowed data role → number of finalists/trials → after-view status`, привязанный к фактическому числу групп K005. Явно выбрать один протокол, а не утверждать, что только один из W1-вариантов научно допустим.

**Закрытие.** Это преимущественно **сборка**, а не новая обзорная интернет-задача. W2-D предоставляет реальные group/label constraints; сборщик выбирает минимальный train/DEV/lockbox вариант, optional SELECT и optional calibration только при достаточных группах. На frozen SELECT можно выбирать только заранее подготовленные целые pipelines; если там настраиваются параметры, он становится tuning data и следующий CHECK не может быть той же группой. После refit artifact получает новую identity и соответствующий статус независимой проверки. Сохранить общую политику lockbox W1 без повторного поиска leakage papers.



### K007 — Нужен один минимальный causal event acceptance corpus, а не сумма всех стресс-матриц

**Приоритет / тип:** P1; недостающий проверочный вход к уже хорошей спецификации.

**Материал и доказательство.** W1-01/04/05/09 содержат подробные event/phase/gap/owner/dedup tests. Все они пока проекты; нет единого короткого списка, на котором можно сначала доказать правильность semantics и timestamps, до расширенного model search. W1-04-F06 описывает вероятность хотя бы одного идеального sample; она намеренно не доказывает наличие нескольких различающих observations до deadline. Duration distribution приоритетных реальных действий остаётся неизвестна.

**Последствие.** Можно корректно считать mAP и настроить persistence, но так и не проверить, не превращает ли несколько секунд подтверждения пересечение/падение в FN и не глушит ли cooldown второго человека. Сотни подробных stress variations ещё не образуют приоритетную начальную проверку.

**Точно недостающее доказательство.** Для выбранного scope: короткий набор реальных development episodes с PTS/onset/observable/end и negatives; отдельно малая synthetic event-ledger truth table для самого evaluator/FSM. Обязательные различения: late vs timely, дубль продолжающегося эпизода, два разных участника, rearm, ID split/merge, unknown gap, короткое событие между samples, end-of-file censoring. Synthetic ledger не подтверждает detector quality.

**Задание второй волны / закрытие.** W2-D вместе с data readiness выдать компактный acceptance fixture specification и фазовый replay план на исходной временной сетке. Подтвердить доступные durations/timestamps первичным dataset metadata/annotation manual либо оставить их измерению; не придумывать универсальный min FPS. W2-A/W2-F добавляют только необходимые runtime traces. Сборщик фиксирует matcher/tie policy из W1-01 и сохраняет ограниченный первый набор: cache replay проверяет логику, отдельный LinQ wall-clock run — deadline. Собственный capture/recall/latency остаётся unknown до практической проверки.



### K011 — Нет единого маршрута на оставшееся окно и дешёвого режима при незакрытых gates

**Приоритет / тип:** P0/P1; интеграционный пробел программы, а не отсутствие законных вымышленных GPU-hours.

**Материал и доказательство.** W1-11 ограничивает очередь B0→до двух ablations→один challenger→confirmation; W1-15 правильно задаёт DAG одной/двух GPU. Но сумма отдельных W1 экспериментов (pose, trackers, data selection, augmentation, calibration, specialists, DDP, recovery controller) намного шире этой очереди. Нет одного выбранного первого сценария/recipe, owner allocation пяти людей, общего freeze point относительно checkpoint 24.10 11:00/18:00 и сдачи 25.10 10:00, а также stop condition по человеку/разметке/SDK. На контрольное время критика до сдачи оставалось примерно **37 ч 35 мин**, не исходные 45 ч от публикации задания. Это арифметика расписания `CASE_NOTES.md`, не оценка длительности training.

**Последствие.** Можно потратить доступное окно на сборку контейнера, строгий exact-resume adapter, controller/generation protocol и сложный nested evaluation, не получив один полный работающий сценарий. Также возникает круг «до аренды измерить 3090 fit» при ещё не имеющейся 3090. Локальная RTX 4070 есть по контексту, но её VRAM/окружение не установлены; она не доказывает 24GB fit. Вторая GPU не решает этот круг.

**Точно недостающее решение.** Один minimal route с ветвями: (A) pretrained + CPU rules/threshold replay без нового обучения; (B) один fine-tune после data/runtime gates; (C) optional challenger/вторая GPU только при готовой очереди и измеренном reserve. До первой аренды проверяются доступные без GPU документальные/данные/экспортные условия; qualification smoke на конкретной 3090 — отдельная первая оплачиваемая стадия после самостоятельного разрешения, не уже имеющийся предарендный факт. Нужен заранее заданный cutoff новых гипотез и относительный резерв LinQ/финальных материалов без выдумывания часов.

**Закрытие.** Новая отдельная интернет-ветка «как планировать GPU» не нужна: W1-11/15 уже дали сильную базу. После W2-A…G сборщик/автор сводит один маршрут и список deferred работ. Минимальная сохранность — native recovery snapshot до stripping, immutable copy, внешние bytes/hash/load и записанный parent/status; строгий replay/controller предлагается только при доказанной потребности. K001 определяет, какие автоматические изменения должны аннулировать сравнение. Прохождение одного smoke не отменяет отдельный worst-case train/val memory gate. Не разрешать optional runs съесть обязательные evaluation/LinQ/submission reserves.

