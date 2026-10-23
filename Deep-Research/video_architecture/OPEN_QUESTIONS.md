# Открытые вопросы и программа проверок video_architecture

Дата сборки и подтверждённая дата обращения: **2026-10-23 Europe/Moscow (UTC+3)**. Collector не получал новую сеть, не запускал приложения/камеры/SDK/LinQ и не выполнял предложенные E. W1 закончена до прерывания и не повторялась; несохранённый первый critic не восстанавливался. Сохранённый CRITIC создан отдельным fresh-context critic_resume, затем выполнены шесть W2 по K001–K010. Нет полного кейса, issued SDK/grant, actual LinQ output и runtime benchmark. Ранние интервалы W1_01/03 приблизительны: они не являются точным журналом отдельных обращений. SHA snapshot доказывает состав сохранённых bytes, а не неизменность current upstream или работу программы.

Все эксперименты ниже **предложены, НЕ выполнены**. Никаких device/application/benchmark/browser/DB fault результатов эта стадия не добавила. Повторные W1/W2 вопросы и fixtures объединены по решению; native aliases и исходные подробности доступны через ID_MAP и worker locators.

## Первые часы: порядок закрытия

1. **0–2ч:** Q001/Q002/Q003/Q005/Q025; E001 — actual grant, model boundary, accepted witness и один real LinQ golden. GUI/job без usable result/приемлемого cycle → unsupported-live.
2. **2–6ч:** Q004/Q010/Q015; E009 — early remux mapping gate; E015 — actual patched SQLite/runtime; E018 — source→LinQ→own-frame view→event commit. Если exact clips обязательны, snapshot cut не закрывает требование.
3. **6–18ч:** Q007/Q013/Q021; E005/E006/E007/E011 — две камеры, full cycle, gaps, held через restart и slow browser.
4. После slice: E003/E004/E010/E016/E017; optional native video/messenger/image health только после core gates. Эти интервалы — инженерный план, не measured effort/45ч feasibility.

## Реестр неизвестного

<a id="q001"></a>

### Q001 — Issued LinQ grant, собственная модель и принятое доказательство исполнения

**Приоритет:** P0 / 0–2 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Прочитаны LinQ homepage/tech/sol, официальный анонс и вторичный linq_platform. Обещаны онлайн-доступ и inference на LinQ; публичная download/demo форма не даёт callable API, custom-model update или granted host.

**Почему не закрыто:** Нет полного кейса, issued manual/schema, account/grant, matched SDK/native/driver/firmware/model artifacts и принятого execution witness. CPU/mock соседей не device run.

**Какое решение меняет:** Выбирает API, shell, managed video, job или unsupported-live. Service-only без SSH может быть достаточен; GUI-only без машиночитаемых результатов — нет.

**Способ закрытия:** Постановщик + полный кейс + issued артефакт + E001/E018. Сохранить manual revision, allowed model boundary/update, hashes golden input/model/output, request/run/device correlation и accepted witness.

**Связи:** [F001](RAW_FACTS.md#f001) [F003](RAW_FACTS.md#f003) [F005](RAW_FACTS.md#f005) [F007](RAW_FACTS.md#f007) [F023](RAW_FACTS.md#f023) [F204](RAW_FACTS.md#f204) K010 [E001](OPEN_QUESTIONS.md#e001) [E018](OPEN_QUESTIONS.md#e018).

**Происхождение вопросов:** W1-01-Q01, W1-03-Q01, W1-06-Q01, W2-06-Q02.

<a id="q002"></a>

### Q002 — Remote lifecycle, quota, ambiguous submit и native input lifetime

**Приоритет:** P0 / 0–2 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** AWS Batch — один документированный аналог: cancel200 не terminal, running timeout не queue TTL, zero ListJobs не negative proof. Спроектирован persisted held ledger, отдельные local/control/fetch caps и bounded STOPPED.

**Почему не закрыто:** LinQ submit dedup scope/window, lookup visibility, definitive rejection, hidden retries, accepted/running weights, terminal/release/acceptance-cutoff/TTL и safe buffer release не выданы. Старый backup может не знать post-cutoff jobs.

**Какое решение меняет:** Без доказанного release удержать remote credit через timeout/epoch/restart/restore. View TTL освобождает view bytes, не native borrowed input. Нет reliable reconcile — stop соответствующего admission, не held=0.

**Способ закрытия:** Issued manual/owner + E001/E007/E016. Только разрешённые benign calls; lost ACK в own fixture. Фиксировать tenant/quota namespace, terminal witness и режим без auto-resume.

**Связи:** [F134](RAW_FACTS.md#f134) [F136](RAW_FACTS.md#f136) [F138](RAW_FACTS.md#f138) [F139](RAW_FACTS.md#f139) [F143](RAW_FACTS.md#f143) [F144](RAW_FACTS.md#f144) [F145](RAW_FACTS.md#f145) [F146](RAW_FACTS.md#f146) [F170](RAW_FACTS.md#f170) [F195](RAW_FACTS.md#f195) K001 [E007](OPEN_QUESTIONS.md#e007) [E016](OPEN_QUESTIONS.md#e016).

**Происхождение вопросов:** W1-01-Q03, W1-03-Q02, W1-04-Q01, W2-01-Q01, W2-01-Q02, W2-03-Q02, W2-05-Q03, W2-02-Q05.

<a id="q003"></a>

### Q003 — Разрешённое размещение decoder/pre/post и app data plane

**Приоритет:** P0 / 0–2 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** HPS optional video encode и HX/RK3588 decode — разные host/product claims. SSH/VPN не даёт root/Docker/ports/daemon lifetime. Remote compact boxes не обеспечивают analyzed pixels на local projection.

**Почему не закрыто:** Неизвестны host CPU/RAM/ISA/codec/permissions, source reachability, persistence, listeners/tunnel и права CPU NMS/wrapper. Нельзя считать remote RTSP из private LAN доступным.

**Какое решение меняет:** При frame API весь app у команды. Remote decode minimum переносит единый app data plane/DB/recorder/projection к decoder только при полном grant; иначе thin worker и local decode. Возврат JPEG при remote decode — отдельный downlink.

**Способ закрытия:** Owner grant/network inventory + E001/E005/E008/E018; сравнить один clip в допустимых placements, отдельно CPU/network/privacy. Не устанавливать web/DB на shared host без предоставленного права.

**Связи:** [F006](RAW_FACTS.md#f006) [F025](RAW_FACTS.md#f025) [F147](RAW_FACTS.md#f147) [F200](RAW_FACTS.md#f200) [F204](RAW_FACTS.md#f204) K006 K010 [E008](OPEN_QUESTIONS.md#e008) [E018](OPEN_QUESTIONS.md#e018).

**Происхождение вопросов:** W1-01-Q02, W1-02-Q01, W2-01-Q04.

<a id="q004"></a>

### Q004 — Реальные source codec/profile/FPS/GOP/bitrate/PTS

**Приоритет:** P0 / первые 2 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** RTSP/ONVIF/media controls различены; sampling после decode не снижает автоматически decode source FPS. Main/sub могут отличаться crop/FOV/clock; loop — simulated source.

**Почему не закрыто:** Нет организаторских видео/камер, firmware, profiles, ffprobe sample, B-frames/IDR bound, VBR distribution, source NTP/PTS discontinuity rules.

**Какое решение меняет:** Определяет decode compatibility, encoder/GOP recovery, bytes/ring cap и timestamp mapping. Missing PTS запрещает exact clock по FPS/host now.

**Способ закрытия:** Полный кейс/source artifact/камера + ffprobe inventory и E002/E003/E009; сохранить hashes, codec/profile/pix_fmt/FPS/time_base/keyframe structure и raw timestamp trace.

**Связи:** [F038](RAW_FACTS.md#f038) [F040](RAW_FACTS.md#f040) [F041](RAW_FACTS.md#f041) [F042](RAW_FACTS.md#f042) [F043](RAW_FACTS.md#f043) [F151](RAW_FACTS.md#f151) [F158](RAW_FACTS.md#f158) K002 [E002](OPEN_QUESTIONS.md#e002) [E009](OPEN_QUESTIONS.md#e009).

**Происхождение вопросов:** W1-02-Q03, W1-05-Q02, W2-02-Q03.

<a id="q005"></a>

### Q005 — Domain temporal contract: required FPS/max gap/dwell/onset/ID

**Приоритет:** P0 / первые 2 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Анонс перечисляет примеры нарушений. Gap не negative, mean5fps не max-gap guarantee, physical dwell не update count; короткое событие может не попасть sampler.

**Почему не закрыто:** Полный обязательный перечень/точность/задержка/минимальный coverage/ID continuity/onset и interruption semantics отсутствуют. Сетевой tracker поиск этих требований не устанавливает.

**Какое решение меняет:** Без этого 5fps, T_fresh и max_gap — сценарии, не SLA. Снижение FPS/camera count допускается только в пределах метода; no-tracker route не заменяет ID-dependent метод.

**Способ закрытия:** Полный кейс + violation_methods/evaluation/operator_product + E004/E006/E017/E018. Versioned contract с units, denominators, cadence tolerance, missing-PTS policy и quality thresholds.

**Связи:** [F085](RAW_FACTS.md#f085) [F132](RAW_FACTS.md#f132) [F172](RAW_FACTS.md#f172) [F184](RAW_FACTS.md#f184) K005 K010 [E006](OPEN_QUESTIONS.md#e006) [E017](OPEN_QUESTIONS.md#e017).

**Происхождение вопросов:** W1-03-Q03, W1-04-Q02, W1-06-Q02, W2-04-Q01, W2-06-Q01.

<a id="q006"></a>

### Q006 — Фактическое железо и CPU/QuickSync/NVDEC decode capacity

**Приоритет:** P0/P1 / inventory сразу, нагрузка после slice. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** В контексте только RTX4070 и ноутбук. NVDEC13.0 Ada indicative table и T4 DeepStream7.1 — внешние измерения с иными условиями. Portable CPU/QuickSync decode-only per-core числа не найдены; encode/transcode отсечены.

**Почему не закрыто:** CPU, exact SKU/VRAM/driver/thermal power mode, codec backend/build, surfaces/copies и sustained throughput ещё не измерены.

**Какое решение меняет:** Выбор software/hardware decode, threads/shards, resize-before-download и безопасный admission. Нельзя вывести число камер из 903fps, TOPS или одной raw latest-slot оценки.

**Способ закрытия:** Локальный hardware/build inventory + E003/E005. Указать source corpus/codec/GOP, warmed/cold, CPU-seconds/frame, decode+transfer+resize отдельно и per-camera freshness под paced load.

**Связи:** [F045](RAW_FACTS.md#f045) [F046](RAW_FACTS.md#f046) [F047](RAW_FACTS.md#f047) [F048](RAW_FACTS.md#f048) [F049](RAW_FACTS.md#f049) [F123](RAW_FACTS.md#f123) [F197](RAW_FACTS.md#f197) [F198](RAW_FACTS.md#f198) [E003](OPEN_QUESTIONS.md#e003) [E005](OPEN_QUESTIONS.md#e005).

**Происхождение вопросов:** W1-02-Q02, W1-02-Q05.

<a id="q007"></a>

### Q007 — LinQ usable full-chain cycle и per-camera feasibility

**Приоритет:** P0 / после golden. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Необходимы два ограничения: per-camera f_i≤p_i/E[L_i] и aggregate occupancy/capacity; L включает client NMS/cascade/ordered apply. p1,L300ms даёт≤3.33fps даже при K100.

**Почему не закрыто:** Нет measured L/tails, endpoint concurrency/thread-safety/batch, service capacity/shared fairness и minimum domain FPS/maxgap. 1/p95(L) не tail guarantee.

**Какое решение меняет:** Не обещать 5fps/camera по aggregateFPS. p>1 — только при supported stateless/sequencing + bounded sparse sent-ID reorder и полезном выигрыше freshness.

**Способ закрытия:** Issued SDK/API/model + E005/E006/E008/E018 с реальным LinQ. Saturation curve и каждый camera admitted/applied/gaps/age; remote-held accounting отдельно от local parent slots.

**Связи:** [F069](RAW_FACTS.md#f069) [F180](RAW_FACTS.md#f180) [F181](RAW_FACTS.md#f181) [F182](RAW_FACTS.md#f182) [F183](RAW_FACTS.md#f183) K005 [E005](OPEN_QUESTIONS.md#e005) [E018](OPEN_QUESTIONS.md#e018).

**Происхождение вопросов:** W1-06-Q05, W2-04-Q02.

<a id="q008"></a>

### Q008 — JPEG/resolution/chroma/ROI quality на целевых RGB СИЗ

**Приоритет:** P0 / до quality claim. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Два первичных исследования FLIR thermal/COCO показывают риск recall tiny/small. Их Q30/Q40/размерные bins и модели не PPE threshold. Q100 не lossless, camera baseline уже compressed.

**Почему не закрыто:** Нет target RGB labelled sample/модели/thresholds и paired predictions для каски, респиратора, сигареты, дальностей/освещения/толпы.

**Какое решение меняет:** JPEG size — переменная distribution, не обещанное compression ratio. ROI discovery/crop fanout и resize могут менять quality/compute; нельзя экономить сеть без quality gate.

**Способ закрытия:** Datasets/model_stack/evaluation + E004. Paired encode grid с fixed model/preprocess; bytes/CPU и recall по классам/размеру плюс event missed/false alarms.

**Связи:** [F063](RAW_FACTS.md#f063) [F064](RAW_FACTS.md#f064) [F068](RAW_FACTS.md#f068) [F105](RAW_FACTS.md#f105) [E004](OPEN_QUESTIONS.md#e004).

**Происхождение вопросов:** W1-03-Q04.

<a id="q009"></a>

### Q009 — Модель, batch/stateful sequence и каскадная NN-граница

**Приоритет:** P0/P1. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Triton/Hailo — только образцы. ROI discovery тоже работа; person/PPE cascade требует bounded q_max и secondary unknown при quota drop.

**Почему не закрыто:** Не выбраны actual model artifacts/input layout/dtype/quant scales/fixed or dynamic batches/state affinity, secondary cost и допустимая обязательная LinQ boundary.

**Какое решение меняет:** Определяет preprocessing ownership, batch families, primary/secondary caps и допустимость temporal latest-drop. Не считать arbitrary uint8/JPEG/batch поддержанными.

**Способ закрытия:** Model_stack/linq_platform + issued artifacts/полный кейс + E001/E004/E005/E008. Каждый revision повторяет golden/parity; accepted NN boundary фиксируется отдельно от CPU postprocess.

**Связи:** [F054](RAW_FACTS.md#f054) [F061](RAW_FACTS.md#f061) [F065](RAW_FACTS.md#f065) [F066](RAW_FACTS.md#f066) [F182](RAW_FACTS.md#f182) [E005](OPEN_QUESTIONS.md#e005) [E008](OPEN_QUESTIONS.md#e008).

**Происхождение вопросов:** W1-03-Q05, W1-03-Q07.

<a id="q010"></a>

### Q010 — Event→original segment mapping и допустимость snapshot cut

**Приоритет:** P0 / ранний gate2–6 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** MediaMTX1.21.2 mtxi содержит recorder StreamID/SegmentNumber/DTS/NTP, не decoder/source epoch; hooks/UTC filename не дают source PTS. Native export теряет mtxi. Same-demux indexed remux — prospective route.

**Почему не закрыто:** Не выполнен packet-lifetime/reorder/rescale/coverage fixture; missing/duplicate PTS, loops, wrap, decoder-only/recorder-only restart, main/sub uncertainty не измерены.

**Какое решение меняет:** До E009 нет exact clip claim. Gate fail → analyzed snapshot + optional native archive mapping unknown. Если full case требует exact clips, такой cut остаётся blocker.

**Способ закрытия:** Source inventory+собственный prototype+E009/E010/E016. Один H264 video-only профиль/дем ux owner, indices ДО mutable mux, independent decode watermark и 0false-complete.

**Связи:** [F083](RAW_FACTS.md#f083) [F116](RAW_FACTS.md#f116) [F150](RAW_FACTS.md#f150) [F152](RAW_FACTS.md#f152) [F153](RAW_FACTS.md#f153) [F154](RAW_FACTS.md#f154) [F158](RAW_FACTS.md#f158) K002 [E009](OPEN_QUESTIONS.md#e009) [E018](OPEN_QUESTIONS.md#e018).

**Происхождение вопросов:** W1-04-Q03, W1-05-Q03, W2-02-Q02, W2-05-Q05, W2-06-Q04.

<a id="q011"></a>

### Q011 — Finite evidence acceptance, pre/post/retention и квоты

**Приоритет:** P0/P1. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Unbounded remote delay нельзя покрыть finite ring. Проект L_evidence20/P5/Q5/S2/G≤1/C4/J30/H40s и chunk/rollover/quota bounds сохранён как fixture, не требования. Old onset после dwell учитывать отдельно.

**Почему не закрыто:** Нет требуемого evidence window/retention/допустимой partial/snapshot политики, actual max bitrate/GOP/disk и максимальной задержки выдачи.

**Какое решение меняет:** Нужны finite pin admission deadlines, future ranges, job/count/byte caps и visible late/partial/unavailable; не расширять ongoing job бесконечно и не удалять pinned молча.

**Способ закрытия:** Полный кейс/operator_product+device/storage inventory+E010. Требования могут сделать snapshot cut недопустимым; long queue не исправляется только большим H.

**Связи:** [F104](RAW_FACTS.md#f104) [F105](RAW_FACTS.md#f105) [F159](RAW_FACTS.md#f159) [F160](RAW_FACTS.md#f160) [F161](RAW_FACTS.md#f161) K003 [E010](OPEN_QUESTIONS.md#e010).

**Происхождение вопросов:** W1-05-Q01, W1-06-Q04, W2-02-Q01.

<a id="q012"></a>

### Q012 — Target filesystem, commit/file sync, backup failure domain, RPO/RTO

**Приоритет:** P1 / до durability claim. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** SQLite WAL+FULL, patched engine и successful COMMIT — выбранный proposal; DB transaction не включает обычные media files. Supported Connection.backup+verified closed-media inventory, restore/fencing/pin rebuild/remote reconcile описаны.

**Почему не закрыто:** Не известны FS/VFS/device caches/fsync/directory-persistence recipe, storage reserve, power/disk-loss behavior, backup interval/failure domain/key recovery и actual RPO/RTO. Ни один fault run не выполнен.

**Какое решение меняет:** Process kill не power-loss proof; old backup не held=0. До pin rebuild запрещено retention deletion; missing original/unknown mapping не complete.

**Способ закрытия:** Exact target/диск+E010/E016; separate process crash, reboot, OS/power fault, disk loss на disposable authorized testbed; externally durable commit witness и verified backup cutoff.

**Связи:** [F189](RAW_FACTS.md#f189) [F192](RAW_FACTS.md#f192) [F193](RAW_FACTS.md#f193) [F194](RAW_FACTS.md#f194) [F195](RAW_FACTS.md#f195) [F196](RAW_FACTS.md#f196) K008 [E016](OPEN_QUESTIONS.md#e016).

**Происхождение вопросов:** W1-05-Q06, W2-02-Q04, W2-05-Q04.

<a id="q013"></a>

### Q013 — Processed view runtime: profile, credit, teardown и total RSS

**Приоритет:** P0/P1 / до freshness claim. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Pinned websockets17.0.1 чтение подтверждает directions watermarks и send≠render. Проект 1outstanding/connection, exact ACK after draw, credit-cycle age guard, active+closing admission caps; timeout terminal, не новый credit.

**Почему не закрыто:** Нет browser/OS/RTT/throughput/tiles/quality/age inventory; public close_timeout не доказанный wall-clock teardown bound, app-owned references не total kernel/browser RSS.

**Какое решение меняет:** Профиль/количество tiles/FPS/connection cap допускаются по тесту; closing продолжает занимать budget. Экспериментальный transport.abort subclass не public websockets API и не mandatory minimum.

**Способ закрытия:** E011/E012 на exact Python/browser/TLS/proxy/OS; source checksum/ACK/draw trace, hidden/reconnect/blackhole и process RSS/FD/task trends. Physical scanout/operator read отдельно.

**Связи:** [F162](RAW_FACTS.md#f162) [F163](RAW_FACTS.md#f163) [F164](RAW_FACTS.md#f164) [F166](RAW_FACTS.md#f166) [F167](RAW_FACTS.md#f167) [F168](RAW_FACTS.md#f168) [F169](RAW_FACTS.md#f169) [F171](RAW_FACTS.md#f171) K004 [E011](OPEN_QUESTIONS.md#e011) [E012](OPEN_QUESTIONS.md#e012).

**Происхождение вопросов:** W2-03-Q01, W2-03-Q04.

<a id="q014"></a>

### Q014 — Optional native browser video: codec, NAT и source↔RTP↔rVFC mapping

**Приоритет:** P1 / optional после core. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** MediaMTX reader/WHEP signaling lifecycle и ICE media path различны. H265/B-frames/browser ограничены; rVFC best-effort и не произвольный camera frame ID. HEAD reader W1 не lock к 1.21.2.

**Почему не закрыто:** Нет actual browser codec/selected candidate pair, TURN/cert/domain/port grants и sourcePTS→RTP/SSRC/epoch mapping uncertainty. HTTPS200 не media connectivity.

**Какое решение меняет:** Плавный original live отдельно от analyzed own-frame view. Без mapping boxes на latest native frame не рисовать как measurement.

**Способ закрытия:** E013 на площадке; same-tag reader/server, OPTIONS/POST/PATCH/DELETE/CORS, UDP blocked/subpath/TURN и independent frame markers; exact overlay только после доказанного mapping.

**Связи:** [F106](RAW_FACTS.md#f106) [F107](RAW_FACTS.md#f107) [F108](RAW_FACTS.md#f108) [F109](RAW_FACTS.md#f109) [F114](RAW_FACTS.md#f114) [F115](RAW_FACTS.md#f115) K004 [E013](OPEN_QUESTIONS.md#e013).

**Происхождение вопросов:** W1-05-Q04, W1-05-Q05.

<a id="q015"></a>

### Q015 — Provisional artifact baseline vs actual installed target/Astra

**Приоритет:** P0/P1 / 2–6 ч. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Candidate MediaMTX1.21.2/PyAV16.0.1/CPython3.12.15 source/websockets17.0.1/linked patched SQLite3.51.3. CPython3.12.15 source-only; no official Windows installer. Exact PyAV Linux wheel был read-only inspected, не imported.

**Почему не закрыто:** Binary target OS/ISA/ABI/glibc/engine/Compose/image digests/driver и linked SQLite source_id/compile_options неизвестны. Python patch не определяет SQLite. Astra news scopes не support matrix приложения.

**Какое решение меняет:** Не обновлять proprietary supplied env до client Python. Offline own bundle и LinQ network availability различны; W1 catalog snapshots не requirements lock.

**Способ закрытия:** E015 + issued/vendor supported artifacts. Verify actual Python connection SQLite advisory/PRAGMA; clean-target/offline-client smoke и полный golden. Поддержанный vendor backport документировать вместо угадывания version tuple.

**Связи:** [F014](RAW_FACTS.md#f014) [F015](RAW_FACTS.md#f015) [F017](RAW_FACTS.md#f017) [F018](RAW_FACTS.md#f018) [F185](RAW_FACTS.md#f185) [F186](RAW_FACTS.md#f186) [F188](RAW_FACTS.md#f188) [F190](RAW_FACTS.md#f190) K007 [E015](OPEN_QUESTIONS.md#e015).

**Происхождение вопросов:** W1-01-Q04, W1-04-Q04, W2-03-Q03, W2-05-Q01, W2-06-Q06.

<a id="q016"></a>

### Q016 — Лицензия фактически shipped code/native libs/weights

**Приоритет:** P1 / до distribution. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** 8catalog entries имеют direct repo scope. PyAV BSD wrapper не весь bundled libav/x264/x265/gnutls; Linux wheel strings/ZIP и workflow прочитаны. Roboflow nearest superseding license, Ultralytics AGPL/enterprise, SDK/weights отдельно.

**Почему не закрыто:** Нет полного shipped artifact inventory/transitive notices/source obligations, standalone ffmpeg buildflags/hash, proprietary redistribution terms и model/dataset licenses. Идеи из unused catalog не shipped dependency.

**Какое решение меняет:** reuse_mode process/dependency/copied-code/idea-only меняет scope. Другой wheel/OS требует своего чтения. License repo нельзя объявлять license всего продукта.

**Способ закрытия:** Фактический manifest+primary license texts/vendor terms+E015; exact copied path nearest LICENSE и notices, model_stack/datasets. Не выполнять аудит unused projects ради каталога.

**Связи:** [F071](RAW_FACTS.md#f071) [F187](RAW_FACTS.md#f187) [F188](RAW_FACTS.md#f188) K007 [E015](OPEN_QUESTIONS.md#e015).

**Происхождение вопросов:** W1-04-Q05, W2-05-Q02.

<a id="q017"></a>

### Q017 — Event rate, DB/broker need и external idempotency

**Приоритет:** P1. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Одна SQLite БД/one writer/outbox — proposal; WS/SSE projection, CoreNATS ephemeral, Redis pending reclaim и broker QoS не exactly-once external effect. Crash after send beforemarker допускает duplicate.

**Почему не закрыто:** Нет required event/update rate, concurrent operator writers/retention, acceptable backlog и provider durable idempotency key/receiver inbox.

**Какое решение меняет:** Брокер/PostgreSQL вводить после measured need; не держать DB lock во время network await. Один dispatcher для minimum, stable event_id/revision и восстановление history.

**Способ закрытия:** Полный кейс/operator_product+E014/E016. Event generator в units events/s, не cameraFPS; measured commit/backlog age/WAL/duplicates и receiver contract.

**Связи:** [F087](RAW_FACTS.md#f087) [F088](RAW_FACTS.md#f088) [F089](RAW_FACTS.md#f089) [F090](RAW_FACTS.md#f090) [F091](RAW_FACTS.md#f091) [F092](RAW_FACTS.md#f092) [F093](RAW_FACTS.md#f093) [F191](RAW_FACTS.md#f191) K008 [E014](OPEN_QUESTIONS.md#e014).

**Происхождение вопросов:** W1-04-Q06, W1-04-Q07.

<a id="q018"></a>

### Q018 — Alarm delivery boundary, messenger accounts и product access

**Приоритет:** P0/P1. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Event decided/committed/provider accepted/browser drawn/operator acknowledged — разные endpoints. Telegram/MAX rates/docs прочитаны, не измерены/не отправлялись сообщения. MAX endpoint/auth/certificate менялись.

**Почему не закрыто:** Нет полного product канала/recipient IDs/токенов/правабота/MAX business access, network accessibility и accepted alarm boundary/age. Read receipt/latency SLA не установлены.

**Какое решение меняет:** Core — event history/UI; messenger optional после access. Clip pending не задерживает initialalarm. Provider timeout после accept — uncertain outcome/possibleduplicate.

**Способ закрытия:** Operator_product+owner credentials+E014/E017. Fake provider сначала; реальные тестовые отправки только отдельно авторизованной практикой, не production recipients.

**Связи:** [F117](RAW_FACTS.md#f117) [F118](RAW_FACTS.md#f118) [F119](RAW_FACTS.md#f119) [F120](RAW_FACTS.md#f120) [F121](RAW_FACTS.md#f121) [F122](RAW_FACTS.md#f122) [F131](RAW_FACTS.md#f131) [E014](OPEN_QUESTIONS.md#e014) [E017](OPEN_QUESTIONS.md#e017).

**Происхождение вопросов:** W1-05-Q07, W1-06-Q03.

<a id="q019"></a>

### Q019 — Camera encrypted transport, tenant isolation и protected data boundary

**Приоритет:** P1. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Axis/NIST/Docker дают scoped examples: HTTPS управления не encrypted RTSP; Digest не encryption; VLAN/firewall требуют flow inventory; auth проверяется у clip/stream endpoints; Compose secrets не encrypted vault.

**Почему не закрыто:** Неизвестны camera firmware/client TLS/SRTP/RTSPS/accounts, remote tenant isolation/upload retention/logging/delete policy, keys/permissions и approved routes.

**Какое решение меняет:** Camera credentials только у нужного owner; browser получает authenticated application path. Remote decode/recording выбираются вместе с privacy/persistence policy и bandwidth.

**Способ закрытия:** Device/vendor/remote owner + E015 functional security checks: exact flow table, invalid-cert failures, viewer/operator/admin и secret redaction; право/КИИ → market_deployment.

**Связи:** [F011](RAW_FACTS.md#f011) [F019](RAW_FACTS.md#f019) [F020](RAW_FACTS.md#f020) [F022](RAW_FACTS.md#f022) [E015](OPEN_QUESTIONS.md#e015).

**Происхождение вопросов:** W1-01-Q05, W1-01-Q06.

<a id="q020"></a>

### Q020 — Долгая RTSP freshness/RSS, drift и reconnection

**Приоритет:** P1 / после slice. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Version-specific FFmpeg/GStreamer/PyAV/OpenCV параметры и negative cases сохранены. rtspsrc tcp-timestamp обходит drift, но burst source создаёт иной риск; timeout не bound frame age.

**Почему не закрыто:** Нет 2h/overnight paced run actual source/backend, control-alive-no-media, native hang cleanup и true/false tcp-timestamp comparison.

**Какое решение меняет:** Backend/transport/watchdog выбирается по progress/RSS/watermark; ret=True, PID и socket alive недостаточны.

**Способ закрытия:** E002: pinned build/known source, slow consumer, disconnect/restart/media blackhole;10min correctness затем 2h/ночь при доступности. Publisher transcode не смешивать с isolated decode.

**Связи:** [F026](RAW_FACTS.md#f026) [F029](RAW_FACTS.md#f029) [F033](RAW_FACTS.md#f033) [F050](RAW_FACTS.md#f050) [F051](RAW_FACTS.md#f051) [F052](RAW_FACTS.md#f052) [E002](OPEN_QUESTIONS.md#e002).

**Происхождение вопросов:** W1-02-Q04, W1-02-Q06.

<a id="q021"></a>

### Q021 — Opaque tracker cadence/reset и ID quality

**Приоритет:** P0/P1 для ID-dependent метода. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** ByteTrack fixed dt1/update, frame_rate только lost buffer; no-call freeze, valid empty(0,5) — observation, public gap/reset нет. New instance+tracking_generation — wrapper proposal; PTS не меняет dt.

**Почему не закрыто:** Нет tracker smoke/installability/footprint/domain ID metrics или допустимости short-gap carry. Старые np.float/imports и dependencies не tested, cadence/maxgap неизвестны.

**Какое решение меняет:** Tracker optional по gate; cadence violation→reset/unknown. ID-dependent метод при failed gate — degraded/unsupported, не per-frame замена.

**Способ закрытия:** E006 с pinned reference, uniform/burst equal-mean/drop/empty/long-gap traces и separate annotated domain quality. Другая gap-aware реализация/адаптация требует validation.

**Связи:** [F173](RAW_FACTS.md#f173) [F174](RAW_FACTS.md#f174) [F175](RAW_FACTS.md#f175) [F176](RAW_FACTS.md#f176) [F177](RAW_FACTS.md#f177) [F178](RAW_FACTS.md#f178) [F179](RAW_FACTS.md#f179) K005 [E006](OPEN_QUESTIONS.md#e006).

**Происхождение вопросов:** W1-02-Q07, W2-04-Q03, W2-04-Q04.

<a id="q022"></a>

### Q022 — Направленные goodput/clock/resource coefficients для 50/500

**Приоритет:** P1 / до capacity claim. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Input/return/view/control/storage сценарии и memory inventory сохранены.500 registered не 500 tiles/viewer; RAM включает DPB/surfaces/contexts/pools/borrows/TLS/DB, не один raw slot.

**Почему не закрыто:** Нет measured WAN↑↓/RTT/jitter/clock offset, FD/ports/sessions/processes/threads/VRAM/IO replay+backup и mcam/Cinf/Cdec/Cpre/Cwrite coefficients.

**Какое решение меняет:** Нет единственного network X или числа LinQ плат.50 — candidate host после теста,500 — shards/sites roadmap; ресурсы проверяются вместе с per-camera temporal gate.

**Способ закрытия:** E003/E005/E008/E011/E016: topology/dataflow по host/direction, actual profile tails; same-host monotonic durations и optical/sync uncertainty для сквозного возраста.

**Связи:** [F068](RAW_FACTS.md#f068) [F069](RAW_FACTS.md#f069) [F133](RAW_FACTS.md#f133) [F148](RAW_FACTS.md#f148) [F198](RAW_FACTS.md#f198) [F199](RAW_FACTS.md#f199) [F200](RAW_FACTS.md#f200) K006 [E005](OPEN_QUESTIONS.md#e005).

**Происхождение вопросов:** W1-03-Q06, W2-06-Q03.

<a id="q023"></a>

### Q023 — Camera image-health thresholds/false alarms/suitability

**Приоритет:** P2 / optional. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Axis product docs разделяют image-health/причину вмешательства и unsuitable scenes. Progress/age mandatory; repeated/black/white/blur/shift — hypotheses suspected_anomaly.

**Почему не закрыто:** Нет сцен/thresholds/false alarms per camera-hour/CPU cost и day/night/static/detail-poor/legitimate PTZ controls. Overexposure heuristic не заявленная Axis capability.

**Какое решение меняет:** Availability/staleness допустимы в core; image anomaly только с baseline/config revision/suitability и visible suspected label.

**Способ закрытия:** E019 с positive/negative controls; неразделимые controls→cut. Synthetic distortion не real-world tamper proof.

**Связи:** [F201](RAW_FACTS.md#f201) [F202](RAW_FACTS.md#f202) [F203](RAW_FACTS.md#f203) K009 [E019](OPEN_QUESTIONS.md#e019).

**Происхождение вопросов:** W2-06-Q05.

<a id="q024"></a>

### Q024 — Accepted fallback/replay и фактическая 45 ч feasibility

**Приоритет:** P0 / scopego-no-go. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** 45 ч — арифметика официального расписания, не guaranteed LinQ uptime. Есть conditional minimum/5 owners/gates/cuts; ни один полный маршрут не запускался. CPU/RTX/replay должны быть marked.

**Почему не закрыто:** Full case, accepted witness/current grant/required features и реализация не подтверждены;225 person-hours не взаимозаменяемы.

**Какое решение меняет:** Real LinQ golden выше optional features; GUI/job без usable output/cycle unsupported-live. Snapshot cut не закрывает обязательные exact clips.

**Способ закрытия:** Full case/organizer acceptance + E001/E018/checkpoint demo. Сохранить witness/trace, failure states, separate backend counts; saved run не current live.

**Связи:** [F023](RAW_FACTS.md#f023) [F024](RAW_FACTS.md#f024) [F131](RAW_FACTS.md#f131) [F204](RAW_FACTS.md#f204) [F206](RAW_FACTS.md#f206) [F207](RAW_FACTS.md#f207) K010 [E018](OPEN_QUESTIONS.md#e018).

**Происхождение вопросов:** W1-06-Q06.

<a id="q025"></a>

### Q025 — Actual output heads, NMS/quantization и return/postprocess budget

**Приоритет:** P0 / после golden. **Статус:** открыто; proposal/docs/code не runtime closure.

**Известное / где искали:** Triton binary/ensemble — пример, не LinQ. Сценарий [1,84,8400]FP32=2822400B/frame против packed2404B для≤100detections; NMS/cap могут менять quality.

**Почему не закрыто:** Нет actual serialized response/names/shapes/dtypes/scales/layout/head semantics/classmap/coordinates/truncation/result retention. JSON wire bytes не numel×dtype.

**Какое решение меняет:** Raw return может доминировать downlink/CPU/RAM; supported remote NMS/compact API меняет placement. Не делать NMS дважды и не cast dtype без контракта.

**Способ закрытия:** Model artifact/schema + E008: golden reference parity, crowded/empty/invalid/oversize caps, actual wire/poll/fetch/postprocess/full cycle.

**Связи:** [F141](RAW_FACTS.md#f141) [F142](RAW_FACTS.md#f142) [F147](RAW_FACTS.md#f147) [F148](RAW_FACTS.md#f148) [F149](RAW_FACTS.md#f149) K006 [E008](OPEN_QUESTIONS.md#e008).

**Происхождение вопросов:** W2-01-Q03.

## Дискриминирующая программа E

Общий corpus, trace IDs и fixtures переиспользуются; assertions различны. Программы ниже не предписывают нагрузку/kill/reset общего стенда. Реальные sender tests и disruptive fault tests требуют отдельно предоставленного допуска на собственный testbed. Чтение/арифметика этой исследовательской волны к этим E не относятся.

<a id="e001"></a>

### E001 — Issued capability inventory и real LinQ golden path

**Статус:** PROPOSED / NOT RUN.

**Решение:** Выбрать supported access mode и доказать ровно один фактический inference нашей версии модели на LinQ.

**Входы / доступ:** Полный кейс, именной разрешённый grant/manual/schema, golden positive/negative inputs, model/preprocess reference и accepted execution witness; read-only host inventory только если shell предоставлен.

**Шаги:** Разделить model/control/data/lifecycle; зафиксировать custom model upload/update/select; выполнить один documented request, получить machine-readable output и terminal/release evidence; узнать hidden retries, quotas, source reachability и разрешённый restart. Если lifecycle непрозрачен, сохранить UNKNOWN и bounded stop.

**Метрики / сохраняемые артефакты:** Manual revision, hashes model/input/output/config, redacted request/result/job/run IDs, actual backend/device witness, OS/ISA/CPU/codec/permissions; measured local roundtrip отдельно от reported server durations.

**Исходы / действия:** Callable custom service достаточен без SSH. Нет usable outputs/приемлемого cycle → unsupported-live/offline route и точный missing-grant packet. Не заменять LinQ GPU fallback.

**Чего успех не доказывает:** Один golden run не capacity, fairness, p99, TTL, качество всех классов или sustained realtime.

**Связи:** [Q001](OPEN_QUESTIONS.md#q001) [Q002](OPEN_QUESTIONS.md#q002) [Q003](OPEN_QUESTIONS.md#q003) [Q025](OPEN_QUESTIONS.md#q025) K001 K010 [F005](RAW_FACTS.md#f005) [F146](RAW_FACTS.md#f146) [F204](RAW_FACTS.md#f204).

**Сведённые исходные fixtures:** W1-01-E01, W2-01-E02. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e002"></a>

### E002 — RTSP continuous reader, overload, failure и soak

**Статус:** PROPOSED / NOT RUN.

**Решение:** Выбрать PyAV/знакомый GStreamer, TCP/UDP, watchdog/reconnect и bounded latest-frame policy.

**Входы / доступ:** Pinned MediaMTX1.21.2, actual FFmpeg build, H264/H265720p/1080p25/30 samples с visible frame/clock/loop ID; source hashes, ffprobe JSON и GOP. Изолированный own test route.

**Шаги:** Loop publisher с -re -stream_loop -1 -c copy; сравнить naive sleep/read, continuous decode/latest и bounded raw queues. Медленный consumer200ms при source25fps; 2–3 источника, один stalls. Publisher/server disconnect, media-only blackhole/control alive, EOF/native hang; tcp-timestamp true/false при drift/burst.10min correctness затем 2h/ночь по доступности.

**Метрики / сохраняемые артефакты:** Watermark p50/p95/p99 age, input/decode/selected/applied FPS, RSS trend, decode errors, resets/reconnect reasons, fresh recovery time, queue drops, unaffected camera service; configs/versions/CSV/state trace/UI recording.

**Исходы / действия:** Выбрать режим по freshness/CPU/RSS и bounded recovery, config/auth errors выделить. Неуспех isolation→исправить ownership/watchdog либо другой проверенный backend.

**Чего успех не доказывает:** Loop не live industrial camera; soak не LinQ throughput, качество событий или многосуточный production SLA.

**Связи:** [Q004](OPEN_QUESTIONS.md#q004) [Q020](OPEN_QUESTIONS.md#q020) [F026](RAW_FACTS.md#f026) [F052](RAW_FACTS.md#f052) [F075](RAW_FACTS.md#f075).

**Сведённые исходные fixtures:** W1-02-E01, W1-04-E03. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e003"></a>

### E003 — Decode-only и полная цена model input: CPU/NVDEC/QuickSync

**Статус:** PROPOSED / NOT RUN.

**Решение:** Выбрать decode backend/threads/resize placement и actual admitted camera count.

**Входы / доступ:** Actual CPU/GPU/SKU/VRAM/OS/driver/power/cooling, pinned ffmpeg/PyAV/native library build; одинаковый H264/H265720/1080p corpus, profiles8/10bit420, GOP/B-frames. Publisher transcode не конкурирует за CPU.

**Шаги:** Warmup и≥3 repeats; isolated throughput без -re, затем paced1/2/4/8streams. Software1/default/2/4decoder threads; GPU path с проверенным hardware use/fallback disabled. Decode-only, download, GPU resize-before-download, color/letterbox и input packing измерять отдельно. QSV только после runtime/driver inventory.

**Метрики / сохраняемые артефакты:** CPU-seconds/frame и busy-core equivalents, wall frames/s, GPU video clocks/decode/memory, bytes copied, RSS/VRAM, p95 age при paced load; commands/buildconf/corpus hashes/raw measurements.

**Исходы / действия:** Admit только sustained profile с reserve и agreed FPS/age; hardware capability без working build не pass. Оставить программный decode при отсутствии проверенного acceleration.

**Чего успех не доказывает:** Чужой 903fps не наша 4070, isolated max не RTSP reliability, LinQ inference или 500camera proof.

**Связи:** [Q006](OPEN_QUESTIONS.md#q006) [Q022](OPEN_QUESTIONS.md#q022) [F045](RAW_FACTS.md#f045) [F049](RAW_FACTS.md#f049) [F197](RAW_FACTS.md#f197).

**Сведённые исходные fixtures:** W1-02-E02. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e004"></a>

### E004 — RGB compression, resize, ROI и sampling quality

**Статус:** PROPOSED / NOT RUN.

**Решение:** Определить допустимые payload/view/source profiles без скрытой потери мелких нарушений.

**Входы / доступ:** Размеченные целевые RGB PPE/zone scenes, разные размеры/свет/толпа, fixed model/threshold/preprocess. Baseline decoded source уже может быть lossy. Полный кейс задаёт допустимую quality loss.

**Шаги:** Paired JPEG Q95/85/75/60/50 с fixed encoder/chroma, отдельно resize grid. Crop original vs crop recompressed frame; crowd r и bounded ROI fanout, full-frame discovery cost. Сравнить 25fps→select5fps, NONKEY, source-native5fps, GOP25/50/100/B0 и gaps. Сузить grid после finding.

**Метрики / сохраняемые артефакты:** Bytes distribution mean/p95/p99/max, encode/decode CPU, class/size recall/AP, event missed/false alarms, short-act loss, source delta/coverage, geometry parity; paired predictions, examples и hashes.

**Исходы / действия:** Profile допускается по согласованным class/event thresholds. Fail→повысить detail/изменить placement или честно ограничить сценарий; не замещать падение recall стабильной precision.

**Чего успех не доказывает:** FLIR/COCO Q thresholds не PPE; каска не сигарета, Q100 не lossless, снижение CPU не качество inference на LinQ.

**Связи:** [Q005](OPEN_QUESTIONS.md#q005) [Q008](OPEN_QUESTIONS.md#q008) [Q009](OPEN_QUESTIONS.md#q009) [F063](RAW_FACTS.md#f063) [F064](RAW_FACTS.md#f064) [F068](RAW_FACTS.md#f068).

**Сведённые исходные fixtures:** W1-02-E03, W1-03-E02, W1-06-E02. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e005"></a>

### E005 — Paced saturation, fairness, cascade и полный resource budget

**Статус:** PROPOSED / NOT RUN.

**Решение:** Выбрать C/B/p_i, admitted cameras и размещение по per-camera freshness/gaps, не aggregate throughput.

**Входы / доступ:** Source corpus+required FPS/maxgap/age, actual topology/goodput, granted quota; сначала tagged dummy delay route, затем real LinQ. Decoder/record/view/replay/backup ownership counters.

**Шаги:** B1,C1/2/4/8/16 до разрешённого knee, затем supported batches. Constant offered pacing, step overload/recovery, fast/slow/stalled/crowded source, q0..qmax ROI; p1 vs2/3 при fullcycle50/160/200/300/500ms synthetic fixture. Empty view→3×4tiles→slow/hidden→replay+backup.50/500 только при стенде/правах, иначе symbolic extrapolation.

**Метрики / сохраняемые артефакты:** Every camera admitted/completed/fresh ordered applied FPS, max media/wall gaps, age quantiles с full denominator, drop reasons, byte/count caps, remote held/unknown, post CPU. FD/handles/processes/threads/sockets/contexts/surfaces/pools/RSS/PSS/VRAM, NIC↑↓, disk Bps/IOPS/latency, WAL/replay/backup; raw traces/configs/hashes.

**Исходы / действия:** Pass — одновременно agreed per-camera coverage/age, app/resource caps и measured reserve. Knee без fresh throughput→не наращивать C. Reduce admission/profile/viewers/placement только с quality gate. Camera reduction не лечит p1 single-camera ceiling.

**Чего успех не доказывает:** Mock L не LinQ prediction; Little-law means не tails; one-stream peak и synthetic500 не 500 real cameras/general quality.

**Связи:** [Q006](OPEN_QUESTIONS.md#q006) [Q007](OPEN_QUESTIONS.md#q007) [Q009](OPEN_QUESTIONS.md#q009) [Q022](OPEN_QUESTIONS.md#q022) K005 K006 [F180](RAW_FACTS.md#f180) [F182](RAW_FACTS.md#f182) [F198](RAW_FACTS.md#f198).

**Сведённые исходные fixtures:** W1-01-E02, W1-03-E01, W1-03-E03, W1-06-E01, W1-06-E06, W2-04-E03, W2-06-E01. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e006"></a>

### E006 — Ordering/epochs, fixed-dt tracker, valid empty и domain gaps

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить temporal contract, p>1 reorder и допустимость выбранного ID-dependent метода.

**Входы / доступ:** Pinned ByteTrack reference при необходимости, отдельный compatible environment; actual method minFPS/maxgap/ID rules, boxes+empty(0,5), source PTS0,.2,.4 vs0,.2,2.4; annotated PPE episodes.

**Шаги:** Sparse sent100/105/110; ответы 110→105→timeout100→late100, duplicate105, epochE1→E2, timeout wakeup без reply. Compare no-call, real empty, synthetic empty (negative control), new instance/tracking_generation; strict lost > boundary и reactivation-before-expiry. Equalmean uniform/burst/drop/2sgap/reconnect traces; ID quality отдельно от contract.

**Метрики / сохраняемые артефакты:** Append-only sent/arrival/apply/gap/reset/reject/remote-credit trace, KF covariance/framecounter/lost/removed, globalID scope, queue bytes, source deltas и coverage, event recall/false alarms/fragmentation и ID metrics; versions/input hashes.

**Исходы / действия:** 0old epoch/out-of-order apply, no unsent101 wait, один live outcome/request, Gap не negative и не remote release. Cadence violation→explicit reset/unknown; чрезмерные resets→degraded/unsupported method. Variable-dt adaptation требует своего quality validation.

**Чего успех не доказывает:** Correct wrapper trace не качество ID/re-ID; timestamps/frame_rate constructor не variable dt; mock ordering не LinQ lifecycle.

**Связи:** [Q005](OPEN_QUESTIONS.md#q005) [Q007](OPEN_QUESTIONS.md#q007) [Q021](OPEN_QUESTIONS.md#q021) K005 [F173](RAW_FACTS.md#f173) [F175](RAW_FACTS.md#f175) [F183](RAW_FACTS.md#f183) [F184](RAW_FACTS.md#f184).

**Сведённые исходные fixtures:** W1-03-E04, W1-04-E01, W2-04-E01, W2-04-E02, W2-04-E04. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e007"></a>

### E007 — Persisted remote ledger: fake-job fault/restart fixture

**Статус:** PROPOSED / NOT RUN.

**Решение:** Доказать наши reservation/release invariants и honest STOPPED без достаточного external contract.

**Входы / доступ:** Собственный fake service, durable DB, deterministic virtual clock/service active-job log. idempotent_submit on/off, visibility/keyretention/TTL cases; K_remote2/local submit1/control1 — fixture, не LinQ.

**Шаги:** Crash до/после intent commit/send/accept/ack/jobID persist; lostack, sameUUID/differenthash, hiddenretry как 2jobs, cancel200 continuing work, status404/unknown enum, epoch/live timeout, restart с 2held, terminal duplicate, DB ack/release commiterror. Отдельно lateacceptance после предполагаемого TTL.

**Метрики / сохраняемые артефакты:** Ordered intent/send/accept/ack/poll/terminal/release trace, row snapshots/hash/job IDs, service active IDs, held/local slots/bytes, double releases, stale applies, fixture revision/seed.

**Исходы / действия:** 0≤held≤2, каждый возможно active job покрыт reservation, terminal release ровно один. Нет dedup/full TTL/acceptance cutoff→bounded STOPPED; unknown не исчезает после restart. Fail→учесть retries/ownership/atomicity, не разрешить свежие submits ради progress.

**Чего успех не доказывает:** Virtual duration не runtime latency; fixture не подтверждает LinQ contract, DB power durability или general reliability.

**Связи:** [Q002](OPEN_QUESTIONS.md#q002) K001 [F143](RAW_FACTS.md#f143) [F144](RAW_FACTS.md#f144) [F145](RAW_FACTS.md#f145) [F146](RAW_FACTS.md#f146).

**Сведённые исходные fixtures:** W1-01-E04, W1-06-E03, W2-01-E01. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e008"></a>

### E008 — Output schema, numerical parity, NMS placement и return path

**Статус:** PROPOSED / NOT RUN.

**Решение:** Выбрать raw/compact return и postprocess placement, реальные downlink/CPU/RAM coefficients.

**Входы / доступ:** Actual serialized result+all head schemas/scales/classmaps, reference model/preprocess/thresholds/quantization; remote wrapper только при grant. Labelled crowded/empty target sample.

**Шаги:** Сверить body bytes с shape/dtype/batch mapping, endian/layout, head decode/NMS/coordinate transforms. Rawreference vs compact parity в объявленной tolerance; empty/max/invalidshape/oversize/truncation. Измерить polls/status/fetch/postprocess вместе с actual path, не переменить dtype наугад.

**Метрики / сохраняемые артефакты:** Mean/p95/max wire bytes/output, poll QPS/bytes/visibility delay, fetch/post CPU durations local clocks, peak live buffers/RSS, fullcycle/fresh FPS, paired detections/quality/cap misses; schema/reference hashes.

**Исходы / действия:** Parity и bounds→зафиксировать output/postprocess revision и directional50/500 variables. Raw доминирует→remote compact при разрешении; unavailable→admission/architecture cut. AlreadyNMS output не NMS повторно.

**Чего успех не доказывает:** Oneframe CPU не 500capacity; postprocess parity не обязательное execution proof LinQ; scenario[1,84,8400] не actual chosen model.

**Связи:** [Q025](OPEN_QUESTIONS.md#q025) [Q003](OPEN_QUESTIONS.md#q003) [Q007](OPEN_QUESTIONS.md#q007) K006 [F147](RAW_FACTS.md#f147) [F148](RAW_FACTS.md#f148) [F149](RAW_FACTS.md#f149).

**Сведённые исходные fixtures:** W2-01-E03. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e009"></a>

### E009 — Early event→original mapping proof: same-demux indexed remux

**Статус:** PROPOSED / NOT RUN.

**Решение:** Допустить exact event→original route либо сразу выбрать snapshot cut.

**Входы / доступ:** Pinned MediaMTX1.21.2/PyAV16.0.1 с actual libav build; H264 video-only B0/B2, GOP1/10s, VFR, visible frame/loop/clock IDs и hashes. Собственный same-demux indexed remux и native archive для сравнения.

**Шаги:** Индексировать packet PTS/DTS/rational time_base/codec/random-access ДО mutable mux rebase; отдельные refs/lifetime для decode. Сопоставить yielded frame с independently decoded closed original. Inject decoder-only/recorder-only restart, reset/continuous loop, backward PTS vs reorder, известный wrap, missing/duplicate PTS, UTC jump и main/sub negative controls.

**Метрики / сохраняемые артефакты:** Packet/frame/output sample trace, distinct source/decoder/recorder generations, original/output time_base и offsets, mtxi/manifest/hashes; wrong-original/loop, внутренние gaps, max grid error и mapping uncertainty.

**Исходы / действия:** 0 false complete; любое неоднозначное соответствие unknown/partial. Fail→analyzed snapshot, native archive mapping unknown и custom recorder off. Если exact clips обязательны, это blocker; имя файла UTC не обход.

**Чего успех не доказывает:** Один fixture не arbitrary camera/codec/RTCP/main-sub/power-loss/LinQ и не доказанная 45 ч feasibility. Наличие PTS само по себе не lineage proof.

**Связи:** [Q010](OPEN_QUESTIONS.md#q010) K002 [F152](RAW_FACTS.md#f152) [F154](RAW_FACTS.md#f154) [F158](RAW_FACTS.md#f158).

**Сведённые исходные fixtures:** W1-05-E01, W2-02-E01. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e010"></a>

### E010 — Finite evidence windows, pins, low-space и recorder crash

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить конечные count/bytes/lifetime и honest partial/unavailable.

**Входы / доступ:** Own ring/DB/media test volume, измеренный GOP/max bitrate, E009 для complete. H40/P5/Q5/L20/C4/J30s, chunk10s/rollover60s/finite incident quota — только fixture.

**Шаги:** Результаты с delay1/19/21/120s, long dwell/30min ongoing media, stalled post-roll/no IDR, duplicate event/manual expiry/dead worker; concurrent retention/export/low-space. Kill create-before-init/part-write/close/index/hash/publish. Scan/reconcile, validated prefix derivative, future pin intent и reserved bytes на диске, pin rebuild до deletion.

**Метрики / сохраняемые артефакты:** Requested/actual intervals/gaps/generations/hashes; transition/deadline reasons; reservations/unique retained bytes, owner pins/refcounts, GOP/open-part reserve, oldest job и event revisions.

**Исходы / действия:** 0 false complete; late/lost coverage→partial/unavailable. Каждый job terminal≤J+bounded dispatch jitter, metadata incident продолжается после evidence quota. Low-space не удаляет pinned молча; snapshot тоже bounded.

**Чего успех не доказывает:** Finite local policy не remote queue SLA/recall; process kill не power/disk loss; H40s не универсальная глубина и не число камер.

**Связи:** [Q010](OPEN_QUESTIONS.md#q010) [Q011](OPEN_QUESTIONS.md#q011) [Q012](OPEN_QUESTIONS.md#q012) K003 [F159](RAW_FACTS.md#f159) [F160](RAW_FACTS.md#f160) [F161](RAW_FACTS.md#f161).

**Сведённые исходные fixtures:** W1-05-E02, W2-02-E02, W2-02-E03. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e011"></a>

### E011 — Processed WS renderer: slow/hidden/fanout/ACK/lifetime

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить same-frame renderer и 1outstanding/viewer через slow/hidden/reconnect.

**Входы / доступ:** Exact pinned Python/websockets/browser/OS; JPEG с крупным frame ID и own boxes, near-cap profile;3viewers fast/decode3s/hidden60s. Tiny raw pool/checksums/8bounded requests для lifetime.

**Шаги:** Producer10fps, ACK off, main-thread stall/hide/reconnect, старый image до close event, wrong/future/duplicate nonce ACK и early ACK в SENDING. Busy выставляется до await; credit до send; bitmap.close/finally; elapsed credit-cycle check перед draw. Source reset во время decode, oversize header/JPEG/boxes/dimensions/DPR и reconnect до cleanup.

**Метрики / сохраняемые артефакты:** State/key/send/draw/ACK trace, checksum frame/box, retained-view vs borrowed-input counters, latest/outstanding/closing counts, bitmap lifecycle, heap/process RSS/FD, UI capture и drop reasons.

**Исходы / действия:** Outstanding≤1/connection, decode≤1/page через поколения, no old-generation draw/mismatch/extra credit; fast viewer не ждёт slow. Timeout terminal, не новый credit. Malicious ACK после receive может лгать о draw — зафиксировать ограничение.

**Чего успех не доказывает:** App-owned reference bounds не total RSS/kernel/browser cap; canvas ACK не physical scanout/operator read; mock не LinQ safe input release.

**Связи:** [Q013](OPEN_QUESTIONS.md#q013) [Q002](OPEN_QUESTIONS.md#q002) K004 [F166](RAW_FACTS.md#f166) [F167](RAW_FACTS.md#f167) [F168](RAW_FACTS.md#f168) [F169](RAW_FACTS.md#f169) [F170](RAW_FACTS.md#f170).

**Сведённые исходные fixtures:** W1-04-E05, W1-05-E04, W2-03-E01, W2-03-E03, W2-03-E04. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e012"></a>

### E012 — Blocked transport, public close и bounded cleanup

**Статус:** PROPOSED / NOT RUN.

**Решение:** Оценить public-only close и выбрать проверенную mitigation при failure.

**Входы / доступ:** Own isolated exact OS/TLS/proxy/Python/websockets route; peer stops reads, rate≪B/deadline, loss/blackhole, large valid payload.

**Шаги:** Send→deadline→CLOSING→public close с repeated connection attempts. Не cancel/send-again в том же connection. Active+closing остаются в finite admission cap. Отдельная experimental ветка create_connection/subclass сохраняет asyncio transport и вызывает documented abort; это не public websockets API.

**Метрики / сохраняемые артефакты:** Task dumps, send/close elapsed, closing age/count, transport buffers где доступны, socket FD/handles before/after, memory trends и cleanup logs; TLS/proxy yes/no.

**Исходы / действия:** Нет новых send/resources сверх cap после timeout. Hanging teardown — failure public-only route; visible unavailable/admission stop и затем E-tested mitigation. Не вычёркивать closing из budget по таймеру.

**Чего успех не доказывает:** Одна OS не universal TCP/kernel release; source read/close_timeout не hard wall cap; abort не гарантия browser/native RSS release.

**Связи:** [Q013](OPEN_QUESTIONS.md#q013) K004 [F164](RAW_FACTS.md#f164) [F167](RAW_FACTS.md#f167) [F168](RAW_FACTS.md#f168).

**Сведённые исходные fixtures:** W2-03-E02. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e013"></a>

### E013 — Optional native WebRTC/LL-HLS и browser mapping

**Статус:** PROPOSED / NOT RUN.

**Решение:** Допустить optional original live и установить условия overlay.

**Входы / доступ:** Same-version MediaMTX server/reader, actual codec/GOP/browser/OS, network/cert/domain/TURN grant, watermark/frame ID corpus.

**Шаги:** LAN/hotspot/NAT/UDP blocked/HTTPS proxy/subpath/TURN TCP. Проверить OPTIONS/POST201 Location/PATCH/DELETE/Link/CORS, selected candidate pair, H264 B0/H265 negative; rVFC fields/source PTS→RTP/SSRC/epoch mapping, viewport/DPR. Overlay disabled при unknown mapping.

**Метрики / сохраняемые артефакты:** Time-to-first-frame, glass-to-glass p50/p95 с quantization, bitrate/CPU/RSS30–60min, reconnect, skew/no-match/stale и UI/packet metadata.

**Исходы / действия:** Нет codec/media route→processed view либо проверенный HTTP fallback с visible delay. Exact overlay только с measured mapping; original live может работать без inference.

**Чего успех не доказывает:** HTTP200/STUN docs не media connectivity;600ms part math не benchmark, домашний тест не площадка, rVFC не arbitrary camera ID.

**Связи:** [Q014](OPEN_QUESTIONS.md#q014) [F106](RAW_FACTS.md#f106) [F109](RAW_FACTS.md#f109) [F114](RAW_FACTS.md#f114) [F115](RAW_FACTS.md#f115).

**Сведённые исходные fixtures:** W1-05-E03. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e014"></a>

### E014 — Event/outbox durability, replay и optional notifier

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить сохранность committed incidents и честно показать possible duplicates.

**Входы / доступ:** Own DB/fake receiver с durable inbox/idempotency on/off,429 retry_after/500/timeout до и после accept, required event rate, disconnected UI/history cursor.

**Шаги:** Kill до commit/после commit до send/после accept до marker; provider/broker offline, poison payload, stale lease/fencing. Valid/expired cursor replay/snapshot resync. Overall/per-recipient rates и bounded retry/backoff/jitter. Реальный test bot/chat/clip/link — только отдельно авторизованной практикой.

**Метрики / сохраняемые артефакты:** Unique event_id/revision/outbox keys, commit operation IDs/attempts/external IDs, pending oldest age/count, commit p95/WAL, receiver effects и дубли; provider accept/browser draw/operator ack отдельно.

**Исходы / действия:** Committed event/outbox восстанавливаются в заявленном process-crash scope; receiver inbox даёт dedup его DB effects. Без provider idempotency duplicate возможен. Broker/PostgreSQL только после measured need.

**Чего успех не доказывает:** Fake не Telegram/MAX access/latency; Message response не read receipt, QoS/Kafka transactions не external exactly-once или power durability.

**Связи:** [Q017](OPEN_QUESTIONS.md#q017) [Q018](OPEN_QUESTIONS.md#q018) [F093](RAW_FACTS.md#f093) [F119](RAW_FACTS.md#f119) [F120](RAW_FACTS.md#f120) [F121](RAW_FACTS.md#f121).

**Сведённые исходные fixtures:** W1-04-E02, W1-04-E04, W1-05-E05, W1-05-E06. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e015"></a>

### E015 — Artifact/runtime/offline/Astra/security gate

**Статус:** PROPOSED / NOT RUN.

**Решение:** Зафиксировать фактический bundle и проверить ровно target configuration.

**Входы / доступ:** Разрешённый clean target OS/ISA/glibc/driver, artifacts/hashes/licenses/model/static assets, installed/supplied engine/Compose/host drivers. Proprietary LinQ environment отдельно.

**Шаги:** Verify hashes offline; inventory CPython/av.library_versions/library_meta/websockets и linked SQLite source_id/compile_options/PRAGMAs именно Python connection. Reject unpatched WAL либо документировать vendor backport. Load images/up--no-build--pull never без CDN/pip/apt/model downloads. Web→volume→decode→LinQ golden→event/view/restore. Astra edition/kernel/policy/device/rootless только approved config; auth roles, invalid TLS/token, log/frontend secret redaction.

**Метрики / сохраняемые артефакты:** Final artifact/lock manifest, platform/build flags/transitive notices/hashes, image IDs/digests, source_id/PRAGMA returns, redacted startup/network logs, sample→event trace и access/flow table.

**Исходы / действия:** 0 missing mandatory imports/ABI; patched SQLite доказан, own offline client не fetch packages. Fail→supplied environment/isolated worker/remote API/scope cut; не менять shared SDK/mandatory protection наугад.

**Чего успех не доказывает:** Source pin не binary/installed; offline images не offline LinQ; UI на Astra не driver support/сертификат; functional security checks не pentest/IEC compliance.

**Связи:** [Q015](OPEN_QUESTIONS.md#q015) [Q016](OPEN_QUESTIONS.md#q016) [Q019](OPEN_QUESTIONS.md#q019) K007 [F185](RAW_FACTS.md#f185) [F186](RAW_FACTS.md#f186) [F187](RAW_FACTS.md#f187) [F188](RAW_FACTS.md#f188) [F190](RAW_FACTS.md#f190).

**Сведённые исходные fixtures:** W1-01-E03, W1-01-E05, W1-01-E06, W2-05-E01. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e016"></a>

### E016 — SQLite commit/fault, supported backup/restore и remote reconciliation

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить acknowledged commit, verified backup и safe admission после restore.

**Входы / доступ:** Own isolated exact patched SQLite/local FS, event/outbox/ledger/pins/media fixture, disposable bounded volume; externally durable witness для разрешённых power classes, не общий стенд.

**Шаги:** Kill before/after BEGIN/write/COMMIT/response; BUSY/IOERR/disk-full/long-reader WAL growth. Connection.backup в maintenance window + immutable media inventory/holds/hash; integrity_check+foreign_key_check. Создать remote obligations после cutoff, restore в новый каталог, fence old owners/new boot, orphan/missing/tail validation и pin rebuild до retention, documented remote reconcile. Reboot/forced OS/power/disk loss отдельно.

**Метрики / сохраняемые артефакты:** Commit IDs/recovered rows, WAL/journal сохранены, errors/queue/durations; backup cutoff/schema/runtime/hashes, missing/orphan/partial statuses, refcounts/reservations/held before/after, failed backup publication, measured RPO/RTO/witness.

**Исходы / действия:** 0 acknowledged success без recovered commit в declared process-crash scope; no event without outbox, no failed backup published, no false complete/deletion до rebuild. Post-cutoff unknown не free credit; no reliable reconcile→STOPPED. File publish durability требует actual FS recipe.

**Чего успех не доказывает:** Process kill не power/disk loss, integrity_check не FK/media/remote proof, checksum не fsync; один backup не HA/универсальная durability.

**Связи:** [Q002](OPEN_QUESTIONS.md#q002) [Q012](OPEN_QUESTIONS.md#q012) [Q015](OPEN_QUESTIONS.md#q015) K008 [F189](RAW_FACTS.md#f189) [F191](RAW_FACTS.md#f191) [F193](RAW_FACTS.md#f193) [F194](RAW_FACTS.md#f194) [F195](RAW_FACTS.md#f195) [F196](RAW_FACTS.md#f196).

**Сведённые исходные fixtures:** W1-06-E05, W2-05-E02, W2-05-E03, W2-05-E04. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e017"></a>

### E017 — Alarm latency с onset/dwell и полным denominator

**Статус:** PROPOSED / NOT RUN.

**Решение:** Измерить agreed event-to-operator endpoint и отделить compute/video latency.

**Входы / доступ:** Controlled physical onset/разметка, temporal dwell contract, paced source/actual LinQ/view/recording, optical source+screen запись либо доказанная clock sync с error bound.

**Шаги:** Phase sweep sampler,1camera затем admitted load. Каждый planned episode с ID: physical onset/first qualifying frame/rule eligible/committed/delivered-drawn/optional operator ack. Cold/steady/reconnect; misses/timeouts/session-ended pending остаются в denominator.

**Метрики / сохраняемые артефакты:** Raw same-host monotonic durations+clock domain/UTC uncertainty; end-to-end p50/p95/p99 с n/warmup/load, fraction offered alerted within SLA, missed/censored/downtime; optical evidence и quantization bound.

**Исходы / действия:** Total quantiles только из e2e traces/совместимых histograms, не сумма stage p95/средний worker p95. При>1% timeouts не обещать unconditional p99 ниже deadline по success subset; показать short-event misses.

**Чего успех не доказывает:** Canvas ACK не physical scanout/operator read; success latency не event recall, mock/media test не LinQ или другая сеть.

**Связи:** [Q005](OPEN_QUESTIONS.md#q005) [Q018](OPEN_QUESTIONS.md#q018) [Q022](OPEN_QUESTIONS.md#q022) [F125](RAW_FACTS.md#f125) [F126](RAW_FACTS.md#f126) [F127](RAW_FACTS.md#f127) [F132](RAW_FACTS.md#f132) [F207](RAW_FACTS.md#f207).

**Сведённые исходные fixtures:** W1-06-E04. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e018"></a>

### E018 — Integrated minimum/mode go-no-go

**Статус:** PROPOSED / NOT RUN.

**Решение:** Проверить required vertical slice и выбрать конкретный scope cut.

**Входы / доступ:** Issued grant/full case, golden model/input/reference/accepted witness, actual selected bundle, positive/empty/error/late/old-generation fixtures.

**Шаги:** Real LinQ→1source→own-frame view→event commit/history→snapshot/clip status, затем 2camera isolation. Raw/compact parity, ambiguous submit/restart, gap/order/epoch, early E009 либо snapshot cut, slow viewer/DB fault/backup-restore/clean target. Gates0–2/2–6/6–18/18–32/32–40/40–45 ч — план.

**Метрики / сохраняемые артефакты:** Trace packet source/frame→request/model→LinQ run→result→event revision→evidence coverage→draw/ACK; ledger/pins before/after restart, versions/hashes/planned outcomes, required quality/FPS/gaps/age и visible failure states.

**Исходы / действия:** Pass: actual LinQ и full-case required route/temporal/persistence contracts. Нет automated result/cycle→unsupported-live. Exact clips required+mapping fail→blocker; иначе согласованный snapshot cut. Optional native/messenger/blur/broker/extra cameras после core.

**Чего успех не доказывает:** Mock не pass;2camera не 50/500/industrial proof; saved witnessed replay не current live; proposal не доказанная 45 ч feasibility.

**Связи:** [Q001](OPEN_QUESTIONS.md#q001) [Q005](OPEN_QUESTIONS.md#q005) [Q007](OPEN_QUESTIONS.md#q007) [Q010](OPEN_QUESTIONS.md#q010) [Q024](OPEN_QUESTIONS.md#q024) K010 [F204](RAW_FACTS.md#f204) [F206](RAW_FACTS.md#f206) [F207](RAW_FACTS.md#f207) [F205](RAW_FACTS.md#f205).

**Сведённые исходные fixtures:** W2-06-E03. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.

<a id="e019"></a>

### E019 — Camera-health positive/negative controls

**Статус:** PROPOSED / NOT RUN.

**Решение:** Оставить progress/age либо допустить ограниченные suspected image signals.

**Входы / доступ:** Annotated day/night/static/detail-poor/machinery corpus, known onset/hash/baseline/ROI; repeated pixels/new PTS, repeated PTS/new pixels, loop continuous/reset, corrupt/black/white/blur/shift.

**Шаги:** По одному фактору и controls lights-off/IR switch/white wall/truck/legitimate PTZ; restore/relearn/suitability. Отдельно transport blackhole с control alive. Bounded downsample/rate, thresholds/config revision.

**Метрики / сохраняемые артефакты:** Signal/delay timeline, false alarms/camera-hour/scene, recovery/hysteresis/CPU budget, confusion table/source/config/UI statuses.

**Исходы / действия:** Mandatory: no progress→stale в watchdog+tolerance; новые frames не analysis healthy. Optional: согласованные false-alarm/delay на этой выборке, unsuitable→unknown/suspected; неразделимые controls→cut.

**Чего успех не доказывает:** Synthetic distortion не real-world tamper proof/причина вмешательства/quality PPE; универсальных thresholds нет.

**Связи:** [Q023](OPEN_QUESTIONS.md#q023) K009 [F201](RAW_FACTS.md#f201) [F202](RAW_FACTS.md#f202) [F203](RAW_FACTS.md#f203).

**Сведённые исходные fixtures:** W2-06-E02. Подробные versioned команды и уникальные negative cases сохраняются также в соответствующих worker sections и RAW_FACTS.
