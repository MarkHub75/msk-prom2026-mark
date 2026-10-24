# MOSPROM final video-first handoff — 24 October 2026

The ready local package is `/workspace/artifacts/matvey-final-20261025/video-first-v2/`.
Read its README.md, FINAL_ML_EVIDENCE.md, MODEL_REGISTRY_HANDOFF.md,
VIDEO_MANIFEST.json, SCENARIO_COVERAGE.json and REPRODUCE.md. The previously
issued `matvey_final_v1.zip` remains unchanged.

Seven NEW complete real scenes were consumed from immutable Training outputs:
four S04 fire/smoke/control clips,1983frames/3966CUDA calls; three S07 UR previews,
665frames/1330CPU calls. A foreign GPU job was present for the latter, so no CUDA
allocation was attempted. Every original source RGB/PTS/input/raw/decoder binding
was checked. No held/interpolated detections, no fresh TPU calls. The selected
new package also includes three previous full scenes:10scenes/3297frames/7243calls.
Original MP4 bytes are retained where available. FIRESENSE originals are AVI,
with prior complete MP4 playback derivatives; UR clips are preexisting lossy RGB
crop previews, explicitly not native originals. SHA and rights travel with each.

New verified model: `matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4`,
extra detect,0smoke/1fire, FP32 static640→[1,6,8400],conf.25/iou.45. The pinned
checkpoint is b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f.
ONNX real-frame parity passed12inputs with0changed decoded decisions. Local-only
registry addition is ml/models.video_first.yaml; weights/ONNX/head/tail are outside
Git in new_fire_model/. No training, paired improvement or new TPU qualification.

The unchanged Argus main f6b5358a contract SHA remains
f26c4351739fd1faccb1a2a47599773414061e100393b8e12dbe80e55732e828.
Exact names agree with ML_INTEGRATION.md. Mark owns all rules/backend/UI; none
were edited. New actual normal Argus local job on smoke:408CPU ONNX calls,
204of407sourceframes/model,48.434s processing,1episode/1persisted event/1JPEG,
APIevents/detail200. Own isolated SQLite and outputs are actual_argus/S04_smoke/.
The older actual S02 CPU114call job is preserved separately. No production/staging
or UI acceptance is claimed, no caches or GT events injected.

Source detection metrics on30fixed provided DFiretest files: smoke GT6,TP5/FP1/FN1,
F1.8333; fire GT14,TP13/FP2/FN1,F1.8966. MacroAP50.8636202,AP50:95.4696761,
101point source evaluator. Original membership/model overlap and human annotation
exhaustiveness UNKNOWN; these are not independent industrial/event metrics.
Eight declared-train RGB calibration candidates remain explicitly UNAPPROVED.

Three available presentation sets: demos/S04_fire/, demos/S04_smoke/ and
 demos/S02_equipment/. They cover two official directions, not three independent
quality-qualified scenarios. Fire/headlight false alert is retained. S02 has no
appropriate distance/policy/negativeGT. PPE is an additional model visualization,
without a PPE rule in current Argus. All target-event metrics remain NOT_MEASURED.

S07 is NOT accepted as a successful current Argus demo: sourceFall03 missed,
ordinaryADL01 noepisode,bedADL10 alert. Saved actual COCO80 has bed59/couch57 on
257of300bedframes, excluded by current productfilter. Exact class agreement and
rule handling are pending Mark; no silent filter/rule changes. Removing pose in
one saved-output diagnostic did not resolve the outcome. Historical complete-clip
GMD P(Fall) separates these3source categories, but is noncausal and not a YOLO
ModelSpec or new event result. Source referenceJSON is included separately.

All eight historical observation prototypes remain executable. Current main model
availability/quality is represented honestly in SCENARIO_COVERAGE.json. New Data
notices19:04/19:20UTC offer research-only forklift/person train295/val84 and ABI-only
cigarette checkpoint; no verified Training-quality release yet. Forklift0/person1
is not a COCO80primary replacement or an agreed truck alias. Read-only receipt
provenance/LATEST_DATA_TRAINING_RECEIPT.json records this dependency. No automatic
training or foreign worktree changes.

Software:528testsPASS,4skipped,7.521s in existing linq-client env. The first final
suite attempt used the app-contract env with missing PIL/pika/jsonschema; failed
import log is retained, no dependency installation. Actual app used its existing
contract runtime. Root changes only adapters/model registry/local isolated test/
renderer metadata; explicit actual off-image predicted COCO17 values are retained.
A CUDA label in three generated CPU summary headers was corrected before release;
per-frame origins and numeric outputs were already correct.

LinQ remains blocked for new submissions: no own Matvey staging receipt and no
approved fire calibration. No compile/staging/program was created. Historical
Helmet/SplitPose15real TPU calls/13unique sourceframes and raw-tail checks remain
available under linq_historical/, clearly historical. Full new numeric raw trees
stay in place under `/workspace/artifacts/matvey-video-first-20261025/`, referenced
by immutable Training handoff SHAa578f4d538d6c5a32a5a761034b85d8f7cc50364a9589325d1b51afaa566954b.
They are about8.3GB and intentionally not duplicated in the ZIP. No off-host
binary backup is verified. Data/Training delegates completed, no own model jobs.
Final archive hashes/commit receipts live next to the package; see the release
checkpoint for the final exact SHA. Push only matvey_cv without force.
