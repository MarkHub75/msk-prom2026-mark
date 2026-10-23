# OPEN_QUESTIONS — evaluation

Состояние после 15 W1 и четырёх W2, 23 октября 2026, Europe/Moscow (+03:00). Сборщик новых источников не получал. Все [E001](OPEN_QUESTIONS.md#e001)–[E011](OPEN_QUESTIONS.md#e011) ниже — будущие, **не выполнены**. Выполненные source-level/synthetic fixtures перечислены в [F001](RAW_FACTS.md#f001). P0 определяет допустимость ключевого утверждения/обязательного LinQ-пути; P1 — воспроизводимость и следующий инженерный выбор. Ближайшая группа: [Q001](OPEN_QUESTIONS.md#q001)/Q002 и [Q009](OPEN_QUESTIONS.md#q009)–[Q014](OPEN_QUESTIONS.md#q014). Частные входы не заменяются новой общей статьёй.

## Q001 — Полный кейс, официальный evaluator и полезная тревога
<a id="q001"></a>

**P0; постановщик/артефакт.** Нужны обязательная taxonomy, score/unit/split/unknown policy, deadline D, reset/reminder/delivery semantics и permitted preparation/adaptation. Official brief/regulation прочитаны ([S119](SOURCES.md#s119), [S120](SOURCES.md#s120), [F207](RAW_FACTS.md#f207)–[F208](RAW_FACTS.md#f208)); численной AP/FPS-формулы/industrial deadline они не дают. Получить оригинал/version/hash из аккаунта и адресное разъяснение спорных требований. Ответ меняет GT, matcher, working point и claims; supplemental не станет official. Связи: [F003](RAW_FACTS.md#f003)/F005/F006, [K002](CRITIC.md#k002)–[K006](CRITIC.md#k006), [E001](OPEN_QUESTIONS.md#e001)/E004/E005.

## Q002 — Exhaustive truth, ownership и наблюдаемость реальных данных
<a id="q002"></a>

**P0; originals/schema + независимая разметка.** Для каких persons/classes/relations/intervals labels полны, есть ли negative time, visibility, wearer edges, unknown/ignore и context? Open Images/VOC/CrowdHuman/AVA/PPE sources изучены, actual files не supplied. Landing page не audit labels. Получить source originals, annotation revision/completeness manifest, провести import/pilot review. Ответ выбирает detector-only/person-chain/event scope. Основания: [F008](RAW_FACTS.md#f008)–[F018](RAW_FACTS.md#f018), [F034](RAW_FACTS.md#f034)–[F048](RAW_FACTS.md#f048), [S002](SOURCES.md#s002)–[S007](SOURCES.md#s007)/S013–[S019](SOURCES.md#s019); [E003](OPEN_QUESTIONS.md#e003)/E009/E010, [Q014](OPEN_QUESTIONS.md#q014).

## Q003 — Что означает «правильно носит»
<a id="q003"></a>

**P0; владелец требований.** Достаточны visible position/coverage или нужны видимая застёжка/subtype/external certification/fit? PPE methods различают presence/owner/wearing, но не устанавливают нужную норму. Hidden fastening, respirator seal, certification и combustibility не устанавливаются одними пикселями. Получить approved context/rule, разделить observable criteria и external/unknown. Ответ меняет labels и название violation. [F008](RAW_FACTS.md#f008)–[F018](RAW_FACTS.md#f018), [F034](RAW_FACTS.md#f034)–[F048](RAW_FACTS.md#f048); [E003](OPEN_QUESTIONS.md#e003)/E008/E009.

## Q004 — Согласие разметчиков и стоимость review
<a id="q004"></a>

**P1; практическая независимая разметка.** Проектные agreement/annotation speed не измерены; methodology и raw-versus-adjudicated protocol есть ([S001](SOURCES.md#s001), [F017](RAW_FACTS.md#f017)–[F019](RAW_FACTS.md#f019)). Выполнить [E009](OPEN_QUESTIONS.md#e009) на отдельно обозначенных pilot/reliability scenes, сохранить contingency/rare/unknown/missing counts, finding/boundary disagreements. Ответ определяет reproducible scope и бюджет audit. Универсальных kappa threshold/sample size нет. [Q002](OPEN_QUESTIONS.md#q002); [E009](OPEN_QUESTIONS.md#e009)/E010.

## Q005 — Lineage и честный holdout
<a id="q005"></a>

**P0; acquisition metadata + audit.** Нужны original video/camera-view/site/session/timestamps, transformed cuts и synchronized same-incident links. Split APIs/WILDS/leakage изучены, actual manifests отсутствуют. API их не восстанавливает. Получить originals/lineage, выполнить [E011](OPEN_QUESTIONS.md#e011), freeze protected components. Один giant component требует новой acquisition или narrow demo claim. Ответ определяет независимость test. [F085](RAW_FACTS.md#f085)–[F103](RAW_FACTS.md#f103), [S042](SOURCES.md#s042)–[S051](SOURCES.md#s051); [E006](OPEN_QUESTIONS.md#e006)/E011.

## Q006 — Разрешённая target adaptation
<a id="q006"></a>

**P0; organizer rules, затем protocol.** Разрешены ли ROI setup, supervised setup, unlabeled online/transductive access и future frames? Tent/WILDS/frozen-fit guidance показывают settings, не разрешения соревнования. Получить rules; сохранить chronology, update/reset и prediction-before/after-update. Ответ выбирает zero-shot/known-camera/adapted/transductive claim. [F096](RAW_FACTS.md#f096)–[F101](RAW_FACTS.md#f101), [S049](SOURCES.md#s049)–[S050](SOURCES.md#s050); [E004](OPEN_QUESTIONS.md#e004)/E006, [Q001](OPEN_QUESTIONS.md#q001).

## Q007 — Actual checkpoint и pretraining overlap
<a id="q007"></a>

**P1; model artifact/provenance.** Weights/hash/repository/corpora/version неизвестны. Dedup literature не сертифицирует closed pretraining. Получить bytes/model card/disclosed memberships и проверить доступные lineage matches. Писать «не найдено методом M среди available assets», не «contamination excluded». Ответ ограничивает score interpretation. [F095](RAW_FACTS.md#f095), [F092](RAW_FACTS.md#f092)–[F094](RAW_FACTS.md#f094); [E011](OPEN_QUESTIONS.md#e011), [Q011](OPEN_QUESTIONS.md#q011).

## Q008 — Temporal support и state lifecycle
<a id="q008"></a>

**P0; methods/product/architecture contract.** Actual context/dwell/unknown pause-or-reset/cooldown/rearm/reconnect и temporal-support mapping не supplied. Исследованы discontinuities/window leakage/coverage. Получить versioned policy/expected cadence, разделить raw state/confirmation/delivery. Это задаёт purge, short-event opportunity и возможность переводить completed frames в analyzed hours. Без defensible mapping публиковать sample completion/gaps. [F057](RAW_FACTS.md#f057)–[F073](RAW_FACTS.md#f073), [F168](RAW_FACTS.md#f168)–[F174](RAW_FACTS.md#f174); [E004](OPEN_QUESTIONS.md#e004)/E007.

## Q009 — Совместимый LinQ package и выбранное устройство
<a id="q009"></a>

**P0; supplied artifact/access → linq_platform.** Нужны exact wheel/build/dependencies, driver/firmware/device identity и полный working example. [S124](SOURCES.md#s124) прочитан/сохранён: blocking sync documented, actual import/run отсутствует; Python3.11/3.8, defaults/imports/fragments не разрешены. Получить metadata/hash/actual signatures/logs. Ответ открывает smoke/parity, не capacity claim. [F002](RAW_FACTS.md#f002), [F216](RAW_FACTS.md#f216)–[F223](RAW_FACTS.md#f223), [K001](CRITIC.md#k001); [E002](OPEN_QUESTIONS.md#e002).

## Q010 — Remote completion и ошибки
<a id="q010"></a>

**P0; versioned remote contract/access.** Как различаются accepted/completed/output-ready, timeout/cancel/retry/late/concurrent sessions и server placement? Public local-host manual не описывает hackathon RPC. Получить schema/docs и actual job/request logs. Если только client timestamps, измерять same-client completed RTT; pure device interval unknown. Ответ определяет timing/ledger/online route. [F222](RAW_FACTS.md#f222), [F230](RAW_FACTS.md#f230), [K001](CRITIC.md#k001)/K002; [E002](OPEN_QUESTIONS.md#e002)/E007.

## Q011 — Exact export/compiled artifacts и parity
<a id="q011"></a>

**P0; artifacts + execution → model_stack.** Нужны actual preprocess/input/output/opset/shapes/dtypes, compiler/quantizer/config/calibration hashes и available intermediates. PyTorch/Ultralytics/ONNX/ORT evidence показывает границы, но exact graph не supplied. Supported family name не гарантирует этот export. Получить artifacts, выполнить [E002](OPEN_QUESTIONS.md#e002) stage ladder; quality-loss allowance фиксирует task owner до test. [F131](RAW_FACTS.md#f131)–[F145](RAW_FACTS.md#f145), [F217](RAW_FACTS.md#f217)–[F221](RAW_FACTS.md#f221), [S070](SOURCES.md#s070)–[S081](SOURCES.md#s081)/S124; [K001](CRITIC.md#k001).

## Q012 — Hardware timer и operation placement
<a id="q012"></a>

**P0 для device-only/full-target claim; P1 для host RTT.** Есть ли documented timer boundaries, per-op trace/placement, fallback policy/disable mode? Inspected manual различает compile/memory slicing/load, но не даёт такого контракта. TLM estimate/profiler name не measurement. Получить vendor evidence либо сохранить unavailable; host decode/pre/post отделить от model core. [F002](RAW_FACTS.md#f002), [F215](RAW_FACTS.md#f215), [F217](RAW_FACTS.md#f217), [F222](RAW_FACTS.md#f222), [S124](SOURCES.md#s124)/S126; [E002](OPEN_QUESTIONS.md#e002)/E007, [K001](CRITIC.md#k001).

## Q013 — Clocks, IDs и конечное закрытие
<a id="q013"></a>

**P0; instrumentation artifacts.** Нужны immutable source/epoch/frame/evidence anchors, scheduled/original release, attempts/batches/logical/visible IDs, destination create/update/presentation logs, clock maps/error, retry lifetime/outstanding at E/C. Timing/RTP/NTP/loadgen/W2 ledger изучены; actual logs нет. Instrument supplied runtime, сначала reconcile tiny ledger observed IDs. Получить capture semantics либо ограничиться receiver proxy/replay lag. Finite close не eventual closure; pending не даёт finite duplicate upper bound. [F146](RAW_FACTS.md#f146)–[F174](RAW_FACTS.md#f174), [F229](RAW_FACTS.md#f229)–[F234](RAW_FACTS.md#f234), [K002](CRITIC.md#k002); [E005](OPEN_QUESTIONS.md#e005)/E007/E008.

## Q014 — Closed matching context и interval/censored truth
<a id="q014"></a>

**P0; annotations + adjoining source/logs.** Нужны independent GT roster, identity/reset/onset joint constraints и opportunity follow-up, complete competing component. W2 даёт protocol/counterexamples, actual truth/logs не supplied. Получить context; сохранить coherent alternate truth cases. Не выбирать midpoint, не retain only censored successes, не называть possible-union maximum attainable. Без closure — narrower estimand/unknown ledger; incidence может быть доступна без recall. [F006](RAW_FACTS.md#f006), [F240](RAW_FACTS.md#f240)–[F244](RAW_FACTS.md#f244), [F258](RAW_FACTS.md#f258)–[F265](RAW_FACTS.md#f265), [K003](CRITIC.md#k003)–[K006](CRITIC.md#k006); [E001](OPEN_QUESTIONS.md#e001)/E005/E010.

## Q015 — Population и поддерживаемая точность
<a id="q015"></a>

**P1; deployment/sampling frame + actual sample.** Camera/site/session selection, shared incidents и positive-bearing groups неизвестны. Cluster/SciPy/survey methods изучены. Finite-corpus randomization не требует iid camera contents; future-camera extrapolation требует дополнительной population модели/выборки. Получить frame либо ограничить claim fixed corpus; показывать per-group counts/undefined/degenerate results. Frames/bootstrap draws не дают sample size/power автоматически. [F004](RAW_FACTS.md#f004), [F176](RAW_FACTS.md#f176)–[F189](RAW_FACTS.md#f189), [F242](RAW_FACTS.md#f242), [S099](SOURCES.md#s099)–[S109](SOURCES.md#s109)/S131; [E006](OPEN_QUESTIONS.md#e006)/E010, [K004](CRITIC.md#k004).

## Q016 — Scalable supplemental matcher
<a id="q016"></a>

**P1; implementation после actual component sizes.** Tiny exact lex-offline-v1/512 graphs проверены; production capacity/official compatibility нет. NetworkX не установлен/не запускался. При необходимости написать fixed-cardinality-cost-canonical-tie candidate с pinned version/tick conversion и сравнить с oracle [E001](OPEN_QUESTIONS.md#e001). Ответ меняет calculation confidence/integration cost, не model quality. [F005](RAW_FACTS.md#f005), [F256](RAW_FACTS.md#f256)–[F261](RAW_FACTS.md#f261), [S133](SOURCES.md#s133)–[S135](SOURCES.md#s135), [K006](CRITIC.md#k006).

## Q017 — Oracle interfaces
<a id="q017"></a>

**P1; actual interfaces → violation_methods/model_stack.** Можно ли заменить ровно persons/IDs/PPE/owner/state/generated events без других изменений? TIDE/conditional interventions изучены, pipeline schemas нет. Получить adapters, фиксировать replaced boundary и negative/unexpected results. Oracle gain — conditional sensitivity, не гарантированный repair/upper bound. Ответ направляет fix вместо ошибочного retraining. [F190](RAW_FACTS.md#f190)–[F206](RAW_FACTS.md#f206), [S110](SOURCES.md#s110)–[S118](SOURCES.md#s118); [E003](OPEN_QUESTIONS.md#e003)/E006.

## Q018 — Что сравнивается и как выбран победитель
<a id="q018"></a>

**P1; training/evaluation provenance.** A/B — isolated code, separately tuned systems, training/data recipe или selected winner reused test? Selection/variance literature изучена, actual variants/budget/history нет. Получить search/access log, frozen artifacts/paired inputs/full recipe. Owner задаёт tradeoff/constraints либо Pareto table. Ответ определяет causal/generalization claim. [F104](RAW_FACTS.md#f104)–[F118](RAW_FACTS.md#f118), [F185](RAW_FACTS.md#f185)–[F206](RAW_FACTS.md#f206); [E004](OPEN_QUESTIONS.md#e004)/E006.

# Программа будущих экспериментов

[E001](OPEN_QUESTIONS.md#e001)–[E011](OPEN_QUESTIONS.md#e011) — **PROPOSAL, не выполнены**. D/tau/epsilon/budget/workload/stop-window выбирает ответственный владелец до test, numeric official thresholds не придуманы. Общий сохраняемый run package: [F212](RAW_FACTS.md#f212), immutable manifest/GT/config/artifact versions, predictions/status, timestamps с domains, matches/metrics/errors и actual environment/command/logs. Выполненные branch fixtures можно переиспользовать как expected answers, не как system results.

## E001 — Evaluator conformance
<a id="e001"></a>

**Решение/гипотеза:** доверять ли wrapper/scorer; importer/empty/ignore/tie/partial assignment может изменить expected counts. **Входы/доступ:** actual evaluator/version, manually specified GT/predictions, saved COCO/sed_eval/TrackEval examples и lex-offline-v1 oracle/results; device не нужен. **Независимая единица:** deterministic fixture, не sample quality.

**Fixed/changed:** freeze coords/classes/comparators/IDs/clocks/expected edges; менять implementation либо один boundary case. **GT/matching:** заранее expected answers именованного benchmark или supplemental protocol, их не смешивать. Cases: duplicates, wrong class/person, unmatched, crowd/ignore, absent/all-empty, exact equality/caps, state-independent person matching, split/merge, linked uncertain onsets/censored successes/failures. **Процедура:** schema→edges/ignore→pairs/cost→counts→aggregation; compare candidate/oracle across saved graphs/permutations, отдельно importer/tick serialization. Generic Hungarian не подменяет priorities.

**Метрики/экспозиция:** applicable cases passed/total с failure IDs, exact pairs/cost/TP/FP/FN/NA; camera-hours не применимы. **Сохранить:** inputs, expected/actual intermediate outputs, hashes/environment, diffs/errors. **Исходы:** match supports tested contract; mismatch требует fix либо нового protocol version. **Остановка:** весь заранее заданный suite обработан, каждая discrepancy исправлена/изолирована до использования score. **Предел:** не model robustness/truth/clocks/production scale. [F019](RAW_FACTS.md#f019)–[F033](RAW_FACTS.md#f033), [F005](RAW_FACTS.md#f005), [F258](RAW_FACTS.md#f258)–[F265](RAW_FACTS.md#f265); [Q014](OPEN_QUESTIONS.md#q014)/Q016, [K005](CRITIC.md#k005)/K006.

## E002 — Native/export/compiled parity и LinQ execution
<a id="e002"></a>

**Решение/гипотеза:** принять ли exact target artifact; preprocess/export/quantization/postprocess или placement может менять поведение. **Входы/доступ:** native/export/compiled hashes/config, common decoded tensors/sequences, separate calibration/dev/test, compatible LinQ package/device/remote contract, raw outputs если доступны, independent GT для quality. **Независимая единица:** paired source sequence/session/camera для quality; tensor elements/timing repeats не deployment samples.

**Fixed/changed:** same frames/tensors/order/reset/class map/downstream/GT/scorer; менять по одному P0–P6 stage. **GT/matching:** tensor reference — named native output, не physical truth; class-aware one-to-one agreement отдельно от independent annotation AP/person/event scores. **Процедура:** actual version/device/job selection/load/completed outputs→input tensor transforms→raw schema/numbers→common decoder/NMS→person/events. Недоступный stage отметить unavailable. Fixed-policy и retuned-on-dev candidate раздельны.

**Метрики/экспозиция:** shapes/nonfinites/error/tolerance exceedances с predefined epsilon, matched/unmatched detections, GT quality/unknown/misses/duplicates/source hours; host completed-call/client RTT samples+n+outcomes. TLM µs — estimate; device interval только documented measured timer. **Сохранить:** tensors/transforms, calibration/qparams, all hashes/compile/device/request logs, outputs/matches/traces/timestamps. **Исходы:** earliest divergence направляет fix; smoke-only claim не parity, quality без placement не LinQ claim. **Остановка:** declared stages/shapes обработаны либо соответствующий claim явно blocked missing access/artifact; load — [E007](OPEN_QUESTIONS.md#e007). **Предел:** sample не capacity/all-ops-on-TPU/unseen-camera safety. [F002](RAW_FACTS.md#f002), [F131](RAW_FACTS.md#f131)–[F145](RAW_FACTS.md#f145), [F216](RAW_FACTS.md#f216)–[F223](RAW_FACTS.md#f223); [Q009](OPEN_QUESTIONS.md#q009)–[Q012](OPEN_QUESTIONS.md#q012), [K001](CRITIC.md#k001).

## E003 — Person–PPE ownership и полный знаменатель
<a id="e003"></a>

**Решение/гипотеза:** bottleneck objects/owner/state/missed persons; высокий object AP может скрывать wearer failures. **Входы/доступ:** exhaustive frames/clips с persons/PPE/known owner/visibility/requirement GT, frozen predictions; target access только для target claim. **Независимая единица:** acquisition/session/camera, person-frames вложены.

**Fixed/changed:** same images/GT/thresholds/decoder; отдельно normal chain, GT-person, GT-PPE, GT-owner interfaces. **GT/matching:** person geometry independent of predicted state; missed violating GT/abstentions остаются FN, unknown separate, unmatched/duplicate predictions under fixed ROI. Cases: neighbor/held helmet, two containing persons, hidden head/distant person/empty scene. **Процедура:** full chain→single oracle diagnostics→GT-anchored ledger→event replay выбранного repair.

**Метрики/экспозиция:** exact object AP/support, all-person localization/decision coverage, known/unknown/not-applicable, full-chain V recall, adjudicable precision с unresolved assertions, edge precision/recall и per-camera/person-time strata. Frame ratio не delivery burden. **Сохранить:** rosters/relations/visibility, pairs/unmatched reasons, every replaced boundary, all denominator bins/errors/regressions. **Исходы:** gain localizes conditional sensitivity, не guaranteed repair; unknown visibility может потребовать scope/view change. **Остановка:** prespecified cases/strata обработаны, все counts reconciled; новые hypotheses в dev. **Предел:** oracle не deployable/guaranteed upper bound, selected suite не prevalence. [F034](RAW_FACTS.md#f034)–[F048](RAW_FACTS.md#f048), [F258](RAW_FACTS.md#f258); [Q002](OPEN_QUESTIONS.md#q002)/Q003/Q017.

## E004 — Temporal policy selection/freeze
<a id="e004"></a>

**Решение/гипотеза:** выбрать persistence/cooldown/rearm; smoothing уменьшает excess, но может терять short/re-entry episodes и увеличивать delay. **Входы/доступ:** continuous dev truth/predictions, separate whole-group test, retained raw candidates below every planned threshold, owner D/reset/delivery semantics. **Независимая единица:** acquisition/camera/session, whole episodes protected.

**Fixed/changed:** freeze weights/preprocess/NMS/source/GT/matcher; vary prespecified joint threshold/dwell/unknown/hysteresis/cooldown list и search budget. **GT/matching:** same person/type/zone/causal evidence/deadline/end, closed one-to-one universe; GT не объединять под cooldown; uncertain/pre-existing/censored strata separate. **Процедура:** continuous replay каждой dev config→tradeoff table→owner choice→config hash lock→heldout run. Static PR sweep не симулирует changing event population.

**Метрики/экспозиция:** timely/event recall, semantic false/excess/strict unmatched отдельно, total source-hour/wall-hour burden при known schedule, TP delay quantiles+n рядом с misses/censoring/coverage; F1 только shared closed universe. **Сохранить:** все tried configs/results, state/timer/delivery traces, matches/reject reasons, selection/freeze/test access. **Исходы:** supported Pareto choice; unsupported/sparse choice остаётся provisional. **Остановка:** fixed search complete и locked test завершён; redesign переводит test в dev. **Предел:** dev optimum не unseen-camera/production proof. [F061](RAW_FACTS.md#f061)–[F073](RAW_FACTS.md#f073), [F104](RAW_FACTS.md#f104)–[F118](RAW_FACTS.md#f118), [F259](RAW_FACTS.md#f259); [Q001](OPEN_QUESTIONS.md#q001)/Q008/Q018.

## E005 — Continuous-video false delivered burden
<a id="e005"></a>

**Решение/гипотеза:** допустима ли bounded workload claim; curated positives/short drain могут скрывать excess/late records. **Входы/доступ:** immutable source I/H, frozen service, complete destination census/evidence anchors/retry/outstanding ledger, all-alert context/adjudication; independent reference дополнительно для normal/recall. **Независимая единица:** fixed corpus descriptive count; future rate требует отдельной acquisition/population/stochastic модели.

**Fixed/changed:** source/config/delivery identity/owner/E/C/drain до outputs; разные closes — named snapshots. **GT/matching:** semantic false, intentional reminder, duplicate/excess и useful unmatched разные labels; useful precision требует entire matching neighborhood. **Процедура:** reconcile source/logs→adjudicate every record→source-by-C и receiver-wall totals→independent reference/E010 при recall→unknown/outstanding publication.

**Метрики/экспозиция:** F_I(C)/H_I, excess/H_I, total/H_I; N(J)/(wall seconds/3600), coverage/masks/unknowns. Fixed independent U labels допускают [F/H,(F+U)/H], но changing matching — нет. Zero count — observed count/H; Poisson one-sided2.995732/H только с supported explicit model/fixed exposure. **Сохранить:** unions/epochs/timebases, census/adjudication/competing context, E/C state, by-close versions/deltas и interval assumptions. **Исходы:** complete all-alert review supports named source burden, не recall/verified-normal; low load при lost coverage не improvement. **Остановка:** fixed exposure/C, every visible item known/unresolved, residuals explicit; не stop при красивом bound. **Предел:** no eventual closure при pending retries, no future reliability из short zero/demo. [F003](RAW_FACTS.md#f003), [F074](RAW_FACTS.md#f074)–[F084](RAW_FACTS.md#f084), [F224](RAW_FACTS.md#f224)–[F234](RAW_FACTS.md#f234); [Q013](OPEN_QUESTIONS.md#q013)/Q014, [K002](CRITIC.md#k002)/K003.

## E006 — Paired A/B и причины улучшения
<a id="e006"></a>

**Решение/гипотеза:** принять named repair/recipe; expected change задан заранее, например fewer wrong-person alerts from owner correction. **Входы/доступ:** frozen A/B, identical untouched group-heldout footage/GT/exposure/matcher, selection history/budget и oracle logs. **Независимая единица:** camera/site/session под claim; recipe claim дополнительно full training/tuning run, не inference seed.

**Fixed/changed:** один isolated code factor при fixed weights/policy либо equal dev budgets для separately tuned systems, явно total-system comparison. **GT/matching:** identical unknown/censor/box/person/event protocols и все eligible units, не only matched persons. **Процедура:** same-input/reset runs→improved/regressed/unchanged/abstain/missing ledger→per-group counts→paired group resampling либо descriptive leave-one-group-out при few groups. Nonlinear metric recompute с namespaced draw copies; iid frame bootstrap не замена.

**Метрики/экспозиция:** B−A с units/sign, counts/denominators/exposure, recall/burden/delay/coverage, all groups, undefined resample fraction; fixed-artifact и recipe uncertainty отдельно. **Сохранить:** exact diff/artifacts/search/seeds/access, all outputs/disagreements/regressions, GT revisions applied both, draw/method/version. **Исходы:** consistent scope-limited gain supports fix; confounding/opposite group effects ограничивают interpretation. **Остановка:** fixed paired budget completed; новые fixes в dev. **Предел:** four groups/bootstrap draws не certified future coverage, oracle gain не unique cause/injury benefit. [F176](RAW_FACTS.md#f176)–[F206](RAW_FACTS.md#f206); [Q015](OPEN_QUESTIONS.md#q015)/Q017/Q018.

## E007 — Load, drops, freshness и recovery
<a id="e007"></a>

**Решение/гипотеза:** выбрать supported workload/queue policy; fast successes могут скрывать schedule lag/drops/stale queue. **Входы/доступ:** actual target/remote service, independent expected source schedule/GT, request/result/delivery clocks/IDs, bounded load/fault ladder/recovery predicate. **Независимая единица:** workload run cell для engineering behavior; repeated scene не новая quality sample.

**Fixed/changed:** freeze model/policy/source/truth; vary offered streams/cadence/resolution, batch/in-flight/burst по одному, затем bounded interactions/faults. Unpaced/paced/live отдельны. **GT/matching:** requested-footage known events during outage remain misses; missing GT/log follow-up unresolved. Temporal-support mapping frozen; иначе samples/gaps, не fabricated H_analyzed. **Процедура:** baseline→increased→overload→fault→recovery→predeclared drain/C, every attempt/logical terminal bin сохранён.

**Метрики/экспозиция:** offered/admitted/unique frames/s и batches/s, attempts/errors/timeouts/pending, on-time/all-selected, successful scheduled→ready и submit→ready quantiles+n с failures, per-camera backlog/gaps/requested/analyzed/fresh masks, full-window timely recall и source/wall burden. Capture age только verified map, иначе proxy/replay lag. **Сохранить:** workload/arrival trace/seed, target/environment, ledgers/masks/raw time, E/C queue state, fault location и first fresh recovery. **Исходы:** supports tested cell; lower latency с lost coverage marks overload; unknown placement blocks target capacity claim. **Остановка:** fixed ladder/windows/recovery/failure limit/C, residual work explicit. **Предел:** offline FPS не live multicamera/industrial reliability. [F146](RAW_FACTS.md#f146)–[F174](RAW_FACTS.md#f174), [F230](RAW_FACTS.md#f230); [Q008](OPEN_QUESTIONS.md#q008)–[Q013](OPEN_QUESTIONS.md#q013), [K002](CRITIC.md#k002).

## E008 — Unknown и неблагоприятные условия
<a id="e008"></a>

**Решение/гипотеза:** корректно ли observable scope/operator status; hidden body/darkness/gap может стать false safe/violation/stale silence. **Входы/доступ:** annotated adverse clips/manual, source/session logs, actual destination/UI если claim о presentation, bounded mock/real fault input. **Независимая единица:** acquisition scenario/session; curated suite не prevalence sample.

**Fixed/changed:** baseline media/policy/manual; один condition либо отдельные real strata, synthetic darkening/reencoding маркировать sensitivity. **GT/matching:** GT unknown/model abstain/technical unavailable/not-applicable различны; known V stays denominator, unknown correctness не выдумывать; continuity/reset независимо. **Процедура:** hidden head/neighbor/novel view/darkness→occlusion return→disconnect/stale reply→trace raw state/timers/status/recovery.

**Метрики/экспозиция:** known coverage/error/misses, unsupported assertions on unknown, reason/time counts, stale/unavailable status, duplicate/recovery delay, requested/fresh coverage по [E005](OPEN_QUESTIONS.md#e005)/E007. **Сохранить:** original/synthetic lineage, GT/context, transitions/reset logs, request/delivery/display evidence. **Исходы:** correct explicit unknown supports conformance; unsupported confidence требует policy/view change; absent display logs limits claim. **Остановка:** declared suite complete, each failure issue recorded. **Предел:** abstain не detects all OOD, silence не safety, selected cases не rate. [F008](RAW_FACTS.md#f008)–[F018](RAW_FACTS.md#f018), [F112](RAW_FACTS.md#f112)–[F130](RAW_FACTS.md#f130), [F172](RAW_FACTS.md#f172); [Q002](OPEN_QUESTIONS.md#q002)/Q003/Q013.

## E009 — Independent annotation agreement
<a id="e009"></a>

**Решение/гипотеза:** можно ли reproducibly label state/owner/onset; disagreement может отражать visibility/manual. **Входы/доступ:** permitted originals/context, approved requirements, two independent annotators, frozen manual и prespecified reliability sample; device не нужен. **Независимая единица:** sampled scene/session/camera; common-roster classification отдельно от finding persons.

**Fixed/changed:** pilot discussion затем fresh frozen-manual pass; revision — новая version и affected-scope reannotation. **GT/matching:** save raw independent labels; common-roster table versus one-to-one person finding/localization, unknown label versus workflow-missing, unmatched persons retained; temporal bounds/censoring не midpoint. **Процедура:** pilot→blinded pass→full contingency/finding/boundary review→adjudication/reasons/remaining unknown.

**Метрики/экспозиция:** Po/full rare-state counts, выбранные kappa/alpha implementation/assumptions, missing/unknown, matched/unmatched/IoU, jointly covered duration и boundary differences only observable pairs; sample method/groups/exposure/effort. **Сохранить:** manual/sample/draw/raw labels/timestamps, matches, adjudicated versions/reasons. **Исходы:** narrow reproducible state enables comparison; persistent hidden criteria требуют scope/view/external change. **Остановка:** selected independent sample complete и disagreements classified/unresolved, не repair до высокого coefficient. **Предел:** agreement не truth/safety/learnability или model score. [F013](RAW_FACTS.md#f013), [F017](RAW_FACTS.md#f017)–[F018](RAW_FACTS.md#f018); [Q002](OPEN_QUESTIONS.md#q002)/Q004.

## E010 — Probability-sampled continuous reference review
<a id="e010"></a>

**Решение/гипотеза:** оценить fixed-corpus onset/missed totals при budget; alert-only/any-overlap может смещать findings. **Входы/доступ:** immutable complete source frame/context/log follow-up, frozen full-run outputs, independent reviewers/manual, fixed allocation/draw с context reserve. **Независимая единица:** randomized disjoint core при stratified SRSWOR; contents/events не обязаны iid. Future-camera claim отдельный.

**Fixed/changed:** core/strata/N/n/seed/outcome frozen, every core positive pi, non-alert cores selectable; service не rerun/reset по cores. **GT/matching:** predictions-hidden full-core discovery, unique half-open onset owner; context расширять до owner/opportunity/component closure, не extra samples. Onset ambiguity/nonresponse/missing closure/censoring unresolved, не replacement/zero. **Процедура:** enumerate sorted IDs→uniform permutation per stratum→save draw→review every selected core→close context→E/T/M→HT totals + separate ratio; interval только supported design/approximation.

**Метрики/экспозиция:** pi=n/N и pairwise law, Ehat/That/Mhat=Σy/pi, rates/full source H; Rhat if Ehat>0 generally biased; FPC variance requires n_h≥2 noncertainty, certainty zero; raw contributions/unknown/context cost. Zero miss-bearing sample supports hypergeometric core bound, не episode bound без external cap. Не складывать dual-frame totals. **Сохранить:** full frame/allocation/permutation/pi, reference-first labels/context/masks/competing edges/pairs, per-core values/estimator/version. **Исходы:** complete values дают unbiased fixed-corpus totals; sparse ratio/unknowns могут блокировать useful interval/point claim. **Остановка:** fixed allocation complete, selected unresolved retained; extra random phase separately specified. **Предел:** randomization не исправляет human misses/future sites; possible union bound не attainable worlds. [F004](RAW_FACTS.md#f004), [F235](RAW_FACTS.md#f235)–[F249](RAW_FACTS.md#f249); [Q014](OPEN_QUESTIONS.md#q014)/Q015, [K004](CRITIC.md#k004)/K005.

## E011 — Lineage/split conformance
<a id="e011"></a>

**Решение/гипотеза:** допустим ли independent test; filenames/frame splits могут cross protected source/event/domain. **Входы/доступ:** originals/hash/time/camera/site/session/transform records, intended claim/context windows, candidate frames/checkpoint provenance; device не нужен. **Независимая единица:** protected dependency component/outer population group.

**Fixed/changed:** freeze forbidden crossing relations/claim; compare existing/component-aware split без model-score selection. **GT/matching:** adjudicated parent/same-event links, IDs/interval overlaps и reviewed near-duplicate candidates с pinned method; similar static background не automatic duplicate. **Процедура:** lineage→graph/components→cross-ID/time audit→candidate review→window purge→group/exposure table→freeze corrected split/narrow claim.

**Метрики/экспозиция:** confirmed crossing components/pairs и reviewed candidates/audited units (не universal leakage prevalence), independent groups/positives/source hours per split, unknown provenance. **Сохранить:** old/new manifest/hash, transforms/links/evidence/candidate decisions, split diff/exclusions/pretraining limits. **Исходы:** crossing требует regroup/recollect; none found supports audited method only; giant component значит no requested holdout. **Остановка:** known protected relations/windows checked, unknowns logged. **Предел:** не certifies undisclosed pretraining/representativeness/model quality. [F085](RAW_FACTS.md#f085)–[F103](RAW_FACTS.md#f103); [Q005](OPEN_QUESTIONS.md#q005)–[Q007](OPEN_QUESTIONS.md#q007).

# Адресные передачи соседним исследованиям

Это подготовленные материалы, без внешних сообщений и запуска соседних research. Завершённые соседние отчёты в этой папке не предоставлены.

| Адресат | Конкретное основание и решение | Следующий вопрос/артефакт |
|---|---|---|
| datasets | [F008](RAW_FACTS.md#f008)–[F018](RAW_FACTS.md#f018), [F085](RAW_FACTS.md#f085)–[F103](RAW_FACTS.md#f103), [F239](RAW_FACTS.md#f239)–[F244](RAW_FACTS.md#f244); [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S043](SOURCES.md#s043), [S131](SOURCES.md#s131). Box labels не дают owner/event truth; lineage и onset ownership определяют holdout/audit. | [Q002](OPEN_QUESTIONS.md#q002)/Q005/Q014: originals, completeness/visibility/relations, source/camera lineage, adjoining context; [E009](OPEN_QUESTIONS.md#e009)–[E011](OPEN_QUESTIONS.md#e011). |
| violation_methods | [F034](RAW_FACTS.md#f034)–[F073](RAW_FACTS.md#f073), [F258](RAW_FACTS.md#f258)–[F265](RAW_FACTS.md#f265); [S013](SOURCES.md#s013), [S016](SOURCES.md#s016), [S020](SOURCES.md#s020), [S029](SOURCES.md#s029). Object/owner/zone/temporal state — разные truth/interfaces. | [Q003](OPEN_QUESTIONS.md#q003)/Q008/Q017: observable misuse, safe-reset/unknown/rearm, oracle adapters; [E003](OPEN_QUESTIONS.md#e003)/E004. |
| training_strategy | [F096](RAW_FACTS.md#f096)–[F118](RAW_FACTS.md#f118), [F175](RAW_FACTS.md#f175)–[F189](RAW_FACTS.md#f189); [S049](SOURCES.md#s049), [S052](SOURCES.md#s052), [S054](SOURCES.md#s054), [S108](SOURCES.md#s108). Full-policy calibration/selection на dev, paired group comparison и equal search budgets нужны до claim улучшения. | [Q006](OPEN_QUESTIONS.md#q006)/Q015/Q018: permitted adaptation, independent groups, search/access history и freeze record; [E004](OPEN_QUESTIONS.md#e004)/E006. |
| model_stack | [F131](RAW_FACTS.md#f131)–[F145](RAW_FACTS.md#f145), [F217](RAW_FACTS.md#f217)–[F221](RAW_FACTS.md#f221); [S070](SOURCES.md#s070), [S072](SOURCES.md#s072), [S074](SOURCES.md#s074), [S124](SOURCES.md#s124). Actual tensor transforms/NMS и compiled graph lineage нужны раньше tolerance/quality claim. | [Q007](OPEN_QUESTIONS.md#q007)/Q011: weights/export/compiler/calibration schemas/hashes и raw intermediates; [E002](OPEN_QUESTIONS.md#e002). |
| linq_platform | [F002](RAW_FACTS.md#f002), [F216](RAW_FACTS.md#f216)–[F223](RAW_FACTS.md#f223); [S121](SOURCES.md#s121)–[S126](SOURCES.md#s126). Public blocking sync documented, actual package/remote/placement/time не verified; TLM estimate отдельно. | [Q009](OPEN_QUESTIONS.md#q009)/Q010/Q012: wheel/working sample, endpoint/completion states, timer/fallback/placement evidence; [E002](OPEN_QUESTIONS.md#e002)/E007. |
| video_architecture | [F146](RAW_FACTS.md#f146)–[F174](RAW_FACTS.md#f174), [F229](RAW_FACTS.md#f229)–[F234](RAW_FACTS.md#f234); [S082](SOURCES.md#s082), [S091](SOURCES.md#s091), [S093](SOURCES.md#s093), [S095](SOURCES.md#s095), [S128](SOURCES.md#s128). Independent expected work, original release/source anchors, clock domains, per-ID outcomes и E/C ledger делают latency/coverage воспроизводимыми. | [Q008](OPEN_QUESTIONS.md#q008)/Q010/Q013: actual source support mapping, timestamp provenance, logical/attempt/visible IDs, outstanding/retry closure; [E005](OPEN_QUESTIONS.md#e005)/E007. |
| operator_product | [F003](RAW_FACTS.md#f003), [F229](RAW_FACTS.md#f229), [F230](RAW_FACTS.md#f230), [F259](RAW_FACTS.md#f259); [S127](SOURCES.md#s127), [S128](SOURCES.md#s128). Semantic truth, timely usefulness, duplicate/reminder и visible interruption различаются; silent/unknown/unavailable не safe. | [Q001](OPEN_QUESTIONS.md#q001)/Q003/Q013: active-after-end/D, reminder utility, unknown action, durable versus displayed endpoint; [E004](OPEN_QUESTIONS.md#e004)/E008. |
| market_deployment | [F074](RAW_FACTS.md#f074)–[F084](RAW_FACTS.md#f084), [F229](RAW_FACTS.md#f229), [F242](RAW_FACTS.md#f242); [S036](SOURCES.md#s036), [S037](SOURCES.md#s037), [S038](SOURCES.md#s038), [S131](SOURCES.md#s131). Natural exposure/prevalence/population ограничивают перенос demo; нет invented economics/injury coefficient. | [Q001](OPEN_QUESTIONS.md#q001)/Q015: deployment camera/shift mix и acceptable review burden; actual source/wall burden и последствия пропуска требуют своих входов. |
| hackathon_strategy | [F001](RAW_FACTS.md#f001), [F207](RAW_FACTS.md#f207)–[F215](RAW_FACTS.md#f215); [S119](SOURCES.md#s119), [S120](SOURCES.md#s120), [S124](SOURCES.md#s124). 45 часов publication→upload; smoke/demo/independent/actual-target evidence различаются. | [Q001](OPEN_QUESTIONS.md#q001)/Q009: original case/submission interpretation, actual target run. Для защиты traceable positive, negative/unknown/recovery и artifact IDs; cached output маркировать recorded. |

# Условные маршруты в 45-часовом контексте

Это порядок по доступным доказательствам, не обещание часов разметки/FPS/statistical power. Сначала truth/manifest/evaluator, затем одна полезная цепочка и actual target, затем freeze/comparison; команда сохраняет buffer до submission. Если official scoring появляется поздно, reproduce mandated score отдельно, не заменяя им supplementary useful-warning checks.

| Доступные материалы | Последовательность и достигаемый уровень | Остаток неизвестного |
|---|---|---|
| Images и weights | [E011](OPEN_QUESTIONS.md#e011) lineage→[E009](OPEN_QUESTIONS.md#e009) annotation scope→[E001](OPEN_QUESTIONS.md#e001) detection fixtures→object/person [E003](OPEN_QUESTIONS.md#e003) при соответствующем GT; [E002](OPEN_QUESTIONS.md#e002) доступные stages | Continuous events/natural burden/live age/target execution без доступа. |
| Небольшие независимые clips | Whole-group split/manual→[E003](OPEN_QUESTIONS.md#e003)/E004 dev→freeze→[E006](OPEN_QUESTIONS.md#e006) heldout с raw group counts/unknown/censoring | Few-camera generalization и natural operator workload. |
| Длинное partly unlabelled video | Complete all-alert [E005](OPEN_QUESTIONS.md#e005); independent [E010](OPEN_QUESTIONS.md#e010) или census для onset/missed totals; source/wall cohorts отдельно | Recall без complete sampled outcomes; future population без [Q015](OPEN_QUESTIONS.md#q015). |
| Несколько cameras/shifts/sites | Claim-specific [E011](OPEN_QUESTIONS.md#e011)→paired group [E006](OPEN_QUESTIONS.md#e006); fixed-corpus [E010](OPEN_QUESTIONS.md#e010) отдельно | Representativeness, rare positive-bearing groups, undisclosed pretraining. |
| Поздний official evaluator | [E001](OPEN_QUESTIONS.md#e001) mandated semantics, immutable predictions и official result; supplemental operational view отдельно | Official score не задаёт неизвестный industrial endpoint. |
| Limited/unstable remote LinQ | [Q009](OPEN_QUESTIONS.md#q009)/Q010→[E002](OPEN_QUESTIONS.md#e002) completed smoke/parity→[E007](OPEN_QUESTIONS.md#e007) pacing/fault/recovery с IDs/close | Pure device time/placement, если не exposed; CPU/RTX не target proof. |
| Только staged/demo footage | [E001](OPEN_QUESTIONS.md#e001)/E003/E008 conformance, traceable demonstration и labeled recording | Independent field quality/natural FP/hour/injury reduction. |
| Невидимый PPE/action | [E009](OPEN_QUESTIONS.md#e009) scope/unknown→[E008](OPEN_QUESTIONS.md#e008) status/action; conditional known-state quality с coverage | Hidden physical compliance не восстанавливается silence/non-detection. |
