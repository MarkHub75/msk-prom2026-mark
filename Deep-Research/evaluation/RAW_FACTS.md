# RAW_FACTS — evaluation

Собрано по завершённым 15 W1 и четырём W2; новые источники после W2 не получались. Дата исследования — 23 октября 2026, Europe/Moscow (UTC+03:00); точные моменты доступа относятся к соответствующим S-записям. Это подробная фактическая база, а не измерение системы. [Реестр источников](SOURCES.md), [вопросы и будущие эксперименты](OPEN_QUESTIONS.md), [исходная критика и dispositions](CRITIC.md).

У каждого F сохранены исходный контекст, определения, параметры, граничные случаи и фактический статус проверки. DOC — первичная документация; CODE — прочитанный исходник; PUB/PAPER — опубликованный результат/метод авторов; LOCAL/LOCAL MATH — фактически выполненная маленькая синтетическая проверка/арифметика; INFERENCE/DERIVATION — наш вывод/вывод формулы; PROPOSAL/PROPOSED — предложенный договор; UNKNOWN — недостающий вход. Тип основания и выполнение различаются: прочитанный код не считается запущенным. Групповые F-записи сохраняют исходные метки каждого наблюдения внутри, не превращая всё содержимое в один измеренный факт.

## F001 — Фактический уровень выполненной работы
<a id="f001"></a>

**Основание: локальное состояние и выполненные исследователями действия.** Существуют 19 завершённых branch-результатов и сохранённые первичные snapshots/locators. Исполнены только явно названные source-level/synthetic mathematical fixtures (COCO matching/accumulation, извлечённые sed_eval validators, TrackEval metrics на supplied similarity, статистическая арифметика, ActEV extracted function, конечная sampling enumeration и tiny matcher oracle). Ни один не является измерением модели, промышленного видео, LinQ, event recall, FPS или эксплуатационной безопасности. Нет полученного SDK, endpoint/device access, actual model/weights, organizer data/evaluator или соседних готовых отчётов. Для будущих прогонов используются E-карточки в OPEN_QUESTIONS.

## F002 — LinQ: публичный blocking path установлен; actual execution неизвестен
<a id="f002"></a>

**DOC/CODE/INFERENCE; чтение, без исполнения.** Руководство IVA H1 2025 RU.РМДВ.04.06.014-03 34 01 описывает list/open/load/inference и blocking `inference.sync(...)` с returned output mapping. Оно не было установлено/исполнено. TLM `execution_time_us` — estimate, µs, не hardware samples. Устаревшая широкая формулировка W1 о неизвестном completion API ниже читается только как неизвестная actual package/remote applicability. Python3.11 versus3.8, signature/default and sample-fragment расхождения сохранены. Wheel/build, working example, allocated hardware, remote job semantics, placement/fallback и physical timer требуют артефакта/доступа ([Q009](OPEN_QUESTIONS.md#q009)–[Q012](OPEN_QUESTIONS.md#q012)); [K001](CRITIC.md#k001).

Основание: [S124](SOURCES.md#s124), [F217](#f217)–[F223](#f223); manual printed pp5–10,17,19–25, сохранённый numbered text L0–L650.

## F003 — Экспозиция и достаточность review зависят от estimand
<a id="f003"></a>

**PROPOSAL/INFERENCE, W2 уточняет W1.** Complete destination-delivery census + adjudication всех record assertions с достаточным context может установить semantic false records / fixed logged source camera-hours без полной разметки каждого non-alert кадра. Это не recall, не verified-normal exposure и не false-active duration. Strict useful one-to-one precision дополнительно требует закрытого matching neighborhood. Для recall нужна независимая discovery всех GT onsets либо корректный probability-sampled core audit. Поэтому W1 formulations «fully reviewed hours» ниже сохраняются только для соответствующего более строгого endpoint. Source burden использует immutable latest-consumed-input evidence anchor при first logical alert creation; wall-hour workload — actual visible records в receiver interval. У record exactly one source owner, поздний retry не меняет owner. Finite close C именует delivered-by-C snapshot, не eventual total; все pending/late/drain/carry-in/out остаются в ledger. Source-alert precision и onset-GT recall не имеют автоматически общего TP/F1. См. [Q013](OPEN_QUESTIONS.md#q013), [Q014](OPEN_QUESTIONS.md#q014), [K002/K003](CRITIC.md).

Основание: [F224](#f224)–[F234](#f234), source-derived distinctions [S127](SOURCES.md#s127), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129); ownership/close rules являются нашими proposals.

## F004 — Randomized finite-corpus review: unbiased totals, generally biased ratio
<a id="f004"></a>

**PROPOSAL/DERIVATION + LOCAL MATH.** Disjoint exhaustive half-open cores, known positive inclusion π, independent full-core reference review, onset ownership и достаточный adjoining context позволяют design-unbiased HT totals Σy/π для fixed recorded corpus. Это randomization inference: iid camera contents/events не требуются. Future-camera inference требует отдельного population/sample model. Recall That/Ehat — generally biased ratio, даже если оба total estimates unbiased; tiny exact enumeration mean ratio .5625 против истинных .3. Контекст не становится дополнительным selected unit. Global one-to-one outcomes требуют closure всего competing component; произвольный margin не гарантирует closure. Неответ/нечитаемый selected core нельзя заменить/заполнить нулём. Нулевой Ehat даёт NA recall; n_h=1 noncertainty stratum не даёт указанной variance estimate. [Q014](OPEN_QUESTIONS.md#q014), [Q015](OPEN_QUESTIONS.md#q015), [K004](CRITIC.md).

Основание: [F235](#f235)–[F249](#f249), [S131](SOURCES.md#s131), [S117](SOURCES.md#s117), [S132](SOURCES.md#s132); exact invented-population outputs сохранены в [fixtures.json](_WORK/W2_03_SOURCES/fixtures.json).

## F005 — Предложенный lex-offline-v1 — tiny exact oracle
<a id="f005"></a>

**PROPOSAL + выполненные LOCAL MATH fixtures.** Objective lexicographically minimizes (-pair count, summed nonnegative exact cost, sorted stable pair list), invalid edges absent, unmatched explicit. Costs Fraction/ticks; no epsilon/big-M. Выполнены 13 named graphs/permutations, все512 labeled3×3 graphs cardinality versus SciPy1.17.1 и independent partial-injection oracle для всех трёх priorities. Reference exponential, годится для tiny conformance; scalable production implementation не проверена. Sum delay не min max/p95: fixed selected subsets имеют permutation-invariant sum(d)-sum(s). Это отдельный supplemental protocol, не замена COCO/ActivityNet/sed_eval/official scoring. [Q016](OPEN_QUESTIONS.md#q016), [K006](CRITIC.md).

Основание: [F251](#f251), [F252](#f252), [F256](#f256)–[F261](#f261); solver semantics [S133](SOURCES.md#s133), [S134](SOURCES.md#s134); our [reference/results](_WORK/W2_04_SOURCES/results.json).

## F006 — Interval truth, censoring и граница K005
<a id="f006"></a>

**PROPOSAL/DERIVATION + tiny LOCAL MATH.** Exact point endpoint требует известной truth/identity/clock и полного opportunity follow-up. Unknown onset support не probability distribution. Definite-edge graph и possible-edge union дают только outer matching count bounds при fixed known roster; possible union maximum не обязательно attainable: linked onsets s1=θ,s2=θ+1 допускают individually possible2, jointly max1. Общего solver по jointly feasible truth worlds не создано и не заявлено. Unknown roster/identity меняет знаменатель и требует quarantine/конкретных совместных truth cases. Primary complete-component endpoint исключает весь incomplete stratum/component, включая successes, с counts/exposure; это narrow conditional endpoint, не unbiased whole-population recall. Known short episodes с завершившейся opportunity остаются полными; processing outage при известном GT/log — operational miss, missing logs/follow-up — unresolved. [Q014](OPEN_QUESTIONS.md#q014), [K005](CRITIC.md).


Основание F006: [F253](#f253), [F254](#f254), [F262](#f262)–[F265](#f265); [joint-onset/censor fixtures](_WORK/W2_04_SOURCES/results.json). Joint-world general solver не является полученным источником или выполненной реализацией.


# W1_01 — сохранённые подробные наблюдения

Происхождение: [W1_01](_WORK/W1_01.md); [snapshots и локальные fixtures](_WORK/W1_01_SOURCES/). Контекст доступа и выполнения:  Research cell W1_01. Research date: 2026-10-23, Europe/Moscow (UTC+03:00). Primary sources accessed 03:03:50–03:03:55 UTC (06:03:50–06:03:55 Moscow); exact per-source timestamps and SHA-256 in `W1_01_SOURCES/retrieval_manifest.json`. Context: industrial video safety examples, with no organizer taxonomy, truth schema, data or evaluator supplied. This is annotation methodology research, not a dataset catalog, model test or legal analysis.


## F007 — Decision
<a id="f007"></a>

Adopt a versioned truth contract separating four claims: visible object, observed person–object relation/state, temporal episode, and policy-defined violation. Keep unknown, not reviewed, out of scope and negative distinct. Annotators must be able to mark a person while declining to infer that person's head protection. Establish independent agreement before model comparisons; preserve initial annotations and adjudication separately. These are project proposals, not organizer requirements.


## F008 — Missing annotation is not a negative. Documentation: [S002, S003]
<a id="f008"></a>

**[F008](#f008) — Missing annotation is not a negative. [Documentation: [S002](SOURCES.md#s002), [S003](SOURCES.md#s003)]** Open Images distinguishes positively verified, negatively verified and unannotated image classes. Its documented detection policy ignores predictions for unannotated classes and counts detections for negatively verified classes as false positives. Box completeness is conditional on available positive image labels, with group/body-part qualifications. “All boxes annotated” must name its scope. An arbitrary imported label file is not necessarily exhaustive truth.


## F009 — Object annotation does not establish an associated action. Documentation: [S005]
<a id="f009"></a>

**[F009](#f009) — Object annotation does not establish an associated action. [Documentation: [S005](SOURCES.md#s005)]** VOC action guidelines require clear direct visual evidence, allow simultaneous actions and permit uncertain people to remain unannotated. They distinguish a phone at the ear from one held, and playing an instrument from holding it. “Other” requires confidence that no listed action applies. Transfer to PPE is an inference: a helmet detection does not establish wearing, correct use or ownership.


## F010 — Visibility and person existence can be separate annotations. Documentation: [S006]
<a id="f010"></a>

**[F010](#f010) — Visibility and person existence can be separate annotations. [Documentation: [S006](SOURCES.md#s006)]** CrowdHuman documents visible-body, full-body and head boxes; separate person/head attributes include ignore, occlusion and head uncertainty. Attributes are optional. Certain crowds/reflections/person-like regions are ignored. This supports a schema pattern, not importing its exact ignore rules. Missing optional fields must not automatically mean known and unoccluded.


## F011 — Benchmark policy may contradict deployment assumptions. Documentation: [S004]
<a id="f011"></a>

**[F011](#f011) — Benchmark policy may contradict deployment assumptions. [Documentation: [S004](SOURCES.md#s004)]** VOC2011 uses visible-area boxes, leaves uncertain objects unlabelled, permits small-object discretion, labels mirror objects and certain photorealistic pictures. A workplace alarm should explicitly distinguish physical workers from reflections/posters. Identical class names therefore do not establish label compatibility. Historical VOC percentage conventions are not proposed project thresholds.


## F012 — Evaluated empty time differs from excluded time; truth changes by revision. Documentation: [S007]
<a id="f012"></a>

**[F012](#f012) — Evaluated empty time differs from excluded time; truth changes by revision. [Documentation: [S007](SOURCES.md#s007)]** AVA v2.2 evaluates included timestamps even when no action is annotated, while explicitly excluded timestamps are not evaluated. Rows link persons, actions, interval middle frames and person IDs. The v2.2 update inserted missing labels, increasing annotations by 2.5%, and corrected some box aspect-ratio issues. This demonstrates version-sensitive truth, not continuous event-boundary precision.


## F013 — Agreement concerns the procedure and chosen units. Methodology: [S001]
<a id="f013"></a>

**[F013](#f013) — Agreement concerns the procedure and chosen units. [Methodology: [S001](SOURCES.md#s001)]** Artstein/Poesio explain chance models, prevalence effects and alpha's accommodation of multiple coders/missing values. They require explicit usable instructions and independent coders for reproducibility studies. High raw agreement may coexist with weak rare-label discrimination. They caution against universal coefficient interpretation and equating agreement with machine-learnability. The video-specific protocol below is a proposal; no project agreement has been measured.


## F014 — Proposed truth schema
<a id="f014"></a>

These fields are an original proposal, not official format or SDK/API.

| Layer | Required information | Interpretation |
|---|---|---|
| Asset/review scope | Stable camera/video/frame IDs; media checksum; decoded dimensions; frame index/timestamp convention; reviewed intervals and classes/relations; protocol/revision | Empty labels become meaningful only with explicit review completeness. |
| Person/object | Local object ID; class/taxonomy version; visible box; separately named optional amodal box; coordinates; occlusion/truncation/blur; physical/reflection/depiction; ignore reason | Establishes objects, not wearer states. |
| Person–PPE relation | Person/PPE IDs; relevant body-part evidence; on_head/on_face, held, hanging, nearby, owner_unknown; relation status/reason | Ownership cannot be inferred from overlap alone. |
| Observable person state | Per person/requirement/time: present_in_required_visible_position, absent_from_required_visible_region, visibly_mispositioned, unknown; reason/evidence | Correct use must be decomposed into observable criteria. |
| Requirement context | Rule ID/version, applicable location/work context/time, required protection class; authoritative source; whether applicability known | A visible state becomes a task-defined violation only with an applicable rule. |
| Episode | Person/rule; evidence intervals; earliest/latest supported onset/end; left/right censoring; visibility gaps; identity certainty | First positive frame need not be true onset. |
| Provenance | Annotator/role; independent pass; initial label/time; adjudication/reason; manual version; superseded revision | Adjudicated agreement is not independent agreement. |

Use two axes. **Review:** reviewed / not_reviewed / out_of_scope. **Evidence for a reviewed attribute:** positive / negative / unknown. A person may have positive existence, unknown helmet state and negative zone entry. `ignore` is a task-specific evaluator instruction on a named region/time with a reason; it is not a synonym for all unknowns.

Unknown reasons: target body part occluded/outside frame; insufficient resolution; blur/glare; subtype unresolved; ownership unresolved; rule applicability unavailable; identity unresolved; temporal boundary unobservable. An unanswered item is missing workflow data, distinct from deliberate unknown.

For a missing-helmet question, an absence label requires sufficient evidence that the relevant head region is visible and lacks the required visible protection under the frozen manual. A hidden head remains unknown even if the algorithm detects no helmet. Decompose position, visible coverage, visible fastening and distinguishable subtype. Pixel evidence alone does not establish certification, respirator seal or hidden fastening. These are epistemic limits of the proposed task, not legal norms.


## F015 — Denominators and empty cases
<a id="f015"></a>

- N_scope: all eligible GT person-time units in fully reviewed intervals, including attribute-unknown people.
- N_determinate: units with supported positive/negative states for the specific question. Keep N_unknown, N_not_reviewed and N_ignore with reason distributions separately.
- Observability coverage = N_determinate / N_scope. State units explicitly: person-frames or duration-weighted person-time, never interchange them.
- State precision/recall among determinate units is conditional on observability. A predicted-person chain must retain missed GT people; a test only on matched people is conditional/oracle evaluation and must say so.
- On GT-unknown cases, describe system abstention/forced decisions; ordinary correctness cannot be scored without additional truth.

Fix temporal sampling or duration weights. Irregular frame counts are not duration. Empty N_scope/N_determinate gives NA with counts, not perfect agreement/accuracy. No positive states gives undefined recall. A reviewed empty scene can contribute negative camera exposure but has no person-state units. Not-reviewed exposure cannot support a completed evaluation claim. This cell does not specify event matching.


## F016 — Counterexamples for the annotation manual
<a id="f016"></a>

All cases below are proposed diagnostics, not measured results.

| Case | Required truth behavior | Error prevented |
|---|---|---|
| Helmet held in hand, visible bare head | Helmet object positive; held relation; head-protection absence | Object presence becomes safe state. |
| Adjacent workers, only one helmet | Separate people and wearer relation | Neighbor PPE assignment. |
| Torso behind machine, hidden head | Person positive; helmet unknown | Non-detection becomes violation. |
| Cloth mask versus respirator unresolved at distance | Face-covering evidence may be positive; subtype unknown | Broad class satisfies specific protection. |
| Respirator below visible nose | Record criterion failure if manual specifies it; filter/seal unknown | Mask object hides visible misuse. |
| Helmet on head, strap occluded | Position positive; strap unknown if applicable | Correct use inferred from partial evidence. |
| Worker plus reflection/poster | Physical/depicted distinction and scope | Duplicate or fictitious worker. |
| Same state before/after a hidden gap | Gap unknown; continuity uncertain unless disclosed inference rule exists | Retrospective filling of hidden intervals. |
| First clip frame already shows absence | State known; onset left-censored | Clip start becomes real onset. |
| Hand-to-mouth gesture near stacked material | Action unknown without defined visual evidence; combustibility from approved context or unknown | Gesture and assumed material become violation. |
| Unmarked person in sparse imported annotation | Review completeness unknown | Missing label becomes false positive. |
| Blurry person-like shape | Ambiguous region/reason | Localization uncertainty disappears. |


## F017 — Independent annotation and adjudication
<a id="f017"></a>

1. Write positive, negative, unknown and borderline examples; body-part visibility, box and ownership rules; temporal sampling and permitted context. Distinguish streaming-only evidence from offline future-frame context. Future context may clarify truth retrospectively but does not prove it was observable earlier.
2. Discuss/revise a pilot manual on calibration clips. Do not report this discussed set as independent agreement. Choose a subsequent reliability sample with ordinary exposure and difficult strata; retain selection method and per-stratum counts. There is no universal sample size guaranteeing reliability across cameras or rare labels.
3. Have at least two annotators work independently from the same frozen manual/context without seeing each other's labels or model outputs. Save initial outputs before discussion. Correcting an existing annotation is useful QA, not an independent replicate.
4. Separate finding units from classifying states. A common adjudicated person/time roster supports conditional state agreement. Independently annotating persons and states also reveals omissions/localization disagreement. Report the route; do not conflate the two.
5. On a common roster publish the full contingency table including explicit unknown. Observed agreement = identical paired labels / units with both independent responses. Workflow-missing responses are not unknown labels. Give per-state/pair counts. For two coders, Cohen kappa = (Po-Pe)/(1-Pe), with Pe from individual label marginals. For multiple coders/missing responses, nominal alpha may be suitable, but pin implementation and missing handling before use. Undefined expected disagreement gives NA. No pass threshold is asserted.
6. With independently found units, predeclare class eligibility, coordinates, one-to-one box matching, IoU convention and threshold. Retain unmatched persons. Report localization IoU distribution and finding agreement separately: averaging IoU only among matched people hides omissions. This report does not invent a benchmark threshold.
7. For temporal truth report jointly covered duration, unknown gaps, episode counts and boundary uncertainty. Boundary difference in seconds applies only when both boundaries are observable; publish pair/censored counts. Frame-state kappa does not establish episode/onset agreement.
8. Adjudicate against permitted evidence and document reasons, retaining unresolved unknowns. A new rule means a new manual version; identify affected labels and reannotate consistently. Measure agreement on raw independent annotations, not after replacements. Do not patch only examples where a model fails.

**Mathematical example, not a local experiment:** for 100 common units, 98 negative/negative, one positive/negative and one negative/positive, observed agreement is 98%. Both positive marginals are 1%, so Pe = .99² + .01² = .9802 and kappa ≈ -.0101. Positive/positive agreement is zero. Thus publish the table and rare-state counts rather than treating 98% as sufficient. This calculation does not prescribe a rejection threshold.


## F018 — Proposed experiment
<a id="f018"></a>

**Decision:** can a visible-use label support reproducible model comparison, or should the scope/view/manual change? Inputs: permission-cleared clips, view IDs, approved context/rules, frozen manual, independent annotators and sampling/provenance manifest. LinQ access is unnecessary.

Select camera/scene episodes as independent sampling units; code person-time units while retaining scene clustering. Fixed parameters: media, review scope, permitted future context, sampling, coordinates, roster route and unknown vocabulary. Revise the manual only during pilot; freeze it for the independent pass.

Independently annotate; compute [F017](#f017) counts/agreement; inspect causes by label/view; adjudicate and store initial/final outputs and reasons. Reproducible states permit a narrow evaluation. Persistent subtype/occlusion/ownership ambiguity calls for reduced label scope, better view or external context; instruction ambiguity calls for manual revision. Stop the pilot once remaining uncertainty is represented and a fresh independent pass can be specified, not at an invented scalar target. Success demonstrates annotation reproducibility on sampled conditions, not safety effectiveness or unseen-camera reliability. No local agreement, annotation speed, model score or power claim was measured.


# W1_02 — сохранённые подробные наблюдения

Происхождение: [W1_02](_WORK/W1_02.md); [snapshots и локальные fixtures](_WORK/W1_02_SOURCES/). Контекст доступа и выполнения:  Researcher cell W1_02. Access: 2026-10-23 06:01–06:06 +03:00 (Europe/Moscow). Scope: bounding-box detection, not person violations, temporal events, operational alerts or LinQ performance. No model ranking or acceptance target is established.


## F019 — (source inspection + inference):
<a id="f019"></a>

**[F019](#f019) (source inspection + inference):** “AP” or even “mAP50” is insufficient for a comparison. Freeze GT/images/categories, annotation completeness and ignore policy, coordinate conversion, score/NMS/output caps, evaluator revision/dependencies and every evaluation parameter. Report per-class support and explicit undefined results alongside the aggregate. COCO AP measures ranked detection quality under a specific matching procedure; it does not measure a deployed confidence operating point or alert workload.


## F020 — (source inspection):
<a id="f020"></a>

**[F020](#f020) (source inspection):** The pinned reference is cocodataset/cocoapi commit `6c3b394c07aed33fd83784a8bf8798059a1e9ae4`, dated 2019-12-25 19:22:32 UTC. GitHub commits API queried for `PythonAPI/pycocotools/cocoeval.py` returned this as the most recent change to that path at access time. This is a valid immutable repository snapshot, not a claim that the entire repository HEAD has this hash. Raw `cocoeval.py`, `coco.py` and `common/maskApi.c` were retrieved at the same snapshot. Source downloaded and read; only the explicitly described small examples below were executed.


## F021 — (S008–S010 code):
<a id="f021"></a>

**[F021](#f021) ([S008](SOURCES.md#s008)–[S010](SOURCES.md#s010) code):** Initialize explicitly with `iouType='bbox'`; default constructor type is `segm`, so relying on default is a different evaluation. `bbox` is `[x,y,width,height]`, with continuous rectangle extents: `bbIou` computes intersections from x+w/y+h, without pixel-inclusive `+1`. Coordinates must be restored to the GT image coordinate system after resize/letterbox. This code path does not establish a robust validation or clipping policy for invalid boxes. Do not assume normalized values, xyxy, negative dimensions or wrong class IDs will be diagnosed helpfully.

Detection results carry `image_id`, `category_id`, bbox and confidence `score`. `loadRes` asserts detection image IDs belong to the GT image set and assigns detection IDs; its bbox branch derives detection area as width×height. GT `area` comes from annotations, not recomputation here, and can be segmentation area even in bbox evaluation. Therefore changing GT area conventions can change AP by size without changing bbox IoU.


## F022 — (S008 Params):
<a id="f022"></a>

**[F022](#f022) ([S008](SOURCES.md#s008) Params):** Defaults: ten IoU thresholds 0.50, 0.55, …, 0.95; 101 recall samples 0, .01, …, 1; category-aware evaluation (`useCats=1`); caps `[1,10,100]`; area ranges in squared image pixels: all `[0,10^10]`, small `[0,1024]`, medium `[1024,9216]`, large `[9216,10^10]`. The tests use `< lower` or `> upper`, so boundaries 1024 and 9216 occur in both neighboring bins. This is exact code behavior, not the common informal disjoint-bin description. “Small” is not a physical-size claim or universally appropriate industrial-camera stratum.


## F023 — (S008 evaluate/computeIoU/evaluateImg):
<a id="f023"></a>

**[F023](#f023) ([S008](SOURCES.md#s008) evaluate/computeIoU/evaluateImg):** Matching occurs per selected image and category, separately for every IoU threshold and area range. Detections are sorted descending by score with stable mergesort and capped at the largest maxDets. For each score-ranked detection, a greedy scan finds the highest qualifying IoU among available GT, favoring nonignored GT over ignored GT. A normal GT can be consumed only once at each threshold; crowd GT may match multiple detections. This is not a global Hungarian assignment. Qualifying comparison is effectively `IoU >= threshold`; threshold initialization uses `min(t,1-1e-10)`. Equal-IoU candidates can replace an earlier candidate because only strictly lower overlap is skipped. Equal score order inherits input order within images; accumulated ties inherit image concatenation order (evaluation image IDs are uniqued/sorted). Preserve output ordering for exact reproducibility.


## F024 — (S008/S010, unusually important):
<a id="f024"></a>

**[F024](#f024) ([S008](SOURCES.md#s008)/[S010](SOURCES.md#s010), unusually important):** `_prepare` first reads/defaults a GT `ignore` field, then immediately overwrites it with the value of `iscrowd` (or false if absent). Thus `ignore=1, iscrowd=0` does **not** provide an arbitrary ignored region in this pinned bbox implementation. Later `computeIoU` directly indexes `iscrowd`, so normal bbox annotations should supply it. Area-range exclusion adds `_ignore` independently. A detection matching ignored GT is ignored; an unmatched detection outside the current area range is ignored. Ignored detections contribute neither TP nor FP; ignored GT is removed from the positive denominator. Crowd overlap is intersection / detection area rather than ordinary intersection / union (`bbIou`), allowing several contained detections to be absorbed by one crowd region. Do not encode every ambiguous PPE annotation as crowd without an explicit semantic policy and compatibility test.


## F025 — (S008 accumulate):
<a id="f025"></a>

**[F025](#f025) ([S008](SOURCES.md#s008) accumulate):** For each category/area/cap, retained detections from all evaluated images are concatenated and globally sorted by confidence, again stable mergesort. Nonignored matched detections count TP; nonignored unmatched detections count FP. Cumulative recall = TP / number of nonignored GT; cumulative precision = TP/(TP+FP+machine-spacing). This is pooled per-class ranked detection evaluation, not the average of frame-level precision values. No true-negative count exists in this AP calculation.

Precision is replaced by its right-to-left monotonic envelope. At each recall sample, `searchsorted(..., side='left')` takes the first achieved recall at or above that sample; unattainable recall samples retain zero. AP is the arithmetic mean of these 101 sampled precision values, then mean over selected IoUs and valid categories for the requested area/cap. It is not simply precision at score .5 or exact integral over all unique recall breakpoints. AR uses the final attainable recall for each IoU and averages valid entries; AR@100 is not a deployed thresholded recall.


## F026 — (S008 empty cases):
<a id="f026"></a>

**[F026](#f026) ([S008](SOURCES.md#s008) empty cases):** If a category-area setting has zero nonignored GT over the evaluation image set, precision/recall remain sentinel -1, even when there are detections. Summary excludes values <= -1. Consequently a class absent throughout the test can yield no AP penalty from its false predictions; separately report its FP count and exposure. If that class has GT somewhere, predictions on its negative images are pooled FPs and can affect AP. If GT exists but detections are absent, AP and recall are zero. An image-category with neither GT nor detection returns `None` and adds no TN benefit. All-crowd GT similarly has no positive denominator. An all-empty **result list** is an additional loader problem: [S009](SOURCES.md#s009) indexes `anns[0]` and will raise rather than directly construct empty predictions. A harness must explicitly support the no-prediction case and test its wrapper.


## F027 — (S008 summarize):
<a id="f027"></a>

**[F027](#f027) ([S008](SOURCES.md#s008) summarize):** Standard bbox summary is 12 numbers: AP@[.50:.95], AP50, AP75, AP small/medium/large, AR@1/@10/@100, AR small/medium/large at 100. Values are fractions on [0,1] before display scaling. Frameworks may show percent [0,100]; record units. Main summary AP uses default helper cap=100, while several other entries index `params.maxDets[2]`. `summarize` explicitly assumes defaults: editing cap list/thresholds and trusting unchanged headline labels can give invalid or empty summaries. For custom settings explicitly select and label tensor entries instead of assuming the standard printed vector remains meaningful.


## F028 — (locally executed, deliberately limited):
<a id="f028"></a>

**[F028](#f028) (locally executed, deliberately limited):** `small_examples.py` runs the downloaded `evaluateImg` and `accumulate` bodies with supplied IoU matrices, one image/class, one IoU=.5, all area and cap 100. Environment NumPy 2.4.2. It substitutes `dtype=float` for obsolete `dtype=np.float` and removes the relative mask import; no matching/accumulation logic changed. It does not execute loader, mask extension, raw-coordinate IoU, full evaluate or full 12-value summarize. Script/output saved; output includes progress text before JSON.

| Constructed data | Match result | AP50 | Implication |
|---|---|---:|---|
| One GT; score .9 perfect box, .8 duplicate | TP, FP | approximately 1 | A duplicate lowers terminal precision to 1/2 but may leave interpolated AP unchanged when it arrives after full recall. AP alone cannot establish duplicate-free output. |
| One GT; score .9 no overlap, .8 perfect box | FP, TP | .5 | Same one TP and one FP, different ranking, different AP. |
| No GT for class, one prediction | FP in per-image matching, undefined aggregate | null; tensor -1 | Not AP=0; absent class is excluded. |
| One GT, zero predictions | no TP, one missed GT | 0 | Empty predictions are a real failure when positives exist. |
| Crowd-only GT, two qualifying predictions | both matched and ignored | null; tensor -1 | Matching to crowd is not positive recall credit. |


## F029 — (own inference from formulas, not run):
<a id="f029"></a>

**[F029](#f029) (own inference from formulas, not run):** A correct xyxy box `[10,20,30,40]` mistakenly passed as xywh becomes rectangle x=10..40, y=20..60 rather than x=10..30, y=20..40. Its size, IoU and size stratum change despite an apparently plausible JSON. Swapped category mapping yields unmatched GT and wrong-class detections; an out-of-evaluation category can instead be filtered out. Validate IDs against the manifest rather than assuming contiguous zero-based IDs.


## F030 — (own inference from matching, not run):
<a id="f030"></a>

**[F030](#f030) (own inference from matching, not run):** A real but unannotated helmet, predicted correctly in a fully scored noncrowd region, becomes FP unless it accidentally matches another compatible GT. It does not establish that the visual detector is wrong. On an image declared empty, every retained evaluated-category prediction is unmatched; whether that means a valid negative test or annotation omission is external truth-contract evidence.


## F031 — (own inference, not run):
<a id="f031"></a>

**[F031](#f031) (own inference, not run):** For 101 noncrowd positive instances of one class in one image, cap=100 limits maximum recall to at most 100/101 even with otherwise perfect detection. Cap is per image-category for default useCats=1; it is not a global video or per-second cap. Candidate generation, NMS and model output truncation can impose lower caps before the evaluator sees detections.


## F032 — VOC/COCO: interpolation, matching, coordinates and difficult/crowd differences
<a id="f032"></a>

**[F032](#f032):** Official VOC2012 §3.4.1 states that from 2010 AP integrates the monotonic precision envelope at unique recall changes; the earlier VOC method samples eleven recall levels. This differs from COCO's 101 samples and ten-IoU headline. [S012](SOURCES.md#s012)'s pinned `voc_ap` implements both variants. Its `voc_eval` uses pixel-inclusive xyxy area with `+1`, strict `ovmax > ovthresh`, global class confidence sorting with `np.argsort` without specified stable kind, and a `difficult` mask excluded from positive count. Detections on a best-matching difficult GT are ignored. It selects the highest-overlap GT first and counts a repeat best match as FP; it does not search for an alternative unused GT the way COCO's candidate scan can. Consequently even “AP50 with the same boxes” can differ because of coordinates, equality, difficult/crowd handling, ranking ties, and assignment—not only interpolation. The official document and this implementation should not be conflated as one pinned artifact.

No framework-specific “fast COCO equivalent” or model-library mAP is assumed equivalent without a versioned implementation check. No organizer evaluator or installed package was supplied, so exact future official metric compatibility remains unknown.


## F033 — Proposed detector comparison contract (F033; proposal, not organizer rule)
<a id="f033"></a>

1. Freeze image manifest including truly negative images, annotation revision/hash, categories and mapping, all GT areas/crowd flags and annotation/ignore semantics. State which regions/classes were exhaustively labeled and which are unknown. Preserve original image size and coordinate convention.
2. Preserve raw predictions and evaluated postprocessed predictions. Record score threshold used for export, NMS method/IoU/class-awareness, pre/post NMS top-k, resizing/letterboxing, coordinate inverse transform, rounding/clipping, model/runtime revisions. A high export score threshold can remove low-score TPs and distort AP; choose/report it as part of the evaluation design rather than tune it on held-out results.
3. Pin evaluator source commit, package version, extension version/build, Python/NumPy environment and wrapper. Save `imgIds`, `catIds`, `useCats`, `iouType`, `iouThrs`, `recThrs`, `maxDets`, `areaRng`/labels and all transforms. Validate empty predictions and custom parameters before trusting summary.
4. Report standard COCO bbox AP/AP50/AP75 with fraction-or-percent unit, per-class AP and number of nonignored GT, image count, absent class list, crowd/ignored counts and all caps. Add thresholded precision/recall with explicit confidence and IoU policy and TP/FP/FN counts. For zero denominators, publish undefined plus counts, not fabricated 0 or 1. If computing F1, state policy and denominator explicitly.
5. Keep distinct reports for person ownership/violations and temporal delivered alerts; detector AP does not certify correctly worn protection, PPE ownership, timely warnings, false alerts per camera-hour or execution on LinQ. Those require additional GT units and matching contracts.
6. Regression fixtures should cover: exact IoU equality; duplicate after TP; FP before TP; two nearby GT with greedy competition; score ties; missing/wrong category; xyxy/xywh/letterbox inversion; unmatched small/large boxes; boundary area; crowd and generic-ignore behavior; positive no predictions; fully negative image; globally absent class; all-empty result list. Freeze expected intermediate matches and counts, not just one headline AP.

Unresolved: official category taxonomy, annotation completeness/unknown policy, evaluator revision, coordinate and area policy, required caps, and whether custom ignore regions exist. These are localized missing inputs, not reasons to assume standard COCO semantics automatically. Handoff to annotation/training/harness owners: preserve this evaluator specification and small fixtures; object AP must remain separate from person/event quality.


# W1_03 — сохранённые подробные наблюдения

Происхождение: [W1_03](_WORK/W1_03.md); [snapshots и локальные fixtures](_WORK/W1_03_SOURCES/). Контекст доступа и выполнения:  Research cell: W1_03. Author: independent first-wave researcher. Completed 2026-10-23, Europe/Moscow (UTC+03:00). Scope: evaluation and annotation contract for person-level PPE state; no architecture selection, legal conclusion, model benchmark or target-device claim.


## F034 — Decision and principal findings
<a id="f034"></a>

**Recommend two mandatory evaluations:** (A) a GT-person oracle diagnostic, and (B) the complete predicted-person → evidence/association → person-state chain. Object AP and cropped-region accuracy alone cannot establish person-level violation detection. Fix eligibility from GT visibility, never from successful detector/pose outputs. Keep all annotated people in an accounting ledger, including unknown head/face state and failed localization.


## F035 — [documented method]:
<a id="f035"></a>

- **[F035](#f035) [documented method]:** The head-center study explicitly distinguishes person and helmet detection from their relationship. It discusses annotation of a waist-down person as no-hardhat as an observability error. Its Algorithm 1 retains a generic person state if a head keypoint is unavailable; otherwise helmet containment changes the state. This is a relevant precedent for a third state, not a guarantee that a predicted keypoint establishes visibility. Source [S013](SOURCES.md#s013).


## F036 — [source inspection]:
<a id="f036"></a>

- **[F036](#f036) [source inspection]:** The author CPPE repository is conditional on pose evidence: `loc_head` and `loc_upbody` skip sparse keypoints and print warnings; other branches print invisible head/body warnings. Dropping those cases from a downstream accuracy denominator can reward reduced coverage. This conclusion is about the inspected localization utilities, not a reconstruction of the paper’s full evaluator. Source [S014](SOURCES.md#s014).


## F037 — [documented annotation]:
<a id="f037"></a>

- **[F037](#f037) [documented annotation]:** SH17 distinguishes an item being on/off a person in its extended tags. An item-present box and worn/not-worn tag are therefore different label layers. The described schema does not by itself establish an explicit per-person owner-ID relation in crowded scenes; the released full annotations were not downloaded or audited here. Source [S015](SOURCES.md#s015).


## F038 — [documented method plus mathematical counterexample]:
<a id="f038"></a>

- **[F038](#f038) [documented method plus mathematical counterexample]:** Published overlap-based association is a concrete separate inference step. Intersection/PPE-area avoids small-object IoU dilution but cannot distinguish two containing person boxes: both yield one. More overlap does not imply physically nearer owner. Source [S016](SOURCES.md#s016) and own example [F044](#f044) below.


## F039 — [documented method]:
<a id="f039"></a>

- **[F039](#f039) [documented method]:** Another primary method first matches by nonzero maximal IoU and then classifies relative geometry, including a helmet held in a hand. Thus “PPE overlaps person” is expressly weaker than “person wears PPE.” Source [S017](SOURCES.md#s017).


## F040 — [dataset metadata]:
<a id="f040"></a>

- **[F040](#f040) [dataset metadata]:** SHEL5K adds person-with/without-helmet classes, demonstrating an alternative direct state annotation. Its version-4 landing page and paper report different label totals. This is a version/count discrepancy to resolve against actual files, not a reason to silently merge their totals. Sources [S018](SOURCES.md#s018)–[S019](SOURCES.md#s019).

No numerical model-performance result is adopted as a target, ranking, or transfer claim. Evidence here supports what needs to be measured; it does not establish performance on organizer cameras, respirators, LinQ, or this project.


## F041 — Evaluation unit and manifest
<a id="f041"></a>

The atomic unit is `(camera, clip, frame timestamp, GT person instance, PPE requirement)`; units below are person–PPE–frame opportunities. A person can be evaluable for helmet and unknown for respirator on the same frame. Preserve source resolution, resize transform, annotated ROI, completeness status and annotation version. If only sampled frames are annotated, explicitly call results frame-sample results; do not infer continuous-event recall.

Record **every GT person** in the declared ROI, including partially visible/truncated people, with an explicit bounded ignore region only when individual boxes/IDs cannot be reliably separated. Define visible-box versus amodal-box convention once. Mark unannotated areas separately. A dense crowd is not empty background. Do not let detector success define the GT population.


## F042 — Minimum schema
<a id="f042"></a>

| Entity | Required fields / semantics |
|---|---|
| Frame | camera/clip/frame/time; image width/height; exhaustively annotated ROI; incomplete/ignore regions; annotator/adjudication version |
| GT person | frame-local `person_id`, bbox, optional visible region; truncation/occlusion attributes; optional temporal track ID (not worker identity) |
| Relevant body region | head/face/torso as appropriate; bbox/keypoint if annotatable; `visibility = sufficient / insufficient / ambiguous`; reason = occluded/outside/too small/blur/view/annotation unresolved |
| GT PPE item | `ppe_id`, bbox/class; item visible confidence from annotation; `relation = worn / carried / nearby-unworn / relation-unknown`; physical holder optional and distinct from wearer |
| Relation edge | item ID → person ID + body region; owner-known flag; no forced assignment if ambiguity; distinguish item absent from owner unknown |
| Person state for requirement | `visible_worn / visible_absent / visibly_incorrect / unknown / not_applicable`; separate externally supplied requirement flag `required / not_required / unknown` |
| Prediction | predicted person ID/box/score; state and confidence; evidence item IDs/relations if system exposes them; abstain/failure reason; config/model/preprocess hashes |

“Visible absent” requires sufficient observation of the relevant expected area and no required PPE visible there. A failed PPE detector is never the annotation rule for absence. A hidden head with a helmet elsewhere is unknown for wearing state. Unknown PPE subtype can coexist with a visible covering. “Correctly worn” may need separate visible attributes; do not collapse all proper-use claims into a helmet-present label. A medical mask category cannot simply become a respirator. Physical fit, filter class, certification, hidden fastening and legal applicability remain unknown unless independently supplied.

`not_applicable` is not a negative state used to improve accuracy; it follows external requirements or scope. Keep its count. For unknown requirement, evaluate visual state if observable but do not assert violation compliance. Label `visibly_incorrect` only for an agreed visually checkable criterion. If those criteria are not supplied, retain descriptive evidence such as “held in hand” rather than inventing a legal violation.


## F043 — Separate tests
<a id="f043"></a>

1. **GT-person oracle diagnostic:** supply every GT person region, keeping original coordinates and neighboring context policy fixed, to the component under study. Depending on component, also supply GT relevant regions or GT PPE detections. Report separately exactly which signals are oracle. This answers conditional state/association ability, not worker-finding ability. Never mix GT crops and predicted crops under one name.
2. **Predicted-person chain:** run normal localization, PPE recognition, ownership/state rules on the unchanged images. Compare all outputs to all eligible GT people. This is the primary frame-level person-state result. A missed person remains a missed opportunity even if conditional classification on found people is perfect.
3. **Association diagnostic with GT objects:** hold person/PPE object boxes fixed, ask for wearer/relation edges. For models without explicit edges, report that this diagnostic is unavailable; use state tests and controlled counterexamples, rather than fabricate inferred edges from output labels.
4. **Matched-person diagnostic:** optionally report state confusion only for matched detections, accompanied by the exact matched fraction. It localizes errors; it is not full-chain recall.

An oracle improvement identifies a sensitivity to that component under replacement. It does not alone prove a production fix, because replacing crops changes input distributions and errors can interact.


## F044 — Association cases and explicit counterexamples
<a id="f044"></a>

These are proposed regression cases / mathematical examples, not measured dataset frequencies or claims that a particular model fails.

| Case | GT / expected test consequence |
|---|---|
| Helmet in hand | Item exists and may be assigned to holder for carrying; head-visible absent remains absent. Item AP can be perfect while wearing classification is wrong. |
| Neighbor’s helmet | A's helmet projects inside B's large person box. The worn relation stays A→helmet; B does not gain protection. Include both same-depth and foreground/background overlap. |
| Crowded scene | One item lies in two person boxes. Explicit owner or unknown edge; do not credit the same item as worn by both. Preserve all persons in state denominator. |
| Head occluded | Person box correct; head not assessable. State unknown, not no-helmet. A confident absent assertion is an unsupported-state assertion to audit. |
| Small distant person | Keep person and visibility reason in ledger; if head is visually assessable by GT, model’s size filter does not remove this opportunity. If not, keep GT unknown count. |
| Person missed | Observable GT absence without predicted person is an end-to-end FN; conditional classifier has no trial for it, and must disclose this coverage loss. |
| Wrong PPE type | Visible face covering but type not resolvable: subtype/respirator state unknown, not inferred compliant. |
| Duplicate person | At most one prediction matches each GT person; additional violating predictions are extra alarms unless explicitly ignored by an annotated region. |
| Empty scene | No GT people and a violating predicted person: FP in exhaustively labeled ROI. No recall denominator; report recall N/A, never 100%. |
| Temporal occlusion | A previous worn state does not annotate an invisible present frame as freshly observed worn. A temporal decision may be tested separately with a stated evidence horizon. |

**Exact overlap example:** person boxes P1=[0,0,100,200], P2=[40,0,140,200]; helmet H=[50,5,70,25]. H is contained in both. IOC(P1,H)=IOC(P2,H)=1; IoU(P1,H)=IoU(P2,H)=400/20000=0.02. All boxes can equal GT exactly, so object recognition/localization contains no ownership error. Yet either tie choice can be wrong for the true wearer, and assigning to both wrongly marks one unprotected person protected. Extra pose/context may help but cannot universally resolve a truly occluded owner.

**Object-AP invariance example:** take two GT persons, A worn and B visibly absent, and one GT worn helmet on A. Fix every object box/class/confidence exactly. Association X maps helmet→A and outputs correct states. Association Y maps helmet→B and reverses states. A detector evaluator receives identical boxes/classes/ranks for X and Y; its score cannot change. At person level Y produces a false absence on A and misses absence on B. This is a proof by identical evaluator inputs, not an experimentally measured AP value; exact AP aggregation in empty classes is delegated to W1_02.


## F045 — Matching independent of state
<a id="f045"></a>

Freeze a person matching IoU threshold `tau_person`, coordinate convention, tie rule and ROI policy on development data; no universal numerical threshold is justified here. One proposal is maximum-cardinality one-to-one matching over edges IoU≥tau, then maximum summed IoU, then stable IDs for ties. Match with person boxes independent of predicted PPE state. This prevents state labels from deciding which person is evaluated. Pin implementation/version and tiny expected-result fixtures before comparing models. A standard score-ordered detector matcher is another possible protocol; it answers a different ranking question and must be named separately.

Match predicted PPE objects to GT items by class and a declared object IoU protocol for the relation diagnostic. Count an edge correct only when both endpoint matches, required relation label, and GT wearer agree. A generic held-by relation does not satisfy worn-by. Distinguish no-item, wrong wearer, duplicate assignment, missed item and unknown GT owner. Ignore matches to GT-unknown ownership for correctness, but report how many were excluded. First match valid GT persons, then account for remaining predictions against explicit ignore regions; unknown-state GT persons are still real persons, not generic suppressing regions.


## F046 — Denominators, abstentions and empty cases
<a id="f046"></a>

Let `N_all` be all annotated GT person–PPE–frames in scope; partition once into `N_known` (observable, applicable state), `N_unknown`, `N_not_applicable` and declared ignored count. If requirement is unknown, visual-state eligibility and violation eligibility differ and both denominators must be retained. Below binary V/non-V applies only when the requirement and violation rule are fixed and GT is known.

Let `N_V` and `N_N` be known violating/nonviolating GT opportunities. Use a GT-anchored matrix with rows V/non-V/unknown and columns predicted V/non-V/abstain/missed-person; keep wrong localization and unmatched prediction counts alongside it. Unknown rows are not used as negative labels.

| Quantity | Numerator / denominator; interpretation |
|---|---|
| Person localization coverage | matched eligible GT persons / all eligible GT persons, independent of state; also report matched all-person / N_all |
| Decision coverage on known GT | matched GT-known opportunities receiving a determinate state / N_known; absent detection and abstention reduce this |
| GT observability fraction | N_known / N_all with scope caveats; this is annotation/data coverage, not model quality |
| Full-chain violation recall | correctly matched predicted V on GT V / N_V; all unmatched GT V and abstentions on V remain in denominator |
| Violation misses | split GT V into missed-person, predicted non-V, abstained, and correctly predicted V; these counts must sum to N_V |
| False violation on known non-V | matched predicted V on GT non-V / N_N; call it false-positive rate per known-negative opportunity, not precision |
| Adjudicable violation precision | TP_V / (TP_V + matched V on known non-V + unmatched V in exhaustively labeled ROI + duplicate V); additionally publish unknown/ignore assertions below |
| Unknown-state assertions | number predicted V/non-V on matched GT unknown, separately; their correctness is not established by pixels |
| Conditional state accuracy | correct determinate states / all matched known GT opportunities, counting abstain as not-correct; optional selective accuracy divides only by determinate predictions and MUST display coverage |
| Association correctness (GT objects) | correct wearer+relation edges / all GT edges with known wearer+relation; pair with predicted-edge precision and owner-unknown count |
| Complete association correctness | same endpoint/edge check with predicted boxes; missed person/item becomes a missed known edge |

Precision on unknown assertions is not silently scored as true or false. Publish total predicted V count reconciled as adjudicable TP + adjudicable FP + assertions on unknown GT + ignored/out-of-scope/incomplete-annotation outputs. The quoted adjudicable precision must display this last coverage count; it can look high if many alerts remain unresolved. If desired report pessimistic/optimistic bounds treating all unresolved alert assertions as incorrect/correct, explicitly labeled bounds, not estimates.

When denominator is zero report N/A and raw counts. Zero positives does not establish recall. Zero predictions with positives gives recall zero and precision N/A. Empty frames contribute unmatched false predictions but have no person-state recall trials. For incomplete annotation do not call unmatched predictions false positives; use a separate output bin pending review. “Unknown” from the model on known GT is abstention, never GT-unknown; a detector that abstains on all hard people receives low known-state coverage and full-chain recall.

Aggregate micro counts with camera/clip and PPE-specific results and a visibility/size/crowding breakdown. A macro average over cameras/classes, if used, must state treatment of zero denominators and weights. Do not treat adjacent person-frames as independent for confidence intervals; W1_13 owns uncertainty. Repeated video frames are repeated opportunities here, not unique workers or episodes. Frame-level precision is not delivered-alert precision and cannot replace W1_05/W1_06 event/exposure protocols.


## F047 — Why coverage must accompany an oracle score
<a id="f047"></a>

Own arithmetic example: 100 known GT person opportunities, 20 violating. A system detects 50 people including only 5 violating people and classifies all detected states correctly. Matched-person accuracy=50/50=100%; localization coverage=50/100=50%; full-chain violation recall=5/20=25%. The 15 missed violating people are not difficult samples to discard. A GT-person oracle can be 100/100 correct while the complete chain remains at 25% violation recall. This arithmetic illustrates denominator choice; it is not a model experiment or an acceptance goal.


## F048 — Suggested minimal evaluation deliverable and limits
<a id="f048"></a>

A reviewable person-PPE evaluation package should contain: frame/GT manifest with complete/unknown/ignore flags; person/item/relation annotations; predicted-person/state records; frozen matching and threshold config; GT-anchored confusion ledger; metrics with all raw counts/coverage; and a compact regression suite covering every [F044](#f044) case. Synthetic geometry fixtures test evaluator conformance; real annotated cases test visual inference. Passing synthetic fixtures says nothing about detector robustness.

For `violation_methods`, preserve conditional and full-chain metrics and require worn-vs-carried/neighbor ownership cases before interpreting object AP as safety performance. For `datasets`, check whether ownership edges, unknown body-region states and complete negative scenes actually exist; an object-box dataset can train/evaluate detection while needing additional relation/state GT. For `video_architecture`, preserve per-frame abstention and provenance so temporal state does not silently convert hidden evidence to confirmed compliance.

Unresolved inputs: organizer PPE taxonomy, required versus optional equipment by zone/activity, measurable visible proper-use criteria, camera visibility distribution, evaluation ROI and box convention, relation annotation availability, and official matching/alert evaluator. No threshold, required sample count, target performance, legal norm, LinQ API, or hardware performance is invented. This report chooses a measurement contract; it does not choose an architecture.



Local retrieval integrity (SHA-256, computed after download; not a model execution):
- `W1_03_SOURCES/BPASTS_2023_71_6_3833.pdf`: `3DE4C4805065530F4673933A7968D7B84021E9666065DF749965FB80D3B69C91`.
- `W1_03_SOURCES/2407.04590v1.html`: `6DEEFACD68FA330809B31E7FC9C6FE966CDFD1F5803FE318C7ED887581E8F1A5`.


# W1_04 — сохранённые подробные наблюдения

Происхождение: [W1_04](_WORK/W1_04.md); [snapshots и локальные fixtures](_WORK/W1_04_SOURCES/). Контекст доступа и выполнения:  Research date: 2026-10-23. Result for violation_methods / video_architecture. No organizer zone definition, camera data, calibration, target SDK or device execution was supplied. No acceptance threshold is established here.


## F049 — Decision in one paragraph
<a id="f049"></a>

Adopt an explicit **observable zone-membership contract before calling it physical danger-zone entry**. A polygon in a frame, a person's ground contact, and any part of their body entering a hazardous volume are different targets. Fix the polygon coordinate system, anchor definition, boundary inclusion, visibility/unknown policy and zone version. Keep raw per-frame membership separate from temporal confirmation and delivered alerts. A correct point-in-polygon implementation establishes conformance to that declared geometry; it does not establish physical hazard truth. For a floor-zone case, use independently annotated ground-contact/foot evidence where observable, and mark unresolved contacts unknown. Treat bottom-center of a detection box as an explicitly tested proxy rather than a physical fact. These are proposals, not supplied organizer rules.


## F050 — Documentation plus source inspection.
<a id="f050"></a>

**[F050](#f050) — Documentation plus source inspection.** OpenCV's `pointPolygonTest(contour, pt, false)` distinguishes interior (+1), exterior (-1), and edge/vertex (0); `true` returns signed distance to the nearest contour edge. Thus `r > 0` excludes boundary; `r >= 0` includes boundary. Distance is in the supplied coordinate units, e.g. pixels for pixel coordinates, not automatically metres. The frozen 4.12.0 header states the contract; `geometry.cpp` implements it [[S020](SOURCES.md#s020)]. In its integer branch lines 117–146 and floating branch 161–190, the implementation checks edge/vertex contact and uses odd/even crossing counts. Inspection is not execution. A single contour is not a shell-plus-holes data model: implement declared hole semantics separately or select a polygon API supporting holes.


## F051 — Documentation.
<a id="f051"></a>

**[F051](#f051) — Documentation.** For a point, Shapely 2.1.2 `contains(zone, point)` excludes the boundary, whereas `covers(zone, point)` includes it [[S021](SOURCES.md#s021), [S022](SOURCES.md#s022)]. Do not generalize this into “contains always excludes every boundary contact of an arbitrary second geometry”: a line with endpoints on the polygon boundary can still be contained when its interior lies inside. `contains(zone, zone)` is true. A footprint predicate must be specified independently from a point predicate. Missing inputs can return false, so validate missingness before interpreting booleans as outside.


## F052 — Source inspection, failure case.
<a id="f052"></a>

**[F052](#f052) — Source inspection, failure case.** In OpenCV 4.12.0 `geometry.cpp` lines 103–112, contour vector shape and depth are asserted, and an accepted zero-length contour returns -1, or -DBL_MAX with distance enabled [[S020](SOURCES.md#s020)]. The numeric answer must not silently turn a missing zone into normal “outside.” Reject invalid/missing zone configuration upstream. There is no user-selected geometric tolerance in this API; floating comparisons and coordinate precision are part of behavior. Source inspection found no general polygon validity certification in this function. Reject self-intersecting/degenerate input through the application's validity contract instead of treating a numeric result as approval of geometry.


## F053 — Documentation.
<a id="f053"></a>

**[F053](#f053) — Documentation.** Shapely analysis is planar; supplied z values do not create 3D collision tests. Construction does not generally validate topology, and invalid rings may give errors or wrong results in subsequent operations [[S023](SOURCES.md#s023)]. A 2D polygon even with xyz vertices is insufficient to prove body intrusion into a 3D hazardous volume.


## F054 — Documentation and mathematical implication.
<a id="f054"></a>

**[F054](#f054) — Documentation and mathematical implication.** OpenCV's homography tutorial describes a plane-to-plane projective map, with 8 degrees of freedom; its planar-pose example uses coplanar points and undistorted/normalized image observations [[S024](SOURCES.md#s024)]. Its pure-rotation example is a special case and does not justify one global warp for arbitrary translated views of a scene with varying depths. Consequently a ground-plane map applies to floor contacts on that plane, not a person's head or a platform at another height. Lens distortion and camera-coordinate preprocessing must be accounted for consistently. A physical metric scale must come from known world coordinates or another justified measurement, not the appearance of a rectangle.


## F055 — Documentation.
<a id="f055"></a>

**[F055](#f055) — Documentation.** OpenCV calibration's pinhole model uses camera intrinsics and pose; resolution changes require corresponding intrinsic scaling. Real lens distortion adds parameters. `findHomography` documents robust estimation from four-pair subsets while discarding collinear subsets, an inlier reprojection threshold in the destination coordinate units, and an empty result when estimation fails [[S025](SOURCES.md#s025)]. RANSAC inlier status is agreement with an estimated transform, not a certificate that control points belong to the floor or that the physical boundary is correct. Default API constants are not safety acceptance thresholds.


## F056 — Alternative truth contracts: choose one, do not average them
<a id="f056"></a>

All rows below are proposed task specifications, requiring task-owner agreement when a real case arrives.

| Contract | What is positive | GT evidence | What it does not establish |
|---|---|---|---|
| Image anchor membership | Declared image point belongs to polygon using declared boundary rule | Human-annotated point or exactly declared box-anchor derivation, zone polygon in same image coordinates | Physical body or floor location without further justification |
| Image extent overlap | `area(person_extent ∩ zone) > 0`, or a declared ratio/comparison | Polygon/mask or box with declared meaning | Ground entry: body projects above floor, box contains background |
| Floor contact / support footprint | Either foot contact, both feet, midpoint, or footprint intersects floor zone — one explicitly chosen | Observable contacts and calibrated plane/world boundary, or image projection of a verified floor boundary | Head/hand intrusion, elevated decks, airborne bodies |
| Physical body intrusion | A specified body surface/volume intersects specified 3D hazard volume | Suitable calibrated multi-view/depth/3D measurements and hazard geometry; visibility limitations recorded | Cannot be supplied merely by 2D overlap or a ground homography |

Even within floor membership, “either foot in” and “midpoint in” disagree for a straddling person. A visible foot is not necessarily a ground contact while walking or climbing. Polygon-only annotations on an image may define a useful visual rule even when no metric calibration is available; label that claim honestly. In an ideal distortion-corrected planar model, testing a true floor point against the exact projected floor polygon can give the same membership without constructing a metric bird's-eye view. Homography is necessary for the chosen measurement only when that measurement needs it; perspective alone does not invalidate a correctly projected planar membership rule. Pixel distance or area-ratio thresholds nevertheless have location-dependent physical meanings.

For overlap ratios, state the denominator. `area(person∩zone)/area(person)` answers how much of the person extent is covered; IoU divides by the union. A fully in-zone small person box can have low IoU with a very large zone. The `intersects` predicate includes boundary-only contact; positive intersection area does not. Changing between these rules changes GT, not just tuning.


## F057 — Proposed record schema and state semantics
<a id="f057"></a>

Zone record: `camera_id, zone_id, zone_version, valid_from, valid_to, reference_frame_id/hash, reference_width/height, coordinate_space(raw/distortion_corrected/model_input/world_plane), axes_origin, units, outer_ring, holes, polygon_validity, boundary_policy, physical_meaning, calibration_id, transform_chain, calibration_validity_interval, geometry_owner/evidence`.

Person observation: `video_id, source_frame_id, source_timestamp/timebase, gt_person_id, zone_version, anchor_kind, anchor_xy_or_footprint, anchor_source, visibility, localization_uncertainty, membership(interior/boundary/exterior/unknown), unknown_reason`. Keep prediction source separately (`predicted_box_bottom_center`, detected footpoint etc.). Never turn interpolated/predicted hidden feet into independently observed GT.

Proposed anchor for a box is `( (xmin+xmax)/2, ymax )` in a continuous coordinate convention. If xmax/ymax are exclusive integer bounds, whether the anchor is on the outside edge or last pixel centre must be resolved before using this formula. Store `xyxy` versus `xywh`, normalized versus pixel coordinates, axis orientation, resize scales, crop/letterbox offsets, rotation and inverse transformation. The image point and zone must be in the same space and zone version; normalized coordinates alone do not fix a crop mismatch.

Temporal states: membership state first; episode/entry second. `outside → inside` on observed valid samples can support observed entry. First appearance already inside is left-censored occupancy, not proven entry at that timestamp. `outside → unknown → inside` bounds entry to an interval rather than establishing an exact onset. `inside → unknown` does not establish exit. Two outside endpoints with a line segment crossing the polygon are not proof of actual entry unless an explicit motion/interpolation assumption is adopted. Dropped/low-rate frames can miss rapid entry and exit entirely. Temporal persistence, cooldown, tracking continuity and delivered deduplication belong to the event contract and must retain the source membership evidence.


## F058 — Exact geometry fixtures and counterexamples
<a id="f058"></a>

These expected answers are analytical acceptance fixtures to run against the selected library/runtime later. They are not measured OpenCV/Shapely conformance results. A small **own Python 3.11.9 mathematical calculation** produced the six square signed distances and height example in `W1_04_SOURCES/analytical_examples.json`. Neither OpenCV nor Shapely is installed in this environment, so no execution claim for those libraries is made.

For square Z = [(0,0),(10,0),(10,10),(0,10)], continuous units:

| Point | signed distance | strict interior | closed membership |
|---|---:|---|---|
| (5,5) | +5 | true | true |
| (-1,5) | -1 | false | false |
| (0,5) edge | 0 | false | true |
| (0,0) vertex | 0 | false | true |
| (0.000001,5) | +0.000001 | true | true |
| (-0.000001,5) | -0.000001 | false | false |

Required extensions: same answers after reversing vertex order; implicit last-to-first edge versus explicit closure; horizontal/slanted edges and each vertex; concave notch interior/exterior; hole interior (outside), hole edge (boundary), adjacent zones sharing edge (closed membership can assign both; strict can assign neither). Reject nonfinite point, null/empty point, empty zone, zero-area ring, self-intersection, duplicate collapse and unsupported coordinate precision according to an explicit error/unknown path. Do not assume these invalid configurations all behave identically across APIs. A unique-zone use case needs a separate overlap/priority policy; independent hazard zones may legitimately both apply.

Partial-overlap fixture: person box B = [9,-5,13,5], square Z above. B intersects Z in area 5, while B area is 40, fraction is 0.125, union is 135 and IoU is 5/135. Bottom centre (11,5) is outside. `intersects`, positive area, midpoint membership and ratio thresholds can therefore disagree on the very same perfect detection. A box touching only x=10 can intersect Z with zero common area. Test all stated comparators, including exact equality to any configured ratio threshold.

Perspective/height counterexample (own analytic geometry, not camera measurement): camera centre C=(0,0,4) metres, elevated point P=(3,0,z). Its image ray, falsely intersected with ground z=0, yields X=3*4/(4-z): X=3 for z=0, X=4 for z=1, X=6 for z=2. A point elevated above an outside ground position can be falsely placed inside a floor zone [5,7] metres. This happens with perfect pixels and exact calibration; more accurate detection cannot repair an inappropriate plane assumption.

Other mandatory regressions: (a) torso overlaps floor polygon while feet remain outside; (b) one foot inside but midpoint outside; (c) feet hidden by machine, box ends at occluder; (d) box clipped by image edge; (e) crouching/leaning changes bottom-centre; (f) worker on ramp/stairs/platform; (g) shadow/reflection inside zone; (h) camera pan/tilt/zoom/vibration with a static old zone; (i) resize/letterbox/crop and distortion mismatch; (j) stopped worker near boundary with predicted anchors alternating either side; (k) physical zone moves with a machine; (l) wrong floor control-point correspondences giving a plausible-looking warp.


## F059 — Uncertainty, motion and proposed validation layers
<a id="f059"></a>

Do not hide boundary uncertainty by silently rounding points or expanding polygons. Proposed static uncertainty contract: if the possible anchor region U is wholly in the selected zone, inside; if U is disjoint, outside; otherwise uncertain. This makes a bound's source essential: annotator disagreement, image localisation, calibration residuals and drift are not one interchangeable number. A metric uncertainty bound requires metric validation. A pixel uncertainty band is not a universal metre margin. If a signed-distance band `|d| <= delta` is used, record delta's units, choice on development evidence and boundary-band denominator. It changes the decision contract and does not create a new observable physical truth.

Proposed hysteresis is a **temporal policy**, e.g. confirm inside beyond a declared inward band and confirm outside beyond a declared outward band, retain/unknown in between. Record initial state and handling of unknown, camera discontinuity and track restart. Temporal smoothing can reduce jitter alerts while delaying or suppressing short true entries. Evaluate that tradeoff at the event level, not only as smoother visual tracks. No band width, dwell duration or cooldown is selected here.

For camera movement, version/invalidate the image polygon or calibration whenever its validity no longer holds. Re-registration can use a verified floor plane; generic background homography can follow the wrong depth layer. A stable-looking overlay on one landmark is insufficient validation across the whole monitored floor. Camera-motion detector, drift criterion and fallback behavior remain unspecified until footage and deployment constraints exist.

Separate four validation layers:

1. **Geometry code conformance:** run deterministic fixtures including edge equality, holes, invalid inputs, coordinate conversions and serialization/export parity. Report correct cases / applicable fixtures and failure identities; test count is not video accuracy.
2. **Calibration/site validation:** independent surveyed/known floor checkpoints not reused to fit H, spread near actual zone boundaries and operational depth range. Report Euclidean world-coordinate error in metres when world GT is metric; for projected controls use pixels. State count, error distribution, fitting vs held-out split, outlier treatment, spatial coverage and calibration timestamp/version. Reprojection training residual alone is insufficient. Degenerate placement, unknown floor shape and extrapolation remain risks. No universal acceptable error follows from docs.
3. **Oracle-person geometry evaluation:** independently annotated GT anchors/contacts, GT zone and visibility. Count membership confusion on valid GT person-zone observations; provide per-zone/camera strata and boundary/occlusion strata. No person matching needed when geometry receives GT identities/anchors. This isolates geometry assumptions; it cannot measure missing people.
4. **Full chain and events:** use a declared one-to-one person matching rule and report matched-state performance plus missed GT persons and unmatched predicted persons. An inside GT person without a prediction remains a full-chain miss. Delivered false alerts, repeated boundary oscillations, entry interval and delay require the temporal/event protocol. Do not report layer 3 as complete layer 4 quality.

Proposed membership recall = correctly classified inside GT observations / all evaluable inside GT observations; precision = correct inside predictions / all evaluable inside predictions under the declared person matching and boundary mapping. Aggregate counts before micro ratios, and optionally camera-macro separately. GT boundary is either explicitly included, excluded, or a third class; choose before scoring. Unknown GT cases are excluded from binary truth denominators but counted with reasons and coverage. Prediction abstentions on known inside GT are not successful detections: either count as misses in full-chain recall or report selective recall alongside nonselective recall. Evaluable coverage = count of known GT membership person-zone observations / all annotated person-zone observations; retain unknown counts. With irregular sampling also report time-weighted coverage using declared source-time support, so high frame rate does not masquerade as longer observation. Empty denominators are undefined/NA with raw counts, not automatically 100%. A no-positive clip can still contribute false positives and exposure; geometry fixture pass rates have no statistical hazard-safety interpretation.


## F060 — Unresolved inputs and downstream decisions
<a id="f060"></a>

Needed from actual case: floor region versus body volume; any foot versus midpoint versus body intersection; boundary is hazardous or excluded; zone owner and physical evidence; camera movement and optics; floor planarity and units; GT treatment of hidden feet; frame cadence/drop policy; source timestamps; allowable uncertainty/alert workload and task-specific acceptance owner. These remain localized unknowns, not reasons to invent norms. Transfer to violation_methods: retain alternative anchors and difficult people, declare boundary and unknown mapping. Transfer to video_architecture: preserve source-frame coordinates/timestamps, preprocessing inverses, zone/calibration versions and validity discontinuities; expose raw state separately from event/alert state.


# W1_05 — сохранённые подробные наблюдения

Происхождение: [W1_05](_WORK/W1_05.md); [snapshots и локальные fixtures](_WORK/W1_05_SOURCES/). Контекст доступа и выполнения:  Prepared 2026-10-23, Europe/Moscow (UTC+03:00). Scope: reproducible evaluation choices for industrial safety video; no organizer evaluator, full case, event taxonomy, hardware or measured model outputs were supplied. Sources and small examples are in `W1_05_SOURCES/`. This is a proposed local evaluation contract, not a claim about competition scoring.


**Уточнение сборки:** точные eligibility/assignment/censoring уточнены [F005](#f005), [F006](#f006). Common-TP formulas применяются лишь в shared closed universe; boundary source/onset cohorts см. [F003](#f003).


## F061 — Own inference from inspected sources:
<a id="f061"></a>

**[F061](#f061) — Own inference from inspected sources:** report segment quality and useful delivered alerts separately. A segment can overlap an episode almost perfectly yet start too late to be useful; an immediate, correct notification can have tiny segment overlap. “Event F1” is insufficiently specified without eligibility, temporal rule, assignment, duplicate treatment, operating point and censoring. A detector AP improvement does not establish a reduction in operator interruptions.

Recommended minimal outputs: (1) optional temporal segment AP/tIoU diagnostics, (2) one-to-one timely delivered-alert precision/recall with explicit deadline, (3) latency distribution and late/missed counts, (4) delivered duplicate count and false alerts per evaluated camera-hour, with coverage from W1_06/W1_12. Do not import audio-benchmark collars or tIoU thresholds as industrial acceptance targets.


## F062 — Source-code inspection, ActivityNet:
<a id="f062"></a>

**[F062](#f062) — Source-code inspection, ActivityNet:** `compute_average_precision_detection` sorts each class's predictions by decreasing score, then considers GT in the same video by descending tIoU. Each GT is locked once per threshold; a prediction uses at most one unlocked eligible GT. Remaining predictions are FP. This is score-ordered greedy assignment, not globally optimal bipartite assignment. Equality to the threshold passes. Recall is cumulative TP / class GT count; precision is cumulative TP / cumulative predictions. Wrapper macro-averages AP over GT-derived classes and then thresholds (default ten thresholds 0.50–0.95). No predictions returns AP zero. Label vocabulary comes from GT subset; an unknown prediction label triggers mapping failure. Same class, wrong person is not distinguishable by these fields. [Pinned evaluator](https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/eval_detection.py#L182) [[S026](SOURCES.md#s026)].


## F063 — Source-code inspection, ActivityNet utility:
<a id="f063"></a>

**[F063](#f063) — Source-code inspection, ActivityNet utility:** tIoU is intersection duration / union duration, where intersection is clamped to zero. It is unitless if all timestamps use the same unit; use seconds in our schema. AP integrates a monotonic precision envelope at recall changes. Thus two identical predictions for one GT produce TP then FP, but AP can remain 1.0: the extra FP arrives after recall has already reached 1.0. A single AP number therefore need not expose duplicate burden. These formulas assume positive, valid interval durations; point alerts should not be represented as zero-duration segments and passed to this metric. [Pinned utilities](https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/utils.py#L14) [[S027](SOURCES.md#s027)].


## F064 — Source-code inspection, sed_eval:
<a id="f064"></a>

**[F064](#f064) — Source-code inspection, sed_eval:** collar validity uses `abs(pred_onset - ref_onset) <= t_collar`; offset validity uses `abs(pred_offset - ref_offset) <= max(t_collar, percentage_of_length * reference_duration)`. Default onset and offset checks are enabled, collar 0.2 seconds, relative offset tolerance 0.5. `optimal` forms same-label valid edges and performs one-to-one matching; `greedy` is retained. Each file is evaluated separately, and counts accumulate. Classwise FP = Nsys − Ntp; FN = Nref − Ntp. Overall error-rate accounting also separates substitutions, so its FP/FN fields should not be silently treated as classwise unmatched counts. [Pinned source](https://github.com/TUT-ARG/sed_eval/blob/0cb1b6d11ceec4fe500cc9b31079c9d8666ed6eb/sed_eval/sound_event.py#L1108) [[S028](SOURCES.md#s028)].


## F065 — Source-code inspection and documentation:
<a id="f065"></a>

**[F065](#f065) — Source-code inspection and documentation:** sed_eval's utility implements maximum-cardinality bipartite matching, not “first eligible” matching; tied maximum matchings need not minimize delay. Documentation explicitly warns that greedy matching can depend on GT order. The metric helpers return NaN precision when Nsys=0 and NaN recall when Nref=0; `empty_system_output_handling='zero_score'` can override empty-system precision. Record and report empty strata rather than silently averaging only defined scores. [Matching code](https://github.com/TUT-ARG/sed_eval/blob/0cb1b6d11ceec4fe500cc9b31079c9d8666ed6eb/sed_eval/util/event_matching.py#L7), [metric helpers](https://github.com/TUT-ARG/sed_eval/blob/0cb1b6d11ceec4fe500cc9b31079c9d8666ed6eb/sed_eval/metric.py#L31), [API docs](https://tut-arg.github.io/sed_eval/generated/sed_eval.sound_event.EventBasedMetrics.html) [[S029](SOURCES.md#s029)/[S030](SOURCES.md#s030)/[S031](SOURCES.md#s031)].


## F066 — Official benchmark documentation:
<a id="f066"></a>

**[F066](#f066) — Official benchmark documentation:** DCASE is not one fixed temporal rule. DCASE 2017 Task 2 specifies onset-only evaluation with 0.5-second collar; DCASE 2020 Task 4 specifies 0.2-second onset and max(0.2 seconds, 20% of reference duration) offset collars. These differ from the library's default 50% offset tolerance. A symmetric onset collar accepts a prediction slightly before reference onset; that is boundary agreement, not automatically a valid causal early warning. [2017 evaluation settings](https://dcase.community/challenge2017/download), [2020 evaluation](https://dcase.community/challenge2020/task-sound-event-detection-and-separation-in-domestic-environments) [[S032](SOURCES.md#s032)/[S033](SOURCES.md#s033)].


## F067 — Published methodological counterexample:
<a id="f067"></a>

**[F067](#f067) — Published methodological counterexample:** Ferroni et al. compare collars, fixed-size segments and PSDS intersection rules. Fixed bins can collapse several short events or overweight long events; intersection criteria intentionally permit some interrupted and merged detections. This supports choosing a metric for the question, not assuming all “event” rules are equivalent. The paper's audio results do not establish industrial safety alert thresholds. [Paper, sections 2.1 and 3](https://arxiv.org/html/2010.13648v1) [[S034](SOURCES.md#s034)].


## F068 — Additional code inspection, applicability failure:
<a id="f068"></a>

**[F068](#f068) — Additional code inspection, applicability failure:** archived PSDS code sums same-class intersection fractions per detection for DTC, then GT coverage from qualifying detections for GTC; it drops duplicate GT IDs before final TP counting. This can credit one detection spanning several GT episodes or several fragments covering one GT. It is intentionally different from one notification per independently actionable episode. Repository now resolves at j-bernardi; old audioanalytic Git endpoint failed. This snapshot is supporting historical code, not asserted as the current official DCASE evaluator. [Pinned PSDS code](https://github.com/j-bernardi/psds_eval/blob/20896ee131922f4b5f8733a8c6c4a079f3827b92/src/psds_eval/psds.py#L237) [[S035](SOURCES.md#s035)].


## F069 — Locally executed small examples, not model measurements.
<a id="f069"></a>

**[F069](#f069) — Locally executed small examples, not model measurements.** `small_examples.py` extracts and executes only the pinned sed_eval onset/offset validators and its bipartite matching function; tIoU is our scalar formula. Full evaluators were not run. JSON results are preserved. Seconds throughout. Illustrative settings: tIoU ≥0.5; collar onset 0.2 s, offset max(0.2 s, 20% GT length); all labels/keys agree. These settings are examples, not acceptance targets.

| GT / prediction | tIoU outcome | Onset + offset collar outcome | Notification interpretation under proposed D=5 s example |
|---|---|---|---|
| GT [10,110], prediction [15,110] | 0.95, TP | onset fails, offset passes → no match | delivery at 15 is timely exactly at D; D<5 would fail despite excellent tIoU |
| GT [10,20], prediction [10,11] | 0.10, no match | onset passes, offset fails → no match | delivery at 10 can be a useful TP without predicting full duration |
| GT [10,20], fragments [10,15] and [15,20] | each 0.50; one TP + one FP under one-to-one | neither passes both boundaries → 0 TP, 2 FP, 1 FN | deliveries at 10 and 15: one TP and one duplicate, P=1/2, R=1 |
| GT [10,14] and [16,20], merged prediction [10,20] | 0.40 against each → 0 TP | neither passes both boundaries | single delivery at 10: 1 TP, 1 FN; no notification of second entry |

The merged example would pass DTC=0.5 and GTC=0.5 in the inspected PSDS criterion: 8/10 detection coverage and 4/4 coverage of each GT. That arithmetic is our inference from code, not an executed PSDS result. Split fragments covering all of one GT likewise illustrate why coverage and notification multiplicity differ.


## F070 — Executed assignment ambiguity:
<a id="f070"></a>

**[F070](#f070) — Executed assignment ambiguity:** GT onsets 10.0, 10.3; predicted onsets 10.15, 9.85; collar 0.2 s. First prediction has edges to both GT, second only to first. First-found assignment can obtain one match; executed maximum-cardinality matching obtains two (prediction 9.85 → GT 10.0; prediction 10.15 → GT 10.3). Confidence ranking, chronological greedy and global assignment must not be conflated. Retain stable IDs and explicit tie policy in a local alert evaluator.


## F071 — Mathematical AP duplicate example:
<a id="f071"></a>

**[F071](#f071) — Mathematical AP duplicate example:** one GT [10,20], exact predictions with scores .9 and .8. Ranked precision is 1 then 1/2; recall is 1 then 1. The interpolated AP is 1, whereas delivered-alert precision is 1/2 if both notifications reach the operator. This example is analytically derived, not execution of the old ActivityNet evaluator.


## F072 — Proposed industrial alert contract (F072; own proposal)
<a id="f072"></a>

The contract below is for useful delivered notifications. Freeze its parameters before test; organizer rules, if supplied, remain a separate result.

1. **GT episode:** `episode_id, camera_id, violation_type, person_instance_id (or explicit identity-unavailable), zone_id if relevant, observable_start, observable_end, onset_status, offset_status, onset_uncertainty, evaluated_support, annotation_version`. Use half-open state intervals [start,end). Define what makes two episodes distinct: e.g. observed safe exit/reset followed by a new entry. A gap caused by an occlusion is not automatically a safe reset. Distinguish actual continued violation from inability to observe it; this requires truth policy from W1_01/W1_04/W1_09.
2. **Raw candidate versus delivered alert:** retain `candidate_id`, evidence frame timestamp, predicted support interval, confidence, confirmation timestamp, `logical_alert_id`, delivery attempt ID, delivery timestamp/status and stream epoch. Candidate suppression, logical alert creation, transport retries and UI delivery are different layers. Count every actual extra operator interruption in workload; retries collapsed idempotently into one visible notification remain one delivery, with retry logs retained. Candidate-only metrics must be named accordingly.
3. **Compatible keys:** same camera, violation, zone and correct person when the task is person-specific. Matching by model track ID alone is invalid; track IDs can switch. If person correspondence cannot be annotated, report a separately named scene/zone alert result, not person-alert precision. For zone-wide alerts about simultaneous people, define an actionable group GT beforehand.
4. **Timely edge:** alert delivered at `t_delivery` is eligible for episode g when `0 <= t_delivery - observable_start(g) <= D_type` and delivery occurs while the episode is observably active (end boundary excluded). Deadline D is an explicit application requirement, currently unknown. Any allowed pre-onset tolerance for annotation uncertainty must be separately declared; it should not silently authorize predicting future violations. A warning-after-episode policy, if wanted, needs another named rule. For uncertain onset intervals, report bounded delay/sensitivity rather than falsely precise latency.
5. **Assignment:** maximize number of eligible one-to-one pairs; among equally large matchings minimize total nonnegative delay, then resolve ties by stable episode/alert IDs. This is our deterministic offline proposal. It is not ActivityNet's greedy rule or sed_eval's latency objective. Never allow one delivery to clear several independently actionable GT episodes. For audit, save eligibility edges, final pair list and reason for each unmatched item.
6. **Count:** TP = matched delivered alerts; FN = eligible, fully evaluable GT − TP; FP = unmatched evaluable delivered alerts. `P=TP/(TP+FP)`, `R=TP/(TP+FN)`, `F1=2TP/(2TP+FP+FN)`. Decompose unmatched deliveries: duplicate of already notified episode, correct-but-late, wrong person/type/zone, no GT, uncertain/unreviewed. Late is outside timely TP and therefore contributes FP plus an unmatched GT FN in this strict endpoint; also report eventual episode detection separately so the interpretation is clear. Duplicate is an FP subtype, never an extra TP. Unknown/ignored deliveries are counted separately and do not establish correctness.
7. **Aggregation:** sum counts over evaluated streams for micro P/R/F1; report per violation, camera and duration stratum as well as any explicitly defined macro average. GT episode is recall unit, delivered alert is precision unit. Units of delay are seconds; ratio scores unitless (or percent, clearly marked). Empty denominators → undefined with raw counts; do not call all-negative empty clips perfect recall. All-negative fully reviewed clips still contribute unmatched alerts/workload/exposure. No duration/threshold averaging without specifying weights.
8. **Latency:** report every eligible episode's timely/missed status alongside TP delay quantiles and number of samples. Quantiles among detected episodes alone can improve when slow episodes are missed. Retain confidence-threshold and temporal-policy configuration (dwell, smoothing, exit hysteresis, gap tolerance, cooldown, rearm rule), versions and timestamps. Choose these on development data; test output is locked.


## F073 — Episode lifecycle, cooldown and censoring (F073; own proposal)
<a id="f073"></a>

**Repeated entry and cooldown:** GT [10,14] then [16,20] are two episodes if a qualifying safe exit is observed. A 10-second cooldown suppressing the second delivery produces FN under that task. Do not merge GT to fit the cooldown. Conversely, if state stays unsafe through a short occlusion and only a tracker ID changes, a re-alert is a duplicate, not a new GT. Scope cooldown to defined keys; a scene-wide cooldown can suppress another worker's new violation. Reminders/escalations need a separate output type and utility endpoint; retain them in the delivered interruption count even when the product intentionally requests them.

**Left censoring/pre-existing episodes:** observation starts at 0 while actual episode began at −10. Annotate `onset_status=pre_existing_or_unknown` and observable unsafe state at 0. Do not label 0 as true onset or claim ten-second physical-onset latency. Measure a separate startup/pre-existing-state notification endpoint from first sufficient observable evidence. Segment metrics on the clipped [0,30] support can be perfect yet physical onset detection remains unknowable.

**Right censoring:** GT begins at 28, file stops at 30, D=5 s. A run ending at 30 cannot demonstrate what would be delivered by 33. Mark deadline-followup incomplete and report count; do not automatically call no alert a full-window miss. If delivered at 29, observed timely success is known, but mixing such successes with excluded no-alert cases biases recall. Primary complete-window recall should exclude the entire right-censored eligibility stratum consistently, and report its partial observations separately. A separate “detected before recording end” endpoint can score all such episodes with its shorter opportunity explicitly named. Prefer longer continuous recordings when possible.

**Unobservability, cut clips and reconnects:** unknown video intervals and delivery-outage intervals are distinct. A hidden unsafe person is not evidence of a safe exit. Store episode continuation ID across adjacent cuts; avoid double-counting one episode in two clips. Reconnect creates a stream epoch and possible left-censored state; do not fabricate onset. For segmentation scoring, visible GT may be clipped to evaluated support, but original censor flags persist and onset/offset localization results exclude unknown boundaries. Fully observed early episode endings are real task conditions, not censoring; our active-episode delivery criterion intentionally gives them less response opportunity.

**Four clocks:** physical true onset may precede observable sign; first observable sign precedes or coincides with sufficient annotation evidence; algorithm confirmation after dwell is an algorithm timestamp; delivery is when notification becomes available at the defined receiving boundary. Example: physical 8, observable 10, confirmation 12, delivery 15 → observable-to-delivery 5 s, confirmation-to-delivery 3 s, physical-to-delivery 7 s only if physical onset is independently known. Backdating prediction start to 10 does not make a delivery at 15 instantaneous. Clock-domain reconciliation belongs to W1_11.


# W1_06 — сохранённые подробные наблюдения

Происхождение: [W1_06](_WORK/W1_06.md); [snapshots и локальные fixtures](_WORK/W1_06_SOURCES/). Контекст доступа и выполнения:  Research date: 2026-10-23; access timezone UTC (Moscow = UTC+03:00). Scope: evaluation design for industrial safety video analytics, not measured performance of any model or LinQ. No organizer evaluator, continuous deployment data, delivered-alert log, or annotation contract was supplied. No acceptance threshold is inferred. This cell proposes a protocol and gives mathematical examples, not an operational workload guarantee.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F074 — Decision supported
<a id="f074"></a>

A defensible workload statement needs the count of actually delivered notifications, their adjudicated status, and the camera-time over which those notifications could have occurred and been evaluated. “Zero false alerts” without duration, coverage, review status, fixed configuration, and population is not a rate claim. Reviewing only alert clips can establish alert correctness on those clips; it cannot establish missed-event recall. A long quiet-camera recording is weak evidence for a busy unseen camera even when the arithmetic camera-hours is large.

Evidence labels below: **DOC** = primary documentation/paper; **DERIVATION** = mathematical consequence under stated model; **PROPOSAL** = our evaluation rule, not an existing benchmark requirement; **LOCAL MATH** = arithmetic executed locally without video/model; **UNKNOWN** = missing task evidence. No evaluator code was inspected or executed in this cell.


## F075 — DOC, S036.
<a id="f075"></a>

**[F075](#f075) / DOC, [S036](SOURCES.md#s036).** TRECVid 2008 uses spurious event observations divided by processed camera-hours (section 2.4.2). It explains why an ordinary true-negative event count is problematic for events with arbitrary onset and duration. Its data comprise five synchronized cameras over multiple days (section 2.2), and its retrospective task allows multiple video passes (section 2.1.1). Thus this is a relevant continuous-surveillance precedent for an exposure denominator, but does not certify live delivery, latency, current industrial event truth, or our chosen duplicate rules. The source itself warns that camera-hour false-alarm rate differs from a Type-I error probability because target observations are included in the denominator.


## F076 — DOC, S037–S038.
<a id="f076"></a>

**[F076](#f076) / DOC, [S037](SOURCES.md#s037)–[S038](SOURCES.md#s038).** NIST's constant HPP/exponential model estimates occurrence rate by count / total operating time, and supplies a zero-failure one-sided bound. Scholz derives exact conservative Poisson mean bounds by inverting tail probabilities; the zero-count 95% upper mean is 2.995732. These are model-conditional statistical results, not evidence that video false notifications follow that model.


## F077 — DOC, S039.
<a id="f077"></a>

**[F077](#f077) / DOC, [S039](SOURCES.md#s039).** FDA guidance section 4.1 explains verification bias when reference-standard review is partial, and that naive full-verification formulas need not apply. Its scope is diagnostic studies, not surveillance rules. Its transferable lesson is to declare review sampling and adjust estimation, rather than silently treating unreviewed material as negative. Sections 5 and 7 distinguish agreement with an imperfect comparator from correctness. This does not authorize adopting medical sample-size or regulatory rules here.

**Counterexample search result / retrieval limitation.** NIST ActEV21 search results describe a time-based false-alarm measure, unlike counts of delivered notifications. Actual page opening twice timed out, and an attempted full NIST report open exceeded the web tool's content limit; direct retrieval returned 403. These snippets are leads, not verified evidence for an exact ActEV metric. Do not import its formula or ranking threshold from this cell. The conceptual distinction below is our definition, independent of that inaccessible source.


## F078 — PROPOSAL — Units and exposure ledger
<a id="f078"></a>

For each fixed run/configuration and event class, record non-overlapping time intervals with camera ID, source timestamps, schedule/eligibility, successful analysis status, truth review status, observability, and declared boundary handling. An hour means 3,600 seconds of source camera timeline; it is not an hour of fast offline computation, frame count / nominal FPS when timestamps are irregular, or wall-clock duration shared by several cameras. Two cameras each supplying one hour give two camera-hours. Replaying the same hour ten times gives repeated execution evidence but not ten independent hours of scene evidence.

Maintain distinct durations, all in camera-hours:

| Quantity | Definition and use |
|---|---|
| H_scheduled | Eligible scheduled source camera-time, with exclusions fixed before evaluating outputs. |
| H_analyzed | Camera-time actually processed under the frozen policy, including normal configured temporal sampling. Outage gaps are excluded here and reported separately. |
| H_reviewed | Source time with adequate reference review for the requested metric. Review only near alerts is not exhaustive event annotation. |
| H_eval | Intersection of eligible, analyzed and adequately reviewed/observable time for that metric. Union interval lengths within each camera before summing across cameras. |
| H_unknown | Time for which event truth cannot be adjudicated or review is incomplete; report reasons and overlap, rather than assuming it is safe time. |

Always report H_analyzed / H_scheduled and H_eval / H_scheduled with the rate. Do not add H_unknown blindly to H_eval: intervals and causes can overlap. Report configuration (detector, model hash, input rate/resolution, thresholds, zone and temporal rules, cooldown, tracker, delivery retries) and per-camera/shift durations. Fixed sampling is part of the tested service; a low frame sampling rate does not make one source hour a shorter camera-hour. Missing processing and unobservability need separate masks so a broken service cannot win by doing less work. A report may additionally give delivered load / scheduled hour, but this is a distinct descriptive service measure and needs explicit outage counts.

Person-hour exposure is a different estimand: integrate ground-truth visible/eligible person occupancy over time, using declared visibility rules. It can be useful for a per-person hazard question, but cannot replace camera-hours for operator workload. Empty-camera time contributes camera-hours and zero person-hours; false detections can occur there. Predicted person-hours are particularly risky: missed people shrink the denominator and link exposure to the model being judged. A crowded camera may have many person-hours in a single camera-hour; neither measure implies independence.


## F079 — PROPOSAL — What to count
<a id="f079"></a>

Separate raw model candidates, grouped event hypotheses, service delivery attempts, and notifications actually exposed to the operator. Pick a delivery boundary such as a durable UI inbox record with a unique notification ID and delivery timestamp. A network retry that updates the same record is not another notification; a retry that creates another operator-visible record is. Log both so workload reconciliation is possible. No particular transport API is assumed.

Use adjudicated, class-compatible, camera/person-compatible temporal event matching specified in advance by the event-matching cell. Under a one-to-one contract, only one delivered record may claim a given GT episode; subsequent redundant records are counted separately as duplicate excess. Proposed exhaustive ledger for notifications within H_eval:

`N_delivered_eval = N_matched_valid + N_duplicate_excess + N_other_false + N_unknown`.

Also retain a reason flag for late delivery or wrong person/zone; whether these fail usefulness belongs to the frozen timeliness/matching contract. A true but late notification should not be relabeled as a nonexistent event: report usefulness failure and truth status separately. For workload, report `(N_duplicate_excess + N_other_false) / H_eval` as **false/excess delivered notifications per evaluated camera-hour**, with components. This avoids implying that duplicate excess is always a semantic falsehood. A semantic-false-only rate is also useful, explicitly named. Report `N_delivered_eval / H_eval`, precision with its matching definition, GT event recall, and a timeliness measure alongside either rate.

Never deduplicate the delivered log after the fact and call the result operator workload. If a new cooldown reduces ten notifications to one but misses repeat entries, both changes must appear. Frame false-positive counts, seconds in a false state, number of false episodes, and number of delivered notifications are different numerators: one false 60-second episode could generate 60 notifications or only one, with identical false-state duration. Do not rename these quantities interchangeably.

Empty/unknown rules: H_eval = 0 makes the rate undefined; N_delivered_eval = 0 makes precision undefined, not 100%; no GT episodes makes event recall undefined. No people/no events is valid background exposure if adequately reviewed and eligible. Unknown truth is not an automatic false alert, true alert, or negative interval. Keep its count and duration visible. If U delivered notifications remain unknown and all other matching outcomes are fixed, semantic false rate is bounded descriptively between F/H and (F+U)/H; this is a classification-completeness range, not a confidence interval. Complex unknown intervals that can change matching require re-adjudication or a separate restricted estimand, not this shortcut.


## F080 — PROPOSAL — Partial review and missed events
<a id="f080"></a>

1. Freeze the service, eligible exposure and selection design before reviewing outputs. Maintain complete delivered-notification logs over that exposure.
2. For delivered false/excess load, adjudicate every delivered item with enough context to establish truth, ownership and duplicate status. Full annotation of every non-alert frame is not logically necessary for this numerator, but reference event context and matching must be complete around all delivered items. Unknown delivery outcomes stay unresolved.
3. Independently inspect continuous intervals, including non-alert intervals, for missed GT episodes. Exhaustive annotated H_eval gives straightforward event recall on that exposure. Reviewing only notifications cannot find episodes that never produced notifications.
4. If review is sampled, use a prespecified probability sample with known inclusion probabilities. Stratified alert review can estimate a finite-population false total with an estimator such as sum(false_i / inclusion_probability_i); divide by the full corresponding logged exposure and compute design-aware uncertainty. Convenience samples of suspicious alerts cannot support that extrapolation. Sampled non-alert intervals need separate weighting and boundary rules for event recall; do not pool sampled frames as independent episodes.
5. Report selected, reviewed, adjudicated and unresolved counts/durations per stratum, including class/camera/time. “No false alerts among 20 reviewed” is not “zero false alerts in all logged camera-hours” when other deliveries are unreviewed.

These are protocol proposals. Human review can still miss events; observability limits, annotator disagreement and adjudication are additional uncertainty, not repaired by a statistical confidence interval.


## F081 — DERIVATION — What zero establishes
<a id="f081"></a>

Assume a fixed, completely observed exposure H > 0, a fixed tested configuration, correct classification of every relevant delivered alert, and a homogeneous Poisson false/excess notification process with constant rate lambda per camera-hour and independent increments. Then N ~ Poisson(lambda H), so P(N=0) = exp(-lambda H). Solving exp(-lambda_U H) = alpha gives the one-sided upper confidence bound:

`lambda_U = -ln(alpha) / H`.

At 95% one-sided confidence, lambda_U = 2.995732 / H. This is a frequentist procedure with coverage under its model, not a 95% posterior probability and not a guarantee of no future false notification. The estimate N/H is zero; the upper bound is positive. An equal-tailed two-sided 95% interval uses alpha/2 in the upper endpoint and gives 3.688879/H at zero, so “95% interval” must declare sidedness. [S037](SOURCES.md#s037) uses the reciprocal MTBF form; [S038](SOURCES.md#s038) directly bounds a Poisson mean. For N > 0 the analogous one-sided upper rate solves the Poisson lower-tail equation P_Poisson(lambda_U H)(X <= N) = alpha; a software version/method must accompany any implementation. No nonzero-count interval was run here.


## F082 — LOCAL MATH
<a id="f082"></a>

**[F082](#f082) / LOCAL MATH**, Python standard library arithmetic, stored in `W1_06_SOURCES/math_examples.json`:

| Zero false/excess count in H camera-hours | 95% one-sided upper rate, notifications / camera-hour |
|---:|---:|
| 1 | 2.9957 |
| 10 | 0.29957 |
| 100 | 0.029957 |
| 300 | 0.0099858 |

These are illustrative exposure levels, not target requirements or measured results. If an owner later specifies a rate ceiling r, zero-count planning under the same assumptions requires H >= -ln(alpha)/r. No ceiling is specified here. Preselect H; repeatedly checking and stopping as soon as a conventional bound looks good needs a sequential method, not unqualified reuse of this fixed-exposure result.


## F083 — DERIVATION — Heterogeneity and prevalence failures
<a id="f083"></a>

If independent camera processes have known fixed exposures H_c and different constant rates lambda_c, their summed count is Poisson with mean sum(lambda_c H_c). A pooled bound constrains only the exposure-weighted rate for that observed mix. It does not bound every lambda_c or an equal-camera mean, and provides no bound for an unseen camera with zero exposure. Report per-camera counts/exposure plus the pooled micro rate `sum(F_c)/sum(H_c)`; an equal-camera average `mean(F_c/H_c)` answers a different question. Small-camera denominators remain unstable.

Shared lighting changes, shifts, crowds, repeated detections from one persistent artifact, overlapping views and temporal bursts can violate independent increments/common-rate assumptions. A scenario with 999 quiet camera-hours and one untested high-risk camera is not representative just because the total exceeds 999. One synchronized hour across 100 cameras may contain common causes unlike 100 separated hours. Under a genuinely independent Poisson model with deterministic time-varying intensity, the same count argument can bound the integrated average intensity of that observed exposure; it still does not extrapolate across a changed deployment mix. Without an adequate stochastic model there is no distribution-free future rate guarantee from zero observations. Report descriptive counts/exposure and state the limitation; do not manufacture precision by treating frames as independent.

For a separately defined binary opportunity population, Bayes' identity gives PPV = sensitivity*p / [sensitivity*p + (1-specificity)*(1-p)]. **[F083](#f083) / LOCAL MATH:** sensitivity .90 and specificity .99 give PPV .9091 at p=.10 and .08264 at p=.001, even though the conditional error probabilities were held fixed. This is our algebraic example; it is not a frame-to-event conversion. In continuous video there is no uniquely defined number of negative opportunities, so do not insert camera-hours as a prevalence probability or derive notification precision from object specificity. Event density (GT episodes/hour), visible occupancy, scene composition and repeated episodes should be reported separately. Changing prevalence alone need not preserve false notifications/hour: it may alter non-target exposure, interactions, grouping and cooldown. Staged balanced clips therefore do not establish natural continuous-video alert workload.


## F084 — Minimal result record and open decisions
<a id="f084"></a>

Suggested report row: run/config hash; class; camera/shift/domain; H_scheduled, H_analyzed, H_eval and unknown-duration reasons; all delivered, matched, duplicate, other-false and unknown counts; GT episode count and missed count where independently available; delivery/matching/timeliness versions; micro and per-camera rates; interval method, sidedness and assumptions; sampling/review design. Preserve source timestamp intervals and delivery IDs so numbers can be reconciled.

**UNKNOWN:** actual event taxonomy, observability rules, notification delivery boundary, whether repeated reminders are desired, official temporal matching, intended camera/shift distribution, required operator workload, exhaustive-versus-sampled review budget, policy for late/censored episodes, and any industrial camera measurements. Resolve these with the owning team/context; no source here supplies them. Handoff dependencies: W1_05 matching; W1_01 observability/adjudication; W1_12 processing coverage; W1_13 dependence/uncertainty. Low false load must be interpreted with recall, latency and availability.


# W1_07 — сохранённые подробные наблюдения

Происхождение: [W1_07](_WORK/W1_07.md); [snapshots и локальные fixtures](_WORK/W1_07_SOURCES/). Контекст доступа и выполнения:  Prepared 2026-10-23, Europe/Moscow (+03:00). Scope: evaluation design for industrial safety video; no organizer data, hidden evaluator, model training or LinQ access supplied. No model performance is measured here. Sources retrieved 2026-10-23 approximately 03:11–03:16 UTC (06:11–06:16 Moscow); exact downloaded-source timestamps are in `W1_07_SOURCES/retrieval.json`, `pinned.json`, `extra-retrieval.json`.  Evidence labels: **DOC** official documentation; **CODE** inspected source, not executed; **PAPER** original methodology / published study; **INFERENCE** application to this task; **PROPOSED** team protocol; **UNKNOWN** not established. IDs are local for consolidation.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F085 — INFERENCE from [S045/S046/S047].
<a id="f085"></a>

**[F085](#f085) [INFERENCE from [S045](SOURCES.md#s045)/[S046](SOURCES.md#s046)/[S047](SOURCES.md#s047)].** A random frame split cannot support a claim about unseen cameras when train and test share those cameras. It may answer a much narrower question about sampled frames conditional on the observed installations. “New data” must specify whether it means later footage from the same camera, another camera in the same workshop, another site, or new people. None is interchangeable with another. Larger blocks are not automatically a more accurate estimate of the same quantity: they can change interpolation into extrapolation. Do not promise that a universal camera/day gap removes all dependence.

| Intended claim | Outer test grouping / chronology, proposed | Permitted development information | Residual limitation |
|---|---|---|---|
| Later operation on configured known cameras | Earlier development blocks, then untouched later recording sessions/days from those cameras; preserve whole episodes and input windows | Earlier footage and declared configuration for these cameras | Does not establish new-camera transfer; weather, production process and worker mix may still change |
| New camera within represented sites | Disjoint camera/installation IDs, with distinct validation cameras | Training cameras and separate validation cameras; declared target setup only | Shared site, uniforms and simultaneous events can remain dependent; claim is conditional on represented sites |
| New site/workshop | Disjoint site IDs with cameras nested within site | Development sites; separate validation sites if available | Few sites imply narrow evidence; one held-out site is a case study, not all-factory reliability |
| Adapted deployment on a new camera | Split each held-out camera into a declared setup/adaptation portion and a later scoring portion; or a preregistered causal online protocol | Only explicitly permitted setup labels / unlabeled observations | This evaluates the adaptation procedure plus model; not zero-shot transfer |
| Only one short video available | Keep source episode together; use whole material for debugging if no honest holdout exists | All visible debugging material | Demonstration/regression evidence only; no independent new-camera score |


## F086 — PAPER, [S045].
<a id="f086"></a>

**[F086](#f086) [PAPER, [S045](SOURCES.md#s045)].** Roberts et al. connect split design to temporal/spatial/hierarchical dependence and the intended prediction task. Their guidance warns that blocking can create extrapolation and that residual autocorrelation alone can underestimate required blocking. This ecological methodology motivates the table; it supplies no industrial-video block duration, sample size or accuracy guarantee.


## F087 — DOC+CODE, [S042/S043].
<a id="f087"></a>

**[F087](#f087) [DOC+CODE, [S042](SOURCES.md#s042)/[S043](SOURCES.md#s043)].** scikit-learn **1.6.1**, `GroupKFold(n_splits=5, shuffle=False, random_state=None)`, splits by supplied group labels. A group is held out together; across folds every group is in test once; number of groups must be at least `n_splits`. In `_split.py:610–660`, `shuffle=True` permutes unique groups then uses `array_split`; `shuffle=False` greedily assigns larger groups to the currently lightest fold by sample count. Labels `y` do not stratify this algorithm. No timestamps, original-video provenance or site relationships are inferred.


## F088 — CODE counterexample, [S043].
<a id="f088"></a>

**[F088](#f088) [CODE counterexample, [S043](SOURCES.md#s043)].** The 1.6.1 API prose says test sample counts are approximately balanced when shuffling. The inspected shuffled branch balances numbers of unique groups rather than their sizes. With group sizes 1000,1,1,1 and two folds, each receives two groups, hence sizes 1001 and 2. This is a hand-worked consequence of code, not an executed sklearn test. Therefore record actual fold camera counts, exposure and event counts; never rely on “balanced” as a class/exposure guarantee. `shuffle` and `random_state` were added in 1.6, so commands copied to older installations may fail.


## F089 — DOC+CODE, [S044/S043].
<a id="f089"></a>

**[F089](#f089) [DOC+CODE, [S044](SOURCES.md#s044)/[S043](SOURCES.md#s043)].** `TimeSeriesSplit(n_splits=5,max_train_size=None,test_size=None,gap=0)` supplies expanding-prefix training and later index blocks. `gap` is a number of **samples**, not seconds. `_split.py:1238–1300` ignores `groups`, computes test starts from array length and `train_end=test_start-gap`; it does not sort timestamps or enforce camera independence. Equal temporal spacing is needed for equal-duration test folds. A concatenated multi-camera array or dropped-frame stream therefore needs an explicit timestamp/group manifest. Neither API alone implements grouped, chronological video evaluation.


## F090 — PAPER+official correction, [S047].
<a id="f090"></a>

**[F090](#f090) [PAPER+official correction, [S047](SOURCES.md#s047)].** WILDS/iWildCam is an applicable methodological counterexample from camera imagery, not a PPE dataset recommendation. Its official release notes say dataset v1.0 randomly split ID images, allowing the same seconds-long sequence across training/ID validation/ID test. Dataset v2.0 keeps a camera-day in one ID partition, still sharing cameras across partitions. The paper separately defines camera-disjoint OOD evaluation. **WILDS package version and iWildCam dataset version are different version axes.** A public benchmark name or random seed does not prove independence.


## F091 — PAPER, [S048; INFERENCE].
<a id="f091"></a>

**[F091](#f091) [PAPER, [S048](SOURCES.md#s048); INFERENCE].** Barz/Denzler distinguish exact, near-duplicate and highly similar images; modified copies can differ in color, scaling or translation. Their candidate retrieval plus manual review demonstrates why exact equality alone is insufficient. The study is image classification and does not quantify video leakage here. Its journal/arXiv abstract ambiguously describes a relative “accuracy” change while experimental tables report **classification error rates**; no numerical transfer claim is used here.


## F092 — [PROPOSED].
<a id="f092"></a>

**[F092](#f092) [PROPOSED].** Establish original-video lineage before extracting clips, frames, crops or augmentations. Preserve `original_asset_id`, source acquisition ID and parent transformations. All derived views of a protected source/episode inherit its split. Renaming a clip, transcoding H.264 to another bitrate, changing fps or extracting every tenth frame creates no independent observation. A byte hash detects identical files; a decoded-frame hash detects some lossless equivalent encodings; perceptual hashes/embeddings retrieve some transformed candidates. None proves that different files are independent or that all overlap is absent. Static backgrounds can be similar across distinct events; false duplicate matches require review rather than automatic deletion.


## F093 — [PROPOSED].
<a id="f093"></a>

**[F093](#f093) [PROPOSED].** Construct a dependency graph for **relations that the intended claim forbids crossing**: shared original capture, overlapping source time intervals, copied/re-encoded segments, same continuous event recorded by multiple cameras, or same site if evaluating unseen sites. Connected components are indivisible split units. Not every shared person must be forbidden: the answer depends on whether the claim requires unseen people. Unknown lineage gets `unknown`, not a fabricated unique ID. If constraints produce one giant component, the dataset cannot provide the requested independent comparison; collect another acquisition unit or narrow the claim. Do not break the component merely to obtain a desired percentage split.


## F094 — [PROPOSED].
<a id="f094"></a>

**[F094](#f094) [PROPOSED].** Purge or keep together overlapping input/label windows around temporal boundaries: include the model’s past/future context, temporal smoothing, confirmation interval and complete episode boundaries. A gap larger than one frame can still leave the same violation on both sides. The required gap depends on these windows and dependence in the data, and remains a measured/declared design choice. When continuous recordings are long, blocking entire sessions/days can be more meaningful than treating every file as independent; splitting two adjacent recorder files is insufficient.


## F095 — [UNKNOWN].
<a id="f095"></a>

**[F095](#f095) [UNKNOWN].** Unknown foundation-model pretraining overlap cannot be certified clean by deduplicating only the team’s fine-tuning files. Record pretrained checkpoint source, hash/version, disclosed training corpora and cutoff when available; inspect disclosed memberships or URLs where possible. Say “no duplicate found by method M among available assets,” not “pretraining contamination excluded.” New privately acquired evaluation footage reduces direct known reuse risk but does not by itself establish broad target representativeness. No inspected source establishes the provenance of the model the team will actually use.


## F096 — DOC, [S049; INFERENCE].
<a id="f096"></a>

**[F096](#f096) [DOC, [S049](SOURCES.md#s049); INFERENCE].** Official scikit-learn guidance keeps test observations out of fitting and model choices, including learned preprocessing. For the frozen-model route, weights, checkpoint selection, NMS/association thresholds, per-class cutoffs, calibration, temporal confirmation, cooldown and ignore/unknown rules all belong to development. A threshold changed after seeing test errors is another selected variant; the same test is no longer an untouched estimate for that selected variant. Do not relabel it independent because no gradient update occurred.


## F097 — PAPER+CODE, [S050].
<a id="f097"></a>

**[F097](#f097) [PAPER+CODE, [S050](SOURCES.md#s050)].** Unlabeled test use is not inherently invalid: Tent is an explicit test-time adaptation setting. Inspected `Tent.forward` updates during testing, supports episodic reset, and its evaluation script resets at corruption/severity combinations. Thus a general “never fit anything at test” rule describes frozen inductive evaluation; declared adaptation answers another question. Tent on image classification does not establish useful or deployable PPE adaptation.


## F098 — [PROPOSED].
<a id="f098"></a>

**[F098](#f098) [PROPOSED].** Every run declares one of: (a) frozen model and preprocessing; (b) target configuration from pixels, e.g. operator-drawn ROI/zone, with provenance and no label-driven selection; (c) supervised target-camera adaptation using a separate labeled setup subset; (d) unsupervised target adaptation; (e) transductive access to the entire scored stream. These are disclosure categories, not organizer permissions. For (d)/(e), specify exact observations available, ordering, batch size/composition, parameters/statistics updated, optimizer/steps, reset boundaries, warmup/scored intervals, prediction-before-or-after-update and whether any future frame is accessible. Chronological online claims cannot use later test frames to improve earlier predictions. Hyperparameters for adaptation are selected on development domains. A labeled-test search remains label-driven tuning regardless of category.


## F099 — [PROPOSED].
<a id="f099"></a>

**[F099](#f099) [PROPOSED].** Annotation correction after error inspection needs an audit trail. Freeze predictions before adjudication; retain old GT, new GT, reasons, annotator/reviewer and timestamps. Prefer review blinded to model identity and apply the clarified rule to the whole affected evaluation subset, including unalerted intervals, rather than only “fixing false positives.” Report scores on corrected GT with explicit version. Once those observations influence model/policy design or the truth policy is tailored to a variant’s errors, use that set for development and seek fresh holdout for subsequent performance claims. Legitimate independent correction is not automatically forbidden, but it must not silently alter the denominator in favor of one model.


## F100 — [PROPOSED schema].
<a id="f100"></a>

**[F100](#f100) [PROPOSED schema].** One row per source-time interval, with child asset tables rather than frame-only filenames:

```text
asset_id, file_sha256, original_asset_id, acquisition_session_id,
site_id, camera_installation_id, camera_view_config_version,
start_timestamp, end_timestamp, timezone, timestamp_quality,
source_start_pts, source_end_pts, decode_version,
event_family_ids, dependency_component_id, duplicate_review_status,
split_role, fold_id, split_reason, split_manifest_version,
annotation_version, class_mapping_version, coverage_status,
allowed_use, adaptation_role, annotation_access_timestamp
```

Use null/unknown with reasons for absent provenance. Camera relocation or substantial view change gets a versioned installation/view ID while retaining the physical-device relationship. Event-family IDs connect cuts of one event and synchronized multi-camera views without claiming worker identity. Keep source acquisition and download dates separate. Freeze the manifest plus content hash; log exceptions and official splits without silently repairing them.


## F101 — [PROPOSED routes].
<a id="f101"></a>

**[F101](#f101) [PROPOSED routes].**

1. **Only supplied demo clips:** establish provenance and inspect potential same-source overlap; annotate reproducible scenarios and report behavior on these clips. If no independent group remains, stop at functional/regression evidence.
2. **Several independent acquisitions, known-camera deployment:** reserve later untouched sessions for test; use earlier sessions for training and validation, with temporal boundary handling. Freeze complete pipeline before test. No generic 80/10/10 ratio is justified by current inputs.
3. **New-camera/site transfer:** outer split at camera/site level; do tuning on remaining groups using distinct inner validation groups. A small grouped CV can aid development, but selecting the best CV variant and publishing its selected CV value as fresh test evidence introduces selection optimism. Keep an outer test if the available independent units permit it; otherwise label CV as exploratory and report group-level variability.
4. **Declared target adaptation:** choose rules on development cameras, then run the exact setup/adaptation/scoring procedure on untouched target cameras. Compare adapted and frozen systems on the same scored intervals, with adaptation cost and available target information stated.
5. **Late organizer evaluator:** preserve and reproduce its mandated split/result; run the independent group-aware analysis separately when possible. A team’s protocol does not override official rules or invent missing organizer permissions.

Rare classes may be absent in validation/test groups. Report per-class counts and undefined metrics rather than splitting one episode across partitions to make every class appear. More frames cannot create more camera/site units. Group balancing may use prespecified counts for allocation, but not repeated searches for favorable model scores.


## F102 — [PROPOSED reporting contract].
<a id="f102"></a>

**[F102](#f102) [PROPOSED reporting contract].** Splitting has no true-positive matching rule itself; the GT/matcher is inherited unchanged from the detector/person/event protocol. Always report the number of independent sites, camera installations, sessions, original videos and episode families per partition, alongside evaluated camera-hours, observable GT person-time or GT episode counts as appropriate. Keep unknown/ignored/unannotated exposure separate. “Accuracy over frames” and “average over cameras” estimate differently weighted quantities. For a downstream event protocol, pooled recall is summed matched GT episodes / summed eligible GT episodes; equal-camera mean recall averages the defined per-camera recalls. A camera with no eligible GT episode has undefined recall, not zero or one; report how many such cameras exist and retain their exposure for false-alert analysis. False alerts per evaluated camera-hour uses total delivered false-alert count / total **evaluated, sufficiently annotated** camera-hours under the same delivery/cooldown rule. Do not average camera rates without declaring weights. Unit and matching definitions must be identical before comparing variants. These are proposed reporting requirements, not official competition metrics.


## F103 — [PROPOSED, not run]: lineage/split audit.
<a id="f103"></a>

**[F103](#f103) [PROPOSED, not run]: lineage/split audit.** Decision: whether an “independent” result can be claimed, or whether data must be regrouped/recollected. Hypothesis: filename/frame splits cross protected lineage/event/domain units. Inputs: original manifest, timestamps, camera/site mapping, transformation records, optionally decoded candidate frames; no LinQ needed. Independent unit: outer claim’s camera/site/session plus protected dependency components. Fixed: target claim and forbidden crossing relations. Vary: original split versus component-aware split, without training or choosing on test performance. Procedure: enumerate intersecting group IDs and overlapping source intervals; retrieve duplicate candidates with a documented method/version and review them; inspect temporal windows crossing boundaries; reconcile group and exposure tables. GT: human-reviewed lineage/same-event links, not model-predicted violations. Matching: shared IDs / interval intersection plus adjudicated candidate pairs; numerator confirmed forbidden cross-split pairs or crossing components, denominator candidate pairs reviewed or components audited, explicitly **not** a universal leakage prevalence estimate. Save manifest/hash, candidate/review decisions, exclusions, counts, unresolved unknowns and split-diff. Stop after all known protected relations are checked and unresolved provenance is logged; no universal candidate-distance threshold. If violations found, freeze a corrected split before further selection; if none found, state audit coverage and method limits. Success proves split conformance for available provenance, not target-domain accuracy or unknown pretraining cleanliness.


# W1_08 — сохранённые подробные наблюдения

Происхождение: [W1_08](_WORK/W1_08.md); [snapshots и локальные fixtures](_WORK/W1_08_SOURCES/). Контекст доступа и выполнения:  Prepared 2026-10-23. Scope: industrial video analytics evaluation; no organizer evaluator, target data, LinQ SDK/device configuration or measured model output was supplied. Examples below are proposed contracts and mathematical counterexamples, not measured project results. Source IDs and evidence types are explicit. No acceptance targets are inferred.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F104 — Decision in one paragraph
<a id="f104"></a>

Select and freeze the **whole delivered-alert policy** on development/validation data independent at the deployment-relevant camera/video/session grouping. Model checkpoint, preprocessing, candidate cutoff, NMS, person association, tracker, calibration, class thresholds, temporal confirmation, unknown handling and cooldown jointly determine that policy. Report held-out person/event recall, timely recall, delivered false alerts per evaluated camera-hour, latency and coverage alongside object metrics. A classifier probability calibrated for one population/unit is not automatically a probability that a timely, correctly associated event alarm is useful. Calibration helps interpret a specified score; it does not specify the operational tradeoff or repair unseen events.


## F105 — Published classification result, not a video guarantee.
<a id="f105"></a>

**[F105](#f105) — Published classification result, not a video guarantee.** Guo et al. define confidence calibration through correctness conditional on confidence; their ECE weights binwise absolute confidence–accuracy gaps by bin occupancy. They fit positive scalar temperature T on validation logits via NLL, using softmax(z/T); this preserves the within-example argmax. Their experiments concern image/document classification. They report temperature scaling often effective, with a Reuters exception; this is not a theorem of calibration on a new camera or event pipeline. [[S052](SOURCES.md#s052), §§2, 4.2, 5]


## F106 — Documentation.
<a id="f106"></a>

**[F106](#f106) — Documentation.** Scikit-learn separates estimating scores from deciding actions. `TunedThresholdClassifierCV` selects a threshold to optimize a chosen scorer; default balanced accuracy is a software default, not an industrial objective. Its default stratified fivefold CV does not encode camera/session independence. `cv='prefit'` requires separate threshold-tuning validation data rather than reuse of classifier training data. The positive class and scorer parameters must be explicit. [[S053](SOURCES.md#s053), §§3.3.1–3.3.1.2]


## F107 — Documentation.
<a id="f107"></a>

**[F107](#f107) — Documentation.** A calibrator must see predictions independent of base-model fitting; otherwise confidence is biased. Scikit-learn's CV calibration avoids that fitting reuse, but the caller must choose appropriate folds. Absent classes in training or calibration folds produce problematic probability/calibrator behavior. Brier/log loss combine calibration with discrimination and outcome uncertainty, so a lower loss alone does not establish better calibration. [[S054](SOURCES.md#s054), §§1.16.1–1.16.3]


## F108 — Documentation and inspected code.
<a id="f108"></a>

**[F108](#f108) — Documentation and inspected code.** `precision_recall_curve` is binary sample classification, not detection/event matching. At real thresholds it uses score >= threshold, tied scores move together, and thresholds increase. The final (precision=1, recall=0) is a plotting endpoint with no threshold. Code warns and sets recall=1 at all actual thresholds when there are no positive labels; this convention must not become a claim of observed operational recall. See pinned `_ranking.py`, `_binary_clf_curve` lines 882–908 and `precision_recall_curve` lines 1019–1057. Code inspected, not executed. [[S055](SOURCES.md#s055), [S061](SOURCES.md#s061)]


## F109 — Documentation and inspected code.
<a id="f109"></a>

**[F109](#f109) — Documentation and inspected code.** `calibration_curve` accepts binary positive-class probabilities; default five uniform bins differs from other ECE conventions. Uniform and quantile bins differ. Empty bins are omitted; returning fewer points does not mean those confidence regions were validated. The code uses `np.searchsorted` on interior edges and divides only nonempty bin totals. Explicitly pin boundaries and retain bin counts when implementing ECE rather than assuming the plot returns a complete histogram. [[S056](SOURCES.md#s056), [S060](SOURCES.md#s060), `calibration_curve` lines 1032–1070; inspected, not executed]


## F110 — Documentation.
<a id="f110"></a>

**[F110](#f110) — Documentation.** Scikit-learn 1.7.2 Brier loss is mean squared probability error. Binary customary scaling is [0,1]; multiclass sum-of-squares is [0,2]. `scale_by_half='auto'` (added in 1.7) rescales only binary cases; `labels`, class column order and positive label matter. Comparisons must record scaling and class set. [[S057](SOURCES.md#s057)]


## F111 — Published counterevidence.
<a id="f111"></a>

**[F111](#f111) — Published counterevidence.** Ovadia et al. evaluate uncertainty on classification distributions with shifts/corruptions and OOD inputs. Their experiments show that calibration on held-out in-distribution examples does not ensure calibration under shift; temperature scaling can deteriorate under shifted data. This directly limits extrapolation from an in-domain calibration plot. Their results do not quantify this project's degradation or establish an alternative model as sufficient for PPE alarms. [[S058](SOURCES.md#s058), §§2–4, particularly §4.1 and Fig.1]


## F112 — Published formal setting.
<a id="f112"></a>

**[F112](#f112) — Published formal setting.** Geifman and El-Yaniv define selective classification using prediction f and acceptance g: reject means “don't know.” Coverage is accepted probability mass and selective risk is loss on accepted examples divided by coverage. Their risk-control setting assumes labeled examples sampled i.i.d. from a fixed distribution. Its guarantees cannot be transferred by treating consecutive video frames as independent samples or silently changing the target to delivered events. [[S059](SOURCES.md#s059), §§2–3]


## F113 — Documentation.
<a id="f113"></a>

**[F113](#f113) — Documentation.** Torchvision 0.23 NMS suppresses lower-score boxes when IoU > the specified threshold, so lowering this IoU threshold increases suppression. Exact score ties may select different boxes on CPU/GPU. This makes ordering, equality cases and runtime version relevant to association and subsequent events; do not conflate NMS IoU threshold with confidence threshold. [[S062](SOURCES.md#s062)]


## F114 — Proposed selection protocol (own protocol; F114)
<a id="f114"></a>

1. **Fix truth and deployment population first.** Define classes, persons, visible/unknown states, zones and episode starts/ends; define event matching, timeliness deadline reference, duplicates and ignore intervals. Decide known-camera future-time versus new-camera evaluation. Preserve grouped independence in calibration, selection and final testing. No legal obligation or protection correctness is inferred solely from image recognition.
2. **Declare the search unit.** One candidate is the complete configuration theta: model/weights and input processing; candidate confidence floor; NMS class mode/IoU/ties/max outputs; person/PPE association and tracking; calibrator and fitting subset; per-class decision thresholds; window measured in seconds or explicitly sampled frames; confirmation, hysteresis, missing-frame reset, cooldown and alert delivery. Record search budget/list and all tried candidates. Retuning any of these after test inspection is another selection round.
3. **Use train/development, calibration, policy-selection validation and untouched test roles.** These may be grouped folds rather than four huge datasets. When data are scarce, grouped nested/out-of-fold fitting can reuse data efficiently while keeping the predictions used to evaluate a choice independent of that choice's fitting. Do not mechanically use random frame CV. Jointly fitting a calibrator and selecting thresholds on one validation set is allowable as development, but that same score is optimistic as final evidence; test remains untouched. Final refitting changes the predictor and requires the frozen calibration/threshold recipe to match that refit.
4. **Fit calibration only for a named target/unit.** Example: probability of absent helmet for an observable GT-matched person's crop versus probability that a post-NMS candidate is a correctly localized helmet. Those targets need different GT and denominators. Event correctness can only be calibrated after defining candidate events, matching, horizon and duplicate ownership. A candidate-event calibrator excludes missed events by construction: separately count all GT episodes and misses. Do not train on GT-oracle person crops and label confidence calibrated for the complete detector pipeline.
5. **Replay continuous validation video for each policy.** Save object/person results for diagnosis, but choose operational settings using the complete event/delivery results. Cached raw predictions are useful only if their retention floor and output cap do not discard candidates needed for an alternative setting. Changing NMS after caching post-NMS detections cannot recover suppressed boxes. Temporal tuning on isolated positive clips cannot estimate camera-hour workload.
6. **Select by stated utility/constraints, not a magical 0.5 or maximum F1.** Owner supplies recall/timeliness priorities and tolerated alert/review workload, or the team reports a validation Pareto table and declares a provisional choice. Example symbolic optimization: maximize timely event recall subject to a specified false-alert rate, minimum analysis/decision coverage and latency requirement; alternatively report all tradeoffs when no constraint is supplied. This is not a supplied numerical requirement. For each class, show denominators and constraints; macro averages can hide a failed rare class. Per-class thresholds are extra fitted parameters and require enough independent relevant evidence; unsupported class-specific estimates remain unknown.
7. **Freeze before test.** Store config/artifact hashes, split manifest, calibrator, code/library versions, exact comparisons (>= versus >), timestamp units, sorting/ties, candidate floor and event matcher. Evaluate once on final target-relevant held-out data. If findings prompt redesign, label the set development and obtain fresh independent evidence or narrow the claim. Failed constraints are reported, not “fixed” by test threshold tuning.


## F115 — What to measure and keep in the denominator (F115)
<a id="f115"></a>

| Output | GT and counting unit | Numerator / denominator and boundary rules |
|---|---|---|
| Person state PR | Observable labeled person-times; fixed sampling/weighting, association rule | TP/(TP+FP), TP/(TP+FN). Unmatched persons must appear in complete-chain miss accounting; conditional matched-person scores are labeled conditional. Unknown GT is separately counted, not relabeled safe. |
| Event operating point | GT episodes and delivered alert records under frozen one-to-one matching | TP alerts/(TP+FP alerts); matched GT episodes/all eligible GT episodes. Duplicates consume delivered workload and matching policy determines FP. Timely recall requires qualifying matched delivery within declared deadline. |
| Workload | Reviewed continuous eligible camera-time | Delivered false alerts / evaluated camera-hours; also all delivered alerts/hour and review requests/hour. Record coverage/dropped time to prevent “improvement” by processing less. No camera-hour inference from class balance of selected clips. |
| Reliability/ECE | Named binary outcome or multiclass top-label correctness and held-out score unit | For bins B: ECE=sum |B|/N * abs(mean probability - outcome fraction). Dimensionless [0,1], or percentage points if multiplied by 100. State bin edges, top-label/classwise target, N and per-bin counts; empty bins contribute no observations, N=0 is unavailable. |
| Brier | Fully labeled score units, explicit binary or multiclass convention | Binary sum (p-y)^2/N; dimensionless [0,1]. Label unknown is excluded from this labeled-outcome computation but its count/coverage remains visible. N=0 unavailable; prevalence and weighting must match comparison. |
| Abstention | All eligible person decisions or camera-time under the chosen unit | Coverage=accepted/all eligible; conditional error=errors among accepted/accepted. Zero accepted => conditional risk unavailable, coverage zero. Also report total positive episodes detected, missed or unobservable and review burden. |

With no positive GT episodes, recall and timely recall are **not estimable** from that stratum. With no delivered predictions, operational precision is undefined, not evidence of perfect precision; workload can be zero with positive eligible exposure. Zero exposure leaves rate undefined. Pooled counts weight busy cameras/classes more; show pooled and per-camera/per-class counts rather than implying a macro average is pooled precision. Sampling weights must reflect the intended population; weighting frames does not create independent episodes.


## F116 — Failure cases and exact boundary tests (own inference/examples; F116–F116)
<a id="f116"></a>

- **[F116](#f116), frame calibration does not multiply across time.** Construct 100 equal-length tracks of ten frames, all scored 0.9 for a violation. Ninety tracks truly violate throughout; ten are persistently wrong (e.g., occlusion). Frame predictions are exactly calibrated at 0.9. Requiring three consecutive scores leaves 90% of event decisions correct, not 99.9%. Independence of repeated evidence was never supplied. Longer persistence also delays true detection and can remove short GT episodes. Python arithmetic executed locally; no classifier was run.
- **[F116](#f116), perfect crop classifier cannot recover absent persons.** If all provided crops are correct but the person detector misses one dangerous episode entirely, crop calibration/reliability remains excellent. No crop score exists for that missed episode, and the complete-chain event recall decreases. Likewise a correctly detected helmet belonging to the neighbor gives wrong person ownership despite object correctness.
- **[F116](#f116), calibration without usefulness.** A constant probability 0.01 on a population with exactly 1% positives is calibrated, with binary Brier 0.0099. At threshold 0.5 it detects none. Low aggregate ECE/Brier is not a recall requirement. Conversely, a coarse bin can hide subgroups with opposite calibration gaps; rare-camera errors contribute little pooled mass.
- **[F116](#f116), prevalence sensitivity.** Hypothetical binary decisions with TPR=0.9, FPR=0.01 have precision 47.62% at 1% prevalence and 8.26% at 0.1% prevalence: TP share pi*TPR divided by pi*TPR+(1-pi)*FPR. This calculation holds fixed class-conditional decision behavior, not probability calibration after shift. It is neither a project estimate nor a camera-hour false-alert conversion.
- **[F116](#f116), no object implies unknown or negative evidence?** Hidden head, frame loss or missing person cannot automatically mean absent PPE. A low “helmet present” score is not by itself a calibrated “helmet absent” probability. A three-way violation/safe/unknown contract needs truth for visibility and a declared action for unknown; rejecting uncertain negatives can hide true violations if excluded from recall.
- **[F116](#f116), selection changes population.** Calibrating all person crops then filtering by detector score/NMS/visibility changes the retained set. Calibrating event candidates before changing temporal merging/cooldown changes both positive meaning and candidates. Recheck reliability for the actual selected policy. A single-label softmax's unchanged argmax does not imply unchanged thresholded detections or alert timestamps; multiclass temperature scaling need not preserve rankings of a class score across different samples.
- **[F116](#f116), equality and time.** Include scores exactly at threshold, IoU exactly at NMS cutoff, tied scores, one score just above/below after export, onset exactly on deadline, exactly K confirmations, variable frame intervals, dropped frames inside a window and cooldown expiry equality. Specify whether unknown pauses, resets or expires persistence. Count a policy's confirmation/delivery time separately from GT onset. Sliding windows based on received frame count can represent different physical duration under load.
- **[F116](#f116), abstention is an action.** Unknown GT, model rejection, OOD flag and unavailable video are distinct reasons. Route review requests separately from violation alarms; a human review queue has workload/latency too. A high-confidence threshold cannot guarantee catching novel hazards or shift: OOD may be confidently wrong. Do not inherit selective-classification i.i.d. guarantees for correlated videos or changed cameras.

Small arithmetic outputs are preserved in `W1_08_SOURCES/small_examples.json`. No library/model benchmark or on-device execution occurred.


## F117 — Unresolved and handoff
<a id="f117"></a>

No supplied operational utility, required per-class recall, camera-hour workload limit, timeliness deadline, unknown action, independent target validation set or event matching convention exists in this cell's evidence. These are decisions to make explicitly, not thresholds to extract from Guo. Calibration data availability may make a complicated per-class/event calibrator unjustified; report reliability counts and unsupported regions rather than promise a sample size. LinQ execution/export may shift threshold-boundary decisions; parity evidence is separate. Handoff to training_strategy: grouped independent calibration/selection and freeze record. Handoff to violation_methods/video_architecture: temporal/unknown/cooldown semantics and complete-chain replay. Handoff to evaluation: distinct object/person/event probabilities; all eligible positives, exposure, abstention and missing coverage retained.


## F118 — Additional temporal-selection boundary (F118; own inference)
<a id="f118"></a>

A frame-score PR sweep assumes fixed scored samples. A full alert policy can change the samples themselves: raising a threshold may remove an early trigger, shift confirmation later, alter episode merging or free a cooldown slot for a later alert. Delivered false-alert counts and timed event matches therefore need not vary monotonically with confidence threshold. For example, if a true early trigger starts a shared cooldown that suppresses two later spurious triggers, removing the true trigger can allow those spurious triggers (depending on cooldown duration and spacing). This is an intentionally policy-dependent counterexample, not a recommended global cooldown design. Recompute event records/matching for every joint configuration rather than apply `precision_recall_curve` to a fixed list and assume it simulates temporal replay. Maintain separate per-class and per-person cooldown contracts if those are the intended semantics; freeze and test cross-class/person interference explicitly.


# W1_09 — сохранённые подробные наблюдения

Происхождение: [W1_09](_WORK/W1_09.md); [snapshots и локальные fixtures](_WORK/W1_09_SOURCES/). Контекст доступа и выполнения:  Research completed 2026-10-23; access window 03:16–03:22 UTC (06:16–06:22 Europe/Moscow, UTC+03:00). Scope: primary papers, pinned TrackEval source, four tiny evaluator examples. No industrial dataset/model benchmark, device test, or proof of LinQ execution was performed.


## F119 — own inference from [S063–S068].
<a id="f119"></a>

**[F119](#f119) [own inference from [S063](SOURCES.md#s063)–[S068](SOURCES.md#s068)].** Track quality and alert quality require separate evidence. HOTA/IDF1/MOTA evaluate detections and their association to annotated trajectories; they do not read PPE ownership, violation state, alert delivery, cooldown or episode semantics. Good tracking can support temporal policies but cannot certify them. A tracker ID is a sequence-local token; it does not establish an employee’s name, badge identity, legal identity, or even cross-camera identity. An event ID and a track ID should be distinct fields.


## F120 — [documentation/paper].
<a id="f120"></a>

**[F120](#f120) [documentation/paper].** HOTA explicitly separates detection and association; its paper demonstrates failure modes of prior metrics, including MOTA’s emphasis on detection and IDF1’s global trajectory matching behavior. These are metric-design results on MOT tasks, not measurements of industrial alert performance. Ristani et al. explain that identity-based and event-based tracking measures answer different user questions; their “event-based” CLEAR errors are tracking decisions, not delivered safety-alert episodes. [[S063](SOURCES.md#s063), [S068](SOURCES.md#s068)]


## F121 — [source inspection; proposed annotation contract].
<a id="f121"></a>

**[F121](#f121) [source inspection; proposed annotation contract].** The metric routines consume aligned frame lists `gt_ids`, `tracker_ids`, pairwise similarity matrices and totals of IDs/detections/timesteps. The MOTChallenge adapter reads frame, ID, x/y/width/height, GT mark/class or tracker confidence; it computes box IoU, remaps IDs to contiguous indices, and rejects duplicate IDs within a frame. Preserve stable GT person IDs across every interval where annotators can establish continuity; tracker numeric IDs need not equal GT numeric IDs. GT has to identify which person is which, independently of predictions. [[S064](SOURCES.md#s064)–[S067](SOURCES.md#s067)]

Proposed minimum record: `sequence_id, camera_id, frame_index, source_timestamp, gt_person_id, bbox, annotation_status, visibility, identity_link_status`. Add `episode_id, violation_type, observable_state, onset/end bounds` for alert evaluation, and `pred_track_id, state_owner_id, emitted_alert_id, delivery_timestamp, reset/transfer_reason` in predictions/logs. These extra fields are our proposal, not TrackEval inputs. Specify whether IDs persist across complete occlusion, exit/re-entry, a file boundary, camera restart or camera change. Uncertain linking must be recorded as uncertain, not guessed to obtain a score.


## F122 — source inspection, [S064].
<a id="f122"></a>

**[F122](#f122) [source inspection, [S064](SOURCES.md#s064)].** HOTA uses alpha values 0.05, 0.10, …, 0.95. It builds a whole-sequence alignment matrix from similarities, performs per-frame Hungarian assignment on alignment × similarity, and retains assigned pairs meeting alpha. At each alpha: `DetA=TP/(TP+FN+FP)`. For a matched GT/predicted-ID pair with m matches and G/P detections, association Jaccard is `m/(G+P−m)`; AssA averages this over TP detections. `HOTA_alpha=sqrt(DetA_alpha*AssA_alpha)`; summary HOTA averages alpha values. LocA is mean matched similarity, reported separately. Localization affects HOTA via alpha integration: **HOTA is not sqrt(DetA*AssA*LocA)**. `HOTA(0)` in this implementation indexes the first alpha, 0.05.


## F123 — source inspection, [S065].
<a id="f123"></a>

**[F123](#f123) [source inspection, [S065](SOURCES.md#s065)].** Identity uses configurable similarity threshold 0.5 by default. It counts potential threshold-qualified matches per GT/predicted-ID pair over the sequence, then globally assigns trajectories one-to-one by minimizing IDFN+IDFP with dummy assignments. `IDTP=GT_detection_count−IDFN`; `IDF1=2IDTP/(2IDTP+IDFP+IDFN)`, `IDR=IDTP/(IDTP+IDFN)`, `IDP=IDTP/(IDTP+IDFP)`. These counts are detection instances across frames, not unique workers or switch counts. A good segment excluded by the best one-to-one trajectory assignment can still incur identity errors. Sequence aggregation sums ID counts and recomputes ratios.


## F124 — source inspection, [S066].
<a id="f124"></a>

**[F124](#f124) [source inspection, [S066](SOURCES.md#s066)].** CLEAR defaults to threshold 0.5. Hungarian matching favors continuation of the previous assignment by adding 1000 before similarity, subject to the threshold. IDSW compares each matched GT ID with its last matched tracker ID, including after gaps. For positive GT count, `MOTA=1−(FN+FP+IDSW)/GT_detection_count`; it may be negative. `Frag` accumulates returns to matched status after interruptions, excluding the first matched segment; it is different from IDSW. MOTP is mean matched similarity in this adapter, not physical position accuracy. Sequence aggregation sums counts and recomputes ratios. Implementation-specific empty branches and gap behavior need care ([F127](#f127)).

Units: all above ratios are dimensionless; raw code returns fractions, displayed tables scale floats to percent. IDSW/Frag/FP/FN are counts, not counts per hour. HOTA combines sequences using summed detection counts and TP-weighted association terms before recomputing; it is not an unweighted mean of sequence HOTA. The base metric summarizes alpha arrays by their mean. Class-averaged and detection-averaged methods differ; pin the chosen aggregation, class scope and empty-class option. [[S064](SOURCES.md#s064)–[S067](SOURCES.md#s067)]


## F125 — source inspection, [S067].
<a id="f125"></a>

**[F125](#f125) [source inspection, [S067](SOURCES.md#s067)].** MOTChallenge preprocessing is a benchmark-specific pedestrian policy: match against GT at IoU 0.5 and remove predictions matched to designated distractor classes; filter GT by target class/mark; this adapter has no crowd-ignore regions. `DO_PREPROC`, benchmark selection and class mapping therefore change scores. It is not a generic rule for unknown PPE or unobservable people. An industrial adapter needs its own explicit ignore policy and tests. Merely omitting unlabeled people makes predictions against them appear false positive, and omitting hard intervals can overstate association quality.


## F126 — [source inspection; own inference].
<a id="f126"></a>

**[F126](#f126) [source inspection; own inference].** Empty conventions do not prove correctness: identity returns zero-valued ratios with IDFN or IDFP set on an empty side. HOTA returns HOTA zero and LocA one for an empty side (including both empty). CLEAR’s sequence-empty early branches return initialized MOTA zero, rather than applying its normal formula; combining counts later can differ from interpreting that per-sequence zero as performance. Record GT/prediction counts and report no-evidence cases as such. A LocA of one with no TP is a convention, not perfect localization. Unknown violation state is not representable as an identity score; report its coverage separately. [[S064](SOURCES.md#s064)–[S066](SOURCES.md#s066)]


## F127 — [locally executed small examples, not a benchmark].
<a id="f127"></a>

**[F127](#f127) [locally executed small examples, not a benchmark].** `W1_09_SOURCES/small_examples.py` loads the unchanged pinned metric modules and skips package initialization. Python 3.11.9, NumPy 2.4.2, SciPy 1.17.1; only runtime aliases `np.float=float`, `np.int=int` were supplied because the 2022 code uses removed aliases. No matching/counter logic was changed. The script supplies preprocessed IDs/similarity directly, so it does not validate file parsing or preprocessing. Results in `small_examples.json`:

| Synthetic input | MOTA | IDF1 | HOTA | IDSW | Frag |
|---|---:|---:|---:|---:|---:|
| 10 frames, 1 GT person, perfect similarity and stable ID | 1 | 1 | 1 | 0 | 0 |
| Same 10 perfect detections, ID0 for 5 then ID1 for 5 | .9 | .5 | .707107 | 1 | 0 |
| 3 GT frames; ID0 / no predictions / ID0 | .666667 | .8 | .666667 | 0 | 0 |
| Same, but middle has an unrelated IoU-zero prediction | .333333 | .666667 | .577350 | 0 | 1 |

The last comparison precisely localizes a pinned implementation failure: CLEAR lines 70–76 `continue` on an entirely empty GT/tracker frame without resetting `prev_timestep_tracker_id`; the ordinary matching path resets it at lines 102–107. Thus absence of reported Frag does not guarantee uninterrupted output. The extra unrelated prediction correctly adds an FP but also changes interruption accounting. This is a narrow reproducible observation, not a claim about every CLEAR evaluator or a patched benchmark. Preserve official scores and expose a separate gap diagnostic; document any future evaluator correction/version.


## F128 — [proposed protocol].
<a id="f128"></a>

**[F128](#f128) [proposed protocol].** Full IDs: annotate target persons across complete evaluated clips, define occlusion and re-entry linkage rules, preserve dense negatives and visibility masks, then run the fixed adapter/config. Report HOTA/DetA/AssA/LocA, IDF1 with its counts, MOTA with FP/FN/IDSW and Frag, per-sequence counts and pooled totals. Keep online/causal output distinct from offline relabeling; retroactive smoothing may improve identity scores while arriving too late to help a live alert. Evaluate the same frozen alert policy on the produced tracks.

No full IDs: do not claim HOTA, IDF1, MOTA IDSW or whole-clip identity continuity by assigning a fresh GT ID to every frame or using tracker IDs as truth. You can evaluate exhaustive per-frame person/state recognition on annotated frames, and independently annotated violation episodes/delivered alerts under a stated matching policy. Manually linked short intervals can support a clearly named **annotated-window tracking diagnostic** only: report eligible windows/persons/duration, how selected, identity exclusions and boundary censoring; reset IDs at boundaries and do not pool them as if continuity across boundaries were known. A few inspected alerts cannot estimate missed episodes without independent review of non-alert footage.


## F129 — [proposed tests; not existing benchmark rules].
<a id="f129"></a>

**[F129](#f129) [proposed tests; not existing benchmark rules].** Match alerts to independent person-linked violation episodes where identity is observable, using the event contract owned by W1_05. Do not use equality of raw tracker IDs as the correctness test. Preserve all delivered duplicate alerts before any analysis deduplication. Report explicit denominators below; rates on selected diagnostic clips describe those clips only.

| Controlled case | Failure to expose | Proposed diagnostic and denominator |
|---|---|---|
| Continuous visible violation; replace track ID mid-episode without changing boxes/state | Cooldown is keyed only to ID, so duplicate alert | Additional delivered alerts after the first eligible episode alert / matched episodes; separately episodes with a post-switch duplicate / episodes containing a switch |
| Worker A violates; IDs swap at crossing with compliant B | A’s persistent violation/evidence transfers to B | Wrong-person state/alert transfers / adjudicated crossing opportunities; count episodes and duration of incorrect owner attribution |
| A compliant, B violating; swap IDs | B inherits suppression or A’s timer, missing or premature alert | Missed eligible episodes and alert delay relative to observable onset; denominator all independently annotated eligible B episodes |
| Partial and complete occlusion, return same person with same/new ID | Unknown treated as compliant; premature reset; unbounded carried state | Re-alerts, missed alerts and wrong carryover by occlusion stratum; denominator occlusion-return cases with independently resolvable identity |
| Person exits; different person later receives recycled numeric ID | Old state suppresses or contaminates new person | Incorrect carried-state cases / ID-reuse opportunities; test reset reason and track lifetime |
| Same person resolves violation then repeats it | Cooldown hides a genuinely new episode | Detected/delivered second episodes / eligible repeated episodes; specify clearance and new-onset rule |
| Tracker reconnect/restart or file boundary during ongoing episode | Repeated alert, silent timer reset, stale state | Delivered duplicates/misses / restart-spanning eligible episodes; mark censored onset |
| Same person, stable perfect tracking, wrong PPE ownership or delayed delivery | High tracking score coexists with wrong or late alert | Person-state/ownership correctness and timely delivered episode recall with their own GT |

Proposed causal logs: frame/source timestamp, current track ID and lifetime, person-state evidence, unknown/visible flag, accumulator value, active episode, cooldown expiry, transfer/reset decision, alert creation and delivery. This makes state propagation reviewable without asserting that a track is a worker identity. Report both numbers of events and coverage; confidence intervals and exposure accounting belong with W1_06/W1_13.


## F130 — [own counterexamples].
<a id="f130"></a>

**[F130](#f130) [own counterexamples].** With 1,000 perfect detections split into two long IDs, one switch costs only 1/1,000 MOTA, yet a per-ID alert engine may emit two alerts for one continuous episode. Conversely, a more fragmented tracker can still deliver one correct alert if episode state survives a proven same-person relink. Both examples are thought experiments about downstream policy, not measured model outcomes. A high HOTA with swapped PPE labels remains possible because PPE labels are absent from the tracking inputs. A high offline IDF1 can coexist with unacceptable live decision delay because trajectory matching uses the whole sequence and has no delivery clock. Therefore selecting a tracker only by one pooled score can reverse the decision relevant to operations.


# W1_10 — сохранённые подробные наблюдения

Происхождение: [W1_10](_WORK/W1_10.md); [snapshots и локальные fixtures](_WORK/W1_10_SOURCES/). Контекст доступа и выполнения:  Research cutoff: 2026-10-23, approximately 03:23 UTC / 06:23 Europe/Moscow (UTC+03). Assignment: industrial-safety video analytics; LinQ inference required by supplied context, but no SDK, device configuration, model or access supplied. This is a research result and proposed test contract, not a measured deployment result. Code was inspected, not executed for inference. No model, LinQ compiler or target benchmark was run.


## F131 — Decision and principal findings
<a id="f131"></a>

**Keep four separate claims:** (1) artifact is structurally accepted; (2) numerical outputs agree within a declared contract; (3) application quality and alert behavior remain acceptable; (4) the named target actually executed the declared workload. Evidence for one does not establish the next. Establish the native baseline, then isolate export, compiler/runtime, quantization and application changes in paired stages. The task owner must approve task-level degradation limits; the deployment owner must establish actual device placement. No universal epsilon, mAP loss allowance or LinQ command is justified by available evidence.


## F132 — documentation:
<a id="f132"></a>

- **[F132](#f132) — documentation:** Floating-point operation ordering, platform and batching can change outputs without a software defect. Bitwise agreement is not a default cross-runtime criterion, even for FP32. PyTorch v2.5.1 explicitly documents this; archived TensorRT 10.x troubleshooting agrees. A reproducibility requirement within one pinned environment is a separate question. [[S070](SOURCES.md#s070), [S077](SOURCES.md#s077)]


## F133 — code inspection:
<a id="f133"></a>

- **[F133](#f133) — code inspection:** Preprocessing can differ before either network runs. Ultralytics v8.3.0 provides an unusually useful counterexample: `pre_transform` makes `LetterBox(auto=same_shapes and self.model.pt, ...)`; therefore native `.pt` and non-`.pt` paths can use different padding even with the same `imgsz`. Its `preprocess` normalizes non-tensor images by 255 and converts BGR/BHWC to RGB/BCHW, but a tensor input bypasses those image-path operations. A parity test must compare actual tensors, not assert that filenames and resolution settings match. This is a version-specific example, not a recommendation to adopt Ultralytics. [[S072](SOURCES.md#s072)]


## F134 — code inspection/documentation:
<a id="f134"></a>

- **[F134](#f134) — code inspection/documentation:** NMS is a semantic boundary. ONNX NMS-11 has boxes `[batch, boxes, 4]`, scores `[batch, classes, boxes]`, a format attribute, per-class output cap and selected-index output. Its default cap of zero produces no selected boxes. Ultralytics' inspected NMS consumes another layout, applies strict `>` confidence filtering, class handling and a global retained-detection cap. Substituting one for the other requires an explicit adapter. [[S074](SOURCES.md#s074), [S073](SOURCES.md#s073)]


## F135 — documented counterexample:
<a id="f135"></a>

- **[F135](#f135) — documented counterexample:** Equal-score overlapping boxes need not produce the same selected box on Torchvision CPU and GPU. Output-array equality can fail while both obey that API. Sort-order changes must be distinguished from missing/extra detections and from changed selected geometry. [[S075](SOURCES.md#s075)]


## F136 — documentation/code inspection:
<a id="f136"></a>

- **[F136](#f136) — documentation/code inspection:** Quantization is lossy. Static calibration estimates activation parameters from calibration inputs; parameter choices and hardware arithmetic matter. The ORT debugging code can expose and match activations, but its `collect_activations` defaults to CPU and disabled graph optimization. Running it unchanged would not demonstrate compiled LinQ behavior. [[S076](SOURCES.md#s076), [S078](SOURCES.md#s078)]


## F137 — documentation plus inference:
<a id="f137"></a>

- **[F137](#f137) — documentation plus inference:** ORT can partition a graph among execution providers and use CPU for nodes unsupported by a higher-priority provider. Thus registered providers and successful inference are insufficient proof of full accelerator placement. This is a concrete ORT failure mode supporting a general evidence requirement, not evidence that LinQ uses ORT or permits fallback. [[S079](SOURCES.md#s079)]


## F138 — own inference:
<a id="f138"></a>

- **[F138](#f138) — own inference:** Small tensor error is neither necessary nor sufficient for identical alerts. Thresholding, NMS, association, zone boundaries and temporal state introduce discontinuities. Conversely, nearly identical application metrics can conceal serious failures on rare event classes. Report both paired behavior differences and ground-truth quality.


## F139 — Proposed stage-localization protocol
<a id="f139"></a>

Everything below is a proposed protocol, not an organizer rule or a promise of device capability. Use one immutable manifest with decoded frame IDs and timestamps. Freeze native weights and evaluation mode, preprocessing, class map, postprocessing, association, temporal rules and evaluator. Keep calibration/tuning data separate from the final evaluation set; changes after examining final results need a new declared evaluation. Exact partition policy belongs to W1_07.

| Pair/stage | Controlled comparison | Failure localizes toward | Necessary limitation |
|---|---|---|---|
| P0: decode/preprocess | Same archived frame bytes through each proposed input path; save tensor plus resize/pad metadata | Decode, color, normalization, layout, dtype, shape | Same compressed video decoded differently is not guaranteed same pixels; first use a common decoded snapshot |
| P1: native vs exported floating-point graph | Identical saved input tensors, aligned raw output tensors; same host-side postprocessor | Export, unsupported behavior, output interpretation | CPU reference differs from accelerator arithmetic too; name the reference backend |
| P2: exported reference vs target-compiled floating-point, if supported | Same tensors, output schema and precision intent | Compilation, runtime kernel, layout, precision or target-specific transform | If target cannot run floating-point, this isolating stage is unavailable; do not imply it passed |
| P3: floating-point vs quantized graph on a reference runtime, if supported | Same model lineage and tensors; calibration frozen | Quantization graph/scale change | It does not isolate final target kernels or prove target support |
| P4: quantized reference vs compiled target | Matched artifacts/parameters and same inputs | Target quantized lowering/runtime; adaptation errors | A compiler may perform its own quantization; compare actual derived graph/config, not nominal `INT8` names |
| P5: common raw-output fixture through each postprocessor | Decoder, scoring, NMS and inverse transform tested independently | Postprocessing port | Embedded NMS may prevent raw access; state observability gap |
| P6: native full chain vs target full chain | Same ordered, timestamped sequences; equal initial state; policies frozen | Combined behavior and temporal propagation | Identical frames with different drops/timing may be a load/freshness test instead of pure parity |

If a runtime cannot expose intermediate or raw tensors, preserve this as an observability limit. Use the earliest common observable boundary and retain end-to-end tests. Do not fake one-to-one tensor correspondences after fusion or different detector heads. A target result can be useful with incomplete stage observability, but debugging confidence is lower.

For each pair, make two reports: **fixed-policy parity** (same thresholds/rules), and, only if needed, **retuned deployment candidate** (retune on designated development data, freeze a new config, evaluate separately). Retuning can recover quality but cannot be reported as unchanged export parity.


## F140 — Input and output contract to record
<a id="f140"></a>

Proposed fields, not a LinQ API:

1. Input identity: frame/video hash; frame index; timestamp basis; decoder/version; orientation/crop policy; original width/height; channel count and alpha behavior. Use a saved decoded reference image to isolate neural computation first.
2. Resize: target height/width, keep-aspect versus stretch, scale-up policy, interpolation implementation, rounding, stride padding, left/top/right/bottom pad, pad color and location. Store actual integer pad and realized dimensions per frame. A nominal `640` is insufficient.
3. Tensor: semantic color order, HWC/CHW and batch axis, contiguous/strided storage assumptions, channel mean/std, numeric range, cast order, signedness, quantized input scale/zero point and per-axis axis where applicable. Distinguish a byte image from an already normalized tensor. Record graph-internal versus host preprocessing to avoid double normalization.
4. Native model: weights hash, repository commit, framework/dependency versions, evaluation/training mode, augmentations, seed/determinism controls if relevant, batch size, actual hardware and precision controls. The framework's FP32 tensor dtype alone does not state all computation precision. PyTorch's pinned numerical note discusses TF32 separately. [[S070](SOURCES.md#s070)]
5. Export/compiler: exporter generation/options, ONNX IR/opset imports and custom domains, dynamic shape bounds/profile, batch/shape combinations actually tested, graph simplification/fusion options, compiler/runtime/driver/firmware versions, plugin versions, derived artifact hash and compile log. The pinned PyTorch export overview distinguishes exporter paths and documents static tracing limitations; do not generalize from one traced example to all shapes or data-dependent branches. [[S071](SOURCES.md#s071)]
6. Raw output: name/order/dtype/shape, candidate axis, logits or probabilities, box encoding and coordinate space, class index-to-name map, background handling, objectness combination if that model uses it, whether decode/NMS is embedded. Do not assume every YOLO generation has the same output schema or an objectness column.
7. Postprocessor: decoder version; score transformation; comparison operators at thresholds; multi-label/best-class policy; class-aware/agnostic NMS; IoU formula; NMS threshold; pre-NMS top-k and post-NMS cap; tie policy; invalid boxes/nonfinite handling; any timeout; inverse resize/pad transform and clipping. Ultralytics v8.3.0 has NMS candidate and output limits and a time-limit break; these can affect outputs independently of the network. [[S073](SOURCES.md#s073)]
8. Temporal chain: association/tracker config; zone geometry and anchor; unknown-state policy; dwell/debounce; cooldown and rearming; timestamp handling; track reset/stream restart behavior; output event schema. Record versions and hashes independently from detector weights.

For letterbox geometry, proposed inverse-map check is `x_original=(x_network-pad_left)/gain_x`, `y_original=(y_network-pad_top)/gain_y`, followed by the declared clipping. Use realized transform metadata rather than assume symmetric padding. Stretching requires distinct x/y gains. Test points and boxes at padding edges, original-image edges and odd-sized inputs. For an unchanged input representation, tensor hashes can detect exact identity; casts/quantization require a declared equivalence transform, not identical bytes.


## F141 — Tensor agreement (no annotation GT)
<a id="f141"></a>

Reference is a named implementation's output on the same tensor, not physical truth. Check names/shapes, semantic axis mapping and dtype first. For corresponding finite elements `a_i` (reference), `b_i` (candidate), a possible declared check is `|b_i-a_i| <= atol + rtol*|a_i|`. Absolute tolerance has the tensor's units; relative tolerance is dimensionless. This is a proposed criterion, not a source-derived default. Near-zero reference values need absolute tolerance; relative error alone can be unstable. Choose tolerances before held-out evaluation using expected numeric behavior and task sensitivity; no value is established here.

Report: number compared `N`; mismatched-shape tensors; nonfinite counts per side; mean/max absolute error; declared quantiles; relative-error denominator definition; count and fraction exceeding tolerance `N_fail/N`; all-finite pass/fail. Aggregate separately per output/tensor/frame and optionally worst frame; a global element-weighted average can hide a small critical head. NaN, Inf and zero-element tensors need explicit policies: do not silently drop nonfinites; report empty tensors as empty and denominator zero as undefined. Exact integer IDs/shapes need semantic checks, not an FP epsilon. For quantized tensors compare qparams and integer encodings where representation should match; compare dequantized values where encodings legitimately differ. Cosine similarity/SQNR can be diagnostics but do not alone establish a threshold decision or useful boxes.

No universal bitwise requirement follows from FP32. [[S070](SOURCES.md#s070), [S077](SOURCES.md#s077)] Quantization error includes rounding and clipping, and FP16 can overflow. [[S080](SOURCES.md#s080)] If tensors diverge, inspect aligned intermediates as available, remembering that added debug outputs can alter optimization. [[S077](SOURCES.md#s077)] Verify the production artifact again after diagnosing with an instrumented artifact.


## F142 — Detection agreement (reference predictions, not annotation GT)
<a id="f142"></a>

Canonicalize to one original-frame coordinate system and class map before matching. Do not compare array order. Proposed deterministic one-to-one matching: only same frame and same class; eligible edges satisfy a **predeclared** IoU gate; select maximum-cardinality matching, then maximum summed IoU among those, then declared stable tie-break. Report every unmatched detection. The gate is a test parameter, not a quality acceptance threshold and not automatically COCO's settings.

Report per class and sequence: native count `R`, candidate count `C`, matched pairs `M`, reference agreement recall `M/R`, candidate agreement precision `M/C`, unmatched counts `R-M`, `C-M`; coordinate absolute differences in original pixels (and normalized units if useful), matched IoU and score differences. Counts are per evaluated frame; micro aggregation sums counts, macro aggregation averages only declared defined class/sequence results and reports inclusion. Duplicate boxes count individually until one-to-one matching. If both sets are empty, record both-empty; ratios have zero denominator and remain undefined unless an explicit convention is separately stated. Class disagreement creates unmatched detections under class-aware matching; a supplementary class-agnostic diagnostic may localize it but must not conceal it.

These are parity statistics. Recompute detector AP/precision/recall against independent annotation GT under the frozen evaluator as a different report; a native error reproduced perfectly is still an error. Compare quality on the same frame manifest and preserve all ignore/unknown rules. W1_02 owns exact AP semantics.


## F143 — Person states and events
<a id="f143"></a>

Replay identical full sequences, including gaps, with state reset at the same boundaries. Compare person-level states/unknowns and associations as intermediate outputs. Track numeric IDs are not automatically comparable across runs; require a declared identity mapping or use annotation-based person matching. A detector change can change ownership or track continuity even if boxes remain near one another.

For parity events, reference events are native-chain outputs. Match one-to-one by predeclared event type, camera, identity/zone rules and temporal rule, with stable tie-break; report unmatched events, duplicates, split/merge patterns and onset/end differences in seconds. The exact event matching rule belongs to W1_05 and must be recorded rather than improvised as a universal tolerance. Separately score each chain against annotated observable events and evaluated camera-time: event precision/recall, delivered false alerts per camera-hour and timing. Numerators, denominators, censoring and unknown intervals must follow that evaluator; native agreement is not event truth. If no GT-positive events exist, recall is undefined; if no evaluated camera-time exists, false-alert rate is undefined. Unknown/unreviewed intervals cannot silently become negatives. Macro per-camera results and count/exposure-weighted totals answer different questions and should be labeled.

A tensor tolerance pass does not override an event failure. A task-metric pass does not prove tensor conformance. Report both outcomes and localize the discrepancy.


## F144 — Counterexamples / compact regression cases
<a id="f144"></a>

All following examples are **own hypothetical constructions**, not observations on an actual model or performance claims. Numeric values illustrate discontinuities and are not proposed acceptance targets.

- Score threshold `0.5`, strict `>`: native `0.50001`, candidate `0.49999`. Absolute difference is `0.00002`, yet a candidate disappears. With an illustrative five-consecutive-frame confirmation policy, moving one of five positive frames below threshold can suppress the alert. If a missing helmet is inferred from absence of a detection, the direction can reverse; unknown handling must be tested.
- Two overlapping, equal-score boxes: Torchvision's documented CPU/GPU tie may retain different geometry. If one person's anchor lies just inside a zone and the other's outside, counting one kept box in both runs can hide an application change. A stable tie policy is a product choice, not guaranteed by all NMS backends. [[S075](SOURCES.md#s075)]
- Native auto padding versus fixed square export padding: raw network inputs can differ despite equal image file and nominal size. A tensor mismatch here must not be attributed immediately to INT8. [[S072](SOURCES.md#s072)]
- Tensor supplied in `[0,255]` while the tensor path expects the caller to normalize: native image path and tensor path differ by scale. Sending already normalized data through image normalization can cause a second division. Test both API input kinds if used. [[S072](SOURCES.md#s072)]
- Forgetting top pad during inverse transformation gives plausible boxes with systematic vertical shift. Detector score tensors may agree perfectly while PPE-person association and danger-zone tests fail.
- ONNX NMS uses corner order `[y1,x1,y2,x2]` when `center_point_box=0`; blindly copying an `xyxy` adapter is wrong. The NMS overlap outcome alone may not reveal swapping x/y consistently, while displayed boxes and physical-zone anchors are wrong. [[S074](SOURCES.md#s074)]
- Export output already includes NMS, then host applies NMS again with different class policy or cap. One-image demo still looks plausible; crowd scenes diverge.
- Quantization calibration omits dark scenes or small PPE: proposed risk is unrepresentative activation ranges. It requires stratified validation, not an assertion of an observed failure. Redoing calibration on the final test set would change the evaluation protocol.
- Graph accepted and fast, but a critical head returns NaN or the class map swaps helmet/no-helmet. Loading success and throughput remain true; usefulness fails.
- Provider list includes the requested accelerator plus CPU: some nodes execute on CPU. Quality can agree and the target claim still be overstated. This behavior is documented for ORT; LinQ status remains unknown. [[S079](SOURCES.md#s079)]
- Only easy daytime frames agree, while the final negative-video workload becomes noisier. Aggregate AP and successful export do not establish false-alert workload or rare-event recall.

The regression set should include portrait/landscape/odd sizes, representative supported shape/batch extremes, empty scene and empty predictions, multiple nearby people/PPE, tiny and boundary objects, tied/near-threshold scores, overlapping boxes, unknown visibility, nonfinite/invalid synthetic outputs, stream cuts and threshold/dwell/zone-edge cases. This is a coverage checklist, not a promised sufficient sample size. Separate constructed semantic fixtures from representative deployment evaluation footage.


## F145 — Quantization and acceptance ownership
<a id="f145"></a>

ORT's documentation describes static activation parameters from calibration data and dynamic parameters computed during inference; it warns quantization can harm accuracy and supports weight/activation matching. Its CPU U8S8 saturation example is specifically architecture-dependent, demonstrating why an integer-format label is insufficient. These ORT recommendations are not evidence of LinQ format support. [[S076](SOURCES.md#s076)]

Proposed artifact record: calibration manifest/hash, split/selection method, input preprocessing, sample coverage rationale, quantizer/compiler version, static/dynamic/PTQ/QAT route, quantization format, tensor granularity/axis, scale/zero point/range, signedness, excluded operations/mixed precision, embedded calibration-cache hash and supported shape coverage. If unavailable from a proprietary compiler, mark fields unavailable. Recalibration, excluding sensitive ops or QAT creates a new candidate with a new hash and evaluation; none guarantees recovery. Pin resulting artifact rather than just the source weights.

| Acceptance item | Proposed accountable owner | Evidence required | Status here |
|---|---|---|---|
| Truth and useful alert definition | Task/product owner with annotation/evaluation owner | Observable state/event contract; event rule and evaluated exposure | Not supplied |
| Numeric and decoder conformance | Model/export engineer | Paired saved inputs/outputs, schema, error report, diagnosed boundary cases | Protocol only |
| Quality loss allowance | Task/evaluation owner, informed by deployment constraints | Predeclared per-class/person/event limits and paired held-out results | No numbers authorized |
| Quantization/calibration selection | Model engineer with deployment engineer | Frozen dev/calibration lineage and target compatibility | Unknown |
| Target execution/placement | Deployment engineer or SDK/device owner | Build, assignment/profiling evidence, actual runtime/device identity, fallback declaration | LinQ unverified |
| Final demonstration claim | Team owner | Exact artifact/config/manifest plus all applicable evidence above | Cannot claim verified target execution |

A vendor-specific placement/trace mechanism must be learned from the actual supplied LinQ SDK and device. No LinQ API, compiler option, ONNX operator support, integer type, profile, fallback prohibition or full-chip utilization is established here. The general requirements are: bind the runtime to a named device/configuration; identify the executed artifact; retain compilation/partition logs; determine whether unsupported ops fail, fall back or run on host; report host preprocessing/postprocessing separately; retain enough output/trace evidence to associate predictions with that run. If only model-core inference is on target, describe precisely that scope instead of implying whole-video-pipeline placement. Successful import is a smoke test only.


# W1_11 — сохранённые подробные наблюдения

Происхождение: [W1_11](_WORK/W1_11.md); [snapshots и локальные fixtures](_WORK/W1_11_SOURCES/). Контекст доступа и выполнения:  Research status: primary documentation and source inspection; no inference, SDK, target device or timing benchmark executed. Access: 2026-10-23 03:20–03:23 UTC (06:20–06:23 Europe/Moscow). Source downloads, individual retrieval timestamps and SHA-256 hashes: `W1_11_SOURCES/retrieval.json`.


**Уточнение сборки:** публичный blocking sync найден и сохранён; blanket unknown уточнён [F002](#f002). Actual environment остаётся unknown.


## F146 — Proposed protocol.
<a id="f146"></a>

**[F146](#f146) — Proposed protocol.** Report separately host-observed completed-request latency, verified device interval when available, frame age, and observable-event-to-delivered-alert delay. Each requires named start/end events and clock domain. Submission return is not necessarily completion. Throughput alone does not establish timely live analysis. No acceptance threshold follows from the supplied context.


## F147 — Unknown.
<a id="f147"></a>

**[F147](#f147) — Unknown.** No LinQ runtime/SDK version, asynchronous completion primitive, device clock or profiler was supplied. CUDA mechanisms below apply only to the NVIDIA baseline. They are not LinQ commands. Until LinQ completion semantics are verified, report host-observed results and mark device execution time unavailable. An RPC acknowledgement must not be relabeled target completion.


## F148 — Source inspection.
<a id="f148"></a>

**[F148](#f148) — Source inspection.** LoadGen v5.1 `QuerySamplesComplete` captures `PerfClock::now()` at entry. `ResponseDelegateDetailed::SampleComplete` computes latency from query scheduled time. Server scheduler separates scheduled and actual issue time; SingleStream waits for previous completion before assigning next start. Timing only after a worker dequeues excludes delay which scheduled-to-completion includes. Code read, not run. [[S082](SOURCES.md#s082), [S083](SOURCES.md#s083)]


## F149 — Counterexample.
<a id="f149"></a>

**[F149](#f149) — Counterexample.** `loadgen.h` permits an untimed response callback after completion timestamp capture; it can make accelerator data host-resident, and requires MLPerf approval. Therefore legitimate LoadGen completion does not universally mean all host output bytes are available, much less that an operator sees an alert. Preserve the actual benchmark rule; add a separate application delivery boundary. [[S084](SOURCES.md#s084)]


## F150 — Documentation.
<a id="f150"></a>

**[F150](#f150) — Documentation.** MLPerf distinguishes response-driven SingleStream, Poisson Server and bulk Offline workloads. Policies time from scheduled query presentation to received reply; Network division includes actual input/response transport. These are boundary/workload precedents, not safety deadlines or certification of camera replay. Policy HEAD and code v5.1 are different snapshots; no release-compliance claim is made. [[S085](SOURCES.md#s085)]


## F151 — NVIDIA documentation.
<a id="f151"></a>

**[F151](#f151) — NVIDIA documentation.** Host timing examples synchronize after enqueue. GPU-event examples record start/end in a stream and wait for end. Per-request synchronization can perturb overlap. Inference-only guidance excludes application-specific pre/postprocessing. Host and GPU intervals answer different questions. Its Python example uses `time.time()`; use a documented monotonic clock for our elapsed-time harness. [[S086](SOURCES.md#s086), [S089](SOURCES.md#s089)]


## F152 — NVIDIA documentation.
<a id="f152"></a>

**[F152](#f152) — NVIDIA documentation.** Archived `trtexec` examples explicitly omit transfers; queries/s differs from images/s for batch >1. The guide states defaults of at least 200 ms warmup, then at least 10 iterations or 3 seconds, whichever longer. These are tool defaults, not sufficient-duration recommendations. Environment guidance discusses clocks, power, temperature and transfers. Record actual installed version/options; documentation example results are not measured RTX 4070 performance. [[S087](SOURCES.md#s087), [S088](SOURCES.md#s088)]


## F153 — Clock documentation.
<a id="f153"></a>

**[F153](#f153) — Clock documentation.** Microsoft recommends QPC for same-system intervals and states it is independent of external time. Cross-machine UTC needs synchronization. Python 3.13 documents monotonic/performance counters, integer-nanosecond variants and clock implementation/resolution inspection. Units do not establish accuracy; unrelated monotonic origins cannot be subtracted. [[S089](SOURCES.md#s089), [S090](SOURCES.md#s090)]


## F154 — RTP/NTP documentation.
<a id="f154"></a>

**[F154](#f154) — RTP/NTP documentation.** RTP timestamps use a payload-defined clock and random initial offset; transmission order can differ from sampling order. RTCP sender reports pair RTP and NTP-reference time, but relative/zero NTP timestamps are allowed when absolute time is unavailable. RTSP transport alone does not prove accurate capture UTC. NTP defines offset/delay and dispersion/error concepts; enabling NTP supplies no measured numerical error bound here. [[S091](SOURCES.md#s091), [S092](SOURCES.md#s092)]


## F155 — Proposed timestamp contract
<a id="f155"></a>

These fields are schema names, not SDK APIs. Use a run manifest and records keyed by run, camera, stream-session, source-frame, request, batch and event/alert IDs. Reconnect creates a new session; repeated PTS is not unique identity. Every timestamp carries clock domain, units, event definition and provenance. Missing values are null with reason, never zero.

| Marker | Exact proposed boundary | Clock/qualification |
|---|---|---|
| media_pts | Source presentation/sampling position with rational time base | Media timeline; preserve origin/discontinuity; not assumed UTC |
| capture_time | Verified camera acquisition/sampling reference | Camera domain; unavailable until semantics/mapping verified |
| scheduled | Intended replay/request release | Harness monotonic |
| received | Complete compressed frame available at named receiver | Receiver monotonic; first packet would be another boundary |
| decoded | Frame ready for preprocessing | Host monotonic |
| submit | Runtime call entry after defined preprocessing | Host monotonic |
| submit_return | Runtime call returns with status | May mean enqueue/accept only |
| completion_observed | Documented fence/notification observed | Host monotonic; name actual primitive |
| output_ready | Required output usable by named host consumer | Includes required copy/wait |
| decision_ready | Association/tracking/temporal rules finish | Attach policy version |
| alert_delivered | Named destination confirms usable alert | Consumer domain or same host; send alone is another endpoint |
| ui_presented | Instrumented/observed display | Optional; backend queue insertion is insufficient |

Manifest: input/output shapes and precision; resize/color path; model/export/compiler hashes; device identity; runtime/driver versions; batch formation timeout; queue/drop policy; streams/workers; source cadence/resolution; compression/transport; host load; warm/cold state; duration. Record which stages execute locally/remotely.

For remote LinQ, client submit-to-client-output-ready on one monotonic clock is the primary completed-request interval. It includes serialization, network, remote queue/execution and response handling inside these boundaries. Server receive/compute/send intervals may be reported on its own clock. Never subtract server and client monotonic timestamps. Device timing needs a verified mechanism covering relevant streams/dependencies. A completion callback can follow physical completion; call it completion observed. Low latency does not prove target execution provenance.


## F156 — Proposed definitions.
<a id="f156"></a>

**[F156](#f156) — Proposed definitions.** Mechanical request-latency ground truth is reconciled event logs and IDs. Event-alert delay additionally needs independently annotated observable onset and the one-to-one GT/alert rule agreed with W1_05. Store native integer readings and conversions; interval units below are milliseconds.

| Quantity | Formula/population | Limit |
|---|---|---|
| Completed-call latency | output_ready − submit, unique valid successful requests | Earlier queue/preprocess excluded |
| Scheduled response latency | output_ready − scheduled | Includes dispatch/backlog; pair with failures |
| Receiver pipeline latency | decision_ready − received | Excludes upstream camera/network delay |
| Submission overhead | submit_return − submit | Not asynchronous execution duration |
| Device interval | Verified device end − start | Optional; identify mechanism |
| Frame age | mapped decision_ready − capture_time | Requires compatible reference clocks and uncertainty |
| Receive-age proxy | decision_ready − received | Label limited interval; capture age unknown |
| Event delivery delay | matched delivered alert − observable onset | Misses/censoring/duplicates reported separately |
| Useful throughput | unique valid successful results / elapsed seconds | Frames/s plus batches/s and images/batch |
| Request deadline success | valid logical requests completed by D / all eligible released requests | Drops/timeouts remain denominator |
| Timely event recall | matched GT episodes delivered by D / all eligible GT episodes | D owner-selected before test; report unknown/censored |

Report per-stream p50/p90/p95/p99, mean/max, n, elapsed duration and failures with raw records. Declare percentile implementation: proposed nearest rank x[ceil(p*n)] in 1-based sorted indexing, without interpolation. n=0 means unavailable, not zero; small-n tail percentiles may equal maximum. Do not average p99s and call it pooled p99. Provide request-weighted pooled and per-camera summaries: busy cameras otherwise dominate. Do not add component p99s; measure paired end-to-end intervals. Overlap prevents treating summed stage durations as elapsed time.

Reconcile released requests into disjoint outcomes at accounting close: valid success, failure, timeout without valid result, cancellation/drop after release, unresolved. Retain late arrivals and state the reconciliation rule. Retries have attempt IDs under one logical request; user-visible latency begins at original release. Separately count scheduled-never-released frames, deliberate sampling, decode losses, rejections and duplicate results. Fix drain/cutoff policy before run. Failed requests do not receive invented zero latency. Success-only percentiles can improve while most frames disappear, so report failure/deadline rates jointly. Empty results are not fast operation.


## F157 — File, RTSP and remote routes
<a id="f157"></a>

**File.** Separate unpaced throughput replay from paced queue/freshness replay. Preserve source media positions. For declared monotonic start m0, media origin p0, replay speed s, proposed due time is m0+(pts−p0)/s after time-base conversion. decision_ready−due_time is replay lag, not age of the originally filmed scene. Specify variable cadence, seek, missing-PTS and discontinuity policy. Source-seconds per wall-second does not prove every episode timely. Declare preload/caching and whether decode is included, consistently across comparisons.

**RTSP/RTP.** Receiver-boundary latency remains measurable without camera time. Capture-to-alert requires verified camera timestamp semantics, RTP/reference mapping and payload frequency, wrap/discontinuity/session handling, synchronization and buffering at camera/receiver/jitter buffer/decoder. Record mapping availability; arrival UTC is arrival, not acquisition. Ten seconds buffered upstream plus twenty-ms inference still yields old results. Reconnect/reset cannot silently join unrelated timelines.

**Remote.** Include transport and target queues in client-result metrics. Persist frame/request identities through batching and out-of-order completion. If protocol returns a job handle, distinguish accepted, completed and result downloaded using its actual documentation when supplied. Device-only profiling remains unavailable without verified support.

For clocks with defensible bounds, proposed worst-case age uncertainty is ±(capture error + delivery error + mapping error), also allowing timestamp-placement/quantization error. This sum requires no independence assumption. Statistical synchronization estimates must remain labeled estimates, not guaranteed bounds. Apparent negative age calls for clock/mapping investigation.


## F158 — Proposed protocol.
<a id="f158"></a>

**[F158](#f158) — Proposed protocol.** Separate compile/deployment, process/runtime initialization, model load, first successful result and warm steady inference. Define cold state: restart, retained/cleared cache, device power state, connection and model residency. Repeated warm calls are not repeated cold evidence. Record excluded warmup requests/duration, shape/profile changes and available clock/power/temperature telemetry; warmup does not prove thermal equilibrium.

Use workload cells varying source streams/cadence/resolution, batch/formation timeout, concurrent in-flight requests and workers, with fixed transfer scope. One outstanding request isolates response time; external paced arrivals expose queues suppressed by a wait-for-completion loop. Batch members retain their individual original release times, including batch-fill wait. Keep input/policy fixed and report quality: dropping frames changes event recall.

Proposed harness falsification checks, not executed:

1. Slow mocked asynchronous backend: verify submission returns before output readiness, IDs survive out-of-order results. This tests instrumentation, not target speed.
2. Add known receiver queue delay: receiver-to-result rises even if device interval stays constant; pre-receiver delay changes true capture age instead.
3. Overload paced replay: inspect growing age, drops and deadline success. A latest-frame policy can reduce age by discarding work; report the lost coverage.
4. Inject timeout/disconnect/duplicate/late replies; reconcile logical requests and avoid retry throughput inflation.
5. Synthetic wall-time jumps or isolated clock test: elapsed measurements use monotonic time; cross-host age remains unknown without useful synchronization evidence.

Pure mathematical example: 30 frames/s arrive, 20 frames/s complete FIFO, no other costs. Backlog grows about ten frames/s even if per-frame runtime stays 50 ms. Latest-frame replacement can improve age while reducing analyzed-frame coverage. This is not a device measurement or acceptance threshold.


## F159 — Handoff and unknowns
<a id="f159"></a>

Before measured claims obtain LinQ runtime/completion semantics, deployment/transfer topology, camera timestamp provenance and synchronization uncertainty, delivery endpoint, workload/drop policy and owner-selected deadlines. Host/client instrumentation can be specified without invented APIs. Coordinate event eligibility/misses with W1_05, load/failure/coverage with W1_12, execution provenance with W1_15. No source supplies a justified industrial safety deadline.


# W1_12 — сохранённые подробные наблюдения

Происхождение: [W1_12](_WORK/W1_12.md); [snapshots и локальные fixtures](_WORK/W1_12_SOURCES/). Контекст доступа и выполнения:  Checked: 2026-10-23, UTC (+00:00); precise retrieval times are in `_WORK/W1_12_SOURCES/retrieval.json`. Scope: proposed evaluation contract for industrial safety video analytics, including required LinQ inference. No hardware, LinQ SDK, running application, dataset or official acceptance targets were supplied. No load benchmark or application code was executed. English standalone research note.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F160 — Decision and evidence status
<a id="f160"></a>

**Decision:** every quality result needs its workload, missing-work ledger, exposure and freshness next to it. Fewer false alerts alone cannot establish improvement when less camera-time was analyzed. A request-success fraction and a fast latency percentile cannot establish video coverage or timely warnings.

Evidence labels used below: **DOC** = primary published documentation; **CODE** = source read at an immutable revision, not executed; **INFERENCE** = reasoning from explicitly stated assumptions; **PROPOSAL** = our evaluation convention, not an official contest or vendor standard; **UNKNOWN** = unresolved access/configuration/ground truth.


## F161 — DOC, S085:
<a id="f161"></a>

- **[F161](#f161) — DOC, [S085](SOURCES.md#s085):** MLPerf distinguishes Single Stream (next query after previous completion), Server/Interactive (Poisson arrivals), Offline (all samples issued initially) and Multistream (queries with eight samples, next query after completion). Its latency starts at scheduled query time, not merely actual dispatch. **INFERENCE:** closed-loop completion-driven tests reduce offered work when the system slows; they do not reproduce independent camera arrivals. MLPerf's term Multistream is a benchmark query pattern, not proof of eight independently paced video decoders. Its prescribed durations/percentiles are benchmark rules, not acceptance targets for this case.


## F162 — CODE, S093:
<a id="f162"></a>

- **[F162](#f162) — CODE, [S093](SOURCES.md#s093):** `ScheduleDistribution<TestScenario::Server>` uses exponential interarrival times; the response path records completion latency from `scheduled_time` and traces scheduling delay separately from issue-to-done time. `IssueQueries` flushes queries and obtains expected completion latencies before deriving active duration. This supports keeping delayed issue and tail completion visible. It does not provide a video truth/coverage protocol or prove arbitrary application failures are safely handled.


## F163 — DOC, S094:
<a id="f163"></a>

- **[F163](#f163) — DOC, [S094](SOURCES.md#s094):** LoadGen is model/data-format unaware and does not score output accuracy itself. The user must return completion for each received sample and assess the accuracy log. This clarifies an apparent simplification in the rules' description of LoadGen as responsible for validating accuracy: the framework supplies traffic/logging, while the task-specific scorer remains necessary. Our camera-time/event evaluator must therefore be explicit.


## F164 — DOC, S095:
<a id="f164"></a>

- **[F164](#f164) — DOC, [S095](SOURCES.md#s095):** Triton exposes successful/failed requests, inference samples and batch executions as different counts. A request may contain multiple samples; cached requests are excluded from inference/execution counts. Its pending gauge covers backend-waiting work, not all front-end activity or executing work. Failure categories include scheduler rejection, cancellation, backend and other errors. Ensemble/component failure counts can overlap. **INFERENCE:** do not sum per-model counters into unique user transactions, infer complete end-to-end success from backend success, or interpret zero pending as no outstanding work. These are examples of accounting boundaries, not a recommendation or assumption that LinQ uses Triton.


## F165 — DOC, S096:
<a id="f165"></a>

- **[F165](#f165) — DOC, [S096](SOURCES.md#s096):** GStreamer appsink queues samples and permits bounded queues with dropping of old/new buffers. `dropped`, `in`, `out`, `leaky-type` and current-level counters are documented since 1.28; `drop` is deprecated there. A null timed pull can mean stopped, EOS or timeout. **INFERENCE:** queue policy changes freshness and missing evidence; a missing frame cannot automatically be labeled a model rejection. Older installed versions may lack these counters. Appsink accounting does not measure upstream camera/network losses.


## F166 — DOC, S097:
<a id="f166"></a>

- **[F166](#f166) — DOC, [S097](SOURCES.md#s097):** Perf Analyzer separates constant outstanding-request concurrency from requested requests/second and supports supplied intervals or a fixed timestamp schedule. **INFERENCE:** offered rate, in-flight concurrency and stream count are distinct workload dimensions. A generator only attempts the schedule; actual schedule adherence needs measurement. Neither Poisson arrivals nor identical loops necessarily represent synchronized camera bursts.


## F167 — DOC, S098:
<a id="f167"></a>

- **[F167](#f167) — DOC, [S098](SOURCES.md#s098):** Google's SRE workbook separates SLI specification from instrumentation location and discusses pipeline freshness, coverage and correctness. Its coverage example counts expected versus processed records and explicitly notes that misconfiguration can hide records the pipeline never knew about. Client-side measurement can better reflect user experience. **INFERENCE:** the independent camera manifest and planned schedule must live outside the analyzed system's success log; otherwise an omitted camera can disappear from both numerator and denominator.


## F168 — Proposed immutable workload matrix (F168)
<a id="f168"></a>

Each cell is a run configuration, not a performance promise. Choose actual levels after source/device access; do not invent supported stream counts, FPS, resolutions or deadlines. Hold model weights, thresholds, temporal policy and video/GT fixed across load comparisons. Replaying the same scene under additional load can isolate scheduling degradation; it does not create independent accuracy samples.

| Dimension | Required record / deliberate variation | Failure this can reveal |
|---|---|---|
| Source and pacing | file as-fast-as-possible; file at source pacing; genuinely live source; original camera clock/PTS mapping; exact clip order | Offline throughput mistaken for live service |
| Streams | camera IDs, simultaneous count, per-camera phase, independent versus identical content | One starved camera hidden by aggregate throughput |
| Input/decode | source width/height, nominal and observed FPS, variable-rate timeline, codec/profile/bitrate where known; decoder and resize settings | Equal network FPS but unequal decode/pixel work |
| Analysis policy | fixed planned per-camera analysis schedule, source frame eligibility, model input dimensions, planned skipping, adaptive reduction | Quiet load shedding presented as accuracy gain |
| Request/execution | sample-to-request map, request batch size, dynamic batch policy, in-flight limit, device/model concurrency | Requests/s confused with frames/s or executions/s |
| Arrival pattern | steady independent pacing; synchronized phases; bounded burst; recorded arrival trace; random seed if used | Mean-rate test hides short queue overflow |
| Scene | people/crowding/PPE visibility, event duration, geometry, lighting, motion and per-frame object count strata | Heavy scenes dropped preferentially |
| Transport | local versus remote inference, bandwidth/latency/jitter/loss test conditions and injection point | Server-only timing hides network loss |
| Fault/recovery | camera disconnect; decode failure; inference error/timeout; result transport loss; model/process restart; reconnect | Work silently erased, stale replay, duplicate alerts |
| State/duration | cold start, warmup, steady interval, fault interval, recovery interval, end drain; separate start/end cutoffs | Warmup or draining silently omitted |
| Target | verified execution location, runtime/device/build, fallback route if any, temperatures/resource traces if available | Host fallback credited as LinQ capacity |

Test baseline → increased offered load → explicit overload → recovery, using a bounded chosen ladder. Change one load factor first; a small selected set of interactions (for example synchronized streams plus reconnect) follows observed bottlenecks. Numerical levels, run lengths, repetitions, burst envelopes, freshness deadlines and coverage limits require a team/organizer decision; none is established by these sources. Log offered and actually issued rate, schedule lag, backlog and resource use even when the generator misses its schedule.


## F169 — Proposed counters and reconciliation (F169)
<a id="f169"></a>

The counting unit is always explicit: **source frame**, **logical analysis opportunity**, **request attempt**, **batch execution**, **logical delivered result** or **alert**. Never add these together. Use immutable `(run_id, camera_id, source_session_id, source_frame_id/PTS)` identifiers; a reconnect changes session identity when timestamps/sequence numbers reset. Preserve parent logical ID and unique attempt ID for retries. Batched request IDs map to all contained frame IDs. Counters are deltas within an epoch; counter resets create a new epoch rather than negative work. Maintain IDs as audit evidence, not only totals.

1. **Source ledger.** For an offline file with known decoded timeline, list every eligible source frame or declared temporal sample. For live input, independently scheduled expected opportunities exist even when no frame arrives. Separate `not_received`, `received_decode_failed`, `decoded`, and `pending_decode` for the expected opportunities. Account for duplicates/reordering explicitly. Nominal FPS times elapsed time is only an expectation for live/variable-rate sources, not an exact emitted-frame count. If emission/transport loss cannot be localized, report unknown at that boundary rather than fabricate an equation from absent logs.
2. **Policy ledger.** For every decoded eligible frame: planned exclusion (declared policy), selected logical opportunity, or unresolved policy record. For every selected opportunity at cutoff: `pre_submit_drop`, `submitted_at_least_once`, or `pending_pre_submit`. A fixed policy may intentionally sample fewer frames than the source; report this as planned sampling, separately from overload drops. A changed/adaptive policy is a changed evaluated system.
3. **Attempt ledger.** At the client boundary: `attempts_started = successful_valid_response + explicit_error + timeout_or_canceled + unresolved_at_cutoff`. Terminal bins are exclusive at the chosen cutoff; an eventual late response after timeout is a supplemental observation linked to that attempt, not a second successful terminal attempt. Record timeout, rejection, backend error, transport error and schema/parity failure separately where evidence supports attribution. A client timeout does not prove the device stopped executing.
4. **Logical result ledger.** Deduplicate attempts by logical opportunity. `selected = valid_delivered_by_deadline + valid_delivered_late + failed_without_valid_result + dropped_without_submission + unresolved` at final adjudication. Define valid as the expected complete output/schema at the chosen end-to-end boundary; an empty detection list can be a valid result, while an absent response is not. A result may be transport-valid yet semantically wrong; correctness belongs to the GT evaluator. Record stage-local successes separately from final delivery.
5. **Alert ledger.** Distinguish candidate, suppressed, attempted-delivery and actual delivered alert IDs. Link delivered repeats/retries to their event and delivery attempt. Keep duplicates as operator workload under the chosen event rule. Failure/recovery notifications are separate from violation alerts. A confirmed device result or emitted network message does not prove UI receipt; instrument the boundary claimed by the report.

These are **proposed disjoint accounting partitions**, conditional on trustworthy IDs and complete logs at each boundary; no vendor counter guarantees them. A conservation residual is reported as unexplained work with count and camera/time, not forced into successes. Pending work is a gauge at cutoff, not an accumulated failure counter. Publish start/end outstanding counts, stopping rule and drain duration. Distinguish results for work scheduled within the measurement interval from any carry-in from a prior interval. Warmup and drain have their own accounting.

**Useful request-level metrics:** attempt error fraction = `(explicit_error + timeout_or_canceled)/attempts_started`, alongside unresolved fraction; logical on-time completion fraction = `valid_delivered_by_deadline/selected`; unique delivered frames per measured wall second; batch executions per wall second; per-camera offered, admitted and delivered rates; maximum and sampled backlog. Error categories are conditional on the selected boundary. A rejected request still counts in offered work; repeated attempts increase attempt denominator but never unique opportunity denominator. Give raw counts. For a zero denominator report N/A, not zero errors or 100% availability.


## F170 — Wall time, camera-time and review exposure are separate (F170)
<a id="f170"></a>

Let `W` be host-monotonic measured run duration in seconds. Let `I_c` be the predeclared source-time interval expected from camera `c`. Define `H_requested = sum_c length(I_c)/3600` camera-hours. Ten cameras over one simultaneous hour give ten camera-hours but one wall hour. An offline clip of ten source hours may take a different wall time to process. A file completion benchmark therefore needs both source duration and elapsed wall duration.

Maintain interval masks on source time, per camera and task:

- `R`: independently reviewed/annotated intervals with sufficiently complete truth for the claimed question. Reviewing only emitted alerts can judge sampled alert precision but cannot establish missed-event recall or reviewed negative exposure.
- `O`: source evidence adequate for the target property to be judged (task observability). Hidden heads may be unobservable for helmet state while the same interval is observable for person presence. This is an annotation fact, not an algorithm abstention.
- `A`: intervals for which the declared analysis sampling/temporal support contract was actually completed with valid results. Derive this from scheduled opportunity IDs and a predeclared mapping to source intervals. One processed frame must not confer coverage over the entire intervening gap. If no defensible temporal support mapping exists, publish frame/sample completion and gap distributions; do not invent processed camera-hours.
- `F`: intervals with adequate recent results at the operational boundary within the declared freshness/deadline rule. A stale cached status is not fresh coverage. Separately flag whether state was reset/reinitialized after a gap or reconnect.

Report `H_reviewed`, `H_observable_reviewed`, `H_analyzed_under_policy`, and `H_fresh_under_policy` as measures of the corresponding masks, in camera-hours. Also report intersections actually used by a metric, e.g. `H_R∩O∩A`; masks overlap and must not be summed. Publish `coverage = H_A/H_requested`, fresh coverage `H_F/H_requested`, per-camera values, worst camera, longest missing interval and inter-result gap distributions. The independent manifest includes entirely absent cameras. The resolution/sampling policy accompanies each exposure value; equal camera-hours at different sampling density do not imply equal ability to observe short violations.

**Live freshness needs another axis.** Frame age at result receipt is `receipt time − mapped source capture time`; it is meaningful only with source-to-receiver clock mapping and stated synchronization error. Source PTS alone may not identify wall-clock capture time. If mapping is unknown, label true age unknown and report receiver-local residence/queue delay separately. Time since latest receipt does not prove scene freshness, because an old frame can arrive now. No alert is not evidence of freshness. Freshness thresholds are configurable protocol parameters requiring an owner, not universal safety values.

**Availability is named by its predicate.** A health endpoint uptime fraction establishes that endpoint's availability. Proposed analytic availability is camera-time satisfying the declared valid-result/cadence predicate; proposed useful live availability additionally requires freshness and delivery. Publish requested-time denominators including startup and failures for the end-to-end claim, plus clearly labeled steady-state subsets. Algorithmic `unknown`/abstention, unobservable GT, transport absence and invalid output are separate states. Do not convert any of them to a negative safety decision.


## F171 — Joint quality reporting that cannot improve by censoring hard work (F171)
<a id="f171"></a>

Use two views on the **same requested source footage and independent truth**:

1. **End-to-end operational view:** all reviewed observable GT episodes in the fixed requested footage remain in the recall denominator, whether frames were dropped, inference failed or alerts arrived too late. Match only actually delivered valid timely alerts using the separately specified one-to-one temporal/event contract. A known GT episode missed during downtime is an end-to-end miss, with cause annotated as unavailable rather than model misclassification. Report late detections separately. This is the main comparison for useful warnings.
2. **Conditional diagnostic view:** quality only where analysis was completed under the declared support contract. Explicitly name its restricted mask and episode eligibility rule. It can localize model behavior; it is vulnerable to selection bias and cannot replace view 1. Use a fixed common support intersection for a paired diagnostic comparison, while showing how much/requested work that intersection discards.

False-alert reporting needs both actual operator workload and exposure. Count delivered false/duplicate alerts according to the frozen event taxonomy, and report raw count, false alerts per fully reviewed applicable requested camera-hour, plus the conditional rate per reviewed analyzed camera-hour. The former describes observed delivered burden under this run's availability; it cannot establish detector improvement without recall/coverage. The latter can still be selected toward easy footage. Never count unreviewed hours as verified no-false-alert exposure. Reviewing alerts alone can estimate their false fraction under a declared sampling design, but is not continuous-video negative coverage. Alerts with unknown truth stay unresolved; provide count and denominator handling. If full requested footage is unreviewed or unavailable, call full-window quality unknown rather than treating outage periods as no violations.

**Mathematical counterexample, not measurements ([F171](#f171)):** A and B each receive the same ten reviewed camera-hours containing ten GT episodes. A analyzes all ten hours and delivers eight timely true alerts plus ten false alerts. B processes only the first hour, containing one GT episode, delivering one true alert plus one false alert. Raw false count improves 10→1, and false alerts/requested camera-hour improve 1→0.1; neither shows better safety performance. B's analyzed-time false rate is still 1/hour; requested-footage recall falls 8/10→1/10, and coverage falls 100%→10%. Conditional recall can be 100% for B because it excluded nine episodes. These figures require complete independent truth, identical matching and valid temporal support masks. In real unrecorded downtime the nine episodes might be unknowable; the proper conclusion is missing evidence and coverage loss, not a computed event recall.


## F172 — Latency, faults and recovery (F172)
<a id="f172"></a>

Report successful-response latency distributions with sample count, measurement endpoints, wall interval, workload and failure/unresolved fractions. Successful-only p95 can decrease when the slowest requests time out. Do not assign failed requests zero latency or silently delete them; report deadline completion fraction across all scheduled logical opportunities, late fraction, failed fraction and pending fraction next to p50/p95/p99 where sample counts support those quantiles. Do not claim a failed request's eventual latency is infinite or a known finite value: it is unobserved/censored at cutoff. A timeout's elapsed time is time-to-timeout, not inference completion time.

For each bounded fault exercise record planned fault interval and location, observed affected camera-time, first error, last fresh result, reconnect attempts, first valid new-session frame, first fresh useful result and restored cadence. Specify recovery predicate before the run. A successful reconnect alone need not mean decoded frames, correct model state or timely delivery. Replaying an accumulated backlog can restore completeness later while live freshness remains poor. Dropping old frames may restore freshness while lowering coverage. Report both outcomes. Preserve event states across failure only under a declared policy; test repeated notifications, ID/session resets and false violation persistence after recovery. No particular recovery behavior is prescribed without application semantics.


## F173 — Minimal report row and decisions affected
<a id="f173"></a>

**One workload cell row:** run/config/artifact hashes; target execution evidence; camera manifest and source intervals; wall time including labeled warmup/drain; offered/actual rates and schedule lag; source/selected/request/batch/unique-result counts; error/drop/pending counts by boundary; per-camera reviewed/observable/analyzed/fresh camera-hours and longest gaps; delivered true/false/duplicate/unresolved alerts; requested-footage timely recall where GT supports it; conditional quality with coverage; success-only latency count/quantiles alongside on-time/late/failure fractions. Attach logs and masks so totals can be reconciled.

Transfers: **video_architecture** needs IDs, clock mapping, independent expected workload, queue/drop boundaries and reconnect epochs ([F162](#f162)/[F164](#f164)/[F165](#f165)/[F167](#f167); [F169](#f169)/[F170](#f170)/[F172](#f172)). **operator_product** needs receipt evidence, stale/unknown status and duplicate notification accounting ([F169](#f169)/[F170](#f170)/[F171](#f171)). **training_strategy/model_stack** must freeze policy when comparing quality and disclose adaptive resolution/FPS/fallback changes ([F168](#f168)/[F171](#f171)). **hackathon_strategy** can claim only cells actually exercised on the verified target; an offline throughput result cannot establish multi-camera live coverage ([F161](#f161)/[F166](#f166)).


## F174 — Local execution and unresolved questions
<a id="f174"></a>

Locally executed only small retrieval/provenance tasks: GitHub commit lookup, `git ls-remote`, HTTP downloads, text extraction and source inspection. No inference, fault injection, hardware counters, latency or coverage measurements. [F171](#f171) is exact illustrative arithmetic, not a model test.

**[Q013](OPEN_QUESTIONS.md#q013):** What independently records actual camera emission, source sessions/capture timestamps and requested monitoring intervals? Without it, distinguish expected schedule coverage from proven emitted-frame loss.

**[Q008](OPEN_QUESTIONS.md#q008):** What analysis cadence/temporal support and freshness deadline does the task owner require per event type? Source FPS alone does not determine sufficient event visibility; unknown short-event coverage must remain unknown.

**[Q009](OPEN_QUESTIONS.md#q009):** What are actual LinQ runtime, transport, batching, timeout/cancellation, completion and fallback observability capabilities? Sources here intentionally do not invent APIs or target capacity.

**[Q014](OPEN_QUESTIONS.md#q014):** Is independent full requested-footage GT available under faults and which UI/delivery boundary can be instrumented? Without it, quantify missing work and restricted quality rather than full operational recall.


# W1_13 — сохранённые подробные наблюдения

Происхождение: [W1_13](_WORK/W1_13.md); [snapshots и локальные fixtures](_WORK/W1_13_SOURCES/). Контекст доступа и выполнения:  Prepared 2026-10-23; research access around 03:27–03:33 UTC (06:27–06:33 Europe/Moscow, UTC+03:00). Scope: evaluation methodology for industrial safety video analytics, with no organizer dataset, evaluator or measured system outputs supplied. All numbers below are mathematical examples or locally executed calculations on invented arrays, **not model tests**. No acceptance threshold or universal minimum sample size is proposed.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F175 — Decisions supported
<a id="f175"></a>

1. Define the target population and independent sampling unit before choosing an interval. Thousands of adjacent frames from one incident do not provide thousands of independent incident trials. For claims about new cameras, count independent cameras/sites, not just episodes or frames.
2. Compare frozen systems A and B on the same truth, video, exposure and matching policy. Resample whole independent groups jointly for both systems and recompute the difference. `paired=True` in SciPy preserves corresponding indices; the caller must make those indices represent the independent groups.
3. With very few groups, give raw counts, per-group results and leave-one-group-out sensitivity. A bootstrap interval can describe sensitivity to the observed groups; it does not by itself justify a nominal population coverage claim.
4. Zero observed failures require a nonzero uncertainty bound under explicit binomial or Poisson assumptions. An ordinary bootstrap on all zeros cannot discover an unobserved failure.
5. Separate sampling uncertainty, run/seed variability, selection optimism, annotation uncertainty and domain uncertainty. Increasing bootstrap draws only reduces simulation noise conditional on the same data.


## F176 — Documentation, SciPy bootstrap [S099].
<a id="f176"></a>

**[F176](#f176) — Documentation, SciPy bootstrap [[S099](SOURCES.md#s099)].** The current documentation rendered as SciPy 1.18.0. Its API exposes paired index resampling, percentile/basic/BCa intervals, sample axis, number of resamples, and an RNG. Defaults include 9,999 resamples, unpaired samples and BCa. It warns that degenerate data may produce undefined BCa bounds. The RNG keyword changed in 1.15.0; new code should use `rng`. None of these options identifies video dependence or selects a cluster structure.


## F177 — Source inspected and execution version [S100, S101, F185].
<a id="f177"></a>

**[F177](#f177) — Source inspected and execution version [[S100](SOURCES.md#s100), [S101](SOURCES.md#s101), [F185](#f185)].** Local Python 3.11.9, SciPy 1.17.1, NumPy 2.4.2. SciPy reports git revision `527eb7fd7953a1de068f94bf8b322f249b9405ae`, matching the peeled release tag. Pinned `_resampling.py` wraps paired statistics with a common index sample; `_bootstrap_resample` draws indices with replacement along the observation dimension. Pinned `_binomtest.py` inverts binomial tails for exact proportion bounds, using half alpha for two-sided bounds and full alpha for one-sided bounds; the alternative stored by `binomtest` controls the interval direction. This is code inspection plus a small executable check, not a verification of every SciPy branch.


## F178 — Published methodology [S102, S103].
<a id="f178"></a>

**[F178](#f178) — Published methodology [[S102](SOURCES.md#s102), [S103](SOURCES.md#s103)].** Field and Welsh analyze bootstrap consistency for particular clustered-data models: validity depends on both the bootstrap and the generating model. Cameron and Miller discuss regression inference with independent clusters and dependent observations within clusters; few-cluster inference can remain unreliable, including some pairs cluster bootstrap procedures. Their regression corrections are not a ready-made event recall evaluator. This evidence supports caution about pseudoreplication and tiny numbers of groups, not an automatic transfer of an econometric method to this task.


## F179 — Documentation, proportions [S104].
<a id="f179"></a>

**[F179](#f179) — Documentation, proportions [[S104](SOURCES.md#s104)].** `binomtest(k, n, alternative=...).proportion_ci(confidence_level=.95, method='exact')` returns Clopper–Pearson bounds; `wilson` and `wilsoncc` are alternatives. These APIs concern a binomial proportion, requiring a suitable Bernoulli-trial model for the interpretation. They do not make correlated episodes independent. A confidence interval describes a procedure's coverage under its assumptions, not a posterior probability that the fixed unknown parameter lies inside this realized interval.


## F180 — Documentation, rate [S105, S106].
<a id="f180"></a>

**[F180](#f180) — Documentation, rate [[S105](SOURCES.md#s105), [S106](SOURCES.md#s106)].** R `stats::poisson.test(x, T, ...)` is documented for Poisson rates/rate ratios, with exposure in `T`; this page identifies package stats 4.6.0 and was not executed. SciPy's Poisson probability mass function gives `P(N=0)=exp(-mu)`. Therefore with known exposure `T` and a homogeneous Poisson process, the one-sided 95% zero-count upper rate is `-log(.05)/T`. This derivation assumes the count/exposure mechanism, not just a label saying camera-hours.


## F181 — Documentation, paired binary outcomes [S107].
<a id="f181"></a>

**[F181](#f181) — Documentation, paired binary outcomes [[S107](SOURCES.md#s107)].** Statsmodels documents `mcnemar(table, exact=True, correction=True)`: the exact case uses a binomial distribution of discordant paired outcomes; continuity correction belongs to the chi-square approximation. This is useful for independent paired binary episodes. It is not a general interval for AP, F1, alert rates or clustered event outcomes.


## F182 — Published methodology, selection and variability [S108, S109].
<a id="f182"></a>

**[F182](#f182) — Published methodology, selection and variability [[S108](SOURCES.md#s108), [S109](SOURCES.md#s109)].** Cawley and Talbot demonstrate overfitting of model selection criteria and subsequent optimistic evaluation; their discussion includes nested evaluation. Bouthillier et al. study variability from data sampling, initialization and hyperparameter choices, showing that seed-only repetitions do not cover the whole benchmark procedure. These publications do not quantify the uncertainty of the present unseen dataset. Their study-specific compute gains or sample sizes are not transferred here.


## F183 — Proposed evaluation contract: population first
<a id="f183"></a>

The following is **our proposed protocol/inference**, not an organizer rule or a result proved for these data.

| Intended claim | Plausible unit for sampling uncertainty | Required qualification |
|---|---|---|
| Performance on this fixed annotated corpus | No sampling interval needed for the corpus value itself | Counts and evaluator rules suffice for a descriptive value; annotation and stochastic execution may remain uncertain |
| Future time on the same installed cameras | Independent recording sessions/days or sufficiently justified temporal blocks within each fixed camera | A block duration must be justified by dependence and incident duration; arbitrary frame chopping is insufficient |
| New cameras from a defined deployment population | Camera, or site when cameras share conditions/incidents | The observed cameras must plausibly represent that population; a convenience sample does not become representative after bootstrap |
| New industrial sites | Site | Multiple cameras within one site cannot establish between-site variation |
| Re-training the algorithm | A full run, including declared data split/tuning procedure | Same test corpus across seeds is crossed reuse of the corpus, not additional independent footage |

People, events and cameras may form nested or crossed dependencies. The same worker on repeated days, synchronized cameras viewing one episode, or one smoke source affecting multiple views can make camera rows dependent. Choose a group high enough to preserve the relevant dependence, document this judgment, and retain the event linkage. More aggregation can leave too few groups; that is an evidence limitation, not a reason to pretend independence at a lower level. A mixed-effects/parametric model could add assumptions, but needs separate justification and diagnostics.


## F184 — Metrics and paired grouped resampling
<a id="f184"></a>

Freeze the person/event truth, visibility/unknown policy, one-to-one event matching rules, temporal tolerance, confidence threshold, cooldown, and delivery point before A/B comparison. This cell does not invent the matching contract; it requires the selected contract to be identical. For each group retain at least GT event count, matched GT count, emitted alert count, matched alert count, false/duplicate alert count, and evaluated exposure for each system.

| Quantity | Numerator / denominator | Aggregation and empty cases |
|---|---|---|
| Event recall | Matched eligible GT violation episodes / all eligible GT violation episodes | Micro: ratio of sums. No GT positives: undefined, not 100%; keep the group's exposure/FP evidence |
| Delivered alert precision | Matched delivered alerts / all eligible delivered alerts | No delivered alerts: undefined; zero recall may coexist with no alerts. Duplicates follow the frozen matching rule |
| False alerts per camera-hour | Delivered unmatched/false alerts / fully evaluated eligible camera-hours | Sum counts and exposure; same time window for A/B. No exposure: undefined. Unreviewed time cannot establish a false-alert count |
| A/B difference | Metric(B) minus metric(A), with declared sign | Recall differences in percentage points; alert-rate differences in alerts/hour. Do not infer difference uncertainty from overlap of two separate intervals |

Unknown/ignore observations are excluded only by a truth policy fixed independently of model success. Publish their count and exposure, plus coverage of observable opportunities; otherwise dropping hard cases can increase apparent performance. Camera-specific recall with no positives must not silently disappear from a macro average presented as covering all cameras. Separate a macro average over positive-bearing cameras from exposure-weighted micro recall and state its population meaning. A change in analyzed coverage is itself an outcome; where coverage differs, report paired common-window quality plus each system's coverage/failures. Never claim improvement from a lower FP count caused by dropped analysis.

For a new-camera claim with `G` independent camera groups, draw `G` group IDs with replacement; carry each selected camera's entire GT and A/B predictions/exposure together. Recompute the chosen metric and its B−A difference each draw. Repeated selections create separate copies: namespace GT/prediction IDs by draw instance to avoid matching the copies against one another. For nonlinear metrics such as AP or temporal matching, rerun the pinned evaluator on those copies, including global score ranking where relevant. Averaging per-camera AP is a different statistic from pooled AP. For metrics reducible to sufficient counts, paired arrays of group counts and denominators are enough.

An illustrative **executed calculation** in [F185](#f185) uses `bootstrap((a,b,n), delta, paired=True, vectorized=True, method='percentile', rng=13, n_resamples=9999)`, where `delta(a,b,n,axis=-1)` is `(sum(b)-sum(a))/sum(n)`. These array elements are whole-camera matched counts and GT counts. The percentile choice is explicit for illustration; it has no promised coverage with four cameras. The same common-index principle applies to camera FP counts and exposures. Applying `paired=True` to per-frame arrays would preserve A/B correspondence while still resampling the wrong independence unit.

For a fixed-camera claim with multiple independent sessions, preserve camera identity and sample the relevant sessions within camera, or use a justified multistage scheme matching the actual sampling design. Do not add an inner iid frame resample to a camera bootstrap by default: that changes the sampling model and can destroy temporal events. Block/session results require sensitivity to block definition, event boundary/censoring rules, and dependence beyond a block. No block length is justified by the current context.


## F185 — Small examples and concrete failures
<a id="f185"></a>

All numbers below were executed locally in [F185](#f185) from invented data; outputs are preserved in `W1_13_SOURCES/examples.txt`.


## F186 — Zero errors, one positive, and absent denominators
<a id="f186"></a>

Under **independent Bernoulli trials with one common probability**, exact 95% two-sided bounds are:

| Observation | Estimate | Clopper–Pearson interval |
|---|---:|---:|
| 0 failures / 20 trials | 0 | [0, 0.168433] |
| 20 detected / 20 true events | 1 | [0.831567, 1] |
| 1 detected / 1 true event | 1 | [0.025, 1] |
| 1 detected / 5 true events | 0.2 | [0.005051, 0.716418] |
| 0 detected / 1 true event | 0 | [0, 0.975] |

For zero failures in 20 trials, a **one-sided** 95% upper bound is 0.139108; for 20 successes the one-sided lower bound is 0.860892. The former follows `(1-p)^20=.05`, so `p_upper=1-.05**(1/20)`. Do not interchange these with two-sided 95% limits. Twenty correlated frames from one event do not meet the independent-trial premise. With zero GT positive events, recall has no denominator; there is no binomial recall estimate to bound. With only one positive episode one can state exactly how that episode performed, but cannot establish stable high recall.

On twenty zero-valued observations, SciPy 1.17.1 BCa produced NaN bounds and a `DegenerateDataWarning` (also a runtime warning); the percentile interval was exactly [0,0]. This is an observed counterexample to treating any successful bootstrap call as evidence of zero risk. A library fallback from BCa to percentile fixes a numerical display, not the missing failure information.


## F187 — Rates and exposure
<a id="f187"></a>

Under a homogeneous Poisson count assumption, 0 false alerts / 10 evaluated camera-hours gives one-sided 95% upper 0.299573 alerts/hour. A two-sided 95% exact interval is [0, 0.368888] alerts/hour. With 1 false alert / 10 hours the two-sided interval is approximately [0.002532, 0.557164] alerts/hour. These are rate bounds, not probabilities per frame or per person.

The two-sided calculations use `L=chi2.ppf(.025,2*k)/(2*T)` for `k>0`, otherwise `L=0`; `U=chi2.ppf(.975,2*(k+1))/(2*T)`. They are mathematical Poisson-tail inversions implemented here through SciPy chi-square quantiles, not execution of R's `poisson.test`. `scipy.stats.poisson.interval(.95, mu)` instead returns a count-distribution interval for an already specified mean; it must not be substituted as an interval estimate for an unknown rate.

Bursting duplicate alerts or heterogeneous dependent cameras can violate the simple Poisson model. A no-alert blackout gives no evidence about the false-alert rate of a functioning system. Pooling 10 hours across observed cameras can bound only an assumed common/pooled exposure rate; it cannot provide a worst-camera guarantee or bound an unseen camera's rate. Specify the sampling/exposure model or label these bounds illustrative.


## F188 — Paired comparison, weighting and few groups
<a id="f188"></a>

Four invented cameras have GT positives `[10,2,5,1]`, A matches `[9,1,4,0]`, and B matches `[10,1,3,1]`. Pooled recall is A=0.777778, B=0.833333, improvement 0.055556 (5.56 percentage points). The paired camera percentile bootstrap at seed 13 gives difference interval approximately [−0.142857, 0.333333]. With only four groups this is a sensitivity display conditional on those cameras, not a certified 95% new-camera statement. Macro recall instead changes from 0.55 to 0.775, difference 0.225: weighting alone changes the headline.

If only one of four cameras contains positive events, an ordinary four-camera resample has no positives with probability `(3/4)^4=0.31640625`. Thus almost a third of resamples have undefined pooled recall. Do not discard them and call the remaining conditional quantiles the original 95% procedure. Report undefined fraction and insufficient support; restricting to positive cameras changes the estimand. BCa jackknife deletion of the sole positive group also exposes the problem. Stratification can be appropriate if the sampling design truly fixes positive/negative strata, but must not manufacture missing positive-camera diversity.

For independent paired binary event outcomes, let `b` be episodes correct only for A and `c` correct only for B. The exact McNemar comparison conditions on `b+c` and tests a binomial probability 0.5. An invented `b=1,c=2` yields two-sided p=1.0, despite B having one more correct event. This does not prove equality; it reflects very little discordant information. Repeated events within one camera or one physical incident invalidate the independent-pair premise unless handled at the appropriate group/model level. McNemar does not test FP/hour or provide a joint workload/recall decision.


## F189 — Selection, seeds and reporting recommendation
<a id="f189"></a>

Freeze the operating point using training/development/validation footage; log all tried models, thresholds, temporal rules and seeds. Evaluate the frozen candidates on reserved groups. Selecting the highest test recall among many trials and bootstrapping only that winner estimates conditional sampling variation while omitting the selection optimism. Either preserve an untouched final test set or, where justified and feasible, put the whole selection procedure inside an outer grouped evaluation. Repeated overlapping folds are dependent; the number of fold scores is not automatically the number of independent data samples.

For one trained A and B, a paired group interval concerns those frozen artifacts. For an algorithmic claim, add repeated full training/tuning runs using a predeclared budget and matching data partitions across A/B. Show every run and seed; do not select a lucky seed after seeing the final test. Record separate seeds for split, training/augmentation and resampling. A fixed seed gives repeatability of a draw sequence, not robustness. Multiple inference runs on identical deterministic predictions add no dataset evidence. Repeated seeds on one fixed test set do not turn that set into independent test corpora. With too little budget, explicitly restrict the claim to the tested artifacts rather than pretending to have quantified training variation.

Recommended report row: metric and sign; value and raw numerator/denominator; GT/matching/evaluator revision; eligible and unknown counts; population; group definition and group count; camera/site/session breakdown; coverage/exposure; interval method/level/one- or two-sided direction; RNG/library versions and resample count; invalid/degenerate resamples; paired difference; per-group values and leave-one-group-out range; tuning/selection history; tested artifact hashes. The full range across annotations or domain scenarios is a separate sensitivity analysis, not a sampling confidence interval.

Annotations should be adjudicated or evaluated under specified alternative plausible truths, preserving both versions. A narrow bootstrap interval around mislabeled truth does not correct annotation bias. No statistical interval on existing cameras accounts automatically for a new plant, camera angle, season, clothing policy or unobserved violation class. These uncertainties remain unresolved until actual sampling/annotation/device contracts are available.


# W1_14 — сохранённые подробные наблюдения

Происхождение: [W1_14](_WORK/W1_14.md); [snapshots и локальные fixtures](_WORK/W1_14_SOURCES/). Контекст доступа и выполнения:  Checked: 2026-10-23, approximately 06:25–06:35 Europe/Moscow (UTC+03:00). Actual per-download UTC timestamps and SHA256 are in [retrieval.json](_WORK/W1_14_SOURCES/retrieval.json). Scope: evaluation research for industrial-safety video analytics; no organizer dataset, official evaluator, LinQ SDK/device access, or measured system outputs supplied. Helmet/respirator/zone/smoking examples do not establish the complete task taxonomy.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F190 — Decision and evidence status
<a id="f190"></a>

Use two connected records: **what observable output went wrong** and **what evidence supports a cause**. A missing alert is an outcome; “detector failed” is a hypothesis until upstream input, annotation, association, temporal policy and delivery are checked. Prioritize fixes with paired full-chain outcomes and component interventions, while preserving conditional oracle results separately.

Legend: DOC = primary documentation/paper method; CODE = inspected source, not executed; PUB = authors' published result; LOCAL = executed mathematical illustration; PROPOSED = our evaluation design; INFERENCE = our conclusion; UNKNOWN = unavailable evidence. No TIDE, detector, tracker, export or LinQ benchmark was run. Python has numpy, but pycocotools was absent; there was no dependency installation. Downloading and inspecting code does not constitute reproducing the paper.


## F191 — DOC; TIDE is an output-error diagnostic.
<a id="f191"></a>

**[F191](#f191) — DOC; TIDE is an output-error diagnostic.** TIDE partitions detection errors into classification, localization, both, duplicate, background and missed GT. Its oracle score is ΔAP = AP after fixing one category minus baseline AP. Each category starts from the same baseline; progressive fixes change apparent importance with order. Missed-GT repair reduces the GT count rather than inventing a confidence for a new detection. These are metric counterfactuals, not deployable repairs. The paper uses foreground/background IoU thresholds; defaults are 0.5/0.1. See [[S110](SOURCES.md#s110)](https://arxiv.org/abs/2008.08115v2), §2.2–2.3 and appendix B.1–B.2.


## F192 — CODE; pin the executable definition.
<a id="f192"></a>

**[F192](#f192) — CODE; pin the executable definition.** Inspected TIDE commit `49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1`, version 1.0.1. In `quantify.py`, `TIDEExample._run` sorts predictions by score, caps the image list by `max_dets`, and greedily matches same-class GT at IoU ≥ positive threshold, marking GT used. `TIDERun._eval_image` checks Box, Class, Duplicate, Background, then Other; ignored predictions may participate in error analysis. `fix_main_errors(progressive=False)` separately repairs categories and clips negative ΔAP to zero. Exact-threshold cases need fixtures: its Box branch includes both endpoints (`bg_thresh <= IoU <= pos_thresh`) and precedes Duplicate. For an already-used same-class GT at exactly the positive threshold, this can select Box rather than Duplicate. This is a code-reading observation, not an executed counterexample. [[S111](SOURCES.md#s111)](https://github.com/dbolya/tide/blob/49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1/tidecv/quantify.py#L198).


## F193 — CODE; AP conventions and empty cases must travel with the chart.
<a id="f193"></a>

**[F193](#f193) — CODE; AP conventions and empty cases must travel with the chart.** `APDataObject.get_ap` computes cumulative TP/(TP+FP), TP/nonignored-GT recall, a precision envelope and mean precision at 101 recall locations, scaled to 0–100. Zero GT returns AP 0. `ClassedAPDataObject.get_mAP` averages nonempty objects; prediction-only classes can therefore contribute zero, while completely absent classes are omitted. A wholly empty run needs a guard outside the bare mean (no denominator guard there). Default error analysis is AP50; `evaluate_range` can report a threshold range while storing errors at its selected positive threshold. Therefore do not label its default ΔAP as COCO AP50:95 error contribution. [[S112](SOURCES.md#s112)](https://github.com/dbolya/tide/blob/49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1/tidecv/ap.py#L71), [[S111](SOURCES.md#s111)](https://github.com/dbolya/tide/blob/49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1/tidecv/quantify.py#L459).


## F194 — DOC/PUB; ignore handling changes the diagnosis.
<a id="f194"></a>

**[F194](#f194) — DOC/PUB; ignore handling changes the diagnosis.** TIDE's v1.0.1 changelog reports that previously excluding ignored predictions from oracle repair overrepresented Missed and underrepresented Class/Loc, materially changing LVIS conclusions. The authors report smaller changes on COCO; that is their result, not a guarantee for this task. Appendix E of the revised paper documents the correction. Use revised paper and pinned code together, not unversioned plots from v1.0.0. [[S113](SOURCES.md#s113)](https://github.com/dbolya/tide/blob/49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1/CHANGELOG.md), [[S110](SOURCES.md#s110)](https://arxiv.org/abs/2008.08115v2).


## F195 — DOC/PUB; characteristic analysis is useful but correlational.
<a id="f195"></a>

**[F195](#f195) — DOC/PUB; characteristic analysis is useful but correlational.** Hoiem, Chodpathumwan and Dai analyze false positives and sensitivity to size, occlusion, truncation, viewpoint and visible parts on PASCAL VOC 2007. Their normalized precision addresses unequal positive counts across subsets; raw subset AP is not a pure measure of intrinsic difficulty. The project page records a 2014 summary-plot bug and a 2017 replaced annotation file. Their rankings for historical models/data do not predict our PPE bottleneck. [[S114](SOURCES.md#s114)](https://dhoiem.web.engr.illinois.edu/publications/eccv2012_detanalysis_derek.pdf), §2–3; [[S115](SOURCES.md#s115)](https://dhoiem.web.engr.illinois.edu/projects/detectionAnalysis/).


## F196 — DOC; sampling design is part of diagnosis.
<a id="f196"></a>

**[F196](#f196) — DOC; sampling design is part of diagnosis.** Census A3 calls for explicit population, sampling frame, strata/clusters, selection probabilities and information needed for weights. Its scope is Census statistical products, not a mandatory safety-video standard. It supports an analogous discipline for an error audit. Statistics Canada's methodological paper defines exhaustive disjoint strata and gives the stratified simple-random-sample total estimator Σ N_h ȳ_h. [[S116](SOURCES.md#s116)](https://www.census.gov/about/policies/quality/standards/standarda3.html), A3-2 to A3-5; [[S117](SOURCES.md#s117)](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019002/article/00006/02-eng.htm), §2, eq. 2.2.


## F197 — DOC/PUB; reproducible numbers do not guarantee stable findings.
<a id="f197"></a>

**[F197](#f197) — DOC/PUB; reproducible numbers do not guarantee stable findings.** Bouthillier, Laurent and Vincent distinguish reproducibility of methods from reproducibility of conclusions, and demonstrate sensitivity to experimental variation. A fixed seed helps replay one run; it does not establish robustness across training runs or camera samples. No universal number of seeds follows. [[S118](SOURCES.md#s118)](https://proceedings.mlr.press/v97/bouthillier19a.html), introduction and §2–3.


## F198 — INFERENCE.
<a id="f198"></a>

**[F198](#f198) — INFERENCE.** A large TIDE localization ΔAP can coexist with unchanged alert quality if all relevant person–PPE associations and zone anchors already tolerate those box errors. Conversely a small detector AP change can alter a high-cost event through an ID switch, a boundary crossing, or a confidence threshold. Six detection bins are not a taxonomy of safety-service root causes. Individual oracle gains are generally nonadditive; they are neither a unique causal decomposition nor a promise of attainable improvement.


## F199 — Proposed error record: separate outcome, stage, and evidence
<a id="f199"></a>

Everything below is PROPOSED for this project, not a TIDE feature or organizer rule. Keep stable IDs from source frame through the displayed alert. One incident may have several contributory causes. To avoid double-counting in summary tables, retain all tags and separately nominate a primary cause only when evidence warrants it; allow `unresolved` and `multiple`. “Earliest observed divergence” localizes evidence; it does not prove the deepest cause.

Recommended fields: `case_id`, camera/video/hash, clip interval and pre/post-context, source timestamps/frame IDs, evaluation unit and GT revision, person/track/event IDs, annotation visibility/unknown flags, A/B prediction and config hashes, output error, suspected stage(s), primary cause status, evidence links/log keys, oracle intervention/result, full-chain regression result, reviewer/adjudicator, stratum/inclusion probability, whether selected for diagnosis or estimation, and engineering action. Preserve pre-NMS/post-NMS and generated/queued/delivered/displayed alert IDs when available.

| Observable failure | Candidate stage, counterexample | Evidence or intervention that changes the next step |
|---|---|---|
| Missing person or PPE box | Detector class/localization/recall; alternatively wrong resize, class map, cap/NMS, or missing frame | Identical decoded frame hash; raw output, transformed coordinates, pre/post-NMS; GT-person substitution. Fix ingestion/mapping before collecting model-training data if boxes were already present upstream. |
| Person marked protected by neighbor's helmet | Ownership/association; helmet-in-hand may also violate the state contract | Annotated person/PPE ownership and visibility; freeze object predictions and substitute only ownership edges. A correct helmet box is insufficient evidence of correct wearing. |
| Wrong person receives event | Track association or state transfer; alternatively annotation track ID error | Identity traces before/after occlusion; GT-ID intervention with detections fixed. Track ID is not worker identity. |
| Spurious zone entry | Anchor/polygon/calibration/camera movement; alternatively GT boundary convention mismatch | Versioned polygon and coordinate transform, exact edge/vertex fixtures, frame with visible feet or unknown anchor. Fix geometry before retraining a detector when coordinates already agree. |
| Missed, fragmented or repeated episode | Temporal confirmation/cooldown/rearm; alternatively intermittent observability or ID change | Per-frame state series, event state transitions, selected event matching; oracle state sequence and time replay. Include episodes shorter than confirmation window. |
| Late alert | Confirmation delay, skipped frames, queue, runtime, transport, UI | Synchronized boundary timestamps with clock error, queue/drop logs, generated and delivered IDs. A screenshot cannot distinguish these causes. |
| Correct native output becomes incorrect on target | Input layout/color/scale, export/quantization/compiler, postprocess | Same input tensor, stagewise outputs, matched detections/events, device execution evidence. Test one transformation boundary at a time; import success is not parity. |
| Generated alert absent, duplicated or stale in interface | Queue/retry/deduplication/transport/rendering/filter | Durable event and delivery IDs, acknowledgement/display timestamps, replay of an identical event payload. Retraining cannot fix this layer. |
| Prediction disagrees with label | Annotation, ambiguous policy, incomplete labels or unobservable task; may still be a real model error | Independent review of original full-context clip, adjudication against frozen rules, provenance. Never relabel merely to agree with the model. |
| Fewer alarms after optimization | Better classifier, more aggressive policy, or lower analysis coverage | Reconcile evaluated camera-time, drops/timeouts, missing frames and state abstention. Fewer alarms with fewer processed intervals is not established quality improvement. |

Keep **symptom** (FP/FN/wrong person/duplicate/late/stale) distinct from **context** (small head, dark, crowd, new camera) and **mechanism** (wrong class map, identity switch, timer reset). Context is a useful slice; “darkness caused this error” needs a controlled intervention or more qualified language. A brightened/reencoded image alters the input distribution and can change several visual cues; its improvement is an illustrative sensitivity test, not isolated proof that lighting is the sole cause.


## F200 — Oracle component tests: what each comparison establishes
<a id="f200"></a>

Common contract: same held-out clips, same GT revision and coverage; replace exactly one declared interface while replaying the same downstream logic. Mark oracle inputs as unavailable at deployment and keep natural-run results primary. Record all evaluable GT people/episodes, including those the baseline missed. Avoid running only on people already detected by A; that silently changes the denominator.

| Intervention | Hold fixed | Useful interpretation and failure of inference |
|---|---|---|
| GT person boxes/IDs into state pipeline | PPE predictions, state classifier, downstream rule/config | Measures downstream behavior conditional on perfect person input. Gains suggest upstream dependence. Cannot predict gains from a practical detector; GT crops and IDs may be distribution-shifted. Report original unmatched persons and mapping decisions. |
| GT PPE boxes, then GT ownership, as separate tests | Predicted persons and all other interfaces | Separates missing PPE evidence from assigning existing evidence. Does not make hidden protection observable; unmatched/unknown cases remain explicit. |
| GT person-state timeline | Temporal and delivery stack | Tests episode construction, deduplication and timing conditional on perfect state. Does not test recognition. Retain genuine unknown intervals with the declared unknown policy. |
| GT track IDs with predicted boxes | State/zone logic and temporal policy | Can expose ID-switch driven re-alerts or state transfer. Cannot establish perfect tracker gains under different occlusion predictions. |
| Fixed synthetic state or point timeline | Geometry or temporal implementation | Tests exact software contract, including boundary equality and timer transitions. Establishes conformance on fixtures, not physical hazard validity or field accuracy. |
| Captured native detections into target downstream stack | Same detection payload and timestamps | If outputs still differ, defect lies downstream of this interface or in replay state. Does not prove target neural inference parity. |
| Captured generated events replayed into delivery/UI | Same payload, rate schedule, failures | Localizes lost/duplicate/stale delivery. A successful replay at low load does not establish loaded service reliability. |

For two interacting components, evaluate baseline, X only, Y only and X+Y when feasible. Define interaction `M_XY - M_X - M_Y + M_0` on a declared metric and direction. This is a descriptive interaction on tested data, not a universal decomposition. A zero single-oracle gain does not clear a component: another bottleneck can mask its effect; an intervention can also break interface assumptions. Record failures and unexpected negative effects, not only “upper bound” wins. GT replacements are not guaranteed upper bounds when the unchanged downstream system expects noisy predictions.


## F201 — PROPOSED, next engineering choice.
<a id="f201"></a>

**[F201](#f201) — PROPOSED, next engineering choice.** Hypothesis example: correcting person–PPE ownership reduces wrong-person violations. Inputs: fully annotated same-camera clips with person boxes/IDs, PPE ownership, visibility and event GT; captured detections; versioned baseline; candidate ownership change. Independent unit is a camera or predeclared independent recording group for generalization; episodes nested inside a camera are not independent camera replications.

1. Freeze split, GT version, frame selection, evaluator/matching, source decode, runtime condition, operating point and coverage definition before comparison. Keep only ownership logic changed. Record weights, preprocessing/NMS, zone/policy, FPS, compiler and software versions even when unchanged.
2. Run A and B on identical inputs. Record all outputs, including unknown, missing, errors and empty predictions. State reset/warmup rules matter for sequence tests. Offline deterministic replay is useful for algorithm diagnosis; separately test live execution where scheduling/drop behavior can change.
3. At a frozen operating point, compute object diagnostics, person-state errors over all eligible GT people, and full-chain alert results. If tuning is necessary, give A and B equal development-data search budget, lock each selected configuration, then compare those complete systems on untouched test data. Label it a system comparison rather than the isolated effect of ownership.
4. Inspect paired disagreements: improved cases, regressions, unchanged successes/failures, abstention transitions, per-camera effects. Re-run annotations only under an adjudication procedure blind to method identity where feasible. Any GT revision applies to both A and B and is versioned; report how it changed the result.
5. Report Δmetric with uncertainty using matched camera/block resampling when groups support it; preserve A/B pairing. Very few groups imply weak inference regardless of frame count. Do not pretend a per-frame interval accounts for between-camera variability. If training changed, repeat matched training conditions/seeds when feasible; distinguish one fixed-weight intervention from a training recipe claim.
6. Stop when the declared comparison is complete; unexpected hypotheses go to development or a later reserved evaluation. Repeatedly selecting on the same test converts it into development evidence.

Metrics and edge contract for this proposed comparison:

- Person error rate: erroneous decidable person-state opportunities / all GT person-state opportunities declared decidable by the annotation contract. Report correct, wrong, abstained, missing-person counts separately; a predicted missing person must not disappear. If undecidable GT are excluded, show their count/time and the reason. Avoid frame weighting if the intended unit is a person episode.
- Event precision: one-to-one matched valid delivered alerts / all evaluated delivered alerts. Event recall: matched GT episodes / all eligible GT episodes. Matching must declare class/person/camera, allowed temporal relation/deadline, tie-breaking, duplicate treatment and censored episodes; these are supplied by the event protocol, not invented here. Empty alert set gives undefined precision with count 0; empty positive set gives undefined recall, not perfect recall. Unknown intervals must be reported, not called negatives.
- False delivered alerts per evaluated camera-hour: false delivered alert count / fully adjudicated, observed exposure hours. Keep total intended camera-hours, unknown/unreviewed intervals and analysis coverage beside it. For continuous normal-only exposure, recall is unmeasured.
- Latency: delivery time minus declared observable onset, with clock/synchronization uncertainty. Report missed/deadline-failed episodes alongside conditional latency of delivered true alerts. Otherwise suppressing slow successes can improve the median deceptively.
- TIDE ΔAP: percentage points on the explicitly named AP scale/IoU/config, with GT and ranked prediction list. It is not a false-alarm rate, percent of engineering defects, or additive share of the AP gap.

A practical training ablation also fixes train/validation/test manifests, training examples, augmentation, optimizer budget and model selection rule. If adding data is the intervention, state whether training steps or epochs are held fixed; either choice changes exposure differently. Report the total recipe effect when several factors changed. An attractive before/after clip establishes only that those outputs differ on that clip.


## F202 — PROPOSED.
<a id="f202"></a>

**[F202](#f202) — PROPOSED.** Maintain two collections: a regression/diagnostic set selected for engineering insight, and a probability sample for estimating frequency. Include successes, false positives, missed episodes, unknowns, and delivery failures. An alert-only sample can estimate precision/alert error composition if sampled correctly; it cannot find events that produced no alert. Audit randomly selected continuous intervals or all independent GT episodes to discover misses. Sample from the union of A/B alerts and a source-time frame when comparing systems, so candidates unique to either system remain eligible.

Define population and unit first. A delivered-alert population estimates alert workload/error composition; an episode population estimates episode outcomes; a camera-time population estimates time coverage. These are different denominators. A rare class can be oversampled for diagnosis without pretending it is common in deployment. Use disjoint exhaustive design strata (for example camera group × alert outcome class × score band); keep overlapping explanatory tags such as darkness/crowd separately. Unknown true strata cannot be used as if known for unsampled records; a two-phase design needs both inclusion probabilities.

Within stratum h of N_h known units, draw n_h at random, save RNG seed and membership list, and record π_i = n_h/N_h. Estimate a binary error total as Σ_h N_h k_h/n_h and proportion by dividing by known population N. For unequal-probability designs use Σ y_i/π_i with the corresponding design; do not apply simple-stratum weights blindly. If estimating among errors, the frame must enumerate errors or use an appropriate two-phase audit; it is not enough to guess N_h from a reviewed convenience subset. If π_i is unknown, publish selected examples as qualitative, with no population percentage.


## F203 — LOCAL mathematical illustration, not model performance.
<a id="f203"></a>

**[F203](#f203) — LOCAL mathematical illustration, not model performance.** [illustrations.py](_WORK/W1_14_SOURCES/illustrations.py) was executed, output [illustrations.json](_WORK/W1_14_SOURCES/illustrations.json). Suppose population strata have 900 and 100 alerts. Review 10 from each and find respectively 1 and 8 association errors. Naive selected-sample fraction is 9/20 = 45%; design-weighted estimate is `(900×1/10 + 100×8/10)/1000 = 17%`. This illustrates weighting only; it gives no reliable precision claim about an actual model and is not a sample-size recommendation. Precision of the estimate needs the sampling design and stratum variability; related alerts may be clustered by episode/camera.

Store one review row per sampled unit; repeated screenshots of the same episode are not new independent errors. Ensure enough context to judge transitions, hidden people and delivery timing. Record no-judgment cases and adjudication outcomes. Don't replace an inconvenient sampled clip silently. Regression clips may deliberately stress tiny heads, overlap, boundary jitter and outages; their success rate measures that selected suite only.


## F204 — LOCAL arithmetic, hypothetical episodes.
<a id="f204"></a>

**[F204](#f204) — LOCAL arithmetic, hypothetical episodes.** The same illustration script uses 30 paired episodes: both succeed 16, A only 2, B only 7, both fail 5. A succeeds 18/30 = 60%; B 23/30 ≈ 76.7%; paired difference is +5/30 ≈ +16.7 percentage points. The useful engineering record contains seven improvements **and two regressions**. No independence or significance is implied; 30 episodes from one camera do not establish new-camera performance. The illustrative four-configuration scores 0.50, 0.60, 0.55, 0.80 yield interaction +0.15, demonstrating why isolated gains cannot simply be summed. These numbers are invented mathematical inputs, not observed safety analytics.

Counterexamples that must remain visible:

- A changes only score threshold; apparent precision gain comes with missed episodes. It does not establish improved representation or training.
- A now skips crowded frames; false alerts drop, camera-time coverage and recall fall. Lower counts alone misdiagnose improvement.
- B is evaluated on a brighter/newly trimmed clip; the model change is confounded with input composition. Re-run both on the same manifest.
- GT helmet boxes improve alerts because ownership also changed inadvertently. This is a joint intervention, not isolated detector attribution.
- Relabeling all baseline “false” alerts after seeing B can manufacture an advantage; adjudicate method-independently, apply revision to both, preserve original results.
- One screenshot contains an apparently correct alert, but a preceding ID switch caused a duplicate and the alert arrived after the episode ended. Need full sequence plus logs.
- Localization ΔAP shrinks after a box adjustment while per-person state worsens because a neighboring helmet is assigned incorrectly. Keep person/event outcomes primary for that claim.
- Export changes a score near threshold; the final alert changes after temporal accumulation even when average tensor differences are small. Diagnose threshold decisions and full chain, not only tensor mean error.


## F205 — PROPOSED evaluator/diagnosis fixtures.
<a id="f205"></a>

**[F205](#f205) — PROPOSED evaluator/diagnosis fixtures.** Before interpreting charts, use synthetic, expected-answer fixtures for: duplicate at exact IoU thresholds; same box/wrong class; same-class low IoU; wrong class plus low IoU; no predictions with one GT; predictions with zero GT; all-empty run; ignored detection that could repair another GT; max-detection truncation; equal-score ties. Pin bbox coordinate convention, category IDs and all evaluator options. Stop when each observed output agrees with the documented intended contract, or isolate a version discrepancy. This validates those evaluator behaviors only, not real-world model quality. TIDE itself was not executed in this research.


## F206 — PROPOSED full-chain regression cases.
<a id="f206"></a>

**[F206](#f206) — PROPOSED full-chain regression cases.** Use GT-linked short clips covering neighbor PPE, helmet in hand, hidden head, crowded crossing, occlusion/ID change, zone edge/hidden feet, short episode versus confirmation window, repeated entry/cooldown, clip starts inside an event, lost frame/transport retry and stale UI. Expected outputs come from the frozen task contract, not from today's model. Preserve timestamp/log traces. Stop when the declared set passes or each failure has an unresolved issue. Success supports conformance on these illustrative cases, not prevalence, field reliability or injury reduction.

Controlled replay supports “this code change altered these outputs on these fixed inputs.” A single-component ablation supports a conditional effect under that configuration, subject to interface validity. Independent replicated evaluation supports broader predictive generalization within its sampled population. None automatically establishes a unique physical cause of an industrial hazard, causal injury reduction, or performance on unobserved cameras. Oracle analysis is especially vulnerable to replacing an interface with information impossible to observe in deployment.


# W1_15 — сохранённые подробные наблюдения

Происхождение: [W1_15](_WORK/W1_15.md); [snapshots и локальные fixtures](_WORK/W1_15_SOURCES/). Контекст доступа и выполнения:  Research access: 2026-10-23, approximately 06:27–06:31 Europe/Moscow (+03:00). Evidence is public documentation read, not code executed or hardware measured. No SDK installation, compilation, device listing, inference, or model benchmark was performed. All harness requirements below are proposed team protocol, not organizer acceptance rules.


**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.


## F207 — Official scope and timing (documentation, S119).
<a id="f207"></a>

**[F207](#f207) — Official scope and timing (documentation, [S119](SOURCES.md#s119)).** The official landing page dates participation 23–25 October 2026 and advertises 45 hours. Its schedule lists case publication in participant accounts at 13:00 on 23 October, solution upload deadline 10:00 on 25 October, and defenses 12:00–17:30. The 45-hour interval is consistent with publication-to-upload arithmetic, not 45 hours after opening ceremony. The LinQ brief requires model inference on LinQ accelerators and promises participant online access. It describes live camera analysis and immediate notifications, with industrial-safety examples. This public brief does not supply a dataset, evaluator, numerical detection threshold, latency acceptance target, or online endpoint. Do not promote examples into an exhaustive scored taxonomy. Exact local-account updates and full case remain unknown.


## F208 — Assessment evidence (documentation, S120).
<a id="f208"></a>

**[F208](#f208) — Assessment evidence (documentation, [S120](SOURCES.md#s120)).** Regulation §1.4 gives a ten-minute defense allocation: two preparation, five presentation, three questions. §§6.1–6.4 use integer scores 0–3 across prototype functionality, primary problem, development/deployment value, novelty, UX/UI, secondary problems, and analysis. These are jury criteria, not a published AP/FPS formula. §3.6 requires at least one checkpoint with the full team for defense admission, and accessible submission links including code, teaser, demo and presentation; presentation ≤10 MB and accessibility at least 90 working days after results. §1.2 permits demo as video or prototype link. Relevant preparation caveat: §4.1.2 disallows pre-prepared prototype code/material, §4.1.6 mentions public free resources, and §7.3 contains an assistance prohibition. This research is planning evidence, not a determination of how organizers apply those clauses. The team must reconcile allowed preparation/submission practice with organizer instructions. No exhaustive regulation review was undertaken.


## F209 — Public executable-path instructions exist (documentation, S124).
<a id="f209"></a>

**[F209](#f209) — Public executable-path instructions exist (documentation, [S124](SOURCES.md#s124)).** The 2025 IVA H1 operator manual, RU.РМДВ.04.06.014-03 34 01, specifies Ubuntu 20.04, ≥32 GB RAM and Python 3.11 (§2.1, printed p5); installation needs a supplied wheel (§2.2, pp5–6). It illustrates ONNX→TensorFlow→quantization→compilation, `.tpu` serialization, then `tpu.Device.list_devices()`, `Device.open`, device `load`, `inference()`, and blocking `inference.sync(...)` (pp19–21). The sample is ResNet-50 classification, not industrial detection. Printed p17 reports `tlm_result.execution_time_us` as TLM estimated execution time; p24's approximately 5627 µs is example output, not this team's measurement. §3.2, p10 warns STAGING can produce invalid programs or compile too long. Tested-network list pp21–22 ends with yolo5s, whereas current tech page lists yolo8/yolo11. Manual Python 3.11 conflicts with software-page Python 3.8 API description. These version scopes require verification. Code was read, not run.

The exact manual link is https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf . Page numbering above is printed numbering; corresponding zero-based PDF pages are one less. The document contents calls the instructions §3.3, while the body labels the worked example §3.4 (p11); use page and function locators. Do not infer installed SDK/runtime versions or compatibility from the public example.


## F210 — Hardware marketing is not event latency (documentation S121/S122/S126; inference).
<a id="f210"></a>

**[F210](#f210) — Hardware marketing is not event latency (documentation [S121](SOURCES.md#s121)/[S122](SOURCES.md#s122)/[S126](SOURCES.md#s126); inference).** `/tech` advertises LinQ H int8 peak throughput and supported families. `/sol` advertises approximately 2.3 ms ResNet-50 latency at small batch, possible optimization to 1.5 ms, PyTorch through ONNX, and Python API/CLI quantization/compilation. The HPS datasheet explicitly says batch=1, names performance tools and developer SDK/support. These do not specify a reproducible full measurement protocol for our model. TOPS, a classifier example, and a named profiler cannot establish live video age, alert delivery, hardware placement, or new model compatibility.


## F211 — Access failure is scoped (observed retrieval).
<a id="f211"></a>

**[F211](#f211) — Access failure is scoped (observed retrieval).** Web open successfully retrieved all four requested pages plus `/docs`, operator manual and HP hardware manual. PowerShell Invoke-WebRequest failed TLS/transport for every attempted download; curl.exe independently failed schannel handshake on the framework PDF. `_WORK/W1_15_SOURCES/retrieval.json` preserves PowerShell failures. This is a local transport failure, not absent public documentation or absent vendor capability. `/docs` has linked documentation, but an installable wheel or hackathon remote endpoint was not obtained. No supplied credentials/device environment were present. Public API documentation is verified; an installed compatible API and executable device access are unverified. This explicitly refines any earlier blanket claim that LinQ execution APIs are undocumented/unavailable.


## F212 — Minimal harness contract (F212, proposal)
<a id="f212"></a>

Use one evaluator on immutable prediction artifacts for native/exported/target runs; permit runtime adapters to differ while freezing input and evaluation semantics. Keep runtime failures in the manifest rather than converting them to empty successful predictions. Begin with an auditable small contract, then extend it when actual case/data arrive.

| Artifact | Required content and why |
|---|---|
| `manifest.jsonl` | Clip/frame identifiers; original-byte SHA-256, decoding version, camera/group, split, source/license, image dimensions, frame index, original PTS and timebase, segment start/end, frame-selection rule, expected count, annotation coverage. Re-encoding needs a new identity and link to source. |
| `annotations.jsonl` | Schema/taxonomy revision; person and object geometry; visibility/unknown/ignore; ownership where observable; zone definition and coordinate system; event onset/offset and censored flags; reviewed intervals and adjudication provenance. A missing annotation row must not silently mean safe background. |
| `config.json` | Model/export/compiled-artifact hashes; preprocessing, color/layout/dtype/shape; class mapping; association/NMS/score thresholds; zone anchor/boundary; temporal confirmation/cooldown; batching/concurrency; timeouts and drop policy. Also evaluator source revision and matching policy. |
| `predictions.jsonl` | Raw-output artifact reference when available; detections in declared coordinates; person state/unknown; track IDs; event candidates and delivered alert IDs; score meanings; per-input success/error/drop status. Link outputs to request and input tensor hash. |
| `timestamps.jsonl` | Request/frame ID, clock domain and unit; capture/PTS, ingest, preprocess boundaries, submission, completion, postprocess, event confirmation and delivery acknowledgement. State whether capture is real UTC or file-media time. |
| `run.json` | Run ID; source commit plus dirty patch hash; environment lock/runtime/compiler/driver/firmware/device identity when available; command actually run; seed/determinism settings; start/end and timezone; cold/warm phase; configuration and artifact hashes; stderr/exit status; known limitations. Secrets excluded. |
| `report.json` + rendered table | Metrics with counts, units, evaluator revision and per-stratum denominators; failures and coverage; links to errors and source artifacts. Preserve the machine-readable result even when demo overlays are edited. |

Hashes identify exact bytes; they do not prove annotation correctness, hardware placement or reproducibility by themselves. Canonicalize configuration before hashing, hash every dependency of the result, and retain the original evaluated bytes. A checksum of a rendered video alone cannot identify its model or establish alert accuracy.


## F213 — Layers and verification order (F213, proposal)
<a id="f213"></a>

1. **Schema smoke:** validator checks unique IDs, coordinate bounds, finite scores, time order/domain, valid class mapping, complete prediction status, hashes and split membership. A schema pass establishes wiring only.
2. **Evaluator fixtures:** tiny hand-authored expected matches for duplicate detections, wrong class, ignored/unknown person, no positives/no predictions, one alert split into two, two events merged, event already active at clip start, and exact zone boundary. Test numerator/denominator and tie-break behavior, not only final rounded scores.
3. **Diagnostic model regression:** fixed small clips with observable expectations and deliberately hard counterexamples: helmet held in hand, neighboring worker's helmet, hidden head/feet, smoking-like hand motion without observable cigarette, repeated zone entry, track ID switch, sudden camera motion, empty scene, corrupt frame, backend timeout and delayed stale response. No fabricated data is called organizer evaluation. A failure fixture may be a synthetic request failure; label it accordingly.
4. **Parity regression:** identical saved tensors through native/exported/compiled target when available. Compare raw outputs, postprocessed detections/person states and final events separately; localize divergence. Record quantization calibration set and prevent test use for calibration/tuning. A classifier smoke result cannot replace detector/event regression.
5. **Demo:** show a labeled recorded replay or live source, request IDs, frame age, event/alert timeline, measured backend identity status and a failure/recovery example. Mark recorded target output as recorded. Display the same saved report/artifact IDs; never imply cached overlays are current target inference.
6. **Independent evaluation:** freeze model/config/GT and run on previously untouched grouped footage once; report exposure and uncertainty. If no independent split exists, call results diagnostic/dev results. Rerunning demo clips is regression evidence, not generalization evidence.

A useful 45-hour allocation is milestone-based rather than a guessed hourly promise: first executable smoke and schema; then one complete observable violation path with regression; then verified target run/parity; finally freeze, evaluate, package and rehearse. Preserve a submission buffer selected by the team. Do not spend all available time comparing architectures while target execution remains untested.


## F214 — Metrics card and accounting (F214, proposal)
<a id="f214"></a>

For every metric supply GT unit, prediction unit, eligibility, matching, threshold, numerator/denominator, aggregation, ignore/unknown policy and empty case. At minimum:

- Object AP only with a pinned evaluator and coordinate/class mapping; do not call it violation precision.
- Person-state recall = correctly identified eligible violation persons / all eligible GT violation persons under full-chain matching. Report missed person detection and unknown coverage separately; an oracle-GT-person experiment is conditional.
- Event precision = matched delivered alerts / eligible delivered alerts; event recall = matched GT events / eligible GT events, under frozen one-to-one temporal/person/class matching. Count unmatched duplicate alerts as false alerts unless contract explicitly declares otherwise. Zero denominator → NA with counts, not perfect score.
- False alerts per evaluated camera-hour = unmatched delivered alerts / fully reviewed eligible camera-hours; list unknown/unreviewed time and do not treat it as negative evidence. Coverage = eligible camera-time successfully analyzed / eligible expected camera-time, with exact treatment of frame sampling and short gaps.
- Host request duration = host completion minus host submission using one monotonic clock; report milliseconds, N, p50/p95 and failures, with warm/cold and batch/concurrency. This includes host/runtime effects inside the boundary, not guaranteed pure device execution. Host remote round-trip is similarly not isolated device time.
- Alert delay requires event observable onset and delivery acknowledgement in compatible clocks; file PTS measures media delay only after an explicit playback mapping. Cross-clock subtraction requires synchronization error bound. Report timeout/missing completion separately; do not erase them from a favorable latency distribution.
- Reconcile expected inputs = successes + failures + drops + unfinished at observation end. For retries use stable logical input ID plus attempt ID to prevent double counting. Report independent sessions/cameras separately before pooled aggregation.

Thresholds/tolerances and service targets require case-owner decisions; none are invented here. Evaluation artifacts may allow another researcher to reproduce arithmetic even if the vendor hardware remains unavailable, but must not label that as rerunning device inference.


## F215 — What is sufficient evidence of LinQ execution? (F215, proposal/inference)
<a id="f215"></a>

Maintain an explicit ladder: (a) public API documented; (b) compatible package actually installed/imported; (c) assigned target identified/listed; (d) exact compiled artifact loaded; (e) exact input requests completed with outputs; (f) useful detections/events after parity checks; (g) measured sustained workload with quality/coverage. Current research establishes only (a).

For (c)–(e), preserve organizer-provided endpoint/session identity and version information, target device enumeration or vendor-supported job metadata, compile report, model/tensor hashes, request IDs, full run logs and outputs. If a remote API hides devices, ask for its supported attestation/placement report later; no fictional endpoint or command is supplied here. Backend name in the UI alone is insufficient. Declare CPU/host preprocessing, decoding and postprocessing, and any fallback; “all operations on LinQ” needs operation-placement evidence rather than a successful import or `.tpu` file.

Device-only time requires a vendor-supported timer with a verified boundary and clock. TLM estimates must be stored as estimates in microseconds, never substituted for target measurements. If only client timestamps are exposed, report end-to-end request duration and state isolated device duration unknown. Public manuals and generic supported-network names do not establish custom YOLO operator/export compatibility.

For a five-minute presentation (own proposal informed by [S120](SOURCES.md#s120)), prioritize a single traceable violation-to-alert example, one negative/unknown and one recovery example, the frozen metric card and target execution evidence, then limitations. Keep the recording fallback clearly labeled and retain downloadable artifacts. A polished clip demonstrates the displayed path; representative performance requires the independent evaluated corpus and counts.


# W2_01 — сохранённые подробные наблюдения

Происхождение: [W2_01](_WORK/W2_01.md); [snapshots и локальные fixtures](_WORK/W2_01_SOURCES/). Контекст доступа и выполнения:  Дата исследования: 2026-10-23, около 06:51–06:56 Europe/Moscow (03:51–03:56 UTC). Роль: вторая волна, исследование первичных документов. Прочитаны исходные договоры, K001, W1_10/11/12/15 и handoff. DOC означает опубликованную документацию; OBS — фактически выполненное чтение/получение источника; INFERENCE — наш ограниченный вывод; PROPOSAL — будущий договор измерения; UNKNOWN — отсутствующий вход. Никакие SDK, модели или устройства здесь не запускались.


## F216 — DOC + INFERENCE.
<a id="f216"></a>

**[F216](#f216) — DOC + INFERENCE.** Публичный путь завершённого локального inference существует: перечисление устройств → открытие выбранного устройства → загрузка `.tpu` → создание inference session → `inference.sync(...)` → полученный словарь выходов. Руководство прямо называет последний вызов блокирующим. Это уточняет [F147](#f147): неизвестен не сам факт публично описанного completion primitive, а его соответствие будущему пакету/устройству/удалённому сервису. Документ не даёт оснований называть TLM estimate измеренным аппаратным временем. [[S124](SOURCES.md#s124), printed pp20–21 / PDF indices19–20]

Возможная будущая формулировка после реального выполнения: «Для указанного пакета и выбранного устройства получен результат блокирующего `sync` на сохранённых входах; длительность завершённого вызова измерена хостом». Она требует журналов фактического прогона и не равна утверждениям о чистом времени TPU, о выполнении всей видеоцепочки на TPU или о конкретной производительности. Сейчас подтверждено только наличие описанного пути.


## F217 — Матрица documented / actual / needed
<a id="f217"></a>

Все locators [S124](SOURCES.md#s124): printed page, затем zero-based PDF index; numbered lines доступны в сохранённом тексте.

| Предмет | Что прочитано / scope DOC | Применимость к реальному запуску, оставшийся вход |
|---|---|---|
| Installation/version | pp5–6 [4–5], L59–97: Ubuntu20.04, ≥32GB, Python3.11; поставляемый `tpu_framework-py3-none-any.whl`; import/exit-code smoke | Wheel действительно не получен и не установлен. Его metadata/dependencies и согласованные SDK/driver/firmware нужны прежде исполнения. Import не доказывает device execution. |
| Conversion | p7 [6] L100–108; p11 [10] L215–222: ONNX→TF, converter возвращает graph и mapping | Версия ONNX/opset/operator coverage и exporter конкретного детектора не установлены. Нужен фактический converter/package и его рабочий пример. |
| Calibration and input | pp12–16 [11–15] L243–390; p25 [24] L605–607: calibration images проходят preprocess; NHWC sample; `rescale` у quantized TF route | Пример crop/224×224/RGB/mean subtraction относится к ResNet50. Не переносить на YOLO или PPE без спецификации входа. Точные input dtype/layout/scale/names для реального runtime — контракт модели/SDK. |
| Compilation target / memory placement | pp9–10 [8–9] L159–213, p19 [18] L474–479: `compile_`, `get_hw_params`, `TPU_128x128_PARAMS`, DEFAULT/STAGING; `slicing_scheme` описывает распределение тензоров в памяти IVA H1 | Это target compile configuration и memory placement, не доказанный trace реально исполненных операций. STAGING имеет документированное предупреждение о неверной программе/долгой компиляции. Сохранить реально выбранные parameters и compile report. |
| Serialization / boundary | p20 [19] L482–496: TLM program / `.tpu`, `TpuProgram.from_executable(*tlm_program)` и `.to_file(...)`; отдельно Framework и SDK | Файл идентифицирует скомпилированную программу только при сохранённом происхождении/hash. Один `.tpu` не доказывает её загрузку или исполнение. |
| Device assignment | p20 [19] L497–505: `tpu.Device.list_devices()`, assert nonempty, `tpu.Device.open(available_tpu_devices[0])`, `tpu_device.load(...)`, `.inference()` | Описан локальный host, первый доступный TPU. Сохранять enumeration и выбранный устойчивый device identity; индекс0 не доказывает конкретную модель/serial. Публичный пример не описывает hackathon RPC. |
| Completion/output | p21 [20] L512–523: `inference.sync(input_dict_with_op_names)` — blocking; возвращённый mapping используется как output для общей проверки | Подтверждены blocking call и используемый output. Формальные timeout/cancel/exception semantics, async API, thread safety/concurrent sessions и buffering lifetime в этом прочитанном руководстве не определены. Их отсутствие в документе не означает отсутствия в SDK. |
| Output transformation / parity | pp17–18 [16–17] L395–446: OP/tensor suffix mapping, TLM output_data; p21 [20] тот же checker для TPU | Checker проверяет один ожидаемый top class; это не tensor tolerance, detection AP, person-state/event quality или полноценная parity. Нужны raw outputs/schema и собственные staged comparisons W1_10. |
| TLM timing | p17 [16] L414–420 и p24 [23] L581: `model_execute`, `tlm_result.execution_time_us`; label estimate | Единица microseconds. Число примера относится к TLM; никаких target timing samples в нашей работе нет. Нужен vendor device timer/profiler с определёнными границами либо честный host duration. |
| Debug visibility | pp23–24 [22–23] L547–590: logging configurable; debug output может отсутствовать; Original/Quantized/TLM/TPU class output | Нет обязательного подписанного provenance/placement trace. Наличие или отсутствие обычного debug log само по себе не аттестует устройство. Нужны связанные run/device/model/request/output records. |


## F218 — DOC, ограничение calibration.
<a id="f218"></a>

**[F218](#f218) — DOC, ограничение calibration.** Демонстрационные 2 изображения (pp14–15) выбраны для простоты; glossary p25 рекомендует 100 образцов. Это разные уровни инструкции. Ни два, ни сто не доказывают достаточность для целевого PPE distribution. Повторяется исходный W1_10 запрет использовать final evaluation set для calibration; actual representative calibration manifest остаётся входом.


## F219 — DOC, unresolved version discrepancies.
<a id="f219"></a>

**[F219](#f219) — DOC, unresolved version discrepancies.** Python3.11 в §2.1/p5 конфликтует с Python3.8 на [S122](SOURCES.md#s122) («Программное обеспечение»), причём встроенный log p23 [S124](SOURCES.md#s124) также содержит путь `venv/lib/python3.8/`. [S124](SOURCES.md#s124) p7 дополнительно печатает `as_graph(...platform='64x64_fpga')`, а описание параметра ниже называет default `128x128_asic`. Нельзя выбрать один default/интерпретатор из этих фрагментов. Пример задаёт target parameters явно; будущий запуск должен закрепить actual package signature/config и не полагаться на спорный default.


## F220 — DOC + INFERENCE, family scope.
<a id="f220"></a>

**[F220](#f220) — DOC + INFERENCE, family scope.** [S124](SOURCES.md#s124) pp21–22 даёт список протестированных сетей с `yolo5s`; [S121](SOURCES.md#s121) дополнительно перечисляет `yolo8`, `yolo11`. Различаются и источник, и формулировка: tested list конкретного manual против текущей supported-family страницы без version. Это не доказанное логическое опровержение ни одного списка и не гарантия конкретных weights, opset, shape, NMS или export. Разрешение — versioned compatibility report + actual compile/run/parity для точного графа.


## F221 — OBS + limitation.
<a id="f221"></a>

**[F221](#f221) — OBS + limitation.** Пример руководства является последовательностью пояснений и фрагментов, а не полученным исполняемым исходным проектом. В доступном тексте `tlm_program` используется для сериализации без видимого присваивания результата compiler call; import описан как `pytpu`, затем используется `tpu`. В p16 отсутствует comma после `batch_size=1`, в p17 extraction обрывает comprehension после `.item`. Часть может быть редакционной/извлекательной ошибкой. Нельзя молча «исправить» всё и выдать получившийся скрипт за проверенный vendor example. Нужен полный version-matched example package. Target input/output scaling для device route не следует дописывать по аналогии с отдельным TF quantized route.


## F222 — PROPOSAL, повторно использует W1_11/12.
<a id="f222"></a>

**[F222](#f222) — PROPOSAL, повторно использует W1_11/12.** Названия столбцов ниже — измерительные поля команды, не придуманный LinQ API.

| Величина | Единица / population / empty case | Что требуется и что остаётся за границей |
|---|---|---|
| TLM execution estimate | µs / отдельно для exact compiled model+input+simulation config; это не sample hardware distribution | Сохранить estimate как estimate. Перевод µs→ms арифметичен, но не превращает его в measured device latency. |
| Host completed sync duration | ms = same-host monotonic return−entry; N завершённых вызовов, raw samples; N=0→NA | Соответствующий API должен реально совпасть с [S124](SOURCES.md#s124). Внутренние copy/queue/runtime costs внутри call включены; pre-call work исключено. Ошибки/timeouts/unresolved имеют отдельные counts, не нулевые latency. |
| Remote completed request duration | ms = client output-ready−client submit; успешные unique logical requests, N и outcome ledger | Может включать transport/remote queue/host work. Job accepted не равно done. Remote SDK semantics пока неизвестны; public local sync не переносится на RPC. |
| Device execution interval | µs или ms по documented device timer, exact begin/end и measured workload | UNKNOWN. В [S124](SOURCES.md#s124) не найдено callable hardware timer/profiler API или границ аппаратного счётчика. Называемое в W1_15-S08 Performance Tools не заменяет такую инструкцию. |
| Advertised classifier latency | ms / vendor classifier claim | [S122](SOURCES.md#s122) имеет ≈2.3ms, optimization possibility1.5ms для ResNet50; это не наша модель, нагрузка, measurement protocol или event latency. |
| Event→delivered alert | ms или s / независимые GT episodes, matching и compatible clocks W1_11 | Требует video/evidence/temporal policy/delivery endpoint; вообще не измеряется простым `sync`. Misses/censoring сохраняются. |

Публичный manual различает compile target и реальную загрузку на выбранное локальное устройство. Это первичное основание для будущего **model-core** placement claim при actual matching SDK/device logs. Он не перечисляет per-op fallback/partition inspection, disable-fallback mode, signed device attestation или device profiler contract в inspected pp4–25. Не утверждаем отсутствие этих возможностей у производителя. Host pre/postprocessing прямо присутствует в примере, поэтому blanket claim «всё на LinQ» не следует даже из успешного sample.


## F223 — OBS, source retrieval/check only.
<a id="f223"></a>

**[F223](#f223) — OBS, source retrieval/check only.** Выполнены web opens/clicks, чтение полного numbered extracted manual, объединение двух перекрывающихся extracts и проверка всех L0–L650; сохранены JSON/text и SHA256 собственных snapshot bytes. Python requests HTTPS retrieval завершился SSL EOF; `LOCAL_RETRIEVAL.json` содержит точное время и exception. Локальные операции касались получения/чтения документов. PDF skill прочитан для аккуратной работы с page locators; создание/редактирование PDF не выполнялось.

Поиск по точным `tpu_framework inference.sync`, `tpu_framework model_execute` и LinQ profiler не дал использованного первичного source repository; шумная выдача сохранена в `web_1.json` исключительно как retrieval trail, snippets не являются фактическим основанием. На публичных /docs, /tech, /sol не получен installable package или полный example source. Это ограниченная поисковая проверка, не заявление, что публичного кода не существует.

**Не выполнено:** SDK install/import; graph export/quantization/compilation; TLM execution; list/open/load device; sync inference; model quality/parity/latency measurement; remote access; target benchmark. Цифры в документах — авторский sample/claim, ни одна не переименована в наш результат.


# W2_02 — сохранённые подробные наблюдения

Происхождение: [W2_02](_WORK/W2_02.md); [snapshots и локальные fixtures](_WORK/W2_02_SOURCES/). Контекст доступа и выполнения:  Research date: 2026-10-23, Europe/Moscow UTC+03:00. New native acquisition 03:52–03:55 UTC; exact times and hashes in `W2_02_SOURCES/retrieval.json` and `actev_provenance.json`. Assignment: K002/K003. This result reuses W1_05/06/11/12/15 and their saved sources. No system, model, LinQ, camera or throughput benchmark was performed. All cohort rules below are **our proposed supplemental evaluation protocol**, not organizer rules or a claim about an industry standard.


## F224 — INFERENCE, reconciliation of W1.
<a id="f224"></a>

**[F224](#f224) / INFERENCE, reconciliation of W1.** A complete delivery census plus adjudication of every delivery, with adequate source/person/event context, can support **semantic false delivered records per fixed logged source camera-hour**. It does not require annotation of every non-alert frame. Its denominator describes the supplied source population; it does not certify that those hours were normal, analyzed, observable for every person, or free of missed events. Use a fixed denominator and retain unknown alert truth, unavailable source context and unresolved delivery outcomes. The stricter “fully reviewed hours” formulation in [F171](#f171) and [F214](#f214) should be restricted to metrics that actually require continuous reference truth. [F080](#f080).2 is the appropriate sufficiency statement for the delivery-census estimand.


## F225 — PROPOSAL.
<a id="f225"></a>

**[F225](#f225) / PROPOSAL.** Publish two separate cohort systems: (a) records attributable to immutable source input/evidence ownership, divided by that fixed source exposure; (b) actual visible interruptions occurring in a receiver wall-time interval, divided by that wall interval. Draining changes what has been observed, never the original source owner. A finite snapshot is named **delivered by accounting close C**; it is not eventual burden unless delivery/retry closure is actually established. A shorter drain must yield a different named snapshot and its outstanding ledger, not a silently improved final result.


## F226 — CODE, S127.
<a id="f226"></a>

**[F226](#f226) / CODE, [S127](SOURCES.md#s127).** In pinned NIST ActEV Scorer, `actev_sdl_v2.py:124–131` selects `fa_meas_v2`. `metrics.py:353–391` integrates `sys_temp - ref_temp_add`, divides by accumulated non-reference area, and returns `None` if that denominator is zero. `sparse_signal.py:77–78` clips subtraction to nonnegative differences; `area`, lines 96–109, integrates piecewise values. `metrics.py:621–634` constructs additive reference activity counts and their complement. Thus this particular TFA counts excess instance-time, including multiplicity, rather than delivered messages. This is code inspection plus the small extracted-function check below, not execution of its complete scorer or proof of every ActEV edition's behavior.


## F227 — DOC, S128.
<a id="f227"></a>

**[F227](#f227) / DOC, [S128](SOURCES.md#s128).** Apache Beam's programming guide §8.4 distinguishes event timestamps from processing clocks and warns that arrival order can differ. Watermarks estimate input completeness; configured lateness can discard later data. §§9.1–9.2 distinguish event-time and processing-time triggers. This supports retaining both axes and explicit close policy. It is an accounting analogy: a video PTS or watermark cannot establish physical capture time, complete delivery follow-up, or correctness of an application delivery log. We do not propose installing Beam.


## F228 — DOC, S129.
<a id="f228"></a>

**[F228](#f228) / DOC, [S129](SOURCES.md#s129).** The recovered 2019 ActEV SDL plan §2.2 (printed p5, PDF page 5) describes forensic full-corpus processing. Its selected-frame file index is defined in §4.1 (pp7–8). Therefore a continuous-video benchmark's temporal output and exposure do not by themselves establish live UI delivery. This older plan is deliberately not presented as the unavailable 2021 plan.

**New evidence vs reuse.** [F075](#f075) already supplies TRECVid's spurious-observations/camera-hours precedent and its retrospective limitation. [F077](#f077)'s FDA reference-standard discussion supplies the partial-verification warning, with medical scope. W1-11's saved LoadGen completed-request paths and [S085](SOURCES.md#s085)/[S093](SOURCES.md#s093)/[S094](SOURCES.md#s094)/[S098](SOURCES.md#s098) supply original-release/completion, per-ID accounting and separate coverage/freshness/correctness rationale. No new broad survey of those topics was needed. The primary public evidence does not decree our source-anchor rule, industrial deadline, duplicate policy or review protocol; those are explicit proposals below.


## F229 — Metric-specific reference sufficiency (F229)
<a id="f229"></a>

Let I be fixed non-overlapping eligible source intervals, identified by camera and source epoch; H_I = total union length / 3600 camera-hours. Exclusions are frozen before outputs. Let V_I(C) be distinct operator-visible delivery records with immutable source owner in I and delivery observed by C. A delivery record is not a transport attempt. A complete destination log must include updates and creation identity so that retries can be reconciled. H_I can be known from an immutable file manifest even when non-alert frames have no event annotations. For live scheduled but unrecorded intervals, use **scheduled camera-hours**, not “known supplied source-hours”; if origins or exposure cannot be established, source-attributed rates are unavailable.

| Estimand / unit | Numerator and denominator | Minimum sufficient review/evidence | Unknown and empty cases; excluded claim |
|---|---|---|---|
| Semantic false delivery burden by C; records/camera-hour | F_I(C) / H_I; F means the asserted person/type/zone/state is false under frozen truth rule | Complete delivery census; source-owner linkage; every record adjudicated with enough context to resolve that assertion. All non-alert intervals need not be annotated | U remains separate; with fixed classifications/ownership, descriptive interval [F/H_I,(F+U)/H_I]. This bounds truth classification among delivered-by-C records only. H_I=0 → NA. No recall or verified-normal-hours claim |
| Delivered excess/duplicate burden by C; records/camera-hour | E_I(C) / H_I | All records, including neighboring-cohort deliveries that can already have notified the same episode; sufficient identity, safe-reset, continuation and reminder context; explicit intentional reminder policy | Unknown episode identity/rearm → unresolved excess status. No automatic unknown→new episode. Product-intended reminders remain total interruptions and have separate utility labels |
| Strict timely unmatched delivered burden by C; records/camera-hour | (N_known_eligible_deliveries − N_timely_matched)/H_I, with unknown-eligible/matching records separate | All delivery records; complete relevant GT episode set around every delivery plus all competing records; frozen compatible keys, deadline/end rule, clock mapping, assignment and boundaries | This can be established without exhaustive no-alert GT only if the *entire matching neighborhood* is complete. Unknown GT that can alter matching requires feasible-world sensitivity or unresolved counts, not a simple F+U shortcut. Correct-but-late is unmatched here, not semantic false |
| Delivery precision / unitless | Semantic correctness: T/(T+F), U reported; or timely one-to-one precision: M/N under named matching contract | Same local review as corresponding numerator; all alerts or a named probability design | Complete-case precision must say “among adjudicated records”; if U>0 also report full-population bounds where valid. No records → NA, never 100%. Semantic truth can include true duplicate assertions, so it differs from useful precision |
| All operator interruptions; records/wall-hour | N_visible(J) / (length(J)/3600) | Complete defined receiving-boundary log in fixed receiver interval J; no GT needed | Include carry-in, late, duplicate, unknown, technical-health/reminder categories separately. Destination log missing → incomplete census. No source clock required. length(J)=0 → NA |
| Source-attributed all deliveries; records/camera-hour | N_visible,I(C) / H_I | Complete census, source ownership and close/follow-up records; no semantic GT needed | Does not prove correctness, recall, normal time or deployment workload at another replay speed |
| Event recall / unitless | Timely matched eligible GT episodes / all eligible GT episodes in fixed onset-owned GT cohort | Independent exhaustive episode discovery over cohort and needed margins, or separately designed probability-sampled reference review/estimation (W2_03); complete relevant delivered log and deadline follow-up | Alert-only review cannot reveal never-alerted episodes. Outage with known GT remains operational miss; unknown GT/delivery follow-up remains unresolved. No eligible episodes → NA. Entire censored stratum handled consistently (W1_05/W2_04) |
| False-active union duration; seconds or fraction | Measure of predicted-active AND reference-inactive support; optionally divide by fixed evaluable source duration or verified non-reference duration, each explicitly named | Complete predicted temporal states and reference state on required support; classification can be limited to predicted-active regions for numerator, but verified normal denominator requires independent complete reference on denominator | Point-delivery logs do not reconstruct duration. Unknown states give unknown duration/bounds. Zero verified non-reference time → NA. ActEV additive excess-time TFA is a separately named metric, not this union metric |
| Verified normal exposure; camera-hours | H_normal = length of eligible reference-negative support /3600 | Independent sufficiently complete reference truth throughout claimed negative support, with class/person observability rule | No-alert time is not verified normal. A single person's hidden PPE does not automatically invalidate camera-time for all other classes/claims |
| Conditional analyzed or fresh source rate | Corresponding numerator with owner in fixed mask A or F, divided by H_A or H_F | Saved completion/freshness masks with prespecified temporal support mapping; plus the relevant truth evidence above | Label conditional; expose discarded H and all-outage strata. Do not divide all-window alerts by only analyzed hours. H_A=0 → NA. Never substitute for requested-footage operational recall |

The numerator and denominator must share the same source ownership filter. A missing analysis mask does not block a fixed-manifest delivery burden rate; it blocks a claim about analyzed-hour rate. Conversely, an available mask does not create GT. Class-specific unknown truth attaches to records/intervals for that question, rather than erasing an entire hour from every metric.

**Full matching context caveat.** If a delivered record can match GT outside I, obtain the relevant adjoining context and competing alerts, then apply the same global matching convention before restricting results. A source-anchor alert cohort and an onset-owned GT cohort can contain different sides of boundary-crossing matched pairs. Their M counts need not be equal. Do not combine such precision and recall into one F1 using an assumed common TP. Either evaluate a shared closed matching universe or report the separately named cohort metrics with boundary-pair counts. This is a further limitation of “all-alert review is enough”: it must support the actual matching endpoint, not merely a screenshot per message.


## F230 — Reproducible attribution and close contract (F230, own proposal version 1)
<a id="f230"></a>

1. **Freeze source population.** Retain `run_id, config_hash, camera_id, source_epoch, source_file_hash or emission/session identity, timebase, I_start, I_end, eligibility_reason`. Use half-open [a,b). Union intervals per camera/epoch, then sum lengths. Planned policy sampling does not shorten source hours. Keep requested/scheduled, supplied, analyzed A, fresh F, reference-reviewed R and property-observable O masks distinct. Never condition H_I on whether a delivered assertion was easy to adjudicate.

2. **Freeze evidence ownership.** Every logical violation alert has exactly one primary `(camera, epoch, source_input_id)` anchor: the latest source input actually consumed when that logical alert was first created. Save its original source time and complete evidence-support input IDs. This is an auditable software provenance definition, not a claim that the asserted onset equals the anchor. Assign owner interval by this immutable source anchor, even if support crosses intervals, prediction onset is backdated, batches mix sources or a retry later uses new context. A genuinely new re-evaluation/alert gets a new logical ID and anchor. Multi-camera group alerts require a separately frozen group population/anchor policy or remain unattributed; never count one record once per camera and call that a delivery count. Alternative legitimate rules—episode-onset-owned true-alert utility or original-release-wall cohorts—may be reported with their own names, but cannot silently replace this rule, especially for semantic false alerts with no GT onset.

3. **Retain original release.** For each selected logical analysis opportunity record scheduled release, actual first release, all attempt IDs, batch membership and all consumed source IDs. Retry release never resets original release or scheduled lag. A batch completion is not one source frame and not one alert. Preserve source alert creation, confirmation, send, durable destination create/update, UI presentation if instrumented, and their clock domains. Our primary delivered boundary is a newly created usable durable destination record; a claim about on-screen interruptions requires actual presentation evidence and a correspondingly named unit.

4. **Count delivery identity at the boundary.** Same logical alert/attempt can produce zero, one or several distinct visible records. A retry updating the same durable record creates zero extra interruptions. A retry creating a fresh record creates an extra delivery, retaining original owner. Different logical alerts about one continued episode can also be excess; transport deduplication alone cannot resolve event duplication. Store `visible_record_id`, `logical_alert_id`, `delivery_attempt_id`, `created_at`, update/presentation IDs, source owner and event linkage. Unknown source owner is an explicit unattributed bucket; do not distribute it in proportion to exposure.

5. **Two-dimensional ledger.** For every distinct visible record save owner I (or other/unattributed) and actual receiver delivery time. Source view filters owner; wall view filters time. In any wall window J, `N_visible(J) = N_ownerI(J) + N_other_owner(J) + N_unattributed(J)`. With common close C and start context, `N_ownerI(by C) = N_ownerI(in main window) + N_ownerI(in drain) + N_ownerI(in any other observed window)`. Carry-in means owner before I but delivery in J; carry-out means owner I but delivery after the main J. These are accounting terms, not truth labels. Left/pre-existing GT onset status is independent of carry-in input ownership.

6. **Predeclare end E, close C, and observation termination.** Stop new cohort releases at their declared schedule boundary E; record other streams/epochs separately. Continue destination/result observation through C under a frozen drain rule, preserving queue state and cancellation/retry records. Report drain length, all in-flight work and delivery state at E and C. Snapshot membership uses delivery `<= C`; receiver workload bins remain half-open. An event exactly at an adjacent wall-bin boundary belongs to the next bin; a close snapshot includes what is observed at C. Close means report cutoff, not automatic backend cancellation or proof that nothing can arrive later.

7. **No hidden deletion after timeout/close.** Attempts retain exclusive terminal status at cutoff (`valid response`, explicit error, timeout/cancel, unresolved). A result seen after an attempt timed out is a linked late-response observation; it does not rewrite the historical attempt as an on-time success or create a second logical opportunity. Logical outcome may later become valid-late. Every actual late visible alert is counted in its owner cohort's later snapshot and actual wall interval. Publish a correction/delta after C; never overwrite a frozen snapshot without its version. If future delivery is not prevented/observed to closure, label eventual count unknown. One pending item does not give a finite upper bound on eventual visible duplicates when retries can create unbounded records.

8. **Separate pending, late and missed.** `No delivery observed by C` is not `never delivered`. Finite-close completeness needs reliable destination census through C; eventual completeness additionally needs bounded retry lifetime and verified queue/attempt terminality or other justified closure. Event recall requires delivery observation through each included deadline and adequate source/GT follow-up. C at the end of a source file alone is insufficient. Do not keep censored successes while excluding otherwise comparable censored no-alert episodes from the same recall endpoint.

9. **Clock mapping by route.** In true live input, map independently meaningful capture/observable-onset timestamps to receiver clock, with synchronization/placement uncertainty. Without it, source-to-delivery age is unknown; receiver-local residence remains measurable. In paced replay, save an immutable per-input scheduled due time from the actual playback schedule, including speed changes/pauses/discontinuities; report delivery-minus-due as **replay lag**. It is not physical capture age. At constant speed s, due(p)=m0+(p−p0)/s. Variable speed requires the actual piecewise schedule. For unpaced replay use source exposure and host completion timing, plus original-release-to-delivery where instrumented; no live timeliness claim follows. Do not subtract a media PTS from an unrelated host monotonic/UTC timestamp or convert a receiver delivery to source time without an actual mapping.


## F231 — LOCAL extracted-source fixture.
<a id="f231"></a>

**[F231](#f231) / LOCAL extracted-source fixture.** `W2_02_SOURCES/fixtures.py` loads only pinned `SparseSignal` and extracts only the AST function `fa_meas_v2`; it does not import/run the full ActEV scorer. Timeline 100 frames; one reference [20,40), system matching [20,40), extra overlapping system [25,35), and spurious system [50,60). Verified result: excess instance-time 20 frame-units / non-reference 80 frames = TFA .25. Union false-active time strictly outside reference is 10 frames; that separately defined fraction is .125 over 80. With zero non-reference denominator, source function returned `None`. Notifications could be zero/one/many for identical segment outputs; those counts are unspecified by this fixture. This confirms the unit distinction and an empty case, not benchmark performance.


## F232 — LOCAL own ledger fixture.
<a id="f232"></a>

**[F232](#f232) / LOCAL own ledger fixture.** Seconds; I=[0,100), H_I=100/3600=1/36 camera-hours. For this constructed example only, source origin maps to receiver monotonic origin with speed 1. Main wall J=[0,100); drain [100,112); snapshot C=112. D=5 s is an illustrative parameter, not an industrial requirement. Six logical IDs have delivered records by C; L6 is pending and has no visible record. Adequate identity/context is stipulated for all known outcomes; no unlisted GT matches are possible in this toy case.

| Record / logical ID | Immutable anchor; original release | Destination delivery | Known interpretation | Source I by C=112 / wall bin |
|---|---:|---:|---|---|
| v0 / L0 | −5; −5 | 10 | Semantic false, carry-in | Excluded / main |
| v1 / L1 | 10; 10 | 12 | True timely, onset 10 | Included / main |
| v2 / L2 | 95; 95 | 105 | Semantic false, delivery in drain | Included / drain |
| v3 / L3 | 98; 98 | 109 | True but late, onset 98; deadline 103 | Included / drain; strict unmatched |
| v4 / L4 | 70; 70 | 72 | True timely, onset 70 | Included / main |
| v4retry / L4 | 70; original 70 | 115 | Retry creates a distinct visible duplicate of v4 after close | Excluded from by-112 snapshot; included by-120, same owner I / later wall |
| v5 / L5 | 80; original 80 | 108 | Attempt timed out 85; valid result arrives 107, then semantic false delivery 108 | Included / drain; attempt remains timed-out with linked late result |
| none / L6 | 90; 90 | none by 120 | Delivery outcome unresolved | No visible numerator; pending at both closes |
| v7 / L7 | 60; 60 | 65 | Asserted PPE truth unobservable with available context | Included as unknown / main |
| v8 / L8 | 100; 100 | 110 | Semantic false; exact anchor at right boundary belongs to next source cohort | Excluded / drain |

Executed assertions and saved JSON establish:

- At C=112: source-owned visible records = 6 = timely 2 + late 1 + duplicate 0 + semantic false 2 + unknown 1. All receiver records through C = 8 = source-owned 6 + other-owned 2; no unattributed records in this fixture. Wall main has 4 records, drain 4. Wall main rate is 4/(100/3600)=144 interruptions/wall-hour; drain rate is 4/(12/3600)=1200. These tiny rates are arithmetic illustrations.
- Semantic false source burden by112 = 2/(1/36)=72 records/camera-hour; classification range allowing U=1 is [72,108]. Strict known unmatched = false2+late1=3, rate108, with U separate. Timely precision among known records is 2/5; full six-record precision range is [2/6,3/6] only under the stipulated independent unknown eligibility and no matching changes. Semantic-correct known assertions are 3/5; its six-record range is [3/6,4/6]. GT recall is unavailable without an independent roster of never-alerted events.
- At C=120: source-owned visible records =7, still only6 logical IDs with visible delivery; duplicate1 is newly observed. Semantic false remains2, unknown1; strict known unmatched becomes4, rate144. Total receiver records=9, partition main4+drain4+later1. Logical L6 remains pending. Future eventual count is not proven closed.
- An idempotent retry updating v4 would create no v4retry record and no extra interruption. A counter increment per transport attempt would overcount that case; deduplicating all L4 rows would undercount the actual distinct-record fixture.
- At a hypothetical earlier close C=100, source deliveries v2/v3/v5 have not been observed yet. This is a smaller by100 snapshot, with those paths not closed; it cannot replace by112 as a final run comparison. Late delivery v3 still fails D even if included in a longer drain. Dropping its row cannot make it timely.


## F233 — LOCAL playback fixture.
<a id="f233"></a>

**[F233](#f233) / LOCAL playback fixture.** Playback starts m0=1000 at PTS0; speed1 until PTS50, then speed2. PTS80 is due at1050+(80−50)/2=1065. Delivery1068 has replay lag3 s. Using the stale speed1 map gives due1080 and a false negative lag−12 s. Source exposure [0,100) stays100/3600 camera-hours while scheduled playback duration becomes75 wall seconds. The same source delivery count can therefore have different wall-hour workload. The fixture executed this arithmetic. Physical filming-to-delivery age remains unknown.


## F234 — Review/failure counterexamples with permissible claims (F234, own paper fixtures)
<a id="f234"></a>

| Evidence available | Supported statement | Unavailable statement / accounting |
|---|---|---|
| Immutable10 source camera-hours; complete closed delivery log100 records; all100 reviewed with sufficient context: F20, true80; non-alert periods unannotated | Semantic false delivered burden20/10=2 per source camera-hour; semantic correctness80/100=.8 for this corpus/configuration | Recall, GT event density, verified normal exposure and false-active duration unknown. No claim that silence establishes safe scenes |
| Same ten hours/100 records; known F20, known true75, U5 | Delivered-by-close false classification range[2,2.5]/hour; adjudicated semantic correctness75/95=.78947, explicitly conditional; all-record correctness range[.75,.80] | Dropping U from source exposure or declaring them negative is invalid. If U affects event identity/matching, useful precision needs joint matching sensitivity |
| Independently reviewed observable4 hours known to contain no target activity; complete log zero deliveries and completed analysis | Observed zero delivered false notifications/4 verified-normal camera-hours; event recall NA because zero GT; false-active duration only if temporal outputs are also available | Zero future false-alert rate or all-target miss performance not established. Statistical bound requires stated model/design, reused W1_06 rather than assumed |
| Same requested10 hours and independent complete GT10 episodes; analysis completes1 hour, containing1 timely detection; remaining9 known episodes during outage | Requested-footage timely recall1/10=.1; analyzed-only recall1/1=1, coverage1/10. Both are reported | A low delivered false burden does not establish improved recognition; failure cause is unavailable processing, not automatically semantic FN classification |
| Requested10 live scheduled hours; only first hour recorded/analyzed; other9 have no source/GT evidence; one known detected episode | Scheduled service coverage1/10 under declared cadence; actual logged destination interruptions and conditional recorded-hour quality | Full-window event recall and actual emitted-source exposure unknown. Report missing evidence. Scheduled-hour delivery load can be named, but not verified normal/supplied-source false exposure |
| All alerts reviewed, but destination log absent for an outage interval | Correctness of enumerated records only; missing log interval separately quantified | Complete delivered census, finite-close source total and operator workload not established. No finite upper count from observed records alone |

The independently verified-normal alternative and fixed-source all-alert alternative are both legitimate. They answer different questions. Probability-sampled review is another legitimate route only under its saved selection/inclusion design (W2_03); these paper examples make no sampled-estimator claim.


# W2_03 — сохранённые подробные наблюдения

Происхождение: [W2_03](_WORK/W2_03.md); [snapshots и локальные fixtures](_WORK/W2_03_SOURCES/). Контекст доступа и выполнения:  Research/access: 2026-10-23, approximately 06:45–07:02 Europe/Moscow (UTC+03:00); native retrieval timestamps are in [retrieval.json](_WORK/W2_03_SOURCES/retrieval.json). Assignment is methodology research for `evaluation`, with no organizer footage, GT, official evaluator, alert log, SDK or device supplied. No model, LinQ or camera benchmark was run. Original contracts, K004/handoff, W1_06, W1_13 and W1_14/E02 were read and reused. Dates of source publication below are separate from access dates.


## F235 — INFERENCE + original PROPOSAL.
<a id="f235"></a>

**[F235](#f235) / INFERENCE + original PROPOSAL.** A limited annotation budget can support a design-unbiased estimate of a **fixed recorded corpus's event or false-alert total**, provided all frame units have known positive selection probabilities and each selected unit's outcome is established under an exhaustive reference-review rule. Sample disjoint source-time cores, count episodes only in the core owning their onset, and treat surrounding video as context rather than extra selected units. No pre-existing episode roster is needed: the sampling frame enumerates windows, whose previously unknown episode counts are discovered during review.

Recall is a ratio of two unknown totals; its plug-in estimate is generally biased in finite samples. Sparse sampled positives, unresolved truth, or missing matching context can defeat a useful recall interval even when the sampling law is correct. The practical default is therefore **report estimated event and missed totals, sampled raw counts/unknowns and the weighted recall point estimate together; publish an interval only when its design and approximation are supported**. Zero sampled positives means undefined recall, not perfect detection. This completes the missing specification in [F080](#f080).4/[F202](#f202) rather than applying the alert estimator directly to an unenumerated episode population.

Evidence labels: DOC = opened primary authored method; LOCAL MATH = executed invented finite-population calculation; DERIVATION = mathematical consequence; PROPOSAL = this branch's original protocol, not an organizer or industrial standard; UNKNOWN = input not supplied. The protocol below is a conditional executable paper procedure, not a report that annotation has occurred.


## F236 — DOC, S131.
<a id="f236"></a>

**[F236](#f236) / DOC, [S131](SOURCES.md#s131).** Aronow and Samii define known positive first-order inclusion probabilities for unbiased HT totals and distinguish the pairwise probabilities needed for the usual unbiased variance estimator. Their §2.2 shows why zero joint inclusion probabilities make particular variance terms unobservable. Consequently a positive sampling probability alone does not supply a valid variance estimate. Their paper concerns finite survey designs, not video observability or event matching. [Primary §2](https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831/section2-eng.htm).


## F237 — DOC, S117; reused S117 with newly saved bytes.
<a id="f237"></a>

**[F237](#f237) / DOC, [S117](SOURCES.md#s117); reused [S117](SOURCES.md#s117) with newly saved bytes.** The stratification paper defines disjoint exhaustive strata, independently sampled SRS without replacement, total `sum_h N_h * mean_h(y)` and its finite-population variance. This supplies the selected simple design, without adopting the paper's optimization algorithm. [§2, eqs. 2.1–2.3](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019002/article/00006/02-eng.htm).


## F238 — DOC, S132.
<a id="f238"></a>

**[F238](#f238) / DOC, [S132](SOURCES.md#s132).** Knottnerus and Scholtus analyze small-sample ratio variance/MSE, including denominator fluctuations, residuals and bias expansions (§2, eqs. 2.1, 2.7–2.9). Their abstract warns that widely used variance formulas can severely underestimate at small sample sizes. Their corrections are not adopted as an automatic sparse-video solution: they contain approximations and additional quantities, and do not fix zero observed denominators. [Original article](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003-eng.htm), [§2](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003/02-eng.htm).

W1_13 remains applicable to extrapolation to new cameras, annotation uncertainty and selection. There is a useful distinction: **finite-corpus randomization inference does not require independent camera contents or iid events**. Window values can be correlated, adjacent, or contain the same physical cause; the fixed population and actual randomized draw define uncertainty. A camera/site sampling model is additionally needed for future-camera claims. A bootstrap over the sampled frames or an assumed iid episode binomial model is not a replacement for this window design.


## F239 — PROPOSAL — finite frame, selection law and saved artifacts
<a id="f239"></a>

1. Freeze the tested configuration, event definitions, GT reset/unknown rules, delivery outcome definition, matching version and source cohort before the audit. Lock the finite set of original recordings, hashes, camera/session lineage and nonduplicated source intervals `[a_c,b_c)`. Camera timestamps/PTS and real delivery-clock mapping must be known where needed (→ W2_02). Duplicate encodings are not additional source exposure. Multiple camera views can remain separate camera-view units, but the resulting estimand is camera-view episodes, not unique physical incidents.
2. Partition each source interval into disjoint, exhaustive half-open cores `[a+iL,min(a+(i+1)L,b))`; retain the shorter last core. Select `L` for review cost/context, with no universal value asserted. A source-time gap remains an explicit unavailable interval; do not concatenate it as continuous safe video. The full known exposure is `H=sum(core_duration_seconds)/3600` camera-hours. An unequal final duration is harmless for **episode totals** with window weights; time-normalized measures use actual H, not N×L. Record requested/analyzed coverage separately.
3. Frame row: `frame_version, core_id, camera_id, original_session_id, source_hash, t0, t1, duration_s, stratum_id, N_h, n_h, pi, exclusion_reason_if_predeclared, decodability/coverage_mask_ref, context_available_left/right`. Strata use attributes known for **every** core before reference annotation: camera/session, light metadata, or an indicator that the frozen complete log contains an alert anchored to that core. A stratum based on the unknown true event/error cannot be constructed from just reviewed cores.
4. Minimal design: one stratum, uniform SRSWOR of `n` of `N` cores. Optional design: mutually exclusive/exhaustive strata with independent SRSWOR `n_h` of `N_h`. Every nonempty noncertainty stratum gets `n_h>0`; non-alert cores must remain selectable. Use `n_h>=2` when possible for sample variance, or explicitly give up that variance estimate. Sampling all cores in a small stratum is allowed. Do not allocate all budget to alert cores and claim missed-event recall.
5. Exact draw procedure: sort all stable core IDs within each stratum, initialize a named/versioned pseudorandom generator with a saved prespecified seed, uniformly permute that list, retain its first `n_h` IDs. Save generator/library version, seed, original sorted list, full permutation, selected IDs, allocation and code/hash. This is pseudocode specification; no corpus draw was performed here. Under the intended law each size-n_h subset has probability `1 / choose(N_h,n_h)`. Save draw artifacts, not just seed, so a library change cannot erase reproducibility.
6. Inclusion: `pi_i=n_h/N_h`; for distinct cores in the same stratum `pi_ij=n_h(n_h-1)/(N_h(N_h-1))`; across independently drawn strata `pi_ij=pi_i*pi_j`; `pi_ii=pi_i`. Certainty-unit pi is 1. Retain these or enough design metadata to reconstruct them. Do not substitute per-draw probabilities from a different with-replacement design. This protocol samples without replacement; repeated viewing does not create a second observation. If redesigning with replacement, unit inclusion and multiplicity estimators require a separate contract.
7. Freeze a budget including context/adjudication reserve. Complete every selected unit; do not replace difficult windows, stop when enough errors appear, or silently add convenient positives. Additional random audit phases require their own predeclared law/inclusion accounting; a new fixed independent audit can be reported separately. Context discoveries and diagnostic cases are saved but not pooled into the initial probability estimate.

An alert-presence stratum may deliberately oversample alert-bearing cores. That is a **probability sample conditional on known frozen predictions**, not an independent-reference failure: every core still has positive known pi and reference reviewers find truth without using predictions. The review pass itself must be independent of alerts as described next.


## F240 — PROPOSAL — review, onset ownership and edges
<a id="f240"></a>

For each selected core, first review original continuous video with predictions/notifications hidden, enumerate **all** GT persons and qualifying observable state/entry transitions in the core, including short/no-alert events, and preserve unknown intervals. A reviewer must cover the whole core, not inspect only a set of candidate frames. Record annotation frame granularity, playback/inspection procedure and whether a second independent reviewer/adjudicator checked the core. A review procedure's missed annotations are measurement error; random selection does not cure them. Adjudicate against a fixed manual, not to improve a system score. Reveal complete logs only after this reference pass to establish outcomes.

Define episode identity by `(camera, reference-person, class, zone/rule, observed-reset sequence)` under the fixed annotation manual. Unknown occlusion is not automatically a safe reset. Define one **observable onset** `s_e`, with a saved operational rule such as the first sufficient observable evidence after the required observed safe reset. An onset exactly at core boundary belongs to the core beginning there. For an eligible onset in `[a_c,b_c)`, `owner(e)` is its unique containing core. Count it once only if that core was selected. Person first appearing already in a violation is an entry/prevalent-state stratum unless the frozen task explicitly defines entry as the event; do not silently equate first visibility with true onset.

Start review with predeclared left/right margins `M_left`, `M_right`; choose their values from reset and outcome requirements, not from a statistical article. Then extend original context as needed until the prior safe reset/onset ownership and relevant outcome are resolved. Margins are **not** a guarantee that arbitrary-duration episodes fit. Save actual context extents, reason for extension, boundary flags, reference IDs linking repeated context, and cost. Reading extra context changes information, not selection probability or counting ownership.

| Boundary case | Required counting/review action |
|---|---|
| Long episode starts in selected core and lasts through several others | Count once in owner. Follow enough context for identity/reset/outcome. For fixed-deadline recall a known end beyond the deadline is sufficient; exact final duration need not be known. Do not weight by number of windows touched. |
| Episode started in another core, overlaps selected core | Context-only record, zero onset-owned contribution here. Its owner has its own pi. If its owner is also selected, link the same stable episode and count once there. |
| Episode demonstrably started before source cohort begins | Exclude from incident-onset denominator by definition; report carry-in/prevalent-state inventory separately. Do not call it a missed new onset. This is a narrower incidence claim, not recall for all active hazards. |
| State already active at recording start; onset not known | Mark left-censored. If proof establishes onset before cohort, carry-in; if possible onset straddles cohort start/core edge, retain ownership ambiguity. Do not force onset to first frame. |
| Onset interval `[l,u]` spans core edge | Resolve with original context/adjudication if possible; otherwise selected-core totals are unresolved. Save feasible ownership alternatives under a shared episode ID; do not give it full weight in both cores, or pick the midpoint. |
| Known onset before source end, episode continues beyond it | It contributes to incidence count if onset/eligibility are known. It cannot receive a certain fixed-deadline failure if observation/log follow-up ends too soon. Count/right-censor outcome separately. |
| Very short episode ends before deadline | Keep denominator under the chosen event definition; exact end and eligibility follow fixed matcher. Do not exclude because the service was slow. |
| Gap, reconnect or unobservable person state | Preserve unknown. Do not invent safe reset, join/split or classify non-alert time as negative. A core with incomplete event enumeration is not a zero-event core. |

For a headline fixed-deadline endpoint, the simplest safe cohort uses cores in an **advance-defined onset range with complete reference video and log follow-up available through the maximum required horizon**, plus left context. For example, onset cohort ending b, with original video/logs available to b+D after appropriate clock mapping. This changes the target interval explicitly; it does not discard failures after seeing outputs. If such follow-up is unavailable, retain all sampled cohort events, show complete/censored outcome counts and refuse the unconditional recall point estimate or give justified sensitivity bounds. Censored successes and failures cannot be selectively retained/dropped. A success before censoring is recorded as observed success, but its inclusion does not license excluding comparable censored failures from a headline denominator.


## F241 — Matching locality is a precondition, not a margin assumption
<a id="f241"></a>

For each owned event, establish its outcome using the frozen class/person/zone/timing rules and **complete** relevant delivery logs, including delivery drain (→ W2_02) and known duplicates. Fixed-deadline eligibility bounds can make the necessary temporal context finite. Do not rerun the service with state reset at every sampled core: audit the already-frozen full-corpus run and its actual outputs.

A global one-to-one matcher may assign an alert to a neighboring unselected GT event. Run it on a closed connected component of all compatible alerts/GT episodes affecting any sampled owned event, then retain only sampled owners' outcomes. Expand reference annotation beyond the core to enumerate competing events/edges until no external eligible edge remains; verify closure under the declared temporal bound, keys and reset semantics. Save the full component, matches and closure evidence. Extra owners remain context, not sampled observations. If closure needs the entire session, that is the actual cost. No fixed arbitrary margin proves it. If a component cannot be completed, mark affected outcomes unknown; do not claim the original global-match recall from a locally truncated graph.

Practical narrower fallback: predeclare an **episode notification coverage** endpoint, “at least one independently attributable valid delivered notification for this reference episode within the declared time window,” only where each accepted notification maps uniquely to one reference episode. Duplicates count separately in workload. This avoids competition only when unique attribution is established; it is not automatically the global one-to-one event-recall endpoint. If unique attribution is also unresolved, report onset counts and sampled outcome evidence, without a recall claim. → W2_04 owns the exact matcher and uncertain-boundary truth policy.


## F242 — PROPOSAL + DERIVATION — estimators and uncertainty
<a id="f242"></a>

For every core i in the finite frame let `E_i` be its number of eligible onset-owned episodes, `T_i` the number successful under the specified completed outcome contract, and `M_i=E_i-T_i` the missed/deadline-failed number. These are **fixed but initially unknown** corpus values. They become observed only when selected review/context is complete. For complete values:

`Ehat = sum_selected E_i/pi_i`, `That = sum_selected T_i/pi_i`, `Mhat = sum_selected M_i/pi_i`.

Units are episodes; `Ehat/H`, `Mhat/H` are episodes/camera-hour over the corresponding known finite source exposure, with H>0. Since `E[I_i/pi_i]=1`, each total is design-unbiased. No iid event assumption occurs in that proof. A point estimate can exceed an intuitive corpus count or vary widely when weights are large; that is sampling variation, not proof of an impossible event rate.

`Rhat=That/Ehat` estimates `R=T/E` when Ehat>0. It is a **combined ratio of totals**, not an average of stratum/camera recalls; it is not generally unbiased. If Ehat=0, recall is undefined and no detected-event delay distribution is supplied. If actual E=0, corpus recall itself is undefined. A nonempty alert set with no GT events remains useful false-alert evidence. H=0 makes rates undefined.

For any total variable y under the chosen stratified SRS design, an unbiased estimated variance is

`v(Yhat)=sum_h N_h^2*(1-n_h/N_h)*s_h(y)^2/n_h`,

where `s_h(y)^2=sum_selected_in_h(y_i-ybar_h)^2/(n_h-1)`. Certainty strata contribute zero sampling variance. A noncertainty stratum with n_h=1 has no sample variance estimate under this formula; setting it to zero is invalid. Pairwise probabilities/local correlation are already handled by this design formula. Do not resample individual episodes or frames within selected cores.

For a sufficiently supported ratio, first-order Taylor approximation uses `z_i=T_i-Rhat*E_i`:

`v_lin(Rhat)=sum_h N_h^2*(1-f_h)*s_h(z)^2/n_h / Ehat^2`.

This is this branch's direct first-order linearization of the ratio; it uses the **same sampled cores** for both totals and includes their covariance. It is an approximation, not an exact unbiased ratio variance or proof of 95% coverage. A normal/t-based interval requires justified large-sample behavior and degrees-of-freedom/design choices; no universal n, event count or CI is asserted here. [S132](SOURCES.md#s132) gives a specific reason not to rely blindly on small-sample ratio variance. Truncating an invalid interval to [0,1] does not repair its coverage. A resampling alternative must reproduce the actual stratified without-replacement design with its finite-population corrections; generic camera bootstrap or iid window bootstrap is not automatically that design.

**Few/sparse groups fallback:** report selected/all frame counts per stratum, raw E/T/M, weights and totals, per-core contributions, censoring/unknowns, and descriptive ratio if defined; label precision insufficient. Budget permitting, expand to a predeclared census of the finite corpus or conduct a separately specified larger random audit, rather than create a nominal interval. Do not claim future-camera reliability from one fixed camera even after a corpus census. If selected cores have all zero misses, the sample-variance formula can be zero while unseen cores contain many misses; a degenerate zero-width interval is unsupported.

There is a narrower exact zero result for SRSWOR: if K of N cores contain at least one missed episode, observing zero such cores in n selected cores has probability `choose(N-K,n)/choose(N,n)` (zero if n>N-K). Inverting this can bound the **number of miss-bearing windows** under complete review, not the number of missed episodes. Without a defensible maximum episode count per core, a missed-episode total has no useful finite upper bound from this zero observation alone. Do not invent a cap from a detector's maximum tracks. This is a finite-design combinatorial derivation, not the Poisson 2.995732/H calculation reused from W1.


## F243 — Unknown truth and nonresponse
<a id="f243"></a>

Save one outcome per selected core: `complete`, `partial-reference`, `unreadable`, `ownership-unresolved`, `matching-unresolved`, `followup-censored`, with reason and reviewed/context seconds. No replacement; no zero filling; keep pi unchanged. A selected window that cannot be reviewed is statistical nonresponse as well as an engineering failure. Weighting only responders by their original pi does not restore design-unbiased corpus totals. Response-probability weighting/imputation would add unverified assumptions; this protocol does not silently use either.

If every core's possible count is bounded by justified external information, propagate coherent lower/upper totals through the fixed weights; evaluate recall over jointly feasible assignments with `0<=T_i<=E_i`. A shared uncertain episode has one owner in every feasible truth, so independent per-core maxima may be incoherent. These are annotation/identification sensitivity ranges for the estimate, **not confidence intervals or bounds for all unseen corpus outcomes**. With no upper bound on events hidden by a selected unreadable segment, no finite episode upper sensitivity bound is justified. Report the missing selected units and withhold the complete-corpus point claim. Weighted known-event contributions alone are not an unbiased total of all events.


## F244 — independent alert audit versus source-window audit
<a id="f244"></a>

| Population/estimand | Selection and estimator | What remains unmeasured |
|---|---|---|
| Complete frozen delivery log: semantic false delivered total F | All-alert adjudication gives F exactly conditional on truth/log completeness. Or SRS/stratified probability sample from immutable notification IDs: `Fhat=sum f_j/pi_j`. Divide by matching **full logged source exposure H** for source-hour burden (W2_02 cohort/drain); do not divide by just sampled clip hours. With known alert total A, `1-Fhat/A` estimates semantic correctness, not necessarily one-to-one useful-alert precision. | Non-alert misses; unseen GT roster. Duplicate/timeliness distinctions require separate outcomes and context. Unknown f_j is unresolved. |
| One-to-one matched delivered-alert precision | `Phat=Vhat/A` with A known and probability-reviewed alert validity V_j fully adjudicated including competing notifications/GT; all-alert census is simplest. | Event recall remains unmeasured. Sampled alert validity cannot ignore global duplicate/matching competition. |
| Onset event total / missed total / event recall | Independent full-core reference review, [F239](#f239)–[F242](#f242), with no-alert cores selectable and outcomes complete. | Unobservable hazards, pre-existing states outside target, physical incidents across cameras, future sites. |
| Convenience samples near alerts, curated errors, adaptive interesting clips | Report selected cases and regression behavior only, unless a separately specified probability design is reconstructed. | No general frequency/recall/total extrapolation with unknown pi. |

An alternative estimates false alerts in sampled source cores by assigning **each delivered item** to one immutable source-evidence anchor and summing its false indicator in that core, then applying the core weights. It requires W2_02's complete cohort/log attribution and full adjudication context. It targets an alert total, with a different ownership unit from event onset. Do not assign false deliveries to nonexistent GT episode onsets. Source-anchor alert precision and onset-owned event recall can have different matched numerators at corpus boundaries; do not construct a common-TP F1 unless both endpoints use the same closed event/alert universe. Do not add an alert-frame estimate to a window-frame estimate of the same total: that double-counts without a designed dual-frame estimator. Independent all-alert review plus random core reference annotation are complementary, not automatically pooled samples.


## F245 — LOCAL MATH — actual exhaustive tiny checks
<a id="f245"></a>

[fixtures.py](_WORK/W2_03_SOURCES/fixtures.py) ran under Python 3.11.9; [fixtures.json](_WORK/W2_03_SOURCES/fixtures.json) preserves all six equally likely size-2 samples, exact fractions and assertions. No video, model, evaluator package or hardware was executed. An initial helper rejected a generator (`len` unavailable); it was corrected to materialize the six-item iterable, then all checks passed. This does not validate real annotation or matching.


## F246 — F05: boundary and duration example.
<a id="f246"></a>

**[F246](#f246): boundary and duration example.** Invented onset cohort [0,40), four cores [0,10), [10,20), [20,30), [30,40), each pi=1/2 when n=2. Source context extends before 0 and through 45. Known episode intervals below are invented exact truth; the last success is assumed observable in complete follow-up under a declared endpoint.

| Episode | Interval seconds | Owner / included onset? | Outcome | Cores positively overlapped |
|---|---:|---|---|---:|
| carry-in P | [-5,2) | outside cohort, carry-in only | outside incidence denominator | 1 |
| short A | [2,3) | core 0 | miss | 1 |
| long B | [8,29) | core 0 | success | 3 |
| boundary C | [10,12) | core 1 | miss | 1 |
| right-crossing D | [39,45) | core 3 | success, complete context required | 1 within core frame |

Owned E=[2,1,0,1], T=[1,0,0,1]; true totals E=4,T=2,M=2. Core 2 has **zero owned onsets despite containing long B**. Selected cores {0,2} give Ehat=4,That=2,Mhat=2, Rhat=.5, with context B counted only under owner 0. Across all six draws, Ehat is [6,4,6,2,4,2], mean 4; That mean 2. Exact design variance of Ehat and mean estimated variance both equal 8/3. This validates the arithmetic design on this fixture only.


## F247 — F06: any-overlap bias.
<a id="f247"></a>

**[F247](#f247): any-overlap bias.** An event overlapping m of N cores is observed at least once with probability `q_e=1-choose(N-m,n)/choose(N,n)` under this SRS design. Here m=1 gives q=.5, m=2 gives 5/6, and long B (m=3) gives q=1. Deduplicating any-overlap episodes and weighting all by 1/pi=2 gives long B an expected contribution 2 instead of 1, while a one-core event contributes 1. Counting every overlapping selected window also counts B repeatedly. Correct inverse-q weighting could work **only if the full overlap set/frame membership is ascertained**, with appropriate joint probabilities for variance; a fragment in a selected window cannot reveal its unknown total duration. This is why onset ownership is the practical default. Enlarged margins must not become unweighted extra event samples. Context-only discoveries have a more complicated union inclusion probability if promoted to a sample.


## F248 — F07: unbiased totals, biased ratio.
<a id="f248"></a>

**[F248](#f248): unbiased totals, biased ratio.** Different invented four-core corpus E=[1,1,1,7], T=[1,1,1,0], n=2. True recall=3/10=.3; estimated event and detected totals have means 10 and 3. Three samples contain two one-event cores, ratio 1; three contain the seven-event missed core, ratio 1/8. Mean sample ratio=9/16=.5625, **not .3**. This exact enumeration refutes a claim that a ratio of unbiased totals must be unbiased. No undefined ratios were needed for the counterexample. In another population E=[0,0,0,7], n=2 misses the only positive core with probability 1/2: no sampled positives cannot show that no corpus events exist.


## F249 — F08: oversampling alert windows.
<a id="f249"></a>

**[F249](#f249): oversampling alert windows.** For [F246](#f246) counts, suppose frozen alert-bearing stratum={cores 0,1}, census n=2 of N=2; non-alert stratum={2,3}, sample n=1 of N=2. Thus pi=[1,1,.5,.5]. If selected={0,1,3}, Ehat=2+1+2×1=5, That=1+0+2×1=3, Rhat=.6; naive selected ratio=2/4=.5. If selected no-alert core is instead 2, Ehat=3, That=1; means over both draws are true E=4,T=2. The noncertainty stratum has only one sampled unit, so this example deliberately lacks the usual sample variance estimate. Oversampling must retain its actual weights and uncertainty limitation. Alert-bearing labels in this illustration are arbitrary metadata; they do not assert every alert is successful or every non-alert core contains no success (delivery/source attribution and cross-window outcome windows can differ). For example, D's qualifying alert source evidence may fall after time 40 in follow-up, outside its onset-owned core.


## F250 — Provenance, scope, remaining acquisition and K disposition
<a id="f250"></a>

Native HTML snapshots are saved in this branch only. [collect.py](_WORK/W2_03_SOURCES/collect.py) records URLs, UTC access timestamps, final URL, status, byte length and SHA-256. Text extraction used BeautifulSoup; MathType annotation blocks were removed for the readable [S132](SOURCES.md#s132) extraction, while original HTML/MathML remains preserved. HTML status 200 was checked for the known unavailable-page text. No source implementation was needed or claimed; all executed mathematics is our own exhaustive tiny enumeration. Download hashes identify mutable document snapshots; no software commit applies to those HTML sources.

| ID | Primary identity/version/date | Locator, retrieval, supported scope |
|---|---|---|
| [S131](SOURCES.md#s131) | Peter M. Aronow, Cyrus Samii, *Conservative variance estimation for sampling designs with zero pairwise inclusion probabilities*, Survey Methodology 39(1), June 2013; exact release day not established; HTML modified 2017-09-20 | [Article](https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831-eng.htm), [§2.1–2.2](https://www150.statcan.gc.ca/n1/pub/12-001-x/2013001/article/11831/section2-eng.htm). Web and native HTTP 200; `[S131](SOURCES.md#s131)_ht_main.html`, `[S131](SOURCES.md#s131)_ht_section2.html`. First/second-order inclusion conditions and variance limitation only. |
| [S117](SOURCES.md#s117) | J.A. de Moura Brito, T.M. da Veiga, P.L. do Nascimento Silva, *An optimisation algorithm applied to the one-dimensional stratification problem*, 2019; W1 metadata release 2019-06-27, retrieved section modified 2019-07-04 | [§2](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019002/article/00006/02-eng.htm), eqs. 2.1–2.3; web/native 200, `[S117](SOURCES.md#s117)_stratified.html`. Reused [S117](SOURCES.md#s117); exact author/title/date provenance also in W1. Used survey formulas, not optimization results. |
| [S132](SOURCES.md#s132) | Paul Knottnerus, Sander Scholtus (Statistics Netherlands), *On a new estimator for the variance of the ratio estimator with small sample corrections*, Survey Methodology 45(3), release/modified 2019-12-17 | [Main](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003-eng.htm), [§2](https://www150.statcan.gc.ca/n1/pub/12-001-x/2019003/article/00003/02-eng.htm), eqs. 2.1, 2.7–2.9. Web route timed out, direct native 200; `[S132](SOURCES.md#s132)_small_ratio.html`, `[S132](SOURCES.md#s132)_small_ratio_section2.html`, readable text. Small-sample warning and bias/variance methodology; corrections not executed or imported. |

Additional leads retained transparently: Thomas Lumley's `svyratio` documentation timed out in web/native TLS and was not used as read evidence. De Haan/Hendriks ratio/SPAR §2 initially rendered an unavailable page via web but native retrieval subsequently succeeded (`failed_ratio_lead.html` is a historical filename); its ratio-bias paragraph was read. It is corroborative context, not needed for the protocol or fixture proof; do not describe the article as globally unavailable. [S132](SOURCES.md#s132) was obtained by its linked actual article route; the first guessed `00007` URL was a different genetic-algorithm article and was not used as ratio evidence.

**[Q002](OPEN_QUESTIONS.md#q002) / UNKNOWN → datasets + annotation owner.** Need actual immutable source manifest, timestamp/coverage gaps, original context availability, class/reset/visibility manual, and review budget including adjudication. Obtain originals and pilot reference review cost on separately identified development footage; freeze the frame/allocation before the estimation audit. Determines whether full-core enumeration is feasible; no public methodology proves human exhaustiveness.

**[Q014](OPEN_QUESTIONS.md#q014) / UNKNOWN → evaluation/operator_product/video_architecture.** Need frozen outcome deadline/short-event policy, unique source/delivery IDs, follow-up/drain, event-person keys and matching closure conditions. Obtain actual logs and policy; test boundary fixtures with W2_02/W2_04. Without them, onset incidence counts may be estimable while missed-event/recall outcomes remain unresolved.

**[Q015](OPEN_QUESTIONS.md#q015) / UNKNOWN → deployment owner.** The finite corpus does not establish future-camera/site population inclusion, expected operating mix or between-site variation. Acquire a defined deployment sampling frame and real probability sample (or explicitly restrict conclusions). No number of extra bootstrap draws closes this question.

**K004 disposition: closed for the methodological/public gap, scoped for application.** Closure evidence: [F239](#f239) exact window frame/draw/pi and artifacts; [F240](#f240) onset/context/left/right/unknown ownership plus matching-closure condition; [F242](#f242) estimands, variance limits and unknown/nonresponse policy; [F244](#f244) independent no-alert review versus alert audit; executed [F246](#f246)–[F249](#f249) fixtures demonstrate duration selection, boundary ownership, unequal weights, ratio bias and zero-positive insufficiency. No hidden duration bias or automatic unbiased-ratio claim remains. Actual annotation completeness, resolvable boundaries/log follow-up, numerical precision and population generalization remain [Q002](OPEN_QUESTIONS.md#q002)–[Q015](OPEN_QUESTIONS.md#q015); they are unavailable-input questions, not gaps that another generic public sampling article can close.


# W2_04 — сохранённые подробные наблюдения

Происхождение: [W2_04](_WORK/W2_04.md); [snapshots и локальные fixtures](_WORK/W2_04_SOURCES/). Контекст доступа и выполнения:  Research: 2026-10-23, Europe/Moscow UTC+03:00. New source acquisition 04:00:12–04:00:19 UTC (07:00 local); exact provenance in `W2_04_SOURCES/retrieval.json`. Assignment K005/K006. This branch inspected primary solver source and ran **small exact mathematical fixtures only**, with Python 3.11.9 and SciPy 1.17.1. No detector, application, camera, LinQ, or performance benchmark ran; NetworkX is not installed and was not installed or executed. All industrial matching/eligibility rules below are **our proposal**, named `lex-offline-v1`, rather than a benchmark or jury standard.


## F251 — CODE + LOCAL MATH.
<a id="f251"></a>

**[F251](#f251) / CODE + LOCAL MATH.** A reproducible proposed matcher is now available: exact lexicographic minimization of `(-number_of_pairs, summed_cost, sorted_pair_list)`. Invalid edges are absent; unmatched vertices are explicit skips; no epsilon, dummy penalty, or big-M is used. The reference implementation is exponential and suitable for tiny validation fixtures only. It gives an unambiguous executable specification for a future scalable implementation, not a claim about runtime capacity. `fixtures.py::assign` and `results.json` preserve all pairs and costs.


## F252 — LOCAL MATH.
<a id="f252"></a>

**[F252](#f252) / LOCAL MATH.** Sum delay is neither maximum delay nor p95. With onsets G1=0,G2=2 and deliveries A1=3,A2=4, all four edges compatible, both complete assignments have total delay5: `(G1,A1),(G2,A2)` has delays3,2; `(G1,A2),(G2,A1)` has4,1. Our ID rule selects the first. For fixed chosen GT and alert subsets, sum(d−s)=sum(d)−sum(s), independent of permutation. The second objective can select subsets when cardinality leaves alternatives, but often cannot distinguish pairings. We make no latency-tail optimization claim. Keys can eliminate this abstract ambiguity in an actual task.


## F253 — PROPOSAL.
<a id="f253"></a>

**[F253](#f253) / PROPOSAL.** Exact-boundary, known-identity, complete-follow-up components support a point score. Interval truth supports edge classification and declared sensitivity; unresolved joint truth remains unresolved. The maximum matching of the union of individually possible edges is an **outer upper bound**, not necessarily an attainable optimistic score. Entire incomplete-follow-up strata/components are retained outside the primary point score, including their observed successes. This closes the censor-success selection loophole in W1.


## F254 — INTEGRATION with F229/F230.
<a id="f254"></a>

**[F254](#f254) / INTEGRATION with [F229](#f229)/[F230](#f230).** Source-evidence-owned alert precision and onset-owned event recall can have different matched counts at interval boundaries. They do not automatically form an F1 with a common TP. Common-TP counts in this branch apply only to the same fully specified, closed bipartite universe. Real interval reporting must either retain those separately named cohort metrics plus boundary-pair counts, or explicitly define a shared closed universe. No denominator may be inferred by silently dropping carry-in/out or post-close deliveries.


## F255 — Evidence reused and new primary solver evidence
<a id="f255"></a>

Read/reused [F045](#f045)/[F046](#f046) (state-independent person correspondence), W1_05 entire contract and saved `sed_eval_event_matching.py`, `small_examples_results.json`, W1_09 person identity/lifecycle rules and narrow CLEAR examples; W1_01 onset/unknown schema, W1_04 observed entry gaps, W1_10 matching agreement contract. W1_05 source confirms that sed_eval maximum-cardinality matching lacks our delay/ID objectives; the W1 collar fixtures were not a run of this proposed matcher. COCO, ActivityNet, sed_eval, TrackEval results and semantics remain unchanged and separately named.


## F256 — CODE, S133/S134.
<a id="f256"></a>

**[F256](#f256) / CODE, [S133](SOURCES.md#s133)/[S134](SOURCES.md#s134).** SciPy's `maximum_bipartite_matching` treats an existing CSR entry as an edge even when its stored value is zero, returns−1 for unmatched vertices, and solves cardinality, not delay. Its source explicitly warns that tied output may vary across SciPy/Python versions. Its adjacent `min_weight_full_bipartite_matching` instead requires cardinality=min(partition sizes), or fails if no full matching exists; it is not a drop-in solution for arbitrary partial matching. Locators: source lines17–58,123–132; adjacent function266–329. In our fixture CSR matrices contain stored ones only for valid edges; costs are never encoded as sparse adjacency zeros.


## F257 — DOC, S135; not executed.
<a id="f257"></a>

**[F257](#f257) / DOC, [S135](SOURCES.md#s135); not executed.** NetworkX documents minimum-cost flow with node demands and capacities and warns about floating-point weights/demands. This offers a future scalable route with exact integer ticks, but does not implement our stable-ID priority automatically. We chose a direct exact reference rather than installing a dependency or asserting that a generic assignment call has the desired three priorities. The rolling page was labeled NetworkX3.7 at access; its version is not our runtime version.


## F258 — Proposed closed-universe input and person correspondence contract
<a id="f258"></a>

1. Freeze taxonomy, ROI, coordinate convention, box gate, zone version, episode separation/reset rule, common clock mapping, source cohort I, finite accounting close C and all stable IDs **before scoring**. Any trial numeric values below are fixture parameters only. No industrial deadline or IoU threshold was established. Reject duplicate immutable IDs, invalid timestamps, negative costs, malformed boxes and inconsistent keys rather than silently coerce them.
2. Stable GT IDs come from the independently frozen annotation roster; stable prediction IDs come from immutable source/frame/output lineage, not input-array position, sort stability, or changing model track labels. This implementation compares unique ASCII strings lexicographically. For production, specify canonical byte serialization of composite IDs. A tied ID-based result may change if IDs are renamed; it is invariant under row permutation with unchanged IDs. Do not permit an evaluator to rename IDs to favor a result.
3. At a frame, person edges require same camera/source epoch/frame and IoU≥predeclared tau, using person geometry **independent of PPE/state prediction and its confidence**. Use all real annotated persons, including unknown-state persons. Known GT state, not successful detection, defines the full-chain state denominator. Perform max-cardinality, then max summed exact IoU, then stable pairs. With fixed cardinality, minimizing `sum(1−IoU)` is equivalent. Integer/rational boxes admit rational IoU; otherwise freeze decimal/tick quantization once and preserve the conversion. Do not call rounded coordinates exact continuous geometry.
4. Apply predicted states only after person matching. Example with unique geometry pairs GA↔PA, GB↔PB: GT GA=N,GB=V; prediction PA=V,PB=N gives TP_V0,FP_V1,FN_V1 with N_known2. State-dependent re-pairing could hide both ownership errors. This fixture is executed and saved. Unmatched known violating GT remains FN; duplicates cannot create multiple corresponding persons. Unknown-state GT remains a person with separately counted unsupported assertions, not a generic ignore region.
5. Frame correspondence does not prove temporal identity. An alert's evidence/person pointer must resolve independently to a GT person/episode at its evidence anchor. Numeric tracker-ID equality is insufficient. Track changes can resolve to one continuing GT person; a recycled track ID can resolve to another. Unknown identity makes person-specific matching unresolved, not correct. A separately named scene/zone endpoint may be used when person truth is unavailable. No forced global GT-person↔tracker-ID bijection is imposed here: one tracker ID can switch people and one person can have several tracker IDs.
6. Event compatible keys require same actual source camera/continuity scope, violation definition, relevant zone/version, correct GT person correspondence, and evidence ownership. Stream epoch change is recorded; it need not create a new GT episode if independent continuity is established. Unknown linking across reconnect is retained as uncertainty. A group alert needs a separately defined actionable group GT; one alert cannot clear several independent people/episodes by default.

The optional detection-agreement protocol in W1_10 uses same-class edges. Person correspondence above deliberately does not gate on predicted PPE state/class. These are distinct layers and must not be merged.


## F259 — Exact event eligibility, objective and accounting
<a id="f259"></a>

Let G be the independently annotated event set, A the actually visible delivery-record set by close C. Repeated transport attempts that update the same visible record are not extra A; retries creating a second visible record are separate A. Preserve logical/attempt/visible IDs and all outside-close records. W2_02 defines immutable source evidence ownership, original-release mapping, source exposure and delivery wall time; this matcher does not rewrite them.

Each GT has exact observable onset s, half-open unsafe support [s,e), first sufficient causal evidence h, relevant known support/identity and a frozen deadline D≥0. Each alert has a genuine evidence anchor a and delivery d. All comparisons below use a declared common **elapsed clock** after an explicitly valid map; seconds are the reporting unit. All fixtures use one common clock and integral second ticks. Do not subtract native PTS from unrelated receiver clock, or use unpaced replay as live onset-to-delivery latency. Physical onset, observable onset s, sufficient evidence h, algorithm confirmation and delivery remain distinct fields. Here latency is d−s; it is physical latency only if physical onset is independently the chosen truth endpoint.

An exact edge requires compatible keys, sufficient causal evidence `h≤a≤d`, evidence a belonging to that episode's known active support, `0≤d−s≤D`, and `d<e` with GT known active at delivery. Equality at deadline passes; equality at end fails. Requiring active-at-delivery is a proposed utility endpoint; warning-after-end is another valid named policy requiring owner choice. Known true short episodes are not removed merely because they end before D. A delivery before sufficient evidence cannot be credited by retrospective onset backdating. No pre-onset collar is imported from audio.

For any feasible one-to-one matching M⊆E define key:

`key(M) = (−|M|, Σ_(g,a)∈M cost(g,a), tuple(sorted((g_id,a_id) for (g,a)∈M)))`.

For events cost=d−s (nonnegative exact ticks); for person boxes cost=1−IoU. Choose the unique minimum key. ID pairs are compared only after cardinality and cost, never as an epsilon added to a float. No edge means forbidden, never zero cost. Unmatched GT is an explicit skip; unmatched alerts are those not chosen. Empty graph and empty partitions are well defined.

Reference algorithm: sort G/A by immutable IDs; recurse over each G, either skip it or pair with each unused compatible A; memoize `(GT_index, used_alert_bitmask)`; retain the smallest full tuple at each state. Induction on remaining G proves the result enumerates every partial injection and minimizes the stated key. The sorted pair tuple is built in increasing G order. This is exponential in alerts; it is a correctness oracle for tiny graphs, not a recommendation to deploy it on long video. The code uses `Fraction`, exact integer/rational costs, and no numerical tolerance.

A scalable substitute must first determine maximum cardinality k, then find minimum cost among **exactly k** pairs, then choose the lexicographically smallest pair list among optimal matchings. One route is capacity-one min-cost flow with source demand−k/sink+k, followed by sorted-edge include/exclude feasibility checks preserving k and optimal cost: prefer the first edge if some optimal completion includes it, otherwise exclude it and continue. Edges conflicting with fixed included pairs are unavailable. This is a proposal, not executed NetworkX evidence. Preserve a future implementation/version and cross-check against this oracle; sorting the solver's input alone is not a proof of canonical tied output.

Within the **same known, complete, closed universe**, N_G=|G|, N_A=|A|, M=|matching|; TP=M,FN=N_G−M,FP=N_A−M; P=M/N_A,R=M/N_G,F1=2M/(N_A+N_G). Ratios are unitless; zero denominator→NA with counts. Both sets empty→P/R/F1 NA; G>0,A=0→R0/P NA/F1=0; G=0,A>0→P0/R NA/F1=0. Latency distribution has M samples; zero samples→NA. Micro aggregation sums counts from compatible closed strata before division. Do not silently discard undefined strata in macro averaging.

For original source cohort I, follow W2_02's separate precision/recall attribution unless a shared universe is demonstrably closed. In practice, obtain the full adjoining candidate matching neighborhood and all competitors, score that closed universe, then restrict the requested alert/GT cohort sides separately. A shared F1 on an expanded closed component describes that expanded universe, not automatically I. An exterior or unresolved competitor can alter which internal pairs are chosen.

Unmatched known deliveries receive an audit ledger, not just FP: compatible with an already served episode→excess/duplicate candidate; compatible semantics but beyond D or after end→late/after-end; known wrong person/type/zone; no matching GT; unresolved identity/truth/cohort; out-of-scope. Reasons can overlap, so save reason flags and, if a disjoint headline breakdown is needed, predeclare precedence. Semantic true duplicates/late alerts differ from semantically false assertions. All visible records remain operator workload. Never call every strict unmatched alert a semantic false alert. Retain per-alert eligible-edge list and rejected-edge reasons.


## F260 — Executed exact pair/count fixtures
<a id="f260"></a>

All graph costs and edges are explicitly constructed, not visual detections. `fixtures.py` asserts expected pairs, then checks every input permutation for each named graph. Counts below describe the fixture's closed universe; ambiguous examples presume all stated edges satisfy the frozen keys.

| Fixture / valid edges and costs | Selected pairs | TP / FP / FN | Cost/delay observation |
|---|---|---|---|
| G=∅,A=∅ | ∅ | 0/0/0 | P/R/F1 NA |
| G1, no A | ∅ | 0/0/1 | R0, P NA |
| No G, A1 | ∅ | 0/1/0 | P0, R NA |
| A1→G1(0),G2(0); A2→G1(1) | G1–A2,G2–A1 | 2/0/0 | Chronological A1→first G1 greedily yields only1 pair; offline reassigns |
| G1–A1(0),G1–A2(100),G2–A1(100) | G1–A2,G2–A1 | 2/0/0 | Cardinality precedes cost200; unrestricted minimum-cost partial matching could choose empty |
| Onsets0,2; deliveries3,4; complete graph | G1–A1,G2–A2 | 2/0/0 | Delays3,2 sum5 max3; tied alternative4,1 sum5 max4 |
| All four person IoU=.5 (cost=.5) | G1–P1,G2–P2 | 2/0/0 localization | Equal IoU tie fixed by IDs |
| Person edges IoU G1–P1=.9,G1–P2=.4,G2–P1=.4 | G1–P2,G2–P1 | 2/0/0 localization | Cardinality2 with summed IoU.8 beats cardinality1 IoU.9; gate assumed already applied |
| One continuing episode, A1 cost1,A2 cost2 | G1–A1 | 1/1/0 | Duplicate/split fragment or independently resolved ID-switch re-alert; extra remains FP/excess |
| G1,A1; wrong person or wrong type, no edge | ∅ | 0/1/1 | Reassigning to a nearby different person is forbidden |
| G1,G2 distinct safe-reset entries; one A1 eligible only for G1 | G1–A1 | 1/0/1 | Merged prediction does not notify second entry |
| Same reset entries; separate A1/A2 with one valid edge each | G1–A1,G2–A2 | 2/0/0 | Genuine re-entry has new GT; cooldown cannot rewrite it |
| Two G, two A, no valid edges | ∅ | 0/2/2 | Invalid edges are absent |


## F261 — execution record.
<a id="f261"></a>

**[F261](#f261) / execution record.** `python _WORK/W2_04_SOURCES/fixtures.py` completed successfully, all assertions passed:13 named assignment cases;512 possible labelled3×3 edge graphs cross-checked for cardinality with installed SciPy1.17.1; those same512 checked for all three objectives against a separately enumerated product of partial injections; all input permutations of named graphs;8 interval-edge cases;4 censoring ledgers; one wrong-person-state ledger; one shared-onset-constraint example. Saved `results.json` includes exact pair costs/IDs. This does not validate data import, annotation correctness, clock conversion, full external evaluators or production scalability. The SciPy cardinality comparison does not certify our second/third objectives; the independent exhaustive oracle addresses those only on these finite graphs.

Online chronological first-fit is an explicitly different convention. It may be appropriate for a fixed streaming decision audit but cannot retroactively revise a first notification. Our offline scorer can reassign earlier alerts using later context; it scores a frozen complete delivery set and does not change measured delivery times or prove a causal online policy. A future online endpoint must freeze arrival order, episode choice, tie rules and late-arrival behavior separately.


## F262 — Interval onset/end: exact claims, outer bounds and unresolved truth
<a id="f262"></a>

Annotation onset uncertainty `[l,u]` is a support set for the true boundary, not a confidence interval or a random uniform distribution. Unknown video gaps are state/identity uncertainty; clock error is uncertainty in a mapping; sampling confidence intervals refer to a probability design. Keep separate fields and reasons. The formulas below assume the stated independent interval support is valid; use a constrained truth set Ω if boundaries/identities/episode counts are jointly related.

With fixed h,a,d,D, onset s∈[l,u], end e∈[v,w] (state[s,e)), independently constrained and s<e:

- Definite edge: compatible keys and anchor ownership are known, `h≤a≤d`, `u≤a`, `d−l≤D`, `d<v`, and active-at-delivery truth known throughout all allowed worlds. This is eligibility for every allowed s,e.
- Possible edge: causal/key constraints can hold, and `L=max(l,d−D)≤U=min(u,a,d)`, with some allowed end e>d, and active/identity relation possible. Under simple independent closed end bounds this requires d<w. Equality d=w fails. An additional constraint such as a shared safe reset can invalidate this independent test; then mark unresolved pending joint treatment.
- Forbidden edge: none of Ω can satisfy eligibility. Otherwise possibly-but-not-definitely eligible remains unresolved for the point endpoint.
- Raw observable-onset delay lies `[d−u,d−l]`; for an eligible edge, feasible onset is restricted to[L,U], giving `[d−U,d−L]`. Do not report the minimum as an observed latency or clamp a negative raw lower bound to zero and call onset known. No need to invent a midpoint.

Uncertain episode existence/owner or pre-existing onset cannot be reduced to an arbitrary finite onset interval. If uncertain roster membership changes N_G, do not divide graph-bound counts by a fabricated fixed denominator. Report the unresolved roster/component, or compute metrics per jointly allowed truth configuration with denominator recorded in each world. Without this, leave point recall/F1 unavailable.

For **fixed G/A and jointly known eligibility population**, let E_def be edges valid in every Ω, E_pos edges valid in at least one Ω. For every world, `E_def⊆E_world⊆E_pos`; hence `maximum_cardinality(E_def)≤M_world≤maximum_cardinality(E_pos)`. This bounds counts, not which pairs the world-specific three-objective scorer chooses. A definite edge is not automatically selected in all worlds. Definite-only pair latency bounds are not the true scorer's selected-delay bounds. With fixed denominators the count bounds induce P/R bounds; they are deterministic sensitivity bounds, not statistical confidence intervals. They may be loose and endpoints may not be attainable. True attainable extrema require optimizing/recomputing the complete scorer over jointly feasible Ω, including boundary/identity/roster constraints; this branch does not claim such a general solver.


## F263 — LOCAL MATH, limiting counterexample.
<a id="f263"></a>

**[F263](#f263) / LOCAL MATH, limiting counterexample.** Two different person-specific episodes have linked annotation onsets s1=θ,s2=θ+1 with θ∈[0,10]. Deliveries d1=1,d2=11 belong to their respective persons, D=1, active end20, adequate causal evidence assumed. Edge G1–A1 requires θ∈[0,1]; G2–A2 requires θ∈[9,10]. Both edges are individually possible, so union graph has matching2, but no common θ supports both; attainable maximum is1. Script enumerates integer θ and verifies maximum1; the disjoint feasible intervals establish the same continuous result. This is a constructed annotation-constraint example, not measured camera/clock uncertainty. A similar hazard can arise from shared clock error, but clock errors must be modeled as their own joint variables.


## F264 — Eligibility and censoring expected-answer ledger
<a id="f264"></a>

Times below are common-clock seconds; D=5 is an illustrative parameter. The point-score column uses a closed, fully known singleton universe unless explicitly quarantined. “Possible count” means an edge-existence bound only under the listed independent truth alternatives. A1's causal anchor a must be real retained evidence, not a backdated prediction boundary.

| Case and fixed input | Eligibility / delay | Expected numerator and denominator / disposition |
|---|---|---|
| Exact s0,e20,h0,a0,d5 | Definite, d−s5; equality deadline accepted | G1,A1,M1 → TP1/FP0/FN0,P1,R1 |
| s∈[0,2],e20,h2,a2,d6 | Possible, raw delay[4,6]; timely worlds s∈[1,2], eligible delay[4,5] | Fixed G1,A1, M∈[0,1]; P/R bounds[0,1], no point classification |
| s∈[0,2],e20,h2,a1,d1 | Forbidden causal evidence (d<h) regardless of retrospectively early s; raw delay[−1,1] | G1,A1,M0 → TP0/FP1/FN1; audit unsupported/premature assertion; cannot call it measured onset detection |
| Known short s0,e2,h0,a0,d2; full truth/log through2 | Forbidden, delivery equals excluded end | G1,A1,M0 → TP0/FP1/FN1; known short event stays denominator |
| Same short episode, d1 | Definite, delay1 | G1,A1,M1 → TP1/FP0/FN0 |
| Known short s0,e2, no delivery, full truth/log through2 | Complete opportunity ends2 before D | G1,A0,M0 → FN1,R0,P NA; not right-censored |
| s0,end∈[3,5],a0,d4, full follow-up | Possible active-at-delivery; delay exact4 | Fixed G1,A1,M∈[0,1]; no point TP/FP assignment |
| s0,e10; anchor1 valid; state unknown[3,5),d4 | Active-at-delivery possible, not definite; delay4 if eligible | Fixed episode if continuation independently established; M∈[0,1]. If reset/identity could alter roster, whole component unresolved |
| Event already active when recording begins0; physical onset unknown, first sufficient evidence h0,d1 | Physical/incident onset latency unknown; not incident-onset cohort | Incident primary GT0/alerts0, separate pre-existing count1; startup-from-h endpoint may have G1,A1,M1,delay1 if that endpoint frozen |
| s28,e unknown after30; F30, d29 | Observed success, delay1, but required opportunity through33 incomplete | Primary complete-follow-up GT0/alerts0; quarantined GT1, observed-success1, alert1. Never include success alone in primary numerator |
| Same s28,F30, no delivery by30 | No full-deadline outcome known | Primary GT0/alerts0; quarantined GT1, observed-success0. Paired with preceding row: truncated stratum GT2, observed success1, full-window recall unresolved |
| s0, ongoing at recording stop6, D5, no delivery, complete log through5 | End right-censored but deadline opportunity complete | G1,A0,M0,FN1; unknown eventual end does not censor this deadline endpoint |
| s0,e20,a0,d6; log/GT complete | Known late; delay6 exceeds D | G1,A1,M0 → TP0/FP1/FN1 in strict timely endpoint; eventual matching endpoint can have TP1, explicitly separate |
| Same late delivery first appears after finite C5 | Not in delivered-by-C set; source membership unchanged | By-C G1,A0,M0,FN1 if deadline/log through5 complete; post-C ledger A1 late. Longer close cannot make it timely |
| Observed unsafe[0,2), observed qualifying safe reset[2,3), unsafe[3,8); alerts1,4 | Two GT episodes, edges G1–A1,G2–A2 | G2,A2,M2 → TP2/FP0/FN0; if cooldown suppresses second A: G2,A1,M1,FN1 |
| Unsafe before/after hidden[2,4), same person independently known; alerts1,5 | No observed safe reset; if continuation established, one GT | G1,A2,M1 → TP1/FP1/FN0 (second extra); without continuity evidence, roster/matches unresolved, not two invented episodes |
| Reconnect at3 during continuous unsafe; delivery1 then new-track delivery4 | With proven GT continuity, one episode, two A | G1,A2,M1 → TP1/FP1/FN0; with unknown continuity use quarantined identity/left-censor component |
| Known GT during processing outage, independent truth and delivery log through deadline complete; no alert | Eligibility unchanged by model unavailability | G1,A0,M0,FN1 operationally; tag processing failure. Unknown delivery log is unresolved follow-up, not known failure |

Eight direct onset/end edge rows are asserted by `interval_edge`; four censoring records and the wrong-person-state record are saved in JSON. Reset/reconnect/cooldown rows apply the executed one-G/two-A and two-G fixtures to explicit lifecycle assumptions; these are proposed ledger consequences, **not execution of a tracking, streaming, reconnect or cooldown engine**. The script's interval helper assumes its evidence anchor is independently known active; it does not infer that fact from a box or fill unknown gaps.


## F265 — Follow-up completeness without selecting successes
<a id="f265"></a>

For each allowed exact (s,e), the latest possible useful opportunity under the active-delivery rule is `r(s,e)=min(s+D,e)` (at e the state has ended, so the interval closes immediately before e). Primary complete-follow-up requires independent truth/ownership context and complete delivery ascertainment covering the opportunity, through `sup_Ω r(s,e)` under declared clocks. For exact short end e this can be before s+D. If e remains unknown but the state/opportunity is observed through s+D, the deadline endpoint is complete even though eventual episode end is censored. Unknown observation/state within the opportunity remains an eligibility uncertainty; simply observing a long file is insufficient.

Observation cutoff F, known state/identity gaps, source acquisition failure, processing outage and receiver-log close C are different fields. An algorithm outage with known GT/logs is an operational miss. Incomplete recording/GT or missing delivery logs can make the endpoint unresolved. By-C without delivery does not establish no future arrival; a delivery log closed through a passed deadline can establish no timely delivery, while later records remain workload/late outcomes.

For the primary point score, remove **the entire incomplete eligibility stratum**, including successes, and disclose its count. To avoid cross-stratum assignment changes, quarantine every potential-matching connected component touching uncertain identity/roster/eligibility or incomplete follow-up; include its alerts, successful pairs and GT in the unresolved ledger. Retain known semantically false records in their independent truth/workload ledger. This deliberately conservative complete-component endpoint is narrower than all requested footage and must report excluded counts/exposure; it is not an unbiased population recall estimate. If this quarantines most data, publish no primary F1 and obtain more context rather than broaden claims.

For the two s28,F30 cases above, complete-follow-up primary has0 eligible events, hence recall NA, not100%; truncated stratum has2 events,1 observed before-end success. A separately named observed-by-F endpoint includes **both** events and gives1/2 for that shortened opportunity. Full-D eventual success count is between1 and2 if exhaustive roster/follow-up constraints allow, so recall[.5,1] is a deterministic unknown-outcome bound, not an estimate or confidence interval. Different follow-up lengths must be reported; they cannot silently substitute for a common-D endpoint. No survival estimator is needed or claimed here.
