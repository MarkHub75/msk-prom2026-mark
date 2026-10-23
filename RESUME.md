# Resume MOSPROM ML/CV — saved checkpoint

## Start here

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

An async question was issued: whether the stock example has been run successfully, not yet run, or errored. No answer was received before checkpoint. Do not ask for passwords/tokens. Actual stock-call completion is UNKNOWN/NOT_CAPTURED, not disproved by local preflight.

Priority1 on resume:
1. Read docs/JUPYTER_RUNBOOK.md. User runs the inspected supplied example in their existing Jupyter session.
2. Bind capture_call to the ACTUAL existing notebook inference expression; the runbook intentionally has guarded placeholders instead of inventing remote API/variable names. If adaptation is needed, request only manually cleaned preprocessing/call code, no auth/source secrets or notebook outputs.
3. Export only capture.json, inputs.npz, outputs.npz. Transfer into a user-chosen directory outside Git, e.g. /workspace/case/linq-capture/.
4. Verify via `python -m ml.pipeline.capture_review --capture PATH [--expected-program-sha256 SHA]`, inspect actual supplied API, then compare numeric outputs against the matching reference. User attestation/correlated completion and integrity checks must not be described as independently verified chip placement.
5. Then test own helmet and preferred split-pose programs on real TPU, verify runtime ABI/codec/name mapping. Do not flip runtime_abi_verified without this.
6. Connect actual team backend/evidence hosting, then measure full-chain latency and independent target-video precision/recall.

## Pending packaging task — NOT DONE

Root was about to create a small `linq-jupyter-kit.zip` with current helper/source/runbook, without weights/profiles/secrets. **This small kit has NOT been built.** Build it on resume if needed. Do not call the existing archive current for these new helpers.

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
