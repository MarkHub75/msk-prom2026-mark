# COLLECTOR_HANDOFF — вход High автора video_architecture

Статус: обе 6W1/6W2 содержательно собраны; исходный fresh-context CRITIC сохранён,10K статусов дописаны ниже. Автор создаёт связный русский черновик, новую сеть/SDK/замеры не получает. Все важные условия и unknown остаются рядом с выводом. Это навигация и данные для автора, не литературный отчёт.

Дата сборки и подтверждённая дата обращения: **2026-10-23 Europe/Moscow (UTC+3)**. Collector не получал новую сеть, не запускал приложения/камеры/SDK/LinQ и не выполнял предложенные E. W1 закончена до прерывания и не повторялась; несохранённый первый critic не восстанавливался. Сохранённый CRITIC создан отдельным fresh-context critic_resume, затем выполнены шесть W2 по K001–K010. Нет полного кейса, issued SDK/grant, actual LinQ output и runtime benchmark. Ранние интервалы W1_01/03 приблизительны: они не являются точным журналом отдельных обращений. SHA snapshot доказывает состав сохранённых bytes, а не неизменность current upstream или работу программы.

## Файлы и точные ссылки

- [SOURCES](../SOURCES.md): primary chains/revisions, access отдельно от publication, snapshots/local locators и supporting F.
- [RAW_FACTS](../RAW_FACTS.md): подробные extraction records в 13 тематических группах; команды/configs/версии/units/conditions/negative cases сохранены.
- [OPEN_QUESTIONS](../OPEN_QUESTIONS.md):25 сведённых вопросов и 19E с decision/inputs/steps/metrics/outcomes/limits; E все PROPOSED/NOT RUN.
- [CRITIC](../CRITIC.md): оригинал + K001..K010 W2 results; точный статус anchor `#k001-w2` и далее.
- [ID_MAP](ID_MAP.md): native→stable, включая составные F/общие primary chains и catalog supplemental F.
- [COLLECTOR_STATE](COLLECTOR_STATE.json), [CURATED](COLLECTOR_CURATED.json): машинная служебная карта, не новые итоговые отчёты.

Перед каждым stable record есть явный HTML anchor: `../RAW_FACTS.md#f001`, `../SOURCES.md#s001`, `../OPEN_QUESTIONS.md#q001`/`#e001`. Из корневых отчётов убрать `../`. Не ссылаться на автоматический длинный heading slug/turn IDs. Native IDs в provenance не отдельные measurements.

## Быстрый маршрут чтения тематической базы

| Тема автора | Главные stable записи | Что сохранять |
|---|---|---|
| Доступ/маршруты/реальный LinQ | [F001](../RAW_FACTS.md#f001) [F005](../RAW_FACTS.md#f005) [F006](../RAW_FACTS.md#f006) [F007](../RAW_FACTS.md#f007) [F143](../RAW_FACTS.md#f143) [F146](../RAW_FACTS.md#f146) [F204](../RAW_FACTS.md#f204) [Q001](../OPEN_QUESTIONS.md#q001) [Q002](../OPEN_QUESTIONS.md#q002) | Нет issued grant; shell/API/jobs/GUI — условия, не выданные возможности |
| Ingress/decode knobs | [F026](../RAW_FACTS.md#f026) [F027](../RAW_FACTS.md#f027) [F028](../RAW_FACTS.md#f028) [F029](../RAW_FACTS.md#f029) [F030](../RAW_FACTS.md#f030) [F031](../RAW_FACTS.md#f031) [F032](../RAW_FACTS.md#f032) [F033](../RAW_FACTS.md#f033) [F034](../RAW_FACTS.md#f034) [F037](../RAW_FACTS.md#f037) [F038](../RAW_FACTS.md#f038) [F052](../RAW_FACTS.md#f052) | timeout units/defaults, post-decode dropping, open-only, loop TCP и epoch |
| Payload/quality/return | [F063](../RAW_FACTS.md#f063) [F064](../RAW_FACTS.md#f064) [F067](../RAW_FACTS.md#f067) [F068](../RAW_FACTS.md#f068) [F147](../RAW_FACTS.md#f147) [F148](../RAW_FACTS.md#f148) [F149](../RAW_FACTS.md#f149) | JPEG size variable; class/size recall; raw outputs/NMS/polling в отдельном направлении |
| Scheduler/temporal | [F083](../RAW_FACTS.md#f083) [F084](../RAW_FACTS.md#f084) [F085](../RAW_FACTS.md#f085) [F086](../RAW_FACTS.md#f086) [F173](../RAW_FACTS.md#f173) [F175](../RAW_FACTS.md#f175) [F177](../RAW_FACTS.md#f177) [F180](../RAW_FACTS.md#f180) [F181](../RAW_FACTS.md#f181) [F182](../RAW_FACTS.md#f182) [F183](../RAW_FACTS.md#f183) [F184](../RAW_FACTS.md#f184) | source clocks/gaps vs result arrival; sparse sent IDs; fixed dt не меняется PTS;1/L не aggregateK |
| Event/outbox/DB | [F087](../RAW_FACTS.md#f087) [F088](../RAW_FACTS.md#f088) [F089](../RAW_FACTS.md#f089) [F090](../RAW_FACTS.md#f090) [F091](../RAW_FACTS.md#f091) [F093](../RAW_FACTS.md#f093) [F096](../RAW_FACTS.md#f096) [F189](../RAW_FACTS.md#f189) [F190](../RAW_FACTS.md#f190) [F191](../RAW_FACTS.md#f191) [F193](../RAW_FACTS.md#f193) [F194](../RAW_FACTS.md#f194) [F195](../RAW_FACTS.md#f195) [F196](../RAW_FACTS.md#f196) | volatile frames/durable events, successful COMMIT, duplicate window, patched runtime/backup/pin rebuild/remote held |
| Evidence mapping/finite disk | [F097](../RAW_FACTS.md#f097) [F100](../RAW_FACTS.md#f100) [F104](../RAW_FACTS.md#f104) [F151](../RAW_FACTS.md#f151) [F152](../RAW_FACTS.md#f152) [F153](../RAW_FACTS.md#f153) [F154](../RAW_FACTS.md#f154) [F158](../RAW_FACTS.md#f158) [F159](../RAW_FACTS.md#f159) [F160](../RAW_FACTS.md#f160) [F161](../RAW_FACTS.md#f161) | recorder≠decoder generation; segment minimum; early proof/snapshot cut; late/partial/unavailable |
| Browser | [F106](../RAW_FACTS.md#f106) [F109](../RAW_FACTS.md#f109) [F114](../RAW_FACTS.md#f114) [F116](../RAW_FACTS.md#f116) [F164](../RAW_FACTS.md#f164) [F166](../RAW_FACTS.md#f166) [F167](../RAW_FACTS.md#f167) [F168](../RAW_FACTS.md#f168) [F169](../RAW_FACTS.md#f169) [F170](../RAW_FACTS.md#f170) [F171](../RAW_FACTS.md#f171) |1rendercredit/connection, TTL views≠borrows; closing counts; hard RSS/teardown неизвестно |
| Measurement/resilience/health | [F123](../RAW_FACTS.md#f123) [F125](../RAW_FACTS.md#f125) [F126](../RAW_FACTS.md#f126) [F127](../RAW_FACTS.md#f127) [F131](../RAW_FACTS.md#f131) [F132](../RAW_FACTS.md#f132) [F201](../RAW_FACTS.md#f201) [F202](../RAW_FACTS.md#f202) [F203](../RAW_FACTS.md#f203) [F207](../RAW_FACTS.md#f207) | vendor conditions, whole denominator/clock error/censoring; suspected image anomaly |
| Deployment/catalog/capacity/minimum | [F017](../RAW_FACTS.md#f017) [F018](../RAW_FACTS.md#f018) [F133](../RAW_FACTS.md#f133) [F185](../RAW_FACTS.md#f185) [F186](../RAW_FACTS.md#f186) [F187](../RAW_FACTS.md#f187) [F188](../RAW_FACTS.md#f188) [F198](../RAW_FACTS.md#f198) [F199](../RAW_FACTS.md#f199) [F200](../RAW_FACTS.md#f200) [F206](../RAW_FACTS.md#f206) | W1 snapshots≠lock, native bundle scope, directions/resource inventory,5owners/gates/cuts |

## Установленные выводы и условные рекомендации

1. **Доказано источниками/кодом:** library knobs/version caveats, interframe decode vs sample, native recorder metadata/generation limits, fixed-step tracker semantics, WS send/close/queue directions и patched SQLite/backup mechanisms. Это чтение первичных материалов; наши runtime tests не выполнялись.
2. **Вычислено локально:** payload/storage/pixels/occupancy scenarios с явными inputs; это не benchmark камеры/платы.
3. **Рекомендуемый proposal:** модульное приложение, один логический actor/camera, bounded stateless scheduler/bytes/remote credits, actual LinQ adapter, one local DB writer/outbox, own-frame processed view. MediaMTX — relay; custom indexed remux допускается ранним E009, иначе snapshot cut. Не добавлять broker/NVR/NVIDIA runtime ради схемы.
4. **Неизвестно:** actual grant/full case/model output/NN boundary/LinQ Cinf/runtime safety/source profiles/quality/network/target FS и реальная 45 ч feasibility. Ни один proposed route не назвать экспериментально работающим.

## Матрица LinQ для конечного решения

| Выданный mode | Размещение | Gate / честный исход |
|---|---|---|
| Image/tensor API | Team: ingest/decode/preprocess/state/DB/record/UI; remote: documented NN/pre/post | Input/output/schema/model updates/witness, bytes/quotas/lifecycle; tensor dtype/shape не подменять |
| Shell + own persistent daemon + source ingress + CPU/codec/storage/ports grant | Единый app data plane/DB/recorder/projection рядом с decoder; supplied proprietary worker отдельной deployment unit | Все permissions/persistence/network/privacy подтверждены. Если local projection нужна, считать retainedimage+compact return, не metadata only |
| Shell, только ephemeral NN worker | Team app как API route; thin remote worker в supplied env | SSH не root/Docker/DB/persistence. Loss/restart→remote reconcile |
| Job API/shared queue | Team persisted ledger/collector, fair latest scheduler, queue+poll+fetch+post в full cycle | Live только при lifecycle/return/freshness/per-camera gates. Unbounded delay→bounded stop/degraded/offline; evidence finite |
| GUI/manual либо job без usable result/turnaround | Witnessed/offline LinQ run + честно marked replay/mock product flow | Unsupported-live; click automation/CPU/RTX не закрывают real-time LinQ requirement |

Общая очередь — дополнительная ось любого mode, VPN — network transport. Managed-video/events-only endpoint требует своего model/classes/timestamp/output contract; его наличие не установлено.

## Расчёты 50/500: формулы и допущения

Все значения ниже — **INFERENCE/LOCAL arithmetic**, не hardware/source measurements. SI:1kB=1000B,1MB=10⁶B,1GB=10⁹B,1TB=10¹²B; Mbit/s=10⁶bit/s. Scenario: N50/500, source1080p25, main4Mbit/s, optional720p25 sub1Mbit/s, analysis 5fps, JPEG100000B/frame. JPEG size/quality и modeloutput не установлены. Units/stride/copies/transport/retransmits/VBR tails/reserve учитывать дополнительно.

| Величина / формула |50 камер|500 камер|Граница |
|---|---:|---:|---|
| Camera→gateway main N×4Mb/s |200Mb/s|2Gb/s|Compressed ingest, не API uplink того же full-duplex segment |
| Main+sub N×(4+1)Mb/s |250Mb/s|2.5Gb/s|Если оба приходят в узел |
| JPEG uplink 8NfE[J] |200Mb/s|2Gb/s|При 100kB×5fps=4Mb/s/camera: экономии против main4 нет |
| Tensor640²RGB uint8:8Nf×640×640×3 |2.4576Gb/s|24.576Gb/s|Только при actual uint8 contract |
| Тот же FP32 ×4 |9.8304Gb/s|98.304Gb/s|4915200B/frame; input dtype не произвольный выбор |
| Raw1080p NV12×5fps:8NfWH×1.5 |6.2208Gb/s|62.208Gb/s|Nominal8bit420, без stride/copies |
| Raw1080p RGB×5fps:8NfWH×3 |12.4416Gb/s|124.416Gb/s|Raw1080p frame6220800B |
| Remote→client rawhead:8Nf×(1×84×8400×4) |5.6448Gb/s|56.448Gb/s|2822400B/frame, условный shape/dtype, не выбранная NN |
| Remote→client compact:8Nf×(100×24+4) |4.808Mb/s|48.08Mb/s|≤100packed records coords/score/class, без envelope, не JSON/masks |
| Remote decode→local projection sampledJPEG return |+200Mb/s|+2Gb/s|Если все analyzed images возвращаются у команды; иначе colocated projection→selected tiles |
| Viewer egress8ΣvΣtile f×E[J] |19.2Mb/s|19.2Mb/s|3viewers×4selected tiles×2fps×100kB; не все registered camera |
| Main storage/day=N×10.8×b GB |2.16TB/day|21.6TB/day|При b4Mb/s;43.2GB/camera/day |
| Main30days |64.8TB|648TB|Payload без FS/replicas/резерва/backup |
| Main7days |15.12TB|151.2TB|Те же условия |
| Compressed ring40s=N×b×40/8 MB |1GB|10GB|20MB/camera при 4Mb/s; реальный cap по maxbitrate+overshoot/parts/reserve |
| Decode1080p25=NWHf_source |2.592GPix/s|25.92GPix/s|Full source FPS, не analysis 5 |
| Decode720p25 |1.152GPix/s|11.52GPix/s|Разрешение не задаёт автоматически bitrate |
| One nominal1080p NV12 latest slot=NWH×1.5 |155.52MB|1.5552GB|Не totalRSS/VRAM |
| One nominal1080p RGB slot=NWH×3 |311.04MB|3.1104GB|DPB/surfaces/contexts/pools/borrows/outputs/view/DB сверх |
| Required source observations N×5 |250/s|2500/s|Secondary crops/model invocations отдельно |

Control: `q_poll≈ceil(J_jobs/b_query)/Δ`; status↑↓=8q×measured request/response bytes. FixtureJ50/Δ0.5/b1→100calls/s;1kBup/2kBdown→0.8/1.6Mb/s. Ideal poll wait[0,Δ),meanΔ/2 только periodic/no outage/uniform phase; actual visibility/backoff unknown. Неуменьшать response bytes пропорционально batchquery автоматически.

Viewer 1 credit/connection:4tiles×2fps требуют 8messages/s иидеально ACK cycle≤125ms. Несколько tiles невыдаютнесколько credits. Один JPEG encode/source frame неубирает V copies NIC. Replay/seek/clip downloads/backup добавляютсяповерх live.

Concurrency: necessary per-camera `f_req_i≤p_i/E[L_i]`, где L полныйциклс NMS/cascade/apply. При p1,L300ms ceiling3.33fps:globalK100 нелечиткамеру. Necessary means`Σf_i E[L_i]≤K_local`; remote occupancy`Σ_i f_i E[Σjobs L_rj]≤K_remote`, учитывать corr(q,L), actual quota units и unknown held после live Gap. Little-lawmeans не p95/p99/maxgap.

Aggregate Nmax — minimum measured usable inference/decode/preprocess/input/return/postCPU/network/storage/RAM/FD/session budgets **после** per-camera temporal gate. `S=N*b*T/8`; `Cwrite` измерять вместе replay/hash/backup; `mcam` измерить actualbackend. Theoretical ops/TOPS не Cinf. Гипотетический Cinf300fps,u0.7→210effective:ceil(250/210)=2 узла,ceil(2500/210)=12; при Cinf1000,u0.7→1/4. Это не LinQ numbers/закупка, другие bottlenecks могутувеличитьчисло.

## Benchmark conditions, которые нельзя потерять

[F045](../RAW_FACTS.md#f045) [F123](../RAW_FACTS.md#f123) — NVDEC13.0 Ada indicative:1920×1080YUV420/Windows11/SDK13/video2160MHz/perengine,H264903/HEVC1641/Main101520/AV11018fps. Не actual4070/backend/fullservice. DeepStream7.1T4:dualXeonE5-2650v4/48threads,T4clock1513MHz,Ubuntu22.04,driver535.161.08,CUDA12.2,TRT8.6.1.6;1080p30files,PGIE TrafficCamNet batchN interval0,IOU960×544,2SGIEResNet18batch32async,tiler/render/OSDoff;45H265/31H264streams. Нет WAN/UI/p95/p99/duration/LinQ переноса. Подробный memoryliteral/context в RAW, не исправлятьпо памяти.

## Provisional selected baseline и точные артефакты

[F185](../RAW_FACTS.md#f185) [F186](../RAW_FACTS.md#f186) [F187](../RAW_FACTS.md#f187) [F188](../RAW_FACTS.md#f188); authoritative [PROVISIONAL_ARTIFACT_MANIFEST.json](MATERIALS/W2_05/PROVISIONAL_ARTIFACT_MANIFEST.json). Везде selection=provisional, installation_evidence=none.

| Компонент | Pin/artifact | Роль/license/gate |
|---|---|---|
| MediaMTX |1.21.2,914e39535ece709919ac325aaeed98d394ed9093|relay process/MIT; actual binary/imageOS/ISA/digest unknown; optionalreader тотже tag |
| PyAV |16.0.1,7687256d87f22f78cb75bb4aba94dc6e504c9983|decode/prospective remux,Python≥3.10;BSD wrapper≠native bundle |
| Linux PyAV wheel |av-16.0.1-cp312-cp312-manylinux_2_28_x86_64.whl;SHA256 daecc2072b82b6a942acbdaa9a2e00c05234c61fef976b22713983c020b07992|Read-onlyZIP/strings/hashchecked,noimport;glibc/ISA gate. Native libav/x264/x265/gnutls notices scopeopen |
| CPython |3.12.15source;Python-3.12.15.tar.xz SHA256 c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a|Source-only security release,officialWindows installer нет;binary/linked SQLite unknown;suppliedLinQPython необновлять |
| websockets |17.0.1,fd3f16cc4f57ace08e323a7806f1432e957cb75e;universalwheelSHA256 c6be9cba65c65cc76dfa3d4619e359ff02a4476c74e179b215236c11a0b32345|Python≥3.11,BSD-3-Clause,standalone asyncio,no ASGI extras |
| SQLite |3.51.3 SOURCE_ID2026-03-13 10:38:09 737ae4a34738ffa0c3ff7f9bb18df914dd1cad163f28fd6b6e114a344fe6d618|Actual Python connection gate;WALresetbugfixed3.51.3/backports3.44.6/3.50.7;documented vendor backport alternative;not standard pip install sqlite3 |
| FFmpegCLI |n8.0sourcebasis;actual binary vendor/buildflags/hashunknown|Optional publisher/ffprobe/derivative process;отдельноот PyAVlinkedlibavvendor8.0-2/license |
| Proprietary/model/other imports |issued LinQ bundle/weights/OpenCV/NumPy/Pillow etc UNKNOWN|Добавлятьтолькопофактическойпотребности/manifest/license,не implicitdependencies |

## Каталог 8 проектов — образцы, не selected dependencies

| Project | Snapshot/лицензия | Прикладной reuse/ограничение | Stable catalog |
|---|---|---|---|
|Frigate|91e91c68efe504e17b7fd3fb437b34068b4387ca / MIT, trademarks отдельно|Original recording vs detect sampling; shared slots/per-camera watchdog. Не переделывать NVR под unknownSDK.|[F217](../RAW_FACTS.md#f217)|
|MediaMTX|b37cdf55707f3ef0bab87b3e69985832ae6a6e9b / MIT; selected stable1.21.2 отдельно|Готовый relay/record/playback; protocol conversion не automatic transcoding, incidents/pins/identity добавляет приложение.|[F218](../RAW_FACTS.md#f218)|
|go2rtc|c245815e75e2a5fd60b4290f12bfc04e55a984d3 / MIT|Альтернатива relay для нестандартных камер; security портов 1984/8554/8555; второй сервер в минимум не входит.|[F219](../RAW_FACTS.md#f219)|
|Savant|24a3c8d82fc42cc04a903c71e62084ba7ee9f8a0 / Apache2.0 repo|Adapters/source cleanup/correlation; NVIDIA production0.5.x/DS7.0 vs dev0.6.x/DS7.1/TRT10.9; LinQ runtime не установлен.|[F220](../RAW_FACTS.md#f220)|
|DL Streamer|51c317f8d969574784caae2ba02c494e40b62002 / MIT repo|Metadata pipeline; Intel CPU/GPU/NPU не arbitrary NPU. gvametapublish теряет metadata во время reconnect; нужен outbox.|[F221](../RAW_FACTS.md#f221)|
|Roboflow Inference|15d1f4478e1b5cf531ec87ad6d55e30afe58ba0f / core Apache2.0 + superseding paths|Live ADAPTIVE_DROP_OLDEST vs file WAIT, VideoFrame/latency envelope; idea-only, nearest license при копировании.|[F222](../RAW_FACTS.md#f222)|
|Ultralytics|e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 / AGPL3.0 или Enterprise|Latest/barrier pattern и local baseline; нет PTS/epoch/full NVR; weights отдельно.|[F223](../RAW_FACTS.md#f223)|
|DeepStream Python Apps|8ad0349ed7a496fae35ebb21c350641727070b89 / Apache2.0 sample/bindings repo|Batch/tee/metadata/lifecycle example; SDK9.0 bindings deprecated/no wheels/PyServiceMaker; license SDK отдельно.|[F224](../RAW_FACTS.md#f224)|

## Адресные передачи соседям

| Topic | Находка/решение | Evidence / остаётся неизвестно |
|---|---|---|
|linq_platform|Issued custom model/I/O/lifecycle/terminal/quota/borrow/network/hostgrant; device witness. API можетдостаточенбез SSH.|[Q001](../OPEN_QUESTIONS.md#q001) [Q002](../OPEN_QUESTIONS.md#q002) [Q003](../OPEN_QUESTIONS.md#q003) [Q025](../OPEN_QUESTIONS.md#q025) [E001](../OPEN_QUESTIONS.md#e001) [E007](../OPEN_QUESTIONS.md#e007) [E008](../OPEN_QUESTIONS.md#e008)|
|model_stack|Actualhead/dtype/scales/NMS/coordinates/caps/parity; batch/stateful/ROIwork и NN boundary; weights licenses.|[F147](../RAW_FACTS.md#f147) [F149](../RAW_FACTS.md#f149) [F182](../RAW_FACTS.md#f182) [Q009](../OPEN_QUESTIONS.md#q009) [Q016](../OPEN_QUESTIONS.md#q016) [Q025](../OPEN_QUESTIONS.md#q025)|
|violation_methods|Versioned minFPS/maxgap/dwell/ID/coverage/reset contract. Gap не negative,ByteTrack fixed step,per-camera cycle ceiling.|[F173](../RAW_FACTS.md#f173) [F175](../RAW_FACTS.md#f175) [F180](../RAW_FACTS.md#f180) [F184](../RAW_FACTS.md#f184) [Q005](../OPEN_QUESTIONS.md#q005) [Q021](../OPEN_QUESTIONS.md#q021) [E006](../OPEN_QUESTIONS.md#e006)|
|evaluation|RGB JPEG/resolution/ROIclass-sizerecall; full onset/dwell/denominator/clock uncertainty; lost/late/censored visible.|[F063](../RAW_FACTS.md#f063) [F064](../RAW_FACTS.md#f064) [F132](../RAW_FACTS.md#f132) [E004](../OPEN_QUESTIONS.md#e004) [E017](../OPEN_QUESTIONS.md#e017)|
|operator_product|Separate video/analysis/evidence/delivery health;pending/partial/unknown clips,accepted/rendered/read различны;channel access optional.|[F119](../RAW_FACTS.md#f119) [F161](../RAW_FACTS.md#f161) [F171](../RAW_FACTS.md#f171) [Q011](../OPEN_QUESTIONS.md#q011) [Q013](../OPEN_QUESTIONS.md#q013) [Q018](../OPEN_QUESTIONS.md#q018)|
|market_deployment|Directional50/500/VBR/retention/IOreserve/privacy/security/license actual artifact scope;не purchasecapacity/legal certification.|[F017](../RAW_FACTS.md#f017) [F018](../RAW_FACTS.md#f018) [F187](../RAW_FACTS.md#f187) [F198](../RAW_FACTS.md#f198) [F200](../RAW_FACTS.md#f200) [Q012](../OPEN_QUESTIONS.md#q012) [Q016](../OPEN_QUESTIONS.md#q016) [Q019](../OPEN_QUESTIONS.md#q019) [Q022](../OPEN_QUESTIONS.md#q022)|
|hackathon_strategy|Real LinQ golden/core gates/cuts/owners;45 ч window не uptime;GUI/job unsupported-live,CPU/RTX/replay marked;required exact clip failure blocker.|[F023](../RAW_FACTS.md#f023) [F024](../RAW_FACTS.md#f024) [F204](../RAW_FACTS.md#f204) [F206](../RAW_FACTS.md#f206) [Q024](../OPEN_QUESTIONS.md#q024) [E018](../OPEN_QUESTIONS.md#e018)|

Передача означает подготовленные файловые ссылки, не внешние сообщения/запуск соседнего research. Не предполагать наличие иных соседних отчётов: подтверждён только прочитанный linq_platform пакет через S001.

## Указания для литературного синтеза

Сначала объяснить зависимость topology от неизвестного access mode и действия первого часа. Затем связать pipeline, temporal state, evidence, browser, failures, measurement и capacity. Существенные условия помещать рядом с рекомендацией. Сохранить полезные version-specific параметры/defaults и negative cases; selected baseline отличать от каталога альтернатив. Первичные vendor benchmarks пересказать с конфигурацией и пределами переноса. Автор пишет русский черновик, следующая роль редактирует финальный текст; collector литературный отчёт не создавал.
