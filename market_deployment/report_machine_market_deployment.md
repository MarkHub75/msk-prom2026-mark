---
topic: market_deployment
context_version: mosprom-research-v1
checked_at: "2026-10-23T10:05:32.8161230+03:00"
checked_at_basis: "Evidence assembly completion recorded in _WORK/RUN_STATE.md; source access occurred earlier on 2026-10-23, not at report-writing time."
scope: "Russian-first industrial occupational-safety video analytics: competing products, deployment evidence, prices, buyer requirements, law, inference hardware, ownership cost, Moscow pilot mechanisms and falsifiable positioning; selective global comparators."
not_covered:
  - "linq_platform: SDK/compiler/runtime implementation and actual access validation"
  - "model_stack, violation_methods: model/repository selection and recognition implementation"
  - "datasets, training_strategy: dataset catalog, training and adaptation experiments"
  - "evaluation: complete model evaluation implementation"
  - "video_architecture, operator_product: full service architecture and user research"
  - "hackathon_strategy: final competition scope and pitch strategy"
answers:
  A01: "Which Russian/global products offer which functions, deployment modes and constraints?"
  A02: "Which public deployments and effects are documented, and how independent is the evidence?"
  A03: "Which dated license, service, procurement and hardware prices are known, and what do they buy?"
  A04: "What do customer specifications actually require, and can requirement frequencies be estimated?"
  A05: "Which personal-data, labor, CII, procurement and registry conditions constrain Russian deployment?"
  A06: "What documented barriers and operating costs exist; are pilot failures or their frequencies established?"
  A07: "Who initiates, approves, pays, integrates and operates; what remains customer-specific?"
  A08: "How can injury risk, labor, penalties, insurance and three-scenario TCO/NPV be estimated honestly?"
  A09: "Which hardware has Russian commercial evidence in 2026, and what can be claimed about LinQ?"
  A10: "How do Moscow nonfinancial pilots, grants and purchases differ; what happened to past winners?"
  A11: "How should a pilot measure event quality, response, exposure, labor and business value?"
  A12: "Which proposed advantages survive known alternatives, and how can the prototype falsify them?"
keywords:
  - "PPE / СИЗ / HSE / occupational safety / industrial safety"
  - "LinQ / ХайТэк / HighTech / IVA CV / Cognitive Solutions / ПАК ОТПБ"
  - "Macroscop / TRASSIR / DSSL / VizorLabs / Axxon One / NVI"
  - "Intenseye / Protex AI / Visionify / VisionAI / Voxel / viAct / EDGIRA"
  - "ШСУ / НТЭК / procurement / CCTV / VMS / NVR / BOM / SLA"
  - "152-ФЗ / 265-ФЗ / 187-ФЗ / 239 / 220 / 1875 / КИИ"
  - "631-ПП / 410-ПП / 2474-ПП / МИК / Moscow pilot / Rospatent"
  - "TCO / NPV / q / causal effect / exposure / false alerts / frozen evaluation"
entity_schema:
  competitors: [product_version_date, functions, deployment_egress_hardware, license_price_registry, customer_evidence, limits_references]
  prices: [item, amount_unit_date, evidence_parties, included_scope, unknowns_limits_references]
  effects: [project_period, result, evidence_origin, missing_design, permitted_use_references]
takeaways:
  - "PPE, respirators, smoking, zones, temporal rules, review, edge and some full-local modes already exist. IVA CV explicitly documented a LinQ PPE demonstration in June 2026; general 'PPE on LinQ is unique' is refuted."
  - "Public projects establish feasibility more strongly than causal injury reduction or transferable ROI. No comparable executed full PPE-system price, complete LinQ quote or causal safety coefficient was obtained."
  - "The fully read Russian industrial specification is n=1 and concerns design: 26 operating cameras plus 4 spares, at least 9 analytic points and at least 32 VMS/NVR channels are different quantities."
  - "Remote LinQ requires actual parties, countries, purposes, copies and processing authority. A Russian chip, no face recognition, blur or no archive does not settle personal-data/CII compliance."
  - "P and L remain unknown. The illustrative base incremental NPV is RUB 363930-(P+L); new infrastructure, q=0 and unsuitable cameras can invalidate labor-only payback."
  - "Moscow pilot status, grant and purchase are separate. Direct staffing gates were repealed; April resource scoring is a separate document whose October applicability is unconfirmed."
case_materials:
  available: "Short case announcement; mandatory inference on LinQ; promised online access; public competition site and relevant rules."
  unavailable: "Full case, final classes/events/metrics, organizer datasets, actual SKU/SDK/compiler/runtime/OS, access quotas, execution and data-processing terms."
actual_verification:
  completed: "Two saved research waves, fresh criticism and evidence assembly; document/web reading with source-specific locators; selected PDF pages visually inspected by researchers; illustrative model arithmetic executed by researcher D. Compressor read the final human report and saved evidence, and checked its own YAML, references and consistency."
  not_completed: "No new network research by compressor; no app development, model/device run, independent warehouse inspection, end-to-end hardware benchmark, commercial outreach, customer interview, legal opinion or causal-effect experiment."
  caveats: "Several full legal texts were read on normative mirrors, not obtainable official originals. Rosstat XLSX was read through a public PDF conversion. Access failures remain access observations."
human_report: report_human_market_deployment.md
evidence_files: [SOURCES.md, RAW_FACTS.md, CRITIC.md]
open_questions_file: OPEN_QUESTIONS.md
---

# Industrial safety video analytics: market, deployment and economics

Use a reproducible implementation on the supplied LinQ configuration, a stated applicability boundary and the chain **camera → event → accountable person → action**. Quality, price, setup speed, energy advantage, injury reduction and payback remain hypotheses until measured. This report is independently usable in English; the [Russian report](report_human_market_deployment.md) is the narrative counterpart, not a prerequisite. Evidence details: [facts](RAW_FACTS.md), [sources](SOURCES.md), [questions and proposed checks](OPEN_QUESTIONS.md), [criticism and W2 dispositions](CRITIC.md).

Terms: PPE = personal protective equipment (СИЗ); HSE = health, safety and environment; VMS = video management system; NVR = network video recorder; BOM = bill of materials; CII = critical information infrastructure (КИИ); MIC = Moscow Innovation Cluster (МИК); OT = occupational safety; SDK = software development kit; TCO = total cost of ownership; NPV = net present value; SLA = service-level agreement.

Evidence legend: **VC** vendor/interested supplier claim; **CC** customer claim (stronger provenance for project existence, still interested); **DOC** product/specification documentation; **LAW-M** law on a reference system/normative mirror; **LAW-O** official artifact; **STAT** official statistics with stated coverage/retrieval; **STUDY** published study, limited to its intervention; **OBS** local access/document observation; **INF** our inference; **ASSUME/CALC** explicit assumption/arithmetic; **U** unknown in this corpus, not proof of product absence. **IM** would denote an independent directly relevant measurement; no comparable causal PPE-on-LinQ injury/ROI measurement was obtained. Published vendor benchmarks remain VC measurements, not our test. F/S/Q/E identifiers are stable within `market_deployment`; ranges include their endpoints. Reprints of one release are one provenance chain.

The five-person team has an RTX 4070 computer, a laptop and possible cloud GPU access; OS, VRAM, drivers and quotas are unspecified. The case setter is ООО «ХайТэк». Helmet, removed respirator, dangerous-zone entry and smoking near flammables are announcement examples, not an exhaustive requirement. Full case/materials remain U (Q001/Q002). The initial competition schedule is 23–25 October 2026: full tasks 23 October 13:00; submission 25 October 10:00, a 45-hour window. An industrial pilot cannot be completed in that window. Relevant rules score criteria 0–3 and include effect versus development/deployment costs and audience/problem/competitor analysis. The site promises piloting of best solutions by Moscow's industrial department, without an individual funding amount, schedule or contract. DOC/VC F059–F060, S083–S084: [site](https://hackathon2026.otkroimosprom.ru/), [rules §6 pp.9–10](https://firsts3.ru/mosprom-2026/public/documents/polozhenie-mosprom-2026.pdf).

## A01 — Competitor functions, deployment, licensing and constraints

The class is established. Compare an added module in a suitable installed VMS, an analytically capable replacement camera, a specialized platform, a holding company's own stack and a new integrated hardware/software system (ПАК). Existing cameras/rights/resources require qualification; they are not automatically suitable or costless. Foreign products disprove worldwide feature uniqueness even where Russian procurement, delivery/service and lawful data processing are U. Catalog entries follow `entity_schema.competitors`; U applies only to stated missing fields, not an assertion of absence. Most entries are DOC/VC; no cross-product quality ranking was measured.

| product_version_date | functions | deployment_egress_hardware | license_price_registry | customer_evidence | limits_references |
|---|---|---|---|---|---|
| Macroscop workwear control; 4.7 released 13.10.2026, requirements updated 22.10.2026; exact supplied build U | Helmet, vest, respirator, glasses, shield, hearing protection, gloves/mittens, chosen clothing color; event journal; 4.7 phone/external-event journal with archive jump | Windows/Linux server VMS, version-dependent CPU/GPU/neural package; LinQ/mandatory egress U | One IP camera/listed capabilities; ULTRA analytics except LPR; price details A03; current exact registry U | Named PPE-module client U | Fix build: same URL exposed 4.6/4.7 navigation. VMS/neural-package updates linked. F005–F008/F168–F169; S008–S014/S207–S208 |
| TRASSIR/DSSL Hardhat 28515 and Wear 41902; build/publication date U | Hardhat absence; Wear color workwear/vest; alerts; Custom Detector for nonstandard tasks | NeuroStation/offload/VMS; SKU sizing, air-gap/mandatory egress and LinQ U | DSSL RUB 8900/9900 per processed channel; same-package term/VAT/base/key/server/support U; exact registry U | Named clients of these two modules U | Separate detectors, not a proven full respirator/shoes/smoking package; Custom Detector already offers adaptation, roughly week–month, separate server and priced logic. F001–F004/F118–F119/F170; S001–S007/S146–S147/S209 |
| VizorLabs H&S / distinct Platform 4.0; server guide 29.09.2026; supplied model/build U | PPE including respirator, smoking, zones, actions/regulations; zone/time/sequence/external-data rules; event card, notification, integration, human review | Cloud, hybrid local inference, dedicated customer environment; Ubuntu/Astra, Docker, NVIDIA; LinQ and exact egress/offline behavior U | Basic/Standard/Pro/4.0 branches A03; H&S 10990 and 4.0 33642 have different holders, direct current extracts U | LUKOIL Volgograd refinery, vendor case | Pilot camera/error checks and temporal/context rules already offered; fix edition and contract. F013–F017/F138–F139; S021–S025/S170–S173 |
| IVA CV / Cognitive Solutions; ПАК ОТПБ demo release 19.06.2026, event 9–10.06.2026 Tomsk; build U | Task-dependent PPE, phone, dangerous situations, alerts; site separately claims smoking; exact respirator classes U | Datacenter/cloud/edge; explicitly LinQ TPU plus NVIDIA/Intel/RK3588; exact TPU/board/runtime, HSE throughput/power/egress U | Platform/module rights, integration and support separate; price/term/transfer U; platform claims registry 7272 of 03.11.2020, current extract/new ПАК coverage U | Gazprom Transgaz Tomsk executive's favorable response in vendor release; buyer/acceptance/production deployment U | **Direct counterexample to general 'PPE on LinQ is unique'.** Demo is not shipment/benchmark/Gazprom purchase. Ownership/contract link to HighTech U. Website Linux ≥ 6.1 versus PDF ≥ 6.0 unresolved; PDF general minimum RAM 8 GB/disk 256 GB is not sizing. F171–F175; S210–S215 |
| Axxon One Equipment detector PPE, 3.0/3.1 context; docs 13.08.2026; supplied build U | Body segmentation; helmets in seven colors, yellow/orange vests; other sets trainable | CPU/GPU/Neuro Pack; gateway stop 5–10 s or freely moving production zone; egress/LinQ U | Price, exact Russian package/registry U | Named PPE client U | Not gateway-only: recommended 1 FPS gateway versus 7 FPS production. Claimed 80–95% accuracy/5–20% false detections lack comparable method. Do not equate English Axxon One with Russian «Интеллект». F009–F010; S015–S016 |
| NVI owl.Base / Guard+; mobile release 13.02.2026; build U | Seven typical personnel/PPE/zone/fire/smoke events; web, sound, reports; exact PPE U | Own/customer cameras/servers; mobile operation without stable connection; accelerator/egress U | Price, rights/registry U | Named client of examined package U | Up to 6 streams, 5-minute deployment, 8–12 h autonomy and IP65 are VC, not tested; mobile is not an empty niche. F018–F019; S027–S029 |
| Ivideon People add-on; base tariff help 06.05.2026; build U | Head-based counts; crowding, too few, restricted-zone presence/work-zone absence; PPE/smoking U | Cloud service/local archive with remote access; full isolated add-on/hardware U | Paid base required; RUB 200–875/camera-month paid annually, add-on price U; registry 9358 vendor claim, direct extract U | Relevant-module client U | Base CCTV/archive is not PPE pricing; local archive does not prove autonomous on-prem. F011–F012; S017–S020 |
| Dahua SD6E425MB-HNR-A-PV1-ATC; date U | Six helmet colors, uploaded uniform examples, masks/shoe covers, lone-worker/absence | Specific regional 4 MP PTZ camera with built-in analytics; egress U | Price, Russian delivery/registry U | Named client U | One SKU, not every Dahua camera; no transferable scene-quality result. F020; S030 |
| Hikvision explosion-proof/anti-corrosion AIOP brochure lead; date/build U | Indexed PPE-related lead only; exact supported functions U | Hardware/egress U beyond brochure family | Price, rights, Russian availability/registry U | Named client U | Full PDF unread; not a strong technical comparator. F021; S031–S032 |
| Intenseye; FAQ/privacy dates/build U | PPE/zones/unsafe acts, H.264/RTSP, notification API; privacy edge face/body masking, dynamic masking, storage control, timestamp anonymization | FAQ cloud/on-premise; exact mode/mandatory egress and LinQ U | Numeric price and Russian rights/registry U | Huhtamaki/Henkel/Oldcastle in vendor catalog | Older FAQ/new privacy differ on blur controls; fix configuration by contract, do not propagate one mode's clip retention to another. F085–F087; S113–S115 |
| Protex AI safety platform; build/privacy date U | PPE/risk rules, dwell, suppression, shifts, PLC state and feedback | Local RTSP appliance; standard cloud review receives roughly 10-second clips/metadata; blur, ghosting, videoless; appliance SKU/LinQ U | Numeric quote/Russian rights/registry U | DHL Denmark customer-confirmed PoC, not entire DHL network | Hybrid; videoless still has cloud metadata, not air-gap. Claimed two-week shadow mode/99% precision not comparative benchmark. F088–F092; S116–S121 |
| Visionify / VisionAI; documentation version/date U | PPE; exact respirator/smoking package U; Enterprise private-model training, API, customization and optional source access | Box full intranet with limited alerts/reports; SaaS edge+Visionify cloud; Enterprise customer infrastructure; verified current BOM/LinQ U | Partial USD 1299 plus U subscription; approved 30-day ≤ 10-camera trial/Order Form; Enterprise rights not established for Box; Russian rights/registry U | Relevant Enterprise named legal client U; anonymous testimonials | Recommended ≤ 3 scenarios/camera; scene geometry applies; optional sources do not confer free transfer to LinQ. F093–F096/F174; S122–S125/S214/S216 |
| Voxel; build/date U | PPE, ergonomics, vehicle interactions, spills, blocked exits, owner/correction tracking; temporal open-door logic | Edge + AWS cloud; body blur, RBAC, encryption; isolated on-prem/LinQ U | Price/Russian rights/registry U | Port of Virginia vendor case | Operational case metrics are not independent injury reduction. F097–F099; S126–S128 |
| viAct; build/date U | PPE, height, dangerous/confined zones, transport, housekeeping, ergonomics | Cloud/on-prem/hybrid claim less fully extracted than module list; exact hardware/privacy/LinQ U | Project/subscription lead, numeric price/Russian rights/registry U | Named examined client U | Partial page extraction; mode details weaker than feature evidence. F100; S129 |
| Everguard Sentri 360; 28.05.2020 release and NSC 2026 listing; current build U | Historical PPE/human-activity recognition and immediate alerts | Current architecture/hardware/egress/LinQ U; main site 403 | Price/Russian rights/registry U | Named examined client U | Old COVID modules not a current specification; 2026 catalog supports enterprise-offer existence only. F101; S130–S131 |
| Spot AI; vendor facts October 2026; build U | Broad security/safety/operations, API/webhooks; exact required PPE U | Local Intelligent Video Recorder AI/storage + cloud dashboard; guaranteed offline/LinQ U | Per-location subscription; amount/Russian rights/registry U | Named examined client U | Competes for CCTV infrastructure/budget; not a fully specified PPE alternative. F102; S132–S133 |
| EDGIRA; build/date U | PPE/zones/temporal/behavioral tasks, VC | Compact NPU/GPU local processing + cloud/on-prem orchestration; chip/egress/LinQ U | Price/Russian rights/registry U | Customers U | Counterexample to worldwide 'local NPU video' uniqueness, not independent benchmark. F103; S134 |

Macroscop camera constraints are **product-specific DOC**, not universal CV laws: color ≥ 1280×720, ≥ 3 FPS, even lighting, overhead tilt ≤ 35°, no PTZ in that scenario; head ≥ 60×60 pixels for small head PPE, glove hand ≥ 40×40, hands visible, glove presence ≥ 10 s; hidden face limits facial PPE. GPU Standard lists AVX, NVIDIA Compute Capability ≥ 6.1 and VRAM ≥ 4 GB, still requiring channel sizing. F006/S011: [requirements](https://doc.macroscop.com/analytics/hard-hats/requirements.htm). API availability is edition/operation-specific: reading `safetygear` settings through configuration API since 4.6 requires Enterprise/ULTRA and senior administrators. Clients not separately licensed; USB key transferable, activated software key machine-bound; Enterprise/ULTRA floating licensing documented. F007/F168, S012/S207: [API](https://doc.macroscop.com/rest-api/configure/channels/channel-id/safetygear/get.htm), [licensing](https://doc.macroscop.com/licensing/overview.htm).

Critical direct competitor sources: [VizorLabs H&S](https://vizorlabs.ru/products/health-safety/), [deployment modes](https://vizorlabs.ru/technology/docs/deployment-models/?product=platform4), [server guide](https://vizorlabs.ru/technology/docs/server-preparation/); [IVA CV demo release](https://ivacv.ru/когнитив-солюшнс-представили-свой-па/), [platform](https://ivacv.ru/platforma/), [admin guide](https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf); [VisionAI deployment](https://docs.visionify.ai/reference/deployment/), [Enterprise rights](https://docs.visionify.ai/reference/customization/); [Protex privacy](https://www.protex.ai/guides/privacy). URL path `/2026/05/` does not establish IVA guide publication date. Its binary download failed; researchers used saved web-extracted relevant pages, not a claimed local original. Older 2025 IVA slides omitting LinQ are superseded by the direct 2026 evidence.

Catalog limits: most suppliers' revenue/headcount/current registry extracts and foreign Russian supply/service terms U. Eocortex versus Russian Macroscop editions requires verification; ISS and others lack full separate cards. Selective coverage is not evidence that missing products/functions do not exist (Q019). Human review, privacy controls, temporal/context rules, adaptation and optional sources already occur in competitors. Blur alone does not prove legal anonymization: camera/time/shift/clothes can reconnect a person.

### Market-size boundaries: broad CCTV is not narrow HSE TAM

Narrow Russian HSE-video TAM/SAM is **U**, Q018. Do not average incompatible markets or turn monetary analytics share into technically accessible camera share.

- VC F105/S135, Ivideon 28.05.2026: 2025 B2B/B2G CCTV RUB 67.6bn; separately analytics RUB 9.4bn. Method describes public finances of 237 legal entities, selected 107 companies/93 brands and relevant revenue. Categories are broad and not additive independent markets. [Ivideon](https://ru.ivideon.com/blog/bezopasnost-i-analitika-k-2030/).
- Secondary analyst chain F106/F111–F112, S136–S137: TelecomDaily 22.07.2025 gives industrial analytics RUB 2.4bn in 2024, forecasts 2.8bn in 2025 and 5.6bn in 2030. Industry includes quality control and safety; full method U. 2.8bn is not observed 2025/2026 revenue; Seldon/SberPro are the same chain. [SberPro](https://sber.pro/publication/rinok-promishlennoi-videoanalitiki-viros-na-264-v-2024-godu-do-24-mlrd-rublei/).
- Paid-report abstracts only, models not reproduced (F107–F110/S138–S141): GVR January 2025 USD 37.84bn analytics by 2030; Emergen September 2026 USD 5.62bn 2025 base including analytics share of edge/cameras/servers; 360iResearch USD 14.61bn 2025 and 17.45bn 2026. GVR CCTV additionally includes equipment/VMS/services. [GVR](https://www.grandviewresearch.com/press-release/global-video-analytics-market), [Emergen](https://www.emergenresearch.com/industry-report/video-analytics-market), [360iResearch](https://www.360iresearch.com/library/intelligence/video-analytics).

INF bottom-up SAM structure: genuinely suitable sites × eligible cameras/scenarios × confirmed price over an agreed period × share with authority and budget to buy. Inputs remain U; this formula is not a revenue estimate.

## A02 — Deployment and effect evidence: existence is stronger than causality

Customer-side accounts establish projects/processes; none supplies a transferable causal coefficient for our PPE injury prevention or ROI. Alerts are not prevented accidents, and fewer registered violations are not necessarily fewer injuries. Effects catalog follows `entity_schema.effects`.

| project_period | result | evidence_origin | missing_design | permitted_use_references |
|---|---|---|---|---|
| Nornickel annual report 2024 | Event card to manager then occupational/industrial-safety coordinator; height, equipment danger zones, transport of people | CC, customer report | Injury effect, cost/ROI U | Evidence for event→responsible workflow. F024/F036, S036; [report](https://ar2024.nornickel.ru/ru/business-overview/innovation-technologies.html) |
| SIBUR, owner account 02.07.2020 | Tomsk/Tobolsk/Voronezh; some off-spec output/emergency stops avoided, no monetary calculation | CC, product owner | Comparable occupational injury endpoint/control/cost U | Mainly technological process effect. F023, S035; [account](https://habr.com/ru/companies/sibur_official/articles/509218/) |
| Gazprom Neft, 10.04.2024 | Dangerous actions detected in ≤ 3 s | CC, authored industry account | Streams/configuration/percentile/time boundaries U | Motivation to measure full latency, not transferable SLA. F025, S037; [account](https://www.secuteck.ru/articles/videoanalitika-dlya-neftyanoj-promyshlennosti-opyt-kompanii-gazprom-neft) |
| MMK | Chute-cover monitoring: time/percent closed, photo/email | CC, corporate material | PPE quality and monetary result U | Evidence for equipment safety analytics only. F030, S041; [MMK](https://mmk.ru/ru/press-center/news/na-mmk-mashinnoe-zrenie-pomogaet-v-proizvodstve-chuguna-/) |
| Kola NPP / Rosenergoatom, 2024 publications | 10-fold fewer violations over 5 years; up to 98% registration; 8 further NPPs in trial operation; corporate journal claims no injuries from improper PPE in controlled rooms and less labor | CC plus promotional CNews; official customer channel/corporate journal trace same interested claims | Exposure, 98% denominator, stable detector, concurrent measures, hours/roles/budget U | Violations, not 10-fold injury reduction; zero rare injuries is not zero risk; trial not confirmed serial rollout. F026–F027/F150–F151, S038/S189–S190; [customer](https://t.me/s/rosenergoatom/1789), [journal](https://atomvestnik.ru/2024/06/28/vvjer-v-cifrovom-izmerenii/) |
| CherMK, three-workshop pilot, 21.03.2026 | >400 detected violations, 8 types | Press-service account retold by RUБЕЖ | Period/person-hours/duplicates/FP/prior detection U | Detection volume, not '400 accidents prevented'. F028, S039; [publication](https://ru-bezh.ru/kompanii-i-ryinki/news/26/03/21/severstal-vnedryaet-ii-platformu-dlya-profilaktiki-narusheniy-pr) |
| Qmonitoring / ООО «РАЗУМ», Astrakhan housing construction 2025 | 64 first-month incidents; −80% violations; 95% unspecified metric; old-camera false PPE events; stream/threshold tuning together with contractor prevention | Interested primary project-award self-report | Frozen version, control/exposure, metric definition U; project June–November versus pilot completion September are different stages | Concrete camera/error mechanism; construction not factory; behavior change inseparable from reduced detector sensitivity. F149, S188; [project](https://globalcio.ru/projectoftheyear/list/53782/) |
| LUKOIL Volgograd refinery / VizorLabs | PPE/regulations/groups/rounds/zones, 640×480, 'up to 95%' | VC named customer case | Protocol/metric definition/independent acceptance/cost/injuries U | Industrial use claim, not measured recall. F016, S025; [case](https://vizorlabs.ru/projects/neftegaz/lukoyl/) |
| DHL Global Forwarding Denmark / Protex; release 29.11.2023 | PoC, observations followed by corrective actions | CC on DHL site/release | Causal injury reduction and global rollout U | Stronger existence evidence than vendor-only case. F091, S119–S120; [DHL](https://www.dhl.com/be-en/microsites/csi/computer-vision/logistics-use-cases/people-health-and-safety.html) |
| Intenseye / Huhtamaki, since 2023; Oldcastle | Claimed 23 sites in 10+ countries and reduced TRIR; Oldcastle machine-stop integration | VC customer catalog | Independent causal test/stop safety certification U | Maturity/use claims, not certification or local effect. F087, S115; [catalog](https://www.intenseye.com/customers) |
| Voxel / Port of Virginia | −50% speeding, −15% vest violations, +85% efficiency | VC case | Customer primary protocol/exposure U | Operational measures, not injury effect. F098, S128; [case](https://www.voxelai.com/customer-stories/the-port-of-virginia) |
| NLMK 2020, anti-concealment program from late 2019 | More recorded minor injuries explained by improved reporting | CC | Not a video-analytics intervention estimate | Registration can rise while observation improves; analogous measurement trap, not CV causal evidence. F029/F037, S040; [NLMK](https://nlmk.com/ru/sustainability/occupational-health-and-safety/?from=en) |
| Levine/Toffel/Johnson, Science 2012 | 409 inspected versus 409 control establishments; −9.4% injuries, −26% workers' compensation claim cost | STUDY independent of CV vendors; abstract/HBS release read | Full PDF/CLEAR evaluation not obtained; intervention is government inspection | Supports evaluation reasoning, coefficients not transferable to AI/Russia/LinQ. F031, S042–S043; [PubMed](https://pubmed.ncbi.nlm.nih.gov/22605775/) |
| Lee/Kim 2024 | 50 construction workers, controlled masonry task ~30 min, incentives/feedback | STUDY | Long-term factory injuries/ROI not studied | Short-term compliance design only. F032, S044; [paper](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2024.1430697/full) |

Keep version/exposure independent of the intervention. Counts can fall from threshold changes, people leaving view, less production or fewer workers; better registration can initially raise counts. A short pilot can assess events, response, labor and dangerous exposure; rare injuries/LTIFR need longer exposure and an appropriate design. Causal CV effect and documented industrial PPE failures remain Q013.

## A03 — Price register: module, platform, survey and contract are different units

A comparable RUB/PPE-camera range is **not established**. Normalize identical functions/concurrent detectors, coverage, edition, rights term/transfer, VAT, equipment, integration and support. Compare incremental additions symmetrically when infrastructure is suitable. Prices below are saved offers/records, not guaranteed future prices or executed-system costs. Catalog follows `entity_schema.prices`; hardware prices are also included here and qualified in A09. Dates U are not silently replaced by access date; web cards were accessed 23.10.2026.

| item | amount_unit_date | evidence_parties | included_scope | unknowns_limits_references |
|---|---|---|---|---|
| DSSL Hardhat | RUB 8900/processed video channel; publication date U | Primary current vendor web card | Detector with NeuroStation/VMS/channel context | VAT, rights term, base/key/server/work/support U; availability to clarify. F170/S209; [DSSL](https://www.dssl.ru/products/hardhat-detector-detektor-nalichiya-kasok/) |
| DSSL Wear | RUB 9900/processed channel; date U | Primary vendor web price | Color workwear, mainly vest | Not full PPE system; VAT/term U. F002/S003; [DSSL](https://www.dssl.ru/products/wear-detector-detektor-specodezhdy/?CODE=wear-detector-detektor-specodezhdy) |
| TRASSIR Hardhat / Tinko | RUB 8900 retail, 7565 wholesale/unit described as one channel; date U | Distributor offer | Hardhat module | VAT/term/support U; separate seller. F002/S004; [Tinko](https://www.tinko.ru/catalog/product/290200/) |
| TRASSIR / Syssoft | Quote only; stated 3–14 business days; date U | Reseller terms | Electronic perpetual license, one video channel | Cannot combine this term/delivery with DSSL price as one contract. F119/S147; [Syssoft](https://www.syssoft.ru/dssl/osnovnye-intellektualnye-moduli-trassir/) |
| TRASSIR AnyIP / Win 64 / Pro / Pro Win 64 | RUB 4590 / 5990 / 6390 / 7690 from 02.12.2024 | Historical primary recommended price | Base channel rights, not PPE | Not verified October 2026 price; XLSX dated 15.10.2026 found but cells unread. F004/S006–S007; [historical PDF](https://www.dssl.ru/partners/izmeneniya-v-prays-liste-dssl-s-02-12-2024-po-trassir.pdf), [price section](https://www.dssl.ru/integratoram/price/) |
| Macroscop / LNC | RUB 9000/module; date U | Reseller web card | Card actually describes helmet | Channels/build/VAT/term U; not current respirator quote. F008/S013; [LNC](https://www.lnc.ru/catalog/macroscop/licenses-and-extensions/workwear-control) |
| Macroscop LS/ST/Enterprise/ULTRA | RUB 3500 / 5000 / 9000 / 13000; date U | Linked store | ULTRA from 50 cameras, analytics except LPR included | Price unit unlabeled; do not assume channel unit or add LNC price. F008/S014; [store](https://macroscoptrade.com/aboutmc) |
| VizorLabs 3.0 Basic | RUB 120000/stream, minimum 5; revision date U | Primary indicative web tariff | H&S included | VAT/rights term U; work/infrastructure/SLA separate. F015/S024; [tariffs](https://vizorlabs.ru/tariffs/) |
| VizorLabs 3.0 Standard | RUB 3000000/50-stream package; revision date U | Same primary tariff | H&S, integrations/adaptation/BI described | VAT/term U; package÷50 is not a universal alternative-package channel tariff. F015/S024 |
| VizorLabs 3.0 Pro / 4.0 | Pro server RUB 950000 **or** cluster 1500000 + from 60000/stream; H&S RUB 600000 for Pro/4.0; 4.0 base individual | Same primary tariff | Distinct base/stream/H&S branches | Never add server and cluster branches; RUB 600000 not whole system or camera; VAT/term U, hardware/work/support/updates separate. F015/S024 |
| Ivideon base service | Online 200; Cloud 3/7/14/30 days 350/500/625/875 RUB/camera-month paid annually; help updated 06.05.2026 | Primary service help | Different cloud-archive depths | People add-on extra, price U; not PPE price. F012/S019; [help](https://support.ivideon.com/l_rus/knowledge_base/item/180905?b_from_widget=1%3Fsid%3D43348) |
| RedKrab custom development | Design from RUB 1m /15 business days; network from 10m /5 months; interfaces from 1m /15 business days; VAT excluded; revision U | Primary service offer | Separate stages; design 50/50 payment; customer buys hardware | Do not sum minima into fictitious quote for our site. F117/S145; [offer](https://redkrab.ru/services/razrabotka-iskusstvennogo-intellekta/videoanalitika/) |
| Visionify partial configurator/trial | USD 1299 + U subscription; date U; current trial 30 days ≤ 10 cameras | Vendor configurator/offer | Trial subject to approval and Order Form, no automatic renewal | Hardware literal not corroborated and excluded from hardware comparison; tax/geography/Russian delivery/full price U; old G2 amount not current terms. F095–F096/S124–S125; [pricing](https://www.visionify.ai/pricing), [trial](https://www.visionify.ai/starter-kit) |
| NTEK-32-877/24, 19.06.2024 | 83333.33, **currency unnamed**, VAT excluded | Primary concluded-contract register; NTEK / ООО «Софтлоджик Рус» | Survey turbine hall, boiler/turbine workshop, CHP-3, feasibility of PPE/OT video analytics | Header says 'in contract currency'; do not label RUB. Not deployment price, acceptance/payment proof or universal survey rate. Initiator УОТиПБ СП. F077/F179/F185, S103 p.1/p.18 row 257; [source record](SOURCES.md#s103), [read page](_WORK/W2_A_MATERIALS/NTEK_P18.png) |
| Rosseti Siberia №32616289558 / 26-4035, announced 13.08.2026 | RUB 11m including VAT, initial maximum price | Secondary Synapse/Energybase; customer licenses VizorLabs H&S, actual supplier U | Scope/count unknown without primary attachments | Synapse 'completed' versus Energybase cancellation/protocol archive unresolved. No primary specification/protocol/contract/fulfillment. '1 unit'/line count not PPE streams; no per-camera division or technical-failure claim. F022/F185, S033–S034/S110; [Synapse](https://synapsenet.ru/zakupki/fz223/32616289558%231--krasnoyarskij-kraj-priobretenie-licenzij-ispolzovaniya), [Energybase](https://energybase.ru/tender/019fff50-1f5f-70f1-bddc-ec92caa57b26) |
| LinQ HPQ / framework OEM | Numeric price U, quote only; access 23.10.2026 | Manufacturer OEM description and Russian catalog | Framework commercial terms tied to OEM hardware | Full host/decode/rights/VAT/stock/lead time/warranty/SLA U. F062/F181, S086/S174; [OEM](https://lin-q.ru/sol), [catalog](https://www.goszakupki-it.ru/catalog/resheniya_dlya_tsod_i_ii/uskoriteli_linq_dlya_ii/linq_hpq/) |
| NVIDIA T4 16 GB new board / Servermall | From RUB 118935; card VAT 22%, base 97488 +21447; access 23.10.2026 | Seller claim | Board; claims stock, one-year onsite warranty, RF delivery from 2 days | Manufacturer/PN to verify; host/software/rights extra; dubious FP4 line excluded. F143/S175; [card](https://servermall.ru/catalog/videokarty/nvidia-t4-16gb/) |
| Jetson Orin Nano Super 8 GB Developer Kit PN945-13766-0000-000 / ONPAD | RUB 76990 'all taxes'; VAT rate U; access 23.10.2026 | Seller claim | Module/carrier/Wi-Fi/Bluetooth/heatsink/power supply; claims stock | Storage not stated; three-month shop microcomputer warranty, software excluded, not public offer; Moscow MKAD delivery RUB 500; industrialization/service extra. F144–F145, S176–S178; [card](https://onpad.ru/catalog/cubie/nvidia/3914.html), [warranty](https://onpad.ru/warranty/), [delivery](https://onpad.ru/delivery/) |
| Huawei Atlas 200 module / Russian seller | Quote depends on payment/quantity; access 23.10.2026 | Seller 'in stock' claim | Embedded module | Exact PN/4 or 8 GB/VAT/SKU warranty U; carrier/host/power/HSE stack extra. F146/S179–S180; [card](https://russia-hw.com/modul-ii-uskoritelya-huawei-atlas-200/) |
| НТЦ «Модуль» NM Quad board | Numeric price U; sales contact for price/term | Manufacturer catalog | Board | Host/stack/PPE sizing/supply terms U; indexed conditions not fully read terms. F072/F181, S098/S187; [card](https://www.module.ru/products/modul-nm-quad/) |

Other procurement leads (DOC/OBS F120/F185): «Салаватстекло» B1903261413153 card describes per-operation control/OT analytics; DOCX not retrieved, price/winner U. Tender.pro 1201618 ООО «РТ-Инжиниринг» card mentions corporate design/deployment ≥ 20 cameras with simultaneous detectors; primary attachments/contract U. ШСУ design specification is read but price/winner/execution U. None supplies an executed comparable PPE delivery. Q008/Q009 are the next primary-document/normalized-quote tasks, not missing evidence to fill by interpolation.

## A04 — Customer specification: ШСУ design, n=1

The fully read Russian industrial specification is a **seven-page design task**, not a deployed system or representative procurement sample. It concerns CCTV for ООО «ШСУ» repair/mechanical area, 2026; approval day/month blank. Match to secondary procedure 114275-ТТ uses title/customer/file name, not a proven contract outcome. Thus 'almost always/often/rarely required' cannot be estimated. DOC F113–F116/F120/F180, S143–S144. [Primary specification](https://etp.metal-it.ru/files/get/62wbdjrEsToerTN9EwXP9CpFfBsF9xSzNKxV8QdmWuGdUN4P1Z9RmCqv6HC6Gmdg7j/%D0%A2%D0%B5%D1%85.%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5.pdf); [saved original](<_WORK/W2_A_MATERIALS/Тех. задание.pdf>); SHA256 `53499b8652f9a7f5cf99ecff9ea98968c78235183c0857b6620ed17ea8391a02`.

| Requirement | What the read ШСУ task says | Decision/limit |
|---|---|---|
| Camera quantities | 'Up to 30': 16 indoor +10 outdoor +4 spares =26 operating +4 spare | Not 30 operating PPE channels |
| Analytics | At least 5 indoor +4 outdoor cameras with built-in **or** server helmet/vest/shoes analytics | At least 9 analytic points, distinct from ≥ 32 VMS/NVR channels; LinQ not prescribed; concurrent detector load to clarify |
| Events/notification | PPE, danger zones, smoke/fire; responsible persons by email/mobile app | Event start/end/duration, PPE obligation and applicability need definition |
| Archive | ≥ 50 days; customer approves drive calculation | Inference sampling does not remove recording bandwidth/storage |
| Network/power | Segmented gigabit network; UPS ≥ 1 hour | Include PoE/switches/access and measured total load |
| Access | Parsec for **server-room door**; CCTV access roles | Not evidence of access-control identification of PPE offenders |
| Deliverables/time | Two paper copies +PDF; 20 business days | Design-document deadline, not industrial commissioning |
| Acceptance/change | Customer/contractor commission, project act; substitutions approved in writing; task changes by addendum | Design acceptance not installation proof; operating-system test/acceptance procedure (ПМИ) separate |
| Quality/security/service | Numerical P/R, FP/hour, latency and separate ПМИ not found in seven pages; air-gap/CII/exact registries/software SLA U | Not evidence of absent future demands or weak market acceptance; §8.2 replacement-equipment guarantees do not define whole application warranty |

Locators: S143 pp.2–5, especially p.3 §§4.1–4.3. Project form is useful for estimating integration scope; frequencies and typical prices remain U.

Other documents must retain their different populations/stages:

- DOC F078–F079/S104, Rosseti technology registry pp.36–38 §1.4: desired PPE/work-team perimeter/activity/work-time control, situational-center alerts/reports, customer server/virtualization, LAN/WLAN/WAN, ERP/ОТУ, encryption. It is a corporate desired-technology registry, not a tender specification. 96% is faces, <0.5 s biometric-database search, 99% security zones/events; no defined PPE event recall/end-to-end latency follows. [Registry](https://www.rosseti-sz.ru/upload/about/innovationpolicy/reestr2025.pdf).
- Foreign DOC F082–F084/F185, S107–S109: NRL 2019 PPE+ANPR installation within 12 weeks after PO; >80% refers to ANPR, INR 26000 is security, not system price. HPGCL includes 5 PPE cameras among 35 analytic cameras, SAT and five-year warranty/maintenance. TPSODL amendment 06.09.2024 has 40 PPE licenses, two VA/VMS servers for 400 cameras, VMS scalability to 3000; not 400/3000 PPE channels; price columns blank. These are not Russian prices, fulfillment evidence or a shared PPE threshold. [NRL](https://www.nrl.co.in/upload/Tender/NRL5102019103134AM_OC23000042_NIT.pdf), [HPGCL](https://hpgcl.org.in/uploads/tenderdoc/CCTVNITPTPSAddendum.pdf), [TPSODL](https://admin.tpsouthernodisha.com/Docs/Tenders/2024/COR7f271f4735c34c5c929a680f2e20a6c6.pdf).

## A05 — Russian law: data flow, employment, CII and procurement

Applicability depends on actual data/parties/purposes/countries and the customer's classified object/procurement. Several complete relevant legal texts were read on reference systems/mirrors; official originals, notably 265-ФЗ and FSTEC 220, were inaccessible. Do not label these reads official originals or rule out later amendments from transport failure. The preserved state is 23.10.2026; official artifacts and actual site facts remain necessary for a concrete legal conclusion. LAW-M/INF F121–F136/F178; Q004–Q007/Q020–Q022. This is a design-conditions map, not a site legal opinion.

### Personal data, biometrics and authorized processing

- **152-ФЗ art.3:** identifiable or indirectly identifiable video/tracks/time/camera/shift can be personal data (PD). Processing includes live use/transmission/anonymization, not merely storage. No face recognition, pseudonymous track ID or no archive is not proof of anonymization. Blurring a result does not undo the remote stand's prior receipt of raw frames. F039/F178/S054.
- **Arts.5/6:** fix necessary purpose, legal basis, scope/minimization. Occupational safety, investigation, jury demo and vendor general-model training are not automatically one purpose. Neither 'consent always required' nor 'safety never needs consent' follows universally. Statutory duties, consent and other bases have distinct conditions. F040/F121, S055–S056.
- **Art.11:** biometrics depends on physiological/biological features used by the operator to establish identity. Person/PPE/zone detection is not automatically biometric identification; linking to a badge is PD but not itself proof that physiological features establish identity. Face-template identity matching needs separate art.11/written-consent/exception analysis. Old RKN 2013 explanation is not treated as current universal permission; primary withdrawal artifact U. F042/F122, S057/S077.
- **Art.6(3–5):** map employer, organizer, team, stand operator, hoster, integrator, support and subcontractors to actual roles. Technical equipment 'operator' is not automatically PD controller; one party may process on instruction for one purpose and independently control another. Instruction must cover data/operations/purposes/confidentiality/localization/security/evidence/incidents; verify authority for outsourcing separately. Processor need not obtain separate consent under part 4; controller responsibility to subjects remains under part 5. Support access does not authorize vendor's own training. F121/F178/S056.

| Processing mode | Data that may remain personal | Required site-specific determination |
|---|---|---|
| Local non-identifying inference | Raw frames, track, time/camera/zone, PPE classes | Controller/basis, necessary purpose, notice/local acts, access, justified short buffer and card retention; outside access instructions |
| Remote LinQ raw frames | Frames/video and possible audio, network logs, caches/temp files, crash dumps/telemetry | Legal entities/roles of all recipients; country/database at collection and later stages; access/copies, outsourcing basis, localization and cross-border route |
| Clips/metadata | Short video, track ID, site/shift/time/classes/cards/exports | Reidentifiability, recipients of journal/email/messenger, retention/backups and prohibited reuse; only verified unlinkable aggregates may leave PD scope |
| Badge/face/training | Name/personnel ID, template/embedding, history, training frames/labels | Separate HSE/HR/training, identity purpose/biometrics if present, training authority and video/annotation/model rights/recipients/retention |

INF from F121–F129/F178: trace **camera/local buffer → preparation → channel → LinQ → result → journal/display → archive/training**. At each arrow record data, recipient, country, purpose and basis, including failure/support paths. Raw-frame model input cannot be described as 'anonymous aggregates only' without changing/verifying the input. Until Q004 is answered, use demonstrably permitted organizer tests, properly authorized staged data or synthetic inputs; this does not assert the organizer has already cleared all rights, nor waive mandatory LinQ.

### Localization, cross-border transfer and notices: exact dates

| Rule / preserved version | Product/process implication | Evidence / qualification |
|---|---|---|
| Art.18(5), wording of 23-ФЗ 28.02.2025 | Listed collection operations for RF citizens using foreign databases prohibited except enumerated art.6(1) grounds 2/3/4/8; consent alone is not listed | Not 'all foreign servers forbidden'; determine collection stage, database and basis, then later transfer separately. F125/S058; [art.18](https://www.consultant.ru/document/cons_doc_LAW_61801/cbf4e15b7c330f9372e876cdf2bc928bad7950ef/) |
| 265-ФЗ 26.07.2026, arts.1/7 | Art.12 amendment in art.1 effective **26.07.2026**; distinct art.2 concerning Moscow public information systems deferred **01.09.2027** | Full mirror read, official original U; do not defer cross-border amendment to 2027. F123/S148; [full mirror](https://meganorm.ru/mega_doc/FZ_upd_01082026/federalnyj-zakon/0/federalnyy_zakon_ot_26_07_2026_N_265-fz_o_vnesenii_izmeneniy.html) |
| Current read art.12 | Separate advance cross-border notification in addition to art.22; adequate-protection list matters, Convention membership not standalone immediate-transfer test | Part 10 listed country may transfer after notice before decision; part 11 other countries wait part 9 terms except specified vital-interest case; information request may suspend review. Not universal 'wait ten days'; account for recipient, safeguards, regulator restriction and part 14 destruction. F124/S149; [art.12](https://www.consultant.ru/document/cons_doc_LAW_61801/e4ebbe1780de623c7cf32a59ca82a7bb523a25dd/) |
| Art.22 | Former general employment-notice exception repealed: part 2 points 1–6 expired 01.09.2022; limited points 7–9 remain | Notice per purpose: subjects/data/basis/operations/methods. Changes by 15th of next month; cessation within 10 business days. Recheck new training/external recipient. F126/S150; [art.22](https://www.consultant.ru/document/cons_doc_LAW_61801/d996966e22e1320c9de1ab82d9f6be12c3d9d765/) |

A Russian chip or website domain does not establish country of processing. Geographies, citizenship, host/support copies and lawful collection remain U (Q004/Q022).

### Employee information, disciplinary decisions, security and retention

LAW-M/DOC F047–F048/F128, S064–S066: Labor Code **214.2** gives employer a right to remote recording/storage for work-process safety, not a universal duty to buy AI. **216.2** requires informing employees about recording means. Vologda prosecutor's official explanation 20.05.2024 describes visible coverage zones, signed notice and signs; changing rooms/similar areas do not match the work purpose. Explanation is not a new norm or consent for every reuse. [214.2](https://www.consultant.ru/document/cons_doc_LAW_34683/441967302a674ca7126cbc968e1e789100f5b0bd/), [216.2](https://www.consultant.ru/document/cons_doc_LAW_34683/2b217d80473de222d83a03b6f243c5223e3c39a1/), [official explanation](https://epp.genproc.gov.ru/ru/proc_35/activity/legal-education/explain/e334755/).

LAW-M F128, S062/S151–S152: **152-ФЗ art.16** limits solely automated decisions affecting rights/interests. **Labor Code 192** requires fault/work duty and consideration of circumstances with defined sanctions; **193** requires written explanation, two business days to answer, formal procedure/deadlines/appeal. Detection score/photo is not established guilt or an automatic fine. Full comparable employment judgment and criminal-liability case analysis were not obtained (Q020); human review does not legalize unlawfully obtained video. [Art.16](https://www.consultant.ru/document/cons_doc_LAW_61801/22e884a41450dcb5cb62d956583ad32abe2bbbe9/), [192](https://klerk.systems/docs/tk_rf/article/192/), [193](https://www.consultant.ru/document/cons_doc_LAW_34683/43ed606b7fffbec97c5ef7e6037b56e62094b34d/).

INF proposed process beyond statutory information: discuss purpose/errors/access/retention/correction/appeal with workers, HR and representatives before pilot; provide unconfirmed/unassessable statuses, human reason and correction log. This is a proposed trust/operating process, not an evidenced mandatory collective procedure or known union position. Frequency of worker resistance is U.

LAW-M F044–F045/F129, S059–S060/S153: arts.5/18.1/19 require purpose minimization, local acts, control/training, threat model, access/action accounting. **PP 1119** security level depends on system/threats/data/subjects, not 'no face recognition'. Contractor employees are not automatically employees of the controller. Russian OS/chip do not substitute for protection design; universal certification of every PPE detector is not established. [Art.19](https://www.consultant.ru/document/cons_doc_LAW_61801/ca9e5658710519f09ab2fdb8196fcb3eb024a051/), [PP 1119](https://www.consultant.ru/document/cons_doc_LAW_137356/8c86cf6357879e861790a8a7ca8bea4227d56c72/).

LAW-M F127/F178/S061: **art.21** confirmed inaccuracies corrected within 7 business days; unlawful processing stopped within 3 business days, if legalization impossible destroyed within 10 business days. Applicable incident: RKN notification within **24 h**, investigation results **72 h**. Termination/deletion after achieved purpose within 30 days with exceptions is **not** a universal exactly-30-day video archive. Buffer/clip/card/export/training retention each needs a basis, deletion/access procedure across agreed caches/processor/backups. Model unlearning/deletion from every artifact must not be promised without verification. [Art.21](https://www.consultant.ru/document/cons_doc_LAW_61801/d3fe43a7c415353b17faab255bc0de92bea127da/).

### CII and national procurement regime are separate tests

| Instrument / version read | Applicable distinction and product consequence | Evidence / remaining U |
|---|---|---|
| 187-ФЗ, edition 07.04.2025; 58-ФЗ main part effective 01.09.2025, read edition 26.07.2026 | Private Russian Federation (RF) entities in listed sectors can be subjects; significant-object status depends on categorization/registry. Separate server or 'demo' label does not establish exclusion | Transitional/own-use software conditions require object-specific analysis; no blanket immediate replacement of every factory stack. F130, S154–S157; [187-ФЗ](https://www.consultant.ru/document/cons_doc_LAW_220885/), [58-ФЗ transitions](https://www.consultant.ru/document/cons_doc_LAW_502581/b004fed0b70d0f223e4a81f8ad6cd92af90a7e3b/) |
| 360-р 26.02.2026; 1237-р 27.05.2026 | Typical-object list spans 14 sectors including metallurgy/chemistry/mining, not a substitute for functional/system boundaries | Amendment known from reference card; consolidated amended rows unread, no HSE object number assigned. F131, S158–S159 |
| Presidential Decree 166, edition 07.04.2025 | From 31.03.2022 approval for foreign software/services procurement for owned significant objects by specified 223-ФЗ customers; from 01.01.2025 use prohibition for public authorities/these customers with federal-law exception | Addressees not identical to every 187-ФЗ subject. F132/S078; [mirror](https://meganorm.ru/mega_doc/dop_norm_update_05072025/pnst_964-2024_predvaritelnyy_natsionalnyy_standart/0/ukaz_prezidenta_rf_ot_30_03_2022_N_166_red_ot_07_04_2025_o.html) |
| FSTEC 220, 16.07.2026 | Changes **235**, effective **01.03.2027**, not 239 from September 2026. Future Кзи calculation ≥ every 6 months, results to FSTEC in 5 business days; Узи every 3 years and for relevant contractor before access then every 3 years; head informed of nonconformity within 3 calendar days | Relevant full text on mirror; official original U. Roadmap, not hackathon-date duty; no separate published alleged 2026 amendment to 239 established. F133, S160–S164; [220](https://rulaws.ru/acts/Prikaz-FSTEK-Rossii-ot-16.07.2026-N-220/) |
| FSTEC 239, edition 28.08.2024; mirror states effective 05.11.2024 | §31 already limits outside remote updating/administration, uncontrolled local access and uncontrolled transfer to developers/others. If remote access cannot be excluded, authorized persons/devices, least privilege, monitoring, protected channel/action logs; relevant storage/processing in significant category 1–2 objects located in RF subject to exceptions | **Remote inference is not automatically remote administration or every API forbidden.** Determine boundaries/roles/flows; §§28–29 have distinct conformity/application-software conditions. F134/F136, S162; [§§28–31](https://meganorm.ru/mega_doc/dop_fire_update_01052025/kodeks_rossiyskoy_federatsii_ob_administrativnykh/5/prikaz_fstek_rossii_ot_25_12_2017_N_239_red_ot_28_08_2024_ob.html) |
| PP 1875, reference-system edition 30.09.2026 | Check customer 44/223/private, subject/appendices, OKPD2 **and** name, rights form, exceptions and procedure date. Software origin has own registry proof; trusted software separately specified | Some cloud delivery, preinstallation, development/modification with rights transfer included: SaaS not automatic exemption. National regime not created merely by private factory's RF address. F135/S073; [§§3–4](https://www.consultant.ru/document/cons_doc_LAW_494318/92d969e26a4326c5d02fa79b8f9cf4994ee5633b/) |

Deployable compliance package (INF): recipient/country/purpose map; legal basis/processing instruction; notices/local acts; retention/deletion; threat/access model; actual CII/procurement classification; exact complete-kit registry documents; human confirmation/appeal. Registry layers and supply scope are in A09, not automatically inherited from Russian silicon.

## A06 — Deployment barriers, failure evidence and operating responsibilities

No representative barrier frequencies or fully verified industrial PPE contract/litigation proving failed scaling due to the algorithm were obtained. Difficulty is not proven failure; missing rollout news is not a negative outcome (Q013). Evidence supports these **specific mechanisms**:

| Mechanism | Documented observation | Mitigation / evidence boundary |
|---|---|---|
| Domain false positives | Volzhsky Pipe Plant OT representative describes moving machine parts detected as people, own dataset jointly prepared; email has shop/area/video danger-zone link | CC F080/S105; no numeric FP or abandonment established. Inspect scene and hard negatives before training. [Account](https://hsedays.com/ru/insights/video-analytics-safety-violations?geo=com) |
| Unsuitable imagery | РАЗУМ describes old-camera resolution/view/angle/sun/night and false PPE events | Self-report F149/S188; survey object pixels/light/occlusion; invisible PPE cannot be recovered by training. Not all existing cameras are free reusable input |
| Access/acceptance organization | Center 2M says camera access took 3 weeks: unavailable head, expert lacks signal owner, security uninformed; tests delayed by unprepared participants; links acceptance to ТЗ/ПМИ | Integrator self-report, anonymous customer/date/scaling outcome U. F081/S106; appoint owner/approvers/acceptors before pilot clock. [Account](https://center2m.ru/etapi-razrabotki) |
| Analytics overload hidden by healthy video | НЕЙРОСС documents skipped analytical frames under resource shortage while decoding continues; load depends on scene/objects/profile, ROI/perspective/debounce | DOC F075/S101; separate stream health from event quality and expose frame loss. [Docs](https://support.itrium.ru/pages/viewpage.action?pageId=923241165) |
| Camera degradation | Axis Image Health Analytics covers obstruction, shift, blur, underexposure | DOC F076/S102; product-specific PTZ stabilization delays not universal. [Docs](https://help.axis.com/en-us/axis-image-health-analytics) |

Privacy, worker/union resistance, ownership changes, missing budget, lock-in, drift and insufficient ROI are sensible interview/planning hypotheses, not measured common causes here. F187 is an indexed adjacent hospital/security administrative dispute, **not industrial PPE failure**; no algorithm-failure inference uses it.

INF operating scope F006/F063/F075–F076/F169/F177: include scene qualification and correction labor; labels/export/quantization/compile/INT8 validation; zones/thresholds/deduplication; integration/training; cameras/PoE/network/channel rights/CPU/RAM/SSD/decode/archive/redundancy/concurrent clients; confirmation/escalation/action minutes for **true and false** alerts; repair/substitute/spares/travel and permitted support; compatible OS/driver/runtime/VMS/neural-package versions, update window/control set/rollback; camera/network/queue health plus random non-alert video to find misses. Agree responsibility for cleaning/re-aiming cameras, new light/PPE/work changes, labeling and post-update reacceptance. Suppliers may differ across camera/VMS/accelerator/model; assign one intake/diagnosis path and who pays.

SLA must separately cover pipeline availability, restoration and algorithm quality **within agreed observable conditions**. A server running 24×7 is not visibility or zero misses. Contractually handle obscured camera, scene change, network loss and overload; 24×7 corporate support without numerical response/restore is not a numerical SLA (Q024).

## A07 — Buyer, payer, integrator and procurement path

Observed roles are organization-specific: Nornickel manager/OT coordinator review events; NTEK УОТиПБ СП initiates survey with Softlogic Rus; ШСУ customer/director signs a design task. These do not establish HighTech's buyer, org chart or budget owner. DOC/CC/INF F024/F058/F077/F113/F184, Q012.

Proposed discovery sequence: shift responder defines action → OT/industrial safety validates risk/rules → IT establishes camera/VMS/RTSP/API/network/archive ownership → security/legal approve data/access → budget owner/procurement define value, CAPEX/OPEX limit and procedure → integrator delivers interfaces/commissioning → operations accepts support. This is a meeting/RACI hypothesis, not a measured typical-market role distribution. Design signatory may not own rollout budget; survey initiator may not fund server.

An integrator can bridge camera/network/VMS, accelerator/runtime, event rules, archive/alerts, staff training and field repair. HighTech's role (hardware seller, technology partner or full offer member) is U. Establish who licenses, signs acceptance and diagnoses 'camera/video works, analytics misses' before pilot finishes. Survey, design, pilot, rights, installation and support may be separate purchases. Apply 44-ФЗ, 223-ФЗ or private contract according to actual entity/subject, not the word 'factory'; future procedure/deadlines/participant conditions remain U (Q008/Q012/Q016/Q024).

## A08 — Economics: statistical coverage, risk and reproducible conditional NPV

The evidence permits a **conditional spending threshold**, not a typical-factory quote, forecast or proven payback. No local causal risk reduction, complete LinQ node price `P`, full rights price `L`, monetizable labor baseline or customer loss data was obtained. Mandatory/social safety value can justify spending with negative monetary NPV; label that decision explicitly.

### Rosstat injury data: observed population, not all RF incidents

STAT F152/S191: `pr_travm_2025.xlsx` was visually read through Google Docs Viewer PDF conversion; origin XLSX not retrieved, cells not independently compared with origin. [Rosstat origin](https://rosstat.gov.ru/storage/mediabank/pr_travm_2025.xlsx), [read conversion](_WORK/W2_D_MATERIALS/pr_travm_2025_VIEWER_CONVERTED.pdf).

| Year | Injured | Fatal | Disability person-days | Days per injured person | OT spending per worker |
|---|---:|---:|---:|---:|---:|
| 2025 | 20.8 thousand | 1.07 thousand | 0.96 million | 46.1 | RUB 31459.8 |
| 2024 | 21.4 thousand | 1.04 thousand | 0.97 million | 45.3 | U in this report |

Rounded thousands are not exact integer cases. OT spending/worker is not cost/injury; falling total does not imply every risk fell. Excludes DNR/LNR/Kherson/Zaporizhzhia regions. F153/S192/S196: Rosstat 538 of 30.09.2025 appendix 2 explicitly concerns `7-травматизм`, with enterprise types, OKVED/OKOPF, thresholds/exclusions. **15–20% sampling applies only to type 1, not the entire final statistic**; another organization portion has no such percentage in read conditions. Historical method combines complete large/medium and sampled small firms excluding microenterprises, but current detailed catalog is more complex and type codes not all decoded. Relevant appendix pages were read, not the entire 246-page order. [Order 538](https://www.rosstat.gov.ru/storage/mediabank/met_538-30092025.pdf), [historical method](https://rosstat.gov.ru/storage/mediabank/MET_travma.pdf).

Safe scope: surveyed population with different observation components, not all workers/all accidents in Russia. Moscow-city primary number U: Mosstat catalog found, table inaccessible; catalog 64507 is **Moscow Oblast**, not city. Rosstat/SFR/Rostrud populations must not be summed. National counts do not provide risk per camera; use site's injuries, work/person-hours, relevant exposure and uninsured loss composition (Q014/Q015).

### Risk, penalties and insurance must not become invented revenue

INF F038/F186:

```text
E[B_risk] = sum_i Exposure_i * lambda_i * a_i * e_i * C_i
```

`Exposure` = comparable person-hours/operations; `lambda` = relevant baseline injury frequency per unit; `a` = portion reachable by chosen scenario/view; `e` = **causal** reduction with working response; `C` = enterprise's uninsured Russian cost. All require local evidence. Precision/recall are not `e`: a correct alert may not be acted on and the action might never have produced injury. Do not import US-dollar injury costs or national average risk. Avoid double counting downtime/output loss, substitute labor/productivity loss, compensation/covering insurance. Downtime needs documented hours, production boundary, recovery capacity and uninsured loss; universal RUB/hour U. Risk benefit is **zero as unproven monetary income** in the model, not a claim of no human/social benefit.

LAW-M F035/S049, КоАП5.27.1 read edition 04.08.2026: legal-entity part 1 warning or RUB 50000–80000; part 4 failure to provide PPE RUB 130000–150000. A missing helmet in video does not establish failure-to-provide offense, liable party or inspection probability. `alerts * RUB150000` avoided-fine calculation is invalid. [Article](https://www.consultant.ru/document/cons_doc_LAW_34661/88755cc3b9fd053aebba33b58078eb459aa5a1d8/).

LAW-M/DOC F034/F154, S048/S193–S195: SFR discount **up to 40% of the established insurance tariff**, not payroll/all contributions. Under 125-ФЗ art 22/PP 524/method 39н compare three-year paid-benefits/contributions, insured cases per 1000 workers, disability days per nonfatal case with sector values; all three must be below sector for discount, plus СОУТ/medical checks and restrictions. Insurer decides. Application no later than **1 November**, ≥ 3 years activity, no specified debt/penalties/fines at application; decision by **1 December**. Fatal-case restrictions, 2025 shelling/terrorism exceptions and АУСН exclusion apply. Full numeric reconstruction of partly image-published formulas was not executed. [SFR21.10.2026](https://sfr.gov.ru/branches/novgorod/news/~2026/10/21/285762), [125-ФЗ](https://www.consultant.ru/document/cons_doc_LAW_19559/08e74b4d74c4e346d83aa85a9473ae5f2ab91b7c/), [PP 524](https://legalacts.ru/doc/postanovlenie-pravitelstva-rf-ot-30052012-n-524/), [39н](https://www.kontur-extern.ru/info/normativ/document/1/501493-prikaz-mintruda-rf-ot-01-08-2012-n-39n).

Conditional incremental insurance benefit = insured base × tariff × (discount with project − discount without). At a purely assumed 1% tariff, maximum 40% discount is **0.4 percentage points**. Cameras alone do not earn it; baseline discount cannot be attributed to project. Risk, fines, SFR benefit and grants are zero in evidenced base cash benefit until separately justified.

### Cost boundary and assumptions: same nine-point result, two investment variants

ASSUME/CALC F155/F177/F182/E008; [MODEL.py](_WORK/W2_D_MATERIALS/MODEL.py), [saved results](_WORK/W2_D_MATERIALS/MODEL_RESULTS.json). Researcher D ran arithmetic, not hardware. Shape borrowed from ШСУ design:26 operating cameras+4 spares, ≥ 32 VMS/NVR channels, 9 PPE points, 50-day archive, UPS ≥ 1 h. Required equal illustrative result: helmet/vest/shoes on those 9 points, access/alerts and agreed quality. Wear-only price is not equivalent.

**A = incremental addition to proven suitable installed infrastructure.** Cameras/VMS/archive/UPS and resources already paid for; verify suitability, do not count sunk cost as new. **N = new whole CCTV infrastructure** for same result. Conservatively all common costs allocated to project here; customer must allocate them explicitly for multiple purposes. Never burden competitor with a full new contour while costing only our detector.

| Initial input | Value, RUB unless stated | Provenance / boundary |
|---|---:|---|
| `P`, complete LinQ compute node(s) | **U** | Need board/host/memory/cooling/decode/delivery/warranty and measured node count |
| `L`, complete initial rights | **U** | PPE 9 points/runtime-OEM/integration, scope/term U; annual rights belong in OPEX, no CAPEX duplication |
| A survey | 40 h×1500 =60000 | Assumption, not market rate |
| A integration | 80 h×1500 =120000 | Assumption |
| A acceptance/validation | 40 h×1500 =60000 | Assumption |
| A training/procedure | 20 h×1500 =30000 | Assumption |
| A other initial reserve | 30000 | Assumption, not quote |
| N additional cameras/spares | 30×12000 =360000 | Quantity from task; unit price assumption |
| N additional network/PoE; archive; UPS | 80000;150000;50000 | Assumptions, capacity/power still uncalculated |
| N additional VMS; design; installation | 32×6000 =192000;60000;120000 | Only channel count 32 from task; rates assumptions, not DSSL historical price |

`I_A=300000+P+L`; `I_N=1312000+P+L`; `X=P+L>=0`. `X=0` is an optimistic lower-cost bound for falsification, **not free LinQ/rights**. Archive assumption is not capacity proof:26 cameras×2 Mbit/s×50 days gives **28.08 decimal TB** before RAID/reserve/metadata;2 Mbit/s assumed, camera count/days from task. General formula `TB=cameras*bitrate_Mbit_s*86400*days/8/10^6`. Sparse inference need not reduce streaming/archive bit rate.

All model sums: RUB constant prices at assumed `t0`;3 years, 10% discount, zero residual, initial spend at`t0`, annual cash at year-end, no borrowing/profit tax/inflation. Costs after recoverable VAT; customer's VAT status U, nonrecoverable VAT add separately. Not a cash procurement budget. For uneven payments use year-specific cash flows.

`H` = **displaceable previous labor** hours/month at equal coverage, not all safety-team time or an imaginary 24 h operator. New coverage may have `H=0`. `q∈[0,1]` = portion actually changing paid labor/overtime/contracting or a documented avoided hire. Redeployed salaried time can be useful capacity without cash saving. All new analytics review/admin/retraining labor is `H_ai` in OPEX and **not subtracted from H again**. Model charges new labor fully even if absorbed internally (conservative resource cost); distinguish actual cash payments separately. Previous/new operating labor assumed RUB 800/h, initial engineering RUB 1500/h. `S` = support excluding already-counted new labor.

Assumed compute energy 0.3 kW×8760 h×RUB 8/kWh =**21024/year**; neither power nor tariff measured. N adds CCTV 0.08 kW plus RUB 24000 maintenance =**29606.4/year**, not duplicated in LinQ energy. General energy formula: average AC kW×hours×documented ancillary-infrastructure factor×tariff. One continuous kW is 8760 kWh/year (arithmetic). TDP is not average AC; arbitrary PUE must not be assigned.

```text
G = 12 * H * 800 * q                  # gross monetizable labor benefit/year
O_A = S + 12 * H_ai * 800 + 21024     # new annual cost
O_N = O_A + 29606.4
C = G - O                            # net annual cash/resource flow
TCO_3 = I + 3*O                       # undiscounted
F = sum(t=1..3) 1/(1.1)^t = 2.486851991
NPV_3 = -I + C*F
simple_payback = I/C                 # only C>0
H_break_even = (O + I/F)/(12*800*q)   # NPV_3>=0, only q>0
NPV = -I_0 + sum_t((B_t-O_t)/(1+r)^t) + Residual_T/(1+r)^T
```

At `q=0` no labor cash payback and division by q is undefined. Broader coverage is not displaced prior service.

### Three illustrative scenarios and adverse stresses

Every H/q/H_ai/S is an **assumption**, not industry interval/probability/observed site result. X stays unknown; NPV rounded to RUB. O/C values annual.

| Scenario | H h/month; q; H_ai h/month; S RUB/year | O_A | C_A | NPV_A3 | NPV_N3 |
|---|---|---:|---:|---:|---:|
| Conservative | 60;0;40;144000 | 549024 | −549024 | −1665341−X | −2750968−X |
| Base | 120;0.5;20;96000 | 309024 | 266976 | 363930−X | −721697−X |
| Optimistic | 160;1;10;72000 | 189024 | 1346976 | 3049730−X | 1964103−X |

Base `TCO_A3=1227072+X`, `TCO_N3=2327891.2+X`; gross monetizable benefit over 3y RUB 1728000. Simple payback A `(300000+X)/266976` years; N `(1312000+X)/237369.6` years. Unknown X means formulas, not a LinQ payback date.

Base A nonnegative NPV requires **X ≤ RUB 363930**. This is one artificial model's spending ceiling, **not price, quote, market limit or suggested LinQ selling price**. Base N negative already at X=0: labor savings insufficient before compute/rights. Base A operating break-even H 64.38 h/month; three-year investment threshold at X=0: A 89.51, N 180.46 h/month. Positive X increases thresholds; annual L reduces affordable upfront amount by present value of recurring rights.

| Stress, retaining base conditions except stated | Result | Consequence |
|---|---|---|
| q=0, H120 | NPV_A=−1068497−X | Time freed may be useful, cash savings unproven |
| Unsuitable cameras: assumed RUB 180000 correction/replacement, H_ai 40 h/month, S 192000/year | O 597024; C−21024; NPV_A=−532284−X | Mechanism grounded in РАЗУМ, amounts assumed. If view cannot be restored, coverage unequal: stop/redesign rather than claim cheapness |
| +20 h/month review/admin | +RUB 192000/year cost; NPV −RUB 477476 | True alerts also consume capacity |
| +RUB 96000/year support | NPV −RUB 238738 | Combined with labor stress eliminates positive base bound before CAPEX changes |
| More nodes, larger archive/UPS, actual AC, repeated L, grant 0 | Numerical inputs U; costs can rise | Measure/quote, do not replace missing economics by invented prevented injuries |

Negative NPV does not prove a mandatory safety measure useless. Customer may explicitly purchase better control or duty fulfillment under a different criterion; monetary payback then remains unconfirmed.

## A09 — Inference hardware, Russian supply evidence and LinQ position

Distinguish catalog listing, orderability, seller stock claim, contracted lead time and fulfilled shipment. A03 records saved Russian offers; no independent stock inspection or comparable fulfilled-delivery register. T4/Jetson price is not LinQ price; developer kit, board and complete HSE system are different units.

LinQ has PCIe HP/HPD/HPQ, rack HPS and HX SBC (LinQ+RK3588). Ecosystem examples are interested primary announcements: Graviton 23.09.2025 HPC with two HPS, RSK ScaleStream-C PCIe array and С2122ИУ server; Astra 07.10.2026 HX integration with Astra Linux Embedded/joint development. These do not establish named HSE customer, whole-PАК certification, all-SKU serial availability or price (F061/F066–F067, S085/S089–S090). [LinQ](https://lin-q.ru/), [Astra](https://astra.ru/about/press-center/news/khaytek-i-gruppa-astra-razrabatyvayut-sovmestnoe-reshenie-na-osnove-rossiyskogo-ii-uskoritelya-dlya-/), [Graviton](https://graviton.ru/news/graviton-linq-i-rsk-razrabotali-rossiyskiy-pak-dlya-zadach-ii-s-rekordnoy-proizvoditelnostyu/).

VC F147/S185: Aquarius–HighTech–NtechLab agreement 19.05.2026 for AQserv+LinQ+NtechLab; first commercial deliveries **planned** H2 2026. SKU/customer/price/acceptance/shipment U, not confirmed delivery. [Aquarius release](https://www.aq.ru/press-center/news/aquarius-khaytek-i-ntekh-lab-sozdadut-pervyy-polnostyu-rossiyskiy-pak-dlya-ii-zadach-/).

### Performance and power claims retain workloads and boundaries

| Hardware/reference | Preserved number and test context | Invalid extrapolation |
|---|---|---|
| LinQ2026 presentation | i 7-10700K, Ubuntu 24.04, Runtime 16.18.6, Framework 2026.8.43, references MLCommons MLPerf method. HP `yolo5s` batch 1 throughput 106.1 FPS/latency 23.71 ms; `yolov8n_pose`104.8 FPS/21.51 ms. HPQ throughput 424.4/419.2 FPS respectively | Vendor measurement, not independently verified MLPerf submission, our PPE model or camera count; some other latency units/method unresolved. Throughput reciprocal and latency can differ by execution mode. F065/F073, S088/S099; [presentation](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf) |
| LinQ power | Presentation HP<30, HPD<55, HPQ<105, HPS<1150, HX<45 W; HPS datasheet TDP300/600/900/1500 W by frequency/cooling/power management, 3U up to 1500 W | **HPS 1150/1500 modes unresolved**; component ceilings/TDP not average wall power. Video ASIC is optional, not included decode.24×7 corporate support has U price/response/restore/substitute. F063–F064/F148, S087–S088; [datasheet](https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf) |
| NVIDIA DeepStream 7.1 T4 | 45 H.265 or 31 H.264 streams 1080p 30, TrafficCamNet+IOU+two classifiers, rendering/OSD/tiler off, batch=N | Traffic workload, not PPE or team's RTX4070 benchmark. F069/S095; [table](https://archive.docs.nvidia.com/metropolis/deepstream/7.1/text/DS_Performance.html) |
| Huawei Atlas 200/Ascend 310 | 16INT8 TOPS and 16 hardware-decode channels | Decode capacity not 16 streams of a particular model; exact Russian SKU/PN to verify. F071/S097; [doc](https://support.huaweicloud.com/intl/en-us/adevg-atlas500app/atlas500development_01_0006.html) |
| NM Quad | Manual 28.02.2025: typical 50/max 75 W with ventilation conditions | Do not mix other older card values/versions; model/PPE sizing U. F072/S098; [manual](https://www.module.ru/uploads/products/re-nmquad-f04d0c8979.pdf) |
| Jetson historical MSRP | USD 249 developer kit 17.12.2024 | Not Russian 2026 system cost; sparse TOPS not directly comparable to LinQ INT8. F070/S096; [announcement](https://developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/) |

INF proposed E001/E003/F177 sizing: include decode/copy/all models/tracking/events/delivery/review/archive in declared mode. Record source/analytic FPS, dropped frames/queues, end-to-end p 50/p 95/p 99, CPU/RAM/accelerator/temperature/version; AC idle/mean/peak only with meter. Increase cameras to agreed quality/latency boundary with explicitly justified reserve (reserve amount U). One model success does not establish 9 PPE channels; RTX/CPU success does not prove LinQ execution. SDK download requiring registration/verification is not a received team SDK (Q002).

### Registry layers: chip, board, SDK and sold system are separate objects

DOC/OBS F017/F137–F142/F181, S165–S184; direct current extracts often inaccessible. Catalog product-ID is **not** registry number; status/certification cannot be inherited across layers.

| Layer | Found evidence | Boundary / missing proof |
|---|---|---|
| LinQ H / К1945ВМ3Я chip | GISP product-ID **4767267**; Technopolis catalog links names; secondary №**10675504**, document 22.08.2025 through 31.12.2028, ООО «ХайТэк» | Current official extract U; not whole-node registry proof |
| LinQ HPQ board | Primary inclusion announcement; GISP product-ID **4781119** | Official number/validity/points unread; secondary IVA HPD1M-11 №**10785804**04.03.2026–03.03.2031 not proven identical to HPQ |
| IVA H1 framework/SDK | ARPP catalog+official index №**32778**, 31.03.2026, ООО «ХайТэк», class 04.03 SDK | Direct current card inaccessible; runtime/build/application coverage not inherited; do not confuse with IVA CV |
| HPS/HPC/AQserv complete system | Specs/partnership claims | Registry entry for entire sold configuration/BOM U; OS/server certification not whole HSE ПАК |
| VizorLabs H&S | №**10990**, 09.07.2021, ООО «ВизорЛабс» | Old product, not automatic 4.0 coverage |
| VizorLabs Platform 4.0 | №**33642**, 21.05.2026, ООО «Лаборатория промышленного интеллекта» | Direct current card/rights transfer history/seller authority U, same brand insufficient |
| IVA CV platform | Vendor registry claim №**7272**, 03.11.2020 | Current official card/new ПАК coverage U; not software-registration certificate**2019618023** or H1№32778 |

[H1 ARPP](https://catalog.arppsoft.ru/product/6475487), [old H&S](https://catalog.arppsoft.ru/product/6078544), [Platform 4.0](https://catalog.arppsoft.ru/product/6484481), [LinQ technical page](https://lin-q.ru/tech), [HPQ GISP](https://gisp.gov.ru/goods/#/product/4781119), [secondary chip](https://torgs.ru/industrial-products/417709/), [secondary HPD1M-11](https://torgs.ru/industrial-products/510834/).

Defensible current 'why LinQ': mandatory case condition, Russian hardware ecosystem and opportunity to validate a specific supply for target environment. Lower total cost/power, unlimited supply, no sanctions risk or automatic CII approval are **not demonstrated**. Business advantage needs equal workload/quality plus complete dated quote. IVA CV's LinQ offer refutes novelty and may motivate comparison/cooperation; corporate independence from setter remains U (Q003/Q007/Q010).

## A10 — Moscow: nonfinancial pilot, grant and purchase require separate decisions

There is a documented route, but no guaranteed individual subsidy, open October intake or purchase. LAW-O/DOC F157–F167/F184: 2474-ПП14.09.2026 fully read in official «Вестник Москвы»№52, printed pp.6–8/PDF7–9. Effective date 14.09.2026 found in GARANT index; no separate commencement clause in read act, official-publication chain not fully independently confirmed. [Official issue](https://vestnikmoscow.mos.ru/wp-content/uploads/2026/09/zhurnal-vestnik-moskvy-%E2%84%96-52.pdf), [reference card](https://base.garant.ru/414946382/) (S197/S079). Old information PDFs must not silently override amendments. Q011/Q021/Q023.

### 631-ПП nonfinancial testing: applicant, rights, site and agreement

F158/S197–S198/S075: applicant is legal entity or individual entrepreneur, not simply five individuals; GISP describes MVP/ready solution. New§4.3 requires exclusive ownership **or use under an exclusive license** of at least one relevant **Rospatent-registered IP result (РИД)**: computer program, invention, utility model or industrial design. General 'lawful use' no longer enough. Licenses for licensed activity and absence of liquidation/bankruptcy/suspension remain. [Base 631-ПП](https://www.mos.ru/upload/content/files/2b552d79304ffcce8e7c77de6d655d8f/0Post.pdf), [GISP measure](https://gisp.gov.ru/nmp/measure/12449148).

F159/S197–S199:§5 participant status requires agreement with registered site and MIC Foundation (or with Foundation for its own test). Agreement establishes methodology, schedule, organization/report form. Achieved criteria can lead to solution registry entry, not duty to buy. New§§9–10 link site status to registry after cooperation agreement and require evaluation/report/recommendations. GISP01.01.2025–25.12.2026 period is **nonfinancial measure period**, not grant window. [537-ПП amendment](https://www.mos.ru/upload/documents/files/8910/537-PP.pdf).

F056/F159/S080/S206: February official site registry includes ВНИИЖТ, МЗТА, ПАО «Калибр», АО НТЦ «Модуль», ОЭЗ «Технополис Москва». Later order 30.09.2026 №П-18-12-215/26 found only in reference system; current primary full list U. Names are route candidates, not demonstrated HSE demand/cameras/budget. [February registry](https://www.mos.ru/upload/documents/files/6526/20_02_2026_P_18_12_29_26_Avdeeva_A_I_Avdeeva_A_I__removed.pdf).

CC F057/S081: ВНИИЖТ reports agreement 29.09.2026 with MIC/«Роботехникс» and **planned** demolition-robot test on Shcherbinka Experimental Ring. Concrete agreement/future-test example, not completed test/payment/PPE demand or identified hackathon-winner outcome. [ВНИИЖТ](https://vniizht.ru/news/robotizatsiya-infrastruktury-v-moskve-protestiruyut-innovatsionnogo-demontazhnogo-robot/).

### 410-ПП grant after 2474-ПП: direct staffing gates repealed, other gates remain

F160/S197/S200: **direct** appendix§§1.2.12/1.2.13 (minimum 5 employees and no >20% headcount drop) repealed. Do not repeat them as current direct admission gates. Registration age ≥ 12 months and salary condition remain with Startup/High-Tech Company Registry exceptions; amended reference concerns these two points. MIC and pilot participant statuses, no duplicate financing and other unrepealed conditions remain. Added checks include impending EGRUL/EGRIP exclusion, 223-ФЗ bad-supplier registry, UN Security Council lists and overdue Moscow debt. [Base 410-ПП](https://www.mos.ru/upload/documents/files/9314/PostanovleniePravitelstvaMoskviot22032022410-PP.pdf).

F161/S197§2.6: **grant-eligible** site narrower than general testing registry. Test in Moscow in Foundation or status site of specified types: Moscow public institution/unitary enterprise; company Moscow owns >50%; city-created NPO; federal institution/unitary enterprise (ФГУП); Skolkovo Foundation or entity it directly owns ≥ 50%. Site must not be founder/shareholder of applicant; risk acceptable. Private LLC on broad registry not automatically eligible for grant.

| Grant branch | Ceiling / required rights |
|---|---|
| Computer program | Up to **RUB 2m**, MIC participant owns exclusive right to relevant Rospatent-registered software |
| Patent IP older than 12 months | Up to **RUB 2m**, exclusive right to invention/utility model/industrial design registered **more than 12 months** before application |
| Fresh patent IP younger than 12 months | Up to **RUB 4m**, corresponding exclusive right **plus industry/interindustry cluster participation** |
| Cross-cutting caps | Up to **RUB 1m per expense direction**, **RUB 4m per participant per financial year**; outside Startup Registry additionally ≤ 50% prior-year taxes/fees paid to Moscow budget excluding personal-income tax as tax agent |

F162/S197§2.13/new§§2.2.1–2.2.2. Ceilings are not awards; amount depends on approved estimate. 'More than 12 months' wording pertains to patent IP, not automatic age gate for software certificate; exactly 12 months boundary requires clarification. Exclusive license sufficient for nonfinancial route is not exclusive ownership required by money branch. Rospatent registration and MinDigital software registry are distinct.

F163/S197/S199/S200: eligible directions include delivery/assembly/disassembly/commissioning, site adaptation/restoration, consumables/components/spares, maintenance/repair, auxiliary-equipment rent, payroll, measurement/testing, insurance; amendment adds spares/refines periods. Certification/registration/clinical testing is a separate pre-application branch from 1 January preceding year. Named personal-income tax/contributions excluded from payroll reimbursement. Not permission to buy all equipment or fund whole development. Conditional **50% advance**, balance after approved report/expense confirmation; deadlines contractual. Advance not unconditional funding; 'reimbursement' not necessarily postpayment-only.

### Intake and April resource scoring are different from direct staffing admission

LAW-O/DOC F164/S201: Foundation order№П-02-ПТ-16/26 of 06.04.2026 confirms spring application **15.04.2026 09:00–01.06.2026 18:00 Moscow**; only pp.1–4 of 30-page file visually read. Window closed, program not thereby nonexistent. After 2474 announcement must give budget/dates/expense periods/documents/review terms, publish ≥ 5 business days ahead; intake ≥ 40 calendar days with early termination for insufficient remaining funds. October/next window U. [Spring order](https://gisp.gov.ru/nmp/upload/docs/7dd7592238429eb2c5dc9618f8f45540c2fc6aa88544674ad53f27ab0aaa7d9b.pdf).

F165/S202: fully visually read risk order№П-01-ОД-23/26 of 20.04.2026 requires **total ≥ 5/11 and each of four criteria ≥ 1**. TRL 1–5→0, TRL 6→1, 7→2, 8→3, 9→4. Thus an MVP eligible for nonfinancial testing does not necessarily pass grant risk filter. Resource subcriteria include documented revenue ≥ RUB 1m; headcount (startup legal entity ≥ 1, other legal entity ≥ 5, entrepreneur automatically 1 point); small technology company (МТК) registry; also rights/permits and reputation. MinDigital software registry for software developer is a separate subcriterion. [Risk order](https://gisp.gov.ru/nmp/upload/docs/5d78d92ca2c61258b40b399cd551f6351a98f6b911a95fc41c79d7bf63d672b4.pdf).

Repeal of direct staffing gates does **not automatically repeal a separate April resource subcriterion**. Post-September scoring update not found; neither current October applicability nor automatic repeal is established. Need actual call, risk edition, eligible site/rights and individual determination. Baseline grant=0.

### Past hackathon winners and program outcomes

DOC F166/S203–S204: official industrial portal 23.10.2025 lists SummitTeam (SEZ HR platform), «Хайлоджикс» (ТТР) and Digital Rover (Excel→web); describes 2025 as first hackathon. Targeted name+pilot/testing/deployment searches did not establish signed pilot, act, live customer product or purchase. This is **U**, not proof of no implementation. [Official release](https://prommoscow.info/news/hackathon-moscow-practical-tasks).

Department-reported program accounting F167/S205 pp.3–4:2022–2024 approved 299 pilots for 287 companies; by 28.04.2025 implemented 85 solutions (28%). This is broad program administrative accounting, not independent HSE evidence, winner conversion or our success probability. [Expert conclusion](https://www.mos.ru/upload/documents/files/373/Zakluchenie410-PP.pdf).

Proposed route: establish applicant/IP chain → with HighTech find site/risk owner → qualify cameras/data/response → verify current site/program → agree methodology/schedule/report → separately apply for grant if current eligible call exists → measure pilot → independently procure/accept operations/support. Rights/access/contracts/money can take unknown time; proposed evaluation weeks do not include them.

## A11 — Pilot evaluation: quality, response, exposure and money

This is **a proposed procedure**, not performed acceptance, Moscow-program timing or organizer requirements. INF/ASSUME F156/F176–F178/E001–E008. Agree numerical gates with risk owner. A working bounding-box demo tests only part of the value chain.

### Scene, permissions and event definition before evaluation clock

Fix site/work/PPE obligation/observable geometry; event start/end/minimum duration/separation/debounce/deduplication and unassessable case. Absence of helmet in permitted nonmandatory zone differs from absence in mandatory danger zone. Respirator visibility does not prove seal/filter class/fit-test. Smoking needs positive and difficult negative episodes (food/phone/hand near face); such data U. No automatic promise of vapes/all angles.

Camera passport: owner/access, position/height, PPE/object pixels, codec/resolution/FPS/bitrate, day/night/sun/weather where relevant, occlusion/moving machinery. Do not silently exclude mandatory bad-view zones. Correct them with cost or report stop/limitation. Check observability/modification rights before retraining. Lawful data/recipient/country/retention/deletion precede sending real video; performance testing does not authorize transfer.

Appoint shift responder, backup, confirmer and escalation. Event card must lead to authorized action: warn, inspect, stop specified work under responsible person's powers, fix cause or reject error. Ordinary video demo does not establish safety-certified automatic equipment stopping. No feasible response means observation, not completed prevention.

### Baseline and frozen independent test

Proposed organizational start **after data/permissions**:1week survey, 2 weeks baseline, 2–4 weeks frozen evaluation. Access/development/procurement separate; not regulatory/program deadline. Extend for rare events; calendar end does not create sample size.

Measure actual current control/coverage/labor and random ordinary video, not hypothetical staff work. Shadow mode can tune; causal before/after requires a stable measurement instrument and parallel independent review. Split tuning/test by days/shifts/cameras; adjacent frames of one episode not independent examples. Freeze model/weights/export/quantization/runtime/thresholds; documented changes create new stage/reacceptance. Two experts resolve ambiguous episodes and preserve disagreement/reason logs.

Sample **non-alert video randomly**. Alert-only review estimates precision, cannot recover recall/missed events. Unobservable/unassessable episodes separate from both success and failure; do not expand exclusions to improve numbers.

| Layer | Measurement and denominator | Interpretation |
|---|---|---|
| Observability | Available/suitable camera-hours, mandatory-zone coverage, unassessable share | Healthy server with blocked camera not successful control |
| Events | Per required PPE/condition TP/FP/FN; `precision=TP/(TP+FP)`; `recall=TP/(TP+FN)` with uncertainty intervals, predefined event matching | Average must not conceal night/respirator/camera failure |
| Alert load | FP/camera-hour or 100 camera-hours; duplicates/episode; alerts/shift; review minutes | Repeated frames not independent successes; precision not workload |
| Latency/reliability | Physical onset→available notification p 50/p 95, p 99 if needed; model/queue/delivery separate; outage/recovery | Model latency not useful-action latency |
| Response | Confirmation/action/remediation times; closure share/reasons | Card is not prevented injury |
| Exposure | Independently confirmed violations per person-hours in applicability; dangerous-exposure duration; vehicle operations/crossings when relevant | Less work/headcount not safety improvement; camera-hours and person-hours not interchangeable |
| Labor/cost | Previous displaced H, new H_ai, engineering hours/support, q from budget facts, full dated quotes | Freed salaried capacity not automatic cash; no double labor |

`r=confirmed violations/exposure_person_hours*1000`; select 100/1000scale beforehand. For PPE fraction use violating episodes/eligible person episodes under PPE obligation. Also keep duration: many short episodes and one long event differ.

### Causal comparison and decision gates

Use comparable zones/shifts and repeated before/after measures. If permissible without weakening mandatory controls, phase notifications across zones; never create hazards or disable required safety. Log training/production/contractor/shift/manager/light/equipment changes and observation/Hawthorne conditions. Proposed difference-in-differences:

```text
D = (r_pilot_after-r_pilot_before) - (r_control_after-r_control_before)
```

Negative D is greater pilot reduction **conditional on comparable trends**; justify/check them and account for dependence within day/shift clusters. Without control label as before/after observation, not causal effect. STUDY/DOC F176/S050: NIOSH guide discusses controls/repeated measurements/phased implementation, selection/contamination/observed-group responses. OSHA leading-indicator page only indexed auxiliary lead. [NIOSH guide](https://www.cdc.gov/niosh/docs/2001-119/pdfs/2001-119.pdf).

Short pilot cannot establish rare injury/LTIFR reduction; 'no injuries this month' without sufficient exposure weak. Unsafe action not automatically classified near-miss without agreed taxonomy. Keep long-term injury indicators separately.

**Proposed starting gates**, not industry standard/ШСУ/hackathon mandate: availability ≥ 95% of agreed hours, event precision ≥ 90% and recall ≥ 85% **for each required PPE** with sufficient independent sample; no unagreed exclusion of required zones. Small n→insufficient data/extend, not automatic go. Agree workload/p 95 with responder capacity. Technical go covers frozen applicability/quality/reliability; operational go needs feasible actual response/workload; financial go needs observed H/H_ai/q, complete P/L/work/support quote, agreed horizon and NPV ≥ 0 with stresses. Negative ROI can be accepted only under explicitly different safety-value criterion.

Stop/redesign: systematic FN in mandatory scene, irrecoverable view, missing rights/access/responder, intolerable load, hidden fallback or excess budget. Lowering sensitivity, discarding hard cameras or inventing prevented-injury income is not remediation. Reevaluate changed scene/model.

Retain lawful inputs/hashes, scene/version passports, split/labels/disagreements, **all predictions and non-alert sample**, raw timestamps, response/change logs, availability/drops, resource/AC profile if measured, labor/dates/taxes/quotes/model assumptions/results, go/rework/stop and signed limitations. Reproducibility does not justify indefinite PD storage.

## A12 — Defensible differentiation and prototype falsification

Generic PPE/edge/privacy/temporal rules/review/adaptation/measurability/setup and **LinQ PPE** are not established advantages. Documentation suffices to refute general feature novelty; superiority requires same inputs/metrics/edition/starting infrastructure and an actual comparison. No row below is a completed result. INF F104/F112/F168–F175/F183/E006.

| Value hypothesis / need | Closest alternative | What a narrow prototype could establish | Falsifier / limit |
|---|---|---|---|
| Fit installed video environment | Suitable Macroscop/TRASSIR add-on | One input→event→clip/review→test recipient path, documented format/resources | Existing module same result at lower incremental cost removes detector advantage; test recipient not production customer connector |
| Small PPE/respirator on supplied video | Macroscop/VizorLabs respirator; camera reposition/ROI | Event TP/FP/FN by size/occlusion, FP/camera-hour/p 95 and unusable scenes | If camera correction solves it, do not attribute to model; no independent test or equal/better module means advantage U; no seal/filter/fit-test proof |
| Smoking in required zone | VizorLabs/IVA CV already claim smoking | With data/supported export: positives/hard negatives, temporal rule/duplicates/errors | No resolvable action/object/sample/mandatory case requirement→withdraw; vapes/all views not automatic |
| Complete local cycle | VisionAI Box, VizorLabs dedicated, IVA CV edge | If local configuration available, disconnect internet and test inference/review/journal/observed egress | Remote hackathon LinQ not on-prem; one offline run not lifetime activation/update/security/legal proof; no isolation need→no standalone value claim |
| Real LinQ execution | IVA CV explicit LinQ/demo | Actual SDK/runtime/model hashes, compile/run logs, host/accelerator boundary, full throughput/latency/load | **General novelty already refuted**; CPU/GPU fallback not mandatory LinQ success; model FPS not camera sizing |
| Fewer redundant alerts/easier action | VMS journals, VizorLabs review, Protex dwell/suppression | Same episodes: duplicate/FP rate, review minutes, human decision and misses outside alerts | Suppression hiding distinct events or equal competitor removes claim; fewer alerts≠safer; video evidence not neural-network internal explanation |
| Faster reproducible setup | Working VMS base, transferable Macroscop key, VisionAI Enterprise | Clean documented start→first valid event, steps/versions/config export/labor | Prepared own system versus fresh competitor unfair; without same start only own elapsed time known; transfer rights distinct from technical export |
| Lower cost/energy | Incremental VMS, ready ПАК, corrected camera/equal node | Resource/BOM list, measured wall power only with meter, normalized quote/TCO sensitivities | No equal kit/term/tax/support/quality→withdraw 'cheaper'; TOPS/board watts/T4 price not LinQ TCO |

Within 45 hours after full case, choose one mandatory observable scene/minimum connected set, execute on supplied LinQ and retain reproducible error-aware evaluation. That can establish a scoped hackathon result, not cross-factory universality, annual SLA, causal injury reduction, complete registries, serial supply or monetary payback. After testing, state 'on this version/scene/test, these P/R/FP/p 95 and response boundaries'; add comparative superiority only after equal test. One undefined '99% accuracy' is insufficient.

## E001–E008 — Proposed checks, required artifacts and decision consequences

All are **unperformed proposals**. The only executed computation in this research was D's model arithmetic. Full procedural records and Q/K links are in [OPEN_QUESTIONS](OPEN_QUESTIONS.md); the following retains each check's decision, inputs, procedure, output and success limit.

| Check | Inputs and procedure | Evidence / decision / limit |
|---|---|---|
| E001 case/artifact/device passport | Full case, actual device/SDK/compiler/runtime, authorized test data and documented logging; save versions/hashes, read supplied example, map host↔accelerator/fallback/roles/countries, run minimal permitted nonindustrial example | Operator/format support, errors, compile/run/version/profile logs, model hash and command **from supplied docs**. Success→E003/E004; failure→supported export/model or setter clarification. Does not prove PPE quality, camera count or authority for other video. Q001/Q002/Q004 |
| E002 camera suitability | Authorized day/night fragments, scene/PPE passport, settings access, safety expert; label visibility/occlusion/object pixels/hard negatives; compare same episodes before/after permitted ROI/light/angle correction without creating danger | Eligible hours/episodes, missed-cause labels, installation hours/cost, lawful clips/settings. Irrecoverable→redesign/stop; correctable→fix imagery before model; suitable→E004. One camera not universal/free reuse. Q017/Q016/Q003 |
| E003 LinQ end-to-end sizing/energy | Actual hardware/SDK and permitted codec/resolution/FPS/bitrate streams; fixed models/INT8/thresholds, meter if measuring power; increase streams including decode/copy/tracking/events/review/archive, test overload/outage/recovery | Source/analytic FPS, loss/queues, p 50/p 95/p 99, CPU/RAM/accelerator/temp/AC idle/mean/peak, raw timing/version/config/input profile. Bad fallback/latency→reduce load or recount nodes. No annual SLA/price/superiority from one success. Q002/Q003/Q024 |
| E004 frozen event quality | Agreed event/applicability and independent day/shift/camera split, non-alert sample; tune separately, freeze versions/thresholds, two-expert disputed labels; count TP/FP/FN/unassessable | Per-PPE/condition P/R+intervals, FP/camera-hour/shift, duplicates/duration/p 95/exposure; preserve predictions/labels/disagreements. Small n→insufficient data; systematic FN→stop. Proposed 90/85/95 gates not external standard; no fit-test/risk removal/superiority inferred. Q001/Q016/Q017 |
| E005 operational/business pilot | Site/permissions/responder, actual baseline work/labor, independent events and comparable control where feasible; proposed 1week survey+2baseline+2–4frozen evaluation, extend if rare; retain mandatory safety/log concurrent changes and compare trends | Confirmed violations/person-hours, response/remediation/closure, old/new hours, q from actually avoided pay/contract/overtime/hire. Keep all alerts/random non-alerts. No response/overload/unequal coverage→rework/stop. Before/after alone not causality; short pilot not LTIFR proof. Q012/Q013/Q015/Q016 |
| E006 normalized alternatives | Legal access to exact alternatives, same scenes/labels/gates/start, dated quotes/BOM/term/tax/support; compare installed-VMS add-on, camera correction, ready local/IVA CV and own solution | P/R/FP/hour/p 95/workload, first-valid-event time, rights/integration and full incremental TCO. Preserve versions/quotes/logs/boundary; unavailable alternative stays untested. Equal/better cheaper module→withdraw advantage/consider integration. Scene win not general novelty/universality. Q007/Q009/Q010/Q019 |
| E007 data route/isolation/deletion | Recipient/country/purpose/basis map, synthetic marked frames, config/traffic/log/backup access, security/legal; trace camera→buffer→LinQ→event→journal→archive/export/train, activation/support/failure/cache/telemetry; delete agreed copies, check roles; offline only for declared local mode | Recipients/copies/geography/access/deletion, traffic/config/trace/act and inaccessible-copy residuals. Unapproved transfer→stop/change inputs. Technical success not legal opinion/certification/absolute absence of copies or reidentification. Q004/Q005/Q006/Q020/Q021/Q022 |
| E008 local economics/stresses | Actual P/L/work/support quotes, sizing/AC/H/H_ai/q, taxes/term/residual/rate/horizon; reproduce assumed model then separately replace with sourced local inputs, equal incremental/new boundary | TCO/NPV/affordable P+L/break-even H, cash versus capacity separately; retain dated inputs/model/results. Stress q 0/bad cameras/alert load/SLA/recurring L/nodes/archive/grant 0; all new AI labor in O, no double subtraction. Negative NPV may support explicitly noncash safety purchase, never cash payback. Positive local model not market forecast/prevented injuries/grant guarantee. Q003/Q009/Q011/Q015/Q024 |

## Q001–Q024 — Unknowns, priorities and authoritative next channels

P0 implementation: **Q001/Q002/Q004**. P0 commercial pilot: **Q003/Q012/Q016**. Check Q017 before promising retraining. These questions localize absent facts; they did not prevent completing this documentary report. No external requests, interviews, quote solicitations or applications were sent.

| ID / priority | Exact unresolved decision input | Next artifact/channel |
|---|---|---|
| Q001 P0 | Full mandatory scenarios/PPE/zones/inputs/event rules/interfaces/metrics and dataset rights, not announcement examples | Setter's versioned full case/files; E001/E004 |
| Q002 P0 | Supplied SKU/revision/OS/SDK/compiler/runtime, supported operators, access limits and actual LinQ execution | Setter's artifacts/device/logging; E001/E003 |
| Q003 P0 | Full node and rights/BOM quote, VAT/validity/payment/delivery/stock/warranty/SLA/spares/real AC; HPS 1150/1500 modes | HighTech/integrator written SKU-host-decode-memory-cooling-OS-VMS-rights terms; E003/E008 |
| Q004 P0 | Real data recipients/controllers/processors, subjects/citizenship, countries/databases at collection/later stages, caches/backups/support and authority | Setter+enterprise+legal/security map/instruction/agreement; E007 |
| Q005 P1 | Official 265-ФЗ/220 originals/current consolidated norms, later changes and effective provenance | Official artifact/site counsel verification; mirrors already read, no invented original access |
| Q006 P1 | Customer 44/223/private status, actual CII boundaries/category/sector, consolidated 360-р after 1237-р, procurement subject/OKPD2 | Site security/procurement categorization/specification/current list; E007 |
| Q007 P1 | Current precise chip/board/full-system/H1-runtime-app/alternative registry extracts and seller authority, HPQ versus HPD1M-11 mapping | Vendor/customer extracts, SKU↔design-doc↔BOM/software scope; E006 |
| Q008 P1 | Primary Rosseti/Salavatsteklo/RT-Engineering task/protocol/contract/acts, ШСУ/NTEK fulfillment/currency and cancellation reason | Customer/platform primary bundles; do not infer from aggregator status |
| Q009 P1 | Equal-result VMS/PPE/LinQ quote: edition/rights/tax/term/transfer/updates/hardware/work/support | Comparable vendor quotes/licenses; DSSL XLSX cells still unread; E006/E008 |
| Q010 P1 | IVA CV demo's LinQ/SDK/model/build/rights, actual serial product, exact respirator/smoking package, HighTech relationship | Cognitive Solutions/HighTech build/demo/contract/quote artifacts; E006; novelty already refuted |
| Q011 P1 | Current Moscow call/budget/window, post-September risk scoring/site list and 2474 official commencement chain | MIC Foundation/applicant current announcement/orders/agreement/estimate; baseline grant 0 |
| Q012 P0 | Named HighTech HSE clients/pilots/target segment, survey/pilot/rollout budget owner, risk owner/integrator/acceptor/support | Setter/customer-specific authority, CAPEX/OPEX limits and commercial roles; E005/E008 |
| Q013 P2 | Causal AI effect with exposure/stable detector/control; documented no-rollout/PPE litigation or failure | Customer raw protocol/primary procurement/court outcome; E005; difficulty/self-report not failure frequency |
| Q014 P2 | Moscow-city/sector primary statistics, current 7-травматизм instructions/type-code decoding, site injury history/exposure | Rosstat/Mosstat official artifacts and enterprise; XLSX origin still U, 64507 is Oblast |
| Q015 P1 | Equal-coverage displaced H, cash-realizable q, new labor/support, local loss/tariff/counterfactual SFR discount and buying criterion | Customer finance/actual labor-pay-contract facts/quotes; E005/E008 |
| Q016 P0 | Confirm/close actor/action/capacity, P/R/FP/latency/availability gates and sufficiently independent sample | Setter/OT/label expert's scene passport and ПМИ; E004/E005; proposed gates not standards |
| Q017 P1 | Actual PPE/action visibility by view/shift/light/occlusion, camera/light/mount correction rights/cost | Real permitted video/site survey; E002 before adaptation claim |
| Q018 P2 | Narrow HSE TAM method and reachable sites with demand/cameras/price/authority/budget | Targeted method artifact plus bottom-up segment interviews after Q012; broad abstracts not SAM |
| Q019 P2 | Close alternatives' current editions/holders/RF delivery/service/revenue/headcount/exact clients; Eocortex/ISS gaps | Vendor/public registry artifacts, deepen only decision-changing comparator |
| Q020 P1 | Admissibility/sufficiency of specific lawful employment recording, duty/fault/timing/procedure and criminal question if needed | Employer legal/HR actual bundle/full judgments; score not guilt, human not cure for unlawful video |
| Q021 P1 | Code/weights/labels/video ownership and training/demo/distribution rights, H1 license, sufficient IP for pilot/grant | Setter/rights-holder/team/site license/agreement chain; exclusive license≠exclusive ownership |
| Q022 P1 | Verified deletion across copies/buffers/logs/backups and actual egress/activation/update/support behavior | Security/device traces/config/deletion act with residual copies; E007; blur/local/videoless not proof |
| Q023 P2 | Signed pilots/tests/acts/purchases of 2025 winners and individual support outcome | Winner/customer/Foundation dated agreement/act/procurement, not general 299/85program statistics |
| Q024 P1 | Camera/VMS/OS/model/LinQ maintenance/update/reacceptance/repair/rollback/spares and sizing reserve | Integrator/operations/HighTech RACI/SLA/version control; E003/E004/E008 |

## Handoffs to neighboring research topics

No neighboring reports were available/received; their existence/content is not assumed. These are prepared file-based handoffs, not messages to other chats/people or authorization to start their research.

| Topic | Finding and changed decision | Evidence / unresolved |
|---|---|---|
| `linq_platform` | Actual SKU/SDK/runtime/operators and inference proof; OEM rights/full BOM, registry layers, HPS 1150/1500 | F062–F065/F137–F148/F181; Q002/Q003/Q007; E001/E003 |
| `model_stack` | Vendor model FPS≠PPE pipeline; IVA CV support≠our export compatibility; verify INT8 and fallback on supplied build | F065/F171–F173; Q002; E001/E004 |
| `violation_methods` | Respirator/smoking/context already marketed; full case+observability select events; ШСУ helmet/vest/shoes not complete hackathon list | F005–F006/F013/F114/F183; Q001/Q017 |
| `evaluation` | Event TP/FP/FN, non-alert sampling, camera/shift splits, frozen versions, unassessability, FP/hour, full p 95; small n not go | F156/F176; Q016; E004/E005; vendor 95–99% not comparable standard |
| `video_architecture` | Include decode/copy/CPU/queue/archive/AC; healthy video can hide analytic drops;50 days/UPS 1 h is one design; remote LinQ needs recipient/country map | F075–F076/F115/F133/F136/F177–F178/F181; Q003/Q004/Q006/Q022/Q024 |
| `operator_product` | Event→confirmation→action, responder capacity/correction/appeal; no automatic sanction; Parsec only server-room door | F024/F128/F156/F184; Q012/Q016/Q020; E005 |
| `datasets`, `training_strategy` | Separate training authority/PD purposes/code-data-model rights; moving equipment hard negatives; geometry before retraining | F080/F121/F149/F178; Q017/Q021; E002/E004; no new dataset produced |
| `hackathon_strategy` | No 'first PPE on LinQ', 'cheaper than GPU', causal injury reduction or payback without evidence; use scoped measured result/errors/conditional economics/pilot path | F059–F060/F171–F175/F182–F183; Q001/Q003/Q010/Q016; win≠grant/purchase |

Immediate sequence after full case: archive case/rights/versions → E001 permitted minimum on actual LinQ and host/fallback boundary → E002 visibility → E003 full load → E004 frozen events → E007 data trace. Unsupported export, unobservable PPE or unauthorized recipient changes implementation; never conceal fallback. Commercial follow-up packages scene/errors/versions/load, data map, proposed criteria/times, response roles and full quote request. At site run E005/E006/E008; separately establish applicant/IP/MIC/site/current support eligibility. Positive pilot still needs purchase, operational acceptance and support contract.
