---
topic: hackathon_strategy
context_version: mosprom-research-v1
checked_at: '2026-10-23T11:26:02+03:00'
checked_at_scope: 'Local reading, compression and document consistency only; no renewed external verification'
timezone: Europe/Moscow
scope: >-
  Evidence-based preparation for five people in the 45-hour Otkroy#Mosprom 2026
  industrial-safety video case from ООО «ХайТэк», including mandatory LinQ inference,
  rules, unresolved permissions, scoring, scope selection, execution, checkpoints,
  quality claims, demonstration, defence, submission and post-defence obligations.
not_covered:
  - 'linq_platform: current SDK implementation, compiler support and device qualification'
  - 'model_stack, training_strategy: selecting or training the final model'
  - 'datasets, violation_methods, evaluation: full data, recognition and evaluation research'
  - 'video_architecture, operator_product: production architecture and user research'
  - 'market_deployment: market sizing, prices, ROI and field deployment verification'
  - 'Ready-to-submit code, slides, teaser, speech or demo script'
answers:
  - 'What do the saved 2026 rules require, and which FAQ/PDF conflicts remain unresolved?'
  - 'Are criterion weights, score aggregation and checkpoint contributions known?'
  - 'What do past Mosprom winners, comparable cases and LinQ precedents actually establish?'
  - 'What is publicly known about the sponsor, experts and current case jury?'
  - 'How should scope change with the full case, data, access mode and mandatory endpoints?'
  - 'What should the team decide in the first two hours and ask in the first hour?'
  - 'How can five owners coordinate interfaces, integration, sleep, freezes and late access?'
  - 'What belongs in each checkpoint package, and what remains unknown about admission?'
  - 'What is the minimum proposed proof of a completed LinQ run for shell/service/job/catalog?'
  - 'Which quality and speed claims are supported by each available reference/log configuration?'
  - 'How should live, recorded and fallback demonstrations fit the 2+5+3-minute defence?'
  - 'Which Q&A topics are reported versus anticipated, and how should answers use 180 seconds?'
  - 'How do originality, AI, paid resources, assistance, recording, licensing and IP affect work?'
  - 'How should the team submit, preserve links, attend awards and handle prize paperwork?'
  - 'Which proposed checks and addressed handoffs should guide the next work?'
keywords:
  - Otkroy#Mosprom
  - Открой#Моспром
  - ООО «ХайТэк»
  - LinQ
  - TPU
  - PPE
  - industrial safety
  - accepted witness
  - target mapping
  - checkpoint
  - CP
  - 45 hours
  - ground truth
  - source camera-hours
  - wall-hours
  - D_useful
  - 2+5+3
  - AGPL-3.0
  - AI disclosure
  - section 7.3
  - 90 working days
availability:
  full_case: not_received
  team_account_and_individual_slots: not_received
  issued_linq_access: not_received
  matching_sdk_and_device: not_received
  production_video_gt_and_team_runtime_logs: not_received
verification:
  basis: 'Saved two-wave research and final human report; compressor used local materials only'
  source_access_date: '2026-10-23; individual publication/revision/event dates remain in SOURCES.md'
  reported_research_windows:
    wave_1: 'Approximate task windows 09:31-09:50 Europe/Moscow; per-request timestamps under _WORK/SOURCES'
    wave_2: 'W2A 10:00-10:07; W2B completed about 10:14; W2D 10:07-10:18 Europe/Moscow; other per-request timestamps under _WORK/SOURCES'
  window_limit: 'Reported task windows are not exact first/last network-call bounds; checked_at is later local synthesis time'
  own_linq_inference_runs: 0
  observed_video_runtime_and_qa_fragments: 0
  model_training_benchmark_and_app_execution: not_performed
  proposed_checks: 'E001-E010; none performed'
  regulation_and_vendor_pdf: 'Text extractions only; original bytes/hash/visual pages absent'
  faq: 'Russian browser-agent text; delivered HTML/images absent; erroneous English summaries excluded'
  operator_report_2025: 'Browser-reported pages 1-13 of 41; pages 14-41 unchecked'
files:
  human: report_human_hackathon_strategy.md
  sources: SOURCES.md
  facts: RAW_FACTS.md
  criticism: CRITIC.md
  open_questions: OPEN_QUESTIONS.md
  provenance_map: _WORK/ID_MAP.md
  addressed_handoff: _WORK/COLLECTOR_HANDOFF.md
entity_schema:
  criterion: [criterion, evidence, limit]
  analogue: [case, established_basis, lesson, limit]
  outcome: [outcome, prerequisites, acceptance, limit]
  branch: [id_condition, action, owners, limit]
  owner: [owner, output, recipient_backup]
  contract: [boundary, agreed_fields]
  timeline: [moment_msk, status, action, guard]
  checkpoint: [checkpoint, package, decision]
  question: [timing_owner, ids, request, decision]
  access_proof: [mode, save_first, trust_limit]
  claim: [inputs, allowed, forbidden, next_input]
  defence_budget: [function, seconds, evidence]
  qa: [id, status, topic, evidence_owner]
  procedure: [id, status, question, inputs_actions, evidence_limit]
  handoff: [topic, decision, evidence_open]
takeaways:
  - 'Complete a real, version-linked LinQ path early; sample, own model and full-case coverage are different milestones.'
  - 'Minimum proposed proof is permitted input + exact model/revision + completion/output + trusted device mapping or an accepted witness; the sponsor decides sufficiency.'
  - 'Seven PDF criteria versus six FAQ criteria remain unresolved; equal 0-3 scales establish neither weights nor a final maximum of 21 nor a CP contribution.'
  - 'Use one shared runnable release and small transfers between five owners; mandatory endpoints cannot be removed to declare an MVP complete.'
  - '225/145/30 person-hours are conditional calendar upper bounds, not productivity or coding budgets; downstream durations remain unknown.'
  - 'Choose one reference-supported result with counts, support, denominator, unknowns, close and NA; delivered-alert census does not establish recall.'
  - 'Recording/publication, paid tools/compute, assistance and AI marking require specific clarification; a budget or accessible link is not permission.'
  - 'Protect CP2 drafts, all four final artifact groups, presenter selection, receipt, 90 working days of links, defence and team attendance at awards.'
  - 'Own LinQ inference and observed Q&A are zero; all E procedures are proposed; this file contains preparation principles rather than submission materials.'
---

# Hackathon strategy: evidence, mandatory outcomes and a recoverable release

Our recommendation is to complete the earliest genuine LinQ run, connect it to a required case outcome, preserve its evidence and then expand. Five owners should maintain one reproducible accepted release. Model quality, useful user action, independent startup, formal acceptance and defence each need their own time. This is a conditional operating policy, not an official scoring formula or a guarantee of winning. [F060](RAW_FACTS.md#f060), [F077-F081](RAW_FACTS.md#f077), [F087-F094](RAW_FACTS.md#f087).

## Evidence legend, date and unavailable inputs

Evidence labels describe the basis; verification status describes what actually happened. `RULE/read` = official regulation or FAQ text with retrieval limitations; `DOC/read` = primary documentation; `CLAIM/read` = statement by a vendor, participant or other interested author; `CODE/read` = static source inspection, not execution; `PUB/read` = another party's published measurement/study under its conditions; `LOCAL/read` = actual local retrieval/comparison observation; `INFER` = our interpretation; `PROP` = our proposed policy/procedure; `UNK` = missing evidence. `RUN/measured` would require an actual team execution: none exists here. Multiple readings or reposts of one origin are not independent corroboration. F/S/Q/K/E identifiers are local to `hackathon_strategy` unless a topic prefix is explicit.

The evidence was assembled on **23 October 2026, Europe/Moscow, UTC+3**; competition dates are **23-25 October 2026**. Saved W1 task windows are approximately **09:31-09:50**; W2A reports **10:00-10:07**, W2B completion about **10:14**, W2D **10:07-10:18**. These describe recorded research work, not certified bounds of every network request; original access records remain under `_WORK/SOURCES`. The later YAML `checked_at` describes local reading/compression/document consistency, **not renewed external checking**. Access date is not publication, approval or revision date. The full case, team account, issued LinQ access, matching SDK/device, production videos, ground truth (GT) and team system logs were not received. **Own LinQ inference = 0; observed video/runtime/Q&A = 0.** Resources reported by the user are five people, RTX 4070, a laptop, possible cloud GPU rental and AI access; OS, VRAM, drivers, skills, budgets and accounts are unknown. Resources do not establish permission to use paid services. [F108](RAW_FACTS.md#f108).

`LOCAL/read`: regulation text extractions W1/W2 match after removing whitespace, but PDF bytes/hash/visual inspection are absent. FAQ is browser-agent Russian text without delivered HTML/screenshots; erroneous English summaries are excluded. Vendor performance PDF is text-only. The operator's 2025 report is browser-reported pages **1-13/41**; **14-41 are unchecked**. Questionable summary totals, including 123, are not accepted statistics. A linked video, API availability or author timestamp is not a viewed fragment. Retrieval failures describe particular channels, not the nonexistence of sources or exceptions. [F024-F027](RAW_FACTS.md#f024), [F041-F043](RAW_FACTS.md#f041), [F055](RAW_FACTS.md#f055), [F058](RAW_FACTS.md#f058), [Q018](OPEN_QUESTIONS.md#q018).

Primary navigation: [human report](report_human_hackathon_strategy.md), [source registry](SOURCES.md), [facts](RAW_FACTS.md), [original criticism and W2 outcomes](CRITIC.md), [32 questions, 10 proposed checks and 14 QA topics](OPEN_QUESTIONS.md). No new network evidence, training, runtime test or video viewing was performed during compression.

## 2026 rules: calendar, deliverables, scoring and admission

`RULE/read`: the [official site](https://hackathon2026.otkroimosprom.ru/) links the [regulation and payment rules](https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf); the organizer may amend rules/schedule, clarifies through [FAQ](https://hackathon2026.otkroimosprom.ru/#faq), and may change CP parameters in the personal account (LK). Save the actual case/rules/FAQ/announcements with time, and check individual slots. Old 2025 instructions are not 2026 rules. [F001-F003](RAW_FACTS.md#f001).

`RULE/read`: team size **3-5**, Russian citizenship, age **18-35**, one team per participant, at least **three confirmations**. FAQ confirmation deadline was **21 October 12:00 MSK**, case assignment **22 October**. Actual team admission is unverified. [F002](RAW_FACTS.md#f002).

| moment_msk | status | action | guard |
|---|---|---|---|
| 23 Oct 13:00 | Public official anchor | Full assignments in LK | Save the received revision; 45 calendar hours to final deadline |
| 23 Oct 16:30 | Public official anchor | Opening | Count the actual attendees' occupied time |
| 23 Oct 18:00 | Public official anchor | CP1 | Our choice is all five attending; official minimum is one full-team CP |
| 24 Oct 11:00 | Public official anchor | CP2 | Three drafts must be uploaded by its start |
| 24 Oct 18:00 | Public official anchor | CP3 | Check individual slot and unresolved mandatory work |
| 24 Oct 19:00-19:45 | Public official anchor | Pitch roast | Reserve time to incorporate agreed changes |
| 25 Oct 10:00 | Official final deadline | Upload final artifacts and select presenter in LK | Receipt and late replacement rules are unknown |
| 25 Oct 12:00-17:30 | Public official anchor | Defences | Use the actual team slot |
| 25 Oct 18:00 | Public official anchor | Awards | Check case slot; team attendance is required by FAQ |

### Four final artifact groups and 90 working days

`RULE/read`: final solution includes **code/case-defined result, teaser, demo, presentation**. Teaser covers general description, technical features and uniqueness; FAQ adds benefit. Regulation definitions and the final-upload FAQ allow a video demonstration **or an accessible prototype**. Another short FAQ answer describes video only; this does not establish a universal video mandate. The full case may impose more specific requirements. [F004](RAW_FACTS.md#f004), [Q016](OPEN_QUESTIONS.md#q016).

The PDF specifically places code on **Яндекс Диск**, lists links to all four groups and limits presentation to **10 Мб**; file extension and MB/MiB interpretation are unspecified. FAQ permits open cloud storage with Яндекс Диск as an example and asks for an attached presentation in LK. `PROP`: keep Git history and place the same frozen code release on Яндекс Диск; attach the presentation and retain an accessible link. A private repository/access request is insufficient; GitHub alone does not literally satisfy the more specific PDF. Resolve publication/rights under §7.3 separately rather than assuming an open archive is authorized. [F005](RAW_FACTS.md#f005), [F017](RAW_FACTS.md#f017).

All listed links must permit download/viewing during the hackathon and **at least 90 working days from announcement of results**, not 90 calendar days or demo-only retention. No final calendar expiry is calculated without a counting convention. Assign a storage owner and margin. A second participant should open every link without authentication, download the code archive, verify playback and version correspondence. Owner access is not reviewer access. Availability does not grant rights to third-party data. [F005](RAW_FACTS.md#f005), [E006](OPEN_QUESTIONS.md#e006).

Before **25 October 10:00**, upload in LK **and select the presenter in its special field**. A chat link is not submission. Fields, accepted formats, receipt, post-deadline artifact changes and presenter replacement are unverified. Representative absence at defence is an explicit disqualification ground. [F006](RAW_FACTS.md#f006), [Q016](OPEN_QUESTIONS.md#q016).

After defence, captain and backup must monitor the case chat, distribute the moderator's award link issued minutes before the ceremony, connect the team, and use the required team name plus presenting person's first/last name. Specific sanction for missing awards is unknown; do not invent automatic prize forfeiture. [F028](RAW_FACTS.md#f028), [Q029](OPEN_QUESTIONS.md#q029).

### Seven criteria, six FAQ entries and unknown formula

`RULE/read`: PDF §§6.1-6.4.7 requires integer **0-3** for every criterion; §§8.4-8.11 requires at least **three jury members per case**, judge name and all criterion scores for a valid form. Exact Russian criterion titles are retained below; explanations are ours. [F008](RAW_FACTS.md#f008), [F010](RAW_FACTS.md#f010).

| criterion | evidence | limit |
|---|---|---|
| Прототип | Accepted runnable version; observable action; reproducible startup | Promised, fixture-based and functioning features remain distinct |
| Решение основной проблемы | Requirement -> implemented outcome -> appropriate check | Binary detection does not establish required violation types |
| Разработка и внедрение | Cost components, access/integration needs, measured effect where available, next pilot check | No invented ROI, zero-cost support or industrial-readiness promise |
| Новаторские идеи | Narrow relevant difference from named baseline/comparator and a test of benefit | A neural network or an undocumented competitor gap is not established novelty |
| Пользовательский опыт (UX) / Пользовательский интерфейс (UI) | Completed target-user action, evidence access, understandable error state | Attractive UI is not user research or model quality |
| Второстепенные проблемы | Named additional problem and a functioning part | Extra features must not displace mandatory work |
| Аналитика | Traceable audience/problem/comparator facts that changed scope | No invented interviews, market shares or generic safety rhetoric |

`UNK/conflict`: technological FAQ lists **six**, omitting UX/UI. It places expert/tracker assessment at CP and jury assessment at defence, but its winner descriptions refer variously to jury scores and all three groups. Weights, level descriptors, sum/mean across judges, missing-score handling, rounding, tie-break and CP contribution are **unknown**. Equal scales do not prove equal weights. **21** is only the hypothetical sum of seven maxima for one simply added form, not the official final maximum. Claims of **1/7** per criterion or “half the points are not ML” are unsupported assumptions from the input prompt. The jury memo should reach judges three calendar days before the start; this does not mean participants receive it. [F009-F010](RAW_FACTS.md#f009), [Q001](OPEN_QUESTIONS.md#q001).

`PROP`: request the current technological LinQ score form/memo, coefficients, aggregation and CP rules. Until clarified, prepare evidence for all seven PDF criteria and prioritize mandatory outcomes over speculative marginal points. Public expert cards do not identify the LinQ jury.

### Checkpoints: requirements versus our operating policy

`RULE/read`: three tracker/expert meetings at assigned times; **at least one full-team CP** for defence admission. FAQ adds **20 minutes**, **two of three visits required**, a representative allowed at the other meetings, and disqualification for two misses or two zero-result CPs. Meaning of zero, one miss plus one zero, presence confirmation, CP2 receipt and treatment of a shared LinQ outage are unknown. A status presentation is not guaranteed nonzero progress. [F011-F013](RAW_FACTS.md#f011), [Q006](OPEN_QUESTIONS.md#q006).

`PROP`: reserve all three; all five at CP1, captain/integrator plus backup for CP2/CP3. Check slot/link/name/audio, establish presence, show the post-start delta and exact blocker, ask for result qualification, material acceptance and next mandatory step. Save answer author, role, time, channel, case version and scope; confirm oral clarifications in an allowed channel. Do not record meetings without permission.

| checkpoint | package | decision |
|---|---|---|
| CP1, 23 Oct 18:00 | Full team; problem/mandatory matrix; first slice; actual artifacts; access/data status and reproducible blocker | Confirm semantics/scope, accepted LinQ proof, nonzero progress definition, missing input owner and time |
| CP2, 24 Oct 11:00 | Uploaded **draft teaser, draft presentation, open-cloud code/case-information link**; shared baseline or exact blocker; actual result versus promise | Confirm receipt; identify highest-priority missing mandatory item; check quality/analytics/deployment claims |
| CP3, 24 Oct 18:00 | Delta since CP2; integrated slice/status; final scope, startup, limits, submission/demo plan | Last critical fixes; accepted short recheck/fallback; actual submission and defence format |

No minimum draft percentage or slide count is established. URL entry alone is not receipt. Use the 20 minutes to resolve dependencies, then repeat decisions/owners; this structure is our proposal, not observed historical CP practice. [F012-F013](RAW_FACTS.md#f012).

## Past winners, analogous failures and sponsor evidence

Use history to identify checks, not to infer current jury preferences or causes of winning. There is no reliably attributed **2025 submitted winner package/revision**. The chain official result -> team/person -> exact submitted code/deck/teaser/demo remains incomplete. Similar functions/dates do not establish identity. [F035-F046](RAW_FACTS.md#f035), [Q019](OPEN_QUESTIONS.md#q019).

`CLAIM/read`: [2025 published outcomes](https://prommoscow.info/news/hackathon-moscow-practical-tasks) name six winners: **221** (ДИПП financial/operational analysis with AI agents); **Хайлоджикс** (Моспром TTR measures by ТН ВЭД code); **SummitTeam** (Технополис Москва employers/universities/jobseekers); **Лайтхаус** (Росатом knowledge answers with uncertain cases transferred to an operator); **Скачать фильмы бесплатно** (Микрон/Р-Фарм internal social network); **Digital Rover** (Яковлев Excel catalog and collaboration). These are brief product results, not criterion scores, architectures or reasons for winning. Our inference is to explain a completed user outcome; no causal claim about its scoring follows. [F029](RAW_FACTS.md#f029).

The university's **357 started/137 finalists/133 final solutions** and contractor's **186 without stage** are not a reconciled funnel. Partial report hints about stages do not close it; questionable **123** is excluded. Non-finishers are not proven disqualifications, and counts do not predict LinQ-2026 win probability. The known MIREA composition of one winner and SoloTech's **second place**, distinct from Digital Rover's first, still do not identify submitted revisions. `trade-defense-platform` names **НейроСанитары**, not Хайлоджикс; the Росатом README is not established as Лайтхаус. [F030](RAW_FACTS.md#f030), [F035-F036](RAW_FACTS.md#f035), [F043-F046](RAW_FACTS.md#f043), [Q030](OPEN_QUESTIONS.md#q030).

| case | established_basis | lesson | limit |
|---|---|---|---|
| Москабельмет, Dec 2021 | `CLAIM/read`: sponsor names МИФИ and completeness of cable-segmentation requirements as reason for selection | Trace requirement -> result -> evidence | One historical jury/case, not 2026 weights; internship invitation is not deployment [F031](RAW_FACTS.md#f031) |
| Returnname, Apr 2022 | `CLAIM/read`: winner of extrusion-operator video sequence case; described as offering “two solutions” | Preserve required temporal semantics | Meaning of two solutions, metrics/artifacts/pilot unknown; no inference that two models are needed. 2022 was in person, **12+7 minutes**, **1-10** scale [F032](RAW_FACTS.md#f032) |
| Cable Justice, 2021-2022 | `CLAIM/read`: МИФИ «Гики-рейв» refined product with enterprise after January internship; July 2022 mobile product/OEE Award | Separate hackathon prototype from owned production refinement | No independent quality/economic effect/users/current availability; award/refinement do not prove reduced industrial risk [F033](RAW_FACTS.md#f033) |
| РЖД 2024, Чёрная уточка | `CLAIM/read`: about **30 videos**, **16** with violations; local/offline interface clarified early; 3DCNN abandoned; Roboflow model unavailable for local download; local YOLO/binary result. Authors report **2nd**, UI/speech **3/3**, completeness **2/3**, startup **1/3** | Ask semantic level/types and run-from-another-machine requirements before training | Participant account, not official protocol. Single-file versus batch is not real-time multistream [F049](RAW_FACTS.md#f049), [F106](RAW_FACTS.md#f106) |
| Black Duck source | `CODE/read`: HEAD `65bb40f68bd1b43f37dba873835d77763ae62cdf`; one file/report/timestamp UI; `get_frames(video_path, 0.5)` samples about one frame per two seconds; class-frame answer | Verify empty/positive/error paths; distinguish sampling from full video throughput | No run. `keys[0]` without empty guard is an unreplicated risk hypothesis, not a proven crash; author CPU speed does not establish live cameras [F050](RAW_FACTS.md#f050) |
| Норникель camera contamination, Dec 2024 | `CLAIM/read`: server effectively accepted baseline YOLO11; alternatives failed; **250 real/147 synthetic** images; author reports first by final metric, second overall | Check official execution path before architecture tuning; improve data/processing around a supported core | No official protocol/server logs. Source HEAD `eba17d4346a6eaf5af154c6ca614f04cebdff519` is **9 Feb 2025**, after event; CPU/example metadata and divergent environments do not identify submitted release [F051-F052](RAW_FACTS.md#f051) |
| AgroCode 2021 | `CLAIM/read`: installation forced framework change; people entered assumed blind zone; DeepSort coordinate changes stretched masks; fix after event. `CODE/read`: HEAD `5791a49299feb008dabdae79050586b85464e9a1`, `fix boxes` | Check coordinate/mask/ID boundaries and spatial counterexamples | No execution/external weights fetched. Author's sleep-loss explanation for deleting training code is not causal experiment; prior-code permission does not transfer [F053](RAW_FACTS.md#f053) |
| Моспром-2025 `mosprom.hack` | `CLAIM/read`: pinned README admits broken whole frontend and unbuilt Docker, commit `4e7c92251f7d0e2f44564180de3a155e53ae962d` | Integrate and independently start early | Rank, defence state and score effect unknown; shared-SHA todaisy repo is one origin [F040](RAW_FACTS.md#f040) |
| ЛЦТ-2025 complaint | `CLAIM/read`: losing participant disputes mandatory-spec treatment | Obtain and record mandatory-scope interpretation | Allegations independently unverified; localhost and repo traffic do not prove absent Docker/code review; reported **6:20** is not observed video [F056](RAW_FACTS.md#f056) |

Reliable separate editions under the exact title in **2023/2024** were not established; do not fill gaps with unrelated events. [F034](RAW_FACTS.md#f034).

`CLAIM/read`: ХайТэк's **11-13 Oct 2024 СЗФО** case involved aircraft detection/classification and adaptation to supplied domestic compute; organizer confirms **НКБТех-1**, **AI Crusades**, **OpenАйАйАй** places. Winner [НКБТех post 8](https://t.me/nkb_tech/8) reports modified YOLOv8, color-to-IR data generation and porting to TPU IVA Technologies. It provides no weights, commit, SDK/runtime versions or physical execution evidence. The post links the [organizer defence recording](https://rutube.ru/video/ce1ce8c6459fe7bece7d31c378f98668/) at **01:08:00**; this is **author-linked, not viewed**. The August ЛЦТ talk is another event. [F047](RAW_FACTS.md#f047), [F057-F058](RAW_FACTS.md#f057), [Q020-Q021](OPEN_QUESTIONS.md#q020).

`CLAIM/read`: **Навигационный интеллект 2025** vendor lists load stability and “false compatibility” among five nominations. Formal meaning and a negative-report acceptance example are absent. Failed compilation, runtime crash, wrong values and hidden execution are our possible diagnostic interpretations, not official definitions. A useful negative report does not replace successful mandatory 2026 inference. [Leader-ID 580121](https://leader-id.ru/events/580121) describes qualification/preparation before the final; those permissions/calendar do not transfer. [F048](RAW_FACTS.md#f048), [F059](RAW_FACTS.md#f059).

`CLAIM/read`: sponsor's public aims include talent, applied problems, AI community and testing domestic hardware. Technofest 2026 motion-controlled Mortal Kombat 3 through LinQ HX illustrates an understandable input -> response, not FPS, accuracy, industrial suitability or jury taste. [F054](RAW_FACTS.md#f054).

The website has mixed ДИПП/ML/industry/design/tracking experts and duplicate cards; it does **not** assign LinQ jury membership. АНО «Моспром» organizes; ООО «КОНТАКТ» handles payments; «Импульс Кода» self-reports organization work. None identifies the LK-2026 developer or proves transparent score aggregation. Alexander Saprykin's professional statement about early constraints suggests bringing a concrete barrier and dependent decision, not a promise of points. [F037-F039](RAW_FACTS.md#f037), [Q031-Q032](OPEN_QUESTIONS.md#q031).

## Useful outcome, observable semantics, novelty and deployment

The short case announcement requires LinQ inference and operational notification; helmet absence, respirator removal, dangerous-zone entry and smoking near combustible materials are **examples, not the recovered full mandatory list**. Helmet detection != helmet-person relation != observable absence != observed removal over time. Smoking alone does not establish adjacent flammables. Training cannot create absent pixel/context evidence. [F088-F089](RAW_FACTS.md#f088), [F095-F096](RAW_FACTS.md#f095), [Q002](OPEN_QUESTIONS.md#q002).

`CLAIM/read`: КГМК July 2025 account describes local sound on entry near an operating line, recording, email and «Суперника» messages. Browser review need not precede the sound. Correct gate passage involves a separate line-disable procedure; automatic protective stop by video analytics is not established. April account supports retrospective operational review, not completion of the planned change. **8 cameras in April/9 in July** are unexplained and not capacity evidence. No ХайТэк workflow, human ACK, numeric SLA or prevented injury follows. [F068-F069](RAW_FACTS.md#f068).

`PROP`: choose an accepted user outcome after the full case. Both branches below are our internal framework, not the sponsor's established process. [F074](RAW_FACTS.md#f074), [E005](OPEN_QUESTIONS.md#e005).

| outcome | prerequisites | acceptance | limit |
|---|---|---|---|
| Timely intervention | Agreed action/useful window **D**; authorized on-shift recipient/deputy/device or approved local output; network, policy and clocks | Event/source/accepted run evidence -> technical delivery -> human receipt -> permitted action, logged separately | HTTP ACK is not human receipt; laptop sound is not shop-floor output. Without D no sufficiency claim; timely claim needs GT onset and compatible clocks. Never create a real hazard for a demo |
| Asynchronous review | Permitted archive/frame/clip, named review owner and operating mode | Owner finds evidence, records `supported/false/insufficient` with history, optionally links measure/assignee; completion report separate from verification | Review does not prevent a past event; frame-only does not prove removal/duration. No material/permission means unavailable, not reviewed. This scope cannot replace a mandatory real-time outcome |

No duty operator may justify a review backlog rather than fictitious immediate escalation, only if the full case permits it. Browser review plus phone call requires actual authority, channel and useful time.

`DOC/read`: Intenseye API v2 already separates alert UUID/camera/rule/time, vendor/customer false-positive assessments and tasks with assignee/deadline/status. Unreviewed can be `null`, not false. GET schemas/examples were read; UI/write/workflow effect was not tested. The [Accuracy API](https://docs.intenseye.com/docs/v2_accuracy/index.html) sample does not define `accuracyRate`; alert sampling is not an independent missed-event reference. [F070-F071](RAW_FACTS.md#f070).

`CLAIM/read`: Cognitive Solutions **19 June 2026** ОТПБ release already claims **PPE + TPU LinQ + reports/notifications**; IVA CV separately lists LinQ hardware support. This defeats a generic “first PPE on LinQ” assertion, but does not prove serial deployment, acceptance, current SKU/SDK, measured HSE throughput or price. `PROP`: test a narrow contribution such as exact input -> model revision -> accepted LinQ witness -> event -> actual test delivery/review -> separate action, with unknowns/failures/late results visible. Compare a named SKU/build under comparable conditions; competitor absence of that function and our superiority remain unproven. If no difference is established, say **novelty not established** and describe the integration contribution. [F072-F073](RAW_FACTS.md#f072), [Q027](OPEN_QUESTIONS.md#q027).

`PROP`: deployment explanation should use cost components, not invented ROI. Obtain/measure compute device/SDK/model/resolution/offered cadence/completions/errors/queue (training, compile and inference separately); storage bytes/retention/replicas/backups; network paths/egress/retries; RTSP/file/ROI/line status/API/identity/RBAC/secrets/audit integration; actual setup/label/review/action/IT effort; rights/licenses/support. Storage is the sum of retained bytes plus copies: unknown bitrate/retention gives no justified GB/price. Browser button is not a finished 1С/СКУД connector. Minimal pilot inputs are one approved process/rule/owner, permitted source/lineage, actual target contract, expected outcome/insufficiency rule, allowed test receiver/channel and rights. No LinQ prices, camera sizing, labor rates, ROI or prevented injuries were established. [F075](RAW_FACTS.md#f075).

## First two hours: intake, composed branches and scope admission

`PROP`: **23 Oct 15:00 is an internal route/status checkpoint**, not a promise to finish LinQ in two hours. Access issuance, compile and queues are unknown. [F095](RAW_FACTS.md#f095).

1. **13:00-13:20:** everyone reads the full case. P5 records mandatory violations/types/episodes/UI/API/metrics/deadlines; P1 inventories issued access/release; P2/P3 inspect native video/labels/time; P4 inspects the required interface. Save case revision/permissions and distinguish current absence from observed removal, frame from event, file from live.
2. **13:20-14:00:** three short parallel checks: supported target path; data semantics/scorer/independent holdout; frame -> response -> event -> presentation contract. P2 first transfers exact model input to P1, then does intake, without two simultaneous full commitments. P5 does not hold P2 in a long call for each label.
3. **14:00-14:30:** choose the first admitted vertical slice; every mandatory endpoint gets known/assumption/blocker plus owner. Unverifiable mandatory work triggers a specific sponsor question.
4. **14:30-15:00:** freeze route revision: live/offline/target-unverified, CP1 result, switch conditions, interfaces, useful model deadline and next dependency review. Explicit fixtures support independent work while missing target proof remains unresolved.

All branch records are `PROP`, grounded in [F096](RAW_FACTS.md#f096). Conditions compose; they are not separate projects.

| id_condition | action | owners | limit |
|---|---|---|---|
| B01: dataset and exact evaluator supplied | Reproduce baseline, exact I/O, split and scorer before external data | P2 intake/holdout; P5 score/support; P1 target in parallel | Object score is not event quality |
| B02: description only or vague metric | Agree priority outcome and small permitted diagnostic protocol | P2/P5 positive/negative/unknown; P3 event contract | Functional feasibility without invented general accuracy |
| B03: long mandatory list | Matrix every endpoint; seek shared compatible core | P5 required/partial coverage; P1/P2 network/data | One early scenario orders implementation; it does not delete remaining requirements |
| B04: violations freely selectable | Choose important observable scenario with data and little new NN graph | P2/P5 importance/support; P1/P3 one core | Second scenario only after first acceptance; announcement examples not automatically supported |
| B05: stable LinQ/docs/sample | Supported sample -> own golden model/input -> case path; immediate snapshot | P1 platform; P2 contract; P3/P4 agreed output | Sample proves that path, not the team's network |
| B06: no docs/import failure/no issued access | One reproducible blocker; request exact sample/release/slot; fixtures for independent work | P1 ticket/status/review time; P5 escalation; P2-P4 independent | CPU-only remains target-unverified |
| B07: queue/manual jobs only | Establish terminal status/result/limits and full short job cycle | P1/P3 IDs/results; P5 offline admissibility | Job simulation or replay does not establish real-time cadence |
| B08: real native site video | Inspect observability, PTS/timebase, geometry, camera/session lineage, negative exposure | P2/P5 GT; P3 decoding/time; P4 material access | One camera/site does not establish generalization |
| B09: no real video, only donor images | Request permitted target clips/stand; inspect rights | P5 permission; P2 diagnostic data; P3 allowed replay | Image result does not prove removal/duration/FP-hour/site operation; no assumed right to film |
| B10: required UI/API/integration | Cross that exact external format/boundary early | P3 API; P4 client/UI | Arbitrary dashboard cannot replace the required endpoint |
| B11: interface free | Shortest result -> source/time/reason/evidence action | P4 minimal UI; P5 utility/claims | Redirect spare time to quality/startup/submission, not extra panels |

Composition example **B01+B03+B07+B08+B10** means scorer-compatible baseline plus required API, all mandatory endpoints and measured job cycle on real video; selecting only a helmet under B04 is not allowed. **B06+B09** yields missing inputs/rights/owners and a removal plan, not an invented finished demo.

### New-feature admission and stop rule

`PROP`: record outcome, mandatory status, I/O, owner, data/SDK/dependencies, check and full remaining path. Admit only meaningful/mandatory work that can pass save -> clean load -> export -> quantization -> compile -> device run -> quality/review -> integration before its useful deadline. Symbolic rule **`now + CP_remaining <= D_useful`**, where `CP_remaining` means **remaining critical path**, not checkpoint. Do not double-count parallel stages or omit queues/retries/transfers. Unknown stage duration first needs a bounded probe; free GPU does not replace a busy engineer. [F087](RAW_FACTS.md#f087), [F094](RAW_FACTS.md#f094).

After mandatory core acceptance, consider one bounded improvement: same-network second violation, minimal zone setting or needed filter. New network/VLM/pose/re-ID cascade, framework change, scratch training, distributed infrastructure/full editor wait for demonstrated slack unless required by the case. Stop for absent signal, rights/access, compatibility, sufficient evaluation, remaining time or degraded mandatory result. Preserve the failure and roll back the **whole** accepted weights/class-map/pre/post/rules/dependency/runtime bundle. Rolling back weights alone does not restore a changed system. [F087-F089](RAW_FACTS.md#f087), [E006](OPEN_QUESTIONS.md#e006).

## Five owners, interface contracts and shared integration

All assignments below are `PROP`; map them to actual skills. Merging P1/P3 into one person reduces real parallelism. P3 accepts application integration, P1 platform evidence, P5 scope/claims; mandatory work, recoverable release and deadline outrank optional experiments. [F090](RAW_FACTS.md#f090), [Q028](OPEN_QUESTIONS.md#q028).

| owner | output | recipient_backup |
|---|---|---|
| P1 platform/export/LinQ | Issued contract, minimal adapter, exact model/artifact/config, completion/output/provenance/error, repeatable instruction | P3 consumes; P2 repeats accepted run |
| P2 data/model | Immutable inputs/class labels, dev/holdout distinction, baseline/one candidate, complete train/export bundle | P1 consumes and repeats accepted inference; P5 checks claims |
| P3 video/events/integration | Source -> frame -> event store, IDs/geometry/time/gaps, common accepted release and recovery | P4/P5 consume; P4 repeats smoke/restart |
| P4 interface/presentation | Minimal user action and evidence access, other-machine startup, artifact packaging | P3 repeats UI start; P5 accepts claims; P4 backs up submission |
| P5 task/quality/criteria/submission | Mandatory matrix, questions/answers, separate result review, CP, acceptance and upload | P2 prepares labels/ledger; P4 packages/uploads as backup; captain/agreed owner decides |

P5 must handle CP, disputed-label review, release acceptance and upload **sequentially**, not simultaneously. P2 prepares reference/ledger; P5 gets a separate checking window. P3 produces release; P4 prepares artifacts; P5 accepts outside CP and submits with a second awake checker. If independent review is unavailable, reduce corpus/claim, retain unknowns or use diagnostic status. Tuning by P2 on the same data does not create an independent holdout; rereading one's own result is not independent adjudication. [F079-F081](RAW_FACTS.md#f079).

Our contract is **not an SDK API**. Version only fields needed by the slice. [F091](RAW_FACTS.md#f091).

| boundary | agreed_fields |
|---|---|
| Source -> frame | source/camera ID, reconnect epoch, frame ID, original W/H, PTS/timebase or absence, clock source, permitted original/reference |
| Frame -> inference | request ID/frame reference, model/artifact/preprocess revision, payload and `dtype/layout/color/shape`, resize/letterbox/inverse transform, payload/concurrency limits |
| Inference -> rule | Same IDs, executed revision, status/error, `boxes/classes/confidence` meaning, coordinates, NMS location; empty observation distinct from missing observation |
| Rule -> UI/evaluation | Event ID/revision, actor/track with epoch, rule revision, time/interval/clock, positive/negative/unknown, material reference, actual backend/provenance/availability |
| Model -> accepting owner | Weights/export/hash, class order, pre/post, pinned dependencies, support/result/limits and complete previous rollback bundle |

Fixtures must include positive, empty, error/timeout and late previous-epoch result. Check geometry on the exact frame and a nonstandard size; correct boxes on another frame are wrong linkage. Add tracking when temporal semantics require it; single-frame uncovered cannot stand in for observed removal. A **technical skeleton** crosses real external boundaries; a **useful slice** additionally produces the agreed case outcome on positive/negative/unknown inputs. One permitted camera/file, scenario, LinQ route, event and action starts integration without proving the whole list or multistream requirement. [F088](RAW_FACTS.md#f088), [E002](OPEN_QUESTIONS.md#e002).

`DOC/read` Pryce and Fowler support early external-boundary checking and frequent return to one tested build, not an empirically optimal hackathon routine. `PROP`: sync roughly every **2-3 waking hours** and on access change: working result, exact blocker, next transfer, scope delta. Use only necessary owners during incidents. Merge small changes after a short behavioral check; Git detects textual conflicts, not class-order/ID errors. Coordinate schema/class/preprocess changes with all consumers and update fixtures. Large weights/data need manifest/hash/location and visible revision, not silent overwrites. [F082-F084](RAW_FACTS.md#f082), [F092](RAW_FACTS.md#f092).

Before sleep/handover leave current version/status, next exact project procedure, unfinished job IDs, access limits, known issue, full accepted rollback and authorized restarter. Do not leave the only working path in one person's memory or publish secrets. Clean start, positive/empty/error, exact frame/scale and recovery are useful early smoke checks; they do not establish statistical quality or SLA.

## 45-hour calendar, sleep, freezes and two access scenarios

`INFER/arithmetic`: **5 x 45 = 225 calendar person-hours**. Two **8-hour sleep opportunities per person** remove **80**, leaving **at most 145 before food/meetings/breaks/context switching**. All five at all three 20-minute CPs costs another **5 person-hours**, leaving at most **140 before other work**. These are upper bounds, not productivity/coding budgets. Opening/roast costs actual attendees x duration. Unattended compute may overlap people only under the actual contract; serial compile/load/run/integration and scarce engineers remain bottlenecks. Training/compile/queue/retry/review/upload times are unknown. [F078](RAW_FACTS.md#f078).

`PUB/read`: Van Dongen 2003 abstract (48 adults, 14 nights) and Stepan 2019/2020 abstract (138 participants) associate restricted/deprived sleep with cognitive/procedural deficits and imperfect self-assessment. Full studies were not read; neither tests five programmers over 45 hours or an optimal rotation. [F085-F086](RAW_FACTS.md#f085).

`PROP/example sleep opportunities`: P1/P3 **23 Oct 23:00 -> 24 Oct 07:00**, then **24 Oct 21:00 -> 25 Oct 05:00**. P2/P4/P5 **24 Oct 01:00-09:00**, then **24 Oct 23:00 -> 25 Oct 07:00**. Each gets two uninterrupted eight-hour opportunities; actual sleep can differ. Overlap **01:00-07:00** first night and **23:00-05:00** second has **no required human watch**: valid only if the system can stop or run an agreed safe automatic task. A unique nighttime LinQ slot requires moving owner/backup windows while preserving rest and cutting optional daytime work. Continuous manual queues require a different staffed calendar. Count travel, meals and post-10:00 defence; repeated missed steps trigger transfer to an awake backup and two-person submission. [F093](RAW_FACTS.md#f093).

All internal times below are `PROP`, recalculated from actual probes. They do not prescribe compiler durations or extend deadlines. [F094](RAW_FACTS.md#f094), [E004](OPEN_QUESTIONS.md#e004).

| moment_msk | status | action | guard |
|---|---|---|---|
| 23 Oct 13:00-15:00 | Internal work window | Intake, priority questions, access/semantics/contracts/owners, earliest platform probe | 15:00 fixes route/status/blocker owner/review time, not guaranteed LinQ success |
| 15:00-16:30 | Internal work window | Early available-boundary skeleton; parallel data check | No second framework before understanding first blocker; account for opening |
| Before CP1 18:00 | Official anchor with internal preparation | All five; actual artifacts, slice/access/data questions | Connection check; proposed package is not guaranteed nonzero CP |
| After CP1 to 22:00-23:00 | Internal work window | First domain baseline, full snapshot/rollback, initial event artifacts | No device success -> escalation/supported path, not endless architecture switching |
| Night 23/24 | Internal rest/handover | Written handoffs; approved bounded jobs only | No new dependency known only by a sleeping owner |
| 24 Oct 09:00-10:30 | Internal preparation | Shared build, other-machine start, three CP2 drafts/links | 10:30 is buffer before public 11:00; earlier if individual slot requires |
| CP2 11:00 | Official anchor | Baseline/status and actual draft receipt | New mandatory answer recalculates path; optional suggestion does not automatically redefine task |
| After CP2 to indicative 15:00 | Internal candidate deadline example | One bounded improvement and useful downstream-ready bundle | `D_useful` includes compile/run/quality/integration; local best score alone is insufficient |
| 15:00-17:00 | Internal stabilization | Negative/error cases, supported quality result and limits | Indicative feature freeze 17:00 protects hour before CP3 |
| CP3 18:00 | Official anchor | Delta/final scope/startup/mandatory answers | Thereafter fixes, evidence and presentation; new scope only for mandatory critical defect |
| 19:00-19:45 | Official roast | Clarity/timing review | Do not rebuild product around an optional presentation idea |
| Before 20:30-21:00 | Internal release target | Accepted release candidate, complete rollback, packaging/startup | Major packaging before early group rests; recording only if permitted |
| Night 24/25 | Internal rest/handover | Bounded text/access checks; early group receives status | Do not make mandatory training/compile the only unproven overnight chance |
| 25 Oct 07:00-08:30 | Internal submission target | Clean startup, four links, Яндекс Диск code, presentation, presenter, receipt | First complete submission by 08:30 leaves 1.5-hour internal margin |
| 08:30-10:00 | Internal correction buffer; 10:00 official | Fix upload/link/access defects; freeze exact accepted files/hashes | No features; avoid cosmetic replacement risk |
| After 10:00 | Continuing official obligations | Rest/food, connection, rehearse accepted release, actual defence/awards | No assumed right to modify submitted files; monitor award chat |

Freeze **ideas**, **new model candidates**, **interfaces/full bundle** and **submission** separately. The last useful model start is counted backward through the real remaining path to protected packaging/submission time, with observed-error margin. Unknown duration means unknown feasibility.

**Scenario A, early transparent access — `PROP`, not actual account state.** P1 completes supported sample then an appropriate own run; P2 checks data/baseline; P3/P4 wire agreed fixtures; P5 resolves scope/rights/recipient. By internal 15:00 obtain status; by CP1 success or reproducible blocker. After a complete slice, one useful model/parity cycle is allowed if downstream fits. P2 prepares diagnostic reference; P5 reviews separately. P3 produces release, P1 verifies exact final provenance, P4 packages; P5 attends CP then accepts release, later uploads with another awake checker. No claim that every possible full case or all E checks fit. [F079](RAW_FACTS.md#f079).

**Scenario B, access at 24 Oct 20:00 or opaque access — `PROP/stress scenario`.** **14 calendar hours** remain, or **70 calendar person-hours**. If all five second eight-hour sleep opportunities remain, subtract **40**: **at most 30 person-hours before meals/handoffs/startup/packaging/acceptance**, not 30 free LinQ hours. Sequential stages may still not fit. Before access, retain requirements/rights, native baseline labeled by actual backend, fixtures/UI, CP2 drafts, packaging and exact access blocker. Internal warning is **23 Oct 15:00**, escalation CP1 and again CP2, not disqualification deadlines. [F080-F081](RAW_FACTS.md#f080).

With a known accepted path, P1 prioritizes run -> completion/output/mapping; P2 backs up I/O; P3 integrates one revision; P4 prepares workflow/artifacts; P5 checks claims in a separate slot. Firmware/profiler/wide A/B/multicamera stress are not first-run milestones unless required. Output without revision/mapping remains target-unknown pending a supported witness. Catalog-only requires explicit coverage/admissibility check. Late mandatory requirements recalculate/escalate; they cannot be deleted to call MVP complete. Without access/accepted alternative, submit truthful available work while mandatory LinQ remains unproven; acceptance is not guaranteed.

Cut optional dashboard/editor/connector, extra model and broad comparisons first. Preserve mandatory scope, accepted LinQ route, CP, minimal required materials, rest and receipt. A new model/runtime after snapshot needs new linked execution; old success does not cover new bytes. Unknown remaining duration is not “we will finish by morning.”

## Priority questions to sponsor and organizer

These are **prepared, not sent or answered**. Batch release/I/O/limits questions; record author/role/time/channel/case revision and precise answer. Historical unknowns must not displace current access/submission. [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

| timing_owner | ids | request | decision |
|---|---|---|---|
| First hour, P5/P1 | [Q002](OPEN_QUESTIONS.md#q002) | Full mandatory types/episodes/UI/API/live/multistream/custom model/NN stages; allowed host work; partial coverage | Final scope versus first integration only |
| First hour, P1 | [Q009](OPEN_QUESTIONS.md#q009) | Issued shell/container, sync service, async jobs or catalog; matching working sample; own weights/updates | Platform/model route and adapter |
| First hour, P1/P2 | [Q010](OPEN_QUESTIONS.md#q010) | Exact SDK/compiler/runtime/device/model release, export, `dtype/layout/color/shape`, pre/post/NMS, golden I/O | Compatibility and output decoding |
| First hour, P1/P3 | [Q011](OPEN_QUESTIONS.md#q011) | Quotas/payload/batch/concurrency/queue/slots/status/cancel/timeout/retry/idempotency/persistence/network/background rights | Live/job cadence and full cycle |
| First hour, P5/P1 | [Q008](OPEN_QUESTIONS.md#q008), [Q023](OPEN_QUESTIONS.md#q023) | Accepted concrete-run witness/request-revision-device mapping, live mandate, common outage treatment | Proof milestone, trust boundary and fallback |
| First hour, P2/P5 | [Q012](OPEN_QUESTIONS.md#q012) | Official scorer/revision/format/split/threshold, GT semantics/completeness, camera/session lineage | Optimization and allowed quality endpoint |
| First hour, P2/P5 | [Q007](OPEN_QUESTIONS.md#q007) | Rights/consents for processing/storage/transfer/showing/publication/additional filming | Permitted training/test/demo inputs |
| No later than CP1, P5 | [Q001](OPEN_QUESTIONS.md#q001) | 6/7 criteria, weights/descriptors/aggregation/rounding/tie-break/CP contribution; current form/memo | Verified scoring policy |
| No later than CP1, P5 | [Q006](OPEN_QUESTIONS.md#q006) | Zero CP, mixed miss/zero, shared outage, presence/CP2 acceptance | Admission and required meeting evidence |
| Before disputed resource, P5 | [Q004](OPEN_QUESTIONS.md#q004), [Q024](OPEN_QUESTIONS.md#q024) | Paid development subscription/API, runtime API, training GPU, service compute; templates/weights/vendor debugging/external assistance separately | Permitted development and dependencies |
| Before AI/use/submission, P5 | [Q005](OPEN_QUESTIONS.md#q005) | Case AI prohibition; mixed/edited code, video/slides marking; versions/prompts/links | Disclosure and artifacts |
| Before recording, P4/P5 | [Q003](OPEN_QUESTIONS.md#q003) | Separately create/show/submit/publicly distribute code/frames/logs/screencast; §7.3 | Permitted primary/fallback artifacts |
| CP1, P4/P5 | [Q013](OPEN_QUESTIONS.md#q013) | Recipient/deputy/action authority/channel/local output, miss/false cost, reminders, useful window D | Timely intervention or review |
| CP1/CP2, P1/P3 | [Q014](OPEN_QUESTIONS.md#q014) | Sources/cadence/format/live capture/FPS/latency/clock boundaries | Load and real-time claims |
| CP2, P5 | [Q002](OPEN_QUESTIONS.md#q002), [Q006](OPEN_QUESTIONS.md#q006) | Accepted drafts, remaining mandatory gaps, which new feedback is actually mandatory | Reduced optional scope and recalculated path |
| CP3, P1/P5 | [Q008](OPEN_QUESTIONS.md#q008) | Run X/revision Y/status Z: accepted evidence, short recheck and fallback | Final proof/release |
| On room issuance, P4/P5 | [Q015](OPEN_QUESTIONS.md#q015) | Product/mode/role, screen/file/video/audio, answering participants, presenter replacement/rehearsal | Actual viewer route and authorized backup |
| Before final upload, P4/P5 | [Q016](OPEN_QUESTIONS.md#q016) | Fields/formats/limits/receipt, late changes, Git versus Яндекс Диск | Packaging and formal acceptance |

Team-owned [Q017](OPEN_QUESTIONS.md#q017)/[Q028](OPEN_QUESTIONS.md#q028) require actual stage durations, skills, access, travel/rest and backups. Historical source/winner/video/proof unknowns are [Q018-Q022](OPEN_QUESTIONS.md#q018), operator/statistics/jury [Q030-Q032](OPEN_QUESTIONS.md#q030); IP/licenses/comparison [Q025-Q027](OPEN_QUESTIONS.md#q025). Current award slot is [Q029](OPEN_QUESTIONS.md#q029).

## LinQ proof: minimal accepted witness and honest failure mode

`INFER`: proof has two links: source model/export/config -> loaded/executed revision and allowed placement; exact input/request -> completion of that revision on mapped device -> output. Hash establishes byte identity, not quality, creation time, placement or execution. Correct output can come from CPU; aggregate device utilization can belong to another job. [F065](RAW_FACTS.md#f065).

`PROP/minimum`: agree mandatory NN scope and accepted witness with the sponsor, while trying one safe supported example. Preserve **(1) permitted input ID/hash/version and exact clip/frame/range**, distinguishing source video from preprocessed tensor; **(2) exact own weights/export/program hash or stable server deployment/model/catalog revision**, not just “YOLOv8”; **(3) command/request/job ID, terminal completion and corresponding output/time/context**; **(4) trusted mapping of that run/revision to LinQ or sponsor-accepted witnessed run**, with witness author/role/date and exact input/revision/run scope. If tensor/internal bytes are unavailable, preserve the supplied preprocessing/server revision and state the gap. Local ONNX hash does not equal server revision without mapping. [F060](RAW_FACTS.md#f060), [E001](OPEN_QUESTIONS.md#e001), [Q008](OPEN_QUESTIONS.md#q008).

| mode | save_first | trust_limit |
|---|---|---|
| Shell/container | Input/model/compiled-artifact identity, actual command/config without secrets, status/output, available runtime/device IDs | Match load/run/completion plus supplied device/runtime mapping or accepted witness. Process completion alone is only process completion |
| Synchronous managed service | Input ID/hash, endpoint/deployment revision, request ID, full completed response/output | Server request -> revision -> LinQ mapping or accepted witness. SSH/firmware not intrinsically required for integration; client RTT is not device latency |
| Asynchronous job | Input/model revision, job ID, terminal successful status, output artifact ID/hash/linkage | Execution record or witness for this job. Submitted/running/queued is not success; pending/failed/cancelled remain separate |
| Ready-model catalog | Model key/exact revision, input/request ID, completion/output, available team pre/post revision | Operator contract plus concrete-run mapping or accepted witness; only that catalog path is established, not own weights/full case |

Managed service stable revision/documented contract may be the strongest available evidence; **the 2026 sponsor decides whether to accept that trust boundary**. Missing firmware/compiled bytes need not block integration. Missing **any** trusted mapping leaves target execution unknown. `backend=LinQ` is not evidence. Submit/HTTP ACK/queue admission is not completion; timeout is unknown until supported status lookup, and blind retries may duplicate jobs.

Additional fields **if available**: compiler/runtime/device/firmware versions, compile report, loaded artifact hash, profiler trace, hardware timer and no-fallback semantics. They become contest requirements only if the actual rules say so. “All NN on LinQ” separately defines NN stages and decode/pre/post/NMS/tracking/secondary networks/fallback; one accepted run is not hardware attestation of every application node. [F063-F066](RAW_FACTS.md#f063), [Q010-Q011](OPEN_QUESTIONS.md#q010).

`DOC/read`: MLPerf scenarios/timing and LoadGen responsibilities do not certify our device/weights/correctness; even `VALID` performance logs are insufficient. ORT provider registration versus node coverage illustrates the principle only: **no LinQ EP or LinQ fallback was established**. Historical profiler/Python fields are not current commands. IVATech 2020 result is **Xilinx Alveo U200**, old compiler/runtime, not ASIC LinQ-2026; its **60000 ms** minimum is not a current test norm. [F061-F067](RAW_FACTS.md#f061).

Immediately snapshot a successful run by permitted means. A model/runtime change requires new linked execution. Preserve the whole matching release, not weights alone. Ordinary text logging does not authorize secrets/confidential fields or public distribution; §7.3 applies separately to recording/publication. At access failure keep last genuine success/date/revision and current broken link. Permitted alternatives may be restored live run, authorized past proven run, or separately labeled local comparison; the latter two are not LinQ running now. Without any successful run or accepted alternative, mandatory inference remains unproven. CPU/RTX/mock/cache/catalog labels and negative compatibility reports do not fill that gap. [E006](OPEN_QUESTIONS.md#e006), [E008](OPEN_QUESTIONS.md#e008), [F080](RAW_FACTS.md#f080), [F102-F103](RAW_FACTS.md#f102).

## Quality claims: reference sufficiency, denominators, unknown and close

`PROP`: first ask “quality of what?” Object, wearer relation, observable violation, episode, delivery and human action are separate. Missing observation is not a normal frame; timeout/camera outage/empty detection must differ. Freeze input/model/config/evaluator before calculation. Record goal/unit, data origin/support, independence or diagnostic status, success/threshold, numerator, denominator, unknowns, errors and applicability. Neighboring frames of one video do not create an unseen-camera test. **Expected inputs = successes + errors/drops + unfinished**, with retries linked. Zero denominator -> **NA**. Missing required official scorer is an unresolved mandatory gap, not license to substitute a convenient metric. [F076-F077](RAW_FACTS.md#f076), [F110](RAW_FACTS.md#f110), [E003](OPEN_QUESTIONS.md#e003).

No team GT/logs/quality measurements exist. The following `PROP` matrix defines future admissibility, not results.

| inputs | allowed | forbidden | next_input |
|---|---|---|---|
| Official evaluator with exact version/format/split/output | Named official score, counts/support/failures/scope | Supplemental score as official; tuned-on test as independent | Issued scorer/example; otherwise official number unavailable |
| Complete known-domain frame boxes/classes GT | Object metric under frozen procedure/classes/GT; diagnostic if dev | Wearing/ownership/temporal-event quality or event recall from object AP | Person/PPE relation, visibility and rule labels |
| Small fixed diagnostic set with explicit expectations | Passed/failed/unknown counts and errors | Unbiased new-camera accuracy or natural production error rate | Independent lineage/group-heldout sample and reference |
| Complete delivered-claim census for fixed source **I**, **H source camera-hours**, sufficient review context | Semantic false delivered records **F/H** at close **C**, true/false/unknown counts; descriptive **[F/H, (F+U)/H]** if truth labels independently fixed | Recall, H “normal hours”, false-active duration, outage-induced low rate as recognition improvement | Independent search of all GT episodes for recall; reference of negative support for normal-hours claims |
| Selected alert-review subset only | Correctness of reviewed records with selection stated; a specifically defined probability-sampling estimate if designed | Recall or extrapolation of subset precision without sampling design | Full census or sampling frame/probabilities/protocol |
| Complete independent event GT and completion/delivery ledger, frozen match/deadline/boundaries | Event TP/FP/FN/U and recall in the defined onset-owned cohort; empty denominator NA | Removing outage misses; F1 combining precision/recall from different boundary cohorts with invented common TP | Adjacent context, competing alerts, follow-up to deadline; narrow/unresolved claim until matching closes |
| No GT, complete destination log in wall interval **J** | Visible records per wall-hour, types/pending: channel workload | False-alert rate, accuracy, recall, safety | Truth/context for a named quality claim; raw workload itself needs no GT |
| Two-three positive/empty/error smoke inputs | Named wiring cases and observed errors, mock labeled | Statistical quality, industrial reliability, p95 or generalization | Reference for desired endpoint; smoke count is no universal sample size |
| One overlay frame/clip | Illustration with mode/revision | Measured quality, live target execution without run, removal from one frame | Original/labels/execution references |
| Completed requests under one monotonic clock with all outcomes | Host duration/completed client RTT, N/raw samples, separate errors/timeouts/unfinished | Device-only latency, useful response time, all NN on LinQ, industrial camera sizing | Documented timer/placement; GT onset/clock map/delivery for response |
| Recorded replay with PTS/schedule | Replay lag/source exposure with speed/pauses | Physical capture-to-recipient latency or live real-time | Live capture semantics, clocks and tested load |

For the all-alert census, **I** fixes source material, **H** is its source camera-hours, **F** false delivered records, **U** unresolved truth outcomes and **C** review close. Independently fixed reference judgments permit the descriptive bounds; they are not a confidence interval. Reviewing every delivered alert can support this narrow semantic burden **without labeling all silence**. Recall still needs independent missed-event search. Unreviewed non-alert periods are not automatically normal. Source camera-hours differ from operator/channel wall-hours; low F/H during outage cannot show improved recognition without coverage/errors/unfinished alongside it. [F076](RAW_FACTS.md#f076).

Label semantic correctness, timeliness, intentional reminders and excess/duplicate records separately. A late true alert remains semantically true; a true extra record still adds burden. State close C, remaining U and unresolved matching. Intenseye `accuracyRate` is not a recovered formula or evidence of recall. [F071](RAW_FACTS.md#f071).

Minimal package: one permitted input/model/config manifest, linked completed run/output/accepted target proof, one supported result table with counts/denominator/NA, source reference, one failure/unknown and explicit limit. P2 supplies GT type/completeness/lineage; P3 completion/delivery logs; P1 exact revision/mapping. **Stop unsupported percentage calculation** if needed input will not arrive before protected packaging; use diagnostic counts/NA and name the next input. Missing mandatory official metric remains unfinished. [F077](RAW_FACTS.md#f077).

### Speed: four boundaries and vendor limits

Device inference interval needs a documented device timer; completed service **RTT** uses one client monotonic clock; end-to-end **frame -> durable event/visible UI** needs named endpoints and compatible clocks; throughput counts completed real samples per wall duration. Distinguish model-only from decode/pre/post/tracking/transport and real batch samples from padding. **`1/FPS` is not latency** under batching/pipelines/concurrency; **RTT minus ping is not device time**, because transfer/queue/serialization/server processing differ. Sent/ACKed requests are not completed work. [F061-F062](RAW_FACTS.md#f061), [F109](RAW_FACTS.md#f109).

Attach model/precision, source/resolution, device/runtime versions, batch/inflight/concurrency/streams/offered cadence, warmup rule/cold start, duration/N/raw samples, p50/p95 with n where justified, drops/errors/outstanding and queue effects. One probe does not estimate a tail. Replay needs PTS/speed/pauses; accelerated playback is not live capture. A shared-service queue is not entirely chip latency. Successful-only timing must retain coverage/failure counts. [E009](OPEN_QUESTIONS.md#e009).

`CLAIM/read`, text-only [LinQ 2026 PDF](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf): Core i7-10700K @3.80GHz, Ubuntu 24.04, TPU Runtime **16.18.6**, TPU Framework **2026.8.43**, separate throughput/latency columns and MLCommons MLPerf claim. No visual original or reproduced team benchmark. Its FPS does not establish our camera count, compile duration or useful alert deadline. Exclude it from capacity promises pending issued-path/load tests. [F055](RAW_FACTS.md#f055), [Q014](OPEN_QUESTIONS.md#q014), [Q022](OPEN_QUESTIONS.md#q022).

## Defence: actual viewer path, 300 seconds and honest fallback

`RULE/read`: **10 minutes = 2 technical + 5 presentation + 3 questions**. PDF calls the first two connection/preparation, FAQ connection/disconnection. LK supplies room link; case startup file supplies structure. Prepared video is allowed as presentation mode, subject to unresolved recording/rights §7.3. **2026 room/product/mode/role is unknown**: current MTS partner link and 2025 partnership do not identify Встречи/Вебинары, screen/file/audio privileges or backup-presenter permission. Internal backup assignment is not organizer approval. [F007](RAW_FACTS.md#f007), [F097](RAW_FACTS.md#f097), [Q015](OPEN_QUESTIONS.md#q015).

`PROP`: choose live/recorded/hybrid only after format clarification and full viewer rehearsal. Live shows current reaction but depends on access/network/warmup/role. An authorized recording of a real run shows **that past run**, with date/revision/log linkage and data rights, not current operation. Hybrid must serve distinct evidence needs without duplicate results/switching waste. Static permitted evidence is past state and does not replace mandatory functioning demo. Required live remains required despite a recording; recording prohibition requires an accessible prototype/other agreed backup. Never make an unapproved screencast the only fallback or show cache/mock as new LinQ inference. [F102](RAW_FACTS.md#f102).

Conditional MTS documentation is mode-specific: web audio sharing uses a **Chrome tab**, screen and presentation cannot be simultaneous, screen detail adapts to network. SaaS transport/browser/proxy requirements differ from ПО/on-premise guidance listing **MP4, H.264 Baseline, AAC** and unsupported embedded presentation multimedia. Do not turn another mode's codecs/bitrates into hackathon-room requirements or a 10 Мб rule. File extension/upload success is not playback. [F098-F100](RAW_FACTS.md#f098).

After room issuance, test usual connection/name/mic/screen, presentation -> prototype/permitted video -> presentation, readable evidence/sound and one failure, with an **independent remote viewer** on the intended client/network/role. Keep laptop backup ready, one active audio source/headset, no nearby duplicate sound. Before disabling VPN check LinQ dependency; a conference fix may sever mandatory hardware access. Separating accelerator access and presentation across approved devices/networks is a conditional route to test. Network bandwidth alone does not fix blocked transport/permissions. [F099-F101](RAW_FACTS.md#f099), [E007](OPEN_QUESTIONS.md#e007).

`PROP` failure responses: missing screen rights -> request during technical window/authorized presenter route; no video sound -> voice/captions only if sufficient, state missing evidence if sound matters; playback/conversion failure -> tested separate file/permitted static evidence; LinQ overrun/outage -> permitted last proven run with date/revision/current fault; speaker loss -> approved backup; unreadable log -> enlarge unchanged essential values and retain full artifact; app failure -> prior stable release with truthful current/past distinction. Rehearsal recovery budget **5-10 seconds** is our adaptable threshold, not an official extension or exemption from live requirements. [F103](RAW_FACTS.md#f103).

One observable input -> decision -> useful action is the demonstration core, with source/time/status/evidence/failure visible. A successful clip needs a supported evaluation result or explicit “not statistically evaluated.” One evidence unit is a claim, its concrete basis and its material limit. Prepare a separate seven-criterion coverage matrix, not seven equal speaking portions. [F104-F105](RAW_FACTS.md#f104).

The following **our 300-second example** is an explanation budget, not ready speech/slides or jury formula; full-case template can change it.

| function | seconds | evidence |
|---|---:|---|
| User/site/main problem boundary | 20 | Whose central outcome is addressed |
| Observable operation/useful result | 90 | Prototype, main problem, UX and any functioning secondary result |
| Quality/LinQ/speed/limits | 55 | Version-linked execution and supported numbers |
| Approach difference/additional value | 35 | Specific contribution/comparator difference |
| Analytical basis of scope | 30 | Audience/problems/analogs that changed the decision |
| Deployment/economics | 30 | Confirmed inputs/cost components and unknowns |
| Completed result/next check | 20 | What is finished and testable next |
| Transitions/reserve | 20 | Actual switching margin |

Total **300 s**. If recording is permitted, a **45-60 s** actual-run clip may fit inside the 90-second result segment; mandatory live can occupy it instead. Video share itself is not a criterion. Use one readable analytical fact rather than rapidly reading a dense table; cost components rather than invented payback. Our rehearsal target **4:40-4:45** leaves margin within official five minutes. Ralston's investor-demo advice supports early product/user explanation, readable slides, practice and one lead; his “no demo”/record-rehearsal advice does not override mandatory demo/§7.3. [F104-F105](RAW_FACTS.md#f104), [E007](OPEN_QUESTIONS.md#e007).

Teaser/presentation/demo/code must describe the same version and status: shown, measured, partial, planned. No reliably attributed winner teaser was obtained; do not invent one. Submission materials must be created during the event.

## 180-second Q&A: provenance and answer ownership

**Observed Q&A = 0.** QA001/QA002 are **reported**, both from the **same** Black Duck participant article about РЖД-2024 (five-minute talk plus five-minute questions, local offline recordings), not Mosprom footage. QA003-QA014 are **anticipated**, derived by us from criteria/announcement/risks. No frequency or current-judge preference is established. НКБТех **01:08:00** remains an unviewed linked timestamp. [F041](RAW_FACTS.md#f041), [F058](RAW_FACTS.md#f058), [F106](RAW_FACTS.md#f106), [QA bank](OPEN_QUESTIONS.md#qa001).

| id | status | topic | evidence_owner |
|---|---|---|---|
| [QA001](OPEN_QUESTIONS.md#qa001) | reported | Which violations are recognized? | Same РЖД article; mandatory -> implemented -> verified types, P2/P5 |
| [QA002](OPEN_QUESTIONS.md#qa002) | reported | How many videos per run? | Same article; actual file/batch mode, not real-time camera count, P3 |
| [QA003](OPEN_QUESTIONS.md#qa003) | anticipated | What runs on LinQ and how can it be checked? | Exact input/revision/completion/output/mapping and NN scope, P1 |
| [QA004](OPEN_QUESTIONS.md#qa004) | anticipated | Live, recording, cache or mock? | Mode/date/status/reproduction path, P3/lead |
| [QA005](OPEN_QUESTIONS.md#qa005) | anticipated | False alarms/misses on which data? | Split/lineage/support/unit/reference sufficiency, P2/P5 |
| [QA006](OPEN_QUESTIONS.md#qa006) | anticipated | Night/occlusion/bad camera? | Checked slices or explicit untested status, P2 |
| [QA007](OPEN_QUESTIONS.md#qa007) | anticipated | Streams and latency? | Exact config/cadence/completions/drops/timing boundaries, P3/P1 |
| [QA008](OPEN_QUESTIONS.md#qa008) | anticipated | Human review and error correction? | Actual process/history/unknown/authority, P4/P5 |
| [QA009](OPEN_QUESTIONS.md#qa009) | anticipated | Difference from baseline/products? | Narrow sourced comparison and own contribution, P5/P2 |
| [QA010](OPEN_QUESTIONS.md#qa010) | anticipated | Pilot cost/deployment inputs? | Confirmed components/unknowns, no invented prices, P5/P3 |
| [QA011](OPEN_QUESTIONS.md#qa011) | anticipated | Video/person/dependency rights? | Exact origin/licenses/permissions/showing scope, P5/P2 |
| [QA012](OPEN_QUESTIONS.md#qa012) | anticipated | Created here and AI use? | History/third-party components/marking/disclosure/contribution, P5 |
| [QA013](OPEN_QUESTIONS.md#qa013) | anticipated | Camera/network/LinQ failure? | Tested failure/pending/unknown/recovery/last genuine proof, P3/P1 |
| [QA014](OPEN_QUESTIONS.md#qa014) | anticipated | What is unfinished and next? | Specific limit/minimal input/next check, relevant owner |

`PROP`: jury speech consumes part of **180 s**, so question count is unknown. Rehearse **15-25 s** answers as a target, not an official limit: **direct answer -> one concrete basis with conditions -> material limit**. Clarify whether the question concerns current prototype, measurement or future pilot if needed. If unmeasured, state what is unknown, existing fact and smallest next test; do not guess FPS/zero false alarms/LinQ cost/pilot date. One lead routes to one owner, no habitual multi-person additions. Backup may locate artifacts if team connection is permitted. Open details only for the actual question/time. Name observed failure and last success without blaming organizer absent evidence. [F107](RAW_FACTS.md#f107).

## Compliance: originality, AI, paid resources, recording, licenses and IP

### Originality and assistance

`RULE/read` §§4.1.2,5.3-5.4,10.2.8 requires a prototype created during participation and prohibits preprepared code, code parts and other materials; plagiarism/copying/early templates can cause disqualification. Git history supports origin but is not a required platform/13:00 first-commit rule or immunity; commit time does not prove content creation time. Earlier own educational code gets no automatic exemption through disclosure. Research/knowledge/procedures are preparation; ready code/slides/teaser/demo are not authorized pre-event deliverables. Free public libraries/templates/software may be a foundation/supplement, with rights and origin; pretraining/generators/framework starters require precise boundary clarification. [F014-F015](RAW_FACTS.md#f014), [Q024](OPEN_QUESTIONS.md#q024).

Expert/tracker consultation is provided, while §§7.3/10.2.4 broadly prohibit hints/other assistance without exhaustive definition. Do not create an exception for outside colleagues, forums, hired developers or vendor-written code. SDK/sample delivery, consultation and direct coding are distinct questions. No messages were sent externally in this research. [F020](RAW_FACTS.md#f020).

### AI permission, paid tools and disclosure

`RULE/read`: AI is conditionally allowed **unless the case prohibits it**; a case prohibition can cover all stages including code/design/text/images/analytics. With permission, require substantial team intellectual/technical contribution to architecture/logic/functionality; mark **all AI-generated content**, disclose tools in solution description/presentation, include own integration code in repository, link third-party open AI tools/embedded features. Organizer confidential data must not go to public AI services. [F016](RAW_FACTS.md#f016), [Q005](OPEN_QUESTIONS.md#q005).

`UNK`: §4.1.6 permits public **free** foundations, but §3.6 own expenses does not grant paid-tool exceptions. Neither “budget permits everything” nor “every paid tool is prohibited” follows. Obtain separate answers for already-paid development AI subscription, development API, API in prototype, training/debug GPU and paid service runtime/compute. Development-editor permission does not authorize runtime dependency. [F015](RAW_FACTS.md#f015), [Q004](OPEN_QUESTIONS.md#q004).

`PROP`: track artifact/fragment -> tool/version/date -> purpose -> human contribution/rework; visible appropriate labels in generated files/blocks/visuals and a description/presentation summary. This is **not an approved sufficient template**. Mixed-file granularity, edited AI code, required prompts/versions/links and human-edit exceptions remain unknown. A general README cannot be assumed sufficient for all source/slides/video. Confirm a concrete approach with the organizer. [F016](RAW_FACTS.md#f016).

### §7.3: separate create, show, submit and public distribution

`RULE/read/conflict`: §7.3 broadly prohibits independent photo/video recording of task materials **and/or results** during participation and publication of task/results; it is not limited to filming a factory. Other provisions allow video demo and require accessible final links. No general exception for screencast/LinQ recording/public repository/video hosting was obtained. Do not infer universal permission from FAQ or prohibit all required submission by our own interpretation. Agree a concrete object/action/audience package. Access-by-link does not resolve the conflict. [F017](RAW_FACTS.md#f017), [Q003](OPEN_QUESTIONS.md#q003).

For **code**, creation during event and judge review are required; accessible submission and broader public distribution need reconciliation with §7.3 and data/dependency rights. For **screen/video**, prepared-video presentation mode is permitted, but creating the recording, submitting its link and public dissemination need separate scope/rights clarification. For **frames**, creation/storage/processing/jury showing/submission/publication each requires dataset/person rights. For **text logs**, no blanket ordinary-save ban was found, but confidential fields/secrets/person data, judge showing, submission and public dissemination remain separate questions. CP/defence/other-participant recording has no established permission. Preserve a permitted accessible prototype and allowed evidence while clarification is pending.

`RULE/read`: §4.1.4 requires consent for images of individuals under the established procedure. Dataset license/public URL does not automatically establish every person's consent or every permitted action. Site privacy concerns organizer processing of website users; winner payment consents concern organizer/payment relations. Neither authorizes team publication of industrial-worker frames. Face blur/eye masking is not universally sufficient by assumption. Obtain scope, audiences, retention and transmission rights from the sponsor/rightsholder. [F018](RAW_FACTS.md#f018), [Q007](OPEN_QUESTIONS.md#q007).

### Licenses and result rights

`PROP`: inventory exact source/revision/LICENSE/terms, permitted actions, distribution/commercial restrictions and attributions for each package/model/weight/video/labels. **Code, weights and data separately.** Free does not mean obligation-free. The AGPL-3.0 example §13 concerns offering corresponding source to network users of a modified version under the stated interaction; whether an integrated work is derivative/combined depends on the integration. It does not prove every independent product using any AGPL library must open everything. Ultralytics' trained-model/derivative-project interpretation is that rightsholder's position; not every YOLO has one license. Paid Enterprise also needs contest paid-resource approval. [F021](RAW_FACTS.md#f021), [Q026](OPEN_QUESTIONS.md#q026).

`RULE/read`: PDF §5 retains participant exclusive rights in created results; no assignment to sponsor was found there. FAQ separately adds organizer informational/advertising use and modification/shortening/addition without remuneration. Do not silently attribute the FAQ addition to PDF, call participation automatic IP assignment or promise no other use rights. Obtain exact applicable permission for commercial decisions. [F019](RAW_FACTS.md#f019), [Q025](OPEN_QUESTIONS.md#q025).

### Formal route, sanctions and prize paperwork

`PROP`: start with admission/current rules/case/permissions; before CP check slot/presence/actual acceptance, including three CP2 drafts; at freeze accept whole bundle/rights/licenses/AI/claims and clean startup/rollback with an awake second participant; internal **08:30** checks four anonymous links/code download/presentation size+attachment/presenter/receipt; by official **10:00** fix access/upload defects and freeze release. Afterwards preserve links, attend defence and team awards, monitor chat and maintain **90 working days** availability.

`RULE/read`: disqualification grounds include ineligible/false data, prohibited assistance, jury influence, presence breaches, plagiarism/prepared material, absent defence representative, insults/ethics and other rule breaches. These are **grounds**, not verified historical punishment cases. Jury professional scores/winner decisions are final without appeal; the separate negotiation/written-claim procedure with **15 working days** does not create score appeal. [F022](RAW_FACTS.md#f022).

`RULE/read`: team prizes **250/150/100 thousand RUB with НДФЛ**, distributed equally. Copies/forms by **30 October**, verification by **6 November**, original-document request by **13 November**, originals sent by **20 November**. Payment within **30 working days from publication of results**, not before required documents; false/missing documents can forfeit payment. Template **13%** does not establish individual actual tax treatment. Payment rules do not resolve scoring or create an award-absence sanction. [F023](RAW_FACTS.md#f023).

## Risks to catch during ordinary work

`PROP`: catch unsupported weights/21 maximum before prioritization; binary-only answers before type claims; “all components ready” without common startup before CP2; late better weights without export/compile/run/integration before acceptance; backend labels without target mapping before LinQ claims; successful-only denominators before metrics; alert review masquerading as recall; low alarms during outage masquerading as better quality; universal operator/novelty claims before product explanation; unapproved recording-only fallback; 09:55 packaging; simultaneous P5 CP/review/upload; sleep sacrificed to every delay; multiple owners extending every Q&A answer; team dispersal before awards. Each has a concrete check in the relevant section and E procedure. Author stories do not prove any one error necessarily loses a prize. [F009](RAW_FACTS.md#f009), [F028](RAW_FACTS.md#f028), [F040](RAW_FACTS.md#f040), [F049-F053](RAW_FACTS.md#f049), [F072-F081](RAW_FACTS.md#f072), [F087-F094](RAW_FACTS.md#f087), [F103](RAW_FACTS.md#f103), [F107](RAW_FACTS.md#f107).

## Proposed checks E001-E010: inputs, evidence and limits

All records are **proposed, not performed**. This is not an instruction to prebuild submission code or run a large benchmark; not all ten must fit in 45 hours. Begin with a short linked **E001 + E002 + E003** package; E004 turns observed durations into calendar decisions; E006/E007 protect release/submission/viewer. Other checks depend on mandatory scope/access. [F077](RAW_FACTS.md#f077).

| id | status | question | inputs_actions | evidence_limit |
|---|---|---|---|---|
| [E001](OPEN_QUESTIONS.md#e001) | proposed | Is there a completed accepted target path? | Issued access/matching sample/docs, permitted input, exact model/deployment revision; complete and obtain mapping/witness | Manifest/ledger input/revision/request/completion/output/mapping. Catalog only proves catalog; no mapping -> target unknown; one run is not quality |
| [E002](OPEN_QUESTIONS.md#e002) | proposed | Are component boundaries and failures correct? | Positive/empty/error/late-old-epoch fixtures; exact frame/pre/post/IDs/geometry/timebase/recovery; label mocks | Expected/observed/raw output/pass/fail/U. Wiring success is not accuracy/SLA |
| [E003](OPEN_QUESTIONS.md#e003) | proposed | Which quality endpoint is supported? | GT/log inventory, origin/split/evaluator/unit/match/deadline/unknown/close; freeze revisions, count all outcomes | Numerator/denominator/support/U/NA and failure case. Insufficient reference -> narrow or stop percentage; official gap remains |
| [E004](OPEN_QUESTIONS.md#e004) | proposed | Does the entire useful path fit? | Small candidate/actual slots; time access/compile/queue/load/run/restart/startup/package/upload and active human work; check P5 conflicts | Duration ledger/revised D_useful/last start/escalation. One probe is not p95 or whole-case training duration; 225/145/30 only conditional upper bounds |
| [E005](OPEN_QUESTIONS.md#e005) | proposed | Is an actual user outcome shown? | Approved rule/process/rights/test receiver or output/clocks/policy/D; delivery/receipt/action or review/history plus one unclear/failure case | IDs/times/status/history. HTTP ACK != human; laptop sound != shop floor; review != prevention; no dangerous staged event |
| [E006](OPEN_QUESTIONS.md#e006) | proposed | Can another person run the accepted release and verify receipt? | Complete bundle/instruction/rights/AI/LK; P3 produces, P5 accepts separately, P4 backup; awake second checker does clean start/positive/empty/error/full rollback/four links/Яндекс Диск/presentation/presenter/receipt; CP2 analogue | Release ID/hashes/issues/receipt/storage owner. Does not authorize publication/late change or guarantee nonzero CP; 08:30 internal, 10:00 official |
| [E007](OPEN_QUESTIONS.md#e007) | proposed | Can remote viewer see proof within 2+5+3? | Actual room/product/role, permitted artifacts/backup, independent viewer; connection/transitions/legibility/audio, one fault, separate 180 s Q&A | Client/network/role/time/defects/fallback. One rehearsal does not guarantee jury network; recording only if permitted; awards monitored separately |
| [E008](OPEN_QUESTIONS.md#e008) | proposed | Does access failure preserve truthful proof/status? | Accepted bundle/run, permitted store/status/retry; immediate snapshot, new run after model/runtime change, lookup timeouts, recover without blind retries | Last verified revision/time, failure/queued/unfinished IDs. Restored live or agreed dated past run/local comparison; backup cannot create a missing past LinQ run |
| [E009](OPEN_QUESTIONS.md#e009) | proposed | Do available model stages agree, and what is timed? | Exact native/export/target revisions, same inputs/pre/post/tolerance; compare available raw/detection/event outputs; completed RTT/raw N/all outcomes, replay PTS/speed | Versioned parity/timing report. Device timer for device claim; GT onset/clock map/receipt for timely claim; no `1/FPS` or RTT-ping; small run not p95 |
| [E010](OPEN_QUESTIONS.md#e010) | proposed | Which missing source link can an exact artifact close? | Working original/issued file and rights; PDF bytes/hash/visual pages, Russian FAQ captures, winner identity/revision, actual video range/context/Q&A | Original/locator/comparison or precise access limit. URL/summary/01:08:00 is not viewing; unrelated event_doc is not 580121 rules; no hidden third research wave |

If target execution fails, seek the supported path/witness; if it runs but semantics fail, localize object/relation/rule/delivery; missing rights require the rightsholder. After mandatory-chain acceptance, only a bounded improvement with the whole downstream path is admitted. Preserve time for clean release and viewer check.

## Addressed handoffs to neighboring research

These are prepared local transfers, **not external messages**. All rows refer to the **23 October 2026** assembly; same F numbers across topics differ. Neighbor policies are not measurements, and vendor originals reused by several reports remain one provenance chain. Full detail: [collector handoff](_WORK/COLLECTOR_HANDOFF.md).

| topic | decision | evidence_open |
|---|---|---|
| `linq_platform` | Minimal completed input/revision/completion/output plus trusted mapping/accepted witness; managed integration may continue without firmware/internal compiled bytes | [hackathon_strategy:F060-F067](RAW_FACTS.md#f060), [E001](OPEN_QUESTIONS.md#e001), [Q008-Q011](OPEN_QUESTIONS.md#q008), [Q023](OPEN_QUESTIONS.md#q023). `linq_platform:F287-F294`, S026/S063/S075 are historical/analysis, not current run; [base](../research_link_platform/RAW_FACTS.md) |
| `evaluation` | Separate object/person/event/delivery/timeliness; one reference-supported endpoint with counts/support/U/close/NA; all-alert burden need not label all silence | [hackathon_strategy:F071](RAW_FACTS.md#f071), [F076-F077](RAW_FACTS.md#f076), [E003](OPEN_QUESTIONS.md#e003); `evaluation:F224/F229/F230/F234`; [base](../evaluation/RAW_FACTS.md). Team GT/logs absent |
| `operator_product` | Separate warning/review/delivery/action; local warning can precede browser review; no-duty backlog conditional on full case | [hackathon_strategy:F068-F075](RAW_FACTS.md#f068), [Q013](OPEN_QUESTIONS.md#q013), [Q027](OPEN_QUESTIONS.md#q027); `operator_product:F105-F108/F136-F143`; [base](../operator_product/RAW_FACTS.md). HTTP ACK not human; F136 not measured labor |
| `market_deployment` | No general first-PPE-on-LinQ claim; Cable Justice refinement/product without measured effect; cost components instead of ROI | [hackathon_strategy:F033](RAW_FACTS.md#f033), [F072-F075](RAW_FACTS.md#f072); S061/S062 are same originals as `market_deployment:S210/S211`, F171-F173; [base](../market_deployment/RAW_FACTS.md) |
| `video_architecture` | Source/frame/request/revision ledger from first slice; pending/error/unknown/late-old-epoch states; jobs/manual not live; conference and LinQ/VPN together | [hackathon_strategy:F060](RAW_FACTS.md#f060), [F076](RAW_FACTS.md#f076), [F091](RAW_FACTS.md#f091), [F097-F103](RAW_FACTS.md#f097); `video_architecture:F204-F208/F215`, Q001-Q005; [base](../video_architecture/RAW_FACTS.md). Proposed team contract, not SDK API |
| `model_stack`, `training_strategy` | Immutable whole bundle and D_useful including downstream; new model after snapshot needs new proof; FPS not compile/export duration | [hackathon_strategy:F015](RAW_FACTS.md#f015), [F021](RAW_FACTS.md#f021), [F080](RAW_FACTS.md#f080), [F087](RAW_FACTS.md#f087), [F092-F094](RAW_FACTS.md#f092); `training_strategy:F282-F284`; [training base](../training_strategy/RAW_FACTS.md). Proposed policy; paid compute unknown; unavailable model_stack content not invented |
| `datasets`, `violation_methods` | First 20-minute origin/rights/GT intake; absent PPE versus observed removal versus hazardous context; training cannot create absent signal | [hackathon_strategy:F018](RAW_FACTS.md#f018), [F049](RAW_FACTS.md#f049), [F076](RAW_FACTS.md#f076), [F095-F096](RAW_FACTS.md#f095); `datasets:F070/F071/F102`, `violation_methods:F102/F103/F117/F123`; [data](../datasets/RAW_FACTS.md), [methods](../violation_methods/RAW_FACTS.md). Method boundaries, not empirical quality |

Next operational result is a small linked package another participant can open and repeat: current form/mandatory matrix, issued execution route/accepted witness, permitted input, one supported endpoint, named owners and last useful candidate deadline. Expansion remains conditional on mandatory materials, rest, acceptance, defence and awards time.
