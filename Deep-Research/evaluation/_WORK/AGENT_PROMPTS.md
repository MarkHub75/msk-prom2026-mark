# INDIVIDUAL AGENT PROMPTS

## Shared self-contained instructions for every first-wave researcher

You are an independent first-wave researcher, GPT-6.1 Sol (`gpt-6.1-sol`) at medium effort. Working folder: `D:/msk-prom2026-mark/evaluation`. Read this shared section and your assigned cell below; read both input contracts completely if you need fuller context. Team of five prepares for Otkroy#Mosprom 2026, industrial safety video analytics, examples helmet/respirator absence, danger-zone entry, smoking near combustible material. These are examples, not established taxonomy. Inference on LinQ is required by the supplied context; no full case, organizer data/evaluator, SDK, device configuration or access is supplied. RTX 4070 and cloud capability are contextual, no specifications or measured performance assumed. Goal: separate object recognition, person-level violations, useful timely alerts, and verified target execution.

Use available web search/browsing and primary documents/code/papers; open actual sources, do not treat snippets as evidence. You may use network reads through Python/PowerShell for source files and metadata; preserve source provenance, code commit and exact locator. Search beyond seeds when useful; explicitly search for counterexamples and applicability failures. No external messaging, no user questions, no large benchmarks, no application building. Do not spawn more agents. Do not write shared final registries or other cells' files.

Write a substantive standalone Russian or English result `_WORK/W1_XX.md`, UTF-8. Use local IDs `W1-XX-S01`, `W1-XX-F01` etc. Sources must include title, author/org, URL, publication/version date or unknown, access timestamp timezone, section/function, retrieval status and limitations. Facts must separate documentation, source-code inspection, published measurements, locally executed small examples, own inference, proposed protocol and unknown. Record metric units, GT, matching, numerator/denominator, aggregation, ignore/unknown/empty cases, implementation/version, limits. No invented acceptance targets, commands or APIs. Code read is not code run. Preserve contradictions. Paraphrase rather than reproduce long passages. Store any source downloads only in `_WORK/W1_XX_SOURCES/` and keep native names when needed.

At completion give root a short handoff: key findings, decisions affected, output path and unresolved questions. Finish when there is a useful supported answer or precisely localized unknown after substantive search, not a link quota. Full details remain on disk. Honor the user's unattended run and continue autonomously.

## W1_01 — Truth, observability and annotation agreement

Question: How can examples become a reproducible truth contract? Decision: what to annotate and when the task cannot be observed. Investigate object/state/event, visible PPE versus correctly worn PPE, hidden head, unknown protection type, incomplete annotation, ignore/ambiguous; independent annotators, agreement and adjudication. Seek primary annotation methodology and benchmark policies. Give concrete schema and counterexamples; no universal sample-size promise or legal norm inferred from pixels. Boundaries: no dataset catalog or legal analysis. Output `_WORK/W1_01.md`; transfer needs to datasets/violation_methods.

## W1_02 — Detection AP and exact evaluator behavior

Question: When are AP/precision/recall comparable? Decision: detector comparison configuration. Start https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/cocoeval.py ; obtain immutable commit and inspect evaluateImg/accumulate/summarize/Params. Document matching, IoU/ranking/AP interpolation, size, maxDets, crowd/ignore, absent classes. Compare relevant evaluator variants only with sources. Counterexamples: duplicates, wrong coordinates/class mapping, unlabeled object, empty image/class. Output `_WORK/W1_02.md`; no model ranking.

## W1_03 — Person state and PPE association

Question: Why can object AP coexist with person-level alert errors? Decision: full-chain test versus conditional classification. Find primary PPE annotation/evaluation methods and concrete association failure cases. Specify GT persons, visibility, PPE ownership, unknown; matched/unmatched persons, GT-person oracle vs predicted chain. Cases helmet in hand, neighbor PPE, crowd, occlusion; coverage and denominator prevent excluding difficult people. Output `_WORK/W1_03.md`; do not choose architecture for violation_methods.

## W1_04 — Danger-zone geometry and boundary semantics

Question: What does entry into a zone mean in image versus physical space? Decision: truth and geometry tests. Primary point-in-polygon boundary APIs, camera calibration/homography limits; anchor points, perspective, hidden feet, camera motion, jitter, partial overlap. Give alternative contracts, exact edge tests and unknowns, distinguish code conformance from physical hazard proof. No universal threshold. Output `_WORK/W1_04.md`; handoff to violation_methods/video_architecture.

## W1_05 — Event matching, duplicates, fragmentation and censoring

Question: Which temporal protocols answer which alert question? Decision: explicit proposed event matching. Inspect primary ActivityNet/DCASE or related evaluator code pinned to revision. Compare segment tIoU, onset/collar and one-to-one alert matching. Explain duplicates, splits, merges, cooldown, repeated entry, pre-existing or cut-off episodes; true onset vs observable sign vs algorithm confirmation vs delivery. Include contrasting worked examples and distinguish benchmark rule from own proposal. Output `_WORK/W1_05.md`.

## W1_06 — Rare events, false alarms and exposure

Question: What can false alerts per evaluated camera-hour and zero observed alerts establish? Decision: duration/annotation evidence required for workload claims. Seek primary statistical rate bounds and continuous-video protocols. Define unit/exposure, delivered duplicates, unreviewed intervals, person-hour pitfalls, prevalence change, reviewing alert samples versus finding missed events. Derive zero-count bound with explicit assumptions and heterogeneous-camera limitations. Output `_WORK/W1_06.md`; no fabricated operational threshold.

## W1_07 — Splits, leakage and target population

Question: Which independent groups support known-camera versus new-camera claims? Decision: manifest split and adaptation declaration. Official GroupKFold/TimeSeriesSplit, original leakage/spatial temporal dependency sources. Same-video cuts, near duplicates, re-encoding, unknown pretraining overlap; tuning thresholds on test, post-error annotation, unlabeled test adaptation. Give conditional dev/validation/test routes and limits of deduplication. Output `_WORK/W1_07.md`; handoff datasets/training_strategy.

## W1_08 — Thresholds, calibration, abstention

Question: How select operating point without test tuning? Decision: joint model/NMS/temporal policy selection. Read Guo https://proceedings.mlr.press/v70/guo17a.html and official calibration/threshold docs; pin library version where relevant. Object/person/event confidence differ. Explain PR selection, per-class thresholds, precision/recall/workload constraints, ECE/reliability/Brier limitations, unknown and domain shift. Counterexamples for calibrated classification transferring to event alarms. Output `_WORK/W1_08.md`.

## W1_09 — Tracking and identity continuity

Question: What do HOTA/IDF1/MOTA establish and miss about alerts? Decision: tracker evidence and alert regression cases. Inspect https://github.com/JonathonLuiten/TrackEval and https://arxiv.org/abs/2009.07736 ; pin code and describe required IDs, association, localization, ID switches, fragmentation. Track ID is not worker identity. Re-alert after ID switch, state transfer between persons, occlusion; full-ID versus no-ID annotation routes. Output `_WORK/W1_09.md`.

## W1_10 — Export and quantization parity

Question: How compare native, exported and target-compiled behavior? Decision: stage localization and acceptance owner. Use primary export/runtime/quantization docs, versioned where possible. Input resize/letterbox/color/dtype/range/layout, raw outputs, coordinates, class order, NMS, threshold-boundary changes. Tensor tolerances versus detections versus events; not bitwise identity by default. Successful import is not useful detection or all-ops-on-LinQ proof. Output `_WORK/W1_10.md`; no invented LinQ API.

## W1_11 — Latency, clocks, freshness

Question: What exactly starts and ends each time measurement? Decision: timestamp contract for file/RTSP/remote LinQ. Read MLPerf inference source/guidance, TensorRT performance guidance, primary clock/synchronization docs. Submit versus completion, warmup/cold, batch/concurrency, transfers, percentiles, clock domains and sync error. Frame age versus compute latency, throughput versus live freshness. Device timing only with verified mechanism. Output `_WORK/W1_11.md`.

## W1_12 — Load, degradation, availability and coverage

Question: Can lower false alert count merely reflect less analysis? Decision: joint quality/load report. Primary loadgen/scenario definitions and failure-accounting evidence. Multi-stream rate/resolution/concurrency/bursts, timeouts/network failure/reconnect, successful/failed/dropped requests, camera-time coverage. Define workload matrix, counts reconciliation, latency with failure rates, observed versus unobservable periods. No architecture implementation. Output `_WORK/W1_12.md`.

## W1_13 — Small samples, uncertainty and paired comparisons

Question: What uncertainty can few cameras/episodes support? Decision: comparison and honest claim. Read https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html and primary proportion/rate/paired methods. Population and resampling unit, clustered/paired bootstrap, zero errors, one positive, repeated selection/seeds, annotation/domain uncertainty. Official API does not solve dependent frames. Numerical examples labeled mathematical, not model tests. Output `_WORK/W1_13.md`.

## W1_14 — Error analysis and causes of improvement

Question: Which diagnosis changes the next engineering step? Decision: error taxonomy and controlled ablations. Primary TIDE paper/source and related detection error methodology. Localization/class/missing person/association/temporal/geometry/annotation/export/transport/UI; stratified error samples and sampling weights. Oracle component tests and paired controlled changes, alternative causes and limits of screenshots. Output `_WORK/W1_14.md`.

## W1_15 — Harness, demonstration and official evidence

Question: What reproducible harness is useful during 45-hour hackathon and what official evidence exists now? Decision: honest demonstration and LinQ execution proof. Open official https://hackathon2026.otkroimosprom.ru/ and relevant rules https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf (only relevant timing/assessment claims); inspect https://lin-q.ru/tech and https://lin-q.ru/sol for actual available SDK/timing/execution evidence, distinguish access failure from missing capability. Manifest, annotation/prediction/config/timestamp/artifact hashes, smoke/regression/demo/independent evaluation; compact diagnostic cases. Output `_WORK/W1_15.md`. Do not invent full case or device access; no exhaustive competition-regulation research.
