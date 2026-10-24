# MOSPROM ML/CV implementation guide

Diagnostic follow-up after f99edc8d is CLOSED (E006/E007/E008); read the top of NIGHT_REPORT.md and RESUME.md. User's repeated night-mode directive did not reset candidate budgets E001–E005. Do not repeat saved-output audits or start another training/inference/compile/task cycle automatically. Wait for a new user task after the report; new model hypotheses require eligible immutable data and explicit bounded scope. Shared infrastructure restrictions below remain active.

## Current directive: ML quality sprint

Night cycle 2026-10-24 is explicitly authorized after the previous checkpoint. Do not repeat the previous confidence/tiling, upright-history or Pose industrial-PTQ hypotheses without new data. At most two NEW justified candidates per direction; evidence labels OBSERVED/MEASURED/SIMULATED/INFERRED/UNKNOWN, readiness flags may coexist. Root owns MODEL_INVENTORY.md, SCENARIO_COVERAGE.md, NIGHT_REPORT.md and the consumer handoff contract. Use immutable READY snapshots with verified bytes/hashes, split/groups, rights scope and task capabilities; READY for annotation is not event GT. No source discovery duplicated from Data Orchestrator and no automatic merge of its branch.

CRITICAL SHARED INFRASTRUCTURE: no network/routes/OpenVPN/SSH/firewall/service changes. Never modify, overwrite or remove /auto/cache/<login>/baseline or mosprom_*_cut_ap9999*.tpu; never consume/redeclare/delete foreign queues. All NEW own remote files must live under matvey/, all new program/queue/artifact names start matvey_. One own active TPU request maximum. No new remote submission through legacy unisolated bindings. Keep all credentials runtime-only; Jupyter OMP/OpenCV/ORT1–2threads. If own isolated staging or network is unavailable, record the blocker and work locally. No intermediate user questions during the autonomous night. Confirm actual branch before edits; no main/captain branch modifications/push/merge or moving uncommitted work across branches. Do not touch another worktree. Stop after the night report and commits; no automatic next cycle.

The user's latest directive and /workspace/ML_24H_PLAYBOOK.md supersede earlier integration priorities. Work only on ML/CV data, annotation, baseline/candidate experiments, independent evaluation and LinQ release gates. Do not edit backend/frontend/API or external event schemas. Keep the existing video pipeline unless a measured defect requires a minimal fix. Read official case pages4/5/7/8/13/15/18 for quality, latency and deadlines; Helmet is additional to the page4 behavioral examples.

Latest steering: a separate Data Orchestrator owns new source discovery, acquisition and data curation. ML agents stop new dataset searches and hand off existing intake records; do not edit /workspace/agents/data-audit or its branch. ML owns models, offline scoring, existing pipeline and LinQ qualification. Maintain BASELINE -> EVALUATED -> IMPROVED -> FROZEN stages, never mark IMPROVED without a paired gain. At most two failed justified hypotheses per scenario before freezing the best verified checkpoint and moving to the next scenario. A parameter sweep of two confidence values is one hypothesis, with both operating points recorded. A freeze may retain an unimproved baseline; it must explicitly record skipped improvement and outstanding quality gates.

Root alone owns ml/PROGRESS.md, DATASET_CARD.md, DATASET_MANIFEST.csv, EXPERIMENTS.csv, EVAL_PROTOCOL.md, ERROR_ANALYSIS.md, EVAL_REPORT.md and RELEASE_MANIFEST.json. Additional exclusive ownership: Detection agent owns ml/quality/helmet/ and tests/test_helmet_quality*.py; Behavior agent owns ml/quality/temporal/ and tests/test_temporal_quality*.py. Root owns other ml/quality helpers/integration tests. Existing ownership below remains in force elsewhere. All coding occurs in the corresponding isolated worktree.

At most one heavy GPU job, explicitly allocated by root and protected by /workspace/artifacts/quality/gpu.lock. Root controls actual LinQ requests and runtime credentials. Calibration uses training/calibration groups only; model/threshold/ROI selection uses validation only; final test is sealed until one final baseline/candidate comparison. Record source/lineage/rights, exact and near duplicates and uncertain class coverage. No missing annotation is a negative. Unit tests do not establish accuracy. Partial-label/source-label metrics must be separated from reviewed exhaustive metrics and event-level quality.

Historical research/media are read-only. New raw/processed data and full GT/predictions/checkpoints remain outside Git; only small provenance manifests, code and metric summaries are committed. User authorized a final non-force push of matvey_cv through the playbook and an off-Vast binary backup; never push main or upload private media. A backup is not verified until an authorized external destination and matching digest exist.

Continue the approved MVP: missing helmet and suspected fall/prolonged lying with visible-keypoint immobility. Official case in /workspace/case is the requirements authority. Research is reference material, never evidence of executed hardware or model quality.

## Ownership and Git

Integration branch matvey_cv lives at /workspace/project. Never modify main. Root orchestrator owns this worktree; delegated agents must not edit it. Each coding agent exclusively owns its own worktree:

| Agent | Worktree | Branch | Allowed source paths |
|---|---|---|---|
| CV Detection | /workspace/agents/detection | agent/detection | ml/detection/, tests/test_detection*.py, docs/DETECTION.md |
| Behavior Analysis | /workspace/agents/fall | agent/fall | ml/behavior/, tests/test_behavior*.py, docs/BEHAVIOR.md |
| LinQ Integration | /workspace/agents/linq | agent/linq | ml/linq/, tests/test_linq*.py, docs/LINQ.md, docs/JUPYTER_RUNBOOK.md |
| Orchestrator | /workspace/project | matvey_cv | Shared contracts, pipeline, configuration, architecture, task register and integration tests |

/workspace/agents/speed is reserved and inactive. No simultaneous writers in a worktree. Merge the assigned integration baseline before working; commit only owned paths. Shared interfaces/dependencies require the orchestrator's integration. Do not merge another agent's worktree or use destructive Git operations. Orchestrator reviews diffs and tests, then merges finished branch commits into matvey_cv.

## Contracts and execution evidence

Read docs/CONTRACTS.md and docs/INTEGRATION.md. JSON schemas live in ml/contracts/schemas. Use original-frame xyxy pixels, COCO-17 points, explicit media time, source epoch and request/model identity. Gaps are missing observations, not safe frames. Preserve event UUID/revision on retries. Backend must persist before ACK and suppress repeated incident notifications.

Use split_pose_v8 for candidate LinQ pose. Original mixed-output pose loses keypoint confidence in quantized-reference simulation and is rejected. Separate model preparation, compilation, SDK simulation, runtime ABI verification, actual TPU completion and target-video quality. Never automatically fall back from LinQ to GPU. Compiler PASS or mocked runner success is not TPU execution.

## Security and assets

Never request, print, share between agents or commit passwords/tokens/cookies/private VPN profiles. Do not inspect credential stores or dump process environments. Jupyter authentication is performed by the user in their existing session. Do not run or publish an unknown notebook wholesale. Use its supplied runtime call after inspection; do not invent a remote inference endpoint. Export only allowlisted execution metadata and explicit numeric tensors, not entire notebook outputs/session state.

Do not commit source videos, weights, ONNX/TPU binaries, runtime state or the research archive. Existing Deep-Research content is historical and read-only: never re-add or modify it during implementation. Artifacts live under /workspace/artifacts, outside Git. This workspace is not volume-backed; external preservation remains necessary. No remote push, public service or message to another person is implied by delegation.

## Dependencies and verification

Keep the existing main PyTorch environment intact. Compiler environment /workspace/.venvs/linq-sdk and preparation environment /workspace/.venv-cv-prepare are separate. Do not install drivers, modify kernel networking or attempt Docker-in-Docker. Use actual supplied SDK versions and artifact hashes.

Run meaningful owned tests; orchestrator runs python -m unittest discover -s tests -q plus affected integration checks. Preserve failed experiments alongside corrected candidates. Report exact commit, checks run, evidence paths, remaining blockers and claims not verified. Update docs/TASKS.md only through the orchestrator. A completed coding agent is not an active worker; report live status honestly.
