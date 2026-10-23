# W2-11 — Checkpoint objective, lifecycle и freeze→unfreeze

K011; checked_at: 2026-10-23T07:42:52+03:00, Europe/Moscow. Время исследования, не время training. Роль W2 gpt-6.1-sol/medium, без делегирования. Прочитаны контекст/тематическое задание, PLAN, K011 и внешние неизвестные CRITIC, назначенные W1-02/10/12/15 и W2-01. Выполнены primary search, web open и read-only HTTP чтение исходников. Training/resume/export и изменение trainer **не выполнялись**. Единственный результат этой ветки — этот файл.

**Решение:** заранее сохранять неизменяемые pre-strip EMA checkpoints через штатный `on_model_save` при `save=True, val=True`; свой evaluator выбирает bundle независимо от AP-best. Для stage2 с новой freeze/BN/LR политикой предпочтителен явно новый run из выбранных weights с `resume=False`. Даже сохранённый pre-strip checkpoint не обеспечивает exact trajectory continuation: штатный payload содержит EMA вместо online weights и не содержит scheduler/RNG/loader state. `freeze` на данном pin **разрешён при resume**, но это уже вмешательство в оптимизацию, если маска меняется.

## Источники и граница версии

Все code observations относятся к U=`e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`, package `8.4.184`. Дата commit `2026-10-22T20:27:18Z` установлена W1-12 и W2-01; здесь не заявляется повторный metadata test или установка package. W2-01 установил связь wheel с этим деревом. Access всех источников ниже: 2026-10-23; публикационные даты live docs не установлены. Код открыт как текст, не исполнен.

| S-ID | Первичный источник Ultralytics | Точный локатор / назначение |
|---|---|---|
| W2-11-S01 | [engine/trainer.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/trainer.py) | BaseTrainer.train, _setup_train, _do_train, save_model, validate, final_eval, check_resume, _load_checkpoint_state, resume_training, build_optimizer, _model_train, _setup_scheduler. Получен raw HTTP и web open |
| W2-11-S02 | [utils/torch_utils.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/torch_utils.py) | ModelEMA, strip_optimizer, convert_optimizer_state_dict_to_fp16, EarlyStopping; raw HTTP + web open |
| W2-11-S03 | [engine/model.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/model.py) | Model.train, add_callback; raw HTTP + web open |
| W2-11-S04 | [callbacks/base.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/utils/callbacks/base.py) | on_train_epoch_end/on_model_save/on_fit_epoch_end/on_train_end; web open |
| W2-11-S05 | [Training callbacks](https://docs.ultralytics.com/usage/callbacks/) | Live vendor guide, add_callback examples; search→open. Не источник pin-specific порядка |
| W2-11-S06 | [Train](https://docs.ultralytics.com/modes/train/) | Live vendor guide, Resuming Interrupted Trainings, Training Arguments; search→open |
| W2-11-S07 | [nn/tasks.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/nn/tasks.py) | load_checkpoint: EMA-or-model → float/eval, default fuse=False; raw HTTP |
| W2-11-S08 | [engine/validator.py на U](https://github.com/ultralytics/ultralytics/blob/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/ultralytics/engine/validator.py) | BaseValidator.__call__/get_model: training EMA, FP32 weights under autocast; raw HTTP |

Поиск по exact callback/resume names вывел official guide/reference и GitHub; дальнейшее решение принято по U. Текущий main/reference может меняться, поэтому snippets main не являются основанием call order. Новых количественных claims качества/скорости нет.

## W2-11-F01 — Порядок одного epoch и нормального завершения

**CODE, S01/S02/S04/S08; уточняет W1-12-F05 и W1-15-F08.** Порядок ниже существенен: observer callback после save уже не может задним числом изменить fitness этого файла.

| Порядок в `_do_train` | State / следствие |
|---|---|
| `self.epoch=epoch`; `on_train_epoch_start`; `scheduler.step()`; `_model_train()` | Callback epoch-start выполняется **до** model.train/BN freeze. BN eval, выставленный только этим callback, затем может быть сброшен |
| batches → backward → накопление → `optimizer_step()` | unscale → clip norm 10 → scaler.step/update → zero_grad → EMA.update. EMA update count не равен batch count |
| criterion.update (если есть); LR snapshot; `on_train_epoch_end` | Validation ещё не выполнена; metrics здесь могут относиться к предыдущему epoch |
| EMA.update_attr(yaml/nc/args/names/stride/class_weights) | Training validation получает EMA; weights float, eval, inference-mode/autocast в validator |
| `final_epoch = epoch+1 >= epochs`; conditional `validate()` | Выполняется при `val or final_epoch or stopper.possible_stop or stop`. Для каждого-epoch отбора требуется `val=True`; `val=False` не гарантирует свежую fitness каждого save |
| `validate`: validator → pop fitness → update best_fitness | Standard detect fitness — AP50:95, установлен W1-15-F08. Best обновляется строго при improvement; fallback при отсутствии fitness — negative loss |
| `_handle_nan_recovery(epoch)` | При recovery до save/callbacks возврат к epoch loop, повреждённый pass не считается новым candidate |
| save_metrics → stopper(epoch+1, fitness) / final_epoch → time-stop | CSV epoch — one-based; checkpoint epoch — zero-based. Stopper сохраняется уже после текущего решения |
| `(args.save or final_epoch) and save_model()` → `on_model_save` | Только rank -1/0; callback вызывается после successful write. `last` и AP-best уже записаны, final stripping ещё впереди |
| epoch-time/time-mode пересчёт epochs/scheduler → `on_fit_epoch_end` | Может уже отличаться args.epochs от записанного train_args при time mode. Потом memory cleanup, DDP stop broadcast, break/next epoch |
| после loop → `final_eval()` | Strip last; strip best с train_results из last; validate best, если он существует. Если best нет, last не заменяет best в final validation |
| final best validation → metrics.pop(fitness) → epoch временно +1 → `on_fit_epoch_end` → epoch обратно | **Дополнительный** вызов этого callback без нового save и без новой assigned self.fitness. Нельзя считать его ещё одним training epoch |
| plot_metrics → `on_train_end`; loader cleanup; train-finally `teardown` | on_train_end уже слишком поздно для копии pre-strip last/best. finally обеспечивает teardown, но не аварийный checkpoint |

`EarlyStopping` обновляет best_epoch при `fitness>best_fitness` (и специальном initial zero), поэтому равенство положительной fitness не продлевает patience. При этом `save_model` пишет best при `best_fitness==fitness`: tie может **перезаписать best** более поздними weights. Детекторный AP-best и epoch stopper не обязаны совпадать при ties.

## W2-11-F02 — last/best/periodic и предел защиты от прерывания

**CODE, S01/S02.** save_model один раз сериализует общий buffer: `last.pt` всегда; `best.pt` при equality текущего fitness с best; `epoch{self.epoch}.pt` при `save_period>0 and epoch % save_period==0`. Например `save_period=1` сохраняет epoch0, epoch1…; `save_period=5` — epoch0, epoch5… (это zero-based индекс, не «пятая законченная эпоха»). Periodic save находится **внутри** save_model: `save_period` не заменяет `save=True`. Штатный final_eval strips только last/best; periodic/callback copies остаются pre-strip, пока кто-либо явно их не обработает.

Time limit проверяется после optimizer step и после epoch validation; soft stop завершает путь validation/save, затем final_eval/strip. Это не hard wall-clock deadline: val/save/final val выходят за train cap. При time mode epoch estimate и scheduler пересоздаются после epoch. `save=False` опасен: early/time stop не обязательно final_epoch, поэтому последний soft stop может не записаться. Выбор `save=True` закрывает этот случай. Callback может выставить `trainer.stop=True` между batches; это partial epoch с последующей validation/save и индексом этого epoch. При resume штатный start_epoch будет **следующим** epoch: необработанный остаток partial epoch не воспроизводится.

Hard kill/KeyboardInterrupt/exception не имеют гарантированного вызова save_model/final_eval: остаётся лишь ранее завершённый save. `write_bytes` не является транзакционной atomic save; kill во время записи может повредить last. Нужны immutable copies и проверка reload/hash, а не только существование файла. Mid-epoch gradients и sampler cursor не сохраняются. NaN recovery/OOM retry могут менять фактический ход: их нужно сохранять в log, не считать normal continuation.

## W2-11-F03 — Реально сохранённое и точный смысл resume

**CODE + INFERENCE, S01/S02/S07.** «Resume поддержан» и «восстановлена та же траектория» — разные свойства. Payload штатного pre-strip save:

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

**W2-11-F04 — Boolean resume может тихо стать новым training. CODE S03/S01.** `YOLO(path).train(resume=True)` проверяет `self.ckpt.epoch>=0` и optimizer!=None. Если checkpoint stripped, пишет warning и меняет resume=False: стартует новый training. Явный `.train(resume="path/to/prestrip.pt")` идёт через check_resume; недопустимый epoch затем вызывает assert. Поэтому считать режим по resolved args/log/start_epoch, а не по написанному `resume=True`. Для возобновления использовать explicit immutable path и preflight state; не `get_latest_run` fallback.

## W2-11-F05 — Freeze/unfreeze, args и новая стадия

**CODE S01; уточняет W1-02-E01/E02 и W1-12-Q07.** Полный whitelist U check_resume:

`imgsz, batch, device, close_mosaic, augmentations, save_period, workers, cache, patience, time, freeze, val, plots, channels_last, distill_model, save_dir`.

`data` обрабатывается отдельно: supplied data заменяет ckpt_args data. Остальные изменённые args (кроме исключённых служебных model/data/mode/resume/pretrained) дают warning и используют checkpoint values. В частности **epochs, optimizer, lr0, lrf, momentum, weight_decay, warmup_epochs, cos_lr, amp, seed** не разрешены этим whitelist. `project/name` не являются штатным способом перенести resume; `save_dir` разрешён. Не считать молчание на pretrained доказательством применения: setup_model игнорирует pretrained override при resume.

Freeze формируется заново в `_setup_train`: integer→range(N), list→явные индексы, плюс always `.dfl`, а для KD teacher_model. Совпавшие параметры получают requires_grad=False, прочие floating ранее frozen параметры **размораживаются**. Значит сохранённая ручная requires_grad mask не является контрактом следующего setup. `_model_train` каждую эпоху делает model.train(), потом frozen matching `BatchNorm2d` переводит eval; остальные BN работают train. Возврат unfreeze переводит их BN в train, если нет другой политики. DFL остаётся frozen и при freeze=0. Любая другая BN политика требует своего проверенного callback/custom trainer; отдельного штатного BN-policy flag эта ветка не установила.

`build_optimizer` перебирает все named parameters, без фильтра requires_grad. Поэтому штатный freeze→unfreeze при resume не обязательно ломает param-group размеры: ранее frozen params уже могли быть в groups, но без state до первого gradient. Их дальнейший update с новым gradient и старым optimizer/state остальных — **смешанная история**, а не fresh low-LR stage2. Это code-supported possibility, не runtime гарантия для изменённой топологии/KD/QAT. Менять masks после optimizer creation вручную здесь не предлагается.

Минимальный операционный выбор:

| Намерение | Штатный интерфейс U / смысл |
|---|---|
| Продолжить прерванный recipe | Новый процесс; explicit resume path к pre-strip file; те же data/teacher hashes, freeze, batch/geometry и допустимые overrides без изменения recipe. Проверить start_epoch и загруженный optimizer/scaler/EMA/stopper. Это штатный resume с указанными F03 ограничениями |
| Новая stage2: unfreeze + новый LR/optimizer/budget | `YOLO(selected_weights).train(resume=False, data=..., freeze=0, optimizer=..., lr0=..., epochs=..., project=..., name=...)`; значения символические/выбираются до trial. Новый optimizer/scaler/EMA/stopper/scheduler/epoch0/warmup; **warm start** из выбранной EMA, а не resume |
| Намеренно unfreeze в прежнем run | resume с `freeze=0` разрешён, но optimizer/LR и budget наследуются; записать intervention и проверить masks/BN/groups после setup. Не применять как замену строке stage2 выше |

Для supervised stage2 брать проверенный student-only **отдельный** artifact. Можно сделать производную stripped копию через штатный `strip_optimizer(f=immutable_prestrip, s=distinct_student_path)`; источник остаётся нетронутым. Не fuse перед будущим training. `distill_model=None` в новом supervised run задавать явно, иначе train_args старого KD могут повторно включить distillation. Для новой KD стадии — явно та же/новая teacher admission и отдельная provenance.

## W2-11-F06 — Candidate objective без изменения trainer

**PROPOSED INTERFACE на S01/S03/S04/S05, не готовый evaluator.** Для сохранения по event/critical-class constraints custom trainer **не обязателен**: штатный `model.add_callback("on_model_save", callback)` даёт trainer после validation/write, пока checkpoint ещё pre-strip. Достаточный интерфейс callback:

1. На rank -1/0 скопировать `trainer.last` в уникальный `candidate_epoch{trainer.epoch}_{hash}.pt` **синхронно до возврата**, записать hash/epoch/EMA source и args/data/class/split/evaluator manifests. Never overwrite accepted candidate. Базовые настройки `save=True, val=True, save_period=1` страхуют каждый завершённый save; storage budget назначить отдельно. При недостатке места save_period=1 можно заменить callback-only архивом, сохранив every-epoch copy policy.
2. Внешний evaluator принимает **path/hash** immutable serialized candidate, val episode manifest, preprocessing/decoding/NMS/threshold policy, event-rule version и returns per-class/events/exposure metrics + constraint status + support. EMA deepcopy snapshot в памяти допустим как дополнительный diagnostic reference, но selection итогового artifact проверять после его reload.
3. При дорогой event evaluation можно ставить immutable paths в отдельную очередь; копировать нужно сразу, а оценивать позже. Это не реализованный async service. Pipeline обязан дождаться решения по нужным candidates, иначе финальное best по AP не заменяет отсутствующий event result. Lockbox не участвует.
4. Сохранять constrained winner как bundle с model hash, rules/thresholds и metric evidence, отдельно от `best.pt`. Сначала eligibility по constraints, затем заранее заданная utility/tie policy; AP stop/fitness остаются штатными. `patience=0` штатно отключает AP early-stop, если иной stopping contract требует этого; time cap остаётся независимым. Своё bounded stop допускает callback `trainer.stop=True`, с оговоркой partial epoch F02.

`on_fit_epoch_end` также после save, но final_eval вызывает его ещё раз; именно `on_model_save` проще исключает финальный дубль. `on_train_epoch_end` слишком рано для текущей val fitness, `on_train_end` слишком поздно для pre-strip copy. Validator callbacks доступны, но `on_val_end` ещё до BaseTrainer.validate присвоения self.fitness; не следует рассчитывать, что изменение trainer.fitness там перепишет корректно весь selection.

Если команда хочет **заменить** встроенный fitness/AP-best/stopper своей event objective, а не вести внешний winner, требуется reviewed custom validator/trainer integration, возвращающая fitness до validate/stop/save. Одного `on_model_save` для этого недостаточно. Такой port не выполнен и для минимальной схемы не требуется. Callbacks/внешняя очередь/selector сами не сериализуются как их runtime progress: хранить selection ledger отдельно и регистрировать callbacks заново в новом process. Local runtime hooks на EMA могут сломать pickle; использовать обычную immutable disk copy, не навешивать на неё локальные hooks.

## W2-11-F07 — Что normal stripping уничтожает

**CODE S01/S02 + W2-01-F07.** strip_optimizer меняет EMA→model, model→FP16, requires_grad=False, criterion=None; epoch=-1; optimizer/best_fitness/stopper/ema/updates/scaler=None, train_args ограничиваются default keys. Final best получает **train_results из last**, поэтому CSV history в best не доказывает его winning epoch. Pre-strip winner epoch/hash ledger нужен заранее.

KD correction: teacher уже **отсутствует в EMA** (`teacher_model=None`) до save; EMA wrapper сохраняет projectors. Final strip снимает hooks и извлекает student, удаляя wrapper/projectors из model graph. Для interrupted KD resume нужны teacher bytes/path/hash и projector state pre-strip. `distill_model` path override допустим; тот же path с другими bytes меняет эксперимент. После strip projectors/optimizer/epoch/EMA count/stopper/scaler из student не восстановить. Online weights/RNG/loader/scheduler не существовали и в штатном pre-strip payload; они не «теряются только при strip».

Путь method→implementation→candidate→benefit: external constrained selection — наш protocol, штатные callbacks/save установлены; candidate contract выше code-supported; конкретного evaluator, целевого выигрышного epoch и выполненного reload нет. Final inference/student contract code-supported W2-01, actual export/LinQ по-прежнему неизвестен.

## W2-11-E01 — Future save/reload/stage-transition gate

**PROPOSED, не выполнено; дополняет W1-12-E03 и W1-15-E02/E04, не отдельный quality trial.** Решение: допускается ли recipe к длительному training и передаче artifact. Входы: pinned package/environment, допустимый unfused model/teacher hashes, небольшой fully reviewed train diagnostic set, независимые development inputs, selection/rule manifest. Budget/success tolerance назначить заранее из фактической среды. Lockbox не открывать; correctness predictions не считать quality evidence.

1. В bounded smoke зарегистрировать copy callback до train; проверить после setup mask, BN flags/buffers, optimizer groups и callbacks registration. Снять online/EMA tensor manifests раздельно. Получить хотя бы один successful save и hash immutable copy; сверить zero-based epoch, last/best/epochN равенство bytes там, где они должны происходить из общего buffer, и ledger.
2. В новом процессе inspect trusted pre-strip checkpoint: model=None, ema есть; optimizer/scaler/stopper/epoch/updates/args корректны; все необходимые tensors finite. Для KD teacher=None внутри EMA, projectors есть, внешний teacher hash доступен. Затем на **копии** проверить штатный resume: start_epoch+1 contract, optimizer state/param ordering/dtypes, scaler, stopper best epoch, EMA count, reconstructed scheduler LR, first actual update и BN policy. Записать ожидаемые отличия online/EMA/rounding/RNG; не требовать битового совпадения.
3. Нормально закончить smoke; проверить last/best stripped fields и отсутствие KD wrapper/projectors в final graph, periodic/callback copy всё ещё pre-strip. Загрузить student derivative в другом process без teacher path для inference. Сравнить outputs с тем же serialized pre-strip EMA student, одинаковые inputs/mode/precision/postprocess, заранее допустимая погрешность; live FP32 EMA не подменяет reference без учёта FP16 save.
4. Проверить новую stage2 `resume=False`: epoch0; fresh optimizer/scaler/EMA updates/stopper/scheduler; ожидаемые weights переносятся; freeze=0 снимает planned layers, DFL/teacher остаются fixed; BN stats и gradients соответствуют политике. Для supervised явно distill_model=None. Один finite фактический update с новым LR подтверждает wiring, не полезность.

Observables: exact args/log/ignored overrides, code+environment+weight hashes, model/optimizer state summaries, original and restored epochs/EMA updates, per-group LR/decay/betas/momentum, trainable names/BN deltas, first update, serialized candidate predictions, save/val/reload wall time, files+ledger. Soft time-stop отдельно при необходимости проверяет partial epoch и превышение cap, не оценивает качество. Hard-kill simulation не обязательна: достаточно не обещать гарантии за пределами completed copies.

Outcomes: корректный copy/reload/stage switch → reuse W1-15 controlled comparison/export gate; state mismatch → остановить длинный run и локализовать interface/version/mask; final inference требует teacher → KD extraction gate failed; неприемлемая serialized parity → не promote этот artifact. Stop: missing/неfinite state, wrong class mapping/mask, отсутствующая immutable copy, unexpected new run вместо resume или unexpected distillation. Успех не подтверждает convergence, benefit, bitwise continuation, target quantization или LinQ.

## Остаток K011 и передача

| Q-ID / тип | Остаток и решение | Как закрыть |
|---|---|---|
| W2-11-Q01 / case+evaluation, P0 | Какая constrained objective, support/FP exposure, tie/stop policy и стоимость event evaluator? | Полный кейс + evaluation; утвердить contract до selection. AP-best не достаточен |
| W2-11-Q02 / artifact+experiment, P0 | Работают ли copy callback, fresh-process load/resume и stage2 в фактической package/dependency среде? | E01; public code не runtime результат |
| W2-11-Q03 / experiment, P1 | Нужно ли сохранять exact online/RNG/loader/scheduler/gradient state для иной цели продолжения? | Если нужно exact trajectory, штатный формат U недостаточен: отдельный reviewed serializer/trainer contract и тест. Не обещать восстановление задним числом |
| W2-11-Q04 / SDK, P0 | Пригоден ли final selected student artifact/graph для actual LinQ path? | Reuse W1-15-E04/W2-01-E01, доступ SDK и реальный compile/run |

**Outcome K011:** публичная lifecycle/operational часть закрыта и область «exact resume» существенно сужена. До training необходимо сохранить every-save immutable pre-strip files, provenance/selection ledger и teacher bytes для KD; normal stripped last/best служат inference/warm-start artifacts. Stage2 по новым LR/optimizer/BN требованиям — новый run. Target objective, working event evaluator и reload evidence остаются внешними входами, не дополнительным бесконечным public search.

**→ model_stack:** реализовать только callback copy/ledger interface и E01 на выбранном package; штатный trainer не менять ради внешнего selection. **→ evaluation:** возвращать metrics+constraints+support по immutable serialized path, фиксировать event rules/thresholds. **→ W2-12:** E01 — reused correctness gate; не добавлять обязательный quality trial. **→ linq_platform:** принимать final student derivative + selected hash/settings, не KD training wrapper; resume file хранить отдельно.
