# Открытые вопросы и программа проверки

Состояние на 2026-10-23, Europe/Moscow. Два поисковых захода завершены. Никакой model/export/import/PTQ/QAT/compiler/device benchmark не выполнен. Полный кейс сохранён, но grant, exact stack, выбранные weights и независимый GT не получены. Ниже вопросы после W2; это отправная точка отдельной разрешённой практической работы. Подготовленные запросы никому не отправлялись.

Для каждого Q различаются: DOC/CODE — ещё можно уточнить по versioned публичному материалу; ARTIFACT/ACCESS — нужен фактически выданный объект; CPU-TEST/SDK/DEVICE — нужен выполненный тест; DECISION — значение принимает команда/постановщик. Поиск общего обзора не закрывает ARTIFACT/DECISION. P0 блокирует дорогой путь или соответствующий claim, P1 меняет выбор/силу оценки, P2 нужен при намерении воспроизводить чужой результат.

## Спросить у инженеров LinQ сейчас

1. **Q001–Q002:** какой доступ реально выдан и какой один matched bundle/model example является supported? Нужны версии и hashes, права custom build/upload, actual SKU/target, инструкция и unchanged known-good input/output.
2. **Q004–Q005:** какой именно importer стоит, как отображаются tensor values и ports, какие opsets/attributes и outputs поддержаны, как выполнить float ONNX→TF до квантования?
3. **Q006–Q007:** что percentile изменяет в этом release и какой численный контракт compiler принимает от QAT/QDQ/encodings/FP islands? Нужны effective settings и минимальный preservation proof до GPU.
4. **Q008–Q009:** что означает completion `.run/.sync` и FULL/PRE/POST/RAW у выданного ABI, какие user/raw descriptors/codec и per-job device/placement evidence реально доступны?
5. **Q010–Q011:** что принимает video/file service, как сохраняются frame identity/PTS/конец файла, как считаются пропуски и где уведомление считается доставленным? CPU preprocessing/NMS/rules и дополнительная neural pose/ReID граница требуют явного согласования.

Точный D/сценарии/цену ошибок принимает команда с постановщиком (Q012); независимые размеченные clips и права получает data owner (Q013), а не SDK-инженер по умолчанию.

<a id="Q001"></a>
## Q001 — Фактический grant и доступная граница управления

**P0; ACCESS+ARTIFACT; владелец platform lead/организатор.** VM shell, restricted runtime или catalog service? Разрешены ли custom weights, compile, `.qm/.tpu`/ONNX upload, files и raw outputs; каковы quotas/допустимая нагрузка? Известно: кейс с.8 обещает VM и сервис, публичный guide показывает локальный tensor runtime; устный CPU+TPU/file-upload — working assumption. Искали в кейсе, guide2025, официальных pages, W1-13/15 и W2-01/05/06. Причина unknown: grant/access manual не передан. Решение: какой путь вообще исполним; нет custom grant — не тратить GPU на неразвёртываемую модель. Закрытие: выданная инструкция+capability inventory и допустимый unchanged smoke, не факт существования URL. Связи: F001, F205, F234, F245; K001/K007/K008/K011; E001/E003.

<a id="Q002"></a>
## Q002 — Один совместимый SDK/native/target bundle

**P0; ARTIFACT+SDK+DEVICE; platform lead/LinQ engineer.** Нужны OS/arch/Python, фактические wheel filenames/versions/hashes и imported module paths Framework/importer/quantizer/compiler/pytpu, TF/ONNX/NumPy lock, libtpu/driver/firmware/SKU, compatibility `.tpu` и matched manual. Известны guide2025/Python3.11, live Python3.8, pytpu15.0.24>=3.6 и vendor benchmark16.18.6/2026.8.43; это разные scopes. W2-01 свежо получил sdist, исправил stale README обобщение, но wheel→manual mapping не найден. Причина: actual environment не выдана. Решение: исключить перебор поколений и скрытые retries. Закрытие: manifest+hashes+поддержанный import и completed known-good device inference; один import слаб из-за lazy CDLL. Связи F197–F205/F238; K001/K011; E001/E003.

<a id="Q003"></a>
## Q003 — Exact model/source/output contract

**P0; ARTIFACT+CPU-TEST; model lead/model_stack.** Какие checkpoint/config/source commits, partial-load keys, EMA/fused state, classes/nc/order, task/head/end2end, skeleton/K/D/visibility, export flags/shape/batch/dtypes и external dependencies реально выбраны? W1-01/02/04 и W2-02 дают source-derived пример, но weights отсутствуют. Нельзя восстановить class meaning по C=84 или filename. Причина unknown: artifact не предоставлен. Решение: создать настоящий source baseline, применять decoder только к установленному head. Закрытие: immutable bundle/лицензия/load log+source repeated outputs; catalog без source сужает claim до service-to-GT. Связи F004–F012/F206–F211/F243; K003/K010; E001/E002/E004.

<a id="Q004"></a>
## Q004 — Identity и semantic mapping фактического ONNX importer

**P0; ARTIFACT+SDK+CPU-TEST; SDK/import owner.** Нужны distribution/module/callable identity, version/build/hash, signatures, mapping keys/direction/ports/layout/cuts и float executor. Guide называет `onnx_direct.onnx_to_tf`; pinned build пробует два imports/kwargs, strips port и выбирает первый output. W2-02 exact-name/PyPI/GitHub поиск не дал реализации; 404 публичного package endpoint не доказывает отсутствия private wheel. Причина: supplier implementation/bundle не выдан. Решение: отделить ONNX→TF от quantizer, сохранить все required outputs. Закрытие: реальные mapping+IO descriptors и E005 Identity/Transpose/Split, затем actual neural float gate. Связи F212/F213; K002; E005.

<a id="Q005"></a>
## Q005 — Operator/IR/opset/shape/target/preset constraints

**P0 для custom route; ARTIFACT+SDK; compiler lead/LinQ.** Какие IR/opsets/domains/dtypes/attrs, static/dynamic B/H/W, batches/memory/multi-output допустимы? Каков actual `as_graph` default/explicit target, save/from_quantized_model schema и resolved DEFAULT/STAGING/O1/O5? Guide extraction имеет platform discrepancy и нет visual PDF verification. Default opset13 стороннего скрипта не maximum LinQ. W2-01/02/06 сузили точные места, actual support неизвестен. Закрытие: matched signatures/operator matrix/config dumps, original/corrected PDF и compile report для concrete inventory, без угадывания aliases. Решение: минимальная адресная specialization/lowering либо reject route. Связи F159–F185/F200–F202/F241–F244; K001/K002/K008; E004/E005/E007/E011.

<a id="Q006"></a>
## Q006 — Percentile: requested, passed и effective

**P0 до sweep; ARTIFACT+SDK+DEVICE; quantization lead/SDK engineer.** Точный object weights/activations/both, formula/tails/domain/units, granularity/axis, порядок относительно weight quantization, thresholds/scales dump и cache semantics? Guide связывает параметр с weights/default100; `RegularModel.calibrate` code ловит любой TypeError и повторяет default. W2-03 targeted vendor search не дал current definition. Причина: numerical implementation неизвестна, документационная формула отсутствует. Решение: не называть sweep различными activation policies. Закрытие: matched definition+fresh successful calls и E006 2×2, supported frozen-weight intervention либо честное confounding. Изменившиеся activation thresholds сами по себе не доказывают прямой activation-percentile. Связи F214–F216/F175; K004; E006.

<a id="Q007"></a>
## Q007 — Consumer численного контракта для recovery/QAT/mixed precision

**P0 до training; ARTIFACT+SDK+DEVICE; quantization/compiler owners.** Поддерживается preserve external QDQ/sidecar, native matching QAT simulator или только native PTQ? Какие W/A/bias/accumulator types/scales/zp/axis, rounding/clipping/saturation/requantization, fusion, exclusions/FP islands/placement, возможность freeze/bypass recalibration? W1-08/09 и W2-03 открыли реальные APIs иных backend, но vendor-specific consumer не найден. Причина: actual release contract отсутствует; compile acceptance недостаточно. Решение: запускать только передаваемый recovery; AdaRound иной grid не сохраняет обещанный эффект. Закрытие: official matched recipe+known-good micrograph+E007 preservation до GPU. Отсутствие evidence не запрет функции. Связи F221–F224/F230–F233/F239; K005/K006; E007/E011.

<a id="Q008"></a>
## Q008 — Completion и numeric user/raw boundary текущего ABI

**P0 до timing/parity claim; ARTIFACT+SDK+DEVICE; runtime engineer.** Что гарантируют `.run/.sync`, output readiness/barrier, status/error/timeout/cancel/reset/retry/thread safety? Где PRE/POST, как устроены user/raw tensors/packing/padding/scales/codec? Исторический15.0.24 зовёт native run→reads→status; guide называет sync blocking, `.run` из этого не следует. RAW mode и RAW program различны; codec требует internal `tpu_tlm_is`. Причина unknown: native source/current manual не получены. Закрытие: matching manual/descriptors+completed known-input trace и supported FULL↔RAW+codec check. Решение: не измерить enqueue и не сделать double rescale/astype вместо codec. Связи F238–F240; K011; E003/E006/E007/E010.

<a id="Q009"></a>
## Q009 — Достаточное device и neural-placement evidence

**P0 для LinQ claim; ARTIFACT+DEVICE+DECISION; platform lead/постановщик.** Какие artifact/session/device/input/completion/output traces и compiler/partition/profiler доступны, где исполняются дополнительные pose/ReID/temporal NN, допустим ли neural CPU fallback? W1-12/15 и W2-05 определяют evidence levels. Inventory/label/utilization не proof завершения/всего graph. Причина unknown: actual granted observability ещё неизвестна; пока это DATUM_MISSING, не уже установленное NOT_EXPOSED. Закрытие: E003/E007 trace; закрытый service — operator attestation с IDs отдельно от собственного observed placement. Решение: честная область LinQ исполнения. Связи F141/F195/F223/F238/F239; K005/K010/K011; E003/E007/E010/E012.

<a id="Q010"></a>
## Q010 — Серверный media/preprocess/output interface

**P0; ACCESS+ARTIFACT+CPU-TEST/SDK; video_architecture/platform.** Container/codec/profile/bit depth/limits, file identity receipt, decode rotation/SAR/colorspace, RGB/BGR/range/layout/quant input, built-in preprocessing/NMS/dequantization, all output names/valid-count? Guide local tensors не задаёт file service. W1-05/15 и W2-02 показывают backend-dependent transforms, API не выдан. Закрытие: actual contract+one decoded/tensor/output dump G01 и E002, полученное ограничение видимости явно записать. Решение: same tensor либо limited black-box comparison; не менять model в ответ на геометрию. Связи F048–F057/F207–F211; K002/K003/K011; E002/E003/E008.

<a id="Q011"></a>
## Q011 — Source time, scheduling, delivery и closure

**P0 для operational claim; ACCESS+ARTIFACT+TEST+DECISION; video_architecture/event owners.** Source PTS/timebase/epochs, VFR/drops/reorder/late replies, retry idempotency, file reset/drain, clock mapping/uncertainty, alert-visible boundary, allowed load? W1-11/12/15 и W2-05 отделили local runtime timer от E2E и нашли batch/warmup counter seam. Причина: service trace/policy не предоставлены. Закрытие: actual terminal ledger+clock mapping+E009/E010 causal replay и measured schedule. Решение: sampling/confirmation policy и честный latency denominator. Связи F119–F141/F186–F196/F240; K010/K011; E009/E010/E012.

<a id="Q012"></a>
## Q012 — Подписанный acceptance policy и supported scope

**P0; DECISION; risk/product owner+CV/evaluation lead, D уточнить у постановщика.** Какие сценарии/исключения, actor/episode/onset/end/observable-evidence semantics, deadline, must-pass IDs, absolute floors/caps, δ/non-inferiority/equivalence, α/sidedness/multiplicity/stop rules принимаем до winner selection? Кейс не задаёт универсальных процентов/1FPS. W2-07 подготовил AR01, решения отсутствуют. Закрытие: versioned approved AR01 policy, заранее заполненные required endpoints и limits; никакая публикация не назначает цену ошибки. Решение: настоящий PASS/FAIL вместо условной формы. Связи F001/F138–F141/F247–F250 и RAW AR01; K009/K010; E001/E008–E012.

<a id="Q013"></a>
## Q013 — Licensed independent GT и continuous negatives

**P0; ARTIFACT+DATA; data/annotation owners+rights holder.** Где source clips/frames с camera/site/session/incident lineage и правами, независимые detection/pose/person/event labels, uncertainty/adjudication, source intervals и complete follow-up? W1-01/07/10/12 и W2-07 задают pack, коллекция NOT_COLLECTED. Source predictions не GT; curated negatives не дают natural-stream burden. Закрытие: immutable rights/media/GT/split manifests и review protocol, затем измерение. Решение: absolute quality, recall silence и ложные/camera-hour. Связи F009–F012/F091–F118/F138–F141/F249; K009/K010; E001/E008/E009/E010.

<a id="Q014"></a>
## Q014 — Независимость, finite roster и статистическая сила

**P1; DATA+DESIGN+TEST; evaluation/data lead.** Что за population/estimand, independent trial/cluster, camera mix/selection, required slices, actual n и exposure? W2-07 дал точные условные bounds, но counts не измерены, dependence неизвестна. При zero misses iid bound `1−α^(1/n)`; при homogeneous Poisson zero false `−lnα/T`; n=0/T=0 undefined. Нельзя подставить adjacent frames, произвольный n_eff или “300 клипов” без lineage. Закрытие: design/manifest+complete ledger+предобъявленный stopping; few clusters — descriptive/INCONCLUSIVE вместо выдуманного exact CI. Решение: scope claim и сбор дополнительных независимых сессий. Связи F138/F139/F246–F250; K009/K010; E008/E009/E012.

<a id="Q015"></a>
## Q015 — Наблюдаемость промежуточных границ

**P1; ARTIFACT+SDK; importer/compiler/evaluation leads.** Доступны ли float target, quantized reference/TLM, raw/intermediate outputs и reports; как instrumentation меняет fusion? W1-03/06/12/14 и W2-02/03 показывают методы, actual API неизвестен. Закрытие: granted interface inventory+supported dump на одном artifact, сравнение debug/unchanged deployment; after grant пометить truly NOT_EXPOSED с evidence. Решение: отделить import/quant/compiler либо назвать переход confounded, сохранив возможный end-to-end GT gate. Связи F027–F047/F206–F224; K002/K005/K011; E004–E008.

<a id="Q016"></a>
## Q016 — Практическая пригодность запасных routes

**P1, P0 перед выбором fallback; ARTIFACT+CPU-TEST+SDK+DEVICE; model/export/platform owners.** RT-DETR-l/U8.3.230 требует GridSample16/TopK/attention; RTMPose-m/M1.3.2+MMDeploy1.3.1 требует dependency override/registry/metadata smoke,2 outputs/GAU/ScaleNorm, crop schedule. W2-06 закрепил exact source cards, bytes weights/hash и matched lock/target не получены. Default MMDeploy requirements M1.0.0 не совпадает с newer input_center/scale contract; flip test bypass — иной baseline. Закрытие: E011 route admission+E004/E005/E007; unsupported boundary без equivalent lowering — stop, не QAT. Решение: prefer/reject конкретную альтернативу либо реально доступный vendor artifact. Связи F241–F245; K008; E011.

<a id="Q017"></a>
## Q017 — Реальный бюджет correction/QAT на выбранной машине

**P1; ARTIFACT+разрешённый GPU pilot; training_strategy/model lead.** Peak allocated/reserved VRAM/RAM, steady step time, caching/eval/export/compile/target overhead, один/два GPU/DDP и provider rate? W1-08 даёт cost model, статьи не прогноз 3090/LinQ; две GPU не общий пул памяти. Причина: model/data/target/host не выбраны, pilot не запускался. Закрытие: E007 перед E011, approved bounded pilot с rollback/checkpoints/BN-observers, measured cost ledger; test закрыт. Решение: продолжить/откатить/сменить исполнимую модель. Связи F088–F102/F230/F231; K005/K006; E011.

<a id="Q018"></a>
## Q018 — Чужие LinQ result artifacts и original table bytes

**P2, P0 если цитировать measured author accuracy; ARTIFACT+DOC; platform lead/автор benchmark через команду.** Для TinyYOLO3 отдельно нужны program/metadata/source-model hashes, env, predictions/COCO metrics, native MLPerf config/summary/detail/stdout/stderr/exit code/run ID/roster; self-build YOLOv8 отдельный bundle. W2-05 complete tree/release/Actions scope не содержит указанных logs; это не отрицание run. Vendor presentation numbers получены extraction, PDF визуально не проверен; нужны original bytes/footnote/input shapes/precision/timing scope и независимость HPQ. Закрытие: attributable raw artifact либо цитирование только limited vendor report, не fabricated source-target pair. Решение: сила стороннего сравнения/демо. Связи F234–F240; K007/K011; E012.

<a id="Q019"></a>
## Q019 — Нативная работа ORT automatic mixed precision на выбранном host

**P1 только при выборе этого диагностического tool; CODE+CPU/GPU-TEST; local runtime owner.** Какой entry point converter1.16.0, ORT wheel/version/build/providers/optimized graph реально работает? W2-03 нашёл отдельный provider-selectable model-path API, ModelProto path остаётся CPU; ORT1.23.2 вставляет FP32 CPU casts для части FP16 nodes. Совместная работа не запускалась, converter не pin ORT; live docs не release contract. Закрытие: exact lock+один supported fixture+placement/optimized graph на целевом provider до search. Решение: не считать CPU validation native FP16/CUDA/LinQ proof. Связи F225–F229; K005; E011 (опциональная local tooling admission).

<a id="experiment-program"></a>
## Единая программа E001–E012 — все PROPOSED / UNRUN

Статусы **всех** E сейчас: **UNRUN; actual measured values none**. Это спецификация будущей разрешённой практической работы, не выполненный пилот и не право устанавливать SDK/арендовать GPU/входить на сервер автоматически. `PASS(scope)` возможен только после actual complete run. `FAIL` — подтверждённое нарушение invariant/предпринятого budget. `HOLD` — нет input/access/approved policy. `INCONCLUSIVE` — измерение есть, но недостаточно precision/coverage/assumptions. `UNAVAILABLE` — граница/операция фактически недоступна; будущий неизвестный grant ещё не NOT_EXPOSED. HOLD/INCONCLUSIVE/UNAVAILABLE не превращаются в общий PASS.

Общие prerequisites: immutable source/candidate/decoder/preprocess/tracker/rule/evaluator bundles; один frozen sample manifest с rights/group/split/PTS и independent GT отдельно от model outputs; accepted input scope; owner и acceptance-policy version. Numeric tolerances выводят на dev из repeatability/единиц/риска, quality floors/caps/δ/D/α заранее принимает Q012. Ни один tutorial default не норматив. Каждая ступень хранит adjacent и source→final deltas; скрытую границу называют confounded, не присваивают фиктивный float-target PASS.

### Будущие sample IDs

Имена `manifest.select(role=...)` ниже — **селекторы будущего frozen manifest**, а не существующие sample IDs/файлы. До любого E001 owner материализует ordered ID lists и hash; реальный ID нельзя сочинить в отчёте. Roles: `normal_person_machine`, `empty`, `tiny_phone_or_ppe`, `odd_landscape`, `odd_portrait`, `boundary_zone`, `occlusion_ownership`, `pose_critical`, `short_event`, `fall_or_lying`, `persistent_incident`, `two_episodes_reentry`, `hard_negative_continuous`, `vfr_gap_reconnect`, `file_end`. Positive event type используется только если scope/GT подтвердили его. Synthetic decoder/geometry/index fixtures имеют отдельный `origin=synthetic`, не industrial benchmark. Calib/dev/test groups не пересекаются по incident/session/camera согласно design; crops/augments/синхронные камеры наследуют lineage. Небольшой debug roster не становится независимым test.

**Три первых практических проверки:** E002 (input/output/geometry admission), E003 (unchanged LinQ completed smoke), E005 (same-tensor float ONNX→TF mapping после E004). E001/получение Q001–Q003 — их обязательная подготовка. Если разрешён только catalog, E005 честно UNAVAILABLE, а следующий путь E008/E009 black-box service-to-GT.

<a id="E001"></a>
### E001 — Freeze provenance, data splits и acceptance record

**Цель/решение:** получить проверяемый baseline и запретить некорректное сравнение до вычислений; owner model+data+evaluation leads. Inputs/access: source checkpoint/config/license/load log/runtime, chosen route/grant, source files/rights/GT; Q001–Q003/Q012–Q014. Baseline→target: полученные artifacts→immutable comparison contract/AR01; аппаратного этапа нет. Samples: все будущие roles с группами и ordered IDs.

**Процедура:** записать hashes source/sidecars/config/classes/skeleton/dependencies, eval/fusion/EMA/partial-load; media→pixels→tensor geometry+PTS lineage; назначить train/calib/dev/independent test до sampling/fit; проверить exact/near duplicates и связанные multicamera incidents; утвердить scope/metrics/units/budgets/stop rule. Для incomplete history сохранить known since acquisition, pretraining leakage UNKNOWN. AR01 разделяет TEAM_DECISION_PENDING/DATUM_MISSING/NOT_EXPOSED/MEASURED; сейчас MEASURED none.

**Наблюдаемые выходы:** versioned signed contract, actual manifests/hashes/rights, group audit, missing list, rollback bundle identity; TPU proof N/A. **PASS:** все required поля этого freeze получены и approved до выбора winner; **FAIL:** обнаруженная запрещённая leakage/identity inconsistency; **HOLD:** отсутствует model/GT/policy; unknown pretraining остаётся ограничением. Возможный исход — frozen narrow debug pack при population HOLD. PASS не доказывает численную parity/accuracy/device и не устраняет неизвестную историю весов. Основания F004–F012/F246–F250; K010.

<a id="E002"></a>
### E002 — Input/output, decoder и geometry admission smoke

**Цель/решение:** отличить adapter/geometry ошибку от model loss; owner adapter/CV lead. Inputs: E001, actual service/SDK IO contract, pinned head/preprocess/NMS/inverse, permitted local CPU environment. Stages: source media→canonical pixels→tensor; fabricated raw output→canonical detection/pose. Samples: materialized `odd_landscape`, `odd_portrait`, `empty`, `occlusion_ownership`, `pose_critical`, плюс synthetic channel/ramp/layout/nc1/2/3 fixtures.

**Процедура:** проверить RGB/BGR, range/layout/dtype/rotation/SAR, actual rounded resize/pad/crop ledger и normalization owner; same tensor bypass policy. Явно проверить все output names/roles/dtypes/shapes/ports, C=5/6/7 против final6, BCN/BNC collision A=6/84/85, missing/shuffled multi-output, keypoint/proto association; DFL/sigmoid/objectness ровно по выбранному head; class map custom, dequant once. NMS tests score t−ε/t/t+ε, IoU boundary/ties/class-aware/agnostic/multi-label/global/per-class caps/padded count и timeout. G01–04 expectations брать v8.3.230: boxes без round и low-conf xy не zeroed; старую8.3.0 policy отдельно.

**Выходы:** exact prepared tensors/hash/ranges/geometry, canonical expected/actual arrays, schema rejects, implementation/dependency/NMS branch log. Device N/A до E003. **PASS:** заранее заданные structural/synthetic arithmetic checks выполняются; numeric comparison по versioned policy. **FAIL:** wrong axes/role/geometry/normalization/silent output fallback; **HOLD/UNAVAILABLE:** сервер скрывает tensors, тогда только доступная output/black-box часть. Возможные причины: helper version, dtype boundary, double transform; исправить adapter, не QAT. PASS не оценивает industrial quality/модель/device. Связи F034–F057/F206–F213; K002/K003/K011.

<a id="E003"></a>
### E003 — Неизменённый known-good completed LinQ smoke

**Цель/решение:** проверить actual access/runtime/artifact identity до custom build; owner platform/LinQ runtime. Inputs: Q001/Q002/Q008/Q009, supplier-supported `.tpu`/service revision+IO+golden input/output и matched bundle, разрешённая invocation instruction. Stages: unchanged supported artifact→actual LinQ completed output. Samples: два действительных known inputs (`normal_person_machine`, `empty` если sample model применим), IDs из manifest; не выдумывать детектор для classifier sample.

**Процедура:** записать source/export/compiled/service hashes/revisions и device/session; вызвать только действительный documented path, подтвердить completion/readiness/error semantics. Связать input hashes/batch slots/job→actual device→completion→named output; корректно прочитать user/raw format; проверить finite/schema и vendor known expected output. `.run` не считать blocking по имени. Сохранить error/timeout/late output; load/import не admission всего пути.

**Выходы/TPU proof:** matched versions/target, load/compile provenance где доступно, request+session+device+input/completion/output trace и разрешённый partition/profile, terminal census. **PASS:** конкретный unchanged inference завершён с нужным output и достаточной attribution; **FAIL:** неверный artifact/backend/schema/output либо runtime error; **HOLD:** только inventory/UI label/accepted enqueue без proof; restricted catalog attestation отдельно. Причина может быть access/ABI/device/program; остановить custom build до локализации. PASS не доказывает custom-model support, full graph placement без report, detection/event quality или throughput. Основания F203–F205/F234/F238/F239; K001/K007/K011.

<a id="E004"></a>
### E004 — Source repeatability, preparation и FP export

**Цель/решение:** локализовать loss до importer/PTQ; owner model/export. Inputs E001/E002, exact source runtime/weights/config и version-pinned exporter, CPU либо отдельно разрешённый source backend; никаких target precision предположений. Baseline→target: source eager→prepared eval/fused/export head→unsimplified ONNX same dtype→alternate runtime same dtype. Samples: frozen normal/empty/tiny/odd/pose/ownership плюс разрешённые shapes/batches/branch negative controls.

**Процедура:** repeated same input/state/batch/fresh process выявляет source noise; capture actual flags/TF32/autocast/accumulator policy. Отделить fusion/C2f/export head rewrite от ONNX translation; explicit opset по Q005. Сохранить original portable graph, каждый pass/static specialization/simplifier/IR change как отдельный parent. Проверить input byte identity, все output count/role/shape/dtype/finite-mask, index tensors exact, per-head/channel abs/relative errors+near-zero handling/worst IDs; source expected отдельно от ONNX-derived expected. Проверить control-flow обе ветви, B/[a,b]/[b,a], rectangular shape только в accepted dynamic scope. `verify`, checker и check_ok не самостоятельный gate.

**Выходы:** checkpoints/ONNX+sidecars hashes, effective exporter/report/warnings/actual optimization, stage arrays/errors/inventory. TPU proof N/A. **PASS:** agreed repeatability+structural/numerical и stage/source-final budgets на roster; **FAIL:** first divergence/invalid schema/nonfinite/unapproved pass; **HOLD:** нет tolerances/source; unavailable target float не выдумывать. Remedies: revert first transform/repair semantic operator/shape, не train. PASS не доказывает GT quality или LinQ importer. Связи F004–F033/F058–F069/F206; K002/K003.

<a id="E005"></a>
### E005 — Identity/ports и отдельный float ONNX→TF gate

**Цель/решение:** не приписать importer loss quantization; owner SDK/import. Inputs: E004, actual Q004/Q005 bundle, permitted supported float executor. Baseline→target: exact ONNX→actual supplier imported float TF до QM. Samples: synthetic Identity+Transpose на X[1,3,2,2] с `100*c+10*h+w`, Split двух outputs одного node с distinct ports; затем те же actual normal/odd/tiny/Pose inputs E004.

**Процедура:** записать module/distribution/file/callable/version/hash/signatures; не заменить onnx_direct одноимённым converter. Для каждого ONNX value сохранить output ordinal, producer/port/type/shape/role→TF tensor с port/layout→будущий QM descriptor; никаких strips `:1`/first output/retries без explicit branch evidence. Проверить обе synthetic roles независимо от dict ordering, exact arithmetic/transpose; после actual model сверить все raw channels/candidates/keypoints и общий decoder. Static metadata rewrite/simplification отдельно сериализованы и проверены, не скрыты in-memory.

**Выходы:** parent graph chain/hashes/changes, complete mapping/IO/layout table, actual TF outputs+float deltas/traceback. TPU N/A. **PASS:** mapping однозначен, роли и численные budgets сохраняются; **FAIL:** wrong endpoint/port/permutation/missing role; **UNAVAILABLE/NOT_EXPOSED после факта:** float executor/mapping не выданы, ONNX→QM переход confounded; можно дальше black-box quality с ограниченным claim. PASS простого micrograph не доказывает весь YOLO/RTDETR operator set, PTQ или устройство. Связи F212/F213; K002; Q004/Q005/Q015.

<a id="E006"></a>
### E006 — Effective PTQ/calibration, percentile и save/load

**Цель/решение:** установить реальный фактор calibration и воспроизводимость; owner quantization/SDK. Inputs: passed float boundary, supported small weighted graph+observed encodings/hooks, same graph/preprocess, separate calib/dev manifests; Q006/Q008/Q015. Baseline→target: float TF→native quantized reference, отдельно supported save→new-process load. Samples: materialized calib distribution A/B с известными разными tails и dev tiny/lighting/hard negatives; test untouched.

**Процедура:** две документированно допустимые P settings×две frozen distributions, fresh model каждый cell и два fresh repeats одной cell; no blanket TypeError retry. Записать requested→passed→resolved/effective kwargs/defaults, actual weights/thresholds/scales/zp/axis/signedness/ranges/counts/order/cache. Не придумать 99.x domain. Отделить прямой activation effect от весового через supported frozen-weight intervention/implementation trace; без неё confounded. Сопоставить float значения за bounds и clipping, а не endpoint-hit fraction. Save/load без recalibrate сравнить outputs/encodings; byte hash change сериализации сам по себе не numerical loss. Затем минимальные calibration method/coverage/size/order comparisons только доступного backend на dev, без полного декартова продукта.

**Выходы:** effective config, encodings/weights/threshold dumps где exposed, calibration hashes/coverage+N/groups, QM parents/reload outputs/warnings/first divergence. Device proof только если отдельный completed target leg E007, не из TF reference. **PASS:** реальное применение policy и repeatability объяснены, agreed numerical/task dev gates соблюдены; **FAIL:** проигнорированный supported option/invalid scales/serialization drift; **HOLD/INCONCLUSIVE:** scope не различим или inputs/implementation скрыты; отсутствие изменения не доказательство игнорирования. PASS не доказывает лучший percentile, industrial safety/independent quality или current QAT support. Связи F070–F081/F173–F185/F214–F216; K004.

<a id="E007"></a>
### E007 — Compiler/quant contract и proof перед recovery training

**Цель/решение:** выбрать действительно передаваемый native PTQ/QDQ/native-simulator/mixed route; owner compiler/quant/platform. Inputs: matched official recipe Q005/Q007/Q008, E003/E005/E006, vendor-supported weighted micrograph с различимыми nontrivial scales/axis/zero point, actual target/allowed presets/batches. Baseline→target: quantized reference→TLM если доступен→compiled program→completed device; для external contract reference→imported→QM→compiled→device.

**Процедура:** сохранить один clean QM parent; explicit target/preset/config/batch, compile executable+tensor descriptors, rounding/clipping/half-step/zero-point/bias/accumulator probes. Выбрать только officially asserted route A external preserve либо B native matching simulator; parser acceptance не preservation. При запрошенных FP islands проверить поддержанную Q→FP→Q boundary+shared/residual tensor, encodings/placement и numeric outputs, не просто count QDQ. Сравнить user FULL с supported RAW+codec лишь по текущему ABI; double rescale запрещён контрактом. Для model graph сравнить first observable boundary и ordinary deployment artifact, debug outputs могут менять fusion.

**Выходы/TPU proof:** immutable QM/TPU hashes+compile args/report/preset/target/precision/partition/cpu portions, input/job/device/completion/output trace, same-input deltas. **PASS:** numerical contract сохранён или documented equivalent lowering, agreed budgets/placement соблюдены; **FAIL:** changed arithmetic/wrong target/hidden fallback/unsupported boundary; **HOLD/UNAVAILABLE:** consumer/report не exposed — не расходовать GPU на неподтверждённый route. Без float/TLM transition confounded явно. PASS не доказывает улучшение full detection/pose/event или faster runtime; оно только admission конкретного numerical contract. Связи F217–F224/F238/F239; K001/K005/K011.

<a id="E008"></a>
### E008 — Независимый detection/pose regression gate

**Цель/решение:** принять качество конкретного candidate после исполнимого route; owner CV/evaluation. Inputs: A/B complete prediction roster, independent grouped test+rights/GT/skeleton/visibility, frozen decoder/preprocess/NMS/evaluator+approved Q012 policy; не search set. Stages: source A и actual final B независимо→GT; adjacent stages отдельно. Samples: all frozen `normal_person_machine`, `empty`, `tiny_phone_or_ppe`, `occlusion_ownership`, `pose_critical`, lighting/scale/hard negatives, chosen critical IDs.

**Процедура:** class-consistent diagnostic A↔B one-to-one matching отдельно от official GT evaluator; count unmatched/lost/gained/all GT, candidate margins и score drift. AP unit 0–1/0–100 явно; per-class/size/input-pixel/occlusion/visible vs annotated-hidden slices; critical joints+unmatched persons и skeleton-compatible OKS/PCK normalization. Source agreement не truth. Paired inference по допустимым clusters пересчитывает pooled evaluator/matcher, сохраняет undefined draws/few-cluster sensitivity; zero failures bounds только under assumptions, не universal AP CI. Fixed smoke reused для debug — narrow regression scope.

**Выходы:** canonical predictions/GT/evaluator config+hashes, matched/unmatched ID ledger, raw counts/AP/OKS/PCK/pose drift+units, paired deltas/uncertainty/absolute levels/coverage. TPU proof берётся linked E003/E007 actual B, не COCO score. **PASS:** все approved absolute/slice/noninferiority/invariant gates в заявленном scope; **FAIL:** confirmed violation/critical must-pass miss; **INCONCLUSIVE:** zero rare positives/wide bounds/few clusters; **HOLD:** policy/GT missing. Нельзя compensate новый critical miss gained TP. PASS не доказывает tracking/event usefulness, exposure rate или population вне design. Связи F107–F118/F134–F141/F230–F233/F246–F250; K006/K009/K010.

<a id="E009"></a>
### E009 — Fixed-input causal tracking/event parity

**Цель/решение:** отделить propagation модели от tracker/rules; owner tracking/event/evaluation. Inputs: E008 predictions, continuous clips/PTS/epoch, independent physical actor/episode GT+onset uncertainty/complete follow-up, frozen tracker/FSM/zones/thresholds/reset/warm prefix/deadline. Baseline→target: A→same downstream против B→same downstream на одинаковом source schedule. Samples: `short_event`, `fall_or_lying` при применимости, `occlusion_ownership`, `boundary_zone`, `persistent_incident`, `two_episodes_reentry`, `file_end`, continuous negatives.

**Процедура:** B→B harness repeatability перед comparison; сохранять low/high/new track pools/association costs/derived predicates/FSM/consumed frame evidence и первое divergent decision. Named track ID equality не criterion, actor continuity оценивается по GT. Scores-only/boxes-only/pose-on-fixed-crops interventions отдельная diagnostic oracle branch, не production score/аддитивное разложение. Time source PTS, не update count; fixed dt=1 не PTS-aware после frame_rate setting. Online decisions без будущей interpolation/backdating. Event matcher one-to-one по class/camera/actor/zone/declared temporal/deadline policy, no silence-as-success.

**Выходы:** четырёхклеточная paired episode table+IDs/unknown, timely recall по всем GT, late/miss/wrong actor/duplicate/false counts, source-camera-hour exposure full census, tracking DetA/AssA/HOTA при GT, latency n+misses. Device proof не новый: linked actual prediction lineage. **PASS:** agreed event/continuity/dedup/absolute gates и complete closure; **FAIL:** new critical miss/wrong person/duplicate ongoing/future leakage; **HOLD/INCONCLUSIVE:** truth/follow-up/rare support insufficient. PASS не доказывает реальные queues/load/delivery/backend. Связи F119–F141/F247–F250; K009/K010.

<a id="E010"></a>
### E010 — Actual schedule, server video, нагрузка и полезная доставка

**Цель/решение:** выбрать actual sampling/concurrency/drop policy и честно измерить speed/latency; owner video_architecture/runtime/product. Inputs: E003/E008/E009, actual granted service/Q010/Q011, allowed load/fault mechanisms, matched clocks/boundaries и AR01. Baseline→target: fixed causal replay→actual file-service scheduler/completion→visible alert. Samples: frozen continuous positive/negative/short-event/VFR/gap/reconnect/file-end roles; same original file bytes/PTS, no mandatory laptop stream assumption.

**Процедура:** один поток smoke, далее только разрешённая declared concurrency; save source/sampled/scheduled/completed/dropped/failed/unresolved census, real/padded slots/retry IDs. Warmup целыми batches либо exact matching accounting; timer до readiness/barrier, named infer-call versus decode/queue/copy/NMS/event/delivery отдельно. Source PTS не вычитать из UTC/monotonic без mapping; paced anchor+speed для replay, unpaced throughput отдельно от live SLA. Sampling sweep rates×предdeclared discrete phases плюс burst gaps на всех GT; adaptive sampling causal. Error/late/reordered/duplicate/EOF/drain via supported validation mechanism, без произвольного hardware outage. Timed-out не значит cancel, late response не новое событие.

**Выходы/TPU proof:** linked artifact/job/device/completion/output+placement evidence, terminal status ledger, useful completed real FPS+точный interval, per-stage p50/p95/p99/n и misses/timeouts/age/max observation gap, timely event and false/duplicate burden/exposure under actual load. **PASS:** quality/completeness/latency/device gates при конкретной нагрузке; **FAIL:** deadline/coverage violation/hidden neural backend switch; **HOLD:** no completion/clock/device evidence; **INCONCLUSIVE:** insufficient exposure/support. High FPS alone не PASS. Возможны correct model+bad queues либо unfair batch denominator; remedies architecture/policy, не QAT. PASS не гарантирует другие N streams/sites/события любой длительности/1FPS. Связи F124–F141/F186–F196/F237–F240; K007/K010/K011.

<a id="E011"></a>
### E011 — Ограниченное recovery или alternate-route admission

**Цель/решение:** тратить обучение только на локализованный исполнимый loss; owner model/quant/training. Inputs: failing stage+IDs из E004–E010, clean parent/accepted rollback, fixed calib/dev и sealed holdout, Q007 consumer proof, отдельно разрешённый measured GPU pilot если нужен. Baseline→target: один frozen PTQ→одна correction/selective policy/QAT либо alternate model; каждый новый artifact снова export/import/compiler→actual B. Samples: dev failure roles+independent future holdout IDs, same eval roster между кандидатами.

**Процедура:** сначала проверить geometry/decoder/export/import, then effective calibration; supported single-block rescue по semantic graph regions до шести и максимум две boundary/interaction probes — выбранный bounded budget, не норматив. FP head после QDQ не undo upstream loss; shared/residual interactions не additive. Bias correction для mean shift, CLE только algebraically valid, AdaRound для stable grid, BRECQ требует architecture-specific blocks/cache; одна correction с ablation. QAT только matched simulator/consumer, BN/observer/checkpoint/export round-trip и measured memory/time/cost pilot; no fake hours/24GB fit. Победитель определяется dev и E008/E009 independent test один раз.

**Альтернативы:** exact RT-DETR-l source route сначала sampler16/TopK/attention float admission, output BNC300; exact RTMPose-m сначала dependency override/registry/input_center-scale/2 outputs/flip-off/fixed-crop smoke, then network+host decoder, cost detector+N crops. Weights bytes/hash не скачаны здесь. Catalog-only — выбрать actual supplied model, не объявлять локальную alternative deployable. Optional ORT auto search — exact entry point/provider/optimized graph smoke, CPU casts не GPU/LinQ proof.

**Выходы:** parent/config/scales/weights+compile lineage, actual affected precision/placement, dev reconstruction/task/event/latency outcomes+failed attempts, pilot allocated/reserved VRAM/step/eval/export/compile/billable ledger, holdout unchanged. **PASS:** reproducible gain с required absolute/quality/device/latency gates и supported contract; **FAIL:** gain исчез после export/compile, critical regression/budget violation; **HOLD:** no consumer/data/pilot permission; **UNAVAILABLE:** route unsupported on actual grant. Stop при unsupported boundary без equivalent lowering, исчерпанном согласованном rescue/trial budget или принятом варианте; rollback entire bundle. PASS не обосновывает universal метод/bitwidth/GPU speedup и не production safety. Связи F082–F106/F214–F245; K004/K005/K006/K008.

<a id="E012"></a>
### E012 — Reviewable acceptance, demo и полный rollback

**Цель/решение:** выпускать только доказуемый scope и восстановить последнюю принятую конфигурацию; owner evaluation/team approver. Inputs: E001–E011 применимые результаты, policy approvals, complete source/candidate bundle+device traces/GT/logs, secrets removed. Baseline→target: collected actual evidence→versioned decision/demo; не новый benchmark. Samples: all evaluated IDs плюс одинаковые source/target/GT хорошие и худшие примеры/negative clip, selected before presenting story.

**Процедура:** заполнить AR01 MEASURED только из actual logs, каждый required gate отдельно PASS/FAIL/HOLD/INCONCLUSIVE/UNAVAILABLE+scope; adjacent и source→final deltas, estimates+uncertainty assumptions/counts/exposure, worst/lost/gained/dropped IDs и missing proof. Demo связывает original clip hash/frame PTS→source/export/compiled/model revision→completed device job→raw/canonical outputs→GT/evidence→visible alert. Чужие vendor/paper numbers с их условиями отдельно от своих. Не создавать synthetic industrial footage или fake LinQ/NVIDIA comparison. Тест rollback возвращает model+preprocess+decoder+class/skeleton+tracker/rules/sampling complete bundle, а не только weights.

**Выходы/TPU proof:** portable reviewable bundle, quality/timing/device claim table с F/S/Q links, signed decision/owner/date/unresolved risks и reproducible baseline restoration. **PASS:** все required gates действительно пройдены в explicit scope и evidence прослеживаем; **FAIL:** required violation/неверный claim/rollback не восстановил baseline; **HOLD:** missing/insufficient required evidence. Возможен только narrow fixed-roster PASS при population INCONCLUSIVE. Новый model/shape/dtype/compiler/runtime/preprocess/decoder/schedule/rule/camera geometry повторно открывает нужные gates. PASS не является сертификацией или гарантией будущей безопасности. Связи F001–F003/F134–F141/F186–F196/F234–F250; все K, особенно K010/K011.
