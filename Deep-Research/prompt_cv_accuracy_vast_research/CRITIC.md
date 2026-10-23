# Независимая критика первой волны cv_accuracy_vast

Дата: 2026-10-23. Контроль часов при анализе: 17:25:26 UTC / 20:25:26 Europe/Moscow. Это исходная критика **до второй волны**; результаты её закрытия должны быть добавлены позднее с сохранением исходных замечаний.

Прочитаны полностью `Context-prompt.md`, `prompt_cv_accuracy_vast_research.md`, `_WORK/PROMPT_CRITIC.md`, `_WORK/CASE_NOTES.md`, `_WORK/PLAN.md` и все 16 результатов `_WORK/W1_01.md` … `_WORK/W1_16.md`. Большие результаты прочитаны порциями; пропущенные из-за ограничения вывода диапазоны дочитаны отдельно. Дополнительно просмотрены локальные `NEIGHBOR_LEADS.md`, `HANDOFFS.md`, metadata источников и отдельные сохранённые исходники W1-13/14. Нового интернет-поиска, аренды, обучения, экспорта, аппаратных измерений, внешних сообщений и субагентов в этой роли не было. Кейс использован через явно атрибутированные визуальные наблюдения root в `CASE_NOTES.md`; повторного независимого визуального прочтения PDF критик не выполнял.

## Общая оценка

Первая волна содержательна и в основном правильно ограничивает силу выводов. Она уже даёт полезные решения: сначала полный baseline и ошибки, затем узкие изменения; своевременные события и нагрузка уведомлений вместо одного mAP; independent split и закрытый lockbox; одна GPU по умолчанию; отдельные inference/recovery checkpoints; проверка каждого реального deployment bundle на LinQ. Нет основания объявлять всю эту программу методологически несостоятельной или повторять 16 обзоров.

Главный оставшийся разрыв — переход от набора корректных условных протоколов к **одному короткому, непротиворечивому и проверяемому маршруту**. Его исходные материалы ещё не определены: доступны ли нужные видео и метки; какой точный training/export stack берём; какой checkpoint юридически и технически доступен; что реально принимает выданный LinQ; сколько готовых работ существует для второй GPU. Отсутствие собственных target measurements в этом исследовании не является нарушением: большие прогоны прямо не поручены. Недопустимо лишь превращать предлагаемый smoke или будущий эксперимент в пройденный gate.

Есть и конкретная новая проблема, обнаруженная в уже сохранённом исходнике: выбранный Ultralytics автоматически меняет batch и выполняет внутреннее recovery, тогда как программа сравнения трактует OOM/NaN как технически невалидный неизменяемый trial. Это требует отдельного исправления контракта, а не ещё одной общей рекомендации «сохранять checkpoint».

## Что уже достаточно обосновано и не требует повторного обзорного поиска

1. **COCO AP не является качеством заводских событий.** W1-02-F05/F08 перечисляют недостающие классы и малые объекты; W1-01 отделяет object/event/notification metrics. Условия авторских AP/latency и разные pretraining ветки сохранены. Не найдено безоговорочного обещания, что COCO-победитель победит в цехе.
2. **Event quality определена существенно лучше одного F1.** W1-01 даёт timely recall, late/missed/duplicate alerts, exposure, coverage, one-to-one matching, censoring и ограничения CI. ActEV TFA правильно отделён от числа уведомлений. Дубликаты истинного события и неверный участник не исчезают из оценки нагрузки.
3. **«1 FPS достаточно» не рекомендовано.** W1-04-F03/F06, E04 и W1-09 описывают фазу sampling, длительность события, свежесть наблюдения, burst gaps, причинность и цену confirmation. Формула попадания одного идеального sample явно не названа event recall. Остаток здесь — реальные durations, данные и runtime, а не поиск ещё одной статьи против 1 FPS.
4. **Leakage и многократный отбор признаны.** W1-07-F09/W1-11-F10 охватывают lineage исходного видео, crops, синтетику, episode/site/camera grouping, повторный selection и слабость frame bootstrap. SELECT не объявлен новым test после просмотра; tuning lockbox запрещён. Конкретная несогласованность ролей наборов выделена K006, но общего отсутствия защиты нет.
5. **Рецепты и память не представлены сопоставимыми по умолчанию.** W1-06/W1-11 различают equal-updates ablation и resource-bounded product comparison, native schedules, EMA/raw, late phase, physical/effective batch. W1-02-F07/W1-15 правильно отвергают fit по числу параметров и pooling 2×24 GB. Измеренного fit нет и он не заявлен.
6. **Vast исследован по существующим первичным интерфейсам.** W1-12 сохраняет реальные public offers с временем, whole-offer compute, disk, ingress/egress, host/machine IDs и условиями. Storage не прибавляется второй раз к `dph_total`; stopped/expired/destroy/volumes и противоречия billing не замолчаны. Цены не выдаются за резерв.
7. **Recovery существенно глубже совета «сохрани best».** W1-13/14 выявили EMA-only native YOLO state, final stripping, stage-aware D-FINE и Lightning `.ckpt` RF-DETR; copy acceptance отделена от destination bytes/hash/load. Требовать побитовый exact resume от всех stock trainers первая волна не предлагает.
8. **Причины не брать вторую GPU уже сильны.** W1-15 имеет ready-work, per-GPU fit, joint CPU/RAM/I/O, deadline/value/budget gates; DDP отделён от independent jobs. Найден конкретный global/local-rank риск D-FINE multi-node. Общий повторный поиск «почему две GPU не всегда быстрее» не нужен.
9. **Multi-model LinQ не спрятан.** W1-10/W1-16 перечисляют production neural nodes и суммарную/burst нагрузку, proposal ceilings, state reset и fallback. Teacher-only путь отделён от online verifier. Совместимость CUDA/ORT не приравнена к LinQ.
10. **Source freshness в основном зафиксирована.** Ключевые detector/recovery/CLI snapshots имеют полные SHA и даты; HEAD/dev и release различаются. Старые papers используются как механизмы и контрпримеры, а не как latest benchmark. Не требуется обновлять SHA ради самого обновления. Нужен один выбранный набор артефактов, а не новое плавающее latest.

## Замечания K-ID

Обозначения приоритетов: **P0** — меняет допуск ближайшего обучения/финального inference; **P1** — меняет выбор и достоверность сравнения; **P2** — полезная ограниченная доводка. «Неизвестно» не означает «не работает»; «предложено» не означает «выполнено».

### K001 — Автоматические OOM/NaN восстановления нарушают заявленную неизменяемость trial

**Приоритет / тип:** P0; обнаруженный по сохранённому исходнику конкретный пропуск.

**Материал и доказательство.** W1-06-F04, W1-11 раздел `Бюджет, deadline и прекращение поиска`, W1-14 predicate `SUCCEEDED` и W1-15 registry требуют считать OOM/NaN технической неудачей, а изменение batch — новой recipe. Однако `_WORK/W1_14_MATERIALS/ultra_trainer.py` для того же SHA `de290d865035acbfa4bb24cc88960d8b52c26e45`, L566–606, автоматически обрабатывает first-epoch OOM и некоторые backend-memory RuntimeError: уменьшает batch, перестраивает pipeline, **сохраняет существующий optimizer state**, сбрасывает часть счётчиков и повторяет эпоху. L638–640 продолжает loop после recovery. L1089–1126 `_handle_nan_recovery` загружает EMA из `last.pt` в online model, восстанавливает training state и повторяет эпоху. В W1 нет явного разбора этих внутренних переходов. Это статическое наблюдение, не воспроизведённая авария.

**Последствие.** Успешный exit и конечный effective config могут скрыть дополнительные уже обработанные примеры, смену physical batch/accumulation/weight decay и EMA warm restart. Сравнение «A/B с одинаковыми updates и одной recipe» перестаёт быть тем сравнением, которое записано в spec. Внешний controller, видящий только итоговый CSV и exit code, может пропустить нарушение.

**Точно недостающее доказательство.** Семантика всех native recoveries на выбранной **исполняемой** ревизии, доступный способ их обнаружить/запретить; перечень реально изменяемого состояния и счётчиков; правило регистрации такой попытки. Отдельно проверить accumulation на native epoch checkpoint: `nbs>batch` не гарантирует отсутствие незавершённых gradients на конце эпохи, а resume начинает с `zero_grad` (L494). Уже признанный режим `native_ema` допустим, но нельзя поверх него обещать точную lossless boundary.

**Задание второй волны / закрытие.** W2-A: независимо прочитать релевантные source paths и официальные callback/override интерфейсы, предложить минимальную fail/fork policy. Результат — таблица `trigger → hidden mutation → detection → allowed status → next action`, точные locators и небольшой будущий negative drill. Если безопасного stock switch нет, явно выбрать обнаружение и новый run либо зафиксированный adapter; не выдумывать флаг. Закрыть документальный контракт можно статическим evidence; runtime/RPO подтверждение остаётся отдельной короткой практической проверкой. Не запускать training в research.

### K002 — Есть pinned base image, но нет согласованного training/export recipe одного кандидата

**Приоритет / тип:** P0; локализованный пробел воспроизводимости, не утверждение об ошибочности новых версий.

**Материал и доказательство.** W1-13-F01 предлагает PyTorch `2.14.1-cuda12.6-cudnn9-runtime` и digest, прямо называя его candidate. W1-02/06 используют текущий Ultralytics и RF-DETR dev snapshot, D-FINE — другую dependency историю. W1-16 отдельно показывает, что YOLO wrapper задаёт `dynamo=False`, а D-FINE exporter не фиксирует mode и наследует Torch default. W1-13 приводит generic API Torch и признаёт отсутствие final lock/derived image. Ни один результат не предъявляет единую разрешённую комбинацию Python/Torch/vision/exporter/ONNX/ORT для первого baseline и запасного пути.

**Последствие.** Сборка наиболее нового base, native requirements и экспортного инструмента может потребовать отдельной отладки уже на оплачиваемом host. «Все SHA закреплены» не означает, что такие пакеты совместимы друг с другом. Случайная замена Torch ради exporter создаст другой recipe и может изменить checkpoint loading или serialized graph.

**Точно недостающее доказательство.** Для одного baseline и одного нужного challenger — объявленные первичными проектами ограничения и конкретный выбранный compatibility envelope; explicit exporter implementation/mode/flags; путь резервного более консервативного стека; список зависимостей, которые ещё только предстоит разрешить/проверить. Фактический installed lock может появиться только при сборке и не должен быть подменён выдуманным.

**Задание второй волны / закрытие.** W2-B: проверить requirements/pyproject, native training/export docs, релевантные официальные release notes и несовместимые API для **выбранных** snapshots. Выдать два коротких recipe manifests с exact entrypoints и статусом каждого поля, разделить training и export environment при необходимости. Не строить универсальный образ для всех семейств. Документальная часть закрывается source-backed envelope; imports/forward/backward/export/24GB peaks — `not run`, с последовательностью smoke после отдельного поручения.

### K003 — Лицензия и доступность конкретных весов ещё не закрывают практический shortlist

**Приоритет / тип:** P0 до передачи/распространения; признанный, но существенный пробел.

**Материал и доказательство.** W1-02-F06 хорошо различает AGPL/Enterprise, Apache-designated RF-DETR и non-commercial DEIMv2/EdgeCrafter. Но для D-FINE/RT-DETRv2/YOLOX остаётся code LICENSE вместо полного provenance выбранных checkpoint/backbone; RTMPose-s в W1-03 имеет точный URL, но отдельный grant не установлен. Часть весов найдена лишь как авторские ссылки; бинарная доступность и содержимое не проверены. RF Large legacy/current различены, но нельзя растянуть найденный grant на произвольный variant или dependency.

**Последствие.** Команда может выбрать permissive код и получить неустановленные условия initialization, backbone или данных; либо потратить integration window на недоступный asset. С другой стороны, автоматически исключать модель лишь из-за отсутствия отдельного weight LICENSE тоже было бы необоснованно: нужен конкретный статус, а не юридическая догадка.

**Точно недостающее доказательство.** Для фактически retained весов — первичный model card/release/license scope, способ получения, revision/имя, notices и известный training lineage; какие условия прямо распространяются на веса, а какие лишь на код. Отдельно выбранный способ поставки AGPL-кандидата. Не требуется юридически доказывать разрешённость всех upstream фотографий интернета.

**Задание второй волны / закрытие.** W2-C закрывает detector weights, W2-E — один specialist. Проверить точный asset и легковесные metadata/redirect/content-type, не загружая большие бинарники без нужды; сохранить grant locators. Итоговая таблица: `explicit grant / project-level claim / unresolved / incompatible with chosen use`, без автоматического вывода «все .pth Apache». Реальный SHA256 байтов и окончательное принятие условий остаются gate получения артефакта. Нерешённый кандидат сохраняется условно, а не под видом проверенно permissive.

### K004 — Приоритет detector challengers пока основан на удобстве и общем benchmark, а не на сопоставимом evidence для доминирующей ошибки

**Приоритет / тип:** P1; пробел обоснования порядка, не обнаруженное ложное ранжирование.

**Материал и доказательство.** W1-02 назначает YOLO26s первым baseline, D-FINE-M основным challenger, RF-DETR-M альтернативой; W1-06/11 наследуют этот порядок. Таблица аккуратно разделяет dense/e2e, COCO/O365, T4/V100 и разные input. Но нет согласованного разбора сравнимых малых объектов/окклюзии для этой пары и цены родного short fine-tune. Опубликованные AP не дают оснований ожидать именно phone/PPE event improvement. W1 это признаёт; критик не превращает отсутствие собственных данных в требование уже назвать победителя.

**Последствие.** Сильная условная рекомендация может быть прочитана как технически доказанный accuracy ranking. При одном полезном challenger run команда должна понимать, почему он, а не higher-resolution/crop/label fix текущей модели, меняет нужное решение.

**Точно недостающее доказательство.** Минимальная like-for-like таблица для baseline и одного challenger: evaluator/split/input/head/pretraining/train exposure и доступные size/occlusion/domain results. Где контролируемого сравнения нет — явный `not comparable`. Нужна одна конкретная гипотеза ошибки, а не ещё десять архитектур.

**Задание второй волны / закрытие.** W2-C искать ограничивающее evidence в авторских papers/configs/ablation, особенно AP_small/разрешение/дополнительное pretraining и target adaptation. Либо подтвердить содержательное основание конкретного challenge, либо понизить его до «проверяем по инженерной удобности» и поставить перед ним spatial/data ablation. Закрытие не требует и не допускает объявить COCO ranking заводским. Финальный порядок меняется после DEV error audit, target superiority остаётся unknown до будущего опыта.

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

### K008 — Для temporal/verifier части shortlist содержит архитектуры, но не конкретных воспроизводимых кандидатов

**Приоритет / тип:** P1; неполнота обязательного shortlist, частично оправданная границами темы.

**Материал и доказательство.** RTMPose-s в W1-03 имеет config/checkpoint; W1-04 прямо говорит, что TSM/MoViNet/SlowFast/PoseC3D — архитектурные основания, а не выбранные deployment weights. W1-10 crop specialist описан без family/checkpoint/trainer. Теория proposal ceiling и условного вызова хороша, но команда пока не может оценить цену запуска **одного** такого кандидата. Полный поиск поведенческих весов вынесен отдельно и здесь не нужен.

**Последствие.** «Добавим лёгкий verifier» может оказаться новой разработкой модели, loss/data contract, export и runtime state вместо небольшого улучшения. Distillation тоже не является готовой запасной кнопкой; первая волна это верно признаёт, но shortlist всё ещё выглядит более готовым, чем набор её артефактов.

**Точно недостающее доказательство.** Один конкретный initialization/recipe для компактного crop classifier и один ограниченный causal temporal вариант **либо** явное решение отложить neural temporal branch. Для retained кандидата: source/config, weights/license, input preprocessing/classes, native export boundary, state/reset и train-data requirements. Отсутствие phone-use/fall классов в generic pretraining писать явно.

**Задание второй волны / закрытие.** W2-E выбрать по механизму ошибки K005 максимум один verifier и один representative temporal route; не обозревать всё action recognition. Проверить official model card/config/weights и online-vs-offline checkpoint semantics, особенно возможность ошибочно выдать bidirectional pretrained за causal. Результат — конкретная карточка «готовый initialization для будущего fine-tune» или «architecture-only, не включать в первые runs» с причинами. Наличие лицензированного generic веса не доказывает target ability, 24GB fit и LinQ pass.

### K009 — Публичный LinQ путь исторический; нет проверенного запасного baseline и не разрешён neural CPU boundary

**Приоритет / тип:** P0 до финального выбора; главным образом внешний unknown.

**Материал и доказательство.** W1-16-F06 нашёл manual IVA H1 2025 с ONNX→TF→quantized→TPU и tested `yolo5s`; полный текст сохранён через extract, PDF bytes/screenshots не получены. Это реальное документальное основание, но не operator matrix актуального сервера. Основной YOLO26s и запасной YOLOX-s не являются испытанными на LinQ в этой работе. W1-10/16 правильно требуют учёта всех neural nodes, а допустимость neural CPU внутри LinQ-сервера оставляют организаторам. Последнее — консервативная плановая обязанность, **не найденная буквальная формула кейса «каждая сеть только на TPU»**.

**Последствие.** Поздний отказ TopK/Gather/shape/export может оставить команду без финального neural path. С другой стороны, чрезмерно строгая трактовка CPU запретит допустимую архитектуру без основания. Повторный полный research LinQ здесь нарушит границы и всё равно не заменит закрытый SDK.

**Точно недостающее доказательство.** Узкое публичное подтверждение применимого примера/артефакта и точная identity исторического fallback; визуальная проверка критичных страниц manual/команд, если PDF удастся получить. Отдельно — delivered SDK/SKU/operators, разрешённый neural CPU/fallback path, model residency/concurrency и фактическое выполнение каждого retained node. Последнее публичным поиском может не решаться.

**Задание второй волны / закрытие.** W2-F проверить первичные текущие публичные docs/examples ровно для раннего smoke и fallback; разнести `historically demonstrated / publicly documented / source-inferred / device-unverified`. Не объявлять YOLOv5 совместимым серверу 2026 по одному старому manual и не заменять baseline автоматически. Выдать точный bundle handoff и краткую последовательность probes для владельца выданного SDK, включая multi-model burst/residency и CPU boundary. Если actual package нет, K009 закрывается **уточнением границы**, а execution остаётся открытым Q. Полное PTQ/QAT исследование не запускать.

### K010 — Lifecycle/стоимость описаны хорошо, но выбранный CLI artifact и спорные billed states ещё не дают однозначного runbook

**Приоритет / тип:** P0 до оплаты/удаления единственной копии; ограниченный документальный и аккаунтный пробел.

**Материал и доказательство.** W1-13-F04 различает CLI HEAD `42c3a47…` и release v1.9.0 `28bde482…`; `copy()` с непроверенным subprocess returncode проанализирован на HEAD. Пример интерфейса не гарантирует ту же семантику у будущего `pip install vastai`. W1-12-F08/W1-14 сохраняют current/legacy конфликт offline billing и неоднозначность loading; stopped rate, image/package ingress, byte divisor и account autobilling/invoice не проверены. Это честные ограничения, но их нельзя потерять при сжатии до «$0.218/h, stop выключает».

**Последствие.** Поведение transfer/SSH и lifecycle может не совпасть с source claim, а полный счёт — с headline. Формула W1-12 уже достаточна; проблема в заполнении конкретного contract и необоснованном снятии unknowns. Даже valid copy command не отменяет destination hash/load.

**Точно недостающее доказательство.** Один выбранный CLI release/source artifact и его API behavior для search/show/copy/stop/destroy; таблица `running/loading/stopped/offline/expired/destroyed/volume → documented charge → conflict → verification`. Для финальных значений — account Charges/Invoice и refreshed offer после отдельного разрешения владельца; их нельзя получить из старой public quote.

**Задание второй волны / закрытие.** W2-G сравнить relevant release и HEAD code paths, актуальные первичные docs/schema, дать точные non-executed команды с выбранной версией и platform caveat Windows/rsync. Разрешить документальные противоречия, где есть первичное основание; остальное оставить Q с конкретной строкой Charges/единицей проверки. Не нужен новый обзор рынка, покупка, учётные ключи или ручная имитация invoice. Destroy разрешён в будущем только после receipt архива в рамках отдельно порученного lifecycle; во второй волне ничего не арендовать/удалять.

### K011 — Нет единого маршрута на оставшееся окно и дешёвого режима при незакрытых gates

**Приоритет / тип:** P0/P1; интеграционный пробел программы, а не отсутствие законных вымышленных GPU-hours.

**Материал и доказательство.** W1-11 ограничивает очередь B0→до двух ablations→один challenger→confirmation; W1-15 правильно задаёт DAG одной/двух GPU. Но сумма отдельных W1 экспериментов (pose, trackers, data selection, augmentation, calibration, specialists, DDP, recovery controller) намного шире этой очереди. Нет одного выбранного первого сценария/recipe, owner allocation пяти людей, общего freeze point относительно checkpoint 24.10 11:00/18:00 и сдачи 25.10 10:00, а также stop condition по человеку/разметке/SDK. На контрольное время критика до сдачи оставалось примерно **37 ч 35 мин**, не исходные 45 ч от публикации задания. Это арифметика расписания `CASE_NOTES.md`, не оценка длительности training.

**Последствие.** Можно потратить доступное окно на сборку контейнера, строгий exact-resume adapter, controller/generation protocol и сложный nested evaluation, не получив один полный работающий сценарий. Также возникает круг «до аренды измерить 3090 fit» при ещё не имеющейся 3090. Локальная RTX 4070 есть по контексту, но её VRAM/окружение не установлены; она не доказывает 24GB fit. Вторая GPU не решает этот круг.

**Точно недостающее решение.** Один minimal route с ветвями: (A) pretrained + CPU rules/threshold replay без нового обучения; (B) один fine-tune после data/runtime gates; (C) optional challenger/вторая GPU только при готовой очереди и измеренном reserve. До первой аренды проверяются доступные без GPU документальные/данные/экспортные условия; qualification smoke на конкретной 3090 — отдельная первая оплачиваемая стадия после самостоятельного разрешения, не уже имеющийся предарендный факт. Нужен заранее заданный cutoff новых гипотез и относительный резерв LinQ/финальных материалов без выдумывания часов.

**Закрытие.** Новая отдельная интернет-ветка «как планировать GPU» не нужна: W1-11/15 уже дали сильную базу. После W2-A…G сборщик/автор сводит один маршрут и список deferred работ. Минимальная сохранность — native recovery snapshot до stripping, immutable copy, внешние bytes/hash/load и записанный parent/status; строгий replay/controller предлагается только при доказанной потребности. K001 определяет, какие автоматические изменения должны аннулировать сравнение. Прохождение одного smoke не отменяет отдельный worst-case train/val memory gate. Не разрешать optional runs съесть обязательные evaluation/LinQ/submission reserves.

## Предлагаемая содержательная карта второй волны

Рекомендую **7 целевых Medium-задач**. Это не повтор 16 веток и не отдельный финальный аудит. Каждая получает исходные K-ID, соответствующие W1 и обязана принести новое первичное сведение/контрпример либо точно локализовать невозможность проверки. K006/K011 закрываются интеграцией результатов назначенным сборщиком, а не созданием двух синтетических поисковых обзоров.

| Задача | K-ID | Новое содержание и конкретный выход | Граница завершения |
|---|---|---|---|
| **W2-A. Native trainer mutation/recovery** | K001, K011 | Независимый source walk OOM/backend-memory/NaN/accumulation/native resume и callback lifecycle выбранного Ultralytics; разрешённая fail/fork policy, actual-progress schema, минимальный будущий recovery/negative drill | Точные hooks/доступные switches или честное отсутствие; никакого выполненного GPU drill. Не повторять весь W1-14 и не проектировать новую платформу |
| **W2-B. Один совместимый training/export stack** | K002, K001 | Requirements/release/API matrix для YOLO baseline и одного challenger; explicit exporter/head/mode, dependencies, conservative fallback stack, роль training vs export env | Source-backed manifests со статусами; lock/import/fit/export остаются unrun, если сборки не было. Не подбирать newest image ради newest |
| **W2-C. Evidence для detector выбора + точные веса** | K003, K004 | Одна baseline/challenger пара и permissive fallback: сравнимость родных recipes, small-object/occlusion/domain evidence и ограничивающие ablation; grant/provenance/asset availability retained checkpoint | Либо уточнённый приоритет, либо понижение до условной инженерной гипотезы. Не добавлять длинный каталог свежих моделей, не объявлять target winner |
| **W2-D. Минимальные данные и causal acceptance corpus** | K005, K006, K007, K011 | Проверить 1–2 адресных первичных data leads из соседних reports; exact labels/rights/groups/FPS/negative exposure; выбрать возможный первый scope, минимальную доразметку, event-ledger/phase fixtures | Readiness и `missing` таблица, без фиктивно полученных team data. Не повторять полный datasets/behavioral research; не требовать сотен независимых событий до первого feasibility |
| **W2-E. Один concrete specialist вместо архитектурного обещания** | K008, K003, K009 | Official initialization/config/weights/license для одного crop verifier и ограниченного causal temporal route либо обоснованный отказ от второй ветви; train/export/state contract, proposal failure conditions | 1–2 конкретные карточки или architecture-only/deferred. Не обещать generic pretraining распознавание нарушения, не предлагать обязательный ensemble/KD |
| **W2-F. Узкий LinQ smoke/fallback и multi-model obligations** | K009, K002, K008 | Текущие публичные первичные examples/docs и critical manual pages; точная historical fallback identity; графовые/CPU/state/residency вопросы actual SDK и probe sequence для всех retained neural nodes | Чёткая граница public vs delivered vs run. Без SDK не обещать close target compatibility. Без полноценной новой программы quantization |
| **W2-G. Vast release/runbook и disputed charges** | K010, K011 | Выбранный CLI artifact: release vs HEAD copy/lifecycle semantics; state-by-state charges с первичными locators, трансфер на Windows, обновляемый offer/ledger contract | Документальные вопросы закрыты или сформулированы узко; account invoice/платёж/реальная аренда остаются внешними gates. Никаких расходов/удалений |

Практические зависимости: W2-A/B/C/F могут независимо сузить допустимый baseline; W2-D задаёт, какой из этих кандидатов вообще имеет data input; W2-E не должен задерживать baseline и может завершиться решением `defer`. W2-G не выбирает модель. После их результатов K006 получает единый split-role contract, K011 — единую очередь и ветвь без обучения. Количество W2 задач допустимо скорректировать, если новые материалы устранят необходимость отдельной specialist ветви; содержательная пустота не заполняется обзором ради числа.

## Что нельзя обещать закрыть новым публичным поиском

| Неизвестное | Что уже есть | Проверка / ответственный следующий шаг |
|---|---|---|
| Реальные данные команды, их права, independent camera/incident groups и continuous negative exposure | Требования и адресные leads, K005 | Инвентаризация фактически переданных assets владельцем данных; manifests и label QA. Если доступа нет — точный Q, а не бесконечный поиск идеального датасета |
| Ресурсы и release конкретного LinQ, operator/shape/IR/precision support, neural CPU interpretation | Исторический manual/vendor docs и полный контракт W1-16, K009 | Владелец выданного SDK/сервера получает версии, запускает разрешённый single-model probe, уточняет трактовку CPU у постановщика; никакие внешние сообщения этой критикой не разрешены |
| Fit/throughput одной 3090, joint contention двух, длительность recipe | Нативные configs и правильная memory model, K001/K002/K011 | После отдельного поручения — representative train+val+save/reload smoke на конкретном host; затем measured baseline. Значения до проверки `unknown` |
| Реальное recovery/RPO/RTO и результат interruption | Статические checkpoint/copy findings W1-13/14 и K001 | Минимальный controlled drill с полученной вне хоста копией. Native approximate recovery и exact continuation оценивать раздельно |
| Полный invoice/FX/tax/autobilling, availability/условия будущего оффера | Timestamped public offers и формула W1-12, K010 | Владелец аккаунта проверяет Charges/Invoice/лимит и повторяет offer query непосредственно перед покупкой; сохранённая цена не является разрешением тратить |
| Заводское event quality, gain от challenger/augmentation/verifier, эффект 1 FPS | Сильная спецификация и проверяемые гипотезы, K004/K007/K008 | Будущая causal evaluation на независимых episodes/negative exposure, затем full LinQ path. Результаты собственной системы в текущем исследовании отсутствуют |

## Как дополнять этот файл после второй волны

У каждого K-ID сохранить исходный текст и добавить: `статус`, W2-файл/локатор, новое первичное evidence, изменившееся решение, остаточный Q/практический gate. Подходящие статусы: **закрыто документально; уточнено; опровергнуто; противоречие; остаётся открытым; потеряло значение после сужения scope**. Например, найденный правильный callback закрывает часть K001, но не превращает неисполненный recovery drill в пройденный; найденный manual не закрывает actual LinQ compatibility. Это обработка второй волны внутри согласованной сборки, не отдельная финальная проверяющая роль.

---

## Результаты второй волны и интеграции сборщика — 2026-10-23

Исходный текст K001–K011 выше сохранён. Этот раздел добавлен High-сборщиком после завершения всех семи W2; новая сеть, третья волна, обучение/экспорт/аренда/LinQ или финальный аудитор не выполнялись. Evidence/ID-normalization находятся в [SOURCES.md](SOURCES.md), [RAW_FACTS.md](RAW_FACTS.md) и [_WORK/ID_MAP.md](_WORK/ID_MAP.md). «Закрыто документально» означает разрешение конкретной source/методологической проблемы, **не выполненный runtime gate**. Все E001–E012 — proposed / UNRUN, остатки локализованы Q001–Q024 в [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

### K001 — Закрыто документально; runtime guard/наблюдаемость открыты

**Новое evidence:** [_WORK/W2_A.md](_WORK/W2_A.md), «Первичные свидетельства», trigger→mutation таблица, stock switches/guard и actual progress; W2-B «Конкретные несовместимости». Повторно прочитанный pinned Ultralytics source подтверждает first-start-epoch OOM retry с сохранением уже изменённого optimizer, NaN replay, first-epoch continuation и отдельные EMA/half save repairs. Reserved `optimizer_step`/`on_before_zero_grad` callbacks stock loop не dispatch; нет установленного stock disable flag. Accumulation pending gradients не serialized, epoch boundary не lossless. PyTorch fused step hook не доказывает applied update.

**Изменившееся решение:** F010/F015/F153–F159: любое native OOM/NaN/repair исключает immutable comparable trial; salvage/approximate resume отдельный child/status с lineage. Applied updates unknown остаются null, observability gaps блокируют comparable success. Минимальный pinned guard+append-only log+pre-strip snapshot/receipt предложен; exact replay controller deferred. D-FINE stage reload заранее recipe, unexpected nonfinite также invalid trial.

**Остаток/owner/gate:** Q009/Q011/Q012, R3 и independent verifierR2; E004/E005. Adapter/AMP observer/negative drill/RPO ещё не выполнены. Исходная критика подтверждена, не отменена finite checkpoint или exit0.

### K002 — Закрыто документально по одному выбранному envelope; installed/tested stack открыт

**Новое evidence:** [_WORK/W2_B.md](_WORK/W2_B.md), manifests A/B, native requirements/API/metadata и экспортные отрицательные находки. Official Torch2.5.1/vision0.20.1 pair, Python3.11.9; isolated project train cu124 и CPU export, NumPy1.26.4/ONNX1.17.0/ORT1.20.1/OpenCV4.10.0.84; conservative2.4.1/vision0.19.1 alternative. Native D-FINE `--simplify` store_true/defaultTrue не отключается отсутствием flag; предложен static1 explicit-legacy adapter. Torch2.6 load default change и transitive gaps локализованы.

**Решение:** F007/F160–F166 заменяют W1 latest-image candidate как активное предложение. YOLO e2e/dense и D-FINE deployed head — разные exact bundles; train/export env не являются выданным SDK. Не смешивать pins в единый «tested Docker».

**Остаток:** Q006/Q008/Q009/Q018/Q019, R3/R4; E003/E004. Actual resolver/lock/import/checkpoint load/export/ORT/parity/24GB/device gate UNRUN. W1 image metadata не опровергнута, но не evidence совместимости.

### K003 — Частично закрыто/уточнено; отдельные права и actual artifact gates открыты

**Новое evidence:** [_WORK/W2_C.md](_WORK/W2_C.md), exact asset/license table+HEAD и upstream terms; [_WORK/W2_E.md](_WORK/W2_E.md), pinned specialist modelcard/README license contradiction. YOLO explicit code/models/docs AGPL/Enterprise, actual model HEAD и metadata digest; author HF D-FINE-M exact repository Apache designation+LFS hash сильнее project-level GitHub claim. Native HGNetv2-B2 init имеет отдельный unresolved scope; YOLOX release/codeApache не individual weight grant. Specialist exact modelcardApache против project ImageNet weight notice unresolved. Objects365 lineage и upstream terms не растянуты в самостоятельный запрет trained weights.

**Решение:** F005/F006/F014: выбирается D-FINE-M HF exact asset для условного C, без утверждения byte identity GitHub/HF. YOLOX лишь условный fallback, timmV не включён в A. Форма AGPL поставки должна быть принята командой; отсутствие отдельного LICENSE не автоматически запрет, code grant не автоматически clearance всех weights/data.

**Остаток:** Q002/Q008/Q017, R5/license owner+R3; accepted use/notices+actual model byte hash/trusted load/init chain. Никакие большие weights не скачаны; HEAD не tensor inspection. K003 нельзя целиком объявить закрытым.

### K004 — Закрыто документально через downgrade; target ranking открыт

**Новое evidence:** [_WORK/W2_C.md](_WORK/W2_C.md), pairwise table/APsmall/control caveats. YOLO26s released lineage O365v1→COCO, не COCO-only; denseAPsmall29.5 отдельно от e2eAP47.8. D-FINE-M COCO52.3/33.2 против O365→COCO55.1/37.9, capacity/recipes/exposure различны. APsmall annotation area не actual resized visibility. Qualitative X occlusion gallery не controlled M target result; STAL counterexample не universal improvement.

**Решение:** F005/F167–F172: D-FINE-M условный engineering challenger для остаточной visible localization error, после label/visibility/input-pixel audit и одной spatial baseline alternative. Published COCO таблицы не priority accuracy ranking. Дополнительная RF-DETR ветка для закрытия вопроса не понадобилась.

**Остаток:** Q010/Q022, R2/R3; E007 при reserve. Target superiority, одинаковая короткая adaptation cost/convergence и converted quality unknown. Отсутствие измерения честно сохранено.

### K005 — Уточнено конкретным obtaining/reannotation path; training input остаётся внешним gate

**Новое evidence:** [_WORK/W2_D.md](_WORK/W2_D.md), primary URFD/CAUCAFall records/readiness. Exact URFD pair HEAD200 и реально полученный fall01CSV160rows/0…5305ms; NC-use/camera lineage/labels ограничены. CAUCAFallv5 CC-BY4.0 и fall/no-fall segmentation по card, но motion-triggered DVR не continuous negative hours. Видео не декодированы, event labels/team assets отсутствуют.

**Решение:** F003/F173–F181: A только observable lying-state при принятом use и пригодном frontend/media, иначе team-video zone fallback после получения разрешённого asset; не claim «fall/unconsciousness». Минимум positive+contrast negative для feasibility, затем rearm/two-actor episodes при наличии; не требовать ложной статистической квоты до первого smoke. Object fine-tune и event-eval packages разделены.

**Остаток:** Q001–Q004, R1 с reviewerR2/R5; E002/E006. Actual files/rights/PTS/labels/independent background/positives не появляются от public search. Не выполненный DEV replay не заявлен PASS.

### K006 — Закрыто интеграционным решением; выбран один data-role contract

**Основание и решение:** F004 и подробный F177 на основе W2-D readiness, W1-09/11. Обязательные роли **TRAIN / DEV / LOCKBOX**; CAL/TUNE/CHECK/SELECT не суммируются в семь subsets. Текущая exact pair только DEV feasibility, TRAIN пуст и independent LOCKBOX отсутствует. Optional grouped CV только внутри development, если хватает групп; folds повторяют всю fit/calibration/selection procedure.

**Decision→allowed data→after-view:** gradients TRAIN; все threshold/checkpoint/recipe/crop/rule/export fixes DEV; optional CAL внутри DEV; optional SELECT не более двух заранее frozen whole pipelines и никакого knob tuning; просмотр для изменения параметров поглощает SELECT в DEV. Один final frozen bundle→непросмотренный LOCKBOX. Любая tuning реакция на lockbox делает его development; новые independent claims требуют новых групп. Refit TRAIN+DEV создаёт новый artifact ID и verification status, старый pass другого checkpoint не переносится. Таблица с числом вариантов и after-view status находится F004.

**Остаток:** Q004/Q022 у R1/R2 — фактическое наличие независимых групп, не нерешённая интеграция. При недостатке positives/background честный результат feasibility/raw counts/N/A; не выдавать CI кадрами за независимость. Эта критика закрыта выбором протокола, без новой сетевой задачи.

### K007 — Закрыто спецификацией короткого acceptance corpus; исполнение открыто

**Новое evidence:** [_WORK/W2_D.md](_WORK/W2_D.md), «Малый synthetic event-ledger acceptance corpus» и W2-D-E01. C01–C10 покрывают timely/deadlineboundary/late/duplicate/twoactors/rearm/IDsplit/IDmerge/unknown/short-between-samples/EOFcensor; inclusive deadline, half-open interval, maximum timely cardinality→delay→lexical tie. Константы fixturev0 искусственные, не industrial dwell/deadline.

**Решение:** F008/F019/F178–F180; E001 exact oracle/matcher/FSM acceptance до tuning, затем E002 real oracle/frontend phase replay с frame/PTS/freshness, после него отдельный LinQ wallclock E003. GT разных фаз одного эпизода не independent groups, unknown не negative exposure. Cached replay не deadline benchmark.

**Остаток:** Q003/Q005/Q021, R2/R1/R4. Fixture runner/media/labels/phase execution/recall/FP-hour unknown; synthetic spec не model evidence и не выполненные тесты.

### K008 — Закрыто документально в ограниченном объёме; neural temporal отложен

**Новое evidence:** [_WORK/W2_E.md](_WORK/W2_E.md), exact crop card/trainer/head/export/state и TSM countercheck. Единственный conditional init timm `mobilenetv3_small_100.lamb_in1k` exact HF revision+model.safetensors hash metadata, codev1.0.22; будущая supervised3-head PPE crop schema, не готовая violation model. Native exporter dynamicbatch/default trap отмечен. Обычный TSM shift читаетt+1; online MobileNetV2 Jester27 другой checkpoint/state contract, без target ability/reset guarantee.

**Решение:** F014/F182–F188: V только при visible wrong-class error+proposal ceiling/labels/license/device gates; baseline от него не зависит. Neural temporal deferred, pose/ReID/KD/ensemble не скрытые обязательные стадии A. CPU FSM остаётся первый route.

**Остаток:** Q010/Q017/Q020/Q021, R2/R3/R4/R5; E011 только после observed reason/reserve. Exact specialist use conflict остаётся K003; actual train/export/target quality UNRUN. Закрытие не означает готовую модель phone-use/fall.

### K009 — Уточнена граница публичного evidence; actual target gate остаётся открытым

**Новое evidence:** [_WORK/W2_F.md](_WORK/W2_F.md), public support table/historical identity/probesP0–P8. Manual worked example — **ResNet50 classification**, `yolo5s` только tested-name; currenttech yolo8/yolo11 не exact variants/heads/opsets. PDF bytes/visual не получены, extract не copy-paste verified. Одной программы/sync/STAGING недостаточно для residency/concurrency. Буквального neuralCPU ban не найдено, нужен отдельный policy answer+placement trace.

**Решение:** F013/F189–F195: infrastructure smoke из actually delivered vendor sample, при manual-only диагностический ResNet50; exact detection fallback **unknown**, YOLO26/YOLOX device-unverified. Каждый retained runtime neuralnode получает собственный graph/placement/parity/state/load/burst gate; teacher-only отсутствует online лишь при реальном исключении.

**Остаток:** Q006/Q007/Q018–Q021, R4/R5; E003. ВыданныеSDK/SKU/access/ops/IR/precision/backend/CPUinterpretation/capacity/performance не решаются публичным именем family; ни одного target run нет. Public documentary boundary закрыта уточнением, а не объявлением compatibilityPASS.

### K010 — Закрыто документально по actual CLI artifact/runbook; billing contradiction и account остаются

**Новое evidence:** [_WORK/W2_G.md](_WORK/W2_G.md), actual wheel bytes/entrypoint/source comparison, command table/state table/OpenAPI charges. Выбран releasev1.9.0 wheel SHA256 `dfa2349701a2302bdf2ea902bc0548609870da2888167883ab32eec954eed98b`. **Legacy shell=True claim исправлен для actual wheel:** modularcopy subprocess argv list, но unchecked returncode и StrictHostKeyChecking=no остались. Destroy y/N prompt, CLI search default rentedfalse отсутствует, explicitlocal dispatch отличается от unprefixed path. CurrentFAQ storage loading против currentBilling/Manage nocharge — оставленный current-current conflict; current offline exemption versus legacyoffline claim различены.

**Решение:** F011/F012/F196–F201: pinned executable source contract, Linux/WSL/rsync caveats, explicit filters, separate poll; independent immutable bytes/hash/trusted-load receipt перед будущим destroy. Charges type/source/gpu/disk/bwd/bwu с allpages/UTC, invoices не usage. Wholeoffer/disk/units double-count исправления сохранены; старые quotes только timestamped observation.

**Остаток:** Q012–Q016, R3/account owner/verifierR2; E005/E012. Actual installation/offer/rates/byte divisor/loading/Charges/invoice/autobilling/taxFX не проверены и расходов нет. CLI success не архив, stop не бесплатное завершение, destroyinstance не deletevolume.

### K011 — Закрыто интеграционным маршрутом и cutoff; execution inputs остаются gates с owners

**Выбранное решение:** F003/F017, не union всех branch experiments. **A** pretrained+CPU causal rules/threshold replay без обучения; **B** один fine-tune только после data/rights/env/export/runtime gates и отдельно разрешённой actual3090 qualification; **C** один optional challenger/втораяGPU только с readywork и измеренным оставшимся reserve. При незакрытых gates сужениеscope/feasibility, не новый sweep. Native pre-strip snapshot+immutable outside receipt первый минимум; exact replay/controller/neuraltemporal/KD/ensembles/ASHA deferred.

**Предлагаемые пять owners:** R1data/labels/rights, R2evaluation/FSM/reviewer/lockbox, R3baseline/training/Vast/artifacts, R4LinQ/runtime, R5product/submission/coordinator. Это не фактически назначенные люди. НаW2finish23.10 20:50:48MSK осталось37ч09м12с до25.10 10:00, не45ч. К24.10 11:00 один end-to-end feasibility либо конкретный blocker+scope reduction; после11:00 expansion лишь при finished incumbent/readyinput/measuredreserve. К24.10 18:00 freeze scenario/models/head/rules/sampling/evaluator, прекращение optionalnewruns; далее mandatory parity/LinQ/evaluation/archive/UI/submission и только blockingfix с новымID/повтором affectedgate. Ни один traininghour estimate не выдуман.

**Нециркулярная аренда:** до rental документальные/data/localCPU-export checks и archive readiness; measurement3090fit — отдельно разрешённая первая paid qualification, затем heavytrain. Optionalrun не начинается при unknown/незащищённом mandatory LinQ/evaluation/product/submission/recovery reserve. Работа, не успевающая доfreeze, не запускается; незавершённоеoptional к18:00 не получает бесконечных «ещё эпох».

**Остатки уже локализованы:** Q001–Q024 с proposedowners и observable closure, особенно Q009hardware/Q013spend/Q022readywork/Q023actualroleassignment. Они не отменяют закрытое интеграционное решение. Никакой дополнительной интернет-ветки планирования/финального аудитора не создано.
