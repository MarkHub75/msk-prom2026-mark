---
topic: datasets
scope: >-
  Two-wave investigation of primary PPE, helmet/head/person, smoking, factory-video,
  action and auxiliary datasets: exact artifacts, acquisition, annotation semantics,
  geometry, coverage, provenance, rights layers, splits, independence, scale,
  conditional roles and a reproducible next practical programme.
not_covered:
  - "Final mandatory taxonomy, organizer data and target-camera distributions: unavailable in the research snapshot."
  - "Model/weight selection, loaders and export implementation: model_stack."
  - "Training and partial-label loss implementation: training_strategy."
  - "Violation inference, person-item association and temporal policy implementation: violation_methods."
  - "Full evaluation methodology, model accuracy and operational false-alert measurements: evaluation."
  - "LinQ configuration, SDK, verified execution, throughput and latency: linq_platform/video_architecture."
  - "General legal clearance, NC prize-hackathon interpretation and SA/AGPL effects on weights: unresolved action-specific questions."
answers:
  - "Which datasets should be acquired first, and for which conditional train/adapt/donor/replay/calibration/holdout/demo roles?"
  - "What exact versions, download routes and payload layers were actually obtained?"
  - "What are the exact source class maps and object/head/torso/person/image/clip supervision units?"
  - "What did the SH17 raw-to-release comparison establish, and what does on/off mean?"
  - "How do SFCHD media membership, COCO/YOLO geometry, validation protocols and inferred groups differ?"
  - "What do SHEL5K extra person labels, CPPE media exceptions and Construction-PPE no_* labels permit?"
  - "Can available mask and smoking data supervise industrial respirator removal and smoking near flammables?"
  - "What real video, timing and event ground truth exist, and what remains missing?"
  - "Which rights apply to code, annotations, photos/video, assemblies, articles and redistribution?"
  - "Which dataset lineages prevent an independent cross-dataset test, and how should partial labels and groups be handled?"
  - "What do measured donor object sizes imply for target preprocessing, without claiming model or LinQ performance?"
  - "How should organizer data, locked holdout, reversible mappings and provenance manifests be prepared?"
  - "Which Q001-Q020 unknowns and proposed E001-E018 checks should drive the next practical work?"
  - "Which findings must be passed to model_stack, violation_methods, training_strategy, evaluation and other topics?"
keywords:
  - PPE
  - CCTV
  - SH17
  - SFCHD
  - SCALE
  - SHWD
  - SHD
  - SHEL5K
  - CHV
  - GDUT-HWD
  - CPPE-5
  - respirator
  - smoking
  - Smoker Detection Dataset
  - Onal
  - "Önal/Dandıl"
  - SARD
  - PhysicalAI-Event-Videos
  - Pictor-PPE
  - Construction-PPE
  - SODA
  - partial labels
  - unknown
  - lineage
  - locked holdout
  - manifest
  - LinQ
entity_schema:
  dataset_selection_record:
    representation: "Rows of the Dataset acquisition and role catalogue table."
    fields:
      dataset: string
      artifact: string
      actual_access: string
      conditional_role: string
      remaining_gates: string
      facts: "list of F-ID links within the cell"
  mapping_record:
    representation: "Rows of the Preliminary class mapping table; target names are concepts, not assigned numeric IDs."
    fields:
      source_literal: string
      semantic_unit: string
      preliminary_target: string
      relation: "conditional | partial | incompatible | not_annotated"
      condition: string
      facts: "list of F-ID links within the cell"
  lineage_record:
    representation: "Rows of the Dataset lineage and independence table."
    fields:
      parent: string
      derivative: string
      established_relation: string
      independence_consequence: string
      unresolved: string
      facts: "list of F-ID links within the cell"
  video_probe_record:
    representation: "Rows of the Önal timing table; all eight clips H.264 1920x1080."
    fields:
      clip: string
      bytes: integer
      duration_s: number
      start_s: number
      displayed_fps: number
      tbn: integer
  scale_record:
    representation: "Rows of the donor min-axis quantile table; continuous hypothetical letterbox 640 in declared frames."
    fields:
      scope_class: string
      n_objects: integer
      native_q10_q50_q90_px: "three numbers separated by /"
      letterbox640_q10_q50_q90_px: "three numbers separated by /"
takeaways:
  - "Organizer intake and a locked target holdout precede external mixing; final case/taxonomy/media/LinQ input were unavailable."
  - "SFCHD is a leading factory-adaptation candidate, conditionally on rights and grouping: full COCO 12,373 records/50,559 boxes; archive intersection 12,372 media names/50,552 boxes."
  - "SH17 exact Kaggle v1 is a broad object/body-part donor. Thirteen released YOLO files/228 annotation boxes matched mapped raw; thirteen raw/current-Pexels visual samples are a separate scope; only 13376117 has an exact released JPEG."
  - "Eight obtained Önal MP4 support replay/manual event pilots; 691 selected clips are not 4,000 public raw hours or a continuous safe-period denominator."
  - "Missing annotations, invisibility, object off, person absence and policy violation are distinct. Masks are not an exact industrial-respirator taxonomy."
  - "Parent/derivative datasets and crops cannot form independent train/test evidence; supplied group IDs remain nullable and inferred groups retain evidence."
  - "E001-E018 are proposed programmes; E019-E033 are completed bounded checks. No training, model accuracy, CCTV transfer or LinQ performance was measured."
checked_at: "2026-10-23T08:31:50.417165+03:00"
timezone: Europe/Moscow
context_version: mosprom-research-v1
research_snapshot:
  source_access_date: "2026-10-23"
  collector_freeze_at: "2026-10-23T07:37:53.376622+03:00"
  version: datasets-collector-freeze-2026-10-23
  publication_dates: "Source-specific; see SOURCES.md. Access, publication, capture and generation dates are distinct."
case_material_state:
  available: "Provided general/thematic prompts and public short case description."
  unavailable: "Full case; organizer media/labels/terms; final taxonomy/metrics; exact LinQ device/SDK/input/preprocessing contract."
actual_checks:
  research: "Two waves; bounded artifact/metadata/annotation/visual checks E019-E033, itemized in this body and OPEN_QUESTIONS.md."
  compression: "Local UTF-8 reading, frozen-human SHA256, YAML/schema/ID/local-link consistency and unchanged-input hashes; see _WORK/COMPRESSION_NOTE.md for final results. No new network/research."
  not_performed: "Training; model inference/quality; LinQ throughput/latency; full chosen-mixture media/semantic/near-duplicate audit; reviewed continuous target camera-hours; complete legal clearance."
files:
  human: report_human_datasets.md
  sources: SOURCES.md
  facts: RAW_FACTS.md
  critic: CRITIC.md
  open_questions: OPEN_QUESTIONS.md
human_freeze:
  bytes: 157315
  lines: 479
  whitespace_words: 11593
  sha256: 9da1f9971e4ded7666c88c721c0d0da13e6019cfa9de739fc4b4ccf851c70c49
---

# Datasets: acquisition, supervision and independent target evidence

Start with organizer intake and a locked target holdout. Among investigated external sources, prioritize SFCHD for factory adaptation/development, the eight obtained Önal/Dandıl MP 4 for replay and manual event pilots, and exact SH17 Kaggle v1 for broad object/body-part supervision. SHEL5K/SHWD are conditional donors for distinct head/person tasks; CPPE-5 supplies broad face-protection objects, not a ready industrial-respirator removal task. No investigated accessible source was established to jointly cover exact respirator subtype/correctness/removal, person associations/tracks, site policies/zones and long representative safe periods. This is a bounded search result, not proof that such data do not exist. [I: F004](RAW_FACTS.md#f004), [I: F100](RAW_FACTS.md#f100), [P: F102](RAW_FACTS.md#f102).

Evidence legend, used throughout: **C** author/vendor claim or published measurement (not ours); **D** primary document/schema/terms; **A** code/artifact metadata observation; **T** our executed local count/parse/decode/visual check, with explicit scope; **I** inference from cited evidence; **P** proposed procedure/hypothesis; **U** unknown. Reading code is not executing it; metadata paths/bytes are not downloaded media; successful parsing is not semantic validation. F-IDs resolve in [RAW_FACTS.md](RAW_FACTS.md); source/version/access locators in [SOURCES.md](SOURCES.md), Q/E programmes in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). The [critic history](CRITIC.md) retains K001–K015 before and after W2; [ID map](_WORK/ID_MAP.md) retains branch provenance.

The research access snapshot is **2026-10-23, Europe/Moscow (UTC+3)**; collector freeze `2026-10-23T07:37:53.376622+03:00`. The machine file generation/check time in front matter is later and does not refresh source access. The case examples are helmet absence, removed respirator, hazardous-zone entry and smoking near flammables; gloves/boots/vest/harness remain possible extensions. Final mandatory scope and organizer data were unavailable. RTX 4070/cloud availability does not establish VRAM, SDK or LinQ input. [D: F001](RAW_FACTS.md#f001).

## Dataset acquisition and role catalogue

These are conditional selections, not a declaration that every artifact has permission for every action or is fully downloaded. Rows follow `dataset_selection_record`; detailed versions, counts and exceptions are in the named sections. Calibration/threshold tuning use development; independent evaluation stays locked; demo additionally requires display rights. [I: F100](RAW_FACTS.md#f100).

| dataset | artifact | actual_access | conditional_role | remaining_gates | facts |
|---|---|---|---|---|---|
| Organizer data | Not supplied at snapshot | None | Primary target development and locked holdout after intake | Full case, terms, schema, observability, groups | [F001](RAW_FACTS.md#f001), [F102](RAW_FACTS.md#f102) |
| SFCHD | Commit `7bfabb4533613e6917461dc3758dcff5f304bd03`; external Drive ZIP | Full annotations/directory; 7 JPEG/27 visual boxes | First factory adaptation/development candidate | Rights, selected-media decode, explicit split and inferred groups | [F023](RAW_FACTS.md#f023), [F024](RAW_FACTS.md#f024), [F027](RAW_FACTS.md#f027), [F036](RAW_FACTS.md#f036) |
| Önal/Dandıl | Mendeley `xjmtb22pff/1` | Full 691-MP 4 metadata; 8 MP 4 obtained/probed | Real replay; manual zone/event pilot | Event GT, continuous safe periods, supplied groups | [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068), [F069](RAW_FACTS.md#f069), [F071](RAW_FACTS.md#f071) |
| SH17 | Kaggle exact v1 `mugheesahmad/sh17-dataset-for-ppe-detection` | Full manifest; 13 released YOLO; separate raw XML and visual scopes; 1 exact released JPEG | Broad object/body-part donor; raw-state derivative separately | NC/action rights, full selected labels/media, coverage, source groups | [F006](RAW_FACTS.md#f006), [F007](RAW_FACTS.md#f007), [F013](RAW_FACTS.md#f013), [F021](RAW_FACTS.md#f021) |
| SHEL5K | Mendeley `9rcv8mm682/1` | All 5,000 XML hash-matched; 7 PNG | Separate helmet/head/person-state donors | 8 unresolved person objects; split membership; NC/photo rights | [F050](RAW_FACTS.md#f050), [F051](RAW_FACTS.md#f051), [F054](RAW_FACTS.md#f054), [F055](RAW_FACTS.md#f055) |
| SHWD | Repo `c952631dfc352e0defdd54b4785a9be6576451ad`; `VOC2028.zip` | Directory, 4 splits, 20 XML/8 JPEG | Normal/helmeted-head donor | Coordinate/ordinary-hat protocol; SCUT/photo rights; group audit | [F042](RAW_FACTS.md#f042), [F043](RAW_FACTS.md#f043), [F044](RAW_FACTS.md#f044), [F045](RAW_FACTS.md#f045) |
| CHV | Repo `907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d`; author ZIP | Directory/map/splits; 27 TXT/4 JPEG | Vest/helmet-color donor if needed | Coverage, parent crosswalk and action rights | [F046](RAW_FACTS.md#f046), [F047](RAW_FACTS.md#f047), [F048](RAW_FACTS.md#f048), [F049](RAW_FACTS.md#f049) |
| CPPE-5 | Original v0.1.0; HF `66f6a5efd474e35bd7cb94bf15dea27d4c6ad3f8` | Range tar prefix; complete train/test COCO; HF test 29; 2 original PNG/2 HF JPEG | Broad Mask/Goggles/Face_Shield donor | Per-image source rights, exact pixels, subtype/state relabel; 762 quarantine | [F057](RAW_FACTS.md#f057), [F059](RAW_FACTS.md#f059), [F060](RAW_FACTS.md#f060), [F061](RAW_FACTS.md#f061) |
| Smoker Detection | Mendeley `j45dj8bgfc/1` | Full RAR; all 1,120 JPEG decoded | Crop classification; manually retagged hard-negative candidates | Target transfer, near/source groups, upstream photo rights | [F063](RAW_FACTS.md#f063), [F064](RAW_FACTS.md#f064) |
| Zhang smoking/calling | Electronics 12, 3225 (2023) | Full primary PDF; data not received | Localization donor only if obtained | Reasonable author request, payload/schema/groups/terms | [F065](RAW_FACTS.md#f065), [F066](RAW_FACTS.md#f066) |
| Pictor-v3 | Repo `8f41c9525bbd1f45245f593c7502a1934eef06fa`; crowd labels | 9 TXT over 774 images; 1 JPEG | Fallback worker/head/state tasks | Approach 2 numeric map, 42 vest-box coverage, rights | [F080](RAW_FACTS.md#f080), [F081](RAW_FACTS.md#f081), [F082](RAW_FACTS.md#f082) |
| Construction-PPE | Full ZIP pinned by SHA256; mutable v0.0.0 | ZIP/directory/all labels; 4 semantic images | Optional objects/part-local negative labels | Filter 1,416 pairs, none protocol, coverage, upstream rights | [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084), [F085](RAW_FACTS.md#f085), [F086](RAW_FACTS.md#f086) |
| SARD | Zenodo `19926448`, v1/revision 4 | ZIP directories, supplementary 4.txt; unrelated Core clip | Core construction actions/plumbing; defer supplementary | Schema, linked media, ID lifecycle, source/split rights | [F072](RAW_FACTS.md#f072), [F073](RAW_FACTS.md#f073), [F074](RAW_FACTS.md#f074), [F075](RAW_FACTS.md#f075) |
| PhysicalAI-Event-Videos | v1.0; HF `7f79b39fcd1ef1dc39f23f227cd8a9480d6077db` | Metadata and deterministic join only | Optional synthetic plumbing/augmentation after real GT | Exact media, generator/scenario grouping, restrictive action terms | [F076](RAW_FACTS.md#f076), [F077](RAW_FACTS.md#f077), [F078](RAW_FACTS.md#f078), [F079](RAW_FACTS.md#f079) |

## SFCHD: factory adaptation, exact membership and competing splits

SFCHD is one of the closest investigated donors to factory CCTV, but its defensible role is conditional adaptation/development. Authors describe two chemical plants, nearly 40 indoor/outdoor scenes, one week saving one image every 10 frames when people were present, about 40,000 candidates reduced to 12,373. Six professional safety inspectors annotated and three graduate students reviewed. These are collection/protocol claims; original FPS, representative empty/safe camera-hours and perfect annotation quality are not established. Time, plant location and sensitive fields were de-identified; do not reconstruct reliable timestamps from pixelated overlays. [C/D: F023](RAW_FACTS.md#f023), [paper/repo](https://github.com/lijfrank/SFCHD-SCALE/tree/7bfabb4533613e6917461dc3758dcff5f304bd03).

`all_data.json` (20,359,104 bytes) was fully parsed: **12,373 unique image records/50,559 unique annotations**, no duplicate IDs or empty image records. Declared sizes: 11,349 at 1280×704; 1,024 at 1920×1080. Paper maximum 1920×1280 differs from the JSON maximum. COCO `bbox` is pixel `xywh`; empty `segmentation`/`iscrowd=0` provides no masks, tracks or person-item relations. [T/A: F024](RAW_FACTS.md#f024).

Exact artifact class map and full-COCO box counts (including the record without pixels):

```text
0 person          17,010  person region; PPE state not defined
1 helmet          14,298  helmet object
2 self_clothes        780  Other Clothing, predominantly torso
3 safety_clothes   14,813  Safety Clothing/torso, not automatically reflective vest
4 head             1,200  head region; source no-helmet candidate
5 blur_head        1,134  head protection indistinguishable under light/shadow
6 blur_clothes     1,324  clothing indistinguishable
```

Keep blur states unknown/ignore for target wearing; `self_clothes` is not ready `no_vest`. Seven selected JPEG/27 overlay boxes confirmed head/torso/person distinctions and dark, overexposed and distant cases; class-driven selection does not estimate error prevalence. [T/D: F025](RAW_FACTS.md#f025), [T: F033](RAW_FACTS.md#f033).

The official [Drive ZIP](https://drive.google.com/file/d/1-2z7r3J4sZdLvVt5mllvSEwAFO49Y-zj/view) directory/Range totals show **1,972,746,810 bytes**, 37,216 entries, **12,372 JPG** in `QY_final_dataset/images/`. Only COCO basename `192.168.2.20_1c_29.jpg` lacks media; it has seven boxes, one per ID 0–6. It also lacks a modern TXT and author train/val membership. An old TXT was extracted and agrees with candidate COCO conversion; it cannot recover the missing JPEG. Use **12,372 media names/50,552 boxes**, retaining the original record under `media_not_in_author_archive` quarantine until exact pixels arrive ([Q006](OPEN_QUESTIONS.md#q006)). Full JPEG decoding, whole-ZIP SHA256 and immutable external-archive revision remain undone/unknown. [T: F027](RAW_FACTS.md#f027), [U: F035](RAW_FACTS.md#f035).

All **50,552 shared boxes** agree COCO↔YOLO by class and normalized `cxcywh` at tolerance `1e-5`; actual maximum error `2.5673907444456745e-16`. `labels.zip` is 3,569,708 bytes with 12,372 nonempty TXT plus directory. Agreement establishes representation lineage, not independent semantic correctness. Prefer pinned COCO as source and generate YOLO reversibly if required. Strict bounds at `1e-6 px` flag 530 boxes: **518 overflow ≤0.001 px; 12 material overflow >0.001 and >0.01 px**, maximum `9.000288 px`, ten person/two safety_clothes. Annotation 640 of `192.168.2.20_35.jpg` has `[139.00032,456.00016,187.00032,257.000128]` in 1280×704. No clipping/deletion was performed. Preserve original boxes; any derived clipping requires decoded dimensions and a change reason. [T/I: F028](RAW_FACTS.md#f028), [T: F029](RAW_FACTS.md#f029).

Published totals 50,558/50,559/50,552 coexist. Full COCO is 50,559; media intersection is 50,552. This arithmetic does not prove the historical explanation for every publication discrepancy. [T/C: F026](RAW_FACTS.md#f026).

There are **two validation protocols**: TXT train 9,897/val 2,475 disjoint, union 12,372; COCO `val.json`2,475 images/10,336 annotations. Their val overlap is only **520**, with 1,955 unique to each and symmetric difference 3,910. All six `test.txt` paths are already in TXT val; `annotations/test.json` is 0 bytes. No independent third test exists in those artifacts. Reproducing a paper metric requires the exact protocol/config/version ([Q007](OPEN_QUESTIONS.md#q007)); do not merge the two val sets into one named benchmark. [T: F030](RAW_FACTS.md#f030).

The six tiny-test basenames are `192.168.11.13_neg_7c_2832.jpg`, `192.168.2.35_neg_12c_362.jpg`, `192.168.2.28_caiji_1_24.jpg`, `192.168.2.221_400.jpg`, `192.168.2.34_neg_12c_275.jpg`, `192.168.2.220_480.jpg`. Author TXT uses a machine-local absolute prefix: remap to portable relative paths after collision checking. Duplicate sample copies in git do not add unique images. [T: F031](RAW_FACTS.md#f031).

Removing final `_integer` gives **231 inferred runs**, 205 spanning train/val, 24 train-only/2 val-only; initial IPv 4-like strings give **40 prefixes, all spanning train/val**. These are proxies, not supplied camera/run IDs. Two different runs under one prefix show the same stable factory view, so run-disjoint splitting is insufficient for a new-view claim. Prefix grouping plus manual view merging is a more conservative initial proxy; different prefixes may still share sites/views. Keep supplied IDs null and proxy evidence separate; obtain non-sensitive equivalence groups rather than recovering removed timestamps ([Q008](OPEN_QUESTIONS.md#q008)). [T/I: F032](RAW_FACTS.md#f032), [I: F034](RAW_FACTS.md#f034).

Explicit action permission was not found in pinned tree/root LICENSE/archive directory; this is a bounded notice gap, not a proven blanket prohibition. Do not deserialize `labels.cache` as trusted executable material; TXT/JSON suffice. Rights remain [Q003](OPEN_QUESTIONS.md#q003)/E014. Pin commit, name the chosen split, form the media intersection, decode the selected subset, log geometry exceptions and group evidence. [T/U: F035](RAW_FACTS.md#f035), [P: F036](RAW_FACTS.md#f036).

## SH17: exact release, raw states and historical image identity

SH17 is a broad object/body-part donor from Pexels/web industrial photographs, not original CCTV. Empty images were excluded. Authors describe manual annotation/review (three annotators, lead correction and graduate review), but exhaustive all-class/min-size/occlusion rules were not found. No supplied tracks, zones, events or person-item relation IDs exist in the examined protocol. [C/D: F005](RAW_FACTS.md#f005), [paper2407.04590v1](https://arxiv.org/html/2407.04590v1), [pinned repo](https://github.com/ahmadmughees/SH17dataset/tree/2f832c289f9deea063367045ed8230b26e3e7ea9).

Use **Kaggle version 1** `mugheesahmad/sh17-dataset-for-ppe-detection`, id 5329058, creation `2024-07-03T23:09:23.513Z`. Completed pagination found **32,398 unique paths=8,099×4+2**: equal stem sets for `images/`, `labels/`, `meta-data/`, `voc_labels/`, plus two split files. Listed bytes: images 14,203,596,226; YOLO 2,998,015; metadata 10,672,761; VOC 19,863,513. Earlier API `totalBytes`14,096,291,832 is a different metadata field. None is a locally measured whole download. Start with small labels/metadata rather than all 14 GB of photos. [T/A: F006](RAW_FACTS.md#f006), [Kaggle](https://www.kaggle.com/datasets/mugheesahmad/sh17-dataset-for-ppe-detection).

The tested single-file route is:

```text
https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName={path}
```

Actual payload: **13 released YOLO files, 2 VOC, 2 metadata JSON, 1 released image ZIP**. Old path-suffix route and `released_sh17.yaml` returned 404 JSON. A JPEG-named request can return ZIP; inspect signatures, preserve request/status/hash, and pin received content. The full 8,099 released YOLO layer was not obtained/parsed. Exact requests are in [S004](SOURCES.md#s004). [T: F007](RAW_FACTS.md#f007).

Exact zero-based `sh17.yaml` map; YOLO normalized `cxcywh`:

```text
0 person; 1 ear; 2 ear-mufs; 3 face; 4 face-guard; 5 face-mask;
6 foot; 7 tool; 8 glasses; 9 gloves; 10 helmet; 11 hands; 12 head;
13 medical-suit; 14 shoes; 15 safety-suit; 16 safety-vest
```

Preserve literal `ear-mufs`; TableII order is not this ID map. `ear-mufs` can include headphones; `glasses` merges safety/vision; `shoes` merges ordinary/nominal safety footwear; `foot` includes socks and is not universal `no_boots`; `head`/`hands` are not `no_helmet`/`no_gloves`. TableII author object counts in ID order are **13,802; 7,730;318; 8,950;134;669;796; 4,647; 1,945; 2,790;927; 15,850; 11,985;155; 4,560;530;530**. They were not fully recounted in release. Rare face-guard/ear-mufs support is not comparable to body-part support. [D/C: F008](RAW_FACTS.md#f008).

Actual `train_files.txt`6,479/`val_files.txt`1,620 have intersection 0/union 8,099. No third split appears in full listing; test request 404. Paper calls the 20% partition test, artifact calls it val; do not count both. CSV has 8,099 unique URLs and one alias: `carrying-on-head-indian-farm-worker-158011.jpeg` versus split/raw `carrying-head-indian-farm-worker-158011.jpeg`. Join release paths with an explicit alias table. [T: F009](RAW_FACTS.md#f009).

The separate [author raw ZIP](https://github.com/user-attachments/files/17777364/SH17-raw.zip), linked from [issue4](https://github.com/ahmadmughees/SH17dataset/issues/4), is 5,835,796 bytes, SHA256 `ebac83a98d36b32c54d00efa9e8591279bb80232711fdd385d5dbac09cf462a9`. All **8,102 XML/76,008 objects** parsed; errors 0, empty XML 4480451/4614217. Two raw boxes exceed declared bounds:258626 person `[1725,4430,1874,4664]` in 3456×4608; 259265 tools-off `[1559,123,3509,1358]` in 3504×2336. Raw flags:71,949 truncated 0/difficult 0 and 4,059 truncated 1/difficult 0; no difficult 1. These are raw structural findings, not final-release error rates. [T: F010](RAW_FACTS.md#f010).

Raw release-member intersection removes the two empty XML and 12069485 with one `fork-lift`:76,007 objects remain. Removing 13 further `fork-lift` objects outside the 17-map gives candidate **75,994**. Candidate conversion collapses on/off, colors, safety/vision and demographics→person, correcting `halmet`→`helmet`; total arithmetic does not establish full released-label equality or cleanup. [T/I: F012](RAW_FACTS.md#f012).

**Keep the three evidence scopes separate:** (1)13 released YOLO files/**228 annotation boxes** matched mapped raw classes/normalized geometry with `maxabs<1e-6`, unmatched 0, 16/17 IDs (missing foot 6); (2)13 raw XML/current-Pexels visual samples were inspected separately; (3)exact released JPEG was obtained only for **13376117**. This is **not 13 complete released media/label pairs** and not a full release audit. [T: F013](RAW_FACTS.md#f013), [T: F014](RAW_FACTS.md#f014), [T: F016](RAW_FACTS.md#f016).

Raw on/off object counts (not independent people/events):

```text
gloves 2669/121; glasses-vision 1357/163; glasses-safety 373/52;
ear-mufs 211/107; face-mask-medical 635/35; safety-shoes 1150/22;
other-shoes 3287/101; tools 1739/2903; safety-vest 525/5;
safety-suit 234/6; face-guard 123/11.  Format: on/off objects.
```

Raw has 60 categories; `halmet-*` retains typo/state/color, `medical-suit-on`157; body parts hands 15,850/head 11,985/face 8,950/ear 7,730. Safety-shoes definition can include thick joggers; a label is not industrial certification. [T/D: F011](RAW_FACTS.md#f011).

Observed counterexamples refute **off→person without PPE**:5691469 empty glove on a surface; 3822859 hanging safety glasses; 5715901 glasses in hand; 209719 hanging vest-off, wall helmet-off and helmet-on on a head simultaneously; 8961520 helmet in hand beside a bare head. Mask-off 5726785 is below the chin; face-guard-off 3379761 is held near a welder's face. On does not prove correct fit. Add a separate person/item relation and visibility/state layer rather than rewriting source objects as person absence. [T/I: F014](RAW_FACTS.md#f014), [T: F015](RAW_FACTS.md#f015), [P: F020](RAW_FACTS.md#f020).

Targeted noise candidates:5691606 `glasses-vision-on` visually covers glove/tool, and release ID 8 preserves it; 8488036 has overlapping yellow/red `halmet-on` boxes on one head. Do not infer overall noise frequency. For 13376117, current Pexels is 8688×5792 versus raw/released VOC 8192×5461; a 4,580,857-byte release ZIP yielded the exact 8192×5461 JPEG, whose overlay aligns. The earlier shift came from substituting current external pixels, not proven mass annotation displacement. Equal dimensions in the other 12 current samples do not prove pixel identity. [T: F013](RAW_FACTS.md#f013), [T: F015](RAW_FACTS.md#f015), [T: F016](RAW_FACTS.md#f016).

Unresolved author tables: safety-suit 530 versus 195+45=240; medical-suit 155 versus 157; mask 669 versus 670; foot 796 versus 759. Full released per-class counts/cleanup remain [Q004](OPEN_QUESTIONS.md#q004), formal off/coverage/source groups [Q005](OPEN_QUESTIONS.md#q005). Author duplicate-removal claim lacks method/cluster list; disjoint names and photographer IDs are not independent photo sessions. All raw/released/crop/augmentation derivatives inherit original groups/split. [C/U: F017](RAW_FACTS.md#f017), [U/I: F022](RAW_FACTS.md#f022).

Rights conflict stays explicit: Kaggle v1/README **CC BY-NC-SA 4.0/research-education**; [Zenodo12659325v1](https://zenodo.org/api/records/12659325) **CC BY-NC 4.0**, restricted/empty file listing. Paper commercial wording does not cancel artifact NC. Separate code license and raw-attachment scope were not found/clarified. [Pexels Terms](https://www.pexels.com/terms-of-service/) updated 20.10.2026 allow commercial/noncommercial uses subject to restrictions including standalone redistribution, false endorsement and some uses of people/brands; crop/resize alone does not remove standalone restrictions. Current terms do not establish each photo's 2024 conditions or blanket ML permission. Prize-hackathon/weights/SA scope remains Q003/E014. Public demo can instead use appropriately permitted organizer/own media. [D/U: F018](RAW_FACTS.md#f018).

## SHWD: literal person is a head region

Use SHWD only as a conditional head donor. README claims 7,581 images/9,044 helmet-wearing objects/111,514 normal-head negatives; positives come from Google/Baidu and some normal heads from SCUT-HEAD. Aggregate object counts were not fully recounted. VOC uses text names; code `CLASSES=['hat','person']` assigns loader order 0/1. **`shwd:person -> normal_head_region`; `shwd:hat -> helmeted_head_region`**, often including face, not shell-only helmet. [C/D: F042](RAW_FACTS.md#f042), [I: F045](RAW_FACTS.md#f045), [repo](https://github.com/njvisionpower/Safety-Helmet-Wearing-Dataset/tree/c952631dfc352e0defdd54b4785a9be6576451ad).

Actual [VOC2028.zip](https://drive.google.com/file/d/1qWm7rrwvjAWs1slymbrLaCf7Q-wnGLEX/view) has 1,117,970,537 bytes by Content-Range, 15,171 entries, 7,581 XML/7,581 media stems (7,571 `.jpg`, 10 `.JPG`), unmatched 0. Obtained directory, 4 split TXT, 20 XML, 8 JPEG; whole archive SHA256/revision unknown. Actual train 5,457/val 607/test 1,517 are pairwise filename-disjoint; trainval 6,064=train+val. No supplied camera/session IDs. [T: F043](RAW_FACTS.md#f043).

The 20 XML contain 214 objects (24 hat/190 person); 8 visual pairs include 127 person/14 hat boxes and matching declared/decoded dimensions. Web stock portraits, portrait collage, classrooms, street and construction views confirm mixed domain/head geometry. XML filename can be stale: archive `PartA_00772` contains `772.jpg`; join actual archive-member stem, preserving XML fields. VOC integer `xyxy` origin/inclusive convention and ordinary-hat/carried-helmet/occlusion policies remain [Q009](OPEN_QUESTIONS.md#q009). MIT root covers software/associated documentation; SCUT upstream is academic-research-only, photo rights separate. Do not call all photos MIT. CHV is not independent after SHWD. [T: F044](RAW_FACTS.md#f044), [D/U: F045](RAW_FACTS.md#f045).

## SHEL5K: six geometries and eight unresolved person objects

SHEL5K reannotates the same 5,000 SHD images (`andrewmvd/hard-hat-detection`), expanding 3→6 classes; SHD is not SHWD. [Mendeley9rcv8mm682/1](https://data.mendeley.com/datasets/9rcv8mm682/1), 23.04.2021, supplies 5,000 XML/5,000 PNG matching stems. **All 5,000 XML obtained and every SHA256 matched author metadata; 7 PNG obtained.** Metadata sums XML 19,154,616 bytes/PNG 1,310,436,038 bytes are not a downloaded compressed ZIP. Empty root API `files: []` does not mean no nested data. [D/T: F050](RAW_FACTS.md#f050), [paper](https://doi.org/10.3390/s22062315).

Full XML parse: **75,578 objects=75,570 advertised six-class objects+8 unexpected `person`**:

```text
helmet 19,252; head_with_helmet 16,048; person_with_helmet 14,767;
face 14,135; head 6,120; person_no_helmet 5,248; person 8.
```

No source numeric IDs in VOC: assign/version a derived loader map explicitly. Parse failures, empty XML, filename-stem/hash mismatches 0. Integer bounds `0<=xmin<xmax<=W`, `0<=ymin<ymax<=H` violations 0; exact origin/inclusive convention remains unproven. Declared W/H:416×416(2,192),416×415(2,461),415×416(324),415×415(23), not uniformly square. Flags 69,531 `(truncated,difficult)=(0,0)`/6,047 `(1,0)`; difficult 0 everywhere does not mean easy data. [T: F051](RAW_FACTS.md#f051), [T: F052](RAW_FACTS.md#f052).

Geometry is genuinely different: `hard_hat_workers0` helmet `[360,118,406,149]` versus head_with_helmet `[360,118,406,175]`; 1000 person_with_helmet `[249,92,416,311]` versus helmet `[327,91,409,147]`. Crowded 2743 has 104 objects/partial heads/faces. No explicit relation IDs or correct-fastening GT. [T: F053](RAW_FACTS.md#f053).

Unexpected objects, all filenames prefixed `hard_hat_workers`:

```text
1016: [75,125,232,325], [256,105,284,176]
1303: [87,94,211,374], [242,133,370,378]
1571: [325,130,393,329], [380,139,416,318]
1595: [211,74,262,251]
380:  [259,33,335,286]
```

Only 1016/1303 were additionally inspected as pairs: hidden/indistinguishable head, tiny worker, explicit yellow helmet and ambiguous headwear occur. **Blanket person→no_helmet is refuted.** Preserve `raw_person_unresolved`; quarantine from six-class loss, ignore or manually relabel with reasons. Do not infer states of the remaining four objects. [T/P: F054](RAW_FACTS.md#f054).

Paper random 4,000/1,000 gives sizes, not supplied membership/seed; names were not found in pinned repo/manifests/XML. Obtain author split or name an own source/group-aware split. CC BY-NC 3.0 is not SA; upstream photos remain separate. SHEL5K is a conditional donor for separate object/head/person-state tasks; SHD is not independent holdout after it. [U/D/I: F055](RAW_FACTS.md#f055), [Q011](OPEN_QUESTIONS.md#q011).

## CHV: body, vest/torso and colored helmet objects

CHV is a selected/reannotated child of SHWD+GDUT-HWD, not 1,330 new independent scenes. Authors selected 1,330 images from about 10,000 parents, reporting 9,209 objects and random 1,064/133/133; exact parent crosswalk remains unmeasured. [C/D: F046](RAW_FACTS.md#f046), [paper](https://doi.org/10.3390/s21103478), [pinned repo](https://github.com/ZijianWang-ZW/PPE_detection/tree/907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d).

Actual [CHV_dataset.zip](https://drive.google.com/file/d/1fdGn67W0B7ShpBDbbQpUF0ScPQa4DR0a/view):439,733,771 bytes, 1,330 JPG/TXT pairs excluding `__MACOSX/`/AppleDouble `._*`. Archive README fixes normalized YOLO center `cxcywh`: **0 person, 1 vest, 2 blue helmet, 3 red helmet, 4 white helmet, 5 yellow helmet**. Actual train 1,064/valid 133/test 133 are filename-disjoint. Whole image decode/9,209-object recount not performed. [T/D: F047](RAW_FACTS.md#f047).

Twenty-seven TXT contain 194 objects (77 person/48 vest/10 blue/11 red/33 white/15 yellow); 4 JPEG/37 visual boxes establish body/visible-person, reflective clothing/torso and helmet-object units. `ppe_0183` has a person without an obvious helmet, but no no_helmet class/status; missing helmet box is not exhaustive negative GT. No association/correctness layer. README “open for free use” plus citation is a permissive statement with unspecified modification/republication/commercial scope, not blanket upstream clearance. Add CHV when vest/color gains justify coverage/rights/overlap checks; never use it as independent test after SHWD. [T: F048](RAW_FACTS.md#f048), [D/I: F049](RAW_FACTS.md#f049), [Q010](OPEN_QUESTIONS.md#q010).

## CPPE-5: broad face protection, Apache annotations and quarantined pixels

CPPE-5 is a conditional broad-object donor, not an exact industrial-respirator removal dataset. Medical/non-iconic web photos are predominantly Flickr, less Google Images. Seven categories were considered; separate respirator/shoe-cover dropped for insufficient rich examples, full-facepiece respirator absent even from the initial list. Respirator-like products nevertheless occur inside final `Mask`. Two independent volunteers plus adjudicator/review are author protocol; claimed exhaustiveness covers five final classes, not every desired subtype/state. [C/D: F056](RAW_FACTS.md#f056), [paper](https://arxiv.org/abs/2112.09569).

Original [v0.1.0 release](https://github.com/Rishit-dagli/CPPE-Dataset/releases/tag/v0.1.0) published 14.12.2021 19:20:05 UTC, tag commit `c18d33dd33230c601c62f944df2626cd73412a79`; `dataset.tar.gz` metadata 238,482,705 bytes. HTTP Last-Modified 15.04.2023 is distinct; later v0.2.0 has no assets. Obtained Range prefix 8,388,608 bytes with complete `train.json`690,419 bytes/`test.json`30,993 bytes and 2 PNG. Full tar manifest and README MD5 `f4e043f983cff94ef82ef7d57a879212` were not validated. Current repo pinned at `8d6701db6a25a3ce482f8a3d9766ebe318b1f1dc`. [T: F057](RAW_FACTS.md#f057).

Actual original annotations: train **1,000 image records/4,491 boxes**, test **29/207**, total **1,029/4,698**, not full media decode. Original COCO IDs **1 Coverall, 2 Face_Shield, 3 Gloves, 4 Goggles, 5 Mask**, pixel `xywh`; [HF revision](https://huggingface.co/datasets/rishitdagli/cppe-5/tree/66f6a5efd474e35bd7cb94bf15dea27d4c6ad3f8) uses 0–4 in same order. All 29 test IDs/declared dimensions/category+bbox multisets matched after **`HF category+1 -> original category`**, joined by `image_id`, not row order. Test counts 45 Coverall/17 Face_Shield/61 Gloves/32 Goggles/52 Mask. Original PNG↔HF JPEG byte/pixel identity untested. Paper 1,029 training+another 100 testing does not establish a public 1,129-image archive; additional 100 protocol remains Q012. [T/D: F058](RAW_FACTS.md#f058), [T/U: F059](RAW_FACTS.md#f059).

Author Table 3 object counts 1,197 Coverall/447 Face_Shield/1,343 Gloves/407 Goggles/1,304 Mask are published figures, not interchangeable with the public annotation totals. Keep underscores and category shift. [C: F058](RAW_FACTS.md#f058).

Concrete pixels: H F101 2 shows an elastomeric half-mask with filters/straps; 1013 a molded filtering half-mask. These are our visual subtype descriptions, not author subtype GT/certification/fit-test. Original 15.png actual/declared 943×663 shows three masked people but only 2 Mask boxes 114/115: investigate possible partial labels without claiming overall omission rate. Exact filename 762.png/image_id 762 is actual 2246×1498 versus declared 1200×1200 with 3 Mask boxes: **coordinate/version quarantine**, no silent rescaling. Unlike SH17 13376117, the correct historical coordinate frame is unresolved. Train 762 is outside test 29 scale audit. [T: F061](RAW_FACTS.md#f061).

The dated [author comment29.03.2022](https://github.com/Rishit-dagli/CPPE-Dataset/issues/6#issuecomment-1082077175) explicitly applies **Apache 2.0 to code and annotations**; do not revert to “only code, labels unknown.” Photo copyright/Flickr terms are separate. COCO root/images lack source URL/author/license inventory; checked release tree/assets/HF did not provide numeric image_id→source/author/license join. Remaining tar/author inventory were not examined, so do not assert it does not exist. Photo/crop publication and subtype selection need that join and exact selected pixels. [D/T/U: F060](RAW_FACTS.md#f060), [Q012](OPEN_QUESTIONS.md#q012).

Mask/Goggles/Face_Shield can remain broad object tasks with explicit partial coverage; target industrial subtype, visibility, worn/removed/incorrect/unknown and person association need a new layer. Missing Mask is not no_respirator; visible appearance cannot certify fit or product protection. [I/P: F062](RAW_FACTS.md#f062).

## Smoking: image classification, localization and temporal policy remain separate

Smoker Detection Dataset [Mendeleyj45dj8bgfc/1](https://data.mendeley.com/datasets/j45dj8bgfc/1), 15.08.2022, was fully obtained: **65,575,997-byte RAR**, SHA256 `2b0ef67ec714a507cff7248ef7f3d7bbdb4c4e00adc8e309cfac02cd2b6e5d18` matched API; 1,120 JPG all decoded 250×250. Training 716=358+358, Validation 180=90+90, Testing 224=112+112. Canonical decoded-RGB exact duplicate groups 0; near-duplicate/subject/session/source independence untested. `smoking_`/`notsmoking_` are image labels, no cigarette boxes/tracks/FPS/intervals/zones. [T: F063](RAW_FACTS.md#f063).

Web portraits/studio/crops differ from factory CCTV. Forty initial negative thumbnails gave actual candidates: `notsmoking_0091` phone at face, 0053 phone in hands, 0120 inhaler at mouth, 0041 ambiguous hand at face. These are our proposed tags, not source annotations/frequencies. Collection queries mentioning drinking/eating do not establish those actions in the actual inspected set. Conditional crop-classification/hard-negative relabel donor; no operational false-alerts/hour evidence. Card CC BY 4.0 is an assembly terms layer, individual search-photo rights not recovered. [T/D/I: F064](RAW_FACTS.md#f064).

Zhang et al., *Intelligent Recognition of Smoking and Calling Behaviors for Safety Surveillance*, Electronics 12, 3225, 26.07.2023, is the stronger localization lead. [Primary PDF/DOI](https://doi.org/10.3390/electronics12153225) obtained after HTML 429. Authors sample indoor/outdoor videos every several frames, retain face-containing images via MTCNN, manually LabelMe behavior regions covering face+associated objects (`smoking/calling/normal`) and separate hand/cigarette/phone boxes. Face coordinates are automated MTCNN, not manual face GT; behavior region is not full person or interval. [D: F065](RAW_FACTS.md#f065).

Author train 10,461 frames=4,516 smoking+3,968 calling+1,977 normal; object counts 9,861 hand/6,197 cigarette/4,873 phone. Test 1,167 images from other videos/webpages is not verified person/camera/session independence. Face selection limits top/distant/turned-away views. Data only upon reasonable request to corresponding author; actual payload/terms not received, no email sent. Article CC BY 4.0 is not data permission. [C/U: F065](RAW_FACTS.md#f065), [D/U: F066](RAW_FACTS.md#f066), [Q013](OPEN_QUESTIONS.md#q013).

Neither source supplies smoking-near-flammables policy/continuous safe denominator. An independent route is E012: permitted native target clips, cigarette/hand/phone/face/head boxes, person relations, confusers phone/drink/eat/inhaler/hands-to-face, visibility, uncertain onset/end, plus separate flammable-zone rule/context. A photo's smoking class does not establish a site-policy violation. [I/P: F004](RAW_FACTS.md#f004), [F066](RAW_FACTS.md#f066).

## Önal/Dandıl: eight real MP 4, variable timing and missing event ground truth

The obtained inputs support replay/manual pilots now; they do not provide operational event metrics. Authors describe two UNV IPC 2122 CR 3-PF 40-A cameras at Kafaoğlu Metal Plastik Makine San. ve Tic. A.Ş., Eskişehir,~4 m height, capture 05.11–13.12.2022, daylight/night lamps. **About 4,000 h raw** is an author source-capture volume; public release is **691 selected clips**, not 4,000 available hours. [C/D: F067](RAW_FACTS.md#f067), [data v1](https://data.mendeley.com/datasets/xjmtb22pff/1), [article110791](https://doi.org/10.1016/j.dib.2024.110791).

Complete metadata inventory:691 MP 4/16 leaf class-split folders, train 566/test 125, advertised 9,999,951,582 bytes. Exact author class map with train/test clips:

```text
0 Safe Walkway Violation          178/32
1 Unauthorized Intervention        97/11
2 Opened Panel Cover              129/13
3 Carrying Overload with Forklift  48/8
4 Safe Walkway                    50/25
5 Authorized Intervention         23/15
6 Closed Panel Cover              19/13
7 Safe Carrying                   22/8
```

Names `0_tr1`/`0_te1` encode class/split/clip. Manifest has no interval/polygon/track/multilabel sidecars, README or license files; unpublished GT is not ruled out. Article permits multiple behaviors per clip; folder class is not exhaustive per-person state. [T/D: F068](RAW_FACTS.md#f068).

Eight actual H.264 1920×1080 MP 4, `yuv420p`/`yuvj420p`; selected JPEG frames extracted, hashes/UUID/probes saved in [SAMPLE_OBSERVATIONS.json](_WORK/MATERIALS/W2-10/SAMPLE_OBSERVATIONS.json). Full 691-clip decode not performed. Each row preserves native timing; displayed FPS is not a global constant:

| clip | bytes | duration_s | start_s | displayed_fps | tbn |
|---|---:|---:|---:|---:|---:|
| `0_te23` | 6391494 | 10.48 | 0 | 23 | 19672 |
| `0_te9` | 33474374 | 17.02 | 0 | 24.80 | 15872 |
| `4_te5` | 4217183 | 10.44 | 0 | 25.10 | 19672 |
| `4_te19` | 28558205 | 15.06 | 0 | 24.83 | 19864 |
| `0_tr128` | 3021735 | 10.45 | 0 | 25.08 | 19672 |
| `0_tr16` | 34584860 | 16.98 | 0.040008 | 24.80 | 15872 |
| `4_tr13` | 3240413 | 10.41 | 0 | 25.06 | 19672 |
| `4_tr6` | 42290441 | 20.84 | 0 | 25.05 | 16032 |

20.84 s refines paper 1–20 s; use timestamps/timebase/start, not frame number divided by hardcoded 24 FPS. Container probes are not throughput/latency measurements. [T: F069](RAW_FACTS.md#f069).

Green walkway is site-specific; authors flag 2D projection ambiguity. Hazard-zone GT needs polygon, ground contact/footpoint, policy, visibility and time. Authorization/overload require person/equipment/context. Two observed framing groups span train/test; these are inferred viewsA/B, not supplied camera IDs. Some clips start with person already present (left-censored onset). Safe-Walkway `4_tr6` shows a person outside the stripe in selected frames: multiple actors/behaviors or author convention may explain it; not an automatic label error. Full-clip manual tracks, intervals, cut flags, relations and policy must be separate from folder labels. [T/D/I: F070](RAW_FACTS.md#f070).

No continuous raw URL, supplied camera/session IDs or reviewed long safe periods were obtained ([Q014](OPEN_QUESTIONS.md#q014)). Eight selected clips cannot support representative false alerts per camera-hour. Card data CC BY 4.0 and article CC BY-NC 4.0 apply to different artifacts; company/employee permissions are author claims, not independently audited. Retain attribution/DOI/changes; 2022 footage is not own 2026 capture. [D/I/U: F071](RAW_FACTS.md#f071).

## Pictor-v3 and Construction-PPE: fallback semantics require explicit gates

Pictor offers three tasks on shared images, not three independent datasets: Approach 1 worker/hat/vest objects+classifierW/WH/WV/WHV; Approach 2 whole-worker states; Approach 3 worker-crop classification. README reports 774 crowd images/2,496 workers plus 698 web/2,230 workers=1,472/4,726. Actual retrieved annotations cover **774 crowd images only**, not web 698. [D/C: F080](RAW_FACTS.md#f080), [repo](https://github.com/ciber-lab/pictor-ppe/tree/8f41c9525bbd1f45245f593c7502a1934eef06fa).

Nine TXT (3 approaches×3 splits) have matching membership 502 train/120 valid/152 test, union 774/intersections 0. Format filename plus tab-separated integer `x1,y1,x2,y2,class` tuples. Approach 1 train 2,752/valid 707/test 726 boxes; classes 0=1,646/1=42/2=2,497. One paired sample confirms 2 worker and 0 hat-head; 1 vest follows README/exclusion, no paired vest-positive inspected. Approach 2 counts 0=873/1=1,583/2=1/3=40, **numeric W/WH/WV/WHV map unknown**, not README order. Approach 3 all 2,497 worker boxes class 0. Actual 2,497 versus author 2,496 remains version/protocol unknown. [T/U: F081](RAW_FACTS.md#f081).

One `image_from_china(1).jpg`1221×912,583,945 bytes, SHA256 `82c4d916bdcecd8dbd36a27817cc9a8e6b5cd60898a2995fe44bd1228b04d5c2` links 3 worker boxes across approaches; no full-media completeness/independence claim follows. No explicit license in pinned repo/annotations; citation request is not redistribution grant. Keep conditional crowd/state fallback after numeric-map/rights checks; 42 vest boxes make it a weak first vest choice. [T/U/I: F082](RAW_FACTS.md#f082), [Q017](OPEN_QUESTIONS.md#q017).

Construction-PPE [ZIP](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip) fully obtained:178,415,813 bytes, SHA256 `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`, asset updated `2025-09-07T05:14:00Z`. Mutable tagv 0.0.0 is not immutable; pin hash. Internal normalized YOLO `cxcywh` map:

```text
0 helmet; 1 gloves; 2 vest; 3 boots; 4 goggles; 5 none; 6 Person;
7 no_helmet; 8 no_goggle; 9 no_gloves; 10 no_boots
```

`no_vest` absent; preserve capital `Person` and singular `no_goggle`. Internal full AGPLv 3 notice/YAML AGPL-3.0 are artifact evidence; 19.11.2007 dates the license text, not dataset. Neither upstream-photo rights nor automatic weights obligations are established by that notice. [T/D: F083](RAW_FACTS.md#f083).

ZIP 2,852 entries: **1,416 images/1,426 labels/1,416 exact stem pairs**. Image splits 1,132/143/141, label splits 1,142/143/141. Ten train orphans `image 940(1)`,941(1),944(1),945(1),946(1),947(1),948(1),949(1), 95(1),950(1) must not autojoin stems without `(1)` or become 10 extra images. All 1,426-label counts **including orphans**:helmet 1,750/gloves 1,461/vest 1,632/boots 1,613/goggles 526/none 800/Person 2,265/no_helmet 485/no_goggle 411/no_gloves 556/no_boots 115. These are not paired-only training counts. [T: F084](RAW_FACTS.md#f084).

Four semantic images show no_helmet=head, no_goggle=eye region, no_gloves=hands, no_boots=feet/footwear, Person=body. `image 1120.jpg` has ordinary glasses despite no_goggle; meaning is not absence of any glasses. `none` is torso in one sample, insufficient to rename no_vest. Child/sport/portrait examples defeat a factory-CCTV-only characterization. No exhaustive visibility/occlusion/source-photo protocol found. Filter exact 1,416 pairs; quarantine orphans; preserve units and uncertain person-item relations. Conditional extra donor only if gloves/boots/goggles justify preparation. [T/I/P: F085](RAW_FACTS.md#f085), [F086](RAW_FACTS.md#f086), [Q018](OPEN_QUESTIONS.md#q018).

## SARD and PhysicalAI: detailed metadata does not establish validated tracks or media

SARD supplementary is deferred pending schema/identity gates; Core is at most a conditional construction-action/plumbing donor. [Zenodo19926448](https://zenodo.org/records/19926448), Wu, Chengfeng, v1/revision 4: publication 30.04.2026, created/modified 13.05.2026. Card claims Core 748 clips/11 activities/27 HOI; supplementary 9 clips/67,098 annotated frames/1,018,232 person boxes, last counts not fully recounted. Core ZIP 8,250,845,424 bytes, MD5 `0302eb8d2af0722a9aa02f578cd03f89`, directory 748 media; supplementary 35,002,552,520 bytes, MD5 `ba5586b6b5badf1987c62d84b876829c`, 9 MP 4+9 TXT. Full archives not downloaded. [D/A/T: F072](RAW_FACTS.md#f072).

Core folder counts:Carry object 52/Climb ladders 47/Hammer nails 51/Install scaffolding 79/Laying bricks 104/Measure 46/Mix concrete 86/Pour concrete 96/Saw 54/Shovel 49/Weld 84. These are directories, not numeric activity IDs inferred from order. [T: F072](RAW_FACTS.md#f072).

Supplementary `4.txt`5,963,836 bytes/160,824 lines CRC-checked. Safe parser preserves first 2 integers as **raw_id_1/raw_id_2**, source class, variable-length middle action, final 4 coordinates; preserve `Unknow`/empty. Classes:person 49,546/vest 47,417/helmet 38,901/slogan 10,484/hopper 10,272/hook 2,446/board 1,357/scaffold 381/brick 11/ebox 9. raw_id_1 has 43,951 unique in 1..60,432;raw_id_2 has 2,180 unique in 1..4495. **340 raw_id_2 occur with different classes**, including 48 person/vest and 174 helmet/hook/person/vest. Smooth boxes/repeated IDs support a temporal hypothesis, not stable object tracks. Eleven `wear mask(O3d)` rows are not 11 independent respirator events. [T/U: F073](RAW_FACTS.md#f073).

Obtained Core `Mix concrete/27115_29941.mp4` is a **different sequence, not paired 4.txt**:81,218 member bytes/172,585 network bytes, H.264 480×270, 2.84 s, start 0, displayed 23.96 FPS, tbn 19168. Do not assign its FPS to 4.mp 4. Schema/frame offset/ID lifecycle/supplied split/source manifest not found in examined Zenodo fields/directories/related searches; this does not prove unpublished definitions absent. Obtain linked 4.mp 4 excerpt+offset/author schema before E011. Deposit CC BY 4.0 does not establish all upstream-video rights; activity is not unsafe-policy GT. [T/U/I: F074](RAW_FACTS.md#f074), [F075](RAW_FACTS.md#f075), [Q015](OPEN_QUESTIONS.md#q015).

PhysicalAI-Event-Videos v1.0, creation 15.06.2026,[revision `7f79b39fcd1ef1dc39f23f227cd8a9480d6077db`](https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/tree/7f79b39fcd1ef1dc39f23f227cd8a9480d6077db), remains optional synthetic plumbing/augmentation **after real GT** and action review. Metadata has 1,612 parent records/3,796 labeled chunks; documented bundled generated media 1,486 parents/2,939 clips=2,919 labeled+20 unlabeled QC-excluded. CHAD/VAD-R 1 are external pointers, not bundled payload; 20 unlabeled are not negatives. Veo 3/Cosmos 3 Super generation, hybrid labels and partly model-generated captions/queries with selective human correction (provenance Gemma 4-31b-it, temperature 0.7). Train-only, no official val/test. [D/A: F076](RAW_FACTS.md#f076).

Executed ordered-category join (non-anomaly→Normal; else first regex match; defaultOther) yields **Smoking/vaping 282 labeled chunks/157 unique parents**:143 chunks NV-VAD-v1 / 139 NV-VAD-v1.1, external 0, all documented bundled. Unique `(dataset,video_id,chunk_index)`282; join dataset+basename(parent.video_path)→dataset+manifest.filename yields exactly 1 match/chunk. Old substring `smok|vap` selected 187 parents(96/87/4) in a different scope; never substitute 187 for 157. Reporting family is not closed cigarette ontology. Actual ZIP members/media bytes unverified. [T: F077](RAW_FACTS.md#f077).

Selected declared metadata FPS 24.0/windows valid:NV-VAD-v1/video_00375 parent 8 s/192 frames, chunk[0, 5]s/frames 0..119;NV-VAD-v1.1/video_01415 parent 7.875 s/189 frames, chunk[2.875, 7.875]/frames 69..188. Example inclusive ends are not a proven universal protocol. Overlapping windows/near-identical generation scenarios threaten independence; supplied scenario IDs missing. Captions “industrial loading dock” are not visual domain verification; no measured media FPS/boundaries. [T/D/U: F078](RAW_FACTS.md#f078).

Read [NVIDIA license](https://assets.ngc.nvidia.com/products/api-catalog/legal/Personas-Dataset-NVIDIA-Training-Dataset-License-Agreement-2025-11-26.pdf), text version 21.11.2025: limited/revocable/non-transferable/non-sublicensable grant solely AI training/development;§2 secure authorized users;§3.2 no transfer/distribute/embed/host/make available dataset whole/part;§3.3 notices;§3.4 no dataset subject to open source;§4 Trustworthy AI reference not separately reviewed;§12.3 trade conditions. Card “redistributable” describes NVIDIA packaging, not recipient raw/crop/label republication. [Google terms§17a/b](https://cloud.google.com/terms/service-terms) additionally apply to Veo output; per-video Veo/Cosmos assignment unknown. No blanket commercial/weights clearance. Prepared pinned paths `2026/train/videos.zip`7,954,992,209 bytes/`chunks.zip`3,853,242,520 bytes are retrieval plans, **not downloads**. Synthetic success cannot validate real CCTV. [D/U/I: F079](RAW_FACTS.md#f079), [Q016](OPEN_QUESTIONS.md#q016).

## SODA, harness, Foundation Pit and generic data: narrow auxiliary roles

Site Object Detection **SODA, Duan et al.2022** is construction SODA, not SODA-D/A or SODA 10 M. Paper counts 19,846 JPG/286,201 boxes/15 classes:person, helmet, vest, board, wood, rebar, brick, scaffold, handcart, cutter, ebox, hopper, hook, fence, slogan. Numeric IDs not obtained. UAV/handheld/hook-monitoring, 86%1920×1080; 21,863 initial→19,846 cleaned, random 90/10=17,861/1,985. “Every 30 frames” is not FPS. Blurred/ambiguous images filtered and some partially occluded/inconvenient objects omitted; not a continuous safe negative distribution. Fence is not hazard polygon; slogan not policy. Direct [VOCv1.zip](https://scut-scet-academic.oss-cn-guangzhou.aliyuncs.com/SODA/2022.2/VOCv1.zip) Range GET 403 AliyunOSS: one failed route, not proof all access closed. No XML/internal terms/hash/map; paper “open-source” is not full media grant. Defer unless construction scope matters. [D/C/T/U: F088](RAW_FACTS.md#f088), [F089](RAW_FACTS.md#f089).

Harness Xu/Huang/Huang 2023 [paper](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.12696) links [tree `251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c`](https://github.com/Huangjiajing96/Dataset/tree/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c):3,300 XML/3,300 JPEG (3,299`.jpg`+1`.JPG`). Authors describe 2,000 clothes+1,300 harness, transformed Wang helmet data+surveillance+web, split 16:4:5; supplied membership/source crosswalk/license not found. Two actual XML show person=body, harness/clothes=chest: `Dangerous0001.xml`400×486 clothes[109, 63,266,166]/person[77, 11,342,352]; `SafetyHarness0001.xml`1920×1080 harness[608,183,908,613]/person[403, 1,950, 1078]. No decoded images/numeric IDs/relations. Chest harness does not prove secured anchor/hook; `Dangerous` filename not event GT. [D/T/U: F087](RAW_FACTS.md#f087).

Foundation Pit [v2 `xjm2czccx9/2`](https://data.mendeley.com/datasets/xjm2czccx9/2), 07.11.2025, CC BY 4.0 card claims added video sequences; counts/FPS/identities/polygons/events unknown. An incorrectly guessed API 404 is not general unavailability. Inspect only if excavation scenario requires it. [D/U: F096](RAW_FACTS.md#f096), [Q019](OPEN_QUESTIONS.md#q019).

COCO/CrowdHuman/MOT support person/ROI/pose/occlusion/tracker fixtures, **not missing-PPE negatives**. COCO2017 reuses 2014 images (official rounded train 118 K/18 GB, val 5 K/1 GB, test 41 K/6 GB, annotations 241 MB; not our counts); 2020 adds no new detection/keypoint set. COCO zero-indexed pixel `xywh`, read actual categories rather than library list. Image fields include id/W/H/file_name/license/flickr_url/coco_url/date_captured, not supplied camera/session. Website/annotations CC BY 4.0, photos per-image Flickr rights. Full payload/categories not obtained. [D: F090](RAW_FACTS.md#f090).

COCO keypoint `(x,y,v)` usesv 0 not labeled/v1 labeled not visible/v2 visible; pose mainly medium/large noncrowd, not exhaustive all-person annotation. CrowdHuman author counts 15,000 train/4,370 val/5,000 test,470 K trainval persons/~23 per image, not local counts. ODGT JSON-lines `ID`, `gtboxes{tag,vbox,fbox,hbox,extra,head_attr}`, `xywh`visible/full/head, ignore/occ/unsure. **`tag=mask` is ignore/person-like/crowd/reflection, not medical mask.** ODGT/media not obtained; noncommercial research/education and image redistribution prohibited per [official page](https://www.crowdhuman.org/download.html). [D/C: F091](RAW_FACTS.md#f091).

MOT17 **21 train/21 test entries=7 base videos×3 detector variants(DPM/FRCNN/SDP) per split**, 14 base videos total, not 42 independent scenes. MOT16/17 reuse source videos. Actual 10,107,022-byte LabelsZIP/105 entries:21 train GT files form 7 SHA256 groups of 3, an annotation equality check, no pixel comparison. Sample MOT17-01-DPM seqinfo 30 FPS/450 frames/1920×1080;GT 9 numeric columns. Keep class filtering/ignore/unsure/crowd rules from exact instructions (checked route 410; do not invent filters). Online application/evaluation closed at access snapshot; use local regression, not promised submission. CC BY-NC-SA 3.0+possible upstream conditions. [D/T: F092](RAW_FACTS.md#f092), [I/P: F093](RAW_FACTS.md#f093).

MaskedFace-Net: current README 133,783=67,049 CMFD+66,734 IMFD, 1024×1024; older abstract 137,016 is another claimed state. Synthetic deformed medical-mask overlays on FFHQ faces supervise face-position, not industrial fit-test/removal-in-time. Assembly BY-NC-SA 4.0; FFHQ image conditions include BY 2.0/BY-NC 2.0/CC0/PublicDomainMark/USGovernment. Commit not pinned(API 403); no media obtained. [D/U: F094](RAW_FACTS.md#f094).

HMDB51 official 6,849 clips/51 classes includes smoke/eat/drink/chew/talk; movie/web clip classes, unstabilized/stabilized and 3 split protocols are not independent datasets or puff/onset/policy GT. Page CC BY 4.0 is not exact payload-rights verification. SED 11 subjects/20 sessions/2.69 h;SED-FL 7 subjects/10 all-day sessions/78.3 h, 3 shared subjects: public 6 DoF smartwatch pickle, smartphone video used for GT but public visual delivery unconfirmed; exclude as visual training payload. CMA [repo `06c11e0777f122e286752e2f39b45cfdd4191fd0`](https://github.com/S1mpleyang/ConstructionActionRecognition/tree/06c11e0777f122e286752e2f39b45cfdd4191fd0) README 1,595 clips/7 actions, Baidu code`z7a2`, research-only/no-commercial data separately from MITrepo; actual 7 names/IDs/full payload unknown. [D/U: F095](RAW_FACTS.md#f095).

## Preliminary class mapping: preserve box unit, unknown and coverage

Final target IDs are unassigned until full case definitions. Each row follows `mapping_record`; relations are provisional relative to the named target concept, not claims that all source labels are exhaustive. `exact` is an allowed future relation after verification, not asserted for the mappings below. Object presence, worn object, visible person state, correct wearing and policy event require different GT. [I/P: F002](RAW_FACTS.md#f002), [F097](RAW_FACTS.md#f097).

| source_literal | semantic_unit | preliminary_target | relation | condition | facts |
|---|---|---|---|---|---|
| SH17 `helmet` | Object; raw state/color flattened | Helmet object | conditional | Keep lost raw qualifiers; do not create person wearing/absence | [F008](RAW_FACTS.md#f008), [F020](RAW_FACTS.md#f020) |
| SH17 `head` / `hands` / `foot` | Body parts | Head/hand/foot regions | incompatible | Incompatible with automatic no_helmet/no_gloves/no_boots; visibility/state needed | [F008](RAW_FACTS.md#f008), [F020](RAW_FACTS.md#f020) |
| SH17 `glasses` / `shoes` | Broad objects | Safety goggles/industrial boots | partial | Safety/vision and ordinary/safety merged; split/relabel before exact task | [F008](RAW_FACTS.md#f008), [F011](RAW_FACTS.md#f011) |
| SH17 raw `*-off` | Item in varied states/contexts | Person without that PPE | incompatible | Off can be lying/hanging/carried/below chin; association and new state layer required | [F014](RAW_FACTS.md#f014), [F015](RAW_FACTS.md#f015) |
| SHWD `person` / `hat` | Normal-head / helmeted-head region | Head-state tasks | conditional | Keep head extent, ordinary-hat/occlusion policy unresolved | [F044](RAW_FACTS.md#f044), [F045](RAW_FACTS.md#f045) |
| SHEL5K `helmet` / `head_with_helmet` | Object / head | Separate object and head tasks | conditional | No direct merge across units; no correctness/relation IDs | [F053](RAW_FACTS.md#f053) |
| SHEL5K `person_with_helmet` / `person_no_helmet` | Person with observed attribute | Person-state task | conditional | Own map/group split; not correct fastening | [F053](RAW_FACTS.md#f053), [F055](RAW_FACTS.md#f055) |
| SHEL5K unexpected `person` | Person, unresolved attribute | `raw_person_unresolved` | incompatible | Eight cannot map wholesale to absence/presence; quarantine/adjudicate | [F054](RAW_FACTS.md#f054) |
| SFCHD `helmet` / `head` | Object / source no-helmet candidate head | Separate helmet/head-state tasks | conditional | Keep source units and visibility rules | [F025](RAW_FACTS.md#f025), [F033](RAW_FACTS.md#f033) |
| SFCHD `blur_head` / `blur_clothes` | Indistinguishable head/clothing region | Unknown/ignore | incompatible | Never absence labels | [F025](RAW_FACTS.md#f025), [F098](RAW_FACTS.md#f098) |
| SFCHD `safety_clothes` / `self_clothes` | Clothing/torso | Target vest/no_vest | partial | Clothing definitions differ; no automatic reflective-vest or absence equivalence | [F025](RAW_FACTS.md#f025) |
| CHV `person` / `vest` / helmet colors | Body / clothing-torso / object | Person, vest, colored objects | conditional | Add relations manually; no missing-label absence inference | [F047](RAW_FACTS.md#f047), [F048](RAW_FACTS.md#f048) |
| CPPE `Mask` / SH17 `face-mask` | Broad face-protection object | Exact industrial respirator subtype/state | partial | Medical/filtering/elastomeric mixture; subtype/person/state GT needed | [F056](RAW_FACTS.md#f056), [F061](RAW_FACTS.md#f061), [F062](RAW_FACTS.md#f062) |
| CPPE `Face_Shield` / SH17 `face-guard` | Shield object | Respirator | incompatible | Shield does not provide respiratory subtype/fit/removal GT | [F056](RAW_FACTS.md#f056), [F097](RAW_FACTS.md#f097) |
| Construction `no_helmet/no_goggle/no_gloves/no_boots` | Head/eyes/hands/feet | Part-local negative state | conditional | Not whole-person compliance; preserve literal and visibility | [F085](RAW_FACTS.md#f085) |
| Construction `none` | Torso in one inspected case | Target no_vest | incompatible | One example does not establish exhaustive none definition | [F085](RAW_FACTS.md#f085) |
| Pictor Approach 2 IDs 0–3 | Whole-worker state | W/WH/WV/WHV | conditional | Numeric mapping unknown; stop before assigning states | [F081](RAW_FACTS.md#f081) |
| Smoker `smoking_` / `notsmoking_` | Image class | Cigarette box or temporal site event | incompatible | Separate localization/interval/policy annotation required | [F063](RAW_FACTS.md#f063), [F066](RAW_FACTS.md#f066) |
| Önal class folders | Clip class, potentially multiple actors/behaviors | Per-person zone event | partial | Need policy/polygon/footpoint/tracks/intervals/censoring | [F068](RAW_FACTS.md#f068), [F070](RAW_FACTS.md#f070) |
| Generic person/pose/tracking sources | Person/head/pose/track | PPE absence | not_annotated | Missing PPE labels are out-of-scope, not verified negatives | [F091](RAW_FACTS.md#f091), [F093](RAW_FACTS.md#f093) |

The proposed target representation keeps separate fields: `annotation_status={verified_present,verified_absent,not_annotated,out_of_scope,ambiguous}`, `visibility={visible,occluded,too_small,blurred,unreviewed}`, `observed_state={worn,unworn,adjusting,incorrect,unknown}`. `incorrect` requires target instruction. Also preserve `semantic_unit`, `coverage_by_dataset_class`, person-item relation evidence and policy/event fields. These are proposed fields, not supplied across all datasets. [P: F098](RAW_FACTS.md#f098).

Verified absence requires a visible relevant body region and defined annotation protocol. Invisibility, out-of-scope class, missed annotation and true absence must remain distinct. Partial-label routes are separate dataset heads/loss masks, small targeted relabeling, locally reviewed complete crops, or exclusion; loss implementation is deferred to model_stack/training_strategy. Crops change context and can lose carried-item association; record that. [I/P: F020](RAW_FACTS.md#f020), [F098](RAW_FACTS.md#f098).

Conditional merging requires matching concepts **and units**, reversible/versioned maps, established coverage or explicit partial-label strategy, action permission, source-group/overlap controls and change reasons. Object route can combine selected SH17/SFCHD/CPPE/CHV tasks only under those gates. Head route uses SHWD/SHEL head regions separately from helmet objects. Person-state route uses explicit SHEL/Pictor states after unresolved-map quarantine. Event route needs new target tracks/intervals/rules; static objects and clip classes remain auxiliary. [I/P: F097](RAW_FACTS.md#f097), [F100](RAW_FACTS.md#f100).

## Dataset lineage and independence

Known parent relations already prohibit assuming independent parent-child holdout, even before exact image crosswalks. Rows follow `lineage_record`; shared web domains alone indicate risk, not established duplicates. [D/I: F099](RAW_FACTS.md#f099).

| parent | derivative | established_relation | independence_consequence | unresolved | facts |
|---|---|---|---|---|---|
| SCUT-HEAD | SHWD | Partly included per author | Retain upstream/source groups and academic restrictions | Exact share/matches | [F042](RAW_FACTS.md#f042), [F045](RAW_FACTS.md#f045), [F099](RAW_FACTS.md#f099) |
| SHWD + GDUT-HWD | CHV | Selection/reannotation with vest/color labels | CHV is not independent after parent training | Exact image crosswalk | [F046](RAW_FACTS.md#f046), [F099](RAW_FACTS.md#f099) |
| SHD5000 | SHEL5K | Same images, expanded/fixed annotations | SHD not independent after SHEL5K | SHD↔SHWD exact overlap unknown; do not equate names | [F050](RAW_FACTS.md#f050), [F055](RAW_FACTS.md#f055), [F099](RAW_FACTS.md#f099) |
| SH17 raw | SH17 released v1 | Membership/map lineage; sample 228 boxes match | Raw/release versions and crops stay in same source group/split | Full release cleanup equivalence | [F012](RAW_FACTS.md#f012), [F013](RAW_FACTS.md#f013), [F022](RAW_FACTS.md#f022) |
| CPPE original | CPPE HF | Test 29 annotation equality after category shift | Not independent cross-dataset test | PNG/JPEG pixel identity, full source inventory | [F059](RAW_FACTS.md#f059), [F060](RAW_FACTS.md#f060) |
| Pictor crowd images | Approaches 1/2/3 and crops | Shared 774 image membership | Tasks/crops inherit original split/groups | Web 698, numeric state map | [F080](RAW_FACTS.md#f080), [F081](RAW_FACTS.md#f081), [F082](RAW_FACTS.md#f082) |
| MOT16/base MOT17 videos | MOT17 detector variants | Source reuse; train GT 7 hash groups×3 | Keep variants/base sequence together | Media pixel audit/class filters | [F092](RAW_FACTS.md#f092) |
| COCO2014 images | COCO2017 splits | Reused images, different split | Year names are not independent sources | Actual chosen-subset overlap | [F090](RAW_FACTS.md#f090) |
| PhysicalAI parents | Chunks | Parent windows can overlap; similar scenarios documented | Group by parent and scenario when established | Supplied scenario IDs/media bytes | [F076](RAW_FACTS.md#f076), [F078](RAW_FACTS.md#f078) |
| Wang helmet data + surveillance/web | Harness dataset | Author-described transformation/assembly | Treat parent relation as leakage risk | Exact source version/image matches | [F087](RAW_FACTS.md#f087), [F099](RAW_FACTS.md#f099) |
| Shared web sources | SH17/Pictor/CPPE | Common source-domain risk only | Audit chosen mix before independent-test claim | No specific overlap established solely by web provenance | [F099](RAW_FACTS.md#f099) |
| Any original image/video | Resize/crop/re-encode/augmentation/relabel | Derived samples retain parent | One connected source group and split | Missing parent chain must be quarantined/recovered | [F101](RAW_FACTS.md#f101) |

Audit byte SHA256, then canonical decoded-pixel SHA256, then near-duplicate candidates and common source groups. pHash/embedding scores retrieve candidates; no universal truth threshold is established. Manually decide crop/resize/flip/re-encode/burst/adjacent-frame matches; retain pair score/decision/reason/contact sheet and connected components. Zero Smoker exact RGB groups does not exclude the same subject/session. Supplied camera/session/site/person IDs stay null when absent; inferred grouping keeps algorithm/version/evidence. A photographer is not a session; SFCHD prefix/run and Önal views are proxies. [I/P: F022](RAW_FACTS.md#f022), [F063](RAW_FACTS.md#f063), [F101](RAW_FACTS.md#f101), [Q020](OPEN_QUESTIONS.md#q020).

## Donor object scale: continuous 640 calculations are not a LinQ contract

SFCHD has many small helmet/head features after resize, motivating target full-frame/crop/tile comparison; this does not establish a detector pixel threshold or accuracy. Rows follow `scale_record`, q10/q50/q90 of min-axis in pixels. SFCHD scope is full COCO including 7 boxes without media; CPPE scope only HF test 29/207; SH17 scope raw all 8,102 XML, not final-release counts. Transform is continuous `s=min(640/W,640/H)` in declared dimensions, with upscale allowed and no raster rounding/clipping. [T: F019](RAW_FACTS.md#f019), [F037](RAW_FACTS.md#f037), [F062](RAW_FACTS.md#f062).

| scope_class | n_objects | native_q10_q50_q90_px | letterbox640_q10_q50_q90_px |
|---|---:|---|---|
| SFCHD helmet | 14298 | 12/27/58 | 6/13/29 |
| SFCHD head | 1200 | 12/21.06/39 | 4.21/9/18.5 |
| SFCHD blur_head | 1134 | 4/14/24 | 2/6.5/12 |
| SFCHD blur_clothes | 1324 | 9/26/53.51 | 4.5/12.5/25.37 |
| SFCHD person | 17010 | 27/58/129 | 13/28/63.02 |
| SFCHD safety_clothes | 14813 | 24/49/105 | 11.32/23.5/52.5 |
| SFCHD self_clothes | 780 | 28/53/100.1 | 11.97/26/50.05 |
| CPPE test Coverall | 45 | 102.8/300/525.4 | 95.02/196/327.25 |
| CPPE test Face_Shield | 17 | 67/122/316.6 | 40.35/88/184.02 |
| CPPE test Gloves | 61 | 34/59/194 | 22/37.33/77 |
| CPPE test Goggles | 32 | 24.2/40/161.7 | 22.42/29.5/58.3 |
| CPPE test Mask | 52 | 24/54/210.8 | 21.45/38.78/74.12 |
| SH17 face-mask-medical-off | 35 | 47/225/708.4 | 5.27/26.56/64.42 |
| SH17 face-mask-medical-on | 635 | 58.4/301/762.6 | 7.38/33.81/86.2 |
| SH17 gloves-off | 121 | 66/196/752 | 7.25/20.98/95.56 |
| SH17 gloves-on | 2669 | 56/263/942.4 | 7.24/30.67/102.46 |
| SH17 glasses-safety-off | 52 | 140.9/285/793.2 | 15.14/30.34/75.31 |
| SH17 glasses-safety-on | 373 | 81/298/613.4 | 10.33/37.04/76.28 |
| SH17 glasses-vision-off | 163 | 102/268/775.8 | 11.89/29.69/76.81 |
| SH17 glasses-vision-on | 1357 | 81.6/229/471.4 | 9.71/24.75/51.24 |

At hypothetical 640, helmet min-axis<16 px occurs in 8,845/14,298 and blur_head in 1,100/1,134. Source SFCHD **small `area_fraction<0.001`(0.1%), large`>0.002`(0.2%), otherwise medium**, equality→medium. Source Table 3 is reproduced only by 0.1%, not the nearby cited SPIE 0.12% mistakenly used in W1. Counts small/medium/large:helmet 7,717/3,030/3,551;head 941/164/95;blur_clothes 730/313/281;blur_head 1,078/41/15. At 0.12%, small counts would be 8,472/1,010/799/1,096 respectively. Relative area, COCO 32² and min-axis are different criteria. [T/D: F038](RAW_FACTS.md#f038), [F039](RAW_FACTS.md#f039), K013.

Example calculation:1920×1080 head 30×24→10×8 at 640; 3840×2160 same native box→5×4. A 180 px-wide person crop resized to 640 can yield 106.7×85.3 input head pixels, but native optical samples remain 30×24. Padding changes position, not size; crops cannot restore missing optics. Compare first-stage misses, crop context and end-to-end costs in later model experiments.640 is hypothetical, not verified LinQ input. [I/calculation: F040](RAW_FACTS.md#f040).

Executed scale audit has **132 dataset/class groups/202,781 rows**=SFCHD 50,559+SH17 raw 76,008+SH17 raw release-members 76,007+CPPEtest 207. Raw subsets intentionally overlap; never sum as independent observations. Full 132 groups/60 raw categories, exact quantiles 0/.1/.25/.5/.75/.9/1(numpy linear), native/640 width/height/area/min-axis/area_fraction, histograms and input hashes remain in [QUANTILES.csv](_WORK/MATERIALS/W2-13/QUANTILES.csv), [SCALE_SUMMARY.json](_WORK/MATERIALS/W2-13/SCALE_SUMMARY.json), [RAW_FACTS appendix](RAW_FACTS.md#приложение-к-f041--все-132-datasetclass-groups-scale-audit). Min-axis 640 bins[0,4),[4,8),[8,16),[16,32),[32,64),[64,128),[128,256),[256,640),[640,inf). VOCwidth=xmax−xmin(no+1),COCOxywh. This is declared-frame geometry, not optical visibility/model quality; rare1–10object categories do not gain stable population estimates. [T: F041](RAW_FACTS.md#f041), E031.

## Action-specific rights and acquisition decisions

Maintain separate code, annotation, original-photo/video, assembly, article and weights layers for the exact version/hash. Record permission evidence separately for local train/adapt, modification, public originals/crops/demo, labels, weights and deployment. An unknown layer neither cancels an established annotation grant nor authorizes media use. A paper's license does not transfer to its dataset. [D/I/P: F018](RAW_FACTS.md#f018), [F060](RAW_FACTS.md#f060), [F071](RAW_FACTS.md#f071), [F101](RAW_FACTS.md#f101).

Immediate open actions: SFCHD explicit grant; SH17 exact-v1 NC-SA versus alternative NC/raw/photo layers; SHWD SCUT research-only; CHV unspecified free-use scope; SHEL5K NC 3.0; CPPE Apache code+annotations with missing per-image photo join; Smoker search-photo rights; Pictor absent grant; Construction internal AGPL with unknown upstream photos; PhysicalAI AI-development-only grant and redistribution restrictions. Source-specific conditions remain in the dataset sections. Prize-hackathon NC and SA/AGPL on weights were not resolved. [U: Q003](OPEN_QUESTIONS.md#q003), [P: E014](OPEN_QUESTIONS.md#e014--action-specific-rightsprovenance-ledger).

Possible outcomes are a permitted local-research subset, restricted delivery, own annotations under applicable terms, demo on organizer/own media, source replacement or deferral. Prepare any owner question with exact version/hash/actions; **no external messages were sent** by this research. Unknown rights for one source do not block source-registry/parser preparation or authorized organizer/own-media work. [I/P: F100](RAW_FACTS.md#f100), [F101](RAW_FACTS.md#f101).

Acquisition order is organizer originals/terms→SFCHD exact annotations+selected media and eight Önal replay inputs→SH17 v 1 labels/metadata+selected pixels→SHEL5K/SHWD if head/person tasks→CHV if vest/color→CPPE if face protection→Smoker/localization lead if smoking→Construction/Pictor for justified extra classes. SARD supplementary, PhysicalAI, SODA/harness/FoundationPit remain need-driven. This ordering can change after actual target coverage/scale is known. [I/P: F100](RAW_FACTS.md#f100), [F102](RAW_FACTS.md#f102).

## Organizer intake and locked target holdout

Intake is proposed, not performed: no organizer files/full case were available. Never infer their volume, quality, camera count or format from external datasets. [P/U: F102](RAW_FACTS.md#f102), [E015](OPEN_QUESTIONS.md#e015--organizer-data-triage-до-внешней-смеси).

1. Freeze the full case/allowed actions/metrics/LinQ constraints and definitions for object, wearing, respirator, removed, incorrect, smoking, zone, event and unknown. Obtain positive/negative/ignore examples. Missing definitions stay explicit assumptions, not silently imported donor semantics.
2. Preserve immutable originals, byte counts/hashes, annotations/names/metadata. Check decoding, codec/W/H/timestamps/timebase/start, pairs/schema/geometry. Log damaged/missing/ambiguous records; never repair originals in place, presume constant FPS or rename two TXT integers into frame/track IDs.
3. Map exact source IDs/literals, box units, coverage, visibility/state, relations, zones/events before conversion. Unknown source class, unannotated target class and verified absence are separate states.
4. **Lock target holdout before external mixing**, using supplied camera/site/session/person/time groups or documented inferred groups with limitations. Preserve official test for evaluation; no threshold/donor selection, calibration or repeated solution choice on it. Every derivative inherits original group/split.
5. On development only, inspect per-class sizes/visibility/occlusion/light/background/confusers/coverage; compare donors and audit exact/near/source overlap with external candidates. Select donors for an observed gap.
6. Add a small targeted manual layer: two independent annotators, adjudication/reason log, uncertainty and observability retained. Events require policy/tracks/intervals/relations/censoring. Freeze a separate GT version for holdout.
7. Release chosen dataset revision with manifest, partial-label strategy/converter and exclusions. Calibration examples and thresholds come from development; export/LinQ execution/latency remain separate topic experiments.

If organizer development covers the scenario, adapt around it and add donors only for gaps. If labels are incomplete, compare targeted relabel cost with partial-label handling. If the camera cannot observe a requested state, narrow the claim or clarify the case. If no usable target data arrive, use permitted own capture/additional organizer material with a defined protocol; this research sets no invented collection size. [I/P: F004](RAW_FACTS.md#f004), [F102](RAW_FACTS.md#f102), [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002).

Operational event evaluation needs continuous reviewed footage including safe periods, with denominator matching reviewed camera-hours/camera set/policy. Selected violation clips can support episode recall/demo but not operational false-alert rates. Left-censored onset begins before clip; right-censored end is not observed. Neither is a complete latency/duration observation. Keep multiple actors, uncertain boundaries and repeat-alert/cooldown semantics. [I/P: F070](RAW_FACTS.md#f070), [F071](RAW_FACTS.md#f071), [E013](OPEN_QUESTIONS.md#e013--zoneevent-pilot-и-continuous-safe-denominator).

## Reproducible manifest: originals, nullable groups and reversible derivation

The manifest is a proposed delivery contract, not a claim all sources already supply these fields. It must recover where each sample came from, its original class/box/media/group/split, what changed and why it was included. Source registry distinguishes publication from access, source expected checksum from local payload SHA256, and code/labels/photos/assembly/article notices from one another. Extend the source record with actual archive byte count and download file_id when available. [P: F101](RAW_FACTS.md#f101).

The following is a **field/type template, not an actual dataset instance**; null original groups illustrate permitted absence. Populate organizer-provided IDs when present, and never copy inferred values into supplied-ID fields:

```yaml
source:
  dataset_id: string
  source_family: string
  revision: string_or_null
  publication_date: date_or_null
  accessed_at: datetime_with_timezone
  download_url: string
  expected_checksum: {value: string_or_null, origin: string_or_null}
  archive_sha256: string_or_null
  license_layers: list_of_notices_with_hashes_and_action_evidence
original:
  path: string
  image_id: string_or_null
  media_sha256: string_or_null
  decoded_pixel_sha256: string_or_null
  pixel_normalization_protocol: string_or_null
  declared_dimensions: dimensions_or_null
  decoded_dimensions: dimensions_or_null
  annotation_path: string
  annotation_sha256: string
  source_class_id: integer_or_null
  source_literal: string
  source_bbox: original_values
  coordinate_convention: string_or_null
  semantic_unit: string
  split_original: string_or_null
  group_id_original: string_or_null
  groups_original:
    camera_id: null
    session_id: null
    site_id: null
    person_id: null
  groups_inferred:
    group_id: string_or_null
    algorithm_version: string_or_null
    evidence: list
derived:
  parent_original: original_record_id
  mapping_version: string
  mapping_relation: exact_or_conditional_or_partial_or_incompatible_or_not_annotated
  target_class: string_or_null
  coverage_by_dataset_class: structured_record
  annotation_status: string
  visibility: string
  observed_state: string
  person_item_relation: structured_record_or_null
  policy_event_layer: structured_record_or_null
  transform_history: ordered_list
  usage_role: string
  inclusion_reason: string
  quarantine_reason: string_or_null
```

Preserve text VOC source IDs as null rather than inventing author numeric IDs. Record source split protocol name; file SHA256 differs from decoded-pixel SHA256, whose orientation/color normalization must be specified. `transform_history` orders orientation, scale, padding, crop bounds, clipping, coordinate conversion and relabel. Each crop/augmentation points to parent and inherits group/split. Reversible means source record/provenance recoverable; clipping or cropping cannot mathematically restore lost pixels, so retain original values. [P: F101](RAW_FACTS.md#f101).

Keep exclusions in accounting: SFCHD missing pixels, CPPE 762, Construction orphan labels and SHEL unresolved person. An E018 independent read must reconstruct original name/class/bbox/media/group/split/reason and count lost fields, unknown remaps, untraceable crops and split changes. Roundtrip success establishes traceability/portability, not correct labels/model quality/full rights. [P: F101](RAW_FACTS.md#f101), [E018](OPEN_QUESTIONS.md#e018--manifest-и-lineage-roundtrip-доставки).

## Q001–Q020: explicit unknowns and decision impact

All questions remain actionable at the frozen snapshot; a partial answer is not an implied guarantee. [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) retains known evidence, searched locations, priority, required route and K/F/E links.

| Question | Unresolved decision and next evidence |
|---|---|
| [Q001](OPEN_QUESTIONS.md#q001), P 0 | Full mandatory taxonomy/state/policy/metrics/ignore protocol; obtain full case/organizer definitions before final IDs/promises. |
| [Q002](OPEN_QUESTIONS.md#q002), P 0 | Native target resolution/FPS/timebase/views/night mode/object scale and actual LinQ preprocessing; obtain native clips/input contract, E008/E015. |
| [Q003](OPEN_QUESTIONS.md#q003), P 0 public delivery | Exact version/action permission for selected sources; owner/organizer clarification plus E014, without treating unknown as blanket ban/grant. |
| [Q004](OPEN_QUESTIONS.md#q004), P 1 | SH17 release cleanup/counts beyond 13 YOLO/228 boxes; get exact label layer and compare all selected members, E001/E003. |
| [Q005](OPEN_QUESTIONS.md#q005), P 1 | SH17 formal off/coverage/person associations/source sessions; guideline, stratified double review and grouping, E004–E007. |
| [Q006](OPEN_QUESTIONS.md#q006), P 1 | Exact SFCHD `192.168.2.20_1c_29.jpg` pixels; obtain author artifact, not regenerated TXT, E001/E002. |
| [Q007](OPEN_QUESTIONS.md#q007), P 1 | Which SFCHD val protocol underlies each published metric; exact code/config/split/version, E007. |
| [Q008](OPEN_QUESTIONS.md#q008), P 1/P 0 new-camera claim | Non-sensitive supplied SFCHD camera/scene/light equivalence groups; author manifest or explicit inferred-view limits, E007. |
| [Q009](OPEN_QUESTIONS.md#q009), P 1 | SHWD VOC origin/inclusive convention, ordinary hats/carried/occluded heads; exact guidelines/targeted pairs, E003/E004. |
| [Q010](OPEN_QUESTIONS.md#q010), P 1 | Helmet-family exact parent crosswalks/photo rights; selected-image comparison/notices, E006/E014. SHD↔SHWD overlap unknown. |
| [Q011](OPEN_QUESTIONS.md#q011), P 1 | Intended SHEL 8 person map and official 4,000/1,000 membership; author clarification or explicit own split/relabel, E004/E007. |
| [Q012](OPEN_QUESTIONS.md#q012), P 0 exact respirator/media | CPPE source/license join/exact media frames/additional 100 test; rest of tar/author inventory and targeted review, E001/E002/E004/E014. |
| [Q013](OPEN_QUESTIONS.md#q013), P 1/P 0 localization | Zhang actual images/LabelMe map/video-subject-camera groups/terms; reasonable author request not yet sent, E012/E014. |
| [Q014](OPEN_QUESTIONS.md#q014), P 0 operational metrics | Önal or target continuous safe recordings, supplied IDs/polygons/tracks/onsets; permitted continuous data/manual protocol, E013. |
| [Q015](OPEN_QUESTIONS.md#q015), P 1 | SARD schema/frame indexing/ID lifecycle/source/splits; linked 4.mp 4 excerpt+offset/definitions, E011. Supplementary deferred. |
| [Q016](OPEN_QUESTIONS.md#q016), P 2/P 1 synthetic | PhysicalAI exact ZIP members/media/generator/scenario/action scope; terms then bounded retrieval, E010/E014. |
| [Q017](OPEN_QUESTIONS.md#q017), P 1/P 2 | Pictor numeric state map/2,496 vs 2,497/web 698/terms; exact version/guideline and pairs, E004/E005/E014. |
| [Q018](OPEN_QUESTIONS.md#q018), P 1/P 2 | Construction none/coverage/source-photo rights/orphan policy/paired-only counts; filter and targeted review, E002–E005/E014. |
| [Q019](OPEN_QUESTIONS.md#q019), P 2 | SODA/harness/FoundationPit/generic payload/schema/terms gaps; investigate only for a concrete case need, E001/E009/E014. |
| [Q020](OPEN_QUESTIONS.md#q020), P 0 independent quality | Chosen-mixture coverage and exact/near/source independence; E005/E006/E007 before claiming independent performance. |

## E001–E018: proposed practical programme, not completed full audits

Recommended dependency order: **E015→E001/E002/E003→E004/E005→E006/E007→E008**, with **E014 in parallel**; E012/E013 close state/event gaps; E017 freezes uncertain GT; E016/E018 finalize the selected version. Each programme below is proposed even if a bounded W2 component touched it. Full inputs/versions/actions/metrics/artifacts/outcomes/limits are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). [P: F100](RAW_FACTS.md#f100), [F102](RAW_FACTS.md#f102).

| Programme | Inputs, action and saved evidence | Decision and success limit |
|---|---|---|
| E001 exact retrieval | Exact commit/revision/fileID registry; save HTTP/Range/advertised bytes/checksum origin; distinguish HTML/LFS/JSON error from data and prefix from full file; archive path safety/directory/CRC/SHA256; acquisition manifest/failure/retry log | Exact payload→E002; unavailable/gated→specific fallback/Q. Download does not prove rights/semantics/independence. |
| E002 pairing/decode | Exact media/labels; documented-ID/member-stem joins with case/collision checks; count missing/empty/orphan/decode errors, declared↔decoded W/H and hashes; PAIRS/QUARANTINE/DECODE/overlays | Use verified subset or obtain historical pixels; no silent CPPE 762 rescale/current-Pexels substitution/Construction `(1)` autojoin. Sample success does not cover all media or semantics. |
| E003 geometry/roundtrip | Exact categories/coordinates/decoded W/H and converter version; check origin/inclusive/xyxy/xywh/normalized-center; distinguish floating tolerance/material OOB; source→canonical→source per-object diffs/count/split/maxerror/IoU; converter commit/input-output hashes | Conversion/reject/derived clipping with original retained. SFCHD 50,552/SH17 228 comparisons are not full chosen-ingestion re-export; geometry is not class/coverage correctness. |
| E004 semantics/states | Target definitions and stratified pairs incl SH17 off/SHWD/SHELextra/CPPE/Pictor/Construction; pre-record selection reasons/strata/seed, two independent annotators+adjudication; unit/item/state/relation evidence, unknown/reject/disagreement by stratum, overlays/reasons | Usable mapping/new labels/quarantine; convenience sample gives no overall error rate; on not correct fit, agreement not certification. |
| E005 coverage/partial labels | Full-size source/target frames; double-annotate visible target objects, compare missed/out-of-scope/occluded/verified-absent, save coverage_by_dataset_class/status/adjudication/missed-false-unknown counts per defined sample | Choose dataset heads/loss masks/relabel/locally complete crops/exclusion. Small audit not full exhaustiveness; loss implementation→model_stack/training_strategy. |
| E006 duplicates | Selected original mix and parent links; file/canonical-pixel SHA256 then pHash/embedding candidates with crop/resize/flip/re-encode/burst/frame manual review; pair scores/decisions/reasons/contact sheets/connected groups | Group or quarantine ambiguous components. Zero exact matches does not prove independent session/video. |
| E007 groups/splits/locked test | Supplied IDs or nullable originals plus proxies; preserve official reproduction split, separately construct own group split/manual view merges; all derivatives/variants together; save intersections/unresolved provenance/class-scale coverage/holdout lock | Honest development/calibration/test roles; repeated tuning makes test development. Proxy split is not proof of new camera/site. |
| E008 target scale/transforms | Native target clips, permitted input contract and S048 donor distributions; label target head/person/PPE/cigarette with visibility/light; compare native/transformed width/height/area/min-axis for full frame/crop/tiles on same groups, save spec/histograms/overlays | Select preprocessing/observable scope; quality/latency require separate model/runtime experiment incl first-stage misses/crop context.640 not verified LinQ input; upscale adds no optics. |
| E009 generic fixtures | Actual COCO categories/pose, CrowdHumanODGT, MOTbase GT/media/instructions under terms; verify F/V/H/ignore/unsure/crowd/class filters/timestamps; group variants; subset/filter/log fixtures for switches/fragmentation/occlusion/cooldown | Local pipeline regression only, no PPE/event-quality claim; generic missing labels and CrowdHumanmask are not PPE GT. |
| E010 optional synthetic | Pinned PhysicalAI metadata join 282/157+action review; check directory/member/checksum/window-payload links, generator/scenario groups, visual artifacts/uncertainty; save actual counts/timing/visual/group evidence | Optional plumbing/augment or defer; metadata already joined but media not obtained. Successful synthetic test not real camera-hour holdout or public-asset grant. |
| E011 SARD schema | Author column/HOI/split definitions+linked 4.mp 4 excerpt/native FPS/frame offset+4.txt; overlay start/middle/end/occlusion, frame/coordinate/bounds/ID reset/class/action tests; schema/overlays/transitions/unresolved log | Bounded supplementary role or defer; raw IDs stay raw until proven. Unrelated Core clip/parser do not validate tracks; a few frames not nine videos. |
| E012 smoking/respirator pilot | Permitted native target clips/definitions, CPPE exact pixels and Zhang donor if obtained; subtype/visibility/person association, cigarette/hand/phone/face/head/confusers, separate flammable-policy context; double review/manual hashes/relations/uncertain intervals/agreement/observable coverage | Minimal trustworthy object/state/event GT or exclude nonobservable promise; no photo certification, no training/operational benchmark implied. |
| E013 zones/events/safe denominator | Eight Önal inputs for replay then continuous target/own footage; full review, policy_id/polygon/footpoint/tracks/visibility/ignore/onset-end/censored cuts/multiple actors/episode relations/cooldown; save events/polygons/manual intervals/reviewed camera-hours | Event recall/missed episodes/onset delay/repeat alerts in defined scope; false alerts/hour only from reviewed safe hours. Folder class/clip start is not onset, eight clips not long-run rate. |
| E014 action rights | Exact revisions/hashes/notices and owner clarification if needed; source-author/license/date/notice hash by code/labels/photos/assembly/article/weights×train/modify/publicraw-crop-demo/labels/weights/deploy; save matrix/answers | Permitted role/restricted delivery/own-organizer replacement/defer; no blanket commercial_ok, no guarantee of all third-party rights or automatic NC/SA/AGPL conclusion. |
| E015 organizer triage | Actual full case/files/terms; immutable inventory/timing/pairs/geometry/semantics/groups, locked target holdout before donors, development coverage/scale/confuser comparison; save intake assumptions/questions/lock protocol | Revise order and minimal target relabeling. No assumptions of size/quality; successful intake is not LinQ execution/realtime/accuracy proof. |
| E016 full selected integrity | Source/subset passing access/rights/semantics; apply E001–E007 to **every actually used record**, save actual paired-only class counts/dimensions/errors/quarantine/derived totals/split components/lineage | Reproducible chosen train/development revision, not all discovered datasets. Never rename bounded W2 checks as this full selected audit. |
| E017 uncertainty agreement | Target holdout/policy; two independent reviewers of visibility/state/boundaries, adjudication, separate object/person/event/unknown; frozen GT/version/change/review log, disagreement/not-observable by class/scale/light | Honest metric/claim scope, precision/recall only where GT supports it; human agreement cannot make an invisible property observable. |
| E018 manifest delivery roundtrip | Converted subset/schema; independent reconstruction of source class/name/bbox/media/group/split/reason, nullable IDs/checksum origin/transforms/exclusions; lost fields/remaps/untraceable crops/split-change counts and tolerances | Portable traceable delivery to downstream topics; provenance success not semantic/model/legal proof. |

## E019–E033: completed bounded checks and their limits

The following are already executed research checks. Their scope cannot expand merely because their subjects resemble E001–E018. [T: F003](RAW_FACTS.md#f003); detailed execution locators in [completed-check register](OPEN_QUESTIONS.md#реестр-уже-выполненных-bounded-checks-e019e033).

| ID | Actual coverage and result | Remaining limit |
|---|---|---|
| E019 | SH17 full manifest/stems; 13 released YOLO/228 mapped boxes;exact released 13376117; F006/F012/F013/F016 | No full released-label/semantic audit; not 13 release media pairs. |
| E020 | SH17 separate 13 raw/current-Pexels visual samples/contact sheets; F014–F016 | Targeted states, no error-rate estimate; historical pixels not guaranteed. |
| E021 | SFCHD full annotation equivalence/splits/OOB tolerance; F024–F031 | No full image/semantic validation. |
| E022 | SFCHD official media directory; 7 pairs/27 boxes;prefix/run overlap; F027/F032–F035 | Proxy groups not supplied camera IDs. |
| E023 | SHWD directory/4 splits/20 XML/8 JPEG; F043/F044 | Confirms head geometry, not ordinary-hat/completeness protocol. |
| E024 | CHV directory/map/splits/27 labels/4 JPEG; F047/F048 | Not 9,209 object recount/complete rights. |
| E025 | SHEL5K all 5,000 XML hash-matched; 4 new PNG plus 3 W1; F050–F055 | Remaining 4,993 PNG not checked; extra-person intention unresolved. |
| E026 | CPPEtar prefix/2 complete COCO/29 HFannotation comparison/2 PNG/author license comment; F057–F061 | Not full tar/source-photo inventory;762 quarantined. |
| E027 | Smoking primary PDF;Smoker 1,120 decodedRGB and 40 negative thumbnails; F063–F066 | Zero exact duplicates not source/subject independence; no Zhang data. |
| E028 | Önal 691 metadata entries/8 actual MP 4 container probes/frames; F068–F071 | Not event GT/continuous safe periods. |
| E029 | SARD 4.txtparser/ID-class analysis and bounded unrelated Core member; F072–F075 | No paired 4.mp 4/schema/validated tracks. |
| E030 | Bounded exact rights notices, corrected Zenodo identity; F018/F035/F060/F079/F083 | Not legal clearance/owner response. |
| E031 | Scale 132 groups/202,781 rows;SFCHD 0.1%table reproduction; F019/F037–F041/F062 | Declared frames, not model accuracy/target visibility/LinQ input. |
| E032 | Pictor 9 TXT/1 JPEG;Construction full ZIP/labels/4 semantic images; F080–F086 | Not full semantic QA/independence. |
| E033 | PhysicalAI deterministic 282 chunks/157 parents and primary terms read; F076–F079 | No media-member/visual/generator/scenario verification. |

Critic outcomes are preserved in [CRITIC.md](CRITIC.md): K005 closed only the critical SHWD head-geometry gate; K013 closed annotation-scale/threshold questions only. K001/K002/K004/K006/K008–K012/K014/K015 narrowed applicability; K003 localized membership/geometry/split contradictions; K007 explained count discrepancy. No criticism became a general dataset-fitness certificate; no hidden third wave or final auditor followed.

## Handoffs by topic

These are addressed knowledge transfers, not claims that neighboring reports exist or were read. Paths/content of other topic reports are unknown.

- **→ model_stack:** exact maps/coordinate formats, SHWD head geometry, SHEL multiple units/8 unresolved labels, CPPE 1-based→HF 0-based, Construction part-local no_*. Preserve source literal/unit/coverage/reversible mapping rather than only target ID. Implement converter/partial-label handling under E003/E005/E018; final IDs await case. [F008](RAW_FACTS.md#f008), [F025](RAW_FACTS.md#f025), [F044](RAW_FACTS.md#f044), [F054](RAW_FACTS.md#f054), [F058](RAW_FACTS.md#f058), [F085](RAW_FACTS.md#f085), [F097](RAW_FACTS.md#f097), [F101](RAW_FACTS.md#f101).
- **→ violation_methods:** object/on-off/person-attribute/event/policy distinctions; most donors lack associations/intervals; preserve blur/invisible unknown; exact respirator subtype/removal needs target layer. This determines associations/time conditions and uncertainty reaching operator. E004/E012/E013. [F002](RAW_FACTS.md#f002), [F014](RAW_FACTS.md#f014), [F020](RAW_FACTS.md#f020), [F061](RAW_FACTS.md#f061), [F065](RAW_FACTS.md#f065), [F070](RAW_FACTS.md#f070), [F073](RAW_FACTS.md#f073), [F098](RAW_FACTS.md#f098).
- **→ training_strategy:** SFCHD factory-adaptation/SH17 broad-object/SHEL separate-state/CPPE broad-face roles; selected-positive distributions/rare classes/partial coverage/domain and scale gaps/rights decide donor subsets, relabeling and loss masks. E004–E008/E014/E016; no donor benefit or specific loss was measured/implemented. [F005](RAW_FACTS.md#f005), [F008](RAW_FACTS.md#f008), [F023](RAW_FACTS.md#f023), [F055](RAW_FACTS.md#f055), [F062](RAW_FACTS.md#f062), [F100](RAW_FACTS.md#f100).
- **→ evaluation:** twoSFCHD val protocols/tiny-test overlap, proxy-group limits, parent lineages, Smoker 0 exact RGB groups with unknown subjects/sessions, selected Önal clips without safe-hours denominator, train-only synthetic. Lock target holdout; separate object/person/event units and uncertain GT; E006/E007/E013/E017. [F009](RAW_FACTS.md#f009), [F022](RAW_FACTS.md#f022), [F030](RAW_FACTS.md#f030), [F032](RAW_FACTS.md#f032), [F063](RAW_FACTS.md#f063), [F070](RAW_FACTS.md#f070), [F076](RAW_FACTS.md#f076), [F099](RAW_FACTS.md#f099), [F102](RAW_FACTS.md#f102).
- **→ linq_platform/video_architecture:** eight hashed 1080p H.264 Önal inputs with variable native timing and donor scale distributions can support representative development replay/decode/calibration once real input contract is known. Check transfer/display actions separately;640 input and LinQ latency/performance unestablished. E008/E015. [F037](RAW_FACTS.md#f037), [F040](RAW_FACTS.md#f040), [F041](RAW_FACTS.md#f041), [F069](RAW_FACTS.md#f069), [F071](RAW_FACTS.md#f071), [F102](RAW_FACTS.md#f102).
- **→ operator_product/hackathon_strategy:** exact respirator/removal, smoking-near-flammables and site-policy zones lack complete target GT. Clip class is not every actor's state; retain unknown through interface/review. Scope/demo claims await observability/holdout. Q001–Q003/Q012–Q014, E012/E013/E017. [F001](RAW_FACTS.md#f001), [F004](RAW_FACTS.md#f004), [F066](RAW_FACTS.md#f066), [F070](RAW_FACTS.md#f070), [F098](RAW_FACTS.md#f098), [F102](RAW_FACTS.md#f102).
- **→ market_deployment:** preserve layer/action-specific notices and unknown permissions for public delivery/demo/deployment negotiations; no single commercial_ok. Q003/E014; exact source conditions in SH17/SFCHD/SHWD/CHV/SHEL/CPPE/Smoker/Önal/PhysicalAI/Pictor/Construction sections. [F018](RAW_FACTS.md#f018), [F035](RAW_FACTS.md#f035), [F045](RAW_FACTS.md#f045), [F049](RAW_FACTS.md#f049), [F055](RAW_FACTS.md#f055), [F060](RAW_FACTS.md#f060), [F064](RAW_FACTS.md#f064), [F071](RAW_FACTS.md#f071), [F079](RAW_FACTS.md#f079), [F082](RAW_FACTS.md#f082), [F083](RAW_FACTS.md#f083).

**No training, model-quality measurement, target-CCTV transfer test or LinQ throughput/latency measurement was performed.** The next dataset version begins with actual organizer intake/locked target holdout and adds external data for a demonstrated gap, preserving source identity, uncertainty and action conditions. [T/U/P: F003](RAW_FACTS.md#f003), [F100](RAW_FACTS.md#f100), [F102](RAW_FACTS.md#f102).
