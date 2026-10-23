# W2-A — минимальный fail/fork/progress контракт native trainer

Дата исследования/доступа: **2026-10-23**. Host clock: 17:32:49 UTC / 20:32:49 Europe/Moscow. Исполняемая ревизия-кандидат: Ultralytics **8.4.184**, SHA **de290d865035acbfa4bb24cc88960d8b52c26e45**, committer timestamp 2026-10-23 15:51:48Z. Это независимо повторно полученный из интернета source snapshot, **не установленная и не исполненная среда**. Новое первичное чтение: trainer, config/parser, callback registry, model entrypoint, AMP source, official customization/callback docs. W1 использованы для понимания критики. Ни training, ни export, ни аренда, ни устройство, ни fault injection не запускались. Сохранены только собственные `_WORK/W2_A*` материалы.

## Решение и статус критики

**W2-A-F01. Выбрать native_ema как дешёвое приблизительное восстановление, но любой native OOM retry, NaN epoch replay и repair/sanitize весов исключать из неизменяемого A/B trial.** Сохранять результат для диагностики либо отдельно оценённого product candidate; для продолжения создавать дочерний run с объявленной историей. Для чистой ablation перезапускать с исходного immutable initialization и новой recipe. Не строить exact-resume controller. Это предлагаемое правило, его реализация и runtime проверка ещё не выполнены.

**K001: документальная часть закрыта; runtime применимость открыта.** Исходное замечание `CRITIC.md`, K001, сохраняется: W1 пропустила внутренние изменения, exit0+CSV недостаточны. Новые факты расширяют критику: первая NaN-эпоха может продолжиться без rollback; save имеет отдельное исправление/санитизацию; callbacks с именами optimizer_step/on_before_zero_grad в stock loop не вызываются. Закрыт вопрос «какое правило принять и где наблюдать», но не доказано исполнение будущего adapter/архива на реальном host. RPO не подтверждён.

**K011: применимость уточнена, глобально остаётся открыта у сборщика.** Минимум W2-A — pinned trainer, небольшой fail guard, append-only events/progress, immutable копия native recovery snapshot до stripping, внешний bytes/hash/load receipt. Строгий replay/controller отложить. Наша ветка не выбирает за всю команду сценарий, owners и freeze times; это задача root. GPU-часы не рассчитаны.

## Первичные свидетельства

L далее — **1-based строки сохранённых raw файлов**, совпадающих с pinned GitHub blob; web-парсер сжимает пустые строки. Полные полученные исходники и URL/SHA256: [materials](W2_A_MATERIALS/sources.json). Все S — статический код/документация, политики и эксперименты — рекомендации.

| ID | Автор, версия, точный locator | Evidence/ограничение |
|---|---|---|
| W2-A-S01 | Ultralytics contributors, [trainer.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py), L301–339, 450–466, 474–640, 651–685 | OOM/pipeline/warmup. SHA тот же, что W1, получен заново; код не исполнялся. |
| W2-A-S02 | Тот же source, L768–837, 909–920, 1005–1022, 1071–1145 | save/repair, scaler/EMA, NaN/resume; control flow, не docstring. |
| W2-A-S03 | Ultralytics, [default.yaml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/default.yaml) целиком; [cfg/__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/cfg/__init__.py), get_cfg L350+, check_dict_alignment L638–685 | Stock keys и rejection неизвестных overrides; отрицательный результат только для данного SHA. |
| W2-A-S04 | Ultralytics [callbacks/base.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/callbacks/base.py), L31–40,61–64,127–147; [Callbacks](https://docs.ultralytics.com/usage/callbacks), Trainer Callbacks/Forward Hooks | Pinned registry плюс live docs. Docs прямо отмечают reserved callbacks; live page не recipe pin. |
| W2-A-S05 | Ultralytics [model.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/model.py), train L807+,888; [Advanced Customization](https://docs.ultralytics.com/usage/engine), BaseTrainer/Using YOLO with Custom Trainers | Публичный subclass entrypoint; private recovery methods не стабильный API. |
| W2-A-S06 | PyTorch contributors [AMP examples 2.14](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html), Gradient clipping/accumulation; [GradScaler v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/amp/grad_scaler.py), raw L364–479,486–556 | Generic skip и fused special path. Tag, не выбранная установленная dependency. GitHub API resolution SHA получила 403 rate limit; tag не выдаём за независимо проверенный SHA. Raw bytes сохранены. |
| W2-A-S07 | PyTorch [step_post_hook 2.14](https://docs.pytorch.org/docs/2.14/generated/torch.optim.Optimizer.register_step_post_hook.html), signature/description; [Adam v2.14.0](https://github.com/pytorch/pytorch/blob/v2.14.0/torch/optim/adam.py), raw L104–107,810–899 | Hook означает вызов step, не гарантию applied update; fused found_inf корректирует state steps. |
| W2-A-S08 | Ultralytics [torch_utils.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/torch_utils.py), strip_optimizer L895–959; [__init__.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/__init__.py) L3 | Stripping/version; runtime artifact contents предстоит load-verify. |

**W2-A-F02 — control-flow границы.** OOM retry относится к `epoch == start_epoch`, включая первую эпоху resume, только `RANK == -1`, catch вокруг forward/backward. Backend literals отдельны от case-insensitive OOM. Batch1 тоже может retry без уменьшения. NaN gate проверяет текущие loss/fitness, а не всю tensor history; start epoch возвращает False. Save ремонтирует live EMA, затем санитизирует half copy. Поэтому finite checkpoint не доказывает clean trajectory. EMA cadence не обусловлена applied optimizer update. S01/S02; реальных аварий не наблюдалось.

## Trigger → mutation → detection → status → next action

Таблица — **наш контракт**, statuses не являются Ultralytics flags. Events хранить вне resettable counters trainer.

| Trigger | Mutation/locator | Detection | Allowed status | Next action |
|---|---|---|---|---|
| First-start-epoch RuntimeError: OOM либо CUBLAS_STATUS_ALLOC_FAILED, CUDNN_STATUS_INTERNAL_ERROR, unable to find an engine | Halve batch floor1; rebuild; optimizer сохранён; S01 L566–640 | Warning + _oom_retries>0 на повторном epoch start; batch diff недостаточен | FAILED_TECH для A/B; RECOVERED_NONCOMPARABLE для product | Stop до новых batches; child recipe; чистый initialization для ablation |
| Поздний OOM, RANK!=-1, четвёртый retry, OOM в val/optimizer/save | Этот recovery не применяется | Exception/exit/stderr | FAILED_TECH | Устранить причину; новая attempt/recipe |
| Поздние nonfinite loss/fitness | Last EMA→online, state restore, epoch replay; S02 L1088–1126,658–661 | Guard до handler; persistent replay event | FAILED_TECH; salvage child native_ema | Не зачислять в исходный equal-updates trial |
| Nonfinite start epoch | Native continuation без rollback | Per-batch loss guard и fitness до handler | FAILED_TECH | Fail, не ждать max retries |
| Nonfinite EMA/overflow half snapshot | Save repair/sanitize; S02 L775–795 | Pre-save online/EMA/half guard | FAILED_TECH | Finite bytes не снимают failure |
| AMP nonfinite gradients | Skip/backoff, EMA cadence продолжается | Attempts, scale trace, проверенный applied observer | CLEAN только при заранее разрешённой AMP политике, иначе INCOMPLETE_OBSERVABILITY | Не выводить updates из EMA/epochs |
| Native external resume | EMA continuation, pending gradients потеряны | Parent hash/receipt, boundary, resume_mode | Child/attempt RESUMED_APPROX | DEV evaluation; не обещать exact |
| Gap event/progress log | История неизвестна | Sequence/heartbeat/final seal | INCOMPLETE_OBSERVABILITY | Блокировать SUCCEEDED_COMPARABLE до reconcile |

OOM — не только новый batch: прежние online/optimizer/EMA изменения сохраняются, примеры повторяются. Rebuild меняет validation loader, accumulation/decay, nb/nw, scheduler cadence и mosaic gate. После успешного прохода retry counter обнуляется. NaN last может быть старше предыдущей эпохи при редком save; raw online в checkpoint отсутствует. Эти детали определяют policy, но не означают failure на наших данных.

## Stock switches и маленький guard

**W2-A-F03. В S03 нет stock fail_on_oom, disable_oom_recovery, nan_recovery=False или max_retries=0; нужных config branches нет и в trainer.** Не добавлять вымышленные flags. amp=False не отключает OOM/NaN handler; resume=False не запрещает внутреннее recovery; explicit integer batch не запрещает halving. AutoBatch setup и runtime retry — разные механизмы. save=False не является запретом NaN и final save; deterministic не даёт exact resume. DDP не использовать как способ отключить recovery.

Предлагаемый минимум — **pinned guard subclass DetectionTrainer** через документированный `model.train(trainer=...)` (S05). Не копировать loop и не реализовывать RNG/scheduler replay. Спецификация, **не готовая реализация**:

1. В `_build_train_pipeline` до super проверять `getattr(self,'_oom_retries',0)>0`, записывать fail и raise отдельное исключение. Batch assignment уже произошла, но rebuild и новые batches ещё нет. Не мутировать приватный retry counter ради отключения handler.
2. В `_handle_nan_recovery` до super проверять finite loss/fitness и fail, включая start epoch. Отдельный per-batch loss guard нужен для transient NaN, позднее перезаписанной loss. Batch-end guard срабатывает после backward/возможного step; invalid становится вся attempt.
3. В `save_model` до super проверять online/EMA и выбранную half policy. Простой строгий режим отклоняет непредставимые FP16 values; это дополнительное ограничение, не native guarantee. Guard conversion/overflow отдельно проверить drill.
4. В `on_model_save` синхронно создать immutable recovery copy до final_eval stripping, записать bytes/hash/checkpoint epoch; внешний load receipt закрывает архивирование. Mutable last.pt не архив. on_train_end для этой копии уже поздно.
5. Append-only JSONL events/progress и final seal вне CSV. Использовать add_callback, не стирать интеграционные handlers через set_callback.

Stock-only fallback без времени на guard: warnings, repeated epochs и persistent config counters плюс новый run. Это **не полная гарантия**, особенно против save sanitize/аварии до flush. При неполной наблюдаемости — INCOMPLETE_OBSERVABILITY, не «вероятно clean». Product salvage можно разрешить отдельно. Adapter здесь не создан: перед эксплуатацией нужен pin/review/drill.

## Accumulation boundary и actual progress

**W2-A-F04. Native epoch checkpoint не lossless accumulation boundary.** Нет обязательного tail flush: после последнего step остаются gradients, используемые следующей непрерывной эпохой. Они не сериализованы; resume начинает с zero_grad и новой локальной cadence. nbs>batch не гарантирует делимость, warmup меняет accumulate. nbs=batch тоже не решает EMA/raw, RNG/loader/precision отличия. S01/S02 — отсутствие гарантии, не измеренная потеря.

Невыполненный арифметический контрпример: warmup0, nb5, accumulate3, epoch0, last_opt_step=-1. Условие делает step на ni2; ni3,4 pending. Непрерывная следующая эпоха делает step на ni5 с тремя microbatches. Resume теряет pending, сбрасывает last_opt_step и делает иной step на первом batch. Это вывод из исходника, не запуск модели.

Sidecar ниже — **предложение**. Неизвестное null с причиной, не epoch×dataset. Обязательны monotonic consumed work и restored state frontier: rollback не уменьшает затраченный ресурс.

| Поля | Смысл/получение |
|---|---|
| run_id, attempt_id, parent_run_id, parent_checkpoint_sha256, recipe_hash, code_sha, adapter_sha, env_lock_hash | Lineage; fixed spec не перезаписывается effective config |
| event_seq, UTC, monotonic_time, rank/process, epoch_index, epoch_visit | Повтор эпохи получает новый visit; время/seq не сбрасываются |
| requested/resolved/per_rank_batch, actual_batch_len, nbs, accumulate_current, loader_len, warmup, LR/decay groups | Реальная длина из image tensor, не числа cls |
| batches_entered, images_entered, backward_completed_observed, images_backward_completed_observed | Preprocess/forward entry против batch-end observation; exception/time-break промежутки censored |
| optimizer_step_attempts, optimizer_step_calls, optimizer_updates_applied, update_observer_kind, skipped_updates | Разные события; applied только при проверенном observer, иначе null |
| ema_updates, scaler_enabled, scale_before/after, nonfinite_loss/grad/model/ema events | Диагностика, не замена applied counter |
| pending_microbatches/images, pending_gradients_present, boundary_kind | Нет точной наблюдаемости — unknown; epoch label недостаточен |
| oom_events_total, nan_events_total, save_repair_events, recovery_events, replayed_images_observed, rollback_frontier | Append-only history; native resettable counters только дополнение |
| checkpoint_state_epoch, state_frontier_updates, snapshot_sha256/bytes, external_receipt, resume_mode | State может отставать от consumed work |
| comparison_eligible, status, stop_reason, observability_gaps, final_seal | Exit0 — одно из условий приёмки |

**W2-A-F05. Callback по имени optimizer_step создаёт ложную измеримость.** S04 помечает optimizer_step/on_before_zero_grad/on_params_update reserved; stock trainer их не dispatch. Для attempts нужен override метода с super, не одноимённый callback. PyTorch post-hook подтверждает вызов step, однако fused CUDA Adam/AdamW здесь передаёт overflow внутрь kernel. S06/S07 показывают special path: hook count не автоматически applied updates. Равенство весов также не доказывает skip: легитимный update бывает нулевым.

Дешёвый resource-bounded контракт: публиковать attempts/known skips, applied оставлять null до проверки observer. Для equal-applied-updates ablation null блокирует допуск: сначала actual optimizer state-step/skip drill. Не менять optimizer/fused молча ради счётчика — это новая recipe. Сохранённый nominal effective batch не отменяет физическую batch mutation.

## Будущий negative drill — не выполнен

**Вопрос:** отклоняет ли guard ложный clean-success и сохраняет ли native recovery честную lineage? Входы: разрешённый tiny train-only/synthetic набор с batch IDs, pinned executable environment+guard, disposable output, маленький внешний archive endpoint. Нужны отдельное поручение исполнения и при необходимости разрешение ресурсов. Без lockbox, sweeps, реального исчерпания GPU памяти/диска на единственной копии.

1. Однократный synthetic RuntimeError в forward/backward после успешного update: четыре recognized messages. Контроль без guard наблюдает native dispatch; guard должен fail и не выполнять следующие batches. Повтор batch1 проверяет detector без batch diff. Это тест dispatch, не реального fit.
2. Nonfinite loss/fitness в start и поздней эпохе; поздней дать tiny last. Guard должен fail до accepted save. Отдельно transient NaN одного batch, позже перезаписанная loss.
3. Перед save испортить EMA tensor при finite online; отдельно непредставимое half значение. Guard отклоняет accepted snapshot даже если stock контроль запишет finite bytes. Только disposable model.
4. nb5/accumulate3: pending metadata на epoch boundary, normal continuation против native_ema resume. Совпадения не обещать, отклонения документировать; actual warmup учитывать.
5. AMP overflow: сравнить attempts, hook calls, state-step delta, EMA и scale trace. Неверный applied observer для fused path блокирует equal-updates claims. CPU без AMP не подтверждает этот пункт.
6. Final save: immutable pre-strip copy → внешние bytes/hash/load → finalization. Corrupted/stale duplicate не должна пройти receipt; хорошую единственную копию не портить.

Метрики/артефакты: false clean-success (приёмка 0 для выполненных negative cases); next-batches-after-fail (0); event classification/seq; attempts/applied/EMA traces; pending/replayed counters; code/adapter/env hashes; checkpoint manifests и receipts. Время/размеры только после измерения.

Успех подтверждает проверенный scope guard; не доказывает реальный 24GB train/val fit, crash RPO, exact resume, independent accuracy, license acceptance, export, LinQ parity/latency, надёжность Vast. Trace mismatch исправляет observer, не переписывает историю.

## Отрицательные находки и handoffs

- K001 подтверждён; W1 SUCCEEDED дополнить event/observability gate, исходную критику сохранить.
- Backend engine/internal error не доказательство физического OOM: native код объединяет сообщения, причина требует диагностики.
- Native_ema допустим, но требует parent, replayed work, changed recipe и DEV evaluation. History не восстановить из sanitized checkpoint.
- W2-B/training owner: actual Torch/optimizer stack и adapter pin; Ultralytics source SHA установлен, binary/runtime lock отсутствует. PyTorch2.14 здесь механизм, не рекомендация менять согласуемый stack.
- Registry/W1-14/15: comparison_eligible, persistent recovery events, unknown-progress semantics; не строить новую controller platform.
- Root/K011: без закрытых data/runtime/license gates default путь без обучения; один fine-tune после gates; challenger после измеренного обязательного резерва. Native snapshot+receipt — минимум, exact replay deferred.
- Evaluation: salvage candidate оценивать с историей; retries/checkpoint selection не дают доступ к lockbox. Train/DEV/SELECT/lockbox разделять по independent camera/scene/episode, без соседних кадров.
- LinQ: передавать accepted checkpoint hash+label map+preprocessing; recovery success не evidence финального inference.

Открыто: owner guard, actual environment/optimizer, archive endpoint, размеры/latency checkpoints, applied observer, target recovery behaviour. Public research не закрывает runtime вопросы. Расходы и запуски отчёт не авторизует.
