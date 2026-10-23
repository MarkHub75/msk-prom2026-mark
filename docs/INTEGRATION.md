# ML-worker integration v1

## Scope and verified boundaries

The worker owns video sampling, inference adapters, observation ordering, pose/head ownership, episode rules, snapshots and a persistent event outbox. Backend/frontend remain team-owned. It does not start a public service or modify their source.

Three execution boundaries are explicit: observation JSONL replay (no neural inference), `native` (PyTorch reference), `linq` (requires provisioned TPU runner). Neither replay nor native is evidence of LinQ execution.

## Run

From repository root, with installed project dependencies:

```bash
python -m unittest discover -s tests -v
python -m ml.pipeline.cli --help
python -m ml.pipeline.cli --state-dir runtime video \
  --source /path/to/input.mp4 --backend native --device cuda:0 \
  --manifest /workspace/artifacts/detection/pose/manifest.json \
  --manifest /workspace/artifacts/detection/helmet/manifest.json
```

Both manifests are required for the two-scenario MVP. An explicit detector-only diagnostic does not satisfy pose ownership. Video file timestamps must advance; source loops start a new epoch. Live ingress has one latest decoded frame and rejects stale results. Receive time is not camera capture time; reported cycle latency does not measure camera buffering or delivered-alert latency. Live source loss raises/stops the worker; automatic reconnect is not implemented. Maximum usable observation gap defaults to 750 ms: if measured processing cannot sustain this, temporal rules abstain rather than fabricate continuity.

JSONL replay:

```bash
python -m ml.pipeline.cli --state-dir runtime replay --input observations.jsonl
```

Replay does not fabricate a snapshot. Events without media have evidence status unavailable.

## Backend handoff

Configure the full event URL with `--backend-url https://.../api/v1/ml/events`. Backend credentials are read only from the process environment `MOSPROM_BACKEND_TOKEN`; never place them in Git or CLI arguments. Authenticated non-loopback HTTP and redirects are rejected.

The backend must commit events idempotently by `(event_id, revision)` and return JSON:

```json
{"committed": true, "event_id": "the-exact-event-id", "revision": 1}
```

A 200 status without this ACK is not enough. Receiver must send one notification on incident opening, upsert later revisions, and treat operator review separately from incident state. Filtering: type, camera, zone, media/UTC time. Wall UTC is emitted_at; media_time_ms is not a Unix timestamp.

Snapshots are atomically written under state-dir/evidence before event COMMIT. The receiver must have access to this exact artifact tree. Set `--evidence-base-url https://.../ml-artifacts` to the configured serving prefix. Worker does not expose files or claim an arbitrary local path is reachable. If media status is ready and no serving prefix is configured, dispatch remains pending. Provision shared artifact serving with the backend team before a remote demo. Do not expose secrets or SQLite state through this prefix; serve only evidence/.

```bash
python -m ml.pipeline.cli --state-dir runtime \
  --backend-url https://.../api/v1/ml/events \
  --evidence-base-url https://.../ml-artifacts dispatch
```

Outbox records and behavior checkpoint commit in one SQLite transaction. Retries reuse IDs/revisions and use bounded backoff. A send accepted by backend followed by a worker crash can resend; backend deduplication is mandatory. Single worker owns the state directory; do not share SQLite across hosts. Snapshot files can become orphaned after storage failure; keep runtime retention bounded operationally until automated cleanup is added. A fresh CLI video run creates a new source epoch; checkpoint identity is preserved for continued same-epoch observation replay, not cross-restart person reidentification.

## Quality evaluation

`python -m ml.pipeline.evaluation --truth truth.json --predictions events.jsonl`

Truth is a JSON array of fully reviewed observable intervals with camera_id, stream_epoch, type, start_media_ms, end_media_ms. Predictions contain only worker JSONL event records. Revisions count once. Matching requires same camera/epoch/type and confirmation within both the GT interval and the configured 5-second onset deadline. Output is finite-corpus timely confirmation precision/recall; it is not delivered-alert quality, natural false alarms/hour or deployment reliability. Absence of GT yields undefined recall, not 100%.

Before claiming MVP quality, independently review >=20 positive episodes per declared type and >=30 minutes of negatives including bends, crouches, work near the floor, occlusion, helmets held in hand, crowded ownership, motion and gaps. Keep calibration/tuning and evaluation groups separate. Targets are precision >=.90, recall >=.80; delivered-alert p95 <=5 seconds remains unmeasured until real LinQ and backend are connected.

## Branch ownership

- agent/detection: ml/detection and its tests/docs.
- agent/fall: ml/behavior and its tests/docs.
- agent/linq: ml/linq and its tests/docs.
- matvey_cv: contracts, dependencies, pipeline and integration.
- agent/speed: preserved, inactive in this MVP.

Merge small verified commits into matvey_cv. Do not simultaneously edit common contracts. Model binaries/runtime files stay outside Git. /workspace is not volume-backed: git commits and artifacts need an authorized remote backup; no remote push is performed implicitly without an established destination.

## LinQ model binding

The detection manifest retains its original preprocessing/decoder fields. Add a `linq` block only after checking the compiled runtime ABI on the execution host:

```json
{
  "linq": {
    "runtime_abi_verified": false,
    "program_path": "compiled/model.tpu",
    "program_sha256": "REPLACE_WITH_ACTUAL_SHA256",
    "inputs": [{"name": "ACTUAL_RUNTIME_INPUT", "shape": [1, 3, 640, 640], "dtype": "float32"}],
    "outputs": [{"name": "ACTUAL_RUNTIME_OUTPUT", "shape": [1, 6, 8400], "dtype": "float32"}],
    "input_map": {"images": "ACTUAL_RUNTIME_INPUT"},
    "output_map": {"ACTUAL_RUNTIME_OUTPUT": "output0"}
  }
}
```

This is a helmet binding template, not actual runtime metadata. Pose has a different output shape. Do not change dtype/layout/shape merely to match a template. The worker refuses unverified ABI. Once validated, `--backend linq` opens one context-owned `LocalPytpuRunner` per model on a host with the actual runtime/device. A supplied remote bridge can instead be configured with `--linq-runner-factory package.module:create_runner`; factory receives that model's effective manifest and returns a callable `(inputs, metadata)` or a context manager yielding one. It must preserve request/model/program correlation and own the remote lifetime. No remote transport is guessed or automatically exposed.
