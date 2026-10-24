# Internal prototype contract — eight official scenarios

This opt-in ML interface does not change ObservationBatch v1 or EventMutation v1.
The latter still accepts missing_helmet/suspected_fall/prolonged_lying only. New
scenario proposals are internal EventCandidates, written to a separate local
journal; they are not sent to Mark's existing endpoint as unsupported types.

One shared engine updates the existing BehaviorEngine once per frame. A context
contains batch (original ObservationBatch), people (current unambiguous person
detections plus track_key, previous, dt_ms), objects (current observed object
detections plus object_key, previous, dt_ms), and legacy_events from that same
BehaviorEngine update. No rule creates its own detector, tracker or LinQ client.

Each independent `evaluate(context, config)` returns Finding dictionaries:
scenario_id 01..08, subrule, track_key, verdict POSITIVE/NEGATIVE/UNKNOWN/BLOCKED,
reason, score (finite0..1 or null), attributes (finite JSON object). Shared logic
handles observed duration, gaps, episode UUID/revision, dedup and evidence. Scene
policies are camera-specific original-image geometry with provenance/revision;
unconfigured policy is BLOCKED, never an invented factory layout.

Additional sourced observations use optional batch.scenario_context:

```json
{"coverage":{"phone":"unknown"},"facts":[{"track_key":"camera/epoch/0/1","name":"running_action","value":true,"score":0.9,"source":"explicit-synthetic-test","frame_id":4,"media_time_ms":2000}]}
```

Every fact must match the exact original frame/time and track, have a source and
confidence, and be unique for that name. Manual/synthetic facts remain explicitly
labelled and cannot establish model/video quality. Missing annotation/detection
does not mean absence. Coverage declarations are observation capabilities, not a
claim of detector recall. UNKNOWN and gaps never accumulate confirmation time.

Neural stages reuse existing LinQ backends and the own Matvey admission/namespace.
No new model is selected from an export-only handoff. Specialist classes/actions,
rights/GT and camera policies remain separate gates. Current rule thresholds and
synthetic demonstrations are prototypes, not industrial accuracy or realtime.

## Freeze clarifications

For every non-synthetic fact, camera_id and stream_epoch must match the batch;
source_sha256 is mandatory when the batch has a media hash. Contradicting these
fields is rejected even in synthetic mode. Unknown object identity is not borrowed
from a different detection. All duplicate explicit object_key instances are
quarantined and coverage for those classes becomes unknown. Real sourced facts
remain classifier/manual observations, not independent GT or an implicit approved
model release. Training producers must preserve model/checkpoint provenance.

Real frame evidence is decoded sequentially by ordinal against encoded PTS and
source SHA, never accepted from an unchecked seek. Opt-in state writers acquire
the same video.lock before restoring behavior/suite state; candidate and legacy
writes share one SQLite transaction. Site policies bind camera_id and original
image_size. Mere harness presence does not establish in_use; floor lying needs
observable floor. Candidate07 support/confirmation times preserve original legacy
or visible-immobility support, while evidence names the exact observed frame.
