# AUTHOR_HANDOFF — training_strategy

Сборщик прочитал оба входа, общие правила и роль COLLECTOR, PLAN/RUN_STATE, исходную критику, все 15 W1 и 12 W2. Усечённые ответы дочитаны диапазонами. Новой сети, обучения, генерации данных, модельного инференса, экспорта, pruning surgery и LinQ execution не было. W2-01 выполнил только служебное получение wheel ZIP, сравнение bytes и SHA.

Готовы [SOURCES.md](../SOURCES.md), [RAW_FACTS.md](../RAW_FACTS.md), [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md), outcomes в [CRITIC.md](../CRITIC.md). Реальные counts: 220 канонических S, 284 F, 51 E, 31 Q. S001 — пользовательская постановка. Сведены исходные 251 S / 292 F / 62 E / 154 Q; отличающиеся условия и версии сохранены. [ID_MAP.md](ID_MAP.md) даёт все branch→global связи; [COLLECTOR_BUILD.py](COLLECTOR_BUILD.py) воспроизводит служебную сборку без сети.

## Доказательная картина

Нужен связный рассказ о выборе следующего действия. Начало цепочки — воспроизводимая baseline и контракт наблюдения: смысл классов и событий, фактическое изображение после preprocessing, полнота annotations, независимые группы оценки, способ сохранения и ранняя feasibility LinQ. Наблюдаемая ошибка затем превращается в гипотезу и одно различающее сравнение. Методы не образуют обязательный набор; отказ или inconclusive результат тоже меняет решение, если сохранены причины и рабочий bundle.

Содержательный риск — неверное supervision или selection. Источник никогда не размечал класс, пропущен второй instance уже размечаемого класса, изображение полностью unlabeled и проверен настоящий negative — разные случаи. TXT/conversion может стереть различие ещё до loss. Небольшой полностью проверенный subset — конкретная условная альтернатива сложному trainer, но его превосходство и человеческая стоимость на наших данных не измерены. Тысячи соседних кадров не заменяют независимые эпизоды, камеры или отсутствующий визуальный сигнал.

Большой teacher может дать предразметку с коррекцией, поиск примеров, noisy labels, online EMA supervision или feature KD. Это разные вмешательства. Их стоимость и окончательная inference branch различаются; teacher AP нельзя сообщать как student AP. Confidence не подтверждает правильный class+box+wearing/event, а калибровка не восстанавливает объекты без detections.

Вторая волна дала положительные implementation contracts, а не только ограничения: опубликованный native KD package, конкретную YOLO11 пару, trace hidden-label negatives, авторские one-stage SSOD и source-free routes, detector QAT и физический pruning. Они остаются условными вариантами с точными prerequisites, доступными артефактами и локализованными gaps. Полезность на target не установлена.

Обязательный platform outcome — фактический инференс выбранного artifact на LinQ — не выполнен. Публичные заявления yolo5s/yolo8/yolo11, int8, Compiler и DNN Quant не определяют exact SDK/device/operator/quant contract. CPU/RTX/ORT дают reference и отладку; каждый selected student/graph должен пройти реальную цепочку reload→export→quant/compiler→target.

## Навигация для выборочного чтения

У F/E имеются стабильные anchors: ../RAW_FACTS.md#f001 и #e001; источники — ../SOURCES.md#s001, вопросы — ../OPEN_QUESTIONS.md#q001. В F сохранены тип основания, source/locator, actual read/run status, числа и условия. Важные W2 поправки стоят и у затронутых ранних F. Source blocks содержат bibliography/access, а не случайно захваченные fact/experiment blocks.

| Решение | F | E | Q |
|---|---|---|---|
| Baseline, причина ошибки, object против event | F001–F007, F080–F082, F186 | E001 baseline, E002 oracle stages, E003 visibility | Q001/Q004/Q010/Q017/Q029 |
| Малая разметка, limited/full, BN, class transfer | F008–F032, F234–F240 | E004 depth, E005 BN, E006 sample variance, E048 initialization | Q005/Q014/Q015/Q026 |
| Hidden class B, hidden instance C, assignment/ignore | F023–F031, F040–F042, F194–F205 | E007 A/B/C + W2 supplement; E008 sparse inference | Q003/Q013 |
| Rare exposure, RFS, weights, hard negatives | F033–F049 | E009 counts, E010 один balancing trial, E011 negatives vs diverse annotation | Q003/Q004/Q010 |
| Augmentation semantics и small-label survival | F050–F071 | E012 gate, E013 ablation, E014 tiny survival, E015 real degradation | Q001/Q017/Q018/Q019 |
| Resolution/tiles/cascade и полная цена | F072–F082 | E003, E016 input/tiles, E017 predicted crops, E018 scale training | Q007/Q009/Q017 |
| Domain mixing, retention, new session/camera | F083–F092, F241–F246 | E019 mixing, E020 source-free, E021 camera/rules | Q002/Q003/Q004/Q022 |
| AL, ручная разметка, CVAT, output scores | F093–F101, F220–F226 | E022 output/cost + equal minutes, E023 assistance | Q006/Q012/Q016 |
| Teacher admission, pseudo и online SSOD | F102–F114, F206–F219, F227–F233 | E024 audit, E025 corrected supervised, E026 online gate | Q011/Q013/Q021 |
| Native/heterogeneous KD, final student | F115–F129, F187–F193 | E027 native smoke+quality, E028 extraction, E029 FGD/LD | Q005/Q007/Q011/Q025/Q030 |
| Synthetic и Gen2Det gap | F130–F147, F247–F254 | E030 labels, E031 real transfer/exposure, E032 shortcuts | Q019/Q020 |
| Optimization, реальные updates, EMA/state | F148–F154, F272–F277, F193 | E033 loader, E034 update, E035 tiny/reload/save/stages, E036 optimizer | Q006/Q014/Q025 |
| PTQ/QAT/pruning/target | F155–F167, F255–F271 | E037 parity+lockbox, E038 calibration, E039 umbrella, E049 QAT, E050 pruning | Q007–Q009/Q023/Q024/Q031 |
| GPU/DDP/cost/queue | F168–F179, F278–F284 | E040 profile, E041 loader/cache, E042 DDP, E043 annotation, E044 dispatch, E051 queue | Q012/Q027/Q028 |
| Selection, independence, uncertainty, rollback | F177, F180–F186, F272–F277 | E045 partitions, E046 weights vs rules, E047 repeats, E037 frozen bundle | Q004/Q010/Q025/Q026/Q031 |

Global ranges здесь действительно последовательны; точные branch ranges после слияния раскрыты в базе и ID_MAP. 51 E — банк альтернатив и переиспользуемых gates, не 51 обязательный запуск. Исходные caps W1, например diagnostic tiny run до 300 updates или 15 минут, сохраняют статус предложений конкретного smoke test.

## Поправки W2, которые нельзя потерять

**Native KD — F187–F193.** Wheel 8.4.184 действительно получен; SHA256 d04c80f27d335fe27a057dcf00f91c843b11f99d21e7b3017616959a523bfc8a, десять contract files byte-equal U. U=e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 — следующий docs commit после release R=f7dd275e5853801674ca78ef51896617bb5362ba, не release tag. YOLO11n←target-trained YOLO11s имеет documented family support и code-supported стандартные grids/channels/strides. Runtime/quality/export/LinQ не проверены. Teacher сохраняет собственный task/nc/names; max-class weighting допускает другое nc технически, но не создаёт semantic knowledge нового класса. EMA payload уже teacher-free; wrapper/projectors остаются до final unwrap. Строка distill_model в final train_args не доказывает inference dependency.

**Partial labels — F194–F205.** В objectness-free U случай B допускает custom BCE column validity без безусловного изменения bbox loss, если остальные классы exhaustive. C требует другой spatial/negative policy; ignore не создаёт missing localization. Legacy YOLOv5 требует отдельного objectness handling. В active E2ELoss надо проверять обе assignments/loss branches; displayed logs только one-to-one. MMDetection crowd route class-agnostic, thresholds default -1, zero regular GT назначает всё background. Это static trace, не измеренный gradient test.

**One-stage SSOD — F206–F219.** UTv2 FCOS std branch остаётся Python eval field, стандартный cls_n_ctr ranking её не использует; удаление/export — proposed инженерная работа. Default evaluation teacher. EfficientTeacher active path — legacy YOLOv5, не generic current Ultralytics. Raw student, online pseudo teacher EMA и secondary best/export EMA различны. Domain heads вычисляются даже при нулевом loss, снимаются явно через --da. Export raw levels требует собственного sigmoid/grid/anchor decoder и parity.

**Acquisition и teacher audit — F220–F233.** Detect Results содержит original xyxy, scalar conf/cls; probs=None, boxes.data уже postprocessing. Low-confidence retained ranking не entropy. Нулевое число дополнительных forwards относится к score поверх уже выполненного pool inference, а не к полной стоимости acquisition. No-box/error/cap records и exploration входят в предложенную policy. Probability P и targeted D audit нельзя сливать в population rate без известного design. Calibration не восстанавливает recall пропусков. GT класса 0 → recall N/A; accepted 0 при GT>0 → precision N/A, recall 0. Degenerate CI unavailable. Никакая страта teacher пока не допущена к unchecked labels.

**Initialization — F234–F240.** DetCo representation не обученная detector head. DETReg передаёт localization/transformer/query компоненты, но pretrain loader удаляет class_embed; SwAV/FrozenBN ancestry существенна. Base/no-base сравнение меняет ещё и schedules, не чистый effect source-stage. Filename scratch означает no supervised base stage, а не отсутствие pretraining. Results/assets обновлены в 2023 при release label 2021; label не tensor hash. Готовый artifact и pretraining с нуля имеют разную цену.

**Source-free — F241–F246.** Simple-SFOD eval-only вызывает model.train/no_grad и AdaBN, до 1401 forward; frozen baseline так не получают. Активный путь не вызывает reset helper. JSON registration может оставаться target GT, подмена manual. Source ValLossHook создаёт source-label/state exposure, ordinary loss не чинит omissions. Repo найден; compatible source weights, lock, fixed-row selection и target usefulness не установлены.

**Synthetic — F247–F254.** Gen2Det author trainer/fork/config/schema не найден после primary paper/author/GitHub tracing. Это public artifact gap, не отсутствие capability. Paper p=0.2 — whole-batch probability; tau_i=0 — все synthetic background regions в RPN+head. Low-data COCO не применяет filtering/background-ignore. LVIS ablations немонотонны, COCO/XPaste comparison имеет отдельное происхождение. Fully reviewed whole synthetic images + ordinary supervised detector — наш data-only route, не reproduction Gen2Det. Equal updates при replacement не означает equal real exposure; draw ledger обязателен.

**QAT — F255–F261.** NVIDIA YOLOv7 finetune использует feature reconstruction MSE без detector GT loss. Это не supervised обучение новых PPE classes; labels нужны для оценки. Добавление detection loss — новый port с matched controls. Reference toolkit 2.1.2 не доказанная historical author environment. QDQ signedness/axes/fusion/rules/opset13 не LinQ arithmetic match. README 640 и script 672, mixed head precision ограничивают перенос AP/FPS. Найденный MMrazor RetinaNet config — PTQ.

**Physical pruning — F262–F271.** TP 1.6.1 + old Ultralytics 8.0.90, C2f_v2, patched trainer/save и full-object serialization. Не current U 8.4.184 или YOLO11. Conversion-only parity нужна отдельно от surgery; original YAML + plain state_dict не восстанавливают topology, clean process должен импортировать custom class. Toy coco128 override опасен custom ontology. Speed_up в script — MAC ratio. Demo break не откатывает последний rejected stage перед export. Smoke/reload/FP export/compiler acceptance новых dense shapes нужны до recovery. Меньший штатный student — comparator, LinQ speed неизвестна.

**Checkpoint — F272–F277/F193.** on_model_save после validation/write до strip позволяет immutable serialized EMA candidates и внешний constrained winner. on_train_epoch_end рано для текущей val; on_train_end поздно; on_fit_epoch_end имеет дополнительный final call. Pre-strip содержит EMA FP16 вместо online weights; scheduler/RNG/loader/gradients отсутствуют. Exact continuation не обеспечивается и до strip. Freeze разрешён при resume, LR/optimizer/epochs нет. Новая stage2 с новым recipe — resume=False, новые optimizer/EMA/warmup; supervised явно distill_model=None. Boolean resume stripped может стать warm start. Учитель/projectors нужны interrupted KD resume, а не final inference.

**Queue/fidelity — F278–F284.** Short epoch budget может менять auto optimizer, warmup, scheduler и close_mosaic; это другой recipe, не автоматически prefix. Hyperband/ASHA не гарантируют detector early ranking. Correctness smoke не позволяет kill по низкому early AP без представленного critical support. Admission зависит от полного critical path до useful artifact, annotation/review/SDK owners и D_useful; GPU utilization не цель.

## Публикационные числа: сохранять исходный вопрос сравнения

В F008/F009 TFA shot — instance/class, не frame или independent scene; sample-set variance не optimizer seed. F011 различает pretraining gain и convergence cost, сохраняя внутреннее 3.4/3.5 расхождение scratch. F033–F035 LVIS — mask AP и long-tail ablation, не PPE box/event forecast. F072–F079 SAHI — aerial AP50, с negative large-object effect, abstract/table deltas и current config differences. F102–F111 SoftTeacher/UTv1 — разные paper/README/teacher/student/threshold contracts; uniform/Gaussian jitter и LR 110k/120k не смешиваются.

F130–F140/F251 содержат полезные negative synthetic mixes, context/contour/mask/GT ограничения; robot cm не detection AP. F121–F126 FGD/LD дают detection-specific evidence при своих grids/GT/bins, не готовый loss любой YOLO. RAW_FACTS хранит все значимые численные строки и протоколы: основной текст может выбирать примеры, но не превращать headline gain в обещание target результата.

## Восемь сценариев и очередь

| Входы | Одно следующее различающее действие |
|---|---|
| Open data и weights | E001 zero-update, actual input, target diagnostic GT и ранний G4 |
| Немного полных target labels | E004 limited vs full; E048 заменяет эту пару только если initialization главный вопрос |
| Target video без labels | Один assistance-vs-manual cost/admission pilot E023/E024; затем corrected labels E025 либо manual |
| Разные камеры | E021 object против camera rules; при detector error E019 target-only vs один replay mix |
| Partial labels | E007 A/B/C metadata→assignment→loss gate до union training |
| Rare/new/tiny | E009/E003 причина; затем один input E016, balancing E010 или независимая annotation addition E043 |
| Working model misses/FP | E002 oracle objects/association; потом один targeted data/augmentation trial |
| Хорошая FP модель дорога или портится после conversion | E037 adjacent-stage parity либо native smaller detector comparator при proven compute bottleneck |

Полная таблица восьми сценариев с artifact/kill/promote/rollback и readiness дорогих routes сохранена в RAW_FACTS, блок W2-12. Сначала earliest failed/unknown gate. E001–E050 — reused gates и условные альтернативы под E051, не mandatory grid. Передавать текущий working bundle сразу с честным статусом; новая ветка допускается, если now + CP_remaining <= D_useful. При отсутствии target execution FP candidate имеет статус target-unverified. Previous accepted bundle не перезаписывается; rollback включает weights, preprocessing, class map, postprocessing и rules.

## Передача соседним topics и границы автора

model_stack нужны Q005/Q006/Q013/Q021–Q025: actual loaders, heads, masks/BN, branches, saver/extraction и hashes/locks. datasets нужны Q001–Q004/Q011/Q019: original coverage, lineage, groups, no-box complete review, unknown states, train-only assets и calibration roles. evaluation нужны Q004/Q010/Q011/Q026/Q031: constrained selection, support/exposure, grouped paired uncertainty, thresholds/rules отдельно weights, serialized candidate evaluator.

violation_methods получает Q001/Q017/Q029: visibility, relations и temporal context, oracle attribution до training. linq_platform/video_architecture получают Q007–Q009/Q031: фактический device/SDK/quant/operator/shape/sample/placement, canonical inputs, decoder/NMS и target timing. operator_product/hackathon_strategy получают Q010/Q012/Q027: измеренный human effort, useful deadline/owner, supported scope и target status. Соседние отчёты не предполагаются существующими; внешних сообщений не было.

K002/K004/K005/K006/K011/K012 закрыты в public/methodical scope; K001/K003/K007/K009/K010 уточнены; K008 author-artifact gap открыт. Следующий этап — большой самостоятельный русский черновик по ROLE_PROMPTS, затем редактор и machine compressor. Автор не получает новую сеть, не заполняет gaps из памяти и не превращает unknown в обещание. Дополнительный финальный аудитор запрещён.

