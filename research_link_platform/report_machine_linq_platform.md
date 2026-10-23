---
topic: linq_platform
scope: >-
  LinQ/IVA H1 hardware and software, public access and delivery evidence, model
  export/import/PTQ/compilation/runtime contracts, video integration, execution
  proof, published performance, conditional implementation routes and experiments
  for the 2026 industrial-safety video hackathon. Evidence is limited to saved
  public sources, actual public-model CPU runs and isolated host helper/mock probes.
not_covered:
  - "model_stack: exhaustive model/weight search, training and final detector selection"
  - "Data research: acquisition, annotation and a completed case-specific dataset"
  - "Architecture/product research: final service implementation, market and competition strategy"
  - "Unissued full case, proprietary SDK internals and actual LinQ device validation"
answers:
  - "What are LinQ H, IVA H1, H1M, HP, HPD, HPQ, HPS, HPC and HX?"
  - "How does a trained model become a .qm and a runnable .tpu?"
  - "Which components, versions, dependencies and licenses were actually obtained?"
  - "Which detector candidates have concrete evidence, and at what level?"
  - "What is known about ONNX operators, opset/IR, shapes, batch and output contracts?"
  - "What can CPU/RTX preparation establish before SDK/device access?"
  - "Which online access modes can support our own model and its updates?"
  - "Where can video decode, preprocessing, NMS, tracking and rules execute?"
  - "What do published FPS/latency results establish about our service?"
  - "Which source defects and integration failures should be diagnosed first?"
  - "Which experiments should run before access and during the first hours?"
  - "Which expert answers change the implementation route first?"
  - "How can request completion on LinQ and whole-graph coverage be proved separately?"
  - "Which implementation routes are viable under different actual grants?"
  - "What exact constraints and artifacts should neighboring research receive?"
keywords:
  - LinQ
  - Linq TPU
  - IVA H1
  - LinQ H1M
  - К1945ВМ3Я
  - HP1M-01
  - HP1M-02
  - HPD1M
  - HPQ
  - HPS
  - HX
  - tpu_framework
  - pytpu
  - libtpu.2.so
  - onnx_direct
  - dnn_quant
  - TLM
  - GraphDef
  - ModelProto
  - .qm
  - .tpu
  - percentile
  - DEFAULT
  - STAGING
  - O1/O5
  - RAW/FULL
  - TinyYOLO3
  - YOLOv8
  - YOLOv5su
  - YOLO11
  - DFL
  - 4+nc
  - 5+nc
  - NMS
  - Squeeze
  - IVA CV
  - stream_epoch
  - partial fallback
entity_schema:
  routes:
    id: "Stable R001-R008, with an explicit HTML anchor"
    fields: [conditions, actions_and_checkpoints, outcomes_and_limits, questions]
  experiments:
    id: "Stable E001-E020, with an explicit HTML anchor"
    fields: [decision_and_prerequisites, actions_and_artifacts, outcomes_and_limits, evidence_and_questions]
takeaways:
  - "The issued access mode and ability to upload/update a custom model remain unknown (Q001-Q005); a suitable service can suffice without SSH."
  - "The 2025 guide, 2026 benchmark stack and legacy public Python bindings are different version contexts, not a reproducible combined installation."
  - "opset13/static batch1/no NMS are exporter choices, not established LinQ limits; current frontend and ABI support remain unknown."
  - "Custom-class adapters must distinguish decoded 4+nc, classic 5+nc, raw heads and post-NMS outputs; the inspected COCO heuristic fails nc1/2/3."
  - "Actual TinyYOLO3 CPU runs and weight comparisons exist, but anchors, NMS, geometry and batch prevent whole-model parity claims."
  - "Effective percentile, quantizer numerics, FULL/RAW conversion and present runtime guarantees require the matching supplied release."
  - "Prove compiler lineage/coverage and per-request device completion separately; utilization and a UI badge do not establish both."
  - "No proprietary SDK install, vendor conversion/PTQ/compile/TLM or LinQ inference occurred; CPU/RTX preparation does not meet the mandatory LinQ condition."
checked_at:
  date: "2026-10-23"
  source_check_window: "04:15-05:14"
  timezone: Europe/Moscow
  utc_offset: "+03:00"
  meaning: "Saved evidence acquisition/check window; report writing added no external verification."
historical_context: "Preparation on the night of 23 October 2026; published full-case-to-submission window is 45 hours."
case_status: "Public short brief and schedule only; full case, datasets, organizer files and issued access configuration were unavailable. Signup outcome was not reported."
hardware_access: "No actual LinQ access; issued SKU, quota, topology and device identity unknown."
sdk_access: "Public guide text, pinned third-party source and legacy public sdists inspected; no proprietary matched SDK/native/driver/firmware bundle obtained or installed."
tested_here:
  - "Public Model Zoo TinyYOLO3: ONNX Runtime 1.31.0 CPUExecutionProvider; synthetic b1 succeeds, selected b2 fails at Squeeze; diagnostic raw-head derivative b1 succeeds."
  - "Actual ONNX/Darknet binary inspection: 13 convolution kernels and two final biases match exactly; 11 BN affine transformations checked under epsilon .001 hypothesis."
  - "Python shape/schema, dtype/Unicode/geometry and historical device-listing-expression probes; CPython 3.11.9/NumPy 2.4.2 fake-native lifecycle and host-memory ownership probes."
  - "Saved source/archive/metadata reading and PDF text extraction; original PDF page images were not visually inspected."
  - "Not performed: proprietary install, vendor conversion/calibration/compile/TLM, custom strict export, LinQ inference or service/video deployment."
human_report: report_human_linq_platform.md
evidence_files: [SOURCES.md, RAW_FACTS.md, CRITIC.md]
unresolved_file: OPEN_QUESTIONS.md
---

# LinQ platform: engineering decisions and evidence boundaries

## Evidence tags, provenance and hard case constraints

**[DOC]** denotes manufacturer technical documentation; **[SRC]** versioned source/metadata inspection; **[CLAIM]** a product or author assertion; **[REPORTED]** somebody else's measurement; **[LOCAL]** an actual saved host run, with its scope stated; **[ANALYSIS]** engineering inference or proposed application policy; **[UNKNOWN]** an unresolved capability, not a declaration of non-support. Linked F records carry normalized evidence and S locators. E IDs are future experiments; R IDs are conditional routes. The 174 S records (166 external URLs + 8 local/derived locators), 333 F records, 35 Q records and 20 K dispositions are not independent confirmations. GitHub LFS and its matching mirror are one artifact lineage. Repeated reading of one author's code is not device corroboration. [SRC, LOCAL: F333](RAW_FACTS.md#f333), [K018](CRITIC.md#k018-w2).

**[DOC]** The public case is industrial-safety video analysis on LinQ, with online accelerator access promised. Missing helmet, removed respirator, dangerous-zone entry and smoking near combustible material are examples, not the confirmed complete class list. Mandatory NN boundaries, own-weight requirements, camera counts, latency targets, event rules and accepted execution proof are unknown: [F302](RAW_FACTS.md#f302), [Q005](OPEN_QUESTIONS.md#q005), [Q029](OPEN_QUESTIONS.md#q029), [Q030](OPEN_QUESTIONS.md#q030). CPU/RTX training and reference work do not replace mandatory LinQ inference.

**[DOC/context]** The published 2026 schedule gives full tasks 23 October 13:00, opening 16:30, checkpoints 23 October 18:00 and 24 October 11:00/18:00, pitch review 24 October 19:00-19:45, submission 25 October 10:00, defenses 12:00-17:30: 45 hours from full task to deadline. Do not transplant 2025 memo dates. No compile-time budget such as “30-60 minutes” was measured. Team context: five experienced participants, RTX 4070, laptop and possible cloud GPUs; OS, VRAM, installed packages and remote hosts are unspecified. This research prepares checks rather than implementing a competition submission. [F034](RAW_FACTS.md#f034), [S035](SOURCES.md#s035).

**[UNKNOWN]** The decisive architectural issue is the actual grant: shell/container, graph-to-compile service, `.tpu` upload, jobs/files, managed video, or catalog only. A custom-model service with version control, outputs and accepted LinQ evidence can suffice without SSH. SSH alone does not supply compiler permissions, device access, camera reachability or persistent workers. Signup outcome is unreported; no current SDK/device grant can be inferred. [F309](RAW_FACTS.md#f309), [F312](RAW_FACTS.md#f312), [Q001](OPEN_QUESTIONS.md#q001).

## LinQ H / IVA H1 / H1M hardware: products, revisions and memory

**[DOC]** LinQ belongs to ООО «ХайТэк», INN `7722826409`. Current `hi-tech.org` identifies «Хайтэк-Интеграция», INN `7722350688`; an old PDF URL returning HTTP 200 HTML does not recover the old document. The [software page](https://lin-q.ru/sol) explicitly links IVA H1 and LinQ H; the presentation links H1M to `К1945ВМ3Я`. Names “LinQ H1” framework and “LinQ H1М” hardware identify a lineage, not universal binary/API compatibility. Historical `FW_TPU_H` and `FW_TPU_E` were distinct products. [F001](RAW_FACTS.md#f001), [F005](RAW_FACTS.md#f005), [F006](RAW_FACTS.md#f006), [F214](RAW_FACTS.md#f214), [F275](RAW_FACTS.md#f275).

**[DOC, revision unspecified]** The [technical page](https://lin-q.ru/tech) describes LinQ H: 28 nm, BGA1296, 128×128 systolic array, primary int8, 16 MB on-chip memory, DDR4+ECC up to 32 GB, control RISC-V, 500-812 MHz, PCIe Gen3 endpoint x8. Chip limits are not the installed board configuration; TOPS cannot establish this detector's latency or camera capacity. [F002](RAW_FACTS.md#f002).

| Product | Documented configuration [DOC] | Consequential boundary |
|---|---|---|
| HP / `HP1M-01` | One H1M; DDR4 ECC 16 GB, 2×8 GB; PCIe 2.0 x8; manual ≤35 W | Separate from -02; actual issued SKU unknown |
| HP / `HP1M-02` | One H1M; DDR4 ECC 32 GB, 2×16 GB; PCIe 2.0 x8; ≤35 W | No established chronological transition from -01 |
| HPD / `HPD1M-00 Active`, `-01 Passive` | Two H1M; 32 GB total, 16 GB/chip; PCIe 3.0 x16; manuals ≤100 W | Two devices do not establish a shared graph memory pool |
| HPQ / `HPD1M-10 Passive`, `-11 Active` | Four H1M; 64 GB total, 16 GB/chip; PCIe 3.0 x16; ≤150 W | Prefix HPD1M without suffix does not identify chip count |
| HPS | Separate multi-accelerator system; cloud/containerization and optional video equipment claimed | Not a specification of the hackathon server/decoder |
| HPC / HX | HPS-based compute complexes and a separate integrated HX platform | HX video/PyTorch/ONNX requirements do not transfer to HP/H1 |

Sources: [F009](RAW_FACTS.md#f009), [F271](RAW_FACTS.md#f271), [F272](RAW_FACTS.md#f272), [F273](RAW_FACTS.md#f273), [F274](RAW_FACTS.md#f274), [F329](RAW_FACTS.md#f329). **[UNKNOWN]** The catalog's generic HP1M-02 link still leads to a 16 GB/Gen3 technical description. Chip Gen3 capability and a particular board's Gen2 link can coexist; the catalog mismatch remains unresolved. Power claims also differ: presentation HP/HPD/HPQ `<30/<55/<105 W`; manuals `≤35/≤100/≤150 W`; HPD technical description `60/70 W`. Fan choice cannot explain all differences because passive HPD also has a 100 W limit. Preserve mode/scope instead of selecting the convenient figure. [F275](RAW_FACTS.md#f275), [Q033](OPEN_QUESTIONS.md#q033).

**[SRC/ANALYSIS]** Obtain `physical card → chip → PCIe endpoint → runtime device ID → team quota`. Four `/dev/tpu*` nodes under somebody else's HPD label do not establish topology. The inspected parallel script loads identical programs on separate devices and splits images among workers: replication. Compiler slicer scheduling and tensor placement across DDR do not establish cross-chip graph partitioning or pooled capacity. Test supported partitioning only with the vendor's explicit example; replication E013 and single-graph E020 answer different questions. [F276](RAW_FACTS.md#f276), [F277](RAW_FACTS.md#f277), [F279](RAW_FACTS.md#f279), [F280](RAW_FACTS.md#f280), [Q016](OPEN_QUESTIONS.md#q016), [Q017](OPEN_QUESTIONS.md#q017).

## SDK access, components, environments and rights

**[DOC/SRC]** Framework prepares/imports/PTQs/compiles; runtime loads and executes `.tpu`; native library, driver and firmware are separate layers. TLM is a documented hardware model/simulator, not a confirmed supplied component. Model Zoo, cloud access and IVA CV are separate products or delivery options. A public manual is not the SDK. [F210](RAW_FACTS.md#f210), [F329](RAW_FACTS.md#f329).

| Component/context | Exact observed version/requirements | Actual availability and limit |
|---|---|---|
| IVA H1 operator guide | 2025, `RU.РМДВ.04.06.014-03`; Ubuntu 20.04, Python 3.11, RAM ≥32 GB | Public [guide](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf) text; example `tpu_framework-py3-none-any.whl` not obtained; lock unknown [DOC] |
| 2026 vendor benchmark | TPU Framework `2026.8.43`, TPU Runtime `16.18.6`, Ubuntu 24.04, Intel Core i7-10700K | Presentation text, not issued SDK; Python/TF/native/driver pairing undisclosed [REPORTED] |
| Website API/CLI | Python 3.8, OEM, LinQCompiler/DNNQuant/Model Zoo | Undated software-page statements [CLAIM] |
| Historical 2021 guide | Ubuntu 18.04+, Python 3.8.6, TF 2.4.1, CUDA 11.0, cuDNN 8.0, GCC 7.3.1 | Historical generation, not a current installation recipe [DOC] |
| `pytpu` | `15.0.24`, uploaded 2023-11-27; Python ≥3.6, NumPy; `/usr/lib/libtpu.2.so` | Actual sdist/metadata/hash read; native binary absent; no current ABI guarantee [SRC] |
| Older bindings | `14.7.0` (2023-04-11), `13.0.13` (2021-12-01) | Actual source archives; historical async/helper/native loader [SRC] |
| `iva_applications` | `11.0.1`, uploaded 2021-10-13 | Host helpers and actual MIT LICENSE; no compiler, weights or Tiny `.tpu` [SRC] |
| `onnx_direct`, `dnn_quant`, compiler, TLM | Names and call sites in guide/source | Current distributions, precise APIs and pairing unknown [DOC/UNKNOWN] |
| Third-party `linq-cv-bench` | Commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140` | Saved [repository](https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140); not a manufacturer SDK or full successful custom-model protocol [SRC] |

Evidence: [F004](RAW_FACTS.md#f004), [F207](RAW_FACTS.md#f207), [F210](RAW_FACTS.md#f210), [F329](RAW_FACTS.md#f329). The third-party venv uses Python 3.11, NumPy `1.26.4`, ONNX approximately `1.16`, ORT approximately `1.18`, TF `2.14.1`; Torch is unpinned, ultralytics separately imported and absent from common requirements. TPU requires preinstalled `libtpu / tpu-dkms / pytpu / tpu_framework / mlperf`. `pip install -r requirements.txt` does not reproduce the whole stack. `py3-none-any` describes one wheel, not universal native/Windows/WSL/ARM support. Do not combine dependency lists from different generations. [SRC: F207](RAW_FACTS.md#f207), [UNKNOWN: Q006](OPEN_QUESTIONS.md#q006).

**[DOC/UNKNOWN]** [Public docs](https://lin-q.ru/docs) and [software downloads](https://lin-q.ru/sol) have different availability. Downloads require registration **and verification**; device permission is a further grant. Only read-only access investigation and user guidance occurred; no automatic registration/messages/private cabinet access. Verification mechanism/duration and user outcome remain unknown. [F198](RAW_FACTS.md#f198), [F199](RAW_FACTS.md#f199), [F200](RAW_FACTS.md#f200), [Q001](OPEN_QUESTIONS.md#q001).

**[ANALYSIS/UNKNOWN]** Separate compilation on a CPU host is a useful hypothesis because `.tpu` and runtime are separate stages. Requirements omitting a board, or deferred imports in old wrappers, do not prove current compiler independence from native libraries, driver, license, network or device. E007 must establish it. A compile service might remove the need for any local proprietary SDK. [F208](RAW_FACTS.md#f208), [Q007](OPEN_QUESTIONS.md#q007).

**[SRC/UNKNOWN]** Rights are per layer. `iva_applications-11.0.1` contains MIT LICENSE, copyright 2020 IVA Technologies: preserve notices when using/modifying those helpers. No explicit LICENSE was found in the inspected pytpu archive; `UNKNOWN` metadata does not license the closed native library. Model Zoo cards/root have conflicting MIT/Apache-2.0 labels. SDK images, weights, `.tpu`, IVA CV and redistribution to five participants need actual supplied terms; commercial pricing is neither a grant nor proof of an execution ban. [F203](RAW_FACTS.md#f203), [F205](RAW_FACTS.md#f205), [F250](RAW_FACTS.md#f250), [F300](RAW_FACTS.md#f300), [Q026](OPEN_QUESTIONS.md#q026), [Q035](OPEN_QUESTIONS.md#q035).

## Model → ONNX/GraphDef → .qm → .tpu: documented preparation path

**[DOC, 2025 guide; not executed here]** The most explicit path is:

1. Frozen TensorFlow `GraphDef` or ONNX `ModelProto`, including weights.
2. `onnx_direct.onnx_to_tf` converts ONNX to a TensorFlow representation plus name mapping.
3. Quantizer consumes graph, named input shapes, output nodes and calibration ndarray data; `.qm` stores topology and numeric information.
4. `Network.from_quantized_model` builds compiler representation; compilation uses explicit target, parameters and optional tensor placement.
5. `TpuProgram` combines executable representation and tensor descriptions; `to_file` writes `.tpu`.
6. Runtime enumerates/opens a device, loads `.tpu`, creates inference and executes named input tensors.

Direct ingestion of `.pt`, state_dict, TorchScript, Keras H5 or SavedModel directory through this API is not established. PyTorch-through-ONNX is advertised. ONNX is not shown as `Device.load` input; `.qm`, quantized TF graph and `.tpu` are distinct artifacts. Current frontend may differ from this guide: [F052](RAW_FACTS.md#f052), [F053](RAW_FACTS.md#f053), [F329](RAW_FACTS.md#f329), [Q008](OPEN_QUESTIONS.md#q008).

**[DOC/SRC]** Guide presets `DEFAULT` and `STAGING`: start new networks with DEFAULT; STAGING may compile for a long time or generate incorrect programs. Third-party `O1/O5` are not proved equivalent. Select actual target such as `128x128_asic` from supplied release; guide `as_graph` default `64x64_fpga` is an unresolved seam, not a safe ASIC default. [F072](RAW_FACTS.md#f072), [F276](RAW_FACTS.md#f276), [Q010](OPEN_QUESTIONS.md#q010).

**[SRC/UNKNOWN]** Guide/source seams remain: converter pair “graph + mapping” versus single assignment; `tf.Graph` versus required GraphDef; `.qm` `save(file_path)` versus `save(file_dir,file_name)`; tuple unpacking of `Network.from_quantized_model`; exact compile-call assignment and tensor names. Use one matched complete example, actual types/signatures and mapping. Do not invent an executable recipe from incompatible fragments. [F218](RAW_FACTS.md#f218), [F219](RAW_FACTS.md#f219), [Q010](OPEN_QUESTIONS.md#q010).

**[SRC, correction]** TF `2.14.1` source confirms `tf.graph_util.import_graph_def` exists and `Session(graph=None)` uses the default graph; the early inevitable-crash suspicion was false. Import defaults to namespace `import` and returns None without `return_elements`, so naming/reimport issues remain. TF 2.14.1 is an inspected upstream/third-party version, not a vendor requirement. Extracted `ModeProto` is suspicious against `ModelProto`, but no PDF-page visual inspection established a printed typo. PDF images of guide/presentation/IVA CV were not inspected; alternative text extraction and a remote text response do not count as visual verification. [F211](RAW_FACTS.md#f211), [F215](RAW_FACTS.md#f215), [F216](RAW_FACTS.md#f216), [F217](RAW_FACTS.md#f217), [K003](CRITIC.md#k003-w2).

**[ANALYSIS]** Give each boundary its own `PASS / FAIL / UNAVAILABLE / NOT_RUN`, immutable input hash and first error. ONNX checker proves format validity, not importer support; float import success does not prove parity; PTQ parity does not prove compilation; `.tpu` creation does not prove correct device execution or whole-graph coverage. [F232](RAW_FACTS.md#f232), [F291](RAW_FACTS.md#f291).

## Detector candidates: source availability is not validated LinQ compatibility

**[ANALYSIS]** Distinguish a family listing, reported benchmark, exporter/build/runner source, obtainable graph/weights, exact successful conversion/compilation, device numerical parity and case quality. None substitutes for the next. Detection, pose, segmentation and OBB are different tasks. No custom detector completed the LinQ pipeline here. [F330](RAW_FACTS.md#f330), [Q020](OPEN_QUESTIONS.md#q020).

| Candidate | Strongest concrete evidence | First unresolved boundary |
|---|---|---|
| Vendor TinyYOLO3 | Author runner/scenario reports HP/HPD success with `tiny_yolo3_b8_o5_128x128_asic.tpu` [SRC/CLAIM] | Actual binary/hash/checkpoint/I/O/golden unavailable |
| YOLOv8n/s detection | Detailed pinned exporter/build/runner; default v8s, 640, opset13, no NMS [SRC] | Author weights/ONNX/.qm/.tpu/success logs absent; exact ultralytics version unpinned |
| Classic `yolo5s` | Vendor b1 `106,1 FPS` HP [REPORTED] | Exact weights/export/input/task unknown; relation to YOLOv5 v7.0 unproved |
| YOLOv5su | Historical 2026-02-27 `yolov5su.pt` author script [SRC] | Objectness-free variant, not classic vendor yolo5s; skeleton is not successful execution |
| YOLO11 detection | Family on site, configuration/control head in source [CLAIM/SRC] | Need a supplied matched ordinary-box detection example |
| YOLO11l OBB | University abstract reports 20 FPS from earlier bench records [REPORTED] | No full protocol or repeat bench; not horizontal PPE detection |
| `yolov8n_pose` | Vendor b1 HP `104,8 FPS`, `21,51 ms` [REPORTED] | Pose task; input/quality/timing scope unknown |
| FCNResNet50 | torchvision `COCO_WITH_VOC_LABELS_V1`, 21 labels, NCHW 520 source [SRC] | Negative final O5 note; not vendor `FCN_8s`; no successful final artifacts/logs |
| Custom ResNet50 | `IMAGENET1K_V2`, 224, NHWC uint8 wrapper with internal normalization [SRC] | Not vendor `resnet50_mlperf`; no author binaries/logs |

Detailed model matrix: [F330](RAW_FACTS.md#f330); history/provenance: [F233](RAW_FACTS.md#f233), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [F236](RAW_FACTS.md#f236). The university publication is separate authorship, but measurement independence from vendor data is unproved. The current author scenario reports Tiny success, not custom YOLOv8 success. Earlier text distinguishes acceptable quality and MLPerf `INVALID` at qps400; expectation of `VALID` at qps2000 does not replace LoadGen logs. Missing binaries/logs are [Q034](OPEN_QUESTIONS.md#q034).

**[ANALYSIS]** A conditional shortlist can retain v8 for detailed source, classic5s for a concrete vendor benchmark once artifact identity is established, and YOLO11 after a matched sample. Do not choose solely by novelty or claim v8s is proven superior. Require reproducible export, understood outputs, an available compilation path and small-PPE quality. [F330](RAW_FACTS.md#f330), [K005](CRITIC.md#k005-w2).

## ONNX opset/IR, dynamic shapes and Ultralytics output boundaries

**[UNKNOWN]** `opset13`, static batch1 and `nms=False` are third-party exporter defaults, not established LinQ ceilings. Exporter flags allow alternatives. Site `PyTorch ≥2.0.0` / `ONNX ≥1.15.0` belongs to HX; ONNX package version is neither model opset nor IR. No versioned current LinQ frontend matrix was obtained for domains, attributes, dtypes, external data, functions, control flow or Q/DQ; modern Framework `2026.8.43` lowering remains unknown. [F220](RAW_FACTS.md#f220), [F228](RAW_FACTS.md#f228), [F230](RAW_FACTS.md#f230), [Q008](OPEN_QUESTIONS.md#q008).

**[SRC/ANALYSIS]** Inventory the actual ONNX: all opset imports/domains, IR, functions, initializers/external data, I/O, nodes and attributes. `Resize` needs mode/coordinate transformation/nearest/scales-or-sizes; `Softmax` needs schema version/axis; `Reshape` needs shape tensor/zero semantics. An omitted attribute can inherit a schema-specific default. Generic NPU “difficult operators” do not establish LinQ prohibitions. Reduce the actual failing graph, retaining constants, attributes and golden output. [F228](RAW_FACTS.md#f228), [F232](RAW_FACTS.md#f232).

**[SRC, Ultralytics v8.3.0 standard Detect]** `nms=False` retains DFL, decode, stride and class sigmoid **inside** the inference graph. Ordinary detection output is decoded `(B,4+nc,A)`: xywh in prepared-input pixels and class probabilities without separate objectness. At 640, A is commonly 8400 but depends on actual feature maps. Do not repeat DFL/sigmoid/stride externally. Raw convolution heads are another export; pose/segmentation/OBB carry additional fields and need their own adapter. v8.3.200 `nms=True` uses a separate NMS wrapper; exact behavior cannot be assigned to the unavailable author's unpinned ONNX. [F223](RAW_FACTS.md#f223), [F224](RAW_FACTS.md#f224), [F226](RAW_FACTS.md#f226), [F238](RAW_FACTS.md#f238).

**[ANALYSIS]** If the frontend fails near DFL/decode, a separately versioned pre-decode wrapper plus host decode can be investigated. It changes the graph and NN boundary; verify the full numerical chain and organizer acceptance of host work. It is not a proved workaround. [F224](RAW_FACTS.md#f224), [Q005](OPEN_QUESTIONS.md#q005).

**[SRC]** `force_static_onnx_input_shape` changes only four dimensions of one `graph.input` to `(1,3,H,W)`. It does not rebuild internal Constant/Reshape/grids/anchors/outputs/value_info. Changing H/W calls for complete re-export and parity; input-header patching is only a labeled diagnostic control. Separate `network.set_batch` programs for 1 and 8 are not one dynamically batched executable. Symbolic N is not an executable-b2 guarantee. [F221](RAW_FACTS.md#f221), [F225](RAW_FACTS.md#f225), [LOCAL counterexample: F247](RAW_FACTS.md#f247), [Q009](OPEN_QUESTIONS.md#q009).

## Custom-class adapter: 4+nc versus 5+nc, NMS and class mapping

**[LOCAL, shape-only]** The pinned runner's COCO84/85 axis heuristic rejects `(1,5/6/7,8400)` for nc1/2/3, accepts `(1,85,8400)`, wrongly transposes `(1,6,84)` to `(1,84,6)`, and silently accepts ambiguous `(1,84,84)`. This was an actual Python helper probe without model, NumPy, torch NMS or TPU. A corrected production adapter and full NMS tests remain unimplemented. [F239](RAW_FACTS.md#f239), [S172](SOURCES.md#s172).

**[SRC]** Classic YOLOv5 v7.0 uses `(B,A,5+nc)` with objectness×class probability. Modern v8.3.0/v8.3.200 NMS expects `(B,4+nc,A)` without that multiplier. Classic obj=.1 and class=.9 must score `.09`; interpreting it as modern can yield `.9` and shift class index, changing admission at threshold `.25`. 85 channels can mean classic 5+80 or modern 4+81; explicit `nc=80` does not make classic85 compatible. [F237](RAW_FACTS.md#f237), [F238](RAW_FACTS.md#f238).

**[SRC]** Inspected NMS has a shortcut `prediction.shape[-1]==6` for already-detected BNC outputs; ordinary synthetic tests should use A≠6 and separately cover A=6. NMS mutates coordinates in place: retain/copy raw outputs before comparison. v8.3.0 places NMS in `utils.ops`; runner imports `ultralytics.utils.nms`, so pinning 8.3.0 alone does not fix import. Record actual package/source/import, conf/iou/agnostic/multi_label/max_det/max_nms. [F240](RAW_FACTS.md#f240), [F241](RAW_FACTS.md#f241).

**[SRC/LOCAL helper]** Other host defects: partial name override loses the second summary name; invalid JSON silently falls back to heuristics; first rank≥3 output is selected; `COCO80_TO_91` is applied to custom classes and cls≥80 can be discarded. Unicode attribute `args.output_tens\u0e2d\u0e23\u0e4c_name` differs from parser `output_tensor_name`, predicting AttributeError before device access. The dtype helper maps a `uint8` descriptor to int8; geometry probes used 1920×1080 and 641×479 formulas without running OpenCV pixels. Fixing the typo alone does not fix schema, dtype, mapping or geometry. [F241](RAW_FACTS.md#f241), [F242](RAW_FACTS.md#f242), [F333](RAW_FACTS.md#f333), [S173](SOURCES.md#s173).

**[ANALYSIS/specification]** Require explicit task/schema/layout/nc/names/category map and all output names from the shared model manifest. Validate `4+nc` for decoded modern heads, `5+nc` for classic heads, separate `(k,6)` post-NMS contract, or all raw heads with anchors/strides. Reject ambiguity with tensor descriptors instead of guessing. E003 covers nc1/2/81, both axis orders, overlaps/empty cases, class-aware suppression, name overrides and rectangular inverse geometry. [F242](RAW_FACTS.md#f242), [E003](#e003).

## TinyYOLO3: actual binary lineage, CPU results and non-parity

**[SRC/LOCAL]** Three objects must remain separate: unavailable vendor `.tpu`; source-only “strict” Darknet cfg/weights exporter (not run here); downloaded Model Zoo ONNX, actually inspected and executed on CPU. “Strict” is a source filename/recipe, not a measured parity status. [F243](RAW_FACTS.md#f243), [F251](RAW_FACTS.md#f251).

| Boundary | Vendor path as assumed by runner [SRC/CLAIM] | Strict exporter source [SRC] | Actual Model Zoo ONNX [LOCAL] |
|---|---|---|---|
| Artifact | `tiny_yolo3_b8_o5_128x128_asic.tpu`, external author path | Darknet → Keras/tf2onnx, opset13 | `35 511 756` bytes; opset11, IR6, keras2onnx1.6.0 |
| Input | float32 NHWC `(8,416,416,3)`, 0..1 assumed | NHWC `(None,416,416,3)`, optional fixed batch | `input_1`: NCHW float; `image_shape`: float `(N,2)` |
| Output | Heuristic rank3 or two rank4 heads; actual descriptor unknown | Two pre-decode/pre-NMS heads | Boxes, scores, embedded-NMS indices |
| Fine anchor mask | Assumes `0,1,2` | Darknet cfg `0,1,2` | Proved `1,2,3` |
| NMS | Host score .001, IoU .45, global max300 defaults | Outside graph | Score `.6000000238418579`, IoU `.5`, max20 per class |
| Batch | Runner default 8, binary contract unverified | Export not executed | Actual b1 passes; selected b2 fails |

**[LOCAL]** The actual Darknet weights consumed `35 434 956` bytes, the whole file. Exactly 13 convolution kernels and two final biases match Model Zoo. Eleven BN layers satisfy the tested affine-transformation algebra under epsilon `.001` hypothesis; this is not equality of all parameters or numerical parity with a strict export. Default TF/Keras numerics and actual strict export remain untested. GitHub LFS pointer and HF binary match hash/size: mirror, not independent model evidence. [F244](RAW_FACTS.md#f244), [F245](RAW_FACTS.md#f245), [F333](RAW_FACTS.md#f333).

**[LOCAL graph/SRC upstream]** Fine-head anchors are `(23,27),(37,58),(81,82)` in Model Zoo; Darknet mask `0,1,2` starts with `(10,14)`. Zero wh logits therefore yield first fine box 23×27 versus 10×14 despite identical logits. Actual initializers/edges prove the difference; keras-yolo3 explains mask `[[3,4,5],[1,2,3]]`. AP impact was not measured; card mAP `.331` is not our evaluation. [F246](RAW_FACTS.md#f246).

**[LOCAL, ORT `1.31.0`, CPUExecutionProvider]** Synthetic constant b1 at 416 yielded float32 `(1,2535,4)`, float32 `(1,80,2535)`, int32 NMS indices `(1,0,3)`, where 2535 = 3×13² + 3×26². Empty selected indices on this synthetic input are not poor-quality evidence. `(2,3,416,416)` with `image_shape (2,2)` fails at `TFNodes/yolo_evaluation_layer_1/Squeeze`: dimension 0 must be 1, got 2. This is a full-graph combination failure, not a general raw-backbone batch prohibition. An in-memory diagnostic derivative keeping ancestors of the two conv heads and removing image_shape/decode/NMS passes b1 with finite `(1,255,13,13)` / `(1,255,26,26)`. It is a different graph. [F247](RAW_FACTS.md#f247), [F328](RAW_FACTS.md#f328).

Actual graph inventory includes 13 Conv, 11 BatchNormalization, 11 LeakyRelu, 6 MaxPool, 1 Resize, 15 Concat, 4 Loop and 1 NonMaxSuppression; full exact inventory is [F328](RAW_FACTS.md#f328). Inventory is not a LinQ operator-support claim. The original graph's image_shape participates in geometry; the diagnostic derivative does not validate full-graph b2 or strict parity.

**[LOCAL protocol]** The saved CPU run time is `2026-10-23T02:02:11.352325Z` (within the source-check window). Initial PowerShell exit1 reflected native stderr from deliberately caught b2 error; a child-process capture records script return0, stdout2029 bytes, stderr858 bytes. The b2 failure remains, not a fix. Reproduction: [HOST_PROBE_RESULT.JSON](_WORK/W2_E/HOST_PROBE_RESULT.JSON), [HOST_PROCESS_RESULT.JSON](_WORK/W2_E/HOST_PROCESS_RESULT.JSON), [PARAMETER_COMPARISON.JSON](_WORK/W2_E/PARAMETER_COMPARISON.JSON), [GOLDEN_SYNTHETIC_RAW.NPZ](_WORK/W2_E/GOLDEN_SYNTHETIC_RAW.NPZ), `COMPARE.py` and `HOST_PROBE.py`; environment/protobuf details in [W2-E](_WORK/W2_E_RESULT.md). No vendor SDK is used. [F333](RAW_FACTS.md#f333).

**[ANALYSIS]** CLI score .001 cannot recover candidates discarded by embedded score .6; global max300 does not undo max20 per class. Model Zoo public outputs are decoded boxes/scores/indices, so raw-head decode, sigmoid and a second inverse-letterbox transform are wrong. AP differences across these objects mix anchors, preprocessing, NMS, batch and unknown vendor checkpoint, not isolated LinQ INT8 loss. [F251](RAW_FACTS.md#f251).

**[SRC/UNKNOWN]** Color/geometry differences are independent confounders:

- Darknet origin is RGB 0..1; strict source does not permute convolution input channels, yet its sidecar says BGR. Sidecar is not proof of correct BGR. Model Zoo PIL recipe is RGB; OpenVINO describes original RGB versus separately converted BGR.
- Vendor runner converts cv2 BGR→RGB; ORT helper leaves BGR and ignores sidecar color. Actual vendor binary color remains unknown: it could have been converted separately.
- Repository letterbox: OpenCV linear, rounded resize, fill114. Model Zoo card: PIL bicubic, truncated resized dimensions, fill128; inverse geometry uses rounded dimensions and floating half-padding. Darknet: own resize, float fill .5. Save actual resized H/W and all four integer pads, including odd dimensions, not scale alone.
- Historical MIT Tiny helper asserts `(1,13,13,255)` and `(1,26,26,255)`, depends on dictionary order, flattens/per-class NMS without batch identity, and directly scales xyxy without inverse letterbox. Removing asserts can mix images; it is not a b8/custom-class decoder.

Evidence: [F248](RAW_FACTS.md#f248), [F249](RAW_FACTS.md#f249), [F251](RAW_FACTS.md#f251). **[ANALYSIS]** Vendor Tiny is an optional environment smoke only when actual `.tpu`, matched runtime and exact golden recipe are issued. It is not mandatory if a compiler plus minimal custom example exists, and never validates a custom PPE detector. [R007](#r007), [Q019](OPEN_QUESTIONS.md#q019).

## PTQ percentile, thresholds, numeric precision and calibration quality

**[DOC/UNKNOWN]** LinQ H primary arithmetic is int8. Runtime float32 I/O or ctypes `uint8*` does not establish device arithmetic precision. Current signedness, zero point, granularity, rounding/saturation, bias/accumulator and residual-scale rules are unknown. Historical float16 flags or prospective fp16/bfloat16 claims do not establish a general FP16 backend. ONNX Q/DQ and QAT are not confirmed bypasses of vendor quantization. [F255](RAW_FACTS.md#f255), [F260](RAW_FACTS.md#f260), [Q013](OPEN_QUESTIONS.md#q013).

**[DOC/UNKNOWN]** Calibration is data-dependent: calibration tensors determine thresholds, then software quantization/scaling and hardware-model representations are produced. The guide's `percentile` description mentions weight coefficients. These can coexist; do not assume activation-histogram clipping or a documentation contradiction. Formula, range/default, sign/absolute-value basis and meaning of `100.0` remain unknown. [F252](RAW_FACTS.md#f252), [Q011](OPEN_QUESTIONS.md#q011).

**[SRC]** The third-party builder catches **any** TypeError from `calibrate(...,percentile=...)` and retries without the parameter. It can hide an internal error after mutation. Summary omits requested/effective percentile, exception/retry, quantizer version and thresholds; `.qm` existence does not prove the intended setting. Use a fresh object per supported combination, retain the first error, and remove unconditional retry from the experiment protocol. Blind 99.9/100 sweeps can test one default or mixed paths. [F253](RAW_FACTS.md#f253), [E005](#e005).

**[SRC/UNKNOWN]** A concrete source path is `thresholds = regular_model.calibrate(...)` → `regular_model.quantize(thresholds)` → `.qm`. Threshold schema, supported persistence/load and cross-graph/version portability remain unknown. Round-trip `.qm` in a fresh process without recalibration; compare normalized metadata/weights and golden outputs rather than demanding byte-identical timestamps. Do not promise arbitrary pickle portability. [F254](RAW_FACTS.md#f254), [Q012](OPEN_QUESTIONS.md#q012), [E006](#e006).

**[DOC/ANALYSIS]** Compare source float → exported ONNX → imported float → quantized reference with its own rescale → TLM if supplied → correct LinQ user I/O. Guide `rescale(data)` belongs to the quantized TF graph; historical `scale * 2. ** shift` from `fpga_data.pickle` and fixed `output_node_1` belongs to that model. Neither is universal `.tpu` dequantization. FULL may already return user-format outputs. If TLM is unavailable, mark `UNAVAILABLE`: compiler/runtime uncertainty stays combined; it is not a universal smoke prerequisite. [F255](RAW_FACTS.md#f255), [F256](RAW_FACTS.md#f256), [F257](RAW_FACTS.md#f257), [F258](RAW_FACTS.md#f258), [F261](RAW_FACTS.md#f261).

**[ANALYSIS]** First divergence determines work: pre-PTQ mismatch → export/import; matching float but poor quantized reference → PTQ/data; passing reference but device mismatch → I/O/codec/compiler/runtime; all numeric stages match but poor task quality → model/data/rules. Keep anchors, color, geometry, output boundary, score/NMS and class map identical before attributing AP loss to INT8. Post-NMS-only access needs matching embedded cutoffs; lowering an external threshold cannot recover discarded candidates. [F251](RAW_FACTS.md#f251), [F261](RAW_FACTS.md#f261).

**[DOC/ANALYSIS]** Prepare calibration/tuning/holdout splits by camera, clip and time, avoiding adjacent-episode leakage and recording shared scenes. Calibration needs actual inference preprocessing and representative lighting/views/distances/small PPE/background/empty/difficult scenes. Two guide images are a demo; guide recommendation 100 is guidance, and 100/500 are budget candidates, not sufficient-sample standards. Float32 `500×3×640×640` storage is `2 457 600 000` bytes, approximately `2.29 GiB`; 100 is approximately `0.458 GiB`. This is array storage arithmetic, not peak RAM; memmap does not prevent SDK copies/activation storage. Measure elapsed, process-tree RSS, disk and failures separately from image preparation. [F259](RAW_FACTS.md#f259), [F261](RAW_FACTS.md#f261).

**[ANALYSIS]** Evaluate AP50/AP50:95 and recall per class/camera/size with support counts and missed examples; retain original-pixel and resized-input object sizes. COCO AP_small is not equivalent to small helmet after resize. Overall mAP can hide respirator failure. Absence violations require person↔PPE association and event-level FP/FN, not object recall alone. Full case supplies allowable degradation and temporal/event criteria; none was invented. [F261](RAW_FACTS.md#f261), [Q029](OPEN_QUESTIONS.md#q029), [Q030](OPEN_QUESTIONS.md#q030).

## Runtime .tpu ABI, user/raw tensors, ownership and lifecycle

**[DOC/SRC]** Local flow is `Device.list_devices()` → `Device.open` → `device.load` → `program.inference` → blocking `sync` with a tensor dictionary. It does not define network transport. Public pytpu `15.0.24` uses ctypes and `/usr/lib/libtpu.2.so`; no native library was loaded here. Python `15.0.24` versus runtime `16.18.6` is not itself incompatibility evidence because version axes may differ. Obtain actual pairing. [F262](RAW_FACTS.md#f262), [F270](RAW_FACTS.md#f270), [F306](RAW_FACTS.md#f306), [Q006](OPEN_QUESTIONS.md#q006).

**[SRC/LOCAL isolated expression]** Historical `list_devices()` filters `/dev` names with `re.match(r'tpu.', f) and len(f)==4`; it does not perform native enumeration/stat/char-device/permission/PCI/ioctl verification. Mock entries `tpu0,tpu9,tpu10,tpux,tpu.,tpu,nvidia0` yield `/dev/tpu0,/dev/tpu9,/dev/tpux,/dev/tpu.`: it accepts tpux/tpu. and excludes tpu10. This is an old Python expression result, not 2026 naming/device-count evidence. [F186](RAW_FACTS.md#f186), [S174](SOURCES.md#s174).

**[SRC, historical only]** `tpu_get_program_info` supplies JSON: input region1/output region2 and hardware parameters. Ordinary output uses `user_dtype/user_shape`; raw-format output is bytes reshaped by `ddr_word_len`. Old codec reads `user_order/tpu_order`, padding, scales, `tpu_shape/tpu_dtype` and `anchor`; this anchor is a tensor-codec field, not YOLO anchors. Numeric conversion lives in unavailable `tpu_tlm_is`; keys/dtypes do not reconstruct packing/dequantization. Current format/schema/alignment/byte sizes and ABI are unknown. Do not apply old ctypes declarations to a new `.so`. [F263](RAW_FACTS.md#f263), [F264](RAW_FACTS.md#f264), [Q014](OPEN_QUESTIONS.md#q014).

**[SRC/UNKNOWN]** RAW file/metadata format and `ProcessingMode RAW/PRE_PROCESS/POST_PROCESS/FULL` are different axes. Historical allocation/return depends on the raw-format flag while enum is passed separately to native code. `mode=RAW` does not guarantee meaningful int8 output from any ordinary `.tpu`; FULL does not establish physical placement of transforms. ctypes `uint8*`, dtype view or reshape is not numeric dequantization. Use supported program×mode×buffer combinations and supplied codec/goldens. [F256](RAW_FACTS.md#f256), [F258](RAW_FACTS.md#f258), [F265](RAW_FACTS.md#f265), [Q018](OPEN_QUESTIONS.md#q018).

**[SRC/LOCAL mock]** Old wrapper validates Mapping, unknown names and native return/status; saying it checks nothing is false. In fake-native host probes, float64 instead of float32, noncontiguous slice and empty Mapping were not rejected by the Python layer before registration. Missing native and current versions were not tested. Our adapter should validate exact names/dtype/shape/C-contiguity/nbytes/batch/finite values before native submission. [F266](RAW_FACTS.md#f266).

**[LOCAL mock, correction]** “Copy outputs” comment in `15.0.24` describes a view chain: bytearray → ctypes `from_buffer` → `np.ctypeslib.as_array` → dtype view → reshape. Pointer mutation is visible. After deleting local context/pointer and GC, `[1.25,-2.5]` persists and base references retain Python-owned backing. No `.copy()` **did not prove dangling/use-after-free**. Native-library memory after destroy was not read. Actual current output validity after next request/session close and input release point remain unknown. Until supplied contract resolves it, keep inputs until terminal completion and copy outputs at a documented point before handing them to another thread/queue; this is conservative app policy. [F267](RAW_FACTS.md#f267), [S160](SOURCES.md#s160), [Q015](OPEN_QUESTIONS.md#q015).

**[LOCAL mock]** Generator context managers in `15.0.24` destroy after yield without try/finally: normal exit destroys; ordinary exception omits it. This is observed control flow, not measured native leakage or a Runtime 2026 defect. `Program.buffer` normal-path destroy is enabled despite TODO; “buffer never destroyed” is false. [F268](RAW_FACTS.md#f268), [K012](CRITIC.md#k012-w2).

## Runtime concurrency, timeout, cancellation and safe recovery

**[SRC, historical]** `15.0.24` test creates eight separate Inference objects on one Program with ThreadPoolExecutor, but has incorrect-result TODO and only prints `X` without assert. `14.7.0` contains native-callback async submission/multiple handles on one device; helper `n_proc` makes coroutines, not OS processes, and does not check callback result or demonstrate timeout/cancel/finally. This disproves an asserted universal “one process per device” requirement; it does not establish current correct concurrency. [F316](RAW_FACTS.md#f316), [F317](RAW_FACTS.md#f317), [F318](RAW_FACTS.md#f318), [F319](RAW_FACTS.md#f319), [F321](RAW_FACTS.md#f321), [Q025](OPEN_QUESTIONS.md#q025).

**[ANALYSIS]** Initial application policy is one session owner and sequential submission. With a supported current example, E017 tests two separate Inference objects, immutable distinguishable A/B inputs, IDs, independent outputs and finite in-flight limit. Multiprocess is a separate permitted test; do not pass handles by assumption. Passing two workers does not prove hardware overlap, fairness or tenant isolation. Mismatch stops parallel admission and returns to sequential golden control. [E017](#e017).

**[UNKNOWN/ANALYSIS]** An app deadline, HTTP timeout or cancelled coroutine is not native cancellation. Keep request outstanding, buffers/handles alive until confirmed terminal state. Blind resubmission may duplicate computation and events; correlate late results to request, worker generation and frame, rejecting stale outputs. Cancel/retry/idempotency and recovery permissions remain unknown. [F311](RAW_FACTS.md#f311), [F323](RAW_FACTS.md#f323), [Q024](OPEN_QUESTIONS.md#q024), [Q028](OPEN_QUESTIONS.md#q028).

**[ANALYSIS]** Pre-submit input-validation error need not damage a session or demand restart. After confirmed completion test documented close/reopen and orderly own-worker replacement: stop admission, drain, close, exit. A new process does not guarantee a stuck native job is released. Killing mid-call, device reset, driver unload and reboot commands were not established here. If a clean worker with the same golden also fails, preserve the first incident packet and escalate to the designated engineer/admin instead of endless restarts. [F324](RAW_FACTS.md#f324), [F325](RAW_FACTS.md#f325), [F326](RAW_FACTS.md#f326), [E016](#e016).

## LinQ execution proof: compiler coverage versus per-request completion

**[ANALYSIS/UNKNOWN]** Two linked assertions are required: (1) intended graph/weights became the loaded artifact and compiler covered the agreed NN boundary; (2) this request completed on the issued LinQ device/service. A correct output, `.tpu` load, aggregate utilization or UI “LinQ” badge alone proves neither pair. The current coverage report/no-fallback guarantee and request-correlated device evidence were not obtained. [F291](RAW_FACTS.md#f291), [F292](RAW_FACTS.md#f292), [F293](RAW_FACTS.md#f293), [F294](RAW_FACTS.md#f294), [Q021](OPEN_QUESTIONS.md#q021).

**[ANALYSIS]** Preserve source commit/weights hash → exporter settings/ONNX hash → compiler version/target/preset/options → transformed/fused/deleted-op report or matching-release “whole TPU graph or error” guarantee → loaded `.tpu` hash. ONNX-node count need not equal TPU instruction count because folding/fusion are legitimate; tensor-core machine code alone does not prove all NN operations are on-device. For completion preserve physical/runtime device mapping, load record, request/input IDs, submit/terminal status/output and trusted request↔device correlation. A/B inputs exclude stale/wrong-model output. A supported allowed wrong-device/unknown-version negative control only proves refusal at that boundary, not absence of partial host execution. [F291](RAW_FACTS.md#f291), [F294](RAW_FACTS.md#f294), [E009](#e009).

**[DOC/SRC/UNKNOWN]** HPS names Performance Profiler, DNN Stat and Power Monitor, but current units/clocks/scope/export/request/model/device IDs are undisclosed. Old README describes transfer-to/executor/transfer-from queues and last/average/maximum; average/max accumulate across Device-object runs, not one concurrent request. Some advertised README statistics are missing from obtained source; `13.0.13` delegates to external native code. `disable_static_checker` is not an established strict/no-fallback flag. No current profiler CLI or equivalent strict flag was established. [F287](RAW_FACTS.md#f287), [F288](RAW_FACTS.md#f288), [F289](RAW_FACTS.md#f289), [F290](RAW_FACTS.md#f290), [Q022](OPEN_QUESTIONS.md#q022).

**[ANALYSIS/UNKNOWN]** Service-only evidence may be trusted request/device trace or organizer-accepted witnessed run in an allocated slot with model hash/device/controlled input. Acceptance is unconfirmed; no mandatory attestation, root or separate profiler requirement is known. Agree the package with jury. Host RGB/layout/packing/codec/NMS/tracker/rules can be ordinary stages outside the agreed graph, subject to case approval; FULL does not place the whole chain on TPU. Detector/pose/re-ID/classifier each need boundary and proof if multiple required NNs are used. [Q005](OPEN_QUESTIONS.md#q005), [E009](#e009).

## Video data/control plane: transport, frame identity, clocks and queue policy

**[DOC/UNKNOWN]** Dataset-image runners are not RTSP services. `.tpu` documentation does not establish hardware video decode. HPS optional encoding and HX RK3588 decoder do not establish decode on LinQ H. Shell may place decode/preprocess on server CPU; a tensor service may require our host; managed video may own these stages. Actual payload/codec/network/CPU quota and camera reachability decide placement. [F332](RAW_FACTS.md#f332), [Q004](OPEN_QUESTIONS.md#q004).

**[ANALYSIS, illustrative arithmetic]** One `1×3×640×640` float32 tensor is `4 915 200` bytes. Hypothetical eight cameras×10 fps require `393 216 000` bytes/s without overhead; uint8 would be `98 304 000` bytes/s. These are not case requirements, selected model contract or measured network rates. JPEG/video transmission helps only with supported decode and a separate quality check. SSH does not establish remote camera reachability. [F312](RAW_FACTS.md#f312).

**[ANALYSIS, proposed app contract; not SDK features]** Each frame carries `camera_id`, new `stream_epoch` after reconnect, monotonic `frame_seq` within epoch, request/job ID, model revision/artifact hash and preprocess/config hash. Outputs map back to identical frame and geometry. Tracking receives actual source time and gaps after dropping frames, not an assumed adjacent-frame cadence. Keep source PTS/timebase where available; local monotonic receive/decode-ready/enqueue/submit/result/event stamps; UTC with clock source for logs. Do not subtract clocks across hosts without synchronization/offset. Unknown capture time permits receive-to-event; opaque remote service permits client roundtrip, not claimed capture-to-event or accelerator compute time. [F313](RAW_FACTS.md#f313).

**[ANALYSIS, proposed policy]** Bound queues by frame count, bytes and permissible frame age after measuring actual limits. For live alerting, replace stale **unsubmitted** frame of the same camera with fresh input and log drops; offline evaluation uses no-drop mode. Total in-flight≤quota; bound each camera's pending queue and schedule fairly across unequal rates. Batch assembly has deadline, real-frame count and explicit padding count; it cannot wait forever for a slow camera. Reconnect creates epoch; model activation creates version boundary. Reject late/stale identity/age, deduplicate events, explicitly reset/rebind tracker state if class map/geometry changes. [F313](RAW_FACTS.md#f313), [E014](#e014).

**[ANALYSIS]** Per camera record ingress/sampled/dropped/processed, queue wait/network/call/postprocess, frame age and event delay. Aggregate FPS without freshness/fairness does not establish realtime fitness. Person↔PPE association, zones, temporal rules and handling missing evidence remain app responsibilities; missed frame or unknown inference is not automatically “PPE absent.” [F332](RAW_FACTS.md#f332), [Q030](OPEN_QUESTIONS.md#q030).

## IVA CV: documented Linq TPU integration, conditional PPE delivery

**[DOC]** IVA CV admin guide literally says “с использованием Linq TPU”; the link is stronger than inference from `/dev/tpu0`. Documented start order is MongoDB → Edge-api → project videoanalytics → VDMS-api → UI, requiring initial DB/reference data, config, models and matched host/runtime. Edge REST/WS/gRPC and device mapping do not make it the hackathon's issued API. Exact H1M/SKU/runtime and this image's PPE backend inventory remain unknown. [F296](RAW_FACTS.md#f296), [F297](RAW_FACTS.md#f297), [F298](RAW_FACTS.md#f298).

**[SRC text correction; no PDF images/registry access]** `walkers-node:0.1.310` was extraction glue: `0.1.3` + next page 10, supported by two page-separated extractions. Likewise `edge-api:0.3.10` + p12, `vdms-api:0.5.22` + p14, `vdms-ui:0.3.2` + p18. Do not deploy a reconstructed tag as a confirmed available release: use issued matched digests. Historical erroneous extraction stays in W1 evidence. [F295](RAW_FACTS.md#f295), [F308](RAW_FACTS.md#f308), [Q027](OPEN_QUESTIONS.md#q027).

**[DOC/UNKNOWN]** ПАК ОТПБ/LinQ/PPE news establishes industrial linkage, not identity with this deployment. `IVA_TENANT="cbr"`, project namespace and walkers-node name do not enumerate models. UI helmet/vest/zone/cigarette/smoke/phone events are not backend model inventory; `defaultVisibleEventTypes` is visibility. `eventsProcessorJobIntervalMs=500` and `eventsProcessorStuckRestartSec=10` are event-record queue/job recovery settings, not 500 ms NN latency or 10 s device timeout. Multiple UI windows do not prove camera capacity; generic RAM/disk minima do not size our load. [F298](RAW_FACTS.md#f298), [F299](RAW_FACTS.md#f299).

**[UNKNOWN]** Real deployment needs images/digests, `config-patch.json`, weights/compiled programs/internal model configuration, initial DB, scripts, keys/allowed methods, driver/runtime pairing and team rights. Registry URL/`pull.sh` is not a delivery. Commercial license/support is not a hackathon grant or an established execution ban. E018 is conditional; without bundle transfer architectural lessons to R001/R002. Four-NN interview was not watched/listened to; annotation is not an observed multistream demonstration. Separate IVA CV1.8 user guide “СИЗ на лицах” means medical-mask/COVID regime, not proven industrial helmet/respirator backend or LinQ execution. [F300](RAW_FACTS.md#f300), [F301](RAW_FACTS.md#f301), [F327](RAW_FACTS.md#f327), [Q026](OPEN_QUESTIONS.md#q026), [Q027](OPEN_QUESTIONS.md#q027).

## Published performance: 2026 LinQ table and historical FPGA evidence

**[REPORTED, vendor; text-only transcription]** [2026 presentation](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf) specifies TPU Runtime `16.18.6`, Framework `2026.8.43`, Ubuntu 24.04, i7-10700K. No original page images/raw logs were obtained. MLPerf-method footnote does not establish submission ID, scenario/LoadGen revision, weight/input hashes/sizes, calibration/accuracy/precision, preset/clocks/queue depth, latency statistic or transfer/decode/NMS boundary. Preserve unusual units; `—` is unreported, not zero. [F130](RAW_FACTS.md#f130), [F281](RAW_FACTS.md#f281), [F331](RAW_FACTS.md#f331).

| Network | Batch | HP FPS | HP latency, ms | HPQ FPS | HPQ latency, ms |
|---|---:|---:|---:|---:|---:|
| anti_spoof_mn3 | 1 | 1561,1 | 985,72 | 6244,4 | 985,72 |
| inception_v3 | 1 | 287,1 | 4,77 | 1148,4 | 4,77 |
| inception_v3 | 8 | 480,8 | — | 1923,2 | — |
| lenet5 | 1 | 12519,7 | 128,90 | 50078,8 | 128,90 |
| lenet5 | 8 | 84961,6 | — | 339846,4 | — |
| mobilenet_v2 | 1 | 1201,7 | 1,44 | 4806,8 | 1,44 |
| mobilenet_v2 | 8 | 2456,8 | — | 9827,2 | — |
| resnet152 | 1 | 228,4 | 5,34 | 913,6 | 5,34 |
| resnet50 | 1 | 432,9 | 2,99 | 1731,6 | 2,99 |
| resnet50 | 8 | 1112,8 | — | 4451,2 | — |
| ssd_mobilenet_v2 | 1 | 556,7 | 3,54 | 2226,8 | 3,54 |
| ssd_mobilenet_v2 | 8 | 428 | — | 1712 | — |
| yolo5s | 1 | 106,1 | 23,71 | 424,4 | 23,71 |
| yolov8n_pose | 1 | 104,8 | 21,51 | 419,2 | 21,51 |

**[ANALYSIS/UNKNOWN]** All 14 HPQ throughputs are exactly 4×HP with identical latency: compatible with chip aggregation, not proof of 4× single-request speedup. Actual HPQ measurement versus extrapolation is unknown. New parallel wrapper sums child-process measured rates, so it is not simply N×one baseline; relation to slide remains unproved. Another wrapper divides completed images by total wall time including worker startup/shutdown. Both need their denominator stated. [F277](RAW_FACTS.md#f277), [F284](RAW_FACTS.md#f284), [F331](RAW_FACTS.md#f331).

**[ANALYSIS/UNKNOWN]** `1000/FPS` is not the table's latency: HP ResNet50 approximately 2.31 ms versus 2.99 ms; yolo5s approximately 9.43 ms versus 23.71 ms. Scenarios/overlap/queue/statistic may differ but cause is unestablished. SSD b8 is slower in FPS than b1; batching is not universally beneficial. Do not silently change anti_spoof `985,72 ms` or lenet5 `128,90 ms` to microseconds. Presentation p3 ResNet50 `460/1046 FPS` differs from p4 `432,9/1112,8`; this is an unresolved scope difference, not proved regression. Original images/errata and protocols are [Q031](OPEN_QUESTIONS.md#q031), [Q032](OPEN_QUESTIONS.md#q032). [F282](RAW_FACTS.md#f282), [F283](RAW_FACTS.md#f283), [F285](RAW_FACTS.md#f285), [F286](RAW_FACTS.md#f286).

**[REPORTED, different scopes]** HPS ResNet50 b1 approximately 2.3 ms / prospective optimization 1.5 ms has incomplete/different scope. University `443/430/142/20 FPS` are prior measurements known only through abstract, not a comparable modern protocol. Do not combine them into a model ranking. [F137](RAW_FACTS.md#f137), [F236](RAW_FACTS.md#f236), [F331](RAW_FACTS.md#f331).

**[REPORTED, actual published historical logs]** IVATech2020 has harness/logs/system description: FPGA Alveo U200, 250 MHz, TF 1.15, int8 input. Single Stream VALID: p90 `12,230138 ms`, mean `12,081844 ms`, p99 `12,345478 ms`. Offline VALID: `88,8239 samples/s`, `24 576` samples/query `276,682437431 s`; accuracy `75,756%` on `50 000` images. This is a useful reproducible-evidence pattern, not current H1M ASIC performance, our benchmark or current ABI compatibility. Pinned MLCommons policies distinguish scenarios/untimed preprocessing but do not determine the vendor's actual scenario. [F331](RAW_FACTS.md#f331), [S075](SOURCES.md#s075), [S077](SOURCES.md#s077).

**[ANALYSIS]** Accept quality first, then measure cold import/open/load/session/first completion; warm b1 with one outstanding request; steady useful-image throughput in a common window with bounded in-flight. Record warmup/count/padding, mean/p50/p90/p95/p99/max, timer boundary and other-user load. Padding is not useful work; target QPS is not achieved QPS, `INVALID` is not `VALID`; full API time may include queue/codec/transfers. Split device compute only with trusted timers. Add decode/network/NMS/tracker/rules/events and per-camera age/drop/fairness before estimating camera capacity. No published TOPS/FPS establishes N cameras. [E012](#e012), [E013](#e013), [E014](#e014).

## Reproducible diagnosis, shared manifests and first-hour ordering

**[ANALYSIS]** Classify the first failing boundary; preserve first error and change one factor. Missing wheel/native/license → delivery/environment; unsupported actual node → frontend/compiler; pre-PTQ numeric mismatch → export/import; loss only after PTQ → quantizer/calibration; passing reference but device mismatch → ABI/I/O/codec/compiler/runtime; correct tensors but wrong boxes/classes → decoder/map/geometry; good detection but poor violation metric → association/rules/data. Do not retrain or sweep opset×shape×preset×TF before a real minimal reproducer. [F232](RAW_FACTS.md#f232), [F242](RAW_FACTS.md#f242), [F261](RAW_FACTS.md#f261), [F326](RAW_FACTS.md#f326).

| Symptom | First useful action [ANALYSIS] | Unsupported conclusion to avoid |
|---|---|---|
| `onnx_direct`/`.so` import error | Compare matched bundle, OS/ISA/Python/native pairing and traceback | Random TF change or mandatory physical board |
| Converted tensor missing | Save converter return type/mapping, GraphDef and exact namespace/suffix | Blindly stripping any `:...` |
| Shape error after H/W change | Compare full re-export against input-header-only patch, constants/grids/outputs | Checker establishes numerical correctness |
| `.qm` after TypeError retry | Save first error/effective call; fresh supported baseline | Requested percentile applied |
| STAGING slow/bad output | Preserve logs/resources; separate documented DEFAULT artifact | O1/O5 share preset semantics |
| API success but wrong custom classes | Explicit schema/map/NMS/names/inverse geometry | Runtime success validates detector |
| Symbolic-N Tiny b2 failure | Fixed b1 control, inspect Squeeze/geometry | All Tiny backbones restricted to b1 |
| Timeout/late output | Stop admission if needed; retain outstanding ledger until terminal state | Cancelled native work or safe blind retry |
| Error after native submit | Current state/recovery contract and incident packet | Every exception requires reset/reboot |

**[ANALYSIS]** Incident packet: full first traceback/stderr/native message, timestamp + monotonic elapsed, phase `open/load/submit/complete/close`, code namespace/version, request/frame/generation, immutable model/input/spec hashes, common environment/native/driver/firmware manifest, permitted device/job identity, output arrays/shape/dtype/hash if present, outstanding/admission state and later actions/outcomes. Retries reference the original packet; do not overwrite it with latest error. Exclude credentials/tokens and restricted frames from public material. [F326](RAW_FACTS.md#f326).

**[ANALYSIS]** Keep three shared records, with single owners:

- `MODEL_MANIFEST`: source commit/weights hash; exporter pins/command; ONNX hash/IR/all opsets; task/nc/names/category map; I/O names/layout/dtype/shapes; color/range/geometry; decode/NMS schema/parameters; calibration split/effective quant options/threshold refs; compile target/preset/version; `.qm/.tpu` hashes; current runtime contract.
- `DATA_MANIFEST`: camera/clip/time/hash/split/labels, with calibration/tuning/holdout separated.
- Golden package: encoded-image and decoded-array hashes; prepared tensor bytes/order/hash; original/resized H/W, scale and all pads per frame; all named pre-NMS outputs; post-NMS detections/class map; provider and justified comparison tolerances.

These prevent alternate UI class maps/exporters/preprocessing from silently creating different models. [F242](RAW_FACTS.md#f242), [F261](RAW_FACTS.md#f261).

**[ANALYSIS, execution order]** Resolve Q001-Q005/E001 while independent E002/E003/data splitting proceeds. Then accepted float export/import → PTQ/compile → one minimal device/golden run and both proof links → task quality → performance → video. Vendor known-good and TLM are optional aids if issued. Do not wait for every low-level answer before a supported first run. Stop parameter sweeps if effective quantization is unknown; stop concurrent admission on mismatch; escalate a clean-worker golden failure. Choose per-branch deadlines using actual elapsed and remaining 45-hour context, not invented platform compile duration. [F329](RAW_FACTS.md#f329), [F333](RAW_FACTS.md#f333), [E001](#e001), [E009](#e009).

## Conditional implementation routes R001-R008

All routes below are **[ANALYSIS]**, contingent on actual grants. Shared acceptance is an allowed model with known contract, reproducible results, task quality and accepted LinQ proof. None asserts an already available endpoint. CPU/RTX preparation is not a compliant final fallback. Dependencies refer to proposed experiments, not completed runs.

<a id="r001"></a>
### R001 — Shell/container with matched compiler and runtime

- **conditions:** Actual shell/container grant, own graph/weight permissions, matching tools (compiler may be elsewhere), device rights, network and sufficient worker lifetime. Local API is documented; competition grant is unknown.
- **actions_and_checkpoints:** E001 environment → E002 model/export → E004 float import → E005 PTQ → E007 compile → E008 metadata/device mapping → E009 proof → E010 numerics → E011 quality, then timing/video. Preserve compiler and runtime lineage even when separated. Remote UI/backend requires allowed ports and long-running workers; otherwise use local components and permitted outbound/polling transport.
- **outcomes_and_limits:** Missing compiler/upload/device rights or viable lifecycle requires another supported mode. A shell does not guarantee any of these. A compiled file alone does not establish device execution/quality. Share actual target/environment/network with model_stack and architecture.
- **questions:** [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Basis: [F329](RAW_FACTS.md#f329), [F312](RAW_FACTS.md#f312).

<a id="r002"></a>
### R002 — Custom-model service without mandatory SSH

- **conditions:** Service accepts graph-to-compile or compatible `.tpu`; permits immutable version selection/update; exposes usable output contract and accepted LinQ correlation. Endpoint/grant is unissued.
- **actions_and_checkpoints:** E001/E002 then E015: register/upload V1/hash, wait ready, golden request/output, permitted activate V2, verify revision/hash/known output. Operator-side PTQ/compile must retain artifacts/logs in the same model lineage. Verify E009 proof, E011 quality and bounded service latency.
- **outcomes_and_limits:** Working custom service makes SSH unnecessary for this path. Catalog-only → R004/other grant. Post-NMS/events-only outputs require deciding whether task/evaluation is possible; hidden raw-head parity remains unavailable. Service success does not establish full video SLA.
- **questions:** [Q001](OPEN_QUESTIONS.md#q001), [Q003](OPEN_QUESTIONS.md#q003), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Basis: [F309](RAW_FACTS.md#f309), [F312](RAW_FACTS.md#f312). Handoff: accepted input format to model_stack; actual transport to architecture.

<a id="r003"></a>
### R003 — Job/file execution

- **conditions:** Own model permitted; actual submission/artifact/result/log contract, queue, storage and turnaround documented.
- **actions_and_checkpoints:** Finite offline run with input/output identity and E009 proof; E002/E007 wherever permitted; E015 actual job lifecycle. Save useful completion count, total turnaround and selected model revision.
- **outcomes_and_limits:** Can support LinQ inference and offline evaluation. Realtime requires measured bounded turnaround/queue and frame association against case; whole-video upload is not automatically realtime. If insufficient, request R001/R002/R005. Give architecture/product measured limits and explicit live/offline status.
- **questions:** [Q001](OPEN_QUESTIONS.md#q001), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Basis: [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313).

<a id="r004"></a>
### R004 — Organizer catalog only

- **conditions:** Available models expose required classes/outputs and organizer accepts supplied models with our rules/UI contribution.
- **actions_and_checkpoints:** Freeze model ID/output schema; E009 device correlation, E011 case quality, E014 video and person↔PPE association. Give model/data work actual semantic labels/thresholds and product accurate component authorship.
- **outcomes_and_limits:** Generic COCO detector does not become a custom PPE model. Missing respirator/other mandatory class, or required own weights, needs upload/compile/another grant. Catalog permission alone does not establish case coverage.
- **questions:** [Q001](OPEN_QUESTIONS.md#q001), [Q005](OPEN_QUESTIONS.md#q005), [Q029](OPEN_QUESTIONS.md#q029). Basis: [F302](RAW_FACTS.md#f302), [F330](RAW_FACTS.md#f330).

<a id="r005"></a>
### R005 — Managed video-inference service

- **conditions:** Actual camera/file/stream contract, allowed custom-model/config updates, event/output schema, logs/proof and network reachability.
- **actions_and_checkpoints:** E015 V1/V2 → E014 one clip/camera → E009 every required NN boundary → E011/E012 quality/service budget. Actual contract determines decode/tracking location; give architecture quotas/clocks/payload and model_stack update constraints.
- **outcomes_and_limits:** Camera unreachable, missing model control, unusable timestamp/reconnect identity → change transport/route. Do not equate this service with IVA CV Edge-api without supplied specification.
- **questions:** [Q003](OPEN_QUESTIONS.md#q003), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Basis: [F312](RAW_FACTS.md#f312), [F332](RAW_FACTS.md#f332).

<a id="r006"></a>
### R006 — Issued IVA CV PPE project bundle

- **conditions:** Matched images/digests, DB/config/models, driver/runtime and actual rights from Q027; public registry URL is insufficient.
- **actions_and_checkpoints:** E018 supplied startup order, positive/negative video and event checks; E009 proof for each required NN. Request actual model/event configuration and source/output contract; UI filters do not enumerate backend.
- **outcomes_and_limits:** No bundle → stop deployment branch, transfer architectural lessons to R001/R002. A UI event alone is not proof of LinQ execution. Distinguish supplied and own components and publication rights.
- **questions:** [Q026](OPEN_QUESTIONS.md#q026), [Q027](OPEN_QUESTIONS.md#q027). Basis: [F295](RAW_FACTS.md#f295), [F300](RAW_FACTS.md#f300).

<a id="r007"></a>
### R007 — Optional known-good vendor artifact smoke

- **conditions:** Actual `.tpu`, matched release, exact golden I/O/pre/post and accepted proof mechanism; vendor Tiny useful when exact recipe is supplied.
- **actions_and_checkpoints:** E008/E009 to isolate environment from custom-model problems. Resolve contradictory descriptors/color/outputs through the package, not visually plausible detections.
- **outcomes_and_limits:** Auxiliary, not a standalone final route; does not validate own PPE training/compilation. Optional when compiler plus minimal own example exists. Give model_stack scoped runtime golden and evaluation its different-model identity.
- **questions:** [Q003](OPEN_QUESTIONS.md#q003), [Q019](OPEN_QUESTIONS.md#q019). Basis: [F251](RAW_FACTS.md#f251), [F330](RAW_FACTS.md#f330).

<a id="r008"></a>
### R008 — CPU/RTX preparation before access

- **conditions:** Allowed source/weights/data and local tools; public CPU/helper protocols already exist, custom/strict exports remain future work.
- **actions_and_checkpoints:** E002/E003, data split, float quality, shared manifests/golden tensors; continue independently of access clarification. Give model/data work reproducible inputs, strategy honest preparation status.
- **outcomes_and_limits:** Does **not** satisfy mandatory LinQ inference. No access means CPU/RTX demo cannot be presented as compliant. Transition to R001-R006 requires actual grant and working call.
- **questions:** [Q001](OPEN_QUESTIONS.md#q001), [Q020](OPEN_QUESTIONS.md#q020), [Q029](OPEN_QUESTIONS.md#q029). Basis: [F302](RAW_FACTS.md#f302), [F333](RAW_FACTS.md#f333).

## Proposed experiments E001-E020: prerequisites, actions and interpretation

All E records are **[ANALYSIS, future]**. Existing local CPU/helper/mock outcomes are separately scoped in [F333](RAW_FACTS.md#f333); no E title implies completed proprietary or hardware work. Use actual supplied commands/API, not invented endpoints. Status per boundary is `PASS / FAIL / UNAVAILABLE / NOT_RUN`; retain first failing artifact/error. Functional owners can be combined by people while manifests stay singular.

<a id="e001"></a>
### E001 — Delivery, environment and license manifest

- **decision_and_prerequisites:** Environment/access owner; actual bundle or service onboarding. Public archives were inspected, current stack not installed. Decide reproducible release and allowed operations.
- **actions_and_artifacts:** Hash files/images/digests; save METADATA/WHEEL/entrypoints/Requires-Python/Requires-Dist, OS/ISA/kernel/glibc/native/driver/firmware pairing and per-layer rights. Install/import only matched delivery and run appropriate dependency check, e.g. `pip check`. API-only mode records client/server contract, possibly no local SDK.
- **outcomes_and_limits:** One shared environment manifest and operations list; on failure retain missing dependency/license/native error instead of random TF/Python sweep. Success proves environment/rights, not compiler/device operation.
- **evidence_and_questions:** [F210](RAW_FACTS.md#f210), [F329](RAW_FACTS.md#f329); [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002), [Q006](OPEN_QUESTIONS.md#q006), [Q026](OPEN_QUESTIONS.md#q026).

<a id="e002"></a>
### E002 — Immutable model/export and golden package

- **decision_and_prerequisites:** Model/export owner; CPU/RTX with exact allowed weights/source. Decide which graph is a valid pre-LinQ reference. Custom/strict export not performed here; W2-E public CPU tensors are diagnostic material.
- **actions_and_artifacts:** Pin source/weights/exporter/command/flags and hashes; inventory ONNX IR/opsets/domains/attributes/functions/externals and complete task/classes/I/O/pre/post. Compare source PyTorch and ORT pre-NMS on common controls, then identical decoder/NMS. Save image bytes/prepared tensors/per-frame geometry. New head/shape/weights creates new manifest revision.
- **outcomes_and_limits:** Frozen candidate and numerical golden; mismatch → fix actual export/head boundary before PTQ. Success does not establish LinQ support.
- **evidence_and_questions:** [F232](RAW_FACTS.md#f232), [F251](RAW_FACTS.md#f251); [Q003](OPEN_QUESTIONS.md#q003), [Q008](OPEN_QUESTIONS.md#q008), [Q009](OPEN_QUESTIONS.md#q009), [Q019](OPEN_QUESTIONS.md#q019), [Q020](OPEN_QUESTIONS.md#q020).

<a id="e003"></a>
### E003 — Custom-class decoder/NMS adapter without SDK

- **decision_and_prerequisites:** Video/adapter owner using shared model manifest; ordinary host. Shape helper already exposed defects, complete torch-NMS suite not run. Decide correct class/score/axis/geometry handling.
- **actions_and_artifacts:** Explicit decoded4+nc/classic5+nc/raw-multihead/post-NMS schemas. Test nc1/2/81, ambiguous axes, A≠6 and A=6 shortcut, empty/overlapping boxes/class-aware NMS, custom category map/output selection and rectangular inverse geometry. Pin NMS source/import and conf/iou/agnostic/multi_label/max_det/max_nms; copy before mutation. Classic `.1×.9=.09` versus modern `.9` must remain distinct.
- **outcomes_and_limits:** Expected classes/scores/boxes or explicit rejection with descriptors for unknown schema. Adapter validation, not model quality or TPU correctness.
- **evidence_and_questions:** [F237](RAW_FACTS.md#f237), [F242](RAW_FACTS.md#f242); [Q003](OPEN_QUESTIONS.md#q003), [Q020](OPEN_QUESTIONS.md#q020).

<a id="e004"></a>
### E004 — Imported float versus source ONNX parity

- **decision_and_prerequisites:** Import/compile owner; matched SDK/frontend and E001/E002. Physical device is not assumed necessary; actual converter dependencies must be established.
- **actions_and_artifacts:** Unmodified supported candidate; retain return type, name mapping, namespace, GraphDef/layout/I/O and all raw outputs on identical prepared tensors. Compare to ORT with justified tolerance, not top1/final boxes only. First error → traceback and reduced actual failing graph retaining constants/attributes. Do not substitute a similarly named converter for `onnx_direct`.
- **outcomes_and_limits:** Float parity permits PTQ. If float outputs inaccessible, record combined import+PTQ uncertainty. Success is neither compilation nor device execution.
- **evidence_and_questions:** [F215](RAW_FACTS.md#f215), [F219](RAW_FACTS.md#f219), [F232](RAW_FACTS.md#f232); [Q008](OPEN_QUESTIONS.md#q008), [Q010](OPEN_QUESTIONS.md#q010).

<a id="e005"></a>
### E005 — Effective percentile and quantizer scope

- **decision_and_prerequisites:** Quantization owner; SDK and supported minimal graph. Decide whether percentile affects weights, activations, both, is unsupported or remains ambiguous. Vendor calibrate has not run here.
- **actions_and_artifacts:** Read current help/signature/parameters; use outlier-sensitive graph and fresh objects for W0/W1×C0/C1×P0/P1, varying weights/calibration distribution/documented distinct percentile independently. Save requested/effective values, thresholds, quantized weights/scales/raw outputs and first error. No unconditional TypeError retry; choose P values capable of differentiating this distribution.
- **outcomes_and_limits:** Classify observed scope; equal outputs on insensitive graph do not prove ignored parameter. Unknown effective setting → stop sweep, retain default baseline. Not AP/QAT/QDQ validation.
- **evidence_and_questions:** [F252](RAW_FACTS.md#f252), [F253](RAW_FACTS.md#f253), [F255](RAW_FACTS.md#f255); [Q011](OPEN_QUESTIONS.md#q011), [Q013](OPEN_QUESTIONS.md#q013).

<a id="e006"></a>
### E006 — .qm/threshold save-load round trip

- **decision_and_prerequisites:** Quantization owner; SDK, E005 reference and documented loading API. Decide whether quantized state can be reproduced without recalibration.
- **actions_and_artifacts:** Save quantized `.qm`; fresh process loads without calibration and executes same goldens. Compare normalized topology/metadata/weights and all named raw outputs. Separately test thresholds persistence only with supported API; retain versions/stage elapsed, no arbitrary-pickle portability assumption.
- **outcomes_and_limits:** Same-version/graph reproducibility or localized state difference. Timestamp-driven file-hash change alone is not numerical failure. One round trip does not establish cross-version portability.
- **evidence_and_questions:** [F254](RAW_FACTS.md#f254), [F261](RAW_FACTS.md#f261); [Q012](OPEN_QUESTIONS.md#q012).

<a id="e007"></a>
### E007 — Explicit-target compilation and CPU-only build feasibility

- **decision_and_prerequisites:** Import/compile owner; matched compiler, accepted E004/E005 model, license/dependencies. CPU-only independence remains unknown.
- **actions_and_artifacts:** Record target/preset/input spec and device/driver presence or absence. Start documented DEFAULT or supplied supported equivalent; do not translate O1/O5. Save actual supplied command/API, logs/first error, wall time, peak process-tree RSS, `.qm/.tpu` and tensor descriptors. Following STAGING trouble, DEFAULT is a separate new artifact. TLM is optional if supplied.
- **outcomes_and_limits:** Compilation only for tested release/target/environment. Distinguish missing native library, license and physical-device requirement. Creation does not establish hardware numerics or task quality.
- **evidence_and_questions:** [F072](RAW_FACTS.md#f072), [F210](RAW_FACTS.md#f210), [F276](RAW_FACTS.md#f276); [Q002](OPEN_QUESTIONS.md#q002), [Q007](OPEN_QUESTIONS.md#q007), [Q009](OPEN_QUESTIONS.md#q009).

<a id="e008"></a>
### E008 — Runtime ABI, artifact metadata and device mapping

- **decision_and_prerequisites:** Runtime/proof owner; current reader/SDK and device if metadata requires load; service operator may supply equivalent. Decide which buffers and allocated hardware match this artifact.
- **actions_and_artifacts:** Hash matched headers/binding/native; read actual format/version, user/raw names/shapes/dtypes/order/sizes/scales without assuming historical JSON keys. Record SKU/revision/serial, PCI BDF/switch, node/runtime instance/team quota. If standard PCI inventory allowed, save LnkCap separately from LnkSta. Do not guess ABI with old ctypes against new `.so`.
- **outcomes_and_limits:** Artifact target/buffer schema/device linked. Not execution or pooled-memory proof; no OOM experiment to infer pooling.
- **evidence_and_questions:** [F263](RAW_FACTS.md#f263), [F270](RAW_FACTS.md#f270), [F279](RAW_FACTS.md#f279); [Q002](OPEN_QUESTIONS.md#q002), [Q014](OPEN_QUESTIONS.md#q014), [Q016](OPEN_QUESTIONS.md#q016), [Q017](OPEN_QUESTIONS.md#q017).

<a id="e009"></a>
### E009 — First LinQ run and two proof links

- **decision_and_prerequisites:** Runtime/proof owner; actual LinQ/service, compatible artifact/golden and E008. Vendor known-good or compiler plus minimal own example can suffice.
- **actions_and_artifacts:** One sequential worker sends distinct valid A/B inputs. Preserve source/export/compiled hashes, load/submit/terminal status/output and trusted request↔device correlation. Separately obtain current graph-coverage report or matching compiler guarantee. Only permitted documented negative control; service-only witnessed run may be agreed with organizer.
- **outcomes_and_limits:** State separately “completion correlated to LinQ” and “compiler covers agreed NN graph.” One without the other is incomplete proof. UI badge/aggregate utilization inadequate. Smoke does not establish PPE quality/performance.
- **evidence_and_questions:** [F291](RAW_FACTS.md#f291), [F294](RAW_FACTS.md#f294); [Q003](OPEN_QUESTIONS.md#q003), [Q005](OPEN_QUESTIONS.md#q005), [Q019](OPEN_QUESTIONS.md#q019), [Q021](OPEN_QUESTIONS.md#q021).

<a id="e010"></a>
### E010 — User/raw/reference numerical comparison

- **decision_and_prerequisites:** Runtime and quantization owners; SDK+LinQ, E008/E009, supported codec/goldens for raw path. Decide first divergence among import/PTQ/compiler/I/O; never guess packed buffers.
- **actions_and_artifacts:** Identical prepared tensor through imported float, quantized reference with its rescale, TLM if available and LinQ FULL. Separately supported RAW with equivalent postprocess. Save named outputs/shapes/dtypes/scales/finite status and max/mean absolute/relative errors before decode; distinct batch-slot images verify order. Pointer type is not numeric dtype.
- **outcomes_and_limits:** Localize earliest mismatch. Missing TLM → `UNAVAILABLE`, combined compiler/runtime uncertainty. Correct outputs do not establish graph coverage; retain E009 separately.
- **evidence_and_questions:** [F256](RAW_FACTS.md#f256), [F258](RAW_FACTS.md#f258), [F265](RAW_FACTS.md#f265); [Q009](OPEN_QUESTIONS.md#q009), [Q013](OPEN_QUESTIONS.md#q013), [Q018](OPEN_QUESTIONS.md#q018), [Q019](OPEN_QUESTIONS.md#q019).

<a id="e011"></a>
### E011 — PPE quality with calibration/tuning/holdout separation

- **decision_and_prerequisites:** Data/evaluation owner with association/rules owner; full case/data. Float baseline can precede SDK, hardware evaluation follows E009/E010. Decide model and event-rule acceptance.
- **actions_and_artifacts:** One DATA_MANIFEST camera/clip/time/hash/split/labels; freeze preprocessing, anchors/output boundary/embedded NMS/thresholds. AP50/AP50:95/recall per class/size/camera with support counts; separate violation FP/FN/person↔PPE association. Check object size in original/input pixels and no adjacent-frame leakage. Calibration 100/500 are budget candidates, not standards.
- **outcomes_and_limits:** Full-TZ acceptance and failure list. Pre-PTQ mismatch → export/import; PTQ-only → calibration; device-only → I/O/runtime; matching numeric chain but poor task → model/data/rules. Small sample/overall mAP does not establish generalization or hard-class quality.
- **evidence_and_questions:** [F259](RAW_FACTS.md#f259), [F261](RAW_FACTS.md#f261); [Q020](OPEN_QUESTIONS.md#q020), [Q029](OPEN_QUESTIONS.md#q029), [Q030](OPEN_QUESTIONS.md#q030).

<a id="e012"></a>
### E012 — Cold start, warm latency and steady throughput

- **decision_and_prerequisites:** Runtime owner, evaluation owner accepts model; actual team LinQ/service and E009/E011. Decide measured resource budget.
- **actions_and_artifacts:** Separately time cold import/open/load/session/first complete; warm b1 with one outstanding; completed real images/common steady window with bounded in-flight. Save elapsed/count/warmup/padding policy, mean/p50/p90/p95/p99/max, API boundary/clock source/other-user load. Separate transfers/compute only with trusted timers; separate device from full video chain.
- **outcomes_and_limits:** Scoped measured latency/throughput. Target QPS≠achieved; 1/FPS≠latency; API time≠tensor-core time. Camera sizing awaits E014.
- **evidence_and_questions:** [F331](RAW_FACTS.md#f331); [Q022](OPEN_QUESTIONS.md#q022), [Q023](OPEN_QUESTIONS.md#q023), [Q032](OPEN_QUESTIONS.md#q032).

<a id="e013"></a>
### E013 — Independent replica scaling

- **decision_and_prerequisites:** Runtime owner; E008 mapping/quota, E012 one-device baseline and permitted 2/4 devices. Decide useful gain from additional allocated devices.
- **actions_and_artifacts:** Same artifact/prepared inputs/stage boundary; compare one versus N replicas in common steady window. Save per-device valid completions, useful count, CPU/RSS/network/fairness. Do not replace measurement with N×baseline or mismatched cold-window rate sums.
- **outcomes_and_limits:** Measured replication scaling for this workload. Not N×lower single-request latency, graph sharding or pooled DDR. Localize host/network bottlenecks; four nodes do not promise 4× gain.
- **evidence_and_questions:** [F277](RAW_FACTS.md#f277), [F284](RAW_FACTS.md#f284); [Q016](OPEN_QUESTIONS.md#q016), [Q017](OPEN_QUESTIONS.md#q017), [Q023](OPEN_QUESTIONS.md#q023).

<a id="e014"></a>
### E014 — Frame correlation, freshness and camera service

- **decision_and_prerequisites:** Video/control-adapter owner; actual payload/network/codec/quota, E009/E012 and allowed clip/stream. Decide timely association under actual load.
- **actions_and_artifacts:** Compare one clip via saved prepared tensors versus real decode; then finite two-camera sequence with unequal rates and reconnect/new epoch. Log frame/request/model IDs, PTS/timebase, local monotonic stages, geometry, bounded queue/drops/stale outputs and in-flight≤quota. Test late result after deadline, reconnect and model change; tracker sees true time gaps.
- **outcomes_and_limits:** Correct correlation and bounded age under tested load. Unknown capture time → receive-to-event; unsynced hosts → client roundtrip, not cross-host subtraction. Two-camera success is not an eight-camera standard.
- **evidence_and_questions:** [F313](RAW_FACTS.md#f313), [F332](RAW_FACTS.md#f332); [Q004](OPEN_QUESTIONS.md#q004), [Q023](OPEN_QUESTIONS.md#q023), [Q030](OPEN_QUESTIONS.md#q030).

<a id="e015"></a>
### E015 — Own-model version control and complete request lifecycle

- **decision_and_prerequisites:** Video/control-adapter and runtime/proof owners; actual shell/service/job procedure and Q001-Q005 answers. Decide whether own model can be used and updated; no endpoint/SDK method is assumed.
- **actions_and_artifacts:** Issued client registers/uploads V1/hash, waits ready, sends golden, retrieves raw or contractual result. Permitted activate V2, verify revision/hash/known output; finite two-source sequence with IDs/limits. Reuse shared export/compile/numeric/proof chain instead of creating another exporter.
- **outcomes_and_limits:** Working custom lifecycle or precisely missing operation. Catalog-only/no update → R004 or request other grant. Generic vendor example does not close own-version check. Service success shows SSH unnecessary here, not full video SLA.
- **evidence_and_questions:** [F302](RAW_FACTS.md#f302), [F312](RAW_FACTS.md#f312); [Q001](OPEN_QUESTIONS.md#q001), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005).

<a id="e016"></a>
### E016 — Normal lifecycle and host-exception recovery

- **decision_and_prerequisites:** Runtime/recovery owner; current lifetime/recovery contract and E009 sequential golden. Native fault tests only through issued safe scenario. Decide behavior after bounded application events.
- **actions_and_artifacts:** Normal close/reopen/repeat golden; catch input-validation exception **before submit**, then valid request if session permitted. After confirmed completion test ordinary host exception/documented close/new own worker. A short app deadline leaves a collector awaiting late completion with buffers retained. Before generation replacement: stop admission, drain, close, orderly exit. Save phases/first incident packet.
- **outcomes_and_limits:** Only tested normal/host-error path confirmed. Pre-submit exception need not restart; timeout does not cancel or permit duplicate submit; new worker does not ensure native job release. Clean golden failure → administrator with packet, not endless restarts.
- **evidence_and_questions:** [F268](RAW_FACTS.md#f268), [F323](RAW_FACTS.md#f323), [F326](RAW_FACTS.md#f326); [Q015](OPEN_QUESTIONS.md#q015), [Q024](OPEN_QUESTIONS.md#q024), [Q028](OPEN_QUESTIONS.md#q028).

<a id="e017"></a>
### E017 — Supported two-request concurrency

- **decision_and_prerequisites:** Runtime owner; current supported example/contract, permitted allocation and E009 sequential golden. Decide whether this configuration can safely leave serial submission.
- **actions_and_artifacts:** Two separate Inference objects per supplied example; immutable distinct A/B goldens/request IDs and independent output copies. Sequential control → finite thread/async run with at most two outstanding → orderly close → sequential control. Multiprocess is separate if allowed; do not transfer handles by guess.
- **outcomes_and_limits:** Correct results validate that path, not hardware simultaneity/fairness/isolation. Mismatch stops parallel admission, returns sequential and generates incident. Old eight-thread TODO/async declarations are not 2026 validation.
- **evidence_and_questions:** [F316](RAW_FACTS.md#f316), [F321](RAW_FACTS.md#f321); [Q025](OPEN_QUESTIONS.md#q025).

<a id="e018"></a>
### E018 — Actual issued IVA CV PPE deployment

- **decision_and_prerequisites:** Video-adapter owner; Q027 matched rights/bundle with driver/runtime/images/digests/DB/config/models/instructions. Decide whether this particular delivery supplies usable LinQ-backed video/events.
- **actions_and_artifacts:** Inventory bundle; supplied startup MongoDB → Edge-api → project videoanalytics → VDMS-api → UI. Positive/negative clips must produce expected events/coordinates/time and device proof for each NN; then second stream/reconnect. Preserve logs/model versions/event IDs; evaluate UI separately from backend proof.
- **outcomes_and_limits:** Reproducibility of this build, not universal deployment recipe. `0.1.3` + p10 does not establish available registry tag; use issued digest. No bundle → stop branch and transfer lessons to R001/R002.
- **evidence_and_questions:** [F295](RAW_FACTS.md#f295), [F300](RAW_FACTS.md#f300); [Q027](OPEN_QUESTIONS.md#q027).

<a id="e019"></a>
### E019 — Original PDF page interpretation and errata

- **decision_and_prerequisites:** Future documentation-clarification owner; authoritative PDF bytes/page images, unavailable visually in this research. This is a future targeted experiment, not another audit stage.
- **actions_and_artifacts:** Hash original; render actual guide p7/11-14/17/19-21, presentation p2-6, IVA admin p9-18. Save images and old/new transcription for units/tags/footnotes. Request benchmark errata/protocol separately; page image cannot explain measurement scenario.
- **outcomes_and_limits:** Visually supported transcription/correction, not SDK support, metric denominator or registry availability. Remote plain-text response is not viewed page evidence.
- **evidence_and_questions:** [F211](RAW_FACTS.md#f211), [F214](RAW_FACTS.md#f214), [F281](RAW_FACTS.md#f281), [F295](RAW_FACTS.md#f295); [Q031](OPEN_QUESTIONS.md#q031), [Q033](OPEN_QUESTIONS.md#q033).

<a id="e020"></a>
### E020 — Supported cross-chip memory/partitioning of one graph

- **decision_and_prerequisites:** Compiler and runtime owners; vendor-documented partition API/example and allowed configuration. Decide whether one model can span chips; ordinary stress/OOM does not answer it.
- **actions_and_artifacts:** Obtain graph-partition manifest: weights/activations/scratch placement per chip, transfer edges/target mapping. Compare staged golden outputs; larger-than-single-DDR model only under supported memory planning. Measure actual allocation/transfers/useful speed/latency with shared artifact lineage.
- **outcomes_and_limits:** Support for tested model/partition/config or localized failure. Replica E013 does not establish pooling. No example/API leaves `UNKNOWN`, not “unsupported”; total board DDR is not automatically single-model capacity.
- **evidence_and_questions:** [F276](RAW_FACTS.md#f276), [F280](RAW_FACTS.md#f280); [Q017](OPEN_QUESTIONS.md#q017).

## Five expert questions that select the route

These **[UNKNOWN]** answers have the highest architectural impact; ask before reciting the complete 35-Q register. Each question already includes the concrete decision it changes.

1. **What access is actually issued, and how can we run/update our own graph and weights?** Shell/container, server graph compilation, `.tpu` upload, job/file or catalog? Where is compiler and can you demonstrate one supported call? Selects R001-R005 and custom-PPE feasibility. [Q001](OPEN_QUESTIONS.md#q001), [F309](RAW_FACTS.md#f309).
2. **What matched release and target must all five participants use?** Image digest or wheelhouse/lock; compiler/runtime/native/driver/firmware pairing; Python/OS/ISA/licenses and reproduction procedure. Resolves installation/ABI and compile-host choice rather than combining 2025 guide, 2026 benchmark and old pytpu. [Q002](OPEN_QUESTIONS.md#q002), [F329](RAW_FACTS.md#f329).
3. **What exactly is the supported detector's or issued `.tpu`'s I/O and golden recipe?** Names/layout/dtype/shapes/batch, ordered classes/category map, raw heads versus decoded versus post-NMS, color/geometry, exporter source and positive/negative golden tensors. Determines decoder/calibration/evaluation/vendor-smoke usefulness. [Q003](OPEN_QUESTIONS.md#q003), [F242](RAW_FACTS.md#f242), [F251](RAW_FACTS.md#f251).
4. **What quotas, lifetime and networking are allowed?** Payload/in-flight/batch/QPS/shared queue, terminal states/timeout/cancel, CPU/RAM/storage/persistence, worker lifetime/camera reachability/results. No numeric public limits were established. Determines placement/transport/frame sampling/batching/queue/recovery. [Q004](OPEN_QUESTIONS.md#q004), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313).
5. **Which NN boundary must execute on LinQ, and what proof does jury accept?** Host NMS/tracking/secondary NNs; shell versus service-only coverage and completion evidence; accepted witnessed run? Determines graph partition and defense package; no SSH/attestation requirement is presumed. [Q005](OPEN_QUESTIONS.md#q005), [F291](RAW_FACTS.md#f291), [F294](RAW_FACTS.md#f294).

Remaining **[UNKNOWN]** answers are localized, not implied restrictions:

| Decision area | Stable unresolved questions and closure |
|---|---|
| Install/frontend/export | [Q006](OPEN_QUESTIONS.md#q006) actual wheel/native/OS pairing; [Q007](OPEN_QUESTIONS.md#q007) CPU-only build; [Q008](OPEN_QUESTIONS.md#q008) current opset/IR/operator matrix; [Q009](OPEN_QUESTIONS.md#q009) shapes/batch; [Q010](OPEN_QUESTIONS.md#q010) complete matched guide/API example → E001/E002/E004/E007 |
| PTQ numerics/persistence | [Q011](OPEN_QUESTIONS.md#q011) effective percentile; [Q012](OPEN_QUESTIONS.md#q012) thresholds/.qm round trip; [Q013](OPEN_QUESTIONS.md#q013) numeric scheme/QAT/QDQ → E005/E006/E010 |
| Buffers/topology | [Q014](OPEN_QUESTIONS.md#q014) artifact/ABI/schema; [Q015](OPEN_QUESTIONS.md#q015) lifetime/current cleanup; [Q016](OPEN_QUESTIONS.md#q016) device mapping; [Q017](OPEN_QUESTIONS.md#q017) per-graph capacity/partitioning; [Q018](OPEN_QUESTIONS.md#q018) RAW/FULL → E008/E010/E016/E020 |
| Model/proof/measurement | [Q019](OPEN_QUESTIONS.md#q019) exact vendor Tiny; [Q020](OPEN_QUESTIONS.md#q020) custom detector path; [Q021](OPEN_QUESTIONS.md#q021) coverage/completion proof; [Q022](OPEN_QUESTIONS.md#q022) current profiler; [Q023](OPEN_QUESTIONS.md#q023) actual workload performance → E002/E009-E014 |
| Operation/delivery | [Q024](OPEN_QUESTIONS.md#q024) timeout/cancel/recovery; [Q025](OPEN_QUESTIONS.md#q025) concurrency; [Q026](OPEN_QUESTIONS.md#q026) rights; [Q027](OPEN_QUESTIONS.md#q027) IVA PPE bundle; [Q028](OPEN_QUESTIONS.md#q028) engineer/support/allowed recovery scope → E001/E016-E018 |
| Case/source corrections | [Q029](OPEN_QUESTIONS.md#q029) full task/classes/metrics; [Q030](OPEN_QUESTIONS.md#q030) data/cameras/time/rights; [Q031](OPEN_QUESTIONS.md#q031) PDF bytes/images/errata; [Q032](OPEN_QUESTIONS.md#q032) benchmark denominator/units; [Q033](OPEN_QUESTIONS.md#q033) SKU/link/power corrections; [Q034](OPEN_QUESTIONS.md#q034) author experiment attachments; [Q035](OPEN_QUESTIONS.md#q035) Model Zoo license conflict → E001/E002/E011/E019 and authoritative supplied material |

## Handoff to model_stack, data, architecture, rules and product

**[ANALYSIS] → model_stack:** Require exact weights/exporter pins/immutable ONNX plus supported export→frontend→compile path. Keep v8 source-detailed, classic5s artifact-matched and YOLO11 matched-sample candidates conditional. YOLOv5su≠classic5s; OBB/pose≠horizontal detection. `nms=False` retains decode/DFL; 4+nc/5+nc/post-NMS/raw heads need explicit schemas; shape-header patch is not full specialization and symbolic N does not promise batch. Own task/nc/names/category map and all output names. Execute E002/E004/E007 on issued version. [F220](RAW_FACTS.md#f220), [F232](RAW_FACTS.md#f232), [F237](RAW_FACTS.md#f237), [F242](RAW_FACTS.md#f242), [F251](RAW_FACTS.md#f251), [F330](RAW_FACTS.md#f330).

**[ANALYSIS] → data/training/evaluation:** Maintain one camera/clip/time split and preprocessing/golden package; record actual small-object input size/support counts. Evaluate float/export/import/PTQ/device separately; 100/500 are budget experiments. Tiny anchor/NMS/color/geometry confound cross-artifact AP differences. QAT needs working import and measured PTQ limitation; QDQ is unconfirmed. Use E005/E006/E010/E011. [F252](RAW_FACTS.md#f252), [F259](RAW_FACTS.md#f259), [F261](RAW_FACTS.md#f261), [F331](RAW_FACTS.md#f331).

**[ANALYSIS] → architecture/video:** Obtain actual own-model update/select-version, payload/outputs/events, quotas/network/reachability/storage/lifecycle and late-result contract. Our bounded per-camera queues/fair dispatch/`stream_epoch/frame_seq`/clock/version policy is not a claimed vendor feature. Decode/NMS/tracking placement is conditional; HPS/HX codec statements do not establish LinQ H decode. IVA CV is a separate conditional delivery. Use E014/E015/E018 and runtime contracts E008/E016/E017. [F298](RAW_FACTS.md#f298), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313), [F332](RAW_FACTS.md#f332).

**[ANALYSIS] → violation rules:** Object recall is not “person without PPE.” Specify association, zone geometry, true temporal gaps/drop semantics and tracker/class-map behavior at model change. Unknown/lost result is not absence. Obtain mandatory classes and event timing/metrics from Q029/Q030; no required NN inventory or confirmation duration was established. [F261](RAW_FACTS.md#f261), [F332](RAW_FACTS.md#f332), [Q029](OPEN_QUESTIONS.md#q029), [Q030](OPEN_QUESTIONS.md#q030).

**[ANALYSIS] → product/demo/strategy:** Demonstrate source/weights/export/compiled hashes, active revision, controlled input/output/event, trusted device completion and coverage or accepted witness. Identify supplied versus own components. UI “LinQ” is app status, not a device measurement; modern slide speed is a research lead, not SLA. CPU/RTX preparation does not satisfy competition execution condition. Use E009/E012/E014. [F291](RAW_FACTS.md#f291), [F294](RAW_FACTS.md#f294), [F331](RAW_FACTS.md#f331), [Q005](OPEN_QUESTIONS.md#q005).

**[ANALYSIS]** Five functional responsibilities map to the five-person context without inventing identities: environment/access owns one delivery/rights/quota manifest; model/export/compile owns immutable MODEL_MANIFEST; quantization/evaluation/data owns DATA_MANIFEST/effective PTQ/quality gate; runtime/proof/recovery owns ABI/device/I/O/traces/bench/incidents; video/control/rules/UI owns frame→request→model→event. People may combine roles; do not create alternate exporters or independent class maps. Neighboring report locations are unknown; only topic handoffs are asserted. [F242](RAW_FACTS.md#f242), [F261](RAW_FACTS.md#f261), [F326](RAW_FACTS.md#f326).

## Critic disposition trace and research limits

**[SRC/ANALYSIS]** W2 narrowed or corrected W1; historical evidence is retained, not silently rewritten. The 20 critic IDs remain navigable:

| Stable K records | Consequential disposition |
|---|---|
| [K001](CRITIC.md#k001-w2), [K002](CRITIC.md#k002-w2) | Signup/download/device grant still separate; matched current dependency/ABI release unknown |
| [K003](CRITIC.md#k003-w2), [K004](CRITIC.md#k004-w2) | TF namespace/Session false alarms narrowed; guide seams and current frontend matrix remain open |
| [K005](CRITIC.md#k005-w2), [K006](CRITIC.md#k006-w2) | Conditional shortlist; custom adapter defects/spec established, production fix/parity not done |
| [K007](CRITIC.md#k007-w2), [K008](CRITIC.md#k008-w2), [K009](CRITIC.md#k009-w2) | Actual Tiny non-parity; effective PTQ and numeric user/raw contract unresolved |
| [K010](CRITIC.md#k010-w2), [K011](CRITIC.md#k011-w2), [K012](CRITIC.md#k012-w2) | HP01/02 scopes clarified, residual hardware/performance conflicts retained; host-owned output view is not dangling proof |
| [K013](CRITIC.md#k013-w2), [K014](CRITIC.md#k014-w2), [K015](CRITIC.md#k015-w2) | Coverage/completion protocol clarified; SSH not intrinsically required; current concurrency/cancel/recovery unknown |
| [K016](CRITIC.md#k016-w2), [K017](CRITIC.md#k017-w2) | IVA `0.1.3`+p10 correction; explicit Linq TPU connection, exact PPE bundle/video budget unproved |
| [K018](CRITIC.md#k018-w2), [K019](CRITIC.md#k019-w2), [K020](CRITIC.md#k020-w2) | Provenance normalized; layer-specific license evidence; actionable 20E/8R handoff completed, not executed hardware results |

**[LOCAL scope]** Actual checks are public ONNX CPU inference, binary weight/graph inspection and isolated helper/mock probes. No proprietary SDK installation, vendor export/conversion/calibration/compile/TLM, LinQ run, own strict export, RTSP/service/IVA deployment or actual LinQ FPS/quality measurement occurred. Fake native was not loaded as vendor native, ownership probes did not measure native leak/use-after-free, and synthetic Tiny input did not measure accuracy. Full case/data/access/SKU/current ABI/opset/percentile/profiler/grant/accepted witness remain unresolved. PDF original pages and four-NN interview were not visually/audibly observed. [F333](RAW_FACTS.md#f333), [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

**[SRC, workflow context]** Evidence came from 15 separately delegated W1 branches, a fresh-context critic, 13 targeted W2 branches and one access helper; research roles were gpt-6.1-sol medium, analytical/writing roles high. Assembly, human author, language editor and machine compressor used saved materials, with no third search wave or separate final auditor. The saved source-check window is 23 October 2026 04:15-05:14 Europe/Moscow; subsequent writing is not a new verification date. Future supplied release evidence should be recorded with version/date rather than reusing old claims as current validation. [_WORK/RUN_STATE.md](_WORK/RUN_STATE.md), [_WORK/AUTHOR_HANDOFF.md](_WORK/AUTHOR_HANDOFF.md).
