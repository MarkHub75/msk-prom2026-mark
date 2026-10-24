# CV Detection implementation

Public API is `preprocess(rgb_uint8_hwc, manifest) -> (tensor, LetterboxTransform)` and `decode(outputs, manifest, transform) -> list[dict]` from `ml.detection`. `NativeReferenceBackend(weights, manifest, device='cpu').infer(request)` is explicitly PyTorch, with no LinQ fallback.

## Model manifest

Required fields: `model_id`, `input` (`name`, static batch-one `shape`, `layout`, `dtype`, `scale`), `decoder`, ordered `classes`. Optional `output_name` is mandatory for multiple-output mappings. `output_layout` is BCN for YOLOv8 and BNC for classic YOLOv5. `thresholds` provides confidence, IoU, max_detections. Pose uses COCO-17 x/y/score. The input is RGB, centered letterbox with value 114, Pillow bilinear resize; exact rounded dimensions are retained for inverse coordinates. This is our explicit recipe; it does not claim pixel equality with OpenCV letterbox implementations.

`detect_v8` and `pose_v8` consume decoded xywh/probabilities. `detect_v5` multiplies objectness by class score. Sigmoid/DFL/anchor/stride decode must already be inside these graphs. Raw conv heads, embedded-NMS and end-to-end outputs are rejected rather than guessed. Host NMS is stable and class-aware. Float raw outputs are required; vendor raw integer packing requires the vendor-supported conversion before this decoder.

## Reproduce export and parity

Use an isolated preparation environment with the compatible installed torch/ultralytics; do not install export dependencies into the TPU compiler environment. Current preparation run used `/workspace/.venv-cv-prepare/bin/python`, Python 3.12.15, torch 2.14.1+cu126, ultralytics 8.4.184, onnx 1.23.2, onnxruntime 1.31.0. These versions are not claimed compatible with LinQ SDK.

```bash
python -m ml.detection.export --weights /path/to/trusted/pose.pt --output /path/to/artifacts/pose --model-id pose-v1 --decoder pose_v8
python -m ml.detection.export --weights /path/to/trusted/helmet.pt --output /path/to/artifacts/helmet --model-id helmet-v1 --decoder detect_v8 --class-map '{"Hardhat":"helmet","NO-Hardhat":"bare_head"}'
python -m ml.detection.verify --manifest /path/to/artifacts/pose/manifest.json --image /path/to/image.jpg --device cuda:0 --output /path/to/parity.json
python -m unittest discover -s tests -p test_detection.py -v
```

Only trusted `.pt` weights should be deserialized. Export writes owned copies of weights, ONNX and a manifest with SHA256, actual names/shapes, class map, versions and `linq_status=NOT_RUN`. Export and ONNX checker success do not establish TPU execution. Calibration data and TPU hashes must be added by the LinQ compiler stage.

## Actual preparation evidence, 2026-10-23

Artifacts are outside Git at `/workspace/artifacts/detection/`:

| Artifact | Source | SHA256 |
|---|---|---|
| helmet.pt | keremberke/yolov8n-hard-hat-detection HF revision `287bafa2feb311ee45d21f9e9b33315ff6ff955d`, best.pt | `05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c` |
| pose.pt | ultralytics/assets release v8.3.0, yolov8n-pose.pt | `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212` |
| bus.jpg | ultralytics/ultralytics tag v8.3.0, ultralytics/assets/bus.jpg | `c02019c4979c191eb739ddd944445ef408dad5679acab6fd520ef9d434bfbc63` |

Both models loaded, exported with static input `[1,3,640,640]`, opset13, and passed `onnx.checker`. Pose output is `[1,56,8400]`; helmet output is `[1,6,8400]` with classes `helmet,bare_head`.

Paired CPU PyTorch vs ONNX CPU inference on the same prepared bus image passed `atol=1e-3, rtol=1e-3`: pose max absolute error 0.000847, 3/3 post-NMS detections; helmet 0.000946, 1/1 detections. Initial CUDA defaults failed raw tolerance (max errors 0.302 and 0.508). Disabling TF32 for paired verification fixed this: pose CUDA max error 0.000710 and helmet CUDA result recorded in parity-cuda-fp32.json. The verify tool explicitly disables TF32; normal reference execution leaves application precision policy unchanged.

These are single-image numerical checks, not accuracy, latency SLA, steady throughput, industrial generalization or LinQ validation. The bus image is not a target helmet/fall evaluation set. Positive/negative target footage and TPU parity remain required. No compiled TPU program, calibration run or actual LinQ inference has been performed by this component.

Weight/dataset rights must be tracked separately from code provenance before redistribution or commercial use. Download links are reproducible provenance, not a blanket license grant.

## Corrective split pose graph for PTQ

The original combined pose graph is retained. A measured vendor quantizer issue assigned coordinate-range scale to keypoint confidence channels, collapsing them to zero in simulation. The corrective export exposes **upstream tensors before mixed concatenation**, rather than gathering from an already mixed graph output:

```bash
python -m ml.detection.split_pose --manifest /workspace/artifacts/detection/pose/manifest.json --output /workspace/artifacts/detection/pose-split
```

`split_pose_v8` requires a named output mapping defined by `split_outputs` in manifest:

| Semantic | Actual source tensor | Shape |
|---|---|---|
| boxes | `/model.22/Mul_2_output_0` | `[1,4,8400]` |
| class_scores | `/model.22/Sigmoid_output_0` | `[1,1,8400]` |
| keypoint_xy | `/model.22/Mul_4_output_0` | `[1,17,2,8400]` |
| keypoint_scores | `/model.22/Sigmoid_1_output_0` | `[1,17,1,8400]` |

The graph-surgery helper discovers these tensors through the final Concat -> keypoint Reshape -> keypoint Concat structure, validates the probability Sigmoid producers, and extracts a backward-reachable subgraph. Both mixed `/model.22/Concat_4_output_0` and terminal `output0` are absent from the new graph. All coordinate decoding and sigmoid operations remain inside ONNX. Host code only concatenates and reshapes the four already-decoded outputs before applying the existing NMS/geometry decoder.

Actual artifact `/workspace/artifacts/detection/pose-split/weights.onnx` SHA256 is `802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00`. ONNX checker passed. Original vs split float ONNX on the same bus image was bit-identical (maxabs 0, three identical post-NMS detections); keypoint probabilities ranged from 0.00341755 to 0.99890792 across all anchors. Evidence is `pose-split/graph-parity.json`. This establishes graph-surgery correctness for that input; vendor quantization, compiler, simulation and device execution must be checked independently by LinQ Integration.

## Compare exported numeric runtime captures (CV-02)

`ml.detection.compare_capture` compares already-captured named tensor arrays. It does not execute a model and cannot establish that the source was real hardware. Capture format agreed with LinQ Integration is `capture.json`, `inputs.npz`, `outputs.npz`. NPZ keys are exact tensor names; arrays are real numeric data only. Loading always uses `allow_pickle=False`; object/string/complex arrays are rejected. Never export notebook locals, session objects or unfiltered outputs.

```bash
python -m ml.detection.compare_capture \
  --reference /path/to/golden-outputs.npz \
  --actual /path/to/capture/outputs.npz \
  --manifest /path/to/model/manifest.json \
  --metadata /path/to/capture/capture.json \
  --output /path/to/comparison.json
```

If runtime tensor names differ, supply an explicit JSON map through `--name-map` or `capture.json`'s `runtime_to_reference`. Direction is **actual runtime name -> reference name**. Without a map only exact identity names are accepted. Unmapped or extra tensors, duplicate map destinations, nonfinite values, different shapes or different dtypes invalidate the capture comparison. Raw integer TPU codes must first be converted through the verified runtime ABI; this tool neither guesses scales nor silently casts mismatching dtypes.

API: `compare_captures(reference, actual, runtime_to_reference=None, manifest=None, metadata=None, relative_epsilon=1e-8, min_match_iou=.1)`. `load_numeric_npz(path)` supplies detached numeric dictionaries. Per-output statistics include shape/dtype, max/mean/p95 absolute differences, and relative differences `abs(actual-reference)/max(abs(reference),epsilon)`. Relative errors around zero can be large, so inspect them with absolute errors. No tolerance produces a quality PASS. Overall `COMPARED` means valid numeric tensors were compared, even if their values differ substantially; `INVALID_CAPTURE` means structural/numeric checks failed. CLI exit 0 means `COMPARED`, exit 2 means invalid capture. No hardware or quality acceptance is implied.

Decoded comparison requires manifest plus `metadata.original_transform` containing exactly integer fields `original_width`, `original_height`, `input_width`, `input_height`, `resized_width`, `resized_height`, `left`, `top`. If missing, decoded stage is explicitly `SKIPPED`. Invalid metadata/output is `INVALID_METADATA_OR_OUTPUT` while preserving valid raw numeric diagnostics. Split pose outputs are restored through the same `split_pose_v8` decoder. Diagnostic detection pairing is greedy same-class descending IoU above `min_match_iou`; this is not ground-truth matching. Reports include unmatched detections, box differences, scores, keypoint confidences, and XY error on jointly visible points at confidence >=.5. These thresholds define diagnostics only, not target acceptance.

Actual smoke evidence saved outside Git:

- `pose-split/capture-golden-smoke.json`: golden NPZ compared to itself, 4 output tensors exactly equal and 3 identical decoded detections. This checks file/decoder plumbing only.
- `pose-split/capture-simulation-comparison.json`: pre-existing vendor **simulation** outputs compared with their saved float references, 3/3 decoded persons, paired box IoUs .911/.872/.781. Largest all-anchor differences are 170.51 px for box channels, 206.02 px for keypoint XY, .1188 class score and .7634 keypoint confidence. Unselected anchors are included in these maxima; they cannot be replaced by favorable selected examples. This is a diagnostic comparison of simulation, not a hardware capture or a target-video quality result.

Every report states `hardware_execution=NOT_ESTABLISHED_BY_COMPARISON` and `target_quality=NOT_EVALUATED`. Actual Jupyter runtime captures and independently labeled video are still needed.

## Verified runtime manifest from existing real captures

`from ml.detection import prepare_verified_manifest` exposes:

```python
manifest = prepare_verified_manifest("helmet", artifacts_root="/workspace/artifacts")
pose_manifest = prepare_verified_manifest("pose-split")
```

This helper reads the existing `linq-rpc/{name}-001` completed capture, its response, `linq-rpc/{name}/staging-receipt.json`, the original detection manifest and `linq-sdk/{name}-compile/compile-report.json` plus local program. It performs no network call, changes no original/candidate manifest and creates no files. `capture_review.review_capture` checks NPZ/file/tensor hashes, finite numeric values and exact shape/dtype. Additional checks require completed service status 0 (integer, not bool), the same canonical request/response/journal UUID, local/compiled/staged/captured program SHA256 equality, staged byte count/name, source ONNX hash equality, exact compiler/capture/response ABI, matching source input ABI and valid source decoder outputs. Both existing real helmet and split-pose captures were decoded locally by this helper.

The returned new dictionary retains an allowlisted preprocessing/decoder contract and adds `linq.runtime_abi_verified=True`, local `program_path`, exact `program_name`, `program_sha256`, `inputs`, `outputs`, identity `input_map`/`output_map` and local `evidence_paths`. Public source URLs and arbitrary capture/account/broker metadata are omitted. The orchestrator injects RPC directories, timeout and runner factory. ABI verification is based on the recorded completed remote calls and consistent bytes; it is not independent hardware attestation or target-video quality acceptance, and does not establish continuous-video capacity.

### Actual source video recommendation (read-only review)

Use `Deep-Research/datasets/_WORK/MATERIALS/W2-10/4_tr6.mp4`, **0–8 seconds**, as a real industrial-camera replay candidate. It is Önal/Dandıl Mendeley `xjmtb22pff/1`, folder `4_safe_walkway`, author member UUID `730fbd88-bb7e-4444-a826-e5f2f461a2b4`. Local SHA256 was rechecked and matches saved metadata: `f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a`. Video is H.264 1920×1080, 522 frames, 25.05 FPS (501/20), duration 20.838323 s, native timebase 1/16032. ffprobe presentation timestamps at source frames 0/50/100/150/200 are 0/1.996008/3.992016/5.988024/7.984032 s respectively, matching OpenCV positions in this sample.

Five decoded frames show a foreground seated worker with visibly uncovered head, plus walking/standing people. This is a plausible bare-head replay input, not a labeled helmet-violation holdout: the folder describes walkway use, site helmet policy is unknown, some heads are small or turned away, and no fall was observed in the inspected window. Use this as real-footage plumbing and operator-evidence demonstration; manually annotate before reporting accuracy. `0_tr16.mp4` is a second real candidate (24.8 FPS, foreground walking person in first 0–4 s), but has different initial timestamp/framing. `W2-11/CORE_SAMPLE.mp4` is a close-up concrete-mixing action, unsuitable for whole-person/helmet demonstration.

Inspection artifacts are outside Git: `/workspace/artifacts/video-review/candidates.jpg`, `inspection.json`, `native-pts.json`. The research archive and source videos were not modified or committed. `reference.avi` is repeated bus imagery and must never be described as real industrial source footage.

## ML-quality sprint: Helmet E00 and object scoring

The quality sprint follows `/workspace/ML_24H_PLAYBOOK.md`. External event/API schemas remain unchanged. New owned tools are in `ml/quality/helmet/`:

- `metrics.evaluate_dataset(dataset, predictions, classes=('helmet','bare_head'), confidence=.25, match_iou=.5, ap_score_floor=.001, max_detections=300, allow_test=False)` computes object P/R/F1, AP50 and mean AP over IoU .50:.05:.95 with a 101-point recall grid. This is an explicitly versioned custom metric, not a claim of exact COCO equivalence.
- Dataset images require `image_id`, `group_id`, `split`, `annotations` (class_name/positive-area original xyxy box/optional ignore), explicit `class_coverage` and optional `ignore_regions`. Predictions must explicitly include every image, including empty lists. Missing inference is an error, not an observed empty frame.
- Only class-complete images contribute to primary precision/recall/AP. Partial-label images get known-positive recall separately; their unannotated objects are never assumed absent. Unknown-class images are excluded. Regular GT matches take precedence over ignore regions; unmatched predictions with >=.5 intersection-over-prediction-area in an applicable ignore region are excluded. A class with zero complete GT has AP null, not zero. Final test requires explicit `allow_test=True`; it has not been invoked.
- `curate` inventories all images/labels, exact byte/decoded-RGB hashes and connected pHash/dHash duplicate proxies, then deterministically freezes a bounded official-val selection before predictions. It preserves original supplied splits and quarantines orphan labels. Perceptual proxies do **not** establish camera/actor/source independence.
- `baseline` accepts validation only, verifies frozen image bytes, acquires the shared `fcntl` GPU lock, stores raw outputs once at score floor .001 and evaluates operating confidence .25. It never trains or uses LinQ and never evaluates a test split.

Existing Construction-PPE ZIP was extracted outside Git to `/workspace/datasets/quality/helmet-construction-v1`. SHA256 `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`. Inventory: 1,416 paired images, 1,268 exact/perceptual proxy components, 30 components crossing original splits, 10 orphan labels quarantined. Frozen first development selection used 32 official-val images, one per proxy group, excluding components touching official test. It is development data only: known same-rooftop actor photos evade tight perceptual grouping, and pretraining-source overlap is unresolved. Do not train/fine-tune on this source under the current sprint decision.

A blind single-agent GT review was saved before predictions, identifying 18 complete/9 partial/5 unknown images and merging nine known rooftop-actor photos. Defects include `image1392.jpg` no_helmet box on the neck, unlabeled visible heads/helmets in `image705.jpg`/`image656.jpg`/`image547.jpg`, and uncertain tiny/occluded heads. A second independent review is still required before treating reviewed metrics as settled. Fixed reviewed dataset digest: `5586d7ab62252dd53829d7571d41da0c705f93ddd2b4924803b8e7ca99162a6f`.

Actual E00 GPU native run is `/workspace/artifacts/quality/helmet/e00-v1/`: frozen-input.json, raw NPZs, predictions.json, metrics-reviewed.json, metrics-source-provisional.json, run.json. At confidence .25/IoU .5 on the 18 single-reviewed complete images: helmet GT20/TP16/FP3/FN4, P .8421/R .8000/F1 .8205/AP50 .8057/mAP50-95 .2710; bare_head GT3/TP1/FP4/FN2, P .2000/R .3333/F1 .2500/AP50 .3366/mAP50-95 .1683. Bare-head support is far too small for stable threshold selection. The all-32 source-label benchmark is separate and provisional because of known annotation defects. Neither report is an independent industrial-video accuracy result. Test inference, training and LinQ execution were not performed by E00.

Primary provenance checked during the sprint: [current baseline model card](https://huggingface.co/keremberke/yolov8n-hard-hat-detection/blob/main/README.md) names the paired dataset; [its dataset card](https://huggingface.co/datasets/keremberke/hard-hat-detection/blob/main/README.md) links Roboflow `hard-hats-fhbh5/2`, reports CC BY 4.0 and 640×640 stretch. Therefore that source is not an independent baseline test. [Construction-PPE official config](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/construction-ppe.yaml) confirms counts/class map and AGPL notice; independent upstream-photo rights remain unresolved. [SHEL5K primary page](https://data.mendeley.com/datasets/9rcv8mm682/1) identifies its SHD5000 parent and CC BY-NC 3.0, so SHD/SHEL cannot be treated as unrelated sources. [SFCHD author repository](https://github.com/lijfrank/SFCHD-SCALE) supplies chemical-plant images with blur_head labels but no explicit blanket dataset license in the inspected repository page. Existing seven SFCHD images are potential source-separated holdout material only after rights, mapping and source/camera grouping decisions; no model has been run on them in this sprint.

### E01 blind GT repair, no model change

Twenty additional official-val images were frozen **from source bare_head labels**, not predictions, with deterministic SHA ordering and unique duplicate-proxy groups excluding official-test-touching components. Original selection digest `e3c06798c54b0909e62015f90d7310a55157ac57fc8560e3d5eaf0066b1830eb`; 32 source head boxes existed, including narrow face/forehead bands, neck misplacements and ordinary hats. Full-resolution blind inspection confirmed these source semantics could not be used uncritically as full-head GT.

`ml.quality.helmet.repair.apply_reviews` applies explicit, versioned AI-agent patches while retaining `source_annotations`. Quality-v2 combines the same original32 plus the fixed new20 (52 images); corrected annotations cover the full observable anatomical head from scalp to chin, excluding long hair down the torso. Ordinary hats, cropped crowns and insufficiently visible background heads have tight localized unknown/ignore regions, not image-wide ignore masks. Source boxes and reasons remain in `/workspace/artifacts/quality/helmet/e01-gt-repairs.json`. There is no human-expert claim.

Four E01 originals (`image1151.jpg`, `image1341.jpg`, `image1183.jpg`, `image1190.jpg`) received ROOT's additional blind AI-agent review before new predictions. Its conservative feedback was incorporated: cropped upper-right head in image1341 is unknown; two foreground heads in image1183 are positive with tight background ignores; feather hat in image1190 is unknown while the visible bald head behind the left side is positive. Full-resolution review also corrected an initial contact-sheet misreading: white headwear in image656 is a backward baseball cap, not a safety helmet. It is unknown, not a new helmet GT.

Quality-v2 artifact `/workspace/artifacts/quality/helmet/development-quality-v2.json` currently has digest `e4a3dbd2c48732fc7b0eafa2438f17aa9dde74f1f70fabfcbd76ab70e1c340f1`, 52 frozen images, 44 class-complete images and 26 clear additional bare-head instances. This version awaits final ROOT review; no new predictions or E02 threshold selection were run against it by this agent. GT-only overlays are `e01-repaired-{1,2,3}.jpg` and `e01-root-four-1.jpg`. Baseline and candidate must be rescored on exactly this same corrected GT; changes from old E00 metrics caused by GT repair are **not model improvements**. Construction-PPE remains development-only, with no training/calibration and no independent-test claim.

### E01-v3 results and predeclared E02 decision

ROOT's blind AI-agent review of four old E00 originals agreed on two fully visible bare heads in image1203, one fully visible helmet in image767 and partial crowded coverage in image654. For image1290, ROOT judged the bare crown/face below the sign labelable, whereas the first conservative pass marked it unknown. This disagreement was explicitly adjudicated as a full visible-head positive `[334,421,444,550]` in quality-v3, preserving quality-v2 and the original source GT. This is AI-only review, not expert ground truth.

The same frozen52 images were inferred once using unchanged helmet-v1 at 640, host NMS .45 and raw confidence floor .001 under the granted `fcntl` GPU lock. GPU was released immediately after completion. Raw outputs and predictions are `/workspace/artifacts/quality/helmet/e01-v2/`; frozen input manifest records dataset, checkpoint and model-manifest hashes. V3 rescoring reused these exact same predictions on CPU; it did not rerun or change the model. Final reviewed GT artifact is `development-quality-v3.json`, digest `39e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a`.

At unchanged confidence .25 on class-complete regions/images of quality-v3: helmet GT25/TP19/FP11/FN6, precision .6333, recall .7600, F1 .6909, AP50 .6661, mAP50-95 .2473; bare_head GT32/TP23/FP7/FN9, precision .7667, recall .71875, F1 .7419, AP50 .8441, mAP50-95 .6318. Macro F1 is .7164. Different GT/support makes comparison with the original E00 numbers a data/protocol change, not an ML improvement.

Only two predeclared increased-confidence operating points were evaluated, both on CPU and on identical v3 GT/predictions/NMS:

| Confidence | Macro F1 | Helmet recall | Bare-head recall | Diagnostic no-recall-decrease guard |
|---|---:|---:|---:|---|
| .25 baseline | .7164 | .7600 | .71875 | reference |
| .40 | .6525 | .6000 | .53125 | fails both classes |
| .50 | .5227 | .4000 | .37500 | fails both classes |

The increased-confidence hypothesis is rejected; retain .25. This is one failed hypothesis family, not evidence that lowering thresholds is useful. AP remains unchanged because AP uses the same recorded score floor .001 rather than these operating-point cutoffs. Full reports and explicit guard definitions are in `e01-v3-rescore/e02-predeclared-comparison.json`. No sealed test, training, PTQ calibration or LinQ run occurred in these experiments.

### Confirmed development-source overlap

A bounded source-overlap audit downloaded **only** the baseline author's pinned `keremberke/hard-hat-detection` validation archive: revision `694c61350faf9a6622586d6cf50f45e1631862dc`, 224,860,587 bytes, SHA256 `3d39f51b1e9cd968b399d1506f014d551ff5cb572d27b076064bfb8458cb6833`, primary dataset card CC BY 4.0. All 3,962 images were compared by byte/decoded-RGB hash and tight pHash/dHash against all1,416 construction images. There were zero exact-byte/pixel matches but156 perceptual candidates involving26 construction images. This is expected when sources have been resized/reencoded.

Visual review confirmed the same photograph for development `image804.jpg` and a baseline-source validation member, plus shared actor/site scenes for `image674.jpg` and `image705.jpg`. Three further construction train images also visibly reuse baseline-source photographs. The fixed original32 selection intersects three perceptual/source-scene matches; the added20 had no match under this limited check. The source training archive is778,928,861 bytes and was not downloaded or examined; no-match is not proof of pretraining independence. Artifacts: `pretraining-overlap-audit.json`, `pretraining-source-valid-features.json`, `pretraining-overlap-contact.jpg`. All Construction-PPE remains development-only; no independent test or training/calibration use is authorized by this audit.

Dataset ownership was subsequently transferred to the separate Data Orchestrator. The Helmet agent stopped acquisition/search at that boundary. SH17's frozen selection and partial acquisition are handed off at `/workspace/artifacts/quality/helmet/sh17-test/DATA_HANDOFF.json`:13 exact-release images present, seven response-format failures, no model predictions, GT review or test evaluation. No continuation of SH17 data work is performed by this agent.

### Final Helmet hypothesis H-HELMET-02: fixed overlapping tiles, rejected

The second and final Helmet hypothesis tested an explicitly fixed, non-adaptive four-tile policy using unchanged helmet-v1 weights and640×640 neural input. For original width W and height H, tile size is `((3*W+2)//5, (3*H+2)//5)` and starts are x=`0,(2*W+2)//5`, y=`0,(2*H+2)//5`: nearest-integer60% dimensions with starts at40%. Tile order is row-major. Exactly four tile calls are made, with no full-frame call and no GT-conditioned ROI. Tile boxes are restored to original-image pixels before class-aware global NMS at IoU .45/max300. Raw confidence floor is .001; operating confidence stays .25. Tile-local suppression is disabled semantically using IoU1.0/anchor-count cap, leaving exactly one effective global NMS.

Implementation is `ml.quality.helmet.tiles`. CPU fixtures verify odd-dimension geometry/coverage, source-coordinate offsets, class-aware cross-tile deduplication, exactly four calls, preservation of local candidates until global NMS, and recall-guard rejection. GPU preflight found0% utilization/2MiB/no compute apps; the short job acquired the shared `fcntl` lock and released it immediately after52-image/208-call native inference. There was no data acquisition, training, threshold tuning or hardware call.

The candidate used exactly the same52 quality-v3 images/GT as the baseline (digest `39e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a`). Predeclared acceptance required increased macro F1 and no per-class recall decrease greater than .02.

| Metric | Full-frame baseline | Fixed four tiles |
|---|---:|---:|
| Macro F1 | .7164 | .6066 |
| Helmet TP/FP/FN | 19/11/6 | 18/30/7 |
| Helmet precision/recall/F1 | .6333/.7600/.6909 | .3750/.7200/.4932 |
| Bare-head TP/FP/FN | 23/7/9 | 27/16/5 |
| Bare-head precision/recall/F1 | .7667/.71875/.7419 | .6279/.84375/.7200 |

Both required conditions failed: macro F1 decreased and helmet recall fell .04. Additional bare-head recall did not compensate for the increased false positives. The policy is rejected. Candidate AP50 was helmet .4924/bare-head .7867; mean AP50-95 was .1602/.4999, also below baseline. These figures are development-image diagnostics with AI GT/source-overlap limitations, not independent industrial performance.

Native mean four-call time was36.39ms; full per-image tile processing averaged137.11ms, p95 196.54ms. Full timing includes preprocessing, tile decoding, global NMS and diagnostic raw-NPZ writes; it excludes image loading and model initialization. It is neither device-only latency nor LinQ performance. Artifacts are `/workspace/artifacts/quality/helmet/h02-tiles-v1/`: frozen-input.json,208 raw NPZ captures, predictions.json, tile-metadata.json, comparison.json and run.json. Source/candidate artifacts and the baseline were preserved.

The failed-hypothesis budget is exhausted: increased confidence was family1, fixed tiling family2. Freeze the existing full-frame helmet-v1 at confidence .25/NMS .45. No further Helmet parameter search is performed. Because this candidate failed native validation, its potential LinQ tile gate and independent final test were not run; no production manifest or external interface was changed.

### Night E001: frozen Helmet quantized-reference evaluation

`ml.quality.helmet.quantized` consumes the exact consumer READY snapshot twice,
requiring `helmet-quality-v3-52/detection_quality` and
`mendeley8-calibration-v1/calibration` before a forward. The GT JSON byte SHA and
its semantic dataset digest are separate identities. All52 validation images
must be pinned by READY; Construction remains development-only with confirmed
source-photo overlap, AI-only annotation review and unresolved upstream photo
rights. No sealed test or training data is implied by these results.

The runner uses the existing SDK CPU hardware-aware graph and recorded input /
output scales, two CPU threads, RGB640 preprocessing, raw confidence floor.001,
class-aware NMS.45 and primary confidence.25. It preserves named numeric output
NPZs, transforms, complete prediction maps, metrics and input/artifact hashes in
fresh output directories. This is **SIMULATED**, never actual LinQ execution.
`--float-onnx` provides a fixed-source ORT CPU control without a new hypothesis.

The single diverse-calibration candidate uses the unchanged reviewed Helmet
ONNX and the existing8-tensor Mendeley corpus; no threshold, tiling or network
weight variants. Acceptance is predeclared against the CURRENT quantized
baseline: macro F1 gain>=.01, no class recall decrease>.02, and bare-head FP
nonincrease. Even a passing simulated comparison requires actual LinQ parity and
independent quality gates before release. Existing native predictions are reused;
no new native forward or training is authorized by this runner.

E001 completed on the same fixed52 quality-v3 images. Frozen existing native and
original Float ONNX control have identical class counts and AP/F1 (macro F1
.716422287; bare-head recall.71875). The current PTQ simulator has macro F1
.741682360 but bare-head recall.59375: the .125 recall loss is downstream of
original float export. Conditioning, PTQ and the simulator codec were not
individually isolated; no actual hardware-quality conclusion follows.

The single Mendeley8 candidate compiled O1/H1M in61.81s, then scored macro F1
.735185185 (delta-.006497175 versus current PTQ), with unchanged per-class recalls
and one extra helmet FP. It is REJECTED; baseline remains preserved. Raw output,
prediction, hash and timing evidence is under
`/workspace/artifacts/night-20261024/E001/`; `summary.json` records all paired
metrics. CPU reference runs took112.63s baseline,110.79s candidate and4.68s float
control. No native rerun, GPU, training, new data, remote staging or actual LinQ
execution occurred. Night Helmet hypothesis1 failed; a separate training
hypothesis remains blocked without producer-approved READY training data.

### Night E005: final Helmet output-boundary hypothesis

`ml.detection.split_detect.export_split_detect` verifies the parent export hash
and extracts the two existing tensors before the final channel Concat:
`/model.22/Mul_2_output_0` boxes[1,4,8400] and
`/model.22/Sigmoid_output_0` class probabilities[1,2,8400]. The
`split_detect_v8` host decoder concatenates them and calls the original decoder,
with no sigmoid or neural decode on CPU and one unchanged class-aware NMS.
The native adapter can expose the same logical ABI by slicing existing output;
no new native inference was performed for this experiment.

This is a hypothesis about compiler/output-boundary quantization sensitivity,
not an established cause. The original Helmet output already has per-channel
scales separating coordinate and class channels; it does NOT share one global
coordinate/confidence scale. E005 changes output ABI only versus E001 Mendeley8:
same trained weights, parent ONNX, input codec, calibration corpus, O1/H1M and
operating thresholds. Acceptance remains against the best current PTQ baseline,
not merely versus the previously rejected data8 candidate.

Before compilation, `ml.quality.helmet.split_control.verify` compared all52
split float outputs restored by host concatenation to the preserved original
Float ONNX raw tensors: ALL were bitwise identical; the full decoded metrics
were identical. Split graph SHA is
`e802cef32d4fc3398128b770ddc29d0ded6888a2e6a58a921e20202d306ee33a`;
parent SHA remains `b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47`.
Evidence lives under `/workspace/artifacts/night-20261024/E005/`.

E005 result: REJECTED. The one split candidate compiled in59.62s; the52-image
CPU simulation completed in114.26s. Macro F1 was.327777778, versus best current
PTQ.741682360 (delta-.413904583) and same-data8 E001.735185185
(delta-.407407407). Helmet counts were12TP/3FP/13FN (recall.48); bare-head counts
were1TP/3FP/31FN (recall.03125). No thresholds or scaling were adjusted to recover
the result. Both new night Helmet hypotheses failed; preserve and freeze the
existing baseline and all failed candidate artifacts. No further Helmet
hypothesis or actual LinQ submission was performed.

CPU graph audit confirms the only removed node is `/model.22/Concat_3`; there are
no added nodes, retained nodes and ALL initializers are byte-identical. Emitted
scale metadata changed: E001 data8 combined output uses shape[1,6,1], whereas
split class output uses shape[1,1,8400] (anchor-dependent) and split boxes scale1.
This is OBSERVED metadata, not proof of a causal mechanism or authority to alter
the runtime codec. The original input scale remains127. Evidence:
`E005/summary.json`, `graph-scale-audit.json`, `anchor-audit.json`, float-parity raw
outputs and complete split simulation outputs. Hardware quality remains UNKNOWN.
