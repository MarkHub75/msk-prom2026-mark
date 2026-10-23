# MVP architecture

Approved scenarios: missing helmet, suspected fall transition, prolonged lying; visible-keypoint immobility updates the same posture incident. Backend and frontend remain team-owned.

```mermaid
flowchart LR
  V[Video / camera] --> I[ML worker: bounded latest-frame ingress]
  I --> P[RGB letterbox + model manifest]
  P --> L[Explicit inference backend]
  L --> T[LinQ supplied runtime]
  T --> D[Named outputs + original-coordinate decoder]
  D --> B[Per-camera tracker + temporal rules]
  B --> E[Exact-frame snapshot + event revision]
  E --> O[Atomic behavior checkpoint + SQLite outbox]
  O --> A[Team backend: persist then ACK]
  A --> U[One incident alert + filtered journal]
```

## Interfaces and ownership

Canonical contracts and schemas: docs/CONTRACTS.md, ml/contracts/schemas. Detection owns preprocess/decode, model manifests and float/TPU tensor comparison. Behavior owns per-camera ordered state, ambiguity, temporal evidence and event lifecycle. LinQ owns supplied runner, tensor ABI, program hashes and execution records. Root owns pipeline, durable delivery and cross-module validation.

Pose candidate has four outputs before coordinate/confidence concatenation. Host processing only assembles already-decoded tensors, NMS and coordinate mapping. A detector or pose graph with runtime_abi_verified=false cannot enter the video LinQ path. Runtime codec/name changes require explicit bindings and tests.

## Deployment and current access

Vast RTX4090 is used for preparation and explicitly labelled reference comparisons. ResNet50, Helmet and Split-Pose have completed actual correlated status-0 calls through the official PyTask codec and AMQP bridge at127.0.0.1:15672. The reviewed model programs were placed through a bounded explicit Jupyter consumer, with returned SHA256 checks. Broker access itself never implies remote filesystem access. Models are not trained or recompiled in the video integration stage.

The file MVP uses the existing video CLI and `ml.linq.video:create_runner`. New runtime manifests are derived from the existing real captures, compiler ABI, staging receipts and hashes; historical candidates remain unchanged. One stream submits models sequentially. Per-logical-frame state points to a durable AMQP UUID; terminal results are reused, UNKNOWN reconciles receive-only, and NOT_SUBMITTED alone permits a fresh UUID. A cross-model fence blocks new submissions behind an unresolved request.

The source fingerprint and stream epoch persist across process restarts. SQLite commits the source cursor, observation, behavior checkpoint and event revisions together. Pausing for a pending request preserves the same frame; source gaps and terminal model failures never count as safe observations. Evidence stores the exact original frame ID/PTS and source/RGB/JPEG hashes before event commit. Backend delivery uses the original v1 event schema and persisted ACK contract; see docs/BACKEND_HANDOFF.md. A local test receiver is explicitly separate from Mark's backend.

Real industrial-frame checks and clearly marked repeated-image integration fixtures must be reported separately. A successful end-to-end fixture is not target-video accuracy or throughput validation. Frame cycles include both model calls and can take tens of seconds; this MVP makes no real-time claim.

## Reliability and boundaries

One latest decoded live frame bounds backlog. Media time drives rules; late/old-epoch responses cannot extend dwell. Missing/ambiguous head observations remain unknown. Event and behavior state commit atomically; retries retain event/revision identity. Snapshot is saved before publishing, and backend-accessible evidence hosting must be configured. Recovery/notification state is separate from observed hazard state.

No source videos, credentials or model binaries in Git. No claim of unconsciousness, validated industrial accuracy, exactly-once external effects, multi-camera capacity or real-time latency until the relevant end-to-end evidence exists.
