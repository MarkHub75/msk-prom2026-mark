---
topic: case_analytics
scope:
  - Audience, work processes, UX problems, comparable digital products, and adoption conditions for the supplied LinQ industrial video-safety case.
  - Decision support for a five-person hackathon team, 23-25 October 2026, with submission due 25 October at 10:00 Europe/Moscow.
  - Documentary research completed in eight first-wave branches, independent criticism, and six second-wave branches; compressed from the final Russian report and normalized evidence.
not_covered:
  - Actual application, detector, slide deck, production installation, user study, or industrial pilot.
  - Verified model conversion, SDK compatibility, LinQ access, throughput, or operational latency; these belong to linq_platform and model_stack.
  - Dataset selection and training implementation, full architecture, procurement quotation, legal approval, or causal injury-reduction evaluation.
answers:
  - question: What does the supplied case actually require, and which features are optional?
    section: case-contract
  - question: Who should receive an event, act on it, own the rule, buy the system, and be consulted?
    section: audience-and-process
  - question: Which UX problems have evidence, and what do the supporting studies actually establish?
    section: ux-problems
  - question: What do Russian and international alternatives document or claim, and what remains unknown?
    section: product-comparison
  - question: What observable evidence is needed for each of the eight PDF examples?
    section: scenario-semantics
  - question: Which documented interaction patterns are transferable, subject to testing?
    section: ux-patterns
  - question: Which injury statistics, prices, and economic calculations can be used without overstating them?
    section: statistics-and-economics
  - question: What worker-trust, data-route, publication, and legal conditions constrain deployment?
    section: deployment-and-trust
  - question: What is the conditional minimum, and when should H-A or H-B be rejected?
    section: minimum-and-hypotheses
  - question: How should UX, deduplication, detection, response, and labor effects be checked?
    section: verification-and-metrics
  - question: What can the team demonstrate to the jury, and which answers are still needed from owners?
    section: jury-and-handoff
keywords:
  - LinQ
  - case_analytics
  - industrial safety
  - occupational safety
  - OHS
  - EHS
  - PPE
  - CCTV
  - human verification
  - duplicate suppression
  - episode matching
  - H-A
  - H-B
  - K007
  - K008
  - Vizorlabs Platform 4.0
  - IVA CV
  - PromVision
  - Vmx SILA:HSE
  - NVI owl.Guard+
  - Macroscop
  - TRASSIR
  - Intenseye
  - Protex AI
  - Voxel
  - viAct
  - Norilsk Nickel
  - SIBUR
  - Severstal
  - EVRAZ
  - Rosstat
  - Rostrud
  - SH17
entity_schema:
  product_comparison:
    representation: Markdown tables in the product-comparison section
    columns:
      - Product / type
      - Input / deployment
      - Observable classes
      - Human workflow / integration
      - Access / price / LinQ
      - Evidence / limits
    missing_value: UNKNOWN means not established in the studied material, never proof of absence.
takeaways:
  - The proposed primary user is the appointed event recipient for one site area; a separate dispatcher, exact buyer, shift coverage, and willingness to pay remain unverified.
  - Complete one mandatory path first, including actual LinQ inference, one alert per episode, persistence, and four filters; a full EHS workflow is outside the hackathon minimum.
  - Vizorlabs 4.0 already documents real-time classification and history; IVA claims LinQ support and has presented a LinQ hardware-software package. Neither human review nor LinQ alone is unique.
  - H-A is lying posture rather than falling or unconsciousness; H-B is presence in a zone active by configuration, not hazardous proximity to moving machinery. Both are HYP and NOT RUN.
  - K008 is settled as an internal measurement convention, with U/X, one-to-one matching, all-reference response denominators, and separate hours and cash; real measurements remain open.
  - No measured UX superiority, current comparable full LinQ price, willingness to pay, causal injury reduction, or production readiness has been established.
checked_at: '2026-10-23T17:33:27+03:00'
checked_at_scope: Local compression artifact check; external evidence retains its recorded 23 October 2026 reading dates and access limits.
timezone: Europe/Moscow
context_version: mosprom-research-v1
case_material:
  status: Supplied local PDF received; all 20 pages visually checked by the orchestrator in the recorded research process.
  source: SOURCES.md#s001
  notes: _WORK/CASE_NOTES.md
  publication_date: Unknown; file creation metadata is not publication evidence.
  public_url_of_local_copy: Not established.
actually_checked:
  inherited_evidence: Source access and reading limits are preserved from the research branches; 184 canonical sources, 259 fact cards, 64 questions, and 11 verification or arithmetic examples.
  compression_work: Final Russian report, editor handoff, consolidated fact and criticism records, source provenance, open questions, and local artifact structure were consulted; no new web evidence was obtained.
  own_artifact: YAML parsing, required metadata, answer-section mapping, declared catalog columns, canonical IDs, local files and anchors, saved-source URL provenance, text hygiene, and final-root inventory checked during creation.
  not_run: Interviews, user tests, product operation, LinQ inference, prototype benchmarks, industrial pilot, and causal effect evaluation.
human_report: report_human_case_analytics.md
evidence_files:
  sources: SOURCES.md
  facts_and_examples: RAW_FACTS.md
  criticism_and_corrections: CRITIC.md
open_questions: OPEN_QUESTIONS.md
compression_notes: _WORK/COMPRESSION_NOTES.md
---

# LinQ case analytics: decisions, evidence, conditions

Start with one observable safety scenario in one production area, an appointed event recipient, an authorized responder, and an OHS rule owner. This is an **INF/HYP recommendation**, not a validated user assignment. Complete the mandatory technical path before adding a corporate incident-management system. Existing products already document many proposed features; the defensible differentiation is a testable quality of a specific path, with no superiority result yet. [F255](RAW_FACTS.md#f255), [F256](RAW_FACTS.md#f256).

Evidence labels: **DOC** = document content; **VENDOR** / **CUSTOMER** = interested-party self-report; **MEAS** = external published measurement; **LOCAL** = recorded local access/artifact observation; **INF** = research inference; **HYP** = untested proposal; **UNKNOWN** = not established. Documentation establishes an interface or stated condition, not usability, installation, Russian availability, or compatibility with the issued LinQ. Copies, mirrors, converted PDFs, and repeated readings do not create independent evidence. All proposed real-world checks are **NOT RUN**. F/S/Q/E links resolve into the normalized [facts](RAW_FACTS.md), [sources](SOURCES.md), [questions](OPEN_QUESTIONS.md), and examples; [criticism](CRITIC.md) preserves both the original objections and second-wave corrections.

<a id="case-contract"></a>
## Case contract: required path, optional features, actual access

**DOC/LOCAL:** The supplied 20-page raster PDF has been found and visually checked by the orchestrator. This compressor relies on the saved reading, rather than claiming a new visual inspection. The local copy is 8,320,969 bytes; SHA-256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Its publication date and a public URL of this exact copy are unknown; creation metadata dated 15 October 2026 is not proof of publication. [S001](SOURCES.md#s001), [CASE_NOTES](_WORK/CASE_NOTES.md).

Page 13 requires: camera streams **or** thematic images; neural recognition; an operational notification containing a frame/clip, camera, time, and type; strictly one notification per violation; a persistent journal with type/camera/zone/time filters; **actual inference on LinQ with speed measurements**. The PDF allows WEB or local GUI; the team's broader instruction retains WEB. Priority scenarios may be selected. Duplicate suppression is mandatory despite also appearing in the optional list. Configurable zones, operator confirmation, dashboard, and multiple streams are optional. The prompt paraphrase adds search; the PDF literally specifies the four filters. A zone filter does not by itself require a polygon editor. [DOC, F254](RAW_FACTS.md#f254).

Page 19 defines analytics through three areas: target/potential audience, UX problems, and other services/experience of comparable digital products. Model architecture alone does not satisfy these. The event regulation specifies integer scores 0-3 per criterion; the slide supplies no numeric weights, and seven maxima do not establish the aggregation rule or guaranteed points. [F153](RAW_FACTS.md#f153), [regulation S134, §§6.1-6.4.7](https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf).

The five-person team's approximately 45-hour development window ends on 25 October 2026 at 10:00 Moscow time. The research therefore recommends one complete path, without invented implementation-hour estimates. Still images are allowed but cannot prove running, immobility over an interval, episode ending, or repeat-alert suppression. The organizers' promise of a remote VM/inference service is not evidence of this team's access, SDK compatibility, or successful execution. Live input, replay processing, and selected-image demonstrations must be labeled separately; video timeline time differs from processing wall time. [F254](RAW_FACTS.md#f254), [F256](RAW_FACTS.md#f256), [Q061](OPEN_QUESTIONS.md#q061).

<a id="audience-and-process"></a>
## Audience and process: conditional users, actual Russian routes, pilot selection

**INF/HYP:** Appoint the first recipient at area level; let a foreman/shift supervisor or another authorized person act, and OHS own rules and periodic review. One person may combine roles. A new dispatcher is justified only if there is an attended post and a demonstrated triage need. The buyer is the organization through its authorized budget holder; neither the exact title nor willingness to pay has been established. IT/security can gate adoption without holding the budget. [F020](RAW_FACTS.md#f020), [F238](RAW_FACTS.md#f238), [F255](RAW_FACTS.md#f255), [Q055](OPEN_QUESTIONS.md#q055).

| Role | Need and information | Proposed usage cadence | Authority / unresolved question |
|---|---|---|---|
| First recipient: existing operator, dispatcher, or foreman | Locate and interpret a current event; frame/clip, area, camera, time, rule, source state | Per event; throughout a shift only at an existing attended post | Who watches which device/channel, with what competing tasks and backup? |
| Foreman / shift supervisor | Contact the area, assess and execute the authorized response, report outcome | Per event and unfinished-event handover; continuous WEB use is not assumed | Who can stop work, call help, or change working conditions? |
| OHS specialist / rule owner | Link the observable rule to local instructions, review ambiguity and recurrence | Daily in the case scenario; configuration on change, periodic analysis | Who approves rules, and where are corrective actions tracked? |
| Worker / driver / contractor | Understand the rule, explain context, report a hazard or error | Affected during covered work; may never log into WEB | How can a person see evidence and challenge an error without an account? |
| OHS service / lawyer / investigation participants | Recover original material and decision history, compare other evidence | On dispute, audit, request, or investigation | Who accesses originals, retains/exports evidence, and records corrections? |
| Management / possible sponsor | Decide on interventions and pilot continuation using coverage, checked events, actions, workload, and TCO | Regular review, exceptional serious cases | Who authorizes spending and acceptance criteria? |
| IT / integrator / information security | Connect and support cameras, model, LinQ, storage, delivery; distinguish failure layers | Setup, changes, failures, maintenance | Versions, locations, logs, support ownership, network constraints? |

These are scenario-based cadences, not observed usage measurements. Seven roles do not imply seven separate interfaces. Workers remain affected stakeholders without being interface users. An accident investigation uses a legally constituted commission and multiple evidence sources; a CV label is not its conclusion. Employer/OHS/worker responsibilities and the OHS-service rule for production employers with more than 50 workers support differentiated authority, not identical structures in a workshop and a holding. Hazardous-facility production control is a distinct regime. [DOC/INF, F001](RAW_FACTS.md#f001), [F004](RAW_FACTS.md#f004), [F006](RAW_FACTS.md#f006), [F009](RAW_FACTS.md#f009), [F255](RAW_FACTS.md#f255).

**CUSTOMER/DOC: three different Russian routes, not one observed national as-is.**

- **Norilsk Nickel:** its 2023 annual report describes an automatic PPE card → manager → OHS/industrial-safety coordinator → administrative decision and behavioral audit with the worker. The first routing recurs in 2024. The exact first job title, emergency-response time, and final closure authority are unknown. A separate 2021 Kola MMC item describes autonomous processing without an operator; do not fuse different sites/years. [F173](RAW_FACTS.md#f173), [F174](RAW_FACTS.md#f174), [F175](RAW_FACTS.md#f175), [F176](RAW_FACTS.md#f176), [2023 S009](https://ar2023.nornickel.ru/ru/business-overview/innovation-digital-technologies.html), [2024 S151](https://ar2024.nornickel.ru/ru/business-overview/innovation-technologies.html).
- **SIBUR:** a first-party article dated 8 October 2026 describes existing technologists/process operators receiving several production data sources; the system selects the camera needing attention. Its pipeline can display video, sound, or email, without proving all channels active for each class. Another loading-rack example has interim control and escalation but concerns production logistics, not an established harness-alarm protocol. New alerts compete with process-control work. [F177](RAW_FACTS.md#f177), [F178](RAW_FACTS.md#f178), [S154](https://habr.com/ru/companies/sibur_official/articles/1091944/).
- **Severstal:** SOVA video analytics feeds the existing KOT corporate system. The integrator describes a Checks module, notifications, and deadlines; the client independently confirms the integration and camera/zone customization. First recipient, closure author, and full API fields are unknown. A risk manager testing one shop is not thereby every alarm's recipient or the buyer. [F179](RAW_FACTS.md#f179), [F180](RAW_FACTS.md#f180), [F181](RAW_FACTS.md#f181), [F182](RAW_FACTS.md#f182), [integrator S010](https://sms-it.ru/iskusstvennyj-intellekt-kompyuternoe-zrenie-i-erm-kot/), [client S155](https://t.me/s/severstal/5198).

**INF/HYP as-is reconstruction:** a person monitors cameras alongside other tasks or receives a worker report, locates/contextualizes the hazard, contacts a supervisor/responder, and records the outcome in an existing tool or an additional record. Public sources confirm fragments, not this complete sequence at the target site. Historical security-CCTV evidence of archive search competing with current work is not a measured prevalence in Russian factories. Severstal already has integrated digital accounting; assuming universal paper-only records is wrong. [F045](RAW_FACTS.md#f045), [F179](RAW_FACTS.md#f179).

**HYP to-be:** configure an explainable local rule → deliver an observation → inspect original context → record truth assessment → route to an authorized responder → verify the actual outcome and review recurrence. Treat observation, truth, viewing, ownership, and corrective action as distinct dimensions. “No longer visible” is not “stood up”; “confirmed” is not “accepted responsibility”; email sent is not received/acted upon; “resolved” needs a defined outcome. A small prototype need not implement all dimensions, but must name implemented actions accurately. [F027](RAW_FACTS.md#f027), [F031](RAW_FACTS.md#f031), [F113](RAW_FACTS.md#f113), [F236](RAW_FACTS.md#f236), [F237](RAW_FACTS.md#f237).

**INF pilot segment:** choose local hazard importance **and** video observability **and** an available useful action. A stable workshop/production-warehouse view with a clear rule and appointed foreman is a candidate, not the proven most profitable industry. Metallurgy, mining, and petrochemicals have documented deployments but substantial infrastructure/security/integration requirements. Transport areas offer visible route conflicts, while dynamic proximity is harder than polygon entry. Construction and temporary repairs change geometry/connectivity more often. Food/packaging hygiene may mean another task and buyer. Small firms combine roles; medium sites need area/shift routing; holdings need access, shared definitions, and integration. Camera count determines infrastructure partly; human load depends on useful/false/duplicate event flow and competing tasks. No TAM, paid-customer count, or industry profitability ranking is established. [F011](RAW_FACTS.md#f011), [F064](RAW_FACTS.md#f064), [F100](RAW_FACTS.md#f100), [F149](RAW_FACTS.md#f149), [F255](RAW_FACTS.md#f255).

Pilot entry conditions are proposed, **NOT RUN**: rule owner; primary/backup recipients; authorized response; explainable rule; visible scene under agreed conditions; lawful material/data route; independent checks including non-alert video; baseline, workload, and continuation criteria agreed before results. Verify the last real event end-to-end, including night shift, false alarm, recipient absence, and existing EHS. Obtain an anonymized card and real routing artifact rather than general approval of AI. [F152](RAW_FACTS.md#f152), [F238](RAW_FACTS.md#f238), [F242](RAW_FACTS.md#f242), [Q055](OPEN_QUESTIONS.md#q055).

<a id="ux-problems"></a>
## UX problems: evidence, causal reasoning, proposed functions, checks

### Attention competition: an event pointer can reduce search, subject to testing

**MEAS/DOC:** A universal attention collapse after 20-30 minutes is not established. HSE uses such guidance for intensive CCTV observation of river-rapids rides, a specific task. A South African CCTV experiment had 42 professional operators from six organizations view one 90-minute industrial compilation with 18 subtle theft targets of four types: mean detection was 55%, without a significant overall decline in that group. Combined analysis with 31 students found decline between the first two half-hour periods in less-experienced groups; specialists maintained performance for an hour and improved in the last period. Volunteer selection, experience/education differences, theft task, and one camera limit transfer. Neither a universal fatigue timer nor immunity to fatigue follows. [F040](RAW_FACTS.md#f040), [F041](RAW_FACTS.md#f041), [F042](RAW_FACTS.md#f042), [F043](RAW_FACTS.md#f043), [F044](RAW_FACTS.md#f044), [study S031](https://ro.ecu.edu.au/ecuworkspost2013/922/), [HSE S032, Appendix 1 §7](https://www.hse.gov.uk/entertainment/assets/docs/health-safety-river-rapids-rides.pdf).

Keval/Sasse observed/interviewed 13 managers and 38 operators in 13 UK CCTV rooms during approximately 4-5-hour visits in 2005-2006. Configuration, image quality, integration, unfamiliar territory, communication, and retrospective/current-task competition constrained work. This qualitative historical security setting does not estimate current Russian industrial frequency. [MEAS, F045](RAW_FACTS.md#f045), [S033](https://discovery.ucl.ac.uk/id/eprint/19823/).

**INF/HYP chain:** competing tasks → need a locator rather than constant manual scanning → event queue with area/camera/time and direct original evidence → expected less search/switching → compare correct place/action identification, important misses, interruption recovery, and time under equal material/coverage/tasks. No measured labor substitution or whole-shift time saving. SIBUR supplies a current example of a busy existing operator, not a measured prototype effect. [F020](RAW_FACTS.md#f020), [F120](RAW_FACTS.md#f120), [F152](RAW_FACTS.md#f152), [F177](RAW_FACTS.md#f177).

### False and duplicate alerts: separate wrong observations from repeated true episodes

**DOC/MEAS:** Milford Haven presented two operators with 275 alarms in the last 11 minutes before the explosion; HSE identifies overload, poor priority, and uninformative alarms. Its chemical-process guidance is not LinQ-operator capacity. In a simulated X-ray task with 122 professional screeners, false-alarm rate 20% and PPV 0.3 accompanied ignoring roughly half the true automation alarms on difficult targets. Conversely, an observational study of 495 conflict alerts at five air-traffic facilities, 45% false, found no expected neglect of true alerts or slower response; controllers often acted before the alert. Different denominators/tasks prevent a universal “X% false means no trust” threshold. [F047](RAW_FACTS.md#f047), [F051](RAW_FACTS.md#f051), [F052](RAW_FACTS.md#f052), [HSE S034](https://www.hse.gov.uk/pubns/chis6.pdf), [screening S037](https://pubmed.ncbi.nlm.nih.gov/32342885/), [aviation S038](https://journals.sagepub.com/doi/pdf/10.1177/0018720809344720).

**INF/HYP chain:** false cards waste checks; duplicate true cards repeat decisions and inflate counts → need one identifiable episode and reviewable errors → define onset/continuation/end/re-arm and retain rejection reasons → expected less repeat handling and more interpretable counts → test long event, confirmed ending/re-entry, gaps, second person, track-ID change, and redelivery. A fixed camera-wide cooldown can hide a different person or new hazard. Publish duplicates, false merges, missed references, and review time separately. Expected attention benefit is not injury reduction. [F023](RAW_FACTS.md#f023), [F056](RAW_FACTS.md#f056), [F133](RAW_FACTS.md#f133), [F195](RAW_FACTS.md#f195), [F257](RAW_FACTS.md#f257), [E001](RAW_FACTS.md#e001).

### Context and ambiguity: label the observation instead of guessing a violation

**DOC/INF:** Phone-like device is not necessarily prohibited phone use; a visible harness does not prove attachment; co-occurrence of person/vehicle is not hazardous moving proximity. Macroscop's “fall detection” explicitly detects lying posture rather than the falling process. An abstract on semi-automated CCTV associates reliable confidence information with lower workload, but the accessible record lacks full method, sample size, and effect size; it does not justify arbitrary raw neural confidence percentages. [F046](RAW_FACTS.md#f046), [F050](RAW_FACTS.md#f050), [F091](RAW_FACTS.md#f091), [F197](RAW_FACTS.md#f197), [S036](https://pureportal.coventry.ac.uk/en/publications/semi-automated-cctv-surveillance-the-effects-of-system-confidence/).

**HYP chain:** evidence without task/time context invites guessing → need currentness, original view, rule and uncertainty → neutral observation, source and receipt times, area/camera, original/annotation toggle, clip when available, explicit live/replay and clip-pending state → expected fewer unsupported decisions → test true/false/ambiguous episodes, wrong location/action, original access, and decision time together with clip readiness. Vizorlabs 4.0 documents a 60-second report, 30 seconds before/after, potentially taking 10-15 minutes to prepare. This is a context/wait tradeoff, not an acceptable delay for our critical alert. Deliver initial evidence without silently waiting for the full clip. [F189](RAW_FACTS.md#f189), [F249](RAW_FACTS.md#f249), [Q056](OPEN_QUESTIONS.md#q056).

### Responsibility and saving: viewing, truth, assignment, and resolution differ

**DOC:** XProtect acknowledgement does not close the alarm; PagerDuty separates acknowledgement and resolution; Genetec documents distinct transitions/history/procedures; Vizorlabs classifies the presence of a violation. Safesite assignment to an empty team can leave nobody notified. **HYP chain:** ambiguous status hides the next actor or loses a decision → need explicit saved truth assessment and trace → minimal review result, author/time/history; later accepted assignment, backup, deadline → expected fewer ownerless cases and recoverable decisions → test two participants, interruption, shift change, decision correction, save/reopen, author/time/next-action recovery. Button latency is separate from physical action. Full workflow remains a later pilot scope. [F031](RAW_FACTS.md#f031), [F034](RAW_FACTS.md#f034), [F113](RAW_FACTS.md#f113), [F130](RAW_FACTS.md#f130), [F188](RAW_FACTS.md#f188), [F237](RAW_FACTS.md#f237).

### Silent queues and misleading summaries: coverage is part of the result

**DOC/INF:** Zero events can mean safe work, inactive rule, failed stream/inference/delivery, active filter, or unreviewed data. AxxonSoft documents health monitoring; Genetec shows filtered/all active counts. Intenseye API distinguishes client/vendor false-positive assessments, permits `null`, and quality export includes `sampleSize`: no assessment is not confirmation. **HYP chain:** hidden coverage or denominator → need visible observation boundaries → active filters/reset, explicit failure/empty states, T/F/U/X, valid coverage, and rule version → expected fewer false management conclusions → test disconnected sources, hiding filters, and equal counts with different coverage. Adding cameras or changing thresholds changes event counts without establishing changed risk. Add health/summary after the mandatory path as readiness permits. [F036](RAW_FACTS.md#f036), [F095](RAW_FACTS.md#f095), [F099](RAW_FACTS.md#f099), [F129](RAW_FACTS.md#f129), [F257](RAW_FACTS.md#f257), [alerts S083](https://docs.intenseye.com/docs/v2_alerts/index.html), [quality S084](https://docs.intenseye.com/docs/v2_accuracy/index.html).

<a id="product-comparison"></a>
## Product comparison: Russian and international capabilities with provenance

**Finding:** event queues, evidence, notifications, filters, behavioral categories, human classification, and history are already present in studied alternatives. Neither “analogs only display detections” nor absolute LinQ uniqueness survives the evidence. No comparative usability test or achieved superiority exists. **UNKNOWN never means absent.** Safety-CV produces observations; VMS/PSIM manages video/alarms; EHS manages hazards/actions/investigations; IT incident products supply selected routing patterns. These are distinct comparison layers. [F057](RAW_FACTS.md#f057), [F079](RAW_FACTS.md#f079), [F113](RAW_FACTS.md#f113), [F187](RAW_FACTS.md#f187).

The following two tables follow the declared `product_comparison` schema. Access/price/LinQ uncertainty applies to the concrete studied offer, not every version of a brand. Public API documentation is not an API key or a deployment right.

| Product / type | Input / deployment | Observable classes | Human workflow / integration | Access / price / LinQ | Evidence / limits |
|---|---|---|---|---|---|
| IVA CV / ПромВижн / presented ОТПБ package; CV platform and industrial offer | VENDOR: IP cameras; data center, cloud, edge | VENDOR: PPE, zones, running, phone, lying person, fire/smoke | DOC: current events → details, timeline and camera/type search; VENDOR: pipeline, storage/archive, notifications, roles/API | VENDOR: LinQ hardware support; LinQ package presented June 2026; exact configuration, performance and price UNKNOWN | [F057](RAW_FACTS.md#f057), [F058](RAW_FACTS.md#f058), [F059](RAW_FACTS.md#f059), [F060](RAW_FACTS.md#f060), [F183](RAW_FACTS.md#f183), [F186](RAW_FACTS.md#f186). ПромВижн/package equivalence and complete review→ownership→resolution/re-arm UNKNOWN; guide web text read, original binary and live session not obtained. |
| Vizorlabs Platform 4.0; safety CV | VENDOR: cameras/detectors | VENDOR: contextual PPE, zones, dynamic areas, people under equipment, other classes | DOC: real-time classification, original/annotated evidence, video, saved decision, comments/history, filters, PDF; VENDOR: anti-spam, external channels | Production access, exact package price and issued-LinQ compatibility UNKNOWN | [F061](RAW_FACTS.md#f061), [F062](RAW_FACTS.md#f062), [F187](RAW_FACTS.md#f187), [F196](RAW_FACTS.md#f196). Responder acceptance, verified correction, episode/re-arm contract, immutability and retention UNKNOWN; documented 4.0 flow is not measured usability. |
| Vmx SILA:HSE; industrial CV | VENDOR: cameras plus file/archive upload | VENDOR: PPE, zones, person-vehicle and machinery interaction | VENDOR: photo/video database, history, channels, PDF/Excel; EVRAZ ZSMK pilot routes to dispatcher | VENDOR: estimate from specification/modules/work; perpetual license, rental or project rights; exact price/LinQ UNKNOWN | [F064](RAW_FACTS.md#f064), [F065](RAW_FACTS.md#f065), [F066](RAW_FACTS.md#f066). >98% concerns person detection, without period/protocol; LTIFR/LTAFR claims are not comparable episode accuracy. |
| NVI owl.Guard+; video/sensor industrial editions | VENDOR: existing or selected infrastructure; well/drilling packages | VENDOR: Base PPE, fire/smoke, danger zones; other editions differ | VENDOR: wall, light/sound, WEB journal with evidence, reports/export/email; automatic plus manual verification stated for retrospective GuardRetro | Concrete quote and LinQ compatibility UNKNOWN | [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068), [F069](RAW_FACTS.md#f069). Do not transfer GuardRetro verification to real-time Base; complex automation effects do not isolate PPE detection. |
| Macroscop; VMS with neural modules | DOC: camera/scene requirements differ by module | DOC: PPE/workwear, phone, lying posture | DOC: boxes, journal events, zone/condition automation | Concrete deployment/TCO and LinQ UNKNOWN | [F070](RAW_FACTS.md#f070), [F071](RAW_FACTS.md#f071), [F072](RAW_FACTS.md#f072), [F091](RAW_FACTS.md#f091), [F094](RAW_FACTS.md#f094). Falling process explicitly excluded; full safety review workflow and episode deduplication UNKNOWN in read chapters. |
| TRASSIR; VMS/analytics | VENDOR: video modules; script extension | VENDOR: helmets, people/vehicles in zones, workplace schedules | VENDOR: client/email/SMS/Telegram notices; history/reports in UAE case | Per-channel licensing identified; numeric current price and LinQ UNKNOWN | [F074](RAW_FACTS.md#f074), [F075](RAW_FACTS.md#f075), [F076](RAW_FACTS.md#f076), [F150](RAW_FACTS.md#f150). Anonymous UAE four-month pilot is supplier-reported; no quality protocol; specific NVI/TRASSIR card unreadable. |
| VisionLabs; platform | VENDOR: industrial video analytics | VENDOR: PPE, zones, lying persons, fire/smoke | Ready OHS human-response route UNKNOWN | Concrete package/price/LinQ UNKNOWN | [F077](RAW_FACTS.md#f077). Class catalog is not an implemented correction workflow. |
| PetrSU system; specific project | Project description: 15 Axis cameras | Claimed helmet/mask recognition | Operator alarm, electronic journal, email to area responsible person described | Customer, period, price and LinQ UNKNOWN | [F078](RAW_FACTS.md#f078). Public independent measurements UNKNOWN. |

Direct Russian materials: [IVA platform S046](https://ivacv.ru/platforma/), [IVA package S045](https://ivacv.ru/когнитив-солюшнс-представили-свой-па/), [IVA guide S158](https://ivacv.ru/wp-content/uploads/2026/05/Руководство-пользователя-сайт.pdf), [Vizorlabs guide S160](https://cloud.lpi.pro/index.php/s/0dRdJ7tPdxtqa5D/download), [Vmx S052](https://videomatrix.ru/solutions/prombezopasnost/), [NVI S055](https://www.nvi-solutions.ru/products/), [Macroscop S058](https://doc.macroscop.com/analytics/hard-hats/overview.htm), [TRASSIR S062](https://solutions.trassir.ru/videoanalitika), [VisionLabs S065](https://visionlabs.ru/solutions/promyshlennost), [PetrSU S066](https://ai.petrsu.ru/projects/project/protection).

**DOC, Vizorlabs 4.0 detail:** Operational Control uses yellow/white rows for unviewed/viewed; truth classification is a different action. A card begins “Не проверено”; changing the decision and pressing “Применить” saves it, unlike closing without saving. Original/annotation, zoom, video, neighboring cards, comments, and history are documented. The verification report uses the latest decision; full history retains changes; third-party-system actions are excluded from that report. Sending to a camera's responsible person/external system does not prove task acceptance. The direct operational-list→card path is not documented step-by-step, and click count/time are not measured. Preserve this distinction when proposing a review/history advantage. [F187](RAW_FACTS.md#f187), [F188](RAW_FACTS.md#f188), [F189](RAW_FACTS.md#f189), [F190](RAW_FACTS.md#f190), [F191](RAW_FACTS.md#f191), [F192](RAW_FACTS.md#f192), [F193](RAW_FACTS.md#f193), [S160, pp.22-25 and 58-66](SOURCES.md#s160).

**Russian deployment evidence, not independent causal trials:** Vmx/EVRAZ ZSMK describes three pilot locations, existing cameras, mesh-fence difficulty, and dispatcher alerts; evaluation duration/independent acceptance/episode precision-recall are unknown. NVI/Gazprom Neft describes integrated video/sensors at a well pad; planned expansion by end-2025 does not prove completion. Kola NPP's first-stage 40-camera switchgear deployment comes from a secondary card; Rosatom's original was not obtained, and “10-fold reduction” lacks method. EYECONT's December 2022 metallurgy pilot describes adaptation with developer/integrator, without public accuracy/price/buyer. A 1C EHS project documents 50 workstations, launch 26 December 2025, corporate integrations, and formerly fragmented tools/paper; it is EHS rather than CV/LinQ, and effect percentages lack methods. [F015](RAW_FACTS.md#f015), [F065](RAW_FACTS.md#f065), [F069](RAW_FACTS.md#f069), [F079](RAW_FACTS.md#f079), [F082](RAW_FACTS.md#f082), [F087](RAW_FACTS.md#f087), [F089](RAW_FACTS.md#f089), [Vmx case S053](https://videomatrix.ru/o-bezopasnoj-rabote-sotrudnikov-evraza-teper-zabotitsya-vmx-videoanalitika/), [Kola secondary S075](https://dtc.techart.ru/public/democases/?action=view&id=1593), [1C project S070](https://solutions.1c.ru/projects/1369685/).

| Product / type | Input / deployment | Observable classes | Human workflow / integration | Access / price / LinQ | Evidence / limits |
|---|---|---|---|---|---|
| Intenseye; safety CV | VENDOR: existing RTSP/H.264 cameras, EHS/IT setup; privacy/no-identification policy | VENDOR: running, climbing, worker-vehicle proximity, harness worn/attached | DOC: structured alerts, filters, separate false-positive assessments and quality export | Demo form; no operated account or API key; exact current quote, Russian procurement and LinQ UNKNOWN | [F095](RAW_FACTS.md#f095), [F101](RAW_FACTS.md#f101), [F116](RAW_FACTS.md#f116), [F158](RAW_FACTS.md#f158). “95 correct alerts in 100” is a target, not universal measured quality; small-PPE visibility constrained. |
| Protex AI; safety CV plus separate Signal physical response | VENDOR: indoor CCTV, edge inference, cloud metadata/event clips; metadata-only option | VENDOR: zone/speed/direction, behavioral risks, phone calls during attention-demanding work | VENDOR: shadow mode, thresholds, repeat suppression, review, investigation/training | Demo form; no operated account; current quote, Russian procurement and LinQ UNKNOWN | [F103](RAW_FACTS.md#f103), [F104](RAW_FACTS.md#f104), [F105](RAW_FACTS.md#f105), [F106](RAW_FACTS.md#f106), [F107](RAW_FACTS.md#f107), [F117](RAW_FACTS.md#f117). Two-week shadow mode/99% precision are supplier procedure, not our acceptance result; edge still permits off-site data. |
| Voxel; safety CV | VENDOR: cameras; installation/line-of-sight dependence | VENDOR: speeding, no-stop, unsafe proximity, pedestrian zones | VENDOR: corrective measures, investigation and coaching/training | Exact current quote, Russian procurement and LinQ UNKNOWN | [F108](RAW_FACTS.md#f108), [F109](RAW_FACTS.md#f109), [F119](RAW_FACTS.md#f119). Supplier outcome cases lack published counterfactual protocol; automatic vehicle control needs separate safety engineering. |
| viAct / viHUB; CV plus broader site platform | VENDOR: CCTV/IP RTSP; IoT/BIM/ePTW layer; separate wearable offers | VENDOR: smoking, zones, proximity, under suspended load, fall/immobility | VENDOR: alerts, photo/video, journal; broader integrations | Exact current quote, Russian procurement and LinQ UNKNOWN | [F110](RAW_FACTS.md#f110), [F111](RAW_FACTS.md#f111), [F118](RAW_FACTS.md#f118), [F203](RAW_FACTS.md#f203), [F207](RAW_FACTS.md#f207). Geometry/small-object/class-quality conditions UNKNOWN; direct W2 man-down material not obtained; wearables are not CV-only. |
| Everguard / SeAH; sensor-fusion safety program | 2022 announcement: edge video plus sensors and wearables | Claimed high-risk zones, cranes, PPE, fall, SOS | Portal for review/coaching described | Concrete current delivery, price, Russian procurement and LinQ UNKNOWN | [F112](RAW_FACTS.md#f112), [F207](RAW_FACTS.md#f207). Announced multiyear program, not verified current completion or quantified effect; not camera-only. |

Direct global materials: [Intenseye FAQ S014](https://www.intenseye.com/resources/faq), [Protex privacy S090](https://www.protex.ai/guides/privacy), [Voxel S106](https://www.voxelai.com/industry-insights/pit-safety-monitoring-software-warehouses), [viHUB S097](https://www.viact.ai/vihub), [Everguard/SeAH S098](https://www.prnewswire.com/news-releases/seah-changwon-integrated-special-steel-and-everguardai-partner-to-enhance-worker-safety-with-worker-centric-ai-301549470.html).

**Customer/supplier outcomes retain their provenance and units:**

- **Swire Coca-Cola 2022 CUSTOMER report:** Intenseye on 20 Hong Kong SAR cameras; vests/speed/zones; safety alerts decreased by more than 60% over a year. Baseline/end counts, exposure normalization, unchanged rules, and control group are not supplied; leadership, training, privacy consultation and worker concerns are part of the program. This establishes adoption and reported alert change, not model-caused injury reduction. Supplier “27% lost day rate” was not corroborated on the read client page and is not merged with the 60%. [F100](RAW_FACTS.md#f100), [F101](RAW_FACTS.md#f101), [F102](RAW_FACTS.md#f102), [S087 pp.72-75](https://corpweb.swirecocacola.com/sbcorpweb/uploads/docs/SCC_SR2022_Full_EN.pdf).
- **DHL CUSTOMER release:** confirms a Protex PoC at DHL Global Forwarding Denmark; read material gives no cameras, duration, or injury effect. **M&S Castle Donington VENDOR case:** video examples changed temporary-worker induction/training; “80% reduction incidents” mixes incidents and unsafe events, lacks counts/exposure, and uses ten weeks in the headline versus three months in the text. It is not 80% fewer injuries or evidence for a specific phone/conveyor detector. [F105](RAW_FACTS.md#f105), [F106](RAW_FACTS.md#f106), [F206](RAW_FACTS.md#f206), [DHL S092](https://group.dhl.com/content/dam/deutschepostdhl/en/media-relations/press-releases/2023/pr-dhl-innovation-center-troisdorf-20231129.pdf), [M&S S091](https://www.protex.ai/case-studies/marks-and-spencer).
- **Voxel VENDOR cases:** Carlex reports vest/no-stop improvements in under three months; Americold reports 70% fewer injuries, 288 → 0 lost-time days, and $1.1 million savings. Technology coincides with coaching/culture changes; baseline proportions, exposure and counterfactual are unpublished. **viAct/Alliad VENDOR:** PPE deviations −41.7%, danger-zone intrusions −46.3% in the first three months, without counts/cameras/exposure. These are possible behavior outcomes to define, not Russian ROI inputs or independent UX evaluations. [F108](RAW_FACTS.md#f108), [F109](RAW_FACTS.md#f109), [F110](RAW_FACTS.md#f110), [Carlex S094](https://www.voxelai.com/customer-stories/carlex), [Americold S095](https://www.voxelai.com/customer-stories/americold-saved-1-1m-annually-and-reduced-injures-by-70), [Alliad S096](https://www.viact.ai/case-studies/alliad-cuts-ppe-deviations-with-viact-ai).

Researchers did not operate gated Protex/Intenseye consoles or view closed demo videos. Privacy pages offer design choices, not approval of a Russian processing route. IVA's LinQ support is a counterexample to a blanket “all Russian analytics requires NVIDIA” claim, without proving our runtime or stream capacity. [F058](RAW_FACTS.md#f058), [F098](RAW_FACTS.md#f098), [F107](RAW_FACTS.md#f107), [F158](RAW_FACTS.md#f158), [F159](RAW_FACTS.md#f159).

<a id="scenario-semantics"></a>
## Scenario semantics: eight PDF examples are different observational tasks

**INF/HYP definitions, not eight implementation commitments:** each class must match visible evidence and local rules; a supplier category proves an offer, not quality on this camera. [F197](RAW_FACTS.md#f197), [F199](RAW_FACTS.md#f199), [F200](RAW_FACTS.md#f200), [F201](RAW_FACTS.md#f201), [F202](RAW_FACTS.md#f202), [F203](RAW_FACTS.md#f203), [F204](RAW_FACTS.md#f204), [F207](RAW_FACTS.md#f207).

| PDF example | Required observation / context | Studied analog basis | Boundary / counterexample |
|---|---|---|---|
| Running / abrupt movement | Motion sequence; geometry for physical speed | VENDOR: Intenseye running, Protex speed/direction | Fast walk, running in place, camera motion; a still image has no speed |
| Hazardous proximity to moving machinery/vehicle | Person, vehicle/machine motion and unsafe approach over time | VENDOR: Intenseye, viAct; Henkel application on supplier material | Co-occurrence or box overlap does not prove hazardous physical distance |
| Phone while working/moving | Visible device interaction plus task context | DOC: Macroscop; VENDOR: Protex phone calls | Radio, scanner, carrying device, permitted stationary use |
| Smoking / open fire outside permitted place | Distinct smoking/flame/smoke cues, prohibited location | VENDOR: viAct smoking; RU fire/smoke catalogs | Steam, welding, drinking, permitted area; smoke alone is not smoking |
| Climbing / under conveyor or suspended load | Body trajectory relative to obstacle or volume beneath active lifting | VENDOR: Intenseye climbing, Protex belts, viAct suspended load | Standing nearby, 2D overlap at a different depth |
| Height work without harness | Defined height operation and required protection; wearing versus attachment | VENDOR: Intenseye worn/attached harness | Hidden anchor/lanyard means unknown, not proven absence |
| Falling / immobility / possible unconsciousness | Fall is transition; lying is posture; immobility is an interval | DOC: Macroscop lying only; VENDOR: general viAct catalog | Floor repair, voluntary lying, mannequin, occluded motion; no medical diagnosis |
| Unsafe load carrying, additional example | Specific operation/rule; visible posture/grip/route where valid | Equivalent not established in four direct analogs studied in W2 | Box size does not establish mass; broad ergonomics is not equivalent |

Direct class sources: [Intenseye S103](https://www.intenseye.com/detection-library), [Protex S104](https://www.protex.ai/safety/behavioural-safety), [viAct smoking S164](https://www.viact.ai/video-analytics-solution/worker-smoking-detection), [proximity S165](https://www.viact.ai/video-analytics-solution/proximity-detection-solution), [suspended load S166](https://www.viact.ai/video-analytics-solution/worker-under-suspended-load-monitoring), [Macroscop S081](https://doc.macroscop.com/analytics/fall-detector/overview.htm).

Macroscop documents head/hand image-size conditions for PPE, visible hands/device plus fixed camera/HD and other conditions for phone, and full-body scale/light/angle for lying posture. These module-specific requirements do not become universally sufficient for our detector. More camera resolution alone does not ensure a small object is distinguishable. Name messages narrowly, e.g. “Person lying; check required” or “Presence in a zone active by configuration”; test whether users understand them. [F071](RAW_FACTS.md#f071), [F092](RAW_FACTS.md#f092), [F093](RAW_FACTS.md#f093), [F094](RAW_FACTS.md#f094), [F198](RAW_FACTS.md#f198), [F199](RAW_FACTS.md#f199), [phone requirements S080](https://doc.macroscop.com/analytics/phone-detection/requirements.htm), [lying requirements S082](https://doc.macroscop.com/analytics/fall-detector/requirements.htm).

<a id="ux-patterns"></a>
## UX patterns: documented mechanics, proposed transfer, testable limits

**INF/HYP:** Transfer an action's meaning and persistence, not only appearance. Familiarity across vendors is not proof of suitability or usability. The minimal first view needs area/camera, observation, source time, evidence, and a clear next step; model details/history can open on demand. Priority uses text/order as well as color, consistent with HSE's caution against color alone. [F048](RAW_FACTS.md#f048), [F120](RAW_FACTS.md#f120), [F134](RAW_FACTS.md#f134).

| Documented pattern | Proposed purpose | Important limit / check |
|---|---|---|
| XProtect visible filters/Clear filter; Genetec filter count and matching/all active X/Y | Show why some events are absent | Find a case and detect/reset the hiding filter. [F121](RAW_FACTS.md#f121), [F122](RAW_FACTS.md#f122), [F129](RAW_FACTS.md#f129) |
| XProtect associated-camera recording; Genetec recording at event time | Open evidence without losing selected event when new ones arrive | Dense table is not proven usable; measure time/context loss. [F120](RAW_FACTS.md#f120), [F131](RAW_FACTS.md#f131), [F135](RAW_FACTS.md#f135) |
| Vizorlabs 4.0 “Не проверено” → decision → “Применить” | Save an explicit assessment instead of ambiguous OK | Check save/reopen, feedback, lost edits, and ambiguous case. [F188](RAW_FACTS.md#f188), [F190](RAW_FACTS.md#f190) |
| Genetec aggregate alarms; Vizorlabs claimed anti-spam | One incident, several observations | Genetec limits by type/location and excludes manual/API triggers; define our episode independently. [F133](RAW_FACTS.md#f133), [F195](RAW_FACTS.md#f195) |
| XProtect/AXIS short instructions; Genetec SOP | Connect class with authorized action | Rule owner approves text; branching workflows/manager process deferred. [F033](RAW_FACTS.md#f033), [F124](RAW_FACTS.md#f124), [F132](RAW_FACTS.md#f132) |
| Genetec On hold with timer | Preserve an unresolved reviewed case and return it visibly | Reviewed-insufficient-evidence differs from unchecked; deadline depends on risk. [F130](RAW_FACTS.md#f130), [F256](RAW_FACTS.md#f256) |
| Genetec Latest activity; Vizorlabs history/PDF | Recover author, corrections, detailed context | Latest-state report differs from full history; immutability unverified. [F134](RAW_FACTS.md#f134), [F138](RAW_FACTS.md#f138), [F191](RAW_FACTS.md#f191), [F192](RAW_FACTS.md#f192) |
| AXIS hotspot; AxxonSoft health | Select a relevant camera and expose failure | Preserve current review; timeout must not steal evidence. [F036](RAW_FACTS.md#f036), [F125](RAW_FACTS.md#f125) |

References: [XProtect S107](https://doc.milestonesys.com/xprotect/xprotect-smart-client/2025r3/en/using-the-alarm-list), [AXIS S110](https://help.axis.com/en-us/axis-camera-station-pro), [Genetec S111](https://techdocs.genetec.com/r/en-US/Genetec-Mission-ControlTM-User-Guide-3.4.1.0/User-interface-tour-for-Mission-Control), [aggregate S117](https://techdocs.genetec.com/r/en-US/Genetec-Mission-ControlTM-Administrator-Guide-3.4.1.0/Aggregate-multiple-alarms-associated-with-an-incident?contentId=f3kwV64ttuJtQdPdMywcHA), [AxxonSoft S027](https://my.axxonsoft.com/products/psim/integrations/integrated-monitoring-module).

Bulk confirmation can propagate an incorrect decision; if added, test similar cards with different evidence. HSE handover calls for preparation, two-way exchange, and cross-checking; changing record owner alone is not handover. Both are later process choices, not mandatory hackathon features. [F049](RAW_FACTS.md#f049), [F134](RAW_FACTS.md#f134), [F187](RAW_FACTS.md#f187), [HSE S020](https://www.hse.gov.uk/humanfactors/topics/shift-handover.htm).

<a id="statistics-and-economics"></a>
## Statistics and economics: populations, observability, costs, hours versus cash

**DOC/INF:** Injury burden supports importance, not the camera-observable/preventable fraction or TAM. Rosstat, Rostrud, and ILO have different populations, years, units, and methods. Do not splice them into one trend or sales calculation. [F258](RAW_FACTS.md#f258).

- **Rosstat 2025:** 20.8 thousand injured persons, including 1.07 thousand fatalities; 1.018 and 0.052 per 1,000 workers in the surveyed statistical scope. **2024:** 21.4 thousand and 1.04 thousand respectively. These are rounded people, not accident counts or precise inputs for small changes. Form 7-traumatism is not all Russian employers/workers; footnote excludes Donetsk/Luhansk people's republics and Kherson/Zaporizhzhia regions. Use the surveyed-organization denominator, not total national employment. [F139](RAW_FACTS.md#f139), [F141](RAW_FACTS.md#f141), [F142](RAW_FACTS.md#f142), [S123](https://rosstat.gov.ru/working_conditions), [2025 S124](https://rosstat.gov.ru/storage/mediabank/pr_travm_2025.xlsx).
- **Rosstat incapacity 2025:** 0.96 million person-days, mean 46.1 days per injured person. Method counts qualifying injuries with at least one working day lost whose temporary incapacity ended in the reporting period. Not each injury's duration, employer cash loss, or days this system saves. Full historical applicability of Order 538 to the series is not established. Original XLSX binary was not obtained; researchers used a visually checked PDF conversion. Methodology reading reused an original obtained by an adjacent topic, rather than constituting new network receipt. [F140](RAW_FACTS.md#f140), [F142](RAW_FACTS.md#f142), [F211](RAW_FACTS.md#f211), [S125](https://www.rosstat.gov.ru/storage/mediabank/met_538-30092025.pdf).
- **Rostrud-based 2024 severe-consequence series:** denominator **5,974 cases** in the VNII Truda review, obtained on a municipal mirror; original administrative report was not independently obtained. Shares: fall from height **22.75%**; moving/rotating objects/machines **19.02%**; transport accidents **17.51%**; electric current **3.67%**. These are cases, not Rosstat persons. A camera may observe some height work, interactions, routes, or access, but cannot generally see anchor integrity, physical 2D proximity, every transport location, or electrical voltage. Shares neither sum to preventable-CV burden nor establish individual risk without exposure. Do not reconstruct exact case counts from rounded percentages. [F143](RAW_FACTS.md#f143), [F208](RAW_FACTS.md#f208), [F209](RAW_FACTS.md#f209), [F210](RAW_FACTS.md#f210), [S126 pp.14,17](https://adminbalagansk.ru/download/viewer/ot/21102025.pdf).
- **Excluded industry table:** annual-yearbook table 5.42/page 137 was ambiguous in machine representation and not obtained visually; its industry counts/rates are excluded. No verified industry ranking by per-worker risk or TAM is available. [F212](RAW_FACTS.md#f212), [F214](RAW_FACTS.md#f214), [Q058](OPEN_QUESTIONS.md#q058).
- **ILO report published 2023, modeled year 2019:** approximately **2.93 million** work-related deaths, including about **2.6 million disease deaths** and **330 thousand accident deaths**; more than **395 million nonfatal injuries**. Nonfatal estimates concern absence of at least four days and use modeling for incomplete countries. Not a sum of registered cases or camera-addressable market; most fatal burden is disease. [F145](RAW_FACTS.md#f145), [F146](RAW_FACTS.md#f146), [ILO S127](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@ed_protect/@protrav/@safework/documents/publication/wcms_903140.pdf), [method S128](https://pmc.ncbi.nlm.nih.gov/articles/PMC10927068/).

**UNKNOWN:** The case's 70-80% human-factor claim lacks a recoverable primary measurement. A similar 2017 review percentage lacks reconstructable sample/geography/period/cause coding and an unambiguous original source. Even a proven human-factor percentage would not be the camera-visible share: workload, design, time pressure and organization influence error. A detected class does not establish accident cause or worker guilt. Illustrative case numbers—40%, threefold decrease in a quarter, call for help in 30 seconds—are not measured outcomes or SLA. [F026](RAW_FACTS.md#f026), [F147](RAW_FACTS.md#f147), [F148](RAW_FACTS.md#f148), [review S129](https://fundamental-research.ru/ru/article/view?id=41309), [HSE human failure S041](https://www.hse.gov.uk/humanfactors/topics/humanfail.htm).

**Prices/TCO:** A comparable full industrial LinQ quotation was not established; this limited search result does not prove no public price exists. TRASSIR per-channel licensing had no obtained numeric quote; old indexed QMonitoring tariffs are not a current offer. Vmx uses a project estimate. **1C EHS КОРП:** published at reading, **770,400 RUB** for the base electronic delivery and **61,600 RUB** for one configuration client workplace license, with platform/server licenses additional where applicable. Tax treatment was not established. These are another product layer, not CV per-camera price or deployment TCO. [F066](RAW_FACTS.md#f066), [F081](RAW_FACTS.md#f081), [F150](RAW_FACTS.md#f150), [1C S069](https://solutions.1c.ru/catalog/ehs_compl_corp/buy).

**INF/HYP economic method, K008:** include scene survey/camera changes, compute/network, licenses, storage, integrations, review, rule tuning, support, and training. Existing EHS may cover some activities but integration still costs work. UK HSE social-cost estimates separate cash, quality of life, and cost bearers; they cannot be converted directly into Russian employer savings. [F151](RAW_FACTS.md#f151), [F257](RAW_FACTS.md#f257), [HSE S130](https://www.hse.gov.uk/statistics/economics/eauappraisal.htm), [Q063](OPEN_QUESTIONS.md#q063).

Use two separate calculations under equal period, coverage, and task:

```text
ΔH = H_old - H_new
C = A - P - O
scenario cash = q_saved*w_saved*H_saved - q_added*w_added*H_added - O
```

`H_new` includes review of T/F/U/X, duplicates, escalation, configuration and support **by role**. `A` = actually avoided payments; `P` = new labor payments; `O` = additional nonlabor expense; capital `I` and period are separate. Unchanged salaries do not create cash saving from freed hours. `q_saved/q_added` are the portions of each side's hours that actually change payments; separate wages and coefficients prevent hiding new paid work with an aggregate `q=0`. Historical `q*w*(H_old-H_new)-O` is superseded. Real wages, q, costs and ROI are unknown. [F257](RAW_FACTS.md#f257).

**E011 fictional arithmetic, not prices or product effect:** old task 8 h, new 11 h → workload +3 h. With unchanged pay, no additional labor payments, and O=500 RUB, cash effect is −500 RUB; if those three extra hours are paid at an illustrative 1,000 RUB/h, −3,500 RUB. A different distribution—2 h saved without payment reduction, 5 new paid hours—has the same ΔH=−3 h but −5,500 RUB at that wage/O. Publish workload and payments separately. [E011](RAW_FACTS.md#e011).

Near-term benefit can be tested on comparable task effort with quality/coverage preserved, useful timely actions and recurring-condition discovery. Injury effects need longer observation and a comparison design; rare injuries and concurrent changes preclude causal claims from a short demo or fewer alerts. [F152](RAW_FACTS.md#f152), [F257](RAW_FACTS.md#f257).

<a id="deployment-and-trust"></a>
## Deployment and trust: affected workers, correction, data routes, publication rights

**MEAS:** Electronic performance-monitoring meta-analysis: 94 independent samples, N=23,461; monitoring is associated with more stress, no overall performance improvement, and better attitudes with more transparent/less invasive monitoring. It spans technologies/tasks, not this factory-safety application or proof every deployment harms workers. APA 2023 is an opt-in survey of mixed monitoring technologies. OECD's 2022 survey covered 5,334 workers and 2,053 firms in manufacturing/finance across seven countries; training/consultation associate with better reported outcomes. A 9-percentage-point health/safety-report difference is an association, not consultation's causal effect or 9% fewer injuries. None predicts Russian worker acceptance. [F053](RAW_FACTS.md#f053), [F154](RAW_FACTS.md#f154), [F155](RAW_FACTS.md#f155), [F156](RAW_FACTS.md#f156), [F157](RAW_FACTS.md#f157), [meta-analysis S039](https://onlinelibrary.wiley.com/doi/10.1111/peps.12514), [OECD S135](https://www.oecd.org/en/publications/the-impact-of-ai-on-the-workplace-main-findings-from-the-oecd-ai-surveys-of-employers-and-workers_ea0a0fe1-en.html).

**CUSTOMER:** Norilsk Nickel describes a specialist canceling an incorrect PPE signal, sometimes caused by unfamiliar PPE types. This establishes human correction, not worker-accessible appeal, trust percentage, or complete correction of downstream consequences. Its annual report also mentions administrative routing, positioning and face recognition; Russian safety CV is not universally anonymous or disconnected from personnel decisions. Exact sanctions or automatic punishment are not established. [F229](RAW_FACTS.md#f229), [F235](RAW_FACTS.md#f235), [S182](https://nornickel.digital/cifra_v_nornikele/za_prombezopasnostyu_na_zavodakh_nornikelya_sledit_iskusstvennyjj_intellekt).

EVRAZ's manual “Охота на риски” describes submission, clarification, status, response about measures, push/email, supervisor-mediated and anonymous company-device routes. Its author describes explaining cross-shop reports to managers and people manufacturing minor risks for points. CV was not integrated at that publication. The **2024 report**, printed pp.82-86, separately describes simplified microinjury investigation intended to avoid fear of punishment, refusal of dangerous work, and discipline for cardinal-rule violations. Adjacent video-analytics text does not make this one CV-appeal procedure. [F230](RAW_FACTS.md#f230), [F231](RAW_FACTS.md#f231), [F232](RAW_FACTS.md#f232), [F233](RAW_FACTS.md#f233), [F234](RAW_FACTS.md#f234), [manual system S183](https://habr.com/ru/companies/evraz/articles/816547/), [official report URL S184](https://www.evraz.ru/upload/iblock/a2c/9gimdu0ootuz5gm0b2pe962mvla00uia/EVRAZ_Sustainability_report_2024.pdf).

**Provenance, S184:** direct original access/download failed; W2-06 obtained a Google Viewer representation of the official URL, saved as [EVRAZ_VIEWER.pdf](_WORK/W2_06_MATERIALS/EVRAZ_VIEWER.pdf), 13,675,425 bytes, 117 PDF spreads, SHA-256 `C1FC6E4A3D6293096C8ECB3C4E44B4F6B46F729DC09EC52CF67B45931C1F309C`. Relevant spreads 43 and 45 were rendered/visually read, with text extracted. Byte identity to the 13,634,746-byte original was not established; the AK&M mirror is the same report's copy, not independent evidence. Exact publication day is unknown; reporting year 2024 is not October-2026 practice. The report is no longer wholly unavailable, but remains organizational self-report without a worker's firsthand CV-appeal account. [S184](SOURCES.md#s184).

**UNKNOWN/HYP correction route:** no verifiable Russian worker account tracing a disputed CV episode, original access, record correction and consequence reversal was found in this sample. This is not proof no enterprise has one. Proposed route: neutral “possible dangerous event” → original context → clarification via foreman/OHS → named review with reason/history → reply to affected person → correction of confirmed statistics and linked conclusions. Entire chain **NOT RUN**, not fully documented in a found Russian CV case. A worker account is optional; a usable channel is necessary. No default personnel scoring; promise of no disciplinary use requires real local commitments. Interview worker/contractor separately from foreman/OHS and compare the same episode. [F249](RAW_FACTS.md#f249), [F253](RAW_FACTS.md#f253), [F259](RAW_FACTS.md#f259), [Q054](OPEN_QUESTIONS.md#q054), [Q060](OPEN_QUESTIONS.md#q060).

**DOC research legal framework:** saved researcher readings on cited legal mirrors dated 23 October 2026, not a new legal opinion or clearance. Actual authorized counsel must verify current official edition and applicability to the concrete people, purposes, operations and site. OPO production-control rules, including questions about Rules 2168 chronology, do not automatically apply to any warehouse. [F171](RAW_FACTS.md#f171), [F172](RAW_FACTS.md#f172), [Q064](OPEN_QUESTIONS.md#q064).

- Labor Code Art.214 addresses information about remote recording; Art.86 limits decisions affecting workers based exclusively on automatically processed/electronically obtained data; Art.89 provides information/access/correction; Art.88 governs third-party transfer/internal access. An operator's confirmation click does not prove compliance. [F004](RAW_FACTS.md#f004), [F162](RAW_FACTS.md#f162), [F163](RAW_FACTS.md#f163), [F220](RAW_FACTS.md#f220), [Art.86 S140](https://www.consultant.ru/document/cons_doc_LAW_34683/01f6157ff985b3cbbb50eb88fa6e26f30202532a/), [Art.89 S141](https://www.consultant.ru/document/cons_doc_LAW_34683/dc0a9a9993940d29a8daafe8144d3454c11b92cc/).
- Personal-data law requires purpose, minimization, accuracy, purpose-limited storage, security and an appropriate basis; consent is one basis rather than a universal substitute. External processing needs defined operations/data/purposes/obligations. Biometrics depends on identity-establishment purpose. No face recognition reduces scope but does not remove ordinary personal data: clothing/shift/camera can identify. Blurring is not general permission; no universal factory-video retention period follows. [F164](RAW_FACTS.md#f164), [F170](RAW_FACTS.md#f170), [F215](RAW_FACTS.md#f215), [F223](RAW_FACTS.md#f223), [Art.5 S142](https://www.consultant.ru/document/cons_doc_LAW_61801/96fbc469f91f57235cc842a85e0516a99f23dc85/), [Art.6 S143](https://www.consultant.ru/document/cons_doc_LAW_61801/315f051396c88f1e4f827ba3f2ae313d999a1873/), [Art.11 S144](https://www.consultant.ru/document/cons_doc_LAW_61801/7336c78762a98b5f4f698b8c3800dca1111acc16/).
- LinQ's Russian hardware brand does not locate VM, gateway, backend, object storage, backups, support, logs or recipients. The read edition of Art.18(5) prohibits specified collection-stage operations with Russian citizens' data through foreign databases, subject to exceptions; the obsolete simplification that a “primary Russian write” is sufficient is not used. Cross-border transfer has its own procedure; remote access neither proves nor excludes it. [F168](RAW_FACTS.md#f168), [F222](RAW_FACTS.md#f222), [F223](RAW_FACTS.md#f223), [F228](RAW_FACTS.md#f228), [Art.18 S146](https://www.consultant.ru/document/cons_doc_LAW_61801/cbf4e15b7c330f9372e876cdf2bc928bad7950ef/), [Art.12 S177](https://www.consultant.ru/document/cons_doc_LAW_61801/e4ebbe1780de623c7cf32a59ca82a7bb523a25dd/).
- Closed processing and public display are separate operations. Disclosure to known recipients differs from dissemination to an indefinite audience; image/personality rights differ from file copyright. Public solution-link requirements do not require publishing a production archive. Demonstration, defense recording, screenshots and teaser each need checked material/audience rights. Silence or a person's prior publication of their photograph is not blanket dissemination consent. [F215](RAW_FACTS.md#f215), [F221](RAW_FACTS.md#f221), [F227](RAW_FACTS.md#f227), [Art.10.1 S174](https://www.consultant.ru/document/cons_doc_LAW_61801/591acc70f577873c1ee54765eda110b7a0271eaf/), [Civil Code Art.152.1 S176](https://www.consultant.ru/document/cons_doc_LAW_5142/14c6c3902cffa17ab26d330b2fd4fae28e5cd059/).

**HYP material routes:** prefer a safe, agreed, self-staged sequence with clear processing/display rights; none has been recorded or authorized in this research. Open datasets are a separate alternative, not preapproved. SH17 README states CC BY-NC-SA 4.0 and Pexels provenance/restrictions; the license does not transfer depicted persons' privacy/personality rights, and Pexels prohibits negative portrayal of recognizable people. Labeling stock subjects “violators” needs separate review. GitHub availability does not automatically authorize external inference or public accusatory display. [F224](RAW_FACTS.md#f224), [F225](RAW_FACTS.md#f225), [F226](RAW_FACTS.md#f226), [F243](RAW_FACTS.md#f243), [F248](RAW_FACTS.md#f248), [SH17 S178](https://github.com/ahmadmughees/SH17dataset), [CC S179](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en), [Pexels S180](https://www.pexels.com/license/).

Before an external frame, obtain a material/route passport: file source/rights, depicted people, purpose/basis for each operation, recipients/countries, endpoints, payload/logs/dumps/telemetry, storage/deletion, support access, and separately publication audience. Without it, a diagram and clearly synthetic cards can explain design but do not validate recognition or replace required LinQ execution. [Q047](OPEN_QUESTIONS.md#q047), [Q053](OPEN_QUESTIONS.md#q053), [Q059](OPEN_QUESTIONS.md#q059).

**INF:** CV supports observation and analysis, not substitution for hazard elimination, engineering guards, safe routes or equipment repair. NIOSH prioritizes elimination/substitution/engineering over administrative controls/PPE. Repeated alerts followed only by repeated instruction can leave the cause intact; management review should examine conditions as well as visible behavior. [F055](RAW_FACTS.md#f055), [F161](RAW_FACTS.md#f161), [NIOSH S139](https://www.cdc.gov/niosh/hierarchy-of-controls/about/index.html).

<a id="minimum-and-hypotheses"></a>
## Minimum and hypotheses: K007, H-A, H-B, rejection conditions

**INF/HYP, corrected K007:** the sum of useful enterprise features is too broad for one demonstrable path in 45 hours. The dependency order below is not an implemented MVP or a measured effort forecast. [F256](RAW_FACTS.md#f256), [CRITIC second-wave resolution](CRITIC.md#k007--результат-w2).

| Priority | Concrete result | Dependency and verification |
|---|---|---|
| Mandatory | Lawful input, neural model, actual LinQ execution and speed log | Save input/model/conversion/runtime versions, outputs/logs; a CPU/RTX run does not satisfy LinQ |
| Mandatory | WEB initial evidence with camera/time/type | Measure event→inference→WEB delivery separately; identify replay |
| Mandatory | One persistent episode/initial notification, continuation updates, new event after established ending | Define identity, gaps, ending and re-arm; E001-E006 rather than only cooldown |
| Mandatory | Journal survives reload; type/camera/zone/time filters | E007 and case retrieval; no implied complex zone editor |
| Minimum useful after mandatory | Enough context, saved review result, author/time/history, neutral insufficient-evidence outcome | True/false/ambiguous cards, save/reopen and history recovery; less dependency than multi-actor corrective workflow |
| Next as ready | Visible live/replay, source unavailability, filters, short action guidance | Disconnect/pending-clip/filtered-empty cases; choose by actual readiness |
| Deferred until confirmed need | Accepted assignment/escalation, branching SOP, shift handover, EHS integration, broad roles/reports | Site walkthrough, authorities and acceptance criteria first |
| Unsupported current promises | Predictive risk, personnel rankings, automatic machine stop, universal industry coverage | Different data, safety engineering, authority and trials required |

Never remove unresolved reviewed cases to improve apparent quality: “reviewed, insufficient evidence” is not false or unchecked. A historical note requires saved author/time data, not a decorative label. [F096](RAW_FACTS.md#f096), [F188](RAW_FACTS.md#f188), [F192](RAW_FACTS.md#f192), [F257](RAW_FACTS.md#f257).

**H-A — “Person lying in the controlled area; check required.” HYP, NOT RUN.** Requires a lawful timed sequence, distinguishable full body, unambiguous posture labels, negative examples and a model runnable on the issued LinQ. It is neither the falling transition nor unconsciousness. Add immobility only after separately validating sensitivity to small movements; a stable person box does not establish it. Include sitting/crouching, floor work, moving while lying, partial occlusion and exit/re-entry. Define onset at first eligible positive observation; alert creation follows predeclared `T_on`, a different timestamp. Ending needs observed posture change under `T_clear`; leaving/occlusion gives interrupted observation or unknown end, not “stood up” or hazard resolved. Choose parameters before the run from material/risk rather than a universal few-second hold. Reject/defer if normal floor work is indistinguishable, sequence is absent, or LinQ suitability is unconfirmed. [F197](RAW_FACTS.md#f197), [F198](RAW_FACTS.md#f198), [F256](RAW_FACTS.md#f256), [Q057](OPEN_QUESTIONS.md#q057).

**H-B — “Person enters/is present in a zone active by configuration.” HYP, NOT RUN.** Requires stable camera, validated surface polygon, visible person ground point, known prohibition state, and sequences of entry/dwell/exit/re-entry. Schedule/switch activation is labeled as configuration, not machine-activity recognition. A box crossing a line is not necessarily feet in a floor zone under perspective/multiple levels. Include nearby passage, inactive zone, boundary jitter, hidden feet and second person. Activation around a person already inside is “presence at activation,” not a fabricated crossing. Lost visibility does not prove exit; polygon changes do not rewrite old event evidence. [F056](RAW_FACTS.md#f056), [F256](RAW_FACTS.md#f256), [AXIS S044](https://help.axis.com/en-us/axis-object-analytics).

H-B **does not satisfy the literal hazardous proximity to moving machinery/transport example on PDF page 4**. That needs verifiable motion, defensible dangerous-distance geometry and equipment-activity information. Without them do not call a static polygon proximity detection. Reject H-B if the expert does not accept its limited scope or material cannot distinguish true presence from perspective overlap. Neither candidate has an established working detector, approved dataset, SDK, access or latency. If a mandatory dependency is missing, label the result precisely as a partial demo—other-hardware recognition, synthetic-event interface, or still-image processing—as applicable. [F200](RAW_FACTS.md#f200), [F204](RAW_FACTS.md#f204), [F256](RAW_FACTS.md#f256), [Q057](OPEN_QUESTIONS.md#q057), [Q059](OPEN_QUESTIONS.md#q059), [Q061](OPEN_QUESTIONS.md#q061).

<a id="verification-and-metrics"></a>
## Verification and metrics: NOT RUN plan and corrected K008 contract

**All UX tasks, LinQ runs and pilot procedures below are NOT RUN.** K008 is closed only as internal consistency of definitions/arithmetic; application remains open. Historical W1 formulas are retained in the evidence history but superseded by [F257](RAW_FACTS.md#f257) and the [second-wave K008 resolution](CRITIC.md#k008--результат-w2). No interviews, participants, recordings, benchmarks or measured improvements exist in this research.

### UX and event checks: explicit tasks and outcomes

1. Walk through a real recent event with recipient/foreman/OHS, independently compare responsibilities, inspect an anonymized card, cover night/backup/false alarm/existing EHS. Separately ask the worker/contractor to trace an objection through original evidence, reviewer, response and corrected consequences. Buyer research needs budget authority/procurement artifacts. [Q055](OPEN_QUESTIONS.md#q055), [Q060](OPEN_QUESTIONS.md#q060).
2. With role-appropriate participants and independently labeled true/false/ambiguous material, test location/currentness/action, original access, uncertainty, duration/end/re-entry, interruption/recovery, four-filter search, correction/save/reopen, failure versus quiet queue, and equal counts under unequal coverage. Observe correctness as well as time, unsupported decisions, missed messages, help, lost edits and recovery. Small formative rounds are not representative usability percentages. Accessible substitute participants must be identified and do not stand in for factory workers. [Q056](OPEN_QUESTIONS.md#q056).
3. Any comparison with an accessible exact Vizorlabs 4.0 installation uses equal camera/material/duration, clip readiness and instructions, alternating order and recorded prior familiarity. A manual is not an operational comparator; no click/time superiority can be inferred from it. [F187](RAW_FACTS.md#f187), [F190](RAW_FACTS.md#f190), [Q056](OPEN_QUESTIONS.md#q056).
4. Before event evaluation, freeze scenario, observability, reference intervals, model/version/threshold, `T_on/T_clear`, gaps and matching. Include close negatives and ambiguous scenes; independently inspect non-alert video. Frames of one clip are not thousands of independent trials; split by scene/camera/shift where evaluating transfer. Changes after failures require preserved original versions. [F152](RAW_FACTS.md#f152), [F257](RAW_FACTS.md#f257), [Q062](OPEN_QUESTIONS.md#q062).

| Canonical plan | Check | Required observation; all NOT RUN |
|---|---|---|
| [E001](RAW_FACTS.md#e001) | Long positive episode across many frames | One card and one initial alert |
| [E002](RAW_FACTS.md#e002) | Proven ending followed by new episode | Two events, no permanent suppression |
| [E003](RAW_FACTS.md#e003) | Redeliver same material within same run | No duplicate; independent new run separately identified |
| [E004](RAW_FACTS.md#e004) | Gap/occlusion during episode | No unsupported resolution/splitting; identity limit visible |
| [E005](RAW_FACTS.md#e005) | H-A/H-B closest negatives | Ordinary posture/passage errors retained |
| [E006](RAW_FACTS.md#e006) | Two people, ID change, boundary jitter/small motion | No merged people; no immobility inference from stable box |
| [E007](RAW_FACTS.md#e007) | Reload and reuse filters | Journal/evidence persist and remain retrievable |
| [E008](RAW_FACTS.md#e008) | Source→first observation→confirmation→LinQ→WEB→record | Separate processing/delivery stages, video time and wall time |

Passing these would validate a described demonstration mechanism under its conditions, not industrial safety across all cameras.

### K008 detection, uncertainty, duplicates and exposure

**INF method:** Unit = predefined episode with camera/zone, object or object pair, start/end. Freeze spatial conditions, gap tolerance, time tolerance and one-to-one matching before evaluation. `TP` is an eligible system/reference pair; `FP` a determinate false unique episode; `FN` a determinate reference without a match. Duplicates are published separately and do not add TP. A card falsely merging two references matches at most one; the second remains FN. Manual splitting/correction is a new derived version, not retroactive repair of the original result. [F257](RAW_FACTS.md#f257), [E010](RAW_FACTS.md#e010).

For unique presented episodes:

```text
N = T + F + U + X
T = true; F = false; U = reviewed but indeterminate; X = unchecked
precision_adjudicated = T / (T + F)
review_coverage = (T + F + U) / N
determinate_coverage = (T + F) / N
unknown = U / N; unchecked = X / N
all-presentations true-share bounds = [T/N, (T+U+X)/N]
recall = TP / (TP + FN)
```

A zero denominator makes the metric undefined. Publish counts beside rates; the true-share bounds are uncertainty bounds, **not a confidence interval**. Recall requires independent complete labeling of the defined evaluation-video scope, including non-alert material; an alert queue alone cannot establish it. `FP / valid camera-hour` requires U/X, unavailable hours and valid-coverage share alongside it. Unavailable time is not known safe. Distinguish presented-card truth accounting from reference matching so duplicates/merges cannot inflate detection success. [F257](RAW_FACTS.md#f257), [Q062](OPEN_QUESTIONS.md#q062).

### K008 timely action: denominator includes missed and unanswered references

Before evaluation define qualified site action, deadline `L`, and visible onset `t0`. A card open/acknowledgement is not necessarily site action. Timely-response completeness = all determinate reference episodes with action `ta <= t0+L` divided by **all determinate reference episodes**. Missed, undelivered and unanswered cases stay in the denominator. Report response latency among respondents with `n/N`, misses, unanswered and overdue counts; separate onset→delivery from delivery→action. New events whose deadline has not expired are right-censored; a simple completed cohort uses `t0 <= cutoff-L`. No answer is not zero latency. Causal notification benefit requires a comparison design. [F237](RAW_FACTS.md#f237), [F257](RAW_FACTS.md#f257).

**E009 fictional arithmetic, not service quality:** of 12 agreed camera-hours, 10 are valid. Independent review finds four determinate reference episodes. Six unique system episodes are T=3, F=1, U=1, X=1, plus one duplicate card. Adjudicated precision=3/4=75%; review coverage=5/6=83.3%; determinate coverage=4/6=66.7%; U/N and X/N each 1/6; true-share bounds=50-83.3%; recall within determinate valid scope=3/4=75%, unknown during the two unavailable hours. One of four references receives action within the illustrative 60-second limit; one is missed, one unanswered, one late → timely completeness=25%. Median 55 seconds among two responders describes only 2/4 references. The fictional 60 seconds is not an SLA; p95 from two observations is not stable. [E009](RAW_FACTS.md#e009).

The same fictional E009 has seven cards: duplicate-card share=1/7=14.3%, additional duplicate load=1/6 unique episodes=16.7%, and FP/valid camera-hour=1/10=0.1. U and X are each additionally 0.1/hour; valid coverage=10/12=83.3%. True-event delivery=3/4=75%, qualified action=2/4=50%, unanswered among delivered true events=1/3=33.3%; missed and late each 1/4=25%. The two action times are 20 and 90 seconds from onset, making the 55-second median; among responders, 1/2=50% meet L, which cannot replace the all-reference 25%. U/X response handling remains in the operational log despite unknown truth. These named denominators are deliberately different. [E009](RAW_FACTS.md#e009).

Labor/cash evaluation uses the separate K008 equations and fictional [E011](RAW_FACTS.md#e011) in [statistics and economics](#statistics-and-economics), retaining review of U/X/duplicates and work shifted to OHS/IT. [E010](RAW_FACTS.md#e010) preserves one-to-one matching/false-merge arithmetic. These examples check definitions, not production performance.

### Pilot progression and continuation

**HYP, NOT RUN:** after technical/legal preparation, begin bounded shadow observation without operational promises, assess scene/noise/workload, then enable agreed delivery to named recipients. Do not import Protex's supplier 99% threshold as our acceptance criterion. Cover agreed shift/light/occlusion conditions, log valid/unavailable periods, and count tuning, review T/F/U/X, duplicates, support and action by role. Existing safety measures remain in force. Agree before results whether observability, workload, timely useful action, correction access and data/security route justify continuation. No numeric acceptance threshold or operational SLA has been established here. [F103](RAW_FACTS.md#f103), [F152](RAW_FACTS.md#f152), [F160](RAW_FACTS.md#f160), [F161](RAW_FACTS.md#f161), [F257](RAW_FACTS.md#f257).

<a id="jury-and-handoff"></a>
## Jury and handoff: defensible claims, owner questions, adjacent topics

**INF:** Analytics evidence should show decisions and their reasons in the three official areas, keeping implemented behavior separate from documentary research. Show recipient→responder→OHS with buyer/IT/affected worker; five UX chains with checks; comparable alternatives and adopted patterns. If implementation exists later, name actual input, model, LinQ runtime, valid episodes and measured stage delays. This report supplies no missing result. Do not claim universal 20-minute attention failure, 70-80% preventability, case illustrations as effects, unique LinQ/human rejection, injury reduction from fewer alerts, or guaranteed jury points. [F153](RAW_FACTS.md#f153), [F254](RAW_FACTS.md#f254), [F257](RAW_FACTS.md#f257).

| Open question / answer owner | Required concrete evidence | Decision affected |
|---|---|---|
| [Q055](OPEN_QUESTIONS.md#q055): process owner/foreman/OHS; budget holder | Recent anonymized event route, primary/backup/shift access, response authority; procurement/budget criteria | Primary user, channel, pilot segment, buyer |
| [Q056](OPEN_QUESTIONS.md#q056): UX team and intended users | Actual true/false/ambiguous tasks; errors/time/save/history; exact accessible comparator if used | Card usefulness and any comparative claim |
| [Q057](OPEN_QUESTIONS.md#q057): domain expert/technical team | Accepted observable H-A/H-B definition, negatives, sequence/ground truth, timing; dynamic geometry if proximity required | Scenario choice or rejection |
| [Q058](OPEN_QUESTIONS.md#q058): statistical-source owner if a stronger sector claim is needed | Original page 137/native table, footnotes, population/denominator; methodology chronology | Whether any industry ranking can be published |
| [Q059](OPEN_QUESTIONS.md#q059): file owner/data controller/provider | File rights/passport, operations/bases, recipients/countries/endpoints/logs/stores/retention, separate display rights | Lawful input and public-demo composition |
| [Q060](OPEN_QUESTIONS.md#q060): worker/contractor, foreman, OHS separately | One disputed episode with original, objection route, reviewer/reason/history/reply and corrected consequences | Correction, neutral language, access, personnel-use policy |
| [Q061](OPEN_QUESTIONS.md#q061): technical team/organizer | Actual access, SDK/runtime/model/conversion/input and reproducible LinQ logs/speed/latency | Mandatory-path feasibility; accurate partial-demo label |
| [Q062](OPEN_QUESTIONS.md#q062): evaluation/domain owner/users | Independent full reference scope, matching, valid hours, qualified action and L, frozen episode parameters | Recall, timely response, workload claims |
| [Q063](OPEN_QUESTIONS.md#q063): buyer/labor/infrastructure owners | Equal-scope role hours, A/P/O/I, contractual compute/license/support/integration costs | TCO and continuation, without converting hours automatically to cash |
| [Q064](OPEN_QUESTIONS.md#q064): authorized counsel | Current official law and applicability to actual people/purposes/operations/site | Real pilot/publication authorization |

→ `operator_product`: conditional roles, five UX chains, observation/truth/action separation, evidence/filter/save/history patterns; no proven need for seven accounts. → `market_deployment`: separate product layers and provenance, unknown exact Russian/global procurement and full LinQ price, hours/payment distinction. → `violation_methods`, `model_stack`, `datasets`, `training_strategy`: eight observable definitions, near negatives, lawful sequences, H-A/H-B rejection; SH17 is not cleared for public demo. → `evaluation`: corrected K008, E001-E011, U/X, duplicates/false merges, coverage, all-reference timely-response denominator. → `video_architecture`, `linq_platform`: source/video/wall-time/inference/delivery/action distinctions, exact remote data route, health and partial-path disclosure. → `hackathon_strategy`: official analytics areas and defensible evidence; separate lawful public material from production archives. Neighboring topic names are handoff destinations, not claims that their results were read or implemented. [F236](RAW_FACTS.md#f236), [F254](RAW_FACTS.md#f254), [F255](RAW_FACTS.md#f255), [F256](RAW_FACTS.md#f256), [F257](RAW_FACTS.md#f257), [F259](RAW_FACTS.md#f259).

The research supports choices and a verification plan. Actual LinQ access, working recognition, usable interaction, adoption, purchasing and industrial effects require separate evidence. Every proposed real-world check remains **NOT RUN**.
