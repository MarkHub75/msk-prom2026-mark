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

## Temporal quality sprint: audited source intake (2026-10-23/24)

The complete `/workspace/ML_24H_PLAYBOOK.md` was read before this intake. Existing
research was inspected read-only. No GPU, model inference, TPU request, backend
change, external event type change or final-test evaluation was performed.

### Available source references and rights

| Source | Primary-source audit | Current local use |
|---|---|---|
| [URFall](https://fenix.ur.edu.pl/~mkepski/ds/uf.html) | Author RGB/depth sequences, synchronization CSV and depth-frame posture labels; CC BY-NC-SA 4.0 with explicit non-commercial academic-use restriction | 20 deterministic development/validation clips and source reference; no redistribution/public-demo/commercial clearance claimed |
| [Mendeley Safe/Unsafe v1](https://data.mendeley.com/datasets/xjmtb22pff/1) | Dataset CC BY 4.0; clip-level classes, two IP cameras; company/employee permissions are author claims | Eight existing research clips copied without modifying archive; all already-viewed development |
| [OmniFall canonical repository](https://huggingface.co/datasets/simplexsigil2/omnifall) | Dense temporal CSV annotations, subject/view fields; [label guidelines](https://huggingface.co/datasets/simplexsigil2/omnifall/blob/83572a37b9e3081df8c06a56874b1d1f2a19386c/LABELS.md) state VIA relabeling; original video rights remain separate | Guidelines/structure/class-map metadata only, heldout media/labels/predictions not acquired |

OmniFall's requested `j-c1/omnifall` card points to `simplexsigil2/omnifall`.
Canonical revision is `83572a37b9e3081df8c06a56874b1d1f2a19386c`. Its card header
says CC BY-NC 4.0 while body says annotations/splits CC BY-NC-SA 4.0: retain that
conflict and restricted noncommercial/share-alike scope, not blanket commercial
permission. Staged source videos must be obtained from their original owners;
the synthetic tar alone is 9,716,480,000 bytes and was not fetched. Public CSV
labels exist, but no bounded original-video heldout subset has yet been obtained.
A primary CAUCAFall page was accessible; attempted Mendeley file APIs returned
403/404. No contact, authentication bypass or giant archive download was used.
URFall is not one of OmniFall's eight staged sources.

### Freeze before predictions and CPU preparation

The original first-four fall/ADL selection was extended **explicitly before model
outputs** to first-ten fall + first-ten ADL. The previous selection is preserved
under `selection-history/`. Selection is source-ID-prefix based, not selected for
model success. All 20 sequences stay in one protected component:
`urfall-all-unknown-subjects-shared-cam0`. `cam0` is a front-view role; the fall
laboratory and ADL home scenes differ, and physical camera/actor identity is not
independently established. No claim of actor-, camera- or source-independent
validation/test follows from splitting these clips. `split=validation` means
this is developmental data, never sealed final test.

**Intake:** 26,348,304 bytes of native MP4; 27,445,711 total downloaded bytes
including CSV and metadata, below the approved 100 MB intake. The 20 MP4s contain
3,274 frames / 109.133333 seconds, not 20 independent people or 20 true falls.

Important visual discovery: linked native MP4s are **640×240 DEPTH|RGB montages**.
The left 320×240 panel is depth; only the right 320×240 RGB panel was cropped on
CPU for model input. Derived RGB MP4 frame counts and decoded presentation PTS
were checked against the original preview. Hashes, crop `[320,0,320,240]`, H264
CRF18 transformation, and native paths remain recorded. These low-resolution,
compressed previews are not the full-resolution RGB PNG archives; target quality
claims must disclose the source representation.

Frame CSVs preserve both exact decoded video PTS and independent author
synchronization timestamps joined by **1-based source frame ID**. Their maximum
observed disagreement is 73.667 ms. Use the explicit mapping, not hardcoded
frame/24 or silently interchangeable clocks. Source label holes remain unknown:
59 frames / 1.966666 seconds total, about 1.802% of this selected duration.

### What the labels establish, and what they do not

URFall author labels are `-1` not lying, `0` temporary transition, `1` lying.
They are supplied independently of our model outputs; the page does not detail
who annotated them or establish a second human adjudication protocol. Import
preserves source states and unknowns before any event-policy crosswalk.

- The ten fall clips each contain one author `0` transition followed by `1`.
  All ten falling windows are exactly one second in these source labels; they
  must **not** be treated as validated exact visual onset. Candidate onset support
  spans the source transition window, not its first-frame midpoint or clip start.
- The `1` tail in every one of the ten fall clips is shorter than the current
  three-second prolonged-lying rule. They are right-censored, insufficient
  followup for a fully observable three-second-positive episode. Do not pad,
  loop, repeat frames, or count these as ten valid prolonged-lying positives.
- **ADL-10 is a crucial exception:** author CSV also has `0` then `1`, but blinded
  RGB inspection shows controlled sitting then lying **on a bed**, not an
  accidental fall or lying on the floor. Its 3.367-second lying tail is not an
  industrial floor-violation positive. Neither the ADL folder nor a literal
  source `0/1` alone is an exhaustive violation label.
- ADL-01/02 show crouching; ADL-03 squat/recovery; ADL-04/05/06 bending/picking up;
  ADL-07/08 sitting on a chair; ADL-09 sitting on a bed; ADL-10 controlled sit/lie.
  These are useful hard-negative **review candidates**, not newly fabricated
  exact per-frame action annotations.
- Blind review used RGB contact sheets at every tenth frame plus final frame,
  without model predictions. Its coarse action/onset supports and visibility
  caveats are saved separately. The reviewer is also a behavior-model developer;
  this is not a second independent human review or an untouched final test.
  Body truncation/occlusion and insufficient torso/head observability are kept
  visible instead of being converted into guaranteed detector observations.

The offline `urfall-reference.json` exports native posture intervals, source
annotation hashes, actor-local placeholder, unknown actor group, camera/scene
provenance, onset-support intervals and left/right censoring. Its 22
`episode_candidates` are **not 22 accepted violation episodes**: 11 native
transition windows include ADL-10, and 11 lying-state intervals include the same
bed example and short followup. Candidate scoring status explicitly requires RGB
semantic/visibility review and an agreed event policy. Exact onset latency is
not claimed. `blind-review.json` separately records 10 visually staged falls and
hard-negative actions, with coarse bounds rather than invented exact onsets.

### Existing industrial clips and missing directions

All eight Mendeley clips total 155,778,705 bytes. Their exact research hashes
were rechecked; raw copies live outside Git. Source train/test names are retained
as provenance only. The saved research already found inferred camera views in
both source partitions. Conservatively keep the **entire factory component**
together; unknown camera, actor and session IDs are not invented from filenames.
Clip-level safe/unsafe walkway labels do not supply actor tracks, a zone polygon,
site policy, event onset, separate run labels or a reviewed safe-hour denominator.
The full unreviewed episode scope is explicitly unknown; metrics are N/A.

Production **Running and Zone intrusion are NOT_IMPLEMENTED**. A stored zone ID
or a floor polygon for lying does not implement intrusion. OmniFall `walk`
explicitly includes jogging/running, so its label cannot provide independent
run-vs-walk GT. No camera polygon/rule provenance and blind actor/entry timestamps
were available for a defensible running/zone experiment; none was invented.
Their precision/recall are `null`/N/A, not zero or a measured baseline. External
JSON/event schemas remain frozen.

### Reproducible commands and handoff

```bash
python -m ml.quality.temporal.acquire \
  --root /workspace/datasets/quality/temporal --count 10 --max-bytes 100000000
# Prefix expansion requires --extend-selection; it is never silent.
python -m ml.quality.temporal.urfall \
  --root /workspace/datasets/quality/temporal --contacts
python -m ml.quality.temporal.audit reference \
  --input /workspace/datasets/quality/temporal/urfall-reference.json \
  --output /workspace/datasets/quality/temporal/reference-audit.json --verify-media
python -m ml.quality.temporal.audit mendeley \
  --source Deep-Research/datasets/_WORK/MATERIALS/W2-10 \
  --root /workspace/datasets/quality/temporal --copy-media
python -m unittest discover -s tests -p 'test_temporal_quality*.py' -v
```

API: `acquire(root,count,max_bytes,extend_selection=False)` freezes source IDs;
`urfall.prepare(root)` returns and writes the reference; `audit_reference(ref,
verify_media=False)` checks exhaustive known/unknown coverage, source groups and
exact-copy split isolation without looking at predictions. Mendeley intake never
writes the historical source archive. No source videos or annotations are added
to Git.

Artifacts ready for the orchestrator's E00 CPU/GPU inference, not yet quality
scores:

- `processed/urfall/*-cam0-rgb.mp4` and `*-frames.csv`;
- `selection.json`, `selection-history/`, `download-ledger.json`;
- `urfall-reference.json`, `reference-audit.json`, `blind-review.json`;
- `mendeley-intake.json`, `source-audit.json`, and private RGB audit sheets.

Twelve focused reference/coverage/leakage/download-bound tests pass. The actual
20-video reference audit passes with one group and explicit unknown duration.
Existing `ml.pipeline.evaluation` expects fully observed exact episode intervals
and cannot itself handle these coarse onset bounds, censored followup, semantic
bed exception or unreviewed actor coverage. Do not feed raw imported candidates
to it and call the result independent event precision/recall. The orchestrator
must freeze the policy crosswalk and review eligibility before baseline scoring;
source-audit counts and unit tests are not ML accuracy. Final independent test,
public-demo rights, representative safe hours and double annotation remain open.
