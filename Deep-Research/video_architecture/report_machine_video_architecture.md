---
topic: video_architecture
context_version: mosprom-research-v1
checked_at: "2026-10-23T09:13:56+03:00"
timezone: Europe/Moscow
scope: "Conditional architecture for industrial-safety video analytics using mandatory remote LinQ inference: access-dependent placement, ingress/decode, bounded scheduling, temporal state, events/evidence, browser presentation, failure recovery, measurement, 50/500-camera arithmetic, deployment, and a five-person 45-hour integration plan."
not_covered:
  linq_platform: "Closed SDK/compiler/runtime investigation and issued-device compatibility; this report consumes the saved neighboring package and specifies required contracts."
  model_stack: "Selection/training/export of actual models and weights."
  violation_methods: "Recognition algorithms, domain rule definitions, and tracker accuracy."
  datasets: "Dataset acquisition, annotation, provenance, and licensing."
  training_strategy: "Adaptation/training recipes."
  evaluation: "Model/event-quality evaluation beyond architecture-facing measurement requirements."
  operator_product: "User research, workflow, and product channel selection."
  market_deployment: "Market/prices, legal requirements, personal data/KII, and certification."
  hackathon_strategy: "Competition strategy beyond architecture scope and demo evidence."
answers:
  - "Which LinQ access modes permit live integration, and where should application components run?"
  - "What frame/result/event contracts preserve identity, clocks, geometry, model provenance, order, and gaps?"
  - "Which ingress/decode/transport stack is proposed, and which version-specific buffering traps matter?"
  - "How can scheduling bound local and unresolved remote work while maintaining per-camera fairness?"
  - "When are per-camera throughput and fixed-dt tracking incompatible with required temporal methods?"
  - "How should events, outbox, evidence clips, finite retention, backup, and restore behave?"
  - "How can a browser display the analyzed frame and bound slow-viewer work without claiming sensor-to-screen timing?"
  - "What latency budgets and measurement denominators apply to API, shell, job, and manual access?"
  - "What do directional network, storage, decode, memory, and concurrency formulas imply for 50/500 cameras?"
  - "Which eight reference projects provide reusable architectural ideas, with what revision/license/hardware limits?"
  - "What failure states, deployment/security gates, and five-person 45-hour integration cuts are proposed?"
  - "Which E001-E019 experiments, Q001-Q025 unknowns, and neighboring-topic handoffs remain?"
keywords: [LinQ, RTSP, ONVIF, H264, H265, PyAV, FFmpeg, GStreamer, MediaMTX, go2rtc, NVDEC, QuickSync, ByteTrack, PTS, DTS, time_base, stream_epoch, Gap, remote_ledger, idempotency, outbox, SQLite, WAL, COMMIT, pre-roll, post-roll, indexed_remux, WSS, Canvas, render_ACK, WebRTC, WHEP, rVFC, latency, throughput, fairness, sizing, Astra, offline, 50_cameras, 500_cameras]
entity_schema:
  reference_project:
    representation: "YAML records in the reference-project catalog; every record has exactly these fields."
    fields:
      id: "Stable catalog-local string."
      name: "Project name."
      url: "Immutable inspected repository snapshot URL."
      snapshot: "Commit and commit date; additional release distinctions where relevant."
      license_scope: "Repository license and excluded/transitive scopes."
      hardware: "Backend/hardware dependency; no inferred LinQ support."
      layers: "List of architectural layers illustrated."
      reuse: "Concrete reusable idea; idea-only unless explicitly selected as process."
      limitations: "Scope and integration traps."
      evidence: "Evidence label and relative F-ID link."
takeaways:
  - "Access chooses topology. Image/tensor API can suffice without SSH; GUI or unusably late jobs remain unsupported-live. Issued LinQ grants and real device execution are unknown (Q001-Q003)."
  - "Use one modular application, one logical camera-state owner, bounded count/byte admission, actual LinQ adapter, one local SQLite writer, and separately processed MediaMTX. This is a proposal, not a validated 45-hour implementation."
  - "Local timeout/Gap/epoch reset does not terminate remote work. Persist intent and held credits before possible submit; unresolved work survives restart/restore; stop when reconciliation cannot establish a safe budget."
  - "A full per-camera cycle limits observation FPS independently of aggregate throughput. ByteTrack reference has fixed dt=1/update; PTS metadata does not make it variable-dt."
  - "Processed JPEG plus same-frame metadata is the honest browser minimum. Exact original clips require early mapping validation; snapshot fallback does not satisfy a mandatory exact-clip requirement."
  - "All 50/500 figures are conditional SI arithmetic, not LinQ sizing. No measured LinQ FPS, safe JPEG quality, portable CPU streams/core, installed target stack, or durability/teardown result exists."
materials_state:
  full_case: absent
  issued_sdk_grant_native_driver_firmware: absent
  real_linq_output_and_platform_witness: absent
  neighboring_reports: "Only the saved linq_platform package was actually consumed; its CPU/mock checks are not device runs."
  selected_stack: "Provisional source/artifact candidates; installation_evidence=none."
  experiments: "All E001-E019 proposed, none executed."
actually_checked:
  - "Saved primary documentation/code and artifact metadata obtained by two research waves; collector/author/editor/compressor used saved evidence."
  - "Linux PyAV wheel downloaded, digest checked, ZIP/native metadata inspected without import or execution."
  - "Conditional resource arithmetic; manuscript structure, local links/IDs, YAML and catalog homogeneity during writing."
  - "No application, camera, LinQ SDK/device, load/fault/browser/DB/offline/Astra runtime test. No new network retrieval by compressor."
files:
  human: report_human_video_architecture.md
  facts: RAW_FACTS.md
  sources: SOURCES.md
  critique: CRITIC.md
  open_questions: OPEN_QUESTIONS.md
  provisional_artifacts: _WORK/MATERIALS/W2_05/PROVISIONAL_ARTIFACT_MANIFEST.json
---

# Video architecture: decisions, contracts, and conditional limits

Evidence labels: **DOC** primary documentation; **CLAIM** vendor/author statement; **CODE** inspected source; **MEASURED** someone else's published measurement under stated conditions; **LOCAL** actual local metadata/arithmetic; **INFERENCE** our engineering deduction/proposal; **HYPOTHESIS** candidate requiring validation; **UNKNOWN** unresolved. Evidence type does not imply execution. Commands/configurations below are proposed and were not run. F-IDs resolve to detailed evidence and S-IDs through [RAW_FACTS.md](RAW_FACTS.md) and [SOURCES.md](SOURCES.md). Historical critique and W2 dispositions remain in [CRITIC.md](CRITIC.md).

The public case concerns industrial-safety video, examples including missing helmet, removed respirator, danger-zone entry, and smoking near flammables. These examples are not a complete mandatory specification. Mandatory NN inference is on LinQ; CPU/RTX are development/comparison paths. Five participants and the 45-hour interval are preparation context, not measured feasibility. Official-material reading limits are [F023](RAW_FACTS.md#f023), [F024](RAW_FACTS.md#f024). **UNKNOWN:** full case, model, actual hardware/OS/VRAM/driver, issued access, and live performance.

## LinQ access matrix and first-hour go/no-go

**INFERENCE:** Choose placement from the issued contract, not public product claims. Prefer one modular application with camera actors, a bounded scheduler, actual LinQ adapter, local event/job/evidence DB, and own-frame processed view; MediaMTX is a separate ready-made media process. A logical actor need not be an OS process. Isolate a blocking native decoder/SDK in a worker when necessary. [F070](RAW_FACTS.md#f070), [F082](RAW_FACTS.md#f082), [F094](RAW_FACTS.md#f094), [F204](RAW_FACTS.md#f204).

| Observed grant | Placement | Gate before commitment |
|---|---|---|
| Image/tensor API | Team-side ingest/decode/sampling/state/DB/evidence/UI; remote NN and only documented pre/post | Own model or adequate catalog; immutable version/update process; actual I/O, limits, batch/concurrency, lifecycle, and accepted execution witness |
| Shell permitting persistent custom process, reachable video, CPU/codecs/storage/ports | Colocate application data plane with decoder: scheduling/state/DB/recording/browser projection; isolate proprietary SDK process | Persistence, permissions, network, package installation, backup and privacy. SSH alone gives neither root nor Docker/listeners |
| Shell allowing only temporary inference worker | Team-side main application; remote thin worker in issued environment | Session loss/process lifetime, safe completion and job rediscovery; one successful SSH is insufficient grounds to move DB |
| Job API/shared queue | Team-side persisted job ledger, result collector, fair fresh-frame admission | Usable outputs; terminal/cancel/TTL/quota semantics; full submit→poll→fetch→post cycle and per-camera fresh cadence; otherwise bounded STOPPED/degraded/offline |
| GUI/manual or job without usable results/acceptable cycle | Verified manual/offline LinQ run, separately labeled product replay/mock | `unsupported-live` until a supported automated integration path exists; clicking automation provides no live SLA |

A shared queue can occur in every mode. VPN establishes reachability, not execution rights. A managed RTSP→events endpoint would be a separate scenario, **UNKNOWN** here; classes/model version/timestamps/rule responsibility would still be required. [F208](RAW_FACTS.md#f208), [F204](RAW_FACTS.md#f204).

**CLAIM/DOC:** [LinQ technology](https://lin-q.ru/tech) describes conversion/int8; [solutions/software](https://lin-q.ru/sol) distinguish optional H.264/H.265 encoding boards for HPS from RK3588 CPU-block decoding in HX. Neither proves a decoder on every LinQ board or the hackathon's remote API. Python 3.8 quantize/compile references do not fix the issued runtime version. Software requires registration/verification, not obtained here. [F005](RAW_FACTS.md#f005), [F006](RAW_FACTS.md#f006), [F007](RAW_FACTS.md#f007).

**LOCAL/UNKNOWN:** Saved neighboring [linq_platform package provenance](SOURCES.md#s001) also lacks matched proprietary SDK/native/driver/firmware/device access; CPU/fake-native checks are not LinQ execution. Do not infer completion of other neighboring reports. [F001](RAW_FACTS.md#f001), [F215](RAW_FACTS.md#f215).

**INFERENCE first hour:** Record endpoint/account/quota namespace, runtime/rights, allowed TCP direction, persistence and privacy; obtain minimal positive/empty/error outputs and immutable model; execute one golden input with accepted platform-side witness; save input/hash, model/artifact/config/preprocess revisions, request/job/run IDs and result. Client send logs prove sending; accelerator utilization proves activity; neither alone binds our NN/result to device execution. Determine which NN/pre/post/cascade stages must be on LinQ from the full case. Test two-camera full cycle after golden success. A remote host may not reach private team RTSP; do not assume public camera exposure is needed. Restart only owned processes within grant; no implied shared-device reset. [F003](RAW_FACTS.md#f003), [F215](RAW_FACTS.md#f215), [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002), [Q003](OPEN_QUESTIONS.md#q003), [Q025](OPEN_QUESTIONS.md#q025), [E001](OPEN_QUESTIONS.md#e001).

## Frame/result/event interfaces, time, and ownership

**INFERENCE data path:** `camera|looped_file → MediaMTX → demux/decode → latest frame → bounded fair scheduler → actual LinQ adapter → validated ordered observation|Gap → camera actor → event+outbox+evidence intent COMMIT → own-frame JPEG+metadata → browser`; optional notification dispatcher reads committed outbox. Indexed remux branches from the same demux only after E009. [F205](RAW_FACTS.md#f205), [F206](RAW_FACTS.md#f206).

| Contract | Required information and semantics |
|---|---|
| `FrameEnvelope` / `StreamStatus` | `schema_version`, stable logical `camera_id`, new UUID `stream_epoch`, monotonically increasing uint64 `frame_id` assigned on decoded presentation-order frames **before sampling**; sparse IDs are normal. Preserve integer `pts` + rational `time_base`, nullable normalized `media_time_ns`, `timestamp_source`, width/height, geometry and reversible transforms |
| Clock provenance | `captured_at_utc` only with proven source→UTC mapping; `received_at_utc` is host receive/decode, not exposure. `ingest_monotonic_ns` includes host/domain/run ID; never subtract across hosts/restarts. Explicit fallback `timestamp_source` such as camera_pts/file_pts/host_decode_monotonic/estimated |
| `InferenceRequest` | Immutable request and parent frame key; `request_id`, model/preprocess/request-contract revisions, payload type, dtype/layout/color/shape/scales, byte size/hash; ROI includes parent reference and parent-coordinate transform |
| `InferenceResult` | Echo correlation keys, **actually executed** model revision, status/error, output kind/coordinate space. Raw heads: names/count/shapes/dtype/endian/scales/zero-point and decoder rules. Compact detections: class-map revision, box format, confidence definition, thresholds, NMS config/implementation revision, top-K/max detections/truncation. Count masks/keypoints/embeddings separately; do not double-NMS end-to-end output |
| `OrderedResult` / `Gap` / resets | Camera actor alone updates accepted watermark, health, tracker/rules/candidates. `Gap(start,end,reason,known_count,duration_or_unknown)` means no observation; valid empty detections mean an observed frame without matching outputs |
| `EventMutation` | Immutable `event_id`, increasing `event_revision`, camera/source epoch, rule ID/revision, observed media interval, evidence frame IDs, coverage/gaps, model/backend/run provenance; separate snapshot/clip/delivery states. Retried delivery keeps ID; UI upserts revision |
| Track identity | `(camera_id, stream_epoch, tracking_generation, local_track_id)`; tracker can reset without source reconnect. Semantic episode dedup belongs to versioned method, separate from transport dedup |
| Storage and evidence | Event store acknowledges only COMMIT. `EvidenceManifest` contains lineage, actual interval/coverage/gaps, hashes, transformations and explicit complete/partial/unavailable status; durable queues carry refs, not unlimited pixels |

These are proposed app contracts, **not an extracted LinQ API**. Positive/empty/error/late/old-generation fixtures must precede parallel implementation. [F083](RAW_FACTS.md#f083), [F096](RAW_FACTS.md#f096), [F147](RAW_FACTS.md#f147), [F205](RAW_FACTS.md#f205), [F215](RAW_FACTS.md#f215).

Frame/event units: an interval `start_media_ns=1000000000`, `end_media_ns=2300000000` means 1.0–2.3 s, not an SLA. Version event kinds opened/updated/closed/interrupted and close reasons; `backend=linq` without external execution evidence is insufficient. [F096](RAW_FACTS.md#f096).

Keep immutable copies or bounded-pool references across processes until the actual consumer releases ownership. View TTL may release retained JPEG bytes but cannot release an SDK-borrowed input still being consumed. `asyncio.to_thread` unblocks the event loop, not proof of CPU parallelism, thread safety or native cancellation. Remote decode with local processed projection must return the analyzed image as well as boxes; alternatively grant colocated projection and send selected remote tiles directly. [F094](RAW_FACTS.md#f094), [F095](RAW_FACTS.md#f095), [F149](RAW_FACTS.md#f149), [F170](RAW_FACTS.md#f170), [F200](RAW_FACTS.md#f200).

## RTSP ingress, decode, sampling, and transport traps

**INFERENCE:** MediaMTX + PyAV is the proposed simple path; GStreamer is an alternative for a team already competent with its bus/state machine/hardware pipeline. Read continuously and replace one latest decoded frame; sparse `read()` can leave old video in upstream queues. Latest slot bounds neither decoder DPB nor socket/RPC/WS/browser queues. Manual RTSP URL entry suffices for minimum; ONVIF discovery is optional. Reachable port 554 does not prove RTP passes firewall. [F025](RAW_FACTS.md#f025), [F038](RAW_FACTS.md#f038), [F041](RAW_FACTS.md#f041).

| Inspected implementation | Exact behavior / trap |
|---|---|
| FFmpeg n8.0 RTSP | External AVOption `timeout`, internal field `stimeout`; saved table does not support old external `-stimeout`. `timeout` and `rw_timeout`: µs; `listen_timeout`: s, listen mode; `reorder_queue_size`: packets; `buffer_size`: bytes. n8.0 also uses timeout in UDP polling. None implements reconnect or a total frame-age deadline |
| PyAV 16.0.1 | `av.open(..., timeout=(open_s, read_s))` in seconds with monotonic interrupt callback. Open and stream-info may have separate timers: `(5,3)` does not prove total opening≤5 s. Read timer restarts per `av_read_frame`; endless old frames may never time out. Close container before reopen. HW decode defaults `allow_software_fallback=True`; request alone is no hardware proof; check actual wheel/driver/backend and download/NumPy cost |
| OpenCV 4.13.0 FFmpeg backend | `CvCapture_FFMPEG::setProperty` does not handle `CAP_PROP_BUFFERSIZE`; `CAP_PROP_BUFFERSIZE=1` is not validated RTSP-buffer control. Timeouts/HW acceleration are open-only and backend/build-dependent |
| GStreamer `rtspsrc` | Defaults `latency=2000` ms, `drop-on-latency=false`, `tcp-timeout=20000000` µs; `timeout` is UDP→TCP fallback wait. `tcp-timestamp=true` also backported to 1.24.10: may help certain drift but worsen burst-arriving streams; long test required |
| GStreamer `queue`/appsink | Queue first limit wins: 200 buffers, 10 MB, 1 s. `leaky=downstream` drops old, `upstream` new. Proposed **after decode**: `max-size-buffers=1 max-size-bytes=0 max-size-time=0`; arbitrary compressed drops break interframe dependencies. appsink has its own queue; `max-buffers=0` is unbounded. `drop=true` deprecated since 1.28 in favor of `leaky-type`; do not put `leaky-type` in 1.24 |

**DOC/CODE:** [FFmpeg RTSP](https://ffmpeg.org/ffmpeg-protocols.html#rtsp), [PyAV 16.0.1](https://github.com/PyAV-Org/PyAV/tree/v16.0.1), [OpenCV code](https://github.com/opencv/opencv/blob/fe38fc608f6acb8b68953438a62305d8318f4fcd/modules/videoio/src/cap_ffmpeg_impl.hpp), [rtspsrc](https://gstreamer.freedesktop.org/documentation/rtsp/rtspsrc.html); [F026](RAW_FACTS.md#f026)–[F037](RAW_FACTS.md#f037).

**DOC/INFERENCE:** Sampling 25→5 fps **after decode** reduces resize/encode/inference/WAN, not H.264 reference decode at source cadence. `skip_frame="NONKEY"` is keyframes only: hypothetical GOP50/25fps≈0.5 fps, not arbitrary 5 fps. A smaller camera substream reduces ingress/decode, but small-PPE quality needs testing. Short GOP trades bitrate for recovery; I-frame≠IDR. [F042](RAW_FACTS.md#f042), [F043](RAW_FACTS.md#f043), [F044](RAW_FACTS.md#f044).

Proposed file camera, FFmpeg n8.0 → MediaMTX 1.21.2 (not run):

```sh
ffmpeg -re -stream_loop -1 -i demo_h264.mp4 -map 0:v:0 -an -c:v copy -rtsp_transport tcp -f rtsp rtsp://127.0.0.1:8554/cam1
```

For TCP-only server, publisher **and reader** choose TCP. Server `rtspTransports` differs from per-path upstream `rtspTransport`. Verify codec/profile first; real-time transcode confounds publisher and decoder load. Label source `looped_file`; loop/seek discontinuity creates new epoch; repeated content alone is not camera failure. [Pinned publisher example](https://github.com/bluenviron/mediamtx/blob/914e39535ece709919ac325aaeed98d394ed9093/docs/3-publish/17-ffmpeg.md), [F038](RAW_FACTS.md#f038)–[F041](RAW_FACTS.md#f041).

**INFERENCE:** Match the issued payload contract: evaluate JPEG bytes/CPU/quality if accepted; tensor dtype/layout/shape/scales are not free bandwidth choices. With an authorized worker and compressed ingress, move decode/pre to avoid raw WAN payload only if directional budgets improve. HTTP binary+connection reuse, async unary gRPC or issued WebSocket are candidates; no equal-payload/RTT/TLS/concurrency benchmark ranks them here. Base64 uses `4×ceil(n/3)` B before JSON. gRPC has no default deadline; HTTP/2 stream limits may hide client queue; streaming write return is not remote completion. WS ordered message bytes do not provide model schema, fairness, idempotency or freshness. Triton binary HTTP demonstrates possibility, not LinQ extension support. [RFC4648](https://www.rfc-editor.org/rfc/rfc4648.txt), [gRPC deadlines](https://grpc.io/docs/guides/deadlines/), [F053](RAW_FACTS.md#f053)–[F059](RAW_FACTS.md#f059), [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068).

**MEASURED, limited transferability:** Bhowmik et al., FLIR thermal 640×512 Person/Bicycle/Car, Cascade R-CNN/FSAF/Deformable DETR: small objects especially sensitive. Cascade R-CNN trained on originals has author's IoU>0.5 mAP 0.822/0.789/0.623/0.109 at Q95/Q50/Q15/Q5 versus original 0.823; not COCO mAP50:95 or RGB PPE. Gandor/Nalepa, COCO val2017 5000 images, nine RetinaNet/Faster R-CNN Detectron2 variants: precision at Tc=0.5 can stay relatively stable while recall/AP small fall; Q30/Q40 conclusions concern different metrics, not one safe threshold. **UNKNOWN:** allowable Q for helmets/respirators/cigarettes. [Bhowmik](https://arxiv.org/html/2205.08002), [Gandor/Nalepa](https://doi.org/10.3390/s22031104), [F063](RAW_FACTS.md#f063), [F064](RAW_FACTS.md#f064), [E004](OPEN_QUESTIONS.md#e004).

ROI traffic is `8Nf×E[Σ(Jcrop+h)] + Rdiscovery`; object discovery and overlap cost remain. Equal-sized classifier inputs do not reduce calls with smaller source area. Crowd density increases secondary jobs under load: reserve primary-detector capacity; bound ROIs/frame, per-camera jobs and bytes. Dropped crop means missing secondary evidence, not negative PPE classification. [F065](RAW_FACTS.md#f065), [F066](RAW_FACTS.md#f066), [F182](RAW_FACTS.md#f182).

## Bounded scheduling, remote ledger, per-camera cycle, and temporal state

**INFERENCE scheduler:** One unsent latest frame/camera; fair round robin among ready cameras with `next_due` or finite-burst token bucket. Obtain admission **before** taking/packing frame; one task per source frame waiting with payload merely hides an unbounded queue. Bound global parent count, input/output bytes and pre/post work; dead camera never blocks others. Start B=1, no intentional batch wait, one parent slot/camera. Compatible batch needs same model/version/input and measured benefit; absent sources must not hold filling. Stateful models need worker affinity/start/end/reset/allowed gaps, not default stateless replacement. [F054](RAW_FACTS.md#f054), [F069](RAW_FACTS.md#f069), [F214](RAW_FACTS.md#f214).

Batch wait consumes freshness: deterministic uniform arrivals λ, B → first-frame wait `(B−1)/λ`; 5 fps, B8 →1.4 s. For Poisson arrivals this is an expectation, not a hard maximum. Partial batches need runtime support; padding is not observation. Triton `max_queue_delay_microseconds` controls batch formation, not separate queue timeout/size. [Triton batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html), [F054](RAW_FACTS.md#f054).

**INFERENCE/LOCAL:** Let `L_i` be full parent-slot cycle: pre/encode, network/remote wait/NN/return, client NMS, mandatory dependent cascade and ordered apply. Necessary mean bound `f_i ≤ p_i/E[L_i]`. At p1 and constant L: 160 ms→6.25 fps; 200 ms→5 fps with zero margin; 300 ms→3.33 fps; 500 ms→2 fps; 1 s→1 fps. K100 cannot fix a slow sequential camera; fewer cameras do not shorten its own cycle. `p_min=ceil(f_target×L)` under constant L is a lower bound, not promised gain: concurrency can increase server wait. Same-camera concurrency requires confirmed stateless parallelism or documented sequence semantics. Little-law `Σf_i E[L_i]≤K_local` is mean occupancy, not p95/max-gap SLA. Remote cascades require `Σ_i f_i E[Σ_jobs_per_parent L_rj]≤K_remote`; correlated crowd job-count/latency cannot generally be factored into means. Quota units (jobs/frames/weight) come from grant. These are not LinQ measurements. [F180](RAW_FACTS.md#f180), [F181](RAW_FACTS.md#f181), [F182](RAW_FACTS.md#f182).

**INFERENCE remote ledger:** Local deadline is not remote completion. Before possible network send, atomically persist immutable intent+reserved credit; track `not_submitted → submitting → accepted|running|unknown → terminal`. `held=count(state in {submitting,accepted,running,unknown})≤K_remote`, `free_remote=K_remote−held`, or conservative worst-case weights. Independently cap submit/control/fetch calls and upload/result/post bytes. Preserve control capacity to reconcile when inference slots fill. One un-deduplicated network attempt is one possible obligation; disable/account hidden SDK/proxy retries; do not assume result dedup prevents duplicate work. [F143](RAW_FACTS.md#f143), [F144](RAW_FACTS.md#f144).

| Outcome/race | Required treatment |
|---|---|
| Lost submit ACK, crash before recorded ID, or crash after intent before send | `unknown`, held retained; job_id=null does not prove nonacceptance. Query by key if supported. Same-key retry only inside actual dedup scope/window with same immutable payload and still-fresh deadline; otherwise query/hold |
| Live timeout, Gap, epoch reset, camera removal | Reject late live result but retain remote credit/job collection; retain borrowed SDK buffer until safe release |
| Cancel returns success, job still running; 404/empty lookup/result expired | Still unresolved unless documented definitive terminal/nonacceptance proof. Persist last remote state and reason |
| Terminal witnessed, crash before local release | Reconcile again; transaction/CAS records terminal witness and releases exactly once, not RAM-first |
| ACK received but DB persistence fails | Stop new submits; prior persisted intent/held survives. Do not continue without ledger |
| Restart or old backup restore | Fence old owners, close admission, restore quota namespace/held, submitting→unknown, reconcile including post-backup-cutoff jobs. New live epochs; no held=0 reset |

Resume only on a **proven free remainder**; unresolved jobs still consume budget. At held cap use STOPPED; distrust of ledger/namespace can require immediate stop. A terminal witness or documented complete lifetime expiry must cover queue/start/retries and latest possible acceptance, with server `not_after`/lease/equivalent acceptance cutoff and clock margin. Client RPC deadline, live frame deadline, execution-attempt timeout, full job lifetime, result retention and idempotency retention are six different limits. Same key after retention can create new work. Without idempotent submit/lookup/full TTL, bounded continuous auto-resume is not generally provable; bounded STOPPED is valid. [F145](RAW_FACTS.md#f145), [F146](RAW_FACTS.md#f146), [F195](RAW_FACTS.md#f195), [Q002](OPEN_QUESTIONS.md#q002), [E007](OPEN_QUESTIONS.md#e007).

**DOC counterexample only:** AWS Batch CancelJob HTTP200 can leave STARTING/RUNNING; attempt timeout starts after startedAt, excludes potentially unbounded RUNNABLE; terminal history≥7 days is not execution TTL. No documented SubmitJob clientToken/dedup promise found. Positive paginated unique-name search can recover ID; zero match is not rejection proof. These are AWS semantics, not asserted LinQ behavior. [CancelJob](https://docs.aws.amazon.com/batch/latest/APIReference/API_CancelJob.html), [timeouts](https://docs.aws.amazon.com/batch/latest/userguide/job_timeouts.html), [F134](RAW_FACTS.md#f134)–[F140](RAW_FACTS.md#f140).

**INFERENCE order/time:** Reorder by actually admitted IDs (e.g.100,105,110 after 25→5 sampling), not nonexistent101. Bound ready count/bytes; independent timer advances expired head even with no new responses. Recheck age, epoch, model and geometry immediately before apply. Example (proposed trace):110/105 arrive before100; expire100→Gap, retain remote obligation, reset tracker if required; apply105 then110 only if fresh and valid in new tracking generation; late100 only updates remote lifecycle. A source timestamp gap of2 s remains a gap despite ordered arrival. Late data cannot rewrite accepted live dwell. [F084](RAW_FACTS.md#f084), [F183](RAW_FACTS.md#f183).

Gap≠valid empty≠safe scene. Measure dwell/coverage in source media time; unknown clock→explicit uncertainty. Long gaps interrupt candidates using versioned closed/interrupted/unknown semantics. Reconnect/seek/source replacement/unexplained discontinuity creates epoch; ordinary B-frame reorder does not. Source, decoder and recorder generations are separate. [F085](RAW_FACTS.md#f085), [F086](RAW_FACTS.md#f086), [F158](RAW_FACTS.md#f158).

**CODE:** ByteTrack commit `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`: Kalman `dt=1`; each `BYTETracker.update()` increments frame_id once. Constructor `frame_rate` changes only `buffer_size=int(frame_rate/30.0×track_buffer)`. No calls means no prediction/lost-track aging; fabricated empty calls change state. Valid empty `(0,5)` can make unmatched confirmed tracks Lost; `None`, `(0,)`, timeout are not equivalent. PTS in envelope does not repair fixed dt. [ByteTrack](https://github.com/ifzhang/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99), [F173](RAW_FACTS.md#f173)–[F176](RAW_FACTS.md#f176).

**INFERENCE tracker gate:** Optional only after agreed fixed source cadence/tolerance/max gap/coverage/reset. Missed cadence/unknown time→explicit reset/new instance and `tracking_generation` before next observation; do not reset class-global ID counter for one camera. Frequent reset may make ID-dependent method degraded/unsupported, not fulfilled by frame boxes. A variable-dt alternative/adaptation requires motion/noise validation; wrapper correctness is not ID/re-ID quality. Every method must supply `min_unique_observation_fps`, target period/cadence tolerance, max media gap, max live result age, coverage denominator, warmup, physical dwell, ID continuity and unknown/reset/interruption semantics. Mean5fps may hide ten-frame burst then2s silence; inspect source gaps and real apply intervals. [F172](RAW_FACTS.md#f172), [F177](RAW_FACTS.md#f177)–[F184](RAW_FACTS.md#f184), [Q005](OPEN_QUESTIONS.md#q005), [Q021](OPEN_QUESTIONS.md#q021).

## Event COMMIT, outbox, SQLite, evidence, and recovery

**INFERENCE:** Volatile frames may be replaced for freshness; committed events require durable state/retry. Proposed minimum: one SQLite DB on a supported **local** filesystem, one writer with bounded queue. One transaction persists event revision, dedup key, outbox, evidence intent/reservation/refs; remote intent+held is committed before network. Keep network/hash/decode/export outside transactions. Only successful `COMMIT` permits `event_committed` or `pin accepted`; RAM enqueue does not. [F087](RAW_FACTS.md#f087), [F191](RAW_FACTS.md#f191).

**DOC/INFERENCE:** SQLite WAL permits readers with one writer and requires one host; network filesystem is not a shared team/LinQ DB. PostgreSQL becomes justified for multiple writing hosts or measured contention; `SKIP LOCKED` suits queue tables but not strict FIFO. Do not add Redis/NATS/Kafka merely for a few demo cameras. Redis Streams requires pending reclamation/retention; Core NATS lacks durable storage, JetStream is separate. MQTT QoS2/Kafka transactions do not atomically cover arbitrary external HTTP effects. [SQLite WAL](https://sqlite.org/wal.html), [F088](RAW_FACTS.md#f088)–[F092](RAW_FACTS.md#f092).

Dispatcher reads committed outbox and records attempt/result/provider message ID; unique key `(event_id,event_revision,destination)`. One dispatcher suffices initially. Crash after commit before send→retry; provider accepts then crash before persisted ACK→possible duplicate. Exactly-once external effects need real provider idempotency or receiver inbox. UI upserts one event by revision; clip completion is a new revision, **alarm does not wait for post-roll**. Poison/permanent failures have finite error/dead policy and retained diagnostics. [F093](RAW_FACTS.md#f093), [F119](RAW_FACTS.md#f119).

**DOC/UNKNOWN runtime:** SQLite WAL corruption advisory covers 3.7.0–3.51.2, fixed in3.51.3/backports3.44.6/3.50.7. One writer does not replace patch when readers/checkpoint/backup use other connections. Candidate SQLite3.51.3 `SOURCE_ID 2026-03-13 10:38:09 737ae4a34738ffa0c3ff7f9bb18df914dd1cad163f28fd6b6e114a344fe6d618`; actual connection must prove linked runtime/source_id/compile_options. A CLI or CPython version is insufficient; documented vendor backport requires manifest amendment. [SQLite release](https://sqlite.org/releaselog/3_51_3.html), [F186](RAW_FACTS.md#f186), [E015](OPEN_QUESTIONS.md#e015).

Proposed Python3.12 writer: explicit `BEGIN IMMEDIATE/COMMIT/ROLLBACK`, no mixed implicit transactions/executescript; owned connection; synchronous calls off WS loop. WAL, `synchronous=FULL`, `foreign_keys=ON`, initial `busy_timeout=1000` ms and `wal_autocheckpoint=1000` pages, verify PRAGMA results. FK cannot be enabled inside active transaction. Busy timeout is not whole-query deadline; autocheckpoint is not WAL hard cap. FULL protects admission records only within actual sync/VFS/storage guarantees, not disk loss. COMMIT BUSY may leave transaction active; FULL/IOERR can be ambiguous: inspect state, bounded retry/rollback/recovery, lookup operation's unique persisted key before reporting success. Long streaming reads block checkpoints and grow WAL. [Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html), [F189](RAW_FACTS.md#f189)–[F192](RAW_FACTS.md#f192).

### Exact event→original mapping is an early gate, not a recorder feature

**INFERENCE:** Record compressed original independently of detector sampling. Streamcopy avoids decode/reencode; boxes/blur/resize/frame-accurate trim require derivative decode/reencode. Original evidence is covering closed source segments+manifest; friendly clip references originals. Longer-than-requested coverage can be explicit, missing coverage is partial. [FFmpeg streamcopy](https://ffmpeg.org/ffmpeg.html), [F099](RAW_FACTS.md#f099), [F100](RAW_FACTS.md#f100), [F226](RAW_FACTS.md#f226).

**CODE/DOC MediaMTX1.21.2:** fMP4 `mtxi` stores StreamID16B, SegmentNumber uint64, DTS int64 ns, NTP UnixNano. Recorder StreamID is not source/decoder epoch. Hooks expose path/segment path (complete adds seconds), not original PTS or source/decode lineage; create precedes writeInit. Playback `/list`/`get` uses filename start time and recorder continuity; export loses mtxi UserData. HTTP200/playable MP4 proves neither correct loop pass nor full event window. Default replaces incoming absolute timestamps with system time; `useAbsoluteTimestamp=true` still requires real source time and does not prove correct UTC or independent-reader agreement. RTCP NTP/RTP mapping, PTS and DTS differ. Main/sub require verified FOV, offset/drift and uncertainty, not only scale. [Recorder code](https://github.com/bluenviron/mediamtx/tree/914e39535ece709919ac325aaeed98d394ed9093/internal/recorder), [absolute timestamps](https://github.com/bluenviron/mediamtx/blob/914e39535ece709919ac325aaeed98d394ed9093/docs/2-features/15-absolute-timestamps.md), [F152](RAW_FACTS.md#f152)–[F155](RAW_FACTS.md#f155).

**INFERENCE proposed minimum after E009:** One H.264/no-audio demux sends same access units to decode and indexed remux. Index packet PTS/DTS/time_base/random-access/codec/extradata/sequence **before mux rebasing**. PyAV mux mutates timestamps/time_base; B-frame delay/flush prevents packet=yielded-frame assumptions. Own separate refs/copies for mutable Packet. Preserve distinct source/decoder/recorder generations; missing/repeated PTS→`mapping=unknown`, not reconstructed average-FPS certainty. Resolve `[event_start−pre,event_end+post]` using camera/profile/source generation, actual presentation coverage and internal gaps, random-access dependencies; independently decode output against frame markers/PTS; save input/output bases, rescale/offset, hashes and mapping uncertainty. [PyAV remux](https://github.com/PyAV-Org/PyAV/blob/v16.0.1/examples/basics/remux.py), [F150](RAW_FACTS.md#f150), [F158](RAW_FACTS.md#f158), [E009](OPEN_QUESTIONS.md#e009).

If E009 fails, disable custom recorder; retain analyzed snapshot and optional MediaMTX archive with `mapping=unknown`; do not build two parallel recorders for minimum. **If exact clips are mandatory, snapshot fallback leaves that requirement blocked.** [F206](RAW_FACTS.md#f206), [F226](RAW_FACTS.md#f226), [Q010](OPEN_QUESTIONS.md#q010).

### Finite evidence windows, pins, byte limits, file protocol

**INFERENCE fixture, not case/LinQ SLA:** Finite storage cannot cover arbitrarily delayed results. Evidence acceptance age starts at **earliest required anchor**, which may precede latest qualifying frame in a long incident. Candidate start can be provisionally pinned only within finite budgets. [F159](RAW_FACTS.md#f159).

| Fixture parameter | Value and meaning |
|---|---|
| `A_live` | 2 s from local ingest, not sensor; later result rejected live |
| `L_evidence` | 20 s from earliest required anchor to committed pin intent; late→partial/unavailable |
| Pre P / post Q | 5 s /5 s, actual coverage verified |
| Target segment S / verified IDR interval G | 2 s /≤1 s; unbounded G prevents closure guarantee |
| Close C / total job J | 4 s after target post-roll /30 s wall-time; terminal partial/failed on expiry |
| Chunk / child-manifest rollover | ≤10 s video/chunk;60 s video/child manifest of same incident |
| Incident retained extent | 10 min or byte cap first; then `coverage_truncated`, continue metadata |
| Ring H | 40 s fixture; byte cap overrides nominal window |

With bounded ingress delay/I/O/GOP and proven media↔ingest mapping: `H ≥ P + L_evidence + S + G + C + maintenance_margin =5+20+2+1+4+3=35 s`; chosen H40s. This assumes committed future-range pin protects post-roll; otherwise add Q or full job span. Size by **max bitrate**, GOP overshoot, open parts and FS/index reserve, not average. [F160](RAW_FACTS.md#f160).

MediaMTX `recordSegmentDuration: 2s` is a minimum: next sync/IDR and source stall prevent hard2s bound. Default hour-long segment is poor for small ring;1s part≠1s segment. `recordMaxPartSize` caps part RAM, not disk. `recordDeleteAfter: 0s` only with working own bounded cleanup; native cleanup does not know DB incident pins. [F151](RAW_FACTS.md#f151), [F157](RAW_FACTS.md#f157).

Evidence lifecycle: `pending → waiting_postroll → waiting_close → validating → complete|partial|failed|unavailable`. Admission atomically persists interval/generation/refs/future range/reserved bytes/deadline. Wait post-roll by media progress with monotonic deadline, not endless PTS wait. One serialized retention/pin owner permits deleting only closed+validated+unpinned+unused files. Manual/backup holds also need owner/expiry/cap; quota counts unique bytes. Low space: expired unpinned files/failed temporary derivatives first; then reject new pins/extensions, never silently remove pinned originals. Exhausted reserve stops recording with `recording_unavailable:disk_full`; analysis may continue if resources permit. [F161](RAW_FACTS.md#f161), [F192](RAW_FACTS.md#f192), [F196](RAW_FACTS.md#f196).

DB and FS have no common transaction: persisted intent/reserve→temporary file→trailer/close→independent validation/hash→flush and supported FS metadata persistence→atomic same-FS rename→DB `closed_validated`/refs commit. Crash after rename before commit→orphan reconciliation. Delete: mark deleting→unlink→tombstone; reject new pins on deleting. Hash/rename alone is not power-loss durability; inspected fMP4 functions lack explicit File.Sync, and documented last-part loss is not our power test. [F156](RAW_FACTS.md#f156), [F196](RAW_FACTS.md#f196).

### Backup and restore must reconcile remote work, too

**DOC/INFERENCE:** Do not copy open `.db` or sequential `.db`/`-wal` as consistent backup; committed state can be in WAL. Never delete active WAL as garbage. Use `Connection.backup` in maintenance process with overall deadline and completion verification; its `sleep` is not overall timeout. DB backup is not atomic media/world snapshot. [SQLite backup](https://sqlite.org/backup.html), [F193](RAW_FACTS.md#f193).

Minimum maintenance: pause mutations/submits/deletion; bounded drain writer; establish cutoff and unresolved-job inventory; pin immutable closed-media inventory during copy; backup to new temp file; separately check integrity_check, foreign_key_check, critical keys/refs, actual media sizes/hashes. Publish only complete verified manifest/cutoff bundle; incomplete tails partial. Independent failure domain needed for disk-loss recovery. RPO is actual cutoff of latest complete backup; RTO remains unknown until restore test. Image archive is not data backup. [F194](RAW_FACTS.md#f194).

Restore: fence old owners, new boot/deployment generation, admission/deletion closed; preserve damaged source separately, no foreign-generation WAL mixing; verify runtime/schema/config/DB/FKs/media/index/tail/hashes; missing referenced file→partial/unavailable; never associate orphan solely by name. Rebuild pins/reservations from jobs/manifests/manual+backup holds before first deletion. Old monotonic leases cannot survive reboot. Reconcile external jobs including acceptance after backup cutoff; without reliable reconciliation LinQ admission remains STOPPED although read UI may be recovering/stale. Process crash, OS/power failure and disk loss are distinct unexecuted tests. [F195](RAW_FACTS.md#f195), [F196](RAW_FACTS.md#f196), [E016](OPEN_QUESTIONS.md#e016).

## Browser own-frame projection, render credit, and optional native video

**INFERENCE:** Retain analyzed-frame representation at admission; never fetch current image after result. Send JPEG+same-frame metadata in one binary message and draw image+boxes in one canvas pass. Lower FPS/greater latency than source is explicit. Thumbnail requires saved transform/profile and is not original evidence. Retain JPEG for viewer, not raw camera ndarray; view and SDK input lifetimes remain separate. [F116](RAW_FACTS.md#f116), [F170](RAW_FACTS.md#f170).

Selected provisional route: standalone `websockets.asyncio.server.serve`17.0.1, native browser WS/Canvas; no ASGI/FastAPI/Starlette/Uvicorn solely for view. One WSS `/view/v1`, bounded HELLO, camera authorization, long-lived sender/connection. Encode JPEG once/accepted frame and share among viewers, but traffic multiplies. Do not use `broadcast()` without backpressure or task/frame. [Pinned source](https://github.com/python-websockets/websockets/tree/fd3f16cc4f57ace08e323a7806f1432e957cb75e), [F162](RAW_FACTS.md#f162), [F163](RAW_FACTS.md#f163), [F166](RAW_FACTS.md#f166).

**CODE/INFERENCE:** Mailbox1 does not bound transport/TCP/browser queues.17.0.1 send writes/drains transport; send completion≠draw. `max_size`/`max_queue` constrain incoming controls; watermarks do not cap all outbound JPEG bytes. Browser `bufferedAmount` is browser→server, not receive queue. Use **one outstanding render credit per connection, shared across all tiles**. Before send atomically claim `(view_epoch,delivery_seq,nonce,camera_id,stream_epoch,frame_id)`. Require both send completion and exact post-draw ACK; early ACK during SENDING waits for send finish. Duplicate/future/stale/wrong-nonce ACK never mints credit. Timeout→terminal CLOSING, not READY; active+closing connections count against admission until cleanup. Public `close_timeout` is not proven hard total real-time teardown under blocked transport; experimental transport.abort subclass is not public API and not minimum. [F162](RAW_FACTS.md#f162)–[F169](RAW_FACTS.md#f169), [E012](OPEN_QUESTIONS.md#e012).

Wire: `[u32 big-endian header_bytes][bounded UTF-8 JSON header][JPEG]`; header contains lengths/dimensions/frame/model/geometry IDs and coordinate-declared boxes. uint64 IDs use decimal strings for JS precision. **Proposed fixture:** envelope≤512 KiB **including4-byte prefix**, metadata≤16 KiB, JPEG≤496 KiB; sublimits cannot jointly exceed envelope cap. ≤1280×720/921600 pixels,≤200 boxes,≤4 tiles/page,≤3 admitted connections. Send progress deadline1s, total render-ACK deadline2s from send start, close wait2s. Oversize→validated profile/FPS/tile reduction or size_cap/unavailable, not unbounded growth. [F166](RAW_FACTS.md#f166), [F167](RAW_FACTS.md#f167).

Renderer sets busy before first await; async onmessage alone is not serial. ≤1 createImageBitmap/decode and1 rAF/draw, bitmap.close in finally. Recheck source/view generations after decode; stale images never draw. Hidden tab invalidates generation/closes subscription; on return wait previous decode cleanup, new view_epoch/latest-only; history separate, no queued-JPEG playback. Check age since local credit both on receipt and just before draw, so delayed TCP image after renderer freeze is not fresh. ACK is frontend telemetry, not physical display/read proof, and malicious client can lie; count/bytes/rate caps remain independent. [F168](RAW_FACTS.md#f168), [F169](RAW_FACTS.md#f169).

App-owned projection bytes approximately `(C+V)B` for C shared latest images and V outstanding active+closing sends, plus encoder slots and possible V envelope copies. This is not RSS: allocator/codec/WS/TLS/kernel/browser bitmap/canvas/GPU add memory. Two nominal RGBA8 images at1280×720≈7.37 MB. Separate retained-for-view/input, send/ACK/view drops/hidden/expiry versus analytics losses. Viewer drop is not missed inference or negative violation evidence. [F168](RAW_FACTS.md#f168), [F170](RAW_FACTS.md#f170).

Clock-local `server_age_at_send=send_mono−ingest_mono` is age since system entry, not sensor. Browser knows receive→draw and since-last-draw; server send→ACK includes return transit. Server age+browser receive→draw omits transit, not exact end-to-end. Conservative upper estimate `server_age_at_send + (draw_local−credit_issued_local)` requires verified duration clocks, common server ingest/send domain, drift margin; can over-reject and excludes physical display. Unknown mapping→unknown total age. [F171](RAW_FACTS.md#f171).

**DOC/INFERENCE optional native video:** WebRTC overlay requires sourcePTS/frame→RTP timestamp/SSRC/epoch→rVFC mapping, not result `Date.now()`. rVFC has no hard real-time guarantee; live mediaTime may be0; RTP field is not arbitrary camera ID. H.265 browser support limited; H.264 B-frames unsuitable in described MediaMTX WebRTC path. WHEP reader requires OPTIONS/POST201/Location/PATCH/DELETE/Link/CORS; ICE media separate from HTTP proxy, STUN≠TURN. Inspected WHEP is active `draft-ietf-wish-whep-05`, not final RFC. LL-HLS default200ms parts and3×200=600ms example are not measured total latency. Until mapping passes, show source video separately without exact overlay claim. Store actual letterbox scale/padding, viewport contain/cover,crop/rotation/flip,DPR; constrain backing canvas with image profile; main/sub aspect ratio does not prove FOV. [F106](RAW_FACTS.md#f106)–[F116](RAW_FACTS.md#f116), [E013](OPEN_QUESTIONS.md#e013).

## API/shell/job latency budgets and honest measurement

**INFERENCE:** Separate `L_result` to usable camera observation, `L_video` to draw of corresponding frame, `L_alarm` to declared delivery boundary; physical display/operator acknowledgement separate. No measured LinQ milliseconds exist. Use stage/clock/bound/failure budgets, then allocate SLO after measurement. [F132](RAW_FACTS.md#f132), [F207](RAW_FACTS.md#f207).

| Stage | Image/tensor API | Colocated authorized shell | Job API | Clock/bound/failure |
|---|---|---|---|---|
| Exposure→ingress | Camera encode/network/relay | Compressed WAN+relay | Actual ingress path | Sensor age unknown without calibration/optical test; read timeout≠age bound |
| Decode/pre/sample | Team host | Remote host | Local prep or issued video job | Same-host monotonic; decode source FPS; bounded count/bytes; no progress→stale |
| Admission | Local scheduler | Remote scheduler | Ledger+submit | Per-camera/byte/held caps; expire→drop, preserve remote held |
| Transfer | Input WAN/RPC | IPC, compressed WAN already counted | Upload/submit ACK | Client round-trip observable; one-way unknown; ambiguity→unknown |
| Queue+NN | Opaque queue+NN | Own worker+shared-device wait+NN | Queue/start/run | Remote durations only if issued; run timeout≠queue bound; no lifecycle→bounded stop |
| Return/post/apply | Raw heads+post or compact parse | Host post+IPC+state | Visibility/poll/fetch/post | Full cycle includes NMS/cascade/order; late→Gap/history |
| Rules+DB | Local | Colocated | After result collection | Dwell in media time; local COMMIT clock; error≠success |
| Processed display | Retained frame+WS+browser | Remote selected frames+WAN+browser | Fresh results only, else history | One credit/connection; browser clock separate; timeout/hidden→close/stale |
| Alarm | Commit→UI/history | Same plus WAN | After result collection | send/provider acceptance/render ACK/optical/read distinct; do not wait clip |
| Clip readiness | Pin/post/close/validate/commit | Colocated recorder | Finite late-result acceptance | GOP/progress/I/O limits; deadline→partial/unavailable |

Trace decompositions (avoid double-counting age before admission):

```text
L_result_API = ingress_age + decode/pre + local_admission + upload
             + remote_queue + NN + output_download + post + ordered_apply
L_result_shell = compressed_ingress_age + remote_decode/pre + remote_admission
               + shared_device_wait + NN + host_post + IPC_apply
L_result_job = input_prep + local_admission + upload/submit + job_queue/start
             + job_run + terminal_visibility + poll_detection + fetch
             + post + ordered_apply
```

Shell with local state/projection additionally needs result serialization and **retained image return**. GUI/manual has no supported automated `L_result_live`. Terminal job≠usable result at client. Ideal periodic polling adds `[0,Δ)`, meanΔ/2 only with uniform phase/no failures; backoff/quota changes it. `L_video_processed` adds own-frame→usable-result projection/encode wait+send/transit+decode/draw; source video is a separate NN-free path. [F207](RAW_FACTS.md#f207).

`L_alarm_onset = sampling/onset uncertainty + dwell qualification + qualifying-observation processing + commit + delivery`. At ideal5fps Δ200ms, first sample waits `[0,200)`ms, mean100ms only independent uniform onset phase; k consecutive positives add `(k−1)Δ` only with no loss/cadence deviation. Physical D-second dwell≠completed-request count; onset versus first-positive anchoring changes quantization. Event shorter thanΔ may be missed entirely. Report onset→alarm and rule-eligible→alarm separately with missed/unknown intervals. [F132](RAW_FACTS.md#f132).

Log every frame's ingest/decode/sample/pre/encode/admission/send/receive/remote-duration-if-real/post/rules/commit/UIreceive/draw with host/run. Monotonic_ns only within domain; UTC correlation does not prove synchronization. Bounded endpoint clock errors εA/εB imply difference uncertainty≤εA+εB. Optical timestamp/LED+screen in common high-speed recording supports sensor→screen; Axis25fps loop-overlay already quantizes up to40ms; onset→alarm needs own test. [Axis latency](https://www.axis.com/dam/public/4a/c9/b0/latency-in-live-network-video-surveillance-en-US-443172.pdf), [F125](RAW_FACTS.md#f125), [F126](RAW_FACTS.md#f126), [E017](OPEN_QUESTIONS.md#e017).

Separate denominators for source/ingest/decode/admitted unique frames/valid RPCs/fresh ordered observations/model calls/ROI calls/draw FPS. Aggregate250fps can conceal camera starvation: publish per-camera service, max media gap, apply interval and frame age. Preserve offered,sampled-out,queue-replaced,timeout,invalid/error,late/epoch-reject,completed,undetected,session-ended pending. Timeout is failure or latency>deadline; unfinished end-of-run requests are right-censored, not deleted. If>1% unfinished, successful-subset p99 below deadline is not unconditional p99. Record n,duration,warmup,offered load, backend/model/hash/precision/batch/input,OS/CPU/GPU/driver,network,queue caps. Pace offers independently of response speed. Cold start/reconnect/downtime remain reliability denominator. End-to-end p95 requires traces/compatible histograms; average worker p95 or sum stage p95 is not system p95. Structured logs/counters/simple metrics suffice initially; Prometheus/Grafana optional. [Prometheus histograms](https://prometheus.io/docs/practices/histograms/), [F127](RAW_FACTS.md#f127), [F132](RAW_FACTS.md#f132), [F184](RAW_FACTS.md#f184).

## Conditional sizing: 50/500 cameras, directional network and complete resources

**LOCAL arithmetic, not measured capacity:** Common scenario N50/500, main1920×1080 25fps4Mbit/s, sub1280×720 25fps1Mbit/s, analysis5fps,JPEG100000B/frame. Resolution does not establish bitrate/JPEG size or target-PPE quality. SI kB1000B,MB10⁶B,GB10⁹B,TB10¹²B,Mbit/s10⁶bit/s; memory nominal8-bit NV12=1.5B/pixel,RGB=3B/pixel, no stride/copies. UI/evidence caps elsewhere use explicit KiB. [F068](RAW_FACTS.md#f068), [F133](RAW_FACTS.md#f133), [F200](RAW_FACTS.md#f200).

| Quantity/formula | N50 | N500 | Assumption |
|---|---:|---:|---|
| Main camera→gateway `N×4 Mb/s` | 200 Mb/s | 2 Gb/s | Compressed; write payload25/250MB/s |
| Main+sub `N×(4+1) Mb/s` | 250 Mb/s | 2.5 Gb/s | Both enter same node |
| JPEG uplink `8NfE[J]` | 200 Mb/s | 2 Gb/s |100kB×5fps=4Mb/s/camera |
|640²RGB uint8 tensor `8Nf×640×640×3` |2.4576 Gb/s|24.576 Gb/s|Actual dtype contract required |
|Same FP32×4 |9.8304 Gb/s|98.304 Gb/s|4915200B/frame |
|Raw1080pNV12 at5fps |6.2208 Gb/s|62.208 Gb/s|Nominal |
|Raw1080pRGB at5fps |12.4416 Gb/s|124.416 Gb/s|6220800B/frame |
|Raw720pNV12/RGB at5fps |2.7648/5.5296 Gb/s|27.648/55.296 Gb/s|Nominal |
|Raw-head return `8Nf×2822400B` |5.6448 Gb/s|56.448 Gb/s|Hypothetical `[1,84,8400] FP32`, not selected model |
|Compact return `8Nf×2404B` |4.808 Mb/s|48.08 Mb/s|≤100 packed detections, excludes envelope/JSON/masks |
|Remote decode→local analyzed JPEG return |+200 Mb/s|+2 Gb/s|Every analyzed image returned |
|Selected UI tiles `8×3×4×2×100000` |19.2 Mb/s|19.2 Mb/s|3viewers×4tiles×2fps |

Raw head bytes=`1×84×8400×4=2822400`; compact100×(4FP32coords+FP32score+INT32class)+4Bcount=2404B. Not actual LinQ output or universal compression ratio. Measure JSON bytes; do not FP16-cast without permitted contract. CPU post bound `NfE[cpu_seconds_post/frame] < available CPU seconds/s`; independent fetch/post/tensor byte limits. [F147](RAW_FACTS.md#f147)–[F149](RAW_FACTS.md#f149), [Q025](OPEN_QUESTIONS.md#q025).

JPEG uplink equals compressed main bitrate in this scenario; remote decode does not automatically save outgoing bandwidth, though it localizes raw/pre/post. Local processed UI adds return pixels; colocated projection can send selected tiles directly. Draw camera LAN, gateway↑/↓, remote-host and app→browser links separately; don't sum opposing full-duplex directions as one link. Hypothetical70% utilization:2Gb/s useful requires≥2/0.7≈2.857Gb/s measured available before VBR/protocol reserves, not a standard. [F133](RAW_FACTS.md#f133), [F200](RAW_FACTS.md#f200).

Control-plane formula with J unresolved jobs, poll intervalΔ, supported batch≤b IDs: `q_poll≈ceil(J/b)/Δ`, traffic `8q_poll×E[request/response bytes]`. Example J50,Δ0.5s,b1,request1kB/response2kB→100calls/s,0.8/1.6Mb/s↑/↓. Not LinQ quota. Batch reduces calls, not automatically traffic by b; status may include large outputs. Unknown jobs keep control load after live stop. UI traffic follows selected tiles, not registered count: all500 to each of3viewers at2fps would be2.4Gb/s but minimum forbids admission. One shared connection credit for4tiles×2fps requires8ACK cycles/s, ideal≤125ms/cycle, not4credits. Add replay/seek/download/backup separately. [F148](RAW_FACTS.md#f148), [F149](RAW_FACTS.md#f149), [F199](RAW_FACTS.md#f199).

Storage `S=N×b×T/8` (b bit/s,T seconds), `GB/day/camera=10.8×b_Mbit/s`:

| Payload storage |N50|N500|
|---|---:|---:|
|Main4Mb/s/day|2.16 TB|21.6 TB|
|Main7days|15.12 TB|151.2 TB|
|Main30days|64.8 TB|648 TB|
|Sub1Mb/s/day|0.54 TB|5.4 TB|
|Every JPEG100kB×5fps/day|2.16 TB|21.6 TB|
|Compressed40s ring at4Mb/s|1 GB|10 GB|
|20events/day/camera×30s×4Mb/s|15 GB/day|150 GB/day|

Excludes container/FS/index/replication/backup/reserve/derivative copies. Saved-time fraction≠violation-frame fraction: pre/post/GOP/segments/long incidents expand it. Overlap may share originals but exports duplicate bytes. Ring mean1/10GB is **not hard cap**; use max bitrate+overshoot/open parts/reserve. Small analysis substream does not shrink retained main archive. [F104](RAW_FACTS.md#f104), [F105](RAW_FACTS.md#f105), [F133](RAW_FACTS.md#f133), [F160](RAW_FACTS.md#f160).

Decode counts source FPS: `Pdecode=NWHf_source`;1080p25→2.592/25.92GPixel/s,720p25→1.152/11.52GPixel/s. Required unique analysis observations250/2500s⁻¹, secondary crops extra.1080p25 nominal memory traffic NV12=3.888/38.88GB/s,RGB=7.776/77.76GB/s before copies. One latest1080p slot each:NV12=155.52MB/1.5552GB,RGB=311.04MB/3.1104GB, **not total RSS/VRAM**. [F133](RAW_FACTS.md#f133).

Full memory inventory: base processes/libraries/contexts; demux/parser/jitter; DPB/reorder/decode/output surfaces; latest pools; immutable admitted frames; SDK-borrowed input; view retention; pre/post scratch; outputs; active+closing WS/TLS/kernel/browser; DB/index/cache/reserve. Full OS inventory: processes/threads/stacks,FD/handles/source+relay+remote+control sockets,ports/TIME_WAIT/NAT,open segments/logs/DB/WAL/IPC. NVDEC minimum decode surfaces/output mappings matter; missing unmap exhausts capacity.500actors≠500processes; larger shard increases native-hang blast radius. Actual bytes/stream,FD/stream unknown. Disk benchmark must overlap recording+playback+exports+hash/validate+backup/checkpoint+derivatives;250MB/s payload does not establish useful Cwrite or tails. [NVDEC guide](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.0/nvdec-video-decoder-api-prog-guide/index.html), [F197](RAW_FACTS.md#f197), [F198](RAW_FACTS.md#f198).

**INFERENCE necessary planning bound**, after per-camera temporal feasibility, for homogeneous JPEG route:

```text
Nmax ≤ floor(min(Cinf/f_a,
                 Cdec/(W×H×f_source), Cpre/f_a,
                 Cin/b_in, Cup/(8×f_a×E[J]), Cdown/(8×f_a×E[O]),
                 Cpost_cpu/(f_a×E[cpu_post]),
                 Cwrite/(b_record/8), Susable/((b_record/8)×T),
                 Musable/mcam, K_local/(f_a×E[L_local])))
```

Use measured **useful** full-chain capacities with reserve; Cinf,Cpre in frames/s;Cdec pixels/s;Cin,Cup,Cdown bit/s;Cpost_cpu CPU-s/s;Cwrite B/s;Susable,Musable bytes;L seconds. Remove inapplicable terms; separately bound remote quota/residency, cascade-dependent jobs,bytes,FD/sessions and per-camera p/gaps. This is not a complete admission algorithm. **UNKNOWN Cinf LinQ.** Hypothetical Cinf300fps,u0.7→210useful fps:ceil(250/210)=2nodes,ceil(2500/210)=12; Cinf1000→1/4. These illustrate formula, not LinQ or procurement advice. TOPS/ops-per-frame does not establish operator support/compile/accuracy/copies/queues/fairness. [F133](RAW_FACTS.md#f133), [F181](RAW_FACTS.md#f181), [F182](RAW_FACTS.md#f182), [Q022](OPEN_QUESTIONS.md#q022).

**MEASURED external calibration only:** NVDEC SDK13.0, Ada per engine,1920×1080YUV420,Windows11,video clock2160MHz:H.264903fps,HEVC1641,HEVCMain10 1520,AV1 1018. Matrix lists RTX4070 Desktop/Laptop Ada with1NVDEC; actual team SKU/VRAM/driver/bitstream/GOP/download/resize/UI/tails remain unknown. NVENC session cap≠NVDEC stream cap. [NVDEC note](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.0/nvdec-application-note/index.html), [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046).

DeepStream7.1 published T4:45H.265/31H.264 1080p30 streams;2×XeonE5-2650v4 2.20GHz/48threads,T4clock1513MHz,Ubuntu22.04,driver535.161.08,CUDA12.2,TensorRT8.6.1.6; source memory literal `360448Mb (22x16384) DDR42666, 2400MHz`. PGIE TrafficCamNetResNet18,batch=N,interval0;IOU960×544;2SGIE ResNet18 VehicleTypes/VehicleMake224×224,batch32 async;tiler/render/OSD off. CPU/GPU51.81%/100% H.265,2.72%/61.23% H.264. No WAN/our RTSP/UI/alarms,p95/p99/duration,or LinQ transfer claim. [DeepStream7.1](https://archive.docs.nvidia.com/metropolis/deepstream/7.1/text/DS_Performance.html), [F123](RAW_FACTS.md#f123).

**UNKNOWN:** Portable CPU/QuickSync decode-only streams/core for unknown team machine not found. Inspected QuickSync tables measure encode/transcode; Smelter decode+encode+composition, so neither is Cdec. Intel VPL is dispatcher; real runtime/iGPU required. GPU resize-before-download can reduce copies, but CPU/API/WAN ends zero-copy. Measure E003 rather than invent coefficient. [F047](RAW_FACTS.md#f047)–[F049](RAW_FACTS.md#f049).

## Provisional stack and exact artifact boundaries

**INFERENCE/LOCAL:** Source pin, binary artifact and installed environment are distinct records. All selected candidates in [PROVISIONAL_ARTIFACT_MANIFEST.json](_WORK/MATERIALS/W2_05/PROVISIONAL_ARTIFACT_MANIFEST.json) have `selection_status=provisional`, `installation_evidence=none`. Overlapping Python requirements is not verified installation. Preserve issued proprietary runtime separately; do not upgrade it to match client. [F185](RAW_FACTS.md#f185), [F188](RAW_FACTS.md#f188).

| Layer | Candidate and pin | Remaining gate |
|---|---|---|
|Media relay|MediaMTX1.21.2,`914e39535ece709919ac325aaeed98d394ed9093`,MIT,separate process|Actual OS/ISA binary/image digest; optional native reader same tag |
|Decode/prospective remux|PyAV16.0.1,`7687256d87f22f78cb75bb4aba94dc6e504c9983`|HW fallback/runtime,ownership,E009; GStreamer alternative |
|App runtime|CPython3.12.15 source candidate|Security source-only release, no official Windows installer;binary/ABI/linked SQLite unknown |
|NN|Actual issued API/SDK process|Not an assumed Triton/Hailo/NVIDIA dependency; model/pre/post contract after grant |
|Temporal state|Own actor/Gap/coverage;tracker optional|ByteTrack reference dependencies torch/scipy/lap/cython_bbox/OpenCV and old np.float require install/quality gates |
|Events/job ledger/outbox/index|stdlib sqlite3 with actual patched SQLite3.51.3/source_id|Local one writer,WAL+FULL;PostgreSQL only measured need |
|Processed projection|websockets17.0.1,`fd3f16cc4f57ace08e323a7806f1432e957cb75e`,BSD-3-Clause,Python≥3.11|Public cleanup bounds,actual browser/OS/version,resource tests;no ASGI extras |
|Evidence|One local directory,bounded snapshots;indexed remux after E009|Archive may remain mapping unknown;MinIO/blur/reencode optional |
|Alarms|DB/UI history+one outbox dispatcher|Optional authorized messenger/account/rate/reachability |

Exact candidate artifacts (**not installed**):

- Linux inspected ZIP `av-16.0.1-cp312-cp312-manylinux_2_28_x86_64.whl`, actual downloaded SHA256 `daecc2072b82b6a942acbdaa9a2e00c05234c61fef976b22713983c020b07992`; requires cp312,x86_64,glibc≥2.28. Never imported. Windows cp312 win_amd64 candidate SHA256 `0c669b6b6668c8ae74451c15ec6d6d8a36e4c3803dc5d9910f607a174dd18f17`, upload2025-10-13, metadata only; Linux library inventory does not transfer to Windows.
- `Python-3.12.15.tar.xz` expected release-metadata SHA256 `c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a`, tarball not downloaded.
- `websockets-17.0.1-py3-none-any.whl` expected SHA256 `c6be9cba65c65cc76dfa3d4619e359ff02a4476c74e179b215236c11a0b32345`.
- PyAV wheel linked libav observed:codec62.11.100,device62.1.100,filter11.4.100,format62.3.100,util60.8.100,swresample6.1.100,swscale9.1.100; frozen build workflow vendor8.0-2. x264/x265/gnutls and other native libs present. BSD-3-Clause wrapper is not entire bundle license; binary strings include LGPL version3 or later and configure flags x264/x265. This is metadata, not a legal bundle-consistency conclusion.

Full artifact URLs/metadata are [F188](RAW_FACTS.md#f188)/manifest. Digest alone does not establish trusted origin or installability. Actual `av.library_versions`, `av.ffmpeg_version_info`, pinned internal `av._core.library_meta`, actual SQLite runtime/compile_options and binary hashes remain unchecked. No standard `pip install sqlite3` runtime pin. Standalone FFmpeg CLI n8.0 is another optional process with unknown build/hash, not PyAV-linked libav; record `-version/-buildconf` and notices; GPL/version3/nonfree flags alter scope. OpenCV/NumPy/Pillow/ONNX only if real imports require them, then pin/transitive review. Code/weights/data/proprietary SDK each need actual license/redistribution grants. [FFmpeg legal](https://ffmpeg.org/legal.html), [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [Q015](OPEN_QUESTIONS.md#q015), [Q016](OPEN_QUESTIONS.md#q016).

## Eight reference projects: homogeneous catalog

Every record follows `entity_schema.reference_project`. Snapshots were inspected, not run on LinQ. Repo license does not automatically cover weights/datasets/plugins/SDK/native codecs. Reuse defaults to ideas; MediaMTX's separately pinned1.21.2 is the selected process candidate. [F217](RAW_FACTS.md#f217)–[F224](RAW_FACTS.md#f224).

```yaml
- id: P01
  name: Frigate
  url: https://github.com/blakeblackshear/frigate/tree/91e91c68efe504e17b7fd3fb437b34068b4387ca
  snapshot: "91e91c68efe504e17b7fd3fb437b34068b4387ca; 2026-10-20"
  license_scope: "MIT repository; trademarks and third-party/models separately scoped."
  hardware: "NVIDIA not required for entire NVR; no LinQ backend found in inspected material."
  layers: [ingress, decode, scheduling, recording, events, UI, watchdog]
  reuse: "Idea-only: original recording independent of detection cadence, shared slots, per-camera lifecycle/watchdog."
  limitations: "Large coupled NVR; motion gating may miss static violations; host pipe timestamp is not camera PTS."
  evidence: "CODE/DOC; [F217](RAW_FACTS.md#f217)"
- id: P02
  name: MediaMTX
  url: https://github.com/bluenviron/mediamtx/tree/b37cdf55707f3ef0bab87b3e69985832ae6a6e9b
  snapshot: "b37cdf55707f3ef0bab87b3e69985832ae6a6e9b; 2026-10-22; selected stable 1.21.2 is separately pinned to 914e39535ece709919ac325aaeed98d394ed9093."
  license_scope: "MIT repository; Go dependency notices separately."
  hardware: "Go media router; no mandatory NVIDIA."
  layers: [relay, publish, read, record, playback]
  reuse: "Process candidate: ready media relay; use stable 1.21.2 rather than silently replacing it with inspected HEAD."
  limitations: "Protocol conversion is not automatic transcoding; incident DB, source identity, evidence pins/coverage remain application responsibilities."
  evidence: "CODE/DOC; [F218](RAW_FACTS.md#f218), [F152](RAW_FACTS.md#f152)"
- id: P03
  name: go2rtc
  url: https://github.com/AlexxIT/go2rtc/tree/c245815e75e2a5fd60b4290f12bfc04e55a984d3
  snapshot: "c245815e75e2a5fd60b4290f12bfc04e55a984d3; 2026-07-13"
  license_scope: "MIT repository; FFmpeg is separate dependency/license/build."
  hardware: "Windows/macOS/Linux/FreeBSD and multiple ISAs; hardware transcoding depends on separate FFmpeg path."
  layers: [camera_gateway, relay, browser_video]
  reuse: "Idea/alternative process: gateway for unusual cameras if MediaMTX path is inadequate."
  limitations: "Not mandatory second relay, NVR or NN engine; defaults1984API,8554RTSP,8555TCP/UDP WebRTC must not be automatically internet-exposed."
  evidence: "CODE/DOC; [F219](RAW_FACTS.md#f219)"
- id: P04
  name: Savant
  url: https://github.com/insight-platform/Savant/tree/24a3c8d82fc42cc04a903c71e62084ba7ee9f8a0
  snapshot: "24a3c8d82fc42cc04a903c71e62084ba7ee9f8a0; 2026-09-04; production0.5.x/DS7.0 versus development0.6.x/customDS7.1/TRT10.9."
  license_scope: "Apache2.0 repository; NVIDIA dependencies separately licensed."
  hardware: "Processing tied to NVIDIA; README driver570.133.20+."
  layers: [source_adapters, video_metadata, pipeline, lifecycle]
  reuse: "Idea-only: adapters/source registry, video-metadata association, EOS cleanup."
  limitations: "Whole NVIDIA runtime is expensive for minimum and does not solve LinQ integration; keep production/development baselines distinct."
  evidence: "CODE/DOC; [F220](RAW_FACTS.md#f220)"
- id: P05
  name: DL Streamer
  url: https://github.com/dlstreamer/dlstreamer/tree/51c317f8d969574784caae2ba02c494e40b62002
  snapshot: "51c317f8d969574784caae2ba02c494e40b62002; 2026-10-22"
  license_scope: "MIT repository; OpenVINO/GStreamer/models separately scoped."
  hardware: "Intel CPU/GPU/NPU via OpenVINO; Intel NPU support does not mean arbitrary LinQ."
  layers: [GStreamer_pipeline, metadata, serialization, publishing]
  reuse: "Idea-only: attach metadata, serialize and publish independently of frame pixels."
  limitations: "gvametapublish does not cache or publish metadata during reconnection, so it is not durable outbox."
  evidence: "CODE/DOC; [F221](RAW_FACTS.md#f221), [F078](RAW_FACTS.md#f078)"
- id: P06
  name: Roboflow Inference
  url: https://github.com/roboflow/inference/tree/15d1f4478e1b5cf531ec87ad6d55e30afe58ba0f
  snapshot: "15d1f4478e1b5cf531ec87ad6d55e30afe58ba0f; 2026-10-22"
  license_scope: "Core Apache2.0; nearer subdirectory/model/Enterprise licenses take precedence."
  hardware: "CPU/CUDA paths; no established LinQ path here."
  layers: [video_frame_contract, stream_reader, buffering, inference_pipeline]
  reuse: "Idea-only: VideoFrame/drop/latency contract, ADAPTIVE_DROP_OLDEST for live versus WAIT for files."
  limitations: "Pin legacy_stream versus split stream_vision version; inspect nearest LICENSE before actual copying/import; current minimum imports neither."
  evidence: "CODE/DOC; [F222](RAW_FACTS.md#f222)"
- id: P07
  name: Ultralytics
  url: https://github.com/ultralytics/ultralytics/tree/e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8
  snapshot: "e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8; 2026-10-22"
  license_scope: "AGPL3.0 or Enterprise; weights separately scoped."
  hardware: "CPU/GPU/export is model-specific; no LinQ backend found in inspected material."
  layers: [model_baseline, stream_loader, latest_frame_pattern]
  reuse: "Idea-only for architecture; local model baseline belongs to model_stack."
  limitations: "Loader common barrier may wait for stalled source; returned batch lacks full PTS/epoch contract; not durable NVR/events."
  evidence: "CODE/DOC; [F223](RAW_FACTS.md#f223)"
- id: P08
  name: DeepStream Python Apps
  url: https://github.com/NVIDIA-AI-IOT/deepstream_python_apps/tree/8ad0349ed7a496fae35ebb21c350641727070b89
  snapshot: "8ad0349ed7a496fae35ebb21c350641727070b89; 2026-04-01; README SDK9.0."
  license_scope: "Apache2.0 sample/bindings repository; SDK separately licensed."
  hardware: "NVIDIA/CUDA; Ubuntu24.04/Python3.12/gst-python1.24.1 in inspected README."
  layers: [batching, tee, metadata, source_lifecycle, broker_sample]
  reuse: "Idea-only: batch/tee/metadata/source lifecycle examples."
  limitations: "Bindings deprecated, no wheels from9.0, PyServiceMaker recommended, NumPy2.x unsupported; first-object-every30frames broker sample is not complete incident logic."
  evidence: "CODE/DOC; [F224](RAW_FACTS.md#f224)"
```

## Failure states, degraded demonstration, and notification boundaries

**INFERENCE:** Keep independent `video_state`, `analysis_state`, `recording_state`, `delivery_state`. Dim last processed image and show age; missing results never mean no violations. CPU/RTX fallback is explicitly labeled with separate backend/run/event counters and mandatory-LinQ unavailable intervals. Saved platform-witnessed run is replay, never current live. GUI/unusable-job route remains `unsupported-live`. [F131](RAW_FACTS.md#f131), [F204](RAW_FACTS.md#f204), [Q024](OPEN_QUESTIONS.md#q024).

| Failure | Detection/recovery | Honest visible result |
|---|---|---|
|Camera EOF/native stall; control alive without media|Check decoded sequence/progress/age;close container;bounded exponential backoff+jitter;reopen/restart owned isolated worker;new session identity|Video unavailable/stale;analysis coverage interrupted |
|LinQ timeout/overload|Live deadline+last usable observation age;latest replacement,bounded recovery probe;held persisted,reconcile jobs|Video may remain live while analysis unavailable/degraded |
|Late/old-model/old-epoch output|Validate correlation/version/age;reject live,finish job accounting separately|No stale boxes on new source;reason in metrics/history |
|Hot source/cascade|Fair admission,parent/ROI/byte caps,measured target|Per-camera actual fresh apply FPS/coverage |
|DB stalled/full disk|Bound writer queue/reserve;reject admission;reopen/reconcile after repair|Event uncommitted versus evidence unavailable reported separately |
|Slow/hidden/disconnected UI|Render-credit timeout/close;new generation/latest resync;revision/cursor DB history|Stale/disconnected view;committed incidents recoverable |
|Process/host restore|Fence owners;DB/media/pin/remote-ledger reconciliation|Recovering,partial/missing evidence,unresolved jobs visible |

Reader states `CONNECTING→STREAMING→STALE/ERROR→BACKOFF→CONNECTING`. Fixture backoff0.5,1,2,4…≤10s+jitter is a proposed test profile. Auth/unsupported-codec errors need config repair, not endless reconnect. Watchdog checks decoded progression, not PID/socket. Docker HEALTHCHECK sets unhealthy; restart policy acts on exited process, not automatically live unhealthy container. Need explicit supervisor action or safe process exit; shared remote hardware reset is not implied. [F052](RAW_FACTS.md#f052), [F128](RAW_FACTS.md#f128), [F129](RAW_FACTS.md#f129).

**DOC/HYPOTHESIS image health:** Mandatory progress/age; optional repeated-content,black/underexposed,overexposure,blur,scene-shift only `suspected_anomaly` with per-scene baseline/ROI/suitability/CPU budget. Static scene with new timestamps may be normal; darkness may be lights-off; blur motion/compression; shift legitimate PTZ/forklift occlusion. Axis notes low-detail scene unsuitability and lighting/occlusion ambiguity. Dark detector is not causal lens-tampering proof; overexposure heuristic is our hypothesis, not stated Axis capability. [Axis Image Health](https://help.axis.com/en-us/axis-image-health-analytics), [F201](RAW_FACTS.md#f201)–[F203](RAW_FACTS.md#f203), [E019](OPEN_QUESTIONS.md#e019).

**DOC/UNKNOWN optional messengers:** Telegram FAQ: avoid >1 message/s/chat; groups≤20/min; free broadcast≈30/s; sendVideo≤50 MB; successful Message≠read; retry_after in seconds. MAX docs: `platform-api2.max.ru`, `Authorization: <access_token>` rather than query token, trusted Russian Ministry of Digital Development (Минцифры) certificate chain (not disabled TLS); POST messages≤2/s/dialog/group/channel, overall cap unknown here. No confirmed team accounts/tokens/tests. Private clip URL may be inaccessible to recipient/provider; authenticated incident-card link+thumbnail can be simpler, with verified access. Real messaging tests require separately authorized credentials/recipient. [Telegram FAQ](https://core.telegram.org/bots/faq), [MAX docs](https://dev.max.ru/docs-api), [F120](RAW_FACTS.md#f120)–[F122](RAW_FACTS.md#f122), [Q018](OPEN_QUESTIONS.md#q018).

## Offline deployment, Astra scope, authorization, and network boundary

**INFERENCE:** Own app and proprietary inference worker/client are separate deployment units. API mode uses team-pinned environment without mixing native LinQ ABI. Offline kit includes app commit/config/migrations,chosen wheels/native libs/license notices,static UI without CDN,permitted models+goldens,images with platform/digest,secret-file inventory and sample→event instructions. Data backup separate: `docker image save/load` does not include volumes,host driver,Docker/Compose or LinQ reachability. Proposed `docker compose up -d --no-build --pull never` requires actual CLI support; image save/load `--platform` requires API1.48+. [Docker save](https://docs.docker.com/reference/cli/docker/image/save/), [Docker load](https://docs.docker.com/reference/cli/docker/image/load/), [F012](RAW_FACTS.md#f012), [F013](RAW_FACTS.md#f013), [F209](RAW_FACTS.md#f209).

Clean target test verifies no runtime pip/apt/model/CDN downloads. Offline client≠offline mandatory remote LinQ. Windows workspace≠target OS; x86-64 image≠ARM HX. Astra inventory:edition/update/kernel/ISA,Docker/Compose,privilege/rootless,mandatory labels,mounts,cgroups,device rights,matched driver/runtime,storage. UI-container success proves neither decoder nor NN driver. `depends_on service_healthy` helps startup, not runtime reconnect. Compose file secrets are mounts, not encrypted secret storage; `_FILE` is image convention only. [F008](RAW_FACTS.md#f008)–[F016](RAW_FACTS.md#f016), [E015](OPEN_QUESTIONS.md#e015).

**CLAIM exact scope:**2025-11-13 release describes LinQ HP+Astra Linux Server integration; full-line testing is planned.2026-10-07 release describes LinQ HX+Astra Linux Embedded; certificates refer to Embedded OS. Neither certifies our app/allSKUs/container/remote connection nor supplies matched kernel/driver/runtime. Supported owner configuration is required, not modifying mandatory controls/rebooting shared host to fix Docker. [HP/Server](https://astra.ru/about/press-center/news/gruppa-astra-i-khaytek-obedinyayut-usiliya-dlya-razvitiya-otechestvennykh-ii-resheniy/), [HX/Embedded](https://astra.ru/about/press-center/news/khaytek-i-gruppa-astra-razrabatyvayut-sovmestnoe-reshenie-na-osnove-rossiyskogo-ii-uskoritelya-dlya-/), [F017](RAW_FACTS.md#f017), [F018](RAW_FACTS.md#f018).

**DOC/INFERENCE security minimum:**camera VLAN/segment→restricted ingest gateway→app segment→allowlisted outbound LinQ. Browser gets authenticated HTTPS app route,never camera password/admin URL/LinQ token. Server checks viewer/operator/admin on clip/event/subscription/rule-mutation routes; hidden button is not authorization. Internal media IDs instead of user FS paths. Only responsible modules read secrets; exclude secrets from frontend/logs/image layers/git; no Docker socket or privileged/all-devices to UI for restart. Camera-management HTTPS/Digest does not encrypt RTSP media; verify actual firmware/client/relay secure transport. Gateway tunnel protects only its scope if local leg clear; not camera-origin end-to-end encryption. Ask remote owner about tenant isolation,upload/result/log retention/deletion. NIST segmentation/MFA are engineering guidance, not IEC62443 conformity; legal/KII→market_deployment. [Axis hardening](https://help.axis.com/en-us/axis-os-hardening-guide), [NIST SP800-82r3](https://doi.org/10.6028/NIST.SP.800-82r3), [F019](RAW_FACTS.md#f019)–[F022](RAW_FACTS.md#f022), [F210](RAW_FACTS.md#f210), [Q019](OPEN_QUESTIONS.md#q019).

## Five participants, 45 hours, integration gates, and path to scale

**INFERENCE, not validated effort:** Start one camera/one model/B1/one profile, then two cameras for isolation.225person-hours are not interchangeable schedule capacity. Real golden LinQ run precedes optional messenger/native video/second model. Everyone integrates contracts early. [F206](RAW_FACTS.md#f206).

| Owner | Responsibility | Early joint artifact |
|---|---|---|
|1 video|Source,relay,demux/decode,clock/identity,index/record validation|Frame lineage with2/3;E009 with5 |
|2 LinQ/model|Issued grant,golden I/O+witness,pre/post parity,adapter|Real result for3/4;lifecycle/bytes/buffer lifetime for5 |
|3 temporal|Fair scheduler/per-camera admission,gaps,rules/state;credits with5|Ordered observations,event revisions/coverage |
|4 product|HTTP/auth/history/UI,WS/render/ACK,degraded states|Same-frame projection and committed history |
|5 storage/integration|DB writer/recovery,remote ledger,pins/outbox,manifest/deploy,metrics/runbook|Unified trace,explicit durability boundaries,reproducible bundle |

| Elapsed from case publication | Required gate | Failure/scope consequence |
|---|---|---|
|0–2h|Mandatory case scope;rights/model/network/quota/OS;real golden+witness;positive/empty/error/late fixtures|Localize missing callable route;unsupported-live+labeled mock in parallel;drop optional |
|2–6h|Source→LinQ→same-frame draw→event COMMIT→history;geometry/backend/freshness;actual SQLite patch;earlyE009|Remux failure→snapshot/unavailable clip;tracker failure→ID-method limitation;no second model before full path |
|6–18h|2cameras/stalled-source isolation;held across timeout/restart;epochs/gaps/no old boxes;DB/outbox/pins;full cycle meets method|Cut native video,messenger,cascade,extra tracking;profile/FPS changes only after quality check |
|18–32h|Independently paced stable load;per-camera FPS/maxgap/age;evidence outcomes;slow browser;storage faults/restart|Explicit admission/degraded scope;fewer cameras cannot fix p1 cycle |
|32–40h|Freeze model/stack;clean target/offline client;tested restore/remote reconcile;venue-network rehearsal|Core/deploy/recovery fixes only;saved witness is replay if current access lost |
|40–45h|Reproducible demo/runbook/submission artifacts/regression|Feature freeze;replay cannot replace mandatory live requirement |

Cut order:optional source WebRTC,messenger without access,image-health heuristics,blur/reencode,object storage/broker,extra cascade/tracker,cameras above measured admission. Preserve real LinQ,request/result/geometry binding,freshness/gaps,committed events/history,honest failure/evidence statuses. ID-required method without tracker gate and exact-clip-required case without mapping remain blockers. [F206](RAW_FACTS.md#f206), [Q024](OPEN_QUESTIONS.md#q024), [E018](OPEN_QUESTIONS.md#e018).

**INFERENCE scaling:**50camera candidate can be one measured-admission ingest/record host+adapter,not automatically a cluster.500camera candidate:site sharding,local main recording,measured substream/JPEG WAN or authorized colocated inference,central compact events/control. `500=10×50` does not remove central aggregate traffic. Introduce PostgreSQL/durable broker/object storage/orchestration when ownership distributes across hosts and measured requirements demand it. N+1 needs spare capacity+tested reconnection/ownership transfer;RAID is not N+1. Edge LinQ HX conditional on SDK/decode/RAM/network validation. [Milestone2026r1](https://doc.milestonesys.com/xprotect/xprotect-system-architecture-guide/2026r1/en/overall-system-architecture), [F124](RAW_FACTS.md#f124), [F133](RAW_FACTS.md#f133), [F200](RAW_FACTS.md#f200).

## Proposed E001–E019 practical programme: decisions, inputs, artifacts, limits

**HYPOTHESIS/INFERENCE:** All experiments are **proposed, unexecuted**; detailed procedures in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). Common evidence:immutable input/config/model/artifact hashes,versioned fixture+offered schedule,structured stage traces,resource series,outcome denominators and retained manifests. Only own disposable authorized fixture for destructive fault tests; no implied shared-host reset or messages to real recipients. Simulator/video success never proves LinQ execution.

| Experiment | Inputs and discriminating actions | Decision/metrics and retained evidence; success still excludes |
|---|---|---|
|[E001](OPEN_QUESTIONS.md#e001) issued capability/golden|Actual grant+model+golden;inventory endpoint/rights/OS/quota/I/O,one device run|Select access mode;save capability contract,input/output hashes,IDs+platform witness;single success≠throughput/TTL |
|[E002](OPEN_QUESTIONS.md#e002) ingress/freshness/soak|Looped RTSP and actual builds;continuous latest versus sleep/read,TCP/UDP,media loss with live control,slow/stopped source;10min correctness then2h/overnight if available|Choose reader/timeout/reconnect;source progress,age,RSS/FD/recovery traces;not production reliability |
|[E003](OPEN_QUESTIONS.md#e003) decode cost|Actual CPU/NVDEC/QSV,source codec/profile,GOP;forbid software fallback;decode-only then download/resize/color/pack,cold/warm,paced streams|Measure useful Cdec/pre,copies,CPU/GPU/memory/tails and actual backend;not LinQ/full-service capacity |
|[E004](OPEN_QUESTIONS.md#e004) quality versus bytes|Target RGB annotations,fixed model/pre;paired JPEG/resize/chroma/ROI/sampling sweep|Choose admissible profile via per-class/size recall,missed events,bytes/CPU;no universal JPEG Q or thermal→PPE transfer |
|[E005](OPEN_QUESTIONS.md#e005) saturation/fairness|Paced fake service then actual LinQ;sweep C/B/p_i,crowd cascade,one stopped camera,all resources|Admission curve,per-camera fresh FPS/maxgap/age,counts/bytes/FD/RSS/disk+WAN;aggregate peak≠method SLA |
|[E006](OPEN_QUESTIONS.md#e006) temporal contract|Sparse100/105/110,out-of-order,no-new-answer timer,late/model/epoch changes,validempty versus Gap,fixed-dt/reset cases|Assert ordered one-time live apply,no stale dwell,correct generation/coverage;retain traces;wrapper success≠target ID quality |
|[E007](OPEN_QUESTIONS.md#e007) remote ledger faults|Own fake-job service;lost ACK,crash before/after send,cancel200 still running,hidden retry,late acceptance,restart|Every possible obligation covered by held;no double release;bounded STOPPED/reconcile trace;not actual LinQ semantics |
|[E008](OPEN_QUESTIONS.md#e008) output/NMS/return|Issued raw/compact outputs,names/quantization/classmap,NMS+geometry goldens;poll/fetch/post load|Choose post location/return path;parity,bytes,CPU/RAM/tails;not accuracy or permission without case |
|[E009](OPEN_QUESTIONS.md#e009) early original mapping|Same-demux pre-mux packet index,independent decode,markers/PTS;B0/B2,long GOP,loop,reset/wrap/missingPTS,separate decoder/recorder restarts|No false complete;save bases/rescale/offset/generations/hash/coverage;fail disables custom recorder;not power durability |
|[E010](OPEN_QUESTIONS.md#e010) finite evidence|Delay1/19/21/120s,long/ongoing event,stoppedpostroll,noIDR,lowspace,retention/export race,recorder crash|Finite jobs/pins/bytes/reserves;complete only actual coverage,otherwise partial/unavailable;not arbitrary queue/pre-roll guarantee |
|[E011](OPEN_QUESTIONS.md#e011) renderer credit/lifetime|Fast viewers,3s decode,60s hidden,no/early/wrong-nonce ACK,oldgen,reconnect-before-cleanup,size/DPR caps,SDK/view ownership|Outstanding≤1/connection,decode≤1/page across generations,no stale draw;server/browser/resource traces;ACK≠physical display |
|[E012](OPEN_QUESTIONS.md#e012) blocked transport close|Own blocked writer/client using public close,active+closing cap,cleanup and reconnect|No extra sends/admission above cap;hung cleanup remains visible+counted;public close hard bound unresolved until tested |
|[E013](OPEN_QUESTIONS.md#e013) optional native video|Actual browser/codec/network/NAT,WHEP lifecycle,source↔RTP↔rVFC mapping,WebRTC/LL-HLS|Enable overlay only on proven mapping;save network/lifecycle+optical traces;defaults≠end-to-end latency |
|[E014](OPEN_QUESTIONS.md#e014) outbox/history|Fake provider accepted-without-local-ACK,429/500/timeout,poison payload;UI revision/cursor replay|No lost committed event;duplicates explicit,finite dead policy;actual bots only authorized credentials;provider accept≠read |
|[E015](OPEN_QUESTIONS.md#e015) artifact/offline/security|Actual target inventory/hash/ABI/SQLite source_id/PRAGMA/licenses;clean offline launch,Astra variant,TLS/auth/secret redaction|Ship known installable kit and tested route authorization;not pentest/certificate or automatic LinQ reachability |
|[E016](OPEN_QUESTIONS.md#e016) DB/file/restore faults|Own disposable storage;COMMIT/BUSY/IOERR,long-readerWAL,process/OS/power/disk separately;backup+old-cutoff restore with later accepted remotejobs|No false success without restored row within stated guarantee,no falsecomplete,no deletion before pin rebuild;process kill≠power test;measure RPO/RTO |
|[E017](OPEN_QUESTIONS.md#e017) alarm timing|Timestamp/LED optical or calibrated clocks;mark physicalonset,ruleeligible,commit,draw;fixed offered load|Onset→alarm versus eligible→alarm,clock error,misses/timeouts/censoring in denominator;not human read unless measured |
|[E018](OPEN_QUESTIONS.md#e018) integrated mode gate|One source/frame→request/model/LinQrun/result→eventrevision/evidence→draw,then2cameras,fault/recovery|Mode supported/degraded/unsupported and actual 45h slice feasibility;golden device proof required;2cameras≠50/500 |
|[E019](OPEN_QUESTIONS.md#e019) optional image health|Scene positives+negatives:lights/static/loop/PTZ/truck,syntheticblur/dark/shift|Per-scene suitability,false alarms/CPU;remove if controls inseparable;no causal tampering proof/universal threshold |

## Open questions: priorities, closure routes, and consequences

**UNKNOWN:** All Q remain open operationally. W2 closed/refined engineering proposals, not execution. Ask first Q001/Q002/Q003/Q005/Q025; then actual source/full-cycle/evidence/runtime gates. [W2 dispositions K001–K010](CRITIC.md#k001-w2) distinguish conceptual closure from runtime unknowns.

| Q | Priority and exact missing decision | Closure route |
|---|---|---|
|[Q001](OPEN_QUESTIONS.md#q001)|P0,0–2h:issued access mode,own-model update and accepted device witness|Owner+grant+E001/E018 |
|[Q002](OPEN_QUESTIONS.md#q002)|P0,0–2h:quota namespace/weights,idempotency scope/window,lookup/terminal/TTL/acceptance cutoff,hidden retries,native borrowed-buffer release|Issued manual/owner+E001/E007/E016;no reliable reconcile→STOPPED |
|[Q003](OPEN_QUESTIONS.md#q003)|P0,0–2h:persistent remote CPU/codecs/DB/ports/storage/privacy/source reachability|Owner/network inventory+E001/E005/E008/E018;otherwise local data plane |
|[Q004](OPEN_QUESTIONS.md#q004)|P0,first2h:actual source codec/profile/FPS/GOP/bitrate/PTS|Probe supplied source+E002/E009;no inherited bitrate/GOP guarantees |
|[Q005](OPEN_QUESTIONS.md#q005)|P0,first2h:required FPS/cadence/maxgap/dwell/onset/coverage/ID|Full case+violation_methods+E006/E017/E018 |
|[Q006](OPEN_QUESTIONS.md#q006)|P0/P1:actual hardware/CPU/QSV/NVDEC useful decode capacity|Inventory now,E003 after slice |
|[Q007](OPEN_QUESTIONS.md#q007)|P0 aftergolden:usable full-chain cycle and per-camera feasibility|E005/E008/E018 with actual service;aggregate FPS insufficient |
|[Q008](OPEN_QUESTIONS.md#q008)|P0 beforequalityclaim:JPEG/resolution/chroma/ROI on targetRGB PPE|Target data/model+paired E004 |
|[Q009](OPEN_QUESTIONS.md#q009)|P0/P1:model,batch,partialbatch,statefulsequence,cascade/mandatoryNN boundary|Fullcase+model_stack+issuedruntime+E001/E005/E008 |
|[Q010](OPEN_QUESTIONS.md#q010)|P0,2–6h:event→original mapping and whether snapshot acceptable|E009/E018+caseowner;exactclip mandatory leaves blocker on failure |
|[Q011](OPEN_QUESTIONS.md#q011)|P0/P1:evidence acceptance/pre/post/retention/quotas|Product/case requirements+E010;finite policy required |
|[Q012](OPEN_QUESTIONS.md#q012)|P1 beforedurabilityclaim:FS/VFS/sync,backupfailure domain,RPO/RTO|Target inventory+E010/E016 |
|[Q013](OPEN_QUESTIONS.md#q013)|P0/P1 beforefreshnessclaim:profile/credit/teardown,totalRSS|Actual browser/network+E011/E012 |
|[Q014](OPEN_QUESTIONS.md#q014)|P1 optional:nativecodec/NAT/source↔RTP↔rVFC mapping|E013,otherwise no native-video overlay |
|[Q015](OPEN_QUESTIONS.md#q015)|P0/P1,2–6h:actual installed target/Astra/binaries/ABI/linkedpatchedSQLite|E015,E016;manifest is provisional |
|[Q016](OPEN_QUESTIONS.md#q016)|P1 beforedistribution:actual code/native/weights/data licenses|Artifact/path-level notices review→model_stack/datasets+E015 |
|[Q017](OPEN_QUESTIONS.md#q017)|P1:event rate,DB/broker need,external idempotency|Measured load+providercontract+E014/E016 |
|[Q018](OPEN_QUESTIONS.md#q018)|P0/P1:alarm delivery boundary,accounts/channels/privateURL access|operator_product+authorized E014/E017;accept/draw/read distinct |
|[Q019](OPEN_QUESTIONS.md#q019)|P1:camera encryption,tenant isolation,video retention/deletion/privacy|Owner+firmware/client/network inventory+E015 |
|[Q020](OPEN_QUESTIONS.md#q020)|P1 afterslice:long RTSP freshness/RSS/drift/reconnect|E002 soak on actual stack |
|[Q021](OPEN_QUESTIONS.md#q021)|P0/P1 if IDmethod:cadence/reset/installability/IDquality|violation_methods+E006,target annotated tracks |
|[Q022](OPEN_QUESTIONS.md#q022)|P1 beforecapacityclaim:directional goodput/clocks/resource coefficients/Cinf/Kremote|E003/E005/E008/E017;no board count now |
|[Q023](OPEN_QUESTIONS.md#q023)|P2 optional:imagehealth thresholds,falsealarms,suitability|E019 controls,otherwise omit |
|[Q024](OPEN_QUESTIONS.md#q024)|P0 scopego/no-go:accepted fallback/replay and actual45hfeasibility|Fullcase+E018;replay/mock cannot silently satisfy mandatorylive |
|[Q025](OPEN_QUESTIONS.md#q025)|P0 aftergolden:actual outputheads/quantization/NMS/return/postbudget|Issued I/O+E008;CPU post permission and actual device boundary |

## Handoffs to neighboring topics

- **→ linq_platform:** Q001–Q003/Q025,E001/E007/E008:actual rights/model/I/O/lifecycle/quota/terminal/buffer release/device witness. API can suffice without SSH;HX RK3588 decode/HPS optional encode are product-specific. [F215](RAW_FACTS.md#f215), [F225](RAW_FACTS.md#f225).
- **→ model_stack:** actual dtype/layout/scales/classmap/NMS/coordinate output parity,batch/stateful/ROI/cascade scope;raw result return may dwarf JPEG input and crowd jobs alter occupancy. CPU post does not replace device proof. **→ datasets/training_strategy:** target RGB quality set and precise weight/data rights;repo license is not their license. [F147](RAW_FACTS.md#f147)–[F149](RAW_FACTS.md#f149), [F182](RAW_FACTS.md#f182), [Q008](OPEN_QUESTIONS.md#q008), [Q009](OPEN_QUESTIONS.md#q009), [Q016](OPEN_QUESTIONS.md#q016).
- **→ violation_methods:** full temporal contract,minFPS/maxgap/cadence/coverage/dwell/reset/ID;Gap is unknown,PTS cannot change fixed ByteTrack dt,full-cycle p1 limits observation cadence. Tracker-free boxes do not satisfy ID-dependent methods. **→ evaluation:** paired compression/sampling tests;source onset and ruleeligible boundaries;clock uncertainty;full denominator with late/missed/censored outcomes. [F173](RAW_FACTS.md#f173)–[F184](RAW_FACTS.md#f184), [F132](RAW_FACTS.md#f132), [E004](OPEN_QUESTIONS.md#e004), [E006](OPEN_QUESTIONS.md#e006), [E017](OPEN_QUESTIONS.md#e017).
- **→ operator_product:** independent video/analysis/evidence/delivery states;pending/partial/unavailable clips;eventCOMMIT≠provideraccept≠draw≠operatorack. User/case determines snapshot acceptability,retention and channel needs;messenger optional. **→ market_deployment:** directional50/500,VBR/retention/I/O reserves,exact OS/Astra/security/license boundaries;not procurement capacity,legal opinion or certification. [F119](RAW_FACTS.md#f119), [F159](RAW_FACTS.md#f159)–[F161](RAW_FACTS.md#f161), [F171](RAW_FACTS.md#f171), [F187](RAW_FACTS.md#f187), [F198](RAW_FACTS.md#f198)–[F200](RAW_FACTS.md#f200).
- **→ hackathon_strategy:** real golden/device witness and integrated trace precede optional features;five owners/gates/cuts,explicit unsupported-live and CPU/RTX/mock/replay labels.45h is schedule difference,not LinQ availability;exactclip/ID requirements remain blockers after failed gates. Demo one trace `backend→source/request/result→event/evidence→render` with controlled failure/recovery and complete denominators. [F023](RAW_FACTS.md#f023), [F024](RAW_FACTS.md#f024), [F204](RAW_FACTS.md#f204), [F206](RAW_FACTS.md#f206), [E018](OPEN_QUESTIONS.md#e018).

These are saved handoffs, not newly launched neighboring research or external messages. Remaining unknowns require the actual case/grant/artifacts and practical wave; the architecture remains a conditional proposal.
