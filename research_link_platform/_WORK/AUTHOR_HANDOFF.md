# AUTHOR_HANDOFF — сборка LinQ evidence, стабильные IDs и инженерные развилки

Сборщик использовал 15 результатов W1, 13 результатов W2, исходную критику и сохранённые первичные материалы и протоколы. Нового внешнего поиска, третьей волны, делегирования и отдельного аудита нет. Отчёты пишет следующий автор. Модель этой роли — gpt-6.1-sol/high. Позднее уточнение RUN_STATE: пользовательский screenshot показал GPT-6.1-Sol high у root; раннюю неопределённость настройки не повторять как постоянную. Все роли исследователей были явно назначены medium, аналитические роли — high.

## Быстрый актуальный индекс для автора

Не читать 326 исторических карточек как 326 независимых подтверждений. Сначала сводные F329–F333, затем точные W2 facts ниже. W1 сохранён для деталей/происхождения; state переносить с W2.

| Тема | Актуальные опорные факты | Что обязательно сохранить |
|---|---|---|
| Доступ/поставка | [F198](../RAW_FACTS.md#f198), [F200](../RAW_FACTS.md#f200), [F209](../RAW_FACTS.md#f209), [F210](../RAW_FACTS.md#f210), [F302](../RAW_FACTS.md#f302), [F309](../RAW_FACTS.md#f309), [F329](../RAW_FACTS.md#f329) | Public guide ≠ SDK; registration ≠ verification ≠ device grant; user outcome unreported; API-only может быть достаточен. |
| Имена/железо | [F005](../RAW_FACTS.md#f005), [F271](../RAW_FACTS.md#f271), [F272](../RAW_FACTS.md#f272), [F273](../RAW_FACTS.md#f273), [F274](../RAW_FACTS.md#f274), [F275](../RAW_FACTS.md#f275), [F279](../RAW_FACTS.md#f279), [F280](../RAW_FACTS.md#f280) | IVAH1↔LinQH явно; H1M↔К1945ВМ3Я; HP01=16/HP02=32; power/Gen link conflicts с scope; replicas не pooling. |
| Путьмодели/версии | [F052](../RAW_FACTS.md#f052), [F053](../RAW_FACTS.md#f053), [F072](../RAW_FACTS.md#f072), [F210](../RAW_FACTS.md#f210), [F329](../RAW_FACTS.md#f329) | Guide2025route и benchmark2026 не один release; O1/O5не эквивалент DEFAULT/STAGING; CPU-only compile is a future check. |
| Guideerrata/TF | [F211](../RAW_FACTS.md#f211), [F212](../RAW_FACTS.md#f212), [F213](../RAW_FACTS.md#f213), [F215](../RAW_FACTS.md#f215), [F216](../RAW_FACTS.md#f216), [F217](../RAW_FACTS.md#f217), [F218](../RAW_FACTS.md#f218), [F219](../RAW_FACTS.md#f219) | TFnamespace и SessionNonefalsealarm снят для upstream2.14.1; tuple/GraphDef/namespace/names/compile call remains open; нет visual. |
| ONNX/modernYOLO | [F220](../RAW_FACTS.md#f220), [F221](../RAW_FACTS.md#f221), [F223](../RAW_FACTS.md#f223), [F224](../RAW_FACTS.md#f224), [F225](../RAW_FACTS.md#f225), [F228](../RAW_FACTS.md#f228), [F230](../RAW_FACTS.md#f230), [F232](../RAW_FACTS.md#f232) | opset13/static/noNMS—source choice, не потолок LinQ; noNMS у v8остается decode/DFL; input patch неполная specialization. |
| Custom adapter | [F237](../RAW_FACTS.md#f237), [F238](../RAW_FACTS.md#f238), [F239](../RAW_FACTS.md#f239), [F240](../RAW_FACTS.md#f240), [F241](../RAW_FACTS.md#f241), [F242](../RAW_FACTS.md#f242) | 4+ncvs5+nc, BCNvsBNC;85 не автоматически objectness; nc1/2/3fail; NMS import version/map/output name/in place. |
| Tiny binary/parity | [F243](../RAW_FACTS.md#f243), [F244](../RAW_FACTS.md#f244), [F245](../RAW_FACTS.md#f245), [F246](../RAW_FACTS.md#f246), [F247](../RAW_FACTS.md#f247), [F248](../RAW_FACTS.md#f248), [F249](../RAW_FACTS.md#f249), [F250](../RAW_FACTS.md#f250), [F251](../RAW_FACTS.md#f251), [F328](../RAW_FACTS.md#f328), [F333](../RAW_FACTS.md#f333) | Actual13convlineage+b1success/b2failure; anchors1,2,3vs0,1,2; NMS.6/.5/max20perclass; vendor unknown/strict not exported. |
| PTQ/quality | [F252](../RAW_FACTS.md#f252), [F253](../RAW_FACTS.md#f253), [F254](../RAW_FACTS.md#f254), [F255](../RAW_FACTS.md#f255), [F256](../RAW_FACTS.md#f256), [F257](../RAW_FACTS.md#f257), [F258](../RAW_FACTS.md#f258), [F259](../RAW_FACTS.md#f259), [F260](../RAW_FACTS.md#f260), [F261](../RAW_FACTS.md#f261) | Percentile scope/effective unknown; no TypeError retry; manual rescale не FULL; holdoutper camera/time;100/500не норма; TLM optional. |
| Runtime/ownership | [F262](../RAW_FACTS.md#f262), [F263](../RAW_FACTS.md#f263), [F264](../RAW_FACTS.md#f264), [F265](../RAW_FACTS.md#f265), [F266](../RAW_FACTS.md#f266), [F267](../RAW_FACTS.md#f267), [F268](../RAW_FACTS.md#f268), [F269](../RAW_FACTS.md#f269), [F270](../RAW_FACTS.md#f270) | Historical schema не current ABI; RAWformat ≠ RAWmode; view backing retained; exception destroy omission: mock only; Mapping/unknown-name validation есть. |
| Performance | [F130](../RAW_FACTS.md#f130), [F137](../RAW_FACTS.md#f137), [F281](../RAW_FACTS.md#f281), [F282](../RAW_FACTS.md#f282), [F283](../RAW_FACTS.md#f283), [F284](../RAW_FACTS.md#f284), [F285](../RAW_FACTS.md#f285), [F286](../RAW_FACTS.md#f286), [F331](../RAW_FACTS.md#f331) | Modern text-only; units unresolved; HPQ4×не independent proof; new wrapper rates не pure arithmetic; FPGAlogs не ASIC; noFPS → cameras. |
| Execution proof | [F287](../RAW_FACTS.md#f287), [F288](../RAW_FACTS.md#f288), [F289](../RAW_FACTS.md#f289), [F290](../RAW_FACTS.md#f290), [F291](../RAW_FACTS.md#f291), [F292](../RAW_FACTS.md#f292), [F293](../RAW_FACTS.md#f293), [F294](../RAW_FACTS.md#f294) | Lineage/coverage и request completion/device—два звена; utilisation/appbadgeweak; strict flag нет; disable_static_checker не strict. |
| IVA CV/video | [F295](../RAW_FACTS.md#f295), [F296](../RAW_FACTS.md#f296), [F297](../RAW_FACTS.md#f297), [F298](../RAW_FACTS.md#f298), [F299](../RAW_FACTS.md#f299), [F300](../RAW_FACTS.md#f300), [F301](../RAW_FACTS.md#f301), [F327](../RAW_FACTS.md#f327), [F332](../RAW_FACTS.md#f332) | 0.1.310glue → 0.1.3+p10, text-only; literal LinQ есть, H1M/PPE manifest нет;500ms/10sjob не inferenceSLA; видео не просмотрено. |
| Online/recovery | [F311](../RAW_FACTS.md#f311), [F312](../RAW_FACTS.md#f312), [F313](../RAW_FACTS.md#f313), [F316](../RAW_FACTS.md#f316), [F317](../RAW_FACTS.md#f317), [F318](../RAW_FACTS.md#f318), [F319](../RAW_FACTS.md#f319), [F320](../RAW_FACTS.md#f320), [F321](../RAW_FACTS.md#f321), [F323](../RAW_FACTS.md#f323), [F324](../RAW_FACTS.md#f324), [F325](../RAW_FACTS.md#f325), [F326](../RAW_FACTS.md#f326) | SSH необязателен; serial owner наш policy; old async/thread есть, but modern contract unknown; timeout не cancel/retry; no reset commands. |

## W1 provisional passages, которые нельзя переносить без W2

- W1-14-F02/F175 и W1-15-F16/F197: tag0.1.310 этоисторияошибочного extraction; актуальнаяпоправка[F295](../RAW_FACTS.md#f295). Неисправлятьсохраняемую W1 цитатумолча; в report пояснить 0.1.3 по page-separatedtext, не визуально.
- W1-15-F08/F189 и F09/F190 говоряткопирование outputs: [F267](../RAW_FACTS.md#f267) подтверждает view и ownedbacking, не dangling; actual current lifetime unknown.
- Общее W1«HP16/32conflict»: [F272](../RAW_FACTS.md#f272), [F279](../RAW_FACTS.md#f279) различает01/02, остаток catalog link сохраняется. Sourcepower/Gen противоречиянепобеждаютсяболееудобнойдатой.
- TFnamespaceinvalid/Session(None)crash гипотеза K003 не подтвердилась:[F215](../RAW_FACTS.md#f215), [F216](../RAW_FACTS.md#f216); importer default scope по-прежнему условный seam. TF2.14.1 не vendor pin.
- W1«noinferencehere»применимо W1/платформе:[F247](../RAW_FACTS.md#f247), [F333](../RAW_FACTS.md#f333) actual public ORT CPU inference в W2; LinQ/SDKcompile всёещёнет.
- W1«publicasync/thread не найден»: [F316](../RAW_FACTS.md#f316), [F318](../RAW_FACTS.md#f318), [F319](../RAW_FACTS.md#f319) old examples есть; modern supported contract нет. Необъявлять oneprocessperdeviceconstraint.
- W1YOLOv8rawhead называть decoded pre NMS, если exact graph подтверждает standard Detect:[F223](../RAW_FACTS.md#f223), [F238](../RAW_FACTS.md#f238). Generic85 не classic objectness; исправление typo недостаточно.
- W1family-levelTinycomparisons заменены[F245](../RAW_FACTS.md#f245), [F246](../RAW_FACTS.md#f246), [F247](../RAW_FACTS.md#f247), [F251](../RAW_FACTS.md#f251): commoncheckpointconvs не whole-model parity. Strict BGR metadata не upstreamRGBrecipe; vendor цвет unknown.

## Рекомендуемая логика человеческого отчёта

Начать с результата: публичные документы и исходники позволяют восстановить путь модели и границы интеграции, но actual release и контракт доступа сильнее всего меняют архитектуру. Порядок объяснения: продукты и версии → путь артефакта → custom detector и контраст TinyYOLO3 → квантование и численные границы → runtime и доказательство исполнения → видео и условные маршруты → производительность → первые часы, эксперименты и вопросы. Источник и статус держать рядом с числами и командами.

Человеческий отчёт нужен на русском, подробный и связный. Машинный — на английском, с YAML-полями из section17 исходного prompt: questions/answers, entity_schema, актуальность, SDK access, actual tested_here и связанные файлы. В tested_here включить реальные публичные CPU ONNX-пробы, сравнение весов и helper/mock tests; явно отделить отсутствующие vendor compile/LinQ runs. Не объявлять known-good vendor artifact или TLM обязательными во всех маршрутах. Неизвестное не означает unsupported. Редактор улучшает текст, затем работает compressor; нового сетевого поиска и отдельного финального аудитора нет.

## Единые manifests и пять владельцев

| Ролькоманды | Единственнаяответственность | Потребляет/передаёт |
|---|---|---|
| Инженерокружения/доступа | issuedmode, versions, delivery/licenses, rights/limits | environment manifest всем; не 5 параллельных inventory |
| Инженермодели/export/compile | один immutableMODEL_MANIFEST, weights/export/frontend/compiler lineage | golden model tensors+artifacts; принимает quant/eval часть |
| Инженер quantization/evaluation/data | один DATA_MANIFEST и qualitygate; thresholds/effectiveparams/PTQ | same prepared inputs/labels/splits; неповторяет runtime inventory |
| Инженер runtime/evidence/recovery | ABI/I/O/deviceproof/bench/lifecycle/concurrency | actual metadata, raw outputs, trace/timings/incident packet |
| Инженер video/controladapter/rules/UI | transport/update/frame identity/bounded queue/event association | model manifest и runtime API; не alternateexporter |

Ролифункциональные, людейне выдумывать; одинчеловекможетпередатьподзадачу, нонераздваивать manifest. MODEL_MANIFEST: source commit+weights hash, exporterpins/command/ONNXhash/IR/opsets, task/nc/names/categorymap, I/O/layout/dtype/shape, color/range/geometry, decode/NMSschema/params, calibration split+quantoptions/thresholdrefs, compile target/preset/version,.qm/.tpuhash, current runtime contract. GOLDEN_INPUT_OUTPUT: legalencodedimagehash+decodedarrayhash, preparedtensorbytes/hash/order, perframeH/W/resizedpads/scale, all named pre-NMS outputs, postNMSdetections+classmap, provider/tolerance. DATA_MANIFESTcamera/clip/time/split/labels раздельно.

## E001–E020 — стабильное дерево экспериментов, не выполненные обещания

<a id="e001"></a>
### E001 — Delivery, environment, license manifest

- Владелец: Инженер окружения/доступа.
- Доступ/предпосылки: Нужна supplied поставка либо serviceonboarding; сейчас public archive inspection уже выполнена, current install нет.
- Действия/сохраняемые артефакты: Hash/digest всех files/images; METADATA/WHEEL/entrypoints/RequiresPython/Dist; OS/ISA/kernel/glibc/native/driver/firmware pairing; license по каждому слою. Install/import тольком atchedbundle, pipcheck; для API необязателен localSDK.
- Исход/stop/предел доказательства: Успех: один воспроизводимый release иотдельно доступные operations. Ошибка: точная missing dependency/license/native, не перебирать TF/Python. Не доказывает compiler/device.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q002](../OPEN_QUESTIONS.md#q002), [Q006](../OPEN_QUESTIONS.md#q006), [Q026](../OPEN_QUESTIONS.md#q026).

<a id="e002"></a>
### E002 — Frozen model/export/golden package

- Владелец: Инженер модели/export.
- Доступ/предпосылки: Можно сейчас на CPU/RTX сразрешёнными exact weights; фактический strict/customexport в research небыло.
- Действия/сохраняемые артефакты: Weights/exporter/ONNX hashes+versions+flags; IR/allopsets/domains/attrs/functions/externals; exactI/O/prepost/classmap. PyTorch↔ORT паритетдо NMS иодинаковый decoder после; canonicalimages/tensors/geometry.
- Исход/stop/предел доказательства: Успех: immutable candidate+numericreference; не LinQ support. На export/headmismatch исправитьодинграф, не PTQ. ActualW2-EpublicCPUtest—seed, не vendor reference.
- Q: [Q003](../OPEN_QUESTIONS.md#q003), [Q008](../OPEN_QUESTIONS.md#q008), [Q009](../OPEN_QUESTIONS.md#q009), [Q019](../OPEN_QUESTIONS.md#q019), [Q020](../OPEN_QUESTIONS.md#q020).

<a id="e003"></a>
### E003 — Host custom-class decoder/NMS adapter

- Владелец: Инженер hostadapter/видео.
- Доступ/предпосылки: Можно сейчас без SDK; fulltorchNMSsuite неисполнена; W2-D только shapeprobe.
- Действия/сохраняемые артефакты: Explicit4+nc(decodedclassprob)/5+nc(objclassprob)/rawmultihead/postNMSschema; nc1/2/81, A ≠ 6, axisambiguity, empty/overlaps/classes/map/rectangularinversegeometry. PinNMSsource/import/params, clonebeforein placemutation.
- Исход/stop/предел доказательства: Успех: knownclasses/scores/boxes, failonambiguousschema; не modelquality/SDKdevice. obj.1×cls.9=.09classic долженотличатьсяот modernprob.9.
- Q: [Q003](../OPEN_QUESTIONS.md#q003), [Q020](../OPEN_QUESTIONS.md#q020).

<a id="e004"></a>
### E004 — Frontend float conversion parity

- Владелец: Инженер compile/import.
- Доступ/предпосылки: Нужен actualSDK/frontend и E001/E002; LinQ непредполагаетсяобязательнымдля converter.
- Действия/сохраняемые артефакты: Unchanged supported candidate; realtype(return), mapping, names/layout/GraphDef/namespace; compareallrawoutputstoORT собъявленной tolerance. Capture first error, minimalfailingrealgraph.
- Исход/stop/предел доказательства: Успех: frontend float parity, не quant/compile/device. Failure → локализоватьпервыйшов; не выдумывать onnx_directreplacement.
- Q: [Q008](../OPEN_QUESTIONS.md#q008), [Q009](../OPEN_QUESTIONS.md#q009), [Q010](../OPEN_QUESTIONS.md#q010).

<a id="e005"></a>
### E005 — Effective percentile/numerical quantizer factor test

- Владелец: Инженер quantization.
- Доступ/предпосылки: Нужен SDK+supported minimal graph; никакой vendor calibrate в research небыло.
- Действия/сохраняемые артефакты: Currenthelp/signature/effectiveoptions; freshobject каждый W0/W1×C0/C1×P0/P1, threshold/quantweights/scaledumps и rawoutputs; noblanketTypeErrorretry. P должныдокументированноразличать survivingoutlierdistribution.
- Исход/stop/предел доказательства: Weight/activation/joint/unsupported/unclearoutcome записать; equaloutputs не proveignored. Не APproof/QATguarantee.
- Q: [Q011](../OPEN_QUESTIONS.md#q011), [Q013](../OPEN_QUESTIONS.md#q013).

<a id="e006"></a>
### E006 — .qm/threshold save-load reproducibility

- Владелец: Инженер quantization.
- Доступ/предпосылки: SDK и E005baseline; documented load API.
- Действия/сохраняемые артефакты: Quantize → reference → save → new process → load без calibrate → same golden; normalizedmetadata/weights/outputs; thresholds roundtrip отдельноесли supported.
- Исход/stop/предел доказательства: Успехтолькоэтот graph/release; bytehash можетменятьсяиз metadata, нечисленный fail. Нет thresholdAPI → не promiseportablepickle.
- Q: [Q012](../OPEN_QUESTIONS.md#q012).

<a id="e007"></a>
### E007 — Targeted DEFAULT compile and CPU-only boundary

- Владелец: Инженер compile/import.
- Доступ/предпосылки: Matching compiler+acceptedE004/E005model; current CPU-only условиеещё unknown.
- Действия/сохраняемые артефакты: Recordtarget/preset/inputs/resources; supported DEFAULT либо matchingreleaseanalogue, неприравнивать O1/O5; capturewall/RSS/processsubtree/logs/.qm/.tpu/tensordescriptions. Device-absent topology записать; при STAGING error документированный DEFAULT новый artifact.
- Исход/stop/предел доказательства: Успех createdartifact доказывает compile толькоэтот target; hardware/quality нет. License/library/deviceerrors раздельно. TLM checkpoint optional впоставке.
- Q: [Q002](../OPEN_QUESTIONS.md#q002), [Q007](../OPEN_QUESTIONS.md#q007), [Q008](../OPEN_QUESTIONS.md#q008), [Q009](../OPEN_QUESTIONS.md#q009).

<a id="e008"></a>
### E008 — Runtime ABI/artifact metadata and physical inventory

- Владелец: Инженер runtime/evidence.
- Доступ/предпосылки: Нужен SDK/currentreader; device если readerrequiresload. Для service operator эквивалент.
- Действия/сохраняемые артефакты: Currentheader/binding/nativehashandpairing; actual artifactformat/version/UserRawdescriptors; boardSKU/serial/BDFswitch/node/runtimeinstance/quota. StandardpermittedlspciLnkCap/LnkSta раздельно; непредполагать oldJSONkeys.
- Исход/stop/предел доказательства: Успехсвязывает artifact/target/schema/allocation; неисполнил model. Нельзяпроверять pooling через OOM или oldctypes на new.so.
- Q: [Q002](../OPEN_QUESTIONS.md#q002), [Q014](../OPEN_QUESTIONS.md#q014), [Q016](../OPEN_QUESTIONS.md#q016), [Q017](../OPEN_QUESTIONS.md#q017).

<a id="e009"></a>
### E009 — One valid LinQ smoke + lineage/coverage/attribution

- Владелец: Инженер runtime/evidence.
- Доступ/предпосылки: LinQ или supplied service, matched artifact/golden+E008; vendor binary полезен, необязателенеслиесть compiler+custom example.
- Действия/сохраняемые артефакты: Singleworker/sequentialA/Bvalidinputs; exactsource/export/compiledhash, load/submit/completion/status/output; current coverage/guarantee и devicecorrelation независимо. Safeinvaliddevice/no-mapping или unknownrevisioncontrol толькоподокументированномуправу; accepted witnessalternative.
- Исход/stop/предел доказательства: Двавыводаотдельно: completion связан cLinQ; compiler покрывает agreedgraph. Одинбезвторогонезакрывает all NN claim. UIbadge/utilizationonly неравны proof.
- Q: [Q003](../OPEN_QUESTIONS.md#q003), [Q005](../OPEN_QUESTIONS.md#q005), [Q019](../OPEN_QUESTIONS.md#q019), [Q020](../OPEN_QUESTIONS.md#q020), [Q021](../OPEN_QUESTIONS.md#q021).

<a id="e010"></a>
### E010 — User/raw/reference numerical parity

- Владелец: Runtime owner + quantization owner.
- Доступ/предпосылки: SDK+LinQ+E008/E009; supported codec+goldenuser/raw, никаких guessedpackedbuffers.
- Действия/сохраняемые артефакты: Same prepared tensor; float import → quantreferencewithitsrescale → optional TLM → FULL. RAW+postequivalent толькодокументированно. Record named outputs, scale/shape/finite/errorstatisticsbeforedecoder.
- Исход/stop/предел доказательства: Локализует import/PTQ/compiler/runtimeI/O; TLMskip фиксироватькак combineduncertainty. Correct output не physical coverage. Nomsbypointertypeuint8.
- Q: [Q009](../OPEN_QUESTIONS.md#q009), [Q013](../OPEN_QUESTIONS.md#q013), [Q018](../OPEN_QUESTIONS.md#q018), [Q019](../OPEN_QUESTIONS.md#q019).

<a id="e011"></a>
### E011 — PPE task quality and calibration/eval separation

- Владелец: Инженер данных/evaluation.
- Доступ/предпосылки: Данные/fullcase; float baseline можносейчас; deviceoutputs после E009/E010.
- Действия/сохраняемые артефакты: One DATA_MANIFEST: camera/clip/time/hash/split/labels; calibration/tuning/holdout без neighborleakage. AP50/AP50:95/recall по class, size/camera/supportcounts; personPPEassociation/violationFPFN отдельно. Frozenprepost/embeddedNMS/anchors;100/500budgetcandidates не norm.
- Исход/stop/предел доказательства: E004fail → export/import; PTQonlyfail → calibration; device only fail → I/O/runtime; allparitypassesqualitybad → model/data/rules. Не overallmAP вместореспиратора.
- Q: [Q020](../OPEN_QUESTIONS.md#q020), [Q029](../OPEN_QUESTIONS.md#q029), [Q030](../OPEN_QUESTIONS.md#q030).

<a id="e012"></a>
### E012 — Quality-first cold/warm/sequential/throughput benchmark

- Владелец: Runtime owner, evaluation owner допускает artifact.
- Доступ/предпосылки: Actual LinQ allocation+E009/E011qualitygate.
- Действия/сохраняемые артефакты: Coldimport/open/load/session/firstcomplete; warmsessionb1oneoutstandingAPI wall time; common window: completed real images/sec при bounded inflight; mean/p50/p90/p95/p99/max, count, warmup/paddingexcluded. Transferscompute отдельнолишь trusted profiler; logscope/clocks.
- Исход/stop/предел доказательства: Никаких TOPS → cameras/reciprocalFPS → latency; QPStarget ≠ achieved; API wall time не tensorcorecompute. Современная slide необязательнакак baseline.
- Q: [Q022](../OPEN_QUESTIONS.md#q022), [Q023](../OPEN_QUESTIONS.md#q023), [Q032](../OPEN_QUESTIONS.md#q032).

<a id="e013"></a>
### E013 — Independent-device replicas scaling

- Владелец: Runtime owner.
- Доступ/предпосылки: E008mapping/quota, E012single device baseline, authorised2/4devices.
- Действия/сохраняемые артефакты: Sameartifact/inputs/stages;1devicevsNindependentreplicas/common steady window; perdevicecompletions/RSS/CPU/network/fairness.
- Исход/stop/предел доказательства: Успехпро throughput реплик, не singlegraphsharding/latencyN×/pooledDDR. Source wrapper чистуюарифметикунеиспользует, но actual scaling unknown.
- Q: [Q016](../OPEN_QUESTIONS.md#q016), [Q017](../OPEN_QUESTIONS.md#q017), [Q023](../OPEN_QUESTIONS.md#q023).

<a id="e014"></a>
### E014 — Video frame identity/freshness/fairness

- Владелец: Инженер video/controladapter.
- Доступ/предпосылки: Actualdata-plane/network/codecquota и E009/E012; captured stream/file сразрешённымиправами.
- Действия/сохраняемые артефакты: One clip: prepared tensors vs real decode; затем 2cameras разной cadence, reconnect epoch; bounded queue/drop/stalelog/inflight≤quota; sourcePTS/timebase+monotonictimes, geometry, model version.
- Исход/stop/предел доказательства: Успех frame association и boundedage под testedload; не норматив 8cameras. Capture unknown → receive-to-event; no host clock sync → clientRTT, невычитатьчужиечасы.
- Q: [Q004](../OPEN_QUESTIONS.md#q004), [Q023](../OPEN_QUESTIONS.md#q023), [Q030](../OPEN_QUESTIONS.md#q030).

<a id="e015"></a>
### E015 — Control/data plane custom revision roundtrip

- Владелец: Инженер video/controladapter +runtime evidence.
- Доступ/предпосылки: Ответ [Q001](../OPEN_QUESTIONS.md#q001)–Q005и actualservice/shell/jobgrant; supplied documented client, невыдуманный endpoint.
- Действия/сохраняемые артефакты: Load/registerV1hash → ready → golden request → rawresult; permittedV2update → verifyrevision/hash+knownoutput; finite2sourcesreplay с IDs/limit. Reuseexistingcompile/numerics/evidenceartifacts.
- Исход/stop/предел доказательства: Service custom success опровергаетобязательность SSH. Catalog-only илинеобновляющаяся model → R004/другой grant. Generic vendor smoke без custom update неполный success.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q004](../OPEN_QUESTIONS.md#q004), [Q005](../OPEN_QUESTIONS.md#q005).

<a id="e016"></a>
### E016 — Lifecycle, ordinary host exception, deadline, graceful worker replacement

- Владелец: Инженер runtime/evidence.
- Доступ/предпосылки: Current lifetime/recoverycontract и normal baselineE009. Nativefaulttest лишь supplied benign path.
- Действия/сохраняемые артефакты: Normalclose/reopenvalidgolden; pre-submit application validation exception → valid request; ordinary exception после terminal → documentedclose/newownworker. Ourdeadlinecollector ждёт late completion сживыми buffers; drain/close/normallyexitbeforegenerationreplace.
- Исход/stop/предел доказательства: Pre-submit error самне restarttrigger. Pendingtimeout не cancel/не duplicate; new worker не guaranteednativejobcleanup; baselinefails → firstincident packet/admin, не unboundedrespawn.
- Q: [Q015](../OPEN_QUESTIONS.md#q015), [Q024](../OPEN_QUESTIONS.md#q024), [Q028](../OPEN_QUESTIONS.md#q028).

<a id="e017"></a>
### E017 — Falsify serial-only policy with supported concurrency2

- Владелец: Инженер runtime/evidence.
- Доступ/предпосылки: Actual supported topology+reserved/authorisedallocation и E009serial baseline.
- Действия/сохраняемые артефакты: Two distinctInferenceobjects/immutableA/Binputs/IDs/outputcopies; matchingthread/asyncsample, finite count; serial baseline после close. Multiprocess толькоотдельным supportedgate.
- Исход/stop/предел доказательства: Correct2workers доказываетэтот path, не hardwareparallel/fairness/isolation. Mismatch → serial admission+packet. Исторические 8threads не greencheck.
- Q: [Q025](../OPEN_QUESTIONS.md#q025).

<a id="e018"></a>
### E018 — Conditional supplied IVA CV PPE deployment

- Владелец: Инженер video/controladapter.
- Доступ/предпосылки: Толькоесли Q027bundle+license+matchingdriver/runtime+DBseed/config/images/digests/models выданы.
- Действия/сохраняемые артефакты: MongoDB → Edge-api → projectvideoanalytics → VDMS-api → UI; knownpositive/negativefile → event/coordinates/timestamp+perNNbackend/deviceevidence; затем secondstream/reconnect.
- Исход/stop/предел доказательства: Успехконкретнойсборки, необщий publicturnkeyrecipe. Page-separated0.1.3 не actual registry tag; взять supplied digest.
- Q: [Q027](../OPEN_QUESTIONS.md#q027).

<a id="e019"></a>
### E019 — Primary PDF render/transcription clarification

- Владелец: Владелец будущего документационного уточнения; не новая рольаудита.
- Доступ/предпосылки: Нужен authoritativeoriginalPDF/pageimage; вэтойсборкенеисполнен.
- Действия/сохраняемые артефакты: Hashsourcebytes/renderactualpages; guidep7/11–14/17/19–21, presentationp2–6, IVAadminp9–18; сравнить units/tags/footnotes, сохранить old/new.
- Исход/stop/предел доказательства: Только visualtranscription/errata; не SDKsupport/measurementprotocol. Нельзяподменитьновым plaintextremoteanswer.
- Q: [Q031](../OPEN_QUESTIONS.md#q031), [Q032](../OPEN_QUESTIONS.md#q032), [Q033](../OPEN_QUESTIONS.md#q033).

<a id="e020"></a>
### E020 — Explicit single-graph multichip memory experiment

- Владелец: Инженер compile/import +runtime owner.
- Доступ/предпосылки: Толькоесли vendor поставил currentdocumentedgraphpartitionAPI/sample; notgenericstress/OOM.
- Действия/сохраняемые артефакты: One graph partition manifest, allocationsweights/activations/scratchperchip, transferedges, target mapping; golden outputs по stages; model заявленнобольше perchipavailableDDR лишьпод supportedplanning.
- Исход/stop/предел доказательства: Успехподдержанной model/schema; replicationtest неэто. Nosample → unknown, не unsupported.
- Q: [Q017](../OPEN_QUESTIONS.md#q017).

## R001–R008 — условные маршруты

<a id="r001"></a>
### R001 — Shell/container с matchingcompiler/runtime

- Условие: Actualgrant+ownmodelallowed+devices/lifecycle/network.
- Путь: E001 → E002/E004/E005/E007 → E008/E009/E010/E011 → E012/E014. Compiler можетбытьотдельным host; UIremote толькоприразрешённых ports, иначе local backend+permittedoutbound/pull.
- Граница/переключение: Shell без compiler/device permissions/long-running незакрывает route; запроситьиной supported path.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q002](../OPEN_QUESTIONS.md#q002), [Q004](../OPEN_QUESTIONS.md#q004), [Q005](../OPEN_QUESTIONS.md#q005).

<a id="r002"></a>
### R002 — Custom model service безобязательного SSH

- Условие: Upload graph+server compile либо matching.tpu; immutableversionselection, raw output contract, accepted device evidence.
- Путь: E001(service contract) → E002reference → E015V1/V2roundtrip+E009proof; E011/E012/E014. Серверможетвыполнить compilerstages, журналысохраняетоператор.
- Граница/переключение: Opaque/preparedonlyendpoint не customroute; еслинет raw outputs проверить достаточность events.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q003](../OPEN_QUESTIONS.md#q003), [Q004](../OPEN_QUESTIONS.md#q004), [Q005](../OPEN_QUESTIONS.md#q005).

<a id="r003"></a>
### R003 — Job/file-only supplied execution

- Условие: Documentedsubmit/artifact/output/queue/persistence, custom model разрешена.
- Путь: E002/E007еслинужны → E015jobroundtrip/E009proof; offline smoke быстреере altime доказательства.
- Граница/переключение: Realtime толькоесли actualboundedturnaround и frame identity удовлетворяют case; whole video upload не автоматически realtime.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q004](../OPEN_QUESTIONS.md#q004).

<a id="r004"></a>
### R004 — Catalog-only модели организатора

- Условие: Требуемыеклассы/outputs доступныи organizer принимаетготовыемодели.
- Путь: E009correlation+E011task quality+E014adapter; наши rules/UI вдопустимом scope.
- Граница/переключение: Нельзяобъявить genericCOCOdetector собственным PPE или custom weight path; если fullcase требует ownmodel, нужениной grant.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q005](../OPEN_QUESTIONS.md#q005), [Q029](../OPEN_QUESTIONS.md#q029).

<a id="r005"></a>
### R005 — Managed video inference service

- Условие: Actualcamera/file/streamcontract+custommodel/configupdates+logs/evidence.
- Путь: E015model control → E014camera/network/timestamp → E009NNproof → E011/E012servicequality/budget.
- Граница/переключение: Неотождествлятьс IVA CVEdge-api; decode/trackingplacement толькопо contract.
- Q: [Q003](../OPEN_QUESTIONS.md#q003), [Q004](../OPEN_QUESTIONS.md#q004), [Q005](../OPEN_QUESTIONS.md#q005).

<a id="r006"></a>
### R006 — Выданная IVA CV PPE project сборка

- Условие: Q027matchedassets/rights, непубличный registryURL.
- Путь: E018 плюс E009 накаждой NN boundary; model/eventconfiguration невыводитьиз UIeventlist.
- Граница/переключение: Еслинет bundle → перенеститолькоархитектурныеуроки, строить R001/R002.
- Q: [Q026](../OPEN_QUESTIONS.md#q026), [Q027](../OPEN_QUESTIONS.md#q027).

<a id="r007"></a>
### R007 — Опциональный known-good vendor artifact smoke

- Условие: Actual.tpu+matching release+goldeninput/output+proofmechanism.
- Путь: Ускоряет environmentisolationE008/E009, особенно Tiny есливыданточный recipe.
- Граница/переключение: Необязательный gate при compiler+custom example; не custom PPEvalidation и notstandalonefinalroute.
- Q: [Q003](../OPEN_QUESTIONS.md#q003), [Q019](../OPEN_QUESTIONS.md#q019).

<a id="r008"></a>
### R008 — CPU/RTX preparation до access

- Условие: Открытыеразрешённые weights/source/data и localtools.
- Путь: E002/E003/datamanifest; actualW2-EpublicCPUevidencealreadyexists.
- Граница/переключение: Не удовлетворяет mandatoryLinQcondition; не fallback длясдачи, если LinQ так ине получен.
- Q: [Q001](../OPEN_QUESTIONS.md#q001), [Q020](../OPEN_QUESTIONS.md#q020), [Q029](../OPEN_QUESTIONS.md#q029).

## Приоритет первых часов, stop/go и соседние исследования

Сначала [Q001](../OPEN_QUESTIONS.md#q001)–[Q005](../OPEN_QUESTIONS.md#q005)/E001, параллельнонезависимые E002/E003/data-split. Одинминимальный approvedartifact и E008/E009неждутвсехисследовательских lowlevel ответов. Еслиесть compiler+custom example, можноначатьимбез R007. После firstfloatexport/frontendpass → PTQ/compile → actualdevice/golden → quality → performance → video. TLM использоватьесливданнойпоставкеесть, иначевпротоколе UNAVAILABLE и combinedcompiler/runtimeuncertainty. Накаждом FAIL сохранить firsterror/artifact; менятьодин factor, непереучиватьмодель/перебиратьвесь opset×shape×preset до minimalreproducer. Deadline каждойветкивыбираеткомандапооставшимся45ч/actualelapsed; в research нетизмеренных 30–60min compile budget.

Передать `→ model_stack`: F220–F242, F251, F329–F330; raw/decoded4+nc/5+nc/NMS, classmap, immutableexportandshapeinvariants. `→ data/evaluation`: F252–F261, F331; camera/timeholdout, smallobjectsize/supportcounts, split and preprocess, embeddedNMSnonparity. `→ architecture/video`: F298–F313, F332; actualmode/quotas/frameclock/queue/age/reconnect, host boundaries conditional. `→ rules/violation`: objectrecall не absenceviolation; person↔PPEassociation, timegap/dropandversiontracking; mandatoryclassesQ029. `→ strategy/demo`: F291–F294, [Q005](../OPEN_QUESTIONS.md#q005); artifact/request/deviceproof, accepted witness, не fakebadge; modernspeedindicativeonly. Путисоседнихотчётовнеизвестны, файлыдлянихнеизобретать.




## Финальный паспорт сборки

Сохранены 174 S-карточки: 166 нормализованных внешних URL и 8 локальных протоколов или производных выписок. Это число локаторов, а не независимых источников или экспериментов. База содержит 333 F-карточки: 306 исходных факт-записей веток, 20 подробных матриц веток и 7 сводных карточек сборщика. Повторные наблюдения одного исходника намеренно сохраняют историю и не повышают силу доказательства. Дополнительно: 35 Q, 20 E, 8 R и 20 K-dispositions.

Есть реальные публичные CPU-проверки ONNX Runtime 1.31.0, сравнение весов и изолированные Python helper/mock-пробы. Никакая установка proprietary SDK, vendor conversion/calibration/compile/TLM или inference на LinQ не выполнены. Пользователь не сообщил исход регистрации. Автор должен сохранить эти границы в начале обоих отчётов и рядом с техническими результатами.

Дополнительные прямые S локальных probes: S172 — W2-D shape/schema; S173 — W1-10 dtype/geometry/argparse; S174 — W1-15 listing-expression. Их bytes прочитаны, новые проверки модели не запускались. Сводный источник actual checks — F333.
