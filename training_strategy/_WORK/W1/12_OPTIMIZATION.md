# W1-12 — Диагностика training и порядок настройки оптимизации

Проверка: 2026-10-23, 07:02–07:07 Europe/Moscow (UTC+3); context_version: mosprom-research-v1. Это время исследования, не время обучения или соревнования. Прочитаны Context-prompt.md, prompt-training-strategy.md, _WORK/PLAN.md, задание W1-12. Учтены внутренние передачи W1-02 и W1-05 по общему commit; их происхождение не считается независимым подтверждением. Первичные источники повторно открыты по нужным функциям. Единственный изменённый артефакт этой ветки — данный файл.

## Решение и граница

До настройки LR нужен последовательный допуск: **семантика и визуальная проверка labels → реально полученный batch → градиенты и фактический optimizer step → намеренное переобучение крошечного набора → сохранение/новая загрузка → независимая validation → изменение recipe**. Это предлагаемый нами диагностический порядок, а не опубликованная гарантия. Низкий mAP сам по себе не различает перепутанные class IDs, пропавшие labels, невозможный масштаб объекта, ошибку evaluation и неудачный LR.

Зафиксированный Ultralytics — пример проверяемой реализации, не заранее выбранный стек для LinQ. Ни один default ниже не является оптимумом для промышленного CCTV. Нет целевых данных/модели/SDK; не выполнены training, benchmark, export, аренда или установка библиотек. Сведения о RTX 4070 ограничены самим названием: её VRAM, конфигурация и скорость здесь не устанавливались.

## Первичные источники

Все S-ID открыты 2026-10-23. Для исходников pin = `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, версия `8.4.184` по передаче W1-02-S05; дата commit повторно получена GitHub API: `2026-10-22T20:27:18Z`. Это дата состояния дерева, не дата появления каждого алгоритма. Даты публикации живых страниц не установлены. Извлечение кода — наблюдение, не выполнение.

| ID | Прямой URL и версия | Локатор / что установлено |
|---|---|---|
| W1-12-S01 | [default.yaml, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/cfg/default.yaml) | Train settings, Hyperparameters; буквальные defaults |
| W1-12-S02 | [trainer.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py) | BaseTrainer._build_train_pipeline; _setup_scheduler; _get_warmup_iterations; _setup_train; _do_train; optimizer_step; build_optimizer; check_resume; resume_training; _load_checkpoint_state; _handle_nan_recovery; final_eval |
| W1-12-S03 | [torch_utils.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/torch_utils.py) | ModelEMA.__init__/update; EarlyStopping.__init__/__call__; strip_optimizer; autocast |
| W1-12-S04 | [dataset.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/dataset.py) | YOLODataset.close_mosaic; DATASET_CACHE_VERSION; cache/verification pipeline |
| W1-12-S05 | [data/utils.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/data/utils.py) | verify_image_label: shape/classes/coordinates, missing/empty/corrupt counters |
| W1-12-S06 | [checks.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/checks.py) | check_amp: surrogate model, skip/failure routes |
| W1-12-S07 | [metrics.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/metrics.py) | Metric.fitness и DetMetrics.fitness |
| W1-12-S08 | [validator.py, pin](https://raw.githubusercontent.com/ultralytics/ultralytics/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/validator.py) | BaseValidator.get_model: training validation получает trainer.ema.ema |
| W1-12-S09 | [Ultralytics Train](https://docs.ultralytics.com/modes/train) | Training Arguments, Resuming Interrupted Trainings, Windows multiprocessing; живая vendor documentation, не pin |
| W1-12-S10 | [PyTorch AMP examples 2.14](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html) | Gradient clipping; Working with Scaled Gradients / Gradient accumulation; stable redirect фактически ведёт на 2.14. Это не версия установленного окружения |
| W1-12-S11 | [PyTorch autograd 2.14](https://docs.pytorch.org/docs/2.14/autograd.html#debugging-and-anomaly-detection) | detect_anomaly(check_nan=True): traceback forward-операции, вызвавшей ошибочный backward; диагностический overhead |
| W1-12-S12 | [Stanford CS231n, Neural Networks Part 3](https://cs231n.github.io/neural-networks-3/) | Before learning: sanity checks; Overfit a tiny subset. Учебное первичное руководство авторов курса; дата страницы не установлена, не detection ablation |
| W1-12-S13 | [GitHub commit metadata API](https://api.github.com/repos/ultralytics/ultralytics/commits/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8) | commit.author.date / commit.committer.date. Web open вернул Internal Error / not accessible via this tool; независимый HTTP Invoke-RestMethod успешно вернул JSON с датой и сообщением Standardize citation admonition titles across docs (#26844) |

Сетевой поиск выполнен по точным optimizer auto/iterations и PyTorch AMP accumulation, затем открыты первичные документы. Доступ raw GitHub успешен и через web open, и через HTTP. Общие советы о tiny overfit взяты как диагностическая мотивация; численные классификационные loss/accuracy из CS231n не переносятся на YOLO detection.

## Версионные факты

### W1-12-F01 — Литеральные defaults: конфигурация, а не рекомендация

Тип: наблюдение по S01. Область — default.yaml закреплённого дерева; фактический запуск может получить model/task overrides и аргументы пользователя.

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

### W1-12-F02 — Actual auto, LR, accumulation: компактная карта реализации

Тип: code observation S02. Локаторы функций указаны в таблице источников. `N=len(train_loader.dataset)`, `B=self.batch_size` (общий batch), `E=self.epochs`:

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

### W1-12-F03 — Какие дополнительные confounds проверить по S02

Тип: вывод из реализации, требующий наблюдения будущего запуска. В auto локальная momentum для построения optimizer=0.9, но warmup для momentum-bearing groups читает args.momentum (default 0.937). AdamW хранит betas, а не поле momentum, поэтому эта ветка warmup не изменяет beta1. При ручном AdamW default lr0 остаётся 0.01, если явно не переопределить: комментарий «Adam/AdamW=1e-3» не меняет YAML.

Для MuSGD код выделяет matrix/conv параметры и может давать части classification-head groups LR×3; одного общего LR из console недостаточно — сохранять все param_groups. Значение batch нельзя подменять одним effective batch: microbatch меняет BN и stochastic transforms, а округление accumulation/warmup, число шагов и decay могут различаться. Простая линейная масштабировка LR по batch не следует автоматически из этого trainer.

### W1-12-F04 — AMP: successful check не означает проверку нашего training

Тип: code observation S06, S03. check_amp использует `yolo26n.pt` и `bus.jpg`, сравнивая FP32/AMP inference boxes: одинаковая shape и allclose с atol=0.5. Это проверка среды на суррогате. Assertion failure выключает AMP; CPU/MPS возвращают False. ConnectionError или AttributeError/ModuleNotFoundError приводят к skip warning и возврату True: статус skipped нельзя пересказать как passed. Возможна одноразовая загрузка surrogate weights.

Тип: code observation S02/S03. `amp=True`/`fp16` запускают check; `False`/`fp32` отключают; `bf16` идёт другим маршрутом, без GradScaler, с проверкой native CUDA bf16 и PyTorch≥1.13 внутри autocast. Поддержку нашей среды надо измерить. AMP — точность обучения, не утверждение о типе конечного LinQ artifact.

Тип: documentation S10. До проверки/clip градиентов их надо unscale; unscale только один раз на optimizer step, после накопления всех microbatches. Масштаб должен оставаться постоянным внутри effective batch; step/update — на его границе. scaler.step может пропустить update при Inf/NaN. Поэтому полезно наблюдать не только loss и scaler scale, но и реальное изменение веса. Нельзя при диагностическом hook второй раз вызывать unscale поверх trainer.

### W1-12-F05 — EMA, checkpoint и early stop

Тип: code observation S03/S08/S07. ModelEMA — eval-копия FP32, параметры без requires_grad; decay=`0.9999*(1-exp(-updates/2000))`, плавающие параметры и buffers обновляются на каждом вызове EMA.update. Training validation получает EMA. Detection fitness — mAP50:95: веса `[0,0,0,1]` для P/R/mAP50/mAP50:95. Это не event recall, редкий класс или число ложных тревог.

EarlyStopping: trainer передаёт cfg patience=100, хотя constructor default=50. `patience=0` отключает. Улучшение — строго `fitness > best_fitness`, с исключением `best_fitness==0`: нулевое плато продолжает обновлять best_epoch. При fitness=None stop=False; possible_stop за epoch до patience; штатный stop при delta≥patience. Встроенный early stop поэтому не заменяет ручной stop rule для нулевого mAP и не гарантирует разумный бюджет короткого кейса.

Тип: code observation S02/S03. EMA.update вызывается после scaler.step/update без отдельной проверки, был ли optimizer update пропущен scaler; EMA.updates поэтому нельзя автоматически считать числом успешных обновлений online weights. В активном checkpoint сохраняются EMA, optimizer, scaler и stopper state; окончательная final_eval strips optimizer у last/best. strip_optimizer заменяет model на EMA, очищает optimizer/scaler/stopper, ставит epoch=-1. **Завершённый best.pt — не полная точка точного resume.** Факт успешной загрузки для inference не равен восстановлению trajectory; при необходимости продолжения нужна отдельно сохранённая пригодная незавершённая точка и manifest.

### W1-12-F06 — close_mosaic и лимиты короткого run

Тип: code observation S04; scheduler boundary — S02. При входе в последние close_mosaic epochs (`epoch >= epochs-close_mosaic`) loader закрывает augmentation и reset. YOLODataset.close_mosaic обнуляет сразу mosaic/copy_paste/mixup/cutmix, перестраивая transforms. `close_mosaic=0` сохраняет исходный режим, а не выключает mosaic. При E≤10 и default close_mosaic=10 условие выполнено с epoch 0: короткая проба не проверяет то же расписание сильных аугментаций, что длинная. Остальные transforms автоматически не обнуляются.

Тип: вывод. Early stopping может завершить training до запланированной финальной фазы без mosaic; факт заданного close_mosaic не доказывает прохождение этой фазы. Сравнение коротких trials требует фиксировать эффективное расписание, а не только args. Полезность конкретной augmentation → W1-05, здесь разобрана механика.

### W1-12-F07 — Resume/OOM/NaN нельзя считать прозрачным продолжением

Тип: code observation S02. check_resume берёт checkpoint args и разрешает только whitelist overrides; optimizer/LR/schedule туда не входят. Для их изменения нужен новый run, иначе warning об ignored overrides. Это существенно при freeze→unfreeze: новый режим надо задавать и проверять сознательно (подробнее W1-02).

В первом epoch single-device trainer может до трёх раз уменьшить batch вдвое после OOM/backend-memory-error и перестроить pipeline; позже и в DDP error пробрасывается. NaN recovery использует last.pt, не может восстановиться в первом epoch, проверяет finite checkpoint и имеет предел трёх последовательных recovery. Следовательно, наличие завершившегося процесса не заменяет осмотр log: фактические batch/перезапуски могли отличаться от плана. Ручной диагностический stop на первом неfinite ниже намеренно строже автоматического восстановления.

### W1-12-F08 — Loader проверяет синтаксис; смысл и полнота остаются нашей задачей

Тип: code observation S05. verify_image_label для detect проверяет five-column rows, нормализацию с 1% tolerance, допустимые class IDs и integer labels; missing, empty, corrupt фиксируются отдельно. Missing/empty annotations могут стать пустым label array, а не fatal error. Текущий dataset cache version=1.0.12, но совпадение версии cache не подтверждает корректность данных.

Тип: вывод. Успешный scan не доказывает отсутствие пропущенных объектов, правильность helmet/no_helmet, пары image-label, независимость камер и корректность boxes после crops/augmentation. Для отрицательного кадра нужны условия annotation coverage. Исправления labels должны сопровождаться проверкой реального прочтения новых данных и cache invalidation, а не предположением, что trainer всё заметил.

## Диагностическая карта: что сделать до tuning

Это наши процедуры, опирающиеся на F01–F08, а не результаты выполненных прогонов. Нет универсального порога «хорошего» detection loss. Даже tiny overfit не доказывает отсутствие всех bugs: Stanford S12 прямо оговаривает возможность запомнить ошибочно подготовленные inputs. Не требовать нулевого общего YOLO loss или 100% AP как универсального критерия; достаточно заранее заданного качественного/численного допуска для конкретного диагностического набора.

| Порядок | Наблюдения и развилка | Что остановить / передать |
|---|---|---|
| 1. Contract/labels | Task, names/IDs, единица bbox, exhaustive vs partial, видимость объекта. Overlay исходных labels на positive/negative кадрах каждого класса/источника | Любой class mismatch или пропущенный обязательный объект → datasets; LR пока не менять |
| 2. Реальный loader | Сверить список файлов/counts/split hashes; полученные img/cls/bboxes/batch_idx; shape/dtype/range/channels, letterbox/crop; overlay после transforms; пустые target batches | Loader hang → workers/cache/I/O, не optimizer. Несовпадение target/geometry → исправить pipeline |
| 3. Forward/backward/step | Loss-компоненты конечны, grad enabled; ожидаемые head/backbone trainable; gradient nonzero на положительном batch, finite; unscaled norm; веса до/после настоящего optimizer step | None grad не всегда bug: frozen/unused branch нормальны. Неизменение всех нужных весов после подтверждённого step → loss detach/freeze/optimizer/scaler диагностика |
| 4. Tiny overfit | Один и тот же вручную проверенный малый набор, без сильных случайных transforms; видеть конкретные boxes до/после обучения; проверка на тех же train images только для sanity | Не способен выучить видимый понятный объект → labels/preprocessing/loss/head/update; длинный full run не запускать |
| 5. Reload | Закрыть процесс; load сохранённого checkpoint; фиксированный input/preprocess/postprocess, сравнить outputs и маленькую val | Расхождение → artifact/version/class map/mode/precision; не обвинять LR |
| 6. Independent validation | Ошибки по классу/камере/размеру; train vs вал; фиксировать thresholds/NMS и geometry | Train хорошо, target плохо → leakage/domain/coverage/visibility; отсутствие сигнала → scale/violation_methods |
| 7. Только теперь tuning | Явный optimizer для LR-сравнения; один фактор, одинаковые inputs/budget/selection | Нет практического выигрыша на выбранном val → сохранить baseline, закрыть гипотезу |

Для исключения процессов loader допустим диагностический workers=0/cache=False (реальные cfg args S01), но это изоляция причины, не рекомендация максимальной скорости. Windows script требует main guard по S09; конкретная ОС будущего training не предполагается. Anomaly detection S11 запускать только на минимальном воспроизводимом batch, охватывая forward и backward; это инструмент поиска операции с NaN, а не оптимизация production training.

## Контролируемые E-процедуры будущей практической волны

Все E — предложения. Ограничения ниже выбраны нами для сдерживания диагностики, не являются результатами paper, SLA или измеренным временем RTX 4070. Инженер до старта обязан записать модель/checkpoint checksum, commit, torch/CUDA/driver/OS, GPU/VRAM, dataset manifest/class map, split и критерий допуска. Если эта информация неизвестна, не заполнять фиктивными значениями.

### W1-12-E01 — Labels/loader gate

**Входы:** выбранный detection checkpoint из model_stack, небольшой вручную проверяемый набор реальных кадров; хотя бы positive каждого доступного обязательного класса, background и сложный пример; раздельные camera/session IDs. Цель — решить, можно ли доверять training inputs. **Контроль:** source image hash и ручной GT; никакой training, lockbox не использовать. **Действия:** вывести counts missing/empty/corrupt и class IDs; overlay исходных и реально преобразованных boxes; workers=0/cache=False при loader failure; сверить цвета/диапазоны/геометрию с конкретным model preprocessing. Не отключать все преобразования одним выдуманным detect augment=False: список действующих transforms задаётся и проверяется по W1-05.

**Метрики/артефакты:** counts с denominators, crop sizes/object pixels, contact sheet before/after, список найденных несоответствий, manifest/config/log. **Исход:** совпало → E02; исправимые labels/loader → исправить и повторить только изменённый gate; объект физически неразличим → W1-06/violation_methods. **Stop:** любое смысловое несоответствие; на один проход ограничить ручной просмотр заранее выбранной стратифицированной выборкой, записать покрытие. **Предел:** выборочная проверка не доказывает полноту всего датасета и не подтверждает generalization.

### W1-12-E02 — Реальный update и локализация nonfinite

**Входы:** прошедший E01 фиксированный positive batch, тот же checkpoint; инструментирование trainer/hooks без изменения loss. **Контроль:** неизменённый frozen reference tensor и выбранный trainable head tensor; точная стадия accumulation. **Действия:** выполнить forward/backward до одного подтверждённого optimizer step; записать loss components, requires_grad, None/zero/nonfinite gradients, unscaled norm и относительное изменение weight. Градиент проверять до zero_grad; отсутствие delta до границы accumulation не считать сбоем. При NaN сохранить воспроизводящий batch; один короткий повтор с amp=False, затем при необходимости autograd anomaly для traceback. Не превращать repeat с FP32 в сравнение качества.

**Метрики/артефакты:** step count, param_groups LR/decay/betas/momentum, AMP check passed/skipped/failed, scaler state/scale, norm до clip, weight deltas, first failing operation, batch hashes/log. **Исход:** finite+update → E03; absent grad/update → loss/freeze/optimizer wiring; только AMP failure → FP32 как диагностический route, затем установить поддержку precision; failing input → E01. **Stop:** первый nonfinite; для исходного batch не более двух сравнительных precision попыток и одного traceback, без автоматического длинного retry. **Предел:** один update не доказывает сходимость; grad≠0 не доказывает правильность labels или полезность направления обновления.

### W1-12-E03 — Tiny overfit и обязательный reload

**Входы:** E01/E02 passed; выделенный diagnostic train set, например 8–16 независимых кадров (это наш предлагаемый бюджет, не target label budget), видимые объекты и понятные labels; baseline predictions. **Контроль:** одни и те же кадры/checkpoint/size; augmentation явно минимизирована, weight_decay=0 как диагностическая абляция, не финальная recipe; явный optimizer и LR из одобренного baseline; warmup/scheduler/accumulation заранее записаны. Для короткого run учесть F06 и warmup capped E−1. Намеренное использование train images для этой проверки явно маркируется sanity-only; validation результата не публикуется как перенос.

**Действия:** ограниченно обучить на этих примерах, смотреть loss и boxes именно для них; затем сохранить artifact, завершить процесс, загрузить заново и повторить те же входы. Сравнивать EMA с EMA/reloaded model: сравнение online weights с EMA без оговорки создаёт ложное расхождение. До запуска согласовать практический допуск по localization/classification и численный tolerance outputs для выбранных dtype/backend; exact byte equality не обещается.

**Метрики/артефакты:** optimizer updates, loss components, train per-class recall/precision при фиксированных thresholds и IoU, overlays, checkpoint checksum, config/seed, до/после reload predictions и численное расхождение. **Исход:** выучил и reload совпал → E04; выучил, reload расходится → artifact gate; не выучил → остановить full training и вернуться к E01/E02/head/loss, затем scale/visibility. **Stop:** первый nonfinite; максимум 300 реальных optimizer updates или 15 минут wall-clock, что раньше (предложенный диагностический cap); не более одного исправления установленной причины с повтором. Непрохождение cap не доказывает невозможность научить модель, только отсутствие допуска к дорогому trial. **Предел:** memorization не подтверждает independent quality, event logic, export или LinQ.

### W1-12-E04 — Только проверяемая оптимизационная гипотеза

**Входы:** E03 passed; реальная train/val с независимыми camera/session groups, untouched lockbox вне tuning, baseline и заранее выбранная практическая метрика evaluation. **Контроль:** одинаковые source weights, train/val, sampling, resolution, transforms, seed, postprocess; фиксированный optimizer для LR sweep. **Действия:** сначала baseline, затем один кандидат; например LR понижен при подтверждённых spikes/oversized updates, или изменён warmup при проблеме начала training. Конкретное число выбирается после baseline, не назначается как universal recipe. Batch/accumulation проверять отдельным опытом: равный effective batch не делает BN/decay/updates равными. Scheduler/close_mosaic/early stop аблировать отдельно, с фактическими LR curves и количеством пройденных фаз.

**Метрики/артефакты:** mAP50:95 и per-class/size breakdown, критичные misses и FP по согласованному evaluation protocol, валидированный checkpoint по заранее фиксированному selection, wall-clock/updates/GPU peak memory, error gallery, run manifest и logs. Встроенный best.pt может оптимизировать другую цель, чем event-level safety requirement; заранее согласовать сохранение кандидата. **Исход:** выигрыш достаточен → W1-15 conditional repeat/selection и далее export gate; нет выигрыша/регрессия редкого класса → baseline; одинаковая проблема при всех recipe → данные/scale/domain. **Stop:** первый неустранённый nonfinite, OOM после согласованного снижения batch, отсутствие пригодного checkpoint; заранее установленный time/update cap и число кандидатов (для первого опыта baseline+один). Увеличение бюджета только после содержательной причины. **Предел:** один seed на одной validation не доказывает устойчивый выигрыш и ничего не устанавливает о LinQ.

## Открытые вопросы и адресные передачи

| ID / адресат | Недостающее и решение | Нужное подтверждение |
|---|---|---|
| W1-12-Q01 → model_stack | Какой checkpoint/task/version реально выбраны? Где фактические model overrides и loss? | Получить immutable model/config/weight hashes; сравнить actual args и optimizer groups с F01–F03. Если другой стек/commit — не переносить defaults |
| W1-12-Q02 → datasets | Exhaustive ли annotations? Правильно ли missing/empty трактуются как negatives? | Annotation coverage contract, camera/session IDs и E01. Успешный scan S05 недостаточен |
| W1-12-Q03 → evaluation, W1-15 | Какую цель оптимизирует checkpoint selection: detector AP или event metric/critical recall/FP? | Формально задать val protocol, constraints и stop/accept thresholds. Встроенный fitness S07 не даёт эту цель автоматически |
| W1-12-Q04 → W1-14/video_architecture | Какие реальные B, accumulation, OOM retries, loader stalls и precision? | E02 + profiling; никакой оценки времени или VRAM по имени RTX 4070 |
| W1-12-Q05 → violation_methods/W1-06 | Есть ли нужный визуальный сигнал при реальном масштабе/occlusion? | Ошибки на вручную проверенных crops и эпизодах; невозможность увидеть сигарету/ношение СИЗ не исправляется одним LR |
| W1-12-Q06 → linq_platform/model_stack | Какой student/checkpoint после EMA и final stripping требуется экспортёру/SDK? | Отдельно пройти load/export/target-execution и paired output/quality check. Training precision и training success не доказывают LinQ support |
| W1-12-Q07 → W1-02 | Как сделать freeze→unfreeze без игнорируемых resume overrides и с известным BN? | Новый режим с проверкой trainable mask/BN stats и state manifest; S02.check_resume; не считать смену freeze автоматически чистым сравнением |

Обоснованные направления дальнейшего поиска узкие: если E02 обнаружит precision failure — конкретная model/op и версия PyTorch; если tiny overfit проходит, а val нет — coverage/domain/visibility; если recipe-кандидат выигрывает — независимость и variance W1-15. Общий дальнейший поиск «лучшего optimizer для CCTV» до этих наблюдений не даёт проверяемого выбора.
