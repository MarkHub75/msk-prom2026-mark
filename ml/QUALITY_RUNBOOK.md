# Reproduce and inspect ML quality experiments

Start with EVAL_REPORT.md, SCENARIOS.md and EXPERIMENTS.csv. These are development diagnostics. Independent test and an accurate industrial release are not yet established. Data Orchestrator owns new source acquisition/curation; ML does not edit its worktree.

## Inspect completed evidence first

* Helmet baseline and rejected thresholds: /workspace/artifacts/quality/helmet/e01-v3-rescore/e02-predeclared-comparison.json.
* Rejected tiling: /workspace/artifacts/quality/helmet/h02-tiles-v1/comparison.json.
* Native Fall E00: /workspace/artifacts/quality/pose/e00-native-ur20/run.json and event-evaluation-v1.1.json.
* Paired 2FPS quantized references: /workspace/artifacts/quality/pose/e03-ur20-{baseline-ptq,candidate-ptq}/. Only status COMPLETED with225 calls is eligible for scoring.
* Actual baseline LinQ: /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps/. journal-integrity-review.json verifies all11 correlated status0 numeric journals; sdk-input-parity.json and sdk-decoded-comparison.json compare the exact source inputs and decoded outputs. performance-first-call-window.json keeps uncached timings; finalization/cached timings are separate.

Source-author coarse posture reference and prediction-blind sampled AI review are not expert exhaustive GT. At matched 2FPS the source indices are0,15,30,... with original PTS, not fabricated timestamps. Prolonged lying has no eligible positive support in this subset.

## Local software checks

```bash
cd /workspace/project
/workspace/.venvs/linq-client/bin/python -m unittest discover -s tests -q
```

The AMQP runtime environment intentionally has no Torch. Fixture tests mock Torch without installing it; actual native/SDK experiments use their existing separate environments. Tests do not measure model accuracy.

## Explicit native/SDK diagnostics

Already completed experiments must not be rerun merely to regenerate a report. For an authorized new data version, use a fresh output directory and the shared GPU allocation protocol:

```bash
/venv/main/bin/python -m ml.quality.pose_reference \
  --reference /path/to/frozen-development-reference.json \
  --manifest /workspace/artifacts/detection/pose-split/manifest.json \
  --weights /workspace/artifacts/detection/pose-split/weights.pt \
  --output /workspace/artifacts/quality/pose/NEW-native-run --device cuda:0

/workspace/.venvs/linq-sdk/bin/python -m ml.linq.quantized_video \
  --reference /workspace/datasets/quality/temporal/urfall-reference.json \
  --manifest /workspace/artifacts/detection/pose-split/manifest.json \
  --compile-dir /path/to/reviewed-compile \
  --output /workspace/artifacts/quality/pose/NEW-sdk-run \
  --frozen-selection /workspace/artifacts/quality/pose/e03-ur20-2fps-frozen-selection.json \
  --budget-seconds 600
```

The first command acquires /workspace/artifacts/quality/gpu.lock nonblocking. Coordinate all heavy jobs with Data Orchestrator; an advisory lock cannot constrain an external process which ignores it. The second command is CPU-only, two pinned CPUs, checks all selected RGB hashes/counts before loading its graph, and cannot be presented as TPU execution.

## Existing real LinQ worker

This exact completed run reuses its state and makes no new requests. It is useful for inspecting the command; do not replace the state directory merely to repeat the benchmark.

```bash
cd /workspace/project
set +x
set -a
source /workspace/linq-client/connection.env
set +a
export PYTHONPATH=/workspace/linq-client:/workspace/project
/workspace/.venvs/linq-client/bin/python -m ml.pipeline.cli \
  --state-dir /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps \
  video --source /workspace/datasets/quality/temporal/processed/urfall/fall-01-cam0-rgb.mp4 \
  --camera-id urfall-development-fall-01 --backend linq \
  --linq-runner-factory ml.linq.video:create_runner \
  --manifest /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps/pose-split-verified.json \
  --sample-fps 2 --max-frames 11 --end-ms 5333 --linq-timeout 60
```

Runtime credentials stay outside Git and logs. UNKNOWN means resume the same durable request receive-only, not a fresh TPU submission. No local neural fallback. The candidate program is not allowed by baseline runtime bindings and is not automatically staged. Preserve baseline names/hashes and completed journals.

## Running/Zone

```bash
python -m ml.quality.temporal.running_zone \
  --input /path/to/observation-batches.jsonl \
  --config /path/to/reviewed-camera-geometry-and-speed-policy.json \
  --output /workspace/artifacts/quality/NEW-running-zone-diagnostics.jsonl
```

This emits internal UNVALIDATED_PROTOTYPE diagnostics. A speed threshold in pixels/s or image diagonals/s is camera-specific and does not establish running. No m/s without physical calibration. Zone geometry needs a version, source and explicit camera identity; arbitrary polygons cannot establish a safety violation. Public event schemas and application services remain unchanged.

## Checkpoint and rollback

RELEASE_MANIFEST.json pins both selected baseline checkpoints, exports, TPU hashes, thresholds, codec and behavior code. Rejected tile/host-rule/PTQ artifacts remain separate and are never silently selected. Restoring a prior model is an explicit manifest/config selection with a fresh run state; do not edit old request identities or overwrite compiled baseline files.

The local model-only archive is /workspace/artifacts/quality/release/mosprom-ml-models-quality-checkpoint-20261024.tar.gz; its checksum is in model-backup-local.json. It contains no source images/videos or numeric input/output captures. Local storage is not an off-Vast backup; external destination/readback is a separate release gate.

Offline motion episode scoring and explicitly labelled fixture command: see ml/quality/temporal/MOTION_EVAL.md. Final default test discovery includes335 tests. A SYNTHETIC_FIXTURE result is never a real data accuracy metric.
