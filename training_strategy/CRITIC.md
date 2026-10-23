# Критика первой волны training_strategy

Исходная критика создана отдельной ролью gpt-6.1-sol/high со свежим контекстом, без истории оркестратора. Дата анализа: 23.10.2026, начало фиксации после 04:18 UTC / 07:18 Europe/Moscow. Полностью прочитаны UTF-8 Context-prompt.md, prompt-training-strategy.md, _WORK/ROLE_PROMPTS.md, _WORK/PLAN.md и все 15 файлов _WORK/W1/*.md; большие файлы читались последовательными диапазонами, недостающие после усечения диапазоны дочитаны. Первичные указатели и локаторы изучены по сохранённым материалам веток. Нового сетевого поиска, обучения, inference, export, установки и проверки SDK критик не выполнял.

Это исходная критика перед второй волной. Сборщик впоследствии добавляет outcomes по K-ID, сохраняя приведённые формулировки и различие между найденным ранее и найденным позднее.

## Общий вывод

Первая волна содержательно покрыла все восемь сценариев и пятнадцать направлений задания. Её сильная сторона — отсутствие вымышленного универсального recipe: методы связываются с наблюдаемой ошибкой, типом данных, контролируемым сравнением и состоянием целевого артефакта. Случайное кадровое разбиение, псевдоразметка как GT, нули как ускорение и ONNX как доказательство LinQ не приняты за достаточные основания. Повторять эти предупреждения во второй волне ради независимого подтверждения не нужно.

Остаточный риск другой: несколько практически привлекательных развилок заканчиваются общим вопросом к model_stack, хотя часть ответа ещё можно получить чтением публичной реализации. Нужно довести выбранные сильные маршруты от документации до точного training/data/artifact contract и проверить ограничивающие условия. При этом исследование не должно превращаться в разработку trainer или попытку угадать неизвестный кейс.

Ни один K-ID не означает, что опубликованный метод обязан улучшить наши данные. Вторая волна может завершить замечание отрицательным ответом или точной границей применимости. «Реализация существует», «прочитан код» и «проверено выполнением» остаются разными статусами.

## Установленное, которое необходимо сохранить

| Материал | Сильное установленное знание | Что не нужно исследовать повторно |
|---|---|---|
| W1-01 F01–F07, E01–E03 | Detection error taxonomy не устанавливает причину; oracle object/association подстановка отделяет detector от event errors; наблюдаемость и actual model input проверяются до большого training | Новый общий обзор TIDE или повтор доказательства, что object AP не равен качеству события |
| W1-02 F01–F12; W1-03 F01–F05/F15; W1-15 F01–F03 | TFA shots — instances/class; различаются sample-set, optimizer и camera/session variance. TFA predictor-only не равен любому YOLO freeze; проверены native freeze/BN и class-row transfer на конкретном pin | Универсальное «30 seeds» либо ещё один пересказ TFA без нового implementation/protocol ответа |
| W1-03 F06–F14; W1-04 F09/F10/F15 | Class coverage, sparse instances и unlabelled images требуют разных механизмов; FedLoss не чинит missing boxes; пустой txt не доказывает negative | Ещё один общий совет «разметьте полностью» вместо уточнения поддержанного loss/assignment пути |
| W1-04 F01–F17 | RFS image-frequency и cls_pw instance-frequency различны; cls_pw умножает и negative BCE entries; focal classification не равен DFL; hard-negative кадр требует полной рабочей разметки | Объявление focal/oversampling универсально полезными; повтор LVIS таблицы как ожидаемого CCTV gain |
| W1-05 F01–F22; W1-06 F04–F11 | Зафиксированы switches, bbox-only CopyPaste no-op, версия Albumentations, small-label survival; SAHI merge defaults и fallback batch важны; cascade recall ограничен usable-crop coverage | Ещё один каталог transforms, формула «площадь 4× = latency 4×» или oracle-crop качество как system качество |
| W1-07 F01–F10; W1-08 E01; W1-09 F13/E01–E03 | Adaptation/selection/new-session/new-camera роли разделены, включая unlabelled exposure. AL pool отделён от lockbox. Аудит учителя должен искать no-detection misses, а не только precision предложенных boxes | Повтор общих правил leakage и confidence≠correctness |
| W1-10 F01–F15 | На pin 8.4.184 найдена native feature KD; FGD/LD имеют конкретные grids/heads/GT contracts; teacher/student и final unwrap различаются; GroundingDINO phrase→class substring — реальная точка отказа | Отрицание KD по неверному guessed path; перенос LD в DFL-free YOLO26 одним коэффициентом; teacher AP как student AP |
| W1-11 F01–F19 | Синтетическое изображение и достоверные labels — разные артефакты; опубликованы и gains, и отрицательные naive mixes; состояние/отношение требует повторной верификации | Новое доказательство «синтетика иногда помогает», миллион картинок как самоцель |
| W1-12 F01–F08; W1-14 F01–F12; W1-15 F04–F09 | Восстановлены auto optimizer, accumulation, EMA, close_mosaic, early stop и resume границы; DDP не объединяет VRAM; timing и T_ready отделены; best.pt/AP convenience output не заменяют selection/support contract | Универсальный optimizer, прогноз минут по названию RTX 4070, FLOPs как latency |
| W1-13 F01–F14; W1-15 E04 | FP/export/optimization/quant/target effects разделены; LinQ публично заявляет Compiler/DNN Quant/int8, но SDK/quant contract не установлен; mask pruning не уменьшает плотные dimensions | Ещё один общий ORT overview или объявление отсутствия LinQ capability по отсутствию документа |

Эти ветки не лишены практических неизвестных; они уже достаточны для соответствующих условных выводов. Их первичные числа должны сохранять модели, версии, единицы, split и недостаточно восстановленный checkpoint-selection protocol.

## Приоритеты второй волны

P0 означает высокую ценность публичного уточнения, а не обязательный метод будущего хакатонного решения. P1 — полезная условная развилка. P2 — дорогой специализированный маршрут, который исследуется ограниченно и допускает закрытие как неприоритетный.

| K-ID | Приоритет | Что меняет решение | Medium задача / собственный результат |
|---|---|---|---|
| K001 | P0 | Какие native KD пары действительно можно ставить рядом с публичными LinQ YOLO5s/8/11 leads | W2-01 → _WORK/W2/01_NATIVE_KD_CONTRACT.md |
| K002 | P0 | Возможен ли безопасный union неоднородных labels без нового loss/assignment | W2-02 → _WORK/W2/02_PARTIAL_ASSIGNMENT.md |
| K003 | P1 | Есть ли содержательный one-stage SSOD маршрут вместо переноса двухэтапных recipes по названию | W2-03 → _WORK/W2/03_ONESTAGE_SSL.md |
| K004 | P0 | Какой дешёвый AL selector можно получить из фактических detector outputs | W2-04 → _WORK/W2/04_ACQUISITION_INTERFACE.md |
| K005 | P1 | Можно ли допускать неисправленные pseudo-labels; что означает качество малого аудита | W2-05 → _WORK/W2/05_TEACHER_AUDIT.md |
| K006 | P1 | Что именно выбирать в предобучении при малой целевой разметке | W2-06 → _WORK/W2/06_DETECTION_PRETRAINING.md |
| K007 | P2 | Что реально требуется source-free camera adaptation и какой deployment graph остаётся | W2-07 → _WORK/W2/07_SOURCEFREE_ROUTE.md |
| K008 | P1 | Как Gen2Det сохраняет supervision после удаления labels и насколько это портируемо | W2-08 → _WORK/W2/08_SYNTHETIC_SUPERVISION.md |
| K009 | P1 | Есть ли конкретный detector QAT→export путь и какие quant параметры нужно запросить у LinQ | W2-09 → _WORK/W2/09_DETECTOR_QAT.md |
| K010 | P2 | Существует ли физически уменьшенный multi-branch detector graph, а не только masks | W2-10 → _WORK/W2/10_PHYSICAL_PRUNING.md |
| K011 | P0 | Как не потерять нужный epoch/EMA и правильно начать staged fine-tuning | W2-11 → _WORK/W2/11_CHECKPOINT_CONTROL.md |
| K012 | P0 | Как не превратить множество E-процедур в перегруженную обязательную очередь | W2-12 → _WORK/W2/12_TRIAL_QUEUE.md |

## K001 — Native KD найден, но проверенная пара и версия не доведены до маршрута выбора

**Проблема.** W1-10 правильно установил наличие KD и final unwrap, однако наиболее конкретный пример — YOLO26n←YOLO26s. Публичный список LinQ из W1-13 называет yolo5s/yolo8/yolo11, а exact graph для кейса неизвестен. Не установлено, для каких пар этих более близких к публичному lead семейств новый wrapper действительно получает нужные feature/head contracts; одно число levels и отсутствие constructor family check этого не доказывают. Восемь веток используют один свежий SHA/version; это одна цепочка происхождения, а не независимые confirmations. Версия исходного дерева ещё не означает доступный релиз/пакет с тем же поведением.

**Материал.** _WORK/W1/10_TEACHER.md F01–F06/F12, Q01/Q04/Q05; _WORK/W1/02_FINETUNING.md F06–F10; _WORK/W1/13_COMPRESSION.md F13/F14.

**Последствие для решения.** Нельзя превращать «есть штатный KD» в первый готовый training recipe для любой выбранной LinQ-oriented модели. При отсутствии проверенной пары дополнительная интеграция может перевесить малый опубликованный gain; при наличии пары маршруту можно придать более высокий условный приоритет.

**Нужное доказательство.** Pinned package/release provenance и code trace пары teacher/student: Detect inputs/levels/strides, head score shapes, one-to-many/one-to-one branches, dataset-driven class setup обеих моделей, teacher buffers/gradients и извлечение final student. Таблица documented support / code-observed compatibility / needs execution. Семантическое совпадение классов нельзя установить по одному nc.

**Точная Medium задача.** W2-01: восстановить ограниченную compatibility matrix native KD для YOLO8/11/26 detect на том же pin и проверить доступность релизного артефакта. Не запускать модели и не делать вывод о LinQ. Достаточно одного понятного сильного candidate path и явно исключённых/непроверенных комбинаций.

## K002 — Для partial labels нет полного отрицательного supervision trace выбранного one-stage criterion

**Проблема.** Предупреждение W1-03 убедительно, но его concrete special losses относятся преимущественно к proposal-based Detic/Niitani/SparseDet. По Ultralytics прочитаны empty labels и общий BCE; не проведён полный путь class-unknown и hidden-instance через assigner, task-specific criterion и end-to-end ветви. Поэтому остаётся недостающий публичный ответ: какие участки придётся менять и есть ли уже штатный interface, сохраняющий coverage/ignore.

**Материал.** _WORK/W1/03_FEWSHOT_PARTIAL.md F06–F14/E02/Q02; _WORK/W1/04_IMBALANCE.md F09/F10/F15; _WORK/W1/12_OPTIMIZATION.md F08.

**Последствие для решения.** Команда может недооценить цену «добавим маску loss» либо ошибочно отказаться от поддержанного механизма. Выбор доразметка / separate task / специальный trainer должен учитывать действительное назначение negatives, а не только format labels.

**Нужное доказательство.** На pin 8.4.184 проследить loader→target preprocessing→assignment→positive/negative targets→classification/regression/другие affected losses для A полных labels, B полностью скрытого класса и C одного скрытого instance present class. Установить, что доступно через публичный API, а что требует изменения кода; учесть используемые head families и end-to-end branch. Статический trace не выдавать за градиентный тест.

**Точная Medium задача.** W2-02: подготовить минимальный implementation contract для трёх случаев и decision table, включая потерю metadata при обычном bbox export. Не разрабатывать patch; будущий E02 остаётся проверкой правильности исполнения.

## K003 — One-stage SSOD остаётся общей оговоркой вместо конкретной условной альтернативы

**Проблема.** W1-09 подробно восстановил SoftTeacher/UTv1 и корректно отказался переносить их в YOLO. UTv2/FCOS разобран по статье, но actual uncertainty head и его eval/export path не прочитаны. Из этого материала пока нельзя отличить реальную one-stage интеграционную цену от отсутствия исследованного маршрута.

**Материал.** _WORK/W1/09_PSEUDO.md F01–F12, E03, Q02/Q04; _WORK/W1/03_FEWSHOT_PARTIAL.md F10–F12.

**Последствие для решения.** Offline fully corrected labels остаются хорошим первым кандидатом. Однако online SSOD нельзя ранжировать как готовую YOLO опцию или как исключительно двухэтапный legacy путь. Должна существовать хотя бы одна честная concrete branch либо доказательная причина её низкого приоритета.

**Нужное доказательство.** Авторский code/config одной one-stage SSOD реализации: поддержанная architecture/head, L/U streams, geometry, missing-positive treatment, regression confidence/uncertainty, EMA/checkpoint выбор и final inference graph. Контроль additional labeled audit и сравнение compute сохраняются. При перспективной YOLO-specific реализации можно заменить менее релевантный кандидат, объяснив пользу, без каталога всех SSL.

**Точная Medium задача.** W2-03: сначала закрыть unread implementation UTv2; затем ограниченно проверить один авторский YOLO-specific lead, если он меняет решение. Дать цену портирования в интерфейсах и минимальный correctness gate, без обещанного качества/времени.

## K004 — Практическому AL loop не хватает подтверждённого контракта доступных scores

**Проблема.** W1-08 показывает, почему ActiveTeacher ROI entropy нельзя считать готовым selector для YOLO, и предлагает простой uncertainty/disagreement. Но не установлено, доступны ли у выбранного публичного candidate реальные class vectors, pre-NMS boxes, embeddings или только max score/class после top-k/NMS. Для sigmoid detection entropy и наличие objectness также нельзя подразумевать по классификационному примеру.

**Материал.** _WORK/W1/08_ACTIVE.md F01/F02/F05, таблица вариантов, Q03; _WORK/W1/10_TEACHER.md F04/F15; _WORK/W1/15_SELECTION.md F09.

**Последствие для решения.** Без этого «дешёвый selector» может потребовать больше изменения inference code, чем ручной/стратифицированный random. Неправильно вычисленный score может систематически выбирать плотные сцены и игнорировать confident misses.

**Нужное доказательство.** Pinned public prediction interface, точная семантика returned scores/classes и стадия filtering для YOLO8/11/26; различие scalar max confidence, complete vector, background/objectness и embeddings. Один реально доступный selection route с no-detection exploration, temporal caps, annotation completeness и учётом дополнительных forwards.

**Точная Medium задача.** W2-04: построить минимальный контракт acquisition из имеющихся outputs и указать, что требует hooks/модификации модели. Не писать runnable selector и не объявлять предложенный ranking лучше random.

## K005 — Малый teacher audit не даёт правила допуска unchecked labels и переносимой оценки coverage

**Проблема.** W1-09 E01/F13 хорошо требуют missed-positive audit и denominators. Но class-aware cutoff остаётся предложением без разобранной связи class confidence с bbox correctness и без решения, какие выводы допускают малые, стратифицированные и коррелированные данные. Достаточность редкого класса нельзя закрыть одной общей precision или неопределённым «если достаточно GT».

**Материал.** _WORK/W1/09_PSEUDO.md F13/E01/Q03; _WORK/W1/08_ACTIVE.md F08/F09/E01; _WORK/W1/10_TEACHER.md E01; _WORK/W1/15_SELECTION.md F06/F07.

**Последствие для решения.** Для полной ручной коррекции calibrated scores не обязательны. Для unattended pseudo-label branch нужно уметь отказаться от auto-accept, когда evidence недостаточно, и не скрыть пропуски за высоким threshold. Это влияет на выбор manual assistance против unchecked SSOD, а не на обязательный запуск новой calibration модели.

**Нужное доказательство.** Detection-specific primary calibration/selection evidence, различающее class correctness, IoU, coverage и отсутствие предсказания. Процедура аудита с random prevalence component и targeted diagnostics, явной единицей независимости и способом отчёта, когда interval невалиден/невычислим. Не подставлять iid box-count в формулу при общих сценах; выбранные по тому же аудиту cutoffs требуют отдельного статуса оценки.

**Точная Medium задача.** W2-05: дополнить E01 таблицей допустимых claims и отказов для small/stratified audit, сохранив отдельный holdout. Показать, что именно публичные источники устанавливают, а сколько данных нужно нашему редкому классу — неизвестно до case.

## K006 — Ветка выбора предобучения не сравнила detector-specific initialization

**Проблема.** W1-02 силён по freeze/BN/row transfer, но основная pretraining абляция — ImageNet initialization против scratch в Mask R-CNN. Вопрос задания шире: какие исходные знания полезнее малой target разметке — целый source detector, representation pretrained на classification/self-supervision или task-specific detector. Конкретные веса — область model_stack, но условия стратегии переноса не должны свестись к «pretrained или scratch».

**Материал.** _WORK/W1/02_FINETUNING.md F01–F05 и карта стратегии; _WORK/W1/03_FEWSHOT_PARTIAL.md F01–F05; _WORK/W1/01_BASELINE.md F04/E01.

**Последствие для решения.** Можно выбрать несовместимый/слабый initialization или приписать gain предобучению, одновременно заменив head/training recipe/объём source data. «Мало target labels» само по себе не выбирает победителя.

**Нужное доказательство.** Ограниченный набор detection-specific primary ablations с одинаковыми downstream data/budget/model или явно учтёнными confounds: transferred components, source task/data, target label unit, base/novel retention, recipe/checkpoint selection и стоимость получения pretraining. Нужно отделить использование готового artifact от обучения pretraining с нуля.

**Точная Medium задача.** W2-06: дать conditional initialization decision table и минимальную честную comparison пару; не составлять каталог PPE weights и не обещать supervised/self-supervised победителя. Leads из references W1-02, DetCo/DETReg рассматриваются как непроверенные направления до чтения первичных материалов.

## K007 — Source-free detector путь недостаточно восстановлен для выбора по одной камере

**Проблема.** W1-07 корректно отделил source-free от UDA и показал transductive trap, но для исходного SFOD2021 не найден авторский repo, а самоentropy остаётся proxy. Публичная часть вопроса «какой минимальный source-free detector artifact/loop действительно существует» осталась открытой; её нельзя смешивать с неразрешимым сейчас вопросом качества на наших камерах.

**Материал.** _WORK/W1/07_DOMAIN.md F06–F08/E02/Q01–Q04; _WORK/W1/02_FINETUNING.md E02; _WORK/W1/09_PSEUDO.md E03.

**Последствие для решения.** При отсутствии source images и наличии target video команда должна знать, сравнивает ли она простой self-training, изменение BN, дополнительный teacher loop или другой архитектурный метод. Ниже цена source-free не следует из самого названия.

**Нужное доказательство.** Один авторский публичный route: source checkpoint requirements, допущение shared closed-set ontology, доступные target inputs и role exposure, losses/teacher/BN state, model-selection inputs, final graph и зависимости. Нужен ограничивающий пример или protocol, показывающий предел proxy selection/forgetting.

**Точная Medium задача.** W2-07: ограниченно довести один source-free detection route до implementation/selection contract либо честно закрыть как неподтверждённый низкоприоритетный маршрут. Не искать способ доказать target gain без целевых labels и не повторять полный обзор domain adaptation.

## K008 — Synthetic background-ignore доказан статьёй, но не конкретным trainer

**Проблема.** W1-11 F10/F11 содержит особенно полезный отрицательный результат naive synthetic mix и положительный полный Gen2Det package. Однако inspected artifacts — README XPaste/context_aug; actual Gen2Det filtering/sampling/background-ignore loss не прочитан. Нельзя пока установить, какие false negatives остаются в proposals/assignment и какой минимальный код требуется, чтобы новый JPG не стал отрицательным supervision.

**Материал.** _WORK/W1/11_SYNTHETIC.md F08–F14, E01/E02, Q05; _WORK/W1/03_FEWSHOT_PARTIAL.md E02.

**Последствие для решения.** Синтетику можно применять как fully reviewed data-only intervention. Неисправленные filtered labels требуют отдельного trainer contract, и успех полного Gen2Det нельзя переносить на обычный YOLO folder merge.

**Нужное доказательство.** Versioned author implementation, если доступна: где и на каких classes/regions подавляется negative loss, какие stages остаются supervised, как sampling влияет на real/synthetic exposures, как сохраняются masks/classes/metadata и что остаётся при eval. Если авторский code недоступен, точно назвать недостающее звено и не изобретать алгоритм из paper.

**Точная Medium задача.** W2-08: проверить один Gen2Det supervision path и его ограничивающие ablations, включая происхождение опубликованной строки. Итог — route fully reviewed data / special loss / not established; генерировать данные и реализовывать port не требуется.

## K009 — QAT пока описан принципом, без detector-specific export route

**Проблема.** W1-13 верно отделил QAT от training dtype и указал неизвестный LinQ quant contract. Но практический ответ на QAT часть задания остаётся на уровне общей работы Jacob и ORT, который QAT trainer не предоставляет. Даже при получении target contract неясен публично доступный detector recipe и способ получить нужный export.

**Материал.** _WORK/W1/13_COMPRESSION.md F02/F04/F12, Q02/Q05, E03; _WORK/W1/10_TEACHER.md F12; _WORK/W1/15_SELECTION.md E04.

**Последствие для решения.** Команда не должна начинать произвольный QAT после потери PTQ или считать fake-quant checkpoint пригодным LinQ input. При этом отсутствие исследованного recipe не означает отсутствия detector QAT как capability.

**Нужное доказательство.** Один конкретный detection QAT training/export маршрут с pinned toolchain, поддержанной моделью/операторами, weight/activation quantization, scales/zero points/axes, fusion/fake-quant behavior и форматом итогового артефакта. Показать соответствие/неизвестное относительно public LinQ DNN Quant lead; same-data FP continuation нужен как контроль дополнительного training.

**Точная Medium задача.** W2-09: восстановить один публичный detector QAT route и составить compatibility questions к SDK. Не требуется повторно доказывать, что ORT≠LinQ; реальное соответствие выдаваемому SDK остаётся открытым.

## K010 — Ветка pruning не имеет практического пути физического уменьшения детектора

**Проблема.** W1-13 отлично разобрал маски PyTorch, но positive physical-pruning evidence — историческая классификационная CNN работа. Для multi-branch detector с concat/residual/neck/head не восстановлен ни один graph-surgery инструмент/recipe. Вопрос задания о pruning сейчас отвечает преимущественно «что не доказывает ускорение».

**Материал.** _WORK/W1/13_COMPRESSION.md F08–F11/E03; _WORK/W1/10_TEACHER.md F04/F12.

**Последствие для решения.** Нельзя оценить, заслуживает ли physical pruning места рядом с меньшим готовым student/KD. Риск — потратить время на masks или необратимо изменить head/classes без пригодного exporter.

**Нужное доказательство.** Одна авторская detection-aware dependency/graph surgery реализация с pin, поддержанной architecture/version, правилами удаления зависимых channels, excluded layers/head handling, recovery training и serialization/export. Уменьшенные tensor dimensions — одно доказательство; измерение latency именованного runtime — другое. Для LinQ измерения отсутствуют.

**Точная Medium задача.** W2-10: проверить ограниченный путь Torch-Pruning/DepGraph или более релевантный авторский detector route и сравнить интеграционные предпосылки с меньшим штатным student. Не делать surgery и не утверждать ускорение из FLOPs.

## K011 — Для custom checkpoint objective и staged training не хватает операционной схемы сохранения

**Проблема.** W1-12/W1-15 доказали, что встроенный best — EMA/mAP и final stripping разрушает полноценный resume, а resume игнорирует часть overrides. Но рекомендация сохранить нужные epoch artifacts и выполнить freeze→unfreeze заканчивается вопросом к model_stack. Публичный trainer уже позволяет выяснить порядок callbacks/save/validation и точный warm-start/resume contract.

**Материал.** _WORK/W1/12_OPTIMIZATION.md F05–F07/E03/E04/Q07; _WORK/W1/15_SELECTION.md F08/E02/E04/Q03; _WORK/W1/10_TEACHER.md F03/F06.

**Последствие для решения.** Нужный по critical recall/event constraint epoch может быть перезаписан; «продолжить best.pt» может означать новый optimizer/start state, а не продолжение траектории. Отсутствие сохранённого состояния нельзя исправить правильным manifest задним числом.

**Нужное доказательство.** Pinned call-order: online/EMA validation, fitness assignment, best/last/periodic files, callbacks, stripping, сохранённые state keys и whitelist overrides. Развести exact resume, warm start и новый staged run; RNG/loader trajectory подтверждается только реально сохранёнными полями и будущей проверкой.

**Точная Medium задача.** W2-11: дать минимальную схему сохранения candidate bundle по собственной constrained metric и схему freeze→unfreeze без неявно игнорируемых overrides, с разделением штатного API и требуемой кастомизации. Чтение кода не заменяет reload/continuation test.

## K012 — Множество хороших E-процедур ещё не образует исполнимую очередь

**Проблема.** В W1 есть десятки полезных E-ID и отдельные caps. W1-14 правильно описывает T_ready и критический путь, но совокупность baseline/full/head/mixing/AL/SSL/KD/synthetic/scale/compression/repeats легко прочитать как обязательную программу. Есть также известная опасность cheap-fidelity отбора: короткий run с close_mosaic, warmup, auto optimizer и малой validation может быть другой recipe, а не ранней стадией длинного кандидата.

**Материал.** Все _WORK/W1 E-процедуры; особенно _WORK/W1/12_OPTIMIZATION.md F02/F05/F06, _WORK/W1/14_COMPUTE.md F12/E03–E05, _WORK/W1/15_SELECTION.md E03/Q07.

**Последствие для решения.** Обильные GPU не снимают последовательные annotation/SDK/selection/export зависимости. Неверный ранний kill может отвергнуть полезный кандидат; широкая очередь может не оставить времени получить проверяемый artifact.

**Нужное доказательство.** Содержательный synthesis зависимостей существующих E-ID, отдельно обязательные correctness/target gates и альтернативные hypothesis trials; измеримые условия назначения seed/full run/DDP/teacher/annotation. Если предлагается multi-fidelity/ASHA/ранний ranking, нужны первичные основания и предел переноса на detection, особенно fidelity-induced recipe changes. Численные T_ready без workload не требуются и недопустимы.

**Точная Medium задача.** W2-12: создать ограниченную условную очередь для восьми сценариев, с первыми наблюдениями, одним следующим различающим сравнением, stop/kill/promote и deadline для получения useful artifact. Использовать W1/W2 зависимости, не назначать всем методам место в mandatory grid. Не объявлять оптимальный scheduler без измерения.

## Неизвестные, которые вторая публичная волна не может закрыть

Следующее должно перейти в OPEN_QUESTIONS.md с конкретными способами закрытия. Это не основания запускать одинаковые сетевые задачи заново.

| Неизвестное | Что уже известно | Чем закрывается и что меняет |
|---|---|---|
| Полная ontology, mandatory classes/events, допустимость unlabelled/test adaptation и критерии сдачи | Есть лишь анонс кейса и исходное расписание | Полный кейс/постановщик; выбирает все task/data/selection contracts |
| Реальная source×class coverage, independent positives, camera/session/episode provenance и визуальный сигнал | Есть нужные manifest/audit схемы; целевые файлы не получены | Артефакты и ручной audit; разрешает merge, sampling, few-shot claim и observation scale |
| Лучший checkpoint/pretraining, freeze mask/BN policy, useful augmentation, cutoff или mixing ratio | Есть условные варианты и versioned code, универсального optimum нет | Контролируемое обучение/инференс после получения данных; public paper не выдаёт target gain |
| Качество teacher на критичных class/size/conditions, экономия annotation minutes, safety auto-accept | Teacher artifacts/leads есть, audit не выполнен | Blind complete audit + annotation pilot; определяет manual assistance/unchecked labels/KD |
| Реальный LinQ device/SDK/compiler/quant contract и поддержка конкретного graph | Производитель заявляет int8, Compiler/DNN Quant и некоторые YOLO families, exact версия неизвестна | Выдаваемые SDK/доступ, versioned guide и compile/run; никакая W2 framework matrix не даёт proof execution |
| QAT arithmetic match, placement/fallbacks, export/quant quality и target latency | Есть правильная цепочка parity и вопросы к SDK | Реальные artifacts и target test; ORT/reference metric только промежуточное evidence |
| Конфигурация RTX 4070/облака, VRAM, throughput, DDP scaling и integration time | Известны названия доступных ресурсов, profiling не выполнялся | Inventory + bounded profiling; не оценивать минуты из названия GPU |
| Numerical acceptance margins, rare-event reliability и population uncertainty | Есть предлагаемый constrained-selection contract и правильные единицы | Кейс + baseline support + independent groups; не превращать N/A/degenerate CI в нули |

## Передача сборщику и авторам

Сохранить published measurements с их исходной задачей: LVIS mask AP, SAHI AP50, COCO AP50:95, pedestrian miss rate/FPPI и robot cm не являются одним quality scale. Различать число изображений, instances, независимых episodes, cameras, human minutes и GPU-hours. Один общий Ultralytics pin — удобная связная опора, но не независимость evidence и не обязательный стек команды.

Из W2 нужно получить новую реализационную определённость, отрицательные результаты или локализованные public gaps. После неё не добавлять третью поисковую волну: unresolved public artifact/recipe и empirically unknown benefit заносятся отдельно. Неполные checkpoint-selection данные старых papers не мешают использовать их как ограниченное доказательство идеи; они мешают выдавать таблицу за точный быстрый recipe или ожидаемый gain.

В отчётах обязательны развилки, а не одновременное применение всех E-ID. Сначала установить task/data/artifact contracts и причину ошибки, затем выбрать одно содержательное сравнение. Высокая стоимость teacher/SSL/pruning не означает запрет; наличие работающей реализации и существенного relevant gain может изменить приоритет. Единственный заранее обязательный platform outcome — фактически подтверждённое выполнение выбранного inference artifact на LinQ, когда доступ будет получен.

## Outcomes второй волны

На момент исходной критики W2 ещё не выполнена. Сборщик добавляет для каждого K-ID: путь результата, новые source/fact IDs, статус «закрыто / уточнена область / противоречие / открыто / потеряло значение», изменённое решение и оставшийся case/SDK/experiment вопрос. Исходные замечания выше не переписываются.

<!-- COLLECTOR_W2_OUTCOMES -->

## Сборщик: outcomes K001–K012 после второй волны

Дата сборки: 2026-10-23T08:35:02+03:00, Europe/Moscow. Исходный текст выше сохранён. Новые основания —12 самостоятельных W2 результатов; сборщик прочитал их вместе со всеми15W1. Ни один outcome не означает выполненное обучение/экспорт/target inference. Закрытие относится к указанному public/methodical вопросу, остаток вынесен в OPEN_QUESTIONS.

### K001: уточнена область

- **Результат:** [_WORK/W2/01_NATIVE_KD_CONTRACT.md](_WORK/W2/01_NATIVE_KD_CONTRACT.md).
- **Новые/уточняющие источники:** S078, S137, S138, S139, S080, S140, S012, S011.
- **Глобальные факты:** F187, F188, F189, F190, F191, F192, F193; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E027, E028; Q005, Q006, Q007, Q011, Q025, Q030.
- **Что найдено:** Установлена package provenance: release R не U, wheel8.4.184 действительно получен, SHA и10нужныхfiles byte-equal U. Конкретизирован documented same-family/code-supported YOLO11n←target-trainedYOLO11s: grids/channels/strides/raw scores и native student extraction.
- **Как изменилось решение:** Разное nc технически допустимо max-class feature weighting; teacher сохраняет свой class contract. Это не semantic transfer и не quality admission. EMA уже без teacher, wrapper/projectors до unwrap. KD теперь конкретная опция при готовом полезном teacher, без обязательного обучения нескольких families.
- **Остаток case/SDK/artifact/experiment:** Installation, actual checkpoint compatibility/BN/gradients/VRAM, teacher competence, controlled student gain/export/LinQ не выполнены.

### K002: закрыто

- **Результат:** [_WORK/W2/02_PARTIAL_ASSIGNMENT.md](_WORK/W2/02_PARTIAL_ASSIGNMENT.md).
- **Новые/уточняющие источники:** S025, S141, S026, S012, S142, S143, S144, S145, S146.
- **Глобальные факты:** F194, F195, F196, F197, F198, F199, F200, F201, F202, F203, F204, F205; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E007; Q003, Q006, Q013, Q007.
- **Что найдено:** Закрыт именно публичный static loader→assignment→loss gap: hidden GT не создаёт targets, U dense BCE отрицательна по zero-target entries, regression только known foreground, две active E2ELoss branches. Legacyv5 отдельно objectness.
- **Как изменилось решение:** B unknown class допускает custom image×class validity при exhaustive остальных; C hidden instance не решается той же полной class mask. Нужны positive precedence/reduction/geometry и transformed coverage. MMDet known crowd route class-agnostic, thresholds defaultoff, zero regularGT всё background. Unsafe union не готов по одному ignore flag.
- **Остаток case/SDK/artifact/experiment:** Практические gradients/mask correctness/actual coverage/target gain не проверены. Default conditional альтернатива — fully checked subset либо separate exhaustive own tasks; это не claim always-best.

### K003: уточнена область

- **Результат:** [_WORK/W2/03_ONESTAGE_SSL.md](_WORK/W2/03_ONESTAGE_SSL.md).
- **Новые/уточняющие источники:** S147, S148, S149, S150, S151, S152, S153, S154, S155, S156, S157, S158.
- **Глобальные факты:** F206, F207, F208, F209, F210, F211, F212, F213, F214, F215, F216, F217, F218, F219; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E026; Q002, Q004, Q011, Q021, Q007.
- **Что найдено:** Найдены и прочитаны concrete UTv2 FCOS и отдельный EfficientTeacher legacy YOLOv5 route, с head/loader/geometry/pseudo losses/state/extraction boundaries.
- **Как изменилось решение:** UTv2 std branch остаётся Python eval, teacher default. ET rawstudent/onlineEMA/secondarybest/export различны, --da снимает domain heads, export raw levels требует decode. Нельзя назвать generic modernYOLO feature; один compatible route — альтернатива corrected-supervised.
- **Остаток case/SDK/artifact/experiment:** Weights/lock/runtime/empty/mixed gradients/clean extraction/export parity и actual target benefit/LinQ открыты.

### K004: закрыто

- **Результат:** [_WORK/W2/04_ACQUISITION_INTERFACE.md](_WORK/W2/04_ACQUISITION_INTERFACE.md).
- **Новые/уточняющие источники:** S159, S160, S161, S162, S163, S164, S165, S166, S167, S168.
- **Глобальные факты:** F220, F221, F222, F223, F224, F225, F226; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E022; Q006, Q012, Q016, Q002.
- **Что найдено:** Публичный U Results interface закрыт: original xyxy, scalar conf/cls, detect probs=None. Full logits/vectors/features находятся до filtering и требуют другого interface.
- **Как изменилось решение:** Минимальный proposed route low-confidence retained scores + metadata exploration не требует extra forwards поверх уже выполненного pool inference. Это не entropy/calibrated uncertainty. No-box/error/cap rows и exploration обязательны; scan/human QA могут быть дорогими.
- **Остаток case/SDK/artifact/experiment:** Actual checkpoint interface/cost/ranking usefulness против stratified random при equal total human minutes не измерены.

### K005: закрыто

- **Результат:** [_WORK/W2/05_TEACHER_AUDIT.md](_WORK/W2/05_TEACHER_AUDIT.md).
- **Новые/уточняющие источники:** S169, S170, S171, S172, S173, S174.
- **Глобальные факты:** F227, F228, F229, F230, F231, F232, F233; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E024, E023; Q004, Q010, Q011, Q012, Q013.
- **Что найдено:** Закрыт public-methodical admission gap: detection calibration определяется class+IoU criterion и не может калибровать recall пропусков без scores; netcal получает matched per prediction.
- **Как изменилось решение:** Blind completeGT/no-detection audit, probability P против diagnostics D, известные inclusion probabilities/weighted ratios и group uncertainty сохранены. Cutoff chosen audit не independent confirmation; insufficient support/N/A — отказ от unchecked claim. Fully reviewed assistance не требует calibrator.
- **Остаток case/SDK/artifact/experiment:** Ни один actual teacher/class не допущен: нет target support, numerical acceptance, audit/cost/confirmation.

### K006: закрыто

- **Результат:** [_WORK/W2/06_DETECTION_PRETRAINING.md](_WORK/W2/06_DETECTION_PRETRAINING.md).
- **Новые/уточняющие источники:** S175, S176, S177, S178, S179, S180, S181, S182, S183.
- **Глобальные факты:** F234, F235, F236, F237, F238, F239, F240; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E048, E004; Q005, Q015, Q002, Q030, Q007.
- **Что найдено:** Публичное различение initialization восстановлено: DetCo representation versus DETReg localization/transformer/query components сверх SwAV backbone versus supervised source detector/base stage.
- **Как изменилось решение:** Source/base stage schedules/exposure/normalization/head confound исключают простое causal ranking. DETReg2023few-shot/assets/latepaper и filename scratch не no-pretraining. Предложена одна identical-backbone/head tensor ablation; готовый artifact отличается от pretraining с нуля.
- **Остаток case/SDK/artifact/experiment:** Actual weight key/hash lineage, exact author checkpoint-selection, лучший target init/retention и SDK совместимость не установлены.

### K007: уточнена область

- **Результат:** [_WORK/W2/07_SOURCEFREE_ROUTE.md](_WORK/W2/07_SOURCEFREE_ROUTE.md).
- **Новые/уточняющие источники:** S055, S184, S185, S186, S187, S188, S189, S190.
- **Глобальные факты:** F241, F242, F243, F244, F245, F246; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E020; Q002, Q005, Q022, Q007.
- **Что найдено:** Найден author-linked simple-SFOD AdaBN→fixed pseudoJSON→FasterR-CNN, то есть public implementation больше не только название.
- **Как изменилось решение:** Runnable artifact/selection частично открыты: weights local, JSON ручной и может остаться GT; eval-only реально меняет BN, source ValLossHook/state exposure нарушает строгий source-free. No-grad не frozen evaluation. Fixed ordinary loss не лечит omissions.
- **Остаток case/SDK/artifact/experiment:** Исходный SFOD2021 repo не установлен; exact fixed-row selection/cutoff, compatible source detector/lock, runtime/audit/benefit/retention/LinQ требуют artifact/experiment. P2 conditional, без proxy quality claim.

### K008: открыто

- **Результат:** [_WORK/W2/08_SYNTHETIC_SUPERVISION.md](_WORK/W2/08_SYNTHETIC_SUPERVISION.md).
- **Новые/уточняющие источники:** S099, S191, S192, S193.
- **Глобальные факты:** F247, F248, F249, F250, F251, F252, F253, F254; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E030, E031, E007; Q019, Q020, Q003, Q007.
- **Что найдено:** Author Gen2Det trainer/fork/config/schema не найден после paper→author pages→GitHub exact-name/author tracing. Это локализованный public gap, не отсутствие кода/capability.
- **Как изменилось решение:** Уточнён paper scope: background-ignore RPN+detector head, tau_i0 все synthetic bg, p0.2 whole batches, poolratio/drawfraction/schedule различны. Low-data COCO без filtering/ignore; LVIS ablations и COCO borrowedXPaste provenance ограничивают causal reading. Negative naive-mix сохранён.
- **Остаток case/SDK/artifact/experiment:** До нового primary artifact special-loss route не concrete recipe. Доступная future альтернатива — fully reviewed whole synthetic frames + ordinary supervised detector с real holdout/exposure controls; польза target неизвестна.

### K009: уточнена область

- **Результат:** [_WORK/W2/09_DETECTOR_QAT.md](_WORK/W2/09_DETECTOR_QAT.md).
- **Новые/уточняющие источники:** S194, S195, S196, S197, S198, S199, S200, S201, S202, S203, S204.
- **Глобальные факты:** F255, F256, F257, F258, F259, F260, F261; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E049, E038, E037; Q008, Q023, Q004, Q007.
- **Что найдено:** Concrete detector QAT→export code найден: NVIDIA YOLOv7 fuse→quant/rules→calibration→feature reconstruction→ONNXQDQopset13→TensorRT.
- **Как изменилось решение:** Actual finetune loss featureMSE/no detectorGT; это не supervised newclass adaptation. Historical detector/toolkit lock неполон, reference2.1.2 не установленная авторская версия. MMrazor detector config оказался PTQ. Нельзя переносить route на modernYOLO/LinQ по имени.
- **Остаток case/SDK/artifact/experiment:** Dependency/container/weights/ONNX hashes, arithmetic/fusion/import matchSDK, FP continuation/reconstruction controls и actual exported/target quality открыты. QAT только после PTQ diagnostics.

### K010: уточнена область

- **Результат:** [_WORK/W2/10_PHYSICAL_PRUNING.md](_WORK/W2/10_PHYSICAL_PRUNING.md).
- **Новые/уточняющие источники:** S205, S206, S207, S208, S209, S210, S211, S212, S213, S214, S215.
- **Глобальные факты:** F262, F263, F264, F265, F266, F267, F268, F269, F270, F271; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E050, E037; Q024, Q007, Q009.
- **Что найдено:** Положительный detector-aware graph surgery route найден в author-hosted TP example: dependency groups физически уменьшают Conv/BN/dense dimensions, защищают head outputs.
- **Как изменилось решение:** Ограничение старое: TP1.6.1+U8.0.90/C2f_v2/patched train/save/fullobject, custom import при reload; originalYAML+state_dict topology не восстановит. Conversion-only parity/export/compile доrecovery. Speed_up — MAC ratio, demo break экспортирует current rejected stage без rollback.
- **Остаток case/SDK/artifact/experiment:** Actual pinned execution, conversion/reload/export correctness, recovery useful quality и LinQ latency/memory не измерены. P2 резерв после меньшего native student, не запрет и не mandatory trial.

### K011: закрыто

- **Результат:** [_WORK/W2/11_CHECKPOINT_CONTROL.md](_WORK/W2/11_CHECKPOINT_CONTROL.md).
- **Новые/уточняющие источники:** S011, S081, S164, S216, S217, S105, S012, S104.
- **Глобальные факты:** F272, F273, F274, F275, F276, F277, F193; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E035, E046, E037; Q025, Q010, Q007.
- **Что найдено:** Публичная lifecycle/operational часть закрыта exact save/val/callback/strip/override trace. on_model_save после write доstrip даёт immutable EMA candidates и внешний constrained winner без замены APfitness.
- **Как изменилось решение:** Существенные уточнения ранних формулировок: freeze разрешён resume; LR/optimizer/epochs нет. Prestrip уже EMA вместо online и без scheduler/RNG/loader/accumulation state; strip не единственная причина отсутствия exact continuation. Booleanresume stripped может тихо стать новым training. Новая stage2 с новым recipe явно resumeFalse.
- **Остаток case/SDK/artifact/experiment:** Actual copy/evaluator/reload/stage-transition test, target objective/support/acceptance и finalSDK execution отсутствуют. Exact trajectory требует иного reviewed saver; не обещать восстановление задним числом.

### K012: закрыто

- **Результат:** [_WORK/W2/12_TRIAL_QUEUE.md](_WORK/W2/12_TRIAL_QUEUE.md).
- **Новые/уточняющие источники:** S218, S219, S220.
- **Глобальные факты:** F278, F279, F280, F281, F282, F283, F284; [RAW_FACTS.md](RAW_FACTS.md).
- **E/Q:** E051; все E001–E050 как reused gates/alternatives; Q027, Q028, Q001, Q010, Q007.
- **Что найдено:** Методическая queue часть закрыта: все исходные E размещены в reused G0–G4 или conditional alternatives;8сценариев имеют первое наблюдение, один discriminating next trial, kill/promote/rollback/useful artifact.
- **Как изменилось решение:** Hyperband/ASHA не дают detector rank-preservation guarantee. ShortU может менять autooptimizer/warmup/schedule/close_mosaic, resume не exactprefix; correctness smoke не ранний quality ranking. Admission по wholeCP/D_useful, reviewer/SDK/annotation dependencies, не GPU utilization.
- **Остаток case/SDK/artifact/experiment:** Actual times, workload, resource configuration, independent support, useful deadline и scheduler benefit остаются case/experiment; numerical timetable/optimal scheduler не заявлены.

Статусы: закрыто — K002/K004/K005/K006/K011/K012 (6); уточнена область — K001/K003/K007/K009/K010 (5); открыто — K008 (1). Противоречащие старые/новые ограничения не скрыты: поправки стоят также у затронутых F в RAW_FACTS. Отдельной финальной проверки отчётов этот файл не содержит.
