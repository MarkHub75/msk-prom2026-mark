# OPEN_QUESTIONS — training_strategy

Сборка: 2026-10-23T08:35:02+03:00, Europe/Moscow. Нового поиска после27 веток нет. Вопрос не означает отсутствия capability. Public contracts отделены от missing artifact, неизвестного target benefit и невыполненного SDK/experiment. Исходные154 локальные формулировки сведены в31 decision object с сохранением условий/истории. W2 уточняет ранние W1 вопросы; закрытый public trace не запрашивается повторно как общий обзор.

Короткая P0 группа: Q001 ontology; Q002 exposure permission; Q003 coverage; Q004 independent support; Q005/Q006 actual artifacts/environment; Q007–Q009 LinQ/quant/placement; Q010 acceptance. Перед unchecked labels нужны Q011/Q013; перед long training Q025. Actual LinQ execution — обязательный outcome, сейчас не выполнен. Q020 — локализованный public author-code gap; Q022–Q024 — условные artifact/implementation ветки, не третья волна.

<a id="q001"></a>

## Q001 — Ontology объектов, состояний и событий; visibility/unknown/ignore

- **Приоритет:** P0.
- **Mode to close:** Кейс/постановщик + annotation guideline.
- **Что известно:** Примеры СИЗ, зон и курения не задают полный mandatory vocabulary. Object/носит/отсутствует/не видно не одно понятие.
- **Где искали/что прочитали:** Входы; W1-01/03/05/06/11; W2-02/05/06; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-08](_WORK/W1/08_ACTIVE.md), [W1-09](_WORK/W1/09_PSEUDO.md), [W1-10](_WORK/W1/10_TEACHER.md), [W1-11](_WORK/W1/11_SYNTHETIC.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Согласовать definitions с positive/negative/ambiguous примерами до разметки.
- **Related IDs:** [F066](RAW_FACTS.md#f066), [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068), [F069](RAW_FACTS.md#f069), [F070](RAW_FACTS.md#f070), [F071](RAW_FACTS.md#f071), [E024](RAW_FACTS.md#e024), [E030](RAW_FACTS.md#e030); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q01** ([ветка](_WORK/W1/01_BASELINE.md)): Q001 | Точная ontology/events, обязательные metrics и разрешённый context; без них нельзя принять baseline | Полный кейс/ответ постановщика; приоритет высокий

- **W1-03-Q04** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q001 | Нужен новый semantic class или новый domain уже известного; base checkpoint и trainable tensors | model_stack/W1-02: выбрать full/head-only и считать retention

- **W1-05-Q01** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q001, P0, полный кейс / datasets / violation_methods:** object labels или person states/events? Видимый head без каски и невидимый head — разные состояния? Какие ignore/unknown/occlusion правила? Изменяет допуск F066, F067, F068, F069, F070, F071; получить ontology и примеры аннотатора до mixing/occlusion.

- **W1-08-Q02** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q001, P0 → violation_methods/datasets:** annotation unit — object box, PPE state, связь person–PPE или temporal event? Какие состояния unknown/occluded/ignore допустимы? Это меняет coverage, стоимость и смысл кадра.

- **W1-09-Q01** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q001 → datasets/evaluation (высокий):** какие классы действительно наблюдаемы и полностью размечены; что означает absence/no-helmet, где ignore/occlusion; разрешено ли использовать предоставленный unlabeled target stream для adaptation? Полный кейс и audit E024, не поиск универсального threshold.

- **W1-10-Q03** ([ветка](_WORK/W1/10_TEACHER.md)): Q001 | Полная ontology: object «каска», состояние ношения на человеке, event? Как сопоставлять phrases, class IDs, unknown и отсутствие наблюдения? | Полный кейс + annotation guideline; → datasets/violation_methods

- **W1-11-Q01** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q001, P0 → datasets / violation_methods:** labels — отдельные PPE objects, person states или events? Каковы правила unknown/occluded, visible/amodal box и связи wearer? Без ontology E030 не может разрешить генеративное редактирование; нужны guide и разобранные реальные примеры.

<a id="q002"></a>

## Q002 — Разрешённое unlabelled exposure и независимый test

- **Приоритет:** P0.
- **Mode to close:** Кейс/постановщик + manifests.
- **Что известно:** BN statistics, embeddings, backgrounds, pseudo mining и pretraining тоже exposure. Разрешение не получено.
- **Где искали/что прочитали:** W1-07-F10; W1-08-E01; W2-06/07/12; полный history/locators в [W1-07](_WORK/W1/07_DOMAIN.md), [W2-03](_WORK/W2/03_ONESTAGE_SSL.md), [W2-04](_WORK/W2/04_ACQUISITION_INTERFACE.md), [W2-06](_WORK/W2/06_DETECTION_PRETRAINING.md), [W2-07](_WORK/W2/07_SOURCEFREE_ROUTE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Получить правило кейса и роли каждого camera/time group; выбирает SSL/SFOD/pretraining и transfer claim.
- **Related IDs:** [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F206](RAW_FACTS.md#f206), [F207](RAW_FACTS.md#f207), [F220](RAW_FACTS.md#f220), [F221](RAW_FACTS.md#f221), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [F241](RAW_FACTS.md#f241), [F242](RAW_FACTS.md#f242), [E019](RAW_FACTS.md#e019), [E020](RAW_FACTS.md#e020), [E022](RAW_FACTS.md#e022), [E026](RAW_FACTS.md#e026), [E048](RAW_FACTS.md#e048); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-07-Q01** ([ветка](_WORK/W1/07_DOMAIN.md)): Q002 | Можно ли пользоваться unlabeled target/test video для adaptation? | S054 показывает, насколько это меняет смысл цифры. Получить прямое правило кейса; manifest должен различать exposed/unseen images. При запрете исключить любое test-image statistics/training

- **W2-03-Q03** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q002 case/data P0 | Ontology/adaptation permission/teacher critical coverage/independent groups неизвестны | Кейс + datasets audit/E024; разрешает online вообще

- **W2-04-Q02** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)): Q002 / case+data / P0 | Разрешённый acquisition pool, taxonomy, annotation unit/unknown, независимые groups и длительность event | Полный кейс и dataset manifest; определяет splits, completeness, temporal cap и permission adaptation

- **W2-06-Q04** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)): Q002 | **Case/data, высокий:** допустим ли in-domain unlabelled pretraining и какие camera/time groups образуют assessment? Есть ли source duplication? | Полный кейс + datasets provenance audit; влияет на claim/protocol и inclusion в очередь

- **W2-07-Q04** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q002 | Case/data: разрешение target exposure, taxonomy/visual signal, U/A/V/H/R | Полный кейс, inventory и audit; выбирает допустимость adaptation и силу выводов

<a id="q003"></a>

## Q003 — Source×class coverage, verified negatives, sparse instances и ROI

- **Приоритет:** P0.
- **Mode to close:** Original annotations + ручной audit.
- **Что известно:** TXT missing/empty дают zero rows; ordinary conversion теряет verified/crowd/coverage. Штатный U не partial-aware.
- **Где искали/что прочитали:** W1-03/04/12; W2-02; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W1-07](_WORK/W1/07_DOMAIN.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md), [W1-13](_WORK/W1/13_COMPRESSION.md), [W2-02](_WORK/W2/02_PARTIAL_ASSIGNMENT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Получить originals/coverage до union; различить hidden class B и hidden instance C.
- **Related IDs:** [F001](RAW_FACTS.md#f001), [F002](RAW_FACTS.md#f002), [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F033](RAW_FACTS.md#f033), [F034](RAW_FACTS.md#f034), [F042](RAW_FACTS.md#f042), [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F148](RAW_FACTS.md#f148), [F155](RAW_FACTS.md#f155), [F156](RAW_FACTS.md#f156), [F194](RAW_FACTS.md#f194), [F195](RAW_FACTS.md#f195), [E033](RAW_FACTS.md#e033); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q02** ([ветка](_WORK/W1/01_BASELINE.md)): Q003 | Есть ли target video, camera/session metadata, labels и annotation policy; разрешено ли adaptation на нём | Получить артефакты и проверить provenance вместе с datasets/evaluation; высокий

- **W1-03-Q01** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q003 | Действительная source×class coverage, hidden instances, ROI и ambiguous labels; annotation policy и ручной audit | datasets: решает, можно ли объединять источники

- **W1-04-Q03** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q003 | Annotation coverage смешанных источников и ignore semantics неизвестны | datasets + W1-03: audit coverage; model_stack: partial-label pathway | Допустимы ли hard negatives/oversampling вообще

- **W1-07-Q02** ([ветка](_WORK/W1/07_DOMAIN.md)): Q003 | Есть ли target labels, сколько независимых cameras/sessions и какие source images доступны? | Ничего из этого не установлено. Инвентаризация после выдачи кейса выбирает строку карты решений; не считать checkpoint доступом к source

- **W1-07-Q03** ([ветка](_WORK/W1/07_DOMAIN.md)): Q003 | Совпадают ли label semantics и exhaustive coverage? | До mixing сравнить guidelines и audit реальных кадров. datasets/model_stack должны подтвердить partial-label masking либо отказ от небезопасного merge

- **W1-12-Q02** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q003 → datasets | Exhaustive ли annotations? Правильно ли missing/empty трактуются как negatives? | Annotation coverage contract, camera/session IDs и E033. Успешный scan S026 недостаточен

- **W1-13-Q03** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q003 → datasets/evaluation:** какие камеры/сессии доступны для calibration, validation и независимой проверки, есть ли редкие состояния и мелкие объекты? Универсального числа calibration frames не назначаем. Labels для calibration inputs не обязательны по ORT API, но без labels нельзя измерить деградацию.

- **W2-02-Q01** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)): Q003 — case/artifact, P0 | Фактические source×class states, exhaustive/sparse instance coverage, ignore/ROI/visibility policy и original metadata. Уже известно, что обычный TXT не сохраняет их. datasets должен получить originals и ручной audit; определяет A/B/C и допустимость union.

<a id="q004"></a>

## Q004 — Независимые камеры/сессии/эпизоды и rare support

- **Приоритет:** P0.
- **Mode to close:** Данные + split/duplicate audit + полный GT.
- **Что известно:** Boxes/frames не independent groups. N/A не ноль; target inventory отсутствует.
- **Где искали/что прочитали:** W1-03/07/15; W2-05; полный history/locators в [W1-02](_WORK/W1/02_FINETUNING.md), [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W1-08](_WORK/W1/08_ACTIVE.md), [W1-11](_WORK/W1/11_SYNTHETIC.md), [W1-15](_WORK/W1/15_SELECTION.md), [W2-05](_WORK/W2/05_TEACHER_AUDIT.md), [W2-09](_WORK/W2/09_DETECTOR_QAT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Grouped splits/counts objects/events/camera-hours/blind GT; выбирает claim и необходимость доразметки.
- **Related IDs:** [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F033](RAW_FACTS.md#f033), [F034](RAW_FACTS.md#f034), [F055](RAW_FACTS.md#f055), [F093](RAW_FACTS.md#f093), [F094](RAW_FACTS.md#f094), [F130](RAW_FACTS.md#f130), [F177](RAW_FACTS.md#f177), [F227](RAW_FACTS.md#f227), [F228](RAW_FACTS.md#f228), [F255](RAW_FACTS.md#f255), [F256](RAW_FACTS.md#f256), [E024](RAW_FACTS.md#e024), [E031](RAW_FACTS.md#e031), [E045](RAW_FACTS.md#e045); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-02-Q02** ([ветка](_WORK/W1/02_FINETUNING.md)): Q004 | Сколько независимых целевых сцен и полных labels; какие старые классы обязательны? Без этого неизвестны риск overfit и нужный retention test | → datasets/evaluation/постановщик: ontology + manifests + coverage audit; высокий

- **W1-03-Q03** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q004 | Есть ли отдельные независимые episodes/cameras и полностью размеченный assessment; сколько independent positives | evaluation: K boxes недостаточно для claims о переносе

- **W1-04-Q04** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q004 | Нет camera/session/episode IDs и гарантии независимого split | datasets + evaluation: построить группы/проверить near duplicates | Не спутать повторы кадров с ростом данных и переобучение с переносом

- **W1-08-Q01** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q004, P0 → datasets/evaluation:** можно ли отделить целые независимые камеры/сессии и редкие события до отбора? Если есть только одно видео одной сцены, возможна лишь ограниченная проверка; получить данные/условия постановщика.

- **W1-11-Q03** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q004, P0 → evaluation / W1-15:** имеются ли независимые real cameras/sessions и достаточные critical-state positives/negatives? Нужен E031; без него нельзя заявить synthetic-to-real benefit. Сохранить статус target video, использованного для backgrounds или настройки generator.

- **W1-15-Q02** ([ветка](_WORK/W1/15_SELECTION.md)): Q004 → datasets | Достаточно ли независимых cameras/sessions/rare events, исчерпывающие ли labels, нет ли пересечений open/source/target | Inventory/annotation contract/duplicate audit; E045. Few-shot boxes не равны разнообразию сцен

- **W2-05-Q02** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)): Q004, P0, data/experiment | Сколько independent positive groups и какая population/camera support реально доступны для calibration/confirmation? До получения pool неизвестны sampling probabilities, precision uncertainty и возможность independent claim. Inventory + blind complete E024; при нехватке — review, не численная фикция

- **W2-09-Q03** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)): **Q004 — experiment, P1 → evaluation/datasets.** Есть ли независимые labels/сессии для измерения критичного recall после преобразования и отдельные development inputs для calibration/reconstruction? В W1 уже задан правильный split; неизвестна фактическая coverage. Без неё хорошее feature MSE не подтверждает пригодность детектора. Приоритет Q004 повышается только после FP export/PTQ diagnostics и SDK agreement.

<a id="q005"></a>

## Q005 — Фактические обучаемые checkpoints: provenance, classes, rights, unfused state

- **Приоритет:** P0.
- **Mode to close:** Artifact/manifest + loader smoke.
- **Что известно:** Публичные links/metadata и wheel есть; выбранных target weights нет. URL не вес и не разрешение использования.
- **Где искали/что прочитали:** W1-02/03/07/10; W2-01/06/07; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-02](_WORK/W1/02_FINETUNING.md), [W1-07](_WORK/W1/07_DOMAIN.md), [W2-01](_WORK/W2/01_NATIVE_KD_CONTRACT.md), [W2-06](_WORK/W2/06_DETECTION_PRETRAINING.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Получить bytes/hash/YAML/ancestry/class definitions/licence, transfer tensor inventory.
- **Related IDs:** [F001](RAW_FACTS.md#f001), [F002](RAW_FACTS.md#f002), [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [E027](RAW_FACTS.md#e027); K001.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q03** ([ветка](_WORK/W1/01_BASELINE.md)): Q005 | Исходный checkpoint, class coverage, package release, preprocess/output contracts | model_stack даёт hash/config и небольшой reference test; высокий

- **W1-02-Q01** ([ветка](_WORK/W1/02_FINETUNING.md)): Q005 | Какой checkpoint/YAML реально выбран и пригоден к обучению: source data/labels, normalization, unfused state, лицензия, class map, export constraints? Это определяет допустимые arms | → model_stack: получить конкретный hash/version и training load smoke test; высокий

- **W1-07-Q06** ([ветка](_WORK/W1/07_DOMAIN.md)): Q005 | Применима ли CC-BY-NC4.0 авторского AT к намеренному использованию? | S049 README. Решить для конкретного способа заимствования/поставки; исследование статьи и копирование кода имеют разные последствия

- **W2-01-Q01** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)): Q005 — artifact/experiment, P0 | Есть ли выбранные **реальные** student/teacher checkpoints стандартных YOLO11 с нужным task и разрешённым provenance? | model_stack фиксирует hashes/unfused artifacts/YAML; E027 проверяет old checkpoint compatibility. Public package route установлен, выбранных weights нет

- **W2-06-Q01** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)): Q005 | **Artifact/case, высокий:** какой пригодный source checkpoint с известной ancestry/classes и training loader реально дан команде? Это выбирает переносимые tensors | → model_stack/datasets: конкретные bytes/hash/config, source/teacher manifests, licence, class semantics, missing/unexpected inventory; S176/S179/S183 только публичные зацепки

<a id="q006"></a>

## Q006 — Выбранный package/dependency lock и trainer runtime

- **Приоритет:** P0.
- **Mode to close:** Artifact + inventory + bounded smoke.
- **Что известно:** U8.4.184 исследован, wheel10файлов сверены. Это не installation test. Docs PyTorch2.14 не версия команды.
- **Где искали/что прочитали:** W1-02/05/08/12/14; W2-01/04/11; полный history/locators в [W1-02](_WORK/W1/02_FINETUNING.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-08](_WORK/W1/08_ACTIVE.md), [W1-10](_WORK/W1/10_TEACHER.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md), [W2-01](_WORK/W2/01_NATIVE_KD_CONTRACT.md), [W2-04](_WORK/W2/04_ACQUISITION_INTERFACE.md), [W2-12](_WORK/W2/12_TRIAL_QUEUE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Pin OS/Python/torch/CUDA/driver/GPU/VRAM/dependencies, actual criterion/head и finite update/reload.
- **Related IDs:** [F050](RAW_FACTS.md#f050), [F051](RAW_FACTS.md#f051), [F052](RAW_FACTS.md#f052), [F053](RAW_FACTS.md#f053), [F054](RAW_FACTS.md#f054), [F055](RAW_FACTS.md#f055), [F056](RAW_FACTS.md#f056), [F057](RAW_FACTS.md#f057), [F148](RAW_FACTS.md#f148), [F149](RAW_FACTS.md#f149), [F150](RAW_FACTS.md#f150), [E004](RAW_FACTS.md#e004), [E012](RAW_FACTS.md#e012), [E022](RAW_FACTS.md#e022), [E027](RAW_FACTS.md#e027); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-02-Q03** ([ветка](_WORK/W1/02_FINETUNING.md)): Q006 | Поддерживает ли фактический trainer наш selector, row remap и нужную BN политику? Найдено для 8.4.184, не произвольной установленной версии | → model_stack: pin package/commit и E004 setup/update audit; высокий

- **W1-04-Q02** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q006 | Локальная модель/версия trainer неизвестны; class weighting подтверждён только pinned Ultralytics8.4.184, RFS — Detectron2 commit выше | model_stack: показать package/commit, criterion и loader output | Готовый параметр против изменения кода; не переносить новые flags в старое окружение

- **W1-05-Q02** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q006, P0, artifact/runtime:** какой фактический checkpoint, trainer и package lock? Поддерживает ли будущая среда custom list без тихого skip? Известны source signatures; нужен E012, не ещё одно предположение по live docs. → model_stack/W1-12: F050, F051, F052, F053, F054, F055, F056, F057, особенно bbox-only copy-paste, classification erasing и фактический смысл close_mosaic.

- **W1-08-Q06** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q006, P1 → tooling:** какая редакция и версия CVAT реально доступны, совместимы ли SDK/server и платные QA/Analytics? На сайте v2.80.0 существует tag `bb0a873fe071e70d71458cd82127052025e05807` (commit date2026-10-21), но versioned docs tool не открыл; прочитанный develop не выдаётся за установку команды.

- **W1-10-Q01** ([ветка](_WORK/W1/10_TEACHER.md)): Q006 | Какая **фактически установленная** Ultralytics версия и выбранная family? Наличие KD в U не подтверждает старую среду команды | Version/commit + capability smoke test; → model_stack

- **W1-12-Q01** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q006 → model_stack | Какой checkpoint/task/version реально выбраны? Где фактические model overrides и loss? | Получить immutable model/config/weight hashes; сравнить actual args и optimizer groups с F148, F149, F150. Если другой стек/commit — не переносить defaults

- **W2-01-Q04** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)): Q006 — environment/runtime, P0 | Работают ли installed dependency set, wrapper setup, gradient path и serialization? | E027 на фактической машине с inventory; package bytes inspection не installation test

- **W2-04-Q01** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)): Q006 / artifact / P0 | Actual family/checkpoint/backend/pin; доступен ли нужный режим и совпадает ли returned contract с U? Это разрешает public-only route | model_stack передаёт artifact/hash/version/args; E022 smoke/reload/overlay. Public поиск не выбирает веса команды

- **W2-12-Q02** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q006 | Artifact/experiment: actual runnable model/pin, save/extract/BN/resume behavior, source/class coverage | model_stack/datasets получает W2 contract и выполняет affected G1/G2; public wheel/код не local runtime evidence.

<a id="q007"></a>

## Q007 — LinQ device/SDK build и accepted graph/input/export

- **Приоритет:** P0.
- **Mode to close:** SDK/доступ + compile/run.
- **Что известно:** Vendor называет yolo5s/yolo8/yolo11,int8,Compiler/DNN Quant. Exact устройство/SDK/opset/shapes/postprocess не получены.
- **Где искали/что прочитали:** W1-13-S11/S12; W2-01/03/09/10; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-02](_WORK/W1/02_FINETUNING.md), [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W1-06](_WORK/W1/06_SCALE.md), [W1-07](_WORK/W1/07_DOMAIN.md), [W1-09](_WORK/W1/09_PSEUDO.md), [W1-10](_WORK/W1/10_TEACHER.md), [W1-11](_WORK/W1/11_SYNTHETIC.md), [W1-13](_WORK/W1/13_COMPRESSION.md), [W2-01](_WORK/W2/01_NATIVE_KD_CONTRACT.md), [W2-03](_WORK/W2/03_ONESTAGE_SSL.md), [W2-04](_WORK/W2/04_ACQUISITION_INTERFACE.md), [W2-06](_WORK/W2/06_DETECTION_PRETRAINING.md), [W2-07](_WORK/W2/07_SOURCEFREE_ROUTE.md), [W2-08](_WORK/W2/08_SYNTHETIC_SUPERVISION.md), [W2-10](_WORK/W2/10_PHYSICAL_PRUNING.md), [W2-11](_WORK/W2/11_CHECKPOINT_CONTROL.md), [W2-12](_WORK/W2/12_TRIAL_QUEUE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Получить versioned guide/sample/operator-shape matrix; выполнить selected artifact на LinQ.
- **Related IDs:** [F001](RAW_FACTS.md#f001), [F002](RAW_FACTS.md#f002), [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F033](RAW_FACTS.md#f033), [F034](RAW_FACTS.md#f034), [F055](RAW_FACTS.md#f055), [F072](RAW_FACTS.md#f072), [F073](RAW_FACTS.md#f073), [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F115](RAW_FACTS.md#f115), [F116](RAW_FACTS.md#f116), [F130](RAW_FACTS.md#f130), [F155](RAW_FACTS.md#f155), [F156](RAW_FACTS.md#f156), [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [F193](RAW_FACTS.md#f193), [F206](RAW_FACTS.md#f206), [F207](RAW_FACTS.md#f207), [F220](RAW_FACTS.md#f220), [F221](RAW_FACTS.md#f221), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [F241](RAW_FACTS.md#f241), [F242](RAW_FACTS.md#f242), [F247](RAW_FACTS.md#f247), [F248](RAW_FACTS.md#f248), [F262](RAW_FACTS.md#f262), [F263](RAW_FACTS.md#f263), [F272](RAW_FACTS.md#f272), [F278](RAW_FACTS.md#f278), [F279](RAW_FACTS.md#f279), [E028](RAW_FACTS.md#e028), [E030](RAW_FACTS.md#e030), [E031](RAW_FACTS.md#e031); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q04** ([ветка](_WORK/W1/01_BASELINE.md)): Q007 | Реальное LinQ input shape, preprocessing, export/runtime и evidence выполнения | linq_platform; версия SDK и actual artifact, высокий

- **W1-02-Q05** ([ветка](_WORK/W1/02_FINETUNING.md)): Q007 | Изменение nc/head совместимо с целевым LinQ compiler/runtime и postprocessing? | → linq_platform/model_stack: actual graph/input/output compile + execution; высокий

- **W1-03-Q06** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q007 | Исполним ли итоговый graph/cosine head/C-RPN, actual shapes/output/postprocess на LinQ | linq_platform/model_stack: training method не устанавливает target execution

- **W1-04-Q07** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q007 | Экспорт выбранного обученного checkpoint и LinQ не проверены | model_stack + linq_platform; реальные export/compile/run artifacts | Готовность результата к обязательной платформе

- **W1-06-Q02** ([ветка](_WORK/W1/06_SCALE.md)): Q007 → linq_platform | Какие статические/dynamic NCHW shapes, batch sizes, число одновременно resident models/engines; размещение resize/crop/NMS; fixed-shape padding, remote request overhead, допустимость host stages? | SDK/version+device access, небольшой compile/run позже; P0. Ни одна из этих возможностей в исследовании не установлена.

- **W1-07-Q07** ([ветка](_WORK/W1/07_DOMAIN.md)): Q007 | Допускает ли LinQ граф выбранного detector и teacher extraction/export? | Здесь не установлено. linq_platform/model_stack: реальный compile+inference check, parity и timing после заморозки weights/preprocessing

- **W1-09-Q05** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q007 → linq_platform/video_architecture:** извлечённый student checkpoint, preprocessing, shape/class map, postprocessing и output contract должны пройти реальный export/runtime путь. Teacher работает offline/при обучении и не обязан исполняться на LinQ; это не снимает требований к student. Доступа/измерений LinQ у этой ветки нет.

- **W1-10-Q04** ([ветка](_WORK/W1/10_TEACHER.md)): Q007 | Какой student graph и export ops разрешены фактическим LinQ SDK? YOLO26 end2end и LD head нельзя считать поддержанными | Получить SDK/compiler target specification и исполнить E028; → linq_platform/model_stack

- **W1-11-Q07** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q007, P1 → linq_platform / model_stack:** data-only augmentation может сохранить detector inference architecture, но E031 candidate нужно реально экспортировать и проверить на LinQ. Ни trainer из papers, ни masks для подготовки не устанавливают поддержанный runtime. Новые input size/cascade или architecture требуют нового целевого пути.

Закрыто на уровне research: первичные доказательства полезности и вреда найдены; задачи и ограничения отделены; доступны versioned author artifacts; для принятия решения нужны target ontology, assets и controlled real E030/E031. Публикационное отсутствие PPE-протокола не является доказательством невозможности синтетики для PPE.

- **W1-13-Q01** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q007, приоритет критический → linq_platform:** какая реально выдаваемая модель устройства, SDK/compiler/runtime build, operator/opset matrix и пример входного артефакта? Меняет весь export/quant route. Закрытие: файлы SDK и успешная компиляция минимального фактического детектора, не пресс-релиз.

- **W2-01-Q03** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)): Q007 — SDK/target, P0 | Примет ли реальный LinQ exact final YOLO11n graph/input/postprocessing/quant representation? | linq_platform/model_stack получают build/op matrix/sample и выполняют compile/run. Vendor `yolo11` lead не закрывает

- **W2-03-Q05** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q007 SDK P0 | FCOS/ET exported graph, Integral/GN/shape/raw postprocess совместимость LinQ неизвестны | Versioned SDK и actual compile/run; может исключить route до training

- **W2-04-Q05** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)): Q007 / SDK / P1 | Target graph LinQ и его outputs могут отличаться от offline PT. Допустим ли offline acquisition? | Условия кейса/SDK; исполнение финального student остаётся отдельным platform gate, успех selector ничего о нём не доказывает

- **W2-06-Q05** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)): Q007 | **SDK, высокий:** проходит ли выбранная architecture/изменённая head через actual LinQ compiler/runtime? | → linq_platform/model_stack: выданный SDK/version и реальный compile/run, не framework paper

- **W2-07-Q06** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q007 | SDK: исполнение VGG/Faster R-CNN graph | linq_platform/model_stack actual export/compile/run; backend paper не доказательство LinQ

- **W2-08-Q04** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)): Q007 — artifact/SDK, P1 | Какой именно final detector graph и export реально принимает выданный LinQ? Нужны выбранный checkpoint/config и actual target toolchain; для special-loss author route сначала Q020 | → linq_platform/model_stack; data-only design сохраняет архитектуру, но не гарантирует исполнение

- **W2-10-Q03** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)): Q007 / SDK-device / platform-critical для promotion | Компилирует ли actual LinQ stack новые dense widths/C2f-derived ONNX; какие opset/alignment/fusion/fallback/quant условия? Public YOLO-family support F166/F14 не устанавливает поддержку этого изменённого graph. | Versioned SDK sample/operator-shape matrix и реальный compiler/run/placement report. Это не вопрос sparse kernels: route меняет плотные shapes.

- **W2-11-Q04** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)): Q007 / SDK, P0 | Пригоден ли final selected student artifact/graph для actual LinQ path? | Reuse E037/E027, доступ SDK и реальный compile/run

- **W2-12-Q03** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q007 | SDK/experiment: actual compile/import/quant/shape/placement и end-to-end cost | linq_platform/video_architecture: полученный SDK+реальный baseline/финальный G4, timestamps. Это может поменять ранний выбор архитектуры и CP, но не блокирует независимый data audit.

<a id="q008"></a>

## Q008 — Quant import/arithmetic: DNN Quant, QDQ/QOperator, ranges/axes/fusion

- **Приоритет:** P0.
- **Mode to close:** SDK/sample + numerical boundary tests.
- **Что известно:** ORT/NVIDIA reference установлены; arithmetic match LinQ неизвестен. QAT graph может быть отвергнут/перекалиброван.
- **Где искали/что прочитали:** W1-13; W2-09-Q02; полный history/locators в [W1-13](_WORK/W1/13_COMPRESSION.md), [W2-09](_WORK/W2/09_DETECTOR_QAT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Signedness/range/rounding/zp/axes/accumulator/bias/requant, scale-sharing/fusion/exclusions и accepted sample.
- **Related IDs:** [F155](RAW_FACTS.md#f155), [F156](RAW_FACTS.md#f156), [F255](RAW_FACTS.md#f255), [F256](RAW_FACTS.md#f256), [E037](RAW_FACTS.md#e037), [E049](RAW_FACTS.md#e049); K009.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-13-Q02** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q008, критический → linq_platform/model_stack:** кто делает quantization — DNN Quant или внешнее средство; принимаются FP ONNX, QDQ, QOperator, QAT graphs? Каковы signedness, scales/axes, zero point, accumulation, rounding, fusion, exclusions? Нужны versioned guide, sample, compiler diagnostics. Публичный поиск этого контракта не установил; отсутствие результата не доказывает отсутствия поддержки.

- **W2-09-Q02** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)): **Q008 — SDK contract, критический → linq_platform.** Запрашивать не абстрактное «есть ли int8», а следующие ответы **для фактически выданного SDK/compiler/runtime build и устройства**:

1. Кто задаёт ranges/quantization: DNN Quant из FP ONNX или внешний QAT? Принимаются ли ONNX QDQ opset13, сохранённые training scales/zero points; сохраняются они или перекалибруются? Нужен рабочий SDK sample с graph и expected outputs.
2. S8 activations+weights? Per-tensor activations, per-output-channel Conv weights axis=0 в KCRS? Как трактуются layout changes, depthwise/group Conv и detection head axes? Range `[-128,127]` или `[-127,127]`; zero-point обязательно 0? Каковы rounding tie rule, clipping, bias/accumulator/requant precision?
3. Fusion до/после QDQ: Conv+BN/RepConv/implicit head допустимы? Scale sharing Concat/MaxPool, Add, Resize/Upsample, sigmoid/decode поддерживаются? Можно ли исключать head/sensitive nodes или оставлять FP16/FP32; как это отражается в log и выполнении?
4. Допустим ли данный decoded head без NMS, input layout/normalization/static H/W/dynamic batch? Где выполняются NMS и обратное преобразование координат? Какие ops fallback на host, какой final binary format и reproducible compiler command?

Изменяемое решение: при FP-only import с собственным quantizer внешний QDQ route может не иметь смысла; при совпадении QAT import contract появляется основание маленького trial. Ответ «ONNX поддерживается» не закрывает Q008. Общий LinQ public search не повторялся.

<a id="q009"></a>

## Q009 — Placement/fallback и model/end-to-end latency/memory

- **Приоритет:** P0.
- **Mode to close:** SDK profiler + target measurement.
- **Что известно:** FLOPs/MACs/INT8/compiled file не execution или acceleration. Network/decode/queue/crops могут доминировать.
- **Где искали/что прочитали:** W1-06/13/14; W2-09/10/12; полный history/locators в [W1-06](_WORK/W1/06_SCALE.md), [W1-13](_WORK/W1/13_COMPRESSION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Placement/precision/fallback logs, fixed timing boundary, p50/p95/throughput/calls/exposure.
- **Related IDs:** [F072](RAW_FACTS.md#f072), [F073](RAW_FACTS.md#f073), [F155](RAW_FACTS.md#f155), [F156](RAW_FACTS.md#f156), [E016](RAW_FACTS.md#e016), [E017](RAW_FACTS.md#e017); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-06-Q05** ([ветка](_WORK/W1/06_SCALE.md)): Q009 → video_architecture | Реальный frame rate/число потоков/person count distribution и стоимость network/queue/crops/model swaps; поддерживаются ли timestamps каждого stage? | E016/E017 на целевой конфигурации; P0. Нельзя объявлять tile FPS model-only скоростью сервиса.

- **W1-13-Q04** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q009 → linq_platform/video_architecture:** какие операции реально идут на ускорителе, что остаётся на host, как получить graph placement/precision/fallback log и синхронизированное время? Скомпилированный файл и название int8 не отвечают.

- **W1-13-Q06** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q009 → linq_platform:** есть ли sparse kernels, supported pattern/layout и ограничения shapes? До подтверждения unstructured pruning оставлен исследовательским вариантом без обещания latency.

<a id="q010"></a>

## Q010 — Constrained objective: critical recall/FP/margins/selection/tie/stop

- **Приоритет:** P0.
- **Mode to close:** Кейс + evaluation + baseline.
- **Что известно:** AP-best=EMA AP50:95, не event/rare objective. Numerical margins/sample floors не установлены.
- **Где искали/что прочитали:** W1-04/15; W2-05/11/12; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-06](_WORK/W1/06_SCALE.md), [W1-07](_WORK/W1/07_DOMAIN.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md), [W1-15](_WORK/W1/15_SELECTION.md), [W2-05](_WORK/W2/05_TEACHER_AUDIT.md), [W2-11](_WORK/W2/11_CHECKPOINT_CONTROL.md), [W2-12](_WORK/W2/12_TRIAL_QUEUE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Primary/delta_min/epsilon/R_min/FP exposure/tie/candidate budget до tuning; решает promote/rollback.
- **Related IDs:** [F064](RAW_FACTS.md#f064), [F065](RAW_FACTS.md#f065), [F227](RAW_FACTS.md#f227), [F230](RAW_FACTS.md#f230), [E009](RAW_FACTS.md#e009), [E013](RAW_FACTS.md#e013), [E015](RAW_FACTS.md#e015), [E016](RAW_FACTS.md#e016), [E024](RAW_FACTS.md#e024), [E045](RAW_FACTS.md#e045); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q06** ([ветка](_WORK/W1/01_BASELINE.md)): Q010 | Какие требования достаточности и допустимые пропуски/тревоги установлены для редких событий | Кейсовые критерии и evaluation; без них нет честного stop/acceptance threshold

- **W1-04-Q01** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q010 | Фактические классы, critical error costs, нормальный поток и положительные независимые события отсутствуют; пороги редкости нельзя назначить | datasets / постановщик; inventory E009 | Нужен ли balancing, что считать negative, какой допустим FP/hour

- **W1-04-Q05** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q010 | Приемлемый rare-recall/FP trade-off и event grouping не заданы | evaluation + violation_methods: fixed event protocol и denominator | Acceptance balancing/mining; AP не заменяет эксплуатационный критерий

- **W1-05-Q04** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q010, P1, evaluation:** какие critical-class gates и допустимый clean/robustness trade-off? → evaluation/W1-15: E013/E015, F064/F065; synthetic severities и соседние frames не независимый test.

- **W1-06-Q04** ([ветка](_WORK/W1/06_SCALE.md)): Q010 → evaluation | Зафиксировать full-frame/event GT, operating-point policy, matching/maxDets/ignore; original-size bins, группировка session/camera. Каков допустимый FP/hour и recall/latency budget? | Кейс+контракт оценки до E016; P0.

- **W1-07-Q05** ([ветка](_WORK/W1/07_DOMAIN.md)): Q010 | Какой old-domain retention обязателен и есть ли независимые данные? | Без old-domain holdout forgetting не измеряется; source-free не решает это автоматически. evaluation/постановщик: согласовать gate по критичным классам/камерам

- **W1-12-Q03** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q010 → evaluation, W1-15 | Какую цель оптимизирует checkpoint selection: detector AP или event metric/critical recall/FP? | Формально задать val protocol, constraints и stop/accept thresholds. Встроенный fitness S103 не даёт эту цель автоматически

- **W1-15-Q01** ([ветка](_WORK/W1/15_SELECTION.md)): Q010 → evaluation / постановщик | Реальная primary metric, event matching, critical recall/FP budget, practical delta и non-inferiority margins. Без них нельзя честно задать numerical acceptance | Полный кейс, GT/exposure/support baseline; согласовать E045 contract до tuning

- **W2-05-Q01** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)): Q010, P0, case/data | Какие mandatory classes/visibility/ignore, critical conditions и допустимые precision/coverage/localization losses? Публичные papers не задают safety acceptance; полный кейс + annotation guideline + baseline устанавливают gate до cutoff tuning. Связь K005/F227/F230/E024

- **W2-11-Q01** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)): Q010 / case+evaluation, P0 | Какая constrained objective, support/FP exposure, tie/stop policy и стоимость event evaluator? | Полный кейс + evaluation; утвердить contract до selection. AP-best не достаточен

- **W2-12-Q01** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q010 | Case/evaluation: primary/constraints/margins, allowable target-stream exposure, независимый population claim | Кейс + evaluation/datasets contract до подтверждающих trials. Без rare support N/A/предварительный результат, не ungrounded acceptance.

<a id="q011"></a>

## Q011 — Качество teacher и допуск pseudo labels по class×size×camera

- **Приоритет:** P0 перед unchecked/KD.
- **Mode to close:** Blind complete audit + independent confirmation.
- **Что известно:** Calibration не восстанавливает no-detection misses; precision без retained recall/localization/support недостаточна.
- **Где искали/что прочитали:** W1-09/10; W2-01/03/05; полный history/locators в [W1-09](_WORK/W1/09_PSEUDO.md), [W1-10](_WORK/W1/10_TEACHER.md), [W2-01](_WORK/W2/01_NATIVE_KD_CONTRACT.md), [W2-03](_WORK/W2/03_ONESTAGE_SSL.md), [W2-05](_WORK/W2/05_TEACHER_AUDIT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Frozen score/IoU/matching/cutoff, P probability+D diagnostics отдельно, confirmation; выбирает assistance/review/unchecked/KD.
- **Related IDs:** [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F115](RAW_FACTS.md#f115), [F116](RAW_FACTS.md#f116), [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [F206](RAW_FACTS.md#f206), [F207](RAW_FACTS.md#f207), [F227](RAW_FACTS.md#f227), [F228](RAW_FACTS.md#f228), [E024](RAW_FACTS.md#e024); K005.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-09-Q03** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q011 → evaluation (высокий):** независимые camera/session группы для audit/calibration/V/H и минимально полезное изменение/критичная регрессия; сколько фактических positive для каждой редкой страты? Увеличение коррелированных кадров не закрывает нехватку независимых событий.

- **W1-10-Q02** ([ветка](_WORK/W1/10_TEACHER.md)): Q011 | Есть ли target teacher, превосходящий student по нужным class/scale/occlusion errors? Без этого KD может копировать bias | Независимый development audit; → datasets/evaluation/W1-09

- **W2-01-Q02** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)): Q011 — case/data/experiment, P0 | Достаточно ли teacher лучше student именно на нужных class/size/camera errors? | teacher audit + E027. Ни большее число parameters, ни target ontology equality сами по себе не ответ

- **W2-03-Q04** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q011 experiment/selection P1 | Полезность raw/teacher/EMA на target неизвестна | Раздельные V metrics/branch manifest, controlled E03/H protocol; не переносить teacher AP на student

- **W2-05-Q03** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)): Q011, P1, artifact/experiment | Конкретный teacher/checkpoint, его floor/caps/NMS/score semantics и cost полного исправления? Проверить outputs/overlays и randomized cost pilot E024; устанавливает, полезнее assistance, manual либо отдельный unchecked trial. Published calibration recipe не выбирает teacher

<a id="q012"></a>

## Q012 — Полная human cost manual/preannotation/selection/QA

- **Приоритет:** P1.
- **Mode to close:** Randomized matched cost pilot.
- **Что известно:** Images/objects/clicks не person-minutes. CVAT imported/interpolated/net counters не минуты/сцены.
- **Где искали/что прочитали:** W1-08/10/14; W2-04/05; полный history/locators в [W1-08](_WORK/W1/08_ACTIVE.md), [W1-14](_WORK/W1/14_COMPUTE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Selection+draw/correct+miss search+review/adjudicate+export QA, annotator/order; выбирает teacher/AL/manual.
- **Related IDs:** [F093](RAW_FACTS.md#f093), [F094](RAW_FACTS.md#f094), [F168](RAW_FACTS.md#f168), [F169](RAW_FACTS.md#f169), [E022](RAW_FACTS.md#e022), [E023](RAW_FACTS.md#e023), [E043](RAW_FACTS.md#e043); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-08-Q04** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q012, P1:** сколько стоит полный цикл в наших руках? Источники не дают нашего распределения minutes/actions; закрывается E022 pilot/E023.

- **W1-14-Q03** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q012 → datasets/W1-08:** сколько независимых сцен нужно для полезной добавки labels, каков реальный QA throughput и покрытие ошибок? Закрывается E043, не количеством соседних кадров.

<a id="q013"></a>

## Q013 — Coverage/ignore mechanism выбранного assignment/loss

- **Приоритет:** P0 для partial.
- **Mode to close:** Implementation artifact + A/B/C gradient gate.
- **Что известно:** B U-objectness-free допускает custom class validity; C spatial policy, legacy objectness и обеE2E branches отдельно. MMDet defaults off/zero-GT limit.
- **Где искали/что прочитали:** W1-03-E02; W2-02; полный history/locators в [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-04](_WORK/W1/04_IMBALANCE.md), [W2-02](_WORK/W2/02_PARTIAL_ASSIGNMENT.md), [W2-05](_WORK/W2/05_TEACHER_AUDIT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Metadata/transforms/assignment/unreduced losses/gradients, positive precedence и denominator; сравнить доразметку.
- **Related IDs:** [F194](RAW_FACTS.md#f194), [F195](RAW_FACTS.md#f195), [F196](RAW_FACTS.md#f196), [F197](RAW_FACTS.md#f197), [F198](RAW_FACTS.md#f198), [F199](RAW_FACTS.md#f199), [F200](RAW_FACTS.md#f200), [F201](RAW_FACTS.md#f201), [F202](RAW_FACTS.md#f202), [F203](RAW_FACTS.md#f203), [E007](RAW_FACTS.md#e007), [E009](RAW_FACTS.md#e009), [E010](RAW_FACTS.md#e010); K002.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-03-Q02** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q013 | Поддерживает ли выбранный trainer per-class/per-region ignore во всех affected losses и assignment; точный commit/API | model_stack: E007 до обучения; обычный bbox loader не считать partial-aware

- **W1-04-Q06** ([ветка](_WORK/W1/04_IMBALANCE.md)): Q013 | EQLv2 не проверен на нашем head/soft targets, код не закреплён и не запущен; полного преимущества над простым sampling для нас нет | model_stack, только если E009/E010 подтверждают gradient problem; отдельная будущая интеграция | Стоит ли сложный loss своей цены; сейчас не приоритет по умолчанию

- **W2-02-Q02** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)): Q013 — engineering/experiment, P0 | Выбранный trainer/checkpoint и actual criterion/head branches; custom validity mechanism не создан. model_stack получает F194, F195, F196, F197, F198, F199, F200, F201, F202/F203 и E007; закрытие — code/API и execution diagnostics E007. Публичный static trace на U не подтверждает локально установленную версию.

- **W2-02-Q03** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)): Q013 — experiment, conditional | Полезен ли conservative negative suppression против полной доразметки при одинаковом holdout и измеренном annotation/engineering budget. Public source не устанавливает target gain; только после correctness gate, без обязательного grid.

- **W2-02-Q04** ([ветка](_WORK/W2/02_PARTIAL_ASSIGNMENT.md)): Q013 — artifact/experiment, conditional | Если выбран MMDet known-ignore route: реально ли target images имеют regular positives, нужную geometry и согласованные transforms; как поступать с zero regular GT. Проверить pinned configs и E007, затем отдельно export/SDK. Не переносить найденное на все MMDetection assigners.

- **W2-05-Q04** ([ветка](_WORK/W2/05_TEACHER_AUDIT.md)): Q013, P0 до unchecked trial, implementation | Как chosen student criterion обрабатывает omitted positives/unknown classes/empty outputs? Нужен actual loader/assigner/loss trace из model_stack/W2-02, либо full corrected labels. Хорошая precision accepted boxes не закрывает negative supervision

<a id="q014"></a>

## Q014 — Target trainable mask, BN/freeze/full/staged optimum

- **Приоритет:** P1.
- **Mode to close:** Controlled comparison + buffer/update audit.
- **Что известно:** TFA predictor-only не YOLO freeze. U freeze BN eval, manual mask может быть отменена; freeze разрешён resume, новый LR нет.
- **Где искали/что прочитали:** W1-02/12; W2-11; полный history/locators в [W1-02](_WORK/W1/02_FINETUNING.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Один target init, actual masks/groups/stats; limited vs full, BN/staged только при причине.
- **Related IDs:** [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F042](RAW_FACTS.md#f042), [F148](RAW_FACTS.md#f148), [E004](RAW_FACTS.md#e004), [E005](RAW_FACTS.md#e005); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-02-Q04** ([ветка](_WORK/W1/02_FINETUNING.md)): Q014 | Какая точная mask оптимальна и нужен ли freeze→unfreeze? Papers не отвечают за target CCTV | E004; staged arm только после рабочей пары B/C, с суммарным update/time budget; средний

- **W1-02-Q06** ([ветка](_WORK/W1/02_FINETUNING.md)): Q014 | Нужна ли адаптация BN и достаточно ли batch diversity для устойчивых target statistics? | E005, только если диагностическая причина остаётся после E004; средний

- **W1-12-Q07** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q014 → W1-02 | Как сделать freeze→unfreeze без игнорируемых resume overrides и с известным BN? | Новый режим с проверкой trainable mask/BN stats и state manifest; S011.check_resume; не считать смену freeze автоматически чистым сравнением

<a id="q015"></a>

## Q015 — Detector-specific tensors сверх одинакового backbone

- **Приоритет:** P1.
- **Mode to close:** Artifact + matched initialization trial.
- **Что известно:** DetCo/DETReg transfer components различны; base stage/schedule/exposure confounds. Artifact не pretraining с нуля.
- **Где искали/что прочитали:** W2-06; полный history/locators в [W2-06](_WORK/W2/06_DETECTION_PRETRAINING.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Identical backbone/head state, только detector tensors отличаются, target/retention/compute.
- **Related IDs:** [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [E048](RAW_FACTS.md#e048); K006.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W2-06-Q02** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)): Q015 | **Experiment, средний:** дают ли detector components пользу сверх того же backbone на независимых target groups? | E048 после correctness/target gates; public Tables не закрывают этот вопрос

<a id="q016"></a>

## Q016 — Minimal acquisition usefulness и raw/vector interfaces

- **Приоритет:** P1; raw P2.
- **Mode to close:** Output smoke + equal-human-minutes trial.
- **Что известно:** Results xyxy/conf/cls,probs=None. Low-confidence не entropy. No-box exploration входит proposed policy.
- **Где искали/что прочитали:** W1-08; W2-04; полный history/locators в [W1-08](_WORK/W1/08_ACTIVE.md), [W2-04](_WORK/W2/04_ACQUISITION_INTERFACE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Records/caps/time/rank; одна arm vs stratified random. Raw/hooks/embeddings только по отдельной нужде.
- **Related IDs:** [F093](RAW_FACTS.md#f093), [F094](RAW_FACTS.md#f094), [F220](RAW_FACTS.md#f220), [F221](RAW_FACTS.md#f221), [E022](RAW_FACTS.md#e022); K004.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-08-Q03** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q016, P0 → model_stack:** доступны ли полные class scores и proposals, поддержка partial labels, стабильный matching, export of predictions? Для post-NMS top confidence output не обещать восстановление paper entropy.

- **W1-08-Q05** ([ветка](_WORK/W1/08_ACTIVE.md)): - **Q016, P1:** какой budget fraction exploration и temporal exclusion соответствуют длительности PPE/event состояний? Устанавливать по train видео и cost/coverage, не копировать ±15 frames чужого датасета.

- **W2-04-Q03** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)): Q016 / experiment / P1 | `c_pool`, caps, exploration fraction и low-confidence ranking действительно полезнее random за полные минуты? | E022 interface pilot + существующий E022; quality labels и полная стоимость, без универсальных thresholds

- **W2-04-Q04** ([ветка](_WORK/W2/04_ACQUISITION_INTERFACE.md)): Q016 / implementation / P2 | Если later нужен vector/feature score: кто отдаёт logits/probabilities, branch identity, indices и decoder до filtering? | model_stack реализует/проверяет custom predictor или raw-head capture отдельно. Требовать shape/dtype, class order, coordinate frame, sigmoid/logit flag, head/top-k/NMS stage, original location IDs и memory/cost; не восстанавливать их из Results

<a id="q017"></a>

## Q017 — Визуальный сигнал/scale/crop/cascade и системная цена

- **Приоритет:** P0 при tiny failure.
- **Mode to close:** Native→actual input audit + inference comparison.
- **Что известно:** Resize не создаёт информацию; cascade recall≤usable-crop coverage. SAHI AP50 не AP50:95, recipe revisions различны.
- **Где искали/что прочитали:** W1-01/06; W2-12; полный history/locators в [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-06](_WORK/W1/06_SCALE.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Pixel/visibility audit, один большийinput либо predicted cascade с upstream misses; target shapes/calls/latency.
- **Related IDs:** [F074](RAW_FACTS.md#f074), [F075](RAW_FACTS.md#f075), [F076](RAW_FACTS.md#f076), [F077](RAW_FACTS.md#f077), [F080](RAW_FACTS.md#f080), [F082](RAW_FACTS.md#f082), [E003](RAW_FACTS.md#e003), [E014](RAW_FACTS.md#e014), [E016](RAW_FACTS.md#e016), [E017](RAW_FACTS.md#e017), [E018](RAW_FACTS.md#e018); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-05-Q03** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q017, P0, target data:** реальный размер evidence в пикселях, blur/lighting/codec и independent cameras? Без samples нельзя назначить compression quality, kernel size и силу scale. → datasets/W1-06: E014 и список требуемых difficult slices.

- **W1-06-Q01** ([ветка](_WORK/W1/06_SCALE.md)): Q017 → datasets, violation_methods | Есть ли в исходном видео наблюдаемые сигарета/респиратор и корректные состояния; какие camera/session и полные negatives/parent relations доступны? E003/F080/F082 определяют, нужен crop или иной признак. | Полный кейс+целевые данные+annotation audit; P0.

- **W1-06-Q03** ([ветка](_WORK/W1/06_SCALE.md)): Q017 → model_stack | Какой checkpoint/class map/input stride и export route реально доступны; adapter может native batch или делает loop; multiscale/crop training поддерживает корректные ignored/clipped labels? | Проверка конкретной pinned реализации; F074, F075, F076, F077, E016, E017, E018; P0.

- **W1-12-Q05** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q017 → violation_methods/W1-06 | Есть ли нужный визуальный сигнал при реальном масштабе/occlusion? | Ошибки на вручную проверенных crops и эпизодах; невозможность увидеть сигарету/ношение СИЗ не исправляется одним LR

<a id="q018"></a>

## Q018 — Польза и semantics аугментаций

- **Приоритет:** P1.
- **Mode to close:** Dataloader replay/survival + real ablation.
- **Что известно:** Defaults не optimum; bbox-only CopyPaste no-op, erasing classification; Alb2.0.8 signatures не live.
- **Где искали/что прочитали:** W1-05/06; полный history/locators в . Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Before/after labels/relations/ROI/temporal/evidence; clean/real degraded, один intervention.
- **Related IDs:** ; K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

Сборщик выделил вопрос из фактов/контрактов, отдельного branch Q не было.

<a id="q019"></a>

## Q019 — Synthetic assets/masks/relations/review и real transfer

- **Приоритет:** P1.
- **Mode to close:** Assets/ontology + semantic gate + real comparison.
- **Что известно:** Prompt не GT; occlusion не no_PPE. Fully reviewed data-only route конкретен, benefit неизвестен.
- **Где искали/что прочитали:** W1-11; W2-08; полный history/locators в [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-11](_WORK/W1/11_SYNTHETIC.md), [W2-08](_WORK/W2/08_SYNTHETIC_SUPERVISION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Whole-frame review/train-only provenance; updates/real/synthetic draw ledger и independent real holdout.
- **Related IDs:** [F055](RAW_FACTS.md#f055), [F071](RAW_FACTS.md#f071), [F133](RAW_FACTS.md#f133), [F141](RAW_FACTS.md#f141), [F142](RAW_FACTS.md#f142), [E012](RAW_FACTS.md#e012), [E030](RAW_FACTS.md#e030), [E031](RAW_FACTS.md#e031); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-05-Q06** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q019, P1, W1-11:** есть ли masks и валидированные person-PPE group relations для copy-paste? Передавать F055/F071; просто включить `copy_paste` для bbox-only недостаточно.
- **→ linq_platform/model_stack:** перечисленные data augmentations не являются доказательством исполнения на ускорителе. Сохранять итоговый checkpoint и фактические input shape/preprocessing; экспорт/квантизацию/target runtime проверять отдельно. Ни timings RTX4070, ни память, ни поддержка LinQ не установлены.

Ветка завершена на уровне research: установлены фактические switches/version boundaries, семантические риски и наблюдения, которые разрешают или отвергают вмешательство. Универсальная вероятность/strength для отсутствующих данных намеренно не объявлена найденной.

- **W1-11-Q02** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q019, P0 → datasets / W1-05 / model_stack:** есть ли разрешённые masks и person–PPE groups? F055 показывает no-op bbox-only switch. Если masks нет, сравнить стоимость их проверки с прямой target доразметкой. Авторские pipelines F141/F142 существуют, но интеграция/зависимости не проверены.

- **W1-11-Q04** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q019, P1 → W1-06 / datasets:** какие pixel sizes evidence, occlusion и viewpoints реально отсутствуют в train? F133 не покрывает tiny objects; выбрать один gap до дорогостоящей генерации.

- **W2-08-Q02** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)): Q019 — case/data, P0 для trial | Ontology, review scope, unknown/ignore/visible masks, независимый real holdout и допустимые train backgrounds ещё не получены. Нужны dataset audit/полный кейс и review pilot | → datasets/violation_methods; разрешает fully reviewed route либо делает real annotation первым выбором

- **W2-08-Q03** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)): Q019 — experiment, P1 | Полезна ли синтетика относительно real correction/annotation при фактических human minutes и target failure slice? Закрывается E030/E02 с E031 accounting | → evaluation/очередь W2-12; publication AP не задаёт expected benefit или optimal ratio

<a id="q020"></a>

## Q020 — Gen2Det author fork/config/schema и actual loss

- **Приоритет:** P1 conditional.
- **Mode to close:** Новый primary artifact; затем correctness test.
- **Что известно:** После paper/author pages/GitHub exact search code не найден, это не отсутствие capability. p whole batches,tau_i0 synthetic bg RPN+head,lowdata иной.
- **Где искали/что прочитали:** W2-08 S01–S04/search log; полный history/locators в [W1-11](_WORK/W1/11_SYNTHETIC.md), [W2-08](_WORK/W2/08_SYNTHETIC_SUPERVISION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Author fork+commit/filter/sample schema/empty/assignment/reduction/sampling/final graph; до этого reviewed route.
- **Related IDs:** [F139](RAW_FACTS.md#f139), [E030](RAW_FACTS.md#e030), [E031](RAW_FACTS.md#e031); K008.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-11-Q05** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q020, P1 → model_stack / W1-03:** поддерживает ли выбранный trainer ignore regions/partial labels, если filtering удаляет annotation, оставляя object? F139 требует loss changes; plain folder merge не воспроизводит Gen2Det.

- **W2-08-Q01** ([ветка](_WORK/W2/08_SYNTHETIC_SUPERVISION.md)): Q020 — author artifact, P1 | Получить author release/fork+commit, exact configs и filtering→serialized dataset examples; проследить class matching, empty images, source metadata, все affected losses/reductions, sampler и final checkpoint. Искали S099, S191, S192, S193; public code не найден. Новый поиск только при новой первичной ссылке/выдаче артефакта, не бесконечный поиск по тому же названию | → model_stack; special-loss synthetic сейчас не concrete recipe. K008 остаётся с этим gap

<a id="q021"></a>

## Q021 — One-stage online SSOD loop/state/extraction exact family

- **Приоритет:** P1 conditional.
- **Mode to close:** Artifact lock + correctness/extraction smoke.
- **Что известно:** UTv2 std остаётся eval field/teacher default. ET active YOLOv5, onlineEMA/secondary/best/export различны, raw decoder/domain heads.
- **Где искали/что прочитали:** W2-03; полный history/locators в [W1-07](_WORK/W1/07_DOMAIN.md), [W1-09](_WORK/W1/09_PSEUDO.md), [W2-03](_WORK/W2/03_ONESTAGE_SSL.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Один compatible route; geometry/empty/mixed/nohiddenGT/branch hashes/extraction/export, затем supervised comparison.
- **Related IDs:** [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F206](RAW_FACTS.md#f206), [F207](RAW_FACTS.md#f207), [E026](RAW_FACTS.md#e026); K003.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-07-Q04** ([ветка](_WORK/W1/07_DOMAIN.md)): Q021 | Какой trainer реально поддерживает выбранный detector и source-free режим? | AT code — конкретный Detectron2/Faster R-CNN, S050, S051, S052, S053. model_stack: предъявить pinned implementation, dry-run loss/loader test, извлечение одного teacher, exporter compatibility. Поддержка YOLO не установлена

- **W1-09-Q02** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q021 → model_stack (высокий):** какая конкретная student architecture/version имеет runnable supervised trainer, class/box contract и export? Есть ли проверенная SSOD implementation именно этой головы и partial-label loss? Проверенные здесь Faster R-CNN repos и FCOS UTv2 не закрывают вопрос YOLO.

- **W2-03-Q01** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q021 artifact/environment P1 | UT model zoo Coming soon; точный lock/pretrained detector не получен; ET weight links не binary check | Получить weights/provenance/lock и bounded E026; не считать уже runnable

- **W2-03-Q02** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q021 experiment P1 | UT std removal не входит в score, но parity/load/export не выполнены; ET --da/raw decoder code прочитан, ONNX schema не проверена | Extraction/export parity до long trial; определяет пригодность/цену single detector

- **W2-03-Q06** ([ветка](_WORK/W2/03_ONESTAGE_SSL.md)): Q021 experiment/state P1 | Empty/mixed U gradients, real semantics-preserving transforms, full resume двух EMA/adaptor не проверены | E026 diagnostics/reload; unmet budget→corrected supervised

<a id="q022"></a>

## Q022 — Source-free artifact и BN/eval/JSON/hook/selection

- **Приоритет:** P2.
- **Mode to close:** Compatible checkpoint + bounded smoke + labeled V.
- **Что известно:** simple-SFOD code есть, local weights; eval-only меняет BN, manualJSON/sourcevalhook risk. Fixed-row selection gap.
- **Где искали/что прочитали:** W2-07; полный history/locators в [W2-07](_WORK/W2/07_SOURCEFREE_ROUTE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Exact source detector, frozen eval buffers, U-only AdaBN/explicitJSON/no sourceGT hooks; V selection/H.
- **Related IDs:** [F241](RAW_FACTS.md#f241), [F242](RAW_FACTS.md#f242), [E020](RAW_FACTS.md#e020); K007.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W2-07-Q01** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q022 | Artifact: source detector weights и exact preprocessing/class-map | Compatible checkpoint от model_stack/авторов либо отдельный source training вне текущей волны; до этого no runnable package claim

- **W2-07-Q02** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q022 | Public/protocol: fixed-row checkpoint selection, exact AdaBN sampling/reset/momentum и cutoff0.7 helper vs intended recipe | Full resolved run/config от авторов или собственный заранее заданный V-based protocol; не объединять несовпадающие code/paper настройки

- **W2-07-Q03** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q022 | Implementation: JSON replacement, hidden GT/source hooks, import dependencies, empty-pseudo images, ordinary eval и BN state | Только reviewed smoke E020; статическое чтение уже локализовало пути, дополнительный общий обзор SFOD не требуется

- **W2-07-Q05** ([ветка](_WORK/W2/07_SOURCEFREE_ROUTE.md)): Q022 | Experiment: target benefit и retention | Paired E020 с independent labels; unlabeled loss не закрывает вопрос

<a id="q023"></a>

## Q023 — Detector QAT lock/export artifact/architecture

- **Приоритет:** P1 conditional.
- **Mode to close:** Artifact lock/sample + parity smoke.
- **Что известно:** YOLOv7 featureMSE/noGT route; historical YOLO/toolkit не pinned. Reference2.1.2 не installed author env.
- **Где искали/что прочитали:** W2-09; полный history/locators в [W1-13](_WORK/W1/13_COMPRESSION.md), [W2-09](_WORK/W2/09_DETECTOR_QAT.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Container/package/source/weight/ONNX hashes, ranges/export outputs/SDK; supervisedport назвать новым.
- **Related IDs:** [F256](RAW_FACTS.md#f256), [F257](RAW_FACTS.md#f257), [F258](RAW_FACTS.md#f258), [F259](RAW_FACTS.md#f259), [F260](RAW_FACTS.md#f260), [E037](RAW_FACTS.md#e037), [E049](RAW_FACTS.md#e049); K009.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-13-Q05** ([ветка](_WORK/W1/13_COMPRESSION.md)): - **Q023 → model_stack:** поддержан ли QAT выбранным training/export stack именно для этого detector, и соответствует ли он Q008? Training flags не выдуманы.

- **W2-09-Q01** ([ветка](_WORK/W2/09_DETECTOR_QAT.md)): **Q023 — artifact/environment, P1 → model_stack.** Для выбранной архитектуры получить единый manifest: source SHA detector и QAT patch, wheel version/hash toolkit, torch/ONNX/exporter versions, container digest, checkpoint class definitions и SHA256, calibration/range state, export command/effective settings, sample FP+QDQ graphs с expected outputs. Что известно: все code locators F256, F257, F258, F259, F260 доступны; чего нет: verified historical combination и полученный binary graph. Закрытие — предоставленный авторский lock либо отдельный будущий compatibility smoke на явно выбранных pins. Не выдавать reference toolkit 2.1.2 за установленную автором версию. Для PPE потребуется готовый supervised FP checkpoint; этот script не добавляет новые классы.

<a id="q024"></a>

## Q024 — Physical pruning old topology/recovery/usefulness

- **Приоритет:** P2.
- **Mode to close:** Custom artifact + conversion/reload/export smoke.
- **Что известно:** TP1.6.1/U8.0.90/C2f_v2/patchedtrainer/fullobject; YAML+state_dict не topology; MACratio не latency, no rollback.
- **Где искали/что прочитали:** W2-10; полный history/locators в [W2-10](_WORK/W2/10_PHYSICAL_PRUNING.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Conversion parity/customimport/headclass/compile доrecovery; native smaller comparator, actual target timing.
- **Related IDs:** [F262](RAW_FACTS.md#f262), [F263](RAW_FACTS.md#f263), [E050](RAW_FACTS.md#e050); K010.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W2-10-Q01** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)): Q024 / experiment-artifact / P2 | Выполняется ли T/U/PyTorch 2.5.1 комбинация, сохраняет ли C2f conversion output parity и clean reload? Есть код и compatibility pin, но ничего не запускалось; README предупреждает о version drift. | Bounded E050 steps 1–3, до recovery. Failure держит pruning вне practical queue.

- **W2-10-Q02** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)): Q024 / case-data-experiment / P2 | Даёт ли пруненный larger model лучшее constrained quality/target cost, чем native smaller student и FP continuation? Целевых данных/thresholds/проверенных weights нет. | Получить полный кейс и labels, выполнить контролируемый E050 recovery/selection; не переносить coco128/mAP screenshot.

- **W2-10-Q04** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)): Q024 / experiment / P2 | Есть ли actual target latency/memory gain с сохранением quality и оправданным T_ready? Авторский speed_up здесь MAC ratio; exact runtime timing не представлен. | E050 final gate, одинаковые runtime/input/batch/time boundaries и native control.

- **W2-10-Q05** ([ветка](_WORK/W2/10_PHYSICAL_PRUNING.md)): Q024 / artifact-port / P2 | Если команда выберет U 8.4.184/YOLO26 либо другую модель, кто поддержит forward/dependency/exclusion/save/export port? Этот route этого не устанавливает. | Сначала показать необходимость после native baseline; затем отдельный versioned port+smoke, а не механически обновлять pip/импорты.

<a id="q025"></a>

## Q025 — Immutable candidate saver/evaluator/resume/stages

- **Приоритет:** P0 training; exact P1.
- **Mode to close:** Callback/evaluator + fresh-process smoke.
- **Что известно:** on_model_save доstrip; prestrip EMA, online/RNG/loader/scheduler нет; booleanresume может стать warmstart.
- **Где искали/что прочитали:** W2-11; полный history/locators в [W1-15](_WORK/W1/15_SELECTION.md), [W2-11](_WORK/W2/11_CHECKPOINT_CONTROL.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Copy/hash ledger/save/val/pathbasedeval; explicit prestripresume vs newstage resumeFalse; exactstate требует иного saver.
- **Related IDs:** [F185](RAW_FACTS.md#f185), [E035](RAW_FACTS.md#e035); K011.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-15-Q03** ([ветка](_WORK/W1/15_SELECTION.md)): Q025 → model_stack / W1-12 | Как сохранить epoch, оптимальный по нужной цели; где online/EMA/stripped/resume artifacts и RNG state | Проверить hooks/save cadence/reload выбранного version; F185 и F152. Не полагаться на имя best.pt

- **W2-11-Q02** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)): Q025 / artifact+experiment, P0 | Работают ли copy callback, fresh-process load/resume и stage2 в фактической package/dependency среде? | E035; public code не runtime результат

- **W2-11-Q03** ([ветка](_WORK/W2/11_CHECKPOINT_CONTROL.md)): Q025 / experiment, P1 | Нужно ли сохранять exact online/RNG/loader/scheduler/gradient state для иной цели продолжения? | Если нужно exact trajectory, штатный формат U недостаточен: отдельный reviewed serializer/trainer contract и тест. Не обещать восстановление задним числом

<a id="q026"></a>

## Q026 — Paired/group uncertainty и repeat/sample/split design

- **Приоритет:** P1.
- **Mode to close:** Данные + evaluation estimator.
- **Что известно:** Sample/optimizer/split/resampling seeds различны. Degenerate/zero support CI unavailable; seeds не новые scenes.
- **Где искали/что прочитали:** W1-15; W2-05/12; полный history/locators в [W1-14](_WORK/W1/14_COMPUTE.md), [W1-15](_WORK/W1/15_SELECTION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Hierarchy/estimand/paired groups/all repeats/cap; при нехватке independent support нужны новые группы.
- **Related IDs:** [F177](RAW_FACTS.md#f177), [E044](RAW_FACTS.md#e044), [E047](RAW_FACTS.md#e047); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-14-Q04** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q026 → evaluation/W1-15:** какой эффект меняет решение, какие slices критичны, сколько paired repeats оправдано? Seeds не должны замещать независимые группы. Источники F177 и proposed E044.

- **W1-15-Q04** ([ветка](_WORK/W1/15_SELECTION.md)): Q026 → evaluation | На каком уровне resampling отвечает operational claim; достаточен ли rare support для interval | Задать camera/session hierarchy и metric estimator; E047. Нельзя получить значимое n из кадров одного события

<a id="q027"></a>

## Q027 — Resource costs/D_useful/ownership/critical path

- **Приоритет:** P0 scheduling.
- **Mode to close:** Inventory + bounded profile/time + owner.
- **Что известно:** RTX4070 не VRAM/минуты. DDP не объединяет память; setup/validation/save/export/review могут доминировать.
- **Где искали/что прочитали:** W1-14; W2-11/12; полный history/locators в [W1-10](_WORK/W1/10_TEACHER.md), [W1-12](_WORK/W1/12_OPTIMIZATION.md), [W1-14](_WORK/W1/14_COMPUTE.md), [W1-15](_WORK/W1/15_SELECTION.md), [W2-12](_WORK/W2/12_TRIAL_QUEUE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Stage timestamps/headroom/personminutes/GPUhours/queue; admit now+CP_remaining<=D_useful.
- **Related IDs:** [F009](RAW_FACTS.md#f009), [F042](RAW_FACTS.md#f042), [F115](RAW_FACTS.md#f115), [F116](RAW_FACTS.md#f116), [F148](RAW_FACTS.md#f148), [F168](RAW_FACTS.md#f168), [F169](RAW_FACTS.md#f169), [F177](RAW_FACTS.md#f177), [F278](RAW_FACTS.md#f278), [F279](RAW_FACTS.md#f279), [E023](RAW_FACTS.md#e023), [E027](RAW_FACTS.md#e027), [E034](RAW_FACTS.md#e034), [E040](RAW_FACTS.md#e040), [E042](RAW_FACTS.md#e042), [E047](RAW_FACTS.md#e047); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-10-Q07** ([ветка](_WORK/W1/10_TEACHER.md)): Q027 | Реальная цена teacher pool inference и исправления; помещается ли teacher+student в доступную VRAM? | E023/E027 profiling на фактической конфигурации; → W1-14

- **W1-12-Q04** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q027 → W1-14/video_architecture | Какие реальные B, accumulation, OOM retries, loader stalls и precision? | E034 + profiling; никакой оценки времени или VRAM по имени RTX 4070

- **W1-14-Q01** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q027 → model_stack, приоритет первый:** какой checkpoint/trainer/image shape реально выбран и сколько памяти занимает один полный training step вместе с optimizer/EMA/объектами? От этого зависит batch, accumulation и вообще смысл DDP. Получить manifest и E040, не выводить из названия RTX 4070.

- **W1-14-Q02** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q027 → training owner/окружение:** какая ОС, torch wheel/backend, GPU count/topology, CPU/RAM/shared memory, local/network storage и доступ? S105 даёт конкретный Windows compatibility gate, но окружение неизвестно. Способ ответа — inventory и bounded startup E042; не покупка ресурсов.

- **W1-14-Q05** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q027 → W1-12/model_stack:** требуется ли изменение цикла accumulation для no_sync и как проверить loss normalization, BN и хвосты? S011 показывает текущее поведение, но правка trainer здесь не сделана и её выгодность не установлена. Нужен trace E042 и correctness comparison до изменения.

- **W1-14-Q06** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q027 → linq_platform/video_architecture:** какое время нужно на фактический export/compile/upload/inference verification и какие входы/модели допустимы? Этот последовательный gate должен участвовать в T_ready; RTX profiling и Ultralytics `profile` его не измеряют.

- **W1-14-Q07** ([ветка](_WORK/W1/14_COMPUTE.md)): - **Q027 → hackathon_strategy:** какие подтверждённые сроки checkpoint/integration и какой человек принимает quality решение? Параллельность GPU ограничена доступным review; рекомендации этой ветки не являются обещанным расписанием.

Главная оставшаяся неопределённость эмпирическая: неизвестен workload и bottleneck. Первичные документы достаточны для выбора измерений и обнаружения скрытых изменений recipe, но не дают честной численной оценки скорости/стоимости нашей команды.

- **W1-15-Q07** ([ветка](_WORK/W1/15_SELECTION.md)): Q027 → W1-14 / hackathon_strategy | Какой repeat и integration reserve реально помещаются по измеренным затратам | Короткое profiling/стоимость baseline; заранее cap E047. «Сделать 30 seeds» не вытекает из TFA для 45 часов

- **W2-12-Q04** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q027 | Experiment/resource: T_setup/train/validate/save/export/decision, H_annotation/review, throughput/headroom/contended owners | W1-14 bounded profiling/cost pilot и W2-11 serialized save timing. Пока unknown — нет честного numerical schedule/DDP/teacher promise.

- **W2-12-Q06** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q027 | Integration/human process: кто и к какому фактическому D_useful принимает artifact, сколько занимает review/SDK очередь? | Назначить owner и измерить downstream path. Не подменять фиксированным 45h timetable или универсальной долей reserve.

<a id="q028"></a>

## Q028 — Early quality proxy для immutable full recipe

- **Приоритет:** P2; no proxy default.
- **Mode to close:** Full histories + dev rank-reversal analysis.
- **Что известно:** Hyperband/ASHA не detector-ranking guarantee. ShortU меняет auto/warmup/schedule/mosaic, resume не exactprefix.
- **Где искали/что прочитали:** W2-12; полный history/locators в [W2-12](_WORK/W2/12_TRIAL_QUEUE.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Short runs correctness-only; proxy при самостоятельной нужде/историях/support/полном artifact deadline.
- **Related IDs:** [F278](RAW_FACTS.md#f278), [F279](RAW_FACTS.md#f279), [E051](RAW_FACTS.md#e051); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W2-12-Q05** ([ветка](_WORK/W2/12_TRIAL_QUEUE.md)): Q028 | Experiment/fidelity: есть ли полезный early signal при immutable full recipe, реальном critical support и continuation contract? | По умолчанию no proxy ranking. Только при самостоятельной потребности и уже доступных full-budget histories проверить rank reversals/late gains и именно критичные constraints на dev. Новый pilot должен сам помещаться в CP; не запускать специально HPO grid ради оправдания HPO. S218/S219 не закрывают этот вопрос.

<a id="q029"></a>

## Q029 — Object/association/temporal attribution и trace interface

- **Приоритет:** P0 event error.
- **Mode to close:** Кейс + stage logs/oracle substitution.
- **Что известно:** BoxAP не wearing/zone/smoking event. Сохраняющаяся с oracle objects ошибка не основание detectortraining.
- **Где искали/что прочитали:** W1-01-E02; W1-06/07/15; полный history/locators в [W1-01](_WORK/W1/01_BASELINE.md), [W1-05](_WORK/W1/05_AUGMENTATION.md), [W1-09](_WORK/W1/09_PSEUDO.md), [W1-11](_WORK/W1/11_SYNTHETIC.md), [W1-15](_WORK/W1/15_SELECTION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** A обычные→B правильныеobjects→C правильныеrelations при fixedrules; решает training vs logic/context.
- **Related IDs:** [F001](RAW_FACTS.md#f001), [F002](RAW_FACTS.md#f002), [F009](RAW_FACTS.md#f009), [F050](RAW_FACTS.md#f050), [F051](RAW_FACTS.md#f051), [F055](RAW_FACTS.md#f055), [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F130](RAW_FACTS.md#f130), [F177](RAW_FACTS.md#f177), [E024](RAW_FACTS.md#e024), [E025](RAW_FACTS.md#e025), [E026](RAW_FACTS.md#e026), [E046](RAW_FACTS.md#e046); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-01-Q05** ([ветка](_WORK/W1/01_BASELINE.md)): Q029 | Доступна ли stage-level подстановка объектов/связей в event rules | violation_methods/video_architecture; если нет — минимальный trace contract, средний

- **W1-05-Q05** ([ветка](_WORK/W1/05_AUGMENTATION.md)): - **Q029, P1, violation_methods/video_architecture:** используются ли camera-fixed ROI, tracks или клипы? Для них transforms должны включать ROI/relations и temporal coherence. Иначе ограничить вмешательство обучением object detector с отдельным неизменным event layer.

- **W1-09-Q06** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q029 → violation_methods:** teacher boxes не являются подтверждённым нарушением. Ошибка связи person–PPE, temporal state, опасной зоны и невидимого объекта может не устраняться pseudo-labeling; audit должен отделить detector failure от отсутствия наблюдаемого сигнала/ошибки правила.

Ветка даёт основание начать с E024 и выбрать E025 либо E026. Она не устанавливает наличие target data, допустимые классы, качество какого-либо teacher на заводских камерах, экономию времени в минутах, достижимый прирост student или поддержку LinQ.

- **W1-11-Q06** ([ветка](_WORK/W1/11_SYNTHETIC.md)): - **Q029, P1 → violation_methods / video_architecture:** нужны ли клипы/tracks? Для них согласовывать pose/camera/lighting/IDs во времени, иначе synthetic frame improvement ничего не говорит о событии; курение и вход в зону требуют отдельной семантики.

- **W1-15-Q05** ([ветка](_WORK/W1/15_SELECTION.md)): Q029 → violation_methods / operator_product | Что именно изменялось: признаки объекта или связь/длительность/зона/cooldown; как трактовать repeated alarms | Полный event contract и E046 factorial table; gains rules сообщать отдельно от training

<a id="q030"></a>

## Q030 — Recipe→checkpoint→published row lineage и contradictions

- **Приоритет:** P1/P2 conditional.
- **Mode to close:** Авторский artifact/log/revision по нужде.
- **Что известно:** SAHI abstract/table/config; SoftTeacher jitter/LR/README; FGDgamma; DETReg2023assets; SFODcutoff/selection differences сохранены.
- **Где искали/что прочитали:** W1-02/03/05/06/09/10/11; W2-06/07/08; полный history/locators в [W1-03](_WORK/W1/03_FEWSHOT_PARTIAL.md), [W1-06](_WORK/W1/06_SCALE.md), [W1-09](_WORK/W1/09_PSEUDO.md), [W1-10](_WORK/W1/10_TEACHER.md), [W2-01](_WORK/W2/01_NATIVE_KD_CONTRACT.md), [W2-06](_WORK/W2/06_DETECTION_PRETRAINING.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Для буквальной replication exactconfig/hash/tablemap; иначе ограниченное evidence и собственный trial, без третьей волны.
- **Related IDs:** [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F072](RAW_FACTS.md#f072), [F073](RAW_FACTS.md#f073), [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F115](RAW_FACTS.md#f115), [F116](RAW_FACTS.md#f116), [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [E003](RAW_FACTS.md#e003), [E006](RAW_FACTS.md#e006), [E023](RAW_FACTS.md#e023), [E024](RAW_FACTS.md#e024), [E027](RAW_FACTS.md#e027), [E048](RAW_FACTS.md#e048); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-03-Q05** ([ветка](_WORK/W1/03_FEWSHOT_PARTIAL.md)): Q030 | SparseDet split manifests против несогласованного текста; реальные constraints C-RPN и matching dependency versions | Только если ветка выбрана; иначе integration cost/неизвестное достаточно для низкого приоритета

- **W1-06-Q06** ([ветка](_WORK/W1/06_SCALE.md)): Q030 → training_strategy W2 | Нужна ли буквальная SAHI replication? Если да, найти исторический commit и конкретные config/result/checkpoint, разрешить crop480–640 vs480–960 и abstract/table deltas. | Открытые git history/result metadata; P1 при выборе SAHI, иначе известная граница, не blocker.

- **W1-09-Q04** ([ветка](_WORK/W1/09_PSEUDO.md)): - **Q030 → model_stack/W2:** paper/code discrepancies: SoftTeacher LR 110k vs 120k, uniform vs Gaussian jitter; README AP vs paper AP; UT reader commands 16/16 vs config 32/32; точное checkpoint selection и run/fold variability. Для воспроизведения выбрать один полностью resolved recipe и сравнивать внутри него, не объединять удобные части.

- **W1-10-Q05** ([ветка](_WORK/W1/10_TEACHER.md)): Q030 | Native KD table не задаёт полного training protocol/variance. Каковы seeds, schedule, teacher checkpoint provenance и selection? | Найти training artifact/config автора либо воспроизводить как новую собственную проверку; не заполнять пробел предположением

- **W1-10-Q06** ([ветка](_WORK/W1/10_TEACHER.md)): Q030 | FGD paper gamma vs pinned recipe gamma: какой artifact дал опубликованную строку? | Авторский resolved config/checkpoint; до ответа считать два разных recipe

- **W2-01-Q05** ([ветка](_WORK/W2/01_NATIVE_KD_CONTRACT.md)): Q030 — public artifact/experiment, P1 | Есть ли авторский complete YOLO11 KD recipe/quality evidence с teacher hashes и schedule/selection? | В просмотренном guide его нет; package contract позволяет собственный trial. Остаток не повод переносить YOLO26 gain или бесконечно ждать recipe

- **W2-06-Q03** ([ветка](_WORK/W2/06_DETECTION_PRETRAINING.md)): Q030 | **Public recipe/artifact, средний:** точное правило выбора checkpoint для DETReg few-shot и полное соответствие released weights поздним таблицам | Найдено version/changelog и assets, но не training logs/hash→table lineage; при воспроизведении потребуются author logs/config/state. Не отдельная обязательная поисковая волна

<a id="q031"></a>

## Q031 — Serialized selected artifact quality reload/export/quant/target

- **Приоритет:** P0 promotion.
- **Mode to close:** Artifacts + adjacent-stage paired inference/GT.
- **Что известно:** Чтение code не execution. CPU/RTX/ORT не LinQ. Actual training/export/LinQ не выполнены.
- **Где искали/что прочитали:** W1-13-E01/W1-15-E04; W2-01/09/10/11; полный history/locators в [W1-12](_WORK/W1/12_OPTIMIZATION.md), [W1-15](_WORK/W1/15_SELECTION.md). Сборщик новых HTTP не получал.
- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.
- **Недостающее звено / решение / способ закрытия:** Canonical tensors/preprocess/decoder/NMS/rules; raw deviations+GT/support/hashes/placement, frozenbundle+rollback.
- **Related IDs:** [F009](RAW_FACTS.md#f009), [F042](RAW_FACTS.md#f042), [F148](RAW_FACTS.md#f148), [F177](RAW_FACTS.md#f177), [E037](RAW_FACTS.md#e037); K012.

**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):

- **W1-12-Q06** ([ветка](_WORK/W1/12_OPTIMIZATION.md)): Q031 → linq_platform/model_stack | Какой student/checkpoint после EMA и final stripping требуется экспортёру/SDK? | Отдельно пройти load/export/target-execution и paired output/quality check. Training precision и training success не доказывают LinQ support

- **W1-15-Q06** ([ветка](_WORK/W1/15_SELECTION.md)): Q031 → linq_platform / model_stack / W1-13 | Actual export/quant/compiler path, decoding/NMS location, outputs/precision/fallbacks и устройство | SDK/device access + E037. Здесь нет проверенного LinQ quality/speed и нет гарантии поддержанного графа

