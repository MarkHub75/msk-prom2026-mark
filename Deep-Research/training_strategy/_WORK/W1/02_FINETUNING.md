# W1-02 — Предобучение, head-only/full fine-tuning, freeze и BatchNorm

Проверено 2026-10-23, 03:40–03:46 UTC / 06:40–06:46 Europe/Moscow. Это время исследования, не расписание соревнования. Роль: исследователь первой волны; контекст mosprom-research-v1. Прочитаны входные Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, задание W1-02 и сохранённый W1/01_BASELINE.md. Последний используется как внутренняя передача baseline, а не независимый первоисточник.

## Решение команды

**Нет основания заранее назначить head-only универсальным победителем для малого CCTV-набора.** TFA даёт сильное detection-specific основание проверить обучение последних предикторов на сбалансированной малой разметке после обучения детектора на базовых классах. Оно не доказывает, что любой YOLO с замороженным backbone получит тот же эффект. Полное обучение и частичная адаптация должны сравниваться на одном checkpoint, одинаковой разметке и независимой проверке, с явно зафиксированным поведением BN. При этом «число обучаемых весов» и «какие статистики меняются» — разные характеристики режима.

Для короткого исследовательского цикла практически полезны три кандидата: неизменённые веса как reference; ограниченный fine-tuning с проверенной маской; полный fine-tuning из тех же исходных весов. Последовательность freeze→unfreeze — отдельный кандидат, требующий отдельного бюджета и контроля, а не автоматически лучший рецепт. Выбор модели сначала ограничивается нужными outputs и возможным целевым graph; обучение не подтверждает исполнение на LinQ.

Ни обучение, ни модельный benchmark, ни export здесь не запускались. Выполнены веб-поиск, открытие материалов, HTTP-чтение закреплённых исходников и metadata API. Скорость/память RTX 4070, качество на target CCTV и поддержка LinQ не установлены.

## Источники и происхождение

Все источники ниже открыты 2026-10-23; локаторы функций надёжнее номеров строк, поскольку web-parser удаляет пустые строки.

| ID | Первичный источник, версия/дата | Локатор и статус | Поддерживает |
|---|---|---|---|
| W1-02-S01 | Wang, Huang, Gonzalez, Darrell, Yu. [Frustratingly Simple Few-Shot Object Detection, PMLR 119](https://proceedings.mlr.press/v119/wang20j.html), ICML 13–18 July 2020; открытый [arXiv PDF](https://arxiv.org/pdf/2003.06957), полученная версия маркирована v1, 16 March 2020 | §3.1, §4 implementation, Table 3, §4.2, Fig.5; PDF прочитан по релевантным разделам. Числа ниже относятся к этому PDF, не молча к финальному PMLR PDF | F01–F02 |
| W1-02-S02 | Авторский [FsDet](https://github.com/ucbdrive/few-shot-object-detection), commit `148a039af7abce9eff59d5cdece296ad1d2b8aa0`, metadata committer date `2021-10-27T16:53:42Z` | [10-shot COCO config](https://raw.githubusercontent.com/ucbdrive/few-shot-object-detection/148a039af7abce9eff59d5cdece296ad1d2b8aa0/configs/COCO-detection/faster_rcnn_R_101_FPN_ft_all_10shot.yaml), [base config](https://raw.githubusercontent.com/ucbdrive/few-shot-object-detection/148a039af7abce9eff59d5cdece296ad1d2b8aa0/configs/Base-RCNN-FPN.yaml), [GeneralizedRCNN.__init__](https://raw.githubusercontent.com/ucbdrive/few-shot-object-detection/148a039af7abce9eff59d5cdece296ad1d2b8aa0/fsdet/modeling/meta_arch/rcnn.py). Чтение кода, не запуск | F03 |
| W1-02-S03 | He, Girshick, Dollár. [Rethinking ImageNet Pre-training](https://arxiv.org/abs/1811.08883), arXiv v1 21 November 2018, [PDF](https://arxiv.org/pdf/1811.08883) | §5.2, Fig.7–8, §6. Это технический отчёт v1; не приписывать его буквально поздней ICCV-редакции | F04 |
| W1-02-S04 | Qiao et al. [DeFRCN](https://arxiv.org/abs/2108.09017), submitted 20 August 2021, [открытый PDF](https://arxiv.org/pdf/2108.09017), ICCV 2021 | §3.3.1, §4 implementation, Table 4, Fig.4. Прочитаны релевантные разделы; benchmark авторов, не наш | F05 |
| W1-02-S05 | Ultralytics [`trainer.py`](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py), commit `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, committer date `2026-10-22T20:27:18Z`; [`__init__.py`](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/__init__.py) задаёт `8.4.184` | BaseTrainer._setup_train, _model_train, _do_train, build_optimizer. Открыто web и HTTP; только code observation | F06–F08 |
| W1-02-S06 | Ultralytics [`nn/tasks.py`](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/tasks.py), тот же commit/version | BaseModel.load, BaseModel._remap_cls_by_names; только code observation | F09 |
| W1-02-S07 | Ultralytics [`models/yolo/detect/train.py`](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/models/yolo/detect/train.py), тот же commit/version | DetectionTrainer.get_model; только code observation | F10 |
| W1-02-S08 | PyTorch [BatchNorm2d, versioned docs 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html), дата публикации страницы не установлена | `affine`, `track_running_stats`, train/eval statistics. `stable` при чтении перенаправил на 2.14; это не установленная версия локального PyTorch | F11 |
| W1-02-S09 | Ultralytics [Fine-Tuning Guide](https://docs.ultralytics.com/guides/finetuning-guide), живая документация, дата страницы не установлена | Weight transfer, freezing, two-stage fine-tuning, forgetting. Прочитано как vendor guidance, не как контролируемое исследование | F12 |

Даты commit получены HTTP-запросами GitHub API `repos/{owner}/{repo}/commits/{ref}`. Web-tool эти API URL не открыл; прямой HTTP открыл. Не создавать видимость, что README гарантирует совместимость сегодняшнего Detectron2 с FsDet 2021 года.

## Подробные факты

### Detection evidence: head-only не равно заморозить произвольный backbone

**W1-02-F01 [PAPER-MEASUREMENT; S01 §3.1, §4, Table 3].** TFA: Faster R-CNN, ResNet-101+FPN; сначала base detector, затем box classifier/regressor на balanced base+novel K-shot instances, остальные feature-компоненты фиксированы. SGD batch16, momentum0.9, decay0.0001; LR0.02→0.001. COCO novel AP при 10/30 shots: full fine-tuning авторской реализации 9.2/12.5; TFA fc 10.0/13.4, cosine 10.0/13.7. Это objects, не независимые CCTV clips. Table3 — старый протокол; не смешивать с generalized Fig.5. В изученном фрагменте точные GPU, wall time и правило выбора checkpoint для этих строк не установлены.

**W1-02-F02 [PAPER-PROTOCOL; S01 §4.2, Fig.5].** Revised protocol измеряет base и novel; COCO Fig.5 усредняет 10 random samples с 95% CI. Балансировка включает старые классы. Поэтому результат не подтверждает сохранение всех старых знаний при обучении только новых классов; он также не даёт единого image budget для нашего кейса.

**W1-02-F03 [CODE; S02].** COCO all_10shot config явно задаёт backbone FREEZE, proposal generator FREEZE и ROI_HEADS.FREEZE_FEAT=True; GeneralizedRCNN.__init__ ставит requires_grad=False соответственно backbone, proposal_generator и roi_heads.box_head. Это оставляет обучение predictor, а не всего RoI feature head. Config: 80 classes, CosineSimOutputLayers, batch16, LR0.001, MAX_ITER160000, STEPS144000, checkpoint period10000; base config train min-size 640…800. Config содержит путь к `model_reset_combine.pth`, не просто произвольный COCO checkpoint. Историческая конфигурация не доказывает быстрое завершение на нашей машине. Поведение normalization всего дерева зависимостей этим чтением не установлено.

**W1-02-F04 [PAPER-MEASUREMENT; S03 §5.2, Fig.7–8].** В Mask R-CNN R50-FPN+GroupNorm на 10k COCO images pretrained достиг 26.0 bbox AP при 60k iterations, scratch 25.9 при 220k; validation val2017, hyperparameters подобраны для pretrained и перенесены на scratch. При 1k images: текст даёт 9.9 против 3.5 AP; caption Fig.8 — 3.4 вместо 3.5, небольшое внутреннее расхождение сохраняем. Даже отдельный поиск scratch hyperparameters дал 5.4. Это показывает зависимость от data/compute и отсутствие универсального запрета scratch; не обосновывает scratch при нашем неизвестном малом наборе. На этой ветке classification pretraining исследовано как исторический контроль; лучший конкретный detection checkpoint для PPE не определён.

**W1-02-F05 [PAPER/ABLATION; S04 §3.3.1, §4, Table4/Fig4].** DeFRCN обучает больше компонент Faster R-CNN, регулируя gradient flow, вместо жёсткого ограничения TFA. ResNet-101 ImageNet pretrained, SGD batch16, LR0.02 base/0.01 novel, momentum0.9, decay5e-5; RPN gradient coefficient0, RCNN0.75 base/0.01 novel. COCO Table4 plain FRCN novel AP10/30-shot 7.9/12.2; добавление GDL только в novel stage 15.2/19.0. Дополнительный PCB действует в inference. Это архитектурная абляция, не чистый спор «все веса против head при прочих равных», и не готовая YOLO-функция. Практический смысл: ограниченная адаптация backbone и head-only — разные проверяемые кандидаты; заморозка сама по себе не является законом few-shot detection.

### Фактическое поведение Ultralytics 8.4.184

**W1-02-F06 [CODE; S05 _setup_train, freeze block].** int `freeze=N` превращается в range(N); список используется напрямую; имена получают префикс `model.` и суффикс `.`. `.dfl` включён в always-freeze. Совпавшие параметры получают requires_grad=False; floating параметры вне маски, ранее False, получают True. Поэтому ручная предварительная заморозка может быть отменена trainer. Именованные подмодули допустимы через список, но соответствие архитектуре необходимо проверять.

**W1-02-F07 [CODE; S05 _model_train, _do_train].** В начале эпохи _model_train вызывает model.train(), затем переводит совпавшие по freeze names nn.BatchNorm2d в eval(). Следовательно, в этой версии обычная freeze-маска также фиксирует running statistics соответствующих BatchNorm2d. Это не утверждение обо всех версиях, SyncBatchNorm/custom normalization или пользовательских callbacks.

**W1-02-F08 [CODE; S05 build_optimizer].** `optimizer=auto` выбирает optimizer/LR и явно игнорирует заданный lr0; порог iterations участвует в выборе. Для сравнения freeze/full надо зафиксировать фактические optimizer, LR и budget либо признать сравнение полных recipes. Автоматически одинаковый CLI lr0 не гарантирует одинаковый optimizer setup.

**W1-02-F09 [CODE; S06 BaseModel.load/_remap_cls_by_names].** Loader пересекает совместимые tensors; отдельно обрабатывает ширину hidden cls-веток при совместимых head inputs. Class-logit rows remap по strip/lower names, включая одинаковый nc с другим порядком; placeholder names исключены, несовместимая trailing shape пропускается. Изменение class count не означает сброс всей head. Предупреждается использование fused inference weights вместо unfused training checkpoint. Переименование класса по строке не проверяет совпадение его смысла.

**W1-02-F10 [CODE; S07 DetectionTrainer.get_model].** Trainer строит DetectionModel с dataset nc/channels, устанавливает model names через set_model_names_for_load, затем вызывает model.load(weights). Проверять надо именно итоговую модель trainer после настройки, поскольку объект до train может иметь другой class contract.

**W1-02-F11 [DOCS; S08].** BatchNorm2d имеет learnable affine gamma/beta и отдельно running estimates. При track_running_stats=True они обновляются во время train и используются в eval; при False batch statistics используются и в eval. Поэтому запрет градиента affine параметрам сам по себе не описывает режим статистик. Документация не устанавливает, какие statistics оптимальны для малой target CCTV-выборки.

**W1-02-F12 [VENDOR-GUIDANCE; S09].** Живой guide описывает freeze и последовательное обучение, но его советы о малом наборе не являются независимой абляцией. В нём `freeze=10` для YOLO26 оставляет последний backbone block trainable; полный backbone — `freeze=11`. Эти индексы нельзя переносить на другие YAML. Фраза guide об «only reliable» предотвращении forgetting через смешивание данных слишком сильна для общего вывода; наша рекомендация — измерять сохранение нужных старых классов, независимо от выбранного метода.

## Условная стратегия [INFERENCE/PROPOSED из F01–F12]

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

## W1-02-E01 — head-only/limited freeze против full из одного checkpoint

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

## W1-02-E02 — различить влияние BN и обновления feature weights

**Статус:** PROPOSED. Не обязателен до E01; нужен при малом batch, подозрении на drift статистик или различии результата train/eval. **Входы:** рабочий E01 и возможность менять trainer с логами. **Контроль:** одна trainable-weight mask, один initialization/data order и optimizer; меняется только политика BatchNorm2d running statistics: fixed source stats против target updates. Affine parameters и остальные normalization types фиксируются одинаково. В native Ultralytics freeze fixed-stats поведение уже встроено для совпавших BN (F07); второй arm требует явной проверенной модификации, готового штатного флага эта ветка не установила.

**Действия:** снять running_mean/var/num_batches_tracked до/после; убедиться в неизменности affine/weight mask; выполнить ограниченную paired adaptation; оценить оба checkpoint в одинаковом eval и на одинаковых inputs. **Метрики:** изменение BN buffers, целевые per-class/per-camera quality и старые условия, batch composition/размер; отдельно воспроизводимость predictions. **Артефакты:** trainer diff, normalization inventory, buffer deltas, configs, predictions. **Исходы:** target updates помогают на независимых target groups без неприемлемого ущерба — кандидат; ухудшают/нестабильны — fixed stats; различия малы — не усложнять режим. **Stop rule:** случайно изменилась mask/augmentation либо BN фактически работает иначе ожидаемого — comparison invalid. **Предел:** это тест одной реализации и данных; не доказывает общую полезность Adaptive BN, не устанавливает cross-camera перенос и не разрешает использовать assessment video для adaptation.

## Открытые вопросы и передачи

| ID | Предмет неизвестного; что меняет | Как закрыть и приоритет |
|---|---|---|
| W1-02-Q01 | Какой checkpoint/YAML реально выбран и пригоден к обучению: source data/labels, normalization, unfused state, лицензия, class map, export constraints? Это определяет допустимые arms | → model_stack: получить конкретный hash/version и training load smoke test; высокий |
| W1-02-Q02 | Сколько независимых целевых сцен и полных labels; какие старые классы обязательны? Без этого неизвестны риск overfit и нужный retention test | → datasets/evaluation/постановщик: ontology + manifests + coverage audit; высокий |
| W1-02-Q03 | Поддерживает ли фактический trainer наш selector, row remap и нужную BN политику? Найдено для 8.4.184, не произвольной установленной версии | → model_stack: pin package/commit и E01 setup/update audit; высокий |
| W1-02-Q04 | Какая точная mask оптимальна и нужен ли freeze→unfreeze? Papers не отвечают за target CCTV | E01; staged arm только после рабочей пары B/C, с суммарным update/time budget; средний |
| W1-02-Q05 | Изменение nc/head совместимо с целевым LinQ compiler/runtime и postprocessing? | → linq_platform/model_stack: actual graph/input/output compile + execution; высокий |
| W1-02-Q06 | Нужна ли адаптация BN и достаточно ли batch diversity для устойчивых target statistics? | E02, только если диагностическая причина остаётся после E01; средний |

**→ model_stack:** F06/F09/F10: нельзя считать freeze настроенным до trainer setup. Нужны actual trainable mask, head-row transfer log, обе cls/box/one-to-one ветки при их наличии, normalization inventory. Не копировать `freeze=10/23` из другого YAML. Сохранять training checkpoint отдельно от fused inference artifact.

**→ datasets/evaluation:** F01/F02: K-shot — число objects на класс, а не универсальное количество images; проверять base/novel retention и diversity. Наш выбор между full и limited требует одних и тех же исправленных annotations и независимого assessment. Partial-label handling — соседняя W1-03, автоматически background не назначать.

**→ linq_platform/video_architecture:** freeze обычно меняет обучение, а не удаляет inference layers. Не ожидать сокращения graph/latency от меньшего числа trainable parameters. Новый nc/class mapping влияет на outputs; любой выбранный artifact снова проверяется в фактическом целевом runtime. Поддержка graph ни одним paper этой ветки не установлена.

**→ violation_methods:** E01 исправляет object representation/predictor; если ошибки сохраняются при oracle objects из W1-01-E02, очередной режим fine-tuning не решает установленную downstream причину.

## Ограничения доступа и завершения

PMLR PDF не открылся через web-tool: `Content length is too large: 15467493`; запасной arXiv PDF открыт. Локальная попытка читать PDF Python pypdf не выполнена из-за `ModuleNotFoundError`; пакет не устанавливался, источник затем прочитан web-tool. CVF ICCV2019 HTML вернул HTTP403; поэтому S03 явно привязан к arXiv v1. Один угаданный путь FsDet `docs/GETTING_STARTED.md` вернул404; он не используется как источник и не означает отсутствия документации.

Ветка завершена как research: установлены различия detection методов и actual implementation, найдены ограничивающая абляция и контрпример универсальному scratch/pretrain тезису, подготовлены controlled E01/E02. Неизвестный лучший target режим оставлен экспериментальным вопросом. Ни универсального LR/epochs, ни гарантии отсутствия forgetting, ни ускорения/LinQ исполнения не заявляется.
