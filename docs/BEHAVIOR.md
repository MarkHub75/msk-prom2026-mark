# Behavior Analysis v1

`from ml.behavior import BehaviorEngine`

```python
engine = BehaviorEngine({"zone_id": "workshop-01"})
mutations = engine.update(observation_batch)
interrupted = engine.on_gap({"camera_id": "cam-01", "stream_epoch": "e1",
                             "media_time_ms": 4500, "reason": "inference_timeout"})
checkpoint = engine.export_state()  # plain JSON-compatible mapping
# Commit checkpoint and event/outbox mutations in one transaction.
restored = BehaviorEngine({"zone_id": "workshop-01"})
restored.restore_state(checkpoint)
```

One ordered owner per camera calls the engine. Combine the pose model's `person`
boxes and COCO-17 keypoints with PPE model `bare_head` / `helmet` boxes in the
same original-image coordinate space and source frame. The engine uses the
shared `ObservationBatch` and event contracts. Optional batch `model_ids`
records all contributing models. Evidence starts `pending`; the pipeline owns
snapshot production, publication readiness, persistence and delivery.

## Rules and configurable defaults

- Detection/keypoint acceptance: score >=0.5; thresholds are policy values.
- Helmet: a positive `bare_head` bbox must contain a visible head keypoint and
  have its centre inside exactly one person's bbox. Multiple items or candidate
  owners are unknown. An explicit `helmet` observation closes an open missing-
  helmet incident; non-detection is unknown. Dwell is 2000 ms.
- Pose: shoulders and hips (COCO indices 5,6,11,12) must be visible. A torso
  vector >=10 px is required. Horizontal torso ratio >=1.3 and bbox width/height
  >=1.15 give a lying candidate; vertical torso ratio >=1.3 and bbox ratio <=0.85
  give upright. Other poses are unknown. Optional `floor_polygon` (original
  pixel coordinates) restricts the lying bbox centre to a configured ground ROI.
- A last upright observation followed by lying within 1500 ms is a suspected
  fall, confirmed after 1000 ms lying. Lying without an observed transition is
  prolonged lying, confirmed after 3000 ms. Recovery closes the posture event.
- Source-time gap >750 ms interrupts active events, clears pending evidence and
  starts a new tracking generation. Explicit gaps/errors do likewise. No dwell
  bridges unknown pose, missing person observations, or failed inference.
- Visible-keypoint immobility is an attribute on the existing posture incident,
  never a new alert or medical diagnosis. For consecutive lying observations,
  require at least 6 common visible body keypoints (COCO 5..16). Compare the
  maximum keypoint displacement, normalized by observed torso length and elapsed
  seconds, against 0.04 torso lengths/second. The maximum prevents a moving wrist
  from being hidden by many stationary joints. Require 3000 ms continuously low
  observed motion after the first valid motion comparison. All values are
  configurable (`immobility_min_points`, `immobility_max_speed`,
  `confirm_immobility_ms`); movement, unknown pose, insufficient common points,
  missing observations and gaps reset the pending window.
- First immobility confirmation emits one new revision of the same event with
  `attributes.immobility_observed=true`, `immobility_since_media_ms`, and
  `immobility_confirmed_media_ms`. This records a historical observed interval,
  not a promise that the person remains still afterwards. No repeat confirmation
  update is emitted for that incident. Pending motion history and the confirmed
  marker persist in engine checkpoints.
- A valid empty frame clears candidates and permits track-exit accounting; it
  is different from a gap. A track absent >2000 ms closes with `track_exit`.
- Matching uses bbox IoU plus normalized centre distance; conflicting near-equal
  matches are not applied. Full key is camera/epoch/generation/local-track-id.
- Duplicate/late frames and previously retired epochs are ignored. New source
  epochs interrupt old events. Different cameras have independent state.
- At most one helmet and one posture notification are opened per uninterrupted
  tracked presence. Posture never generates a second alert when a suspected
  fall becomes long lying. After observed compliance/recovery, the same tracked
  presence remains suppressed; updates do not create new notification IDs.
- Restart suppression requires atomic persistence of `export_state()` alongside
  mutations/outbox and preservation of source epoch/timestamps. A checkpoint
  cannot be restored with different configuration; restart migration is explicit.

Set `allow_bbox_head_association=true` only after validating sparse, upright
views: this opt-in permits an item in the upper 30% of a narrow upright bbox
without visible head keypoints. Default is false.

## Evidence boundary and limitations

This is implemented temporal logic over neural observations, with synthetic
fixture tests. Geometric pose thresholds are not trained fall recognition,
physical floor contact, injury, intent, or a diagnosis of lost consciousness.
They need camera-specific tuning and independent target-video evaluation.
Perspective, leaning, work under machinery and tracking fragmentation remain
important negative examples. Immobility uses visible body-keypoint motion, not a stable bbox alone. Occluded
limbs, small/faint motion, keypoint jitter, perspective and camera motion limit
this measurement; it does not prove whole-body physical immobility.

Identity cannot be guaranteed across occlusion, ambiguous crossings, a stream
reset or a lost tracker. Such cases interrupt evidence or abstain instead of
borrowing another person's history; a later generation may create a new event.
No claim of human re-identification or exactly-once semantic incidents across
unknown gaps is made. Transport idempotency belongs to the event store/receiver.

Run `python -m unittest discover -s tests -p test_behavior.py -v`.

## BH-02 deterministic acceptance scenarios

Generate synthetic observations and a semantic expectation manifest in an
explicitly selected artifact directory:

```bash
python -m ml.behavior.scenarios \
  --output-dir /workspace/artifacts/behavior/acceptance
# Optional selection; repeat --scenario to select several independent cameras.
python -m ml.behavior.scenarios \
  --output-dir /workspace/artifacts/behavior/fall-only \
  --scenario fall_immobility
python -m ml.pipeline.cli --state-dir /workspace/artifacts/behavior/replay-state \
  replay --input /workspace/artifacts/behavior/acceptance/observations.jsonl
python -m unittest discover -s tests -p 'test_behavior*.py' -v
```

`observations.jsonl` contains normalized detector observations, not source images
or model outputs. Every batch uses `backend="synthetic-test"`. `expected.json`
contains explicit scenario descriptions, expected incident types, confirmation
media times, revision/state sequences, immobility flags and notification counts.
UUID values and emission UTC are intentionally not predetermined: expectations
instead require each incident's revisions to retain the same generated UUID.
Existing output files are not overwritten unless `--overwrite` is explicit.

The eight independent cases cover these temporal contracts:

| Scenario | Observations | Incidents | Persisted revisions | Expected meaning |
|---|---:|---:|---:|---|
| missing_helmet | 10 | 1 | 1 | Two seconds of positive bare-head evidence, one notification |
| fall_immobility | 14 | 1 | 2 | Observed transition; later immobility updates the same UUID |
| starts_lying | 12 | 1 | 2 | Prolonged lying without claiming an observed fall |
| compliance | 12 | 0 | 0 | Visible helmet and upright pose |
| gaps | 13 | 1 | 2 | Gap breaks pending dwell and interrupts confirmed incident |
| ambiguous_people | 12 | 0 | 0 | Shared head ownership remains unknown |
| no_repeat | 16 | 1 | 2 | Compliance closes; reappearance of bare head during same presence does not notify again |
| epoch_reset | 12 | 2 | 3 | New clock creates new identity; previous end time uses previous epoch clock |

Open incidents at finite trace end are censored; the generator does not fabricate
EOF hazard resolution. JSONL replay has no media and correctly reports evidence
unavailable. It cannot demonstrate useful visual evidence or live video ingress.

### Test report — 2026-10-23

On integration baseline `d88d0844`, all 30 owned behavior/acceptance test methods
passed; the eight scenario subcases exercise the actual `Pipeline` and SQLite
`Outbox` with temporary state directories. Each case restarts the process midway,
restores committed state, finishes, restarts again and replays the entire trace.
The checks assert persisted UUID/revision identity, no reopened incidents or
additional notifications, one immutable record per revision and no regression of
an old epoch's end time below its confirmation time.

Delivery acceptance uses an explicitly labelled **test-double receiver** following
the documented backend idempotency contract. It simulates a lost ACK after a
receiver commit and verifies that Outbox retry preserves the revision payload
and does not add another notification. This does not test the team's production
backend, UI, network availability or receipt of a real operator alert.

The acceptance replay exposed a concrete duplicate-gap bug: replaying an already
accepted equal-time gap incremented the tracking generation after restoration.
The engine now ignores a repeated gap when the last accepted item was already
that gap, while preserving a first EOF gap at the last valid frame timestamp.
No behavior threshold changes were needed.

The full baseline suite also passed: **64 test methods**, including the 30 owned
methods. Generated example artifacts: `/workspace/artifacts/behavior/bh02-acceptance/`
contains 101 synthetic observations plus the expected semantic manifest.

These results establish synthetic temporal/persistence contracts only. They
establish neither neural inference nor TPU execution, target-video accuracy,
false-alarm rates, real-world fall recognition, nor delivered-alert latency.
