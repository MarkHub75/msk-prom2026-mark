# Resume MOSPROM ML/CV — saved checkpoint

## CURRENT STATE — supersedes earlier checkpoints

Stock automatic Vast->LinQ ResNet50 has actually completed and passed capture integrity/class checks. Results are /workspace/artifacts/linq-rpc/resnet50-001/; do NOT repeat this job. Official pure-Python format source is /workspace/linq-client/tpu_pycloud_format, user-confirmed version0.0.1 with reviewed hashes at /workspace/artifacts/linq-rpc/format-source.json. Use /workspace/.venvs/linq-client/bin/python with PYTHONPATH=/workspace/linq-client:/workspace/project. Runtime config is /workspace/linq-client/connection.env; never print/commit its values.

OWN MODELS SUCCEEDED ON LINQ. User started the bounded Jupyter helper. Both uploads completed with matching remote SHA256: Helmet 2,751,596 bytes / request adcc0b06-5767-45c6-851a-9bd6b5b7e593; Split-Pose 2,929,222 bytes / request ee97f734-5132-4278-a5ce-ee35ef077251. Receipts are /workspace/artifacts/linq-rpc/{helmet,pose-split}/staging-receipt.json. Do not upload again.

Exactly one real inference per own model completed:

- Helmet request 262bdaa1-c24b-48ac-b073-6b28fd014248: status 0, matching response ID, float32 [1,6,8400], full call 10234.49 ms. /workspace/artifacts/linq-rpc/helmet-001/ contains capture/inputs/outputs/response/integrity/comparison/detections/model-check. Smoke PASS: 2 bare_head detections at 0.352586 / 0.259503. The float reference has 1 detection, matched at IoU 0.925226; 1 extra actual detection. Coordinate/class/confidence checks PASS. This is not target-video quality validation.
- Preferred Split-Pose request 1f986b07-896d-48b9-8b4f-6ce2d0f8dc16: status 0, matching response ID, four expected float32 tensors, full call 11152.85 ms. Same artifact set under /workspace/artifacts/linq-rpc/pose-split-001/. Smoke PASS: 3 persons, matched IoU 0.7812..0.9108; visible keypoints 16/17/9, confidence preserved. Original mixed pose still excluded.

scripts/linq_models_auto.sh all is resumable: completed captures are locally reviewed/reused, not resubmitted. Pending UUIDs reconcile receive-only. Do not rerun a completed TPU job. Next project stage is wiring this verified remote transport into the existing video-worker/backend integration; these single-image probes do not claim end-to-end video quality/performance. Historical packaged manifests remain unverified templates and are not automatically promoted to production bindings.

Network steering: user is moving Arch SSH bridge to autossh/systemd because VPN can drop. Do not change SSH/VPN/NetworkManager from Vast. Durable RPC core 7f705a32, CLI/capture followup 474afee8 and durability fix 97a7a5d2 are merged: fsynced intent/context BEFORE network, UNKNOWN after possible submission, retained reply queue and receive-only reconciliation; terminal tensors saved BEFORE ACK. Both real uploads and inferences used this core; the last fix additionally retains replies if final fsync is uncertain. Root added cached/pending capture resume and concurrency/request locking. Own-session heartbeat 5 s bounds failure detection; Pika blocking RPC/close may overrun the polling deadline, so 60 s is not hard wall-clock cancellation. Missing response never licenses a blind repeat. Previous full suite (160 PASS) was not repeated. No additional network probes or ResNet calls.

## Final checkpoint — iteration closed at the user's request

STOP after the final report. Wait for a new user instruction; do not automatically start any following task, research, experiment or agent. LinQ agent completed its work and review; Detection/Behavior agents have no active tasks. No server was stopped and no artifacts were deleted.

Implemented: pinned automatic Jupyter file staging through a distinct explicit consumer; existing official AMQP client with unique UUIDs, bounded waits, durable intent and selected numeric response; receive-only/offline recovery; duplicate suppression and deployment locking; numeric capture, integrity review, ABI checks and model decoding/comparison. The real service returned successful correlated responses for both models. Full-call latency is separate from recovery/cache time.

Final checks: 20 affected AMQP + 17 recovery tests passed in the isolated LinQ worktree; 13 deployment/recovery tests passed in the integration worktree after merge. Total: 50 affected checks PASS, not a rerun of the full project suite. git diff --check is clean. Runtime artifacts and private configuration remain outside Git; the final integration commit contains code/tests/docs only. Use git log -1 on matvey_cv for that checkpoint's exact hash.

Known limits: Helmet produced one extra detection relative to the float smoke reference. These single-image tests do not establish target-video accuracy or throughput. Actual VPN-loss recovery was not exercised on the live service; fault/crash recovery was checked with targeted tests. Blocking Pika operations can exceed the polling deadline while heartbeat detects loss. Historical packaged manifests remain templates rather than automatically approved video-worker bindings. Backend/frontend end-to-end integration is still pending.

Next three priorities, ONLY after the user explicitly resumes:

1. Bind the verified Helmet/Split-Pose remote transport to the existing video worker with per-model ABI/identity and durable request context; preserve UNKNOWN semantics, with no automatic GPU fallback.
2. Connect real backend event delivery, evidence, notifications and journal; verify persisted ACK and idempotent event revisions across the full MVP.
3. Evaluate target-video detection/behavior quality, latency/throughput and controlled reconnect recovery; keep the extra Helmet detection and quantization differences visible in acceptance reports.

The sections below are historical snapshots. Their old pending statuses and instructions are superseded by CURRENT STATE and this final checkpoint.

## Earlier start instructions (historical)

Continue the approved implementation; do not restart research or model selection. User requested this checkpoint because remaining usage is low. Resume only when the user returns. Do not spawn new work merely from reading this file.

Repository /workspace/project; integration branch matvey_cv. Read AGENTS.md, docs/TASKS.md, docs/ARCHITECTURE.md and this file. Check git status first. Never modify main, commit source videos/secrets/research archive, or share credentials between agents.

## Implemented and verified

- Previous baseline 118e068b: video ML-worker, shared contracts, helmet + split-pose, behavior rules, snapshots, durable SQLite outbox/checkpoint, HTTP committed ACK, actual compiler programs, SDK simulation, 61 tests.
- Current continuation adds AGENTS.md, architecture/task register, stricter consistent wire validators/schemas, ready-evidence delivery fixes, captured-output comparator, deterministic behavior acceptance fixtures, safe Jupyter call capture, and independent capture-integrity review.
- Last full test: `python -m unittest discover -s tests -q` — **96 tests PASS**. Includes mock call capture -> integrity review -> numeric comparator; tampered artifact, invalid tensor manifest, failed call and wrong program hash rejection.
- CLI replay of 8 synthetic acceptance scenarios: 101 observations, 7 incidents, 12 revisions; backend label synthetic-test, pending outbox12, no actual backend deliveries. Artifacts /workspace/artifacts/behavior/orchestrator-acceptance and orchestrator-events.jsonl/orchestrator-summary.json.
- No real TPU capture has been obtained by the orchestrator. No target-video accuracy or real backend/frontend integration claim.

## Actual agent stages

All three native agents were really resumed in separate Git worktrees and completed their coding tasks. They are not currently background workers. Root reviewed/merged their branches into matvey_cv. If a fresh session has no agent objects, spawn replacements with the same isolated ownership only after user resumes.

| Agent | Worktree / branch | Completed stage | Last relevant agent commit |
|---|---|---|---|
| CV Detection | /workspace/agents/detection / agent/detection | CV-02 named NPZ comparison, explicit runtime-to-reference mapping, decoded pose diagnostics; 14 owned tests | 133ea22e |
| Behavior Analysis | /workspace/agents/fall / agent/fall | BH-02 8 synthetic scenarios, restart/replay/ACK-loss acceptance; fixed duplicate equal-gap tracking-generation reset; 30 owned tests | 50dd2f65 |
| LinQ Integration | /workspace/agents/linq / agent/linq | LQ-01 one-call safe notebook capture + manual Jupyter runbook; 31 owned tests | fd5adcbf |
| Root | /workspace/project / matvey_cv | Shared validation, review/merge, capture integrity/comparison integration; 96 combined tests | See git log |

/workspace/agents/speed / agent/speed remains reserved and inactive. No same-worktree concurrent editing.

## Most recent new interfaces

- `ml.linq.notebook.capture_call(run, *, inputs, output_names, program_path, output_dir, model_id, input_specs=None, output_specs=None, runtime_to_reference=None, original_transform=None, expected_class=None, placement_attested=False, max_bytes=...)`.
- Invokes explicitly supplied callable once. New directory contains capture.json, inputs.npz, outputs.npz. No notebook/session/environment/auth dumps. Error messages are reduced to phase/type. Hardware independently_verified always false.
- `ml.pipeline.capture_review.review_capture(directory, expected_program_sha256=None)` verifies completed status, program identity if specified, file hashes, numeric arrays, per-tensor hashes/shape/dtype/nbytes. Hash consistency is not independent hardware proof.
- `ml.detection.compare_capture.compare_captures(reference, actual, runtime_to_reference=None, manifest=None, metadata=None, ...)` returns COMPARED/INVALID_CAPTURE, never hardware/target-quality PASS. CLI `python -m ml.detection.compare_capture --help`.
- `python -m ml.behavior.scenarios --output-dir PATH` writes observations.jsonl + expected.json. Synthetic only.

## LinQ access truth and next priority

The USER CONFIRMS authenticated LinQ Jupyter access and stock example.ipynb with a ready ResNet50 TPU program. This session is not exposed through tools to the orchestrator. Vast still fails DNS for hackathon.lin-q.ru and has no /dev/net/tun/OpenVPN; that does NOT negate user access.

The earlier async question was answered when the user resumed: stock example succeeded with status_code0, class257 and response0.39s. This result is user-reported; numeric tensors and the actual call source are not yet captured locally. Do not ask for passwords/tokens.

Priority1 on resume:
1. Read docs/JUPYTER_RUNBOOK.md. User runs the inspected supplied example in their existing Jupyter session.
2. Bind capture_call to the ACTUAL existing notebook inference expression; the runbook intentionally has guarded placeholders instead of inventing remote API/variable names. If adaptation is needed, request only manually cleaned preprocessing/call code, no auth/source secrets or notebook outputs.
3. Export only capture.json, inputs.npz, outputs.npz. Transfer into a user-chosen directory outside Git, e.g. /workspace/case/linq-capture/.
4. Verify via `python -m ml.pipeline.capture_review --capture PATH [--expected-program-sha256 SHA]`, inspect actual supplied API, then compare numeric outputs against the matching reference. User attestation/correlated completion and integrity checks must not be described as independently verified chip placement.
5. Then test own helmet and preferred split-pose programs on real TPU, verify runtime ABI/codec/name mapping. Do not flip runtime_abi_verified without this.
6. Connect actual team backend/evidence hosting, then measure full-chain latency and independent target-video precision/recall.

## Earlier checkpoint packaging task — now completed

At the earlier checkpoint the small kit had not been built. This task has now been completed; see the latest resumed-work section below and docs/validation/jupyter-kit.json. Do not rebuild models or repeat prior research.

Existing `/workspace/artifacts/linq-handoff.zip` (~65MB) is the earlier model/compiler handoff from previous baseline. It contains helmet + split-pose TPU programs, golden references, vendor ResNet50 assets and earlier source. It does NOT contain latest capture/review/comparison helpers. Its prior SHA256 is in docs/validation/2026-10-23.json.

## Existing model/artifact evidence

- /workspace/artifacts/detection/{helmet,pose,pose-split}/: weights, ONNX, manifests, golden/parity and comparison reports.
- /workspace/artifacts/linq-sdk/{helmet,pose,pose-split}-compile/: actual TPU programs, compile reports, quantized models/scales and SDK simulation.
- Original mixed pose is REJECTED: PTQ zeroed all keypoint confidences.
- Corrective split-pose extracts boxes, class scores, keypoint XY and confidences BEFORE mixed Concats; float output bit-identical on smoke image. SDK simulation preserves confidences; 3/3 decoded people. One-image calibration only, not quality validation.
- Preferred split program SHA256 c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b.
- Helmet program SHA256 408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa.
- Compiler env /workspace/.venvs/linq-sdk; preparation env /workspace/.venv-cv-prepare; existing main PyTorch env unchanged.

## Persistence and limits

/workspace is NOT volume-backed. Local commits and artifacts survive stop/start but not recycle/destroy. No remote push or external backup has been performed in this continuation. Preserve repository/artifacts outside the instance before recycle/destroy. No raw video, credentials, model binary or research archive has been newly committed.

## Latest resumed work — portable kit

User reports successful stock example.ipynb: status_code0, class257, response0.39s. Recorded as user-reported service execution; selected numeric capture still pending. Built /workspace/artifacts/linq-jupyter-kit.zip (~9.5MB), including current code, instructions, runtime-only dependencies and existing Helmet/Split-Pose programs plus golden arrays. See docs/JUPYTER_KIT.md and docs/validation/jupyter-kit.json. LQ-02 helper from56a3d13f merged.113 tests passed; extracted kit imported in isolated Python and both prepare_case calls passed.

The actual remote notebook import/call/result extraction has NOT been provided. An async request for cleaned code was issued, without credentials, but no snippet arrived before packaging. The archive explicitly marks NOT_PROVIDED_YET; bindings.py refuses requests until filled. Do not call the public LOCAL pytpu reference the organizer remote API. No own-model hardware execution has occurred. Next: receive that cleaned fragment, bind the actual successful service API, update the kit, capture stock + Helmet, inspect integrity/ABI/decoded results, then Split-Pose. No training or model regeneration is needed.
