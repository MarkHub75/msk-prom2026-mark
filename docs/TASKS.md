# Active ML/CV task register

Baseline: matvey_cv 118e068b; continuation retains the approved MVP. Root is the sole writer here. Existing 61 tests and model/compiler/simulator evidence are documented in docs/STATUS.md.

| ID | Owner / directory | Task | Acceptance | State |
|---|---|---|---|---|
| LQ-01 | LinQ / agents/linq | Capture a real supplied notebook call without notebook/session secrets | Numeric tensors + program/input/output hashes + timing; safe failure; tests; user-run cells/runbook | Code merged fd5adcbf; real capture pending user session |
| CV-02 | Detection / agents/detection | Compare captured TPU tensors to float/golden and decode split pose | Explicit name map, shape/dtype checks, per-output and decoded differences; tests; no automatic PASS quality claim | Merged 133ea22e; actual TPU capture pending |
| BH-02 | Behavior / agents/fall | Reproducible event acceptance scenarios | Helmet, fall, lying, immobility, gaps, ambiguous owners, no repeat; source-native backend label; deterministic semantic expectations | Merged 50dd2f65; 8 scenarios / 101 observations / 7 incidents / 12 revisions |
| OR-02 | Root / project | AGENTS, architecture, contract consistency, review and integration | Isolated branches, no main/research/media changes, combined tests pass | Implemented; checkpoint RESUME.md, 96 combined tests PASS |
| HW-01 | User existing Jupyter | Run stock example.ipynb and export safe capture | Completed ResNet50 TPU call; no credentials/full notebook outputs in export | User reports stock status_code=0/class257/0.39s; numeric capture pending |
| APP-01 | Backend/frontend team | Real event endpoint, evidence serving, alert/journal | Persist-before-ACK + idempotent event revisions + visible evidence and filters | External integration pending |

Historical completed coding agents are not counted as running. Live state must be checked through native agent tools; this table records work items rather than pretending hardware access or background execution.

Checkpoint saved at user request: see ../RESUME.md. All three coding agents completed; no continuing background tasks. The later resumed packaging stage below supersedes that checkpoint; the current kit has been built.

## Resumed packaging stage

- KIT-01: current portable kit builder, runtime-only source/dependencies/docs and existing Helmet + Split-Pose TPU programs; archive is /workspace/artifacts/linq-jupyter-kit.zip. Inventory and isolated imports/model preparation checked.
- LQ-02: portable prepare_case/capture_case merged from agent/linq 56a3d13f; no new training, export or SDK experiments.
- Binding limitation: actual remote example.ipynb import/call/result extraction is still not available locally. User was asked for only credential-free code. bindings.py refuses to issue any request until an actual binding exists. The public local pytpu example is clearly labelled LOCAL and is not substituted for the working remote API.
- Current suite:113 tests PASS. Stock inference is confirmed by user report; own-model hardware capture remains pending.

## Own-model upload and network resilience

- STOCK-RPC: actual automatic ResNet50 completed, results/integrity outside Git; never repeat as a connection check.
- DEPLOY-01: pinned two-model upload agent and one-command orchestration implemented. Latest file-upload preflight: agent not ready, no publication. Await user bootstrap cell in existing Jupyter.
- RPC-RECOVERY: add durable pre-publication journal, UNKNOWN state, preserve late-response queues and reconcile without publish after reconnect. LinQ agent owns transport changes in its worktree; root owns integration/resume.
- INFRA: Arch user manages autossh/systemd/VPN; Vast must not change this configuration.
- Tests:160 combined tests most recently passed; run only new/affected recovery checks for upcoming changes.
