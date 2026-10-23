---
topic: violation_methods
context_version: mosprom-research-v1
checked_at: "2026-10-23T07:28:35.8658654+03:00"
timezone: Europe/Moscow
source_access: "2026-10-23, approximately 05:59–06:26 MSK; compression uses saved evidence, without new source access"
scope:
  - "Operational video predicates, PPE ownership and coverage, visibility/abstention, floor zones and proximity, tracking and source-time event logic."
  - "Conditional methods for smoking, respirator state/removal, lying/fall and harness/hook; camera envelopes, neural workloads, LinQ/INT8 gates, event evaluation and proposed experiments."
not_covered:
  linq_platform: "Assigned hardware, SDK/compiler/runtime inventory, access and supported operations."
  model_stack: "Complete model/weight/export catalogue and executed model chains."
  datasets: "Dataset inventory, licences and full annotation-archive audits."
  training_strategy: "Training/adaptation implementation."
  evaluation: "Complete final acceptance protocol; this report specifies method-selection requirements."
  video_architecture: "Complete video service, transport and deployment implementation."
  operator_product: "Operator interface and incident workflows."
  market_deployment: "Legal qualification, market/economics and deployment certification."
  hackathon_strategy: "Complete competition/presentation strategy."
case_materials:
  available: "Both task prompts, public announcement, two research waves, fresh-context critique, collected evidence and edited human report."
  unavailable: "Full case, customer native-resolution videos/data, assigned LinQ device/SDK/compiler/runtime and acceptance programme."
  announcement_examples: [no_helmet, respirator_removed, danger_zone_entry, smoking_near_flammables]
  execution_requirement: "Model inference on LinQ; online access promised. Scope of auxiliary neural stages remains Q005."
actual_checks:
  research: "Documents/code/metadata read; selected XML/JSON/images inspected. Code reading and manual traces were not runtime execution."
  compression: "English synthesis of saved final human report and evidence; own YAML, schema and relative-link consistency."
  not_executed: "Models, training, benchmarks, LinQ export/compile/inference, VMS runtime and every E001–E017."
files:
  human: report_human_violation_methods.md
  sources: SOURCES.md
  facts: RAW_FACTS.md
  critique: CRITIC.md
  questions_and_experiments: OPEN_QUESTIONS.md
answers:
  - "What is observable violation T, rule F or unknown U, and how do item, coverage and removal differ?"
  - "Which conditional method, ownership relation, geometry, data and workload fit each violation within 45 hours?"
  - "When are detector, crop attributes, pose, HOI, temporal model, OVD or VLM justified?"
  - "What do product camera pixel/FPS/angle conditions establish, and when must a method abstain? Target admission remains Q004."
  - "How should floor occupancy, directional crossing, metric proximity, activation and authorisation be separated? Case policy remains Q003/Q014."
  - "How do track identity, source timestamps, reuse/prediction, gaps and stale evidence affect event correctness? Actual cadence remains Q007."
  - "How should confirmation, observed clear, technical end, deduplication and notification cooldown work? Selected settings remain Q008/Q013."
  - "What typed rule and evidence schema can represent the proposed event pipeline?"
  - "Which neural inputs and INT8 risks must be presented to LinQ, and which four gates establish an exact artifact? Execution remains Q005/Q006/Q020."
  - "What evidence supports fixed/dynamic OVD and reject-only VLM verification? Our paired VLM benefit remains Q019."
  - "How should actor-aware event matching, negative camera-hours, latency, coverage and censoring be measured? Acceptance remains Q008."
  - "What actionable procedures E001–E017, first 15–20 minute decisions, P0 questions and topic handoffs follow?"
keywords: [PPE, СИЗ, hardhat, helmet, respirator, gas_mask, coverage, item_doffing, ownership, T/F/U, Strong_Kleene, abstention, risk_coverage, floor_zone, bottom_center, ankle, homography, proximity, TTC, smoking, cigarette, fall, lying, harness, hook, ByteTrack, OC-SORT, BoT-SORT, Frigate, source_timestamp, PTS, measured_reused_predicted, LinQ, ONNX, INT8, PTQ, QAT, OVD, YOLO-World, YOLOE, Grounding_DINO, VLM, event_matching, FA_per_hour]
entity_schema:
  violation_method:
    fields: [id, semantics, cues_association, method_geometry_time, admission_data_errors, workload_execution, checks_feasibility]
    conventions: "Every VM record has all seven fields. PROP routes inherit the explicitly linked contracts. T/F/U refers to the stated predicate/rule, never universal safety."
  experiment:
    fields: [id, decision, inputs, steps, measurements, evidence, outcomes_limits]
    conventions: "Every E record is proposed/unexecuted; thresholds are calibrated then frozen before test."
takeaways:
  - "Conditional baseline: detector + explicit part/owner association + CPU tracker/geometry + source-time T/F/U rules and evidence. Fixed floor zone and helmet are shortest routes only with suitable camera/data and a proven LinQ artifact."
  - "Missing detection is not uncovered; spare/off-body PPE is not missing body coverage. A false named rule is not global compliance."
  - "Uncovered state, coverage-loss and strict item-doffing require different GT and inputs. Blind gaps bound change; they do not establish observed removal."
  - "Use source/analytics/native-crop/tensor pixels separately. Product minima/optima are scoped; DORI and thermal smoking distance are not RGB PPE guarantees."
  - "U neither accumulates positive observed duration nor establishes observed clear. Track loss, scene invalidation and stream loss need technical end/censoring."
  - "Export correctness, compilation, actual assigned-LinQ execution and preserved output/event quality are separate gates; none was executed here."
  - "Pose/crops/ReID/clip/VLM add neural inputs and failure paths. Include them after measured benefit and an authorised execution path."
  - "VLM reject-only benefit needs paired baseline TP/FP→accepted/rejected/unverified, TP-loss/FP-rescue and latency. It cannot recover upstream misses."
  - "All E001–E017 remain proposed; full case, native camera admission, exact LinQ and acceptance are explicit unknowns."
---

# Video violation methods: decisions and evidence

**INF/PROP:** Start with the simplest available detector, explicit person–part–item relations, a CPU tracker, geometry and a source-time event engine. Admit each camera-region/predicate separately. Add pose, native crops, ReID, temporal networks or VLM only for an identified error and measured benefit within the execution/latency budget. This is a research recommendation, not a tested system. [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F116](RAW_FACTS.md#f116), [F119](RAW_FACTS.md#f119), [F123](RAW_FACTS.md#f123).

**UNK:** The announcement examples are not a complete mandatory list. Full case/data/native customer video, assigned LinQ and acceptance are absent. RTX/laptop can support training/reference/debugging; their exact configuration is unknown and success there does not establish LinQ execution. [DOC F065](RAW_FACTS.md#f065), [Q005](OPEN_QUESTIONS.md#q005), [Q006](OPEN_QUESTIONS.md#q006).

Evidence tags: **DOC** primary documentation/method disclosure; **CODE** source read, not executed; **PUB-MEAS** authors' published measurement; **VENDOR** interested-party claim, including abstract-only reports; **LOCAL-OBS** actual artifact/image inspection; **INF** inference from linked evidence; **PROP** proposed specification/test; **UNK** unresolved or access-limited. Evidence type and executed-check status differ. Repeated reading of one chain is not independent replication. F/S/Q/E IDs link to portable local anchors. Late W2 corrections supersede historical W1 interpretations; [CRITIC.md](CRITIC.md) preserves that history. No E was executed.

<a id="semantics"></a>
## Item, body-part coverage and rule T/F/U

**PROP:** Keep this pipeline explicit: `source frame/time → detections/parts → track and relations → observable body-part state → T/F/U rule → temporal confirmation → event/evidence`. AWS PPE separates person/bodypart/item/coverage confidence and `PersonsWithRequiredEquipment`, `PersonsWithoutRequiredEquipment`, `PersonsIndeterminate`; Macroscop leaves respirator/glasses indeterminate when the face is invisible. These support a contract, not use of AWS or measured quality of our gate. [DOC F013](RAW_FACTS.md#f013), [F014](RAW_FACTS.md#f014), [F017](RAW_FACTS.md#f017), [PROP F100](RAW_FACTS.md#f100).

| Proposed record | Required meaning |
|---|---|
| `item_observation` | frame/time, item ID/type/bbox, relation to person/target part, on-target/off-target/unknown and relation provenance. Ownership of an object differs from whom it currently protects; a table item may have no known wearer. |
| `coverage_observation` | person/track incarnation, part (`head`, `eyes`, `nose-mouth`, `torso`, left/right hand), source time, approved-type policy, visibility/quality, T/F/U, item evidence IDs and reason. |

`coverage=T` requires visibly adequate coverage by at least one approved item. `coverage=F` requires a visible target part and evidence that every allowed covering is absent, or visibly insufficient coverage under the agreed policy. Missing positive boxes, an unknown type, off-body items, or all detected items being off-body do not establish F. Hidden/too-small/low-quality/ambiguous owner/unsupported type/inference missing → U. An invisible pose joint remains a hypothesis despite its confidence. Proposed reason literals: `part_not_visible`, `too_small`, `low_quality`, `owner_ambiguous`, `unsupported_type`, `inference_missing`. Visual coverage does not prove fit, seal, certification or condition. [PROP F100](RAW_FACTS.md#f100), [F119](RAW_FACTS.md#f119).

Spare glasses in hand do not cancel glasses on eyes; a respirator on the neck does not establish an uncovered face if another is worn or the face is hidden. For both gloves, `C=C_left AND C_right`: visible bare left + hidden right → F; gloved left + hidden right → U. Product logic accepting one visible glove measures another predicate. [DOC F018](RAW_FACTS.md#f018), [PROP F100](RAW_FACTS.md#f100).

T = supported assertion; F = supported negation; U = insufficient evidence. They are not confidence bands. Strong Kleene `NOT T=F; NOT F=T; NOT U=U`:

| AND | T | F | U |
|---|---|---|---|
| T | T | F | U |
| F | F | F | F |
| U | U | F | U |

For PPE, `R=requirement for approved type active`, `Z=subject in its scope`, `C=approved target coverage`, `G=R AND Z`, `V_ppe=G AND NOT C`. A non-zonal rule defines Z=T. Unknown role/operation does not set R=F. The AND table plus the table below factor all 27 C/R/Z combinations; an additional genuinely required action A uses AND and yields all 81 combinations. A continuous wearing requirement must not require a removal action: an already-uncovered arrival can violate it. [PROP F100](RAW_FACTS.md#f100), [F102](RAW_FACTS.md#f102).

| Applicability G | C=T | C=F | C=U |
|---|---|---|---|
| T | F | T | U |
| F | F | F | F |
| U | F | U | U |

For smoking, `V_smoke=S AND H`, with S defined smoking in an observable window and H supplied hazardous/flammable context plus the person's position there. Necessary activation/material/zone components also use T/F/U. Missing cigarette/smoke/action is not S=F; define a sufficiently observable negative interval in GT. Drinking does not automatically exclude simultaneous smoking. Rule F means only the named compound rule is false, not absence of smoking or universal safety. [PROP F100](RAW_FACTS.md#f100), [F123](RAW_FACTS.md#f123).

Five hand-checked semantic counterexamples (not a model/code benchmark):

| Observation | Correct result | Required negative evidence |
|---|---|---|
| Inside, mouth/hands hidden | H=T,S=U,V=U | observable negative smoking window or H=F; missing cue is insufficient |
| Smoking visible, reliable position outside supplied zone | S=T,H=F,V=F | H=F already negates this rule; S remains T |
| Smoking visible, anchor/material/zone unknown | S=T,H=U,V=U | reliable H=F or agreed negative S window |
| Approved item worn plus spare off-body | C=T,R=Z=T,V_ppe=F | worn approved coverage suffices; spare changes nothing |
| Off-body item visible, target head/face hidden | item off-target,C=U,R=Z=T,V_ppe=U | observe target covered for V=F or visibly uncovered for V=T |

**LOCAL-OBS:** SH17 firefighter photo has a labelled helmet on a removed jacket while the person's head is outside frame: item off-target, head coverage U. Two inspected VOC/XML examples lack wearer/on-off/relation fields; TXT has five columns. This is not an audit of all 8099 images or proof that no separate extended export exists. [F066](RAW_FACTS.md#f066)–[F068](RAW_FACTS.md#f068), [image](_WORK/SOURCES_W2A/firefighter.jpeg), [Q010](OPEN_QUESTIONS.md#q010).

<a id="formulations"></a>
## PPE formulations, annotation semantics and ownership

**INF:** No universal formulation wins. Select by annotation unit, available detail, actual bottleneck and deployable artifact; compare on identical data. [PROP F120](RAW_FACTS.md#f120).

| Formulation | Direct output / conditional use | Failure/cost |
|---|---|---|
| Person + PPE object boxes | shared fullframe graph when detail suffices | object presence needs separate part/owner relation |
| Head-state detector | local worn/bare/unknown semantics correctly labelled | `head` may mean any head; missing box is not bare |
| Direct person states | few combinations, sufficiently large person | combinations proliferate; invisible parts can be mislabelled nonwearer |
| Person crop + multilabel classifier | native detail with a controlled ROI | person-stage misses, neighbour/held item in crop; cost scales with people |
| Pose + part crops | measured leaning/ownership bottleneck | keypoint/crop error precedes classifier; more neural inputs |
| Learned association/HOI | relation GT and actual export path available | new labels/graph; difficult default within 45 hours |
| Temporal action model | endpoint needs a sequence | timestamped buffer, sampling and boundary GT; upstream misses persist |
| OVD/VLM | candidate discovery, annotation assistance or measured verification | names/answers do not establish wearer, coverage, time or visibility |

**DOC/CODE:** Pictor-PPE A1 detects worker/hat/vest then relations; A2 predicts `W/WH/WV/WHV` (neither/hat only/vest only/both); A3 worker→crop classifier. Inspected `detect.py` establishes decode/NMS, not the complete downstream A1 tree. SHWD `person` means negative normal-head object, not COCO full-body person; preserve geometry and semantic remap. [F001](RAW_FACTS.md#f001), [F003](RAW_FACTS.md#f003), [F004](RAW_FACTS.md#f004).

**PUB-MEAS:** Same X101 detector on 7035 images (5269 train/1766 test): keypoint AP .675 vs refit decision tree .664; same-training direct wearer/nonwearer .663; both AP50 .826. APsmall .211 vs .222 refit and .248 direct limits any claim of pose superiority. Not a crowded ownership benchmark or our run. A modular pose/crop study uses elbows/wrists, rejects hands behind torso and back-facing glasses crops, and exposes `indecisive`/`undefined`. Closed-CCTV crop classifier accuracies hardhat/vest/glove/eyeglass .92/.98/.86/.95 omit upstream chain/event failures and use different splits. [F008](RAW_FACTS.md#f008)–[F012](RAW_FACTS.md#f012).

**PROP ownership:** Generate person–head–PPE candidates by containment, overlap/anchor and normalised distance; assign one-to-one to target parts. Person-box containment is candidate generation, not wearing. Upper-box fractions require a validated upright/sparse scene and fail at leaning/crouching/lying. Respirator links to lower face; gloves link to two specific hands. One item must not cover multiple people. Conflicting owners → `owner_ambiguous`/U. Calibrate thresholds; none is universal. Separate false violation from missed PPE and false coverage from neighbour/held/spare PPE. E002 first holds oracle boxes fixed, then the real detector fixed, to isolate relation error. Include crowd crossing, bends, raised removal hand, held/table/belt/spare PPE, caps/hoods/hair/bald heads, partial bodies/foreign feet, reflections/posters/mannequins and tools. [F120](RAW_FACTS.md#f120), [E002](OPEN_QUESTIONS.md#e002).

**DOC/LOCAL-OBS annotation acceptance:** SH17 `head` is any head; `face` requires a visible nose; medical mask is not generic industrial respirator. Table category order differs from actual YOLO `helmet=10`, `hands=11`, `head=12`, `face-mask=5`. Published extended on/off tags do not establish that a base TXT loader retrieves wearer/coverage relations: obtain artifact, guide and examples. R2PPE `absent` includes nonwearing or uncovered nose and mouth; `incomplete` exposes nose while mouth is covered; N95 complete is separate. Unresolvable ambiguity was omitted, not labelled absent. Actual `annotations/combined.json`: 10034 images, 123751 annotations, 18 categories; union keys `area,bbox,category_id,id,image_id,iscrowd,segmentation`, no wearer/track/relation or neck/hand/remove labels. `N95_Strap_s` is not a seal result; healthcare images are not industrial cartridge scenes. [F005](RAW_FACTS.md#f005), [F007](RAW_FACTS.md#f007), [F072](RAW_FACTS.md#f072), [F073](RAW_FACTS.md#f073), [F101](RAW_FACTS.md#f101), [E001](OPEN_QUESTIONS.md#e001).

<a id="violation-methods"></a>
## Violation → method records

All records are **PROP/INF**, not accepted implementations. PPE rules use [item/coverage T/F/U](#semantics); state-event timing uses the proposed [event sweep](#event-time), never a safety norm. Workload symbols and exact LinQ gates are in [neural workload](#linq). Every camera/type/part needs [admission](#camera); missing detail cannot be repaired by upscaling or VLM.

### VM01 — Helmet missing

- **id:** VM01.
- **semantics:** V=T when approved helmet is required in scope and a visible head has no approved coverage; V=F with approved worn helmet or false applicability; U for hidden/tiny/unknown type/ambiguous owner. `helmet-on` does not prove strap, suspension, condition or service life; `strap_visible_closed` is a separate endpoint if required.
- **cues_association:** helmet↔head one-to-one; a rear-visible helmet need not wait for visible face. Hand/table/belt/spare helmet never establishes head coverage alone.
- **method_geometry_time:** correct head-state detector or person+helmet+head association; geometry baseline for upright sparse fixed scenes. Test pose only for demonstrated crowd/leaning errors. Use source-time confirmation/clear/gap policy.
- **admission_data_errors:** readable head; worn, visibly bare and U labels plus hood/cap/hair/baldness, white overexposure, reflection/neighbour and off-body negatives. High thresholds/missed small helmet → false violation; held/neighbour helmet → false coverage.
- **workload_execution:** shared fullframe detector f; optional native head crops/pose add inputs. Small-head confidence/coordinate drift under INT8 must preserve relations and events; no family-name support assumption.
- **checks_feasibility:** E001/E002/E003/E015; strong early 45-hour candidate if camera/data/exact graph pass. [F009](RAW_FACTS.md#f009), [F023](RAW_FACTS.md#f023), [F119](RAW_FACTS.md#f119), [F120](RAW_FACTS.md#f120).

### VM02 — Vest / required protective garment missing

- **id:** VM02.
- **semantics:** required approved torso coverage visibly absent → V=T; approved coverage → F; hidden torso, unrecognised substitute or unsupported colour-dependent IR → U. Policy may allow a jacket rather than vest.
- **cues_association:** worn garment on this torso; garment/helmet colour is not authorisation. Macroscop's generic sleeveless garment of any colour is not certified high-visibility clothing.
- **method_geometry_time:** fullframe garment detector or crop attributes with torso relation and source-time state confirmation.
- **admission_data_errors:** readable torso/strips, approved clothing alternatives and disallowed lookalikes, occlusion and actual night/IR labels. RGB colour cannot be asserted from monochrome nearIR.
- **workload_execution:** often the same f detector; crops add P×r. Check strip/detail and confidence changes after INT8; validate real camera mode rather than promising universal night support.
- **checks_feasibility:** E001/E003/E013/E015; short conditional extension if taxonomy/data match. [DOC F017](RAW_FACTS.md#f017), [F018](RAW_FACTS.md#f018), [F048](RAW_FACTS.md#f048), [PROP F119](RAW_FACTS.md#f119).

### VM03 — Respirator coverage missing / insufficient now

- **id:** VM03.
- **semantics:** A=`face visibly uncovered under requirement`; visible insufficient/absent approved nose-mouth coverage under R=Z=T → V=T. Approved coverage → F; back/hidden/tiny/type/owner unknown → U. Finding a removed item is unnecessary for this state.
- **cues_association:** current readable nose-mouth region, owner, policy and source time. Neck/hand/spare object does not establish uncovered face, and medical mask does not automatically satisfy industrial cartridge policy.
- **method_geometry_time:** head/face-state detector or native local classifier; independent current state after a gap. Bound recent wearing evidence; never smooth stale wearing through removal. Use checkpoint or validated camera-region if wide view fails.
- **admission_data_errors:** approved on-face, visible uncovered/insufficient, wrong substitute, neck/hand/spare and U; beard/hood/shield, second worn item, turning, adjustment and neighbour negatives. YOLOv8-LPE has front/side `wear_mask`, `no_wear`, `wear_wrong`, seventh `back_head`; wrong includes medical mask instead of industrial 3M cartridge. 7992 images, 6058/1934 train/test, real+simulated; no obtained neck/hand/removal labels/code/artifact. §3.2 confuses AP IoU and confidence threshold; Table 2 F1 inconsistent.
- **workload_execution:** local calls scale with readable faces; optional chain misses/queues add stale state. INT8 checks include small face, neck/spare and backlight/IR. 3M 6000 requires strap adjustment, each-donning seal check and fit testing: RGB cannot prove leak, correct cartridge, fit or life.
- **checks_feasibility:** E001/E003/E016/E015; state-only feasible within 45 hours only with readable industrial-type face/data/graph. Exact endpoint Q002 and artifact Q011 remain open. [F016](RAW_FACTS.md#f016), [F069](RAW_FACTS.md#f069), [F070](RAW_FACTS.md#f070), [F102](RAW_FACTS.md#f102).

### VM04 — Observed respirator coverage-loss / item-doffing

- **id:** VM04.
- **semantics:** Coverage-loss requires reliable C=T before and C=F after for same person with allowed continuity. Strict D_item requires that particular item on-target before, observed temporally linked removal/contact trajectory, off-target after and item/person continuity. D=T can coexist with C=T if another approved item remains; violation due to removal requires `D AND R AND Z AND NOT C`.
- **cues_association:** before/during/after evidence and track/item identity. Already-uncovered entry can violate VM03 but is not observed removal. No before-state, ID switch, hidden critical interval or ambiguous item identity → transition U, not forced-negative.
- **method_geometry_time:** sequence and item/person association; C(t), D_item(t), R/Z and visibility separate. A blind gap bounds change between last T and first F; it establishes neither exact onset nor observed action.
- **admission_data_errors:** target-type sequences wear→remove→neck/hand→rewear, hidden removal, entry already uncovered, spare/duplicate/swap and neighbour/ID-switch cases; GT state and transition separately.
- **workload_execution:** aligned temporal inputs/item association add networks, buffer and latency relative to VM03; actual exported graphs and INT8 event effects must pass gates.
- **checks_feasibility:** Q002/Q011, E016/E015; include within 45 hours only if required endpoint and suitable clips/access exist. If only state is observable, name it state and retain transition U. [F100](RAW_FACTS.md#f100), [F102](RAW_FACTS.md#f102).

### VM05 — Protective glasses missing

- **id:** VM05.
- **semantics:** visible eyes insufficiently covered under approved-type policy → V=T; approved eye coverage → F; hidden/indistinct/type/owner ambiguity → U. Forehead glasses are not eye coverage; spare glasses do not cancel worn ones.
- **cues_association:** eye-level relation to this person; distinguish corrective glasses, safety glasses, goggles and visor. Glare/transparent frames can remove discernible evidence.
- **method_geometry_time:** native eye/head crop classifier or detector, optionally pose-selected ROI after measured benefit; bounded current evidence and source-time state lifecycle.
- **admission_data_errors:** close enough original eyes/frame, approved alternatives, forehead/held/spare/visor and back/occlusion U; pose confidence does not prove visibility.
- **workload_execution:** crops/pose add per-person inputs; upstream localisation, small-object/coordinate INT8 drift and latency are part of end-to-end quality.
- **checks_feasibility:** E001/E002/E003/E013/E015; lower priority for overview cameras, conditional close-view extension. [F011](RAW_FACTS.md#f011), [F017](RAW_FACTS.md#f017), [F119](RAW_FACTS.md#f119).

### VM06 — Required left/right gloves missing

- **id:** VM06.
- **semantics:** both-required C=left AND right; one visibly bare required hand is enough for C=F/V=T; one gloved and other unknown → U; all required hands covered → F. One-glove presence is a different endpoint.
- **cues_association:** two named hands and their owner; tool, pocket, hand behind torso and neighbour hand cause visibility/association errors.
- **method_geometry_time:** hand crops, optionally elbow/wrist pose for candidate ROI with visibility gate; state/age per hand rather than incompatible best moments.
- **admission_data_errors:** readable native hands, glove types, tools/pockets/occlusion, held gloves and spare labels. Steel-plant person YOLOv8m→worker ROI→PPE YOLOv8m study reports average PPE F1 .93 yet gloves fully missed in >20% of low-light frames and framewise false non-compliance without history/tracking; ambiguous labels excluded, operational metrics closed and one/multistage comparison illustrative.
- **workload_execution:** per-part crop rate h×r, optional pose; INT8 small hand/glove and stale state can change events. Crop classifier .86 is not chain event recall.
- **checks_feasibility:** E001/E002/E003/E004/E013/E015; close-view/GT/budget required; overview may legitimately retain U. [F011](RAW_FACTS.md#f011), [F012](RAW_FACTS.md#f012), [F018](RAW_FACTS.md#f018)–[F020](RAW_FACTS.md#f020), [F119](RAW_FACTS.md#f119).

### VM07 — Fixed floor-zone occupancy

- **id:** VM07.
- **semantics:** required valid ground-contact anchor inside agreed floor polygon → T; reliable outside → F; hidden contact/invalid scene/unknown applicability → U. Hand in mechanism, whole-body containment and 3D overhead volume are different rules.
- **cues_association:** own ground contact, not neighbour feet; `ground_contact_observable` independent of detector/pose confidence. Truncated bottom, platform or machine occlusion can invalidate bottom center.
- **method_geometry_time:** person→CPU track→point-in-polygon. Bottom center baseline; `ankle-any` for “at least one foot”, not mean of ankles. Choose spatial hysteresis from calibration localisation error; occupancy uses current point, dwell/unique entries need history. [Geometry contract](#geometry).
- **admission_data_errors:** fixed/versioned camera and agreed floor semantics, visible contact; GT walks, leaning, one foot, hidden feet/crowd and boundary jitter. Bbox overlap gives false floor entry; no ankle is U, not violation.
- **workload_execution:** person detector f; tracking/geometry/temporal rules on CPU. Pose optional extra graph; verify anchor/INT8 error near boundary and actual cadence.
- **checks_feasibility:** E006/E009/E010/E015; shortest geometric branch within 45 hours when scene is valid. Q003 fixes floor vs volume. [DOC/CODE F027](RAW_FACTS.md#f027), [F036](RAW_FACTS.md#f036), [F037](RAW_FACTS.md#f037), [PROP F103](RAW_FACTS.md#f103).

### VM08 — Directional finite-line crossing

- **id:** VM08.
- **semantics:** same subject observed on reliable side before and opposite side after, valid finite-segment intersection and required direction → T. First appearance inside establishes occupancy, not observed crossing; absent history/large gap → U. Reliable observed non-crossing under defined sampling/window can be F; two outside samples alone cannot exclude traversal between them.
- **cues_association:** actor-consistent side history and ground anchor; line and direction vector separate, identity ambiguity invalidates transition claim.
- **method_geometry_time:** signed side with boundary band and finite-segment check; separate entry/exit lines if needed. Large gap leaves crossing onset unknown; interpolated path remains a hypothesis.
- **admission_data_errors:** fixed valid scene, correct coordinate transform, sufficient cadence for shortest event, walks in both directions, jitter, short-zone pass and already-inside arrival.
- **workload_execution:** same person detector plus CPU history/geometry; optional pose costs extra. Low FPS/INT8 anchor changes can change crossings; no detector FPS alone proves coverage.
- **checks_feasibility:** E006/E008/E009/E010; short 45-hour extension once VM07/time contract works. DeepStream `extended=0` finite vs `extended=1` extended line illustrates semantics, not LinQ portability. [DOC F038](RAW_FACTS.md#f038), [PROP F103](RAW_FACTS.md#f103).

### VM09 — Person–equipment proximity / active restricted envelope

- **id:** VM09.
- **semantics:** T only for agreed envelope/threshold and active rule; metric uncertainty/height/activation/authorisation unknown propagates U. “Unauthorised in active zone” requires confirmed presence, envelope, active hazard and authorisation=F. Missing access feed is not unauthorised; stationary equipment may be active.
- **cues_association:** person/equipment pair tracks, valid footprint/working envelope, supplied machine-state/permission sources with TTL. Helmet/vest colour and tracker ID do not prove role or access.
- **method_geometry_time:** fallback explicitly named dynamic image-zone; metres only after same-floor calibration/error validation. Minimum distance to footprint/working envelope, not bbox centers; Minkowski buffer is proposed geometry, not safety norm. Heading differs from travel direction; lifted forks/boom and other elevations need another model. TTC requires stable relative velocity/error budget; stop/turn/large error → U.
- **admission_data_errors:** geometry correspondences, independent distance/time reference, dimensions, equipment orientation/working organ and external-input contracts. Test near/far/edges, turns, occlusion and height changes without dangerous real approaches.
- **workload_execution:** person/equipment detector and CPU geometry; speed uses source timestamps. A monocular network would add its own graph, calibration and gates. INT8 footprint/anchor drift enters threshold FP/FN.
- **checks_feasibility:** E007/E010, Q003/Q014; optional case-added branch with required inputs; TTC/collision prevention is not a default 45-hour promise. [F028](RAW_FACTS.md#f028), [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046), [F104](RAW_FACTS.md#f104).

### VM10 — Smoking near supplied flammable/hazardous context

- **id:** VM10.
- **semantics:** `S AND H` with temporally overlapping evidence. `cigarette_visible`, `hand_to_mouth_pattern`, `smoking_action` differ; cigarette in hand is not a current puff, one gesture is not smoking, smoke need not be visible. S=U,H=T → U; S=T,H=F → this rule F while smoking remains T; S=T,H=U → U. A barrel/cylinder/container appearance does not establish contents/flammability.
- **cues_association:** readable original face/object and/or per-track hand trajectory with owner continuity; use supplied hazardous ROI/map/operation. Mobile-material proximity additionally needs material identity and geometry. Negative S needs agreed observable interval, not missing cue.
- **method_geometry_time:** A: when humans distinguish cigarette from pen/tool in native face ROI, object/face relation + temporal evidence. B: if object hidden but hand trajectory readable, compare per-track action candidate vs object+temporal; gesture alone remains candidate until matched test. Both unreadable → U/checkpoint. Long systematic FP can survive temporal confirmation.
- **admission_data_errors:** label action/cue/window separately; eat/drink/straw/lollipop, phone/radio, PPE adjustment/cough/scratch, pen/tool/finger, pocket/table/held-without-puff, neighbour smoker, vape, steam/dust/welding/reflection, blur/occlusion/ID switch. Native source, not preview, must carry detail.
- **workload_execution:** selected frames×readable faces/parts/heads; pose is neural even if wrist distance is CPU. Clip graph adds aligned buffer/stride/3D or attention operations; INT8 tiny object, crop/context loss and event effects need E015. VLM does not restore absent signal.
- **checks_feasibility:** E011/E013/E015, Q009; narrow close-view plus supplied zone within 45 hours, otherwise candidate/U/checkpoint. No matched industrial object/gesture/fusion event-FA-hour result was obtained. [F090](RAW_FACTS.md#f090)–[F093](RAW_FACTS.md#f093), [F108](RAW_FACTS.md#f108), [F109](RAW_FACTS.md#f109), [F123](RAW_FACTS.md#f123).

### VM11 — Lying, fall transition and post-fall immobility

- **id:** VM11.
- **semantics:** `person_lying` posture, `suspected_fall_transition` observed before/during/after transition and `post_fall_immobility` additional state are separate. Fast recovery does not cancel observed fall. Clip starts lying/transition occluded/track broken → transition U even if posture T. RGB does not automatically establish injury, medical emergency or intent.
- **cues_association:** same actor and visible transition; planned maintenance lying, slow/fast deliberate lying, kneeling/sliding/quadruped are necessary comparisons. Rapid deliberate lying may be visually indistinguishable without context.
- **method_geometry_time:** posture baseline vs timestamped temporal model. Do not impose long lying/inactivity as definition of every fall; an immobility endpoint may legitimately have its own gate. Camera movement can invalidate pixel-speed/pose cues.
- **admission_data_errors:** native whole-body/transition detail and separate GT timelines, include short/occluded/fast-recovery cases in U/coverage rather than removing them. Macroscop 4.7 fall explicitly detects lying and excludes falling process.
- **workload_execution:** detector/pose baseline or extra temporal/optical-flow network/buffer; legacy flow model is not a ready LinQ path. Validate all graphs and event consequences of INT8/low cadence.
- **checks_feasibility:** Q018/E012/E015, P2 if full case adds it; label output by actual endpoint. [F049](RAW_FACTS.md#f049), [F095](RAW_FACTS.md#f095), [F096](RAW_FACTS.md#f096), [F110](RAW_FACTS.md#f110), [F124](RAW_FACTS.md#f124).

### VM12 — Harness / hook state / attachment at height

- **id:** VM12.
- **semantics:** separate `in_height_work_context`, `harness_worn`, `lanyard_visible`, `hook_visible`, `hook_attached_to_valid_anchor`, `gate_locked`. Harness presence supports only itself; hidden hook/gate → U. Box intersection/proximity does not prove mechanical attachment. Image height is not work height in metres.
- **cues_association:** correct worker–harness–lanyard–hook–known anchor relations and readable native close crop. Physical GT required for attachment/locking; anchor/load strength cannot be certified by ordinary RGB.
- **method_geometry_time:** agreed visual-state detector/relations; supervised HDS classes `Wrong place`, `Safe`, `Wrong tie`, `Too thin`, `Not closed` are wider than presence, but `Safe` is not mechanical certification. Ground-floor calibration cannot establish elevated mechanism geometry.
- **admission_data_errors:** same-looking attached/unattached/open/hidden rig pairs, known anchors and expert inspection; tiny hook/occlusion/proximity are critical. HDS source-group split before augmentation unreported; no physical gate-lock/anchor protocol.
- **workload_execution:** fine-detail detector/native crops and relation logic; possible extra inputs and small-coordinate INT8 risk; exact artifact gates remain required.
- **checks_feasibility:** Q018/E012/E015, P2 if mandatory in full case. Within 45 hours harness presence in supplied context is a narrower defensible output; attachment needs separate observable endpoint/test. [F054](RAW_FACTS.md#f054), [F094](RAW_FACTS.md#f094), [F111](RAW_FACTS.md#f111), [F124](RAW_FACTS.md#f124).

<a id="scenario-evidence"></a>
## Smoking, fall and hook evidence that changes method selection

**DOC/PUB-MEAS:** Domination's RGB face→cigarette-near-face route has a narrow camera envelope in [camera table](#camera), not published action-window/hard-negative event evaluation. DAHD-YOLO (Sensors, 26.02.2025) is a single `cigarette` class, 2810 internet images, 8:1:1 image split; AP=mAP because there is one class. Fingers/pens/railings are documented FP. “Generalisation” retrains on cigarette-butts data, not camera transfer of a ready smoking model. CDPA-Net (26.04.2026) uses 6890 industrial ICSSD images and VOC cigarette-region boxes; “pose-aware” refers to contour/orientation/spectral features, not tracked skeleton/action sequence. Temporal cues remain future work. Neither provides matched object/gesture/fusion event FP/hour on eat/drink/phone/PPE-adjustment negatives. [F090](RAW_FACTS.md#f090)–[F092](RAW_FACTS.md#f092).

**CODE:** `Multidimensional-Smoking-Detection`, commit `9e70e3fe7816a305187621c4443953842d1e3f7e`, processes every third frame: YOLO cigarette/mouth width 640 + MediaPipe Hands on original, maximum 2 hands, distance 90 px, history 20 processed observations, threshold 8 hand-near-mouth. Global history, first mouth/cigarette `[0]`, no person tracks/ownership. Thus history ≈60 source frames, not 20; wall time depends on FPS. Scores cigarette .5/coexistence 1/joint proximity 2.5/history 1, smoking≥2 can combine current object+mouth with history without current hand-cigarette relation. This is static inspection without runtime or paired validation; do not copy `No Smoking` on missing cues. [F093](RAW_FACTS.md#f093).

**DOC/PUB-MEAS limits:** Earlier smoking clip work uses 3D ResNet34; §2.3 says 16 frames, §2.4 32 frames at 112×112. 70 smoking videos/HMDB51 negatives, 80/20 split and comparison on 20 clips, but inconsistent negative accounting and no industrial event denominator. It supports testing sequences/hard negatives, not production FA. TP-LINK 5–10 m smoking distance uses AI plus temperature detection; it is not an RGB or nearIR distance guarantee. [F051](RAW_FACTS.md#f051), [F053](RAW_FACTS.md#f053).

**PUB-MEAS fall:** Iazzi et al.: silhouette/SVM→floor overlap 85%→stand/sit transition <25 frames→inactivity 25 frames; authors' experimental gates. Table 11 reports 155/159 falls, 4 FP/136 nonfalls, but excludes short/occluded falls and uses one person; fast recovery not separately evaluated. Núñez-Marcos et al.: TV-L1 horizontal/vertical flow, VGG16 input `224×224×20` from 10 flow frames, step 1; overlapping-stack errors, not alarms/hour. Pre/postfall labelling mismatch accounts for 51.41% of analysed FP stacks; slow bending→lying 14.06%, with knees/quadruped/topview/distant blank-flow failures. These motivate endpoint/GT design, not expected industrial quality. [F095](RAW_FACTS.md#f095), [F096](RAW_FACTS.md#f096).

**PUB-MEAS hook:** Lim recognises worker/harness, misses small hook and leaves connection detection to future implementation. HDS fulltext does classify five hook states, preventing the overbroad conclusion that vision never addresses attachment. HDS: 3378 staged/internet photos→9738 after masking/flips→8:1:1; source-disjoint pre-augmentation split unspecified. mAP50 .912, `Not closed` AP .870, 24 FPS on TITAN XP at 640×640. No described physical truth protocol makes `Safe` equal valid load-bearing anchor/locked gate. [F054](RAW_FACTS.md#f054), [F094](RAW_FACTS.md#f094).

<a id="geometry"></a>
## Floor geometry, line crossing and metric proximity contract

**PROP:** Choose what intersects before drawing a polygon. Bottom center answers floor contact only when bbox bottom is the subject on that floor. `ankle-any` and ankle mean answer different questions. Bbox overlap can trigger on a leaning upper body with feet outside; even any of four box corners is not exact intersection with a thin polygon through the box centre. Whole-person containment may require an explicitly defined box/mask. Hands over machinery, crane load volume and elevated work need another image/3D/context model. [DOC/CODE F027](RAW_FACTS.md#f027), [F036](RAW_FACTS.md#f036), [PROP F103](RAW_FACTS.md#f103).

Supervision `BOTTOM_CENTER` is default; any/all anchors and its current count do not establish entry history (`trigger` does not use tracker_id). DeepStream 9.2 requires tracker/history for direction/crossing, separates direction vector and line, and `extended=0/1` finite/extended line. These illustrate primitives; NVIDIA plugin portability to LinQ is not established. [F036](RAW_FACTS.md#f036)–[F038](RAW_FACTS.md#f038).

Boundary hysteresis is proposed: choose inner/outer bands from localisation error, preserve prior geometric state within band while recording boundary uncertainty. No universal 10 px/20 cm band was found. Crossing needs reliable side history, segment and direction for same actor. Large gap → unknown crossing time; linear interpolation is hypothetical; two outside points do not exclude a rapid traversal. E006/E008 test anchors and actual observation intervals. [F103](RAW_FACTS.md#f103).

Image ROI does not require homography. Metres/ground distance do: planar 3×3 homography has eight degrees of freedom. Proposed calibration uses at least four known noncollinear correspondences on the same floor, plus independent control points near/far/edges. Keep units, source resolution, distortion handling, `calibration_version`, validity region and residual error. Floor transform on head, bucket, lifted forks, ladder/platform adds an unproven plane. Perspective pixels cannot become metres with one global scale. [DOC F039](RAW_FACTS.md#f039), [PROP F103](RAW_FACTS.md#f103), [E007](OPEN_QUESTIONS.md#e007).

`scene_version` changes with pan/tilt/zoom/crop/rotation/camera/preset. Agreed resize permits coordinate scaling; perspective change requires restored calibration. Proposed scene health check compares stable scene points and marks geometry invalid until recovered. Tracker GMC does not validate a physical zone. AXIS requires recalibration on PTZ preset change; ≥15 s between guard-tour presets is a product recommendation, not general stabilisation time. [DOC F043](RAW_FACTS.md#f043), [PROP F103](RAW_FACTS.md#f103).

**PROP proximity ladder:** static image ROI → equipment-track image expansion → calibrated ground footprint/envelope → direction/speed/swept footprint → operational active/permission rule. Each adds inputs, not certainty by naming. Compare distance to contour, not centres. Body heading and velocity differ; TTC requires stable relative velocity, error and latency budget; stop/turn/height mismatch/large error → U. Monocular excavator paper assumes known camera height/azimuth, flat ground, distortion correction and machine geometry; nonplanar ground is future work. Frigate speed requires four measured ground-zone sides, stable visible bottom center and straight motion; AXIS speed filter read here uses secondary radar. None establishes our monocular speed/FA/hour. [F028](RAW_FACTS.md#f028), [F045](RAW_FACTS.md#f045), [F046](RAW_FACTS.md#f046), [F104](RAW_FACTS.md#f104).

<a id="camera"></a>
## Camera pixel units, versioned product envelopes and failure handling

**INF:** `Full HD` alone is insufficient. Record source stream, analytics frame, native crop and tensor resolution; target part width/height at each stage, mode, angle/visibility and actual observation cadence. Letterbox approximately `target_px_tensor = target_px_source × min(W_tensor/W_source, H_tensor/H_source)` before padding: geometry, not quality. Full 4K shrunk to same tensor adds no usable tensor detail unless ROI/input policy changes. Native decoded-frame crop can preserve existing detail; preview crop/upscale cannot create absent signal. [CODE F081](RAW_FACTS.md#f081), [INF F112](RAW_FACTS.md#f112).

The following are **DOC conditions of specific products**, not minima for our detector. Head 60×60 px, PPE 20 px high and person 96 px high are different measurements.

| Product/version | Explicit camera/target/time conditions | Transfer boundary |
|---|---|---|
| Macroscop 4.7; page Last updated 22.10.2026 | Neural modes ≥3 FPS, HD 1280×720, colour; head ≥60×60 px for respirator/glasses/shield/earmuffs; hand ≥40×40 px; vest ≥60×60 px; person ≥80 px high and ≥2% frame width/8% frame height; downward tilt ≤35°, face angle ≤60° for facial PPE. Gloves: visible hands, no objects/pocket, ≥10 s in frame. | Invisible face → respirator/glasses not determined. “Above HD does not increase object number/fineness” is its pipeline. One visible glove presence is not both-glove coverage. [F017](RAW_FACTS.md#f017), [F018](RAW_FACTS.md#f018), [manual](https://doc.macroscop.com/analytics/hard-hats/requirements.htm). |
| Bosch VCA 6.30 Releaseletter 16.10.2024 p.5; CPP14 excluding 3000/multi/corner/panoramic | Analytics 1280×720 or 1024×576 for 8MP cameras; vest ≥48 px **person height**, helmet ≥96 px person height; ≥200 lx; upright standing/walking, PPE facing camera, unoccluded, one-at-a-time recommended; detection/tracking 7.5 FPS; PPE attributes about once per 3 s/person. | Vest strips visible, white helmet not overexposed. Attribute cadence differs from camera FPS and LinQ throughput. [F048](RAW_FACTS.md#f048), [PDF](https://cdn.commerce.boschsecurity.com/public/documents/RL_VCA_Release_Note_enUS_88157155723.pdf). |
| Axxon Next 4.5.0–4.5.10 PPE VL; updated 29.05.2023 | Colour; typical tasks ≥13 FPS; visible ≥8 frames; PPE height on part: helmet/hood/gloves 20 px, vest 50 px; stable illumination, human visual discernibility, no compression/barriers/vibration/fisheye. | Source says “200 lux per square meter”: preserve the defective unit, do not create a norm. Next VL differs from One and is not arbitrary IR support. [F076](RAW_FACTS.md#f076), [F077](RAW_FACTS.md#f077), [S062](SOURCES.md#s062), [S063](SOURCES.md#s063). |
| Domination Analytics Service 1.17 §8.8; document date unknown | Horizontal installation; tilt ≤15°, height 2–4 m, face distance 3–8 m; ≥1920×1080, 2592×1944 recommended; **optimal** linear face size 100 px; ≥5 FPS; no wide-angle/fisheye; uniform light, auto white balance/other auto settings off; known smoking zones, single scenes/max 3 potential people, no crowd/constant unrelated motion. | 100 px is optimum, not universal minimum. IR conditional on equal quality, not thermal. Default sensitivity 50% is a setting, not accuracy; face orientations add load. Parsed section read; visual QA failed; 1.18 mirror same provenance. [F090](RAW_FACTS.md#f090), [S072](SOURCES.md#s072). |
| Macroscop 4.7 fall | ≥10 FPS, optimum HD/Full HD, colour/stable light, whole person ≥8% frame height, tilt to horizontal ≤35°, no mirror reflections. | It detects lying, not fall transition. [F049](RAW_FACTS.md#f049), [F050](RAW_FACTS.md#f050). |

**DOC boundary:** DORI 25/63/125/250 px/m means human detection/observation/recognition/identification in Axis's explanation of IEC 62676-4:2014. Software analytics has other definitions. Full standard was not read; no current 2026 PPE norm established. DORI plans view, not respirator/cigarette admission. [F060](RAW_FACTS.md#f060), [Axis April 2026](https://whitepapers.axis.com/en-us/pixel-density-based-on-iec-62676-4-2014).

**PROP compensation contract:** assess camera-region × mode × part/type × preprocessing × observation intervals, then admit or abstain. [F122](RAW_FACTS.md#f122), E003/E013.

| Symptom | Candidate corrective step | U/invalid boundary |
|---|---|---|
| Source detail lost at resize | bounded native part crop, allowed larger input or tiles | original crop still unreadable or unavailable |
| Exposure/denoise motion blur or ghosts | shorter exposure with light; evaluate gain/noise, moderate denoise | needed moving edges lost; old clear frame is not current |
| Codec blocks/ringing | less aggressive source compression/bitrate/quality | received source already lacks target detail |
| Actual monochrome nearIR | separate validated night data/model or light for colour mode | RGB colour rule unsupported or detail unreadable |
| Steam/dust/exhaust | viewpoint/light/cleaning; process-background exclusions only by agreed purpose; hard negatives | target hidden; masking smoke does not prove PPE |
| Top view/occlusion | another view/checkpoint; accept only visible helmet predicate | face/owner/floor contact still assumed |
| Camera movement/fisheye/dirty lens | restore optics/stability/calibration and scene validity | zone coordinates/parts invalid |

Axis XFQ1656 July 2026 describes visible+nearIR→monochrome and exposure/gain/compression tradeoffs. Real nearIR is neither grayscale daytime augmentation nor thermal. Bosch/Keenfinity blur/ghosting advice applies, but embedded analytics sees **pre-encoder** images; its compression independence does not transfer to decoded RTSP. Direct measured PPE error curves for dust/steam/topview were not obtained; no numerical compensation guarantee. [F078](RAW_FACTS.md#f078), [F079](RAW_FACTS.md#f079), [F122](RAW_FACTS.md#f122).

**PUB-MEAS/INF tiling:** SAHI overlaps tiles/merges, optionally full-image pass. Gains 6.8/5.1/5.3 AP50 percentage points are FCOS/VFNet/TOOD on VisDrone19 test-dev, SAHI+FI+25% overlap vs FI, not PPE/smoking. Frigate developer reports more FP when enlarging tiny regions, without denominator. For W×H source, w×h tile, strides s_w/s_h, approximate `K=(ceil(max(0,W−w)/s_w)+1)×(ceil(max(0,H−h)/s_h)+1)` forwards/frame plus optional fullframe; implementation edge handling matters. Bounded native crops of visible parts/candidates may cost less than full tiling. Cap per-track/candidate refresh and total budget; low confidence must not trigger endless crops. Evaluate border duplicate/miss, context/owner loss and p95 latency together. [F059](RAW_FACTS.md#f059), [F080](RAW_FACTS.md#f080), [F113](RAW_FACTS.md#f113), [E013](OPEN_QUESTIONS.md#e013).

<a id="tracking"></a>
## Track incarnation, source timestamps, freshness and best evidence

**PROP:** ByteTrack without ReID on CPU is a baseline for fixed camera/moderate occlusion; retain weak person detections for association, not automatically as reliable PPE attributes. OC-SORT is a second candidate for nonlinear motion/occlusion. Add ReID by event misses/duplicates/contaminated-attribute benefit and measured neural cost. A track ID is neither employee identity nor proof of visible state continuity. [F040](RAW_FACTS.md#f040)–[F042](RAW_FACTS.md#f042), [F105](RAW_FACTS.md#f105).

**CODE:** Read ByteTrack `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`: `frame_id` advances per update, `buffer_size=int(frame_rate/30*track_buffer)`, Kalman dt=1. Changing `frame_rate` changes buffer, not timestamp-aware motion. Irregular results need variable-dt transition/process covariance or fixed processing cadence with explicit missed steps; event time remains source-time. `max_age=30` at 3 vs 30 updates/s means different physical intervals. BoT-SORT `251985436d6712aaf682aaaf5f71edb4987224bd` gates appearance with both appearance and geometric proximity thresholds; ReID does not guarantee recovery over large gaps; GMC does not calibrate zones. [F040](RAW_FACTS.md#f040), [F042](RAW_FACTS.md#f042).

**PUB-MEAS:** Same MOT20-test detections, ByteTrack/OC-SORT: HOTA 61.3/62.1, MOTA 77.8/75.5, IDF1 75.2/75.9, IDs 1223/913, Frag 1460/1198. Better association and lower MOTA coexist. Low FPS/fast motion can still yield zero IoU; virtual ORU observations are not visible violation evidence. Compare actual events with identical cached detections in E008. [F041](RAW_FACTS.md#f041).

**PROP error handling:** fragmentation resets dwell or creates duplicate events; ID switch moves bare-head/coverage state to neighbour; false reactivation merges independent incidents; prediction-only retains track without new visual evidence. Per-part attributes need visibility, quality, source timestamp, age/expiry and provenance. Ambiguous reassociation freezes/expires rather than copies state by proximity. Track incarnation key includes camera/scene epoch and segment; event_id has separate lifecycle and may link segments only by explicit uncertain continuity policy. New ID is not automatically same person; repeated revision of event_id is not new notification. [F105](RAW_FACTS.md#f105), [F106](RAW_FACTS.md#f106).

Every observation needs source frame ID/PTS/timestamp, inference completion/receive time and `measured/reused/predicted` provenance; source timestamp alone is insufficient. Engine operates in source-time; capture→publication latency includes processing/transport separately. Check result order; late old frame must not rewind state arbitrarily. Configured FPS, average throughput and actual fresh-observation cadence differ; burst losses and regular samples with equal mean miss different short events. [F105](RAW_FACTS.md#f105), [Q007](OPEN_QUESTIONS.md#q007).

**PROP best evidence:** bounded recent window per head/face/left/right part, selected by quality/visibility independently of test GT. Max violation score over a long track can pick one FP; old worn frame can hide later removal. Do not combine incompatible moments into “all PPE worn.” Preserve last reliable value/time/age; U adds no positive observed duration and cannot establish observed clear. Calibrate pause/reset/expiry in E004/E009. Evaluate accepted error with decision coverage over **all required person-time**, recall including abstention and U reasons. Confidence-only vs size+visibility vs combined gate on held-out camera; near-total abstention can inflate precision without solving coverage. Selective-classification i.i.d./same-distribution guarantees do not automatically hold for correlated CCTV/another plant. [F015](RAW_FACTS.md#f015), [F121](RAW_FACTS.md#f121), [E005](OPEN_QUESTIONS.md#e005).

<a id="frigate-static"></a>
## Frigate v0.18.2 static time/provenance counterexample

**CODE, not runtime:** `cfa08c56b23d23280c3d0a218e5a43182c97445b` was pinned; all `zone_presence/zone_loitering` writes, caller, Norfair, init/reset/end/new ID and same-commit documentation were traced. Ordinary enabled person zone, filters passed, no speed, same ID, updates after constructor: stored presence P, loitering L, current C, entered E. [F085](RAW_FACTS.md#f085)–[F088](RAW_FACTS.md#f088), [S070](SOURCES.md#s070).

| Static branch/trace | Exact implication within those gates |
|---|---|
| score=P+1; in below inertia I stores P+1; out below I stores score−1 | out preserves prior P, not reset/decrement. Disabled/label mismatch also skips without resetting saved counters. |
| I=3,L0: `in,out,in,in` | after first three updates P=1,1,2; **no entry at `in,out,in`**. Fourth in enters with P remaining 2. `in,out,in,out,in` also reaches entry at third in. |
| I=1,fps5,L1s (threshold5) | two in→L2, out retains L2, three in reach C/E=Z with stored L4; later out clears current only, next in enters immediately under same gates. Dwell counts eligible updates across gap. |
| Prediction-only, last measured inside | ordinary anchor reads last measured `centroid.x/box.bottom`, not predicted estimate. While Norfair still returns ID, downstream update can advance counters on old inside geometry. Last measured outside + estimate inside does not itself enter. Lifetime unmeasured. |
| Stationary reuse | `update_frame_times`/stationary seed can assign current `frame_time` to reused box without new detector call. Timestamp equality is not fresh neural evidence. |
| Caller and loss | missing frame/full queue can omit packet; camera update has no general freshness gate for ordinary zone. New ID constructor has clean counters and no same-iteration update. Removed path sets end/callback without clearing zone fields; final cleanup deletes later. Disabled camera is not observed exit; resolution reset is separate. |

Same-commit docs say consecutive frames, so this is a scoped static DOC/CODE discrepancy with manual ledgers. Norfair lifetime, runtime cadence/queue and actual event effect were not measured; earlier deletion changes path. It is **not a reproduced runtime bug**, all-version defect, safety suitability finding or recommendation to use Frigate. E017 proposes narrow replay; E009 tests our independent engine. [Q015](OPEN_QUESTIONS.md#q015).

<a id="event-time"></a>
## Event lifecycle, temporal operators and declarative evidence

**PROP:** per `rule × subject × scene_version` (person/equipment pair for proximity): `clear → candidate → active → resolving → ended`; parallel `observation_state=observed / occluded / stale / signal_lost / scene_invalid`. Active can coexist with loss. Clear before confirmation is not proof of safety under U. Candidate stores first qualifying source time/evidence; active requires selected temporal predicate. Separate `observed_start` and `confirmed_at`; resolving uses its own visible clear/exit hysteresis. [F106](RAW_FACTS.md#f106).

Ended reason: `observed_exit`, `observed_compliance`, `rule_disabled`, `scene_invalid`, `track_lost_timeout`, `stream_lost`, `identity_ambiguous`. Only first two establish observed cessation. Short occlusion may preserve incident for investigation with `last_observed_at`/coverage updated, but U neither accumulates positive duration nor establishes continuity across the blind interval. Long gap technically ends with censored boundary; return is new event or `possibly_same_incident` by explicit policy. Track/process/violation lifecycles are separate. [DOC F029](RAW_FACTS.md#f029), [PROP F106](RAW_FACTS.md#f106).

| Operator | Required definition | Failure/tradeoff |
|---|---|---|
| Consecutive hits | N fresh valid T; explicit F/U reset/pause | N updates ≠ seconds |
| N/M | N positives among last M all samples or eligible samples, explicitly chosen | denominator/U matter; correlated persistent FP survives vote |
| Positive duration in W | sum bounded supported T-intervals in source-time window | maximum gap; old value cannot fill a long hole |
| Continuous observed duration | first→last T with gap≤G and discrete support specified | no proof of unsampled interval; low cadence widens uncertainty |
| Merge gap | link episodes under allowed identity continuity | may hide real exit/reentry |
| Notification cooldown | suppress repeated delivery for key, continue state/evidence | broad key may hide independent incident |

**PROP sweep for E009:** confirm `0/0.5/1/2 s`; exit `0/0.5/1 s`; gap `0 / one expected interval / two expected samples`; N/M `1/1, 2/3, 3/5` with explicit U/denominator. Select on calibration by shortest important episode/max delay; freeze before test. Cooldown initially off to reveal raw duplicates, then test per-event delivery and merging separately. Two-second confirmation may be unacceptable for immediate short entry. These are hypotheses, not product defaults/safety norms. [F106](RAW_FACTS.md#f106).

**DOC/CODE product parameter distinctions:** Frigate `inertia=3`, `loitering_time=0`, `speed_threshold=None`, `detect.fps=5`; computed `min_initialized=max(int(fps/2),2)`, `max_disappeared=fps*5`; 40 s alert/30 s detection cutoffs group review, not violation cooldown. Detection `min_score`, median history `threshold`, track init and safety confirmation are different gates. AXIS `timeShortLivedLimit` measures age visible in image, not zone dwell: old-visible person can alarm immediately on entering include area; `triggerDelay` occupancy is another primitive. Query `getConfigurationCapabilities` for actual supported ranges/combinations; do not copy ambiguous Time/Distance table names as API truth. [F030](RAW_FACTS.md#f030), [F031](RAW_FACTS.md#f031), [F034](RAW_FACTS.md#f034), [F035](RAW_FACTS.md#f035), [F045](RAW_FACTS.md#f045).

**PROP typed rules:** within 45 hours, use known predicates, explicit units, temporal operators, U policy and versions. Free text alone does not validate scene/safety semantics. Sources show class/ROI/direction/filter/capability primitives, not a universal scene-graph DSL. The following is **pseudoconfiguration**, not any LinQ/library API; E009 selects values, E010 accepts semantics. [F107](RAW_FACTS.md#f107).

```yaml
rule_id: helmet_required_Z1
rule_version: 1
camera_id: camera_01
scene_version: camera_01_preset_A_v1
subject: person_track_incarnation
semantics: required_helmet_coverage_missing_in_floor_zone
when:
  all:
    - requirement_active: {policy_id: approved_helmet_policy_v1}
    - inside_zone:
        zone_id: Z1
        anchor: bottom_center
        requires: ground_contact_observable
    - not:
        approved_coverage: {part: head, policy_id: approved_helmet_policy_v1}
logic: strong_kleene
temporal:
  operator: continuous_observed_duration
  confirm_seconds: SELECT_BY_E009
  max_observation_gap_seconds: SELECT_BY_MEASURED_CADENCE
on_unknown: freeze_incident_do_not_accumulate_positive_duration
end:
  observed_clear_confirmation_seconds: SELECT_BY_E009
  track_loss: end_with_censored_reason_after_selected_timeout
notifications:
  deduplicate_by: event_id
```

An optional `equipment_active` needs valid external source/TTL; absent feed → U or deliberately simplified/renamed rule, never substituted false. Unknown role does not disable requirement. Rule threshold change and camera movement have different versions; active event retains old rule version or explicitly ends/recreates. [F104](RAW_FACTS.md#f104), [F107](RAW_FACTS.md#f107).

**PROP observation fields:** `camera_id`, `scene_version`, `source_timestamp`, `source_frame_id`, `inference_received_at` and completion, `model_version`, `track_id`, `track_segment_id`/incarnation, bbox, anchor/method, geometry validity, visibility/quality, predicates `{name,value:true|false|unknown,score,provenance}`, `fresh_measurement` and measured/reused/predicted. Pair rules add equipment track and activation/geometry sources. Score does not replace T/F/U/visibility. [F086](RAW_FACTS.md#f086), [F107](RAW_FACTS.md#f107).

| Proposed event field group | Purpose |
|---|---|
| `event_id`, `revision`, `rule_id/version`, `scene_version`, `model_version` | reproduce decision and deduplicate delivery |
| camera, involved track segments, actor/equipment association status | avoid treating tracker ID as real person identity |
| `observed_start`, `confirmed_at`, `last_observed_at`, `observed_end`, `published_at` | distinguish observation, decision, end and delivery latency |
| status, observation_state, end_reason, duration_lower_bound, censored | distinguish observed clear from technical loss; do not invent duration |
| zone/anchor/calibration version, metric units/error | disclose measured geometry |
| evidence frame IDs/time, fullframe, part crop, pre/post clip | verify detail, owner, scene and temporal evidence |
| contributing observations, visibility/decision coverage, temporal settings | expose gaps hidden by one good image |
| delivery IDs/revisions, merged_from, possible related events | explain merging/repeated messages |

Best snapshot aids review but cannot prove 12 seconds. Keep fullframe for context/owner/zone, crop for detail, clip beginning before confirmation. One detection score is not calibrated probability of a whole event. → operator_product. [F107](RAW_FACTS.md#f107).

<a id="linq"></a>
## Neural workload, exact LinQ artifact and INT8 quality gates

**INF requirements matrix, not supported-ops list.** Let f=analysed frames/s, P=people, r=per-person crop refresh/s, h=selected head/hand regions, K=tiles/frame, c=candidate events/s, v=frames/verifier call. Batch can reduce submissions, not computation of distinct P crops; low f alone does not cap crowd workload. [F116](RAW_FACTS.md#f116).

| Method | Neural inputs/computation | CPU after networks | Artifact/platform question |
|---|---|---|---|
| Multiclass fullframe detector | f forwards/s | decode/NMS at chosen boundary, ownership, tracker, rules | shapes/opset, bbox/class/DFL heads, postprocess boundary |
| Person→attributes | f + P×r images/s | crop selection/association/aggregation | detector+classifier, batching/queue/staleness bound |
| Person→head→small PPE | f + P×r_head + h×r_ppe | coordinate/time/owner mapping | 2–3 graphs/heads; early miss breaks chain |
| Bottom-up pose | f pose inputs/s | skeleton/relations | coords/confidence or heatmap layout/stride/argmax |
| Top-down pose | f + P×r_pose | track/keypoint matching | per-person graph/occluded-joint handling |
| ReID | extra crop embeddings by track policy | appearance/geometric association | exact graph/refresh and separate neural budget |
| Tiles/SAHI | K×f plus optional f | merge/NMS/reprojection | repeated detector/memory/queues/context |
| Clip/temporal action | per-person sliding clips at declared stride | timestamped buffer/event state | temporal shape, 3D conv/pool or attention/RNN |
| Fixed-vocabulary OVD | f image forwards; text prepared offline | class mapping/ownership/rules | prepared head/neck/embeddings and exported graph |
| Dynamic OVD | image+text dependent | prompt preparation/rules | tokenizer/text encoder, attention/matmul/LN/Softmax, multiple inputs/shapes |
| VLM verifier | c calls/s, v frames/call + token generation | candidate gating/parser/evidence | encoder/projector, generation/KV cache/lengths and authorised execution |

ROI/homography, assignment, tracker without ReID, state machine, rules and notification cooldown need no neural inference. ReID embeddings, pose and classifiers do. CPU postprocessing alone does not establish compliance for auxiliary networks; CPU decode/NMS and external verification boundaries require Q005. [F116](RAW_FACTS.md#f116), [Q005](OPEN_QUESTIONS.md#q005).

**VENDOR/UNK:** LinQ tech lists int8/CNN/RNN and `yolo5s/yolo8/yolo11`, without exact checkpoint/shape/opset/postprocess/SDK. HPS advertises PyTorch through ONNX, LinQ Compiler/DNN Quant; fp16/bfloat16 are prospective. HPS is one line, not the assigned hackathon accelerator. Family/“full ONNX”/throughput claims do not establish our pose/seg/OVD artifact or RPC latency. [F063](RAW_FACTS.md#f063), [F064](RAW_FACTS.md#f064), [LinQ tech](https://lin-q.ru/tech), [Q006](OPEN_QUESTIONS.md#q006).

**PROP four sequential gates:** (1) export matches reference → (2) graph compiles with known fallback → (3) actual execution on assigned LinQ proved → (4) outputs/detection/track/event quality retained. Compilation ≠ execution; execution ≠ quality; one checkpoint ≠ family/cascade support. Obtain device/SDK/access/proof method at P0. **No gate was executed here.** [F117](RAW_FACTS.md#f117), [E015](OPEN_QUESTIONS.md#e015).

**INF INT8:** representative calibration/test slices: small head/cigarette, respirator on neck/hand, blur/backlight/real IR, crowd association and keypoint displacement. Confidence/coordinate drift can change NMS, track birth/death and N/M events despite small average mAP change. Heatmap coordinate discretisation differs from arithmetic INT8. Do not declare pose/attention/3D unsupported without exact ops evidence or promise QAT/mixed precision/float heads before SDK confirmation. [F118](RAW_FACTS.md#f118), [Q020](OPEN_QUESTIONS.md#q020).

**PUB-MEAS scoped examples:** PTQ4ViT discusses uneven post-softmax and asymmetric GELU; uniform PTQ may drop >1% accuracy even at 8 bit, specialised twin-uniform gives <0.5% ImageNet ViT/DeiT/Swin drop. It is not a LinQ implementation. NVIDIA PeopleNet ResNet18 mAP FP32 78.37→PTQ 59.06→QAT 78.06; ResNet34 80.2→62→79.57 with spurious TensorRT-PTQ boxes. This is DetectNet/PeopleNet/calibrator-specific, not predicted YOLO/PPE loss. Preserve paired raw outputs and new false events rather than transferring these percentages. [F061](RAW_FACTS.md#f061), [F062](RAW_FACTS.md#f062).

<a id="ovd-vlm"></a>
## Fixed OVD vocabulary, dynamic text and paired VLM verification

**DOC/INF OVD:** Short known vocabulary can be prepared offline. YOLO-World developer documentation includes text embeddings in parameters: final classification 1×1 convolution instead of transpose/matmul, `YOLOWorldHeadModule`, `MaxSigmoidCSPLayerWithTwoConv`, NxD embeddings. YOLOE RepRTA reparameterises auxiliary text network into classification head; SAVPE visual prompts/LRPC prompt-free are different mechanisms. New vocabulary needs new prepared artifact, possibly recompilation (LinQ inference, not confirmed API). Preserve class order, embeddings/head dimensions and preprocessing. Do not infer all graph attention is removed from one reparameterised classification head. [F055](RAW_FACTS.md#f055), [F056](RAW_FACTS.md#f056), [F114](RAW_FACTS.md#f114).

Grounding DINO has text-image fusion, language-guided queries and self/cross-attention decoder: dynamic prompt graph/input workload differs. LinQ feasibility unknown, not disproved. `helmet` box does not state wearer/on-head/approved/condition. Test “worker without respirator” on hidden face, neck/spare and tiny head; absent box never establishes negative. Useful proposed OVD roles: candidate search, annotation assistance and new-camera inspection, followed by E001/E003/E015. [F057](RAW_FACTS.md#f057), [F114](RAW_FACTS.md#f114).

**PROP VLM:** Detector+rules stays an independent baseline. Optional reject-only verifier receives native crop plus sufficient context/short clip and a narrow observable predicate, enum `supported / contradicted / not_visible`; save model/revision/prompt/settings/selected frames/raw answer/schema-parser status/time. Generic “is there a violation?” mixes policy with image. Timeout/decode/schema failure → unverified, never negative. Multi-frame input does not guarantee temporal reasoning; lost source detail, container contents and invisible gate remain U. Reject-only cannot recover upstream missed candidates. [F115](RAW_FACTS.md#f115), [F125](RAW_FACTS.md#f125).

| Direct evidence | What it establishes | Missing for our suppressor |
|---|---|---|
| NVIDIA VSS 3.3.0 developer workflow | detector/tracking/behaviour→sporadic candidate clip verification; short-clip/model failures; remote timeout default 5 s; semantically `rejected` may fail raw A/B or Yes/No schema and remain verification-failed | independent paired rescue/loss benefit; our exact chain/device latency. [DOC F099](RAW_FACTS.md#f099), [workflow](https://docs.nvidia.com/vss/vision-agent/agent-workflows/alert-verification). |
| Guo et al., 25.08.2026 | abstract-only industrial recheck: 1068 on-site alarm images, 3 domestic VLM, terminal volume −33.6%, false-alarm share 31.9→12.5% | exact models/prompts/split, TP losses, hardware/latency/event denominator; not our KPI. [VENDOR F098](RAW_FACTS.md#f098), [S080](SOURCES.md#s080). |
| Kim et al., PMLR 296/2025 fulltext | each-frame Florence2large fp16, positive VLM lowers YOLO threshold .5→.3 plus VLM-validated alarm. 1081 mixed real/synthetic images; YOLOv8s fire precision .843→.838, smoke .944→.931; recall .835→.904/.833→.885. Table C.1 .28 s/2.3 GB; deployment 4 FPS, RTSP/upload overhead 1.6× offline. | Different objective: recall gain with precision loss, not reject-only FA reduction. Checkpoint revision/evaluation GPU unknown, no claimed camera-heldout or required paired event table. [PUB-MEAS F097](RAW_FACTS.md#f097), [paper](https://proceedings.mlr.press/v296/kim25a.html). |

POPE supports hallucination risk for studied 2023 LVLM, not measured benefit/harm of a current chosen verifier. Direct cascade traces exist; neither automatic FA reduction nor universal uselessness follows. E014 freezes baseline candidates and measures TP→accepted/rejected/unverified, FP→accepted/rejected/unverified; FP-rescue denominator baseline FP, TP-loss denominator baseline TP. Fix failure policy before downstream P/R/FAh/coverage/latency. Reject suppression if TP loss or delay unacceptable; secondary review or no VLM remains valid. Changing candidate thresholds/objective requires new comparison. Execution path still Q005/Q006. [F058](RAW_FACTS.md#f058), [F125](RAW_FACTS.md#f125), [Q019](OPEN_QUESTIONS.md#q019).

<a id="evaluation"></a>
## Actor-aware event matching, denominators and acceptance evidence

**PROP:** Object AP/crop accuracy diagnoses components; operator receives an actor-specific rule event. Before measurement, define GT `(camera, rule semantics, GT actor/relations, onset, offset, observed/unknown intervals, scene_version)`, independent of tracker ID. Onset can mean crossing, first visible uncovered state or allowed dwell expiry; fix it before latency comparison. [F107](RAW_FACTS.md#f107), [Q008](OPEN_QUESTIONS.md#q008).

State intervals: predeclared temporal overlap/tIoU. Point crossing: onset collar and direction. Match actor-aware **one-to-one** among compatible camera/rule/zone/time: neighbour is not TP; extra predictions for one GT are duplicate FP; unmatched GT FN. Report split/merge errors separately. Set thresholds by task/annotation precision before test; separate sensitivity analysis, no choosing best test threshold. DCASE onset 200 ms/offset max(200 ms,20% duration) is an **audio-protocol example**, not CCTV norm. [DOC F047](RAW_FACTS.md#f047), [PROP F107](RAW_FACTS.md#f107), [E010](OPEN_QUESTIONS.md#e010).

Required proposed reporting: event precision/recall/F1 with GT/TP/FP/FN counts; false alerts per **observed violation-free camera-hour**, hours and availability vs scheduled time; duplicates/active-time fragmentation/shortest-important-event misses; observable-onset→confirmation and live capture→publication p50/p95/max separately; accepted decision coverage over all required person-time, U reasons and recall including abstention; false coverage from held/neighbour/spare PPE; wrong actor and censored end reasons. A short balanced clip set or zero FP there is not shift-level FA/hour evidence. Offline end-of-clip/stream-loss active intervals are right-censored; do not invent offset. Camera downtime cannot improve apparent quality: include both observed and scheduled denominators/availability. Smoking/VLM comparisons are paired; INT8 compares event consequences with identical preprocessing. [F107](RAW_FACTS.md#f107), E010/E011/E014/E015.

**DOC procurement, not achieved accuracy:** Oil India Limited `GEM/2026/B/7902194`, dated 11.08.2026, PPE and Unsafe Act Detection using Video Analytics. Official NIT and Minutes of Pre-Bid Meeting 25.08.2026, published 01.10.2026, obtained. Quoted SoW §7.13 demands 90% ideal/80% challenging; customer says per-use-case assessment, methodology at Design with OIL approval. A question cites conflicting 95% vs 90/80%; no new formula resolves denominator/FP/FN/matching. SAT/signoff planned, criteria before UAT/SAT; full SoW `1786430899.pdf`, signed SAT and achieved performance not obtained. Not an accuracy/SLA result. [F082](RAW_FACTS.md#f082), [F083](RAW_FACTS.md#f083), [S068](SOURCES.md#s068), [S069](SOURCES.md#s069), [Q016](OPEN_QUESTIONS.md#q016).

Oil India small PPE on legacy wide cameras → joint survey/remediation report and OIL upgrades; zones fixed positions/approved stable PTZ; steam/dust/exhaust/flares camera-wise exclusions/calibration. Bidder's objection to 80% outside IR range was not accepted as a physical guarantee. No PPE degradation curves or FA/hour SLA found. Russian “Видеоконтроллер” grant design ToR demands helmet **on head** ≥95%, glasses **on face** ≥98%, shield/mask **on face** ≥98%, gloves **on hands** ≥90%, 1–50 zones/frame. “Reliability” denominator insufficient; test programme to be developed, no achieved acceptance and not established industrial procurement. It supports relational semantics, not attainable percentages. [F025](RAW_FACTS.md#f025), [F084](RAW_FACTS.md#f084).

**UNK evidence access limits:** RegistryKeys/VMDA target tables not read (`VMDA.oneAlarmPerTrack`, `LongInZoneTimeout2`, `report_frequency` remain leads; snippet 1/10 s/3000 ms are not accepted defaults). Pictor full A1 downstream/full paper, CHV full paper, N95 PPE-CLS/FMR-DB full bodies and predecessor gas-mask restricted body not obtained. No complete SH17 archive audit/industrial neck-hand-removal artifact. Guo abstract-only; Domination parsed section without visual QA; OIL full SoW/SAT missing; ACM smoking fusion body inaccessible. Failed access is not proof of nonexistence. [SOURCES access register](SOURCES.md), [Q010](OPEN_QUESTIONS.md#q010), [Q011](OPEN_QUESTIONS.md#q011), [Q016](OPEN_QUESTIONS.md#q016), [Q017](OPEN_QUESTIONS.md#q017).

<a id="experiments"></a>
## E001–E017 actionable practical programme — all PROP, none executed

Thresholds/gates are calibrated on separate clips/cameras, then frozen before test. Shared clips/GT across E are one evidence source, not independent replications. Save source-time, actor links, versions, U/availability and denominators. No unknown-SDK command is invented. Suggested order: E001/E003/E013 admission; E010 rule/evaluator agreement and simple chain; E002 ownership, E004/E008/E009 time/tracks, selected E011/E016 and exact LinQ E015; E005 selective tradeoff; E006/E007 geometry; optional E012/E014. E017 is a narrow external replay, not MVP dependency. Do not postpone first available exact-artifact LinQ test until all other experiments finish. Full cards and Q/K links: [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md#e001).

### E001 — Annotation semantic acceptance

- **id:** [E001](OPEN_QUESTIONS.md#e001), Q001/Q010/Q011.
- **decision:** state/coverage/removal GT accepted, remapped/relabelled/ignored, or positive-object-only.
- **inputs:** actual archive/guide/YAML/revision; approved policy; two annotators; stratified tiny/partial/back/on-face/neck/hand/spare/occluded/head-out-of-frame examples.
- **steps:** hash/unit→actual IDs vs YAML→wearer/track/time/relation/on-off fields→separate item relation, coverage, visibility, requirement, zone, rule labels→adjudicate omission vs visible negative. Repeat spare+worn and hidden-head counterexamples; no forced-negative ambiguity.
- **measurements:** wrong-unit fraction, taxonomy conflicts, U wrongly negative, disagreements/ambiguity and field presence.
- **evidence:** actual sample annotations/crops, mapping, guide locator, hash and adjudication/decision log.
- **outcomes_limits:** state artifact→model; object-only→own coverage/relations labels; contradictions→relabel/ignore/exclude. Does not establish licence, transfer, weights or LinQ. Existing two SH17/R2PPE inspections are not completed E001.

### E002 — Ownership on identical detections

- **id:** [E002](OPEN_QUESTIONS.md#e002), Q012.
- **decision:** geometry enough or pose/HOI worth extra cost.
- **inputs:** GT person/head/PPE boxes and owner/part links; isolation/crowd crossing/bends/held/table/spare/donning; pose output; calibration/separate test scene.
- **steps:** oracle boxes compare containment/normalised distance, one-to-one head matching and pose anchors; then same actual detector for all variants. Invisible joint is not observed. HOI only with relation data/export path.
- **measurements:** owner accuracy with resolved-link denominator, ambiguity/U, false coverage held/neighbour, missed violations, size/pose errors, calls/crops/latency per person.
- **evidence:** immutable detections/GT, assignment/version/threshold traces, overlays, paired errors/timing.
- **outcomes_limits:** cheapest method meeting event goal; pose only with demonstrated benefit/budget, ambiguous→U. Oracle success is not chain quality; staged crowd is not deployment crowd.

### E003 — Per-PPE observability and empirical admission

- **id:** [E003](OPEN_QUESTIONS.md#e003), Q001/Q004.
- **decision:** admitted camera-region/part/type, crop/view/checkpoint or omitted predicate.
- **inputs:** native target clips/approved PPE/GT, real distances/angles/day/IR/occlusion and source/tensor target sizes; synthetic degradation separate.
- **steps:** two annotators mark visible positive/negative/unobservable; identical GT compares fullframe/native part crop, head-state/local face-hand classifier; helmet/industrial respirator/protective vs corrective glasses/left-right gloves separately. Include neck/hand/spare/visor/unsupported types; calibration gate then held-out camera.
- **measurements:** state confusion, violation P/R, false coverage, U/person-time by size/angle/condition, input counts.
- **evidence:** source/crop pairs, visibility/U GT, metadata, frozen gate and slice tables.
- **outcomes_limits:** human-unreadable part/type/owner stops inference→U/new view. Valid size bin is not universal physical threshold/fit-seal proof; downsample does not replace real distance. E013 measures preprocessing/workload on possibly shared data.

### E004 — U and best-evidence ageing

- **id:** [E004](OPEN_QUESTIONS.md#e004), Q002/Q013.
- **decision:** per-part recent window, pause/reset/expiry and stale limit.
- **inputs:** timestamped wear→remove→hold→occlude→rewear, already-uncovered, all-U/negative, spare/duplicate and reassociation clips with C/visibility GT.
- **steps:** per-frame vs recent eligible aggregation/quality-selected evidence and U policies; selection independent of test GT; per-part age and temporal compatibility; correct/ambiguous reassociation separate.
- **measurements:** event P/R/FA per negative camera-hour, onset delay, false observed clear in occlusion, stale age, decision coverage and evidence readability.
- **evidence:** predicate/selection timelines, timed crops, visibility intervals, end reasons/settings.
- **outcomes_limits:** reject U-as-observed-clear or stale wearing hiding removal; choose declared coverage/recall tradeoff. Synthetic trace success fixes neither detector nor domain transfer; lifecycle E009.

### E005 — Selective prediction under camera/domain shift

- **id:** [E005](OPEN_QUESTIONS.md#e005), Q013.
- **decision:** whether/how to abstain profitably.
- **inputs:** calibration and unseen camera/shift, T/F/U GT including unsupported types/long occlusion.
- **steps:** same inputs ungated/confidence-only/visibility+size/combined; freeze gates before test; separate OOD and signal loss; retain all required person-time denominator.
- **measurements:** risk–coverage, accepted error, event FA, recall including abstention, U reasons/calibration error/extra neural calls.
- **evidence:** splits/gates, full-denominator tables/curves, accepted/rejected mistakes.
- **outcomes_limits:** use only useful measured tradeoff; near-total abstention requires revised model/scope. I.i.d. theory does not guarantee correlated CCTV or new-plant performance.

### E006 — Floor anchor, boundary and crossing

- **id:** [E006](OPEN_QUESTIONS.md#e006), Q003/Q004.
- **decision:** bottom center, visible ankles, different view or different zone semantics.
- **inputs:** fixed/versioned scene, agreed polygon/meaning, walk/bend/one-foot/hidden-feet/crowd clips, contact/U GT.
- **steps:** frozen detections compare bbox intersection/bottom center/ankle-any/mean, preserving “one foot”; then real detector errors. Calibrate boundary band; finite direction crossing, first-inside track, resize vs scene shift invalidation.
- **measurements:** false/missed entry, boundary error, delay, U coverage, CPU/neural calls.
- **evidence:** anchor/polygon/GT overlays, source-time predicate traces and scene/config.
- **outcomes_limits:** simplest admitted anchor+hysteresis; invisible contact/invalid scene→U; pose by gain. Does not prove 3D/hand-in-mechanism/another camera.

### E007 — Metric proximity and moving envelope

- **id:** [E007](OPEN_QUESTIONS.md#e007), Q003/Q004/Q014.
- **decision:** metres/speed valid or image-zone only.
- **inputs:** floor correspondences/dimensions/control marks, independent distance/time reference, safe recorded trajectories, footprint/heading/working organ.
- **steps:** independent near/far/edge calibration controls; contour vs centre distance; turns/occlusion/raised forks/other height; perturb camera/calibration; source-time velocity, heading separate from motion. No dangerous real approaches.
- **measurements:** distance p50/p95/max error, threshold FP/FN, speed error, missed envelopes, U/delay.
- **evidence:** matrix/version/units/distortion/residuals, independent reference, overlays/trajectories/outside-validity cases.
- **outcomes_limits:** metric claim only in validated region with error margin; otherwise image ROI and metric/3D U. Not stopping-distance certification/collision prevention/TTC guarantee.

### E008 — Tracker at actual cadence and loss patterns

- **id:** [E008](OPEN_QUESTIONS.md#e008), Q007/Q012.
- **decision:** ByteTrack/OC-SORT/BoT-SORT and ReID necessity.
- **inputs:** identical cached detections including weak scores, GT actors/events/source times, exact commits/config/ReID artifact, measured LinQ cadence when available.
- **steps:** each tracker same detections; ReID separate on/off; full rate, uniform **stress** 10/5/2 FPS, burst losses/jitter with same mean, reconnect/crossings. Buffers in updates and physical time; tune calibration only, frame_rate is not variable dt.
- **measurements:** IDS/Frag/IDF1/HOTA plus event F1/misses/duplicates/wrong transferred PPE, CPU/latency/ReID inputs.
- **evidence:** detection cache, sampling schedules, track/event ledgers, switch clips and timing/budget.
- **outcomes_limits:** cheapest event-adequate tracker, ReID by benefit; ambiguous identity never confidently transfers coverage. Cache replay is not end-to-end LinQ/network measurement.

### E009 — Confirmation, clear, loss, deduplication and cooldown

- **id:** [E009](OPEN_QUESTIONS.md#e009), Q007/Q008/Q013.
- **decision:** time operator/entry/exit/gap, technical end, merge and delivery policy.
- **inputs:** deterministic predicate traces plus positive/long-negative clips: brief FP/real short entry/boundary jitter/exit-return/stationary/occlusion/ID switch/scene shift/stream reconnect/out-of-order.
- **steps:** manual expected-state trace replay without inference then video chain. Compare consecutive, explicit-denominator/U N/M, supported positive duration and continuous observed duration/max gap. Sweep confirm 0/0.5/1/2 s, exit 0/0.5/1 s, gap 0/one interval/two samples, N/M 1/1,2/3,3/5. Cooldown off first; delivery suppression and merging separate; incarnation is not automatic identity.
- **measurements:** FP/FN/duplicates, short-event misses, confirmation/publication delay, U/censored reasons, physical-time resampling invariance, event-ID/revision stability.
- **evidence:** versioned config/source-time/expected-vs-actual ledgers, observed_start/confirmed_at/end_reason, crops/clips.
- **outcomes_limits:** reject stale confirmation or loss-as-clear; select by minimum important episode/max delay. Correct automaton cannot fix detector/zone semantics; E017 is separate external replay.

### E010 — Typed rule and event evaluator acceptance

- **id:** [E010](OPEN_QUESTIONS.md#e010), Q001/Q003/Q008/Q014.
- **decision:** full-case rule/measurement contract unambiguous and evaluator correct.
- **inputs:** full case/expert policy/schema and handmade GT/predictions: wrong actor/two overlapping people/split/merge/duplicates/crossing/interval/censored boundary.
- **steps:** expert fixes endpoints/applicability; Strong Kleene and five F100 counterexamples, units/versions/TTL/missing inputs; independently hand-match actor-aware one-to-one and compare evaluator. Point collar separate from interval tIoU; thresholds before test. Extra predictions FP/unmatched GT FN.
- **measurements:** ambiguity, invalid rules accepted, manual/evaluator divergence, wrong-actor/duplicate FP, GT/event/negative-hour counts/availability; live vs offline delay separate.
- **evidence:** agreed/signed semantic examples/GT contract, hand matching table and denominator specification.
- **outcomes_limits:** disputed rule disabled/U pending answer, evaluator fixed before CV scoring. Contract/accounting success is not recognition; DCASE 200 ms not borrowed as norm.

### E011 — Paired RGB smoking route selection

- **id:** [E011](OPEN_QUESTIONS.md#e011), Q004/Q008/Q009, K002.
- **decision:** object/face A vs gesture/object+time B and candidate/confirmed boundary.
- **inputs:** native video/PTS/camera ID, actor/action/visibility GT and supplied hazard; people/clip calibration-test split plus held-out view/camera; sample volume by precision of estimate/negative coverage, no universal N.
- **steps:** same pool/owner/event logic compares object-only, gesture-only, fusion. Include all VM10 negatives plus one cue without other. Timestamp processed windows explicitly; raw cue vs S AND H separate; human-unobservable→U.
- **measurements:** paired TP retained/lost, FP removed/added, event P/R/F1, FP/negative camera-hour, first-alert delay, U/coverage, negative-category errors, source/tensor sizes, calls/s and total p50/p95.
- **evidence:** immutable pool/GT/split, exact model/config, raw detection/pose/relation/time traces, paired table/clips/timing.
- **outcomes_limits:** unreadable human cue→stop/checkpoint; B without budgeted event benefit→A+U. Balanced clips not negative hours; RGB success not new camera/nightIR/LinQ/container-content proof.

### E012 — Case-added fall/hook endpoints

- **id:** [E012](OPEN_QUESTIONS.md#e012), Q018, K007.
- **decision:** posture/transition/immobility and precise observable hook predicate.
- **inputs:** safely staged slow/fast deliberate lying, kneel/slide/quadruped/maintenance, fall-like transition+fast recovery/immobility, occlusion/lost history; hook rig same-geometry attached/unattached/open/hidden pairs, expert physical GT/anchor map and native target crop.
- **steps:** separate endpoint timelines, keep short/occluded cases in U/coverage; temporal vs posture baseline; fast recovery does not cancel transition. Human hook admission then class contract; presence/visible open gate distinct from mechanical locking/strength.
- **measurements:** transition recall/delay/intentional-lying confusion, short/fast-recovery misses; hook class P/R/confusion/U size-angle and false attachment from proximity.
- **evidence:** before/during/after, separate GT, physical inspection/rig photos, camera/size/config/U reasons.
- **outcomes_limits:** posture only→`person_lying`; temporal evidence→`suspected_fall_transition`; harness only→presence; hidden gate→U. Not medical/intent/trauma diagnosis, load certification or mandatory announcement scope.

### E013 — Camera/preprocessing and bounded crop/tile budget

- **id:** [E013](OPEN_QUESTIONS.md#e013), Q004/Q007, K004.
- **decision:** admitted region/mode and fullframe/native crops/tiles within budget.
- **inputs:** native streams/scene/ROI versions, actual colour day/nightIR, exposure/gain/codec/bitrate/QP if available, exact preprocessing/source times and paired clear/degraded target visibility/action GT.
- **steps:** source→analytics→native crop→tensor target extents/letterbox; same candidates compare fullframe/bounded part-person crops/tiles+optional fullframe with fixed merge/NMS. One factor at a time, real vs synthetic separate; moving/static PPE/topview/occlusion/steam/dust/process background. Record refresh/batch/queue and bounded evidence age.
- **measurements:** paired state/event P/R/FA per negative hour, U/coverage per predicate, border/context duplicate/miss, forwards/s/P×refresh and p50/p95 latency.
- **evidence:** source/crop/tensor examples/metadata, frozen split/preprocess, per-condition errors, load logs/admitted list.
- **outcomes_limits:** native crop only if detail and budget retained; otherwise stream/light/view/checkpoint/omit predicate. Upscale/day-grayscale is not real IR/dust/distance proof; pre-encoder Bosch claim not RTSP. E003 is distinct per-PPE admission on potentially shared data.

### E014 — Reject-only VLM: FP rescue versus TP loss

- **id:** [E014](OPEN_QUESTIONS.md#e014), Q005/Q006/Q019, K008.
- **decision:** suppressor, secondary review or no verifier.
- **inputs:** frozen detector+rules/candidate events/GT including baseline TP/FP; original context/crop/clip, camera/clip calibration-test splits, authorised execution, exact model/revision/prompt/settings/parser/schema and timing.
- **steps:** retain event ID/selected frames/input/prompt/raw answer/verdict/parser status/time for every candidate. Tune calibration only; owner ambiguity/tiny PPE/allowed lying/reflections/screens/steam/unknown view and timeout/decode/schema failures; repeat identical inputs for stability. `supported/contradicted/not_visible`; execution failure separate unverified.
- **measurements:** TP→accepted/rejected/unverified; FP→accepted/rejected/unverified; FP-rescue over baseline FP, TP-loss over baseline TP. Fix failure policy then event P/R/FAh/coverage/total p50/p95/calls/event/memory; upstream misses separate.
- **evidence:** immutable baseline/pool/split/GT, all raw requests/responses/context/revisions/parser outcomes, paired errors/timing.
- **outcomes_limits:** unacceptable TP loss/delay→no suppression; secondary uncertainty review possible. Changed candidate threshold/objective requires new test (Kim .5→.3 differs). Success not full-stream recall or whole-chain LinQ execution; VLM existence does not imply FA↓.

### E015 — Exact LinQ export/compile/execute/quality

- **id:** [E015](OPEN_QUESTIONS.md#e015), Q005/Q006/Q007/Q020.
- **decision:** exact promised graph/precision/device/scope.
- **inputs:** assigned hardware/SDK/compiler/runtime/opset/account/proof method; hashes of checkpoint/graph/classes/pre-postprocessing; float reference outputs; representative calibration/test slices.
- **steps:** export/reference correctness→actual ops/shapes/heads/decode inspection→compile report/fallback→actual LinQ execution proof→same frames raw tensors/detections/tracks/events vs reference. Include small cigarette/head, neck/hand, backlight/IR/blur/crowd, keypoint/NMS drift. QAT/mixed precision only if supported; device inference vs RPC/queue/crop throughput separate.
- **measurements:** gates/pass/fallback, tensor drift, APsmall/coordinate error, false coverage/event recall/FAh, calls, availability and p95 capture→publish.
- **evidence:** hashes/version/calibration manifest, compile and execution logs/proof, paired raw outputs/event ledgers/timing.
- **outcomes_limits:** compile failure→change graph; quality failure→available calibration/precision/model/scope route. One checkpoint not family/cascade support; offline run not online SLA; PeopleNet/ViT percentages not forecast. All gates unexecuted here; no invented SDK API.

### E016 — Respirator state, coverage-loss and item-doffing on same clips

- **id:** [E016](OPEN_QUESTIONS.md#e016), Q001/Q002/Q011, K003.
- **decision:** visible-uncovered A, coverage-loss, strict item-doffing or limited demo.
- **inputs:** native target-type/source times; separate C(t), D_item(t), visibility/approved policy/R/Z GT; removal-neck/hand-rewear, already-uncovered, hidden/gaps/spare/swap/duplicate/neighbour/ID switch.
- **steps:** human observability/adjudication first; same clips compare face/head state A vs sequence/item relation B. B requires before/after/continuity, strict D item link; D=T,C=T remains possible. Blind gap→change bounds/removal U; no before-state not forced-negative.
- **measurements:** state confusion/false coverage, U/person-time, state/transition event recall/FA-hour, onset delay/bounds, false removal from gaps/missing history.
- **evidence:** separate C/D/R/Z and item/part/track timelines, before/after frames/clips, gap/adjudication, model/config/paired outcomes.
- **outcomes_limits:** state-only visibility→name state; transition only with agreed endpoint/benefit; unreadable face→checkpoint/U. Staged success not plant transfer/fit-seal or perfect item identity through occlusion.

### E017 — Narrow pinned Frigate runtime replay

- **id:** [E017](OPEN_QUESTIONS.md#e017), Q015/Q007, K006.
- **decision:** runtime scope of static ledgers and implications for own E009 policy.
- **inputs:** v0.18.2/`cfa08c56b23d23280c3d0a218e5a43182c97445b`, ordinary enabled person zone/no speed/filters passed, exact config/FPS/timed detections/Norfair state; runtime not yet launched.
- **steps:** after constructor A inertia3/L0 `in,out,in,in`; B inertia1/fps5/L1s partial dwell/out/reentry; C prediction-only last measured inside/outside while tracker returns ID; D stationary reuse/no new detector. Add removed/end/finished/new ID, camera disable/resolution reset/missing frame/queue drop. Do not attribute entry to first `in,out,in` at I3.
- **measurements:** box/centroid/estimate/frame_time/current time, P/L/current/entered, ID/end_time, caller gates, update count/Norfair lifetime and actual-measurement flag; expected-ledger divergence.
- **evidence:** exact code/config hashes, expected/actual runtime trace, overlays/drops/provenance.
- **outcomes_limits:** match confirms only specified path; mismatch→revise caller/lifetime/filter assumptions and weaken claim. Later own-video event effects belong E009. Neither result certifies Frigate safety suitability or all-version defect; proposed, not completed replay.

<a id="first20"></a>
## First 15–20 minutes after full case: scope and P0 answers

**PROP:** Five-person team can divide policy/data, camera admission, exact LinQ artifact, event agreement and minimal integration, then combine one endpoint map. This interval selects a route, not a completed implementation. [F102](RAW_FACTS.md#f102)–[F107](RAW_FACTS.md#f107), [F117](RAW_FACTS.md#f117), [F122](RAW_FACTS.md#f122), [F123](RAW_FACTS.md#f123).

| Source-time after case arrival | Action/output |
|---|---|
| 0–4 min | Extract mandatory endpoints, approved PPE/alternatives, state vs transition, floor vs volume, metric unit, shortest important episode/max delay/U policy. Open Q001/Q002/Q003/Q008/Q009 explicitly. |
| 4–8 min | Inspect **native** head/face/hands/feet/cigarette, mode/angle/scene and actual target pixels; mark each camera-region/fact readable, candidate-only or U; preserve native ROI examples for E003/E013. |
| 8–12 min | Map each fact to simplest detector/state/crop/geometry route, owner/anchor/time/gate, event evidence and missing external inputs. |
| 12–16 min | Present exact graph/inputs/heads and device/SDK/compiler/access/execution-proof questions; agree auxiliary neural and CPU boundary Q005/Q006/Q007; start available E015 gate, without claiming compile/run success. |
| 16–20 min | Freeze admitted scope/fallback/checkpoint, deferred predicates, first-checkpoint questions and minimum paired/event checks. |

Conditional fallback: overview camera may support floor zone/helmet; respirator/smoking may need close view/checkpoint. Mandatory observed removal cannot be silently replaced by uncovered state: agree Q002/E016 and retain missing history U. Without supplied flammable context evaluate smoking separately, compound rule unconfirmed. If only one detector artifact passes LinQ, add auxiliary networks only after execution/policy confirmation; CPU geometry/rules still provide event logic. For an unreadable mandatory cue, show exact source/crop and missing input. [F102](RAW_FACTS.md#f102), [F103](RAW_FACTS.md#f103), [F117](RAW_FACTS.md#f117), [F123](RAW_FACTS.md#f123).

**UNK P0 — full case/customer/access must answer; general search cannot replace them:**

| Question | Decision changed / closure |
|---|---|
| [Q001](OPEN_QUESTIONS.md#q001): mandatory approved types/parts/alternatives, both gloves, helmet strap, role/operation scope? | Taxonomy/GT/eligibility; expert allowed/disallowed/U examples→E001/E003. Unsupported type U until settled. |
| [Q002](OPEN_QUESTIONS.md#q002): “removed” = current uncovered, coverage-loss or strict item-doffing; already-uncovered/hidden transition? | State vs sequence/item graph/GT→E016; no observed history is not removal. |
| [Q003](OPEN_QUESTIONS.md#q003): floor, any body part or 3D volume; crossing vs occupancy; supplied flammable context? | Anchor/geometry/onset/external inputs→E006/E007/E010. |
| [Q004](OPEN_QUESTIONS.md#q004): native streams/resolution/codec/exposure/IR/angle/target sizes, original ROI/checkpoint, real negatives? | Camera-region admission/crops/scope→E003/E013/E011. |
| [Q005](OPEN_QUESTIONS.md#q005): all neural stages on LinQ, allowed CPU decode/NMS, external verifier/auxiliary execution and proof? | Authorised entire chain, not inferred from postprocessing→execution contract/E015. |
| [Q006](OPEN_QUESTIONS.md#q006): assigned device/SDK/compiler/runtime/opset/shapes/heads/precision/fallback/account? | Exact graph shortlist→four E015 gates. Unknown capability is not unsupported capability. |
| [Q007](OPEN_QUESTIONS.md#q007): capture clock/PTS, ordering, cadence/jitter/bursts/queue/network delay? | Tracker/max gap/stale TTL/latency→capture→inference→receive→publish traces, E008/E009/E015. |
| [Q008](OPEN_QUESTIONS.md#q008): event unit/GT/split/matching/minimum episode/max delay, FP/duplicates/U/availability/negative hours? | Thresholds/time tradeoff/evaluator→agreed programme/E010 before quality claim. |
| [Q009](OPEN_QUESTIONS.md#q009): cigarette/puff/lit session/vape, observable negative window and simultaneous actions? | Candidate vs confirmed smoking/GT/route A or B→expert contract/E011. |

**UNK follow-up index:** [Q010](OPEN_QUESTIONS.md#q010) actual SH17 extended export/guide and semantic remap→E001; [Q011](OPEN_QUESTIONS.md#q011) industrial neck/hand/removal artifacts/weights→author artifact or own clips/labels, E001/E016; [Q012](OPEN_QUESTIONS.md#q012) target pose/HOI ownership benefit→E002; [Q013](OPEN_QUESTIONS.md#q013) best-frame ageing/pause/expiry/abstention/incident return→E004/E005/E009; [Q014](OPEN_QUESTIONS.md#q014) hazard/authorisation source, person match/TTL/outage→integration contract/E010. Q010–Q014 and [Q020](OPEN_QUESTIONS.md#q020) exact INT8 effects/options→E015 are P1. [Q015](OPEN_QUESTIONS.md#q015) pinned Frigate runtime effect→E017 and [Q016](OPEN_QUESTIONS.md#q016) full OIL SoW/actual SAT→specific document are limited external comparisons; baseline does not depend on them. [Q017](OPEN_QUESTIONS.md#q017) RegistryKeys target-version tables is P2, use only after full table/units/defaults obtained. [Q018](OPEN_QUESTIONS.md#q018) required fall/hook endpoint/physical GT→E012 and [Q019](OPEN_QUESTIONS.md#q019) our reject-only VLM net benefit→E014 are P2 dependent on full-case priority/time. None is declared closed by a proposed E.

<a id="handoffs"></a>
## Topic handoffs: facts that change a neighbour's decision

These are prepared file pointers, not messages to external people or claims that neighbouring reports exist. Outside this folder cite `violation_methods:F...` to disambiguate local IDs. [Human handoff](report_human_violation_methods.md).

| Topic | Decision / evidence / remaining action |
|---|---|
| `linq_platform` | Establish exact device/SDK/operator/postprocess boundary and proof for **all** neural stages, available precision. [F063](RAW_FACTS.md#f063)/F064/F116–F118; Q005/Q006/Q007/Q020; E015. YOLO/ONNX claim does not accept artifact. |
| `model_stack` | Select head-state/person+PPE and industrial approved-type classifier; only measured bottleneck justifies pose/fixed OVD/clip. [F009](RAW_FACTS.md#f009)/F069/F070/F102/F114/F116/F120; Q006/Q011/Q012; E002/E015/E016. No weight/export catalogue made here. |
| `datasets` | Accept actual annotation unit/index/omission/relations/visibility/time; relabel or ignore when state GT absent. [F001](RAW_FACTS.md#f001)/F005/F007/F066–F073/F100–F102; Q001/Q010/Q011; E001/E016. Missing annotation is not visible negative. |
| `training_strategy` | Collect held/spare/neighbour PPE, approved clothing alternatives, hood/cap/unknown parts, eat/drink/phone/adjustPPE and actual nightIR/blur/domain slices. [F010](RAW_FACTS.md#f010)/F019/F089/F119–F123; Q004/Q011/Q012/Q020; E001/E002/E003/E011/E013/E015. Do not train U as negative. |
| `evaluation` | Freeze endpoint/actor-aware one-to-one matching, point collar vs interval tIoU, negative hours, U/availability/censoring before tuning; paired smoking/VLM and state/removal/INT8 event outcomes. [F100](RAW_FACTS.md#f100)/F102/F105–F107/F123–F125; Q008/Q009/Q013/Q019/Q020; E008–E012/E014–E016. |
| `video_architecture` | Deliver source PTS and measured/reused/predicted provenance, order/staleness, native ROI, bounded crop age/calls and scene invalidation. [F078](RAW_FACTS.md#f078)–F081/F085–F088/F105/F112/F113/F116/F121; Q004/Q007/Q013; E008/E009/E013/E015/E017. Configured FPS/timestamp equality is not fresh cadence. |
| `operator_product` | Separate item/coverage/rule, U reason and technical end vs observed clear; maintain event revision, rule/scene/model versions, fullframe+crop/pre-post clip and approved policy/context. [F100](RAW_FACTS.md#f100)/F102/F106/F107/F119/F121/F125; Q001/Q003/Q008/Q013/Q014; E004/E009/E010/E014/E016. Delivery cooldown must preserve incident history. |
| `market_deployment` | Camera-specific applicability/survey/remediation and actual acceptance needed; requirements ≠ achieved accuracy. RGB/NIR/thermal separate. [F018](RAW_FACTS.md#f018)/F048/F076–F079/F082–F084/F090; Q004/Q008/Q016; E003/E010/E013. Headline accuracy does not supply SLA/PMI/SAT. |
| `hackathon_strategy` | Select mandatory observable endpoints and exact passing LinQ artifact within 45 hours; demonstrate hard negative, U/loss and execution proof alongside positive event. [F065](RAW_FACTS.md#f065)/F102–F107/F117/F119/F123–F125; Q001–Q009; E003/E006/E009/E010/E011/E015/E016. Fixed floor/helmet route is conditional; respirator/smoking need readable detail. |

Next practical input is native customer video plus exact graph/device access: admit camera/predicate, test simple event chain, then decide whether each added neural stage pays for itself. Every claim should identify observable fact, owner, evidence age, active rule and remaining U.
