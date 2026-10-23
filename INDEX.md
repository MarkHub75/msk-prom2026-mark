# MOSPROM 2026 — AI knowledge index

This repository supports a five-person team building industrial-safety video analytics for «Открой#Моспром» 2026. Neural inference must run on LinQ; CPU/RTX preparation does not satisfy that requirement. Public examples include missing helmets, removed respirators, dangerous-zone entry and smoking near flammables. They are **examples, not the complete technical case**. The saved schedule gives 23 October 13:00 → 25 October 10:00 MSK (45 hours).

**Inventory:** ten topic directories under [Deep-Research](Deep-Research/), nine complete human/machine report pairs, and one **incomplete `model_stack`** investigation. No full organizer case or demonstrated own-model LinQ execution was found in the saved research. The reports mostly describe a morning-of-23-October preparation snapshot; compilation timestamps do not establish refreshed sources or current access.

## Read only what the task needs

Use the routing table below → open the indicated machine report and named section → follow the necessary neighboring topic. Use the Russian human report for explanation, `RAW_FACTS.md` for the exact claim and verification boundary, `SOURCES.md` for provenance/version/saved artifact, and `CRITIC.md` plus `OPEN_QUESTIONS.md` for corrections and remaining gates. These four support files sit beside each complete report pair. For `model_stack`, start with its critic and branch-local evidence instead.

Research recommendations are not proof of an implemented product. Do not read all reports by default, execute copied commands blindly, or treat a proposed experiment as a completed test.

## Research directory

Topic IDs below are logical names; actual folder names and the nested model investigation are preserved.

| Topic | What it actually helps decide | Entry points |
|---|---|---|
| `linq_platform` | Exact SDK/release and hardware boundaries; import → PTQ → compile → runtime; detector/output compatibility; access-dependent routes R001–R008. Public source and CPU probes exist; target execution does not. | [Machine][linq] · [Human][linq-human] |
| `model_stack` **incomplete** | Candidate repositories/weights, taxonomy, CPU ONNX export and pre/post parity. Sixteen WAVE1 branches, critic and six partial WAVE2 documents; no consolidated reports, SOURCES, RAW_FACTS or OPEN_QUESTIONS. Scratch-only artifacts may be unavailable. | [Read critic first][models] → [PPE weights][ppe-weights] / [base-weight catalog][base-weights] / [export][model-export] / [pre/post][model-parity] |
| `violation_methods` | Observable person–body-part–item relations; true/false/unknown predicates; floor geometry, tracking, source-time episodes, respirator state versus removal and smoking evidence. Does not select final weights. | [Machine][methods] · [Human][methods-human] |
| `datasets` | Exact acquired artifacts, annotation units/coverage, competing splits, lineage, scale and action-specific rights. Includes bounded archive/image/video audits, not target model accuracy. | [Machine][data] · [Human][data-human] |
| `training_strategy` | Whether adaptation addresses the actual bottleneck; few-label selection, teacher assistance, partial labels, KD/PTQ/QAT/pruning, checkpoint handoff and deadline gates. All 51 proposed experiments remain unexecuted. | [Machine][training] · [Human][training-human] |
| `evaluation` | Object → person-state → episode → delivered-alert quality; GT, leakage, frozen policy, uncertainty, clocks, failures and target parity. Tiny synthetic/source/math fixtures ran; no detector/video/device benchmark. | [Machine][eval] · [Human][eval-human] |
| `video_architecture` | Conditional API/shell/job placement; RTSP freshness, bounded scheduling, remote obligations, frame identity, event/outbox persistence, evidence and same-frame display. Stack and 50/500-camera arithmetic are proposals, not measured capacity. | [Machine][video] · [Human][video-human] |
| `operator_product` | Recipient roles, review/action workflows, evidence cards, independent states, camera/rule onboarding and a 17-group product–architecture contract. Documentary patterns; no user study or implemented UI. | [Machine][product] · [Human][product-human] |
| `market_deployment` | Competitor/price units, deployment evidence, conditional TCO/NPV, data-flow/legal questions, LinQ supply and separate pilot/grant/purchase routes. Executed economic arithmetic is not measured customer ROI. | [Machine][market] · [Human][market-human] |
| `hackathon_strategy` | Saved official obligations versus proposed scope; five owners, integration/deadline gates, submission and defense evidence. Preserves PDF/FAQ disagreements rather than inventing scoring weights. | [Machine][strategy] · [Human][strategy-human] |

## Route by question or task

Quoted phrases identify sections inside the linked report. Follow only the additional sources needed for the decision.

| Question / task | Read first | Then read / condition |
|---|---|---|
| What can we actually run on the issued LinQ access? | [LinQ][linq]: “Conditional implementation routes R001–R008” and SDK environments | [Video][video]: access matrix; [strategy][strategy]: accepted execution witness. A custom-model API with versioned outputs and accepted execution proof can suffice without SSH; GUI/catalog/job access may not satisfy the actual case. |
| Where are traceable pretrained helmet/PPE weights? | [Model critic][models] → [W1-05 PPE weights][ppe-weights] | [Dataset acquisition catalog][data] → [LinQ detector candidates][linq]. SH17 weights are candidates with class-map/version/rights gates, not a proven LinQ deployment or a `no_helmet` classifier. |
| How do we export a custom-class detector and decode its outputs? | [LinQ][linq]: ONNX boundaries; “Custom-class adapter: 4+nc versus 5+nc, NMS and class mapping” | [Model export][model-export] and [pre/post probes][model-parity]; [evaluation][eval]: native/export/compiled parity. Pin exact exporter, graph, class map, geometry and NMS semantics. |
| How should INT8/calibration failures or compiler rejection be diagnosed? | [LinQ][linq]: PTQ percentile and runtime tensor ABI | [Training D13](Deep-Research/training_strategy/report_machine_training_strategy.md#d13) for conditional PTQ/QAT/pruning choices; [evaluation][eval] for first divergence. CPU fake quantization is not vendor PTQ or hardware accuracy. |
| How do we turn a missing helmet or respirator detection into a violation? | [Methods: semantics](Deep-Research/violation_methods/report_machine_violation_methods.md#semantics) and [formulations](Deep-Research/violation_methods/report_machine_violation_methods.md#formulations) | [Datasets][data]: literal annotation units; [evaluation][eval]: person–PPE ownership. Non-detection is not absence; hidden/too-small/unobserved is unknown. Respirator absence, transition and specific-item removal need different evidence. |
| How do zones, tracking and time become a defensible episode? | [Methods: tracking](Deep-Research/violation_methods/report_machine_violation_methods.md#tracking) and [event time](Deep-Research/violation_methods/report_machine_violation_methods.md#event-time) | [Video][video]: ordered observations/Gap/epochs; [evaluation][eval]: geometry and event matching. Floor homography does not establish 3D intrusion; source loss does not prove compliance. |
| Can smoking, pose or VLM cascades cover the remaining classes? | [Methods][methods]: smoking evidence, observability and VLM cascade | [Datasets][data]: smoking localization versus classification; [LinQ][linq]: exact auxiliary-network placement. RGB cannot prove respirator fit, hazardous container contents or hidden actions. |
| Which data may we train on, demonstrate or redistribute? | [Datasets][data]: “Action-specific rights and acquisition decisions” plus exact dataset section | [Model critic][models] for weight/code rights; [market][market] for site/data flow. No blanket commercially usable list: code, annotations, photographs, weights and assembly have distinct rights. |
| Which split and annotation mapping are safe? | [Datasets][data]: dataset lineage, competing SFCHD splits, preliminary class mapping | [Evaluation][eval]: splits/lineage/adaptation; [training D08](Deep-Research/training_strategy/report_machine_training_strategy.md#d08). Group originals and derivatives before selection; ordinary union of partial YOLO labels can create false negatives. |
| Is training worth the remaining time, and what should be labeled next? | [Training D01](Deep-Research/training_strategy/report_machine_training_strategy.md#d01), D04–D06 and [input-dependent scenarios](Deep-Research/training_strategy/report_machine_training_strategy.md#scenarios) | [Evaluation][eval]: independent support and paired selection; [datasets][data]: target coverage. Use stage/oracle diagnosis first; teacher confidence cannot establish missed-positive recall. |
| Which checkpoint can be selected, resumed and handed off safely? | [Training D15](Deep-Research/training_strategy/report_machine_training_strategy.md#d15) | [Model critic][models] and [strategy][strategy]: immutable full-bundle rollback. Saved EMA/stripped initialization is not exact online-state resume; preserve export/prepost/rules/runtime provenance too. |
| How can we measure false alarms and misses honestly? | [Evaluation][eval]: false delivered records, source ownership/finite close, probability-sampled continuous review | [Methods][methods] for episode semantics; [product][product] for human review. A complete delivery census with sufficient-context adjudication can support semantic false records/source-camera-hour; recall and verified-normal exposure require independent source review. |
| How should events be matched, deduplicated and counted? | [Evaluation][eval]: temporal benchmarks, `lex-offline-v1`, uncertain onset/censoring | [Methods][methods]: episode/cooldown; [video][video]: event revisions/outbox; [product][product]: review versus delivery. Tiny exact oracle is not a scalable production scorer; transport retries and recurring incidents are different. |
| What architecture supports several RTSP cameras without stale results? | [Video][video]: ingress traps, bounded scheduling and per-camera cycle | [Methods][methods]: required cadence/gaps; [evaluation][eval]: load/freshness denominators. Sampling after decode does not remove source decode cost; aggregate FPS does not guarantee any one camera's coverage. |
| What must survive timeout, reconnect or restart? | [Video][video]: remote ledger; event COMMIT/outbox; backup/recovery | [Product][product]: independent health/media/delivery states. Local timeout does not terminate remote work or release quota; missing observation is not an empty safe frame. |
| Which analyzed image/clip should the operator see, and who acts? | [Product][product]: recipient maps, evidence card and 17-group contract | [Video][video]: own-frame projection and early event→original mapping gate. Snapshot fallback cannot fulfill a mandatory exact-clip requirement; delivery ACK is not human acceptance or hazard clearance. |
| What can we claim about 50/500 cameras, costs or differentiation? | [Video][video]: conditional sizing; [market][market]: A08 economics, A09 hardware, A12 differentiation | [Evaluation][eval] for measured full-chain load. No measured LinQ capacity/node count; IVA CV's June 2026 PPE+LinQ announcement defeats generic “first on LinQ” novelty without proving shipment or performance. |
| What evidence and artifacts make a convincing, compliant defense? | [Strategy][strategy]: official obligations, LinQ proof, reference sufficiency and actual viewer path | [LinQ][linq] + [evaluation][eval] + [product][product]. Private GitHub alone is not submission; preserve the exact saved rules, receipt requirements and replay/live distinction. |

## Decisions that need several studies

- **Commit to a model:** model critic/weights → dataset class units and rights → LinQ exact-graph gate → evaluation parity/target support. Add training only when detector adaptation addresses the diagnosed error. A family name is not an artifact compatibility claim.
- **Commit to a violation workflow:** methods' observable predicate and owner → video's source-time/cadence/Gap contract → product recipient/action/media states → evaluation event and delivery endpoints. Freeze the whole policy, including cooldown and unknown handling.
- **Commit to a deployable demo:** strategy's actual-case/last-useful-deadline gate → LinQ trusted completion → video integrated trace → product evidence/action → evaluation claim level. One successful request does not establish mandatory class coverage or live capacity.
- **Commit to a pilot:** market buyer/data-flow/BOM assumptions → product accountable response → video measured resources → evaluation frozen acceptance protocol. A pilot, a grant and a purchase are separate decisions; detected incidents are not demonstrated injury reduction.

## Critical constraints and disagreements

1. **Hardware evidence is incomplete.** Public documentation does describe local blocking `inference.sync(input_dict)`; saying “no completion API exists” is too broad ([evaluation F002](Deep-Research/evaluation/RAW_FACTS.md#f002)). It does not supply the allocated remote service, matching SDK/native/driver/firmware or own-model execution. Link graph coverage and completed request/output to the actual LinQ run or an case-setter-accepted execution witness.
2. **Versions and graph boundaries differ.** Model/training material inspects Ultralytics 8.4.184; LinQ analyzes 8.3.0/8.3.200 contexts. In particular, `nms=False` is not a version-independent output contract. Early model-fragment DFL compilation claims are unsupported by the final [LinQ candidate boundary, F330](Deep-Research/research_link_platform/RAW_FACTS.md#f330). Historical source defects are not proof of a current runtime defect.
3. **Dataset labels are not policy truth.** SHWD `person` boxes are head regions; SH17 `Off` describes an item's state, not automatically a violating wearer. SFCHD has two 2,475-image validation protocols sharing only 520 images, with test overlap. Parent/child datasets are not independent holdouts. CPPE's Apache grant covers code/annotations; photo rights remain separate. Start with the exact [dataset artifact sections][data].
4. **Temporal and operational gaps remain visible.** Tracking predictions/reused frames are not new observations. ByteTrack's inspected fixed update step is not repaired by attaching PTS. Cooldown suppresses delivery, not incident history. Video, analysis, recording, delivery, review and hazard status cannot be collapsed into one green indicator.
5. **Metrics need named endpoints.** AP, person-state recall, timely episode recall, semantic false deliveries and operator workload answer different questions. Later [evaluation W2 corrections, F003–F006](Deep-Research/evaluation/RAW_FACTS.md#f003) refine stricter early review/matching claims; do not silently combine normal-hours and source-hours denominators or incompatible TP populations.
6. **Official rules have unresolved differences.** Saved PDF lists seven 0–3 criteria; FAQ lists six, omitting UX/UI. Weights/aggregation are unknown. The 45-hour plan, suggested feature cuts, pilot thresholds and scale estimates are recommendations, not organizer guarantees. Use [strategy][strategy] for obligations and conflicts, not another report's shortened rules summary.

## Highest-impact unknowns and how to close them

These are **unresolved in the saved materials**, not claims about what organizers have supplied since then.

| Closure owner / input | Missing decision | Exact starting register |
|---|---|---|
| Organizers | Full mandatory taxonomy, observability/latency/quality/scorer, neural-stage placement, accepted LinQ witness, submission/recording/AI/resource rules and scoring conflicts | [Strategy questions](Deep-Research/hackathon_strategy/OPEN_QUESTIONS.md): Q001–Q008, Q016; [methods questions](Deep-Research/violation_methods/OPEN_QUESTIONS.md): Q001–Q009 |
| Issued LinQ access + local experiment | Matching bundle/model/golden tensors, upload/update rights, actual output/NMS, quotas, submit ambiguity, cancellation/terminal state and trusted completion | [LinQ questions](Deep-Research/research_link_platform/OPEN_QUESTIONS.md): Q001–Q005, Q020–Q023; [video questions](Deep-Research/video_architecture/OPEN_QUESTIONS.md): Q001–Q003, Q025 |
| Dataset inspection + independent reference | Native target footage/rights, original groups and complete observable labels; selected donor/license/split protocol; continuous or probability-sampled source review for the intended metric | [Data questions](Deep-Research/datasets/OPEN_QUESTIONS.md): Q001–Q003, Q007–Q008, Q014, Q020; [evaluation questions](Deep-Research/evaluation/OPEN_QUESTIONS.md): Q002, Q005–Q006, Q014–Q018 |
| Team decision + integrated experiment | Realistic scope/deadline, model-stack consolidation, measured full cycle/cadence, clip mapping, runtime installability and recovery | [Model critic][models]; [training scenarios](Deep-Research/training_strategy/report_machine_training_strategy.md#scenarios); [video questions](Deep-Research/video_architecture/OPEN_QUESTIONS.md): Q005, Q007, Q010, Q015, Q024 |
| Customer/site owner | Responsible recipient/action window, channels, retained media/data flow, complete node/license quote and pilot acceptance | [Product questions](Deep-Research/operator_product/OPEN_QUESTIONS.md): Q001–Q006; [market questions](Deep-Research/market_deployment/OPEN_QUESTIONS.md): Q003–Q004, Q012, Q016 |

## Evidence and reliability

F/S/Q/E identifiers are **topic-local**, sometimes branch-local in `model_stack`; always retain topic + file + ID. `RAW_FACTS` leads to source records and saved `_WORK` artifacts. `SOURCES` records inspected versions, dates, retrieval limits and provenance; repeated use of one source across topics is not independent corroboration. In the incomplete model study, facts/sources live inside WAVE1 branches.

Keep each report's evidence labels and scope: documentation, vendor claim, inspected code, external measurement, local observation, inference, hypothesis and unknown are distinct. `LOCAL` may mean metadata or arithmetic, not model execution. Datasets include completed bounded artifact checks; evaluation includes tiny evaluator fixtures; LinQ/model fragments include CPU probes. Product, training and video's experiment banks are proposals. A critic's “closed” can mean a corrected design or explanation while runtime benefit remains untested.

For a critical decision, inspect the exact fact, source version and retained artifact, then the latest W2 disposition. Research histories are preserved; older claims can remain in raw/branch files. Do not overwrite them with a synthesized certainty.

[linq]: Deep-Research/research_link_platform/report_machine_linq_platform.md
[linq-human]: Deep-Research/research_link_platform/report_human_linq_platform.md
[models]: Deep-Research/research-model-stack-claude/model_stack/CRITIC.md
[ppe-weights]: Deep-Research/research-model-stack-claude/model_stack/_WORK/WAVE1/W1-05_PPE_HELMET_VEST.md
[base-weights]: Deep-Research/research-model-stack-claude/model_stack/_WORK/WAVE1/W1-03_files/assets_catalog.tsv
[model-export]: Deep-Research/research-model-stack-claude/model_stack/_WORK/WAVE1/W1-10_EXPORT_ONNX.md
[model-parity]: Deep-Research/research-model-stack-claude/model_stack/_WORK/WAVE1/W1-11_PRE_POST.md
[methods]: Deep-Research/violation_methods/report_machine_violation_methods.md
[methods-human]: Deep-Research/violation_methods/report_human_violation_methods.md
[data]: Deep-Research/datasets/report_machine_datasets.md
[data-human]: Deep-Research/datasets/report_human_datasets.md
[training]: Deep-Research/training_strategy/report_machine_training_strategy.md
[training-human]: Deep-Research/training_strategy/report_human_training_strategy.md
[eval]: Deep-Research/evaluation/report_machine_evaluation.md
[eval-human]: Deep-Research/evaluation/report_human_evaluation.md
[video]: Deep-Research/video_architecture/report_machine_video_architecture.md
[video-human]: Deep-Research/video_architecture/report_human_video_architecture.md
[product]: Deep-Research/operator_product/report_machine_operator_product.md
[product-human]: Deep-Research/operator_product/report_human_operator_product.md
[market]: Deep-Research/market_deployment/report_machine_market_deployment.md
[market-human]: Deep-Research/market_deployment/report_human_market_deployment.md
[strategy]: Deep-Research/hackathon_strategy/report_machine_hackathon_strategy.md
[strategy-human]: Deep-Research/hackathon_strategy/report_human_hackathon_strategy.md
