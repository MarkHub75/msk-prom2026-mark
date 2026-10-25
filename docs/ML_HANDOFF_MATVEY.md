# ML handoff for Mark — final contract and Phone candidate

## Final integration configuration — 25 October

Use [FINAL_INTEGRATION_READINESS_20261025.md](handoffs/FINAL_INTEGRATION_READINESS_20261025.md)
for the current model connection instructions and verified RC. Four existing
ModelSpecs are provided by `ml/models.matvey.release.yaml`; six ML profiles live
under `ml/profiles/matvey/`. Stable default retains COCO80, Matvey Pose and Helmet;
Fire is optional local demo only. No new experimental checkpoint was promoted.

Current main94213c5f:6doctor checks/6model API200,8ONNX checks,531software tests
PASS(4skipped). Three real CPU jobs:800calls,2persisted events/evidence/API200;
S07 reference still missed, not quality accepted. No new GPU/TPU calls or writes
to captain/backend/main/LinQ staging. The next immutable Training progress
handoff was reviewed once; no accepted replacement. Exact SHA, absolute/portable
paths, versions, frame gaps and original PTS are in the single RC and its ZIP.

## P0 final delivery — 25 October

Current handoff: [LINQ_FINAL_LIVE_HANDOFF_20261025.md](handoffs/LINQ_FINAL_LIVE_HANDOFF_20261025.md)
and [FINAL_MODEL_STATUS.md](handoffs/FINAL_MODEL_STATUS.md). Main94213c5f/techv9
was reviewed read-only. Captain confirms S28/R32 live LinQ; no repeat run or
additional integration stand was started. S28/S29 have implemented the older
nc/input_name, optional-tail, providers, timeout, importer and extra-fallback gaps
listed in the historical434b review below.

PRIVATE payload: `/workspace/artifacts/matvey-release-final/mark-private-v1/`.
Existing runner ZIP and original producing-agent handoff were found and hashed.
Five unique checkpoints, six ModelSpecs and twelve ONNX files are present; all
ONNX files pass static checks without inference. The separate local stable
profile is `ml/pipeline.matvey.stable.yaml`; the older default Matvey YAML remains
an explicit fire evaluation profile. Phone and rejected Forklift/PPE replacements
remain inactive.

Critical missing file: captain's baseline three-output Pose640 tail is not
available here. Its expected path is
`models/linq/pose640_cut_ap9999/pose640_cut_ap9999_tail.onnx`.
Our608-byte four-input Split-Pose tail is incompatible with that program.
Keep captain's already-working baseline pair. No replacement/recompile or
unverified remote placement is claimed. Exact per-model hashes, source metrics
and missing dependencies are in the new handoff. No public media upload occurred.

The previous434b evidence and measurements below remain historical records.

Latest verified main: **434b0f75d66a46b5fc15294562e8d69ed170d175**, tech.md **v6**.
Read `/workspace/shared/contracts/MATVEY_CONTRACT_v1.md` in full; its SHA256 is
9893f941a8e1c1ea4adf1343218c75edfe05d9735c77ffce63548c1f366f0ac1.
LinQ_CONTRACT controls hardware; tech.md controls other disagreements; the older
ML_INTEGRATION.md still describes several pre-v6 limitations. Source snapshots
and exact document pins: `/workspace/artifacts/matvey-contract-v1-20261025/contract/`.
No application source, main branch, backend, external schema or production DB was changed.

**S08 `load_carrying` is NOT implemented in Argus.** Its plugin has status
`skeleton` and `observe()` returns `[]`. Historical eight ML observation prototypes
and software acceptance cases do not implement this application scenario. Do not
report eight quality-qualified working Argus scenarios.

## Files Mark can read from matvey_cv

- `ml/models.matvey.yaml`: six immutable ModelSpec records, integer class IDs.
- `ml/pipeline.matvey.yaml`: tested local evaluation profile, COCO80 + Pose + Helmet + fire/smoke.
- `ml/demo.matvey.yaml`: six real source videos for the actual local demo build.
- `ml/pipeline.matvey.phone.experimental.yaml`: isolated experimental Phone profile.
- `ml/pipeline.matvey.linq.example.yaml` and `ml/demo.matvey.linq.example.yaml`:
  conditional existing-common-program LinQ build, **not executed live here**.
- `ml/reports/phone-integration-20261025.json`: source metrics and video-transfer decision.

Merge records by `id@version`. Matvey Pose/Helmet are already registered in main:
retain identical records instead of appending duplicate references. Never replace
different bytes/maps/thresholds under an existing version. Lists such as
`pipeline.extra` are replaced wholesale; preserve the agreed composition deliberately.
Application policy, zones, delivery and restart remain Mark's responsibility.

## Exact models and physical binaries

| Model reference | Role / class map | Evidence and readiness |
| --- | --- | --- |
| `coco-reference-yolov8n@640-v1-a6a8c37f7e45` | primary, actual dense COCO80 output; retained IDs0person/2car/5bus/6train/7truck/67`cell phone` | unchanged official weights, local ABI and real video verified; no new Matvey TPU capture |
| `matvey-pose-yolov8n@640-v1-acc5f51228b9` | pose,0person/COCO17 | unified full ONNX[1,56,8400] and actual four-output TPU→tail historical evidence; new placement not verified |
| `matvey-helmet-yolov8n@640-v1-5c3af1f3b855` | extra,0helmet/1no_helmet | stable baseline retained; v6 no_helmet plugin exists; site/event quality not independently established |
| `matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4` | extra,0smoke/1fire | actual local ONNX/video/source metrics; headlight and equipment false-alert risks retained; no new TPU |
| `matvey-phone-object-yolov8n@640-contract-v1-7115481796de` | experimental extra,0`cell phone` | new trained checkpoint/ONNX/source gain verified, weak video transfer; **inactive in default profile** |
| `matvey-phone-eval-coco-person-vehicles@640-c010-no67-v1-dc6f449a09f7` | diagnostic primary, same COCO80 weights with ID67 filtered | distinct ID/version/cache, only to isolate the Phone candidate; stable primary weights are not replaced |

All `local_onnx` paths now exist with verified bytes under
`/workspace/project/models/matvey/`. They are ignored binaries, not Git content.
Exact paths, hashes and model fingerprints are in the artifact manifests:
`/workspace/artifacts/matvey-contract-v1-20261025/MATVEY_MANIFEST.json` and
`/workspace/artifacts/matvey-phone-integration-20261025/MODEL_INTEGRATION.json`.
The first manifest describes the initial four-model contract check; Phone/diagnostic
records are added by the final release manifest. Full ONNX, source graph and decoder
projection remain separate files. Compilation, placement and actual TPU execution
are separate gates. Canonical historical program names in Pose/Helmet ModelSpec do
not prove those names were newly staged. Local-only models keep `linq_program:null`.

Phone best PT SHA256:
`7115481796ded62b8854c51f42897dba714640623bdbdff2ca36480c9faba3e7`.
Canonical product ONNX SHA256:
`d15369d253141315281d59cd93ef0f2c58de7425f72ccd0cd2294a6385f8f1c7`.
Source ONNX SHA256:
`420023c48c993dd2bb87ba1c8b2edaea63a5ff8dde720d302f54cb2d8caafd61`.
Native FPI classes are **phone0/face1**; face is not person. Product output is
FP32 `images[1,3,640,640] → decoded[1,5,8400]`, **cell phone0** only. The graph
preserves native two-class argmax before filtering: if face wins, phone score is
zero. Simply deleting the face channel changes decisions and is invalid.
Recording floor .25, NMS .45; actual rule threshold `cell phone:.30`. A real
current-scene ONNX CPU probe and the supplied 127-frame export parity both pass.

No new accepted PPE replacement was published. PPE17/PPE19 and the newly trained
PPE replacement remain rejected. Respirator/no_respirator and no_harness are not
invented from mask, harness-present or missing labels. GMD scalar heads are not
YOLO extras. Do not register fictional objects or convert their logits into events.

## Real application and demo proof

`/workspace/artifacts/matvey-contract-v1-20261025/doctor_v6_v1.log`: actual
`safewatch doctor`, exit0, four local ONNX files found. Phone-specific doctor:
`/workspace/artifacts/matvey-phone-integration-20261025/doctor_phone_v1.log`, exit0.
All model shapes/classes and version-change cache invalidation were checked.

New normal Argus v6 smoke job: **816 actual CPU ONNX calls**,204/407frames per
model,96.664s processing; event1/evidence1/API200. Files:
`/workspace/artifacts/matvey-contract-v1-20261025/matvey_argus_v6_smoke_v3/`.

Actual `safewatch demo build` with local/fake=false: **6 videos,2580 sourceframes,
6060 CPU model calls,24 validated model JSONLs**. Then actual `demo import`, six
cached-only jobs, real-clock broadcasts, event5/evidence5/API200, SQLite integrity
ok; **zero new inference during import**. Pack:
`/workspace/artifacts/matvey-contract-v1-20261025/demo_local_v1/`.
Proof: `demo_import_check_v1/validation.json`, `events.json`, `coverage.json`,
`api_readbacks.json` and the isolated app database. Events are four fire_smoking
and one proximity predictions. Fire also triggers in the equipment context;
headlight false alert is retained. Helmet is formally active but no accepted
helmet event was produced. The illustrative helmet-required zone is demo policy,
not enterprise GT. Do not call these events verified violations or TPU results.

The new v6 dependency imageio-ffmpeg0.6.0 was installed only into the owned artifact
runtime_deps directory from the main uv.lock wheel with verified SHA. Existing
PyTorch, preparation, SDK and application environments were not modified.

## Phone: actual source comparison and full videos

Training's reported .35955→.765625 compared the task-adapted two-class baseline
with fine-tune. Root additionally ran the **unchanged COCO80** on the same127FPI
validation files. At conf.30/NMS.45/matchIoU.5:

| Model | GT phone | TP | FP | FN | Precision | Recall | F1 | AP50 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| unchanged COCO80 phone67 |67|16|6|51|.7273|.2388|.35955|.39668|
| fine-tuned Phone |67|49|12|18|.8033|.7313|.765625|.79834|

The unchanged COCO operating-point counts happen to equal the adapted baseline;
identities are separate and their AP differs. This is source validation used in
development, not an independent industrial benchmark or phone-use event score.
Source annotation completeness/training overlap remain limited. Candidate FP
count doubles6→12 at the stated point; the gain is not a production guarantee.
Numeric FP/FN examples, raw and inputs:
`/workspace/artifacts/matvey-phone-integration-20261025/coco_fpi127_v1/`.

Four NEW complete scenes: **1539frames×3models=4617 actual CUDA calls**,398.159s,
no skipped/interpolated/tracker-carried neural rows. Original GMD/Mendeley MP4s
are byte-identical copies. MEVA originals are AVI; the two action-segment MP4s
are explicit lossless RGB derivatives,963/963source/roundtripRGB matches. Original
source frame/PTS and derivative frame/PTS are retained separately. Immutable index:
`paired_videos_v1/CONSUMER_RUNS.FINAL.v1.json`, handoff SHA
`2e7d717ee651b8b02b4ee9cbdc7576b224f02600790785a61ad069b2ec541f67`.
Per-scene sources, annotated MP4, three Argus JSONLs, confidence, COCO17, raw,
input hashes and coverage are under `paired_videos_v1/scenes/`.

At .30 the candidate produces only one proposal in GMD; COCO produces zero.
Neither detector proposes phones on the other three scenes. GMD's phone hint is
not GT. MEVA G506 has source phone actions; G331 has a document actor coexisting
with phone actors, **not a negative scene**. Mendeley is an unlabelled industrial
context, not a confirmed phone-negative. Exhaustive industrial phone-bbox/event
GT and labelled tool-negative video are unavailable. Keep FP/FN/event F1
NOT_MEASURED there rather than manufacturing negatives. Book/tool controls and
any bounded source-still diagnostic have separate scope in the final report.

Actual unchanged Argus compared both detector profiles on every frame, with
shared actual Pose. Candidate evaluation filters primary67 under a NEW reference,
so a COCO phone cannot be credited to the extra. Read-only return profiling
records exact `attach_objects` and PhonePlugin outputs; no rule was replaced.
Candidate's one score.30456 proposal attaches to track1, yielding one P observation;
**baseline phone episodes0, candidate phone episodes0**. Actual defaults are
hold10s/danger_hold3s/min_person120px/upper_frac.6/wrist_dist_bh.25. The supplied
contract's approximate80px is not the pinned configuration; no parameter was
lowered to force an event. Rule N/U/P traces are predictions, not GT labels.
Results: `argus_paired_v1/SUMMARY.json`, per-scene `phone_association.jsonl`,
`analysis.json`, `events.json`. Event accuracy remains NOT_MEASURED.

A separately frozen source control set contains12 unchanged COCO128 images:
book,scissors,knife,remote,laptop;8with people, no source phone67 annotations.
Actual24CPU ONNX calls at.30: unchanged COCO phone proposals0; candidate3 on2images.
Visual review shows game/TV remotes at scores.7216/.8524 and a hand-region proposal
at.3516. Book/tool sample gave no phone proposals. This is source-file diagnostic,
with COCO pretraining overlap and unknown human exhaustiveness, not an independent
industrial false-alert rate. Inputs, source labels, raw, annotated FP images and
review: `hard_confusors_intake_v1/`, `hard_confusors_results_v1/` under the Phone root.
No still images were repeated into fake videos. Annotated tool-negative MP4 GT
remains unavailable. Raising a threshold was not used to hide these failures.

**Decision: Phone is EVALUATED_SOURCE_ONLY / FROZEN_EXPERIMENTAL.** It is not
activated in the stable pipeline and does not replace the COCO detector. No new
ROI/confidence/tiling hypothesis was run; previous ten video/ROI runs are retained.

## JSONL, PTS and cache

Actual per-model JSONL is exactly `frame_idx,ts_ms,detections[cls,name,score,
bbox_xyxy,kpts]`; original-frame pixels,17COCO triples for Pose. `name` is ignored
by Argus; ModelSpec numeric map is authoritative. Empty processed frames have a
real empty row. Missing frames are listed separately, never filled as predictions.
Phone full-scene JSONLs preserve precise encoded scene PTS. The normal local
backend rounds ts_ms to0.1ms; `coverage.json` also retains exact ffprobe PTS for
every source frame. MEVA native source PTS/ordinal are not confused with segment PTS.

The cache omits weights/classes/conf/IoU. New model, projection, mapping, threshold,
preprocess or ROI policy needs a new immutable version/fingerprint. The Phone and
no67 diagnostic refs differ from old cache references; version invalidation passed.
Hashes belong in MATVEY_MANIFEST, not invented ModelSpec fields.

## LinQ route and requested application fixes

No new TPU request, upload, compile or PTQ occurred. Historical15real TPU calls/
13unique sourceframes are preserved and their JSONLs pass the new reader at
`/workspace/artifacts/matvey-contract-v1-20261025/historical_TPU_JSONL/`.
These sparse captures are historical, not a fresh/full LinQ video run.

LinQ Agent report: `matvey-contract-v1-20261025/linq/ROUTE_HANDOFF.v1.md`.
The actual route is Matvey's existing laptop VPN gateway → existing SSH tunnel →
authenticated Jupyter → RabbitMQ, video inference inside Jupyter. This Vast process
has no configured Jupyter runtime keys or own new staging receipts; current TPU
availability is UNKNOWN. No gateway/tunnel/service/foreign queue was changed.
Future own execution: unique matvey directory/file prefix, inflight1 and root gate.
Legacy uploader's documented namespace exception was not exercised.

Phone SDK static preflight: `matvey-phone-integration-20261025/linq_preflight_v1/`.
Native real cuts: `/model.22/dfl/conv/Conv_output_0`[1,1,4,8400] and
`/model.22/Sigmoid_output_0`[1,2,8400]. CPU tail must decode AND preserve native
phone/face argmax then project phone0. The supplied1160B decoded-output projection
is **not a LinQ cut-tail**. Industrial admission, approved train/calibration groups,
actual compile/simulator/placement/TPU remain open. Weak video transfer means no
production LinQ release is approved from this source F1 gain alone.

Concrete application gaps at tested main434b, for Mark only:

1. `import-artifact` CLI is still absent; service `artifact_import` exists. Its
   metrics=None path assumes the current analysis step, which can mis-key sparse
   historical outputs. Expose/validate true cadence or require supplied metrics.
2. nc/input_name and local.providers exist in schema/specification but are not yet
   wired by the corresponding backend; current local runtime is CPU. Our primary
   remains COCO80 and input images, so this does not block current local models.
3. Optional-tail, adaptive timeout/--reply-timeout, extra-error fallback and extra
   metrics are not all implemented yet. New Phone has no TPU program/tail; do not
   switch it to LinQ based on schema alone.
4. `load_carrying` remains skeleton. Model registration does not implement S08.
5. Review strict Matvey namespace/durable-request handling before live remote
   execution; existing uploader stages under mosprom_work and forces mosprom_;
   app reply identities differ from the isolated root journal. No unisolated call
   was made to bypass this review.

No source fix is applied by this branch. Final archive paths, verified digests,
commit and publication receipt are recorded in the release checkpoint.
