# RAW_FACTS — training_strategy

Сборка: 2026-10-23T08:35:02+03:00, Europe/Moscow. Полностью прочитаны оба входа, PLAN/RUN_STATE, исходная CRITIC и все27 W1/W2. Нового сетевого получения сборщик не делал. Подробная база сохраняет численные результаты с единицами, версии, протоколы, negative results, implementation contracts, противоречия и проекты проверок.

**Actual checks:** research search/open и read-only metadata/text; W2-01 дополнительно wheel ZIP/bytes/SHA comparison в памяти. Это не установка/модельный запуск. Training, annotation audit, dataset generation, model inference/backward, export, physical surgery, model profiling и LinQ execution не выполнены. Полный кейс, target data, выбранные weights, фактическая GPU/VRAM конфигурация и SDK не предоставлены. Target usefulness всех методов не установлен.

**Основание отдельно от проверки:** DOC/CLAIM — документация/заявление; CODE/REP — исходник; PAPER/PUB/MEASUREMENT — опубликованное авторами описание/измерение; LOCAL/META/BYTES — служебное наблюдение; INFERENCE/INF — наш вывод; PROPOSED/PROP — предлагаемое действие; UNKNOWN — неизвестно. Исходные метки/локаторы в каждом F сохранены. Чтение кода не выполнение, published measurement не наш тест.

**Источники и повторы:** [SOURCES.md](SOURCES.md) хранит версии/access/locators; [_WORK/ID_MAP.md](_WORK/ID_MAP.md) — branch→global. Общий U=e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/8.4.184 — одна evidence chain, не независимые confirmations и не обязательный стек. Одинаковое наблюдение сведено под один F с сохранением дополнительных условий/версий; новая определённость W2 остаётся отдельным фактом. Это парафразы исследования, не полные копии внешних источников.

**Несопоставимые единицы:** COCO box AP50:95, SAHI AP50, LVIS mask AP, novel AP, pedestrian miss-rate/FPPI, event recall/false-alarms-hour и robot cm не объединяются. Images/instances/episodes/cameras/person-minutes/GPU-hours различаются. Missing support/N/A/невалидный CI не становятся нулём.

## Обязательные gates и условный банк

G0 task/decision; G1 data/observation; G2 correctness только при выбранном training; G3 comparison/selection; G4 deploy/rollback — переиспользуемые допуски. AL/SSL/KD/synthetic/initialization/scale/QAT/pruning/repeats — альтернативы, не mandatory grid. Сначала earliest unknown gate, затем одно различающее сравнение. Gates переиспользуются только для того же task/class/data/split/code/dependency/head/input/preprocess/save/export/SDK contract key. Ранний LinQ feasibility и финальное actual execution различны; обязательный platform outcome сейчас не выполнен.

Очередь всех восьми сценариев, дорогих альтернатив и исходного банка E сохранена в синтезе W2-12 ниже. Caps W1 — illustrative proposed diagnostics, не общие бюджеты. Deadline useful artifact задаёт integration owner: now+CP_remaining<=D_useful с измеренными costs, без выдуманных минут RTX4070.

## Критические уточнения и противоречия

1. Native KD существует: wheel8.4.184/10files bytes verified, U — следующий docs commit после release R. YOLO11n←target-trainedYOLO11s doc/code-supported; installation/runtime/benefit/target нет.
2. Teacher сохраняет свои classes; max-class weighting допускает другое nc технически, semantic competence проверяется отдельно. EMA checkpoint уже teacher-free, projectors до final unwrap.
3. Hidden class B и hidden instance C различны. U dense BCE без objectness, legacyv5 objectness и обе activeE2ELoss branches требуют своих validity. MMDet ignore defaults off/zero-regular-GT исключение.
4. UTv2 std auxiliary остаётся Python eval и defaultteacher; EfficientTeacher rawstudent/onlineEMA/secondarybest/export разные, domain heads удаляются явно, rawlevels нужен decoder.
5. Results scalarconf/cls,probs=None; low-confidence heuristic не entropy. No-box/error records+exploration обязательны для предложенной policy; superiority неизвестна.
6. Teacher audit ищет всеGT/no-detection misses; probability P и targeted D отдельно без выдуманных inclusion weights; calibration не восстанавливает recall.
7. Pretraining — состав tensors/ancestry. DETReg base/no-base schedules/unlabelled exposure confound;2023assets/results не ранний2021release.
8. Source-free eval-only меняет BN; source-val hooks/manual JSON могут раскрыть source/hiddenGT. No-grad не frozenstate.
9. Gen2Det author code не найден после primary traces. Paper p whole batches, tau_i0 synthbg RPN+head, lowdata безfilter/ignore; foldermerge не reproduction.
10. NVIDIA detectorQAT — featureMSE reconstruction/noGT, historical lock неполон; QDQ/TensorRT не LinQ arithmetic match.
11. Physical pruning TP1.6.1+oldU8.0.90/C2f_v2/patchedtrain/fullobject; YAML/state_dict не topology; speed_up MACratio, no rejected-stage rollback.
12. Freeze разрешён resume, новыйLR/optimizer/epochs нет. Даже prestrip без online/RNG/loader/scheduler exactstate; on_model_save позволяет immutable serialized EMA candidates.


## W1-01 — W1-01 — выбор стратегии через baseline и диагностику ошибок

<a id="f001"></a>

### F001 — [PAPER]. TIDE разбивает ошибки detection на классификацию, локализацию, их сочетание, дубликаты, фон и пропущенные GT. В основном определении используются…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S002](SOURCES.md#s002). **Исходные IDs:** W1-01-F01.

**W1-01-F01: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F001 [PAPER].** TIDE разбивает ошибки detection на классификацию, локализацию, их сочетание, дубликаты, фон и пропущенные GT. В основном определении используются foreground IoU 0.5 и background IoU 0.1; это диагностические настройки авторов, не пороги бизнес-событий. Каждый oracle считается относительно исходного результата: ΔAP = AP после условного исправления − исходный AP. Последовательное исправление разных ошибок меняет их кажущийся вклад. Применение требует predictions и GT, не устройства обучения. [S002, §2.1–2.3]

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f002"></a>

### F002 — [INFERENCE из F001]. Разложение описывает проявление ошибки, а не причинный диагноз. Пропуск может соответствовать маленькому объекту, occlusion, неверному…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S002](SOURCES.md#s002). **Исходные IDs:** W1-01-F02.

**W1-01-F02: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F002 [INFERENCE из F001].** Разложение описывает проявление ошибки, а не причинный диагноз. Пропуск может соответствовать маленькому объекту, occlusion, неверному preprocessing, отсутствующему классу или недостатку обучения. ΔAP oracle нельзя объявлять достижимым выигрышем следующего fine-tuning. TIDE не оценивает, правильно ли человек связан с каской и достаточно ли длительно нарушено правило.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f003"></a>

### F003 — [CODE/DOC/LOCAL]. `setup.py` содержит package `tidecv`, version `1.0.1`; HEAD — `49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1`. Авторский пример принимает COCO-result…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S003](SOURCES.md#s003). **Исходные IDs:** W1-01-F03.

**W1-01-F03: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F003 [CODE/DOC/LOCAL].** `setup.py` содержит package `tidecv`, version `1.0.1`; HEAD — `49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1`. Авторский пример принимает COCO-result файл через `datasets.COCOResult` и вызывает `tide.evaluate(..., mode=TIDE.BOX)`, `summarize`, `plot`. Это возможный путь анализа уже сохранённых predictions; работа с нашим форматом и текущим Python не проверена. Для нестандартных классов нужен корректный адаптер/GT; стандартный пример COCO нельзя молча считать оценкой кейса.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f004"></a>

### F004 — [DOC]. Пример переводит COCO-pretrained Faster/Mask R-CNN на пользовательские классы, заменяя predictor. В контракте torchvision boxes имеют XYXY pixel coordinates,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S004](SOURCES.md#s004). **Исходные IDs:** W1-01-F04.

**W1-01-F04: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F004 [DOC].** Пример переводит COCO-pretrained Faster/Mask R-CNN на пользовательские классы, заменяя predictor. В контракте torchvision boxes имеют XYXY pixel coordinates, `labels` — integer, `0` зарезервирован для background, `image_id` уникален. В tutorial отдельно проверяются forward с targets и inference в `eval()`. Это основание для проверки контракта данных и mode до эксперимента; conventions других детекторов проверяются отдельно. Демонстрационный Penn-Fudan содержит 170 изображений и 345 pedestrian instances; его случайное image-level разбиение не задаёт независимый протокол для соседних CCTV-кадров. Мы не переносим его AP, optimizer recipe или время на команду.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f005"></a>

### F005 — [PAPER]. Авторы рассматривают missing labels/drops, class flips, box shifts и background spawns. Их способ ранжирования использует classification и regression…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S005](SOURCES.md#s005). **Исходные IDs:** W1-01-F05.

**W1-01-F05: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F005 [PAPER].** Авторы рассматривают missing labels/drops, class flips, box shifts и background spawns. Их способ ранжирования использует classification и regression losses обеих стадий двухстадийного detector; высокий score или uncertainty не эквивалентны проверенной ошибке label. Исследование включает симулированные и реальные ошибки. Здесь не переносим численный precision из abstract, поскольку его полный режим и база для нашего кейса не сопоставлены. Практическое следствие: спорное FP сначала проверять человеком против annotation policy; автоматическое несовпадение model/GT не выбирает, кто прав. Метод loss inspection не является установленной функцией выбранного YOLO trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f006"></a>

### F006 — [DOC]. Документация предупреждает: official weights без явного `data` могут использовать fallback task dataset `coco8.yaml`. Настройки confidence и NMS IoU влияют…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S005](SOURCES.md#s005), [S006](SOURCES.md#s006). **Исходные IDs:** W1-01-F06.

**W1-01-F06: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F006 [DOC].** Документация предупреждает: official weights без явного `data` могут использовать fallback task dataset `coco8.yaml`. Настройки confidence и NMS IoU влияют на итог; validation geometry может отличаться от predict/fixed export, в том числе из-за rectangular padding. В текущем тексте есть сохранение predictions JSON и per-image TP/FP/FN. Проверять конкретные API и defaults нужно на зафиксированном release. Следствие для baseline: явно фиксировать dataset, split, геометрию и postprocessing, а не полагаться на автоматическое восстановление settings.

### Недоступный первичный след

Missing Labels in Object Detection, Xu/Bai/Ghanem, CVPRW 2019: PDF `https://openaccess.thecvf.com/content_CVPRW_2019/papers/Weakly%20Supervised%20Learning%20for%20Real-World%20Computer%20Vision%20Applications/Xu_Missing_Labels_in_Object_Detection_CVPRW_2019_paper.pdf` и HTML по тому же названию вернули web-tool HTTP 403 Forbidden. Поиск видел документ, но он не считается прочитанным. Независимый первичный путь для текущего решения — открытый полный текст S005; выводы и числа недоступной статьи не используются. Дальнейший поиск её exact recipe не меняет решение W1-01 и передаётся ветке partial labels при необходимости.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f007"></a>

### F007 — [INFERENCE из F001/F004/F005/F006 и исходной постановки]. Baseline — это комплект из checkpoint и неизменяемого контракта наблюдения, а не только один mAP. До…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-01-F07.

**W1-01-F07: условия/наблюдение** ([ветка](_WORK/W1/01_BASELINE.md)):

**F007 [INFERENCE из F001/F004/F005/F006 и исходной постановки].** Baseline — это комплект из checkpoint и неизменяемого контракта наблюдения, а не только один mAP. До выбора обучения нужно собрать следующие сведения:

1. **Что считается успехом.** Развести object classes, наблюдаемые состояния и violation events. Уточнить неоднозначное: «helmet присутствует» против «helmet надет данным человеком»; «нет видимого респиратора» против «нарушено обязательное правило ношения». Не вводить эти классы как уже заданные организаторами.
2. **Что видно.** Посмотреть исходный кадр и фактический input после resize/padding/crop; записать размер нужного объекта в пикселях на обоих этапах, размытие, перекрытия и доступность временного контекста. Ручная неразличимость — сигнал ограничения наблюдения, а не математическое доказательство невозможности для любой модели. Если различимость появляется только в исходнике, проверять input geometry раньше большого обучения; если требуется контекст вне изображения, уточнять постановку/камеру.
3. **Что загружено.** Хеши weights/config; class names и mapping; размер/цветовой порядок/нормализацию; формат boxes; inverse transforms; actual runtime; режим eval; confidence, NMS и max detections. Визуализировать GT и predictions на реальном входе после transforms. Неверное отображение labels/coordinates сначала исправляется как ошибка pipeline.
4. **На чём сравнивается.** Разделить рабочий материал для диагностики/доразметки/настройки и независимую оценку, сохранив camera/session/time provenance. Не разбивать соседние frames одной траектории случайно между train и validation. Разные часы одной камеры и новая камера отвечают на разные вопросы; оценка внутри камеры не доказывает перенос на новую.
5. **Какая ошибка повторяется.** Таблица объектов: class, TP/FP/FN, категория TIDE/ручного разбора, размер, камера, условия видимости, GT audit status. Таблица событий: event ID, interval, person/track, требуемый object evidence, правило, тревога, причина спорного решения. Число errors сопровождать denominators и покрытием; выборка только ошибок непригодна для оценки распространённости.
6. **Можно ли воспроизвести.** Сохранить сырые predictions до event logic, промежуточные связи/траектории, overlays, выбранные timestamps и решения аннотатора. Иначе изменение правила легко принять за улучшение detector.

Не задаём заранее число кадров: оно должно обеспечить представительство камер, условий, позитивов и негативов, которое допускают фактические данные и время ручной работы. Если редкое событие не встретилось, это отсутствие свидетельства о качестве, а не «нулевые ошибки».

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-02 — W1-02 — Предобучение, head-only/full fine-tuning, freeze и BatchNorm

<a id="f008"></a>

### F008 — [PAPER-MEASUREMENT; S007 §3.1, §4, Table 3]. TFA: Faster R-CNN, ResNet-101+FPN; сначала base detector, затем box classifier/regressor на balanced base+novel K-shot…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S007](SOURCES.md#s007). **Исходные IDs:** W1-02-F01, W1-03-F03.

**W1-02-F01: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F008 [PAPER-MEASUREMENT; S007 §3.1, §4, Table 3].** TFA: Faster R-CNN, ResNet-101+FPN; сначала base detector, затем box classifier/regressor на balanced base+novel K-shot instances, остальные feature-компоненты фиксированы. SGD batch16, momentum0.9, decay0.0001; LR0.02→0.001. COCO novel AP при 10/30 shots: full fine-tuning авторской реализации 9.2/12.5; TFA fc 10.0/13.4, cosine 10.0/13.7. Это objects, не независимые CCTV clips. Table3 — старый протокол; не смешивать с generalized Fig.5. В изученном фрагменте точные GPU, wall time и правило выбора checkpoint для этих строк не установлены.

**W1-03-F03: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F008 [PAPER/MEASURED-BY-AUTHORS, S007 Table 3, §4].** На COCO novel classes при 10/30 shots TFA cosine даёт nAP 10.0/13.7 против собственной FRCN full-finetuning baseline 9.2/12.5; nAP75 9.3/13.4 против 9.2/12.0. Это AP points, не относительные проценты, не AP50 и не event recall. Модель Faster R-CNN R101-FPN; статья сообщает SGD, batch 16, momentum 0.9, weight decay 0.0001, base LR 0.02 и few-shot LR 0.001. Эти цифры — авторский режим, не рекомендация для нашего trainer; RTX wall-clock/VRAM, перенос на LinQ и достаточность такого nAP не установлены. Table 3 относится к существующему протоколу, его нельзя смешивать с multi-sample generalized protocol Fig.4–5. Точный checkpoint-selection protocol для этого численного сравнения отдельно не восстановлен, поэтому числа не служат оценкой ожидаемого выигрыша команды.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f009"></a>

### F009 — [PAPER-PROTOCOL; S007 §4.2, Fig.5]. Revised protocol измеряет base и novel; COCO Fig.5 усредняет 10 random samples с 95% CI. Балансировка включает старые классы.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S007](SOURCES.md#s007). **Исходные IDs:** W1-02-F02, W1-03-F02, W1-15-F01.

**W1-02-F02: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F009 [PAPER-PROTOCOL; S007 §4.2, Fig.5].** Revised protocol измеряет base и novel; COCO Fig.5 усредняет 10 random samples с 95% CI. Балансировка включает старые классы. Поэтому результат не подтверждает сохранение всех старых знаний при обучении только новых классов; он также не даёт единого image budget для нашего кейса.

**W1-03-F02: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F009 [PAPER, S007 §4.2/Fig.3–4].** Авторы меняют случайный набор training shots и оценивают base AP, novel AP и общий AP. Fig.3 показывает cumulative mean и 95% CI по 40 repeated runs для novel classes первого VOC split, K=1/3/5/10; стабилизация около 30 — наблюдение конкретного benchmark. Fig.4 агрегирует 30 random samples. Это прежде всего вариативность выбора few-shot examples, а не только разных optimizer seeds. Универсального требования «всегда 30 прогонов» статья для CCTV не устанавливает.

**W1-15-F01: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: опубликованный протокол S007, не наш тест.** Для Faster R-CNN few-shot detection авторы меняют группы размеченных training shots, сообщают base AP, novel AP и overall AP. Revised benchmark усредняет 30 групп для PASCAL VOC и 10 для COCO; Appendix A задаёт half-width `1.96*s/sqrt(n)` для среднего. Fig.3 показывает нестабильность первых runs на VOC, Fig.4 — generalized evaluation по base и novel. Единица shot — размеченный экземпляр объекта, не независимая камера. Эти числа характеризуют протокол статьи; это не предписание запускать 30 наших trials. Здесь не заимствуются численные выигрыши TFA и не задаются compute, скорость или ожидаемый AP нашего CCTV. Протокол не устанавливает отдельно variance только от optimizer RNG.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f010"></a>

### F010 — [CODE; S008]. COCO all_10shot config явно задаёт backbone FREEZE, proposal generator FREEZE и ROI_HEADS.FREEZE_FEAT=True; GeneralizedRCNN.__init__ ставит…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S008](SOURCES.md#s008). **Исходные IDs:** W1-02-F03.

**W1-02-F03: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F010 [CODE; S008].** COCO all_10shot config явно задаёт backbone FREEZE, proposal generator FREEZE и ROI_HEADS.FREEZE_FEAT=True; GeneralizedRCNN.__init__ ставит requires_grad=False соответственно backbone, proposal_generator и roi_heads.box_head. Это оставляет обучение predictor, а не всего RoI feature head. Config: 80 classes, CosineSimOutputLayers, batch16, LR0.001, MAX_ITER160000, STEPS144000, checkpoint period10000; base config train min-size 640…800. Config содержит путь к `model_reset_combine.pth`, не просто произвольный COCO checkpoint. Историческая конфигурация не доказывает быстрое завершение на нашей машине. Поведение normalization всего дерева зависимостей этим чтением не установлено.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f011"></a>

### F011 — [PAPER-MEASUREMENT; S009 §5.2, Fig.7–8]. В Mask R-CNN R50-FPN+GroupNorm на 10k COCO images pretrained достиг 26.0 bbox AP при 60k iterations, scratch 25.9 при 220k;…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S009](SOURCES.md#s009). **Исходные IDs:** W1-02-F04.

**W1-02-F04: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F011 [PAPER-MEASUREMENT; S009 §5.2, Fig.7–8].** В Mask R-CNN R50-FPN+GroupNorm на 10k COCO images pretrained достиг 26.0 bbox AP при 60k iterations, scratch 25.9 при 220k; validation val2017, hyperparameters подобраны для pretrained и перенесены на scratch. При 1k images: текст даёт 9.9 против 3.5 AP; caption Fig.8 — 3.4 вместо 3.5, небольшое внутреннее расхождение сохраняем. Даже отдельный поиск scratch hyperparameters дал 5.4. Это показывает зависимость от data/compute и отсутствие универсального запрета scratch; не обосновывает scratch при нашем неизвестном малом наборе. На этой ветке classification pretraining исследовано как исторический контроль; лучший конкретный detection checkpoint для PPE не определён.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f012"></a>

### F012 — [PAPER/ABLATION; S010 §3.3.1, §4, Table4/Fig4]. DeFRCN обучает больше компонент Faster R-CNN, регулируя gradient flow, вместо жёсткого ограничения TFA. ResNet-101…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S010](SOURCES.md#s010). **Исходные IDs:** W1-02-F05.

**W1-02-F05: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F012 [PAPER/ABLATION; S010 §3.3.1, §4, Table4/Fig4].** DeFRCN обучает больше компонент Faster R-CNN, регулируя gradient flow, вместо жёсткого ограничения TFA. ResNet-101 ImageNet pretrained, SGD batch16, LR0.02 base/0.01 novel, momentum0.9, decay5e-5; RPN gradient coefficient0, RCNN0.75 base/0.01 novel. COCO Table4 plain FRCN novel AP10/30-shot 7.9/12.2; добавление GDL только в novel stage 15.2/19.0. Дополнительный PCB действует в inference. Это архитектурная абляция, не чистый спор «все веса против head при прочих равных», и не готовая YOLO-функция. Практический смысл: ограниченная адаптация backbone и head-only — разные проверяемые кандидаты; заморозка сама по себе не является законом few-shot detection.

### Фактическое поведение Ultralytics 8.4.184

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f013"></a>

### F013 — [CODE; S011 _setup_train, freeze block]. int `freeze=N` превращается в range(N); список используется напрямую; имена получают префикс `model.` и суффикс `.`. `.dfl`…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-02-F06.

**W1-02-F06: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F013 [CODE; S011 _setup_train, freeze block].** int `freeze=N` превращается в range(N); список используется напрямую; имена получают префикс `model.` и суффикс `.`. `.dfl` включён в always-freeze. Совпавшие параметры получают requires_grad=False; floating параметры вне маски, ранее False, получают True. Поэтому ручная предварительная заморозка может быть отменена trainer. Именованные подмодули допустимы через список, но соответствие архитектуре необходимо проверять.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f014"></a>

### F014 — [CODE; S011 _model_train, _do_train]. В начале эпохи _model_train вызывает model.train(), затем переводит совпавшие по freeze names nn.BatchNorm2d в eval().…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-02-F07.

**W1-02-F07: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F014 [CODE; S011 _model_train, _do_train].** В начале эпохи _model_train вызывает model.train(), затем переводит совпавшие по freeze names nn.BatchNorm2d в eval(). Следовательно, в этой версии обычная freeze-маска также фиксирует running statistics соответствующих BatchNorm2d. Это не утверждение обо всех версиях, SyncBatchNorm/custom normalization или пользовательских callbacks.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f015"></a>

### F015 — [CODE; S011 build_optimizer]. `optimizer=auto` выбирает optimizer/LR и явно игнорирует заданный lr0; порог iterations участвует в выборе. Для сравнения freeze/full…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-02-F08.

**W1-02-F08: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F015 [CODE; S011 build_optimizer].** `optimizer=auto` выбирает optimizer/LR и явно игнорирует заданный lr0; порог iterations участвует в выборе. Для сравнения freeze/full надо зафиксировать фактические optimizer, LR и budget либо признать сравнение полных recipes. Автоматически одинаковый CLI lr0 не гарантирует одинаковый optimizer setup.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f016"></a>

### F016 — [CODE; S012 BaseModel.load/_remap_cls_by_names]. Loader пересекает совместимые tensors; отдельно обрабатывает ширину hidden cls-веток при совместимых head inputs.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012). **Исходные IDs:** W1-02-F09.

**Уточнение W2 к исходному утверждению:** F191: class-row transfer — student; KD teacher target nc/names не получает. Different nc не обязательно shape failure для max-class weighting.

**W1-02-F09: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F016 [CODE; S012 BaseModel.load/_remap_cls_by_names].** Loader пересекает совместимые tensors; отдельно обрабатывает ширину hidden cls-веток при совместимых head inputs. Class-logit rows remap по strip/lower names, включая одинаковый nc с другим порядком; placeholder names исключены, несовместимая trailing shape пропускается. Изменение class count не означает сброс всей head. Предупреждается использование fused inference weights вместо unfused training checkpoint. Переименование класса по строке не проверяет совпадение его смысла.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f017"></a>

### F017 — [CODE; S013 DetectionTrainer.get_model]. Trainer строит DetectionModel с dataset nc/channels, устанавливает model names через set_model_names_for_load, затем…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S013](SOURCES.md#s013). **Исходные IDs:** W1-02-F10.

**W1-02-F10: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F017 [CODE; S013 DetectionTrainer.get_model].** Trainer строит DetectionModel с dataset nc/channels, устанавливает model names через set_model_names_for_load, затем вызывает model.load(weights). Проверять надо именно итоговую модель trainer после настройки, поскольку объект до train может иметь другой class contract.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f018"></a>

### F018 — [DOCS; S014]. BatchNorm2d имеет learnable affine gamma/beta и отдельно running estimates. При track_running_stats=True они обновляются во время train и используются…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S014](SOURCES.md#s014). **Исходные IDs:** W1-02-F11.

**W1-02-F11: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F018 [DOCS; S014].** BatchNorm2d имеет learnable affine gamma/beta и отдельно running estimates. При track_running_stats=True они обновляются во время train и используются в eval; при False batch statistics используются и в eval. Поэтому запрет градиента affine параметрам сам по себе не описывает режим статистик. Документация не устанавливает, какие statistics оптимальны для малой target CCTV-выборки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f019"></a>

### F019 — [VENDOR-GUIDANCE; S015]. Живой guide описывает freeze и последовательное обучение, но его советы о малом наборе не являются независимой абляцией. В нём `freeze=10`…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S015](SOURCES.md#s015). **Исходные IDs:** W1-02-F12.

**W1-02-F12: условия/наблюдение** ([ветка](_WORK/W1/02_FINETUNING.md)):

**F019 [VENDOR-GUIDANCE; S015].** Живой guide описывает freeze и последовательное обучение, но его советы о малом наборе не являются независимой абляцией. В нём `freeze=10` для YOLO26 оставляет последний backbone block trainable; полный backbone — `freeze=11`. Эти индексы нельзя переносить на другие YAML. Фраза guide об «only reliable» предотвращении forgetting через смешивание данных слишком сильна для общего вывода; наша рекомендация — измерять сохранение нужных старых классов, независимо от выбранного метода.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-03 — W1-03 — Few-shot detection и неполная разметка

<a id="f020"></a>

### F020 — [PAPER, S007 §3/3.1]. Синтетические few-shot VOC/COCO protocols используют одинаковое K аннотированных object instances на класс. TFA: сначала обычное обучение…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S007](SOURCES.md#s007). **Исходные IDs:** W1-03-F01.

**W1-03-F01: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F020 [PAPER, S007 §3/3.1].** Синтетические few-shot VOC/COCO protocols используют одинаковое K аннотированных object instances на класс. TFA: сначала обычное обучение Faster R-CNN на data-abundant base classes; затем сбалансированный набор base+novel с K shots каждого класса и обновление последних classification/regression layers при фиксированных backbone, RPN и RoI feature extractor. Наличие большого base-pretraining — содержательная предпосылка, не бесплатное следствие нескольких новых labels.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f021"></a>

### F021 — [DOC, S008 datasets/README.md]. VOC image-list для K-shot может содержать больше K instances; авторы дополнительно случайно выбирают K instances. Предоставлены 30…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S008](SOURCES.md#s008). **Исходные IDs:** W1-03-F04.

**W1-03-F04: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F021 [DOC, S008 datasets/README.md].** VOC image-list для K-shot может содержать больше K instances; авторы дополнительно случайно выбирают K instances. Предоставлены 30 groups для VOC, 10 для COCO; LVIS v0.5 balanced subset содержит до 10 instances каждого класса. README задаёт VOC2007+2012 trainval → VOC2007 test, 15 base/5 novel classes и три class splits; COCO2014 — 20 VOC-like novel/60 base, 5k held-out validation images, остальные train/val для training. Эти sampling groups не равны новым независимым камерам. В исходном FsDet старый стек: README перечисляет Linux/Python>=3.6, Detectron2 v0.2.1/v0.3/v0.4 с соответствующими tags. На нашей среде не установлен и не проверен. Авторский pipeline и веса доступны как зацепка, но портирование в выбранный YOLO trainer — отдельная задача model_stack.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f022"></a>

### F022 — [INFERENCE из F020/F021]. Benchmark может преднамеренно оставлять только K labels в изображениях, содержащих больше объектов. Это определяет опубликованную задачу,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S008](SOURCES.md#s008). **Исходные IDs:** W1-03-F05.

**W1-03-F05: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F022 [INFERENCE из F020/F021].** Benchmark может преднамеренно оставлять только K labels в изображениях, содержащих больше объектов. Это определяет опубликованную задачу, но не делает произвольную неполную разметку безопасной в production fine-tuning. Для CCTV не следует выбрасывать уже известные правильные boxes ради красивого K-shot числа: считать бюджет можно отдельно от полноты обучающего изображения. Отчёт должен хранить одновременно image_count, annotated_instance_count_per_class и независимые episode/track/camera counts; последние — предлагаемый учёт, не определение авторов TFA.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f023"></a>

### F023 — [PAPER, S016 §4.1–4.3/Algorithms 1–2]. В proposal-based detector используется per-RoI/per-category sigmoid classification с состоянием ignore для выбранных пар.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S016](SOURCES.md#s016). **Исходные IDs:** W1-03-F06.

**W1-03-F06: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F023 [PAPER, S016 §4.1–4.3/Algorithms 1–2].** В proposal-based detector используется per-RoI/per-category sigmoid classification с состоянием ignore для выбранных пар. Part-aware sampling игнорирует part-category classification loss внутри box subject, только если part-category отсутствует в verified categories данного изображения. Нужны verified positive/negative categories, subject boxes, mapping part→subject и spatial condition. Pseudo-label-guided sampling отбирает predictions вне verified categories, исключает overlap с GT и фильтрует по per-class thresholds, подобранным по precision на withheld set; отобранные регионы задают **ignore categories**, а не автоматически новые доказанные GT. Метод отличается от positive pseudo-label mining. Для каски/person это возможная гипотеза spatial prior, но у нас каска может быть в руке, на столе или вне person box; association и нарушение ношения таким prior не доказываются. Специальный loader/loss необходим; обычный YOLO text label не хранит все эти сведения.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f024"></a>

### F024 — [PAPER, S017 §3]. Для federated LVIS annotations авторы выбирают подмножество классов S: все positive categories плюс случайные negative categories, взвешенные…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S017](SOURCES.md#s017). **Исходные IDs:** W1-03-F07.

**W1-03-F07: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F024 [PAPER, S017 §3].** Для federated LVIS annotations авторы выбирают подмножество классов S: все positive categories плюс случайные negative categories, взвешенные square-root frequency. В опытах |S|=50; binary classification loss считается только на S. Это class subsampling, а не spatial поиск unannotated instances и не проверка отсутствия каждого sampled class. Механизм не является federated learning между устройствами. Если недоразмеченный объект относится к участвующему классу, сам факт subsampling не гарантирует исключения его false-negative penalty; отсутствие отдельного spatial решения принципиально.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f025"></a>

### F025 — [CODE, S018]. `sigmoid_cross_entropy_loss` строит one-hot GT по RoI, удаляет background column и умножает BCE на маску appeared classes от `get_fed_loss_inds`.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S018](SOURCES.md#s018). **Исходные IDs:** W1-03-F08.

**W1-03-F08: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F025 [CODE, S018].** `sigmoid_cross_entropy_loss` строит one-hot GT по RoI, удаляет background column и умножает BCE на маску appeared classes от `get_fed_loss_inds`. Helper включает `torch.unique(gt_classes)` и при нехватке добирает категории `torch.multinomial(..., replacement=False)` по frequency weights. В этом интерфейсе нет проверенной per-image positive/negative/unknown coverage map или spatial mask пропущенных объектов. Mask снижает набор classification columns; она не исправляет proposal assignment и не добавляет missing boxes. Режим inference вычисляет probabilities через sigmoid при `use_sigmoid_ce`; FedLoss sampling там не вызывается. При переходе от softmax trainer к sigmoid изменяется scoring convention — threshold заново валидируется, даже если сам loss является train-time. Это чтение кода, не исполнение.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f026"></a>

### F026 — [INFERENCE из F024/F025]. FedLoss нельзя рекомендовать как универсальный patch для PPE-набора с несколькими классами и random missing boxes. Число 50 из LVIS не…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S018](SOURCES.md#s018). **Исходные IDs:** W1-03-F09.

**W1-03-F09: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F026 [INFERENCE из F024/F025].** FedLoss нельзя рекомендовать как универсальный patch для PPE-набора с несколькими классами и random missing boxes. Число 50 из LVIS не переносится на маленький class vocabulary: в проверенном helper нет явного ограничения `num_sample_cats` величиной доступного C, а добор идёт без replacement. Несогласованные параметры могут запросить больше категорий, чем есть; конкретный runtime error не проверялся. Даже корректно уменьшенный subset не превращает unknown в verified negatives и не решает пропуск второго объекта уже positive class. До выбора такой ветки нужны настоящий C, flags, loss/assignment audit и E007.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f027"></a>

### F027 — [PAPER, S019 p.1–3]. SAOD означает missing instances внутри annotated image; обычная SSOD-постановка — немного fully labeled images плюс полностью unlabeled images.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S019](SOURCES.md#s019). **Исходные IDs:** W1-03-F10.

**W1-03-F10: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F027 [PAPER, S019 p.1–3].** SAOD означает missing instances внутри annotated image; обычная SSOD-постановка — немного fully labeled images плюс полностью unlabeled images. Co-mining обменивает mined pseudo-positive labels между двумя views с общими весами. Авторы прямо описывают две branches в training и одну в inference; это их утверждение об architecture, а не измеренная нами скорость. Оно не распространяется автоматически на все sparse methods или на чужую реализацию. Достаточность pseudo-label precision и риски confirmation bias передаются W1-09.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f028"></a>

### F028 — [PAPER, S020 §4.2/4.3/4.6.1]. SparseDet объединяет features двух views для common RPN, выделяет pseudo-positive regions и использует self-supervision. §4.3…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S020](SOURCES.md#s020). **Исходные IDs:** W1-03-F11.

**W1-03-F11: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F028 [PAPER, S020 §4.2/4.3/4.6.1].** SparseDet объединяет features двух views для common RPN, выделяет pseudo-positive regions и использует self-supervision. §4.3 описывает inference с backbone features original+augmented для RoIs, final detections — по original features. §4.6.1 убирает augmentation, но region proposals всё ещё генерирует C-RPN. Поэтому фраза «это только loss modification, обычный detector можно экспортировать без изменений» не подтверждается. Article Table 6 на COCO Split-1 при 70% removal сообщает AP 32.68 с augmented inference / 32.67 без него: это абляция внутри SparseDet, не доказательство parity обычного Faster R-CNN, скорости или экспорта. Опубликованный режим R101-FPN/Detectron2, batch 8; on COCO 270000 iterations, VOC 18000; не измерены wall-clock команды и LinQ feasibility.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f029"></a>

### F029 — [PAPER/DOC, S020 §4.2 и README]. SparseDet различает class-aware удаление annotations по dataset, class-aware удаление категорий внутри image и class-agnostic…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S020](SOURCES.md#s020). **Исходные IDs:** W1-03-F12.

**W1-03-F12: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F029 [PAPER/DOC, S020 §4.2 и README].** SparseDet различает class-aware удаление annotations по dataset, class-aware удаление категорий внутри image и class-agnostic удаление boxes внутри image. Одинаковые «70% missing» не задают одинаковую learning problem. В тексте есть несогласованность: описание Split-2 допускает images без labels, последующее обсуждение говорит, что Splits-2/3 сохраняют минимум одну annotation; проценты в narrative сравнений также расходятся с Table 1. Здесь не выбираем удобную трактовку: точное содержимое split необходимо проверять по manifests. README указывает Python 3.6.15, torch1.10.1+cu111/torchvision0.11.2+cu111, Detectron2 wheel channel и пример на 4 GPU. Version Detectron2 package в строке install не pinned; это риск воспроизведения. Ссылка на Google Drive splits существует, архивы и зависимости не получены, training не запущен. Не выдавать команды автора за проверенный recipe команды.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f030"></a>

### F030 — [INFERENCE из F022, F023, F024, F025, F026, F027, F028, F029]. Нижеследующая таблица — наша схема данных/решений, а не готовая спецификация конкретного trainer. Её…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-03-F13.

**Уточнение W2 к исходному утверждению:** F194–F205: U loader/assignment/BCE/regression/E2E trace. Hidden class B и hidden instance C различны; MMDet default/zero-GT ограничения.

**W1-03-F13: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F030 [INFERENCE из F022, F023, F024, F025, F026, F027, F028, F029].** Нижеследующая таблица — наша схема данных/решений, а не готовая спецификация конкретного trainer. Её цель — не потерять unknown при преобразовании разнородных источников.

| Состояние source/image/class | Что известно | Чего label не доказывает | Условный путь |
|---|---|---|---|
| Exhaustive для оговорённых классов/ROI/размеров | Все допустимые видимые экземпляры перечислены по policy | Полноту вне ROI, для tiny/occluded/других классов | Обычный supervised loss в пределах policy, единый class mapping |
| Verified absent class | Человек/источник проверил отсутствие в оговорённой области | Отсутствие по умолчанию в кадре без боксов | Разрешить negative loss для подтверждённого class/ROI |
| Verified present + exhaustive instances данного класса | Класс есть, его instances перечислены | Исчерпывающую разметку других classes | Class-aware loss/отдельная задача либо доразметка остальных |
| Positive image label без boxes | Где-то есть класс | Локализацию, число instances, negative регионы | Image-supervised метод с отдельной поддержкой; не подставлять как bbox GT |
| Sparse boxes одного/нескольких классов | Boxes подтверждают конкретные positives | Что остальные регионы — background, даже для того же класса | Доразметка или проверенный spatial ignore/mining/assignment-aware метод |
| Source никогда не размечал класс | Unknown для этого source | Verified absent в каждом его изображении | Preserve source×class coverage; masked training, separate model/task или доразметка |
| Пустой label-файл, provenance неизвестен | Нет записанных boxes | Negative scene; fully reviewed image | Quarantine/audit; не отправлять автоматически как hard negative |
| Ignore/crowd/неразличимый регион | Policy ограничивает достоверное решение | Корректный negative внутри региона | Передать геометрию ignore и её поддержку в loader/assignment/loss/evaluator |

Минимальный manifest: source/version, image/camera/session/episode IDs, timestamp, class mapping и определение класса; для class — present/verified_absent/unknown, instance coverage exhaustive/sparse/unknown, annotation ROI и ignore regions, ограничения размера/видимости, способ верификации. Это предложенные поля; простой bbox export может их потерять. Class-absent source и случайно пропущенный box внутри размечаемого класса требуют разных масок. Сохранение только `class_names` не решает эту проблему.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f031"></a>

### F031 — [INFERENCE]. Пример условный: source A содержит только person boxes, source B — только helmet boxes. Простое слияние и общий closed-world loss могут обучать helmet…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-03-F14.

**W1-03-F14: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F031 [INFERENCE].** Пример условный: source A содержит только person boxes, source B — только helmet boxes. Простое слияние и общий closed-world loss могут обучать helmet как negative в A и person как negative в B. Полезные варианты: доразметить небольшой согласованный subset для всех нужных classes; использовать trainer с проверенной coverage-aware поддержкой; либо сохранить отдельные задачи/модели с проверяемым association. Вариант выбирается по сложности и target quality; separate models меняют integration/inference cost и не имеют установленной поддержки LinQ. Отсутствие helmet detection не превращается в GT «нарушение»: видимость и связь с человеком относятся к violation_methods.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f032"></a>

### F032 — [INFERENCE из F020, F009, F008, F021, F022 и W1-01]. Число labels отчётно следует разложить на изображения, boxes per class, независимые physical episodes/people…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-03-F15.

**W1-03-F15: условия/наблюдение** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):

**F032 [INFERENCE из F020, F009, F008, F021, F022 и W1-01].** Число labels отчётно следует разложить на изображения, boxes per class, независимые physical episodes/people tracks, камеры/сессии и условия. Число людей не всегда известно и не должно выдумываться. Повторяющиеся views допустимы в training, но не должны проходить через независимый assessment split одной траектории. Сохранять ontology base/novel/known-but-new-domain: если нужный смысл уже есть в weights, это domain adaptation, а не обязательно novel-class discovery.

Базовый контролируемый набор кандидатов — unchanged weights (если нужные классы присутствуют), head-only/частичный fine-tuning, full fine-tuning, либо дополнение качественной разметки с тем же trainer. Точный список trainable tensors устанавливается в W1-02/model_stack; TFA «последний predictor» не равен произвольному `freeze` N слоёв YOLO. Если меняется cosine head, class cardinality, input или cascade, нужно вновь проверять output/export contract. Sample-set seed и optimization seed фиксировать раздельно; сравнивать кандидатов на одних и тех же labeled subsets. Если выигрыш меняет знак при другой независимой группе examples, нельзя продавать его как устойчивое улучшение.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-04 — W1-04 — редкие классы, sampling и hard negatives

<a id="f033"></a>

### F033 — paper measurement. LVIS v0.5, Mask R-CNN ResNet-50-FPN с ImageNet pretraining; train v0.5 (~57k изображений), validation v0.5; mask AP, не box AP. Table 3b,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S021](SOURCES.md#s021). **Исходные IDs:** W1-04-F01.

**W1-04-F01: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F033 — paper measurement.** LVIS v0.5, Mask R-CNN ResNet-50-FPN с ImageNet pretraining; train v0.5 (~57k изображений), validation v0.5; mask AP, не box AP. Table 3b, среднее±SD пяти запусков: без resampling AP **21.0±0.17**, AP_r **3.2±0.35**, AP_f **27.7±0.12**; RFS `t=0.001`: **23.2±0.21 / 13.4±0.80 / 27.1±0.07**. CAS: **18.7±0.46 / 8.5±1.56 / 22.3±0.19**. Больший `t=0.01`: AP **21.8±0.25**, AP_r **9.8±1.27**. Значит, усиление балансировки не давало монотонного выигрыша.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f034"></a>

### F034 — paper protocol. B.1–B.2: SGD, batch16, 90k updates (60k/20k/10k при LR .02/.002/.0002), momentum .9, weight decay .0001, warmup1000, короткая сторона800, horizontal…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S021](SOURCES.md#s021). **Исходные IDs:** W1-04-F02.

**W1-04-F02: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F034 — paper protocol.** B.1–B.2: SGD, batch16, 90k updates (60k/20k/10k при LR .02/.002/.0002), momentum .9, weight decay .0001, warmup1000, короткая сторона800, horizontal flip, без TTA; Table 3b сохраняет score threshold0 и max300 detections/image. GPU и правило выбора checkpoint здесь не установлены. Отдельный label budget отсутствует: полный train release.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f035"></a>

### F035 — paper observation / our caution. Table 3a отдельно меняет inference threshold и лимит detections; эти изменения нельзя записывать как эффект sampling. В тексте B.2…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S021](SOURCES.md#s021), [S022](SOURCES.md#s022). **Исходные IDs:** W1-04-F03.

**W1-04-F03: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F035 — paper observation / our caution.** Table 3a отдельно меняет inference threshold и лимит detections; эти изменения нельзя записывать как эффект sampling. В тексте B.2 есть перевёрнутое неравенство относительно порога; формула и код S022 задают oversampling при `f_c<t`. Не копировать ошибочную прозу как рецепт.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f036"></a>

### F036 — code reading. Частота `f_c` — доля изображений, содержащих хотя бы одну annotation класса; несколько экземпляров в кадре считаются один раз. По умолчанию…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S022](SOURCES.md#s022). **Исходные IDs:** W1-04-F04.

**W1-04-F04: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F036 — code reading.** Частота `f_c` — доля изображений, содержащих хотя бы одну annotation класса; несколько экземпляров в кадре считаются один раз. По умолчанию `sqrt=True`: `r_c=max(1,sqrt(t/f_c))`; image factor — максимум классов кадра, для пустого изображения1. Stochastic rounding реализует дробные повторы в ожидании; размер очередного «epoch» меняется. Distributed slicing делит общий поток между rank. Параметр меняет обучение, не inference graph.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f037"></a>

### F037 — code reading / our calculation. Докстрока «frequency half threshold → repeated twice» неверна при default sqrt: формула даёт `sqrt(2)`, а2 получается при `f=t/4`.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S022](SOURCES.md#s022). **Исходные IDs:** W1-04-F05.

**W1-04-F05: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F037 — code reading / our calculation.** Докстрока «frequency half threshold → repeated twice» неверна при default sqrt: формула даёт `sqrt(2)`, а2 получается при `f=t/4`. Реальный код важнее этой фразы. `t` нужно выбирать после просмотра фактической частоты; LVIS `.001` для малого набора может вообще ничего не повторить. Отсутствующий класс не появляется в `category_freq`.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f038"></a>

### F038 — code reading. `DATALOADER.SAMPLER_TRAIN="RepeatFactorTrainingSampler"` выбирает RFS через loader; defaults `REPEAT_THRESHOLD=0.0`, `REPEAT_SQRT=True`.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S023](SOURCES.md#s023). **Исходные IDs:** W1-04-F06.

**W1-04-F06: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F038 — code reading.** `DATALOADER.SAMPLER_TRAIN="RepeatFactorTrainingSampler"` выбирает RFS через loader; defaults `REPEAT_THRESHOLD=0.0`, `REPEAT_SQRT=True`. `FILTER_EMPTY_ANNOTATIONS=True` по умолчанию, и loader применяет фильтр изображений без не-crowd instances. Для mining настоящих пустых кадров необходимо проверить, что они не исчезли до sampler. Доступны также dataset weights и `WeightedCategoryTrainingSampler`: последняя перемножает dataset- и category-repeat factors. Название не означает CAS из LVIS. IterableDataset имеет другую ветку и не получает этот sampler автоматически.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f039"></a>

### F039 — method / paper measurement. Focal loss умножает CE на `(1-p_t)^gamma`, подавляя лёгкие примеры; исходная мотивация — foreground/background dense detection.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S024](SOURCES.md#s024). **Исходные IDs:** W1-04-F07.

**W1-04-F07: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F039 — method / paper measurement.** Focal loss умножает CE на `(1-p_t)^gamma`, подавляя лёгкие примеры; исходная мотивация — foreground/background dense detection. RetinaNet R50-FPN, ImageNet initialization, COCO trainval35k (~115k train images), minival5k, scale600: Table1, balanced CE31.1 AP, focal34.0 AP, выигрыш2.9 AP; `gamma=2`, `alpha=.25` (alpha подбирали для каждого gamma). 90k SGD updates, batch16 на8 GPU, LR.01 со снижением60k/80k, momentum.9, WD.0001, horizontal flips; prior foreground probability.01 при initialization. Это box COCO AP; полного отдельного малого label budget нет. Конкретный checkpoint-selection rule не установлен. Результат не доказывает исправление class-to-class long tail в любой YOLO.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f040"></a>

### F040 — code reading. `get_class_counts` считает экземпляры из train labels, не изображения или события. Для присутствующего класса вес `(1/count)^cls_pw`, нормируется к…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S013](SOURCES.md#s013). **Исходные IDs:** W1-04-F08.

**W1-04-F08: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F040 — code reading.** `get_class_counts` считает **экземпляры** из train labels, не изображения или события. Для присутствующего класса вес `(1/count)^cls_pw`, нормируется к среднему1; `cls_pw` ограничен `[0,1]`,0 отключает вычисление. Отсутствующий класс получает средний предварительный вес, после normalization1, а не бесконечность. При отсутствии всех counts функция возвращается. Веса устанавливаются на модель, при distillation — на `student_model`. Это доступный training mechanism, не доказательство улучшения и не подтверждение наличия в старом локальном релизе.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f041"></a>

### F041 — code reading. `v8DetectionLoss` создаёт `BCEWithLogitsLoss(reduction="none")`. `class_weights` имеет broadcast shape `(1,1,nc)` и умножает BCE до суммирования и…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S025](SOURCES.md#s025). **Исходные IDs:** W1-04-F09.

**W1-04-F09: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F041 — code reading.** `v8DetectionLoss` создаёт `BCEWithLogitsLoss(reduction="none")`. `class_weights` имеет broadcast shape `(1,1,nc)` и умножает BCE до суммирования и деления на `target_scores_sum`. Поэтому вес класса усиливает **всю его BCE-компоненту, включая отрицательные target entries**, а не только rare positives. `FocalLoss(gamma=1.5,alpha=.25)` существует отдельно; из этого не следует включённый focal loss в прочитанном detection criterion. `dfl` относится к bbox loss. Подменять BCE focal-модулем без проверки reduction/soft targets/normalization — отдельное изменение кода.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f042"></a>

### F042 — code reading. И пустой label file, и отсутствующий label file превращаются в пустой массив labels; счётчики `ne`/`nm` различаются. Это не проверка реального…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S026](SOURCES.md#s026). **Исходные IDs:** W1-04-F10, W1-12-F08.

**W1-04-F10: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F042 — code reading.** И пустой label file, и отсутствующий label file превращаются в пустой массив labels; счётчики `ne`/`nm` различаются. Это не проверка реального отсутствия объектов. **Our inference:** случайно потерянная annotation и проверенный background проходят этот участок с одинаковой пустой разметкой. Для hard-negative pool требуется явный provenance/статус проверки, а не только наличие пустого txt.

**W1-12-F08: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S026. verify_image_label для detect проверяет five-column rows, нормализацию с 1% tolerance, допустимые class IDs и integer labels; missing, empty, corrupt фиксируются отдельно. Missing/empty annotations могут стать пустым label array, а не fatal error. Текущий dataset cache version=1.0.12, но совпадение версии cache не подтверждает корректность данных.

Тип: вывод. Успешный scan не доказывает отсутствие пропущенных объектов, правильность helmet/no_helmet, пары image-label, независимость камер и корректность boxes после crops/augmentation. Для отрицательного кадра нужны условия annotation coverage. Исправления labels должны сопровождаться проверкой реального прочтения новых данных и cache invalidation, а не предположением, что trainer всё заметил.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f043"></a>

### F043 — method / paper measurement. OHEM выбирает наиболее loss-heavy RoIs, включая foreground и background, внутри Fast R-CNN; это не offline сбор только negative кадров.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S027](SOURCES.md#s027). **Исходные IDs:** W1-04-F11.

**W1-04-F11: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F043 — method / paper measurement.** OHEM выбирает наиболее loss-heavy **RoIs**, включая foreground и background, внутри Fast R-CNN; это не offline сбор только negative кадров. Для устранения коррелированных областей авторы делают loss-based NMS с IoU.7. VGG16, VOC2007 trainval→test, single scale, bbox regression: reproduced baseline67.2→69.9 mAP (Table3). SGD80k, LR.001, decay×.1 каждые30k, N2 images/B128 RoIs; отдельного малого label budget нет. В §5.1 preprocessing отослан к Fast R-CNN defaults; полностью здесь не восстановлен. Точное GPU и checkpoint-selection rule не установлены. Применимость к современному YOLO и стоимость интеграции не подтверждены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f044"></a>

### F044 — paper method, без переноса чисел. EQLv2 рассматривает положительные и отрицательные градиенты каждого классификатора отдельно; накопленное отношение задаёт разные…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S028](SOURCES.md#s028). **Исходные IDs:** W1-04-F12.

**W1-04-F12: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F044 — paper method, без переноса чисел.** EQLv2 рассматривает положительные и отрицательные градиенты каждого классификатора отдельно; накопленное отношение задаёт разные веса positives/negatives. Авторы подчёркивают, что одно количество примеров не определяет баланс градиентов: много лёгких негативов могут влиять меньше нескольких трудных позитивов. Это содержательно отличается от единственного множителя всей class BCE в F041. Метод — кандидат при диагностированном gradient imbalance; здесь не восстановлен его полный репликационный путь, поэтому численные выигрыши abstract не используются как основание назначения нам.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f045"></a>

### F045 — our inference: четыре счётчика до любой балансировки. Нужна таблица `class × {source,camera,session,episode}` с image count, instance count, independent positive…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S013](SOURCES.md#s013), [S022](SOURCES.md#s022). **Исходные IDs:** W1-04-F13.

**W1-04-F13: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F045 — our inference: четыре счётчика до любой балансировки.** Нужна таблица `class × {source,camera,session,episode}` с image count, instance count, independent positive group count и длительностью нормального материала. Десять объектов одного класса в одном кадре изменят S013 weights, но почти не изменят S022 RFS; соседние кадры одного эпизода могут изменить оба, не добавляя разнообразия. Показать гистограммы исходного набора и фактического sampled stream. Выбор group-aware sampler вместо RFS — наша гипотеза, не встроенная подтверждённая возможность прочитанного trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f046"></a>

### F046 — our inference: цена false alarms. Обогащённая positive training distribution может быть полезна для обучения, но не задаёт рабочую prevalence. На потоке с редкими…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-04-F14.

**W1-04-F14: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F046 — our inference: цена false alarms.** Обогащённая positive training distribution может быть полезна для обучения, но не задаёт рабочую prevalence. На потоке с редкими событиями даже небольшой FP rate может давать много тревог. Поэтому рядом с rare-class AP/recall нужны FP на отрицательный frame и, после неизменной логики объединения, false alarms per camera-hour, длительность просмотренного normal footage и event recall с числом независимых событий. Нельзя доказать приемлемость тревог тестом, искусственно поровну набранным из positives/negatives. Ноль FP на коротком видео не устанавливает нулевую частоту ложных тревог.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f047"></a>

### F047 — our inference: hard-negative loop без отравления supervision. Mining-пул берётся из разрешённого train/adaptation материала. Для каждой находки фиксируется…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-04-F15.

**W1-04-F15: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F047 — our inference: hard-negative loop без отравления supervision.** Mining-пул берётся из разрешённого train/adaptation материала. Для каждой находки фиксируется predicted class/score, frame/time, камера/эпизод и человек проверяет весь кадр по полной рабочей таксономии. Настоящие positives получают boxes; неоднозначное/невидимое состояние не объявляется negative. Нельзя оставить в полноразмерном кадре другие видимые рабочие классы без labels, чтобы «наказать только эту FP». Если loader не поддерживает ignore/partial labels, доразметить кадр либо исключить его. Сохранять отдельно look-alike negatives и обычный фон, распределять quota по причинам, ограничивать повторы одного эпизода; параллельно сохранять позитивный rehearsal-набор. Рост уверенного FP может требовать знания зоны/связи с человеком/времени, которое этот single-frame loss не даёт.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f048"></a>

### F048 — our inference: сравнение по бюджету. При sampling «одинаковые epochs» могут означать разное число optimizer updates/показанных изображений. Сопоставить…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-04-F16.

**W1-04-F16: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F048 — our inference: сравнение по бюджету.** При sampling «одинаковые epochs» могут означать разное число optimizer updates/показанных изображений. Сопоставить фиксированный update/image-exposure budget; отдельно записать wall-clock и повторную экспозицию каждому классу/группе. Если sampler меняет число итераций и schedule, различие качества нельзя приписать одной балансировке. Сначала пробовать одно вмешательство: sampling **или** weights **или** negatives. Их комбинация может быть полезна, но скрывает причину и может дважды усилить один noisy rare example.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f049"></a>

### F049 — our inference: inference/export. RFS/offline mining меняют данные обучения; прочитанные weights/FocalLoss относятся к training criterion. Они сами не требуют новой…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-04-F17.

**W1-04-F17: условия/наблюдение** ([ветка](_WORK/W1/04_IMBALANCE.md)):

**F049 — our inference: inference/export.** RFS/offline mining меняют данные обучения; прочитанные weights/FocalLoss относятся к training criterion. Они сами не требуют новой архитектуры детектора. Но checkpoint, фактический exporter и граф после export всё равно нужно проверить, а inference на LinQ остаётся отдельным неизвестным. Успех обучения/ONNX не доказывает LinQ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-05 — W1-05 — Аугментации промышленных камер

<a id="f050"></a>

### F050 — code/config observation, S029. Буквальные значения pinned default.yaml:

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S029](SOURCES.md#s029). **Исходные IDs:** W1-05-F01.

**W1-05-F01: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F050 — code/config observation, S029.** Буквальные значения pinned default.yaml:

```yaml
hsv_h: 0.015
hsv_s: 0.7
hsv_v: 0.4
degrees: 0.0
translate: 0.1
scale: 0.5
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.5
bgr: 0.0
mosaic: 1.0
mixup: 0.0
cutmix: 0.0
copy_paste: 0.0
copy_paste_mode: flip
close_mosaic: 10
rect: False
multi_scale: 0.0
auto_augment: randaugment
erasing: 0.4
```

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f051"></a>

### F051 — interpretation of config, S029/S030. Не все числа — probabilities: degrees/shear — углы, translate — доля сдвига, scale — диапазон масштаба относительно единицы;…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S029](SOURCES.md#s029), [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F02.

**W1-05-F02: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F051 — interpretation of config, S029/S030.** Не все числа — probabilities: degrees/shear — углы, translate — доля сдвига, scale — диапазон масштаба относительно единицы; `copy_paste` связан с долей eligible objects. Последние два параметра блока (`auto_augment`, `erasing`) предназначены classification; нельзя выдавать `erasing=0.4` за включённую bbox-окклюзию. Эти defaults не измерение и не recommendation optimum. `multi_scale` — отдельный параметр изменения размеров обучения; его нельзя незаметно добавить в тест фотометрии.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f052"></a>

### F052 — code observation, S030/v8_transforms. Порядок: pre-transform mosaic/affine и copy-paste, затем MixUp, CutMix, Albumentations, HSV, vertical/horizontal flips.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F03.

**W1-05-F03: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F052 — code observation, S030/v8_transforms.** Порядок: pre-transform mosaic/affine и copy-paste, затем MixUp, CutMix, Albumentations, HSV, vertical/horizontal flips. Поэтому отдельные изменения не независимы от оставленного pre-transform; для чистой ablation необходимо зафиксировать остальную цепочку. Здесь не проверялся tensor graph экспортера: это pipeline training data, что само по себе не добавляет операцию аугментации к inference, но не доказывает поддержку модели на LinQ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f053"></a>

### F053 — code observation, S030/Albumentations. При наличии optional библиотеки default extra list: Blur/MedianBlur/ToGray/CLAHE по `p=0.01`; RandomBrightnessContrast,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F04.

**W1-05-F04: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F053 — code observation, S030/Albumentations.** При наличии optional библиотеки default extra list: Blur/MedianBlur/ToGray/CLAHE по `p=0.01`; RandomBrightnessContrast, RandomGamma и ImageCompression по `p=0.0` (у последнего задан `quality_range=(75,100)`). Custom list заменяет именно этот список, сохраняя другие операции Ultralytics. Spatial transforms распознаются рекурсивно через DualTransform/BaseCompose; bbox поля: `format="yolo"`, `label_fields=["class_labels","idx"]`. ImportError пропускается; другие ошибки initialization логируются. Значит, config и успешное обучение ещё не подтверждают наличие нужной операции: сохранить версии, startup log и фактические samples. Наличие лишь минимальной version check 1.0.3 не доказывает совместимость любой более новой библиотеки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f054"></a>

### F054 — code observation, S030/RandomPerspective.box_candidates. После преобразования и clipping фильтр detection требует ширину и высоту строго больше 2 px, отношение…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F05.

**W1-05-F05: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F054 — code observation, S030/RandomPerspective.box_candidates.** После преобразования и clipping фильтр detection требует ширину и высоту строго больше 2 px, отношение площадей new/old строго больше 0.10, aspect ratio строго меньше 100. Для сегментов используется area threshold 0.01. Это геометрический фильтр, а не оценка видимости СИЗ/состояния. Маленькие сигареты/части лица могут систематически выпадать после scale/crop; нужен счётчик survival по классам и исходным размерам, а не только visual mosaic.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f055"></a>

### F055 — code observation, S030/CopyPaste.__call__. При `len(instances.segments)==0` или p==0 операция возвращает исходные labels. У bbox-only detect изменение `copy_paste`…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F06, W1-11-F14.

**W1-05-F06: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F055 — code observation, S030/CopyPaste.__call__.** При `len(instances.segments)==0` или p==0 операция возвращает исходные labels. У bbox-only detect изменение `copy_paste` поэтому не создаёт полноценный paste. Перенос по маске требует segments/соответствующей подготовки. Даже корректный mask не даёт автоматической семантики ношения. Самостоятельный bbox-rectangle paste — уже другой метод со своей проверкой, не свойство этого флага.

**W1-11-F14: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F055 — переданный code observation соседней ветки.** В [W1-05](_WORK/W1/05_AUGMENTATION.md), F135, Ultralytics `8.4.184`, SHA `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, `ultralytics/data/augment.py:CopyPaste.__call__`: при отсутствии segments операция возвращает исходные labels. В этой ветке код повторно не исполнялся. Bbox-only dataset + `copy_paste` flag не реализует методы F131/F137; требуются masks/подготовка или иной явно реализованный compositor.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f056"></a>

### F056 — code observation, S030/MixUp/CutMix. MixUp использует Beta(32,32) для смешивания. CutMix выбирает область без перекрытия destination boxes; source selection требует…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S030](SOURCES.md#s030). **Исходные IDs:** W1-05-F07.

**W1-05-F07: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F056 — code observation, S030/MixUp/CutMix.** MixUp использует Beta(32,32) для смешивания. CutMix выбирает область без перекрытия destination boxes; source selection требует достаточную долю объекта внутри области (0.1 для boxes, 0.01 при segments). Эти эвристики не валидируют взаимодействие человека, СИЗ и опасной зоны. Отсутствие пересечения bounding boxes не означает физическую корректность сцены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f057"></a>

### F057 — code observation, S031. `rect=True` в YOLODataset.build_transforms обнуляет mosaic/mixup/cutmix; `close_mosaic` обнуляет mosaic/copy_paste/mixup/cutmix и…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S031](SOURCES.md#s031). **Исходные IDs:** W1-05-F08.

**W1-05-F08: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F057 — code observation, S031.** `rect=True` в YOLODataset.build_transforms обнуляет mosaic/mixup/cutmix; `close_mosaic` обнуляет mosaic/copy_paste/mixup/cutmix и перестраивает transforms. При сравнении поздних эпох это несколько операций, а не одно изменение mosaic. Сохранить фактически resolved configuration и epoch schedule.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f058"></a>

### F058 — documentation claim, S032. Руководство предлагает учитывать постоянство точки обзора и допустимость частичных объектов при выборе геометрии/mosaic. Оно также…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S032](SOURCES.md#s032). **Исходные IDs:** W1-05-F09.

**W1-05-F09: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F058 — documentation claim, S032.** Руководство предлагает учитывать постоянство точки обзора и допустимость частичных объектов при выборе геометрии/mosaic. Оно также описывает custom Albumentations через Python API. Это рекомендации разработчика библиотеки, без измерения пользы на нашем CCTV. Команда должна связать их с последующими E-ID.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f059"></a>

### F059 — code observation, S033. Для Albumentations 2.0.8 правильные имена — `BboxParams(format=..., clip=...)`. Defaults `min_area=min_visibility=min_width=min_height=0.0`,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S033](SOURCES.md#s033). **Исходные IDs:** W1-05-F10.

**W1-05-F10: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F059 — code observation, S033.** Для Albumentations 2.0.8 правильные имена — `BboxParams(format=..., clip=...)`. Defaults `min_area=min_visibility=min_width=min_height=0.0`, `check_each_transform=True`, `clip=False`, `filter_invalid_bboxes=False`, `max_accept_ratio=None`. `label_fields` связывает labels с удаляемыми boxes. В `filter_bboxes` clipping выполняется перед проверками площади/размеров; площадь и размер считаются в пикселях по shape. Default аргументы самой helper-функции для min_width/min_height равны 1.0, а BboxParams передаёт свои 0.0: нельзя смешивать эти defaults.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f060"></a>

### F060 — inference from S033, not measurement. `min_visibility` фильтрует по геометрии конкретной операции: обычное clipping сравнивает площадь clipped bbox с bbox до…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S033](SOURCES.md#s033). **Исходные IDs:** W1-05-F11.

**W1-05-F11: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F060 — inference from S033, not measurement.** `min_visibility` фильтрует по геометрии конкретной операции: обычное clipping сравнивает площадь clipped bbox с bbox до clipping, а не распознаёт, видна ли каска за человеком. Это доля bbox, не confidence правильности класса. `filter_invalid_bboxes` и clip не заменяют исправление аннотаций: тихое удаление дефектных labels меняет распределение редких классов. Логировать до/после и причину каждого удаления; число удалённых объектов отдельно от числа кадров без labels.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f061"></a>

### F061 — docs observation, S034. Live reference использует `coord_format`, `clip_bboxes_on_input`, `clip_after_transform` и расширенные targets. Это не signature 2.0.8. Не…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S034](SOURCES.md#s034). **Исходные IDs:** W1-05-F12.

**W1-05-F12: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F061 — docs observation, S034.** Live reference использует `coord_format`, `clip_bboxes_on_input`, `clip_after_transform` и расширенные targets. Это не signature 2.0.8. Не копировать live snippet в pinned env без сверки; не объявлять текущую major version сайта установленной. Наличие transform в общей таблице означает поддержку типа target в этой библиотеке, но не интеграцию каждого target в конкретный trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f062"></a>

### F062 — code observation, S035. В pinned Alb 2.0.8 ImageCompression — ImageOnlyTransform с JPEG/WebP (`compression_type="jpeg"` по умолчанию), `quality_range=(99,100)`,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S035](SOURCES.md#s035). **Исходные IDs:** W1-05-F13.

**W1-05-F13: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F062 — code observation, S035.** В pinned Alb 2.0.8 ImageCompression — ImageOnlyTransform с JPEG/WebP (`compression_type="jpeg"` по умолчанию), `quality_range=(99,100)`, `p=0.5`; RandomBrightnessContrast также image-only; MotionBlur существует и строит направленный blur. Имена можно использовать в custom Python transform list после smoke-check. JPEG/WebP не являются точной моделью временной деградации H.264/H.265: для CCTV сохранять реальные decoded frames и codec/bitrate metadata, если доступны. Последнее — инженерное ограничение применимости, не измерение эквивалентности кодеков.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f063"></a>

### F063 — code observation, S036. CoarseDropout наследует BaseDropout; bbox handling через `filter_bboxes_by_holes` использует min_area/min_visibility bbox processor. Таким…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S036](SOURCES.md#s036). **Исходные IDs:** W1-05-F14.

**W1-05-F14: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F063 — code observation, S036.** CoarseDropout наследует BaseDropout; bbox handling через `filter_bboxes_by_holes` использует min_area/min_visibility bbox processor. Таким образом, blanket утверждение «dropout никогда не меняет targets» для 2.0.8 неверно. Но даже survival по площади не гарантирует сохранение visual evidence конкретного PPE-состояния. Удаление helmet box не превращает соответствующий person в `no_helmet` автоматически.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f064"></a>

### F064 — published measurement, S037 §§2.1–2.2/3.3 Table2, не наш тест. Faster R-CNN R50-FPN, COCO train2017 → val2017, полная доступная instance-разметка, не few-shot…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S037](SOURCES.md#s037). **Исходные IDs:** W1-05-F15.

**W1-05-F15: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F064 — published measurement, S037 §§2.1–2.2/3.3 Table2, не наш тест.** Faster R-CNN R50-FPN, COCO train2017 → val2017, полная доступная instance-разметка, не few-shot budget. Для standard / combined standard+stylized training: clean AP 36.3 / 34.6, corruption-mean mPC 18.2 / 20.4, relative rPC 50.2% / 58.9%. Проверка по 15 типам corruptions, 5 severity; это AP, не AP50. Appendix A: short edge 800, 12 epochs, LR schedule 8/11, фактически четыре GPU по две картинки/GPU с linear LR scaling. Правило выбора лучшего checkpoint и точная модель GPU здесь не восстановлены. Пример показывает trade-off clean/robustness; не доказывает, что stylization нужна для PPE или что такая же прибавка будет у YOLO. Для быстрого CCTV-плана полезнее отдельный clean и degraded slice.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f065"></a>

### F065 — provenance caution, S038/S037. README автора в Evaluation details называет COCO metric mAP50, тогда как Table2 paper и leaderboard COCO подписаны AP. Для чисел F064…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S037](SOURCES.md#s037), [S038](SOURCES.md#s038). **Исходные IDs:** W1-05-F16.

**W1-05-F16: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

**F065 — provenance caution, S038/S037.** README автора в Evaluation details называет COCO metric mAP50, тогда как Table2 paper и leaderboard COCO подписаны AP. Для чисел F064 использована версия paper v2; не смешивать metric labels README с таблицей статьи. Отдельный локальный benchmark этой веткой не выполнялся.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f066"></a>

### F066 — photometric | Разница света/экспозиции, тени, режим день/ночь в реальных train-camera samples | Если цвет кодирует тип каски/жилета, aggressive hue и gray могут…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F17.

**W1-05-F17: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F066 photometric | Разница света/экспозиции, тени, режим день/ночь в реальных train-camera samples | Если цвет кодирует тип каски/жилета, aggressive hue и gray могут изменить label evidence. Оставлять texture/края лица различимыми; HSV не имитирует IR night mode физически. Сверять целые составные transforms, не только каждый отдельно. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f067"></a>

### F067 — blur/compression/noise | Размытый человек в движении, дефокус, низкий bitrate действительно встречаются | Boxes могут остаться точными, а сигарета/ремни/респиратор…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F18.

**W1-05-F18: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F067 blur/compression/noise | Размытый человек в движении, дефокус, низкий bitrate действительно встречаются | Boxes могут остаться точными, а сигарета/ремни/респиратор исчезнуть. Не требовать от модели распознавания невидимого состояния; отдельно annotation policy unknown/ignore. JPEG proxy проверять на реальном видеопотоке. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f068"></a>

### F068 — геометрия/scale/crop/flips | Неуверенность в положении человека, несколько ракурсов, небольшая вибрация камеры | Синхронно менять boxes, masks, keypoints и…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F19.

**W1-05-F19: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F068 геометрия/scale/crop/flips | Неуверенность в положении человека, несколько ракурсов, небольшая вибрация камеры | Синхронно менять boxes, masks, keypoints и ROI-полигоны, если labels зависят от них. Для фиксированной камеры image-space zone нельзя оставить на старом месте после flip/affine. Вертикальный flip/сильная перспектива обычно не соответствует монтажу камеры; допускать только при реальном сценарии. Crop человека может убрать head/person association. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f069"></a>

### F069 — mosaic/mixup | Гипотеза о детекции объектов на разных масштабах/фонах; проверяется отдельно | Четыре сцены не имеют единого физического пола/зоны; прозрачные люди…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F20.

**W1-05-F20: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F069 mosaic/mixup | Гипотеза о детекции объектов на разных масштабах/фонах; проверяется отдельно | Четыре сцены не имеют единого физического пола/зоны; прозрачные люди MixUp не являются реальной окклюзией. Не переносить person-PPE relations через границы patches; event label целого кадра нельзя просто конкатенировать. Падение small-object survival — причина снизить/выключить. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f070"></a>

### F070 — occlusion/CoarseDropout/CutMix | Реальные перекрытия корпусами, оборудованием; object detection с согласованной политикой visibility | Закрыть голову не равно снять…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F21.

**W1-05-F21: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F070 occlusion/CoarseDropout/CutMix | Реальные перекрытия корпусами, оборудованием; object detection с согласованной политикой visibility | Закрыть голову не равно снять каску. Для `no_helmet` нужен видимый непокрытый head согласно ontology. Удаление части маски/box не создаёт достоверное нарушение. Для person-state bbox нужна проверка evidence region головы/лица, не доли person bbox. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f071"></a>

### F071 — copy-paste | Есть masks, правильные физические масштабы/позиции и конкретная нехватка сцен | Переносить связку person+PPE+relations, либо контролируемо создавать…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-05-F22.

**W1-05-F22: условия/наблюдение** ([ветка](_WORK/W1/05_AUGMENTATION.md)):

| F071 copy-paste | Есть masks, правильные физические масштабы/позиции и конкретная нехватка сцен | Переносить связку person+PPE+relations, либо контролируемо создавать состояние с повторной верификацией labels. Вклеенная каска рядом с головой не означает «надета». Footpoint/zone relation считать заново. Детали синтетического data generation — передача W1-11, не отдельное обещание здесь. |

Для smoking наличие маленького предмета не тождественно событию: руки/рот/временной контекст могут быть решающими. Покадровая аугментация не решает отсутствие события во времени. Для event/track-модели случайные пространственные параметры должны быть согласованы на клипе, если метод не предусматривает иной протокол; независимые скачки кадров создадут искусственное движение. Это вопрос к violation_methods/video_architecture.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-06 — W1-06 — масштаб объектов, разрешение, crops и каскады

<a id="f072"></a>

### F072 — SAHI: опубликованный протокол и единицы [PUB; S039 §4]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S039](SOURCES.md#s039). **Исходные IDs:** W1-06-F01.

**W1-06-F01: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

VisDrone: 6471 train, 548 val images; Table 1 — **test-dev**. xView: random 75/25 train/val. Это размеченные aerial datasets, не few-shot PPE. FCOS/VFNet/TOOD, MMDetection; original images плюс sliced patches. Train patch ranges: 480–640 px VisDrone, 300–500 px xView; resize с сохранением aspect ratio, 800–1333 px. Inference: 640×640 и 400×400 px соответственно; PO=25% overlap, NMS IoU=0.5. Метрика **AP50**, IoU=0.5, maxDets=500, не AP50:95. GPU/time и правило checkpoint selection из статьи не установлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f073"></a>

### F073 — gains и ограничения SAHI [PUB + арифметический INF; S039 Tables 1–2]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S039](SOURCES.md#s039). **Исходные IDs:** W1-06-F02.

**W1-06-F02: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

VisDrone TOOD: FI=29.4; SAHI=31.9; SAHI+PO=32.5; SAHI+FI+PO=34.7; SF+FI=36.8; SF+SAHI+FI+PO=43.5 AP50. Для large: FI=50.0, SAHI+PO=43.6. Следовательно, crop может ухудшать large/context. Для FCOS FI=25.8→SAHI+FI+PO=31.0 (**+5.2 п.п.**, abstract говорит 6.8); TOOD combined 43.5−29.4=**14.1 п.п.**, abstract говорит 14.5. Сохранять табличные числа и расхождение. xView TOOD SF+SAHI+PO=20.6, с добавленным FI=20.4: полный проход не гарантирует улучшение. Это авторские результаты, не наши измерения.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f074"></a>

### F074 — реальный benchmark не тождествен бумажному recipe [REP; S040]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S040](SOURCES.md#s040). **Исходные IDs:** W1-06-F03.

**W1-06-F03: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

`requirements.txt`: sahi==0.9.3, mmdet==2.21.0, mmcv-full==1.4.3; README: PyTorch1.10.0/torchvision0.11.1/CUDA11.3. Eval script: confidence=0.01, NMS/IOU=.5, class_agnostic=False, force_postprocess_type=True, max_detections=500. TOOD config: RandomCrop absolute_range=(480,960), Resize=(1333,800), keep_ratio=True; 24 epochs, steps16/22, warmup500, `save_best="auto"`; COCO TOOD R50-FPN checkpoint `tood_r50_fpn_1x_coco_20211210_103425-20e20746.pth`. Crop range **480–960** отличается от статьи 480–640. Нельзя заявлять буквальную репликацию бумаги по текущему commit; нужна историческая revision/config-to-result связь. Значение `save_best="auto"` не устанавливает выбранный авторами конкретный checkpoint.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f075"></a>

### F075 — актуальная SAHI API имеет иные merge defaults [REP; S041]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S041](SOURCES.md#s041). **Исходные IDs:** W1-06-F04.

**W1-06-F04: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

`get_sliced_prediction`: overlap_height_ratio=overlap_width_ratio=0.2, perform_standard_pred=True, postprocess_type="GREEDYNMM", postprocess_match_metric="IOS", match_threshold=.5, class_agnostic=False, batch_size=1. Сначала slices, затем batch inference, shift predictions в координаты кадра, optional standard pass при num_slices>1, merge. При model confidence<0.1 автоматически переключается на NMS/IOU, если force_postprocess_type=False. Поэтому изменение confidence способно незаметно изменить merge. Сравнение должно фиксировать оба механизма. `durations_in_seconds` даёт slice/prediction/postprocess, но не удостоверяет полную задержку нашего сервиса.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f076"></a>

### F076 — обработка crop GT и grid [REP; S042]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S042](SOURCES.md#s042). **Исходные IDs:** W1-06-F05.

**W1-06-F05: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

`get_slice_bboxes`: шаг — tile dimension минус `int(overlap_ratio*dimension)`; граничные окна сдвигаются к краю. `process_coco_annotations` обрезает annotation и сохраняет её при cropped_area/original_area>=min_area_ratio. `slice_image` и `slice_coco` default min_area_ratio=0.1; у `slice_coco` ignore_negative_samples=False. Эта геометрическая фильтрация не знает семантику «правильно надет респиратор»: оставшиеся 10% bbox не гарантируют наблюдаемость состояния. Нужен аудит обрезанных positives/ignore policy, иначе видимые фрагменты могут превратиться в ошибочные negatives.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f077"></a>

### F077 — batch API не равно batch на устройстве [REP; S043]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S043](SOURCES.md#s043). **Исходные IDs:** W1-06-F06.

**W1-06-F06: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

Базовый `perform_batch_inference` сохраняет images; последующая конвертация вызывает одиночный `perform_inference` для каждого изображения. Native batch требует override адаптера; docstring приводит Ultralytics/HuggingFace. Наличие параметра batch_size не доказывает уменьшение accelerator invocations или latency для иного runtime. Адаптер LinQ в этой ветке не установлен и не проверен.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f078"></a>

### F078 — просто multi-scale и selective-scale различаются [PUB; S044 §§4–7, Tables 1–2]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S044](SOURCES.md#s044). **Исходные IDs:** W1-06-F07.

**W1-06-F07: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

R-FCN ResNet50 ablation, proposals Deformable-RFCN ResNet101; COCO. Для small (<32×32 px) при test1400×2000 Table1: 800all=19.6, 1400all=19.9, MST=19.5, SNIP=21.4 mAP; small-only training=16.4. Нельзя принять большее разрешение/случайный multi-scale за гарантированное улучшение. SNIP selectively ignores gradients объектов вне scale range, использует их на подходящих масштабах. Table2: single-scale AP34.5/APS16.3; MS train/test35.6/19.5; SNIP37.8/21.4. Данные: 123k train, 20,288 test-dev; 118k/5k minival для proposal recall. RCN7 epochs, RPN6; проверенные baseline8/9 epochs были хуже7. Это специальный detector/trainer, не универсальный YOLO flag. Размер `<32×32` относится к dataset convention, не к физическому пределу видимости сигареты.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f079"></a>

### F079 — crop training должен видеть трудный фон [PUB; S045 §§3–4, Table2]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S045](SOURCES.md#s045). **Исходные IDs:** W1-06-F08.

**W1-06-F08: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

SNIPER Faster-RCNN/ResNet101, COCO: AP43.4 без negative chips против46.1 с ними; 2 scales43.3. RPN recall при этом AR65.4 в обоих вариантах: recall не отражает FP. Chips512² px, около5/image, примерно30% больше pixels, чем single800×1333; batch128,6 epochs, LR.015. Негативные chips выбирает отдельно обученный RPN. Timing авторов:14h training на8×V100 плюс2h RPN; около5 images/s наV100 при parallel processes, average batch100. Эти числа не являются нашей оценкой RTX4070/LinQ. Чипы/негативный mining требуют специального pipeline, не только генерации положительных crops; checkpoint-selection rule здесь не установлен.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f080"></a>

### F080 — геометрия масштаба [INF из координат resize; не эксперимент]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-06-F09.

**W1-06-F09: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

Для letterbox без растяжения scale r=min(Winput/Wsource,Hinput/Hsource), а объект w×h исходных px занимает rw×rh входных px до padding. Например, **условный** исходный 1920×1080 и вход640²: объект12×6 px становится4×2 px; crop640²→input640² сохраняет12×6 px. Новые наблюдённые детали при интерполяции не появляются. Это расчёт, а не минимальный допустимый размер детектора. Нужны distributions min(w,h), area, blur, visibility в исходном и фактическом model input, отдельно по классам/камерам/дистанции. Размер человека не заменяет размер респиратора.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f081"></a>

### F081 — стоимость вызовов [INF; S041, S042, S043]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S041](SOURCES.md#s041), [S042](SOURCES.md#s042), [S043](SOURCES.md#s043). **Исходные IDs:** W1-06-F10.

**W1-06-F10: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

При W,H>=tile s и фиксированном overlap o оценка grid по оси: n=1+ceil((D−s)/(s−floor(os))); проверять реальные координаты S042 на границах. Число tiles NxNy, плюс optional full frame. Иллюстрация, **не runtime measurement**: 1920×1080,640²,25%:4×2=8 crops; с FI=9 image forwards при batch1. Для true batch B число групп ceil(8/B)+1, но объём изображений остаётся9; fallback адаптер может выполнить9 одиночных вызовов. Считать image forwards, API requests и accelerator launches раздельно. Увеличение входа640→1280 увеличивает canvas area в4 раза; это не доказательство4× latency или memory.

| Вмешательство | Сохранение сигнала и риски | Что учитывать в полной стоимости |
|---|---|---|
| Full frame большее input | Меньше downsampling; контекст остаётся; меняется scale distribution и input graph | Decode, resize, transfer, engine, NMS; отдельная compiled shape, memory и качество |
| Fixed tiles | Не зависит от person recall; border truncation, duplicates, мало контекста | Все tile forwards, optional FI, merge, host crops, передача, batching, RAM и queue |
| Person→head/PPE crop | Выбор области сохраняет больше px для лица; FP/FN person/head stage, промах crop, occlusion | Stage1+variable number crops; idle/crowded scenes; две модели/две shapes, batching и swap |
| GT/oracle crops | Диагностика второго stage при идеальной локализации | Нельзя выдавать за deployable result; upstream cost и misses исключены |
| Crop training + original frames | Scale alignment, но больше correlated examples; label/context/negative coverage | Единый исходный split до slicing, число exposures, iterations и annotation audit |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f082"></a>

### F082 — cascade recall и контекст [INF; предлагаемый accounting]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-06-F11.

**W1-06-F11: условия/наблюдение** ([ветка](_WORK/W1/06_SCALE.md)):

Для системы без fallback, у которой положительный результат возможен только при пригодном upstream crop: R_end=P(usable crop|positive)×P(correct final|positive,usable crop). Это chain rule, без допущения независимости. End recall не выше usable-crop coverage. Head crop может исключить руку/сигарету, person crop — расположение относительно опасной зоны или горючих материалов; какой контекст необходим, задаёт класс/событие. Сохранить полные координаты, parent IDs и внешний контекст. Классификация crop «маска есть» не равна событию «респиратор надет правильно». Если GT — отношение/событие, одной object AP недостаточно.

Одинаковый threshold contract означает одинаковые классы, matching/ignore regions/maxDets, frame GT, merge rules и заранее выбранное правило operating point. Численно одинаковый confidence у разных cascade stages не означает одинаковый смысл score. Сначала фиксированный low-score detection export и одинаковый scorer; затем thresholds каждого кандидата выбираются **на validation** по одному требованию FP/recall и замораживаются. Не сравнивать oracle-positive crops с full-frame negatives. Merge/NMS изменения выделять отдельно от training gain.

Полная задержка измеряется от выбранной точки поступления кадра до готового результата/события, с одинаковой границей: decode+preprocess+queue/network+все stages+transfer+merge+event logic. Для async pipeline сумма средних stage times не заменяет p95 latency/throughput. FPS, p50/p95 ms/frame, frames dropped, calls/frame, bytes/frame, peak host/device memory и crowd dependence — отдельные единицы. Все значения для нашей системы пока неизвестны.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-07 — W1-07 — Смешивание источников, перенос домена и новая камера

<a id="f083"></a>

### F083 — Классическая UDA detection требует двух доменов

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S046](SOURCES.md#s046), [S047](SOURCES.md#s047). **Исходные IDs:** W1-07-F01.

**W1-07-F01: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**published**, S046 §§3–4: DA Faster R-CNN добавляет image- и instance-level domain classifiers с adversarial training и consistency regularization к двухэтапному детектору. Source размечен, target без supervised labels. **code**, S047 Usage: реализация основана на `py-faster-rcnn`, требует Caffe/pycaffe; source/target различаются префиксами имён. Это конкретная историческая training implementation, а не опция современного YOLO. **inference:** отключение source-loader не превращает этот метод в source-free. Отдельное доказательство совместимости trainer/backbone/head и экспорта требуется до практической очереди.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f084"></a>

### F084 — Adaptive Teacher: сильное измерение с узкими условиями

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S048](SOURCES.md#s048). **Исходные IDs:** W1-07-F02.

**W1-07-F02: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**published**, S048 §§3–4, Table3: AT соединяет teacher/student, weak/strong augmentation и adversarial alignment. Cityscapes→Foggy Cityscapes: Faster R-CNN/VGG16, ImageNet initialization, 8 классов; source train2975, target train без labels, target validation500. Авторы сообщают mAP50.9% против source-only23.5% и своего target-supervised oracle42.7%. Paper: shorter side600, SGD LR0.04, source warm-up10k + mutual learning50k, EMA0.9996, threshold0.8; 8V100, batch16. Точный checkpoint-selection protocol не установлен. Table4 отдельно исследует unseen artistic domain, шесть общих классов, R101. **Граница:** обычная адаптация к target и domain generalization — разные эксперименты; «oracle» здесь лишь конкретная supervised baseline.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f085"></a>

### F085 — Цена воспроизведения AT и ограничения лицензии

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S049](SOURCES.md#s049). **Исходные IDs:** W1-07-F03.

**W1-07-F03: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**code / author documentation**, S049: README указывает `Detectron2 == 0.3`, Python≥3.6, PyTorch≥1.5; tested environments8V100 и4×2080Ti. Лицензия проекта указана CC-BY-NC4.0. Часть весов/результатов в README обозначена `coming soon`, для internal weights предупреждается о несовпадении key names. **inference:** наличие репозитория не подтверждает загрузку совместимого checkpoint. Лицензионную применимость к сдаче/дальнейшему продукту нужно решить отдельно, до заимствования кода; это не установленный запрет нашего кейса.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f086"></a>

### F086 — Actual recipe отличается от paper

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S051](SOURCES.md#s051). **Исходные IDs:** W1-07-F04.

**W1-07-F04: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**code**, S051: `META_ARCHITECTURE: DAobjTwoStagePseudoLabGeneralizedRCNN`, `PseudoLabRPN`, `StandardROIHeadsPseudoLab`, `NUM_CLASSES: 8`; `IMG_PER_BATCH_LABEL: 16`, `IMG_PER_BATCH_UNLABEL: 16`, `BASE_LR: 0.04`, `MAX_ITER: 100000`, `BURN_UP_STEP: 20000`, `BBOX_THRESHOLD: 0.8`, `EMA_KEEP_RATE: 0.9996`, `UNSUP_LOSS_WEIGHT: 1.0`. Datasets: `cityscapes_fine_instance_seg_train`, `cityscapes_foggy_train`; test `cityscapes_foggy_val`; `EVAL_PERIOD: 1000`. Файл содержит повторный ключ `DATASETS:` — значение parsing здесь не запускалось. **inference:** paper10k+50k и текущий config20k/100k нельзя объединять в одну якобы воспроизведённую recipe. При повторении фиксировать commit и реально resolved config.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f087"></a>

### F087 — Training loop и итоговый inference артефакт AT

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S050](SOURCES.md#s050), [S052](SOURCES.md#s052), [S053](SOURCES.md#s053), [S054](SOURCES.md#s054). **Исходные IDs:** W1-07-F05.

**W1-07-F05: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**code**, S050: loader выдаёт labeled/unlabeled strong/weak views; до `BURN_UP_STEP` идёт supervised burn-in; после него teacher копируется/обновляется, target labels снимаются, pseudo boxes фильтруются confidence threshold. В lines572–589 `loss_rpn_loc_pseudo` и `loss_box_reg_pseudo` умножаются на0, discriminator losses — на `DIS_LOSS_WEIGHT`. Это изменения loader, trainer и loss, а не смешивание YAML-путей. **code**, S052: `--eval-only` строит teacher/student ensemble для загрузки checkpoint и вызывает `Trainer.test(...modelTeacher)`. **code**, S053: при eval `forward` переходит в `self.inference`; domain-loss branch отдельно. **inference:** при deploy нужен выбранный teacher detector и корректное извлечение весов. Не нужен онлайн adaptation loop по этому evaluation пути, но экспорт, удаление training-only state и исполнение такого графа нами не проверены. У других DA методов ситуация иная: S054 §3.3 явно использует context vectors при test; нельзя объявлять все domain branches удаляемыми.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f088"></a>

### F088 — Negative transfer существует в object detection, включая source degradation

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S054](SOURCES.md#s054). **Исходные IDs:** W1-07-F06.

**W1-07-F06: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**published**, S054 §§1,4–4.1 Tables1–2: Faster R-CNN/R101, ImageNet, VOC2007+2012 trainval→Clipart,20 классов. В авторском сравнении target mAP source-only27.8%, global BDC25.6%; source VOC77.5%→73.6%. Strong matching глобальной сцены может вредить при различии layout/object co-occurrence. Short side600,70k iterations (50k LR0.001 +20k LR0.0001), minibatch1source+1target; reported final checkpoint. Hardware/seeds не установлены. Строка DA-Faster19.8% — их reimplementation без consistency, а не исходное измерение Chen. **Критично:** все1000 Clipart images участвуют в unlabeled training и testing; это transductive оценка. Её нельзя выдавать за независимую новую камеру. IoU convention по прочитанному фрагменту точно не установлена: сохраняем авторское mAP, не переименовываем в COCO AP50:95.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f089"></a>

### F089 — Source-free не означает отсутствие исходного знания и не гарантирует quality gate

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S055](SOURCES.md#s055). **Исходные IDs:** W1-07-F07.

**Уточнение W2 к исходному утверждению:** F241–F246: simple-SFOD author route найден, local weights/manual JSON/eval BN/source hooks/selection gap не ready target package.

**W1-07-F07: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**published**, S055: SFOD2021 использует source-trained Faster R-CNN/VGG16 с ImageNet initialization; source samples нужны на pretrain, при adaptation не используются. SED выбирает pseudo-label threshold через self-entropy, затем Mosaic моделирует трудные пропуски. Авторы отдельно указывают noisy pseudo-labels и false negatives малых/окклюдированных объектов. Implementation: short side600, SGD LR0.001, batch1; source-only/oracle оцениваются на target validation. Compute/checkpoint-selection в этом чтении не установлены. **inference:** self-entropy — внутренняя proxy, не независимая проверка recall/FP. Для промышленной эксплуатации отсутствие target labels не позволяет доказать полезность adaptation по одному снижению entropy. Реализация под наш detector не установлена.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f090"></a>

### F090 — Temporal mining может искать пропуски, но готовый trainer не равен всей pipeline

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S056](SOURCES.md#s056), [S057](SOURCES.md#s057). **Исходные IDs:** W1-07-F08.

**W1-07-F08: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**published**, S056 abstract/§§3–4: авторы используют confident detections, tracking для hard positives и soft-label distillation; задачи — лица WIDER→surveillance и pedestrians BDD clear/day→другие условия. Это основание рассмотреть временной сигнал, а не доказательство переноса person tracks на каску/сигарету.

**author documentation**, S057: hard-positive mining на100k videos занял у авторов около недели на UMass GPU cluster; pipeline mining не включён, предлагаются извлечённые frames/pseudo-labels. Train scripts рассчитаны на4GPU; README single-model results отличаются от paper averages over5 rounds. **inference:** нельзя обещать готовый быстрый end-to-end mining по наличию training scripts. В нашем случае tracker может продлевать ошибочный объект; временная устойчивость не подтверждает правильный класс.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f091"></a>

### F091 — Локальный статус проверки

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-07-F09.

**W1-07-F09: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**local:** выполнены primary search+open, прочитаны перечисленные PDF/HTML/raw code, получены SHA/dates через GitHub API. Не выполнялись: training/benchmark, установка авторских зависимостей, проверка complete dataset files, download weights, inference/export, измерение VRAM или LinQ. **inference:** ниже — порядок принятия решений и предложенные абляции, без обещания процента выигрыша или времени на RTX4070.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f092"></a>

### F092 — proposed protocol, не результат статьи. В manifest у каждого файла нужны `camera_id`, `session_id`, временной диапазон, source dataset, group/track identifiers при…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-07-F10.

**W1-07-F10: условия/наблюдение** ([ветка](_WORK/W1/07_DOMAIN.md)):

**F092 — proposed protocol, не результат статьи.** В manifest у каждого файла нужны `camera_id`, `session_id`, временной диапазон, source dataset, group/track identifiers при наличии, доступность labels и роли использования. Разбить до отбора кадров, pseudo-labeling, аугментаций и ручного mining. Соседние кадры одного эпизода не распределять случайно по ролям. Хэш-дубликаты и одно и то же исходное видео должны оставаться в одной группе; производные (crop/translated/augmented) наследуют её.

Роли следует различать:

1. **Adaptation pool:** данные разрешены для gradient updates, teacher pseudo-labels, style/BN statistics, image translation и любого выбора обучающих примеров.
2. **Selection validation:** отдельные размеченные sessions для выбора mixing ratio, threshold, checkpoint и решения о продолжении. Если labels здесь существуют, режим не следует описывать как полностью zero-target-label model selection.
3. **Independent new-session test:** поздняя/другая сессия адаптируемой камеры, изображения которой не использовались ни в adaptation, ни в настройке.
4. **Independent new-camera test:** камера, исключённая полностью, включая unlabeled exposure. Только этот режим поддерживает вывод о переносе на ещё одну камеру; при одной камере его сделать невозможно.
5. **Old-domain retention:** отдельный holdout исходных/ранее работающих камер, если сохранение их качества требуется.

Можно отдельно измерить transductive режим, когда test images использованы без labels. Тогда явно сообщать, какие изображения и statistics были видны модели и как. Не объединять его число с independent новым-camera результатом. Если real deployment предполагает предварительный доступ ко всем неразмеченным видео данной камеры, transductive режим может быть релевантен этой постановке, но не подтверждает перенос на неизвестную будущую сессию. Пороговые настройки событий и геометрия опасной зоны также относятся к camera-specific adaptation: фиксировать их отдельно от обучения detector.

При слабом количестве независимых sessions полезнее честно показать paired differences по группам и характер ошибок, чем объявлять тысячи соседних кадров большим independent test. Набор ручного аудита pseudo-labels внутри adaptation pool служит контролю data quality; он не заменяет independent validation/test.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-08 — W1-08 — Active learning и ручная доразметка

<a id="f093"></a>

### F093 — S058 /  — Active Teacher: что именно означает diversity

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-08-F01.

**W1-08-F01: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

Peng Mi et al., **Active Teacher for Semi-Supervised Object Detection**, CVPR, June 2022, pp.14482–14491: [страница CVF](https://openaccess.thecvf.com/content/CVPR2022/html/Mi_Active_Teacher_for_Semi-Supervised_Object_Detection_CVPR_2022_paper.html). Полный текст реально открыт через [arXiv:2303.08348v1](https://arxiv.org/pdf/2303.08348), версия от 2023-03-15. Разница дат — поздняя публикация preprint, не новый CVPR-2023 метод. Локаторы: §3.2, Eq.7–11; §4.1–4.2; Tables 1,2,4; §5 Limitation. Доступ: 2026-10-23.

**Опубликованный метод/измерение:** difficulty — усреднённая энтропия class predictions; information — сумма confidence boxes; diversity — число различных **предсказанных категорий в одном изображении**. AutoNorm делит каждый показатель на максимум по пулу и суммирует нормированные показатели (L1). Это не расстояние между изображениями, не embedding coverage и не temporal deduplication.

Faster R-CNN/ResNet-50, COCO train2017 ≈118k, val2017 5k, mAP@[.50:.95]. Половина целевого label budget выбирается случайно, половина активно после SSOD; единица budget — изображения с доступной полной GT, не boxes или минуты. Авторы используют 2k supervised pretraining steps, 180k steps на SSOD stage, batch 64 = 32 labeled + 32 unlabeled, weak flip/strong color/gray/blur/CutOut. Table 1: 5% labels — 30.07 AP против Unbiased Teacher 28.27; 10% — 32.58 против 31.50. Table 2: 40% labels — 37.92, fully supervised reference 37.63. §5 предупреждает о дополнительных training stages; выигрыш не является бесплатным. Выбор checkpoint для каждого табличного числа и wall-clock здесь не установлен. Эти цифры не доказывают экономию нашего времени аннотатора или перенос на PPE.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f094"></a>

### F094 — S059 /  — Реальная реализация ActiveTeacher и её границы

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S058](SOURCES.md#s058). **Исходные IDs:** W1-08-F02.

**W1-08-F02: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

[Официальный репозиторий HunterJ-Lin/ActiveTeacher](https://github.com/HunterJ-Lin/ActiveTeacher), зафиксирован commit `8da0f5c386eef16e25fdb3a385abac73a53d95d6`, committer date `2023-03-27T06:40:41Z` (GitHub REST API). Реально прочитаны README и следующие pinned файлы, код не запускался:

- [tools/inference_for_active_pick.py](https://github.com/HunterJ-Lin/ActiveTeacher/blob/8da0f5c386eef16e25fdb3a385abac73a53d95d6/tools/inference_for_active_pick.py), `uncertainty_entropy`, `inference`, `args.opts`;
- [tools/active_pick_evaluation.py](https://github.com/HunterJ-Lin/ActiveTeacher/blob/8da0f5c386eef16e25fdb3a385abac73a53d95d6/tools/active_pick_evaluation.py), `PreprocessData`, `norm_dict`, `CombineMetrics`;
- [README](https://github.com/HunterJ-Lin/ActiveTeacher/blob/8da0f5c386eef16e25fdb3a385abac73a53d95d6/README.md), Training Steps 0–4.

**Наблюдение кода:** selector получает ROI logits через hook teacher box predictor. `uncertainty_entropy` усредняет энтропии, затем одно image entropy записывается в каждый emitted box. Поэтому присваивание `_difficult = box['entropy']` внутри цикла не равно потере всех boxes, кроме последнего: записанное значение повторяется. Но усреднение происходит на hooked ROI tensor, не явно на только финальных boxes Eq.7. Inference фиксирует score threshold/NMS `0.5`, cap `TEST.DETECTIONS_PER_IMAGE=20`. При пустом списке итоговые показатели нулевые. `norm_dict` не защищает нулевой максимум. В исходнике есть `np.float`/`np.int`, что требует проверки совместимости установленного NumPy. README зависит от Detectron2 без найденного точного lock версии; пример использует восемь GPU, выборочную модель `model_best.pth` и последующее обучение заново. Это framework-specific исследовательский код, не подтверждённый drop-in selector для другого детектора.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f095"></a>

### F095 — S060 /  — Видеоредундантность: поддержана абляцией, но не универсальное окно

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S059](SOURCES.md#s059). **Исходные IDs:** W1-08-F03.

**W1-08-F03: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

Hamed H. Aghdam et al., **Active Learning for Deep Detection Neural Networks**, ICCV October 2019: [CVF](https://openaccess.thecvf.com/content_ICCV_2019/html/Aghdam_Active_Learning_for_Deep_Detection_Neural_Networks_ICCV_2019_paper.html), [прочитанный arXiv PDF 1911.09168v1, 2019-11-20](https://arxiv.org/pdf/1911.09168). Локаторы §3 Selecting images, §4, Figures 9–12; доступ 2026-10-23.

**Метод/авторская абляция:** ранжирование кадров дополняется запретом выбора соседей внутри текущего и следующих циклов. На Caltech Pedestrian temporal selection rules существенно важнее temporal smoothing; это разные операции. Budget B/b выражен в изображениях (footnote1). Используется собственный dense pedestrian detector без bbox regression; CityPersons — исходное обучение, Caltech/BDD100K — адаптационный пул, labels фильтруются по росту ≥50 px и aspect ratio. Метрика — miss rate относительно FPPI, не COCO AP. На BDD100K random лучше после первого цикла; поздний выигрыш предлагаемого отбора мал. Авторы связывают это с ограниченной capacity модели. Значит, AL не решает автоматически недостаточную выразительность/наблюдаемость. В Caltech-обсуждении текущий цикл исключает ±15 frames, но копировать 15 кадров в CCTV без FPS/длительности состояния нельзя. Опубликованные оценки времени разметки не являются нашими замерами.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f096"></a>

### F096 — S061 /  — Контрпример к «uncertainty обязательно лучше random»

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S060](SOURCES.md#s060). **Исходные IDs:** W1-08-F04.

**W1-08-F04: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

Jan Schneegans, Maarten Bieshaar, Bernhard Sick, **A Practical Evaluation of Active Learning Approaches for Object Detection**, IAL@ECML/PKDD 2022, CEUR Vol.3259, pp.49–67: [полный первичный PDF](https://ceur-ws.org/Vol-3259/ialatecml_paper5.pdf). Локаторы §3–4, §5, Fig.4–8, §6–7; доступ 2026-10-23. Точная календарная дата выпуска PDF не установлена.

**Опубликованный протокол/ограничение:** Faster R-CNN/BDD100K, entropy/BALD/eIOU с разной агрегацией; 30 циклов ×512 изображений =15,360 из 60k обучающего пула, каждый цикл заново от pretrained model, два повторения. 10k test отделены из train, original validation 10k; 13 classes. 10 epochs/cycle, batch20, LR1e-5, brightness/contrast/noise augmentation. §5: learning curves и итоговое качество подходов близки; objectness selection даёт малый выигрыш при примерно +40% **аннотированных объектов**. Их cost proxy — количество GT objects, не измеренные минуты, коррекции или клики. Вывод авторов ограничивает обоснование сложности AL; он не доказывает бесполезность всех AL. Видео/temporal information не исследованы. Статус выбора checkpoint для итоговых сравнений здесь не восстановлен. [Авторский код](https://git.ies.uni-kassel.de/public_code/a_practical_evaluation_of_active_learning_approaches_for_object_detection) указан §7, но web tool адрес не открыл; реализация не подтверждена запуском.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f097"></a>

### F097 — S062 /  — Classification uncertainty не измеряет локализацию

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S061](SOURCES.md#s061). **Исходные IDs:** W1-08-F05.

**W1-08-F05: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

Chieh-Chi Kao et al., **Localization-Aware Active Learning for Object Detection**, [arXiv:1801.05124v1 от 2018-01-16](https://arxiv.org/html/1801.05124v1), реально открыт полный HTML. Локаторы §3.1–3.3, §4.1–4.4, Table1; доступ 2026-10-23.

**Метод/протокол:** LT оценивает overlap proposal/final box и требует proposal stage; LS измеряет изменения boxes после Gaussian noise и проверяется также с SSD. Поэтому LT не является готовым интерфейсом one-stage YOLO. Эксперимент использует уже существующие GT, без людей. FRCNN/VGG16/PASCAL2012: pool 5,717 train images, 5,823 val для testing, initial500, +200 images/round, 15 rounds, 20 epochs/model, пять trials, shortest side600. Table1 на 1,100 images: random52.9, classification-only54.0, LS+C55.3 mAP. Это изображение-центричный результат, без измеренного annotation cost. LS требует дополнительных forward passes; нестабильность под шумом не равна вероятности полезной разметки промышленного объекта. Конкретную прибавку на PPE работа не устанавливает.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f098"></a>

### F098 — S063 /  — CVAT: интерфейс предразметки, class mapping и качество

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S062](SOURCES.md#s062). **Исходные IDs:** W1-08-F06.

**W1-08-F06: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

[CVAT Auto-annotation API](https://docs.cvat.ai/docs/api_sdk/sdk/auto-annotation/), [Automated QA](https://docs.cvat.ai/docs/qa-analytics/auto-qa/). Это опубликованные страницы **develop**, не обещание возможностей локального deployment. Зафиксирован исходник `cvat-ai/cvat` commit `70efd4284614adc2fb5bfede6d98bc94b90c7df7`, committer `2026-10-22T20:28:14Z`; [driver.py](https://github.com/cvat-ai/cvat/blob/70efd4284614adc2fb5bfede6d98bc94b90c7df7/cvat-sdk/cvat_sdk/auto_annotation/driver.py), `annotate_task`, строки522–617; [QA source](https://github.com/cvat-ai/cvat/blob/70efd4284614adc2fb5bfede6d98bc94b90c7df7/site/content/en/docs/qa-analytics/auto-qa.md), Basics/Validation modes. Доступ 2026-10-23.

**Документация/код:** AA function возвращает shapes; driver по умолчанию добавляет annotations, `clear_existing=False`. Код использует `allow_unmatched_labels=False`, `conf_threshold=None`. Несовпадение labels вызывает ошибку; разрешение unmatched позволяет их пропустить. В текстовой странице встречается singular `allow_unmatched_label`, поэтому буквальный API брать из pinned code и сверять installed SDK. Правильное сопоставление labels не проверяет фактическое содержание картинки.

QA сравнивает annotations с вручную подготовленной GT subset; это зависит от качества эталона. Рекомендована случайная независимая выборка; документационные 5–15% не являются статистической гарантией для редкого нарушения. Honeypots требуют image tasks с random ordering, не поддерживают tracks; видео с tracks требует Ground Truth mode. Автоматическая QA/аналитика отмечена Online/Enterprise: доступность в Community не предполагать. Предразметка не гарантирует правильный GT; reviewer должен искать также отсутствующие объекты.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f099"></a>

### F099 — S064 /  — CVAT cost counters не равны человеку-минутам и сценам

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S063](SOURCES.md#s063). **Исходные IDs:** W1-08-F07.

**W1-08-F07: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

[CVAT Analytics](https://docs.cvat.ai/docs/qa-analytics/analytics/), локаторы Summary, Annotations, Events; develop на дату доступа 2026-10-23 (publication date не установлена). **Документация:** доступны working time по annotation events, net objects created minus deleted, keyframes/interpolated frames/tracks, objects/hour, экспорт events CSV; Analytics платная в CVAT Online/Enterprise. Net objects могут быть отрицательными; интерполированные boxes не равны числу ручных действий. Для cost experiment нужно дополнить события таймером проверки/поиска/обсуждений и учётом импортированных annotations; способность конкретного deployment экспортировать нужные данные не проверена.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f100"></a>

### F100 — собственный вывод из F093, F094, F095, F096, F097, F098, F099. Внутрикадровое разнообразие predicted classes, межкадровое coverage и количество независимых…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-08-F08.

**W1-08-F08: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

**F100 — собственный вывод из F093, F094, F095, F096, F097, F098, F099.** Внутрикадровое разнообразие predicted classes, межкадровое coverage и количество независимых наблюдений — три разные величины. Статичная камера способна породить тысячи почти одинаковых касок; рост frames/boxes не означает рост независимых сцен. Временная группа должна иметь camera_id/session_id/time interval; track_id помогает определить повтор одного появления, но не заменяет scene grouping при ошибках tracker. Разметка нескольких фаз одного действия может быть необходима для события, даже если эти кадры избыточны для object detector. Окно dedup задаётся по реальным временным масштабам и сохраняется в manifest.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f101"></a>

### F101 — собственная гипотеза, не новое измерение. Комбинация stratified random + targeted errors + uncertainty/disagreement с cap по scene должна уменьшать слепые зоны.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-08-F09.

**W1-08-F09: условия/наблюдение** ([ветка](_WORK/W1/08_ACTIVE.md)):

**F101 — собственная гипотеза, не новое измерение.** Комбинация stratified random + targeted errors + uncertainty/disagreement с cap по scene должна уменьшать слепые зоны. Random-компонента нужна потому, что confident wrong predictions и no-detection images не обязаны попадать в top uncertainty; diversity по predictions также не видит неизвестный класс. Человеческий отбор способен обнаружить такие случаи, но требует строгого журнала причин и времени поиска. Representativeness не гарантирует редкие нарушения: целевые квоты по видимости/масштабу/негативам дополняют распределение камер. Квоты по predicted rare class нельзя выдавать за истинные rare labels.

| Отбор | Что нужно | Риск и проверка |
|---|---|---|
| Random по scene/camera/session | metadata, seeded sampling | Редкое событие может не встретиться; показывать coverage и интервалы неопределённости |
| Ручной по taxonomized errors | разрешённый train/dev material, annotator | Время просмотра входит в бюджет; субъективность, подтверждение любимой гипотезы |
| Uncertainty | versioned scores/logits, правила агрегации | Dense scenes, outliers, empty images; проверять расход минут и no-detection audit |
| Disagreement teacher/student или augmented views | два результата с одинаковым class mapping/coordinates | Общая уверенная ошибка останется общей; matching boxes и стоимость inference фиксируются |
| Diversity/representativeness по embeddings/metadata | единый feature extractor или metadata | Возможен отбор по фону; смотреть независимые группы и покрытие трудных состояний |

Таблица — проект вариантов проверки, а не список одинаково подтверждённых реализаций. Embedding selector для выбранного стека пока не найден/не нужен как обязательная зависимость. Disagreement через MC dropout требует корректного включения dropout; произвольные модели с disabled dropout не получают BALD автоматически.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-09 — W1-09 — Pseudo-labels и semi-supervised detection

<a id="f102"></a>

### F102 — Soft Teacher: измерение статьи, не наш результат

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S065](SOURCES.md#s065). **Исходные IDs:** W1-09-F01.

**W1-09-F01: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**paper; S065, §4.1–4.3/Tables 2–4.** COCO train2017: около 118k изображений; partial setting: 1/5/10% изображений размечены, остальные скрыты; пять folds, среднее на val2017 (5k), COCO AP. Faster R-CNN/FPN, ImageNet ResNet-50. Baseline → Soft Teacher: `10.0±0.26 → 20.46±0.39`; `20.92±0.15 → 30.74±0.08`; `26.94±0.111 → 34.04±0.14`. Partial: 180k iterations, 8 GPUs × 5 images, SGD LR .01, drops 110k/160k, momentum .9, WD .0001. Full: все train2017 + 123k unlabeled2017, `40.9 → 44.5`, 720k iterations, 8×8 images, drops 480k/680k. Foreground threshold .9; labeled sampling ratio .2/.5, сокращается к нулю в последние 10k/20k. Jitter: 10, threshold .02; статья описывает uniform ±6%. Teacher получает слабые, student сильные преобразования. Критерий выбора лучшего checkpoint явно не восстановлен; нельзя молча назвать это одним last/best checkpoint. Это COCO detection, не CCTV events и не оценка RTX 4070.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f103"></a>

### F103 — Нельзя смешивать результаты README, статьи и inference threshold

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S066](SOURCES.md#s066). **Исходные IDs:** W1-09-F02.

**W1-09-F02: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read/documentation; S066, Main Results/Notes/Requirements.** README сообщает для 1% baseline 10.0, ours 21.62 (`thr=5e-2`) / 22.64 (`thr=1e-3`); для 5% — 20.92 / 30.42 / 31.7; для 10% — 26.94 / 33.78 / 34.7. `thr` здесь именно **`model.test_cfg.rcnn.score_thr`**, а не teacher confidence cutoff. Все модели README обучены на 8×V100. Окружение авторов: Python 3.6, PyTorch 1.9.0, MMDetection `2.16.0+fe46ffe`, MMCV 1.3.9, Ubuntu 16.04. Доступность старого репозитория не доказывает его работоспособность в нашем пока неизвестном окружении. Причину всех расхождений README–paper одним score threshold не установлено; сохранять обе версии раздельно.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f104"></a>

### F104 — Что Soft Teacher реально делает с пропусками и координатами

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S067](SOURCES.md#s067). **Исходные IDs:** W1-09-F03.

**W1-09-F03: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S067, названные функции.** Teacher заморожен для градиентов; labeled training выполняет student. Для unlabelled views сопоставляются filename, boxes переводятся матрицей teacher→student. На student proposals, назначенных background, `unsup_rcnn_cls_loss` заменяет вес на teacher background score. Так неоднозначный пропущенный positive не получает такой же жёсткий отрицательный вес, как уверенный background. Regression использует отдельный фильтр normalized uncertainty; `compute_uncertainty_with_aug` считает std координат после teacher regression относительно размеров boxes. Это не доказательство истинности box.

В `extract_teacher_info` не-float `pseudo_label_initial_score_thr` приводит к `NotImplementedError("Dynamic Threshold is not implemented yet.")`. Поэтому class-aware/dynamic threshold не следует выдавать за готовый аргумент этого кода. `aug_box` использует **`torch.randn × box_scale × frac`**, а не uniform распределение из F102. Это обнаруженное различие paper/code; для воспроизведения нужно выбрать и зафиксировать реализацию, а не смешать описания. Чтение не включало численную проверку jitter.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f105"></a>

### F105 — Версионный config SoftTeacher

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S068](SOURCES.md#s068). **Исходные IDs:** W1-09-F04.

**W1-09-F04: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S068.** В `semi_wrapper.train_cfg`: `pseudo_label_initial_score_thr=0.5`, `rpn_pseudo_threshold=0.9`, `cls_pseudo_threshold=0.9`, `reg_pseudo_threshold=0.02`, `jitter_times=10`, `jitter_scale=0.06`, `unsup_weight=4.0`, `use_teacher_proposal=False`. Разные cutoff выполняют разные задачи; их нельзя свести к одному confidence.

`base.py`: Caffe-style R50, frozen norm; BGR normalize mean `[103.530,116.280,123.675]`, std `[1,1,1]`. Resize range `(1333,400)`–`(1333,1200)`, ratio preserved; weak: resize/flip, strong: дополнительно photometric/geometric/erase. Test `(1333,800)`, без flip, pad divisor 32. `SemiDataset` и branches `sup`, `unsup_teacher`, `unsup_student`; sampler `[1,4]`. `MeanTeacher(momentum=.999, interval=1, warm_up=0)`; SGD .01/.9/.0001, LR steps **120k/160k**, runner 180k; evaluation/checkpoint every 4k, fp16 dynamic loss scaling. LR 120k отличается от paper 110k. Это recipe на данном SHA, не «универсальные defaults» и не оптимум для СИЗ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f106"></a>

### F106 — Partial config и запуск не адаптируют метод к новой голове автоматически

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S069](SOURCES.md#s069). **Исходные IDs:** W1-09-F05.

**W1-09-F05: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S069.** Partial config задаёт 5 samples/GPU, 5 workers, JSON paths `instances_train2017.${fold}@${percent}.json` и `...-unlabeled.json`, `[1,4]`; default fold=1, percent=1. Launcher выбирает разные baseline/semi configs, параметры fold/percent передаются в MMDetection config. Для новой таксономии дополнительно требуются dataset registration/num_classes/checkpoint mapping и проверка loss, а для YOLO — иной интерфейс assignment/head; это наша интеграционная задача, отсутствующая в проверенных файлах.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f107"></a>

### F107 — EMA и inference stream — отдельные решения

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S070](SOURCES.md#s070). **Исходные IDs:** W1-09-F06.

**W1-09-F06: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S070.** Hook клонирует student→teacher при нулевой итерации; фактический momentum на шаге — `min(momentum, 1-(1+warm_up)/(iter+1+warm_up))`, то есть заданные .999 не означают постоянные .999 с первого шага. Обновляются `named_parameters`. `MultiSteamDetector` направляет inference в выбранную submodule, а F105 задаёт `inference_on="student"`. Следствие: wrapper не требует двойного inference, но извлечение/экспорт одной ветви и совпадение выходов ещё нужно проверить; весь checkpoint teacher+student нельзя считать готовой LinQ моделью.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f108"></a>

### F108 — Unbiased Teacher v1: иной протокол и результат

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S071](SOURCES.md#s071). **Исходные IDs:** W1-09-F07.

**W1-09-F07: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**paper; S071, §3–4/Table 1/A.4.** COCO-standard: .5/1/2/5/10% размеченных изображений, остальные unlabeled; Faster R-CNN/FPN ImageNet R50, AP50:95. Для 1% supervised `9.05±.16`, UT `20.75±.12`; для 10% `23.86±.81 → 31.50±.10`. Оценивается **teacher**, поэтому эти значения не являются качеством student. 180k iterations, labeled/unlabeled batches 32/32; burn-in 1/2/6/12/20k соответственно доле разметки; SGD LR .01, momentum .9. Threshold .7, EMA .9996, unsup weight 4. Weak flip; strong color/grayscale/blur/cutout, без дополнительных geometry. Class-wise NMS, focal ROI classifier; unsupervised regression исключён: class confidence не измеряет качество координат. Appendix A.2.2: высокий .9 даёт мало boxes, слишком низкий threshold приводит к шуму/несходимости в исследованном режиме. COCO-additional: train2017 + unlabeled2017; Appendix A.4 описывает 360k включая 90k burn-in. Число независимых folds и точное best/last правило в прочитанном протоколе не установлены; знак ± не следует самостоятельно объявлять стандартным отклонением по пяти folds.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f109"></a>

### F109 — Авторский UT recipe и библиотека

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S072](SOURCES.md#s072). **Исходные IDs:** W1-09-F08.

**W1-09-F08: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**documentation; S072.** Авторский repo использует Detectron2; README требует Python ≥3.6, PyTorch ≥1.5 и совместимый torchvision, Linux/macOS. Пример запуска: 8 GPUs и overrides `SOLVER.IMG_PER_BATCH_LABEL 16`, `...UNLABEL 16`, хотя config F111 содержит 32/32. Поэтому «команда README + config» и «чистый config» — разные effective batch. Сборку текущих зависимостей и работу на Windows не проверяли. Не выводить совместимость из минимальных требований README.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f110"></a>

### F110 — UT online integration по trainer

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S073](SOURCES.md#s073). **Исходные IDs:** W1-09-F09.

**W1-09-F09: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S073.** Loader возвращает четыре группы strong/weak labeled/unlabeled. Истинные labels unlabeled удаляются. До burn-up используются только labeled strong+weak; на границе teacher копирует student (`keep_rate=0`), затем EMA по config. Teacher no-grad на weak unlabeled, ROI predictions фильтруются scalar threshold, их hard boxes/classes передаются strong student. `loss_rpn_loc_pseudo` и `loss_box_reg_pseudo` явно умножаются на **0**, другие pseudo losses — на `UNSUP_LOSS_WEIGHT`; затем backprop/optimizer только student. Это supervised regression по labeled данным, а не полное отключение regression сети.

`threshold_bbox` для ROI использует `scores > thres`; class-wise threshold dictionary здесь нет. `build_hooks` раздельно оценивает student (суффикс `_student`) и teacher. Сохранить обе оценки и явно назвать экспортируемую ветвь; прирост teacher нельзя приписывать student. EMA не добавляет отсутствующие классы автоматически и не заменяет ручной контроль.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f111"></a>

### F111 — Точный UT 1% config

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S074](SOURCES.md#s074). **Исходные IDs:** W1-09-F10.

**W1-09-F10: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**code-read; S074.** `TwoStagePseudoLabGeneralizedRCNN`, `PseudoLabRPN`, `StandardROIHeadsPseudoLab`, ROI `FocalLoss`, RPN `CrossEntropy`; R50 weights `detectron2://ImageNetPretrained/MSRA/R-50.pkl`. Config: MAX_ITER 180000, steps `(179990,179995)`, LR .01, labeled/unlabeled 32/32, SUP_PERCENT 1.0, RANDOM_DATA_SEED 1, BBOX_THRESHOLD .7, BURN_UP_STEP 2000, EMA_KEEP_RATE .9996, TEACHER_UPDATE_ITER 1, UNSUP_LOSS_WEIGHT 4.0, evaluation every 1000, test `coco_2017_val`. Base INPUT short sides `(640,672,704,736,768,800)`; полный resolved preprocessing зависит также от Detectron2 version/defaults, не восстановлен. Почти весь run до двух последних LR drops имеет constant LR; сохранять literal config, не заменять его пересказом «обычный schedule».

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f112"></a>

### F112 — Offline pseudo-labeling существует отдельно от EMA

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S075](SOURCES.md#s075). **Исходные IDs:** W1-09-F11.

**W1-09-F11: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**documentation; S075, Training steps 1–3.** STAC author workflow: обучить detector labeled → предсказать boxes/classes на unlabeled → обучить STAC с labeled+pseudo-labels и strong augmentation. README использует сохранённый `pseudo_data.npy`, `TRAIN.CONFIDENCE=.9`, `TRAIN.WU=2` и Faster R-CNN. Такой offline artifact можно инспектировать до обучения; это не автоматическое доказательство качества его labels. Предлагаемая нами ручная полная коррекция — дополнительная процедура, а не часть доказанного STAC recipe.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f113"></a>

### F113 — Почему перенос к one-stage нельзя считать заменой пары флагов

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S076](SOURCES.md#s076), [S077](SOURCES.md#s077). **Исходные IDs:** W1-09-F12.

**Уточнение W2 к исходному утверждению:** F206–F212: UTv2 code теперь прочитан; std остаётся Python eval, default teacher, обычный export не доказан. F213–F219 — legacy YOLOv5 EfficientTeacher route.

**W1-09-F12: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**paper; S076, §3.2–3.3 pp.4–5; documentation S077.** UTv2 разбирает FCOS: centerness×classification score и center sampling могут вести себя хуже при noisy pseudo-labels, чем соответствующие упрощения. Listen2Student сравнивает uncertainties teacher/student для отбора regression supervision; uncertainty требует добавленной ветви и специального обучения. Это свидетельство зависимости SSL от head/assignment, а не основание переносить FCOS вывод на любую версию YOLO. Код этой дополнительной ветви и её фактическое удаление/сохранение при экспорте здесь не проверялись.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f114"></a>

### F114 — Практический вывод: confidence ≠ correctness

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-09-F13.

**W1-09-F13: условия/наблюдение** ([ветка](_WORK/W1/09_PSEUDO.md)):

**inference из F104/F108/F110/F113.** Score — внутренний выход модели после её обучения и postprocessing. Без отдельной эмпирической проверки на целевом домене он не равен вероятности «класс и bbox верны», тем более вероятности нарушения. Даже калиброванный class score не подтверждает IoU, полноту набора objects и правильную person–PPE association.

Аудит только принятых boxes оценивает precision, но скрывает missed positives. Аудит только uncertain frames скрывает confident errors и easy negatives. Для полноты нужна отдельная полностью вручную размеченная выборка кадров из train-domain с реальными негативами и независимыми сценами; инспектор должен искать все классы без подсказок teacher хотя бы на контрольной части. Считать one-to-one совпадения correct class + заранее заданный IoU, отдельно локализацию при верном классе и пропущенные объекты. Объекты ниже cutoff всё ещё могут быть positive, пустой output не подтверждает negative frame.

Class-aware threshold — **proposed**, выбирать по precision/coverage на calibration/audit данных; редкий класс с недостатком примеров оставлять в human review. Нельзя снижать cutoff только ради одинаковых counts по классам: распределение сцен может быть реально неравным. Если выбранный supervised loader трактует неуказанные объекты как background, одобрение отдельных boxes без дорисовки остальных создаёт partial-label проблему. Нужны полная коррекция кадра либо реально поддержанный ignore/masking loss; наличие ignore следует проверить в выбранном model_stack.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-10 — W1-10 — Offline teachers, VLM и distillation

<a id="f115"></a>

### F115 — Штатный KD Ultralytics существует в проверенной версии

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S029](SOURCES.md#s029), [S078](SOURCES.md#s078), [S079](SOURCES.md#s079). **Исходные IDs:** W1-10-F01.

**W1-10-F01: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: docs + код, не запуск.** S078, S079, S029, S011. Guide открывается с redirect от URL с trailing slash к URL без него. `__version__ = "8.4.184"`; в defaults есть `distill_model` и `dis: 6.0`. BaseTrainer импортирует `DistillationModel` и при заданном teacher path создаёт wrapper. Это положительное доказательство реализации. Минимальный официальный пример: student `yolo26n.pt`, teacher `yolo26s.pt`, вызов `model.train(data="coco8.yaml", epochs=100, distill_model="yolo26s.pt")`. `coco8.yaml` — демонстрационный вход, не протокол оценки промышленного CCTV.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f116"></a>

### F116 — Поддержка и опубликованный benchmark имеют границы

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S078](SOURCES.md#s078). **Исходные IDs:** W1-10-F02.

**W1-10-F02: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: документация/измерение производителя.** S078. Docs требуют одну YOLO family и одинаковую task; cross-family не поддерживается. Реализованы detect/segment/pose/obb, но accuracy benefit экспериментально подтверждён автором только для detect; classify/semantic/depth/RT-DETR исключены. Таблица COCO val2017, single-model single-scale, 640 px: YOLO26n baseline 40.9 → distilled 41.5 mAP50–95; e2e 40.1 → 40.9. NMS/e2e пути различаются. Label budget, полный training compute, seed variance и checkpoint selection из этой таблицы не восстановлены. Это не обещание +0.6 AP на PPE.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f117"></a>

### F117 — Путь trainer и цена online KD

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-10-F03.

**W1-10-F03: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: чтение кода.** S011. `_setup_train` отключает `compile` при `distill_model`, защищает teacher parameters от размораживания, создаёт wrapper до EMA/optimizer; DDP использует `find_unused_parameters` при выключенном compile. `setup_model` при resume восстанавливает student и teacher по сохранённому `distill_model`, затем projector weights. Следствие: teacher path/веса нужно сохранять для продолжения training; готовый inference artifact этого требования иметь не должен. Exact wall-clock, VRAM и стоимость облака неизвестны. Нужны как минимум teacher forward на каждом batch плюс student forward/backward; это измеряемая дополнительная стоимость, а не универсальный множитель «вдвое».

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f118"></a>

### F118 — Что конкретно сопоставляется у Ultralytics

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S080](SOURCES.md#s080), [S082](SOURCES.md#s082). **Исходные IDs:** W1-10-F04.

**W1-10-F04: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: чтение кода.** S080/S082. `get_distill_layers` находит `Detect`, возвращает его входы и head. Для YOLO26: `[16,19,22,23]`, neck P3/8, P4/16, P5/32. Каждый student feature проходит Conv1×1→ReLU→Conv1×1 к teacher channels; затем score-weighted L2. Weight — максимум sigmoid teacher class score в location; для end-to-end head сначала усредняются one2many/one2one scores. Teacher frozen/eval/no_grad; обе модели видят один `batch["img"]`. Одинаковое число levels проверяется явно. Пространственный размер автоматически не ресемплируется. Это feature guidance, не KL logits и не teacher-box regression. Локаторы: `__init__`, `loss`, `loss_sl2`.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f119"></a>

### F119 — Class/head mapping нельзя считать решённым автоматически

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S029](SOURCES.md#s029), [S080](SOURCES.md#s080). **Исходные IDs:** W1-10-F05.

**W1-10-F05: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: код + наш вывод.** S080/S029. В просмотренном wrapper нет semantic class remapping; confidence берётся через максимум по teacher classes. Поэтому совпадение `nc` само по себе недостаточно: до KD зафиксировать `class_id→name→definition` обеих моделей и task. `cls_remap` в defaults относится к переносу pretrained classifier rows при fine-tuning; это не доказательство semantic remapping teacher в KD. Нет явной проверки одинаковой family в прочитанном constructor: code-level возможность создать пару не расширяет documented support. Несовместимые spatial grids или head output contracts могут сломать loss; одинаковое число levels этого не исключает.

Практический условный путь: сильный **целевой** teacher той же family → student той же ontology/входных каналов/разрешения → обычные supervised losses + KD. Загруженный COCO teacher без требуемого PPE-класса не становится учителем этого класса от добавления `distill_model`.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f120"></a>

### F120 — Final student и промежуточный checkpoint различаются

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S081](SOURCES.md#s081). **Исходные IDs:** W1-10-F06.

**Уточнение W2 к исходному утверждению:** F193: saved EMA wrapper уже teacher-free; projectors до unwrap. F274: pre-strip не exact online/RNG/loader/scheduler continuation.

**W1-10-F06: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: чтение кода.** S011/S081. EMA удаляет teacher из своей копии wrapper. Training checkpoint поэтому может всё ещё содержать wrapper/projectors и путь teacher для resume. В штатном `final_eval` вызывается `strip_optimizer` для last и best; там убираются feature hooks, wrapper заменяется `student_model`. `fuse` также возвращает student. Следовательно, нормальный законченный путь предназначен для стандартного student graph. Прерванный run/ручное сохранение нельзя объявить таким же artifact без осмотра. Реальный сохранённый .pt и ONNX в этой работе не проверялись. Приёмка должна отдельно доказать загрузку/инференс без teacher file и отсутствие KD узлов в exported graph (E028).

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f121"></a>

### F121 — Detection-specific KD: FGD даёт доказательство идеи, а не рецепт YOLO

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S083](SOURCES.md#s083). **Исходные IDs:** W1-10-F07.

**W1-10-F07: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: опубликованное измерение.** S083, §4.1–4.3 Table 2. COCO, 80 classes, авторы описывают около 120k train и 5k validation images; supervised boxes, не few-shot. 24 epochs SGD, momentum 0.9, weight decay 0.0001; MMDetection. Teacher RetinaNet ResNet101: 38.9 AP; student ResNet50 baseline 37.4; FGD 39.6, с inheriting neck/head 39.7. APsmall: 20.6 baseline против 22.9 FGD без inheriting. Inheriting требует одинаковой head structure. Полная стоимость teacher training, GPU/time и критерий checkpoint selection здесь не установлены. Appendix E прямо отмечает риск наследования teacher biases. Исследованные здесь студенты не дают основания переносить величину gain на nano YOLO/PPE.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f122"></a>

### F122 — Конкретный FGD route и integration debt

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S084](SOURCES.md#s084), [S085](SOURCES.md#s085). **Исходные IDs:** W1-10-F08.

**W1-10-F08: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: author repo/config.** S084/S085. Репозиторий требует `mmdet==2.11.0`, `mmcv-full==1.2.4`; необходимо добавлять distillation module и заменять `mmdet/apis/train.py`, `tools/train.py`. Это отдельный legacy training stack.

Recipe `configs/distillers/fgd/fgd_retina_r101_fpn_2x_distill_retina_r50_fpn_2x_coco.py`:

- teacher config `configs/retinanet/retinanet_r101_fpn_2x_coco.py`;
- teacher checkpoint `https://download.openmmlab.com/mmdetection/v2.0/retinanet/retinanet_r101_fpn_2x_coco/retinanet_r101_fpn_2x_coco_20200131-5560aee8.pth`;
- student config `configs/retinanet/retinanet_r50_fpn_2x_coco.py`;
- hooks `neck.fpn_convs.0.conv` … `.4.conv` ↔ одноимённые teacher modules, 256→256 channels; `init_student=True`;
- config: `temp=.5`, `alpha_fgd=.001`, `beta_fgd=.0005`, `gamma_fgd=.0005`, `lambda_fgd=.000005`, SGD lr .01, samples_per_gpu 2.

Здесь есть существенное расхождение recipe и paper: для anchor-based one-stage §4.2 paper сообщает gamma 0.001, а pinned recipe — 0.0005. Не исправлять молча; для воспроизведения выбирать и фиксировать конкретный recipe. Это ещё одна причина не подавать paper table как гарантированный результат произвольного переноса.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f123"></a>

### F123 — FGD использует GT geometry, extraction предусмотрен отдельно

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S085](SOURCES.md#s085), [S086](SOURCES.md#s086), [S087](SOURCES.md#s087). **Исходные IDs:** W1-10-F09.

**W1-10-F09: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: код.** S086/S087. Teacher извлекает features под no_grad, student считает свой supervised loss. FGD использует `gt_bboxes` и `img_metas` для foreground/background masks; `FeatureLoss` требует одинаковых H×W, при различии channels добавляет 1×1 align. Поэтому просто подать неполную VLM-предразметку как исчерпывающие GT boxes меняет маски и supervision. Semantic output KD в этом рецепте не выполняется; neck/head inheritance отдельно требует совместимых параметров и ontology. `simple_test` делегирует student; `pth_transfer.py` выбирает только ключи с prefix `student.`, снимает prefix и удаляет optimizer. Финальный graph должен быть обычный RetinaNet R50-FPN; export этого конвертированного checkpoint и LinQ не проверены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f124"></a>

### F124 — Localization distribution KD отличается от hard boxes и class logits

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S088](SOURCES.md#s088). **Исходные IDs:** W1-10-F10.

**W1-10-F10: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: paper measurement.** S088 §4.1/Table 2–3. COCO train2017 118k, val2017 5k; ablations single-scale 1×=12 epochs, GFocal settings; baselines переобучены авторами в тех же условиях. GFocal R101 teacher → R50 student: 40.1 baseline → 42.1 AP при Main KD + Main LD + VLR LD; добавление VLR class KD даёт 42.0. Main class KD отдельно 40.2; Main LD 41.1. LD передаёт распределения границ, а не только decoded teacher box. Для R34→R18 в отдельной абляции pseudo-box regression 35.9 при baseline 35.8 против LD 36.3. Это протокол COCO, не наша оценка; seed variance, teacher-training budget и checkpoint selection не установлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f125"></a>

### F125 — Concrete LD mapping и причина не копировать loss в любой YOLO

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S089](SOURCES.md#s089). **Исходные IDs:** W1-10-F11.

**W1-10-F11: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: код/config.** S089. Recipe `ld_r18_gflv1_r101_fpn_coco_1x.py` строит student ResNet18-FPN/`LDHead`, teacher `configs/gfl/gfl_r101_fpn_mstrain_2x_coco.py`; checkpoint:

https://download.openmmlab.com/mmdetection/v2.0/gfl/gfl_r101_fpn_mstrain_2x_coco/gfl_r101_fpn_mstrain_2x_coco_20200629_200126-dd12f847.pth

Студент: 80 classes, 5 FPN levels, strides `[8,16,32,64,128]`, `reg_max=16`; LD KL weight .25/T=10. Input resize 1333×800 keep_ratio, normalization/pad32. `LDHead.loss_single` reshapes student и teacher box logits в `4*(reg_max+1)` и class logits в одинаковый `cls_out_channels`; locations сопоставляются по сетке/level. Teacher не регистрируется как nn.Module через `__setattr__`, forward_train получает teacher outputs без градиента. В inference используется student single-stage path. Это требует точного совпадения представления/сетки/классов, а не названия «детектор». Checkpoint/export отдельно не запускались.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f126"></a>

### F126 — DFL-free YOLO26 не является drop-in LD student

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S082](SOURCES.md#s082), [S089](SOURCES.md#s089). **Исходные IDs:** W1-10-F12.

**W1-10-F12: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: architecture config + наш вывод.** S082/S089. В pinned YOLO26 `reg_max: 1`, `end2end: True`, три P3–P5 levels. В рассмотренном LD student reg_max16 и пять levels. Следствие: перенос localization-distribution loss требует другой реализации/head contract; установить один коэффициент LD в штатный YOLO trainer недостаточно. Нативный YOLO KD выше использует features и обходит это несовпадение. Менять head ради LD — значит заново исследовать graph/export/исполнение, что существенно для LinQ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f127"></a>

### F127 — Grounding DINO измеряет open-set detection, не достоверность preannotation

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S090](SOURCES.md#s090). **Исходные IDs:** W1-10-F13.

**W1-10-F13: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: опубликованное измерение.** S090 §4.2/Table 2: Grounding-DINO-T/Swin-T, pretrain O365+GoldG+Cap4M, COCO val2017 zero-shot 48.4 AP, fine-tune 57.2. Именно T соответствует предлагаемому ниже OGC teacher path по README model zoo. Более известные 52.5 AP относятся к Swin-L/O365+OI+GoldG, а ODinW mean 26.1 — к другой L-модели с более широким pretraining. Их нельзя приписывать Swin-T checkpoint. Это не качество конкретной каски/респиратора на CCTV и не проверка student после pseudo-label training. Grounding pretraining помогает сформировать кандидатов; маленький/закрытый объект, отношения ношения и отрицательное состояние требуют целевого audit. Teacher benchmark его не заменяет.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f128"></a>

### F128 — Доступный offline teacher path

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S091](SOURCES.md#s091). **Исходные IDs:** W1-10-F14.

**W1-10-F14: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: author README.** S091. Доступны config `groundingdino/config/GroundingDINO_SwinT_OGC.py` и веса `https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth`. README описывает 900 candidate boxes с similarities к input words, `box_threshold` и `text_threshold`, разделение class names точками. Отмечены CPU-only inference и CUDA extension installation; training code в TODO не помечен завершённым. Не утверждается, что README установка работает на нашей ОС/GPU. Этот route выбирается для offline inference/предразметки, а не как доказательство готового fine-tuning trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f129"></a>

### F129 — Слабое место VLM→class IDs конкретно видно в коде

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S092](SOURCES.md#s092). **Исходные IDs:** W1-10-F15.

**W1-10-F15: условия/наблюдение** ([ветка](_WORK/W1/10_TEACHER.md)):

**Тип: код.** S092. `predict` возвращает normalized cxcywh boxes, max token sigmoid scores и phrases; image resize short side800/max1333 с ImageNet normalization. `post_process_result` масштабирует исходными W/H, переводит cxcywh→xyxy. `predict_with_classes` соединяет class names через точки; `phrases2classes` выбирает первый class string, являющийся substring phrase, иначе None. Это не semantic ontology resolver: похожие имена/комбинированные phrases могут ошибочно сопоставиться. Предлагаемый путь в student: explicit phrase→canonical-class table + unknown/review + человек проверяет все целевые instances → YOLO/COCO labels → обычный fine-tuning выбранного student. Ни токен scores, ни совпадение фразы не превращают предразметку в GT.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-11 — W1-11 — Синтетика, copy-paste и domain randomization

<a id="f130"></a>

### F130 — опубликованная постановка/измерение, S093 §§III–IV. Исходный DR — предсказание Cartesian положения геометрических предметов на столе для робота, а не COCO-подобные…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S093](SOURCES.md#s093). **Исходные IDs:** W1-11-F01.

**W1-11-F01: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F130 — опубликованная постановка/измерение, S093 §§III–IV.** Исходный DR — предсказание Cartesian положения геометрических предметов на столе для робота, а не COCO-подобные boxes/PPE states. MuJoCo randomizes текстуры, освещение, distractors, камеру, шум; фиксированная высота стола ограничивает геометрию. Авторы показали перенос simulated RGB → real без real-image pretraining, около 1.5 cm локализационной ошибки и grasping. Эта единица не detection AP. Не переносить её на голову человека или tiny PPE. Точный checkpoint-selection budget и аппаратную стоимость здесь не восстанавливали; работу используем как доказательство принципа в узкой исходной задаче.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f131"></a>

### F131 — метод, S094 §3. Copy-Paste использует instance masks двух изображений после scale jitter/flip, вставляет случайный subset объектов; fully occluded annotations…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S094](SOURCES.md#s094). **Исходные IDs:** W1-11-F02.

**W1-11-F02: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F131 — метод, S094 §3.** Copy-Paste использует instance masks двух изображений после scale jitter/flip, вставляет случайный subset объектов; fully occluded annotations удаляются, partly occluded masks и boxes обновляются. Масштабы/совстречаемость могут быть нереалистичны. Это задача instance segmentation с известными masks, не обещание корректного label после прямоугольной вклейки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f132"></a>

### F132 — опубликованное измерение, S094 §4.1/Table 1. Mask R-CNN ResNet50-FPN, input 1024, COCO train 118k images, LSJ: box/mask AP 47.2/41.8 → 48.2/42.4 с paste. Batch 256;…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S094](SOURCES.md#s094). **Исходные IDs:** W1-11-F03.

**W1-11-F03: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F132 — опубликованное измерение, S094 §4.1/Table 1.** Mask R-CNN ResNet50-FPN, input 1024, COCO train 118k images, LSJ: box/mask AP 47.2/41.8 → 48.2/42.4 с paste. Batch 256; обычно random initialization; обучение до прекращения улучшения validation, для LSJ+paste приведено 576 epochs. Сравнивается augmentation внутри большого COCO recipe, не fine-tuning на нескольких CCTV labels. Детальный аппаратный бюджет и независимое повторение нами не установлены. Числа нельзя смешивать с headline Cascade/self-training result или выдавать за ожидаемый gain YOLO. F131, F132 используют один paper, не два независимых подтверждения.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f133"></a>

### F133 — опубликованное измерение, S095 §4.1/Table 1. Car boxes: Faster R-CNN Inception-ResNet-v2 pretrained ImageNet, 100k DR images против 2.5k Virtual KITTI; AP@0.5 на…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S095](SOURCES.md#s095). **Исходные IDs:** W1-11-F04.

**W1-11-F04: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F133 — опубликованное измерение, S095 §4.1/Table 1.** Car boxes: Faster R-CNN Inception-ResNet-v2 pretrained ImageNet, 100k DR images против 2.5k Virtual KITTI; AP@0.5 на 500 случайно выбранных real KITTI images: DR 78.1 против VKITTI 79.7. Отбор объектов: height >40 px, truncation <0.15. Batch 4, NVIDIA DGX Station; photometric/geometric augmentations. Синтетические budgets не равны. Критически: authors stopped training при saturation на названном test set и report best results; это слабее untouched lockbox.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f134"></a>

### F134 — ограничение/измерение, S095 §4.1–4.2/Fig.6/8. В этой работе real fine-tuning после synthetic улучшал результат, но DR хуже VKITTI при высоком recall; авторская…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S095](SOURCES.md#s095). **Исходные IDs:** W1-11-F05.

**W1-11-F05: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F134 — ограничение/измерение, S095 §4.1–4.2/Fig.6/8.** В этой работе real fine-tuning после synthetic улучшал результат, но DR хуже VKITTI при высоком recall; авторская гипотеза — mismatch структуры/контекста. Рост synthetic size насыщался: примерно 10k с pretraining и 50k без него. Числа относятся к cars/easy-filtered split и указанным detector recipes. Они не обосновывают «сгенерировать миллион» или преодоление tiny-object visibility. Не извлекаем точные значения Fig.6 из смешанного OCR без визуальной сверки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f135"></a>

### F135 — ограничивающее опубликованное измерение, S096 §§4.1–4.3/4.5/Table 3. BlitzNet ResNet50 pretrained ImageNet, input 300, VOC detection/AP при IoU 0.5; cutouts из…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S096](SOURCES.md#s096). **Исходные IDs:** W1-11-F06.

**W1-11-F06: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F135 — ограничивающее опубликованное измерение, S096 §§4.1–4.3/4.5/Table 3.** BlitzNet ResNet50 pretrained ImageNet, input 300, VOC detection/AP при IoU 0.5; cutouts из VOC12train-seg. Table 3: среднее AP первых пяти категорий при отдельном обучении категорий: Base-DA 48.7, Random-DA 48.3, Context-DA 57.5. Это не mAP всех VOC classes. При 25% train images Base/Context 32.5/38.3. Random placement немного ухудшил baseline, context placement помог. Detector Adam; checkpoint rule контекстной модели — divergence train/validation loss. Compute/checkpoint detector для этой строки полностью не восстановлены. Отличие от F131 не разрешается универсальным лозунгом: разные данные, модели, бюджеты и augmentations; для PPE нужен свой controlled comparison.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f136"></a>

### F136 — метод/ограничение, S097 §§5–6/Table 1. Работа об instance detection известных бытовых предметов BigBIRD/GMU Kitchen/Active Vision с Faster R-CNN. Авторы используют…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S097](SOURCES.md#s097). **Исходные IDs:** W1-11-F07.

**W1-11-F07: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F136 — метод/ограничение, S097 §§5–6/Table 1.** Работа об instance detection известных бытовых предметов BigBIRD/GMU Kitchen/Active Vision с Faster R-CNN. Авторы используют foreground masks, paste на backgrounds, вариации blending, rotations, truncation и overlaps. Table 1: same-image multi-blend 73.7 mAP против no blending 65.9 в их протоколе. Удаление contour artifacts оказалось существенным. Это распознавание конкретных предметов, а не категории «человек без каски». Сам по себе реалистичный patch не устанавливает person–PPE relation. Число собственных CCTV labels, экономия annotation time, стоимость на RTX4070 и перенос на LinQ данной работой не установлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f137"></a>

### F137 — метод/протокол, S098 §§3–4.1. X-Paste отделяет генерацию/поиск картинки от получения pseudo masks и фильтрации. Используется StableDiffusion v1.4; несколько…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S098](SOURCES.md#s098). **Исходные IDs:** W1-11-F08.

**W1-11-F08: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F137 — метод/протокол, S098 §§3–4.1.** X-Paste отделяет генерацию/поиск картинки от получения pseudo masks и фильтрации. Используется StableDiffusion v1.4; несколько foreground segmentation методов, CLIP-guided mask selection/filtering; masks с площадью <5% или >95% отбрасываются. Основной ablation recipe: CenterNet2 ResNet50 pretrained ImageNet22k, 640 input, batch32, 48 epochs, LVIS 100k train/20k val. Это большой исходный labeled dataset и дополнительные instance pools, не бесплатная замена target annotation.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f138"></a>

### F138 — опубликованная ablation, S098 Tables 2/5/10. При равном pool size: 300k generated-only → box/mask AP 35.3/31.6; 300k retrieved-real → 36.1/32.0; 150k+150k →…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S098](SOURCES.md#s098). **Исходные IDs:** W1-11-F09.

**W1-11-F09: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F138 — опубликованная ablation, S098 Tables 2/5/10.** При равном pool size: 300k generated-only → box/mask AP 35.3/31.6; 300k retrieved-real → 36.1/32.0; 150k+150k → 36.6/32.7 на LVIS. Более высокий CLIP threshold не монотонно лучше; quality–diversity trade-off. COCO CenterNet2 R50: 46.0/39.8 → 46.6/39.9, заметно меньший gain. GPU cost и checkpoint selection здесь не установлены. Semantic similarity threshold — не вероятность правильного класса/маски. Все числа — авторов, не наша репликация.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f139"></a>

### F139 — метод, S099 §§3.2–3.4. Gen2Det inpaints изображения по исходным boxes/classes; применяет image/detector filtering, separate sampling и background-ignore. После…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W1-11-F10.

**Уточнение W2 к исходному утверждению:** F248–F254: Gen2Det paper RPN+head ignore не inspected trainer. Author artifact gap Q020 открыт; reviewed data-only route отличается.

**W1-11-F10: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F139 — метод, S099 §§3.2–3.4.** Gen2Det inpaints изображения по исходным boxes/classes; применяет image/detector filtering, separate sampling и background-ignore. После удаления ошибочной annotation сам объект остаётся в картинке, а генератор может создать лишние instances. Поэтому авторы меняют training loss; masks для synthetic не известны и mask loss на них выключен. Копировать исходные masks после inpainting неправомерно. Важная переносимость: это специальный Detectron2 training route, не просто папка новых JPG для любого trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f140"></a>

### F140 — ограничивающее измерение, S099 Table 2/5, §4.1/Supp.§6. COCO CenterNet2 box/mask AP: real-only 46.00/39.8, vanilla real+synth 44.35/37.03, полный Gen2Det…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W1-11-F11.

**Уточнение W2 к исходному утверждению:** F249/F250/F251: whole-batch exposure, low-data без filtering/ignore, Table2/Table5 provenance; naive-mix negative result сохранён.

**W1-11-F11: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F140 — ограничивающее измерение, S099 Table 2/5, §4.1/Supp.§6.** COCO CenterNet2 box/mask AP: real-only 46.00/39.8, vanilla real+synth 44.35/37.03, полный Gen2Det 47.18/40.44. LVIS Mask R-CNN box AP: real-only 22.29, naive mix20.75, полный24.42. Есть sampling/recipe confound; результат полного пакета нельзя приписать одним картинкам. Авторы отмечают затруднение воспроизведения точного XPaste результата по опубликованным code/configs. Нашего воспроизведения нет. Не используем их параметры как PPE defaults; аппаратный бюджет/выбор checkpoint здесь не восстановлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f141"></a>

### F141 — наблюдение авторского артефакта, S100 README. Опубликован route generation/text2im.py → segment_methods/reseg.py → filtering/object pool → detector training; нужны…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S100](SOURCES.md#s100). **Исходные IDs:** W1-11-F12.

**W1-11-F12: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F141 — наблюдение авторского артефакта, S100 README.** Опубликован route generation/text2im.py → segment_methods/reseg.py → filtering/object pool → detector training; нужны внешние foreground models и ручное указание их путей. README использует обновление diffusers/transformers/xformers без полного lock. Наличие авторского code подтверждено; воспроизводимость в текущей Windows-среде и готовая интеграция в Ultralytics не проверены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f142"></a>

### F142 — наблюдение авторского артефакта, S101 README. context_aug содержит контекстную CNN и pipeline выбора мест, извлечения VOC instances и paste; основан на BlitzNet,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S101](SOURCES.md#s101). **Исходные IDs:** W1-11-F13.

**W1-11-F13: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F142 — наблюдение авторского артефакта, S101 README.** context_aug содержит контекстную CNN и pipeline выбора мест, извлечения VOC instances и paste; основан на BlitzNet, часть blending borrowed из syndata-generation. Это дополнительный pipeline подготовки, а не встроенная опция любого detector.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f143"></a>

### F143 — источник GT определяет доверие. Renderer даёт точные координаты геометрии в своей сцене, но только при корректном projection/visibility implementation и совпадении…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-11-F15.

**W1-11-F15: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F143 — источник GT определяет доверие.** Renderer даёт точные координаты геометрии в своей сцене, но только при корректном projection/visibility implementation и совпадении ontology. Copy-paste даёт детерминированное преобразование проверенной маски, но меняет перекрытия. Generator даёт изображение, которому ещё нужны проверенные labels. Detector/VLM/CLIP filter оставляет pseudo-label uncertainty. У всех методов отдельный gate: изображение соответствует классу; геометрия соответствует изображению; состояние/отношение соответствует требованиям задачи. Проверка одного уровня не заменяет другие.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f144"></a>

### F144 — : состояние/операция | Допуск и обязательное обновление | Причина отказа

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-11-F16.

**W1-11-F16: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

| F144: состояние/операция | Допуск и обязательное обновление | Причина отказа |
|---|---|---|
| Paste целого person с PPE | Сохранять person ID, head/PPE masks, отношения; один transform для группы; пересчитать clipping/occlusion | Чужая каска потеряла связь с головой; head/PPE исчезли за новым объектом |
| Paste отдельной каски/респиратора | Проверить контакт, pose, размер, orientation и реальную видимость evidence; повторно присвоить state | Каска над/рядом с головой не означает надета; респиратор на шее не означает закрывает дыхательные пути |
| Remove PPE через inpainting | Переразметить результат и появившиеся объекты; проверить восстановленную анатомию и открытый head/face | Prompt «без каски» не доказывает, что генератор действительно создал видимую непокрытую голову |
| Occlusion головы | Согласовать unknown/ignore policy; менять visible mask/box по правилам annotation | Закрытая голова не становится `no_helmet`; отсутствие видимого PPE не доказывает нарушение |
| Перенос человека в ROI | Пересчитать footpoint/ground-plane relation; учитывать perspective, support surface и scale | Box intersect ROI не равен входу; случайный paste может создать человека без физического пола |
| Smoking | Отдельно проверить предмет, hand–mouth geometry и временную семантику | Вклеенная сигарета не подтверждает курение или соседство с горючим материалом |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f145"></a>

### F145 — масштаб и occlusion. До rasterization задать целевой диапазон размера по train-camera observations, после конечного resize/letterbox повторно проверить размер…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-11-F17.

**W1-11-F17: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F145 — масштаб и occlusion.** До rasterization задать целевой диапазон размера по train-camera observations, после конечного resize/letterbox повторно проверить размер evidence. Маска может быть точной, но исчезнувший в двух пикселях ремень уже не даёт человеку надёжно подтвердить state. Не выдумывать универсальный минимальный pixel size. Хранить отдельно amodal geometry и visible geometry; выбирать bbox convention по target dataset, а не механически использовать visible box каждого paste paper. Для частично перекрытого person annotation state может стать unknown даже при большой видимой доле person bbox.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f146"></a>

### F146 — контекст и разнообразие. F131 и F135 дают разные результаты случайного размещения, F138/F140 показывают ограниченную/отрицательную пользу части рецептов. Для…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-11-F18.

**W1-11-F18: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F146 — контекст и разнообразие.** F131 и F135 дают разные результаты случайного размещения, F138/F140 показывают ограниченную/отрицательную пользу части рецептов. Для object-only detection случайная композиция может ослаблять фоновые shortcut; для отношений «надето» и зон она способна разрушать сам label. Разнообразие считать по исходным людям, PPE assets, позам, backgrounds, cameras и sessions; тысяча вариантов одного cutout — не тысяча независимых случаев. Фон holdout камеры нельзя использовать для генерации, а затем называть эту камеру unseen. Если разрешена adaptation на её unlabelled video, это transductive protocol с отдельным session holdout, явно указанным в отчёте.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f147"></a>

### F147 — практический выбор по пробелу. Если нет masks и времени на их проверку, сначала реальная доразметка нужного случая и обычные допустимые transforms; F055 не…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-11-F19.

**W1-11-F19: условия/наблюдение** ([ветка](_WORK/W1/11_SYNTHETIC.md)):

**F147 — практический выбор по пробелу.** Если нет masks и времени на их проверку, сначала реальная доразметка нужного случая и обычные допустимые transforms; F055 не позволяет получить paste одним флагом. Если есть проверенные cutouts и нужен новый фон — group paste, E030/E031. Если не хватает ракурса, которого нет в cutouts, paste не создаёт новую 3D форму; renderer требует assets/rig/camera и отдельной стоимости подготовки. Если нет достоверных реальных примеров состояния вообще, generator может служить поиском гипотез/инструкцией для аннотатора, но не доказательством определения класса. Без real holdout полезность остаётся открытой, даже если synthetic images выглядят убедительно.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-12 — W1-12 — Диагностика training и порядок настройки оптимизации

<a id="f148"></a>

### F148 — Литеральные defaults: конфигурация, а не рекомендация

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S029](SOURCES.md#s029). **Исходные IDs:** W1-12-F01.

**W1-12-F01: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: наблюдение по S029. Область — default.yaml закреплённого дерева; фактический запуск может получить model/task overrides и аргументы пользователя.

| Группа | Значения |
|---|---|
| Budget | `epochs: 100`; `time:` (null); `patience: 100` |
| Batch/input | `batch: 16`; `nbs: 64`; `imgsz: 640`; `multi_scale: 0.0`; `rect: False` |
| Optimizer | `optimizer: auto`; `lr0: 0.01`; `lrf: 0.01`; `momentum: 0.937`; `weight_decay: 0.0005` |
| Warmup | `warmup_epochs: 3.0`; `warmup_momentum: 0.8`; `warmup_bias_lr: 0.1` |
| Schedule/precision | `cos_lr: False`; `amp: True`; `close_mosaic: 10` |
| Reproducibility | `seed: 0`; `deterministic: True`; `compile: False`; `channels_last:` (null) |
| I/O | `workers: 8`; `cache: False`; `fraction: 1.0`; `save: True`; `save_period: -1` |
| Validation/init | `val: True`; `split: val`; `pretrained: True`; `resume: False`; `freeze:` (null) |

Null — отсутствие заданного значения, не строка. `dropout: 0.0` помечен classify-only; это не подтверждённый общий регулятор YOLO detection. В cfg отсутствуют пользовательские `accumulate`, `ema_decay` и `grad_clip` как отдельные аргументы; нельзя выдумывать их CLI. Нужна кастомизация trainer при изменении встроенных механизмов.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f149"></a>

### F149 — Actual auto, LR, accumulation: компактная карта реализации

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-12-F02.

**W1-12-F02: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S011. Локаторы функций указаны в таблице источников. `N=len(train_loader.dataset)`, `B=self.batch_size` (общий batch), `E=self.epochs`:

| Механизм | Реальная формула / развилка |
|---|---|
| Оценка iterations для auto | `ceil(N/max(B,nbs))*E` |
| `iterations > 10000` | `MuSGD`, LR=0.01, momentum=0.9 |
| Иначе, включая ровно 10000 | `AdamW`, LR=`round(0.002*5/(4+nc),6)`, beta1=0.9 |
| auto side effect | Переписывает args.optimizer/args.lr0; `warmup_bias_lr=0.0`; ручной lr0 игнорируется |
| Номинальное accumulation | `max(round(nbs/B),1)`; без time ограничено сверху `len(loader)*E` |
| Decay | `weight_decay*B*accumulate/nbs`; веса decay, bias/нормализации без decay |
| Linear factor | `max(1-epoch/E,0)*(1-lrf)+lrf` |
| Cosine | `cos_lr=True` → one_cycle(1,lrf,E) |
| Warmup length | `round(min(warmup_epochs,max(E-1,0))*len(loader))`; нет старого minimum 100 iterations |
| Warmup | accumulation 1→nominal; LR bias/other стартуют warmup_bias_lr/0 → initial_lr*factor; momentum-group 0.8→args.momentum |
| Step | `ni-last_opt_step >= accumulate`; unscale→clip norm 10→scaler.step→scaler.update→zero_grad→EMA |

Здесь formula iterations — эвристическая оценка количества optimizer updates, не буквально число minibatches. Поэтому сравнение эпох/датасетов с `optimizer=auto` может одновременно менять оптимизатор и LR: это confound, который надо записать или исключить явным optimizer. `lrf` — множитель, не абсолютный LR; дискретный последний epoch не обязан иметь ровно lr0*lrf.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f150"></a>

### F150 — Какие дополнительные confounds проверить по S011

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-12-F03.

**W1-12-F03: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: вывод из реализации, требующий наблюдения будущего запуска. В auto локальная momentum для построения optimizer=0.9, но warmup для momentum-bearing groups читает args.momentum (default 0.937). AdamW хранит betas, а не поле momentum, поэтому эта ветка warmup не изменяет beta1. При ручном AdamW default lr0 остаётся 0.01, если явно не переопределить: комментарий «Adam/AdamW=1e-3» не меняет YAML.

Для MuSGD код выделяет matrix/conv параметры и может давать части classification-head groups LR×3; одного общего LR из console недостаточно — сохранять все param_groups. Значение batch нельзя подменять одним effective batch: microbatch меняет BN и stochastic transforms, а округление accumulation/warmup, число шагов и decay могут различаться. Простая линейная масштабировка LR по batch не следует автоматически из этого trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f151"></a>

### F151 — AMP: successful check не означает проверку нашего training

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S081](SOURCES.md#s081), [S102](SOURCES.md#s102), [S106](SOURCES.md#s106). **Исходные IDs:** W1-12-F04.

**W1-12-F04: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S102, S081. check_amp использует `yolo26n.pt` и `bus.jpg`, сравнивая FP32/AMP inference boxes: одинаковая shape и allclose с atol=0.5. Это проверка среды на суррогате. Assertion failure выключает AMP; CPU/MPS возвращают False. ConnectionError или AttributeError/ModuleNotFoundError приводят к skip warning и возврату True: статус skipped нельзя пересказать как passed. Возможна одноразовая загрузка surrogate weights.

Тип: code observation S011/S081. `amp=True`/`fp16` запускают check; `False`/`fp32` отключают; `bf16` идёт другим маршрутом, без GradScaler, с проверкой native CUDA bf16 и PyTorch≥1.13 внутри autocast. Поддержку нашей среды надо измерить. AMP — точность обучения, не утверждение о типе конечного LinQ artifact.

Тип: documentation S106. До проверки/clip градиентов их надо unscale; unscale только один раз на optimizer step, после накопления всех microbatches. Масштаб должен оставаться постоянным внутри effective batch; step/update — на его границе. scaler.step может пропустить update при Inf/NaN. Поэтому полезно наблюдать не только loss и scaler scale, но и реальное изменение веса. Нельзя при диагностическом hook второй раз вызывать unscale поверх trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f152"></a>

### F152 — EMA, checkpoint и early stop

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S081](SOURCES.md#s081), [S103](SOURCES.md#s103), [S104](SOURCES.md#s104). **Исходные IDs:** W1-12-F05.

**Уточнение W2 к исходному утверждению:** F272/F273/F274/F275/F276/F277: точный lifecycle. Pre-strip EMA вместо online, scheduler/RNG/loader не сохраняются; boolean resume stripped может стать new training.

**W1-12-F05: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S081/S104/S103. ModelEMA — eval-копия FP32, параметры без requires_grad; decay=`0.9999*(1-exp(-updates/2000))`, плавающие параметры и buffers обновляются на каждом вызове EMA.update. Training validation получает EMA. Detection fitness — mAP50:95: веса `[0,0,0,1]` для P/R/mAP50/mAP50:95. Это не event recall, редкий класс или число ложных тревог.

EarlyStopping: trainer передаёт cfg patience=100, хотя constructor default=50. `patience=0` отключает. Улучшение — строго `fitness > best_fitness`, с исключением `best_fitness==0`: нулевое плато продолжает обновлять best_epoch. При fitness=None stop=False; possible_stop за epoch до patience; штатный stop при delta≥patience. Встроенный early stop поэтому не заменяет ручной stop rule для нулевого mAP и не гарантирует разумный бюджет короткого кейса.

Тип: code observation S011/S081. EMA.update вызывается после scaler.step/update без отдельной проверки, был ли optimizer update пропущен scaler; EMA.updates поэтому нельзя автоматически считать числом успешных обновлений online weights. В активном checkpoint сохраняются EMA, optimizer, scaler и stopper state; окончательная final_eval strips optimizer у last/best. strip_optimizer заменяет model на EMA, очищает optimizer/scaler/stopper, ставит epoch=-1. **Завершённый best.pt — не полная точка точного resume.** Факт успешной загрузки для inference не равен восстановлению trajectory; при необходимости продолжения нужна отдельно сохранённая пригодная незавершённая точка и manifest.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f153"></a>

### F153 — close_mosaic и лимиты короткого run

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S031](SOURCES.md#s031). **Исходные IDs:** W1-12-F06.

**W1-12-F06: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S031; scheduler boundary — S011. При входе в последние close_mosaic epochs (`epoch >= epochs-close_mosaic`) loader закрывает augmentation и reset. YOLODataset.close_mosaic обнуляет сразу mosaic/copy_paste/mixup/cutmix, перестраивая transforms. `close_mosaic=0` сохраняет исходный режим, а не выключает mosaic. При E≤10 и default close_mosaic=10 условие выполнено с epoch 0: короткая проба не проверяет то же расписание сильных аугментаций, что длинная. Остальные transforms автоматически не обнуляются.

Тип: вывод. Early stopping может завершить training до запланированной финальной фазы без mosaic; факт заданного close_mosaic не доказывает прохождение этой фазы. Сравнение коротких trials требует фиксировать эффективное расписание, а не только args. Полезность конкретной augmentation → W1-05, здесь разобрана механика.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f154"></a>

### F154 — Resume/OOM/NaN нельзя считать прозрачным продолжением

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-12-F07.

**Уточнение W2 к исходному утверждению:** F276: freeze входит в resume whitelist; новый LR/optimizer/epochs нет. Новая stage2 с новым recipe — resume=False, unfreeze в прежнем run технически разрешён.

**W1-12-F07: условия/наблюдение** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):

Тип: code observation S011. check_resume берёт checkpoint args и разрешает только whitelist overrides; optimizer/LR/schedule туда не входят. Для их изменения нужен новый run, иначе warning об ignored overrides. Это существенно при freeze→unfreeze: новый режим надо задавать и проверять сознательно (подробнее W1-02).

В первом epoch single-device trainer может до трёх раз уменьшить batch вдвое после OOM/backend-memory-error и перестроить pipeline; позже и в DDP error пробрасывается. NaN recovery использует last.pt, не может восстановиться в первом epoch, проверяет finite checkpoint и имеет предел трёх последовательных recovery. Следовательно, наличие завершившегося процесса не заменяет осмотр log: фактические batch/перезапуски могли отличаться от плана. Ручной диагностический stop на первом неfinite ниже намеренно строже автоматического восстановления.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-13 — W1-13 — PTQ/QAT, pruning и целевое исполнение

<a id="f155"></a>

### F155 — Представление ONNX quantization [документация S110]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S110](SOURCES.md#s110). **Исходные IDs:** W1-13-F01.

**W1-13-F01: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

QOperator использует отдельные quantized operators, например `QLinearConv` и `MatMulInteger`. QDQ вставляет `QuantizeLinear`/`DequantizeLinear`. Документация связывает QDQ также с некоторыми экспортами QAT. Наличие QDQ не означает, что каждый оператор реально исполняется целочисленно или что выбранный backend его примет.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f156"></a>

### F156 — PTQ и QAT [документация S110]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S110](SOURCES.md#s110). **Исходные IDs:** W1-13-F02.

**W1-13-F02: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Static PTQ получает activation ranges на calibration inputs; dynamic рассчитывает параметры во время inference с дополнительной работой. ORT рекомендует static для CNN, dynamic для RNN/transformers, но это рекомендация ORT. QAT предлагается при неудовлетворительном PTQ; retraining выполняется исходным framework, ORT здесь не является QAT trainer.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f157"></a>

### F157 — Подготовка и потеря точности [документация S110]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S110](SOURCES.md#s110). **Исходные IDs:** W1-13-F03.

**W1-13-F03: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Shape inference и отдельная предварительная оптимизация облегчают quantization/debugging; fusion Conv+BN изменяет граф. Quantization не сохраняет точность гарантированно. Поддержка и выигрыш зависят от hardware/runtime; рекомендации S8S8/QDQ для ORT CPU не являются настройками LinQ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f158"></a>

### F158 — Реальные параметры ORT `v1.23.2` [код S111, чтение без запуска]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S111](SOURCES.md#s111). **Исходные IDs:** W1-13-F04.

**W1-13-F04: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Подпись `quantize_static`: `calibration_data_reader`, `quant_format=QuantFormat.QDQ`, `per_channel=False`, `reduce_range=False`, `activation_type=QuantType.QInt8`, `weight_type=QuantType.QInt8`, `calibrate_method=CalibrationMethod.MinMax`, `nodes_to_quantize=None`, `nodes_to_exclude=None`, `op_types_to_quantize=None`, `use_external_data_format=False`, `calibration_providers=None`, `extra_options=None`. Это установленные defaults выбранного tag, не оптимум детектора.

У API есть выбор операторов и исключения узлов: допустимо исследовать selective quantization при локализованной деградации, если target compiler допускает соответствующий mixed graph. Наличие параметра в ORT не устанавливает такую возможность LinQ. Код main из поисковой выдачи не использован для переноса новых параметров в tag.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f159"></a>

### F159 — Calibration data contract [код S112]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S112](SOURCES.md#s112). **Исходные IDs:** W1-13-F05.

**Уточнение W2 к исходному утверждению:** F256: найден reconstruction QAT без detector GT loss. Labels нужны quality measurement, но не каждому QAT objective; supervised QAT — другой contract.

**W1-13-F05: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

`CalibrationDataReader.get_next()` возвращает dict inputs для ONNX inference; `None` завершает итерацию. Enum выбранного tag включает `MinMax`, `Entropy`, `Percentile`, `Distribution`; список enum шире краткого веб-описания. Само наличие enum не является оценкой пользы метода или универсальной поддержкой downstream.

Аннотации не входят в этот интерфейс. Наш вывод: нужны корректные фактические model inputs; labels требуются отдельно для оценки качества и обучающего QAT loss. Calibration pool должен быть отделён от независимой проверки; подбор метода по validation делает validation частью разработки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f160"></a>

### F160 — Локализация расхождения [код S113]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S113](SOURCES.md#s113). **Исходные IDs:** W1-13-F06.

**W1-13-F06: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Модуль предназначен сравнивать веса/активации FP и quant graph на одинаковых inputs. В нём есть добавление промежуточных outputs, сбор активаций и matching. Наш вывод: сравнивать нужно одинаковую стадию графа; различия после отдельной FP-оптимизации не следует приписывать только quantization. Для LinQ доступность intermediates и соответствие tensor names ещё неизвестны.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f161"></a>

### F161 — `.ort` не синоним INT8 [документация S114]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S114](SOURCES.md#s114). **Исходные IDs:** W1-13-F07.

**W1-13-F07: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

ORT format предназначен в том числе для уменьшенных сборок ORT; полная сборка читает ONNX и ORT. Конвертер загружает/оптимизирует ONNX, пишет `.ort` и operator configuration для reduced build. Это отдельная ось от QDQ/QOperator и разрядности; хранить FP ONNX до такой конвертации необходимо для переносимого дальнейшего маршрута. Поддержка `.ort` LinQ не установлена.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f162"></a>

### F162 — F162 — «Structured pruning» инструмента может означать маску [документация S115 и код S116]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S115](SOURCES.md#s115), [S116](SOURCES.md#s116). **Исходные IDs:** W1-13-F08, W1-13-F09.

**W1-13-F08: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Tutorial показывает `ln_structured(..., n=2, dim=0)` с занулением целых output channels. Маска и original parameters сериализуются. `remove` закрепляет pruned weight и убирает reparameterization; tutorial не утверждает уменьшение размерности слоя.

Закреплённый код подтверждает: `apply_mask` умножает original tensor на mask; `LnStructured.compute_mask` создаёт mask той же формы. Значит этот API сам по себе не делает graph surgery с удалением каналов/соединений. Даже structured mask нельзя выдавать за компактный плотный экспорт. Это наблюдение по коду, а не замер размера файла или runtime.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f163"></a>

### F163 — Нули и sparse kernels [авторское техническое объяснение S117]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S117](SOURCES.md#s117). **Исходные IDs:** W1-13-F10.

**W1-13-F10: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

PyTorch объясняет, что dense kernels продолжают обрабатывать занулённые элементы. Ускорение sparsity требует compressed representation и соответствующих sparse kernels. 2:4 — специальный pattern с не более двух ненулевых значений в группе четырёх; описанная аппаратная ветка относится к NVIDIA и библиотечной поддержке. Нельзя переносить её на LinQ или любой Conv graph.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f164"></a>

### F164 — Физическое удаление фильтров [первичная работа S118]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S118](SOURCES.md#s118). **Исходные IDs:** W1-13-F11.

**W1-13-F11: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Работа удаляет целые filters и соответствующие feature maps, получая меньшие dense operations вместо irregular sparsity. Это основание отличать архитектурное уменьшение от маски; в статье исследуются классификационные CNN/CIFAR/ImageNet, не наш PPE detector. Числа выигрыша из abstract не используются как прогноз скорости LinQ. Для detection neck/head, residual/concat связей и малых объектов нужен отдельный корректный путь graph surgery, fine-tuning и проверки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f165"></a>

### F165 — Что QAT должно моделировать [первичная работа S119]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S119](SOURCES.md#s119). **Исходные IDs:** W1-13-F12.

**W1-13-F12: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Fig.1.1 и §3 описывают simulated quantization в FP training, включая weights и activations; inference scheme использует integer arithmetic. Метод совместно проектируется с целевой арифметикой, а не просто понижает dtype обучаемых параметров. Работа рассматривает MobileNet classification и COCO detection на CPU; она не подтверждает SDK LinQ. Наш вывод: до QAT нужны требования rounding/clipping, scales/zero points, fusion placement и поддерживаемого экспортера. Сам fake-quant checkpoint ещё не deploy artifact.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f166"></a>

### F166 — F167 — Что публично заявляет LinQ [заявление производителя S120/S121]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S120](SOURCES.md#s120), [S121](SOURCES.md#s121). **Исходные IDs:** W1-13-F13.

**W1-13-F13: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Tech page называет int8 IP-ядро и включает `yolo5s`, `yolo8`, `yolo11` в список сетей. Datasheet HPS описывает PyTorch→ONNX→LinQ Compiler, DNN Quant для int8, а также Developer SDK/портал. Это публичные заявления о семействе/стеке без версии и exact model graph.

Проверенные разделы не раскрывают accepted opset, QDQ/QOperator, signedness, per-tensor/per-channel axes, calibration format/algorithm, экспорт QAT, fallback и sparse formats. SDK не получен. Слово «поддержка ONNX» не заменяет operator/version matrix. Информация HPS не устанавливает, что организаторы выдадут HPS или идентичный software stack.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f167"></a>

### F167 — F167 — Что публично заявляет LinQ [заявление производителя S120/S121]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S120](SOURCES.md#s120), [S121](SOURCES.md#s121). **Исходные IDs:** W1-13-F14.

**W1-13-F14: условия/наблюдение** ([ветка](_WORK/W1/13_COMPRESSION.md)):

Tech page называет int8 IP-ядро и включает `yolo5s`, `yolo8`, `yolo11` в список сетей. Datasheet HPS описывает PyTorch→ONNX→LinQ Compiler, DNN Quant для int8, а также Developer SDK/портал. Это публичные заявления о семействе/стеке без версии и exact model graph.

Проверенные разделы не раскрывают accepted opset, QDQ/QOperator, signedness, per-tensor/per-channel axes, calibration format/algorithm, экспорт QAT, fallback и sparse formats. SDK не получен. Слово «поддержка ONNX» не заменяет operator/version matrix. Информация HPS не устанавливает, что организаторы выдадут HPS или идентичный software stack.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-14 — W1-14 — GPU, независимые trials, DDP и цена информации

<a id="f168"></a>

### F168 — DDP не объединяет память в одну GPU. Документация S122 описывает синхронизацию градиентов между replicas и рекомендует отдельный процесс на GPU; входы необходимо…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S122](SOURCES.md#s122). **Исходные IDs:** W1-14-F01.

**W1-14-F01: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F168 — DDP не объединяет память в одну GPU.** Документация S122 описывает синхронизацию градиентов между replicas и рекомендует отдельный процесс на GPU; входы необходимо распределять sampler-ом. Из этого следует: обычное DDP не решает случай, когда одна модель/её состояния не помещаются на одном устройстве; это уже вопрос другого memory strategy. Дополнительные GPU делят работу над данными, а не автоматически слой/параметры. Тип: documentation → наш вывод.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f169"></a>

### F169 — accumulation и коммуникация различаются. S122: `no_sync()` подавляет gradient synchronization в накопительных проходах; forward тоже должен быть внутри context. DDP…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S122](SOURCES.md#s122). **Исходные IDs:** W1-14-F02.

**W1-14-F02: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F169 — accumulation и коммуникация различаются.** S122: `no_sync()` подавляет gradient synchronization в накопительных проходах; forward тоже должен быть внутри context. DDP усредняет градиенты, поэтому суммируемый и усредняемый loss требуют различать. Это интерфейс PyTorch, а не обещание его применения любым trainer. Тип: documentation.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f170"></a>

### F170 — конкретный trainer меняет смысл сравнения. По S011: global batch делится на world size; AutoBatch `<1` отвергается в multi-GPU, `rect=True` принудительно становится…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W1-14-F03.

**W1-14-F03: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F170 — конкретный trainer меняет смысл сравнения.** По S011: global batch делится на world size; AutoBatch `<1` отвергается в multi-GPU, `rect=True` принудительно становится False. Nominal accumulate = max(round(nbs/global_batch),1), затем есть ограничение длительностью; warmup меняет accumulate. Перед backward distributed loss умножается на world size. В прочитанном `_do_train` нет `no_sync`: backward выполняется каждый microbatch, optimizer — по accumulate. Нельзя обещать сокращение all-reduce до одного на update; проверять trace. Тип: code observation, без запуска.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f171"></a>

### F171 — effective batch — бухгалтерия экспозиций, не гарантия эквивалентности. При полных равных microbatches приблизительно B_update = world_size × local_microbatch ×…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S129](SOURCES.md#s129). **Исходные IDs:** W1-14-F04.

**W1-14-F04: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F171 — effective batch — бухгалтерия экспозиций, не гарантия эквивалентности.** При полных равных microbatches приблизительно B_update = world_size × local_microbatch × accumulation. Для S011 global batch уже включает world size: второй раз умножать `args.batch` на число GPU нельзя. Хвосты, padding sampler, warmup и retries требуют журналировать фактические sample IDs/optimizer steps. S129: BatchNorm считает статистики по mini-batch в forward. Наш вывод: накопление нескольких forwards не превращает их BN-statistics в статистики одного большого batch. Даже при равном B_update могут измениться порядок примеров, stochastic augmentation, число обновлений, LR schedule и численные ошибки. Детали optimizer/AMP/EMA — W1-12, не повторяются как новый recipe.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f172"></a>

### F172 — sampler имеет цену корректности. По S124 DistributedSampler при drop_last=False добавляет индексы до делимости по replicas; при True отбрасывает хвост. Для нового…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S124](SOURCES.md#s124), [S127](SOURCES.md#s127). **Исходные IDs:** W1-14-F05.

**W1-14-F05: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F172 — sampler имеет цену корректности.** По S124 DistributedSampler при drop_last=False добавляет индексы до делимости по replicas; при True отбрасывает хвост. Для нового shuffle нужен `set_epoch` до итерации. По S127 train использует DistributedSampler при shuffle, loader ограничивает фактический batch размером dataset; S011 вызывает set_epoch. Наш вывод: считать уникальные кадры, processed images и optimizer updates отдельно, особенно на tiny set; DDP не создаёт новые независимые сцены. Тип: docs/code → inference.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f173"></a>

### F173 — workers/prefetch — измеряемые настройки. S127 сохраняет workers между итерациями InfiniteDataLoader; фактическое число ограничено CPU/device count, запрошенными…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S124](SOURCES.md#s124), [S127](SOURCES.md#s127). **Исходные IDs:** W1-14-F06.

**W1-14-F06: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F173 — workers/prefetch — измеряемые настройки.** S127 сохраняет workers между итерациями InfiniteDataLoader; фактическое число ограничено CPU/device count, запрошенными workers и числом batches; при единственном batch workers=0. Prefetch factor при workers>0 равен 4 для shuffle и 2 иначе; pin_memory включается только при доступном accelerator. S124 предупреждает о дополнительной памяти процессов и OS-dependent multiprocessing; pin_memory ускоряет передачу поддержанных tensors в CUDA. Больше workers не является универсальным ускорением. Тип: code/docs.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f174"></a>

### F174 — cache имеет прогрев, объём и версии. По S126 disk cache пишет декодированный `.npy`, проверяя mtime; существующий свежий `.npy` может читаться даже при другом cache…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S126](SOURCES.md#s126). **Исходные IDs:** W1-14-F07.

**W1-14-F07: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F174 — cache имеет прогрев, объём и версии.** По S126 disk cache пишет декодированный `.npy`, проверяя mtime; существующий свежий `.npy` может читаться даже при другом cache mode. RAM cache пакуется в `_ImageCache`: contiguous tensor, sharing с loader workers; при недостаточном Linux `/dev/shm` сериализация может перейти к копированию. Есть предупреждение о nondeterministic RAM caching. Это не доказательство единственного cache на все DDP ranks: dataset создаётся процессами. Наш вывод: cache=False не равнозначен доказанному холодному диску; измерять RAM по процессам, shared memory, disk bytes и начало run отдельно. Не применять старые issues о копировании памяти к новой версии без проверки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f175"></a>

### F175 — profiler изменяет наблюдаемую систему. S123 даёт CPU/CUDA activities, расписание wait/warmup/active, trace export. `record_shapes`/`with_stack` добавляют overhead;…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S123](SOURCES.md#s123). **Исходные IDs:** W1-14-F08.

**W1-14-F08: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F175 — profiler изменяет наблюдаемую систему.** S123 даёт CPU/CUDA activities, расписание wait/warmup/active, trace export. `record_shapes`/`with_stack` добавляют overhead; сохранение shapes может удерживать ссылки на tensors и менять память. Для CUDA trace нужен поддержанный backend/CUPTI; отсутствие kernel trace не доказывает отсутствие GPU работы. Наш вывод: локализовать bottleneck trace-ом, итоговый throughput повторить без profiler. Тип: docs → inference.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f176"></a>

### F176 — корректный timing должен дождаться GPU. S128: CUDA operations асинхронны, поэтому CPU timer вокруг enqueue без synchronization недостоверен. Документация показывает…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S128](SOURCES.md#s128). **Исходные IDs:** W1-14-F09.

**W1-14-F09: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F176 — корректный timing должен дождаться GPU.** S128: CUDA operations асинхронны, поэтому CPU timer вокруг enqueue без synchronization недостоверен. Документация показывает CUDA Events и synchronize. Наш вывод: для end-to-end окна дождаться устройства на границах; для device-only времени использовать events. Не вставлять synchronize после каждой операции при измерении обычного pipeline: это меняет overlap. Тип: docs → instrumentation proposal.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f177"></a>

### F177 — seed не гарантирует перенос повторяемости. S125 не обещает идентичность между релизами, commits, платформами, CPU/GPU даже при одинаковом seed; детерминизм может…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S125](SOURCES.md#s125), [S131](SOURCES.md#s131). **Исходные IDs:** W1-14-F10, W1-15-F03.

**W1-14-F10: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F177 — seed не гарантирует перенос повторяемости.** S125 не обещает идентичность между релизами, commits, платформами, CPU/GPU даже при одинаковом seed; детерминизм может снижать скорость. Наш вывод: одинаковый seed на local/cloud нужен как контроль, но не служит доказательством равенства обучения. Повтор seed на одном split изучает training randomness; повтор независимых камер/сессий отвечает на другой вопрос. Тип: docs → inference; протокол качества передать evaluation/W1-15.

**W1-15-F03: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: документация S131.** Идентичный seed не гарантирует совпадение между releases/commits/platforms либо CPU и GPU. PyTorch, Python, NumPy и отдельные NumPy Generator имеют свои источники случайности; DataLoader требует осознанного worker/generator seeding. Отключение cuDNN benchmark не равно включению deterministic algorithms; детерминированный режим может замедлять и выдавать ошибку для неподдержанной операции.

**Наш вывод:** сохранять среду и фактические настройки; утверждение «воспроизводится» ограничивать зафиксированной средой и измеренным допуском. Детерминизм нужен для диагностики пары, а повтор optimization seeds — для оценки чувствительности; это разные цели.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f178"></a>

### F178 — живая документация требует environment gate. S105 сообщает ограничение Windows multi-GPU с official PyTorch wheels >=2.4 из-за libuv/TCPStore и предлагает…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S105](SOURCES.md#s105). **Исходные IDs:** W1-14-F11.

**W1-14-F11: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F178 — живая документация требует environment gate.** S105 сообщает ограничение Windows multi-GPU с official PyTorch wheels >=2.4 из-за libuv/TCPStore и предлагает Linux/WSL2. Она также предупреждает: custom trainer/dataset/augmentation не переносятся автоматически во внутренний DDP subprocess, нужен явный distributed launch пользовательского script. Это vendor documentation, не локальная проверка и не утверждение об ОС команды. Поле `profile` описано как ONNX/TensorRT speed profiling; оно не заменяет исследование loading/backward/communication и не измеряет LinQ.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f179"></a>

### F179 — распределять ресурс по ожидаемому изменению решения. Рабочая карточка каждого trial: «неизвестное → две различимые причины → один изменяемый фактор → что решаем при…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W1-14-F12.

**W1-14-F12: условия/наблюдение** ([ветка](_WORK/W1/14_COMPUTE.md)):

**F179 — распределять ресурс по ожидаемому изменению решения.** Рабочая карточка каждого trial: «неизвестное → две различимые причины → один изменяемый фактор → что решаем при каждом исходе → цена → срок полезности результата». Не запускать пять отличающихся многими параметрами recipes только ради занятых GPU. Не назначать численные вероятности успеха без данных. Приоритет выше у проверки, которая открывает или закрывает несколько последующих веток и успевает повлиять на интеграцию.

| Альтернатива | Когда её знание ценнее | Реальные статьи затрат, которые измерить | Условие продолжения |
|---|---|---|---|
| Независимые hypotheses, по одному GPU | Причина ошибки неизвестна: labels, scale, source/target, sampling | Подготовка каждого config, перенос dataset, короткий train, validation и разбор | Кандидат меняет нужный error slice при контролях; затем подтверждение |
| Дополнительные seeds | Разница кандидатов мала/нестабильна, выбор уже сужен | Полные paired repeats обоих кандидатов, оценка; не только выигравшего | Эффект согласован с правилом W1-15; иначе сохраняем неопределённость |
| Более длинный run | Проверены pipeline и labels, validation ещё улучшает нужные метрики | Дополнительные epochs плюс validation/checkpoint и позднее изменение recipe | Улучшение не ограничено train loss и не съедает время export/integration |
| DDP одного run | Установленный рецепт слишком медленен на критическом пути | Setup, all-reduce, sampler/BN checks, storage, дополнительные GPU-hours | Измеренное end-to-end ускорение даёт полезный результат раньше дедлайна |
| Ручная разметка/QA | Ошибки отражают missing/wrong labels, новый домен, мало разнообразия | Отбор, annotation, adjudication, export и повтор train; считать минуты и независимые группы | Ошибки исправлены и улучшение на нетронутом материале |
| Teacher/offline prelabel | Teacher закрывает нужный пробел с проверяемыми labels/student | Setup, inference по пулу, storage, ручная коррекция, student train/validation | Пригодный student улучшен; teacher AP сам по себе недостаточен |

DDP и независимые trials могут сочетаться: сначала небольшие раздельные проверки, затем распределённый финальный кандидат. Это не фиксированный план по часам. Для пяти человек общий дефицит может быть в review/annotation/доступе SDK: ещё один GPU не ускоряет последовательное согласование класса и compile gate. Резерв на validation/export/демо задаётся по реальному критическому пути, не по выдуманной универсальной доле времени.

### Измеримая экономика без выдуманных тарифов

Обозначить T_setup (env/data transfer/cache/DDP startup), T_train, T_validation, T_save, T_export_verify и H_review/H_annotation в person-minutes. Полезный результат приходит через T_ready = T_queue + T_setup + T_train + T_validation + T_save + T_export_verify + T_decision. Некоторые части перекрываются: хранить и timestamps, и critical path, а не механически складывать все задачи команды.

Для N одинаково оплачиваемых GPU: GPU-hours = N × оплачиваемое wall time в часах; денежная цена = GPU-hours × подтверждённый тариф + storage/network/минимальный billing interval/неудалённый instance. Тариф и условия доступа здесь не получены, поставщик не выбран. Учесть charging setup/idle/failure и срок жизни диска по реальным условиям будущего провайдера. Не объявлять локальный GPU бесплатным в смысле доступности: он может блокировать demo/debug.

Для одинакового объёма работы S_N=T_1/T_N и efficiency=S_N/N. Это только throughput comparison при сопоставимом workload, не quality scaling. DDP быстрее по wall-clock, но при S_N<N расходует больше GPU-hours. Для k одинаковых trials на k GPU независимый режим может дать k результатов примерно за длительность одного trial только при отсутствии очереди и общей CPU/storage/network конкуренции. Проверить это E042, а не обещать.

Кэш окупается по времени, если T_build + R×T_epoch_cached < R×T_epoch_uncached для реального числа повторов R; расходы на хранение/копирование и инвалидирование учитываются отдельно. При короткой проверке T_build может превышать всю экономию. При облачном cache на network filesystem требуются реальные read/write throughput и persistence; локальный SSD не предполагается.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W1-15 — W1-15 — Checkpoint, независимость сравнения и завершение адаптации

<a id="f180"></a>

### F180 — Название seed в FsDet не означает только seed обучения

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S130](SOURCES.md#s130). **Исходные IDs:** W1-15-F02.

**W1-15-F02: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: code/documentation S130.** `datasets/README.md` описывает 29 дополнительных VOC training-shot групп к исходной, COCO — 10 групп с exactly K instances/category. В `get_config(seed, shot)` seed включается в имя `DATASETS.TRAIN`; для output/config создаются отдельные пути. Значит, механически перенести сравнение «много seeds» как повтор одного неизменного train set было бы неверно. Само чтение этой функции не устанавливает все RNG всего trainer.

**Наш вывод из F009/F180:** в manifest отдельно хранить `training_sample_seed`, `training_manifest_hash`, `optimization_seed`, `split_manifest_hash`, `evaluation_resampling_seed`. Смена sample при том же optimization seed отвечает на иной вопрос. При нескольких clips одного эпизода K boxes нельзя интерпретировать как K независимых наблюдений.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f181"></a>

### F181 — Validation становится частью выбора модели

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S132](SOURCES.md#s132). **Исходные IDs:** W1-15-F04.

**W1-15-F04: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: методологическая работа S132.** Оптимизация noisy finite-sample model-selection criterion может переобучиться сама; выбор и оценка на одном материале дают selection bias. Авторская рекомендация рассматривать model-selection procedure как часть обучения мотивирует независимую внешнюю оценку. Эксперименты статьи не дают количественной оценки bias нашего detection pipeline.

**Наш вывод:** checkpoint/epoch, architecture, data mixture, confidence, NMS и temporal rule — всё, что меняют по результатам набора, входит в selection. Набор после многократного просмотра ошибок является рабочей validation. Назвать его test и зафиксировать seed недостаточно. Lockbox после открытия для диагностики больше не закрытая независимая проверка будущих исправлений.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f182"></a>

### F182 — Единица независимости должна соответствовать задаче переноса

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S133](SOURCES.md#s133). **Исходные IDs:** W1-15-F05.

**W1-15-F05: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: документация S133.** Group-wise validation не допускает одну группу в train и validation; обычное i.i.d. разбиение некорректно для зависимых групп. Близкие во времени наблюдения коррелированы; time-aware проверка отвечает на другой вопрос, чем случайный split.

**Наш протокол для CCTV:** camera/session/episode IDs строятся до извлечения frames/crops. Все потомки кадра и одного эпизода наследуют partition. Для новой камеры удерживается camera целиком; для будущего времени на известной камере удерживается более поздняя session с временным разрывом. Разные временные куски той же камеры не подтверждают unseen-camera перенос. Exact/perceptual duplicate audit дополняет IDs. Если камер мало, несколько «session groups» не превращают их в большое число независимых cameras. Target unlabeled adaptation тоже раскрывается: использованные потоки нельзя молча назвать полностью unseen.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f183"></a>

### F183 — Парность сохраняется и при оценке неопределённости

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S134](SOURCES.md#s134). **Исходные IDs:** W1-15-F06.

**W1-15-F06: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: API documentation S134.** `paired=True` использует одинаковые resampled indices для всех входных массивов; обычное независимое resampling разрушает соответствие пары. Документация предупреждает о degenerate bootstrap distributions, для которых BCa interval может быть NaN.

**Наш проект процедуры:** для одинаковых camera/session groups сравнивать `Delta=M(candidate)-M(baseline)`, resample независимые группы с возвращением и включать обе модели для каждого выбранного group. Для AP заново агрегировать GT/predictions всей resample с корректными уникальными image IDs, а не усреднять image-AP; для rates пересчитывать сумму counts/сумму exposure. Интервал bootstrap характеризует наблюдаемый домен/выбранную единицу; несколько камер и нулевые rare positives не дают надёжного population claim. Frame bootstrap здесь не заменяет group bootstrap. Этот cluster-specific алгоритм не обещается одной готовой командой SciPy.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f184"></a>

### F184 — Сводный AP не свидетельствует о классе без GT

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S135](SOURCES.md#s135). **Исходные IDs:** W1-15-F07.

**W1-15-F07: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: COCO code S135.** bbox evaluation имеет отдельные IoU thresholds `.5:.05:.95`, recall grid, area ranges и `maxDets`. Precision/recall для settings без GT обозначаются `-1`, summary усредняет только `s>-1`. Следовательно, среднее может выглядеть приемлемо при неподтверждённом обязательном классе. Нельзя заменять missing support нулём или приписывать отсутствующему классу доказанное качество. COCO matching — detection matching, не event protocol и не SLA.

**Наш вывод:** рядом с AP писать positive objects, independent positive episodes/groups, negatives и проверенную video exposure. При нуле positive episodes recall — N/A; при нуле evaluable exposure FP/hour — N/A. Для редких событий хранить TP/FN/FP и matching/censoring rules; 0 FP на просмотренном отрезке не доказывает нулевую будущую частоту. Пустые/неполные annotations требуют отдельного annotation contract.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f185"></a>

### F185 — Встроенный best и per-class convenience output требуют проверки

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S103](SOURCES.md#s103). **Исходные IDs:** W1-15-F08.

**Уточнение W2 к исходному утверждению:** F272/F273/F274/F277: immutable candidates через on_model_save до strip; AP-best/custom objective раздельны, pre-strip не exact continuation.

**W1-15-F08: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: code S103.** `Metric.fitness` использует веса `[0,0,0,1]` для `[P,R,mAP50,mAP50:95]`. `save_model` пишет best при `best_fitness==fitness`; последний tie может обновить файл. `Metric.maps` сначала заполняет все `nc` общим `self.map`, затем заменяет entries из `ap_class_index` измеренным AP. Поэтому `maps[class_id]` само по себе не доказывает, что класс имел оцениваемый GT. Использовать `ap_class_index` и support counts, а не только эту convenience array. Это конкретное поведение pin; перенос на другой version/task требует проверки.

F152 дополнительно установил EMA validation и stripping итогового checkpoint: inference artifact не равен точной resume point. Здесь не вводится новый default trainer. Если выбранная event цель отличается от detector mAP, нужно заранее сохранить нужные epoch artifacts и проверять их на validation по одному правилу; нельзя после завершения обещать восстановить уже перезаписанный checkpoint.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f186"></a>

### F186 — Порог меняет решение без обучения

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S136](SOURCES.md#s136). **Исходные IDs:** W1-15-F09.

**W1-15-F09: условия/наблюдение** ([ветка](_WORK/W1/15_SELECTION.md)):

**Основание: classification documentation S136.** Для неизменных scores изменение decision threshold меняет labels; ROC/PR curves исходных scores остаются теми же в приведённом примере. Threshold tuning тоже может переобучиться; docs запрещают использовать training data для настройки такого порога.

**Наш перенос с ограничением:** в detection после confidence filtering/NMS/caps состав predictions и даже измеряемый AP могут изменяться, поэтому нельзя обещать инвариантность AP к любому postprocessing. Для событий меняются association, dwell time, cooldown и зона; улучшение итоговых тревог от этих правил полезно, но не является улучшением learned weights. Сравнивать 2 оси по E046.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-01 — W2-01 — Native KD: package provenance, YOLO11 pair и student contract

<a id="f187"></a>

### F187 — Есть опубликованный пакет, но U не является release commit

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** служебная metadata/wheel/bytes проверка выполнена; install/runtime нет.

**S/locator:** [S137](SOURCES.md#s137), [S138](SOURCES.md#s138), [S139](SOURCES.md#s139). **Исходные IDs:** W2-01-F01.

**W2-01-F01: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**META + LOCAL-BYTES; S137, S138, S139.** `__version__=8.4.184` в U было недостаточно. Теперь установлена цепочка annotated tag → R → release → PyPI wheel. U — следующий commit с изменениями docs. Поэтому запись «U есть тег 8.4.184» неверна; корректно: «U code contract для выбранных файлов совпадает с wheel 8.4.184».

- Wheel SHA256: `d04c80f27d335fe27a057dcf00f91c843b11f99d21e7b3017616959a523bfc8a`; computed digest равен PyPI JSON.
- Sdist SHA256 из metadata: `e556832d07f70ba2f73aa8140dceb2a8fb3d5e9a0d9c70827f22a658d292d0ad`; independently computed digest отсутствует, sdist не читался.
- Проверены exact bytes следующих десяти wheel entries относительно raw U: `ultralytics/nn/distill_model.py`, `engine/trainer.py`, `utils/torch_utils.py`, `nn/tasks.py`, `nn/modules/head.py`, `models/yolo/detect/train.py`, `cfg/models/11/yolo11.yaml`, `cfg/models/v8/yolov8.yaml`, `cfg/models/26/yolo26.yaml`, `cfg/default.yaml` (все пути после первого относительно `ultralytics/`). Все equal=True.
- Для ключевого `nn/distill_model.py` SHA256 bytes: `190311d996f9964a9f4302a41f43bd25f3b482516270e148df16f491b9d4fc9b`.

Это воспроизводимый **package artifact**, а не воспроизведённая установка. Metadata допускает Python >=3.8, torch>=1.8.0 с отдельным исключением torch==2.4.0 на Windows; множество зависимостей задаётся диапазонами. Для будущего smoke нужен собственный resolved dependency lock/driver record. Wheel не содержит доказательства, что любая разрешённая комбинация зависимостей успешно выполнит данный route. Архив прочитан в памяти; дополнительных source files на диске не создавали.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f188"></a>

### F188 — Documented support шире примера, runtime status уже

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S078](SOURCES.md#s078), [S080](SOURCES.md#s080), [S140](SOURCES.md#s140). **Исходные IDs:** W2-01-F02.

**W2-01-F02: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**DOC + CODE; S078/S080, S140, S012.** Same-family detect для YOLOv8 и YOLO11 прямо назван в FAQ; это не только наше предположение из `isinstance(Detect)`. Но named recommended pairs и benchmark в guide — YOLO26. Следовательно, YOLO11n←YOLO11s имеет documented family support + code-supported конкретный tensor route, без опубликованного в этом guide YOLO11 pair benchmark и без нашего runtime test.

Constructor проверяет наличие Detect-family head и одинаковое число hooked entries (neck levels плюс head), но не family/task names, class semantics или равенство strides. Успех constructor сам по себе не расширяет documented matrix. Cross-family YOLO11↔YOLO26 оставляем unsupported по docs, даже если какие-то tensor формы могли бы пройти.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f189"></a>

### F189 — Feature/head contract стандартных n/s

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S080](SOURCES.md#s080), [S140](SOURCES.md#s140). **Исходные IDs:** W2-01-F03.

**W2-01-F03: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**CODE + INFERENCE FROM CODE; S080, S140, S012.** Candidate checkpoint interface: unfused standard detect YOLO11n student initialization и отдельно уже обученный/проверенный на требуемом target task YOLO11s teacher `.pt`, с сохранёнными hash/YAML/ontology. Названия `yolo11n.pt`/`yolo11s.pt` описывают архитектуру; наличие готового target-trained teacher пока неизвестно. COCO teacher не объявляется PPE teacher.

| Contract field | Student YOLO11n | Teacher YOLO11s | Область подтверждения |
|---|---|---|---|
| YAML/scales | yolo11.yaml, n: depth .50, width .25, max_channels 1024 | тот же YAML, s: .50/.50/1024 | S140; стандартные YAML, без custom P2/P6/head |
| Detect inputs/head index | `[16,19,22]`, head 23 | `[16,19,22]`, head 23 | get_distill_layers возвращает `[16,19,22,23]` обеим |
| Neck strides | `[8,16,32]` | `[8,16,32]` | YAML geometry; DetectionModel вычисляет stride dummy forward в будущем выполнении |
| Neck channels | `[64,128,256]` | `[128,256,512]` | Выведены scaling в parse_model, не local tensor observation |
| Example grids at square 640 | `80×80,40×40,20×20` | те же | Аналитический пример: 640 кратно 32; всего N=8400 locations, это не batch benchmark |
| Channel adaptation | 3 отдельных Conv1×1→ReLU→Conv1×1 projector | teacher features — targets | Только channels; interpolation/resampling отсутствует |
| Head type | Detect, legacy=False, reg_max16, no dual o2o | то же | C3k2 выставляет legacy=False; YAML не задаёт end2end/reg_max, defaults parse_model дают false-like и 16 |
| Raw score interface | B×nc_student×N | B×nc_teacher×N | forward_head возвращает dict `boxes/scores/feats`; KD использует teacher `scores` |

Teacher и student получают **один и тот же `batch['img']`**, включая уже применённую геометрию/augmentation. На каждый batch hook features сопоставляются по порядку levels. Нужно равенство реальных H/W и layout для каждого level при каждом training shape. В wrapper нет compare stride/H/W и нет автоматического spatial align: flatten+MSE не является проверкой правильной геометрии. Число locations одинакового произведения H×W тоже не доказывает одинаковое пространственное соответствие.

Constructor делает отдельный zero dummy forward размером **2×ch×imgsz×imgsz**, чтобы определить channel dimensions; это дополнительная allocation даже до первого training batch. В штатном trainer imgsz предварительно нормализуется check_imgsz с max_dim=1. Ни факт наличия dummy forward в исходнике, ни наша арифметика не означают, что он помещается в имеющуюся VRAM.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f190"></a>

### F190 — Head scores: усредняются logits, равенство reg_max не проверяется KD

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S080](SOURCES.md#s080). **Исходные IDs:** W2-01-F04.

**W2-01-F04: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**CODE; S080 `loss/decouple_outputs`, S012 `Detect.forward_head/forward`.** В текущем общем Detect `scores` — pre-sigmoid class logits. Teacher eval возвращает `(decoded, raw)`; decouple_outputs берёт raw tuple[1].

- У стандартных YOLO8/11 raw dict не имеет `one2many/one2one` wrappers. Вызовы decouple_outputs для обеих branches возвращают **один и тот же** dict; `(scores+scores)/2` оставляет обычные logits неизменными. Поэтому отсутствие dual head не ломает feature KD route.
- У стандартного YOLO26 raw dict содержит обе branches. Wrapper усредняет **logits** one2many и one2one, затем делит locations по реальным teacher neck H×W, применяет sigmoid и max по class dimension. Это не среднее двух sigmoid probabilities и не веса после NMS/top-k.
- Получается score каждого location формы B×1×N_level. Он взвешивает squared error всех feature channels. Student class logits или box distributions в KD напрямую не сопоставляются; supervised detection criterion остаётся student criterion.
- `reg_max` участвует в устройстве собственной box branch Detect, но wrapper не требует teacher/student equality reg_max и не передаёт localization-distribution targets. Для безопасного candidate обе стандартные YOLO11 имеют reg_max16; YOLO26 имеет reg_max1. Не превращать это в поддержку cross-family: её docs исключают.
- Teacher checkpoint для dual-head route должен сохранять ожидаемые raw branches. Deploy-fused/обрезанный checkpoint, где one2many удалена, не следует автоматически допускать как teacher: wrapper обращается к обеим `scores`. Для конкретной YOLO11 пары сохраняем unfused training artifact; не используем arbitrary exported artifact.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f191"></a>

### F191 — Student получает target nc/names, teacher сохраняет свой task/class contract

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S080](SOURCES.md#s080). **Исходные IDs:** W2-01-F05.

**W2-01-F05: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**CODE; S080 `__init__`, S012 `DetectionTrainer.get_model/set_model_attributes/load_checkpoint`.** Student строится с dataset `nc`/`channels`; target names задаются до `model.load` для class-row remap, затем trainer attaches dataset names/nc/args. Это F016/F10, теперь прослеженное до KD boundary.

Teacher загружается через `load_checkpoint(teacher_path)`: выбирается checkpoint EMA либо model, float/eval; dataset nc/names туда не передаются. Если teacher input channels не совпадают, wrapper **пересоздаёт teacher с ch student, но nc из teacher YAML**, затем `.load(weights)`. Это не target-class adaptation teacher. Такой channel rebuild может изменить/частично перенести входные weights; semantic/quality equivalence нового teacher не установлена. Для выбранного route gate требует одинаковые исходные channels и отсутствующий неожиданный rebuild.

В wrapper нет class-remap teacher→student и нет проверки равенства nc/names. Однако **разное nc само по себе не означает tensor error**: max по teacher class dimension сворачивает её до одного числа на location. Даже permutation teacher class rows оставляет max score тем же при неизменных features/logits. Поэтому W1 «зафиксировать совпадение ontology» следует понимать как conservative teacher-admission/interpretation gate, а не обязательное условие shape equality в loss.

Различаем случаи:

| Teacher/student class relation | Technical trace | Что можно утверждать о знании |
|---|---|---|
| Одна ontology и корректные target-trained teacher weights | Score weights/features технически согласуются при верной геометрии | Разумный основной candidate; качество teacher и student всё ещё измеряются |
| Те же nc, другой порядок имён | Wrapper не переставляет классы; max weighting permutation-invariant | Для этого feature loss порядок не создаёт logit matching error; metadata/inference semantics и supervised student row transfer отдельно проверить |
| Разные nc или subset/superset | Может пройти: teacher class axis сворачивается; student имеет собственный supervised loss | Feature guidance возможно, польза на новых классах неизвестна; это не передача их teacher logits |
| Те же имена, иной смысл или COCO без нужного target class | Никакой semantic error detector в wrapper нет | Load success не доказывает target competence; teacher может придавать вес нерелевантным объектам и смещать features |

Следствие для очереди: не переписывать teacher class count только ради nc equality и не называть случайный новый target head «готовым teacher». Сначала отдельно обучить/получить соответствующий teacher и подтвердить его полезность на development slices. Сохранить реальные source/target class definitions, даже если loss не использует их строки.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f192"></a>

### F192 — Limited support matrix

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-01-F06.

**W2-01-F06: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

| Пара/режим | Documented | Code-observed на U / wheel 8.4.184 | Требует runtime / не установлено |
|---|---|---|---|
| **YOLO11n←YOLO11s detect** standard P3–P5 | Same family/task прямо разрешены; named recommendation для этой пары не дана | `[16,19,22,23]`, 3 grids, channel projectors, single raw-score dict; reg_max16; student-only extraction | Exact chosen checkpoints, old serialization compatibility, gradient/freeze/BN/VRAM/reload/export; target benefit и LinQ |
| YOLOv8n←YOLOv8s detect standard | Same-family support прямо названа | `[15,18,21,22]`, P3/8–P5/32; n→s channels `[64,128,256]→[128,256,512]`; legacy=True cls branch, reg_max16; тот же raw dict contract | Не второй обязательный trial; те же artifact/runtime gates; legacy checkpoint нельзя считать протестированным |
| YOLO26n←YOLO26s detect standard | Named recommended pair, guide example и benchmark | `[16,19,22,23]`, 3 levels; reg_max1; dual head, logits-average weighting | Native example сильнее по docs, но пригодность конкретного graph для LinQ неизвестна |
| YOLO11←YOLO26 / YOLO8←YOLO11 | Cross-family docs исключают | Constructor не проверяет family; отдельные совпадения tensors возможны | Не предлагается как supported route; требует самостоятельного исследовательского port/обоснования |
| Custom P2/P6, чужой head, deploy-only teacher | Не покрыто конкретным candidate contract | Количество levels проверяется, H/W/stride/branch semantics не полностью | Нельзя наследовать поддержку от названия family; отдельная проверка или stop |

Наличие двух code-compatible leads не означает требование обучить обе пары. Если model_stack выберет подтверждённый LinQ student YOLO11n, достаточно first smoke этой пары. Если выбран YOLO8, переносится логика admission и меняются pinned artifacts/indices; не обещается одинаковый результат.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f193"></a>

### F193 — Teacher исчезает до final strip, projectors — при unwrap

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S080](SOURCES.md#s080), [S081](SOURCES.md#s081). **Исходные IDs:** W2-01-F07, W2-11-F07.

**W2-01-F07: условия/наблюдение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):

**CODE; S080/S011.** Существенное уточнение F120: стандартный `save_model` сериализует не полный live teacher, а deepcopy **EMA wrapper**, у которого ModelEMA.__init__ уже выставил `teacher_model=None`. На диске остаются student + projectors + wrapper/hook machinery и путь teacher в train_args. Teacher file нужен для **восстановления training**, а не содержится в обычном сохранённом EMA checkpoint.

| Стадия | Реальный model payload по коду | Teacher dependency / extraction |
|---|---|---|
| Live train | DistillationModel(student, frozen teacher, trainable projectors); teacher eval/no_grad | Teacher занимает память и выполняет forward каждого batch. Compile при KD отключается |
| EMA | Deepcopy wrapper → `teacher_model=None`; student+projectors retained | Отдельный дубликат teacher в EMA убран; это не unwrap student |
| save_model → last/best/epochN | `model=None`, `ema=half EMA wrapper`; epoch/optimizer/scaler/train_args и прочий state | Teacher weights из обычного payload отсутствуют; artifact ещё KD wrapper. Periodic files штатный final_eval не обрабатывает |
| setup_model из interrupted wrapper checkpoint | Новый dataset-driven student из weights.student_model; DistillationModel rebuilt; projector state restored | Teacher берётся из weights.teacher_model, если есть, иначе args.distill_model; нужен тот же сохранённый teacher artifact/path/hash |
| normal final_eval | strip_optimizer(last), strip_optimizer(best), затем final validation best | `_remove_feature_hooks()` → `model=student_model`; projectors вместе с wrapper больше не model graph |
| strip result | Model — student FP16, criterion=None, requires_grad=False; epoch=-1; optimizer/stopper/EMA/updates/scaler None | Стандартный inference artifact; train_args может всё ещё содержать строку distill_model. Само наличие строки не доказывает inference dependency |
| fuse() на wrapper | Удаляет hooks и возвращает student.fuse() | Вызвавший должен использовать **возвращённую** модель; это другой путь извлечения, не resume guarantee |

Прерывание до `final_eval` не получает student-only contract автоматически. Ветка с periodic/immutable checkpoint копией сохраняет возможность resume, тогда как нормальное финальное stripping last/best удаляет optimizer и projector training state вместе с wrapper. Это не exact bitwise continuation: полноценный scheduler/RNG/loader audit принадлежит W2-11. Здесь установлены только дополнительные KD зависимости.

`distill_model` входит в разрешённые check_resume overrides. Можно восстановить доступный путь к **тем же** teacher bytes; подмена teacher по новому path без hash verification меняет эксперимент, даже если загрузка проходит. После normal strip projectors восстановить из student нельзя. Новый supervised/KD run из финального student должен быть обозначен как warm start, а не продолжение старой KD оптимизации.

Final-only graph не подтверждён нашим export. Фраза docs об одинаковой скорости/размере — авторское утверждение о normal student graph; фактические file size, placement и latency должны сравниваться для выбранных artifacts/input/runtime. Метаданные, FP16 serialization и экспортные transformations тоже требуют осмотра.

**W2-11-F07: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**CODE S011/S081 + F193.** strip_optimizer меняет EMA→model, model→FP16, requires_grad=False, criterion=None; epoch=-1; optimizer/best_fitness/stopper/ema/updates/scaler=None, train_args ограничиваются default keys. Final best получает **train_results из last**, поэтому CSV history в best не доказывает его winning epoch. Pre-strip winner epoch/hash ledger нужен заранее.

KD correction: teacher уже **отсутствует в EMA** (`teacher_model=None`) до save; EMA wrapper сохраняет projectors. Final strip снимает hooks и извлекает student, удаляя wrapper/projectors из model graph. Для interrupted KD resume нужны teacher bytes/path/hash и projector state pre-strip. `distill_model` path override допустим; тот же path с другими bytes меняет эксперимент. После strip projectors/optimizer/epoch/EMA count/stopper/scaler из student не восстановить. Online weights/RNG/loader/scheduler не существовали и в штатном pre-strip payload; они не «теряются только при strip».

Путь method→implementation→candidate→benefit: external constrained selection — наш protocol, штатные callbacks/save установлены; candidate contract выше code-supported; конкретного evaluator, целевого выигрышного epoch и выполненного reload нет. Final inference/student contract code-supported W2-01, actual export/LinQ по-прежнему неизвестен.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-02 — W2-02 — Partial labels: loader → assignment → все affected detection losses

<a id="f194"></a>

### F194 — [CODE, S026; уточняет /]. Детекторный TXT loader читает class + четыре box coordinates. `verify_image_label` требует пять columns, class integer и допустимый range.…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S026](SOURCES.md#s026). **Исходные IDs:** W2-02-F01.

**W2-02-F01: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F194 [CODE, S026; уточняет F030/F042].** Детекторный TXT loader читает class + четыре box coordinates. `verify_image_label` требует пять columns, class integer и допустимый range. Нет специального отрицательного class ID для ignore box; обычный `-1` не является поддержанным ignore target. Missing/empty получают одинаковые zero-row arrays при разных scan counters. `result_to_label` сохраняет im_file/shape/cls/bboxes/segments/keypoints/normalized/bbox_format, но не source×class exhaustive/unknown, verified negatives, crowd или ROI coverage. `update_labels_info` превращает geometry в `Instances`; `Format` создаёт cls/bboxes/batch_idx. `collate_fn` может сохранить произвольный дополнительный key как tuple, но **это не consumer coverage**: criterion не читает такие keys автоматически. Следовательно, отсутствие поля в стандартном cache не мешает разработать subclass, но стандартный route не создаёт его и не использует downstream.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f195"></a>

### F195 — [CODE/INFERENCE, S026, S012, S142]. `convert_coco` просто пропускает `iscrowd` annotations, оставляя image pixels; пишет только box/segment/keypoint rows. Не…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S026](SOURCES.md#s026), [S142](SOURCES.md#s142). **Исходные IDs:** W2-02-F02.

**W2-02-F02: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F195 [CODE/INFERENCE, S026, S012, S142].** `convert_coco` просто **пропускает `iscrowd` annotations**, оставляя image pixels; пишет только box/segment/keypoint rows. Не передаёт ignore geometry, per-image verified category lists, `neg_category_ids`/`not_exhaustive_category_ids` или arbitrary ROI. `lvis=True` дополнительно пишет список всех images, включая unannotated, но не превращает TXT в LVIS-aware supervision. `Format.return_mask`, `overlap_mask`, `mask_ratio` относятся к instance segmentation masks, а не к missing-label ignore. `classes`, `single_cls`, `cls_remap` меняют выбор/представление категорий или head transfer, не делают неразмеченный class unknown. Если crowd dropped, его область может стать detector negative по F198. Это конкретный опасный путь conversion, не утверждение, что любой COCO-compatible loader теряет metadata.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f196"></a>

### F196 — [CODE, S025/S141]. `v8DetectionLoss.get_assigned_targets_and_loss` читает только `batch_idx`, `cls`, `bboxes` для GT. Preprocess собирает `[B,max_GT,5]`,…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S025](SOURCES.md#s025), [S141](SOURCES.md#s141). **Исходные IDs:** W2-02-F03.

**W2-02-F03: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F196 [CODE, S025/S141].** `v8DetectionLoss.get_assigned_targets_and_loss` читает только `batch_idx`, `cls`, `bboxes` для GT. Preprocess собирает `[B,max_GT,5]`, coordinates → pixel xyxy. `mask_gt=gt_bboxes.sum(...).gt_(0)` — **valid padding mask**, не unknown-region mask. Assignment получает detached sigmoid class scores `[B,A,C]`, detached decoded boxes, anchor points, gt_labels/boxes и mask_gt. Detached assignment не означает отключение BCE/backprop по logits: `pred_scores` далее остаются исходными differentiable tensors. В этой работе backprop не исполнялся.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f197"></a>

### F197 — [CODE, S141]. TAL рассматривает только перечисленные GT. Candidate pool: anchor centres внутри GT, причём tiny sides расширяются до `stride_val` вокруг центра;…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S025](SOURCES.md#s025), [S141](SOURCES.md#s141). **Исходные IDs:** W2-02-F04.

**W2-02-F04: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F197 [CODE, S141].** TAL рассматривает **только перечисленные GT**. Candidate pool: anchor centres внутри GT, причём tiny sides расширяются до `stride_val` вокруг центра; поэтому проверка лишь точек внутри исходного tiny box недостаточна. Alignment = score соответствующего GT class в степени alpha × overlap в степени beta; criterion задаёт alpha=.5, beta=6. Top-k/valid-GT mask задают candidate positives, multiple-GT conflicts разрешаются через overlap, при topk2 дополнительно ограничиваются. `get_targets` создаёт one-hot class score для назначенного GT и обнуляет все columns у non-foreground; затем alignment normalization даёт soft target scores. Скрытый GT не имеет своей строки и не может получить собственные positive/regression targets. На его области anchor может остаться background **или** быть назначен другому сохранённому GT; геометрический регион сам по себе не гарантирует fg=False. Если GT во всём batch нет, early return явно даёт zero target_scores и false fg_mask. Если пусто только одно image смешанного batch, padding mask не даёт ему positives.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f198"></a>

### F198 — [CODE, S025]. Classification BCE считается на всех `[B,A,C]`, включая non-fg anchors и non-target classes у positive anchors; class_weights broadcast умножает и…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S025](SOURCES.md#s025). **Исходные IDs:** W2-02-F05.

**W2-02-F05: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F198 [CODE, S025].** Classification BCE считается на **всех** `[B,A,C]`, включая non-fg anchors и non-target classes у positive anchors; class_weights broadcast умножает и negative entries. Denominator `target_scores.sum().clamp_(min=1)`; после этого gains и batch-size multiplier. При target=0 непропущенная BCE-компонента соответствует отрицательному обучающему сигналу для class logit; это аналитическое свойство BCE, а не измеренный здесь gradient. У U Detect нет отдельного objectness channel: `no=nc+4*reg_max`, raw outputs boxes/scores/feats. Поэтому фраза «надо исправить objectness YOLO» неверна для этого head, хотя отсутствие отдельного objectness не устраняет false negatives.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f199"></a>

### F199 — [CODE/INFERENCE, S025/S141]. Bbox CIoU и DFL считаются только на fg indices, с весом sum(target_scores at that anchor) и тем же denominator. При `reg_max<=1` вместо…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S025](SOURCES.md#s025), [S141](SOURCES.md#s141). **Исходные IDs:** W2-02-F06.

**W2-02-F06: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F199 [CODE/INFERENCE, S025/S141].** Bbox CIoU и DFL считаются только на fg indices, с весом sum(target_scores at that anchor) и тем же denominator. При `reg_max<=1` вместо DFL используется normalized ltrb L1; имя gain `dfl` не доказывает наличие DFL. У скрытого GT не появляется отрицательная regression loss на фоне: он **теряет собственное regression supervision**. Но удаление GT может изменить конкуренцию за anchors, target_gt_idx, soft scores, regression targets и denominator для сохранённых objects; нельзя гарантировать численную идентичность их вкладов между A/B/C. Простая scalar post-mask общего loss уже не разделяет эти случаи. Если цель — лишь не penalize unknown class в B у objectness-free detect, сохранённый bbox supervision можно оставить; это не требует выдуманного ignore-box regression target.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f200"></a>

### F200 — [CODE, S025/S012]. `DetectionModel.init_criterion` на U выбирает `E2ELoss` по наличию `one2one_cv2`, иначе `v8DetectionLoss`. Active E2ELoss использует one2many TAL…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S025](SOURCES.md#s025). **Исходные IDs:** W2-02-F07.

**W2-02-F07: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F200 [CODE, S025/S012].** `DetectionModel.init_criterion` на U выбирает `E2ELoss` по наличию `one2one_cv2`, иначе `v8DetectionLoss`. Active E2ELoss использует one2many TAL topk=10 и one2one topk=7/topk2=1, один batch для обеих; weighted sum обеих losses, но возвращаемые detached log items относятся **только к one2one**. Initial gains .8/.2, one2many decays до .1; одна исправленная branch не закрывает negative supervision второй. `Detect.forward` делает detached features для one2one при training: её head всё равно обучается своим loss, и one2many продолжает воздействовать на backbone. Legacy `E2EDetectLoss` рядом в файле суммирует topk=10/1 branches, но не является выбранным `DetectionModel.init_criterion` на этом pin. Не выбирать trace по имени существующего класса. YOLO26 YAML задаёт end2end=True/reg_max=1; обычный non-E2E detect 8/11 проходит v8DetectionLoss с DFL при reg_max>1. Семейство/режим конкретного checkpoint всё равно нужно сохранить в E02.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f201"></a>

### F201 — [CODE/INFERENCE, S025, S141, S026, S012]. В проверенном default detect route нет consumers для per-class coverage, crowd/ROI-ignore или `[B,A,C]` loss-validity…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S025](SOURCES.md#s025), [S026](SOURCES.md#s026), [S141](SOURCES.md#s141). **Исходные IDs:** W2-02-F08.

**W2-02-F08: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F201 [CODE/INFERENCE, S025, S141, S026, S012].** В проверенном default detect route нет consumers для per-class coverage, crowd/ROI-ignore или `[B,A,C]` loss-validity mask. `get_assigned_targets_and_loss(..., **assign_kwargs)` — extension point, а не готовый ignore interface: forwarding идёт через TAL в `pair_overlaps`, базовый `pair_overlaps` принимает только indices/gt_bboxes/pd_bboxes; произвольное `ignore` не реализует suppression BCE. Штатные useful outputs этого method — fg_mask/target_gt_idx/target_bboxes/anchor_points/stride_tensor и loss totals; **target_scores, per-entry BCE и pre-conflict masks не возвращаются**, поэтому для полного audit нужны instrumentation/custom criterion/assigner. Пересылка metadata отдельно недостаточна. Это отрицательное наблюдение про конкретно прослеженный chain, не доказательство отсутствия всех сторонних partial-label методов.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f202"></a>

### F202 — [CODE/INFERENCE, S143; architecture boundary]. В legacy YOLOv5 v7.0 `build_targets` сопоставляет только переданные GT с anchor ratios/grid offsets. `tobj` в каждом…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S143](SOURCES.md#s143). **Исходные IDs:** W2-02-F09.

**W2-02-F09: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F202 [CODE/INFERENCE, S143; architecture boundary].** В legacy YOLOv5 v7.0 `build_targets` сопоставляет только переданные GT с anchor ratios/grid offsets. `tobj` в каждом layer сначала нулевой по всей grid, positive positions получают detached IoU. BCEobj вычисляется на **всей grid**. Classification BCE вычисляется только на matched positives (`nc>1`), со smoothing cp/cn; lbox — только matched positives. Поэтому B/C в hidden-only местах штрафуются прежде всего **objectness**, а не dense class BCE; unknown class также может оставаться negative class entry на positives других known classes. Маска c в BCEcls не убирает BCEobj. Нужны пространственная objectness-validity mask `[B,na,H,W]` на каждом level, positive precedence, осознанное reduction/autobalance и при необходимости per-positive class-validity mask. Нет готового такого аргумента в `ComputeLoss(p,targets)`; targets — обычные `[image,class,xywh]`. Для B без геометрии missing class class-agnostic objectness не знает, где подавлять штраф; отключить все background objectness image можно лишь ценой потери всех достоверных negatives. Скрытый объект не регрессируется, пока отсутствует target. Не смешивать legacy `cls_pw` как BCE pos_weight с U class_weights из W1-04.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f203"></a>

### F203 — [INFERENCE из F194, F195, F196, F197, F198, F199, F200, F201, F202]. Минимальные interfaces зависят от loss semantics:

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-02-F12.

**W2-02-F12: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F203 [INFERENCE из F194, F195, F196, F197, F198, F199, F200, F201, F202].** Минимальные interfaces зависят от loss semantics:

| Потребность | Что маскировать/сохранить | Чего это не устанавливает |
|---|---|---|
| B, objectness-free detect | Image×class validity расширить до BCE `[B,A,C]`; известные class positives/negatives сохранить, c unknown исключить; policy denominator явно задать | Нет missing c localization, нет гарантии target benefit; это ещё custom implementation |
| C / class-specific uncertain ROI | Class×anchor validity `[B,A,C]` по преобразованной geometry; **известный positive target имеет приоритет** над generic ignore; известные positive bbox targets не обнулять blanket fg mask | Из knowledge «класс sparse» геометрия hidden object не выводится; prior/pseudo regions могут ошибаться |
| Class-agnostic unknown region | Удалять negative entries в выбранном spatial scope, проверяя конфликт с known objects и valid ROI edges | Грубое удаление всего anchor может отключить правильный person positive из-за unknown helmet внутри person |
| Legacy objectness | Дополнительно level-wise objectness validity и reduction; class mask отдельно | Objectness не class-specific, поэтому class coverage table одна не достаточна |
| Любая композиция sources/augmentations | Маски/coverage должны преобразовываться вместе с images, boxes, ROI и sampler; mosaic требует spatial/source provenance, mixup — явного семантического решения | Один global image×class флаг для composite не сохраняет локальную полноту |

Это **interface requirements, не patch и не готовый алгоритм**. Надо разделять два требования: (1) убрать заведомо неверный negative penalty и (2) научить пропущенный object. Ignore может выполнить первое в ограниченном scope, но не создать bbox regression для второго. Нельзя требовать parity всех assignments A/C без предоставления hidden GT: сравнение assignments должно объяснять изменения, а не считать любое изменение bug.

Проверка удобной class-mask рекомендации дала ограниченно положительный ответ B/U detect и отрицательный ответ её универсальности для C/legacy objectness. «Ни один class mask никогда не поможет C» тоже слишком сильная формулировка: можно консервативно удалить все **negative** c entries и оставить positives, но это другая supervision policy с потерей известных negatives. Её качество неизвестно. Полностью доразметить небольшой subset — конкретная альтернатива, а не claim о всегда лучшем качестве.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f204"></a>

### F204 — [CODE, S144, S145, S146]. Существует более длинная штатная цепочка для известной геометрии class-agnostic ignore, без самостоятельного написания всей criterion:

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146). **Исходные IDs:** W2-02-F10.

**W2-02-F10: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F204 [CODE, S144, S145, S146].** Существует более длинная штатная цепочка для **известной геометрии class-agnostic ignore**, без самостоятельного написания всей criterion:

1. В CocoDataset `ann.ignore=True` **пропускается**, а `iscrowd=True` становится `ignore_flag=1`. Поэтому generic поле `ignore` и crowd не синонимы.
2. `LoadAnnotations` создаёт `gt_ignore_flags` вместе с boxes; `PackDetInputs` разделяет regular `gt_instances` и `ignored_instances`. `unpack_gt_instances` передаёт вторые downstream как batch_gt_instances_ignore.
3. TwoStageDetector передаёт copies data samples в RPN, обнуляя class labels regular GT для class-agnostic RPN. AnchorHead assignment принимает ignored instances. StandardRoIHead отдельно передаёт ignored instances в bbox_assigner.
4. MaxIoUAssigner с **положительным** `ignore_iof_thr` измеряет IoF priors↔ignore boxes; при default `ignore_wrt_candidates=True` denominator связан с candidate area. Он ставит overlap columns кандидатов с IoF выше threshold в -1. При наличии regular GT это оставляет их assignment ignored=-1; RandomSampler выбирает positives `gt_inds>0`, negatives `==0`, игнорируемые не попадают ни туда, ни туда.
5. RPN AnchorHead оставляет label_weights/bbox_weights нулевыми вне выбранных positives/negatives; bbox weights только positive. RoI BBoxHead строит targets по sampled positives/negatives и regresses positives. Поэтому excluded ignored proposals не дают RoI background classification и не добавляют regression.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f205"></a>

### F205 — [CODE/INFERENCE, S144, S145, S146; counterexample]. Найденный route имеет существенные пределы:

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146). **Исходные IDs:** W2-02-F11.

**W2-02-F11: условия/наблюдение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):

**F205 [CODE/INFERENCE, S144, S145, S146; counterexample].** Найденный route имеет существенные пределы:

- Base FasterRCNN config v3.3.0 ставит `ignore_iof_thr=-1` **и RPN, и RCNN**. Одно сохранение crowd metadata не включает suppression. Конкретные configuration interfaces: `model.train_cfg.rpn.assigner.ignore_iof_thr`, `model.train_cfg.rcnn.assigner.ignore_iof_thr`; positive значения выбираются/проверяются для geometry, здесь не назначается универсальное число.
- При `num_gts==0` `assign_wrt_overlaps` ставит **все** `assigned_gt_inds=0`; предварительная запись в нулевую по GT размерность overlaps не защищает ignore candidates. Поэтому только ignored regions без regular GT не удовлетворяют ожидаемому ignore contract на этом pin. Это static counterexample из raw 220–269, не выполненный runtime reproduction.
- Ignore использует bbox geometry, не class labels ignored instances; это **class-agnostic**, не per-category coverage-aware suppression. Может лишить correct overlapping object положительных candidates. Box-crossing geometry не равна pixel mask: IoF cutoff не гарантирует suppression каждого окна, захватывающего hidden object.
- Неизвестные coordinates скрытого второго instance не возникают из `iscrowd`: upstream всё ещё должен знать ignore region. Для узкого сценария C, где регион уже известен, прочитанный route условно готов без нового loss при nonempty regular GT и настройке обоих assigners. Для случайно недостающих boxes B/C вообще он не является найденным решением.

**Решение:** не рекомендовать смену framework только ради слова `ignore`. Этот route полезен как bounded candidate для dataset с достоверными ignore boxes и как тест границ future implementation; зависимости/weights/export/LinQ для команды не проверены. Для empty-GT cases требуется иная проверенная реализация, изменение handling или исключение image. Niitani/FedLoss из W1 остаются methodological contrast: per-RoI/per-category verified-label treatment ≠ generic crowd drop; FedLoss не назначает missing instances.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-03 — W2-03 — One-stage SSOD: UTv2 FCOS и один YOLOv5 route

<a id="f206"></a>

### F206 — Available implementation и неоднородные зависимости

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S148](SOURCES.md#s148). **Исходные IDs:** W2-03-F01.

**W2-03-F01: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**DOC/CODE-READ; S148.** README: Linux/macOS, Python≥3.7, PyTorch≥1.10 с соответствующим torchvision, Detectron2≥0.6, ссылка v0.6. Локальный старый INSTALL: Python3.6/PyTorch1.4/`detectron2-semi` fork без pin. Не воспроизводить смешанное окружение. Кандидат — README/v0.6 boundary плюс новый lock перед smoke. Это не доказанная работа Windows/current torch. README model zoo ещё «Coming soon»: recipe доступен, готовый FCOS detector checkpoint не получен. Tree также содержит standalone `configs/FCOS/R_50_1x.yaml` со ссылкой на отсутствующий `Base-GFocal.yaml`; выбранный ниже route его не использует.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f207"></a>

### F207 — Head/config и расход входов

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S151](SOURCES.md#s151), [S152](SOURCES.md#s152). **Исходные IDs:** W2-03-F02.

**W2-03-F02: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S148/S149/S151/S152.** Выбран `configs/FCOS/coco-standard/fcos_R_50_ut2_sup10_run0.yaml` → `Base-FCOS.yaml`: OneStageDetector→R50/FPN→FCOS; p3–p7, strides8/16/32/64/128; default80 foreground classes. Начальные веса `detectron2://ImageNetPretrained/MSRA/R-50.pkl` — backbone, не готовый target detector. Class map и `MODEL.FCOS.NUM_CLASSES` менять совместно, head/checkpoint transfer проверить отдельно.

L/U global batches8/8, 180000 iterations, burn-up30000, LR.01, AMPtrue, 10% fully labeled COCO images/остальные U, seed1, val каждые2000. `CENTER_SAMPLE=False`, resize short-side range400–1200. Это literals source recipe, не назначение бюджета для команды. Студент получает обе L views; teacher Uweak, student Ustrong: стоимость не равна одному mixed supervised forward. Время/VRAM по числу passes не установлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f208"></a>

### F208 — Общая геометрия позволяет копировать pseudo boxes

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S149](SOURCES.md#s149), [S150](SOURCES.md#s150). **Исходные IDs:** W2-03-F03.

**W2-03-F03: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S150/S149.** `build_detection_semisup_train_loader_two_crops` делит L/U seeded manifest либо cross-dataset streams; отдельные samplers/loaders, aspect ratio grouping. RFS здесь NotImplementedError. Mapper сначала делает общий Detectron2 geometric transform изображения и annotations. Strong строится из **уже преобразованного weak**: ColorJitter/Grayscale/GaussianBlur/три RandomErasing, без новой отдельной geometry; H/W совпадают. Trainer удаляет U `instances`, присваивает одни pseudo Instances обоим views. Матрица teacher→student здесь не нужна именно благодаря общей geometry. Добавление student-only crop/mosaic нарушит contract.

COCO U annotations могли присутствовать при mapper/split, но `teacher_weak` их не использует, перед student они удаляются. Это не разрешение передавать target validation в U. Custom registration и filtering пустых кадров проверять в resolved config.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f209"></a>

### F209 — Разные pseudo sets и разные confidence definitions

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S149](SOURCES.md#s149), [S151](SOURCES.md#s151). **Исходные IDs:** W2-03-F04.

**W2-03-F04: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S149/S151.** No-grad teacher даёт dense outputs. Classification NMS criterion `cls`: sigmoid class score, cutoff.5. Regression второй NMS по тем же outputs `cls_n_loc`: class score×mean четырёх `1-sigmoid(reg_pred_std)`, затем sqrt и cutoff.5. Два cutoff.5 относятся к разным scores. Centerness отдельно; обычный test `cls_n_ctr` использует sqrt(class×centerness). Не сводить три режима к одному «teacher confidence».

При `REG_DISCRETE=True`: regression4×(16+1) channels, softmax+Integral; `bbox_pred_std`4 channels, centerness1 channel. Uncertainty обучается supervised NLLoss: sigma=sigmoid(std), regression error/log variance и IoU weighting, вес.05. Это не jitter SoftTeacher. `instances_class` задаёт cls/ctr, `instances_reg` — loc supervision.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f210"></a>

### F210 — Boundary selection не решает все missing positives

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S151](SOURCES.md#s151). **Исходные IDs:** W2-03-F05.

**W2-03-F05: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S151.** Assignment: l/t/r/b grid locations, inside-box/size-of-interest по FPN; минимальная площадь при нескольких boxes; center sampling выключен. Regression selection **по каждой стороне**: teacher confidence>.8 и >student confidence+.1. По выбранным entries `smooth_l1_loss(beta=0)`; если select пуст, явный CUDA zero. Псевдорегрессия включена, в отличие от UTv1 F110.

Trainer: supervised cls/ctr делится на3, pseudo cls/ctr×2/3; supervised loc делится на1.2, pseudo loc×.2/1.2. Это не один общий unsup coefficient для всех terms.

Pseudo classification target нулевой по всем locations/classes с единицами на assigned positives; sigmoid focal суммирует остальные negatives. Пропущенный teacher объект не получает автоматически ignore. При empty bbox set assignment all-background; pseudo cls path не фильтрует `keep_locations`, в отличие от supervised path. Assertion в trainer `len(unlabel_data)!=0` проверяет **dictionary, не число boxes**, вопреки тексту сообщения. Empty-positive fallbacks есть; finite/gradient correctness all-empty batch не выполнена. SSOD не считать общим SAOD/partial-label fix (F027).

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f211"></a>

### F211 — Teacher/student и extraction

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S149](SOURCES.md#s149), [S152](SOURCES.md#s152). **Исходные IDs:** W2-03-F06.

**W2-03-F06: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S149/S152.** Teacher отдельный, сразу `.eval()`; комментарий train step о не-переключении режима не отменяет initialization. На burn-up keep_rate0, затем EMA.9999 каждый iteration по **state_dict**, включая buffers, до teacher forward данного шага. Backprop/optimizer student, teacher no-grad. Wrapper имеет namespaces `modelTeacher`/`modelStudent`, checkpointer сохраняет его с optimizer/scheduler.

Hooks оценивают обе ветви: student metric suffix `_student`, teacher без suffix. `train_net.py --eval-only` в ubteacher route явно оценивает **modelTeacher**. Нельзя выбрать по teacher AP, экспортировать student и присвоить ему AP. Выбор best по нашей critical metric в route не установлен: нужны iteration/config и обе оценки. Структура позволяет извлечь отдельную submodule/state_dict; ready exporter в tree не найден. Ни extraction, ни reload здесь не выполнены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f212"></a>

### F212 — Uncertainty остаётся Python eval branch

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S151](SOURCES.md#s151), [S152](SOURCES.md#s152). **Исходные IDs:** W2-03-F07.

**W2-03-F07: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ + INFERENCE; S151/S152.** `FCOSHead.forward` без условия training вызывает bbox_pred_std при KL_LOSStrue; FCOS eval передаёт std в predict_proposals, который сохраняет `boxlist.reg_pred_std`. OneStageDetector postprocess возвращает Instances. Утверждение «training-only branch автоматически удалена» неверно на этом SHA.

При `cls_n_ctr` std не входит в boxes/scores/NMS. Наш вывод: detection-only export wrapper мог бы удалить unused computation либо отдельный inference build с KL disabled мог бы загрузить совпадающие веса без std keys. **Ни один вариант не реализован/не измерен**. Strict load, auxiliary fields, normalization/resize, Integral/postprocess/NMS и равенство outputs проверить. Это изменённый FCOS inference build, не гарантия загрузки в произвольный standard FCOS/YOLO.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f213"></a>

### F213 — Почему выбран этот lead и где family claim заканчивается

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S153](SOURCES.md#s153), [S154](SOURCES.md#s154), [S155](SOURCES.md#s155). **Исходные IDs:** W2-03-F08.

**W2-03-F08: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**DOC/CODE-READ; S153, S154, S155.** Авторская arXiv entry ссылается на AlibabaResearch repo; название прямо YOLOv5. README заявляет YOLOv5/YOLOX/v6/v7/v8 library, conversion из YOLOv5 v6.0+, custom YOLOv5 configs, ONNX/back-conversion scripts. Их binaries/conversion parity не проверены. В active `SSODTrainer.train_instance` teacher path реализован при `model_type in ['yolov5']`; остальные здесь `NotImplementedError`. Выбран конкретный **P5 anchor-based YOLOv5l**, depth/width1/1, три anchor sets, Head YoloV5. Наличие YoloV8Detect в builder не доказывает полный online SSOD support этой головы.

README описывает проверенный авторами Modelscope container Ubuntu20.04/CUDA11.3/Python3.7/torch1.11; requirements разрешает torch≥1.9/torchvision≥.8.1, это не lock. Это candidate environment, не runnable stack команды. Современный Ultralytics package не dependency interface данного trainer. Lead полезен потому, что позволяет проверить существующий YOLOv5 recipe вместо самостоятельного переноса FCOS uncertainty/assignment.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f214"></a>

### F214 — Config routes и полнота labels

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S154](SOURCES.md#s154), [S155](SOURCES.md#s155). **Исходные IDs:** W2-03-F09.

**W2-03-F09: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S154/S155.** Custom config: train/val/test/target image lists, nc/names, input640; BGR→RGB CHW, `/255`; ComputeLoss для L, ComputeStudentMatchLoss для U. Custom YAML имеет20 epochs/burn10, COCO10% YAML300/burn0, README общая инструкция говорит про burn220. Эти literals нельзя соединять в один recipe. Здесь выбран custom route с явным warm-start/burn contract; sample hyperparameters не назначаются для СИЗ.

Custom `ssod_hyp.with_gt=False` создаёт fake labels U; COCO config True для GT diagnostics. `FairPseudoLabel.create_pseudo_label_online_with_gt` строит targets из teacher predictions/NMS, GT использует только в debug plots; trainer при target_with_gt также считает diagnostic matching. Для реального U False, независимый audit не передавать loss. L проходит обычный supervised loss, значит нужны полностью проверенные labels по task ontology. Partial L не становится безопасным автоматически. Скрытые U positives ниже threshold также могут стать objectness negatives.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f215"></a>

### F215 — Geometry требует metadata interface

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S155](SOURCES.md#s155). **Исходные IDs:** W2-03-F10.

**W2-03-F10: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S155.** LoadImagesAndFakeLabels возвращает `(strong, labels, path, shapes, original_weak, M_s)`; teacher использует weak, student strong. Weak может быть mosaic canvas; strong — recorded perspective/scale/translation, HSV/flips и conditional cutout/autoaugment. M_s хранит image index, 3×3 matrix, scale, flip flags. FairPseudoLabel делает NMS, xywh→xyxy, transform четырёх углов M, clipping/box_candidates filtering, normalization и отдельные flips. У online_label_transform perspective default0: matrix fidelity должна соответствовать chosen augmentation settings.

Некоторые cutout/autoaugment выполняются только если `len(labels)>0`; при fake-empty U это может быть no-op. Реальные transforms проверять с **with_gt=False**, а не только в COCO diagnostic режиме. Штатный loader не является доказанным semantics-preserving augmentation для wearing/association задач.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f216"></a>

### F216 — Soft objectness и граница missing-positive treatment

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S154](SOURCES.md#s154), [S156](SOURCES.md#s156). **Исходные IDs:** W2-03-F11.

**W2-03-F11: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S154/S156.** Effective default `pseudo_label_type='FairPseudoLabel'`: custom/10% YAML его не меняют. Dynamic GMM thresholds из LabelMatch нельзя приписать этому route. NMS conf.1/IoU.65, low/high.1/.6. select_targets делит по final confidence: high reliable, intermediate uncertain. При pseudo_label_with_obj uncertain target использует teacher objectness, а не final class product. Optional uncertain regression допускается при objectness≥.99; optional uncertain cls при class confidence≥.99. Custom включает uncertain bbox и выключает uncertain cls.

YOLOAnchorAssigner использует anchor-size ratio cutoff anchor_t и соседние grid offsets; это не FCOS assignment и не современный task-aligned assigner. Reliable: IoU box loss, class BCE на matched anchors, objectness target=detached IoU. Все tobj сначала **нули**. На uncertain matched anchors `ignore_obj=True` поставил бы -1 и исключил BCE; config здесь **False**, значит soft teacher score и BCE. Остальные anchors/не найденные teacher объекты остаются negatives. Название ignore thresholds не означает spatial-ignore всей неопределённой области.

Whole batch без proposals даёт invalid_target_shapeTrue, trainer ставит unsup loss0. Кадр без proposals внутри непустого batch требует проверки objectness negatives. Корректность чисел/градиентов не выполнена; никакого гарантированного решения всех missing boxes здесь нет.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f217"></a>

### F217 — Два уровня EMA и разные роли checkpoints

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S155](SOURCES.md#s155), [S158](SOURCES.md#s158). **Исходные IDs:** W2-03-F12.

**W2-03-F12: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S155/S158.** `self.model` — оптимизируемый student; `self.ema=ModelEMA(student)` создаёт pseudo labels. После optimizer step обновляется EMA, затем secondary `self.semi_ema` обновляется **от self.ema.ema**. Первая EMA имеет ramp decay, secondary — cosine от.999 к.9999 либо fixed. После burn-in trainer оценивает raw student, затем secondary semi_ema. Второй результат заменяет self.results, определяет fitness/best. Checkpoint model=raw student, ema=secondary после burn, плюс optimizer/epoch/updates; updates относится к первой EMA. Полное возобновление обоих EMA/adaptor состояний этим набором не доказано.

Финальный strip_optimizer заменяет model на ema, зануляет optimizer/ema/updates, epoch=-1. Export loader также предпочитает ema. Default final/export — secondary smoothed detector, **не raw student и не online pseudo teacher**. Нужны branch manifest и validation/export parity именно выбранной ветви. Raw student отдельно сохранить до stripping. Epoch-adaptor меняет число batches на длину U loader; equal epochs не equal L exposure/updates/compute.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f218"></a>

### F218 — Domain heads сохраняются даже при нулевом loss

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S155](SOURCES.md#s155), [S157](SOURCES.md#s157), [S158](SOURCES.md#s158). **Исходные IDs:** W2-03-F13.

**W2-03-F13: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S155/S157/S158.** yolo_ssod.Model всегда создаёт det_8/det_16/det_32; _forward_once вычисляет их и возвращает detector_out + domain features. При with_da_lossFalse trainer умножает domain losses на0, но модули/forward остаются. Поэтому actual inference object не буквально standard YOLOv5 без extraction.

Найден concrete extraction path: `export.py --da` заменяет forward на forward_export, удаляет три det_*; forward_export выполняет backbone→neck→head. Это прочитанный path, **не успешный export**. Без --da могут остаться дополнительные outputs/operators. Флаг нужен по actual class graph, даже если domain loss был выключен.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f219"></a>

### F219 — Export head возвращает raw levels до decode

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S157](SOURCES.md#s157). **Исходные IDs:** W2-03-F14.

**W2-03-F14: условия/наблюдение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):

**CODE-READ; S157.** Export loader предпочитает EMA, fuse/eval, ставит Detect exportTrue. В yolov5_head.py этот режим возвращает list raw per-level tensors `B×anchors×(H*W)×(nc+5)` при np0, **до sigmoid/grid/anchor decode**. Обычный eval возвращает decoded concat + raw levels, существуют post_process methods. Нельзя объявить output standard decoded xywh/objectness/classes только по имени YOLOv5.

deploy.model_convert.export_onnx задаёт один output name и generic dynamic axes, хотя head отдаёт несколько levels; это место future shape/name проверки, не доказанный баг выполнения. Run API default opset12, CLI default9: сохранять resolved invocation. Decode/NMS/class map и actual output schema требуют parity gate. ONNX не является LinQ proof. Back-conversion scripts из README не audited.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-04 — W2-04 — Acquisition interface и минимальный отбор на доразметку

<a id="f220"></a>

### F220 — Detect Results не содержит полного вектора классов

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S159](SOURCES.md#s159), [S160](SOURCES.md#s160). **Исходные IDs:** W2-04-F01.

**W2-04-F01: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: наблюдение кода S159/S160.** `construct_result` масштабирует координаты к исходному изображению и создаёт `Results(..., boxes=pred[:, :6])`. Для обычного detect строка имеет `x1,y1,x2,y2,conf,cls`; `Boxes` разрешает 6 или 7 колонок, седьмая связана с tracking ID. `conf` и `cls` — последние две колонки, `xyxy` — первые четыре. У detect конструктор не получает `probs`, поэтому `result.probs` здесь `None`. Классификационный `Probs` не восстанавливает отброшенные detection scores. `boxes.data` иногда называется raw в docs, но это **raw storage данного Results после postprocessing**, не raw head logits. Нет отдельного background/objectness channel, ROI proposals, complete class vectors или всех locations в этом объекте. F129 про token scores GroundingDINO имеет иной interface и не меняет этот факт.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f221"></a>

### F221 — Полные векторы существуют раньше Results, но это другой контракт

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S161](SOURCES.md#s161), [S167](SOURCES.md#s167). **Исходные IDs:** W2-04-F02.

**W2-04-F02: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: код S161/S167.** У `Detect.forward_head` отдельные `boxes`, `scores`, `feats`; `scores` ещё logits. `_inference` применяет sigmoid и соединяет decoded boxes с `nc` scores. При one-to-many decoded output имеет `(B,4+nc,A)`; это не `(B,5+nc,A)`: отдельного objectness или background logit нет. Native non-export forward возвращает `(decoded_predictions, raw_dict)`; export возвращает только выбранный output. У dual head raw dictionary может включать `one2many`/`one2one`, у обычного — непосредственно `boxes/scores/feats`. End-to-end выбранная ветка проходит top-k до выхода decoded prediction. Векторы нельзя извлечь обратно из final `conf/cls`.

**Вывод:** categorical `-sum p log p` для normalized softmax classes здесь не возникает автоматически. Можно отдельно определить Bernoulli uncertainty для независимых sigmoid entries или нормировку по классам, но это разные новые score hypotheses, не вероятность неправильного box. Минимальный route ниже ничего такого не требует.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f222"></a>

### F222 — NMS path уже удаляет кандидаты до выдачи scalar scores

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S162](SOURCES.md#s162). **Исходные IDs:** W2-04-F03.

**W2-04-F03: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: код S162.** `non_max_suppression` берёт первый элемент native tuple, фильтрует locations по `amax(class_scores)>conf_thres`, переводит `xywh→xyxy`, при стандартном `multi_label=False` оставляет лучший класс. Далее class filter, ограничение `max_nms`, class-aware либо agnostic IoU suppression и `max_det`. DetectionPredictor не включает `multi_label=True`. Поэтому снижение `conf` не отключает NMS и не возвращает complete vectors; `iou` не восстанавливает отброшенные class scores. Class filtering применяется к уже выбранному argmax: запрос определённого класса не равен поиску всех locations, где score этого класса превысил floor. `max_nms`/time limit тоже могут ограничивать результат. Финальные boxes описывают retained predictions, а не все возможные гипотезы.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f223"></a>

### F223 — NMS-free в U означает one-to-one top-k, а не полную плотную сетку

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S163](SOURCES.md#s163), [S165](SOURCES.md#s165), [S166](SOURCES.md#s166). **Исходные IDs:** W2-04-F04.

**W2-04-F04: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: docs S166 + код S163/S012/S165; связано с F221/F222.** В проверенном U YOLO26 prediction/validation по умолчанию использует one-to-many+NMS. `nms=False` задаёт native backend `end2end=True` до fusion. Гайд различает экспорт: `nms=None` — raw one-to-many, `True` — embedded NMS, `False` — one-to-one processed output. Нельзя переносить значение флага predict на exported graph: граф уже определяет выходы.

После head top-k e2e branch NMS-функции делает только confidence/class filtering и cap, без IoU suppression. `iou` там не превращается в подавление overlapping boxes. При class-aware top-k возможны разные class entries одного location; это также не complete vector. Индексы e2e filtering относятся к уже сокращённому input, не автоматически к исходным anchors. У YOLO8/11 YAML нет one-to-one; setter предупреждает и оставляет one-to-many. Называние family недостаточно: проверять actual graph/head и аргументы. Fusion может удалить неиспользуемую ветку; для сравнения режимов нужен исходный artifact и корректное пересоздание backend, не смена private flag fused object.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f224"></a>

### F224 — Embeddings публично доступны, однако не добавляются к обычным Results

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S012](SOURCES.md#s012), [S164](SOURCES.md#s164), [S166](SOURCES.md#s166). **Исходные IDs:** W2-04-F05.

**W2-04-F05: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: код S164/S012 и подтверждающие live docs S166.** Native Ultralytics PyTorch `model.embed(source)` проверяет тип модели; default — second-to-last layer. В `_predict_once` указанные feature maps проходят adaptive average pool до image vectors, concatenate и early return при последнем выбранном layer. Predictor при `args.embed` выдаёт tensors и пропускает обычный detection postprocess. Для стандартного «Results плюс embedding» нужны отдельный проход или custom совместное извлечение. Выход зависит от layer ID/channels и preprocessing; это не person/ROI embedding или готовая мера полезности кадров. Public wrapper не поддерживает этот interface для exported formats/чужих модулей. У выбранного checkpoint совместимость ещё не проверена.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f225"></a>

### F225 — Object features и raw tensors требуют отдельной инженерной границы

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S159](SOURCES.md#s159), [S164](SOURCES.md#s164), [S165](SOURCES.md#s165). **Исходные IDs:** W2-04-F06.

**W2-04-F06: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**Тип: код S159/S164/S165, наш вывод.** `DetectionPredictor` умеет добавить `r.feats`, если заранее установлен private `_feats`, используя сохранённые indices. Это условная внутренняя ветка, не стандартное поле каждого detection Results. Обычный public `predict` не обещает ROI vectors. Для one-to-many native output custom predictor может перехватить вход `postprocess` до NMS; API принимает custom `predictor` class. Доступ к raw dict, decoding и сохранение индексов — ответственность такой реализации. Для one-to-one pre-top-k vectors нужны native raw head tensors/decoding либо hook до top-k. Не следует использовать training mode ради logits: он меняет поведение модели. Export с already processed output не отдаёт потерянные векторы без нового graph/export. Это адресная потребность model_stack, а не выполненная интеграция.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f226"></a>

### F226 — наша предложенная спецификация, не найденный готовый selector и не проверенный выигрыш. Выбран route `retained-low-confidence + metadata exploration`, использующий…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-04-F07.

**W2-04-F07: условия/наблюдение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):

**F226 — наша предложенная спецификация, не найденный готовый selector и не проверенный выигрыш.** Выбран route `retained-low-confidence + metadata exploration`, использующий только F220. Он конкретизирует arm C существующего E022, а не создаёт обязательный новый AL algorithm.

1. **Вход:** разрешённый train acquisition pool, отделённый от dev/lockbox; hashes кадров, camera/session/group IDs, timestamps, source FPS/timebase и заранее определённая единица временного исключения. Checkpoint hash, package U либо вновь прочитанный pin, canonical class map и режим head закреплены. Не строить embedding/selector на lockbox.
2. **Стандартный API:** обычный detect `model.predict(..., stream=True)` с `embed=None`, `augment=False`, заранее выбранными `imgsz/rect`, precision/device/batch, `conf=c_pool`, `iou`, `max_det`, `agnostic_nms`, `nms`. Не выдавать `c_pool` за event operating threshold. Он фиксирует видимую selector выборку; неизвестные значения выбираются в train-only correctness pilot, не по lockbox. Минимально использовать `classes=None`, чтобы class filter дополнительно не скрывал hypotheses; scope labels контролировать отдельно. Для чистоты сравнения все arms используют одинаковую preannotation policy.
3. **Сохраняемый public output:** row per frame, даже если boxes пусты; `frame_id/group_id/time/orig_shape`, все retained `xyxy,conf,cls`, count, model/config hashes и status. Сохранять числа без округления до display confidence. Пустой список, decode/inference error и пропуск frame — разные состояния. `Results.path` для кадров из видео недостаточен как уникальный frame ID. Полные Results с orig_img в памяти не обязательны: переносить компактные записи на CPU и отделять images по manifest.
4. **Явный score:** для непустого кадра `u(frame)=max_b(1-conf_b)=1-min_b(conf_b)`, сортировка по убыванию, ties — закреплённый seed/frame key. Это low-confidence heuristic по retained boxes, **не entropy**. Для пустого кадра `u` отсутствует (`null`), а не искусственные 0/1. Количество boxes и predicted class записываются для анализа density/class bias. Более плотный кадр имеет больше шансов получить один low score; выбранная формула этого не исправляет и требует cost audit.
5. **Очередь:** заранее разделить budget на ranked часть и seeded exploration по camera/session/scene strata. Exploration имеет доступ ко всему пулу, включая high-confidence и no-box кадры; дополнительно обеспечить заранее описанное покрытие no-box stratum, когда он есть. Недостаток empty frames в stratum отмечать, не синтезировать. Доли/квоты — параметры будущего опыта, универсальных процентов нет. Общий temporal cap действует между rank/random/targeted частями и между rounds; dedup не должен слить разные фазы обязательного event.
6. **Human output:** выбранный image/clip размечается полностью для in-scope taxonomy с unknown/ignore по guidelines. Проверять области вне proposals, иначе уверенные пропуски станут background. Score не выбирает только один box для исправления. Причина отбора, минуты просмотра/разметки/QA и итоговая coverage сохраняются; неполная разметка требует отдельно подтверждённого partial-label loader/loss.

Низкий `c_pool` увеличивает число слабых hypotheses и стоимость NMS/сериализации; нет основания ставить его в ноль ради «всех ошибок». `N==max_det` отмечать как **возможную** цензуру, не доказанное число потерянных boxes. E2e top-k может скрыть слабый/редкий класс ещё до `conf` и class filter. Одна фиксированная настройка между rounds делает сравнение интерпретируемым; изменение head/cutoff/preprocessing считается изменением selector bundle.

Общие confident errors и объекты, которых нет в taxonomy, остаются невидимыми ranking. Поэтому metadata exploration — обязательная часть этого предложенного контракта; disagreement тоже не гарантирует их обнаружение. Нет labels → нельзя сообщать, какой arm лучше, по одной привлекательности error gallery.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-05 — W2-05 — Teacher admission: localization, retained coverage и малый audit

<a id="f227"></a>

### F227 — Detection calibration относится к выбранному TP criterion, не восстанавливает recall

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S169](SOURCES.md#s169). **Исходные IDs:** W2-05-F01.

**W2-05-F01: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Paper-read, S169 §3.1.** Target calibration — совпадение confidence с precision условно по классу и свойствам predicted box. Correctness включает class match и заданный IoU. Авторы явно указывают: GT без detection не имеют confidence, поэтому black-box recall calibration невозможна. **Наш вывод:** score calibration не создаёт отсутствующие boxes; completeness требует полного независимого GT. Это сильнее общего F114 «confidence не вероятность».

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f228"></a>

### F228 — Малый глобальный calibration error не устанавливает качество сложной страты

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S169](SOURCES.md#s169). **Исходные IDs:** W2-05-F02.

**W2-05-F02: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Paper-read, S169 §4/5.1.** D-ECE учитывает box properties; его значения при разных bins/dimensions напрямую несопоставимы, дробление уменьшает поддержку bins. Calibration/test разделены по изображениям COCO, не по CCTV sessions. Fig.3 — иллюстрация скрытой location miscalibration, не полевой safety benchmark. **Наш вывод:** один global ECE не заменяет per-class/size/location support и retained coverage; detector-specific calibration по этому paper не является нашей проверкой камер. Численный gain из таблиц здесь не используется.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f229"></a>

### F229 — Доступная реализация принимает уже вычисленный matched, а не ищет пропуски

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S170](SOURCES.md#s170). **Исходные IDs:** W2-05-F03.

**W2-05-F03: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Code/docs-read, S170.** README detection example передаёт `matched` — binary correct-class/IoU match per prediction; `LogisticCalibration(detection=True)` принимает confidence + relative box feature, затем `fit`/`transform`; `ECE(..., detection=True)` измеряет D-ECE. В `_prepare_input` detection `y` должен быть binary и используется как `matched`; shape проверяет одинаковое число X/y. Matching policy должен предоставить вызывающий код. В ECE `sample_threshold` исключает малонаполненные bins из metric; `return_num_samples` позволяет показать поддержку. **Наш вывод:** исключённые bins нельзя считать успешно проверенными, а отсутствие строк для FN не означает отсутствие FN. Для нашего audit нужны собственные frozen matching и полные GT counts; default bin count/threshold не назначаются target-настройкой.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f230"></a>

### F230 — High cutoff действительно может отвергнуть много true positives и не исправить localization

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S171](SOURCES.md#s171). **Исходные IDs:** W2-05-F04.

**W2-05-F04: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Опубликованное наблюдение/объяснение авторов, S171 §3.2–3.3/Fig.3.** Для анализа Fig.3 взяты случайные 10k unlabeled training images COCO train2017, модель обучена на 10% labeled images, используемый default detector работы — Faster R-CNN R50-FPN. Высокий foreground threshold даёт высокую precision и низкий retained recall; authors показывают слабую связь foreground score с IoU и вводят отдельный box-jitter regression filter. Это диагностический анализ teacher candidates, не independent CCTV benchmark и не универсальный cutoff. Точный checkpoint-selection для фигуры не установлен. **Наш вывод:** plain folder pseudo-labeling с высоким cutoff не воспроизводит Soft Teacher: отвергнутые positives могут стать background без соответствующего loss treatment. Числа precision/recall рисунка намеренно не превращены в наши expected rates.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f231"></a>

### F231 — Состав detector score и assignment влияют на то, что отбирается

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S172](SOURCES.md#s172). **Исходные IDs:** W2-05-F05.

**W2-05-F05: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Paper-read, S172 §3.2–3.3.** UTv2 на FCOS разбирает centerness×classification score: высокий product может быть обусловлен ненадёжной centerness при ограниченных labels. Confidence threshold также не определяет надёжность каждой из четырёх regression boundaries; noisy box сдвигает assignment. Listen2Student вводит дополнительную uncertainty branch и сравнение teacher/student. **Наш вывод:** score semantics надо читать у выбранного teacher, а не переносить численный cutoff с Faster R-CNN на FCOS/YOLO/VLM. Новый head/calibrator не требуется для fully reviewed assistance. Здесь не предлагается портировать UTv2: evidence ограничивает универсальный scalar gate, numeric table gains не используются.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f232"></a>

### F232 — Oversampling требует сохранять вероятности отбора

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S173](SOURCES.md#s173). **Исходные IDs:** W2-05-F06.

**W2-05-F06: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Первичная статистическая документация, S173.** Неравные вероятности отбора и deliberate oversampling меняют состав sample; population estimate требует sampling weights, design metadata и определённой population. **Наш проект применения:** отделить probability component от purposive diagnostics и применять явные веса только к известному probability design. У targeted находок с неизвестной inclusion probability нет корректного population weight, восстановимого одним делением на число boxes. См. E024.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f233"></a>

### F233 — Больше boxes одной сцены не означает больше независимой поддержки

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S174](SOURCES.md#s174). **Исходные IDs:** W2-05-F07.

**W2-05-F07: условия/наблюдение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):

**Первичная статистическая документация, S174.** Внутрикластерная корреляция и differential weighting влияют на variance; simple-random/iid расчёт может занижать standard errors. **Наш вывод для teacher admission:** количество independent camera/session/episode groups надо показывать рядом с instance counts; bootstrap всех boxes без group design не обоснован. Выбор уровня resampling зависит от claim, см. E024. Документ не даёт универсальной нижней границы количества CCTV scenes.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-06 — W2-06 — Detection-specific initialization: переносимые модули и честное downstream сравнение

<a id="f234"></a>

### F234 — Публикации действительно различают downstream initialization [AUTHOR-MEASUREMENT]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S175](SOURCES.md#s175), [S178](SOURCES.md#s178). **Исходные IDs:** W2-06-F01.

**W2-06-F01: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

Числа — авторские box AP / novel box AP, не наш тест и не event recall. В таблице намеренно оставлен узкий набор строк. Источники: S175 Tables 3/11 и S178 Tables 1/3/4/5.

| Сопоставление | Downstream и label budget/split | Результат и существенный контроль |
|---|---|---|
| DetCo / supervised ImageNet | Mask R-CNN R50-FPN, весь COCO train2017 → val2017, 90k updates | 40.1 / 38.9 AP; backbone pretrain 200 epochs; это representation transfer |
| DETReg / SwAV / supervised backbone | Deformable DETR R50, весь COCO train2017 → val2017, 50 epochs | 45.5 / 45.2 / 44.5 AP; IN1K pretraining |
| DETReg / supervised DDETR; с supervised base этапом | COCO 60 base classes, затем 10/30 instances на каждый из 80 классов; оценка 20 novel | 13.7/22.6 против 12.4/20.4 nAP |
| Те же, без base этапа | Те же единицы 10/30-shot; COCO novel evaluation | 9.1/16.5 против 6.7/12.5 nAP; full FT |
| In-domain DETReg / SwAV | DDETR, 1% labels COCO train2017 → val2017 | 14.58±0.3 / 11.79±0.3 AP; DETReg дополнительно видел весь train2017 без labels; 5 seeds |

У DetCo Table11 добавление intermediate supervision уменьшило linear classification Top1 64.3→63.2 при росте VOC detection AP 56.3→57.0. Classification ranking не выбирает detection initialization. DETReg low-data §4.2 обучает до 2000 epochs/прекращения роста validation; §4.4 — до convergence. Полная идентичность downstream recipe/selection разных работ не установлена.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f235"></a>

### F235 — DetCo: доступен transfer route, но это не whole-detector checkpoint [CODE/DOC; S176/S177]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S176](SOURCES.md#s176), [S177](SOURCES.md#s177). **Исходные IDs:** W2-06-F02.

**W2-06-F02: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

Авторский README даёт DetCo-200ep/200ep-AA links, downstream scripts и одновременно оставляет собственно `Pretext Task Pretrain` в состоянии `Coming Soon`. Поэтому публично обнаружены веса/маршрут переноса; complete reproducible pretrain trainer этим repo не установлен. Упоминание OpenSelfSup не восполняет отсутствующий конкретный implementation автоматически. README ограничивает применение академическим использованием и направляет коммерческое использование к авторам; разрешение на кейс/последующее использование надо выяснить до принятия этого artifact.

Converter читает `obj['state_dict']`, переименовывает stem/layer/bn/downsample в Detectron2 representation и пишет pickle с `matching_heuristics=True`. Он не реализует class map и не создаёт trained detector predictor. В нём нет общего фильтра, который надёжно вырежет произвольный MLP/teacher checkpoint: нужны **реальные keys полученного файла** и load report. Совместимость backbone не доказывает наличие neck/RPN/RoI knowledge. Detection-specific здесь означает цель representation learning, а не supervised knowledge о нужных PPE classes.

Сохранённые FPN configs особенно полезны как попытка опровергнуть «чистую замену весов». Supervised config ссылается на MSRA `R-50.pkl`; SSL override одновременно задаёт RGB, mean/std и `STRIDE_IN_1X1=False`. Эти различия могут быть необходимыми условиями корректного применения pretrained backbone, но они означают сравнение согласованных initialization packages. Нельзя без аудита назвать его эффектом только чисел в weight tensors. У обоих наследуется batch16, LR0.02, min-size 640…800, 90k steps с decay 60k/80k; есть SyncBN backbone/FPN и PreciseBN. Эти параметры исторического Detectron2 recipe не перенесены в Ultralytics CLI.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f236"></a>

### F236 — DETReg: код объясняет, что сохраняется кроме backbone [CODE; S180/S181/S182]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S180](SOURCES.md#s180), [S181](SOURCES.md#s181), [S182](SOURCES.md#s182). **Исходные IDs:** W2-06-F03.

**W2-06-F03: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

`--load_backbone swav` приводит к загрузке `swav_800ep_pretrain.pth.tar`; teacher encoder также загружается оттуда и замораживается. Backbone использует FrozenBatchNorm2d. При `lr_backbone=0` feature weights не обучаются; при обычном backbone trainability `BackboneBase` всё равно фиксирует ранние слои за пределами layer2/3/4. Поэтому фраза «предобучен весь detector» не означает, что каждый backbone tensor изменялся этим pretext этапом.

`DETReg_top30_in.sh` задаёт topk/max_prop30, object_embedding_loss, замороженный backbone и 5 epochs; COCO-pretrain shell использует ту же идею, а duration берёт из defaults. Deformable defaults: 50 epochs, LR drop40, 300 queries; downstream default backbone LR2e-5. Есть отдельный object embedding output, включаемый только при `object_embedding_loss`.

В `main(args)` путь `args.pretrain` извлекает `checkpoint['model']`, **удаляет все keys с `class_embed`**, затем `load_state_dict(..., strict=False)`. Он не удаляет `bbox_embed`, transformer, query embeddings или input projections. Следовательно, при совпавшей topology их передача возможна и ожидаема; она ещё требует наблюдения actual missing/unexpected keys. Class-agnostic object-vs-background classifier не переносится как готовый PPE classifier. При обычном downstream shell embedding loss выключен; builder не запрашивает вспомогательную embedding ветвь, её checkpoint keys должны быть отдельно учтены как unused. Сохранение/поведение final graph проверяется будущим load/export, а не названием статьи.

Важная ловушка для будущего инженера: `args.pretrain` безусловно выбрасывает classifier даже у уже supervised source detector. Для source-detector class-row transfer этот путь недостаточен. `args.resume` — другой режим, способный восстанавливать optimizer/scheduler/epoch; его нельзя подставлять как универсальный warm-start с новым class count. Нужен явный audited weight loader, согласованный с model_stack. В Ultralytics такой контракт иной: см. F016/F10, а не механический перенос этого delete rule.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f237"></a>

### F237 — «Одинаковый downstream» имеет несколько уровней [CODE + INFERENCE; S179/S180/S182]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S179](SOURCES.md#s179), [S180](SOURCES.md#s180), [S182](SOURCES.md#s182). **Исходные IDs:** W2-06-F04.

**W2-06-F04: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

Более близкие сравнения — внутри одного detector и одного label set. Но даже они не автоматически измеряют один причинный фактор. DETReg versus supervised backbone меняет и происхождение backbone, и дополнительные detection components. DETReg versus SwAV ближе к вопросу о дополнительных localization/transformer weights. Доказать полную эквивалентность стартовых backbone tensors можно только hashes, не общим словом SwAV.

Авторский README даёт для few-shot один sample-set seed0; base route использует 60 classes/~99k labelled images, затем 150 epochs с drop140. No-base route использует 1000 epochs с drop990. Поэтому сравнение строк «с base» и «без base» из F234 показывает разные **packages supervision+training**, а не чистую пользу наличия supervised source detector. Это новое содержательное ограничение сверх W1 pretrained/scratch: нельзя приписать разницу исключительно source task или количеству transferred modules. F234 также не содержит base-class retention метрики: novel AP не доказывает сохранение нужных старых outputs.

Для COCO percentage budget `CocoDetection.__init__` случайно выбирает **images** с seed и `round(image_count*filter_pct)`. Это не percentage instances и не новые независимые scenes. В config1% стоит epochs2000/lr_drop2000, тогда как статья описывает выбор по прекращению улучшения validation. В прочитанном `main.py` epoch loop сохраняет current/periodic checkpoints и запускает eval; автоматического best selector/early stopper для заявленного convergence критерия не установлено. Воспроизведение требует восстановить внешний selection, а не считать последний checkpoint тем самым опубликованным best. Downstream transforms: train variable resize/crop, eval shortest side800/max1333; это также часть recipe.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f238"></a>

### F238 — Версии few-shot и artifact dates нельзя смешивать [METADATA/DOC; S178/S179/S183]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S178](SOURCES.md#s178), [S179](SOURCES.md#s179), [S183](SOURCES.md#s183). **Исходные IDs:** W2-06-F05.

**W2-06-F05: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

README changelog датирует обновление few-shot results и публикацию соответствующих checkpoints 17.07.2023; для чисел F234 использован arXiv v5 от20.07.2023. Оставшийся introductory claim старого README не используется как актуальная численная few-shot абляция. Это не основание объявить всю работу ошибочной: нужно выбрать конкретную редакцию и соответствующий artifact.

Release tag1.0.0 опубликован в2021, но few-shot assets обновлены 18.07.2023. `checkpoint_imagenet.pth` имеет size296372204 bytes, `checkpoint_coco.pth`296372268; четыре few-shot assets479887988 каждый, timestamps2023. Существуют отдельные `full_coco_finetune.pth` и files с `scratch` в имени. В README `scratch` здесь соответствует **отсутствию supervised base-class этапа**, а не полному отсутствию pretrained SwAV/DETReg knowledge. Одно имя файла не заменяет lineage.

GitHub release link устанавливает наличие опубликованного asset в API, но не его стабильный tensor hash, не доступность всех зависимостей и не успешный load. Assets не скачивались. Тот же tag допускает позднюю замену/добавление asset; для будущего manifest нужны URL, bytes/hash, created/updated timestamp и actual model state inventory.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f239"></a>

### F239 — Готовый artifact и собственное pretraining имеют разную цену [DOC + INFERENCE; S176/S179/S181/S182]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S176](SOURCES.md#s176), [S179](SOURCES.md#s179), [S181](SOURCES.md#s181), [S182](SOURCES.md#s182). **Исходные IDs:** W2-06-F06.

**W2-06-F06: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

| Маршрут | Цена использовать найденный artifact | Что добавляется при pretraining с нуля |
|---|---|---|
| DetCo backbone | Разрешение использования, получение файла, hash/key audit, conversion, совместимый detector setup и downstream FT | Нужен ещё конкретный pretext trainer: в данном repo не опубликован; ImageNet/SSL recipe/compute. Общая ссылка OpenSelfSup недостаточна |
| DETReg localization package | Release asset + SwAV dependency, build старого CUDA operator stack, load audit, downstream class head и FT | Selective Search proposals/cache, SwAV pretrained representation/teacher, IN/COCO corpus, pretext optimization и storage. Если буквально «с нуля», стоимость SwAV этапа тоже входит |
| Supervised source detector | Provenance/classes/coverage audit, частичный loader, head mapping, target adaptation | Source annotation acquisition/review и полное supervised detector training, помимо backbone origin |

README DETReg описывает Linux/Python>=3.7, PyTorch1.8/torchvision0.9 и компиляцию CUDA ops; установки не было. Его approximate1.5 days/8 V100 для приведённой ветки pretraining не имеет достаточно точной границы, чтобы переносить оценку на любую модель/IN100/IN1K или нашу RTX. Для full COCO FT отдельно указано2 days/8 V100. Это авторские оценки исторического окружения, не наши затраты; расходы подготовки proposals и предшествующего SwAV не объявлены включёнными. Готовые веса позволяют не оплачивать эти stages повторно, но setup/compatibility/human audit/downstream FT остаются. Новое in-domain pretraining не назначается первой работой лишь из-за наличия unlabelled video.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f240"></a>

### F240 — Source overlap и class semantics [INFERENCE из F234, F235, F236, F237, F238, F239 и ]

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-06-F07.

**W2-06-F07: условия/наблюдение** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):

In-domain COCO строка F234 получает весь train2017 как unlabelled exposure. Это содержательно другая постановка, чем ImageNet-only representation плюс1% labels: image exposure и compute неодинаковы. Такой режим допустим как SSOD/pretrain package, но не доказывает превосходство при одинаковых источниках. Val2017 назван evaluation; участие val в выборе остановки делает это development validation, не независимым lockbox. Совпадение нужного domain не даёт права включать будущую assessment camera в pretraining незаметно.

Для команды требуется lineage не только последнего checkpoint: image lists ImageNet/COCO/других source, supervised labels, pseudo/region targets, teacher ancestry, target exposure, duplicates/near-duplicate groups, cameras/sessions. По публичным описаниям этой ветки sample-level overlap ImageNet↔target↔COCO не проверялся; отсутствия overlap не утверждаем. Выявленное совпадение train и source может быть разрешённой подготовкой; пересечение с независимым assessment требует другого claim/protocol. Unknown provenance — отдельное ограничение оценки, а не автоматический ноль качества.

Общий label `person` может переносить localization полезнее, чем source `helmet` с другой annotation policy. Название совпавшего класса не устанавливает wearing/holding/absence/occlusion semantics. Отсутствие каски обычно не получается переносом row класса helmet. Какой именно output нужен, определяет кейс/violation_methods. Пустой или заменённый classifier не стирает pretrained localization knowledge, а shape-compatible classifier не подтверждает правильное состояние PPE.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-07 — W2-07 — Один source-free route: simple-SFOD, AdaBN + Fixed SF-FM

<a id="f241"></a>

### F241 — Маршрут существует, weights не образуют готовый package

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S185](SOURCES.md#s185), [S187](SOURCES.md#s187), [S190](SOURCES.md#s190). **Исходные IDs:** W2-07-F01.

**W2-07-F01: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code/local**, S185/S187/S190. README требует PyTorch≥1.12, Detectron20.6. Fixed recipe выбирает `TRAINER: base_wq`, `GeneralizedRCNN`, VGG backbone, обычные `RPN`/`StandardROIHeads`, 8 classes, `MASK_ON: False`. Source recipe начинает с локального `vgg16_bn.pkl`; fixed recipe — `/cluster/scratch/username/weights/adabn_weight2/adabn.pth`. Conversion helper читает локальный torchvision `vgg16_bn.pth` и переименовывает keys; это не source-trained detector checkpoint. В tree P нет опубликованного `.pth`/`.pkl`, API releases возвращает пустой список; README не предоставляет source detector download. Не проверялись внешние неуказанные хранилища.

**inference:** команда должна получить/создать законный source-trained detector с точной схемой keys/BN buffers/classes. До adaptation source images не требуются, но source training knowledge и pretraining остаются. Recipe не добавляет семантику новых PPE классов: одинаковые численные 8 classes не доказывают одинаковый порядок и смысл. YOLO checkpoint не загружается в этот Faster R-CNN по сходству задачи. Связь с F089/Q002 становится конкретнее, вопрос target compatibility остаётся.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f242"></a>

### F242 — AdaBN entrypoint меняет модель даже под именем eval-only

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S186](SOURCES.md#s186), [S190](SOURCES.md#s190). **Исходные IDs:** W2-07-F02.

**W2-07-F02: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code**, S186/S190. `main(args.eval_only)` строит model, загружает weights, затем вызывает **`base.test_refinement`**, а не закомментированный `Trainer.test`. Там `model.train()`, `torch.no_grad()`, batches из `BaseTrainer(cfg)` train loader, остановка при `i > 1400`, затем test и `DetectionCheckpointer(model).save("adabn")`. На непустом бесконечном train loader это до 1401 forward; это не буквальная одна epoch. Optimizer step отсутствует. BN слои создаются через `nn.BatchNorm2d`; no-grad не фиксирует running buffers. Affine/conv weights не оптимизируются этим loop, но BN state меняется.

Функция `adabn_refinement` отдельно сбрасывает BN statistics и дважды вызывает recursive traversal; **активный entrypoint её не вызывает**. Поэтому нельзя описать активный код как reset→exact full-dataset moments. Batch order, repeated images, momentum, batch size и исходные buffers входят в интервенцию. `TRAIN`, а не сам факт наличия `TRAIN_TARGET`, задаёт этот loader. Если взять source config для target AdaBN без проверки, loader будет source.

**inference:** frozen baseline нельзя получать слепым запуском этого `--eval-only`; нужен проверенный обычный eval path, равенство state до/после и запрет BN updates на holdout. Это новая конкретизация E005 и E020.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f243"></a>

### F243 — Fixed pseudo-label artifact имеет ручной и неоднозначный стык

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S188](SOURCES.md#s188). **Исходные IDs:** W2-07-F03.

**W2-07-F03: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code**, S188. Converter читает predictions `coco_instances_results.json`, отбрасывает scores `<0.7`, переносит `image_id`, `bbox`, `category_id`, присваивает annotation ID. Он читает существующий dataset JSON, **заменяет целиком `annotations`**, сохраняя images/categories, пишет другой жёстко заданный путь. `area`, `iscrowd`, confidence в новые annotations не добавляются. Возможный loader compatibility вопрос нужно проверить, не объявлять автоматически ошибкой.

`datasets.py` для Foggy train использует обычное `instancesonly_filtered_gtFine_train_foggy_beta_0.02.json`; строка специального `_adabn_pred.json` закомментирована. Следовательно, сам config не доказывает обучение по pseudo-labels: необходимо подтвердить, что этот JSON действительно заменён, и сохранить original отдельно. Иначе можно случайно использовать target GT, сохранив название source-free. Категории и image IDs должны соответствовать predictions; ручная подмена чужого JSON без проверки недопустима. Converter cutoff0.7 — факт этого helper, не универсальная confidence calibration.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f244"></a>

### F244 — Fixed training использует обычный detector и все возвращаемые loss terms

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S187](SOURCES.md#s187), [S189](SOURCES.md#s189), [S190](SOURCES.md#s190). **Исходные IDs:** W2-07-F04.

**W2-07-F04: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code**, S187/S189/S190. `BaseWQTrainer` строит один model/optimizer/loader; teacher network/EMA в выбранном route нет. `run_step` суммирует все keys с `loss` и без suffix `val`, делает backward/optimizer step. Здесь нет selective zeroing pseudo regression и нет source replay. RPN/RoI являются штатными detection modules согласно YAML. Отсутствующий pseudo box не получает специального ignore только потому, что данные unlabeled; spatial missing-label проблему этот path не решает.

`BaseWQDetection` оборачивает mapped dataset, применяет strong photometric/erasing augmentation к image, сохраняет instances. `mosaic=True` в wrapper — не доказательство четырёхкадрового Mosaic: в прочитанном `__getitem__` его композиции нет. Есть `yolox` imports и debug `cv2.imwrite` в локальный авторский путь; README requirements неполны для этой цепочки. VGG создаёт BN, а trainer не задаёт специальной fixed-statistics policy: после отдельного AdaBN BN следует train/eval режимам модели и hooks. Полную маску `requires_grad` выбранного установленного Detectron2 надо снять при будущем smoke, а не называть все backbone layers обучаемыми без учёта freeze defaults.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f245"></a>

### F245 — Checkpoint/selection interface не равно zero-label выбору лучшего качества

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S184](SOURCES.md#s184), [S187](SOURCES.md#s187), [S189](SOURCES.md#s189), [S190](SOURCES.md#s190). **Исходные IDs:** W2-07-F05.

**W2-07-F05: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code**, S187/S189/S190. Fixed config: LR0.0025, batch4, `MAX_ITER:100000`, warmup1000, checkpoint period1000, eval period100, seed42; test datasets source val и foggy val. `build_hooks` добавляет PeriodicCheckpointer и EvalHook, но не BestCheckpointer по quality; `last`/финальный checkpoint не означает лучший. `TEST.VAL_LOSS=True` по add_config включает ValLossHook на `TEST[0]`, здесь **source validation**. Hook делает forward под no-grad, не переключая модель в eval. Это label exposure для validation loss; при train-mode BN также возможен state exposure. Отсутствие gradient не превращает такую ветку в строгий source-data-free protocol. Этот hook необходимо отключить/проверить до строгого испытания, а source retention оценивать отдельно без изменения adapted state.

**paper**, S184 §§3.4/4.2/4.6, ограничивающий protocol: авторы предлагают fixed pseudo-labels после AdaBN; backbone Faster R-CNN/VGG16-BN и ImageNet pretraining. Для SF-UT сообщают шаг4000, выбранный по наблюдаемому оптимальному early stopping трёх задач; при этом прямо отмечают недопустимость test-set early stopping в чисто unsupervised режиме. Fig.4 показывает collapse self-training вариантов, а AdaBN+Fixed SF-FM устойчивее в данном опыте. Это не новый label-free checkpoint selector. Порог confidence не валидирует локализацию и пропуски. Published settings: target LR0.0025, batch4, threshold0.8, V10032GiB; metric AP/mAP при IoU0.5, дорожные benchmarks. Числа качества здесь не перенесены на CCTV. Точная last/best процедура для fixed-variant табличной строки не установлена.

**inference:** step4000 не переносить в наш schedule как обоснованный optimum. Code100000 не выдавать за точное повторение выбранного paper checkpoint. SED F089 ищет pseudo-label threshold, а не заменяет независимую model selection. Снижение entropy, loss или увеличение confident box counts не закрывает качество; даже detector confidence безошибочно не измеряет отсутствие unseen positives.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f246"></a>

### F246 — Final graph и source retention

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S187](SOURCES.md#s187), [S189](SOURCES.md#s189), [S190](SOURCES.md#s190). **Исходные IDs:** W2-07-F06.

**W2-07-F06: условия/наблюдение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):

**code/inference**, S187/S189/S190. Для fixed route checkpoint содержит один стандартный `GeneralizedRCNN`: VGG16-BN→RPN→RoI head→boxes/classes/scores, с адаптированными weights/BN buffers. Нет teacher ensemble, source loader или pseudo-label generation в inference. Backbone custom registration нужен для загрузки; это не доказательство совместимости обычного YOLO exporter или LinQ. В deploy важны и model parameters, и BN buffers, config, category mapping, preprocessing/NMS. Не выполнять AdaBN при final holdout inference.

Без независимых old-domain данных нельзя измерить сохранение source качества. Source-free алгоритм не доказывает отсутствие forgetting; frozen fallback сохранять отдельно. Малый source retention evaluator не превращается в разрешение source-data access при adaptation: роли и state effects разнести явно.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-08 — W2-08 — Gen2Det: supervision, artifact gap и exposure contract

<a id="f247"></a>

### F247 — [LOCAL METADATA OBSERVATION] author release не найден

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S191](SOURCES.md#s191), [S192](SOURCES.md#s192), [S193](SOURCES.md#s193). **Исходные IDs:** W2-08-F01.

**W2-08-F01: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

S191, S192, S193 дают узкий отрицательный результат: открытые publication entries не ведут к Gen2Det code; exact-name repository search и публичный список первого автора не выявили implementation. Это не доказывает, что код никогда не публиковался, отсутствует под другим названием или не существует внутри Meta. Содержательный public поиск завершён при отсутствии новой primary зацепки. Недостающее звено — **author Detectron2/CenterNet2 fork + commit, trainer/config, filtering scripts и сериализованный sample annotations**, а не ещё одна общая статья о синтетике.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f248"></a>

### F248 — [PAPER] минимальный filtering/supervision contract

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W2-08-F02.

**W2-08-F02: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

S099 §§3.3–3.4/4.1: image filter отбрасывает целое изображение. Instance filter удаляет annotation без достаточно уверенного overlapping detector prediction; pixels остаются, возможны extra instances. Background-ignore охватывает RPN и detector head; `τ_i=0` означает игнорирование всех synthetic background regions. Synthetic mask loss выключен. Это **не** утверждение о class-aware/spatial tensor implementation: class-match condition фильтра, normalization, порядок assignment/sampling/ignore, CenterNet2-specific terms и empty-valid-box handling не установлены.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f249"></a>

### F249 — [PAPER + OUR DERIVATION] знаменатели ratio различны

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W2-08-F03.

**W2-08-F03: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

S099 §3.4.1/4.1: `p=0.2` — вероятность целиком synthetic batch среди training batches; остальные batches real. Это не доля synthetic objects, не synthetic/real pool ratio и не автоматически 20% файлов в combined folder. В Table 6(c) множитель synthetic data относится к объёму generated sample pool; в Table 6(a) `×` — training schedule. Точный config с абсолютным числом iterations, batch, sample draw/with-replacement, world-size synchronization и mapping этих осей на финальные строки не получен.

**Наша арифметика при явно условных предпосылках:** для `T` optimizer steps с одним batch одинакового размера `B` на step и Bernoulli выбором источника, без accumulation/skips, ожидаемые exposures `E_real=(1-p)TB`, `E_synth=pTB`. При `p=0.2`: synthetic:real exposures `1:4`, synthetic/all `1:5`. Это не равно pool size: даже большой pool может редко встречаться. Если изменение schedule `T0→2T0` действительно применяется к сравниваемому arm, ожидаемая real exposure относительно all-real `T0` равна `1.6`, synthetic — `0.4` baseline-exposure units. Это иллюстрация confound, **не восстановленный бюджет авторской строки**. При accumulation считать фактические source draws и optimizer updates отдельно.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f250"></a>

### F250 — [PAPER LIMIT] low-data результат не доказывает необходимость полного package

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W2-08-F04.

**W2-08-F04: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

S099 Supplement §6 прямо исключает filtering и background-ignore в LD-COCO из-за малого числа изображений/instances. Поэтому low-data gains W1-11 не являются проверкой «без полного Gen2Det loss синтетика не работает». Напротив, это зависимый от режима recipe. Не переносить full-data setting на few-shot PPE без проверки; не выдавать случайные COCO image subsets за независимые камеры или shots/class.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f251"></a>

### F251 — [PUBLISHED ABLATION / PROVENANCE] ограничения causal reading

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W2-08-F05.

**W2-08-F05: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

S099 Table 5, **LVIS Mask R-CNN**, box AP: real 22.29, naive mix 20.75, +sampling 23.49, +image filter 23.78, затем detector-filter-only 23.76, background-ignore-only 23.32, совместно 24.42. Здесь последние три arms отсчитываются от sampling+image-filter arm. Отдельные вмешательства не дают монотонного улучшения; нельзя приписать весь gain одному ignore или одному filtering. §4.1 задаёт ImageNet-1k initialization для Mask/Faster R-CNN; §6 — LR 0.04 LVIS, batch 4× default. Table 6 отдельно варьирует schedule. Absolute iterations/input dimensions/hardware, exact sample accounting и checkpoint selection для каждого row не установлены; не выдавать это за matched-budget causal experiment или PPE expected gain.

F140 COCO CenterNet2 row происходит из S099 Table 2, не Table 5: авторы в §4.1 говорят, что COCO XPaste evaluation numbers заимствованы из-за отсутствующих соответствующих configs/details; LVIS XPaste rerun сделан ими. Поэтому COCO table — не подтверждение полностью воспроизведённого всеми arms local recipe. Это уточнение происхождения сравнения, не обвинение в недостоверности таблицы.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f252"></a>

### F252 — : стадия / term | Что установлено | Какой artifact/metadata нужен; что неизвестно

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S099](SOURCES.md#s099). **Исходные IDs:** W2-08-F06.

**W2-08-F06: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

| F252: стадия / term | Что установлено | Какой artifact/metadata нужен; что неизвестно |
|---|---|---|
| Generate → image | Исходные image, boxes, class names обусловливают inpainting, S099 §3.2 | Generated image ID → source image/split, seed/model revision, source boxes. Реальный author schema не найден |
| Image filter | Отбрасывает изображение целиком, S099 §3.3.1 | Keep/drop ID и score/filter revision; нельзя сохранять его labels с другим image |
| Instance filter → annotations | Удаляет неподтверждённую annotation, S099 §3.3.2 | Mapping original→retained/discarded annotation, predictions/reasons; совпадение predicted class с class GT в фактическом code не известно. Текст описывает score+IoU, что не разрешает додумать class condition |
| Pixels discarded/extra objects | Остаются/могут появиться, S099 §3.4.2 | Positive labels не делают остальной кадр verified negative. Extra instances не «исчезают» после JSON filtering |
| Loader/batch source switch | Paper различает real/synthetic batches | Фактическое поле `is_synthetic` или иной equivalent provenance, mapper propagation, loss dispatch неизвестны. Название поля здесь не API автора |
| RPN assignment + objectness | Paper заявляет background-ignore для RPN | Где создаётся bg/fg label, меняется ли до/после anchor/proposal sampler; сохраняется ли count denominator; какие confident foreground scores используются — неизвестно. Нельзя объявить RPN negatives автоматически решёнными только по RoI mask |
| RPN box regression | Paper не даёт tensor trace | Какие positives остаются после filtering и способ normalization не проверены. Нельзя утверждать, что discarded regions дают нулевой градиент всем параметрам |
| RoI/detector classification | Paper заявляет detector-head bg-region ignore | Background sample ignore и suppress всех negative class entries на positive RoI — разные операции. Class-specific negatives, federated/softmax/sigmoid distinction и spatial scope вне retained positives не установлены |
| Detector box regression | Имеются retained box annotations; exact assignment не показан | Matching targets, sampling positives, ignored GT treatment, empty targets и reduction неизвестны |
| CenterNet2/иные stages | Paper использует адаптированный instance-segmentation CenterNet2 | First-stage heatmap/objectness, stages каскада, dense unmatched locations: actual modified terms не найдены. Нельзя приравнять к standard RPN или перенести на one-stage BCE/DFL |
| Synthetic mask loss | Выключен в paper | Должна отсутствовать попытка использовать старую маску после inpainting; exact conditional dispatch/reduction не известны. Real mask supervision не объявляется выключенным |
| Synthetic image без valid boxes | Paper не определяет реализацию edge case | Может loader отбросить кадр, head вернуть zero или он дать иной loss; ни один вариант не установлен. Не превращать в hard negative |
| Eval/final artifact | Описаны изменения данных/training, не новая inference branch, S099 §§3–4 | Paper-level ожидание обычного detector. Final eval graph/config/checkpoint extraction, отсутствие training-only dependencies при reload/export actual кодом не подтверждены |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f253"></a>

### F253 — [OUR INFERENCE] spatial/class scope. При `τ_i=0` словесный scope — все background regions synthetic image, а не только исходные discarded boxes или конкретные…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-08-F07.

**W2-08-F07: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

**F253 [OUR INFERENCE] spatial/class scope.** При `τ_i=0` словесный scope — все background regions synthetic image, а не только исходные discarded boxes или конкретные filtered classes. Это существенно шире «поставить ignore rectangle на удалённую annotation» и может охватывать hallucinated extra instances. Но bg-region определяется конкретным assigner; невозможно по этой фразе доказать отсутствие negative supervision для другого класса в retained positive region или другого stage. Для `τ_i>0` scope ещё зависит от confidence текущего detector. Указание RPN в paper опровергает удобное упрощение «достаточно поправить один classification head»; actual поведение остаётся Q020.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f254"></a>

### F254 — matrix допустимых маршрутов и final graph

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-08-F08.

**W2-08-F08: условия/наблюдение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):

| Route | Annotation/negative contract | Trainer и окончательный artifact | Решение сейчас |
|---|---|---|---|
| Fully reviewed synthetic | Reviewer проверяет весь кадр, все рабочие classes/instances, extra objects и состояния; исправляет boxes; mask только если реально переразмечена. Negative label допустим лишь после полного review в заданной policy | Обычный выбранный supervised detector с полностью поддержанным annotation format. Данные — единственное вмешательство; архитектура inference не меняется по нашему design. Final checkpoint должен пройти обычные reload/export/LinQ gates | Допустимый будущий data-only trial после real baseline; это наша процедура, не Gen2Det reproduction |
| Filtered pseudo synthetic, special loss | Неисчерпывающие labels; нужны source tag, surviving labels, mask availability и реально обработанный missing-object supervision во всех affected stages | Нужен author fork+commit/config или отдельно проверенная интеграция. Gen2Det paper задаёт intent, но available implementation/port не установлен; final graph также требует artifact inspection | Не ставить в тренировочную очередь до Q020 и hidden-GT correctness gate E007 |
| Unsupported union filtered labels + ordinary closed-world trainer | Оставшиеся pixels и extra instances могут стать negatives; JPG/JSON conversion теряет provenance/coverage | Архитектура может остаться обычной, но это не делает supervision корректным | Не использовать как воспроизведение; перевести в fully reviewed route или остановить |

Fully reviewed означает исчерпывающе в заранее указанной annotation policy (class/ROI/visibility/size); не обещает знать невидимые PPE states. Если policy требует ignore unknown, а trainer его не поддерживает, crop/exclude весь sample по допустимой семантике либо доразметить; не молча записывать unknown как background. Group person+PPE semantic gate из W1-11 остаётся нашим предложением, не техникой Gen2Det.

Для data-only route генератор/filter/reviewer и их models не нужны во время inference. Это вывод из предложенного собственного route, где архитектура фиксирована, а не подтверждённый author export. Для paper route нет основания требовать diffusion model на inference, но нет и inspected artifact, доказывающего clean reload. Ни один маршрут не устанавливает LinQ compiler/operator compatibility или качество wearing/smoking.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-09 — W2-09 — Detector QAT → export: конкретный NVIDIA YOLOv7 route и граница LinQ

<a id="f255"></a>

### F255 — Почему MMrazor не выбран готовым detector QAT recipe

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S203](SOURCES.md#s203). **Исходные IDs:** W2-09-F01.

**W2-09-F01: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Наблюдение по документации/конфигам/дереву, S203.** Guide закрепляет `torch==1.13`, export через ветку MMDeploy `for_mmrazor`; для dense heads предлагает fork MMDetection. Найденный RetinaNet R50-FPN config содержит `PTQLoop`/calibration, а доступные QAT configs в обследованных v1.0.0/main — ResNet18/LSQ. Поэтому соединение RetinaNet PTQ config с ResNet QAT training loop было бы нашим новым port. Это ограниченный negative result данного дерева, не утверждение отсутствия QAT support или любого внешнего detector config.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f256"></a>

### F256 — Training interface найден, но это reconstruction QAT

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S196](SOURCES.md#s196). **Исходные IDs:** W2-09-F02.

**W2-09-F02: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Код S196, `finetune` и `calibrate_model`.** Замена modules использует toolkit default map; затем калибровка собирает ranges и `method="mse"`. QAT создаёт frozen quant-disabled clone; Adam обучает модель по сумме MSE hooked features. GT detector loss не вызывается. Defaults: 10 epochs, максимум 1000 batches/epoch, AMP, LR schedule `0:1e-6, 3:1e-5, 8:1e-6`; это recipe автора, не наша рекомендация. Calibrated ranges отключают дальнейший сбор статистики. Экспорт включает `use_fb_fake_quant`, вызывает `torch.onnx.export` в eval/no_grad и выключает switch. **Вывод:** labels нужны для оценки качества; эта реализация не учит новую семантику классов посредством bbox/class supervision. Данный факт уточняет blanket wording F159 о labels для QAT loss: найден label-free reconstruction вариант.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f257"></a>

### F257 — Detector-specific вход, checkpoint, selection и export

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S195](SOURCES.md#s195). **Исходные IDs:** W2-09-F03.

**W2-09-F03: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Код S195.** Загружается `torch.load(...)["model"]`, выполняется `model.float().eval().fuse()` до quant insertion. COCO train loader: 640, augment=True, batch default 10; calibration/QAT получают `float()/255`. Supervision policy выбирает отдельные top-level layers и исключает last head. Per-epoch COCO AP выбирает сохранение `{"model": model}`; optimizer/resume state не входит. `export_onnx` выставляет last-head `.concat=True`, адаптирует grid, объявляет opset 13, вход `images`, выход `outputs`; `--dynamic` делает динамическим **batch**, не H/W. Default dummy — `[1,3,640,640]` FP32. Это tied-to-YOLOv7 API, не generic exporter для YOLO8/11/26.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f258"></a>

### F258 — Fusion и head являются частью quant contract

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S201](SOURCES.md#s201). **Исходные IDs:** W2-09-F04.

**W2-09-F04: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Код S201.** `Model.fuse` сворачивает Conv+BN, переводит RepConv и OREPA в deploy representation, сворачивает implicit head parameters и меняет forward. В `IDetect.fuseforward` `.concat=True` возвращает concatenated decoded predictions; для COCO head `nc=80`, `no=nc+5`. NMS по этому пути не добавлен. **Наш вывод:** менять fusion order после QAT нельзя без повторной parity проверки. В v0.1 `concat` interface не найден, в обследованном main он есть; release weight URL `v0.1/yolov7.pt` не закрепляет source compatibility экспортера. Нужны source pin и reload smoke, а не подмена source tag названием weight release.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f259"></a>

### F259 — Q/DQ placement не просто автоматическая обёртка Conv

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S197](SOURCES.md#s197). **Исходные IDs:** W2-09-F05.

**W2-09-F05: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Код S197.** Правила просматривают временный ONNX, находят quantizers на ветвях Concat и MaxPool. Они возвращают пары для последующего разделения одного input quantizer между связанными modules. Это ограниченный pattern matcher с предположениями о соседстве Q→DQ→Conv и именовании weight nodes. Он не устанавливает глобальную поддержку произвольного residual/attention/head graph. Не переносить на другую архитектуру по одному имени YOLO. **Вывод:** совпадение scales/axes недостаточно; target должен сохранить смысл размещения QDQ и допустимой fusion.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f260"></a>

### F260 — Arithmetic reference toolkit 2.1.2, условный до environment lock

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S194](SOURCES.md#s194), [S198](SOURCES.md#s198), [S199](SOURCES.md#s199), [S200](SOURCES.md#s200), [S202](SOURCES.md#s202). **Исходные IDs:** W2-09-F06.

**W2-09-F06: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Наблюдение по S198, S199, S200.** Это исследованный reference, а не доказанная package версия S194 experiment.

| Contract field | Установленное по source reference | Ограничение переноса |
|---|---|---|
| Signedness / bit | Descriptor default 8-bit signed, `unsigned=False`, `fake_quant=True` [S198]; route задаёт histogram input descriptor [F256] | Не присваивать unsigned activation по аналогии с OpenVINO/MMrazor |
| Activation granularity | Descriptor default axis=None → per tensor [S198] | Фактический QAT checkpoint нужно инспектировать |
| Conv weight granularity | `QuantConv2d` default `axis=(0)` → output-channel K в KCRS; input/weight quantizers применяются до convolution [S199] | Не axis=1 activation layout; depthwise/head должны проверяться отдельно |
| Range / scale | Descriptor `narrow_range=False`; `_tensor_quant` clamp signed full range `[-128,127]`, inverse scale `127/amax`, round; fake outputs возвращаются в FP [S198] | Это не integer training и не свидетельство accumulator/bias precision LinQ |
| Zero-point / export | `_fb_fake_quant`: scale=`amax/127`, zero point 0; scalar для per-tensor, vector для per-channel, bounds `[-128,127]` [S200] | Не affine offset из произвольного PTQ; фактический emitted dtype/axis ещё требует graph inspection |
| Rounding | Native reference вызывает Tensor `.round_()` [S198]; ONNX QuantizeLinear-13 определяет nearest-even и saturation [S202] | Пограничные half-step/clipping values должны быть будущим parity тестом, не обещанием bit identity |
| Learned ranges | Descriptor default `learn_amax=False` [S198] | Нельзя называть этот route LSQ или learned clipping |

**Финальный format contract:** путь к ONNX использует PyTorch native fake-quant export representation; ожидаются `QuantizeLinear`/`DequantizeLinear`, не `QLinearConv`, не `.ort`. QDQ остаётся в FP operator graph и задаёт quant boundaries; actual backend precision устанавливается compilation/placement log. ONNX per-axis default axis=1 не заменяет явно необходимый Conv weight axis=0. S200/S202 подтверждают требуемую семантику, но реальный binary ONNX здесь не получен.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f261"></a>

### F261 — Авторский backend evidence ограничен и имеет shape discrepancy

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S194](SOURCES.md#s194), [S204](SOURCES.md#s204). **Исходные IDs:** W2-09-F07.

**W2-09-F07: условия/наблюдение** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):

**Документация S194 + код S204.** README связывает detector, COCO evaluation, QAT checkpoint и ONNX; предлагает контейнер `nvcr.io/nvidia/pytorch:22.09-py3`, но `pip install pytorch-quantization` не фиксирует package version. В таблице указан input 640 и TensorRT/Orin, однако `eval-trt.sh` принудительно экспортирует 672 и допускает `--fp16` для detection layer. **Вывод:** не реконструирована точная опубликованная измерительная цепочка, поэтому AP/FPS из README не используются как прогноз/сравнение для LinQ и не приписываются одному закреплённому environment. Claim «all nodes INT8» требует actual layer report; presence QDQ сам его не доказывает.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-10 — W2-10 — Physical detector pruning: один Torch-Pruning/YOLOv8 route

<a id="f262"></a>

### F262 — Versioned positive route ограничен старым YOLOv8

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S206](SOURCES.md#s206), [S207](SOURCES.md#s207), [S212](SOURCES.md#s212). **Исходные IDs:** W2-10-F01.

**W2-10-F01: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: primary documentation + code observation, S206/S207/S212.** README закрепляет U, который действительно объявляет Ultralytics 8.0.90; tested environment перечисляет PyTorch 2.5.1 и TP 1.6.1. GitHub tag TP 1.6.1 разрешается точно в T, на котором прочитан код. Script default model — `yolov8m.pt`; он ожидает C2f/Bottleneck/Detect и старые импорты `ultralytics.yolo.*`. Это не route для W1 pin Ultralytics 8.4.184, YOLO11 или YOLO26. README предупреждает: “This example is crashed due to ultralytics upgrade.” Документированный pin даёт разумную точку воспроизведения, но не наш runtime certificate.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f263"></a>

### F263 — C2f меняется до pruning, веса переносятся по ветвям

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207), [S212](SOURCES.md#s212). **Исходные IDs:** W2-10-F02.

**W2-10-F02: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation, S207 `C2f_v2`, `transfer_weights`, `replace_c2f_with_c2f_v2`; S212 `C2f`/`Bottleneck`.** Штатный C2f делает одну Conv→BN→activation с `2*c` выходами, затем `chunk(2,1)` и concat с результатами bottlenecks. В C2f_v2 две отдельные Conv `cv0/cv1`, их выходы проходят тот же chain и `torch.cat`, после которого работает `cv2`. Старый `cv1.conv.weight` делится по output dimension; обе части BN weight/bias/running_mean/running_var переносятся; `cv2` и ModuleList bottlenecks переиспользуются. Shortcut определяется через `infer_shortcut`, groups/n/e восстанавливаются из исходного блока. Так граница split убирается из forward представления до удаления каналов.

**Вывод:** это topology rewrite даже при нулевом pruning. Сначала нужна численная проверка converted-unpruned против original, отдельно от quality loss от удаления. `self.c` остаётся атрибутом, но в новом forward не используется для `chunk/split`; нельзя восстанавливать actual channels только по этому старому scalar. Функция `initialize_weights` в script вызвана для BN eps/momentum и inplace activations; её имя само по себе не означает новое обучение с нуля. Фактическую эквивалентность переноса нами не проверяли.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f264"></a>

### F264 — DepGraph связывает Conv/BN/branch channels, а не проставляет masks

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S208](SOURCES.md#s208), [S209](SOURCES.md#s209), [S210](SOURCES.md#s210), [S211](SOURCES.md#s211). **Исходные IDs:** W2-10-F03.

**W2-10-F03: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation, S208, S209, S210, S211.** `GroupNormPruner` через base constructor вызывает `DependencyGraph().build_dependency(model, example_inputs=...)`. Требуется включённый autograd; build содержит assert против `torch.no_grad()`. Script ставит `requires_grad=True`, dummy input имеет `[1,3,imgsz,imgsz]`. Хотя script перед constructor вызывает `model.train()`, `_trace` внутри TP переключает model в eval и регистрирует forward hooks; graph строится из реально пройденного forward/autograd graph. Этот нюанс следует сохранить в smoke, а не приписывать tracing train-head outputs.

`_build_dependency` связывает output-channel pruning upstream слоя с input-channel pruning downstream и обратное отношение. `get_pruning_group` проходит вызванные зависимости и применяет index mappings. Residual `Add` представляется elementwise node: связанные каналы ветвей удаляются согласованно, иначе сложение нарушает shape contract. Для channel concat `update_concat_index_mapping` вычисляет размеры ветвей и cumulative offsets; downstream index переносится в правильную ветвь, а branch index — в общий concat tensor. Это относится и к C2f concat, и к neck joins в реально traced графе. Нельзя вручную удалить один Conv filter и игнорировать его потребителей.

`Group.prune` вызывает handlers всех связанных операций. `ConvPruner` уменьшает `in_channels/out_channels` и заменяет weight через `index_select` соответствующей оси, bias при output pruning; `BatchnormPruner` уменьшает `num_features`, affine tensors и running statistics. Это **меньшие dense tensors**, в отличие от F162/F270 `ln_structured` масок исходной формы. Примеры dependent shapes будущего manifest: Conv `[Cout,Cin/groups,kH,kW]`, BN `[Cout]`, следующий Conv input axis, concat consumer sum-of-remaining-branch-channels. Конкретные удалённые indices возникают только в будущем выполнении; здесь их нет.

**Ограничение:** tracing одного input не сертифицирует все dynamic branches/shapes. Неизвестные операции TP может трактовать как elementwise; это повод осмотреть groups/shape assertions, а не считать любой custom detector автоматически поддержанным.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f265"></a>

### F265 — Detect исключён из output pruning; head inputs всё равно зависимы

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207), [S208](SOURCES.md#s208), [S211](SOURCES.md#s211), [S212](SOURCES.md#s212). **Исходные IDs:** W2-10-F04.

**W2-10-F04: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation + вывод, S207 319–334, S211 base 124–145, S208 `get_all_groups`, S212 `Detect`.** Script добавляет каждый `Detect` в `ignored_layers`. BasePruner разворачивает каждый ignored module в его descendants. Эти модули остаются в dependency tracing: список exclusions не передаётся как `ignored_layers` в `build_dependency`, а применяется при выборе pruning groups. Группы с output pruning ignored module отклоняются. Поэтому исключение головы не означает полную изоляцию от upstream channel changes: входные оси первых head Conv могут сокращаться, сохраняя их output widths.

В U Detect `reg_max=16`, `no=nc+4*reg_max`; terminal box Conv имеет 64 outputs, terminal cls Conv — `nc`, DFL сохраняет свой contract. Training head возвращает per-level raw maps; inference формирует `[B,4+nc,N]` decoded xywh и sigmoid class scores; export возвращает этот tensor без обычного tuple с raw maps. Script не заменяет Detect.forward, число классов не сокращает и semantic class remapping не делает. Preserve `nc`, `names` и class order — отдельная обязательная проверка, не следствие уменьшения backbone.

Особенно опасно слепо скопировать demo на custom data: script **перезаписывает** `pruning_cfg['data']='coco128.yaml'`, а pinned trainer `set_model_attributes` присваивает outer model.nc/names из data. В pruning режиме объект головы переиспользуется, вместо штатной пересборки через `get_model(cfg,nc=...)`. Поэтому custom ontology/head следует согласовать **до** surgery, убрать toy override в будущей контролируемой интеграции и проверить head.nc/terminal shapes/data names совместно. Иначе metadata и реальные logits способны разойтись. Это установленная точка риска, а не воспроизведённая ошибка.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f266"></a>

### F266 — Criterion и recovery: итеративное удаление, затем supervised fine-tuning

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207), [S211](SOURCES.md#s211). **Исходные IDs:** W2-10-F05.

**W2-10-F05: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation, S207 `prune`; S211 `GroupMagnitudeImportance`/constructors.** Используется `GroupNormPruner` с `GroupMagnitudeImportance()`; defaults importance — p=2, mean group reduction/normalizer, а не detection-loss saliency. `global_pruning` не задан и по default False. Regularization/backward demo закомментировано: нельзя объявлять этот example sparse-training recipe только по имени GroupNormPruner. One-step pruner создаётся заново для каждого внешнего шага; доля шага вычисляется `1-(1-target_prune_rate)^(1/iterative_steps)`. Это channel schedule, а не гарантия точной общей доли parameters/MACs или времени.

После `step()` выполняется pre-recovery validation, затем `train_v2(pruning=True, ...)`, reload best и post-recovery validation; точки записываются отдельно. Demo жёстко назначает coco128 и 10 epochs на шаг; CLI defaults 16 steps/target rate 0.5/max_map_drop 0.2 — **sample settings, не рекомендация для CCTV**. Нужны настоящие train labels и independent development validation; toy repeated validation не доказывает target quality. Recovery budget должен учитываться целиком, включая промежуточные validations/saves/export.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f267"></a>

### F267 — Normal YAML rebuild уничтожает topology; patch сохраняет actual object

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S206](SOURCES.md#s206), [S207](SOURCES.md#s207), [S214](SOURCES.md#s214). **Исходные IDs:** W2-10-F06.

**W2-10-F06: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation, S207 `train_v2`, `save_model_v2`, `strip_optimizer_v2`; S206.** Нормальная ветка вызывает trainer.get_model с исходным YAML. Pruning branch вместо этого передаёт `self.trainer.model=self.model`, сохраняя изменённую topology. Таким образом YAML исходной YOLOv8 и plain state_dict недостаточны для reconstruction произвольно изменённых widths/C2f_v2. Возможен отдельный shape-aware constructor, но в этом route его нет.

Custom save кладёт в checkpoint full `deepcopy(de_parallel(self.model))` и EMA object, optimizer state/epoch/best_fitness/args/version. `final_eval_v2` использует custom strip, который выбирает EMA как model, убирает optimizer/ema/updates и делает параметры requires_grad=False, сохраняя full-precision model object. Это вмешательство в trainer lifecycle, не универсальный файл `pruned.yaml`. Оно также означает, что final stripped artifact нельзя объявить exact resume state.

**Python dependency:** C2f_v2 должен существовать по подходящему import path при unpickling. В owner reply S214 автор прямо требует импортировать класс в predict process; без этого сообщался `Can't get attribute 'C2f_v2'`. Будущий reusable artifact должен включать versioned custom module и стабильный module path, а clean-process reload — быть gate до recovery budget. Современные torch.load defaults также нельзя молча переносить на исторический script: код использует full-object load без специально заданного weights_only; нужен фактически pinned environment/reload check, а не обещание совместимости любого PyTorch.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f268"></a>

### F268 — Export route указан, но пока не проверен артефактом

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207), [S213](SOURCES.md#s213). **Исходные IDs:** W2-10-F07.

**W2-10-F07: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation + ограниченный вывод, S207 384; S213.** Example заканчивается `model.export(format='onnx')`; собственного patched exporter в нём нет. Pinned YOLO.export передаёт existing model object в Exporter. Exporter deepcopy→eval/float/fuse, ставит Detect.export/format, делает dry runs и `torch.onnx.export`, input `images`, detection output `output0`. `C2f_v2` не subclass C2f, поэтому стандартный switch на C2f.forward_split его не затрагивает: работает его собственный Conv/concat forward. Это объясняет code-level возможность трассировать modified graph без YAML rebuild; наличие строки export не доказывает успешный ONNX/его parity.

Example не задаёт явные opset/static-dynamic/simplify/input args для итогового export. Pinned exporter использует args и fallback opset, поэтому будущий contract обязан сохранить их фактические значения и graph hash. Не считать ONNX opaque custom Python module: после успешного tracing следует проверить реальные ops/shapes, отсутствие неожиданных Python/custom nodes, output decoding и metadata. Exporter в U содержит закомментированный `onnx.checker.check_model`; внешний smoke должен явно включить graph validation и парный inference. Исторический issue #147 содержит reported mismatch после C2f conversion и ответ о возможной проблеме копирования весов; это ограничивающий lead, не доказательство отказа T/U.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f269"></a>

### F269 — Early stop demo не откатывает последний плохой шаг

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207). **Исходные IDs:** W2-10-F08.

**W2-10-F08: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation + вывод, S207 380–384.** Если `init_map-current_map > max_map_drop`, loop делает break; затем всё равно export текущего model. Видимой загрузки последнего допустимого pruning stage перед export нет. Поэтому не использовать этот early stop как acceptance/rollback contract. Хранить immutable stage candidates и экспортировать явный accepted stage; aggregate mAP gate не заменяет critical class/size gate команды.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f270"></a>

### F270 — Строка speed up в script является MAC ratio

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S207](SOURCES.md#s207). **Исходные IDs:** W2-10-F09.

**W2-10-F09: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: code observation, S207 350–353.** `current_speed_up = base_macs / pruned_macs`, после чего печатается `speed up`. В выбранном example отсутствует соответствующий timed runtime benchmark: нет установленного device/software/input-batch/warmup/sync/timing boundary для этого отношения. README иллюстрирует меньшие tensor dimensions/MACs/parameters, но не даёт здесь воспроизводимый target timing protocol. Поэтому численные mAP/скорость из screenshot и generic TP latency таблицы не используются; CUDA/CPU latency других моделей и тем более LinQ gain не выводятся. Serialized bytes также не измерялись. Это сохраняет E039 и уточняет конкретную ловушку имени variable.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f271"></a>

### F271 — Smaller native student имеет другой integration contract

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-10-F10.

**W2-10-F10: условия/наблюдение** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):

**Тип: наш вывод из F262, F263, F264, F265, F266, F267, F268, F269, F270 и F120/F12/E03, E039.** У штатного меньшего detector сохраняются архитектурный constructor, package modules и обычный loader/exporter той версии, которую команда уже проверяет. У physical pruning добавляются custom C2f, channel index/dependency manifest, trainer patches, full-object serialization, отдельная parity conversion и новые dense widths для compiler. KD в W1 при нормальном final unwrap должен оставить стандартный student; pruning намеренно оставляет изменённую topology. Ни один путь не имеет заранее установленного quality/latency ranking на LinQ.

| Условие | Меньший штатный student | Этот physical pruning route |
|---|---|---|
| Исходный artifact | Поддержанный штатный checkpoint/architecture, свой quality baseline | Согласованный trained YOLOv8 checkpoint на U; toy coco128 override нельзя переносить |
| Граф после вмешательства | Штатные widths/modules | C2f_v2 + сокращённые dense dimensions; head output contract сохраняется |
| Recovery | Обычный supervised/KD путь при нужде | Специальный train_v2, повторный supervised recovery каждого принятого stage |
| Serialization | Обычный loader выбранной версии | Full model/EMA objects + доступный custom class; исходный YAML не восстанавливает topology |
| Export | Уже известный штатный route всё равно проверяется | Указан штатный ONNX exporter U, но требуется новый smoke/parity и фактический opset/shape contract |
| LinQ | Неизвестно до compiler/run | Неизвестно; новые widths могут изменить compiler mapping и utilization |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-11 — W2-11 — Checkpoint objective, lifecycle и freeze→unfreeze

<a id="f272"></a>

### F272 — Порядок одного epoch и нормального завершения

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S081](SOURCES.md#s081), [S104](SOURCES.md#s104), [S216](SOURCES.md#s216). **Исходные IDs:** W2-11-F01.

**W2-11-F01: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**CODE, S011/S081/S216/S104; уточняет F152 и F185.** Порядок ниже существенен: observer callback после save уже не может задним числом изменить fitness этого файла.

| Порядок в `_do_train` | State / следствие |
|---|---|
| `self.epoch=epoch`; `on_train_epoch_start`; `scheduler.step()`; `_model_train()` | Callback epoch-start выполняется **до** model.train/BN freeze. BN eval, выставленный только этим callback, затем может быть сброшен |
| batches → backward → накопление → `optimizer_step()` | unscale → clip norm 10 → scaler.step/update → zero_grad → EMA.update. EMA update count не равен batch count |
| criterion.update (если есть); LR snapshot; `on_train_epoch_end` | Validation ещё не выполнена; metrics здесь могут относиться к предыдущему epoch |
| EMA.update_attr(yaml/nc/args/names/stride/class_weights) | Training validation получает EMA; weights float, eval, inference-mode/autocast в validator |
| `final_epoch = epoch+1 >= epochs`; conditional `validate()` | Выполняется при `val or final_epoch or stopper.possible_stop or stop`. Для каждого-epoch отбора требуется `val=True`; `val=False` не гарантирует свежую fitness каждого save |
| `validate`: validator → pop fitness → update best_fitness | Standard detect fitness — AP50:95, установлен F185. Best обновляется строго при improvement; fallback при отсутствии fitness — negative loss |
| `_handle_nan_recovery(epoch)` | При recovery до save/callbacks возврат к epoch loop, повреждённый pass не считается новым candidate |
| save_metrics → stopper(epoch+1, fitness) / final_epoch → time-stop | CSV epoch — one-based; checkpoint epoch — zero-based. Stopper сохраняется уже после текущего решения |
| `(args.save or final_epoch) and save_model()` → `on_model_save` | Только rank -1/0; callback вызывается после successful write. `last` и AP-best уже записаны, final stripping ещё впереди |
| epoch-time/time-mode пересчёт epochs/scheduler → `on_fit_epoch_end` | Может уже отличаться args.epochs от записанного train_args при time mode. Потом memory cleanup, DDP stop broadcast, break/next epoch |
| после loop → `final_eval()` | Strip last; strip best с train_results из last; validate best, если он существует. Если best нет, last не заменяет best в final validation |
| final best validation → metrics.pop(fitness) → epoch временно +1 → `on_fit_epoch_end` → epoch обратно | **Дополнительный** вызов этого callback без нового save и без новой assigned self.fitness. Нельзя считать его ещё одним training epoch |
| plot_metrics → `on_train_end`; loader cleanup; train-finally `teardown` | on_train_end уже слишком поздно для копии pre-strip last/best. finally обеспечивает teardown, но не аварийный checkpoint |

`EarlyStopping` обновляет best_epoch при `fitness>best_fitness` (и специальном initial zero), поэтому равенство положительной fitness не продлевает patience. При этом `save_model` пишет best при `best_fitness==fitness`: tie может **перезаписать best** более поздними weights. Детекторный AP-best и epoch stopper не обязаны совпадать при ties.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f273"></a>

### F273 — last/best/periodic и предел защиты от прерывания

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S081](SOURCES.md#s081). **Исходные IDs:** W2-11-F02.

**W2-11-F02: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**CODE, S011/S081.** save_model один раз сериализует общий buffer: `last.pt` всегда; `best.pt` при equality текущего fitness с best; `epoch{self.epoch}.pt` при `save_period>0 and epoch % save_period==0`. Например `save_period=1` сохраняет epoch0, epoch1…; `save_period=5` — epoch0, epoch5… (это zero-based индекс, не «пятая законченная эпоха»). Periodic save находится **внутри** save_model: `save_period` не заменяет `save=True`. Штатный final_eval strips только last/best; periodic/callback copies остаются pre-strip, пока кто-либо явно их не обработает.

Time limit проверяется после optimizer step и после epoch validation; soft stop завершает путь validation/save, затем final_eval/strip. Это не hard wall-clock deadline: val/save/final val выходят за train cap. При time mode epoch estimate и scheduler пересоздаются после epoch. `save=False` опасен: early/time stop не обязательно final_epoch, поэтому последний soft stop может не записаться. Выбор `save=True` закрывает этот случай. Callback может выставить `trainer.stop=True` между batches; это partial epoch с последующей validation/save и индексом этого epoch. При resume штатный start_epoch будет **следующим** epoch: необработанный остаток partial epoch не воспроизводится.

Hard kill/KeyboardInterrupt/exception не имеют гарантированного вызова save_model/final_eval: остаётся лишь ранее завершённый save. `write_bytes` не является транзакционной atomic save; kill во время записи может повредить last. Нужны immutable copies и проверка reload/hash, а не только существование файла. Mid-epoch gradients и sampler cursor не сохраняются. NaN recovery/OOM retry могут менять фактический ход: их нужно сохранять в log, не считать normal continuation.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f274"></a>

### F274 — Реально сохранённое и точный смысл resume

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S012](SOURCES.md#s012), [S081](SOURCES.md#s081). **Исходные IDs:** W2-11-F03.

**W2-11-F03: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**CODE + INFERENCE, S011/S081/S012.** «Resume поддержан» и «восстановлена та же траектория» — разные свойства. Payload штатного pre-strip save:

| Поле / state | До strip | Restore / ограничение |
|---|---|---|
| epoch; best_fitness | zero-based epoch; текущий best | resume start_epoch=epoch+1; assert `0<start_epoch<epochs`. Это continuation незавершённого budget |
| model; ema; updates | `model=None`; deepcopy EMA → FP16 contiguous; EMA count | Online train weights отдельно **нет**. Setup стартует из EMA; _load_checkpoint_state восстанавливает EMA/count. Даже без random noise начало отличается от uninterrupted online model |
| optimizer | state_dict; часть floating state конвертирована FP16 | exp_avg/exp_avg_sq/square_avg/step исключены из FP16 conversion; например другие FP32 buffers могут потерять precision. Runtime fused берётся из новых groups, затем load_state_dict |
| scaler | scaler.state_dict | Загружается, если nonempty; recreated device/AMP context требует осмотра |
| stopper | только best_fitness и best_epoch | Fresh EarlyStopping берёт новый разрешённый patience; possible_stop первоначально False, восстановленные поля обновляют __dict__ |
| scheduler | **не сериализован** | `_setup_scheduler` строит LambdaLR из args; после resume last_epoch=start_epoch−1, следующий epoch вызывает step. Это реконструкция, не load scheduler.state_dict |
| RNG / loader / accumulation | **нет** Python/NumPy/torch/CUDA states, sampler cursor, worker/prefetch state, gradients, last_opt_step | Новый loader/setup; last_opt_step=-1; optimizer.zero_grad. Seed/deterministic args не восстанавливают consumed RNG stream |
| criterion | snapshot criterion=None | Создаётся заново; resume для one2one head явно init/update criterion с start_epoch. Не general сохранение произвольного loss state |
| modelopt | QAT state, если есть | Отдельный QAT restore; не доказательство generic export/resume совместимости |
| train_args/metrics/results/date/version/git/license/docs | provenance и CSV snapshot | Сохранять дополнительно реальные inputs/splits/settings/evaluator; metadata не заменяют bytes и runtime state |

Save также resyncs nonfinite EMA tensors из finite online tensor и применяет nan_to_num к snapshot после half conversion; поэтому даже EMA-live vs reloaded не следует объявлять byte-equivalent без проверки. Требуется reload acceptance test для **реального serialized candidate**.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f275"></a>

### F275 — Boolean resume может тихо стать новым training. CODE S164/S011. `YOLO(path).train(resume=True)` проверяет `self.ckpt.epoch>=0` и optimizer!=None. Если checkpoint…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S164](SOURCES.md#s164). **Исходные IDs:** W2-11-F04.

**W2-11-F04: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**F275 — Boolean resume может тихо стать новым training. CODE S164/S011.** `YOLO(path).train(resume=True)` проверяет `self.ckpt.epoch>=0` и optimizer!=None. Если checkpoint stripped, пишет warning и меняет resume=False: стартует новый training. Явный `.train(resume="path/to/prestrip.pt")` идёт через check_resume; недопустимый epoch затем вызывает assert. Поэтому считать режим по resolved args/log/start_epoch, а не по написанному `resume=True`. Для возобновления использовать explicit immutable path и preflight state; не `get_latest_run` fallback.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f276"></a>

### F276 — Freeze/unfreeze, args и новая стадия

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011). **Исходные IDs:** W2-11-F05.

**W2-11-F05: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**CODE S011; уточняет E004/E02 и Q014.** Полный whitelist U check_resume:

`imgsz, batch, device, close_mosaic, augmentations, save_period, workers, cache, patience, time, freeze, val, plots, channels_last, distill_model, save_dir`.

`data` обрабатывается отдельно: supplied data заменяет ckpt_args data. Остальные изменённые args (кроме исключённых служебных model/data/mode/resume/pretrained) дают warning и используют checkpoint values. В частности **epochs, optimizer, lr0, lrf, momentum, weight_decay, warmup_epochs, cos_lr, amp, seed** не разрешены этим whitelist. `project/name` не являются штатным способом перенести resume; `save_dir` разрешён. Не считать молчание на pretrained доказательством применения: setup_model игнорирует pretrained override при resume.

Freeze формируется заново в `_setup_train`: integer→range(N), list→явные индексы, плюс always `.dfl`, а для KD teacher_model. Совпавшие параметры получают requires_grad=False, прочие floating ранее frozen параметры **размораживаются**. Значит сохранённая ручная requires_grad mask не является контрактом следующего setup. `_model_train` каждую эпоху делает model.train(), потом frozen matching `BatchNorm2d` переводит eval; остальные BN работают train. Возврат unfreeze переводит их BN в train, если нет другой политики. DFL остаётся frozen и при freeze=0. Любая другая BN политика требует своего проверенного callback/custom trainer; отдельного штатного BN-policy flag эта ветка не установила.

`build_optimizer` перебирает все named parameters, без фильтра requires_grad. Поэтому штатный freeze→unfreeze при resume не обязательно ломает param-group размеры: ранее frozen params уже могли быть в groups, но без state до первого gradient. Их дальнейший update с новым gradient и старым optimizer/state остальных — **смешанная история**, а не fresh low-LR stage2. Это code-supported possibility, не runtime гарантия для изменённой топологии/KD/QAT. Менять masks после optimizer creation вручную здесь не предлагается.

Минимальный операционный выбор:

| Намерение | Штатный интерфейс U / смысл |
|---|---|
| Продолжить прерванный recipe | Новый процесс; explicit resume path к pre-strip file; те же data/teacher hashes, freeze, batch/geometry и допустимые overrides без изменения recipe. Проверить start_epoch и загруженный optimizer/scaler/EMA/stopper. Это штатный resume с указанными F274 ограничениями |
| Новая stage2: unfreeze + новый LR/optimizer/budget | `YOLO(selected_weights).train(resume=False, data=..., freeze=0, optimizer=..., lr0=..., epochs=..., project=..., name=...)`; значения символические/выбираются до trial. Новый optimizer/scaler/EMA/stopper/scheduler/epoch0/warmup; **warm start** из выбранной EMA, а не resume |
| Намеренно unfreeze в прежнем run | resume с `freeze=0` разрешён, но optimizer/LR и budget наследуются; записать intervention и проверить masks/BN/groups после setup. Не применять как замену строке stage2 выше |

Для supervised stage2 брать проверенный student-only **отдельный** artifact. Можно сделать производную stripped копию через штатный `strip_optimizer(f=immutable_prestrip, s=distinct_student_path)`; источник остаётся нетронутым. Не fuse перед будущим training. `distill_model=None` в новом supervised run задавать явно, иначе train_args старого KD могут повторно включить distillation. Для новой KD стадии — явно та же/новая teacher admission и отдельная provenance.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f277"></a>

### F277 — Candidate objective без изменения trainer

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S011](SOURCES.md#s011), [S164](SOURCES.md#s164), [S216](SOURCES.md#s216), [S217](SOURCES.md#s217). **Исходные IDs:** W2-11-F06.

**W2-11-F06: условия/наблюдение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):

**PROPOSED INTERFACE на S011/S164/S216/S217, не готовый evaluator.** Для сохранения по event/critical-class constraints custom trainer **не обязателен**: штатный `model.add_callback("on_model_save", callback)` даёт trainer после validation/write, пока checkpoint ещё pre-strip. Достаточный интерфейс callback:

1. На rank -1/0 скопировать `trainer.last` в уникальный `candidate_epoch{trainer.epoch}_{hash}.pt` **синхронно до возврата**, записать hash/epoch/EMA source и args/data/class/split/evaluator manifests. Never overwrite accepted candidate. Базовые настройки `save=True, val=True, save_period=1` страхуют каждый завершённый save; storage budget назначить отдельно. При недостатке места save_period=1 можно заменить callback-only архивом, сохранив every-epoch copy policy.
2. Внешний evaluator принимает **path/hash** immutable serialized candidate, val episode manifest, preprocessing/decoding/NMS/threshold policy, event-rule version и returns per-class/events/exposure metrics + constraint status + support. EMA deepcopy snapshot в памяти допустим как дополнительный diagnostic reference, но selection итогового artifact проверять после его reload.
3. При дорогой event evaluation можно ставить immutable paths в отдельную очередь; копировать нужно сразу, а оценивать позже. Это не реализованный async service. Pipeline обязан дождаться решения по нужным candidates, иначе финальное best по AP не заменяет отсутствующий event result. Lockbox не участвует.
4. Сохранять constrained winner как bundle с model hash, rules/thresholds и metric evidence, отдельно от `best.pt`. Сначала eligibility по constraints, затем заранее заданная utility/tie policy; AP stop/fitness остаются штатными. `patience=0` штатно отключает AP early-stop, если иной stopping contract требует этого; time cap остаётся независимым. Своё bounded stop допускает callback `trainer.stop=True`, с оговоркой partial epoch F273.

`on_fit_epoch_end` также после save, но final_eval вызывает его ещё раз; именно `on_model_save` проще исключает финальный дубль. `on_train_epoch_end` слишком рано для текущей val fitness, `on_train_end` слишком поздно для pre-strip copy. Validator callbacks доступны, но `on_val_end` ещё до BaseTrainer.validate присвоения self.fitness; не следует рассчитывать, что изменение trainer.fitness там перепишет корректно весь selection.

Если команда хочет **заменить** встроенный fitness/AP-best/stopper своей event objective, а не вести внешний winner, требуется reviewed custom validator/trainer integration, возвращающая fitness до validate/stop/save. Одного `on_model_save` для этого недостаточно. Такой port не выполнен и для минимальной схемы не требуется. Callbacks/внешняя очередь/selector сами не сериализуются как их runtime progress: хранить selection ledger отдельно и регистрировать callbacks заново в новом process. Local runtime hooks на EMA могут сломать pickle; использовать обычную immutable disk copy, не навешивать на неё локальные hooks.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.


## W2-12 — W2-12 — Ограниченная условная очередь trials и срок полезности артефакта

<a id="f278"></a>

### F278 — [PAPER, S218]. Hyperband распределяет заранее определённый resource между конфигурациями через несколько brackets с разной агрессивностью отсева. В §5.2 loss…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S218](SOURCES.md#s218). **Исходные IDs:** W2-12-F01.

**W2-12-F01: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F278 [PAPER, S218].** Hyperband распределяет заранее определённый resource между конфигурациями через несколько brackets с разной агрессивностью отсева. В §5.2 loss sequence каждого arm имеет предел, terminal losses — bounded i.i.d.; guarantees связаны также с бюджетом и скоростью сближения к пределу. Fig.2/§3.7 объясняют, почему близкие terminal values или медленное сближение требуют больше resource. Здесь нет требования монотонного loss каждой конфигурации и нет гарантии сохранения любого раннего ranking до конца нашего detector training.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f279"></a>

### F279 — [PAPER, S219]. ASHA сравнивает конфигурации на resource rungs и убирает ожидание синхронных promotions. §3.3 прямо допускает ошибочные promotions относительно…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S219](SOURCES.md#s219). **Исходные IDs:** W2-12-F02.

**W2-12-F02: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F279 [PAPER, S219].** ASHA сравнивает конфигурации на resource rungs и убирает ожидание синхронных promotions. §3.3 прямо допускает ошибочные promotions относительно итогового состава того же rung; обсуждение малой доли ошибок опирается на рост числа конфигураций. Это отдельная проблема от перестановки ranking между ранним и финальным resource. Возможность checkpoint/resume используется при рассуждении об iterative training; она не устанавливает fidelity или exact continuation конкретного trainer. Published systems/benchmark results не задают скорость/качество нашей очереди.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f280"></a>

### F280 — [INFERENCE, S218, S219, S220, S220]. Для текущего кейса корректность короткого run и его способность ранжировать финальные candidates — разные допуска. Полезный…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S218](SOURCES.md#s218), [S219](SOURCES.md#s219), [S220](SOURCES.md#s220). **Исходные IDs:** W2-12-F03.

**W2-12-F03: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F280 [INFERENCE, S218, S219, S220, S220].** Для текущего кейса корректность короткого run и его способность ранжировать финальные candidates — разные допуска. Полезный smoke подтверждает labels/update/save/reload/export interface. Он не позволяет kill по низкому раннему AP, если late phases/critical support ещё не представлены. Особенно нельзя автоматически отбрасывать «slow starter», сравнивать teacher AP со student AP или N/A critical recall с нулём. При отсутствии проверенного proxy выбрать обычное причинное A/B сравнение с заранее заданным полным целевым recipe и остановкой по реальной стоимости/некорректности; outcome может быть inconclusive.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f281"></a>

### F281 — [CODE-BASED INTERNAL TRANSFER, /F282/F283; –F282]. В U уменьшение заданных epochs может менять не только resource: `optimizer=auto` выбирает AdamW либо MuSGD по…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-12-F04.

**W2-12-F04: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F281 [CODE-BASED INTERNAL TRANSFER, F149/F282/F283; F274, F275, F276].** В U уменьшение заданных epochs может менять не только resource: `optimizer=auto` выбирает AdamW либо MuSGD по `ceil(N/max(B,nbs))*E`; warmup ограничен E−1; scheduler зависит E; при E≤close_mosaic сильные mix transforms закрываются с начала. Уменьшение dataset fraction меняет composition, updates и эту же auto эвристику. Early stop может не дойти до запланированной augmentation phase. Малое разрешение/crops меняют доступный сигнал, а не просто ускоряют тот же опыт. Поэтому отдельный short-recipe run не считать prefix полного run.

Continuation тоже не нейтральна: W2-11 уточнил W1 — штатный pre-strip payload сохраняет EMA вместо online weights, optimizer/scaler/часть stopper, но не scheduler/RNG/loader/accumulated gradients; scheduler реконструируется. Final stripped file ещё беднее. Explicit resume не является bitwise continuation. `freeze` допустим как resume override на U, а LR/optimizer/epochs — нет; новая stage2 с новым LR — явно новый run/warm start, включая fresh optimizer/EMA/warmup и проверку BN. Для fidelity критичны фактические trajectory/state, а не одинаковые имена args.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f282"></a>

### F282 — [PROPOSED POLICY, из S220/S220]. Gate результат переиспользуется только для того же contract key: task/class order + data/coverage/split revision +…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S220](SOURCES.md#s220). **Исходные IDs:** W2-12-F05.

**W2-12-F05: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F282 [PROPOSED POLICY, из S220/S220].** Gate результат переиспользуется только для того же contract key: task/class order + data/coverage/split revision + code/package/dependencies + architecture/head/input/preprocess + save/extract/export/SDK path. Изменение labels требует повторить affected loader/coverage gate; новый loss — update/partial tests; новый input/head/topology — reload/export/target; новый teacher — admission/KD checks. Не надо заново запускать все gates или quality trials при любой правке. Неизменный compiler path не доказывает quality новых weights: финальный serialized artifact всё равно проходит parity/GT/actual-target проверку.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f283"></a>

### F283 — [INTERNAL SYNTHESIS, S220; policy PROPOSED]. Ни наличие public repo, ни priority K-ID не резервируют trial. Ветвь становится ready, только если prerequisites уже…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** [S220](SOURCES.md#s220). **Исходные IDs:** W2-12-F06.

**W2-12-F06: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F283 [INTERNAL SYNTHESIS, S220; policy PROPOSED].** Ни наличие public repo, ни priority K-ID не резервируют trial. Ветвь становится ready, только если prerequisites уже доступны, она меняет unresolved decision и полный artifact path помещается по правилу следующего раздела.

| Альтернатива | Условия ready и один useful comparison | Новое ограничение W2; kill/fallback |
|---|---|---|
| AL selector | Значима цена отбора; pool/QA/independent dev готовы; E022 interface/cost pilot допускает E022: один selected low-confidence+metadata arm против stratified random при равных **полных** person-minutes | `Results.boxes.xyxy/conf/cls` доступны на U; `probs` не class entropy detect. No-box/error/cap records и exploration обязательны для заявленной policy. Не нужны обязательные embeddings/ensemble. Дороже без useful gain→random/targeted; training exposure учесть. |
| Online SSL | U добавляет независимое разнообразие, audit покрывает dropped/no-proposal positives, exact compatible runnable route и выбранная inference branch прошли smoke/extraction | W2-03: ET SHA `64165e24a30cd6dc1dd893cc861c1feab0a536ee` — legacy YOLOv5 route, не U YOLO11 flag. UTv2 FCOS меняет regression head, std остаётся в Python eval, default выбирает teacher. Ordinary corrected supervised — rollback. E026 vs supervised; teacher/student/secondary EMA identities раздельны. |
| Source-free | Source unavailable, adaptation разрешён, compatible Faster R-CNN source checkpoint/lock, independent target V labels, BN/eval и ordinary export действительно отделены | W2-07 P=`ee24594869bde0069947540275a28eebb3d4a540`: AdaBN→fixed pseudo JSON→training, eval entrypoint может обновлять BN; source/GT hooks исключить. E020/E020 дополняют один trial; frozen+small corrected supervised — альтернатива. Нет V→только correctness/audit, quality не выбирать по confidence. |
| KD | Compact native student не достигает quality, target-trained teacher уже есть и закрывает нужный error slice; same-family grids/head/admission/save/extract прошли | W2-01: YOLO11n←YOLO11s code/doc-supported; wheel 8.4.184 проверен по bytes, installation/runtime нет. Wheel SHA256 `d04c80f27d335fe27a057dcf00f91c843b11f99d21e7b3017616959a523bfc8a`; U не release SHA. Different nc не обязательно tensor failure: max class score не remap semantics. Teacher/constructor/preparation time входят в цену. E027 supervised vs KD, E028 reused final extraction gate. Нет teacher→не запускать его обучение автоматически. |
| Synthetic | Выявлен конкретный visual coverage gap; разрешённые assets/labels, fully reviewed whole synthetic frames, real independent dev, стоимость review приемлема | W2-08: Gen2Det author implementation не установлен, ordinary merge не воспроизводит background-ignore. E030→E02, один тип synthetic vs real-only. Equal updates при replacement не даёт одновременно equal real exposure: записать draw ledger; дополнительный control только если ambiguity меняет решение. Broken state/partial labels→real annotation. |
| Scale/cascade | Native evidence есть, input теряет детали; feasible input/calls/memory contract; inference-only проба сначала | E016 либо E03 по вопросу; predicted crops с upstream misses, не oracle-only quality. E018 только после полезной geometry. Cost/coverage ceiling нарушен→прекратить scale ветку. |
| QAT | FP parity пройдена; PTQ/calibration E038 оставляет значимую loss; actual SDK принимает выбранную arithmetic/QDQ/fusion/head, dependency lock совпадает | W2-09 NVIDIA YOLOv7 route SHA `e9b75770ea58713d1cb3902d67c36e11acb888d7` использует **feature reconstruction MSE без detector GT loss**, не supervised PPE fine-tuning. Toolkit historical lock неполон. E049 различает quant-disabled reconstruction и supervised matched-label/updates controls. Не менять family на YOLOv7 ради sample; target mismatch→штатный SDK/PTQ/другой student. |
| Physical pruning | Native smaller student не удовлетворяет quality+actual-target cost; larger модель model-compute-bound; готов pinned old route и новые dense shapes compiler принимает | W2-10: TP v1.6.1 T=`e80127d7c6935c319a7dd6719b8a72e3c1fcbff9`, U-old=`44c7c3514d87a5e05cfb14dba5a3eeb6eb860e70` (8.0.90). C2f_v2+patched trainer/full-object serialization, original YAML+state_dict не восстанавливает topology. Clean reload/import custom class и conversion-only/export smoke **до recovery**. Demo last rejected stage не экспортировать; rollback accepted stage. P2 резерв, не переносить script на U 8.4.184/YOLO11 без отдельного port. |

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

<a id="f284"></a>

### F284 — [PROPOSED POLICY; /E051, E02, E03, E04, E05]. Единица очереди — карточка решения, а не свободная GPU. Карточка содержит hypothesis/две различимые причины, parent…

**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.

**S/locator:** S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение. **Исходные IDs:** W2-12-F07.

**W2-12-F07: условия/наблюдение** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):

**F284 [PROPOSED POLICY; F179/E051, E02, E03, E04, E05].** Единица очереди — карточка решения, а не свободная GPU. Карточка содержит hypothesis/две различимые причины, parent bundle, один intervention, reused gates с contract keys, unresolved dependencies, owner/reviewer, output schema/status, заранее acceptance/kill rule и предельную стоимость. Бюджет назначается по actual pilot и оставшемуся пути до потребителя, не из названия RTX 4070 и не из defaults paper. Нет численного budget — допустим bounded correctness pilot с явно записанным условием завершения/ресурсным headroom, но не неограниченный quality sweep.

| Статья | Что реально измерить | Ответственный bottleneck |
|---|---|---|
| T_setup | Получение weights/lock/data, transfer/cache build, teacher preparation, custom head/loader/SDK setup, cold startup | model_stack/training; для SDK — platform owner |
| T_train | Actual successful optimizer updates, images/source draws, microbatch/accumulation/precision, stalls/retries, GPU allocated time и peak memory | training owner; E040 profiler лишь для причины, throughput без profiler |
| T_validate | Forward + decode/matching + event evaluator + per-group/support aggregation, не только console speed | evaluation owner; очередь review может доминировать |
| T_save | Immutable serialization/copy/checksum/transfer, reload smoke, artifact availability timestamp | training/artifact owner; W2-11 callback/save ledger |
| T_export | Export, checker/parity, quant/calibration, compile/upload/run, placement и GT quality; каждую стадию отдельно | model_stack + linq_platform/video_architecture |
| T_decision | Human review, разбор критичных regression/support, выбор branch, передача интеграции | Назначенный принимающий решение + evaluation |
| H_selection/H_annotation/H_review/H_integration | Person-minutes каждой операции, включая поиск misses/no-box, QA/adjudication/export import, code/debug/SDK review; parallel people sum person-minutes отдельно от wall-clock | datasets/annotators, затем integration owner; пять участников не означают пять доступных reviewers |

Хранить timestamps и dependency DAG. `T_ready = T_queue + T_setup + T_train + T_validate + T_save + T_export + T_decision` — accounting для последовательного пути; перекрывающиеся стадии не суммировать дважды. Для готовых данных/compiled graph соответствующий setup может быть reused, но актуальность проверяется contract key. GPU-hours — сумма фактических оплачиваемых/занятых GPU intervals; independent trials и DDP считают одинаковую границу. Idle/setup/failure не исчезают из стоимости. Цены аренды, VRAM/ОС training-машины и реальные latency здесь неизвестны.

Обозначим `D_useful` фактический срок, к которому принимающий integration owner ещё может использовать результат; он определяется реальным downstream process/кейcом. `CP_remaining(j)` — измеренная или явно интервальная оценка **всего** оставшегося пути trial j→validation→save/reload→export/target→review→integration/smoke. Правило допуска: `now + CP_remaining(j) <= D_useful`, dependencies обеспечены, у узких специалистов есть место и риск ожидания/повтора отражён в оценке. Если длительность unknown, первый useful task — измерить этот узкий gate, а не объявить, что длинный run помещается. Для последовательного участка latest-start=`D_useful−CP_remaining`; это символический расчёт, не фиксированный часовой timetable и не probabilistic guarantee.

Если результат приходит позже, branch не запускается либо заканчивается текущим безопасным save с конкретным статусом. Уже прошедший bundle передаётся независимо от незавершённой идеи. После freeze новые candidates должны заново успевать пройти тот же путь; занятая GPU не оправдывает продолжение. Параллелить можно независимые **разные решения** при готовых prerequisites и свободных review/SDK/annotation ресурсах. Нельзя параллелить зависимый KD до проверки teacher, recovery до reload/export smoke или confirmation по ещё меняющемуся evaluator.

**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.

## Дополнительные карты решений, metadata contracts и восемь сценариев

Ниже — явно предложенные схемы/синтез веток, не новые измерения. Содержательные матрицы сохранены, чтобы F-база не теряла operational contracts между отдельными наблюдениями.

### W1-01: решение и контракты

#### Матрица ситуация → наблюдение → интервенция → проверка

Все строки — условные рекомендации **INFERENCE/PROPOSED**, не подтверждённые на целевых данных.

| Ситуация | Нужное наблюдение | Следующая интервенция | Проверка и предел |
|---|---|---|---|
| Только открытые данные и готовые веса | Есть ли нужный class/output contract; сходны ли ракурс и масштаб | Сохранить zero-update reference; проверить pipeline; запросить/разметить target audit | Open-source validation характеризует source; достаточность на target пока неизвестна |
| Есть немного target labels | Они полны для нужных классов? Независимы ли сцены? Какие ошибки повторяются? | Сначала audit mapping/coverage, затем небольшой controlled fine-tuning против unchanged baseline | Одинаковые target validation, preprocessing, rules; новый camera split при доступности |
| Есть только target video без labels | Есть ли разрешение на его adaptation; какие условия и события представлены | Выделить непересекающиеся adaptation/assessment группы; разметить диагностическую порцию | Без проверенного GT нельзя измерить target AP/recall или доказать пользу pseudo-labels |
| Labels неоднородны, много «FP» | Человек подтверждает missing annotation или иное правило labeling | Исправить policy и спорную разметку; сохранить версии до/после | Не штрафовать модель за незамеченные GT; оценивать обе модели на одинаковом исправленном наборе |
| Boxes/classes верны, тревога ошибочна | Связь person/PPE, зона, длительность, track ID или дедупликация неверны | Исправить соответствующее event/association rule | E002 с вручную проверенным evidence; не требовать нового detector training по умолчанию |
| Объект пропадает после resize | В исходнике различим, на actual input теряет признаки | Контролируемое разрешение/crop experiment, затем при необходимости обучение под тот input | Сравнить object/event quality и число inference calls; LinQ feasibility отдельно |
| Веса не содержат новый класс | Class map действительно не кодирует нужный смысл | Найти подходящие веса или подготовить полную разметку и изменить predictor/training | Confidence threshold не создаёт отсутствующий класс; экспорт изменённого graph вновь проверяется |
| Частый фон путается с классом | FP повторяются на независимых проверенных негативных сценах | Целевая доразметка hard negatives либо focused data change | Проверить, не потерян ли recall редких позитивов; не набирать лишь соседние повторения |
| Ошибки одной камеры/смены | Согласованные labels, та же pipeline, отличия видимости/домена | Представительные target examples; ограниченное supervised adaptation как кандидат | Сохранить оценку других камер и базовых классов; улучшение одной не гарантирует общего |
| Неясен визуальный сигнал | Спор сохраняется при исходном кадре и времени, человеческие решения расходятся | Уточнить определение события, abstention/unknown или нужный обзор камеры | Не объявлять отсутствие видимого объекта доказанным отсутствием объекта |
| Готовые веса проходят требования | Пройден независимый target protocol и интеграционный путь | Сохранить рабочий кандидат; следующий прогон только под конкретную оставшуюся ошибку | Приёмка включает target runtime и event failures; это не пожизненная гарантия |
| FP-модель хороша, после export хуже | Разница воспроизводится на тех же input/predictions | Проверить geometry/numerics/output parsing, затем компрессию | Переобучение до локализации export loss может исправлять неверную причину |

### W1-02: решение и контракты

#### Решение команды

**Нет основания заранее назначить head-only универсальным победителем для малого CCTV-набора.** TFA даёт сильное detection-specific основание проверить обучение последних предикторов на сбалансированной малой разметке после обучения детектора на базовых классах. Оно не доказывает, что любой YOLO с замороженным backbone получит тот же эффект. Полное обучение и частичная адаптация должны сравниваться на одном checkpoint, одинаковой разметке и независимой проверке, с явно зафиксированным поведением BN. При этом «число обучаемых весов» и «какие статистики меняются» — разные характеристики режима.

Для короткого исследовательского цикла практически полезны три кандидата: неизменённые веса как reference; ограниченный fine-tuning с проверенной маской; полный fine-tuning из тех же исходных весов. Последовательность freeze→unfreeze — отдельный кандидат, требующий отдельного бюджета и контроля, а не автоматически лучший рецепт. Выбор модели сначала ограничивается нужными outputs и возможным целевым graph; обучение не подтверждает исполнение на LinQ.

Ни обучение, ни модельный benchmark, ни export здесь не запускались. Выполнены веб-поиск, открытие материалов, HTTP-чтение закреплённых исходников и metadata API. Скорость/память RTX 4070, качество на target CCTV и поддержка LinQ не установлены.

#### Условная стратегия [INFERENCE/PROPOSED из F008, F009, F010, F011, F012, F013, F014, F015, F016, F017, F018, F019]

| Наблюдение | Кандидат и основание | Что может опровергнуть выбор |
|---|---|---|
| Мало полных labels; нужные признаки уже дают полезные boxes | Ограничить trainable predictor/head; быстро проверить сохранение representation | Нет улучшения на независимых сценах; систематические FN в условиях новой камеры остаются |
| Изменились ракурс, освещение, texture; signal различим | Сравнить full или ограниченное unfreeze с frozen вариантом; feature adaptation может требоваться | Full улучшает train, ухудшает целевые val/старые условия; небольшая выборка не позволяет различить результаты |
| Добавляются классы и старые всё ещё нужны | Явный class map, перенос совместимых весов; при доступности включить корректно размеченные старые классы; отдельные base/novel metrics | Общий AP растёт за счёт новых, а обязательный старый класс теряет recall |
| Имена source/target различаются, nc совпадает | Проверить семантику и фактически перенесённые rows; shape success не гарантирует class correctness | Overlays/row audit выявляют неверный порядок или ложный semantic alias |
| Training VRAM ограничивает input resolution | Проверить frozen режим как способ уменьшить gradient storage; измерить actual peak memory | Forward/activation/input остаются узким местом; размер head-only не обещает нужный batch/скорость |
| Target labels достаточно, есть заметное время и плохой pretrained candidate | Scratch может быть контролем после рабочих transfer candidates | Недостаточное время сходимости; исходные статьи не дают порога числа кадров для CCTV |

Термин head-only должен сопровождаться точным перечнем модулей. В TFA это последние box predictors; в YOLO это может быть весь Detect со своими feature transforms, box/cls и one-to-one ветками. Freeze backbone обычно оставляет neck+head, то есть не равен TFA. Full fine-tuning также не означает буквально каждый tensor trainable: у конкретной реализации есть fixed components вроде DFL. Сравнивать надо реальные маски.

Для выборки из видео количество соседних кадров не заменяет независимость сцен. Разбиение camera/session/time, полный task ontology и zero-update baseline уже разобраны в W1/01_BASELINE.md; здесь они только входной контракт эксперимента. Ошибка association/event rule не становится причиной full fine-tuning без локализации object error.

### W1-03: решение и контракты

#### Что меняет практический выбор

1. TFA считает K-shot в аннотированных **экземплярах каждого класса**, а не в кадрах. В видео дополнительно нужно считать независимые эпизоды/траектории/камеры. Один человек в десяти соседних кадрах не даёт десять независимых условий переноса (F020, F009, F008, F021).
2. Новый класс и новая камера — разные изменения. TFA исследует base/novel class protocol с богатой base-подготовкой; он не устанавливает, что любой детектор респираторов переносится на новую камеру после десяти boxes (F020, F009, F008).
3. Неразмеченный объект не является подтверждённым фоном. Маска классификационных классов, маска пространственных регионов и исключение полностью unlabeled images — разные интерфейсы. Исправление только одного loss не доказывает исправление objectness/RPN/assignment всего детектора (F022, F023, F024, F025, F026).
4. Federated Loss уменьшает множество участвующих в classification loss классов. Он не находит пропущенные boxes. В проверенной реализации Detic нет аргумента с spatial ignore regions в `sigmoid_cross_entropy_loss`; background RoI получает нули для выбранных foreground classes (F024, F025).
5. Нельзя автоматически обещать неизменный inference после sparse training: Co-mining описывает одну branch при inference; SparseDet использует C-RPN и в основном режиме обе views даже при inference. Его абляция без augmentation сохраняет C-RPN (F027, F028, F029).

### W1-04: решение и контракты

#### Решение, которое меняет эта ветка

Сначала нужно установить единицу редкости: изображения, экземпляры, независимые события, камеры/условия либо положительные и отрицательные элементы loss. Только затем выбирать вмешательство. Для небольшого CCTV-набора первый кандидат — контролируемое изменение состава данных или умеренный sampling при сохранении репрезентативной проверки; универсально заменять loss на focal оснований нет. Ошибки на конкретных похожих предметах дают основание для проверенных hard negatives. Повторы одного нарушения не компенсируют отсутствие других людей, камер, освещения или способов ношения СИЗ. Это наши выводы F044, F045, F046, F047, а не опубликованные измерения на промышленном видео.

Существенная актуальная находка: в прочитанном Ultralytics **8.4.184**, commit **e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8**, есть `cls_pw` для class weighting; утверждение, что такого механизма нет вообще, неверно для этой версии. Его применимость к выбранному командой checkpoint и установленной версии ещё нужно проверить. Сам класс `FocalLoss` присутствует в файле, но прочитанный `v8DetectionLoss` использует BCE. Distribution Focal Loss для координат не следует путать с focal classification loss.

#### Причина → возможное вмешательство → обязательный контроль

Следующая таблица — **наша условная стратегия**, опирающаяся на F033, F034, F035, F036, F037, F038, F039, F040, F041, F042, F043; это не результат эксперимента.

| Наблюдение | Что сначала проверить | Разумное вмешательство | Чем можно опровергнуть пользу |
|---|---|---|---|
| Редкий класс есть только в немногих кадрах | Есть ли независимые сцены и корректные полные labels; объект различим при рабочем разрешении? | Добыть разнообразные реальные примеры; затем ограниченный image/group sampling | Выигрыш только на знакомой сцене; ухудшение held-out камер; FP растут |
| Мало изображений, много объектов на каждом | Раздельные image count и instance count | Сравнить image-frequency sampling с instance-frequency weighting | Перевзвешивание усиливает шум плотных сцен; редкий класс вне них не улучшается |
| Одно длинное нарушение даёт тысячи кадров | Связать кадры с episode/track/session; найти near-duplicates | Ограничить вклад группы; отбирать различные фазы/ракурсы | Число уникальных событий неизменно, validation по соседним кадрам завышен |
| Поток почти всегда нормальный | Реальная prevalence, длительность normal footage и типы ложных тревог | Обучение можно обогатить позитивами; operating point выбирать на реальном normal/positive материале | Хороший AP на искусственно сбалансированных кадрах не выдерживает FP/hour |
| Повторяющиеся FP на похожем фоне/предмете | Это настоящий negative или пропущенный/неразличимый positive? | Размеченные трудные негативы с dedup и сохранением позитивов | Снижение FP на mining-пуле не переносится на другой negative-пул; падает recall |
| Loss доминируют лёгкие background locations | Какая assignment/loss реально используется | Focal/OHEM только в поддержанной архитектуре как отдельная абляция | Нет выигрыша в paired comparison либо высокие веса уходят в ошибки labels |
| Редкие категории подавлены межклассовым обучением | Градиенты/ошибки по классам, а не одна гистограмма | Class weighting; при обосновании специализированный long-tail loss | Общее качество/частые классы или false alarms выходят за согласованный предел |
| Класс имеет ноль положительных annotations | Семантика и доступность визуального сигнала | Собрать/разметить positive, изменить scope по правилам кейса | Sampling/reweighting не создаёт отсутствующий положительный пример |

### W1-05: решение и контракты

#### Решение команды

Выбирать аугментации по наблюдаемому дефекту камеры и смыслу разметки. Для CCTV первыми кандидатами являются умеренные вариации экспозиции/контраста, компрессии и размытия, если именно такие дефекты есть в train/рабочем потоке. Геометрия, mosaic, mixup, occlusion и copy-paste требуют отдельного решения по классам. Сохранение bbox математически не гарантирует сохранения значения «каска надета», «респиратор снят», «человек в зоне» или «курение». Рецепт по умолчанию Ultralytics — доступный контроль, но не установленный оптимум для нашего кейса.

Наиболее практические ограничения реализации: `copy_paste` не действует на обычные bbox-only labels без segments; `erasing`/`auto_augment` относятся к classification; default JPEG-like compression в дополнительном Albumentations pipeline выключена; `close_mosaic` закрывает четыре mix-операции; `rect` меняет реально применяемые probabilities. Современный сайт Albumentations и архивная библиотека 2.0.8 имеют разные имена аргументов. Ни совместимость среды, ни качество на CCTV, ни исполнение на LinQ этим чтением не подтверждены.

#### Физика и label semantics: условия допуска преобразований

Следующие F066, F067, F068, F069, F070, F071 — наши проектные выводы/гипотезы из постановки и F050, F051, F052, F053, F054, F055, F056, F057, F058, F059, F060, F061, F062, F063, F064, F065. Они не являются опубликованными результатами PPE-experiments.

| ID / группа | Когда есть смысл пробовать | Семантический gate и риск |
|---|---|---|

### W1-06: решение и контракты

#### Решение для команды

Сначала установить, теряет ли pipeline уже имеющиеся в исходном кадре детали при уменьшении изображения. Если да, сравнить увеличение входа, tiles и person/head crops на одинаковой полной разметке кадров. Если отличительный признак неразличим уже в исходном видео, resize сам по себе не доказывает его восстановление: нужна другая камера/ракурс, иной признак события или честное состояние «не наблюдается». Число эпох не исправляет отсутствие доказательного визуального сигнала. Это вывод о проверяемой постановке, а не установленный предел конкретного CCTV.

SAHI — доступная реализация гипотезы сохранения масштаба. Публикационные gains получены на aerial detection; они не гарантируют gain для респиратора/сигареты и не устанавливают совместимость LinQ. Person/head cascade имеет дополнительный предел: пропуск или плохая локализация первого stage исключают правильный crop; качество второго stage на oracle crops не равно качеству системы.

### W1-07: решение и контракты

#### Решение для команды

**Наш вывод:** начать с проверки исходного детектора по камерам и сессиям. Если есть проверенная целевая разметка, первой проверкой сделать обычное target fine-tuning против source+target mixing. Если есть только целевое видео, отделить режим с доступным source от source-free: у них разные входы и реализации. Сложный domain-adaptive trainer оправдан после проверки таксономии, teacher errors и стоимости интеграции. Ни одна просмотренная работа не устанавливает выигрыш на PPE/промышленном CCTV, конкретном YOLO либо исполнимость на LinQ.

Под domain shift здесь понимается изменение изображения и условий наблюдения: ракурс, освещение, компрессия, размер объекта, фон, плотность людей. Отличие смысла labels — например, «каска» против «правильно надета каска» — нельзя автоматически устранить выравниванием признаков. Наличие нужного визуального сигнала и class-map является отдельным условием.

#### Условная карта source/target

Это **proposed / inference**, основанное на различии постановок F083, F084, F085, F086, F087, F088, F089, F090. «Source доступен» означает право и техническую возможность читать изображения с корректными annotations; наличие checkpoint само по себе недостаточно.

| Реальные входы | Первый полезный маршрут | Следующая ветка при положительном gate | Что запрещено считать доказанным |
|---|---|---|---|
| Нет target images; есть source или готовые weights | Source-only baseline; целевые условия пока только гипотезы | Собрать независимый camera/session audit после выдачи данных | Domain adaptation уже выполнена; robustness на новой камере |
| Target labels есть, source доступен | Target-only fine-tuning против mixing; одинаковый стартовый checkpoint | Менять sampling source/target только по validation; проверить forgetting на old domains | Больше source всегда полезнее; общий mAP заменяет camera/class slices |
| Target labels есть, source недоступен | Target fine-tuning с сохранением frozen исходного кандидата | Distillation/replay-free regularization только при отдельной реализации и gate | Возможно измерить source forgetting без source/old-domain holdout |
| Target labels нет, source доступен | Аудит frozen detector и небольшая target разметка для измерения; adaptation pool отдельно | UDA teacher/student либо audited offline pseudo-labeling, если trainer реально поддержан | Unlabeled target можно загрузить как обычные полностью отрицательные изображения |
| Target labels нет, source недоступен, source weights доступны | Frozen baseline; ручная выборочная проверка target ошибок | Source-free self-training как рискованная отдельная ветка | AT без source является тем же алгоритмом; entropy доказывает качество |
| Нет target labels и нельзя создать независимые labels даже для проверки | Можно исследовать доступность/покрытие prediction и сохранять frozen fallback | Только предварительная демонстрация, с явно непроверенным quality improvement | Доказано улучшение recall, безопасность или снижение FP |

Если новый target содержит отсутствующий в head класс, это прежде всего supervised class extension / другая модель. Closed-set domain adaptation не даёт новой семантики из отсутствующего сигнала. Если источники различаются полнотой разметки, class-map и exhaustive/partial status проверяются до смешивания; иначе background loss может наказывать реальные неразмеченные объекты. Детальный loader/partial-label путь передаётся W1-03/model_stack.

### W1-08: решение и контракты

#### Решение, которое меняет ветка

Начальный практический кандидат — короткий цикл качественной доразметки с random-контролем, ограничением повторов одной сцены и отдельным бюджетом проверки labels. Сложный AL selector допускается только после сравнения с простой стратифицированной случайной выборкой и осмысленным ручным отбором при одинаковых **человеко-минутах**. Победитель заранее неизвестен. Active Teacher полезен как источник конкретной гипотезы, но его COCO/SSOD-результат не определяет готовый рецепт CCTV/YOLO.

Предлагаемый выбор данных разделяет четыре задачи: поиск уверенных пропусков через случайный аудит; поиск пограничных предсказаний через uncertainty/disagreement; покрытие камер/сессий/масштабов через diversity; устранение дублей через временные группы. Низкий confidence сам по себе не означает полезный обучающий пример. Пропуск объекта вообще может не породить box, пригодный для вычисления uncertainty. Это вывод по структуре методов, а не проведённый эксперимент.

### W1-09: решение и контракты

#### Решение для команды

При наличии целевого неразмеченного видео первым кандидатом считаю **offline-предразметку с полным ручным исправлением небольших независимых порций**. Это предложенный инженерный маршрут, а не доказанный выигрыш на нашем кейсе. До массового принятия автоматических boxes нужен аудит учителя, включающий объекты, которых учитель вообще не предложил. При слабом редком классе сначала разметить его реальные примеры; высокий глобальный confidence threshold может оставить этот класс без обучения.

Online Soft Teacher / Unbiased Teacher — отдельные реализации обучения, а не название операции «сгенерировать labels и вызвать train». Их стоит пробовать только после работающего supervised baseline, независимого validation и подтверждения поддержки нужной архитектуры. Наличие Faster R-CNN/FCOS реализации не устанавливает поддержку выбранного YOLO, Ultralytics или LinQ. Два teacher/student прохода, matching views, EMA, loss и checkpoint state создают интеграционную работу; оценка её времени/VRAM пока отсутствует.

#### Предлагаемые проверки следующей практической волны

Все E ниже **proposed, не выполнены**. Численные критерии принятия задаёт команда после получения классов/метрики и до просмотра сравнительных результатов; здесь не выдуман универсальный безопасный порог precision. Отсутствие достаточного числа редких positive — ограничение вывода, а не нулевая ошибка.

### W1-10: решение и контракты

#### 1. Какие механизмы нельзя смешивать

| Механизм | Что передаётся | Требования к сопоставлению | Что останется в deployment |
|---|---|---|---|
| Предразметка | Boxes, фразы, scores → исправленные labels | Ontology, геометрия координат, полнота разметки | Обычный обученный student; teacher может отсутствовать уже во время его обучения |
| Отбор кадров | Disagreement, неопределённость, найденные редкие объекты | Единица независимости, sampling budget, отдельный test | Student, обученный на выбранных и размеченных данных |
| Offline pseudo-label training | Неисправленные/отфильтрованные teacher boxes как targets | Class mapping, ignore для неполной разметки, качество labels | Student; детали SSL — → W1-09 |
| Feature KD | Intermediate tensors с дополнительным loss | Spatial strides/levels, channels, одинаковый преобразованный вход | Student без teacher/projectors при корректном извлечении |
| Logit KD | Soft class distributions | Одинаковая семантика и порядок классов, foreground/background, соответствие locations/queries | Student; один temperature из classification не решает matching детектора |
| Localization KD | Распределения координат/box regression outputs | Представление box, anchors/points, scale, bins, assignment | Student с исходным head, если inference path не изменён |
| Ensemble как teacher | Совмещённые detections либо отдельные feature teachers | Ontology, дубликаты, fusion/matching и confidence calibration | Один student только при отдельном обучении; ensemble inference сам по себе сжатием не является |

Таблица — наш инженерный вывод по найденным интерфейсам, не опубликованное сравнение эффективности. Grounding DINO с языковым grounding далее обозначен VLM-помощником; это не утверждение, что любая generative chat VLM выдаёт пригодные detection labels. Свободный текст о наличии каски нельзя автоматически превратить в bounding box или метку «человек без каски».

#### 4. Как выбирать route при неизвестных данных

Это условные рекомендации/выводы, не результаты наших испытаний.

| Наблюдаемая ситуация | Кандидат | Gate до дорогой работы | Цена/ограничение |
|---|---|---|---|
| Нет target labels, нужны boxes существующих визуальных объектов | GroundingDINO preannotation + human review | E023: полезность и correction cost по классам | Offline teacher GPU/CPU time, integration координат/ontology, исправление пропусков |
| Student уступает сильному target teacher той же family; data/ontology уже корректны | Native Ultralytics feature KD | E027 + E028 | Дополнительный forward и feature memory, compile disabled; teacher может не добавлять нужный сигнал |
| Плохая локализация при совместимом distribution head и уже есть MMDetection stack | LD как отдельная исследовательская ветка | Tensor contracts и baseline parity | Legacy dependencies, новый loss/trainer; не первый произвольный YOLO эксперимент |
| Нужен heterogeneous backbone teacher/student и есть рабочий legacy FGD stack | FGD | GT completeness, одинаковые feature grids, recipe/version | Porting/hooks/checkpoint conversion; paper improvement не переносится численно |
| Сильный teacher на том же материале тоже систематически пропускает маленький СИЗ | Data/scale/annotation диагностика → W1-06/08 | Видимость и независимый label audit | Копирование ошибки KD само по себе не добавит наблюдаемого сигнала |
| Ensemble/VLM видит «нарушение», но нет определения person-object/event relation | Уточнить observation/ontology → violation_methods | Действительно ли визуального кадра достаточно | Нельзя переносить scene-text response прямо в object-level labels |

Для native KD не требуется teacher в realtime pipeline. Для предразметки teacher вообще можно вынести в отдельную среду; student deployment cost определяется student graph, input size и postprocessing. Но «teacher offline» не отменяет затраты на обработку пула, хранение provenance и проверку. Если учитель обучается специально для KD, его training budget включается в стоимость route. Считать только финальную эпоху student было бы нечестно.

В 45-часовом кейсе нет установленного времени на интеграцию. Приоритет KD условен: он повышается, если target teacher и рабочий same-family trainer уже имеются; снижается, если сначала нужно обучить teacher, переносить legacy stack или выяснять ontology. Эти критерии полезнее неподтверждённого обещания «улучшим компактную модель за N часов».

### W1-11: решение и контракты

#### Решение и граница применимости

Синтетику стоит рассматривать для конкретного установленного пробела: редкий внешний вид объекта, недостающий фон, диапазон поз/масштабов или перекрытий. До целевого датасета нет основания выбирать её главным способом адаптации. Практически наиболее контролируемый первый кандидат — композиция проверенного целого человека вместе с СИЗ и связями на train-only фоне, если есть корректные masks. Генеративное редактирование состояния ношения требует повторной аннотации: сохранённый prompt или исходный box не доказывает истинность нового label.

Проверка полезности обязательна на независимом реальном holdout. Главный контроль — одинаковые real train images и исходные веса с вмешательством real+synthetic против real-only; нужно отдельно контролировать число updates и exposure реальных примеров. Высокая оценка на синтетическом validation показывает соответствие генератору, а не перенос на камеры. Ни одна из открытых здесь работ не устанавливает качество PPE CCTV, событий курения или исполнение модели на LinQ.

### W1-12: решение и контракты

#### Решение и граница

До настройки LR нужен последовательный допуск: **семантика и визуальная проверка labels → реально полученный batch → градиенты и фактический optimizer step → намеренное переобучение крошечного набора → сохранение/новая загрузка → независимая validation → изменение recipe**. Это предлагаемый нами диагностический порядок, а не опубликованная гарантия. Низкий mAP сам по себе не различает перепутанные class IDs, пропавшие labels, невозможный масштаб объекта, ошибку evaluation и неудачный LR.

Зафиксированный Ultralytics — пример проверяемой реализации, не заранее выбранный стек для LinQ. Ни один default ниже не является оптимумом для промышленного CCTV. Нет целевых данных/модели/SDK; не выполнены training, benchmark, export, аренда или установка библиотек. Сведения о RTX 4070 ограничены самим названием: её VRAM, конфигурация и скорость здесь не устанавливались.

#### Диагностическая карта: что сделать до tuning

Это наши процедуры, опирающиеся на F148, F149, F150, F151, F152, F153, F154, F042, а не результаты выполненных прогонов. Нет универсального порога «хорошего» detection loss. Даже tiny overfit не доказывает отсутствие всех bugs: Stanford S108 прямо оговаривает возможность запомнить ошибочно подготовленные inputs. Не требовать нулевого общего YOLO loss или 100% AP как универсального критерия; достаточно заранее заданного качественного/численного допуска для конкретного диагностического набора.

| Порядок | Наблюдения и развилка | Что остановить / передать |
|---|---|---|
| 1. Contract/labels | Task, names/IDs, единица bbox, exhaustive vs partial, видимость объекта. Overlay исходных labels на positive/negative кадрах каждого класса/источника | Любой class mismatch или пропущенный обязательный объект → datasets; LR пока не менять |
| 2. Реальный loader | Сверить список файлов/counts/split hashes; полученные img/cls/bboxes/batch_idx; shape/dtype/range/channels, letterbox/crop; overlay после transforms; пустые target batches | Loader hang → workers/cache/I/O, не optimizer. Несовпадение target/geometry → исправить pipeline |
| 3. Forward/backward/step | Loss-компоненты конечны, grad enabled; ожидаемые head/backbone trainable; gradient nonzero на положительном batch, finite; unscaled norm; веса до/после настоящего optimizer step | None grad не всегда bug: frozen/unused branch нормальны. Неизменение всех нужных весов после подтверждённого step → loss detach/freeze/optimizer/scaler диагностика |
| 4. Tiny overfit | Один и тот же вручную проверенный малый набор, без сильных случайных transforms; видеть конкретные boxes до/после обучения; проверка на тех же train images только для sanity | Не способен выучить видимый понятный объект → labels/preprocessing/loss/head/update; длинный full run не запускать |
| 5. Reload | Закрыть процесс; load сохранённого checkpoint; фиксированный input/preprocess/postprocess, сравнить outputs и маленькую val | Расхождение → artifact/version/class map/mode/precision; не обвинять LR |
| 6. Independent validation | Ошибки по классу/камере/размеру; train vs вал; фиксировать thresholds/NMS и geometry | Train хорошо, target плохо → leakage/domain/coverage/visibility; отсутствие сигнала → scale/violation_methods |
| 7. Только теперь tuning | Явный optimizer для LR-сравнения; один фактор, одинаковые inputs/budget/selection | Нет практического выигрыша на выбранном val → сохранить baseline, закрыть гипотезу |

Для исключения процессов loader допустим диагностический workers=0/cache=False (реальные cfg args S029), но это изоляция причины, не рекомендация максимальной скорости. Windows script требует main guard по S105; конкретная ОС будущего training не предполагается. Anomaly detection S107 запускать только на минимальном воспроизводимом batch, охватывая forward и backward; это инструмент поиска операции с NaN, а не оптимизация production training.

### W1-13: решение и контракты

#### Решение для команды

Сначала сохранить качественный FP checkpoint и доказать корректность его экспорта. Далее проверить фактический маршрут компилятора LinQ; PTQ исследовать на совместимом с этим маршрутом графе. QAT имеет смысл как отдельная гипотеза после локализации потери PTQ и получения требований целевого квантования. QDQ/QOperator — способы представления квантованного ONNX, а `.ort` — формат модели ONNX Runtime; ни одно название само по себе не устанавливает поддержку LinQ.

Публичное основание сильнее, чем простое «всё неизвестно»: LinQ действительно заявляет int8, PyTorch→ONNX→LinQ Compiler и DNN Quant. Но документы не определяют нашу версию SDK, точный opset/operator set, signedness, granularities, формат calibration и импорт QAT. Поэтому нельзя назначить ORT quantizer заменой DNN Quant или обещать, что уже квантованный ONNX будет принят.

Pruning требует различать маску нулей, физическое уменьшение плотного графа и специальный sparse runtime. Процент нулей, уменьшенный архив или FLOPs не являются доказательством ускорения устройства. Для 45-часового кейса безопасный порядок исследования: работающий компактный baseline → реальный export/target → PTQ с разбором потерь → только затем обоснованный QAT или изменение архитектуры. Это наш условный вывод, а не опубликованный результат на CCTV.

#### Условные маршруты

| Наблюдение | Следующее действие | Условие принятия |
|---|---|---|
| FP export уже изменяет outputs/качество | Исправить export/input/output contract до quantization | Согласованная FP цепочка; величина допуска определена по задаче |
| LinQ принимает FP ONNX и сам квантует | Сохранить FP ONNX, calibration pool и настройки DNN Quant | Получены воспроизводимые compiler log, target outputs и качество |
| LinQ требует уже квантованный граф | Получить точный sample и quantization contract | Проверен конкретный exporter/quantizer + SDK version |
| PTQ теряет критичный recall | Проверить coverage calibration, preprocessing, graph matching; затем selective quantization или QAT | Поддержка target и парная оценка, без скрытой смены порогов |
| Нужна меньшая latency, граф dense | Сравнить меньшую поддержанную модель или физически уменьшенный dense graph | Измеренная target latency и приемлемая потеря качества |
| Есть sparse kernel LinQ с известным pattern | Исследовать ровно этот pattern | Компилятор/профиль подтверждает sparse execution; иначе ветка не обоснована |

### W1-14: решение и контракты

#### Решение

При неизвестных данных и пределах модели сначала выгодно получить независимые ответы на разные содержательные вопросы: есть ли полезный исходный detector, покрывает ли разметка ошибки, помогает ли масштаб изображения, проходят ли веса путь целевого исполнения. Это наша условная рекомендация, а не экспериментально доказанный оптимальный scheduler. Несколько GPU позволяют ускорить получение таких ответов независимыми trials. DDP ускоряет один согласованный прогон; оно не проверяет несколько гипотез и не создаёт независимых повторений.

DDP имеет смысл после установления корректного baseline и рецепта, если именно продолжительность одного обязательного training находится на критическом пути, одна replica помещается на устройство, данные успевают загружаться, backend/сеть работают и измеренное ускорение окупает настройку. При малом датасете, коротких прогонах, слабой сети, CPU/дисковом bottleneck или ещё не закрытых вопросах разметки дополнительные независимые trials могут дать больше полезного знания. Число GPU само по себе не определяет выбор.

Известно только наличие RTX 4070, ноутбука и возможности облака. VRAM, ОС машины с GPU, RAM, CPU, диск, driver/CUDA/PyTorch, межсоединение и скорость неизвестны. PowerShell исследовательской среды не устанавливает ОС training-машины. Обязательный инференс на LinQ — отдельный gate; успех на CUDA не подтверждает его.

#### Предлагаемые проверки: не выполнены

Общее для E040, E041, E042, E043, E044: пригодный checkpoint и repo revision от model_stack; snapshot данных и class map от datasets; отдельные train/validation по камерам/сессиям; fixed metrics/thresholds/selection от evaluation. Не использовать lockbox для выбора trials. У каждого run уникальный output directory, config diff, dataset hashes, seed, версии Python/torch/CUDA/driver, GPU model/VRAM фактического устройства, OS/CPU/RAM/storage, startup/finish timestamps и владелец. Успешное выполнение не доказывает inference на LinQ.

### W1-15: решение и контракты

#### Решение, которое меняет ветка

Передавать в интеграцию следует зафиксированную комбинацию weights + preprocessing + postprocessing + event rules, прошедшую независимый протокол. Имя `best.pt` и максимум mAP на многократно просмотренной validation не являются достаточным основанием. Нужно сохранить предыдущий пригодный bundle и различать статусы: перспективен на validation; подтверждён на закрытом материале; прошёл преобразование; реально выполнен на целевой платформе. Последние два статуса пока неизвестны.

В условиях малого бюджета полезнее одно причинно понятное парное сравнение с честным статусом неопределённости, чем несколько одновременно меняющихся recipe. Повторы назначаются по риску: stochastic optimization, выбор малой обучающей выборки и перенос между camera/session — разные вопросы. Ни один не закрывается универсальным «поставить seed=0».

#### Контракт принятия без вымышленных чисел

Следующее — **предложенная политика команды**, а не установленное требование кейса. После получения GT/evaluation contract до trials заполнить параметры `primary_metric`, минимальный практически значимый выигрыш `delta_min`, допустимую регрессию базовых классов/камер `epsilon_c`, критичные recall floors `R_min,c`, FP budget и единицу exposure, uncertainty procedure, maximum candidates/repeats, integration reserve. Пока значения не утверждены из кейса и baseline, результат обозначается exploratory, без binary safety acceptance.

Полезна constrained selection: сначала исключить candidate, нарушающие критичные ограничения; среди оставшихся сравнить основную метрику и стоимость. Для подтверждённого выигрыша можно заранее потребовать lower confidence bound парной Delta выше `delta_min`; для каждого критичного degradation — выдержанный non-inferiority margin. Это строгий вариант, требующий достаточного материала и обоснованного interval. Положительная Delta с интервалом, пересекающим ноль/практический margin, означает «данных недостаточно», а не автоматическую ничью или доказательство бесполезности. При большом числе trials post-selection interval на той же validation не является независимым доказательством; подтверждение — закрытым материалом.

Если objective — fixed FP budget, thresholds каждой модели настраиваются на рабочей validation по одинаковому заранее заданному алгоритму/бюджету; на lockbox они уже фиксированы. Нельзя на lockbox подбирать порог каждой модели, чтобы сравнить «при одинаковом числе FP». Одновременно сохранить результат при общих settings: так видно, переносит ли candidate прежнюю конфигурацию.

Stop/rollback имеют несколько оснований. Немедленный stop дорогого пути: leakage/class-map/annotation corruption; отсутствующий пригодный artifact; неустранённые NaN/reload failures по W1-12. Остановка гипотезы: заранее исчерпан candidate/repeat budget без достаточного выигрыша либо регресс критичных сценариев; сохранить baseline и конкретное знание. Остановка улучшений: лучший допустимый bundle заморожен до integration reserve, новые изменения не успевают пройти тот же протокол. Rollback: деградация после export/quantization/target runtime ведёт к предыдущему прошедшему bundle или к точной локализации преобразования, а не к молчаливой подстройке порога на test.

#### Manifest пригодного результата и rollback

Это предлагаемый набор полей артефакта, не готовая команда или обязательный формат конкретного framework. Сохранять manifest рядом с неизменяемыми файлами; пути и SHA256 должны позволять восстановить **конкретный bundle**, а не искать «последний best».

| Раздел | Обязательные сведения |
|---|---|
| Identity/lineage | run ID, UTC timestamps, owner, hypothesis, parent baseline ID, git SHA/dirty patch, model/task/architecture, source weight hash, class IDs/names/order, license/provenance |
| Data | dataset/annotation revisions и hashes, coverage/ignore rules, train/val/lockbox/calibration/unlabeled roles, camera/session/episode/time mapping, selection history, label budget в objects/images/independent groups |
| Training | effective config, transforms/sampling, all RNG seeds/worker handling, trainable mask, optimizer/update/batch/accumulation/precision, actual budget/retries, environment lock/OS/driver/CUDA/GPU/VRAM; детали по W1-12 |
| Selection | primary/constraints/delta margins, candidate budget, выбранный epoch и criterion, EMA vs online, results всех candidates/seeds, evaluator commit/settings, support/exposure, uncertainty method, lockbox access log |
| Files | inference checkpoint hash, отдельно resume checkpoint и состояние optimizer/scaler/RNG/loader насколько реально сохранены; stripped artifact не объявлять точным resume, actual reload validation |
| Inference | shape/layout/dtype, color/resize/letterbox/normalization/inverse geometry, decoder, confidence/NMS/caps, track/association/zone/temporal rules, dependencies и rule config hashes |
| Export/target | source→export→quant→compiled hashes, opset/flags/calibration subset, compiler/runtime/SDK/device versions и logs, точное место исполнения и known fallbacks, parity/GT results с status |
| Decision/rollback | approved/provisional/rejected/target-unverified и основания, открытые ограничения, ссылка на прежний прошедший bundle, действие переключения model+preprocess+rules+runtime вместе, smoke inputs и критерий восстановления |

Rollback не равен замене одного файла weights при оставшихся новых class map/NMS/rules. Старый bundle не перезаписывать. Прежде чем считать восстановление рабочим, повторить фиксированные smoke inputs и убедиться в соответствии manifest; smoke не заменяет повтор quality на новом домене. После заморозки новые идеи складываются в backlog; внесённое изменение создаёт новую ревизию и возвращается к соответствующему gate.

### W2-01: решение и контракты

#### 1. Решение и границы

Искали, есть ли native KD route ближе к публичному LinQ lead `yolo11`/`yolo8`, чем один пример YOLO26 из W1. Важны три разные проверки: опубликованный package содержит нужную реализацию; конкретная пара совместима по training tensors; финальный inference artifact действительно обычный student. Первая установлена по bytes, вторая по исходникам для стандартной пары, третья по lifecycle кода. Ни одна не доказывает качество на наших камерах или поддержку фактически выдаваемого LinQ.

`U = e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8` — W1 pin, commit 2026-10-22T20:27:18Z. `R = f7dd275e5853801674ca78ef51896617bb5362ba` — release commit, 2026-10-22T17:39:36Z. Далее все code locators относятся к U; десять перечисленных ниже package files побайтно совпадают с опубликованным wheel. Не исследуются полный model_stack, все teacher architectures, QAT или оптимальный `dis`.

#### 6. Маршрут от метода к нашей пользе и outcome K001

| Уровень | Actual status | Что изменилось относительно K001 |
|---|---|---|
| Feature KD описан | Установлено W1, S078/S080 перечитаны | Не нужен новый общий обзор papers; механизм конкретно confidence-weighted neck L2 |
| Available implementation/package | **Установлено новым META+bytes evidence F187** | Не только source tree __version__: wheel доступен, SHA проверен, десять contract files совпадают с U |
| Candidate contract | **Code-supported, documented family support F188, F189, F190, F191, F192** | YOLO11n←target-trained YOLO11s конкретизирован; class count не ложный runtime gate; head single/dual paths разведены |
| Student extraction/resume | **Code-observed F193**, не execution | Teacher отсутствует уже в EMA checkpoint; projectors живут до final unwrap; interrupted и final artifacts различаются |
| Target benefit | **Не установлено** | Нужны teacher audit и controlled student comparison E027; новый benchmark gain не заявлен |
| Actual LinQ | **Не установлено** | Публичный vendor family lead F166/F14 остаётся lead. YOLO11 standard graph/shape/quant contract требует SDK и target run |

**Рекомендуемый outcome для сборщика:** K001 «уточнена область / публичная contract-часть закрыта». Native KD — более конкретная условная опция, но не выбранный default и не готовое обещание прироста. Новых target measurements нет. Числа COCO из W1 не повторены и не перенесены на YOLO11.

### W2-02: решение и контракты

#### Ответ и изменение решения

На Ultralytics pin U=`e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8` штатный detect route не имеет найденного сквозного class-coverage/spatial-ignore интерфейса. Это уже не общий вопрос к model_stack: конкретно установлены читаемые targets, назначение, нулевые class targets, regression foreground и обе end-to-end ветви. В этой цепочке «добавить поле ignore», `mask_gt`, `class_weights`, `overlap_mask` либо отфильтровать class rows недостаточно. [F194, F195, F196, F197, F198, F199, F200, F201]

Уточнение удобной рекомендации: **для objectness-free detect случай B (целиком unknown class) действительно можно ограниченно решить классификационной маской**, если все оставшиеся классы размечены исчерпывающе и нет иных affected tasks. Ей не обязательно менять bbox loss: bbox loss уже только на известных positives. Но это custom criterion/data contract, не установленный CLI. Для C (скрытый второй instance present class) image×class mask либо оставляет false negatives, либо лишает модель правильных positives/negatives; spatial mechanism не восстанавливает отсутствующий GT и его localization. В legacy YOLOv5 дополнительно требуется objectness ignore. Не следует одинаково требовать «переписать все losses» для каждой architecture. [F198/F200/F202/F203]

Найден ограниченный готовый spatial-ignore route в MMDetection Faster R-CNN, но его проверка опровергла универсальность «framework уже поддерживает crowd»: обычные thresholds отключены, ignore class-agnostic, а при zero regular GT MaxIoUAssigner назначает всё background. Для произвольного B/C безопасный union без дополнительной работы не установлен. [F204/F205]

K002: **публичный implementation gap существенно закрыт / область уточнена**. Не закрыты correctness исполнения будущего механизма, реальная coverage данных и полезность обучения. E007 остаётся практическим gate, со специфическими observables ниже.

#### A/B/C: targets, negatives и допустимый маршрут

Обозначения: одинаковое изображение с сохранёнными pixels; A — полный GT; B — удалены все boxes класса c (class coverage unknown, остальные classes exhaustive); C — удалён один из нескольких instances c. Выводы ниже — **static trace**, не запуск сравнения. Отсутствие в TXT не позволяет loader отличить B/C от проверенного отсутствия.

| Вариант на U detect | Assignment / targets | Какие negative terms и regression | Штатная mask support | Engineering / допустимый data route |
|---|---|---|---|---|
| **A** | Известные GT участвуют в TAL; fg и мягкие class targets определяются predictions/geometry; не каждый anchor внутри box positive | BCE у всех entries; negatives включают non-target classes. CIoU + DFL либо L1 только fg | Обычная positive/padding handling; partial mask не нужна при действительно exhaustive policy | Обычный supervised training после loader gate; полная разметка определяется рабочими classes/ROI/visibility policy, а не всеми предметами мира |
| **B: весь c скрыт** | Ни один GT class c не существует; column c target_scores=0 у всех anchors этого image. Другие GT могут назначать anchors в его области | Весь column c даёт negative BCE; missing c не имеет regression. Другие classes продолжают обычные losses | Нет image×class unknown consumer | Для objectness-free detect custom `[B,1,C]` validity mask достаточна, чтобы убрать **этот negative column**, при строгих предпосылках B; оставить остальные positives/box supervision. Нужны loader+augmentation+criterion wiring, обе E2E branches, explicit normalization. Иначе полная доразметка или separate task с exhaustive own classes |
| **C: один из нескольких c скрыт** | Kept c продолжает создавать positives; hidden instance не участвует; область может быть bg либо assigned known object | Hidden-only candidate entries c остаются target=0 → negative BCE; нет hidden regression. Kept targets/normalizer могут измениться | Нет spatial/class-aware unknown consumer | Обычная image×class mask c удалит также правильные positives. Маска только negative entries c по всему image сохранит positives, но удалит и достоверные negatives и не восстановит hidden GT. Для локального suppression нужны actual unknown-region geometry/ROI или проверенный mining/prior; без них наиболее конкретный data route — доразметка. Separate task не лечит missing instances **того же** task |
| **Пустое image после B/C** | Нет positives (в all-empty batch early return, в mixed batch mask_gt=False) | Все class BCE targets=0; box loss пустой foreground. Это не нейтральное unlabeled image | Нет штатного automatic skip-unknown | Явно исключить из supervised stream, доразметить либо special criterion; не считать missing TXT negative |
| **E2E для A/B/C** | Две независимые assignments на тех же GT, разные topk | Оба weighted losses affected; displayed one2one loss скрывает состояние one2many | Нет отдельного готового partial switch | Повторить observables/masks и positive-preservation обеих branches; inference выбор branch не выключает training loss другой |

#### Уровни готовности и выбор data route

| Маршрут | Paper/документ → implementation | Candidate contract | Target benefit |
|---|---|---|---|
| Полная рабочая разметка subset | Обычный supervised detector; U chain прочитан | Exhaustive classes/ROI/visibility policy + loader gate; нет новых partial fields | Не измерен; сравнить количество/разнообразие labels и quality по E006 |
| U B, image×class unknown | W1 обосновал смысл; U mask consumer **не найден** | Нужны custom dataset/transforms/collate + BCE validity, обе branches и reduction audit | Неизвестен; это не готовый training flag |
| U C, spatial sparse | Методологические candidates W1 есть; native consumer не найден | Geometry/prior/mining + per-entry masks + assignment audit; отсутствие hidden box нельзя исправить одним class row | Неизвестен; engineering gate до learning trial |
| MMDet M known ignore boxes | Публичный готовый code chain прочитан | Class-agnostic IoF, positive settings **обоих** assigners, nonempty regular GT; empty case исключён | Не измерен, смена detector и export может быть дороже доразметки |
| Separate tasks | Обычное supervised обучение каждой таксономии | Каждый источник exhaustive для own task; не объединять missing labels в общую head. Missing instances own class всё равно исправлять | Association/inference cost и LinQ support отдельно неизвестны |

### W2-03: решение и контракты

#### Ответ для решения команды

One-stage online SSOD имеет конкретные авторские реализации. UTv2 — **FCOS с изменённой regression head**, отдельными pseudo targets для classification/regression и uncertainty comparison; это не обычный FCOS trainer плюс EMA-флаг. Стандартный eval выбирает teacher. Uncertainty-ветвь **остаётся в фактическом Python eval forward**: при стандартном test scoring её значение не определяет ranking boxes, но возвращается дополнительным полем `Instances`. Автоматическое получение обычного FCOS export не доказано.

Для потенциального anchor-based YOLOv5 ближе **AlibabaResearch/EfficientTeacher**, чем порт Listen2Student из FCOS. На проверенном SHA доступны custom config, pseudo assigner/loss, paired loader, EMA checkpoint и exporter с явным удалением domain heads. Это условная ветка для YOLOv5 family, **не установленная поддержка современного Ultralytics YOLO8/11/26**. README перечисляет несколько families; проверенный online teacher forward для иного `model_type` явно заканчивается `NotImplementedError`.

Сначала E024 и runnable supervised baseline; полностью исправленные labels идут обычным supervised route E025. Online имеет смысл ставить в очередь при достаточном U_train, прошедшем audit teacher, compatible exact trainer и заранее понятном inference artifact. Ни время, ни VRAM, ни target gain этим чтением не измерены.

#### Матрица переноса и цена interfaces

| Interface / ресурс | UTv2 FCOS code-observed | ET YOLOv5 code-observed | Переносимость / ограничение |
|---|---|---|---|
| Данные | fully labeled L + image-level U, D2 Instances/two crops | L labels + U list/fake labels, paired canvas/M_s | Группы/audit reusable; partial L не становится exhaustive |
| Class/head | sigmoid classes, centerness, discrete ltrb/std | anchor-based objectness/classes/xywh | Ontology переносима; channels/assignment/std не переносятся флагом |
| Missing positive | focal negatives вне pseudo positives | objectness0 вне matched reliable/uncertain anchors | Audit omissions обязателен; threshold не добавляет отсутствующий сигнал |
| Regression | relative per-boundary uncertainty, NLL head | IoU и confidence/objectness selection | FCOS findings не дают готовый modern YOLO loss |
| Geometry | common resize/flip; strong photometric/erase | weak/mosaic + M/flip mapping | Нужны overlays/known boxes; не смешивать mapper/loss repos |
| State/compute | student+teacher, L2 views/Uweak/Ustrong | student+EMA+secondary EMA, U epoch adaptor | Измерять extra forward, memory, loader queues, audit/debug |
| Final graph | std остаётся eval field; fixed test score не использует её | --da удаляет auxiliaries; raw outputs требуют decode | Нет измеренной готовности standard exported model |
| Families | FCOS R50 route | YOLOv5l P5 route | Не доказаны current Ultralytics/LinQ |
| Простая альтернатива | E025 | E025 | Полные labels + обычный supervised loss требуют меньше новых interfaces; время не измерено |

ET уточняет K003: если model_stack выбирает compatible YOLOv5 и получает baseline/conversion parity, нет необходимости сначала писать FCOS port. Если выбран иной head либо SDK не принимает exact graph, corrected supervised route остаётся предпочтительным по интеграционным prerequisites. Само наличие ET не оправдывает смену всего стека.

### W2-04: решение и контракты

#### Ответ K004 и изменение решения

Простой кандидат отбора подтверждён на уровне интерфейса: один обычный detect `predict` даёт сохраняемые boxes, scalar confidence и class ID; этого достаточно для явно определённого **low-confidence ranking**, дополненного metadata/seeded exploration. Называть его class entropy, calibrated uncertainty или гарантированно более полезной разметкой нельзя. Дополнительные forward passes и hooks этому кандидату не нужны. Основание считать **вычисление score поверх уже полученных Results** дешёвым сохранилось; основание считать весь acquisition loop дешёвым по полному времени команды отсутствует. Сканирование пула, NMS при низком cutoff, просмотр false positives, полная разметка и QA остаются измеряемыми затратами.

K004 получает статус **публичный interface gap закрыт для U; применимость уточнена, target benefit открыт**. Сложный ROI entropy/feature/diversity selector не становится обязательным. Q016 нужно разделить: стандартный Results interface установлен; raw head integration, конкретный checkpoint и полезность относятся к отдельным gates.

#### Output → допустимый score → ограничение → добавленная цена

Таблица — наши инженерные следствия F220, F221, F222, F223, F224, F225, не измерения качества.

| Доступный материал | Что разрешено вычислить | Что не устанавливается | Добавленная стоимость |
|---|---|---|---|
| Обычный detect Results, NMS или e2e | Явный ranking по retained scalar confidence; count/size/predicted-class strata | Полная entropy, objectness, отсутствующие объекты, локализационная правильность | 0 новых forwards при уже выполненном pool inference; reduction и сохранение `N×6` + metadata |
| Пара Results разных checkpoint/views | Определённый box disagreement после class/coordinate matching | Независимость ошибок, FN обоих моделей, calibrated epistemic uncertainty | Дополнительный inference каждого teacher/view, transform inversion, matching; не выбранный минимальный route |
| Native one-to-many decoded tensor | Vector-based собственная sigmoid score definition; margin с явной семантикой | Categorical posterior, ROI entropy ActiveTeacher, target benefit | Custom predictor/raw-output capture, хранение порядка `A×(4+nc)` на image вместо `N×6`; новые forwards не обязательны |
| Raw head dict до top-k | Logits/features/locations выбранной ветки с документированным decoder | Универсальный API для exports и alignment между heads | Model-specific decoding/индексы, feature memory и regression gate |
| `model.embed` | Image clustering/diversity по закреплённому feature extractor | Semantic/person diversity, редкие GT классы | Native PT; отдельный проход до выбранного layer для совместного использования с Results, vector storage `D`/image, выбор расстояния |
| Camera/session/time metadata | Seeded stratified random + temporal cap | GT diversity внутри одинаковой metadata | Manifest и sampling; inference вообще не обязателен |

Если когда-либо добавляется box disagreement, сначала зафиксировать canonical classes, `xyxy` в original pixel coordinates, class-consistent one-to-one matching и IoU threshold, deterministic tie rule и penalty unmatched boxes. Для augmented view инвертировать transform и исключать невидимые/cropped regions. Один matched IoU не оценивает misses. Это только спецификация возможной будущей ветки; F097 уже показывает цену localization stability через дополнительные forwards.

### W2-05: решение и контракты

#### Ответ и изменение решения

Полная ручная коррекция допускает teacher как помощника без требования сначала построить calibrator. Unchecked pseudo-label branch нуждается в отдельных доказательствах правильности принятых boxes **и** сохранённой полноты на всех GT, включая кадры без detections. Публичный calibration route найден, но он не закрывает missed-positive audit. При нулевой/малой независимой поддержке нужной страты нельзя выдать допуск по хорошей средней precision.

K005 **уточнён и закрыт в публичной/методической части**: установлен detection-specific смысл calibration, её предел по no-detection misses, проект sampling/denominator contract и правила отказа. Actual target support, numerical acceptance и полезность teacher остаются case/experiment неизвестными Q010, Q004, Q011. Ни один класс этим исследованием не разрешён для unattended labels.

### W2-06: решение и контракты

#### Ответ для решения K006

**Предобучение нельзя выбирать одной осью «pretrained/scratch».** Нужны отдельно происхождение backbone, наличие обученных localization/neck/transformer/head-компонент, семантика classifier и дополнительный supervised source этап. Здесь найдены два различающих первичных маршрута: DetCo как detection-friendly representation и DETReg как предобучение компонентов детектора поверх уже сильного SwAV backbone. Полноценный source detector после base-class training — ещё один уровень; его польза не доказывается сопоставлением разных architectures или разных downstream schedules.

Ни DetCo, ни DETReg не назначаются победителем для PPE. Новый материал даёт основания проверять **конкретный состав перенесённых tensors**, а не ожидать выигрыш по названию SSL. Один будущий E048 ниже отделяет detector-specific weights от того же backbone. Готовый пригодный source detector может остаться практическим первым кандидатом, если его задача/граф/лицензия подходят; это условный выбор стоимости и доступности, не опубликованная гарантия target качества.

#### Условный выбор initialization и tensors [PROPOSED; F235, F236, F237, F238, F239, F240, F016/F10]

| Наблюдаемое условие | Кандидат и перенос | Что сбросить/проверить до FT | Условие включения в очередь |
|---|---|---|---|
| Есть подходящий обученный source detector той же architecture, нужная semantics частично совпадает | Backbone+neck/localization/head feature transforms; classifier rows только при семантическом mapping | Unmatched/incompatible rows; class-dependent bbox outputs, anchors/strides, normalization и обе branches при наличии; actual tensor log | Provenance/licence известны, target audit локализует detector error; zero-update reference сохранён |
| Совместимый detector artifact есть, target classes новые | Сохранить совместимые feature/localization tensors; создать корректный target classifier | Background convention, class-specific regressor versus class-agnostic regressor; одинаковые новые rows для сравниваемых arms | Имеются полные target labels и независимые groups; class-name match не используется как единственное основание |
| Есть только classification/SSL backbone подходящей topology | Перенести backbone с правильными channel order/normalization/stride | Neck/RPN/transformer/queries/predictors не считать pretrained; создать и зафиксировать их initialization | Сопоставимая head-training возможность и бюджет; exporter/target graph route не закрыт сменой trainer |
| Есть detector-specific SSL artifact, как DETReg, для уже допустимой architecture | Backbone+поддержанные localization/transformer/query components; сравнить с тем же backbone без них | Class-agnostic classifier reset; embedding branch removal; exact key/shape audit | Только после artifact smoke и при пользе различения; E048, не перенос DETReg алгоритма в неизвестный YOLO |
| Есть только unlabelled in-domain video | Пока использовать допустимый готовый init; audit/annotation может быть следующим действием | Permission/exposure split и GT для quality selection; учесть ancestors teacher/pretrain | Новый domain pretraining только при unmet detector failure, наличии реализации, допустимом времени и контроле дополнительного exposure |
| Нет полного target GT или мало независимых позитивов | Сохранить hypotheses и zero-update reference | Нельзя выбрать init по pretext loss/linear Top1/визуально красивым примерам | Сначала supervised audit/annotation gate; не объявлять победителя |
| Source data/semantics или artifact compatibility неизвестны | Не считать checkpoint готовым кандидатом только по URL | Получить manifest, version/hash, key audit и минимальный load contract | Устранить missing artifact; не начинать дорогое pretraining как автоматический обход |

Эта таблица выбирает способ подготовки стартового состояния, а не весь PPE stack. LinQ пригодность выбранной architecture/export — отдельный обязательный gate, когда SDK доступен.

### W2-07: решение и контракты

#### Ответ, меняющий очередь

Авторский public route найден: **EPFL-IMOS/simple-SFOD, AdaBN → фиксированный COCO pseudo-label artifact → Faster R-CNN с сильной аугментацией**. Это более ясная реализационная зацепка, чем неустановленный repo SFOD2021. Однако это **не готовая воспроизводимая команда**: weights локальные, JSON pseudo-labels заменяется вручную, eval entrypoint выполняет AdaBN, зависимости неполно зафиксированы. K007 получает статус **уточнена область применимости; public implementation найден, runnable artifact/selection contract частично открыт**. Польза для наших камер неизвестна.

До очереди качества нужны допустимость adaptation по кейсу, совпадающая ontology и рабочий source checkpoint, независимые target labels для выбора, исключение скрытого GT/source exposure из loader/hooks, проверенная BN/eval граница и обычный inference/export route. При отсутствии этих условий сохранить frozen baseline и направить небольшой бюджет на полную ручную разметку диагностических кадров. Online adaptation не назначается.

#### Контракт кандидата: найдено / отсутствует

| Звено | Статус после W2 | Следствие |
|---|---|---|
| Paper→author repo | Установлено S184→S185, pin P | Public route перестал быть только названием |
| Source-trained checkpoint | Локальные пути; публичный artifact в tree/releases/README не найден | Нужен compatible artifact; ImageNet backbone недостаточен |
| AdaBN stage | Код прочитан, current eval entrypoint делает refinement | Исправить role boundary, dataset order/budget/buffer audit до quality queue |
| Fixed pseudo-label generation | Converter есть; полный готовый invocation/artifact chain отсутствует | Explicit prediction export→conversion→registration и hidden-GT check |
| Target updates | Один detector, ordinary loss, strong aug, no replay/EMA | Возможны missing-positive negatives; аудит обязателен |
| Selection | Paper SF-UT4000 observation, periodic eval/save code; no validated unsupervised selector | V с labels либо только feasibility claim; fixed-row last/best остаётся gap |
| Deploy | Один Faster R-CNN с BN; export/target не выполнены | Отдельный graph/export/LinQ gate |
| Target benefit | Не измерено | Никакого gain claim |

### W2-08: решение и контракты

#### Ответ, меняющий решение

**Авторский implementation Gen2Det не установлен после содержательного поиска.** Paper v1 задаёт batch sampling и background-ignore на уровне алгоритма; публичный pinned trainer/config/annotation schema, позволяющий проверить каждую loss term, не найден. Нельзя назвать ordinary folder merge воспроизведением Gen2Det или написать предполагаемый loss patch и приписать его авторам. Доступный команде условный путь — полностью переразмеченный synthetic image pool как обычные supervised данные, после E030 и с независимым real holdout E031.

**Статус K008:** область уточнена; public-author-artifact gap локализован и остаётся открытым. Условие задания допускает этот результат. Новые первичные ограничения: ignore в paper затрагивает и RPN, и detector head; рабочее значение порога фактически выключает все synthetic background regions; `p` относится к целым batches; low-data COCO не использует filtering/background-ignore. Эти сведения не заменяют actual implementation evidence.

#### Paper → artifact → metadata → assignment/loss: где цепочка обрывается

Таблица ниже — **audit contract и неизвестные**, не предлагаемый patch. С01 даёт словесный алгоритм. S191, S192, S193 не дают проверяемой реализации. Нельзя считать строку «ignore background» доказательством, что вся цепочка работает на любой family.

### W2-09: решение и контракты

#### Ответ и изменение решения

Публичный detector-specific путь существует: **NVIDIA-AI-IOT/yolo_deepstream, `yolov7_qat`, YOLOv7 → fusion → quantized modules/rules → calibration → feature-reconstruction QAT → ONNX Q/DQ opset 13 → TensorRT**. Код прочитан до конкретного loss и экспортера. Это существенно точнее общего Jacob QAT paper из W1. Однако это **не полностью закреплённый воспроизводимый toolchain**: авторская инструкция клонирует неприкреплённый YOLOv7 и устанавливает неприкреплённый `pytorch-quantization`; historical package lock/checksums опубликованных weights/ONNX не установлены. Ни одного полностью воспроизводимого LinQ QAT route этой работой не установлено.

Особенно важно: найденный QAT не использует detector GT loss; он восстанавливает признаки исходной модели через MSE. Его нельзя назвать штатным supervised fine-tuning для новых PPE classes. Переход с выбранного YOLO8/11/26 на YOLOv7 ради такого примера не обоснован. Следующая работа до QAT — получить **реальный SDK quant contract и sample, совпадающий с выбранной архитектурой**, затем закрыть dependency lock. K009: **уточнена область применимости / найден concrete code route; точный environment и target match открыты**.

#### Paper → implementation → candidate → target: статус уровней

| Уровень | Статус | Что меняет решение |
|---|---|---|
| QAT principle | F165 уже установлен | Не нужен повторный generic paper обзор |
| Detector implementation | Найден и прочитан F256, F257, F258, F259 | Конкретный reconstruction route существует |
| Exact reproducible recipe | **Неполон**: README не фиксирует YOLO/toolkit исторического опыта; ONNX/weights checksum не получены | Нужен artifact/environment lock Q023; source pins этого исследования не заменяют author run manifest |
| Candidate architecture | YOLOv7 sample; selected case model неизвестна | Нельзя объявить поддержку YOLO8/11/26/new class adaptation |
| LinQ arithmetic/export compatibility | **Не установлена** | Нужен Q008; TensorRT-specific rules не target evidence |
| Target benefit | **Не измерен** | Будущий post-export gate E049 |

#### Матрица public supports / tool mismatch / SDK question / future experiment

| Часть | Public supports | Tool mismatch или gap | Вопрос/следующий gate |
|---|---|---|---|
| Training | Detector feature reconstruction with fake quant | Не supervised bbox/class recipe; нет доказанного current environment lock | Q023 + same-data controls E049 |
| Quant representation | Signed symmetric zero-point 0 reference; per-tensor activations/per-output-channel Conv weights | Реальный LinQ может требовать другой range/axes/quantizer | Q008 arithmetic/sample |
| Placement/fusion | YOLOv7 deploy fusion + Concat/MaxPool scale sharing | TensorRT-specific patterns; detector head mixed precision возможна | Q008 placement/exclusions, затем inspect graph |
| Export | ONNX opset13 QDQ; dynamic batch | QDQ ≠ quantized LinQ package; shape 640/672 не унифицирован | SDK versioned acceptance sample, E049 parity |
| Target | Авторские NVIDIA links | Ни LinQ compile, ни actual execution не выполнены | Target placement/raw outputs/metrics обязательны |

### W2-10: решение и контракты

#### Ответ для решения и outcome K010

**Практический positive route существует на уровне прочитанного кода:** авторский репозиторий Torch-Pruning содержит YOLOv8 example, который заменяет C2f, строит DepGraph, физически удаляет зависимые каналы, восстанавливает качество обучением и передаёт изменённый объект в штатный ONNX exporter. Поэтому K010 «не восстановлен ни один физический detector route» закрывается в части implementation evidence. **Работоспособность pinned комбинации, сохранённого артефакта, качество и LinQ speed остаются непроверенными.** README одновременно даёт совместимый старый Ultralytics pin и предупреждает о поломке примера при обновлении Ultralytics. Это основание оценить инженерную цену, а не назначить pruning обязательным trial.

При наличии меньшего штатного student physical pruning следует держать в условном резерве P2. Сначала нужен факт, что штатный меньший кандидат не удовлетворяет совместным ограничениям качества/target cost, а прошедшая quality gate более крупная модель действительно упирается в model execution. Для продвижения pruning нужны ранний smoke/reload/FP export и подтверждение compiler acceptance новых dense shapes; авторский MAC ratio не заменяет эти факты. [F262, F263, F264, F265, F266, F267, F268, F269, F270, F271; E050]

### W2-12: решение и контракты

#### Переиспользуемые gates: что действительно необходимо

Эти узлы — допуски, а не пять дополнительных quality arms. Training gates нужны только при training; partial/teacher/custom graph gates нужны только выбранной ветке. При неизвестном SDK можно вести разрешённую data/FP работу, но deployment feasibility остаётся явной незакрытой зависимостью и ограничивает дальнейшие вложения. Успех FP нельзя promote как LinQ-ready.

| Узел | Необходимый вход и существующие E-ID | Выход/owner; что блокирует |
|---|---|---|
| G0 task/decision | Полный кейс: объекты/состояния/события, adaptation permission, critical constraints; E001/E02, E045 | Task/evaluation contract; owner evaluation + violation_methods. Без него допустима разведка, но нет подтверждающего quality claim/численного safety acceptance. |
| G1 data/observation | Лицензия/происхождение, source×class completeness, camera/session/episode roles; original→actual input; E033, E045, E003/E003; E012/E03 только при transforms | Versioned manifests, support/exposure, coverage/overlays; owner datasets. Leak/неверные labels/неустановимый label → исправить причину, не LR sweep. |
| G2 runnable correctness | Выбранный checkpoint/hash/pin, прошедшие G0/G1; E034/E03 с E035; candidate-specific W2-02/01/03/07/10 gates только при их route | Finite настоящий update, допустимый tiny-overfit result, immutable pre-strip copy, clean reload, actual freeze/BN/state/extraction record; owner model_stack/training. Broken update/reload блокирует long training. Старые illustrative caps W1 не копируются как универсальные бюджеты. |
| G3 comparison/selection | Zero-update reference E001, independent grouped dev, заранее primary/margins/constraints; E046 и условно E03 | Paired predictions/critical support, выбранный serialized epoch и rationale; owner evaluation. AP-best не заменяет external objective; N/A support остаётся N/A. |
| G4 deploy/rollback | Ранний import/compile feasibility на рабочем baseline; финально E037 = reused E037, actual SDK/device; exporter/decoder/quant calibration отдельно | Source FP→reload→export→quant/compiler→LinQ logs/quality/placement + цельный previous bundle; owner linq_platform/model_stack/video_architecture. Нет target доступа → target-unverified, не «принят». Lockbox не служит compile-debug набором. |

G0→G1→reference; training: G1→G2→выбранное сравнение→G3; G4 feasibility идёт рано параллельно доступной FP/data работе, G4 окончательное исполнение зависит от frozen candidate. Не открывать lockbox на каждом gate: debugging/parity используют development материал. После заморозки bundle — согласованная независимая оценка по E037. После изменения по её ошибкам прежний lockbox становится development.

#### Очередь для восьми сценариев

Сценарии могут пересекаться. Тогда выполняется самый ранний незакрытый gate, а не все строки. В столбце «следующий опыт» дан один различающий опыт либо правило выбора одной условной ветви **до** запуска. A/B — контроль и вмешательство, не предписание двух новых обучений, когда reference уже есть. Kill прекращает текущую гипотезу, promote разрешает следующий gate, rollback возвращает ранее прошедший bundle целиком.

| Сценарий | Первое наблюдение/gate | Один следующий различающий опыт и E reuse | Что ждёт его исхода | Kill / promote / rollback; useful artifact |
|---|---|---|---|---|
| 1. Только open data и подходящие weights | G0/G1: совпадает ли task/class map, есть ли хотя бы независимый target diagnostic GT, что видно на actual input; ранний G4 feasibility | **Zero-update baseline**, E001. Если target labels вообще нет — сначала полностью разметить разрешённые diagnostic сцены, это data gate, а не сразу fine-tune на open data | Full/head/SSL/KD/synthetic, pretraining from scratch | Pipeline/class mismatch→kill quality interpretation и исправить. Готовые weights удовлетворяют constrained quality и actual target→promote без training. Иначе получить error table и выбрать следующую строку. Артефакт: runnable reference, predictions, manifest, coverage и target-status; без GT — только feasibility/overlays. |
| 2. Немного fully labelled target | G1/G2: независимые сцены, новый/старый head, достаточный support; один общий target-initialized state | При uncertainty «сколько адаптировать» **limited freeze против full**, E004/E006 как один comparison; unchanged reference reuse только по покрытым классам. При доминирующей uncertainty initialization и уже matching artifacts E048 **заменяет**, а не добавляется к этой паре | BN arm, staged run, несколько pretraining families, repeats до осмысленного A/B | Mask/BN/row mismatch→kill. Critical regression→rollback. Полезное независимое различие→G3; малая/меняющая знак разница→правило repeat/annotation ниже. Артефакт: selected immutable EMA/student + load/mask/BN ledger, paired errors, data hashes. |
| 3. Target video без labels | G0: разрешён ли adaptation; G1: U отдельно dev/H; teacher покрывает ли no-box/rare/size strata, есть ли independent labels для selection | **Teacher assistance против manual** на matched train-only группах, reuse E023/E024/E023, уточнение E024: слепая полная проверка и total human minutes. Это один cost/admission pilot | Unchecked pseudo, online SSL и source-free quality trials. Calibration model не является обязательной предпосылкой полной ручной коррекции | Assistance экономит время при QA→полностью corrected labels и обычный supervised E025. Не экономит/coverage нет→manual; unknown support→unchecked не допускается. Артефакт: reviewed labels, teacher policy/audit counts, no-detection misses, measured annotation cost; не «SSOD gain». |
| 4. Разные камеры/условия | E021/G1: одинаковые detector inputs? Object errors либо camera rules? Holdout camera не участвовала в adaptation | Если detector ошибочен и есть compatible exhaustive source+target: **target-only против одного source-replay mix**, E019, old-domain retention. Если ошибка зоны/association — вместо этого E002 с неизменным detector; без target labels — строка 3 | Ratio grid, adversarial UDA, source-free/online updates, отдельная модель на каждую камеру | Aggregate gain с critical camera regression→rollback. Mix не помогает→target-only/frozen по constraints. Rule error сохраняется при oracle objects→kill detector-training объяснение. Артефакт: per-camera paired predictions/retention, class/data exposure ledger либо versioned camera-rule correction. |
| 5. Partial/heterogeneous labels | G1: distinction unknown class целиком (B), missing instance present class (C), verified absent; ordinary TXT это не сообщает | **A/B/C assignment/loss/metadata gate**, E007 + E007. Полный diagnostic GT у аудитора, hidden GT не доступен training arm. Это correctness test, не quality grid | Union training, class-weight/sampler sweeps, sparse-method training | Нет coverage/geometry consumer→kill unsafe union; fully checked subset либо separate exhaustive own tasks. B objectness-free custom BCE mask может убрать unknown column, но не учит missing localization; C не исправляется одной image×class mask. Legacy objectness и обе E2E branches проверяются отдельно. Артефакт: accepted coverage/criterion contract и преобразуемая metadata либо исправленный exhaustive subset. |
| 6. Rare/new/плохо видимый класс | E009 + G1/observability: нет независимых positives, lost pixels, exposure или missing head? Эти причины выбирают одну ветвь | Сигнал теряется только при resize→**один больший input против baseline без training**, E016; rare exposure при видимом сигнале/верных labels→**один balancing change**, E010; нет разнообразных positives/new class→**качественная independent annotation addition против прежних данных**, E043/E006. Выбрать одну по наблюдению | Одновременный scale×loss×sampling×synthetic grid; cascade/KD как автоматическое лечение rare | Native pixels не содержат различимого evidence→не удлинять training, передать observation/task вопрос. FP/critical quality/calls budget нарушены→rollback. Артефакт: pixel/support audit и один candidate/input или versioned real labels с paired rare/clean metrics; scale требует нового G4. |
| 7. Модель работает, остаются misses/FP | Ошибки с denominators на development, labels проверены; object vs association/temporal rule | **Oracle object/association substitution**, E002. Только если object причина уже установлена этим же gate: targeted hard-negative addition против equal-human-budget diverse annotation, E011; либо одна causal augmentation E013 при real degradation evidence | Следующий большой optimizer run, все hard-negative/AL/augmentation arms одновременно | Oracle objects не исправляют event→kill detector-training путь, править связь/правила. Look-alike FP уменьшаются только на mining episodes→не promote. Артефакт: stage error attribution, fixed-rule traces либо один validated data/weights candidate; mining pool не independent test. |
| 8. Хорошая FP модель дорога/теряет качество после conversion | G4 локализует: FP export mismatch, quant loss или model runtime cost? End-to-end bottleneck может быть decode/network, а не graph | Если conversion loss: **paired adjacent-stage parity**, E037/E037; если parity уже прошла и compute graph дорог: **меньший native detector против current accepted reference** при тех же target входах/метриках. Это диагностически разные входные состояния, выбирается одно | QAT до PTQ diagnosis/SDK; KD без teacher; physical pruning recovery до conversion/reload/compile smoke | FP export сломан→чинить export, не QAT. PTQ проходит→не назначать QAT. Smaller проходит quality+target cost→promote его. Иначе ровно одна подходящая compression альтернатива из таблицы ниже. Артефакт: actual target paired quality/timing/placement и accepted complete bundle; MACs не latency. |

#### Единое правило: repeat, longer run, DDP, teacher или annotation

| Следующая работа | Когда именно меняет решение | Когда не назначать; выход |
|---|---|---|
| Paired repeat A/B | Уже есть causal comparison, эффект около decision margin/меняет знак, и источник неопределённости — optimizer RNG или training-shot selection | Нет независимых scenes/rare positives→новые labels/groups, а не seeds. E047: optimization/sample/split seeds раздельны; A/B обе повторяются, все failures видны. Cap/repeat rule до запуска, без «до первого significance». Выход: stable/provisional/inconclusive. |
| Longer run | G2 пройден, нужные independent dev метрики ещё улучшаются, целевой recipe/фазы/selection явно заданы и artifact path успевает | Train loss падает без нужного dev signal→не основание. Новый E/auto/scheduler или warm-start меняет recipe: отдельно назвать intervention; штатный resume не обещает uninterrupted trajectory. Выход: selected serialized checkpoint либо сохранённый baseline. |
| DDP | Установленный нужный run действительно на critical path, replica помещается в каждую GPU, network/loader/custom code и actual E03 scaling окупаются в T_ready | DDP не объединяет VRAM, не создаёт независимых trials, local batch/BN/order/rect могут измениться. Setup/communication/review bottleneck съедает выигрыш→single/independent. E042, качество после изменений не считать чистой hardware абляцией. |
| Teacher | Ready useful teacher+compatible student/extraction либо assistance экономит total human time; цена teacher preparation включена и проходит CP | Teacher выше по unrelated AP, poor critical coverage, нужен новый expensive trainer→не основание. Выход: corrected labels или validated compact student; teacher AP не report student quality. |
| Annotation/QA | Missing/wrong/partial labels, мало независимых positive groups, domain coverage, unsupported critical audit strata или мало independent evaluation support | Дубли одного episode/неустановимый visual state не решают coverage. E043 сравнивает useful label addition с reuse reference/при необходимости matched compute continuation; сохранить human minutes, quality/support и lineage. |

#### Карта всего W1 банка: reused gates и альтернативы

Эта карта сохраняет покрытие, не добавляя обязательных runs. Слова «optional» означают условный путь, который становится обязательным только **после выбора** соответствующего intervention и прохождения prerequisites.

| W1 файл / E-ID | Место в очереди |
|---|---|
| 01 E051, E02, E03 | E051 reference/G0/G1; E02 object-vs-event diagnostic при event errors; E03 observation gate при visibility uncertainty. Это не три обучения. |
| 02 E051, E02 | E051 одна adaptation-depth альтернатива; E02 BN-specific только при drift/train-eval evidence, не дополнительный routine arm. |
| 03 E051, E02, E03 | E051 reuse few-shot adaptation + conditional repeat; E02 correctness **только** выбранного partial mechanism; E03 custom sparse-method feasibility только при actual artifact, alternative to checked subset. |
| 04 E051, E02, E03 | E051 data/exposure diagnostic; E02 один balancing candidate; E03 hard-negative vs diverse annotation alternative. Не запускать все balancing losses/samplers. |
| 05 E051, E02, E03, E04 | E051/E03 affected transform/label survival gate; E02 одна causal augmentation; E04 real degradation vs controlled corruption diagnostic. Corrupted copies не независимые observations. |
| 06 E051, E02, E03, E04 | E051 observation reuse; E02 **или** E03 input/tiles **или** cascade diagnostic; E04 scale-matched training только после выигрыша предыдущего режима. |
| 07 E051, E02, E03 | E03 camera/rule localization; E051 supervised mixing alternative; E02 UDA/source-free alternative с новыми W2-03/07 gates. W1 illustrative ratio grid не переносится как mandatory. |
| 08 E051, E02 | E02 assistance cost pilot shared с 09-E01/10-E01; E051 один selector vs random при значимом решении, не все A/B/C по умолчанию. |
| 09 E051, E02, E03 | E051 общий teacher-admission audit, E02 corrected-supervised data route; E03 online alternative после runnable/head/loss/extraction gates. Unchecked D-arm отдельна от corrected B. |
| 10 E051, E02, E03, E04 | E051 reuse assistance; E02 KD option; E03 reused student-only/extraction/export gate выбранного KD; E04 legacy FGD/LD только при уже рабочем compatible stack, не обязателен рядом с native KD. |
| 11 E051, E02, E03 | E051 synthetic labels gate выбранной ветки; E02 один real+synthetic comparison; E03 shortcut localization после observed defect, не генерация новых пулов без причины. |
| 12 E051, E02, E03, E04 | E051 loader/data gate; E02 real update; E03 tiny-overfit/reload+W2-11 save gate до expensive training; E04 optimizer гипотеза только после diagnosis, optional. |
| 13 E051, E02, E03 | E051 reuse 15-E04 conversion/target gate; E02 PTQ diagnosis **до** QAT; E03 QAT **или** physical pruning после разных prerequisites, не общий обязательный compression run. |
| 14 E051, E02, E03, E04, E05 | E051 bounded profiling при resource decision; E02 loader/cache только по bottleneck; E03 DDP только когда single run critical; E04 annotation alternative; E05 dispatch rule, не отдельный training arm. |
| 15 E051, E02, E03, E04 | E051 partitions/selection contract reuse; E02 comparison contract; E03 conditional repeat; E04 frozen artifact/lockbox/target acceptance reuse. Это один protocol, не четыре дополнительных эксперимента для каждого метода. |

Снятие mandatory grid не убирает научные вопросы: каждый вмешивающийся contract имеет gate, каждая observed error — доступную альтернативу, каждый promote — independent comparison и target path. До результатов не назначаются численные epochs/trials/minutes и смешанный exhaustive factorial. Исходные численные примеры W1 сохраняют статус illustrative предложений их веток.

## E-процедуры следующей практической волны

**Общий contract C-E.** Все E — PROPOSED/не выполнены. До запуска exact model/task/repo/package/dependency/checkpoint hash получает model_stack либо фиксирует отсутствие как Q005/Q006; выдуманных CLI/weights нет. Data/ontology/coverage/roles/group independence фиксируются версиями Q001–Q004; lockbox не debugging/training/acquisition/calibration pool. OS/torch/CUDA/driver/GPU/VRAM — inventory; SDK/device обязателен для target части Q007–Q009. Если локальная E не задаёт numerical cap/margin, это незаполненный вход Q010/Q027 до trial по фактическому pilot, не неограниченный sweep.

Контроль сохраняет init/class rows/data/split/preprocess/postprocess/rules и заявленный estimand update/exposure/human-time; различия явно записываются. Artifacts: hashes data/config/dependencies/weights/input, отдельные sample/optimization/split/resampling seeds, raw outputs/logs, actual exposures/updates/time, immutable serialized selected checkpoint+reason. Outcomes: promote/kill/inconclusive/rollback, не обещанное улучшение. Любой successful gate ограничен этой реализацией/материалом; unseen cameras/rare events/event safety/LinQ без actual test не подтверждает. Точные дополнительные fields и stop/limit каждой процедуры ниже имеют приоритет. E W2 amendments объединены с исходной процедурой и не добавляют обязательный quality trial.

<a id="e001"></a>

### E001 — воспроизводимая zero-update baseline и выбор первой интервенции

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-01-E01.

**W1-01-E01: исходная процедура** ([ветка](_WORK/W1/01_BASELINE.md)):


**Решение:** можно ли оставить готовые веса; нужен ли data/pipeline fix или training. **Входы:** утверждённая task ontology; лицензированные target images/video и возможность ручного GT; пригодный checkpoint/config от model_stack; фактическое окружение. **Контроль:** weights неизменны; единый evaluation contract, отдельные diagnostic и assessment группы; зафиксированные правила и preprocessing.

**Действия:** (1) Записать manifest, проверить class map и несколько overlays actual model input. (2) Запустить исходные веса в reference runtime, сохранить raw detections и output contract. (3) Сопоставить с проверенной разметкой и разобрать проявления F001, а также связь с масштабом/видимостью. (4) Проверить спорные GT; исправлять данные только версионно. (5) Выполнить события с неизменными правилами. (6) Выбрать одно вмешательство, затрагивающее преобладающую подтверждённую причину; обучение — один из вариантов.

**Метрики:** object AP с явно названным IoU protocol, per-class precision/recall на зафиксированной operating point, TP/FP/FN и denominators по группам; отдельно event recall/false alarms и длительность наблюдения по протоколу evaluation. При отсутствии GT доступны лишь overlays, покрытие и гипотезы; численное target quality не заявляется.

**Артефакты:** dataset/split manifest с camera/session/time и label version, checkpoint hash, code/package version, полный config, raw predictions, actual input overlays, audit corrections с причинами, error table, event log, runtime identity. Не сохранять персональные данные в публичные отчёты без оснований и доступа.

**Исходы:** pipeline invalid → сначала fix и новая reference; labels invalid → audit и единый исправленный evaluation set; objects достаточны/events нет → E002; систематические object errors при видимом сигнале → targeted data + controlled training comparison; сигнал не установлен → E003. **Stop rule:** не начинать большой training при неверной таксономии, невалидных координатах или невозможности оценить target результат. Приёмка готовых весов — только по заранее заданным требованиям и реальному LinQ execution. **Предел:** reference CPU/RTX не подтверждает LinQ, diagnostic sample не доказывает перенос на все камеры.

<a id="e002"></a>

### E002 — локализация object против event ошибки

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-01-E02.

**W1-01-E02: исходная процедура** ([ветка](_WORK/W1/01_BASELINE.md)):


**Решение:** тратить усилия на detector training или на association/temporal logic. **Входы:** короткие диагностические clips с проверенным event GT, object evidence и идентичностями, требуемыми конкретным правилом; воспроизводимый rule engine. **Контроль:** один clip set, same timestamps/rules/zones; меняется только входная информация соответствующего этапа.

**Действия:** A — обычные detections → associations/tracks → events. B — вручную проверенные object boxes/classes на тех же кадрах → те же associations/tracks → events. Если B всё ещё ошибочен, C — проверенные associations/identity/zone evidence → те же temporal rules. Это ручная oracle-подстановка для диагностики, не заявка на production performance. Если интерфейс не позволяет такую подстановку, зафиксировать необходимые stage logs и выполнить структурированный ручной разбор; не заявлять выполненный B/C.

**Метрики:** paired перечень изменившихся event TP/FP/FN, event timing и причина каждого исправления/остатка. **Артефакты:** versions A/B/C evidence, rules, audit decisions, traces, overlays, timestamps. **Исходы:** A→B исправляет ошибки — object stage участвует, но конкретный способ обучения ещё неизвестен; B→C исправляет — association/track issue; C сохраняет ошибку — правило, постановка или event GT требуют проверки. **Stop rule:** если reference labels/identity спорны, прекратить причинную атрибуцию до согласования; не обучать detector ради ошибки, сохраняющейся при правильном object evidence. **Предел:** идеальные objects не гарантируют, что практический detector достижим; oracle не прогнозирует выигрыш AP или event quality.

<a id="e003"></a>

### E003 — тест наблюдаемости и потери сигнала при обработке

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-01-E03, W1-06-E01.

**W1-01-E03: исходная процедура** ([ветка](_WORK/W1/01_BASELINE.md)):


**Решение:** менять input/camera/context либо пробовать data/training. **Входы:** diagnostic positives/negatives, native frame и actual input representation, разрешение просматривать короткий temporal context, согласованная инструкция labeling. **Контроль:** один и тот же физический эпизод; фиксировать, какую информацию видел reviewer.

**Действия:** независимые reviewers при возможности помечают состояние и `unknown` на native frame, actual transformed input и разрешённом clip context. После первоначальных независимых решений обсуждают расхождения; записывают причины, размер объекта и occlusion. Не показывать model label до первичного решения. Это скрининг, не измерение Bayes error.

**Метрики:** counts согласий/расхождений/unknown по representation и условиям; object size distribution; дополнительно paired model results только после actual inference test. **Артефакты:** manifests views, audit form, instructions, disagreement log. **Исходы:** native различим/actual нет → input-scale branch; single frame нет/clip да → temporal context branch; даже clip спорен → task/camera/GT question. **Stop rule:** не расширять training только ради неустановимого target label; уточнить требуемое наблюдение. **Предел:** human disagreement не доказывает абсолютную невозможность model inference, agreement не доказывает достижимую точность. LinQ cost input/crops остаётся отдельным вопросом.

**W1-06-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W1/06_SCALE.md)):


**Входы:** целевые original decoded frames/видеокодек, timestamps, GT/class semantics, mapping независимых camera/session, исходный checkpoint от model_stack. **Контроль:** фиксированный audit subset, original и точный input tensor одного и того же кадра. **Действия:** измерить original/input object px distributions; вручную независимо оценить visible/occluded/ambiguous/unobservable; наложить GT после resize/letterbox и проверить coordinate round-trip. Отдельно размечать дым/руку/сигарету, если эти признаки действительно заданы кейсом. **Метрики:** доля positives с потерянным различимым признаком после resize, agreement аудита, размеры px, recall по bin и доля ambiguous. **Артефакты:** frame manifest, crop gallery, pixel histograms, original→tensor transform, reasons. **Исход:** если detail сохраняется в native crop, E016; если отсутствует в original, вопрос постановщику/violation_methods о наблюдаемости. **Stop:** не подбирать числовой «минимальный размер» по одному примеру; прекратить увеличение размера, если оно лишь интерполирует неразличимые pixels. **Предел:** аудит наблюдаемости не устанавливает достижимый AP и допустимость камеры.

<a id="e004"></a>

### E004 — head-only/limited freeze против full из одного checkpoint

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-02-E01.

**W1-02-E01: исходная процедура** ([ветка](_WORK/W1/02_FINETUNING.md)):


**Статус:** PROPOSED, не выполнено. **Решение:** сколько representation адаптировать при доступной целевой разметке. **Входы:** unfused training checkpoint с hash, версия trainer/YAML, полностью согласованный class map; полные annotations необходимых классов; независимые camera/session groups для development validation и закрытой assessment; базовая evaluation/event pipeline. Если нужный класс отсутствует в source outputs, сначала создать общий корректный target head для обоих training arms; неизменяемый source reference оценивать лишь на покрываемых им outputs и не называть его полноценным baseline нового класса.

**Контроль:** A — unchanged reference; B — ограниченная проверенная маска; C — full adaptation из того же target-initialized state, включая одинаковые случайно созданные class rows. Одинаковые train examples, transforms/input geometry, batch по возможности, optimizer family, checkpoint selection rule и evaluation postprocessing. Записать все различия. BN политика явно указана для каждого arm. Если native freeze меняет одновременно weights и BN stats, B/C измеряют комплексный режим, а не чистый причинный эффект числа весов.

**Действия:**

1. Сохранить source/target names, row mapping, transferred/skipped tensors, initialization seed и хеш общей стартовой target state; проверить labels/overlays.
2. После _setup_train сохранить named_parameters/requires_grad, число trainable elements, optimizer groups, normalization types, training flags, running buffers. Сравнить с ожидаемой маской. Проверить начало каждой эпохи и первый шаг: неизменяемые buffers/параметры действительно не меняются; trainable gradients и updates существуют. Это небольшой smoke test будущей практической волны.
3. Назначить заранее сопоставимый update/sample budget, а также отдельный wall-clock cap. Он не выбирается из цифр TFA. Для оперативного решения сохранить и качество при одинаковом числе предъявлений, и лучшее валидированное качество к deadline; эти два вопроса различаются.
4. Обучить B/C; выбирать checkpoint только на development validation. Если разница меняет решение и данные позволяют, повторить ключевую пару с другой initialization seed/группой few-shot примеров. Не выбирать лучший seed постфактум по assessment.
5. Однократно проверить выбранные кандидаты на независимом assessment; отдельно сравнить необходимые старые classes/условия, target классы и downstream events. Затем передать выбранный checkpoint на actual export/LinQ verification.

**Метрики:** per-class AP и recall при фиксированной operating point; base/novel и camera/condition groups; object FN/FP; сохранение нужных старых классов; training/validation gap. Ресурсы: peak allocated/reserved VRAM, input/batch, elapsed time и число optimizer updates. Event metrics берутся из согласованного evaluation contract, не подменяют object metrics.

**Артефакты:** все manifests/hashes/configs, стартовая target state, row map, фактическая freeze/BN mask, optimizer/LR trace, predictions, per-group metrics, last/best checkpoints и правило выбора, ресурсный log. **Исходы:** B/C одинаково полезны — сохранить более простой проверенный путь; C даёт устойчивое нужное улучшение — адаптировать feature layers; B лучше на независимых сценах — ограничить обновление; оба хуже reference — вернуть reference и проверить labels/representation/optimization, не удлинять прогон автоматически. Недостаточно независимых данных — результат preliminary. **Stop rule:** ошибочная маска/row mapping, невалидные labels, nonfinite loss или отсутствие проверяемого model update прекращают сравнение до исправления; исчерпание заранее заданного времени прекращает arm с сохранением checkpoint. **Предел:** наш target результат, если он появится, действует только для фактического протокола; reference runtime и export success не подтверждают LinQ.

<a id="e005"></a>

### E005 — различить влияние BN и обновления feature weights

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-02-E02.

**W1-02-E02: исходная процедура** ([ветка](_WORK/W1/02_FINETUNING.md)):


**Статус:** PROPOSED. Не обязателен до E004; нужен при малом batch, подозрении на drift статистик или различии результата train/eval. **Входы:** рабочий E004 и возможность менять trainer с логами. **Контроль:** одна trainable-weight mask, один initialization/data order и optimizer; меняется только политика BatchNorm2d running statistics: fixed source stats против target updates. Affine parameters и остальные normalization types фиксируются одинаково. В native Ultralytics freeze fixed-stats поведение уже встроено для совпавших BN (F014); второй arm требует явной проверенной модификации, готового штатного флага эта ветка не установила.

**Действия:** снять running_mean/var/num_batches_tracked до/после; убедиться в неизменности affine/weight mask; выполнить ограниченную paired adaptation; оценить оба checkpoint в одинаковом eval и на одинаковых inputs. **Метрики:** изменение BN buffers, целевые per-class/per-camera quality и старые условия, batch composition/размер; отдельно воспроизводимость predictions. **Артефакты:** trainer diff, normalization inventory, buffer deltas, configs, predictions. **Исходы:** target updates помогают на независимых target groups без неприемлемого ущерба — кандидат; ухудшают/нестабильны — fixed stats; различия малы — не усложнять режим. **Stop rule:** случайно изменилась mask/augmentation либо BN фактически работает иначе ожидаемого — comparison invalid. **Предел:** это тест одной реализации и данных; не доказывает общую полезность Adaptive BN, не устанавливает cross-camera перенос и не разрешает использовать assessment video для adaptation.

<a id="e006"></a>

### E006 — полезна ли малая полная разметка и устойчив ли выигрыш

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-03-E01.

**W1-03-E01: исходная процедура** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):


**Гипотеза/решение:** проверить, даёт ли доступная независимая малая разметка полезное обобщение; выбрать full/head-only/дополнительные labels. **Модель:** model_stack должен назвать repo/commit/checkpoint/hash, class map, фактический head-only interface и export target. При новом классе заранее согласовать predictor expansion и initialization; unchanged checkpoint без класса не становится полноценной new-class baseline.

**Данные/среда:** проверенная ontology; полностью проверенные для нужных классов target images, episode/camera/session metadata; annotation work pool, validation для выбора checkpoint, независимый assessment по группам. Не задаём заранее число кадров/VRAM. Нужны training environment и доступ к licensed data, по необходимости CPU/RTX/cloud после отдельного практического запуска.

**Контроль/действия:** заморозить preprocessing, augmentation, class map, loss, event rules и evaluation contract; создать несколько matched subset manifests по независимым groups, считать instances и scenes отдельно. В каждом subset сравнить предусмотренные режимы с явно записанными trainable tensors, одинаковым checkpoint-selection rule и отдельно указанным budget. Нельзя молча уравнивать epochs, wall-clock и updates: выбрать, какую стоимость сравниваем, и измерить остальные. После первого существенного сравнения повторить на другом sample subset; optimizer seed — отдельный фактор. При выборе доразметки сравнить следующую порцию независимых labels с дополнительным training budget существующего набора, записав human time.

**Метрики:** per-class AP с названным IoU protocol, precision/recall, base/novel AP при осмысленном делении, FP/FN по размеру/камере; paired delta по subsets, event measures отдельно; compute wall-clock/memory/human time измеряются. **Артефакты:** split/subset/annotation versions, sample and optimization seeds, pretrained/checkpoint hashes, tensors frozen/unfrozen, config, selected checkpoint reason, raw predictions, metrics и overlays. **Исходы:** устойчивое улучшение → кандидат для integration; ухудшение base → проверить mixing/баланс без сокрытия регрессии; зависимость от sample selection → расширить независимые labels/ограничить claim; отсутствие выигрыша → audit signal/coverage/domain. **Stop rule:** невалидный split/GT или отсутствие нужного визуального сигнала блокируют причинный вывод; не наращивать прогоны ради удобного seed. **Предел:** небольшой успех не доказывает перенос на новую камеру, event completeness, LinQ или достаточность любого K-shot бюджета.

<a id="e007"></a>

### E007 — сохраняет ли trainer partial-label semantics

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-03-E02, W2-02-E01.

**W1-03-E02: исходная процедура** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):


**Гипотеза/решение:** не штрафует ли pipeline скрытые positive objects как background; можно ли использовать source mixture без доразметки. **Входы:** один зафиксированный checkpoint/trainer от model_stack, малый полностью проверенный diagnostic набор с несколькими instances одного класса и несколькими classes; оригинальные полные labels; spatial ignore/class coverage metadata. Assessment остаётся полностью размеченным и отдельным.

**Контроль/действия:** до длинного обучения создать три версионные copies train labels: A полные; B скрыт весь один class; C скрыт один из нескольких instances уже present class. Зафиксировать фактический mapping этих регионов на proposals/anchors/queries и loss terms. Сравнить обычный loader и предлагаемый partial mechanism с одинаковым input и assignment logs; отдельно проверить classification/objectness/RPN/regression/normalization, а не только sum loss. Для synthetic test скрытый GT доступен аудитору, но не training branch. Проверить пустой label image и сохранение metadata после export/import annotations. Не объявлять mask working только потому, что loss уменьшился. После correctness audit возможен небольшой controlled A/B/C learning comparison по общей E006; это новый практический шаг, не выполненный здесь.

**Метрики/артефакты:** per-region/per-class assignment, mask и loss contributions; gradients по соответствующим logits при доступности, mapping оригинального GT → скрытого/сохранённого, coverage counts, complete-assessment quality после прогона. Сохранять commit/config/seed/tensor diagnostics и visual overlays. **Исходы:** class mask работает в B, но не C → не использовать как random missing-box solution; loss mask работает, objectness нет → интеграция неполна; loader теряет metadata → исправить путь данных; всё проходит → измерять практическую пользу, не считать её доказанной. **Stop rule:** невозможность сохранить coverage или локализовать false-negative supervision → доразметка/отдельная задача вместо неподтверждённого union. **Предел:** искусственное удаление boxes не воспроизводит неслучайные реальные пропуски tiny/occluded objects; correctness loss не доказывает качество.

**W2-02-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)):


**Вопрос/решение:** implementation действительно устраняет выбранный false-negative path B/C, сохраняя known positive supervision, либо следует выбрать доразметку/separate task. **Входы:** checkpoint hash, repo/SHA, loaded head type и reg_max/end2end; оригинальный полностью размеченный diagnostic набор E007, versions A/B/C и mapping hidden→original IDs; class coverage/ROI metadata; custom mechanism только если он реально подготовлен отдельной практической работой. Нужны отдельный fully annotated assessment и выбранный training environment; LinQ не нужен для проверки loss, но нужен позже для итогового artifact.

**Контроль:** fixed predictions либо identical forward/checkpoint/input/preprocessing для локализации; сначала отключить composite augmentation явными настройками конкретного pin, затем отдельно проверить каждую планируемую composite transform. Не сравнивать sum loss как доказательство mask correctness. Hidden GT доступен аудитору, **не training assignment**; если production method использует ignore geometry, для этого test geometry должна быть явно передана как собственный вход, а не украдкой восстановлена из auditor GT.

**Дополнительные действия/observables к существующему E02:**

1. Сохранить post-loader/post-transform `cls/bboxes/batch_idx` и coverage/ROI keys с типами/shapes; счётчики missing/empty. Отдельные variants: all-empty batch, одно empty image в mixed batch, only-ignore/no-regular-GT и overlapping known-positive+ignore. Последний нужен для person/helmet geometry, не для доказательства wearing.
2. Для **каждой** U E2E branch записать raw scores/decoded boxes, candidate membership с tiny-box expansion, `mask_pos` before/after conflicts/topk2, `fg_mask`, `target_gt_idx`, `target_scores`, denominator, validity masks, BCE до weighting/reduction и box/DFL/L1 contributions. Logs только one2one недостаточны. Отделить fg assignment другого retained GT от true hidden-only background.
3. Проверить invariants chosen contract: ignored zero-target class entries не участвуют; kept positive class entries и корректные bbox targets не blanket-masked; verified negatives вне unknown scope остаются. Если intentionally conservative policy убирает все negatives c, явно посчитать потерянное support. A/B/C denominator/assignment различия сохранить, не объявлять все различия implementation defect.
4. Для legacy v5 дополнительно layer-wise `tobj`, BCEobj unreduced + validity, class-positive indices и cls targets, autobalance/reduction. Для MMDet дополнительно regular/ignored instances после PackDetInputs, RPN и RoI `gt_inds`, sampled pos/neg, label/bbox weights; обязательно воспроизвести zero-regular-GT counterexample и проверить фактически выбранный replacement/filter policy.
5. В практическом execution этапе E02 проверить gradients соответствующих logits **до zero_grad**, known positive regression и сохранение/reload criterion/config. Zero ignored gradient при ненулевом остальном loss — полезный correctness observable; нынешний отчёт его не измерял. Лишь после passage допустим learning comparison E006 с full assessment, matched data/budget/selection и отдельным учётом annotation/engineering time.

**Метрики/артефакты:** named tensor dumps/array shapes, post-transform overlays, per-class/region negative/positive participation counts и loss contributions, gains/normalization, branch IDs, metadata round-trip diff, config/code/data/checkpoint hashes; при execution — gradient diagnostics и optimizer update boundary. **Исходы:** B проходит, C нет → применять только источник с class-level unknown/exhaustive own instances; v5 objectness продолжает штрафовать → механизм неполон; only-ignore fails → фильтр/другая implementation до training; metadata lost → data gate failed; всё проходит → проверить пользу на независимом полном GT. **Stop:** первый необъяснённый false-negative contribution или исчезновение correct positive, отсутствие нужной geometry/coverage; не запускать длинное обучение для компенсации ошибки. **Предел:** искусственное deletion не воспроизводит selection bias tiny/occluded labels; correctness не доказывает качество, event metrics, export или LinQ.

<a id="e008"></a>

### E008 — стоимость sparse-method inference и выбор доразметки

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-03-E03.

**W1-03-E03: исходная процедура** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)):


**Гипотеза/решение:** оправдана ли интеграция специального SAOD метода относительно маленького полностью проверенного набора. **Входы:** E007 прошёл; candidate pinned implementation, dependencies, weights и допустимые данные; для SparseDet — конкретный C-RPN path и режим views, для Co-mining — подтверждённый single-branch artifact; reference student/output contract. Доступность archive по URL ещё не означает эти входы.

**Контроль/действия:** сначала read/shape trace итогового eval graph и сравнение input/output со стандартной baseline; затем только при фактической совместимости — минимальный inference/export smoke check. Для SparseDet сравнить original/augmented и no-augmentation режимы при неизменных weights; не удалять C-RPN, называя это опубликованной абляцией. Сопоставить sparse-trainer intervention с качественной доразметкой при записанных annotation и engineering costs. LinQ compiler/runtime — отдельный фактический доступ/тест.

**Метрики/артефакты:** graph/operators/input count, число backbone passes, actual preprocessing, peak memory/latency при названной среде, raw detections и paired object quality, conversion logs, checkpoint+export hashes; human/integration time. **Исходы:** unsupported graph/избыточная сложность → simpler fine-tuning с полными labels; совместимость и quality gain → кандидат на LinQ validation; no-aug parity → выбрать простой из проверенных режимов, сохранив C-RPN contract. **Stop rule:** не тратить длительное обучение до подтверждения исполнимого output path; если дополнительная разметка снимает проблему быстрее в измеренной среде, закрыть сложную ветку. **Предел:** smoke check одного runtime не доказывает LinQ, streaming throughput или пригодность тревог.

<a id="e009"></a>

### E009 — установить, какой дисбаланс существует

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-04-E01.

**W1-04-E01: исходная процедура** ([ветка](_WORK/W1/04_IMBALANCE.md)):


- **Решение/гипотеза:** sampling полезен, только если исходная нехватка экспозиции отличается от нехватки независимых визуальных примеров.
- **Входы:** versioned train annotations, source/camera/session/time, возможность выделить episode/track; исходный checkpoint и fixed preprocessing от model_stack. Отдельно замороженные validation и lockbox, разделённые по подходящим независимым группам.
- **Действия:** посчитать четыре вида покрытия F045; вручную проверить редкие/нулевые классы, near-duplicates и label completeness. Без обучения построить ожидаемые и фактические class/group exposures из выбранного sampler с фиксированным seed. Проверить empty frames на выходе loader.
- **Контроль/метрики:** натуральная очередь против кандидата; image/instance/group frequencies, повторения на episode, доля background, доля камер и sources. Прогнозируемый RFS — формула S022, не выдуманный CLI-флаг.
- **Артефакты:** split manifest, class map, histogram, список groups, factors, sampled indices/seed, примеры labels и список исключений.
- **Исходы:** если RFS не меняет ничего — выбирать threshold по реальной частоте или отказаться; если усиливает один эпизод — доразметка независимых сцен/group cap; если rare positives неверны — исправлять labels раньше loss.
- **Stop rule:** нет надёжной семантики/group metadata или отсутствуют positives — остановить подбор balancing parameters до устранения причины.
- **Предел:** правильные exposures не подтверждают generalization и false alarms.

<a id="e010"></a>

### E010 — один контролируемый balancing trial

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-04-E02.

**W1-04-E02: исходная процедура** ([ветка](_WORK/W1/04_IMBALANCE.md)):


- **Решение/гипотеза:** умеренное усиление недостаточно представленных классов улучшает независимый rare recall при допустимой цене частым классам/FP.
- **Входы:** результаты E009, согласованные критичные классы и допуски; checkpoint/version/trainer от model_stack. Для Detectron2 — pinned RFS; для Ultralytics — сначала проверить локальное наличие S013, S025. Эти стеки — альтернативы, не сопоставимая архитектурная абляция.
- **Сравнение:** baseline natural sampler + default loss против **одного** кандидата: RFS с обоснованным threshold либо `cls_pw>0` в диапазоне поддержки. Начальные значения — гипотеза после histogram, не универсальный рецепт. В обеих ветках одинаковые train split, initialization, augmentation, input size, update budget, scheduler и checkpoint-selection criterion; зафиксировать seed и hash labels.
- **Действия:** короткий пилот на проверку labels/loaders/gradients, затем ограниченный paired training. Проверить сырые per-class predictions при одинаковых postprocessing settings; отдельно построить PR/recall при согласованной FP-нагрузке. Порог выбирать по validation одинаковой процедурой, не по lockbox.
- **Метрики:** per-class box AP50:95 (или фактическая метрика кейса), critical recall, frequent-class degradation, PR, FP/hour после fixed event logic; время, updates, exposures. Показать знаменатели независимых positives и negative camera-hours.
- **Артефакты:** оба config, versions, seeds, input/split hashes, sampler trace/weights, logs, validation predictions, checkpoint selection и checkpoint hash.
- **Исходы:** выигрыш при выполненных допусках — проверить ключевую пару на другом seed/независимой группе по доступному бюджету; выигрыш только train/familiar scene — возвращаться к данным; recall↑ и FP↑ — смотреть PR и operating point, не объявлять победу по одному recall.
- **Stop rule:** вред критичному классу/FP выше заранее назначенного допуска; ненадёжная разметка; отсутствие улучшения на полезной независимой группе. Не запускать широкую сетку t/gamma/alpha только из-за наличия GPU.
- **Предел:** даже повторение пары не устанавливает качество на неизвестной камере, после quantization или на LinQ.

<a id="e011"></a>

### E011 — hard negatives против такого же объёма обычной доразметки

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-04-E03.

**W1-04-E03: исходная процедура** ([ветка](_WORK/W1/04_IMBALANCE.md)):


- **Решение/гипотеза:** конкретные look-alike ошибки устраняются targeted negatives эффективнее, чем случайными новыми кадрами того же человеческого бюджета.
- **Входы:** замороженный baseline, отдельный разрешённый mining pool, список причин FP, аннотатор; independent negative validation и positive event set. Lockbox не участвует в mining.
- **Действия:** baseline inference на mining pool; группировка FP по эпизоду и причине; проверка F047; фиксированный quota по типам. Сравнить baseline, добавление проверенных hard-negative кадров и контрольное добавление разнообразных обычных кадров при сопоставимом annotation effort. Все рабочие классы на добавленном кадре должны быть полностью размечены либо корректно ignored поддержанным loader. Не добавлять выдуманный класс `background` в bbox taxonomy.
- **Контроль/метрики:** одинаковый checkpoint/update budget/positive exposure; FP по причинам и на час нормального видео, rare/critical recall, precision на выбранном validation threshold; human minutes и число независимых новых scenes. Mining-pool FP — диагностическая метрика, а не independent результат.
- **Артефакты:** mining model hash, prediction dump, candidate/review decisions, reason taxonomy, annotations, dedup/group manifest, configs/checkpoints и paired predictions.
- **Исходы:** перенос на новые negative episodes без потери recall — принять данные; эффект только на mining scenes — расширить причины/домены; потеря recall — проверить false-negative labels, quotas и экспозицию positives; недостаток визуального сигнала — передать violation_methods.
- **Stop rule:** mining поставляет преимущественно дубликаты/неоднозначные cases; трудозатраты не дают новых причин; ухудшение critical recall; ложные тревоги определяются другой event logic.
- **Предел:** не доказывает универсального эффекта OHEM и не устанавливает реальную prevalence всего deployment.

<a id="e012"></a>

### E012 — semantic/data-pipeline gate до обучения

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-05-E01.

**W1-05-E01: исходная процедура** ([ветка](_WORK/W1/05_AUGMENTATION.md)):


Вопрос: действительно ли candidate transform действует и сохраняет пригодную разметку? Входы: pinned model/trainer/package lock, train-only изображения с boxes и необходимыми relations/ROI, annotation policy. Включить редкие и маленькие объекты, кадры с частичной видимостью и пустые кадры. Validation/test в training pipeline не подмешивать.

Действия (псевдопроцедура, без выдуманного trainer API): зафиксировать seed и список train IDs; получить before/after из настоящего dataloader для каждой группы отдельно и для полной композиции; сохранить transform parameters/replay, overlays, bbox/class/association arrays. Сопоставить ID объектов до/после. Проверить диапазон/формат координат, label alignment, clipping, пустые targets и отсутствие ошибки при реальном использовании. Для spatial custom transforms сохранить startup log: успешный import недостаточен.

Метрики: survival и удаление labels по классу/исходной pixel area; доля кадров без targets; invalid coords; ручное число semantic failures, где исчезло evidence или сломалась связь. Артефакты: package versions, config, seed, sample manifest, overlays и список причин отказа. Stop rule: не начинать дорогой trial при воспроизводимой геометрической/семантической ошибке; уменьшить strength, исключить transform или определить ignore-policy. Нулевая найденная ошибка на выборке разрешает ablation, но не доказывает глобальную корректность и не измеряет качество модели.

<a id="e013"></a>

### E013 — минимальная содержательная ablation

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-05-E02.

**W1-05-E02: исходная процедура** ([ветка](_WORK/W1/05_AUGMENTATION.md)):


Входы: один подходящий pretrained checkpoint, фиксированный train/validation split по camera/session или независимым клипам; одинаковые classes, labels, imgsz, batch/optimizer/compute budget, seed, checkpoint-selection rule и inference thresholds. Заранее определить critical-class metric и допустимое ухудшение clean slice вместе с evaluation, без выдуманного численного порога сейчас.

Контроли: (B0) текущий воспроизводимый default recipe с явной фиксацией optional Albumentations; (B1) согласованный conservative recipe с выключенными mix-операциями/ненужной геометрией. B1 является кандидатом, не установленно лучшим baseline. Далее относительно выбранного фиксированного контроля: (P) одна фотометрическая группа; (D) compression/blur группа; (G) небольшая геометрия/scale, только если E012 допускает; (M) mosaic отдельно; mixup и occlusion только после конкретной гипотезы ошибки. Не запускать сразу полный factorial grid. Для редких classes главный вопрос — улучшение на независимых видимых instances, а не средний train loss.

Наблюдения: per-class AP/recall и precision при фиксированной рабочей настройке, размерные bins PPE, clean/degraded и camera slices, critical misses, ложные тревоги на независимом видео с фиксированным event logic; измерить epoch/wall-clock cost. Для suppression conf/NMS оставить одинаковыми. Если inference threshold позже настроен отдельно, это отдельное вмешательство.

Артефакты: diff конфигов, manifest/checksums данных, seed, versions, checkpoint selection log, prediction files, per-slice metrics и before/after error examples. Исходы: устойчивый useful gain → сохранить candidate; только synthetic-corruption gain без real-camera gain → исследовать mismatch, не объявлять внедрённым улучшением; потеря clean/critical class → ослабить или отвергнуть. Stop rule: не расширять группу при broken E012 либо ухудшении заранее согласованного critical gate; ключевой выигрыш повторить на другом seed/независимой группе, если size/variance делают выбор неустойчивым. Один trial подтверждает только этот split/seed/budget; совместимость LinQ остаётся отдельной.

<a id="e014"></a>

### E014 — проверить маленький объект и фильтрацию

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-05-E03.

**W1-05-E03: исходная процедура** ([ветка](_WORK/W1/05_AUGMENTATION.md)):


Входы: train subset с маленькими PPE/сигаретами, сохранённый размер после resize/letterbox, pinned source F054/F059. Контроль: та же модель/входной размер без добавленной spatial augmentation. Действия: отдельно включить scale/crop/mosaic, вывести распределения размеров и survival; вручную сопоставить исчезнувшие/оставшиеся labels. Не менять библиотечный filter ради формального роста survival, пока не установлена visual labelability.

Метрики: survival small-instance/class, доля evidence-erased-but-label-retained, per-class small recall на untouched real validation, стоимость загрузчика. Артефакты: object-ID table, overlays на границах фильтра, config/code revision. Исходы: labels исчезают массово → уменьшить strength или пересмотреть масштаб наблюдения с W1-06; видимость утрачена без фильтрации → semantic gate/ignore, не синтетическое `no_PPE`; размеры сохранены, real recall не вырос → прекращать эту ветку. Stop rule: после обнаружения систематического удаления критичного класса прекратить длительный training candidate до коррекции. Это проверяет pipeline и конкретную гипотезу, не устанавливает минимальный детектируемый размер любой модели.

<a id="e015"></a>

### E015 — clean / real degraded / controlled corruptions

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-05-E04.

**W1-05-E04: исходная процедура** ([ветка](_WORK/W1/05_AUGMENTATION.md)):


Входы: независимое реальное validation-видео разных освещений/качества с проверенными labels; от train отделено до аугментаций. Если реальных плохих условий нет, добавить контролируемые corruptions как диагностический secondary set, явно с общими original IDs. Контроль: clean originals с тем же preprocessing. Метрики и артефакты E013 плюс severity, тип transform/codec, camera/session IDs и парные predictions. Не считать corrupted copies независимыми observations.

Исход: synthetic robustness без подтверждения на реальном потоке оставляет transfer открытым; деградация clean запускает trade-off review; выигрыш real target подтверждает лишь представленные режимы. Stop rule: прекратить подбор strengths по lockbox; фиксировать strengths по train/validation, окончательный test использовать после выбора. Проверка кадра не подтверждает event-level false alarms или temporal robustness.

<a id="e016"></a>

### E016 — контролируемая resolution/tiles абляция

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-06-E02.

**W1-06-E02: исходная процедура** ([ветка](_WORK/W1/06_SCALE.md)):


**Входы:** frozen checkpoint+hash, полностью проверенная full-frame GT, исходные video/session splits до нарезки, validation/lockbox, runtime вне/на LinQ по отдельным стадиям доступа. **Контроль:** общий scorer/GT/maxDets/ignore/threshold-selection contract из F082. Начать без fine-tuning: A full-frame штатный размер; B один больший подтверждённый input; C tiles без FI; D те же tiles+FI. Один небольшой tile/overlap набор выбирается по E003; размеры — гипотезы, не рекомендованные defaults. Merge фиксировать явно, не полагаться на F075 auto switch.

**Действия:** сохранить predictions в исходных координатах; посчитать per-class AP50 и AP50:95, recall/precision на согласованном operating point, original-size bins и контекстные подгруппы; учесть border/duplicate/large-object errors; измерить всё из F081, F082. **Артефакты:** configs/hashes/input shape, tile origins, raw/merged predictions, CPU/device/runtime version, warmup/synchronization/timestamp contract, latency traces, gallery discordant pairs. **Исходы:** gain без приемлемой системной цены не принимается; отсутствие gain закрывает slicing данной модели/камеры, а не весь метод. **Stop:** прекратить расширение grid при нарушении согласованного latency/memory/calls budget либо если improvement исчезает на независимой session. **Предел:** удачный результат на RTX/CPU не подтверждает LinQ, inference gain не доказывает training gain.

<a id="e017"></a>

### E017 — локализовать ошибку person/head каскада

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-06-E03.

**W1-06-E03: исходная процедура** ([ветка](_WORK/W1/06_SCALE.md)):


**Входы:** frames с полным GT, parent person/head boxes и связями к PPE/событию, реальные stage1 predictions; stage2 checkpoint. **Контроль:** одинаковый stage2 и crop margin/resize, одинаковый scorer и негативные кадры. **Действия:** сравнить GT/oracle crops, GT crops с измеренной по validation jitter моделью, predicted crops; затем полный cascade с upstream miss accounting. Sweep margin лишь на validation; сохранять закадровый padding и clip policy. Oracle subset не подменяет end-to-end test.

**Метрики:** usable-crop coverage, stage1 recall, crop inclusion/containment, stage2 conditional recall и end-to-end recall/precision; FP/video-hour и event delay при наличии событийного GT; errors miss-parent/miscenter/context/association; costs от0 до crowded max crops/frame. **Артефакты:** parent-child IDs, crop origins, upstream misses, score/threshold manifest, per-frame invocation traces. **Исход:** oracle good/predicted bad→исправлять локализацию/coverage; оба bad→данные/семантика/сигнал/stage2; crop good/event bad→контекст/правила. **Stop:** reject cascade, если coverage ceiling ниже нужного recall или системный бюджет нарушен; budget и target recall ещё должны быть заданы. **Предел:** хороший oracle тест не доказывает deployment; хороший person detection не подтверждает head/PPE localization.

<a id="e018"></a>

### E018 — нужно ли scale-matched обучение?

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-06-E04.

**W1-06-E04: исходная процедура** ([ветка](_WORK/W1/06_SCALE.md)):


**Входы:** победившая/перспективная E016/E017 preprocessing схема, проверенный trainer и dataset. **Контроль:** тот же исходный checkpoint, исходные изображения/GT/split, comparable optimizer updates/exposures и seeds; явно учесть, что crops увеличивают число примеров. **Действия:** A original-frame fine-tune; B original+train crops с negatives и audited truncation; обе модели оценивать одним фиксированным inference режимом. Отдельно при необходимости factorial training crop × inference crop, чтобы разделить эффекты. Multi-scale только при подтверждённой реализации и отдельной ablation; не имитировать SNIP простым random resize. **Метрики/артефакты:** E016 metrics + train exposures/iterations/wall-clock, crop GT audit, dataset/config/checkpoint hashes и checkpoint-selection rule. **Исход/stop:** принимать лишь independent gain, не ухудшающий критичные classes/context; если negatives/labels некорректны — остановить до исправления. **Предел:** не доказывает export/quantized equivalence, SDK compatibility или value на другой камере.

<a id="e019"></a>

### E019 — Target fine-tuning или source+target mixing

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-07-E01.

**W1-07-E01: исходная процедура** ([ветка](_WORK/W1/07_DOMAIN.md)):


**Гипотеза / решение:** source replay помогает сохранить старые камеры, но может мешать target; сравнить с target-only прежде, чем внедрять adversarial trainer.

**Входы:** проверенный model/checkpoint/version от model_stack; target train с исчерпывающей разметкой, class-map source/target, source train с правами использования, selection validation и old-domain retention, полностью скрытые new-session/new-camera группы. Если source недоступен — оставить только frozen и target-only; это другая процедура сравнения, без утверждения об эффекте mixing.

**Контроль:** один initialization, head, preprocessing/resolution, augmentation family, optimizer, total update budget, seeds, validation schedule и NMS. Основная сетка — frozen baseline; продолжение source-only на том же update budget; target-only; mixing с заранее заданной долей target (например0.5) плюс один target-heavy вариант (например0.75). Эти доли — проект эксперимента, не paper-recommended optimum. У всех обучаемых кандидатов зафиксировать число source/target exposures и уникальных групп; mixing при фиксированных updates меняет target exposure, что является частью вмешательства. При спорном результате сделать отдельный exposure-matched контроль, не объявляя его тем же cost-matched опытом.

**Действия:** проверить loader/class coverage; выполнить небольшой controlled run; выбрать checkpoint только по selection validation; разложить ошибки по классам, размеру объектов, камерам и освещению. На независимый test выпускать только выбранного кандидата и frozen baseline. До старта согласовать target primary metric и допустимую потерю old-camera качества; event metrics рассчитывать при одинаковых правилах событий.

**Метрики:** detection AP с явно фиксированным IoU convention; critical-class recall при фиксированном приемлемом FP уровне либо FP/hour при фиксированном recall; old-domain delta; per-camera/session paired delta; unique groups, annotations/объекты, GPU wall-clock и ручные затраты. Если event labels отсутствуют, не выдавать detection FP за FP/hour события.

**Артефакты:** split manifest с ролями и hashes; class mapping/annotation coverage; resolved config; checkpoint и selection criterion; seeds; exposure counts; логи; prediction files на одних и тех же кадрах; ошибки old/target; environment versions.

**Исходы / stop rule:** mixing выигрывает target и соблюдает retention gate — оставить; target-only выигрывает без запрещённого forgetting — выбрать его; выигрыш находится только на адаптационных кадрах — считать memorization/leakage warning, вернуться к группировке. Остановить ветку при нарушении semantics/labels, критическом падении класса, превышении заранее установленного integration/training budget, либо отсутствии целевого улучшения сверх выбранного practically meaningful threshold после запланированной сетки. Не продолжать ratios до случайного попадания в validation. Положительный результат ещё не подтверждает LinQ, unseen site, rare class reliability или устойчивость ко всем сменам камеры.

<a id="e020"></a>

### E020 — UDA / source-free целевое видео

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-07-E02, W2-07-E01.

**W1-07-E02: исходная процедура** ([ветка](_WORK/W1/07_DOMAIN.md)):


**Гипотеза / решение:** дополнительное неразмеченное target видео может дать полезное обучение только если исходный detector покрывает нужные классы и pseudo-label noise контролируем. Цель — решить, стоит ли тратить ресурсы на этот путь вместо ручной разметки.

**Входы:** frozen source model с revision/classes; adaptation pool из отдельных target sessions; доступ к source для UDA либо явно source-free setting; небольшой ручной аудит pseudo boxes внутри adaptation pool и independent labeled selection validation. Если даже independent labels нет, эксперимент ограничен feasibility и аудитом, улучшение качества не подтверждается. Потребны trainer/plugin code review и измерение фактической памяти/скорости; RTX4070 конфигурация неизвестна.

**Контроль / действия:** сравнить frozen baseline с audited offline self-training. UDA AT-подобный вариант добавить лишь после прохождения implementation gate: два loader streams, augmentation bbox correctness, source loss, teacher EMA и checkpoint extraction. Source-free не имитировать занулением source loss AT; выбрать отдельную проверенную реализацию или отказаться от сложной ветки. В первом пилоте не использовать online test-time updates. На случайном и failure-oriented audit проверить precision, missed GT objects, class frequencies, object sizes и пустые кадры, включая negatives. Не маркировать все области вне pseudo boxes достоверным фоном без разбора loss. Не использовать validation/test для mining.

**Метрики / артефакты:** те же независимые detection/event gates, что E019; отдельно pseudo-label precision/recall на аудите, доля кадров без labels, class coverage, class/size distribution shift, FP/FN examples, teacher/student selection, integration time. Сохранить parent checkpoint, raw predictions, threshold policy, teacher version, provenance каждого pseudo-label и человеческую правку. Entropy/confidence записываются как diagnostics, а не accuracy.

**Исходы / stop rule:** если pseudo-label audit показывает систематические пропуски критичного класса, не повышать только confidence threshold; направить эти случаи на доразметку/другой teacher. Если независимо выбранный adapted model хуже frozen по критичной метрике либо удачный aggregate скрывает недопустимое падение камеры/класса — откатить. Остановиться после заранее ограниченного числа циклов self-training без независимого выигрыша или при превышении integration budget. Положительный результат доказывает пользу только для данной модели, размеченных условий и протокола exposure, а не автоматическое распознавание неизвестных классов или совместимость LinQ.

**W2-07-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)):


**PROPOSED, не выполнено.** Не новая обязательная сетка. Решение: заслуживает ли этот legacy Faster R-CNN route quality trial по сравнению с frozen detector и небольшой supervised веткой. Если рабочая модель YOLO и нет соответствующего author port, не тратить время на перенос только ради SFOD.

**Входы/gates до очереди:** разрешённый кейсом adaptation pool U; exact checkpoint hash, config/P/dependencies, class order/semantics; usable source detector в этой architecture; проверенная infer/export feasibility; независимые группы A (полностью размеченный audit внутри adaptation domain), V (размеченные отдельные sessions для selection), H (закрытые new-session/new-camera groups); old-domain holdout R только если требуется retention и доступ разрешён. A/V/H роли не смешивать. U включает только разрешённые train images. При отсутствии V разрешён correctness/audit pilot, но не quality selection по proxy.

**Порядок будущего smoke, процедурный псевдокод:**

1. Получить frozen predictions с обычным eval, проверить неизменность всех parameters и BN buffers. Не использовать активный `train_net.py --eval-only` как frozen оценку. Сохранить исходную модель отдельно.
2. На копии модели выполнить явно ограниченный AdaBN по U; проверить отсутствие optimizer updates, state diff только ожидаемых BN buffers, порядок/число exposures. Не вызывать source train loader или ValLossHook на R/V/H. Сопоставить режим сброса statistics с задуманной процедурой; не выдавать1401 shuffled batches за полный pass.
3. Export predictions по U, явно фиксируя class map, NMS/cutoff; конвертировать в отдельный pseudo JSON. Проверить IDs/categories, bbox format, required COCO metadata, images с нулём retained boxes. Хэш/провенанс подтверждают, что train loader не читает target GT. На A полностью проверить не только accepted boxes, но все пропущенные objects/negatives; A не становится H.
4. Проверить loader/strong aug, BGR/RGB/dtype, small-box survival, empty-pseudo handling и actual freeze/BN mask; импорт YOLOX/debug-write issues — engineering gate. Снять отдельные RPN/RoI cls/reg losses и expected gradients; обычный pseudo JSON может наказывать пропущенные positives. Если аудит неприемлем, перейти к полной ручной коррекции, а не только повышать cutoff.
5. Только после gate разрешить один ограниченный quality comparison: B0 frozen; B1 small fully corrected supervised subset из train-role групп; B2 chosen fixed-pseudo source-free candidate. B1 — явная альтернатива с другой ценой labels, не «unsupervised победитель». Сохранить одинаковый initializer/model/input/inference settings; считать human minutes, unique groups, labels, exposures, training/integration/validation/export time. AdaBN-only как диагностический arm добавлять лишь если BN причина действительно остаётся открытой (reuse E005), не обязательный trial.
6. Selection checkpoint/threshold/budget только по V и заранее согласованной constrained metric; если V labels используются, так и назвать target-supervised selection. Окончательно выбранный model+BN state заморозить, затем один H evaluation против B0. Одинаковые detector postprocessing/event rules; при event labels — event recall/FP per hour, иначе только detection metrics с явным IoU. Проверить per-class/per-size/per-camera recall/FP и R при наличии. Reload predictions parity, затем actual export/target quality gate.

**Артефакты:** source/BN/pseudo/final hashes; repo/dependency lock и исправления entrypoint; resolved configs; split/exposure manifests; pseudo raw scores+JSON+accepted/rejected counts; A GT и ошибки; buffer/weight/gradient deltas; checkpoint iteration/selection reason; V/H predictions; actual time/human minutes; final detector and exporter contract.

**Stop/rollback:** incompatible ontology/weights, hidden GT или source exposure, изменение H/BN при eval, неправильные IDs/geometry, необработанные empty batches, критичный pseudo recall failure — остановить до качества. Если quality gate на V не проходит или путь не успевает дать reviewable artifact в отведённый integration budget — B0/B1, без поиска удачного proxy/checkpoint на H. Положительный H исход поддержит только этот protocol/модель/группы; не доказывает arbitrary new-camera gain, отсутствие source forgetting без R, безопасность редких событий либо LinQ execution без actual test.

<a id="e021"></a>

### E021 — Что именно переносится на новую камеру

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-07-E03.

**W1-07-E03: исходная процедура** ([ветка](_WORK/W1/07_DOMAIN.md)):


**Вопрос / решение:** нужен ли новый detector checkpoint на каждой камере, либо большая часть ошибки относится к scene rules/preprocessing.

**Входы и контроль:** минимум две камеры либо одна камера в нескольких независимых sessions; общий class semantics, frozen baseline и лучший E019/E020 кандидат. Если cameras достаточно, leave-one-camera-out: исключать всю камеру из adaptation/selection; если cameras мало — явно ограничить вывод new-session. Настройки геометрии опасных зон, thresholds и event temporal logic хранить отдельными версиями.

**Действия:** сначала запустить одинаковый detector/preprocessing на всех holdouts; затем отдельно оценить camera-specific rules с неизменным detector; затем проверить detector adaptation при фиксированных правилах. Так изменение зоны не приписывается training. Слепая независимая оценка проводится после заморозки настроек.

**Метрики / артефакты:** detector per-class AP/recall, event FP/hour/recall при event GT, камера/сессия, масштаб и visibility; версии rules и weights, group-level prediction deltas, примеры ошибок. **Stop rule:** если ошибка вызвана невидимым объектом/неразличимым классом либо geometry mapping, не продолжать detector training без нового сигнала. Если adaptation улучшает одну камеру, ухудшая held-out, выбрать camera-specific deployment либо frozen shared candidate, обозначив дополнительную стоимость модели. Успех на одной withheld camera не доказывает любой новый завод, сезон или физический перенос камеры.

<a id="e022"></a>

### E022 — Controlled loop: доразметка против random при равном бюджете

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-08-E01, W2-04-E01.

**W1-08-E01: исходная процедура** ([ветка](_WORK/W1/08_ACTIVE.md)):


**Вопрос:** какой selector даёт лучшее изменение target-качества на единицу полной человеческой стоимости? Входы: предоставленные разрешённые target videos, согласованные классы/visibility/ignore rules, исходный deployable checkpoint и pinned trainer от model_stack; инструмент разметки с версией; хотя бы одна независимая группа проверки. Этот эксперимент предложен, не выполнен.

1. До inference и просмотра ошибок разделить original videos на `train_seed`, `acquisition_pool`, `dev` и `lockbox`. Группировать по camera/session/связному событию, исключить близкие кадры и копии между splits. Для проверки новой камеры holdout должен содержать новую камеру; session holdout отвечает только про новую сессию. Holdout не включать даже без labels в embeddings, teacher adaptation, выбор порогов или annotation queue. Если независимой группы нет, назвать эксперимент внутри-доменным и не заявлять независимый перенос.
2. Зафиксировать полноту annotations train_seed и taxonomy; размечать все in-scope objects выбранного кадра. Если выбраны только некоторые boxes, сохранить coverage/ignore mask и использовать loader/loss, поддерживающий partial labels; иначе оставшиеся объекты становятся ложным background. Не считать отрицательным кадр, просмотренный только вокруг предсказанной каски.
3. Выполнить pilot timing на train-only material: отдельно time поиска кандидатов, drawing, accepting/rejecting proposals, correction, review, adjudication и export QA. Измерить распределение стоимости по плотности и малым объектам. Pilot входит в общий учёт. Выбрать равный бюджет `B` человеко-минут на arm до основного сравнения; величину назначить после измерения, не выдумывать throughput RTX/аннотатора.
4. С одного seed checkpoint и одинакового seed dataset создать arms: A — stratified random по независимым scene groups; B — ручной targeted; C — простой uncertainty/disagreement плюс предварительно заданные scene caps. Для изоляции selector всем одинаковая предразметка, один и тот же review protocol, сопоставимые annotators/распределение работников. Долю exploration внутри C установить заранее; это экспериментальный параметр, не универсальная константа. Состав selection и причины записать до раскрытия labels.
5. Отсортировать очереди; не заменять дорогой/неудобный пример незарегистрированным удобным. Считать **полные человеко-минуты** selection+annotation+QA, не wall-clock двух одновременно работающих людей. Заранее задать правило последнего неделимого job: закончить с записью overrun либо остановить до начала и не использовать недоделанный кадр. Итоговые фактические budgets/overrun показывать, при необходимости сравнить checkpoints learning curve на общем достигнутом бюджете.
6. На каждом arm заново дообучить по одной закреплённой политике (либо все с seed checkpoint, либо все warm-start), одинаковые schedule/compute/checkpoint selection и sampling старых данных. Финальные веса выбирать по dev; score/NMS/event thresholds менять только в отдельном сравнении. Если число размеченных images различается, зафиксировать exposure/update policy: одинаковые epochs дают разное число updates и могут спутать качество selector с compute. Отдельно показать training wall-clock/GPU cost.
7. На dev оценить paired AP/recall по классам, small/occluded objects, camera/session и нужным событиям; event recall/false alarms/hour — после общего event pipeline. Не смешивать это с mAP. Результат против baseline включает regression старых классов и no-detection misses. Неопределённость оценивать по scene/session units, не считать соседние frames независимыми. Если возможно и решение близко, повторить ключевой arm/random с другим acquisition seed; единственный удачный seed не считается устойчивым превосходством.
8. После выбора единственного финального кандидата открыть lockbox по согласованному evaluation протоколу. Если результат lockbox использован для изменения модели/очереди, он становится dev: для новой независимой оценки нужен новый holdout. Не доразмечать ошибки lockbox и затем сохранять название «test».

**Артефакты:** manifest source hashes/frame timestamps/split/group IDs; acquisition ranks и raw scores; selector/feature/model versions; полные причины ручного отбора; время по стадиям и аннотатору; created/edited/deleted/accepted proposals; final boxes/images/scenes/events; label guidelines, reviewed exports и loader overlays; configs/seeds/update counts/checkpoint hashes; paired metric tables и selected checkpoint criterion.

**Основной учёт:** `human_minutes_total = selection + annotate/correct + review/adjudicate + export_QA`; не переводить в boxes через константу из чужой статьи. Отдельно считать actions (тип действия и их количество), boxes финальные и предложенные, число images, число независимых scenes/sessions, целевые события и compute. Для interpolated tracks хранить manual keyframes и derived boxes отдельно. «500 labels» без единицы и coverage недопустимо.

**Исходы:** C лучше A при том же времени и без критичных regressions — оставить простой selector; A/B сопоставимы или лучше — сохранить их и не оплачивать сложность C; рост AP сопровождается критичными misses/false alarms — изменение не принято; все arms слабы на крошечных объектах — передать гипотезу о visual signal/resolution вместо бесконечной доразметки.

**Stop rule:** лимит человеко-минут/числа rounds и минимально полезный gain/допустимые regressions объявить до цикла с evaluation и требованиями кейса. Остановить усложнение, если два последовательных заранее ограниченных batch не дают практически значимого dev-выигрыша против random либо стоимость selector/QA поглощает доступную интеграцию; две порции — предлагаемое operational rule, не доказанная универсальная граница. При label drift, утечке splits или ухудшении QA остановить обучение и исправить данные. Полезный выигрыш этого эксперимента ещё не доказывает generalization к отсутствующим камерам или корректное исполнение LinQ.

**W2-04-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)):


**Вопрос и решение:** можно ли использовать минимальный route из F226 без custom inference и несоразмерных затрат? Это небольшое инженерное дополнение к E022 pilot; сам equal-human-minutes trial не дублируется и сейчас не выполнялся.

**Входы/доступы:** actual checkpoint/hash и установленный version pin от model_stack; разрешённые train-only кадры разных camera/session, включая empty/плотные/малые объекты; class map, fixed preprocessing/postprocessing и независимый dev/lockbox manifest. Для проверки данных нужен полный ручной просмотр pilot, не только boxes. Среда обычного offline inference; LinQ для selector не обязателен, если кейс это разрешает. Не использовать эти кадры как финальный тест.

**Контроль и действия:** с одним checkpoint/режимом выполнить стандартный predict и сохранять строки F226. Проверить типы/shapes, `probs=None` для detect, координаты overlay в original image, соответствие timestamp/hash и наличие записей no-box/error. Отдельно отметить вероятный cap и warnings. При необходимости проверить NMS/e2e как **разные interfaces**, не ранжировать их quality без labels и не смешивать очереди. Проверить deterministic rank/ties/seeded exploration и temporal cap на сериализованных данных; после reload порядок должен восстанавливаться. Не обращаться к private fields ради выбранного route. Затем измерить pilot scan/serialization и human correction+QA, провести полный missed-object audit selected и exploration кадров.

**Наблюдения:** фактические wall-clock decode/preprocess/forward/postprocess/CPU transfer/serialization/ranking, peak memory/bytes, retained counts и no-box/error/cap flags; минуты поиска/разметки/review; доля дублей и coverage независимых strata. Встроенный `Results.speed` из профилирования S163 не заменяет полный pipeline timer: нет общей гарантии включения decode/queue/serialization и human time. Никаких обещаний минут RTX из имени карты.

**Артефакты:** compact prediction records + schema/version, manifest hashes, package/checkpoint/config, raw timing boundaries, overlays, deterministic ranks/ties/seed, empty/error policy, selected group IDs, human-minute log и coverage audit. Сохраняется также цель score и факт, что это не entropy.

**Исходы:** interface стабилен и стоимость допускает сравнение → arm C E022 при равном полном human budget против stratified random; extra inference/custom tensors оказались нужны → сначала оценить их цену отдельно, либо оставить metadata random/targeted; ranking выбирает дубли/непроверяемые outliers → исправить policy на train-only pilot и зафиксировать изменение до основного опыта. **Stop:** mapping/coordinates/provenance нарушены, пропущены no-box records, утечка splits, неразмеченные in-scope objects трактуются как negatives или pilot съедает заранее отведённый reserve — не расширять AL. Нет подтверждённого выигрыша полного времени/качества → не повышать сложность автоматически. **Предел:** успешный gate подтверждает interface и измеренную стоимость конкретного pilot, не преимущество AL, generalization новых камер, правильность event logic или LinQ inference. Training/benefit проверяются исходным E022; thresholds отдельно по E046.

<a id="e023"></a>

### E023 — Проверка, экономит ли CVAT assistance реальное время

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-08-E02, W1-10-E01.

**W1-08-E02: исходная процедура** ([ветка](_WORK/W1/08_ACTIVE.md)):


Входы: небольшая train-only выборка сцен с разной плотностью, видимостью и пустыми кадрами; expert reference, pinned CVAT/SDK и teacher revision. Контроль: matched scene groups и annotator crossover (порядок рандомизирован, не показывать одному аннотатору тот же кадр повторно); manual from scratch против preannotation+full review. Действия: проверить mapping, нарисовать/исправить, специально искать пропуски вне proposals; второму reviewer проверить полноту и спорные states; export→loader overlay round-trip. Работать в копии task, т.к. default append может удвоить annotations при повторном запуске; `clear_existing=True` использовать только осознанно на копии.

Метрики: total minutes, corrections/actions, missing/extra/class/geometry errors по маленьким и частично видимым объектам, reviewer agreement и final accepted coverage. Не считать число принятых proposals доказательством качества. Сохранить model confidence отдельно от human accepted state и unresolved ambiguity. Для спорного невидимого PPE state применять согласованное unknown/ignore, не угадывать по намерению модели.

Исходы: помощь быстрее при допустимой полноте — оставить; reviewer вынужден искать много FN или разбирать duplicates — изменить teacher/threshold или оставить ручной режим. Stop: потеря labels при mapping/export, невыявленные systematic misses или отсутствие экономии полного времени прекращают расширение automatic task. Положительный результат относится к этому инструменту/teacher/сценам, не гарантирует корректность всей разметки. Наличие QA feature не заменяет качественно созданный reference.

**W1-10-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W1/10_TEACHER.md)):


**Гипотеза/решение:** teacher экономит ручную работу без ухудшения labels. Входы: заранее определённые классы/определения, train-only pool независимых camera/session clips, маленький независимый вручную полностью размеченный audit subset, G commit/config/checkpoint hash. Test/lockbox не входит в pool. Нужны среда inference и annotation UI; точные размеры subset определяются доступными сценами, не выдумываются здесь.

**Контроль:** ручная разметка сравнимой группы с той же полнотой/инструкцией; распределение камер/scale/occlusion согласовать до сравнения. Изменение: только наличие предразметки. Зафиксировать prompts, token/class table, box/text thresholds на development audit; после выбора не менять их по lockbox.

**Действия/метрики:** проверить pixel-coordinate overlays после каждого resize/conversion, class/unknown mapping; измерить label precision/recall/IoU по классу и размеру, пропуски, ошибочные отрицательные состояния, время до полностью исправленного изображения/instance, число исправлений. Отдельно проверять кадры без detections — иначе пропуски скрыты. Correction cost сравнивать вместе с полнотой, а не только с количеством нарисованных boxes.

**Артефакты:** image hashes/splits, original teacher outputs, corrected labels, prompts/thresholds, code/config/weight hashes, времена и audit disagreements. **Исходы:** принять как annotation assistance; оставить только для отбора/поиска; отказать для конкретного класса. **Stop:** систематические неоднозначные состояния/пропуски не исправляются дешевле ручной разметки либо нарушена геометрия/полнота. **Предел:** хороший audit не доказывает качество student, event logic или LinQ; auto labels остаются predictions до проверки.

<a id="e024"></a>

### E024 — Аудит учителя и выбор политики допуска labels

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-09-E01, W2-05-E01.

**W1-09-E01: исходная процедура** ([ветка](_WORK/W1/09_PSEUDO.md)):


**Вопрос/решение:** годится ли teacher как помощник предразметки, как источник unchecked pseudo-labels или только как средство отбора на ручную работу?

**Входы:** версия teacher/checkpoint, class map/box contract, целевой U_train, небольшие полностью размеченные audit/calibration frames из независимых camera/session/time групп; U_train не включает validation/holdout. До отбора зафиксировать sampling: случайные независимые сцены + страты размера/ночь/окклюзия/камеры/редкие positive/пустые outputs. Запись реальной частоты random части нужна, чтобы не выдать oversampled hard subset за общую частоту ошибок. Числа кадров — по фактическому наличию и бюджету.

**Действия:** (1) Сохранить raw predictions до cutoff, post-NMS predictions и preprocessing. (2) На части кадров сделать слепую полную human annotation, затем adjudication расхождений. (3) По нескольким заранее заданным cutoffs считать correct-class one-to-one precision, retained recall/coverage, IoU distribution/AP75-sensitive localization, counts accepted/rejected/FN по class/size/camera. (4) Оценить ручное время на пустую разметку и исправление предразметки на сопоставимых группах. (5) Если достаточно GT, отдельно проверить reliability score bins; не называть это универсальной калибровкой.

**Контроль:** одинаковые изображения, matching/IoU, NMS и preprocessing для всех cutoff; не менять teacher. Thresholds выбираются на calibration/audit, не на holdout. Если audit labels потом пойдут в train, они теряют независимый статус.

**Артефакты:** manifest split/group IDs, teacher hashes, raw outputs, audited GT, correction logs, таблицы TP/FP/FN/IoU с denominators, policy cutoff per class или route-to-review, annotator time. Отдельно фиксировать число независимых сцен, не только boxes.

**Исходы/stop:** если даже high score даёт систематический неверный class/box либо редкий класс почти не имеет coverage — запретить unattended auto-accept для этой страты, перейти к полной ручной коррекции/разметке. Если human correction не экономит время или создаёт omissions — отказаться от предразметки для этой страты. При малом числе positives вывод «не установлено», добрать независимые примеры, а не принять класс по общей precision. Успех подтверждает качество конкретной партии teacher outputs, но ещё не улучшение student и не LinQ.

**W2-05-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)):


Это **будущая предлагаемая процедура, не исполненный эксперимент**, расширяющая существующий E024, а не дополнительный обязательный training trial. Использовать также E023 для стоимости assistance и E025 для последующей student-проверки.

**Решение.** Для каждого canonical class×доступной condition-stratum выбрать: fully reviewed assistance; manual annotation/route-to-review; либо ограниченный unchecked pseudo-label candidate trial. Внешнее numerical acceptance, допустимые regressions/ошибки и уровень неопределённости задаются требованиями кейса до выбора cutoff; сейчас они неизвестны. Safety admission без этих входов не установлен.

**Входы и зафиксированный контракт.** Нужны teacher family/version/config/checkpoint hash, prompt/phrase→class table для VLM, box coordinates, preprocessing, score composition, raw output floor/caps, NMS/order; доступный разрешённый train-domain pool с source hashes/camera/session/time/episode IDs; полная annotation guideline по visibility/ignore и in-scope classes; независимые calibration и confirmation groups. Student/loss interface от model_stack нужен до unchecked branch: что делает с отсутствующим box/непокрытым классом/empty annotation. GroundingDINO substring mapping F129 не считается ontology resolver.

#### 1. Сначала определить estimand и две части отбора

Population здесь — конкретный зафиксированный разрешённый pool/период/набор камер, а не все российские заводы или будущие камеры. Выбрать единицу: например, complete sampled frames с объектными counts внутри; либо episode-coverage с собственным определением. Frame-object recall не переименовывать в event recall. Уточнить macro-average по cameras/groups либо object-weighted metric: это разные denominators.

**P, probability component:** seeded random sample групп из полного sampling frame; полный просмотр выбранных кадров, включая teacher-empty. Если cameras — фиксированные страты, случайно выбирать sessions/episodes внутри каждой; если claim о новых cameras, нужны отдельные cameras и их sampling/holdout contract. При subset кадров внутри группы сохранить conditional frame inclusion probability и правило выбора, а не брать только moments с teacher hits. Counts и footage exposure берутся из sampling frame, не из числа предсказанных boxes.

**D, diagnostics component:** дополнительно взять rare-predicted, small/occluded, low/high-score errors, disagreement, output-empty, известные human-found positives. Membership назначается по наблюдаемым до полного GT признакам; «predicted rare» не значит «истинный rare». Сохранять причину/инструмент поиска, стоимость, overlaps, group IDs. Small/GT-rare страты становятся известны после полного annotation: допустимо анализировать их в P; post-hoc отбор богатых ими кадров в D не делает D случайным sample.

По умолчанию P и D репортить раздельно. Если D имеет заранее определённую probability sampling схему с известными frame sizes и probabilities, допустим единый design estimator с учётом пересечений. Нельзя просто слить две таблицы и усреднить precision. Если один frame выбран несколькими путями, deduplicate и учитывать его union inclusion probability; формула `1-(1-pP)(1-pD)` допустима только при реально независимых механизмах отбора. При неизвестном механизме сохранить P как estimator, D — diagnostics.

#### 2. Весовой расчёт — предлагаемый estimator contract, не проверенная библиотечная команда

Для каждого sampled frame i сохранить полную inclusion probability `pi_i>0`, включая group и conditional within-group stages; `w_i=1/pi_i`. При исчерпывающем просмотре sampled frames и frozen matching вычислить для каждого класса/cutoff `TP_i`, `FP_i`, `FN_i`, `GT_i`, `A_i=TP_i+FP_i`. Предлагаемые weighted ratios:

`precision_hat = sum(w_i*TP_i) / sum(w_i*A_i)`;

`retained_recall_hat = sum(w_i*TP_i) / sum(w_i*GT_i)`.

Суммы inverse-probability weighted counts оценивают totals известной finite population при корректном design. Ratio estimates не объявлять точно unbiased finite-sample оценками; variance должна учитывать actual stratification/clustering. При равновероятном frame sample веса сокращаются; при равновероятном **group** sample с разным числом просмотренных кадров это нельзя предполагать без проверки второго этапа. Object-weighted recall использует GT-object denominator; среднее recalls групп оценивает другую величину. Для rates знаменатель — просмотренная/взвешенная exposure, не detections.

Если pi неизвестны для D, допустим только conditional-on-selected-slice отчёт counts и ошибок. Если sampling frame неполон/часть условий имеет pi=0, population claim ограничить покрытой частью, missing strata назвать. Число boxes в страте не заменяет inclusion probability. Не вычислять weighted D-ECE штатным netcal без проверки поддержки weights: S170 выше доказывает prediction-level интерфейс, не наш complex survey estimator.

#### 3. Blind complete GT и одинаковое сопоставление

Разметчик на контрольной части сначала ищет **все** in-scope objects без teacher overlays, затем независимое adjudication; сохраняются uncertain/ignore и причины. Полный обзор teacher-empty frame обязателен. Для assistance отдельно проверять omissions после correction: подтверждение предложенных boxes не равно full review. Держать одинаковые geometry/NMS/caps/class map и matching для всех cutoff. Сохранить candidate outputs до admission cutoff; если detector уже отсёк outputs своим floor/cap/NMS, явно указать, что анализ не восстанавливает потерянные candidates.

TP — one-to-one correct class + заранее объявленный IoU criterion; duplicates — FP по frozen policy. Отдельный localization diagnostic на class-compatible сопоставлениях: IoU distribution, плохие границы/центры, borderline cases; правила такого matching объявить отдельно, не считать его relaxed matches за TP основного gate. Для каждого cutoff показать принятые/отвергнутые predictions, TP/FP, полное GT/FN; разделить GT, потерянные admission cutoff, и GT без usable исходного detection. При изменении cutoff переагрегировать matching по объявленному score order. «Доля оставленных predictions» `accepted/candidates` не называется recall: retained recall имеет denominator всех GT, в том числе не найденных вовсе.

#### 4. Calibration diagnostic и независимое подтверждение cutoff

На calibration groups можно сравнить class-wise precision/retained-recall curves и, если support позволяет, reliability bins при фиксированном class+IoU target. Показать class/size/position/camera support каждого bin, excluded bins, raw counts, число positive groups; не сравнивать D-ECE с разным binning как улучшение. Не вводить новый calibrator, если простого cutoff/review policy достаточно для решения. Если calibrator обучается, отдельно сохранить fit data/parameters и проверить, что score reordering/NMS/order действительно часть frozen policy.

Выбранные на этих данных cutoff, bins, feature set и calibrator — selection. Их значения на той же выборке описательны, не независимое подтверждение. Заморозить policy и один раз применить к отдельным complete-GT confirmation groups, с собственным P/D design. Если confirmation использована для новой правки policy, она стала development: следующий independent claim требует новых нетронутых групп либо явного статуса reused evidence. Final student lockbox E025 не расходовать на повторный teacher tuning; audit data после помещения в train теряют независимый статус.

#### 5. Support и неопределённость: условия отказа

Для instance metrics кластером служит независимая единица отбора/переноса: episode/session при fixed cameras, camera при соответствующем camera-generalization claim. Несколько sessions одной камеры не превращаются в несколько независимых cameras. Сохранять оба уровня; тысячи boxes одного человека/смены не считаются тысячами независимых испытаний. CI/resampling design выбирается по реальному sampling plan; при достаточной поддержке пересчитывать weighted numerator/denominator по resampled independent groups с сохранением обеих compared policies. Простой iid binomial CI по boxes и обычный frame bootstrap не применять автоматически. Bootstrap observed groups также не обнаруживает отсутствующий в них failure mode.

| Наблюдение | Допустимый отчёт | Недопустимый допуск / следующий шаг |
|---|---|---|
| `GT_c=0` в independent confirmation | Recall/coverage класса N/A, positive support 0; observed FP возможны | Не «100% recall», не «0 misses доказано». Полный review/независимый целевой positive collection |
| Accepted predictions класса 0, `GT_c>0` | Precision N/A; retained recall 0 и реальные FN при объявленном matching | Не считать undefined precision идеальной. Unchecked branch не закрывает этот класс |
| Accepted predictions 0 и GT 0 | Обе метрики N/A, явная пустая support cell | Не auto-accept по отсутствию ошибок |
| Есть немного positives, почти все из одной группы | Counts/наблюдаемая point estimate и происхождение, uncertainty «не установлена», если design не поддерживает расчёт | Не переносить на новый camera/condition; искать новые independent groups, не соседние frames |
| Все observed successes либо failures, degenerate bootstrap/NaN | Raw TP/FP/FN, group counts, interval unavailable/неинформативен | Не интервал нулевой ширины как доказательство. Обоснованный иной estimator только с его design assumptions |
| D rare/empty/high-score диагностическая выборка, pi неизвестны | Selected-slice failure descriptions и counts | Не population precision/prevalence; остановить общий claim или использовать только P |
| На P редкий класс отсутствует, на D positives есть | P не оценивает recall класса; D подтверждает наличие failure/success на выбранных примерах | Не переносить conditional D recall на population и не вычислять частоту класса по D |
| Сводная precision высокая, critical slice имеет misses/плохой IoU | Сводка плюс отдельный запрет/неустановленный gate страты | Не скрывать отказ macro/pooled average; review этой страты |

Универсальные sample size, число bins, precision floor и минимальное количество групп не заданы. Нужный объём зависит от accept/reject margins, распределения ошибок/класса, design и independent support; это Q010/Q004. Если доступный support не разрешает требуемый claim, результат — **insufficient evidence**, а не принятие при нулевой наблюдённой ошибке. Даже валидный интервал не исправляет blind-spot неполного GT.

#### 6. Ветви допуска и границы claims

| Ветка | Evidence gate до использования | Что можно заявить при успехе | Stop / предел |
|---|---|---|---|
| Fully reviewed assistance | Полный обзор каждого selected frame, исправление missing/wrong boxes/classes и ontology/geometry QA; controlled cost pilot против manual с одинаковой полнотой | Teacher помог получить reviewed labels; измеренная экономия полных human minutes на заявленных groups | Если omissions/anchoring bias или cost хуже manual — отключить подсказки для страты. Audit предсказаний не заменяет review каждого используемого кадра |
| Unchecked labels / отдельный SSL trial | Frozen policy, independent complete-GT confirmation с precision **и** retained coverage/localization/critical slices, достаточный design support по согласованным acceptance; runnable loss/ignore contract для dropped positives | Ограниченный кандидат на noisy-label training по конкретной frozen policy; происхождение остаётся pseudo | Неподдержанный critical class, unknown support или loader воспринимает omissions как negatives без обоснованной обработки — не auto-accept. Даже хороший audit не доказывает student gain/безопасность deployment |
| Manual route-to-review | Полные annotation instructions и independent QA, прогнозы могут только ранжировать очередь | Получены ручные labels/диагностированы ошибки без заявления качества unchecked teacher labels | Selector не должен исключить все no-detection frames. Расход поиска и review входит в human budget |

**Контроль стоимости:** помощь teacher против ручной разметки сравнивать при одинаковом определении «полностью готово», на сопоставимых/случайно назначенных группах и с учётом аннотатора/порядка работы. Одни и те же изображения последовательно одним человеком создают memory bias; не выдавать такое сравнение за слепой cost trial. Считать selection, drawing/correction, omissions search, review/adjudication/export QA; не только accept clicks. Экономия времени не подразумевает хороший unchecked branch.

**Артефакты:** frozen sampling frame/population/estimand, P/D manifests, probabilities/weights/overlaps и страты, source/group/frame hashes; teacher/checkpoint/config/prompt/class-map/score/NMS/cap versions; raw predictions, cutoff candidates и frozen choice; blind/adjudicated GT с provenance; per-group/class/size таблицы accepted/TP/FP/FN/GT/IoU/exposure и support/bin exclusions; calibration vs confirmation статус; human time/correction log; решение на каждую unsupported stratum, rollback policy. Derived labels не смешивать с human-reviewed labels без provenance.

**Исходы/stop:** assistance экономит полные минуты при сохранённой QA → E025 B/C comparison; teacher пригоден только искать примеры → manual queue; unchecked candidate проходит согласованный gate → отдельная noisy-label D-arm с baseline, не подмешивание в fully corrected B; support/semantics/geometry/loss invalid → стоп этой ветки и ручная коррекция/уточнение. Новый teacher checkpoint/prompt/NMS/условия потока требуют пересмотра applicability, не молчаливого переноса gate. Успешный аудит характеризует frozen policy на объявленном материале, не универсальный safety threshold, student/event quality или исполнение LinQ.

<a id="e025"></a>

### E025 — Offline audited loop против обычного supervised adaptation

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-09-E02.

**W1-09-E02: исходная процедура** ([ветка](_WORK/W1/09_PSEUDO.md)):


**Гипотеза:** исправленная teacher предразметка даёт полезные дополнительные сцены и экономит annotation time. **Входы:** прошедший E024 teacher, runnable baseline student от model_stack, labeled L_train, фиксированный U_train, V_validation и закрытый H_holdout из других сессий/камер согласно целевому claims. Кадры одной сцены/track не разносить по этим частям. Для adaptation claim заранее объявить, какие target streams участвовали в подготовке.

**Контроль и действия:** A — student на исходном L; B — тот же student на L + полностью исправленных pseudo-preannotations. Зафиксировать architecture/checkpoint, preprocessing, optimizer budget, seed, augmentations, class map, validation cadence и inference thresholds. Дополнительный полезный контроль C — та же annotation time на обычную ручную разметку без teacher; не смешивать «тот же набор изображений» и «тот же человеческий бюджет», отчёт должен показать оба ограничения. Студента обучать с supervised losses, если labels полностью исправлены; это не воспроизведение Soft Teacher. При проверке unchecked labels завести отдельную D-arm с явным статусом noisy/partial и поддержанным loss, не подмешивать их в B.

**Метрики:** student AP50:95/per-class AP, critical-class recall при одинаковом FP budget, AP small/IoU/localization, validation slices новых камер и прежнего домена, annotation minutes/corrected positive, время обучения. Выбор checkpoint и cutoff только по V. Сначала сравнить на V; H открыть для зафиксированного кандидата по принятому evaluation protocol, не использовать H для следующего выбора threshold/кадров. Повтор seed/group comparison — если первый эффект мал относительно наблюдаемой вариативности и остаётся время.

**Артефакты:** A/B/C configs, corrected dataset version и provenance каждого label, исключённые frames, teacher prediction/correction trail, seeds/logs, выбранный **student** checkpoint, class map, inference-output examples; export manifest отдельно.

**Исходы/stop:** принять B, если заранее заданный practically useful validation gain/annotation benefit достигнут без запрещённой регрессии критичных slices и подтверждён выбранным holdout протоколом. Если validation деградирует/critical recall падает — вернуть A, анализировать ошибки labels до следующего прогона. Ограничить заранее число итераций и compute/annotation budget; две порции подряд без заранее заданного полезного изменения — основание закончить эту ветку (предлагаемое правило, не paper recommendation). После просмотра H, если нужно менять модель, следующий результат требует нового нетронутого тестового материала или честного статуса повторно использованного holdout. Успех FP student не подтверждает export/quantized/LinQ и event quality.

<a id="e026"></a>

### E026 — Gate для online EMA integration

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-09-E03, W2-03-E01.

**W1-09-E03: исходная процедура** ([ветка](_WORK/W1/09_PSEUDO.md)):


**Вопрос:** стоит ли цена online teacher/student training последующего полноценного trial? **Входы:** runnable exact pinned repo/совместимый trainer, L/U/V/H как E025, supervised checkpoint, confirmed available VRAM/OS, известный deployable student path. В отсутствие runnable implementation для выбранной головы остановить online-ветку, продолжить E025.

**Действия:** сначала небольшой инженерный smoke check: labelled/unlabelled separation; отсутствие скрытого GT в U; геометрическое соответствие weak→strong boxes; no-grad teacher; обновление student и EMA; loss weights; empty pseudo-label batch; сохранение/reload teacher/student/optimizer/iteration. Для SoftTeacher проверить normalized jitter и source-code Gaussian/paper uniform discrepancy; для UT v1 проверить нулевые pseudo regression losses при ненулевом supervised regression. Затем ограниченный paired trial supervised vs online с тем же student backbone, L/U groups, доступным training budget и одинаковым inference policy; отличия compute считать, а не скрывать.

**Teacher quality audit:** фиксированные независимые audit frames E024 проверять в заданные checkpoint моменты, логировать per-class accepted counts/precision/coverage/localization. Рост числа confident boxes без роста correct coverage — сигнал feedback bias. Audit используется для диагностики/selection и не является H.

**Метрики/артефакты:** раздельные teacher/student V metrics, loss traces, teacher drift/EMA state, pseudo class histogram с denominators, actual wall-clock/peak VRAM, full resolved config/repo/dependency lock, выбранный отдельный student, raw output contract и reload parity. Нельзя выбрать teacher по V, экспортировать student и сообщить teacher AP.

**Stop:** ошибки labels/splits/transforms/gradient routing, nonfinite losses, систематическое исчезновение редких pseudo classes или ухудшение критичного validation slice — остановить, исправить integration либо вернуться к supervised/offline route. Если smoke check/короткий trial исчерпал заранее отведённый инженерный бюджет без пригодного student — не превращать оставшиеся часы в переписывание trainer. Финальный допуск только после полной controlled comparison; короткий успех подтверждает работоспособность loop, не published gain, не LinQ и не редкие события.

**W2-03-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)):


**Proposed, не выполнено.** Это детализация существующего gate, не отдельный mandatory benchmark. Вопрос: можно ли получить воспроизводимый single-detector inference artifact из exact online route до назначения большого SSOD trial?

**Входы:** один UT/ET SHA, resolved config/dependency lock, compatible supervised checkpoint/classes/preprocessing; небольшой полностью проверенный diagnostic набор с known boxes: empty, tiny, overlapping classes, edge box. U_train/V/H из независимых допустимых групп; audit/calibration отдельно. Diagnostic GT доступен контролёру, U loss его не получает. Inventory GPU/OS/VRAM и SDK/export prerequisites отдельно. Не проводить оба routes ради покрытия.

**Действия/контроль:**

1. Проверить identifiers/role exposure/class IDs, effective augmentation при U with_gtFalse, отсутствие L/V/H в U. Known boxes: UT общий transform identity между views; ET M/flips/mosaic borders/clipping/removal. Сохранить overlays и численные координаты. Sentinel/perturbed U GT не должен менять pseudo targets/loss, если GT лишь diagnostic.
2. На будущих minimal steps проверить teacher no-grad/eval, student grads/update, EMA formula/timing. UT отдельно cls/reg sets, boundary masks, empty positives; ET reliable/intermediate/no proposals, objectness mask/soft targets. Проверить no proposals на одном image mixed batch и whole batch, boxes исчезли после transform, rare pseudo class отсутствует, all-negative L. Требовать finite losses/gradients, логировать background вклад на hidden known positive. Отсутствие exception не доказывает missing-positive safety.
3. Save/reload **до stripping**: выбранные student/online teacher/secondary EMA, optimizer/iteration/scheduler/scaler/threshold/adaptor metadata по реально поддержанному интерфейсу. Сравнить predictions до/после reload. Не обещать bitwise continuation. UT wrapper→modelStudent/modelTeacher; ET raw/online EMA/secondary EMA с hashes. При отсутствующем state заранее указать custom saver requirement.
4. Final extraction: UT штатный std eval→proposed detection-only wrapper/std removal с cls_n_ctr; ET chosen raw/secondary→--da removal→raw levels→exact decode/NMS. Одинаковые images/preprocess/precision; boxes/classes/scores в заранее заданной numerical tolerance и совпадение post-NMS outcomes. Проверить names/shapes/operators/graph outputs, не только ONNX existence. Успех CPU/ORT не доказывает LinQ.
5. Только после correctness/deploy gate — E026 paired supervised-vs-online. Equal init/data/validation policy плюс L/U exposures, updates, teacher passes/wall-clock: equal epochs недостаточно. E025 annotation control — альтернатива по human budget, не обязательная третья arm. Teacher drift audit E024; H не используется threshold/checkpoint/adaptor selection.

**Метрики/артефакты:** coordinate/gradient/state/branch parity traces, per-class accepted counts и missing-positive supervision, обе UT validation оценки либо явно названные три ET weight states; resolved config/env/hash, manifests/tensor examples/overlays, export hash/operators/output schema, decode/NMS revision. Раздельные T_setup/T_loader/T_step/T_audit/T_save-reload/T_extract/T_export-parity, peak VRAM и human debugging minutes. Числа измерять, не угадывать по RTX4070.

**Исходы/stop:** geometry/leakage/gradient/nonfinite/extraction mismatch — stop, исправление в bounded engineering budget либо fallback E02. Нет явной ветви/final target path — long online не запускать. Correctness pass разрешает только controlled trial, принятие по V critical constraints и независимому H protocol W1-09. Critical degradation/исчезновение редких pseudo classes — rollback. Спорный effect относительно group/seed variation — repeat только если решение ещё актуально. Успех не доказывает target gain, экономию annotation, events или LinQ.

<a id="e027"></a>

### E027 — Даёт ли native feature KD пользу сверх обычного fine-tuning?

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-10-E02, W2-01-E01.

**W1-10-E02: исходная процедура** ([ветка](_WORK/W1/10_TEACHER.md)):


**Входы:** утверждённый train/val split по camera/session, полностью размеченные требуемые classes; baseline student/checkpoint; уже проверенный target teacher той же family/task, U commit или явно новая pinned версия; совместимые levels/shapes. Проверить teacher quality на development material отдельно; не выбирать его по final test. VRAM/драйверы устанавливаются измерением.

**Контроль:** A — supervised student, B — тот же student/init/data/transforms/optimizer/effective batch/resolution/seed/updates + `distill_model`, `dis=6.0` как versioned default, не оптимум. Любые дополнительные `dis` значения — отдельная заявленная абляция. Чтобы не спутать вычисления и метод, записать и одинаковые updates, и wall-clock; не выдавать сравнение разного числа updates за чистый loss effect.

**Действия:** сначала один batch: neck shapes/strides, class contracts, teacher eval и неизменность weights/BN, student/projector gradients, конечность loss, teacher no_grad. Затем небольшой диагностический training; только после корректности — сопоставимый trial. Логи: supervised components и dis_loss, peak allocated/reserved VRAM, step time с прогревом, data loading, весь teacher preparation cost. Validation: AP50–95/APsmall/per-class recall, false detections на релевантном фоне; итоговые event metrics передать evaluation. Threshold/NMS фиксируются в паре.

**Артефакты:** resolved args, package/commit, dataset/class map, seed, init/teacher hashes, logs, selected checkpoints, raw predictions, timing configuration. **Исходы:** B улучшает релевантные ошибки в пределах заранее заданной practical acceptance; эффекта нет; редкие классы ухудшаются; teacher bias наследуется. Повтор seed/группы оправдан, если наблюдаемый gain мал или нестабилен. **Stop:** контракты не сходятся, teacher не лучше на нужных ошибках, memory/time budget не позволяет сравнимый trial, или early validation показывает существенный вред critical class. **Предел:** один trial не доказывает перенос на другие камеры/классы; `.pt` качество не подтверждает export/LinQ.

**W2-01-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)):


**Статус PROPOSED, не выполнено.** Это дополнение operational detail к E027/E03, а не ещё один quality trial. Решение: допускается ли ровно выбранная YOLO11 пара к controlled KD сравнению и final artifact проверке.

**Входы.** Wheel 8.4.184 с указанным SHA либо exact U checkout с dependency lock; установленная фактическая Python/PyTorch/CUDA/driver среда; unfused student initialization и target-trained teacher `.pt` с hashes и provenance; original YAML/scale/head attributes; одинаковые channels; согласованные target class definitions. Нужен небольшой корректный train-only diagnostic batch с полностью проверенными labels, включая допустимый empty image, и отдельные development inputs для reload parity. Camera/session holdout не участвует в debugging. Объём и compute budget назначаются после inventory, здесь не выдумываются.

**Контроль.** Supervised student из той же target-initialized state, тех же labels/geometry/batch/optimizer settings; во время correctness smoke он проверяет обычный head/loss/reload contract, а не superiority KD. Для последующего quality trial сохранить одинаковые sample/update budgets и отдельную цену времени, как E027. Teacher выбирается до lockbox по релевантному audit, а не по финальному student result.

**Действия будущего инженера, процедурный псевдокод без нового CLI.**

1. Проверить установленную version/path и hashes перечисленных files; прочитать фактические student/teacher nc/names/task/channels и **head.nc**. Записать transfer/skipped tensors student; убедиться, что teacher не пересоздан неожиданно из-за channel mismatch. Сохранить полный teacher weight hash и доступный resume path.
2. После штатной trainer setup снять model types и hooks: для обеих `[16,19,22,23]`, actual stride `[8,16,32]`; зарегистрировать actual B/C/H/W каждого neck level. Проверить идентичный transformed input обеим моделям и равенство пространственных grids. Если включён multi_scale, повторить shape check на реально используемых крайних формах; square constructor check этого не заменяет.
3. Для стандартного YOLO11 head убедиться в raw `scores` B×nc_teacher×sum(HW) и отсутствии необходимости o2o. Проверить split sizes ровно H_i×W_i; score weights finite, в [0,1], имеют B×1×H_iW_i. Не интерпретировать их как вероятность корректной детекции. Сохранить отдельно supervised components и dis_loss.
4. Выполнить один разрешённый correctness forward/backward/update: teacher eval, все teacher requires_grad=False, gradients отсутствуют, weights и BN buffers не меняются; student/projector gradients finite и нужные trainable tensors обновляются. Проверить реальный compile=False и наличие projectors в optimizer. Записать peak memory, setup/dummy-forward cost и step time с явной timing boundary. Nonfinite/неожиданный rebuild/shape mismatch останавливают gate.
5. Сохранить отдельную immutable копию **pre-strip** checkpoint. В чистом training process проверить wrapper/projector reconstruction с тем же teacher hash; записать восстановленные keys/epoch/projectors. Это smoke resume, не bitwise equivalence promise. При недоступности teacher training resume должен быть признан неготовым; inference check final student от этого отделён.
6. Нормально завершить bounded smoke run; сравнить pre-strip и final last/best module manifests. Final не должен содержать DistillationModel/projector/FeatureHook в reachable model graph. Оставшаяся train_args.distill_model строка допустима как provenance. Отдельно periodic file не считать автоматически stripped.
7. Загрузить final artifact в новом process, где исходный teacher path недоступен, и выполнить **inference**, не `.train()`. Сравнить outputs с извлечённым тем же EMA student до stripping с учётом FP16 conversion, одинаковых inputs/decoding/NMS и заранее заданных numerical tolerances. Затем E028 продолжает actual exporter/FP parity/SDK compile/target inference для выбранного student.

**Observables/артефакты.** Resolved environment, wheel+code hashes, original and resolved args, dataset/class maps, weight hashes, per-level tensors/strides, raw-score branches/split counts, requires_grad/BN snapshots, gradient/update summaries, optimizer groups, loss components, peak memory/time, immutable interrupted checkpoint, normal final checkpoint, module/key manifests, reload logs/raw outputs. Никаких обязательных AP claims из correctness batch.

**Исходы и next action.** Все contracts проходят → только тогда E027 controlled KD vs supervised и E028 deployment path. Wrapper/head/serialization failure → локализовать exact checkpoint/version и остановить KD, сохранить supervised candidate. Teacher слаб/нерелевантен → сначала data/teacher branch либо отказаться от KD; не увеличивать dis как автоматическое лечение. Нехватка памяти/времени → меньшее разрешённое batch/teacher или отказ от ветки после честного profiling, без выдуманного множителя затрат.

**Stop rule.** Ошибочный data/class transfer, spatial mismatch, teacher mutation, отсутствующий projector update, nonfinite loss, недоступный исходный teacher для resume, зависимость final inference от teacher или неустранимое нарушение resource cap запрещают promotion в большой run. SDK gap блокирует утверждение target success, но не маскируется как native KD failure.

**Предел подтверждения.** Успешный smoke означает корректность выбранных interfaces, сохранения и извлечения в данной среде. Он не доказывает convergence, качество редких классов/событий, преимущество KD, generalization новой камеры, export parity или LinQ execution. Порог practical gain и admissible degradation задаются case/evaluation, здесь не назначаются.

<a id="e028"></a>

### E028 — Финальный artifact действительно содержит только student?

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-10-E03.

**W1-10-E03: исходная процедура** ([ветка](_WORK/W1/10_TEACHER.md)):


**Входы:** нормально завершённые A/B runs E027, immutable copies промежуточного и final checkpoint, точный export path из model_stack, target SDK от linq_platform. **Контроль:** student той же архитектуры без KD. **Действия:** сохранить manifest module types/keys/shapes/params; сравнить wrapper checkpoint до и final после `strip_optimizer`; загрузить финал в чистом процессе без teacher weights/доступа к его path; выполнить inference. Проверить отсутствие teacher/projector/hooks в final model и ONNX, входы/выходы, формы, decoding/NMS. Exported outputs сравнить с .pt на одних изображениях и одной обработке; затем выполнить реальную target compile/inference.

**Метрики:** reload success, dependency on teacher, file/parameter/graph-op counts, численные расхождения outputs, AP/critical recall до/после export и quantization, target latency/throughput/memory. **Артефакты:** source/final/export hashes, graph inspection, environment, compiler/runtime logs, raw outputs и реальное доказательство LinQ execution. **Исходы:** student-only artifact пригоден к дальнейшей target проверке; wrapper не снят; exporter/SDK отвергает graph; качество меняется после conversion. **Stop:** teacher требуется для inference, graph не соответствует утверждённому student или target path не получен. **Предел:** одинаковый parameter count/файл не доказывает одинаковую скорость; успешный ONNX Runtime тест не доказывает LinQ.

<a id="e029"></a>

### E029 — Только при наличии рабочего MMDetection: FGD/LD integration gate

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-10-E04.

**W1-10-E04: исходная процедура** ([ветка](_WORK/W1/10_TEACHER.md)):


**Входы:** pinned F или L env; выбранная recipe; train/val/classes, teacher weights; baseline в той же framework. **Контроль:** обычный student с теми же updates/preprocessing/initialization. Inheriting отделить от distillation: иначе эффект начальных neck/head weights смешан с KD. **Действия:** dry-run tensor/coordinate checks, один training batch, сохранение и student extraction; затем небольшой сопоставимый trial, если путь не требует перестройки выбранного deployment graph. **Метрики:** gradients/losses, memory/time, AP/critical errors; фиксировать paper/config gamma discrepancy для FGD. **Артефакты:** env lock, recipe diff, teacher/config hashes, converted student, validation predictions. **Исходы:** продолжить отдельный route или оставить как research evidence и использовать готовый native KD. **Stop:** legacy dependencies/портирование или head change поглощают выделенный integration budget. **Предел:** воспроизведение COCO recipe не доказывает PPE domain benefit; будущий экспорт всё равно отдельный gate.

<a id="e030"></a>

### E030 — gate labels до обучения

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-11-E01.

**W1-11-E01: исходная процедура** ([ветка](_WORK/W1/11_SYNTHETIC.md)):


Вопрос: допустим ли конкретный compositor/generator для нашего ontology? Входы: annotation guide с visible/amodal/unknown convention, train-only assets/backgrounds с provenance, реальный input preprocessing, renderer/compositor/generator revision/config/seed. Для generative route нужны отдельные reviewer labels; эстетическая оценка и detector confidence не заменяют человека.

Контроль: оригиналы и их annotations; для group paste — неизменённая исходная группа. Действия: получить небольшую заранее стратифицированную batch по классу, масштабу, pose, occlusion и state; в overlays показать исходные/новые masks, boxes, evidence regions и relations; независимый reviewer проверяет class, geometry, state, missing/extra instances. Проверить также фон: после filtering удалённая annotation не должна превращать оставшийся объект в отрицательный background. Для генеративного редактирования проверять весь кадр, не только исходную область.

Метрики: доли неверного class/state/geometry, extra/missing instances; survival evidence после final resize; ошибки по assets/scale/occlusion, время reviewer на пригодный sample. Артефакты: manifest исходников/деривативов и прав, revisions, seeds, transformed annotations, overlays, reviewer decisions/reasons. Stop rule: воспроизводимая ошибка state/relations, систематическая потеря evidence или неизвестная background-label policy блокируют тренировочный trial; исправить generator/policy или исключить группу. Успех gate допускает ablation, но не доказывает перенос и не гарантирует отсутствие редких ошибок.

<a id="e031"></a>

### E031 — controlled real-only vs real+synthetic

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-11-E02, W2-08-E01.

**W1-11-E02: исходная процедура** ([ветка](_WORK/W1/11_SYNTHETIC.md)):


Вопрос: закрывает ли синтетика выбранный реальный failure slice? Входы: подходящий pretrained checkpoint и pinned trainer, один real train split, validation и untouched real lockbox по независимым camera/session/clip groups; verified synthetic из E030. Деривативы наследуют split оригинала. Определить один пробел и заранее critical metric/допустимые regressions с evaluation; численный порог без задания не выдумывать.

Контроли: A real-only с текущими допустимыми augmentations; B тот же real pool + synthetic одного типа. Одинаковые input resolution, исходные веса, classes, optimizer, seed, inference thresholds/NMS и checkpoint selection по real validation. Измерять updates, real-image exposure, synthetic exposure и wall-clock: одинаковое число epochs на увеличенном dataset не означает равный training budget. Основное сравнение фиксирует optimizer-update budget; при выигрыше/сомнении добавить контроль real oversampling до того же real exposure либо matched-wall-clock comparison. Это позволит отличить новую информацию от дополнительных повторов/шагов. Synthetic-only C допустим только как диагностический secondary arm, не обязательная трата.

Метрики: per-class AP/recall, precision при фиксированном рабочем пороге; size/evidence/occlusion slices, target failure slice, clean/background negatives, camera groups; event false alerts на независимом реальном видео при фиксированной event logic. Повторы по seed или независимым группам назначать для решающего неустойчивого сравнения, а не выдавать кадры одной записи за независимые наблюдения. Артефакты: split/asset manifests, config diff, checkpoint/predictions, selection logs, реальные error examples и time/annotation cost.

Исходы: улучшение real critical slice без недопустимой regression → сохранить candidate для export проверки; gain только на synthetic → transfer не подтверждён; regression real/negative cameras → уменьшить долю/исправить контекст или отказаться; gain неотличим от real oversampling → предпочесть более простой путь с учётом затрат. Stop rule: прекратить ветку при broken E030, critical regression или исчерпании выделенного бюджета без подтверждённой real пользы; lockbox не использовать для многократного подбора. Успех подтверждает конкретный dataset/recipe; не доказывает LinQ execution, новую камеру или событийную безопасность.

**W2-08-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)):


**Вопрос/решение:** даёт ли полностью reviewed synthetic pool новую информацию для заранее определённого real failure slice; не получен ли apparent gain из изменения real exposure, updates, masks или selection?

**Входы:** E030 прошёл; выбранный model_stack checkpoint+hash, pinned supervised trainer, class/ignore convention и graph; один real train manifest; derived synthetic assets с train-only provenance и полноценным review; независимые real validation/lockbox camera/session/clip groups. Те же реальные splits, что в E031. Masks не наследовать из исходного inpainted image. Если baseline segmentation требует масок, нужен подтверждённый mixed-supervision criterion либо новые verified masks; bbox data-only route не выдавать за segmentation recipe.

**Основные arms:** A real-only и B real+reviewed-synthetic; одинаковые initialization, input/preprocessing, effective batch, optimizer-update budget, augmentation policy, validation objective, inference thresholds/NMS/event rules. Сохранять **фактический** per-source draw ledger, не только `epochs` и список файлов. Не утверждать одновременно equal updates и equal real exposures при фиксированных batch и ненулевом synthetic replacement: эти constraints несовместимы без дополнительных изменений.

**Минимальная поправка accounting:** заранее выбрать primary estimand — gain при равном числе updates либо gain при равном real exposure. Записать `T_optimizer`, `N_real_draws`, `N_synth_draws`, real unique IDs, synthetic unique IDs/source-layout counts, empty/rejected batch counts, accumulation и skipped updates, LR progression, mask-active counts, human review minutes, `T_setup/T_train/T_validate/T_export`. Pool ratio `N_synth_unique/N_real_unique`, draw fraction `N_synth_draws/(N_synth_draws+N_real_draws)` и `p_batch` — три разных поля.

**Условный дополнительный контроль:** только если B меняет решение, но attribution неоднозначна, провести comparison с matched-real-exposure schedule и отдельным all-real update control, выбрав заранее, какая неопределённость важнее. Например для replacement sampling можно удлинить B до сохранения real draws A, но тогда обязательно указать большее число updates и изменённый LR path; это не «тот же бюджет». Не считать real oversampling волшебным способом одновременно выровнять все знаменатели. Сравнение по wall-clock — иной practically useful estimand, тоже маркировать отдельно. Не назначать все arms заранее.

**Наблюдения/артефакты:** как в E031 — real critical recall/AP, false positives/alerts на real negatives, class/size/occlusion/camera slices; checkpoint selection только по real validation, final lockbox после принятия решения. Дополнительно source ledger, review decisions включая discarded/extra objects, annotation coverage после import, masks/labels overlays после final resize, config diff и candidate hash. Synthetic validation не заменяет real evaluation.

**Исходы/stop:** gain на real critical slice без недопустимого regression → candidate на обычный export/target gate; gain только на synthetic или неотличимый от repeats/schedule → синтетическая польза не установлена; broken semantics/partial coverage/unknown supervision → блокировать B до исправления данных. Если review/integration занимает больше полезного remaining critical path, выбрать real annotation, а не увеличивать pool. Успех подтверждает только данный reviewed dataset/recipe; не доказывает Gen2Det implementation, generalization новой камеры, событийную безопасность или LinQ execution.

**Будущий controlled amendment для special-loss route:** если получен Q020 artifact, использовать существующий E007, без изобретённого patch. Добавить provenance switch real↔synthetic, retained/discarded/extra instances одного и разных classes, images с нулём retained GT, все RPN/first-stage/RoI/dense class negatives, regression/mask/reduction observables, assignment до/после sampling, final graph reload. Пройти correctness до quality trial. До получения артефакта это interface request, не реализованный протокол Gen2Det.

<a id="e032"></a>

### E032 — локализовать источник синтетического shortcut

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-11-E03.

**W1-11-E03: исходная процедура** ([ветка](_WORK/W1/11_SYNTHETIC.md)):


Входы: результаты E031, asset IDs, reviewer labels, real difficult examples. Контроль: original real-only model и real validation; действия — диагностически сравнить same assets с разными blending/backgrounds и context-constrained placement, удерживая label/количество samples. Отдельно измерить group paste против вмешательства только в PPE, если второй вариант прошёл E030. Не менять одновременно detector architecture.

Метрики: ошибки по asset/source/background, per-state confusion, частота FP на paste-like textures, evidence visibility; синтетический набор является диагностикой, основное решение остаётся по real validation. Артефакты: парные примеры, provenance, prediction diffs и reviewer причины. Исход: зависимость от контура → править mask/blend; зависимость от camera/background → проверить sampling/context; неверные person states → остановить такой edit и доразметить реальные случаи. Stop rule: не расширять generator pool до устранения систематического дефекта; если одна контролируемая коррекция не улучшает real целевой slice в выделенном бюджете, перейти к реальной разметке. E032 объясняет конкретный failure, не устанавливает универсальный лучший способ blending.

<a id="e033"></a>

### E033 — Labels/loader gate

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-12-E01.

**W1-12-E01: исходная процедура** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):


**Входы:** выбранный detection checkpoint из model_stack, небольшой вручную проверяемый набор реальных кадров; хотя бы positive каждого доступного обязательного класса, background и сложный пример; раздельные camera/session IDs. Цель — решить, можно ли доверять training inputs. **Контроль:** source image hash и ручной GT; никакой training, lockbox не использовать. **Действия:** вывести counts missing/empty/corrupt и class IDs; overlay исходных и реально преобразованных boxes; workers=0/cache=False при loader failure; сверить цвета/диапазоны/геометрию с конкретным model preprocessing. Не отключать все преобразования одним выдуманным detect augment=False: список действующих transforms задаётся и проверяется по W1-05.

**Метрики/артефакты:** counts с denominators, crop sizes/object pixels, contact sheet before/after, список найденных несоответствий, manifest/config/log. **Исход:** совпало → E034; исправимые labels/loader → исправить и повторить только изменённый gate; объект физически неразличим → W1-06/violation_methods. **Stop:** любое смысловое несоответствие; на один проход ограничить ручной просмотр заранее выбранной стратифицированной выборкой, записать покрытие. **Предел:** выборочная проверка не доказывает полноту всего датасета и не подтверждает generalization.

<a id="e034"></a>

### E034 — Реальный update и локализация nonfinite

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-12-E02.

**W1-12-E02: исходная процедура** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):


**Входы:** прошедший E033 фиксированный positive batch, тот же checkpoint; инструментирование trainer/hooks без изменения loss. **Контроль:** неизменённый frozen reference tensor и выбранный trainable head tensor; точная стадия accumulation. **Действия:** выполнить forward/backward до одного подтверждённого optimizer step; записать loss components, requires_grad, None/zero/nonfinite gradients, unscaled norm и относительное изменение weight. Градиент проверять до zero_grad; отсутствие delta до границы accumulation не считать сбоем. При NaN сохранить воспроизводящий batch; один короткий повтор с amp=False, затем при необходимости autograd anomaly для traceback. Не превращать repeat с FP32 в сравнение качества.

**Метрики/артефакты:** step count, param_groups LR/decay/betas/momentum, AMP check passed/skipped/failed, scaler state/scale, norm до clip, weight deltas, first failing operation, batch hashes/log. **Исход:** finite+update → E035; absent grad/update → loss/freeze/optimizer wiring; только AMP failure → FP32 как диагностический route, затем установить поддержку precision; failing input → E033. **Stop:** первый nonfinite; для исходного batch не более двух сравнительных precision попыток и одного traceback, без автоматического длинного retry. **Предел:** один update не доказывает сходимость; grad≠0 не доказывает правильность labels или полезность направления обновления.

<a id="e035"></a>

### E035 — Tiny overfit и обязательный reload

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-12-E03, W2-11-E01.

**W1-12-E03: исходная процедура** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):


**Входы:** E033/E034 passed; выделенный diagnostic train set, например 8–16 независимых кадров (это наш предлагаемый бюджет, не target label budget), видимые объекты и понятные labels; baseline predictions. **Контроль:** одни и те же кадры/checkpoint/size; augmentation явно минимизирована, weight_decay=0 как диагностическая абляция, не финальная recipe; явный optimizer и LR из одобренного baseline; warmup/scheduler/accumulation заранее записаны. Для короткого run учесть F153 и warmup capped E−1. Намеренное использование train images для этой проверки явно маркируется sanity-only; validation результата не публикуется как перенос.

**Действия:** ограниченно обучить на этих примерах, смотреть loss и boxes именно для них; затем сохранить artifact, завершить процесс, загрузить заново и повторить те же входы. Сравнивать EMA с EMA/reloaded model: сравнение online weights с EMA без оговорки создаёт ложное расхождение. До запуска согласовать практический допуск по localization/classification и численный tolerance outputs для выбранных dtype/backend; exact byte equality не обещается.

**Метрики/артефакты:** optimizer updates, loss components, train per-class recall/precision при фиксированных thresholds и IoU, overlays, checkpoint checksum, config/seed, до/после reload predictions и численное расхождение. **Исход:** выучил и reload совпал → E036; выучил, reload расходится → artifact gate; не выучил → остановить full training и вернуться к E033/E034/head/loss, затем scale/visibility. **Stop:** первый nonfinite; максимум 300 реальных optimizer updates или 15 минут wall-clock, что раньше (предложенный диагностический cap); не более одного исправления установленной причины с повтором. Непрохождение cap не доказывает невозможность научить модель, только отсутствие допуска к дорогому trial. **Предел:** memorization не подтверждает independent quality, event logic, export или LinQ.

**W2-11-E01: W2 операционная поправка/дополнение** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)):


**PROPOSED, не выполнено; дополняет E035 и E046/E04, не отдельный quality trial.** Решение: допускается ли recipe к длительному training и передаче artifact. Входы: pinned package/environment, допустимый unfused model/teacher hashes, небольшой fully reviewed train diagnostic set, независимые development inputs, selection/rule manifest. Budget/success tolerance назначить заранее из фактической среды. Lockbox не открывать; correctness predictions не считать quality evidence.

1. В bounded smoke зарегистрировать copy callback до train; проверить после setup mask, BN flags/buffers, optimizer groups и callbacks registration. Снять online/EMA tensor manifests раздельно. Получить хотя бы один successful save и hash immutable copy; сверить zero-based epoch, last/best/epochN равенство bytes там, где они должны происходить из общего buffer, и ledger.
2. В новом процессе inspect trusted pre-strip checkpoint: model=None, ema есть; optimizer/scaler/stopper/epoch/updates/args корректны; все необходимые tensors finite. Для KD teacher=None внутри EMA, projectors есть, внешний teacher hash доступен. Затем на **копии** проверить штатный resume: start_epoch+1 contract, optimizer state/param ordering/dtypes, scaler, stopper best epoch, EMA count, reconstructed scheduler LR, first actual update и BN policy. Записать ожидаемые отличия online/EMA/rounding/RNG; не требовать битового совпадения.
3. Нормально закончить smoke; проверить last/best stripped fields и отсутствие KD wrapper/projectors в final graph, periodic/callback copy всё ещё pre-strip. Загрузить student derivative в другом process без teacher path для inference. Сравнить outputs с тем же serialized pre-strip EMA student, одинаковые inputs/mode/precision/postprocess, заранее допустимая погрешность; live FP32 EMA не подменяет reference без учёта FP16 save.
4. Проверить новую stage2 `resume=False`: epoch0; fresh optimizer/scaler/EMA updates/stopper/scheduler; ожидаемые weights переносятся; freeze=0 снимает planned layers, DFL/teacher остаются fixed; BN stats и gradients соответствуют политике. Для supervised явно distill_model=None. Один finite фактический update с новым LR подтверждает wiring, не полезность.

Observables: exact args/log/ignored overrides, code+environment+weight hashes, model/optimizer state summaries, original and restored epochs/EMA updates, per-group LR/decay/betas/momentum, trainable names/BN deltas, first update, serialized candidate predictions, save/val/reload wall time, files+ledger. Soft time-stop отдельно при необходимости проверяет partial epoch и превышение cap, не оценивает качество. Hard-kill simulation не обязательна: достаточно не обещать гарантии за пределами completed copies.

Outcomes: корректный copy/reload/stage switch → reuse W1-15 controlled comparison/export gate; state mismatch → остановить длинный run и локализовать interface/version/mask; final inference требует teacher → KD extraction gate failed; неприемлемая serialized parity → не promote этот artifact. Stop: missing/неfinite state, wrong class mapping/mask, отсутствующая immutable copy, unexpected new run вместо resume или unexpected distillation. Успех не подтверждает convergence, benefit, bitwise continuation, target quantization или LinQ.

<a id="e036"></a>

### E036 — Только проверяемая оптимизационная гипотеза

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-12-E04.

**W1-12-E04: исходная процедура** ([ветка](_WORK/W1/12_OPTIMIZATION.md)):


**Входы:** E035 passed; реальная train/val с независимыми camera/session groups, untouched lockbox вне tuning, baseline и заранее выбранная практическая метрика evaluation. **Контроль:** одинаковые source weights, train/val, sampling, resolution, transforms, seed, postprocess; фиксированный optimizer для LR sweep. **Действия:** сначала baseline, затем один кандидат; например LR понижен при подтверждённых spikes/oversized updates, или изменён warmup при проблеме начала training. Конкретное число выбирается после baseline, не назначается как universal recipe. Batch/accumulation проверять отдельным опытом: равный effective batch не делает BN/decay/updates равными. Scheduler/close_mosaic/early stop аблировать отдельно, с фактическими LR curves и количеством пройденных фаз.

**Метрики/артефакты:** mAP50:95 и per-class/size breakdown, критичные misses и FP по согласованному evaluation protocol, валидированный checkpoint по заранее фиксированному selection, wall-clock/updates/GPU peak memory, error gallery, run manifest и logs. Встроенный best.pt может оптимизировать другую цель, чем event-level safety requirement; заранее согласовать сохранение кандидата. **Исход:** выигрыш достаточен → W1-15 conditional repeat/selection и далее export gate; нет выигрыша/регрессия редкого класса → baseline; одинаковая проблема при всех recipe → данные/scale/domain. **Stop:** первый неустранённый nonfinite, OOM после согласованного снижения batch, отсутствие пригодного checkpoint; заранее установленный time/update cap и число кандидатов (для первого опыта baseline+один). Увеличение бюджета только после содержательной причины. **Предел:** один seed на одной validation не доказывает устойчивый выигрыш и ничего не устанавливает о LinQ.

<a id="e037"></a>

### E037 — Парная FP→export→quant→target проверка

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-13-E01, W1-15-E04.

**W1-13-E01: исходная процедура** ([ветка](_WORK/W1/13_COMPRESSION.md)):


**Вопрос/решение:** где возникает потеря и какой артефакт пригоден для интеграции? **Входы:** выбранные model/checkpoint/exporter revisions от model_stack; неизменный class map; реальные независимые frames/clips с labels и camera/session IDs; отдельный calibration pool; SDK/device access для целевой части.

**Контроль:** одна и та же исходная картинка не гарантирует один input. Сохранить и подать одни и те же фактические input tensors (hash, dtype, shape, layout, channel order, normalization), с фиксированными decode/resize/letterbox/padding и обратным mapping координат. Если SDK требует другой input dtype, документировать преобразование и сравнивать эквивалентный контракт, не скрывать его. Зафиксировать batch, static/dynamic dimensions, eval mode, preprocessing, output names/order, logits/decoded boxes, class mapping, thresholds, NMS, top-k и coordinate convention. Не перенастраивать пороги между кандидатами в основном сравнении.

**Действия:** (1) native FP → FP ONNX; (2) FP ONNX → preprocessed FP graph; (3) тот же граф → quant graph или штатный compile/quant route; (4) фактическое target execution. Для каждой соседней пары сохранить raw outputs на одинаковых inputs; отдельно проверить общий event pipeline на тех же clips. Если target FP невозможен, native/ORT FP остаётся reference, но target delta объединяет эффекты compiler и quantization; это явно подписать.

**Метрики:** max/relative tensor deviations там, где tensors сопоставимы; detection AP с указанным IoU protocol, recall/precision по классам/size/camera, критичные пропуски; event recall/false alarms только при неизменных правилах. Считать paired differences на тех же независимых единицах, включая примеры расхождения до/после NMS.

**Артефакты:** hashes checkpoint/graphs/inputs, export args, manifests splits, calibration IDs, версии инструментов, compiler logs, placements/fallback/precision, raw outputs, metric config, визуальные пары ошибок. **Исходы:** FP export плох → чинить export; preprocessing optimization плоха → разбирать fusion; quant плох → E038; target-only плох → compiler/runtime investigation. **Stop rule:** прекратить дальнейшую компрессию при нарушенном FP parity или неизвестном input contract. **Предел:** успех ORT не подтверждает LinQ; успех на небольшой выборке не гарантирует редкие камеры/события.

**W1-15-E04: W2 операционная поправка/дополнение** ([ветка](_WORK/W1/15_SELECTION.md)):


**Гипотеза/решение:** выбранный bundle сохраняет качество и пригодность после реального пути преобразования. **Входы:** frozen A/B и выбранные settings, untouched GT lockbox E045, отдельный calibration/train material, actual exporter/compiler/runtime versions. **Контроль:** одинаковые canonical input frames, class map, geometry/color/normalization, NMS/caps/rules и evaluator; никаких новых labels/threshold tuning по lockbox. **Действия:** сначала на рабочей parity validation сравнить source FP с reloaded FP, затем FP export, quantized artifact и целевой runtime последовательно, чтобы локализовать изменение. Сохранять raw outputs где доступны, decoded predictions, error/matching differences. Отдельно измерить качество каждого этапа; numerical closeness полезна для debugging, но не заменяет GT metrics. После выбора реального deployment bundle выполнить заранее запланированную финальную lockbox оценку против замороженного baseline; получить решение по контракту.

**Метрики/артефакты:** numerical deltas с dtype-specific допуском, bbox/class/count differences, paired detector/event metrics/support; exporter flags/opset, quant calibration IDs/hash, compiler options/logs, runtime/device identity, unsupported ops/fallbacks, bundle checksums. Latency/throughput/end-to-end exposure — по video_architecture на реальном устройстве отдельно от quality. **Исходы:** FP хорошо, export плохо → preprocessing/decoder/export gate; quant плохо → calibration/precision/W1-13; целевое исполнение отсутствует → статус target-unverified; все gates проходят → promotion/rollback bundle фиксируется. **Stop:** любой неподтверждённый class map/output contract, критичный quality regression или невыполненное обязательное target execution; не продолжать адаптацию на lockbox. Если по его ошибкам исправили систему, набор стал development: новая независимая проверка нужна для нового claim. **Предел:** ORT/RTX/source FP успех не доказывает LinQ; один lockbox не подтверждает industrial safety/SLA или другие камеры.

<a id="e038"></a>

### E038 — Calibration и локализация PTQ loss перед QAT

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-13-E02.

**W1-13-E02: исходная процедура** ([ветка](_WORK/W1/13_COMPRESSION.md)):


**Гипотеза:** потеря определяется покрытием activation ranges/несколькими узлами и может быть снижена без нового training. **Входы:** прошедший E037 FP graph; calibration pool из разрешённых development cameras/sessions; validation labels; exact target quantizer contract. **Контроль:** одинаковый FP graph, inputs, split, thresholds/NMS; менять одну calibration стратегию за сравнение. Не использовать финальный holdout для выбора метода.

**Действия:** проверить представительность lighting/scale/background/positive/negative и повторов соседних кадров; сравнить несколько обоснованных subsets и доступные calibration algorithms. В ORT исследовательской ветке S112 даёт reader interface; S113 позволяет activation matching. Для LinQ использовать только полученный SDK interface. При локализованном узле проверить исключение/mixed precision лишь если target поддерживает.

**Метрики/артефакты:** из E037 плюс histogram/ranges/scales, saturation/clipping при доступности, IDs calibration frames и activation divergence. **Исходы:** устойчивое PTQ удовлетворяет критериям → оставить PTQ; loss остаётся и target QAT contract известен → E039; contract неизвестен → Q008, не запускать произвольный QAT. **Stop rule:** остановить перебор при заранее заданном лимите candidate checks или отсутствии релевантного улучшения; лимит назначить по фактическому времени. **Предел:** улучшение calibration validation ещё требует независимого подтверждения.

<a id="e039"></a>

### E039 — QAT или pruning как отдельное вмешательство

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-13-E03.

**W1-13-E03: исходная процедура** ([ветка](_WORK/W1/13_COMPRESSION.md)):


**Входы:** E037 baseline, установленные Q008/Q023; train labels и разрешённые development данные; для pruning — реальная graph surgery или подтверждённый sparse backend. **Контроль:** отделить QAT от дополнительного FP fine-tuning: сопоставить исходный FP, продолженное FP training с сопоставимыми данными/updates, PTQ и QAT export. Для pruning сохранить непрореженный baseline и comparable recovery training. Не менять одновременно resolution/head/classes и attribution.

**Действия:** QAT симулирует установленную target arithmetic; экспорт и прогон обязательны. Pruning фиксирует topology, pattern, удалённые channels, dependent layers; проверить shape/outputs до recovery training и повторить E037 после него. **Метрики:** качество по критичным slices; serialized bytes отдельно от package archive; parameter counts и FLOPs с convention отдельно; actual target model-only latency/peak memory отдельно от end-to-end video latency/throughput.

**Контроль времени:** одинаковые batch/concurrency/input shape, warmup, режим синхронизации, device/SDK, load, transfers и включённые стадии; latency distributions и очередь, без подмены network/RPC/decoder overhead временем модели. **Артефакты:** topology/masks, seeds/config, training checkpoint selection, quant params, compiled artifact и placement log, timing protocol. **Исходы:** меньше FLOPs без ускорения → не заявлять speedup; ускорение ценой критичного recall → отказ/другой компактный baseline; target artifact проходит оба критерия → кандидат интеграции. **Stop rule:** прекратить при несовместимости graph или неподтверждённом target pattern, до дорогого recovery training. **Предел:** локальный runtime speedup не гарантирует ускорение удалённого многокамерного сервиса.

<a id="e040"></a>

### E040 — Найти bottleneck до масштабирования

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-14-E01.

**W1-14-E01: исходная процедура** ([ветка](_WORK/W1/14_COMPUTE.md)):


- Входы/контроль: рабочий single-GPU train; тот же dataset/config/precision/seed; representative object counts и размеры, включая тяжёлые batches. Сначала correctness gate W1-12. Разрешение и модель не менять ради красивого throughput.
- Действия: записать cold setup отдельно; после прогрева ограниченное окно обычного train, затем короткий CPU/CUDA profiler с wait/warmup/active. Разметить получение batch, preprocessing, H2D, forward/loss, backward, update, validation/save. Для реального throughput повторить окно без profiler; дождаться GPU на границах (S123/S128).
- Метрики: processed images/s и unique images; step p50/p95, update count, loader wait, CPU/RAM/disk/network, peak allocated/reserved VRAM, kernel/communication timeline. Stage times при overlap не суммировать как независимые расходы.
- Артефакты: trace JSON, key averages, hardware/software manifest, timestamps и обычный throughput log; cold/warm и profiler on/off различены.
- Исходы: loader stalls → E041; GPU compute → кандидаты batch/precision из W1-12; communication только после DDP → E042. Нет CUDA trace → проверить supported activities/CUPTI, не угадывать bottleneck.
- Stop: заранее ограниченное диагностическое окно (например, до 100 измеряемых batches как предлагаемый cap, не факт скорости); OOM/NaN/ошибка labels немедленно прекращают performance-ветку. Достаточно локализованного bottleneck, не нужен полный train. Предел: профиль окна не предсказывает весь run с validation/close_mosaic/разными object counts.

<a id="e041"></a>

### E041 — Workers и cache с учётом старта

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-14-E02.

**W1-14-E02: исходная процедура** ([ветка](_WORK/W1/14_COMPUTE.md)):


- Входы/контроль: E040, неизменные model/data/augmentation/precision; записанное состояние `.npy`, filesystem cache, RAM и shared memory. Изолировать от других jobs. Не удалять пользовательский cache ради теста: отдельная snapshot-копия/каталог по согласованной инженерной процедуре.
- Действия: сравнить baseline с небольшим увеличением workers; затем отдельно False/disk/ram при достаточном ресурсе. Менять один фактор, включать build time; повторить warm window. Образцы реально полученных images/labels проверить на равенство контракта.
- Метрики/артефакты: startup, first epoch, steady images/s, RSS/PSS где доступно, shared memory, disk bytes/I/O, actual workers/prefetch, warning logs; manifest cache mode и mtime/содержимого. Если ОС не даёт PSS, явно указать ограничение RSS и double counting shared pages.
- Исходы: выбрать минимальную сложность с полезным T_ready; RAM, вызывающий swapping, отвергнуть; cache, который не окупается на числе плановых epochs/trials, не включать ради максимума images/s.
- Stop: превышение заранее установленного headroom RAM/disk/shared-memory или деградация окна → остановка варианта; cap числа вариантов до запуска. Предел: faster loading не гарантирует quality; RAM warning о determinism остаётся существенным.

<a id="e042"></a>

### E042 — Один run DDP против независимой очереди

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-14-E03.

**W1-14-E03: исходная процедура** ([ветка](_WORK/W1/14_COMPUTE.md)):


- Входы: реально доступные несколько GPU, compatible OS/backend и доступ к одному snapshot; workload после E040/E041. Сначала фиксировать доступный topology и failed-launch budget. Аренда не разрешена этим исследованием и не выполнялась.
- Контроль: одинаковый global batch и measured optimizer updates/sample exposure; fixed model, resolution, precision, recipe. Если local batch/BN/order/rect/accumulation неизбежно меняются, отметить это и проводить отдельное quality comparison, а не заявлять чистую hardware абляцию.
- Действия: короткий single-GPU и N-GPU workload, учесть startup/validation/save; trace каждого rank с уникальным именем; проверить actual sampler indices/update/accumulate и reductions. Отдельно N независимых trials с назначенными GPU и общим I/O нагрузить только в рамках малого диагностического окна.
- Метрики/артефакты: T_ready, S_N/efficiency, GPU-hours, per-rank utilization/VRAM/loader wait/collectives; logs env/rendezvous/backend и effective config, качество smoke-validation. Порты/output dirs отдельные; любые custom objects должны быть доступны subprocess.
- Исходы: DDP сокращает критический путь при принятой цене → финальный established recipe; contention/communication/startup съедают выигрыш → independent trials либо single GPU. Несколько слабых/разных машин через сеть не считать одним быстрым узлом.
- Stop: failed startup/расхождение данных/collective hang/time cap → прекратить диагностику, сохранить traceback; не тратить остаток подготовки на неизвестный distributed stack. Предел: короткий scaling-test не доказывает одинаковую сходимость и не переносится на RTX 4070/облако другой конфигурации.

<a id="e043"></a>

### E043 — Цена доразметки против ещё одного compute trial

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-14-E04.

**W1-14-E04: исходная процедура** ([ветка](_WORK/W1/14_COMPUTE.md)):


- Входы: установленный тип ошибки на development-пуле; несколько независимых новых сцен, не test; annotation specification и независимый validation. Число кадров не назначено до появления данных. Контроль A — прежние данные и такой же рецепт; B — проверенная добавка данных; C при необходимости — продолжение A с сопоставимой дополнительной compute exposure.
- Действия: зафиксировать budget в person-minutes, images/objects и независимых scenes; учесть QA и correcting prelabels. Обучить B с тем же checkpoint и одинаковым правилом selection, сравнить A/C по ранее выбранному error slice и общим классам. Compute и annotation бюджеты отчитывать раздельно: это разные единицы.
- Метрики/артефакты: quality delta/FP/recall редких классов с поддержкой по группам, annotation/review/transfer/train elapsed, label changelog, frozen splits и predictions; paired repeats только когда требуется W1-15.
- Исходы: B закрывает пробел → следующая обоснованная порция labels; C лучше → исследовать learning limitation; ни один → пересмотреть visual signal/постановку. Stop: невалидная или неоднозначная разметка сначала разрешается, train прекращается; после исчерпания предзаданного budget без полезного эффекта ветка не расширяется автоматически. Предел: одна порция не устанавливает универсальную learning curve.

<a id="e044"></a>

### E044 — Условия назначения seeds, teacher и длинного run

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-14-E05.

**W1-14-E05: исходная процедура** ([ветка](_WORK/W1/14_COMPUTE.md)):


- Входы/контроль: узкая очередь максимум нескольких объяснимых кандидатов, текущая стоимость E040, независимый validation. Записать решение, минимально полезный эффект и предел wall-clock до начала. Для teacher нужен подтверждённый путь к конечному student от W1-10/model_stack.
- Действия: если ranking близок к observed training noise, paired seeds A/B, а не «ещё seed только победителю»; если ошибка domain coverage — annotation E043; если teacher даёт полезные prelabels, учитывать ручную коррекцию и student training; если validated learning curve ещё полезно растёт — продление с сохранением recipe/selection.
- Метрики/артефакты: per-seed и per-group результаты, teacher QA/student delta, время людей и GPU, decision log и оставшийся integration path. Seed/split протокол не изобретать вместо W1-15/evaluation.
- Исходы/stop: продолжать только ветку, которая ещё может изменить конечный выбор до срока. Нет времени получить validation/export artifact — сохранить лучший уже проверенный кандидат. Stop по data leakage, невоспроизводимому config, потерям критичных классов или исчерпанию заранее назначенного budget. Предел: повтор seed не устанавливает перенос на новую камеру; teacher успех не проверяет student/LinQ.

<a id="e045"></a>

### E045 — Зафиксировать выбор и независимые partitions

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-15-E01.

**W1-15-E01: исходная процедура** ([ветка](_WORK/W1/15_SELECTION.md)):


**Гипотеза/решение:** данные позволяют сравнивать адаптацию в нужном режиме переноса. **Входы:** source/target inventory, GT schema/coverage, camera/session/episode/time IDs, checkpoint SHA256/commit; требования evaluation. **Контроль:** untouched lockbox исключён из training, active/pseudo/calibration/threshold pools; patient-like group principle F182 адаптируется к camera/session. **Действия:** определить operational population; сформировать train, рабочую val, lockbox по группам до frames/crops; проверить hashes/duplicates/time overlap и происхождение labels; зафиксировать selection objective, constraints и число candidates. Для одной камеры явно ограничить claim будущими sessions; если independent holdout невозможен — exploratory protocol.

**Метрики/артефакты:** partition manifests с hashes и ролями данных, overlap audit, per-class objects/episodes/groups/exposure, selection contract, журнал доступа к lockbox. **Исходы:** независимость и support достаточны → E046; leak → пересобрать до training; rare support отсутствует → доразметка/сбор отдельного материала и N/A в текущем отчёте. **Stop:** не начинать подтверждающий trial при leak/неопределённом matching; не обещать покрытие отсутствующего класса. **Предел:** audit не доказывает полноту labels и не гарантирует перенос за пределы представленных камер/условий.

<a id="e046"></a>

### E046 — Отделить обучение от порога/NMS/правила

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-15-E02.

**W1-15-E02: исходная процедура** ([ветка](_WORK/W1/15_SELECTION.md)):


**Гипотеза/решение:** candidate улучшает weights, а не только настройки решения. **Входы:** A baseline, B один обученный candidate с уже пройденными W1-12 gates; одинаковая val E045, зафиксированный evaluator. **Контроль:** в первом сравнении preprocessing, confidence/NMS/caps, event rule и matching одинаковы; всё различающееся в train recipe/данных записано как intervention. **Действия:** сохранить predictions/scores; сравнить A и B при общих settings. Отдельно на рабочей validation выбрать `theta_A` и `theta_B` одинаковой процедурой; измерить таблицу A/B × theta_A/theta_B, если семантика settings совместима. Если новое preprocessing/crop/graph необходимо, назвать опыт bundle comparison и добавить изолированную абляцию, иначе причинного вывода о training нет.

**Метрики:** detector AP с полными settings, per-class measured AP/support, operating recall/precision, event TP/FN/FP, FP/exposure, базовые/редкие классы и камеры. **Артефакты:** raw/retained predictions, evaluator/version, configs, PR data, error gallery и таблица четырёх combinations. Если export скрывает pre-NMS tensors, ограничение фиксируется. **Исходы:** B лучше при общих settings → E047; выигрывает только настроенное правило → принять как rule improvement и оценить отдельно; общий gain скрывает critical regression → не promote. **Stop:** заранее заданное число threshold/rule candidates; одинаковый trial budget для A/B, никакого lockbox tuning. **Предел:** одна val/один training run не доказывают устойчивость; object AP не подтверждает event recall.

<a id="e047"></a>

### E047 — Условные парные повторы и grouped uncertainty

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W1-15-E03.

**W1-15-E03: исходная процедура** ([ветка](_WORK/W1/15_SELECTION.md)):


**Гипотеза/решение:** преимущество сильного кандидата устойчиво к главному источнику неопределённости. **Входы:** A/B E046, fixed grouped val, runnable recipe, фактическая стоимость запуска. **Контроль:** одни training manifests/source weights/budget и selection criterion внутри пары; одинаковые group indices при анализе. **Действия:** сначала выделить вопрос. (a) Optimization sensitivity — повторить A/B на тех же данных с другим optimization seed; по возможности paired seeds, но одинаковый номер не гарантирует одинаковые RNG streams при разных графах. (b) Few-shot sample sensitivity — другая training-shot группа из train pool с тем же label budget; A/B используют одинаковую новую группу, optimization RNG записан отдельно. (c) Camera transfer — заранее заданный дополнительный development group split; внутри него selection повторяется без доступа к внешнему lockbox. Не называть эти три проверки одной величиной seed variance.

Для каждой пары сохранить Delta; сообщить все pair results, median/range и число repeats, включая неудачи. При достаточном числе независимых evaluation groups выполнить paired group bootstrap F183 с заранее заданными confidence/method/resamples/RNG, пересчитывая статистику. Для nested cameras/sessions выбрать resampling level по claim; нельзя считать sessions независимыми cameras. При нескольких seeds на одной val не умножать число независимых scenes на число seeds. При degenerate/too-small support report interval unavailable и raw counts, без выдуманной точности.

**Артефакты:** отдельные sample/optimization/split/resampling seeds, train hashes, все checkpoints и выбора epoch, paired metrics/deltas, group counts, resampling indices и валидность CI. **Исходы:** стабильный практически значимый выигрыш без критичных регрессий → заморозить bundle; смена знака → сохранить baseline и исследовать coverage/ошибки; неопределённость из-за малого числа scenes → добавить реальные независимые данные, а не бесконечные optimizer seeds. **Stop:** до запуска записать максимум repeats и reserve; после его исчерпания результат inconclusive либо provisional. Не добавлять runs только до первого значимого результата. **Предел:** редкий повторный seed не даёт надёжного population CI; bootstrap val не оценивает training-sample variance сам по себе и не исправляет selection bias.

<a id="e048"></a>

### E048 — Отделить detector-specific components от одинакового backbone

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W2-06-E01.

**W2-06-E01: исходная процедура** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)):


**Статус: будущая процедура, не выполнена.** Расширяет initialization часть E004; не повторяет freeze/full grid. Решение: стоит ли использовать конкретный готовый detector-pretraining artifact, если та же допустимая architecture имеет backbone-only initialization. Прямой runnable route здесь DETReg; использовать его как практический trial можно лишь если model_stack допускает такую architecture и есть target execution path. Для выбранного другого detector нужна эквивалентная audited loader interface; команды не выдумываются.

**Входы.** Пригодный checkpoint C с hash/config и ancestry, поддержанный trainer pin, tensor inventory, ontology и полные целевые annotations; camera/session/episode-disjoint train/development/закрытая assessment. Нужны независимые positive groups по критичным классам и старым обязательным условиям. Не задаём число кадров, epochs или ожидаемый gain без данных. Отдельно документируем source↔target overlap и допустимость unlabelled exposure.

**Стартовая пара.** A — общий backbone B, остальные detector tensors из фиксированного случайного состояния R. B-arm — те же **побитно совпадающие backbone tensors B**, а transformer/neck/localization/query components из C; class head создаётся из того же R в обоих arms. В DETReg object-embedding ветвь отсутствует в обоих downstream graphs; `class_embed` не используется. При наличии class-specific box head с несовместимыми labels нельзя оставить source regressor только в одном arm без явного определения вмешательства: его либо совместимо преобразуют в обоих, либо исключают из сравниваемой transfer mask. Сохранить списки каждого imported/reset tensor, normalization buffers и missing/unexpected keys.

**Что сравнение означает.** Это абляция полезности дополнительных detector components **данного C**, сверх его же backbone. Она не сравнивает весь SSL recipe с classification, не ранжирует source datasets и не учитывает стоимость создания C как равную нулю. Если C backbone изменялся при pretraining, он всё равно копируется одинаково в оба arms; общий предшествующий knowledge остаётся. Сравнивать разные готовые source detectors вместо этой пары разрешено как операционное package comparison, но это уже иной вопрос и не чистый ответ E048.

**Контроль и действия.**

1. До training выполнить будущий loader/forward/save/reload smoke, inventory graph и raw input/output. Проверить, что A/B имеют одинаковые class rows, data convention, parameter shapes и inference topology. Исходный C хранить отдельно. Прекратить при незапланированном mismatch, чужих class rows или невалидных labels.
2. Зафиксировать trainable mask/BN policy, input resolution, augmentations, minibatch/sampling, optimizer family и фактические LR groups, warmup/scheduler, update/real-image exposure budget и validation cadence. Основное сравнение — одинаковая supervised downstream recipe. Если нормализация или иная архитектурная деталь должна различаться, оформить как package comparison и не сохранять causal claim.
3. Назначить заранее численные acceptance margins после baseline/кейса: критичный recall/FN при одинаковой operating point, допустимые FP/время наблюдения, сохранение старых классов; selection по development objective, last/best/periodic checkpoints сохранить до перезаписи. Lockbox не выбирать checkpoint. Один одинаковый seed не означает отсутствие variance: при решающем отличии и достаточном бюджете повторить **ключевую пару** по дополнительному seed/sample-group, не весь каталог методов.
4. Обучить только эту пару в будущей практической волне; записать качество при одинаковом числе updates/exposures и время до выбранного пригодного artifact. Число updates и deadline — разные ограничения; не сравнивать early A с converged B как equal-budget результат. Затем один раз оценить выбранные candidates на assessment, per-class/per-camera/per-size. Event rules, thresholds и postprocessing должны быть общими.
5. Измерить separately `T_obtain+T_setup+T_downstream_train+T_validate+T_save+T_export`, human minutes, GPU time/peak memory и дополнительную предшествующую цену C. Провести actual export/quant/target verification выбранного результата; успех reference runtime не подтверждает LinQ.

**Артефакты.** Source/target manifests, hashes/configs/teacher ancestry, transfer-mask и load log, hashes общего backbone/head, actual optimizer/BN inventory, seed/sample lists, checkpoints и selector history, raw predictions/denominators, class/group metrics, clock/resource log, final inference graph/export/runtime identity. Training state и final inference weights хранить раздельно.

**Исходы/следующее решение.** Detector components дают устойчивый нужный выигрыш в рамках acceptance и стоимости — сохранить B и передать integration; качество одинаково — выбрать более простой/дешёвый проверенный artifact route; B хуже — rollback A, исследовать source mismatch/optimization только при содержательной причине; support недостаточен — preliminary результат и annotation, без выбора по шуму. Стоп: неверный data/load contract, nonfinite loss, отсутствие updates, нарушение split или исчерпание заранее согласованного cap; сохранить всё, не удлинять автоматически. Успех не доказывает superiority DETReg на другом detector/domain и не означает, что pretraining с нуля окупится.

<a id="e049"></a>

### E049 — Будущий QAT decision gate с точным контролем

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W2-09-E01.

**W2-09-E01: исходная процедура** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)):


Это уточнение E039 и E037, **не выполненный опыт и не отдельный обязательный trial для каждого метода**.

**Вопрос/входы.** При доказанной PTQ потере на нужных slices восстанавливает ли QAT качество в реально принятом LinQ artifact? Нужны Q023 lock и Q008 sample/contract, frozen supervised FP checkpoint с нужными classes, FP export parity, отдельные calibration/development train данные и независимые labeled camera/session groups. Не начинать по одному training flag или JPEG примерам автора.

**Контроль.** Сохранить исходный FP, FP continuation, PTQ и QAT, начатые от одинаковых weights. FP continuation и supervised QAT должны получать те же labels, order/exposures, augmentations, updates, optimizer budget и checkpoint-selection material; единственное основное вмешательство — target-matched fake quant. **Для найденного reconstruction script это другая постановка:** зафиксировать отсутствие GT loss; дать quant-disabled continuation с теми же images/hooks/optimizer/updates и отдельно назвать reconstruction objective. Такой FP self-reconstruction может почти не давать gradients, что ожидаемо и не равно сильному supervised FP baseline. Если добавлен detection loss/labels, это новый supervised port: одинаковый loss/labels нужен обеим веткам, и это нельзя назвать точным воспроизведением S196. Нельзя скрыто приписать QAT эффект teacher supervision, изменённой data exposure или новых annotations.

**Действия.** После bounded reload/forward/export smoke на development inputs проверить реальный QDQ graph: opset, dtype и ranges, zero points, per-channel axis/length, shared scales, оставшиеся FP islands, head outputs, shape. Сравнить reloaded native FP → FP export → QAT simulated → фактический post-export backend → compiled LinQ outputs на тех же canonical tensors. Если LinQ FP недоступен, target difference включает compiler и quantization, отдельно это записать. Для main comparison фиксировать preprocessing/NMS/thresholds, class map и event rules.

**Измерения/доказательства.** На каждой применимой стадии — AP с указанным IoU protocol, critical-class recall/precision, small-object/camera slices и paired errors; на event clips — fixed-rule event recall/false alarms. Numerical boundary tests — half-step, saturation, zero tensors; tensor differences помогают локализации, не заменяют GT metrics. Сохранять hashes configs/inputs/checkpoints/graphs, actual steps/exposures, selection history, quant params, exporter/SDK logs, fallback/precision/placement, raw outputs и независимые metric tables. Latency/peak memory измерять на actual device с fixed batch/shape/concurrency; модельное и end-to-end время отдельно. Точные бюджеты/допуски назначаются до опыта по фактическим данным/стоимости, здесь не выдуманы.

**Исходы/stop.** PTQ уже проходит constraints → оставить PTQ. FP export плох → чинить export до QAT. QDQ не принимается либо arithmetic меняется → остановить trial, вернуть Q008/штатный SDK путь. Simulated QAT улучшился, post-export ухудшился → investigate placement/arithmetic, не promote checkpoint. Target quality и performance проходят заранее заданные критерии против continuation/PTQ → freeze bundle и выполнить согласованный final holdout gate. Inconclusive/critical recall regression → rollback. Успех TensorRT/reference runtime не закрывает ни LinQ execution, ни camera generalization.

<a id="e050"></a>

### E050 — Будущий bounded smoke → recovery → export gate

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W2-10-E01.

**W2-10-E01: исходная процедура** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)):


Это уточнение pruning части **E039**, с reused FP/quant/target parity из **E037** и clean artifact принципом **E028**. Процедура **не выполнена**. Её цель — решить, заслуживает ли physical pruning дорогого recovery и сравнения с native student; это не grid по pruning ratios.

**Входы:** разрешённый конкретный trained YOLOv8 U checkpoint/hash; TP T и environment lock, установленный smoke environment; custom class source с importable path; согласованные data/head nc/names; train split, development selection split и отдельно закрытый camera/session/episode holdout; native smaller student и непрореженный reference. От linq_platform нужны compiler/import contract, ограничения shapes/opset и затем target access. Критерии quality/runtime и предел engineering budget задаются до trials по полному кейсу; здесь числа не выдумываются.

1. **До surgery:** inventory module tree/keys/shapes/params, nc/names/reg_max/strides, input tensor hashes и raw outputs на representative examples; зафиксировать уже работающий native reference. Проверить pinned imports и путь custom class. Если фактический выбранный detector не U YOLOv8, не выдавать этот script за готовую интеграцию: отдельная port задача только при наблюдаемой необходимости.
2. **Conversion-only gate:** в будущей практике заменить C2f без удаления, проверить eval outputs и AP/critical slices на тех же inputs против original. Отдельно осмотреть BN state, shortcut/group settings. При несогласованности остановить route до pruning/recovery; иначе последующая потеря будет иметь смешанную причину.
3. **Один малый surgery smoke:** autograd включён, выбранный static input; сохранить DepGraph/group listing, root и dependent deleted indices, все changed tensor shapes, concat offsets, residual equalities и head exclusions. Проверить train forward/loss/backward/finite gradients и eval forward; nc/box/DFL outputs не изменились. Выполнить full-object save и clean-process reload с versioned class, сравнить raw outputs. На этом же candidate выполнить FP ONNX export/checker и reference parity; при доступном SDK — ранний compiler acceptance/placement smoke новых shapes. До успеха этих gates большое recovery не назначать.
4. **Recovery comparison:** из одного исходного target checkpoint сохранить unpruned FP continuation control с сопоставимыми labels/updates и pruned recovery, плюс отдельный native smaller student с честно записанным budget/initialization. Нельзя сделать вид, что toy 10 epochs demo — честный оптимальный protocol всех трёх. Данные, resolution, thresholds/NMS, selection objective, разрешённые аугментации и accounting фиксируются; различия budget сообщаются. Stage selection использует development split и immutable candidates, last rejected stage не экспортируется. Holdout не используется для выбора ratio/stage.
5. **Final artifact gate:** reload accepted stage в чистом процессе; экспорт явного artifact/hash с фиксированными opset/input/batch/dynamic/simplify/precision/output contract; повторить E037 FP→export→quant/compiler→target. Замерить target model-only latency distribution/peak memory при одинаковом batch/concurrency/inputs/warmup/sync/transfer boundary, placement/fallback, а end-to-end video delay отдельно. Одно ORT совпадение не закрывает target gate.

**Метрики и сохраняемые доказательства:** conversion/reload/export tensor deltas; detection AP с точной метрикой, critical recall/precision по class/size/camera и paired errors; event metrics только при неизменных event rules. Отдельно actual dense tensor shapes, параметров/MACs counting convention, bytes model/package, target latency/memory и полная цена `T_setup+T_recovery+T_validate+T_save+T_export+T_decision` и human minutes. Сохранить hashes inputs/checkpoints/graphs/compiled file, environment/dependency locks, custom module, patched trainer source, pruning history/index mapping, class map/splits, logs/seeds/config/selection rationale, outputs и compiler placement report.

**Outcomes/stop:** conversion mismatch, head contract drift, incomplete group mapping, reload/FP export failure или compiler rejection → остановить до recovery, сохранить native candidate. Recovery нарушает critical quality gate → rollback accepted prior stage/штатный student; не экспортировать rejected current stage по demo break. Меньшие MACs без требуемого actual target результата → не продвигать по speed claim. Pruned проходит quality и target cost с допустимой ценой интеграции → кандидат, сравниваемый с native smaller student, а не автоматически победитель. Успешный bounded smoke ещё не подтверждает качество после полного recovery, редкие камеры, multicamera throughput или LinQ ускорение.

<a id="e051"></a>

### E051 — Будущая процедура выдачи следующей работы

**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.

**Состав:** W2-12-E01.

**W2-12-E01: исходная процедура** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)):


**Гипотеза/решение:** граф допусков позволяет получить пригодный artifact до его useful deadline и не тратить ресурс на unresolved prerequisites. Это процедура управления уже описанными E, не новый quality experiment и не выполненный scheduler benchmark.

**Входы:** actual task/acceptance/adaptation rules; versioned source/data/class/coverage manifests; candidate checkpoint hashes; W1-15 partitions; actual environment/SDK inventory; доступные люди/устройства и очереди; measured или явно unknown stage costs; current accepted rollback bundle; `D_useful` от реального потребителя. Нет target данных/SDK — отметить соответствующие blocked dependencies, выполнять независимые доступные gates.

**Контроль:** фиксированный parent reference, immutable decision log, единый evaluator/postprocess, одна causal hypothesis. Не сравнивать scheduling benefit только по GPU utilization; успех — timestamp usable artifact с достаточными quality/target доказательствами.

**Действия:**

1. Определить активный сценарий и earliest failed/unknown gate. Собрать карточку с expected artifact/schema/status, owner, two outcomes и заранее kill/accept/cap. При invalid task/data сначала исправить их; большой train не ready.
2. Переиспользовать неизменные gate results по contract key. Выбрать одно next discriminating comparison из строки; остальные hypotheses оставить pending с явным prerequisite, не запускать «на всякий случай».
3. Измерить неизвестную существенную стоимость bounded pilot; заполнить `CP_remaining`, resource/headroom и human-minute accounting. Admit только при feasible useful artifact path. Параллельную карточку допустить лишь без зависимости и contention критичных owners/data/SDK.
4. Записать effective recipe и fidelity purpose: correctness-only, matched-budget quality либо validated early proxy. По умолчанию **не** rank final quality коротким proxy. Pre-strip immutable save/serialized candidate evaluator зарегистрированы заранее; artifact recovery после strip не обещается.
5. По завершении сравнить pair на dev с support/critical constraints; запись outcome: kill текущую гипотезу, promote в следующий gate, inconclusive→один обоснованный repeat/annotation decision либо freeze reference. Повторить только affected gate после исправления причины.
6. Передать integration immutable bundle + manifest + predictions/metrics/support + target execution status + предыдущий bundle и smoke inputs. При conversion/target regression rollback целого bundle; если target не проверен, передать FP candidate как target-unverified и сохранить unresolved gate. Freeze/lockbox по W1-15; новые идеи не меняют уже переданный bundle без нового reviewable revision.

**Метрики/артефакты:** decision/dependency ledger, actual config/state/seed/exposure, timestamps каждой стадии и artifact-ready, H по операциям, GPU-hours, compiler/evaluator versions, raw/decoded predictions и denominators, immutable selected checkpoint/derivative/export hashes, saved rollback bundle. Отдельно причины невыданных/остановленных jobs, расхождения estimated vs actual CP и статус всех gates. Не обещать оптимальность очереди по одному случаю.

**Stop/предел:** leakage/class-map/coverage/nonfinite/reload/extraction error прекращает affected trial до качества; critical regression запрещает promote; исчерпание согласованной стоимости/невозможность timely downstream artifact прекращает расширение branch с сохранением последней пригодной точки. Успешная процедура выдачи не доказывает useful target gain, correctness не проверенных данных, перенос на absent cameras, industrial safety либо LinQ support без actual G4.

