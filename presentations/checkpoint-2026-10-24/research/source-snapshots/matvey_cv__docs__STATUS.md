# Implementation status — 2026-10-23 UTC

Implemented in matvey_cv: shared contracts and JSON schemas, two-model detection/pose decoding, temporal helmet/fall/lying/visible-immobility rules, conservative tracking, source gaps, latest-frame live ingress, exact-frame snapshots, atomic SQLite outbox + behavior checkpoint, HTTP idempotent delivery, explicit native/LinQ execution modes, official local TPU runner, compiler CLI, preflight, finite-corpus evaluator and team handoff docs.

## Verified

- 61 unittest cases passed, including synthetic raw tensor -> decoder -> behavior -> snapshot -> persistent event -> HTTP committed ACK; repeated observations produce one opening notification.
- Real helmet and pose weights exported to static ONNX opset13; CPU and explicit CUDA FP32 outputs agree with ONNX at atol=rtol=1e-3 on the same image. Initial CUDA TF32 differences were retained, not hidden.
- Both complete graphs compiled using actual issued SDK2026.9.45 for TPU_H1M O1, yielding hashed model.tpu files. The compiler conditioned ONNX to opset17. A corrective split-pose graph was also compiled: boxes, scores, XY and keypoint confidences are separate outputs before mixed concatenation.
- Native worker processed 40 frames of a repeated bus image with both real models: p95 cycle about42ms in this smoke run, no stale/failed observations. This is not a live-camera capacity benchmark, source-to-alert latency, or behavior accuracy test.

- Original mixed pose FAILED the SDK quantized-reference smoke: keypoint confidences all became zero. The candidate is rejected for behavior deployment.
- Corrective split-pose float output is bit-identical to the original graph on the smoke image. Its SDK simulation preserves confidences (max0.999023 vs reference0.998908), decodes3/3 people and preserves visible keypoint counts16/17/9. Mean visible XY differences are4.12/4.31/2.78 pixels on this image. This diagnoses the observed scale problem; it is not independent validation or real TPU parity.

## Not yet verified

Actual TPU execution (including vendor ResNet50), TPU numerical/decoded parity, target CCTV precision/recall, representative INT8 calibration, backend/frontend team's real endpoint and artifact hosting, delivered-alert latency and multi-camera capacity.

Continuation: the user confirms authenticated LinQ Jupyter access and a supplied example.ipynb using a ready ResNet50 program. This is user-reported access confirmation; actual TPU completion still requires a captured call. Vast has no /dev/net/tun or OpenVPN; LinQ Jupyter DNS is unavailable from this host. The compiler now exists in a separate environment, while pytpu/native runtime and device remain unavailable here. No passwords or VPN profiles were opened or saved. The next hardware step is execution of the provided stock notebook inside the already authenticated Jupyter session, safe capture of the actual call, then our programs through that supplied API. No authenticated Jupyter tool/session is connected to this orchestrator.

## Artifacts outside Git

- /workspace/artifacts/detection/{helmet,pose,pose-split}/: weights.pt, weights.onnx, manifest.json, parity reports, linq-candidate.json.
- /workspace/artifacts/linq-sdk/{helmet,pose,pose-split}-compile/: model.tpu, conditioned ONNX, quantized model, thresholds, compile report.
- /workspace/artifacts/linq-api/: provided ResNet50 example/program/image and hashed inventory.
- /workspace/artifacts/integration/: safe preflight, repeated-image video and native run summaries.

Candidate manifests intentionally have runtime_abi_verified=false. Do not flip this flag without checking the actual execution host. Compiler smoke used one real image and is not a validated INT8 deployment calibration. All artifacts are on non-volume storage; preserve them outside this instance before recycle/destroy.

Machine-readable evidence: [validation/2026-10-23.json](validation/2026-10-23.json). Operational instructions: [INTEGRATION.md](INTEGRATION.md), [LINQ.md](LINQ.md).

Portable transfer package: `/workspace/artifacts/linq-handoff.zip`, including helmet and preferred pose-split programs, manifests with runtime_abi_verified=false, float golden tensors, source and official ResNet50 smoke assets. It contains no VPN profiles or credential material. SHA256 and size are in the validation report.

## Continuation checkpoint

See [../RESUME.md](../RESUME.md) for exact state and restart steps. All three native agents completed their current isolated coding stages, changes merged into matvey_cv. Combined tests:96 PASS. Capture/comparison/integrity tooling is implemented; actual stock Jupyter call remains not captured by the orchestrator. The small current-source Jupyter kit has not yet been packaged. No new tasks should run until the user resumes.

## Current portable kit

The user reports stock LinQ example success (status_code0,class257,response0.39s). Current /workspace/artifacts/linq-jupyter-kit.zip includes the new helpers and both reviewed precompiled programs. It is distinct from the earlier65MB handoff.113 tests passed. Both model packages passed inventory verification and isolated import/preparation. Actual remote API binding remains explicitly unconfigured because the actual notebook call source has not been provided. See docs/JUPYTER_KIT.md and docs/validation/jupyter-kit.json.
