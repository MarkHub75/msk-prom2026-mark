# Состояние исследования training_strategy

> Актуальное состояние возобновления: обе волны (15+12) и свежий критик завершены; сборщик завершил четыре доказательных файла и ID mapping. COMPLETE: все согласованные этапы завершены, шесть итоговых файлов сохранены в корне темы. MACHINE_COMPRESSOR завершён; дополнительная проверочная роль не создавалась. Подробный финальный статус — в конце журнала. Записи ниже о первой волне «выполняется» относятся к прерванному запуску; последующий журнал содержит фактические завершения. Новая сеть после W2 не выполняется.
Начало: 2026-10-23T05:58:50+03:00 (фактические часы среды). Даты соревнования — контекст входного задания, не результат новой проверки расписания.

Входы Context-prompt.md и prompt-training-strategy.md прочитаны целиком. Текущая папка — итоговая папка темы; входы сохраняются. Соседних отчётов в ней нет.

## Роли и среда

- Доступен настоящий spawn_agent с model, reasoning_effort и fork_turns. Одновременно доступны корень и три дочерних агента; логические задачи выполняются очередями.
- Назначаем gpt-6.1-sol/medium для сетевых исследователей и gpt-6.1-sol/high для критика, сборщика, автора, редактора, сжимателя; fork_turns=none даёт независимый контекст.
- Оркестратор — текущая сессия; её модель и effort не переключаются доступным инструментом. Пользовательские глобальные настройки не меняются. Явно назначаемые профили дочерних ролей фиксируются в запусках.
- Доступны web search/open и PowerShell/Python для служебных файлов. Большие training/benchmark, аренда и генерация данных не выполняются.
- Пользователь требует unattended run. Вопросы и ожидание ответа исключены. Неизвестные данные, конфигурация RTX 4070 и LinQ не выдумываются.

## Принятые решения

1. Первая волна: 15 самостоятельных ячеек по тематическому заданию; три одновременно. Каждая сохраняет отдельный результат и подробные основания.
2. Критик получает входные задания, карту и результаты без истории оркестратора. Вторую волну определит критика.
3. Все новые сетевые материалы получают только Medium-исследователи. High-роли работают с сохранённой базой.
4. Ровно шесть итоговых Markdown-файлов в корне. Служебные задания, выписки и черновики — _WORK.
5. Отдельной финальной проверочной роли/волны не будет; точность и согласованность обеспечиваются сборщиком, редактором и сжимателем в их работе.

## Исторический этап до прерывания

Планирование завершено; первая волна идёт. Индивидуальные задания: AGENT_PROMPTS.md; карта: PLAN.md.

## Журнал запусков

| Агент | Задача | Фактически назначено | Контекст | Результат/статус |
|---|---|---|---|---|
| w1_01 | baseline, выбор стратегии | gpt-6.1-sol / medium | none + входы и индивидуальное задание | _WORK/W1/01_BASELINE.md, выполняется |
| w1_02 | transfer, freeze/full fine-tuning | gpt-6.1-sol / medium | none + входы и индивидуальное задание | _WORK/W1/02_FINETUNING.md, выполняется |
| w1_03 | few-shot, partial labels | gpt-6.1-sol / medium | none + входы и индивидуальное задание | _WORK/W1/03_FEWSHOT_PARTIAL.md, выполняется |

## Ранние находки (ещё до сборки, branch evidence)

- W1-01: target dataset и параметры val/predict должны быть заданы явно; геометрия padding и postprocessing способны изменить baseline без обучения. Подробные основания будут в 01_BASELINE.md.
- W1-02: проверяется Ultralytics commit e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8, версия 8.4.184. Trainer управляет requires_grad и режимом BN; перенос class head может зависеть от names. Это требует версии в каждом эксперименте, а не универсального совета freeze.
- W1-03: K-shot в TFA относится к экземплярам класса, не независимым кадрам. Federated Loss не универсальный механизм обработки пропусков объектов; некоторые sparse-label методы меняют и inference. Вторая волна должна проверять границы применимости, а не только наличие метода.

## Возобновление 2026-10-23

Фактическое время возобновления по часам PowerShell: 2026-10-23T06:40+03:00. Оба входа перечитаны; исходные PLAN.md и AGENT_PROMPTS.md используются без повторного планирования. На диске из результатов первой волны есть только завершённый W1/01_BASELINE.md (34137 bytes); его повторный запуск не нужен. Старые записи «выполняется» для 02/03 не означают сохранённого результата или живого агента. Запущены новые независимые W1-02, W1-03, W1-04, gpt-6.1-sol/medium, fork_turns=none. Роли и модель назначены реальными параметрами collaboration.spawn_agent; одновременно три исследователя. Свежий критик и авторские роли будут назначены после завершения соответствующих входов. AGENTS.md в папке темы и вышележащем каталоге проекта не найден. Вопросов пользователю не будет.

### Первая группа после возобновления

W1-02, W1-03, W1-04 завершены реальными агентами gpt-6.1-sol/medium (fork_turns=none). Сохранены 02_FINETUNING.md, 03_FEWSHOT_PARTIAL.md, 04_IMBALANCE.md. Результаты не являются выполненными training/benchmark. Важные находки: freeze затрагивает BN и trainer может отменять ручную freeze; TFA shot=instance и variance annotation sample не то же самое, что optimizer seed; FedLoss не универсален для missing boxes; SparseDet меняет inference; Ultralytics 8.4.184 имеет cls_pw (нельзя переносить прежний вывод об отсутствии weighting), RFS и weights используют разные частоты. Запущены W1-05/06/07, те же фактические medium/none настройки. Для последующих независимых High-ролей сохранены полные задания ROLE_PROMPTS.md. План и завершённая W1-01 сохранены.

### Следующая группа

W1-05 (аугментации) и W1-06 (масштаб/crops) завершены; собственные файлы в W1. W1-07 продолжает primary evidence domain adaptation. Запущены W1-08 и W1-09 (medium/none). W1-05 установил различие bbox-only/segments для copy_paste, classification-only erasing, версионный разрыв API Albumentations; W1-06 сохраняет AP50 (не AP50:95) и неразрешённое abstract/table расхождение SAHI. Никаких фактических target training/inference результатов нет.

### Первая волна, 07–12

W1-07/08/09 завершены (DOMAIN, ACTIVE, PSEUDO); W1-10 продолжает проверку actual KD implementation; W1-11 и W1-12 запущены gpt-6.1-sol/medium, fork_turns=none. Установлены ограничения transductive domain adaptation, negative transfer и несовпадения paper/config; active selection сравнивается по человеческому времени и независимым сценам; EMA teacher AP не равно student AP, pseudo confidence не подтверждает локализацию/полноту. Существенный новый след W1-10: актуальный Ultralytics содержит distill_model/DistillationModel, поэтому старое общее отрицание штатной KD неверно; конкретные support boundaries ещё проверяются. Все новые ветки читают полностью оба контракта и индивидуальные сохранённые промпты. Сборка не начиналась, критик ждёт все 15 W1.

### Первая волна, финальная группа

W1-10/11/12 завершены. Ветка teacher проверила действительную KD Ultralytics8.4.184 (не отсутствие), same-family/task/feature boundaries и извлечение student; synthetic — отрицательные real+synth результаты и partial-label эффект фильтрации; optimization — actual auto optimizer/warmup/EMA/resume и ограничения tiny runs. Запущены W1-13/14/15, все gpt-6.1-sol/medium, fork_turns=none. Один вызов spawn W1-13 получил thread limit, пока W1-10 ещё завершал передачу; после фактического завершения W1-10 повторный spawn успешен. Это ограничение параллельности, не дополнительный исследовательский запуск. Исследование остаётся первой волной до получения 13/14/15. Все законченные W1 сохранены, baseline не изменялась.

## Переход к свежему критику

Первая волна завершена: все 15 самостоятельных ячеек W1/01…15 существуют. W1-01 переиспользована из прерванного запуска; W1-02…15 реально выполнены в возобновлении отдельными gpt-6.1-sol/medium, fork_turns=none, с primary search/open. W1-13 нашёл только публичные manufacturer claims LinQ, не SDK contract. W1-14 разделяет DDP/trials/annotation cost и не выдумывает GPU timing; W1-15 выявил Metric.maps fallback absent class и отделил sample_seed/optimization_seed/split. Сетевых/практических результатов с целевой моделью нет.

Запущен отдельный critic gpt-6.1-sol/high, fork_turns=none. Переданы только оба входа, карта, ROLE_PROMPTS и все 15 файлов W1, без разговорной истории и обязательной предварительной позиции. Его выходы CRITIC.md и _WORK/W2_TASKS.md. Новую сеть критик не получает, задания второго этапа определит по конкретным gaps. Отдельного финального аудитора не будет.

## Вторая волна

Свежий critic завершён: CRITIC.md содержит K001–K012; _WORK/W2_TASKS.md — полный общий блок и 12 индивидуальных заданий. Он самостоятельно признал покрытие W1 достаточным и выделил конкретные implementation gaps, без нового поиска. Приоритеты/файлы — в CRITIC. Принята содержательная вторая волна из12 задач. W2-12 (bounded queue/fidelity) последняя и использует уже полученные W2, оставаясь второй волной, а не новым аудитом.

Запущены W2-01/02/03, все gpt-6.1-sol/medium, fork_turns=none. Первичные новые evidence получают только они. Их владение: W2/01_NATIVE_KD_CONTRACT.md, 02_PARTIAL_ASSIGNMENT.md, 03_ONESTAGE_SSL.md. Последующие группы будут запускаться после освобождения реальных слотов. Все будущие авторские роли остаются отдельными high/none и работают с сохранённой базой.

### W2 первые результаты

W2-01 и W2-02 завершены. K001 получил package artifact proof (8.4.184 wheel, key files byte-equal U), concrete docs/code YOLO11n←11s contract, но runtime/target gain/LinQ не проверены. Уточнение checkpoint: EMA уже teacher-free, projectors остаются до final unwrap. K002 закрыт implementation trace: hidden objects negative BCE, legacy objectness, e2e обе branches; MMD ignore default/zero-GT ограничение. Практическое hidden-GT/gradient исполнение по-прежнему future E. Запущены W2-04 (K004) и приоритетная W2-11 (K011), gpt-6.1-sol/medium/none. W2-03 ещё работает. Порядок после первой тройки изменён по P0 ценности; coverage12 сохраняется.

### W2: implementation contracts 03/04/11

W2-03/04/11 завершены отдельными medium/none агентами. K003: конкретные UTv2/YOLOv5 EfficientTeacher routes, uncertainty branch/eval teacher/EMA/export различия; не современный generic U integration. K004: фактический Results detect scalar conf/cls, probs=None; native low-confidence acquisition без extra forward доступен, польза неизвестна. K011: exact callback/save lifecycle; immutable candidates через on_model_save; до strip тоже нет online/RNG/loader/scheduler полного состояния; freeze разрешён при resume, отдельная новая стадия resume=False. Противоречия с общими формулировками W1 сохранены для collector, не переписаны задним числом. Работают W2-06/05/08, назначены medium/none. Следующие09/07/10; затем12 на всех доступных итогах.

### W2: 05/06/08

W2-05 завершена: public teacher audit/calibration gap закрыт; no-detection misses требуют полных labels, probability component отдельно targeted diagnostics, no invented acceptance/sample floors. W2-06 завершена: detector/backbone/representation pretraining отличия, версионные исправления few-shot DETReg и recipe confounds. W2-08 завершена: author Gen2Det implementation не найдена после содержательных primary traces; K008 уточнён paper-level supervision/exposure terms, author-artifact gap открыт. Это не доказательство отсутствия кода. Работают W2-09,07,10 (medium/none). После них запустить W2-12 на всех11 результатах, затем collector high/none. Третьей поисковой волны не будет.

### W2-07/09/10 → последняя задача12

Одиннадцать профильных W2 задач завершены. W2-07 нашёл author simple-SFOD и фактические BN updates в eval-only/selection/source-weight gaps. W2-09 нашёл detector-specific NVIDIA YOLOv7 QDQ export route, но actual finetune loss feature MSE и неполный dependency lock; LinQ arithmetic match открыт. W2-10 нашёл физическое dense pruning DepGraph, старый U8.0.90 и C2f_v2/patched serialization; speed up label — MAC ratio, не latency. Все actual training/export/surgery не выполнены.

Запущен W2-12 gpt-6.1-sol/medium/fork_turns=none на всех11 завершённых W2 и банке W1 E. Цель — ограниченная dependency-aware очередь для8 сценариев, не третья волна и не финальный аудит. После неё только согласованные collector→author→editor→machine compressor High-роли, без новой поисковой волны. Остатки unknowns фиксируются открыто.

## Вторая волна завершена → сборщик

W2-12 завершена: reused G0–G4 gates, восемь сценариев/один следующий discriminating trial, mapping банка E в alternatives, kill/promote/rollback и critical path useful artifact; первичные Hyperband/ASHA не дают обещания раннего detector ranking. Все12 W2 (K001–K012) реально выполнены gpt-6.1-sol/medium/fork_turns=none. Новые сети после второй волны запрещены; остатки будут вопросами.

Запущен отдельный collector gpt-6.1-sol/high/fork_turns=none. Переданы оба контракта, роли, карта/состояние, исходная критика и27 завершённых исследовательских файлов. Владение: SOURCES.md RAW_FACTS.md OPEN_QUESTIONS.md, дополнение outcomes CRITIC.md; служебные ID_MAP.md и AUTHOR_HANDOFF.md. Большая подробная база с устойчивыми IDs и происхождением, не короткий пересказ. Затем отдельные author→editor→machine compressor. Фактические training/benchmark/export/LinQ execution не выполнялись.

### Прогресс сборщика

Collector сообщил о полном чтении всех15 W1 и12 W2 (усечённые диапазоны дочитаны), переходит к записи нормализованной базы без сети. Source duplicates сводятся по immutable artifact/revision, branch provenance сохраняется; W2 amendments объединяются с исходными E, W2-12 задаёт банк альтернатив. K008 author-code gap остаётся открытым, а source-free/QAT/pruning не объявляются runnable/target-verified. Автор ещё не запущен: необходимо завершить доказательные файлы.

## Сборка завершена → автор

Collector завершён (gpt-6.1-sol/high/none), внутри роли проверил ID/path/anchors/UTF-8 без ошибок. Созданы SOURCES.md (220S), RAW_FACTS.md (284F,51E), OPEN_QUESTIONS.md (31Q с условиями154branchQ); CRITIC.md сохраняет исходную критику и12 outcomes. _WORK/ID_MAP.md, AUTHOR_HANDOFF.md и воспроизводимый COLLECTOR_BUILD.py сохранены. K002/004/005/006/011/012 закрыты public/methodical; K001/003/007/009/010 уточнены; K008 author-code gap открыт. Actual target training/export/runtime не выполнены.

Запущен отдельный author gpt-6.1-sol/high/fork_turns=none. Полные входы и роль, собранная база и навигация переданы; единственный выход _WORK/AUTHOR_DRAFT.md. Он пишет законченный русский текст с условиями/доказательствами/очередью8сценариев, без новой сети. После него отдельный editor, затем machine compressor; дополнительной финальной роли не будет.


## Автор завершён → редактор

Отдельный AUTHOR high/none завершил _WORK/AUTHOR_DRAFT.md (152573 UTF-8 bytes;31 содержательный заголовок). Покрыты15решений/8сценариев, будущие процедуры, checkpoint lifecycle/LinQ gates/адресные передачи; E-bank как alternatives и одно следующее discriminating comparison. Все W2 corrections сохранены. Внутри авторской роли проверены links/anchors/noTODO/no replacement chars; изменён только черновик. Его ../ ссылки верны для _WORK, финальныйhuman требует переноса в корень.

Запущен отдельный editor gpt-6.1-sol/high/fork_turns=none: литературная редактура и report_human_training_strategy.md, служебные EDITOR_NOTES.md; явное указание убрать ../ из внутренних ссылок при переносе. Нового technical audit/поиска нет. Затем отдельный machine compressor и завершение, без новой проверочной роли.

## Редактор завершён → машинный сжиматель

EDITOR high/none завершил report_human_training_strategy.md в корне и _WORK/EDITOR_NOTES.md. Улучшены связность/русский синтаксис/сценарии/процедуры; сохранены15решений/8сценариев, W2 corrections, literals/URLs/IDs. Внутри роли все280локальныхссылок разрешаются. Доказательные файлы не менялись, новых technical conclusions/поиска нет.

Запущен отдельный machine_compressor gpt-6.1-sol/high/fork_turns=none, финальная согласованная роль. Он получает окончательный human и базу/навигацию, пишет report_machine_training_strategy.md на английском и _WORK/COMPRESSOR_NOTES.md. YAML/answers/schema/local links/IDs проверяет внутри своей writing role; нового аудитора после него нет. После передачи обновить состояние COMPLETE и дать короткое русское финальное сообщение. Training/benchmark/export/LinQ execution не выполнены.

### Прогресс последней роли

Machine compressor сообщил, что report_machine_training_strategy.md уже сохранён в корне:15ответов/implementation contracts/ограничения. Дописывает8сценариев, навигацию E-bank и передачи; собственные YAML/link/ID/coverage checks ещё идут. Это незавершённая последняя writing role, не отдельная проверочная стадия. Не считать весь запуск COMPLETE до передачи compressor.

## COMPLETE — 2026-10-23T09:44:17.6979469+03:00

Задание завершено автономно. Сохранённый план/индивидуальные промпты и W1-01 переиспользованы; первая волна15ячеек завершена (14новых medium/none запусков в возобновлении), отдельный fresh-context critic high/none, вторая волна12medium/none задач, отдельные collector→author→editor→machine compressor high/none выполнены последовательно. Модель дочерних ролей gpt-6.1-sol реально назначалась параметрами инструмента; ограничения управления моделью корневой сессии описаны в начале. Вопросы пользователю/ожидание его ответов отсутствовали.

Ровно шесть итоговых артефактов в текущей папке (два исходных промпта сохранены):
- SOURCES.md —220каноническихисточников.
- RAW_FACTS.md —284факта,51процедура будущей проверки.
- CRITIC.md —исходные K001–K012 и результаты второй волны, без финального аудита отчётов.
- OPEN_QUESTIONS.md —31сведённыйQ, сохраняющий условия154branchQ.
- report_human_training_strategy.md —законченный русский отчёт отдельного автора и редактора.
- report_machine_training_strategy.md —законченный английский отчёт с YAML и15ответами/8сценариями.

Machine compressor завершил файл и COMPRESSOR_NOTES.md. Внутри последней writing role YAML разобран;396локальныхссылок/anchors и упомянутые IDs разрешаются, схемы последовательны,185исходных inline literals сохранены. Это собственные проверки автора машинного файла, не новая завершающая стадия. После него новый аудитор/валидатор/поисковая волна не создавались. Token counts не выдумывались.

Банк E001–E051 —альтернативы и переиспользуемые G0–G4, не обязательная сетка прогонов. Известные исправления W2 сохранены в базе, человеческом и машинном текстах. K008 author-code gap открыт; target usefulness и практические условия остаются связанными Q001–Q031.

Материальные ограничения: полный кейс/целевые данные/выбранныйcheckpoint/фактическая training-конфигурация/SDK и доступ LinQ не получены. Выполнены primary search/open, code/document/metadata reading, служебная обработка и wheel byte/hash comparison без установки. Обучение, модельные forward/backward, аудит фактической целевой разметки, generation, graph surgery, export, profiling, аренда GPU и LinQ inference не выполнялись. Качество/скорость/совместимость не обещаются.

Следующая практическая работа после получения кейса/данных/SDK: task+coverage+split contracts, воспроизводимая zero-update baseline, ранний actual-target gate и один следующий discriminating trial по наблюдаемой ошибке. Подробные маршруты/условия/stop rules —в отчётах и E/Q.
