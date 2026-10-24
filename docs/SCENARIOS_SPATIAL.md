# Runnable rules for official scenarios01/02/05/07

These are pure `evaluate(context, config) -> list[Finding]` rules using the shared internal contract in [SCENARIO_RUNTIME_CONTRACT.md](SCENARIO_RUNTIME_CONTRACT.md). They instantiate no detector, tracker, BehaviorEngine, neural backend or client. The shared engine supplies current unambiguous people/objects with previous observations, updates the existing BehaviorEngine once, and owns all dwell/episode UUID/revision/dedup/evidence/gap handling. Public EventMutation types remain unchanged. Configuration and synthetic tests establish executable predicates, not industrial recognition quality.

Owned modules are `ml/scenarios/rules/{motion,machinery,barriers,fall}.py`; scene configuration templates are `configs/scenarios/{01,02,05,07}.json`. Default policies contain no invented camera geometry. Required but unconfigured/invalid geometry or policy is BLOCKED; missing/insufficient observations are UNKNOWN. A negative means the specific observable predicate is absent in its declared scope, never that an entire frame or factory operation is safe. All outputs have exactly scenario_id,subrule,track_key,verdict,reason,score,attributes.

## 01 — Running and abrupt movement near machinery

Two distinct findings per current person:

- `running` requires one sourced current-frame `running_action` boolean fact at configured confidence. True/false supports POSITIVE/NEGATIVE; no fact, low confidence, conflicting duplicates or stale frame/time supports UNKNOWN. Image-plane speed is never relabelled running. Current action facts may come from a separately qualified classifier or explicitly labelled manual/synthetic observation; these rules contain no running classifier.
- `abrupt_in_machinery_zone` is an explicitly labelled apparent-motion prototype. It requires a declared `abrupt_movement.work_zone` polygon in original pixels, geometry_revision and policy_source; two consecutive observed confident ankle anchors and positive dt≤max_gap_ms; and explicit speed_units/threshold. Units are pixels/s or image-diagonals/s. Uncalibrated metres/s is BLOCKED. Current foot outside the declared work zone is NEGATIVE for this subrule. Inside it, configured high/low apparent displacement supports POSITIVE/NEGATIVE. This does not establish physical speed, gait, a universally valid abrupt-motion threshold, or machinery operation state. A camera-specific zone must actually represent the machinery work area before use.

## 02 — Proximity to moving machinery/transport

`moving_machine_proximity` emits exactly one finding per person, even with several objects. Machine classes are explicitly configured. Movement is either consecutive observed object translation at the declared image-diagonal threshold or a sourced current-frame `moving_state` boolean fact on the object's object_key. A first object sample without that fact is UNKNOWN; stationary translation or explicit false moving state is NEGATIVE. An explicit operation fact may describe moving mechanical parts despite a stationary object center; its source and basis remain in attributes.

Projected distance is from the current observed person foot to the object rectangle, expressed in pixels or observed person bbox heights, with an explicit policy_source/threshold. This is neither metric3D clearance nor validated physical collision risk. No metres/s or metres are invented. Relevant absent detections are UNKNOWN unless every configured machine class has explicit complete observation coverage. Such coverage is a capability declaration, not a measured detector-recall guarantee. Uncertain movement of any pair prevents a global NEGATIVE unless another pair is POSITIVE. Attributes retain evaluated object/pair evidence; a known positive takes precedence, then unknown, then all-negative.

## 05 — Three independent interactions

Each person gets separate `fence_climb`, `under_conveyor`, `under_suspended_load` findings. Each subrule needs its own original-image polygon, barrier_id, geometry_revision and policy_source. The polygon is an explicitly declared interaction scope, not a guessed2D obstruction. Foot outside it is NEGATIVE only for that configured interaction scope. Inside it, proximity, box overlap, line crossing or moving from one side to another alone is UNKNOWN.

A sourced current-frame fact uses the subrule name and a structured value:

```json
{"climbing":true,"barrier_id":"fence-1","height_or_pose_evidence":true}
```

```json
{"under":true,"barrier_id":"conveyor-1","pose_evidence":true,"operation_evidence":true}
```

```json
{"under":true,"barrier_id":"load-1","pose_evidence":true,"suspended_operation_evidence":true}
```

The fact barrier_id must match the declared geometry. The action field must be an actual boolean. An explicit false action supports NEGATIVE; a true action without all required height/pose/operation evidence is UNKNOWN. Thus a generic climbing/under keyword cannot establish a conveyor or suspended-load event. These extra visual/operation observations must be supplied by a qualified model, operator annotation or explicitly labelled synthetic fixture; no such specialist neural model is claimed here.

## 07 — Fall, prolonged lying and observable immobility

`fall.py` wraps existing own-track `suspected_fall`/`prolonged_lying` legacy events, retaining original UUID/revision/type/state and original start/confirmation times in attributes. Positive findings require open events matching the exact current camera/epoch/track. The root engine supplies active events only for tracks observed at current media time; it must not reuse an event through an observation gap. Closure due to observed upright supports NEGATIVE. With no matching legacy episode, an explicit upright posture supplied by the shared existing BehaviorEngine also supports NEGATIVE; an unknown pose remains UNKNOWN. The rule never computes its own pose. Interruption is UNKNOWN. The wrapper does not reclassify poses, instantiate another BehaviorEngine or reinterpret prolonged lying as a new fall.

Prolonged lying and immobility additionally require current **floor** evidence: either exactly current sourced `floor_observed=true` at confidence≥.5, or a declared original-image `floor_polygon` with `floor_policy_source` and `geometry_revision` and the current person bbox center inside it. Missing floor evidence is UNKNOWN; explicit current `floor_observed=false` or a center outside the declared floor region is NEGATIVE for floor-lying/immobility. A legacy lying episode with no floor policy must not label a bed or unknown support surface as floor. Templates keep all floor-policy fields null. `suspected_fall` remains a suspected observed transition and does not require or imply floor lying.

`immobility_observed` can be POSITIVE only when that same open posture event already carries `attributes.immobility_observed=true` from the existing visible-keypoint rule. Otherwise it is UNKNOWN, not an assumption of movement or consciousness. Original `immobility_since_media_ms` and `immobility_confirmed_media_ms` are retained when available, alongside legacy episode timing. The case's “признаки потери сознания” is represented only through the already observed visual state; every finding explicitly records `medical_diagnosis=false` and `consciousness_status=NOT_DETERMINABLE_FROM_VISUAL_STATE`. No medical diagnosis, unconsciousness confirmation or new Fall threshold is introduced.

## Sourced fact envelope and verification

Facts live in the optional batch.scenario_context, not in a parallel untracked stream. Shared `fact` accepts exactly one matching fact per name/track with nonempty source, finite probability score, finite JSON value, and exact original frame_id/media_time_ms. Example (explicitly synthetic):

```json
{"track_key":"camera/epoch/0/1","name":"running_action","value":true,"score":0.95,"source":"explicit-synthetic-test","frame_id":5,"media_time_ms":1000}
```

Defaults must remain blocked/unknown until source capability and camera policies are supplied. Camera/model/actor ambiguity, missing specialist observations, site policy calibration and real target-video accuracy remain release gates. None of the positive synthetic predicates proves actual video recognition, LinQ execution or real-time throughput.

Validation: `python -m unittest discover -s tests -p 'test_scenarios_spatial.py' -q` —25 synthetic tests PASS. They cover positive/negative/insufficient input for each scenario and each05 subrule, sourced fact staleness/conflicts, stationary/first-sample machinery, multi-object aggregation, missing feet/gaps, invalid geometry/uncalibrated units, own-track legacy isolation, floor/bed/unknown semantics, shared upright observation, closure/interruption, immobility timing/semantics and exact Finding keys. Root runs the complete integration suite and all8 scenario pipelines.
