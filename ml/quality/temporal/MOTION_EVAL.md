# Offline Running/Zone episode evaluation readiness

This is an internal ML-only envelope and scorer. It does not extend public Event
schemas, publish alerts, execute models or establish real Running/Zone quality.
Production Running/Zone remains NOT_IMPLEMENTED. `fast_motion_candidate` is an
unvalidated configured image-plane displacement proxy, not a running classifier.

The small example files in `examples/motion_*synthetic*` are labelled
**SYNTHETIC_FIXTURE**. They contain invented annotation/evaluator cases, no real
video, acquired dataset, real person or performance benchmark. Numeric fixture
scores only test the evaluator. Actual scene GT, actor correspondence and zone
policy have not yet been provided; absent those, the scorer returns
`NOT_EVALUATED` with null metrics rather than zero accuracy.

## API and CLI

```python
from ml.quality.temporal.motion_evaluation import evaluate, wrap_prototype_result

# Versioned bindings are supplied explicitly by the caller, never guessed.
rows = wrap_prototype_result(
    prototype_result,
    source_id="SOURCE_ID", group_id="PROTECTED_SOURCE_GROUP",
    config_version="FROZEN_PROTOTYPE_CONFIG_VERSION",
    mapping_version="FROZEN_SCENARIO_MAPPING_VERSION",
    actor_by_track=reviewed_track_actor_mapping,
    zone_id="EXPLICIT_CONFIGURED_ZONE_ID",
)
report = evaluate(
    ground_truth, rows, evaluated_source_ids,
    allow_experimental_running_proxy=True,
    deadline_ms=5000,
)
```

```bash
python -m ml.quality.temporal.motion_evaluation \
  --truth ml/quality/temporal/examples/motion_gt.synthetic.json \
  --predictions ml/quality/temporal/examples/motion_predictions.synthetic.jsonl \
  --evaluated-sources ml/quality/temporal/examples/motion_evaluated_sources.synthetic.json \
  --allow-experimental-running-proxy \
  --output /tmp/motion-evaluation.synthetic.json
python -m unittest discover -s tests -p 'test_temporal_quality_motion_evaluation.py' -v
```

Without the explicit running-proxy acknowledgement, Running is NOT_EVALUATED;
Zone can still be evaluated if its annotation/polygon policy is complete. The
report never calls a proxy-versus-running-GT comparison a validated running
model. It preserves the configured scenario-to-diagnostic mapping and version.
The current explicit map is `running -> fast_motion_candidate` and
`zone_entry -> observed_polygon_entry`. Exit/direction diagnostics are not
silently reclassified as either target.

## Internal ground-truth envelope

Schema name: `motion-zone-episode-gt-v1`. Example JSON is the small executable
shape reference. Required semantics:

- Top level: annotation artifact kind, `config_version`, `mapping_version`, exact
  `scenario_to_diagnostic`, `scenes` and an explicit `episodes` list. A missing
  episode list is not a declaration of negative footage.
- Each scene/source: source ID, camera ID, source epoch, scene ID, protected group
  and split, duration on the original media clock, image size and media identity.
  Group/source copies cannot cross splits. `source_sha256=null` is used only by
  this no-media synthetic fixture; real annotation handoff requires actual hash.
- Annotation declaration: `annotation_status=ANNOTATED`, annotator identity,
  `prediction_blind_annotation=true`, complete actor census, and explicit
  `episode_annotations_complete_for`. Missing completeness is NOT_EVALUATED.
- Coverage: a complete ordered partition of the source duration into known and
  unknown windows **for each actor/scenario/zone scope**. Unknown is not safe.
  Coverage gaps or absent actor/zone scopes are NOT_EVALUATED, not implicit
  negatives. Actor-scenario milliseconds are not source-camera hours and are
  never labelled as an operational false-alarm denominator.
- Zones: explicit zone ID, original-image polygon, image geometry revision,
  provenance and rule revision. Missing polygon/site rule is NOT_EVALUATED.
  A zone ID or a floor polygon used by another rule does not supply intrusion GT.
- Track/actor bindings: source-time interval, predicted tracker key including its
  generation, GT actor ID, association revision and review provenance. Unresolved
  binding is separately unadjudicated; the evaluator does not assume tracker ID
  equals a real person. Known incorrect actor assertions are unmatched FPs.
- Episodes: source ID, actor ID, `running` or `zone_entry`, zone ID (null for the
  actor-scoped running scenario), onset lower/upper support, observed end,
  left/right censoring and known/unknown event observability. Left-censored or
  unknown episodes are unresolved, not manufactured exact-onset targets.

Running annotation must distinguish real gait/activity from walking and rapid
walking under an explicit definition. A speed threshold, filename or a source
class that combines walking/jogging/running is not that GT. Zone entry annotation
must follow a supplied site/polygon/anchor policy, active time, direction rule if
relevant and actor crossing intervals. Pixels/second are never metres/second.

## Internal prediction envelope

Predictions retain explicit source/camera/epoch/group and the matching config and
mapping versions. Every asserted episode has `prediction_episode_id`, tracker
key, reviewed/claimed actor ID, scenario, mapped diagnostic kind, zone and
geometry revision, and source-media confirmation time. The wrapper creates a
stable key from source/epoch/track/scenario/zone/episode-anchor; it does not merge
arbitrary nearby records to conceal repeated notifications.

Repeated observations of the **same logical prediction episode** count once at
its first confirmation. Reusing that episode ID with a different actor, tracker,
source, zone or configuration is rejected. Distinct prediction episode IDs
against the same single GT episode remain duplicate false assertions after
one-to-one matching. Gap/abstention records create no predicted episode and are
counted explicitly. Model gaps do not erase known GT positives or hide misses.

## Metrics and limitations

The scorer reports per-type TP/FP/FN, P/R/F1 for definite and possible onset
matching, using deterministic maximum-cardinality one-to-one matching. A point
estimate is supplied only when onset bounds agree. P is undefined with no
adjudicable predictions, R with no positive GT, and F1 uses the count definition
`2TP/(2TP+FP+FN)` when its denominator is nonzero. Unknown reference windows,
unresolved track/zone policy and censored episodes are reported separately.
Wrong known actors/zones cannot match the correct episode. An unsupported zone
geometry revision remains unresolved instead of being silently scored as a
matching physical intrusion.

An explicit census of actually processed sources is mandatory. Annotated but
unrun clips are listed, never counted as misses or true negatives. Missing real
GT/polygon/complete coverage yields NOT_EVALUATED/null, never synthetic accuracy
presented as a model baseline. The evaluated-source list must come from the run
manifest, not be inferred from the presence of alerts. Strict timely unmatched
assertions can include semantically true late or repeated alerts; the report does
not call them measured operational false alarms. Delivery latency, physical
calibration and real quality remain unestablished.

## Data Orchestrator handoff

Before a real evaluation provide:

1. Rights-cleared source videos and immutable media/timing manifest, camera/view
   identity, source/actor/session groups and frozen split. Final test must remain
   independent of threshold/model/polygon selection.
2. Prediction-blind run/walk/hard-negative activity intervals with actor IDs,
   uncertain onset/end support, explicit visibility/unknown windows, annotator
   provenance and preferably a second independent review.
3. Per-camera original-image polygon and anchor policy, geometry/rule revision,
   site/operator provenance, active intervals and directional policy. Explicitly
   annotate first-seen-inside/left-censored and occluded crossings.
4. Complete per-actor/scenario/zone coverage and an explicit episode discovery
   completeness declaration; do not turn unannotated areas into negatives.
5. Independently reviewed geometric GT-person to predicted-track association
   intervals, including generation resets/ID swaps, with association provenance.
   Do not derive actor truth from the violation assertion being scored.
6. A frozen diagnostic configuration/scenario mapping, actual processed-source
   census and saved diagnostic envelopes. Running-proxy acknowledgement is still
   required and does not turn the proxy into a validated gait classifier.

Fifteen meaningful synthetic evaluator tests cover repeated versus distinct
logical episodes, onset support, unknown coverage, model gaps, censoring,
wrong actor/zone, unresolved identity/geometry, config/source reuse and partial
processed-source census. They establish evaluation readiness only. No dataset
search/download, neural inference, GPU/LinQ operation or Fall change was made.

Non-synthetic references require each source to carry a valid 64-character lowercase SHA256; missing or malformed hashes are rejected. The synthetic fixture explicitly uses null because no media exists.
