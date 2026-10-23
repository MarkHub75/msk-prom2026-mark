# Implementation status — 2026-10-23 UTC

Implemented in matvey_cv: shared contracts and JSON schemas, two-model detection/pose decoding, temporal helmet/fall/lying/visible-immobility rules, conservative tracking, source gaps, latest-frame live ingress, exact-frame snapshots, atomic SQLite outbox + behavior checkpoint, HTTP idempotent delivery, explicit native/LinQ execution modes, official local TPU runner, compiler CLI, preflight, finite-corpus evaluator and team handoff docs.

## Verified

- 57 unittest cases passed, including synthetic raw tensor -> decoder -> behavior -> snapshot -> persistent event -> HTTP committed ACK; repeated observations produce one opening notification.
- Real helmet and pose weights exported to static ONNX opset13; CPU and explicit CUDA FP32 outputs agree with ONNX at atol=rtol=1e-3 on the same image. Initial CUDA TF32 differences were retained, not hidden.
- Both complete graphs compiled using actual issued SDK2026.9.45 for TPU_H1M O1, yielding hashed model.tpu files. The compiler conditioned ONNX to opset17.
- Native worker processed 40 frames of a repeated bus image with both real models: p95 cycle about50ms in this smoke run, no stale/failed observations. This is not a live-camera capacity benchmark, source-to-alert latency, or behavior accuracy test.

## Not yet verified

VPN/Jupyter authentication, actual TPU execution (including vendor ResNet50), TPU numerical/decoded parity, target CCTV precision/recall, representative INT8 calibration, backend/frontend team's real endpoint and artifact hosting, delivered-alert latency and multi-camera capacity.

Vast has no /dev/net/tun or OpenVPN; LinQ Jupyter DNS is unavailable outside VPN. The compiler now exists in a separate environment, while pytpu/native runtime and device remain unavailable here. No passwords or VPN profiles were opened or saved. The next hardware step is VPN/Jupyter validation on the Arch laptop, followed by the provided vendor program and our programs using the actual supplied remote example.

## Artifacts outside Git

- /workspace/artifacts/detection/{helmet,pose}/: weights.pt, weights.onnx, manifest.json, parity reports, linq-candidate.json.
- /workspace/artifacts/linq-sdk/{helmet,pose}-compile/: model.tpu, conditioned ONNX, quantized model, thresholds, compile report.
- /workspace/artifacts/linq-api/: provided ResNet50 example/program/image and hashed inventory.
- /workspace/artifacts/integration/: safe preflight, repeated-image video and native run summaries.

Candidate manifests intentionally have runtime_abi_verified=false. Do not flip this flag without checking the actual execution host. Compiler smoke used one real image and is not a validated INT8 deployment calibration. All artifacts are on non-volume storage; preserve them outside this instance before recycle/destroy.

Machine-readable evidence: [validation/2026-10-23.json](validation/2026-10-23.json). Operational instructions: [INTEGRATION.md](INTEGRATION.md), [LINQ.md](LINQ.md).
