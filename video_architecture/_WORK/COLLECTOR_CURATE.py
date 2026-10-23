"""Curated cross-wave questions/experiment program and final evidence assembly."""
import BUILD_COLLECTOR as c
import re,json,hashlib
from pathlib import Path
Q=[];E=[]
def q(n,title,priority,known,why,decision,closure,refs,aliases):
    Q.append(dict(id=f'Q{n:03}',title=title,priority=priority,known=known,why=why,decision=decision,closure=closure,refs=refs,aliases=aliases.split()))
def e(n,title,decision,inputs,steps,metrics,outcomes,limit,refs,aliases):
    E.append(dict(id=f'E{n:03}',title=title,decision=decision,inputs=inputs,steps=steps,metrics=metrics,outcomes=outcomes,limit=limit,refs=refs,aliases=aliases.split()))

q(1,'Issued LinQ grant, собственная модель и принятое доказательство исполнения','P0 / 0–2ч',
  'Прочитаны LinQ homepage/tech/sol, официальный анонс и вторичный linq_platform. Обещаны онлайн-доступ и inference на LinQ; публичная download/demo форма не даёт callable API, custom-model update или granted host.',
  'Нет полного кейса, issued manual/schema, account/grant, matched SDK/native/driver/firmware/model artifacts и принятого execution witness. CPU/mock соседей не device run.',
  'Выбирает API, shell, managed video, job или unsupported-live. Service-only без SSH может быть достаточен; GUI-only без машиночитаемых результатов — нет.',
  'Постановщик + полный кейс + issued артефакт + E001/E018. Сохранить manual revision, allowed model boundary/update, hashes golden input/model/output, request/run/device correlation и accepted witness.',
  'W1-01-F01 W1-01-F03 W1-01-F05 W1-01-F07 W1-01-F23 W2-06-F09 K010 E001 E018',
  'W1-01-Q01 W1-03-Q01 W1-06-Q01 W2-06-Q02')
q(2,'Remote lifecycle, quota, ambiguous submit и native input lifetime','P0 / 0–2ч',
  'AWS Batch — один документированный аналог: cancel200 не terminal, running timeout не queue TTL, zero ListJobs не negative proof. Спроектирован persisted held ledger, отдельные local/control/fetch caps и bounded STOPPED.',
  'LinQ submit dedup scope/window, lookup visibility, definitive rejection, hidden retries, accepted/running weights, terminal/release/acceptance-cutoff/TTL и safe buffer release не выданы. Старый backup может не знать post-cutoff jobs.',
  'Без доказанного release удержать remote credit через timeout/epoch/restart/restore. View TTL освобождает view bytes, не native borrowed input. Нет reliable reconcile — stop соответствующего admission, не held=0.',
  'Issued manual/owner + E001/E007/E016. Только разрешённые benign calls; lost ACK в own fixture. Фиксировать tenant/quota namespace, terminal witness и режим без auto-resume.',
  'W2-01-F01 W2-01-F03 W2-01-F05 W2-01-F06 W2-01-F10 W2-01-F11 W2-01-F12 W2-01-F13 W2-03-F09 W2-05-F11 K001 E007 E016',
  'W1-01-Q03 W1-03-Q02 W1-04-Q01 W2-01-Q01 W2-01-Q02 W2-03-Q02 W2-05-Q03 W2-02-Q05')
q(3,'Разрешённое размещение decoder/pre/post и app data plane','P0 / 0–2ч',
  'HPS optional video encode и HX/RK3588 decode — разные host/product claims. SSH/VPN не даёт root/Docker/ports/daemon lifetime. Remote compact boxes не обеспечивают analyzed pixels на local projection.',
  'Неизвестны host CPU/RAM/ISA/codec/permissions, source reachability, persistence, listeners/tunnel и права CPU NMS/wrapper. Нельзя считать remote RTSP из private LAN доступным.',
  'При frame API весь app у команды. Remote decode minimum переносит единый app data plane/DB/recorder/projection к decoder только при полном grant; иначе thin worker и local decode. Возврат JPEG при remote decode — отдельный downlink.',
  'Owner grant/network inventory + E001/E005/E008/E018; сравнить один clip в допустимых placements, отдельно CPU/network/privacy. Не устанавливать web/DB на shared host без предоставленного права.',
  'W1-01-F06 W1-02-F01 W2-01-F14 W2-06-F04 W2-06-F09 K006 K010 E008 E018',
  'W1-01-Q02 W1-02-Q01 W2-01-Q04')
q(4,'Реальные source codec/profile/FPS/GOP/bitrate/PTS','P0 / первые2ч',
  'RTSP/ONVIF/media controls различены; sampling после decode не снижает автоматически decode source FPS. Main/sub могут отличаться crop/FOV/clock; loop — simulated source.',
  'Нет организаторских видео/камер, firmware, profiles, ffprobe sample, B-frames/IDR bound, VBR distribution, source NTP/PTS discontinuity rules.',
  'Определяет decode compatibility, encoder/GOP recovery, bytes/ring cap и timestamp mapping. Missing PTS запрещает exact clock по FPS/host now.',
  'Полный кейс/source artifact/камера + ffprobe inventory и E002/E003/E009; сохранить hashes, codec/profile/pix_fmt/FPS/time_base/keyframe structure и raw timestamp trace.',
  'W1-02-F14 W1-02-F16 W1-02-F17 W1-02-F18 W1-02-F19 W2-02-F02 W2-02-F09 K002 E002 E009',
  'W1-02-Q03 W1-05-Q02 W2-02-Q03')
q(5,'Domain temporal contract: required FPS/max gap/dwell/onset/ID','P0 / первые2ч',
  'Анонс перечисляет примеры нарушений. Gap не negative, mean5fps не max-gap guarantee, physical dwell не update count; короткое событие может не попасть sampler.',
  'Полный обязательный перечень/точность/задержка/минимальный coverage/ID continuity/onset и interruption semantics отсутствуют. Сетевой tracker поиск этих требований не устанавливает.',
  'Без этого5fps, T_fresh и max_gap — сценарии, не SLA. Снижение FPS/camera count допускается только в пределах метода; no-tracker route не заменяет ID-dependent метод.',
  'Полный кейс + violation_methods/evaluation/operator_product + E004/E006/E017/E018. Versioned contract с units, denominators, cadence tolerance, missing-PTS policy и quality thresholds.',
  'W1-04-F17 W1-06-F14 W2-04-F01 W2-04-F13 K005 K010 E006 E017',
  'W1-03-Q03 W1-04-Q02 W1-06-Q02 W2-04-Q01 W2-06-Q01')
q(6,'Фактическое железо и CPU/QuickSync/NVDEC decode capacity','P0/P1 / inventory сразу, нагрузка послеslice',
  'В контексте только RTX4070 и ноутбук. NVDEC13.0 Ada indicative table и T4 DeepStream7.1 — внешние измерения с иными условиями. Portable CPU/QuickSync decode-only per-core числа не найдены; encode/transcode отсечены.',
  'CPU, exact SKU/VRAM/driver/thermal power mode, codec backend/build, surfaces/copies и sustained throughput ещё не измерены.',
  'Выбор software/hardware decode, threads/shards, resize-before-download и безопасный admission. Нельзя вывести число камер из903fps, TOPS или одной raw latest-slot оценки.',
  'Локальный hardware/build inventory + E003/E005. Указать source corpus/codec/GOP, warmed/cold, CPU-seconds/frame, decode+transfer+resize отдельно и per-camera freshness под paced load.',
  'W1-02-F21 W1-02-F22 W1-02-F23 W1-02-F24 W1-02-F25 W1-06-F01 W2-06-F01 W2-06-F02 E003 E005',
  'W1-02-Q02 W1-02-Q05')
q(7,'LinQ usable full-chain cycle и per-camera feasibility','P0 / послеgolden',
  'Необходимы два ограничения: per-camera f_i≤p_i/E[L_i] и aggregate occupancy/capacity; L включает client NMS/cascade/ordered apply. p1,L300ms даёт≤3.33fps даже при K100.',
  'Нет measured L/tails, endpoint concurrency/thread-safety/batch, service capacity/shared fairness и minimum domain FPS/maxgap. 1/p95(L) не tail guarantee.',
  'Не обещать5fps/camera по aggregateFPS. p>1 — только при supported stateless/sequencing + bounded sparse sent-ID reorder и полезном выигрыше freshness.',
  'Issued SDK/API/model + E005/E006/E008/E018 с реальным LinQ. Saturation curve и каждый camera admitted/applied/gaps/age; remote-held accounting отдельно от local parent slots.',
  'W1-03-F17 W2-04-F09 W2-04-F10 W2-04-F11 W2-04-F12 K005 E005 E018',
  'W1-06-Q05 W2-04-Q02')
q(8,'JPEG/resolution/chroma/ROI quality на целевых RGB СИЗ','P0 / доquality claim',
  'Два первичных исследования FLIR thermal/COCO показывают риск recall tiny/small. Их Q30/Q40/размерные bins и модели не PPE threshold. Q100 не lossless, camera baseline уже compressed.',
  'Нет target RGB labelled sample/модели/thresholds и paired predictions для каски, респиратора, сигареты, дальностей/освещения/толпы.',
  'JPEG size — переменная distribution, не обещанное compression ratio. ROI discovery/crop fanout и resize могут менять quality/compute; нельзя экономить сеть без quality gate.',
  'Datasets/model_stack/evaluation + E004. Paired encode grid с fixed model/preprocess; bytes/CPU и recall по классам/размеру плюс event missed/false alarms.',
  'W1-03-F11 W1-03-F12 W1-03-F16 W1-05-F09 E004',
  'W1-03-Q04')
q(9,'Модель, batch/stateful sequence и каскадная NN-граница','P0/P1',
  'Triton/Hailo — только образцы. ROI discovery тоже работа; person/PPE cascade требует bounded q_max и secondary unknown при quota drop.',
  'Не выбраны actual model artifacts/input layout/dtype/quant scales/fixed or dynamic batches/state affinity, secondary cost и допустимая обязательная LinQ boundary.',
  'Определяет preprocessing ownership, batch families, primary/secondary caps и допустимость temporal latest-drop. Не считать arbitrary uint8/JPEG/batch поддержанными.',
  'Model_stack/linq_platform + issued artifacts/полный кейс + E001/E004/E005/E008. Каждый revision повторяет golden/parity; accepted NN boundary фиксируется отдельно от CPU postprocess.',
  'W1-03-F02 W1-03-F09 W1-03-F13 W1-03-F14 W2-04-F11 E005 E008',
  'W1-03-Q05 W1-03-Q07')
q(10,'Event→original segment mapping и допустимость snapshot cut','P0 / раннийgate2–6ч',
  'MediaMTX1.21.2 mtxi содержит recorder StreamID/SegmentNumber/DTS/NTP, не decoder/source epoch; hooks/UTC filename не дают source PTS. Native export теряет mtxi. Same-demux indexed remux — prospective route.',
  'Не выполнен packet-lifetime/reorder/rescale/coverage fixture; missing/duplicate PTS, loops, wrap, decoder-only/recorder-only restart, main/sub uncertainty не измерены.',
  'До E009 нет exact clip claim. Gate fail → analyzed snapshot + optional native archive mapping unknown. Если full case требует exact clips, такой cut остаётся blocker.',
  'Source inventory+собственный prototype+E009/E010/E016. Один H264 video-only профиль/демux owner, indices ДО mutable mux, independent decode watermark и0false-complete.',
  'W1-04-F15 W1-05-F20 W2-02-F01 W2-02-F03 W2-02-F04 W2-02-F05 W2-02-F09 K002 E009 E018',
  'W1-04-Q03 W1-05-Q03 W2-02-Q02 W2-05-Q05 W2-06-Q04')
q(11,'Finite evidence acceptance, pre/post/retention и квоты','P0/P1',
  'Unbounded remote delay нельзя покрыть finite ring. Проект L_evidence20/P5/Q5/S2/G≤1/C4/J30/H40s и chunk/rollover/quota bounds сохранён как fixture, не требования. Old onset после dwell учитывать отдельно.',
  'Нет требуемого evidence window/retention/допустимой partial/snapshot политики, actual max bitrate/GOP/disk и максимальной задержки выдачи.',
  'Нужны finite pin admission deadlines, future ranges, job/count/byte caps и visible late/partial/unavailable; не расширять ongoing job бесконечно и не удалять pinned молча.',
  'Полный кейс/operator_product+device/storage inventory+E010. Требования могут сделать snapshot cut недопустимым; long queue не исправляется только большим H.',
  'W1-05-F08 W1-05-F09 W2-02-F10 W2-02-F11 W2-02-F12 K003 E010',
  'W1-05-Q01 W1-06-Q04 W2-02-Q01')
q(12,'Target filesystem, commit/file sync, backup failure domain, RPO/RTO','P1 / доdurability claim',
  'SQLite WAL+FULL, patched engine и successful COMMIT — выбранный proposal; DB transaction не включает обычные media files. Supported Connection.backup+verified closed-media inventory, restore/fencing/pin rebuild/remote reconcile описаны.',
  'Не известны FS/VFS/device caches/fsync/directory-persistence recipe, storage reserve, power/disk-loss behavior, backup interval/failure domain/key recovery и actual RPO/RTO. Ни один fault run не выполнен.',
  'Process kill не power-loss proof; old backup не held=0. До pin rebuild запрещено retention deletion; missing original/unknown mapping не complete.',
  'Exact target/диск+E010/E016; separate process crash, reboot, OS/power fault, disk loss на disposable authorized testbed; externally durable commit witness и verified backup cutoff.',
  'W2-05-F05 W2-05-F08 W2-05-F09 W2-05-F10 W2-05-F11 W2-05-F12 K008 E016',
  'W1-05-Q06 W2-02-Q04 W2-05-Q04')
q(13,'Processed view runtime: profile, credit, teardown и total RSS','P0/P1 / доfreshness claim',
  'Pinned websockets17.0.1 чтение подтверждает directions watermarks и send≠render. Проект1outstanding/connection, exact ACK after draw, credit-cycle age guard, active+closing admission caps; timeout terminal, не новыйcredit.',
  'Нет browser/OS/RTT/throughput/tiles/quality/age inventory; public close_timeout не доказанный wall-clock teardown bound, app-owned references не total kernel/browser RSS.',
  'Профиль/количествоtiles/FPS/connection cap допускаются по тесту; closing продолжает занимать budget. Экспериментальный transport.abort subclass не public websockets API и не mandatory minimum.',
  'E011/E012 на exact Python/browser/TLS/proxy/OS; source checksum/ACK/draw trace, hidden/reconnect/blackhole и process RSS/FD/task trends. Physical scanout/operator read отдельно.',
  'W2-03-F01 W2-03-F02 W2-03-F03 W2-03-F05 W2-03-F06 W2-03-F07 W2-03-F08 W2-03-F10 K004 E011 E012',
  'W2-03-Q01 W2-03-Q04')
q(14,'Optional native browser video: codec, NAT и source↔RTP↔rVFC mapping','P1 / optional послеcore',
  'MediaMTX reader/WHEP signaling lifecycle и ICE media path различны. H265/B-frames/browser ограничены; rVFC best-effort и не произвольный camera frame ID. HEAD reader W1 не lock к1.21.2.',
  'Нет actual browser codec/selected candidate pair, TURN/cert/domain/port grants и sourcePTS→RTP/SSRC/epoch mapping uncertainty. HTTPS200 не media connectivity.',
  'Плавный original live отдельно от analyzed own-frame view. Без mapping boxes на latest native frame не рисовать как measurement.',
  'E013 на площадке; same-tag reader/server, OPTIONS/POST/PATCH/DELETE/CORS, UDP blocked/subpath/TURN и independent frame markers; exact overlay только после доказанного mapping.',
  'W1-05-F10 W1-05-F11 W1-05-F12 W1-05-F13 W1-05-F18 W1-05-F19 K004 E013',
  'W1-05-Q04 W1-05-Q05')
q(15,'Provisional artifact baseline vs actual installed target/Astra','P0/P1 / 2–6ч',
  'Candidate MediaMTX1.21.2/PyAV16.0.1/CPython3.12.15 source/websockets17.0.1/linked patched SQLite3.51.3. CPython3.12.15 source-only; no official Windows installer. Exact PyAV Linux wheel был read-only inspected, не imported.',
  'Binary target OS/ISA/ABI/glibc/engine/Compose/image digests/driver и linked SQLite source_id/compile_options неизвестны. Python patch не определяет SQLite. Astra news scopes не support matrix приложения.',
  'Не обновлять proprietary supplied env доclient Python. Offline own bundle и LinQ network availability различны; W1 catalog snapshots не requirements lock.',
  'E015 + issued/vendor supported artifacts. Verify actual Python connection SQLite advisory/PRAGMA; clean-target/offline-client smoke и полныйgolden. Поддержанный vendor backport документировать вместо угадывания version tuple.',
  'W1-01-F14 W1-01-F15 W1-01-F17 W1-01-F18 W2-05-F01 W2-05-F02 W2-05-F04 W2-05-F06 K007 E015',
  'W1-01-Q04 W1-04-Q04 W2-03-Q03 W2-05-Q01 W2-06-Q06')
q(16,'Лицензия фактически shipped code/native libs/weights','P1 / доdistribution',
  '8catalog entries имеют direct repo scope. PyAV BSD wrapper не весь bundled libav/x264/x265/gnutls; Linux wheel strings/ZIP и workflow прочитаны. Roboflow nearest superseding license, Ultralytics AGPL/enterprise, SDK/weights отдельно.',
  'Нет полного shipped artifact inventory/transitive notices/source obligations, standalone ffmpeg buildflags/hash, proprietary redistribution terms и model/dataset licenses. Идеи изunused catalog не shipped dependency.',
  'reuse_mode process/dependency/copied-code/idea-only меняет scope. Другой wheel/OS требует своего чтения. License repo нельзя объявлять license всего продукта.',
  'Фактический manifest+primary license texts/vendor terms+E015; exact copied path nearest LICENSE и notices, model_stack/datasets. Не выполнять аудитunused projects ради каталога.',
  'W1-04-F02 W2-05-F03 W2-05-F04 K007 E015',
  'W1-04-Q05 W2-05-Q02')
q(17,'Event rate, DB/broker need и external idempotency','P1',
  'Одна SQLite БД/one writer/outbox — proposal; WS/SSE projection, CoreNATS ephemeral, Redis pending reclaim и broker QoS не exactly-once external effect. Crash after send beforemarker допускает duplicate.',
  'Нет required event/update rate, concurrent operator writers/retention, acceptable backlog и provider durable idempotency key/receiver inbox.',
  'Брокер/PostgreSQL вводить после measured need; не держать DB lock во время network await. Один dispatcher дляminimum, stable event_id/revision и восстановлениеhistory.',
  'Полный кейс/operator_product+E014/E016. Event generator в units events/s, не cameraFPS; measured commit/backlog age/WAL/duplicates и receiver contract.',
  'W1-04-F19 W1-04-F20 W1-04-F21 W1-04-F22 W1-04-F23 W1-04-F24 W1-04-F25 W2-05-F07 K008 E014',
  'W1-04-Q06 W1-04-Q07')
q(18,'Alarm delivery boundary, messenger accounts и product access','P0/P1',
  'Event decided/committed/provider accepted/browser drawn/operator acknowledged — разные endpoints. Telegram/MAX rates/docs прочитаны, не измерены/не отправлялись сообщения. MAX endpoint/auth/certificate менялись.',
  'Нет полного product канала/recipient IDs/токенов/правабота/MAX business access, network accessibility и accepted alarm boundary/age. Read receipt/latency SLA не установлены.',
  'Core — event history/UI; messenger optional послеaccess. Clip pending не задерживаетinitialalarm. Provider timeout послеaccept — uncertain outcome/possibleduplicate.',
  'Operator_product+owner credentials+E014/E017. Fake provider сначала; реальные тестовые отправки только отдельно авторизованной практикой, не production recipients.',
  'W1-05-F21 W1-05-F22 W1-05-F23 W1-05-F24 W1-05-F25 W1-05-F26 W1-06-F13 E014 E017',
  'W1-05-Q07 W1-06-Q03')
q(19,'Camera encrypted transport, tenant isolation и protected data boundary','P1',
  'Axis/NIST/Docker docs дают ограниченный example: HTTPS admin не encrypted RTSP, Digest не encryption, VLAN/firewall по flow inventory, role/auth уclip/stream endpoints; Compose secrets не encrypted vault.',
  'Не известны camera firmware/client TLS/SRTP/RTSPS/account support, remote tenant isolation/upload retention/logging/delete policy, keys/permissions и approved network routes.',
  'Camera credentials остаются только унеобходимого owner, browser получаетauth application path. Удалённый decode/recording выбирается вместе privacy/persistence policy, не толькоbandwidth.',
  'Device/vendor/remote owner + E015 functional security checks. Exact flow table, invalid-cert failures, viewer/operator/admin and secret-redaction; legal/КИИ →market_deployment.',
  'W1-01-F11 W1-01-F19 W1-01-F20 W1-01-F22 E015',
  'W1-01-Q05 W1-01-Q06')
q(20,'Долгая RTSP freshness/RSS, drift и reconnection','P1 / послеslice',
  'FFmpeg/GStreamer/PyAV/OpenCV knobs и version-specific negative cases сохранены. rtspsrc tcp-timestamp обходит drift, но burst source создаёт иной риск; timeout не stale-age bound.',
  'Нет 2h/overnight paced run actual source/backend, read/control-alive-no-media, native hang cleanup, continuous loop reset evidence и true/false tcp-timestamp comparison.',
  'PyAV vs знакомый GStreamer, TCP/UDP и watchdog определяется progress/RSS/frame-watermark tests. ret=True/PID/socket alive недостаточны.',
  'E002 с pinned build/known source, slowconsumer, publisherloss/restart, media blackhole/control alive;10min correctness затем2h/ночь еслидоступно. Не смешиватьpublisher transcode сisolated decode.',
  'W1-02-F02 W1-02-F05 W1-02-F09 W1-02-F26 W1-02-F27 W1-02-F28 E002',
  'W1-02-Q04 W1-02-Q06')
q(21,'Opaque tracker cadence/reset и ID quality','P0/P1 дляID-dependent метода',
  'Pinned ByteTrack dt1/update, frame_rate толькоlostbuffer; no-callfreeze, empty(0,5) реальноеobservation, no publicgap/reset. Новыйinstance+tracking_generation — projectwrapper. НаличиеPTS не variable dt.',
  'Нет tracker smoke/installability/footprint/domainIDmetrics или допустимого short-gap carry. Старые np.float/imports иdependencies не tested. Universal cadence/maximumgap неизвестны.',
  'Trackeroptional gate; strict cadence violation→reset/unknown. Если ID нужно, gate fail даётdegraded/unsupportedметод, не замена per-frameboxes.',
  'E006 с pinned reference/code, source-time uniform/burst equalmean/drop/empty/longgap, separate orderingtrace и annotateddomainquality. Другойgap-awaretracker/адаптация требует validation.',
  'W2-04-F02 W2-04-F03 W2-04-F04 W2-04-F05 W2-04-F06 W2-04-F07 W2-04-F08 K005 E006',
  'W1-02-Q07 W2-04-Q03 W2-04-Q04')
q(22,'Направленные goodput/clock/resource coefficients для50/500','P1 / доcapacity claim',
  'Сценарные таблицыinput/return/view/control/storage иmemoryinventory сохранены. 500registered !=500tiles/viewer. RAM includesDPB/surfaces/contexts/pools/borrows/TLS/DB, а не rawslot.',
  'Нет measuredWAN↑↓/RTT/jitter/clockoffset, FD/ports/session/process/thread/VRAM/IOreplay+backup andmcam/Cinf/Cdec/Cpre/Cwrite coefficients.',
  'Нет одногоnetworkX или числаLinQплат. 50candidatehost послетеста;500shards/sites roadmap. Условия ресурсов проверяются вместе сper-camera temporalgate.',
  'E003/E005/E008/E011/E016. Build topology/dataflow поhost/direction иactual profile tails; same-hostmonotonicdurations, optical/sync uncertainty дляcross-hostage.',
  'W1-03-F16 W1-03-F17 W1-06-F15 W2-01-F15 W2-06-F02 W2-06-F03 W2-06-F04 K006 E005',
  'W1-03-Q06 W2-06-Q03')
q(23,'Camera image-health thresholds/false alarms/suitability','P2 / optional',
  'Axis product docs разделяют image-health/causality и unsuitable scenes. Progress/age mandatory; repeated/black/white/blur/shift signals — hypotheses suspected_anomaly, не tamperproof.',
  'Нет сцен/thresholds/qualityfalsealarms/camera-hour/CPUcost и daynight/static/detailpoor/legitimatePTZ controls. Overexposure heuristic не заявленная Axiscapability.',
  'Можно показыватьavailability/staleness; imageanomaly включать лишь сbaseline/configrevision/suitability иvisible suspectedlabel.',
  'E019 positive/negativecorpus; unseparablecontrols→cut. Realcamera/modelqualityне выводятся изsynthetic distortion.',
  'W2-06-F06 W2-06-F07 W2-06-F08 K009 E019',
  'W2-06-Q05')
q(24,'Accepted fallback/replay и фактическая45ч feasibility','P0 / scopego-no-go',
  '45ч — разностьофициальногорасписания, неguaranteedLinQ uptime. Естьconditionalminimum/5owners/gates/cuts; hardwaremock/media/DBrouteне запущены. CPU/RTX/replayдолжныбытьmarked.',
  'Полныйкейс/acceptedexecutionproof/currentgrant/requiredfeatures иуспеваемостьimplementationне подтверждены;225person-hoursневзаимозаменяемы.',
  'GoldenrealLinQвыше optionalfeatures; GUI/jobбезusableoutputs/turnaroundunsupported-live. Snapshotcutне закрываетобязательныеexactclips.',
  'Fullcase/organizeracceptance+E001/E018 иcheckpointdemo. Retainwitnessedgoldenrun/trace, failurestates иseparatebackendcounts; не выдатьsavedrunзаcurrentlive.',
  'W1-01-F23 W1-01-F24 W1-06-F13 W2-06-F09 W2-06-F10 W2-06-F11 K010 E018',
  'W1-06-Q06')
q(25,'Actual output heads, NMS/quantization и return/postprocess budget','P0 / послеgolden',
  'Tritonbinary/ensembledocsдаютпример,неLinQ. Сценарий[1,84,8400]FP32=2822400B/frame противboundedpacked2404Bиз100detections. NMS/capменяютquality.',
  'Не получены actualserializedresponse/names/shapes/dtypes/scales/layout/headsemantics/classmap/coordinates/truncation/resultretention. JSONwirebytesне numel×dtype.',
  'Rawreturnможетдоминировать downlink/CPU/RAM; supportedremoteNMSилиalreadycompactAPIменяетplacement. Не делатьNMSдважды/неcastdtypeсамовольно.',
  'Model/artifact/schema+E008. Goldenreferenceparity, crowded/empty/invalid/oversizecaps; measureactualwire/poll/fetch/postprocess иfullcycle.',
  'W2-01-F08 W2-01-F09 W2-01-F14 W2-01-F15 W2-01-F16 K006 E008',
  'W2-01-Q03')

e(1,'Issued capability inventory и real LinQ golden path',
  'Выбрать supported access mode и доказать ровно один фактический inference нашей версии модели на LinQ.',
  'Полный кейс, именной разрешённый grant/manual/schema, golden positive/negative inputs, model/preprocess reference и accepted execution witness; read-only host inventory только если shell предоставлен.',
  'Разделить model/control/data/lifecycle; зафиксировать custom model upload/update/select; выполнить один documented request, получить machine-readable output и terminal/release evidence; узнать hidden retries, quotas, source reachability и разрешённый restart. Если lifecycle непрозрачен, сохранить UNKNOWN и bounded stop.',
  'Manual revision, hashes model/input/output/config, redacted request/result/job/run IDs, actual backend/device witness, OS/ISA/CPU/codec/permissions; measured local roundtrip отдельно от reported server durations.',
  'Callable custom service достаточен без SSH. Нет usable outputs/приемлемого cycle → unsupported-live/offline route и точный missing-grant packet. Не заменять LinQ GPU fallback.',
  'Один golden run не capacity, fairness, p99, TTL, качество всех классов или sustained realtime.',
  'Q001 Q002 Q003 Q025 K001 K010 W1-01-F05 W2-01-F13 W2-06-F09',
  'W1-01-E01 W2-01-E02')
e(2,'RTSP continuous reader, overload, failure и soak',
  'Выбрать PyAV/знакомый GStreamer, TCP/UDP, watchdog/reconnect и bounded latest-frame policy.',
  'Pinned MediaMTX1.21.2, actual FFmpeg build, H264/H265720p/1080p25/30 samples с visible frame/clock/loop ID; source hashes, ffprobe JSON и GOP. Изолированный own test route.',
  'Loop publisher с -re -stream_loop -1 -c copy; сравнить naive sleep/read, continuous decode/latest и bounded raw queues. Медленный consumer200ms при source25fps; 2–3 источника, один stalls. Publisher/server disconnect, media-only blackhole/control alive, EOF/native hang; tcp-timestamp true/false при drift/burst.10min correctness затем2h/ночь по доступности.',
  'Watermark p50/p95/p99 age, input/decode/selected/applied FPS, RSS trend, decode errors, resets/reconnect reasons, fresh recovery time, queue drops, unaffected camera service; configs/versions/CSV/state trace/UI recording.',
  'Выбрать режим по freshness/CPU/RSS и bounded recovery, config/auth errors выделить. Неуспех isolation→исправить ownership/watchdog либо другой проверенный backend.',
  'Loop не live industrial camera; soak не LinQ throughput, качество событий или многосуточный production SLA.',
  'Q004 Q020 W1-02-F02 W1-02-F28 W1-04-F06',
  'W1-02-E01 W1-04-E03')
e(3,'Decode-only и полная цена model input: CPU/NVDEC/QuickSync',
  'Выбрать decode backend/threads/resize placement и actual admitted camera count.',
  'Actual CPU/GPU/SKU/VRAM/OS/driver/power/cooling, pinned ffmpeg/PyAV/native library build; одинаковый H264/H265720/1080p corpus, profiles8/10bit420, GOP/B-frames. Publisher transcode не конкурирует заCPU.',
  'Warmup и≥3 repeats; isolated throughput без -re, затем paced1/2/4/8streams. Software1/default/2/4decoder threads; GPU path с проверенным hardware use/fallback disabled. Decode-only, download, GPU resize-before-download, color/letterbox и input packing измерять отдельно. QSV только после runtime/driver inventory.',
  'CPU-seconds/frame и busy-core equivalents, wall frames/s, GPU video clocks/decode/memory, bytes copied, RSS/VRAM, p95 age при paced load; commands/buildconf/corpus hashes/raw measurements.',
  'Admit только sustained profile с reserve и agreed FPS/age; hardware capability без working build не pass. Оставить программный decode при отсутствии проверенного acceleration.',
  'Чужой903fps не наша4070, isolated max не RTSP reliability, LinQ inference или500camera proof.',
  'Q006 Q022 W1-02-F21 W1-02-F25 W2-06-F01',
  'W1-02-E02')
e(4,'RGB compression, resize, ROI и sampling quality',
  'Определить допустимые payload/view/source profiles без скрытой потери мелких нарушений.',
  'Размеченные целевые RGB PPE/zone scenes, разные размеры/свет/толпа, fixed model/threshold/preprocess. Baseline decoded source уже может быть lossy. Полный кейс задаёт допустимую quality loss.',
  'Paired JPEG Q95/85/75/60/50 с fixed encoder/chroma, отдельно resize grid. Crop original vs crop recompressed frame; crowd r и bounded ROI fanout, full-frame discovery cost. Сравнить25fps→select5fps, NONKEY, source-native5fps, GOP25/50/100/B0 и gaps. Сузить grid после finding.',
  'Bytes distribution mean/p95/p99/max, encode/decode CPU, class/size recall/AP, event missed/false alarms, short-act loss, source delta/coverage, geometry parity; paired predictions, examples и hashes.',
  'Profile допускается по согласованным class/event thresholds. Fail→повысить detail/изменить placement или честно ограничить сценарий; не замещать падение recall стабильной precision.',
  'FLIR/COCO Q thresholds не PPE; каска не сигарета, Q100 не lossless, снижение CPU не качество inference на LinQ.',
  'Q005 Q008 Q009 W1-03-F11 W1-03-F12 W1-03-F16',
  'W1-02-E03 W1-03-E02 W1-06-E02')
e(5,'Paced saturation, fairness, cascade и полный resource budget',
  'Выбрать C/B/p_i, admitted cameras и размещение по per-camera freshness/gaps, не aggregate throughput.',
  'Source corpus+required FPS/maxgap/age, actual topology/goodput, granted quota; сначала tagged dummy delay route, затем real LinQ. Decoder/record/view/replay/backup ownership counters.',
  'B1,C1/2/4/8/16 до разрешённого knee, затем supported batches. Constant offered pacing, step overload/recovery, fast/slow/stalled/crowded source, q0..qmax ROI; p1 vs2/3 при fullcycle50/160/200/300/500ms synthetic fixture. Empty view→3×4tiles→slow/hidden→replay+backup.50/500 только при стенде/правах, иначе symbolic extrapolation.',
  'Every camera admitted/completed/fresh ordered applied FPS, max media/wall gaps, age quantiles с full denominator, drop reasons, byte/count caps, remote held/unknown, post CPU. FD/handles/processes/threads/sockets/contexts/surfaces/pools/RSS/PSS/VRAM, NIC↑↓, disk Bps/IOPS/latency, WAL/replay/backup; raw traces/configs/hashes.',
  'Pass — одновременно agreed per-camera coverage/age, app/resource caps и measured reserve. Knee безfresh throughput→не наращивать C. Reduce admission/profile/viewers/placement только с quality gate. Camera reduction не лечит p1 single-camera ceiling.',
  'Mock L не LinQ prediction; Little-law means не tails; one-stream peak и synthetic500 не500 real cameras/general quality.',
  'Q006 Q007 Q009 Q022 K005 K006 W2-04-F09 W2-04-F11 W2-06-F02',
  'W1-01-E02 W1-03-E01 W1-03-E03 W1-06-E01 W1-06-E06 W2-04-E03 W2-06-E01')
e(6,'Ordering/epochs, fixed-dt tracker, valid empty и domain gaps',
  'Проверить temporal contract, p>1 reorder и допустимость выбранного ID-dependent метода.',
  'Pinned ByteTrack reference при необходимости, отдельный compatible environment; actual method minFPS/maxgap/ID rules, boxes+empty(0,5), source PTS0,.2,.4 vs0,.2,2.4; annotated PPE episodes.',
  'Sparse sent100/105/110; ответы110→105→timeout100→late100, duplicate105, epochE1→E2, timeout wakeup безreply. Compare no-call, real empty, synthetic empty (negative control), new instance/tracking_generation; strict lost > boundary и reactivation-before-expiry. Equalmean uniform/burst/drop/2sgap/reconnect traces; ID quality отдельно от contract.',
  'Append-only sent/arrival/apply/gap/reset/reject/remote-credit trace, KF covariance/framecounter/lost/removed, globalID scope, queue bytes, source deltas и coverage, event recall/false alarms/fragmentation и ID metrics; versions/input hashes.',
  '0old epoch/out-of-order apply, no unsent101 wait, один live outcome/request, Gap не negative и не remote release. Cadence violation→explicit reset/unknown; чрезмерные resets→degraded/unsupported method. Variable-dt adaptation требует своего quality validation.',
  'Correct wrapper trace не качество ID/re-ID; timestamps/frame_rate constructor не variable dt; mock ordering не LinQ lifecycle.',
  'Q005 Q007 Q021 K005 W2-04-F02 W2-04-F04 W2-04-F12 W2-04-F13',
  'W1-03-E04 W1-04-E01 W2-04-E01 W2-04-E02 W2-04-E04')
e(7,'Persisted remote ledger: fake-job fault/restart fixture',
  'Доказать наши reservation/release invariants и honest STOPPED без достаточного external contract.',
  'Собственный fake service, durable DB, deterministic virtual clock/service active-job log. idempotent_submit on/off, visibility/keyretention/TTL cases; K_remote2/local submit1/control1 — fixture, не LinQ.',
  'Crash до/после intent commit/send/accept/ack/jobID persist; lostack, sameUUID/differenthash, hiddenretry как2jobs, cancel200 continuing work, status404/unknown enum, epoch/live timeout, restart с2held, terminal duplicate, DB ack/release commiterror. Отдельно lateacceptance после предполагаемогоTTL.',
  'Ordered intent/send/accept/ack/poll/terminal/release trace, row snapshots/hash/job IDs, service active IDs, held/local slots/bytes, double releases, stale applies, fixture revision/seed.',
  '0≤held≤2, каждый возможно active job покрыт reservation, terminal release ровно один. Нет dedup/full TTL/acceptance cutoff→bounded STOPPED; unknown не исчезает после restart. Fail→учесть retries/ownership/atomicity, не разрешить свежие submits радиprogress.',
  'Virtual duration не runtime latency; fixture не подтверждает LinQ contract, DB power durability или general reliability.',
  'Q002 K001 W2-01-F10 W2-01-F11 W2-01-F12 W2-01-F13',
  'W1-01-E04 W1-06-E03 W2-01-E01')
e(8,'Output schema, numerical parity, NMS placement и return path',
  'Выбрать raw/compact return и postprocess placement, реальные downlink/CPU/RAM coefficients.',
  'Actual serialized result+all head schemas/scales/classmaps, reference model/preprocess/thresholds/quantization; remote wrapper только при grant. Labelled crowded/empty target sample.',
  'Сверить body bytes сshape/dtype/batch mapping, endian/layout, head decode/NMS/coordinate transforms. Rawreference vs compact parity в объявленной tolerance; empty/max/invalidshape/oversize/truncation. Измерить polls/status/fetch/postprocess вместе сactual path, не переменитьdtypeнаугад.',
  'Mean/p95/max wire bytes/output, poll QPS/bytes/visibility delay, fetch/post CPU durations local clocks, peak live buffers/RSS, fullcycle/fresh FPS, paired detections/quality/cap misses; schema/reference hashes.',
  'Parity и bounds→зафиксировать output/postprocess revision и directional50/500 variables. Raw доминирует→remote compact при разрешении; unavailable→admission/architecture cut. AlreadyNMS output не NMS повторно.',
  'Oneframe CPU не500capacity; postprocess parity не обязательное execution proof LinQ; scenario[1,84,8400] не actual chosen model.',
  'Q025 Q003 Q007 K006 W2-01-F14 W2-01-F15 W2-01-F16',
  'W2-01-E03')
e(9,'Early event→original mapping proof: same-demux indexed remux',
  'Допустить exact evidence route или немедленно выбрать snapshot cut.',
  'MediaMTX1.21.2/PyAV16.0.1 сactual libav build, H264video-onlyB0/B2, GOP1/10s/VFR, burnt frame/loop/clock IDs, sample hashes. Собственный prospective indexed remux +native archive comparator.',
  'Index original packet pts/dts/rationaltb/codec/extradata/randomaccess ДО mux rebase; отдельный packetref/lifetime дляdecode. Сопоставить yieldedframe PTS/decodedwatermark сclosed independently decoded originals иactual requested coverage. Decoder-only/recorder-onlyrestart, reset/continuousloop, backwardPTSvsreorder, known-domainwrap, missing/duplicatePTS, UTCjump, main/subnegative.',
  'Packet/frame/sample trace, original/outputtime_base+offsets, distinct source/decoder/recordergenerations, mtxi, manifests/hashes, wrongoriginal/loop count, internal holes, maxgriderror/mappinguncertainty,0falsecomplete.',
  'Pass только testedlineage/profile. Fail→snapshot analyzed frame иarchive mappingunknown; customrecorderoff, одинrecorderroute. Еслиexactclipобязателен—blocker. Не заменятьfailure сравниваниемfilenameUTC.',
  'Нет гарантии arbitrarycodec/camera/RTCP/main-sub/powerloss/LinQ или45чfeasibility. Packet timestamp presence само по себе не mapping.',
  'Q010 K002 W2-02-F03 W2-02-F05 W2-02-F09',
  'W1-05-E01 W2-02-E01')
e(10,'Finite evidence windows, pins, low-space и recorder crash',
  'Проверить finite count/bytes/lifetime с honest partial/unavailable вместо бесконечного ongoing job.',
  'Test ring/DB/media volume, measured GOP/maxbitrate, proposed H40/P5/Q5/L20/C4/J30s/chunk10s/rollover60s/finite incidentquota — fixturevalues. Clock/mapping proof E009 prerequisite дляcomplete.',
  'Fake result delay1/19/21/120s, longdwell/30min ongoingmedia, stalledpostroll/noIDR, duplicate events/manualholdexpiry/deadworker; concurrentretention/export/lowdisk. Kill наcreate-beforeinit/partwrite/close/index/hash/publish; recovery scan, validateprefixderivative, pinrebuild доdeletion. Futurepinintent иreservedbytes должныpersist.',
  'Requested/actual intervals/gaps/generation/hash, jobstate/deadline/reasons, reserved/unique retainedbytes, pins/refcounts/owners, openpart/GOPreserve, rejected extensions, terminaljobage иvisibleeventrevisions.',
  '0falsecomplete; lostpre-roll/latemapping→partial/unavailable. Всеjobsterminal≤J+boundeddispatchjitter; metadataincidentпродолжается послеevidencecap. Lowspace не удаляетpinnedмолча. Snapshotcacheтожеbounded.',
  'Finite local policy не remote queueSLA/quality; processkill не power/diskloss. Нельзя вывести число камер только изH40s.',
  'Q010 Q011 Q012 K003 W2-02-F10 W2-02-F11 W2-02-F12',
  'W1-05-E02 W2-02-E02 W2-02-E03')
e(11,'Processed WS renderer: slow/hidden/fanout/ACK/lifetime',
  'Проверить own-frame correspondence и приложение с1outstanding/viewer безотставания/накопления.',
  'Pinned Python/websockets17.0.1 иbrowser/OS, generatedJPEG+bigframeID+ownbox, nearcapsprofile;3viewersfast/decode3s/hidden60s. Tinyrawpool/checksums/8boundedrequests дляlifetimefixture.',
  'Producer10fps; ACKoff, mainthreadstall/hide/reconnect, oldimage доcloseevent, wrong/future/duplicate/nonce ACK, earlyACKduringSENDING, sourceepochresetduringdecode. Проверятьbusyдоawait, exactkey, creditbeforeSend, bitmap.close/finally; localcredit-cycleelapsedпередdraw. Oversizeheader/JPEG/boxes/dimensions/DPR; reconnectне создаётновыеdecodersдоcleanup.',
  'State/key/send/draw/ACK/bytestrace, checksumframe/box, retainedviewvsborrowedinput, localdecode/drawdurations, latest/outstanding/closingcount, browserheap/processRSS/FD/bitmap lifecycle, UIcapture иdrop/rejectreasons.',
  'Connectionoutstanding≤1, page decode≤1 acrossgenerations, no mismatch/oldgenerationdraw/extra credit; fastviewerне ждётslow. Timeoutterminal→close, nonewcredit; historyresync отдельно. MaliciousACKпослеreceive можетлгатьоdraw—зафиксироватьlimitation.',
  'App-ownedrefbound не totalRSS/kernel/browser limit, canvasdrawACK неphysicalscanout/operatorread; mock неLinQborrowrelease.',
  'Q013 Q002 K004 W2-03-F05 W2-03-F06 W2-03-F07 W2-03-F08 W2-03-F09',
  'W1-04-E05 W1-05-E04 W2-03-E01 W2-03-E03 W2-03-E04')
e(12,'Blocked transport, public close и bounded cleanup',
  'Выбрать приемлемый public-only WSroute либо E-testedmitigation без hardteardownобещания.',
  'ExactOS/TLS/proxy/Python/websocketsstack, peerstopreads, rate≪B/deadline/lossblackhole иlargevalidpayload; ownisolatedroute.',
  'send→deadline→CLOSING→publicclose приrepeatedconnectattempts. Неcancel/sendagainвтомжеconnection. Active+closingcountsсохранятьдоcleanup; finite caprejectsnew. Отдельно experimental create_connection/subclass сохранённого transport→documentedasyncioabort; неpublicwebsocketsAPI.',
  'Taskdumps/send/closeelapsed, closingage/count, transportbuffersгдедоступны, socketFD/handlesbeforeafter, memorytrends/cleanupreasons; сравнитьTLS/proxy yes/no.',
  'Нет unboundednewresources/sendtasks, timeoutненовыйcredit. Зависшийteardown—failurepublic-onlyroute: visibleunavailable/admissionstop, затемпровереннаяmitigation. Closingнеудалятьизbudgetпотаймеру.',
  'ОднаOSне universalTCP/kernelrelease, sourcecode/close_timeoutнеhardwallcap. ExperimentalabortнеguaranteednativebrowserRSSrelease.',
  'Q013 K004 W2-03-F03 W2-03-F06 W2-03-F07',
  'W2-03-E02')
e(13,'Optional native WebRTC/LL-HLS и browser mapping',
  'Разрешитьoriginalliveиопределитьусловияoverlay; optionalпослеprocessedcore.',
  'Same-versionMediaMTXserver/reader, codec/profile/GOP, exactbrowser/OS, actualnetwork/cert/domain/TURNpermission. FrameID/watermarkcorpus.',
  'LAN/hotspot/NAT/UDPblocked/HTTPSproxy/subpath/TURNTCP. ПроверитьOPTIONS/POST201Location/PATCH/DELETE/Link/CORS, selectedcandidatepair, H264B0/H265negative. rVFCfieldavailability/sourcePTS→RTPSSRCepoch mappingиgeometryDPR; overlaydisabledприunknown.',
  'Time-to-first-frame, glass-to-glassp50/p95 сmeasurementquantization, bitrate/CPU/RSS30–60min,reconnect, skew/no-match/stalecount, packet/metadata/UIrecording.',
  'Нетmedia/codecroute→processedviewиличестныйHTTPfallbackсdelay. Exactoverlayтолькоприevidencebound; originalnativeможетжитьбезаналитики.',
  'HTTP200/STUN/TURNdocsнеactualconnectivity;600mspartmathнеbenchmark, домашнийтестнеплощадка, rVFCнеcameraIDguarantee.',
  'Q014 W1-05-F10 W1-05-F13 W1-05-F18 W1-05-F19',
  'W1-05-E03')
e(14,'Event/outbox durability, replay и optional notifier',
  'Проверитьno lost committedincidents иdocumentedpossibleduplicates, выбранныйdeliveryendpoint.',
  'OwnDB/fakereceiver сdurableinbox/idempotencyon/off,429retry_after/500/timeout-beforeafteraccept, eventgeneratorпоrequiredrate, disconnectedUI/historycursor.',
  'Kill доcommit/послеcommitдосend/послеacceptдомarker; broker/provideroffline, poisonpayload, leaseexpiry/fencing. Replayvalid/expiredcursor/snapshotresync. Rateoverall/perrecipient, retriesbackoffjitter bounded. Реальныйbot/chat/clip/privatelinkтолькоотдельноавторизованныйtestпослеcredentials.',
  'Uniqueevent_id/revision/outboxkey, operationcommitIDs/attempts/externalID, pendingoldestage/count, commitp95/WALgrowth, receiverduplicateeffects, provideraccept/browserdraw/operatorackраздельно.',
  'Committedeventиoutboxsurviveprocesscrashвdeclaredstorageconditions; optionalreceiverinboxпредотвращаетduplicateDBeffect. Безprovideridempotency duplicateвозможен/видим. Newbroker/DBтолькопослеmeasuredneed.',
  'FakesuccessнеTelegram/MAXaccess/latency, providerMessageнеreadreceipt, MQTTQoS/Kafkatransactionнеexternalexactlyonce/powerdurability.',
  'Q017 Q018 W1-04-F25 W1-05-F23 W1-05-F24 W1-05-F25',
  'W1-04-E02 W1-04-E04 W1-05-E05 W1-05-E06')
e(15,'Artifact/runtime/offline/Astra/security gate',
  'Зафиксироватьactualcoherentbundleиверифицироватьровноtargetконфигурацию.',
  'РазрешённыйcleantargetOS/ISA/glibc/driver, preparedartifacts/hashes/licenses/model/staticassets; engine/Compose/hostdriversalreadyinstalledилиsupplied. LinQproprietaryenvотдельно.',
  'Verifyofflinehashes; inventoryCPython/av.library_versions/library_meta/websockets/actualPythonSQLitesource_id+compile_options+PRAGMA. RejectunpatchedWALruntimeлибоdocumentvendorbackport. Loadallimages/up--no-build--pullnever; noCDN/pip/apt/modeldownloads. Поочередноweb/volume/decode/LinQgolden/fullslice/restore. Astraedition/kernel/policy/device/rootlessтольковapprovedconfig. AuthUI/API/clip/streamroles, invalidTLS/token, log/frontendsecretredaction.',
  'Finalartifact/lockmanifest, exactplatform/buildflags/native/transitivenotices/hashes, imageIDs/digests, sourceID/PRAGMAreturns, startupnetworklogsredacted, sample→eventtrace, accessdecisions/flowtable.',
  '0missingmandatoryimports/ABI, патчSQLiteдоказан, ownofflineclientнеfetchpackages. Fail→suppliedenv/isolatedworker/remoteAPIилиscope cut; не менятьsharednativeSDKиmandataryprotection.',
  'Manifest≠installed, sourcepin≠binary; offlineimagesнеLinQofflineservice, UIcontainerнаAstraнесертификация/devicecompatibility; functionalchecksнеpentest/IECcompliance.',
  'Q015 Q016 Q019 K007 W2-05-F01 W2-05-F02 W2-05-F03 W2-05-F04 W2-05-F06',
  'W1-01-E03 W1-01-E05 W1-01-E06 W2-05-E01')
e(16,'SQLite commit/fault, supported backup/restore и remote reconciliation',
  'Проверитьграницыacknowledgedcommit, verifiedbackupиsafeadmissionпослеrestore.',
  'OwnisolatedDBсexactpatchedruntime/localFS, event/outbox/ledger/pins/mediafixture, disposableboundedvolume; externallydurablewitnessдляpowerclasses. Необщийдиск/стенд.',
  'ProcesskillbeforeafterBEGIN/write/COMMIT/response, BUSY/IOERR/diskfull, frozenlongreader/WALcheckpoint. Connection.backupвmaintenancewindow+closedimmutablemediainventory/holds/hash, verifydestinationintegrity_check+foreign_key_check. Создатьpost-cutoffremoteobligations, restoreвновыйкаталог, fenceoldowners/newboot, mediaorphan/missing/tailvalidation/rebuildpinsдоretention, reconcileknownunknownjobs. Reboot/forcedOS/powercut/disklossтестироватьотдельноиразрешённо.',
  'CommitoperationIDs/recoveredrows, WAL/journalpreserved, errors/queue/durations, backupcutoff/schema/runtime/hashes, missing/orphan/partialstatus, refcounts/reservations/heldbeforeafter, failedbackuppublication, measuredRPO/RTO/faultwitness.',
  'Ниодногоsuccessбезrecoveredcommitвdeclaredprocesscrashscope; noeventwithoutoutbox; failedbackupнеpublished; nofalsecomplete/deletionbeforepinrebuild; postcutoffunknownнеfreecredit. Noreliableproviderreconcile→admissionSTOPPED. FULLfilepublishrequiresactualFSrecipe.',
  'Processkillнеpower/diskloss, integrity_checkнеFK/media/remoteproof, checksumнеfsync; onebackupнеHA/универсальнаяdurability.',
  'Q002 Q012 Q015 K008 W2-05-F05 W2-05-F07 W2-05-F09 W2-05-F10 W2-05-F11 W2-05-F12',
  'W1-06-E05 W2-05-E02 W2-05-E03 W2-05-E04')
e(17,'Alarm latency с onset/dwell и полным denominator',
  'Проверить agreed event-to-operatorboundиотделитьегоотcompute/video latency.',
  'Размеченный/controlledphysicalonset, temporaldwellcontract, pacedsource/actualLinQ/view/storage, externalhigh-fpsopticalrecordingsource+displayилидоказаннаяclocksyncсerrorbound.',
  'Phase sweepотносительноsampler;1cameraзатемadmittedload. ДлякаждогоplannedepisodeIDисохранятьphysicalonset/firstqualifyingframe/ruleeligible/eventcommitted/deliverydraw/optionaloperatorack. Cold/steady/reconnectиmiss/timeout/sessionendpendingнеисключать.',
  'Rawsame-hostmonotonicdurations+domain, UTCmappinguncertainty, e2eobservationsp50/p95/p99 сn/warmup/load, fractionofferedalertedwithinSLA, missed/censoredcases/downtime; opticalsourcevideoиquantizationbound.',
  'Толькоe2etracesдаютtotalquantiles; stagesнеp95sum, summariesworkersнеaveragep95. При>1%timeoutsнеобещатьunconditionalp99нижеdeadlineпосuccesssubset. Revealshorteventmisses/gaps.',
  'CanvasACKнеphysicalscanout/человекпрочитал, successlatencyнеeventrecall; mock/mediaнеLinQ илидругаясеть.',
  'Q005 Q018 Q022 W1-06-F04 W1-06-F05 W1-06-F06 W1-06-F14 W2-06-F11',
  'W1-06-E04')
e(18,'Integrated minimum/mode go-no-go',
  'Подтвердитьrequiredverticalsliceисделатьконкретныйscope cut; неоценивать45чпооценкеpersonhours.',
  'Issuedgrant/fullcase/goldenmodel/input/reference/witness, selectedactualbundle, commonpositive/empty/error/late/oldgenerationfixtures.',
  'RealLinQrun→1source→ownframeview→eventcommit/history→snapshot/clipstatus;2camera isolation. Raw/compactparity, ambiguoussubmit/restart, gaps/order/epoch, earlyE009либоsnapshotcut, slowviewer/DBfailure/backuprestore/clean-target. Gate0–2/2–6/6–18/18–32/32–40/40–45чизW2_06какплан.',
  'Tracepacket source/frame→request/model→LinQrun→result→eventrevision→evidencecoverage→draw/ACK; ledger/pinsbeforeafterrestart, versions/hashes, plannedoutcomes/quality/FPS/gap/age иvisiblefailurestates.',
  'PassтолькореальныйLinQ+fullcase-requiredroute/temporal/persistencecontracts. Нетusableautomatedresult/cycle→unsupported-live. Exactcliprequiredиmappingfail→blocker, иначеapprovedsnapshotcut. Optionalnative/messenger/blur/broker/extra camerasпослеcore.',
  'Mockнеpass,2cameraне50/500capacity/industrialquality, savedwitnessedreplayнеcurrentliveиproposalнеproven45чfeasibility.',
  'Q001 Q005 Q007 Q010 Q024 K010 W2-06-F09 W2-06-F10 W2-06-F11 W2-06-F12',
  'W2-06-E03')
e(19,'Camera-health positive/negative controls',
  'Оставитьmandatoryprogress/ageилидопуститьограниченныеsuspectedimagesignals.',
  'Annotatedday/night/static/detailpoor/machinerycorpus, knownonset/hash/baseline/ROI; повторpixelsсnewPTSиповторPTSсnewpixels, loopcontinuous/reset, corrupt/black/white/blur/shift.',
  'Поодномуфактору иcontrols lights-off/IRswitch/whitewall/truck/legitimatePTZ; restore/relearn/suitability. Transportblackholeприcontrolaliveотдельно. Сигналынаboundeddownsample/rate, thresholdconfigversion.',
  'Signal/delaytimeline, falsealarms/camera-hour/scene, recovery/hysteresis/CPUbudget, confusiontable/source/config/UIstatusproof.',
  'Mandatory: noprogress→staleвconfiguredwatchdog+tolerance; framesaliveнеanalysishealthy. Optional: acceptedfalsealarm/delayнаэтойвыборке, unsuitable→unknown/suspected, unseparablecontrols→cut.',
  'Syntheticdistortionнеrealworldtamperproof, imageanomalyнеcausalintent/качествораспознаванияСИЗ, универсальныхthresholdsнет.',
  'Q023 K009 W2-06-F06 W2-06-F07 W2-06-F08',
  'W2-06-E02')

# Clear prose for the dense technical procedures; original full fixtures remain at their locators.
def polish_q(n,values):
    rec=Q[n-1]
    for key,value in zip(['known','why','decision','closure'],values):rec[key]=value
polish_q(19,[
 'Axis/NIST/Docker дают scoped examples: HTTPS управления не encrypted RTSP; Digest не encryption; VLAN/firewall требуют flow inventory; auth проверяется у clip/stream endpoints; Compose secrets не encrypted vault.',
 'Неизвестны camera firmware/client TLS/SRTP/RTSPS/accounts, remote tenant isolation/upload retention/logging/delete policy, keys/permissions и approved routes.',
 'Camera credentials только у нужного owner; browser получает authenticated application path. Remote decode/recording выбираются вместе с privacy/persistence policy и bandwidth.',
 'Device/vendor/remote owner + E015 functional security checks: exact flow table, invalid-cert failures, viewer/operator/admin и secret redaction; право/КИИ → market_deployment.'
])
polish_q(20,[
 'Version-specific FFmpeg/GStreamer/PyAV/OpenCV параметры и negative cases сохранены. rtspsrc tcp-timestamp обходит drift, но burst source создаёт иной риск; timeout не bound frame age.',
 'Нет2h/overnight paced run actual source/backend, control-alive-no-media, native hang cleanup и true/false tcp-timestamp comparison.',
 'Backend/transport/watchdog выбирается по progress/RSS/watermark; ret=True, PID и socket alive недостаточны.',
 'E002: pinned build/known source, slow consumer, disconnect/restart/media blackhole;10min correctness затем2h/ночь при доступности. Publisher transcode не смешивать с isolated decode.'
])
polish_q(21,[
 'ByteTrack fixed dt1/update, frame_rate только lost buffer; no-call freeze, valid empty(0,5) — observation, public gap/reset нет. New instance+tracking_generation — wrapper proposal; PTS не меняет dt.',
 'Нет tracker smoke/installability/footprint/domain ID metrics или допустимости short-gap carry. Старые np.float/imports и dependencies не tested, cadence/maxgap неизвестны.',
 'Tracker optional по gate; cadence violation→reset/unknown. ID-dependent метод при failed gate — degraded/unsupported, не per-frame замена.',
 'E006 с pinned reference, uniform/burst equal-mean/drop/empty/long-gap traces и separate annotated domain quality. Другая gap-aware реализация/адаптация требует validation.'
])
polish_q(22,[
 'Input/return/view/control/storage сценарии и memory inventory сохранены.500 registered не500 tiles/viewer; RAM включает DPB/surfaces/contexts/pools/borrows/TLS/DB, не один raw slot.',
 'Нет measured WAN↑↓/RTT/jitter/clock offset, FD/ports/sessions/processes/threads/VRAM/IO replay+backup и mcam/Cinf/Cdec/Cpre/Cwrite coefficients.',
 'Нет единственного network X или числа LinQ плат.50 — candidate host после теста,500 — shards/sites roadmap; ресурсы проверяются вместе с per-camera temporal gate.',
 'E003/E005/E008/E011/E016: topology/dataflow по host/direction, actual profile tails; same-host monotonic durations и optical/sync uncertainty для сквозного возраста.'
])
polish_q(23,[
 'Axis product docs разделяют image-health/причину вмешательства и unsuitable scenes. Progress/age mandatory; repeated/black/white/blur/shift — hypotheses suspected_anomaly.',
 'Нет сцен/thresholds/false alarms per camera-hour/CPU cost и day/night/static/detail-poor/legitimate PTZ controls. Overexposure heuristic не заявленная Axis capability.',
 'Availability/staleness допустимы в core; image anomaly только с baseline/config revision/suitability и visible suspected label.',
 'E019 с positive/negative controls; неразделимые controls→cut. Synthetic distortion не real-world tamper proof.'
])
polish_q(24,[
 '45ч — арифметика официального расписания, не guaranteed LinQ uptime. Есть conditional minimum/5 owners/gates/cuts; ни один полный маршрут не запускался. CPU/RTX/replay должны быть marked.',
 'Full case, accepted witness/current grant/required features и реализация не подтверждены;225 person-hours не взаимозаменяемы.',
 'Real LinQ golden выше optional features; GUI/job без usable output/cycle unsupported-live. Snapshot cut не закрывает обязательные exact clips.',
 'Full case/organizer acceptance + E001/E018/checkpoint demo. Сохранить witness/trace, failure states, separate backend counts; saved run не current live.'
])
polish_q(25,[
 'Triton binary/ensemble — пример, не LinQ. Сценарий [1,84,8400]FP32=2822400B/frame против packed2404B для≤100detections; NMS/cap могут менять quality.',
 'Нет actual serialized response/names/shapes/dtypes/scales/layout/head semantics/classmap/coordinates/truncation/result retention. JSON wire bytes не numel×dtype.',
 'Raw return может доминировать downlink/CPU/RAM; supported remote NMS/compact API меняет placement. Не делать NMS дважды и не cast dtype без контракта.',
 'Model artifact/schema + E008: golden reference parity, crowded/empty/invalid/oversize caps, actual wire/poll/fetch/postprocess/full cycle.'
])
def polish_exp(n,values):
    rec=E[n-1]
    for key,value in zip(['decision','inputs','steps','metrics','outcomes','limit'],values):rec[key]=value
polish_exp(9,[
 'Допустить exact event→original route либо сразу выбрать snapshot cut.',
 'Pinned MediaMTX1.21.2/PyAV16.0.1 с actual libav build; H264 video-only B0/B2, GOP1/10s, VFR, visible frame/loop/clock IDs и hashes. Собственный same-demux indexed remux и native archive для сравнения.',
 'Индексировать packet PTS/DTS/rational time_base/codec/random-access ДО mutable mux rebase; отдельные refs/lifetime для decode. Сопоставить yielded frame с independently decoded closed original. Inject decoder-only/recorder-only restart, reset/continuous loop, backward PTS vs reorder, известный wrap, missing/duplicate PTS, UTC jump и main/sub negative controls.',
 'Packet/frame/output sample trace, distinct source/decoder/recorder generations, original/output time_base и offsets, mtxi/manifest/hashes; wrong-original/loop, внутренние gaps, max grid error и mapping uncertainty.',
 '0 false complete; любое неоднозначное соответствие unknown/partial. Fail→analyzed snapshot, native archive mapping unknown и custom recorder off. Если exact clips обязательны, это blocker; имя файла UTC не обход.',
 'Один fixture не arbitrary camera/codec/RTCP/main-sub/power-loss/LinQ и не доказанная45ч feasibility. Наличие PTS само по себе не lineage proof.'
])
polish_exp(10,[
 'Проверить конечные count/bytes/lifetime и honest partial/unavailable.',
 'Own ring/DB/media test volume, измеренный GOP/max bitrate, E009 для complete. H40/P5/Q5/L20/C4/J30s, chunk10s/rollover60s/finite incident quota — только fixture.',
 'Результаты с delay1/19/21/120s, long dwell/30min ongoing media, stalled post-roll/no IDR, duplicate event/manual expiry/dead worker; concurrent retention/export/low-space. Kill create-before-init/part-write/close/index/hash/publish. Scan/reconcile, validated prefix derivative, future pin intent и reserved bytes на диске, pin rebuild до deletion.',
 'Requested/actual intervals/gaps/generations/hashes; transition/deadline reasons; reservations/unique retained bytes, owner pins/refcounts, GOP/open-part reserve, oldest job и event revisions.',
 '0 false complete; late/lost coverage→partial/unavailable. Каждый job terminal≤J+bounded dispatch jitter, metadata incident продолжается после evidence quota. Low-space не удаляет pinned молча; snapshot тоже bounded.',
 'Finite local policy не remote queue SLA/recall; process kill не power/disk loss; H40s не универсальная глубина и не число камер.'
])
polish_exp(11,[
 'Проверить same-frame renderer и1outstanding/viewer через slow/hidden/reconnect.',
 'Exact pinned Python/websockets/browser/OS; JPEG с крупным frame ID и own boxes, near-cap profile;3viewers fast/decode3s/hidden60s. Tiny raw pool/checksums/8bounded requests для lifetime.',
 'Producer10fps, ACK off, main-thread stall/hide/reconnect, старый image до close event, wrong/future/duplicate nonce ACK и early ACK в SENDING. Busy выставляется до await; credit до send; bitmap.close/finally; elapsed credit-cycle check перед draw. Source reset во время decode, oversize header/JPEG/boxes/dimensions/DPR и reconnect до cleanup.',
 'State/key/send/draw/ACK trace, checksum frame/box, retained-view vs borrowed-input counters, latest/outstanding/closing counts, bitmap lifecycle, heap/process RSS/FD, UI capture и drop reasons.',
 'Outstanding≤1/connection, decode≤1/page через поколения, no old-generation draw/mismatch/extra credit; fast viewer не ждёт slow. Timeout terminal, не новый credit. Malicious ACK после receive может лгать о draw — зафиксировать ограничение.',
 'App-owned reference bounds не total RSS/kernel/browser cap; canvas ACK не physical scanout/operator read; mock не LinQ safe input release.'
])
polish_exp(12,[
 'Оценить public-only close и выбрать проверенную mitigation при failure.',
 'Own isolated exact OS/TLS/proxy/Python/websockets route; peer stops reads, rate≪B/deadline, loss/blackhole, large valid payload.',
 'Send→deadline→CLOSING→public close с repeated connection attempts. Не cancel/send-again в том же connection. Active+closing остаются в finite admission cap. Отдельная experimental ветка create_connection/subclass сохраняет asyncio transport и вызывает documented abort; это не public websockets API.',
 'Task dumps, send/close elapsed, closing age/count, transport buffers где доступны, socket FD/handles before/after, memory trends и cleanup logs; TLS/proxy yes/no.',
 'Нет новых send/resources сверх cap после timeout. Hanging teardown — failure public-only route; visible unavailable/admission stop и затем E-tested mitigation. Не вычёркивать closing из budget по таймеру.',
 'Одна OS не universal TCP/kernel release; source read/close_timeout не hard wall cap; abort не гарантия browser/native RSS release.'
])
polish_exp(13,[
 'Допустить optional original live и установить условия overlay.',
 'Same-version MediaMTX server/reader, actual codec/GOP/browser/OS, network/cert/domain/TURN grant, watermark/frame ID corpus.',
 'LAN/hotspot/NAT/UDP blocked/HTTPS proxy/subpath/TURN TCP. Проверить OPTIONS/POST201 Location/PATCH/DELETE/Link/CORS, selected candidate pair, H264 B0/H265 negative; rVFC fields/source PTS→RTP/SSRC/epoch mapping, viewport/DPR. Overlay disabled при unknown mapping.',
 'Time-to-first-frame, glass-to-glass p50/p95 с quantization, bitrate/CPU/RSS30–60min, reconnect, skew/no-match/stale и UI/packet metadata.',
 'Нет codec/media route→processed view либо проверенный HTTP fallback с visible delay. Exact overlay только с measured mapping; original live может работать без inference.',
 'HTTP200/STUN docs не media connectivity;600ms part math не benchmark, домашний тест не площадка, rVFC не arbitrary camera ID.'
])
polish_exp(14,[
 'Проверить сохранность committed incidents и честно показать possible duplicates.',
 'Own DB/fake receiver с durable inbox/idempotency on/off,429 retry_after/500/timeout до и после accept, required event rate, disconnected UI/history cursor.',
 'Kill до commit/после commit до send/после accept до marker; provider/broker offline, poison payload, stale lease/fencing. Valid/expired cursor replay/snapshot resync. Overall/per-recipient rates и bounded retry/backoff/jitter. Реальный test bot/chat/clip/link — только отдельно авторизованной практикой.',
 'Unique event_id/revision/outbox keys, commit operation IDs/attempts/external IDs, pending oldest age/count, commit p95/WAL, receiver effects и дубли; provider accept/browser draw/operator ack отдельно.',
 'Committed event/outbox восстанавливаются в заявленном process-crash scope; receiver inbox даёт dedup его DB effects. Без provider idempotency duplicate возможен. Broker/PostgreSQL только после measured need.',
 'Fake не Telegram/MAX access/latency; Message response не read receipt, QoS/Kafka transactions не external exactly-once или power durability.'
])
polish_exp(15,[
 'Зафиксировать фактический bundle и проверить ровно target configuration.',
 'Разрешённый clean target OS/ISA/glibc/driver, artifacts/hashes/licenses/model/static assets, installed/supplied engine/Compose/host drivers. Proprietary LinQ environment отдельно.',
 'Verify hashes offline; inventory CPython/av.library_versions/library_meta/websockets и linked SQLite source_id/compile_options/PRAGMAs именно Python connection. Reject unpatched WAL либо документировать vendor backport. Load images/up--no-build--pull never без CDN/pip/apt/model downloads. Web→volume→decode→LinQ golden→event/view/restore. Astra edition/kernel/policy/device/rootless только approved config; auth roles, invalid TLS/token, log/frontend secret redaction.',
 'Final artifact/lock manifest, platform/build flags/transitive notices/hashes, image IDs/digests, source_id/PRAGMA returns, redacted startup/network logs, sample→event trace и access/flow table.',
 '0 missing mandatory imports/ABI; patched SQLite доказан, own offline client не fetch packages. Fail→supplied environment/isolated worker/remote API/scope cut; не менять shared SDK/mandatory protection наугад.',
 'Source pin не binary/installed; offline images не offline LinQ; UI на Astra не driver support/сертификат; functional security checks не pentest/IEC compliance.'
])
polish_exp(16,[
 'Проверить acknowledged commit, verified backup и safe admission после restore.',
 'Own isolated exact patched SQLite/local FS, event/outbox/ledger/pins/media fixture, disposable bounded volume; externally durable witness для разрешённых power classes, не общий стенд.',
 'Kill before/after BEGIN/write/COMMIT/response; BUSY/IOERR/disk-full/long-reader WAL growth. Connection.backup в maintenance window + immutable media inventory/holds/hash; integrity_check+foreign_key_check. Создать remote obligations после cutoff, restore в новый каталог, fence old owners/new boot, orphan/missing/tail validation и pin rebuild до retention, documented remote reconcile. Reboot/forced OS/power/disk loss отдельно.',
 'Commit IDs/recovered rows, WAL/journal сохранены, errors/queue/durations; backup cutoff/schema/runtime/hashes, missing/orphan/partial statuses, refcounts/reservations/held before/after, failed backup publication, measured RPO/RTO/witness.',
 '0 acknowledged success без recovered commit в declared process-crash scope; no event without outbox, no failed backup published, no false complete/deletion до rebuild. Post-cutoff unknown не free credit; no reliable reconcile→STOPPED. File publish durability требует actual FS recipe.',
 'Process kill не power/disk loss, integrity_check не FK/media/remote proof, checksum не fsync; один backup не HA/универсальная durability.'
])
polish_exp(17,[
 'Измерить agreed event-to-operator endpoint и отделить compute/video latency.',
 'Controlled physical onset/разметка, temporal dwell contract, paced source/actual LinQ/view/recording, optical source+screen запись либо доказанная clock sync с error bound.',
 'Phase sweep sampler,1camera затем admitted load. Каждый planned episode с ID: physical onset/first qualifying frame/rule eligible/committed/delivered-drawn/optional operator ack. Cold/steady/reconnect; misses/timeouts/session-ended pending остаются в denominator.',
 'Raw same-host monotonic durations+clock domain/UTC uncertainty; end-to-end p50/p95/p99 с n/warmup/load, fraction offered alerted within SLA, missed/censored/downtime; optical evidence и quantization bound.',
 'Total quantiles только из e2e traces/совместимых histograms, не сумма stage p95/средний worker p95. При>1% timeouts не обещать unconditional p99 ниже deadline по success subset; показать short-event misses.',
 'Canvas ACK не physical scanout/operator read; success latency не event recall, mock/media test не LinQ или другая сеть.'
])
polish_exp(18,[
 'Проверить required vertical slice и выбрать конкретный scope cut.',
 'Issued grant/full case, golden model/input/reference/accepted witness, actual selected bundle, positive/empty/error/late/old-generation fixtures.',
 'Real LinQ→1source→own-frame view→event commit/history→snapshot/clip status, затем2camera isolation. Raw/compact parity, ambiguous submit/restart, gap/order/epoch, early E009 либо snapshot cut, slow viewer/DB fault/backup-restore/clean target. Gates0–2/2–6/6–18/18–32/32–40/40–45ч — план.',
 'Trace packet source/frame→request/model→LinQ run→result→event revision→evidence coverage→draw/ACK; ledger/pins before/after restart, versions/hashes/planned outcomes, required quality/FPS/gaps/age и visible failure states.',
 'Pass: actual LinQ и full-case required route/temporal/persistence contracts. Нет automated result/cycle→unsupported-live. Exact clips required+mapping fail→blocker; иначе согласованный snapshot cut. Optional native/messenger/blur/broker/extra cameras после core.',
 'Mock не pass;2camera не50/500/industrial proof; saved witnessed replay не current live; proposal не доказанная45ч feasibility.'
])
polish_exp(19,[
 'Оставить progress/age либо допустить ограниченные suspected image signals.',
 'Annotated day/night/static/detail-poor/machinery corpus, known onset/hash/baseline/ROI; repeated pixels/new PTS, repeated PTS/new pixels, loop continuous/reset, corrupt/black/white/blur/shift.',
 'По одному фактору и controls lights-off/IR switch/white wall/truck/legitimate PTZ; restore/relearn/suitability. Отдельно transport blackhole с control alive. Bounded downsample/rate, thresholds/config revision.',
 'Signal/delay timeline, false alarms/camera-hour/scene, recovery/hysteresis/CPU budget, confusion table/source/config/UI statuses.',
 'Mandatory: no progress→stale в watchdog+tolerance; новые frames не analysis healthy. Optional: согласованные false-alarm/delay на этой выборке, unsuitable→unknown/suspected; неразделимые controls→cut.',
 'Synthetic distortion не real-world tamper proof/причина вмешательства/quality PPE; универсальных thresholds нет.'
])

def readable(text):
    # Make Russian/English/unit boundaries explicit; preserve code/IDs/hashes.
    text=re.sub(r'([а-яё])([A-Za-z])',r'\1 \2',text)
    text=re.sub(r'([A-Za-z])([а-яё])',r'\1 \2',text)
    text=re.sub(r'([а-яё])([0-9])',r'\1 \2',text)
    text=re.sub(r'([0-9])([а-яё])',r'\1 \2',text)
    fixes={'поодномуфактору':'по одному фактору','полныйкейс':'полный кейс','выданныйрежим':'выданный режим','неподтверждены':'не подтверждены','неизвестны':'неизвестны','невзаимозаменяемы':'не взаимозаменяемы','45 чпооценке':'45 ч по оценке','собственнойверсии':'собственной версии','неUniversal':'не universal'}
    for a,b in fixes.items():text=text.replace(a,b)
    return text
for rec in Q+E:
    for k,v in list(rec.items()):
        if isinstance(v,str) and k not in ('id','refs'):rec[k]=readable(v)

# Every native Q/E maps to a deduplicated substantive question/experiment.
c.qmap={alias:r['id'] for r in Q for alias in r['aliases']}
c.emap={alias:r['id'] for r in E for alias in r['aliases']}
c.mapping={**c.smap,**c.fmap,**c.qmap,**c.emap}

# Preserve unique additions rather than repeat the entire same-source observation.
for rec in c.facts:
    if rec.get('old',[None])[0] in ['W1-01-F01','W1-01-F02','W1-01-F03','W1-01-F04']:
        rec['body']=re.sub(r'(?<![\w:-])([FQ]\d{3})\b',r'linq_platform:\1',rec['body'])
        rec['title']={
          'W1-01-F01':'Отсутствие issued bundle/device access в соседнем linq_platform; CPU/mock не device run',
          'W1-01-F02':'Условные access modes и разделение host decode vs TPU в linq_platform',
          'W1-01-F03':'Незакрытые issued-access/I-O/quota/recovery вопросы соседнего linq_platform',
          'W1-01-F04':'Корпоративный HPS SLA и вакансии не устанавливают hackathon API/SLA'
        }[rec['old'][0]]
    if rec.get('old')==['W1-06-F02']:
        rec['body']='MEASURED/CLAIM: повторное чтение той же NVDEC13.0 primary таблицы, не независимое измерение. Дополнение к W1-02-F21: показатели на один NVDEC engine, зависят от GPU class/video clock; floor(903/25)=36 — только арифметика, не доказанный лимит камер. RTX4070 VRAM, actual clocks/driver/contexts/copies/CPU остаются UNKNOWN.'
    if rec.get('old')==['W1-04-F12']:
        rec['body']='CODE: тот же latest-frame/barrier pattern, что W1-03-F10, дополнительно прочитан в HEAD e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 (S07). Unique observations: retrieve failure выдаёт zero image и cap.open; умерший thread приводит к StopIteration/закрытию loader. Return sources/images/info не содержит PTS/epoch. Это два snapshots одной implementation chain, не LinQ runtime.'
    if rec.get('old')==['W2-06-F05']:
        rec['body']='INFERENCE: интеграционное подтверждение W2-04-F10, не новый независимый факт. Necessary per-camera f_required_i≤p_i/E[L_i] с full cycle и aggregate occupancy не заменяют remote-held cap/temporal tails. Cinf LinQ/Cdec/Cpre/CPU_post/Kremote и targetFPS/maxgap UNKNOWN. TOPS→N, чужой NVDEC→4070 и225person-hours→feasibility недопустимы.'

def link_ids(text):
    text=c.norm(text)
    def repl(m):
        v=m[0];kind=v[0]
        fn={'S':'SOURCES.md','F':'RAW_FACTS.md','Q':'OPEN_QUESTIONS.md','E':'OPEN_QUESTIONS.md'}.get(kind)
        return f'[{v}]({fn}#{v.lower()})' if fn else v
    return re.sub(r'\b[SFQE]\d{3}\b',repl,text)

def open_questions():
    out=['# Открытые вопросы и программа проверок video_architecture\n',c.PROVENANCE,
      'Все эксперименты ниже **предложены, НЕ выполнены**. Никаких device/application/benchmark/browser/DB fault результатов эта стадия не добавила. Повторные W1/W2 вопросы и fixtures объединены по решению; native aliases и исходные подробности доступны через ID_MAP и worker locators.\n',
      '## Первые часы: порядок закрытия\n',
      '1. **0–2ч:** Q001/Q002/Q003/Q005/Q025; E001 — actual grant, model boundary, accepted witness и один real LinQ golden. GUI/job без usable result/приемлемого cycle → unsupported-live.\n2. **2–6ч:** Q004/Q010/Q015; E009 — early remux mapping gate; E015 — actual patched SQLite/runtime; E018 — source→LinQ→own-frame view→event commit. Если exact clips обязательны, snapshot cut не закрывает требование.\n3. **6–18ч:** Q007/Q013/Q021; E005/E006/E007/E011 — две камеры, full cycle, gaps, held через restart и slow browser.\n4. После slice: E003/E004/E010/E016/E017; optional native video/messenger/image health только после core gates. Эти интервалы — инженерный план, не measured effort/45ч feasibility.\n',
      '## Реестр неизвестного\n']
    for r in Q:
        out += [f'<a id="{r["id"].lower()}"></a>\n',f'### {r["id"]} — {r["title"]}\n',f'**Приоритет:** {r["priority"]}. **Статус:** открыто; proposal/docs/code не runtime closure.\n',f'**Известное / где искали:** {r["known"]}\n',f'**Почему не закрыто:** {r["why"]}\n',f'**Какое решение меняет:** {r["decision"]}\n',f'**Способ закрытия:** {r["closure"]}\n',f'**Связи:** {link_ids(r["refs"])}.\n', '**Происхождение вопросов:** '+', '.join(r['aliases'])+'.\n']
    out.append('## Дискриминирующая программа E\n\nОбщий corpus, trace IDs и fixtures переиспользуются; assertions различны. Программы ниже не предписывают нагрузку/kill/reset общего стенда. Реальные sender tests и disruptive fault tests требуют отдельно предоставленного допуска на собственный testbed. Чтение/арифметика этой исследовательской волны к этим E не относятся.\n')
    for r in E:
        out += [f'<a id="{r["id"].lower()}"></a>\n',f'### {r["id"]} — {r["title"]}\n','**Статус:** PROPOSED / NOT RUN.\n',f'**Решение:** {r["decision"]}\n',f'**Входы / доступ:** {r["inputs"]}\n',f'**Шаги:** {r["steps"]}\n',f'**Метрики / сохраняемые артефакты:** {r["metrics"]}\n',f'**Исходы / действия:** {r["outcomes"]}\n',f'**Чего успех не доказывает:** {r["limit"]}\n',f'**Связи:** {link_ids(r["refs"])}.\n','**Сведённые исходные fixtures:** '+', '.join(r['aliases'])+'. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.\n']
    (c.ROOT/'OPEN_QUESTIONS.md').write_text('\n'.join(out),encoding='utf-8')

def id_map():
    out=['# Стабильные ID и происхождение\n',c.PROVENANCE,
      'Формат точной ссылки: `RAW_FACTS.md#f001`, `SOURCES.md#s001`, `OPEN_QUESTIONS.md#q001`/`#e001`: перед каждой записью есть явный `<a id="…"></a>`. Из _WORK ссылки на итоговые файлы требуют `../`. Native aliases — только provenance, не отдельные доказательства. Диапазон native F может сводиться к одному составному F.\n',
      '## Содержательная дедупликация\n',
      'NVDEC13.0 W1-02-F21/W1-06-F02 — одно primary измерение, unique per-engine caveats объединены. Ultralytics latest/barrier W1-03-F10/W1-04-F12 — одна implementation chain с двумя разными явно сохранёнными snapshots; unique failure semantics добавлены к общему F. W2-06-F05 — интеграционный повтор per-camera gate W2-04-F10, не новая независимая проверка. Остальные F различают документацию, source/version scopes и analytic decisions; W2 уточняет W1, не переписывает историю. Source chains pinned repo+revision и exact document URL объединены. Q/E сведены по substantive decision, а не числу вызовов. Вводные и K-матрицы не объявлены дополнительными F; каталог8проектов выделен отдельно.\n']
    for kind,title in [('S','Источники'),('F','Факты'),('Q','Вопросы'),('E','Эксперименты')]:
        out.append(f'## {title}\n\n| Native ID | Stable ID | Сохранённый локатор |\n|---|---|---|\n')
        for old,new in c.mapping.items():
            if new[0]!=kind:continue
            m=re.match(r'W([12])-(\d{2})-',old)
            name=f'W{m[1]}_{m[2]}' if m else ''
            out.append(f'| {old} | {new} | [{name}.md]({name}.md) |\n')
    out.append('## Дополнительные тематические записи / каталог\n\n| Запись | Stable F | Источник |\n|---|---|---|\n')
    for r in c.supplements:out.append(f'| {r["title"]} | {r["id"]} | [{r["report"]}.md]({r["report"]}.md), L{r["line"]} |\n')
    out.append('## Вторичные аналитические источники\n\n'+ '\n'.join(f'- {name}: {sid}; saved worker, не независимый primary chain.' for name,sid in c.local_s.items())+'\n')
    text='\n'.join(out)
    text=re.sub(r'(\|[^\n]*\n)\n+(?=\|)',r'\1',text)
    (c.WORK/'ID_MAP.md').write_text(text,encoding='utf-8')

if __name__=='__main__':
    c.build_sources();c.build_raw();open_questions();id_map()
    # Augment machine-readable intermediate with curated final maps, not a new report.
    c.dump_state()
    (c.WORK/'COLLECTOR_CURATED.json').write_text(json.dumps({'questions':Q,'experiments':E,'mapping':c.mapping},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'S':len(c.groups),'F':len(set(r['id'] for r in c.allfacts)),'Q':len(Q),'E':len(E),'aliases':len(c.mapping)},ensure_ascii=False))


