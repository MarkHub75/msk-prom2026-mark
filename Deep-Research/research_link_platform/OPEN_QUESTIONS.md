# OPEN_QUESTIONS — адресные неизвестные LinQ

Состояние:23.10.2026 после двух волн. Q — неизвестное, а не отсутствие функции. E — будущий проверяемый эксперимент, R — условный маршрут; E/R allocation в [_WORK/AUTHOR_HANDOFF.md](_WORK/AUTHOR_HANDOFF.md). SDK/signup outcome не сообщён пользователем; ни actual release, ни device grant не выводятся из публичного предложения.

Первая встреча: Q001–Q005 в этом порядке. Они объединяют доступ/свою модель, согласованный release, I/O, limits/network и критерий LinQ. Остальные вопросы не следует превращать в анкету первой встречи.

## Пять первых вопросов экспертам — сначала меняют маршрут

<a id="q001"></a>
### Q001 — Какой actual access и путь своей модели выданы: shell/container, custom service, job либо catalog; можно ли менять graph/weights и где compiler?

- Важность: блокирует основной путь.
- Почему открыт / что известно / где искали: Публичный кейс обещает online LinQ; /sol gate и Cloud claims не onboarding. W2-A/L проверили live navigation/demo, custom upload/schema не найдены; signup outcome пользователем не сообщён.
- Решение и последствие ответа: Определяет [R001](_WORK/AUTHOR_HANDOFF.md#r001)–[R005](_WORK/AUTHOR_HANDOFF.md#r005) и возможность custom PPE вместо готового detector.
- Как закрыть / зависимость доступа: Ответ организатора+actual onboarding+один supplied working call; [E015](_WORK/AUTHOR_HANDOFF.md#e015). SDK нужен только для выбранного маршрута; device/service grant нужен.
- Возможные исходы → действия: Custom upload → [R002](_WORK/AUTHOR_HANDOFF.md#r002); shell+tools → [R001](_WORK/AUTHOR_HANDOFF.md#r001); job → [R003](_WORK/AUTHOR_HANDOFF.md#r003); catalog → [R004](_WORK/AUTHOR_HANDOFF.md#r004) только при достаточных классах/разрешении; unknown → adapter contract не выдумывать.
- Основания: [F302](RAW_FACTS.md#f302), [F309](RAW_FACTS.md#f309), [F312](RAW_FACTS.md#f312); критика [K001](CRITIC.md#k001-w2), [K014](CRITIC.md#k014-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001), [E015](_WORK/AUTHOR_HANDOFF.md#e015). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q002"></a>
### Q002 — Каков единый matching release/SKU target и полный delivery manifest compiler/runtime/driver/firmware/Python/dependencies/licenses?

- Важность: блокирует основной путь.
- Почему открыт / что известно / где искали: 2025guide,2026benchmark,2023pytpu и authorTF2.14.1 не единый стек. Ни modernwheel/image/native/header не выданы; навигация и PyPI inspected.
- Решение и последствие ответа: Выбор окружения/ABI/compile target; исключает часы случайного pip/ctypes pairing.
- Как закрыть / зависимость доступа: Versioned bundle+image digest или wheelhouse/lock+install guide и actual metadata; [E001](_WORK/AUTHOR_HANDOFF.md#e001)/[E008](_WORK/AUTHOR_HANDOFF.md#e008).
- Возможные исходы → действия: Готовый supported image → сохранить ииспользовать; compiler-only → отдельный runtime handoff; API-only → неустанавливатьлокальный SDK как prerequisite.
- Основания: [F209](RAW_FACTS.md#f209), [F210](RAW_FACTS.md#f210), [F262](RAW_FACTS.md#f262), [F329](RAW_FACTS.md#f329); критика [K002](CRITIC.md#k002-w2), [K012](CRITIC.md#k012-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001), [E007](_WORK/AUTHOR_HANDOFF.md#e007), [E008](_WORK/AUTHOR_HANDOFF.md#e008). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q003"></a>
### Q003 — Каков exact input/output/pre/post contract поддержанного custom detector либо выданного .tpu: names/layout/dtype/shapes/classes/decode/NMS и golden tensors?

- Важность: блокирует корректность.
- Почему открыт / что известно / где искали: GuideResNet, authorYOLO, Tiny и FCN различны; vendorTinybytes/golden неизвестны; custom runnerCOCOheuristics дефектны.
- Решение и последствие ответа: Нужен immutable model manifest; определяет decoder/calibration/quality и допустимость host stages.
- Как закрыть / зависимость доступа: Получить actual artifact+metadata+supported exporter+source pre/post+positive/negative golden; [E002](_WORK/AUTHOR_HANDOFF.md#e002)–[E004](_WORK/AUTHOR_HANDOFF.md#e004)/[E008](_WORK/AUTHOR_HANDOFF.md#e008)–[E010](_WORK/AUTHOR_HANDOFF.md#e010).
- Возможные исходы → действия: Rawheads → host decoder по spec; decoded/noNMS → без повторного DFL/sigmoid; postNMS → нельзя recover отброшенных candidates; no outputs → проверить достаточность events.
- Основания: [F238](RAW_FACTS.md#f238), [F241](RAW_FACTS.md#f241), [F243](RAW_FACTS.md#f243), [F251](RAW_FACTS.md#f251), [F263](RAW_FACTS.md#f263); критика [K006](CRITIC.md#k006-w2), [K007](CRITIC.md#k007-w2), [K009](CRITIC.md#k009-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E003](_WORK/AUTHOR_HANDOFF.md#e003), [E004](_WORK/AUTHOR_HANDOFF.md#e004), [E008](_WORK/AUTHOR_HANDOFF.md#e008), [E010](_WORK/AUTHOR_HANDOFF.md#e010). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q004"></a>
### Q004 — Каковы per-team quotas/lifecycle/network: max payload/inflight/batch/QPS, shared queue, timeouts/cancel, CPU/RAM/storage/persistence и доступ worker к камерам/результатам?

- Важность: блокирует realtime архитектуру.
- Почему открыт / что известно / где искали: W2-L не нашёл численных limits; shell не гарантирует ports/long-running/network; model API может принимать лишь raw tensors.
- Решение и последствие ответа: Определяет sampling/camera admission/batching/placement UI и bounded queue.
- Как закрыть / зависимость доступа: Issued limits+network rules+documented terminal states; затем [E012](_WORK/AUTHOR_HANDOFF.md#e012)/[E014](_WORK/AUTHOR_HANDOFF.md#e014)/[E015](_WORK/AUTHOR_HANDOFF.md#e015).
- Возможные исходы → действия: Tensor API → считать bytes; stream service → проверить codec/reachability; no persistence → локальный manifest/reupload; timeout without cancel → считать request inflight до terminal.
- Основания: [F309](RAW_FACTS.md#f309), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313); критика [K014](CRITIC.md#k014-w2), [K017](CRITIC.md#k017-w2); эксперименты [E012](_WORK/AUTHOR_HANDOFF.md#e012), [E014](_WORK/AUTHOR_HANDOFF.md#e014), [E015](_WORK/AUTHOR_HANDOFF.md#e015), [E016](_WORK/AUTHOR_HANDOFF.md#e016). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q005"></a>
### Q005 — Какую NN-границу обязаны выполнить на LinQ и какое execution evidence принимает жюри для shell и service-only; допустимы hostNMS/tracking/secondaryNN?

- Важность: блокирует принятие результата.
- Почему открыт / что известно / где искали: Кейс требует LinQ inference бездоказательногоформата/распределения. Profiler именован, coverage/per requesttrace current не получены.
- Решение и последствие ответа: Определяет graphpartition и пакетзащиты; не навязывать attestation или SSH.
- Как закрыть / зависимость доступа: Ответ постановщика+matchingruntime/coverage report либо accepted witnessedrun; [E009](_WORK/AUTHOR_HANDOFF.md#e009).
- Возможные исходы → действия: Trace+coverage → двухзвенноедоказательство; witnessedslot → указать trustboundary; onlybadge/utilization → недостаточнонашейатрибуции; все NN на LinQ → проверятькаждую NNstage.
- Основания: [F287](RAW_FACTS.md#f287), [F291](RAW_FACTS.md#f291), [F293](RAW_FACTS.md#f293), [F294](RAW_FACTS.md#f294); критика [K013](CRITIC.md#k013-w2), [K014](CRITIC.md#k014-w2); эксперименты [E009](_WORK/AUTHOR_HANDOFF.md#e009). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

## Нужен SDK/поставка либо предоставленный сервер

<a id="q006"></a>
### Q006 — Какой exact wheel/native/driver pairing даёт tpu_framework, pytpu, onnx_direct, TLM; какие OS/ISA/Python/kernel/glibc поддержаны?

- Важность: блокирует локальнуюустановку.
- Почему открыт / что известно / где искали: W2-A sourcearchives не содержат modern native; py3-none-any относится wheel, не транзитивным libs. Windows/WSL/ARM неиспытаны.
- Решение и последствие ответа: Решает CPU compiler host vsremoteimage; исключает переносстарого binding нановую.so.
- Как закрыть / зависимость доступа: [E001](_WORK/AUTHOR_HANDOFF.md#e001) archiveMETADATA/WHEEL/systemmanifest+vendor compatibility matrix.
- Возможные исходы → действия: Native Linux only → Windows клиент remote; CPUpreparationunsupported → build на suppliedhost/service; allowed system library without device → отдельнопроверить import/compile.
- Основания: [F038](RAW_FACTS.md#f038), [F039](RAW_FACTS.md#f039), [F204](RAW_FACTS.md#f204), [F329](RAW_FACTS.md#f329); критика [K002](CRITIC.md#k002-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q007"></a>
### Q007 — Может ли actual release компилировать CPU-only безплаты/driver/device grant; каковы license/network и RAM/time требования?

- Важность: влияетнавыбор.
- Почему открыт / что известно / где искали: Guide разделяет prepare/.tpu/run инеперечисляет GPU/плату, но actual compile небыло; importmayneednative/license.
- Решение и последствие ответа: Можно вынести build судалённогоквотированного runtime, бюджет 45 ч.
- Как закрыть / зависимость доступа: [E007](_WORK/AUTHOR_HANDOFF.md#e007) в matching CPU environment с one supported model; отдельнофиксировать importdependency/license/device errors.
- Возможные исходы → действия: Success → доказано толькоэтот release/target безплаты; library missing → не путатьс physical device requirement; license/device required → remote compile.
- Основания: [F045](RAW_FACTS.md#f045), [F208](RAW_FACTS.md#f208), [F210](RAW_FACTS.md#f210); критика [K002](CRITIC.md#k002-w2), [K020](CRITIC.md#k020-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001), [E007](_WORK/AUTHOR_HANDOFF.md#e007). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q008"></a>
### Q008 — Какой current ONNX frontend и support opset/IR/domains/attrs/dtypes/externaldata/controlflow; ONNX → TF seam ещё актуален?

- Важность: блокирует custom import.
- Почему открыт / что известно / где искали: W2-C targetedsearch/PyPIexact404 не дали parser matrix; upstreamexportversioned, не LinQlowering.
- Решение и последствие ответа: Выбор exact export иминимального failinggraph; не браковать DFL/Resize по genericNPU рискам.
- Как закрыть / зависимость доступа: MatchingAPIreference/source+E004unchanged candidate; фактический inventory before import.
- Возможные исходы → действия: Direct ONNX current → не навязывать oldTF; documentedloweropset → reexport одинвариант; unsupported node → minimalreproducer/alternatehead.
- Основания: [F220](RAW_FACTS.md#f220), [F224](RAW_FACTS.md#f224), [F228](RAW_FACTS.md#f228), [F230](RAW_FACTS.md#f230), [F232](RAW_FACTS.md#f232); критика [K004](CRITIC.md#k004-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E004](_WORK/AUTHOR_HANDOFF.md#e004). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q009"></a>
### Q009 — Какие shapes/batch/layout можно импортировать и менять готовойпрограмме безперекомпиляции?

- Важность: влияетнавыбор.
- Почему открыт / что известно / где искали: GuideOptionaldims/batchaxis и authorstatic1/8 неуниверсальная dynamiccapability. Model ZooNsymbolic реально b2fails. Input-onlyshape patch меняетлишь graph input.
- Решение и последствие ответа: Batchformation/resolution/exportstrategy и correctanchors/grids.
- Как закрыть / зависимость доступа: Actual compiled metadata+supported shape API; [E004](_WORK/AUTHOR_HANDOFF.md#e004)/[E007](_WORK/AUTHOR_HANDOFF.md#e007)/[E010](_WORK/AUTHOR_HANDOFF.md#e010) static1/static8 иразные batchslots.
- Возможные исходы → действия: Fixed batch → отдельные artifacts/paddingcount; dynamic allowed → проверить allinternaldims; H/Wchange → полный reexport/parity, не protobufheaderpatch.
- Основания: [F221](RAW_FACTS.md#f221), [F225](RAW_FACTS.md#f225), [F247](RAW_FACTS.md#f247), [F265](RAW_FACTS.md#f265); критика [K004](CRITIC.md#k004-w2), [K007](CRITIC.md#k007-w2), [K009](CRITIC.md#k009-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E004](_WORK/AUTHOR_HANDOFF.md#e004), [E007](_WORK/AUTHOR_HANDOFF.md#e007), [E010](_WORK/AUTHOR_HANDOFF.md#e010). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q010"></a>
### Q010 — Каков настоящий complete end_to_end source и converter return/name mapping/compilecall длявыданного release?

- Важность: блокируетбуквальноеисполнение guide.
- Почему открыт / что известно / где искали: W2-B не получил binaryPDF/sourcearchive; TF2.14.1опроверг namespace/crashfalsealarm, но tuple/GraphDef/compileassignmentseams открыты.
- Решение и последствие ответа: Собратьправильный frontend pipeline, неизобретать vendorrecipe.
- Как закрыть / зависимость доступа: Suppliedsourcearchive/errata+E004type/signature/nameparity. PDFvisual поможеттексту, неподменит SDK.
- Возможные исходы → действия: Matchingexampleworks → followexact; guidefragmentdifferent → сохранить errata; source невыдают → APIref+minimal custom example достаточны.
- Основания: [F211](RAW_FACTS.md#f211), [F215](RAW_FACTS.md#f215), [F216](RAW_FACTS.md#f216), [F218](RAW_FACTS.md#f218), [F219](RAW_FACTS.md#f219); критика [K003](CRITIC.md#k003-w2); эксперименты [E004](_WORK/AUTHOR_HANDOFF.md#e004). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q011"></a>
### Q011 — Что именно меняет percentile, supportedrange/default и как доказать effective setting без TypeError retry?

- Важность: влияетна PTQ качество.
- Почему открыт / что известно / где искали: Guide weightcoefficientpercentile и data-dependentcalibration сосуществуют; summary несохраняетдаже requestedP/retry.
- Решение и последствие ответа: Нельзяначинатьслепой sweep99.9/100илиприписывать activationclipping.
- Как закрыть / зависимость доступа: Currentquantizerref+E005freshobject2×2×2W/C/P с threshold/weights/activationdumps.
- Возможные исходы → действия: Weightsonly/activation/joint → настроитьсоответствующий factor; equality не proveignored без sensitivegraph; unsupportedkeyword → фиксировать default без sweep.
- Основания: [F252](RAW_FACTS.md#f252), [F253](RAW_FACTS.md#f253); критика [K008](CRITIC.md#k008-w2); эксперименты [E005](_WORK/AUTHOR_HANDOFF.md#e005). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q012"></a>
### Q012 — Каковы threshold/.qm schema, save/load и determinism/portability между graphs/releases?

- Важность: влияетнавоспроизводимость.
- Почему открыт / что известно / где искали: Calibrate возвращает thresholds, quantize ихпринимает;.qm содержит topology/numericdata; schema и API roundtrip не получены.
- Решение и последствие ответа: Сохранить calibrationresult без повторногообучения/калибровки; versionedcache.
- Как закрыть / зависимость доступа: [E006](_WORK/AUTHOR_HANDOFF.md#e006) documented roundtrip вновом process; normalized metadata+rawoutputcomparison.
- Возможные исходы → действия: Roundtrip parity → доказантот release/graph; timestampbytehashdiff нечисленный fail; nopublicthresholdsave → незаявлять portability через pickle.
- Основания: [F254](RAW_FACTS.md#f254), [F261](RAW_FACTS.md#f261); критика [K008](CRITIC.md#k008-w2); эксперименты [E006](_WORK/AUTHOR_HANDOFF.md#e006). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q013"></a>
### Q013 — Какие signedness/zero-point/granularity/rounding/saturation/bias/accumulator/residual-scale и currentQAT/QDQ contract?

- Важность: влияетнавыбор.
- Почему открыт / что известно / где искали: Int8 ядроустановлено; точнаячисленнаясхеманеоткрыта. Historicalfloat16flag/scale-shifthelper не H1Mspec.
- Решение и последствие ответа: Нужноотличить PTQloss от I/Oerror; QAT толькопри working import path.
- Как закрыть / зависимость доступа: Matching quantizer reference+supportedminimalgraphs; [E005](_WORK/AUTHOR_HANDOFF.md#e005)/[E010](_WORK/AUTHOR_HANDOFF.md#e010), QDQ отдельный test по API.
- Возможные исходы → действия: QDQsupported → matchedfloat/QDQprobe; unsupported/unknown → vendorPTQbaseline; mixed precision claim → привязатьоперации/target, не floatinginput.
- Основания: [F255](RAW_FACTS.md#f255), [F257](RAW_FACTS.md#f257), [F260](RAW_FACTS.md#f260); критика [K008](CRITIC.md#k008-w2), [K009](CRITIC.md#k009-w2); эксперименты [E005](_WORK/AUTHOR_HANDOFF.md#e005), [E010](_WORK/AUTHOR_HANDOFF.md#e010). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q014"></a>
### Q014 — Какой current .tpu format/schema/compatibility и где actual user/raw names, shape, dtype, order, packing, size, alignment, scales/anchor?

- Важность: блокирует tensor adapter.
- Почему открыт / что известно / где искали: HistoricalZIPmetadata/region1,2 и codec fields есть; currentartifact/header/native нет; scalesformula отсутствует.
- Решение и последствие ответа: Предотвратить wrongbuffer/doublescale; перенос compiled artifact.
- Как закрыть / зависимость доступа: [E008](_WORK/AUTHOR_HANDOFF.md#e008) safelyreadactual artifact/currentProgram.info+schema/reference; reader можеттребовать device.
- Возможные исходы → действия: ZIP подтверждён → read-onlyinspect; schema иная → не hardcodeoldkeys; missing fields → vendor contract, не scale1/defaultshape.
- Основания: [F262](RAW_FACTS.md#f262), [F263](RAW_FACTS.md#f263), [F264](RAW_FACTS.md#f264), [F270](RAW_FACTS.md#f270); критика [K009](CRITIC.md#k009-w2), [K012](CRITIC.md#k012-w2); эксперименты [E008](_WORK/AUTHOR_HANDOFF.md#e008). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q015"></a>
### Q015 — Какие object/buffer lifetime и thread/process guarantees послеуспеха/ошибки; исправленли historical exception cleanup?

- Важность: влияетнаустойчивость.
- Почему открыт / что известно / где искали: W2-G fake-native подтвердил omission после exception, но outputview backing retained. Actualnormaldestroy включён. Currentfixunknown.
- Решение и последствие ответа: Правильный copy/borrowboundary, close/reuse/workerreplacement без doublefree.
- Как закрыть / зависимость доступа: Currentreference/source/releasenote; E016valid input output lifetime и ordinary host exception after terminal.
- Возможные исходы → действия: Borrowedoutput → documented copy; owned stable → немотивироватьлишний copydanglingclaim; post-errorinvalid → штатный reload/new worker; неуниверсальный restart любого Exception.
- Основания: [F266](RAW_FACTS.md#f266), [F267](RAW_FACTS.md#f267), [F268](RAW_FACTS.md#f268), [F323](RAW_FACTS.md#f323); критика [K012](CRITIC.md#k012-w2), [K015](CRITIC.md#k015-w2); эксперименты [E008](_WORK/AUTHOR_HANDOFF.md#e008), [E016](_WORK/AUTHOR_HANDOFF.md#e016). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

## Нужен LinQ или доверенный оператор реального сервиса

<a id="q016"></a>
### Q016 — Как связаны actual SKU/boardrevision/serial → PCI BDF/switch → device node → runtime instance ивыделенная quota?

- Важность: блокирует hardwareclaims.
- Почему открыт / что известно / где искали: W2-HHP01/02разделил, но four/dev под HPDlabel не physicalmapping; PCI2805:0006rev08 общий.
- Решение и последствие ответа: Correcttarget/memory/scaling/evidence, числодоступных devices.
- Как закрыть / зависимость доступа: [E008](_WORK/AUTHOR_HANDOFF.md#e008)/E013operatorinventory; permittedlspci/sysfs/currentdeviceinfo; service эквивалентотоператора.
- Возможные исходы → действия: FourchipsoneHPQ/twoHPD/other → записатьреально; containerhidesBDF → operator trace; devices видныноне выданы → неиспользовать.
- Основания: [F271](RAW_FACTS.md#f271), [F272](RAW_FACTS.md#f272), [F278](RAW_FACTS.md#f278), [F280](RAW_FACTS.md#f280); критика [K010](CRITIC.md#k010-w2), [K013](CRITIC.md#k013-w2); эксперименты [E008](_WORK/AUTHOR_HANDOFF.md#e008), [E013](_WORK/AUTHOR_HANDOFF.md#e013). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q017"></a>
### Q017 — Каковы per-graph DDR/cache/scratch/reserve limit и поддерживаетсяли explicit multi-chip graphpartitioning/remoteallocation?

- Важность: влияетна modelsize.
- Почему открыт / что известно / где искали: Физическая DDR на chip разнесена; slicing_schemeguide одногомикропроцессора; source parallel это replicas. Ни pooling, низапретне установлены.
- Решение и последствие ответа: Можно ли одна model использоватьсуммарную DDR илинужнынезависимые models/shards.
- Как закрыть / зависимость доступа: Plannerreport+current API reference; [E020](_WORK/AUTHOR_HANDOFF.md#e020) толькоесли supplied supported multichip graph.
- Возможные исходы → действия: Only replicas → memoryfitperchip; supportedsharding → partitionmanifest/transferredges/correctness; nodocs → не OOMsharedhost.
- Основания: [F011](RAW_FACTS.md#f011), [F276](RAW_FACTS.md#f276), [F277](RAW_FACTS.md#f277), [F279](RAW_FACTS.md#f279); критика [K010](CRITIC.md#k010-w2); эксперименты [E008](_WORK/AUTHOR_HANDOFF.md#e008), [E020](_WORK/AUTHOR_HANDOFF.md#e020). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q018"></a>
### Q018 — Каковы actual FULL/RAW allowed program×mode×bufferrepresentation и nativepre/post численнаясемантика/placement?

- Важность: блокирует raw experiments.
- Почему открыт / что известно / где искали: FileRAW и ProcessingModeRAW независимы; Pythonallocation/reshape по_is_raw; codec не получен.
- Решение и последствие ответа: Не castint8/doublescale; coveragevsnormalboundaryseparation.
- Как закрыть / зависимость доступа: Current native contract+user/rawgoldenpairs; [E010](_WORK/AUTHOR_HANDOFF.md#e010) толькодокументированным encoder.
- Возможные исходы → действия: FULL user parity → не addrescale; correctRAWpair → локализует codec; unsupportedcombination → неиспытывать malformedpointers; placement через report/reference, не parity.
- Основания: [F256](RAW_FACTS.md#f256), [F257](RAW_FACTS.md#f257), [F263](RAW_FACTS.md#f263), [F265](RAW_FACTS.md#f265), [F292](RAW_FACTS.md#f292); критика [K009](CRITIC.md#k009-w2), [K013](CRITIC.md#k013-w2); эксперименты [E010](_WORK/AUTHOR_HANDOFF.md#e010). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q019"></a>
### Q019 — Какие exact vendor Tiny checkpoint/exporter/BN/color/resize/anchors/output/NMS и b8 user contract?

- Важность: влияетна smoke/baseline.
- Почему открыт / что известно / где искали: Не supplied.tpu; filename не I/Omanifest. Model Zoo конвыобщиесо strict, но fineanchors/NMS/geometry различны; vendor цветневыбран.
- Решение и последствие ответа: Неатрибутировать APdeltaquantization, выбратьчестный golden.
- Как закрыть / зависимость доступа: Vendor hash+manifest+referenceinput/rawoutput; [E009](_WORK/AUTHOR_HANDOFF.md#e009)/[E010](_WORK/AUTHOR_HANDOFF.md#e010) и E002head parity.
- Возможные исходы → действия: Rawstandardheads → shared decoder; integratedNMS → matchrecipe; no identity → label smoke только vendor reference, не custom validation.
- Основания: [F243](RAW_FACTS.md#f243), [F245](RAW_FACTS.md#f245), [F246](RAW_FACTS.md#f246), [F247](RAW_FACTS.md#f247), [F248](RAW_FACTS.md#f248), [F251](RAW_FACTS.md#f251); критика [K007](CRITIC.md#k007-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E009](_WORK/AUTHOR_HANDOFF.md#e009), [E010](_WORK/AUTHOR_HANDOFF.md#e010). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q020"></a>
### Q020 — Какой exact custom detector воспроизводимо проходит matched export → compile → LinQ → quality: v8, classic5s либо 11?

- Важность: блокируетвыборгарантированногокандидата.
- Почему открыт / что известно / где искали: W2-D102commits/history/release выдали source, незамкнутый custom route;5su не classic5s;11OBBpriorbench ненаш detection.
- Решение и последствие ответа: Распределение training/export ресурсов; невыбиратьпо brand/popularity.
- Как закрыть / зависимость доступа: Получить supported custom sample+immutable manifest, затем [E002](_WORK/AUTHOR_HANDOFF.md#e002)/[E004](_WORK/AUTHOR_HANDOFF.md#e004)/[E007](_WORK/AUTHOR_HANDOFF.md#e007)/[E009](_WORK/AUTHOR_HANDOFF.md#e009)/[E011](_WORK/AUTHOR_HANDOFF.md#e011).
- Возможные исходы → действия: Exact5s/11worksfirst → можетстать primary; v8passesfloat/PTQ → продолжить; onlyfamilyclaim → оставить conditional.
- Основания: [F233](RAW_FACTS.md#f233), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [F236](RAW_FACTS.md#f236), [F242](RAW_FACTS.md#f242), [F330](RAW_FACTS.md#f330); критика [K005](CRITIC.md#k005-w2), [K018](CRITIC.md#k018-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E004](_WORK/AUTHOR_HANDOFF.md#e004), [E007](_WORK/AUTHOR_HANDOFF.md#e007), [E009](_WORK/AUTHOR_HANDOFF.md#e009), [E011](_WORK/AUTHOR_HANDOFF.md#e011). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q021"></a>
### Q021 — Какое current execution/coverage report или wholegraph/no-fallback guarantee и per-request device completion доступны?

- Важность: блокируетстрогоеисполнение claim.
- Почему открыт / что известно / где искали: Machinecodeclaim не coverage; invaliddevicefailure не partialpartitioncontrol; aggregateutilization можетчужая.
- Решение и последствие ответа: Разделить lineage/coverage ифизическуюатрибуцию.
- Как закрыть / зависимость доступа: [E009](_WORK/AUTHOR_HANDOFF.md#e009) compiled lineage+currentreport/guarantee+request/artifact/devicecorrelation/witnessaccepted по Q005.
- Возможные исходы → действия: CompileonlyTPUorerrorguarantee → документировать version; mixed stage → описатьграницы; noaudittrail → operatorwitness/оговореннаянезависимость.
- Основания: [F287](RAW_FACTS.md#f287), [F291](RAW_FACTS.md#f291), [F293](RAW_FACTS.md#f293), [F294](RAW_FACTS.md#f294); критика [K013](CRITIC.md#k013-w2); эксперименты [E009](_WORK/AUTHOR_HANDOFF.md#e009). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q022"></a>
### Q022 — Каковы current profiler units/clocks/scope/reset/lastavgmax/overhead и привязка model/request/device?

- Важность: влияетна measurement claim.
- Почему открыт / что известно / где искали: HPS именует tools; oldREADMEavg/maxaccumulateddeviceobject, actualimplementationmissing. Нет currentmanual/report.
- Решение и последствие ответа: Нельзяподписывать syncwallcompute/averageper request.
- Как закрыть / зависимость доступа: Current manual+raw sample export; [E012](_WORK/AUTHOR_HANDOFF.md#e012) наодном controlledrequest при documented trace.
- Возможные исходы → действия: Per-tasktrace → stage counters; aggregate only → supplementaryload; estimatedonly → отделитьот measured; no tool → API wall time+accepted witness безвыдуманного linq-smi.
- Основания: [F287](RAW_FACTS.md#f287), [F288](RAW_FACTS.md#f288), [F289](RAW_FACTS.md#f289), [F290](RAW_FACTS.md#f290); критика [K011](CRITIC.md#k011-w2), [K013](CRITIC.md#k013-w2); эксперименты [E009](_WORK/AUTHOR_HANDOFF.md#e009), [E012](_WORK/AUTHOR_HANDOFF.md#e012). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q023"></a>
### Q023 — Каковы actual warm latency/throughput/CPUtransfer и многокамерная frameage при quality-checkedartifact?

- Важность: влияетнасервисбюджет.
- Почему открыт / что известно / где искали: Vendor14rows неимеют matchedcontract; image-runnertimer нет pre/NMS/video; noourLinQbench.
- Решение и последствие ответа: Sampling/batch/cameracount и deadline, resourcebudget.
- Как закрыть / зависимость доступа: E012cold/warm/sequential/commonwindow; затем E014sameclip/2cameras; countrealcompletedimages и drops.
- Возможные исходы → действия: Throughputhighbutagegrows → admission/drop; batchslower → оставить b1; bottleneckhost/network → перенестиподдержанныестадии, не TOPScalc.
- Основания: [F130](RAW_FACTS.md#f130), [F282](RAW_FACTS.md#f282), [F285](RAW_FACTS.md#f285), [F331](RAW_FACTS.md#f331), [F332](RAW_FACTS.md#f332); критика [K011](CRITIC.md#k011-w2), [K017](CRITIC.md#k017-w2); эксперименты [E012](_WORK/AUTHOR_HANDOFF.md#e012), [E014](_WORK/AUTHOR_HANDOFF.md#e014). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q024"></a>
### Q024 — Какие same-session retry/reload/new worker/recoveryallowed и errorcodes/timeout/cancelterminalguarantees current release?

- Важность: влияетнаустойчивость.
- Почему открыт / что известно / где искали: W2-M status0/1/2historical не resetmap; skippedwatchdog не currentreproducer; clienttimeout не cancel.
- Решение и последствие ответа: Безопасный boundedincidentrecovery, не duplicateinflight/общий reset.
- Как закрыть / зависимость доступа: Currenterrortable/statemachine+participant manual; E016benignhostexception/deadline/gracefulreplacement; native error test толькос uppliedbenignpath.
- Возможные исходы → действия: Pre-submit validation → исправить request; terminalreusable → bounded reuse; pendingunknown → stop admission; baselinecleanworkerfails → packetadmin.
- Основания: [F320](RAW_FACTS.md#f320), [F323](RAW_FACTS.md#f323), [F324](RAW_FACTS.md#f324), [F326](RAW_FACTS.md#f326); критика [K015](CRITIC.md#k015-w2), [K012](CRITIC.md#k012-w2); эксперименты [E016](_WORK/AUTHOR_HANDOFF.md#e016). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q025"></a>
### Q025 — Какая allowed concurrency: separate Inference per thread, async, multiprocess/perdevice, multitenant/fork; есть ли fairness/isolation?

- Важность: влияетна throughput.
- Почему открыт / что известно / где искали: 14.7async и 15.0.24thread test существуют;8threadsTODOmismatch и noassertion. Oneprocessperdevice—sample policy, не platformconstraint.
- Решение и последствие ответа: Может ли безопасно повысить inflight без mixup/memorygrowth.
- Как закрыть / зависимость доступа: Current contract+allocatedreservedtopology; E017serial → 2distinct descriptors, validA/BwithIDs; multiprocess отдельноесли allowed.
- Возможные исходы → действия: Correct2workers → толькоэта topology, не hardware parallel guarantee; mismatch → serialfallback/bugpacket; undocumented → консервативный serial owner какнашвыбор.
- Основания: [F311](RAW_FACTS.md#f311), [F316](RAW_FACTS.md#f316), [F317](RAW_FACTS.md#f317), [F318](RAW_FACTS.md#f318), [F319](RAW_FACTS.md#f319), [F322](RAW_FACTS.md#f322); критика [K015](CRITIC.md#k015-w2); эксперименты [E017](_WORK/AUTHOR_HANDOFF.md#e017). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

## Требуется решение/разъяснение постановщика и владельца поставки

<a id="q026"></a>
### Q026 — Какие execute/modify/share/redistribute права SDK/native/compiler/image/checkpoint/.tpu дляпятиучастников и submission?

- Важность: влияетнаупаковку/маршрут.
- Почему открыт / что известно / где искали: MIThelperlicense прочитана; bindings/repolicenseunknown; Model ZooMITvsApachemetadataconflict; OEM/PDform не EULA.
- Решение и последствие ответа: Можно лираздать image, перенестистендилиопубликовать binaries; unknown неозначаетзапрет read/execute.
- Как закрыть / зависимость доступа: Actualsupplylicense/EULA/modelnotice+ответвладельца; E001license inventory.
- Возможные исходы → действия: Execute team only → ссылки/свои adapters без binaries; redistributionallowed → retainnotices; proprietaryimage → supplieraccessperteam; нераспространятьправососеднегопакета.
- Основания: [F203](RAW_FACTS.md#f203), [F205](RAW_FACTS.md#f205), [F250](RAW_FACTS.md#f250), [F300](RAW_FACTS.md#f300); критика [K019](CRITIC.md#k019-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q027"></a>
### Q027 — Есть ли разрешённая matched IVA CV PPE сборка для actual LinQ икаков image digest/config/models/backendinventory/eventschema?

- Важность: влияетнаготовый routeR006.
- Почему открыт / что известно / где искали: Literal LinQ TPU guide подтверждён, ноне H1M/PPEbuild; ПАКОТПБновостьне manifest; тег 0.1.3page-separated, не pullresult.
- Решение и последствие ответа: Turnkeyroute возможентолькопри suppliedassets/правах; иначе architecturelessons.
- Как закрыть / зависимость доступа: Интегратор/постановщикпередаёт bundle+license; E018file → event with device evidence.
- Возможные исходы → действия: MatchedPPEyes → [R006](_WORK/AUTHOR_HANDOFF.md#r006); genericwalkersonly → не объявлять PPE; noaccess → свой adapterR001/[R002](_WORK/AUTHOR_HANDOFF.md#r002); registryURL не grant.
- Основания: [F295](RAW_FACTS.md#f295), [F296](RAW_FACTS.md#f296), [F297](RAW_FACTS.md#f297), [F298](RAW_FACTS.md#f298), [F300](RAW_FACTS.md#f300); критика [K016](CRITIC.md#k016-w2), [K019](CRITIC.md#k019-w2); эксперименты [E018](_WORK/AUTHOR_HANDOFF.md#e018). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q028"></a>
### Q028 — Каков официальный support/incident путь, окнаинженеров и допустимый scope участникадля restart/recovery?

- Важность: влияетнавременириска.
- Почему открыт / что известно / где искали: Корпоративный HPS24/7SLA нехакатонобещание; currentreset команды/права unknown.
- Решение и последствие ответа: Когдаэскалироватьвместобесконечных retries, какнезатронутьдругиекоманды.
- Как закрыть / зависимость доступа: Issuedparticipantmanual/ответорганизатора; ownerincident packetE016.
- Возможные исходы → действия: Per job reset allowed → толькосвой scope; shareddeviceadminonly → эскалация; нетканала → заранеесогласовать fallbackdemo/acceptedrecording безобещаний.
- Основания: [F030](RAW_FACTS.md#f030), [F326](RAW_FACTS.md#f326); критика [K001](CRITIC.md#k001-w2), [K015](CRITIC.md#k015-w2); эксперименты [E016](_WORK/AUTHOR_HANDOFF.md#e016). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

## Зависит от полного кейса и данных

<a id="q029"></a>
### Q029 — Каковы полноеТЗ, обязательныеклассы/метрики/данные/разрешённые NN границы идопустимый qualityloss?

- Важность: блокируетфинальнуюоценку.
- Почему открыт / что известно / где искали: Publicexamples каска/респиратор/опаснаязона/курение неполныйобязательныйсписок; fullcase не получен; schedule2026 нестарый 2025.
- Решение и последствие ответа: Выбор head/classes/evaluator/qualitygate; association/rules не objectAP.
- Как закрыть / зависимость доступа: Опубликованное fullcase/датасет/organizeranswer, зафиксировать version/date; E011criteria.
- Возможные исходы → действия: SmallPPEmandatory → stratifiedrecall; eventmetric → violation-levelFP/FN; ownmodelrequired → catalogroutefails; менятьтолькоофициальноподтверждённыеусловия.
- Основания: [F033](RAW_FACTS.md#f033), [F034](RAW_FACTS.md#f034), [F035](RAW_FACTS.md#f035), [F261](RAW_FACTS.md#f261); критика [K005](CRITIC.md#k005-w2), [K017](CRITIC.md#k017-w2), [K020](CRITIC.md#k020-w2); эксперименты [E011](_WORK/AUTHOR_HANDOFF.md#e011). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q030"></a>
### Q030 — Какие камеры/видеоданные/права доступны, sourcePTS/timebase/annotation иразделение calibration/tuning/holdout возможно?

- Важность: влияетнакачество/realtime.
- Почему открыт / что известно / где искали: RandomimageIDsplitauthor непредотвращает nearbyframeleakage; реальныеданныеещёне выданы.
- Решение и последствие ответа: Calibration coverage малыхСИЗ, valid quality claim, fairlivequeue.
- Как закрыть / зависимость доступа: Dataset owner+fullcase; E011camera/timeblockmanifest, E014source clock record.
- Возможные исходы → действия: Onecamera → time heldout, необещать camera heldout; missing capture clock → receive-to-event; scarceholdout → iterations назвать tuning иотложитьнезависимуюпроверку.
- Основания: [F096](RAW_FACTS.md#f096), [F261](RAW_FACTS.md#f261), [F313](RAW_FACTS.md#f313); критика [K008](CRITIC.md#k008-w2), [K017](CRITIC.md#k017-w2), [K020](CRITIC.md#k020-w2); эксперименты [E011](_WORK/AUTHOR_HANDOFF.md#e011), [E014](_WORK/AUTHOR_HANDOFF.md#e014). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

## Можно разрешить будущим чтением первичного материала; текущая сборка не открывает третью волну

<a id="q031"></a>
### Q031 — Каковы оригинальные PDFbytes/pageimages/checksum guides/presentation и точные errata/units?

- Важность: полезноуточнить; P1 дляцитатчисел.
- Почему открыт / что известно / где искали: Многиеканалы TLS/screenshotfailed; только textlayer/remoteplaintext. W2-B/H/I/K ихнеповысилидовизуальных.
- Решение и последствие ответа: Точные punctuation/tuple/ModeProto/tableunits; не останавливаетдругие preparedSDKgates.
- Как закрыть / зависимость доступа: Будущее authoritativebinary отвендора/primarymirror, render+actualviewE019; вэтойсборкенового search нет.
- Возможные исходы → действия: Visualagrees → повыситьтолькотранскрипцию; officialerrata → сохранить old/new; stillunknown → labeltext-only; sourceSDK семантиканезависима.
- Основания: [F211](RAW_FACTS.md#f211), [F212](RAW_FACTS.md#f212), [F213](RAW_FACTS.md#f213), [F281](RAW_FACTS.md#f281), [F295](RAW_FACTS.md#f295); критика [K003](CRITIC.md#k003-w2), [K010](CRITIC.md#k010-w2), [K011](CRITIC.md#k011-w2), [K016](CRITIC.md#k016-w2); эксперименты [E019](_WORK/AUTHOR_HANDOFF.md#e019). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q032"></a>
### Q032 — Что означают modernslideFPS/latency: units/scenarios/denominator/percentile и HPQmeasured или extrapolated?

- Важность: влияетна benchmark ссылки.
- Почему открыт / что известно / где искали: W2-I оставил985.72/128.90ms,14rows4×, нет logs; альтернативные scenarios неопровергнуты.
- Решение и последствие ответа: Можно лицитироватькак measuredlatency/aggregatethroughput, не camcapacity.
- Как закрыть / зависимость доступа: Авторский rawlog+model/config/LoadGenrevision+точноесопоставление p3/p4; visualE019 лишьтекст, своё [E012](_WORK/AUTHOR_HANDOFF.md#e012) дастновуювыданнуюсреду.
- Возможные исходы → действия: Separatescenarios → не reciprocalcompare; typo official → correct with provenance; arithmeticHPQ → labelestimate; noanswer → indicativevendorclaim.
- Основания: [F281](RAW_FACTS.md#f281), [F282](RAW_FACTS.md#f282), [F283](RAW_FACTS.md#f283), [F284](RAW_FACTS.md#f284), [F331](RAW_FACTS.md#f331); критика [K011](CRITIC.md#k011-w2); эксперименты [E012](_WORK/AUTHOR_HANDOFF.md#e012), [E019](_WORK/AUTHOR_HANDOFF.md#e019). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q033"></a>
### Q033 — Разрешаютсяли familydatasheet/catalogHP02link, PCIeGen2/3 и power60/70/100,120/140/150,1000/1150/1500Вт authoritativeSKU/BOMrevision?

- Важность: полезноуточнить; actual inventory важнее.
- Почему открыт / что известно / где искали: W2-H нашёл HP01=16HP02=32иодинаковые active/passivemaxima; revisionchronology неустановлена.
- Решение и последствие ответа: Power/clock/memoryexpectations дляреальнойплаты; невыписыватьменьший powerlimit изслайда.
- Как закрыть / зависимость доступа: Matchingboardpassport/BOM+suppliererrata; E008actualLnkCap/LnkSta и clockmode вразрешённыхправах.
- Возможные исходы → действия: Differentrevision → разделить cards; catalogmislink → привязатьисправление; unknown → оба scopes безусреднения.
- Основания: [F272](RAW_FACTS.md#f272), [F273](RAW_FACTS.md#f273), [F274](RAW_FACTS.md#f274), [F275](RAW_FACTS.md#f275), [F279](RAW_FACTS.md#f279); критика [K010](CRITIC.md#k010-w2); эксперименты [E008](_WORK/AUTHOR_HANDOFF.md#e008), [E019](_WORK/AUTHOR_HANDOFF.md#e019). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q034"></a>
### Q034 — Можно лизаконнополучить rawmodernexperimentattachments автора repo/ВКР, exactweights/export/quality/versions?

- Важность: полезноуточнить; неблокируетсвой test.
- Почему открыт / что известно / где искали: Repohistory/release/ignoredassets открытого result непоказали; thesismetadata говорит priorbench и restricted full text; cloud table404.
- Решение и последствие ответа: Понятьподдержанный model route и independence безвымышленногоуспеха.
- Как закрыть / зависимость доступа: Авторский publicappendix/sourcepackage либоразрешённаяпередача; не обходить login. ExistingsearchhistoryW2-D/I.
- Возможные исходы → действия: Matchedlogs → новыйточный support record; onlyabstract → оставить scope; no artifacts → выполнитьсвои [E002](_WORK/AUTHOR_HANDOFF.md#e002)–[E012](_WORK/AUTHOR_HANDOFF.md#e012) при access вместоочередногобзора.
- Основания: [F233](RAW_FACTS.md#f233), [F234](RAW_FACTS.md#f234), [F236](RAW_FACTS.md#f236), [F285](RAW_FACTS.md#f285), [F286](RAW_FACTS.md#f286); критика [K005](CRITIC.md#k005-w2), [K018](CRITIC.md#k018-w2); эксперименты [E002](_WORK/AUTHOR_HANDOFF.md#e002), [E009](_WORK/AUTHOR_HANDOFF.md#e009), [E012](_WORK/AUTHOR_HANDOFF.md#e012). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.

<a id="q035"></a>
### Q035 — Какова точнаялицензия Model ZooTinyONNX/checkpoint вконфликтующих MIT/Apache2cards иусловиявесов?

- Важность: полезноуточнитьперед redistribution.
- Почему открыт / что известно / где искали: ActualHFfrontmatterApache2/bodyMIT, onnxmodelREADMEMIT/rootApache2, Darknet root public domain; direct weights отдельной license непоставлено.
- Решение и последствие ответа: Включение notices/binary в submission; неизменяет CPUprobeprovenance.
- Как закрыть / зависимость доступа: Модельный licensefile/maintainerclarification для exacthash, необщаялицензиявсехслоёв; Q026 для actual supplied binary.
- Возможные исходы → действия: ArtifactMIT → retainMITnotice; Apache2 → applicableNOTICE/LICENSE; unresolved → сохранить conflict ираздаватьсвои code/ссылкипоправиламсдачи.
- Основания: [F250](RAW_FACTS.md#f250); критика [K019](CRITIC.md#k019-w2); эксперименты [E001](_WORK/AUTHOR_HANDOFF.md#e001). Полный bounded search/access history — соответствующие branch RESULT и первичные карточки S в RAW_FACTS; новое внешнее получение в сборке не выполнялось.
