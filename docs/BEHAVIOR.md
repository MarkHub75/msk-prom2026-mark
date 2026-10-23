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

## Saved LinQ capture audit for sequential video sampling

Audited on integration baseline `0c4cb5ff`; this section describes **replay of
saved decoded single-image results**, not a new video inference run. No broker,
Jupyter session, password or live TPU call is used by these tests.

External inputs:

- `/workspace/artifacts/linq-rpc/helmet-001/detections.json`
- `/workspace/artifacts/linq-rpc/pose-split-001/detections.json`

The test pins both decoded-file SHA256s and verifies that their numeric
`inputs.npz` arrays match the same captured input SHA256:
`9f03adcc058f220364e1c1ebcc5e41051702228a11083c655356413bd4611160`.
Both were prepared from the same 810×1080 bus photograph. Capture status is
completed. Their saved hardware-placement evidence is user-supplied runtime
attestation, not independent hardware verification by these behavior tests.
Artifacts are external and not copied into Git; tests explicitly skip when they
are absent, and fail if present files differ from the pinned capture.

### Confidence and ownership

The saved helmet output contains two `bare_head` detections with unchanged scores
**0.35258615016937256** and **0.25950342416763306**. The saved SplitPose output
contains three persons with scores about .8833/.8694/.8554. The first two head
boxes each contain observed head keypoints of a separate person and have their
centres within that person's bbox. Strict pose-based ownership succeeds without
bbox fallback. The third person has no associated positive bare-head observation
and remains unknown for the helmet rule. Its partly unobserved torso does not
establish a lying or fall event.

The default behavior `min_score=.5` rejects both head candidates and produces no
missing-helmet events. That is expected policy behavior, not an integration
failure. For an explicitly labelled **DEMO** investigation the orchestrator may
choose this policy in its own configuration:

```json
{
  "min_score": 0.25,
  "keypoint_score": 0.5,
  "allow_bbox_head_association": false,
  "rule_version": "demo-low-confidence-v1"
}
```

No engine default is changed by this audit. `min_score` currently applies to all
object classes, including persons; the demo setting is not a class-specific
helmet threshold. Keypoint confidence, visibility, one-to-one ownership,
confirmation windows, missing-observation handling and repeat suppression remain
unchanged. The decoder already uses confidence .25 for this model: raising the
behavior threshold afterwards cannot recover filtered detections, and changing
the threshold must never rewrite or inflate model scores.

Choosing .25 admits an additional unvalidated candidate: saved numeric/reference
comparison has one head matched to the reference and a second actual head
unmatched. This is not ground-truth proof of a false positive or true positive.
The lower setting is useful for integration diagnostics only until independently
reviewed on target video; it does not establish a precision improvement or
industrial acceptance.

### Source time versus wall time

For a **prerecorded video processed offline**, ordered samples with actual source
PTS 0,500,1000,1500,2000 ms satisfy the current 750 ms maximum observation gap.
Five positive samples can confirm the two-second helmet episode even if each
sequential pair of model requests takes roughly 20 seconds of wall time. The
engine deliberately uses source media time, not request duration, for this
semantic rule. Outputs of both models must come from the same immutable source
frame with the same epoch/geometry; do not merge results of successively decoded
frames merely because their calls completed nearby.

Saved single-image call times are approximately 10.23 seconds for Helmet and
11.15 seconds for SplitPose, with total wrappers about 21.43 seconds combined.
Applying those single-image observations illustratively, five sequential paired
samples could require over 100 seconds of processing before the first alarm;
this is not a measured video benchmark. A two-second **media** confirmation is
therefore not a two-second delivered-alert delay or real-time capability.

For a **live latest-frame** source, actual PTS gaps of ~20 seconds exceed the
750 ms rule limit and correctly interrupt candidates. Do not assign fabricated
500 ms PTS to old or newly captured frames, enlarge `max_gap_ms` to hide slow
inference, or interpret an unchanged screenshot as new evidence. Sparse samples
can also miss a rapid fall: an unobserved transition remains unknown; subsequent
observable lying may independently confirm `prolonged_lying` after its own
continuous observation window. Missing observations never prove recovery.

A repeated saved screenshot is useful only for testing association, timer
contracts and persistence. It cannot validate behavior recognition over time,
fall detection, temporal recall, camera motion, tracking continuity in real
video, or delivered-alert latency. The replay test backend is explicitly
`replayed-real-capture`, while its modified negative controls are marked as such.

### Focused acceptance report

`python -m unittest discover -s tests -p 'test_behavior*.py' -v` passes **37 tests**
on the available artifact set, with **zero artifact-related skips**:

- Unmodified saved detections at 500 ms source intervals yield exactly two
  missing-helmet incidents at 2000 ms under the explicit demo policy; no fall or
  lying incident is created and model scores remain unchanged.
- Real `Pipeline`/SQLite `Outbox` checkpoint restart and complete replay preserve
  those two event UUIDs at revision 1 without repeated opening or replacement
  incidents. Snapshot evidence correctly remains unavailable in observation-only
  replay.
- The same capture at 1000 ms source intervals cannot accumulate dwell.
- An explicit missing observation breaks pending confirmation; low-confidence
  head observations and insufficiently visible head keypoints remain unknown.
  These negative controls are deliberately modified copies of saved results,
  not additional actual model outputs.
- A separate honestly labelled synthetic transition case with a gap before lying
  does not establish `suspected_fall`; only later prolonged lying is observable.

No behavior-engine change was needed for these captured observations. The audit
adds acceptance checks and guidance, not a new violation type, relaxed ownership
or a claimed production quality result.
