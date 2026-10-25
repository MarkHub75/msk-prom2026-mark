# Final model intake — 25 October 2026

All five pretrained checkpoints and Data CPU ABI reports are received and SHA verified. No new model has passed the Training parity/quality intake gates. The stable private release and active
model configurations are unchanged. Main94213c5f/techv9 was fetched and reviewed
read-only; no backend/app/foreign-worktree change or new integration stand.

## Actual incoming model status

| Candidate | Actual checkpoint identity | Intake decision |
|---|---|---|
| nobita111222/fire-smoke-yolov8n | b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f | Exact byte duplicate of existing fire/smoke. Reuse640-s04-v1-4c9f5d05c4d4, existing ONNX/video/metrics; no new model/version or repeated experiment. False headlights/equipment alerts remain. |
| iam-tsr/yolov8n-helmet-detection | c8eb324e365cf4faeab491d9cc301535ec745171b55e8b1acadea62be5101a9d | Data restricted CPU ABI PASS only. Source0With Helmet/1Without Helmet. Await Training real-input ONNX parity, measured comparison and video outputs; verify head-region versus whole-worker box semantics before Argus alias/association. Stable Helmet retained. |
| keremberke/yolov8n-forklift-detection | 0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38 | Data restricted CPU ABI PASS; rights remain on hold and Training ONNX parity/video quality are absent. No ModelSpec activation or TPU readiness. |
| keremberke/yolov8s-forklift-detection | 30b6148f970cbe78b783dc6c65d9a8f2ef96298fc9d82909f2adf1c043ab4a95 | Data restricted CPU ABI PASS; rights remain on hold and Training ONNX parity/video quality are absent. No ModelSpec activation or TPU readiness. |
| luiscrmartins/yolo11n-trained-ppe-model/PyTorch/default/1 | b721e82d8497148a4346aad1fe7199aba51279bb2e1db13fe66a8c650250f740 | Data CPU ABI PASS10classes. Await Training ONNX parity, real video/quality. Native0Hardhat/2NO-Hardhat may support helmet/no_helmet only after association review. Mask is not respirator;Machinery/Vehicle are not forklift;Person does not replaceCOCO80. |
| Targeted fine-tune matvey-forklift-yolov8n@640-targeted-row-v1-9f8536d5d58d | 9f8536d5d58d8a24e25a5d154515351bf0e4d6dec2b607470188d6e7fe87bd00 | REJECT. SourceF1.761905 below.82 gate; press proposals261/261 remain. Real ONNX parity passes93frames, which does not override failed quality. No activation. |

The new Factory-ne9pd native4-class and Factory-glvmn2-class packages are
RESEARCH_TRAIN_READY inputs, not trained model releases. Their validation is
source DEV with only8forklift GT boxes; no proximity-event GT or independent
industrial accuracy. Preserve native forklift/helmet/jacket/person IDs; jacket
is not vest, helmet absence is not no_helmet. NVIDIA source synthetic metrics
remain separate; final Data wrapper now supplies38train/40DEV images from2existing original syntheticMP4s. Its IDs are0person/1forklift, reversed relative to pretrained0forklift/1person; explicit head reorder/reset and a new model classmap are required. No new independent industrial test or trained model is supplied.

## Verified stable evidence and integration

The unchanged COCO80 full ONNX9c97d577... now has Training's real9-frame native/
ONNX parity:0changed decisions at.1/.25/.35. This is an evidence update, not
new model bytes or a quality gain; its canonical version stays unchanged.

Already available to Mark/Egor:
`/workspace/artifacts/matvey-release-final/matvey_final_private_handoff_20261025_v1.zip`
(176139796bytes,SHA3640159067ce7b4526c78fe8bd0eb8671f5ea1704ac3409f99c9607579a6036a).
Use stable local config `ml/pipeline.matvey.stable.yaml`; captain keeps the
working baseline LinQ pair. Phone/newForklift/PPE replacements remain inactive.
No GPU-only source model is TPU READY. No new hardware research or request.

Actual ML import defect fixed: lowercaseS07 andS02 no longer silently becomeS04.
The converter preserves explicit scenario_id/official_scenario, supports legacy
UR andS01–S08 IDs, and rejects unknown/conflicting metadata. This changes only
scene metadata, not neural outputs, external event schemas or Argus rules.

531software tests pass(4skipped); the3new checks cover that routing defect.
They establish software behavior, not recognition accuracy.

## Release isolation correction

The old expanded contract-phone-v1 document was hardlinked to working
`docs/ML_HANDOFF_MATVEY.md`; our earlier P0 update unintentionally changed both.
The issued ZIP was intact. Restored the old document byte-for-byte from the
verified ZIP and detached13tracked working files from release hardlinks without
content changes. All348old payload hashes and93private-payload hashes now pass.
The changed document was preserved in the intake artifact folder as an audit.
Explicitly authorized pruning of external historical raw files is recorded by
Data; it is not described as loss inside either verified release archive.

## Producer handoff and freeze

Root consumer ACKs and requirements are under
`/workspace/shared/ml-handoff/matvey-final-20261025/`:
`FINAL_MODEL_INTAKE_ACK.v1.json`, `FINAL_MODEL_INTAKE_REQUEST.v1.json`,
`PRETRAINED_FIRST_CONSUMER_ACK.v1.json`, `PRETRAINED_FIVE_CONSUMER_ACK.v2.json`.

Final provider release is WEIGHTS_MANIFEST.json plus TRAIN_READY.json(02:13UTC), acknowledged in PRETRAINED_FINAL_DATA_CONSUMER_ACK.v1.json. All five checkpoint hashes were checked; no accepted Training model is implied. Earlier CPU snapshot is WEIGHTS_FIRST_READY.v3.json. Its CPU forwards are
Data operations, not root model inference, ONNX parity, measured quality or TPU
qualification. Latest Data retractions override prior READY: helmet-evxi3 and
factory-ms6xz are now NEEDS_FIX, as is factory-u8ib6. Do not use the retracted
packages for quality selection or declare burned-in labels/source splits human
event GT. Factory-ne9pd/glvmn READY remains a training-input status only.

For each later accepted model: immutable checkpoint/productONNX/SHA/class maps,
actual real-input parity and measurements → new ModelSpec/version/separate
pipeline → local doctor and real MP4/JSONL → unchanged Argus event review →
conditional LinQ proposal. No production promotion from weights/download or
compiler status alone. Failed or unissued candidates stay out of stable config.

08:00MSK(05:00UTC) freezes architecture: thereafter regression, packaging and
handoff only. Root has not launched competing GPU training or source discovery.
Actual access to staging and captain baselinePose tail bytes remain with captain;
no separate stand is created to work around missing access.
