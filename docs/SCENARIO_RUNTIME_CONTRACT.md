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
