# MOSPROM ML/CV implementation guide

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
