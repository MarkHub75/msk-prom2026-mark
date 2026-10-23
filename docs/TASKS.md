# Active ML/CV task register

Baseline: matvey_cv 118e068b; continuation retains the approved MVP. Root is the sole writer here. Existing 61 tests and model/compiler/simulator evidence are documented in docs/STATUS.md.

| ID | Owner / directory | Task | Acceptance | State |
|---|---|---|---|---|
| LQ-01 | LinQ / agents/linq | Capture a real supplied notebook call without notebook/session secrets | Numeric tensors + program/input/output hashes + timing; safe failure; tests; user-run cells/runbook | Assigned; hardware call pending user session |
| CV-02 | Detection / agents/detection | Compare captured TPU tensors to float/golden and decode split pose | Explicit name map, shape/dtype checks, per-output and decoded differences; tests; no automatic PASS quality claim | Assigned |
| BH-02 | Behavior / agents/fall | Reproducible event acceptance scenarios | Helmet, fall, lying, immobility, gaps, ambiguous owners, no repeat; source-native backend label; deterministic semantic expectations | Assigned |
| OR-02 | Root / project | AGENTS, architecture, contract consistency, review and integration | Isolated branches, no main/research/media changes, combined tests pass | In progress |
| HW-01 | User existing Jupyter | Run stock example.ipynb and export safe capture | Completed ResNet50 TPU call; no credentials/full notebook outputs in export | Waiting for prepared capture instructions |
| APP-01 | Backend/frontend team | Real event endpoint, evidence serving, alert/journal | Persist-before-ACK + idempotent event revisions + visible evidence and filters | External integration pending |

Historical completed coding agents are not counted as running. Live state must be checked through native agent tools; this table records work items rather than pretending hardware access or background execution.
