# P0 NVIDIA S02 handoff for Mark Night Shift

Artifact root: `/workspace/artifacts/matvey-nvidia-s02-handoff-20261025-v1/`.
Read its `README.md` and `RECOMMENDATIONS.md`. Shared ready notice:
`/workspace/shared/ml-handoff/matvey-final-20261025/NVIDIA_S02_FILES_READY.v2.json`.

PRIVATE archive: `/workspace/artifacts/matvey_nvidia_s02_nightshift_20261025_v1_PRIVATE.zip`.
90,492,183 bytes; SHA-256
`b4684fc6568781fe997c9edbd6eb9dbbaec0434d04cc029f275e3c9c19c97011`.
93 ZIP members/92 payload SHA checks and CRC PASS;64 text files scanned with
zero secret-signature matches, no runtime/credential files. No public upload.
Receipt is alongside the archive with suffix `.receipt.json`.

Both requested FitA visualizations have been matched to the original clean
ceiling_00 MP4s by all 600 decoded source RGB hashes and native PTS. They are
full 10-second/300-frame GPU captures, not the former mixed-camera montage.
run25 has300 new producerGPU observations; run10 has280 new and20 verified
same-camera/frame/RGB/checkpoint/protocol cached GPU observations. Root made
six actual CPU ONNX parity probes, no GPU/LinQ call, training or staging change.
Twelve actual GPU raw tensor samples are packaged and decode consistently.

## Model and configuration

`ml/models.matvey.nvidia-demo.yaml` and
`ml/profiles/matvey/pipeline.nvidia-s02.local.yaml` are a separate experimental
NVIDIA-demo profile. Stable release registry/profiles are unchanged.

- Model: `matvey-nvidia-fit-a-native-yolov8n@640-c035-native2-demo-v1-7afb8fd728a4`.
- Native class map: **0=forklift,1=person**; `nc: 2`, output`[1,6,8400]`.
- Checkpoint SHA: `7afb8fd728a474fdd08f93b86606ee4512e27dc40535bcf06ee367ea0734f157`.
- ONNX SHA: `f1c5b921e2cb3f2d840dd02378406a807fe38f3777349a603d996adf6c073048`.
- ONNX and checkpoint are under artifact root's
  `models/matvey/matvey-nvidia-fit-a-native-yolov8n/640-c035-native2-demo-v1-7afb8fd728a4/`.
- Full native ONNX is `source_model.onnx`; do not replace it with the one-class
  product export. Tail/program=null; **not TPU READY**.
- `vehicle_classes` includes forklift. No forklift→truck alias.
- This is synthetic-demo-only experimental, not an industrial replacement.

Main94213c5f/techv9 supports custom primarync and name-based people/machinery.
Actual unmodified ModelSpec/JSONL/analysis and localdoctor passed. Version change
invalidates the cache. Use30FPS/step1 and backendlocal,fakefalse for this GPU
import. The profile is global in current Argus; Mark must confine it to the
NVIDIA demo session, without changing the working SIBINTEK profile.

The official ready `argus_demo_pack/manifest.json` can be used with
`safewatch demo import <artifact-root>/argus_demo_pack` in Mark's configured app.
It contains originals and true predictions only. No separate server or ML app
import was started. No backend/rules/main/foreign worktree was changed.

## Actual result and unresolved warning

Unmodified Argus offline replay of the saved predictions:

| Scene | Proximity episodes | Person track frames | Vehicle track frames |
|---|---:|---:|---:|
| run25 | 1 |269/300|259/300|
| run10 | 0 |215/300|270/300|

run25 confirms at frame73/2433ms, auto-calibrated distance. This is an offline
prediction, not a verified Mark API event. run10 has person gap156..237,
30driver-excluded frames and interrupted P observations. Its warning remains
unverified. A saved-observation export at existing tracker floor.1 added only
1/2person track frames and did not change event counts; not promoted.
Mark owns any camera/proximity/driver/hold changes. Do not force or fabricate
an event. Exact trace, settings, source PTS and episode uncertainty are delivered.

Known synthetic source-agent matches atconf>.35/IoU≥.5:
run25 person277/296(FN19),forklift269/300(FN31);
run10 person219/300(FN81),forklift278/300(FN22).
Unmatched proposals2/4 are UNKNOWN, not certified FP. Precision/F1/event quality
NOT_MEASURED: partial source-agent GT is not exhaustive industrial/event GT.
No certified negative scene is claimed. Rule N intervals are explicitly labelled.

Track-review MP4s contain actual observed boxes/IDs and no interpolated missing
boxes; they visibly mark Mark-confirmed event overlay PENDING. Confirmed events,
HUD and effective config with matching sourceSHA/modelref are still needed from
Mark before rendering the final reaction. There is no fresh LinQ on these clips.

Source provenance/license/camera correction and all paths/hashes are in the
artifact manifest.531softwaretestsPASS(4skipped), localdoctorPASS, ONNXcheckerPASS,
six native2 CPU/GPU parity probesPASS. These checks do not establish accuracy.
