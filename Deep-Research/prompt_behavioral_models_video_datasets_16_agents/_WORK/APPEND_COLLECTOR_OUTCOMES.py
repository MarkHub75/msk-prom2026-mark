from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent.parent
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).isoformat()
original=(R/'_WORK/CRITIC_ORIGINAL.md').read_bytes()
current=(R/'CRITIC.md').read_bytes()
assert current.startswith(original),'CRITIC no longer begins with frozen original bytes'
assert hashlib.sha256(original).hexdigest()=='891d8bcf9a2e3673d0fc7ec47288a1c71a7b8cf7fd7464f880b2277af977ac51'
if b'COLLECTOR_OUTCOMES_V1' in current:raise SystemExit('Already appended; original and outcomes left unchanged')
text=f'''

<!-- COLLECTOR_OUTCOMES_V1 -->
## Датированные исходы W2 — отдельная сборка после обеих волн

Сборка: {now}, Europe/Moscow. Роль: отдельный High collector; только сохранённые материалы, без нового сетевого поиска, моделей, training/export/compile/LinQ и без субагентов. Исходный критический текст выше сохранён **побайтно**; SHA256 frozen original `891d8bcf9a2e3673d0fc7ec47288a1c71a7b8cf7fd7464f880b2277af977ac51`. У всех семи замечаний итог **scope_narrowed**. Закрытие отдельных артефактных подпунктов не означает closure ещё не выполненного события или устройства.

<a id="K001"></a>
### K001 — scope_narrowed: exact pose payload established, full frontend remains conditional

Основание: [W2_01](_WORK/W2_01.md), [static graph](_WORK/W2_01_EVIDENCE/GRAPH.json), [archive manifest](_WORK/W2_01_EVIDENCE/MANIFEST.json), [detector graph](_WORK/W2_01_EVIDENCE/DETECTOR_GRAPH.json); канонические [F003](RAW_FACTS.md#F003), [F005](RAW_FACTS.md#F005). Полный body7 ZIP/ONNX получен/хеширован, IR6/opset11, два SimCC outputs и COCO17 по параметрам головы подтверждены; SDK1.2 RGB/CropResizePad/minSimCC разобран. Точный body7 source-PTH URL найден, но PTH parity не запускалась. Recipe detector05d8511e PTH получен. Фактический CPU demo содержит другой96154d0b detector и старую AIC+COCO pose; это контрдоказательство молчаливому объединению поставок. Python warpAffine/BGR path отличается от SDK rounded/clipped CropResizePad/RGB, numerical delta неизвестна. Tiny имеет тот же pipeline hash, меньший граф, без runtime comparison.

**Изменение решения:** можно планировать точную pose reference, но нельзя объявить готовую согласованную detector→pose→LinQ поставку. Следующий gate — matching detector export, полный runtime/prepost pin, права weights/dependencies, numerical/target-event/device execution. [Q004](OPEN_QUESTIONS.md#Q004), [E003](OPEN_QUESTIONS.md#E003), [E008](OPEN_QUESTIONS.md#E008).

<a id="K002"></a>
### K002 — scope_narrowed: four exact media clocks joined, no long hold or independent GT

Основание: [W2_02](_WORK/W2_02.md), [decode manifest](_WORK/W2_02_EVIDENCE/decode_manifest.json), [method corrections](_WORK/W2_02_EVIDENCE/METHOD_NOTES.md); [F008](RAW_FACTS.md#F008). Три точных GMD оригинала и URFD adl10 preview декодированы полностью с PTS; GMD converter copy и decoder source устанавливают **stream-relative**, а не raw-PTS join для этих bytes. S1 raw start.033333/last6.0974 не противоречит label end6.08: last relative6.064067 внутри. Ранний raw-clock tail diagnostic superseded. Это не package-wide conversion run и не всеобщий clock сертификат.

Observed labelled horizons3.364067/1.148067/2.184167/3.338s не равны неподвижности; S4 падает на кровать/кушетку, UR adl10 садится/ложится на диван и частично обрезан. Ни один из **этих четырёх** не даёт10/30s post-transition hold либо полный recovery/clear/rearm. Это не отсутствие длинных видео во всём корпусе. Subject4 source-test member после review — development. UR preview ordinal join не доказывает canonical PNG pixel identity/capture clock. MIT/CC BY4 GMD grants сохранены; OmniFall NC/SA conflict и UR noncommercial scope отдельно.

**Изменение решения:** готов конкретный clock/semantics development fixture для короткой transition проверки; длительный hold, independent operational GT и промышленный lockbox остаются внешним экспериментом. [Q005](OPEN_QUESTIONS.md#Q005), [E002](OPEN_QUESTIONS.md#E002), [E004](OPEN_QUESTIONS.md#E004).

<a id="K003"></a>
### K003 — scope_narrowed: native spatial alignment and opportunity arithmetic, origin still uncertain

Основание: [W2_03](_WORK/W2_03.md), [mapping](_WORK/W2_03_EVIDENCE/mapping.json), [phase/drop opportunity](_WORK/W2_03_EVIDENCE/phase_observability.json), [duplicate audit](_WORK/W2_03_EVIDENCE/duplicate_audit.json); [F009](RAW_FACTS.md#F009). Native1× CAVIAR center boxes и BEHAVE top-left boxes согласуются; гипотеза2×BEHAVE отвергнута. Global−35450 даёт нужный subclip. ±1origin остаётся неоднозначным; synthetic i/25 evaluation clock не восстановленное physical capture time. У CAVIAR repeated/nonincreasing PTS соответствуют новым RGB images, не доказанным adjacent duplicates. BEHAVE25Hz acquired video не заменяется XML full-source1FPS.

Групповые nested RunTogether rows не стали dense gait truth всех людей; крайний actor6 bbox7×4 показывает ограничение видимости. Полный phase sweep1/2/5/native и заданные random/burst потери выполнены как annotation arithmetic, не recognition. Возможность zero1FPS observations не модельный recall.

**Изменение решения:** reproducible sanity/reserve pack с документированными clock/scale границами; headline gait acceptance требует per-actor visibility/physical-action truth, origin sensitivity и target fast-walk/brief-burst tests. [Q006](OPEN_QUESTIONS.md#Q006), [E006](OPEN_QUESTIONS.md#E006).

<a id="K004"></a>
### K004 — scope_narrowed: exact AVA route failures and desk-phone fallback, phone stays reserve

Основание: [W2_04](_WORK/W2_04.md), [player1](_WORK/W2_04_EVIDENCE/player_1.json), [player2](_WORK/W2_04_EVIDENCE/player_2.json), [Charades clock](_WORK/W2_04_EVIDENCE/clock_checks.json), [source row](_WORK/W2_04_EVIDENCE/charades_original_row.json); [F010](RAW_FACTS.md#F010). Два exact YouTube cases возвращают playerERROR без media; первый сообщает copyright removal on Reliance Entertainment request, второй unavailable без причины. HTML200 не playable video; это локализованный failure, не всё AVA отсутствует.

Charades2RFLZ полностью inspected по222frames/PTS, один видимый actor, reach→ear→return возле стола. Script/cord контекст — desk phone. Concurrent walking+use не установлено; broad c0193.0–10.4 не dense ear-use onset. Нет source actor/phone boxes/ID и walking interval. AVA sparse77person-seconds и UPT image pair не складываются в проверенную одну цепочку. Positive AVA annotation CC BY4 и Charades research/evaluation scope сохранены; source copyright/public redistribution отдельно.

**Изменение решения:** phone-use при equipment work **или workshop movement** остаётся reserve; нужен permissioned target same-actor visible-device/concurrence pack с radio/scanner/tool/allowed-phone controls, затем reference/event/device. [Q007](OPEN_QUESTIONS.md#Q007), [E002](OPEN_QUESTIONS.md#E002).

<a id="K005"></a>
### K005 — scope_narrowed: real routine moving forklift confirmed, risk and scope not closed

Основание: [W2_05](_WORK/W2_05.md), [decode](_WORK/W2_05_EVIDENCE/decode.json), [checkpoint static map](_WORK/W2_05_EVIDENCE/checkpoint_static.json), [official scope notes](_WORK/W2_05_EVIDENCE/official_web_notes.md); [F011](RAW_FACTS.md#F011). Полный60s Camera0000/hash/1800PTS подтверждён, sampled full-timeline review показывает отдельных workers и advancing driven forklift/reach-truck с operator-like context. Это **routine passage/co-presence**, не certified near-miss, metre risk или policy event; полного stationary-near/moving-far/driver/reverse/turn control set нет.

Точный detector acquired/hash/static map0forklift/1person, противоположный AI City numeric order. Положительные CC BY4 и official download statements сохранены. В той же текущей revision Croissant/paper hidden-target/privacy/train wording остаётся unresolved contradiction/scope. FAQ challenge protocol не универсальная external copyright prohibition. Real GT/depth withheld; calibration не independent safety survey.

**Изменение решения:** “нет подтверждённого реального machine footage” больше неверно, но moving-machine hazard остаётся supplementary reserve. Нужны разрешение на exact intended reuse, target pair-event GT/driver/motion controls и surveyed envelope; не обучать на challenge test и не считать синхронные views новыми hours/events. [Q008](OPEN_QUESTIONS.md#Q008), [Q009](OPEN_QUESTIONS.md#Q009), [E007](OPEN_QUESTIONS.md#E007).

<a id="K006"></a>
### K006 — scope_narrowed: flame artifact and full manifest closed, mist video UNCONFIRMED

Основание: [W2_06](_WORK/W2_06.md), [checkpoint static](_WORK/W2_06_EVIDENCE/checkpoint_static.json), [complete RAR manifest](_WORK/W2_06_EVIDENCE/mmodalfire_manifest.json), [sensor audit](_WORK/W2_06_EVIDENCE/sensor_csv_audit.json), [actual short video decode](_WORK/W2_06_EVIDENCE/small_video_decode.json); [F012](RAW_FACTS.md#F012). Exact current fire best.pt acquired/hash/map0smoke1fire/explicitAGPL подтверждены статически. MmodalFire RAR non-solid103members manifest reached exact end/valid headers; full archive checksum не проверен. Workbook mist/dry-ice sessions и Humidifier4sensor pair получены.

Единственное извлечённое короткое видео имеет clock Aug2~09:33, вне Aug4dryice/Aug10mist. **Mist video UNCONFIRMED**, не actual negative GT. Opaque-member mapping и bigger selected member acquisition остаются открыты.28raw videos/38settings versus65paper experiments/two labs — unresolved units/layout, не65false. Binary sequence/midpoint windows не dense ignition/clear/rearm. Factory steam/allowed furnace/welding/permit controls не получены.

**Изменение решения:** narrow visible-flame development route доступен, ready industrial event MVP не установлен. Smoking/ownership отдельно; AGPL/CC BY/MIT positive grants не заменяют upstream/target-media review. [Q010](OPEN_QUESTIONS.md#Q010), [E002](OPEN_QUESTIONS.md#E002), [E004](OPEN_QUESTIONS.md#E004).

<a id="K007"></a>
### K007 — scope_narrowed: streaming signatures established, task-specific event head absent

Основание: [W2_07](_WORK/W2_07.md), [float graph](_WORK/W2_07_EVIDENCE/static_graph.json), [INT8 graph](_WORK/W2_07_EVIDENCE/int8_static_graph.json), [INT8 model grant](_WORK/W2_07_EVIDENCE/kaggle_int8_metadata.json); [F013](RAW_FACTS.md#F013). Full float27.14MB и INT8variant3.276MB hashes/static signature44/44 image+43states/logits+43states получены. FLOAT32 external image/buffers/logits и INT32 counters сохранены; int8内部 computation не int8IO. Model-instance Apache2 grant положительно установлен для INT8.

Обе головы аккумулируют prefix feature sum/count. Float также держит block cumulative pools; INT8 — **другая modified architecture**,30block state I/O identities после removal squeeze/excitation, head active. Это не чистая float→INT8 precision pair. Нет embedded PTS/actor/policy или onset/clear. K600 class map exact, но nearest action name не industrial head. Cold-start/prefix dilution/persistence/reset/cadence — будущие controls, не измеренный temporal behavior. Historical Pixel4/blog numbers не LinQ/float/event performance.

**Изменение решения:** есть воспроизводимый static first-run contract, но MoViNet остаётся generic training/video donor, не критический готовый hazard frontend. Нужны relevant target labels/head, state lifecycle reference, causal event ablation и exact device path. [Q014](OPEN_QUESTIONS.md#Q014), [E005](OPEN_QUESTIONS.md#E005), [E006](OPEN_QUESTIONS.md#E006), [E008](OPEN_QUESTIONS.md#E008).

Все закрытые подпункты ограничены конкретными bytes/источниками/часами/операциями выше. Ни один K outcome не утверждает numerical parity, real industrial event quality, safety certification, legal clearance beyond observed grant, либо LinQ execution. Следующий конвейер — отдельный автор, редактор и сжиматель, без третьей поисковой волны или финального аудитора.
'''
with (R/'CRITIC.md').open('ab') as f:f.write(text.encode('utf-8'))
print(json.dumps({'appended_at':now,'frozen_prefix_preserved':(R/'CRITIC.md').read_bytes().startswith(original),'outcomes':7,'status':'scope_narrowed'},indent=2))
