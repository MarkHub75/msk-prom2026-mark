"""Append W2 handling and prepare author handoff; offline assembly checks only."""
import COLLECTOR_CURATE as cc
import BUILD_COLLECTOR as c
from pathlib import Path
import re,json,hashlib,math

K=[
 ('K001','Уточнена область; проектный пробел закрыт, LinQ lifecycle остаётся открыт',
  'AWS Batch даёт конкретное ограничение cancel200/attempt timeout/history retention. Persisted intent+held до возможного send, separate local/control/fetch budgets, ambiguous submit и restart traces, finite STOPPED. Local deadline/Gap/source reset не release remote obligation; stale backup не held=0. Не требуется ждать всех unknown, если свободный остаток доказан; при недостоверном ledger/namespace stop.',
  'W2-01-F01 W2-01-F03 W2-01-F05 W2-01-F06 W2-01-F10 W2-01-F11 W2-01-F12 W2-01-F13 W2-03-F09 W2-05-F11 Q002 E007 E016',
  'LinQ idempotency/lookup/quota/terminal/TTL/acceptance cutoff и borrowed-buffer release неизвестны; fake fixture не выполнен.'),
 ('K002','Уточнена область; runtime exact mapping остаётся открыт',
  'Pinned MediaMTX mtxi сильнее UTC filename, но StreamID — recorder generation, не decoder/source epoch. Hooks/API не отдают необходимые lineage поля; native get теряет mtxi, HTTP200 не полнота. Preferred prospective route — один demux, packet index до mux rebase, distinct generations, independently validated coverage. Early E009 обязателен; fail→analyzed snapshot/native archive mapping unknown.',
  'W2-02-F01 W2-02-F03 W2-02-F04 W2-02-F05 W2-02-F06 W2-02-F09 Q010 E009 E018',
  'Packet lifetime/reorder/rescale/missing PTS/main-sub uncertainty не испытаны. Если exact clips обязательны, snapshot cut остаётся blocker.'),
 ('K003','Закрыто как bounded project policy; operational полнота открыта',
  'Finite evidence acceptance от EARLIEST anchor, post-roll monotonic deadline, bounded close/job/chunks/rollover/incident bytes, persisted future pins/reservations и low-space/crash lifecycle. Unbounded queue не покрывается finite ring. H40s и bounds20/5/5/2/1/4/30 — fixture assumptions, не LinQ SLA/кейс.',
  'W2-02-F02 W2-02-F07 W2-02-F08 W2-02-F10 W2-02-F11 W2-02-F12 Q011 Q012 E010 E016',
  'Actual GOP/max bitrate/FS/close/dispatch bounds, evidence requirements и real result delay неизвестны; no false-complete/byte/lifetime tests не выполнены.'),
 ('K004','Уточнена область; DOC/CODE/project часть закрыта, runtime открыта',
  'Выбран standalone websockets17.0.1 asyncio route. Credit занят ДО send, один outstanding/connection, exact ACK после draw, serial sender/renderer, active+closing cap, immutable latest/history payloads, hidden→close/latest resync, local credit-cycle guard и source/view lifetime раздельны. Timeout terminal, не новый credit. send/drain/ping/browser bufferedAmount не renderer evidence.',
  'W2-03-F01 W2-03-F02 W2-03-F03 W2-03-F04 W2-03-F05 W2-03-F06 W2-03-F07 W2-03-F08 W2-03-F09 W2-03-F10 Q013 E011 E012',
  'App-owned bytes bound не process/kernel/browser total RSS; public close_timeout не hard teardown guarantee. Experimental transport.abort subclass не public WS API; physical display/read/actual network/SDK borrowing открыты.'),
 ('K005','Противоречие timestamp-only гипотезе установлено; область исправлена, quality открыто',
  'Pinned ByteTrack dt1/update; constructor frame_rate меняет lost buffer, no-call останавливает aging, real empty(0,5) меняет track state. PTS envelope не исправляет динамику. Minimum tracker optional по fixed-cadence/reset gate, separate tracking_generation; ID-dependent метод без gate degraded/unsupported. Per-camera1/E[L] с NMS/cascade/apply отдельно от aggregateK; sparse sent-ID reorder и независимый timeout wakeup.',
  'W2-04-F02 W2-04-F03 W2-04-F04 W2-04-F05 W2-04-F06 W2-04-F08 W2-04-F09 W2-04-F10 W2-04-F11 W2-04-F12 W2-04-F13 Q005 Q007 Q021 E006',
  'Domain minFPS/maxgap/dwell/ID quality, installability и real full cycle неизвестны; code read не measured tracker quality.'),
 ('K006','Параметрический пробел закрыт; actual capacity остаётся открыта',
  'R_return, raw/compact shape example, polling/status/fetch CPU/RAM добавлены отдельно от input uplink. Viewer fanout по selected tiles, не registered camera count. Complete memory/process/FD/session/DPB/surfaces/pool/IO replay+backup inventory. Directional50/500; remote decode с local processed projection добавляет analyzed JPEG return либо требует granted colocated app data plane.',
  'W2-01-F14 W2-01-F15 W2-01-F16 W2-06-F01 W2-06-F02 W2-06-F03 W2-06-F04 W2-04-F10 Q022 Q025 E005 E008',
  'Actual output/model profiles, WAN↑↓/goodput/tails, LinQ Cinf/Kremote и OS/resource coefficients не measured. Нет числа плат/500-camera guarantee.'),
 ('K007','Уточнена область; coherent provisional manifest есть, installability не доказана',
  'Выбраны MediaMTX1.21.2 server+optional same-tag reader, PyAV16.0.1, CPython3.12.15 source candidate, websockets17.0.1, linked patched SQLite3.51.3/source_id gate. CLI FFmpeg и wheel libav разные artifacts. Linux wheel read-only inspected с native library/license strings; wrapper BSD не весь bundle. Used-as-process/dependency/copied-code/idea-only и exact expected hashes в manifest.',
  'W2-05-F01 W2-05-F02 W2-05-F03 W2-05-F04 Q015 Q016 E015',
  'CPython source-only, actual binary/ABI/OS/ISA/images/SQLite linkage/transitive notices/weights/proprietary bundle неизвестны. No install/smoke; W1 catalog не lockfile.'),
 ('K008','DB/backup/reconcile proposal закрыт; operational durability открыта',
  'Одна local SQLite DB/one writer, WAL+FULL/FK/bounded busy и successful COMMIT boundary, patched engine gate. Long reads/WAL/checkpoint и disk-full учтены. Supported Connection.backup + verified closed-media inventory/holds/cutoff; restore fences owners, проверяет DB/FK/media, rebuild pins до deletion и reconciles remote obligations после old backup. File publish/delete — отдельный protocol.',
  'W2-05-F02 W2-05-F05 W2-05-F06 W2-05-F07 W2-05-F08 W2-05-F09 W2-05-F10 W2-05-F11 W2-05-F12 Q012 Q015 E016',
  'Actual FS/VFS/cache/sync, runtime code, power/disk-loss, RPO/RTO не tested. FULL/hash/atomic rename не универсальная сохранность; старый backup не release remote work.'),
 ('K009','Уточнена область; scope gap закрыт, threshold quality открыта',
  'Первичный Axis product example с unsuitable/lighting/occlusion/legitimate move ограничениями. Разделены transport dead, stale PTS, repeated content, black/underexposed, overexposure, blur, scene shift и counterexamples. Mandatory progress/age; optional image signals only suspected_anomaly с per-scene baseline, suitability и CPU budget.',
  'W2-06-F06 W2-06-F07 W2-06-F08 Q023 E019',
  'Не испытаны actual камеры/сцены/heuristics; нет universal thresholds/causal tamper proof. Overexposure candidate — наш hypothesis, не заявленная Axis capability.'),
 ('K010','Закрыто как последовательный conditional engineering proposal; real feasibility открыта',
  'Одна модульная app topology, bounded scheduler/actor, actual LinQ adapter, one SQLite writer, early-gated same-demux remux или snapshot cut, own-frame processed view. Per-access placement, unsupported-live GUI/job,5owners, gates/cuts0–45ч, per-mode stage/clock/bound/failure budgets и discriminating E сформированы с finalW2_01..05. Golden real LinQ run приоритетен.',
  'W2-06-F09 W2-06-F10 W2-06-F11 W2-06-F12 Q001 Q005 Q024 E001 E018',
  'Нет полного кейса/grant/actual golden/full-chain prototype/effort proof.2camera не50/500,225person-hours не schedule feasibility; обязательный exact clip нельзя закрыть необязательным snapshot.'),
]

def critic():
    path=c.ROOT/'CRITIC.md';saved=c.WORK/'CRITIC_ORIGINAL.md'
    if not saved.exists():saved.write_bytes(path.read_bytes())
    original=saved.read_bytes()
    out=['\n\n## Collector: результаты содержательной W2 (2026-10-23)\n',
      'Исходный раздел критики выше сохранён byte-for-byte; нижние статусы относятся только к последующей обработке. Это не финальный аудит отчётов. Новых сетевых или runtime доказательств collector не получал. `Закрыто как proposal` не означает выполненный эксперимент.\n']
    for kid,status,change,refs,unknown in K:
        out += [f'<a id="{kid.lower()}-w2"></a>\n',f'### {kid} — {status}\n',f'**Результат W2 / изменение решения:** {change}\n',f'**Доказательства и проверки:** {cc.link_ids(refs)}.\n',f'**Сохраняемая неизвестность:** {unknown}\n']
    path.write_bytes(original+'\n'.join(out).encode('utf-8'))
    assert path.read_bytes().startswith(original)
    return hashlib.sha256(original).hexdigest()

def hlinks(text):
    return cc.link_ids(text).replace('](SOURCES.md#','](../SOURCES.md#').replace('](RAW_FACTS.md#','](../RAW_FACTS.md#').replace('](OPEN_QUESTIONS.md#','](../OPEN_QUESTIONS.md#')

def fref(old):return hlinks(old)
def handoff():
    out=['# COLLECTOR_HANDOFF — вход High автора video_architecture\n',
      'Статус: обе6W1/6W2 содержательно собраны; исходный fresh-context CRITIC сохранён,10K статусов дописаны ниже. Автор создаёт связный русский черновик, новую сеть/SDK/замеры не получает. Все важные условия и unknown остаются рядом с выводом. Это навигация и данные для автора, не литературный отчёт.\n',c.PROVENANCE,
      '## Файлы и точные ссылки\n',
      '- [SOURCES](../SOURCES.md): primary chains/revisions, access отдельно от publication, snapshots/local locators и supporting F.\n- [RAW_FACTS](../RAW_FACTS.md): подробные extraction records в13тематических группах; команды/configs/версии/units/conditions/negative cases сохранены.\n- [OPEN_QUESTIONS](../OPEN_QUESTIONS.md):25сведённых вопросов и19E с decision/inputs/steps/metrics/outcomes/limits; E все PROPOSED/NOT RUN.\n- [CRITIC](../CRITIC.md): оригинал + K001..K010 W2 results; точный статус anchor `#k001-w2` и далее.\n- [ID_MAP](ID_MAP.md): native→stable, включая составные F/общие primary chains и catalog supplemental F.\n- [COLLECTOR_STATE](COLLECTOR_STATE.json), [CURATED](COLLECTOR_CURATED.json): машинная служебная карта, не новые итоговые отчёты.\n',
      'Перед каждым stable record есть явный HTML anchor: `../RAW_FACTS.md#f001`, `../SOURCES.md#s001`, `../OPEN_QUESTIONS.md#q001`/`#e001`. Из корневых отчётов убрать `../`. Не ссылаться на автоматический длинный heading slug/turn IDs. Native IDs в provenance не отдельные measurements.\n',
      '## Быстрый маршрут чтения тематической базы\n',
      '| Тема автора | Главные stable записи | Что сохранять |\n|---|---|---|\n',
      '| Доступ/маршруты/реальный LinQ | '+hlinks('W1-01-F01 W1-01-F05 W1-01-F06 W1-01-F07 W2-01-F10 W2-01-F13 W2-06-F09 Q001 Q002')+' | Нет issued grant; shell/API/jobs/GUI — условия, не выданные возможности |\n',
      '| Ingress/decode knobs | '+hlinks('W1-02-F02 W1-02-F03 W1-02-F04 W1-02-F05 W1-02-F06 W1-02-F07 W1-02-F08 W1-02-F09 W1-02-F10 W1-02-F13 W1-02-F14 W1-02-F28')+' | timeout units/defaults, post-decode dropping, open-only, loop TCP и epoch |\n',
      '| Payload/quality/return | '+hlinks('W1-03-F11 W1-03-F12 W1-03-F15 W1-03-F16 W2-01-F14 W2-01-F15 W2-01-F16')+' | JPEG size variable; class/size recall; raw outputs/NMS/polling в отдельном направлении |\n',
      '| Scheduler/temporal | '+hlinks('W1-04-F15 W1-04-F16 W1-04-F17 W1-04-F18 W2-04-F02 W2-04-F04 W2-04-F06 W2-04-F09 W2-04-F10 W2-04-F11 W2-04-F12 W2-04-F13')+' | source clocks/gaps vs result arrival; sparse sent IDs; fixed dt не меняется PTS;1/L не aggregateK |\n',
      '| Event/outbox/DB | '+hlinks('W1-04-F19 W1-04-F20 W1-04-F21 W1-04-F22 W1-04-F23 W1-04-F25 W1-04-F28 W2-05-F05 W2-05-F06 W2-05-F07 W2-05-F09 W2-05-F10 W2-05-F11 W2-05-F12')+' | volatileframes/durableevents, successfulCOMMIT, duplicatewindow, patchedruntime/backup/pinrebuild/remoteheld |\n',
      '| Evidence mapping/finite disk | '+hlinks('W1-05-F01 W1-05-F04 W1-05-F08 W2-02-F02 W2-02-F03 W2-02-F04 W2-02-F05 W2-02-F09 W2-02-F10 W2-02-F11 W2-02-F12')+' | recorder≠decoder generation; segmentminimum; earlyproof/snapshotcut; late/partial/unavailable |\n',
      '| Browser | '+hlinks('W1-05-F10 W1-05-F13 W1-05-F18 W1-05-F20 W2-03-F03 W2-03-F05 W2-03-F06 W2-03-F07 W2-03-F08 W2-03-F09 W2-03-F10')+' |1rendercredit/connection, TTLviews≠borrows; closingcounts; hardRSS/teardown未知 |\n',
      '| Measurement/resilience/health | '+hlinks('W1-06-F01 W1-06-F04 W1-06-F05 W1-06-F06 W1-06-F13 W1-06-F14 W2-06-F06 W2-06-F07 W2-06-F08 W2-06-F11')+' | vendorconditions, wholedenominator/clockerror/censoring; suspectedimageanomaly |\n',
      '| Deployment/catalog/capacity/minimum | '+hlinks('W1-01-F17 W1-01-F18 W1-06-F15 W2-05-F01 W2-05-F02 W2-05-F03 W2-05-F04 W2-06-F02 W2-06-F03 W2-06-F04 W2-06-F10')+' | W1snapshots≠lock, nativebundlescope, directions/resourceinventory,5owners/gates/cuts |\n',
      '## Установленные выводы и условные рекомендации\n',
      '1. **Доказано источниками/кодом:** library knobs/version caveats, interframe decode vs sample, native recorder metadata/generation limits, fixed-step tracker semantics, WS send/close/queue directions и patched SQLite/backup mechanisms. Это чтение первичных материалов; наши runtime tests не выполнялись.\n2. **Вычислено локально:** payload/storage/pixels/occupancy scenarios с явными inputs; это не benchmark камеры/платы.\n3. **Рекомендуемый proposal:** модульное приложение, один логический actor/camera, bounded stateless scheduler/bytes/remote credits, actual LinQ adapter, one local DB writer/outbox, own-frame processed view. MediaMTX — relay; custom indexed remux допускается ранним E009, иначе snapshot cut. Не добавлять broker/NVR/NVIDIA runtime ради схемы.\n4. **Неизвестно:** actual grant/full case/model output/NN boundary/LinQ Cinf/runtime safety/source profiles/quality/network/target FS и реальная45ч feasibility. Ни один proposed route не назвать экспериментально работающим.\n',
      '## Матрица LinQ для конечного решения\n',
      '| Выданный mode | Размещение | Gate / честный исход |\n|---|---|---|\n',
      '| Image/tensor API | Team: ingest/decode/preprocess/state/DB/record/UI; remote: documentedNN/pre/post | Input/output/schema/modelupdates/witness, bytes/quotas/lifecycle; tensor dtype/shape не подменять |\n',
      '| Shell + own persistent daemon + source ingress + CPU/codec/storage/ports grant | Единый app data plane/DB/recorder/projection рядом с decoder; supplied proprietary worker отдельной deployment unit | Всеpermissions/persistence/network/privacy подтверждены. Если localprojectionнужна, считатьretainedimage+compactreturn, неmetadataonly |\n',
      '| Shell, только ephemeral NN worker | Team app как API route; thin remote worker в supplied env | SSH не root/Docker/DB/persistence. Loss/restart→remote reconcile |\n',
      '| Job API/shared queue | Team persistedledger/collector, fair latest scheduler, queue+poll+fetch+post в fullcycle | Live только при lifecycle/return/freshness/per-camera gates. Unbounded delay→bounded stop/degraded/offline; evidence finite |\n',
      '| GUI/manual либо job без usable result/turnaround | Witnessed/offline LinQ run + честно marked replay/mock product flow | Unsupported-live; click automation/CPU/RTX не закрывают real-time LinQ requirement |\n',
      'Общая очередь — дополнительная ось любого mode, VPN — network transport. Managed-video/events-only endpoint требует своего model/classes/timestamp/output contract; его наличие не установлено.\n',
      '## Расчёты50/500: формулы и допущения\n',
      'Все значения ниже — **INFERENCE/LOCAL arithmetic**, не hardware/source measurements. SI:1kB=1000B,1MB=10⁶B,1GB=10⁹B,1TB=10¹²B; Mbit/s=10⁶bit/s. Scenario: N50/500, source1080p25, main4Mbit/s, optional720p25 sub1Mbit/s, analysis5fps, JPEG100000B/frame. JPEG size/quality и modeloutput не установлены. Units/stride/copies/transport/retransmits/VBR tails/reserve учитывать дополнительно.\n',
      '| Величина / формула |50камер|500камер|Граница |\n|---|---:|---:|---|\n',
      '| Camera→gateway main N×4Mb/s |200Mb/s|2Gb/s|Compressedingest, не API uplink того же full-duplex segment |\n',
      '| Main+sub N×(4+1)Mb/s |250Mb/s|2.5Gb/s|Если оба приходят в узел |\n',
      '| JPEG uplink 8NfE[J] |200Mb/s|2Gb/s|При100kB×5fps=4Mb/s/camera: экономии противmain4нет |\n',
      '| Tensor640²RGB uint8:8Nf×640×640×3 |2.4576Gb/s|24.576Gb/s|Только при actual uint8 contract |\n',
      '| Тот же FP32 ×4 |9.8304Gb/s|98.304Gb/s|4915200B/frame; input dtype не произвольный выбор |\n',
      '| Raw1080p NV12×5fps:8NfWH×1.5 |6.2208Gb/s|62.208Gb/s|Nominal8bit420, без stride/copies |\n',
      '| Raw1080p RGB×5fps:8NfWH×3 |12.4416Gb/s|124.416Gb/s|Raw1080p frame6220800B |\n',
      '| Remote→client rawhead:8Nf×(1×84×8400×4) |5.6448Gb/s|56.448Gb/s|2822400B/frame, условный shape/dtype, не выбранная NN |\n',
      '| Remote→client compact:8Nf×(100×24+4) |4.808Mb/s|48.08Mb/s|≤100packed records coords/score/class, без envelope, не JSON/masks |\n',
      '| Remote decode→local projection sampledJPEG return |+200Mb/s|+2Gb/s|Если все analyzed images возвращаются укоманды; иначе colocated projection→selectedtiles |\n',
      '| Viewer egress8ΣvΣtile f×E[J] |19.2Mb/s|19.2Mb/s|3viewers×4selectedtiles×2fps×100kB; не всеregisteredcamera |\n',
      '| Main storage/day=N×10.8×b GB |2.16TB/day|21.6TB/day|Приb4Mb/s;43.2GB/camera/day |\n',
      '| Main30days |64.8TB|648TB|Payload безFS/replicas/резерва/backup |\n',
      '| Main7days |15.12TB|151.2TB|Тежеусловия |\n',
      '| Compressed ring40s=N×b×40/8 MB |1GB|10GB|20MB/camera при4Mb/s; реальныйcapпоmaxbitrate+overshoot/parts/reserve |\n',
      '| Decode1080p25=NWHf_source |2.592GPix/s|25.92GPix/s|FullsourceFPS, не analysis5 |\n',
      '| Decode720p25 |1.152GPix/s|11.52GPix/s|Разрешение не задаёт автоматическиbitrate |\n',
      '| One nominal1080p NV12 latest slot=NWH×1.5 |155.52MB|1.5552GB|Не totalRSS/VRAM |\n',
      '| One nominal1080p RGB slot=NWH×3 |311.04MB|3.1104GB|DPB/surfaces/contexts/pools/borrows/outputs/view/DBсверх |\n',
      '| Required source observations N×5 |250/s|2500/s|Secondary crops/modelinvocations отдельно |\n',
      'Control: `q_poll≈ceil(J_jobs/b_query)/Δ`; status↑↓=8q×measuredrequest/responsebytes. FixtureJ50/Δ0.5/b1→100calls/s;1kBup/2kBdown→0.8/1.6Mb/s. Idealpollwait[0,Δ),meanΔ/2 толькоperiodic/nooutageuniformphase; actualvisibility/backoffunknown. Неуменьшатьresponsebytesпропорциональноbatchqueryавтоматически.\n',
      'Viewer1credit/connection:4tiles×2fps требуют8messages/s иидеальноACKcycle≤125ms. Несколькоtilesневыдаютнесколькоcredits. ОдинJPEGencode/sourceframeнеубираетVcopiesNIC. Replay/seek/clipdownloads/backupдобавляютсяповерхlive.\n',
      'Concurrency: necessary per-camera `f_req_i≤p_i/E[L_i]`, гдеLполныйциклсNMS/cascade/apply. Приp1,L300ms ceiling3.33fps:globalK100нелечиткамеру. Necessarymeans`Σf_i E[L_i]≤K_local`; remoteoccupancy`Σ_i f_i E[Σjobs L_rj]≤K_remote`, учитыватьcorr(q,L), actualquotaunits иunknownheldпослеliveGap. Little-lawmeansнеp95/p99/maxgap.\n',
      'Aggregate Nmax — minimum measured usable inference/decode/preprocess/input/return/postCPU/network/storage/RAM/FD/session budgets **после** per-camera temporalgate. `S=N*b*T/8`; `Cwrite` измерять вместеreplay/hash/backup; `mcam` измеритьactualbackend. Theoreticalops/TOPS не Cinf. ГипотетическийCinf300fps,u0.7→210effective:ceil(250/210)=2узла,ceil(2500/210)=12; приCinf1000,u0.7→1/4. Это не LinQ numbers/закупка, другиеbottlenecksмогутувеличитьчисло.\n',
      '## Benchmark conditions, которые нельзя потерять\n',
      hlinks('W1-02-F21 W1-06-F01')+' — NVDEC13.0 Ada indicative:1920×1080YUV420/Windows11/SDK13/video2160MHz/perengine,H264903/HEVC1641/Main101520/AV11018fps. Не actual4070/backend/fullservice. DeepStream7.1T4:dualXeonE5-2650v4/48threads,T4clock1513MHz,Ubuntu22.04,driver535.161.08,CUDA12.2,TRT8.6.1.6;1080p30files,PGIETrafficCamNet batchN interval0,IOU960×544,2SGIEResNet18batch32async,tiler/render/OSDoff;45H265/31H264streams. НетWAN/UI/p95/p99/duration/LinQпереноса. Подробныйmemoryliteral/contextвRAW, не исправлятьпо памяти.\n',
      '## Provisional selected baseline и точные артефакты\n',
      hlinks('W2-05-F01 W2-05-F02 W2-05-F03 W2-05-F04')+'; authoritative [PROVISIONAL_ARTIFACT_MANIFEST.json](MATERIALS/W2_05/PROVISIONAL_ARTIFACT_MANIFEST.json). Везде selection=provisional, installation_evidence=none.\n',
      '| Компонент | Pin/artifact | Роль/license/gate |\n|---|---|---|\n',
      '| MediaMTX |1.21.2,914e39535ece709919ac325aaeed98d394ed9093|relayprocess/MIT; actualbinary/imageOS/ISA/digestunknown; optionalreaderтотжеtag |\n',
      '| PyAV |16.0.1,7687256d87f22f78cb75bb4aba94dc6e504c9983|decode/prospectiveremux,Python≥3.10;BSDwrapper≠nativebundle |\n',
      '| LinuxPyAVwheel |av-16.0.1-cp312-cp312-manylinux_2_28_x86_64.whl;SHA256daecc2072b82b6a942acbdaa9a2e00c05234c61fef976b22713983c020b07992|Read-onlyZIP/strings/hashchecked,noimport;glibc/ISA gate. Native libav/x264/x265/gnutls notices scopeopen |\n',
      '| CPython |3.12.15source;Python-3.12.15.tar.xz SHA256c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a|Source-onlysecurityrelease,officialWindowsinstallerнет;binary/linkSQLiteunknown;suppliedLinQPythonнеобновлять |\n',
      '| websockets |17.0.1,fd3f16cc4f57ace08e323a7806f1432e957cb75e;universalwheelSHA256c6be9cba65c65cc76dfa3d4619e359ff02a4476c74e179b215236c11a0b32345|Python≥3.11,BSD-3-Clause,standaloneasyncio,noASGIextras |\n',
      '| SQLite |3.51.3 SOURCE_ID2026-03-13 10:38:09 737ae4a34738ffa0c3ff7f9bb18df914dd1cad163f28fd6b6e114a344fe6d618|ActualPythonconnectiongate;WALresetbugfixed3.51.3/backports3.44.6/3.50.7;documentedvendorbackportalternative;notstandardpipinstall sqlite3 |\n',
      '| FFmpegCLI |n8.0sourcebasis;actualbinaryvendor/buildflags/hashunknown|Optionalpublisher/ffprobe/derivativeprocess;отдельноотPyAVlinkedlibavvendor8.0-2/license |\n',
      '| Proprietary/model/otherimports |issuedLinQbundle/weights/OpenCV/NumPy/PillowetcUNKNOWN|Добавлятьтолькопофактическойпотребности/manifest/license,неimplicitdependencies |\n',
      '## Каталог8проектов — образцы, не selected dependencies\n',
      '| Project | Snapshot/лицензия | Прикладнойreuse/ограничение | Stablecatalog |\n|---|---|---|---|\n']
    catalog=[
      ('Frigate','91e91c68efe504e17b7fd3fb437b34068b4387ca / MIT, trademarks отдельно','Original recording vs detect sampling; shared slots/per-camera watchdog. Не переделывать NVR под unknownSDK.','W1-04-P01'),
      ('MediaMTX','b37cdf55707f3ef0bab87b3e69985832ae6a6e9b / MIT; selected stable1.21.2 отдельно','Готовый relay/record/playback; protocol conversion не automatic transcoding, incidents/pins/identity добавляет приложение.','W1-04-P02'),
      ('go2rtc','c245815e75e2a5fd60b4290f12bfc04e55a984d3 / MIT','Альтернатива relay для нестандартных камер; security портов1984/8554/8555; второй сервер в минимум не входит.','W1-04-P03'),
      ('Savant','24a3c8d82fc42cc04a903c71e62084ba7ee9f8a0 / Apache2.0 repo','Adapters/source cleanup/correlation; NVIDIA production0.5.x/DS7.0 vs dev0.6.x/DS7.1/TRT10.9; LinQ runtime не установлен.','W1-04-P04'),
      ('DL Streamer','51c317f8d969574784caae2ba02c494e40b62002 / MIT repo','Metadata pipeline; Intel CPU/GPU/NPU не arbitrary NPU. gvametapublish теряет metadata во время reconnect; нужен outbox.','W1-04-P05'),
      ('Roboflow Inference','15d1f4478e1b5cf531ec87ad6d55e30afe58ba0f / core Apache2.0 + superseding paths','Live ADAPTIVE_DROP_OLDEST vs file WAIT, VideoFrame/latency envelope; idea-only, nearest license при копировании.','W1-04-P06'),
      ('Ultralytics','e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 / AGPL3.0 или Enterprise','Latest/barrier pattern и local baseline; нет PTS/epoch/full NVR; weights отдельно.','W1-04-P07'),
      ('DeepStream Python Apps','8ad0349ed7a496fae35ebb21c350641727070b89 / Apache2.0 sample/bindings repo','Batch/tee/metadata/lifecycle example; SDK9.0 bindings deprecated/no wheels/PyServiceMaker; license SDK отдельно.','W1-04-P08')]
    for title,version,reuse,pid in catalog:
        rec=next(r for r in c.supplements if pid in r['title'])
        out.append(f'|{title}|{version}|{reuse}|[{rec["id"]}](../RAW_FACTS.md#{rec["id"].lower()})|\n')
    out += ['## Адресные передачи соседям\n',
      '| Topic | Находка/решение | Evidence / остаётся неизвестно |\n|---|---|---|\n',
      '|linq_platform|Issued custommodel/I/O/lifecycle/terminal/quota/borrow/network/hostgrant; devicewitness. API можетдостаточенбезSSH.|'+hlinks('Q001 Q002 Q003 Q025 E001 E007 E008')+'|\n',
      '|model_stack|Actualhead/dtype/scales/NMS/coordinates/caps/parity; batch/stateful/ROIwork и NNboundary; weightslicenses.|'+hlinks('W2-01-F14 W2-01-F16 W2-04-F11 Q009 Q016 Q025')+'|\n',
      '|violation_methods|Versioned minFPS/maxgap/dwell/ID/coverage/resetcontract. Gapнеnegative,ByteTrackfixedstep,per-cameracycleceiling.|'+hlinks('W2-04-F02 W2-04-F04 W2-04-F09 W2-04-F13 Q005 Q021 E006')+'|\n',
      '|evaluation|RGBJPEG/resolution/ROIclass-sizerecall; fullonset/dwell/denominator/clockuncertainty; lost/late/censoredvisible.|'+hlinks('W1-03-F11 W1-03-F12 W1-06-F14 E004 E017')+'|\n',
      '|operator_product|Separatevideo/analysis/evidence/deliveryhealth;pending/partial/unknownclips,accepted/rendered/readразличны;channelaccessoptional.|'+hlinks('W1-05-F23 W2-02-F12 W2-03-F10 Q011 Q013 Q018')+'|\n',
      '|market_deployment|Directional50/500/VBR/retention/IOreserve/privacy/security/licenseactualartifactscope;неpurchasecapacity/legalcertification.|'+hlinks('W1-01-F17 W1-01-F18 W2-05-F03 W2-06-F02 W2-06-F04 Q012 Q016 Q019 Q022')+'|\n',
      '|hackathon_strategy|RealLinQgolden/coregates/cuts/owners;45чwindowнеuptime;GUI/jobunsupported-live,CPU/RTX/replaymarked;requiredexactclipfailureblocker.|'+hlinks('W1-01-F23 W1-01-F24 W2-06-F09 W2-06-F10 Q024 E018')+'|\n',
      'Передача означает подготовленные файловые ссылки, не внешние сообщения/запуск соседнего research. Не предполагать наличие иных соседних отчётов: подтверждён только прочитанный linq_platform пакет через S001.\n',
      '## Указания для литературного синтеза\n',
      'Сначала объяснить unknownaccess→conditionaltopology ибыстрыйпервыйчас, затемсвязатьpipeline/temporal/evidence/view/faults/measurement/capacity. Критическиеconditionsпомещатьрядом с рекомендацией, не в концеобщимdisclaimer. Сохранить конкретные knobs/defaults/version иnegativecases ввыбранномстеке. Каталог не растягиватьсимметрично;selectedbaselineвышеunusedalternatives. Первичныйvendorbenchmarkпересказатьсусловиями,неподставлятькакLinQ. Русскийчеловеческийчерновикпишетавтор,финальнуюредактуру—следующаяроль;collectorneсоздавалreport.\n']
    text='\n'.join(out)
    # Readability around script/unit boundaries, leaving links and exact literals intact.
    text=cc.readable(text.replace('未知','неизвестно'))
    replacements={
      'unknownaccess':'unknown access','conditionaltopology':'conditional topology','volatileframes':'volatile frames','durableevents':'durable events','successfulCOMMIT':'successful COMMIT','duplicatewindow':'duplicate window','patchedruntime':'patched runtime','pinrebuild':'pin rebuild','remoteheld':'remote held','segmentminimum':'segment minimum','earlyproof':'early proof','snapshotcut':'snapshot cut','TTLviews':'TTL views','closingcounts':'closing counts','hardRSS':'hard RSS','vendorconditions':'vendor conditions','wholedenominator':'whole denominator','clockerror':'clock error','suspectedimageanomaly':'suspected image anomaly','W1snapshots':'W1 snapshots','nativebundlescope':'native bundle scope','resourceinventory':'resource inventory','modelupdates':'model updates','documentedNN':'documented NN','localprojection':'local projection','compactreturn':'compact return','metadataonly':'metadata only','persistedledger':'persisted ledger','fullcycle':'full cycle','Compressedingest':'Compressed ingest','actualbinary':'actual binary','rawslot':'raw slot','selectedtiles':'selected tiles','registeredcamera':'registered camera','FullsourceFPS':'Full source FPS','analysis5':'analysis 5','modelinvocations':'model invocations','measuredrequest':'measured request','Idealpollwait':'Ideal poll wait','nooutageuniformphase':'no outage/uniform phase','actualvisibility':'actual visibility','backoffunknown':'backoff unknown','responsebytes':'response bytes','Viewer1credit':'Viewer 1 credit','ACKcycle':'ACK cycle','JPEGencode':'JPEG encode','sourceframe':'source frame','VcopiesNIC':'V copies NIC','clipdownloads':'clip downloads','Necessarymeans':'Necessary means','remoteoccupancy':'remote occupancy','actualquotaunits':'actual quota units','unknownheld':'unknown held','liveGap':'live Gap','temporalgate':'temporal gate','Theoreticalops':'Theoretical ops','LinQnumbers':'LinQ numbers','FP32return':'FP32 return','PGIETrafficCamNet':'PGIE TrafficCamNet','LinuxPyAVwheel':'Linux PyAV wheel','relayprocess':'relay process','prospectiveremux':'prospective remux','BSDwrapper':'BSD wrapper','nativebundle':'native bundle','ActualPythonconnectiongate':'Actual Python connection gate','actualbinaryvendor':'actual binary vendor','digestunknown':'digest unknown','Pythonconnectiongate':'Python connection gate','onlysecurityrelease':'only security release','Windowsinstaller':'Windows installer','linkSQLiteunknown':'linked SQLite unknown','standaloneasyncio':'standalone asyncio','noASGIextras':'no ASGI extras','documentedvendorbackportalternative':'documented vendor backport alternative','notstandardpipinstall':'not standard pip install','Optionalpublisher':'Optional publisher','derivativeprocess':'derivative process','otherimports':'other imports','issuedLinQbundle':'issued LinQ bundle','PillowetcUNKNOWN':'Pillow etc UNKNOWN','Stablecatalog':'Stable catalog','automatictranscoding':'automatic transcoding','sourcecleanup':'source cleanup','supersedingpaths':'superseding paths','latencyenvelope':'latency envelope','nearestlicenseifcopy':'nearest license if copied','barrierpattern':'barrier pattern','localbaseline':'local baseline','weightsseparate':'weights separate','bindingsrepo':'bindings repo','lifecycleexample':'lifecycle example','devicewitness':'device witness','custommodel':'custom model','weightslicenses':'weights licenses','ByteTrackfixedstep':'ByteTrack fixed step','cameracycleceiling':'camera cycle ceiling','resetcontract':'reset contract','RGBJPEG':'RGB JPEG','fullonset':'full onset','clockuncertainty':'clock uncertainty','censoredvisible':'censored visible','Separatevideo':'Separate video','deliveryhealth':'delivery health','unknownclips':'unknown clips','channelaccessoptional':'channel access optional','licenseactualartifactscope':'license actual artifact scope','legalcertification':'legal certification','RealLinQgolden':'Real LinQ golden','coregates':'core gates','jobunsupported':'job unsupported','replaymarked':'replay marked','requiredexactclipfailureblocker':'required exact clip failure blocker','NNboundary':'NN boundary',
      'ибыстрыйпервыйчас':'и быстрый первый час','Критическиеconditions':'Критические conditions','рядом с рекомендацией, не в концеобщим':'рядом с рекомендацией, не в конце общим','Сохранить конкретные knobs/defaults/version иnegativecases ввыбранномстеке.':'Сохранить конкретные knobs/defaults/version и negative cases в выбранном стеке.','не растягиватьсимметрично':'не растягивать симметрично','Первичныйvendorbenchmarkпересказатьсусловиями,неподставлятькакLinQ':'Первичный vendor benchmark пересказать с условиями, не подставлять как LinQ','Русскийчеловеческийчерновикпишетавтор,финальнуюредактуру':'Русский человеческий черновик пишет автор, финальную редактуру','collectorneсоздавалreport':'collector не создавал report','послеlive':'после live','вслучае':'в случае','Тежеусловия':'Те же условия','укоманды':'у команды','безFS':'без FS','сверх':'сверх'
    }
    for a,b in sorted(replacements.items(),key=lambda kv:-len(kv[0])):text=text.replace(a,b)
    text=re.sub(r'Сначала объяснить unknown access.*\Z','Сначала объяснить зависимость topology от неизвестного access mode и действия первого часа. Затем связать pipeline, temporal state, evidence, browser, failures, measurement и capacity. Существенные условия помещать рядом с рекомендацией. Сохранить полезные version-specific параметры/defaults и negative cases; selected baseline отличать от каталога альтернатив. Первичные vendor benchmarks пересказать с конфигурацией и пределами переноса. Автор пишет русский черновик, следующая роль редактирует финальный текст; collector литературный отчёт не создавал.\n',text,flags=re.S)
    text=re.sub(r'(\|[^\n]*\n)\n+(?=\|)',r'\1',text)
    text=re.sub(r'SHA256(?=[a-f0-9]{64})','SHA256 ',text)
    (c.WORK/'COLLECTOR_HANDOFF.md').write_text(text,encoding='utf-8')

if __name__=='__main__':
    original_hash=critic();handoff()
    (c.WORK/'COLLECTOR_ORIGINAL_CRITIC_HASH.txt').write_text(original_hash+'\n',encoding='utf-8')
    print('W2 statuses appended; author handoff saved; original CRITIC SHA256 '+original_hash)
