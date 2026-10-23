---
topic: operator_product
scope: >-
  Evidence-based roles and human workflows around industrial safety video analytics:
  alert handling, camera/rule onboarding, feedback, corrective measures, management
  review, privacy, product-to-architecture requirements, and a conditional 45-hour MVP.
  Russian public practice is prioritized; foreign product and human-factors evidence
  retains its original scope. This is research and proposed design, not a built service.
not_covered:
  linq_platform: SDK/compiler/runtime configuration, device access and execution verification implementation
  model_stack: Model selection, weights, export and reproducible inference pipelines
  violation_methods: Detection algorithms, episode boundaries, tracking, geometry and event matching methods
  datasets: Dataset acquisition, licensing, class definitions and annotation production
  training_strategy: Training implementation and measured adaptation benefit
  evaluation: Full statistical evaluation protocol and model benchmarks
  video_architecture: Implemented streaming, storage, scaling and service architecture
  market_deployment: Pricing, economics, Russian legal assessment and deployment compliance
  hackathon_strategy: Overall competition strategy and final scope after receipt of the full case
answers:
  - Who can observe, review, intervene and own a corrective measure, and how strong is the role evidence?
  - When should a staffed alert queue or local warning with later review be used?
  - What are the documented as-is fragments and proposed to-be steps of the four workflows?
  - What belongs in an episode card, and how do review, delivery, acceptance, hazard and measure states differ?
  - How should camera and rule onboarding handle test location, PPE results and a changed camera view?
  - What evidence supports notification channels, urgency, alarm-load controls and interface defaults?
  - How should false detections, disputes, suspected misses and training permissions be handled?
  - Which management questions and metrics remain meaningful under changing coverage and review selection?
  - What do privacy and worker evidence establish, including the Protex DPA exceptions?
  - Which 17 data groups, clock distinctions and six failure fallbacks does the product need?
  - What conditional priorities, reduction gates, three surfaces and two demos fit the proposed minimum?
  - Which proposed checks, HiTech questions and handoffs are needed before stronger claims?
keywords:
  - OHS
  - HSE
  - PPE
  - СИЗ
  - ПАБ
  - охрана труда
  - промышленная безопасность
  - ООО ХайТэк
  - LinQ
  - video episode
  - alarm fatigue
  - corrective action
  - camera-hours
  - miss_candidate
  - Intenseye Public API v2
  - falsePositive
  - customerFalsePositive
  - accuracyRate
  - Protex AI
  - Voxel
  - Carlex
  - UAW
  - FindFace Multi 2.2.1
  - Alarm Monitor
  - Alarm Feed
  - Milestone XProtect 2025r3
  - Macroscop
  - TRASSIR
  - Telegram
  - MAX
  - Express
  - 1С:EHS
  - review_result
  - delivery_attempt.state
  - acceptance
  - hazard_observation
  - measure.execution
  - measure.verification
  - actor_origin
  - source_event_id
  - idempotency_key
  - revision
  - input_ref
  - PTS
  - live
  - replay
  - stored_result
  - WCAG 2.2
entity_schema:
  role:
    fields: [role, evidence_strength, decisions, inputs, location_device, frictions_unknown, product_implication]
    representation: Role map table; proposed decisions and product implications are INF, not observed client practice
  proposed_check:
    fields: [id_status, question_inputs, actions_evidence_metrics, outcome_limit]
    representation: Proposed checks table; every entry is NOT RUN
takeaways:
  - >-
    Build one traceable path: permitted input/rule, actual LinQ result with execution
    provenance, evidence card, explicit human decision and persistent history. Add one
    justified extension only after this works; effort has not been measured.
  - >-
    A staffed recipient is conditional. Authorized urgent warning may precede or run
    alongside review. Without a usable channel or useful intervention window, use
    asynchronous review; local warning is not a protective stop.
  - >-
    Delivery, human acceptance, evidence review, hazard observation, completion report
    and measure verification are independent. Auto-ACK, a comment and no new events
    establish neither human intervention nor safety.
  - >-
    Privacy follows originals and every derivative/copy, including LinQ, QA and training.
    Protex's October 2025 DPA allows a bounded unblurred-cloud QA/training exception;
    later public training/refinement scopes remain unresolved. Blurring is not full anonymity.
  - >-
    Raw vendor/customer labels and curated decisions remain separate. No independent
    archive means suspected misses without recall; reviewed-only metrics and camera-hours
    do not establish overall quality, risk exposure or prevented injuries.
  - >-
    Full case, datasets, SDK/runtime, actual LinQ access/execution proof, client duty matrix,
    field delivery, direct Russian worker voice and live competitor UX remain unavailable.
    All E001-E015 checks are proposed and NOT RUN.
checked_at: '2026-10-23T10:13:44.1564311+03:00'
context_version: mosprom-research-v1
source_access_date: '2026-10-23'
case_materials:
  received: [Context-prompt.md, prompt-operator-product.md, saved public announcement and 2026 rules evidence]
  not_received: [full case, mandatory classes and metrics, organizer datasets, personal-account materials, LinQ SDK/runtime, actual LinQ access, execution proof]
actually_checked:
  - Compressor read both input prompts, final human report, role brief and handoffs, with relevant saved F/S/Q/K records
  - Research waves read specified public documents and retained source/version/locator metadata; API descriptions were not API executions
  - Earlier attempted live UX capture failed because iab was unavailable and app/browser inventory was empty
  - Compressor checked its own YAML, canonical IDs, relative links, UTF8 and answers coverage during file manufacture
  - No new network research, interviews, product tests, LinQ jobs, delivery trials, subagents or final audit in compression
human_report: report_human_operator_product.md
evidence_files: [SOURCES.md, RAW_FACTS.md, CRITIC.md]
open_questions: OPEN_QUESTIONS.md
---

# Operator product: traceable evidence, human decisions and corrective measures

The recommended minimum is **one permitted input and checked rule → actual LinQ inference with execution provenance → evidence card → explicit human decision → persistent history**. A measure is linked when the process needs one; an external channel, universal second verifier, editor and dashboard are optional extensions. This is HYP, not an implemented service, received client API or measured person-hour estimate. The full case can change the minimum. [F136](RAW_FACTS.md#f136), [F137](RAW_FACTS.md#f137).

## Evidence legend, verification status and case boundaries

Evidence type and verification status are independent:

| Label | Meaning | Verification boundary |
|---|---|---|
| DOC | Specific primary documentation, regulation or contractual text | The cited section was read; capability or wording is not demonstrated deployment |
| VENDOR | Supplier product claim or supplier-curated customer story | Read as a claim; no independent effectiveness or implementation verification |
| SELF-REPORT | Company/practitioner/user account of their own experience | Source context retained; no independent causal or prevalence inference |
| MEAS | Published measurement with author and study conditions | Not our experiment; transfer requires matching conditions |
| LOCAL-OBS | Actual local observation during this research | Limited to the observed action/environment |
| INF | Our synthesis or design requirement derived from cited evidence | No client/process/field validation |
| HYP | Proposed product choice or testable design hypothesis | Not implemented or tested here |
| UNKNOWN | Missing answer, inaccessible artifact or unresolved scope | Remains linked to Q-ID; absence of evidence is not evidence of absence |

The two research waves produced **87 S records, 147 F records, 20 Q records and 15 proposed E procedures**. Source access is **2026-10-23, Europe/Moscow**; `checked_at` is compilation metadata, not a source publication date. [SOURCES.md](SOURCES.md) retains dates/versions/locators; [RAW_FACTS.md](RAW_FACTS.md) retains conditions; [CRITIC.md](CRITIC.md) preserves original criticism and W2 outcomes. Compression added no external evidence or product experiment. Actual role assignments and environment limitations are in [_WORK/RUN_STATE.md](_WORK/RUN_STATE.md); the root model was not asserted to have been reconfigured.

DOC: The [public 2026 announcement](https://hackathon2026.otkroimosprom.ru/) requires real-time industrial video analysis, prompt notification and inference on Russian **LinQ** accelerators, with online access promised. Helmet, respirator, dangerous-zone entry and smoking near flammable material are examples, not an established exhaustive class list. Full case/classes/metrics, datasets, account files, SDK/runtime, real access and execution proof were not received. A scheduled publication time does not prove receipt. [F099](RAW_FACTS.md#f099), [F103](RAW_FACTS.md#f103), [Q004](OPEN_QUESTIONS.md#q004).

DOC: The [2026 rules](https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf) specify **seven criteria using an integer 0–3 scale**, including UX/UI, analytics, development/deployment, main and secondary problems. Analytics includes audiences, UX problems, competitors and analogous products. Separate weights/aggregation formula were not established; do not turn the input's “equally weighted” wording into a verified formula. Five minutes presentation plus three minutes questions; video or prototype link is allowed. Feature-to-criterion links below are INF, not predicted scores. The preparation context gives a 45-hour submission window. [F100](RAW_FACTS.md#f100).

Terminology: an **episode** is a bounded observation with source/time, initially a candidate; a **signal** communicates it; a **measure** is a process action that can cover several episodes. `review` evaluates available evidence; `verification` evaluates execution of a measure. `live`, `replay` and `stored_result` are distinct provenance modes. Internal `incident_id` does not confer formal incident status. [F132](RAW_FACTS.md#f132), [F142](RAW_FACTS.md#f142).

## Role map: observer, reviewer, intervenor, measure owner

No evidence establishes a universal full-time video-analytics operator or a plant-size/sector mapping such as “large holding = control room, medium plant = foreman, construction = phone.” The professional standard supports information, coordination, control and prescriptions, not permanent video-wall viewing. Order №274н and the new №324н must retain temporal scope: the new standard takes effect **1 March 2027**, after this research date. Local hierarchy, stop authority and workspace remain client questions. DOC/INF [F001](RAW_FACTS.md#f001), [F002](RAW_FACTS.md#f002), [F003](RAW_FACTS.md#f003), [F004](RAW_FACTS.md#f004), [F143](RAW_FACTS.md#f143).

Every role row follows the declared schema. Decisions, required inputs and implications are INF; evidence strength concerns the cited source, not confirmation at HiTech customers.

| Role | Evidence strength | Decisions | Inputs | Location/device | Frictions/unknown | Product implication |
|---|---|---|---|---|---|---|
| CCTV/security observer | Primary Mostotrest vacancy: observe, record, report, contact response team, report failures; transport-security scope. Bobrovsky plant aggregator combines OHS/theft/archive/statistics; employer original not recovered. [F010](RAW_FACTS.md#f010), [F011](RAW_FACTS.md#f011) | Assess or route candidate under authority | Place/time, evidence, instruction, recipient | Shift work in particular examples; camera/screen counts and continuous viewing unknown | Real interruptions, load and complaints unmeasured; not automatically HSE owner | Separate observation from intervention and technical diagnosis |
| Dispatcher/branch specialist | Gazprom Burenie interview: specialist can call foreman; KGМК account: image/fragment reaches console. SELF-REPORT [F020](RAW_FACTS.md#f020), [F105](RAW_FACTS.md#f105) | Route to an authorized shift recipient; retain outcome | Landmark, freshness, contact/deputy, handoff result | Console only in the cited example; device and night coverage unknown | Job title, combined tasks, stop authority unknown | Staffed queue only after duty matrix and useful window are confirmed |
| Foreman/shift or line supervisor | Titan-Polymer vacancy includes subordinate OHS control; drilling account names foreman and possible work stop. DOC/SELF-REPORT [F005](RAW_FACTS.md#f005), [F020](RAW_FACTS.md#f020) | Accept responsibility; choose authorized intervention; report action | Where/what, local instruction, permitted action, handoff destination | Field presence is a scenario condition; issued phone and safe viewing point unknown | Coverage, phone permission and actual response time unknown | Short place/evidence/accept/action path, conditional on safe device/channel |
| OHS/industrial-safety specialist, review owner | Professional standard and company materials support control, coordination, prescriptions, cause/measure analysis. DOC/SELF-REPORT [F001](RAW_FACTS.md#f001), [F068](RAW_FACTS.md#f068), [F072](RAW_FACTS.md#f072) | Rule applicability, evidence sufficiency, recurrence and measures | Rule/context, related episodes/actions, verification basis | Office, device, workload and cycle unknown | No observed complaints about client screens | Evidence review and later analysis can be asynchronous |
| Technical owner/integrator/automation center | Titan-Polymer technical CCTV/access-control duties; KGМК automation-center notifications. DOC/SELF-REPORT [F005](RAW_FACTS.md#f005), [F105](RAW_FACTS.md#f105) | Diagnose and restore failed stage/configuration | Test origin, stage health, last good, camera/rule/view versions | Duty and device unknown | Receipt of diagnostics does not make this role measure owner | Separate technical failures from production signals; assign repair owner |
| Area/production manager | Company reports on prescriptions, recurrence, causes, measures; KGМК decision to seek another operation method. SELF-REPORT [F068](RAW_FACTS.md#f068), [F106](RAW_FACTS.md#f106) | Allocate resource; change operation/protection; prioritize unfinished measure | Open actions, recurrence after application, observation coverage | Actual buyer, budget, report format and day/week rhythm unknown | No measured management usability or causal benefit | Use a decision-oriented linked list before risk rankings |
| Worker/contractor | Behavioral safety audit includes conversation; company procedures allow hazard reporting/refusal under their rules; contractor admission/control differs. DOC/SELF-REPORT [F006](RAW_FACTS.md#f006), [F007](RAW_FACTS.md#f007), [F014](RAW_FACTS.md#f014) | Explain context, report hazard, challenge error, follow authorized local action | Purpose, observation context, allowed action and appeal path | Device/access/channel unknown | No direct interviews or client acceptance evidence; contractor is not automatically employee | Accessible appeal and accurate purpose/sanction communication |
| Worker representative/union | FNPR discusses digitalization risks; ROSPROFZHEL reports digital prescription control. SELF-REPORT [F073](RAW_FACTS.md#f073), [F078](RAW_FACTS.md#f078) | Discuss purposes, access, use policy and appeal | Data path, recipients, permitted uses, suitable aggregates | Client representation/access unknown | No pilot agreement or direct worker voice | Role name does not authorize access to all originals |
| Annotation curator/data owner | Separate curator is our proposal, motivated by vendor/customer disagreement. INF [F123](RAW_FACTS.md#f123), [F126](RAW_FACTS.md#f126) | Adjudicate or preserve dispute; approve curation eligibility separately from training | Raw opinions, visibility, rule, permitted original, rationale/revision | Dedicated staff/resource unknown | Agreement is not infallible gold; need not block urgent warning | Preserve raw labels, curated result, lineage and permissions separately |
| Information security/data-policy/corporate-register owner | Necessary decision owners in our contract; client organization not received. INF [F122](RAW_FACTS.md#f122), [F142](RAW_FACTS.md#f142) | Approve purposes/copies/recipients/retention and external classification | Original/export/attachment/QA/training rights, local policy, external ID | Responsible person/device unknown | Demo role is not legal permission | Enforce rights before display/export/notification, not as a later badge |

Vacancy = stated duty at one workplace; VMS manual = capability; deployment story = reported practice. None establishes prevalence, cameras/person, viewing norm, tolerated load or response deadline. UNKNOWN [Q001](OPEN_QUESTIONS.md#q001), [Q012](OPEN_QUESTIONS.md#q012).

### Two conditional recipient maps: staffed queue and local warning

**Map A — staffed recipient plus field intervenor.** Candidate → known shift recipient reviews/routes → foreman or other authorized recipient explicitly accepts → permitted field action → optional linked measure → reported execution/verification under local policy. For an urgent class, authorized preliminary warning can precede or run alongside review. Entry conditions: duty/deputy list, channel/device, authority, useful intervention window. INF [F138](RAW_FACTS.md#f138), [F139](RAW_FACTS.md#f139).

**Map B — local warning plus later review.** Authorized automatic local output warns on site; journal persists; a named owner later reviews circumstances/recurrence and links a measure. No permitted/working local output → asynchronous detection/review only, with backlog/history as the main surface and no prompt-prevention claim. Local warning is an informational action, **not a protective stop or human ACK**. INF [F107](RAW_FACTS.md#f107), [F108](RAW_FACTS.md#f108), [F138](RAW_FACTS.md#f138).

SELF-REPORT context: Gazprom Burenie **4 December 2024** describes specialist→foreman call, no numeric SLA or measured response. KGМК **3 April 2025** describes console plus automation/industrial-safety distribution; **28 July 2025** describes local sound and responsible recipients. These are related publications on one line, not independent impact measurements; differing camera counts are unexplained and not used. A separate well-repair pilot has warning before later brigade analytics; system “24/7” does not establish human duty. KGМК's useful management outcome is a decision to find another way to perform an operation judged unsafe; completion is unproven. [F020](RAW_FACTS.md#f020), [F105](RAW_FACTS.md#f105), [F106](RAW_FACTS.md#f106), [F107](RAW_FACTS.md#f107), [F108](RAW_FACTS.md#f108), [S071](SOURCES.md#s071), [S073](SOURCES.md#s073).

## Workflow 1: signal → review/handoff → action and measure

**As-is evidence:** SIBUR behavioral safety audit (ПАБ) has preparation, observation, conversation and report. Dangerous behavior/conditions can require safe stopping, discussion of consequences/safer method, agreement and thanks; safe behavior also receives positive feedback. Video supplies observation material, not the conversation. Gazprom Shelfproject stop-card description covers intervention, localization and escalation beyond one's ability; the obtained regulation PDF contains only a title page, so full procedure/deadlines are unknown. A 1С:EHS implementer describes distinct stop-cards, daily reports, permits, inspections, measures and investigations, with executor/notification/control for measures. These fragments do not form an observed HiTech route. DOC/SELF-REPORT [F014](RAW_FACTS.md#f014), [F015](RAW_FACTS.md#f015), [F016](RAW_FACTS.md#f016), [F017](RAW_FACTS.md#f017), [F018](RAW_FACTS.md#f018), [F019](RAW_FACTS.md#f019).

**To-be INF:** the sequence is a coordination model; authorized preliminary warning is not universally gated by review. Gaps such as absent recipient, undocumented phone result or document-without-action are plausible failure modes, not measured frequencies. [F144](RAW_FACTS.md#f144).

| Step / actor | Information | Decision/result | Failure and retained evidence |
|---|---|---|---|
| Register / system | Input/result, source, rule/model version, times/mode/health | Stable candidate; agreed urgency policy | Unknown place/time/provenance explicit; detection is not established violation |
| Warn if permitted / system + recipient | Freshness, local instruction, allowed output | Preliminary warning before/parallel to review | Pending clip need not block warning; no output/window means no prompt-intervention promise |
| Review / authorized reviewer | Original/overlay by rights, frame/clip, rule/zone/place/time | Supported, false detection, insufficient, not applicable, duplicate | Occlusion, masking or missing clip can legitimately yield insufficient evidence |
| Handoff / dispatcher + recipient | Current owner, intended recipient/deputy, attempts, instruction | Assignment plus separate explicit acceptance | Sent/HTTP 202/auto-ACK ≠ person; pending transfer preserves former owner/dispatch |
| Act / authorized field person | Place/context/permitted intervention | Record concrete action; link one measure to one/many episodes if needed | Leaving frame does not establish removal of cause; detector does not select safe technology |
| Execute/verify / executor and policy verifier | Action/time/basis | Completion report distinct from accepted verification | Comment ≠ measure; optional verifier is `not_required`, not verified |
| Finish review or hand over / owner | History, open measures, server revision, new context | Complete selected work, transfer, dispute or revise | Open measures survive completed review; concurrency/offline action must remain visible |

### Episode evidence card and media sufficiency

The card answers **what is visible, where/when, whether evidence suffices, and who acts next**. Show actual frame/clip and readable rule centrally; bounding box/line/confidence help locate a feature but do not replace image/context. Original and overlay are different renditions. A floor map requires trustworthy mapping; otherwise use a checked text landmark. DOC/INF [F031](RAW_FACTS.md#f031), [F033](RAW_FACTS.md#f033), [F034](RAW_FACTS.md#f034), [F134](RAW_FACTS.md#f134).

Minimum: episode ID; mapped source/place; candidate type; rule/version and model reference; observation and receipt times; `live/replay/stored_result`; stream/inference health; media reference/readiness/rights; current review with author; owner/intended recipient/acceptance; delivery attempts; history. Add instruction/measure only when process-defined. End/duration/pre-post/related camera/archive are conditional on real data; no applicable seconds-before/after value was established. Show `pending`, frame-only, `not recorded`, `expired`, `forbidden` and retrieval failure distinctly. `forbidden` is not absent. Current live opens separately and must not substitute for historical evidence. One frame may be insufficient for a temporal violation. INF [F081](RAW_FACTS.md#f081), [F134](RAW_FACTS.md#f134), [F135](RAW_FACTS.md#f135).

### Independent states: review, delivery, acceptance, hazard, measure

DOC: Milestone acknowledgement expresses intent to handle an alarm and moves it to In progress. FindFace Multi **2.2.1 Alarm Monitor** can auto-ACK; **Alarm Feed** can become **Completed after the first comment**. These are product-specific processing facts, not proof of human receipt, true observation or resolved cause. [F032](RAW_FACTS.md#f032), [F063](RAW_FACTS.md#f063), [F128](RAW_FACTS.md#f128), [F129](RAW_FACTS.md#f129).

The following is an **INF logical model**, not a client API or implemented state machine. Small independent labels can share one card. [F132](RAW_FACTS.md#f132), [F133](RAW_FACTS.md#f133).

| Dimension | Proposed literals | Meaning/authority and limit |
|---|---|---|
| `review_result` | `unreviewed`, `supported`, `false_detection`, `insufficient_evidence`, `rule_not_applicable`, `duplicate` + original reference | Authorized human evidence judgment with revision/origin/evidence. `supported` is reviewer-supported observation, not formal act. Dispute remains `disputed/unresolved` with raw opinions |
| `delivery_attempt.state` | `queued`, `sent`, `transport_accepted`, `failed`, `unknown` | System/adapter fact per channel/recipient/response/time; many attempts possible. Transport acceptance is not reading |
| `acceptance` | `unaccepted`, `accepted`, `declined`, `transferred_pending`; separate current owner/intended recipient | Explicit human action accepted by server, or recorded manual contact with recorder/reporter distinguished. Assignment is not acceptance |
| `hazard_observation` | `unknown`, `observed_present`, `observed_absent`, `stale` | Human/system observation with `as_of`, scope and evidence. Absence is bounded to evidence, not cause/future/out-of-frame safety |
| `measure.execution` | `proposed`, `open`, `in_progress`, `completion_reported`, `cancelled` | Owner/executor reports concrete action; reported completion remains a report |
| `measure.verification` | `not_required`, `pending`, `accepted`, `rejected` | Policy/verifier/basis where required. `not_required` ≠ verified; rejected verification ≠ false detection |

One measure can cover several episodes; no mandatory task/comment/second verifier per frame or minor action. Due date is `null` until assigned; “overdue” requires an actual deadline and completion policy. Completed review must not hide an open measure. Preserve raw `external_status`, product/version and `mapping_version`; FindFace Completed maps only to comment-recorded processing, VMS Closed only to alarm closed in VMS. Never infer review/hazard/measure from those labels. A display name alone does not prove authority. INF [F115](RAW_FACTS.md#f115), [F130](RAW_FACTS.md#f130), [F132](RAW_FACTS.md#f132).

Audit records need actor and origin. Preserve the source schema's `actor_origin=human/system/external_system`; if origin is unavailable it remains **unknown**, never upgraded to human. An external machine ACK remains a system-origin fact with external provenance. Oral report entered by dispatcher retains `recorded_by` and `reported_by`. Demo roles are explicitly `demo`. Corrections append `revision`, prior opinion, reason and `supersedes`; concurrent server revisions yield explicit conflict/reload. Offline click is pending until server acceptance. Same `request_id`/source-event retry is idempotent, not a new real episode. New episode grouping across people/zones is a separate `violation_methods` problem. INF [F132](RAW_FACTS.md#f132), [F133](RAW_FACTS.md#f133).

Four mandatory semantic counterexamples: false detection + system auto-ACK leaves human acceptance unknown/unaccepted; two episodes may link one measure without doubling it; unaccepted shift transfer retains pending recipient and visible former owner/dispatch; camera outage with no events yields health unavailable and hazard stale/unknown, not “safe,” effective measure or timeout closure. These are proposed consistency cases, not passed tests. [F133](RAW_FACTS.md#f133), [E001](RAW_FACTS.md#e001).

## Notification channels, urgency and alarm-load controls

A channel is useful only if it reaches an authorized person within a useful window and can be used safely. DOC: TRASSIR describes Telegram, MAX, Express, email, SMS and alarm outputs; MAX requires a particular bot profile/moderation. Telegram's returned `Message` proves a send result, not reading; callback is a separate action. XProtect Mobile depends on license, permissions, settings and push. None establishes HiTech field access or actual receipt. [F053](RAW_FACTS.md#f053), [F054](RAW_FACTS.md#f054), [F056](RAW_FACTS.md#f056), [F079](RAW_FACTS.md#f079).

INF default until authorization/configuration/test: a second **internal demo role** explicitly accepts a record; server stores author/time. This demonstrates role semantics, not delivery to a factory. An agreed manual contact to a test recipient can be a reserve with actual attempt/response. External delivery requires named shift/deputy, token/session, device, network, permission, permitted payload and actual receive plus human-ACK evidence. If images cannot leave the perimeter, use approved minimal text and authorized link; attachment/export rights remain separate. Without any required input, remove external-delivery claim. Unconnected local warning is labeled unconnected; browser sound is not industrial warning. Phone prohibition/distraction requires another approved location/device; radio/hands-free is not automatically safe. [F140](RAW_FACTS.md#f140), [Q006](OPEN_QUESTIONS.md#q006).

The Nornickel local security document describes security duty/document handling, not HSE-AI roles. Scan transmission and departmental reply deadlines are document workflow, not intervention SLA. Permission for photo/video capture is not a universal mobile-viewing prohibition. DOC [F109](RAW_FACTS.md#f109), [F110](RAW_FACTS.md#f110).

**Urgency comes from consequences, permitted action, existing protection and useful window; confidence describes a model result.** Helmet absence in old footage differs from active hazardous work; zone crossing without machine-state context differs from entry during operation. No applicable numerical SLA was found. “Immediately,” clip length, VMS minute defaults and 48-hour warranty repair are not intervention deadlines. Define separate observation→event-ready, event→send, send→actual receive, receive→human acceptance, acceptance→action, action→verification intervals, with clock basis/uncertainty and overdue policy. If guaranteed stopping is required, this advisory video layer is insufficient. INF/UNKNOWN [F031](RAW_FACTS.md#f031), [F043](RAW_FACTS.md#f043), [F139](RAW_FACTS.md#f139), [Q002](OPEN_QUESTIONS.md#q002), [Q016](OPEN_QUESTIONS.md#q016).

Human-factors evidence supports questions and bounded hypotheses, not universal quotas:

| Evidence | Original conditions and result | Product boundary |
|---|---|---|
| HSE process-alarm guidance, DOC | Chemical/related process industry: long-term normal-operation average one alarm per ten minutes; up to ten displayed alarms in first ten minutes of major upset; example priority split 5/15/80. Useful information, defined response, grouping/filtering, suppression with return, nuisance monitoring. [F025](RAW_FACTS.md#f025), [F026](RAW_FACTS.md#f026), [F027](RAW_FACTS.md#f027), [F030](RAW_FACTS.md#f030) | Not video-HSE, detections, messenger messages or cameras/person norms. Full paid EEMUA/ISA/IEC texts not obtained. Event grouping needs separate method validation |
| Donald CCTV study, MEAS | Practicing operators and novices in 90-minute active surveillance; no universal vigilance decline in the whole practicing-operator group, specialization mattered. [F028](RAW_FACTS.md#f028) | Not PPE/factory shift; no “all operators stop noticing after N minutes” rule |
| Wogalter voice-warning study, MEAS | 198 participants; voice improved compliance with mask/glove instruction in a laboratory task using harmless substances presented as hazardous. [F057](RAW_FACTS.md#f057) | Not helmets, Russian language/shop noise, repeated AI voice or injury outcome. Field intelligibility/PPE and confusion with emergency alarms require safe testing |
| SafeWork NSW / UK HSE, DOC | Device distraction around mobile/high-risk plant; emergency-signal distinguishability and training. [F059](RAW_FACTS.md#f059), [F080](RAW_FACTS.md#f080) | Questions for local test, not Russian norms or proof that “put on a helmet” prevents harm |
| Cognitive forcing in human-AI decision making, MEAS | Short MTurk ingredient-substitution task: reduced following incorrect AI advice, most effective variants less liked, participant differences. [F061](RAW_FACTS.md#f061), [F062](RAW_FACTS.md#f062) | Not urgent industrial response; mandatory delay may harm useful intervention. Satisfaction/trust ≠ joint decision quality |

HYP: present unique episodes, linked recurrence and explicit next action. An ongoing episode can update duration/count; different people/zones/operations must not disappear into arbitrary time grouping. Suppression needs author/reason/scope/expiry/visible return; disabled rule remains lost control. DOC: FindFace Multi **2.2.1 Alarm Monitor** warns of a queue over **20 events**, removal of unprocessed events and optional counter; this is that monitor's behavior, not proven deletion of source archive or every FindFace version. [F029](RAW_FACTS.md#f029), [F032](RAW_FACTS.md#f032). Queue load and unnecessary per-event manual work remain unmeasured [E002](RAW_FACTS.md#e002), [Q012](OPEN_QUESTIONS.md#q012).

## Workflow 2: camera/rule onboarding and controlled view changes

**As-is DOC:** VMS manuals describe address/protocol/device or ONVIF, credentials/stream parameters, image test, module/ROI or line/direction/object sizes, control result, action/schedule and Apply. This is documented sequence, not observed pilot duration or bulk-onboarding performance. Macroscop Configurator tests from the **computer running Configurator**: laptop/subnet and server reachability can differ. A PPE-check event can carry positive or negative result; notification needs the correct result filter. VMS diagnostics separate camera/authentication, recording, analytics server and overload; view displacement/overexposure are image-quality problems. Live picture alone proves neither inference nor archive. [F035](RAW_FACTS.md#f035), [F036](RAW_FACTS.md#f036), [F037](RAW_FACTS.md#f037), [F038](RAW_FACTS.md#f038), [F039](RAW_FACTS.md#f039), [F040](RAW_FACTS.md#f040), [F044](RAW_FACTS.md#f044), [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046), [F050](RAW_FACTS.md#f050).

**To-be INF for one camera × rule:** [F145](RAW_FACTS.md#f145).

| Actor/step | Information | Decision | Failure/fallback |
|---|---|---|---|
| Area/OHS define condition | Operation/place, required PPE/condition, basis, permitted action | One checkable condition and consequence-based priority | Ambiguous local requirement remains draft; detector does not establish the norm |
| IT/integrator map permitted source | Site/area/camera/input IDs, VMS/stream, owner/rights/test method | One mapped source | Keep RTSP secrets out of card/export/demo; VMS read does not authorize copying whole archive |
| Technical owner test processing | Test location, last frame/check/last good, transport/decode/inference/media health | Ready stages and repair owner | Laptop/server/LinQ visibility differs; unknown is distinct from ready/failure |
| Area/admin verify geometry and semantics | Current view revision, ROI/line/direction, positive/negative examples | Intended zone/result condition | Changed view requires rule recheck; PPE check itself is not violation |
| Policy owner set timing/output | Timezone, enabled schedule, midnight crossing, recipient/deputy | When active and what output | Disabled schedule visible; calendar window is not work permit |
| Authorized publisher Apply | Version/author/reason/time/config snapshot | Publish selected configuration explicitly | Historical events retain old rule/view versions; full rollback UI optional |
| Technical/subject owners maintain | Stage health, view, changes/recovery | Disable/restore/retest under policy | Disabled/unavailable/unknown distinct; disabled rule cannot yield “violation-free shift” |

A configuration file plus read-only rule summary can satisfy the minimum; rule version is required even without editor. Archive dry-run, approvals, rollback UI, bulk configuration and text rules are conditional extensions, not proven market universals. Identity exceptions require reliable association, authorization owner/scope/expiry and stale handling. Nearest badge is not the anonymous detector's person; issued helmet ≠ worn helmet; authorized entry ≠ permission to omit PPE. Machine state/work permit requires a concrete interface and freshness rule. [F052](RAW_FACTS.md#f052), [F082](RAW_FACTS.md#f082), [F085](RAW_FACTS.md#f085), [F087](RAW_FACTS.md#f087), [Q011](OPEN_QUESTIONS.md#q011).

## Workflow 3: false detections, suspected misses, curation and release

**As-is DOC/VENDOR:** Milestone supports acknowledgement/false-positive handling. **Intenseye Public API v2** documents separate supplier `falsePositive` and customer `customerFalsePositive` plus bookmarks. It was read, **not called**; GET/export does not prove write UI/API, dispute procedure, learning or an actual feedback button. Protex claims flags feed refinement, but deployment-only tuning, daily updates and later QA scopes do not establish what changes after a click. [F079](RAW_FACTS.md#f079), [F118](RAW_FACTS.md#f118), [F119](RAW_FACTS.md#f119), [F120](RAW_FACTS.md#f120), [F123](RAW_FACTS.md#f123), [S083](SOURCES.md#s083).

**To-be INF:** store raw human opinions separately from a current product decision and `curated_review_result`; keep author/origin/time/evidence/model/rule/media revisions, curator/basis/revision and unresolved dispute. An initial reviewer need not diagnose every cause. Supported/false/insufficient/not applicable/duplicate plus optional short reason can suffice. Proposed reasons—occluded/small, wrong PPE-person association, ROI/schedule, exception, duplicate, other—are design hypotheses, not observed user complaints. [F064](RAW_FACTS.md#f064), [F126](RAW_FACTS.md#f126), [F146](RAW_FACTS.md#f146).

| Actor/step | Information | Decision/actual change | Failure/unknown |
|---|---|---|---|
| Reviewer assess found event | Permitted evidence and local rule | Append raw opinion/reason/origin/versions | Invisible feature remains insufficient; label is not gold or training consent |
| Rule/camera owner or curator route issue | Concrete cause/context | Configuration review, camera diagnosis or subject adjudication | Threshold does not fix invisibility; correct detection can use wrong rule |
| Observer report suspected miss | Camera/time interval/description/permitted evidence link | `miss_candidate`, `origin=manual`, assigned review | No archive/visibility/health means no confirmed FN; no reports means no claim about misses |
| Subject curator resolve dispute | Independent opinions, rule, permitted original | New curated revision with rationale, or unresolved | Two-person agreement is not infallible truth; preserve raw vendor/customer labels |
| Data owner/curator authorize reuse | Purpose/recipients/lineage | `eligible_for_curation` separately from `approved_for_training` | View/export access does not grant training rights |
| Configuration/data/model/evaluation/LinQ owners release change | Checked request and independent test data | Configuration change or training/calibration → evaluation → new release → actual execution/monitoring | Click does not improve model; keep test set out of training |

P0 can stop at persisted review/history, with truthful feedback such as “flagged for subject review.” Miss journal and curation are extensions. Full competitor missed-event submission workflow was not observed. UNKNOWN [Q007](OPEN_QUESTIONS.md#q007), [Q019](OPEN_QUESTIONS.md#q019).

**Recall needs independent material outside detected-event clips.** Intenseye Accuracy export describes sampled alerts with `alertCount`, `sampleSize`, `falsePositiveCount`, `accuracyRate`; JSON examples are not measurements, sampling/miss-label methodology is not established. Confirmation share in selectively reviewed alerts is neither recall nor automatically overall precision or general “accuracy.” Without an independent continuous archive, keep `miss_candidate` and remove numeric recall. Occlusion, bad ROI, stale event, missing evidence, vendor/customer dispute and camera-ok/inference-down remain different causes. DOC/INF [F124](RAW_FACTS.md#f124), [F125](RAW_FACTS.md#f125), [F127](RAW_FACTS.md#f127), [E007](RAW_FACTS.md#e007).

## Workflow 4: daily unfinished work and periodic management decisions

**As-is SELF-REPORT:** 1С:EHS describes daily reports and measure control; company materials describe prescription registers, recurrence/causes/criticality, management review and technical measures. HiTech's daily/weekly rhythm was not received. Nornickel reports removing injury KPIs that impeded objective recording and changing ineffective ПАБ; these are company accounts, not causal policy evaluation. Preventive messaging can coexist with sanctions; do not promise “coaching only” without policy. [F018](RAW_FACTS.md#f018), [F065](RAW_FACTS.md#f065), [F066](RAW_FACTS.md#f066), [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068), [F070](RAW_FACTS.md#f070), [F072](RAW_FACTS.md#f072).

**To-be INF management question:** “For this operation, is there recurrence after the measure, or is the measure unfinished—must the work method or protection change?” A linked list can answer before a universal risk ranking. Same place/rule does not establish common root cause. [F106](RAW_FACTS.md#f106), [F141](RAW_FACTS.md#f141), [F147](RAW_FACTS.md#f147).

| Step / actor | Information | Decision | Failure |
|---|---|---|---|
| Shift/day / OHS-area owner | Relevant unreviewed candidates, unaccepted handoffs, open measures, camera×rule outages | Assign review/recipient/resource/repair | Auto-ACK or no events mistaken for completed work |
| Before comparison / analytics owner | Observation period, mode/perimeter, cohort, review snapshot/selection, versions/health | Comparable rates, qualified count or list only | New camera, replay/import, disabled rule, selective reviews alter data |
| Week/agreed period / manager + OHS | Reviewed same-condition episodes, measures and applied time | Investigate recurrence; change operation/protection, involve owner | Similar observations do not prove one cause |
| Measure / process owner | Action/owner/actual assigned due date | Organizational/engineering action, conversation, configuration repair, resource and verification policy | KPI closure, invented deadlines or detector-prescribed technology |
| Follow-up / policy owner | Execution report, verification evidence and observation coverage | Accept/reject/retain unknown/next review | No recorded recurrence mistaken for removal of cause |

### Management metric definitions and comparability

Define cohort by source/rule/version/period/mode, plus observation interval, review snapshot and selection. Today's review of an old clip is not today's hazard. The following is an INF dictionary, not mandatory MVP statistics. [F141](RAW_FACTS.md#f141).

| Metric | Definition | Adjacent scope/limit |
|---|---|---|
| Open/overdue measures | Unfinished by agreed policy; overdue only with elapsed assigned due date. Share denominator: all due-dated measures in cohort | Ownerless/undated separate; execution report and verification separate |
| Recurrence after measure | Reviewed same explicit condition occurring after recorded application | Place/operation/rule/versions and actual coverage; no automatic common-cause/failed-measure inference |
| Review coverage | Candidates with finished human review / registered cohort candidates after defined dedup | Snapshot, disputes and insufficient evidence separate; detector misses absent from denominator |
| Support among reviewed | Supported / judgments supported or rejected in same cohort | Not-applicable/insufficient separate; selection visible; not overall precision/recall |
| Control availability | Confirmed working time of camera×rule×version / planned enabled time of that pair | Planned-off, disabled, failed, unknown separate; camera-hours measure observability, **not people's risk exposure** |
| Human acceptance time | Defined interval distribution, e.g. human ACK minus send, only with both real timestamps | Eligible count, ACK count, pending/censored cases, channel/mode/clock uncertainty. Unaccepted ≠ zero; ACK ≠ action |

Counts do not yield LTIFR/TRIR: formal injury statistics need their own definitions, population and person-hours. Adding a camera changes perimeter; doubling people-flow can double events without changing behavior or camera-hours; disabling a rule creates zero detections without improvement; reviewing severe cases changes confirmation/time distributions. Mark breaks/selection/pending work or remove comparison. No numerical scenarios were measured here. [F071](RAW_FACTS.md#f071), [F141](RAW_FACTS.md#f141), [E009](RAW_FACTS.md#e009), [Q013](OPEN_QUESTIONS.md#q013), [Q020](OPEN_QUESTIONS.md#q020).

## Privacy: originals, derivatives, Protex exceptions and worker voice

**A blurred thumbnail or no face recognition does not establish anonymity.** Clothing/time/workplace/context can identify a person. NVR may independently retain originals; LinQ may receive unmasked inputs; player rendition can differ from overview; messenger/export copies escape console RBAC. These are INF data-flow limits, not a measured re-identification attack. [F122](RAW_FACTS.md#f122).

Protex VENDOR descriptions say edge processing, deletion of full current feed and retention of short event clips; masking is configurable, including **No Blurring** and **Videoless**. However, **DOC October 2025 Website DPA, Schedule 1 §1.2(a–c), p.6** makes edge anonymisation a client option and permits temporary cloud processing of short **unblurred video segments** for event QA and training/fine tuning general environmental models, with restricted access and masking as early as possible. Schedule 2 p.8 includes QA/annotation contractors **Sunix/Cogiotech (India), Abelling (Bangladesh), Encord**. §§8.1–8.2 address forwarding/help with subject requests. §11's **30 days after termination** is not universal event retention; de-identified elements can be retained for improvements. This is a public contractual template, not a signed client contract or proof a particular original was transferred. [F116](RAW_FACTS.md#f116), [F117](RAW_FACTS.md#f117), [S079](SOURCES.md#s079).

**Unresolved scope, not an established violation:** Protex ai-info **updated 09.10.2026** describes site-data fine tuning during deployment, no client training after go-live/no site-model sharing, and Bedrock foundation models without training on client data. Homepage FAQ describes daily model updates after calibration, flags into refinement and improvements in hours–days, not a verified weight-change mechanism or SLA. Site models, general environmental models, late QA and configuration relevancy may differ; public material does not resolve object/period. Do not collapse this into “everything stays blurred at edge,” “no learning after launch,” or proven logical/legal contradiction. Need applicable agreement/version/mode/exceptions. VENDOR/INF [F118](RAW_FACTS.md#f118), [F119](RAW_FACTS.md#f119), [F120](RAW_FACTS.md#f120), [S080](SOURCES.md#s080), [S081](SOURCES.md#s081).

INF permission checklist across actual stages; not a demand for a separate store per row:

| Stage | Distinction to preserve | Unresolved owner/policy input |
|---|---|---|
| Camera/NVR/stream | Original, independent archive, read rights, actual recording locations | Owner/purpose/retention/readers |
| LinQ input/job | Unmasked vs derived input, execution/transfer location, temp/cache/logs, secret-free input/job refs | Permitted perimeter/transfer and cleanup owner |
| Event media | Original/masked/overlay renditions, masking lineage/version/status, readiness/rights | Upstream material and immutable reference |
| Console | Role/site access; original opening separate from masked overview | Authorized original readers and audit basis |
| Notification | Approved minimum text/link preferred when permitted; attachment separate | Channel/recipient/perimeter/payload approval |
| Export/report | Who/when/why/fields/rendition manifest; links can disclose data | Destination, retention and deletion of copy |
| Appeal | Raw opinion plus separate appeal, owner and new revision | Accessible worker channel without all-video access |
| Feedback/curation/training | Review access ≠ curation eligibility ≠ training approval | Purpose, frame/person/region scope, recipients/contractors and lineage |
| Deletion | UI/NVR/cache/export/messenger/backup/dataset copies separately | Retention/legal hold and effective mechanism per real copy |

Revoking a link does not delete downloads/forwarding/screenshots; deleting a console record affects all copies only if an actual mechanism does so. “Masked frame; original restricted separately” is supportable; “fully anonymous,” “nobody sees faces,” “original never leaves site” is unproven. Masking can hide the respirator feature: assess model input and human display separately, and permit insufficient evidence when original access is unavailable. Foreign agreements/guidance do not establish Russian compliance, local retention or sanction admissibility. INF/UNKNOWN [F122](RAW_FACTS.md#f122), [Q008](OPEN_QUESTIONS.md#q008), [Q018](OPEN_QUESTIONS.md#q018), [E008](RAW_FACTS.md#e008).

**Worker acceptance is unknown at Russian client sites.** FNPR publications discuss surveillance/cognitive-load concerns; ROSPROFZHEL reports its own digital control tools. Neither automatic opposition nor consent follows. OECD **2022**, manufacturing/finance in **seven countries, not Russia**: among manufacturing workers who reported AI data collection, **56% additional pressure, 51% privacy concern**—a conditional subgroup, not all workers. Consultation is associated with better AI assessments; causality not established. ILO guidance does not replace Russian procedure. Voxel/Carlex **Vonore, Tennessee/UAW** story links cooperation, non-punitive data and training to traffic/layout changes, but is **vendor-curated**, without direct worker/UAW voice or agreement text. No representative consent, causal consultation effect or Russian practice is established. SELF-REPORT/MEAS/VENDOR [F073](RAW_FACTS.md#f073), [F074](RAW_FACTS.md#f074), [F075](RAW_FACTS.md#f075), [F076](RAW_FACTS.md#f076), [F077](RAW_FACTS.md#f077), [F078](RAW_FACTS.md#f078), [F121](RAW_FACTS.md#f121), [Q009](OPEN_QUESTIONS.md#q009), [E015](RAW_FACTS.md#e015).

## Competitor workflows and operator interface: documented patterns, no live UX audit

**LOCAL-OBS:** attempted Protex capture returned `Browser is not available: iab`; inventory had `apps=[]`, `browsers=[]`. No live product tab/screenshots/click path, visual hierarchy, click count or accessibility audit was obtained. **`DPA_P06.png` is a rendered document page, not product UI.** Environment limitation is not a Protex defect or proof no demo exists. [F112](RAW_FACTS.md#f112), [F113](RAW_FACTS.md#f113), [Q010](OPEN_QUESTIONS.md#q010).

| Documented pattern | Evidence | Transferable idea and boundary |
|---|---|---|
| Instruction, source/map/related cameras, owner/priority | Milestone alarm definition, DOC [F031](RAW_FACTS.md#f031) | Context/next action; no map/video without data, default timeout not client SLA |
| Event/discussion/corrective action work item | Intenseye Actions, VENDOR [F089](RAW_FACTS.md#f089) | Linked measure/history; camera verification claim is not proof of removed cause |
| Action from incident; executor reports completion | Voxel product article, VENDOR [F090](RAW_FACTS.md#f090) | Action/owner/evidence relation; report ≠ verification, no proof all prior HSE tools were inconvenient |
| Zone/count/direction rule builder and follow-up | Protex page, VENDOR [F091](RAW_FACTS.md#f091) | Readable where/when/what/to-whom summary; editor usability/API/states not established |
| Explicit Apply and PPE result filter | Macroscop, DOC [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046) | Draft vs applied state; PPE check is not violation, no inferred archive dry-run |
| Diagnostic path separate from production events | Macroscop, DOC [F036](RAW_FACTS.md#f036), [F037](RAW_FACTS.md#f037) | Test location, broken stage/last good/repair owner; one live frame does not mean fully ready |
| Customer/vendor labels separate | Intenseye Public API v2, DOC [F123](RAW_FACTS.md#f123) | Raw origin + curated result; export does not prove write/learning/gold |

SELF-REPORT G2 context: **Amanda B.**, Sr Director IT Solutions, enterprise, Current User/Validated, **Source: G2 invite**, reports false alerts in **ergonomics**. **Syed Z.**, Regional Project Manager, Validated, **Organic**, describes internal approval time in HSE/construction and four tested scenarios including PPE. **Ariana L.**, HSE/DG Specialist, enterprise, Current User/Validated, **Organic**, identifies data/cybersecurity as primary concern. Invite ≠ proven payment; identities/product version/site were not independently checked. Foreign ergonomics complaints do not measure Russian PPE performance or represent HiTech workers. These motivate tests of review load, approval and data protection, not comparative superiority of our UI. [F114](RAW_FACTS.md#f114), [S077](SOURCES.md#s077).

INF interface defaults: distinguish risk priority, handling stage and review result with text/icons, not color alone. Prefer Russian labels identifying object: «Ответственность принята», «наблюдение подтверждено проверяющим», «исполнитель сообщил», «выполнение проверено». Use meaningful place/camera names rather than IP. Terms require client agreement. [F098](RAW_FACTS.md#f098), [F132](RAW_FACTS.md#f132).

DOC **WCAG 2.2**: normal text **4.5:1**, large text **3:1** with exceptions; meaningful graphics/controls **3:1** under applicable conditions; keyboard access, visible focus and status messages; AA Target Size Minimum **24×24 CSS px** or defined exceptions, dragging alternative when applicable. This is a web minimum, not glove/video-wall ergonomics. Full ISA-101/TR101.02 were not read; committee scope does not establish a palette, screen count or mandatory dark theme. American Water HMI material remained unavailable, **F096 UNKNOWN/rejected lead**. [F095](RAW_FACTS.md#f095), [F096](RAW_FACTS.md#f096), [F097](RAW_FACTS.md#f097), [E012](RAW_FACTS.md#e012).

## Product → architecture contract: 17 data groups and missing-data behavior

INF requirements below are not a received HiTech API. **M** = needed for trustworthy provenance/card; **C** = needed for the conditional feature. Missing M does not authorize fabricated values: retain incomplete candidate/diagnostic and withdraw affected claim. Fields may live in linked entities rather than one payload. First obtain one real event + accessible media + mode/clock/health, then failure fixtures. No stream passwords/tokens in cards, exports, traces or demo recordings. Metadata-only input can register/route a candidate but cannot enable visual confirmation. [F134](RAW_FACTS.md#f134), [Q005](OPEN_QUESTIONS.md#q005).

| Group | Truth owner / minimum content | Missing → product fallback and withdrawn promise |
|---|---|---|
| 1 M event identity | Generator/adapter: `event_id`, `schema_version`, `source_event_id/idempotency_key` | Local `receipt_id`, source identity unconfirmed; no cross-system dedup/trace |
| 2 M source/place | Registry/integrator: `source_system`, camera/site/area IDs, `mapping_version` | Unmapped source; no guessed field destination/person ID |
| 3 M input binding | Ingest/VMS/file: `input_ref`, frame/PTS/range, `source_time_basis` | Event evidence unavailable/insufficient; live separate |
| 4 M observation time | Source clock ID, nullable start/end, timezone/offset, sync/uncertainty | Preserve raw timestamp/basis; no invented local time/duration/latency |
| 5 M record processing time | Server `received/update/revision`; upstream generated time separate | Receipt does not replace occurrence; only supported local intervals |
| 6 M mode | Driver/job: `live/replay/stored_result`, replay session, processed time | Provenance mode unconfirmed; no real-time claim |
| 7 M result/versions | Violation method/runtime/rule registry: type/result, rule/model refs | Version unavailable; no reproducible rerun claim; unfiltered PPE check not violation |
| 8 C geometry | Rule/preprocessing: coordinate space/resolution, overlay, view revision | Hide incompatible overlay; retain original and text rule |
| 9 C media/readiness | Media/VMS: refs/range/gaps/origin, `pending/ready/failed/not recorded/expired/forbidden` | Frame + pending, frame-only or explicit absence; no unsupported pre/post/duration |
| 10 C media access | Auth/media owner: allowed actions, expiry, original/masked/overlay | Forbidden distinct from absent; permitted access request/insufficient; export disabled |
| 11 M control health | Each stage: camera/decode/inference/event/media, test origin, checked/last good | Live stream + unavailable analytics shown separately; unknown distinct, test scope/age visible |
| 12 C freshness/current state | Architecture + policy: freshness, evidence/`as_of/valid until` | Historical event retained; current hazard stale/unknown; old frame cannot justify current intervention |
| 13 M human work | Our ledger/agreed external system: review/origin/revision, owner/acceptance, delivery attempts, measure refs | Unknown ACK stays unknown; system origin distinct; explicit version conflict |
| 14 C LinQ provenance | Platform/runtime: job/input/model/result/execution artifact, processing times/environment | LinQ execution unconfirmed. Although C for UI feature, **mandatory case input remains blocked** |
| 15 C external record | Actual receiver: ticket/ref, integration/mapping version | JSON/CSV is export, not connector/human-accepted measure |
| 16 C privacy/renditions | Media/auth/policy: rendition/masking lineage, original/export/attach rights, recipient/channel/purpose | No unauthorized display/attachment; masked thumbnail says nothing about original |
| 17 C management cohort | Analytics: scope, observed interval, review snapshot/selection, camera×rule×version health, measure applied time | Local list only; no rate/ranking/recall from incomplete data |

### Clock domains and six failure cases

Source/NVR wall clock, file **PTS** timeline, server audit wall clock, server monotonic local durations, remote-job clock, media-ready time, device click and server acceptance are distinct. **PTS is not Unix time**. Cross-domain latency requires mapping/sync/uncertainty; Macroscop webhook local timestamp may be server time rather than camera time. Do not silently “fix” negative delay after clock jump. UI can use observation/source/mode, received time, media state and current-state age. INF [F084](RAW_FACTS.md#f084), [F135](RAW_FACTS.md#f135).

| Failure | Expected behavior | Claim removed |
|---|---|---|
| Event arrives before clip | Candidate + available frame; clip pending; insufficient allowed; policy warning may proceed | Complete context before media ready |
| Frame only, no archive | Explicit frame-only; review limited to visible evidence | Pre/post, duration proof, archive miss search/recall |
| Late event | Occurrence time/age, historical/replay/stale label, separate live | Current hazard/timely intervention from old image |
| Camera moved | View-revision mismatch, zone requires review/retest | Previous ROI ready merely because picture is live |
| Transport/system retry | One source event/operation with attempts/retry; real new episodes separate | Retry as a new violation; unknown dedup cannot silently hide load |
| Live works, LinQ unavailable | Camera ok / inference unavailable; old result `as_of`; no invented new detections | Full control and compliance with mandatory inference |

These are proposed contract cases, not executed failures. Actual LinQ input→model/job/environment→result→event→review linkage needs an accessible secret-free execution artifact. **CPU/RTX, a UI badge or unproven stored result is not proof.** A proven stored result can be a labeled demo reserve; replay proves recorded-input processing, not end-to-end live real time. One successful job proves neither throughput, accuracy nor reliability. [F103](RAW_FACTS.md#f103), [F135](RAW_FACTS.md#f135), [E011](RAW_FACTS.md#e011).

### Corporate integrations and regulated terminology

VMS owns source/archive/time/rights; access control owns credential events, not automatic identity of nearest person; PPE inventory owns issuance/norms, not wearing; HSE register owns its observation/measure process; MES/EAM/permit supplies scoped current state only through a concrete interface. Missing/stale does not mean permitted. DOC/INF [F082](RAW_FACTS.md#f082), [F083](RAW_FACTS.md#f083), [F085](RAW_FACTS.md#f085), [F087](RAW_FACTS.md#f087).

Choose one real test exchange with returned external ID. 1С HTTP-service capability is not a ready HSE-create endpoint: configuration/release/customizations/object schema/publication rights/owner/test environment are needed. Macroscop webhook examples expose localized enums/numbers and missing variables left literally in text. HTTP 200/202 is technical result, not human acceptance or measure execution. If only JSON/CSV exists, call it export. DOC/INF [F084](RAW_FACTS.md#f084), [F086](RAW_FACTS.md#f086), [F130](RAW_FACTS.md#f130), [Q014](OPEN_QUESTIONS.md#q014), [E010](RAW_FACTS.md#e010).

UI names «Сигналы»/«Видеоэпизоды» are proposed. A narrowly read Article 1 industrial-safety-law copy associates formal «инцидент» with technical-device failure/damage at hazardous facilities or process deviation; site applicability was not established. This is terminology evidence, not legal advice/compliance finding. ПАБ, stop-card, prescription, formal investigation and official act have their own procedure. `supported` does not establish guilt, sanction admissibility or Russian compliance. Do not claim injury prevention, universal SLA/retention or protective control. Door/machine/siren commands are not just another notification adapter; formal/protective scope would require redesign with requirement owner. INF/UNKNOWN [F111](RAW_FACTS.md#f111), [F142](RAW_FACTS.md#f142), [Q016](OPEN_QUESTIONS.md#q016).

## Conditional 45-hour MVP priorities and reduction gates

**HYP:** P0 is the demonstrable path, not a promise of full-case compliance or measured effort. P1 means one justified extension after P0, not all P1 items. Full case can add mandatory classes/metrics. Criterion mapping is INF from [F100](RAW_FACTS.md#f100); novelty needs separate case-based justification, not more screens. Privacy/rights/provenance/mode constrain every row. [F136](RAW_FACTS.md#f136).

| Priority / user task | Basis | Criterion and demonstrable artifact | Dependency and first reduction |
|---|---|---|---|
| P0 actual mandatory inference | [F099](RAW_FACTS.md#f099), [F103](RAW_FACTS.md#f103) | Prototype/main problem: input/model/job/result/event refs + execution artifact | LinQ/runtime/input rights from platform/model owners; no access blocks compliance. Remove classes/effects first; CPU/RTX no substitute |
| P0 know what/where is controlled | [F036](RAW_FACTS.md#f036), [F044](RAW_FACTS.md#f044), [F046](RAW_FACTS.md#f046) | Prototype; conditional deployment: one mapped source/rule/time/mode/version/health | Registry/sample/real path; read-only config/file instead of discovery/bulk wizard; file labeled replay |
| P0 evaluate evidence/retain uncertainty | [F031](RAW_FACTS.md#f031), [F132](RAW_FACTS.md#f132), [F134](RAW_FACTS.md#f134) | UX/UI/main problem: actual frame/clip + supported/false/insufficient/not applicable with author | Media/time/rights; frame-only removes timeline/pre-post/duration; no image means visual-review path incomplete |
| P0 see outage/late result | [F037](RAW_FACTS.md#f037), [F135](RAW_FACTS.md#f135) | Secondary problems/prototype: real failure or labeled fixture, last good/age/stale/replay | Stage health; status/reason instead of monitoring dashboard; fixture is not measured infrastructure failure |
| P0 persist human decision/history | [F130](RAW_FACTS.md#f130), [F132](RAW_FACTS.md#f132), [F133](RAW_FACTS.md#f133) | UX/UI/prototype: server-accepted decision, stable demo role, origin, revision/retry/conflict | Small store/auth/idempotency; reduce full IAM/SSO/task system, not history |
| P1 Map A handoff | [F056](RAW_FACTS.md#f056), [F140](RAW_FACTS.md#f140) | UX/UI; conditional deployment: attempt + actual test receive + explicit human ACK | Channel/token/device/recipient/permission/E004; internal demo role if missing, remove adapter/escalation |
| P1 act on observation/cause | [F018](RAW_FACTS.md#f018), [F106](RAW_FACTS.md#f106), [F141](RAW_FACTS.md#f141) | Main problem/UX: one measure/action/owner linked to episodes and completion report | Actual need/owner; one card field + measure ID, no task board/default deadline/generative agent |
| P1 verify only by policy | [F090](RAW_FACTS.md#f090), [F133](RAW_FACTS.md#f133) | Conditional deployment/secondary: verification basis or honest not required | Verifier/policy/evidence; retain “executor reported” if missing, no universal second person/no-event verification |
| P1 one checked configuration change | [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046), [F052](RAW_FACTS.md#f052) | UX/conditional deployment: ROI/condition + Apply/version snapshot in new event | Coordinates/view/positive-negative samples; read-only config instead of universal editor, bulk, text rules, schedule/rollback UI |
| P1 route feedback to subject review | [F123](RAW_FACTS.md#f123), [F126](RAW_FACTS.md#f126) | Secondary/conditional analytics: raw opinion/reason/origin + actual backend result | Owner/storage/reuse rights; flag for review, no auto-learning/tuning/active-learning dashboard; no archive means no recall |
| P1 management demo, otherwise P2 | [F068](RAW_FACTS.md#f068), [F141](RAW_FACTS.md#f141) | Analytics/conditional main problem: recurrence/unfinished-measure question with links/coverage/selection | Applied time/perimeter/health/owner; list rather than trend/risk ranking/LTIFR; may precede editor/channel |
| P2 external register | [F084](RAW_FACTS.md#f084), [F086](RAW_FACTS.md#f086), [F087](RAW_FACTS.md#f087) | Conditional deployment: tested exchange/external ID or labeled export | Actual version/schema/access; JSON/CSV only without receiver, no universal connector claim |
| P2 or separate mandatory full-case path: local warning | [F107](RAW_FACTS.md#f107), [F108](RAW_FACTS.md#f108) | Conditional main problem/deployment: real permitted output plus later review | Policy/freshness/safe test/real perimeter; async review if missing; browser audio not field warning |

**Minimum A:** one source/rule/card/history, one negative branch, explicit internal human role, actual LinQ trace; measure only when needed. **Extension B:** add one confirmed bottleneck—external channel, measure/verification, rule edit, or management list—then rerun the same end-to-end route. No assumed ERP, identity recognition, mobile app or bulk editor. No measured person-hours or assignment of the five team members was established. [F136](RAW_FACTS.md#f136).

Reduction gates, HYP: (1) full case: recheck classes/metrics/real-time/artifacts and role; (2) first actual input→LinQ→result: if absent, reduce extensions and record mandatory blocker, fixtures remain fixtures; (3) first event→media: select frame-only/late/no-rights branch immediately; (4) first human decision: demo role if recipient/channel absent, optional verifier removed only within policy, pattern-level measure if justified; (5) first rehearsal: cut unsupported/breaking extension according to cause. **Never cut provenance, mode, health or mandatory LinQ to preserve decoration.** Proven saved LinQ output/recording can be reserve with `stored_result`/mode label; it does not prove live real time. [F100](RAW_FACTS.md#f100), [F103](RAW_FACTS.md#f103), [F136](RAW_FACTS.md#f136), [Q017](OPEN_QUESTIONS.md#q017).

### Three working surfaces

HYP, not a delivered layout or usability result [F104](RAW_FACTS.md#f104), [F136](RAW_FACTS.md#f136):

1. **Episodes + card panel:** Map A queue or Map B backlog/history. Place/rule/time/age/mode/media/review/owner distinct; actual original/overlay by rights, independent states, attempts/acceptance, optional measure and ordered history; health/last good nearby. Enough for P0.
2. **Source + rule:** readable camera×rule summary, test location, stage health, view/rule versions, ROI/condition/enabled state. Edit/Apply only with actual backend and checked samples; no RTSP secrets on stage.
3. **Period review, conditional:** linked episodes/measures, execution/verification and next-action question with coverage/selection. If scope unknown, keep links in card instead of BI/task system.

An approved mobile path can adapt place/evidence→accept→report action. A second laptop is labeled internal role, not a foreman's phone in a factory. Device/network/safe viewing remain unknown. [F079](RAW_FACTS.md#f079), [F080](RAW_FACTS.md#f080), [F140](RAW_FACTS.md#f140).

### Two alternative five-minute demos

Both are **HYP, NOT REHEARSED**, not both required within five minutes. Need permitted input, checked rule and actual LinQ result tied to execution artifact. Replace role/class/mode after full case. A labeled fixture can illustrate history/negative branch, never client outcome. [F137](RAW_FACTS.md#f137), [E013](RAW_FACTS.md#e013).

| Time | Demo 1: evidence reaches accountable decision | Demo 2: later review turns recurrence into a measure |
|---|---|---|
| Opening | 0:00–0:30 role/need and camera×rule; Map A or explicit demo role | 0:00–0:35 review owner/source mode; local output only if authorized/tested |
| Actual processing | 0:30–1:30 permitted input→real job/result→event; mode labeled | 0:35–1:35 input→real LinQ→episode evidence/place/time/rule/coverage |
| Human assessment | 1:30–2:30 actual material/place/version, supported/false/insufficient | 1:35–2:35 reviewer assesses and links measure or action/owner; several events can share measure |
| Next action | 2:30–3:30 second person explicitly accepts; optional justified action/measure | 2:35–3:35 reported execution, verification and post-application episodes only if data exists |
| Negative branch | 3:30–4:20 false detection + system ACK, or pending/forbidden evidence; no false resolution | 3:35–4:25 unavailable camera/rule and no new events; zero is not success |
| Finish | 4:20–5:00 real history, unfinished work, unknown and next input | 4:25–5:00 owner selects next step/history; no risk/injury-reduction claim |

Choose demo 2 without a constant operational recipient or for a confirmed management task. Shorten to one card/measure when history is unavailable; no invented “safer after deployment.” Frame-only removes player expectation. Do not require create→complete→second verifier if policy does not require it. No channel means no field-delivery claim. [F133](RAW_FACTS.md#f133), [F136](RAW_FACTS.md#f136), [F140](RAW_FACTS.md#f140), [F141](RAW_FACTS.md#f141), [F147](RAW_FACTS.md#f147).

## Proposed checks E001–E015: all NOT RUN

These are HYP procedures for later authorized practice, not tests performed during research/compression, and not a requirement to run all fifteen before submission. Keep secret-free inputs, versions, decisions and observations; actual recording/synthetic fixtures are labeled. The linked E record contains fuller protocol. Scope success never implies injury prevention, Russian compliance or full-case completion.

| ID / status | Question and required inputs | Actions, evidence and metrics | Outcome changing decision / limit |
|---|---|---|---|
| [E001](RAW_FACTS.md#e001) NOT RUN | Recipient/state semantics; anonymized client route, duty/authority matrix, statuses/payload, completion policy | Walk false+auto-ACK, two events/one measure, pending shift, outage, concurrent decision, offline action. Save before/after, actor/origin/times/revision/request ID; count false acceptance/resolution, lost owners, duplicates | No duty/window → async; second verifier only by policy. Paper/prototype success not real shift or prevention |
| [E002](RAW_FACTS.md#e002) NOT RUN | Episode queue/load; permitted video, labeled episode boundaries, frame-vs-episode presentations, participant with parallel task | Alternate order for same burst/repeat/false/unclear sequence; no silent drops, suppression scope/reason/expiry. Compare per-event vs cause-level measures if allowed. Save groups, false unique episodes/hour, backlog/max, critical misses, review/first-action/active time, unfinished tasks | Hidden people/zones → change grouping; overload → change notifications/resource. Five team members not representative shift/norm |
| [E003](RAW_FACTS.md#e003) NOT RUN | Card sufficiency; permitted occluded helmet, ambiguous zone, ended-action frames/clips and allowed renditions | Unaided place/feature/applicability/sufficiency/next-role decisions; pending/forbidden, late event vs live. Save prototype capture/media version, location/action errors, overclaims, evidence requests and decision time | Confused live or guessed respirator → change labels/material/rights, remove unsupported judgment. Fast click not sufficient; no precision/sanction-admissibility result |
| [E004](RAW_FACTS.md#e004) NOT RUN | Field delivery/reserve; site/IS/OHS permissions, payload, safe device place, main/deputy contacts, owner and useful window | Normal path then no network, locked screen, DND, push denied, expired token/session, changed recipient, unavailable clip; actual receive confirmed by recipient/observer, reserve separately. Voice intelligibility under actual noise/PPE and emergency distinction only safely. Save event/observation/send/receive/human ACK/action times with clock uncertainty, errors/reserve receipt | Failure changes channel/duty/promptness claim. One receipt not reliability statistic or prevented injury |
| [E005](RAW_FACTS.md#e005) NOT RUN | One camera/control readiness; permitted source/owner, reference view, stage health/test origin | Wrong password, laptop/server route asymmetry both ways, inference down with live, no recording, view shift/overexposure. Save test place/time/last frame/last good/reason/repair owner/recovery and ready/unavailable/unknown | Global ready during failed analytics → split statuses. One source not PPE accuracy, hundreds of streams or LinQ proof |
| [E006](RAW_FACTS.md#e006) NOT RUN | Rule meaning/change; local condition, allowed positive-negative sample, view version/timezone | OHS states condition, admin configures, another predicts firing; both PPE results, wrong filter, midnight shift, disabled schedule, moved view, new Apply preserving old events; rollback only if built. Save input ref/hash, expectations/results/versions/author/reason/time/fixes | Ambiguous rule stays draft. Editor success not valid exceptions or all-class quality |
| [E007](RAW_FACTS.md#e007) NOT RUN | Feedback/misses; independent continuous permitted archive, times/versions/health/visibility, boundaries/matching, reviewer/curator | Evaluation owner fixes sampling frame/blocks before system results, seed/strata if used; reviewer sees no alert list/overlay, records observable events/unknown/outages/scene changes; independent control/dispute opinions and unresolved outcome retained, then match system. Save plan/blocks/labels/versions/adjudication/matches; FN/TN only in defined observable sample | No archive → suspected misses, no numeric recall. Separate model/rule/ingest/visibility errors; no plant generalization or learning proof |
| [E008](RAW_FACTS.md#e008) NOT RUN | Data path/masking usefulness; clear/ambiguous PPE views, original/masking variants, rights at all real stages including LinQ/temp/cache/contractors | Separately check model/human visibility and permitted original comparison; trace camera→LinQ→media→console→link/attach→export→feedback/training→deletion. Save locations/recipients/purposes/retention owners, input/job/rendition/mask refs and access/export/training logs | Hidden feature → change rendition/rights or remove confirmation. No anonymity/Russian-law/recall/external screenshot-deletion proof |
| [E009](RAW_FACTS.md#e009) NOT RUN | Management reading; event↔measure links, versions/occurrence/applied times, health/perimeter, snapshot/selection and decision owner | Open measure, reported-not-verified completion, no repeat with camera off; labeled added-camera, doubled people-flow, rule-off, selective-review fixtures. Save numerators/denominators/cohorts, decisions/false safety conclusions, pending/censored/off/outage/unknown | Misleading comparison → remove ranking/chart, keep measure/coverage question. No causal benefit/LTIFR reduction |
| [E010](RAW_FACTS.md#e010) NOT RUN | One exchange; authorized versioned receiver/schema, source-place mapping/timezone | Send type then duplicate ID, missing field, wrong camera/timezone/localized enum/literal missing variable, receiver unavailable/external ID, auth expiry/original-export rights/retries. Save secret-free requests/responses/schema/mapping/IDs/idempotency/error queue | JSON/CSV only → export label. One exchange not all-config compatibility or permission to command door/machine |
| [E011](RAW_FACTS.md#e011) NOT RUN | LinQ provenance/failures; actual authorized access/artifact, input/rule, source/time/media/health | Link input→model/job/environment→result→event→review, secret-free artifact, clocks/sync/uncertainty/mode; exercise six contract failures without fake live/trace, retain server history | No artifact → mandatory LinQ open; CPU/RTX/badge no substitute. Replay not live; one job not throughput/accuracy/reliability |
| [E012](RAW_FACTS.md#e012) NOT RUN | Accessibility/meaning; own prototype, keyboard/screen reader, measured contrast, ideally actual monitor/distance/light/client terms | Queue/card/decision without mouse/color; focus/status, dragging alternative and applicable WCAG exceptions; reading distance/status meaning. Field/gloves only authorized. Save own screenshots/contrast/keyboard path/read/meaning errors and actual-vs-lab environment | Fix violations; choose density/theme from observation. Short test not long shift or competitor audit |
| [E013](RAW_FACTS.md#e013) NOT RUN | End-to-end minimum/demo; received full case, permitted input/rule, actual LinQ artifact/media/test role | Unaided participant gets/decides, second optional field role, third verifies provenance. Chosen minimum + negative branch, reductions at gates. Save screen recording/input-job-event-review-delivery-action refs, timeline/roles/mode/real-vs-conditional, place/false-closure errors and criterion rationale | No LinQ → incomplete mandatory path; no duty → later review; no clip → frame/insufficient. Reserve recording only actual route; no factory benefit/accuracy/full unseen-TZ claim |
| [E014](RAW_FACTS.md#e014) NOT RUN | Wrong advice/cost of review; safe permitted ambiguous clips with deliberately wrong predictions | Compare direct judgment with evidence+short reason; incorrect-advice acceptance, decision correctness/insufficient use, active time/load/preference; save actual backend effect of feedback | Confidence without verification → change presentation; unnecessary workload → reduce optional steps; no forced delay in urgent path without harm assessment. Trust/satisfaction not joint quality/injury reduction |
| [E015](RAW_FACTS.md#e015) NOT RUN | Purpose understanding/appeal; employer/representative permission, approved flow/purposes/sanctions/appeal | Show worker/representative data path/readers/export/training; ask what collected/who sees original/how correct; collect concerns and test appeal without imposed “coaching only” promise. Save de-identified understanding errors/participation conditions/appeal owner-outcome/policy changes | Concerns about real purposes → change policy/rights/communication/pilot criteria. No workforce representativeness/causal consultation/Russian legality proof |

Initial practice needs E001/E003/E005/E011/E013 for an honest path; E004 before field-delivery claims, E008 before privacy/external-copy claims, E007 before recall. Other checks follow selected use case rather than adding all procedures to MVP.

## Open decisions: first HiTech contact and remaining Q-ID map

The first meeting should produce one real route and artifacts, not “notify the responsible person.” Six requests have P0 impact:

1. **Recipient/authority:** current shift recipient, location/device, ability to intervene, night/deputy, combined tasks, list owner; one anonymized observation→action route. Chooses Map A/B and demo role. [Q001](OPEN_QUESTIONS.md#q001), [E001](RAW_FACTS.md#e001).
2. **Class-specific useful window:** required action, interval start/end, permitted pre-review warning, existing protections and warning-vs-protective output. Too-short window removes prompt-intervention promise or requires separate protective scope. [Q002](OPEN_QUESTIONS.md#q002), [Q016](OPEN_QUESTIONS.md#q016).
3. **Full case and real technical inputs:** classes/metrics/modes; LinQ access and input→model/job→result artifact; one event/media/time/health payload, frame/archive/pre-post/clock mapping/rights. Chooses P0, frame vs clip and real-time boundary. [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005), [E011](RAW_FACTS.md#e011).
4. **Primary/reserve field channel:** permission/device/safe viewing/network/token/recipient/payload and proof of actual receipt; obtain test contact/perimeter. Otherwise internal demo role. [Q006](OPEN_QUESTIONS.md#q006), [E004](RAW_FACTS.md#e004).
5. **Existing document/measure:** assigner/executor/completion/verifier/basis; anonymized observation→measure→reported/verified execution and external ID/classifier. Chooses measure scope without invented act. [Q003](OPEN_QUESTIONS.md#q003).
6. **Purposes and full copy path:** original/NVR/LinQ/temp/cache, view/export/attach/QA/train recipients/contractors/retention, sanctions and appeal. Need approved mode rather than “anonymous.” [Q008](OPEN_QUESTIONS.md#q008), [E008](RAW_FACTS.md#e008), [E015](RAW_FACTS.md#e015).

Remaining UNKNOWNs retain specific closure routes, not assumed answers:

| Q | Missing decision input | How to close / effect |
|---|---|---|
| [Q007](OPEN_QUESTIONS.md#q007) | Independent archive and subject curator | Artifact/access + E007; permits bounded missed-event evaluation rather than miss candidates |
| [Q009](OPEN_QUESTIONS.md#q009) | Direct workers/representatives' views and usable appeal | Authorized consultation + E015; changes purposes/rights/rollout, no presumed consent |
| [Q010](OPEN_QUESTIONS.md#q010) | Observed competitor workflow and tolerable manual effort | Future accessible product surface + actual task observation; documentary patterns are not UX audit |
| [Q011](OPEN_QUESTIONS.md#q011) | Rule/exception approver, versions, archive dry-run need | Client condition/artifact + E006; chooses editor/configuration scope |
| [Q012](OPEN_QUESTIONS.md#q012) | Real workspace/load/device and suitable density | Expert/workplace observation + E002/E012; no borrowed camera/time quota |
| [Q013](OPEN_QUESTIONS.md#q013) | Summary reader/decision and comparable exposure | Actual report/process/perimeter + E009; determines list vs valid comparison |
| [Q014](OPEN_QUESTIONS.md#q014) | Required VMS/access-control/1С/HSE versions and exchange | Named configuration/schema/test access + E010; export vs tested connector |
| [Q015](OPEN_QUESTIONS.md#q015) | Applicable industrial HSE-AI specification with roles/fields/SLA | Actual client/TZ artifact; inaccessible procurement attachment is not a requirement |
| [Q016](OPEN_QUESTIONS.md#q016) | Formal incidents/reporting/protective scope and Russian applicability | Requirement owner + legal/process specialist; advisory prototype may be insufficient |
| [Q017](OPEN_QUESTIONS.md#q017) | Minimum fitting actual case/access/rehearsal | Received inputs + E013/gates; no measured effort promise |
| [Q018](OPEN_QUESTIONS.md#q018) | Masking hides PPE/respirator for model or reviewer | Permitted original/derivative comparisons + E008; display/input paths separately |
| [Q019](OPEN_QUESTIONS.md#q019) | Who evaluates/releases improvement after feedback | Named data/model/evaluation owners, rights, independent test/release artifacts; no click-to-learning claim |
| [Q020](OPEN_QUESTIONS.md#q020) | Evidence of process benefit beyond detection counts | Agreed real participants/perimeter/process measurements + E009; no count-to-prevented-injury conversion |

## Addressed handoffs to neighboring topics

Neighbor reports are unavailable in this folder; no paths/results are invented. These are prepared evidence handoffs, not messages sent to external people.

| Topic | Evidence / decision changed | Required next input |
|---|---|---|
| `video_architecture` | [F134](RAW_FACTS.md#f134), [F135](RAW_FACTS.md#f135), [F122](RAW_FACTS.md#f122), [F140](RAW_FACTS.md#f140): 17 groups, clocks/media/rights/stage health/freshness/retry/revision constrain trustworthy card and delivery | One real payload+media; source/PTS/wall-clock mapping/uncertainty, health/test origin/auth expiry/LinQ temp-cache path; six failure fixtures; no numeric SLA established here |
| `linq_platform`, `model_stack` | [F099](RAW_FACTS.md#f099), [F103](RAW_FACTS.md#f103), [F137](RAW_FACTS.md#f137): mandatory execution and input/model/job/result/artifact/mode | Actual access/artifact linkage, format/location and masked/unmasked input; job success separate from real-time/throughput |
| `violation_methods` | [F029](RAW_FACTS.md#f029), [F046](RAW_FACTS.md#f046), [F050](RAW_FACTS.md#f050), [F133](RAW_FACTS.md#f133): boundaries, PPE result vs violation, geometry/view revision, people/zone grouping | Start/end/matching, coordinate transform/freshness, changed-view samples; same type is not transport duplicate |
| `evaluation` | [F127](RAW_FACTS.md#f127), [F135](RAW_FACTS.md#f135), [F141](RAW_FACTS.md#f141): archive/unknown/outage, selection/censoring/clocks; reviewed-only not recall, counts not prevention | Sampling/matching/quality/visibility protocol, independent exposure where needed; E002/E007/E009/E011; no FN inferred from event clips |
| `datasets`, `training_strategy` | [F123](RAW_FACTS.md#f123), [F126](RAW_FACTS.md#f126), [F122](RAW_FACTS.md#f122): raw origin, curated revision/unresolved, curation vs training rights; disputed/invisible not gold | Named curator/data owner, lineage/recipients/rights, independent test set, release/evaluation; feedback button not automatic training |
| `market_deployment` | [F117](RAW_FACTS.md#f117), [F120](RAW_FACTS.md#f120), [F122](RAW_FACTS.md#f122), [F142](RAW_FACTS.md#f142): cloud-original exception/scope ambiguity, purposes/sanctions/copies/authority/terms | Russian law/hazardous-site/local policy, per-copy retention/original-export-training/appeal, advisory-vs-protective boundary; foreign guidance/template not compliance |
| `hackathon_strategy` | [F100](RAW_FACTS.md#f100), [F136](RAW_FACTS.md#f136), [F137](RAW_FACTS.md#f137), [F143](RAW_FACTS.md#f143), [F144](RAW_FACTS.md#f144), [F145](RAW_FACTS.md#f145), [F146](RAW_FACTS.md#f146), [F147](RAW_FACTS.md#f147): one conditional hero/path, negative branch, reduction gates, understandable management result | Full case/classes/metrics, real mode/media/channel/proof and actual E013; do not sum all P1 into must-have or predict jury scores |

The next demonstrable product result is a person correctly locating permitted evidence of known provenance, understanding its limits, saving a decision and seeing the unfinished next step. Factory benefit requires a separately agreed perimeter, real participants and process measurements; a detection counter or five-minute rehearsal cannot establish it. HYP/UNKNOWN [F136](RAW_FACTS.md#f136), [Q017](OPEN_QUESTIONS.md#q017), [Q020](OPEN_QUESTIONS.md#q020).
